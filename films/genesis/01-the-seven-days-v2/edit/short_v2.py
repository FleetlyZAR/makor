#!/usr/bin/env python3
"""The Seven Days v2 Short: the cold open as a 9:16 film, under 60 s (YouTube Shorts, Reels, TikTok).

The cold open is already a whole arc (God speaks in the dark, the drop, the burst, starlight, the earth, the garden,
history to today, the pull back to a spark, the brick-maker, "Let Us make man in Our image", the guide's line about
Babylon, the title), so the Short is that stretch of the finished cut (exports/full-cut-v4.mp4, picture and mix),
reframed shot by shot to 9:16 (FOCUS: where the subject sits across the 16:9 frame), with large words on screen for
silent viewing, then a 5 s end card over the music alone. Words stay clear of the Shorts interface (the top 200 px,
the bottom 420 px and the right 150 px).

Writes exports/the-seven-days-v2-short.mp4 (1080x1920, 30 fps, -14 LUFS) and a light WhatsApp Status copy.

    python3 films/genesis/01-the-seven-days-v2/edit/short_v2.py
"""
import json, pathlib, subprocess, sys

from PIL import Image, ImageDraw, ImageFilter

FILM = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(FILM.parents[1] / "tools"))
import platform_versions as pv  # noqa: E402

SRC = FILM / "exports" / "full-cut-v4.mp4"
OUT = FILM / "edit" / "short-v2"
END_AT, END = 47.0, 5.0                       # the cold open runs to 47 s; then the end card
W, H = 1080, 1920
CROP_W = 608                                  # 9:16 out of the 1080 px tall frame
# where each shot's subject sits across the frame (0 left, 1 right); default the centre
FOCUS = {"s008": 0.47, "s011": 0.47, "s012": 0.56, "s013": 0.3, "s014": 0.42, "s016": 0.5,
         "s021": 0.42, "s022": 0.36, "s023": 0.36}


def ff(*a):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *map(str, a)], capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr[-3000:])


def canvas():
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))


def shade_behind(img, box):
    sh = Image.new("L", img.size, 0)
    ImageDraw.Draw(sh).rounded_rectangle(box, radius=70, fill=140)
    return Image.composite(Image.new("RGBA", img.size, (6, 14, 16, 255)), img, sh.filter(ImageFilter.GaussianBlur(50)))


def words_png(p, text, ref=None, god=False, size=64, centre=1180):
    img = canvas()
    f = pv.serif(size, 500)
    d = ImageDraw.Draw(img)
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= 860 or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    lh = int(size * 1.28)
    top = centre - lh * len(lines) // 2
    widest = max(d.textlength(x, font=f) for x in lines)
    img = shade_behind(img, [540 - widest / 2 - 70, top - 40, 540 + widest / 2 + 70, top + lh * len(lines) + (70 if ref else 30)])
    d = ImageDraw.Draw(img)
    y = top
    for x in lines:
        d.text((540, y), x, font=f, fill=(240, 218, 168) if god else pv.CREAM, anchor="ma")
        y += lh
    if ref:
        d.text((540, y + 12), ref.upper(), font=pv.serif(34, 600), fill=pv.GOLD_TEXT, anchor="ma")
    pv.halo(img, blur=10, k=1.8).save(p)


def title_png(p):
    img = canvas()
    lk = pv.lockup(90)
    img.alpha_composite(pv.halo(lk), (540 - lk.width // 2, 760))
    t = canvas()
    td = ImageDraw.Draw(t)
    td.text((540, 960), "THE SEVEN", font=pv.serif(120, 600), fill=pv.CREAM, anchor="mm")
    td.text((540, 1090), "DAYS", font=pv.serif(120, 600), fill=pv.CREAM, anchor="mm")
    td.text((540, 1200), "Genesis 1:1 to 2:3", font=pv.serif(48, 400), fill=pv.GOLD_TEXT, anchor="mm")
    img.alpha_composite(pv.halo(t, blur=8))
    img.save(p)


def endcard(p):
    bg = Image.open(FILM / "stills" / "movement" / "s040.jpg").convert("RGB")
    s = H / bg.height
    bg = bg.resize((int(bg.width * s), H))
    x = int(bg.width * 0.62) - W // 2
    bg = bg.crop((x, 0, x + W, H)).filter(ImageFilter.GaussianBlur(6))
    bg = Image.blend(bg, Image.new("RGB", bg.size, (8, 22, 24)), 0.45).convert("RGBA")
    lk = pv.lockup(100)
    bg.alpha_composite(pv.halo(lk), (540 - lk.width // 2, 640))
    t = canvas()
    td = ImageDraw.Draw(t)
    td.text((540, 860), "Watch the full film", font=pv.serif(70, 600), fill=pv.CREAM, anchor="mm")
    td.text((540, 960), "Genesis 1, all seven days", font=pv.serif(46, 400), fill=pv.GOLD_TEXT, anchor="mm")
    td.text((540, 1030), "on the Makor channel", font=pv.serif(46, 400), fill=pv.GOLD_TEXT, anchor="mm")
    td.rounded_rectangle([340, 1130, 740, 1220], radius=45, fill=(*pv.GOLD, 255))
    td.text((540, 1175), "SUBSCRIBE", font=pv.serif(40, 700), fill=pv.INK, anchor="mm")
    bg.alpha_composite(pv.halo(t, blur=8))
    bg.convert("RGB").save(p)


def chunks(text, a, b, n):
    """Split a line into n pieces at sentence or clause breaks, each timed by its share of the characters."""
    import re
    parts = [x.strip() for x in re.split(r"(?<=[.;])\s+", text) if x.strip()]
    while len(parts) > n:
        i = min(range(len(parts) - 1), key=lambda k: len(parts[k]) + len(parts[k + 1]))
        parts[i:i + 2] = [parts[i] + " " + parts[i + 1]]
    total = sum(len(x) for x in parts)
    out, t = [], a
    for x in parts:
        d = (b - a) * len(x) / total
        out.append((x, t, t + d))
        t += d
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    shots = [s for s in json.loads((FILM / "script/shotlist.json").read_text()) if s["start"] < END_AT]
    T = json.loads((FILM / "script/movement-timeline.json").read_text())
    durs = json.loads((FILM / "script/movement-durations.json").read_text())
    # the crop follows each shot's subject
    xs = [(s["start"], FOCUS.get(s["id"], 0.5)) for s in shots]
    expr = "0"
    for start, f in reversed(xs):
        x = max(0, min(1920 - CROP_W, round(1920 * f - CROP_W / 2)))
        expr = f"if(gte(t\\,{start:.3f})\\,{x}\\,{expr})"
    items = []
    for e in T["events"]:
        if e["kind"] != "line" or e["t"] >= END_AT - 0.5:
            continue
        a, b = e["t"], e["t"] + durs[e["id"]]
        if e["speaker"] == "GOD":
            p = OUT / f"w-{e['id']}.png"
            words_png(p, e["text"], e.get("ref", "").replace(", flash-forward", ""), god=True, size=72)
            items.append((p, a, b + 0.5))
        else:
            for k, (x, ca, cb) in enumerate(chunks(e["text"], a, b, 3)):
                p = OUT / f"w-{e['id']}-{k}.png"
                words_png(p, x, centre=1390)       # lower: the push in fills the upper frame with his face
                items.append((p, ca, cb + 0.2))
    tp = OUT / "title.png"
    title_png(tp)
    items.append((tp, 42.6, END_AT))
    ec = OUT / "endcard.jpg"
    endcard(ec)
    ins = ["-t", END_AT, "-i", SRC]
    fc = [f"[0:v]crop={CROP_W}:1080:x='{expr}':y=0,scale={W}:{H}:flags=lanczos,setsar=1,fps=30[b0]"]
    for k, (p, a, b) in enumerate(items):
        ins += ["-loop", 1, "-framerate", 30, "-t", f"{b - a:.3f}", "-i", p]
        fc.append(f"[{k + 1}:v]format=rgba,fade=in:st=0:d=0.3:alpha=1,fade=out:st={max(0.1, b - a - 0.4):.2f}:d=0.4:alpha=1,"
                  f"setpts=PTS+{a:.3f}/TB[o{k}]")
        fc.append(f"[b{k}][o{k}]overlay=0:0:eof_action=pass:enable='between(t,{a:.2f},{b:.2f})'[b{k + 1}]")
    n = len(items) + 1
    ins += ["-loop", 1, "-framerate", 30, "-t", END, "-i", ec,
            "-ss", END_AT, "-t", END, "-i", FILM / "edit/score/music.wav"]
    fc.append(f"[b{len(items)}]trim=0:{END_AT},setpts=PTS-STARTPTS[film]")
    fc.append(f"[{n}:v]scale={W}:{H},fps=30,fade=in:d=0.6,format=yuv420p[end]")
    fc.append(f"[0:a]atrim=0:{END_AT},asetpts=PTS-STARTPTS,afade=out:st={END_AT - 1.5}:d=1.5[fa]")
    fc.append(f"[{n + 1}:a]aformat=sample_rates=48000:channel_layouts=stereo,afade=in:d=1,afade=out:st={END - 1.8}:d=1.8[ea]")
    fc.append("[film][fa][end][ea]concat=n=2:v=1:a=1[v][a]")
    graph = OUT / "graph.txt"
    graph.write_text(";\n".join(fc))
    raw = OUT / "short-raw.mov"
    ff(*ins, "-/filter_complex", graph, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "18", "-preset", "slow",
       "-pix_fmt", "yuv420p", "-r", 30, "-t", f"{END_AT + END:.2f}", "-c:a", "pcm_s16le", raw)
    final = FILM / "exports" / "the-seven-days-v2-short.mp4"
    pv.loudnorm_copy(raw, final)
    ff("-i", final, "-vf", "scale=720:1280", "-c:v", "libx264", "-crf", "27", "-preset", "slow", "-c:a", "aac", "-b:a", "96k",
       "-movflags", "+faststart", FILM / "exports" / "the-seven-days-v2-short-whatsapp.mp4")
    print(f"short: {final}, {len(items)} on-screen word cards")


if __name__ == "__main__":
    main()
