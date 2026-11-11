# Scripture of the day

Every day has its own verse, planned 90 days ahead. The app home, the landing
page at `/daily/<slug>/`, the share cards, and the weekday email all show the
same verse on the same date. A scheduled run tops the calendar up each day
(see `DAILY-RUN.md`).

## Source of truth

- `verses/<slug>.json`: one file per daily: `ref`, `verse` (verbatim BSB from
  the committed study), `story` (three paragraphs), `studyUrl`, `theme`,
  `core` (1 to 50 for the original rotation, 0 for calendar verses), `added`.
- `calendar.json`: `{"YYYY-MM-DD": "<slug>"}` for every day.

Everything else is generated from those two:

| Output | Made by |
| --- | --- |
| `public/daily/<slug>.png` (1080x1920), `<slug>-share.png` (1200x630), `<slug>/index.html` | `render.py` |
| `src/data/daily.js` (core rotation, scheduled verses, calendar) | `build.py` |
| `public/daily/feed.json` (calendar and email fields, pulled by Supabase) | `build.py` |
| `out/sync.sql` (manual fallback: the same upserts as SQL) | `build.py` |

## Tools

```
PY=tools/daily/.venv/bin/python
$PY tools/daily/plan.py                      # open dates, season hints, books to avoid
$PY tools/daily/new.py "Isaiah 26:3" --date 2026-11-11
$PY tools/daily/check.py --stories <slugs>   # the writer's check
$PY tools/daily/render.py                    # cards and pages for anything missing
$PY tools/daily/build.py [--from DATE]       # daily.js and out/sync.sql
$PY tools/daily/check.py                     # the full gate; must exit 0
```

One time setup of the venv (fonts are vendored in `fonts/`, OFL):

```
python3 -m venv tools/daily/.venv
tools/daily/.venv/bin/pip install pillow numpy
```

## Why it cannot run dry (the fail safe layers)

1. **Ninety days of runway.** The calendar is filled 90 days ahead, so a missed
   run, or a week of them, changes nothing a reader sees. `check.py` fails
   under 60 days covered and warns under 90. Each run fills every open date,
   so it catches up on its own.
2. **Frozen past.** A date that is today or earlier can never change:
   `new.py` refuses it and `check.py` compares against the committed calendar.
   An email that went out keeps its verse in the database too (the sync uses
   `on conflict do nothing` for those dates).
3. **Verbatim text, real links.** `new.py` pulls the verse from the committed
   study and records that study's URL; `check.py` re-derives both on every run,
   and cross checks the BSB database.
4. **Never a repeat.** No verse or overlapping range twice in 365 days; new
   verses never overlap the core 50; never the same book two days running.
5. **Mechanical writing checks.** Three paragraphs within word limits, no em
   or en dashes, no template tokens, no whole verse quoted back.
6. **Nothing ships unchecked.** The run commits only after `check.py` exits 0
   and `npm run build` succeeds; otherwise it reverts its own files.
7. **The app never goes blank.** The app bundle is frozen at build time. It
   carries the calendar from its build date onward, and for any date beyond
   that it falls back to the core 50 rotation by day of the year.
8. **The email follows the site.** The daily run has Supabase fetch the live
   `/daily/feed.json` with pg_net and apply it through
   `sync_from_feed.sql`, which validates first and changes nothing on any error.
   Making this fully automatic with pg_cron is drafted in
   `proposed-feed-sync-cron.sql`, awaiting approval.
9. **The email never goes blank.** `comms.pick_today()` reads
   `comms.daily_schedule` first and falls back to the original least sent random
   pick if today has no row or its verse is inactive.

## Church seasons

`lib.season()` computes Advent, Christmas, New Year, Epiphany, Ash Wednesday,
Lent, Palm Sunday, Holy Week, Easter, Ascension and Pentecost for any year
(Easter by the Gregorian computus), so the seasonal hints never run out.
