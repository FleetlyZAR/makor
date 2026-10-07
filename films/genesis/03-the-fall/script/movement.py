#!/usr/bin/env python3
"""Full movement film script: The Fall (Genesis 3:1 to 24), YouTube epic. DRAFT for review.

Scripture comes only from the study JSON (verified by films/tools/movement_script.py).
GUIDE lines are Makor's own words, each tagged with its study field.

    python3 films/genesis/03-the-fall/script/movement.py
"""
import pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "films" / "tools"))
from movement_script import Film  # noqa: E402

# Decision D2 (see PRODUCTION-PLAN.md): every speaker other than God is read by the READER.
VOICE_MAP = {"MAN": "READER", "WOMAN": "READER", "SERPENT": "READER"}

# Genesis 3 tags its speech in ways the generic detector cannot read ("called out to the
# man," "asked the LORD God.", "said to the serpent:"), so every verse where God speaks is
# split by hand. The generator checks each split joins back into the exact verse.
# The serpent's, the woman's and the man's words (3:1 to 5, 3:10, 3:12, 3:13b) stay READER,
# including the woman's version of God's command in 3:3, which is her words, not His.
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
        ("PIC", "The garden as The Garden left it: Eden in full morning light, the two far off among the trees, at peace. Then, low in the grass at the edge of the frame, something moves."),
        ("GUIDE", "The last chapter ended with a man and a woman naked and unashamed in a good garden. This chapter answers the question every reader eventually asks: if the world began like that, why is it like this?", "study.oneStory"),
        ("CARD", "THE FALL / Genesis 3:1 to 24"),
        ("BEAT", 4, "The grass is still again. Music opens, darker than before."),
    ]),
    ("Did God really say?", [
        ("PIC", "Long grass at the foot of the trees; a small snake, far off and half hidden, moving through the grass toward the centre of the garden."),
        ("V", "3:1", "3:1"),
        ("GUIDE", "The chapter opens with a pun English cannot keep. The pair were naked, arummim. The serpent is crafty, arum. The two words sound almost the same.", "study.originalLanguages"),
        ("GUIDE", "The ancient world wove the snake into its royal and sacred imagery. Genesis calls it simply a creature the LORD God had made. But later Scripture names the enemy behind the voice:", "study.context.historical, lexicon.serpent"),
        ("Q", "that ancient serpent called the devil and Satan", "Revelation 12:9", "READER"),
        ("GUIDE", "He never commands. He only asks, and his first move is a question about what God said.", "study.context.literary, study.hermeneutics.authorIntent"),
        ("PIC", "The tree in the middle of the garden, seen from far off between the trunks of other trees; beneath it, very small, the woman in profile; the snake low in the grass near her, a thin dark line, far off."),
        ("V", "3:2", "3:3"),
        ("GUIDE", "God gave every tree freely and set one limit. She drops the freely, adds touching, and softens the warning. She shrinks the gift and enlarges the limit.", "study.originalLanguages, study.crossReferences (Genesis 2:16 to 17)"),
        ("V", "3:4", "3:5"),
        ("GUIDE", "The serpent takes God's own warning and puts a not in front of it. He contradicts God word for word, and paints the Giver of every tree as jealous. The root of sin, as Genesis tells it, is not ignorance but distrust.", "study.originalLanguages, study.god, study.hermeneutics.authorIntent"),
        ("GUIDE", "Notice too that the narrator says the LORD God, His covenant name, but in this conversation they say only God. The personal name drops out just as trust in Him is dissolving.", "study.originalLanguages"),
    ]),
    ("She took and ate", [
        ("PIC", "The tree in the middle of the garden in warm light, heavy with fruit of no particular kind; two very small figures beneath it, far off, framed by branches. Nothing close."),
        ("V", "3:6", "3:6"),
        ("GUIDE", "This is the only window the narrator gives into her mind, and it climbs. Good for food: the appetite. Pleasing to the eyes: the eye. Desirable for wisdom: ambition.", "study.context.literary"),
        ("GUIDE", "Desirable is the verb of the tenth commandment, you shall not covet. What God made to be enjoyed becomes something to be seized. And the man was with her, saying nothing at all.", "study.originalLanguages, study.context.literary"),
        ("PIC", "Broad fig leaves in the foreground, dark against the evening light; far beyond them, two tiny figures withdrawn into the shade of the trees."),
        ("V", "3:7", "3:7"),
        ("GUIDE", "Their eyes are opened, but what they see is their own exposure. One act fractures every relationship at once, and shame arrives before any sentence is spoken. The fig leaves are their own attempt to cover it.", "study.originalLanguages, study.hermeneutics.authorIntent, study.typology[0]"),
    ]),
    ("Where are you?", [
        ("PIC", "Evening in the garden. Wind moves through the treetops in a long wave, and light shifts across the ground between the trunks, as though something passes through. No figure anywhere."),
        ("V", "3:8", "3:8"),
        ("GUIDE", "Walking is the verb later used for God's presence moving through Israel's camp. And they hide from Him among the very trees He planted.", "study.context.historical, study.christ"),
        ("PIC", "Deep among dark trunks, the evening light moving through the leaves toward the place where the two are hidden, far off and unseen."),
        ("V", "3:9", "3:9"),
        ("GUIDE", "Many readers see this question at the centre of the chapter. The turning point is not the eating but the God who comes looking. He knows where they are. He asks so that the guilty will speak the truth.", "study.context.literary, study.god"),
        ("V", "3:10", "3:10"),
    ]),
    ("The woman whom You gave me", [
        ("PIC", "The garden in failing light; two far off figures half hidden among dark trunks; in the low grass between the trees, the snake lies still."),
        ("V", "3:11", "3:12"),
        ("GUIDE", "The man said nothing until he was questioned, and now he speaks to excuse himself.", "study.context.literary"),
        ("V", "3:13", "3:13"),
        ("GUIDE", "The sin travelled from serpent to woman to man. The blame is passed back down the line. What she says is true, but it is not a defence.", "study.context.literary, study.hermeneutics.debates[0].bearing"),
        ("GUIDE", "And God questions the man and the woman, but puts no question to the serpent. He does not negotiate with evil. He sentences it.", "study.god"),
    ]),
    ("He will crush your head", [
        ("PIC", "Bare dust at the edge of the garden in low light; the snake, small and far off, going on its belly through the dust. Wind over the ground."),
        ("V", "3:14", "3:14"),
        ("GUIDE", "Cursed falls on the serpent, and on the ground, never on the man or the woman themselves. Even in Isaiah's renewed world, this one sentence stands:", "study.god, study.crossReferences (Isaiah 65:25)"),
        ("Q", "the food of the serpent will be dust", "Isaiah 65:25", "READER"),
        ("PIC", "Dawn breaking low over the dust at the garden's edge; a single line of gold light falling across the ground; the snake gone into shadow."),
        ("V", "3:15", "3:15"),
        ("GUIDE", "Enmity means open war. The rescue of the world begins as God's declaration of war on evil.", "lexicon.enmity"),
        ("GUIDE", "One verb stands behind both blows: the head against the heel, a fatal blow against a wounding one. And the seed is he. A long war between two lines, but the decisive blow is struck by one.", "study.originalLanguages, lexicon.seed, study.hermeneutics.debates[1]"),
        ("GUIDE", "This is the first announcement of the gospel, spoken before a single sentence falls on the man and the woman.", "study.basic.christ, study.god"),
    ]),
    ("Dust you are", [
        ("PIC", "The garden under a heavy sky at dusk, wind bending the long grass; no figures."),
        ("V", "3:16", "3:16"),
        ("GUIDE", "Her pain is the same word as the man's toil. And the desire and the rule describe a marriage bent by sin, not God's design: a sorrowful description of the world under judgment, never a charter for it.", "study.originalLanguages, study.hermeneutics.debates[2].bearing, study.hermeneutics.descriptionVsPrescription"),
        ("PIC", "Beyond the trees, a hard field under a hot sky; thorns and thistles rising from cracked ground; dry wind lifting the dust."),
        ("V", "3:17", "3:19"),
        ("GUIDE", "Chapter two ran from dust to a living man. Chapter three runs that film backward: the man taken from the ground will return to it.", "study.context.literary, study.god"),
        ("GUIDE", "Yet mercy is laced through the judgment. Childbearing continues, so the promised seed can still come. Work continues, so life goes on.", "study.god"),
    ]),
    ("Mother of all the living", [
        ("PIC", "First light over the garden after the night; far off among the trees, two small figures standing together; nothing close."),
        ("V", "3:20", "3:20"),
        ("GUIDE", "Eve sounds like the Hebrew for living. In the very hour death enters, a small act of hope in God's promise.", "lexicon.eve"),
        ("PIC", "Simple garments of skin resting in warm light at the foot of a tree; far beyond, the two small figures among the trunks."),
        ("V", "3:21", "3:21"),
        ("GUIDE", "The fig leaves were their own covering. These garments are God's, and the words are the ones used when Moses clothed Israel's priests.", "study.typology[0], study.originalLanguages"),
        ("GUIDE", "The text does not describe a sacrifice, so the link is an inference, but a fair one: the covering came from a life taken.", "study.typology[0]"),
    ]),
    ("East of Eden", [
        ("PIC", "The tree of life at the far centre of the garden in soft light, seen from a great distance through the trees; wind in the leaves; no figure."),
        ("V", "3:22", "3:22"),
        ("GUIDE", "Even the exile is a mercy. It guards them from living forever in a fallen state.", "study.god"),
        ("PIC", "The eastern edge of the garden at dusk: two very small figures walking away east into a wide dry land, seen from behind, far off; behind them, in the opening between the trees, a slow turning flame of light."),
        ("V", "3:23", "3:24"),
        ("GUIDE", "To Israel this sounded like being barred from the sanctuary: its door faced east, and cherubim were worked into the veil before the Most Holy Place.", "study.context.historical"),
        ("GUIDE", "And east becomes a direction in Genesis. Cain settles east of Eden. Babel's builders journey east. Humanity keeps moving away from the presence it lost.", "study.context.literary"),
    ]),
    ("The seed of the woman", [
        ("PIC", "A wilderness of stone and dry hills at first light, empty, no figures."),
        ("GUIDE", "Verse fifteen does not name the victor. The promise narrows to Abraham, then to David, and comes to rest on one person. God sent His Son, Paul says,", "study.christ"),
        ("Q", "born of a woman", "Galatians 4:4", "READER"),
        ("GUIDE", "Luke traces Jesus back to Adam, and the next scene is the temptation. The last Adam meets the same enemy in a wilderness, hungry, and answers with what God said. He wins where the first man lost.", "study.christ"),
        ("PIC", "An olive grove at night across a dry stream bed; then a rock cut tomb in a garden at first light, the stone rolled back; no figures."),
        ("GUIDE", "Adam hid among the trees. Christ was hung on a tree. Adam reached for what was forbidden. Christ, in a garden, prayed:", "study.christ"),
        ("Q", "not as I will, but as You will", "Matthew 26:39", "READER"),
        ("GUIDE", "Adam wore thorns as the fruit of his sin; Christ wore them as a crown. Adam left the garden to die; Christ was laid in a garden tomb, and rose. And the promise never pictured a victory without cost. He shared our flesh and blood,", "study.christ"),
        ("Q", "so that by His death He might destroy him who holds the power of death", "Hebrews 2:14", "READER"),
        ("GUIDE", "The strike to the heel and the crushing of the head happen in the same act.", "study.christ"),
    ]),
    ("The way to the tree of life", [
        ("PIC", "A great woven curtain torn from top to bottom, warm light pouring through the tear; then a radiant city with a river, and the tree of life on both banks."),
        ("GUIDE", "When Jesus died, the veil with its cherubim was torn from top to bottom. Believers now come in", "study.typology[3]"),
        ("Q", "by the new and living way opened for us through the curtain of His body", "Hebrews 10:19 to 20", "READER"),
        ("GUIDE", "The Bible closes by undoing this chapter. No longer any curse. The tree of life open beside the river. And the pair who hid from God are answered by a people who", "study.crossReferences (Revelation 22:1 to 4)"),
        ("Q", "will see His face", "Revelation 22:4", "READER"),
        ("PIC", "Back in the garden at evening: wind in the trees, light moving gently between the trunks."),
        ("GUIDE", "So hear God's questions as grace. Do not hide or blame. Come out and confess, and trust the God who promised a Rescuer and clothed the naked.", "study.god"),
        ("GUIDE", "God covered their shame with garments He provided. What are you using to cover your own shame, and what would it mean to receive God's covering in Christ instead?", "questions[3]"),
        ("BEAT", 4, "Hold on the light. Music resolves."),
        ("CARD", "Study The Fall / makor.co.za/genesis/the-fall"),
        ("BEAT", 4, "End card."),
    ]),
]

HEADER = """# The Fall: full movement film script (DRAFT)

Genesis 3:1 to 24. The third Makor movement film, after The Seven Days and The Garden, with the
same method and tools. Generated by `script/movement.py`; edit that file, not this one.

Runtime: **{total}** ({basis}). All {n} verses appear once, in order, verbatim BSB from the
study JSON (checked by the generator). Words: {words}.

## Voices

Same three as the earlier films (films/VOICES.md): READER for Scripture and for every speaker
who is not God (the serpent, the woman, the man), GOD only for God's own words (3:9, 3:11,
3:13a, 3:14 to 19, 3:22), GUIDE (`am_michael`) for everything else. The splits are set by hand
in `SPEAKERS` and verified against the study text.

## Chapters

```
{chapters}
```
"""

if __name__ == "__main__":
    Film(HERE, REPO / "src/content/studies/genesis/03-the-fall.json", VOICE_MAP, SPEAKERS).build(CHAPTERS, HEADER)
