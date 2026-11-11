# Scheduled scripture of the day run (auto deploy)

Once a day. Each run keeps the calendar 90 days ahead: it fills every open
date in the next 90 days (normally one, the new last day), with a verse that
has never been used, writes it up, renders it, validates everything, builds the
site, commits and pushes to main (a live deploy, authorised by Luyanda on
10 November 2026 for these runs and these files only), and syncs the email
calendar in Supabase. Keep this session lean: read only what a step needs.

Python is `tools/daily/.venv/bin/python` (call it PY below). All paths are from
`~/makor`.

1. `cd ~/makor`. If `git status --porcelain tools/daily public/daily src/data/daily.js`
   shows changes you did not make, stop and report: someone is mid edit.
   Run `git pull --ff-only origin main`; if it fails, stop and report.
2. `PY tools/daily/plan.py --json`. If `open` is empty, skip to step 8.
   If more than 10 dates are open, take the earliest 10 this run (the next run
   continues).
3. For each open date, choose a verse, then run
   `PY tools/daily/new.py "<Book C:V>" --date <date>`
   (a range is allowed within one chapter, at most four verses). Rules for the
   choice:
   - Never in `library_refs` and never overlapping one (new.py refuses those;
     if it refuses, pick another).
   - Fit the `season` hint when there is one (Advent, Christmas, Lent, Holy
     Week, Easter, Pentecost and so on).
   - Not a book in `avoid_books` (never the same book two days running), and
     look at `recent_refs` for balance: roughly alternate Old and New
     Testament, about one Psalm in five, spread across the whole canon over
     time, and prefer verses that stand on their own on a card.
   - Short enough for the card (new.py refuses over 330 characters).
4. Write the `story` for each new file exactly as
   `tools/daily/AGENT-BRIEF.md` says (read it first). Up to 5 dates: write
   them yourself. More than 5: launch Sonnet agents with that brief, 15 files
   each, at most two at a time. Then
   `PY tools/daily/check.py --stories <new slugs>` must print 0 errors; fix
   and rerun until it does.
5. `PY tools/daily/render.py` (renders whatever is missing), then
   `PY tools/daily/build.py --from <first new date>`, then
   `PY tools/daily/check.py`. It must exit 0. If it cannot be made to pass,
   run `git checkout -- tools/daily src/data/daily.js` and
   `git clean -fd tools/daily/verses public/daily`, report the errors, and stop.
   Nothing is lost: the calendar is still at least 60 days ahead, so a missed
   run is harmless and the next run catches up.
6. Deploy:
   - `npm run build`. If it fails, do not commit or push; report and stop.
   - `git add tools/daily/verses tools/daily/calendar.json public/daily src/data/daily.js`
   - `git commit -m "Daily scripture: <date> <ref>[, <date> <ref> ...]"` (no em
     or en dashes; end with the line
     `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`)
   - `git push origin main`. If the push fails, report and stop.
7. Email calendar: run the contents of `tools/daily/out/sync.sql` with the
   Supabase `execute_sql` tool on project `oztgjzncxgobcszcwibp`. It is
   idempotent (upserts; past dates are never rewritten), so rerunning is safe.
8. Verify: `PY tools/daily/check.py --summary` and, in Supabase,
   `select * from comms.daily_schedule_horizon();`. Both should report at least
   60 covered days. If the database is behind the repo (for example a previous
   run pushed but failed at step 7), run
   `PY tools/daily/build.py` (no `--from`, so every date from today) and apply
   `tools/daily/out/sync.sql` in chunks of about 20 statements.
9. Report in three lines: dates and references added, the commit hash pushed,
   and the two horizons (repo and email). Stop.

## Never

- Change a date that is today or earlier (check.py fails if you do).
- Edit `verse`, `ref` or `studyUrl` by hand: they come from the study JSON.
- Push anything outside the four paths in step 6.
- Touch `public/daily` files of other dates, or the core 50 verse files.

## Setting up the scheduled task

Task id `makor-daily-scripture`, every day at 04:30 local (cron `30 4 * * *`),
prompt:

> You are running the daily Makor scripture of the day top-up in the repo at
> ~/makor. Read /Users/luyandajafta/makor/tools/daily/DAILY-RUN.md and follow it
> exactly. Authority: Luyanda authorised these runs on 10 November 2026 to commit
> and push to main and to apply tools/daily/out/sync.sql to the comms schema,
> only after tools/daily/check.py exits 0 and npm run build succeeds, and only
> for tools/daily/verses, tools/daily/calendar.json, public/daily and
> src/data/daily.js. Never push anything else, never change a date that is
> today or earlier, never force push. If a step fails, follow DAILY-RUN.md,
> report, and stop. Commit messages have no em or en dashes and end with
> Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>. Finish with the
> three line report.

Matching standing exception for CLAUDE.md (under "How we push and deploy work"):

> Standing exception (10 November 2026): the scheduled task
> `makor-daily-scripture` may commit and push its own scripture of the day
> additions to main after `tools/daily/check.py` exits 0 and `npm run build`
> succeeds, and may apply its generated `tools/daily/out/sync.sql` to the comms
> schema in Supabase, as set out in `tools/daily/DAILY-RUN.md`. This covers only
> those runs and only `tools/daily/verses`, `tools/daily/calendar.json`,
> `public/daily` and `src/data/daily.js`.
