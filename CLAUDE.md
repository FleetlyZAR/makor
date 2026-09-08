# Makor working notes (persistent memory for Claude)

## How we push and deploy work (permanent)

Luyanda pushes and deploys Makor himself through Visual Studio (VS Code Source
Control). Claude does NOT run git or publish.sh to push. When work is ready,
Claude prepares the files in the repo, then hands back:

1. a clear, ready to paste commit message, and
2. the Visual Studio steps (and the equivalent terminal git commands as a
   fallback),

and then stops. Claude only runs the push itself if Luyanda explicitly says so
in that message.

Commit handoff format (permanent): whenever work is ready, Claude gives a single
ready to paste terminal block that runs from ANY terminal on the Mac, not only
one already sitting in the repo. The block opens with `cd ~/Documents/Developer/makor || exit 1`
so it locates itself, then the `git add` command (list the changed files, or
`git add -A` when a delete is involved), then `git commit -m "..."`. Not just a
bare message. Luyanda runs the block and pushes himself. No em dashes or en
dashes in commit messages.

The repo now lives at ~/Documents/Developer/makor, a plain local folder, not in
iCloud. Do not use the old ~/Documents/makor or the iCloud Drive copy.

Deploy facts: work is committed on the `main` branch and pushed to `origin`
(GitHub, FleetlyZAR/makor). Cloudflare rebuilds automatically on push, and the
site is usually live within about two minutes. Any push to main is a live
production deploy, so treat it with care.

## Study waves (authoring the studies)

The plan for authoring studies book by book, current progress, the wave method,
and the validator live in `WAVE-HANDOFF.md` at the repo root. Read that before
running the next wave.

## Section maps

Each book of the Bible has a movement level plan at the repo root named
`<BOOK>-SECTION-MAP.md` (for example `GENESIS-SECTION-MAP.md`). These fix the
order and slug of every future study so they stay stable. Status `done` means
the study JSON exists in `src/content/studies/<book-kebab>/`. Psalms uses three
digit orders (001 to 150) because it has more than 99 movements.

## Native app link handling (permanent)

Capacitor's iOS local server does not resolve directory URLs. `CapacitorRouter`
returns the ROOT `index.html` for any path with no file extension, so navigating
to `/genesis/the-seven-days` inside the app renders the website landing page at
that URL instead of the study. Every same-origin navigation in the native app
must therefore go through `window.makorHref` (defined in
`src/components/AppNav.astro`), which rewrites a directory path to its explicit
`/…/index.html`. This applies to link clicks, JavaScript navigation, and
incoming Universal Links alike. If a native page ever lands on the landing page,
this is the first thing to check.

Universal Links are claimed by `public/.well-known/apple-app-site-association`
and `ios/App/App/App.entitlements` (`applinks:makor.co.za` and the www host).
The routing lives at the end of `src/layouts/Base.astro`: it normalises the path
through `window.makorHref`, confirms the page exists in this build of the bundle,
and opens the link in the system browser when it does not, because the bundle is
frozen at build time while the site keeps gaining studies.
