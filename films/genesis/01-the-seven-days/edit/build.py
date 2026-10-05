#!/usr/bin/env python3
"""Day One edit: builds exports/day-01-v1.mp4 from the clips, stills, voices,
sound effects and music, reproducibly.

    python3 films/genesis/01-the-seven-days/edit/build.py [v1|v2] [segments] [audio] [final]

  v1: the pilot as first cut (narrator also reads the two non Scripture lines).
  v2: Scripture only (default). Drops the study line with its shot 7, and the
      closing line; everything after shifts up 7.5 s.

Steps
  1. Captions and end card as transparent PNGs (PIL). Verse captions are built
     from the study JSON and checked to join back into the exact BSB verse.
  2. One video segment per shot (1080x1920, 30 fps), with the per shot fixes
     agreed at the checkpoints (trim, freeze, reverse, still push, grade).
  3. Audio mix: voices placed on the timeline, music cut from the Suno track and
     ducked under speech, sound effects, then two pass loudness to -14 LUFS.
  4. Final pass: 0.5 s dissolves between shots, captions, fades, mux.

Everything it writes goes to edit/ (ignored by git) and exports/.
"""
import json, pathlib, re, subprocess, sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

FILM = pathlib.Path(__file__).resolve().parents[1]
REPO = FILM.parents[2]
EDIT, CLIPS, STILLS, AUDIO = FILM / "edit", FILM / "clips", FILM / "stills", FILM / "audio"
CUT = next((a for a in sys.argv[1:] if a in ("v1", "v2")), "v2")
OUT = FILM / "exports" / f"day-01-{CUT}.mp4"
W, H, FPS = 1080, 1920, 30
XF = 0.5  # dissolve length between shots

# ---------------------------------------------------------------- timeline
# Shot boundaries from script/day-01-script.md (seconds).
SHOT_LEN = {1: 6.0, 2: 6.0, 3: 7.0, 4: 7.0, 5: 6.5, 6: 6.0, 7: 7.5, 8: 6.5, 9: 6.0}
SHOT_NOS = [1, 2, 3, 4, 5, 6, 7, 8, 9] if CUT == "v1" else [1, 2, 3, 4, 5, 6, 8, 9]
SHOTS = [SHOT_LEN[n] for n in SHOT_NOS]
TOTAL = sum(SHOTS)  # v1 58.5, v2 51.0
SHIFT = 0.0 if CUT == "v1" else -7.5   # applied to every cue after shot 6

# Voice cues: (file, start). Retimed to the eleven_multilingual_v2 renders.
VOICE = [
    ("narrator/n01.mp3", 1.0), ("narrator/n02.mp3", 7.0), ("narrator/n03.mp3", 17.6),
    ("god/g01.mp3", 20.0),
    ("narrator/n04.mp3", 24.4), ("narrator/n05.mp3", 27.0), ("narrator/n06.mp3", 33.0),
    ("narrator/n08.mp3", 47.6 + SHIFT),
] + ([("narrator/n07.mp3", 39.3), ("narrator/n09.mp3", 53.5)] if CUT == "v1" else [])
GOD_WINDOW = (19.6, 22.2)      # music drops almost to silence under God's line
MUSIC_FILE = AUDIO / "music" / "light-breaking.wav"
MUSIC_IN = 118.55              # track time at film 0; puts the track's swell (141.0) on the light (22.45)

# ---------------------------------------------------------------- captions
FONT_SERIF = "/System/Library/Fonts/NewYork.ttf"
FONT_SERIF_IT = "/System/Library/Fonts/NewYorkItalic.ttf"
FONT_SANS = "/System/Library/Fonts/Avenir Next.ttc"
CREAM, GOLD = (244, 236, 216, 255), (214, 170, 92, 255)
BAND_X0, BAND_X1, BAND_MID = 90, 900, 1290   # safe caption band (style bible)


def verses():
    d = json.loads((REPO / "src/content/studies/genesis/01-the-seven-days.json").read_text())
    plain = lambda t: re.sub(r"\{\{[^|}]+\|([^}]+)\}\}", r"\1", t)
    return {v["n"]: plain(v["text"]) for v in d["text"]["units"][0]["verses"]}


def split(text, *marks):
    """Split a verse after each mark; the parts must join back to the verse."""
    parts, rest = [], text
    for m in marks:
        i = rest.index(m) + len(m)
        parts.append(rest[:i].strip()); rest = rest[i:]
    parts.append(rest.strip())
    assert " ".join(parts) == text, f"split broke the verse: {parts}"
    return parts


def caption_list():
    v = verses()
    v2 = split(v[2], "the deep.")
    v3 = split(v[3], "God said,", "“Let there be light,”")
    v5 = split(v[5], "“night.”")
    st = "He separates and names, gives each thing its place and its role."
    assert st.rstrip(".") in json.dumps(json.loads((REPO / "src/content/studies/genesis/01-the-seven-days.json").read_text()),
                            ensure_ascii=False), "study line not found verbatim"
    # (name, label, text, start, end, italic, fade_in, fade_out)
    return [
        ("c01", "Genesis 1:1", v[1], 0.8, 4.4, False, True, True),
        ("c02", "Genesis 1:2", v2[0], 6.8, 12.45, False, True, True),
        ("c03", "Genesis 1:2", v2[1], 12.45, 16.8, False, False, True),
        ("c04", "Genesis 1:3", v3[0], 17.4, 19.9, False, True, False),
        ("c05", "Genesis 1:3", f"{v3[0]} {v3[1]}", 19.9, 24.3, False, False, False),
        ("c06", "Genesis 1:3", v[3], 24.3, 26.4, False, False, True),
        ("c07", "Genesis 1:4", v[4], 26.8, 32.4, False, True, True),
        ("c08", "Genesis 1:5", v5[0], 32.8, 38.2, False, True, True),
        ("c10", "Genesis 1:5", v5[1], 47.4 + SHIFT, 51.3 + SHIFT, False, True, True),
    ] + ([("c09", "", st, 39.1, 44.0, True, True, True),
          ("c11", "", "But the waters still have no shape.", 53.3, 55.4, True, True, True)] if CUT == "v1" else [])


def wrap(draw, text, font, width):
    lines, cur = [], ""
    for word in text.split():
        t = f"{cur} {word}".strip()
        if draw.textlength(t, font=font) <= width:
            cur = t
        else:
            lines.append(cur); cur = word
    return lines + [cur]


def shadowed(layer, color=(8, 20, 22)):
    """Soft halo under the text so it reads on gold, cream and black."""
    a = layer.split()[3]
    halo = Image.new("RGBA", layer.size, (*color, 0))
    halo.putalpha(a.filter(ImageFilter.GaussianBlur(9)).point(lambda p: min(255, int(p * 1.6))))
    return Image.alpha_composite(halo, layer)


def render_caption(name, label, text, italic):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_SERIF_IT if italic else FONT_SERIF, 60)
    lab = ImageFont.truetype(FONT_SANS, 30, index=0)
    lines = wrap(d, text, font, BAND_X1 - BAND_X0)
    lh = 80
    block = len(lines) * lh + (54 if label else 0)
    y = BAND_MID - block // 2
    if label:
        d.text(((BAND_X0 + BAND_X1) // 2, y), label.upper(), font=lab, fill=GOLD, anchor="mt")
        y += 54
    for ln in lines:
        d.text(((BAND_X0 + BAND_X1) // 2, y), ln, font=font, fill=CREAM, anchor="mt")
        y += lh
    # soft ink band behind the text: full width, feathered top and bottom
    top, bot = BAND_MID - block // 2 - 70, BAND_MID + block // 2 + 70
    band = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(band)
    for yy in range(top, bot):
        f = (yy - top) / (bot - top)
        alpha = int(165 * (1 - abs(2 * f - 1) ** 2.2))
        bd.line([(0, yy), (W, yy)], fill=(14, 42, 46, alpha))
    Image.alpha_composite(band, shadowed(img)).save(EDIT / "captions" / f"{name}.png")


def render_endcard():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx = (BAND_X0 + BAND_X1) // 2
    ink, gold = (14, 42, 46, 255), (150, 104, 30, 255)   # dark text: Shot 9's sky is pale cream
    d.text((cx, 560), "DAY TWO", font=ImageFont.truetype(FONT_SANS, 36, index=2), fill=gold, anchor="mt")
    d.text((cx, 640), "Makor", font=ImageFont.truetype(FONT_SERIF, 128), fill=ink, anchor="mt")
    d.text((cx, 820), "makor.co.za/genesis/the-seven-days", font=ImageFont.truetype(FONT_SANS, 42, index=2),
           fill=ink, anchor="mt")
    shadowed(img, color=(250, 244, 230)).save(EDIT / "captions" / "endcard.png")


# ---------------------------------------------------------------- helpers
def ff(*args):
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *map(str, args)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit("ffmpeg failed:\n" + " ".join(cmd)[:2000] + "\n" + r.stderr[-3000:])
    return r


def dur(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                 str(path)], capture_output=True, text=True).stdout)


COOL = "eq=saturation=0.55,colorbalance=rs=-0.05:gs=0.0:bs=0.04:rm=-0.04:bm=0.03:rh=-0.03:bh=0.02"
BASE = f"scale={W}:{H}:flags=lanczos,setsar=1,tpad=stop_mode=clone:stop_duration=1"
ENC = ["-an", "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", FPS]
INTERP = f"minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:vsbmc=1"


def seg_len(i):
    """Each segment overlaps its neighbours by half a dissolve."""
    return SHOTS[i] + (XF / 2 if i in (0, len(SHOTS) - 1) else XF)


def build_segments():
    for i in range(len(SHOTS)):
        n, L = SHOT_NOS[i], seg_len(i)
        out = EDIT / f"seg-{n:02d}.mp4"
        clip = CLIPS / f"shot-{n:02d}.mp4"
        if n == 3:   # wind: only the first 3.3 s, before the cold light rises; slowed to fill
            ff("-t", 3.3, "-i", clip, "-vf", f"setpts=PTS*({L}/3.3),{INTERP},{BASE},{COOL}", "-t", L, *ENC, out)
        elif n == 4:  # hold the dark first frame while God speaks, then the light breaks
            hold = 2.7
            ff("-i", clip, "-vf", f"fps={FPS},tpad=start_duration={hold}:start_mode=clone,{BASE}", "-t", L, *ENC, out)
        elif n == 8:  # evening fades (forward), morning returns (same frames reversed); no sun
            ff("-t", 2.4, "-i", clip, "-filter_complex",
               f"[0:v]split[a][b];[b]reverse[r];[a][r]concat=n=2:v=1,setpts=PTS*({L}/4.8),{INTERP},{BASE}[v]",
               "-map", "[v]", "-t", L, *ENC, out)
        elif n == 9:  # slow rise on the approved keyframe instead of the clip (breaking waves)
            ff("-loop", 1, "-framerate", FPS, "-t", L, "-i", STILLS / "shot-09.jpg", "-vf",
               f"scale=1200:-2:flags=lanczos,crop={W}:{H}:60:'(ih-{H})*(1-t/{L})',setsar=1,tpad=stop_mode=clone:stop_duration=1", "-t", L, *ENC, out)
        else:
            grade = f",{COOL}" if n in (1, 2) else ""
            ff("-i", clip, "-vf", f"fps={FPS},{BASE}{grade}", "-t", L, *ENC, out)
        if dur(out) < L - 0.01:  # interpolated segments can end a few frames early: hold the last frame
            tmp = out.with_suffix(".pad.mp4")
            ff("-i", out, "-vf", "tpad=stop_mode=clone:stop_duration=1", "-t", L, *ENC, tmp)
            tmp.replace(out)
        print(f"segment {n}: {dur(out):.2f}s (want {L:.2f})")


# ---------------------------------------------------------------- audio
def build_audio():
    ins, chains, voices = [], [], []
    ins_index = []
    def inp(path, *pre):
        ins.extend([*map(str, pre), "-i", str(path)]); ins_index.append(path); return len(ins_index) - 1
    fmt = "aformat=sample_rates=48000:channel_layouts=stereo"
    for j, (f, t) in enumerate(VOICE):
        k = inp(AUDIO / f)
        chains.append(f"[{k}]{fmt},adelay={int(t * 1000)}:all=1[v{j}]")
        voices.append(f"[v{j}]")
    chains.append(f"{''.join(voices)}amix=inputs={len(voices)}:normalize=0,apad=whole_dur={TOTAL}[vox]")
    chains.append("[vox]asplit[voxmix][voxkey]")
    m = inp(MUSIC_FILE, "-ss", MUSIC_IN, "-t", TOTAL)
    g0, g1 = GOD_WINDOW
    chains.append(f"[{m}]{fmt},afade=in:st=0:d=2.5,afade=out:st={TOTAL - 4}:d=4,"
                  f"volume='if(between(t,{g0},{g1}),0.12,0.6)':eval=frame[mus]")
    chains.append("[mus][voxkey]sidechaincompress=threshold=0.02:ratio=6:attack=30:release=500:makeup=1[musd]")
    w = inp(AUDIO / "sfx/wind-deep-water.mp3")
    chains.append(f"[{w}]{fmt},atrim=0:15,afade=in:d=2,afade=out:st=12.5:d=2.5,volume=0.45,adelay=4500:all=1[wind]")
    r = inp(AUDIO / "sfx/rumble-under-god.mp3")
    chains.append(f"[{r}]{fmt},volume=0.7,adelay=19300:all=1[rum]")
    s = inp(AUDIO / "sfx/light-swell.mp3")
    chains.append(f"[{s}]{fmt},volume=0.55,adelay=21900:all=1[swell]")
    rt = inp(AUDIO / "sfx/room-tone-calm-sea.mp3", "-stream_loop", 1)
    chains.append(f"[{rt}]{fmt},atrim=0:{TOTAL},afade=in:d=3,afade=out:st={TOTAL - 3}:d=3,volume=0.22[room]")
    chains.append(f"[voxmix][musd][wind][rum][swell][room]amix=inputs=6:normalize=0,atrim=0:{TOTAL}[mix]")
    raw = EDIT / f"mix-raw-{CUT}.wav"
    ff(*ins, "-filter_complex", ";".join(chains), "-map", "[mix]", "-ar", 48000, raw)
    # two pass loudness: measure, then apply
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(raw), "-af",
                        "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    blob = r.stderr[r.stderr.rindex("{"):]
    meas = json.loads(blob[:blob.index("}") + 1])
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={meas['input_i']}:measured_TP={meas['input_tp']}:"
          f"measured_LRA={meas['input_lra']}:measured_thresh={meas['input_thresh']}:offset={meas['target_offset']}:"
          "linear=true")
    ff("-i", raw, "-af", ln, "-ar", 48000, EDIT / f"mix-{CUT}.wav")
    print(f"audio: measured {meas['input_i']} LUFS, normalised to -14")


# ---------------------------------------------------------------- final
def build_final():
    caps = caption_list() + [("endcard", "", "", 55.0 if CUT == "v1" else TOTAL - 5.0, TOTAL, False, True, False)]
    ins, fc = [], []
    for i in range(len(SHOTS)):
        ins += ["-i", str(EDIT / f"seg-{SHOT_NOS[i]:02d}.mp4")]
    # dissolve chain
    prev, boundary = "[0:v]", 0.0
    for i in range(1, len(SHOTS)):
        boundary += SHOTS[i - 1]
        lab = f"[x{i}]"
        fc.append(f"{prev}[{i}:v]xfade=transition=fade:duration={XF}:offset={boundary - XF / 2:.3f}{lab}")
        prev = lab
    fc.append(f"{prev}fade=in:st=0:d=1.8,fade=out:st={TOTAL - 1.0}:d=1.0[base]")
    prev = "[base]"
    for j, (name, _l, _t, s, e, _it, fin, fout) in enumerate(caps):
        k = len(SHOTS) + j
        ins += ["-loop", "1", "-framerate", str(FPS), "-t", f"{e - s:.3f}", "-i", str(EDIT / "captions" / f"{name}.png")]
        fx = "format=rgba"
        if fin:
            fx += ",fade=in:st=0:d=0.3:alpha=1"
        if fout:
            fx += f",fade=out:st={e - s - 0.35:.3f}:d=0.35:alpha=1"
        fc.append(f"[{k}:v]{fx},setpts=PTS+{s}/TB[c{j}]")
        fc.append(f"{prev}[c{j}]overlay=0:0:eof_action=pass:enable='between(t,{s},{e})'[o{j}]")
        prev = f"[o{j}]"
    a = len(SHOTS) + len(caps)
    ins += ["-i", str(EDIT / f"mix-{CUT}.wav")]
    OUT.parent.mkdir(exist_ok=True)
    ff(*ins, "-filter_complex", ";".join(fc), "-map", prev, "-map", f"{a}:a", "-t", TOTAL,
       "-c:v", "libx264", "-crf", "18", "-preset", "slow", "-pix_fmt", "yuv420p", "-r", FPS,
       "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", OUT)
    print(f"export: {OUT.relative_to(FILM)}  {dur(OUT):.2f}s")


def main():
    (EDIT / "captions").mkdir(parents=True, exist_ok=True)
    for name, label, text, _s, _e, italic, _fi, _fo in caption_list():
        render_caption(name, label, text, italic)
    render_endcard()
    print("captions: rendered")
    only = [a for a in sys.argv[1:] if a not in ("v1", "v2")] or ["segments", "audio", "final"]
    if "segments" in only:
        build_segments()
    if "audio" in only:
        build_audio()
    if "final" in only:
        build_final()


if __name__ == "__main__":
    main()
