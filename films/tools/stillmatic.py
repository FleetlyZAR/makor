#!/usr/bin/env python3
"""Review cut of a movement film with stills in place: every keyframe on the real
timeline with its slow push, pull, pan or tilt, over the voice track and the act
scores. Free; no paid calls. (Captions come in the real edit.)

    python3 films/tools/stillmatic.py films/genesis/01-the-seven-days

Shots with no keyframe yet show plain ink.
"""
import json, pathlib, subprocess, sys

FPS, W, H = 25, 1920, 1080
# act scores and the chapter each one starts on
ACTS = [("act1.wav", "Cold open"), ("act2.wav", "Day Two: the sky"), ("act3.wav", "Day Four: the lights"),
        ("act4.wav", "Day Six: the image of God"), ("act5.wav", "Day Seven: rest"),
        ("act6.wav", "In the beginning was the Word")]


def ff(*a):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *map(str, a)], capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr[-2500:])


def move(motion, n):
    """zoompan expressions for the shot's edit move over n frames."""
    m = motion.lower()
    p = f"(on/{n})"
    if "pull back" in m:
        return f"z='1.12-0.12*{p}'", "x='iw/2-(iw/zoom/2)'", "y='ih/2-(ih/zoom/2)'"
    if "pan" in m or "drift" in m or "across" in m:
        return "z='1.12'", f"x='(iw-iw/zoom)*{p}'", "y='ih/2-(ih/zoom/2)'"
    if "tilt up" in m or "rise" in m:
        return "z='1.12'", "x='iw/2-(iw/zoom/2)'", f"y='(ih-ih/zoom)*(1-{p})'"
    return f"z='1+0.12*{p}'", "x='iw/2-(iw/zoom/2)'", "y='ih/2-(ih/zoom/2)'"   # push in


def main():
    film = pathlib.Path(sys.argv[1]).resolve()
    shots = json.loads((film / "script" / "shotlist.json").read_text())
    tl = json.loads((film / "script" / "movement-timeline.json").read_text())
    kdir, sdir = film / "stills" / "movement", film / "edit" / "stillmatic"
    sdir.mkdir(parents=True, exist_ok=True)
    byid = {s["id"]: s for s in shots}
    parts = []
    for s in shots:
        src_id = s["flags"].split("use:")[1].split()[0] if s["kind"] == "reuse" else s["id"]
        key = kdir / f"{src_id}.jpg"
        motion = s["motion"] or byid[src_id]["motion"]
        # frames from the cumulative timeline, so rounding never drifts across 124 shots
        n = max(1, round((s["start"] + s["dur"]) * FPS) - round(s["start"] * FPS))
        out = sdir / f"{s['id']}.mp4"
        if key.exists():
            z, x, y = move(motion.split(" Painterly")[0], n)
            ff("-i", key, "-vf", f"scale=3840:-2,zoompan={z}:{x}:{y}:d={n}:s={W}x{H}:fps={FPS},setsar=1",
               "-frames:v", n, "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p", out)
        else:
            ff("-f", "lavfi", "-i", f"color=c=0x0E2A2E:s={W}x{H}:r={FPS}:d={s['dur']}", "-frames:v", n,
               "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p", out)
        parts.append(out)
    lst = sdir / "concat.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in parts))
    video = sdir / "video.mp4"
    ff("-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", video)
    # score: each act from its chapter start to the next act, faded in and out
    starts = {name: t for t, name in tl["chapters"]}
    total = tl["total"]
    ins, chains, labels = [], [], []
    for i, (f, ch) in enumerate(ACTS):
        a = starts[ch]
        b = starts[ACTS[i + 1][1]] if i + 1 < len(ACTS) else total
        L = b - a + 2.0
        ins += ["-i", str(film / "audio" / "music" / f)]
        chains.append(f"[{i + 2}:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{L:.2f},"
                      f"afade=in:d=2,afade=out:st={L - 3:.2f}:d=3,adelay={int(a * 1000)}:all=1,volume=0.4[m{i}]")
        labels.append(f"[m{i}]")
    fc = ";".join(chains) + f";{''.join(labels)}amix=inputs={len(labels)}:normalize=0[mus];" \
         f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,apad=whole_dur={total},asplit[v][key];" \
         f"[mus][key]sidechaincompress=threshold=0.02:ratio=8:attack=30:release=600[md];" \
         f"[v][md]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5[a]"
    out = film / "exports" / "movement-stillmatic.mp4"
    ff("-i", video, "-i", film / "audio" / "movement" / "voice-track.wav", *ins, "-filter_complex", fc,
       "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-t", f"{total:.3f}",
       "-movflags", "+faststart", out)
    have = sum(1 for s in shots if (kdir / f"{s['id']}.jpg").exists() or s["kind"] == "reuse")
    print(f"stillmatic: {have}/{len(shots)} shots with pictures -> {out}")


if __name__ == "__main__":
    main()
