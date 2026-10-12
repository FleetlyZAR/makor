#!/usr/bin/env python3
"""Storyboard and shot list for The Garden v2 (photoreal, films/CINEMA-STANDARD.md).

Built the way The Seven Days v2 storyboard is (01-the-seven-days-v2/script/storyboard.py): every
picture segment of the timeline (each PIC beat in script/movement.py) is cut into shots, fast in the
cold open, the montages and the four set pieces, longer under teaching. Shots that v1 of The Garden
already made (photoreal, approved at its C2) are reused rather than paid for again.

Kinds: veo (new keyframe, then animated), still (new keyframe with a move in the edit), reuse (an
approved keyframe from v1 or The Fall; anim=True animates it like a veo shot), graphic (built in
the edit). Prompts get the photoreal rules (films/tools/photoreal.py) and the cast references, and
are checked for banned words.

Writes script/movement-shots.json, shotlist.md (for still.py and still_batch.py), shotlist.json
(for the animation and the edit) and storyboard.md (to read).

    python3 films/genesis/02-the-garden-v2/script/storyboard.py
"""
import json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
FILM = HERE.parent
sys.path.insert(0, str(HERE.parents[3] / "films" / "tools"))
import photoreal as PR  # noqa: E402

V1 = "../02-the-garden/stills/movement/"
FALL = "../03-the-fall/stills/movement/"
SD2 = "../01-the-seven-days-v2/stills/movement/"
REF = {"adam": "stills/cast/adam.jpg", "adam_turn": "stills/cast/adam-turnaround.jpg", "eve": "stills/cast/eve.jpg",
       "bm": "stills/cast/brickmaker.jpg", "bm_turn": "stills/cast/brickmaker-turnaround.jpg",
       "wife": "stills/cast/wife.jpg", "wife_turn": "stills/cast/wife-turnaround.jpg"}
NOFIG = "No people, no figures, no faces, no silhouettes."
NOGOD = "No hands and no figure in the sky, in the light or in the wind."
NOCHRIST = "No figures at all; never a figure meant to be Christ."
DISTANT = "Any people are small and far off, faces not visible."
CAMP = ("A wilderness camp of Israel in the Sinai desert in the time of Moses: low tents of black goat hair in rows on "
        "sand and gravel, rocky desert mountains behind, cooking fires; at the centre of the camp a large tent sanctuary "
        "of woven curtains inside a courtyard fence of white linen hung on posts. No stone buildings, no towers, no "
        "statues, no carvings of figures, no domes.")
BM = ("The man is the brick-maker in the reference images, now free in the wilderness: keep his face, skin tone, curly "
      "dark hair with grey, full beard with grey at the chin and build exactly; he wears a plain undyed knee length "
      "linen tunic, clean now, no mud. Quiet, thoughtful, at peace, never grinning. Framed from the chest up or wider, "
      "never an extreme close up of the face.")
WIFE = ("The woman is the brick-maker's wife in the reference images: keep her face, skin tone, grey strands in her hair, "
        "long black braid, plain undyed linen head cloth and long undyed wool tunic exactly. Framed from the chest up "
        "or wider.")
MAN = ("The man is the man in the reference portrait: keep his face, skin tone, hair and beard exactly, but not the "
       "cloth on his shoulder. He wears nothing; he is seen from the chest up, facing the camera, in profile or from "
       "behind, or with tall grass covering him below the chest. Nothing below the chest is visible. No other people.")
WOMAN = ("The woman is the woman in the reference portrait: keep her face, skin tone and long curly hair exactly, but "
         "not the cloth on her shoulder. A head and shoulders view: her long thick hair falls forward over her bare "
         "shoulders and chest. Nothing below the shoulders is visible. No other people.")
PAIR = PR.BEFORE_FIGS
SHARP = ("Sharp focus from the foreground to the horizon: the ground or water at the bottom of the frame is crisp and "
         "detailed right to the bottom edge, with no blur, no haze, no fog, no mist band and no faded band at the bottom.")
BANNED = ["deity", "god figure", "divine being", "halo", "glowing man", "angel", "temple", "idol"]


def S(scene, kind="still", refs=(), flags="", motion="Slow push in.", w=1.0, src=None, cue=None, anim=False, verb=None,
      omni=None):
    # cue: words in the narration; the shot starts as they are spoken. verb: on screen word (Down to the ground).
    # omni: how films/tools/omni_clips.py makes a hero clip (image, morph to a last frame, or same: cut from another)
    return dict(scene=scene, kind=kind, refs=list(refs), flags=flags, motion=motion, w=w, src=src, cue=cue,
                anim=anim, verb=verb, omni=omni)


def R(src, motion="Slow push in.", w=1.0, cue=None, anim=True, verb=None, note="", omni=None):
    return S(note, "reuse", src=src, motion=motion, w=w, cue=cue, anim=anim, verb=verb, omni=omni)


def bm(scene, kind="veo", motion="Slow push in.", w=1.0, cue=None):
    return S(scene, kind, ["bm", "bm_turn"], "bm", motion, w, cue=cue)


def man(scene, kind="veo", motion="Slow push in.", w=1.0, cue=None):
    return S(scene, kind, ["adam", "adam_turn"], "man", motion, w, cue=cue)


SEG = {
    # 0 Cold open: from the finished world of The Seven Days down to one grain of dust (one continuous fall)
    0: [R(V1 + "s001.jpg", "The camera tips forward and begins to fall toward the land.", w=1.6, anim=True,
          omni=dict(mode="image", prompt=(
              "One continuous shot, the camera falling from the sky to the ground. [0-2.5s] High above a wide bay at rest "
              "in long golden light, the camera tips forward and begins to dive. [2.5-5s] Plunging fast down through "
              "white clouds, a dry river land opening below. [5-7.5s] Rushing low and fast over bare dry red brown "
              "ground at first light, the ground filling the frame. [7.5-10s] The camera slows hard and comes to rest "
              "in extreme close up on single grains of dry dust, one grain catching the light; stillness. No people, "
              "no animals, no buildings, nothing made by hands. Sound: wind rushing, then silence."))),
        S("Plunging down through white clouds in golden morning light, a dry river land opening far below.", "veo",
          motion="Fast dive down through the clouds.", w=1.6,
          omni=dict(mode="same", clip="s001", at=2.5)),
        R(V1 + "s002.jpg", "Fast descent toward the ground, slowing hard at the end.", w=1.4, anim=True,
          omni=dict(mode="same", clip="s001", at=5.0)),
        S("Extreme macro of dry dust on bare ground: individual grains of red brown earth, sharp, one grain at the centre "
          "catching first light.", "veo", motion="The fall stops dead; stillness.", w=1.4,
          omni=dict(mode="same", clip="s001", at=7.5))],
    # 1 the breath: dust lifts; hard cut to the eye opening
    1: [S("Extreme macro of dark damp dust on the ground at first light; the grains begin to lift and swirl in a low "
          "wind.", "veo", motion="A wind passes across the dust and lifts it in a swirl.", w=2.0),
        man("An extreme close view of the man's eyes, from the brow to the cheekbones only, lying on the ground in first "
            "light: his eyes opening for the first time, dew on his lashes, light in his eyes.",
            motion="His eyes open; a first breath.", w=2.0)],
    # 2 flash-forward montage (about a second a shot), then black under God's line
    2: [R(V1 + "s028.jpg", "Fast push down toward the four rivers.", anim=True),
        R(V1 + "s029.jpg", "Water moves over the gold.", anim=True),
        R(V1 + "s024.jpg", "Fast push in toward the two trees."),
        S("A lion in long golden grass in the garden, walking straight toward the camera, calm and unafraid, morning light.",
          "veo", motion="The lion walks toward the camera."),
        R(V1 + "s060.jpg", "Push in."),
        S("The woman's face in morning light among garden leaves, three quarter view, from the brow to the chin, her long "
          "dark curly hair framing her face, calm and full of wonder.", "veo", ["eve"], "woman",
          motion="She turns her face toward the camera."),
        S("Two bare hands reaching toward each other and meeting, fingers interlacing, in warm morning light: on the left "
          "the man's hand, deep dark brown skin exactly like the man in the first reference image, on the right the "
          "woman's hand, warm dark olive brown skin exactly like the woman in the second reference image; neither hand "
          "is pale or light skinned. "
          "morning light against blurred green leaves; only the bare hands and bare forearms in the frame, no sleeves, "
          "no clothing, no watch, no rings, no jewellery.", "veo", ["adam", "eve"],
          motion="The hands meet and hold."),
        S("", "graphic", flags="black: God's line, 'It is not good for the man to be alone.' (made in the edit)", w=5.0)],
    # 3 the camp at night; the hook; title over dry ground
    3: [S(f"Night in the wilderness camp under countless stars: rows of black goat hair tents, and at the centre the tent "
          f"sanctuary in its white linen courtyard, fire and smoke rising before its gate. {CAMP}", "veo", flags="distant",
          motion="Slow push over the camp toward the sanctuary."),
        bm("Night: he sits at the door of his goat hair tent with his forearms on his knees, firelight on his face, "
           "looking across the camp toward the sanctuary's fire. " + CAMP, motion="Very slow push in."),
        S(f"The gate of the tent sanctuary at night from across the camp: the courtyard's white linen walls glowing with "
          f"firelight, smoke rising into the stars, the gate facing east. {CAMP}", "still", flags="distant"),
        bm("Close: his face in the firelight, chest up, eyes on the sanctuary, thinking. " + CAMP,
           motion="Very slow push in.", cue="They would have noticed"),
        R(V1 + "s002.jpg", "Very slow push.", note="title: THE GARDEN / Genesis 2:4 to 25", cue="It looks like one")],
    # 4 Down to the ground (2:4): the heavens to the earth
    4: [R(V1 + "s003.jpg", "Slow descent."), R(V1 + "s004.jpg", "Slow descent.", cue="when they were created"),
        R(V1 + "s007.jpg", "Slow push.", cue="Listen to the turn"),
        R(V1 + "s006.jpg", "The camera settles at ground level.", cue="the camera comes down", anim=True)],
    # 5 the nine verbs on screen over the film's own shots; then the close up of day six
    5: [R(V1 + "s008.jpg", "Slow push."), R(V1 + "s005.jpg", "Slow push.", cue="In chapter one He speaks"),
        R(V1 + "s010.jpg", "Slow push down toward the ground.", cue="Here He stoops"),
        R(V1 + "s016.jpg", verb="FORMS", cue="He forms"), R(V1 + "s019.jpg", verb="BREATHES", cue="breathes,"),
        R(V1 + "s023.jpg", verb="PLANTS", cue="plants,"), R(V1 + "s036.jpg", verb="TAKES", cue="takes,"),
        R(V1 + "s037.jpg", verb="PLACES", cue="places,"), R(V1 + "s040.jpg", verb="COMMANDS", cue="commands,"),
        R(V1 + "s054.jpg", verb="BRINGS", cue="brings,"), R(V1 + "s060.jpg", verb="CLOSES", cue="closes and"),
        R(V1 + "s065.jpg", verb="BUILDS", cue="builds"),
        R(V1 + "s009.jpg", "Slow push.", cue="This is not a second"), R(V1 + "s022.jpg", "Slow push.", cue="close up of the sixth")],
    # 6 Dust and breath: lack; springs
    6: [R(V1 + "s011.jpg", "Slow push."), R(V1 + "s012.jpg", "Slow push.", cue="nor had any plant"),
        R(V1 + "s006.jpg", "Slow push.", cue="had not yet sent rain"),
        R(V1 + "s013.jpg", "Water spreads over the dust.", cue="But springs", anim=True),
        S("Macro: clear spring water spreading in thin ribbons through dry red brown dust, darkening it, tiny bubbles "
          "rising, first light.", "veo", motion="The water creeps across the dust.", cue="The scene opens"),
        R(V1 + "s014.jpg", "Slow push.", cue="rain, and no man"),
        S("Macro: single drops of water falling into damp dust, each one darkening a small circle, silence.", "veo",
          motion="Drops fall into the dust.", cue="Every lack")],
    # 7 SET PIECE 1: the forming and the breath
    7: [R(V1 + "s015.jpg", "The dust whirls and gathers.", anim=True),
        S("Low at ground level at dawn on a wide plain of damp red brown earth with tall grass at its edges: a long low "
          "drift of loose damp dust lying on the ground, the length and outline of a man lying on his back, still only "
          "earth, a thin whirl of dust lifting around it, soft warm light across it. No rocks, no boulders, no mound of "
          "stone, no hill, no hands, no figure above it.", "veo",
          motion="The dust settles into the shape; wind moves over it.", cue="formed man from the dust",
          omni=dict(mode="morph", last=V1 + "s016.jpg", prompt=(
              "One continuous shot, low at ground level at dawn. [0-4s] A low whirling wind draws loose damp dust together "
              "on the ground into the long outline of a man lying on his back; the earth gathers and settles. [4-8s] "
              "Grass rises around it and the shape of dust becomes a man lying still in deep grass, seen from the side, "
              "the grass covering him below the chest. [8-10s] Stillness; soft warm light. No hands and no figure above "
              "him, nothing in the sky; the wind is the only cause. Nothing below his chest is ever visible. "
              "Sound: low wind, then silence."))),
        R(V1 + "s016.jpg", "Slow push in.", cue="breathed the breath", anim=True,
          omni=dict(mode="same", clip="s046", at=6.3)),  # the forming and the man in the grass are one take
        S("Wind rushing low across tall grass toward the camera at first light, the grass bending in one long wave.", "veo",
          motion="A single strong gust sweeps across the grass toward the camera.", w=0.8),
        man("Lying on his back in deep grass at first light, seen from the side at head and shoulder height, his chest "
            "rising with his first deep breath, eyes open to the sky.", motion="His chest rises; a first deep breath.", w=1.2),
        S("Close: the hand of the man in the reference portrait: deep dark brown skin exactly like his face, never pale, never light skinned; a bare hand lying on dark earth closing slowly around a handful of soil, grass around it, first "
          "light; only the bare hand and bare forearm in the frame, no sleeve, no clothing, no watch, no rings.", "veo", ["adam"], motion="The fingers close on the earth."),
        man("Close, chest up: his face as first light moves across it, eyes wide in wonder, breathing.",
            motion="Light crosses his face; he breathes.", w=1.2),
        R(V1 + "s019.jpg", "Slow push.", anim=True),
        R(V1 + "s021.jpg", "Wind moves over the grass.", w=1.2, anim=True)],
    # 8 the brick-maker's hands in dust; the potter; clay servants; adam and adamah
    8: [bm("By day in the wilderness camp he kneels on the sand and lets dry dust run through his fingers, looking at it. "
           + CAMP, motion="The dust runs through his fingers."),
        S("Close: a man's work scarred hands letting dry desert dust run through the fingers in the sun; only the hands "
          "in the frame.", "veo", motion="Dust pours from the hands.", cue="hands shaping clay"),
        R(V1 + "s018.jpg", "The wheel turns slowly.", cue="we are the clay", anim=True),
        R(SD2 + "s027.jpg", "Slow push.", cue="The nations also told"),
        R(V1 + "s023.jpg", "Slow push.", cue="Genesis is different"),
        R(V1 + "s020.jpg", "Slow push.", cue="Man, adam"),
        R(V1 + "s014.jpg", "Slow push.", cue="We are earthy creatures"),
        R(V1 + "s021.jpg", "Wind moves over the grass.", cue="the breath of the Almighty", anim=True)],
    # 9 a garden in the east: growth montage (2 to 3 s), then the two trees
    9: [S("Time-lapse at ground level: green shoots breaking up through dark damp earth at first light.", "veo",
          motion="The shoots push up out of the soil.", w=0.8),
        S("One single full frame photograph, not a sequence, no panels: a young fig tree with broad unfurling leaves "
          "standing alone on bare open ground in a wide green valley in the east, morning sun; no walls, no buildings.", "veo",
          motion="The tree grows and its leaves open.", w=0.8),
        S("Time-lapse: young trees rising across a wide valley in the east, the land turning green.", "veo",
          motion="The trees rise.", w=0.8),
        S("Close: figs swelling and ripening on the branch, dew, warm light, blurred fig leaves and trees behind; no walls, "
          "no stones, nothing made by hands. One single continuous full frame image.", "veo", motion="The fruit swells.",
          cue="every tree that is pleasing", w=0.7),
        S("Close: pomegranates ripening red gold on the branch in warm light.", "still", w=0.7),
        S("Close: heavy clusters of dates ripening on a date palm against the sky.", "still", w=0.7),
        S("Close: grape clusters ripening on the vine, sun through the leaves.", "still", w=0.7),
        R(V1 + "s023.jpg", "Slow rise over the garden.", cue="good for food", anim=True),
        R(V1 + "s024.jpg", "Slow push toward the two trees.", cue="And in the middle", anim=True),
        R(V1 + "s025.jpg", "Slow push.", cue="Eden means delight"),
        R(V1 + "s026.jpg", "Slow push.", cue="Notice the two trees"),
        R(V1 + "s024.jpg", "Very slow push.", cue="with the man, the woman")],
    # 10 SET PIECE 2 begins: the river
    10: [R(V1 + "s027.jpg", "Slow push along the river.", anim=True),
         S("Flying fast and low just above a clear river through a green garden, trees blurring past on both banks, "
           "the water sparkling below.", "veo", motion="Fast flight along the river just above the water."),
         S("Climbing up from the river into the sky as it splits below into four great headwaters, the land spreading "
           "out to the horizon.", "veo", motion="The camera climbs and the four rivers appear.")],
    # 11 the four rivers named; the set piece's peak; the teaching
    11: [S("From the air, a broad river winding through a land of ochre hills and pale sand in the east, gold glinting "
           "in its bed, early light.", "veo", motion="Slow flight following the river."),
         R(V1 + "s029.jpg", "Water moves over the gold.", cue="And the gold of that land", anim=True),
         R(V1 + "s030.jpg", "Slow push along the river.", cue="the Gihon", anim=True),
         R(V1 + "s031.jpg", "Slow push.", cue="the Tigris"),
         R(V1 + "s028.jpg", "A slow rise high above the four rivers.", cue="And the fourth river", anim=True),
         S("Sweeping aerial over two great rivers converging across a vast green plain at golden light, the camera "
           "banking.", "veo", motion="A great banking aerial sweep.", w=1.2),
         S("From very high above at golden evening light, the four great rivers running out across a vast land toward "
           "four horizons, shining like threads of gold.", "veo", motion="A very slow rise; the rivers shine."),
         R(V1 + "s033.jpg", "Mist drifts over the water.", anim=True),
         R(V1 + "s032.jpg", "Very slow push.", cue="The geography is deliberately"),
         R(V1 + "s031.jpg", "Slow push.", cue="Every Israelite knew"),
         R(V1 + "s030.jpg", "Slow push.", cue="cannot be identified"),
         S("High on a mountain at first light, a great spring pouring from the rock and running down in streams that "
           "spread out over the land below.", "veo", motion="The water pours and spreads.", cue="the dwelling of a god"),
         R(V1 + "s027.jpg", "Slow push.", cue="Here a river flows out")],
    # 12 the sanctuary turn: the camp at sunrise
    12: [bm("Sunrise in the camp: he walks between the goat hair tents toward the tent sanctuary at the centre, seen from "
            "behind and to the side. He wears one long plain undyed tunic falling below his knees to mid calf, belted "
            "with a cord, and a plain cloak over his shoulders; no shorts, no trousers, no separate garment on his legs. "
            + CAMP, motion="He walks toward the sanctuary."),
         S(f"The gate of the tent sanctuary's courtyard facing east straight into the rising sun, its curtain of blue, "
           f"purple and scarlet woven linen lit by the sunrise. {CAMP}", "veo", motion="The sun rises behind the camera; "
           "light floods into the gate.", cue="Its entrance faces east"),
         S("Inside the courtyard at sunrise: gold catching the light on the posts and furnishings of the tent sanctuary, "
           "polished bronze basin, smoke from the altar.", "still", flags="distant", cue="Gold and onyx"),
         S("Close on the shoulders of a priest of Israel seen from behind and to the side: on each shoulder of his woven "
           "gold, blue and scarlet garment, a large dark onyx stone set in gold, engraved with rows of ancient Hebrew "
           "letters; his face not visible. One single continuous full frame image with the sky and camp behind.", "still", flags="distant", cue="two onyx stones"),
         S("Inner curtains of fine woven linen in blue, purple and scarlet thread, embroidered with stylised palm trees "
           "and open flowers, ancient Near Eastern weaving, lit by lamplight; no figures, no creatures, no faces, no "
           "wings.", "still",
           cue="God walks in the garden"),
         S(f"From a rocky rise at dawn, the whole camp below: thousands of tents in ordered rows around the tent "
           f"sanctuary at the centre, smoke rising, people small and far off moving between the tents. {CAMP}", "veo",
           flags="distant", motion="Slow rise over the camp.", cue="I will walk among you"),
         R(V1 + "s034.jpg", "Slow push into the opening between the trees.", cue="Israel's worship", anim=True)],
    # 13 to cultivate and keep: Adam at work; the Levite
    13: [R(V1 + "s037.jpg", "Slow push.", anim=True),
         man("In the garden at first light he tends a grapevine, lifting a heavy branch onto a living trellis of young "
             "trees, seen from the chest up at medium distance among the leaves.", motion="He lifts the vine."),
         R(V1 + "s038.jpg", "Slow push.", cue="Cultivate and keep"),
         S("Close: the hands of the man in the reference portrait: deep dark brown skin exactly like his face, never pale, never light skinned; bare hands pressing dark soil firmly around a young fig seedling in the garden at first light; "
           "only the bare hands and bare forearms, no sleeves, no clothing, no watch, no rings.", "still", ["adam"],
           cue="the ordinary word for serving God"),
         S(f"In the courtyard of the tent sanctuary at first light a Levite in a plain white linen tunic tends the altar "
           f"fire, adding wood, seen from the side at medium distance, his face turned away. {CAMP}", "veo",
           flags="distant", motion="He lays wood on the fire.", cue="The second means"),
         S(f"A Levite in a white linen tunic stands guard at the gate of the sanctuary courtyard with a staff, seen "
           f"from behind at medium distance, the camp beyond. {CAMP}", "still", flags="distant",
           cue="Together they describe"),
         R(V1 + "s036.jpg", "Slow push.", cue="Adam's work is farming", anim=True),
         R(V1 + "s024.jpg", "Slow push toward the two trees.", cue="A keeper of a sanctuary", anim=True)],
    # 14 one word: the tree; God's command; the teaching
    14: [R(V1 + "s040.jpg", "Wind moves through the leaves.", anim=True),
         man("Seen from behind at long distance, small, standing in tall grass before the great tree at the centre of "
             "the garden, the tree filling the frame above him.", motion="Wind moves through the tree; he stands still.",
             cue="commanded him"),
         R(V1 + "s046.jpg", "Wind moves through the leaves.", cue="You may eat freely", anim=True),
         R(V1 + "s044.jpg", "Very slow push.", cue="but you must not"),
         R(V1 + "s042.jpg", "Slow push.", cue="Listen to the order"),
         R(V1 + "s043.jpg", "Slow push.", cue="only then sets one limit"),
         R(V1 + "s046.jpg", "Leaves move.", cue="God's commands are not", anim=True),
         R(V1 + "s041.jpg", "Slow push.", cue="And the warning is plain"),
         R(V1 + "s026.jpg", "Slow push.", cue="His word defines"),
         R(V1 + "s045.jpg", "The shadow lengthens.", cue="life depends", anim=True),
         S("Close: one heavy fruit hanging on the great tree, leaves moving around it in the wind, beautiful, nothing "
           "glowing.", "veo", motion="The leaves move in the wind; the fruit sways a little.", cue=None, w=0.8),
         R(V1 + "s044.jpg", "Very slow push.", cue="Whatever the knowledge"),
         R(V1 + "s040.jpg", "Very slow push.", cue="or seize it"),
         R(V1 + "s025.jpg", "Slow push.", cue="So the garden has everything"),
         R(V1 + "s048.jpg", "Slow push.", cue="And then God Himself")],
    # 15 not good: the man alone; ezer
    15: [R(V1 + "s049.jpg", "Very slow pull back.", anim=True),
         R(V1 + "s050.jpg", "Slow push.", cue="It is not good"),
         R(V1 + "s047.jpg", "Slow push.", cue="The first thing in the Bible"),
         R(V1 + "s051.jpg", "Slow push.", cue="Helper is ezer"),
         R(V1 + "s052.jpg", "Light rises over the hills.", cue="My help comes", anim=True),
         R(V1 + "s053.jpg", "Slow push.", cue="Suitable means")],
    # 16 the naming: driving montage (2 to 3 s); stops on the man alone
    16: [R(V1 + "s054.jpg", "Slow push.", anim=True, w=0.8),
         S("A lion walking through tall golden grass in the garden toward the camera, unafraid, morning light.", "veo",
           motion="The lion walks forward.", w=0.7),
         S("A herd of gazelle bounding across a wide open green meadow in the garden, fruit trees all around, morning "
           "light; no buildings, no walls, no paths.", "veo",
           motion="The gazelle run across the frame.", w=0.7),
         R(V1 + "s056.jpg", "Slow push.", anim=True, w=0.8),
         S("A great eagle landing on a branch of a fruit tree, wings spread wide.", "veo", motion="The eagle lands and "
           "folds its wings.", w=0.7),
         R(V1 + "s055.jpg", "Birds land.", anim=True, w=0.7),
         S("A Syrian brown bear walking slowly out of the trees into a meadow in the garden, calm.", "veo",
           motion="The bear walks forward.", w=0.7, cue="The man gave names"),
         S("A pair of turtle doves on a branch, side by side, morning light.", "still", w=0.6),
         man("Chest up, three quarter view: he looks at something before him and speaks a name, attentive, grass "
             "around his shoulders.", motion="He speaks.", w=0.8),
         S("Wild aurochs cattle and Nubian ibex walking in pairs across a meadow in the garden.", "veo",
           motion="The animals walk across the frame.", w=0.7),
         R(V1 + "s057.jpg", "Slow push.", w=0.8, cue="But for Adam"),
         R(V1 + "s058.jpg", "Very slow pull back.", cue="God brings the animals", anim=True)],
    # 17 the deep sleep; the builder's word
    17: [R(V1 + "s062.jpg", "Stars wheel slowly.", anim=True),
         R(V1 + "s059.jpg", "Very slow push.", cue="while he slept"),
         R(V1 + "s060.jpg", "The soft light gathers.", cue="from the rib", anim=True),
         R(V1 + "s061.jpg", "Slow push.", cue="The deep sleep is the same"),
         R(V1 + "s062.jpg", "Very slow push.", cue="God works while"),
         S(f"Night in the wilderness camp: the framework of the tent sanctuary being raised, upright boards of acacia wood "
           f"overlaid with gold standing side by side in silver bases, lamplight on them, no people. {CAMP}", "still",
           cue="Rib can mean side"),
         R(V1 + "s063.jpg", "Dawn light grows.", cue="God builds the woman", anim=True)],
    # 18 SET PIECE 3: the woman brought to the man; his words
    18: [S("Morning light breaking through the trees of the garden in long shafts, dew shining, birds lifting.", "veo",
           motion="The light grows through the trees."),
         S("The woman walking through the garden toward the camera in morning light among fruit trees, seen from the "
           "shoulders up at medium distance, her long thick dark curly hair falling over her shoulders and chest.", "veo",
           ["eve"], "woman", motion="She walks slowly forward through the trees."),
         man("He wakes beneath the great tree and sits up in the deep grass, seen in profile from the chest up, turning "
             "toward the light.", motion="He wakes, sits up and turns."),
         man("Chest up, facing the camera: his face as he sees her for the first time, wonder and joy breaking over it.",
             motion="His face changes as he sees her."),
         S("Head and shoulders, three quarter view: her face as she sees him, calm and glad, morning light, long hair "
           "over her shoulders.", "veo", ["eve"], "woman", motion="A slow smile."),
         S("The man and the woman face to face in profile, close but not touching, seen from the shoulders up, morning "
           "light between them, garden leaves behind.", "veo", ["adam", "eve"], "pair", motion="They look at each other."),
         R(V1 + "s064.jpg", "Very slow push.", cue="This is now bone", anim=True),
         R(V1 + "s065.jpg", "Slow push.", cue="for out of man"),
         R(V1 + "s066.jpg", "Slow push.", cue="These are the first recorded"),
         R(V1 + "s068.jpg", "Slow push.", cue="Bone of my bones is")],
    # 19 one flesh: the brick-maker's home
    19: [S("Evening in the wilderness camp: the brick-maker and his wife sit together at the door of their goat hair tent, "
           "side by side, the sanctuary's fire far beyond. " + BM + " " + WIFE + " " + CAMP, "veo",
           ["bm", "wife"], "family", motion="Very slow push in."),
         S("Inside a goat hair tent by lamplight, two small children asleep under a woven blanket, faces turned away.",
           "still", cue="The narrator steps out"),
         S("Close, chest up, filling the frame: her face in the evening light at the tent door, looking toward her husband "
           "off camera; no other person in the frame. " + WIFE + " " + CAMP, "veo",
           ["wife", "wife_turn"], "wife", motion="Very slow push in.", cue="the word Ruth uses"),
         S("Close: his hand resting over hers on her knee in the firelight; only the hands and forearms, his plain undyed "
           "linen sleeve and her plain undyed smooth woven wool sleeve, no knit pattern, no rings.", "veo", motion="His hand closes over hers.", cue="Hold fast to Him"),
         R(V1 + "s067.jpg", "Slow push.", cue="Marriage is a loyalty"),
         R(SD2 + "s128.jpg", "Very slow push.", cue="This chapter was written")],
    # 20 naked and not ashamed; the turn
    20: [R(V1 + "s070.jpg", "Slow push.", anim=True), R(V1 + "s071.jpg", "Slow rise.", cue="not ashamed"),
         S("Dusk at the foot of the great tree in the middle of the garden: the tall grass at its roots stirs and parts "
           "as something unseen moves through it; long shadows.", "veo", motion="The grass at the foot of the tree "
           "stirs and parts, then is still."),
         R(V1 + "s072.jpg", "Very slow push.", cue="Naked, and not ashamed"),
         R(V1 + "s069.jpg", "Very slow push.", cue="Every gift")],
    # 21 the last Adam: the gardens of the passion; the tomb; the breath
    21: [R(V1 + "s073.jpg", "Slow push.", anim=True),
         S("An olive grove on a hillside at night under a full moon, old twisted trees, and torches moving between the "
           "trees far off, carried by small distant figures, faces not visible.", "veo", flags="distant",
           motion="The torches move through the grove.", cue="The first man Adam"),
         R(V1 + "s076.jpg", "Slow push.", cue="Adam was placed"),
         R(V1 + "s075.jpg", "Slow push.", cue="He failed at every point"),
         R(V1 + "s077.jpg", "Slow push toward the open tomb.", cue="Jesus is arrested", anim=True),
         R(V1 + "s078.jpg", "Very slow push.", cue="Mary thinks"),
         S("Sunrise in the garden of the tomb: light flooding along the stone path out of the open tomb, the grass and "
           "leaves bending in a sudden wind. No figures.", "veo", flags="christ",
           motion="Light floods out; wind sweeps through the garden."),
         R(V1 + "s074.jpg", "Wind in the olive leaves.", anim=True),
         R(V1 + "s079.jpg", "Slow push.", cue="That evening"),
         R(V1 + "s080.jpg", "Slow push.", cue="Receive the Holy Spirit"),
         R(V1 + "s081.jpg", "Slow push.", cue="And Paul says"),
         R(V1 + "s068.jpg", "Slow push.", cue="I am speaking about Christ")],  # two vines grown into one (v1 s082 has a spired city)
    # 22 dark flash-forward to chapter three; the prophets' promise in the wilderness
    22: [R(FALL + "s060.jpg", "Fast push.", anim=True, w=0.8),
         S("Close: a man's bare scratched hands tearing at thorn bushes in hard cracked ground, dust and sweat, no tools, "
           "no metal; only the bare hands and forearms. One single continuous full frame image.", "veo", motion="The hands strike the hard ground.", w=0.8),
         R(FALL + "s079.jpg", "The sword of flame turns.", anim=True, w=0.8),
         R(V1 + "s084.jpg", "Slow pull back.", cue="and the way to the tree"),
         bm("At the edge of the camp at dusk he stands looking out over the empty desert, seen from the side, wind in his "
            "tunic. " + CAMP, motion="Very slow push in.", cue="But the prophets"),
         S("One single continuous full frame image, no panels, no split, no grid. A dry desert valley breaking into green, grass and flowers spreading over the sand after rain, "
           "water running in the wadi.", "veo", motion="The desert turns green.", cue="will make her wilderness")],
    # 23 SET PIECE 4: Eden restored
    23: [S("Before dawn, no sun in the sky, the light coming from the city itself: the radiant city of the new creation, its pale gold stone shining from within as if lit by gold and crystal, warm light pouring from every doorway and along the street, seen along its great street: a clear river flowing down the middle of the "
           "street, fruit trees on both banks, a vast square city of pale gold stone glowing with its own light, low flat roofed buildings of the ancient Near East, no towers, no spires, no pinnacles, no arches reaching up, no cathedral, no domes, no castle, no modern or European architecture.", "veo", motion="Slow rise toward the city."),
         S("Before dawn, no sun in the sky, the light coming from the city itself. Close at the riverbank: one great tree of life beside the clear river in the city, heavy with fruit, its leaves lit warmly from the shining city behind, "
           "catching the light, its roots at the water; behind it, softly out of focus, a vast square city of pale gold stone glowing with its own light, low flat roofed buildings of the ancient Near East, no towers, no spires, no pinnacles, no arches reaching up, no cathedral, no domes, no castle, no modern or European architecture.", "veo",
           motion="Leaves move; the river flows.", cue="The river of the water of life"),
         R(V1 + "s087.jpg", "The river shines.", cue="eat from the tree of life", anim=True),
         S("Full frame with no black bars. A great aerial rise over the city of light: a clear river running through its centre between groves of the "
           "tree of life, the city of pale gold stone glowing with its own light, low flat roofed buildings of the "
           "ancient Near East, no towers, no spires, no domes, no castle, no modern or European architecture.", "veo",
           motion="A slow great aerial rise over the city."),
         S("Close at the riverbank in the city of light: leaves of the tree of life moving over the clear water, fruit "
           "hanging in the light; behind, only more trees of life and soft glowing light, no bridge, no buildings, no "
           "European architecture.", "veo", motion="Leaves move over the water."),
         S("Wide at golden light: the garden city, the clear river winding through groves of fruit trees on both banks, "
           "and beyond them a vast square city of pale gold stone glowing with its own light, low flat roofed buildings of the ancient Near East, no towers, no spires, no pinnacles, no arches reaching up, no cathedral, no domes, no castle, no modern or European architecture.", "veo", motion="Slow push."),
         S("Dawn over the garden from a rise: groves of fruit trees and a river winding toward the horizon, and far beyond "
           "them, small and shining, a vast square city of pale gold stone glowing with its own light, low flat roofed "
           "buildings of the ancient Near East, no towers, no spires, no pinnacles, no cathedral, no domes, no castle.",
           "veo", motion="Slow push toward the city.", cue="The garden has become a city")],
    # 24 dust that breathes
    24: [R(V1 + "s089.jpg", "A breath of wind lifts the dust.", anim=True),
         bm("At dawn in the camp he opens his hand and the wind lifts the dust from his palm. " + CAMP,
            motion="The dust lifts from his palm.", cue="Every good gift"),
         R(V1 + "s090.jpg", "Wind moves over the grass.", cue="You were formed", anim=True),
         R(V1 + "s091.jpg", "Dawn light spreads.", cue="change how you see")],
    # 25 open loop into The Fall; end card
    25: [S("The great tree in the middle of the garden at dusk, the light going; at its foot the grass moves as something "
           "unseen passes through it.", "veo", motion="The grass at the foot of the tree moves; then stillness.", w=1.4),
        R(V1 + "s072.jpg", "Very slow push.", cue="In the next chapter"),
         S("", "graphic", flags="end card: Study The Garden, makor.co.za/genesis/the-garden; WATCH NEXT The Fall",
           cue="Study The Garden", w=1.0)],
}


def _orig():
    out = {}
    for pre, f in ((V1, "../02-the-garden/script/shotlist.json"), (FALL, "../03-the-fall/script/shotlist.json"),
                   (SD2, "../01-the-seven-days-v2/script/shotlist.json")):
        for x in json.loads((FILM / f).read_text()):
            out[pre + x["id"] + ".jpg"] = dict(scene=x.get("scene") or "", flags=x.get("flags") or "")
    return out


ORIG = _orig()


PEOPLE = {"man", "woman", "pair"}
STILL_PEOPLE = {   # shot: LTX motion, with the clip's last frame locked to the keyframe (clip review, 11 October)
    "s103": "He stands still among the trees, seen from behind; only the wind moves the leaves and the grass. He does not walk.",
    "s120": "He stands still at evening, seen from behind; only the wind moves the leaves. He does not walk or turn.",
    "s126": "The animals walk slowly across the meadow; the man stands still in the tall grass, far off. He does not walk.",
    "s147": "He sits in the deep grass beneath the tree and turns his head toward the light; he does not stand up.",
    "s149": "She turns her face slowly toward the light and smiles a little; no other people, nobody else appears.",
}
CALM = {"s041": "Clear spring water seeps up and spreads slowly over the dust, darkening it; gentle mist; no spray, no "
                "steam jets, no spouts."}


def prompt_for(sh):
    f = sh["flags"]
    if f == "pair":
        who = PAIR + " " + PR.NEAR_EAST
    elif f == "woman":
        who = WOMAN + " " + PR.NEAR_EAST
    elif f == "man":
        who = MAN + " " + PR.NEAR_EAST
    elif f == "bm":
        who = BM + " No other people close to the camera."
    elif f == "wife":
        who = "No other people close to the camera."
    elif f == "family":
        who = "No other people close to the camera."
    elif f == "distant":
        who = DISTANT
    elif f == "christ":
        who = NOCHRIST
    else:
        who = NOFIG
    refs = [REF[r] for r in sh["refs"]]
    p = f"{sh['scene']} {who} {NOGOD}{PR.REFNOTE if refs else ''} {PR.SUFFIX} {SHARP}"
    low = p.lower() + sh["motion"].lower()
    for w in BANNED:
        assert w not in low, f"banned word {w!r} in: {sh['scene'][:60]}"
    assert "–" not in p and "—" not in p
    return p, refs


def cue_time(T, durs, words, a, b):
    for e in T["events"]:
        if a - 0.01 <= e["t"] < b and e["kind"] in ("line", "card") and words.lower() in e["text"].lower():
            if e["kind"] == "card":
                return e["t"]
            k = e["text"].lower().index(words.lower())
            return e["t"] + durs.get(e["id"], 0) * k / max(1, len(e["text"]))
    raise SystemExit(f"cue not found in its segment: {words!r}")


def main():
    T = json.loads((HERE / "movement-timeline.json").read_text())
    durs = json.loads((HERE / "movement-durations.json").read_text())
    pics = [e for e in T["events"] if e["kind"] == "pic"]
    assert len(pics) == len(SEG), f"{len(pics)} picture segments, {len(SEG)} in SEG"
    shots, n = [], 0
    for i, e in enumerate(pics):
        end = pics[i + 1]["t"] if i + 1 < len(pics) else T["total"]
        segs = SEG[i]
        starts = [None] * len(segs)
        starts[0] = e["t"]
        for k, s in enumerate(segs):
            if s.get("cue") and k:
                starts[k] = cue_time(T, durs, s["cue"], e["t"], end)
        bounds = [k for k in range(len(segs)) if starts[k] is not None] + [len(segs)]
        times = starts + [end]
        for a, b in zip(bounds, bounds[1:]):
            t0, t1 = times[a], times[b]
            assert t1 > t0, f"cues out of order in segment {i}: {[(s.get('cue'), round(x,1) if x else x) for s, x in zip(segs, starts)]}"
            tot = sum(s["w"] for s in segs[a:b])
            for k in range(a, b):
                starts[k] = t0
                t0 += (t1 - times[a]) * segs[k]["w"] / tot
        for k, s in enumerate(segs):
            n += 1
            d = (starts[k + 1] if k + 1 < len(segs) else end) - starts[k]
            assert d > 0.4, f"s{n:03d} only {d:.2f} s"
            shots.append(dict(id=f"s{n:03d}", chapter=e["chapter"], start=round(starts[k], 3), dur=round(d, 3),
                              picture=e["text"], **s))
    assert abs(shots[-1]["start"] + shots[-1]["dur"] - T["total"]) < 0.01
    md = ["# The Garden v2: shot list (photoreal)\n",
          "Generated by `script/storyboard.py`. Reuse and graphic shots carry no prompt.\n"]
    sb = ["# The Garden v2: storyboard\n", "Generated by `script/storyboard.py`.\n",
          "| Shot | Time | Length | Kind | Picture |", "|---|---|---|---|---|"]
    counts, out = {}, []
    for k, sh in enumerate(shots, 1):
        counts[sh["kind"]] = counts.get(sh["kind"], 0) + 1
        mm, ss = divmod(sh["start"], 60)
        desc = sh["scene"] or (f"reuse {sh['src']}" if sh["src"] else sh["flags"])
        if sh["kind"] == "reuse" and sh["scene"]:
            desc = f"reuse {sh['src']} ({sh['scene']})"
        if sh["verb"]:
            desc += f" + on screen {sh['verb']}"
        sb.append(f"| {sh['id']} | {int(mm)}:{ss:04.1f} | {sh['dur']:.1f} s | {sh['kind']}{' anim' if sh['anim'] else ''} | {desc} |")
        rec = dict(sh)
        if sh["kind"] in ("veo", "still"):
            p, refs = prompt_for(sh)
            keep = PR.KEEP if sh["flags"] in ("bm", "family", "pair", "man", "woman", "wife") else ""
            mp = f"{sh['scene']} {sh['motion']}{keep} {PR.MOTION}"
            assert not any(w in mp.lower() for w in BANNED), sh["id"]
            rec.update(prompt=p, refs=refs, motion=mp)
            md.append(f"### Shot {k}: {sh['id']} {sh['chapter']} ({sh['dur']:.1f} s, {sh['kind']})")
            if refs:
                md.append("- Refs: " + ", ".join(refs))
            md += ["- Image prompt", f"> {p}", f"- Motion: {sh['motion']}", ""]
        elif sh["kind"] == "reuse":
            assert (FILM / sh["src"]).exists(), f"missing {sh['src']}"
            # the whole scene from the shot list that made the image (CINEMA-STANDARD animation rule 2), and its flags
            orig = dict(ORIG.get(sh["src"], {}))
            f = orig.get("flags", "")
            orig["flags"] = "pair" if "woman" in f else "man" if "people" in f else "" if "nofig" in f or not f else f
            keep = PR.KEEP if orig.get("flags") in ("pair", "man", "woman", "bm", "family") else ""
            rec.update(motion=f"{orig.get('scene', '')} {sh['motion']}{keep} {PR.MOTION}".strip(),
                       flags=orig.get("flags", ""))
        if rec["id"] in STILL_PEOPLE or rec["id"] in CALM:
            rec["ltx_prompt"] = (STILL_PEOPLE.get(rec["id"]) or CALM[rec["id"]]) + " " + PR.MOTION
        if rec.get("flags") in PEOPLE:
            rec["lock"] = True
        out.append(rec)
    (HERE / "movement-shots.json").write_text(json.dumps(
        [dict(id=s["id"], chapter=s["chapter"], n=0, start=s["start"], dur=s["dur"], picture=s["scene"] or s["picture"])
         for s in out], indent=1, ensure_ascii=False))
    (HERE / "shotlist.md").write_text("\n".join(md))
    (HERE / "shotlist.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    (HERE / "storyboard.md").write_text("\n".join(sb) + "\n")
    new = counts.get("veo", 0) + counts.get("still", 0)
    print(f"{len(shots)} shots {counts}; new images: {new}; reused animated: {sum(1 for s in out if s['anim'])}")


if __name__ == "__main__":
    main()
