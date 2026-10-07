#!/usr/bin/env python3
"""Music auditions for The Seven Days v2: each candidate track under the real voice.

For every cue, each candidate is placed so that its loudest passage lands on the cue's crest
(the set piece BEAT), mixed under the voice with the multiband method from films/SCORING.md
(version C: duck hardest in 1.5 to 5 kHz), and normalised with one fixed gain to -16 LUFS so the
dynamics survive (films/CINEMA-STANDARD.md). Output: edit/audition/<cue>--<candidate>.m4a.

    makor-audio/.venv/bin/python films/genesis/01-the-seven-days-v2/edit/audition_mix.py [cue ...]
"""
import json, pathlib, subprocess, sys

import numpy as np

FILM = pathlib.Path(__file__).resolve().parents[1]
VOICE = FILM / "audio/movement/voice-track.wav"
OUT = FILM / "edit/audition"
MUSIC = FILM / "audio/music-v2"            # Suno themes
PREVIEW = FILM / "audio/music-preview"     # Epidemic low quality previews until WAVs can be downloaded

# cue: (window start, window end, crest time or None, [candidates])
CUES = {
    "02-other-stories": (33.1, 87.2, None, ["river-of-tears", "too-fast", "rivers-collapse"]),
    "03-light": (87.2, 142.4, 115.5, ["theme-light", "nascency", "dissemination", "hour-of-truth"]),
    "05-forming": (204.1, 305.7, 287.8, ["road-less", "tavore"]),
    "09-image": (490.0, 600.0, 517.6, ["theme-image", "monuments", "leave-no-one", "behind-the-moon"]),
    "11-word": (723.8, 808.5, 776.0, ["theme-word", "samudra"]),
    "12-all-new": (808.5, 858.8, 853.8, ["abode-of-snow", "samudra"]),
}


def ff(*a):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *map(str, a)], capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr[-1500:])


def track(name):
    for p in (MUSIC / f"{name}.wav", PREVIEW / f"{name}.mp3"):
        if p.exists():
            return p
    sys.exit(f"missing music: {name}")


def peak_time(path, win=6.0):
    """Centre of the loudest `win` seconds of the track."""
    sr = 4000
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                                     capture_output=True).stdout, np.float32)
    e = np.convolve(x ** 2, np.ones(int(sr * win)) / (sr * win), mode="valid")
    return (int(np.argmax(e)) + sr * win / 2) / sr


def lufs(path):
    r = subprocess.run(["ffmpeg", "-nostats", "-i", str(path), "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    s = r[r.rindex("Summary"):]
    return float(s.split("I:")[1].split("LUFS")[0]), float(s.split("LRA:")[1].split("LU")[0])


def mix(cue, cand):
    a, b, crest, _ = CUES[cue]
    L = b - a
    src = track(cand)
    # place the track: its peak on the crest, or its start at the window start
    shift = (peak_time(src) - (crest - a)) if crest else 0.0        # seconds of track before the window starts
    ss, delay = (shift, 0.0) if shift >= 0 else (0.0, -shift)
    raw = OUT / f"{cue}--{cand}-raw.wav"
    bands = [(2, 0.03), (4, 0.03), (12, 0.02), (2, 0.03)]
    g = (f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{L:.2f},afade=in:d=1.5,"
         f"afade=out:st={max(0, L - delay - 3):.2f}:d=3,adelay={int(delay * 1000)}:all=1,apad=whole_dur={L:.2f},"
         f"volume=0.6,extrastereo=m=1.3,acrossover=split=250 1500 5000:order=8th[b0][b1][b2][b3];"
         f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,apad=whole_dur={L:.2f},asplit[v][key];"
         f"[key]asplit=4[k0][k1][k2][k3];")
    for i, (r, t) in enumerate(bands):
        g += f"[b{i}][k{i}]sidechaincompress=threshold={t}:ratio={r}:attack=25:release=500[d{i}];"
    g += f"[d0][d1][d2][d3]amix=inputs=4:normalize=0[m];[v][m]amix=inputs=2:normalize=0,atrim=0:{L:.2f}[mix]"
    ff("-ss", f"{a}", "-t", f"{L}", "-i", VOICE, "-ss", f"{ss:.2f}", "-i", src, "-filter_complex", g, "-map", "[mix]",
       "-ar", 48000, raw)
    i, lra = lufs(raw)
    out = OUT / f"{cue}--{cand}.m4a"
    ff("-i", raw, "-af", f"volume={-16 - i:.2f}dB,alimiter=limit=0.89:level=false", "-c:a", "aac", "-b:a", "192k", out)
    raw.unlink()
    print(f"{out.name:40s} peak placed {'at crest' if crest else 'from start'} | LRA {lra:4.1f} LU")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for cue in sys.argv[1:] or CUES:
        for cand in CUES[cue][3]:
            mix(cue, cand)
