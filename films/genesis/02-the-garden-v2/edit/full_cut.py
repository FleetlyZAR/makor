#!/usr/bin/env python3
"""The Garden v2: the full cut (picture on the voice timeline, with edit/score/mix.wav underneath).

Built on The Seven Days v2's edit (01-the-seven-days-v2/edit/preview_cut.py). Each shot from
script/shotlist.json becomes exactly its share of frames at 1920x1080, 24 fps, so the picture never drifts
from the sound. Its picture is, in order: the Omni hero clip (clips/omni; a shot marked "same" cuts from
another shot's take), else the LTX clip (clips/ltx), else its keyframe with a slow push. The clip review
(edit/clip_trims.json) sets the usable part of each clip ("use"), sends shots whose clip failed back to the
keyframe ("still"), and crops baked in borders ("crop"). On screen: the title, the nine verbs as they are
spoken, the names of the four rivers, black under God's line, and the end card.

    python3 films/genesis/02-the-garden-v2/edit/full_cut.py [START END] [--out exports/full-cut-v1.mp4]
"""
import json, pathlib, subprocess, sys

from PIL import Image, ImageDraw, ImageFont

FILM = pathlib.Path(__file__).resolve().parents[1]
FPS = 24
FONT = FILM.parents[1] / "fonts" / "Fraunces[SOFT,WONK,opsz,wght].ttf"
SHOTS = json.loads((FILM / "script/shotlist.json").read_text())
BYID = {s["id"]: s for s in SHOTS}
REVIEW = json.loads((FILM / "edit/clip_trims.json").read_text())
CREAM, GOLD, INK = (244, 236, 216), (214, 170, 92), (6, 8, 8)

# source ranges by hand, in each clip's own seconds (joined to fill the shot)
CLIP_TRIMS = {
    "s001": [(0.0, 2.5)], "s002": [(2.5, 5.0)], "s003": [(5.0, 7.5)], "s004": [(7.5, 10.0)],  # the fall: one Omni take
    "s046": [(0.0, 6.3)], "s047": [(6.3, 10.0)],          # the forming: dust becomes the man, then he lies in the grass
}
TITLE_AT = 42.6                                           # THE GARDEN lands with the low hit (score_mix.py)
RIVERS = {"the Gihon": "GIHON", "the Tigris": "TIGRIS", "And the fourth river": "EUPHRATES"}


def ff(*a):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *map(str, a)], capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr[-2000:])


def probe(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                                capture_output=True, text=True).stdout)


def serif(size, weight=500):
    f = ImageFont.truetype(str(FONT), size)
    f.set_variation_by_axes([min(144, size // 3), weight, 0, 0])
    return f


def overlays():
    """shot id: (text, kind, seconds into the shot)."""
    out = {}
    title = next(s for s in SHOTS if s["start"] <= TITLE_AT < s["start"] + s["dur"])
    out[title["id"]] = ("THE GARDEN|Genesis 2:4 to 25", "title", TITLE_AT - title["start"])
    for s in SHOTS:
        if s.get("verb"):
            out[s["id"]] = (s["verb"], "verb", 0.0)
        if s.get("cue") in RIVERS:
            out[s["id"]] = (RIVERS[s["cue"]], "river", 0.3)
    pishon = next(s for s in SHOTS if s["chapter"] == "Four rivers" and "gold glinting in its bed" in (s["scene"] or ""))
    out[pishon["id"]] = ("PISHON", "river", 0.3)
    return out


def card(text, kind, png):
    im = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if kind == "title":
        t, sub = text.split("|")
        d.text((960, 470), t, font=serif(110, 500), fill=CREAM + (255,), anchor="mm")
        d.text((960, 580), sub, font=serif(44, 400), fill=GOLD + (255,), anchor="mm")
    elif kind == "verb":                                 # one word, centre, as the GUIDE says it
        d.rectangle([0, 450, 1920, 630], fill=(6, 12, 12, 110))
        d.text((960, 540), text, font=serif(120, 600), fill=CREAM + (255,), anchor="mm")
    elif kind == "river":                                # the river's name, top left (the bottom belongs to the Scripture)
        d.text((110, 150), text, font=serif(64, 500), fill=CREAM + (235,), anchor="ls")
        d.line([(110, 172), (110 + 36 * len(text), 172)], fill=GOLD + (220,), width=3)
    im.save(png)


def clip_for(sh):
    if sh["id"] in REVIEW["still"]:
        return None
    o = sh.get("omni") or {}
    src = o.get("clip") if o.get("mode") == "same" else sh["id"]
    for p in (FILM / "clips/omni" / f"{src}.mp4", FILM / "clips/ltx" / f"{src}.mp4"):
        if p.exists():
            return p
    return None


def crop_for(sid):
    c = REVIEW["crop"].get(sid)
    if not c:
        return ""
    l, r, t, b = c.get("l", 0), c.get("r", 0), c.get("t", 0), c.get("b", 0)
    return f"crop=iw*{1 - l - r:.4f}:ih*{1 - t - b:.4f}:iw*{l:.4f}:ih*{t:.4f},"


def window(sh, clip, d):
    if sh["id"] in CLIP_TRIMS:
        return CLIP_TRIMS[sh["id"]]
    n = probe(clip)
    if sh["id"] in REVIEW["use"]:                        # only the clean first part (the review)
        return [(0.1, round(n * REVIEW["use"][sh["id"]], 2))]
    L = min(n - 0.2, d * (1.5 if d < 1.0 else 1.0))      # the middle of the clip, a little faster for montage shots
    a = max(0.2, (n - L) / 2)
    return [(round(a, 2), round(a + L, 2))]


def segment(sh, out, tmp, nf, ov):
    d = nf / FPS
    base = "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1"
    png = None
    if sh["id"] in ov:
        png = tmp / f"ov-{sh['id']}.png"
        card(ov[sh["id"]][0], ov[sh["id"]][1], png)
    over = (lambda at: f";[v0][1:v]overlay=0:0:enable='gte(t,{at:.2f})'[v]") if png else None
    if sh["kind"] == "graphic":
        if "end card" in sh["flags"]:
            im = Image.new("RGB", (1920, 1080), INK)
            dr = ImageDraw.Draw(im)
            dr.text((960, 430), "Study The Garden", font=serif(84, 500), fill=CREAM, anchor="mm")
            dr.text((960, 520), "makor.co.za/genesis/the-garden", font=serif(40, 400), fill=GOLD, anchor="mm")
            dr.text((960, 700), "WATCH NEXT  ·  THE FALL", font=serif(34, 500), fill=CREAM, anchor="mm")
            p = tmp / "endcard.png"
            im.save(p)
            ff("-loop", "1", "-i", p, "-vf", f"fps={FPS},fade=in:d=0.8", "-frames:v", nf, "-c:v", "libx264", "-crf", "16",
               "-pix_fmt", "yuv420p", out)
        else:                                            # black under God's line
            ff("-f", "lavfi", "-i", f"color=c=0x060808:s=1920x1080:r={FPS}", "-frames:v", nf, "-c:v", "libx264",
               "-crf", "16", "-pix_fmt", "yuv420p", out)
        return
    clip = clip_for(sh)
    ins = ["-loop", "1", "-i", png] if png else []
    at = ov[sh["id"]][2] if png else 0
    if clip:
        parts = window(sh, clip, d)
        tot = sum(b - a for a, b in parts)
        chain = "".join(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[p{i}];" for i, (a, b) in enumerate(parts))
        chain += "".join(f"[p{i}]" for i in range(len(parts))) + f"concat=n={len(parts)}:v=1:a=0,"
        chain += crop_for(sh["id"]) + f"{base},"
        slow = d / tot
        chain += f"setpts=PTS*{slow:.4f}," + (f"minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:vsbmc=1"
                                                if slow > 1.15 else f"fps={FPS}") + ",tpad=stop_mode=clone:stop_duration=3"
        chain += ("[v0]" + over(at)) if png else "[v]"
        ff("-i", clip, *ins, "-filter_complex", chain, "-map", "[v]", "-frames:v", nf, "-an", "-c:v", "libx264",
           "-crf", "16", "-pix_fmt", "yuv420p", "-r", FPS, out)
        return
    img = FILM / (sh["src"] if sh["kind"] == "reuse" else f"stills/movement/{sh['id']}.jpg")
    fast = d < 1.2                                       # montage shots move faster so they still feel alive
    z = f"1.04+{0.10 if fast else 0.06}*on/{nf}"
    vf = (f"{crop_for(sh['id'])}scale=3840:2160:force_original_aspect_ratio=increase,crop=3840:2160,"
          f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={nf}:s=1920x1080:fps={FPS}")
    if png:
        ff("-loop", "1", "-i", img, *ins, "-filter_complex", f"[0:v]{vf}[v0]" + over(at), "-map", "[v]",
           "-frames:v", nf, "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", out)
    else:
        ff("-loop", "1", "-i", img, "-vf", vf, "-frames:v", nf, "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", out)


def main():
    args = [x for x in sys.argv[1:] if not x.startswith("--") and not x.startswith("s")]
    T = json.loads((FILM / "script/movement-timeline.json").read_text())
    a, b = (float(args[0]), float(args[1])) if len(args) >= 2 else (0.0, T["total"])
    out = FILM / (sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "exports/full-cut-v1.mp4")
    shots = [s for s in SHOTS if a - 0.01 <= s["start"] < b - 0.01]
    tmp = FILM / "edit/cut-tmp"
    tmp.mkdir(parents=True, exist_ok=True)
    ov, parts = overlays(), []
    redo = set(sys.argv[sys.argv.index("--redo") + 1].split(",")) if "--redo" in sys.argv else set()
    for sh in shots:
        p = tmp / f"{sh['id']}.mp4"
        f0, f1 = round(sh["start"] * FPS), round((sh["start"] + sh["dur"]) * FPS)
        if not p.exists() or not redo or sh["id"] in redo:   # --redo s013,s050 re-renders only those shots
            segment(sh, p, tmp, f1 - f0, ov)
        got = int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                                  "stream=nb_read_frames", "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout)
        assert got == f1 - f0, f"{sh['id']}: {got} frames, wanted {f1 - f0}"
        parts.append(p)
        print(sh["id"], flush=True)
    lst = tmp / "list.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in parts))
    ff("-f", "concat", "-safe", "0", "-i", lst, "-ss", f"{a}", "-t", f"{b - a}", "-i", FILM / "edit/score/mix.wav",
       "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
       "-shortest", "-movflags", "+faststart", out)
    print(f"{len(shots)} shots -> {out}")


if __name__ == "__main__":
    main()
