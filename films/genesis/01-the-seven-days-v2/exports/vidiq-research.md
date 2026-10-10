# The Seven Days (v2): vidIQ packaging research

Research of 9 October 2026 with the vidIQ connector (keyword research, outliers, YouTube search,
similar videos, title and thumbnail scoring). Research only: nothing was uploaded or changed on
YouTube. Read with `films/YOUTUBE-PLAYBOOK.md` and `exports/youtube-pack.md`.

## Recommendations (summary)

**Primary keyword:** `genesis 1` (about 32,900 searches a month, competition 42/100, overall 63.5).
It is the most searched phrase that means exactly this film. The broader words are bigger but
polluted: "creation" (125K) is mostly content creation and games, "genesis" (359K) is mostly cars,
anime and games.

**Secondary keywords:** `7 days of creation` / `seven days of creation` (4,200 and 4,900, low
competition 29 to 32), `genesis chapter 1` (4,900, competition 18, the easiest win), `in the
beginning` (31,700, competition 26.5, mixed intent), `let there be light` (30,000), `book of
genesis` (23,600 and rising 142%), `genesis 1 explained` / `genesis 1 bible study` (about 5,300
each), `bible study` (251K, the umbrella).

**Title (keep this one while the thumbnail test runs):**

    Genesis 1 Like You've Never Seen It: The 7 Days of Creation

59 characters, vidIQ score 97/100 (the highest of the 13 scored). Primary keyword first, the
second keyword in full, and the promise (a cinematic, photoreal film) is one the film keeps.

**Alternates (to pair with the thumbnail test; swap in the winner's title afterwards):**

    Light Before the Sun? Genesis 1 and the 7 Days of Creation          (58 chars, score 88)
    The 7 Days of Creation: What Genesis 1 Told a Nation of Slaves      (62 chars, score 88)

**Brand:** leave "| Makor" off. It cost 1 point every time it was tested (97 to 96, 91 to 90),
adds 8 characters that push the keywords towards the mobile cut, and YouTube already prints the
channel name under every video. Keep Makor in the description, tags and on screen.

**Thumbnails for Test & Compare** (made by `exports/art/concepts/make_concepts_research.py`,
3840x2160, all under 1.4 MB; previews and a phone feed mock in `exports/art/concepts/research-*`):

| File | Concept | On-screen text | Frame | Paired title |
|---|---|---|---|---|
| `exports/art/thumbnail-r1.jpg` | A face: the brick-maker looking up by the kiln fire | GENESIS 1:27 / MADE IN **GOD'S IMAGE** | `stills/cast/shot-06.jpg` (the frame behind s023) | The 7 Days of Creation: What Genesis 1 Told a Nation of Slaves |
| `exports/art/thumbnail-r2.jpg` | A question: light racing over the black deep, no sun in the sky | DAY ONE · GENESIS 1:3 / WHERE'S THE **SUN?** | s040 | Light Before the Sun? Genesis 1 and the 7 Days of Creation |
| `exports/art/thumbnail-r3.jpg` | Spectacle, movie poster style: the earth from space | THE SEVEN DAYS / **GENESIS 1** | s005 | Genesis 1 Like You've Never Seen It: The 7 Days of Creation |

My pick to win: **r1** (a large, warm, human face is what the data rewards; see the evidence).

**Tags** (422 characters):

    genesis 1, the 7 days of creation, seven days of creation, genesis chapter 1, creation story,
    in the beginning, let there be light, genesis creation, book of genesis, genesis explained,
    genesis 1 explained, genesis 1 bible study, genesis bible study, bible study, creation of the
    world, how god created the world, light before the sun, image of god, sabbath, cinematic bible,
    bible movie, bible story, old testament, makor

**First two lines of the description** (what shows above "...more"):

    Genesis 1 like you've never seen it: the 7 days of creation read in full (Genesis 1:1 to 2:3), filmed day by day, and what it meant to a nation of slaves coming out of Egypt.
    Why is there light before the sun? Why does the seventh day have no evening? Study it free: https://www.makor.co.za/genesis/the-seven-days/

Then the rest of the current description from `youtube-pack.md` (the chapters must stay, starting
at 0:00).

**Pinned comment:**

    On Day One there is light, but the sun does not appear until Day Four, and Genesis 1 never even
    calls it by name: in Egypt the sun was a god, here it is simply a light God sets in the sky.
    What stayed with you most: the light before the sun, the image of God given to slaves, or the
    seventh day with no evening? The full study with notes: makor.co.za/genesis/the-seven-days

**Two things to act on outside the packaging:**

1. The v1 film is live as "The 7 Days of Creation: What They Meant to the First Hearers"
   (`5vExqi1jGvc`, 6 October, 81 views, 0.7 views an hour). Its painted landscape thumbnail scored
   **43/100**. When v2 goes up with the title above, the two will not compete for the same exact
   title; unlist v1 a week later as planned.
2. The label space is crowded: at least a dozen small AI channels uploaded "Genesis 1: The Creation
   of the World | Cinematic Bible" in the last year and almost all sit at 20 to 1,500 views. A
   label title and a pretty landscape will be lost among them. The face and the question are what
   set this film apart.

## Evidence

### 1. Keywords (vidIQ, global estimates, 9 October 2026)

Volume and competition are vidIQ's 0 to 100 scores; overall combines them (higher is a better
opportunity). Growth compares the current month with the 30 day baseline where vidIQ had one.

**Core terms for this film**

| Keyword | Searches / month | Volume | Competition | Overall | Note |
|---|---:|---:|---:|---:|---|
| genesis 1 | 32,940 | 67.4 | 42.4 | 63.5 | primary; down 38% on a 53K baseline (seasonal), still the largest exact match |
| in the beginning | 31,692 | 67.2 | 26.5 | 69.7 | lowest competition at scale; related terms include film music, so mixed intent |
| let there be light | 29,973 | 66.8 | 40.7 | 63.8 | mixed with songs and films |
| book of genesis | 23,585 | 65.3 | 40.9 | 62.8 | up 142% |
| sabbath | 23,180 | 65.2 | 50.1 | 59.1 | mixed (the band) |
| reading genesis 1 | 8,187 | 58.4 | 28.3 | 63.7 | |
| genesis bible study | 7,345 | 57.7 | 28.5 | 63.2 | |
| six days of creation | 5,410 | 55.7 | 26.4 | 62.9 | |
| genesis 1 bible study | 5,412 | 55.7 | 30.9 | 61.1 | |
| genesis explained | 5,384 | 55.7 | 43.0 | 56.2 | |
| genesis 1 explained | 5,283 | 55.6 | 34.3 | 59.6 | |
| how god created the world | 5,147 | 55.4 | 33.0 | 60.0 | |
| genesis chapter 1 | 4,947 | 55.1 | 18.3 | 65.8 | easiest win |
| seven days of creation | 4,889 | 55.1 | 28.6 | 61.6 | |
| image of god | 4,696 | 54.8 | 38.2 | 57.6 | |
| 7 days of creation | 4,221 | 54.1 | 31.8 | 59.8 | |
| genesis creation | 4,092 | 53.9 | 38.5 | 57.0 | |
| creation of the world | 3,800 | 53.4 | 36.3 | 57.5 | |
| creation story | 3,389 | 52.7 | 47.5 | 52.6 | |
| genesis movie | 3,387 | 52.7 | 38.8 | 56.1 | |
| creation story bible | under 750 | 0 | 38.5 | 24.6 | too small |

**Long tail and questions that match what the film teaches**

| Search | Searches / month | Competition | Overall | Fit |
|---|---:|---:|---:|---|
| the hebrew word for "created" in genesis 1 is reserved for god | 12,479 | 9.7 | 72.8 | the film does not dwell on bara; description only |
| god 7 days of creation | 5,558 | 36.0 | 59.1 | yes |
| how to interpret genesis 1-3 | 5,586 | 22.8 | 64.4 | yes (how Israel heard it) |
| the hidden meaning behind the 7 days of creation | 5,338 | 19.3 | 65.7 | yes (forming and filling) |
| do the 7 days of creation predict ... | 5,250 | 24.1 | 63.7 | no (science framing) |
| the 7 days of creation were never days | 4,979 | 11.9 | 68.4 | **avoid**: the film does not argue the length of the days |
| what was before creation genesis 1 1 explained | 4,586 | 33.8 | 59.3 | partly |

**Umbrella terms**

| Keyword | Searches / month | Volume | Competition | Overall |
|---|---:|---:|---:|---:|
| bible stories | 903,550 | 88.9 | 64.0 | 67.7 |
| bible | 781,844 | 88.0 | 63.9 | 67.2 |
| genesis (mostly cars, anime, games) | 358,696 | 82.9 | 71.0 | 61.4 |
| bible study | 250,841 | 80.6 | 50.1 | 68.3 |
| bible story | 201,493 | 79.2 | 47.5 | 68.5 |
| bible animation | 196,077 | 79.0 | 55.0 | 65.4 |
| creation (59% Brazil; matching terms are content creation and games) | 125,547 | 76.1 | 41.5 | 69.1 |
| adam and eve | 75,559 | 72.8 | 54.8 | 61.8 |
| apologetics | 72,193 | 72.5 | 55.5 | 61.3 |
| theology | 40,502 | 68.8 | 45.8 | 62.9 |
| bible study with me | 21,995 | 64.8 | 31.3 | 66.4 |
| bible movie | 11,531 | 60.6 | 54.5 | 54.6 (up 158%) |

**By country (in-country monthly searches, vidIQ country search)**

| Country | What the data shows |
|---|---|
| US | bible stories 168,146; bible 131,774; bible study 84,175; genesis 58,359 (mostly non-Bible: Star Wars, Evangelion, Sega, cars); bible study for beginners 12,787; creation 5,584 |
| ZA | bible stories for kids 16,839; bible 15,374; bible animation 7,906; bible project 5,120; bible study 5,101; bible study for beginners 3,197; genesis 2,432 |
| NG | genesis 4,863; "creation" in Nigeria is entirely AI video and content creation |
| GB | bible stories 32,336; bible study 20,406; bible animation 18,447; bible 17,570; bible in a nutshell 10,304; bible stories movies 7,879; bible project 7,680 |
| PH | genesis 1 5,459 (the one market where "genesis 1" itself shows up in-country) |
| IN | bible 79,065; bible stories 58,204; bible reading 34,492; bible in a nutshell 23,185 |

Reading: outside the US, people search the broad words (bible, bible stories, bible animation,
bible study) far more than chapter references. That is why the title carries both the exact
phrase (Genesis 1) and the plain one (7 Days of Creation), and the tags carry "bible story",
"bible movie" and "cinematic bible".

### 2. Competitors and outliers

**Biggest winners on this topic** (views as shown on 9 October 2026)

| Video | Channel | Views | Format / packaging |
|---|---|---:|---|
| [Book of Genesis Summary (Part 1)](https://youtu.be/GQI72THyO5I) | BibleProject | 10.6M | label, flat illustration, 2015 |
| [The Book of Genesis Full Movie](https://youtu.be/W10-Xwk_fsU) | GIDEON FILMS | 12.7M | 4 h visualised movie |
| [The Book of Genesis: The Movie (2026)](https://youtu.be/n0n0Iw_E8F4) | Unraveling the Scriptures (729K subs) | 1.29M | 2 h AI movie; Eve's face large, gold serif "GENESIS THE MOVIE", 4K badge |
| [Is Genesis 1 Really About How the World Was Made?](https://youtu.be/afVN-7vY0KA) | BibleProject | 2.13M | question title, 7:43 |
| [Charlie Kirk Breaks Down Genesis 1](https://youtu.be/Etql4uVwr1s) | Psalms & Palms (32K subs) | 679K | famous face, outlier 151x |
| [The 7 Days of Creation, The Grand Narrative Ep. 2](https://youtu.be/epE6YktzOy0) | Childlike Media | 225K | 4:23 cinematic, cosmic image with white serif title |
| [What the First Word of Genesis Actually Says in Hebrew](https://youtu.be/6WsekC1clrA) | The Bible Unfolded (5K subs) | 132K | breakout 291x; old man's face plus "IS NOT 'In The Beginning'" |
| [Who Wrote Genesis?](https://youtu.be/WnPhEa9lKrE) | Lamb of Odd (1.7K subs) | 148K | breakout 179x; 2 word question on black |
| [What Sumerian History Reveals About Genesis](https://youtu.be/nfB---q87JY) | The Buried Bible Podcast (5.7K subs) | 101K | breakout 79x; Babylon/Sumer angle, two faces |
| [If Adam Was First, Why Does Genesis 1:2 Show a Ruined Earth?](https://youtu.be/K5f1k3quhLA) | Sons of Heaven (4.9K subs) | 43K | 562 views an hour; "BEFORE ADAM?" over a figure |
| [What Happened Between Genesis 1:1 and 1:2?](https://youtu.be/ZJy8-Y9lh-4) | Les Feldick Bible Study | 59K | breakout 35x; question |

**The light before the sun question works for tiny channels**

| Video | Channel (subs) | Views | Signal |
|---|---|---:|---|
| [How could there have been day and night before God created the Sun?](https://youtu.be/I06DtJdFc24) | Creation Ministries International (217K) | n/a | outlier 179x |
| [The Hebrew Word Genesis Uses for Light (It's Not What You Think)](https://youtu.be/hVAAaAUyTxY) | Bible Made Bare (108 subs) | 8,507 | outlier 151x, 33 views an hour; same teaching as ours (or vs meorot, sun gods, forming and filling, John 1) |
| [Did Genesis Get the Sun Wrong?](https://youtu.be/SKAHm_yhh3E) | The Science Christian Guy (2.3K) | 8,108 | outlier 16x |

**Cinematic AI Bible channels: the movie poster pattern**

| Video | Views | Note |
|---|---:|---|
| [Daniel, The Movie (2026)](https://youtu.be/2R1aaROltxE) (Unraveling) | 9.1M | 2,084 views an hour; small figure against a giant lion, gold serif title, 4K badge |
| [Enoch, The Movie (2026)](https://youtu.be/wJkXjNbsD-Y) (Unraveling) | 5.0M | 2,281 views an hour; same template |
| [Elijah, The Movie (2026)](https://youtu.be/nfpMvVE8LGU) (Unraveling) | 2.1M in 6 days | 11,363 views an hour |
| [The Complete Book of Isaiah Like You've Never Seen It Before](https://youtu.be/WnSOeve1wa0) (Iron Pen, 8.8K subs) | 269K | **breakout 5,290x**; one big warm face, gold "ISAIAH", "FULL MOVIE" |
| [13 Creatures from the Bible like you've never seen before](https://youtu.be/8dEiQpB6rbQ) (Unraveling) | 611K | same "never seen" promise |
| [Shadrach, Meshach and Abednego (Cinematic Bible Story)](https://youtu.be/p4FrGy2Y9gg) (The Great Bible Stories, 1.5K subs) | 152K | breakout 141x |

**The crowded label space** (all published in the last 12 months, all "Genesis 1 ... Cinematic"):
Bible in Video 4k 329 views; Movie Bible 1189 319 and 396; Wanna Know? 327; Elyon 238; The Bible
Stories 1,470; LIVE BIBLE 147; Cinematic Bible 21; Genesis1Bible 29; Bible Flow 1; 루아루미 1,387;
Trust in God 1,001. Same words, a landscape, a label: almost nobody clicks.

**Short form**: Mysteries of the Kingdom's question Short "Genesis 1 vs. Genesis 2: Were There Two
Creations of Humanity?" has 34K views on a 2K sub channel; Bible Animations' "Jesus name is HIDDEN
in Genesis 1:1" has 2.0M. Questions win in Shorts too; a 45 to 60 s "Where's the sun?" Short
pointing to the film is the obvious first trailer.

**Thumbnail patterns across the winners** (montage checked by eye):

1. One figure or face, large and warmly lit (Isaiah, Eve, the Hebrew word video, Charlie Kirk).
2. Gold or cream serif type, 1 to 4 words, often a question ("BEFORE ADAM?", "Who wrote Genesis?").
3. Scale or contrast (a man beside a lion; a figure in a ruined world).
4. Dark, cinematic grade with one warm light source.
5. Landscapes without a figure and plain labels are what the small channels use, and they lose.

**Makor itself** (`UC_APDhxL92jfp0VdZZijDUA`): one long upload, the v1 film (81 views, 7 likes,
3 comments, 0.7 views an hour, breakout 2.5); no Shorts yet. Nothing yet to learn from our own
numbers, so this pilot's Test & Compare result will be the first real data point.

### 3. Title scores (vidIQ score_title, long form, with the Makor channel ID)

| Title | Chars | Score |
|---|---:|---:|
| **Genesis 1 Like You've Never Seen It: The 7 Days of Creation** | 59 | **97** |
| Genesis 1: The 7 Days of Creation Like You've Never Seen Them | 61 | 97 |
| The 7 Days of Creation Like You've Never Seen Them \| Genesis 1 | 62 | 97 |
| Genesis 1 Like You've Never Seen It: The 7 Days of Creation \| Makor | 67 | 96 |
| The 7 Days of Creation: What They Meant to the First Hearers (live v1) | 60 | 96 |
| The 7 Days of Creation: What Genesis 1 Told Slaves in Egypt | 59 | 91 |
| In the Beginning: Genesis 1 and the Seven Days of Creation | 58 | 91 |
| In the Beginning: Genesis 1 and the Seven Days of Creation \| Makor | 66 | 90 |
| Genesis 1 Was Never About Science. A Nation of Slaves Heard It First | 68 | 89 |
| **Light Before the Sun? Genesis 1 and the 7 Days of Creation** | 58 | **88** |
| **The 7 Days of Creation: What Genesis 1 Told a Nation of Slaves** | 62 | **88** |
| Genesis 1 Explained: The 7 Days of Creation, Day by Day | 55 | 86 |
| Made in God's Image: What Genesis 1 Told Slaves in Egypt | 56 | 86 |
| Genesis 1 vs Babylon: The Creation Story That Set Slaves Free | 61 | 84 |
| Genesis 1: Why Was There Light Before the Sun? | 46 | 82 |

Notes:

- The scorer clusters high (82 to 97) and even rated the live v1 title 96, which has 81 views,
  so treat it as a tie breaker, not proof. The outlier data above carries more weight.
- The primary title takes the top score and the keyword order the search data asks for.
  "Like You've Never Seen It" is the phrase behind Iron Pen's 5,290x breakout and Unraveling's
  611K video, and it is honest here: every day of Genesis 1 is shown in photoreal footage.
- "Told a Nation of Slaves" is used instead of "Slaves in Egypt" (91) because the film's line is
  "Then a nation of slaves heard this one", and Israel heard it coming out of Egypt, not in the
  brick pits. Accuracy over 3 points.
- Rejected: "Set Slaves Free" (the film does not claim that), anything about the length of the
  days, and "Was Never About Science" (the film does not argue science either way).

### 4. Thumbnails

**Scoring.** vidiq_score_thumbnail needs a public image URL or a vidIQ-hosted upload; it cannot read
local files, and hosting our drafts somewhere public would mean publishing them, so the three drafts
(`thumbnail-v2-*.jpg`) and the three new files were **not scored**. For calibration I scored, against
our video ID and proposed titles:

| Image | Score | vidIQ's main notes |
|---|---:|---|
| Makor v1 live thumbnail (painted coast, "THE SEVEN DAYS") | 43 | no clear focal point or eye guidance; composition too empty |
| Bible Made Bare "Genesis 1 Light Before the Sun" (scroll diagram) | 33 | busy, no face, no wow factor |
| Iron Pen "ISAIAH" (big warm face, gold serif title) | 86 | sharp, clear value, bold contrast |

The scorer rewards exactly what the outliers show: a large lit face, one clear subject, bold
contrast, a few words. r1 is built on that template; r2 and r3 test the question and the
spectacle against it.

**r1, a face: MADE IN GOD'S IMAGE** (`exports/art/thumbnail-r1.jpg`)

- Frame: `stills/cast/shot-06.jpg`, the brick-maker by the kiln at dusk lifting his eyes (it is the
  still behind s023 in the cold open). Cropped at zoom 1.25 so his face fills the left 40% of the
  frame; his upward gaze leads the eye across to the words.
- Text: kicker "GENESIS 1:27" (sans, gold), then "MADE IN" (cream) / "GOD'S" / "IMAGE" (gold),
  Fraunces 120, right aligned at the top right over the dark brick wall, shaded right. Never over the
  face; bottom right (fire glow) left clear for the duration badge.
- Why: faces are the strongest single signal in this niche (Iron Pen 86 and 5,290x; The Bible
  Unfolded 291x; Unraveling's Genesis movie leads with Eve's face). The words state the film's
  central reversal: in Babylon's story people carry the gods' labour; in Genesis the image of God
  is given to a slave. The thumbnail does not repeat the title, it completes it.
- Paired title: The 7 Days of Creation: What Genesis 1 Told a Nation of Slaves.
- Paid off at: the cold open (0:24) and Day Six, the image of God (8:24).

**r2, a question: WHERE'S THE SUN?** (`exports/art/thumbnail-r2.jpg`)

- Frame: s040, the line of gold light racing over the black ocean on Day One. Cropped (zoom 1.18,
  focus left of centre) so the light edge cuts diagonally under the words; contrast lifted, bottom
  and left shaded.
- Text: kicker "DAY ONE · GENESIS 1:3", then "WHERE'S" / "THE SUN?" with SUN? in gold, Fraunces
  150, top left. Two lines only, readable at 360 px wide (see the feed mock).
- Why: light before the sun is the one Genesis 1 question with proven pull on small channels
  (CMI 179x, Bible Made Bare 151x on 108 subscribers, Science Christian Guy 16x), and the picture
  itself raises the question: there is light and no sun. Different from the earlier "LIGHT BEFORE
  THE SUN?" draft: shorter, two lines, and it asks the viewer to look for the sun.
- Paired title: Light Before the Sun? Genesis 1 and the 7 Days of Creation.
- Paid off at: Day One (1:41 to 3:38) and Day Four, the first sunrise (5:19).

**r3, spectacle: GENESIS 1** (`exports/art/thumbnail-r3.jpg`)

- Frame: s005, the earth from space with Africa and Arabia facing us (cold open). Brightened and
  cropped so the lit limb arcs across the upper two thirds; black space below.
- Text: kicker "THE SEVEN DAYS" (spaced sans, gold), then "GENESIS 1" (Fraunces 150, gold),
  centred low in the black. Ends 100 px short of the duration badge.
- Why: this is the movie poster template of the channels pulling millions (Daniel 9.1M, Enoch 5.0M,
  Genesis 1.29M: one image, one gold serif title). It tests whether the scale of the film alone
  sells it. No "4K" badge, because the upload is 1080p.
- Paired title: Genesis 1 Like You've Never Seen It: The 7 Days of Creation.
- Paid off at: the cold open (0:00 to 0:47) and every day after it.

**Checks done:** all three rendered at 1280x720 and at 3840x2160, looked at full size and in the
phone feed mock (`exports/art/concepts/research-feed-mock.jpg`, 360 px wide with the 15:26 badge).
Text is legible at phone size, nothing is cut off, no text crosses a face, and the bottom right is
clear in all three. File sizes: r1 1.24 MB, r2 1.24 MB, r3 1.40 MB. The existing
`thumbnail-v2-*.jpg` files were not touched.

**How to run the test:** upload r1, r2 and r3 to Test & Compare with the primary title. When
YouTube picks a winner (watch time share), switch the title to that thumbnail's paired title only if
the winner is r1 or r2, and record the result in `films/YOUTUBE-PLAYBOOK.md`.

### 5. Tags, description and pinned comment: reasoning

- Tags lead with the exact film keywords (genesis 1, 7 days of creation, genesis chapter 1),
  then the questions the film answers (light before the sun, image of god, sabbath), then the
  broad discovery words that dominate outside the US (bible study, bible story, bible movie,
  cinematic bible, old testament), then the brand. 422 of 500 characters.
- Dropped from the old tag list: "bible study for beginners" (the film is not a beginners' course),
  "adam and eve" (Genesis 2 is The Garden's keyword; keep it for that film), "sabbath rest"
  (folded into "sabbath").
- The first description line repeats the title's two keywords in plain words and the second asks
  the two questions the film answers, so search snippets show the hook, not a URL.
- The pinned comment carries the light before the sun hook and a three way choice, which is easier
  to answer than an open reflection question and still points to the study.
