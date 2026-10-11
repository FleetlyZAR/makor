#!/usr/bin/env python3
"""Animate a movement film's shots locally with LTX-2.5 on the Mac (MLX), free and without limits.

Same plan as films/tools/omni_clips.py (script/shotlist.json and each shot's `omni` field): every shot with a
picture gets a clip from its own keyframe as the first frame and its motion prompt. A "bridge" anchors the
previous clip's frame at the cut as the first frame and the shot's keyframe as the last. "text" takes are made
from the prompt alone; "same" shots cut from another clip; "extend" takes are left to Omni (LTX extension is
in beta). Shots with no clip of any kind go first, then the rest, so the gaps fill before the comparisons.

Clips are 1280x704 at 24 fps from the distilled two stage pipeline, long enough for the shot plus a margin
(8 frame steps, 2 to 10 s), with no sound. Writes clips/ltx/<id>.mp4 and clips/ltx/log.json (render
seconds). Resumable; one shot at a time (the GPU is the limit). The edit (edit/preview_cut.py) prefers an Omni
clip where both exist unless told otherwise.

    python3 films/tools/ltx_clips.py films/genesis/01-the-seven-days-v2 [s021 s100-s120 ...] [--all]
"""
import argparse, json, math, pathlib, subprocess, sys, time

LTX = pathlib.Path.home() / "ml/ltx-2-mlx/.venv/bin/ltx-2-mlx"
MODEL = pathlib.Path.home() / "ml/models/ltx-2.5-mlx-q8"
W, H, FPS = 1280, 704, 24


def frames_for(d):
    want = min(10.0, max(2.0, d * 1.15 + 0.4)) * FPS
    return int(math.ceil((want - 1) / 8) * 8 + 1)


def frame_at(clip, t, dest):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", str(clip), "-frames:v", "1", "-q:v", "2",
                    str(dest)], check=True)
    return dest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("film")
    ap.add_argument("shots", nargs="*")
    ap.add_argument("--all", action="store_true", help="also shots that already have an Omni clip")
    ap.add_argument("--seed", type=int, default=7)
    args = ap.parse_args()
    film = pathlib.Path(args.film).resolve()
    shots = json.loads((film / "script/shotlist.json").read_text())
    out, tmp = film / "clips/ltx", film / "clips/ltx/tmp"
    tmp.mkdir(parents=True, exist_ok=True)
    lf = out / "log.json"
    log = json.loads(lf.read_text()) if lf.exists() else {}
    want = set()
    for a in args.shots:
        lo, _, hi = a.partition("-")
        want |= {f"s{n:03d}" for n in range(int(lo[1:]), int((hi or lo)[1:]) + 1)}
    omni = lambda s: (film / "clips/omni" / f"{s['id']}.mp4").exists()
    todo = [s for s in shots if (not want or s["id"] in want) and s["kind"] != "graphic"
            and (s.get("omni") or {}).get("mode", "image") in ("image", "bridge", "text")
            and not (out / f"{s['id']}.mp4").exists() and (args.all or want or not omni(s))]
    todo.sort(key=lambda s: omni(s))            # gaps first
    print(f"{len(todo)} clips to make with LTX-2.5 at {W}x{H}", flush=True)
    for sh in todo:
        o = sh.get("omni") or {}
        mode = o.get("mode", "image")
        n = frames_for(sh["dur"])
        key = film / (sh["src"] if sh["kind"] == "reuse" else f"stills/movement/{sh['id']}.jpg")
        cmd = [str(LTX), "generate", "--model", str(MODEL), "--distilled", "-H", str(H), "-W", str(W), "-f", str(n),
               "--frame-rate", str(FPS), "--seed", str(args.seed), "--no-audio", "--quiet"]
        if mode == "text":
            prompt = o["prompt"]
        elif mode == "bridge":
            src = film / "clips/omni" / f"{o['clip']}.mp4"
            if not src.exists():
                print(f"{sh['id']}: needs {o['clip']} first", flush=True)
                continue
            first = frame_at(src, o["at"], tmp / f"{sh['id']}-first.jpg")
            cmd += ["--image", str(first), "0", "1.0", "--image", str(key), "last", "1.0"]
            prompt = o["prompt"]
        else:
            if not key.exists():
                print(f"{sh['id']}: no keyframe", flush=True)
                continue
            cmd += ["--image", str(key), "0", "1.0"]
            prompt = o.get("prompt") or sh.get("ltx_prompt") or sh["motion"]
            if sh.get("flags") == "pair" or sh.get("lock"):
                # lock: The Garden v2, unclothed figures that LTX dressed or moved (s147 trousers, s149 extra women)
                # modesty: LTX let the pair rise out of the grass (s101, s112), so the last frame is the keyframe too
                cmd += ["--image", str(key), "last", "1.0"]
                prompt += " They stay where they are; the framing ends as it began, the grass and their hair as in the image."
        dest = out / f"{sh['id']}.mp4"
        # only a real render (a Python process running the ltx-2-mlx script), never a shell whose text mentions it
        while subprocess.run(["pgrep", "-f", r"^[^ ]*[Pp]ython[^ ]* [^ ]*ltx-2-mlx generate"],
                             capture_output=True).returncode == 0:
            time.sleep(20)                   # another LTX job holds the GPU (two at once run out of memory)
        t0 = time.time()
        r = subprocess.run(cmd + ["--prompt", prompt, "-o", str(dest)], capture_output=True, text=True)
        secs = round(time.time() - t0)
        if r.returncode or not dest.exists():
            print(f"{sh['id']}: failed after {secs} s: {(r.stderr or r.stdout)[-600:]}", flush=True)
            continue
        log[sh["id"]] = dict(frames=n, secs=secs, mode=mode, seed=args.seed)
        lf.write_text(json.dumps(log, indent=1))
        print(f"{sh['id']}: {n} frames in {secs} s", flush=True)


if __name__ == "__main__":
    main()
