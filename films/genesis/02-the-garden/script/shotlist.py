#!/usr/bin/env python3
"""M4 shot list for The Garden. Shot ids and timings from script/movement-shots.json.
Writes script/shotlist.md (for the still and clip tools) and script/shotlist.json (for the edit).

Kinds: veo (keyframe then Veo), ff (Veo first and last frame), still (keyframe; depth motion in
the edit), reuse (another shot's keyframe). Flags: lite (Veo 3.1 Lite, calm shots), people
(decision D1 wording), calm, dark, last:sNNN (ff end frame), use:sNNN (reuse).

    python3 films/genesis/02-the-garden/script/shotlist.py
"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
SDW = "../01-the-seven-days/stills/world"
SDM = "../01-the-seven-days/stills/movement"
REF = {**{f"g{i:02d}": f"stills/world/shot-{i:02d}.jpg" for i in range(1, 14)},
       "sd_bay": f"{SDW}/shot-01.jpg", "sd_plants": f"{SDW}/shot-02.jpg", "sd_night": f"{SDW}/shot-04.jpg",
       "sd_herds": f"{SDW}/shot-06.jpg", "sd_rest": f"{SDW}/shot-08.jpg", "sd_tomb": f"{SDW}/shot-11.jpg",
       "sd_new": f"{SDW}/shot-12.jpg", "sd_tent": f"{SDM}/s097.jpg", "sd_lamp": f"{SDM}/s056.jpg",
       "sd_thorns": f"{SDM}/s113.jpg"}
EDEN = ("a vast lush garden planted in the east: groves and orderly rows of fruit trees of every kind, open glades "
        "of soft grass, a clear river flowing out of the garden toward the east")
SUFFIX = ("Hand painted matte painting, painterly illustration with visible brush texture and soft canvas grain, "
          "reverent, still and quiet, soft diffused light, restrained palette of deep ink teal (#0E2A2E) shadows, "
          "water teal (#0F6C6C) midtones and warm muted gold (#B8862F) light, warm cream highlights, greens rendered "
          "as deep teal greens within the palette, wide 16:9 cinematic composition with calm space in the lower "
          "third, fully painted edge to edge with no blank or flat areas, full frame with no borders or black bars, "
          "no text, no lettering, no watermark, not photoreal, not cartoon, not 3D render.")
MOTION = ("Painterly matte painting style preserved exactly, brush texture stays visible, slow and steady camera, "
          "no camera shake, no cuts, no text appears.")
CALM = " The water stays calm, no breaking waves, no spray."
NOFIG = "No people, no figures, no faces, no silhouettes."
NOGOD = "No hands and no figure in the sky, in the light or in the wind."
PEOPLE = ("Any human figure is tiny and far away, seen from behind or in profile, framed by trees and light, so "
          "small that no body, clothing or face detail can be seen. No close up, no other people.")
NOCHRIST = "Never a figure meant to be Christ."
REFNOTE = " Match the painting style, palette and light of the reference images."

# id: (kind, scene, motion, refs, flags)
S = {
 # Cold open
 "s001": ("veo", "High above the finished world: a wide crescent bay at rest in long golden light, seen from the sky, everything calm and complete.", "A slow steady descent from the sky toward the ground.", ["sd_rest"], "lite calm"),
 "s002": ("still", "Ground level on wide dry earth at first light, the land empty to the horizon, a calm open space across the middle of the frame.", "Slow push in.", ["g01"], ""),
 # From the heavens to the ground
 "s003": ("still", "A vast sky over a wide empty land at dawn: the heavens and the earth.", "Slow tilt down.", ["g01"], ""),
 "s004": ("still", "A great sky of slow clouds over the land, first light breaking through.", "Slow drift across.", ["g01"], ""),
 "s005": ("veo", "A great sky of slow clouds over a wide empty land at dawn.", "The camera tilts slowly down from the sky to the ground and settles on the earth.", ["g01"], "lite"),
 "s006": ("still", "Dry earth at ground level in close view, fine cracks, tiny beads of moisture catching first light.", "Slow push in.", ["g01"], ""),
 "s007": ("still", "Warm early light falling low and close across the empty land, as though drawing near, with no source visible.", "Slow push in.", ["g01"], ""),
 "s008": ("still", "The empty land in widening morning light.", "Slow pull back.", ["g01"], ""),
 "s009": ("still", "From high above, a wide crescent bay with herds grazing on the green hills: the sixth day, seen again.", "Slow push down toward the land.", ["sd_herds", "sd_bay"], ""),
 "s010": ("still", "One patch of bare ground seen from close above, quiet and ready.", "Slow push in.", ["g01"], ""),
 # Dust and breath
 "s011": ("veo", "A barren plain with no shrub and no plant, under a pale sky with no rain, a dry wind lifting a little dust.", "A dry wind moves fine dust low across the ground; slow lateral drift.", ["g01"], "lite"),
 "s012": ("still", "An empty field with no plant anywhere, a pale cloudless sky.", "Slow push in.", ["g01"], ""),
 "s013": ("veo", "Springs welling up from the earth, water spreading over the dust, mist rising over the whole surface of the ground.", "Water wells up and spreads over the dust; mist drifts upward.", ["g01"], "lite"),
 "s014": ("still", "A wide damp field after the springs, darkened earth, with no one there to work it.", "Slow pull back.", ["g01"], ""),
 "s015": ("still", "A very wide plain of damp earth at dawn; far away, tiny in the frame, a whirl of dust and a soft column of warm light, and in the veil of dust the faint low outline of a man lying on the earth, no more than a long low mound.", "Very slow push in.", ["g02"], "noanatomy"),
 "s016": ("veo", "Far away on the ground at first light, a man lying where he was formed, and a breath of wind and warm light passing over him like a living current, the grass bending.", "The current of wind and light passes slowly over the distant man and the grass; nothing else moves.", ["g03"], "people"),
 "s017": ("still", "Clay vessels drying in a row in soft light beside a still potter's wheel.", "Slow drift across.", [], "nofig"),
 "s018": ("still", "Wet clay on a potter's wheel in close view, smooth and shaped, catching soft light.", "Slow push in.", [], "nofig"),
 "s019": ("still", "Far away on the ground at morning, the man lying in the grass now alive, wind in the grass around him.", "Slow pull back.", ["g03"], "people"),
 "s020": ("still", "Rich red brown earth of the field in close view, the ground the man was taken from.", "Slow push in.", ["g01"], ""),
 "s021": ("still", "Wind moving over grass at dawn, light streaming low across it.", "Slow drift across.", ["g03"], ""),
 # A garden in Eden
 "s022": ("ff", "Wide bare land in the east at first light, empty of trees.", "Trees rise and spread across the land until a lush garden fills it, the river flowing out through it.", ["g01", "g04"], "last:s023"),
 "s023": ("still", f"Seen from a rise, {EDEN}. Every tree pleasing to the eye and good for food.", "Slow push in.", ["g04"], ""),
 "s024": ("still", "At the centre of the garden in a quiet glade, two great living trees standing apart in soft light, both full of leaves and fruit, each a different kind.", "Slow push in.", ["g05"], ""),
 "s025": ("veo", "A glade in the garden with fruit trees, soft grass and light falling through the leaves.", "A soft breeze moves the leaves and light dapples the grass.", ["g04"], "lite"),
 "s026": ("still", "The two great trees at the centre of the garden seen a little closer, both living and fruitful, standing apart.", "Very slow push in.", ["g05"], ""),
 "s027": ("veo", "A clear river flowing out of the garden toward the east between banks of trees.", "The river flows steadily out of the garden; leaves stir on the banks.", ["g04", "g06"], "calm"),
 "s028": ("veo", "From very high above, one river flowing out of a green garden and dividing into four great headwaters winding across a vast land, gold glinting in the riverbeds.", "Slow forward glide high above the rivers.", ["g06"], "calm"),
 "s029": ("still", "A clear shallow riverbed: pure gold, pale bdellium resin and dark banded onyx among the pebbles under moving water.", "Slow push in.", ["g07"], ""),
 "s030": ("still", "Ground level beside a broad river winding through a dry southern land of low ochre hills and scattered palms, far from the garden.", "Slow drift across.", [], ""),
 "s031": ("still", "Two great rivers flowing side by side across a flat green plain under a wide sky, low hills on the far horizon, seen from a riverbank.", "Slow pull back.", [], ""),
 "s032": ("still", "Four rivers far below in a vast land, two clear and two fading away into haze, beyond reach.", "Slow pull back.", ["g06"], ""),
 "s033": ("still", "Mist over the headwaters where the river divides, early light.", "Slow push in.", ["g06"], ""),
 "s034": ("still", "The eastern side of the garden: a wide opening between great trees facing the rising light.", "Slow push in.", ["g04"], ""),
 "s035": ("still", "A woven tent sanctuary in the desert, its entrance facing east toward the dawn, curtains of blue, purple and scarlet.", "Slow push in.", ["sd_tent"], "nofig"),
 # To cultivate and keep
 "s036": ("still", "Far away, a tiny man walking into the garden through its eastern opening, the great trees around him.", "Slow push in.", ["g08", "g04"], "people"),
 "s037": ("still", f"Inside the garden in early light, groves of fruit trees, and far away between the trees a man at work tending the ground.", "Slow drift across.", ["g08"], "people"),
 "s038": ("still", "Rows of young fruit trees and tended soil in morning light, a small water channel running between them.", "Slow push in.", ["g04"], ""),
 "s039": ("still", "Inside a tent of heavy woven curtains, a seven branched golden lampstand with small flames burning.", "Slow push in.", ["sd_lamp"], "nofig"),
 "s040": ("still", "Stillness at the centre of the garden: the tree of the knowledge of good and evil standing alone in its glade, leaves stirring.", "Very slow push in.", ["g05"], ""),
 "s041": ("veo", "The two great trees at the centre of the garden in a quiet glade.", "Wind moves softly through the leaves of the great trees; nothing else moves.", ["g05"], "lite"),
 "s042": ("veo", "Groves of the garden heavy with fruit of every kind in warm light.", "A gentle breeze moves the branches and the fruit sways.", ["g04"], "lite"),
 "s043": ("still", "A single fruit tree heavy with fruit, generous and full, in warm light.", "Slow push in.", ["g04"], ""),
 "s044": ("still", "The tree of the knowledge of good and evil alone in its glade, beautiful and still.", "Slow pull back.", ["g05"], ""),
 "s045": ("still", "Late light over the garden, a long shadow from the tree reaching across the glade.", "Slow push in.", ["g05"], ""),
 "s046": ("still", "Leaves and fruit of the great tree in close view, beautiful, nothing glowing.", "Slow push in.", ["g05"], ""),
 "s047": ("still", "Far off, a tiny man sitting beneath a tree at evening, looking out over the garden.", "Slow pull back.", ["g08"], "people"),
 "s048": ("still", "The garden at evening, calm, the river catching the last light.", "Slow drift across.", ["g04"], "calm"),
 # Not good to be alone
 "s049": ("still", "The man alone at evening in the wide garden, very small among the trees.", "Very slow push in.", ["g08"], "people"),
 "s050": ("still", "An empty glade at dusk with a single path, quiet.", "Slow push in.", ["g04"], ""),
 "s051": ("still", "Hill country at dawn, ranges of hills fading into the distance, strong and still.", "Slow tilt up.", [], "nofig"),
 "s052": ("still", "Morning light rising over the hills, strength and help.", "Slow pull back.", [], "nofig"),
 "s053": ("still", "Two great trees side by side facing each other across a glade, a matched pair.", "Slow push in.", ["g05"], ""),
 "s054": ("veo", "A wide meadow in the garden: deer, oxen, wild goats, a lion and birds coming across the grass one after another toward a tiny distant man at the far edge.", "The animals walk slowly across the meadow; birds glide in to land.", ["g09"], "people"),
 "s055": ("still", "Birds of many kinds landing in the branches of the garden.", "Slow drift across.", ["g09"], ""),
 "s056": ("still", "Far off at the edge of a meadow, the tiny man with animals standing before him one by one.", "Slow push in.", ["g09"], "people"),
 "s057": ("still", "Animals grazing in pairs across the meadow, each with its kind, and far off the man alone at the edge.", "Slow pull back.", ["g09"], "people"),
 "s058": ("still", "The man alone at the far edge of the meadow at dusk, the animals moving away.", "Very slow push in.", ["g09"], "people"),
 # Bone of my bones
 "s059": ("veo", "The garden at night under stars, and far away beneath a great tree a man lying asleep.", "Very slow push in; the stars glint and the leaves barely stir.", ["g10"], "lite people"),
 "s060": ("still", "The garden at night, far off a man asleep beneath a great tree, a soft warm light gathering quietly near him.", "Very slow push in.", ["g10"], "people"),
 "s061": ("still", "A desert night under countless stars, a single small campfire glowing far away.", "Slow tilt up.", ["sd_night"], "nofig"),
 "s062": ("still", "The night garden under stars, deep and still.", "Slow drift across.", ["g10"], ""),
 "s063": ("still", "First light of dawn over the garden and the great tree where the man slept.", "Slow push in.", ["g10", "g04"], ""),
 "s064": ("still", "Morning light in the garden; far across a glade two tiny human figures meeting among the trees, a man and a woman.", "Very slow push in.", ["g11"], "people"),
 "s065": ("still", "Seen from a hill above the garden, the whole green garden spread below in morning light, and far down in a glade two tiny figures together, barely visible.", "Slow pull back.", ["g04", "g11"], "people"),
 "s066": ("still", "The garden in morning light, birdsong in the branches, peace.", "Slow drift across.", ["g04"], ""),
 "s067": ("still", "Two paths crossing a morning field and joining into one.", "Slow push in.", ["g04"], ""),
 "s068": ("still", "Two vines grown together around one another on a living trellis, in warm light.", "Slow push in.", [], "nofig"),
 "s069": ("veo", "The garden in full light, and far off two tiny figures among the trees.", "A soft breeze moves through the trees; the figures stay small and still.", ["g11"], "lite people"),
 "s070": ("still", "Two tiny figures far off among the trees in full warm light, peace and no fear.", "Very slow push in.", ["g11"], "people"),
 "s071": ("still", "The whole garden in full light from a rise, the two figures too small to see.", "Slow pull back.", ["g04"], ""),
 "s072": ("still", "The two great trees at the centre in late light, a stillness, a long shadow across the glade.", "Very slow push in.", ["g05"], ""),
 # The last Adam
 "s073": ("still", "A garden at dawn: an olive grove on a hillside, dew on the grass.", "Slow push in.", ["g12"], "nofig christ"),
 "s074": ("still", "First light over the olive grove, a breath of wind in the leaves.", "Slow drift across.", ["g12"], "nofig christ"),
 "s075": ("veo", "An olive grove on a hillside at night under a pale moon, old twisted trees, the city wall faint across a valley.", "Wind moves through the olive leaves under the moon; very slow push in.", ["g12"], "lite nofig christ"),
 "s076": ("still", "The olive grove at night, empty, the city across the valley.", "Slow pull back.", ["g12"], "nofig christ"),
 "s077": ("still", "A rock cut tomb in a garden hillside at first light, the great round stone rolled back from the open entrance.", "Slow push in.", ["sd_tomb"], "nofig christ"),
 "s078": ("veo", "The empty tomb in the garden at first light, folded linen just visible inside.", "Sunlight slowly reaches into the open entrance and falls across the folded linen.", ["sd_tomb"], "nofig christ"),
 "s079": ("still", "An upper room at evening, lamps lit, the doors shut, the room empty.", "Slow push in.", ["sd_lamp"], "nofig christ"),
 "s080": ("veo", "An evening room with an open window and lamps burning.", "A breath of wind and warm light moves in through the window and passes through the room; the lamp flames bend.", ["sd_lamp"], "nofig christ"),
 "s081": ("still", "A long wedding table set beneath a tree with lamps hung in the branches, waiting.", "Slow drift across.", ["g04"], "nofig christ"),
 "s082": ("still", "Dawn over the garden with a city of light far beyond it.", "Slow push in.", ["g04", "g13"], "nofig christ"),
 # Eden restored
 "s083": ("still", "Thorns and dry ground under a grey sky, the ground cursed.", "Slow pan.", ["sd_thorns"], "nofig"),
 "s084": ("still", "The eastern edge of the garden at dusk seen from far outside it: a wide opening between great trees, glowing faintly, far away and out of reach. No gate, no arch, no wall, no building.", "Slow pull back.", ["g04"], "nofig"),
 "s085": ("veo", "A radiant city of light with a clear river flowing down its great street, fruit trees on both banks, lit from everywhere.", "Light swells softly; the river flows; slow push toward the city.", ["g13"], "calm nofig"),
 "s086": ("veo", "The tree of life on both banks of the clear river in the city, heavy with fruit, leaves catching the light.", "The river flows and leaves stir gently.", ["g13"], "lite calm nofig"),
 "s087": ("still", "Fruit and leaves of the tree of life in close view beside the shining river.", "Slow push in.", ["g13"], "nofig"),
 "s088": ("still", "Wide: the garden city in light, the river winding through groves of fruit trees, the city of light rising beyond. No houses in the foreground, no ordinary buildings.", "Slow pull back.", ["g13"], "nofig"),
 # Dust that breathes
 "s089": ("veo", "Damp earth at first light and a breath of wind lifting a little dust.", "A breath of wind moves fine dust low over the ground and passes on; light rises.", ["g01", "g03"], "lite"),
 "s090": ("still", "Wind moving over grass at dawn.", "Slow drift across.", ["g03"], ""),
 "s091": ("still", "Dawn light spreading over the land and the garden beyond.", "Slow push in.", ["g04"], ""),
 "s092": ("still", f"The garden in calm morning light, {EDEN}, wide open space across the middle of the frame.", "Very slow push in.", ["g04"], ""),
}

BEFORE_MAN = {f"s{i:03d}" for i in range(1, 16)}


def main():
    shots = json.loads((HERE / "movement-shots.json").read_text())
    assert [s["id"] for s in shots] == sorted(S), "shot ids do not match movement-shots.json"
    banned = ["deity", "god figure", "divine being", "halo", "glowing man", "angel", "temple", "idol"]
    md = ["# The Garden: shot list (M4)\n", "Generated by `script/shotlist.py`. Decisions D1, D2 and D4 are in every prompt.\n"]
    out, counts = [], {}
    for i, sh in enumerate(shots, 1):
        kind, scene, motion, refs, flags = S[sh["id"]]
        counts[kind] = counts.get(kind, 0) + 1
        if "people" in flags:
            excl = PEOPLE
        elif "noanatomy" in flags:
            excl = "No anatomy, no visible body detail, no standing figures, no people anywhere else, no close up."
        else:
            excl = NOFIG
        excl += " " + NOGOD + (" " + NOCHRIST if "christ" in flags else "")
        if sh["id"] in BEFORE_MAN and "people" not in flags and "noanatomy" not in flags:
            excl += " No person exists yet."
        m = motion + (CALM if "calm" in flags else "")
        prompt = f"{scene} {excl}{REFNOTE if refs else ''} {SUFFIX}"
        mprompt = f"{m} {MOTION}"
        low = (prompt + mprompt).lower()
        for w in banned:
            assert w not in low, f"{sh['id']}: banned word {w}"
        assert "–" not in prompt + mprompt and "—" not in prompt + mprompt
        out.append(dict(sh, kind=kind, scene=scene, prompt=prompt, motion=mprompt, refs=[REF[r] for r in refs],
                        flags=flags))
        md.append(f"### Shot {i}: {sh['id']} {sh['chapter']} ({sh['dur']:.1f} s, {kind}{', lite' if 'lite' in flags else ''})")
        if refs:
            md.append("- Refs: " + ", ".join(REF[r] for r in refs))
        md += ["- Image prompt:", f"  > {prompt}"]
        md += (["- Motion prompt:", f"  > {mprompt}"] if kind in ("veo", "ff") else [f"- Edit move: {motion}"])
        md.append("")
    (HERE / "shotlist.md").write_text("\n".join(md))
    (HERE / "shotlist.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    lite = sum(1 for s in out if "lite" in s["flags"])
    print(f"wrote script/shotlist.md: {len(shots)} shots {counts}; Veo {counts.get('veo', 0) + counts.get('ff', 0)} "
          f"({lite} Lite)")


if __name__ == "__main__":
    main()
