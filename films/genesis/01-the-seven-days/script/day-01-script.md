# Day One: script and shot list

Film: Makor story film 01, Genesis 1:1 to 2:3, The Seven Days, Day One movement
Passage: Genesis 1:1 to 5 (BSB, verbatim from `src/content/studies/genesis/01-the-seven-days.json`, `text.units[0]`)
Format: 9:16, 1080 by 1920, 30 fps, target runtime 58.5 s (hard limit under 60 s)
Speakers: NARRATOR (Makor voice, Kokoro `am_michael`, speed 1.0) and GOD (one ElevenLabs designed voice, verbatim lines only)
Study URL: https://www.makor.co.za/genesis/the-seven-days/ (on screen as `makor.co.za/genesis/the-seven-days`)

## The one idea

God speaks, and darkness gives way to light and order. Everything else in the
film serves that one idea.

## Notes on the arc

1. **Verse order kept.** The brief puts "And God saw that the light was good" in
   the Verdict, after the separation and naming. In Genesis 1:4 the seeing comes
   first: "And God saw that the light was good, and He separated the light from
   the darkness." Splitting 1:4 and playing it out of order would reshape the
   verse, so verse 1:4 is read whole at the end of The word, and the Verdict
   becomes evening, morning, the first day (1:5b). Every verse plays once, in
   order, complete.
2. **"day" and "night"** are God's naming words in 1:5, inside the verse. The
   NARRATOR reads them as part of the verse. The GOD voice speaks only "Let there
   be light," so it lands once and alone. (Alternative if you prefer: GOD says
   "day" and "night" as single words. It makes the line choppy, so I do not
   recommend it.)
3. **The plain line from the study** is from `study.god`: "He separates and
   names, gives each thing its place and its role." Used verbatim.
4. **The open loop line** "But the waters still have no shape." is the brief's
   own line, NARRATOR, not Scripture.
5. Durations below are measured from a local Kokoro render of each line (free,
   offline). The GOD line is budgeted at 2.7 s for a slower designed voice.

## Script

Times are in seconds from the first frame. Captions show exactly what is spoken;
verse captions carry the BSB text exactly as in the JSON, curly quotes included.

### Hook, 0.0 to 6.0
Picture first: pure black, then the faintest dark swell of water surfaces out of it.
- 0.8 NARRATOR (Gen 1:1, 3.9 s): In the beginning God created the heavens and the earth.
- On screen, top: `Genesis 1` small, fades out at 4.0.

### World, 6.0 to 19.0
Picture first: the formless deep, then wind moving over its surface.
- 6.4 NARRATOR (Gen 1:2, 10.4 s): Now the earth was formless and void, and darkness was over the surface of the deep. And the Spirit of God was hovering over the surface of the waters.
- 17.4 NARRATOR (Gen 1:3a, 1.8 s): And God said,

### The word, 19.0 to 32.5
Picture first: total dark, held. Then light breaks across the deep.
- 19.8 GOD (Gen 1:3, about 2.7 s): Let there be light,
- 22.5 to 24.6 no voice. Light breaks along the horizon and races across the water. Music rises, soft swell.
- 24.6 NARRATOR (Gen 1:3b, 1.9 s): and there was light.
- 26.8 NARRATOR (Gen 1:4, 5.6 s): And God saw that the light was good, and He separated the light from the darkness.

### Turn, 32.5 to 46.0
Picture first: day and night side by side over the same water, then a calm, ordered deep.
- 33.0 NARRATOR (Gen 1:5a, 4.3 s): God called the light “day,” and the darkness He called “night.”
- 39.2 NARRATOR (study, 4.7 s): He separates and names, gives each thing its place and its role.

### Verdict, 46.0 to 52.5
Picture first: the light lowers into evening, then returns as morning.
- 46.5 NARRATOR (Gen 1:5b, 4.1 s): And there was evening, and there was morning, the first day.
- Music resolves under "the first day".

### Pull, 52.5 to 58.5
Picture first: pale light over waters that still run into waters, unshaped.
- 53.3 NARRATOR (brief, 2.6 s): But the waters still have no shape.
- 55.0 On screen: `Day Two` then `makor.co.za/genesis/the-seven-days` and the `Makor` wordmark text.
- 57.5 to 58.5 fade to black, near silence.

### Line list (one audio file per line)

| File                     | Speaker  | Text |
|--------------------------|----------|------|
| narrator/n01.wav         | NARRATOR | In the beginning God created the heavens and the earth. |
| narrator/n02.wav         | NARRATOR | Now the earth was formless and void, and darkness was over the surface of the deep. And the Spirit of God was hovering over the surface of the waters. |
| narrator/n03.wav         | NARRATOR | And God said, |
| god/g01-<voice>.wav      | GOD      | Let there be light, |
| narrator/n04.wav         | NARRATOR | and there was light. |
| narrator/n05.wav         | NARRATOR | And God saw that the light was good, and He separated the light from the darkness. |
| narrator/n06.wav         | NARRATOR | God called the light “day,” and the darkness He called “night.” |
| narrator/n07.wav         | NARRATOR | He separates and names, gives each thing its place and its role. |
| narrator/n08.wav         | NARRATOR | And there was evening, and there was morning, the first day. |
| narrator/n09.wav         | NARRATOR | But the waters still have no shape. |

## Shot list

Nine shots, 6.0 to 7.5 s each, 58.5 s total. Each clip is generated a little
long and trimmed in the edit. Every still prompt ends with the style suffix from
`films/STYLE-BIBLE.md`; every motion prompt ends with the motion suffix.

Style suffix (S), written out in full in each prompt below:

> Hand painted matte painting, painterly illustration with visible brush texture and soft canvas grain, reverent, still and quiet, soft diffused light, restrained palette of deep ink teal (#0E2A2E) shadows, water teal (#0F6C6C) midtones and warm muted gold (#B8862F) light, warm cream highlights, vertical 9:16 composition with calm empty space in the lower middle, no people, no figures, no faces, no silhouettes, no animals, no birds, no text, no lettering, no watermark, not photoreal, not cartoon, not 3D render.

Motion suffix (M):

> Painterly matte painting style preserved exactly, brush texture stays visible, slow and steady camera, no camera shake, no cuts, no people, no figures, no faces, no silhouettes, no birds, no text appears.

---

### Shot 1: The dark (0.0 to 6.0, 6.0 s)
- On screen: near black. A vast, still, dark water surface is barely visible in the lower third; above it, nothing.
- Camera: locked, imperceptible push in. Fade up from pure black over the first 2 s.
- Over it: n01 (Gen 1:1). Caption 1:1.
- Image prompt:
  > Almost total darkness over a vast, still, empty ocean at night with no light source anywhere. The lower third shows the faintest suggestion of slow, heavy swells, their crests catching a barely visible trace of cold dark teal; above the water there is only deep ink black emptiness with no horizon detail, no sky, no stars, no moon. Overwhelming stillness and emptiness, the world before anything. Hand painted matte painting, painterly illustration with visible brush texture and soft canvas grain, reverent, still and quiet, soft diffused light, restrained palette of deep ink teal (#0E2A2E) shadows, water teal (#0F6C6C) midtones and warm muted gold (#B8862F) light, warm cream highlights, vertical 9:16 composition with calm empty space in the lower middle, no people, no figures, no faces, no silhouettes, no animals, no birds, no text, no lettering, no watermark, not photoreal, not cartoon, not 3D render.
- Motion prompt:
  > Locked camera with an extremely slow push in. The dark water heaves gently with slow, long, low swells that rise and fall in place. The water stays low and calm, no breaking waves, no whitecaps, no spray, no surf, no wave rises toward the camera. Everything stays cold, dim and dark teal: no light appears, no glints, no gold, no warm tones. Nothing else moves. Painterly matte painting style preserved exactly, brush texture stays visible, slow and steady camera, no camera shake, no cuts, no people, no figures, no faces, no silhouettes, no birds, no text appears.

### Shot 2: Formless and void (6.0 to 12.0, 6.0 s)
- On screen: the formless deep from just above the surface, heavy swells running to a horizon lost in darkness. No shore, no land.
- Camera: slow forward drift low over the swells.
- Over it: n02 first half (Gen 1:2a). Caption 1:2.
- Image prompt:
  > A formless, empty, dark ocean seen from just above its surface, heavy rolling swells stretching away to a horizon that dissolves into darkness, no shore, no land, no rocks, no sky detail, no clouds. Deep ink teal water fading to black, only the faintest cold, dim water teal sheen along the crests of the nearest swells. There is no light anywhere yet: no glow on the horizon, no bright crests, no warm tones, no gold, no haze or mist above the water, only cold darkness. The sense of a world not yet shaped and not yet filled. Hand painted matte painting, painterly illustration with visible brush texture and soft canvas grain, reverent, still and quiet, soft diffused light, restrained palette of deep ink teal (#0E2A2E) shadows, water teal (#0F6C6C) midtones and warm muted gold (#B8862F) light, warm cream highlights, vertical 9:16 composition with calm empty space in the lower middle, no people, no figures, no faces, no silhouettes, no animals, no birds, no text, no lettering, no watermark, not photoreal, not cartoon, not 3D render.
- Motion prompt:
  > Slow forward drift low over the dark swells, which roll slowly toward and under the camera. The horizon stays lost in darkness. The water stays low and calm, no breaking waves, no whitecaps, no spray, no surf, no wave rises toward the camera. Everything stays cold, dim and dark teal: no light appears, no glints, no gold, no warm tones. Painterly matte painting style preserved exactly, brush texture stays visible, slow and steady camera, no camera shake, no cuts, no people, no figures, no faces, no silhouettes, no birds, no text appears.

### Shot 3: Wind over the waters (12.0 to 19.0, 7.0 s)
- On screen: close and low over the deep. An unseen wind moves across the surface: a travelling band of fine ripples and lifted spray curving across the water. The wind itself is invisible.
- Camera: slow lateral track following the wind across the surface.
- Note: no light on the water yet; spray is cold teal, never gold.
- Edit: the clip brightens from about 3.4 s; use 0.0 to 3.3 s only, slowed with motion interpolation to fill 7.0 s, warm tones cooled in the grade.
- Over it: n02 second half (Gen 1:2b, "And the Spirit of God was hovering"), then n03 "And God said," at 17.4. Caption 1:2 continues, then 1:3 begins.
- Image prompt:
  > Low and close over a dark, still ocean, an invisible wind passing across the surface, shown only by a long curving band of fine ripples racing over the water and a thin veil of spray lifting and trailing behind it, the rest of the water calm and black. The spray and ripples are cold, dim water teal and grey, with no warm tones and no light falling on them, because no light exists yet. The wind is unseen and has no shape of its own, only its effect on the water. Darkness above with no sky detail, no clouds. Hand painted matte painting, painterly illustration with visible brush texture and soft canvas grain, reverent, still and quiet, soft diffused light, restrained palette of deep ink teal (#0E2A2E) shadows, water teal (#0F6C6C) midtones and warm muted gold (#B8862F) light, warm cream highlights, vertical 9:16 composition with calm empty space in the lower middle, no people, no figures, no faces, no silhouettes, no animals, no birds, no text, no lettering, no watermark, not photoreal, not cartoon, not 3D render.
- Motion prompt:
  > Slow lateral track across the water following the moving wind. The band of ripples travels steadily across the dark surface, fine spray lifts and drifts and settles behind it, and the water behind slowly calms again. The wind has no visible form. The open water stays low and calm, no breaking waves, no whitecaps, no surf, no wave rises toward the camera; only the light spray lifted by the wind. Everything stays cold, dim and dark teal: no light appears, no glints, no gold, no warm tones. Painterly matte painting style preserved exactly, brush texture stays visible, slow and steady camera, no camera shake, no cuts, no people, no figures, no faces, no silhouettes, no birds, no text appears.

### Shot 4: Let there be light (19.0 to 26.0, 7.0 s)
- On screen: total dark held over the deep while GOD speaks. Then warm gold light breaks along the horizon and spreads across the water toward camera. No sun, no beam from a point: the light has no visible source.
- Camera: locked for the first 3.5 s, then a slow push in as the light arrives.
- Over it: GOD g01 "Let there be light," at 19.8 over darkness; light breaks at 22.5; n04 "and there was light." at 24.6. Caption 1:3 completes.
- Image prompt (first frame):
  > A vast dark ocean under total darkness, seen from just above the water, the horizon a level line barely readable against black, and along the far edge of the horizon the first hairline of warm gold light just beginning, thin as a thread, with no visible source, no sun, no beam, no glow from any point. Everything else deep ink teal and black, a single faint gold glint on the farthest swell. Hand painted matte painting, painterly illustration with visible brush texture and soft canvas grain, reverent, still and quiet, soft diffused light, restrained palette of deep ink teal (#0E2A2E) shadows, water teal (#0F6C6C) midtones and warm muted gold (#B8862F) light, warm cream highlights, vertical 9:16 composition with calm empty space in the lower middle, no people, no figures, no faces, no silhouettes, no animals, no birds, no text, no lettering, no watermark, not photoreal, not cartoon, not 3D render.
- Motion prompt:
  > Locked camera. For the first three seconds nothing changes at all: total darkness over the low, calm water, held completely still. Then warm gold light rises evenly along the whole width of the horizon at once, from edge to edge, and spreads smoothly and gradually across the water toward the camera, the swells catching gold one after another, the darkness lifting upward and away. The light has no source and no centre: no sun, no point of light, no bright column, no glittering reflection path on the water, no beams. The water stays low and calm, no breaking waves, no whitecaps, no spray, no surf, no wave rises toward the camera. A slow push in begins only as the light arrives. Painterly matte painting style preserved exactly, brush texture stays visible, slow and steady camera, no camera shake, no cuts, no people, no figures, no faces, no silhouettes, no birds, no text appears.

### Shot 5: The light was good (26.0 to 32.5, 6.5 s)
- On screen: wide. The deep flooded with warm gold light across its whole surface; the darkness drawn back into a deep teal band at the top of frame, a soft clear boundary forming between light and dark.
- Camera: slow pull back revealing the breadth of the light.
- Over it: n05 (Gen 1:4) at 26.8. The boundary is visibly settling before "and He separated" at about 29.9. Caption 1:4.
- Image prompt:
  > Wide view of a calm ocean now flooded with warm gold light across its whole surface, the water glowing softly gold and cream, gentle swells shining. The darkness has drawn back into a deep ink teal band across the top of the frame, and between the gold light and the dark there is a soft, clear, level boundary. No sun, no visible source of the light, no clouds, no land. Peaceful, full, good. Hand painted matte painting, painterly illustration with visible brush texture and soft canvas grain, reverent, still and quiet, soft diffused light, restrained palette of deep ink teal (#0E2A2E) shadows, water teal (#0F6C6C) midtones and warm muted gold (#B8862F) light, warm cream highlights, vertical 9:16 composition with calm empty space in the lower middle, no people, no figures, no faces, no silhouettes, no animals, no birds, no text, no lettering, no watermark, not photoreal, not cartoon, not 3D render.
- Motion prompt:
  > Slow pull back revealing the full breadth of the gold light on the water. The darkness at the top gently withdraws and the boundary between light and dark settles into a clean, steady line. The swells shimmer softly. The water stays low and calm, no breaking waves, no whitecaps, no spray, no surf, no wave rises toward the camera. Painterly matte painting style preserved exactly, brush texture stays visible, slow and steady camera, no camera shake, no cuts, no people, no figures, no faces, no silhouettes, no birds, no text appears.

### Shot 6: Day and night (32.5 to 38.5, 6.0 s)
- On screen: the same sea split side by side. Left half bathed in warm gold daylight, right half in deep ink teal night, a wide, soft gradient of twilight blending them, with clear air and no clouds.
- Camera: slow push in toward the twilight between them.
- Over it: n06 (Gen 1:5a) at 33.0. Caption 1:5 first half.
- Image prompt:
  > One continuous calm ocean divided side by side into two halves: the left half bathed in warm gold daylight with shining cream and gold water, the right half in deep ink teal night with dark, quiet water, and between them a wide, soft gradient of water teal twilight blending one into the other across the middle of the frame, painted, not a hard edge. Clear, empty air above the water with no clouds and no sky texture. The horizon is one level line across both halves. No sun, no moon, no stars, no clouds, no land. Balanced, ordered, calm. Hand painted matte painting, painterly illustration with visible brush texture and soft canvas grain, reverent, still and quiet, soft diffused light, restrained palette of deep ink teal (#0E2A2E) shadows, water teal (#0F6C6C) midtones and warm muted gold (#B8862F) light, warm cream highlights, vertical 9:16 composition with calm empty space in the lower middle, no people, no figures, no faces, no silhouettes, no animals, no birds, no text, no lettering, no watermark, not photoreal, not cartoon, not 3D render.
- Motion prompt:
  > Slow push in toward the soft twilight where gold day blends into ink teal night. Gentle swells move across both halves; the blend stays steady. The water stays low and calm, no breaking waves, no whitecaps, no spray, no surf, no wave rises toward the camera. Painterly matte painting style preserved exactly, brush texture stays visible, slow and steady camera, no camera shake, no cuts, no people, no figures, no faces, no silhouettes, no birds, no text appears.

### Shot 7: Each thing in its place (38.5 to 46.0, 7.5 s)
- On screen: the calm, ordered deep under settled light. Long, even, parallel swells in a steady rhythm toward a clear level horizon. Where before there was chaos, now order.
- Camera: very slow push in.
- Over it: n07 (study line) at 39.2. Caption, narration style.
- Image prompt:
  > A calm, ordered ocean under settled, even light, long gentle parallel swells rolling in a steady, measured rhythm toward a clear, perfectly level horizon line, warm gold light resting above the horizon and deep water teal water below, every line in the scene calm and balanced. Above the horizon is clear, empty, smooth air with a soft even gold glow and no clouds, no bands, no streaks, no sky texture at all. No sun, no visible source of the light, no land. Serene and ordered where before there was only formless dark. Hand painted matte painting, painterly illustration with visible brush texture and soft canvas grain, reverent, still and quiet, soft diffused light, restrained palette of deep ink teal (#0E2A2E) shadows, water teal (#0F6C6C) midtones and warm muted gold (#B8862F) light, warm cream highlights, vertical 9:16 composition with calm empty space in the lower middle, no people, no figures, no faces, no silhouettes, no animals, no birds, no text, no lettering, no watermark, not photoreal, not cartoon, not 3D render.
- Motion prompt:
  > Very slow push in over the calm water. The long parallel swells roll in a steady, even rhythm toward the level horizon; nothing else changes. The water stays low and calm, no breaking waves, no whitecaps, no spray, no surf, no wave rises toward the camera. Painterly matte painting style preserved exactly, brush texture stays visible, slow and steady camera, no camera shake, no cuts, no people, no figures, no faces, no silhouettes, no birds, no text appears.

### Shot 8: Evening and morning (46.0 to 52.5, 6.5 s)
- On screen: the same calm deep. The gold light lowers along the horizon into ink teal evening, the water darkens, then a pale gold glow returns along the horizon as morning. No sun disc at any point.
- Camera: locked, very slow push in.
- Over it: n08 (Gen 1:5b) at 46.5, "evening" as the light fades, "morning" as it returns. Caption 1:5 second half.
- Image prompt (first frame):
  > The calm ocean at evening, the warm gold light lying low and fading into deep ink teal dusk along a level horizon, the water darkening to water teal and ink with a last soft band of gold reflected near the horizon. No sun disc, no moon, no stars, no clouds, no land. Quiet, ending, peaceful. Hand painted matte painting, painterly illustration with visible brush texture and soft canvas grain, reverent, still and quiet, soft diffused light, restrained palette of deep ink teal (#0E2A2E) shadows, water teal (#0F6C6C) midtones and warm muted gold (#B8862F) light, warm cream highlights, vertical 9:16 composition with calm empty space in the lower middle, no people, no figures, no faces, no silhouettes, no animals, no birds, no text, no lettering, no watermark, not photoreal, not cartoon, not 3D render.
- Motion prompt:
  > Locked camera with a very slow push in. The low gold light fades fully into ink teal night and the water darkens, then a soft pale gold glow returns along the horizon as morning and spreads gently over the water. No sun, moon or stars appear at any point. The water stays low and calm, no breaking waves, no whitecaps, no spray, no surf, no wave rises toward the camera. Painterly matte painting style preserved exactly, brush texture stays visible, slow and steady camera, no camera shake, no cuts, no people, no figures, no faces, no silhouettes, no birds, no text appears.

### Shot 9: Waters without shape (52.5 to 58.5, 6.0 s)
- On screen: pale early light over vast waters with no shape: water meeting water in a hazy, undivided horizon, no expanse yet, no land. The upper half calm and empty for the end card text. Fades to black at the end.
- Camera: slow rise upward over the water.
- Over it: n09 at 53.3. End card text from 55.0: `Day Two`, `makor.co.za/genesis/the-seven-days`, `Makor`.
- Image prompt:
  > Pale early morning light over vast, unshaped waters stretching in every direction, the water rising into a soft haze where water seems to meet water with no clear horizon and no division between them. The upper part is smooth, even, softly luminous haze with no clouds, no cloud shapes, no streaks, no brushy sky texture, no sky at all, no land, no sun. Soft cream and pale gold light, water teal mist, deep ink teal at the lower edge. A feeling of waiting, of something not yet done. The upper half of the frame is calm, soft and nearly empty. Hand painted matte painting, painterly illustration with visible brush texture and soft canvas grain, reverent, still and quiet, soft diffused light, restrained palette of deep ink teal (#0E2A2E) shadows, water teal (#0F6C6C) midtones and warm muted gold (#B8862F) light, warm cream highlights, vertical 9:16 composition with calm empty space in the lower middle, no people, no figures, no faces, no silhouettes, no animals, no birds, no text, no lettering, no watermark, not photoreal, not cartoon, not 3D render.
- Motion prompt:
  > Slow rise upward over the still waters, the soft haze where water meets water shimmering gently and staying undivided. Calm and expectant. The water stays low and calm, no breaking waves, no whitecaps, no spray, no surf, no wave rises toward the camera. Painterly matte painting style preserved exactly, brush texture stays visible, slow and steady camera, no camera shake, no cuts, no people, no figures, no faces, no silhouettes, no birds, no text appears.

## Rule check on this script

- No em dashes or en dashes in this file.
- Every verse line matches `text.units[0].verses` of the study JSON exactly once, in order.
- GOD speaks only "Let there be light," verbatim from 1:3.
- No prompt depicts God, a figure or a bird; the Spirit is shown only as wind on water.
- Banned words list checked against every prompt: none present.
- Day One continuity: no sun, moon, stars, land, clouds or creatures in any prompt.
