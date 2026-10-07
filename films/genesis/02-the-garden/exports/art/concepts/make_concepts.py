"""Thumbnail concepts for The Garden (photoreal), October 2026.

Five question-led thumbnails plus a phone-size YouTube feed mock to judge them
at the size viewers actually see. Layouts are written at 1280x720; --final
renders the chosen concepts (2 and 5) at 3840x2160 into exports/art/. Run from
anywhere:

    python3 films/genesis/02-the-garden/exports/art/concepts/make_concepts.py [--final]
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[2]
STILLS = FILM / "stills"
FONT = HERE.parents[4] / "fonts" / "Fraunces[SOFT,WONK,opsz,wght].ttf"
SANS = "/System/Library/Fonts/Avenir Next.ttc"

S = 3 if "--final" in sys.argv else 1  # layout units are 1280x720 px
W, H = 1280 * S, 720 * S


def u(n):
    return round(n * S)
CREAM = (246, 238, 220)
GOLD = (232, 182, 78)


def serif(size, weight=800):
    f = ImageFont.truetype(str(FONT), u(size))
    f.set_variation_by_axes([144, weight, 0, 0])
    return f


def sans(size, index=2):  # Avenir Next: 2 = Demi Bold
    return ImageFont.truetype(SANS, u(size), index=index)


def cover(path, box, focus=(0.5, 0.5), zoom=1.0):
    """Scale an image to fill box (w, h), cropping around focus (0..1)."""
    im = Image.open(path).convert("RGB")
    bw, bh = box
    r = max(bw / im.width, bh / im.height) * zoom
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x = min(max(round(im.width * focus[0] - bw / 2), 0), im.width - bw)
    y = min(max(round(im.height * focus[1] - bh / 2), 0), im.height - bh)
    return im.crop((x, y, x + bw, y + bh))


def grade(im, contrast=1.12, color=1.08, bright=1.0):
    im = ImageEnhance.Contrast(im).enhance(contrast)
    im = ImageEnhance.Color(im).enhance(color)
    return ImageEnhance.Brightness(im).enhance(bright)


def shade(im, side="left", strength=0.85, reach=0.6):
    """Darken one side with a smooth gradient so text reads."""
    g = Image.new("L", (W, H), 0)
    px = g.load()
    for x in range(W):
        t = x / W if side == "right" else 1 - x / W
        if side == "bottom":
            continue
        a = max(0.0, (t - (1 - reach)) / reach)
        v = round(255 * strength * a ** 1.1)
        for y in range(H):
            px[x, y] = v
    if side == "bottom":
        for y in range(H):
            a = max(0.0, (y / H - (1 - reach)) / reach)
            v = round(255 * strength * a ** 1.1)
            for x in range(W):
                px[x, y] = v
    black = Image.new("RGB", (W, H), (8, 10, 8))
    return Image.composite(black, im, g)


def vignette(im, strength=0.45):
    m = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(m)
    d.ellipse((-W * 0.25, -H * 0.3, W * 1.25, H * 1.3), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(u(160)))
    dark = ImageEnhance.Brightness(im).enhance(1 - strength)
    return Image.composite(im, dark, m)


def text(im, xy, lines, size, anchor="la", spacing=0.95, shadow=14):
    """lines: list of lines; each line is a list of (word, colour) runs."""
    font = serif(size)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d, ds = ImageDraw.Draw(layer), ImageDraw.Draw(sh)
    x0, y = u(xy[0]), u(xy[1])
    for line in lines:
        full = "".join(w for w, _ in line)
        lw = d.textlength(full, font=font)
        x = x0 - lw if anchor == "ra" else (x0 - lw / 2 if anchor == "ma" else x0)
        for word, col in line:
            ds.text((x + u(4), y + u(6)), word, font=font, fill=(0, 0, 0, 230))
            d.text((x, y), word, font=font, fill=col)
            x += d.textlength(word, font=font)
        y += u(size) * spacing
    sh = sh.filter(ImageFilter.GaussianBlur(u(shadow)))
    im = im.convert("RGBA")
    im.alpha_composite(sh)
    im.alpha_composite(sh)
    im.alpha_composite(layer)
    return im.convert("RGB")


def kicker(im, xy, label, anchor="la", colour=GOLD):
    d = ImageDraw.Draw(im)
    f = sans(30)
    x, y = u(xy[0]), u(xy[1])
    lw = d.textlength(label, font=f)
    if anchor == "ra":
        x -= lw
    d.text((x + u(2), y + u(3)), label, font=f, fill=(0, 0, 0))
    d.text((x, y), label, font=f, fill=colour)
    return im


C, G = CREAM, GOLD


def concept_temple():
    # Adam at work among the figs: "to cultivate and keep" = priestly service.
    im = grade(cover(STILLS / "movement/s037.jpg", (W, H), focus=(0.40, 0.42), zoom=1.3))
    im = vignette(shade(im, "left", 0.9, 0.62))
    im = kicker(im, (60, 150), "GENESIS 2")
    return text(im, (54, 196), [[("EDEN WAS", C)], [("A TEMPLE?", G)]], 118)


def concept_two_creations():
    # Split: Genesis 1 wide world vs Genesis 2 the one man, face to camera.
    left = grade(cover(STILLS / "movement/s004.jpg", (W // 2, H), focus=(0.5, 0.5), zoom=1.12), bright=0.8)
    right = grade(cover(STILLS / "cast/adam.jpg", (W // 2, H), focus=(0.5, 0.40), zoom=1.0))
    im = Image.new("RGB", (W, H))
    im.paste(left, (0, 0))
    im.paste(right, (W // 2, 0))
    d = ImageDraw.Draw(im)
    d.rectangle((W // 2 - u(3), 0, W // 2 + u(3), H), fill=GOLD)
    im = shade(im, "bottom", 0.85, 0.55)
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
    eve = grade(cover(STILLS / "cast/eve-b.jpg", (W // 2, H), focus=(0.5, 0.42), zoom=1.0))
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


def feed_mock(items, out):
    """Phone-width YouTube home feed: 360 px thumb, title beside a channel dot."""
    tw, th, pad = 360, 202, 18
    rowh = th + 92
    sheet = Image.new("RGB", (tw + pad * 2, pad + rowh * len(items)), (15, 15, 15))
    d = ImageDraw.Draw(sheet)
    tf, mf = sans(17, 2), sans(14, 0)
    for i, (img, title) in enumerate(items):
        y = pad + i * rowh
        sheet.paste(img.resize((tw, th), Image.LANCZOS), (pad, y))
        d.rounded_rectangle((pad + tw - 50, y + th - 26, pad + tw - 6, y + th - 6), 4, fill=(0, 0, 0))
        d.text((pad + tw - 45, y + th - 25), "11:02", font=mf, fill="white")
        d.ellipse((pad, y + th + 12, pad + 34, y + th + 46), fill=(40, 52, 44))
        words, lines, cur = title.split(), [], ""
        for w in words:
            t = (cur + " " + w).strip()
            if d.textlength(t, font=tf) > tw - 46:
                lines.append(cur)
                cur = w
            else:
                cur = t
        lines.append(cur)
        for j, ln in enumerate(lines[:2]):
            d.text((pad + 46, y + th + 10 + j * 22), ln, font=tf, fill=(241, 241, 241))
        d.text((pad + 46, y + th + 10 + min(len(lines), 2) * 22 + 2), "Makor · new", font=mf, fill=(170, 170, 170))
    sheet.save(out, quality=90)


FINAL = {"2-two-creations": "thumbnail-a", "5-dust": "thumbnail-b"}


if __name__ == "__main__":
    if S > 1:
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
    feed_mock([(old, "The Garden of Eden: Genesis 2 Read and Explained | Makor")] + made,
              HERE / "feed-mock.jpg")
