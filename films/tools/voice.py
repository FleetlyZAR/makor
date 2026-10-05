#!/usr/bin/env python3
"""Design candidate GOD voices with ElevenLabs Voice Design and render GOD lines.

  design: one Voice Design call (eleven_ttv_v3) from the brief, with verbatim BSB
          sample text from the study; saves each preview, then saves each preview
          as a voice in the account (POST /v1/text-to-voice).
  render: renders every GOD line from the script's line list in each candidate.

The API key comes only from the macOS Keychain (service makor-elevenlabs). It is
never printed or written to disk. Credits are logged in the film's COSTS.md at
the Creator plan rate.

    python3 films/tools/voice.py design films/genesis/01-the-seven-days
    python3 films/tools/voice.py render films/genesis/01-the-seven-days
    python3 films/tools/voice.py final films/genesis/01-the-seven-days

  final:  renders the film's lines in the chosen voices from films/VOICES.md:
          GOD lines to audio/god/<g>.mp3, NARRATOR lines to audio/narrator/<n>.mp3.
"""
import base64, json, pathlib, re, subprocess, sys, urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from clip import log_cost  # noqa: E402

API = "https://api.elevenlabs.io/v1"
USD_PER_CREDIT = 22 / 131000  # Creator plan: 22 USD a month for 131,000 credits
BRIEF = ("deep, warm, resonant male voice, slow and completely unhurried, authority without volume, "
         "never shouting, clearly different from an American documentary narrator")
# Verbatim BSB, Genesis 1:3 to 5, from the study JSON. Only used to audition the voice.
SAMPLE = ("And God said, “Let there be light,” and there was light. And God saw that the light was good, "
          "and He separated the light from the darkness. God called the light “day,” and the darkness He "
          "called “night.” And there was evening, and there was morning, the first day.")
TTS_MODEL = "eleven_multilingual_v2"


def key():
    return subprocess.run(["security", "find-generic-password", "-s", "makor-elevenlabs", "-w"],
                          capture_output=True, text=True, check=True).stdout.strip()


def post(path, body, k, raw=False):
    req = urllib.request.Request(API + path, data=json.dumps(body).encode(), method="POST",
                                 headers={"xi-api-key": k, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return r.read() if raw else json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"{path}: HTTP {e.code}: {e.read().decode()[:800]}")


def god_lines(script: pathlib.Path):
    for row in script.read_text().splitlines():
        m = re.match(r"\|\s*god/(g\d+)-<voice>\.wav\s*\|\s*GOD\s*\|\s*(.+?)\s*\|$", row)
        if m:
            yield m.group(1), m.group(2)


def design(film: pathlib.Path, k):
    out = film / "audio" / "god"
    out.mkdir(parents=True, exist_ok=True)
    res = post("/text-to-voice/design", {"voice_description": BRIEF, "text": SAMPLE,
                                         "model_id": "eleven_ttv_v3"}, k)
    previews = res.get("previews", [])
    log_cost(film, "ElevenLabs Voice Design (eleven_ttv_v3)", f"{len(previews)} GOD voice previews",
             f"{len(SAMPLE)} credits", len(SAMPLE) * USD_PER_CREDIT)
    cands = []
    for i, p in enumerate(previews, 1):
        (out / f"preview-v{i}.mp3").write_bytes(base64.b64decode(p["audio_base_64"]))
        v = post("/text-to-voice", {"voice_name": f"Makor GOD candidate {i}", "voice_description": BRIEF,
                                    "generated_voice_id": p["generated_voice_id"],
                                    "labels": {"project": "makor-films", "role": "god"}}, k)
        cands.append({"candidate": i, "voice_id": v["voice_id"], "preview": f"audio/god/preview-v{i}.mp3"})
        print(f"candidate {i}: saved voice, preview at audio/god/preview-v{i}.mp3")
    (film / "audio" / "god" / "candidates.json").write_text(json.dumps(cands, indent=2))


def render(film: pathlib.Path, k):
    cands = json.loads((film / "audio" / "god" / "candidates.json").read_text())
    script = film / "script" / "day-01-script.md"
    for c in cands:
        for name, text in god_lines(script):
            audio = post(f"/text-to-speech/{c['voice_id']}?output_format=mp3_44100_192",
                         {"text": text, "model_id": TTS_MODEL}, k, raw=True)
            dest = film / "audio" / "god" / f"{name}-v{c['candidate']}.mp3"
            dest.write_bytes(audio)
            log_cost(film, f"ElevenLabs TTS ({TTS_MODEL})", f"GOD {name} candidate {c['candidate']}",
                     f"{len(text)} credits", len(text) * USD_PER_CREDIT)
            print(f"{dest.relative_to(film)}  {text}")


VOICES = {"GOD": ("bItqJOjNBHK6rbwcdlOT", 0.85), "NARRATOR": ("pRrdgJxlE0SsVTIYEjli", 1.0)}  # films/VOICES.md


def final(film: pathlib.Path, k):
    script = (film / "script" / "day-01-script.md").read_text().splitlines()
    for row in script:
        m = re.match(r"\|\s*(god|narrator)/([gn]\d+)(?:-<voice>)?\.wav\s*\|\s*(GOD|NARRATOR)\s*\|\s*(.+?)\s*\|$", row)
        if not m:
            continue
        folder, name, who, text = m.groups()
        vid, speed = VOICES[who]
        audio = post(f"/text-to-speech/{vid}?output_format=mp3_44100_192",
                     {"text": text, "model_id": TTS_MODEL, "voice_settings": {"speed": speed}}, k, raw=True)
        dest = film / "audio" / folder / f"{name}.mp3"
        dest.write_bytes(audio)
        log_cost(film, f"ElevenLabs TTS ({TTS_MODEL})", f"{who} {name} final",
                 f"{len(text)} credits", len(text) * USD_PER_CREDIT)
        print(f"{dest.relative_to(film)}  {text}")


if __name__ == "__main__":
    cmd, film = sys.argv[1], pathlib.Path(sys.argv[2])
    {"design": design, "render": render, "final": final}[cmd](film, key())
