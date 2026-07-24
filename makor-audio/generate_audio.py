#!/usr/bin/env python3
"""
Makor audio pipeline (multi-voice)
==================================

Turns one Makor study JSON (schema v1.2) into narrated audio using Kokoro, a
free, Apache 2.0 open source text to speech model. It renders one file per
movement and one per Basic teaching step, plus a single whole-study track, for
each requested voice, and writes a manifest the player reads.

Backend: kokoro-onnx (no PyTorch, no system espeak). The model is loaded once
and reused across all voices.

Voices (all four by default):
    af_heart   US female, warm        am_michael US male, steady
    bf_emma    UK female, measured     bm_george  UK male, dignified

Output layout, under --outdir (default public/studies/<book>/<slug>/audio):
    af_heart/intro.mp3, af_heart/passage-01.mp3, af_heart/full.mp3, ...
    am_michael/...  bf_emma/...  bm_george/...
    manifest.json   (study meta, audioBase, and every voice's tracks)

Pronunciation: put fixes in pronounce.json next to this script, e.g.
    { "Elohim": "Eloheem", "toledot": "toh-leh-DOTE" }
They are applied to the spoken text only, never to the on-screen study.

Design note: studies are permanent, static artifacts. Generate ONCE at build
time, upload to R2, and serve static. Never synthesise on a page view.

Examples
--------
    # see the spoken text (with pronunciation fixes applied), no install needed
    python3 generate_audio.py --study sample-study/01-the-seven-days.json --dry-run

    # all four voices, WAV, listen locally
    python3 generate_audio.py --study sample-study/01-the-seven-days.json --outdir demo-audio

    # production: MP3, tagged with the R2 public base for the manifest URLs
    python3 generate_audio.py --study src/content/studies/genesis/01-the-seven-days.json \\
        --format mp3 --base https://audio.makor.co.za/
"""

import argparse
import json
import re
import subprocess
import sys
import urllib.request
import wave
from pathlib import Path

SAMPLE_RATE = 24000

ONNX_MODEL_URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx"
ONNX_VOICES_URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin"

# The four launch voices, in the order the player shows them.
VOICES = {
    "af_heart":   {"label": "US, female", "lang": "en-us"},
    "am_michael": {"label": "US, male",   "lang": "en-us"},
    "bf_emma":    {"label": "UK, female", "lang": "en-gb"},
    "bm_george":  {"label": "UK, male",   "lang": "en-gb"},
}
DEFAULT_VOICE = "am_michael"
# Bump this whenever the spoken content changes, so the uploader knows to redo
# studies whose audio was made by an older build (while staying resumable).
BUILD_ID = "v2-fullstudy"

# ---------------------------------------------------------------------------
# Text assembly (verified by --dry-run; no model needed)
# ---------------------------------------------------------------------------

LEX_TOKEN = re.compile(r"\{\{[^|}]+\|([^}]*)\}\}")   # {{elohim|God}} -> God
QUOTES = {"“": '"', "”": '"', "‘": "'", "’": "'", "—": ", ", "–": ", "}


def load_pronounce() -> dict:
    p = Path(__file__).resolve().parent / "pronounce.json"
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"  warning: could not read pronounce.json ({e}); ignoring it")
        return {}


def clean(text: str) -> str:
    text = LEX_TOKEN.sub(r"\1", text or "")
    for a, b in QUOTES.items():
        text = text.replace(a, b)
    return re.sub(r"\s+", " ", text).strip()


def apply_pronounce(text: str, overrides: dict) -> str:
    """Replace whole words (case-insensitive) with their spoken form."""
    for word, spoken in overrides.items():
        text = re.sub(rf"\b{re.escape(word)}\b", spoken, text, flags=re.IGNORECASE)
    return text


def verses_to_text(unit: dict) -> str:
    parts = [clean(v.get("text", "")) for v in unit.get("verses", [])]
    return " ".join(p for p in parts if p)


def advanced_for(key: str, study: dict) -> str:
    """The 'Go deeper' (Advanced) content for a teaching step, as spoken prose.
    Original-script characters are never included; only speakable text."""
    s = study.get("study", {})
    if key == "context":
        c = s.get("context", {}) or {}
        bits = []
        if c.get("literary"): bits.append("Literary. " + clean(c["literary"]))
        if c.get("historical"): bits.append("Historical. " + clean(c["historical"]))
        if c.get("canonical"): bits.append("Canonical. " + clean(c["canonical"]))
        return " ".join(bits)
    if key == "hermeneutics":
        h = s.get("hermeneutics", {}) or {}
        bits = []
        if h.get("authorIntent"): bits.append("The author's intent. " + clean(h["authorIntent"]))
        if h.get("descriptionVsPrescription"): bits.append("Description and prescription. " + clean(h["descriptionVsPrescription"]))
        for d in h.get("debates", []) or []:
            q = clean(d.get("question", ""))
            if q: bits.append("A question interpreters raise. " + q)
            for v in d.get("views", []) or []:
                lab, ca = clean(v.get("label", "")), clean(v.get("case", ""))
                if lab or ca: bits.append((lab + ". " + ca) if lab else ca)
            b = clean(d.get("bearing", ""))
            if b: bits.append("On balance. " + b)
        return " ".join(bits)
    if key in ("originalLanguages", "christ", "god", "oneStory"):
        return clean(s.get(key, ""))
    if key == "typology":
        out = []
        for t in s.get("typology", []) or []:
            ty, fu = clean(t.get("type", "")), clean(t.get("fulfillment", ""))
            if ty or fu: out.append((ty + ". " + fu) if ty else fu)
        return " ".join(out)
    if key == "crossReferences":
        out = []
        for c in s.get("crossReferences", []) or []:
            rf, nt = clean(c.get("ref", "")), clean(c.get("note", ""))
            if rf or nt: out.append((rf + ". " + nt) if rf else nt)
        return " ".join(out)
    return ""


def build_segments(study: dict, layer: str, overrides: dict) -> list[dict]:
    segments: list[dict] = []
    section = study.get("section", {})
    book = study.get("book", "")
    title = section.get("title", "")
    passage_ref = section.get("passageRef", "")
    thesis = clean(section.get("thesis", ""))

    intro_bits = [b for b in [f"{book}.", f"{title}.", f"{passage_ref}." if passage_ref else "", thesis] if b]
    segments.append({"id": "intro", "label": title or "Introduction", "kind": "intro",
                     "text": clean(" ".join(intro_bits))})

    if layer in ("passage", "both"):
        for i, unit in enumerate(study.get("text", {}).get("units", []), start=1):
            body = verses_to_text(unit)
            if not body:
                continue
            label = clean(unit.get("label", "")) or f"Movement {i}"
            spoken = f"{label}. {body}" if unit.get("label") else body
            segments.append({"id": f"passage-{i:02d}", "label": label, "kind": "passage", "text": spoken})

    if layer in ("basic", "both"):
        basic = study.get("study", {}).get("basic", {})
        step_titles = {
            "context": "Context", "hermeneutics": "How to read it",
            "originalLanguages": "The original words", "typology": "Patterns and shadows",
            "christ": "Christ, the point", "god": "What we learn about God",
            "crossReferences": "Cross references", "oneStory": "The one story",
        }
        for key, heading in step_titles.items():
            base_val = clean(basic.get(key, ""))
            adv = advanced_for(key, study)
            parts = [f"{heading}."]
            if base_val:
                parts.append(base_val)
            if adv:
                parts.append("Going deeper. " + adv)
            if len(parts) == 1:
                continue
            segments.append({"id": f"teaching-{key}", "label": heading, "kind": "teaching",
                             "text": " ".join(parts)})

        # Round out the full study: translation notes, then reflection questions.
        tn = []
        for n in study.get("translationNotes", []) or []:
            rf, nt = clean(n.get("ref", "")), clean(n.get("note", ""))
            if rf or nt:
                tn.append((rf + ". " + nt) if rf else nt)
        if tn:
            segments.append({"id": "teaching-translationNotes", "label": "Translation notes",
                             "kind": "teaching", "text": "Translation notes. " + " ".join(tn)})
        qs = [clean(x) for x in (study.get("questions", []) or []) if clean(x)]
        if qs:
            segments.append({"id": "questions", "label": "Questions for reflection",
                             "kind": "teaching", "text": "Questions for reflection. " + " ".join(qs)})

    if overrides:
        for s in segments:
            s["text"] = apply_pronounce(s["text"], overrides)
    return segments


# ---------------------------------------------------------------------------
# WAV + MP3 helpers
# ---------------------------------------------------------------------------

def write_wav(samples, path: Path):
    import numpy as np
    pcm = np.clip(np.asarray(samples, dtype="float32"), -1.0, 1.0)
    pcm16 = (pcm * 32767.0).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(pcm16.tobytes())
    return len(pcm16) / SAMPLE_RATE


def read_wav(path: Path):
    import numpy as np
    with wave.open(str(path), "rb") as w:
        raw = w.readframes(w.getnframes())
    return np.frombuffer(raw, dtype="<i2").astype("float32") / 32767.0


def concat_wavs(paths: list[Path], out_wav: Path, gap_seconds: float = 0.6):
    import numpy as np
    gap = np.zeros(int(SAMPLE_RATE * gap_seconds), dtype="float32")
    pieces = []
    for p in paths:
        pieces.append(read_wav(p))
        pieces.append(gap)
    full = np.concatenate(pieces) if pieces else np.zeros(1, dtype="float32")
    return write_wav(full, out_wav)


def ffmpeg_exe():
    """System ffmpeg, else the pip-installable imageio-ffmpeg binary, else None."""
    from shutil import which
    if which("ffmpeg"):
        return "ffmpeg"
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None


def wav_to_mp3(exe: str, wav_path: Path, mp3_path: Path):
    # 48 kbps mono is clear for speech and about 0.36 MB per minute.
    subprocess.run([exe, "-y", "-loglevel", "error", "-i", str(wav_path),
                    "-ac", "1", "-b:a", "48k", str(mp3_path)], check=True)
    wav_path.unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# Kokoro engine (load model once, render any voice)
# ---------------------------------------------------------------------------

def download_if_missing(url: str, dest: Path):
    if dest.exists() and dest.stat().st_size > 0:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    print(f"  downloading {dest.name} (one time) ...")
    try:
        subprocess.run(["curl", "-fL", "--retry", "3", "-o", str(dest), url], check=True)
        return
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass
    try:
        import ssl
        import certifi
        ctx = ssl.create_default_context(cafile=certifi.where())
        with urllib.request.urlopen(url, context=ctx) as r, open(dest, "wb") as f:
            f.write(r.read())
    except Exception as e:
        raise SystemExit(
            f"Could not download {dest.name}: {e}\n"
            f"Download it by hand into {dest.parent} then re-run:\n"
            f"    curl -fL -o '{dest}' {url}"
        )


def make_engine():
    """Return create(text, voice) -> float32 samples, loading the model once."""
    try:
        from kokoro_onnx import Kokoro
    except ImportError:
        Kokoro = None

    if Kokoro is not None:
        models_dir = Path(__file__).resolve().parent / "models"
        model_path = models_dir / "kokoro-v1.0.onnx"
        voices_path = models_dir / "voices-v1.0.bin"
        download_if_missing(ONNX_MODEL_URL, model_path)
        download_if_missing(ONNX_VOICES_URL, voices_path)
        ko = Kokoro(str(model_path), str(voices_path))

        def create(text: str, voice: str):
            lang = VOICES.get(voice, {}).get("lang", "en-us")
            samples, _sr = ko.create(text, voice=voice, speed=1.0, lang=lang)
            return samples
        return create

    # Fallback: torch-based kokoro (one pipeline per language)
    try:
        from kokoro import KPipeline
    except ImportError:
        sys.exit(
            "No Kokoro backend found. Install the ONNX build:\n"
            "    pip install kokoro-onnx soundfile\n"
        )
    import numpy as np
    pipes: dict[str, object] = {}

    def create(text: str, voice: str):
        code = voice[0]
        if code not in pipes:
            pipes[code] = KPipeline(lang_code=code)
        chunks = [audio for _gs, _ps, audio in pipes[code](text, voice=voice, speed=1.0)]
        return np.concatenate(chunks)
    return create


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Generate Makor study audio with Kokoro.")
    ap.add_argument("--study", required=True)
    ap.add_argument("--outdir", default=None)
    ap.add_argument("--voices", default=",".join(VOICES.keys()),
                    help="comma separated voice ids (default: all four)")
    ap.add_argument("--layer", choices=["passage", "basic", "both"], default="both")
    ap.add_argument("--format", choices=["wav", "mp3"], default="wav",
                    help="wav (no extra deps) or mp3 (needs ffmpeg or 'pip install imageio-ffmpeg')")
    ap.add_argument("--base", default="",
                    help="public base URL for the manifest (e.g. your R2 domain); empty = serve locally")
    ap.add_argument("--dry-run", action="store_true",
                    help="print spoken text and exit; no model, no setup")
    args = ap.parse_args()

    study_path = Path(args.study)
    study = json.loads(study_path.read_text(encoding="utf-8"))
    overrides = load_pronounce()
    segments = build_segments(study, args.layer, overrides)
    voices = [v.strip() for v in args.voices.split(",") if v.strip()]

    words = sum(len(s["text"].split()) for s in segments)
    print(f"Study: {study.get('book','')} - {study.get('section',{}).get('title','')}")
    print(f"Segments: {len(segments)} | words: {words} | est. minutes: {words/150:.1f} "
          f"| voices: {len(voices)}"
          + (f" | pronunciation fixes: {len(overrides)}" if overrides else "") + "\n")

    if args.dry_run:
        for s in segments:
            print(f"[{s['id']}]  ({s['kind']}, {len(s['text'].split())} words)  {s['label']}")
            print(f"    {s['text'][:280]}{'...' if len(s['text'])>280 else ''}\n")
        print("Dry run only. Re-run without --dry-run to synthesise audio.")
        return

    # Match the site's bookSlug() exactly: lower, non-alphanumerics to dashes, trim.
    book = re.sub(r"[^a-z0-9]+", "-", study.get("book", "book").lower()).strip("-")
    slug = study.get("section", {}).get("slug", study_path.stem)
    outdir = Path(args.outdir) if args.outdir else Path(f"public/studies/{book}/{slug}/audio")
    outdir.mkdir(parents=True, exist_ok=True)

    ext = args.format
    exe = None
    if ext == "mp3":
        exe = ffmpeg_exe()
        if not exe:
            print("  no ffmpeg found; run 'pip install imageio-ffmpeg' for MP3. Falling back to WAV.\n")
            ext = "wav"

    engine = make_engine()

    manifest = {
        "study": {"book": study.get("book", ""), "title": study.get("section", {}).get("title", ""),
                  "slug": slug, "passageRef": study.get("section", {}).get("passageRef", "")},
        "audioBase": args.base,                 # empty => player resolves next to manifest
        "studyPath": f"studies/{book}/{slug}/audio/",
        "format": ext,
        "build": BUILD_ID,
        "defaultVoice": DEFAULT_VOICE if DEFAULT_VOICE in voices else voices[0],
        "voices": {},
    }

    for voice in voices:
        vdir = outdir / voice
        vdir.mkdir(parents=True, exist_ok=True)
        print(f"Voice {voice} ({VOICES.get(voice,{}).get('label','?')})")
        seg_wavs = []
        for s in segments:
            wav = vdir / f"{s['id']}.wav"
            print(f"  synth {s['id']} ({s['label']}) ...")
            dur = write_wav(engine(s["text"], voice), wav)
            seg_wavs.append((s, wav, dur))

        full_wav = vdir / "full.wav"
        full_secs = concat_wavs([w for _s, w, _d in seg_wavs], full_wav)

        seg_meta = []
        for s, wav, dur in seg_wavs:
            out = vdir / f"{s['id']}.{ext}"
            if ext == "mp3":
                wav_to_mp3(exe, wav, out)
            seg_meta.append({"id": s["id"], "label": s["label"], "kind": s["kind"],
                             "file": f"{voice}/{s['id']}.{ext}", "seconds": round(dur, 1)})
        if ext == "mp3":
            wav_to_mp3(exe, full_wav, vdir / f"full.{ext}")

        manifest["voices"][voice] = {
            "label": VOICES.get(voice, {}).get("label", voice),
            "segments": seg_meta,
            "full": {"file": f"{voice}/full.{ext}", "seconds": round(full_secs, 1)},
        }

    (outdir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"\nDone. {len(voices)} voices x {len(segments)} segments written to {outdir}")
    print(f"Manifest: {outdir/'manifest.json'}")


if __name__ == "__main__":
    main()
