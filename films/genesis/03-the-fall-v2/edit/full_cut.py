#!/usr/bin/env python3
"""The Fall v2: the full cut (picture on the voice timeline, with edit/score/mix.wav underneath).

Built on The Garden v2's edit (02-the-garden-v2/edit/full_cut.py). Each shot from script/shotlist.json becomes
exactly its share of frames at 1920x1080, 24 fps, so the picture never drifts from the sound. Its picture is, in
order: a clip it borrows (`clip`, The Garden v2's own clips, played backward when `reverse`), the Omni hero clip
(clips/omni; a shot marked "same" cuts from another shot's take), the LTX clip (clips/ltx), else its keyframe
with a slow push. edit/clip_trims.json (from the clip review) sets the usable part of each clip ("use"), sends
failed clips back to the keyframe ("still"), and crops baked in borders ("crop").

On screen: the title; the words of the lie built against God's words (Genesis 2:16 to 17 and 3:2 to 5, BSB);
the Hebrew words with their meaning; the shape of the blame; AND THEN HE DIED; black under God's question; the
end card. Text stays above the bottom 120 px (YouTube's controls).

    python3 films/genesis/03-the-fall-v2/edit/full_cut.py [START END] [--out exports/full-cut-v1.mp4] [--redo s013,s050]
"""
import json, pathlib, subprocess, sys

from PIL import Image, ImageDraw, ImageFont

FILM = pathlib.Path(__file__).resolve().parents[1]
FPS = 24
FONT = FILM.parents[1] / "fonts" / "Fraunces[SOFT,WONK,opsz,wght].ttf"
SHOTS = json.loads((FILM / "script/shotlist.json").read_text())
BYID = {s["id"]: s for s in SHOTS}
TRIMS_F = FILM / "edit/clip_trims.json"
REVIEW = json.loads(TRIMS_F.read_text()) if TRIMS_F.exists() else {"use": {}, "still": [], "crop": {}, "range": {}}
CREAM, GOLD, INK, EMBER = (244, 236, 216), (214, 170, 92), (6, 8, 8), (226, 120, 70)

# Omni takes: the usable seconds (edit/clip-review.md); "same" shots cut from the wind take s074
CLIP_TRIMS = {"s052": [(0.0, 9.0)], "s172": [(0.0, 5.0)], "s206": [(0.0, 5.0)],
              "s074": [(0.0, 3.0)], "s076": [(3.0, 5.5)], "s077": [(5.5, 8.0)]}
TITLE_AT = 39.4

GODS = ("“You may eat freely from every tree of the garden, but you must not eat from the tree of the knowledge "
        "of good and evil; for in the day that you eat of it, you will surely die.”")
HERS = ("“We may eat the fruit of the trees of the garden, but about the fruit of the tree in the middle of the "
        "garden, God has said, ‘You must not eat of it or touch it, or you will die.’”")
HIS = "“You will not surely die,” the serpent told the woman."


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


def wrap(d, text, f, width):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) > width and cur:
            lines.append(cur); cur = w
        else:
            cur = t
    return lines + [cur]


def compare_card(im, step):
    """The lie built on screen: God's words, hers, the serpent's (steps 1 to 3), then the name dropping out (4)."""
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 1920, 1080], fill=(6, 10, 10, 150))
    if step == 4:
        d.text((960, 430), "THE LORD GOD", font=serif(110, 500), fill=CREAM + (255,), anchor="mm")
        d.text((960, 560), "the narrator", font=serif(38, 400), fill=GOLD + (255,), anchor="mm")
        d.text((960, 700), "GOD", font=serif(110, 500), fill=CREAM + (150,), anchor="mm")
        d.text((960, 820), "the serpent and the woman", font=serif(38, 400), fill=GOLD + (200,), anchor="mm")
        return
    f, small = serif(40, 400), serif(30, 500)
    y = 150
    for label, text, show in (("GOD, Genesis 2:16 to 17", GODS, True), ("THE WOMAN, Genesis 3:2 to 3", HERS, step >= 1),
                              ("THE SERPENT, Genesis 3:4", HIS, step >= 3)):
        if not show:
            continue
        d.text((180, y), label, font=small, fill=GOLD + (255,))
        y += 50
        for line in wrap(d, text, f, 1560):
            d.text((180, y), line, font=f, fill=CREAM + (255,))
            # the changed words, marked as the GUIDE names them
            for word, colour, strike in (("freely", EMBER, step >= 2 and label.startswith("GOD")),
                                         ("surely", EMBER, step >= 2 and label.startswith("GOD")),
                                         ("or touch it,", EMBER, False), ("not surely", EMBER, False)):
                if word in line and (strike or (word == "or touch it," and step >= 2 and "WOMAN" in label)
                                     or (word == "not surely" and step >= 3 and "SERPENT" in label)):
                    x0 = 180 + d.textlength(line[:line.index(word)], font=f)
                    x1 = x0 + d.textlength(word, font=f)
                    if strike:
                        d.text((x0, y), word, font=f, fill=EMBER + (255,))
                        d.line([(x0, y + 26), (x1, y + 26)], fill=EMBER + (255,), width=3)
                    else:
                        d.text((x0, y), word, font=f, fill=EMBER + (255,))
            y += 56
        y += 40


def blame_card(im, step):
    """serpent, woman, man: the sin runs down (1), the questions and blame run back (2), the sentences (3)."""
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 1920, 1080], fill=(6, 10, 10, 120))
    xs, y = (480, 960, 1440), 470
    f = serif(64, 500)
    for x, name in zip(xs, ("SERPENT", "WOMAN", "MAN")):
        d.text((x, y), name, font=f, fill=CREAM + (255,), anchor="mm")
    lab = serif(34, 400)

    def arrow(x0, x1, yy, colour):
        d.line([(x0, yy), (x1, yy)], fill=colour + (255,), width=4)
        s = 18 if x1 > x0 else -18
        d.polygon([(x1, yy), (x1 - s, yy - 10), (x1 - s, yy + 10)], fill=colour + (255,))

    if step >= 1:
        arrow(580, 840, y - 90, GOLD); arrow(1080, 1340, y - 90, GOLD)
        d.text((960, y - 150), "the sin", font=lab, fill=GOLD + (255,), anchor="mm")
    if step >= 2:
        arrow(1340, 1080, y + 90, EMBER); arrow(840, 580, y + 90, EMBER)
        d.text((960, y + 150), "the questions, and the blame passed back", font=lab, fill=EMBER + (255,), anchor="mm")
    if step >= 3:
        d.text((960, y + 260), "the sentences: serpent, woman, man", font=lab, fill=CREAM + (255,), anchor="mm")


def overlays():
    """shot id: (text, kind, seconds into the shot)."""
    out = {}
    title = next(s for s in SHOTS if s["start"] <= TITLE_AT < s["start"] + s["dur"])
    out[title["id"]] = ("THE FALL|Genesis 3:1 to 24", "title", TITLE_AT - title["start"])
    steps = {"Genesis 2:16 to 17": 1, "FREELY fades": 2, "NOT drops": 3, "THE LORD GOD": 4}
    for s in SHOTS:
        if s.get("verb"):
            out[s["id"]] = (s["verb"], "word", 0.2)
        for k, n in steps.items():
            if k in (s.get("note") or ""):
                out[s["id"]] = (str(n), "compare", 0.0)
    return out


def card(text, kind, png):
    im = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if kind == "title":
        t, sub = text.split("|")
        d.rectangle([0, 380, 1920, 650], fill=(6, 12, 12, 130))      # the ink band, so it reads on gold and cream
        d.text((960, 470), t, font=serif(110, 500), fill=CREAM + (255,), anchor="mm")
        d.text((960, 580), sub, font=serif(44, 400), fill=GOLD + (255,), anchor="mm")
    elif kind == "word":                                 # a Hebrew word and its meaning, or a phrase, centre
        top, _, sub = text.partition(" / ")
        d.rectangle([0, 420, 1920, 680], fill=(6, 12, 12, 110))
        d.text((960, 520 if sub else 550), top, font=serif(104, 600), fill=CREAM + (255,), anchor="mm")
        if sub:
            d.text((960, 615), sub.lower() if top.isupper() and len(top.split()) == 1 else sub, font=serif(54, 400),
                   fill=GOLD + (255,), anchor="mm")
    elif kind == "compare":
        compare_card(im, int(text))
    im.save(png)


def clip_for(sh):
    if sh["id"] in REVIEW["still"]:
        return None
    if sh.get("clip"):
        p = FILM / sh["clip"]
        return p if p.exists() else None
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
    if sh["id"] in REVIEW.get("range", {}):
        return [tuple(r) for r in REVIEW["range"][sh["id"]]]
    if sh["id"] in CLIP_TRIMS and "clips/omni" in str(clip):
        return CLIP_TRIMS[sh["id"]]
    n = probe(clip)
    if sh.get("reverse"):                                # the whole clip, played backward (dust to dust)
        return [(0.0, round(n - 0.05, 2))]
    if sh["id"] in REVIEW["use"]:                        # only the clean first part (the review)
        return [(0.1, round(n * REVIEW["use"][sh["id"]], 2))]
    L = min(n - 0.2, d * (1.5 if d < 1.0 else 1.0))      # the middle of the clip, a little faster for montage shots
    a = max(0.2, (n - L) / 2)
    return [(round(a, 2), round(a + L, 2))]


def still_card(sh, nf, tmp):
    """Graphic shots: black, black with words, the blame over its background, the end card."""
    f = sh["flags"]
    if "end card" in f:
        im = Image.new("RGB", (1920, 1080), INK)
        dr = ImageDraw.Draw(im)
        dr.text((960, 430), "Study The Fall", font=serif(84, 500), fill=CREAM, anchor="mm")
        dr.text((960, 520), "makor.co.za/genesis/the-fall", font=serif(40, 400), fill=GOLD, anchor="mm")
        dr.text((960, 700), "WATCH NEXT  ·  CAIN AND ABEL", font=serif(34, 500), fill=CREAM, anchor="mm")
        return im, "fade=in:d=0.8"
    if "AND THEN HE DIED" in f:
        im = Image.new("RGB", (1920, 1080), INK)
        dr = ImageDraw.Draw(im)
        dr.text((960, 520), "AND THEN HE DIED", font=serif(96, 500), fill=CREAM, anchor="mm")
        dr.text((960, 620), "Genesis 5:5", font=serif(40, 400), fill=GOLD, anchor="mm")
        return im, "fade=in:d=0.4"
    return None, None


def segment(sh, out, tmp, nf, ov):
    d = nf / FPS
    base = "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1"
    enc = ["-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p"]
    if sh["kind"] == "graphic":
        if sh["flags"].startswith("graphic") and sh.get("src"):     # the blame, drawn over a slow push on its picture
            step = 1 if "draws down" in sh["flags"] else 2 if "climb back" in sh["flags"] else 3
            png = tmp / f"ov-{sh['id']}.png"
            im = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
            blame_card(im, step)
            im.save(png)
            vf = (f"scale=3840:2160:force_original_aspect_ratio=increase,crop=3840:2160,"
                  f"zoompan=z='1.04+0.05*on/{nf}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={nf}:s=1920x1080:fps={FPS}")
            ff("-loop", "1", "-i", FILM / sh["src"], "-loop", "1", "-i", png, "-filter_complex",
               f"[0:v]{vf}[v0];[v0][1:v]overlay=0:0[v]", "-map", "[v]", "-frames:v", nf, *enc, out)
            return
        im, fx = still_card(sh, nf, tmp)
        if im:
            p = tmp / f"card-{sh['id']}.png"
            im.save(p)
            ff("-loop", "1", "-i", p, "-vf", f"fps={FPS},{fx}", "-frames:v", nf, *enc, out)
        else:                                            # black (God's question, the boom, before the end card)
            ff("-f", "lavfi", "-i", f"color=c=0x060808:s=1920x1080:r={FPS}", "-frames:v", nf, *enc, out)
        return
    png = None
    if sh["id"] in ov:
        png = tmp / f"ov-{sh['id']}.png"
        card(ov[sh["id"]][0], ov[sh["id"]][1], png)
    over = (lambda at: f";[v0][1:v]overlay=0:0:enable='gte(t,{at:.2f})'[v]") if png else None
    clip = clip_for(sh)
    ins = ["-loop", "1", "-i", png] if png else []
    at = ov[sh["id"]][2] if png else 0
    if clip:
        parts = window(sh, clip, d)
        tot = sum(b - a for a, b in parts)
        chain = "".join(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[p{i}];" for i, (a, b) in enumerate(parts))
        chain += "".join(f"[p{i}]" for i in range(len(parts))) + f"concat=n={len(parts)}:v=1:a=0,"
        if sh.get("reverse") or sh["id"] in REVIEW.get("reverse", []):
            chain += "reverse,"
        chain += crop_for(sh["id"]) + f"{base},"
        slow = d / tot
        chain += f"setpts=PTS*{slow:.4f}," + (f"minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:vsbmc=1"
                                                if slow > 1.15 else f"fps={FPS}") + ",tpad=stop_mode=clone:stop_duration=3"
        chain += ("[v0]" + over(at)) if png else "[v]"
        ff("-i", clip, *ins, "-filter_complex", chain, "-map", "[v]", "-frames:v", nf, "-an", *enc, "-r", FPS, out)
        return
    img = FILM / (sh["src"] if sh["kind"] == "reuse" else f"stills/movement/{sh['id']}.jpg")
    fast = d < 1.2                                       # montage shots move faster so they still feel alive
    z = f"1.04+{0.10 if fast else 0.06}*on/{nf}"
    vf = (f"{crop_for(sh['id'])}scale=3840:2160:force_original_aspect_ratio=increase,crop=3840:2160,"
          f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={nf}:s=1920x1080:fps={FPS}")
    if png:
        ff("-loop", "1", "-i", img, *ins, "-filter_complex", f"[0:v]{vf}[v0]" + over(at), "-map", "[v]",
           "-frames:v", nf, *enc, out)
    else:
        ff("-loop", "1", "-i", img, "-vf", vf, "-frames:v", nf, *enc, out)


def main():
    args = [x for x in sys.argv[1:] if not x.startswith("--") and not x.startswith("s") and not x.startswith("exports")]
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
