#!/usr/bin/env python3
"""Animate a movement film's shots with Gemini Omni Flash (films/CINEMA-STANDARD.md).

Reads script/shotlist.json. Every shot with a picture gets one 10 second clip, by default from its own
keyframe as the first frame, with the cast portraits as references so faces hold. A shot's `omni`
field (set in the film's storyboard.py) changes how its clip is made:

  text    no image: the prompt alone (a set piece built as one continuous take)
  same    no clip of its own: the edit cuts it from another shot's clip (`clip`)
  extend  continues another shot's clip in the same take (Omni multi turn), so the join is seamless
  bridge  first frame taken from another shot's clip at `at` seconds, its own keyframe as the last frame

Writes clips/omni/<id>.mp4 (with Omni's own sound, which the edit drops) and clips/omni/log.json
(interaction ids, for extending). Resumable: existing clips are skipped. Stops a model on its daily
limit and says so; rerun the next day. Cost is logged per clip in COSTS-movement.md.

    python3 films/tools/omni_clips.py films/genesis/01-the-seven-days-v2 [s003 s019-s030 ...] [--workers 3]
        [--model gemini-omni-1.1-flash] [--res 1080p] [--redo]
"""
import argparse, base64, json, pathlib, subprocess, sys, threading, time, urllib.error, urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from clip import log_cost  # noqa: E402

API = "https://generativelanguage.googleapis.com/v1beta/interactions"
USD_PER_VIDEO_TOKEN = 17.5 / 1e6          # Omni 1.1 Flash video output (8,688 tokens a second at 1080p)
USD_PER_INPUT_TOKEN = 1.5 / 1e6
STYLE = ("Photoreal live action cinema, a feature film, shot on 35mm, natural light, deep ink teal shadows and warm "
         "muted gold highlights. One continuous shot with no cuts and no scene changes, steady unhurried motion through "
         "the whole ten seconds, no camera shake, no text, no captions, no logos, no watermark.")
SOUND = " Sound: natural ambience only. No music, no dialogue, no voices."
LOCK, QUOTA = threading.Lock(), threading.Event()


def key():
    return subprocess.run(["security", "find-generic-password", "-s", "makor-gemini", "-w"],
                          capture_output=True, text=True, check=True).stdout.strip()


def b64(path):
    return base64.b64encode(pathlib.Path(path).read_bytes()).decode()


def frame_at(clip, t, dest):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", str(clip), "-frames:v", "1", "-q:v", "2",
                    str(dest)], check=True)
    return dest


def call(body, k):
    req = urllib.request.Request(API, json.dumps(body).encode(), {"Content-Type": "application/json", "x-goog-api-key": k})
    attempt = waits = 0
    while True:
        try:
            return json.load(urllib.request.urlopen(req, timeout=1200))
        except urllib.error.HTTPError as e:
            msg = e.read().decode()[:600]
            if e.code == 429 and "spend-based" in msg and waits < 18:
                waits += 1                   # Google's spending rate cap for young accounts eases within minutes
                print(f"  spend rate cap, waiting 10 minutes ({waits})", flush=True)
                time.sleep(600)
                continue
            if e.code == 429:
                raise RuntimeError(f"quota: {msg}")
            attempt += 1
            if e.code >= 500 and attempt < 3:
                time.sleep(20)
                continue
            raise RuntimeError(f"HTTP {e.code}: {msg}")
        except (TimeoutError, urllib.error.URLError) as e:
            attempt += 1
            if attempt >= 3:
                raise RuntimeError(f"network: {e}")
            time.sleep(20)


def request_for(sh, film, log, args, tmp):
    """The request body for one shot, or None when the shot has no clip of its own."""
    o = sh.get("omni") or {}
    mode = o.get("mode", "image")
    rf = {"type": "video", "resolution": args.res, "aspect_ratio": "16:9"}
    body = {"model": args.model, "response_format": rf}
    if mode == "same" or sh["kind"] == "graphic":
        return None
    if mode == "text":
        body["input"] = [{"type": "text", "text": o["prompt"]}]
        return body
    if mode == "extend":
        prev = log.get(o["clip"], {}).get("interaction")
        if not prev:
            raise RuntimeError(f"needs {o['clip']} first")
        body.update(previous_interaction_id=prev, input=[{"type": "text", "text": o["prompt"]}])
        return body
    key_img = film / (sh["src"] if sh["kind"] == "reuse" else f"stills/movement/{sh['id']}.jpg")
    if not key_img.exists():
        raise RuntimeError(f"no keyframe {key_img.name}")
    imgs, tags = [], []
    if mode == "bridge":
        src = film / "clips/omni" / f"{o['clip']}.mp4"
        if not src.exists():
            raise RuntimeError(f"needs {o['clip']} first")
        imgs = [frame_at(src, o["at"], tmp / f"{sh['id']}-first.jpg"), key_img]
        tags = ["[# Sources <FIRST_FRAME>@Image1 <LAST_FRAME>@Image2]"]
        text = o["prompt"]
    elif mode == "morph":
        # one take from this shot's keyframe to another approved image (The Garden v2: dust becoming the man)
        imgs = [key_img, film / o["last"]]
        tags = ["[# Sources <FIRST_FRAME>@Image1 <LAST_FRAME>@Image2]"]
        text = o["prompt"]
    else:
        refs = [film / r for r in sh.get("refs", []) if not r.endswith("turnaround.jpg")]
        imgs = [key_img] + refs
        tags = ["[# Sources <FIRST_FRAME>@Image1]"]
        if refs:
            tags.append("[# References " + " ".join(f"<IMAGE_REF_{i}>@Image{i + 2}" for i in range(len(refs))) + "]")
        text = (o.get("prompt") or sh["motion"]) + " Use the first image as the starting frame" + (
            ", and keep each person exactly as in the reference images." if refs else ".")
    body["input"] = [{"type": "image", "data": b64(p), "mime_type": "image/jpeg"} for p in imgs] + [
        {"type": "text", "text": " ".join(tags) + " " + text + " " + STYLE + ("" if "Sound:" in text else SOUND)}]
    return body


def save(r, dest):
    for st in r.get("steps", []):
        for c in st.get("content", []):
            if c.get("type") == "video" and c.get("data"):
                dest.write_bytes(base64.b64decode(c["data"]))
                return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("film")
    ap.add_argument("shots", nargs="*")
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--model", default="gemini-omni-1.1-flash")
    ap.add_argument("--res", default="1080p")
    ap.add_argument("--redo", action="store_true")
    args = ap.parse_args()
    film = pathlib.Path(args.film).resolve()
    shots = json.loads((film / "script/shotlist.json").read_text())
    out, tmp = film / "clips/omni", film / "clips/omni/tmp"
    tmp.mkdir(parents=True, exist_ok=True)
    lf = out / "log.json"
    log = json.loads(lf.read_text()) if lf.exists() else {}
    want = set()
    for a in args.shots:
        lo, _, hi = a.partition("-")
        want |= {f"s{n:03d}" for n in range(int(lo[1:]), int((hi or lo)[1:]) + 1)}
    todo = [s for s in shots if (not want or s["id"] in want) and s["kind"] != "graphic"
            and (s.get("omni") or {}).get("mode") != "same" and (args.redo or not (out / f"{s['id']}.mp4").exists())]
    # clips that others extend or bridge from go first, in their own wave
    deps = {(s.get("omni") or {}).get("clip") for s in shots if (s.get("omni") or {}).get("mode") in ("extend", "bridge")}
    waves = [[s for s in todo if s["id"] in deps], [s for s in todo if s["id"] not in deps]]
    k, done, failed = key(), [], []
    print(f"{len(todo)} clips to make with {args.model} at {args.res}")

    def one(sh):
        if QUOTA.is_set():
            return
        try:
            body = request_for(sh, film, log, args, tmp)
            t0 = time.time()
            r = call(body, k)
            dest = out / f"{sh['id']}.mp4"
            if not save(r, dest):
                raise RuntimeError(f"no video returned (status {r.get('status')}): "
                                   + json.dumps(r)[:400])
            u = r.get("usage", {})
            vt = sum(m["tokens"] for m in u.get("output_tokens_by_modality", []) if m["modality"] == "video")
            usd = vt * USD_PER_VIDEO_TOKEN + u.get("total_input_tokens", 0) * USD_PER_INPUT_TOKEN
            with LOCK:
                log[sh["id"]] = dict(interaction=r.get("id"), model=args.model, res=args.res, secs=round(time.time() - t0),
                                     video_tokens=vt, usd=round(usd, 3), mode=(sh.get("omni") or {}).get("mode", "image"))
                lf.write_text(json.dumps(log, indent=1))
                log_cost(film, f"Gemini Omni ({args.model})", f"clip {sh['id']} {args.res}", f"{vt} video tokens", usd,
                         log="COSTS-movement.md")
                done.append(sh["id"])
                print(f"{sh['id']}: done in {time.time() - t0:.0f} s, about {usd:.2f} USD", flush=True)
        except RuntimeError as e:
            if str(e).startswith("quota"):
                QUOTA.set()
            with LOCK:
                failed.append(sh["id"])
                print(f"{sh['id']}: {e}", flush=True)

    for wave in waves:
        with ThreadPoolExecutor(args.workers) as ex:
            list(ex.map(one, wave))
    if QUOTA.is_set():
        print(f"daily limit reached for {args.model} after {len(done)} clips; rerun tomorrow (or try "
              f"--model gemini-omni-flash-preview)")
    print(f"done {len(done)}, not made {len(failed)}: {' '.join(failed)}")


if __name__ == "__main__":
    main()
