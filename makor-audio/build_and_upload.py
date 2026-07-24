#!/usr/bin/env python3
"""
Makor audio: bulk, resumable generate + upload to Cloudflare R2
===============================================================

For each study JSON it: (1) checks R2 to see if that study is already done and
skips it, (2) otherwise renders all four voices to a local staging folder,
(3) uploads every file to R2 with the right content type, (4) deletes the local
staging to save disk. Because step 1 checks R2, you can stop this at any time
(close the lid, a crash, Ctrl+C) and just run it again: it picks up where it
left off.

Setup (one time):
    pip install boto3
    fill in makor-audio/.env  (R2 keys, endpoint, bucket, public base)

Run:
    cd makor-audio
    python3 build_and_upload.py --book genesis        # one book first
    python3 build_and_upload.py --all                 # the whole Bible
    python3 build_and_upload.py --study ../src/content/studies/ruth/01-naomi-and-ruth.json
    python3 build_and_upload.py --all --regen         # force re-render even if present

The site reads audio from the same paths this uploads to, so once a study is
uploaded its player appears on the live site automatically.
"""

import argparse
import json
import mimetypes
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STUDIES_DIR = (HERE / ".." / "src" / "content" / "studies").resolve()
STAGE = HERE / "_stage"

CONTENT_TYPE = {".mp3": "audio/mpeg", ".json": "application/json",
                ".wav": "audio/wav", ".ogg": "audio/ogg"}


def load_env() -> dict:
    env = {}
    envfile = HERE / ".env"
    if not envfile.exists():
        sys.exit("Missing makor-audio/.env . Fill it in first (see the file for keys).")
    for line in envfile.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip()
    missing = [k for k in ("R2_ACCESS_KEY_ID", "R2_SECRET_ACCESS_KEY", "R2_ENDPOINT", "R2_BUCKET", "PUBLIC_BASE") if not env.get(k)]
    if missing:
        sys.exit("makor-audio/.env is missing values for: " + ", ".join(missing))
    return env


def book_slug(book: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", str(book).lower()).strip("-")


def s3_client(env):
    try:
        import boto3
        from botocore.config import Config
    except ImportError:
        sys.exit("boto3 not installed. Run:  pip install boto3")
    # Adaptive retries absorb brief network blips; timeouts keep it from hanging.
    cfg = Config(retries={"max_attempts": 10, "mode": "adaptive"},
                 connect_timeout=15, read_timeout=120)
    return boto3.client(
        "s3",
        endpoint_url=env["R2_ENDPOINT"],
        aws_access_key_id=env["R2_ACCESS_KEY_ID"],
        aws_secret_access_key=env["R2_SECRET_ACCESS_KEY"],
        region_name="auto",
        config=cfg,
    )


def already_done(s3, bucket, key):
    import botocore
    try:
        s3.head_object(Bucket=bucket, Key=key)
        return True
    except botocore.exceptions.ClientError:
        return False


def remote_size(s3, bucket, key):
    import botocore
    try:
        return s3.head_object(Bucket=bucket, Key=key)["ContentLength"]
    except botocore.exceptions.ClientError:
        return None


def collect_studies(args):
    if args.study:
        return [Path(args.study).resolve()]
    files = sorted(STUDIES_DIR.rglob("*.json"))
    if args.book:
        want = book_slug(args.book)
        files = [f for f in files if f.parent.name == want]
    return files


def main():
    ap = argparse.ArgumentParser(description="Bulk, resumable Makor audio generate + upload to R2.")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--all", action="store_true", help="every study in the repo")
    g.add_argument("--book", help="one book folder, e.g. genesis or '1-samuel'")
    g.add_argument("--study", help="a single study JSON path")
    ap.add_argument("--voices", default="af_heart,am_michael,bf_emma,bm_george")
    ap.add_argument("--regen", action="store_true", help="re-render and re-upload even if already on R2")
    ap.add_argument("--keep-stage", action="store_true", help="do not delete local staging after upload")
    args = ap.parse_args()

    env = load_env()
    bucket = env["R2_BUCKET"]
    s3 = s3_client(env)
    studies = collect_studies(args)
    if not studies:
        sys.exit("No studies matched.")

    # Fail clearly up front if R2 is unreachable, rather than mid-run.
    try:
        s3.list_objects_v2(Bucket=bucket, MaxKeys=1)
    except Exception as e:
        sys.exit(f"Cannot reach R2 bucket '{bucket}' ({type(e).__name__}). "
                 f"Check your internet and the .env values, then re-run.")

    print(f"{len(studies)} studies to consider. Voices: {args.voices}\n")
    done_skipped = generated = uploaded_files = 0

    for i, f in enumerate(studies, 1):
        try:
            doc = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[{i}/{len(studies)}] SKIP unreadable {f.name}: {e}")
            continue
        bslug = book_slug(doc.get("book", ""))
        slug = doc.get("section", {}).get("slug", f.stem)
        study_path = f"studies/{bslug}/{slug}/audio/"
        manifest_key = study_path + "manifest.json"

        try:
            if not args.regen and already_done(s3, bucket, manifest_key):
                done_skipped += 1
                print(f"[{i}/{len(studies)}] done already: {bslug}/{slug}")
                continue
        except Exception as e:
            print(f"\nLost connection to R2 ({type(e).__name__}). Stopping cleanly.\n"
                  f"Reconnect to the internet and re-run the same command to resume.")
            break

        outdir = STAGE / bslug / slug / "audio"
        print(f"[{i}/{len(studies)}] rendering {bslug}/{slug} ...")
        r = subprocess.run(
            [sys.executable, str(HERE / "generate_audio.py"),
             "--study", str(f), "--outdir", str(outdir),
             "--voices", args.voices, "--format", "mp3", "--base", env["PUBLIC_BASE"]],
            cwd=str(HERE),
        )
        if r.returncode != 0:
            print(f"    generation failed for {bslug}/{slug}; leaving it for a re-run and moving on")
            continue
        generated += 1

        # Upload every file under outdir, preserving structure under study_path.
        # Manifest.json sorts last, so it lands only after all audio: a study is
        # never marked done half-uploaded.
        try:
            for path in sorted(outdir.rglob("*")):
                if not path.is_file():
                    continue
                rel = path.relative_to(outdir).as_posix()
                key = study_path + rel
                size = path.stat().st_size
                if not args.regen and remote_size(s3, bucket, key) == size:
                    continue
                ct = CONTENT_TYPE.get(path.suffix.lower()) or mimetypes.guess_type(path.name)[0] or "application/octet-stream"
                s3.upload_file(str(path), bucket, key, ExtraArgs={"ContentType": ct})
                uploaded_files += 1
        except Exception as e:
            print(f"\nUpload interrupted at {bslug}/{slug} ({type(e).__name__}). Stopping cleanly.\n"
                  f"This study was not finished; staged files kept. Reconnect and re-run to resume.")
            break
        print(f"    uploaded {bslug}/{slug}")

        if not args.keep_stage:
            shutil.rmtree(STAGE / bslug / slug, ignore_errors=True)

    print(f"\nSummary: {generated} rendered, {uploaded_files} files uploaded, "
          f"{done_skipped} already done and skipped.")
    print("Safe to re-run any time; finished studies are skipped.")


if __name__ == "__main__":
    main()
