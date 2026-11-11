# -*- coding: utf-8 -*-
"""Validate the scripture of the day calendar. Nothing ships unless this passes.

  python check.py            full check (errors exit 1, warnings print only)
  python check.py --summary  one line: horizon and counts

ERRORS (block a commit):
  calendar   every date is YYYY-MM-DD and names a verse file
  frozen     no date up to and including today differs from the committed calendar
  gaps       no missing day between the first future date and the last
  horizon    today and the next HORIZON_MIN days are all covered
  verse      reference parses; slug matches; text equals the committed study text
             for exactly those verses; study URL resolves to that study; no dashes;
             at most MAX_VERSE characters
  repeat     no verse (or overlapping range) appears twice within NO_REPEAT_DAYS,
             and no new verse overlaps a core verse
  story      exactly three paragraphs: opening 6 to 35 words, middle 25 to 120,
             close 6 to 45; no em or en dash, no spaced hyphen, no {{ tokens,
             no straight double quotes left unpaired, every paragraph ends with
             punctuation
  book       never the same book two days running
  assets     both cards and the landing page exist for every date from today on,
             and the page carries the verse text and the study link
  daily.js   the generated file matches what build.py would write now

WARNINGS (report only):
  horizon under HORIZON_DAYS, a book more than its share in a 30 day window,
  study text that differs from the BSB database beyond Makor's dash edits.
"""
import collections
import datetime as dt
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib

CORE_RETURN = "2027-11-11"   # core verses may come back onto the calendar from here
BOOK_CAP_30 = {"psalms": 7, "isaiah": 6, "luke": 7}   # per rolling 30 days; others 4


def committed_calendar():
    try:
        raw = subprocess.run(["git", "-C", lib.REPO, "show", "HEAD:tools/daily/calendar.json"],
                             capture_output=True, text=True, check=True).stdout
        return json.loads(raw)
    except Exception:
        return {}


def words(s):
    return len(s.split())


def check_story(slug, story, err):
    if not isinstance(story, list) or len(story) != 3:
        err(f"{slug}: story must be exactly three paragraphs")
        return
    lims = [(6, 35), (25, 120), (6, 45)]
    for i, (p, (lo, hi)) in enumerate(zip(story, lims)):
        n = words(p)
        if not lo <= n <= hi:
            err(f"{slug}: paragraph {i + 1} has {n} words (want {lo} to {hi})")
        if any(c in p for c in lib.DASHES) or " - " in p or "--" in p:
            err(f"{slug}: paragraph {i + 1} has a dash")
        if "{{" in p or "}}" in p:
            err(f"{slug}: paragraph {i + 1} has a template token")
        if p.count('"') % 2:
            err(f"{slug}: paragraph {i + 1} has an unpaired straight quote")
        if not re.search(r"[.!?”’]$", p.strip()):
            err(f"{slug}: paragraph {i + 1} does not end with punctuation")


def expected_daily_js(verses, cal):
    import build
    keep = open(lib.DAILY_JS, encoding="utf-8").read() if os.path.exists(lib.DAILY_JS) else None
    try:
        build.write_daily_js(verses, cal)
        return open(lib.DAILY_JS, encoding="utf-8").read()
    finally:
        if keep is not None:
            with open(lib.DAILY_JS, "w", encoding="utf-8") as f:
                f.write(keep)


def stories_only(slugs):
    """python check.py --stories SLUG [...]: the writer's check, write-ups only."""
    errors = []
    for s in slugs:
        try:
            v = lib.load_verse(s)
        except FileNotFoundError:
            errors.append(f"{s}: no verse file")
            continue
        check_story(s, v.get("story"), errors.append)
        joined = " ".join(v.get("story") or [])
        if v["verse"] in joined:
            errors.append(f"{s}: the write-up quotes the whole verse word for word; paraphrase it")
    for e in errors:
        print("ERROR", e)
    print(f"{len(slugs)} write-ups checked, {len(errors)} errors")
    sys.exit(1 if errors else 0)


def main(argv):
    if "--stories" in argv:
        stories_only([a for a in argv if not a.startswith("--")])
    errors, warnings = [], []
    err, warn = errors.append, warnings.append
    today = lib.iso(lib.today())

    verses = lib.load_all_verses()
    cal = lib.load_calendar()

    # calendar shape
    for d, s in cal.items():
        try:
            lib.parse_date(d)
        except Exception:
            err(f"calendar: bad date {d!r}")
        if s not in verses:
            err(f"calendar: {d} names {s} but tools/daily/verses/{s}.json does not exist")

    # frozen past
    old = committed_calendar()
    for d, s in old.items():
        if d <= today and cal.get(d) != s:
            err(f"frozen: {d} was {s} in the committed calendar and is now {cal.get(d)}; published days never change")

    # gaps and horizon
    future = sorted(d for d in cal if d >= today)
    if future:
        d0, d1 = lib.parse_date(future[0]), lib.parse_date(future[-1])
        n = (d1 - d0).days + 1
        if n != len(future):
            have = set(future)
            miss = [lib.iso(d0 + dt.timedelta(days=i)) for i in range(n) if lib.iso(d0 + dt.timedelta(days=i)) not in have]
            err(f"gaps: {len(miss)} missing dates, first {miss[:5]}")
    covered = 0
    t = lib.today()
    while lib.iso(t + dt.timedelta(days=covered)) in cal:
        covered += 1
    if covered < lib.HORIZON_MIN:
        err(f"horizon: only {covered} days covered from today (minimum {lib.HORIZON_MIN})")
    elif covered < lib.HORIZON_DAYS:
        warn(f"horizon: {covered} days covered from today (target {lib.HORIZON_DAYS})")

    # each verse used on the calendar, plus every verse file
    used = set(cal.values())
    for s, v in verses.items():
        try:
            if lib.daily_slug(v["ref"]) != s:
                err(f"{s}: slug does not match reference {v['ref']} (expected {lib.daily_slug(v['ref'])})")
            url, text = lib.find_study(v["ref"])
        except Exception as e:
            err(f"{s}: {e}")
            continue
        if v.get("verse") != text:
            err(f"{s}: verse text differs from the study text\n    file:  {v.get('verse')}\n    study: {text}")
        if v.get("studyUrl") != url:
            err(f"{s}: studyUrl {v.get('studyUrl')} but the verses live in {url}")
        if any(c in v["verse"] + v["ref"] for c in lib.DASHES):
            err(f"{s}: dash in verse or reference")
        if len(v["verse"]) > lib.MAX_VERSE and not v.get("core"):
            err(f"{s}: verse is {len(v['verse'])} characters (max {lib.MAX_VERSE})")
        if s in used or v.get("core"):
            check_story(s, v.get("story"), err)
        bsb = lib.db_text(v["ref"])
        if bsb and lib.norm_compare(bsb) != lib.norm_compare(text):
            warn(f"{s}: study text differs from the BSB database beyond punctuation")

    # repeats and overlaps
    keys = {s: lib.verse_keys(v["ref"]) for s, v in verses.items() if "ref" in v}
    core = {s for s, v in verses.items() if v.get("core")}
    for s in verses:
        if s in core:
            continue
        for c in core:
            if keys.get(s, set()) & keys.get(c, set()):
                err(f"repeat: {s} overlaps core verse {c}")
    dated = sorted(cal.items())
    for i, (d, s) in enumerate(dated):
        if s in core and d < CORE_RETURN and d > today:
            err(f"repeat: {d} schedules core verse {s} before {CORE_RETURN}")
        for d2, s2 in dated[i + 1:]:
            if (lib.parse_date(d2) - lib.parse_date(d)).days >= lib.NO_REPEAT_DAYS:
                break
            if keys.get(s, set()) & keys.get(s2, set()):
                err(f"repeat: {s} on {d} and {s2} on {d2} overlap inside {lib.NO_REPEAT_DAYS} days")

    # book rhythm
    def folder(s):
        return lib.book_folder(lib.parse_ref(verses[s]["ref"])[0]) if s in verses else ""
    for (d, s), (d2, s2) in zip(dated, dated[1:]):
        if d2 >= today and folder(s) == folder(s2) and (lib.parse_date(d2) - lib.parse_date(d)).days == 1:
            err(f"book: {folder(s)} two days running ({d} {s}, {d2} {s2})")
    fut = [(d, s) for d, s in dated if d >= today]
    flagged = set()
    for i in range(len(fut)):
        win = [folder(s) for d, s in fut[i:i + 30]]
        for b, n in collections.Counter(win).items():
            if n > BOOK_CAP_30.get(b, 4) and b not in flagged:
                flagged.add(b)
                warn(f"book: {b} appears {n} times in the 30 days from {fut[i][0]}")

    # assets
    for d, s in dated:
        if d < today or s not in verses:
            continue
        v = verses[s]
        for p in (f"{s}.png", f"{s}-share.png", f"{s}/index.html"):
            if not os.path.exists(os.path.join(lib.PUBLIC, p)):
                err(f"assets: public/daily/{p} missing (run render.py)")
        page = os.path.join(lib.PUBLIC, s, "index.html")
        if os.path.exists(page):
            html = open(page, encoding="utf-8").read()
            vtext = v["verse"].replace("&", "&amp;").replace('"', "&quot;")
            if vtext not in html and v["verse"] not in html:
                err(f"assets: {s} page does not carry the current verse text (run render.py {s})")
            if lib.SITE + v["studyUrl"] not in html:
                err(f"assets: {s} page does not link {v['studyUrl']} (run render.py {s})")
            if v.get("story") and v["story"][1].split()[0] not in html:
                err(f"assets: {s} page write-up looks stale (run render.py {s})")

    # generated daily.js in step
    if not errors:
        want = expected_daily_js(verses, cal)
        have = open(lib.DAILY_JS, encoding="utf-8").read()
        if want != have:
            err("daily.js: out of date (run build.py)")

    summary = (f"daily calendar: {covered} days covered from {today}, last date {future[-1] if future else '-'}, "
               f"{len(used)} verses scheduled, {len(verses)} in library, {len(errors)} errors, {len(warnings)} warnings")
    if "--summary" not in argv:
        for w in warnings:
            print("WARN ", w)
        for e in errors:
            print("ERROR", e)
    print(summary)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
