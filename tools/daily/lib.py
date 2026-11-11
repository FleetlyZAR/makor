# -*- coding: utf-8 -*-
"""Shared helpers for the Makor scripture of the day calendar.

Source of truth:
  tools/daily/verses/<slug>.json   one file per daily (verse, write-up, study link)
  tools/daily/calendar.json        {"YYYY-MM-DD": "<slug>"} for every day

Everything else (cards, landing pages, src/data/daily.js, the Supabase sync SQL)
is generated from those two by render.py and build.py, and checked by check.py.
"""
import datetime as dt
import glob
import json
import os
import re
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
VERSES_DIR = os.path.join(HERE, "verses")
CALENDAR = os.path.join(HERE, "calendar.json")
OUT_DIR = os.path.join(HERE, "out")
PUBLIC = os.path.join(REPO, "public", "daily")
STUDIES = os.path.join(REPO, "src", "content", "studies")
DAILY_JS = os.path.join(REPO, "src", "data", "daily.js")
SCRIPTURE_DB = os.path.join(REPO, "tools", "scripture", "makor-scripture.db")
SITE = "https://makor.co.za"
TZ_OFFSET = dt.timedelta(hours=2)  # Africa/Johannesburg, no daylight saving

HORIZON_DAYS = 90        # the calendar must always reach this far ahead
HORIZON_MIN = 60         # below this the run is failing to keep up: loud warning
NO_REPEAT_DAYS = 365     # the same verse never appears twice inside this window
MAX_VERSE = 330         # characters; longer verses do not fit the card cleanly

DASHES = ("—", "–")

REF_RE = re.compile(r"^((?:[123] )?[A-Z][a-z]+(?: of [A-Z][a-z]+)?) (\d+):(\d+)(?:-(\d+))?$")


def today():
    """Today's date in South Africa, which is the date the email uses."""
    return (dt.datetime.utcnow() + TZ_OFFSET).date()


def iso(d):
    return d.isoformat()


def parse_date(s):
    return dt.date.fromisoformat(s)


# ---------- references ----------

def parse_ref(ref):
    """'Psalm 36:9' -> ('Psalm', 36, [9]); 'Luke 1:46-47' -> ('Luke', 1, [46, 47])."""
    m = REF_RE.match(ref)
    if not m:
        raise ValueError(f"bad reference {ref!r}: use 'Book C:V' or 'Book C:V-W' within one chapter")
    book, ch, v1, v2 = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4)
    v2 = int(v2) if v2 else v1
    if v2 < v1 or v2 - v1 > 3:
        raise ValueError(f"bad verse range in {ref!r}: at most four verses")
    return book, ch, list(range(v1, v2 + 1))


def book_folder(book):
    if book == "Psalm":
        return "psalms"
    return book.lower().replace(" ", "-")


def daily_slug(ref):
    book, ch, vs = parse_ref(ref)
    return f"{book_folder(book)}-{ch}-{vs[0]}" if book != "Psalm" else f"psalm-{ch}-{vs[0]}"


def verse_keys(ref):
    """Set of (folder, chapter, verse) a reference covers, for overlap checks."""
    book, ch, vs = parse_ref(ref)
    f = book_folder(book)
    return {(f, ch, v) for v in vs}


# ---------- studies ----------

TOKEN = re.compile(r"\{\{[^|}]+\|([^}]*)\}\}")


def clean_text(t):
    return " ".join(TOKEN.sub(r"\1", t).replace("\n", " ").split())


_study_cache = {}


def load_book(folder):
    if folder in _study_cache:
        return _study_cache[folder]
    out = []
    for p in sorted(glob.glob(os.path.join(STUDIES, folder, "*.json"))):
        try:
            d = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        vmap = {}
        for u in d.get("text", {}).get("units", []):
            for v in u.get("verses", []):
                vmap[(v.get("chapter"), v.get("n"))] = v.get("text", "")
        sec = d.get("section", {})
        out.append({"path": p, "slug": sec.get("slug"), "title": sec.get("title"), "vmap": vmap})
    _study_cache[folder] = out
    return out


def find_study(ref):
    """Return (study_url_rel, verse_text) from the committed study holding the whole
    reference, or raise. Verse text is the study's own text with tokens removed, which
    is the BSB text with Makor's no dash edits already applied."""
    book, ch, vs = parse_ref(ref)
    folder = book_folder(book)
    studies = load_book(folder)
    if not studies:
        raise LookupError(f"{ref}: no studies in src/content/studies/{folder}")
    for s in studies:
        if all((ch, v) in s["vmap"] for v in vs):
            text = " ".join(clean_text(s["vmap"][(ch, v)]) for v in vs)
            return f"/{folder}/{s['slug']}/", text
    raise LookupError(f"{ref}: no single committed study contains all of these verses")


# ---------- the BSB database (cross check) ----------

def db_text(ref):
    book, ch, vs = parse_ref(ref)
    name = "Psalms" if book == "Psalm" else book
    con = sqlite3.connect(SCRIPTURE_DB)
    try:
        row = con.execute("select id from book where commonName = ? or name = ?", (name, name)).fetchone()
        if not row:
            return None
        parts = []
        for v in vs:
            r = con.execute("select text from verse where bookId=? and chapter=? and verse=?", (row[0], ch, v)).fetchone()
            if not r:
                return None
            parts.append(r[0])
        return " ".join(" ".join(p.split()) for p in parts)
    finally:
        con.close()


def norm_compare(s):
    """Loose form for comparing study text with the BSB database: Makor rewrites
    dashes, so compare on letters and digits only."""
    return re.sub(r"[^a-z0-9]", "", s.lower())


# ---------- data files ----------

def load_calendar():
    if not os.path.exists(CALENDAR):
        return {}
    return json.load(open(CALENDAR, encoding="utf-8"))


def save_calendar(cal):
    with open(CALENDAR, "w", encoding="utf-8") as f:
        json.dump(dict(sorted(cal.items())), f, indent=1, ensure_ascii=False)
        f.write("\n")


def verse_path(slug):
    return os.path.join(VERSES_DIR, f"{slug}.json")


def load_verse(slug):
    return json.load(open(verse_path(slug), encoding="utf-8"))


def load_all_verses():
    out = {}
    for p in sorted(glob.glob(os.path.join(VERSES_DIR, "*.json"))):
        d = json.load(open(p, encoding="utf-8"))
        out[d["slug"]] = d
    return out


def save_verse(d):
    os.makedirs(VERSES_DIR, exist_ok=True)
    with open(verse_path(d["slug"]), "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
        f.write("\n")


# ---------- church seasons (computed, so they never run out) ----------

def easter(year):
    a = year % 19
    b, c = divmod(year, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return dt.date(year, month, day)


def season(d):
    """A short theme hint for a date, or ''. Used to steer verse choice."""
    y = d.year
    xmas = dt.date(y, 12, 25)
    advent1 = xmas - dt.timedelta(days=(xmas.weekday() + 1) % 7 or 7) - dt.timedelta(weeks=3)
    e = easter(y)
    fixed = {
        (12, 24): "Christmas Eve: the birth announced",
        (12, 25): "Christmas Day: the Word made flesh",
        (12, 31): "New Year's Eve: numbering our days",
        (1, 1): "New Year's Day: new mercies, a new song",
        (1, 6): "Epiphany: the light revealed to the nations",
    }
    if (d.month, d.day) in fixed:
        return fixed[(d.month, d.day)]
    if d == e - dt.timedelta(days=46):
        return "Ash Wednesday: dust, repentance, return to the LORD"
    if d == e - dt.timedelta(days=7):
        return "Palm Sunday: the King comes, humble, on a donkey"
    if d == e - dt.timedelta(days=3):
        return "Maundy Thursday: the Last Supper, love that serves"
    if d == e - dt.timedelta(days=2):
        return "Good Friday: the cross"
    if d == e - dt.timedelta(days=1):
        return "Holy Saturday: the waiting tomb"
    if d == e:
        return "Easter Sunday: He is risen"
    if d == e + dt.timedelta(days=39):
        return "Ascension Day: Christ exalted"
    if d == e + dt.timedelta(days=49):
        return "Pentecost: the Spirit poured out"
    if advent1 <= d < dt.date(y, 12, 24):
        return "Advent: waiting, promise, the coming King"
    if dt.date(y, 12, 26) <= d <= dt.date(y, 12, 30):
        return "Christmastide: the incarnation"
    if e - dt.timedelta(days=46) < d < e - dt.timedelta(days=7):
        return "Lent: repentance, the road to the cross"
    if e - dt.timedelta(days=7) < d < e:
        return "Holy Week"
    if e < d < e + dt.timedelta(days=7):
        return "Easter week: resurrection life"
    return ""
