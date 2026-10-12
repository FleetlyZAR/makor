#!/usr/bin/env python3
"""Review sheets for The Fall v2's LTX clips (films/CINEMA-STANDARD.md, animation rules 4 and 13).

For each clip in clips/ltx/: five frames from start to end in one labelled strip, and the strips
gathered into sheets of eight clips (edit/review/clips-NN.jpg). Clips whose shot has people
(flags man, woman, pair, bm, wife, family, or a cast reference) also get their five frames saved at
full size in edit/review/people/ for the modesty and face check.

    python3 films/genesis/03-the-fall-v2/edit/clip_review.py [s001 s047 ...]
"""
import json, pathlib, subprocess, sys

from PIL import Image, ImageDraw, ImageFont

FILM = pathlib.Path(__file__).resolve().parents[1]
CLIPS = FILM / "clips/ltx"
OUT = FILM / "edit/review"
PEOPLE = {"man", "woman", "pair", "manf", "womanf", "pairf", "hides", "hideclose", "hands", "bm"}
FONT = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 30)
TW, TH = 384, 211


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout)


def frames(clip, n=5):
    d = dur(clip)
    out = []
    for k in range(n):
        t = d * (0.04 + 0.92 * k / (n - 1))
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", str(clip), "-frames:v", "1", "-f", "image2pipe",
                              "-vcodec", "png", "-"], capture_output=True).stdout
        out.append((t, raw))
    return out


def main():
    shots = {s["id"]: s for s in json.loads((FILM / "script/shotlist.json").read_text())}
    want = sys.argv[1:] or sorted(p.stem for p in CLIPS.glob("s*.mp4"))
    (OUT / "people").mkdir(parents=True, exist_ok=True)
    strips = []
    for sid in want:
        clip = CLIPS / f"{sid}.mp4"
        if not clip.exists():
            continue
        sh = shots[sid]
        people = sh.get("flags") in PEOPLE or any("cast" in r for r in sh.get("refs", []))
        strip = Image.new("RGB", (TW * 5, TH + 44), (8, 20, 22))
        d = ImageDraw.Draw(strip)
        label = f"{sid}  {sh['chapter']}  {sh['dur']:.1f} s in the cut, clip {dur(clip):.1f} s" + ("  PEOPLE" if people else "")
        d.text((8, 4), label, font=FONT, fill=(230, 200, 120) if people else (200, 220, 215))
        for k, (t, raw) in enumerate(frames(clip)):
            tmp = OUT / "people" / f"{sid}-{k}.png"
            tmp.write_bytes(raw)
            im = Image.open(tmp).convert("RGB")
            if people:
                im.save(OUT / "people" / f"{sid}-{k}.jpg", quality=90)
            tmp.unlink()
            strip.paste(im.resize((TW, TH)), (k * TW, 44))
        strips.append(strip)
    for i in range(0, len(strips), 8):
        group = strips[i:i + 8]
        sheet = Image.new("RGB", (TW * 5, sum(s.height for s in group)), (8, 20, 22))
        y = 0
        for s in group:
            sheet.paste(s, (0, y)); y += s.height
        sheet.save(OUT / f"clips-{i // 8 + 1:02d}.jpg", quality=85)
    print(f"{len(strips)} clips reviewed -> {OUT}/clips-NN.jpg")


if __name__ == "__main__":
    main()
