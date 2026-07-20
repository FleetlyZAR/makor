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

### 3. The daily scriptures: FOUNDATION DONE, FULL 50 PENDING SOURCE
The mechanism is split across two systems, which the old brief blurred:
- The in app "verse of the day" reads from `src/data/daily.js` in this repo.
- The daily email reads from `comms.daily_pool` in the private Supabase
  project `oztgjzncxgobcszcwibp`, and sends weekdays 05:00 UTC via
  `comms.run_daily()`, batched through `comms.send_batch()`. Never send with a
  per recipient loop; Resend rate limits at about two per second on an account
  shared with Fleetly.

Five verses are now fully wired on both sides: Genesis 1:1, John 1:1,
Lamentations 3:22-23, Psalm 36:9, and Isaiah 55:1. In this session Psalm 36:9
and Isaiah 55:1 were completed: their daily pages were built at
`public/daily/psalm-36-9/index.html` and `public/daily/isaiah-55-1/index.html`
(verse text pulled verbatim from the study JSON, brand palette, base64 card,
native share, "Read the full study" button), added to `src/data/daily.js`, and
their previously null `study_url` values were set in `comms.daily_pool`
(psalm-36-9 to `/psalms/psalm-036/`, isaiah-55-1 to
`/isaiah/an-invitation-to-the-thirsty/`). Both pool rows already carried
verse_text, writeup_html, writeup_txt, images, and daily_page_url, so both are
now send ready. Cards for both sizes were already deployed.

Outstanding: the full set of 50 daily scriptures needs the restored
`MAKOR-DAILY-50.md` before the remaining verses can be produced. Each new verse
needs, per verse: study JSON located, exact BSB verse text, title, slug and
summary pulled; both cards rendered (vertical 1080x1920 to
`public/daily/<slug>.png`, landscape 1200x630 to `<slug>-share.png`); a daily
page at `public/daily/<slug>/index.html`; an entry in `src/data/daily.js`; and
a row in `comms.daily_pool` with active true and study_url and daily_page_url
set.

Note to resolve: the Isaiah 55:1 pool `verse_text` begins "Come, all you who
are thirsty" without the leading opening quotation mark, while the new daily
page and `daily.js` keep the verbatim JSON opening quote. Pick one form for
consistency.

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
`og-default.png` shipped here was rendered with DejaVu Serif because Fraunces
was not available in the build sandbox; it is intended to be swapped for a
Fraunces rendered version whenever convenient.

## Divergences from the old brief worth remembering
- The site fonts are EB Garamond in the Astro pages; the hand made daily share
  pages use Fraunces and Newsreader with the Ink, Water, Light palette. Both
  are intentional; do not "correct" one to the other.
- The `comms` schema (daily_pool, run_daily, run_weekly, send_batch) lives only
  in Supabase, not in the repo `supabase/` folder. Do not expect it in git.
- Psalms studies use numeric slugs (for example `psalm-036`), so a Psalm study
  URL carries a number even though the general pattern is a thematic slug. Use
  the actual slug from the JSON so links never break.
