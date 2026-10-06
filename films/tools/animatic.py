#!/usr/bin/env python3
"""Animatic for a movement film: the whole film timed to its voice track, with
one title card per shot and the spoken line as a lower third. Free; no paid calls.

  1. Cuts every chapter into shots of about 7 s, each cut on a line or beat
     boundary, and writes script/movement-shots.json (the draft shot list).
  2. Renders one 1920x1080 card per state (shot and current line).
  3. Lays the cards over audio/movement/voice-track.wav with temp music ducked
     under the voices, and writes exports/movement-animatic.mp4.

    python3 films/tools/animatic.py films/genesis/01-the-seven-days
"""
import json, pathlib, subprocess, sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
INK, WATER, GOLD, CREAM = (14, 42, 46), (15, 108, 108), (214, 170, 92), (244, 236, 216)
SERIF, SERIF_IT = "/System/Library/Fonts/NewYork.ttf", "/System/Library/Fonts/NewYorkItalic.ttf"
SANS = "/System/Library/Fonts/Avenir Next.ttc"
TARGET, LO, HI = 7.0, 4.5, 9.5
SPEAKER_COLOUR = {"READER": GOLD, "GOD": (240, 200, 120), "GUIDE": (120, 190, 185)}


def font(path, size, index=0):
    return ImageFont.truetype(path, size, index=index)


def wrap(d, text, f, width):
    lines, cur = [], ""
    for w in text.split():
        t = f"{cur} {w}".strip()
        if d.textlength(t, font=f) <= width:
            cur = t
        else:
            lines.append(cur); cur = w
    return lines + [cur]


def tc(s):
    return f"{int(s // 60)}:{int(s % 60):02d}"


def shots_for(tl):
    events, total = tl["events"], tl["total"]
    bounds = [a for a, _ in tl["chapters"]] + [total]
    shots = []
    for ci, (start, name) in enumerate(tl["chapters"]):
        end = bounds[ci + 1]
        cuts = sorted({e["t"] for e in events if e["chapter"] == name and e["kind"] in ("line", "beat")
                       and start < e["t"] < end})
        t, n = start, 1
        while end - t > HI:
            options = [c for c in cuts if t + LO <= c <= t + HI]
            nxt = min(options, key=lambda c: abs(c - (t + TARGET))) if options else t + TARGET
            if end - nxt < LO:
                break
            shots.append({"chapter": name, "n": n, "start": round(t, 3), "dur": round(nxt - t, 3)}); t, n = nxt, n + 1
        if end - t > HI:   # a long remainder: split it on the cut nearest its middle
            mid = (t + end) / 2
            options = [c for c in cuts if t + LO <= c <= end - LO]
            m = min(options, key=lambda c: abs(c - mid)) if options else mid
            shots.append({"chapter": name, "n": n, "start": round(t, 3), "dur": round(m - t, 3)}); t, n = m, n + 1
        shots.append({"chapter": name, "n": n, "start": round(t, 3), "dur": round(end - t, 3)})
    for i, s in enumerate(shots, 1):
        s["id"] = f"s{i:03d}"
        pics = [e for e in events if e["kind"] == "pic" and e["chapter"] == s["chapter"] and e["t"] <= s["start"] + 0.01]
        s["picture"] = pics[-1]["text"] if pics else ""
        cards = [e["text"] for e in events if e["kind"] == "card" and s["start"] - 0.01 <= e["t"] < s["start"] + s["dur"]]
        if cards:
            s["cards"] = cards
    return shots


def card(shot, idx, total_shots, line, path):
    img = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(img)
    d.text((80, 60), shot["chapter"].upper(), font=font(SANS, 30), fill=GOLD)
    d.text((W - 80, 60), f"{shot['id']}  ({shot['n']} in chapter)  {tc(shot['start'])}", font=font(SANS, 28, 7),
           fill=(150, 170, 170), anchor="ra")
    d.text((80, 140), f"Shot {idx} of {total_shots}  /  {shot['dur']:.1f} s", font=font(SERIF, 64), fill=CREAM)
    y = 250
    for ln in wrap(d, shot["picture"] or "(picture to be written in M4)", font(SANS, 38, 5), W - 160)[:6]:
        d.text((80, y), ln, font=font(SANS, 38, 5), fill=(200, 210, 205)); y += 54
    for c in shot.get("cards", []):
        d.text((W // 2, y + 40), c.replace(" / ", "   "), font=font(SERIF, 54), fill=GOLD, anchor="ma"); y += 80
    if line:
        sp, txt, ref = line["speaker"], line["text"], line.get("ref", "")
        f = font(SERIF_IT if sp == "GUIDE" else SERIF, 46)
        rows = wrap(d, txt, f, W - 360)[:3]
        top = H - 90 - len(rows) * 60 - 50
        band = Image.new("RGBA", (W, H - top + 40), (0, 0, 0, 0))
        bd = ImageDraw.Draw(band)
        for yy in range(band.height):
            fr = yy / band.height
            bd.line([(0, yy), (W, yy)], fill=(6, 20, 22, int(200 * min(1, fr * 2.2))))
        img.paste(band, (0, top - 40), band)
        d = ImageDraw.Draw(img)
        label = sp + (f"  /  {ref}" if ref and sp != "GUIDE" else "")
        d.text((W // 2, top), label.upper(), font=font(SANS, 26), fill=SPEAKER_COLOUR[sp], anchor="ma")
        yy = top + 46
        for r in rows:
            d.text((W // 2, yy), r, font=f, fill=CREAM, anchor="ma"); yy += 60
    img.save(path)


def main():
    film = pathlib.Path(sys.argv[1]).resolve()
    tl = json.loads((film / "script" / "movement-timeline.json").read_text())
    durs = json.loads((film / "script" / "movement-durations.json").read_text())
    shots = shots_for(tl)
    (film / "script" / "movement-shots.json").write_text(json.dumps(shots, indent=1, ensure_ascii=False))
    lines = [dict(e, end=e["t"] + durs[e["id"]]) for e in tl["events"] if e["kind"] == "line"]
    # states change at every shot start, line start and line end
    marks = sorted({0.0, tl["total"], *[s["start"] for s in shots], *[l["t"] for l in lines], *[l["end"] for l in lines]})
    fdir = film / "edit" / "animatic"
    fdir.mkdir(parents=True, exist_ok=True)
    for old in fdir.glob("*.png"):
        old.unlink()
    concat, cache = [], {}
    for a, b in zip(marks, marks[1:]):
        if b - a < 0.02:
            continue
        mid = (a + b) / 2
        si = max(i for i, s in enumerate(shots) if s["start"] <= mid + 1e-6)
        ln = next((l for l in lines if l["t"] <= mid < l["end"]), None)
        keyname = (si, ln["id"] if ln else None)
        if keyname not in cache:
            p = fdir / f"{len(cache):04d}.png"
            card(shots[si], si + 1, len(shots), ln, p)
            cache[keyname] = p
        concat.append((cache[keyname], b - a))
    lst = fdir / "concat.txt"
    lst.write_text("".join(f"file '{p}'\nduration {d:.3f}\n" for p, d in concat) + f"file '{concat[-1][0]}'\n")
    out = film / "exports" / "movement-animatic.mp4"
    out.parent.mkdir(exist_ok=True)
    cfg_f = film / "film.json"
    cfg = json.loads(cfg_f.read_text()) if cfg_f.exists() else {}
    music = (film / cfg["temp_music"]).resolve() if cfg.get("temp_music") else film / "audio" / "music" / "light-breaking.wav"
    voice = film / "audio" / "movement" / "voice-track.wav"
    total = tl["total"]
    fc = (f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,apad=whole_dur={total},asplit[v][key];"
          f"[2:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{total},volume=0.35[m];"
          f"[m][key]sidechaincompress=threshold=0.02:ratio=8:attack=30:release=600[md];"
          f"[v][md]amix=inputs=2:normalize=0,afade=out:st={total - 4}:d=4,loudnorm=I=-14:TP=-1.5[a]")
    r = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
                        "-i", str(voice), "-stream_loop", "-1", "-i", str(music), "-filter_complex", fc,
                        "-map", "0:v", "-map", "[a]", "-r", "25", "-c:v", "libx264", "-crf", "28", "-preset", "fast",
                        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-t", f"{total:.3f}",
                        "-movflags", "+faststart", str(out)], capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr[-2000:])
    print(f"{len(shots)} shots, {len(cache)} cards, animatic {tc(total)} -> {out}")


if __name__ == "__main__":
    main()
