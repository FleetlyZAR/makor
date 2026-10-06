#!/usr/bin/env python3
"""Full movement film script: The Garden (Genesis 2:4 to 25), YouTube epic. DRAFT for review.

Scripture comes only from the study JSON (verified by films/tools/movement_script.py).
GUIDE lines are Makor's own words, each tagged with its study field.

    python3 films/genesis/02-the-garden/script/movement.py
"""
import pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "films" / "tools"))
from movement_script import Film  # noqa: E402

# Decision D3 (see PRODUCTION-PLAN.md): who reads the man's words in 2:23.
# Makor rule so far: anyone other than God is read by the READER.
VOICE_MAP = {"MAN": "READER"}

CHAPTERS = [
    ("Cold open", [
        ("PIC", "High above the finished world of The Seven Days, the bay at rest in golden light. The camera begins to come down, out of the sky, toward the ground."),
        ("GUIDE", "Chapter one gave the world its shape. This chapter gives it a centre: a garden where the LORD God dwells with the man and woman He has made.", "study.oneStory"),
        ("CARD", "THE GARDEN / Genesis 2:4 to 25"),
        ("BEAT", 4, "The camera settles at ground level, on dry earth. Music opens."),
    ]),
    ("From the heavens to the ground", [
        ("PIC", "Dry, empty ground at first light; no shrub, no plant; mist rising from springs in the earth."),
        ("V", "2:4", "2:4"),
        ("GUIDE", "This is the account. It is the first of the headings that divide Genesis into its movements, and each one tells what came out of the thing it names.", "study.context.literary"),
        ("GUIDE", "Listen to the turn inside the verse. The heavens and the earth become the earth and the heavens, and the camera comes down from the sky to the ground.", "study.context.literary"),
        ("GUIDE", "And God now has a name. The LORD, in small capitals, stands for His covenant name. The mighty Creator of chapter one is the same God who draws near.", "lexicon.yhwh"),
        ("GUIDE", "Some read this chapter as a second, separate account. Read as it stands, it is a close up of the sixth day, and Jesus quotes both chapters together as one word from the Creator.", "study.hermeneutics.debates[0]"),
    ]),
    ("Dust and breath", [
        ("PIC", "The bare ground, no plant, no rain; springs welling up and darkening the dust."),
        ("V", "2:5", "2:6"),
        ("GUIDE", "The scene opens with what is missing. No shrub, no plant, no rain, and no man to cultivate the ground. Every lack is about to be met.", "study.context.literary"),
        ("PIC", "The damp dust stirs and gathers, drawn together by an unseen hand of wind and light into the shape of a man lying on the ground, seen from a distance. No hands, no figure of God: only the effect."),
        ("V", "2:7", "2:7"),
        ("GUIDE", "Formed is the potter's verb, the word for hands shaping clay. Isaiah says it plainly:", "study.originalLanguages"),
        ("Q", "we are the clay, and You are the potter,", "Isaiah 64:8", "READER"),
        ("GUIDE", "The animals are formed too, and the man is called a living being, the same words used for them. What sets him apart is that God breathes into him personally.", "study.originalLanguages"),
        ("GUIDE", "Man, adam, is taken from the ground, adamah. We are earthy creatures, given dignity only by the breath of God.", "lexicon.adamah"),
        ("Q", "the breath of the Almighty gives me life,", "Job 33:4", "READER"),
    ]),
    ("A garden in Eden", [
        ("PIC", "A garden planted in the east: trees of every kind, pleasing to the eye and good for food; at its centre, two trees standing apart in soft light."),
        ("V", "2:8", "2:9"),
        ("GUIDE", "Eden means delight. It is a garden of God's own planting, the first place where God dwells with man.", "lexicon.eden"),
        ("GUIDE", "Notice the two trees in the middle. They are placed carefully, with the man, the woman and the command, so that the next chapter can test each one.", "study.context.literary"),
        ("PIC", "A river flowing out of the garden and dividing into four great headwaters across the land, gold glinting in the riverbed."),
        ("V", "2:10", "2:14"),
        ("GUIDE", "The geography is deliberately real and deliberately beyond reach. Every Israelite knew the Tigris and the Euphrates. The Pishon and the Gihon cannot be identified with certainty.", "study.context.historical"),
        ("GUIDE", "And for Israel the garden looked like a sanctuary. Its entrance faces east, as the tabernacle's did. Gold and onyx were the materials of the priestly garments. Israel's worship was, in part, a memory of Eden.", "study.context.historical"),
    ]),
    ("To cultivate and keep", [
        ("PIC", "The man, small in the landscape, at work among the trees of the garden, tending the ground at first light."),
        ("V", "2:15", "2:15"),
        ("GUIDE", "Cultivate and keep. The first verb means to work or serve, and is the ordinary word for serving God in worship. The second means to guard and keep, the word for keeping God's commands.", "study.originalLanguages"),
        ("GUIDE", "Together they describe the Levites in the tabernacle. Adam's work is farming, but it is also priestly service in the place where God dwells.", "study.originalLanguages"),
        ("PIC", "Stillness in the garden; the tree of the knowledge of good and evil standing at the centre; the voice comes with no figure, only wind moving softly through the leaves."),
        ("V", "2:16", "2:17"),
        ("GUIDE", "Listen to the order. The command opens with permission, every tree of the garden, and only then sets one limit. God's commands are not the grudging rules of a jealous master, but the boundaries of a good home.", "study.god"),
        ("GUIDE", "And the warning is plain. God does not hide the consequences of disobedience. His word defines what is good and what is evil, and life depends on trusting it.", "study.god"),
        ("GUIDE", "Whatever the knowledge of good and evil means exactly, the heart of the matter is trust: whether the man will receive it from God's word, or seize it on his own terms.", "study.hermeneutics.debates[1].bearing"),
    ]),
    ("Not good to be alone", [
        ("PIC", "The man alone at evening in the wide garden, very small among the trees."),
        ("V", "2:18", "2:18"),
        ("GUIDE", "The first thing in the Bible called not good. And it is God Himself who names the lack, before the man does.", "study.context.literary"),
        ("GUIDE", "Helper is ezer, and Scripture uses that word most often of God Himself.", "study.crossReferences (Psalm 121)"),
        ("Q", "My help comes from the LORD, the Maker of heaven and earth.", "Psalm 121:2", "READER"),
        ("GUIDE", "It speaks of strength brought alongside, never of someone lesser. Suitable means one who stands face to face with him, his match.", "lexicon.ezer"),
        ("PIC", "The animals and birds of the garden coming before the man one by one, the man at a distance among them."),
        ("V", "2:19", "2:20"),
        ("GUIDE", "God brings the animals to the man to see what he would name each one, and honours his choices. But none of them stands face to face with him.", "study.god"),
    ]),
    ("Bone of my bones", [
        ("PIC", "Dusk deepening into night over the garden; the man asleep beneath a tree, seen from far away; soft light gathering near him. No figure of God."),
        ("V", "2:21", "2:22"),
        ("GUIDE", "The deep sleep is the same sleep that falls on Abram before God makes covenant with him. God works while the man is passive.", "study.originalLanguages"),
        ("GUIDE", "And the verb for made is built. God builds the woman as a builder raises a house, and then He Himself brings her to the man.", "study.originalLanguages"),
        ("PIC", "Morning light. Far across the garden, two small figures meeting among the trees; nothing close, nothing detailed."),
        ("V", "2:23", "2:23"),
        ("GUIDE", "These are the first recorded human words in the Bible, and they are poetry. Man and woman, ish and ishshah, sound alike. Bone of my bones is the language of family.", "study.originalLanguages"),
        ("V", "2:24", "2:24"),
        ("GUIDE", "The narrator steps out of the story to apply it to every marriage after it. To be united is to cling or hold fast, the word Ruth uses of Naomi. Marriage is a loyalty chosen and kept, not only a feeling.", "study.originalLanguages"),
        ("PIC", "The garden in full light, the two far off together among the trees; peace, no fear."),
        ("V", "2:25", "2:25"),
        ("GUIDE", "Naked, and not ashamed. The line closes the scene and sets up the next one. Every gift in this chapter is about to be tested.", "study.context.literary"),
    ]),
    ("The last Adam", [
        ("PIC", "Light falling into a garden at dawn: an olive grove, then a rock cut tomb with its stone rolled back, no figures."),
        ("GUIDE", "Paul quotes this chapter and names Jesus as the last Adam.", "study.christ"),
        ("Q", "The first man Adam became a living being; the last Adam a life-giving spirit,", "1 Corinthians 15:45", "READER"),
        ("GUIDE", "Adam was placed in a garden to serve and guard it, and given one word to keep. He failed at every point. Christ comes as the obedient Man who serves His Father perfectly.", "study.christ"),
        ("GUIDE", "John frames the passion with gardens. Jesus is arrested in a garden, buried in a garden, and on Easter morning Mary thinks He is the gardener. In a sense she is right.", "study.christ"),
        ("GUIDE", "That evening He breathes on His disciples, as God breathed into the first man, and says:", "study.crossReferences (John 20:22)"),
        ("Q", "Receive the Holy Spirit,", "John 20:22", "READER"),
        ("GUIDE", "And He quotes this chapter on marriage, calling it back to how it was from the beginning:", "study.christ"),
        ("Q", "what God has joined together, let man not separate,", "Mark 10:9", "READER"),
        ("GUIDE", "Paul goes further. The one flesh union was always pointing beyond itself.", "study.christ"),
        ("Q", "This mystery is profound, but I am speaking about Christ and the church,", "Ephesians 5:32", "READER"),
    ]),
    ("Eden restored", [
        ("PIC", "The garden seen from far above; then thorns and toil; then a radiant city with a river flowing through it and trees on both banks."),
        ("GUIDE", "When chapter three comes, each gift in this garden is damaged. The ground is cursed, work becomes toil, the marriage is strained, shame replaces nakedness without shame, and the way to the tree of life is barred.", "study.oneStory"),
        ("GUIDE", "But the Bible ends with Eden restored and surpassed. The river of the water of life flows from the throne of God and of the Lamb, and the tree of life stands on either side of it.", "study.oneStory"),
        ("Q", "eat from the tree of life in the Paradise of God,", "Revelation 2:7", "READER"),
        ("GUIDE", "The garden has become a city, but it is still a home where God and His people live together.", "study.oneStory"),
    ]),
    ("Dust that breathes", [
        ("PIC", "Back to the first image: dust on the ground, a breath of wind, first light."),
        ("GUIDE", "We are dust that breathes because He breathed. Every good gift, food, work, beauty, marriage and friendship, comes from His hand, and even His limits are a form of His care.", "study.god"),
        ("GUIDE", "You were formed from dust and given life by God's breath. How does remembering that change how you see your worth today?", "questions[0]"),
        ("BEAT", 4, "Hold on the light. Music resolves."),
        ("CARD", "Study The Garden / makor.co.za/genesis/the-garden"),
        ("BEAT", 4, "End card."),
    ]),
]

HEADER = """# The Garden: full movement film script (DRAFT)

Genesis 2:4 to 25. One film for YouTube, built on the Makor study, using the method and
tools proven on The Seven Days. Generated by `script/movement.py`; edit that file, not this one.

Runtime: **{total}** ({basis}). All {n} verses appear once, in order, verbatim BSB from the
study JSON (checked by the generator). Words: {words}.

## Voices

Same three as The Seven Days (films/VOICES.md): READER for Scripture, GOD for God's own
words (here 2:16 to 17 and 2:18), GUIDE (`am_michael`) for everything else. The man's words
in 2:23 are read by the READER unless decision D3 says otherwise.

## Chapters

```
{chapters}
```
"""

if __name__ == "__main__":
    Film(HERE, REPO / "src/content/studies/genesis/02-the-garden.json", VOICE_MAP).build(CHAPTERS, HEADER)
