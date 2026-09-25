# Go deeper: the deepening campaign

Every teaching step in a study has two levels. The basic paragraph
(`study.basic.<step>`) is what every reader sees. The Go deeper level
(`study.<step>`) opens behind the button. As first drafted, Go deeper was often
no longer than the basic paragraph and said the same things in other words
(median about 70 to 95 words for originalLanguages, typology, christ, god,
crossReferences and oneStory, with roughly half its vocabulary shared with the
basic text). This campaign rewrites the Go deeper level of every study so it
goes as deep as the passage allows and never repeats the basic level.

## What changes and what must not

Change only these keys under `study`:

    context.literary, context.historical, context.canonical
    hermeneutics.authorIntent, hermeneutics.descriptionVsPrescription, hermeneutics.debates
    originalLanguages, typology, christ, god, crossReferences, oneStory

Never touch `study.basic`, `section`, `text`, `lexicon`, `quiz`, `questions`,
`translationNotes`, `meta`, `study.sermon` or `study.media`. The validator
compares every other key to git HEAD and fails the study if anything else moved.

## The bar

1. **New, never restated.** Assume the reader has just read the basic
   paragraph. Go deeper starts where it stops. Do not open by summarising the
   basic point. No sentence may paraphrase a basic sentence. The validator
   measures content-word overlap with the basic paragraph and fails anything
   above 0.30 for a field.
2. **As deep as the passage allows.** Real exegesis: the grammar and syntax,
   the structure of the passage, the history, the intertextual links, the
   theology, the questions careful readers actually wrestle with. Write for a
   serious lay reader or a seminary student, in Makor's plain, warm voice.
3. **Grounded.** Every claim is tied to the text. Cite chapter and verse. Every
   reference must exist (the validator checks each one against the BSB
   database). Use `tools/scripture/makor-scripture.mjs` for exact wording,
   cross reference seeds (`xrefs`) and BSB footnotes.
4. **No fabrication.** No invented lexical claims, statistics, dates,
   quotations, scholars or sources. If a lexical or historical point is not
   something you are sure of, leave it out. Quote Scripture only from the BSB
   and only exactly. Name historical interpreters only for well known,
   verifiable positions (Augustine, Calvin, the Reformers, the church fathers
   in general terms), never with invented quotations.
5. **House rules.** No em dashes or en dashes anywhere (use commas). No
   `{{key|word}}` lexicon tokens in these fields (they would print raw).
   Separate paragraphs with a blank line (`\n\n`); the page renders each as its
   own paragraph. Transliterate Hebrew and Greek in plain Latin letters as the
   studies already do (chesed, nephesh, logos); never original script here.
   Do not mention dashes, punctuation or house style.

## Minimum depth per field (words)

| Field | Minimum | Aim | What belongs there |
|---|---|---|---|
| context.literary | 150 | 200 to 350 | structure and movement of the passage, genre, devices (chiasm, inclusio, parallelism, repetition), where it sits in the book's argument |
| context.historical | 150 | 200 to 350 | setting, date, people, customs, geography, what the first hearers would have heard |
| context.canonical | 150 | 200 to 350 | how the passage is taken up earlier and later in Scripture, and quoted in the New Testament |
| hermeneutics.authorIntent | 120 | 150 to 250 | what the author meant the first hearers to grasp and do |
| hermeneutics.descriptionVsPrescription | 100 | 120 to 200 | what is recorded versus commanded, and how it applies now |
| hermeneutics.debates | 2 debates where real ones exist | | each question, two or three views with their case, and a bearing |
| originalLanguages | 350 | 400 to 650 | three to five words or constructions beyond those the basic text names: root and semantic range, stem, tense or aspect, how the word is used elsewhere (with references), the Septuagint where it matters, translation choices |
| typology | 3 entries | 3 to 6 | each `fulfillment` 60 to 130 words: the correspondence, the escalation in Christ, New Testament references, and where the type falls short |
| christ | 300 | 350 to 550 | how the passage leads to Christ by promise, pattern, theme or contrast, with the New Testament texts that make the link; guard against forced allegory |
| god | 300 | 350 to 550 | the attributes and works of God the passage actually shows, how it shapes the doctrine of God, tensions it holds together, and what it means for worship |
| crossReferences | 8 entries | 8 to 14 | each `note` 30 to 80 words saying exactly how the two texts connect |
| oneStory | 250 | 300 to 500 | where the passage sits in creation, fall, redemption, new creation: what it answers from before, what it sets up after, and how it ends in the new creation |

Context and hermeneutics were already fairly deep in many studies. Keep what is
good there and extend it to the bar; do not throw good material away.

## How to run it (what works)

- One general-purpose agent per 4 to 6 studies. Smaller chunks finish inside
  the connection window. Each agent re-reads and JSON-parses each file right
  after writing it.
- Edit the study file in place with a script that loads the JSON, replaces only
  the listed keys and writes it back with the same indentation style
  (`json.dumps(doc, ensure_ascii=False, indent=2)` is fine; the whole file is
  JSON and the site does not care about layout).
- After each chunk run the validator:

      python3 tools/deeper/check.py src/content/studies/<book>/<file>.json ...
      python3 tools/deeper/check.py --book genesis
      python3 tools/deeper/check.py --all --summary

  Fix every failure before moving on.
- Queue: `tools/deeper/queue.json` holds every study in chunks of four, in
  canonical order. One agent per chunk, prompt: "Read tools/deeper/AGENT-BRIEF.md
  and follow it exactly", plus the chunk's files.
- Per book, once every study passes: refresh the names lexicon
  (`makor-audio/names/README.md`, new words only), then render and upload that
  book's audio (`makor-audio/GPU-RUN.md`; build id `v3-names` forces the redo).

## Progress

Tracked in `tools/deeper/progress.json` (written by `check.py --all --summary`).

Paused 25 September 2026 at 191 of 1354: Genesis, Exodus, Leviticus and
Numbers complete, Deuteronomy 1 to 16, plus the pilots Psalm 23 and Romans 5
(Romans study 10). Resume with Deuteronomy 17. The run was paused to control
cost: each four-study agent used about 230,000 tokens on Opus. Before resuming,
decide the model (Sonnet is much cheaper), the concurrency, and whether to
schedule it in small daily batches.

Issues agents noticed in frozen basic text are listed in `tools/deeper/FLAGS.md`
for a separate, approved fix.
