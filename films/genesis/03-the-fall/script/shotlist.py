#!/usr/bin/env python3
"""M4 shot list for The Fall. Shot ids and timings from script/movement-shots.json.
Writes script/shotlist.md (for the still and clip tools) and script/shotlist.json (for the edit).

Kinds: veo (keyframe then Veo), ff (Veo first and last frame), still (keyframe; depth motion in
the edit), reuse (another shot's keyframe). Flags: lite (Veo 3.1 Lite, calm shots), people
(tiny distant figures), snake (decision D1 wording), calm, christ, nofig, use:sNNN (reuse),
copy:PATH (keyframe copied from another film, never generated), clip:A-B (trim a clip).

    python3 films/genesis/03-the-fall/script/shotlist.py
"""
import json, pathlib, shutil

HERE = pathlib.Path(__file__).resolve().parent
FILM = HERE.parent
G = "../02-the-garden/stills"
REF = {**{f"f{i:02d}": f"stills/world/shot-{i:02d}.jpg" for i in range(1, 15)},
       **{f"g{i:02d}": f"{G}/world/shot-{i:02d}.jpg" for i in range(1, 14)},
       "g_open": f"{G}/movement/s034.jpg", "g_tent": f"{G}/movement/s035.jpg",
       "g_tomb": f"{G}/movement/s077.jpg", "g_linen": f"{G}/movement/s078.jpg",
       "m057": "stills/movement/s057.jpg", "m098": "stills/movement/s098.jpg", "m074": "stills/movement/s074.jpg"}
EDEN = ("a vast lush garden planted in the east: groves and orderly rows of fruit trees of every kind, open glades "
        "of soft grass, a clear river flowing out of the garden toward the east")
SNAKE = ("a small ordinary snake, slender and muted dark olive teal, seen from far away so it is only a thin dark "
         "curve, natural and unremarkable, mouth closed, no legs, nothing monstrous")
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
NOSNAKE = "No snake."
NOCHRIST = "Never a figure meant to be Christ."
FRUIT = "Any fruit is round and of no particular kind, not apples."
REFNOTE = " Match the painting style, palette and light of the reference images."

# id: (kind, scene, motion, refs, flags)
S = {
 # Cold open (decision D10: The Garden's own last keyframes, then a movement in the grass)
 "s001": ("still", "", "Very slow push in.", [], f"copy:{G}/movement/s092.jpg"),
 "s002": ("still", "", "Slow drift across.", [], f"copy:{G}/world/shot-11.jpg"),
 "s003": ("veo", f"Long soft grass at the edge of a sunlit glade in the garden, morning light, the trees of {EDEN.split(':')[0]} beyond.", "The grass at the lower edge of the frame parts and ripples as something small moves through it, unseen, then the grass is still. Slow push in.", ["g04", "f01"], "nofig"),
 # Did God really say?
 "s004": ("veo", f"Inside the garden in late afternoon: long soft grass at the foot of great fruit trees, and in the middle distance {SNAKE}, moving through the grass toward the centre of the garden.", "The small snake glides slowly through the grass away from the camera; the grass stirs; slow push in.", ["f01"], "nofig snake"),
 "s005": ("still", f"Ground level between two great dark tree trunks that frame the view, low golden light, long shadows across the grass, and in the middle distance between them {SNAKE}, lying still.", "Slow push in.", ["f05"], "nofig snake"),
 "s006": ("still", "A wide sunlit meadow in the garden full of tall flowering grass from edge to edge, painted all the way to the bottom of the frame, trees around it, and far off in the middle of the meadow two tiny human figures in full light, at peace, unashamed, no bigger than grass heads.", "Slow drift across.", ["g05"], "people"),
 "s007": ("still", f"Ground level in long grass at the edge of the garden, blades catching the low sun, and far down a path through the grass {SNAKE}.", "Slow push in.", ["f01"], "nofig snake"),
 "s008": ("still", f"The open edge of the garden where it meets a natural meadow of wild grass and flowers: deer and wild goats grazing in the late light, beasts of the field, and among the grass far off {SNAKE}, one creature among the others. No walls, no fences, no stones laid in rows, no garden beds, nothing built.", "Slow pull back.", ["g04"], "nofig snake"),
 "s009": ("still", f"Low at the foot of one massive old tree trunk at dusk, its roots spreading across the grass, the light withdrawing behind it, and in the dark grass between the roots, far off, {SNAKE}.", "Very slow push in.", ["g05"], "nofig snake"),
 "s010": ("still", "A narrow path of flattened grass winding through the long grass toward the great tree in the middle of the garden, which stands small and far off at the end of it.", "Slow push in.", ["f01"], "nofig"),
 "s011": ("still", f"The great tree in the middle of the garden, heavy with fruit, seen from far off between other trunks; beneath it, very small, one human figure in profile, and low in the grass near her {SNAKE}. {FRUIT}", "Slow push in.", ["f02"], "people snake"),
 "s012": ("still", "Branches of the tree in the middle of the garden in close view against the light, heavy round fruit hanging among dark leaves. " + FRUIT, "Slow drift across.", ["f02"], "nofig"),
 "s013": ("veo", f"Orchard rows of fruit trees in the garden, {EDEN.split(':')[1].split(',')[0].strip()}, laden with fruit in warm afternoon light. " + FRUIT, "A soft breeze moves the leaves and the fruit sways gently; slow lateral drift.", ["g04"], "lite nofig"),
 "s014": ("still", f"Seen from a rise, {EDEN}, and at the very centre, small and apart, one great tree in a glade.", "Slow push in.", ["g04", "g05"], "nofig"),
 "s015": ("still", f"Ground level behind the great roots of the tree in the middle of the garden: grass and roots in the foreground, {SNAKE} in the grass a little way off, and far beyond, very small, one human figure in profile.", "Very slow push in.", ["f02", "f01"], "people snake"),
 "s016": ("still", "Light slanting down through the canopy of the tree in the middle of the garden, gold through the leaves, seen from beneath.", "Slow tilt up.", ["f02"], "nofig"),
 "s017": ("still", "The long shadow of the great tree falling across the grass as the sun lowers, the glade half in shadow.", "Slow drift across.", ["g05"], "nofig"),
 "s018": ("still", "A glade of laden fruit trees in warm light, fruit on every branch, everything given and nothing held back. " + FRUIT, "Slow pull back.", ["g04"], "nofig"),
 "s019": ("veo", "The clear river flowing out of the garden in quiet late light, trees on both banks.", "The river flows slowly and steadily; leaves stir on the banks; slow push in.", ["g04"], "lite nofig calm"),
 "s020": ("still", "The low sun behind the garden, long gold light lying across an empty glade.", "Slow push in.", ["g05"], "nofig"),
 # She took and ate
 "s021": ("still", f"The great tree in the middle of the garden in warm light, heavy with fruit, framed by its own branches, and beneath it two very small figures, far off. {FRUIT}", "Very slow push in.", ["f02", "g05"], "people"),
 "s022": ("still", "One branch of the tree in close view, round fruit of no particular kind hanging in warm light, one place on the branch where a fruit is missing. Not apples.", "Slow push in.", ["f02"], "nofig"),
 "s023": ("still", "The crown of the great tree seen from far below, reaching up into the gold light.", "Slow tilt up.", ["f02"], "nofig"),
 "s024": ("still", "Ground level across the grass toward the distant great tree, a fallen leaf in the near foreground, evening coming.", "Slow push in.", ["g05"], "nofig"),
 "s025": ("still", "Fruit trees on the bank of the calm river, reflected in the still water in late light. " + FRUIT, "Slow drift across.", ["g04"], "nofig"),
 "s026": ("still", "Far across the river, beneath the great tree, two tiny human figures side by side, still and silent, seen in profile.", "Very slow push in.", ["g11", "f02"], "people"),
 "s027": ("still", "Broad lobed fig leaves filling the near foreground, dark against the evening light, and far beyond them through a gap in the leaves, two tiny human figures withdrawn into the deep shade of the trees.", "Slow push in.", ["f03"], "people"),
 "s028": ("veo", "Extreme close view of broad lobed fig leaves filling the whole frame, their veins lit from behind by the evening light, nothing else visible.", "The fig leaves stir slowly in a light evening breeze; slow drift across.", [], "lite nofig"),
 "s029": ("still", "The sun sinking behind the garden, the treetops dark against a deepening amber sky, seen from low in an open glade.", "Slow pull back.", ["g05"], "nofig"),
 "s030": ("still", "The glade of the great tree in the first evening shadow, empty.", "Slow push in.", ["g05"], "nofig"),
 # Where are you? (decision D3: by wind, sound and light only)
 "s031": ("veo", "Evening in the garden: tall trees, their crowns catching the last light, soft warm light lying across the grass between the trunks.", "A long slow wave of wind moves through the treetops from one side of the frame to the other, leaves turning silver, and soft light shifts across the grass between the trunks, as though something passes through the garden. Nothing appears. Slow push in.", ["f04"], "nofig"),
 "s032": ("still", "Looking straight up into the crown of one great tree at evening, leaves turning silver in the wind against the sky.", "Slow drift across.", ["g05"], "nofig"),
 "s033": ("still", "Ground level in a glade at evening: tall grass bending in a long wave of wind, warm light moving across it, a few trunks at the edges.", "Slow push in.", ["g05"], "nofig"),
 "s034": ("still", f"From high above at evening, {EDEN}, wind passing over the whole garden in a long wave across the treetops.", "Slow push down.", ["g04"], "nofig"),
 "s035": ("veo", "Deep among dark tree trunks at dusk, layers of trunks and hanging leaves, and far back in the shadows the hint of two tiny hidden shapes, unseen; warm evening light reaching in through the leaves.", "Soft warm light slowly reaches in through the leaves toward the hidden place, moving across the trunks; leaves stir; very slow push in.", ["f05"], "people"),
 "s036": ("still", "From deep inside a dark thicket of leaves and branches, looking out through a small gap toward a glade still lit by the evening light, the leaves close and dark around the edge of the frame.", "Very slow push in.", ["f05"], "nofig"),
 "s037": ("still", "A narrow gap between two great dark trunks at dusk, a thin line of evening light reaching in.", "Slow push in.", ["f05"], "nofig"),
 # The woman whom You gave me
 "s038": ("still", f"The garden in failing light; two far off figures half hidden among dark trunks; in the low grass between the trees {SNAKE}, lying still.", "Very slow push in.", ["f05", "f01"], "people snake"),
 "s039": ("still", "The great tree in the middle of the garden at dusk, dark against a fading sky.", "Slow push in.", ["f02"], "nofig"),
 "s040": ("still", "A darkening open glade with the great tree on one side, and at the far edge of the glade two tiny human figures standing apart, seen in profile.", "Slow drift across.", ["g05"], "people"),
 "s041": ("still", "A natural still pool among reeds and grass in the garden at dusk, its edges soft and uneven, reflecting the dark trees and the last of the sky. No stone edges, nothing built.", "Slow push in.", ["g05"], "nofig calm"),
 "s042": ("still", "Far off near the great tree at dusk, one tiny human figure in profile among the trunks.", "Very slow push in.", ["f02", "g11"], "people"),
 "s043": ("still", f"Long grass in deep dusk shadow, and far off in it {SNAKE}.", "Slow push in.", ["f01"], "nofig snake"),
 "s044": ("still", "A path through the long grass from the great tree into the trees, at dusk.", "Slow push in.", ["f01"], "nofig"),
 "s045": ("still", "Dusk wind over the long grass at the edge of the garden, the light almost gone.", "Slow drift across.", ["f08"], "nofig"),
 # He will crush your head
 "s046": ("veo", f"Bare dry dust at the edge of the garden in low light, the last trees behind, and far off on the dust {SNAKE}, a faint trail behind it.", "The small snake goes slowly on its belly across the dust, away from the camera; wind lifts a little dust; slow push in.", ["f06"], "nofig snake"),
 "s047": ("still", "Bare dust at ground level in close view, a faint winding trail drawn through it, low light.", "Slow push in.", ["f06"], "nofig"),
 "s048": ("still", "A wide flat plain of bare dust seen from high above at dusk, the edge of the green garden along one side of the frame like a dark shore.", "Slow pull back.", [], "nofig"),
 "s049": ("still", "Bare dust in the near foreground, and far beyond it a green meadow at peace where a wolf and a lamb graze side by side.", "Slow push in.", ["g04", "f06"], "nofig"),
 "s050": ("veo", "Dawn breaking low over bare dust at the garden's edge: a single long line of gold light lying across the ground, the rest in deep teal shadow.", "The line of gold light widens very slowly across the ground as dawn grows; fine dust drifts in the light; the light stays soft and even, no flare. Slow push in.", ["f07"], "nofig"),
 "s051": ("still", "A dark sky over bare dust, first light breaking along the far horizon.", "Slow pull back.", ["f07"], "nofig"),
 "s052": ("still", "Close view of the bare ground where the first gold light touches it: cracked dust, small stones and grains catching the light, the rest in shadow.", "Slow push in.", ["f07"], "nofig"),
 "s053": ("still", "Where shadow meets light on the bare ground, a sharp edge between deep teal dark and gold.", "Slow drift across.", ["f07"], "nofig"),
 "s054": ("still", "Dawn rising over the whole land beyond the garden, wide and quiet.", "Slow pull back.", ["f07", "g04"], "nofig"),
 "s055": ("still", "Morning light on the trunks and grass of a quiet glade in the garden, dew on the grass, soft and even.", "Very slow push in.", ["g05"], "nofig"),
 # Dust you are
 "s056": ("veo", "Long grass in the near foreground bending under a heavy grey teal sky at dusk, and the dark line of the garden's trees on the horizon, the gold light almost gone.", "Wind bends the long grass in slow waves; clouds drift slowly; slow push in.", ["m057"], "lite nofig"),
 "s057": ("still", "A pale break in heavy grey clouds over a dark line of trees, a few thin rays falling on a distant field, seen across low grass.", "Slow drift across.", [], "nofig"),
 "s058": ("still", "A single tree bent by the wind on a ridge at dusk, under a heavy sky.", "Slow push in.", ["f08"], "nofig"),
 "s059": ("still", "Heavy rain clouds over a wide empty plain beyond the garden at dusk, veils of rain falling far off.", "Slow pull back.", ["m057"], "nofig"),
 "s060": ("veo", "Beyond the trees of the garden, a hard open field under a hot pale sky: cracked dry ground, thorn bushes and tall thistles, the green garden far behind on the horizon.", "A dry wind moves through the thorns and thistles and lifts fine dust low across the ground; slow lateral drift.", ["f09"], "lite nofig"),
 "s061": ("still", "Thorn bushes in close view over cracked ground in hard light.", "Slow push in.", ["f09"], "nofig"),
 "s062": ("still", "Hard furrows in dry stony ground under a hot sky, the earth resisting.", "Slow drift across.", ["f09"], "nofig"),
 "s063": ("still", "Tall thistle heads catching the light, dry seed drifting from them.", "Slow push in.", ["f09"], "nofig"),
 "s064": ("still", "A thin field of grain bending in a hot wind, dust in the air, a pale sun.", "Slow drift across.", ["f09"], "nofig"),
 "s065": ("still", "Dry dust blowing from bare ground in close view, low light.", "Slow push in.", ["g01"], "nofig"),
 "s066": ("veo", "Wide bare dry ground at evening, empty.", "A breath of dry wind moves fine dust low over the ground and passes on; slow drift.", ["g01"], "lite nofig"),
 "s067": ("still", "Beyond the dry field, the garden at dusk with a last gold light on its trees.", "Slow push in.", ["f09", "g04"], "nofig"),
 "s068": ("still", "Night over the garden: dark treetops against a deep teal sky with the first faint stars, seen from low in a glade.", "Slow pull back.", ["g05"], "nofig"),
 # Mother of all the living
 "s069": ("veo", "First light in the garden after the night: low mist lying in a glade among great trunks, the morning light just reaching it.", "Morning light slowly spreads across the glade and the mist lifts; slow push in.", ["g05"], "lite nofig"),
 "s070": ("still", "First light at the edge of a misty glade seen from far across it, a great tree on the far side, and beneath it two very small human figures standing together, seen from far behind, much smaller than the tree trunk is wide.", "Very slow push in.", ["g05"], "people"),
 "s071": ("still", "At the foot of a great tree in warm early light, two rough garments of soft brown animal hide lying loose over a root, plain shapeless wraps with uneven natural edges, nothing tailored, no seams, collars, buttons or sleeves, and far beyond them across the glade, two tiny human figures among the trunks.", "Slow push in.", ["f10"], "people"),
 "s072": ("still", "Close view of two rough garments of soft brown animal hide, plain shapeless wraps with uneven natural edges lying over a tree root in warm light, filling most of the frame, nothing tailored, no seams, collars, buttons or sleeves.", "Very slow push in.", ["f10"], "nofig"),
 "s073": ("still", "A quiet glade at morning, light and shadow lying across the grass.", "Slow drift across.", ["g05"], "nofig"),
 "s074": ("still", "Two tiny human figures walking along the river bank in morning light, seen from far behind, trees along the water.", "Slow drift across.", ["g05"], "people calm"),
 # East of Eden (decision D5: no figures at the opening, a turning flame only)
 "s075": ("still", "The tree of life at the far centre of the garden in soft light, seen from a great distance through the trunks of nearer trees, wind in its leaves. " + FRUIT, "Very slow push in.", ["f11"], "nofig"),
 "s076": ("still", "Close view of the leaves and round fruit of the tree of life in soft light, a branch filling the frame. Nothing glowing. Not apples.", "Slow push in.", ["f11"], "nofig"),
 "s077": ("still", "The whole garden seen from far outside at dusk: a long dark line of trees across a dry plain, the last light behind them.", "Slow pull back.", ["f12"], "nofig"),
 "s078": ("veo", "Seen from inside the garden, looking out through a wide opening between great trees onto a wide dry land in the evening, and far out on the dry land two tiny human figures walking away from the garden, seen from behind.", "The two tiny figures walk slowly away into the dry land; the camera stays inside the garden and does not follow; dust drifts.", ["f12", "m074"], "people"),
 "s079": ("veo", "The eastern edge of the garden at dusk: a wide opening between the great trees, and standing in the opening a slow turning ring of flame, bright gold fire circling in the air like a wheel, lighting the trunks, nothing and no one inside the ring.", "The ring of flame turns slowly and steadily in the opening, its light flickering on the trunks; nothing else moves; very slow push in.", ["f12", "g_open"], "nofig fire"),
 "s080": ("still", "The eastern opening of the garden seen from far outside across dry land at dusk, a small turning flame of light standing in it, far away and out of reach.", "Slow pull back.", ["f12"], "nofig fire"),
 "s081": ("still", "A woven tent sanctuary in the desert at dawn, its entrance facing east toward the rising light, its curtains in muted deep teal and dull gold cloth, drawn.", "Slow push in.", ["g_tent"], "nofig"),
 "s082": ("still", "A wide dry land stretching east under the evening sky, a faint path leading away into the distance.", "Slow push in.", ["f12"], "nofig"),
 "s083": ("still", "Far behind on the horizon, the garden a dark line of trees at nightfall, the land between empty.", "Slow pull back.", ["f12"], "nofig"),
 # The seed of the woman (decision D6: settings only)
 "s084": ("veo", "A wilderness of stone and dry hills at first light, empty and silent, long shadows.", "Slow lateral drift across the hills; light slowly grows.", ["f13"], "lite nofig christ"),
 "s085": ("still", "A stone manger filled with straw in a dim lamplit shelter at night, empty and quiet.", "Slow push in.", [], "nofig christ"),
 "s086": ("still", "A dry stream bed winding between flat stone ledges in the wilderness at noon, close to the ground, bare rock, empty, no mountains.", "Slow drift across.", [], "nofig christ"),
 "s087": ("still", "Flat round stones lying on the dry ground of the wilderness in close view, hard light.", "Slow push in.", ["f13"], "nofig christ"),
 "s088": ("veo", "An olive grove on a hillside at night under a pale moon, old twisted trees, across a dry stream bed.", "Wind moves through the olive leaves under the moon; very slow push in.", ["g12"], "lite nofig christ"),
 "s089": ("still", "Thorny branches against a darkening sky, close view.", "Slow push in.", ["f09"], "nofig christ"),
 "s090": ("still", "A rock cut tomb in a garden hillside at first light, the great round stone rolled back from the open entrance.", "Slow push in.", ["g_tomb"], "nofig christ"),
 "s091": ("still", "Inside the open tomb, sunlight reaching in across folded linen lying on the stone ledge.", "Slow push in.", ["g_linen"], "nofig christ"),
 "s092": ("still", "Dawn over a garden hillside of olive and fig trees, and far beyond across a valley an ancient walled city of low flat roofed stone houses, light breaking over the trees. No towers, no modern buildings.", "Slow pull back.", ["g_tomb"], "nofig christ"),
 "s093": ("still", "Full morning sunlight over the garden hillside of the tomb, quiet.", "Very slow push in.", ["g_tomb"], "nofig christ"),
 # The way to the tree of life
 "s094": ("veo", "A great heavy woven curtain of deep teal and gold cloth hanging in a tall dim stone hall, torn from top to bottom down its whole length, warm gold light coming through the tear.", "Warm light slowly pours through the tear and spreads across the dark floor; the torn edges sway gently; slow push in.", ["f14"], "nofig christ"),
 "s095": ("still", "Close view of the torn edge of the great woven cloth, heavy threads pulled apart, warm gold light pouring through the gap.", "Slow push in.", ["f14"], "nofig christ"),
 "s096": ("still", "A radiant city made of light with a clear river flowing down its great street, trees heavy with fruit on both banks, lit from everywhere with no sun and no moon. No domes, no spires, no towers, no ordinary buildings.", "Slow push in.", ["g13"], "nofig calm"),
 "s097": ("still", "The tree of life on the bank of the shining river in full light, fruit and leaves, open to all.", "Slow pull back.", ["g13"], "nofig calm"),
 "s098": ("veo", "Back in the garden at evening, tall trees and soft light between the trunks.", "Wind moves gently through the trees and soft light moves slowly between the trunks; slow push in.", ["f04"], "lite nofig"),
 "s099": ("reuse", "", "Slow pull back.", [], "use:s072"),
 "s100": ("still", "Fruit trees along the river bank in calm evening light, close, leaves and fruit reflected in the slow water.", "Slow pull back.", ["g05"], "nofig calm"),
 "s101": ("still", "The garden at evening seen from a rise, soft gold light over the trees, wide open space across the middle of the frame.", "Very slow push in.", ["g04"], "nofig"),
}


def main():
    shots = json.loads((HERE / "movement-shots.json").read_text())
    assert [s["id"] for s in shots] == sorted(S), "shot ids do not match movement-shots.json"
    banned = ["deity", "god figure", "divine being", "halo", "glowing man", "angel", "temple", "idol",
              "serpent", "cherub"]
    md = ["# The Fall: shot list (M4)\n",
          "Generated by `script/shotlist.py`. Decisions D1, D3, D4, D5 and D6 are in every prompt.\n"]
    out, counts, copied = [], {}, 0
    for i, sh in enumerate(shots, 1):
        kind, scene, motion, refs, flags = S[sh["id"]]
        counts[kind] = counts.get(kind, 0) + 1
        excl = PEOPLE if "people" in flags else NOFIG
        excl += " " + NOGOD + ("" if "snake" in flags else " " + NOSNAKE)
        if "fire" in flags:
            excl += " No winged figures, no beings, no faces in the fire, no gate, no wall, no blade held by anyone."
        if "christ" in flags:
            excl += " " + NOCHRIST
        m = motion + (CALM if "calm" in flags else "")
        prompt = f"{scene} {excl}{REFNOTE if refs else ''} {SUFFIX}" if scene else ""
        mprompt = f"{m} {MOTION}"
        if "people" not in flags and kind in ("veo", "ff"):
            mprompt += " No people, no figures appear."
        low = (prompt + mprompt).lower()
        for w in banned:
            assert w not in low, f"{sh['id']}: banned word {w}"
        assert "–" not in prompt + mprompt and "—" not in prompt + mprompt
        src = next((f[5:] for f in flags.split() if f.startswith("copy:")), None)
        if src:   # a keyframe taken from another film, free
            dest = FILM / "stills" / "movement" / f"{sh['id']}.jpg"
            if not dest.exists():
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(FILM / src, dest); copied += 1
        out.append(dict(sh, kind=kind, scene=scene, prompt=prompt, motion=mprompt, refs=[REF[r] for r in refs],
                        flags=flags))
        md.append(f"### Shot {i}: {sh['id']} {sh['chapter']} ({sh['dur']:.1f} s, {kind}{', lite' if 'lite' in flags else ''})")
        if refs:
            md.append("- Refs: " + ", ".join(REF[r] for r in refs))
        if prompt:
            md += ["- Image prompt:", f"  > {prompt}"]
        else:
            md.append(f"- Keyframe: {flags}")
        md += (["- Motion prompt:", f"  > {mprompt}"] if kind in ("veo", "ff") else [f"- Edit move: {motion}"])
        md.append("")
    (HERE / "shotlist.md").write_text("\n".join(md))
    (HERE / "shotlist.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    lite = sum(1 for s in out if "lite" in s["flags"])
    gen = [int(s["id"][1:]) for s in out if s["prompt"]]
    print(f"wrote script/shotlist.md: {len(shots)} shots {counts}; Veo {counts.get('veo', 0) + counts.get('ff', 0)} "
          f"({lite} Lite); {len(gen)} keyframes to generate; {copied} copied")


if __name__ == "__main__":
    main()
