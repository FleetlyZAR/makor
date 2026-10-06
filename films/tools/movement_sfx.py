#!/usr/bin/env python3
"""Sound effects for The Seven Days full film (ElevenLabs Sound Effects).

Writes audio/sfx/movement/<cue>.mp3, skipping cues that exist. Credits are
counted from the prompt lengths' actual usage reported by the account at the
end and logged in COSTS-movement.md. Key from the macOS Keychain only.
The Day One cues in audio/sfx/ (wind, rumble, light swell, room tone) are reused.

    python3 films/tools/movement_sfx.py films/genesis/01-the-seven-days
"""
import json, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from clip import log_cost  # noqa: E402
from sfx import used  # noqa: E402
from voice import USD_PER_CREDIT, key, post  # noqa: E402

NO = "no voices, no music"
CUES = {   # name: (seconds, loop, prompt)
    "storm-sea": (10, False, f"A violent storm over the open sea at night, heavy waves crashing, howling wind, distant rolling thunder, {NO}"),
    "nile-kilns": (12, True, f"A slow river flowing past reeds at dawn, the crackle and roar of brick kilns burning nearby, hot still air, {NO}"),
    "desert-camp": (20, True, f"Soft desert wind over a wide plain, a very distant quiet camp, cloth tents stirring, {NO}, no animals"),
    "lamp-room": (10, True, f"A small oil lamp flame flickering softly in a quiet stone room, near silence, {NO}"),
    "waters-parting": (8, False, f"Deep water lifting and parting with a long soft rushing roar that opens into airy stillness, {NO}"),
    "land-rising": (8, False, f"A deep low rumble of land rising out of the sea, water pouring and draining off rock and earth, {NO}"),
    "grass-wind": (20, True, f"Wind moving through tall grass on open hills above the sea, gentle and steady, distant surf, {NO}, no birds"),
    "night-air": (15, True, f"Quiet night air over a calm bay, faint lapping water, deep stillness, {NO}, no insects, no animals"),
    "whales": (12, False, f"Great whales surfacing in a calm bay, deep breathy blows and spray, distant gentle whale song under water, {NO}"),
    "seabirds": (15, True, f"Seabirds calling over sea cliffs, waves washing against rocks below, open sky, {NO}"),
    "herds": (15, True, f"Herds on open grassland, soft hoofbeats, distant lowing cattle, goats bleating gently, wind in the grass, {NO}"),
    "meadow-birds": (15, True, f"Small birds singing in a sunlit meadow, insects humming softly, gentle breeze, {NO}"),
    "golden-stillness": (20, True, f"Near silence on a warm still evening by a calm sea, the softest air, utterly peaceful, {NO}"),
    "flood": (10, False, f"Rising flood waters heaving and roaring over land, heavy rain and storm wind, {NO}"),
    "new-creation": (15, True, f"A bright airy shimmer of warm air over a clear flowing river, peaceful and radiant, soft high tones of wind, {NO}"),
    "garden-dawn": (12, True, f"A quiet garden at first light, a few distant early birds, dew, deep stillness, {NO}"),
    "single-flame": (8, True, f"A single candle flame burning steadily in a silent dark room, faint soft flutter, {NO}"),
    "river-stones": (15, True, f"A clear stream flowing over smooth stones, gentle and bright, {NO}"),
    "thorn-wind": (12, True, f"A dry cold wind through dead thorn bushes on bare ground, desolate, {NO}"),
}


def main():
    film = pathlib.Path(sys.argv[1])
    cues_f = film / "sfx-cues.json"   # a film's own cue list; The Seven Days uses the CUES above
    cues = {k: tuple(v) for k, v in json.loads(cues_f.read_text()).items()} if cues_f.exists() else CUES
    out = film / "audio" / "sfx" / "movement"
    out.mkdir(parents=True, exist_ok=True)
    k = key()
    before = used(k)
    made = 0
    for name, (secs, loop, text) in cues.items():
        dest = out / f"{name}.mp3"
        if dest.exists():
            continue
        body = {"text": text, "duration_seconds": secs, "loop": loop, "prompt_influence": 0.5,
                "model_id": "eleven_text_to_sound_v2"}
        dest.write_bytes(post("/sound-generation?output_format=mp3_44100_192", body, k, raw=True))
        made += 1
        print(f"{name}: {secs} s", flush=True)
    credits = max(0, used(k) - before)
    if made:
        log_cost(film, "ElevenLabs Sound Effects (eleven_text_to_sound_v2)", f"{made} movement sfx cues",
                 f"{credits} credits reported (counter lags)", credits * USD_PER_CREDIT, log="COSTS-movement.md")
    print(f"done: {made} cues, {credits} credits reported so far")


if __name__ == "__main__":
    main()
