#!/usr/bin/env python3
"""Pre-delivery audit of The Garden v2's full cut (films/CINEMA-STANDARD.md, animation rule 14).

1. Length: the cut's frames against the voice timeline (no drift).
2. One labelled frame from the middle of every shot, with the words being heard at that moment, in sheets
   (edit/review/audit-NN.jpg), to check each picture against its scene and its words.
3. Every one of those frames scanned for flat bands and seams at the edges, and for unintended black.

    makor-audio/.venv/bin/python films/genesis/02-the-garden-v2/edit/audit.py [exports/full-cut-v1.mp4]
"""
import json, pathlib, subprocess, sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

FILM = pathlib.Path(__file__).resolve().parents[1]
FPS = 24
OUT = FILM / "edit/review"
FONT = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 22)


def frame(video, t):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(video), "-frames:v", "1", "-f", "rawvideo",
                          "-pix_fmt", "rgb24", "-s", "960x540", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(540, 960, 3)


def bands(a):
    """Edges that are flat (a band or bar) or a hard seam a little way in."""
    g = a.mean(axis=2)
    found = []
    for name, strip in (("bottom", g[-40:]), ("top", g[:30]), ("left", g[:, :20].T), ("right", g[:, -20:].T)):
        if strip.std() < 3.0 and g.std() > 12:
            found.append(f"flat {name}")
    rows = g.mean(axis=1)
    jump = np.abs(np.diff(rows[300:530]))
    if jump.max() > 18:
        found.append(f"seam at y={300 + int(jump.argmax())}")
    return found


def main():
    video = FILM / (sys.argv[1] if len(sys.argv) > 1 else "exports/full-cut-v1.mp4")
    T = json.loads((FILM / "script/movement-timeline.json").read_text())
    durs = json.loads((FILM / "script/movement-durations.json").read_text())
    shots = json.loads((FILM / "script/shotlist.json").read_text())
    nf = int(subprocess.run(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries",
                             "stream=nb_read_packets", "-of", "csv=p=0", str(video)], capture_output=True, text=True).stdout)
    want = round(T["total"] * FPS)
    print(f"length: {nf} frames, timeline {want} ({(nf - want) / FPS:+.2f} s)")
    lines = [e for e in T["events"] if e["kind"] == "line"]
    tiles, problems = [], []
    for sh in shots:
        t = sh["start"] + sh["dur"] / 2
        a = frame(video, t)
        heard = next((l["text"] for l in lines if l["t"] <= t < l["t"] + durs[l["id"]]), "")
        issues = bands(a)
        if a.mean() < 8 and sh["kind"] != "graphic":
            issues.append("black")
        if issues:
            problems.append(f"{sh['id']} {sh['chapter']}: {', '.join(issues)}")
        im = Image.fromarray(a.copy()).resize((480, 270))
        tile = Image.new("RGB", (480, 330), (8, 20, 22))
        tile.paste(im, (0, 0))
        d = ImageDraw.Draw(tile)
        d.text((6, 274), f"{sh['id']}  {int(sh['start'] // 60)}:{sh['start'] % 60:04.1f}" + ("  !" if issues else ""),
               font=FONT, fill=(230, 200, 120) if issues else (200, 220, 215))
        d.text((6, 300), (heard[:44] + "...") if len(heard) > 44 else heard, font=FONT, fill=(170, 190, 185))
        tiles.append(tile)
    for i in range(0, len(tiles), 20):
        group = tiles[i:i + 20]
        sheet = Image.new("RGB", (480 * 5, 330 * ((len(group) + 4) // 5)), (8, 20, 22))
        for k, t in enumerate(group):
            sheet.paste(t, ((k % 5) * 480, (k // 5) * 330))
        sheet.save(OUT / f"audit-{i // 20 + 1:02d}.jpg", quality=85)
    print(f"{len(shots)} shots, {len(problems)} flagged")
    for p in problems:
        print("  " + p)


if __name__ == "__main__":
    main()
