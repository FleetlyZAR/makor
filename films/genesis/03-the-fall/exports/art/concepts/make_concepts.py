"""Question-led photoreal thumbnails for The Fall, October 2026 (films/YOUTUBE-PLAYBOOK.md).

Three for YouTube's Test & Compare; each question is one the film answers (see
exports/youtube-pack.md). Layouts in 1280x720 units; --final renders 3840x2160 into
exports/art/ as thumbnail-q-*.jpg (the painted thumbnail-a/b stay as they are).

    python3 films/genesis/03-the-fall/exports/art/concepts/make_concepts.py [--final]
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[2]
STILLS = FILM / "stills" / "movement"
CAST = FILM.parent / "02-the-garden" / "stills" / "cast"  # Adam and Eve are cast once, in The Garden
sys.path.insert(0, str(HERE.parents[4] / "tools"))
import thumbs  # noqa: E402
from thumbs import C, G, GOLD, cover, grade, kicker, shade, text, u, vignette  # noqa: E402

if "--final" in sys.argv:
    thumbs.set_scale(3)
W, H = thumbs.W, thumbs.H


def concept_really_say():
    # The serpent's first move is a question about what God said (m006 to m008).
    left = grade(cover(STILLS / "s022.jpg", (W // 2, H), focus=(0.45, 0.4), zoom=1.2), bright=0.75)
    right = grade(cover(CAST / "eve.jpg", (W // 2, H), focus=(0.5, 0.36), zoom=1.2))
    im = Image.new("RGB", (W, H))
    im.paste(left, (0, 0))
    im.paste(right, (W // 2, 0))
    ImageDraw.Draw(im).rectangle((W // 2 - u(2), 0, W // 2 + u(2), H), fill=GOLD)
    im = vignette(shade(im, "left", 0.8, 0.55), 0.3)
    im = kicker(im, (56, 150), "GENESIS 3:1")
    return text(im, (50, 196), [[("DID GOD", C)], [("REALLY", C)], [("SAY?", G)]], 122)


def concept_where():
    # They hide among the trees He planted; God comes looking (m020 to m022).
    im = grade(cover(STILLS / "s035.jpg", (W, H), focus=(0.58, 0.58), zoom=1.3), contrast=1.15, bright=1.2)
    im = vignette(shade(im, "right", 0.75, 0.45), 0.25)
    im = kicker(im, (1280 - 60, 150), "GENESIS 3:9", anchor="ra")
    return text(im, (1280 - 54, 196), [[("WHERE", C)], [("ARE", C)], [("YOU?", G)]], 140, anchor="ra")


def concept_jesus():
    # Verse 15 narrows to one person; Adam left a garden to die, Christ rose from a garden tomb (m064 to m071).
    im = grade(cover(STILLS / "s093.jpg", (W, H), focus=(0.40, 0.5), zoom=1.2))
    im = vignette(shade(im, "left", 0.9, 0.55), 0.3)
    im = kicker(im, (56, 150), "GENESIS 3:15")
    return text(im, (50, 196), [[("JESUS IN", C)], [("GENESIS 3?", G)]], 100)


CONCEPTS = [
    ("1-really-say", concept_really_say, "Did God Really Say? How the Serpent Twisted God's Word"),
    ("2-where", concept_where, "Why Did God Ask Adam “Where Are You?” | Genesis 3 Explained"),
    ("3-jesus", concept_jesus, "The First Promise of Jesus Is in Genesis 3"),
]
FINAL = {"1-really-say": "thumbnail-q-really-say", "2-where": "thumbnail-q-where", "3-jesus": "thumbnail-q-jesus"}

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
    old = Image.open(FILM / "exports/art/thumbnail-a-1280.jpg").convert("RGB")
    thumbs.feed_mock([(old, "The Fall: Genesis 3 Read and Explained | Makor")] + made,
                     HERE / "feed-mock.jpg", "11:54")
