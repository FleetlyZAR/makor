# The Garden: Suno prompts for the score

Method and series sound: `films/SCORING.md`. Six cues, one per act, replacing the borrowed
Seven Days tracks (the older four-act draft in `suno-movement.md` is superseded). Times are
from the current voice track (10:38, with the new cold open) and may move a few seconds when
breaths are added; aim for the length shown or a little longer and I cut to fit.

Drop the WAVs into `films/genesis/02-the-garden/audio/music/` as `garden-1.wav` to `garden-6.wav`.

For every cue:

- Mode: Custom. Instrumental: on.
- Reference ("Cover" or "Use as inspiration", if your Suno has it): The Seven Days
  `act2.wav` ("Forming"), so the room and instruments match the series.
- Exclude styles:

```
vocals, choir, chanting, epic trailer hits, drum kit, snare, hi-hat, electronic beat, synth arpeggio, guitar, orchestral hits
```

The voice carries the film: leave the speech range open, no busy melodies, long arcs.
The Garden's colour is **ney flute and harp**, used sparingly.

---

## Cue 1: Dust and breath (0:00 to 2:26, aim 2:40)

Cold open (the question), from the heavens to the ground, dry earth with no plant and no man.
Key moment: Genesis 2:7 at 1:42, God breathes into the man: the cue's one warm bloom.

Title: `Makor The Garden 1 Dust and Breath`

Style:
```
cinematic underscore, low strings and soft felt piano, warm pad, slow heartbeat pulse of low pizzicato at 64 bpm, dry and waiting, earthy, then one warm major bloom like a first breath, restrained, no drums, no vocals
```

Lyrics box:
```
[Instrumental]
[Intro]
[a question in the strings, descending from high to low]
[Verse]
[low pizzicato pulse, dry earth, waiting, something missing]
[Build]
[slow gentle rise, harmony warming]
[Swell]
[a single warm major bloom, breath, life]
[Outro]
[settles, alive and calm]
[End]
```

## Cue 2: A garden in Eden (2:26 to 4:08, aim 1:55)

Trees good for food, the two trees at the centre, the river dividing into four. Delight. The
garden as a sanctuary.

Title: `Makor The Garden 2 A Garden in Eden`

Style:
```
cinematic underscore, flowing harp and soft ney flute over warm strings, gentle moving pulse at 68 bpm like running water, wonder and delight, morning light, sacred and spacious, restrained, no drums, no vocals
```

Lyrics box:
```
[Instrumental]
[Intro]
[harp ripples like water, morning]
[Verse]
[ney flute melody, warm strings, delight]
[Verse]
[flowing pulse, rivers dividing, wide and spacious]
[Bridge]
[a hushed sacred moment, held chords]
[Outro]
[flowing on, calm]
[End]
```

## Cue 3: To cultivate and keep (4:08 to 5:34, aim 1:40)

Work as worship; the priestly verbs. Then the command at 4:41 (God's voice: the score dips
for it, done in the mix): after it, a first faint shadow.

Title: `Makor The Garden 3 Cultivate and Keep`

Style:
```
cinematic underscore, steady working pulse of muted piano and low pizzicato at 66 bpm, cello melody, purposeful and dignified, then a quiet pause and a faint minor shadow, restrained, no drums, no vocals
```

Lyrics box:
```
[Instrumental]
[Intro]
[steady pulse, purposeful]
[Verse]
[cello melody, work and service, dignity]
[Break]
[pause, near silence]
[Verse]
[the pulse returns, a faint minor shadow, a boundary set]
[Outro]
[settles, thoughtful]
[End]
```

## Cue 4: Not good to be alone (5:34 to 6:47, aim 1:20)

"It is not good for the man to be alone" (God's voice at 5:36). The animals named; no match
found. Longing.

Title: `Makor The Garden 4 Alone`

Style:
```
sparse cinematic ambient, solo cello and distant ney flute, soft pad, slow and searching, longing and incompleteness, gentle pizzicato steps, no drums, no vocals
```

Lyrics box:
```
[Instrumental]
[Intro]
[a solo cello line, alone]
[Verse]
[gentle pizzicato steps, one after another, searching]
[Verse]
[ney flute far off, longing, nothing quite fits]
[Outro]
[hangs open, waiting]
[End]
```

## Cue 5: Bone of my bones (6:47 to 8:23, aim 1:45)

The deep sleep (hush), God builds the woman and brings her. "This is now bone of my bones" at
7:22 is the bloom of the film: joy, restrained. Then "naked, and not ashamed" at 8:08: peace,
with the faintest hint of what is coming.

Title: `Makor The Garden 5 Bone of My Bones`

Style:
```
cinematic score, hushed felt piano and soft pad like deep sleep, slow build with warm strings and harp, then a joyful warm bloom with cello and horn, tender and radiant, restrained, settles to peace with one faint unresolved note, no drums, no vocals
```

Lyrics box:
```
[Instrumental]
[Intro]
[hush, deep sleep, soft piano]
[Build]
[strings and harp gather, something being made]
[Swell]
[a warm joyful bloom, cello and horn, meeting]
[Verse]
[peace, gentle, two together]
[Outro]
[a quiet chord with one faint unresolved note]
[End]
```

## Cue 6: The last Adam and Eden restored (8:23 to 10:38, aim 2:30)

Paul's last Adam; gardens at the passion; breath on the disciples. Then Eden restored and
surpassed (Revelation, about 9:30 to 10:00): the cue's full swell. Then "dust that breathes"
and the closing question: quiet resolution.

Title: `Makor The Garden 6 Eden Restored`

Style:
```
cinematic score, warm strings and french horn, felt piano, steady hopeful pulse at 68 bpm, builds patiently to a full radiant swell, then settles to a quiet resolved chord, reverent and hopeful, no choir, no vocals, no drum kit
```

Lyrics box:
```
[Instrumental]
[Intro]
[soft pulse, a cello line, hope beginning]
[Verse]
[strings join, steady, purposeful]
[Build]
[patient rise, horn enters]
[Swell]
[full radiant swell, a garden become a city]
[Outro]
[settles to quiet peace, a resolved chord]
[End]
```

---

## After the cues land

Acts in `film.json` become `garden-1.wav` (Cold open), `garden-2.wav` (A garden in Eden),
`garden-3.wav` (To cultivate and keep), `garden-4.wav` (Not good to be alone), `garden-5.wav`
(Bone of my bones), `garden-6.wav` (The last Adam). I set offsets so the breath lands on 2:7,
the bloom on 2:23 and the swell on Eden restored, add the breaths, apply the mix targets, and
send an A/B of the full film before it replaces the cut.
