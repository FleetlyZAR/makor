#!/usr/bin/env python3
"""The Garden v2: TEMP score, sound design and mix for the animatic, on the voice timeline.

Built the way The Seven Days v2 was (`01-the-seven-days-v2/edit/score_mix.py`): one cue per
turn of the story, each set piece's crest landed on its peak, music above the voice only in the
set pieces, hard drops before the key lines, a low hit on every chapter card, designed hits and
ambience beds placed by time. Mix per films/SCORING.md version C (the music ducks by band,
hardest in 1.5 to 5 kHz) and films/CINEMA-STANDARD.md (master at -16 LUFS, one fixed gain).

TEMP: the music is borrowed from The Seven Days v2 library (mostly the Epidemic tracks that were
auditioned but not used there) so the pacing can be judged now. The Garden's own cues (ney flute
and harp colour, films/SCORING.md) replace them from the cue sheet in ../TREATMENT.md.

    makor-audio/.venv/bin/python films/genesis/02-the-garden-v2/edit/score_mix.py
writes edit/score/mix.wav, music.wav (music and effects only) and mix.m4a, and
exports/movement-animatic-scored.mp4 (the animatic picture with this mix).
"""
import json, pathlib, subprocess, sys

import numpy as np

FILM = pathlib.Path(__file__).resolve().parents[1]
GEN = FILM.parent
MUSIC = GEN / "01-the-seven-days-v2/audio/music-v2"
OUT = FILM / "edit/score"
T = json.loads((FILM / "script/movement-timeline.json").read_text())
TOTAL = T["total"]

# (track, start, end, crest or None, volume, fade in, fade out[, seek seconds into the track])
CUES = [
    ("rivers-collapse", 0.0, 17.2, None, 0.85, 0.3, 0.3, 20.0),  # the fall, the breath, the montage; cut dead for God
    ("too-fast", 22.0, 46.0, None, 0.5, 2.0, 3.0),               # the camp at night, the hook, into the title
    ("tavore", 45.0, 101.5, None, 0.45, 2.0, 3.0),               # down to the ground: the verbs
    ("nascency", 99.0, 163.5, 152.0, 0.75, 4.0, 4.0),            # lack, springs, the forming: crest on the breath
    ("theme-image", 161.0, 207.0, None, 0.45, 3.0, 3.0),         # the human theme: the brick-maker's hands in dust
    ("behind-the-moon", 204.5, 251.0, None, 0.6, 2.0, 2.5),      # a garden in the east: growth to the two trees
    ("hour-of-truth", 248.5, 327.4, 298.0, 0.75, 2.0, 5.0),      # four rivers: crest on the set piece; the track ends at 327, the river bed carries to the cut
    ("river-of-tears", 333.6, 419.0, None, 0.5, 1.0, 3.0, 37.0), # the sanctuary and the Levite: ancient, reverent
    ("himalayan-moon", 437.0, 497.0, None, 0.35, 4.0, 3.0),      # one word: in after the warning, the slow pulse
    ("forest-run", 537.5, 572.6, None, 0.65, 1.5, 0.3),          # the naming montage; stops dead on the man alone
    ("leave-no-one", 584.0, 648.5, 639.0, 0.75, 5.0, 3.0),       # night, the sleep, the woman brought: the warmest peak
    ("theme-image", 659.5, 726.0, None, 0.45, 3.0, 4.0, 40.0),   # one flesh: the brick-maker's home; darkens on the tree
    ("samudra", 731.0, 808.5, 780.0, 0.6, 3.0, 2.0),             # the last Adam: crest on the empty tomb (as in The Seven Days)
    ("too-fast", 808.0, 834.0, None, 0.6, 0.5, 3.0, 40.0),       # dark flash-forward to chapter three
    ("abode-of-snow", 830.0, 878.0, 863.0, 0.65, 3.0, 4.0),     # Eden restored: crest on the city
    ("theme-word", 875.0, 906.0, None, 0.5, 2.5, 3.0),           # dust that breathes
    ("theme-light", 916.5, TOTAL, None, 0.4, 1.0, 4.0),          # end card
]

V2SFX = "01-the-seven-days-v2/audio/sfx/"
GSFX = "02-the-garden/audio/sfx/movement/"
# designed hits and spot effects, never ducked: (file under genesis/, time, volume[, seconds into the file])
HITS = [
    (V2SFX + "riser.wav", 0.0, 0.7), (V2SFX + "windrush.wav", 0.5, 0.8),      # the fall from the sky
    (V2SFX + "boom-big.wav", 5.6, 0.8),                                       # landing on the grain of dust
    (GSFX + "breath-of-life.mp3", 6.4, 1.0),                                  # the first breath
    (V2SFX + "flyby1.wav", 10.0, 0.5), (V2SFX + "flyby3.wav", 12.4, 0.45), (V2SFX + "flyby2.wav", 14.6, 0.45),
    (V2SFX + "hit.wav", 17.0, 0.6),                                            # cut to black for God's line
    (V2SFX + "hit.wav", 42.6, 0.8),                                            # title
    (GSFX + "breath-of-life.mp3", 148.6, 0.9), (V2SFX + "hit.wav", 152.0, 0.5),  # the breath set piece
    (V2SFX + "hit.wav", 298.0, 0.5), (V2SFX + "hit.wav", 333.1, 0.6),           # rivers peak; hard cut to the camp
    (V2SFX + "hit.wav", 572.6, 0.45),                                          # the music stops on the man alone
    (V2SFX + "hit.wav", 639.0, 0.5),                                           # face to face
    (V2SFX + "bang.wav", 808.1, 0.5),                                          # into the dark flash-forward
    (GSFX + "breath-of-life.mp3", 777.0, 0.7), (V2SFX + "hit.wav", 780.0, 0.5),  # the same wind at the tomb
    (V2SFX + "hit.wav", 863.0, 0.5),
    (GSFX + "breath-of-life.mp3", 876.5, 0.8),                                 # back to the dust: the breath returns
    (V2SFX + "hit.wav", 917.3, 0.6),                                           # end card
] + [(V2SFX + "whoosh.wav", t, 0.3) for t in (205.5, 210.0, 214.0, 249.7, 255.0, 539.5, 544.0, 549.0, 554.0)] \
  + [(V2SFX + "hit.wav", t, 0.35) for t, n in T["chapters"] if n not in ("Cold open", "Down to the ground")]

SD1 = "01-the-seven-days/audio/sfx/"
# ambience beds, ducked lightly: (file under genesis/, start, end, volume)
BEDS = [
    (SD1 + "movement/desert-camp.mp3", 22.0, 42.6, 0.4),
    (GSFX + "dry-wind-plain.mp3", 46.6, 117.7, 0.3), (GSFX + "springs-welling.mp3", 117.7, 148.8, 0.45),
    (GSFX + "dry-wind-plain.mp3", 162.8, 205.5, 0.25),
    (GSFX + "garden-morning.mp3", 205.5, 249.7, 0.35), (GSFX + "river-flowing.mp3", 249.7, 333.1, 0.45),
    (SD1 + "movement/desert-camp.mp3", 334.1, 377.1, 0.4), (GSFX + "garden-morning.mp3", 377.1, 418.9, 0.3),
    (GSFX + "great-trees-wind.mp3", 418.9, 497.0, 0.5),
    (SD1 + "movement/grass-wind.mp3", 496.9, 539.5, 0.4), (SD1 + "movement/herds.mp3", 539.5, 572.6, 0.3),
    (GSFX + "night-garden.mp3", 572.6, 631.7, 0.45), (GSFX + "garden-morning.mp3", 631.7, 674.3, 0.35),
    (SD1 + "movement/desert-camp.mp3", 674.3, 712.9, 0.35), (SD1 + "movement/thorn-wind.mp3", 719.2, 733.4, 0.4),
    (GSFX + "olive-grove-night.mp3", 733.4, 776.2, 0.35), (SD1 + "movement/garden-dawn.mp3", 776.2, 808.1, 0.45),
    (SD1 + "movement/thorn-wind.mp3", 808.1, 839.9, 0.45), (SD1 + "movement/new-creation.mp3", 839.9, 876.3, 0.3),
    (GSFX + "dry-wind-plain.mp3", 876.3, 903.4, 0.3), (SD1 + "rumble-under-god.mp3", 903.4, 917.3, 0.5),
    (SD1 + "movement/thorn-wind.mp3", 903.4, 917.3, 0.35),
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
        ins += ["-stream_loop", "-1", "-i", str(GEN / f)]
        fc.append(f"[{n}:a]{st},atrim=0:{L:.2f},afade=in:d=1.5,afade=out:st={max(0, L - 1.5):.2f}:d=1.5,"
                  f"volume={vol},adelay={int(a * 1000)}:all=1[a{n}]")
        beds.append(f"[a{n}]"); n += 1
    for f, t, vol, *seek in HITS:
        ins += (["-ss", f"{seek[0]}"] if seek else []) + ["-i", str(GEN / f)]
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
    anim = FILM / "exports/movement-animatic.mp4"
    if anim.exists():
        ff("-i", anim, "-i", OUT / "mix.m4a", "-map", "0:v", "-map", "1:a", "-c", "copy", "-shortest",
           "-movflags", "+faststart", FILM / "exports/movement-animatic-scored.mp4")
        print(f"-> {FILM / 'exports/movement-animatic-scored.mp4'}")


if __name__ == "__main__":
    main()
