"""GUIDE lines for The Garden in a minute (script/one-minute-script.md), rendered with the
films narrator engine (Kokoro am_michael). Free and offline:

    makor-audio/.venv/bin/python films/genesis/02-the-garden/edit/short_guide.py
"""
import pathlib, sys
ROOT = pathlib.Path.home() / "makor"
sys.path.insert(0, str(ROOT / "films" / "tools"))
import narrate
ga = narrate.ga
out = ROOT / "films/genesis/02-the-garden/audio/short"
G = {
 "g1": "Genesis two gives the world a centre: a garden where God dwells with the people He made.",
 "g2": "Formed is the potter's verb. We are dust that breathes, because He breathed.",
 "g3": "Helper is ezer, a word used most often of God Himself. Not someone lesser: his match.",
 "g4": "Chapter three damages every gift. The Bible's last pages restore them: God at home with His people.",
}
ov = ga.load_pronounce(); eng = ga.make_torch_engine()
for k, t in G.items():
    s = t
    for a, b in ga.QUOTES.items(): s = s.replace(a, b)
    s = ga.apply_pronounce(s, ov)
    print(k, f"{ga.write_wav(eng(s, narrate.VOICE), out / f'{k}.wav'):.2f}s", t)
