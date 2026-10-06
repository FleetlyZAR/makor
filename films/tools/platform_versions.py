#!/usr/bin/env python3
"""Platform versions of a finished movement film (free, local).

  youtube   16:9: Makor opening (4 s) + the film with a corner mark and one quiet
            like and subscribe prompt at the first natural pause + a 20 s end
            screen laid out for YouTube's Subscribe and Video elements.
  vertical  9:16 for TikTok and Instagram: the film framed in the middle over a
            blurred fill, Makor title band on top, large captions below (Scripture
            with its reference, GUIDE in italics), one follow prompt, end card.
  art       YouTube thumbnail (3840x2160), channel icon (800x800), branding
            watermark (150x150).

    python3 films/tools/platform_versions.py films/genesis/01-the-seven-days youtube vertical art

Reads the v2 edit products: exports/the-seven-days-v2.mp4, edit/movement/picture.mp4,
edit/movement/mix.wav and the script timeline (with the edit's 2 s lead in).
"""
import json, math, pathlib, re, subprocess, sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import movement_edit as me  # noqa: E402

INK, WATER, GOLD, CREAM = (14, 42, 46), (15, 108, 108), (184, 134, 47), (244, 236, 216)
GOLD_TEXT = (214, 170, 92)
SERIF, SERIF_IT, SANS = me.SERIF, "/System/Library/Fonts/NewYorkItalic.ttf", me.SANS
IDENT, END = 4.0, 20.0
URL = "makor.co.za/genesis/the-seven-days"


def ff(*a):
    me.ff(*a)


RING = (58, 176, 170)   # the brighter teal of the app icon rings, readable at small sizes


def serif(size, weight=600):
    """New York at the wordmark's weight (Fraunces 600 on the site)."""
    f = ImageFont.truetype(SERIF, size)
    f.set_variation_by_axes([min(256, max(12, size // 3)), weight, 0])
    return f


def mark(size, alpha=255):
    """The Makor mark: concentric teal rings around the gold source point (public/favicon.svg)."""
    s = size * 4
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = s / 2
    for r, op in [(11 / 32, 0.45), (7.6 / 32, 0.7), (4.2 / 32, 1.0)]:
        rr = r * s
        d.ellipse([c - rr, c - rr, c + rr, c + rr], outline=(*RING, int(255 * op * alpha / 255)), width=max(3, s // 40))
    rr = 1.9 / 32 * s
    d.ellipse([c - rr, c - rr, c + rr, c + rr], fill=(*GOLD, alpha))
    return im.resize((size, size), Image.LANCZOS)


def wordmark(height, colour=CREAM):
    f = serif(height)
    w = int(ImageDraw.Draw(Image.new("RGB", (1, 1))).textlength("Makor", font=f)) + 10
    im = Image.new("RGBA", (w, int(height * 1.35)), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((0, 0), "Makor", font=f, fill=colour)
    return im


def lockup(h):
    """Mark beside the wordmark, as in the site header."""
    m, w = mark(h), wordmark(int(h * 0.62))
    im = Image.new("RGBA", (m.width + int(h * 0.18) + w.width, h), (0, 0, 0, 0))
    im.paste(m, (0, 0), m)
    im.paste(w, (m.width + int(h * 0.18), (h - w.height) // 2 + int(h * 0.06)), w)
    return im


def halo(img, colour=(6, 18, 20), blur=10, k=1.5):
    a = img.split()[3]
    h = Image.new("RGBA", img.size, (*colour, 0))
    h.putalpha(a.filter(ImageFilter.GaussianBlur(blur)).point(lambda p: min(255, int(p * k))))
    return Image.alpha_composite(h, img)


def setup(film):
    """The v2 timeline with the edit's lead in applied."""
    tl = json.loads((film / "script" / "movement-timeline.json").read_text())
    durs = json.loads((film / "script" / "movement-durations.json").read_text())
    for e in tl["events"]:
        e["t"] += me.LEAD
    tl["chapters"] = [[t + (me.LEAD if i else 0), n] for i, (t, n) in enumerate(tl["chapters"])]
    tl["total"] += me.LEAD + me.TAIL
    return tl, durs


def cta_window(tl, durs):
    """The last quiet moment before Day One: no Scripture on screen, between GUIDE lines."""
    day1 = next(t for t, n in tl["chapters"] if n.startswith("Day One"))
    return day1 - 9.0, day1 - 1.5


# ---------------------------------------------------------------- YouTube
def ident(film, out_dir):
    fdir = out_dir / "ident"
    fdir.mkdir(parents=True, exist_ok=True)
    n = int(IDENT * 30)
    lock = lockup(150)
    for i in range(n):
        t = i / 30
        img = Image.new("RGB", (1920, 1080), (8, 22, 24))
        d = ImageDraw.Draw(img, "RGBA")
        c = (960, 470)
        grow = min(1, t / 1.6)
        for k, (r, op) in enumerate([(300, 0.35), (210, 0.6), (120, 0.9)]):
            rr = r * (0.6 + 0.4 * math.sin(grow * math.pi / 2))
            a = int(255 * op * min(1, max(0, (t - 0.2 * k) / 0.8)))
            d.ellipse([c[0] - rr, c[1] - rr, c[0] + rr, c[1] + rr], outline=(*RING, a), width=5)
        dot = 46 * min(1, max(0, (t - 0.5) / 0.7))
        d.ellipse([c[0] - dot, c[1] - dot, c[0] + dot, c[1] + dot], fill=(*GOLD, 255))
        wa = min(1, max(0, (t - 1.4) / 0.8))
        if wa:
            w = wordmark(96)
            w.putalpha(w.split()[3].point(lambda p: int(p * wa)))
            img.paste(w, (960 - w.width // 2, 820), w)
        fade = min(1, max(0, (IDENT - t) / 0.6))
        if fade < 1:
            img = Image.blend(Image.new("RGB", img.size, (0, 0, 0)), img, fade)
        img.save(fdir / f"{i:04d}.png")
    out = out_dir / "ident.mp4"
    ff("-framerate", 30, "-i", fdir / "%04d.png", "-i", film / "audio" / "sfx" / "light-swell.mp3",
       "-filter_complex", f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{IDENT},volume=0.5,"
       f"afade=out:st={IDENT - 1}:d=1,apad=whole_dur={IDENT}[a]",
       "-map", "0:v", "-map", "[a]", "-t", IDENT, "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p",
       "-c:a", "aac", "-b:a", "192k", out)
    return out


def endscreen(film, out_dir, tl):
    bg = Image.open(film / "stills" / "movement" / "s027.jpg").convert("RGB").resize((1920, 1072))
    bg = bg.crop((0, 0, 1920, 1072)).resize((1920, 1080)).filter(ImageFilter.GaussianBlur(6))
    bg = Image.blend(bg, Image.new("RGB", bg.size, (8, 22, 24)), 0.45).convert("RGBA")
    d = ImageDraw.Draw(bg)
    lock = lockup(110)
    bg.alpha_composite(halo(lock), (960 - lock.width // 2, 70))
    f1, f2 = ImageFont.truetype(SERIF, 54), ImageFont.truetype(SANS, 36, index=2)
    t = Image.new("RGBA", bg.size, (0, 0, 0, 0))
    td = ImageDraw.Draw(t)
    td.text((960, 220), "Study The Seven Days", font=f1, fill=CREAM, anchor="ma")
    td.text((960, 296), URL, font=f2, fill=GOLD_TEXT, anchor="ma")
    # quiet labels above the spaces YouTube's end screen elements will fill (set in YouTube Studio)
    lab = ImageFont.truetype(SANS, 30, index=0)
    td.text((240 + 400, 430), "WATCH NEXT", font=lab, fill=(200, 205, 200), anchor="ma")
    td.text((1500, 430), "SUBSCRIBE", font=lab, fill=(200, 205, 200), anchor="ma")
    bg.alpha_composite(halo(t))
    p = out_dir / "endscreen.png"
    bg.convert("RGB").save(p)
    out = out_dir / "endscreen.mp4"
    act6 = film / "audio" / "music" / "act6.wav"
    start = max(0, me.dur(act6) - END - 2)
    ff("-loop", 1, "-framerate", 30, "-t", END, "-i", p, "-ss", start, "-i", act6, "-filter_complex",
       f"[0:v]scale=3840:-2,zoompan=z='1+0.04*(on/{int(END * 30)})':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
       f"d={int(END * 30)}:s=1920x1080:fps=30,fade=in:d=1,fade=out:st={END - 1.5}:d=1.5[v];"
       f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{END},volume=0.35,afade=in:d=2,"
       f"afade=out:st={END - 4}:d=4[a]",
       "-map", "[v]", "-map", "[a]", "-t", END, "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p",
       "-c:a", "aac", "-b:a", "192k", out)
    return out


def cta_png(path, kind, w=1920, h=1080, x=None, y=None, scale=1.0):
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(SANS, int(34 * scale), index=0)
    small = ImageFont.truetype(SANS, int(28 * scale), index=5)
    if kind == "youtube":
        pills = [("LIKE", False), ("SUBSCRIBE", True)]
        line = "for every movement of Scripture, one study at a time"
    else:
        pills = [("FOLLOW MAKOR", True)]
        line = "for every movement of Scripture, one study at a time"
    x = 110 if x is None else x
    y = h - 300 if y is None else y
    m = mark(int(84 * scale))
    img.alpha_composite(m, (x, y - int(4 * scale)))
    cx = x + m.width + int(24 * scale)
    for text, filled in pills:
        tw = d.textlength(text, font=f)
        box = [cx, y + int(8 * scale), cx + tw + int(56 * scale), y + int(72 * scale)]
        if filled:
            d.rounded_rectangle(box, radius=int(32 * scale), fill=(*GOLD, 255))
            d.text((box[0] + int(28 * scale), y + int(40 * scale)), text, font=f, fill=INK, anchor="lm")
        else:
            d.rounded_rectangle(box, radius=int(32 * scale), outline=(*CREAM, 255), width=max(2, int(3 * scale)),
                                fill=(8, 22, 24, 150))
            d.text((box[0] + int(28 * scale), y + int(40 * scale)), text, font=f, fill=CREAM, anchor="lm")
        cx = box[2] + int(18 * scale)
    d.text((x + m.width + int(26 * scale), y + int(96 * scale)), line, font=small, fill=CREAM)
    halo(img, blur=8).save(path)


def youtube(film):
    out_dir = film / "edit" / "youtube"
    out_dir.mkdir(parents=True, exist_ok=True)
    tl, durs = setup(film)
    a, b = cta_window(tl, durs)
    cta = out_dir / "cta.png"
    cta_png(cta, "youtube")
    wm = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    lk = lockup(54)
    lk.putalpha(lk.split()[3].point(lambda p: int(p * 0.6)))
    wm.alpha_composite(lk, (1920 - lk.width - 60, 50))
    wm.save(out_dir / "watermark.png")
    idp, endp = ident(film, out_dir), endscreen(film, out_dir, tl)
    main = film / "exports" / "the-seven-days-v2.mp4"
    total = me.dur(main)
    wm_from = next(t for t, n in tl["chapters"] if n.startswith("A world")) - 2
    fc = (f"[3:v]format=rgba[wm];[4:v]format=rgba,fade=in:st=0:d=0.6:alpha=1,"
          f"fade=out:st={b - a - 0.8:.2f}:d=0.8:alpha=1,setpts=PTS+{a:.3f}/TB[cta];"
          f"[1:v][wm]overlay=0:0:enable='between(t,{wm_from:.2f},{total - 10:.2f})'[m1];"
          f"[m1][cta]overlay=0:0:eof_action=pass:enable='between(t,{a:.2f},{b:.2f})'[m2];"
          f"[0:v][0:a][m2][1:a][2:v][2:a]concat=n=3:v=1:a=1[v][araw]")
    raw = out_dir / "youtube-raw.mp4"
    ff("-i", idp, "-i", main, "-i", endp, "-i", out_dir / "watermark.png",
       "-loop", 1, "-framerate", 30, "-t", f"{b - a:.3f}", "-i", cta,
       "-filter_complex", fc, "-map", "[v]", "-map", "[araw]", "-c:v", "libx264", "-crf", "18", "-preset", "slow",
       "-pix_fmt", "yuv420p", "-r", 30, "-c:a", "pcm_s16le", raw.with_suffix(".mov"))
    final = film / "exports" / "the-seven-days-youtube.mp4"
    loudnorm_copy(raw.with_suffix(".mov"), final)
    print(f"youtube: {final} {me.dur(final):.2f}s; prompt at {a + IDENT:.1f} to {b + IDENT:.1f}s")
    return a + IDENT, b + IDENT


def loudnorm_copy(src, dest):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(src), "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True)
    blob = r.stderr[r.stderr.rindex("{"):]
    m = json.loads(blob[:blob.index("}") + 1])
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    ff("-i", src, "-c:v", "copy", "-af", ln, "-ar", 48000, "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", dest)


# ---------------------------------------------------------------- vertical
VW, VH = 1080, 1920
PIC_Y = 470          # top of the 1080x608 film frame
CAP_TOP = 1150       # captions start; kept clear of TikTok and Reels UI (bottom ~420 px, right ~150 px)


def v_caption(path, label, text, italic):
    img = Image.new("RGBA", (VW, VH), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(SERIF_IT if italic else SERIF, 52)
    rows = me.wrap(d, text, f, 820)
    y = CAP_TOP
    if label:
        d.text((500, y), label.upper(), font=ImageFont.truetype(SANS, 30, index=0), fill=GOLD_TEXT, anchor="ma")
        y += 50
    for r in rows[:5]:
        d.text((500, y), r, font=f, fill=CREAM, anchor="ma"); y += 66
    halo(img, blur=7).save(path)


def vertical(film):
    out_dir = film / "edit" / "vertical"
    cdir = out_dir / "captions"
    cdir.mkdir(parents=True, exist_ok=True)
    tl, durs = setup(film)
    # top band: Makor lockup and the film title; chapter name below it
    top = Image.new("RGBA", (VW, VH), (0, 0, 0, 0))
    bd = ImageDraw.Draw(top)
    for yy in range(0, PIC_Y + 20):          # ink band behind the title area
        bd.line([(0, yy), (VW, yy)], fill=(8, 22, 24, int(205 * min(1, (PIC_Y + 20 - yy) / 140))))
    for yy in range(PIC_Y + 588, VH):        # and behind the captions
        bd.line([(0, yy), (VW, yy)], fill=(8, 22, 24, int(150 * min(1, (yy - PIC_Y - 588) / 160))))
    lk = lockup(96)
    top.alpha_composite(lk, (540 - lk.width // 2, 140))
    td = ImageDraw.Draw(top)
    td.text((540, 268), "THE SEVEN DAYS", font=serif(66), fill=CREAM, anchor="ma")
    td.text((540, 348), "GENESIS 1:1 TO 2:3", font=ImageFont.truetype(SANS, 30, index=0), fill=GOLD_TEXT, anchor="ma")
    halo(top).save(out_dir / "top.png")
    items = []
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    f = ImageFont.truetype(SERIF, 52)
    for e in tl["events"]:
        if e["kind"] != "line":
            continue
        t0, t1 = e["t"], e["t"] + durs[e["id"]]
        cards = me.chunks(e["text"], probe, f, 820, max_lines=5)
        tot = sum(len(c) for c in cards)
        t = t0
        for k, c in enumerate(cards):
            tt = t + (t1 - t0) * len(c) / tot
            p = cdir / f"{e['id']}-{k}.png"
            v_caption(p, "" if e["speaker"] == "GUIDE" else e.get("ref", ""), c, e["speaker"] == "GUIDE")
            items.append((p, t - 0.1, tt + 0.25 if k == len(cards) - 1 else tt))
            t = tt
    for i, (t, name) in enumerate(tl["chapters"]):
        p = cdir / f"chapter-{i:02d}.png"
        img = Image.new("RGBA", (VW, VH), (0, 0, 0, 0))
        ImageDraw.Draw(img).text((540, 405), name.upper(), font=ImageFont.truetype(SANS, 28, index=2),
                                 fill=(200, 210, 205), anchor="ma")
        halo(img).save(p)
        end = tl["chapters"][i + 1][0] if i + 1 < len(tl["chapters"]) else tl["total"]
        items.append((p, t, end))
    for e in tl["events"]:   # the closing study card
        if e["kind"] == "card" and "makor.co.za" in e["text"]:
            p = cdir / "endcard.png"
            img = Image.new("RGBA", (VW, VH), (0, 0, 0, 0))
            d = ImageDraw.Draw(img)
            d.text((540, CAP_TOP + 10), "Study The Seven Days", font=ImageFont.truetype(SERIF, 60), fill=CREAM, anchor="ma")
            d.text((540, CAP_TOP + 100), URL, font=ImageFont.truetype(SANS, 36, index=2), fill=GOLD_TEXT, anchor="ma")
            halo(img).save(p)
            items.append((p, e["t"], tl["total"]))
    a, b = cta_window(tl, durs)
    cta = out_dir / "cta.png"
    cta_png(cta, "follow", VW, VH, x=90, y=1180 - 40, scale=1.0)
    items.append((cta, a, b))
    pic = film / "edit" / "movement" / "picture.mp4"
    ins = ["-i", str(pic), "-i", str(film / "edit" / "movement" / "mix.wav"), "-i", str(out_dir / "top.png")]
    fc = [f"[0:v]split[a][b];"
          f"[a]scale=-2:{VH},crop={VW}:{VH},boxblur=30:2,eq=brightness=-0.18:saturation=0.8[bg];"
          f"[b]scale={VW}:-2[fg];[bg][2:v]overlay=0:0[bgt];[bgt][fg]overlay=0:{PIC_Y}[t0]"]
    prev = "[t0]"
    for k, (p, s, e) in enumerate(items, 3):
        L = e - s
        ins += ["-loop", "1", "-framerate", "30", "-t", f"{L:.3f}", "-i", str(p)]
        fc.append(f"[{k}:v]format=rgba,fade=in:st=0:d=0.25:alpha=1,fade=out:st={max(0, L - 0.3):.3f}:d=0.3:alpha=1,"
                  f"setpts=PTS+{s:.3f}/TB[o{k}]")
        fc.append(f"{prev}[o{k}]overlay=0:0:eof_action=pass:enable='between(t,{s:.3f},{e:.3f})'[p{k}]")
        prev = f"[p{k}]"
    graph = out_dir / "graph.txt"
    graph.write_text(";".join(fc))
    out = film / "exports" / "the-seven-days-vertical.mp4"
    ff(*ins, "-/filter_complex", graph, "-map", prev, "-map", "1:a", "-t", f"{tl['total']:.3f}",
       "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", 30,
       "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out)
    print(f"vertical: {out} {me.dur(out):.2f}s, {len(items)} overlays")


# ---------------------------------------------------------------- art
def art(film):
    out = film / "exports" / "art"
    out.mkdir(parents=True, exist_ok=True)
    W, H = 3840, 2160
    for name, src in [("thumbnail-a", "s025"), ("thumbnail-b", "s087")]:
        bg = Image.open(film / "stills" / "movement" / f"{src}.jpg").convert("RGB")
        r = max(W / bg.width, H / bg.height)
        bg = bg.resize((int(bg.width * r) + 1, int(bg.height * r) + 1), Image.LANCZOS).crop((0, 0, W, H)).convert("RGBA")
        shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sd = ImageDraw.Draw(shade)
        for x in range(W):   # ink gradient from the left so the title reads
            a = int(215 * max(0, 1 - x / (W * 0.62)) ** 1.3)
            sd.line([(x, 0), (x, H)], fill=(8, 22, 24, a))
        bg.alpha_composite(shade)
        t = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(t)
        d.text((220, 640), "THE SEVEN", font=serif(330, 560), fill=CREAM)
        d.text((220, 990), "DAYS", font=serif(330, 560), fill=CREAM)
        d.text((230, 1400), "GENESIS 1:1 TO 2:3", font=ImageFont.truetype(SANS, 92, index=0), fill=GOLD_TEXT)
        bg.alpha_composite(halo(t, blur=18))
        lk = lockup(230)
        bg.alpha_composite(halo(lk), (230, 1720))
        bg.convert("RGB").save(out / f"{name}.jpg", quality=90)
    icon = Image.open(film.parents[2] / "assets" / "icon.png").convert("RGB").resize((800, 800), Image.LANCZOS)
    icon.save(out / "channel-icon-800.png")
    mark(150).save(out / "branding-watermark-150.png")
    print(f"art: {out}")


def main():
    film = pathlib.Path(sys.argv[1]).resolve()
    steps = sys.argv[2:] or ["youtube", "vertical", "art"]
    if "art" in steps:
        art(film)
    if "youtube" in steps:
        youtube(film)
    if "vertical" in steps:
        vertical(film)


if __name__ == "__main__":
    main()
