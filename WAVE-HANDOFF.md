# Makor study waves: handoff for the next wave

This file lets any new chat working in this repo pick up the study-authoring
campaign. It assumes the Scripture Study Pipeline v1.2 project instructions are
active and the repo is connected.

## Progress (35 of 66 books, 379 studies)

Done: Genesis, Ruth, all 12 Minor Prophets (Hosea, Joel, Amos, Obadiah, Jonah,
Micah, Nahum, Habakkuk, Zephaniah, Haggai, Zechariah, Malachi), and all 21 New
Testament epistles (Romans, 1-2 Corinthians, Galatians, Ephesians, Philippians,
Colossians, 1-2 Thessalonians, 1-2 Timothy, Titus, Philemon, Hebrews, James,
1-2 Peter, 1-3 John, Jude).

Remaining (31 books, 975 movements): Exodus, Leviticus, Numbers, Deuteronomy,
Joshua, Judges, 1-2 Samuel, 1-2 Kings, 1-2 Chronicles, Ezra, Nehemiah, Esther,
Job, Psalms, Proverbs, Ecclesiastes, Song of Solomon, Isaiah, Jeremiah,
Lamentations, Ezekiel, Daniel, Matthew, Mark, Luke, John, Acts, Revelation.

## Recommended next wave (wave 5)

Short Old Testament books: Lamentations (5), Ezra (10), Esther (10), Song of
Solomon (11), Daniel (12), Nehemiah (13), Ecclesiastes (15). About 76 movements.
Alternatives: the Gospels and Acts, or the mid Old Testament histories.

Outstanding side task: a sermon-link pass. Many studies in waves 2 to 4 have
sermon status "none" because web verification was unstable during authoring.
Fill them once the network is steady, verifying each link by web search.

## How to run a wave (what worked)

1. One agent per book (general-purpose subagent). Not one per movement. Big books
   (over about 18 movements) can be cut off mid-run; if a book returns partial,
   dispatch a follow-up agent to write only the missing orders.
2. Run only TWO books concurrently. Four at once repeatedly hit API and session
   limits. Verify each sub-batch, then continue.
3. Each agent reads its `<BOOK>-SECTION-MAP.md` (authoritative order and slug)
   plus `src/content/studies/genesis/03-the-fall.json` and a same-genre example
   for format and depth; fetches exact BSB text from
   `https://bible.helloao.org/api/BSB/<CODE>/<CHAPTER>.json`; writes one JSON file
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
