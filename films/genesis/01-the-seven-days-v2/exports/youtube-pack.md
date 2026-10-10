# The Seven Days (v2, the pilot): YouTube publishing pack

File: `exports/the-seven-days-v2-youtube.mp4` (1920x1080, 24 fps, 15:26: the film 15:06 plus a 20 s end
screen; -14 LUFS for YouTube). Captions: `exports/the-seven-days-v2-youtube.srt` (every spoken line, timed to
this file). Built by `edit/youtube_cut.py` from `exports/full-cut-v2.mp4`.

This replaces the painted v1 on the channel. Plan agreed earlier (D-list in V2-TREATMENT.md): upload v2, then
unlist v1 a week later so its views and comments are not lost at once.

## Title (from the vidIQ research, `vidiq-research.md`)

Recommended (keep while the thumbnail test runs):

    Genesis 1 Like You've Never Seen It: The 7 Days of Creation

Alternates, paired with the thumbnails below:

    The 7 Days of Creation: What Genesis 1 Told a Nation of Slaves
    Light Before the Sun? Genesis 1 and the 7 Days of Creation

No "| Makor" in the title: it lowered vidIQ's score every time and YouTube shows the channel under the video.
Primary keyword "genesis 1" (about 32,900 searches a month, competition 42); "genesis chapter 1" is the
easiest win (competition 18); "book of genesis" is rising (up 142%).

## Thumbnails (Test & Compare, all three; from the vidIQ research)

Made by `exports/art/concepts/make_concepts_research.py --final` (3840x2160, under 1.4 MB each).

| File | Thumbnail | Paired title |
|---|---|---|
| `exports/art/thumbnail-r1.jpg` | MADE IN GOD'S IMAGE, Genesis 1:27, the brick-maker's face by the kiln (the research's pick to win: one large face, few gold words) | The 7 Days of Creation: What Genesis 1 Told a Nation of Slaves |
| `exports/art/thumbnail-r2.jpg` | WHERE'S THE SUN?, Day One, Genesis 1:3, gold light racing across the black deep | Light Before the Sun? Genesis 1 and the 7 Days of Creation |
| `exports/art/thumbnail-r3.jpg` | GENESIS 1, The Seven Days, the earth from space (movie poster style) | Genesis 1 Like You've Never Seen It: The 7 Days of Creation |

The earlier drafts (`thumbnail-v2-light`, `-slave`, `-beginning`) stay as spares.

## Description

    Genesis 1 like you've never seen it: the 7 days of creation read in full (Genesis 1:1 to 2:3), filmed day by day, and what it meant to a nation of slaves coming out of Egypt.
    Why is there light before the sun? Why does the seventh day have no evening? Study it free: https://www.makor.co.za/genesis/the-seven-days/

    A slave in the brick pits of Egypt hears the first page of the Bible for the first time. Every nation had a
    story of how the world began; in Babylon's, people were made to carry the labour of the gods. Then came this
    one. This film reads Genesis 1:1 to 2:3 in full, day by day, and shows what it meant to its first hearers,
    how its days of forming and filling answer "formless and void", why the seventh day has no evening, and how
    the New Testament reads it in Christ.

    Made with AI tools; Scripture from the Berean Standard Bible.

    Chapters
    0:00 The Seven Days
    0:47 A world of other stories
    1:41 Day One: In the beginning
    2:36 Formless and void
    3:38 Days Two and Three: The world takes shape
    5:19 Day Four: The first sunrise
    6:36 Day Five: The sea teems
    7:43 Day Six: Living creatures
    8:24 Day Six: The image of God
    10:59 Day Seven: Rest
    12:17 In the beginning was the Word
    13:42 All things new
    14:32 Light in a dark place
    15:05 Watch next: The Garden

    Makor walks through the Bible one movement at a time: the text, its world, and its place in the one story
    that leads to Christ. Genesis, episode 1.

## Tags (422 characters, from the keyword research)

    genesis 1, the 7 days of creation, seven days of creation, genesis chapter 1, creation story,
    in the beginning, let there be light, genesis creation, book of genesis, genesis explained,
    genesis 1 explained, genesis 1 bible study, genesis bible study, bible study, creation of the
    world, how god created the world, light before the sun, image of god, sabbath, cinematic bible,
    bible movie, bible story, old testament, makor

## Pinned comment

    On Day One there is light, but the sun does not appear until Day Four, and Genesis 1 never even
    calls it by name: in Egypt the sun was a god, here it is simply a light God sets in the sky.
    What stayed with you most: the light before the sun, the image of God given to slaves, or the
    seventh day with no evening? The full study with notes: makor.co.za/genesis/the-seven-days

## In the video (already built in)

| Time | What | Why there |
|---|---|---|
| 0:43 to 0:47 | Makor lockup above the title, "Genesis · Episode 1" below | brands the title card without delaying the hook |
| 0:47 to the end screen | Makor lockup, top right, 60% | quiet brand presence after the cold open |
| at each movement | chapter title, top left (eyebrow such as DAY ONE over its name); Day Six has two: Living creatures, then The image of God on "Let Us make man" | orients the viewer; matches the chapters |
| whenever Scripture is read | the words themselves, centred at the bottom above the player controls, at most two lines at a time and timed to the voice, with the reference beneath; God's spoken words in warm gold-cream, the reader's in cream; the GUIDE's teaching is left to the caption file | many watch with the sound off; the Scripture is the heart of the film |
| 1:32 to 1:39 | LIKE / SUBSCRIBE pill | the hook has landed, just before Day One begins |
| 11:42 to 11:50 | LIKE / SUBSCRIBE pill | the quiet of the seventh day, two thirds in |
| 14:43 to 14:53 | TELL US IN THE COMMENTS, with the closing question | the reflection question, to start the comments |
| 15:06 to 15:26 | end screen: Makor, "Study The Seven Days", the study address, WATCH NEXT · THE GARDEN space (left), SUBSCRIBE space (right) | YouTube allows end screens in the last 5 to 20 s |

## Set up in YouTube Studio after upload

1. **End screen** (Editor, End screen, last 20 s): a **Video** element over the left box, set to The Garden
   (or "Best for viewer" until The Garden v2 is up), and a **Subscribe** element over the right circle.
   Optionally a **Playlist** element (Genesis) under the video.
2. **Cards** (Editor, Info cards):
   - 8:24, at "Let Us make man": card to **The Garden**, teaser "How the man and woman were made, up close".
   - 13:42, at "Chapter three is ...": card to **The Fall**, teaser "What went wrong".
   - 1:41, as Day One begins: card to the **Genesis playlist**.
3. **Chapters** come from the description timestamps automatically.
4. **Captions**: Subtitles, upload `the-seven-days-v2-youtube.srt` (English, with timing).
5. **Watermark**: already set on the channel (`../01-the-seven-days/exports/art/branding-watermark-150.png`).
6. **Category** Education; **made for kids** no; **altered or synthetic content** yes (realistic AI imagery).
