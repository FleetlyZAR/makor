#!/usr/bin/env python3
"""Labelled contact sheet of keyframes for review.

    python3 films/tools/sheet.py OUT.jpg img1.jpg img2.jpg ... [--cols 4]
"""
import pathlib, sys

from PIL import Image, ImageDraw, ImageFont


def main():
    args = sys.argv[1:]
    cols = 4
    if "--cols" in args:
        i = args.index("--cols"); cols = int(args[i + 1]); del args[i:i + 2]
    out, files = args[0], args[1:]
    tw = 640
    thumbs = []
    for f in files:
        im = Image.open(f).convert("RGB")
        im.thumbnail((tw, tw))
        thumbs.append((pathlib.Path(f).stem, im))
    th = max(im.height for _, im in thumbs)
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * th), (8, 20, 22))
    font = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 30, index=0)
    for i, (name, im) in enumerate(thumbs):
        x, y = (i % cols) * tw, (i // cols) * th
        sheet.paste(im, (x, y))
        d = ImageDraw.Draw(sheet)
        d.rectangle([x + 8, y + 8, x + 16 + d.textlength(name, font=font), y + 48], fill=(8, 20, 22))
        d.text((x + 12, y + 10), name, font=font, fill=(214, 170, 92))
    sheet.save(out, quality=85)
    print(out)


if __name__ == "__main__":
    main()
