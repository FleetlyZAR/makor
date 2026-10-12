#!/usr/bin/env python3
"""Scan keyframes for black side bars and flat bands (VIDEO-METHODS lessons 14 and 15).

Flags any image whose outer 2 percent strip on a side is near black, or which has a run of rows or
columns with almost no detail (a seam or a faded band the image models sometimes leave).

    python3 films/genesis/03-the-fall-v2/edit/edge_scan.py films/genesis/03-the-fall-v2/stills/movement/*.jpg
"""
import sys

import numpy as np
from PIL import Image


def scan(path):
    a = np.asarray(Image.open(path).convert("L"), dtype=np.float32)
    h, w = a.shape
    out = []
    m = max(4, int(0.02 * min(h, w)))
    for side, strip in (("left", a[:, :m]), ("right", a[:, -m:]), ("top", a[:m]), ("bottom", a[-m:])):
        if strip.mean() < 12 and strip.std() < 6:
            out.append(f"black bar {side}")
    rows = np.abs(np.diff(a, axis=1)).mean(axis=1)
    cols = np.abs(np.diff(a, axis=0)).mean(axis=0)
    for name, prof, n in (("rows", rows, h), ("cols", cols, w)):
        flat = prof < 0.6
        run = best = 0
        for f in flat:
            run = run + 1 if f else 0
            best = max(best, run)
        if best > 0.06 * n:
            out.append(f"flat band in {name} ({best} px)")
    return out


if __name__ == "__main__":
    bad = 0
    for p in sys.argv[1:]:
        r = scan(p)
        if r:
            bad += 1
            print(p.split("/")[-1], "; ".join(r))
    print(f"{bad} of {len(sys.argv) - 1} flagged")
