# Scheduled Go deeper run (low cost, auto deploy)

Six scheduled runs a day. Each run deepens up to 16 studies with Sonnet agents
(never more than two at a time), checks them, refreshes the audio names,
builds the site, commits and pushes to main (a live deploy, authorised by
Luyanda on 25 September 2026 for these runs only), and starts the audio render
for the finished studies. Keep this session itself lean: do not read study
files or agent transcripts; rely on agent reports and the validator.

1. `cd ~/makor`. Run `python3 tools/deeper/next.py 16 --json`: up to four
   groups of four unfinished studies. If it prints `[]`, the campaign is done:
   skip to step 6 (upload), report, and stop.
2. Launch one background Agent per group with `model: "sonnet"`, TWO AT A TIME
   (start two, wait for both, then the next two). Prompt:

   > Read /Users/luyandajafta/makor/tools/deeper/AGENT-BRIEF.md and follow it
   > exactly. The model of the quality bar is the finished pilot
   > src/content/studies/genesis/03-the-fall.json (read its Go deeper fields
   > before you start). Rare-word or "occurs only here" claims must be ones you
   > are certain of; otherwise leave them out. Your study files: <files>. Keep
   > helper scripts in a private scratch folder <unique folder under /tmp>.
   > Finish with every file passing tools/deeper/check.py. Be efficient: read
   > only what you need, write each study in one script.

3. Run `python3 tools/deeper/check.py <all files from step 1>`. Note which
   pass. Failing ones are left for the next run; do not retry now.
4. Names: `cd makor-audio && .venv/bin/python names/harvest.py`. If it reports
   new words, launch one Sonnet agent to review only the new batch files,
   following `makor-audio/names/README.md` and matching the style of
   `names/lexicon.json`. Then `.venv/bin/python names/build.py` (it must
   report no issues; if it does, leave names out of this commit).
5. Deploy the website, only if at least one study passed:
   - `cd ~/makor && npm run build`. If the build fails, do not commit or push;
     report the error and stop.
   - `git add src/content/studies makor-audio/names tools/deeper`
   - `git commit -m "Deepen Go deeper: <books and study numbers that passed>"`
     (no em or en dashes; end with the line
     `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`)
   - `git push origin main`. If the push fails, report it and stop.
6. Audio (runs in the background after this session ends):
   - If `makor-audio/.env` exists, upload what earlier runs finished rendering:
     `cd makor-audio && nohup .venv/bin/python gpu_run.py --upload-staged >> _logs/upload.log 2>&1 &`
   - Write the passing study paths from step 3, one per line, to
     `makor-audio/_logs/render-<date-time>.txt`, then start four render shards:
     `for i in 1 2 3 4; do nohup .venv/bin/python gpu_run.py --files _logs/render-<date-time>.txt --offline --shard $i/4 --threads 3 >> _logs/render.log 2>&1 & done`
7. Report in four lines: studies deepened and pushed this run, total passing
   out of 1354 (`python3 tools/deeper/check.py --all --summary | tail -1`), the
   commit hash pushed, and any new lines in `tools/deeper/FLAGS.md`. Stop.
