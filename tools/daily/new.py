# -*- coding: utf-8 -*-
"""Start a new daily: pull the verbatim verse and study link, put it on a date.

  python new.py "Isaiah 26:3" --date 2026-11-11 [--theme "peace"]

Writes tools/daily/verses/<slug>.json with an empty story for the writer to fill,
and puts the slug on the calendar. Refuses:
  - a date that is today or earlier (published days are frozen),
  - a date that already has a verse (unless --replace, future dates only),
  - a reference that overlaps any verse already in the library (every daily is new),
  - a reference no committed study contains.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib


def main(argv):
    if not argv or "--date" not in argv:
        raise SystemExit(__doc__)
    ref = argv[0]
    date = argv[argv.index("--date") + 1]
    theme = argv[argv.index("--theme") + 1] if "--theme" in argv else lib.season(lib.parse_date(date))
    replace = "--replace" in argv

    lib.parse_date(date)
    if date <= lib.iso(lib.today()):
        raise SystemExit(f"{date} is today or past: published days are frozen")
    cal = lib.load_calendar()
    if date in cal and not replace:
        raise SystemExit(f"{date} already has {cal[date]} (use --replace to swap a future date)")

    slug = lib.daily_slug(ref)
    keys = lib.verse_keys(ref)
    for other in lib.load_all_verses().values():
        if other["slug"] == slug or keys & lib.verse_keys(other["ref"]):
            raise SystemExit(f"{ref} overlaps {other['ref']} already in the library ({other['slug']}); pick a new verse")

    url, text = lib.find_study(ref)
    if any(c in text for c in lib.DASHES):
        raise SystemExit(f"{ref}: study text carries a dash; pick another verse and flag the study")
    if len(text) > lib.MAX_VERSE:
        raise SystemExit(f"{ref}: verse is {len(text)} characters, the card limit is {lib.MAX_VERSE}; pick a shorter verse or range")

    lib.save_verse({"slug": slug, "ref": ref, "verse": text, "story": [], "studyUrl": url,
                    "theme": theme, "core": 0, "added": lib.iso(lib.today())})
    cal[date] = slug
    lib.save_calendar(cal)
    print(f"{date}  {ref}  -> verses/{slug}.json  (study {url})")
    print(f"verse: {text}")



if __name__ == "__main__":
    main(sys.argv[1:])
