# The Seven Days (v2, the pilot): YouTube publishing pack

File: `exports/the-seven-days-v2-youtube.mp4` (1920x1080, 24 fps, 15:26: the film 15:06 plus a 20 s end
screen; -14 LUFS for YouTube). Captions: `exports/the-seven-days-v2-youtube.srt` (every spoken line, timed to
this file). Built by `edit/youtube_cut.py` from `exports/full-cut-v2.mp4`.

This replaces the painted v1 on the channel. Plan agreed earlier (D-list in V2-TREATMENT.md): upload v2, then
unlist v1 a week later so its views and comments are not lost at once.

## Title (most searched words first, brand last, under 70 characters)

Recommended:

    In the Beginning: Genesis 1 and the Seven Days of Creation | Makor

Alternatives:

    The Seven Days of Creation, Like You've Never Seen Them | Genesis 1 | Makor
    Light Before the Sun? Genesis 1, Day by Day | Makor
    Genesis 1 Explained: What Israel Heard in Egypt | Makor

Search data (vidIQ, 8 October 2026): "in the beginning" about 23,000 searches a month with low competition
(26/100); "genesis 1" about 33,000 (42/100); "creation" about 126,000 (41/100); "bible study" about 241,000.

## Thumbnails (Test & Compare, all three)

Made by `exports/art/concepts/make_concepts.py --final` from the film's own frames (3840x2160, under 2 MB each).
Upload all three to Test & Compare (`films/YOUTUBE-PLAYBOOK.md`); keep the recommended title while the test runs,
then set the paired title for the winner.

| File | Thumbnail | Paired title | Answered at |
|---|---|---|---|
| `exports/art/thumbnail-v2-light.jpg` | LIGHT BEFORE THE SUN? (s040, light racing across the black deep) | Light Before the Sun? Genesis 1, Day by Day \| Makor | Day One and 3:25 |
| `exports/art/thumbnail-v2-slave.jpg` | A SLAVE HEARD THIS FIRST (s022, the brick-maker at the kiln) | A Slave in Egypt Heard This First: Genesis 1 \| Makor | 0:24 and 9:25 |
| `exports/art/thumbnail-v2-beginning.jpg` | IN THE BEGINNING (the burst, s003) | In the Beginning: Genesis 1 and the Seven Days of Creation \| Makor | the cold open |

## Description

    Study The Seven Days: https://www.makor.co.za/genesis/the-seven-days/

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

## Tags

    genesis 1, the seven days of creation, in the beginning, creation, genesis creation story, bible study,
    bible study for beginners, genesis bible study, days of creation, let there be light, image of god,
    sabbath rest, genesis explained, old testament, bible story, adam and eve, makor

## Pinned comment

    On the first day God said, let there be light, before the sun existed. Where do you need to ask God to speak
    light into a dark place? Tell us below.

## In the video (already built in)

| Time | What | Why there |
|---|---|---|
| 0:43 to 0:47 | Makor lockup above the title, "Genesis · Episode 1" below | brands the title card without delaying the hook |
| 0:47 to the end screen | Makor lockup, top right, 60% | quiet brand presence after the cold open |
| at each movement | chapter title lower left (eyebrow such as DAY ONE over its name); Day Six has two: Living creatures, then The image of God on "Let Us make man" | orients the viewer; matches the chapters |
| as each verse begins | Scripture reference lower left (GENESIS 1:3, JOHN 1:1 ...), 4 s, kept above the bottom 120 px where the player's controls sit | every quotation is sourced on screen |
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
