# Cinema standard: what the best YouTube documentaries do, and what we change

Studied 7 October 2026, at Luyanda's request ("each film like a movie; where there's an epic it
must be more epic than calming"). References:

- **fern**, "How Meth Is Killing Europe" (30:12, 3.5M views); channel averages 5 to 20M per film.
- **Veritasium**, "The Insane Real Engineering of the Nazi Enigma Machine" (47:42, 16.9M views).

Sources: video metadata and transcripts, and a scene by scene sound and pacing walkthrough of
each, all through vidIQ. The walkthrough's dB and words per minute figures are the analyser's
estimates, not measurements; the cue lists, silences, structure and music credits are reliable.

## What they do

| | fern (30 min) | Veritasium (47 min) | Makor now (11 to 15 min) |
|---|---|---|---|
| Music tracks | **42 credited** (Epidemic Sound, Lens Distortions), several as stems: "No Percussion", "Underscore", "Less Percussion" | 18 cues plus an orchestral classic (Epidemic Sound) | 5 to 6 cues, all borrowed from The Seven Days |
| New music every | about 43 s | about 2.5 min, with sub-changes | about 2 min |
| Music above the voice | only in montages with no narration | only in montage transitions and battle reels | never; voice runs 90 to 92% of the film |
| Silence | before key lines, on emotional breaks, a black frame "30 minutes later" | before punchlines, under the real machine's roar | three 4 s beats per film |
| Sound design | sub-bass hit on every chapter card, whooshes on 3D moves, object foley (glass, needle, heartbeat, rain) | sub booms on chapter breaks and scale jumps, mechanical foley, paper, ticking | ambience beds only; no hits, no whooshes, no object foley |
| Cold open | **flash-forward**: the most intense testimony from deep in the film, then title at 2:14 | **hands-on hook**: the real object, a demo, a question | one GUIDE line over a landscape (Garden now asks a question) |
| Structure | three strands woven (person, expert, data), switching every 2.5 to 3 min | acts of discovery with a host trying and failing; cliffhanger end | verse, then commentary, every 20 to 40 s, in order |
| Shot length | 1.5 to 3 s in montages, 5 to 8 s in testimony | 2.8 to 4.2 s in explanation, 6 to 12 s in interviews | 6.8 to 7.2 s throughout |
| Narration | measured, ~130 wpm, real pauses | 145 to 160 wpm, drops lower for gravity | GUIDE 157, READER **194 to 197**, GOD 143 to 179 wpm |
| Peak | a built crescendo, then total dropout at the breaking point | music strips away for the machine's roar, then an orchestral surge | swells under narration, about 21 dB down |

## The Makor standard (every film from The Fall on, then back to The Garden)

1. **Cold open = the film's most powerful moment first.** A 30 to 60 s flash-forward cut
   from the climax (for The Fall: God's voice, "Where are you?", the flaming sword at the gate),
   then the question, then the title. No teaching before the title.
2. **Two or three epic set pieces per film, with no narration.** 15 to 40 s where picture,
   score and sound carry the story and the music is allowed to go above where the voice was:
   The Fall: the eating; driven out past the cherubim; the seed of the woman to the empty tomb.
   The Garden: the breath into the man; the river and the four heads; the woman brought to him;
   Eden restored. Each is built to (a rise), held, and released into silence.
3. **Let Scripture play as drama, teach in blocks.** Run a whole scene of verses as one
   dramatised sequence (READER and GOD, picture, score, sound), then one GUIDE block that
   explains it, then the next scene. Switch strand every 2 to 3 minutes; end each block on a
   question the next scene answers.
4. **A new cue for every turn: 10 to 15 cues in a 12 to 15 minute film**, each chosen for its
   scene, with stems so the busy parts drop out under the voice.
5. **Sound design pass on every film**: a low hit on each chapter card; whooshes on big camera
   moves and transitions; object foley on what we show (fruit torn, leaves, footsteps in the
   garden, fire of the sword, wind of the Spirit, breath); silence before the key line of each
   chapter.
6. **Narration slower and with room**: READER and GOD about 150 wpm, GUIDE about 140, with a
   held beat after every key line (breaths, `SCORING.md`).
7. **Faster cutting in montage**: 2 to 4 s shots in set pieces; 6 to 8 s holds stay for
   teaching. More shots per set piece rather than longer clips.
8. **Mix**: the multiband method (`SCORING.md`, version C) under narration; in set pieces the
   music is the lead. Master at about -16 LUFS with 6 LU or more of range (measured below).
9. **End on an open loop** into the next film ("Next: Cain and Abel...") as Veritasium ends
   on the Lorenz cipher.

## Measured mixes (7 October 2026)

Audio of both references downloaded with Luyanda's approval and measured against our live
The Seven Days (`ebur128` loudness, 1 s short-term windows, band levels relative to the whole):

| | Integrated | Loudness range | Loudest 2% above median | Sub <80 Hz | Air >6 kHz |
|---|---|---|---|---|---|
| fern | -17.9 LUFS | 4.7 LU | +2.6 LU | -13.5 | -12.5 |
| Veritasium | -15.4 LUFS | 6.2 LU | +3.1 LU | -20.1 | -15.4 |
| Makor v1 | -14.0 LUFS | 3.4 LU | +1.6 LU | -9.6 | -14.3 |

Our mix is louder, flatter and darker: little difference between quiet and epic, a constant
sub drone, less air. Targets from v2 on: **master at about -16 LUFS integrated, loudness range
6 LU or more, true peak -1 dBTP**, so the set pieces can rise well above the narration; keep
sub-bass for hits and set pieces, not as a constant bed; let the score carry air (strings,
shimmer) on top.

## Music sourcing

Both channels score from production libraries with stems (Epidemic Sound; fern also Lens
Distortions), not from one composer. Ten to fifteen cues per film is heavy for Suno alone.
Recommended: **Epidemic Sound for underscore and the sound effects library** (stems, cleared
for YouTube, the hits and whooshes in point 5), and **Suno for the signature themes** (the
promise theme and each film's colour) where a library cannot give us our own melody.

## Animation rules (set by the pilot, 8 October 2026)

From the first Veo Standard clips of The Seven Days v2 (the drop s002, the burst s003):

1. **Veo 3.1 Standard for hero shots** (set pieces, the cold open, cast close ups); Fast for
   teaching cover; Lite for calm landscapes. Our Gemini quota allows only about two Standard
   clips a day, so hero shots are planned first and spread over days.
2. **Every animation prompt carries the whole scene**, the motion, the shared photoreal motion
   wording (`photoreal.MOTION`) and, for cast, the keep-the-face line. Motion alone drifts.
3. **Describe light as rays, a flood or a wave, never a sphere, disc or orb**: the burst grew a
   disc that read as the sun (Genesis gives the sun on Day Four), and had to be cut around.
4. **Review every clip frame by frame before use** and record the usable range in the edit's trim
   list (`edit/preview_cut.py`, CLIP_TRIMS); Veo's 8 s clips usually hold 2 to 4 good seconds.
5. **Cut on sound**: hard cuts land on hits (the boom at the burst); slow motion stretches a
   usable range to fill a shot (the burst: 2 s of clip across 4 s).
6. **Montage shots under 1.2 s** move faster (a stronger push in) so they read as alive even as
   stills; set pieces and cast shots get real motion.
7. **No other animator is connected.** Runway, Kling, Luma or Sora would need a new account and a
   connector; Gemini Omni Flash (`omni_clip.py`, 720p) is a cheaper fallback for non hero shots.
8. **vidIQ (connected) animates without our Google limit**, text to video only in practice (its
   start frame must be passed inline as base64, which is not workable from here). Use it for
   shots with no cast: the Big Bang, the earth, clouds, aerials. Cost: Veo 3.1 Standard 640
   credits and Fast 240 credits per 8 s clip at 1080p (plan: 2,000 a month). Fast held up well
   for the earth zoom.
9. **Name the geography** in any shot of the earth: Veo turned the earth to show North America;
   ask for "Africa, Arabia and the Mediterranean facing the camera, the Tigris and Euphrates at
   the centre" and still check every frame.
10. **One continuous move per clip, cut across shots**: one 8 s clip can serve two or three
   storyboard shots (the earth zoom covers s004 and s005), which halves the cost.
