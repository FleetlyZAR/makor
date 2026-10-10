#!/usr/bin/env python3
"""The Seven Days v2: the finished YouTube video, wrapped around the full cut (exports/full-cut-v2.mp4).

Branding and writing from films/tools/platform_versions.py (the Makor mark, wordmark, prompt pills, Fraunces), so
the series looks the same from film to film:

  title card  the Makor lockup above THE SEVEN DAYS and "Genesis · Episode 1" below it, as the title lands
  chapters    a quiet chapter title as each movement begins (an eyebrow such as DAY ONE over its name)
  Scripture   the reference, lower left, as each verse begins to be read (Genesis 1:3, John 1:1 ...)
  corner mark the lockup, top right, from the end of the cold open until the end screen
  prompts     like and subscribe at two natural pauses; a comment prompt on the closing question
  end screen  20 s, with labelled spaces for YouTube's Video and Subscribe elements (set in YouTube Studio)

Writes exports/the-seven-days-v2-youtube.mp4 (loudness -14 LUFS for YouTube), the captions
(exports/the-seven-days-v2-youtube.srt) and edit/youtube/chapters.txt for the description.

    python3 films/genesis/01-the-seven-days-v2/edit/youtube_cut.py
"""
import json, pathlib, subprocess, sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

FILM = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(FILM.parents[1] / "tools"))
import platform_versions as pv  # noqa: E402

OUT = FILM / "edit" / "youtube"
MAIN = FILM / "exports" / "full-cut-v4.mp4"
FINAL = FILM / "exports" / "the-seven-days-v2-youtube.mp4"
END = 20.0
T = json.loads((FILM / "script" / "movement-timeline.json").read_text())
DURS = json.loads((FILM / "script" / "movement-durations.json").read_text())
EYEBROW = {
    "A world of other stories": "ISRAEL IN EGYPT", "In the beginning": "DAY ONE", "Formless and void": "THE PATTERN",
    "The world takes shape": "DAYS TWO AND THREE", "The first sunrise": "DAY FOUR", "The sea teems": "DAY FIVE",
    "The image of God": "DAY SIX", "Rest": "DAY SEVEN", "In the beginning was the Word": "THE WORD",
    "All things new": "THE LAST PAGES", "Light in a dark place": "FOR YOU",
}
# Day Six opens with the land animals, so its card says so; "The image of God" comes on "Let Us make man"
LET_US = next(e["t"] for e in T["events"] if e["kind"] == "line" and e["text"].startswith("\u201cLet Us make man"))
EXTRA_CHAPTERS = [[LET_US, "The image of God"]]
SHOWN = {("The image of God", round(next(t for t, n in T["chapters"] if n == "The image of God"))): "Living creatures"}
TITLE_AT = (42.6, 47.0)                  # the title card lands 2.9 s into s025 (edit/preview_cut.py TITLES)
PROMPTS = [("youtube", 92.0, 99.6),     # before In the beginning: the hook has landed, the story is about to start
           ("youtube", 702.0, 710.0),   # Rest: the quiet after "very good" and the seventh day
           ("comment", 883.0, 893.0)]   # the closing question: "Where do you need to ask God to speak light ..."


def ff(*a):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *map(str, a)], capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr[-3000:])


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout)


def canvas():
    return Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))


SCRIPTURE_BOOKS = ("Genesis", "Exodus", "John", "Matthew", "Revelation")
CAP_W = 1500                                 # caption width; two lines at most, above YouTube's controls


def wrap(text, font, width):
    words, lines, cur = text.split(), [], ""
    d = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    for w in words:
        test = (cur + " " + w).strip()
        if d.textlength(test, font=font) <= width or not cur:
            cur = test
        else:
            lines.append(cur)
            cur = w
    return lines + ([cur] if cur else [])


def chunks(text, a, b):
    """Split a spoken line into pieces of at most two caption lines, each timed by its share of the characters
    (the voices keep an even pace), so the words on screen follow the voice."""
    f = pv.serif(46, 500)
    lines = wrap(text, f, CAP_W)
    pieces = [" ".join(lines[i:i + 2]) for i in range(0, len(lines), 2)]
    total = sum(len(x) for x in pieces)
    out, t = [], a
    for x in pieces:
        d = (b - a) * len(x) / total
        out.append((x, t, t + d))
        t += d
    out[-1] = (out[-1][0], out[-1][1], b + 0.4)      # the last piece lingers a moment after the voice
    return out


def scripture_png(p, text, ref, god):
    img = canvas()
    f = pv.serif(46, 500)
    lines = wrap(text, f, CAP_W)
    # a soft, feathered shade behind the words, so they read over bright water, grass and dust (5:46, 7:45, 8:05)
    from PIL import ImageFilter
    widest = max(ImageDraw.Draw(img).textlength(ln, font=f) for ln in lines)
    top = 905 - 58 * len(lines) - 26
    shade = Image.new("L", img.size, 0)
    ImageDraw.Draw(shade).rounded_rectangle([960 - widest / 2 - 90, top - 10, 960 + widest / 2 + 90, 960], radius=60, fill=135)
    shade = shade.filter(ImageFilter.GaussianBlur(44))
    img = Image.composite(Image.new("RGBA", img.size, (6, 14, 16, 255)), img, shade)
    d = ImageDraw.Draw(img)
    colour = (240, 218, 168) if god else pv.CREAM
    y = 905 - 58 * len(lines)                     # the block ends above the reference, which ends above y 940
    for ln in lines:
        d.text((960, y), ln, font=f, fill=colour, anchor="ma")
        y += 58
    d.text((960, y + 8), ref.upper(), font=pv.serif(26, 600), fill=pv.GOLD_TEXT, anchor="ma")
    pv.halo(img, blur=9, k=1.8).save(p)


def title_png(p):
    img = canvas()
    lk = pv.lockup(84)
    img.alpha_composite(pv.halo(lk), (960 - lk.width // 2, 300))
    t = canvas()
    td = ImageDraw.Draw(t)
    # the film's title (the title card shot is a moving clip now, so the title is drawn here, not in the cut)
    td.text((960, 470), "THE SEVEN DAYS", font=pv.serif(110, 600), fill=pv.CREAM, anchor="mm")
    td.text((960, 580), "Genesis 1:1 to 2:3", font=pv.serif(44, 400), fill=pv.GOLD_TEXT, anchor="mm")
    td.text((960, 650), "GENESIS  ·  EPISODE 1", font=pv.serif(30, 500), fill=pv.CREAM, anchor="ma")
    img.alpha_composite(pv.halo(t, blur=6))
    img.save(p)


def chapter_png(p, name, brow_text):
    from PIL import ImageFilter
    img = canvas()
    brow, f = pv.serif(28, 600), pv.serif(64, 500)
    x, y = 110, 70          # top left: the bottom of the frame belongs to the Scripture
    w = ImageDraw.Draw(img).textlength(name, font=f)
    shade = Image.new("L", img.size, 0)        # the same soft shade as the Scripture, for bright skies
    ImageDraw.Draw(shade).rounded_rectangle([x - 70, y - 40, x + w + 70, y + 160], radius=60, fill=125)
    img = Image.composite(Image.new("RGBA", img.size, (6, 14, 16, 255)), img, shade.filter(ImageFilter.GaussianBlur(44)))
    d = ImageDraw.Draw(img)
    d.text((x, y), brow_text, font=brow, fill=pv.GOLD_TEXT)
    d.line([(x, y + 46), (x + 90, y + 46)], fill=(*pv.GOLD, 255), width=3)
    d.text((x, y + 62), name, font=f, fill=pv.CREAM)
    pv.halo(img, blur=10).save(p)


def ref_png(p, ref):
    # inside YouTube's safe area: the bottom ~120 px sit under the player's controls and progress bar on phones
    img = canvas()
    d = ImageDraw.Draw(img)
    m = pv.mark(48)
    img.alpha_composite(m, (120, 870))
    d.text((182, 895), ref.upper(), font=pv.serif(38, 600), fill=pv.GOLD_TEXT, anchor="lm")
    pv.halo(img, blur=8).save(p)


def comment_png(p):
    img = canvas()
    d = ImageDraw.Draw(img)
    f, small = pv.serif(34, 600), pv.serif(28, 400)
    m = pv.mark(84)
    x, y = 110, 780
    img.alpha_composite(m, (x, y - 4))
    cx = x + m.width + 24
    text = "TELL US IN THE COMMENTS"
    tw = d.textlength(text, font=f)
    d.rounded_rectangle([cx, y + 8, cx + tw + 56, y + 72], radius=32, fill=(*pv.GOLD, 255))
    d.text((cx + 28, y + 40), text, font=f, fill=pv.INK, anchor="lm")
    d.text((cx + 2, y + 96), "Where do you need God to speak light into a dark place?", font=small, fill=pv.CREAM)
    pv.halo(img, blur=8).save(p)


def watermark_png(p):
    img = canvas()
    lk = pv.lockup(54)
    lk.putalpha(lk.split()[3].point(lambda v: int(v * 0.6)))
    img.alpha_composite(lk, (1920 - lk.width - 60, 50))
    img.save(p)


def endscreen():
    """20 s: the city of light behind, the study link, and labelled spaces for YouTube's end screen elements."""
    bg = Image.open(FILM / "stills" / "movement" / "s148.jpg").convert("RGB").resize((1920, 1080))
    bg = Image.blend(bg.filter(ImageFilter.GaussianBlur(8)), Image.new("RGB", bg.size, (8, 22, 24)), 0.5).convert("RGBA")
    lk = pv.lockup(96)
    bg.alpha_composite(pv.halo(lk), (960 - lk.width // 2, 60))
    t = canvas()
    td = ImageDraw.Draw(t)
    td.text((960, 196), "Study The Seven Days", font=pv.serif(52, 500), fill=pv.CREAM, anchor="ma")
    td.text((960, 268), "makor.co.za/genesis/the-seven-days", font=pv.serif(32, 400), fill=pv.GOLD_TEXT, anchor="ma")
    lab = pv.serif(28, 600)
    # YouTube's elements: a video at left (640x360 at 120,420 in Studio's grid) and Subscribe at right
    td.text((440, 372), "WATCH NEXT  ·  THE GARDEN", font=lab, fill=(220, 222, 214), anchor="ma")
    td.rounded_rectangle([120, 420, 760, 780], radius=12, outline=(*pv.CREAM, 90), width=2)
    td.text((1480, 372), "SUBSCRIBE", font=lab, fill=(220, 222, 214), anchor="ma")
    td.ellipse([1380, 470, 1580, 670], outline=(*pv.CREAM, 90), width=2)
    td.text((960, 900), "Genesis 2 to 3 continues the story", font=pv.serif(30, 400), fill=pv.CREAM, anchor="ma")
    bg.alpha_composite(pv.halo(t))
    png = OUT / "endscreen.png"
    bg.convert("RGB").save(png)
    music = FILM / "audio" / "music-v2" / "theme-word.wav"
    start = max(0.0, dur(music) - END - 2)
    out = OUT / "endscreen.mp4"
    n = int(END * 24)
    ff("-loop", 1, "-framerate", 24, "-t", END, "-i", png, "-ss", start, "-i", music, "-filter_complex",
       f"[0:v]scale=3840:-2,zoompan=z='1+0.03*(on/{n})':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s=1920x1080:fps=24,"
       f"fade=in:d=1,fade=out:st={END - 1.5}:d=1.5[v];[1:a]aformat=sample_rates=48000:channel_layouts=stereo,"
       f"atrim=0:{END},volume=0.35,afade=in:d=2,afade=out:st={END - 4}:d=4[a]",
       "-map", "[v]", "-map", "[a]", "-t", END, "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p",
       "-c:a", "aac", "-b:a", "192k", out)
    return out


def overlays():
    """(png, start, end) for everything laid over the film."""
    items = []
    p = OUT / "title.png"
    title_png(p)
    items.append((p, *TITLE_AT))
    for t, name in T["chapters"] + EXTRA_CHAPTERS:
        if name in EYEBROW:
            p = OUT / f"chapter-{int(t):04d}.png"
            chapter_png(p, SHOWN.get((name, round(t)), name), EYEBROW[name])
            items.append((p, t + 0.8, t + 5.3))
    # the Scripture itself on screen as it is read (READER and GOD lines), with its reference; the GUIDE's teaching
    # stays in the caption file only, so the frame never fills with text
    k = 0
    for e in T["events"]:
        ref = e.get("ref", "")
        if e["kind"] != "line" or e.get("speaker") not in ("READER", "GOD") or not ref.split(" ")[0] in SCRIPTURE_BOOKS:
            continue
        a, b = e["t"], e["t"] + DURS.get(e["id"], 2.0)
        ref = ref.replace(", flash-forward", "")
        for text, ca, cb in chunks(e["text"], a, b):
            k += 1
            p = OUT / f"scripture-{k:03d}.png"
            scripture_png(p, text, ref, e["speaker"] == "GOD")
            items.append((p, ca, cb))
    for kind, a, b in PROMPTS:
        p = OUT / f"prompt-{int(a):04d}.png"
        comment_png(p) if kind == "comment" else pv.cta_png(p, "youtube")
        items.append((p, a, b))
    return items


def srt():
    def tc(s):
        h, m = divmod(int(s), 3600)
        m, sec = divmod(m, 60)
        return f"{h:02d}:{m:02d}:{sec:02d},{int((s % 1) * 1000):03d}"
    rows = [(e["t"], e["t"] + DURS.get(e["id"], 2.0), e["text"]) for e in T["events"] if e["kind"] == "line"]
    (FINAL.with_suffix(".srt")).write_text("".join(f"{i}\n{tc(a)} --> {tc(b)}\n{x}\n\n" for i, (a, b, x) in
                                                   enumerate(rows, 1)))


def chapters_txt():
    lines = ["0:00 The Seven Days"]
    for t, name in sorted(T["chapters"][1:] + EXTRA_CHAPTERS):
        shown = SHOWN.get((name, round(t)), name)
        brow = EYEBROW.get(name, "")
        label = f"{brow.title().replace(' And ', ' and ')}: {shown}" if brow.startswith("DAY") else shown
        lines.append(f"{int(t // 60)}:{int(t % 60):02d} {label}")
    total = T["total"]
    lines.append(f"{int(total // 60)}:{int(total % 60):02d} Watch next: The Garden")
    (OUT / "chapters.txt").write_text("\n".join(lines) + "\n")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    watermark_png(OUT / "watermark.png")
    end = endscreen()
    items = overlays()
    total = dur(MAIN)
    # every looped picture gets an explicit length, or the encoder never stops (a 45 GB file on the first run)
    ins = ["-i", MAIN, "-i", end, "-loop", 1, "-framerate", 24, "-t", f"{total:.3f}", "-i", OUT / "watermark.png"]
    fc = [f"[2:v]format=rgba[wm]", f"[0:v][wm]overlay=0:0:enable='between(t,47.1,{total - 0.5:.2f})'[b0]"]
    for k, (png, a, b) in enumerate(items):
        n = k + 3
        d = b - a
        ins += ["-loop", 1, "-framerate", 24, "-t", f"{d:.3f}", "-i", png]
        fc.append(f"[{n}:v]format=rgba,fade=in:st=0:d=0.5:alpha=1,fade=out:st={max(0.1, d - 0.6):.2f}:d=0.6:alpha=1,"
                  f"setpts=PTS+{a:.3f}/TB[o{k}]")
        fc.append(f"[b{k}][o{k}]overlay=0:0:eof_action=pass:enable='between(t,{a:.2f},{b:.2f})'[b{k + 1}]")
    fc.append(f"[b{len(items)}]trim=0:{total:.3f},setpts=PTS-STARTPTS[film]")
    fc.append(f"[film][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]")
    graph = OUT / "graph.txt"
    graph.write_text(";\n".join(fc))
    raw = OUT / "youtube-raw.mov"
    ff(*ins, "-/filter_complex", graph, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "17",
       "-preset", "medium", "-t", f"{total + END:.3f}", "-pix_fmt", "yuv420p", "-r", 24, "-c:a", "pcm_s16le", raw)
    pv.loudnorm_copy(raw, FINAL)
    srt()
    chapters_txt()
    print(f"youtube: {FINAL} {dur(FINAL):.1f} s, {len(items)} overlays; captions and chapters written")


if __name__ == "__main__":
    main()
