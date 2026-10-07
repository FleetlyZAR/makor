# Scoring method (from The Garden on)

Agreed direction, 7 October 2026: momentum and contrast, not hype. The Seven Days score
(sparse, no pulse, written for creation) stays with The Seven Days. Every film from The
Garden on gets its own score, in the same room so the series sounds like one work.

Why: measured on The Garden and The Fall, the voice runs through 90 to 92% of the film,
the score sat about 21 dB under it (inaudible on a phone), and the borrowed tracks have
about one note event a second and no pulse. See the A/B in
`genesis/03-the-fall/edit/ab-music/`.

## The series sound (every film)

- **The room**: solo cello, low strings, soft felt piano, warm analog pad. The Seven
  Days instruments, so the films belong together.
- **New: a pulse.** A slow heartbeat under most cues, 60 to 72 BPM: low pizzicato, muted
  repeated piano, or a soft frame drum. Felt more than heard. It moves time forward
  without excitement.
- **One colour per film**, from the ancient Near East and used sparingly: ney flute and
  harp for The Garden; duduk and frame drum for The Fall.
- **A theme for the promise.** A short rising line (cello, then horn) that belongs to the
  seed of the woman. It is born in The Fall at Genesis 3:15 and can return in later films
  whenever the promise moves forward.
- **Never**: vocals, choir, chanting, trailer hits, drum kit, snare, hi-hat, electronic
  beats, synth arpeggios, guitar.

## Scoring the story

- **Contrast keeps people awake, not volume.** Drop the score out before the lines that
  matter most and let it come back after them.
- **One cue per act**, changing colour at each turn of the story. Swells are cut to land on
  the verse (offsets in `film.json` acts).
- **Breaths**: 1 to 2 s of score alone at chapter turns and after key lines (added in
  the voice timeline).
- **Silence under God's voice** stays (the edit's existing dip).

## Mix targets (from the A/B)

- Score and effects about **15 dB under the voice** while it speaks (the edit used about
  21). Settings that measured 15.2 dB on The Fall: music level 0.5, sidechain ratio 5,
  threshold 0.03 (`tools/movement_edit.py`, `build_audio`).
- Master at -14 LUFS as now.

## Making the music (Suno)

Each film has `script/suno-score.md` with one prompt per cue. Mode Custom, Instrumental
on; give an existing Makor track as the reference where Suno allows it so the room matches.
Aim a little long; cuts, loops and crossfades happen in the edit. Drop WAVs in the film's
`audio/music/` named as the sheet says.
