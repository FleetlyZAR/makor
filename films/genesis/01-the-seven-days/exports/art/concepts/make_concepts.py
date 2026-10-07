"""Question-led thumbnails for The Seven Days (painted), October 2026.

Added to the already uploaded video through YouTube Studio's Test & Compare (up to
three). Each question is one the film answers; see exports/youtube-pack.md.
Layouts in 1280x720 units; --final renders 3840x2160 into exports/art/.

    python3 films/genesis/01-the-seven-days/exports/art/concepts/make_concepts.py [--final]
"""
import sys
from pathlib import Path
from PIL import Image

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
    # Day One: light breaks across the deep before there is any sun (m111).
    im = grade(cover(STILLS / "s026.jpg", (W, H), focus=(0.42, 0.5), zoom=1.1), contrast=1.18)
    im = vignette(shade(im, "right", 0.75, 0.5), 0.35)
    im = kicker(im, (1280 - 62, 112), "GENESIS 1:3", anchor="ra")
    return text(im, (1280 - 56, 160), [[("LIGHT", G)], [("BEFORE", C)], [("THE SUN?", C)]], 132, anchor="ra")


def concept_sun():
    # Egypt worshipped the sun; Genesis calls it a lamp God made (m008 to m010).
    im = grade(cover(STILLS / "s010.jpg", (W, H), focus=(0.40, 0.45), zoom=1.15))
    im = vignette(shade(im, "left", 0.9, 0.6), 0.35)
    im = kicker(im, (60, 128), "GENESIS 1 VS EGYPT")
    return text(im, (54, 172), [[("THE SUN", C)], [("IS NOT", C)], [("A GOD", G)]], 128)


def concept_how_long():
    # Evenings and mornings: the days question, and the better question (m089 to m092).
    im = grade(cover(STILLS / "s057.jpg", (W, H), focus=(0.5, 0.42), zoom=1.05))
    im = vignette(shade(im, "bottom", 0.9, 0.5), 0.3)
    return text(im, (600, 470), [[("HOW ", C), ("LONG?", G)]], 170, anchor="ma")


CONCEPTS = [
    ("1-light", concept_light, "Light Before the Sun? Genesis 1 Explained, Day by Day"),
    ("2-sun", concept_sun, "What Genesis 1 Said to the Gods of Egypt and Babylon"),
    ("3-how-long", concept_how_long, "How Long Were the Seven Days? The Better Question in Genesis 1"),
]
FINAL = {"1-light": "thumbnail-q-light", "2-sun": "thumbnail-q-sun", "3-how-long": "thumbnail-q-how-long"}

if __name__ == "__main__":
    if thumbs.S > 1:
        for name, fn, _ in CONCEPTS:
            out = HERE.parent / f"{FINAL[name]}.jpg"
            img = fn()
            img.save(out, quality=88, optimize=True)
            img.resize((1280, 720), Image.LANCZOS).save(HERE.parent / f"{FINAL[name]}-preview.jpg", quality=88)
            print(out.name, img.size, f"{out.stat().st_size / 1e6:.2f} MB")
        sys.exit()
    made = []
    for name, fn, title in CONCEPTS:
        img = fn()
        img.save(HERE / f"{name}.jpg", quality=92)
        made.append((img, title))
        print(name, "|", title, f"({len(title)} chars)")
    old = Image.open(FILM / "exports/art/thumbnail-a-preview.jpg").convert("RGB")
    thumbs.feed_mock([(old, "The Seven Days of Creation: Genesis 1, Day by Day | Makor")] + made,
                     HERE / "feed-mock.jpg", "15:18")
