# Scheduled Go deeper run (low cost)

Each scheduled run deepens a small batch of studies with two Sonnet agents,
checks them, and stops. It never commits or pushes: Luyanda commits and deploys
himself (see CLAUDE.md). Keep this session itself lean: do not read study files
or agent transcripts yourself; the agents and the validator do the work.

1. `cd ~/makor`. Run `python3 tools/deeper/next.py 8 --json`. It prints up to
   two groups of four unfinished studies, in canonical order. If it prints
   `[]`, the campaign is done: report that and stop.
2. For each group, launch one background Agent with `model: "sonnet"` and this
   prompt, filling in the files and a unique scratch folder name:

   > Read /Users/luyandajafta/makor/tools/deeper/AGENT-BRIEF.md and follow it
   > exactly. The model of the quality bar is the finished pilot
   > src/content/studies/genesis/03-the-fall.json (read its Go deeper fields
   > before you start). Rare-word or "occurs only here" claims must be ones you
   > are certain of; otherwise leave them out. Your study files: <files>. Keep
   > helper scripts in a private scratch folder <folder>. Finish with every
   > file passing tools/deeper/check.py. Be efficient: read only what you
   > need, write each study in one script.

   Run the two agents at the same time, never more than two.
3. When both report back, run `python3 tools/deeper/check.py <the 8 files>`.
   Any study still failing is simply picked up again by the next run; do not
   retry it now.
4. If a book is now complete (`python3 tools/deeper/check.py --book <book>`
   shows all passing), refresh the audio names for it:
   `cd makor-audio && .venv/bin/python names/harvest.py`. If it reports new
   words, launch one Sonnet agent to review the new batch files, following
   `makor-audio/names/README.md` and matching the style of
   `names/lexicon.json`, then run `.venv/bin/python names/build.py`.
5. Run `python3 tools/deeper/check.py --all --summary` and report in three
   lines: studies done this run, total passing out of 1354, and any new lines
   in `tools/deeper/FLAGS.md`. Then stop.
