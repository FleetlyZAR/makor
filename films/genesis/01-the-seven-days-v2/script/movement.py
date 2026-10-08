#!/usr/bin/env python3
"""The Seven Days v2 (Genesis 1:1 to 2:3): the photoreal, cinematic rebuild.

Structure from V2-TREATMENT.md (films/CINEMA-STANDARD.md): flash-forward open, the
brick-maker as the human strand, three set pieces, Scripture as drama with teaching in
blocks, an open loop into The Garden. Reused GUIDE lines and quotations are copied
verbatim from v1 (ids noted); lines marked "new in v2" are new. Scripture comes only
from the study JSON (checked by films/tools/movement_script.py).

    python3 films/genesis/01-the-seven-days-v2/script/movement.py
"""
import pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "films" / "tools"))
from movement_script import Film  # noqa: E402

CHAPTERS = [
    ("Cold open", [
        ("PIC", "Black. Silence. God speaks into the dark; then a single drop of water falls into still black water, and where it touches, one tiny point of light."),
        ("BEAT", 0.6, "Black. Silence."),
        ("Q", "Let there be light,", "Genesis 1:3, flash-forward", "GOD"),
        ("BEAT", 2.0, "The drop falls and touches the water."),
        ("PIC", "The point of light bursts outward and white-gold light fills the whole screen, then thins and almost fades out, opening the dark of space for what comes next."),
        ("BEAT", 3.4, "The burst: a deep boom and the score's first great swell; the light fills everything, then dims."),
        ("PIC", "Small balls of starlight fly past us as space opens, and we rush into the earth and down into the garden. Then the montage in Genesis order, about one second a shot, the score driving: the deep, the sky, land rising, forests, sea creatures, herds, the man and the woman far off in a garden, the flood, Abraham under the stars, the brick pits of Egypt, the tabernacle in the wilderness, Jerusalem at dawn, the garden tomb with its stone rolled away (no figures), the long road of the centuries, a city of today at night seen from far above."),
        ("BEAT", 12, "Through all of history to today."),
        ("PIC", "Everything rushes backward, faster and faster, and collapses into a single point of light. Silence. The point drifts and becomes a spark rising from a kiln fire in Egypt at night (match cut)."),
        ("BEAT", 4, "Rewind into a single point; silence; the spark."),
        ("PIC", "Egypt at night: brick pits by firelight, mud moulds slapped full, the brick-maker's mud-caked hands. He straightens and lifts his eyes to the sky."),
        ("BEAT", 2, "Wet clay, fire, distant work drums."),
        ("Q", "Let Us make man in Our image,", "Genesis 1:26, flash-forward", "GOD"),
        ("PIC", "Hold on the brick-maker, chest up, firelight on his face; then black."),
        ("GUIDE", "Every nation told a story of how the world began. In Babylon's, people were made to carry the labour of the gods. Then a nation of slaves heard this one.", "study.context.historical, study.hermeneutics.authorIntent"),  # new in v2
        ("CARD", "THE SEVEN DAYS / Genesis 1:1 to 2:3"),
        ("BEAT", 4, "Title over dark water. Low hit, one swell, then quiet."),
    ]),
    ("A world of other stories", [
        ("PIC", "The Nile at blazing dawn; kilns and stacked mud bricks; a clay tablet pressed with wedge script; a storm over a dark sea. Objects and landscapes only. The brick-maker once more, at work under the sun."),
        ("GUIDE", "Israel first heard these words as the opening of the Torah, given through Moses to a people who had spent generations in Egypt.", "study.context.historical"),  # v1 m005
        ("GUIDE", "In Babylon, the god Marduk defeats the sea goddess Tiamat and splits her body to form sky and earth. Human beings are made to carry the labour of the gods, so that the gods may rest.", "study.context.historical"),  # v1 m007
        ("GUIDE", "In Egypt, the sun was worshipped as a god, and Pharaoh was presented as a son of the sun.", "study.context.historical"),  # v1 m008
        ("GUIDE", "Moses wanted Israel to know who their God was before they learned anything else about Him. Not one god among many, but the Maker of the sun that Egypt worshipped, the sea that the nations feared, and the land they were about to enter.", "study.hermeneutics.authorIntent"),  # v1 m010
        ("BEAT", 1, "Hard cut to black and silence."),
    ]),
    ("In the beginning", [
        ("PIC", "Black water under no light; a slow push across the surface of the deep."),
        ("V", "1:1", "1:2"),
        ("PIC", "Wind moving across the water, spray lifting: the Spirit by effect only, never a figure or a bird."),
        ("BEAT", 4, "Wind passes across the water. Hold."),
        ("PIC", "Stillness; a single drop falls into the black water (the sound of the opening); then the horizon ignites and light floods across the water, black turning to gold; two and three second cuts, then one long wide. Day beside night; evening, then morning."),
        ("V", "1:3", "1:3"),
        ("BEAT", 8, "Set piece: the light breaks. The score crests above where the voice sat."),
        ("V", "1:4", "1:5"),
    ]),
    ("Formless and void", [
        ("PIC", "The frame builds from the film's own shots: three realms on the left, their three fillings on the right, the seventh day above. Cards slide in with soft hits."),
        ("GUIDE", "Verse two names the problem. The earth was formless and void. In Hebrew, tohu wabohu.", "study.originalLanguages"),  # v1 m011
        ("GUIDE", "Days one to three give shape to the formless: light from darkness, the waters above from the waters below, the sea from the dry land.", "study.context.literary"),  # v1 m013
        ("GUIDE", "Days four to six fill the void: lights for the light, birds and fish for the sky and sea, animals and people for the land.", "study.context.literary"),  # v1 m014
        ("GUIDE", "And the seventh day stands apart, as the goal.", "section.frameNote"),  # v1 m015
        ("GUIDE", "Over the deep, the Spirit of God is hovering, the same word used of an eagle over its young. Attentively near, poised to bring life.", "lexicon.hover"),  # v1 m016
        ("GUIDE", "Light on the first day, before the sun on the fourth. The point is theological before it is astronomical: light comes from God.", "lexicon.light"),  # v1 m023
        ("GUIDE", "So first, God gives the world its shape.", "study.context.literary"),  # new in v2
    ]),
    ("The world takes shape", [
        ("PIC", "Waters rise and part; an expanse opens between the waters above and below, light like beaten gold. No sun, moon or stars."),
        ("V", "1:6", "1:8"),
        ("PIC", "Seas draw back and dry land rises streaming; grass, seed plants and fruit trees race across the hills in two second time-lapse cuts with whooshes."),
        ("V", "1:9", "1:13"),
        ("BEAT", 3, "Montage at full drive, then the music stops on a wide, green, empty world."),
        ("GUIDE", "Now the three realms stand ready: the light, the sky and the sea, and the dry land. The formless has been given shape.", "study.context.literary"),  # v1 m041
        ("GUIDE", "But it is still empty.", "study.context.literary"),  # v1 m042
        ("BEAT", 2, "Silence."),
    ]),
    ("The first sunrise", [
        ("PIC", "Black sky over the new land; the first sunrise lifts over the sea in one long take."),
        ("BEAT", 5, "The score rises with the light."),
        ("V", "1:14", "1:16"),
        ("PIC", "Moon and stars over the land at night."),
        ("V", "1:17", "1:19"),
        ("PIC", "Cut to Egypt's sun blazing over the brick pits; the brick-maker shades his eyes."),
        ("GUIDE", "Notice what is not said. The sun and moon are not even named. To Egypt the sun was a god. Here they are the greater light and the lesser light, lamps hung in the sky with a job to do, and the stars are mentioned almost in passing.", "study.context.historical"),  # v1 m051
        ("PIC", "A lamp's flame in darkness, then the sun again."),
    ]),
    ("The sea teems", [
        ("PIC", "Shoals turning in the light; a whale rising from the deep and breaching in slow motion; flocks lifting off the water into the sky. Two to four second cuts."),
        ("V", "1:20", "1:23"),
        ("BEAT", 4, "The breach: impact, spray, wingbeats."),
        ("GUIDE", "The great sea creatures, a word that elsewhere names the monsters of the sea, are simply creatures God made and blessed.", "study.context.historical"),  # v1 m059
        ("GUIDE", "And for the first time, God blesses. The whole account moves from emptiness to fullness, because God gives.", "study.god"),  # v1 m060
    ]),
    ("The image of God", [
        ("PIC", "Herds across the plains: aurochs, gazelle, ibex, dust and running. The most driving pulse in the film."),
        ("V", "1:24", "1:25"),
        ("PIC", "The herds slow; the plain empties to first light. The music cuts to nothing."),
        ("GUIDE", "Then the pattern breaks. God does not simply say, let there be. He deliberates.", "study.context.literary"),  # v1 m065
        ("PIC", "Black, then dawn coming up very slowly."),
        ("V", "1:26", "1:26"),
        ("PIC", "The man and the woman in the new world at first light (The Garden's cast, photoreal rules)."),
        ("V", "1:27", "1:27"),
        ("BEAT", 12, "Set piece: the image of God. The second peak, warm and immense, no narration."),
        ("GUIDE", "Three lines of poetry, and the word created sounds three times.", "study.context.literary"),  # v1 m069
        ("GUIDE", "Image, tselem, is the word used for a carved image, the kind Israel was told to destroy in Canaan. In a world full of idols, God places His own living image on the earth.", "study.originalLanguages"),  # v1 m070
        ("PIC", "The brick-maker's face, chest up, in firelight."),
        ("GUIDE", "Remember who first heard this. Slaves who had been treated as tools in Pharaoh's building projects are told that every human being, male and female, is made in the image of God and blessed with a royal calling.", "study.hermeneutics.authorIntent"),  # v1 m071
        ("PIC", "Fields of grain and fruit trees, the man and the woman far off among them."),
        ("V", "1:28", "1:28"),
        ("GUIDE", "Humanity is not made to feed the gods. God feeds humanity.", "study.context.historical"),  # v1 m074
        ("V", "1:29", "1:31"),
        ("PIC", "The whole world in golden light, wide."),
        ("GUIDE", "Seven times God looks and calls it good. The last time, very good. The goodness of the world is not a human judgment, but His.", "study.god"),  # v1 m080
    ]),
    ("Rest", [
        ("PIC", "The finished world in long golden light; nothing moves but light and breath."),
        ("GUIDE", "Then the pattern breaks altogether.", "study.context.literary"),  # v1 m081
        ("V", "2:1", "2:3"),
        ("BEAT", 3, "Silence but for the room tone of a finished world."),
        ("GUIDE", "There is no speech. No it was good. No evening and morning. And the Hebrew names the seventh day three times in two verses.", "study.context.literary"),  # v1 m085
        ("GUIDE", "God does not rest because He is tired. He rests because the work is finished, and good.", "study.god"),  # v1 m086
        ("GUIDE", "Then He blesses a day and sanctifies it, the first thing in the Bible to be made holy. Time itself belongs to Him.", "study.god"),  # v1 m087
        ("PIC", "Evening in the wilderness: the brick-maker's family resting together."),
        ("GUIDE", "Israel's own week was patterned on this one.", "study.crossReferences (Exodus 20:8-11)"),  # v1 m090
        ("Q", "For in six days the LORD made the heavens and the earth.", "Exodus 20:11", "READER"),  # v1 m091
        ("GUIDE", "But the passage itself presses a different question. Not how long God took, but who He is, and whose the world is.", "study.hermeneutics.debates[0].bearing"),  # v1 m092
    ]),
    ("In the beginning was the Word", [
        ("PIC", "A single point of light in total darkness."),
        ("GUIDE", "The New Testament does not treat Christ as a latecomer to this story. It places Him at its beginning.", "study.christ"),  # v1 m093
        ("Q", "In the beginning was the Word,", "John 1:1", "READER"),  # v1 m094
        ("Q", "Through Him all things were made, and without Him nothing was made that has been made,", "John 1:3", "READER"),  # v1 m095
        ("PIC", "The point widens into dawn."),
        ("GUIDE", "Genesis shows God creating by speaking. John tells us that the Speech itself is a person, and that He became flesh.", "study.christ"),  # v1 m096
        ("Q", "The Light shines in the darkness, and the darkness has not overcome it.", "John 1:5", "READER"),  # v1 m097
        ("PIC", "A garden at first light; the stone rolled back from an empty tomb, no figures."),
        ("GUIDE", "The first creation climbed toward a seventh day. Jesus lies in the tomb through the Sabbath, and rises on the first day of the week. The new creation begins on the first day of a new week.", "study.christ"),  # v1 m100
        ("BEAT", 8, "Set piece: the empty tomb at dawn. The third peak, no narration."),
        ("PIC", "Light on the path out of the tomb."),
        ("GUIDE", "Humanity was made to be God's image. Christ is the image of the invisible God, the true Man in whom the human calling is finally carried out.", "study.typology[1]"),  # v1 m101
        ("GUIDE", "And the rest of the seventh day, He offers in person.", "study.typology[0]"),  # v1 m102
        ("Q", "Come to Me, all you who are weary and burdened, and I will give you rest,", "Matthew 11:28", "READER"),  # v1 m103
    ]),
    ("All things new", [
        ("PIC", "The deep returning over the land, creation undone; then a radiant new world with no sun in the sky and no sea."),
        ("GUIDE", "This page sets the standard for everything after it. Chapter three is a tragedy because chapter one was very good. Death, violence and exile are wrong because they were not part of the world God made.", "study.oneStory"),  # v1 m104
        ("GUIDE", "And the last pages of the Bible deliberately echo the first. A new heaven and a new earth. A city that has no need of sun or moon, for the glory of God is its light. The sea is no more.", "study.oneStory"),  # v1 m108
        ("Q", "Behold, I make all things new.", "Revelation 21:5", "GOD"),  # v1 m109
        ("GUIDE", "The story that began with, In the beginning God, ends with God dwelling among His people in a world made new.", "study.oneStory"),  # v1 m110
        ("BEAT", 5, "The new creation: radiant swell."),
    ]),
    ("Light in a dark place", [
        ("PIC", "The dark deep with light breaking across it, as at the start."),
        ("GUIDE", "On the first day God said, let there be light, before the sun existed, because light comes from Him.", "questions[4]"),  # v1 m111
        ("GUIDE", "Where do you need to ask God to speak light into a dark place?", "questions[4]"),  # v1 m112
        ("BEAT", 3, "Hold on the light."),
        ("GUIDE", "Genesis one is the wide shot. In chapter two, the camera comes down to the ground, to the dust, and to a garden.", "series link to The Garden (not from the study)"),  # new in v2
        ("PIC", "A frame of The Garden; then the end card with the study link and a WATCH NEXT space."),
        ("CARD", "Study The Seven Days / makor.co.za/genesis/the-seven-days"),
        ("BEAT", 6, "End card."),
    ]),
]

HEADER = """# The Seven Days v2: full movement film script (DRAFT)

Genesis 1:1 to 2:3, rebuilt photoreal and to films/CINEMA-STANDARD.md. Generated by
`script/movement.py`; edit that file, not this one. Treatment: `../01-the-seven-days/V2-TREATMENT.md`.

Runtime: **{total}** ({basis}). All {n} verses appear once, in order, verbatim BSB from the
study JSON (checked by the generator). Words: {words}.

## Chapters

```
{chapters}
```
"""

if __name__ == "__main__":
    Film(HERE, REPO / "src/content/studies/genesis/01-the-seven-days.json").build(CHAPTERS, HEADER)
