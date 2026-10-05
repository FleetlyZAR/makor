# Makor films: voices

The voices every Makor story film uses. Change them here on purpose, never shot
by shot.

## GOD

- ElevenLabs voice id: `bItqJOjNBHK6rbwcdlOT` (account name "Makor GOD candidate 1")
- Made with Voice Design (`eleven_ttv_v3`) from the brief: "deep, warm, resonant
  male voice, slow and completely unhurried, authority without volume, never
  shouting, clearly different from an American documentary narrator".
- Rendered with `eleven_multilingual_v2`, speed 0.85, mp3_44100_192.
- Rules: speaks only God's own words, verbatim BSB. One voice, never layered,
  never doubled, no reverb tails that turn it into a choir.
- Chosen by Luyanda, 5 October 2026 (Day One pilot).

## NARRATOR

- ElevenLabs voice id: `pRrdgJxlE0SsVTIYEjli` (account name "Makor GOD candidate 2")
- Made in the same Voice Design call as GOD, from the same brief.
- Rendered with `eleven_multilingual_v2`, speed 1.0, mp3_44100_192.
- Chosen by Luyanda, 5 October 2026, in place of the site narrator (Kokoro
  `am_michael`). The Kokoro renders are kept in
  `audio/narrator/kokoro-am_michael/` for comparison.

## Unused candidates

- Candidate 3: `gXRVasxNiidjr0w3Ljuw`. Still saved in the ElevenLabs account;
  delete only with Luyanda's approval.

## Tooling

`films/tools/voice.py final <film>` renders every line in the script's line list
with the voices above. Credits are logged in the film's COSTS.md.
