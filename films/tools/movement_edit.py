#!/usr/bin/env python3
"""The full movement film edit (M7), reproducible from the script files.

Inputs: script/shotlist.json (shots), script/movement-timeline.json (lines and
cards), script/movement-durations.json, stills/movement/, clips/movement/ (Veo
clips are used where they exist; otherwise the keyframe with its slow move),
audio/movement/voice-track.wav, audio/music/act1..6.wav, sound effects.

Output: exports/the-seven-days-v2.mp4 (1920x1080, 30 fps, -14 LUFS) and
exports/the-seven-days-v2.srt (every spoken line, for YouTube captions).

Video: 0.5 s dissolves between shots (per chapter), and between chapters.
Captions: Scripture (READER and GOD) burned in as a lower third on the ink
band with its reference; GUIDE lines are in the SRT only. Chapter titles appear
briefly at the start of each chapter.

    python3 films/tools/movement_edit.py films/genesis/01-the-seven-days [segments] [audio] [final]
"""
import json, pathlib, re, subprocess, sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS, XF = 1920, 1080, 30, 0.5
LEAD, TAIL = 2.0, 4.0   # seconds of dark before the first line; extra hold on the end card
SERIF = "/System/Library/Fonts/NewYork.ttf"
SANS = "/System/Library/Fonts/Avenir Next.ttc"
CREAM, GOLD = (244, 236, 216, 255), (214, 170, 92, 255)
ACTS = [("act1.wav", "Cold open"), ("act2.wav", "Day Two: the sky"), ("act3.wav", "Day Four: the lights"),
        ("act4.wav", "Day Six: the image of God"), ("act5.wav", "Day Seven: rest"),
        ("act6.wav", "In the beginning was the Word")]
# (cue, first shot, last shot, volume); paths under audio/sfx/
SFX = [
    ("room-tone-calm-sea.mp3", "s001", "s005", 0.35), ("wind-deep-water.mp3", "s002", "s004", 0.45),
    ("movement/desert-camp.mp3", "s006", "s006", 0.4), ("movement/lamp-room.mp3", "s007", "s007", 0.4),
    ("movement/storm-sea.mp3", "s008", "s008", 0.5), ("movement/lamp-room.mp3", "s009", "s009", 0.4),
    ("movement/nile-kilns.mp3", "s010", "s010", 0.4), ("room-tone-calm-sea.mp3", "s011", "s011", 0.35),
    ("movement/desert-camp.mp3", "s012", "s014", 0.35), ("room-tone-calm-sea.mp3", "s015", "s023", 0.3),
    ("wind-deep-water.mp3", "s021", "s021", 0.45),
    ("room-tone-calm-sea.mp3", "s024", "s030", 0.3), ("rumble-under-god.mp3", "s024", "s024", 0.6),
    ("light-swell.mp3", "s024", "s024", 0.5),
    ("movement/waters-parting.mp3", "s031", "s032", 0.45), ("room-tone-calm-sea.mp3", "s031", "s036", 0.3),
    ("movement/land-rising.mp3", "s037", "s038", 0.5), ("movement/grass-wind.mp3", "s040", "s046", 0.3),
    ("light-swell.mp3", "s047", "s047", 0.45), ("movement/grass-wind.mp3", "s047", "s049", 0.25),
    ("movement/night-air.mp3", "s050", "s052", 0.35), ("movement/night-air.mp3", "s055", "s055", 0.35),
    ("movement/lamp-room.mp3", "s056", "s056", 0.4), ("movement/night-air.mp3", "s057", "s057", 0.35),
    ("movement/seabirds.mp3", "s058", "s065", 0.3), ("movement/whales.mp3", "s059", "s059", 0.5),
    ("movement/whales.mp3", "s063", "s063", 0.45),
    ("movement/herds.mp3", "s066", "s069", 0.35), ("movement/grass-wind.mp3", "s070", "s077", 0.25),
    ("movement/herds.mp3", "s080", "s081", 0.3), ("movement/meadow-birds.mp3", "s082", "s086", 0.3),
    ("movement/golden-stillness.mp3", "s087", "s096", 0.35), ("movement/desert-camp.mp3", "s097", "s098", 0.35),
    ("movement/golden-stillness.mp3", "s099", "s102", 0.3),
    ("movement/single-flame.mp3", "s103", "s104", 0.35), ("movement/garden-dawn.mp3", "s105", "s105", 0.3),
    ("movement/single-flame.mp3", "s106", "s106", 0.35), ("movement/garden-dawn.mp3", "s107", "s110", 0.3),
    ("movement/river-stones.mp3", "s111", "s112", 0.3),
    ("movement/thorn-wind.mp3", "s113", "s114", 0.35), ("movement/flood.mp3", "s115", "s115", 0.45),
    ("movement/golden-stillness.mp3", "s116", "s117", 0.3), ("movement/new-creation.mp3", "s118", "s121", 0.35),
    ("room-tone-calm-sea.mp3", "s122", "s124", 0.3), ("light-swell.mp3", "s122", "s122", 0.45),
]


def ff(*a):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *map(str, a)], capture_output=True, text=True)
    if r.returncode:
        sys.exit("ffmpeg failed:\n" + r.stderr[-3000:])


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout)


ENC = ["-an", "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", str(FPS)]


def move(motion, n):
    m = motion.lower()
    p = f"(on/{n})"
    if "pull back" in m:
        return f"z='1.12-0.12*{p}'", "x='iw/2-(iw/zoom/2)'", "y='ih/2-(ih/zoom/2)'"
    if "pan" in m or "drift" in m or "across" in m:
        return "z='1.12'", f"x='(iw-iw/zoom)*{p}'", "y='ih/2-(ih/zoom/2)'"
    if "tilt up" in m or "rise" in m:
        return "z='1.12'", "x='iw/2-(iw/zoom/2)'", f"y='(ih-ih/zoom)*(1-{p})'"
    return f"z='1+0.12*{p}'", "x='iw/2-(iw/zoom/2)'", "y='ih/2-(ih/zoom/2)'"


def chapters_of(shots):
    out = []
    for s in shots:
        if not out or out[-1][0] != s["chapter"]:
            out.append((s["chapter"], []))
        out[-1][1].append(s)
    return out


def build_segments(film, shots):
    """One segment per shot, padded by half a dissolve on each side that touches another shot in its chapter."""
    sdir = film / "edit" / "movement" / "seg"
    sdir.mkdir(parents=True, exist_ok=True)
    byid = {s["id"]: s for s in shots}
    for ch, group in chapters_of(shots):
        for j, s in enumerate(group):
            pad_in = XF / 2 if j > 0 else 0
            pad_out = XF / 2 if j < len(group) - 1 else 0
            L = s["dur"] + pad_in + pad_out
            out = sdir / f"{s['id']}.mp4"
            src = s["flags"].split("use:")[1].split()[0] if s["kind"] == "reuse" else s["id"]
            clip = film / "clips" / "movement" / f"{src}.mp4"
            key = film / "stills" / "movement" / f"{src}.jpg"
            n = round(L * FPS)
            use_clip = clip.exists() and byid[src]["kind"] in ("veo", "ff")
            source = clip if use_clip else key
            stamp = sdir / f"{s['id']}.flags"
            same_flags = stamp.exists() and stamp.read_text() == byid[src]["flags"]
            stamp.write_text(byid[src]["flags"])
            if same_flags and out.exists() and out.stat().st_mtime > source.stat().st_mtime \
                    and abs(dur(out) - n / FPS) < 0.05:
                continue   # already built from this source at this length
            flags = byid[src]["flags"].split()
            span = next((f[5:] for f in flags if f.startswith("clip:")), None)
            dis = next((f[9:] for f in flags if f.startswith("dissolve:")), None)
            if dis:   # crossfade between this keyframe and another, each with a slow push, no clip
                other = film / "stills" / "movement" / f"{dis}.jpg"
                h = n // 2
                fc = (f"[0:v]scale=3840:-2,zoompan=z='1+0.06*(on/{n})':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
                      f"d={n}:s={W}x{H}:fps={FPS},setsar=1[a];"
                      f"[1:v]scale=3840:-2,zoompan=z='1.06+0.06*(on/{n})':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
                      f"d={n}:s={W}x{H}:fps={FPS},setsar=1[b];"
                      f"[a][b]xfade=transition=fade:duration={(n - h) / FPS * 0.9:.3f}:offset={h / FPS * 0.6:.3f}[v]")
                ff("-i", key, "-i", other, "-filter_complex", fc, "-map", "[v]", "-frames:v", n, *ENC, out)
            elif use_clip and span:   # only the clean part of the clip, slowed to fill the shot
                a0, a1 = map(float, span.split("-"))
                ff("-ss", a0, "-t", a1 - a0, "-i", clip, "-vf",
                   f"setpts=PTS*({n / FPS}/{a1 - a0}),minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:vsbmc=1,"
                   f"scale={W}:{H}:flags=lanczos,setsar=1,tpad=stop_mode=clone:stop_duration=4",
                   "-frames:v", n, *ENC, out)
            elif use_clip:
                ff("-i", clip, "-vf", f"fps={FPS},scale={W}:{H}:flags=lanczos,setsar=1,"
                   f"tpad=stop_mode=clone:stop_duration=4", "-frames:v", n, *ENC, out)
            else:
                motion = (s["motion"] or byid[src]["motion"]).split(" Painterly")[0]
                z, x, y = move(motion, n)
                ff("-i", key, "-vf", f"scale=3840:-2,zoompan={z}:{x}:{y}:d={n}:s={W}x{H}:fps={FPS},setsar=1",
                   "-frames:v", n, *ENC, out)
        print(f"segments: {ch}", flush=True)


def build_chapters(film, shots):
    """Dissolve the shots of each chapter together; then dissolve the chapters together."""
    sdir, cdir = film / "edit" / "movement" / "seg", film / "edit" / "movement" / "ch"
    cdir.mkdir(parents=True, exist_ok=True)
    groups = chapters_of(shots)
    chfiles = []
    for ci, (ch, group) in enumerate(groups):
        ins = sum([["-i", str(sdir / f"{s['id']}.mp4")] for s in group], [])
        fc, prev, b = [], "[0:v]", 0.0
        for j in range(1, len(group)):
            b += group[j - 1]["dur"]
            fc.append(f"{prev}[{j}:v]xfade=transition=fade:duration={XF}:offset={b - XF / 2:.3f}[x{j}]")
            prev = f"[x{j}]"
        # pad chapter ends by half a dissolve where it meets another chapter
        pre = XF / 2 if ci > 0 else 0
        post = XF / 2 if ci < len(groups) - 1 else 0
        fc.append(f"{prev}tpad=start_mode=clone:start_duration={pre}:stop_mode=clone:stop_duration={post}[v]")
        out = cdir / f"ch{ci + 1:02d}.mp4"
        ff(*ins, "-filter_complex", ";".join(fc), "-map", "[v]", *ENC, out)
        chfiles.append(out)
    ins = sum([["-i", str(c)] for c in chfiles], [])
    fc, prev, b = [], "[0:v]", 0.0
    for ci in range(1, len(groups)):
        b += sum(s["dur"] for s in groups[ci - 1][1])
        fc.append(f"{prev}[{ci}:v]xfade=transition=fade:duration={XF}:offset={b - XF / 2:.3f}[c{ci}]")
        prev = f"[c{ci}]"
    total = sum(s["dur"] for s in shots)
    fc.append(f"{prev}fade=in:st=0:d=2,fade=out:st={total - 2:.3f}:d=2[v]")
    out = film / "edit" / "movement" / "picture.mp4"
    ff(*ins, "-filter_complex", ";".join(fc), "-map", "[v]", "-t", f"{total:.3f}", *ENC, out)
    print(f"picture: {dur(out):.2f}s (timeline {total:.2f}s)")


# ---------------------------------------------------------------- captions
def wrap(d, text, f, width):
    lines, cur = [], ""
    for w in text.split():
        t = f"{cur} {w}".strip()
        if d.textlength(t, font=f) <= width:
            cur = t
        else:
            lines.append(cur); cur = w
    return lines + [cur]


def chunks(text, d, f, width, max_lines=3):
    """Split a long line into caption cards of at most max_lines, at punctuation where possible."""
    if len(wrap(d, text, f, width)) <= max_lines:
        return [text]
    parts = re.split(r"(?<=[,;:.!?”])\s+", text)
    cards, cur = [], ""
    for p in parts:
        t = f"{cur} {p}".strip()
        if cur and len(wrap(d, t, f, width)) > max_lines:
            cards.append(cur); cur = p
        else:
            cur = t
    cards.append(cur)
    assert " ".join(cards) == text
    return cards


def caption_png(path, label, text):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f, lab = ImageFont.truetype(SERIF, 46), ImageFont.truetype(SANS, 26, index=0)
    rows = wrap(d, text, f, 1500)
    lh, top = 60, H - 70 - len(rows) * 60 - 44
    band = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(band)
    for yy in range(top - 70, H):
        fr = (yy - (top - 70)) / (H - top + 70)
        bd.line([(0, yy), (W, yy)], fill=(8, 22, 24, int(185 * min(1, fr * 1.8))))
    d.text((W // 2, top), label.upper(), font=lab, fill=GOLD, anchor="ma")
    y = top + 42
    for r in rows:
        d.text((W // 2, y), r, font=f, fill=CREAM, anchor="ma"); y += lh
    a = img.split()[3]
    halo = Image.new("RGBA", img.size, (6, 18, 20, 0))
    halo.putalpha(a.filter(ImageFilter.GaussianBlur(6)))
    Image.alpha_composite(Image.alpha_composite(band, halo), img).save(path)


def title_png(path, text, size=44, y=150):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    rows = text.split(" / ")
    for i, r in enumerate(rows):
        f = ImageFont.truetype(SERIF, size * 2) if (i == 0 and size > 60) else ImageFont.truetype(SANS, size, index=2)
        d.text((W // 2, y + i * (size * 2 + 20)), r.upper() if size <= 60 else r, font=f,
               fill=CREAM if i == 0 else GOLD, anchor="ma")
    a = img.split()[3]
    halo = Image.new("RGBA", img.size, (6, 18, 20, 0))
    halo.putalpha(a.filter(ImageFilter.GaussianBlur(10)).point(lambda p: min(255, int(p * 1.5))))
    # soft ink band behind the title block so it reads on gold and cream skies
    box = a.getbbox() or (0, 0, W, H)
    band = Image.new("RGBA", img.size, (0, 0, 0, 0))
    bd = ImageDraw.Draw(band)
    t0, t1 = box[1] - 60, box[3] + 60
    for yy in range(max(0, t0), min(H, t1)):
        f = (yy - t0) / (t1 - t0)
        bd.line([(0, yy), (W, yy)], fill=(8, 22, 24, int(150 * (1 - abs(2 * f - 1) ** 2.2))))
    Image.alpha_composite(Image.alpha_composite(band, halo), img).save(path)


def srt_time(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def overlays(film, tl, durs):
    cdir = film / "edit" / "movement" / "captions"
    cdir.mkdir(parents=True, exist_ok=True)
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    f = ImageFont.truetype(SERIF, 46)
    items, srt = [], []
    for e in tl["events"]:
        if e["kind"] != "line":
            continue
        t0, t1 = e["t"], e["t"] + durs[e["id"]]
        srt.append((t0, t1, e["text"]))
        if e["speaker"] == "GUIDE":
            continue
        cards = chunks(e["text"], probe, f, 1500)
        total_chars = sum(len(c) for c in cards)
        t = t0
        for k, c in enumerate(cards):
            tt = t + (t1 - t0) * len(c) / total_chars
            p = cdir / f"{e['id']}-{k}.png"
            caption_png(p, e.get("ref", ""), c)
            items.append((p, t - 0.15, tt + 0.35 if k == len(cards) - 1 else tt, k == 0, k == len(cards) - 1))
            t = tt
    for i, (t, name) in enumerate(tl["chapters"]):
        if name == "Cold open":
            continue
        p = cdir / f"chapter-{i:02d}.png"
        title_png(p, name.replace(": ", " / "))
        items.append((p, t + 0.4, t + 4.4, True, True))
    for e in tl["events"]:
        if e["kind"] == "card":
            p = cdir / f"card-{int(e['t'] * 10)}.png"
            title_png(p, e["text"], size=64, y=330)
            items.append((p, e["t"], min(e["t"] + 8, tl["total"]), True, True))
    (film / "exports").mkdir(exist_ok=True)
    (film / "exports" / "the-seven-days-v2.srt").write_text(
        "\n".join(f"{i}\n{srt_time(a)} --> {srt_time(b)}\n{t}\n" for i, (a, b, t) in enumerate(srt, 1)))
    return items


# ---------------------------------------------------------------- audio
def build_audio(film, shots, tl):
    starts = {name: t for t, name in tl["chapters"]}
    shot_t = {s["id"]: (s["start"], s["start"] + s["dur"]) for s in shots}
    total = tl["total"]
    ins, ch, labels = ["-i", str(film / "audio" / "movement" / "voice-track.wav")], [], []
    n = 1
    for i, (f, chap) in enumerate(ACTS):
        a = starts[chap]
        b = starts[ACTS[i + 1][1]] if i + 1 < len(ACTS) else total
        L = b - a + 2.0
        ins += ["-i", str(film / "audio" / "music" / f)]
        ch.append(f"[{n}:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{L:.2f},afade=in:d=2.5,"
                  f"afade=out:st={L - 3:.2f}:d=3,adelay={int(a * 1000)}:all=1,volume=0.42[m{i}]")
        labels.append(f"[m{i}]"); n += 1
    ch.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0[mus]")
    fx = []
    for j, (cue, a_id, b_id, vol) in enumerate(SFX):
        a, b = shot_t[a_id][0], shot_t[b_id][1]
        L = b - a
        ins += ["-stream_loop", "-1", "-i", str(film / "audio" / "sfx" / cue)]
        ch.append(f"[{n}:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{L:.2f},"
                  f"afade=in:d={min(1.5, L / 3):.2f},afade=out:st={max(0, L - 1.5):.2f}:d={min(1.5, L / 3):.2f},"
                  f"volume={vol},adelay={int(a * 1000)}:all=1[f{j}]")
        fx.append(f"[f{j}]"); n += 1
    ch.append(f"{''.join(fx)}amix=inputs={len(fx)}:normalize=0[sfx]")
    ch.append(f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay={int(LEAD * 1000)}:all=1,"
              f"apad=whole_dur={total},asplit[v][key];"
              f"[key]asplit[k1][k2];"
              f"[mus][k1]sidechaincompress=threshold=0.02:ratio=7:attack=30:release=600[musd];"
              f"[sfx][k2]sidechaincompress=threshold=0.02:ratio=4:attack=30:release=500[sfxd];"
              f"[v][musd][sfxd]amix=inputs=3:normalize=0,atrim=0:{total:.3f}[mix]")
    raw = film / "edit" / "movement" / "mix-raw.wav"
    ff(*ins, "-filter_complex", ";".join(ch), "-map", "[mix]", "-ar", 48000, raw)
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(raw), "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True)
    blob = r.stderr[r.stderr.rindex("{"):]
    m = json.loads(blob[:blob.index("}") + 1])
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    ff("-i", raw, "-af", ln, "-ar", 48000, film / "edit" / "movement" / "mix.wav")
    print(f"audio: measured {m['input_i']} LUFS, normalised to -14")


def build_final(film, tl, durs):
    items = overlays(film, tl, durs)
    pic = film / "edit" / "movement" / "picture.mp4"
    ins, fc, prev = ["-i", str(pic)], [], "[0:v]"
    for k, (p, a, b, fin, fout) in enumerate(items, 1):
        L = b - a
        ins += ["-loop", "1", "-framerate", str(FPS), "-t", f"{L:.3f}", "-i", str(p)]
        fx = "format=rgba" + (",fade=in:st=0:d=0.3:alpha=1" if fin else "") + \
             (f",fade=out:st={L - 0.35:.3f}:d=0.35:alpha=1" if fout else "")
        fc.append(f"[{k}:v]{fx},setpts=PTS+{a:.3f}/TB[o{k}]")
        fc.append(f"{prev}[o{k}]overlay=0:0:eof_action=pass:enable='between(t,{a:.3f},{b:.3f})'[p{k}]")
        prev = f"[p{k}]"
    ins += ["-i", str(film / "edit" / "movement" / "mix.wav")]
    out = film / "exports" / "the-seven-days-v2.mp4"
    script = film / "edit" / "movement" / "final-graph.txt"
    script.write_text(";".join(fc))
    ff(*ins, "-/filter_complex", script, "-map", prev, "-map", f"{len(items) + 1}:a",
       "-t", f"{tl['total']:.3f}", "-c:v", "libx264", "-crf", "18", "-preset", "slow", "-pix_fmt", "yuv420p",
       "-r", FPS, "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out)
    print(f"export: {out} {dur(out):.2f}s, {len(items)} overlays; SRT written")


def main():
    film = pathlib.Path(sys.argv[1]).resolve()
    steps = sys.argv[2:] or ["segments", "audio", "final"]
    shots = json.loads((film / "script" / "shotlist.json").read_text())
    tl = json.loads((film / "script" / "movement-timeline.json").read_text())
    durs = json.loads((film / "script" / "movement-durations.json").read_text())
    # lead in and tail: hold the first shot LEAD s longer and the last TAIL s longer, move everything after
    shots[0]["dur"] += LEAD
    for sh in shots[1:]:
        sh["start"] += LEAD
    shots[-1]["dur"] += TAIL
    for e in tl["events"]:
        e["t"] += LEAD
    tl["chapters"] = [[t + (LEAD if i else 0), n] for i, (t, n) in enumerate(tl["chapters"])]
    tl["total"] += LEAD + TAIL
    (film / "edit" / "movement").mkdir(parents=True, exist_ok=True)
    if "segments" in steps:
        build_segments(film, shots)
        build_chapters(film, shots)
    if "audio" in steps:
        build_audio(film, shots, tl)
    if "final" in steps:
        build_final(film, tl, durs)


if __name__ == "__main__":
    main()
