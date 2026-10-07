#!/usr/bin/env python3
"""The Fall in a minute: the GUIDE led short from script/one-minute-script.md.

9:16, 1080x1920, 30 fps, -14 LUFS, under 60 s. Free: the film's own READER and GOD
renders, the GUIDE lines rendered locally (audio/short/g1..g5.wav, edit/short_guide.py),
and the film's 2K keyframes recropped to 9:16. Adapted from The Garden's edit/short.py.

Outputs exports/the-fall-in-a-minute.mp4 (Reels, Shorts, TikTok) and
exports/the-fall-in-a-minute-whatsapp.mp4 (720x1280, light, for WhatsApp Status).

    python3 films/genesis/03-the-fall/edit/short.py
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
STUDY = FILM.parents[2] / "src/content/studies/genesis/03-the-fall.json"
SD = FILM.parent / "01-the-seven-days"
GD = FILM.parent / "02-the-garden"
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
    guide = {   # draft for C4; rendered by edit/short_guide.py
        "g1": "If the world began so good, why is it like this? Genesis three answers.",
        "g2": "The serpent contradicts God word for word. The root of sin is not ignorance, but distrust.",
        "g3": "God comes looking for the guilty. And before He sentences the man and the woman, He makes a promise.",
        "g4": "The first announcement of the gospel: the seed of the woman will crush the serpent.",
        "g5": "And God covers their shame. In Christ, He still does.",
    }
    def film_line(lid, gap_after=GAP):
        x = lt[lid]
        return dict(file=next(mv.glob(f"{lid}-*")), speaker=x["speaker"], text=x["text"], ref=x["ref"], gap=gap_after)
    def g(k):
        return dict(file=sh / f"{k}.wav", speaker="GUIDE", text=guide[k], ref="", gap=GAP)
    seq = [g("g1"), film_line("m010"), g("g2"), film_line("m021", 0.3), film_line("m022"),
           g("g3"), film_line("m039"), g("g4"), film_line("m054"), g("g5")]
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
    bg = crop916("s101").filter(ImageFilter.GaussianBlur(10))
    bg = Image.blend(bg, Image.new("RGB", bg.size, (8, 22, 24)), 0.5).convert("RGBA")
    t = Image.new("RGBA", bg.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(t)
    lk = pv.lockup(220)
    t.alpha_composite(lk, (W - lk.width // 2, 980))
    d.text((W, 1330), "The Fall", font=pv.serif(150), fill=pv.CREAM, anchor="ma")
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
    g1, v34, g2, v39a, v39b, g3, v315, g4, v321, g5 = seq
    end_t = g5["t"] + g5["d"] + 0.3
    half = lambda x, k=0.5: x["t"] + x["d"] * k
    cuts = []   # (name, image, start, end, zoom)
    cuts.append(("ident", ident_img(1.0), 0, 0.8, (1.0, 1.15)))
    cuts.append(("s001", crop916("s001"), 0.8, half(g1), (1.0, 1.06)))
    cuts.append(("s004", crop916("s004", 0.6), half(g1), v34["t"] - 0.2, (1.0, 1.05)))
    cuts.append(("s015", crop916("s015", 0.8), v34["t"] - 0.2, g2["t"] - 0.2, (1.0, 1.05)))
    cuts.append(("s012", crop916("s012", 0.6), g2["t"] - 0.2, half(g2), (1.0, 1.06)))
    cuts.append(("s017", crop916("s017"), half(g2), v39a["t"] - 0.2, (1.0, 1.05)))
    cuts.append(("s031", crop916("s031"), v39a["t"] - 0.2, g3["t"] - 0.2, (1.0, 1.05)))
    cuts.append(("s036", crop916("s036"), g3["t"] - 0.2, half(g3), (1.0, 1.06)))
    cuts.append(("s037", crop916("s037"), half(g3), v315["t"] - 0.2, (1.0, 1.05)))
    cuts.append(("s046", crop916("s046", 0.45), v315["t"] - 0.2, half(v315), (1.0, 1.05)))
    cuts.append(("s050", crop916("s050", 0.4), half(v315), g4["t"] - 0.2, (1.0, 1.06)))
    cuts.append(("s054", crop916("s054"), g4["t"] - 0.2, v321["t"] - 0.2, (1.0, 1.05)))
    cuts.append(("s071", crop916("s071", 0.25), v321["t"] - 0.2, g5["t"] - 0.2, (1.0, 1.05)))
    cuts.append(("s094", crop916("s094", 0.45), g5["t"] - 0.2, half(g5), (1.0, 1.06)))
    cuts.append(("s097", crop916("s097", 0.6), half(g5), end_t, (1.0, 1.05)))
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
    top = max(1120, min(1240, 1460 - block))   # whole block inside the 1120 to 1460 caption band
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
    v315 = seq[6]
    xf = v315["t"] - 1.0                    # the dark act, then act6's light theme from the promise
    mus = SD / "audio" / "music"
    ins += ["-i", str(mus / "act1.wav"), "-i", str(mus / "act6.wav")]
    ch.append(f"[{n}:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{xf + 2:.2f},"
              f"afade=in:d=1.5,afade=out:st={xf:.2f}:d=2[m1]")
    ch.append(f"[{n + 1}:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{total - xf:.2f},"
              f"afade=in:d=2,afade=out:st={total - xf - 3:.2f}:d=3,adelay={int(xf * 1000)}:all=1[m2]")
    ch.append(f"[m1][m2]amix=inputs=2:normalize=0,apad=whole_dur={total:.2f},atrim=0:{total:.2f},volume=0.5[mus]")
    S = FILM / "audio" / "sfx" / "movement"
    GS = GD / "audio" / "sfx" / "movement"
    SS = SD / "audio" / "sfx" / "movement"
    sfx = [(S / "grass-rustle.mp3", 0.8, seq[2]["t"], 0.35),
           (GS / "great-trees-wind.mp3", seq[2]["t"] - 0.3, seq[3]["t"], 0.25),
           (S / "evening-wind-trees.mp3", seq[3]["t"] - 0.3, seq[6]["t"], 0.4),
           (GS / "dry-wind-plain.mp3", seq[6]["t"] - 0.3, seq[7]["t"], 0.3),
           (SS / "golden-stillness.mp3", seq[7]["t"] - 0.3, seq[8]["t"], 0.25),
           (SS / "garden-dawn.mp3", seq[8]["t"] - 0.3, seq[9]["t"], 0.3),
           (SS / "new-creation.mp3", seq[9]["t"] - 0.3, total, 0.3)]
    fx = []
    for j, (cue, a, b, vol) in enumerate(sfx, n + 2):
        L = b - a
        ins += ["-stream_loop", "-1", "-i", str(cue)]
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
    total = end_t + 3.6
    assert total < 60, f"short runs {total:.1f}s"
    pic, cuts = build_picture(seq, total)
    raw = build_audio(seq, total)
    cdir = OUT / "captions"
    cdir.mkdir(exist_ok=True)
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    f = ImageFont.truetype(pv.SERIF, 58)
    items = []
    for k, x in enumerate(seq):
        lab = "" if x["speaker"] == "GUIDE" else x["ref"]
        cards = me.chunks(x["text"], probe, f, 800, max_lines=3)   # keep clear of the bottom 420 px
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
    final = FILM / "exports" / "the-fall-in-a-minute.mp4"
    pv.loudnorm_copy(cut, final)
    wa = FILM / "exports" / "the-fall-in-a-minute-whatsapp.mp4"
    ff("-i", final, "-vf", "scale=720:1280", "-c:v", "libx264", "-crf", "27", "-preset", "slow", "-pix_fmt", "yuv420p",
       "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", wa)
    print(f"short: {final} {dur(final):.2f}s; whatsapp copy {wa.stat().st_size // 1024} KB; {len(items)} captions")


if __name__ == "__main__":
    main()
