#!/usr/bin/env python3
"""Veo clips for a movement film, driven by script/shotlist.json.

  veo  keyframe stills/movement/<id>.jpg as the first frame
  ff   first and last frame: <id>.jpg to the NEXT shot's keyframe

16:9, 1080p, 8 s, Veo 3.1 Fast by default. Resumable: shots that already have
clips/movement/<id>.mp4 are skipped. On a quota error (HTTP 429) it stops
cleanly and reports what is left, so the next day's run picks up from there.
Costs go to COSTS-movement.md. Key from the macOS Keychain only.

    python3 films/tools/movement_clips.py films/genesis/01-the-seven-days [s024 s031 ...]
"""
import base64, json, pathlib, sys, time, urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from clip import BANNED, BASE, MODELS, SECONDS, call, key, log_cost  # noqa: E402


def img(path):
    return {"mimeType": "image/jpeg", "bytesBase64Encoded": base64.b64encode(path.read_bytes()).decode()}


def main():
    film = pathlib.Path(sys.argv[1])
    only = set(sys.argv[2:])
    shots = json.loads((film / "script" / "shotlist.json").read_text())
    model, rate = MODELS["fast"]
    out = film / "clips" / "movement"
    out.mkdir(parents=True, exist_ok=True)
    todo = [(i, s) for i, s in enumerate(shots) if s["kind"] in ("veo", "ff") and (not only or s["id"] in only)
            and not (out / f"{s['id']}.mp4").exists()]
    print(f"{len(todo)} clips to make", flush=True)
    k, done = key(), 0
    for i, s in todo:
        p = s["motion"]
        assert p and not any(w in p.lower() for w in BANNED), s["id"]
        inst = {"prompt": p, "image": img(film / "stills" / "movement" / f"{s['id']}.jpg")}
        if s["kind"] == "ff":
            last = next((f.split(":")[1] for f in s["flags"].split() if f.startswith("last:")), shots[i + 1]["id"])
            inst["lastFrame"] = img(film / "stills" / "movement" / f"{last}.jpg")
        body = {"instances": [inst], "parameters": {"aspectRatio": "16:9", "resolution": "1080p",
                                                    "durationSeconds": SECONDS}}
        try:
            op = call(f"{BASE}/models/{model}:predictLongRunning", k, body)
        except urllib.error.HTTPError as e:
            msg = e.read().decode()[:400]
            if e.code == 429:
                print(f"quota reached at {s['id']} after {done} clips today; rerun tomorrow to continue", flush=True)
                return
            sys.exit(f"{s['id']}: HTTP {e.code}: {msg}")
        while not op.get("done"):
            time.sleep(10)
            op = call(f"{BASE}/{op['name']}", k)
        if "error" in op:
            print(f"{s['id']}: operation failed: {json.dumps(op['error'])[:300]}", flush=True)
            continue
        samples = op.get("response", {}).get("generateVideoResponse", {}).get("generatedSamples") or []
        if not samples:
            print(f"{s['id']}: no video returned (filtered?)", flush=True)
            continue
        req = urllib.request.Request(samples[0]["video"]["uri"], headers={"x-goog-api-key": k})
        with urllib.request.urlopen(req, timeout=300) as r:
            (out / f"{s['id']}.mp4").write_bytes(r.read())
        done += 1
        total = log_cost(film, f"Veo 3.1 fast ({model})",
                         f"clip {s['id']} ({s['kind']}) -> clips/movement/{s['id']}.mp4",
                         f"{SECONDS} s 1080p", SECONDS * rate, log="COSTS-movement.md")
        print(f"{s['id']}: done ({s['kind']}), running total {total:.2f} USD", flush=True)
    print(f"finished: {done} clips this run", flush=True)


if __name__ == "__main__":
    main()
