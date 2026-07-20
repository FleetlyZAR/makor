# Makor build status (verified 2026-07-20)

This document reconciles the older comms and daily handoff notes against the
actual state of the repo and the live Supabase comms schema. It was written
after a full audit because the previous session was handed a brief that had
gone stale: it referenced `MAKOR-COMMS-HANDOFF.md` and `MAKOR-DAILY-50.md`,
neither of which exists in the repo or in git history, and it described work
(the reading plan page, the plan indexes) that is in fact already built and
live. Treat this file as the current source of truth. Keep `WAVE-HANDOFF.md`
for study authoring; this file covers the plan, the dailies, sharing, and
the calendar.

House rules remain in force: no em or en dashes anywhere; scripture text is
the Berean Standard Bible, pulled verbatim from the study JSON, never typed by
hand; reverent, plain, accessible voice; study URL pattern
`https://makor.co.za/<book>/<slug>/` with a trailing slash. Luyanda pushes and
deploys himself; Claude prepares files and hands back a commit block.

## Task by task

### 1. Reading plan as a real Astro page: DONE
`src/pages/plan.astro` (about 760 lines) is a real page built on the site
`Base.astro` layout, so it inherits the real header and footer. The nav in
`Base.astro` injects a "Reading plan" link to `/plan/` on every page. The
group plans menu item is deliberately held back; the `/groups/` page stays
reachable by URL. The builder keeps all intended behaviour: one, two, three
and four year tracks; a weekday only option; auto selected sittings in the
order morning, evening, midday; a single recurring calendar with per day
overrides; default times 05:00, 13:00, 18:00; and pace calculated against the
full 1354 study total.

### 2. The three plan index files: DONE
They are live Astro endpoints rather than static files, which is better
because every deploy regenerates them so new studies flow in automatically.
`src/pages/plan-index-canonical.json.js`, `-chronological.json.js`, and
`-multitrack.json.js` each delegate to `planIndexResponse(order)` in
`src/lib/planIndex.js`. Every item has the shape `{title, ref, summary, url}`,
pulled from the study JSON: title from `section.title`, ref from
`section.passageRef`, summary from `section.thesis`, and url from
`bookSlug(book)` plus `section.slug`. Canonical uses canon order, chronological
uses a book level chronological ordering, multitrack weaves four parallel
streams so they finish together.

### 3. The daily scriptures: DONE (all 50 wired both sides)
The mechanism is split across two systems, which the old brief blurred:
- The in app "verse of the day" reads from `src/data/daily.js` in this repo.
- The daily email reads from `comms.daily_pool` in the private Supabase
  project `oztgjzncxgobcszcwibp`, and sends weekdays 05:00 UTC via
  `comms.run_daily()`, batched through `comms.send_batch()`. Never send with a
  per recipient loop; Resend rate limits at about two per second on an account
  shared with Fleetly.

All 50 verses from `MAKOR-DAILY-50.md` are now produced. For each: the reference
was matched to its committed study JSON, exact BSB verse text and the real study
slug were pulled, both cards were rendered (vertical 1080x1920 `<slug>.png` and
landscape 1200x630 `<slug>-share.png`), the landing page was built at
`public/daily/<slug>/index.html`, an entry was written to `src/data/daily.js`
(50 entries), and a row was seeded in `comms.daily_pool`. The pool now holds 50
active rows, every one with `study_url` and `daily_page_url` set, so the whole
set is send ready and cues into the weekday rotation automatically.

The generator is vendored at `tools/daily/` (cards, reference-to-study matcher,
build script, and a README) so the set can be regenerated or extended. Cards are
rendered in the brand fonts Fraunces and Newsreader; verse size auto-fits so long
verses stay clean.

Note carried forward: the daily card shows the verbatim BSB verse text, so a few
longer verses (for example John 7:37-38) include their narrative frame. If you
prefer a trimmed quotable line on the card while keeping the full verse in the
study, that is a one-line change in the generator per verse.

### 4. Google Calendar for the plan: CODE DONE, EXTERNAL DEP PENDING
`plan.astro` already contains the full Google Calendar integration described in
the design: least privilege scope `calendar.app.created`, a dedicated "Makor
reading plan" calendar, sign in through the site's existing Supabase Google
auth, and a rebuild that adds only newly published studies on repeat presses.
The `.ics` download is retained as the fallback (a `makor-reading-plan.ics`
blob download). The remaining dependency is external, not code: the owner
OAuth Client ID and Google verification. Confirm that is in place and test the
end to end sign in before calling this shipped.

### 5. og:image on shared links: SITE DEFAULT DONE, PER STUDY CARDS PENDING
`Base.astro` now emits `og:image`, `og:image:width`, `og:image:height`,
`twitter:card`, and `twitter:image` on every page, defaulting to
`https://makor.co.za/og-default.png`, a new branded 1200x630 card in `public/`.
It accepts an optional `ogImage` prop (absolute URL or site relative path) so
any page or study can override the default. Every one of the 1354 study pages
now unfurls the branded default card when shared. Per study cards do not exist
yet; generating one card per study is a separate rendering pipeline. The
`og-default.png` is rendered in the brand fonts Fraunces and Newsreader in the
brand palette.

## Divergences from the old brief worth remembering
- The site fonts are EB Garamond in the Astro pages; the hand made daily share
  pages use Fraunces and Newsreader with the Ink, Water, Light palette. Both
  are intentional; do not "correct" one to the other.
- The `comms` schema (daily_pool, run_daily, run_weekly, send_batch) lives only
  in Supabase, not in the repo `supabase/` folder. Do not expect it in git.
- Psalms studies use numeric slugs (for example `psalm-036`), so a Psalm study
  URL carries a number even though the general pattern is a thematic slug. Use
  the actual slug from the JSON so links never break.
