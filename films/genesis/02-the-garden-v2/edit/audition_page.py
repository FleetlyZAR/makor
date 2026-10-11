#!/usr/bin/env python3
"""Build script/music-audition.html: the Epidemic Sound shortlist for every cue of The Garden v2,
with previews, each track's energy arc and a link to its Epidemic page for the download.
Picks were made by hand from edit/audition/candidates.json (audition_search.py) and a few
extra searches for the film's colour (flute, harp, Middle Eastern strings and qanun).

    python3 films/genesis/02-the-garden-v2/edit/audition_page.py
"""
import html, json, pathlib, urllib.parse

from audition_search import arc, get

FILM = pathlib.Path(__file__).resolve().parents[1]

# (cue, time in the film, what it needs, [(title, artist, why)])
PICKS = [
    ("1. Cold open", "0:00 to 0:17", "The fall from the sky, the first breath, the driving montage, then cut dead for God's line.", [
        ("On the Brink of Glory", "Dian Shuai", "cello and strings, restless and epic, climbs all the way"),
        ("Flying to the Summit", "Siddharth", "big hopeful orchestra, long plateau at full height"),
        ("Temple Dawn", "Stefan Ekström", "elegant build to a broad peak, then falls away"),
        ("Hope Takes Flight", "Jo Wandrini", "starts from near nothing, brass and strings saga"),
    ]),
    ("2. The camp at night", "0:22 to 0:46", "The wilderness camp, the tabernacle's fire, the hook, into the title. Ancient, a little mysterious.", [
        ("Crying Winds", "Deskant", "desert ambient, distant horizon, dark and still"),
        ("Forgotten Shores", "Rymdklang", "Middle Eastern, mysterious, moves gently"),
        ("Dunes of Despair", "Deskant", "desert winds at night, low tension"),
    ]),
    ("3. Down to the ground", "0:45 to 1:41", "A curious pulse under the teaching and the nine verbs on screen; room for the voice.", [
        ("Midst of Life", "Christoffer Moe", "staccato strings, hopeful, a steady forward pulse"),
        ("Absens", "Christoffer Moe", "small ensemble: cello, clarinet, staccato violin; even and light"),
        ("Ducere", "Christoffer Moe", "cello, flute and strings, playful pulse"),
        ("Profound", "Gavin Luke", "contemporary classical, mysterious, two waves"),
    ]),
    ("4. The breath (set piece)", "1:39 to 2:44, crest on 2:32", "Lack, the springs, the forming; from near silence to the film's first immense warm crest.", [
        ("Imminent End", "Christoffer Moe", "long patient build, peak late (the same composer as Nascency, the temp)"),
        ("Open Fields", "Johan Landqvist", "oboe, piano and strings; quiet, then a big romantic lift"),
        ("Eternal Sunrise", "Victor Lundberg", "slow even climb to an uplifting peak"),
        ("Solace", "Christoffer Moe", "cello and orchestra, sentimental, rises from nothing near the end"),
    ]),
    ("5. A garden in the east", "3:25 to 4:11", "Time-lapse growth to the two trees. The Garden's colour: flute and harp.", [
        ("Winds of Aetheria", "Dian Shuai", "flute, harp and folk strings, a gentle build"),
        ("Vagabond's Awakening", "Dian Shuai", "harp leading into an orchestral build"),
        ("Azalea's River", "Rachel Sandy", "cello and flute, hopeful, dreamy"),
        ("Just Above the Clouds", "Jay Taylor", "flute over strings, rises to a bright middle"),
    ]),
    ("6. Four rivers (set piece)", "4:09 to 5:27, crest on 4:58", "Speed and scale: the river breaking into four from the air. The second peak.", [
        ("Crowned Kings", "Dream Cave", "aerial, overland, epic; tagged for exactly this kind of shot"),
        ("Adventures Ahead", "Christoffer Moe", "majestic brass and strings, a long build"),
        ("Eternal Odyssey", "Christoffer Moe", "epic, hopeful, steady climb to a big top"),
    ]),
    ("7. The sanctuary", "5:34 to 6:59", "The camp at sunrise, the gate facing east, the priest, the Levite. Ancient and reverent.", [
        ("Desert Bloom", "Mukryan", "Middle Eastern orchestral, hopeful and peaceful"),
        ("Valley of Ela", "Rymdklang", "Middle Eastern, hopeful, dreamy (named for the valley of Elah)"),
        ("The Sun and the Crescent Moon", "Mukryan", "Iraqi maqam with orchestra, broad and hopeful"),
        ("Ana", "Feras", "solo qanun, peaceful and intimate"),
    ]),
    ("8. One word", "7:17 to 8:17", "After God's warning: one held tone, stillness with a trace of tension.", [
        ("Woodwind Reviere", "Daniella", "dark woodwind drone, floating"),
        ("Lay Down with Me", "Hanna Lindgren", "low drones, mysterious, very still"),
        ("The Big Transformation", "August Wilhelmsson", "light tension, slowly growing"),
    ]),
    ("9a. Not good", "8:17 to 8:57", "The man alone at evening; lonely, sparse. (The temp has no music here, only wind.)", [
        ("Felt Like November", "Magnus Ludvigsson", "solo piano, lonely, calm"),
        ("Yoiyami", "Sayuri", "sparse solo piano, quiet and lonely"),
        ("Into the Divide", "Trevor Kowalski", "sparse piano, storytelling, a little mysterious"),
    ]),
    ("9b. The naming", "8:57 to 9:33", "Driving montage of the animals, stops dead on the man alone.", [
        ("Momentum: I. Quake", "Dian Shuai", "string ensemble, dramatic, chasing"),
        ("With Tenacity", "Christoffer Moe", "staccato strings building to an epic top"),
        ("Momentum: II. Sparkle", "Dian Shuai", "cello and violin, upbeat and hopeful"),
    ]),
    ("10. Bone of my bones (set piece)", "9:44 to 10:49, crest on 10:39", "Night, the deep sleep, then morning and the woman brought to him: the warmest peak in the film.", [
        ("Mirroring", "Christoffer Moe", "oboe and strings, wondrous; quiet for a long time, then blooms"),
        ("Consensus", "Christoffer Moe", "cello, oboe, piano; romantic build to a full orchestra"),
        ("Multiply It by Infinity", "Kevin Dailey", "chamber strings, romantic, a long swell"),
        ("Niveus", "Christoffer Moe", "hopeful, sentimental, rises in the middle"),
    ]),
    ("11. One flesh", "11:00 to 12:06", "The brick-maker's home; tender. The temp uses the human theme from The Seven Days, which could stay.", [
        ("Into Open Arms", "Hanna Ekström", "piano trio with cello and violin, folk and warm (tagged weddings)"),
        ("Reflection of the Sun", "Anna Landström", "cello, piano and strings, romantic and hopeful"),
        ("Safe and Sound", "Anna Landström", "delicate piano and strings, tender"),
    ]),
    ("12. The last Adam", "12:11 to 13:28, crest on 13:00", "Reverent build to the empty tomb. The temp is Samudra, the track The Seven Days used at its tomb; keeping it is a deliberate echo.", [
        ("Breath by Breath", "Helmut Schenker", "beautiful slow build, and the title is the film's own image"),
        ("Renewal", "Aerian", "piano and strings, light rising to a peak"),
        ("The Atom", "Christoffer Moe", "hopeful orchestral build, peaks late"),
    ]),
    ("13a. Chapter three, flash-forward", "13:28 to 13:54", "Thorns, toil, the flaming sword: dark and fast.", [
        ("Ashes of All", "Stefan Ekström", "dark suspense, a single heavy build"),
        ("The Beginning of the End", "Stefan Ekström", "dark, ominous, long plateau"),
    ]),
    ("13b. Eden restored (set piece)", "13:50 to 14:38, crest on 14:23", "The city with the river and the tree of life: radiant.", [
        ("The Sky Remembers Us", "Jo Wandrini", "majestic violins, soaring, hopeful"),
        ("Kingdom of Pride", "Dian Shuai", "horns and strings, epic and sentimental"),
        ("Foretold", "Laura Platt", "epic, hopeful, dreamy"),
    ]),
    ("14. Dust that breathes", "14:35 to 15:06", "The close: quiet resolution before the open loop.", [
        ("Before We Were", "Jakob Ahlbom", "cello, piano and violin; peaceful, then one last swell"),
        ("Whispering Horizon", "Victor Lundberg", "piano and violin, moving, rises from nothing"),
        ("Kairos", "Aerian", "cello, piano and violin, quiet and reflective"),
    ]),
]


def find(title, artist):
    res = get("https://www.epidemicsound.com/json/search/tracks/?" +
              urllib.parse.urlencode({"term": f"{title} {artist}", "limit": 10}))
    for t in res["entities"]["tracks"].values():
        names = " ".join(a["name"] for a in t["creatives"]["mainArtists"])
        if t["title"].lower() == title.lower() and artist.lower() in names.lower():
            return t, names
    raise SystemExit(f"not found: {title} / {artist}")


def main():
    css = """:root{--bg:#f6f1e7;--ink:#14302f;--muted:#5b6b67;--card:#fffdf8;--line:#e2d8c4;--gold:#a87b2c}
@media (prefers-color-scheme:dark){:root{--bg:#0f1c1c;--ink:#efe6d4;--muted:#9fb0aa;--card:#16292a;--line:#26403f;--gold:#d6aa5c}}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 -apple-system,system-ui,sans-serif;padding:16px}
main{max-width:820px;margin:auto} h1{font-family:Georgia,serif;font-weight:600} h2{font-family:Georgia,serif;font-weight:600;color:var(--gold);margin:28px 0 0}
.when{color:var(--muted);font-size:13px;margin:0} .note{color:var(--muted);margin:4px 0 10px}
.cand{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px;margin:8px 0;display:grid;gap:8px}
.meta span{color:var(--muted)} .arc{font-family:ui-monospace,monospace;letter-spacing:1px;color:var(--gold);overflow:hidden}
.why{color:var(--muted);font-size:13px} a{color:var(--gold)} audio{width:100%}"""
    out = [f"<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
           f"<title>Garden v2 Music Audition</title><style>{css}</style></head><body><main>"
           "<h1>The Garden v2: music audition</h1>"
           "<p class='note'>Epidemic Sound previews (low quality). The bars show each track's energy from start to end. "
           "Tell me one pick per cue (or keep the temp); download the WAV with stems from the track's page, name it after "
           "the cue (for example <code>g-04.wav</code>, stems <code>g-04-strings.wav</code>) in "
           "<code>films/genesis/02-the-garden-v2/audio/music/</code>, and I cut it to picture.</p>"]
    for cue, when, need, picks in PICKS:
        out.append(f"<section><h2>{html.escape(cue)}</h2><p class='when'>{when}</p><p class='note'>{html.escape(need)}</p>")
        for title, artist, why in picks:
            t, names = find(title, artist)
            full = t["stems"]["full"]
            bars = arc(full["waveformUrl"])
            mins = f"{t['length'] // 60}:{t['length'] % 60:02d}"
            out.append(f"<div class='cand'><div class='meta'><strong>{html.escape(t['title'])}</strong> "
                       f"<span>{html.escape(names)} · {mins}</span><div class='arc'>{bars}</div>"
                       f"<div class='why'>{html.escape(why)} · <a href='https://www.epidemicsound.com/track/{t['publicSlug']}/' "
                       f"target='_blank' rel='noopener'>open on Epidemic</a></div></div>"
                       f"<audio controls preload='none' src='{full['lqMp3Url']}'></audio></div>")
            print(f"{cue[:28]:28s} {t['title']}")
        out.append("</section>")
    out.append("</main></body></html>")
    (FILM / "script/music-audition.html").write_text("".join(out))
    print("->", FILM / "script/music-audition.html")


if __name__ == "__main__":
    main()
