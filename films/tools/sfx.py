#!/usr/bin/env python3
"""Generate a Makor film's sound effects with ElevenLabs Sound Effects.

Each cue is one call to POST /v1/sound-generation (eleven_text_to_sound_v2).
Credits are measured from the subscription before and after each call and
logged in the film's COSTS.md. Key from the macOS Keychain only.

    python3 films/tools/sfx.py films/genesis/01-the-seven-days [cue ...]
"""
import json, pathlib, sys, urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from clip import log_cost  # noqa: E402
from voice import API, USD_PER_CREDIT, key, post  # noqa: E402

# Day One cues. Prompts describe sound only: no voices, no music, no choirs.
CUES = {
    "wind-deep-water": dict(duration_seconds=22, loop=True, prompt_influence=0.5, text=(
        "Wind moving low across a vast dark open ocean at night, soft steady breath of air over the "
        "water with slow long gusts, gentle hiss of fine spray, deep slow swells lapping, wide and "
        "empty, no birds, no voices, no thunder, no rain, no music")),
    "rumble-under-god": dict(duration_seconds=6, loop=False, prompt_influence=0.5, text=(
        "Very deep, soft sub bass rumble that slowly swells and fades, like vast distant pressure "
        "deep below the sea, warm and steady, no thunder crack, no impact, no music, no voices")),
    "light-swell": dict(duration_seconds=6, loop=False, prompt_influence=0.5, text=(
        "Soft warm airy swell rising gently over four seconds into a bright, open shimmer of air, "
        "then settling and fading, cinematic but restrained, no whoosh, no impact, no bells, no "
        "choir, no voices, no melody")),
    "room-tone-calm-sea": dict(duration_seconds=30, loop=True, prompt_influence=0.5, text=(
        "Very quiet calm open sea ambience, soft distant waves and gentle air, almost silent and "
        "still, no wind gusts, no birds, no boats, no voices, no music")),
}


def used(k):
    req = urllib.request.Request(API + "/user/subscription", headers={"xi-api-key": k})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)["character_count"]


def main():
    film = pathlib.Path(sys.argv[1])
    names = sys.argv[2:] or list(CUES)
    out = film / "audio" / "sfx"
    out.mkdir(parents=True, exist_ok=True)
    k = key()
    for name in names:
        before = used(k)
        body = dict(CUES[name], model_id="eleven_text_to_sound_v2")
        audio = post("/sound-generation?output_format=mp3_44100_192", body, k, raw=True)
        (out / f"{name}.mp3").write_bytes(audio)
        credits = used(k) - before
        log_cost(film, "ElevenLabs Sound Effects (eleven_text_to_sound_v2)",
                 f"sfx {name} ({body['duration_seconds']} s)", f"{credits} credits", credits * USD_PER_CREDIT)
        print(f"audio/sfx/{name}.mp3  {credits} credits")


if __name__ == "__main__":
    main()
