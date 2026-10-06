# Makor films: handoff (6 October 2026)

Read this first in any new session working on Makor films.

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
  - Still to do after the clips: review the task's flags, trim bad clips (`clip:A-B` flag in
    `script/shotlist.py`), rebuild, then the YouTube and vertical versions, artwork, one minute
    short (copy and adapt `01-the-seven-days/edit/short.py`) and publishing packs. Then disable
    the scheduled task.
- Next film after that: movement 3, The Fall (Genesis 3:1 to 24), see `GENESIS-SECTION-MAP.md`.

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
9. Work in checkpoints: show results and wait for approval before the next paid step.

## Decisions that hold for every film

- Voices (`films/VOICES.md`): READER (ElevenLabs `pRrdgJxlE0SsVTIYEjli`) reads all Scripture;
  GOD (`bItqJOjNBHK6rbwcdlOT`) only God's direct speech in the passage (plus Revelation 21:5);
  GUIDE (Kokoro `am_michael`) everything that is not Scripture. Human speakers in the text are
  read by the READER. Words of Jesus are READER quotations.
- People only as tiny distant figures, from behind or in profile, no body, clothing or face
  detail (`films/STYLE-BIBLE.md`).
- Format: 16:9 film for YouTube; vertical framed version for TikTok and Instagram; a GUIDE led
  one minute short for Reels, Shorts, TikTok and WhatsApp Status. Shorts that are not a whole
  movement are Scripture only.
- Fraunces (in `films/fonts/`) for the wordmark and titles.
- YouTube AI disclosure question: answer No for this painted style.
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
