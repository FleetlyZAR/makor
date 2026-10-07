# The Seven Days: YouTube publishing pack

File: `exports/the-seven-days-youtube.mp4` (1920x1080, 30 fps, about 15:18, -14 LUFS).
Captions: `exports/the-seven-days-youtube.srt` (every spoken line, timed to this file).
Uploaded to YouTube (title and thumbnail A as below); see "Question thumbnails for the live video" for the test now planned.

## Title (YouTube Help: up to 100 characters, most important words first, branding at the end, accurate)

Recommended:

    The Seven Days of Creation: Genesis 1, Day by Day | Makor

Alternatives:

    In the Beginning: The Seven Days of Genesis 1 | Makor
    Genesis 1:1 to 2:3, The Seven Days of Creation | Makor
    The Seven Days: Genesis 1 Read and Explained | Makor

All are under 60 characters, so they show in full on most screens. They lead with the
words people search for (seven days, creation, Genesis 1) and keep the brand last.

## Thumbnail

`exports/art/thumbnail-a.jpg` (light breaking across the deep) or
`exports/art/thumbnail-b.jpg` (the full world around the bay). 3840x2160, JPG, about
1.3 MB, as YouTube recommends. Recommended: A for the first upload; it carries the film's
one idea, light out of darkness.

## Question thumbnails for the live video (7 October 2026)

The video is already up with the label title and thumbnail above. Following
`films/YOUTUBE-PLAYBOOK.md`, three question thumbnails were made to test on it, each
asking something the film answers. They are painted (this film predates the photoreal
cast), so they lean on light and contrast instead of a face. Made by
`exports/art/concepts/make_concepts.py --final` (3840x2160, under 2 MB each).

| File | Thumbnail | Paired title | Answered at |
|---|---|---|---|
| `exports/art/thumbnail-q-light.jpg` | LIGHT BEFORE THE SUN? (s026) | Light Before the Sun? Genesis 1 Explained, Day by Day | m111 and Day One |
| `exports/art/thumbnail-q-sun.jpg` | THE SUN IS NOT A GOD (s010) | What Genesis 1 Said to the Gods of Egypt and Babylon | m007 to m010 |
| `exports/art/thumbnail-q-how-long.jpg` | HOW LONG? (s057) | How Long Were the Seven Days? The Better Question in Genesis 1 | m089 to m092 |

The film does not pick a length for the days; it sets out the views and turns to who
God is. So the "how long" title promises "the better question", not an answer; never
retitle it as "Were the Days 24 Hours?".

### Steps in YouTube Studio

1. Content, open The Seven Days, Details. Under Thumbnail choose **Test & Compare**
   and upload the three `thumbnail-q-*` files (up to three; the current painted title
   card can stay as one of them only if you want a baseline, in which case drop
   `how-long`).
2. Leave the title as it is while the thumbnail test runs, so only one thing changes.
   If Studio offers title testing for this video, test the three paired titles instead.
3. When YouTube picks a winner (by watch time share, up to two weeks), set the paired
   title for that thumbnail and record the result here.
4. Optional: open the description with the winning question in one line, above the
   study link.

## Description

    Study The Seven Days: https://www.makor.co.za/genesis/the-seven-days/

    Before the drama of a fallen world begins, God speaks a formless void into an ordered,
    good, and habitable home. This film reads Genesis 1:1 to 2:3 in full, day by day, and
    walks through what the chapter meant to its first hearers, how its two panels of
    forming and filling answer "formless and void", why the seventh day has no evening,
    and how the New Testament reads it in Christ.

    Made with AI tools; Scripture from the Berean Standard Bible.

    Chapters
    0:00 Cold open
    0:43 A world of other stories
    1:45 Formless and void
    2:51 Day One: light
    3:36 Day Two: the sky
    4:22 Day Three: land, sea and green
    5:30 Day Four: the lights
    6:48 Day Five: sea and sky
    7:46 Day Six: the image of God
    10:37 Day Seven: rest
    11:45 How long were the days?
    12:17 In the beginning was the Word
    13:32 The first page and the last
    14:33 Light in a dark place

    Makor walks through the Bible one movement at a time: the text, its world, and its
    place in the one story that leads to Christ.

## Pinned comment (a reflection question from the study)

    On the first day God said, let there be light, before the sun existed, because light
    comes from Him. Where do you need to ask God to speak light into a dark place?

## Calls to action in the video, and where they sit

- **Like and subscribe prompt**: a quiet lower left card (Makor mark, LIKE, SUBSCRIBE, "for
  every movement of Scripture, one study at a time") at about 2:42 to 2:49, the first
  natural pause: after the viewer has had the opening and the context, before Day One
  begins, and while no Scripture is on screen. Once only, no voice, so it never competes
  with the text.
- **End screen**: the last 20 s (14:58 to 15:18 of the file, after the closing card) are
  a calm background with the Makor lockup, "Study The Seven Days" and the study address,
  and two clear spaces labelled WATCH NEXT (left) and SUBSCRIBE (right). YouTube allows
  end screens in the last 5 to 20 seconds of a video of at least 25 seconds.

### Set up in YouTube Studio after upload

1. Editor, End screen: add a **Subscribe** element over the SUBSCRIBE space (right) and a
   **Video** element ("Best for viewer") over the WATCH NEXT space (left), both for the
   full last 20 s.
2. Customisation, Branding, Video watermark: upload `exports/art/branding-watermark-150.png`
   (the Makor mark), display "Entire video". Viewers can subscribe by tapping it.
3. Customisation, Branding, Picture: `exports/art/channel-icon-800.png` (the app icon).
4. Chapters appear automatically from the timestamps in the description (first at 0:00).

## Makor in the video

- Opening: a 4 s Makor ident (the rings drawn outward around the gold source point, then
  the wordmark), fading into the dark deep.
- A small Makor lockup in the top right corner from the second chapter until the closing card.
- The closing card and end screen carry the study address.
