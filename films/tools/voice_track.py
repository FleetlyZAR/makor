#!/usr/bin/env python3
"""Assemble a movement film's voice track from script/movement-timeline.json:
every line placed at its start time, silence for beats. Writes
audio/movement/voice-track.wav (48 kHz mono) for listening and for the animatic.

    python3 films/tools/voice_track.py films/genesis/01-the-seven-days
"""
import json, pathlib, subprocess, sys, wave

import array

SR = 48000


def pcm(path):
    # each line levelled to the same loudness so Kokoro and ElevenLabs sit together
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-af", "loudnorm=I=-18:LRA=7:TP=-2",
                          "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    return array.array("h", raw)


def main():
    film = pathlib.Path(sys.argv[1])
    tl = json.loads((film / "script" / "movement-timeline.json").read_text())
    out = array.array("h", bytes(2 * int((tl["total"] + 2) * SR)))
    adir = film / "audio" / "movement"
    for e in tl["events"]:
        if e["kind"] != "line":
            continue
        f = next(adir.glob(f"{e['id']}-*"))
        a, start = pcm(f), int(e["t"] * SR)
        out[start:start + len(a)] = a
    dest = adir / "voice-track.wav"
    with wave.open(str(dest), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(out.tobytes())
    print(f"wrote {dest.relative_to(film)}: {tl['total'] / 60:.2f} min")


if __name__ == "__main__":
    main()
