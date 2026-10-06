#!/usr/bin/env python3
"""Render every spoken line of a movement film from script/movement-lines.json.

  READER and GOD: ElevenLabs (voices and model from films/VOICES.md)
  GUIDE:          Kokoro am_michael through makor-audio, with the names lexicon
                  plus the film level pronunciations below

One file per line in audio/movement/, resumable (existing files are skipped),
durations written to script/movement-durations.json. ElevenLabs credits are
logged once per run in COSTS-movement.md. Run with the makor-audio venv:

    makor-audio/.venv/bin/python films/tools/movement_voice.py films/genesis/01-the-seven-days
"""
import json, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "makor-audio"))
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from clip import log_cost  # noqa: E402
from voice import USD_PER_CREDIT, TTS_MODEL, VOICES, key, post  # noqa: E402

# Words the GUIDE says that the Makor names lexicon does not cover yet
# (misaki phoneme markup, US forms, in the lexicon's own style).
FILM_NAMES = {"Marduk": "mˈɑɹdʊk", "tohu": "tˈOhu", "wabohu": "vɑbˈOhu", "tselem": "tsˈɛlɛm"}


def dur(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                 str(path)], capture_output=True, text=True).stdout)


def main():
    film = pathlib.Path(sys.argv[1])
    lines = json.loads((film / "script" / "movement-lines.json").read_text())
    out = film / "audio" / "movement"
    out.mkdir(parents=True, exist_ok=True)
    dfile = film / "script" / "movement-durations.json"
    durs = json.loads(dfile.read_text()) if dfile.exists() else {}
    k, engine, ga, credits = None, None, None, 0
    for ln in lines:
        sp, lid, text = ln["speaker"], ln["id"], ln["text"]
        dest = out / f"{lid}-{sp.lower()}.{'wav' if sp == 'GUIDE' else 'mp3'}"
        if not dest.exists():
            if sp == "GUIDE":
                if engine is None:
                    import generate_audio as ga
                    engine, overrides = ga.make_torch_engine(), ga.load_pronounce()
                spoken = text
                for a, b in ga.QUOTES.items():
                    spoken = spoken.replace(a, b)
                spoken = ga.apply_pronounce(spoken, overrides)
                for word, ph in FILM_NAMES.items():
                    spoken = spoken.replace(word, f"[{word}](/{ph}/)")
                ga.write_wav(engine(spoken, "am_michael"), dest)
            else:
                k = k or key()
                vid, speed = VOICES[sp if sp == "GOD" else "NARRATOR"]
                audio = post(f"/text-to-speech/{vid}?output_format=mp3_44100_192",
                             {"text": text, "model_id": TTS_MODEL, "voice_settings": {"speed": speed}}, k, raw=True)
                dest.write_bytes(audio)
                credits += len(text)
        durs[lid] = round(dur(dest), 3)
        print(f"{lid} {sp:6s} {durs[lid]:6.2f}s  {text[:70]}")
        dfile.write_text(json.dumps(durs, indent=1))
    if credits:
        log_cost(film, f"ElevenLabs TTS ({TTS_MODEL})", "movement READER and GOD lines",
                 f"{credits} credits", credits * USD_PER_CREDIT, log="COSTS-movement.md")
    print(f"done: {len(lines)} lines, {credits} ElevenLabs credits this run, "
          f"{sum(durs.values()) / 60:.1f} min of speech")


if __name__ == "__main__":
    main()
