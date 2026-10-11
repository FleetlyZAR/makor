"""Vertical thumbnails (1080x1920) for The Seven Days v2 Short. Text sits in the middle band, which survives the
Shorts shelf crop and stays clear of the play controls. Uses the series fonts and colours (films/tools/thumbs.py).

    python3 films/genesis/01-the-seven-days-v2/exports/art/concepts/make_short_thumbs.py
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[2]
sys.path.insert(0, str(HERE.parents[4] / "tools"))
from thumbs import C, G, serif, sans  # noqa: E402

W, H = 1080, 1920


def vcover(path, focus_x):
    im = Image.open(path).convert("RGB")
    s = H / im.height
    im = im.resize((int(im.width * s), H), Image.LANCZOS)
    x = max(0, min(im.width - W, int(im.width * focus_x - W / 2)))
    im = im.crop((x, 0, x + W, H))
    im = ImageEnhance.Contrast(im).enhance(1.1)
    return ImageEnhance.Color(im).enhance(1.06)


def shade(im, y0, y1, strength=0.8):
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).rectangle([0, y0, W, y1], fill=int(255 * strength))
    m = m.filter(ImageFilter.GaussianBlur(120))
    return Image.composite(Image.new("RGB", (W, H), (6, 14, 16)), im, m)


def words(im, lines, top, size, kicker=None):
    d = ImageDraw.Draw(im)
    f = serif(size // 1)                     # thumbs.serif works in 1280x720 units at scale 1
    y = top
    if kicker:
        d.text((W // 2, y), kicker, font=sans(40), fill=G, anchor="ma")
        y += 70
    for parts in lines:
        total = sum(d.textlength(t, font=f) for t, _ in parts)
        x = W / 2 - total / 2
        for t, col in parts:
            d.text((x + 4, y + 5), t, font=f, fill=(0, 0, 0))
            d.text((x, y), t, font=f, fill=col)
            x += d.textlength(t, font=f)
        y += int(size * 0.98)
    return im


def thumb_image():
    im = vcover(FILM / "stills" / "cast" / "shot-06.jpg", 0.52)
    im = shade(im, 1050, 1500, 0.85)
    return words(im, [[("MADE IN", C)], [("GOD'S IMAGE", G)]], 1110, 128, "GENESIS 1:27")


def thumb_light():
    im = vcover(HERE / "burst-1.6.jpg", 0.5)
    im = shade(im, 1080, 1480, 0.7)
    return words(im, [[("LET THERE", C)], [("BE LIGHT", G)]], 1130, 140, "GENESIS 1:3")


if __name__ == "__main__":
    for name, fn in [("short-thumbnail-image", thumb_image), ("short-thumbnail-light", thumb_light)]:
        out = HERE.parent / f"{name}.jpg"
        fn().save(out, quality=90, optimize=True)
        print(out)


# one thumbnail per question Short (exports/shorts/<name>.mp4), saved as exports/shorts/<name>-thumbnail.jpg
M = FILM / "stills" / "movement"
QA = {
    "light": (M / "s040.jpg", 0.55, "GENESIS 1:3", [[("WHERE'S", C)], [("THE SUN?", G)]]),
    "image": (FILM / "stills" / "cast" / "shot-06.jpg", 0.52, "GENESIS 1:27", [[("MADE IN", C)], [("GOD'S IMAGE", G)]]),
    "days": (M / "s044.jpg", 0.5, "GENESIS 1", [[("HOW", C)], [("LONG?", G)]]),
    "pattern": (M / "s064.jpg", 0.45, "GENESIS 1", [[("THE HIDDEN", C)], [("PATTERN", G)]]),
    "polemic": (M / "s077.jpg", 0.62, "GENESIS 1 VS EGYPT", [[("THE SUN IS", C)], [("NOT A GOD", G)]]),
    "poem": (M / "s061.jpg", 0.5, "GENESIS 1", [[("IT'S A", C)], [("POEM", G)]]),
    "seventh": (M / "s120.jpg", 0.4, "GENESIS 2:2", [[("NO", C)], [("EVENING?", G)]]),
    "us": (M / "s098.jpg", 0.5, "GENESIS 1:26", [[("WHO IS", C)], [("“US”?", G)]]),
    "jesus": (M / "s132.jpg", 0.5, "JOHN 1:1", [[("JESUS IN", C)], [("GENESIS 1?", G)]]),
    "formless": (M / "s046.jpg", 0.5, "GENESIS 1:2", [[("TOHU", C)], [("WABOHU", G)]]),
    "sea": (M / "s080.jpg", 0.5, "GENESIS 1:21", [[("SEA", C)], [("MONSTERS?", G)]]),
    "firstpage": (M / "s145.jpg", 0.32, "REVELATION 21", [[("THE FIRST", C)], [("PAGE", G)]]),
}


def qa_thumbs():
    for name, (src, fx, kick, lines) in QA.items():
        im = shade(vcover(src, fx), 1050, 1500, 0.8)
        size = 128 if max(len("".join(t for t, _ in ln)) for ln in lines) > 8 else 150
        out = FILM / "exports" / "shorts" / f"{name}-thumbnail.jpg"
        words(im, lines, 1110, size, kick).save(out, quality=90, optimize=True)
        print(out.name)


if __name__ == "__main__":
    qa_thumbs()
