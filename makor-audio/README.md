# Makor audio (Kokoro, multi-voice)

Turn a Makor study JSON into narrated audio, cut by movement, in four voices,
then play it in a chapter/track player with background play. Free to run
(Kokoro is Apache 2.0), served static from Cloudflare R2.

## Files

    generate_audio.py                    the pipeline (4 voices, pronunciation map)
    pronounce.json                       spoken-form overrides for hard words
    player.html                          chapter/track player (voice chooser, background play)
    sample-study/01-the-seven-days.json  test fixture (truncated Genesis 1:1-2:3)

## Why it is built this way

Studies are permanent, static artifacts. Audio is generated ONCE at build time,
uploaded to R2, and served static. It is never synthesised on a page view, so
cost stays near zero as you scale toward the whole Bible.

## Hear it locally (four voices)

Everything is already installed. WAV output needs nothing extra:

    cd ~/Documents/Developer/makor/makor-audio
    python3 generate_audio.py --study sample-study/01-the-seven-days.json --outdir demo-audio
    python3 -m http.server 8000

Open http://localhost:8000/player.html . Pick a voice, press play, use the
90-second rewind and 30-second forward, skip between sections, and let it run to
the end to see the "day complete, unscored" badge.

Generate a single voice while testing with `--voices af_heart`.

## Pronunciation fixes

Text to speech mispronounces Hebrew names and transliterations, which matters
for Scripture. Add fixes to `pronounce.json`:

    { "Elohim": "Eloheem", "toledot": "toh-leh-DOTE", "Yahweh": "YAH-weh" }

They are applied to the spoken audio only, never to the on-screen study. Run
`--dry-run` to see the spoken text with fixes applied before you render.

## The voices

    af_heart    US, female (default)     am_michael  US, male
    bf_emma     UK, female               bm_george   UK, male

None is South African. If a local accent becomes a priority, the synth step is
isolated so an Azure en-ZA voice can be added without touching the player.

## Production: MP3 + Cloudflare R2

MP3 is essential at scale (about 2 to 3 MB per study per voice versus roughly
17 MB for WAV). Get an encoder without brew:

    pip install imageio-ffmpeg

Then render tagged with your public R2 base, so the manifest holds live URLs:

    python3 generate_audio.py \
      --study src/content/studies/genesis/01-the-seven-days.json \
      --format mp3 --base https://audio.makor.co.za/

Output goes to `public/studies/<book>/<slug>/audio/`. Upload that tree to R2
(one time bucket setup, then repeatable). Using rclone:

    rclone copy public/studies r2:makor-audio/studies --transfers 8

Point a public R2 custom domain (for example audio.makor.co.za) at the bucket.
Do NOT commit the audio into git or the Pages deploy: Cloudflare Pages caps a
deployment at 20,000 files, and the full audio set is far larger.

## Wiring into the Astro renderer

At build time, run the pipeline per study, upload to R2, and let the renderer
read each study's `manifest.json`. The player logic in `player.html` is
framework-agnostic; lift it into an Astro component. The completion hook is
already there: define `window.onMakorListenedThrough(slug)` and wire it to mark
the day complete and unscored in the user's progress. The player also remembers
a listened-through study in localStorage so the badge persists for the reader.

## Cost and timing for the full 1354-study plan

Estimates, assuming about 6 minutes of audio per study (passage plus Basic
layer) and MP3 output.

    Per study, four voices:   about 10 MB, roughly 25 to 50 minutes to render (one time)
    Whole plan, four voices:  about 13.5 GB, about 65,000 files
    R2 storage:               about 20 US cents per month, zero egress fees
    Compute:                  free on your machine

You never render all 1354 at once. You author book by book in waves, so audio is
generated per study as you go, a few minutes each. The only real ongoing duties
are a quick pronunciation-map pass per book and a spot-check listen; full
listening of every voice is not feasible and not necessary, since the text is
your own vetted prose.

## What is licensed and what is not

The audio reads your own study prose and the public-domain BSB, so it is clean to
host. Do NOT cut and rehost copyrighted sermon recordings; keep linking out via
the study's `sermon.url`, as the schema already does.
