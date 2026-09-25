# Brief for a deepening agent

You are deepening the "Go deeper" level of Makor Bible studies. Repo:
/Users/luyandajafta/makor. Read `DEEPER-HANDOFF.md` at the repo root first; it
is the full specification (what to change, the bar, minimum depth per field,
house rules). Then read your study files.

For each study you are given:

1. Read the whole study JSON: the passage (`text.units`), the basic level
   (`study.basic`), and the current Go deeper level (`study.context`,
   `study.hermeneutics`, `study.originalLanguages`, `study.typology`,
   `study.christ`, `study.god`, `study.crossReferences`, `study.oneStory`).
2. Gather material with the local scripture toolkit (Node 22.5 or newer):

       node tools/scripture/makor-scripture.mjs passage "ROM 5:12-21" --pretty
       node tools/scripture/makor-scripture.mjs xrefs "ROM 5:12" --limit 15
       node tools/scripture/makor-scripture.mjs footnotes ROM 5

   Use exact BSB wording for any quotation. Check each cross reference you use
   says what you claim it says.
3. Rewrite the Go deeper keys to the bar in DEEPER-HANDOFF.md. Keep what is
   already good and extend it; replace anything thin or that restates the basic
   level. Start where the basic paragraph stops. Real exegesis, grounded in the
   text, no fabrication, plain warm voice, no em or en dashes, paragraphs
   separated by a blank line, no `{{..}}` tokens, no original script.
   Before writing, reread every Hebrew or Greek word you name and confirm it
   is the word actually in that verse (for example Deuteronomy 18:18 and
   Jeremiah 1:9 both use natan, "give", not sim). If you are not certain of
   the exact word, describe the English phrase instead of naming a form.
4. Write the study back with a Python script that loads the JSON, replaces only
   the Go deeper keys, and dumps with `json.dumps(doc, ensure_ascii=False,
   indent=2) + "\n"`. Never touch `study.basic`, `section`, `text`, `lexicon`,
   `quiz`, `questions`, `translationNotes`, `meta`, `study.sermon`,
   `study.media`.
5. Run `python3 tools/deeper/check.py <your files>` and fix every failure
   (x lines). Treat ~ warnings seriously: add a second debate where a real one
   exists. Repeat until every file passes.

If you notice an error in the frozen basic level, lexicon or passage text, do
not fix it: append one line describing it to `tools/deeper/FLAGS.md`.

Do not run git, do not edit any other file. Report: each file, PASS or FAIL,
deep word count, and anything you were unsure of or left out for lack of
certainty.
