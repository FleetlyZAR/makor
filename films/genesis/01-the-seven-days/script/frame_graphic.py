#!/usr/bin/env python3
"""The two panel frame of Genesis 1, built from finished stills (free).

  s017  days one to three (forming), left column only
  s019  forming and filling side by side, each filling beside the realm it fills
  s020  the same with the seventh day above both

    python3 films/genesis/01-the-seven-days/script/frame_graphic.py
"""
import pathlib

from PIL import Image, ImageDraw, ImageFont

FILM = pathlib.Path(__file__).resolve().parents[1]
W, H = 2752, 1536
INK, GOLD, CREAM = (14, 42, 46), (214, 170, 92), (244, 236, 216)
SANS = "/System/Library/Fonts/Avenir Next.ttc"
FORM = ["stills/movement/s025.jpg", "stills/movement/s035.jpg", "stills/world/shot-01.jpg"]
FILL = ["stills/world/shot-03.jpg", "stills/world/shot-05.jpg", "stills/world/shot-07.jpg"]
REST = "stills/world/shot-08.jpg"
DAYS_L, DAYS_R = ["Day 1  light", "Day 2  sky and sea", "Day 3  land"], \
                 ["Day 4  lights", "Day 5  birds and fish", "Day 6  animals and people"]


def panel(path, w, h):
    im = Image.open(FILM / path).convert("RGB")
    r = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * r) + 1, int(im.height * r) + 1), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def draw(columns, seventh, out):
    img = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(img)
    lab = ImageFont.truetype(SANS, 46, index=2)
    head = ImageFont.truetype(SANS, 52, index=0)
    top = 420 if seventh else 170
    pw, gap = 1060, 36
    ph = (H - top - 120 - 2 * gap) // 3
    x0 = (W - 2 * pw - 160) // 2
    if seventh:
        sw = 2 * pw + 160
        img.paste(panel(REST, sw, 170), (x0, 120))
        d.rectangle([x0, 120, x0 + sw, 290], outline=GOLD, width=3)
        d.text((x0 + sw // 2, 70), "DAY 7  REST, THE GOAL", font=head, fill=GOLD, anchor="mm")
    for c, (paths, labels, title) in enumerate(columns):
        x = x0 + c * (pw + 160)
        d.text((x + pw // 2, top - 50), title, font=head, fill=GOLD, anchor="mm")
        for r, (p, t) in enumerate(zip(paths, labels)):
            y = top + r * (ph + gap)
            img.paste(panel(p, pw, ph), (x, y))
            d.rectangle([x, y, x + pw, y + ph], outline=GOLD, width=3)
            tw = d.textlength(t, font=lab)
            d.rectangle([x + 16, y + ph - 78, x + 44 + tw, y + ph - 14], fill=INK)
            d.text((x + 30, y + ph - 46), t, font=lab, fill=CREAM, anchor="lm")
    if len(columns) == 2:   # arrows: each filling answers its realm
        for r in range(3):
            y = top + r * (ph + gap) + ph // 2
            xa, xb = x0 + pw + 30, x0 + pw + 130
            d.line([xa, y, xb, y], fill=GOLD, width=5)
            d.polygon([(xb, y - 14), (xb + 22, y), (xb, y + 14)], fill=GOLD)
    img.save(FILM / out, quality=92)
    print(out)


draw([(FORM, DAYS_L, "FORMING  the formless given shape")], False, "stills/movement/s017.jpg")
draw([(FORM, DAYS_L, "FORMING"), (FILL, DAYS_R, "FILLING")], False, "stills/movement/s019.jpg")
draw([(FORM, DAYS_L, "FORMING"), (FILL, DAYS_R, "FILLING")], True, "stills/movement/s020.jpg")
