#!/usr/bin/env python3
"""
Makor audio: GPU runner (whole Bible, all voices, fast)
=======================================================

Same job as build_and_upload.py, but built for a rented cloud GPU box. It loads
the Kokoro model ONCE onto the GPU and reuses it across every study, instead of
spawning a fresh CPU process per study. On a single modern GPU this renders the
whole Bible in all four voices in roughly a day, versus weeks on a laptop CPU.

It reuses the exact text assembly, pronunciation map, R2 upload, and build-stamp
resumability from the local pipeline, so the audio it produces is identical in
content to the CPU path, and the site reads it the same way.

Setup on the box and how to run it: see GPU-RUN.md.

    python3 gpu_run.py --all
    python3 gpu_run.py --book genesis
    python3 gpu_run.py --all --voices am_michael,bf_emma

It also runs well on a Mac without a GPU: split the work into shards and run
one process per shard (about 25x real time from four shards on an M5 Max):

    for i in 1 2 3 4; do .venv/bin/python gpu_run.py --all --shard $i/4 --threads 4 & done; wait
"""

import argparse
import json
import shutil
import sys
from pathlib import Path

import generate_audio as ga
import build_and_upload as bu


def make_gpu_engine():
    """Load the torch Kokoro model once (on CUDA if present) and reuse it. The
    engine applies names/lexicon.json per voice, exactly as the local path does."""
    try:
        import torch
    except ImportError:
        sys.exit("PyTorch not installed. On the GPU box: use a PyTorch/CUDA image, or pip install torch.")
    try:
        import kokoro  # noqa: F401
    except ImportError:
        sys.exit("Kokoro (torch build) not installed. Run: pip install kokoro soundfile")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Torch device: {device}" + ("" if device == "cuda" else "  (no GPU detected: this will be slow)"))
    names = len(ga.load_names()[0]) + len(ga.load_names()[1])
    print(f"Names lexicon: {names} entries")
    return ga.make_torch_engine(device)


OFFLINE_BASE = "https://audio.makor.co.za/"


def staged_current(manifest_path, voices):
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception:
        return False
    return data.get("build") == ga.BUILD_ID and set(voices).issubset(set(data.get("voices") or {}))


def upload_staged():
    """Upload each fully rendered study in _stage (manifest last), then remove it."""
    env = bu.load_env()
    bucket = env["R2_BUCKET"]
    s3 = bu.s3_client(env)
    manifests = sorted(bu.STAGE.glob("*/*/audio/manifest.json"))
    print(f"{len(manifests)} staged studies to upload")
    for n, m in enumerate(manifests, 1):
        outdir = m.parent
        rel_study = outdir.relative_to(bu.STAGE).as_posix()
        study_path = f"studies/{rel_study}/"
        files = [p for p in sorted(outdir.rglob("*")) if p.is_file() and p.name != "manifest.json"] + [m]
        for path in files:
            key = study_path + path.relative_to(outdir).as_posix()
            ct = bu.CONTENT_TYPE.get(path.suffix.lower(), "application/octet-stream")
            s3.upload_file(str(path), bucket, key, ExtraArgs={"ContentType": ct})
        shutil.rmtree(outdir.parent, ignore_errors=True)
        print(f"[{n}/{len(manifests)}] uploaded {rel_study}")


def collect_studies(args):
    if getattr(args, "files", None):
        lines = [l.strip() for l in Path(args.files).read_text().splitlines() if l.strip()]
        return [(Path(l) if Path(l).is_absolute() else (bu.STUDIES_DIR.parents[2] / l)).resolve() for l in lines]
    if args.study:
        return [Path(args.study).resolve()]
    files = sorted(bu.STUDIES_DIR.rglob("*.json"))
    if args.book:
        want = bu.book_slug(args.book)
        files = [f for f in files if f.parent.name == want]
    return files


def main():
    ap = argparse.ArgumentParser(description="Render Makor study audio on a GPU and upload to R2.")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--all", action="store_true")
    g.add_argument("--book")
    g.add_argument("--study")
    g.add_argument("--files", help="a text file listing study JSON paths, one per line")
    g.add_argument("--upload-staged", action="store_true",
                   help="upload every finished study waiting in _stage (after an --offline render)")
    ap.add_argument("--offline", action="store_true",
                    help="render into _stage without R2 (no .env needed); upload later with --upload-staged")
    ap.add_argument("--voices", default=",".join(ga.VOICES.keys()))
    ap.add_argument("--regen", action="store_true", help="redo even if already current on R2")
    ap.add_argument("--keep-stage", action="store_true")
    ap.add_argument("--shard", default="1/1", help="k/n: render only every n-th study, starting at k")
    ap.add_argument("--threads", type=int, default=0, help="torch CPU threads per process (0 = default)")
    args = ap.parse_args()
    if args.threads:
        import torch
        torch.set_num_threads(args.threads)

    if args.upload_staged:
        return upload_staged()
    if args.offline:
        s3 = bucket = None
        base = OFFLINE_BASE
        print(f"Offline: rendering into {bu.STAGE}, nothing uploaded. Manifests point at {base}")
    else:
        env = bu.load_env()
        bucket = env["R2_BUCKET"]
        base = env["PUBLIC_BASE"].rstrip("/") + "/"
        s3 = bu.s3_client(env)
        try:
            s3.list_objects_v2(Bucket=bucket, MaxKeys=1)
        except Exception as e:
            sys.exit(f"Cannot reach R2 bucket '{bucket}' ({type(e).__name__}). Check .env and network.")

    voices = [v.strip() for v in args.voices.split(",") if v.strip()]
    overrides = ga.load_pronounce()
    exe = ga.ffmpeg_exe()
    ext = "mp3" if exe else "wav"
    if not exe:
        print("  ffmpeg not found; writing WAV. Install ffmpeg for smaller MP3 files.")

    studies = collect_studies(args)
    k, n = (int(x) for x in args.shard.split("/"))
    studies = studies[k - 1::n]
    if not studies:
        sys.exit("No studies matched.")
    print(f"{len(studies)} studies. Voices: {voices}. Loading model ...")
    synth = make_gpu_engine()

    done = made = uploaded = 0
    import time
    for i, f in enumerate(studies, 1):
        try:
            doc = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[{i}/{len(studies)}] skip unreadable {f.name}: {e}")
            continue
        bslug = bu.book_slug(doc.get("book", ""))
        slug = doc.get("section", {}).get("slug", f.stem)
        study_path = f"studies/{bslug}/{slug}/audio/"
        manifest_key = study_path + "manifest.json"

        staged = bu.STAGE / bslug / slug / "audio" / "manifest.json"
        if args.offline and not args.regen and staged_current(staged, voices):
            done += 1
            print(f"[{i}/{len(studies)}] staged already: {bslug}/{slug}")
            continue
        if not args.offline and not args.regen and bu.study_current(s3, bucket, manifest_key, voices):
            done += 1
            print(f"[{i}/{len(studies)}] current: {bslug}/{slug}")
            continue

        segments = ga.build_segments(doc, "both", overrides)
        outdir = bu.STAGE / bslug / slug / "audio"
        outdir.mkdir(parents=True, exist_ok=True)
        t0 = time.time()

        manifest = {
            "study": {"book": doc.get("book", ""), "title": doc.get("section", {}).get("title", ""),
                      "slug": slug, "passageRef": doc.get("section", {}).get("passageRef", "")},
            "audioBase": base, "studyPath": study_path, "format": ext,
            "build": ga.BUILD_ID,
            "defaultVoice": ga.DEFAULT_VOICE if ga.DEFAULT_VOICE in voices else voices[0],
            "voices": {},
        }
        try:
            for voice in voices:
                vdir = outdir / voice
                vdir.mkdir(parents=True, exist_ok=True)
                seg_wavs = []
                for s in segments:
                    wav = vdir / f"{s['id']}.wav"
                    ga.write_wav(synth(s["text"], voice), wav)
                    seg_wavs.append((s, wav))
                full_wav = vdir / "full.wav"
                full_secs = ga.concat_wavs([w for _s, w in seg_wavs], full_wav)
                import wave as _wave
                seg_meta = []
                for s, wav in seg_wavs:
                    with _wave.open(str(wav), "rb") as ww:
                        secs = ww.getnframes() / ga.SAMPLE_RATE
                    out = vdir / f"{s['id']}.{ext}"
                    if ext == "mp3":
                        ga.wav_to_mp3(exe, wav, out)
                    seg_meta.append({"id": s["id"], "label": s["label"], "kind": s["kind"],
                                     "file": f"{voice}/{s['id']}.{ext}", "seconds": round(secs, 1)})
                if ext == "mp3":
                    ga.wav_to_mp3(exe, full_wav, vdir / f"full.{ext}")
                manifest["voices"][voice] = {"label": ga.VOICES.get(voice, {}).get("label", voice),
                                             "segments": seg_meta, "full": {"file": f"{voice}/full.{ext}", "seconds": round(full_secs, 1)}}

            (outdir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

            for path in ([] if args.offline else sorted(outdir.rglob("*"))):
                if not path.is_file():
                    continue
                rel = path.relative_to(outdir).as_posix()
                key = study_path + rel
                ct = bu.CONTENT_TYPE.get(path.suffix.lower(), "application/octet-stream")
                s3.upload_file(str(path), bucket, key, ExtraArgs={"ContentType": ct})
                uploaded += 1
        except Exception as e:
            print(f"\nInterrupted at {bslug}/{slug} ({type(e).__name__}: {e}). Staged files kept. Re-run to resume.")
            break

        made += 1
        print(f"[{i}/{len(studies)}] done {bslug}/{slug} in {round(time.time()-t0)}s")
        if not args.keep_stage and not args.offline:
            shutil.rmtree(bu.STAGE / bslug / slug, ignore_errors=True)

    print(f"\nSummary: {made} rendered, {uploaded} files uploaded, {done} already current.")


if __name__ == "__main__":
    main()
