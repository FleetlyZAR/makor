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

Deploy facts: work is committed on the `main` branch and pushed to `origin`
(GitHub, FleetlyZAR/makor). Cloudflare rebuilds automatically on push, and the
site is usually live within about two minutes. Any push to main is a live
production deploy, so treat it with care.

## Section maps

Each book of the Bible has a movement level plan at the repo root named
`<BOOK>-SECTION-MAP.md` (for example `GENESIS-SECTION-MAP.md`). These fix the
order and slug of every future study so they stay stable. Status `done` means
the study JSON exists in `src/content/studies/<book-kebab>/`. Psalms uses three
digit orders (001 to 150) because it has more than 99 movements.
