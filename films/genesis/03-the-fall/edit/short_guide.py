"""GUIDE lines for The Fall in a minute (script/one-minute-script.md), rendered with the
films narrator engine (Kokoro am_michael). Free and offline:

    makor-audio/.venv/bin/python films/genesis/03-the-fall/edit/short_guide.py
"""
import pathlib, sys
ROOT = pathlib.Path.home() / "makor"
sys.path.insert(0, str(ROOT / "films" / "tools"))
import narrate
ga = narrate.ga
out = ROOT / "films/genesis/03-the-fall/audio/short"
G = {
 "g1": "If the world began so good, why is it like this? Genesis three answers.",
 "g2": "The serpent contradicts God word for word. The root of sin is not ignorance, but distrust.",
 "g3": "God comes looking for the guilty. And before He sentences the man and the woman, He makes a promise.",
 "g4": "The first announcement of the gospel: the seed of the woman will crush the serpent.",
 "g5": "And God covers their shame. In Christ, He still does.",
}
ov = ga.load_pronounce(); eng = ga.make_torch_engine()
for k, t in G.items():
    s = t
    for a, b in ga.QUOTES.items(): s = s.replace(a, b)
    s = ga.apply_pronounce(s, ov)
    print(k, f"{ga.write_wav(eng(s, narrate.VOICE), out / f'{k}.wav'):.2f}s", t)
