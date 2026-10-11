#!/usr/bin/env python3
"""File the Epidemic downloads from ~/Downloads into audio/music/ under their cue names
(g-NN.wav for the full mix, g-NN-<stem>.wav for each stem). Waits until all 16 are complete."""
import pathlib, re, shutil, time, zipfile

DL = pathlib.Path.home() / "Downloads"
OUT = pathlib.Path(__file__).resolve().parents[1] / "audio/music"
CUES = {"g-01": "On the Brink of Glory", "g-02": "Crying Winds", "g-03": "Midst of Life", "g-04": "Imminent End",
        "g-05": "Winds of Aetheria", "g-06": "Crowned Kings", "g-07": "Desert Bloom", "g-08": "Woodwind Reviere",
        "g-09a": "Felt Like November", "g-09b": "Momentum", "g-10": "Mirroring", "g-11": "Into Open Arms",
        "g-12": "Breath by Breath", "g-13a": "Ashes of All", "g-13b": "The Sky Remembers Us", "g-14": "Before We Were"}


def done(cue):
    return (OUT / f"{cue}.wav").exists() and (any(OUT.glob(f"{cue}-*.wav")) or (OUT / f"{cue}.nostems").exists())


OUT.mkdir(parents=True, exist_ok=True)
for _ in range(720):
    for cue, title in CUES.items():
        if done(cue):
            continue
        for f in DL.glob("ES_*"):
            if title.lower() not in f.name.lower() or f.suffix not in (".wav", ".zip"):
                continue
            if f.suffix == ".wav" and "STEMS" not in f.name:
                shutil.move(str(f), OUT / f"{cue}.wav"); print(cue, "mix", flush=True)
            elif f.suffix == ".zip":
                try:
                    with zipfile.ZipFile(f) as z:
                        if not any("STEMS" in n for n in z.namelist()):
                            (OUT / f"{cue}.nostems").write_text("Epidemic gave no stems for this track\n")
                        for n in z.namelist():
                            m = re.search(r"STEMS (\w+)", n)
                            if m:
                                (OUT / f"{cue}-{m.group(1).lower()}.wav").write_bytes(z.read(n))
                    f.unlink(); print(cue, "stems", flush=True)
                except zipfile.BadZipFile:
                    pass
    if all(done(c) for c in CUES):
        print("all filed"); break
    time.sleep(10)
