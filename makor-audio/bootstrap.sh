#!/usr/bin/env bash
# One-command setup for a rented GPU box (see GPU-RUN.md).
# Run from the repo root after cloning and creating makor-audio/.env:
#     bash makor-audio/bootstrap.sh
# It installs system + python deps and starts the full render + upload to R2.
set -euo pipefail

cd "$(dirname "$0")"

if [ ! -f .env ]; then
  echo "Missing makor-audio/.env . Create it first (R2 keys). Stopping." >&2
  exit 1
fi

echo "== installing system deps (espeak-ng, ffmpeg) =="
apt-get update -y && apt-get install -y espeak-ng ffmpeg

echo "== installing python deps (kokoro, soundfile, boto3) =="
pip install --quiet kokoro soundfile boto3

echo "== GPU check =="
python3 - <<'PY'
try:
    import torch
    print("CUDA available:", torch.cuda.is_available(),
          "|", (torch.cuda.get_device_name(0) if torch.cuda.is_available() else "no GPU"))
except Exception as e:
    print("torch not importable:", e)
PY

echo "== rendering the whole Bible, all voices, and uploading to R2 =="
python3 gpu_run.py --all
