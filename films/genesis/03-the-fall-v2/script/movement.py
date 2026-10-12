#!/usr/bin/env python3
"""The Fall v2 (Genesis 3:1 to 24): the cinematic rebuild, to films/CINEMA-STANDARD.md.

Structure from ../TREATMENT.md: a flash-forward open (the voice in the garden, "Where are you?",
the sword of flame), the brick-maker from The Seven Days v2 and The Garden v2 as the human strand
(a freed slave of Egypt in the wilderness camp, who knows the serpent on Pharaoh's crown and
watches the priests clothed and the veil with its cherubim), five set pieces with no narration
where the score leads (the eating, the voice in the garden, dust to dust, east of Eden, the
veil to the empty tomb), a fast montage of the long war, Scripture played as drama with teaching
in blocks between, and an open loop into Cain and Abel.

GUIDE lines reused from v1 are marked "v1" (trimmed where noted); lines marked "new in v2" are
new and carry their study field. Scripture comes only from the study JSON (checked by
films/tools/movement_script.py).

    python3 films/genesis/03-the-fall-v2/script/movement.py
"""
import pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "films" / "tools"))
import movement_script  # noqa: E402
from movement_script import Film  # noqa: E402

# Until the voices are rendered, estimate at the v2 pace (as The Garden v2).
movement_script.WPM.update({"READER": 145, "GOD": 135, "GUIDE": 140})

# v1 decision D2 holds: every speaker other than God is read by the READER.
VOICE_MAP = {"MAN": "READER", "WOMAN": "READER", "SERPENT": "READER"}

# The same hand splits as v1 (Genesis 3 tags God's speech in ways the detector cannot read).
SPEAKERS = {
    "3:9": [("READER", "But the LORD God called out to the man,"), ("GOD", "“Where are you?”")],
    "3:11": [("GOD", "“Who told you that you were naked?”"), ("READER", "asked the LORD God."),
             ("GOD", "“Have you eaten from the tree of which I commanded you not to eat?”")],
    "3:13": [("READER", "Then the LORD God said to the woman,"), ("GOD", "“What is this you have done?”"),
             ("READER", "“The serpent deceived me,” she replied, “and I ate.”")],
    "3:14": [("READER", "So the LORD God said to the serpent:"),
             ("GOD", "“Because you have done this, cursed are you above all livestock and every beast of the field! On your belly will you go, and dust you will eat, all the days of your life.")],
    "3:15": [("GOD", "And I will put enmity between you and the woman, and between your seed and her seed. He will crush your head, and you will strike his heel.”")],
    "3:16": [("READER", "To the woman He said:"),
             ("GOD", "“I will sharply increase your pain in childbirth; in pain you will bring forth children. Your desire will be for your husband, and he will rule over you.”")],
    "3:17": [("READER", "And to Adam He said:"),
             ("GOD", "“Because you have listened to the voice of your wife and have eaten from the tree of which I commanded you not to eat, cursed is the ground because of you; through toil you will eat of it all the days of your life.")],
    "3:18": [("GOD", "Both thorns and thistles it will yield for you, and you will eat the plants of the field.")],
    "3:19": [("GOD", "By the sweat of your brow you will eat your bread, until you return to the ground, because out of it were you taken. For dust you are, and to dust you shall return.”")],
    "3:22": [("READER", "Then the LORD God said,"),
             ("GOD", "“Behold, the man has become like one of Us, knowing good and evil. And now, lest he reach out his hand and take also from the tree of life, and eat, and live forever...”")],
}

CHAPTERS = [
    ("Cold open", [
        ("PIC", "Black. Then the garden at evening, very close among the leaves. A wind is coming through the trees from far off, bending them one after another in a long wave, like footsteps. Leaves shiver. Between dark leaves, a man's eye, wide and afraid (Adam, cast portrait): the same eye that opened on the first breath in The Garden."),
        ("BEAT", 6, "The wind comes nearer, tree by tree, each wave louder, then stops. Total silence."),
        ("Q", "Where are you?", "Genesis 3:9, flash-forward", "GOD"),
        ("BEAT", 1.5, "Silence on black."),
        ("PIC", "Flash-forward montage, about one second a shot, a low boom on the first frame: a whirling sword of flame igniting in the eastern opening of the garden, huge; fruit torn from a branch; the serpent's eye, very close; fig leaves pulled from a branch; thorns breaking through cracked ground; a grain of dust; two small figures walking east into a dark land, the fire behind them. Then black."),
        ("BEAT", 7, "Montage at full drive; the flame roars on the last shot, then the music cuts to nothing."),
        ("PIC", "Where The Garden ended: the tree in the middle of the garden at dusk, perfectly still. Something moves in the long grass at its foot."),
        ("GUIDE", "The last chapter ended with a man and a woman, naked and unashamed, in a very good world. This chapter answers the question every reader eventually asks. If the world began like that, why is it like this? It begins with a question. Not God's question. Another voice asks first.", "study.oneStory"),  # v1, reshaped in v2
        ("CARD", "THE FALL / Genesis 3:1 to 24"),
        ("BEAT", 4, "Title over the grass at the foot of the tree. A low hit, a dark swell, then quiet."),
    ]),
    ("A crafty voice", [
        ("PIC", "Low in the grass, very close: scales sliding past, the serpent moving through the garden toward its centre. Then the woman beneath the tree, seen from the shoulders up, turning toward a sound in the branches (Eve, cast portrait)."),
        ("V", "3:1", "3:1"),
        ("GUIDE", "The chapter opens with a pun English cannot keep. The pair were naked, arummim. The serpent is crafty, arum. The two words sound almost the same.", "study.originalLanguages"),  # v1
        ("PIC", "Egypt, remembered. A brick yard under a white sun, and above it on a palace wall a carved king wearing the rearing cobra on his brow, gold catching the light. Cut to the wilderness camp by day: the brick-maker, free now, sitting at his tent door, a scar on his forearm, looking at the dust."),
        ("GUIDE", "The people who first heard this had just come out of Egypt, where a rearing cobra crowned Pharaoh's head. In that world the snake meant wisdom, healing, power. Genesis refuses to make it a god. It is a creature the LORD God had made, and it ends this chapter eating dust.", "study.context.historical"),  # new in v2
        ("GUIDE", "Later Scripture names the voice behind it:", "study.context.historical, lexicon.serpent"),  # v1, trimmed
        ("Q", "that ancient serpent called the devil and Satan", "Revelation 12:9", "READER"),
        ("GUIDE", "Jesus calls him", "study.crossReferences (John 8:44)"),  # new in v2
        ("Q", "the father of lies", "John 8:44", "READER"),
        ("BEAT", 2, "The serpent's eye, very close. Silence."),
        ("GUIDE", "And watch how he works. He never commands. He only asks. His first move is a question about what God said.", "study.context.literary, study.hermeneutics.authorIntent"),  # v1
    ]),
    ("Word against word", [
        ("PIC", "Under the tree, the serpent among the branches above her, a thin dark line against the leaves; she looks up at it, calm, unafraid."),
        ("V", "3:2", "3:5"),
        ("PIC", "On screen over the tree, the three versions one above the other. God's words, Genesis 2:16 to 17. Her words, with FREELY fading out, OR TOUCH IT appearing, and SURELY falling away. Then the serpent's, with NOT dropping in front of God's own words. A soft hit on each change."),
        ("GUIDE", "Lay the two side by side and you can watch the lie being built. God said, eat freely from every tree, with one limit and a clear warning. She drops the freely, adds touching, and softens the warning. She shrinks the gift and enlarges the limit.", "study.originalLanguages, study.crossReferences (Genesis 2:16 to 17)"),  # v1, extended in v2
        ("GUIDE", "Then the serpent takes God's own words and puts a not in front of them. He contradicts God word for word, and he paints the Giver of every tree as jealous, holding something good back.", "study.originalLanguages, study.god"),  # v1
        ("BEAT", 2, "NOT settles on screen in front of God's words. One low hit."),
        ("GUIDE", "Notice too that the narrator says the LORD God, His covenant name. In this conversation they say only God. The personal name drops out just as trust in Him is dissolving.", "study.originalLanguages"),  # v1
        ("GUIDE", "The root of sin, as Genesis tells it, is not ignorance. It is distrust. A willingness to believe that God is holding back something good, and that His word can be edited.", "study.hermeneutics.authorIntent"),  # v1, extended in v2
        ("BEAT", 2, "Hold on the fruit in the branches. One low tone."),
    ]),
    ("She took and ate", [
        ("PIC", "Set piece: the eating. Extreme slow motion and close: the fruit hanging in warm light; her eyes on it; her hand rising through the leaves; fingers closing; the branch springing back as the fruit comes away, leaves falling. She turns and holds it out. His hand takes it (Adam, cast portrait). Fruit of no particular kind, never an apple."),
        ("V", "3:6", "3:6"),
        ("BEAT", 12, "Set piece: the eating, no narration. A rising pulse under the slow motion; on the bite the score cuts out and there is only the wind. The warm light goes cold as a cloud crosses the garden; the wind turns; leaves fall."),
        ("PIC", "Hard cut: an eye opening, very close, exactly as the man's eye opened on his first breath in The Garden, but now the eye is afraid. Then hands tearing broad fig leaves from a branch, fast, the leaves tied together with fibre."),
        ("V", "3:7", "3:7"),
        ("BEAT", 3, "The rip of leaves, close, then silence."),
        ("GUIDE", "This is the only window the narrator gives into her mind, and it climbs. Good for food: the appetite. Pleasing to the eyes: the eye. Desirable for wisdom: ambition.", "study.context.literary"),  # v1
        ("GUIDE", "Desirable is the verb of the tenth commandment.", "study.originalLanguages"),  # v1, split in v2
        ("Q", "You shall not covet", "Exodus 20:17", "READER"),
        ("GUIDE", "What God made to be enjoyed becomes something to be seized. And the man was with her the whole time, saying nothing at all.", "study.originalLanguages, study.context.literary"),  # v1
        ("GUIDE", "Their eyes are opened, as the serpent promised. But what they see is their own exposure. One act fractures every relationship at once. They hide from God, they cover themselves from each other, and the fig leaves are their own attempt to fix it.", "study.originalLanguages, study.hermeneutics.authorIntent, study.typology[0]"),  # v1, extended in v2
    ]),
    ("The voice in the garden", [
        ("PIC", "Set piece: the voice in the garden. Evening. A wind enters the garden from far off and moves through it in one long wave, treetop after treetop bending, light shifting across the ground between the trunks, as though something walks there. No figure anywhere. The man and the woman, in fig leaves, pressing back among dark trunks."),
        ("V", "3:8", "3:8"),
        ("BEAT", 14, "Set piece: the voice in the garden, no narration. Wind like footsteps, each wave nearer and louder; the score builds under it to an immense held chord; the pair's breathing, close; then everything stops."),
        ("V", "3:9", "3:9"),
        ("BEAT", 3, "Silence. Hold on the trees."),
        ("V", "3:10", "3:10"),
        ("PIC", "The wilderness camp at dusk: the tent sanctuary at the centre, smoke rising from before its gate, a wind moving through the camp and stirring the tent cloths. The brick-maker stands at his door and listens."),
        ("GUIDE", "Walking is the very word Israel would later use for God's presence moving through their camp. Their sanctuary was a garden like this one. And here, the man and the woman hide from Him among the trees He planted.", "study.context.historical"),  # v1, extended in v2
        ("GUIDE", "Many readers see this question as the centre of the whole chapter. The turning point is not the eating. It is the God who comes looking. He knows where they are. He asks so that the guilty will speak the truth, as He later asks Cain,", "study.context.literary, study.god"),  # v1, extended in v2
        ("Q", "Where is your brother Abel?", "Genesis 4:9", "READER"),
        ("GUIDE", "and Elijah,", "study.god"),  # new in v2
        ("Q", "What are you doing here?", "1 Kings 19:9", "READER"),
        ("GUIDE", "God's first word to fallen humanity is not a sentence. It is a search.", "study.god"),  # new in v2
    ]),
    ("The woman whom You gave me", [
        ("PIC", "Failing light. The man in fig leaves among dark trunks, chest up, head lowered, not meeting the light; then the woman, the same; the serpent lying still in the grass between them."),
        ("V", "3:11", "3:13"),
        ("PIC", "Graphic over a slow push across the garden floor: three marks, the serpent, the woman, the man. A line draws the sin down from serpent to woman to man; the questions climb back from man to woman; the blame slides back down to the serpent; then the sentences run the first way again, serpent, woman, man."),
        ("GUIDE", "Look at the shape of it. The sin travels from serpent to woman to man. God's questions run the other way, man then woman, and the blame is passed back down the line. The sentences will retrace the first order.", "study.context.literary"),  # v1, extended in v2
        ("GUIDE", "The man said nothing until he was questioned, and now he speaks to excuse himself. The woman whom You gave me. What she says is true, but it is not a defence.", "study.context.literary, study.hermeneutics.debates[0].bearing"),  # v1, merged in v2
        ("GUIDE", "And God puts no question to the serpent. He does not negotiate with evil. He sentences it.", "study.god"),  # v1
    ]),
    ("The long war", [
        ("PIC", "Bare dust at the garden's edge in low light: the serpent going on its belly through the dust, its trail a long line behind it, the wind blowing dust across it."),
        ("V", "3:14", "3:14"),
        ("GUIDE", "Cursed falls on the serpent and on the ground, never on the man or the woman themselves. And even in Isaiah's renewed world, this one sentence still stands:", "study.god, study.context.canonical"),  # v1
        ("Q", "the food of the serpent will be dust", "Isaiah 65:25", "READER"),
        ("PIC", "Dawn breaking low over the dust; a single line of gold light falling across the ground. The serpent rears in shadow at the edge of the light."),
        ("V", "3:15", "3:15"),
        ("BEAT", 2, "One low boom, then silence."),
        ("GUIDE", "Enmity means open war. The rescue of the world begins as God's own declaration of war on evil.", "lexicon.enmity"),  # v1
        ("GUIDE", "One verb stands behind both blows, the head and the heel. The difference is the target: a fatal blow against a wounding one. And the seed is he. Even the old Greek translators heard a person in this promise. A long war between two lines, but the decisive blow is struck by one.", "study.originalLanguages, lexicon.seed"),  # v1, extended in v2
        ("GUIDE", "This is the first announcement of the gospel, and it is spoken before a single sentence falls on the man and the woman.", "study.basic.christ, study.god"),  # v1
        ("PIC", "Montage: the long war, fast and dark, two to three seconds a shot. Two offerings smoking on two altars in a field, one smoke rising, one blown flat; a staff lying in a field at dusk; a line of graves along a hillside, one after another; a great brick tower rising on a plain and people walking east toward it; a long column of captives walking east across a desert under guard toward a great walled city. The words AND THEN HE DIED appear again and again on screen, faster each time. Last: the serpent rearing to strike in the dust. Cut to black."),
        ("BEAT", 12, "Montage: the long war, no narration. Driving low percussion; a hit on every AND THEN HE DIED; it stops dead on the strike."),
    ]),
    ("Dust you are", [
        ("PIC", "The garden under a heavy sky at dusk, wind bending the long grass; the woman, in fig leaves, chest up, her face to the wind."),
        ("V", "3:16", "3:16"),
        ("GUIDE", "Her pain is the same word as the man's toil: the sentence falls on both in the same currency. And the desire and the rule describe a marriage bent by sin, not God's design. It is a sorrowful description of the world under judgment, never a charter for it.", "study.originalLanguages, study.hermeneutics.descriptionVsPrescription"),  # v1
        ("PIC", "Beyond the trees, a hard field under a hot sky: thorns and thistles bursting up through cracked ground in time lapse; the man's hands, bleeding, tearing at the thorns; sweat running down his brow, his face from the chest up."),
        ("V", "3:17", "3:19"),
        ("PIC", "Set piece: dust to dust. The opening of The Garden played backward: the man's eye closing; his face going still; the earth taking him back, the dust drawing in where he lay; a single grain of dust in macro; then the camera rising from the grain, fast, up over bare ground, up through the clouds, up into the high cold light above the world, and holding there."),
        ("BEAT", 14, "Set piece: dust to dust, no narration. The breath from The Garden, played in reverse, drawn back out; the score from The Garden's opening, slowed and darkened; wind rush rising with the camera; silence at the top."),
        ("GUIDE", "Chapter two ran from dust to a living man. Chapter three runs that film backward. The man taken from the ground will return to it. And from here a refrain tolls through Genesis, beginning with Adam himself:", "study.context.literary, study.god"),  # v1, extended in v2
        ("Q", "and then he died", "Genesis 5:5", "READER"),
        ("BEAT", 2, "Silence."),
        ("GUIDE", "Yet mercy is laced through the judgment. Childbearing goes on, so the promised seed can still come. Work goes on, so life goes on. Judgment is real, but it is bounded.", "study.god"),  # v1, extended in v2
    ]),
    ("Clothed", [
        ("PIC", "First light over the garden after the night. The man and the woman standing together among the trees, chest up, in fig leaves, his face toward her."),
        ("V", "3:20", "3:20"),
        ("GUIDE", "Eve sounds like the Hebrew for living. In the very hour death enters, he names her the mother of all the living. A small act of hope in God's promise.", "lexicon.eve"),  # v1
        ("PIC", "Close: simple garments of skin laid over two pairs of shoulders in warm light; the fig leaves falling to the ground. No hands from above, no figure."),
        ("V", "3:21", "3:21"),
        ("PIC", "The tabernacle courtyard by day, seen from across the camp: men in new white linen tunics standing in a line before the bronze altar, an older man in a plain robe fastening a sash on the first of them, faces small and far off. The brick-maker watching from the crowd at the courtyard gate."),
        ("GUIDE", "The fig leaves were their own covering. These garments are God's. And the words are the ones used when Moses clothed Israel's priests. The brick-maker would have watched it happen: tunics, the same word, put on by another's hands.", "study.typology[0], study.originalLanguages"),  # v1, extended in v2
        ("GUIDE", "The text does not describe a sacrifice, so the link is an inference, but a fair one. The covering came from a life taken.", "study.typology[0]"),  # v1
    ]),
    ("East of Eden", [
        ("PIC", "The tree of life at the far centre of the garden in soft light, seen from a great distance through the trees, wind in its leaves; no figure."),
        ("V", "3:22", "3:22"),
        ("GUIDE", "Even the exile is a mercy. It guards them from living forever in a fallen state.", "study.god"),  # v1
        ("PIC", "Set piece: east of Eden. The man and the woman, clothed in skins, walking east out of the garden at dusk, seen from behind, the trees ending, a wide dry land opening before them. Behind them, in the eastern opening between the great trees, fire: a whirling sword of flame, a long blade of living fire turning in the air, its light flashing on the trunks; around it, vast shapes of wings made of flame and shadow, never faces, never figures. The camera pulls back and up until they are two specks in the dark land and the flame is a single point of fire behind them."),
        ("V", "3:23", "3:24"),
        ("BEAT", 16, "Set piece: east of Eden, no narration. The sword ignites with a roar; the biggest swell in the film, choir and drums; the fire turning; their footsteps on hard ground; the pull back; the music drains away to wind and one far crackle of flame."),
        ("GUIDE", "Stationed is the verb of God's dwelling, the root of the word for the tabernacle. The guard that keeps sinners out is described in the language of God's house.", "study.originalLanguages"),  # new in v2
        ("PIC", "The wilderness camp: the tabernacle gate, facing east; then inside the holy place in low lamplight, the great veil, blue, purple and scarlet, with cherubim woven into it. The brick-maker outside the courtyard gate, at dusk, looking in but never going in."),
        ("GUIDE", "To Israel this sounded like being barred from the sanctuary. Its door faced east, and cherubim were woven into the veil before the Most Holy Place. No one simply walked back in.", "study.context.historical, study.god"),  # v1, extended in v2
        ("GUIDE", "And Israel heard its own story in Adam. Given a good land and one word to keep, warned of death, they disobeyed, and they too were carried east, into exile in Babylon. Hosea says they", "study.context.historical"),  # new in v2
        ("Q", "like Adam, have transgressed the covenant", "Hosea 6:7", "READER"),
        ("GUIDE", "East becomes a direction in Genesis. Cain settles east of Eden. The builders of Babel journey east. Humanity keeps moving away from the presence it lost.", "study.context.literary"),  # v1
    ]),
    ("The seed of the woman", [
        ("PIC", "A wilderness of stone and dry hills at first light, empty; loose stones on the ground, each one shaped like a loaf; heat shimmer. No figures."),
        ("BEAT", 4, "Wind over the empty wilderness; a new cue begins, low and patient."),
        ("GUIDE", "Verse fifteen never names the victor, and the rest of the Bible keeps watching for him. The promise narrows to Abraham, then to David, and comes to rest on one person. God sent His Son, Paul says,", "study.christ"),  # v1
        ("Q", "born of a woman", "Galatians 4:4", "READER"),
        ("GUIDE", "Luke traces Jesus back to", "study.christ"),  # new in v2
        ("Q", "the son of Adam, the son of God", "Luke 3:38", "READER"),
        ("GUIDE", "and the very next scene is the temptation. The last Adam meets the same enemy, in a wilderness instead of a garden, hungry instead of surrounded by fruit. The serpent began by questioning what God said. Jesus answers with what God said:", "study.christ"),  # v1, extended in v2
        ("Q", "It is written", "Matthew 4:4", "READER"),
        ("BEAT", 2, "One sustained tone over the stones."),
        ("PIC", "An olive grove at night across a dry stream bed, torchlight moving between the trees; a crown of thorns lying on a flat stone; a rough wooden beam against a dark sky; no figures."),
        ("GUIDE", "Adam hid among the trees. Christ was hung on a tree. Adam reached for what was forbidden. Christ, in a garden, prayed,", "study.christ"),  # v1
        ("Q", "not as I will, but as You will", "Matthew 26:39", "READER"),
        ("GUIDE", "Adam wore thorns as the fruit of his sin. Christ wore them as a crown. Adam left the garden to die. Christ was laid in a garden tomb, and rose. The promise never pictured a victory without cost. He shared our flesh and blood,", "study.christ"),  # v1
        ("Q", "so that by His death He might destroy him who holds the power of death", "Hebrews 2:14", "READER"),
        ("GUIDE", "The strike to the heel and the crushing of the head happen in the same act.", "study.christ"),  # v1
        ("PIC", "Set piece: the veil to the empty tomb. Darkness over the land; the ground shakes; in the holy place the great veil with its cherubim tears from top to bottom and light floods through the tear; dawn in a garden, a rock cut tomb, the stone rolled back, light on the path; at the foot of the rock, in the dust, the serpent lies still, and the wind blows it away as dust. No figures."),
        ("BEAT", 16, "Set piece: the veil to the empty tomb, no narration. Silence and darkness; a deep rumble; the tear, loud, cloth ripping from top to bottom; the score bursts into light; birdsong at the tomb; the same wind that walked in the garden."),
    ]),
    ("The way back", [
        ("PIC", "The torn veil from inside, light pouring through it; then a radiant city with a river of clear water running through its centre and the tree of life on both banks, fruit in the light. No flame, no guard: the way open."),
        ("GUIDE", "The cherubim that barred the way to life stood again over the mercy seat in Israel's sanctuary, where God promised,", "study.god, study.typology[3]"),  # new in v2
        ("Q", "I will meet with you there", "Exodus 25:22", "READER"),
        ("GUIDE", "The guard at the door of Eden became the throne of atonement. And when Jesus died, the veil with its cherubim was torn from top to bottom. Believers now come in", "study.god, study.typology[3]"),  # v1, extended in v2
        ("Q", "by the new and living way opened for us through the curtain of His body", "Hebrews 10:19 to 20", "READER"),
        ("GUIDE", "The Bible closes by undoing this chapter. No longer any curse. The tree of life open beside the river. And the pair who hid from God among the trees are answered by a people who", "study.oneStory"),  # v1
        ("Q", "will see His face", "Revelation 22:4", "READER"),
        ("BEAT", 8, "The city and the tree of life, the river in the light. The warmest swell in the film, no narration."),
    ]),
    ("Come out", [
        ("PIC", "Dawn in the wilderness camp. The brick-maker steps out of his dark tent into first light and walks toward the tabernacle gate, the smoke rising before it."),
        ("GUIDE", "So hear God's questions as grace. The right answer to His question is not to hide and not to blame. It is to come out, confess, and trust the God who promised a Rescuer and clothed the naked.", "study.god"),  # v1
        ("GUIDE", "God covered their shame with garments He provided. What are you using to cover your own shame, and what would it mean to receive God's covering in Christ instead?", "questions[3]"),  # v1
        ("BEAT", 3, "Hold on the light."),
        ("PIC", "East of Eden at evening: a field of hard ground, two smokes rising from two altars, and between them a young man looking back over his shoulder at a door in the dusk. Cut to black."),
        ("GUIDE", "East of Eden, the first children are born. Two brothers bring offerings to God. And the next time God comes asking a question, it will be about a brother.", "series link to Cain and Abel (not from the study)"),  # new in v2
        ("CARD", "Study The Fall / makor.co.za/genesis/the-fall"),
        ("BEAT", 6, "End card with a WATCH NEXT space for Cain and Abel."),
    ]),
]

HEADER = """# The Fall v2: full movement film script 

Genesis 3:1 to 24, rebuilt to films/CINEMA-STANDARD.md like The Seven Days v2 and The Garden v2.
Generated by `script/movement.py`; edit that file, not this one. Treatment and storyboard plan:
`../TREATMENT.md`.

Runtime: **{total}** ({basis}). All {n} verses appear once, in order, verbatim BSB from the
study JSON (checked by the generator). Words: {words}.

## Voices

READER for Scripture and for every speaker who is not God (the serpent, the woman, the man), GOD
only for God's own words (3:9, 3:11, 3:13a, 3:14 to 19, 3:22, and the flash-forward of 3:9),
GUIDE for everything else. Splits set by hand in `SPEAKERS`, as v1, verified against the study.

## Chapters

```
{chapters}
```
"""

if __name__ == "__main__":
    Film(HERE, REPO / "src/content/studies/genesis/03-the-fall.json", VOICE_MAP, SPEAKERS).build(CHAPTERS, HEADER)
