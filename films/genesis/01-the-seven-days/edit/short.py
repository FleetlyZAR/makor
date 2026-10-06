#!/usr/bin/env python3
"""The Seven Days in a minute: the GUIDE led short from script/one-minute-script.md.

9:16, 1080x1920, 30 fps, -14 LUFS, under 60 s. Free: the film's own READER and GOD
renders, the GUIDE lines rendered locally (audio/short/g1..g4.wav), the film's 2K
keyframes recropped to 9:16, and a tall version of the forming and filling panels.

Outputs exports/seven-days-in-a-minute.mp4 (Reels, Shorts, TikTok) and
exports/seven-days-in-a-minute-whatsapp.mp4 (720x1280, light, for WhatsApp Status).

    python3 films/genesis/01-the-seven-days/edit/short.py
"""
import json, pathlib, subprocess, sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

FILM = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(FILM.parents[2] / "films" / "tools"))
import movement_edit as me  # noqa: E402
import platform_versions as pv  # noqa: E402

W, H, FPS, XF = 1080, 1920, 30, 0.4
OUT = FILM / "edit" / "short"
GAP = 0.4
SERIF_IT = "/System/Library/Fonts/NewYorkItalic.ttf"
STUDY = FILM.parents[2] / "src/content/studies/genesis/01-the-seven-days.json"
pv.URL = json.loads((FILM / "film.json").read_text())["url"]


def ff(*a):
    me.ff(*a)


def dur(p):
    return me.dur(p)


# ------------------------------------------------------------------ lines
def lines():
    mv = FILM / "audio" / "movement"
    sh = FILM / "audio" / "short"
    lt = {x["id"]: x for x in json.loads((FILM / "script" / "movement-lines.json").read_text())}
    guide = {
        "g1": "Genesis opens on a world that is formless and void: not yet shaped, and not yet filled.",
        "g2": "Watch the pattern. Days one to three give it shape: light, sky and sea, dry land. Days four to six fill it: lights, birds and fish, animals and people.",
        "g3": "Then the pattern breaks. The seventh day has no evening. God rests, not because He is tired, but because the work is finished, and good.",
        "g4": "And the Bible's last pages answer its first: a new creation, with God Himself as its light.",
    }
    def film_line(lid, gap_after=GAP):
        x = lt[lid]
        return dict(file=next(mv.glob(f"{lid}-*")), speaker=x["speaker"], text=x["text"], ref=x["ref"], gap=gap_after)
    def g(k):
        return dict(file=sh / f"{k}.wav", speaker="GUIDE", text=guide[k], ref="", gap=GAP)
    seq = [film_line("m001"), g("g1"), film_line("m018", 0.5), film_line("m019", 1.0), film_line("m020"),
           g("g2"), film_line("m068"), g("g3"), g("g4")]
    # Scripture in the short must be verbatim from the study JSON
    import re
    study = re.sub(r"\{\{[^|}]+\|([^}]+)\}\}", r"\1", STUDY.read_text())
    for x in seq:
        if x["speaker"] != "GUIDE":
            assert x["text"].strip("“”") in study or x["text"] in study, x["text"]
    t = 0.8
    for x in seq:
        x["t"], x["d"] = t, dur(x["file"])
        t += x["d"] + x["gap"]
    return seq, t - GAP + 0.3


# ------------------------------------------------------------------ pictures
def crop916(src, xfrac=0.5):
    im = Image.open(FILM / "stills" / "movement" / f"{src}.jpg").convert("RGB")
    cw = int(im.height * 9 / 16)
    x = int((im.width - cw) * xfrac)
    return im.crop((x, 0, x + cw, im.height)).resize((W * 2, H * 2), Image.LANCZOS)


def panel(path, w, h):
    im = Image.open(FILM / path).convert("RGB")
    r = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * r) + 1, int(im.height * r) + 1), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def panels_tall():
    """Forming and filling as two columns of three, for a tall frame."""
    img = Image.new("RGB", (W * 2, H * 2), pv.INK)
    d = ImageDraw.Draw(img)
    head, lab = pv.serif(96), ImageFont.truetype(me.SANS, 64, index=2)
    pw, ph, gx = 940, 560, 60   # three rows end above the caption band
    x0, y0 = (W * 2 - 2 * pw - gx) // 2, 420
    d.text((x0 + pw // 2, y0 - 140), "FORMING", font=head, fill=pv.GOLD_TEXT, anchor="ma")
    d.text((x0 + pw + gx + pw // 2, y0 - 140), "FILLING", font=head, fill=pv.GOLD_TEXT, anchor="ma")
    form = ["stills/movement/s025.jpg", "stills/movement/s035.jpg", "stills/world/shot-01.jpg"]   # as frame_graphic.py
    fill = ["stills/world/shot-03.jpg", "stills/world/shot-05.jpg", "stills/world/shot-07.jpg"]
    cols = [(form, ["Day 1", "Day 2", "Day 3"]), (fill, ["Day 4", "Day 5", "Day 6"])]
    for c, (paths, labels) in enumerate(cols):
        x = x0 + c * (pw + gx)
        for r, (p, t) in enumerate(zip(paths, labels)):
            y = y0 + r * (ph + 40)
            img.paste(panel(p, pw, ph), (x, y))
            d.rectangle([x, y, x + pw, y + ph], outline=pv.GOLD, width=6)
            tw = d.textlength(t, font=lab)
            d.rectangle([x + 24, y + ph - 110, x + 70 + tw, y + ph - 24], fill=pv.INK)
            d.text((x + 46, y + ph - 67), t, font=lab, fill=pv.CREAM, anchor="lm")
    return img


def seg(img, L, out, zoom=(1.0, 1.08)):
    p = out.with_suffix(".png")
    img.save(p)
    n = round(L * FPS)
    z0, z1 = zoom
    ff("-loop", 1, "-framerate", FPS, "-i", p, "-vf",
       f"zoompan=z='{z0}+{z1 - z0}*(on/{n})':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps={FPS},"
       "setsar=1", "-frames:v", n, "-an", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", out)
    return out


def endcard_img():
    bg = crop916("s027").filter(ImageFilter.GaussianBlur(10))
    bg = Image.blend(bg, Image.new("RGB", bg.size, (8, 22, 24)), 0.5).convert("RGBA")
    t = Image.new("RGBA", bg.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(t)
    lk = pv.lockup(220)
    t.alpha_composite(lk, (W - lk.width // 2, 980))
    d.text((W, 1330), "The Seven Days", font=pv.serif(150), fill=pv.CREAM, anchor="ma")
    d.text((W, 1540), "FULL FILM ON YOUTUBE", font=ImageFont.truetype(me.SANS, 64, index=0), fill=pv.GOLD_TEXT, anchor="ma")
    d.text((W, 1680), "Study it at", font=ImageFont.truetype(me.SANS, 60, index=5), fill=pv.CREAM, anchor="ma")
    d.text((W, 1770), pv.URL, font=ImageFont.truetype(me.SANS, 70, index=2), fill=pv.GOLD_TEXT, anchor="ma")
    f = ImageFont.truetype(me.SANS, 70, index=0)
    tw = d.textlength("FOLLOW MAKOR", font=f)
    box = [W - tw / 2 - 70, 2000, W + tw / 2 + 70, 2150]
    d.rounded_rectangle(box, radius=75, fill=(*pv.GOLD, 255))
    d.text((W, 2075), "FOLLOW MAKOR", font=f, fill=pv.INK, anchor="mm")
    bg.alpha_composite(pv.halo(t, blur=16))
    return bg.convert("RGB")


def ident_img(alpha):
    img = Image.new("RGB", (W * 2, H * 2), (8, 22, 24))
    m = pv.mark(700)
    m.putalpha(m.split()[3].point(lambda p: int(p * alpha)))
    img.paste(m, (W - 350, H - 350), m)
    return img


def build_picture(seq, total):
    OUT.mkdir(parents=True, exist_ok=True)
    s = {i: x for i, x in enumerate(seq)}
    g1, v3a, god, v3b, g2, v27, g3, g4 = s[1], s[2], s[3], s[4], s[5], s[6], s[7], s[8]
    end_t = g4["t"] + g4["d"] + 0.3
    cuts = []   # (name, image or builder, start, end, zoom)
    cuts.append(("ident", ident_img(1.0), 0, 0.8, (1.0, 1.15)))
    cuts.append(("s001", crop916("s001"), 0.8, g1["t"] - 0.2, (1.0, 1.06)))
    mid = g1["t"] + 3.4
    cuts.append(("s002", crop916("s002"), g1["t"] - 0.2, mid, (1.0, 1.06)))
    cuts.append(("s003", crop916("s003", 0.35), mid, v3a["t"] - 0.2, (1.0, 1.06)))
    cuts.append(("dark", crop916("s024"), v3a["t"] - 0.2, god["t"] + god["d"] + 0.1, (1.0, 1.04)))
    cuts.append(("light", crop916("s025"), god["t"] + god["d"] + 0.1, g2["t"] - 0.2, (1.04, 1.1)))
    m0, m1 = g2["t"] - 0.2, g2["t"] + 7.6
    mont = ["s035", "s045", "s052", "s059"]
    step = (m1 - m0) / len(mont)
    for k, src in enumerate(mont):
        cuts.append((src, crop916(src, 0.5 if src != "s052" else 0.3), m0 + k * step, m0 + (k + 1) * step, (1.0, 1.06)))
    cuts.append(("panels", panels_tall(), m1, v27["t"] - 0.2, (1.0, 1.04)))
    cuts.append(("s074", crop916("s074", 0.42), v27["t"] - 0.2, g3["t"] - 0.2, (1.0, 1.06)))
    half = g3["t"] + 4.6
    cuts.append(("s090", crop916("s090"), g3["t"] - 0.2, half, (1.0, 1.05)))
    cuts.append(("s093", crop916("s093"), half, g4["t"] - 0.2, (1.0, 1.05)))
    cuts.append(("s118", crop916("s118"), g4["t"] - 0.2, end_t, (1.0, 1.06)))
    cuts.append(("end", endcard_img(), end_t, total, (1.0, 1.03)))
    files = []
    for k, (name, img, a, b, z) in enumerate(cuts):
        pad = XF / 2 * ((k > 0) + (k < len(cuts) - 1))
        files.append(seg(img, b - a + pad, OUT / f"{k:02d}-{name}.mp4", z))
    ins = sum([["-i", str(f)] for f in files], [])
    fc, prev = [], "[0:v]"
    for k in range(1, len(cuts)):
        fc.append(f"{prev}[{k}:v]xfade=transition=fade:duration={XF}:offset={cuts[k][2] - XF / 2:.3f}[x{k}]")
        prev = f"[x{k}]"
    fc.append(f"{prev}fade=out:st={total - 0.8:.2f}:d=0.8[v]")
    pic = OUT / "picture.mp4"
    ff(*ins, "-filter_complex", ";".join(fc), "-map", "[v]", "-t", f"{total:.3f}", "-an", "-c:v", "libx264",
       "-crf", "16", "-pix_fmt", "yuv420p", pic)
    return pic, cuts


# ------------------------------------------------------------------ captions
def cap_png(path, label, text, italic):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(SERIF_IT if italic else pv.SERIF, 58)
    rows = me.wrap(d, text, f, 800)
    block = len(rows) * 74 + (52 if label else 0)
    top = max(1240, 1330 - block // 2)
    band = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(band)
    t0, t1 = top - 90, top + block + 90
    for yy in range(t0, t1):
        fr = (yy - t0) / (t1 - t0)
        bd.line([(0, yy), (W, yy)], fill=(8, 22, 24, int(170 * (1 - abs(2 * fr - 1) ** 2.2))))
    y = top
    if label:
        d.text((495, y), label.upper(), font=ImageFont.truetype(me.SANS, 32, index=0), fill=pv.GOLD_TEXT, anchor="ma")
        y += 52
    for r in rows:
        d.text((495, y), r, font=f, fill=pv.CREAM, anchor="ma"); y += 74
    Image.alpha_composite(band, pv.halo(img, blur=7)).save(path)


# ------------------------------------------------------------------ audio
def build_audio(seq, total):
    ins, ch, vox = [], [], []
    for k, x in enumerate(seq):
        ins += ["-i", str(x["file"])]
        ch.append(f"[{k}:a]aformat=sample_rates=48000:channel_layouts=stereo,loudnorm=I=-18:LRA=7:TP=-2,"
                  f"aresample=48000,adelay={int(x['t'] * 1000)}:all=1[v{k}]")
        vox.append(f"[v{k}]")
    n = len(seq)
    god = seq[3]
    light_t = god["t"] + god["d"] + 0.1
    music = FILM / "audio" / "music" / "light-breaking.wav"
    ins += ["-ss", f"{141.0 - light_t:.2f}", "-i", str(music)]   # the track's swell lands on the light
    ch.append(f"[{n}:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{total:.2f},volume=0.5,"
              f"afade=in:d=1.5,afade=out:st={total - 3:.2f}:d=3[mus]")
    sfx = [("wind-deep-water.mp3", seq[1]["t"] - 0.5, seq[2]["t"], 0.4),
           ("rumble-under-god.mp3", god["t"] - 0.6, god["t"] + 5, 0.55),
           ("light-swell.mp3", light_t - 0.6, light_t + 5.4, 0.5),
           ("movement/seabirds.mp3", seq[5]["t"] + 3, seq[5]["t"] + 8, 0.25),
           ("movement/herds.mp3", seq[5]["t"] + 5, seq[6]["t"], 0.25),
           ("movement/golden-stillness.mp3", seq[7]["t"] - 0.3, seq[8]["t"], 0.35),
           ("movement/new-creation.mp3", seq[8]["t"] - 0.3, total, 0.35)]
    fx = []
    for j, (cue, a, b, vol) in enumerate(sfx, n + 1):
        L = b - a
        ins += ["-stream_loop", "-1", "-i", str(FILM / "audio" / "sfx" / cue)]
        ch.append(f"[{j}:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{L:.2f},afade=in:d=0.8,"
                  f"afade=out:st={max(0, L - 1):.2f}:d=1,volume={vol},adelay={int(a * 1000)}:all=1[f{j}]")
        fx.append(f"[f{j}]")
    ch.append(f"{''.join(vox)}amix=inputs={len(vox)}:normalize=0,apad=whole_dur={total:.2f},asplit[vo][key]")
    ch.append(f"{''.join(fx)}amix=inputs={len(fx)}:normalize=0[sfx]")
    ch.append("[mus][key]sidechaincompress=threshold=0.02:ratio=7:attack=30:release=500[musd]")
    ch.append(f"[vo][musd][sfx]amix=inputs=3:normalize=0,atrim=0:{total:.3f}[mix]")
    raw = OUT / "mix-raw.wav"
    ff(*ins, "-filter_complex", ";".join(ch), "-map", "[mix]", "-ar", 48000, raw)
    return raw


def main():
    seq, total = lines()
    end_t = seq[-1]["t"] + seq[-1]["d"] + 0.3
    total = end_t + 4.2
    assert total < 60, f"short runs {total:.1f}s"
    pic, cuts = build_picture(seq, total)
    raw = build_audio(seq, total)
    cdir = OUT / "captions"
    cdir.mkdir(exist_ok=True)
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    f = ImageFont.truetype(pv.SERIF, 58)
    items = []
    # 1:3 builds as it is spoken, like the pilot
    built = ""
    for k, x in enumerate(seq):
        lab = "" if x["speaker"] == "GUIDE" else x["ref"]
        if x["ref"] == "Genesis 1:3":
            built = f"{built} {x['text']}".strip()
            end = x["t"] + x["d"] + (0.25 if x["text"].startswith("and there") else x["gap"])
            p = cdir / f"{k:02d}.png"
            cap_png(p, lab, built, False)
            items.append((p, x["t"] - 0.1, end))
            continue
        cards = me.chunks(x["text"], probe, f, 800, max_lines=4)
        tot = sum(len(c) for c in cards)
        t = x["t"]
        for j, c in enumerate(cards):
            tt = t + x["d"] * len(c) / tot
            p = cdir / f"{k:02d}-{j}.png"
            cap_png(p, lab, c, x["speaker"] == "GUIDE")
            items.append((p, t - 0.1, tt + 0.25 if j == len(cards) - 1 else tt))
            t = tt
    ins, fc, prev = ["-i", str(pic)], [], "[0:v]"
    for k, (p, a, b) in enumerate(items, 1):
        L = b - a
        ins += ["-loop", "1", "-framerate", str(FPS), "-t", f"{L:.3f}", "-i", str(p)]
        fc.append(f"[{k}:v]format=rgba,fade=in:st=0:d=0.2:alpha=1,fade=out:st={max(0, L - 0.25):.3f}:d=0.25:alpha=1,"
                  f"setpts=PTS+{a:.3f}/TB[o{k}]")
        fc.append(f"{prev}[o{k}]overlay=0:0:eof_action=pass:enable='between(t,{a:.3f},{b:.3f})'[p{k}]")
        prev = f"[p{k}]"
    ins += ["-i", str(raw)]
    cut = OUT / "captioned.mov"
    ff(*ins, "-filter_complex", ";".join(fc), "-map", prev, "-map", f"{len(items) + 1}:a", "-t", f"{total:.3f}",
       "-c:v", "libx264", "-crf", "17", "-preset", "slow", "-pix_fmt", "yuv420p", "-r", FPS, "-c:a", "pcm_s16le", cut)
    final = FILM / "exports" / "seven-days-in-a-minute.mp4"
    pv.loudnorm_copy(cut, final)
    wa = FILM / "exports" / "seven-days-in-a-minute-whatsapp.mp4"
    ff("-i", final, "-vf", "scale=720:1280", "-c:v", "libx264", "-crf", "27", "-preset", "slow", "-pix_fmt", "yuv420p",
       "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", wa)
    print(f"short: {final} {dur(final):.2f}s; whatsapp copy {wa.stat().st_size // 1024} KB; {len(items)} captions")


if __name__ == "__main__":
    main()
