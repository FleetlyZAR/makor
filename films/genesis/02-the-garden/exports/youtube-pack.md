# The Garden: YouTube publishing pack (draft)

File: `exports/the-garden-youtube.mp4` (1920x1080, 30 fps, about 11:02, -14 LUFS).
Captions: `exports/the-garden-youtube.srt` (every spoken line, timed to this file).
Nothing here has been uploaded.

Drafted 6 October 2026 from the v1 cut. Shot timings stay the same when the Veo clips go in,
so the chapter times and the call to action times below should hold; check them against the
rebuilt file before upload.

## Title (YouTube Help: up to 100 characters, most important words first, accurate)

Chosen 7 October 2026 (question led, after studying what clicks in this niche; see
`exports/art/concepts/` for the five concepts tested):

    Genesis 1 vs Genesis 2: Are There Two Creation Stories?

Second title, paired with thumbnail B for YouTube's Test & Compare (titles can be
tested alongside thumbnails where the channel has the feature):

    Why Did God Make Adam from Dust? | Genesis 2 Explained

Both are honest: the film answers each question. "Two creation stories" is answered at
m006 ("Read as it stands, it is a close up of the sixth day, and Jesus quotes both
chapters together"); "dust" is the whole Dust and breath chapter (Genesis 2:7). A
neighbouring channel's "Genesis 1 vs. Genesis 2: Were There Two Creations of Humanity?"
Short has 30K views, so the question has a proven audience.

Why the change from "The Garden of Eden: Genesis 2 Read and Explained | Makor": labels
describe, questions open a loop. In the channels studied, question titles with one
concrete hook outperformed plain labels by 10 to 100 times. The brand is dropped from
the title; YouTube shows the channel name under every video anyway, and the thumbnail
and film carry Makor.

Earlier label titles (kept for reference, not recommended):

    The Garden of Eden: Genesis 2 Read and Explained | Makor
    Formed from Dust: The Garden of Genesis 2 | Makor

## Thumbnail

Photoreal, question led, made by `exports/art/concepts/make_concepts.py --final`
(3840x2160 JPG, under YouTube's 2 MB limit; `film.json` sets `thumbnails_custom` so
`platform_versions.py art` no longer overwrites them). The painted v1 thumbnails are
kept in `exports/art/painted/`.

- `exports/art/thumbnail-a.jpg` **TWO CREATIONS?** Split frame: the barren earth of
  Genesis 1 (s004) beside Adam's face (cast/adam). Upload this as the main thumbnail.
- `exports/art/thumbnail-b.jpg` **WHY DUST?** The first breath, the man lying in the
  grass (s016), Genesis 2:7. Add as the second image in Test & Compare.

The thumbnail words do not repeat the title; they add to it. Rules used (keep for every
film): one face or figure, large; text never over a face; two to four words, Fraunces,
key word in gold; bottom right corner left clear for YouTube's duration badge; judged
at phone size (`concepts/feed-mock.jpg`) before choosing.

### Test plan

Run YouTube Studio's Test & Compare with A and B for its full period (up to two weeks;
YouTube picks by watch time share, not clicks alone). Keep the winner, note the result
here, and use it to choose the style for The Fall.

## Description

    Study The Garden: https://www.makor.co.za/genesis/the-garden/

    Chapter 1 gave the world its shape; Genesis 2 gives it a centre, a garden where the
    LORD God dwells with the man and woman He has made. This film reads Genesis 2:4 to 25
    in full and walks through what it meant to its first hearers: the man formed from the
    dust and given the breath of life, a garden in Eden with its river and two trees, the
    work to cultivate and keep it, one command, the helper who is his match, and the first
    marriage. Then it follows the garden through the Bible, to Christ the last Adam and to
    Eden restored.

    Made with AI tools; Scripture from the Berean Standard Bible.

    Chapters
    0:00 Cold open
    0:20 From the heavens to the ground
    1:12 Dust and breath
    2:25 A garden in Eden
    4:07 To cultivate and keep
    5:34 Not good to be alone
    6:46 Bone of my bones
    8:22 The last Adam
    9:30 Eden restored
    10:08 Dust that breathes

    Makor walks through the Bible one movement at a time: the text, its world, and its
    place in the one story that leads to Christ.

## Pinned comment (a reflection question from the study, questions[0])

    You were formed from dust and given life by God's breath. How does remembering that you
    are both earthy and God-breathed change how you see your worth today?

## Calls to action in the video, and where they sit

- **Like and subscribe prompt**: a quiet lower left card (Makor mark, LIKE, SUBSCRIBE, "for
  every movement of Scripture, one study at a time") at about 1:04 to 1:11, just before
  "Dust and breath" begins. Once only, no voice. It sits over a GUIDE line, not Scripture,
  and the YouTube version burns in no GUIDE captions at that spot, so nothing collides.
- **End screen**: the last 20 s (10:42 to 11:02 of the file, after the closing card) are
  the garden in calm morning light (s092) with the Makor lockup, "Study The Garden" and the
  study address, and two clear spaces labelled WATCH NEXT (left) and SUBSCRIBE (right).
  YouTube allows end screens in the last 5 to 20 seconds of a video of at least 25 seconds.

### Set up in YouTube Studio after upload

1. Editor, End screen: add a **Subscribe** element over the SUBSCRIBE space (right) and a
   **Video** element over the WATCH NEXT space (left), both for the full last 20 s. Choose
   The Seven Days as the video, so viewers go back to the start of Genesis.
2. On The Seven Days, once this film is up, you may change its end screen video from "Best
   for viewer" to The Garden, so the two films lead into each other.
3. Add both films to one playlist (for example "Genesis, movement by movement") in order.
4. Chapters appear automatically from the timestamps in the description (first at 0:00).
5. AI disclosure: answer Yes. From 7 October 2026 The Garden is photoreal (realistic people who did not exist); the painted v1 is superseded.

## Makor in the video

- Opening: the 4 s Makor ident (the rings drawn outward around the gold source point, then
  the wordmark), fading into the film.
- A small Makor lockup in the top right corner from "From the heavens to the ground" until
  the closing card.
- The closing card and end screen carry the study address.
