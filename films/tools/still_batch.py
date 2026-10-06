#!/usr/bin/env python3
"""Keyframes through the Gemini Batch API at half the standard price.

Reads the same shot list markdown as still.py (### Shot N: sNNN, - Refs:, - Image prompt),
sends the prompts as inline batch jobs to gemini-3-pro-image-preview with
generationConfig.imageConfig (aspectRatio, imageSize 2K), polls until each job
finishes (usually well within 24 hours), saves each image as <out>/<id>.jpg and logs
the cost at half the standard rate. Reference images are sent downscaled to 1024 px
(they only guide style and continuity), so many requests fit in one 20 MB job.

State is kept in <out>/batch-state.json, so a run can be stopped and resumed: jobs
already submitted are polled, never resubmitted. Key from the macOS Keychain only.

    python3 films/tools/still_batch.py FILM 1 2 3 ... --script script/shotlist.md --out stills/movement \
        --aspect 16:9 --log COSTS-movement.md
"""
import argparse, base64, io, json, pathlib, sys, time, urllib.request

from PIL import Image

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from still import BANNED, key, log_cost, meta, prompts  # noqa: E402

BASE = "https://generativelanguage.googleapis.com/v1beta"
MODEL = "gemini-3-pro-image-preview"   # the batch model id in the Batch API docs
PRICE = 0.134 / 2                      # Batch API: 50 percent of the standard cost
LIMIT = 18 * 1024 * 1024               # stay under the 20 MB inline request limit


def call(url, k, body=None):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None,
                                 method="POST" if body else "GET",
                                 headers={"x-goog-api-key": k, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.load(r)


def small(path):
    im = Image.open(path).convert("RGB")
    im.thumbnail((1024, 1024))
    b = io.BytesIO()
    im.save(b, "JPEG", quality=85)
    return base64.b64encode(b.getvalue()).decode()


def find_inlined(obj):
    """The list of inlined responses, wherever the job response nests it."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "inlinedResponses" and isinstance(v, list):
                return v
            r = find_inlined(v)
            if r is not None:
                return r
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("film")
    ap.add_argument("shots", nargs="*", type=int)
    ap.add_argument("--script", default="script/shotlist.md")
    ap.add_argument("--out", default="stills/movement")
    ap.add_argument("--aspect", default="16:9")
    ap.add_argument("--log", default="COSTS-movement.md")
    a = ap.parse_args()
    film = pathlib.Path(a.film)
    out = film / a.out
    out.mkdir(parents=True, exist_ok=True)
    state_f = out / "batch-state.json"
    state = json.loads(state_f.read_text()) if state_f.exists() else {"jobs": []}
    k = key()
    ps = prompts(film / a.script)
    names, refs = meta(film / a.script)
    pending = {sid for j in state["jobs"] if not j.get("done") for sid in j["ids"]}

    # build and submit new jobs for shots that have no image and are not already submitted
    reqs, size = [], 0
    def submit():
        nonlocal reqs, size
        if not reqs:
            return
        body = {"batch": {"display_name": f"makor-keyframes-{int(time.time())}",
                          "input_config": {"requests": {"requests": [r for r, _ in reqs]}}}}
        res = call(f"{BASE}/models/{MODEL}:batchGenerateContent", k, body)
        name = res.get("name") or res.get("metadata", {}).get("name")
        state["jobs"].append({"name": name, "ids": [sid for _, sid in reqs], "done": False})
        state_f.write_text(json.dumps(state, indent=1))
        print(f"submitted {name} with {len(reqs)} keyframes", flush=True)
        reqs, size = [], 0
    for n in a.shots:
        sid = names.get(n, f"shot-{n:02d}")
        if (out / f"{sid}.jpg").exists() or sid in pending:
            continue
        p = ps[n]
        assert not any(w in p.lower() for w in BANNED), f"{sid}: banned word in prompt"
        parts = [{"text": p}] + [{"inlineData": {"mimeType": "image/jpeg", "data": small(film / r)}}
                                 for r in refs.get(n, [])]
        r = {"request": {"contents": [{"parts": parts}],
                         "generation_config": {"responseModalities": ["TEXT", "IMAGE"],
                                               "imageConfig": {"aspectRatio": a.aspect, "imageSize": "2K"}}},
             "metadata": {"key": sid}}
        rs = len(json.dumps(r))
        if size + rs > LIMIT:
            submit()
        reqs.append((r, sid)); size += rs
    submit()

    # poll every unfinished job; save images when done
    while True:
        open_jobs = [j for j in state["jobs"] if not j.get("done")]
        if not open_jobs:
            break
        for j in open_jobs:
            res = call(f"{BASE}/{j['name']}", k)
            st = res.get("state") or res.get("metadata", {}).get("state", "")
            if st.endswith("SUCCEEDED"):
                items = find_inlined(res) or []
                for it in items:
                    sid = (it.get("metadata") or {}).get("key")
                    parts = [p for c in (it.get("response") or {}).get("candidates", [])
                             for p in (c.get("content") or {}).get("parts", [])]
                    img = next((p["inlineData"] for p in parts if p.get("inlineData")), None)
                    if not sid or not img:
                        print(f"{sid}: no image returned ({json.dumps(it)[:300]})", flush=True)
                        continue
                    (out / f"{sid}.jpg").write_bytes(base64.b64decode(img["data"]))
                    total = log_cost(film, f"still {sid} via Batch API (half price) -> {a.out}/{sid}.jpg",
                                     PRICE, a.log)
                    print(f"{sid}: saved, running total {total:.2f} USD", flush=True)
                j["done"] = True
            elif any(st.endswith(x) for x in ("FAILED", "CANCELLED", "EXPIRED")):
                print(f"{j['name']}: {st}", flush=True)
                j["done"] = True
            state_f.write_text(json.dumps(state, indent=1))
        if any(not j.get("done") for j in state["jobs"]):
            time.sleep(60)
    print("all batch jobs finished")


if __name__ == "__main__":
    main()
