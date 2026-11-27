# Makor films: handoff (6 October 2026)

Read this first in any new session working on Makor films. Then `AUTOPILOT.md` for how a film runs from cast
approval to the final cut.

## Where things stand

- **The Seven Days** (Genesis 1:1 to 2:3), `films/genesis/01-the-seven-days/`: finished and
  uploaded to YouTube by Luyanda. Spend 36.81 USD (`COSTS-movement.md`). 18 of its 41 Veo
  clips exist; the rest are only needed for a re-upload, which is not planned. Versions in
  `exports/`: the film, YouTube, vertical (TikTok and Instagram), one minute short, publishing
  packs (`youtube-pack.md`, `short-pack.md`).
- **The Garden** (Genesis 2:4 to 25), `films/genesis/02-the-garden/`: in production.
  - Done: script (`script/movement.py`, 22 verses verified), voice track, animatic, world bible,
    92 keyframes (`stills/movement/`), sound effects, full cut `exports/the-garden-v1.mp4`
    (10:38, depth motion on every shot, re-cut Seven Days score, 34 sound placements).
  - M5 in progress: 20 Veo clips (12 Lite, 8 Fast) via the scheduled task
    `makor-veo-daily` (09:06 daily, stops at 40 USD). Spend so far 8.25 USD of a 75 USD cap.
    No clips yet: on 6 October the day's Veo quota had gone to The Seven Days, so the first
    run is 7 October and Lite (about 10 a day) finishes on 8 October.
  - One minute short done (6 October, from keyframes, free): script approved
    (`script/one-minute-script.md`), `edit/short.py` (GUIDE lines from `edit/short_guide.py`),
    `exports/the-garden-in-a-minute.mp4` (59.7 s) and the WhatsApp copy, `exports/short-pack.md`.
    Rerun `edit/short.py` if the score or the keyframes change.
  - YouTube and vertical versions built from v1 (6 October): `exports/the-garden-youtube.mp4`
    (11:02, with `the-garden-youtube.srt`, the v1 captions moved 4 s later for the opening) and
    `exports/the-garden-vertical.mp4` (10:38). Rebuild both after the clips land:
    `platform_versions.py films/genesis/02-the-garden youtube vertical`, then shift the new
    v1 captions again (`ffmpeg -itsoffset 4 -i the-garden-v1.srt the-garden-youtube.srt`).
  - Still to do after the clips: review the task's flags, trim bad clips (`clip:A-B` flag in
    `script/shotlist.py`), rebuild, then the YouTube and vertical versions again and the YouTube
    publishing pack. Artwork is done (6 October): thumbnails A s023 (the garden in the east)
    and B s088 (the garden city), with 1280x720 previews, channel icon and watermark, in
    `exports/art/`; it does not change with the clips. Then disable the scheduled task.
- **Photoreal for every film except The Seven Days (7 October 2026).** Luyanda approved the
  photoreal treatment (`STYLE-BIBLE.md`, "Photoreal"; shared prompt wording in
  `tools/photoreal.py`) after the test in `films/tests/`. The Seven Days stays painted as it is.
  Each converted film keeps its painted stills and clips in `stills/*-painted/` and
  `clips/movement-painted/`.
  - The Garden: cast in `stills/cast/` (adam.jpg = portrait B, eve.jpg = option A), photoreal
    world bible and all 92 keyframes passed C2. Clips made 7 October: Veo Standard for people,
    Gemini Omni Flash (`tools/omni_clip.py`) for landscapes; s059 and s069 stay depth motion
    (Veo refused them). v1 rebuilt photoreal 7 October (10:44, 55.51 USD). `makor-veo-daily`
    makes the last three clips (s022, s080, s085) on 8 October and rebuilds; then the YouTube,
    vertical, short and artwork versions (AI disclosure Yes), then disable the task. Methods and
    measured costs: `VIDEO-METHODS.md`.
  - The Fall: `makor-fall-veo-daily` paused (its painted clips retired). `world_bible.py` and
    `shotlist.py` converted (nothing worn before 3:7, fig leaves from 3:7, hides from 3:21;
    key people shots nearer; 3:24 is now a whirling sword of flame, as the BSB says, not a ring).
    World bible and all keyframes done 7 October (29.15 USD), C2 passed. `makor-fall-veo-daily` is
    re-pointed at its 20 photoreal clips (10 Fast, 10 Lite; stop at 47 USD), starting 9 October
    after The Garden finishes; it rebuilds the film when complete.
- **The Fall** (Genesis 3:1 to 24), `films/genesis/03-the-fall/`: started 6 October 2026.
  - M0 draft done: `script/movement.py` (24 verses verified, 11 chapters, about 11:53
    estimated). C1 passed: script and all ten decisions approved (quotations kept), see
    `PRODUCTION-PLAN.md`. Spend 0.00 USD (`COSTS-movement.md`).
  - Done 6 October: voices (11:24), animatic (101 shots), world bible, shot list, sound cues,
    film.json scores and sfx, 98 keyframes (34 rerolled after the rule check). C2 passed.
  - M5: scheduled task `makor-fall-veo-daily` (about 09:46 daily, after The Garden's task; 19 clips,
    9 Fast and 10 Lite; stops at 25 USD for checkpoint C3).
  - M7 built from keyframes (7 October): v1 (11:30), YouTube (11:54) and vertical versions,
    artwork (A s079, B s004), short (59.5 s), packs. C4 passed: short script and thumbnails approved. Rebuild all after the clips
    (see the film's PRODUCTION-PLAN.md). Spend 10.82 USD.
  - Working pattern: run every step without stopping, paid steps included, except checkpoints
    C1 (script), C2 (keyframe sheets), C3 (each 25 USD), C4 (finished versions and packs).
  - `movement_script.py` gained a `SPEAKERS` override (explicit, verified per verse splits)
    because Genesis 3 tags God's speech in ways the generic detector misses.

- **Cain and Abel** (Genesis 4:1 to 16), `films/genesis/04-cain-and-abel/`, episode 4: v3 cut approved by Luyanda
  16 October 2026. Built: `exports/full-cut-v3.mp4` (18:03), the YouTube version `exports/cain-and-abel-youtube.mp4`
  (18:23, captions, chapters), `exports/youtube-pack.md` (vidIQ research, titles, tags), three thumbnails, ten
  question Shorts in `exports/shorts/`. Spend about 31.6 USD. Music is still temp. Waiting on the YouTube ID to
  embed the film in the study (as The Fall: `study.media.film` in the study JSON). Next: Two Lines, Cain and Seth.
- **Two Lines, Cain and Seth** (Genesis 4:17 to 26), `films/genesis/05-two-lines-cain-and-seth/`, episode 5: final
  after C6 (5 November 2026), see its `TREATMENT.md`.
- **From Adam to Noah** (Genesis 5:1 to 32), `films/genesis/06-from-adam-to-noah/`, episode 6: M0 draft 5 November
  2026, `script/movement.py` (32 verses, 26 quotations verified, 20:17 estimated) and `TREATMENT.md` with decisions
  D1 to D9. C1 approved 5 November (all as proposed). Voices rendered (111 lines, 0.61 USD), six breath
  beats added, animatic 20:55 (181 shots), no teaching run over 56 s. Casting: 28 portraits (3.75 USD, total 4.36),
  cast locked 5 November (picks approved, two ages, nine turnarounds; film total 5.97 USD).
  The peoples rule went into STYLE-BIBLE.md the same day: Noah's sons are one family with one skin, and the nations'
  range comes in the Table of Nations and Babel films. World bible: eight new location masters (1.61 USD).
  Storyboard: 193 shots, 148 new keyframes by Batch, 34 rerolls and one more redo; film total 19.91 USD.
  C2 approved 6 November. LTX prompts in script/ltx_prompts.py; 155 clips rendering with --nag under the battery
  rule (about 22 GPU hours). 18 sound effects (0.22 USD) and a temp score with the toll (edit/score_mix.py, -16.0
  LUFS); film total 20.13 USD. All 155 clips made 7 November and reviewed (edit/clip-review.md): 125 pass, 30 back
  for seed 11. The main fault was the prompt line "on a tripod", which drew a camera tripod into 20 clips; it is now
  "static and locked off" with a tripod/crew/cut negative on every clip. The 30 redos reviewed 8 November: 24 pass,
  6 back for seed 13 with hand written prompts (framing to match the keyframe, steady light); all 6 passed, so all
  155 clips pass. C3 cut 9 November: exports/full-cut-v1.mp4 (20:55, -16.1 LUFS, edit/full_cut.py), with the
  count, the long lives timeline and every card painted in the edit. C3 notes (17) fixed the same day: 18 clips re-rendered (five twice), eight new keyframes, "Lived" re-voiced; C4 cut exports/full-cut-v2.mp4 (20:55, -16.1 LUFS), film total 21.47 USD. C4 notes (10) fixed: ten clips re-rendered (s074 twice), six new keyframes, and the voice track rebuilt so the re-voiced "Lived" finally reaches the mix (C4 still had the old take); C5 cut over exports/full-cut-v2.mp4, film total 22.54 USD. C5 approved 10 November 2026. YouTube cut exports/from-adam-to-noah-youtube.mp4 (21:15, -14 LUFS, captions, chapters, end screen to The Grief of God), ten question Shorts in exports/shorts/, publishing pack exports/youtube-pack.md, vidIQ thumbnails in exports/art/vidiq/ (title 98; eight Shorts 95 to 97, main 88, Lamechs 93, Luke 94). Not uploaded. Next: Luyanda uploads, then the study embed once the YouTube ID exists.
- **The Grief of God** (Genesis 6:1 to 8), `films/genesis/07-the-grief-of-god/`, episode 7: M0 draft 10 November
  2026, `script/movement.py` (8 verses, 27 quotations of other Scripture verified, 18:32 estimated, longest
  teaching run 55 s) and `TREATMENT.md` with decisions D1 to D10 (the sons of God never shown by face, the
  taking as seizure never romance, the Nephilim as tall human warriors, God's grief as the light drawing back off
  the plain, creation wound backward, noach turning to chen on screen). C1 approved 12 November (all as proposed). Voices rendered (93 lines, 0.36 USD),
  GOD re-taken slower (0.78, 0.07 USD), scored animatic 18:29 (159 shots, edit/score_mix.py from the cue sheet; no
  animatic ever carries the stock light-breaking track again), longest teaching run 56 s. Cast locked 12 November (13 portraits, three turnarounds; the watcher's
  reference cropped so no face shows). World bible 12 November: 15 new location masters (the plain in four lights, the walled
  town, Noah's shelter, the worn stone, Herod's Jerusalem at evening, the thorns, the beam ground); storyboard 209 shots, 141 keyframes
  checked (ten redone); film total 16.04 USD. C2 approved 12 November; all 199 LTX clips made by 14 November and reviewed (edit/clip-review.md): 185 pass, then 12 of 14 with seed 11, s077 and s128 with seed 13, and s118 (the toy read as a pig) with a new keyframe from the cut review. Final cut v1 by autopilot 14 November (films/AUTOPILOT.md): exports/full-cut-v1.mp4 (18:30, -16.2 LUFS, edit/full_cut.py; the three readings panels, noach turning to chen with a chime, title, end card), notes in edit/final-cut-notes.md; film total 16.31 USD. Luyanda's 30 notes on v1 (15 November, edit/review-v1-notes.md) answered in cut v2 on 16 November: v2 storyboard (picture follows narration, faces close or not seen, seven continuous takes, Jesus only from behind), 66 new LTX clips with ten redone, s074 keyframe redone for dress and skin, exports/full-cut-v2.mp4 (18:30, -16.3 LUFS), notes in edit/final-cut-notes.md; film total 22.67 USD (the 25 USD checkpoint was lifted for this film only). Music is temp. Cut v2 approved by Luyanda 17 November 2026 ("beautiful, near perfect"). YouTube cut exports/the-grief-of-god-youtube.mp4 (18:50, -14.2 LUFS, captions, chapters, end screen to Noah and the Ark; edit/youtube_cut.py), ten question Shorts in exports/shorts/ (edit/shorts_qa.py, edit/shorts_metadata.py), publishing pack exports/youtube-pack.md with the channel's own numbers, Shorts playlist exports/shorts/playlist.md, vidIQ thumbnails in exports/art/vidiq/ (title 98, main thumbnail 96, all ten Shorts titles 96 to 98 and covers 95 to 100; alternate main 85). No new USD spend (1,219 vidIQ credits); film total 22.67 USD. Not uploaded. Next: Luyanda uploads, then the study embed once the YouTube ID exists; then Noah and the Ark (Genesis 6:9 to 22).
- **Noah and the Ark** (Genesis 6:9 to 22), `films/genesis/08-noah-and-the-ark/`, episode 8: M0 draft 17 November
  2026, rewritten the same day for retention against our own YouTube curves and the best performing films on the
  subject (vidIQ; `TREATMENT.md`, "Retention design"). `script/movement.py` (14 verses, 20 quotations of other
  Scripture verified, 18:47 estimated, hook at 0:17, title at 0:48, first verse at 0:51, longest teaching run 55 s;
  God's speech 6:13 to 21 split from the study JSON, not typed) and `TREATMENT.md` with decisions D1 to D12 (the
  ark a chest with no keel or rudder, no flood water or animals at the ark or rainbow in this film, the pattern
  drawn in gold over empty ground, shachat lit four times, the ark's one door match cut to the empty tomb, a
  working title about how the ark was built). C1 approved 17 November: 87 lines voiced; third pass the same day
  for punchier wording (the hook is four questions the film answers; MrBeast's rules in `TREATMENT.md`), 18:27 on
  the real voices (questions 0:14, title 0:33, first verse 0:36). `exports/movement-animatic.mp4` is voices only:
  from this film on no animatic carries sound that will not be in the finished film (no temp music;
  `tools/animatic.py` changed). 13 casting portraits with picks proposed in `script/cast.md` (sheet
  `exports/cast-sheet.jpg`). Cast locked 17 November and autopilot started: five turnarounds, 13 world bible masters
  (the ark a flat sided chest, `stills/bible/ark-finished.jpg`), storyboard of 230 shots, all 206 keyframes made and
  approved (27 redone), film total 21.94 USD. LTX render running under the battery rule since 13:44 on 17 November
  (`governor.log`; 224 clips). Ready: `edit/score_mix.py`, `edit/full_cut.py`, `edit/clip_review.py`. Next: review
  every clip (`edit/clip-review.md`), redo failures, then the cut and its QA. Render ended 21 November 2026 (224 LTX clips, all reviewed in edit/clip-review.md: 216 pass first time, eight redone with hand written prompts in script/ltx_prompts.py, all pass). Final cut v1 by autopilot 21 November: exports/full-cut-v1.mp4 (18:27, -16.4 LUFS, true peak -1.4 dBFS; edit/full_cut.py with the gold chest drawing, shachat, proportions and cube, title, end card; s215 cropped for side bars), review copy exports/full-cut-v1-review.mp4, notes and judgment calls in edit/final-cut-notes.md; film total 21.94 USD. Sound checked by numbers only. Luyanda's ten notes on v1 (21 November) answered in cut v2 the same day: ark redesigned at true 300 x 50 x 30 proportions from a scale model (script/ark_guide.py, new masters in stills/bible/, 33 ark keyframes remade, 25 USD checkpoint lifted to about 27.50 for this redo), gold drawing and proportions card as a 3D box to scale, four new corruption shots, the s048/s049 take, s197 Jesus keyframe remade, static starts trimmed (edit/clip_trims.json); 46 clips redone. exports/full-cut-v2.mp4 (18:27, -16.4 LUFS), review copy exports/full-cut-v2-review.mp4, notes in edit/final-cut-notes.md; film total 27.37 USD. Luyanda's three notes on v2 (0:10 drag, 8:02 backwards walk, 11:35 birds) fixed in cut v3 the same evening: s005 and s149 new keyframes at half price, s100 new prompt (seed 7). exports/full-cut-v3.mp4 (18:27, -16.4 LUFS), review copy exports/full-cut-v3-review.mp4; film total 27.50 USD. Publishing pack built 21 November from cut v3: YouTube cut exports/noah-and-the-ark-youtube.mp4 (18:47, captions, chapters, end screen to The Flood; edit/youtube_cut.py), ten question Shorts in exports/shorts/ (edit/shorts_qa.py, edit/shorts_metadata.py), exports/youtube-pack.md, vidIQ thumbnails in exports/art/vidiq/ (title 100, main thumbnail 97, all ten Shorts titles 95 to 98 and covers 95 to 100). No new USD spend (vidIQ credits only). Not uploaded. Next: Luyanda uploads, then the study embed once the YouTube ID exists; then The Flood (Genesis 7).
- **The Flood** (Genesis 7:1 to 24), `films/genesis/09-the-flood/`, episode 9: M0 draft 21 November 2026, written
  to Noah and the Ark's third pass standard (`TREATMENT.md`). `script/movement.py`: 24 verses and 17 quotations
  verified, 18:13 estimated, the four questions at 0:18, title 0:35, first verse 0:38, longest teaching run 53 s;
  God's speech 7:1 to 4 split from the study JSON. Decisions D1 to D12 (the door shuts with no hand on it; no one
  dies on screen; the water from below and above; no dove, land or rainbow; open loop on "But God remembered
  Noah"). C1 approved 21 November: 94 lines voiced (0.57 USD), 18:16 on the real voices (questions 0:15,
  title 0:31, first verse 0:34); `exports/movement-animatic.mp4` voices only. Cast all carried over from Noah and the
  Ark (`script/cast.md`, `exports/cast-sheet.jpg`), no new portraits. Cast locked 21 November and autopilot started: 11 new world bible
  masters, storyboard of 245 shots, all 216 keyframes made and reviewed (70 redone), the film's own sound effects, score
  and mix (-16.2 LUFS), `edit/full_cut.py` with the Hebrew words and the date in gold. LTX render running under the
  battery rule; render ended 23 November (243 clips, all reviewed in `edit/clip-review.md`: 230 pass first time, five
  remade from current prompts, eight redone at seed 11 with hand written prompts in `script/ltx_prompts.py`, all pass;
  s061 cropped in the cut). Final cut v1 by autopilot 23 November: `exports/full-cut-v1.mp4` (18:16, -16.2 LUFS, true
  peak -1.4 dBFS), review copy `exports/full-cut-v1-review.mp4`, notes and judgment calls in `edit/final-cut-notes.md`.
  Film total 22.37 USD. Luyanda's v1 review (24 November: the ark afloat short and barn like, skin and hair drifting
  from behind, an arm from a top corner, picture against the words, the gap at 12:15) answered in cut v2: two broadside
  afloat masters at true proportions (`script/bible-fix.md`), every afloat keyframe and clip remade locked off, s220 and
  s239 hands remade, the 12:15 passage rewritten and re-voiced; s194 and s197 still pushed in after two seeds, so
  `edit/full_cut.py` STAB cancels the push frame by frame. `exports/full-cut-v2.mp4` (18:17, -16.2 LUFS, true peak
  -1.4 dBFS, no freezes), review copy `exports/full-cut-v2-review.mp4`, notes in `edit/final-cut-notes.md`. Film total
  26.93 USD. Publishing pack built 24 November from cut v2: YouTube cut `exports/the-flood-youtube.mp4` (18:37, -14.1
  LUFS, captions, chapters, end screen to The Waters Recede; `edit/youtube_cut.py`), eight cliffhanger Shorts in
  `exports/shorts/` that stop before their answer and point to the minute of the film that gives it
  (`edit/shorts_qa.py`, `edit/shorts_metadata.py`), `exports/youtube-pack.md`, vidIQ thumbnails in
  `exports/art/vidiq/` (title 99, main thumbnail 98, Shorts titles 95 to 98, covers 96 to 100; 986 vidIQ credits, no
  USD). Not uploaded. Next: Luyanda reviews cut v2 and the pack, then uploads; the study embed once the YouTube ID exists.
- **The Waters Recede** (Genesis 8:1 to 22), `films/genesis/10-the-waters-recede/`, episode 10: M0 draft 24 November
  2026, written to The Flood's standard with its cut v1 review lessons (`TREATMENT.md`). `script/movement.py`: 22 verses
  and 15 quotations verified, 19:11 estimated, 99 lines, the four questions at 0:17, title 0:32, first verse 0:35;
  God's speeches 8:16 to 17 and 8:21 to 22 split from the study JSON. Decisions D1 to D12 (the dove only a bird and no
  Jordan echo; the ark never seen from below; no rainbow; Babylon without its gods; open loop into The Covenant with
  Noah). C1 approved 25 November: 99 lines voiced (0.58 USD), 19:10 on the real voices (questions 0:15, title
  0:29, first verse 0:32, longest teaching run 56 s); `exports/movement-animatic.mp4` voices only. Cast all carried
  over from The Flood (`script/cast.md`, `exports/cast-sheet.jpg`), no new portraits. Cast locked 25 November;
  autopilot ran to cut v1 on 27 November:
  - 240 keyframes and 259 LTX clips.
  - Clip review in `edit/clip-review.md`: 13 redone, and s138 became the animals coming out after three miscounted household keyframes.
  - `exports/full-cut-v1.mp4`: 19:10, -16.2 LUFS, true peak -1.9 dBFS. Review copy `exports/full-cut-v1-review.mp4`.
  - Judgment calls in `edit/final-cut-notes.md`.
  - 22.67 USD in all.
  - Long LTX runs fill swap after a day or so and stall; restart the Mac between long renders.

  Luyanda's v1 review had 12 notes, all fixed in `exports/full-cut-v2.mp4`:
  - The voice track had been built before the timeline, which cut off two lines.
  - Cards are now timed to the spoken word (`edit/word_times.py`).
  - 4 clips were re-prompted and 6 keyframes remade.

  23.07 USD in all. Cut v2 approved 27 November. YouTube pack built (`edit/youtube_cut.py`, `edit/shorts_qa.py`,
  `edit/shorts_metadata.py`):
  - `exports/the-waters-recede-youtube.mp4` (19:31, -14.2 LUFS).
  - Eight cliffhanger Shorts.
  - `exports/youtube-pack.md`: title 99, Shorts titles 96 to 98, covers 98 to 100, main thumbnail 95 with an 88
    cast-true alternate.
  - 780 vidIQ credits, no USD. Not uploaded.

  Next: Luyanda uploads, then the study embed once the YouTube ID exists. The cut review method is now in `films/AUTOPILOT.md`. An older
  movement's fixes go first in the LTX queue.
- **The Covenant with Noah** (Genesis 9:1 to 17), `films/genesis/11-the-covenant-with-noah/`, episode 11: M0 draft 25
  November 2026 (`TREATMENT.md`). `script/movement.py`: 17 verses and every quotation verified, 19:11 estimated, 102
  lines, the four questions at 0:14, title 0:33, first verse 0:36, longest teaching run 50 s; God's speeches split
  from the study JSON. Decisions D1 to D11 (the rainbow as weather; the war bow only as a prop, its direction a
  reading; the first rain is our scene; blood without gore; the king's stone without gods; open loop into Noah's
  Sons). C1 approved 25 November 2026: voiced (0.48 USD), 19:11 on the real voices (questions 0:14, title 0:32,
  first verse 0:34, longest run 49 s), voices only animatic built. Cast carried over from The Waters Recede
  (`exports/cast-sheet.jpg`), no new portraits. Cast approved 25 November; autopilot: world bible done (11 new
  masters, 1.61 USD; 2.09 USD spent in all), storyboard 267 shots (248 keyframes). Keyframes done and reviewed
  27 November (75 redone; see `edit/keyframe-review.md`), about 23.87 USD spent in all. LTX rendering under the
  battery rule (249 clips). The 25 USD checkpoint is close: the sound effects (about 0.20 USD) are the only paid
  step left in the plan.
- **Noah's Sons** (Genesis 9:18 to 29), `films/genesis/12-noahs-sons/`, episode 12: M0 draft 27 November 2026
  (`TREATMENT.md`). `script/movement.py`: 12 verses and every quotation verified, 19:20 estimated, 107 lines, the
  four questions at 0:17, title 0:35, first verse 0:38, longest teaching run 50 s. Noah's oracle (9:25 to 27) read by
  the READER (`SPEAKERS`); the GOD voice only for five words of God quoted from elsewhere. Decisions D1 to D11
  (Noah's nakedness never shown; Ham's sin as the text tells it; one family, one skin, and the "curse of Ham" named
  as a lie; Canaan as a boy from behind; wine without comedy; Christ from straight behind; open loop into The Table
  of Nations). C1 approved 27 November 2026: voiced (0.35 USD), 19:47 on the real voices (questions 0:17, title
  0:35, first verse 0:38, longest teaching run 50 s), animatic built, cast carried over (sheet
  `exports/cast-sheet.jpg`). Waiting for the cast stop; LTX waits behind The Covenant with Noah's clips.

## Rules (from Luyanda, never bend)

1. No em dashes or en dashes anywhere.
2. Scripture is verbatim BSB from the study JSON; never paraphrase; never add to God's words.
3. Never depict God or the face of Christ; God only by effect (light, wind, water, a voice);
   the Spirit is wind, never a figure or a dove; never invent a scene the text does not give.
4. Banned prompt words: deity, god figure, divine being, halo, glowing man, angel, temple, idol.
5. API keys only from the macOS Keychain (`makor-gemini`, `makor-elevenlabs`); never print,
   write or commit them.
6. Look up current docs before using a model or endpoint.
7. Log every paid call in the film's `COSTS-movement.md`; respect the cap; checkpoint with
   Luyanda at every 25 USD.
8. Never upload or publish. Never push: give Luyanda a commit block (see CLAUDE.md).
9. Work in checkpoints: Luyanda approves the script (C1), the cast, and the final cut. From cast approval to the
   final cut Claude runs every step, reviews and fixes on its own (`films/AUTOPILOT.md`, 14 November 2026); only
   the 25 USD money checkpoint stops it.

## Decisions that hold for every film

- Voices (`films/VOICES.md`): READER (ElevenLabs `pRrdgJxlE0SsVTIYEjli`) reads all Scripture;
  GOD (`bItqJOjNBHK6rbwcdlOT`) only God's direct speech in the passage (plus Revelation 21:5);
  GUIDE (Kokoro `am_michael`) everything that is not Scripture. Human speakers in the text are
  read by the READER. Words of Jesus are READER quotations.
- People: photoreal and cast from The Garden on (`films/STYLE-BIBLE.md`, "Photoreal"); in The
  Seven Days, tiny distant painted figures.
- Format: 16:9 film for YouTube; vertical framed version for TikTok and Instagram; a GUIDE led
  one minute short for Reels, Shorts, TikTok and WhatsApp Status. Shorts that are not a whole
  movement are Scripture only.
- Fraunces (in `films/fonts/`) for the wordmark and titles.
- YouTube AI disclosure question: No for the painted Seven Days, Yes for photoreal films.
- Depth motion for every still shot; Veo Lite for calm shots, Fast for creatures, light,
  people and transitions; each model about 10 requests a day.

## The pipeline (all in `films/tools/`)

| Step | Tool |
|---|---|
| Script from study JSON (verifies every verse) | `movement_script.py` (a film's `script/movement.py` defines CHAPTERS) |
| Voices and voice track | `movement_voice.py` (run with `makor-audio/.venv/bin/python`), `voice_track.py` |
| Animatic and shot timings | `animatic.py` |
| World bible, shot list | film's `script/world_bible.py`, `script/shotlist.py` |
| Keyframes (half price) | `still_batch.py` (Gemini Batch API) or `still.py` |
| Veo clips | `movement_clips.py` (`--model lite` for Lite) |
| Depth motion | `depth_move.py` (called by the edit when film.json has "depth": true) |
| Sound effects | `movement_sfx.py` (reads the film's `sfx-cues.json`) |
| Edit | `movement_edit.py FILM segments audio final` (reads the film's `film.json`) |
| YouTube, vertical, artwork | `platform_versions.py FILM art youtube vertical` |
| Review sheets | `sheet.py`, `strip.sh` |

Each film's `film.json` holds its title, study address, act scores (with start offsets), sound
placements, thumbnails and end screen settings.

## Lessons (save money and time)

- Lock timing with voices and an animatic before paying for pictures.
- Veo dramatises: breaking surf, sun glints, light from a point, scene changes. Trim to the clean
  seconds or dissolve between keyframes rather than rerolling blindly. Lite adds halos on lit
  shots.
- Check every keyframe sheet for rule breaks before animating; typical faults: people appearing
  before they exist, invented gates or buildings, dead trees, modern houses, repeated compositions.
- Captions need the ink band to read on gold and cream.
- **Consistency (Cain and Abel, 15 to 16 October 2026).** Make a world bible first: one master image per location
  (and a night version), costume turnarounds per character; every shot sends its location master and cast
  references. Check every cast keyframe face against the portrait before animating. Everyone wears ancient dress
  below the knee, never shorts (the brick-maker included); babies carry the parents' skin tone in the prompt.
- **LTX.** Hold the framing on people; never pin the last frame to the keyframe (LTX cuts away to another person
  in between). Score clips against their keyframes (`04-cain-and-abel/edit/clip_score.py`, `face_trims.py`).
- **Flow.** Build scenes as continuous takes (`TAKES` in the storyboard, `edit/takes.py` extends from the last
  frame, `full_cut.py` plays a take with no cut); no shot may play as a still. Luyanda reviews by timestamp.
- **The sin at the door (Genesis 4:7)** is only two eyes in the dark, never the form of a lion (Jesus is the Lion
  of Judah).
- **Batch keyframes in jobs of 40** (`still_batch.py --per-job`): a 138 image job could not be fetched (503).
  Long renders follow the battery rule: `tools/battery_render.sh FILM 10 80`.
