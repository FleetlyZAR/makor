"""Thumbnail concepts for The Garden (photoreal), October 2026.

Five question-led thumbnails plus a phone-size YouTube feed mock to judge them
at the size viewers actually see. Layouts are written at 1280x720; --final
renders the chosen concepts (2 and 5) at 3840x2160 into exports/art/. Run from
anywhere:

    python3 films/genesis/02-the-garden/exports/art/concepts/make_concepts.py [--final]
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[2]
STILLS = FILM / "stills"
sys.path.insert(0, str(HERE.parents[4] / "tools"))
import thumbs  # noqa: E402
from thumbs import C, G, GOLD, cover, grade, kicker, shade, text, u, vignette  # noqa: E402

if "--final" in sys.argv:
    thumbs.set_scale(3)
W, H = thumbs.W, thumbs.H


def concept_temple():
    # Adam at work among the figs: "to cultivate and keep" = priestly service.
    im = grade(cover(STILLS / "movement/s037.jpg", (W, H), focus=(0.40, 0.42), zoom=1.3))
    im = vignette(shade(im, "left", 0.9, 0.62))
    im = kicker(im, (60, 150), "GENESIS 2")
    return text(im, (54, 196), [[("EDEN WAS", C)], [("A TEMPLE?", G)]], 118)


def concept_two_creations():
    # Split: Genesis 1 wide world vs Genesis 2 the one man, face to camera.
    left = grade(cover(STILLS / "movement/s004.jpg", (W // 2, H), focus=(0.5, 0.5), zoom=1.12), bright=0.8)
    right = grade(cover(STILLS / "cast/adam.jpg", (W // 2, H), focus=(0.5, 0.42), zoom=1.06))
    im = Image.new("RGB", (W, H))
    im.paste(left, (0, 0))
    im.paste(right, (W // 2, 0))
    d = ImageDraw.Draw(im)
    d.rectangle((W // 2 - u(3), 0, W // 2 + u(3), H), fill=GOLD)
    im = shade(shade(im, "bottom", 0.85, 0.55), "bottom", 0.9, 0.22)  # second pass sinks the shoulder cloth
    im = kicker(im, (40, 36), "GENESIS 1", colour=C)
    im = kicker(im, (1280 - 40, 36), "GENESIS 2", anchor="ra", colour=C)
    return text(im, (640 - 30, 500), [[("TWO", G), (" CREATIONS?", C)]], 112, anchor="ma")


def concept_not_good():
    # Adam alone under the fig, the first thing in the Bible called "not good".
    im = grade(cover(STILLS / "movement/s047.jpg", (W, H), focus=(0.52, 0.5), zoom=1.7))
    im = vignette(shade(im, "right", 0.9, 0.6), 0.5)
    im = kicker(im, (1280 - 60, 150), "THE FIRST THING GOD CALLED", anchor="ra", colour=C)
    return text(im, (1280 - 54, 196), [[("“NOT", G)], [("GOOD”", G)]], 168, anchor="ra")


def concept_helper():
    # Face to face: kenegdo, "one who stands face to face with him, his match".
    adam = grade(cover(STILLS / "cast/adam.jpg", (W // 2, H), focus=(0.5, 0.42), zoom=1.0))
    eve = grade(cover(STILLS / "cast/eve.jpg", (W // 2, H), focus=(0.5, 0.42), zoom=1.0))
    im = Image.new("RGB", (W, H))
    im.paste(adam, (0, 0))
    im.paste(eve, (W // 2, 0))
    im = vignette(shade(im, "bottom", 0.92, 0.5), 0.35)
    return text(im, (640 - 40, 500), [[("“HELPER”", G), ("?", C)]], 136, anchor="ma")


def concept_dust():
    # The first breath: the man lying in the grass, eyes closed.
    im = grade(cover(STILLS / "movement/s016.jpg", (W, H), focus=(0.3, 0.55), zoom=1.7))
    im = vignette(shade(im, "right", 0.88, 0.55), 0.4)
    im = kicker(im, (1280 - 64, 120), "GENESIS 2:7", anchor="ra")
    return text(im, (1280 - 56, 170), [[("WHY", C)], [("DUST?", G)]], 190, anchor="ra")


CONCEPTS = [
    ("1-temple", concept_temple,
     "Was the Garden of Eden the First Temple? | Genesis 2 Explained"),
    ("2-two-creations", concept_two_creations,
     "Genesis 1 vs Genesis 2: Are There Two Creation Stories?"),
    ("3-not-good", concept_not_good,
     "The First Thing God Called “Not Good” | Genesis 2 Explained"),
    ("4-helper", concept_helper,
     "Was Eve Made to Serve Adam? What “Helper” Means in Hebrew"),
    ("5-dust", concept_dust,
     "Why Did God Make Adam from Dust? | Genesis 2 Explained"),
]


FINAL = {"2-two-creations": "thumbnail-a", "5-dust": "thumbnail-b"}


if __name__ == "__main__":
    if thumbs.S > 1:
        for name, fn, title in CONCEPTS:
            if name in FINAL:
                out = HERE.parent / f"{FINAL[name]}.jpg"
                img = fn()
                img.save(out, quality=88, optimize=True)
                img.resize((1280, 720), Image.LANCZOS).save(
                    HERE.parent / f"{FINAL[name]}-preview.jpg", quality=88)
                print(out.name, img.size, f"{out.stat().st_size / 1e6:.2f} MB")
        sys.exit()
    made = []
    for name, fn, title in CONCEPTS:
        img = fn()
        img.save(HERE / f"{name}.jpg", quality=92)
        made.append((img, title))
        print(name, "|", title, f"({len(title)} chars)")
    old = Image.open(FILM / "exports/art/painted/thumbnail-a-preview.jpg").convert("RGB")
    thumbs.feed_mock([(old, "The Garden of Eden: Genesis 2 Read and Explained | Makor")] + made,
                     HERE / "feed-mock.jpg", "11:02")
