#!/usr/bin/env python3
"""Storyboard and shot list for The Fall v2 (photoreal, films/CINEMA-STANDARD.md).

Built the way The Garden v2 storyboard is (02-the-garden-v2/script/storyboard.py): every picture
segment of the timeline (each PIC beat in script/movement.py) is cut into shots, fast in the cold open,
the montage and the five set pieces, longer under teaching. Approved photoreal keyframes from The Fall
v1 and The Garden v2 are reused rather than paid for again; dust to dust plays The Garden v2's own
clips backward.

Kinds: veo (new keyframe, then animated), still (new keyframe with a move in the edit), reuse (an
approved keyframe; anim=True animates it), graphic (built in the edit). A cue is either words in the
narration (the shot starts as they are spoken) or a number, seconds from the start of the segment (for
shots inside silent set pieces). clip and reverse: reuse an existing clip, played backward if reverse.
verb: words on screen. omni: a hero take for films/tools/omni_clips.py.

Framing (TREATMENT.md D2): before 3:7 nothing worn, faces, hands and shoulders only, nothing that walks;
from 3:7 fig leaves, chest up, in place; from 3:21 hides, full figures may walk. Cherubim (D3) as
Ezekiel describes them. Christ never shown (D6).

Writes script/movement-shots.json, shotlist.md, shotlist.json and storyboard.md.

    python3 films/genesis/03-the-fall-v2/script/storyboard.py
"""
import json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
FILM = HERE.parent
sys.path.insert(0, str(HERE.parents[3] / "films" / "tools"))
import photoreal as PR  # noqa: E402

F1 = "../03-the-fall/stills/movement/"
G2 = "../02-the-garden-v2/stills/movement/"
G2C = "../02-the-garden-v2/clips/"
REF = {"adam": "stills/cast/adam.jpg", "adam_turn": "stills/cast/adam-turnaround.jpg", "eve": "stills/cast/eve.jpg",
       "bm": "stills/cast/brickmaker.jpg", "bm_turn": "stills/cast/brickmaker-turnaround.jpg"}
NOFIG = "No people, no figures, no faces, no silhouettes."
NOGOD = "No hands and no figure in the sky, in the light or in the wind."
NOCHRIST = "No figures at all; never a figure meant to be Christ."
DISTANT = "Any people are small and far off, faces not visible."
CARVING = "The only face is carved in stone relief on the wall; any workers are small and far off, faces not visible."
FRUIT = "Any fruit is round and of no particular kind, never apples."
SNAKE = ("The serpent is a large slender real snake with muted dark olive teal scales: no legs, no human features, "
         "mouth closed, never speaking.")
CHERUB = ("The cherubim are as the prophet Ezekiel describes them: towering beings, each with four faces, the face of a "
          "man at the front, the face of a lion on the right, the face of an ox on the left and the face of an eagle "
          "behind; four great wings, two spread wide with their tips touching, two folded down covering the body; "
          "human hands beneath the wings; straight legs with feet like a calf's hoof gleaming like burnished bronze; "
          "fire moving back and forth among them with flashes of light; their wings edged with living flame. Never "
          "winged children, never robed people with wings, no rings of light over their heads. No human figures.")
CAMP = ("A wilderness camp of Israel in the Sinai desert in the time of Moses: low tents of black goat hair in rows on "
        "sand and gravel, rocky desert mountains behind, cooking fires; at the centre of the camp a large tent sanctuary "
        "of woven curtains inside a courtyard fence of white linen hung on posts. No stone buildings, no towers, no "
        "statues, no carvings of figures, no domes.")
BM = ("The man is the brick-maker in the reference images, now free in the wilderness: keep his face, skin tone, curly "
      "dark hair with grey, full beard with grey at the chin and build exactly; he wears a plain undyed knee length "
      "linen tunic, clean now, no mud. Quiet, thoughtful, never grinning. Framed from the chest up or wider, never an "
      "extreme close up of the face.")
MAN = ("The man is the man in the reference portrait: keep his face, skin tone, hair and beard exactly, but not the "
       "cloth on his shoulder. He wears nothing; he is seen from the chest up, facing the camera, in profile or from "
       "behind, or with tall grass or leaves covering him below the chest. Nothing below the chest is visible. No other "
       "people.")
WOMAN = ("The woman is the woman in the reference portrait: keep her face, skin tone and long curly hair exactly, but "
         "not the cloth on her shoulder. A head and shoulders view: her long thick hair falls forward over her bare "
         "shoulders and chest. Nothing below the shoulders is visible. No other people.")
MANF = ("The man is the man in the reference portrait: keep his face, skin tone, hair and beard exactly, but not the "
        "cloth on his shoulder. He wears only a covering of broad fig leaves sewn together at his waist (Genesis 3:7); "
        "he is seen from the chest up, facing the camera, in profile or from behind. No other people.")
WOMANF = ("The woman is the woman in the reference portrait: keep her face, skin tone and long curly hair exactly, but "
          "not the cloth on her shoulder. She wears a covering of broad fig leaves sewn together over her chest and "
          "waist (Genesis 3:7), her long thick hair falling over her shoulders; a head and shoulders view. No other "
          "people.")
HIDECLOSE = ("Only shoulders and upper arms in the frame: the man's deep dark brown skin exactly like the man in the "
             "first reference image and the woman's warm dark olive brown skin exactly like the woman in the second; "
             "rough untailored garments of soft brown animal hide over the shoulders, no woven cloth, no seams, no "
             "sleeves. No faces in the frame. No hands from above.")
HANDS = ("Only bare hands and bare forearms in the frame: the man's deep dark brown skin exactly like the man in the "
         "first reference image, the woman's warm dark olive brown skin exactly like the woman in the second; neither "
         "is pale or light skinned; no sleeves, no clothing, no watch, no rings, no jewellery.")
SHARP = ("Sharp focus from the foreground to the horizon: the ground or water at the bottom of the frame is crisp and "
         "detailed right to the bottom edge, with no blur, no haze, no fog, no mist band and no faded band at the bottom.")
BANNED = ["deity", "god figure", "divine being", "halo", "glowing man", "angel", "temple", "idol"]

FLAG_REFS = {"man": ["adam", "adam_turn"], "manf": ["adam", "adam_turn"], "woman": ["eve"], "womanf": ["eve"],
             "pairf": ["adam", "eve"], "hides": ["adam", "eve"], "hideclose": ["adam", "eve"], "hands": ["adam", "eve"],
             "bm": ["bm", "bm_turn"]}
PEOPLE = {"man", "woman", "manf", "womanf", "pairf", "hides", "hideclose", "hands", "pair"}


def S(scene, kind="veo", flags="", motion="Slow push in.", w=1.0, cue=None, verb=None, omni=None, note=""):
    return dict(scene=scene, kind=kind, refs=list(FLAG_REFS.get(flags, [])), flags=flags, motion=motion, w=w,
                src=None, cue=cue, anim=kind == "veo", verb=verb, omni=omni, note=note, clip=None, reverse=False)


def R(src, motion="Slow push in.", w=1.0, cue=None, anim=True, verb=None, note="", omni=None, clip=None,
      reverse=False):
    return dict(scene=note, kind="reuse", refs=[], flags="", motion=motion, w=w, src=src, cue=cue, anim=anim,
                verb=verb, omni=omni, note=note, clip=clip, reverse=reverse)


def G(text, w=1.0, cue=None, bg=None):
    return dict(scene="", kind="graphic", refs=[], flags=text, motion="", w=w, src=bg, cue=cue, anim=False,
                verb=None, omni=None, note="", clip=None, reverse=False)


def man(scene, flags="man", motion="He stays in place; only his eyes and breath move.", **kw):
    return S(scene, "veo", flags, motion, **kw)


def bm(scene, motion="Very slow push in.", **kw):
    return S(scene + " " + CAMP, "veo", "bm", motion, **kw)


SEG = {
    # 0 Cold open: the wind walks through the garden; Adam's eye; black for God's question
    0: [S("Evening in a vast lush garden, very close among broad leaves of fruit trees, the last gold light behind "
          "them; far off through the trees, the tops begin to bend in a wind.", flags="",
          motion="A wind arrives through the trees, tree by tree, nearer each time.", w=2.0,
          omni=dict(mode="image", prompt=(
              "One continuous shot in an ancient garden at evening. [0-3s] Very close among broad leaves, the last gold "
              "light behind them; far off the treetops begin to bend in a wind. [3-6s] The wind comes nearer in a long "
              "wave, tree after tree bending toward the camera, like slow footsteps. [6-8s] The leaves in front of the "
              "camera shiver hard, then go completely still. No people, no figures, no hands, nothing in the sky."))),
        R(F1 + "s032.jpg", "Treetops bend in the wind toward the camera.", w=1.3),
        R(F1 + "s033.jpg", "The grass bends in one long wave toward the camera.", w=1.2),
        man("Between dark evening leaves, an extreme close view of the man's eyes, from the brow to the cheekbones only, "
            "wide and afraid, the leaves blurred in front of him, cold blue evening light.",
            "manf", "His eyes move toward a sound; he does not move his head.", w=1.5),
        G("black: GOD, 'Where are you?'", cue=6.0)],
    # 1 flash-forward montage, about a second a shot
    1: [S("The eastern opening of a vast garden at dusk: a whirling sword of flame bursting alight between two great "
          "trees, a long blade made only of living fire, upright in the air, no hilt, no hand, no one holding it.",
          motion="The blade of fire ignites and flares.",
          omni=dict(mode="image", prompt="A blade of living fire bursts alight between two great trees at dusk and "
                    "begins to turn; sparks; no hand, no figure. Very fast push in.")),
        S(f"Extreme close view among the green leafy branches of a great fruit tree in a lush garden, leaves filling the whole frame: a round fruit being torn from its stem, the branch springing back, green leaves scattering, warm light. No dry ground, no dust. "
          f"{FRUIT}", "veo", "", "The fruit tears away and the branch springs back."),
        S(f"Extreme close view of a serpent's eye among dark leaves, the slit pupil, olive teal scales. {SNAKE}", "veo", "",
          "The eye shifts toward the camera."),
        R(F1 + "s028.jpg", "Fast push in; the leaves shake."),
        R(F1 + "s060.jpg", "Fast push in over the thorns."),
        R(G2 + "s004.jpg", "Fast push in to the grain.", clip=G2C + "ltx/s004.mp4"),
        R(F1 + "s080.jpg", "Fast push toward the far fire.")],
    # 2 where The Garden ended; the hook; the title
    2: [R(F1 + "s026.jpg", "Slow push in.", w=1.0),
        R(F1 + "s014.jpg", "Slow aerial drift.", cue="in a very good world"),
        R(F1 + "s061.jpg", "Slow push in.", cue="why is it like this"),
        R(G2 + "s195.jpg", "Very slow push in; the grass moves at the foot of the tree.", cue="It begins with a question",
          clip=G2C + "ltx/s195.mp4"),
        S(f"Very close, low in the long grass at the foot of a great fruit tree at dusk: olive teal scales sliding "
          f"through the grass blades. {SNAKE}", "veo", "", "The scales slide past, close.", cue="Another voice"),
        R(F1 + "s003.jpg", "Very slow push.", note="title: THE FALL / Genesis 3:1 to 24", cue=23.1)],
    # 3 3:1 the serpent and the woman; the pun
    3: [S(f"Ground level in long grass in the garden by day: a serpent moving through the grass toward the great tree in "
          f"the middle of the garden, its body a long line in the blades. {SNAKE}", "veo", "",
          "The serpent glides through the grass toward the tree."),
        S(f"A serpent coiling up the trunk of the great fruit tree into its lower branches, bark and leaves sharp, warm "
          f"light; all around the tree a lush green garden of fruit trees and long grass, no bare ground, no open plain. {SNAKE}", "veo", "", "The serpent climbs into the branches.", cue="any beast of the field"),
        S("Beneath the great fruit tree, the woman, head and shoulders, turning her face up toward a sound in the "
          "branches above her, curious, unafraid, warm light through the leaves.", "veo", "woman",
          "She turns her head toward the branches; she does not move otherwise.", cue="And he said to the woman"),
        S(f"One single continuous image: among the leaves of the great tree, a serpent's head close, looking down, fruit hanging around it, the leaves filling the frame from top to bottom. {SNAKE} "
          f"{FRUIT} No split, no second image, no panels.", "veo", "", "The head turns slowly.", cue="Did God really say"),
        R(F1 + "s005.jpg", "Slow push in.", cue="The chapter opens"),
        R(F1 + "s019.jpg", "Slow push in.", verb="ARUMMIM / NAKED", cue="naked, arummim", anim=False),
        S(f"A serpent coiled along a branch in late light, still, watching. {SNAKE}", "still", "",
          verb="ARUM / CRAFTY", cue="crafty, arum")],
    # 4 Egypt remembered; the voice behind the serpent
    4: [S("Egypt in the time of the pharaohs: a mud brick yard under a white sun, rows of drying bricks, and above it on "
          "a palace wall a huge painted stone relief of a pharaoh in profile wearing the rearing cobra on the brow of "
          "his crown, gold catching the light.", "still", "carving"),
        S("Close on an ancient Egyptian painted stone relief: the head of a pharaoh carved in profile wearing the tall crown, "
          "and on the brow of the crown a gold rearing cobra with its hood spread, clearly a snake, cracked paint, hard sun.", "still", "", cue="a rearing cobra"),
        bm("By day at his tent door he sits looking down at the dust, an old scar across his forearm, remembering.",
           cue="In that world"),
        R(F1 + "s043.jpg", "Slow push in.", cue="Genesis refuses"),
        R(F1 + "s065.jpg", "Dust blows across the ground.", cue="eating dust"),
        S(f"Deep shadow under dark leaves: a serpent's long body coiled, its scales catching a thin line of light. {SNAKE}",
          "veo", "", "The coils shift slowly in the shadow.", cue="Later Scripture"),
        S(f"Very close in low light: a serpent's head, its forked tongue flicking. {SNAKE}", "veo", "",
          "The tongue flicks once.", cue="Jesus calls him"),
        S(f"Extreme close view of a serpent's eye, the slit pupil narrowing, scales around it. {SNAKE}", "veo", "",
          "The pupil narrows; nothing else moves.", cue=35.7),
        R(F1 + "s010.jpg", "Slow push along the path toward the tree.", cue="And watch")],
    # 5 3:2 to 5 the dialogue
    5: [S("Beneath the great fruit tree, the woman, head and shoulders, looking up into the branches and answering, "
          "calm, warm light.", "veo", "woman", "She speaks a few words, looking up; she does not move otherwise."),
        S(f"Looking up from below: a serpent stretched along a branch above, leaves and hanging fruit around it, the sky "
          f"bright beyond. {SNAKE} {FRUIT}", "veo", "", "The serpent shifts along the branch.",
          cue="but about the fruit"),
        R(F1 + "s012.jpg", "Slow push in.", cue="or you will die"),
        S(f"At the height of the woman's eyes: the serpent's head among the leaves, close, facing the camera. {SNAKE}",
          "veo", "", "The head moves a little closer.", cue="You will not surely die"),
        R(F1 + "s024.jpg", "Slow push in.", cue="For God knows"),
        S(f"Beneath the great fruit tree, the woman's face from the brow to the chin, looking up at the fruit in the branches above, dappled sunlight through the leaves on her face. {FRUIT} The fruit does not glow; no glowing light.",
          "veo", "woman", "Her eyes widen a little; she does not move.", cue="your eyes will be opened")],
    # 6 word against word on screen; the name drops out; distrust
    6: [R(F1 + "s021.jpg", "Very slow push.", note="on screen: Genesis 2:16 to 17, God's words, then hers below",
          anim=False),
        R(F1 + "s029.jpg", "Very slow push.", note="on screen: FREELY fades, OR TOUCH IT appears, SURELY falls away",
          cue="She drops the freely", anim=False),
        R(F1 + "s101.jpg", "Very slow push.", note="on screen: NOT drops in front of God's words",
          cue="Then the serpent takes", anim=False),
        R(F1 + "s017.jpg", "Very slow push.", note="on screen: THE LORD GOD, then GOD", cue="Notice too"),
        S(f"A serpent coiled on the branch above the hanging fruit, its head low over it, deep warm shade. {SNAKE} "
          f"{FRUIT}", "veo", "", "Very slow push in; the serpent is still.", cue="The root of sin"),
        S(f"Close: one round golden fig shaped fruit, pale gold and green, hanging perfectly still on a leafy branch in warm light, a single leaf turning beside it. Not red, not an apple. {FRUIT}",
          "still", "", cue=66.6)],
    # 7 3:6 read, then SET PIECE 1 the eating
    7: [R(F1 + "s022.jpg", "Slow push in."),
        S(f"Beneath the great fruit tree, the woman's eyes and face, from the brow to the chin, gazing up at one fruit hanging in the branches above her, warm light on her skin, leaves around her. No baskets, no piles of fruit, no table. {FRUIT}",
          "veo", "woman", "Her gaze holds on the fruit; she does not move.", cue="pleasing to the eyes"),
        R(F1 + "s011.jpg", "Slow push in.", cue="desirable for obtaining wisdom"),
        man("Beside the tree, the man, chest up, in profile, silent, watching her, warm light.", "man",
            "He watches; he does not move.", cue="who was with her"),
        S(f"Extreme slow motion, among the green leaves of a fruit tree with the sky behind: a woman's bare hand and forearm reaching up from the bottom edge of the frame toward one hanging fruit. The arm comes from below the frame, not from the ground. {HANDS} {FRUIT}",
          "veo", "hands", "The hand rises slowly through the leaves.", cue=19.2),
        S(f"Extreme close, slow motion: one woman's hand alone, its fingers closing around a round fruit still hanging on its stem on the branch. Only one hand in the frame, no second hand, no giving. {HANDS} {FRUIT}", "veo",
          "hands", "The fingers close around the fruit.",
          omni=dict(mode="image", prompt="Extreme slow motion. Fingers close around a round fruit and pull; the stem "
                    "gives. Only the hand in the frame.")),
        S(f"Slow motion, high in a leafy fruit tree against the sky: a living green branch still attached to the tree springing back upward after a fruit has been picked from it, a few leaves shaking loose and drifting down through warm light. Nothing on the ground, no fallen branch, no flying fruit. {FRUIT}", "veo", "", "The branch springs back; leaves fall.",
          omni=dict(mode="image", prompt="Extreme slow motion. The branch springs back, leaves shake loose and fall "
                    "through the light. No hands remain in the frame.")),
        S(f"The woman, head and shoulders, turning toward the camera and lifting one round fruit in her own hand beside her face, offering it. Her own hand, her own arm; no other hands. {FRUIT}", "veo", "woman", "She turns and holds out the fruit; she does not walk."),
        S(f"Close: the man's bare hand reaching in and taking the round fruit from the woman's hand. {HANDS} {FRUIT}",
          "veo", "hands", "His hand takes the fruit."),
        S("From above the garden: a cloud's shadow sweeping fast across the treetops, the warm light going cold and "
          "grey behind it, the wind turning the leaves silver.", "veo", "", "The shadow sweeps across the garden.",
          omni=dict(mode="image", prompt="A cloud shadow sweeps across a vast garden from left to right; the gold light "
                    "goes cold blue grey; the wind turns every leaf over. No people.")),
        R(F1 + "s032.jpg", "Leaves turn silver in a cold wind.")],
    # 8 3:7 eyes opened; fig leaves; the teaching
    8: [man("An extreme close view of the man's eyes, from the brow to the cheekbones only, as in his first waking, but "
            "now the eyes open wide in fear, cold grey light.", "man", "His eyes open wide in fear.", w=1.0),
        S("The woman's eyes and face, from the brow to the chin, looking down at herself in sudden fear, cold grey "
          "light, her hair over her shoulders.", "veo", "woman", "Her eyes drop and she draws back a little.",
          cue="they knew that they were naked"),
        S(f"Close: bare hands tearing broad fig leaves from a branch, fast, in cold light. {HANDS}", "veo", "hands",
          "The hands tear the leaves away.", cue="so they sewed"),
        R(F1 + "s028.jpg", "Slow push in.", cue="fig leaves and made"),
        S(f"Close: bare hands tying broad fig leaves together with a twisted plant fibre, quick and clumsy. {HANDS}",
          "veo", "hands", "The hands pull the fibre tight.", cue=12.0),
        R(F1 + "s015.jpg", "Slow push.", cue="This is the only window"),
        R(F1 + "s025.jpg", "Slow push.", verb="GOOD FOR FOOD", cue="Good for food", anim=False),
        R(F1 + "s013.jpg", "Slow push.", verb="PLEASING TO THE EYES", cue="Pleasing to the eyes", anim=False),
        R(F1 + "s100.jpg", "Slow push.", verb="DESIRABLE FOR WISDOM", cue="Desirable for wisdom", anim=False),
        S("Two rough tablets of grey stone lying on a granite ledge on a desert mountain at dawn, their faces worn and "
          "carved with lines too faint to read.", "still", "", cue="Desirable is the verb"),
        R(F1 + "s018.jpg", "Slow push.", cue="What God made"),
        man("Beside the great tree, the man, chest up, in profile, saying nothing, his eyes on the fruit in her hand "
            "off camera.", "man", "He stays still; only the leaves move.", cue="And the man was with her"),
        S("Among dark trunks at dusk, the man and the woman in their coverings of fig leaves, apart from each other, "
          "heads lowered.", "veo", "pairf", "They stay still; only the leaves move.", cue="Their eyes are opened"),
        R(F1 + "s035.jpg", "Slow push into the dark trunks.", cue="They hide from God"),
        R(F1 + "s027.jpg", "Slow push.", cue="the fig leaves are their own")],
    # 9 3:8 to 10, SET PIECE 2 the voice in the garden
    9: [R(F1 + "s031.jpg", "Slow push in."),
        S("Evening in the garden: a long wave of wind entering the garden from far off, the treetops bending one after "
          "another toward the camera, light shifting across the ground between the trunks, as though something walks "
          "there.", "veo", "", "The wave of wind travels toward the camera.", cue="walking in the garden",
          omni=dict(mode="image", prompt=(
              "One continuous shot. [0-3s] A wave of wind enters a vast garden at evening from far off. [3-7s] Treetop "
              "after treetop bends toward the camera like slow footsteps, gold light moving across the ground between the "
              "trunks. [7-10s] The wave arrives; every leaf shivers; then stillness. No people, no figures, no hands, "
              "nothing in the sky."))),
        S("Deep among dark trunks at dusk, the man and the woman in fig leaves pressed back against a great trunk, half "
          "hidden by hanging leaves.", "veo", "pairf", "They stay pressed still; only the leaves move.",
          cue="they hid themselves"),
        S("The treetops of the garden bending in sequence toward the camera at dusk.", "veo", "",
          "The wave of wind passes overhead.", cue=15.0, omni=dict(mode="same", clip="s074", at=3.0)),
        S("Gold evening light moving across the ground between the trunks, the shadows of leaves racing.", "veo", "",
          "The light moves across the ground.", omni=dict(mode="same", clip="s074", at=5.5)),
        man("Among dark leaves, the man, chest up, his back against a trunk, breathing hard, eyes wide.", "manf",
            "He breathes hard; he does not move."),
        S("Very close: leaves shivering hard in a rushing wind, cold blue evening light.", "veo", "",
          "The leaves shiver hard, then still."),
        S("The woman, head and shoulders, among dark trunks, eyes shut, her hair stirring in the wind.", "veo",
          "womanf", "Her hair stirs; she does not move."),
        R(F1 + "s045.jpg", "The grass bends toward the camera, then is still."),
        R(F1 + "s037.jpg", "Hold; almost no motion.", cue=29.0, anim=False),
        R(F1 + "s036.jpg", "Hold; almost no motion.", cue=34.6, anim=False),
        man("Among dark trunks, the man, chest up, head lowered, not meeting the light.", "manf",
            "He keeps his head down; only the leaves move.", cue=37.6)],
    # 10 the camp; the centre of the chapter; Cain and Elijah
    10: [R(G2 + "s095.jpg", "Slow aerial drift over the camp."),
         R(G2 + "s017.jpg", "Slow push.", cue="Their sanctuary was a garden"),
         R(F1 + "s038.jpg", "Slow push.", cue="And here"),
         bm("Dusk: he stands at his tent door listening, a wind moving through the camp stirring the goat hair tent "
            "cloths around him.", cue="Many readers"),
         S("Evening light moving slowly between dark trunks toward a hidden place deep in the garden.", "veo", "",
           "The light moves deeper among the trunks.", cue="It is the God who comes looking"),
         S("A field of hard ground at dusk outside a garden, empty, a single shepherd's staff lying in the grass.",
           "still", "", cue="Where is your brother Abel"),
         S("The mouth of a cave in a granite mountain at night, a strong wind tearing at the scrub around it.", "veo", "",
           "Wind tears at the scrub; very slow push.", cue="and Elijah"),
         bm("Close, chest up: his face in the last light, listening to the wind.", cue="God's first word")],
    # 11 3:11 to 13 the questions and the blame
    11: [R(F1 + "s042.jpg", "Very slow push."),
         man("Among dark trunks, the man, chest up, eyes down, swallowing.", "manf", "He stays still, eyes down.",
             cue="Have you eaten"),
         man("The man, chest up, turning his head away toward the woman off camera, his jaw set.", "manf",
             "He turns his head away.", cue="The woman whom You gave me"),
         R(F1 + "s041.jpg", "Very slow push.", cue="Then the LORD God said to the woman"),
         S("The woman, head and shoulders, among dark trunks, eyes lowered, her hand at her shoulder.", "veo", "womanf",
           "She lowers her eyes; she does not move.", cue="What is this you have done"),
         R(F1 + "s044.jpg", "Very slow push.", cue="The serpent deceived me")],
    # 12 the shape of the blame (graphic) and no question to the serpent
    12: [G("graphic over a slow push across the garden floor: serpent, woman, man; the sin draws down from serpent to "
           "woman to man", bg=F1 + "s030.jpg"),
         G("graphic: the questions climb back, man then woman; the blame slides back down to the serpent",
           cue="God's questions run", bg=F1 + "s034.jpg"),
         G("graphic: the sentences run the first way again, serpent, woman, man", cue="The sentences will retrace",
           bg=F1 + "s024.jpg"),
         man("Among dark trunks, the man, chest up, silent, looking aside.", "manf", "He stays still.",
             cue="The man said nothing"),
         R(F1 + "s040.jpg", "Slow push.", cue="The woman whom You gave me"),
         S(f"Close in the grass at dusk: the serpent lying still, coiled, its eye open. {SNAKE}", "veo", "",
           "The serpent lies still; the grass moves.", cue="And God puts no question")],
    # 13 3:14 the serpent on its belly; Isaiah 65:25
    13: [R(F1 + "s046.jpg", "Slow push."),
         S(f"Close at ground level: a serpent going on its belly through bare dust at the edge of the garden, dust lifting "
           f"around its body, low light. {SNAKE}", "veo", "", "The serpent slides through the dust.",
           cue="On your belly"),
         R(F1 + "s047.jpg", "Slow push along the trail.", cue="dust you will eat"),
         R(F1 + "s048.jpg", "Slow aerial drift.", cue="Cursed falls"),
         R(F1 + "s049.jpg", "Slow push.", cue="And even in Isaiah"),
         R(G2 + "s005.jpg", "The dust lifts in a low wind.", cue="the food of the serpent")],
    # 14 3:15 enmity; the seed; the first gospel
    14: [R(F1 + "s050.jpg", "Slow push in."),
         S(f"At the edge of a line of dawn light on bare dust, a serpent rearing up in the shadow, hood low, poised. "
           f"{SNAKE}", "veo", "", "The serpent rears and holds.", cue="between your seed and her seed"),
         R(F1 + "s053.jpg", "Very slow push.", cue="He will crush your head"),
         G("black: one low boom", cue=11.3),
         R(F1 + "s051.jpg", "Slow push.", verb="ENMITY / OPEN WAR", cue="Enmity means"),
         R(F1 + "s054.jpg", "Slow push.", verb="ONE VERB / HEAD AND HEEL", cue="One verb stands"),
         R(F1 + "s057.jpg", "Slow push.", verb="HE", cue="And the seed is he"),
         R(F1 + "s059.jpg", "Slow push.", cue="A long war"),
         R(F1 + "s020.jpg", "Slow push.", cue="This is the first announcement")],
    # 15 montage: the long war (2 s a shot)
    15: [S("Two rough stone altars in a field outside a garden at evening: from one the smoke rises straight up, from "
           "the other it is blown flat along the ground.", "veo", "", "Fast push in; the smoke moves."),
         S("A field at dusk: a shepherd's staff lying in the trampled grass, a dark stain on the ground beside it, no "
           "one there.", "veo", "", "Fast push in.", verb="AND THEN HE DIED"),
         S("A line of rough stone graves along a bare hillside at dusk, one after another into the distance.", "veo", "",
           "Fast push along the line of graves.", verb="AND THEN HE DIED"),
         S("A great unfinished tower of fired brick rising on a flat plain at dusk, crowds of small people walking toward "
           "it from the west.", "veo", "distant", "Fast push toward the tower.", verb="AND THEN HE DIED"),
         S("A long column of captives walking east across a desert under guard toward a great walled city of blue glazed "
           "brick with flat topped walls and towers, no domes, no minarets, dust rising, everyone small and far off.", "veo", "distant", "Fast push along the column.",
           verb="AND THEN HE DIED"),
         S(f"Close in dust in hard light: a serpent striking forward, mouth open, fangs bared. {SNAKE}".replace(
             "mouth closed, never speaking", "never speaking"), "veo", "", "The serpent strikes.",
           omni=dict(mode="image", prompt="A serpent strikes forward at the camera in slow motion, dust flying."))],
    # 16 3:16 the woman; pain and toil; description, not charter
    16: [R(F1 + "s056.jpg", "Slow push."),
         S("Under a heavy sky at dusk, the woman, head and shoulders, her face turned into the wind, her hair blowing.",
           "veo", "womanf", "Her hair blows; she does not move.", cue="I will sharply increase"),
         R(F1 + "s058.jpg", "Slow push.", cue="Your desire"),
         R(F1 + "s064.jpg", "Slow push.", verb="PAIN / TOIL", cue="Her pain is the same word"),
         S("At dusk under a heavy sky, the man and the woman in fig leaves standing apart among the trees, not facing "
           "each other, at medium distance.", "veo", "pairf", "They stay still; only the wind moves.",
           cue="And the desire and the rule"),
         R(F1 + "s067.jpg", "Slow push.", cue="never a charter")],
    # 17 3:17 to 19 the ground cursed
    17: [R(F1 + "s060.jpg", "Slow push."),
         S("Time lapse at ground level: thorns and thistles bursting up through cracked dry ground under a hot sky, "
           "stems twisting, spikes opening.", "veo", "", "The thorns burst up through the ground.",
           cue="cursed is the ground"),
         R(F1 + "s061.jpg", "Slow push.", cue="Both thorns"),
         R(F1 + "s062.jpg", "Slow push.", cue="and you will eat the plants"),
         man("In a hard field of thorns and cracked dry ground under a hot white sky, no river, no trees: the man, chest up, sweat running down his brow and dust on his skin, squinting into the sun, exhausted.",
             "manf", "Sweat runs down; he breathes hard; he does not move.", cue="By the sweat of your brow"),
         S(f"Close: the man's bare hands tearing at thorn stems in cracked ground, scratched and bleeding. {HANDS}",
           "veo", "hands", "The hands pull at the thorns.", cue="until you return"),
         R(F1 + "s063.jpg", "Seed drifts from the thistles.", cue="For dust you are")],
    # 18 SET PIECE 3 dust to dust (The Garden v2 open reversed); and then he died; mercy
    18: [man("An extreme close view of the man's eyes, from the brow to the cheekbones only, lying on the ground, the "
             "eyes slowly closing, light fading from them.", "manf", "His eyes close slowly.", w=2.0),
         man("Lying on his back on bare earth, seen from the side at head and shoulder height, the man's face going "
             "still, eyes closed, dust on his skin, grey light.", "manf", "He is still; dust settles.", w=2.0),
         R(G2 + "s046.jpg", "Played backward: the dust draws in where he lay.", w=2.0, clip=G2C + "omni/s046.mp4",
           reverse=True),
         R(G2 + "s004.jpg", "Played backward.", w=1.5, clip=G2C + "ltx/s004.mp4", reverse=True),
         R(G2 + "s002.jpg", "The Garden v2's fall, played backward: rising from the dust up over bare ground, through "
           "the clouds into cold high light.", w=6.5, clip=G2C + "omni/s001.mp4", reverse=True),
         R(F1 + "s066.jpg", "Slow push.", cue=14.0),
         R(F1 + "s052.jpg", "Slow push.", cue="The man taken from the ground"),
         S("A single cairn of rough stones on a bare hillside at dusk, the wind moving the dry grass around it.", "veo",
           "", "The grass moves; very slow push.", cue="a refrain tolls"),
         G("black: AND THEN HE DIED, Genesis 5:5", cue="and then he died"),
         R(F1 + "s073.jpg", "Slow push.", cue="Yet mercy"),
         R(F1 + "s055.jpg", "Slow push.", cue="Work goes on"),
         R(F1 + "s098.jpg", "Slow push.", cue="Judgment is real", anim=False)],
    # 19 3:20 Eve, living
    19: [R(F1 + "s070.jpg", "Slow push."),
         S("At first light in a misty glade, the woman, head and shoulders, her face lifting toward the light.", "veo",
           "womanf", "She lifts her face to the light; she does not move otherwise.",
           cue="because she would be"),
         R(F1 + "s069.jpg", "Slow push.", verb="CHAVAH / LIVING", cue="Eve sounds like"),
         man("At first light, the man, chest up, in profile, looking at the woman off camera, the first hope in his "
             "face.", "manf", "He looks; he does not move.", cue="he names her")],
    # 20 3:21 the garments of skin
    20: [S("Close in warm morning light, seen from behind: rough garments of soft brown animal hide settling over the bare shoulders of a man and a woman standing side by side, and below them on the grass a few loose fig leaves lying where they fell. No leaves on the hides.", "veo", "hideclose",
           "The hides settle over the shoulders; fig leaves fall."),
         R(F1 + "s072.jpg", "Slow push.", cue="and He clothed them")],
    # 21 the priests clothed; the brick-maker watches; a life taken
    21: [S(f"The courtyard of the tent sanctuary by day, seen from across the camp: a line of men in new white linen "
           f"tunics standing before the bronze altar, an older man in a plain robe fastening a sash on the first of them, "
           f"faces small and far off. {CAMP}", "veo", "distant", "Very slow push."),
         R(G2 + "s093.jpg", "Slow push.", cue="And the words are the ones"),
         bm("By day in the crowd at the courtyard gate he watches, chest up, the white linen walls behind him.",
            cue="The brick-maker would have watched"),
         S("Close, from behind: a white linen tunic being drawn down over a man's shoulders by another man's hands, "
           "a sash wound around it; no faces in the frame.", "still", "distant", verb="KUTTONET / TUNIC",
           cue="tunics, the same word"),
         R(G2 + "s101.jpg", "Slow push.", cue="The text does not describe a sacrifice"),
         R(F1 + "s071.jpg", "Slow push.", cue="The covering came from a life taken")],
    # 22 3:22 the tree of life; exile as mercy
    22: [R(F1 + "s075.jpg", "Very slow push."),
         R(F1 + "s039.jpg", "Slow push.", cue="knowing good and evil"),
         R(F1 + "s076.jpg", "Slow push.", cue="lest he reach out"),
         S("At the eastern edge of the garden at dusk, the man and the woman in hides standing at medium distance, "
           "looking back toward the trees, seen from behind.", "veo", "hides", "They stand and look back; wind in the trees.",
           cue="Even the exile is a mercy")],
    # 23 3:23 to 24 and SET PIECE 4 east of Eden
    23: [R(F1 + "s078.jpg", "Slow push toward the opening."),
         S("The man and the woman in hides walking out through a wide opening between great trees into a dry land at "
           "dusk, seen from behind at medium distance.", "veo", "hides", "They walk slowly out of the garden.",
           cue="to work the ground"),
         S("Close at ground level: two pairs of bare feet walking on hard cracked ground, the hems of rough hide garments "
           "above them, dusk.", "veo", "hides", "The feet walk away from the camera.", cue="So He drove out the man"),
         S(f"In the eastern opening of the garden at dusk, cherubim standing guard, towering between the great trees, "
           f"their wings of fire spread, firelight on the trunks. {CHERUB}", "veo", "cherub",
           "The wings of fire move; flashes of light run among them.", cue="and stationed cherubim"),
         R(F1 + "s079.jpg", "The blade of fire turns.", cue="along with a whirling sword"),
         S("Close at dusk in the eastern opening of a garden between great dark trees: a whirling sword of flame, a long straight blade made only of living fire, upright, turning in the air with a roar, sparks flying; it is one single straight vertical column of fire shaped like a long blade, with no crossbar, no cross shape, no side flares, no metal, no hilt, no handle, no crossguard, no hand, no one holding it.", "veo", "", "The blade turns and roars.", cue=21.0,
           omni=dict(mode="image", prompt="A blade of living fire whirls and roars in the air at dusk, sparks flying; "
                     "no hand, no figure holding it. Slow push in.")),
         S(f"Wide at dusk: the cherubim's great wings of fire spread wide across the open gap between two great trees at the eastern edge of the garden, their tips touching, flame running along them; beyond, an open dry land. No gate, no doorway, no walls, no arch, no stone, nothing built. {CHERUB}", "veo", "cherub", "The wings of fire rise and spread."),
         S(f"Close in firelight at dusk: one living cherub's four faces, a man's face of the ancient Near East at the front with dark skin and dark eyes, a lion's face, an ox's face and an eagle's face, all living flesh and feather lit by fire, solemn and watchful, wings of flame behind. A living being, not a statue, not marble, not carved, not white stone. {CHERUB}", "veo", "cherub",
           "Fire moves; the faces are still and watchful."),
         S("Standing in a dry land at dusk, the man and the woman in hides turn and look back over their shoulders toward the garden, an orange glow of great fire far behind the camera lighting their faces, at medium distance. They stand; no campfire, no fire near them, not sitting.", "veo", "hides", "They look back; the firelight flickers."),
         R(F1 + "s080.jpg", "One long pull back and up: from the two figures to two specks in the dark land, one point "
           "of fire behind them.", w=2.0,
           omni=dict(mode="image", prompt=(
               "One continuous shot at dusk. [0-4s] Two small figures in rough hide garments walk toward the camera across a "
               "dry cracked land, away from the dark line of the garden behind them, where one blade of fire burns in "
               "the gap between the trees. [4-10s] The camera rises high into the air and pulls back as they keep walking "
               "toward it, until they are two specks on a vast dark plain and the fire is one small point far behind "
               "them. No other people."))),
         R(F1 + "s083.jpg", "Very slow push."),
         R(G2 + "s143.jpg", "Slow push.", verb="SHAKAN / TO DWELL", cue=37.0)],
    # 24 the veil; barred; Israel's exile; east
    24: [R(G2 + "s091.jpg", "Slow push."),
         S("Inside the holy place of the tent sanctuary in low lamplight: a great veil of blue, purple and scarlet woven "
           "linen hanging across the whole width, with cherubim woven into it in gold thread, each with four faces and "
           "four wings, a gold lampstand burning beside it. No people.", "veo", "",
           "Lamplight flickers on the veil; very slow push.", cue="cherubim were woven into the veil"),
         bm("Dusk: he stands outside the courtyard gate looking in, never going in, the linen walls glowing.",
            cue="No one simply walked back in"),
         R(G2 + "s182.jpg", "Slow push.", cue="And Israel heard"),
         S("Far off across a dry plain at dusk, the great walls and gate of an ancient city of blue glazed brick.",
           "still", "distant", cue="they too were carried east"),
         R(F1 + "s082.jpg", "Slow push along the path east.", cue="like Adam"),
         R(F1 + "s077.jpg", "Slow push.", cue="East becomes"),
         S("An abandoned unfinished tower of fired brick on a flat plain at dusk, empty, scaffolds of poles left "
           "standing, wind blowing dust.", "still", "", cue="The builders of Babel"),
         S("A wide desert at night under countless stars, a long empty track leading east into the dark.", "veo", "",
           "Very slow push along the track.", cue="Humanity keeps moving")],
    # 25 the seed narrows; the wilderness; It is written
    25: [R(F1 + "s084.jpg", "Very slow push."),
         S("A desert at night under a sky full of stars, countless as sand, from horizon to horizon.", "veo", "",
           "The stars wheel very slowly.", cue="The promise narrows"),
         S("Hills of Judea at dawn, terraces and a flock of sheep grazing, far off.", "still", "distant",
           cue="then to David"),
         R(F1 + "s085.jpg", "Slow push.", cue="born of a woman"),
         S("An old scroll partly unrolled on a wooden table in lamplight, columns of faint ancient writing too small "
           "to read.", "still", "", cue="Luke traces"),
         R(F1 + "s086.jpg", "Slow push.", cue="and the very next scene"),
         S("Close at ground level in hard noon light: a few stones on the rocky wilderness floor, each one round and brown like a loaf of bread, the stony ground sharp right to the bottom edge of the frame, heat shimmer beyond.", "still", "", cue="hungry instead"),
         R(F1 + "s087.jpg", "Slow push.", cue="Jesus answers")],
    # 26 the contrasts: tree, garden prayer, thorns, tomb; Hebrews 2:14
    26: [R(F1 + "s088.jpg", "Slow push."),
         R(G2 + "s167.jpg", "Slow push.", cue="Christ, in a garden"),
         S("An old stone olive press in the moonlight in an olive grove at night, dark oil stains on the stone.", "still",
           "christ", cue="not as I will"),
         S("A crown of twisted thorn branches lying on a flat stone in grey light.", "veo", "christ",
           "Very slow push.", cue="Adam wore thorns"),
         R(F1 + "s090.jpg", "Slow push.", cue="Christ was laid in a garden tomb"),
         S("A rough wooden beam standing against a dark sky on a hill, seen from below.", "still", "christ",
           cue="He shared our flesh"),
         R(F1 + "s089.jpg", "Slow push.", cue="so that by His death"),
         S("A bare rocky hill outside an ancient walled city under a sky gone dark at midday, the sun a dim smudge behind black cloud, stony ground and dry grass in the foreground right to the bottom edge of the frame.", "veo", "christ",
           "The darkness deepens.", cue="The strike to the heel")],
    # 27 SET PIECE 5 the veil to the empty tomb
    27: [S("A land gone dark at midday, a black sky over hills and a walled city.", "veo", "christ",
           "The darkness rolls over the land.", w=1.0),
         S("Close at ground level: dust and small stones jumping on bare rock as the ground shakes.", "veo", "christ",
           "The ground shakes; dust jumps.", w=1.0),
         S("Inside a dim lofty room of plain dressed limestone blocks with a flat cedar beamed ceiling, in the style of Herod's Jerusalem, a vast veil of blue, purple and scarlet woven cloth with gold cherubim in its weave tearing from top to bottom, blinding light flooding through the tear. No arches, no vaults, no gothic columns, no church. No people.", "veo", "christ",
           "The veil tears from top to bottom; light floods through.", w=1.5,
           omni=dict(mode="image", prompt="A vast woven veil tears from the top down to the bottom in one stroke; "
                     "blinding light pours through the tear. No people, no hands.")),
         R(F1 + "s095.jpg", "Light pours through the torn edge.", w=1.0),
         R(G2 + "s172.jpg", "Light floods along the path out of the open tomb.", w=1.2),
         S(f"At the foot of a rock cut tomb at sunrise, in the dust of the path, a dead serpent lying still; the "
           f"wind passes and it crumbles and blows away as dust. {SNAKE}", "veo", "christ",
           "The serpent crumbles into dust and blows away.", w=1.3,
           omni=dict(mode="image", prompt="At sunrise a dead serpent lies still in the dust of the path before a rock cut "
                     "tomb. [0-3s] Stillness. [3-6s] Its body turns grey, cracks along its length and collapses into a "
                     "line of fine dust. [6-10s] A wind passes along the path and blows the dust away completely, leaving "
                     "only the clean path in the morning light. No people, no hands.")),
         R(F1 + "s092.jpg", "Slow push; wind in the trees.", w=1.0)],
    # 28 the way back: the mercy seat, the veil, the city
    28: [S("The cover of the ark of the covenant in lamplight: two cherubim of hammered gold, one at each end, facing "
           "each other with their faces turned down toward the cover, their wings spread up and over it.", "veo", "",
           "Lamplight moves on the gold; very slow push."),
         R(F1 + "s094.jpg", "Slow push toward the torn veil.", cue="And when Jesus died"),
         R(F1 + "s096.jpg", "Slow push.", cue="by the new and living way"),
         R(G2 + "s187.jpg", "Slow aerial rise.", cue="The Bible closes"),
         R(G2 + "s189.jpg", "Slow push.", cue="No longer any curse"),
         R(G2 + "s188.jpg", "Slow push.", cue="The tree of life open"),
         R(G2 + "s184.jpg", "Slow push.", cue="will see His face"),
         R(F1 + "s097.jpg", "Slow push.", cue=49.0),
         R(G2 + "s185.jpg", "Slow push.")],
    # 29 come out: the brick-maker steps into the light; the question
    29: [bm("Dawn: he steps out of the dark doorway of his goat hair tent into first light, chest up, squinting at the "
            "sun.", motion="He steps forward out of the doorway into the light."),
         R(G2 + "s090.jpg", "Slow follow.", cue="It is to come out"),
         R(G2 + "s192.jpg", "Slow push.", cue="God covered their shame"),
         bm("Close, chest up: his face in first light, eyes closed, at peace.", cue="What are you using"),
         R(G2 + "s092.jpg", "Slow push.", cue=28.3)],
    # 30 open loop into Cain and Abel; end card
    30: [S("East of Eden at evening: an open field of hard ground, two smokes rising from two stone altars, and between them a young man of the ancient Near East seen from behind, in a plain knee length undyed wool tunic with a rope belt, barefoot, looking back over his shoulder into the dusk; no modern clothes, no trousers, no shirt. No houses, no huts, no buildings anywhere.", "veo",
           "distant", "Very slow push; the smoke rises."),
         G("black", cue="it will be about a brother"),
         G("end card: Study The Fall / makor.co.za/genesis/the-fall, WATCH NEXT Cain and Abel", cue=12.6)],
}


def _orig():
    out = {}
    for pre, f in ((F1, "../03-the-fall/script/shotlist.json"), (G2, "../02-the-garden-v2/script/shotlist.json")):
        for x in json.loads((FILM / f).read_text()):
            out[pre + x["id"] + ".jpg"] = dict(scene=x.get("scene") or x.get("prompt", "")[:400] or "",
                                               flags=x.get("flags") or "")
    return out


ORIG = _orig()


def prompt_for(sh):
    f = sh["flags"]
    who = {"man": MAN + " " + PR.NEAR_EAST, "manf": MANF + " " + PR.NEAR_EAST, "woman": WOMAN + " " + PR.NEAR_EAST,
           "womanf": WOMANF + " " + PR.NEAR_EAST, "pairf": PR.FIG_LEAVES + " " + PR.NEAR_EAST,
           "hides": PR.HIDES, "hideclose": HIDECLOSE, "hands": "", "bm": BM + " No other people close to the camera.",
           "distant": DISTANT, "christ": NOCHRIST, "carving": CARVING, "cherub": ""}.get(f, NOFIG)
    refs = [REF[r] for r in sh["refs"]]
    p = f"{sh['scene']} {who} {NOGOD}{PR.REFNOTE if refs else ''} {PR.SUFFIX} {SHARP}".replace("  ", " ")
    low = p.lower() + sh["motion"].lower()
    for w in BANNED:
        assert w not in low, f"banned word {w!r} in: {sh['scene'][:60]}"
    assert "–" not in p and "—" not in p
    return p, refs


def cue_time(T, durs, words, a, b):
    if isinstance(words, (int, float)):
        return a + words
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
            if s.get("cue") is not None and k:
                starts[k] = cue_time(T, durs, s["cue"], e["t"], end)
        bounds = [k for k in range(len(segs)) if starts[k] is not None] + [len(segs)]
        times = starts + [end]
        for a, b in zip(bounds, bounds[1:]):
            t0, t1 = times[a], times[b]
            assert t1 > t0, f"cues out of order in segment {i}: {[(s.get('cue'), round(x, 1) if x else x) for s, x in zip(segs, starts)]}"
            tot = sum(s["w"] for s in segs[a:b])
            for k in range(a, b):
                starts[k] = t0
                t0 += (t1 - times[a]) * segs[k]["w"] / tot
        for k, s in enumerate(segs):
            n += 1
            d = (starts[k + 1] if k + 1 < len(segs) else end) - starts[k]
            assert d > 0.4, f"s{n:03d} only {d:.2f} s (segment {i})"
            shots.append(dict(id=f"s{n:03d}", chapter=e["chapter"], start=round(starts[k], 3), dur=round(d, 3),
                              picture=e["text"], **s))
    assert abs(shots[-1]["start"] + shots[-1]["dur"] - T["total"]) < 0.01
    # name the omni "same" takes by the shot that makes them
    md = ["# The Fall v2: shot list (photoreal)\n",
          "Generated by `script/storyboard.py`. Reuse and graphic shots carry no prompt.\n"]
    sb = ["# The Fall v2: storyboard\n", "Generated by `script/storyboard.py`. Plan and decisions: `../TREATMENT.md`.\n",
          "| Shot | Time | Length | Kind | Picture |", "|---|---|---|---|---|"]
    counts, out, seen = {}, [], {}
    for k, sh in enumerate(shots, 1):
        counts[sh["kind"]] = counts.get(sh["kind"], 0) + 1
        mm, ss = divmod(sh["start"], 60)
        if sh["kind"] == "graphic":
            desc = sh["flags"] + (f" (over {sh['src']})" if sh["src"] else "")
        elif sh["kind"] == "reuse":
            seen.setdefault(sh["src"], []).append(sh["id"])
            desc = f"reuse {sh['src']}" + (f" ({sh['note']})" if sh["note"] else "")
            if sh["clip"]:
                desc += f", clip {sh['clip']}" + (" played backward" if sh["reverse"] else "")
        else:
            desc = sh["scene"]
        if sh["verb"]:
            desc += f" + on screen {sh['verb']}"
        if sh["omni"]:
            desc += f" [omni {sh['omni']['mode']}]"
        sb.append(f"| {sh['id']} | {int(mm)}:{ss:04.1f} | {sh['dur']:.1f} s | {sh['kind']}{' anim' if sh['anim'] else ''} | {desc} |")
        rec = dict(sh)
        if sh["kind"] in ("veo", "still"):
            p, refs = prompt_for(sh)
            keep = PR.KEEP if sh["flags"] in PEOPLE or sh["flags"] == "bm" else ""
            mp = f"{sh['scene']} {sh['motion']}{keep} {PR.MOTION}"
            assert not any(w in mp.lower() for w in BANNED), sh["id"]
            rec.update(prompt=p, refs=refs, motion=mp)
            md.append(f"### Shot {k}: {sh['id']} {sh['chapter']} ({sh['dur']:.1f} s, {sh['kind']}, {sh['flags'] or 'nofig'})")
            if refs:
                md.append("- Refs: " + ", ".join(refs))
            md += ["- Image prompt", f"> {p}", f"- Motion: {sh['motion']}", ""]
        elif sh["kind"] == "reuse":
            assert (FILM / sh["src"]).exists(), f"missing {sh['src']}"
            if sh["clip"]:
                assert (FILM / sh["clip"]).exists(), f"missing {sh['clip']}"
            orig = dict(ORIG.get(sh["src"], {}))
            f = orig.get("flags", "")
            orig["flags"] = ("pair" if "woman" in f or f == "pair" else "man" if "people" in f or f == "man" else
                             "bm" if f == "bm" else "distant" if f == "distant" else "")
            keep = PR.KEEP if orig["flags"] in ("pair", "man", "bm") else ""
            rec.update(motion=f"{orig.get('scene', '')} {sh['motion']}{keep} {PR.MOTION}".strip(),
                       flags=orig["flags"])
        if rec.get("flags") in PEOPLE and rec.get("flags") != "hides":
            rec["lock"] = True      # hides (from 3:21) may walk, so the exile is not locked to its keyframe
        o = rec.get("omni")
        if o and o.get("mode") == "image" and "[0-" not in o["prompt"] and rec["kind"] in ("veo", "still"):
            # the whole scene goes with the motion (VIDEO-METHODS rule 2)
            rec["omni"] = dict(o, prompt=f"{sh['scene']} {o['prompt']}{PR.KEEP if sh['flags'] in PEOPLE else ''}")
        out.append(rec)
    (HERE / "movement-shots.json").write_text(json.dumps(
        [dict(id=s["id"], chapter=s["chapter"], n=0, start=s["start"], dur=s["dur"], picture=s["scene"] or s["picture"])
         for s in out], indent=1, ensure_ascii=False))
    (HERE / "shotlist.md").write_text("\n".join(md))
    (HERE / "shotlist.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    (HERE / "storyboard.md").write_text("\n".join(sb) + "\n")
    new = counts.get("veo", 0) + counts.get("still", 0)
    dup = {k: v for k, v in seen.items() if len(v) > 1}
    print(f"{len(shots)} shots {counts}; new images: {new}; reused animated: "
          f"{sum(1 for s in out if s['kind'] == 'reuse' and s['anim'])}; omni takes: "
          f"{sum(1 for s in out if s['omni'] and s['omni']['mode'] == 'image')}")
    print("reused more than once:", {k.split('/')[-1] if 'fall' in k else 'g2 ' + k.split('/')[-1]: v for k, v in dup.items()})


if __name__ == "__main__":
    main()
