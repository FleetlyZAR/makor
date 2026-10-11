#!/usr/bin/env python3
"""The Garden v2 (Genesis 2:4 to 25): the cinematic rebuild, to films/CINEMA-STANDARD.md.

Structure from ../TREATMENT.md: a flash-forward open (the breath), the brick-maker from
The Seven Days v2 as the human strand (now free, in the wilderness camp around the
tabernacle), four set pieces with no narration where the score leads (the breath, the
river, the woman brought to the man, Eden restored), Scripture played as drama with
teaching in blocks between, an open loop into The Fall. Reused GUIDE lines are copied
from v1 (ids noted); lines marked "new in v2" are new and carry their study field.
Scripture comes only from the study JSON (checked by films/tools/movement_script.py).

    python3 films/genesis/02-the-garden-v2/script/movement.py
"""
import pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "films" / "tools"))
import movement_script  # noqa: E402
from movement_script import Film  # noqa: E402

# Until the voices are rendered, estimate at the v2 pace measured on The Seven Days v2
# (READER 0.8 = 145 wpm, GOD 0.85, GUIDE 0.85 = about 140 wpm).
movement_script.WPM.update({"READER": 145, "GOD": 135, "GUIDE": 140})

# The man's words in 2:23 are read by the READER (Makor rule, as v1).
VOICE_MAP = {"MAN": "READER"}

CHAPTERS = [
    ("Cold open", [
        ("PIC", "Picking up where The Seven Days ended: high above the finished world in golden light, the camera falls. Through cloud, over the river lands, down and down to bare dry ground, and on into a single grain of dust in extreme macro."),
        ("BEAT", 6, "The fall from sky to ground: wind rush, a whoosh, then sudden silence on the grain of dust."),
        ("PIC", "Silence. Dark damp dust in macro. A wind moves across it and the dust lifts. Hard cut: a man's eye opening, very close, first light in it (Adam, cast portrait). A first breath, loud in the silence."),
        ("BEAT", 4, "The breath: a deep in-breath, the score's first swell under it, then cut to black."),
        ("PIC", "Flash-forward montage, about one second a shot, the score driving: a river splitting into four from far above; gold glinting in a riverbed; two trees standing apart in soft light; a lion, an ibex, an eagle passing before the man; the man asleep under a tree at night; a woman's face in morning light (Eve, cast portrait); two hands meeting. Then black."),
        ("BEAT", 7, "Montage at full drive, then the music cuts to nothing."),
        ("Q", "It is not good for the man to be alone.", "Genesis 2:18, flash-forward", "GOD"),
        ("BEAT", 1.5, "Silence on black."),
        ("PIC", "Night in the wilderness camp. Tents in rows under the stars, and at the centre of the camp a great tent sanctuary, its curtained gate facing east, fire and smoke rising before it. The brick-maker from The Seven Days, free now, sits at the door of his tent and watches it."),
        ("GUIDE", "Seven times in chapter one, God looked at His world and called it good. In chapter two, for the first time, something is not good. And the people who first heard this lived in tents around a sanctuary. They would have noticed something about this garden. It looks like one.", "study.context.literary, study.context.historical"),  # new in v2
        ("CARD", "THE GARDEN / Genesis 2:4 to 25"),
        ("BEAT", 4, "Title over dry ground at first light. Low hit, one swell, then quiet."),
    ]),
    ("Down to the ground", [
        ("PIC", "The wide world of The Seven Days from high above; then a slow descent to the ground, the camera coming to rest at the height of a man's eye on bare earth."),
        ("V", "2:4", "2:4"),
        ("GUIDE", "Listen to the turn inside the verse. The heavens and the earth become the earth and the heavens, and the camera comes down from the sky to the ground.", "study.context.literary"),  # v1 m004
        ("PIC", "On screen, one word at a time over the film's own shots, each with a soft hit: forms, breathes, plants, takes, places, commands, brings, closes, builds."),
        ("GUIDE", "And God now has a name. The LORD, in small capitals, stands for His covenant name. In chapter one He speaks and worlds appear. Here He stoops and works with His hands. He forms, breathes, plants, takes, places, commands, brings, closes and builds.", "lexicon.yhwh, study.god"),  # v1 m005, extended in v2
        ("GUIDE", "This is not a second, competing creation story. It is a close up of the sixth day, and Jesus quotes both chapters together as one word from the Creator.", "study.hermeneutics.debates[0]"),  # v1 m006, trimmed
    ]),
    ("Dust and breath", [
        ("PIC", "Bare dry ground at first light. No shrub, no plant, no cloud. Then springs well up from below and the water spreads, darkening the dust in long slow ribbons."),
        ("V", "2:5", "2:6"),
        ("GUIDE", "The scene opens with what is missing. No shrub, no plant, no rain, and no man to cultivate the ground. Every lack is about to be met.", "study.context.literary"),  # v1 m009
        ("BEAT", 2, "Silence. Water ticking into the dust."),
        ("PIC", "Set piece: the forming. The damp dust stirs and gathers, drawn together by wind and light into the shape of a man lying on the ground, seen from far off; nothing else moves. No hands, no figure: only the effect. Then a wind passes over him, low and close, the grass bending. His chest rises. His eyes open."),
        ("V", "2:7", "2:7"),
        ("BEAT", 14, "Set piece: the breath. The film's first peak, warm and immense, no narration: the man's first breaths, his hand closing on the earth, first light across his face."),
        ("PIC", "The wilderness camp by day: the brick-maker kneels and lets dry dust run through fingers that once shaped bricks in Egypt."),
        ("GUIDE", "Formed is the potter's verb, the word for hands shaping clay. Isaiah says it plainly:", "study.originalLanguages"),  # v1 m011
        ("Q", "we are the clay, and You are the potter,", "Isaiah 64:8", "READER"),  # v1 m012
        ("GUIDE", "The nations also told of humans made from clay, as servants to spare the gods their labour. Genesis is different. This man is given a garden, good food and meaningful work, and God's own breath.", "study.context.historical"),  # new in v2
        ("GUIDE", "Man, adam, is taken from the ground, adamah. We are earthy creatures, given dignity only by the breath of God.", "lexicon.adamah"),  # v1 m014
        ("Q", "the breath of the Almighty gives me life,", "Job 33:4", "READER"),  # v1 m015
    ]),
    ("A garden in the east", [
        ("PIC", "Two to three second cuts, the score rising: shoots breaking the ground, trees climbing toward the light, fruit swelling on the branch: figs, pomegranates, dates, grapes, olives. Then wide: a garden planted in the east, and at its centre two trees standing apart in soft light."),
        ("V", "2:8", "2:9"),
        ("GUIDE", "Eden means delight. It is a garden of God's own planting, the first place where God dwells with man.", "lexicon.eden"),  # v1 m018
        ("GUIDE", "Notice the two trees in the middle. They are placed carefully, with the man, the woman and the command, so that the next chapter can test each one.", "study.context.literary"),  # v1 m019
    ]),
    ("Four rivers", [
        ("PIC", "Set piece: the river. Following one river out of the garden from just above the water, faster and faster, until it breaks into four great headwaters and the camera climbs to see all four running out across the land."),
        ("V", "2:10", "2:10"),
        ("PIC", "Each river in turn from the air, its name on screen: the Pishon winding through a land of gold, gold glinting in the riverbed, pale resin and dark banded stone in the shallows; the Gihon through the far south; the Tigris; the Euphrates."),
        ("V", "2:11", "2:14"),
        ("BEAT", 12, "Set piece: the four rivers, from far above. The second peak, no narration; the score above where the voice sat."),
        ("GUIDE", "The geography is deliberately real and deliberately beyond reach. Every Israelite knew the Tigris and the Euphrates. The Pishon and the Gihon cannot be identified with certainty.", "study.context.historical"),  # v1 m025
        ("GUIDE", "And in the ancient world, the dwelling of a god was a place of abundant water. Here a river flows out from the place where God dwells, to water the whole world.", "study.context.historical"),  # new in v2
        ("BEAT", 1, "Hard cut to the wilderness camp."),
    ]),
    ("A garden like a sanctuary", [
        ("PIC", "The wilderness camp at sunrise. The brick-maker walks toward the great tent at its centre. Its gate faces east into the rising sun. Inside the court, gold catches the light. A priest stands at the gate, two dark onyx stones set on his shoulders, engraved with names. Woven into the inner curtains, cherubim among palms and open flowers."),
        ("GUIDE", "Now look at the camp the first hearers lived in.", "study.context.historical"),  # new in v2
        ("GUIDE", "For Israel, the garden looked like a sanctuary. Its entrance faces east, as the tabernacle's did. Gold and onyx were the materials of the priestly garments, and two onyx stones, engraved with the tribes' names, sat on the high priest's shoulders.", "study.context.historical"),  # v1 m026, extended in v2
        ("GUIDE", "In the next chapter God walks in the garden, the same form of the verb He uses when He promises Israel:", "study.context.historical"),  # new in v2
        ("Q", "I will walk among you and be your God,", "Leviticus 26:12", "READER"),
        ("GUIDE", "Israel's worship was, in part, a memory of Eden.", "study.context.historical"),  # new in v2
    ]),
    ("To cultivate and keep", [
        ("PIC", "The man at work among the trees of the garden at first light, turning the soil, tending a vine. Match cut: a Levite at the sanctuary, tending the court in the same light; then standing guard at its gate."),
        ("V", "2:15", "2:15"),
        ("GUIDE", "Cultivate and keep. The first verb means to work or serve, and is the ordinary word for serving God in worship. The second means to guard and keep, the word for keeping God's commands.", "study.originalLanguages"),  # v1 m028
        ("GUIDE", "Together they describe the Levites in the tabernacle. Adam's work is farming, but it is also priestly service in the place where God dwells.", "study.originalLanguages"),  # v1 m029
        ("GUIDE", "A keeper of a sanctuary needs one more thing. A word from the One who lives there.", "study.hermeneutics.authorIntent"),  # new in v2
    ]),
    ("One word", [
        ("PIC", "Stillness in the middle of the garden. The tree of the knowledge of good and evil, heavy with fruit. No figure: only a wind that moves softly through every leaf at once. The man stands before it, small."),
        ("BEAT", 2, "The wind through the leaves; everything else falls silent."),
        ("V", "2:16", "2:17"),
        ("BEAT", 2, "Hold on the tree after the warning. Silence."),
        ("GUIDE", "Listen to the order. The command opens with permission, every tree of the garden, and only then sets one limit. God's commands are not the grudging rules of a jealous master, but the boundaries of a good home.", "study.god"),  # v1 m033
        ("GUIDE", "And the warning is plain. God does not hide the consequences of disobedience. His word defines what is good and what is evil, and life depends on trusting it.", "study.god"),  # v1 m034
        ("BEAT", 2, "Pause on the tree, heavy with fruit, the wind in its leaves."),  # Luyanda, 11 October: break the longest teaching run
        ("GUIDE", "Whatever the knowledge of good and evil means exactly, the heart of the matter is trust: whether the man will receive it from God's word, or seize it on his own terms.", "study.hermeneutics.debates[1].bearing"),  # v1 m035
        ("GUIDE", "So the garden has everything. Food, beauty, work, and a word to live by. And then God Himself says that something is missing.", "study.context.literary"),  # new in v2
    ]),
    ("Not good", [
        ("PIC", "Evening. The man alone in the wide garden, very small among the trees, the light going."),
        ("BEAT", 2, "Wind; a single bird far off; the music gone."),
        ("V", "2:18", "2:18"),
        ("GUIDE", "The first thing in the Bible called not good. And it is God Himself who names the lack, before the man does.", "study.context.literary"),  # v1 m038
        ("GUIDE", "Helper is ezer, and Scripture uses that word most often of God Himself.", "study.crossReferences (Psalm 121)"),  # v1 m039
        ("Q", "My help comes from the LORD, the Maker of heaven and earth.", "Psalm 121:2", "READER"),  # v1 m040
        ("GUIDE", "It speaks of strength brought alongside, never of someone lesser. Suitable means one who stands face to face with him, his match.", "lexicon.ezer"),  # v1 m041
        ("PIC", "Montage, two to three second cuts, the score driving: the beasts of the field and the birds of the air coming before the man one by one: a lion, a herd of gazelle, an ibex on the rocks, a bear, an eagle settling on a branch, a pair of doves. He looks at each and speaks. Then they pass, and he is alone again."),
        ("V", "2:19", "2:20"),
        ("BEAT", 3, "The last animal turns away. The music stops on the man alone."),
        ("GUIDE", "God brings the animals to the man to see what he would name each one, and honours his choices. But none of them stands face to face with him.", "study.god"),  # v1 m044
    ]),
    ("Bone of my bones", [
        ("PIC", "Dusk deepening into night over the garden; the man asleep beneath a tree, seen from far away; stars; soft light gathering near him. No figure."),
        ("V", "2:21", "2:22"),
        ("GUIDE", "The deep sleep is the same sleep that falls on Abram before God makes covenant with him. God works while the man is passive.", "study.originalLanguages"),  # v1 m047
        ("GUIDE", "Rib can mean side, a builder's word used of the tabernacle's sides. And made is literally built. God builds the woman as a builder raises a house, and then He Himself brings her to the man.", "study.originalLanguages"),  # v1 m048, extended in v2
        ("PIC", "Set piece: the woman brought to the man. Morning light through the garden. She walks toward him through the trees (Eve, cast portrait, framed head and shoulders, long hair). He wakes, rises and turns. His face as he sees her. Face to face."),
        ("BEAT", 14, "Set piece: the third peak, the warmest in the film, no narration; then the music falls away for his words."),
        ("V", "2:23", "2:23"),
        ("BEAT", 2, "Hold on the two faces. Silence."),
        ("GUIDE", "These are the first recorded human words in the Bible, and they are poetry. Man and woman, ish and ishshah, sound alike. Bone of my bones is the language of family.", "study.originalLanguages"),  # v1 m050
    ]),
    ("One flesh", [
        ("PIC", "The wilderness camp at evening: the brick-maker and his wife at the door of their tent, their children asleep inside, the sanctuary's fire beyond."),
        ("V", "2:24", "2:24"),
        ("GUIDE", "The narrator steps out of the story to apply it to every marriage after it. To be united is to cling or hold fast, the word Ruth uses of Naomi, and the word Moses uses of Israel and God:", "study.originalLanguages"),  # v1 m052, extended in v2
        ("Q", "Hold fast to Him,", "Deuteronomy 10:20", "READER"),
        ("GUIDE", "Marriage is a loyalty chosen and kept, not only a feeling. This chapter was written to shape Israel's homes.", "study.originalLanguages, study.hermeneutics.authorIntent"),  # v1 m052 and new in v2
        ("PIC", "The garden in full light, the two far off together among the trees; peace, no fear."),
        ("V", "2:25", "2:25"),
        ("BEAT", 3, "Hold. Then the wind stirs the grass at the foot of the tree in the middle of the garden. The music turns."),
        ("GUIDE", "Naked, and not ashamed. The line closes the scene and sets up the next one. Every gift in this chapter is about to be tested.", "study.context.literary"),  # v1 m054
    ]),
    ("The last Adam", [
        ("PIC", "Light falling into a garden at dawn: an olive grove at night with torches moving through it; then a rock cut tomb in a garden, its stone rolled back, no figures."),
        ("GUIDE", "Paul quotes this chapter and names Jesus as the last Adam.", "study.christ"),  # v1 m055
        ("Q", "The first man Adam became a living being; the last Adam a life-giving spirit,", "1 Corinthians 15:45", "READER"),  # v1 m056
        ("GUIDE", "Adam was placed in a garden to serve and guard it, and given one word to keep. He failed at every point. Christ comes as the obedient Man who serves His Father perfectly.", "study.christ"),  # v1 m057
        ("GUIDE", "John frames the passion with gardens. Jesus is arrested in a garden, buried in a garden, and on Easter morning Mary thinks He is the gardener. In a sense she is right.", "study.christ"),  # v1 m058
        ("BEAT", 8, "Set piece: the empty tomb in the garden at sunrise, light on the path. The same wind that passed over the dust in Eden moves through the garden. No narration."),
        ("GUIDE", "That evening He breathes on His disciples, as God breathed into the first man, and says:", "study.crossReferences (John 20:22)"),  # v1 m059
        ("Q", "Receive the Holy Spirit,", "John 20:22", "READER"),  # v1 m060
        ("GUIDE", "And Paul says the one flesh union was always pointing beyond itself.", "study.christ"),  # v1 m063, trimmed
        ("Q", "This mystery is profound, but I am speaking about Christ and the church,", "Ephesians 5:32", "READER"),  # v1 m064
    ]),
    ("Eden restored", [
        ("PIC", "Flash-forward, dark and fast: thorns breaking the soil; a man's hands bleeding on hard ground; a flaming sword turning before the way to the tree. Then the wilderness camp: the brick-maker looking out over desert."),
        ("GUIDE", "When chapter three comes, each gift in this garden is damaged. The ground is cursed, work becomes toil, the marriage is strained, shame replaces nakedness without shame, and the way to the tree of life is barred.", "study.oneStory"),  # v1 m065
        ("GUIDE", "But the prophets kept the garden alive. They promised a people in the desert that God", "study.context.canonical"),  # new in v2
        ("Q", "will make her wilderness like Eden and her desert like the garden of the LORD,", "Isaiah 51:3", "READER"),
        ("PIC", "Set piece: Eden restored. A radiant city with a river of clear water running through its centre, and the tree of life on both banks, fruit hanging in the light."),
        ("GUIDE", "And the Bible ends with Eden restored and surpassed. The river of the water of life flows from the throne of God and of the Lamb, and the tree of life stands on either side of it.", "study.oneStory"),  # v1 m066
        ("Q", "eat from the tree of life in the Paradise of God,", "Revelation 2:7", "READER"),  # v1 m067
        ("BEAT", 10, "Set piece: Eden restored. The fourth peak, radiant, no narration."),
        ("GUIDE", "The garden has become a city, but it is still a home where God and His people live together.", "study.oneStory"),  # v1 m068
    ]),
    ("Dust that breathes", [
        ("PIC", "Back to the first image: dust on the ground, a breath of wind, first light."),
        ("GUIDE", "We are dust that breathes because He breathed. Every good gift, food, work, beauty, marriage and friendship, comes from His hand, and even His limits are a form of His care.", "study.god"),  # v1 m069
        ("GUIDE", "You were formed from dust and given life by God's breath. How does remembering that change how you see your worth today?", "questions[0]"),  # v1 m070
        ("BEAT", 3, "Hold on the light."),
        ("PIC", "The tree in the middle of the garden at dusk. Something moves in the grass at its foot, unseen. Cut to black."),
        ("GUIDE", "One tree, one word, and a man and a woman who trust it. In the next chapter, another voice speaks in the garden, and the first question it asks is about what God said.", "series link to The Fall (not from the study)"),  # new in v2
        ("CARD", "Study The Garden / makor.co.za/genesis/the-garden"),
        ("BEAT", 6, "End card with a WATCH NEXT space for The Fall."),
    ]),
]

HEADER = """# The Garden v2: full movement film script (DRAFT)

Genesis 2:4 to 25, rebuilt to films/CINEMA-STANDARD.md like The Seven Days v2. Generated by
`script/movement.py`; edit that file, not this one. Treatment: `../TREATMENT.md`.

Runtime: **{total}** ({basis}). All {n} verses appear once, in order, verbatim BSB from the
study JSON (checked by the generator). Words: {words}.

## Chapters

```
{chapters}
```
"""

if __name__ == "__main__":
    Film(HERE, REPO / "src/content/studies/genesis/02-the-garden.json", voice_map=VOICE_MAP).build(CHAPTERS, HEADER)
