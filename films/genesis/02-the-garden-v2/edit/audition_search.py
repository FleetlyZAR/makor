#!/usr/bin/env python3
"""Search Epidemic Sound's public catalogue for each cue in ../TREATMENT.md and write
edit/audition/candidates.json (title, artist, tags, preview url, an energy arc from the
waveform). Free; no account needed for previews. Picks are made by hand from the result
and the page is built by audition_page.py.

    python3 films/genesis/02-the-garden-v2/edit/audition_search.py
"""
import json, pathlib, urllib.parse, urllib.request

FILM = pathlib.Path(__file__).resolve().parents[1]
OUT = FILM / "edit/audition"
UA = {"User-Agent": "Mozilla/5.0"}
BARS = "▁▂▃▄▅▆▇█"

# cue: (seconds needed, queries)
CUES = {
    "01 cold open": (20, ["epic orchestral rise", "cinematic awe build", "epic emotional orchestral"]),
    "02 camp at night": (30, ["ancient middle east mysterious", "ney flute night", "desert ambient mysterious"]),
    "03 down to the ground": (60, ["documentary curious strings", "pizzicato underscore", "documentary pulse wonder"]),
    "04 the breath": (70, ["awe build strings", "cinematic swell emotional build", "creation awe orchestral"]),
    "05 a garden in the east": (50, ["flute harp hopeful", "wonder flute strings", "nature wonder orchestral"]),
    "06 four rivers": (85, ["epic adventure orchestral", "soaring cinematic flight", "majestic aerial orchestral"]),
    "07 the sanctuary": (90, ["ney flute meditative", "ancient middle eastern reverent", "oud frame drum ancient"]),
    "08 one word": (65, ["sustained drone stillness", "minimal tension ambient strings", "reverent ambient pad"]),
    "09 not good and the naming": (80, ["lonely piano", "driving strings ostinato", "adventure strings driving"]),
    "10 bone of my bones": (70, ["tender love orchestral swell", "romantic cinematic emotional", "intimate strings climax"]),
    "11 one flesh": (70, ["warm intimate cello piano", "tender harp", "gentle folk warm"]),
    "12 the last adam": (80, ["reverent hope build", "resurrection hope piano strings", "emotional piano strings build"]),
    "13 eden restored": (75, ["triumphant radiant orchestral", "hopeful epic finale", "dark tension cinematic"]),
    "14 close": (40, ["calm reflective piano", "peaceful resolution strings", "warm reflective harp"]),
}
NO_GENRE = {"Hip Hop", "Beats", "Pop", "Rock", "Electronica", "EDM", "Trap", "Funk", "Jazz", "Country", "Blues",
            "Dance", "Drum and Bass", "Lofi", "Lo-Fi Hip Hop", "Indie Pop", "Reggae", "Latin"}
NO_TAG = {"guitar", "electric guitar", "drum kit", "drums", "snare", "hi-hat", "synth", "synthesizer", "choir",
          "vocals", "beat", "808", "bass guitar", "arpeggiator"}


def get(url):
    return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read())


def arc(wurl, n=23):
    try:
        d = get(wurl)["data"]
    except Exception:
        return ""
    amp = [max(abs(d[i]), abs(d[i + 1])) for i in range(0, len(d) - 1, 2)]
    k = max(1, len(amp) // n)
    seg = [sum(amp[i:i + k]) / k for i in range(0, k * n, k)]
    top = max(seg) or 1
    return "".join(" " if s < top * 0.06 else BARS[min(7, int(s / top * 8))] for s in seg)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    out, seen = {}, set()
    for cue, (need, qs) in CUES.items():
        rows = []
        for q in qs:
            res = get("https://www.epidemicsound.com/json/search/tracks/?" + urllib.parse.urlencode({"term": q, "limit": 25}))
            for t in res["entities"]["tracks"].values():
                genres = {g["displayTag"] for g in t["genres"]} | {g["fatherTag"] for g in t["genres"]}
                tags = {x.lower() for x in t.get("metadataTags") or []}
                if (t["hasVocals"] or t["isSfx"] or t["hidden"] or t["length"] < need or genres & NO_GENRE
                        or tags & NO_TAG or t["id"] in seen):
                    continue
                seen.add(t["id"])
                full = t["stems"].get("full", {})
                rows.append({"id": t["id"], "title": t["title"], "q": q,
                             "artist": ", ".join(a["name"] for a in t["creatives"]["mainArtists"]),
                             "length": t["length"], "bpm": t["bpm"], "energy": t["energyLevel"],
                             "genres": sorted(g["displayTag"] for g in t["genres"]),
                             "moods": [m["displayTag"] for m in t["moods"]], "tags": sorted(tags),
                             "stems": sorted(t["stems"]), "preview": full.get("lqMp3Url"),
                             "waveform": full.get("waveformUrl"), "slug": t["publicSlug"]})
        for r in rows:
            r["arc"] = arc(r["waveform"]) if r["waveform"] else ""
        out[cue] = rows
        print(f"{cue}: {len(rows)} candidates")
    (OUT / "candidates.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
