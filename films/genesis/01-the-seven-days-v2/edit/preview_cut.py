#!/usr/bin/env python3
"""Picture preview of a stretch of The Seven Days v2 with the full mix underneath.

Each shot from script/shotlist.json becomes a 1920x1080, 24 fps segment. Its clip is the Omni clip
(clips/omni, films/tools/omni_clips.py; a shot marked "same" cuts from another shot's clip), else the LTX
clip (clips/ltx, films/tools/ltx_clips.py; PREFER_LTX turns the order round), else an older Veo clip
(clips/movement), else its still with a slow move; graphics are black. CLIP_TRIMS sets the source
ranges by hand (joined to fill the shot); without one the window is chosen automatically: the middle of the
clip, a little faster for montage shots, moved clear of any cut Omni put inside the clip, and shots longer
than the clip are slowed with motion interpolation so they stay smooth. The mix (edit/score/mix.wav) runs
underneath.

    python3 films/genesis/01-the-seven-days-v2/edit/preview_cut.py 0 47.1 [--out exports/cold-open-preview.mp4]
"""
import json, pathlib, subprocess, sys

FILM = pathlib.Path(__file__).resolve().parents[1]
FPS = 24
FONT = FILM.parents[1] / "fonts" / "Fraunces[SOFT,WONK,opsz,wght].ttf"
# shot id: list of (start, end) in the clip's own seconds, joined in order to fill the shot
CLIP_TRIMS = {
    # the opening, cut from Omni takes (times in each source clip; "same" shots cut from another shot's clip)
    "s002": [(6.4, 9.6)],                 # the droplet falls back into the water, light rises where it touched, flares
    "s003": [(0.95, 4.6)],                # s003 take: the point flares, light fills the frame, dims almost to black
    "s004": [(4.6, 7.4)],                 # s003 take: balls of starlight fly past, space opens
    "s005": [(7.4, 10.4)],                # s006 take (s003 extended): the earth grows, Africa and Arabia facing us
    "s006": [(10.4, 12.2)],               # s006 take: into the clouds, the river land opens (cut before farms and houses)
    "s007": [(14.0, 17.0)],               # s006 take: low over palms and groves toward the river
    "s019": [(0.4, 5.2)],                 # from the city up through the clouds; the earth shrinks to one point
    "s020": [(2.0, 10.0)],                # bridge from s019's point: the point becomes a spark; the kiln fire below
    "s022": [(6.8, 9.9)],                 # Omni from the keyframe: he presses the mud, lifts the mould
    "s023": [(0.2, 5.5)],                 # stop before the push ends in an extreme close up (style bible)
}
PREFER_LTX = set()                        # shots where the LTX clip (clips/ltx) beats the Omni one
CROPS = {                                 # by hand: bars() got a clip wrong, or framing must be tightened
}
SHOTS = {s["id"]: s for s in json.loads((FILM / "script/shotlist.json").read_text())}
TITLES = {"s025": ("THE SEVEN DAYS", "Genesis 1:1 to 2:3", 2.9)}   # shot: (title, subtitle, seconds in)


def ff(*a):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *map(str, a)], capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr[-2000:])


def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                       capture_output=True, text=True)
    return float(r.stdout)


def cuts(path):
    """Times of hard cuts inside a clip: a frame that differs from the last far more than the clip's usual motion."""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vf", "scale=48:27,format=gray", "-f", "rawvideo", "-"],
                         capture_output=True).stdout
    n, fps = 48 * 27, 24
    fr = [raw[i:i + n] for i in range(0, len(raw) - n + 1, n)]
    d = [sum(abs(x - y) for x, y in zip(fr[i], fr[i - 1])) / n for i in range(1, len(fr))]
    med = sorted(d)[len(d) // 2] if d else 0
    return [(i + 1) / fps for i, v in enumerate(d) if v > max(18, 6 * med)]


def bars(path):
    """A crop that removes thin black bars Omni sometimes leaves at the edges (up to 80 px a side), or ''."""
    W, H, lim = 1920, 1080, 80
    xs, ys = [], []
    for s in (2.5, 5.0, 8.0):
        g = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(s), "-i", str(path), "-frames:v", "1", "-vf",
                            f"scale={W}:{H},format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
        if len(g) < W * H:
            continue
        col = lambda x: max(g[y * W + x] for y in range(0, H, 8))
        row = lambda y: max(g[y * W:(y + 1) * W:8])
        e = [next((x for x in range(lim) if col(x) > 14), lim), next((x for x in range(lim) if col(W - 1 - x) > 14), lim),
             next((y for y in range(lim) if row(y) > 14), lim), next((y for y in range(lim) if row(H - 1 - y) > 14), lim)]
        xs += [v for v in e[:2] if v < lim]  # a side at the limit is a dark frame, not a bar
        ys += [v for v in e[2:] if v < lim]
    left = right = max(xs, default=0)
    top = bottom = max(ys, default=0)
    x, y = max(left, right), max(top, bottom)
    if x >= lim or y >= lim or (x < 6 and y < 6):
        return ""                            # no bars, or a dark frame where the edges say nothing
    return f"crop={W - 2 * x - 4}:{H - 2 * y - 4},"


def clip_for(sh):
    o = sh.get("omni") or {}
    src = o.get("clip") if o.get("mode") == "same" else sh["id"]
    order = ["ltx", "omni"] if src in PREFER_LTX else ["omni", "ltx"]
    for p in [FILM / "clips" / d / f"{src}.mp4" for d in order] + [FILM / "clips/movement" / f"{src}.mp4"]:
        if p.exists():
            return p
    return None


def auto_window(clip, d):
    """One source range for a shot of d seconds: speed 1, a little faster for montage shots, slowed past the clip."""
    n = probe(clip)
    L = min(n - 0.2, d * (1.5 if d < 1.0 else 1.0))
    a = max(0.2, (n - L) / 2)
    for c in cuts(clip):                     # keep the window inside one continuous stretch
        if a < c < a + L:
            a = c + 0.05 if c < n / 2 else max(0.2, c - L - 0.05)
    return [(round(a, 2), round(min(n, a + L), 2))]


def segment(sh, out, tmp):
    d = sh["dur"]
    clip = clip_for(sh) if sh["kind"] != "graphic" else None
    base = "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1"
    if clip:
        parts = CLIP_TRIMS.get(sh["id"]) or auto_window(clip, d)
        tot = sum(b - a for a, b in parts)
        chain = "".join(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[p{i}];" for i, (a, b) in enumerate(parts))
        chain += "".join(f"[p{i}]" for i in range(len(parts))) + f"concat=n={len(parts)}:v=1:a=0," + (CROPS.get(sh["id"], "") or bars(clip)) + f"{base},"
        slow = d / tot
        chain += f"setpts=PTS*{slow:.4f}," + (f"minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:vsbmc=1[v]"
                                                if slow > 1.15 else f"fps={FPS}[v]")
        ff("-i", clip, "-filter_complex", chain, "-map", "[v]", "-t", f"{d:.3f}", "-an", "-c:v", "libx264", "-crf", "16",
           "-pix_fmt", "yuv420p", "-r", FPS, out)
        return
    if sh["kind"] == "graphic":
        ff("-f", "lavfi", "-i", f"color=c=0x060808:s=1920x1080:r={FPS}:d={d:.3f}", "-c:v", "libx264", "-crf", "16",
           "-pix_fmt", "yuv420p", out)
        return
    img = FILM / (sh["src"] if sh["kind"] == "reuse" else f"stills/movement/{sh['id']}.jpg")
    n = max(2, round(d * FPS))
    fast = d < 1.2                          # montage shots move faster so a 0.8 s shot still feels alive
    z = f"1.04+{0.10 if fast else 0.06}*on/{n}"
    vf = (f"scale=3840:2160:force_original_aspect_ratio=increase,crop=3840:2160,"
          f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s=1920x1080:fps={FPS}")
    if sh["id"] in TITLES:
        from PIL import Image, ImageDraw, ImageFont
        t, sub, at = TITLES[sh["id"]]
        card = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
        dr = ImageDraw.Draw(card)
        f1, f2 = ImageFont.truetype(str(FONT), 110), ImageFont.truetype(str(FONT), 44)
        dr.text((960, 470), t, font=f1, fill=(244, 236, 216, 255), anchor="mm")
        dr.text((960, 580), sub, font=f2, fill=(214, 170, 92, 255), anchor="mm")
        png = tmp / f"title-{sh['id']}.png"
        card.save(png)
        ff("-loop", "1", "-i", img, "-loop", "1", "-i", png, "-filter_complex",
           f"[0:v]{vf}[bg];[1:v]format=rgba,fade=in:st={at}:d=0.8:alpha=1[t];[bg][t]overlay=0:0:shortest=1",
           "-frames:v", n, "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", out)
        return
    ff("-loop", "1", "-i", img, "-vf", vf, "-frames:v", n, "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", out)


def main():
    a, b = float(sys.argv[1]), float(sys.argv[2])
    out = FILM / (sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "exports/preview.mp4")
    shots = [s for s in json.loads((FILM / "script/shotlist.json").read_text()) if a - 0.01 <= s["start"] < b - 0.01]
    tmp = FILM / "edit/preview-tmp"
    tmp.mkdir(parents=True, exist_ok=True)
    parts = []
    for sh in shots:
        p = tmp / f"{sh['id']}.mp4"
        segment(sh, p, tmp)
        parts.append(p)
    lst = tmp / "list.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in parts))
    ff("-f", "concat", "-safe", "0", "-i", lst, "-ss", f"{a}", "-t", f"{b - a}", "-i", FILM / "edit/score/mix.wav",
       "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
       "-shortest", "-movflags", "+faststart", out)
    print(f"{len(shots)} shots -> {out}")


if __name__ == "__main__":
    main()
