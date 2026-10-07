# Makor films: style bible

**Photoreal for every film except The Seven Days (7 October 2026).** Luyanda approved the photoreal
treatment after the test in `films/tests/` (Adam portrait B, the animated sample of "To
cultivate and keep"). Shared prompt wording: `films/tools/photoreal.py`. The section "Photoreal" below replaces "The look", "People", the style
suffix and the motion suffix for every film from The Garden on. The painted rules that follow
it stay for reference and for The Seven Days, which keeps its painted look. Everything under
"What is never shown", "Christ", "History and the nations" and "Banned prompt words" holds for
both looks.

## Photoreal

- Photorealistic cinema, as if shot on 35 mm film in natural light. Real skin, soil and
  plants. Not glossy, not fantasy, no lens flares. The Makor palette is the colour grade:
  deep ink teal shadows, warm muted gold highlights, warm cream whites, no saturated reds or
  purples. Still and reverent; one subject; slow camera.
- Cast once, keep for good. Each person gets a casting portrait (and a turnaround sheet)
  approved by Luyanda, saved in the film's `stills/cast/`, and sent as a reference in every
  shot they appear in. Adam: `films/genesis/02-the-garden/stills/cast/adam.jpg` (dark olive
  brown, short tight black curls, short dense beard, about thirty). The woman:
  `stills/cast/eve.jpg` (option A). Both portraits carry a cloth on the shoulder from the
  model; every prompt says to keep the face but not the cloth.
- People are of the ancient Near East, never the pale European figures of Renaissance art and
  never the long haired screen look that reads as Christ.
- People may be seen at medium distance and their faces may be seen. No extreme close up of a
  face; the frame stays at chest up or wider.
- Before the Fall (Genesis 2:25) the man and the woman wear nothing: frame them from the
  chest up (the woman from the shoulders up), from behind or in profile, with grass, plants
  or landscape covering the rest. Never nudity below the chest. Describe the framing, never
  write "no clothing" (the image model's safety filter refuses it). After 3:21, untailored
  animal hide tied with a leather strip; no woven cloth before then.
- Plants and animals of the ancient Near East only (date palms, figs, pomegranates, olives,
  vines, reeds; ibex, gazelle, fallow deer, aurochs, lion). Name them in the prompt or the
  model drifts tropical. The tree of the knowledge of good and evil is of no recognisable
  species, never an apple. In the garden: "no walls, no buildings, no ruins, nothing made by
  hands", or the model adds mud brick walls.
- YouTube AI disclosure: answer **Yes** for photoreal films (realistic people).
- Veo: Fast for people and movement, Lite only for calm landscape. Check every people clip for
  face drift and for the framing slipping below the chest; use only the clean seconds.

Photoreal style suffix (every still prompt):

    Photorealistic cinematic film still, shot on 35mm film, natural light, colour grade of
    deep ink teal shadows and warm muted gold highlights, warm cream whites, no saturated reds
    or purples, calm and reverent, wide 16:9 composition with calm low detail space in the
    lower third, full frame with no borders or black bars, no text, no lettering, no
    watermark, not a painting, not an illustration, not a 3D render, not cartoon.

Photoreal motion suffix (every image to video prompt), plus for people: "The man's face, skin
tone, hair and beard stay exactly the same throughout; the framing stays modest."

    Photorealistic cinematic footage with natural real world motion, slow and steady camera,
    no camera shake, no cuts, no text appears.

# Painted look (The Seven Days; reference)

One visual style for every Makor story film. Every still prompt and every
motion prompt follows this page. If a shot needs to break a rule here, change
this page first, on purpose, rather than drifting shot by shot.

## The look

- Painterly and illustrated, reverent and still. Hand painted matte paintings
  with soft light, visible brush texture and a faint canvas grain.
- Not photoreal. Not cartoonish. Not glossy 3D. Not anime. Not fantasy game art.
- Large calm negative space. One clear subject per frame. Restraint over spectacle.
- Light is the hero of the palette: it arrives warm and gold out of deep teal dark.

## Palette (the Makor brand)

| Name  | Hex       | Use in film                                          |
|-------|-----------|------------------------------------------------------|
| Ink   | `#0E2A2E` | Shadows, night, the deep, the dark before light      |
| Water | `#0F6C6C` | Midtones, water, sheen on swells, twilight           |
| Light | `#B8862F` | Light, warmth, the source point, gold on water       |

Everything else is a tint or shade of these three. No saturated reds, purples
or neon blues. Whites are warm (a pale gold cream), never pure white.

## Camera language

- Slow push ins, slow pull backs, slow lateral drifts, slow rises.
- One move per shot, held for the whole shot. Never two moves fighting.
- No fast cuts, no whip pans, no shaky cam, no zoom snaps, no handheld feel.
- Cuts land on a breath or a beat of the voice, never in the middle of a word.
- Cross dissolves of about half a second between shots. Fades to and from black
  only at the very start and the very end.

## Frame and text safety (9:16, 1080 by 1920)

- Keep the subject in the centre column. The right 180 px is covered by the
  Shorts and Reels buttons; the bottom 420 px by the caption and channel bar;
  the top 160 px by the progress and title UI.
- Burned in captions sit in a band from y 1120 to y 1460, x 90 to x 900.
- Leave calm, low detail space behind the caption band in every keyframe.

## What is never shown

- God is never depicted, and never the face of Christ. God is shown only by
  effect: light breaking, water moving, a voice.
- The Spirit over the waters is wind on the surface: ripples, a moving breath
  across the water, drifting spray. Never a figure, never a bird, never a dove.
- Never invent a scene the text does not give.
- Creation continuity: show only what exists by that day of the text. On Day One
  that means no sun disc, no moon, no stars, no land, no sky dome or clouds (the
  expanse is Day Two), no plants, no creatures, no people.

## People (from Day Six onward)

- People appear only where the text puts them. Paint them at a distance, in
  natural light, seen from behind or in profile, faces not detailed, partly
  framed by landscape (tall grass, trees, rock). Modest and unposed. Never a
  close up of a face.
- The suffix "no people, no figures" is dropped only for those shots; every
  other shot keeps it.

## Christ

- Never the face of Christ, never a figure meant to be Him. Scenes the New
  Testament gives may be shown by their setting alone, for example the stone
  rolled back from an empty tomb at first light (John 20:1), with no figures.

## History and the nations

- Context about Egypt, Babylon and other nations is shown through objects and
  landscapes only: rivers, brick kilns, clay tablets, seas, cities at a
  distance. Never images or statues of their gods.

## Banned prompt words

Never put these words in any prompt, including in a negative ("no ..."):

    deity, god figure, divine being, halo, glowing man, angel, temple, idol

Exclude what they describe with neutral words instead: "no people, no figures,
no faces, no silhouettes".

## Style suffix (append to every still prompt)

    Hand painted matte painting, painterly illustration with visible brush
    texture and soft canvas grain, reverent, still and quiet, soft diffused
    light, restrained palette of deep ink teal (#0E2A2E) shadows, water teal
    (#0F6C6C) midtones and warm muted gold (#B8862F) light, warm cream
    highlights, vertical 9:16 composition with calm empty space in the lower
    middle, no people, no figures, no faces, no silhouettes, no animals, no
    birds, no text, no lettering, no watermark, not photoreal, not cartoon, not
    3D render.

## Before the light (stills set before light exists, e.g. Genesis 1:1 to 2)

The standard suffix asks for gold light, and the model then sneaks gold glints
into shots that must be dark. For any shot before "Let there be light", swap the
palette clause for this one:

    restrained palette of deep ink teal (#0E2A2E) and black with only cold, dim
    water teal (#0F6C6C) on the crests, no gold, no warm tones, no light source,
    no glow on the horizon

## Calm water in motion

Veo turns "swells" into breaking surf for drama. For any calm water shot, add
to the motion prompt: "the water stays low and calm, no breaking waves, no
whitecaps, no spray, no surf, no wave rises toward the camera".

## Motion for still shots (standard from The Garden onward)

Every still shot gets depth motion (`films/tools/depth_move.py`): a depth map from
Depth Anything V2 Small (Apache 2.0, local) drives a slow push in or sideways drift in
which near layers move more than far ones. Free, about 15 s of rendering per shot. Flat
pushes are only a fallback.

## Veo models (from The Seven Days)

- Veo 3.1 Lite (0.64 USD per 8 s at 1080p): calm shots only: water, grass, landscape drift.
  It adds halos and softens detail on lit or complex shots, and cannot interpolate.
- Veo 3.1 Fast (0.96 USD): creatures, light, people, transitions, first and last frame.
- Each model has its own daily limit of about 10 requests.

## Motion suffix (append to every image to video prompt)

    Painterly matte painting style preserved exactly, brush texture stays
    visible, slow and steady camera, no camera shake, no cuts, no people, no
    figures, no faces, no silhouettes, no birds, no text appears.

The model's own generated audio is always discarded. All sound is laid in the
edit.
