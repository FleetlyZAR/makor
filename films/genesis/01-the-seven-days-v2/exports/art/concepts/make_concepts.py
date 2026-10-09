"""Question-led thumbnails for The Seven Days v2 (photoreal, the pilot), October 2026.

For YouTube Studio's Test & Compare (up to three). Each line is one the film answers; see exports/youtube-pack.md.
Built from the film's own keyframes and its Omni burst, with the shared helpers in films/tools/thumbs.py.
Layouts in 1280x720 units; --final renders 3840x2160 into exports/art/.

    python3 films/genesis/01-the-seven-days-v2/exports/art/concepts/make_concepts.py [--final]
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[2]
STILLS = FILM / "stills" / "movement"
sys.path.insert(0, str(HERE.parents[4] / "tools"))
import thumbs  # noqa: E402
from thumbs import C, G, cover, grade, kicker, shade, text, vignette  # noqa: E402

if "--final" in sys.argv:
    thumbs.set_scale(3)
W, H = thumbs.W, thumbs.H


def concept_light():
    # Day One: light races across the black deep before there is any sun (s040, Genesis 1:3).
    im = grade(cover(STILLS / "s040.jpg", (W, H), focus=(0.55, 0.5), zoom=1.08), contrast=1.15)
    im = vignette(shade(im, "left", 0.8, 0.55), 0.35)
    im = kicker(im, (62, 112), "GENESIS 1:3")
    return text(im, (56, 160), [[("LIGHT", G)], [("BEFORE", C)], [("THE SUN?", C)]], 132)


def concept_slave():
    # The first hearers: a slave in Egypt's brick pits (s022, the cold open and Day Six).
    im = grade(cover(STILLS / "s022.jpg", (W, H), focus=(0.3, 0.45), zoom=1.12), contrast=1.1)
    im = vignette(shade(im, "right", 0.93, 0.55), 0.35)
    im = kicker(im, (1280 - 62, 112), "GENESIS 1", anchor="ra")
    return text(im, (1280 - 56, 160), [[("A SLAVE", G)], [("HEARD THIS", C)], [("FIRST", C)]], 116, anchor="ra")


def concept_beginning():
    # The cold open: the word, then the burst of light (the Omni take s003 at 1.6 s).
    im = grade(cover(HERE / "burst-1.6.jpg", (W, H), focus=(0.5, 0.5), zoom=1.0), contrast=1.05, bright=0.95)
    im = vignette(shade(im, "bottom", 0.92, 0.55), 0.4)
    im = kicker(im, (640, 440), "GENESIS 1:1", anchor="ma")
    return text(im, (640, 480), [[("IN THE ", C), ("BEGINNING", G)]], 120, anchor="ma")


CONCEPTS = [
    ("1-light", concept_light, "Light Before the Sun? Genesis 1, Day by Day | Makor"),
    ("2-slave", concept_slave, "A Slave in Egypt Heard This First: Genesis 1 | Makor"),
    ("3-beginning", concept_beginning, "In the Beginning: Genesis 1 and the Seven Days of Creation | Makor"),
]
FINAL = {"1-light": "thumbnail-v2-light", "2-slave": "thumbnail-v2-slave", "3-beginning": "thumbnail-v2-beginning"}

if __name__ == "__main__":
    out_dir = HERE.parent if thumbs.S > 1 else HERE
    for name, fn, _ in CONCEPTS:
        img = fn().convert("RGB")
        out = out_dir / (f"{FINAL[name]}.jpg" if thumbs.S > 1 else f"{name}.jpg")
        img.save(out, quality=88, optimize=True)
        print(out, img.size, f"{out.stat().st_size / 1e6:.1f} MB")
