# YouTube playbook: titles, thumbnails, openings, style

Research of 7 October 2026, from YouTube search and channel pages (views as shown that
day). First applied to The Garden (`genesis/02-the-garden/exports/youtube-pack.md`).
Makor teaches the faithful, so every rule below is held under one more: **the film must
answer the question the title and thumbnail ask.** No "shocked the world", no claims the
study does not make.

## Who wins our topics

| Channel | Subs | Format | What wins |
|---|---|---|---|
| Unraveling the Scriptures | 722K | Photoreal AI "movies", 40 min to 2 h | Daniel The Movie 8.9M (2 months), Enoch 4.8M, Genesis The Movie 1.28M |
| BibleProject | 5.5M | Animated teaching, 5 to 8 min | Genesis overview 10.6M; "Is Genesis 1 Really About How the World Was Made?" 2.1M |
| Ear to Hear | 1.0M | Maps, timelines, 15 to 25 min | "Genesis Is Not What You Think" (timeline) 1.8M |
| Nils Glenn | 241K | Presenter + maps, 12 to 20 min | **"Why The Garden of Eden Wasn't A Garden" 667K**; 100K to 1M on almost every upload |
| Kingdom Story Films | 555K | Animated teaching | Same Eden title 247K; "How the 7 Days of Creation Predict..." 691K |
| The AI Bible | 416K | Cinematic AI short films | "What if The Bible had a movie trailer" 2.1M; Revelation scenes 0.7 to 1M |
| Bible In a Nutshell | 448K | AI animated movies | David and Goliath 8.1M |
| InspiringPhilosophy | | Apologetics, 25 min | "Are There Two Creation Accounts In Genesis?" 238K |
| Mysteries of the Kingdom | 1.9K | AI Shorts | Question Shorts 30K to 126K; label Shorts under 300 |

Genesis 2 searches specifically: the plain "Genesis 2 explained" results are small (5K
to 60K) unless the title asks something. The question form wins in every search we ran.

## Titles

1. **Ask, don't label.** "Genesis 2 Read and Explained" describes; "Are There Two Creation
   Stories?" opens a loop. Across the channels above, question or tension titles beat
   label titles by 10 to 100 times.
2. **One concrete hook**: a number ("13 Feet Tall"), a disagreement ("The Manuscripts
   Disagree"), a reversal ("Wasn't A Garden", "Was Never About Science"), or "the part
   nobody reads".
3. Searchable words early (Genesis 2, Garden of Eden, Adam and Eve). Under 60 characters.
   Brand not needed in the title; YouTube shows the channel under every video.
4. Makor guard: the reversal must be one the study actually makes (Eden as sanctuary,
   ezer used of God, Genesis 2 as a close up of day six). Never invent a mystery.

## Thumbnails

1. **One face or figure, large**, photoreal, warm light. Now that films have cast, use them.
2. **The thumbnail text is not the title.** Nils Glenn: title "Why The Garden of Eden
   Wasn't A Garden", thumbnail "what was it?". The two together tell the story.
3. **Two to four words.** Fraunces, key word in gold, never over a face.
4. **Keep the bottom right clear** (YouTube's duration badge covers it).
5. **Judge at phone size** before choosing (see `concepts/feed-mock.jpg` in each film).
6. Contrast or scale sells: Genesis 1 world vs one man's face; a man beside a lion.
7. Run Test & Compare with two thumbnails on every upload and record the winner.

## Openings (where retention is won)

The top explainers state the question in the first five seconds and promise the payoff.
The Garden currently opens with a description ("Chapter one gave the world its shape")
and puts the 4 s Makor ident **before** it. Recommended for every film from The Garden on:

- **Hook first, ident second.** The first frame and first line belong to the question on
  the thumbnail. Move the ident to after the hook (around 0:10), or shorten it to 1.5 s.
- **Ask the thumbnail's question in the first line**, then promise what is coming.
  Draft for The Garden (needs your approval and a study check before it goes in
  `script/movement.py`):

  > Genesis one ends with man and woman made on the sixth day. Then chapter two tells it
  > again: dust, a garden, a rib. Two creations? Or one story, told close up for a reason?
  > And why does this garden look like a temple?

- **Pay off early, then raise the next question.** The Garden answers "two creations" at
  about 1:00 (m006); good. Each chapter should end on the question the next one answers.

## Style, music, pacing

What the winning channels share (observed from their videos and packaging; their audio
mixes were not measured, so treat the music notes as hypotheses to test):

- **Never static.** Something changes every few seconds: camera move, cut, map, caption.
  Our Veo clips will help; avoid long holds on one still under GUIDE lines.
- **Score as a bed, lifts at the turns.** The cinematic channels run music under
  everything and lift it at reveals. Keep our bed under the voice and give each chapter
  turn a lift or a sound cue as a pattern break (roughly every 60 to 90 s).
- **Captions burned in for Shorts and verticals**: two lines of serif, lower middle,
  below faces, key word in gold. Mysteries of the Kingdom and the AI movie channels all do
  this; our vertical already keeps captions clear of the platform UI.
- **Length.** Two working lengths: 10 to 25 min explainers (Nils Glenn, Ear to Hear, us)
  and 40 min to 2 h "movies" (Unraveling, Bible In a Nutshell), which collect huge watch
  time. Once Genesis has several films, a compiled **"Genesis: The Movie"** (all
  movements in order, 4K) is the obvious second product and costs no new footage.
- **Shorts as trailers.** Each film's best question gets a 45 to 60 s Short that asks it
  and points to the full film (Mysteries of the Kingdom's best Shorts are all questions).

## Tools that can check this

- **vidIQ** (Claude connector available): keyword research, "outliers" (videos beating
  their channel's average, the best signal for what topics work), similar thumbnails,
  channel stats, trending. Connect it and Claude can run this research per film.
- **YouTube Studio Test & Compare**: built in, free, tests up to three thumbnails (and
  titles where the channel has the feature) by watch time share. Use on every upload.
- **YouTube Analytics** (Studio): audience retention graph per video. The first 30 s
  drop and the dips at chapter turns tell us what to fix in the next film.
- **TubeBuddy**: browser extension, thumbnail A/B and keyword scores; overlaps vidIQ.
- **1of10 / ViewStats**: outlier finders for titles and thumbnails in a niche (paid).
- **OpusClip** (Claude connector available): cuts Shorts candidates from a long film;
  useful as a first pass, but our Shorts are scripted, so optional.
