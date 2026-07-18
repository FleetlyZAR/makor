# Makor study waves: handoff for the next wave

This file lets any new chat working in this repo pick up the study-authoring
campaign. It assumes the Scripture Study Pipeline v1.2 project instructions are
active and the repo is connected.

## Progress (52 of 66 books, 732 studies)

Done: Genesis, Ruth, all 12 Minor Prophets (Hosea, Joel, Amos, Obadiah, Jonah,
Micah, Nahum, Habakkuk, Zephaniah, Haggai, Zechariah, Malachi), all 21 New
Testament epistles (Romans, 1-2 Corinthians, Galatians, Ephesians, Philippians,
Colossians, 1-2 Thessalonians, 1-2 Timothy, Titus, Philemon, Hebrews, James,
1-2 Peter, 1-3 John, Jude), the wave 5 short Old Testament books (Lamentations,
Ezra, Esther, Song of Solomon, Daniel, Nehemiah, Ecclesiastes), the wave 6
Gospels and Acts (Matthew, Mark, Luke, John, Acts), and the wave 7 histories so
far (Joshua, Judges, 1-2 Samuel, 1 Kings).

Remaining (14 books, 622 movements): Exodus, Leviticus, Numbers, Deuteronomy,
2 Kings, 1-2 Chronicles, Job, Psalms, Proverbs, Isaiah, Jeremiah, Ezekiel,
Revelation.

## Wave 7 in progress

Wave 7 (mid Old Testament histories) is partly done: Joshua (26), Judges (25),
1 Samuel (32), 2 Samuel (24), and 1 Kings (22) are written and their maps
flipped to done. Still to author to finish wave 7: 2 Kings (25), 1 Chronicles
(26), 2 Chronicles (34). After that, good targets are Revelation paired with the
wisdom books (Job, Proverbs). The heaviest remaining lifts are Psalms (150
movements, three digit orders), Isaiah, Jeremiah, and Ezekiel; the Pentateuch
(Exodus, Leviticus, Numbers, Deuteronomy) is also large.

Outstanding side task: a sermon-link pass. Many studies in waves 2 to 7 have
sermon status "none" because web verification was unstable during authoring.
Verified so far include wave 5 (Ezra 08 Piper; Esther 07 to 10 and Lamentations
02 to 03 Begg), wave 6 (Acts 08 to 09 Begg, Acts 10 to 11 Keller; Luke 01 to 08,
10 to 12, 16 Begg, Luke 02 and 15 Keller, Luke 17 Piper), and wave 7 (1 Kings 02,
08, 11, 19 Begg; 1 Kings 03, 17 Keller; 1 Kings 18 Piper). All of Matthew, Mark,
John, Joshua, Judges, 1-2 Samuel, and the rest await the link pass. Fill them
once the network is steady, verifying each link by web search.

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
