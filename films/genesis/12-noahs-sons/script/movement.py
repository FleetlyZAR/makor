#!/usr/bin/env python3
"""Noah's Sons (Genesis 9:18 to 29): built to films/CINEMA-STANDARD.md by the method of The Flood, The Waters
Recede and The Covenant with Noah, with the three rules of films/AUTOPILOT.md (the picture follows the narration;
a face is close or it is not seen; nothing looks like a still) and the Flood review lessons (cast skin and short
curled grey hair held from behind; hands enter the frame level and whole) written into the picture lines from the
start.

Structure from ../TREATMENT.md: a flash-forward open (the first vintage, the lamp in Noah's tent, Ham at the door,
the brothers walking backward with the cloak, and Noah's words "Cursed be Canaan!"), then the hook: four
questions the film answers (why does the righteous man end the flood story drunk in his tent, what did Ham
actually do, why is Canaan cursed when Ham did the wrong, how was this chapter twisted to defend slavery). The
brick-maker is the human strand (the fifth commandment at Sinai with his own old father; the warning at the edge
of Canaan; covering his sleeping father at evening). Set pieces with no narration where the score leads: the
first vintage, the covering, the three sons going out.

The film opens where The Covenant with Noah closes (Noah planting a vine on the mountainside) and stops at
Noah's death (9:29), before the Table of Nations, which is the open loop into the next film.

Nothing in Genesis 9:18 to 29 is God's speech. Noah's oracle (9:25 to 27) is a human speaker and the READER reads
it (Makor rule); SPEAKERS keeps 9:25 with the READER, because the generator would otherwise give "he said," to GOD.

Every GUIDE line carries its study field. Scripture comes only from the study JSON (checked by
films/tools/movement_script.py).

    python3 films/genesis/12-noahs-sons/script/movement.py
"""
import json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "films" / "tools"))
import movement_script  # noqa: E402
from movement_script import Film, PLAIN  # noqa: E402

STUDY = REPO / "src/content/studies/genesis/12-noahs-sons.json"

# Until the voices are rendered, estimate at the pace The Covenant with Noah measured (GOD at speed 0.78).
movement_script.WPM.update({"READER": 147, "GOD": 126, "GUIDE": 140})

VOICE_MAP = {}
_V = {f"{v['chapter']}:{v['n']}": PLAIN(v["text"])
      for u in json.loads(STUDY.read_text())["text"]["units"] for v in u["verses"]}
# Noah speaks 9:25 to 27, a human speaker: the READER reads the whole oracle.
SPEAKERS = {"9:25": [("READER", _V["9:25"])]}

CHAPTERS = [
    ("Cold open", [
        ("PIC", "Where The Covenant with Noah ended: Noah (cast, older) on the mountainside in Ararat pressing a vine cutting into turned earth. Years later: the same slope covered in rows of vines heavy with dark grapes in late summer light, the family (cast) small among the rows, seen from behind, cutting the clusters into baskets."),
        ("BEAT", 4, "The first vintage. Baskets of grapes, bare feet treading in a stone press, juice running dark into a jar. A low warm pulse."),
        ("BEAT", 5, "Montage, quick, each shot its own, the pulse slowing: a clay cup filled from a jar by lamplight; Noah's face close, tired and smiling, the cup at his lips; the tent flap falling shut; the lamp inside guttering; the cup on its side on the rug, wine spilled; Ham (cast) at the tent door seen from behind, light spilling out past him; Shem and Japheth (cast) walking backward, a cloak across their shoulders, their faces turned away."),
        ("PIC", "Morning. Noah (cast, older), his face close, waking under a cloak inside the tent, the light through the hide hard and white, his eyes slowly understanding."),
        ("Q", "Cursed be Canaan! A servant of servants shall he be to his brothers.", "Genesis 9:25, flash-forward", "READER"),
        ("BEAT", 2, "Noah's face. Cut to black and silence on the last second."),
        ("PIC", "The picture follows each question. Noah's empty cup lying on its side on a rug in a dim tent. The tent door seen from outside at night, the lamp glowing through the hide, a man's shadow standing in it. A small boy seen from behind, holding his father's hand on a hillside. An old book of the nations open by candlelight, and beside it a pair of iron shackles lying open and empty on rough planks."),
        ("GUIDE", "Why does the man who survived the flood end up drunk in his tent? What did Ham actually do? Why is Canaan cursed, when Ham did the wrong? And how was this chapter twisted to defend slavery? Four questions. Twelve verses.", "study.oneStory, study.hermeneutics.debates[0], study.hermeneutics.debates[1], study.hermeneutics.descriptionVsPrescription (the four questions are ours; each is answered from the study)"),
        ("CARD", "NOAH'S SONS / Genesis 9:18 to 29"),
        ("BEAT", 3, "Title over the vineyard on the mountainside at dawn, mist in the rows. A low hit, then the wind."),
    ]),
    ("The three sons", [
        ("PIC", "The mountainside in the morning: Shem, Ham and Japheth (cast) walking up through the vines toward the camp, side by side, each face close in turn; one family, one skin, the same dark curled hair; Ham's wife (cast) behind them with a small boy, Canaan, holding her hand, seen from behind."),
        ("V", "9:18", "9:19"),
        ("BEAT", 2, "The three brothers at the top of the rows, the land wide below them. Breath."),
        ("GUIDE", "Three names. And from them, the whole earth. Every people that will ever live is about to come from this one family. The next chapter will trace them, nation by nation.", "study.context.literary, study.oneStory"),
        ("GUIDE", "But listen to the line the narrator adds before anything has happened. And Ham was the father of Canaan. He will say it again in a moment. Canaan plays no part in the scene. The narrator is telling us to watch him.", "study.context.literary"),
        ("PIC", "The boy Canaan seen from behind at the edge of the camp, throwing pebbles down the slope; Ham's hand on his shoulder."),
        ("BEAT", 2, "The boy's pebble skipping down the slope. Breath."),
    ]),
    ("A man of the soil", [
        ("PIC", "Noah (cast, older) kneeling among young vines, both hands whole in the frame, tying a shoot to a stake; his face close, the sun on it; the turned red earth around him."),
        ("V", "9:20", "9:20"),
        ("GUIDE", "A man of the soil. In Hebrew, ish ha'adamah. A man of the ground. Adamah is the ground Adam was taken from. The ground that was cursed. When Noah was born, his father Lamech named him in hope of relief from", "study.originalLanguages, study.crossReferences[1]"),
        ("Q", "the ground that the LORD has cursed", "Genesis 5:29", "READER"),
        ("GUIDE", "Now the ground gives its best gift. A vineyard.", "study.originalLanguages"),
        ("BEAT", 2, "Noah's hands on the vine. Breath."),
        ("GUIDE", "The verb behind proceeded to is chalal. To begin. And in these chapters that verb keeps opening new beginnings that go wrong. Before the flood,", "study.originalLanguages, study.translationNotes[0]"),
        ("Q", "when men began to multiply", "Genesis 6:1", "READER"),
        ("GUIDE", "After it, Nimrod", "study.originalLanguages"),
        ("Q", "began to be a mighty one", "Genesis 10:8", "READER"),
        ("GUIDE", "And at Babel,", "study.originalLanguages"),
        ("Q", "if they have begun to do this", "Genesis 11:6", "GOD"),
        ("GUIDE", "Every fresh start in the early world carries the seeds of new trouble.", "study.originalLanguages"),
        ("BEAT", 10, "Set piece: the first vintage, no narration. Each shot its own: grapes heavy and dusty on the vine; the family (cast) cutting clusters into baskets, hands whole and level; the boy Canaan carrying a small basket, seen from behind; Japheth (cast) and Shem's wife (cast) treading grapes in a stone press, their long robes held clear of the juice and falling below the knee, laughing; juice running down a channel into a clay jar; the jar sealed with clay. The warm theme of the camp, rising."),
        ("GUIDE", "Wine was for feasts and offerings across the ancient world. Scripture can praise", "study.context.historical"),
        ("Q", "wine that gladdens the heart of man", "Psalm 104:15", "READER"),
        ("GUIDE", "and it can warn that", "study.context.historical"),
        ("Q", "wine is a mocker", "Proverbs 20:1", "READER"),
        ("GUIDE", "If Noah was the first to plant a vine, he may not have known what it could do. The text does not excuse him. And it does not lecture him either. It simply tells us what happened.", "study.context.historical"),
        ("BEAT", 2, "The sealed jars in the shade of the tent. Breath."),
    ]),
    ("Inside his tent", [
        ("PIC", "Evening at the camp: Noah (cast, older) sitting alone at the door of his tent, a clay cup in his hand, filling it again from a jar; his face close, warm in the lamplight, his eyes heavy. Then he rises unsteadily and goes inside, and the tent flap falls shut behind him."),
        ("V", "9:21", "9:21"),
        ("BEAT", 3, "The tent from outside in the dark, the lamp glowing through the hide and slowly dimming. The wind. No music."),
        ("GUIDE", "So why does the righteous man end the story drunk in his tent? Because the flood had not solved the human problem. This is Noah who", "study.hermeneutics.authorIntent, study.oneStory"),
        ("Q", "walked with God", "Genesis 6:9", "READER"),
        ("GUIDE", "Saved from judgment. Blessed with the words of creation. And within a few verses of the covenant, he falls into shame. The new world is not an innocent world.", "study.hermeneutics.authorIntent"),
        ("GUIDE", "God had said it before the rain had dried. He would never again destroy the earth,", "study.god, study.oneStory"),
        ("Q", "even though every inclination of his heart is evil from his youth", "Genesis 8:21", "GOD"),
        ("GUIDE", "The flood cleaned the world. It could not clean the heart.", "study.basic.oneStory"),
        ("BEAT", 2, "The dim tent. Breath."),
        ("PIC", "Remembered from The Fall: the tree in the garden, a hand closing on its fruit; the man and the woman seen from behind among the trees, holding fig leaves to themselves; then God's provision, the garments of skin lying folded on a stone."),
        ("GUIDE", "Listen to the pattern. A man of the ground plants, as God planted a garden. The fruit is taken and consumed. Nakedness is exposed. Shame follows. A garment covers it. A knowing comes afterward. And the scene ends in curse and blessing.", "study.context.literary, study.crossReferences[0]"),
        ("GUIDE", "The second father of humanity repeats the failure of the first. A new start from inside the old humanity, even one led by a righteous man, cannot make a clean world.", "study.typology[2], study.oneStory"),
        ("BEAT", 2, "The garments of skin on the stone, then the tent at night. Breath."),
        ("GUIDE", "Uncovered himself. The verb is galah, to uncover, to expose, and here its form turns back on Noah. He is the one who exposed himself.", "study.originalLanguages"),
        ("PIC", "Night. Ham (cast) coming up from the flock with a lamp, stopping at his father's tent; the flap blown half open by the wind; Ham seen only from behind in the doorway, the lamplight falling past him into the tent; nothing inside shown. Then his face, close, lit from below, staring."),
        ("V", "9:22", "9:22"),
        ("PIC", "Ham (cast) walking quickly to the fire where Shem and Japheth (cast) sit; Ham talking, his hand gesturing back toward the tent; the brothers' faces close, one after the other, changing."),
        ("GUIDE", "Nakedness. Ervah. It means more than an unclothed body. It carries shame and disgrace. And there is the narrator's second warning. Ham, the father of Canaan.", "lexicon.ervah, study.context.literary"),
        ("BEAT", 2, "The fire, the brothers silent. Breath."),
        ("GUIDE", "So what did Ham actually do? The text says only two things. He saw, and he told. Most readers through history have taken that plainly. The looking itself was the offence, and he made it worse by spreading it. In a culture of honour and shame, that was contempt for a father.", "study.hermeneutics.debates[0]"),
        ("GUIDE", "Others note that in Leviticus, seeing or uncovering nakedness is a way of speaking of a sexual act, and suggest something worse happened in that tent.", "study.hermeneutics.debates[0]"),
        ("BEAT", 2, "The tent in the dark, the flap moving in the wind. Breath."),
        ("GUIDE", "But the text says Noah uncovered himself, and the brothers put it right with a garment. That fits a sin of looking and exposing. Shameful, but no more than the words say. Either way, Ham dishonoured his father, and did it in the open.", "study.hermeneutics.debates[0].bearing"),
        ("GUIDE", "The prophet Habakkuk links wine and exposure the same way. He pronounces woe on the one who gives his neighbours drink,", "study.crossReferences[4]"),
        ("Q", "in order to gaze at their nakedness", "Habakkuk 2:15", "READER"),
        ("BEAT", 2, "Ham's face in the firelight, then turning away. Breath."),
    ]),
    ("Walking backward", [
        ("PIC", "Shem and Japheth (cast) rising from the fire without a word; Shem lifting a heavy woven cloak from a peg by the fire, both hands whole in the frame."),
        ("V", "9:23", "9:23"),
        ("BEAT", 10, "Set piece: the covering, no narration, slow, each step its own shot. The two brothers spreading the cloak between them across their shoulders; turning their backs to the tent door; walking backward step by careful step, their bare feet on the rug; their faces turned aside and close, eyes shut; the cloak lowering out of frame below their shoulders; the lamp; then the two walking out into the night without looking back. Nothing of Noah shown. A single held string note."),
        ("GUIDE", "Watch how slowly the narrator tells it. Ham saw and told. Two verbs. His brothers took the garment, placed it, walked backward, covered their father, and did not see. Almost frame by frame. Their refusal to look stands out against his looking.", "study.context.literary"),
        ("GUIDE", "Three times in two verses, the narrator names the father's nakedness. And the garment has the article in Hebrew. The garment. As if one particular cloak was at hand. They covered him without a second look.", "study.context.literary, study.originalLanguages"),
        ("BEAT", 2, "The two brothers outside the tent in the dark, saying nothing. Breath."),
        ("GUIDE", "Ham exposes. His brothers cover. Ham tells. They act without a word. It is a lesson in how to treat someone else's failure.", "study.hermeneutics.authorIntent"),
        ("PIC", "The wilderness camp at the foot of Sinai, the mountain dark with cloud behind it: the brick-maker (cast), chest up, standing among the people listening, his old father (seen from behind, bent, white haired, leaning on a staff) beside him; the brick-maker's hand under his father's arm."),
        ("GUIDE", "The brick-maker heard the weight of this at Sinai. The fifth commandment.", "study.crossReferences[5] (the brick-maker is the series' first hearer)"),
        ("Q", "Honor your father and mother", "Exodus 20:12", "GOD"),
        ("GUIDE", "Israel's law made it a capital crime to strike or curse a parent, and Moses pronounced a curse on", "study.context.historical"),
        ("Q", "he who dishonors his father or mother", "Deuteronomy 27:16", "READER"),
        ("GUIDE", "This was not only good manners. It reflects God's own order. The Son honours the Father.", "study.god"),
        ("BEAT", 2, "The brick-maker steadying his father as the people sit. Breath."),
        ("GUIDE", "What carries forward from this scene is clear. A warning against drunkenness. Paul writes,", "study.hermeneutics.descriptionVsPrescription"),
        ("Q", "Do not get drunk on wine, which leads to reckless indiscretion", "Ephesians 5:18", "READER"),
        ("GUIDE", "The command to honour parents. And the call to cover the failings of others, not to broadcast them. The New Testament puts it simply. Love covers a multitude of sins.", "study.hermeneutics.descriptionVsPrescription, study.basic.crossReferences (1 Peter 4:8, from the study's summary, not quoted as Scripture)"),
        ("BEAT", 2, "The cloak over the sleeping figure, seen only as a dark shape from the doorway. Breath."),
    ]),
    ("Cursed be Canaan", [
        ("PIC", "Morning in the tent: Noah (cast, older) waking under the heavy cloak, his face close; he sits up slowly, pulls the cloak round him, sees the cup on its side, the spilled wine dark on the rug. Then at the tent door, Shem (cast) standing with his eyes lowered."),
        ("V", "9:24", "9:25"),
        ("BEAT", 3, "Noah's face, close, very still. Silence."),
        ("GUIDE", "These are the only words Noah ever speaks in Scripture. And they are a curse and a blessing.", "study.context.literary"),
        ("GUIDE", "A servant of servants. Ebed abadim. It is the Hebrew way of saying the most. Like holy of holies, the most holy place. Servant of servants means the lowest servant of all.", "study.originalLanguages, lexicon.ebed"),
        ("BEAT", 2, "Shem at the tent door, his eyes lowered. Breath."),
        ("GUIDE", "So why is Canaan cursed, when Ham did the wrong? Some see a correspondence. A son wronged his father, so he is struck through his son. Some suggest Canaan took part, though the text does not say so.", "study.hermeneutics.debates[1]"),
        ("GUIDE", "But the best answer is in the narrator's own signals. He flagged Canaan twice. The oracle is a prophecy. It looks ahead to the Canaanites Israel would meet, a people whose conduct would come to match their forefather's sin.", "study.hermeneutics.debates[1].bearing"),
        ("BEAT", 2, "The boy Canaan, seen from behind, asleep by the fire's ashes. Breath."),
        ("PIC", "The wilderness camp on the plains across the Jordan at evening: the brick-maker (cast), chest up, looking west across the river to the hills of Canaan, his wife and sons beside him seen from behind."),
        ("GUIDE", "For the brick-maker, Canaan was not an idea. It was the land across the river. God warned Israel that its peoples had defiled the land, and that Israel held no immunity. If they copied Canaan, the land would cast them out too.", "study.crossReferences[2], study.context.historical (the brick-maker is the series' first hearer)"),
        ("GUIDE", "And the judgment did not come in haste. God told Abram", "study.crossReferences[3]"),
        ("Q", "the iniquity of the Amorites is not yet complete", "Genesis 15:16", "GOD"),
        ("GUIDE", "The curse waited for centuries, until their own sin had filled up. Scripture insists that each person answers for their own sin.", "study.crossReferences[3], study.hermeneutics.debates[1].bearing, study.god"),
        ("PIC", "Gibeon, later: men of a Canaanite town carrying bundles of wood and water jars up a stony path toward the camp of Israel, seen from behind."),
        ("GUIDE", "Israel's first hearers saw the oracle at work in their own history. Canaanite towns were put to forced labour. The Gibeonites became", "study.context.historical"),
        ("Q", "woodcutters and water carriers", "Joshua 9:23", "READER"),
        ("BEAT", 2, "The water carriers on the path. Breath."),
    ]),
    ("A lie about Ham", [
        ("PIC", "A dim study by candlelight: a heavy old book lying open, a quill beside it; then a pair of iron shackles lying open and empty on weathered planks by the sea, the light cold."),
        ("GUIDE", "Now the fourth question. For centuries, some claimed a curse of Ham to justify the enslavement of Africans. It is one of the worst misuses of the Bible in history.", "study.hermeneutics.descriptionVsPrescription"),
        ("BEAT", 2, "The empty shackles. Silence."),
        ("GUIDE", "And the text gives it no ground. Read it again. Ham is not cursed. Canaan is. The Canaanites lived in the land between Egypt and Syria. And the sons of Ham usually linked with Africa, Cush, Mizraim and Put, are not cursed at all.", "study.hermeneutics.descriptionVsPrescription"),
        ("PIC", "Graphic, gold on dark stone: three names, SHEM, HAM, JAPHETH; under HAM four names branch out, CUSH, MIZRAIM, PUT, CANAAN; only CANAAN is marked, and the line under it runs on into the land between the river of Egypt and the hills of Syria on a faint map."),
        ("GUIDE", "Noah's words are a prophecy of what would come of these lines. They are not a command to anyone to enslave anyone. And servant of servants is not a comment on the worth of any people before God.", "study.hermeneutics.descriptionVsPrescription, study.translationNotes[1]"),
        ("GUIDE", "Any reading that turns this oracle into a ranking of races abuses the text. Shem, Ham and Japheth were brothers. One family. And every nation on earth comes from them.", "study.hermeneutics.descriptionVsPrescription, study.oneStory"),
        ("BEAT", 3, "Faces, close, one after another, all of one family: Shem, Ham, Japheth, their wives. No music."),
    ]),
    ("The God of Shem", [
        ("PIC", "Outside the tent in the morning: Noah (cast, older) standing, the cloak round his shoulders, Shem and Japheth (cast) before him with their heads bowed, Noah's hand on Shem's head; Noah's face close as he speaks."),
        ("V", "9:26", "9:27"),
        ("BEAT", 2, "Noah's hand lifting from Shem's head. The wind. Breath."),
        ("GUIDE", "Listen to what Noah blesses. Not Shem. Blessed be the LORD, the God of Shem. Barak. To speak good over someone. The blessing lies in whom Shem has as his God.", "lexicon.barak, study.originalLanguages"),
        ("GUIDE", "And this is the only place in the oracle where the covenant name appears. The LORD. It is joined to Shem. For Japheth, Noah says simply, God.", "study.originalLanguages"),
        ("GUIDE", "Shem means name. In two chapters, the builders of Babel will say, let us", "study.context.canonical, study.originalLanguages"),
        ("Q", "make a name for ourselves", "Genesis 11:4", "READER"),
        ("GUIDE", "And God will say to Abram, Shem's descendant,", "study.context.canonical, study.crossReferences[6]"),
        ("Q", "I will make your name great", "Genesis 12:2", "GOD"),
        ("GUIDE", "The blessing of the God of Shem becomes the blessing of the God of Abraham.", "study.context.canonical"),
        ("BEAT", 2, "Shem's face, close, lifting. Breath."),
        ("PIC", "Japheth (cast) standing on a ridge at dawn looking out over a vast land of hills and far coasts; then the same dawn on the camp below, the tents of Shem in a row, smoke rising."),
        ("GUIDE", "Then Japheth. May God expand. In Hebrew, yapht. It sounds like his name, yepheth. Both names carry their future. Japheth will be enlarged. Shem will bear the name of God.", "study.originalLanguages"),
        ("GUIDE", "But who will dwell in the tents of Shem? Some read it as God Himself, making His presence live among Shem's descendants. Most translations read it as Japheth, coming to share in Shem's blessing.", "study.hermeneutics.debates[2]"),
        ("GUIDE", "The two are not far apart. If God dwells in Shem's tents, and Japheth comes to live there, both point to one hope. The nations joining the people among whom God has chosen to live.", "study.hermeneutics.debates[2].bearing"),
        ("BEAT", 2, "Japheth walking down toward the tents. Breath."),
    ]),
    ("And then he died", [
        ("PIC", "Many years on: the vineyard terraces spread wide across the mountainside, the camp grown into a settlement of tents and stone pens; children and grandchildren among the vines, seen from behind; Noah (cast, older), his hair white, sitting at his tent door watching them, his face close."),
        ("V", "9:28", "9:29"),
        ("BEAT", 4, "A lamp burning low inside the tent, then out. Noah's three sons (cast), now grey, standing at a cairn of stones on the slope, seen from behind. The wind. Silence."),
        ("GUIDE", "Nine hundred and fifty years. And then he died. It is the refrain of Genesis five. Adam lived, and then he died. Noah's entry in that list began before the flood and was left open through the whole flood story. Now it is closed. The man who came through the waters still goes the way of Adam.", "study.context.literary"),
        ("GUIDE", "And notice what God does not do. The family He rescued fell into sin almost at once. And He sent no flood. His covenant faithfulness does not depend on ours.", "study.god"),
        ("BEAT", 2, "The cairn on the slope, the vineyard below. Breath."),
        ("BEAT", 8, "Set piece: the three sons go out, no narration. Each its own shot from the mountainside: Japheth's family with their flocks walking north and west along a ridge toward far coasts; Ham's family going south down a valley toward the river plains, the boy Canaan, grown now, walking among them; Shem's family staying among the tents of the highlands, smoke rising. All seen from behind. A wide, rising theme."),
        ("GUIDE", "God is sovereign over history. The oracle was spoken by a man who had failed, and it came to pass. God works through broken families to steer history toward His purpose.", "study.god"),
        ("BEAT", 2, "The three families small in the wide land. Breath."),
    ]),
    ("The faithful Son (Christ)", [
        ("PIC", "Remembered from The Fall and from the vineyard: the hand on the fruit; the cup on its side in the tent. Then a road in Galilee at dusk, a man in a seamless robe seen only from straight behind, His warm olive brown skin and thick black curly hair, walking alone; no part of His face shown."),
        ("GUIDE", "Noah was set up as a second Adam. The father of a new humanity, blessed with Adam's words, a man of the ground. And like Adam, he fell. A new humanity needs a new head. Paul calls Christ", "study.typology[2], study.christ"),
        ("Q", "the last Adam", "1 Corinthians 15:45", "READER"),
        ("GUIDE", "Where Noah failed, and a son shamed his father, here is the faithful Son. Jesus said of His Father,", "study.christ, study.basic.christ"),
        ("Q", "I always do what pleases Him", "John 8:29", "READER"),
        ("BEAT", 2, "The figure on the road at dusk. Breath."),
        ("PIC", "The hill outside the city under a dark sky: at the foot of the three posts, far off, no figures; close on soldiers' hands on the ground casting lots over a seamless robe spread on the stones."),
        ("GUIDE", "Ham exposed his father's shame. Shem and Japheth covered it without looking. Christ went further than either. He did not look away from our shame. He took it on Himself. At the cross He was stripped, and soldiers divided His garments. He endured the cross,", "study.christ, study.typology[0]"),
        ("Q", "scorning its shame", "Hebrews 12:2", "READER"),
        ("GUIDE", "so that the naked might be clothed. Paul writes,", "study.typology[0]"),
        ("Q", "all of you who were baptized into Christ have clothed yourselves with Christ", "Galatians 3:27", "READER"),
        ("BEAT", 2, "The robe on the stones. Breath."),
        ("PIC", "A long scroll unrolling on a table by lamplight, a column of names in faint ink; then the hills of Judah at night, a small town below with a few lamps lit."),
        ("GUIDE", "And the blessing on the God of Shem runs on. Shem's line goes to Abram, to Israel, to David. Luke traces Jesus back to", "study.typology[1], study.crossReferences[7]"),
        ("Q", "the son of Shem, the son of Noah", "Luke 3:36", "READER"),
        ("GUIDE", "The blessing announced in a tent after the flood reaches its goal in the one born in Bethlehem. And the tents? John says", "study.christ"),
        ("Q", "The Word became flesh and made His dwelling among us", "John 1:14", "READER"),
        ("GUIDE", "A word that recalls pitching a tent. And the Gentiles, the far nations, are brought in. Paul calls them", "study.christ"),
        ("Q", "no longer strangers and foreigners, but fellow citizens with the saints", "Ephesians 2:19", "READER"),
        ("BEAT", 2, "The lamps of the town. Breath."),
        ("PIC", "A woman of Canaan, her head covered, kneeling on a dusty road, seen from behind; the hem of a seamless robe and a man's sandalled feet stopping before her."),
        ("GUIDE", "And the curse? Christ", "study.christ"),
        ("Q", "redeemed us from the curse of the law by becoming a curse for us", "Galatians 3:13", "READER"),
        ("GUIDE", "In Christ there is no permanent class of the cursed. Rahab of Jericho, a Canaanite, was saved and became an ancestor of Christ. And a Canaanite woman once begged Jesus for her daughter. He praised her great faith and granted what she asked. Mercy, from the son of Shem, to the line of Canaan.", "study.god, study.christ"),
        ("BEAT", 2, "The woman lifting her head. Breath."),
        ("GUIDE", "One care. The vineyard and the wine are not hidden pictures of the Lord's Supper. The links rest on the New Testament's own themes. The last Adam. The bearing of shame. The blessing of the nations.", "study.christ"),
        ("PIC", "High bright light and a great crowd seen from behind, dressed in white, of every nation, filling the frame; no throne and no figure above them."),
        ("GUIDE", "At the end of the story, the people of God are dressed in white. The nations that came from Shem, Ham and Japheth are one family before the throne. And the curse that began with the ground is lifted.", "study.oneStory"),
        ("Q", "No longer will there be any curse", "Revelation 22:3", "READER"),
        ("BEAT", 3, "The crowd in white, the light growing. The warm chord. No narration."),
    ]),
    ("The cloak at evening", [
        ("PIC", "Evening in the wilderness camp: the brick-maker (cast), chest up, coming into his tent; his old father asleep on a mat, seen from behind; the brick-maker lifting his own cloak from his shoulders, both hands whole in the frame, and laying it gently over his father; his face close, tender."),
        ("GUIDE", "The brick-maker's father was old, and he had failed in his time, like every father. The story of Noah's sons taught Israel what kind of people to be. People who honour father and mother. People who cover shame instead of spreading it.", "study.hermeneutics.authorIntent (the brick-maker is the series' first hearer)"),
        ("BEAT", 2, "The cloak settling over the sleeping father. Soft."),
        ("GUIDE", "Ham exposed his father's shame. His brothers covered it. When you learn something embarrassing about someone, which brother are you more like?", "questions[1]"),
        ("BEAT", 3, "The brick-maker sitting down beside his father in the lamplight. The camp quiet outside."),
        ("PIC", "The mountainside in Ararat at dawn, empty: the old vineyard gone wild on the terraces; three paths leading away from it, north, south and east, into a vast land."),
        ("GUIDE", "Three sons. Three paths across the earth. Next, Genesis names their children, nation by nation. And every one of them is family.", "study.oneStory (series link to The Table of Nations, Genesis 10)"),
        ("BEAT", 4, "The three paths in the dawn light, the wind over the terraces. Then quiet."),
        ("CARD", "Study Noah's Sons / makor.co.za/genesis/noahs-sons"),
        ("BEAT", 6, "End card with a WATCH NEXT space for The Table of Nations."),
    ]),
]

HEADER = """# Noah's Sons: full movement film script

Genesis 9:18 to 29, built to films/CINEMA-STANDARD.md like The Waters Recede and The Covenant with Noah. Generated
by `script/movement.py`; edit that file, not this one. Treatment and storyboard plan: `../TREATMENT.md`.

Runtime: **{total}** ({basis}). All {n} verses appear once, in order, verbatim BSB from the
study JSON (checked by the generator). Words: {words}.

## Voices

READER for Scripture, including Noah's oracle (9:25 to 27), the only words Noah speaks: a human speaker, kept with
the READER in `SPEAKERS`. Nothing in the passage is God's speech. As proposed in the treatment (D6), the GOD voice
reads five words of God quoted from elsewhere: Genesis 11:6, 8:21, 15:16 and 12:2, and Exodus
20:12. Words of Jesus are READER quotations. GUIDE for everything else.

## Chapters

```
{chapters}
```
"""

if __name__ == "__main__":
    Film(HERE, STUDY, VOICE_MAP, SPEAKERS).build(CHAPTERS, HEADER)
