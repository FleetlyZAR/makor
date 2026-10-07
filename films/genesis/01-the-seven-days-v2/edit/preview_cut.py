#!/usr/bin/env python3
"""Picture preview of a stretch of The Seven Days v2 with the full mix underneath.

Each shot from script/shotlist.json becomes a 1920x1080 segment: Veo clips with their trims
(CLIP_TRIMS: source ranges joined to fill the shot), stills with a slow move, reuse images
likewise, graphics as black. The mix (edit/score/mix.wav) runs underneath. A first, simple cut to
judge picture against sound; the full edit tool comes later.

    python3 films/genesis/01-the-seven-days-v2/edit/preview_cut.py 0 47.1 [--out exports/cold-open-preview.mp4]
"""
import json, pathlib, subprocess, sys

FILM = pathlib.Path(__file__).resolve().parents[1]
FPS = 30
FONT = FILM.parents[1] / "fonts" / "Fraunces[SOFT,WONK,opsz,wght].ttf"
# shot id: list of (start, end) in the clip's own seconds, joined in order to fill the shot
CLIP_TRIMS = {
    "s002": [(0.2, 2.6)],                 # the drop falls, light flashes at the touch
    "s004": [(0.0, 2.6)],                 # vidIQ Veo Fast: star streaks, the earth small and far off
    "s005": [(5.6, 8.0)],                 # same clip: the dive into the atmosphere (the middle shows North America, cut)
    "s006": [(0.0, 2.4)],                 # vidIQ Veo Fast: down through the clouds
    "s007": [(3.0, 6.0)],                 # same clip: gliding low over the palms toward the river
    "s019": [(0.0, 2.4), (6.2, 8.0)],     # vidIQ Veo Fast: the city falls away, the earth recedes, cut to the point
    "s003": [(0.6, 6.6)],                 # vidIQ Veo 3.1: the point erupts, debris past the lens, the fly-through; 6 s into 4 s
}
TITLES = {"s025": ("THE SEVEN DAYS", "Genesis 1:1 to 2:3", 2.9)}   # shot: (title, subtitle, seconds in)


def ff(*a):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *map(str, a)], capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr[-2000:])


def segment(sh, out, tmp):
    d = sh["dur"]
    clip = FILM / "clips/movement" / f"{sh['id']}.mp4"
    base = "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1"
    if sh["kind"] == "veo" and clip.exists():
        parts = CLIP_TRIMS.get(sh["id"], [(0.0, d)])
        tot = sum(b - a for a, b in parts)
        chain = "".join(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[p{i}];" for i, (a, b) in enumerate(parts))
        chain += "".join(f"[p{i}]" for i in range(len(parts))) + f"concat=n={len(parts)}:v=1:a=0,{base},"
        chain += f"setpts=PTS*{d / tot:.4f},fps={FPS}[v]"
        ff("-i", clip, "-filter_complex", chain, "-map", "[v]", "-t", f"{d:.3f}", "-an", "-c:v", "libx264", "-crf", "16",
           "-pix_fmt", "yuv420p", out)
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
