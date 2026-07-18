# Makor Scripture Toolkit

A lean, offline BSB scripture layer for the Makor study pipeline. It replaces
the live network dependency on `bible.helloao.org` with a small local database
and a zero dependency helper, so every study you produce can pull exact BSB
text, auto seeded cross references, and translation notes with no API calls.

## What is in here

- `makor-scripture.db` (about 20 MB): a purpose built SQLite file containing
  only what the pipeline needs.
  - `book`: the 66 BSB books, with common names and chapter counts.
  - `verse`: all 31,086 BSB verses, exact public domain text.
  - `footnote`: 4,846 BSB footnotes (literal renderings, alternate translations,
    New Testament citations).
  - `xref`: 344,799 scored cross references from the open-cross-ref dataset
    (OpenBible.info), keyed by verse.
- `makor-scripture.mjs`: a Node helper and command line tool. No dependencies.
  Requires Node 22.5 or newer (it uses the built in `node:sqlite`).

This is a build time authoring tool, not a shipped site asset. It never goes
into the browser bundle. The Makor renderer still reads finished studies from
`src/content/studies`. This toolkit feeds the step that produces them.

## Where to put it in the repo

Keep it out of the deploy bundle. Suggested home:

```
makor/
  tools/
    scripture/
      makor-scripture.db
      makor-scripture.mjs
      README-makor-scripture.md
```

Add `tools/scripture/makor-scripture.db` to `.gitignore` if you would rather
not commit 20 MB, and document how to rebuild it. If you do commit it, it is
small enough to be harmless.

## How the v1.2 pipeline uses it

Three study steps get faster and more reliable:

1. Data integrity (the whole passage, always). Instead of fetching each chapter
   over the network and risking `meta.textToVerify` guesses, pull the exact
   verses locally:

   ```
   node makor-scripture.mjs passage "GEN 1:1-2:3" --pretty
   ```

   Every verse comes back in order, in exact BSB, ready to drop into
   `text.units` (still apply the no dashes rule and the day refrain rule).

2. Cross references (study step 7). Seed the list from the scored dataset, then
   curate down and write the notes yourself:

   ```
   node makor-scripture.mjs xrefs "GEN 1:1" --limit 12
   node makor-scripture.mjs xrefs "GEN 1:1-2:3" --per-verse 5
   ```

   Scores rank strength of connection. For Genesis 1:1 the top hits are John
   1:1-3, Hebrews 11:3, Isaiah 45:18, Colossians 1:16-17, the same references a
   careful editor would reach for. The dataset seeds; you still judge.

3. Translation notes and lexicon hints. The BSB footnotes flag literal Hebrew
   and Greek renderings, alternate translations, and NT citations:

   ```
   node makor-scripture.mjs footnotes GEN 1
   ```

   These map onto the `translationNotes` field and often point to the load
   bearing words worth a `lexicon` entry.

## As a module

```js
import { getPassage, getFootnotes, getCrossRefs, listBooks } from "./makor-scripture.mjs";

const passage = getPassage("JHN 1:1-18");
const notes   = getFootnotes("GEN", 1);
const seeds   = getCrossRefs("GEN 1:1-2:3", { perVerse: 5, minScore: 40 });
```

Book codes are the three letter forms (GEN, EXO, PSA, JHN, ROM, REV, and so
on). Run `node makor-scripture.mjs books` for the full list.

## Boundaries and honest caveats

- BSB only, English only. This toolkit deliberately ships one translation. The
  full source set has over 1,000 translations, but the only Southern African
  language present is a Tswana New Testament, so this does not yet unlock
  isiZulu, isiXhosa, or Afrikaans for the driver and owner audience.
- Cross references seed, they do not decide. Always curate and write the
  `note` for each reference in Makor's own voice.
- Commentaries are not included here. The full source carries six public domain
  commentaries (Matthew Henry, Keil-Delitzsch, Jamieson-Fausset-Brown, John
  Gill, Adam Clarke, Tyndale Open Study Notes). They are useful as research for
  the Advanced layer, but they are old and uneven, so they must pass the
  orthodoxy filter and must never be auto published.
- License. BSB is public domain (dedicated 30 April 2023). The cross reference
  dataset is from OpenBible.info, adapted to the Free Use Bible API format.

## Rebuilding the database

The database was extracted from the English subset of the Free Use Bible API
build (`bible.eng.db`). To rebuild or extend it (for example to add a second
translation column, or the Tswana NT), keep the same schema and re index on
`(bookId, chapter, verse)`. Ask and I will regenerate the extractor script.
