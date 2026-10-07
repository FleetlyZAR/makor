#!/usr/bin/env python3
"""M3 world bible for The Fall: look tests for everything this film shows that The Garden did
not. Writes script/world-bible.md in the still tools' format (with - Refs: lines pointing at
The Garden's stills, now photoreal, so the films share one world).

Photoreal treatment from 7 October 2026 (films/STYLE-BIBLE.md, "Photoreal"; shared wording in
films/tools/photoreal.py). The painted stills are in stills/world-painted/.

    python3 films/genesis/03-the-fall/script/world_bible.py
    python3 films/tools/still_batch.py films/genesis/03-the-fall 1 2 ... \
        --script script/world-bible.md --out stills/world --aspect 16:9 --log COSTS-movement.md
"""
import pathlib
import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "tools"))
import photoreal as PR  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
G = "../02-the-garden/stills"   # The Garden's stills, relative to this film

# The Garden's Eden, reused word for word wherever the garden is seen.
EDEN = ("a vast lush garden planted in the east: groves and orderly rows of fruit trees of every kind, open glades "
        "of soft grass, a clear river flowing out of the garden toward the east, and a wide opening in the trees on "
        "its eastern side facing the rising light")
# Decision D1: the serpent is an ordinary small snake, far off. The words serpent and cherubim never go in a prompt.
SNAKE = ("a small ordinary snake, slender and muted dark olive teal, lying low in the grass, seen from far away so it "
         "is only a thin dark curve, natural and unremarkable, mouth closed, no legs, nothing monstrous")
SUFFIX = PR.SUFFIX
NOFIG = "No people, no figures, no faces, no silhouettes."
NOSNAKE = "No snake, no animals."
NOSKY = "No figure in the sky or in the light, no hands, nothing shaped like a person in the light or the wind."
PEOPLE = ("The human figures are tiny and far away, seen from behind or in profile, framed by trees and light, so "
          "small that no body, clothing or face detail can be seen. No close up, no other people.")
FRUIT = "The fruit is round and of no particular kind, not apples."
REFNOTE = PR.REFNOTE.strip()
OUTSIDE = {6, 7, 9, 13, 14}   # items away from the garden: no Eden plant list

ITEMS = [
    ("A snake in the grass", "Did God really say?", [f"{G}/world/shot-04.jpg", f"{G}/world/shot-05.jpg"],
     f"Inside the garden in the late afternoon: long soft grass at the foot of great fruit trees, and in the middle "
     f"distance, {SNAKE}, moving through the grass toward the centre of the garden. The garden is still beautiful "
     "and whole, but the light is lower and the shadows longer.", NOFIG),
    ("The tree in the middle", "Did God really say?", [f"{G}/world/shot-05.jpg", PR.EVE],
     "The great tree in the middle of the garden, heavy with fruit, seen from far off between the trunks of other "
     "trees that frame the view. Beneath it the woman, seen in profile at medium long distance, looking up at the "
     f"fruit, and low in the grass near her, {SNAKE}. {FRUIT}", PR.BEFORE_FIGS.replace("The man and the woman are the man and the woman in the reference portraits", "The woman is the woman in the reference portrait")),
    ("Fig leaves", "She took and ate", [f"{G}/world/shot-11.jpg", PR.ADAM, PR.EVE],
     "Broad lobed fig leaves filling the near foreground, dark against the evening light, and far beyond them through "
     "a gap in the leaves, the man and the woman at medium distance withdrawn into the deep shade of the trees.",
     PR.FIG_LEAVES + " " + NOSNAKE),
    ("The sound in the garden", "Where are you?", [f"{G}/movement/s034.jpg", f"{G}/world/shot-04.jpg"],
     "Evening in the garden: a long wave of wind moving through the treetops, leaves turning silver, and soft warm "
     "light shifting across the grass between the trunks as though something passes through the garden.",
     NOFIG + " " + NOSKY + " " + NOSNAKE),
    ("Hidden among the trees", "Where are you?", [f"{G}/movement/s034.jpg", PR.ADAM, PR.EVE],
     "Deep among dark tree trunks at dusk, layers of trunks and hanging leaves, and far back in the shadows a place "
     "where two people are hiding, unseen, only the hint of two tiny shapes in the dark; evening light reaching in "
     "through the leaves toward them.", PR.FIG_LEAVES + " " + NOSKY),
    ("Dust at the edge of the garden", "He will crush your head", [f"{G}/world/shot-01.jpg"],
     f"Bare dry dust at the edge of the garden in low light, the last trees behind, and far off on the dust, {SNAKE}, "
     "going on its belly through the dust, a faint trail behind it; wind lifting the dust.", NOFIG),
    ("A line of light on the dust", "He will crush your head", [f"{G}/world/shot-01.jpg"],
     "Dawn breaking low over bare dust at the garden's edge: a single long line of gold light falling across the "
     "ground from the low sun, the rest still in deep teal shadow.", NOFIG + " " + NOSNAKE + " " + NOSKY),
    ("The garden under a heavy sky", "Dust you are", [f"{G}/world/shot-04.jpg"],
     f"Seen from a rise, {EDEN}, now under a heavy grey teal sky at dusk, wind bending the long grass, the gold light "
     "almost gone, sorrowful and quiet.", NOFIG + " " + NOSNAKE),
    ("Thorns and thistles", "Dust you are", [f"{G}/world/shot-01.jpg"],
     "Beyond the trees of the garden, a hard open field under a hot pale sky: cracked dry ground, thorn bushes and "
     "tall thistles rising from it, dry wind lifting the dust, the green garden far behind on the horizon.",
     NOFIG + " " + NOSNAKE),
    ("Garments of skin", "Mother of all the living", [f"{G}/world/shot-05.jpg", PR.ADAM, PR.EVE],
     "At the foot of a great tree in warm early light, two rough garments of soft brown animal hide lying loose "
     "over a root, plain shapeless wraps with uneven natural edges, nothing tailored, no seams, no collars, no "
     "buttons, no sleeves, and far beyond them across the glade, two tiny human figures among the trunks.",
     PR.FIG_LEAVES + " No animals, no blood."),
    ("The tree of life, far off", "East of Eden", [f"{G}/world/shot-05.jpg"],
     "The tree of life at the far centre of the garden in soft light, seen from a great distance through the "
     f"trunks of nearer trees, wind in its leaves, the whole garden quiet around it. {FRUIT}",
     NOFIG + " " + NOSNAKE + " Nothing glowing."),
    ("East of Eden", "East of Eden", [f"{G}/movement/s034.jpg"],
     "The eastern edge of the garden at dusk: a wide opening between the great trees, and in the opening a whirling "
     "sword of flame (Genesis 3:24): a long straight blade made only of living fire, upright in the air, turning and "
     "sweeping slowly round, its gold light flashing on the trunks, no hilt, no hand, no one holding it. In the "
     "foreground a wide dry land stretching east, empty.", NOFIG + " No winged figures, no beings, no faces in the "
     "fire, no gate, no wall, no metal sword, no ring, no hoop."),
    ("The wilderness", "The seed of the woman", [f"{G}/world/shot-01.jpg"],
     "A wilderness of stone and dry hills at first light, empty and silent, long shadows, a few low thorn bushes, "
     "nothing living in sight.", NOFIG + " " + NOSNAKE),
    ("The torn curtain", "The way to the tree of life", [f"{G}/world/shot-12.jpg"],
     "A great heavy woven curtain of deep teal and gold cloth hanging in a tall dim stone hall, torn from top to "
     "bottom down its whole length, and warm gold light pouring through the tear into the darkness.",
     NOFIG + " Plain woven cloth with a simple border, no pictures or shapes woven in it."),
]


def main():
    out = ["# The Fall: world bible (M3 look development, photoreal)\n",
           "Look tests at 16:9 for everything The Fall shows that The Garden did not.",
           "Generated by `script/world_bible.py`. Decisions D1 (the serpent), D3 (3:8 by effect), D4",
           "(fig leaves and garments by object) and D5 (3:24, no figures) are written into the prompts.\n",
           f"Eden: {EDEN}.\n"]
    for i, (name, where, refs, scene, excl) in enumerate(ITEMS, 1):
        out += [f"### Shot {i}: {name} ({where})", "- Refs: " + ", ".join(refs), "- Image prompt:",
                f"  > {scene} {excl} {'' if i in OUTSIDE else PR.NEAR_EAST + ' '}{REFNOTE} {SUFFIX}", ""]
    text = "\n".join(out)
    assert "–" not in text and "—" not in text
    prompts = "\n".join(l for l in out if l.startswith("  > ")).lower()
    for w in ["deity", "god figure", "divine being", "halo", "glowing man", "angel", "temple", "idol",
              "serpent", "cherub"]:
        assert w not in prompts, w
    (HERE / "world-bible.md").write_text(text)
    print(f"wrote script/world-bible.md: {len(ITEMS)} prompts")


if __name__ == "__main__":
    main()
