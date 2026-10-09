#!/usr/bin/env python3
"""Storyboard and shot list for The Seven Days v2 (photoreal, films/CINEMA-STANDARD.md).

Every picture segment of the timeline (each PIC beat in script/movement.py) is cut into shots here,
fast in the set pieces and the cold open montage, longer under teaching. Each shot's image prompt
gets the photoreal rules (films/tools/photoreal.py, films/STYLE-BIBLE.md) and the right cast
references automatically, and is checked for banned words.

Writes script/movement-shots.json (timings, replacing the animatic's automatic cut),
script/shotlist.md (for films/tools/still.py and still_batch.py), script/shotlist.json (for the
edit) and script/storyboard.md (to read).

Kinds: veo (keyframe, then animated), still (keyframe with a move in the edit), reuse (an existing
image), graphic (built in the edit from other shots).

    python3 films/genesis/01-the-seven-days-v2/script/storyboard.py
"""
import json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
FILM = HERE.parent
sys.path.insert(0, str(HERE.parents[3] / "films" / "tools"))
import photoreal as PR  # noqa: E402

REF = {"bm": "stills/cast/brickmaker.jpg", "bm_turn": "stills/cast/brickmaker-turnaround.jpg",
       "adam": PR.ADAM, "eve": PR.EVE}
NOFIG = "No people, no figures, no faces, no silhouettes."
NOGOD = "No hands and no figure in the sky, in the light or in the wind."
NOCHRIST = "No figures at all; never a figure meant to be Christ."
DISTANT = "Any people are small and far off, faces not visible."
BM = ("The man is the brick-maker in the reference images: keep his face, skin tone, curly dark hair with grey, "
      "full beard with grey at the chin, build and his rough undyed knee length linen tunic exactly. He is a slave in "
      "Egypt: worn, exhausted, grieving, never smiling. Framed from the chest up or wider, never an extreme close up "
      "of the face.")
MAN = ("The man is the man in the reference portrait: keep his face, skin tone, hair and beard exactly, but not the "
       "cloth on his shoulder. He wears nothing; he is seen from the chest up, facing the camera, in profile or from "
       "behind, or with tall grass covering him below the chest. Nothing below the chest is visible. No other people.")
PAIR = PR.BEFORE_FIGS
WOMAN = ("The woman is the woman in the reference portrait: keep her face, skin tone and long curly hair exactly, but "
         "not the cloth on her shoulder. A head and shoulders portrait: her long thick hair falls forward over her bare "
         "shoulders. No other people.")
BANNED = ["deity", "god figure", "divine being", "halo", "glowing man", "angel", "temple", "idol"]
EGYPT = "Ancient Egypt by the Nile: date palms, reeds, mud brick, no statues, no carvings of figures, no pyramids in close view."


def S(scene, kind="still", refs=(), flags="", motion="Slow push in.", w=1.0, src=None, omni=None, cue=None):
    # omni: how films/tools/omni_clips.py makes this shot's clip when it is not the default (from the keyframe)
    # cue: words in the narration; the shot starts as they are spoken (the shots between cues share the time by w)
    return dict(scene=scene, kind=kind, refs=list(refs), flags=flags, motion=motion, w=w, src=src, omni=omni, cue=cue)


def bm(scene, kind="veo", motion="Slow push in.", w=1.0, flags="bm"):
    return S(scene, kind, ["bm", "bm_turn"], flags, motion, w)


# one list of shots per picture segment, in timeline order (index = PIC event number)
SEG = {
    # God speaks into the black; only then the drop (the light comes after the word)
    0: [S("", "graphic", flags="pure black with the faintest grain while God speaks: no light exists yet (made in the edit)",
          w=2.965),
        S("Extreme macro: a single drop of water falling in total darkness toward still black water, caught just above "
          "the surface, and at the centre of the surface one tiny point of warm white light.", "veo",
          motion="The drop falls and touches the still water; one ring spreads; where it touched, one tiny point of warm "
          "white light appears and brightens until it flares.", w=2.0)],
    # one continuous take (Omni, text to video), cut into s003, s004 and s005; extended for s006 and s007
    1: [S("One single continuous full frame image, no panels, no split, no border. The Big Bang: complete darkness all around, and at the very centre a single point of white-gold light "
          "erupting outward in every direction at once, light and glowing star dust exploding toward the camera, "
          "streams of luminous debris shooting past the lens on every side, the darkness torn open by light.", "veo",
          omni=dict(mode="text", prompt=(
              "One continuous shot, deep space, cinematic. [0-1s] Total darkness; at the exact centre a single tiny point of "
              "white-gold light flares. [1-3s] The light erupts outward in every direction and floods toward the camera until "
              "brilliant white-gold light fills the entire frame edge to edge. [3-4.5s] The light thins and dims, fading almost "
              "to black, as if making room, the dark of space opening. [4.5-7.5s] Out of the dark, countless small glowing balls "
              "of starlight fly past the camera on every side as we move forward ever faster, space opening deep and wide around "
              "us. [7.5-10s] Far ahead a small blue and green world appears, the earth, with Africa, Arabia and the "
              "Mediterranean facing us, and we rush toward it as the last stars stream past. Light as a flood and as points of "
              "starlight, never a single glowing sphere in the middle of the frame. Sound: a deep sub boom at one second, "
              "then rushing air. No music, no voices, no text.")))],
    # the zoom in: the same take; down through the clouds into the garden; then history to today
    2: [S("Small glowing balls of starlight streaming past the camera in deep darkness, space opening, a small blue and green "
          "world far ahead.", "veo", motion="The camera rushes forward, the stars streaming past.", w=1.5,
          omni=dict(mode="same", clip="s003")),
        S("The earth seen from space, blue seas and green land under white cloud, Africa, Arabia and the Mediterranean "
          "facing us, filling more of the frame as we approach.", "veo", motion="The camera dives toward the earth.", w=1.5,
          omni=dict(mode="same", clip="s006")),
        S("Plunging down through white clouds, a green river land opening below in morning light.", "veo",
          motion="The camera dives down through the clouds toward the land.", w=1.5,
          omni=dict(mode="extend", clip="s003", prompt=(
              "Extend this video as one continuous shot, no cut. [0-4s] We plunge into the earth's atmosphere over the Near "
              "East and dive down through bright white clouds; below them a green river land opens in early morning light. "
              "[4-10s] We glide low and fast over date palms, fig and olive groves toward a winding river in a garden at first "
              "light, mist on the water. " + PR.NEAR_EAST + " No people. Sound: wind, then birds and water. No music, no "
              "voices, no text."))),
        S("Aerial descent over date palms, fig and olive groves toward a winding river in a garden at first light. "
          + PR.NEAR_EAST, "veo", motion="The camera descends toward the river and the trees.", w=1.5,
          omni=dict(mode="same", clip="s006")),
        S("The man and the woman together in the garden at first light by the river, a tight two shot of their heads and "
          "shoulders only, both facing the light, the dawn on their faces; her long thick hair falls forward over both her "
          "shoulders; the bottom edge of the frame is at their collarbones, so no chest is in the picture at all; "
          "palms and pomegranate trees soft behind them.", refs=["adam", "eve"], flags="pair", w=0.6,
          omni=dict(prompt="The man and the woman stand side by side in the garden at first light, framed from the chest "
                    "up exactly as in the image, looking toward the dawn with quiet wonder. A soft breeze stirs her long "
                    "hair, which stays where it is over her shoulders. The camera pushes in very slowly. The framing never "
                    "widens or drops lower.")),
        S("Fruit trees and a river in the garden in Eden, morning mist, birds over the water. " + PR.NEAR_EAST, w=0.6),
        S("The garden in Eden at first light: a clear river winding between groves of fruit trees and date palms, "
          "meadows of tall grass, mist in the low sun. " + PR.NEAR_EAST, w=0.6),
        S("A great flood: dark water covering the land under heavy storm clouds, one wooden ark far off on the water.",
          w=0.6),
        S("An old man of the ancient Near East standing outside a goat hair tent in the desert at night, seen from "
          "behind, looking up at a sky crowded with stars.", flags="people", w=0.6),
        S("", "reuse", src="stills/cast/shot-05.jpg", w=0.6),
        S("A large tent of dark woven curtains in a wilderness camp at dusk, the tabernacle of Israel, smoke rising "
          "from an altar before it, many small tents around it, seen from a hill.", flags="distant", w=0.6),
        S("Jerusalem in the age of the kings of Israel, about three thousand years ago, at dawn: a small walled hill "
          "city of pale limestone and flat roofed houses on terraces, thick ancient walls, seen from a hillside of olive "
          "trees. No domes, no minarets, no towers, no modern buildings, no churches.", flags="distant", w=0.6),
        S("A rock cut tomb in a garden at first light, its round stone rolled away from the dark doorway.", flags="christ",
          w=0.6),
        S("An ancient paved road running across hills toward the horizon at sunset, worn stones, centuries old.",
          flags="distant", w=0.6),
        S("A modern city at night seen from far above, rivers of light, streets glowing to the horizon.", w=0.6)],
    # the zoom out: back up from today to the single point, which becomes the spark in Egypt
    3: [S("Rising fast from a modern city at night up through the clouds, the night side of the earth below, the earth "
          "shrinking into darkness toward a single point of light.", "veo", motion="[0-2s] The camera pulls back and up at "
          "tremendous speed from the city through the clouds into space. [2-3.5s] The night side of the earth shrinks away "
          "into the dark until it is a single bright point of light in black. [3.5-10s] The single point of light hangs in "
          "the black and drifts very slowly upward.", w=1.2),
        S("A single glowing spark rising from a kiln fire into the black night sky, a few embers around it.", "veo",
          motion="The spark drifts upward and the fire comes into view below.", w=1.5,
          omni=dict(mode="bridge", clip="s019", at=5.2, prompt=(
              "One continuous shot. The single point of light in the black drifts upward and becomes a glowing ember, a spark "
              "rising into a night sky; the camera tilts gently down to find the kiln fire it rose from, in the brick pits of "
              "ancient Egypt at night, embers drifting. Use the first image as the starting frame and the second image as the "
              "final frame. No people. Sound: crackling fire. No music, no voices, no text.")))],
    4: [S("", "reuse", src="stills/cast/shot-05.jpg"),
        bm("His mud caked hands pressing wet clay into a wooden brick mould by firelight, rows of fresh bricks beside "
           "him; his face partly visible above, lit by the fire.", motion="He presses the clay and lifts the mould.")],
    5: [S("", "reuse", src="stills/cast/shot-06.jpg"),
        S("The night sky over the brick pits of Egypt, faint stars, kiln smoke drifting across them. " + EGYPT,
          motion="Slow tilt up into the stars."),
        S("Still black water in near total darkness, no moon, no stars, no reflection of any light, calm and empty.", w=1.3)],
    6: [S("The Nile at blazing dawn, the sun disc rising over palms and reeds, the river shining. " + EGYPT),
        S("Brick kilns smoking beside the Nile, long rows of drying mud bricks, labourers small and far off. " + EGYPT,
          flags="distant"),
        bm("Under the burning sun he staggers across the brick pits with a heavy stack of mud bricks on his shoulder, bent "
           "under the weight, sweat and mud on his skin, an overseer's shadow falling across the ground. " + EGYPT, motion="He walks slowly across the frame."),
        S("A clay tablet pressed with cuneiform wedge script lying on a reed mat beside a small oil lamp, close."),
        S("The city of Babylon on the Euphrates at dusk seen from far off: mud brick walls, a stepped tower, smoke "
          "from many hearths.", flags="distant"),
        S("A dark sea under a storm, great waves breaking against black rocks, spray in the wind."),
        S("The deep at rest: mist lying over still grey open sea to every horizon, nothing moving, no shore, no land, no trees. One single continuous image filling the whole frame edge to edge, no split, no border, no band, no fog band."),
        S("Egypt's sun at noon over the river, blinding white, shimmering heat over the water and the palms. " + EGYPT)],
    7: [S("Total darkness over an endless black ocean, the dark water clearly visible: heavy black rolling swells to the horizon, their crests catching a faint cold blue-grey sheen so the surface reads as water, utter darkness above, no light source, no moon, no stars, no land.", "veo",
          motion="A slow push across the surface of the deep.", w=1.2),
        S("Close on the surface of black water in darkness, slow heavy swell, a faint sheen."),
        S("A low wide view across a black ocean in darkness, the dark water clearly visible: heavy black rolling swells to the horizon, their crests catching a faint cold blue-grey sheen so the surface reads as water, utter darkness above, no light source, no moon, no stars, no land.")],
    8: [S("Wind moving across the surface of black water in darkness, ripples racing, fine spray lifting into the black air: the wind itself, with nothing in it; the dark water clearly visible: heavy black rolling swells to the horizon, their crests catching a faint cold blue-grey sheen so the surface reads as water, utter darkness above, no light source, no moon, no stars, no land, no golden light anywhere.", "veo", motion="A gust passes across the water from left to right.")],
    9: [S("Extreme macro: a single drop falling into black water in darkness.", "veo", motion="The drop touches the water.",
          w=0.8),
        S("A dark ocean at the moment the horizon ignites: a line of white-gold light breaking along the horizon.", "veo",
          motion="The light along the horizon brightens and spreads.", w=1.2, cue="Let there be light"),
        S("Most of the frame is still black ocean in darkness, heavy dark swells clearly visible in the foreground, and a line of brilliant warm light races across the water toward the camera from the horizon: behind its edge the water is gold, ahead of it the water is black.", "veo",
          motion="The wave of light races across the water toward the camera.", w=1.2, cue="and there was light"),
        S("Waves catching golden light for the first time, spray lit from within.", w=0.8),
        S("A vast ocean, half still in darkness and half in warm light, the line between them sharp.", w=1.2, cue="separated the light from"),
        S("Wide ocean in full warm light under a pale sky with no sun visible, the light everywhere.", "veo",
          motion="Slow rise over the water.", w=1.2),
        S("The same ocean at evening, light fading to deep blue.", w=1.0, cue="And there was evening"),
        S("The same ocean at first morning light, soft gold on calm water.", w=1.0, cue="and there was morning")],
    10: [S("A formless dark world: black water covering everything, mist lying low on it, the dark water clearly visible: heavy black rolling swells to the horizon, their crests catching a faint cold blue-grey sheen so the surface reads as water, utter darkness above, no light source, no moon, no stars, no land."),
         S("Wind moving over the face of the deep, ripples and drifting mist, nothing in it.", "veo",
           motion="Slow drift with the wind over the water."),
         S("", "graphic", flags="frame of three realms and three fillings, built in the edit from shots 34, 37, 48, 60, 69"),
         S("The surface of the deep at dawn, wind moving softly across it."),
         S("Open water to every horizon, the first soft light before any sun lying on it, no shore, no land, no trees anywhere.")],
    11: [S("Waters rising in great columns of mist from the sea, light between them.", "veo",
           motion="The mist rises and parts."),
         S("An expanse of clear sky opening between high clouds and the sea below, light like beaten gold.", "veo",
           motion="Slow rise into the open sky.", cue="Let there be an expanse"),
         S("The vault of the sky in golden light, thin high clouds stretched across it like hammered metal.", cue="So God made the expanse"),
         S("A calm sea under a vast clear sky, the horizon wide and empty.", cue="God called the expanse")],
    12: [S("The sea drawing back from wet black rock, water streaming off it.", "veo", motion="The water drains away."),
         S("Dry land rising out of the sea, streams pouring down its sides in morning light.", "veo",
           motion="Slow rise as the land lifts.", cue="so that the dry land may appear"),
         S("Broad wet mud plains shining as the seas gather into their basins.", cue="God called the dry land"),
         S("Time lapse feeling: the first green grass spreading across bare earth.", "veo", motion="Grass spreads.", w=0.6, cue="Let the earth bring forth vegetation"),
         S("Seed bearing plants unfurling, close, in morning light.", w=0.6),
         S("Young fruit trees with fruit on them: figs, pomegranates, olives, in morning light.", w=0.6),
         S("Hills turning green as far as the eye can see, river valleys between them.", w=0.6, cue="The earth produced vegetation"),
         S("A river valley of the ancient Near East: date palms, reeds, fig trees along the water.", w=0.6),
         S("A pomegranate tree heavy with fruit, close.", w=0.6),
         S("Seas, sky and green land together in one wide view, a shaped and empty world.", w=1.6, cue="the third day"),
         S("The same wide empty green world in silence, no creatures, no people.", w=1.6)],
    13: [S("A black sky over the new land and the sea, the faintest glow on the horizon.", "veo",
           motion="The glow on the horizon grows."),
         S("The first edge of the sun rising over the sea.", "veo", motion="The sun lifts.", cue="Let there be lights"),
         S("The sun rising fully over the sea, the first sunrise, gold across the water.", "veo",
           motion="Slow push toward the sun.", cue="And let them serve as lights"),
         S("Sunlight racing across green hills and valleys."),
         S("The sun high over the land, a bright clear day, long shadows shrinking.", cue="the greater light to rule the day"),
         S("A slender crescent moon and the first faint stars appearing over the sea at dusk, the last light low on the horizon", cue="the lesser light to rule the night")],
    14: [S("A full moon rising over the sea at night, a path of silver on the water.", "veo", motion="The moon rises."),
         S("Countless stars over dark hills.", "veo", motion="Slow tilt up into the stars."),
         S("The band of the Milky Way over the land and the sea, deep night.")],
    15: [S("", "reuse", src="stills/cast/shot-07.jpg"),
         S("Egypt's sun blazing over the brick pits, heat shimmering over rows of bricks. " + EGYPT, flags="distant"),
         S("The sun high and white over the Nile, palms below it. " + EGYPT)],
    17: [S("Underwater: shoals of silver fish turning together in shafts of sunlight.", "veo", motion="The shoal turns."),
         S("A pod of dolphins swimming just beneath the surface of clear blue water in sunlight, seen from above, their bodies sleek and grey, one breaking the surface with its dorsal fin, open sea all around"),
         S("Underwater: a great whale rising from the deep blue toward the light.", "veo", motion="The whale rises.", cue="So God created the great sea creatures"),
         S("A whale breaching out of the sea in slow motion, spray in the sunlight.", "veo",
           motion="The whale breaches and falls back."),
         S("Underwater: a vast shoal of silver fish filling the clear blue sea, shafts of sunlight falling through the water. One single continuous image filling the whole frame edge to edge, no split, no border, no band.", w=0.7),
         S("Flocks of seabirds lifting off the water into the open sky.", "veo", motion="The birds lift and wheel.", cue="let birds multiply"),
         S("Seabirds wheeling over waves in morning light.", w=0.8),
         S("Underwater: a great sea creature gliding slowly through blue light.", w=0.8, cue="a word that elsewhere names"),
         S("Birds flying into a vast open sky above the sea.", w=0.8),
         S("The whole sea alive at golden hour, wide from a cliff top: great flocks of seabirds far off over the calm shining water, sunlight on the waves. One single continuous image filling the whole frame edge to edge, no split, no border, no band.", w=1.2)],
    18: [S("A herd of aurochs stampeding across a grass plain, dust rising.", "veo", motion="The herd runs past."),
         S("Gazelle leaping across the plain.", "veo", motion="The gazelle leap."),
         S("Ibex standing on a high rock cliff above a valley."),
         S("Hooves striking dry earth, dust flying, close.", "veo", motion="Hooves pound past."),
         S("A lion watching from tall grass."),
         S("Wild horses and onagers running along a river, spray."),
         S("A herd seen against a low sun, dust glowing gold."),
         S("The wide plain full of every kind of creature.")],
    19: [S("The herds slowing and grazing, dust settling."),
         S("The plain empty and still in first light, nothing moving.", w=1.3)],
    20: [S("Darkness over the land before dawn, the shapes of hills barely visible."),
         S("The faintest first light on the horizon over the land.", "veo", motion="The light grows very slowly."),
         S("Dawn coming slowly over a vast garden land of trees and grass by a river. " + PR.NEAR_EAST)],
    21: [S("A vast garden land at first light; far off, the man and the woman stand side by side in reeds and grass "
           "that rise to their chests, so only their heads and shoulders show above the green, the light growing around "
           "them.", "veo", ["adam", "eve"], "pair", "Slow push in from far away.", w=1.2),
         S("The man at first light in tall grass, seen from the chest up in three quarter view, his face lit by the "
           "dawn, wonder in his eyes as he looks at the world.", "veo", ["adam"], "man", "He breathes and looks up.", w=1.2, cue="in the image of God He created him"),
         S("The woman at first light, a close portrait framed from the collarbones up, the bottom of the frame at her "
           "collarbones, her long hair falling over her shoulders, her face lit by the dawn, calm and alive, looking out at "
           "the world.", "veo", ["eve"], "woman", "She turns her head toward the light.",
           w=1.2, cue="male and female He created them"),
         S("The man and the woman in the first light turning toward each other, a close two shot framed from the shoulders "
           "up, faces in profile, gentle expressions, her long hair over her shoulders; the frame ends at their shoulders.",
           "veo", ["adam", "eve"], "pair", "They turn toward each other.", w=1.3),
         S("Sunrise over the garden: river, groves and meadows in first gold light. " + PR.NEAR_EAST),
         S("The two standing together in tall grass that rises to their chests, seen from the front at medium distance, "
           "looking out over the new world, the sun rising behind the camera on their faces.", refs=["adam", "eve"],
           flags="pair", w=1.1)],
    22: [bm("Night by a small fire in the brick pits of Egypt; he sits with his forearms on his knees, his face lit by "
            "the fire, eyes wet and heavy, face drawn with exhaustion and grief, listening.", motion="Very slow push in."),
         bm("He lifts his weary, grief-worn face toward the fire's light, as if hearing something he hardly dares believe; no smile.",
            motion="He raises his eyes.")],
    23: [S("Fields of wild grain moving in the wind in golden light. " + PR.NEAR_EAST),
         S("Fruit trees heavy with fruit: figs, pomegranates, dates. " + PR.NEAR_EAST),
         S("Seed bearing plants and herbs close, dew on them."),
         S("The man and the woman far off among fruit trees, tiny in the frame, standing in reeds and grass that rise to "
           "their chests, so only their heads and shoulders show above the green.", refs=["adam", "eve"], flags="pair"),
         S("Deer and gazelle grazing in a green meadow.", cue="And to every beast of the earth"),
         S("A wide fertile valley with a river, groves and meadows. " + PR.NEAR_EAST),
         S("Ripe figs on a branch, close."),
         S("The two walking far off through tall grass toward the trees.", refs=["adam", "eve"], flags="pair"),
         S("The whole created world alive in golden evening light: a river valley with herds grazing, birds over the water, fruit trees and meadows, the sea shining beyond, everything at peace", cue="And God looked upon all")],
    24: [S("The whole world in golden light, sea, land and sky together, wide, seen from a hilltop: green hills, a river and the shining sea. One single continuous image filling the whole frame edge to edge, no split, no border, no band, no fog band.", "veo", motion="Slow rise."),
         S("The whole world in golden light from very high, river, land and sea.")],
    25: [S("A still lake in long golden light, a perfect reflection, nothing moving."),
         S("Tall grass standing perfectly still in evening gold.", cue="And by the seventh day"),
         S("A calm sea at evening, the water like glass.", cue="Then God blessed the seventh day"),
         S("Sunlight through still leaves of a fig tree."),
         S("A deer resting in the grass at evening."),
         S("A wide valley in silence at golden hour."),
         S("The finished world at evening from a hilltop, everything at rest."),
         S("Long evening light across the land, a few birds settling.")],
    26: [bm("Evening in the wilderness: he sits with his wife and children around a small fire outside goat hair tents, "
            "resting, stars appearing. His wife and children are seen from behind or at a distance.", flags="family"),
         S("Children asleep under a woven blanket by a small fire outside a low tent of black goat hair in the wilderness of the ancient Near East at evening, seen from a distance, no modern tent, no canvas; sandy ground and stones fill the foreground to the bottom edge of the frame, no mist. One single continuous image filling the whole frame edge to edge, no split, no border, no band, no fog band.",
           flags="distant"),
         bm("He rests with his eyes closed by the fire, at peace, his hands open on his knees.", motion="Very slow push in.")],
    27: [S("A single point of light in total darkness.", "veo", motion="The point of light glows steadily."),
         S("The point of light, a little larger, soft rays around it, darkness everywhere else.", cue="In the beginning was the Word")],
    28: [S("The point of light widening into a soft dawn across a dark sky.", "veo", motion="The light widens."),
         S("Dawn breaking over hills, first light on the first day of the week.", cue="The Light shines in the darkness")],
    29: [S("A garden of olive trees at first light, dew on the grass, mist.", flags="christ"),
         S("A rock cut tomb in the garden, its great round stone rolled back from the doorway.", "veo", flags="christ",
           motion="Slow push toward the open doorway.", cue="Jesus lies in the tomb"),
         S("The empty doorway of the tomb from close by, light falling inside onto the bare stone ledge.", flags="christ", cue="and rises on the first day"),
         S("Morning light streaming out of the open tomb across the garden path.", "veo", flags="christ",
           motion="The light grows.")],
    30: [S("A stone path through the garden in early morning light, dew shining.", flags="christ"),
         S("Light on dew on grass and leaves, close.", flags="christ"),
         S("The garden in full sunrise, wide, the open tomb small in the distance.", flags="christ")],
    31: [S("Dark flood water pouring over the land, creation undone, under black clouds.", "veo",
           motion="The water spreads over the land."),
         S("Storm over the flood, rain and dark water to the horizon."),
         S("The clouds breaking and light pouring down on the water."),
         S("The new Jerusalem seen from far off at dusk: a vast square city of pale gold stone and clear crystal walls on a "
           "great high mountain, its walls glowing from within with warm light, a high gate of pearl standing open in the "
           "wall with light pouring out across the mountainside; low, broad and ancient in form, simple flat roofed "
           "buildings of the ancient Near East behind the walls. No sun in the sky; the light comes from the city itself. "
           "No castle, no spires, no turrets, no domes, no fairytale palace, no European architecture.", "veo",
           motion="Slow rise toward the city.", w=1.2),
         S("A clear river of the water of life flowing out from the city along a broad street of pale gold stone, trees of "
           "life on both banks bearing fruit, the city walls glowing behind: a vast square city of pale gold stone with glowing crystal walls, low flat roofed buildings of the ancient Near East, no towers, no spires, no domes, no castle, no skyscrapers, no modern or European architecture.", "veo",
           motion="Slow push along the river.", w=1.2),
         S("A new world of hills and rivers in radiant light, with no sea anywhere, a land without end.", w=1.2),
         S("The new creation from far above at golden light: hills, rivers and fields to the horizon, and at the centre, small and shining, the city: a vast square city of pale gold stone with glowing crystal walls, low flat roofed buildings of the ancient Near East, no towers, no spires, no domes, no castle, no skyscrapers, no modern or European architecture. Full frame, no black bars.")],
    32: [S("The dark deep, the dark water clearly visible: heavy black rolling swells to the horizon, their crests catching a faint cold blue-grey sheen so the surface reads as water, utter darkness above, no light source, no moon, no stars, no land.", motion="Slow push."),
         S("Light breaking across the dark deep along the horizon.", "veo", motion="The light spreads across the water.", cue="speak light into a dark place"),
         S("Warm light on the water, the darkness lifting.")],
    33: [S("", "reuse", src="../02-the-garden/stills/movement/s024.jpg")],
}


def prompt_for(sh):
    f = sh["flags"]
    if f == "pair":
        who = PAIR + " " + PR.NEAR_EAST
    elif f == "woman":
        who = WOMAN + " " + PR.NEAR_EAST
    elif f == "man":
        who = MAN + " " + PR.NEAR_EAST
    elif f in ("bm", "family"):
        who = BM + (" No other people." if f == "bm" else "")
    elif f in ("people", "distant"):
        who = DISTANT
    elif f == "christ":
        who = NOCHRIST
    else:
        who = NOFIG
    refs = [REF[r] for r in sh["refs"]]
    p = f"{sh['scene']} {who} {NOGOD}{PR.REFNOTE if refs else ''} {PR.SUFFIX}"
    low = p.lower() + sh["motion"].lower()
    for w in BANNED:
        assert w not in low, f"banned word {w!r} in: {sh['scene'][:60]}"
    assert "–" not in p and "—" not in p
    return p, refs


def cue_time(T, durs, words, a, b):
    """When `words` are spoken inside [a, b): the line's start plus its share of the line by character position
    (the voices keep an even pace, so this lands within a fraction of a second)."""
    for e in T["events"]:
        if e["kind"] == "line" and a - 0.01 <= e["t"] < b and words.lower() in e["text"].lower():
            k = e["text"].lower().index(words.lower())
            return e["t"] + durs.get(e["id"], 0) * k / max(1, len(e["text"]))
    raise SystemExit(f"cue not found in its segment: {words!r}")


def main():
    T = json.loads((HERE / "movement-timeline.json").read_text())
    durs = json.loads((HERE / "movement-durations.json").read_text())
    pics = [e for e in T["events"] if e["kind"] == "pic"]
    shots, n = [], 0
    for i, e in enumerate(pics):
        end = pics[i + 1]["t"] if i + 1 < len(pics) else T["total"]
        if end - e["t"] < 0.05:
            continue                    # a picture note whose lines were cut (the lamp in The first sunrise)
        segs = SEG[i]
        # anchors: the segment's start, each cued shot's start (when its words are spoken), the segment's end
        starts = [None] * len(segs)
        starts[0] = e["t"]
        for k, s in enumerate(segs):
            if s.get("cue") and k:
                starts[k] = cue_time(T, durs, s["cue"], e["t"], end)
        bounds = [k for k in range(len(segs)) if starts[k] is not None] + [len(segs)]
        times = starts + [end]
        for a, b in zip(bounds, bounds[1:]):
            t0, t1 = times[a], times[b]
            assert t1 > t0, f"cues out of order in segment {i}"
            tot = sum(s["w"] for s in segs[a:b])
            for k in range(a, b):
                starts[k] = t0
                t0 += (t1 - times[a]) * segs[k]["w"] / tot
        for k, s in enumerate(segs):
            n += 1
            d = (starts[k + 1] if k + 1 < len(segs) else end) - starts[k]
            shots.append(dict(id=f"s{n:03d}", chapter=e["chapter"], start=round(starts[k], 3), dur=round(d, 3),
                              picture=e["text"], **s))
    assert abs(shots[-1]["start"] + shots[-1]["dur"] - T["total"]) < 0.01
    md = ["# The Seven Days v2: shot list (photoreal)\n",
          "Generated by `script/storyboard.py`. Reuse and graphic shots carry no prompt.\n"]
    sb = ["# The Seven Days v2: storyboard\n", "Generated by `script/storyboard.py`.\n",
          "| Shot | Time | Length | Kind | Picture |", "|---|---|---|---|---|"]
    counts, out = {}, []
    for k, sh in enumerate(shots, 1):
        counts[sh["kind"]] = counts.get(sh["kind"], 0) + 1
        mm, ss = divmod(sh["start"], 60)
        desc = sh["scene"] or (f"reuse {sh['src']}" if sh["src"] else sh["flags"])
        sb.append(f"| {sh['id']} | {int(mm)}:{ss:04.1f} | {sh['dur']:.1f} s | {sh['kind']} | {desc} |")
        rec = dict(sh)
        if sh["kind"] in ("veo", "still"):
            p, refs = prompt_for(sh)
            keep = PR.KEEP if sh["flags"] in ("bm", "family", "pair", "man", "woman") else ""
            mp = f"{sh['scene']} {sh['motion']}{keep} {PR.MOTION}"
            assert not any(w in mp.lower() for w in BANNED), sh["id"]
            rec.update(prompt=p, refs=refs, motion=mp)
            md.append(f"### Shot {k}: {sh['id']} {sh['chapter']} ({sh['dur']:.1f} s, {sh['kind']})")
            if refs:
                md.append("- Refs: " + ", ".join(refs))
            md += ["- Image prompt:", f"  > {p}", f"- Motion: {sh['motion']}", ""]
        out.append(rec)
    (HERE / "movement-shots.json").write_text(json.dumps(
        [dict(id=s["id"], chapter=s["chapter"], n=0, start=s["start"], dur=s["dur"], picture=s["scene"] or s["picture"])
         for s in out], indent=1, ensure_ascii=False))
    (HERE / "shotlist.md").write_text("\n".join(md))
    (HERE / "shotlist.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    (HERE / "storyboard.md").write_text("\n".join(sb) + "\n")
    print(f"{len(shots)} shots {counts}; images to make: {counts.get('veo', 0) + counts.get('still', 0)}")


if __name__ == "__main__":
    main()
