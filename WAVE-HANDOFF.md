# Makor study waves: handoff for the next wave

This file lets any new chat working in this repo pick up the study-authoring
campaign. It assumes the Scripture Study Pipeline v1.2 project instructions are
active and the repo is connected.

## Progress (66 of 66 books, 1354 studies): the whole Bible is drafted

Done: Genesis, Ruth, all 12 Minor Prophets (Hosea, Joel, Amos, Obadiah, Jonah,
Micah, Nahum, Habakkuk, Zephaniah, Haggai, Zechariah, Malachi), all 21 New
Testament epistles (Romans, 1-2 Corinthians, Galatians, Ephesians, Philippians,
Colossians, 1-2 Thessalonians, 1-2 Timothy, Titus, Philemon, Hebrews, James,
1-2 Peter, 1-3 John, Jude), the wave 5 short Old Testament books (Lamentations,
Ezra, Esther, Song of Solomon, Daniel, Nehemiah, Ecclesiastes), the wave 6
Gospels and Acts (Matthew, Mark, Luke, John, Acts), the wave 7 mid Old
Testament histories (Joshua, Judges, 1-2 Samuel, 1-2 Kings, 1-2 Chronicles),
the wave 8 books (Revelation, Job, Proverbs, and the rest of the Pentateuch:
Exodus, Leviticus, Numbers, Deuteronomy, which completes the whole Torah,
Genesis through Deuteronomy), and the wave 9 major prophets Isaiah (64),
Jeremiah (41), and Ezekiel (42), and the Psalter (Psalms, all 150, three digit
orders 001 to 150).

Remaining: none. All 66 books of the Bible now have study JSON on disk. What is
left is verification and the sermon-link pass, not authoring. See the two open
caveats below before treating Psalms as finally sealed.

## Open caveats on Psalms (address on the next healthy run)

1. Text source. During Psalms authoring the local scripture toolkit database
   `tools/scripture/makor-scripture.db` became unreadable through the sandbox
   file mount (persistent "disk I/O error" / "Resource deadlock avoided"), so
   psalms roughly 059 to 150 were built from the exact Berean Standard Bible text
   on biblehub.com rather than from the toolkit. Every agent cross checked each
   psalm's verse count and its first and last verse against this section map, and
   psalms 001 to 058 used the toolkit directly. Still, on the next run when the
   toolkit reads cleanly, spot check a sample of the web sourced psalms
   (say 060, 078, 104, 119, 145) verse by verse against
   `node tools/scripture/makor-scripture.mjs passage "PSA N:1-M"` to confirm exact
   BSB wording.

2. Validation. The full validator could not complete in one pass because the file
   mount intermittently deadlocked on individual psalm files under load. As of
   this run, 119 of 150 psalm files were confirmed by script with zero issues
   (JSON valid, no em or en dashes, quiz weights one each of 0/25/75/100, all
   lexical tokens resolved), and several of the remaining files that the mount
   would not read for the script (for example 002 and 034) were confirmed clean
   by hand through the host file reader. Re run the validator below over
   `psalms` once the mount is healthy to get a clean zero over all 150, and fix
   any stray em dash the way the Ezekiel dashes were fixed this wave.

## Recommended next wave (wave 9)

Wave 8 is complete (240 studies, validator clean): Revelation, Job, Proverbs, and
the Pentateuch remainder (Exodus, Leviticus, Numbers, Deuteronomy). The Torah,
the Gospels and Acts, all the epistles, Revelation, the Minor Prophets, the wisdom
books, and every historical book are now done. Isaiah (64), Jeremiah (41), and
Ezekiel (42) are complete and validator clean, and the Psalter (all 150) is
drafted, which finishes every book of the Bible. There is no authoring left. The
next run is a finishing pass: clear the two Psalms caveats above (toolkit text
spot check and one clean validator sweep over all 150 psalms), then work the
long standing sermon-link pass across the whole site, verifying each link by web
search.

Note on chunk size: keep authoring chunks to about 6 to 8 studies. During
Jeremiah, two subagents assigned 14 studies each were cut off by mid response API
connection errors; one left a file with stray characters (invalid JSON). Smaller
chunks finish inside the connection window, and every agent should re read and
JSON parse each file right after writing it. If a run is interrupted, check which
orders exist, validate them, regenerate any that do not parse, and author the
missing orders in a fresh agent. A same-genre example for the prophets: any Minor Prophet study, for example
`src/content/studies/hosea/` or `src/content/studies/amos/`; the wave 8 Job and
Ecclesiastes studies are the closest models for the Hebrew poetry of the Psalms.

Note on the mount: during wave 8 the workspace file mount intermittently threw
"Resource deadlock avoided" on the section-map files under concurrent load. The
study JSON files always read and wrote fine; only the shared maps contended.
Reliable workarounds that worked: use the Edit tool (not bash sed) to flip map
rows, and validate study files against a reconstructed in-code map when a
`<BOOK>-SECTION-MAP.md` will not read. All wave 8 maps were flipped and confirmed
clean regardless.

Outstanding side task: a sermon-link pass. Many studies in waves 2 to 7 have
sermon status "none" because web verification was unstable during authoring.
Verified so far include wave 5 (Ezra 08 Piper; Esther 07 to 10 and Lamentations
02 to 03 Begg), wave 6 (Acts 08 to 09 Begg, Acts 10 to 11 Keller; Luke 01 to 08,
10 to 12, 16 Begg, Luke 02 and 15 Keller, Luke 17 Piper), and wave 7 (1 Kings 02,
08, 11, 19 Begg, 03, 17 Keller, 18 Piper; 2 Kings 05 Keller, 25 Begg; 1 Chron 26
Keller; 2 Chron 05 Begg, 14 Piper, 18 and 24 Begg). All of Matthew, Mark, John,
Joshua, Judges, 1-2 Samuel, and the rest await the link pass. Fill them once the
network is steady, verifying each link by web search.

## Local scripture toolkit (use this for BSB text and cross refs)

`tools/scripture/` is an offline BSB layer that replaces the live dependency on
`bible.helloao.org`. Prefer it: it is faster, deterministic, and it seeds cross
references and translation notes. It is a build time authoring tool only, never a
shipped site asset; the renderer still reads finished studies from
`src/content/studies`.

Contents:

- `makor-scripture.db` (about 20 MB): SQLite with all 66 books, all 31,086 exact
  BSB verses, 4,846 BSB footnotes, and 344,799 scored cross references from
  OpenBible.info.
- `makor-scripture.mjs`: a zero dependency Node helper and CLI. Needs Node 22.5
  or newer (uses the built in `node:sqlite`).

Command line (book codes are three letter forms, GEN, EXO, PSA, JHN, 1SA, 2KI):

```
node tools/scripture/makor-scripture.mjs passage "1KI 8:1-66" --pretty
node tools/scripture/makor-scripture.mjs xrefs "1KI 8:27" --limit 12
node tools/scripture/makor-scripture.mjs footnotes 1KI 8
node tools/scripture/makor-scripture.mjs books
```

Use it for three study steps: passage text (drop straight into `text.units`,
still apply the no dashes rule), cross reference seeds for study step 7 (the
scores rank strength; you still curate and write each `note` in Makor's voice),
and footnotes that map onto `translationNotes` and often flag the load bearing
words worth a `lexicon` entry. The cross reference dataset seeds, it does not
decide. See `tools/scripture/README-makor-scripture.md` for the module API and
rebuild notes.

## How to run a wave (what worked)

1. One agent per book (general-purpose subagent). Not one per movement. Big books
   (over about 18 movements) can be cut off mid-run; if a book returns partial,
   dispatch a follow-up agent to write only the missing orders.
2. Run only TWO books concurrently. Four at once repeatedly hit API and session
   limits. Verify each sub-batch, then continue.
3. Each agent reads its `<BOOK>-SECTION-MAP.md` (authoritative order and slug)
   plus `src/content/studies/genesis/03-the-fall.json` and a same-genre example
   for format and depth; pulls exact BSB text, cross reference seeds, and
   footnotes from the local scripture toolkit (see the section below), falling
   back to `https://bible.helloao.org/api/BSB/<CODE>/<CHAPTER>.json` only if the
   toolkit is unavailable; writes one JSON file
   per map row to `src/content/studies/<book>/NN-slug.json` per schema v1.2; uses
   inline `{{lexKey|word}}` tokens that all resolve with no unused lexicon keys;
   gives every quiz item exactly one option at each weight 100, 75, 25, 0; writes
   4 to 6 reflection questions; sets sermon status "verified" with a URL only if
   confirmed by web search that session (Alistair Begg / Truth For Life, Tim Keller
   / gospelinlife.com, John Piper / desiringgod.org, Sinclair Ferguson, D.A. Carson),
   otherwise "none".
4. Hard rules: never use em or en dashes anywhere including Bible text (render as
   commas). No fabrication of text, URLs, citations, or lexical claims. Omit media
   unless a video id is verified.
5. After the wave, run the validator (below) and fix flags. The recurring defect is
   quiz weights `[0,25,25,100]`: promote the better of the two 25 options to 75 by
   content. A verse "gap" is acceptable when the BSB legitimately omits a variant
   verse (for example Romans 16:24) and the file documents it in translationNotes.
6. Flip the wave's maps to done:
   `for MAP in BOOK1 BOOK2; do sed -i 's/| planned |/| done |/g' "$MAP-SECTION-MAP.md"; done`
7. Claude never runs git. Hand Luyanda a commit message; he pushes via Visual
   Studio. If git reports index.lock exists, he clears it with
   `sudo rm -f .git/index.lock`.

## Validator (run from repo root; set the books map per wave)

```
python3 - <<'PY'
import json, re, glob, os
books={'lamentations':'LAMENTATIONS','ezra':'EZRA'}  # set to the wave's books
req={'schemaVersion','book','section','text','lexicon','study','quiz','questions','translationNotes','meta'}
def pm(mf):
    rows={}
    for l in open(mf,encoding='utf-8'):
        if re.match(r'^\|\s*\d+\s*\|',l):
            c=[x.strip() for x in l.strip().strip('|').split('|')]
            if '-' in c[1]:
                m=re.search(r'(\d+):(\d+)\s*-\s*(?:(\d+):)?(\d+)',c[1]); sc,sv,ec,ev=int(m[1]),int(m[2]),int(m[3] or m[1]),int(m[4])
            else:
                m=re.search(r'(\d+):(\d+)',c[1]); sc,sv=int(m[1]),int(m[2]); ec,ev=sc,sv
            rows[int(c[0])]=(c[3],(sc,sv),(ec,ev))
    return rows
issues=[]
for kb,MAP in books.items():
    rows=pm(f'{MAP}-SECTION-MAP.md')
    files=sorted(glob.glob(f'src/content/studies/{kb}/*.json'))
    if len(files)!=len(rows): issues.append(f'{kb}: {len(files)} files vs {len(rows)} rows')
    for f in files:
        fn=os.path.basename(f); order=int(fn[:2]); raw=open(f,encoding='utf-8').read()
        try: d=json.loads(raw)
        except Exception as e: issues.append(f'{kb}/{fn}: BAD JSON {e}'); continue
        if '—' in raw or '–' in raw: issues.append(f'{kb}/{fn}: dash')
        if req-set(d): issues.append(f'{kb}/{fn}: missing {req-set(d)}')
        slug,start,end=rows.get(order,(None,None,None))
        if slug and d['section']['slug']!=slug: issues.append(f'{kb}/{fn}: slug')
        v=[(x['chapter'],x['n']) for u in d['text']['units'] for x in u['verses']]
        if start and v and (v[0]!=start or v[-1]!=end): issues.append(f'{kb}/{fn}: bounds')
        lex=set(d['lexicon']); toks=set(re.findall(r'\{\{([^|}]+)\|',raw))
        if toks-lex: issues.append(f'{kb}/{fn}: unresolved {toks-lex}')
        if lex-toks: issues.append(f'{kb}/{fn}: unused {lex-toks}')
        for i,q in enumerate(d['quiz']):
            if sorted(o['weight'] for o in q['options'])!=[0,25,75,100]: issues.append(f'{kb}/{fn}: quiz{i+1} weights')
print("ISSUES:",len(issues))
for i in issues: print("  -",i)
PY
```

## Site notes relevant to authoring

The home page loads each book's movements lazily from `/search-index.json` (a
build-time endpoint) when a book is expanded, so new studies appear automatically
once deployed; no home-page edit is needed per wave. Movement pills have three
states: green (reader completed), gold (available, not done), plain text with a
soon tag (not yet written).

## Audio narration (Kokoro, four voices)

Every study can be narrated by Kokoro (free, Apache 2.0, self-hosted), cut by
movement and by teaching step, in four voices (US and UK, male and female). The
pipeline lives in `makor-audio/` (`generate_audio.py`, `pronounce.json`,
`README.md`). Audio is generated once, stored as static MP3, and served from
Cloudflare R2, never synthesised on a page view.

Per study:

```
cd makor-audio
python3 generate_audio.py \
  --study ../src/content/studies/<book>/NN-slug.json \
  --format mp3 --base https://audio.makor.co.za/
```

Output lands in `public/studies/<book>/<slug>/audio/`. Do NOT commit audio into
git or the Pages deploy (Cloudflare Pages caps a deployment at 20,000 files).
Upload to R2 instead, then it is served from the R2 public domain:

```
rclone copy public/studies r2:makor-audio/studies --transfers 8
```

Bulk run for the whole corpus (all 1354 studies already exist on disk, so this is
a one-time batch, not incremental; budget roughly a day of unattended CPU for all
four voices, then upload):

```
cd makor-audio
find ../src/content/studies -name '*.json' | while read f; do
  python3 generate_audio.py --study "$f" --format mp3 --base https://audio.makor.co.za/
done
rclone copy ../public/studies r2:makor-audio/studies --transfers 8
```

Before a book's bulk run, add its hard names to `makor-audio/pronounce.json` (for
example Melchizedek, Nebuchadnezzar, Zerubbabel), since text to speech will
otherwise mangle them. `--dry-run` prints the spoken text with fixes applied.

### Renderer and completion wiring (done)

`src/components/AppAudioPlayer.astro` renders an inline chapter/track player on
every study page (`[book]/[slug].astro`), resolving the manifest from
`PUBLIC_MAKOR_AUDIO_BASE` (set this env var in Cloudflare Pages; it defaults to
`https://audio.makor.co.za/`). It hides itself when a study has no audio yet, so
it is safe on studies not yet voiced.

Listening all the way through saves an unscored completion: a new attempts row
with `phase: 'listen'`, `score: 0`. This required widening the Supabase check
constraint `attempts_phase_check` to allow `pre`, `post`, and `listen` (migration
`attempts_phase_allow_listen`, already applied to the makor project). The app's
six completion checks (Base, AppHome, AppTabBar, AppStudyBar, index, plan) now
count `post` OR `listen` as done, while quiz scores and the perfect-score badge in
`progress.astro` still come only from `post`. A study can be finished by listening
through, by the quiz, or both; the quiz adds a score, listening does not.
