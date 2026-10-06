#!/usr/bin/env python3
"""M3 world bible for The Garden: look tests for everything this film shows that The Seven
Days did not. Writes script/world-bible.md in the still tools' format (with - Refs: lines
pointing at The Seven Days world stills, so both films share one painted world).

    python3 films/genesis/02-the-garden/script/world_bible.py
    python3 films/tools/still_batch.py films/genesis/02-the-garden 1 2 ... \
        --script script/world-bible.md --out stills/world --aspect 16:9 --log COSTS-movement.md
"""
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
SD = "../01-the-seven-days/stills/world"   # The Seven Days world stills, relative to this film

# Eden, reused word for word wherever the garden is seen (decision D4).
EDEN = ("a vast lush garden planted in the east: groves and orderly rows of fruit trees of every kind, open glades "
        "of soft grass, a clear river flowing out of the garden toward the east, and a wide opening in the trees on "
        "its eastern side facing the rising light")
SUFFIX = ("Hand painted matte painting, painterly illustration with visible brush texture and soft canvas grain, "
          "reverent, still and quiet, soft diffused light, restrained palette of deep ink teal (#0E2A2E) shadows, "
          "water teal (#0F6C6C) midtones and warm muted gold (#B8862F) light, warm cream highlights, greens rendered "
          "as deep teal greens within the palette, wide 16:9 cinematic composition with calm space in the lower "
          "third, fully painted edge to edge with no blank or flat areas, full frame with no borders, no text, no "
          "lettering, no watermark, not photoreal, not cartoon, not 3D render.")
NOFIG = "No people, no figures, no faces, no silhouettes."
NOHANDS = "No hands, no arms, no figure in the sky or in the light, nothing that looks like a person forming him."
PEOPLE = ("The human figures are tiny and far away, seen from behind or in profile, framed by trees and light, so "
          "small that no body, clothing or face detail can be seen. No close up, no other people.")
REFNOTE = "Match the painting style, palette and light of the reference images."

ITEMS = [
    ("Dry ground before the garden", "Dust and breath", [f"{SD}/shot-01.jpg"],
     "Wide dry empty ground at first light, no shrub and no plant anywhere, and springs welling up from the earth so "
     "that the dust darkens and mist rises over the whole surface of the ground.", NOFIG),
    ("Formed from the dust, by effect", "Dust and breath", [f"{SD}/shot-01.jpg"],
     "A very wide, empty plain of damp earth at dawn, seen from far away and slightly above. In the far middle "
     "distance, tiny in the frame, a whirl of dust and a soft column of warm light rise from the ground, and inside "
     "the veil of moving dust the faint low outline of a man lying on the earth is only just taking shape, no more "
     "than a long low mound with a suggestion of a head and shoulders, mostly hidden by the dust.",
     NOHANDS + " No anatomy, no muscles, no visible body detail, no sculpture, no standing figures, no people "
     "anywhere else, no close up."),
    ("The breath of life", "Dust and breath", [f"{SD}/shot-07.jpg"],
     "Far away on the ground at first light, a man lying where he was formed, and a breath of wind and warm light "
     "passing over him like a living current through the air, grass bending; the moment life begins.",
     NOHANDS + " " + PEOPLE),
    ("Eden", "A garden in Eden", [f"{SD}/shot-01.jpg", f"{SD}/shot-08.jpg"],
     f"Seen from a rise, {EDEN}. Morning light, abundant and peaceful, a place of delight.", NOFIG),
    ("The two trees", "A garden in Eden", [f"{SD}/shot-08.jpg"],
     "At the centre of the garden in a quiet open glade, two great living trees standing apart in soft light, both "
     "full of green leaves and both bearing fruit, both beautiful and pleasing to the eye, each a different kind of "
     "tree. Natural trees, nothing glowing, nothing dead or bare, no creature in them.",
     NOFIG + " No snake, no serpent, no animals."),
    ("The four rivers", "A garden in Eden", [f"{SD}/shot-01.jpg"],
     "From very high above, one river flowing out of a green garden and dividing into four great headwaters that "
     "wind away across a vast land, gold glinting in the riverbeds.", NOFIG),
    ("Gold, bdellium and onyx", "A garden in Eden", [f"{SD}/shot-02.jpg"],
     "A close view of a clear shallow riverbed: nuggets of pure gold, pale resin and dark banded onyx stones lying "
     "among the pebbles under moving water.", NOFIG),
    ("To cultivate and keep", "To cultivate and keep", [f"{SD}/shot-07.jpg", f"{SD}/shot-02.jpg"],
     f"Inside the garden in early light, {EDEN.split(':')[1].split(',')[0].strip()}, and far away between the trees "
     "a man at work tending the ground, small in the landscape.", PEOPLE),
    ("The animals brought", "Not good to be alone", [f"{SD}/shot-06.jpg"],
     "A wide meadow in the garden: deer, oxen, wild goats, a lion, birds landing, all coming across the grass one "
     "after another toward a single tiny distant man standing at the far edge of the meadow.", PEOPLE),
    ("The deep sleep", "Bone of my bones", [f"{SD}/shot-04.jpg"],
     "The garden at night under stars, and far away beneath a great tree a man lying asleep, small in the landscape, "
     "and a soft warm light gathering quietly near him in the dark.", NOHANDS + " " + PEOPLE),
    ("Bone of my bones", "Bone of my bones", [f"{SD}/shot-07.jpg"],
     "Morning light in the garden, and far across a glade two tiny human figures meeting among the trees, a man and "
     "a woman, the light warm around them, peace and joy.", PEOPLE),
    ("A garden at night", "The last Adam", [f"{SD}/shot-11.jpg"],
     "An olive grove on a hillside at night under a pale moon, old twisted olive trees, the city wall faint in the "
     "distance across a valley, silent and empty.", NOFIG),
    ("The river and the tree of life", "Eden restored", [f"{SD}/shot-12.jpg"],
     "A radiant city of light with a clear river flowing down its great street, and on both banks of the river "
     "trees heavy with fruit, the whole place lit from everywhere with no sun and no moon.",
     NOFIG + " No sun disc, no moon."),
]


def main():
    out = ["# The Garden: world bible (M3 look development)\n",
           "Look tests at 16:9 for everything The Garden shows that The Seven Days did not.",
           "Generated by `script/world_bible.py`. Decisions D1 (people far off), D2 (God's acts",
           "only by effect) and D4 (Eden) are written into the prompts.\n", f"Eden: {EDEN}.\n"]
    for i, (name, where, refs, scene, excl) in enumerate(ITEMS, 1):
        out += [f"### Shot {i}: {name} ({where})", "- Refs: " + ", ".join(refs), "- Image prompt:",
                f"  > {scene} {excl} {REFNOTE} {SUFFIX}", ""]
    text = "\n".join(out)
    assert "–" not in text and "—" not in text
    low = text.lower()
    for w in ["deity", "god figure", "divine being", "halo", "glowing man", "angel", "temple", "idol"]:
        assert w not in low, w
    (HERE / "world-bible.md").write_text(text)
    print(f"wrote script/world-bible.md: {len(ITEMS)} prompts")


if __name__ == "__main__":
    main()
