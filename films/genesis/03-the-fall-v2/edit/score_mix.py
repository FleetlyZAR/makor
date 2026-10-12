#!/usr/bin/env python3
"""The Fall v2: temp score, sound design and mix, on the voice timeline.

Built the way The Garden v2 was (`02-the-garden-v2/edit/score_mix.py`): one cue per turn of the
story, each set piece's crest landed on its peak, music above the voice only in the set pieces,
hard drops and silence before the key lines (3:9, 3:15, 3:19 and every word God speaks in
judgment), a low hit on every chapter card, foley on what we show, ambience beds placed by time.
Mix per films/SCORING.md version C and films/CINEMA-STANDARD.md (-16 LUFS, one fixed gain).

The emotional line (TREATMENT.md cue sheet): suspense and Egypt for the serpent, a build cut dead
on the bite, lonely piano for the shame, a held chord for the voice in the garden and then
silence, cold winds for the blame, driving percussion for the long war, The Garden's own opening
music played backward and slowed for dust to dust, the first warmth when God clothes them, the
biggest peak for east of Eden, darkness to a burst of light at the veil, the warmest swell for the
way back, and a low unresolved note into Cain and Abel.

Music is TEMP, all from tracks already licensed for the series (The Garden v2 Epidemic cues,
The Seven Days v2 library); The Fall's own cues come from the cue sheet later.

    makor-audio/.venv/bin/python films/genesis/03-the-fall-v2/edit/score_mix.py
writes edit/score/mix.wav, music.wav and mix.m4a, and exports/movement-animatic-scored.mp4.
"""
import json, pathlib, subprocess, sys

import numpy as np

FILM = pathlib.Path(__file__).resolve().parents[1]
GEN = FILM.parent
DIRS = [GEN / "02-the-garden-v2/audio/music", GEN / "01-the-seven-days-v2/audio/music-v2"]
OUT = FILM / "edit/score"
T = json.loads((FILM / "script/movement-timeline.json").read_text())
TOTAL = T["total"]
SHOTS = {s["id"]: s["start"] for s in json.loads((FILM / "script/shotlist.json").read_text())}


def at(shot, plus=0.0):
    return SHOTS[shot] + plus


# (track, start, end, crest or None, volume, fade in, fade out[, seek seconds[, options]])
CUES = [
    ("rivers-collapse", 9.3, 16.3, None, 0.85, 0.05, 0.08, 20.0),  # flash-forward montage at full drive; cut dead
    ("too-fast", 17.0, 43.0, None, 0.5, 2.0, 3.0),                 # the movement in the grass, the hook, the title
    ("river-of-tears", 43.4, 107.6, None, 0.5, 2.0, 0.8, 37.0),    # the serpent and Egypt (the Egypt cue of The Seven Days v2); out for the eye
    ("tavore", 109.4, 219.5, None, 0.42, 2.0, 2.5),                # word against word: waves of suspense as the lie is built
    ("nascency", 220.1, 247.3, 246.0, 0.8, 3.0, 0.08),             # the eating: a build from nothing, cut dead on the bite
    ("g-09a", 266.3, 317.0, None, 0.4, 3.0, 2.5),                  # Felt Like November: the shame, lonely piano
    ("g-04", 317.6, 346.6, 345.0, 0.8, 3.0, 0.15),                 # Imminent End: the voice in the garden to a held crest; then silence for 3:9
    ("g-07", 365.0, 414.0, None, 0.42, 3.0, 3.0),                  # Desert Bloom: the camp, the God who comes looking
    ("g-02", 445.2, 484.0, None, 0.38, 3.0, 3.0),                  # Crying Winds: the blame passed down the line
    ("himalayan-moon", 501.3, 529.5, None, 0.32, 3.0, 0.3, 111.0), # a low pulse under the curse; stops for the boom after 3:15
    ("himalayan-moon", 531.5, 566.0, None, 0.32, 1.5, 3.0, 140.0),  # the pulse returns under enmity and the seed
    ("g-09b", 531.5, 584.7, 579.0, 1.0, 2.0, 0.08),                # Momentum I. Quake: enmity and the long war; stops dead on the strike
    ("g-13a", 599.9, 657.1, None, 0.4, 3.0, 1.0),                  # Ashes of All: pain, toil, thorns
    ("g-01", 657.1, 671.6, None, 1.6, 0.5, 2.0, 0.0, dict(reverse=13.0, rate=0.85)),  # dust to dust: The Garden's opening, backward and slowed
    ("theme-image", 692.9, 761.0, None, 0.42, 4.0, 3.0),           # the human theme: mercy, Eve, the garments; first warmth since the fall
    ("last-frontier", 784.2, 823.5, None, 0.9, 3.0, 3.0, 89.3),    # east of Eden: its hit (110.3 s) lands on the sword at 805.2; drains to wind
    ("river-of-tears", 823.0, 882.5, None, 0.42, 3.0, 3.0, 120.0), # the veil, barred, Israel carried east (the Egypt cue returns for Babylon)
    ("g-12", 883.0, 983.7, None, 0.5, 3.0, 2.0),                   # Breath by Breath: the seed of the woman, a reverent build into darkness
    ("g-13b", 988.0, 1000.5, 995.0, 0.85, 0.2, 1.5),               # The Sky Remembers Us: the veil tears, light bursts, the empty tomb
    ("abode-of-snow", 999.7, 1057.0, 1052.0, 0.6, 3.0, 2.5),       # the way back: the warmest swell on the city and the tree of life
    ("theme-word", 1056.7, 1088.3, None, 0.45, 2.5, 2.0),          # come out: the light theme
    ("g-13a", 1088.0, TOTAL, None, 0.38, 1.5, 4.0, 150.0),         # open loop: a low unresolved note for Cain and Abel
]

SD2 = "01-the-seven-days-v2/audio/sfx/"
F1 = "03-the-fall/audio/sfx/movement/"
F2 = "03-the-fall-v2/audio/sfx/movement/"
GS = "02-the-garden/audio/sfx/movement/"
SD1 = "01-the-seven-days/audio/sfx/"
# spot effects, never ducked: (file under genesis/, time, volume[, seek[, length]])
HITS = [
    (F2 + "wind-footsteps.mp3", 0.0, 0.95, 0.0, 6.0),                     # the wind walks toward us and stops dead
    (F2 + "fearful-breath.mp3", at("s004"), 0.6, 0.0, 1.5),              # Adam's eye
    (SD2 + "boom-big.wav", at("s006"), 0.9), (F2 + "fire-ignite.mp3", at("s006"), 0.8, 0.0, 1.0),
    (F2 + "fruit-tear.mp3", at("s007"), 0.9), (F2 + "serpent-scales.mp3", at("s008"), 0.7, 0.0, 1.0),
    (F2 + "leaves-rip.mp3", at("s009"), 0.8, 0.0, 1.0), (F2 + "thorns-burst.mp3", at("s010"), 0.7, 0.0, 1.0),
    (F2 + "dust-blow.mp3", at("s011"), 0.6, 0.0, 1.0), (F1 + "turning-flame.mp3", at("s012"), 1.0, 0.0, 1.0),
    (SD2 + "hit.wav", 16.3, 0.7),                                        # music cuts to nothing on The Garden's last shot
    (F1 + "grass-rustle.mp3", at("s016"), 0.7, 0.0, 4.0), (F2 + "serpent-scales.mp3", at("s017"), 0.6),
    (SD2 + "hit.wav", 39.4, 0.85),                                       # title
    (F2 + "serpent-scales.mp3", at("s019"), 0.5), (F2 + "serpent-scales.mp3", at("s020"), 0.4),
    (SD2 + "drop.wav", at("s033") - 0.4, 0.5),                            # the serpent's eye in silence
    (SD2 + "hit.wav", 186.4, 0.4),                                       # NOT settles on God's words
    (SD2 + "hit.wav", 218.1, 0.3),
    (SD2 + "riser.wav", at("s052") - 2.0, 0.6),                          # slow motion toward the bite
    (F2 + "fruit-tear.mp3", at("s053"), 1.0),                            # the branch springs back
    (SD2 + "boom-big.wav", 247.3, 0.7), (SD2 + "windrush.wav", 247.3, 0.6),  # the bite: the score cuts out, the wind turns
    (F2 + "fearful-breath.mp3", at("s058"), 0.55, 0.0, 3.0),            # eyes opened in fear
    (F2 + "leaves-rip.mp3", at("s060"), 0.9), (F2 + "leaves-rip.mp3", 263.3, 0.8),  # the rip of leaves, then silence
    (F2 + "wind-footsteps.mp3", 332.6, 1.0),                             # set piece: wind like footsteps (the full 14 s)
    (F2 + "fearful-breath.mp3", 336.5, 0.6),                             # the pair's breathing, close
    (SD2 + "hit.wav", 346.6, 0.4),                                       # everything stops
    (SD1 + "rumble-under-god.mp3", 414.0, 0.4, 0.0, 26.0),               # God's questions
    (SD1 + "rumble-under-god.mp3", 484.0, 0.45, 0.0, 17.0),              # the sentence on the serpent
    (F2 + "serpent-scales.mp3", at("s106"), 0.6),
    (SD2 + "boom-big.wav", 529.5, 0.8),                                  # after 3:15
    (SD2 + "hit.wav", 574.8, 0.45), (SD2 + "hit.wav", 576.8, 0.45), (SD2 + "hit.wav", 578.8, 0.5),
    (SD2 + "hit.wav", 580.8, 0.55),                                      # a hit on each AND THEN HE DIED
    (SD2 + "bang.wav", at("s125"), 0.6),                                 # the strike, then black
    (SD1 + "rumble-under-god.mp3", 584.8, 0.4, 0.0, 15.0),               # the sentence on the woman
    (F2 + "thorns-burst.mp3", at("s133"), 0.8),
    (GS + "breath-of-life.mp3", 657.3, 0.7, 0.0, None, True),            # dust to dust: the breath drawn back out (reversed)
    (SD2 + "windrush.wav", 663.0, 1.0), (SD2 + "riser.wav", 664.0, 0.6), (SD2 + "rewind.wav", 662.0, 0.5),
    (SD2 + "hit.wav", 688.7, 0.4),                                       # and then he died
    (SD1 + "rumble-under-god.mp3", 761.3, 0.4, 0.0, 15.0),               # 3:22
    (F2 + "footsteps-hard.mp3", at("s169"), 0.6, 0.0, 10.0),
    (F2 + "fire-ignite.mp3", 805.2, 1.0), (SD2 + "boom-big.wav", 805.2, 0.9),  # the sword ignites
    (SD2 + "whoosh.wav", at("s173"), 0.45), (SD2 + "whoosh.wav", at("s176"), 0.4),
    (F2 + "footsteps-hard.mp3", at("s175"), 0.5, 0.0, 6.0),
    (SD1 + "rumble-under-god.mp3", 983.7, 0.6, 0.0, 5.0), (F2 + "earth-quake.mp3", at("s205") - 0.5, 0.8),
    (F1 + "torn-cloth.mp3", at("s206"), 1.0), (SD2 + "boom-big.wav", 988.0, 0.7),  # the veil tears; light bursts
    (F2 + "dust-blow.mp3", at("s209") + 0.6, 0.7),                       # the serpent blows away as dust
    (SD2 + "hit.wav", 1052.0, 0.45),
    (SD2 + "hit.wav", 1100.6, 0.6),                                      # end card
] + [(SD2 + "hit.wav", t, 0.35) for t, n in T["chapters"] if n not in ("Cold open",)]

# ambience beds, ducked lightly: (file under genesis/, start, end, volume)
BEDS = [
    (F1 + "dusk-hush.mp3", 16.3, 43.4, 0.3), (GS + "garden-morning.mp3", 43.4, 71.7, 0.3),
    (SD1 + "movement/nile-kilns.mp3", 71.7, 93.0, 0.4), (SD1 + "movement/desert-camp.mp3", 79.8, 93.0, 0.25),
    (F1 + "dusk-hush.mp3", 93.0, 119.0, 0.3), (GS + "garden-morning.mp3", 119.0, 247.3, 0.25),
    (F1 + "heavy-sky-wind.mp3", 247.3, 317.6, 0.35),
    (F1 + "dusk-hush.mp3", 317.6, 364.6, 0.35), (SD1 + "movement/desert-camp.mp3", 364.6, 400.1, 0.4),
    (F1 + "evening-wind-trees.mp3", 400.1, 414.0, 0.35),
    (F1 + "dusk-hush.mp3", 414.0, 484.0, 0.35), (GS + "dry-wind-plain.mp3", 484.0, 572.8, 0.35),
    (SD1 + "movement/thorn-wind.mp3", 572.8, 584.8, 0.4),
    (F1 + "heavy-sky-wind.mp3", 584.8, 621.2, 0.4), (SD1 + "movement/thorn-wind.mp3", 621.2, 657.1, 0.45),
    (GS + "dry-wind-plain.mp3", 671.1, 707.3, 0.35), (SD1 + "movement/garden-dawn.mp3", 707.3, 732.4, 0.4),
    (SD1 + "movement/desert-camp.mp3", 732.4, 761.3, 0.4), (F1 + "dusk-hush.mp3", 761.3, 784.2, 0.35),
    (GS + "dry-wind-plain.mp3", 784.2, 834.4, 0.35), (F1 + "turning-flame.mp3", 800.0, 823.0, 0.55),
    (SD1 + "movement/lamp-room.mp3", 834.4, 849.5, 0.4), (SD1 + "movement/desert-camp.mp3", 849.5, 869.5, 0.35),
    (SD1 + "movement/night-air.mp3", 869.5, 883.0, 0.35), (GS + "dry-wind-plain.mp3", 883.0, 938.3, 0.3),
    (GS + "olive-grove-night.mp3", 938.3, 983.7, 0.35), (F2 + "dawn-birds.mp3", 990.0, 999.7, 0.45),
    (SD1 + "movement/lamp-room.mp3", 999.7, 1012.0, 0.35), (SD1 + "movement/new-creation.mp3", 1025.2, 1056.7, 0.3),
    (SD1 + "movement/desert-camp.mp3", 1056.7, 1088.0, 0.35), (F1 + "heavy-sky-wind.mp3", 1088.0, 1100.6, 0.35),
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


def find(name):
    for d in DIRS:
        if (d / f"{name}.wav").exists():
            return d, d / f"{name}.wav"
    sys.exit(f"missing track {name}")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    mel = []
    ins, fc, mus, beds, hits = ["-i", str(FILM / "audio/movement/voice-track.wav")], [], [], [], []
    n = 1
    st = "aformat=sample_rates=48000:channel_layouts=stereo"
    for cue in CUES:
        name, a, b, crest, vol, fi, fo = cue[:7]
        opt = cue[8] if len(cue) > 8 else {}
        d, src = find(name)
        shift = (peak_time(src) - (crest - a)) if crest else (cue[7] if len(cue) > 7 else 0.0)
        ss, start = (shift, a) if shift >= 0 else (0.0, a - shift)
        L = b - start
        if not opt and dur(src) - ss < L - 0.5:
            print(f"WARNING {name}: track runs out {L - (dur(src) - ss):.1f} s before its cue ends at {b:.1f}")
        stems = sorted(d.glob(f"{name}-*.wav")) if not opt else []
        parts = [(p, "mel" if p.stem.endswith("-melody") else "bed") for p in stems] if stems else [(src, "bed")]
        for path, bus in parts:
            ins += ["-ss", f"{ss:.2f}", "-i", str(path)]
            pre = ""
            if opt:   # played backward and slowed: take the first opt["reverse"] seconds, reverse, drop the rate
                pre = f"atrim=0:{opt['reverse']},areverse,asetrate={int(48000 * opt['rate'])},aresample=48000,"
            fc.append(f"[{n}:a]{st},{pre}atrim=0:{L:.2f},afade=in:d={fi},afade=out:st={max(0, L - fo):.2f}:d={fo},"
                      f"volume={vol},adelay={int(start * 1000)}:all=1[m{n}]")
            (mel if bus == "mel" else mus).append(f"[m{n}]"); n += 1
        print(f"music {name:16s} {start:7.1f} to {b:7.1f}" + (f"  crest on {crest}" if crest else "")
              + ("  (backward, slowed)" if opt else ""))
    for f, a, b, vol in BEDS:
        L = b - a
        ins += ["-stream_loop", "-1", "-i", str(GEN / f)]
        fc.append(f"[{n}:a]{st},atrim=0:{L:.2f},afade=in:d=1.5,afade=out:st={max(0, L - 1.5):.2f}:d=1.5,"
                  f"volume={vol},adelay={int(a * 1000)}:all=1[a{n}]")
        beds.append(f"[a{n}]"); n += 1
    for h in HITS:
        f, t, vol = h[:3]
        seek = h[3] if len(h) > 3 else 0.0
        length = h[4] if len(h) > 4 else None
        rev = h[5] if len(h) > 5 else False
        if vol <= 0:
            continue
        ins += (["-ss", f"{seek}"] if seek else []) + ["-i", str(GEN / f)]
        cut = f"atrim=0:{length},afade=out:st={max(0, length - 0.3):.2f}:d=0.3," if length else ""
        fc.append(f"[{n}:a]{st},{'areverse,' if rev else ''}{cut}volume={vol},adelay={int(t * 1000)}:all=1[h{n}]")
        hits.append(f"[h{n}]"); n += 1
    pad = f"apad=whole_dur={TOTAL:.2f}"
    fc.append(f"{''.join(mus)}amix=inputs={len(mus)}:normalize=0,{pad},extrastereo=m=1.3,"
              f"acrossover=split=250 1500 5000:order=8th[b0][b1][b2][b3]")
    fc.append(f"{''.join(beds)}amix=inputs={len(beds)}:normalize=0,{pad}[beds]")
    fc.append(f"{''.join(hits)}amix=inputs={len(hits)}:normalize=0,{pad}[hits]")
    fc.append(f"[0:a]{st},{pad},asplit[v][key]")
    fc.append("[key]asplit=6[k0][k1][k2][k3][k4][k5]")
    for i, (r, t) in enumerate([(2, 0.03), (4, 0.03), (12, 0.02), (2, 0.03)]):
        fc.append(f"[b{i}][k{i}]sidechaincompress=threshold={t}:ratio={r}:attack=25:release=500[d{i}]")
    fc.append("[d0][d1][d2][d3]amix=inputs=4:normalize=0[bedd]")
    fc.append(f"{''.join(mel)}amix=inputs={len(mel)}:normalize=0,{pad},extrastereo=m=1.3[melr]")
    fc.append("[melr][k5]sidechaincompress=threshold=0.02:ratio=10:attack=20:release=600[meld]")
    fc.append("[bedd][meld]amix=inputs=2:normalize=0[musd]")
    fc.append("[beds][k4]sidechaincompress=threshold=0.04:ratio=2:attack=30:release=600[bedsd]")
    fc.append("[musd][bedsd][hits]amix=inputs=3:normalize=0,asplit[score][score2]")
    fc.append(f"[v][score]amix=inputs=2:normalize=0,atrim=0:{TOTAL:.2f}[mix]")
    raw, music = OUT / "mix-raw.wav", OUT / "music.wav"
    graph = OUT / "graph.txt"
    graph.write_text(";".join(fc))
    ff(*ins, "-/filter_complex", graph, "-map", "[mix]", "-ar", 48000, raw, "-map", "[score2]", "-ar", 48000, music)
    i, lra, pk = lufs(raw)
    ff("-i", raw, "-af", f"volume={-16 - i:.2f}dB,alimiter=limit=0.79:level=false:attack=5:release=80", "-ar", 48000,
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
