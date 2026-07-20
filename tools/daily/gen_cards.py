"""Makor daily scripture card generator.
Reproduces the bespoke fountain-ripple card in both formats:
  vertical status card  1080x1920  -> <slug>.png
  landscape share card  1200x630   -> <slug>-share.png
Brand: Ink #0E2A2E ground, Water #0F6C6C, Light/brass #B8862F, cream #F4EEDF.
Fonts: Fraunces (display) + Newsreader (body). Verse size auto-fits.
"""
from PIL import Image, ImageDraw, ImageFont
import math
import numpy as np

T = "/tmp/ttf/"
FR = {w: T + f"fraunces-{w}.ttf" for w in (400, 600)}
NR = {w: T + f"newsreader-{w}.ttf" for w in (400, 500)}
NR_IT = T + "newsreader-400-italic.ttf"

WATER = (28, 120, 118)
BRASS = (184, 134, 47)
GOLD  = (216, 170, 88)
CORE  = (242, 216, 150)
CREAM = (244, 238, 223)
MUTED = (150, 170, 167)
BG_C  = (16, 48, 52)
BG_E  = (11, 33, 36)

SS = 2

def _f(path, size):
    return ImageFont.truetype(path, int(size * SS))

def _bg(Wc, Hc, cx, cy):
    yy, xx = np.ogrid[0:Hc, 0:Wc]
    dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    maxd = math.hypot(max(cx, Wc - cx), max(cy, Hc - cy))
    t = np.clip(dist / maxd, 0.0, 1.0)
    arr = np.empty((Hc, Wc, 3), dtype=np.uint8)
    for i in range(3):
        arr[:, :, i] = (BG_C[i] + (BG_E[i] - BG_C[i]) * t).astype(np.uint8)
    return Image.fromarray(arr, "RGB")

def _ripple(base, cx, cy, scale=1.0):
    Wc, Hc = base.size
    overlay = Image.new("RGBA", (Wc, Hc), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    glowR = int(172 * SS * scale)
    for i in range(glowR, 0, -2):
        a = int(42 * (1 - i / glowR) ** 2)
        if a > 0:
            d.ellipse([cx-i, cy-i, cx+i, cy+i], fill=(GOLD[0], GOLD[1], GOLD[2], a))
    for rad, alpha in [(20,150),(42,122),(68,96),(96,70),(124,48),(150,30)]:
        r = int(rad * SS * scale)
        d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=(BRASS[0], BRASS[1], BRASS[2], alpha), width=max(1, int(2*SS)))
    ch = int(17 * SS * scale)
    d.ellipse([cx-ch, cy-ch, cx+ch, cy+ch], fill=(GOLD[0], GOLD[1], GOLD[2], 90))
    cr = int(9.5 * SS * scale)
    d.ellipse([cx-cr, cy-cr, cx+cr, cy+cr], fill=(CORE[0], CORE[1], CORE[2], 255))
    base.paste(Image.alpha_composite(base.convert("RGBA"), overlay).convert("RGB"), (0, 0))

def _tracked(d, text, font, cx, y, color, track):
    ws = [d.textlength(ch, font=font) for ch in text]
    total = sum(ws) + track * SS * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, ws):
        d.text((x, y), ch, font=font, fill=color); x += w + track * SS

def _centered(d, text, font, cx, y, color):
    w = d.textlength(text, font=font); d.text((cx - w/2, y), text, font=font, fill=color)

def _wrap(d, text, font, maxw):
    words = text.split(); lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=font) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines

def _clean(t):
    return " ".join(t.replace("\n", " ").split())

def _fit(d, text, font_path, sizes, maxw, max_block, lh_ratio):
    text = _clean(text)
    for sz in sizes:
        font = _f(font_path, sz)
        lines = _wrap(d, text, font, maxw)
        lh = int(sz * lh_ratio * SS)
        if len(lines) * lh <= max_block * SS:
            return font, lines, lh
    sz = sizes[-1]; font = _f(font_path, sz)
    return font, _wrap(d, text, font, maxw), int(sz * lh_ratio * SS)

_BASE = {}

def _base_vertical():
    if "v" in _BASE:
        return _BASE["v"].copy()
    W, H = 1080, 1920
    Wc, Hc = W*SS, H*SS
    cx = Wc // 2
    rcy = int(398 * SS)
    img = _bg(Wc, Hc, cx, rcy)
    _ripple(img, cx, rcy, 1.0)
    d = ImageDraw.Draw(img)
    _tracked(d, "MAKOR", _f(FR[600], 52), cx, int(672*SS), WATER, 20)
    d.rectangle([cx-int(90*SS), int(766*SS), cx+int(90*SS), int(767.5*SS)], fill=BRASS)
    _centered(d, "Scripture of the day", _f(NR_IT, 30), cx, int(790*SS), MUTED)
    d.line([cx-int(170*SS), int(1735*SS), cx+int(170*SS), int(1735*SS)], fill=(70,96,96), width=max(1,SS))
    _centered(d, "Read the study", _f(NR[400], 30), cx, int(1775*SS), CREAM)
    _tracked(d, "makor.co.za", _f(NR[400], 26), cx, int(1820*SS), WATER, 3)
    _BASE["v"] = img
    return img.copy()

def render_vertical(verse, ref):
    W, H = 1080, 1920
    Wc, Hc = W*SS, H*SS
    cx = Wc // 2
    img = _base_vertical()
    d = ImageDraw.Draw(img)
    vfont, lines, lh = _fit(d, verse, FR[400], [64,60,56,52,48,44,40], int(780*SS), 640, 1.42)
    vy = int(1150*SS) - (lh*len(lines))//2
    for ln in lines:
        _centered(d, ln, vfont, cx, vy, CREAM); vy += lh
    _tracked(d, ref.upper(), _f(FR[600], 34), cx, vy + int(34*SS), BRASS, 8)
    return img.resize((W, H), Image.LANCZOS)

def _base_share():
    if "s" in _BASE:
        return _BASE["s"].copy()
    W, H = 1200, 630
    Wc, Hc = W*SS, H*SS
    lx, lcy = int(288*SS), int(268*SS)
    img = _bg(Wc, Hc, lx, lcy)
    _ripple(img, lx, lcy, 0.92)
    d = ImageDraw.Draw(img)
    _tracked(d, "MAKOR", _f(FR[600], 40), lx, int(452*SS), WATER, 16)
    d.line([int(500*SS), int(150*SS), int(500*SS), int(480*SS)], fill=(78,104,104), width=max(1,SS))
    rcx = int(852*SS)
    _centered(d, "Scripture of the day", _f(NR_IT, 27), rcx, int(150*SS), MUTED)
    _centered(d, "Read the full study  ·  makor.co.za", _f(NR[400], 24), rcx, int(556*SS), MUTED)
    _BASE["s"] = img
    return img.copy()

def render_share(verse, ref):
    W, H = 1200, 630
    img = _base_share()
    d = ImageDraw.Draw(img)
    rcx = int(852*SS)
    vfont, lines, lh = _fit(d, verse, FR[400], [46,42,38,34,30,27], int(560*SS), 250, 1.34)
    vy = int(352*SS) - (lh*len(lines))//2
    for ln in lines:
        _centered(d, ln, vfont, rcx, vy, CREAM); vy += lh
    _tracked(d, ref.upper(), _f(FR[600], 26), rcx, vy + int(20*SS), BRASS, 7)
    return img.resize((W, H), Image.LANCZOS)

if __name__ == "__main__":
    render_vertical("The heavens declare the glory of God; the skies proclaim the work of His hands.", "Psalm 19:1").save("/tmp/sample-vertical.png")
    render_share("The heavens declare the glory of God; the skies proclaim the work of His hands.", "Psalm 19:1").save("/tmp/sample-share.png")
    print("wrote samples")
