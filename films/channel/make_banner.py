"""YouTube channel banner for Makor (2560 x 1440).

Everything that must be seen sits inside YouTube's all-device safe area
(1546 x 423, centred). The outer stills only show on desktop and TV.
Run: python3 films/channel/make_banner.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

ROOT = Path(__file__).resolve().parents[1]
STILLS = ROOT / "genesis/02-the-garden-v2/stills/movement"
FONT = str(ROOT / "fonts/Fraunces[SOFT,WONK,opsz,wght].ttf")
OUT = Path(__file__).resolve().parent

W, H = 2560, 1440
INK, WATER, GOLD, CREAM = (14, 42, 46), (15, 108, 108), (184, 134, 47), (244, 236, 220)
SAFE = ((W - 1546) // 2, (H - 423) // 2, (W + 1546) // 2, (H + 423) // 2)

BACKGROUND = "s188.jpg"            # the garden river in morning light
# (still, focus x 0..1) from the centre outward; first pair sits inside the safe area
LEFT = [("s148.jpg", 0.24), ("s010.jpg", 0.5), ("s145.jpg", 0.5)]   # Adam, lion, light in the trees
RIGHT = [("s149.jpg", 0.45), ("s013.jpg", 0.5), ("s075.jpg", 0.5)]  # Eve, the meeting hands, river
PW, PH, GAP = 330, 400, 24
TEXT_HALF = 390


def font(size, wght=500, opsz=None):
    f = ImageFont.truetype(FONT, size)
    try:
        f.set_variation_by_axes([opsz or min(144, size), wght, 50, 0])
    except Exception:
        pass
    return f


def cover(im, w, h, fx=0.5, fy=0.5):
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = round((im.width - w) * fx); y = round((im.height - h) * fy)
    return im.crop((x, y, x + w, y + h))


def panel(name, fx, dim):
    im = cover(Image.open(STILLS / name).convert("RGB"), PW, PH, fx, 0.45)
    if dim < 1:
        im = ImageEnhance.Brightness(im).enhance(dim)
    mask = Image.new("L", (PW, PH), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, PW - 1, PH - 1), 14, fill=255)
    return im, mask


def main():
    bg = cover(Image.open(STILLS / BACKGROUND).convert("RGB"), W, H, 0.5, 0.55)
    bg = bg.filter(ImageFilter.GaussianBlur(5))
    bg = Image.blend(bg, Image.new("RGB", (W, H), INK), 0.62)
    canvas = bg.copy()

    top = (H - PH) // 2
    cx = W // 2
    for side, items in ((-1, LEFT), (1, RIGHT)):
        for i, (name, fx) in enumerate(items):
            inner = cx + side * (TEXT_HALF + GAP + i * (PW + GAP))
            x = inner if side > 0 else inner - PW
            im, mask = panel(name, fx, 1.0 - 0.18 * i)
            # soft shadow, then gold hairline
            sh = Image.new("L", (W, H), 0)
            ImageDraw.Draw(sh).rounded_rectangle((x, top + 10, x + PW, top + PH + 10), 16, fill=150)
            canvas.paste(Image.new("RGB", (W, H), (0, 0, 0)), (0, 0), sh.filter(ImageFilter.GaussianBlur(18)))
            canvas.paste(im, (x, top), mask)
            ImageDraw.Draw(canvas).rounded_rectangle((x, top, x + PW - 1, top + PH - 1), 14,
                                                     outline=GOLD + (0,), width=2)

    # centre plate so the type always reads
    plate = Image.new("L", (W, H), 0)
    ImageDraw.Draw(plate).rounded_rectangle((cx - TEXT_HALF + 6, top, cx + TEXT_HALF - 6, top + PH), 18, fill=170)
    canvas.paste(Image.new("RGB", (W, H), INK), (0, 0), plate.filter(ImageFilter.GaussianBlur(30)))

    d = ImageDraw.Draw(canvas)
    # Makor mark: rings around the gold source point
    my = top + 62
    for r, a in ((44, 0.45), (30, 0.7), (17, 1.0)):
        col = tuple(round(INK[k] + (WATER[k] + 40 - INK[k]) * a) for k in range(3))
        d.ellipse((cx - r, my - r, cx + r, my + r), outline=col, width=4)
    d.ellipse((cx - 8, my - 8, cx + 8, my + 8), fill=GOLD)

    word = font(118, 560)
    d.text((cx, top + 178), "Makor", font=word, fill=CREAM, anchor="mm")
    tag = font(34, 400, 36)
    d.text((cx, top + 252), "The Bible on film, one movement at a time", font=tag, fill=(220, 205, 170), anchor="mm")

    # subscribe pill
    bf = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 30)
    label = "SUBSCRIBE"
    tw = d.textlength(label, font=bf)
    bw, bh = int(tw + 150), 66
    bx, by = cx - bw // 2, top + PH - bh - 26
    d.rounded_rectangle((bx, by, bx + bw, by + bh), bh // 2, fill=(255, 0, 0))
    # play glyph
    gx, gy = bx + 44, by + bh // 2
    d.rounded_rectangle((gx - 22, gy - 15, gx + 22, gy + 15), 8, fill=(255, 255, 255))
    d.polygon([(gx - 6, gy - 8), (gx - 6, gy + 8), (gx + 9, gy)], fill=(255, 0, 0))
    d.text((bx + 82 + tw / 2, gy + 1), label, font=bf, fill=(255, 255, 255), anchor="mm")

    canvas.save(OUT / "youtube-banner.jpg", quality=90, optimize=True)

    # preview with the safe areas marked
    pv = canvas.copy(); pd = ImageDraw.Draw(pv)
    pd.rectangle(SAFE, outline=(0, 255, 0), width=4)
    tablet = ((W - 1855) // 2, (H - 423) // 2, (W + 1855) // 2, (H + 423) // 2)
    pd.rectangle(tablet, outline=(255, 255, 0), width=3)
    pd.rectangle(((W - 2560) // 2, (H - 423) // 2, W, (H + 423) // 2), outline=(0, 160, 255), width=3)
    pv.resize((1280, 720)).save(OUT / "youtube-banner-safe-preview.jpg", quality=85)
    print((OUT / "youtube-banner.jpg").stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
