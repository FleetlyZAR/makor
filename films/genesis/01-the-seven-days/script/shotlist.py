#!/usr/bin/env python3
"""M4 shot list for the full movement film.

Shot ids and timings come from script/movement-shots.json (written by
films/tools/animatic.py from the real voice track). This file adds, for every
shot: how it is made, what is on screen, the motion, and the reference stills.
It writes script/shotlist.md in the format films/tools/still.py and clip.py read,
and script/shotlist.json for the edit.

Kinds
  veo     keyframe, then Veo image to video
  ff      keyframe, then Veo first and last frame (last frame = next shot's keyframe)
  still   keyframe only; slow push built in the edit (free)
  reuse   no new image; reuses another shot's keyframe or clip

    python3 films/genesis/01-the-seven-days/script/shotlist.py
"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
FILM = HERE.parent

REF = {
    "bay": "stills/world/shot-01.jpg", "plants": "stills/world/shot-02.jpg", "sunrise": "stills/world/shot-03.jpg",
    "night": "stills/world/shot-04.jpg", "sea": "stills/world/shot-05.jpg", "herds": "stills/world/shot-06.jpg",
    "people": "stills/world/shot-07.jpg", "rest": "stills/world/shot-08.jpg", "egypt": "stills/world/shot-09.jpg",
    "tablet": "stills/world/shot-10.jpg", "tomb": "stills/world/shot-11.jpg", "new": "stills/world/shot-12.jpg",
    **{f"p{i}": f"stills/shot-0{i}.jpg" for i in range(1, 10)},
}

PALETTE = ("restrained palette of deep ink teal (#0E2A2E) shadows, water teal (#0F6C6C) midtones and warm muted "
           "gold (#B8862F) light, warm cream highlights, greens rendered as deep teal greens within the palette")
DARK = ("restrained palette of deep ink teal (#0E2A2E) and black with only cold, dim water teal (#0F6C6C) on the "
        "crests, no gold, no warm tones, no light source, no glow on the horizon")
SUFFIX = ("Hand painted matte painting, painterly illustration with visible brush texture and soft canvas grain, "
          "reverent, still and quiet, soft diffused light, {pal}, wide 16:9 cinematic composition with calm space in "
          "the lower third, fully painted edge to edge with no blank or flat areas, full frame with no borders or black bars, "
          "no text, no lettering, no watermark, not photoreal, not cartoon, not 3D render.")
MOTION = ("Painterly matte painting style preserved exactly, brush texture stays visible, slow and steady camera, "
          "no camera shake, no cuts, no text appears.")
CALM = " The water stays low and calm, no breaking waves, no whitecaps, no spray, no surf."

# Continuity by chapter: what does not exist yet, or must never be shown.
NOFIG = "No people, no figures, no faces, no silhouettes."
CONT = {
    "Cold open": "No sun, no moon, no stars, no land, no clouds. " + NOFIG + " No animals, no birds.",
    "A world of other stories": NOFIG + " No statues, no carved figures, no images of gods.",
    "Formless and void": "No sun, no moon, no stars. " + NOFIG + " No animals, no birds.",
    "Day One: light": "No sun, no moon, no stars, no land, no clouds. " + NOFIG + " No animals, no birds.",
    "Day Two: the sky": "No sun, no moon, no stars, no land. " + NOFIG + " No animals, no birds.",
    "Day Three: land, sea and green": "No sun disc, no moon, no stars. " + NOFIG + " No animals, no birds.",
    "Day Four: the lights": "The sun and moon are plain discs of light with no faces or symbols. " + NOFIG
                            + " No animals, no birds.",
    "Day Five: sea and sky": NOFIG + " No land animals, no monsters, no dragons.",
    "Day Six: the image of God": NOFIG,
    "Day Seven: rest": NOFIG,
    "How long were the days?": NOFIG,
    "In the beginning was the Word": NOFIG + " Never a figure meant to be Christ.",
    "The first page and the last": NOFIG,
    "Light in a dark place": "No sun, no moon, no stars, no land. " + NOFIG,
}
PEOPLE = ("The man and the woman appear only as two tiny distant shapes against the light, with no detail of "
          "clothing, body or face. No close up, no other people, no modern objects.")

# id: (kind, scene, motion, refs, flags)   flags: dark, people, calm, storm
S = {
 # Cold open
 "s001": ("veo", "Almost total darkness over a vast, still, empty ocean. The faintest heavy swells surface out of black in the lower third; above them only darkness.", "Extremely slow push in. Low swells rise and fall in place. No light appears.", ["p1"], "dark calm"),
 "s002": ("veo", "The formless, empty, dark ocean seen from just above its surface, heavy rolling swells running to a horizon lost in darkness, no shore anywhere.", "Slow forward drift low over the swells.", ["p2"], "dark calm clip:0-5.0"),
 "s003": ("veo", "Low over the dark ocean, an invisible wind passes across the surface, shown only by a long curving band of fine ripples and a thin veil of spray; the wind has no shape of its own.", "Slow lateral track following the wind across the water; the ripples travel and the water behind them calms.", ["p3"], "dark clip:0-3.0"),
 "s004": ("still", "A vast dark ocean seen from high above, endless in every direction, a single faint cold sheen across it, immense in scale.", "Slow pull back.", ["p2"], "dark"),
 "s005": ("still", "The dark deep at horizon level with a wide calm empty space across the middle of the frame, a barely visible cold line where water meets darkness.", "Very slow push in under the title.", ["p1"], "dark"),
 # A world of other stories
 "s006": ("still", "The edge of the Sinai wilderness at dawn: a wide desert plain with a great camp of tents far in the distance under a vast sky, rugged mountains beyond, thin smoke rising from cooking fires.", "Slow push toward the camp.", [], ""),
 "s007": ("still", "A dark wooden table indoors covered with clay tablets and old scrolls, lit by a small oil lamp, wedge script and painted signs on them, mysterious and old. No window, no sea.", "Slow push in.", [], ""),
 "s008": ("veo", "A dark storm sea at night under heavy churning clouds, great waves heaving and breaking, distant lightning inside the clouds, chaos and threat. No shapes or creatures in the waves or clouds.", "Storm waves heave and break, clouds churn, lightning flickers far off.", ["tablet"], "storm"),
 "s009": ("still", "A clay tablet pressed with dense wedge script resting on dark stone, lit by a single oil lamp, a storm sea beyond a stone opening.", "Slow push in on the tablet.", ["tablet"], ""),
 "s010": ("veo", "The Nile in ancient Egypt at dawn under a blazing sun, papyrus on the banks, rows of mud brick kilns smoking, stacks of drying bricks.", "Smoke drifts from the kilns, the river flows slowly, heat haze shimmers.", ["egypt"], ""),
 "s011": ("veo", "The calm dark deep at night, perfectly still water with no storm at all, a faint breath of wind across the surface.", "Very slow push in; a breath of wind ruffles the surface.", ["p2"], "dark calm"),
 "s012": ("still", "Seen from a high desert ridge, a great sun rising over a calm sea; far off lies a long straight shore backed by steep dry hills, vast and serene.", "Slow push toward the horizon.", [], ""),
 "s013": ("veo", "A calm sea under the risen sun, long gold light across the water toward a distant shore of dry, rugged hills.", "Slow pan from the sun toward the shore.", [], "calm"),
 "s014": ("still", "The hill country of Canaan seen from a desert mountain height at golden hour: terraced hills, olive groves and a wide river valley below, waiting to be entered.", "Slow push in.", [], ""),
 # Formless and void
 "s015": ("veo", "The formless dark deep, endless low heavy swells under total darkness.", "Slow push in over the swells.", ["p2"], "dark calm clip:0-4.0"),
 "s016": ("still", "The dark deep beneath a vast empty darkness above, nothing in it, a shapeless haze where water meets dark.", "Slow push in.", ["p2"], "dark"),
 "s017": ("still", "A single painting arranged as three stacked panels down the left half of the frame: at the top, light breaking over dark water; in the middle, a clear sky above the open sea; at the bottom, green land rising from the sea. The right half of the frame is plain dark ink teal canvas.", "Slow push in on the left column.", ["p5", "bay"], ""),
 "s018": ("reuse", "Reuses s017 (closer push on the three forming panels).", "Slow push in.", [], "use:s017"),
 "s019": ("still", "A single painting arranged as six panels in two columns. Left column, top to bottom: light over water, sky over sea, green land. Right column, top to bottom: the sun, moon and stars; whales and birds; herds and two tiny distant human shapes on a ridge. Each right panel sits beside the left panel it fills.", "Slow push across from left to right.", ["sunrise", "sea", "herds", "people"], "people"),
 "s020": ("still", "The same six panel painting with a seventh wider panel above both columns showing a calm bay at rest in long golden light.", "Slow tilt up to the seventh panel.", ["rest"], "people"),
 "s021": ("veo", "A soft breath of wind gently stirring the dark surface of the deep, attentive and near, fine ripples spreading outward. Only the wind's effect on the water is visible.", "The wind moves slowly across the surface, ripples spreading, calm returning behind it.", ["p3"], "dark clip:0-3.5"),
 "s022": ("still", "The calm dark sea at the moment before the first light, utterly still, a quiet expectancy.", "Very slow push in.", ["p1"], "dark calm"),
 "s023": ("still", "Calm dark water stretching to a level horizon, the surface like dark glass, waiting.", "Slow lateral drift.", ["p2"], "dark calm"),
 # Day One
 "s024": ("ff", "A vast dark ocean under total darkness seen from just above the water, a level horizon, and along its far edge the first hairline of warm gold light with no visible source.", "Darkness holds; then warm gold light rises evenly along the whole width of the horizon and spreads across the water toward the camera. No sun, no column of light, no point of light.", ["p4"], "calm dissolve:s025"),
 "s025": ("veo", "Wide view of the calm ocean flooded with warm gold light across its whole surface, the darkness drawn back into a deep teal band at the top of the frame with a soft level boundary between light and dark. No source of the light.", "Slow pull back; the boundary between light and dark settles into a steady line.", ["p5"], "calm"),
 "s026": ("veo", "One calm ocean divided side by side: the left half in warm gold daylight, the right half in deep ink teal night, a wide soft gradient of twilight in water teal blending them. Clear empty air above, no clouds. No pink, no violet, no rainbow colours.", "Slow push in toward the twilight between day and night.", ["p6"], "calm"),
 "s027": ("still", "A calm ocean glowing with soft sourceless gold light, long even swells, peaceful and good.", "Very slow push in.", ["p7"], "calm"),
 "s028": ("veo", "The calm ocean at evening, the gold light lying low along a level horizon and fading into deep ink teal dusk.", "The light fades into night, then a soft pale gold glow returns along the horizon as morning. No sun appears.", ["p8"], "calm"),
 "s029": ("still", "Soft bands of gold light lying across the calm water one behind another toward the horizon, as if spoken into place, with no source.", "Slow push toward the horizon.", ["p7"], "calm"),
 "s030": ("still", "The deep standing calm and firm under settled light, the water perfectly still like glass to the horizon.", "Very slow push in.", ["p7"], "calm"),
 # Day Two
 "s031": ("veo", "Over the open sea in soft sourceless light, a band of clear luminous air opens horizontally across the middle of the frame, separating the waters below from heavy shining mist and waters above.", "The clear band widens slowly as the waters above lift away from the sea below.", ["p9"], "calm"),
 "s032": ("veo", "A vast clear expanse stretched between the calm sea below and a high shining canopy of waters above, like beaten gold stretched thin, soft even sourceless light. No beams, no rays, no shafts of light.", "Slow rise up into the expanse.", ["p9"], "calm"),
 "s033": ("still", "The new sky over the open sea at evening, the light fading softly, the sea quiet beneath.", "Very slow push in.", ["p8"], "calm"),
 "s034": ("still", "A thin sheet of hammered gold resting on dark stone, its hammer marks rippling across it like a sky.", "Slow push across the gold.", [], ""),
 "s035": ("still", "The wide expanse of sky over the open sea seen from just above the water, immense and clear, the canopy above shimmering faintly like beaten metal.", "Slow tilt up.", ["p9"], "calm"),
 "s036": ("still", "The open sea under the new sky, grey and quiet, no land anywhere, calm and waiting.", "Slow push in.", ["p9"], "calm"),
 # Day Three
 "s037": ("ff", "Seen from high above, an open sea in soft light with the first shallows showing where land is about to rise.", "The sea draws back and dry land rises from the water: the crescent bay, the river channel, the ridge and the headland emerge, bare and wet.", ["bay"], ""),
 "s038": ("still", f"The bay newly risen from the sea, bare wet earth and rock, no plants yet, the sea calm in the bay. The same geography as the reference: a wide crescent bay, a river on the left, a ridge and rocky headland on the right.", "Slow push in.", ["bay"], "calm"),
 "s039": ("veo", "The bare new bay and the open sea beyond, small waves lapping the new shore, the river running down to the sea.", "Slow pan along the shore.", ["bay"], "calm"),
 "s040": ("ff", "The newly risen bay seen from the hills: bare brown earth and grey rock only, no grass, no green, no plants of any kind, the river and the sea calm.", "The bare hills turn green: grass spreads across the slopes and the first plants and trees rise.", ["stills/movement/s038.jpg"], "last:s045"),
 "s041": ("still", "A close view on the slope above the bay: seed bearing grasses heavy with seed heads.", "Slow push in.", ["plants"], ""),
 "s042": ("veo", "Fruit trees and seed bearing plants spreading across the green hills above the bay, the bay soft behind.", "Grasses sway gently in a breeze; slow lateral drift.", ["plants", "bay"], ""),
 "s043": ("still", "A fruit tree branch heavy with small fruit, and seed heads beside it, painted with care.", "Slow push in.", ["plants"], ""),
 "s044": ("still", "The green bay at evening, soft sourceless light fading on the hills.", "Very slow push in.", ["bay"], "calm"),
 "s045": ("still", "Wide: the green bay with its river, ridge and headland, the sky above and the open sea, a whole shaped world, every part of the land painted with grass and texture.", "Slow pull back.", ["bay"], "calm"),
 "s046": ("still", "Close in the tall grass on the empty hills above the bay, wind bending the grass, the bay far below, no creature anywhere.", "Slow push in.", ["plants", "bay"], ""),
 # Day Four
 "s047": ("veo", "The first sunrise over the bay: a great warm sun lifting clear of the sea horizon in the east, gold light across the water.", "The sun rises slowly clear of the horizon; light spreads over the bay.", ["sunrise"], "calm"),
 "s048": ("veo", "Gold morning light sweeping across the green hills of the bay as the sun climbs.", "Light moves across the hills; slow pan.", ["sunrise", "bay"], ""),
 "s049": ("veo", "The sun high over the bay, light glittering on the water.", "Light glitters and moves across the water under the high sun; slow push in.", ["sunrise"], "calm"),
 "s050": ("veo", "Dusk over the bay: the sun setting behind the ridge while a pale moon rises over the headland.", "The sun sinks, the sky darkens, the first stars appear around the moon.", ["sunrise", "night"], "calm"),
 "s051": ("still", "The bay at night under a pale full moon and a deep field of stars, silver light on the water.", "Slow tilt up to the stars.", ["night"], "calm"),
 "s052": ("still", "One continuous bay beneath a sky that is day on the left, with the sun over the sea, and night on the right, with the moon and stars over the headland.", "Slow push across.", ["sunrise", "night"], "calm"),
 "s053": ("still", "The sun as a plain disc of light low over the sea, like a lamp hanging in the sky.", "Slow push in.", ["sunrise"], "calm"),
 "s054": ("still", "The Nile in Egypt under one blazing sun, brick kilns on the bank. Only one sun in the sky, no moon, no second disc.", "Slow push toward the sun.", ["egypt"], ""),
 "s055": ("still", "A field of countless small stars over the dark ridge above the bay. No moon, no sun, no planets, no large discs of light.", "Slow drift across the stars.", ["night"], ""),
 "s056": ("still", "Inside a tent of heavy woven curtains, a seven branched golden lampstand with small oil flames burning, curtains on every side. No sky visible, no sun, no moon.", "Slow push in on the flames.", [], ""),
 "s057": ("still", "The moon's phases arcing across the night sky over the bay, from thin crescent to full, painted as one image.", "Slow pan along the arc.", ["night"], "calm"),
 # Day Five
 "s058": ("veo", "The calm bay suddenly teeming: shoals of fish flashing just under the surface, the first birds lifting from the headland.", "Shoals turn and flash under the water; birds lift into the sky.", ["sea"], "calm"),
 "s059": ("veo", "Great whales rising and breaching gently in the calm bay, spray catching gold light.", "A whale rises and rolls slowly, spray drifting.", ["sea"], ""),
 "s060": ("veo", "Seabirds wheeling off the rocky headland into the open sky.", "Birds wheel and glide; slow tilt up.", ["sea"], ""),
 "s061": ("still", "Under the surface of the bay, light streaming down through clear water, a whale and its calf gliding past turning shoals.", "Slow drift alongside.", ["sea"], ""),
 "s062": ("veo", "Great flocks over the sea and birds settling on the headland cliffs in great numbers.", "Flocks swirl and settle.", ["sea"], ""),
 "s063": ("still", "A great whale surfacing calmly beside the rocky headland, gentle and vast, simply a creature.", "Slow push in.", ["sea"], "calm"),
 "s064": ("still", "The bay at evening full of life: birds on the cliffs, whale spouts offshore.", "Slow pull back.", ["sea", "bay"], "calm"),
 "s065": ("still", "Wide: the bay teeming with life in sea and sky under warm light.", "Slow pull back.", ["sea", "bay"], "calm"),
 # Day Six
 "s066": ("veo", "The grassland above the bay comes alive: herds of oxen, deer and wild goats moving across the hills.", "Herds walk and graze; slow pan.", ["herds"], ""),
 "s067": ("still", "Small creatures in the grass in close view: a hare, beetles, a lizard on a warm stone.", "Slow push in.", [], ""),
 "s068": ("veo", "Herds grazing across the slopes with the bay below.", "Animals graze and move slowly; slow drift.", ["herds", "bay"], ""),
 "s069": ("still", "Deer, wild goats and oxen drinking at the river mouth in peace.", "Slow push in.", ["herds", "bay"], ""),
 "s070": ("still", "The whole land falls still at first light: the herds stand quiet, the grass unmoving, a hush over the bay.", "Very slow push in.", ["herds", "bay"], "calm"),
 "s071": ("veo", "The hushed land above the bay in soft first light, the long ridge ahead, empty.", "A slow push across the land toward the ridge as the wind dies away.", ["bay"], ""),
 "s072": ("still", "The long ridge above the bay against the dawn sky, empty, waiting.", "Very slow push in.", ["bay"], ""),
 "s073": ("still", "Tall grass in first light, dew on the blades, in close view.", "Slow push in.", [], ""),
 "s074": ("still", "A vast wide view of the new world at first light: the bay, the river, the herds on the near slopes, and far away on the crest of the ridge two tiny human shapes side by side against the bright dawn.", "Very slow push in.", ["people"], "people"),
 "s075": ("still", "The same two tiny human shapes on the far ridge, seen from across the bay this time, still only small dark shapes against the light, the water between.", "Slow push in.", ["people", "bay"], "people"),
 "s076": ("still", "A carver's chisel and mallet resting on an uncut block of stone in a dim workshop.", "Slow push in.", [], ""),
 "s077": ("still", "The two tiny distant human shapes on the ridge in the full light of morning, the living world spread out below them.", "Slow pull back.", ["people"], "people"),
 "s078": ("still", "The brick kilns of Egypt, rows of stacked mud bricks and a brick mould lying on the ground.", "Slow push in.", ["egypt"], ""),
 "s079": ("still", "A single mud brick marked by its mould lying alone in the dust, the kilns smoking beyond.", "Slow push in.", ["egypt"], ""),
 "s080": ("still", "The whole land and sea in morning light: herds on the hills, birds over the bay, whale spouts offshore, and the two tiny distant human shapes on the ridge.", "Slow pull back.", ["people", "sea"], "people"),
 "s081": ("veo", "Vast flocks of birds over the sea and herds across the hills, abundance everywhere, the whole frame filled with painted land, sea and sky.", "Flocks move across the sky, herds across the hills.", ["sea", "herds"], ""),
 "s082": ("still", "Fruit trees heavy with fruit and fields of seed bearing grain on the slopes above the bay.", "Slow drift across.", ["plants", "bay"], ""),
 "s083": ("still", "Ripe fruit on a branch and full heads of grain in warm light, in close view.", "Slow push in.", ["plants"], ""),
 "s084": ("veo", "Grain fields rippling in a breeze on the hills above the bay.", "The grain ripples in waves of wind.", ["plants", "bay"], ""),
 "s085": ("veo", "Deer and oxen grazing on green grass, small birds feeding among the seed heads.", "Animals graze, birds flit and feed.", ["herds"], ""),
 "s086": ("still", "A doe and her fawn grazing in green grass, peaceful.", "Slow push in.", ["herds"], ""),
 "s087": ("veo", "The whole bay in golden light: sea, sky, land and creatures, all of it full and alive.", "A slow sweeping rise above the bay.", ["rest", "bay"], "calm"),
 "s088": ("still", "Wide: the full world around the bay glowing in evening light.", "Slow pull back.", ["rest"], "calm"),
 "s089": ("still", "Evening over the full bay, the first stars beginning above the ridge.", "Very slow push in.", ["night"], "calm"),
 # Day Seven
 "s090": ("still", "The bay at rest in long golden light, the sea flat calm, nothing moving.", "Very slow push in.", ["rest"], "calm"),
 "s091": ("still", "Creatures resting in the grass above the bay, birds settled on the headland.", "Slow drift across.", ["rest"], "calm"),
 "s092": ("veo", "Golden light lying across the still bay, deep peace.", "Nothing moves but the slow drift of light and a breath of air in the grass.", ["rest"], "calm"),
 "s093": ("veo", "The flat calm sea reflecting a golden sky, perfect stillness.", "The faintest shimmer of light moves across the still water; nothing else moves.", ["rest"], "calm"),
 "s094": ("still", "A single tree on the ridge above the bay in golden light, still.", "Slow push in.", ["rest"], ""),
 "s095": ("still", "The bay at rest seen from the water's edge, golden and complete, full frame.", "Slow pull back.", ["rest"], "calm"),
 "s096": ("still", "Golden light holding over the bay as if the afternoon would never end, timeless.", "Very slow drift.", ["rest"], "calm"),
 "s097": ("still", "In a desert camp under the stars, a woven tent sanctuary with curtains of blue, purple and scarlet, a golden lampstand glowing inside its open entrance.", "Slow push in.", [], ""),
 "s098": ("still", "The tent sanctuary at the centre of a vast camp of tents in the desert at dawn, seen from far above.", "Slow pull back.", [], ""),
 # How long were the days?
 "s099": ("still", "The calm bay painted as one image across a sequence of evenings and mornings, the sky graded from night on one side to day on the other.", "Slow pan across.", ["bay", "night"], "calm"),
 "s100": ("reuse", "Reuses s019 (the six panel frame).", "Slow push in.", [], "use:s019"),
 "s101": ("still", "A quiet desert camp at rest at golden hour, tools laid down beside a tent.", "Slow push in.", [], ""),
 "s102": ("still", "The whole bay from high above in full light: sea, land and sky.", "Slow pull back.", ["bay"], "calm"),
 # In the beginning was the Word
 "s103": ("still", "Darkness with a single small point of warm light at the centre.", "Very slow push in.", [], ""),
 "s104": ("veo", "A single point of warm light in darkness over a dark sea.", "The point of light widens slowly into a dawn spreading across the dark sea.", ["p4"], "calm"),
 "s105": ("still", "Dawn light falling on an ancient hillside path above a lake in Galilee.", "Slow push along the path.", [], "calm"),
 "s106": ("still", "A single flame burning steadily in deep darkness.", "Very slow push in.", [], ""),
 "s107": ("still", "First light breaking into a dark stone room through an open window, falling across the floor.", "Slow push in.", [], ""),
 "s108": ("still", "A rock cut tomb in a garden hillside at first light, the great round stone rolled back from the dark open entrance.", "Slow push in.", ["tomb"], ""),
 "s109": ("veo", "The empty tomb at first light, folded linen cloth just visible inside the open entrance.", "Sunlight slowly reaches into the open entrance and falls across the folded linen.", ["tomb"], ""),
 "s110": ("still", "Dawn over the bay, the two tiny distant human shapes on the ridge again.", "Slow push in.", ["people"], "people"),
 "s111": ("still", "A quiet shaded resting place beside still water in green hills, morning light.", "Slow push in.", [], "calm"),
 "s112": ("still", "Still water and green grass beside a lake at dawn, peaceful.", "Very slow push in.", [], "calm"),
 # The first page and the last
 "s113": ("still", "A withered garden of dead thorn bushes under a heavy grey sky.", "Slow push in.", [], ""),
 "s114": ("still", "Cracked dry earth and a broken stone wall at grey dusk, ruin and exile.", "Slow pan.", [], ""),
 "s115": ("veo", "The waters of the deep rising over the bay and the hills, the land disappearing beneath grey heaving water under storm clouds.", "The water rises and covers the land; waves heave.", ["bay"], "storm"),
 "s116": ("still", "A long road winding through changing landscapes toward a far horizon of light.", "Slow push along the road.", [], ""),
 "s117": ("still", "The bay at rest in golden light seen from far away, distant and calling.", "Slow push in.", ["rest"], "calm"),
 "s118": ("veo", "A new heaven and a new earth: radiant green hills, a clear river shining, a great city of light glowing in the distance, the air full of light with no source.", "Light swells gently through the air; slow push toward the city.", ["new"], ""),
 "s119": ("still", "Close view at the river's edge in the new creation: clear water flowing over bright stones between green banks, lit from everywhere at once; the city is not in view.", "Slow drift along the river.", ["new"], ""),
 "s120": ("veo", "Wide: the new creation, hills, river and the city of light, radiant.", "Light swells softly through the air and the river glints; slow pull back.", ["new"], ""),
 "s121": ("still", "The city of light seen from much nearer, its glowing walls and open gates filling the middle of the frame beyond the last green hill.", "Slow push in.", ["new"], ""),
 # Light in a dark place
 "s122": ("reuse", "Reuses s024 (light breaking across the deep).", "", [], "use:s024"),
 "s123": ("reuse", "Reuses s024's first frame (the dark deep with the first thread of light).", "Very slow push in.", [], "use:s024"),
 "s124": ("reuse", "Reuses s027 (the deep glowing in calm light) under the end card.", "Very slow push in.", [], "use:s027"),
}


def main():
    shots = json.loads((HERE / "movement-shots.json").read_text())
    assert [s["id"] for s in shots] == sorted(S), "shot list ids do not match movement-shots.json"
    banned = ["deity", "god figure", "divine being", "halo", "glowing man", "angel", "temple", "idol"]
    md = ["# The Seven Days: shot list (M4)\n",
          "Generated by `script/shotlist.py` from `script/movement-shots.json`. Kinds: veo (keyframe then Veo),",
          "ff (Veo first and last frame), still (keyframe, push built in the edit), reuse (no new image).\n"]
    out, counts = [], {}
    for i, sh in enumerate(shots, 1):
        kind, scene, motion, refs, flags = S[sh["id"]]
        counts[kind] = counts.get(kind, 0) + 1
        excl = CONT[sh["chapter"]]
        if "people" in flags:
            excl = excl.replace(NOFIG, "").strip() + " " + PEOPLE
        if "storm" not in flags and "calm" in flags:
            motion += CALM
        style = SUFFIX.format(pal=DARK if "dark" in flags else PALETTE)
        refnote = (" Match the painting style, palette and, where shown, the bay geography of the reference images."
                   if refs else "")
        prompt = f"{scene} {excl}{refnote} {style}"
        mprompt = f"{motion} {MOTION}" if motion else ""
        for w in banned:
            assert w not in (prompt + mprompt).lower(), f"{sh['id']}: banned word {w}"
        assert "–" not in prompt + mprompt and "—" not in prompt + mprompt
        rec = dict(sh, kind=kind, scene=scene, prompt=prompt if kind != "reuse" else "", motion=mprompt,
                   refs=[REF.get(r, r) for r in refs], flags=flags)
        out.append(rec)
        md.append(f"### Shot {i}: {sh['id']} {sh['chapter']} ({sh['dur']:.1f} s, {kind})")
        if kind == "reuse":
            md += [f"- {scene}", ""]
            continue
        if refs:
            md.append("- Refs: " + ", ".join(REF.get(r, r) for r in refs))
        md += ["- Image prompt:", f"  > {prompt}"]
        if kind in ("veo", "ff"):
            md += ["- Motion prompt:", f"  > {mprompt}"]
        else:
            md.append(f"- Edit move: {motion}")
        md.append("")
    (HERE / "shotlist.md").write_text("\n".join(md))
    (HERE / "shotlist.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(f"wrote script/shotlist.md: {len(shots)} shots {counts}")


if __name__ == "__main__":
    main()
