#!/usr/bin/env python3
"""Full movement film script: The Seven Days (Genesis 1:1 to 2:3), YouTube epic.

Writes script/movement-script.md. Scripture is never typed here: every verse is
pulled from the study JSON and split into READER and GOD lines automatically
(God's direct speech after "said," goes to GOD; everything else to READER).
GUIDE lines are Makor's own words, each tagged with the study field it comes
from. Quotations of other Scripture are READER lines and must appear verbatim in
the study JSON or the build stops.

    python3 films/genesis/01-the-seven-days/script/movement.py
"""
import json, pathlib, re, sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[3]
STUDY = REPO / "src/content/studies/genesis/01-the-seven-days.json"
OUT = HERE / "movement-script.md"
WPM = {"READER": 185, "GOD": 140, "GUIDE": 155}   # measured from the Day One renders
GAP = 0.6                                          # breath after every line

D = json.loads(STUDY.read_text())
STUDY_TEXT = json.dumps(D, ensure_ascii=False)
PLAIN = lambda t: re.sub(r"\{\{[^|}]+\|([^}]+)\}\}", r"\1", t)
VERSES = [(f"{v['chapter']}:{v['n']}", PLAIN(v["text"])) for u in D["text"]["units"] for v in u["verses"]]
VMAP = dict(VERSES)

# ------------------------------------------------------------------ beats
# ("V", "1:3", "1:5")          verses, split into READER and GOD
# ("GUIDE", text, source)      Makor's words, from the named study field
# ("Q", text, ref, speaker)    quotation of other Scripture, verbatim from the study JSON
# ("PIC", text)                what is on screen
# ("BEAT", seconds, text)      music or silence with no voice
# ("CARD", text)               on screen text

CHAPTERS = [
    ("Cold open", [
        ("PIC", "Black. One low note. The faintest dark swell of water surfaces out of the black (Day One pilot, shots 1 to 3)."),
        ("V", "1:1", "1:2"),
        ("BEAT", 3, "Wind over the deep. Hold."),
        ("GUIDE", "Every other part of the Bible's story is set inside the world this passage describes.", "study.oneStory"),
        ("GUIDE", "Before there is a fall, a covenant, a nation or a cross, there is a Creator, a good world, and a human race made in His image.", "study.oneStory"),
        ("CARD", "THE SEVEN DAYS / Genesis 1:1 to 2:3"),
        ("BEAT", 4, "Title holds over the dark water. Music opens."),
    ]),
    ("A world of other stories", [
        ("PIC", "The Nile at dawn under a blazing sun; brick kilns and stacked mud bricks in Egypt; a clay tablet pressed with wedge script; a dark sea under storm. Objects and landscapes only, no depictions of the nations' gods."),
        ("GUIDE", "Israel first heard these words as the opening of the Torah, given through Moses to a people who had spent generations in Egypt.", "study.context.historical"),
        ("GUIDE", "Their neighbours all told their own stories of how the world began.", "study.context.historical"),
        ("GUIDE", "In Babylon, the god Marduk defeats the sea goddess Tiamat and splits her body to form sky and earth. Human beings are made to carry the labour of the gods, so that the gods may rest.", "study.context.historical"),
        ("GUIDE", "In Egypt, the sun was worshipped as a god, and Pharaoh was presented as a son of the sun.", "study.context.historical"),
        ("GUIDE", "Genesis speaks into that world with deliberate restraint. There is no battle. The deep is simply there, and the Spirit of God is over it.", "study.context.historical"),
        ("GUIDE", "Moses wanted Israel to know who their God was before they learned anything else about Him. Not one god among many, but the Maker of the sun that Egypt worshipped, the sea that the nations feared, and the land they were about to enter.", "study.hermeneutics.authorIntent"),
    ]),
    ("Formless and void", [
        ("PIC", "Back to the dark deep. Then a painted two panel frame builds on screen: three realms on the left, their three fillings on the right, the seventh day standing apart above both."),
        ("GUIDE", "Verse two names the problem. The earth was formless and void. In Hebrew, tohu wabohu.", "study.originalLanguages"),
        ("GUIDE", "Not a description of evil, but of a world not yet shaped and not yet filled. And the six days answer both words in turn.", "study.originalLanguages"),
        ("GUIDE", "Days one to three give shape to the formless: light from darkness, the waters above from the waters below, the sea from the dry land.", "study.context.literary"),
        ("GUIDE", "Days four to six fill the void: lights for the light, birds and fish for the sky and sea, animals and people for the land.", "study.context.literary"),
        ("GUIDE", "And the seventh day stands apart, as the goal.", "section.frameNote"),
        ("GUIDE", "Over the deep, the Spirit of God is hovering, the same word used of an eagle over its young. Attentively near, poised to bring life.", "lexicon.hover"),
        ("GUIDE", "Listen for the refrains. And God said. Let there be. And it was so. God saw that it was good. There was evening, and there was morning. The repetition gives the chapter the cadence of worship, and the variations carry the meaning.", "study.context.literary"),
    ]),
    ("Day One: light", [
        ("PIC", "Day One pilot, shots 4 to 8: the word over darkness, light breaking across the deep, day beside night, evening and morning."),
        ("V", "1:3", "1:5"),
        ("BEAT", 2, "Light settles on the water."),
        ("GUIDE", "Light on the first day, before the sun on the fourth. The point is theological before it is astronomical: light comes from God.", "lexicon.light"),
        ("GUIDE", "Ten times God speaks in this chapter, and each word does what it says. There is no struggle and no strain.", "study.god"),
        ("Q", "He spoke, and it came to be; He commanded, and it stood firm,", "Psalm 33:9", "READER"),
    ]),
    ("Day Two: the sky", [
        ("PIC", "Waters rise and part; a vast clear expanse opens between the waters below and the waters above, like a sheet of beaten gold stretched thin. No sun, moon or stars yet."),
        ("V", "1:6", "1:8"),
        ("GUIDE", "The expanse is raqia, from a verb meaning to spread or beat out, used of hammering gold into thin sheets. The sky is pictured as something God has stretched out over the world, like a craftsman's work.", "study.originalLanguages"),
        ("GUIDE", "Day two is the one day the chapter does not close with God's approval. Day three will hear it twice.", "study.context.literary"),
    ]),
    ("Day Three: land, sea and green", [
        ("PIC", "The sea draws back and dry land rises; then the land greens: grasses, seed bearing plants, fruit trees spreading across the hills. Still no sun disc, no creatures."),
        ("V", "1:9", "1:13"),
        ("GUIDE", "Now the three realms stand ready: the light, the sky and the sea, and the dry land. The formless has been given shape.", "study.context.literary"),
        ("GUIDE", "But it is still empty.", "study.context.literary"),
        ("BEAT", 3, "Wide, empty, green world. Music turns toward the second panel."),
    ]),
    ("Day Four: the lights", [
        ("PIC", "The first sunrise: a great light lifts over the sea; then a pale moon and a field of stars over the new land. The lights read as lamps hung in the sky, not as faces or figures."),
        ("V", "1:14", "1:19"),
        ("GUIDE", "Notice what is not said. The sun and moon are not even named. To Egypt the sun was a god. Here they are the greater light and the lesser light, lamps hung in the sky with a job to do, and the stars are mentioned almost in passing.", "study.context.historical"),
        ("GUIDE", "The word for these lights elsewhere names the light of the tabernacle lampstand, and the seasons they mark is the word for Israel's appointed feasts. They are lamps in God's house that keep His calendar.", "study.originalLanguages"),
    ]),
    ("Day Five: sea and sky", [
        ("PIC", "The sea teems: shoals turning in the light, great whales rising and sounding; flocks lift over the water into the open sky."),
        ("V", "1:20", "1:23"),
        ("GUIDE", "The great sea creatures, a word that elsewhere names the monsters of the sea, are simply creatures God made and blessed.", "study.context.historical"),
        ("GUIDE", "And for the first time, God blesses. The whole account moves from emptiness to fullness, because God gives.", "study.god"),
    ]),
    ("Day Six: the image of God", [
        ("PIC", "Herds across the plains, creatures in the grass. Then the music thins and the picture stills before verse 26."),
        ("V", "1:24", "1:25"),
        ("GUIDE", "Then the pattern breaks. God does not simply say, let there be. He deliberates.", "study.context.literary"),
        ("V", "1:26", "1:26"),
        ("PIC", "A man and a woman in the new world at first light, painted at a distance."),
        ("V", "1:27", "1:27"),
        ("GUIDE", "Three lines of poetry, and the word created sounds three times.", "study.context.literary"),
        ("GUIDE", "Image, tselem, is the word used for a carved image, the kind Israel was told to destroy in Canaan. In a world full of idols, God places His own living image on the earth.", "study.originalLanguages"),
        ("GUIDE", "Remember who first heard this. Slaves who had been treated as tools in Pharaoh's building projects are told that every human being, male and female, is made in the image of God and blessed with a royal calling.", "study.hermeneutics.authorIntent"),
        ("V", "1:28", "1:28"),
        ("GUIDE", "Humanity is not made to feed the gods. God feeds humanity.", "study.context.historical"),
        ("V", "1:29", "1:31"),
        ("GUIDE", "Seven times God looks and calls it good. The last time, very good. The goodness of the world is not a human judgment, but His.", "study.god"),
    ]),
    ("Day Seven: rest", [
        ("PIC", "The whole world at peace in long golden light: sea, sky, land, creatures, all still. Nothing is made. Nothing moves but light and breath."),
        ("GUIDE", "Then the pattern breaks altogether.", "study.context.literary"),
        ("V", "2:1", "2:3"),
        ("BEAT", 3, "Silence but for the room tone of a finished world."),
        ("GUIDE", "There is no speech. No it was good. No evening and morning. And the Hebrew names the seventh day three times in two verses.", "study.context.literary"),
        ("GUIDE", "God does not rest because He is tired. He rests because the work is finished, and good.", "study.god"),
        ("GUIDE", "Then He blesses a day and sanctifies it, the first thing in the Bible to be made holy. Time itself belongs to Him.", "study.god"),
        ("GUIDE", "Israel would hear an echo. The tabernacle account ends the same way, with the work completed, inspected and blessed. The world is the house God built for Himself, and the tabernacle is a small copy of it in the middle of the camp.", "study.context.historical"),
    ]),
    ("How long were the days?", [
        ("PIC", "A slow sequence of evenings and mornings over the same calm sea; the painted two panel frame returns."),
        ("GUIDE", "People ask how long these days were. Christians who hold the full truth of Scripture have answered in different ways: ordinary days, long ages, or a framework that sets out God's work like a working week.", "study.hermeneutics.debates[0]"),
        ("GUIDE", "Israel's own week was patterned on this one.", "study.crossReferences (Exodus 20:8-11)"),
        ("Q", "For in six days the LORD made the heavens and the earth.", "Exodus 20:11", "READER"),
        ("GUIDE", "But the passage itself presses a different question. Not how long God took, but who He is, and whose the world is.", "study.hermeneutics.debates[0].bearing"),
    ]),
    ("In the beginning was the Word", [
        ("PIC", "Light only: a single point of light in darkness widening into dawn; then the stone rolled back from an empty tomb at first light, with no figures. Never a face of Christ."),
        ("GUIDE", "The New Testament does not treat Christ as a latecomer to this story. It places Him at its beginning.", "study.christ"),
        ("Q", "In the beginning was the Word,", "John 1:1", "READER"),
        ("Q", "Through Him all things were made, and without Him nothing was made that has been made,", "John 1:3", "READER"),
        ("GUIDE", "Genesis shows God creating by speaking. John tells us that the Speech itself is a person, and that He became flesh.", "study.christ"),
        ("Q", "The Light shines in the darkness, and the darkness has not overcome it.", "John 1:5", "READER"),
        ("GUIDE", "Paul reaches straight for day one to describe what happens when God brings a person to new birth.", "study.typology[3]"),
        ("Q", "Let light shine out of darkness,", "2 Corinthians 4:6", "READER"),
        ("GUIDE", "The first creation climbed toward a seventh day. Jesus lies in the tomb through the Sabbath, and rises on the first day of the week. The new creation begins on the first day of a new week.", "study.christ"),
        ("GUIDE", "Humanity was made to be God's image. Christ is the image of the invisible God, the true Man in whom the human calling is finally carried out.", "study.typology[1]"),
        ("GUIDE", "And the rest of the seventh day, He offers in person.", "study.typology[0]"),
        ("Q", "Come to Me, all you who are weary and burdened, and I will give you rest,", "Matthew 11:28", "READER"),
    ]),
    ("The first page and the last", [
        ("PIC", "The flood: the deep returning over the land, creation undone; then a long walk of light through the ages; finally a radiant new world with no sun in the sky and no sea."),
        ("GUIDE", "This page sets the standard for everything after it. Chapter three is a tragedy because chapter one was very good. Death, violence and exile are wrong because they were not part of the world God made.", "study.oneStory"),
        ("GUIDE", "In the flood, the waters of the deep return over the land, a creation undone.", "study.oneStory"),
        ("GUIDE", "The seventh day has no evening. God's rest is the goal of creation, and the rest of Scripture is a long journey toward entering it.", "study.oneStory"),
        ("Q", "There remains, then, a Sabbath rest for the people of God.", "Hebrews 4:9", "READER"),
        ("GUIDE", "And the last pages of the Bible deliberately echo the first. A new heaven and a new earth. A city that has no need of sun or moon, for the glory of God is its light. The sea is no more.", "study.oneStory"),
        ("Q", "Behold, I make all things new.", "Revelation 21:5", "GOD"),
        ("GUIDE", "The story that began with, In the beginning God, ends with God dwelling among His people in a world made new.", "study.oneStory"),
    ]),
    ("Light in a dark place", [
        ("PIC", "Return to the first image: the dark deep, and light breaking across it once more."),
        ("GUIDE", "On the first day God said, let there be light, before the sun existed, because light comes from Him.", "questions[4]"),
        ("GUIDE", "Where do you need to ask God to speak light into a dark place?", "questions[4]"),
        ("BEAT", 4, "Hold on the light. Music resolves."),
        ("CARD", "Study The Seven Days / makor.co.za/genesis/the-seven-days"),
        ("BEAT", 4, "End card."),
    ]),
]

# ------------------------------------------------------------------ split verses
SAID = re.compile(r"(said|said to them),\s*$")


def split_range(a, b, state):
    keys = [k for k, _ in VERSES]
    out = []
    for key in keys[keys.index(a): keys.index(b) + 1]:
        text, segs, i = VMAP[key], [], 0
        if state["god"]:   # a God speech carried over from the previous verse
            j = text.find("”")
            segs.append(("GOD", text[: j + 1].strip())); i = j + 1; state["god"] = False
        while i < len(text):
            j = text.find("“", i)
            if j < 0:
                segs.append(("READER", text[i:].strip())); break
            before = text[i:j]
            k = text.find("”", j)
            god = bool(SAID.search(before)) or (not before.strip() and segs and segs[-1][0] == "READER"
                                                and SAID.search(segs[-1][1]))
            if god:
                if before.strip():
                    segs.append(("READER", before.strip()))
                if k < 0:
                    segs.append(("GOD", text[j:].strip())); state["god"] = True; i = len(text)
                else:
                    segs.append(("GOD", text[j: k + 1].strip())); i = k + 1
            else:   # a quoted name such as “day,” stays with the READER
                end = k + 1 if k >= 0 else len(text)
                nxt = text.find("“", end)
                stop = nxt if nxt >= 0 else len(text)
                # keep READER text together up to the next quote that might be speech
                segs.append(("READER", text[i:stop].strip())); i = stop
        segs = [s for s in segs if s[1]]
        merged = []
        for sp, t in segs:   # join neighbouring READER pieces
            if merged and merged[-1][0] == sp == "READER":
                merged[-1] = (sp, merged[-1][1] + " " + t)
            else:
                merged.append((sp, t))
        assert " ".join(t for _, t in merged) == text, f"split changed {key}: {merged}"
        out.append((key, merged))
    return out


# ------------------------------------------------------------------ render
def secs(speaker, text):
    words = len(re.findall(r"[\w']+", text))
    return words / WPM[speaker] * 60 + GAP


def tc(s):
    return f"{int(s // 60)}:{int(s % 60):02d}"


def main():
    state, t, used, lines, chapters = {"god": False}, 0.0, [], [], []
    words = {"READER": 0, "GOD": 0, "GUIDE": 0}
    body = []
    for title, beats in CHAPTERS:
        chapters.append((t, title))
        body.append(f"\n## {tc(t)}  {title}\n")
        for b in beats:
            kind = b[0]
            if kind == "PIC":
                body.append(f"*Picture:* {b[1]}\n")
            elif kind == "BEAT":
                body.append(f"*{b[1]} s, no voice:* {b[2]}\n"); t += b[1]
            elif kind == "CARD":
                body.append(f"`ON SCREEN` {b[1]}\n"); t += 0
            elif kind == "GUIDE":
                body.append(f"**GUIDE** {b[1]}  <sub>[{b[2]}]</sub>\n")
                t += secs("GUIDE", b[1]); words["GUIDE"] += len(b[1].split())
            elif kind == "Q":
                assert b[1] in STUDY_TEXT, f"quotation not verbatim in study JSON: {b[1]}"
                body.append(f"**{b[3]}** {b[1]}  <sub>({b[2]}, quoted verbatim from the study)</sub>\n")
                t += secs(b[3], b[1]); words[b[3]] += len(b[1].split())
            elif kind == "V":
                for key, segs in split_range(b[1], b[2], state):
                    used.append(key)
                    body.append(f"<sub>Genesis {key}</sub>  " + "  ".join(f"**{sp}** {tx}" for sp, tx in segs) + "\n")
                    for sp, tx in segs:
                        t += secs(sp, tx); words[sp] += len(tx.split())
    allkeys = [k for k, _ in VERSES]
    assert used == allkeys, f"verses missing, repeated or out of order: {set(allkeys) ^ set(used)}"
    text = "".join(body)
    for bad in ["–", "—"]:
        assert bad not in text, "dash found"
    head = HEADER.format(total=tc(t), n=len(allkeys), r=words["READER"], g=words["GOD"], gu=words["GUIDE"],
                         chapters="\n".join(f"{tc(s)} {name}" for s, name in chapters))
    OUT.write_text(head + text + FOOTER)
    print(f"wrote {OUT.relative_to(REPO)}: {len(allkeys)} verses verified, est. runtime {tc(t)}, "
          f"words READER {words['READER']}, GOD {words['GOD']}, GUIDE {words['GUIDE']}")


HEADER = """# The Seven Days: full movement film script

Genesis 1:1 to 2:3. One film for YouTube, built as an epic, structured on the
Makor study. Generated by `script/movement.py`; edit that file, not this one.

Estimated runtime: **{total}** before music beats are stretched in the edit.
All {n} verses of the movement appear once, in order, verbatim BSB from the
study JSON (checked by the generator). Words: READER {r}, GOD {g}, GUIDE {gu}.

## Voices

| Voice  | Speaks | Voice id |
|--------|--------|----------|
| READER | Every word of Scripture except God's direct speech, including quotations of other Scripture | ElevenLabs `pRrdgJxlE0SsVTIYEjli` (pilot narrator) |
| GOD    | God's direct speech in the passage, verbatim, nothing else | ElevenLabs `bItqJOjNBHK6rbwcdlOT` |
| GUIDE  | Makor's own words: every line that is not Scripture | Kokoro `am_michael`, the voice that already reads every study on the site |

Rule: if it is not Scripture, the GUIDE says it. If it is Scripture, the READER
says it, unless God is speaking within Genesis 1. Each GUIDE line carries the
study field it comes from, so every claim can be traced to the study.

## Decisions (agreed 5 October 2026)

1. GUIDE voice: Kokoro `am_michael`.
2. People on Day Six: painted at a distance in first light, seen from behind or in profile, faces not detailed, partly framed by landscape (style bible, People).
3. GOD voice: God's speech in Genesis 1 plus Revelation 21:5 only. Words of Jesus are read by the READER as quotation.
4. Christ chapter: light, then the stone rolled back from an empty tomb at first light, no figures.
5. Egypt and Babylon: objects and landscapes only, never their gods.
6. The Day One short is Scripture only: its two GUIDE lines come out (day-01-v2).

## YouTube chapters

```
{chapters}
```
"""

FOOTER = """

## How the shorts come out of this film

- **Seven Scripture only shorts**, one per day, each 30 to 60 seconds: that
  day's verses only, READER and GOD, cut from this film's footage and voice
  tracks, with captions and the study link. No GUIDE lines.
- **The Seven Days in a minute**: one GUIDE led short that explains the whole
  movement, using the frame (formless and void answered in two sets of three
  days, the seventh as the goal) and closing on the study link.
- Producing the full film first means every short reuses finished shots and
  voices instead of being made separately.
"""

if __name__ == "__main__":
    main()
