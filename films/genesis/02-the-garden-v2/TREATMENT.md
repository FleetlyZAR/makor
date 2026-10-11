# The Garden v2: treatment and story arc (DRAFT for C1)

Luyanda, 11 October 2026: begin The Garden "in a similar epic way as The Seven Days", starting
with the story arc and the script. Built to `films/CINEMA-STANDARD.md` and the method of
`../01-the-seven-days/V2-TREATMENT.md`. v1 (`../02-the-garden/`) stays untouched and reproducible.

**Script:** `script/movement.py` (edit that), readable in `script/movement-script.md`. All 22
verses read once, in order, verbatim BSB (the generator checks it). Estimated **15:40** at the
v2 voice pace (v1 ran 10:38); the rendered voices decide the real length.

## The shape

The Seven Days v2 ends: "Genesis one is the wide shot. In chapter two, the camera comes down
to the ground, to the dust, and to a garden." The Garden v2 opens exactly there.

1. **Cold open (flash-forward):** the fall from sky to a single grain of dust; silence; wind
   lifts the dust; Adam's eye opens on his first breath. A one second a shot montage of the
   film's peaks, then on black, God: "It is not good for the man to be alone." Cut to the
   brick-maker, free now, watching the tabernacle at night. Hook: seven goods, then a not
   good; and this garden looks like a sanctuary. Title.
2. **Down to the ground (2:4):** the hinge of the verse; the covenant name; God's nine verbs on
   screen (forms, breathes, plants, takes, places, commands, brings, closes, builds).
3. **Dust and breath (2:5 to 7), SET PIECE 1, the breath:** lack, springs, the forming by
   effect only, the breath, 14 s with no narration. Then the brick-maker's hands in dust;
   the potter's verb; other nations' clay men made as servants, this one given a garden and
   God's breath; adam and adamah.
4. **A garden in the east (2:8 to 9):** time-lapse growth to the two trees.
5. **Four rivers (2:10 to 14), SET PIECE 2, the river:** a speeding river shot that breaks into
   four; each river named on screen; 12 s with no narration. Real geography beyond reach;
   water flowing from where God dwells.
6. **A garden like a sanctuary (the turn):** the camp's sanctuary at sunrise: gate facing east,
   gold, the onyx stones on the priest's shoulders, cherubim among palms. Leviticus 26:12.
   "Israel's worship was, in part, a memory of Eden."
7. **To cultivate and keep (2:15):** match cut from Adam tending the garden to a Levite at the
   gate. Abad and shamar. Ends on the question the next scene answers: a keeper needs a word.
8. **One word (2:16 to 17):** the tree, the voice as wind only, held silence after the warning.
   Permission first, one limit, a truthful warning, trust.
9. **Not good (2:18 to 20):** the payoff of the cold open line. Ezer and Psalm 121:2. A
   driving animal montage for the naming, ending on the man alone and the music stopping.
10. **Bone of my bones (2:21 to 23), SET PIECE 3, the woman brought to the man:** night, deep
    sleep, the builder's verbs; morning, she is brought to him, face to face, 14 s with no
    narration, the warmest peak; then his poem in silence.
11. **One flesh (2:24 to 25):** the brick-maker and his wife at their tent; dabaq, "Hold fast to
    Him"; the chapter shapes Israel's homes. Naked and not ashamed; wind stirs the grass at
    the foot of the tree and the music turns.
12. **The last Adam:** 1 Corinthians 15:45; the gardens of John's passion; the empty tomb
    in a garden at sunrise with the same wind as in Eden (8 s, no narration); "Receive the
    Holy Spirit" answers the breath; Ephesians 5:32.
13. **Eden restored, SET PIECE 4:** a fast dark flash-forward to chapter three; the brick-maker
    looking over the desert and Isaiah 51:3 (wilderness like Eden); the city with the river and
    the tree of life on both banks, 10 s with no narration.
14. **Dust that breathes (close and open loop):** dust, breath, light; the study's question;
    something moves in the grass under the tree; "another voice speaks in the garden" into
    The Fall.

## Approved (Luyanda, 11 October 2026)

C1 passed: arc and script approved, keep the brick-maker (D1). Voices rendered the same day at
the v2 pace (`film.json`): 80 lines, 3,174 ElevenLabs credits (0.53 USD), runtime **15:21**,
`audio/movement/voice-track.wav` (and `.m4a` for listening). Voices approved. Animatic the same
day: `exports/movement-animatic.mp4` (15:21, 131 draft shots of about 7 s, temp music). Pacing
notes: voice 83% of the film; longest teaching run 56 s (One word, 7:19); 46 s of teaching
right after the title (Down to the ground). Next: cast the brick-maker's wife, then
`script/storyboard.py` with set piece cuts of 2 to 4 s.

**Temp score (11 October 2026).** Luyanda found the animatic's music sleepy (one looped track
ducked flat). `edit/score_mix.py` now scores it the Seven Days v2 way: 17 cues placed per turn,
crests landed on the four set pieces, hard drops for God's lines and the man alone, a hit on
every chapter card, the breath as a recurring sound (open, set piece, tomb, close), ambience beds,
multiband ducking, -16.1 LUFS with 7.7 LU of range. Set pieces sit 6 to 7 LU above the teaching.
Music is TEMP, borrowed from The Seven Days v2 library (mostly its unused Epidemic picks); The
Garden's own cues come from the cue sheet below. `exports/movement-animatic-scored.mp4`.
Also added the 2 s pause on the tree in One word (runtime 15:23).

**11 October 2026, later.** Wife: B chosen (`stills/cast/wife.jpg`, turnaround done). Music: the first
pick per cue on `script/music-audition.html`, 16 Epidemic tracks downloaded with stems (Luyanda confirmed
Epidemic's licence check), filed by `edit/file_music.py` as `audio/music/g-NN*.wav`. Storyboard
(`script/storyboard.py`): 197 shots, 122 reused from v1, The Fall and The Seven Days v2, 73 new keyframes
(batch, then 17 rerolls for modern sleeves, a watch, panels, seams, a wall, a bridge, figures in the
cherubim weave). LTX animating the 49 reused shots marked anim. Spend 8.31 USD. C2: new keyframes in
`edit/review/C2-keyframes-*.jpg`, waiting for Luyanda before they are animated.

## Decisions for Luyanda (as proposed)

- **D1, the human strand.** Continue the brick-maker from The Seven Days v2 (his cast portrait
  and turnaround already exist), now free in the wilderness camp around the tabernacle, so the
  series has one first hearer. He pays off at the sanctuary turn, at the potter's verb (his
  hands in dust), at one flesh (with his wife) and at Isaiah 51:3. Needs his wife cast, and a
  priest and a Levite as background figures (no close faces). **Fallback:** the sanctuary
  scenes as objects and places only.
- **D2, the tabernacle on screen.** The study ties Eden to the tabernacle (east gate, gold,
  onyx stones on the high priest's shoulders, cherubim among palms). Shown as the camp's tent
  sanctuary, never with any figure of God. Prompts say "tent sanctuary", never the banned
  word.
- **D3, Adam and Eve framing.** Unclothed before 3:7: faces, shoulders, long hair and foliage
  only; every LTX shot checked at full size; refused shots fall back to depth motion.
- **D4, new GUIDE lines** (marked "new in v2" in `movement.py`, each with its study field):
  the cold open hook, the clay men of the nations, water from where God dwells, the sanctuary
  turn and Leviticus 26:12, "a keeper needs a word", Deuteronomy 10:20, Isaiah 51:3, and the
  open loop into The Fall (the one line not from the study, flagged as v2's was).
- **D5, length.** 15:40 estimated. If that is too long, the first cuts are the knowledge of good
  and evil line (v1 m035) and the two closing GUIDE lines of The last Adam.

## Cue sheet (Epidemic Sound, plus Suno for the series themes)

| Cue | Sequence | Feel |
|---|---|---|
| 1 | Cold open fall and breath | wind rush to silence, a single warm swell on the breath |
| 2 | Montage and title | driving, then cut dead for God's line |
| 3 | Down to the ground | low curious pulse, soft hits for the verbs |
| 4 | The breath (set piece) | near silence building to an immense warm crest |
| 5 | A garden in the east | growth, rising strings, time-lapse whooshes |
| 6 | Four rivers (set piece) | speed and scale, the second peak |
| 7 | The sanctuary | ancient, reverent, frame drum and low strings |
| 8 | One word | one sustained tone; silence after the warning |
| 9 | Not good and the naming | lonely piano into a driving animal montage, stops dead |
| 10 | Bone of my bones (set piece) | night stillness to the warmest peak in the film |
| 11 | One flesh | tender, then a darker turn on the tree |
| 12 | The last Adam | reverent build to the empty tomb |
| 13 | Eden restored (set piece) | dark flash, then radiant swell |
| 14 | Close and open loop | quiet resolution, then a low unresolved note |

Sound design: wind rush and whooshes on the fall; dust grains; the breath (the same breath
returns at the empty tomb and at the close); springs ticking into dust; water and rapids for the
rivers; fire and cloth for the camp; leaves under wind for God's voice; animal calls and
wingbeats; night insects; a low hit on every chapter card.

## Build order after approval

1. Lock `script/movement.py`; `film.json` with the v2 voice speeds.
2. Voices (GUIDE free; READER and GOD credits), then the animatic, then pacing check.
3. Cast the brick-maker's wife; storyboard (`script/storyboard.py`) and keyframes, reusing v1's
   photoreal garden world bible and Adam and Eve.
4. Music and sound from the cue sheet; animate (LTX first, Omni and Veo for hero shots).
5. Edit with the cinema mix, the pre-delivery audit, then the YouTube pack and thumbnails.
