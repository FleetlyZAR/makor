#!/usr/bin/env python3
"""Render a Makor film's NARRATOR lines with the site's own narrator voice.

Same engine and settings as makor-audio: Kokoro (torch build), voice am_michael,
speed 1.0, the names lexicon markup and pronounce.json respellings, the same
quote normalisation. Lines come from the "Line list" table in the film script.
Free and offline; run it with the makor-audio venv:

    makor-audio/.venv/bin/python films/tools/narrate.py films/genesis/01-the-seven-days
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "makor-audio"))
import generate_audio as ga  # noqa: E402

VOICE = "am_michael"


def lines(script: pathlib.Path):
    for row in script.read_text().splitlines():
        m = re.match(r"\|\s*narrator/(n\d+)\.wav\s*\|\s*NARRATOR\s*\|\s*(.+?)\s*\|$", row)
        if m:
            yield m.group(1), m.group(2)


def main():
    film = pathlib.Path(sys.argv[1])
    script = film / (sys.argv[2] if len(sys.argv) > 2 else "script/day-01-script.md")
    out = film / "audio" / "narrator"
    out.mkdir(parents=True, exist_ok=True)
    overrides = ga.load_pronounce()
    engine = ga.make_torch_engine()
    for name, text in lines(script):
        spoken = text
        for a, b in ga.QUOTES.items():
            spoken = spoken.replace(a, b)
        spoken = ga.apply_pronounce(spoken, overrides)
        secs = ga.write_wav(engine(spoken, VOICE), out / f"{name}.wav")
        print(f"{name}  {secs:5.2f}s  {text}")


if __name__ == "__main__":
    main()
