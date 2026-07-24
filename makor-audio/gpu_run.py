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
"""

import argparse
import json
import shutil
import sys
from pathlib import Path

import generate_audio as ga
import build_and_upload as bu


def make_gpu_engine():
    """Load the torch Kokoro model once (on CUDA if present) and reuse it."""
    try:
        import torch
    except ImportError:
        sys.exit("PyTorch not installed. On the GPU box: use a PyTorch/CUDA image, or pip install torch.")
    try:
        from kokoro import KPipeline
    except ImportError:
        sys.exit("Kokoro (torch build) not installed. Run: pip install kokoro soundfile")
    import numpy as np

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Torch device: {device}" + ("" if device == "cuda" else "  (no GPU detected: this will be slow)"))
    pipes = {}

    def synth(text, voice):
        code = voice[0]  # 'a' US, 'b' UK
        if code not in pipes:
            try:
                pipes[code] = KPipeline(lang_code=code, device=device)
            except TypeError:
                pipes[code] = KPipeline(lang_code=code)
        chunks = []
        for _g, _p, audio in pipes[code](text, voice=voice, speed=1.0):
            a = audio.detach().cpu().numpy() if hasattr(audio, "detach") else np.asarray(audio)
            chunks.append(a.astype("float32"))
        return np.concatenate(chunks) if chunks else np.zeros(1, dtype="float32")

    return synth


def collect_studies(args):
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
    ap.add_argument("--voices", default=",".join(ga.VOICES.keys()))
    ap.add_argument("--regen", action="store_true", help="redo even if already current on R2")
    ap.add_argument("--keep-stage", action="store_true")
    args = ap.parse_args()

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

        if not args.regen and bu.study_current(s3, bucket, manifest_key, voices):
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

            for path in sorted(outdir.rglob("*")):
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
        if not args.keep_stage:
            shutil.rmtree(bu.STAGE / bslug / slug, ignore_errors=True)

    print(f"\nSummary: {made} rendered, {uploaded} files uploaded, {done} already current.")


if __name__ == "__main__":
    main()
