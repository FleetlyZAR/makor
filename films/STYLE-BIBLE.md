# Makor films: style bible

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

## Motion suffix (append to every image to video prompt)

    Painterly matte painting style preserved exactly, brush texture stays
    visible, slow and steady camera, no camera shake, no cuts, no people, no
    figures, no faces, no silhouettes, no birds, no text appears.

The model's own generated audio is always discarded. All sound is laid in the
edit.
