#!/usr/bin/env python3
"""Question-led Shorts from The Seven Days v2 (exports/shorts-from-the-film.md), built from the film itself.

Each Short is data below: beats in order, each with its voice lines and its shots. A line is a film line id
(already voiced in audio/movement/, optionally only part of it), or a NEW guide line, voiced here with the film's
GUIDE voice (Kokoro am_michael, speed 0.85, the Makor names lexicon). Lines play end to end with a short breath
between them; each beat's shots share its time. Pictures are cut from the finished film (exports/full-cut-v4.mp4,
each shot's own stretch) and reframed to 9:16 (FOCUS) or, for the forming and filling graphic, set whole on the
dark ground (BOX). Every spoken word is on screen (Scripture with its reference), a headline carries the
question, a quiet bed from the film's score sits under the voice, and the end card is short_v2's.

    makor-audio/.venv/bin/python films/genesis/01-the-seven-days-v2/edit/shorts_qa.py [light image days pattern]
Writes exports/shorts/<name>.mp4 (1080x1920, 30 fps, -14 LUFS).
"""
import json, pathlib, re, subprocess, sys

from PIL import Image, ImageDraw

FILM = pathlib.Path(__file__).resolve().parents[1]
ROOT = FILM.parents[2]
sys.path.insert(0, str(FILM.parents[1] / "tools"))
sys.path.insert(0, str(FILM / "edit"))
import platform_versions as pv  # noqa: E402
import short_v2 as SV  # noqa: E402

SRC = FILM / "exports" / "full-cut-v4.mp4"
OUT = FILM / "exports" / "shorts"
WORK = FILM / "edit" / "shorts-qa"
FPS, W, H, GAP, END = 30, 1080, 1920, 0.4, 4.5
T = json.loads((FILM / "script/movement-timeline.json").read_text())
DURS = json.loads((FILM / "script/movement-durations.json").read_text())
LINES = {e["id"]: e for e in T["events"] if e["kind"] == "line"}
SHOTS = {s["id"]: s for s in json.loads((FILM / "script/shotlist.json").read_text())}
FOCUS = dict(SV.FOCUS, s101=0.47, s102=0.42, s103=0.5, s104=0.5, s107=0.5, s108=0.55, s128=0.6, s075=0.45,
             s028=0.42, s022=0.36, s021=0.42)
BOX = {"s047": (500, 60, 920, 980), "s048": (500, 60, 920, 980)}   # x, y, w, h of the graphic in the film frame

# ---------------------------------------------------------------- the four Shorts (exports/shorts-from-the-film.md)
SHORTS = {
    "light": dict(
        title="Light Before the Sun? Genesis 1 Explained", music=("theme-light", 0.0, 0.35),
        beats=[
            dict(lines=[("new", "light-hook", "Day one has light. The sun does not appear until day four.")],
                 shots=["s040"], headline="LIGHT BEFORE THE SUN?"),
            dict(lines=["m010", "m011", "m012"], shots=["s038", "s039"]),
            dict(lines=["m020"], shots=["s041", "s042", "s043"], headline="LIGHT COMES FROM GOD"),
            dict(lines=["m041"], shots=["s067", "s068", "s071"]),
            dict(lines=["m045"], shots=["s075", "s076", "s077"], headline="THE SUN IS NOT A GOD"),
        ]),
    "image": dict(
        title="What Made in God's Image Meant to Slaves in Egypt", music=("theme-image", 0.0, 0.32),
        beats=[
            dict(lines=[("m060", 0.0, 4.7, "“Let Us make man in Our image, after Our likeness,")],
                 shots=["s022"], headline="MADE IN GOD'S IMAGE"),
            dict(lines=["m061"], shots=["s101", "s102", "s103"]),
            dict(lines=["m063"], shots=["s104", "s105"], headline="TSELEM: A CARVED IMAGE"),
            dict(lines=["m064"], shots=["s107", "s108", "s028"], headline="FIRST HEARD BY SLAVES"),
            dict(lines=["m067"], shots=["s109", "s110"]),
        ]),
    "days": dict(
        title="How Long Were the 7 Days of Creation?", music=("himalayan-moon", 120.0, 0.32),
        beats=[
            dict(lines=[("new", "days-hook", "How long were the six days of creation?")],
                 shots=["s044"], headline="HOW LONG WERE THE DAYS?"),
            dict(lines=[("m014", 6.9, None, "And there was evening, and there was morning, the first day.")],
                 shots=["s045"]),
            dict(lines=[("new", "days-ordinary", "Some read ordinary days. Each one is numbered, and closed with "
                         "evening and morning.")], shots=["s066", "s067"], headline="1. ORDINARY DAYS"),
            dict(lines=[("new", "days-ages", "Some read long ages. The seventh day has no closing evening, and "
                         "its rest is still open.")], shots=["s073", "s074"], headline="2. LONG AGES"),
            dict(lines=[("new", "days-frame", "Some read a framework. Two matching sets of three days, with the "
                         "sun placed on day four.")], shots=["s048"], headline="3. A FRAMEWORK"),
            dict(lines=["m081", "m082"], shots=["s128", "s129"]),
            dict(lines=[("new", "days-bearing", "Christians who hold the full truth of Scripture have held each "
                         "of these views.")], shots=["s120", "s121"]),
            dict(lines=["m083"], shots=["s131", "s132"], headline="NOT HOW LONG. WHO HE IS."),
        ]),
    "pattern": dict(
        title="The Hidden Pattern in the 7 Days of Creation", music=("dissemination", 0.0, 0.3),
        beats=[
            dict(lines=["m015"], shots=["s046"], headline="THE HIDDEN PATTERN"),
            # the graphic runs on the film's own clock, so these three lines keep the film's spacing (FILMSPAN)
            dict(span=(LINES["m016"]["t"], LINES["m018"]["t"] + DURS["m018"] + 0.4), shots=["s047", "s048"]),
            dict(lines=["m035", "m036"], shots=["s064", "s065"], headline="SHAPED. BUT EMPTY."),
            dict(lines=[("m053", 3.1, None, "The whole account moves from emptiness to fullness, because God gives.")],
                 shots=["s087"]),
        ]),
}


def run(*a, **k):
    r = subprocess.run([str(x) for x in a], capture_output=True, text=True, **k)
    if r.returncode:
        sys.exit(r.stderr[-3000:])
    return r


def ff(*a):
    run("ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *a)


def dur(p):
    return float(run("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p).stdout)


# ---------------------------------------------------------------- voice
def voice_new(key, text):
    """A NEW guide line in the film's GUIDE voice (the same path as films/tools/movement_voice.py)."""
    dest = WORK / "voice" / f"{key}.wav"
    if dest.exists():
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(ROOT / "makor-audio"))
    import generate_audio as ga
    if not hasattr(voice_new, "engine"):
        voice_new.engine, voice_new.over = ga.make_torch_engine(), ga.load_pronounce()
    spoken = text
    for a, b in ga.QUOTES.items():
        spoken = spoken.replace(a, b)
    spoken = ga.apply_pronounce(spoken, voice_new.over)
    speed = json.loads((FILM / "film.json").read_text())["voice_speed"]["GUIDE"]
    ga.write_wav(voice_new.engine(spoken, "am_michael", speed), dest)
    return dest


def film_line(lid):
    e = LINES[lid]
    sp = e["speaker"].lower()
    return FILM / "audio" / "movement" / f"{lid}-{sp}.{'wav' if sp == 'guide' else 'mp3'}"


def segments(beat):
    """(audio file, start in file, length, words, speaker, reference) for each line of a beat."""
    out = []
    if "span" in beat:
        a, b = beat["span"]
        for lid, e in LINES.items():
            if a - 0.01 <= e["t"] < b:
                out.append(("span", e["t"] - a, DURS[lid], e["text"], e["speaker"], None))
        return out
    for ln in beat["lines"]:
        if isinstance(ln, str):
            e = LINES[ln]
            ref = e.get("ref", "")
            ref = ref if ref.split(" ")[0] in ("Genesis", "Exodus", "John") and e["speaker"] != "GUIDE" else None
            out.append((film_line(ln), 0.0, DURS[ln], e["text"], e["speaker"], ref))
        elif ln[0] == "new":
            p = voice_new(ln[1], ln[2])
            out.append((p, 0.0, dur(p), ln[2], "GUIDE", None))
        else:
            lid, a, b, text = ln
            e = LINES[lid]
            b = DURS[lid] if b is None else b
            ref = e.get("ref", "") if e["speaker"] != "GUIDE" else None
            out.append((film_line(lid), a, b - a, text, e["speaker"], ref))
    return out


# ---------------------------------------------------------------- words on screen
def headline_png(p, text, top=360):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    f = pv.serif(84, 700)
    d = ImageDraw.Draw(img)
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= 900 or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    widest = max(d.textlength(x, font=f) for x in lines)
    img = SV.shade_behind(img, [540 - widest / 2 - 70, top - 30, 540 + widest / 2 + 70, top + 100 * len(lines)])
    d = ImageDraw.Draw(img)
    for i, x in enumerate(lines):
        d.text((540, top + 100 * i), x, font=f, fill=(232, 182, 78), anchor="ma")
    pv.halo(img, blur=10, k=1.8).save(p)


def pieces(text, a, length):
    """Split spoken words into on-screen pieces of up to about 70 characters, timed by their share of the line."""
    parts = [x.strip() for x in re.split(r"(?<=[.,;:])\s+", text) if x.strip()]
    merged, cur = [], ""
    for x in parts:
        if cur and len(cur) + len(x) > 70:
            merged.append(cur)
            cur = x
        else:
            cur = (cur + " " + x).strip()
    merged.append(cur)
    total = sum(len(x) for x in merged)
    out, t = [], a
    for x in merged:
        d = length * len(x) / total
        out.append((x, t, t + d))
        t += d
    return out


# ---------------------------------------------------------------- build one
def build(name):
    spec = SHORTS[name]
    wd = WORK / name
    wd.mkdir(parents=True, exist_ok=True)
    # timeline: each beat's lines end to end, a breath between them
    t, plan, audio, words = 0.6, [], [], []
    for bi, beat in enumerate(spec["beats"]):
        b0 = t
        boxed = any(s in BOX for s in beat["shots"])
        centre = (1440 if beat.get("headline") else 1420) if boxed else 1360
        segs = segments(beat)
        if "span" in beat:
            a, b = beat["span"]
            audio.append((FILM / "audio/movement/voice-track.wav", a, b - a, t))
            for (_, off, ln, text, sp, ref) in segs:
                words += [(x, t + off + ca, t + off + cb, sp, ref, centre) for x, ca, cb in pieces(text, 0, ln)]
            t += (b - a)
        else:
            for (src, a, ln, text, sp, ref) in segs:
                audio.append((src, a, ln, t))
                words += [(x, ca, cb, sp, ref, centre) for x, ca, cb in pieces(text, t, ln)]
                t += ln + GAP
        plan.append((beat, b0, t))
    total = t + 0.4
    # picture: each beat's shots share its time, cut from the film and reframed
    parts, frame = [], 0
    for beat, b0, b1 in plan:
        if beat is plan[-1][0]:
            b1 = total
        n = len(beat["shots"])
        for k, sid in enumerate(beat["shots"]):
            s0 = b0 + (b1 - b0) * k / n
            s1 = b0 + (b1 - b0) * (k + 1) / n
            nf = round(s1 * FPS) - round(s0 * FPS)
            if beat is plan[0][0] and k == 0:
                nf += round(b0 * FPS)            # the opening breath shows the first shot too
            sh = SHOTS[sid]
            slot = nf / FPS
            take = min(sh["dur"] - 0.1, slot)
            start = sh["start"] + (0.05 if "span" not in beat else 0.0)
            if "span" in beat:                   # the graphic plays on its own clock: start where the span starts
                start = max(sh["start"], beat["span"][0]) if k == 0 else sh["start"]
                take = min(sh["start"] + sh["dur"] - start, slot)
            slow = slot / take
            if sid in BOX:                       # the graphic whole, high in the frame, the words beneath it
                x, y, w, h = BOX[sid]
                gw, gy = (900, 330) if beat.get("headline") else (960, 200)
                vf = (f"crop={w}:{h}:{x}:{y},scale={gw}:-2,pad={W}:{H}:{(W - gw) // 2}:{gy}:color=0x081618")
            else:
                f = FOCUS.get(sid, 0.5)
                cx = max(0, min(1920 - 608, round(1920 * f - 304)))
                vf = f"crop=608:1080:{cx}:0,scale={W}:{H}:flags=lanczos"
            p = wd / f"{len(parts):02d}-{sid}.mp4"
            ff("-ss", f"{start:.3f}", "-t", f"{take + 0.2:.3f}", "-i", SRC, "-vf",
               f"setpts=PTS*{slow:.4f},{vf},setsar=1,fps={FPS},tpad=stop_mode=clone:stop_duration=2",
               "-frames:v", nf, "-an", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", p)
            parts.append(p)
            frame += nf
    lst = wd / "list.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in parts))
    pic = wd / "picture.mp4"
    ff("-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", pic)
    # on-screen words and headlines
    items = []
    for i, (x, a, b, sp, ref, centre) in enumerate(words):
        p = wd / f"w{i:03d}.png"
        SV.words_png(p, x, ref, god=(sp == "GOD"), size=56 if centre in (1420, 1440) else 60, centre=centre)
        items.append((p, a, b + 0.15))
    for bi, (beat, b0, b1) in enumerate(plan):
        if beat.get("headline"):
            p = wd / f"h{bi}.png"
            headline_png(p, beat["headline"], 200 if any(s in BOX for s in beat["shots"]) else 360)
            items.append((p, max(0.0, b0 - 0.3), b1 - 0.1))
    ec = wd / "endcard.jpg"
    SV.endcard(ec)
    # sound: the lines on a quiet bed of the film's score, the bed ducked under the voice
    ins, fc, vl = ["-i", pic], [], []
    for k, (src, a, ln, at) in enumerate(audio):
        ins += ["-ss", f"{a:.3f}", "-t", f"{ln:.3f}", "-i", src]
        fc.append(f"[{k + 1}:a]aformat=sample_rates=48000:channel_layouts=stereo,loudnorm=I=-18:LRA=7:TP=-2,"
                  f"adelay={int(at * 1000)}:all=1[v{k}]")
        vl.append(f"[v{k}]")
    m = len(audio) + 1
    track, seek, vol = spec["music"]
    ins += ["-ss", seek, "-t", total + END, "-i", FILM / "audio/music-v2" / f"{track}.wav"]
    n_ec = m + 1
    ins += ["-loop", 1, "-framerate", FPS, "-t", END, "-i", ec]
    pngs0 = n_ec + 1
    for p, a, b in items:
        ins += ["-loop", 1, "-framerate", FPS, "-t", f"{b - a:.3f}", "-i", p]
    fc.append(f"{''.join(vl)}amix=inputs={len(vl)}:normalize=0,apad=whole_dur={total + END:.2f},asplit[voice][key]")
    fc.append(f"[{m}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={vol},afade=in:d=1.2,"
              f"afade=out:st={total + END - 2.5:.2f}:d=2.5[bed]")
    fc.append("[bed][key]sidechaincompress=threshold=0.03:ratio=6:attack=30:release=450[duck]")
    fc.append("[voice][duck]amix=inputs=2:normalize=0[a]")
    fc.append(f"[0:v]setpts=PTS-STARTPTS[b0]")
    for k, (p, a, b) in enumerate(items):
        fc.append(f"[{pngs0 + k}:v]format=rgba,fade=in:st=0:d=0.25:alpha=1,fade=out:st={max(0.1, b - a - 0.3):.2f}:d=0.3:"
                  f"alpha=1,setpts=PTS+{a:.3f}/TB[o{k}]")
        fc.append(f"[b{k}][o{k}]overlay=0:0:eof_action=pass:enable='between(t,{a:.2f},{b:.2f})'[b{k + 1}]")
    fc.append(f"[b{len(items)}]trim=0:{total:.3f},setpts=PTS-STARTPTS[film]")
    fc.append(f"[{n_ec}:v]scale={W}:{H},fps={FPS},fade=in:d=0.5,format=yuv420p[end]")
    fc.append(f"[a]atrim=0:{total + END:.3f}[aa]")
    fc.append("[film][end]concat=n=2:v=1:a=0[v]")
    graph = wd / "graph.txt"
    graph.write_text(";\n".join(fc))
    raw = wd / "raw.mov"
    ff(*ins, "-/filter_complex", graph, "-map", "[v]", "-map", "[aa]", "-c:v", "libx264", "-crf", "18", "-preset", "slow",
       "-pix_fmt", "yuv420p", "-r", FPS, "-t", f"{total + END:.2f}", "-c:a", "pcm_s16le", raw)
    OUT.mkdir(parents=True, exist_ok=True)
    final = OUT / f"{name}.mp4"
    pv.loudnorm_copy(raw, final)
    print(f"{name}: {final} {dur(final):.1f} s, {len(words)} word cards, {len(parts)} shots")


if __name__ == "__main__":
    for name in (sys.argv[1:] or list(SHORTS)):
        build(name)
