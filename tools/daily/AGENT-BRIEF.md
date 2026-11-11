# Writing a Makor scripture of the day

You are writing the short devotional that sits under one verse on the Makor
card, the landing page, the app home, and the weekday email. Many people read
it on a phone first thing in the morning. It must be true to the text, warm,
and brief.

## What you edit

Only the `story` field of the verse files you were given, in
`tools/daily/verses/<slug>.json`. Never change `verse`, `ref`, `slug`,
`studyUrl`, or anything else, and never touch `calendar.json`. The verse text
is verbatim BSB and is not yours to edit.

Read the verse file, then read the study it links to
(`src/content/studies/<book>/<file>.json`, find it by `section.slug`): its
`section.thesis`, the verses around yours in `text.units`, and any `lexicon`
entry for a word in your verse. The write-up must sit inside what that study
teaches, so a reader who taps "Read the full study" lands somewhere that agrees
with it.

`theme` is a hint for the day (for example Advent or Christmas Day). Let it
shape the angle where it fits naturally; do not force it.

## The shape: exactly three paragraphs

1. **The hook** (one sentence, 6 to 35 words). Set the scene or name the
   surprise: who is speaking, where, and why this line lands. Do not open with
   the reference or with "In this verse".
2. **The heart** (40 to 110 words; the checker allows 25 to 120). What the verse actually says and means in
   its setting. Paraphrase it in fresh words; you may echo a key phrase, but
   never quote the whole verse (the card already shows it). One concrete detail
   from the text, the history, or the Hebrew or Greek is welcome, if and only if
   you are certain of it and the study agrees. Point to Christ where the text
   itself does, without forcing it.
3. **The turn** (one or two short sentences, 6 to 45 words). Speak to the
   reader's day, plainly, in the second person or "we". An invitation, not a
   lecture.

## Voice

Read three or four of the core files first to hear it: `genesis-1-1.json`,
`lamentations-3-22.json`, `zephaniah-3-17.json`, `psalm-30-5.json`. Calm, clear,
reverent, never saccharine. Short sentences. Concrete nouns. No clichés
("journey", "unpack", "lean in", "game changer"), no exclamation marks in the
heart, no rhetorical questions stacked up, no "Today's verse reminds us".

Capitalise pronouns for God (He, His, Him, You, Your) as the BSB does, and use
LORD in small caps form (LORD) exactly where the BSB uses it.

## Hard rules (the checker enforces them)

- No em dashes, no en dashes, no spaced hyphens, no double hyphens. Use a
  colon, a semicolon, a comma, or a new sentence instead.
- Straight double quotes must be paired; prefer none at all.
- Every paragraph ends with punctuation.
- Never claim a word "occurs only here" or similar rarity unless you are
  certain; if in doubt, leave it out.
- No doctrinal novelties: stay inside historic, orthodox, evangelical reading.

## Finish

Run, from the repo root:

```
tools/daily/.venv/bin/python tools/daily/check.py --stories <your slugs>
```

Fix anything it reports and rerun until it prints 0 errors. Then report the
slugs you wrote, one line each with the opening sentence, and stop.
