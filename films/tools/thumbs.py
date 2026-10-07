"""Shared drawing helpers for question-led YouTube thumbnails (films/YOUTUBE-PLAYBOOK.md).

Layouts are written in 1280x720 units; call set_scale(3) before drawing to render
the same layout at 3840x2160. Each film keeps its own concepts script in
exports/art/concepts/make_concepts.py and imports this module.
"""
import pathlib

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

FONT = pathlib.Path(__file__).resolve().parents[1] / "fonts" / "Fraunces[SOFT,WONK,opsz,wght].ttf"
SANS = "/System/Library/Fonts/Avenir Next.ttc"
CREAM = (246, 238, 220)
GOLD = (232, 182, 78)
C, G = CREAM, GOLD

S = 1
W, H = 1280, 720


def set_scale(s):
    global S, W, H
    S, W, H = s, 1280 * s, 720 * s


def u(n):
    return round(n * S)


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
    """Darken one side (left, right or bottom) with a smooth gradient so text reads."""
    n = H if side == "bottom" else W
    ramp = []
    for i in range(n):
        t = i / n if side in ("right", "bottom") else 1 - i / n
        a = max(0.0, (t - (1 - reach)) / reach)
        ramp.append(round(255 * strength * a ** 1.1))
    strip = Image.new("L", (1, n) if side == "bottom" else (n, 1))
    strip.putdata(ramp)
    g = strip.resize((W, H))
    return Image.composite(Image.new("RGB", (W, H), (8, 10, 8)), im, g)


def vignette(im, strength=0.45):
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).ellipse((-W * 0.25, -H * 0.3, W * 1.25, H * 1.3), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(u(160)))
    return Image.composite(im, ImageEnhance.Brightness(im).enhance(1 - strength), m)


def text(im, xy, lines, size, anchor="la", spacing=0.95, shadow=14):
    """lines: list of lines; each line is a list of (word, colour) runs.
    xy in layout units; anchor la (left), ra (right) or ma (centre)."""
    font = serif(size)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d, ds = ImageDraw.Draw(layer), ImageDraw.Draw(sh)
    x0, y = u(xy[0]), u(xy[1])
    for line in lines:
        lw = d.textlength("".join(w for w, _ in line), font=font)
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
    if anchor == "ra":
        x -= d.textlength(label, font=f)
    d.text((x + u(2), y + u(3)), label, font=f, fill=(0, 0, 0))
    d.text((x, y), label, font=f, fill=colour)
    return im


def feed_mock(items, out, duration):
    """Phone-width YouTube home feed: 360 px thumbs with titles, duration badge bottom right."""
    tw, th, pad = 360, 202, 18
    rowh = th + 92
    sheet = Image.new("RGB", (tw + pad * 2, pad + rowh * len(items)), (15, 15, 15))
    d = ImageDraw.Draw(sheet)
    tf = ImageFont.truetype(SANS, 17, index=2)
    mf = ImageFont.truetype(SANS, 14, index=0)
    for i, (img, title) in enumerate(items):
        y = pad + i * rowh
        sheet.paste(img.resize((tw, th), Image.LANCZOS), (pad, y))
        d.rounded_rectangle((pad + tw - 50, y + th - 26, pad + tw - 6, y + th - 6), 4, fill=(0, 0, 0))
        d.text((pad + tw - 45, y + th - 25), duration, font=mf, fill="white")
        d.ellipse((pad, y + th + 12, pad + 34, y + th + 46), fill=(40, 52, 44))
        lines, cur = [], ""
        for w in title.split():
            t = (cur + " " + w).strip()
            if d.textlength(t, font=tf) > tw - 46:
                lines.append(cur)
                cur = w
            else:
                cur = t
        lines.append(cur)
        for j, ln in enumerate(lines[:2]):
            d.text((pad + 46, y + th + 10 + j * 22), ln, font=tf, fill=(241, 241, 241))
        d.text((pad + 46, y + th + 12 + min(len(lines), 2) * 22), "Makor", font=mf, fill=(170, 170, 170))
    sheet.save(out, quality=90)
