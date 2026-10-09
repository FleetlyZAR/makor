#!/usr/bin/env python3
"""The Seven Days v2: full score, sound design and mix, on the voice timeline.

Music (audio/music-v2, Epidemic Sound and the Suno themes) is placed cue by cue, each track's
loudest passage on its crest where the cue has one. Sound design (audio/sfx, designed hits from
Epidemic) and ambience beds (v1's library) are placed by time. The mix follows films/SCORING.md
(version C: the music ducks by band, hardest in 1.5 to 5 kHz) and films/CINEMA-STANDARD.md
(master at -16 LUFS with one fixed gain, true peak about -1 dBFS, so the set pieces keep their lift).
Times are on the voice timeline (script/movement-timeline.json); the edit adds its own lead.

    makor-audio/.venv/bin/python films/genesis/01-the-seven-days-v2/edit/score_mix.py
writes edit/score/mix.wav, music.wav (music and effects only) and mix.m4a for listening.
"""
import json, pathlib, subprocess, sys

import numpy as np

FILM = pathlib.Path(__file__).resolve().parents[1]
V1 = FILM.parent / "01-the-seven-days"
MUSIC, SFX = FILM / "audio/music-v2", FILM / "audio/sfx"
AMB = V1 / "audio/sfx"
OUT = FILM / "edit/score"
T = json.loads((FILM / "script/movement-timeline.json").read_text())
TOTAL = T["total"]

# (track, start, end, crest or None, volume, fade in, fade out[, seek seconds into the track])
# Consecutive cues overlap and crossfade; a track never runs out before its scene (checked below).
CUES = [
    ("last-frontier", 4.0, 26.4, None, 0.9, 0.6, 5.0, 109.26),  # the burst (its hit at 110.3 s lands on 5.04), the
                                                            # starlight, the dive and history; then a 5 s fade under the
                                                            # pull back and the spark, into the track's own dip at 131.5 s
                                                            # (no hard stop: Luyanda, 9 October)
    ("river-of-tears", 23.4, 88.4, None, 0.55, 3.0, 4.0, 37.0),  # Egypt and the other stories; fades before its second break
    ("dissemination", 100.8, 152.0, 127.3, 0.6, 1.5, 4.0),  # In the beginning: crest on the light
    ("himalayan-moon", 147.0, 218.6, None, 0.45, 4.0, 3.0), # formless and void, teaching (crossfades in, no gap)
    ("road-less", 216.0, 304.8, 301.8, 0.6, 3.0, 2.0),      # forming montage, stops dead on the empty world
    ("wonder-of-a-child", 319.7, 397.5, None, 0.6, 1.0, 3.0),  # the first sunrise
    ("overcome", 395.0, 463.6, 417.0, 0.6, 3.0, 1.5),       # the sea teems, crest on the breach
    ("forest-run", 462.6, 496.6, None, 0.65, 1.0, 2.0),     # herds; cut to nothing for "Then the pattern breaks"
    ("monuments", 503.0, 568.0, 528.3, 0.7, 4.0, 5.0),      # Let Us make man: crest on the man and the woman
    ("theme-image", 562.0, 662.0, None, 0.5, 5.0, 4.0),     # the human theme: the brick-maker, the fields, very good
    ("himalayan-moon", 659.0, 739.0, None, 0.3, 5.0, 3.0, 111.0),  # rest: a low pulse, in under the fade (no 6 s gap)
    ("samudra", 736.5, 818.5, 790.0, 0.6, 3.0, 4.0),        # In the beginning was the Word: crest on the empty tomb
    ("abode-of-snow", 815.0, 873.5, 867.8, 0.6, 4.0, 3.0),  # all things new
    ("theme-word", 871.5, TOTAL, 884.0, 0.55, 2.5, 4.0),    # light in a dark place, the light theme returns
]

# designed hits, never ducked: (file, time, volume[, seconds into the file])
HITS = [
    ("drop", 3.0, 1.0), ("bang", 5.04, 1.0),   # God speaks in the black, then the drop, then the burst
    # the expansion, sound designed to the picture: a riser peaking on the burst, a big boom with it, starlight
    # flying past, a low hit on the earth, the wind of the atmosphere peaking in the clouds
    ("riser", 1.0, 0.9, 2.6), ("boom-big", 4.46, 1.0),
    ("flyby1", 7.62, 0.7), ("flyby3", 8.47, 0.6), ("flyby2", 8.51, 0.55),
    ("hit", 9.8, 0.45), ("windrush", 8.55, 0.7),
    ("rewind", 17.5, 0.8), ("hit", 43.1, 0.8),
    ("drop", 123.4, 0.9), ("hit", 127.3, 0.7),               # Day One: the opening's drop returns, then the break
    ("hit", 528.3, 0.6), ("hit", 790.0, 0.6), ("hit", 867.8, 0.5),
] + [("whoosh", t, 0.25) for t in (14.0, 16.5)] \
  + [("whoosh", t, 0.35) for t in (288.0, 292.0, 296.0)] \
  + [("hit", t, 0.35) for t, n in T["chapters"] if n not in ("Cold open", "In the beginning")]

# ambience beds from v1's library, ducked lightly: (file under v1 audio/sfx, start, end, volume)
BEDS = [
    ("movement/nile-kilns.mp3", 23.4, 100.2, 0.45), ("wind-deep-water.mp3", 86.0, 100.2, 0.35), ("wind-deep-water.mp3", 101.2, 129.0, 0.35),
    ("movement/waters-parting.mp3", 218.1, 260.0, 0.3), ("movement/land-rising.mp3", 260.0, 304.8, 0.3),
    ("movement/grass-wind.mp3", 304.0, 319.7, 0.35), ("movement/meadow-birds.mp3", 319.7, 396.5, 0.2), ("movement/whales.mp3", 396.5, 463.1, 0.3),
    ("movement/seabirds.mp3", 425.0, 463.1, 0.25), ("movement/herds.mp3", 463.1, 496.6, 0.35),
    ("movement/garden-dawn.mp3", 495.0, 560.0, 0.6), ("movement/golden-stillness.mp3", 655.0, 740.0, 0.7),
    ("movement/single-flame.mp3", 737.8, 770.0, 0.25), ("movement/new-creation.mp3", 822.5, 872.8, 0.3),
    ("room-tone-calm-sea.mp3", 872.8, TOTAL, 0.25),
]


def ff(*a):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *map(str, a)], capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr[-2500:])


def peak_time(path, win=6.0):
    sr = 4000
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                                     capture_output=True).stdout, np.float32)
    e = np.convolve(x ** 2, np.ones(int(sr * win)) / (sr * win), mode="valid")
    return (int(np.argmax(e)) + sr * win / 2) / sr


def dur(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                                capture_output=True, text=True).stdout)


def lufs(path):
    r = subprocess.run(["ffmpeg", "-nostats", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    s = r[r.rindex("Summary"):]
    return (float(s.split("I:")[1].split("LUFS")[0]), float(s.split("LRA:")[1].split("LU")[0]),
            float(s.split("Peak:")[1].split("dBFS")[0]))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    ins, fc, mus, beds, hits = ["-i", str(FILM / "audio/movement/voice-track.wav")], [], [], [], []
    n = 1
    st = "aformat=sample_rates=48000:channel_layouts=stereo"
    for cue in CUES:
        name, a, b, crest, vol, fi, fo = cue[:7]
        src = MUSIC / f"{name}.wav"
        shift = (peak_time(src) - (crest - a)) if crest else (cue[7] if len(cue) > 7 else 0.0)
        ss, start = (shift, a) if shift >= 0 else (0.0, a - shift)
        L = b - start
        left = dur(src) - ss
        if left < L - 0.5:
            print(f"WARNING {name}: track runs out {L - left:.1f} s before its cue ends at {b:.1f}")
        ins += ["-ss", f"{ss:.2f}", "-i", str(src)]
        fc.append(f"[{n}:a]{st},atrim=0:{L:.2f},afade=in:d={fi},afade=out:st={max(0, L - fo):.2f}:d={fo},"
                  f"volume={vol},adelay={int(start * 1000)}:all=1[m{n}]")
        mus.append(f"[m{n}]"); n += 1
        print(f"music {name:18s} {start:6.1f} to {b:6.1f}" + (f"  peak on {crest}" if crest else ""))
    for f, a, b, vol in BEDS:
        L = b - a
        ins += ["-stream_loop", "-1", "-i", str(AMB / f)]
        fc.append(f"[{n}:a]{st},atrim=0:{L:.2f},afade=in:d=1.5,afade=out:st={max(0, L - 1.5):.2f}:d=1.5,"
                  f"volume={vol},adelay={int(a * 1000)}:all=1[a{n}]")
        beds.append(f"[a{n}]"); n += 1
    for f, t, vol, *seek in HITS:
        ins += (["-ss", f"{seek[0]}"] if seek else []) + ["-i", str(SFX / f"{f}.wav")]
        fc.append(f"[{n}:a]{st},volume={vol},adelay={int(t * 1000)}:all=1[h{n}]")
        hits.append(f"[h{n}]"); n += 1
    pad = f"apad=whole_dur={TOTAL:.2f}"
    fc.append(f"{''.join(mus)}amix=inputs={len(mus)}:normalize=0,{pad},extrastereo=m=1.3,"
              f"acrossover=split=250 1500 5000:order=8th[b0][b1][b2][b3]")
    fc.append(f"{''.join(beds)}amix=inputs={len(beds)}:normalize=0,{pad}[beds]")
    fc.append(f"{''.join(hits)}amix=inputs={len(hits)}:normalize=0,{pad}[hits]")
    fc.append(f"[0:a]{st},{pad},asplit[v][key]")
    fc.append("[key]asplit=5[k0][k1][k2][k3][k4]")
    for i, (r, t) in enumerate([(2, 0.03), (4, 0.03), (12, 0.02), (2, 0.03)]):
        fc.append(f"[b{i}][k{i}]sidechaincompress=threshold={t}:ratio={r}:attack=25:release=500[d{i}]")
    fc.append("[d0][d1][d2][d3]amix=inputs=4:normalize=0[musd]")
    fc.append("[beds][k4]sidechaincompress=threshold=0.04:ratio=2:attack=30:release=600[bedsd]")
    fc.append("[musd][bedsd][hits]amix=inputs=3:normalize=0,asplit[score][score2]")
    fc.append(f"[v][score]amix=inputs=2:normalize=0,atrim=0:{TOTAL:.2f}[mix]")
    raw, music = OUT / "mix-raw.wav", OUT / "music.wav"
    graph = OUT / "graph.txt"
    graph.write_text(";".join(fc))
    ff(*ins, "-/filter_complex", graph, "-map", "[mix]", "-ar", 48000, raw, "-map", "[score2]", "-ar", 48000, music)
    i, lra, pk = lufs(raw)
    gain = -16 - i
    ff("-i", raw, "-af", f"volume={gain:.2f}dB,alimiter=limit=0.79:level=false:attack=5:release=80", "-ar", 48000,
       OUT / "mix.wav")
    ff("-i", OUT / "mix.wav", "-c:a", "aac", "-b:a", "192k", OUT / "mix.m4a")
    i2, lra2, pk2 = lufs(OUT / "mix.wav")
    raw.unlink()
    print(f"mix: {i2:.1f} LUFS, loudness range {lra2:.1f} LU, true peak {pk2:.1f} dBFS -> {OUT / 'mix.m4a'}")


if __name__ == "__main__":
    main()
