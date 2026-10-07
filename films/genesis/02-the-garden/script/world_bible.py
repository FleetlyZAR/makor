#!/usr/bin/env python3
"""M3 world bible for The Garden: look tests for everything this film shows that The Seven
Days did not. Writes script/world-bible.md in the still tools' format.

Photoreal treatment from 7 October 2026 (films/STYLE-BIBLE.md): no painted references; people
items carry the cast portraits in stills/cast/. Items 5 and 8 were made in the photoreal test
(films/tests/photoreal-garden, s041 and s037) and copied in, so they are not regenerated.

    python3 films/genesis/02-the-garden/script/world_bible.py
    python3 films/tools/still_batch.py films/genesis/02-the-garden 1 2 ... \
        --script script/world-bible.md --out stills/world --aspect 16:9 --log COSTS-movement.md
"""
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
ADAM, EVE = "stills/cast/adam.jpg", "stills/cast/eve.jpg"

# Eden, reused word for word wherever the garden is seen (decision D4).
EDEN = ("a vast lush garden planted in the east: groves and orderly rows of fruit trees of every kind, open glades "
        "of soft grass, a clear river flowing out of the garden toward the east, and a wide opening in the trees on "
        "its eastern side facing the rising light")
SUFFIX = ("Photorealistic cinematic film still, shot on 35mm film, natural light, colour grade of deep ink teal "
          "shadows and warm muted gold highlights, warm cream whites, no saturated reds or purples, calm and reverent, "
          "wide 16:9 composition with calm low detail space in the lower third, full frame with no borders or black "
          "bars, no text, no lettering, no watermark, not a painting, not an illustration, not a 3D render, not cartoon.")
NEAR_EAST = ("The land is the ancient Near East by the Tigris and Euphrates: date palms, fig trees, pomegranate trees, "
             "olive trees, grape vines, reeds along the river, no tropical plants, no mango, no banana, no apple trees. "
             "No walls, no buildings, no ruins, no fences, nothing made by hands.")
NOFIG = "No people, no figures, no faces, no silhouettes."
NOHANDS = "No hands, no arms, no figure in the sky or in the light, nothing that looks like a person forming him."
PEOPLE = ("The man is the man in the reference portrait: keep his face, skin tone, hair and beard exactly, but not the cloth on his shoulder. He is seen "
          "at medium or long distance, from behind, in profile or three quarter, with bare shoulders, and tall grass, "
          "plants or the landscape cover him below the chest. Never a close up. No other people.")
WOMAN = ("The woman is the woman in the second reference portrait: keep her face, skin tone and long curly black hair "
         "exactly, but not the cloth on her shoulder; before the Fall neither of them wears anything. Both are seen at long distance with bare shoulders, tall grass and flowers covering them below the "
         "shoulders. Never a close up. No other people.")
BARE = ("A bare plain of the ancient Near East before anything grew: no trees, no palms, no shrubs, no grass, no "
        "plants of any kind, bare earth to the horizon. No walls, no buildings, nothing made by hands.")
BARE_ITEMS = {"Dry ground before the garden", "Formed from the dust, by effect"}
NOT_EDEN = {"A garden at night", "The river and the tree of life"}   # not Eden: walls and a city belong there

ITEMS = [
    ("Dry ground before the garden", "Dust and breath", [],
     "Wide dry empty ground at first light, no shrub and no plant anywhere, and springs welling up from the earth so "
     "that the dust darkens and mist rises over the whole surface of the ground.", NOFIG),
    ("Formed from the dust, by effect", "Dust and breath", [],
     "A very wide, empty plain of damp earth at dawn, seen from far away and slightly above. In the far middle "
     "distance, tiny in the frame, a whirl of dust and a soft column of warm light rise from the ground, and inside "
     "the veil of moving dust the faint low outline of a man lying on the earth is only just taking shape, no more "
     "than a long low mound with a suggestion of a head and shoulders, mostly hidden by the dust.",
     NOHANDS + " No anatomy, no muscles, no visible body detail, no sculpture, no standing figures, no people "
     "anywhere else, no close up."),
    ("The breath of life", "Dust and breath", [ADAM],
     "On the ground at first light, a man lying on his back in deep grass where he was formed, seen from the side at "
     "medium long distance with the grass hiding him below the chest, his eyes closed, and a breath of wind and warm "
     "light passing over him like a living current through the air, grass bending; the moment life begins.",
     NOHANDS + " " + PEOPLE),
    ("Eden", "A garden in Eden", [],
     f"Seen from a rise, {EDEN}. Morning light, abundant and peaceful, a place of delight.", NOFIG),
    ("The two trees", "A garden in Eden", [],
     "At the centre of the garden in a quiet open glade, two great living trees standing apart in soft light, both "
     "full of green leaves and both bearing fruit, both beautiful and pleasing to the eye, each a different kind of "
     "tree. Natural trees, nothing glowing, nothing dead or bare, no creature in them.",
     NOFIG + " No snake, no serpent, no animals."),
    ("The four rivers", "A garden in Eden", [],
     "From very high above, one river flowing out of a green garden and dividing into four great headwaters that "
     "wind away across a vast land, gold glinting in the riverbeds.", NOFIG),
    ("Gold, bdellium and onyx", "A garden in Eden", [],
     "A close view of a clear shallow riverbed: nuggets of pure gold, pale resin and dark banded onyx stones lying "
     "among the pebbles under moving water.", NOFIG),
    ("To cultivate and keep", "To cultivate and keep", [ADAM],
     f"Inside the garden in early light, {EDEN.split(':')[1].split(',')[0].strip()}, and far away between the trees "
     "a man at work tending the ground.", PEOPLE),
    ("The animals brought", "Not good to be alone", [ADAM],
     "A wide meadow in the garden: deer, oxen, wild goats, a lion, birds landing, all coming across the grass one "
     "after another toward a single man standing in tall grass at the far side of the meadow, seen at long distance. "
     "The animals are of the ancient Near East: fallow deer, wild aurochs cattle, Nubian ibex, a lion, each "
     "anatomically correct and separate.", PEOPLE),
    ("The deep sleep", "Bone of my bones", [ADAM],
     "The garden at night under stars, and beneath a great tree a man lying asleep on his side in deep grass, seen at "
     "medium long distance, moonlight on his shoulder, and a soft warm light gathering quietly near him in the dark.", NOHANDS + " " + PEOPLE),
    ("Bone of my bones", "Bone of my bones", [ADAM, EVE],
     "Morning light in the garden, and across a glade the man and the woman meeting among the trees, seen at long "
     "distance, the light warm around them, peace and joy.", WOMAN),
    ("A garden at night", "The last Adam", [],
     "An olive grove on a hillside at night under a full Passover moon, old twisted olive trees, the city wall faint in the "
     "distance across a valley, silent and empty, the image filling the whole frame edge to edge with no black bars.", NOFIG),
    ("The river and the tree of life", "Eden restored", [],
     "A radiant city of light with a clear river flowing down its great street, and on both banks of the river "
     "trees heavy with fruit, the whole place lit from everywhere with no sun and no moon. The city is of pale gold "
     "stone and light, of no recognisable architectural style, not classical, not modern, no columns, no hotels, the "
     "image filling the whole frame edge to edge with no black bars.",
     NOFIG + " No sun disc, no moon."),
]


def main():
    out = ["# The Garden: world bible (M3 look development)\n",
           "Look tests at 16:9 for everything The Garden shows that The Seven Days did not.",
           "Generated by `script/world_bible.py`. Photoreal treatment (7 October 2026). D2 (God's acts",
           "only by effect) and D4 (Eden) are written into the prompts.\n", f"Eden: {EDEN}.\n"]
    for i, (name, where, refs, scene, excl) in enumerate(ITEMS, 1):
        out += [f"### Shot {i}: {name} ({where})", "- Refs: " + ", ".join(refs), "- Image prompt:",
                f"  > {scene} {excl} {BARE + ' ' if name in BARE_ITEMS else '' if name in NOT_EDEN else NEAR_EAST + ' '}{SUFFIX}", ""]
    text = "\n".join(out)
    assert "–" not in text and "—" not in text
    low = text.lower()
    for w in ["deity", "god figure", "divine being", "halo", "glowing man", "angel", "temple", "idol"]:
        assert w not in low, w
    (HERE / "world-bible.md").write_text(text)
    print(f"wrote script/world-bible.md: {len(ITEMS)} prompts")


if __name__ == "__main__":
    main()
