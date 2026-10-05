#!/usr/bin/env python3
"""Animate a Makor film keyframe with Veo 3.1 (image to video).

Reads the shot's motion prompt from the film's script markdown, sends the
keyframe as the first frame (9:16, 1080p, 8 s), polls the long running
operation, downloads the clip to clips/, and logs the paid call in COSTS.md.
Veo always generates audio; it is discarded in the edit.

The API key comes only from the macOS Keychain (service makor-gemini). It is
never printed or written to disk.

    python3 films/tools/clip.py films/genesis/01-the-seven-days 1
"""
import argparse, base64, datetime, json, pathlib, re, subprocess, sys, time, urllib.request

BASE = "https://generativelanguage.googleapis.com/v1beta"
MODELS = {"fast": ("veo-3.1-fast-generate-preview", 0.12), "standard": ("veo-3.1-generate-preview", 0.40)}
SECONDS = 8  # 1080p requires 8 s
BANNED = ["deity", "god figure", "divine being", "halo", "glowing man", "angel", "temple", "idol"]


def key():
    return subprocess.run(["security", "find-generic-password", "-s", "makor-gemini", "-w"],
                          capture_output=True, text=True, check=True).stdout.strip()


def motion_prompts(script: pathlib.Path) -> dict[int, str]:
    out, shot = {}, None
    lines = script.read_text().splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"### Shot (\d+):", line)
        if m:
            shot = int(m.group(1))
        if shot and line.startswith("- Motion prompt") and i + 1 < len(lines):
            out[shot] = lines[i + 1].strip().lstrip(">").strip()
    return out


def call(url, k, body=None):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None,
                                 method="POST" if body else "GET",
                                 headers={"x-goog-api-key": k, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.load(r)


def log_cost(film, tool, what, units, cost):
    f = film / "COSTS.md"
    text = f.read_text()
    rows = [l for l in text.splitlines() if re.match(r"\| \d+ \|", l)]
    total = sum(float(l.split("|")[6]) for l in rows) + cost
    row = f"| {len(rows) + 1} | {datetime.date.today()} | {tool} | {what} | {units} | {cost:.3f} | {total:.3f} |"
    text = re.sub(r"\nRunning total: [\d.]+", "", text).rstrip("\n")
    f.write_text(text + "\n" + row + f"\n\nRunning total: {total:.2f}\n")
    return total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("film")
    ap.add_argument("shots", nargs="+", type=int)
    ap.add_argument("--model", choices=MODELS, default="fast")
    ap.add_argument("--script", default="script/day-01-script.md")
    ap.add_argument("--tag", default="")
    ap.add_argument("--last", type=int, help="shot number whose keyframe is the LAST frame (interpolation)")
    a = ap.parse_args()
    film = pathlib.Path(a.film)
    model, rate = MODELS[a.model]
    ps = motion_prompts(film / a.script)
    k = key()
    for s in a.shots:
        p = ps[s]
        if any(w in p.lower() for w in BANNED):
            sys.exit(f"shot {s}: banned word in motion prompt")
        still = film / "stills" / f"shot-{s:02d}.jpg"
        body = {"instances": [{"prompt": p, "image": {
                    # inlineData is rejected by Veo 3.1 (HTTP 400); bytesBase64Encoded is the accepted form
                    "mimeType": "image/jpeg", "bytesBase64Encoded": base64.b64encode(still.read_bytes()).decode()}}],
                "parameters": {"aspectRatio": "9:16", "resolution": "1080p", "durationSeconds": SECONDS}}
        if a.last:
            last = film / "stills" / f"shot-{a.last:02d}.jpg"
            body["instances"][0]["lastFrame"] = {
                "mimeType": "image/jpeg", "bytesBase64Encoded": base64.b64encode(last.read_bytes()).decode()}
        try:
            op = call(f"{BASE}/models/{model}:predictLongRunning", k, body)
        except urllib.error.HTTPError as e:
            sys.exit(f"shot {s}: HTTP {e.code}: {e.read().decode()[:800]}")
        name = op["name"]
        print(f"shot {s}: submitted to {model}, polling", flush=True)
        while not op.get("done"):
            time.sleep(10)
            op = call(f"{BASE}/{name}", k)
        if "error" in op:
            sys.exit(f"shot {s}: operation failed: {json.dumps(op['error'])[:800]}")
        resp = op.get("response", {}).get("generateVideoResponse", {})
        samples = resp.get("generatedSamples") or []
        if not samples:
            sys.exit(f"shot {s}: no video returned (possibly filtered): {json.dumps(resp)[:800]}")
        dest = film / "clips" / f"shot-{s:02d}{a.tag}.mp4"
        dest.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(samples[0]["video"]["uri"], headers={"x-goog-api-key": k})
        with urllib.request.urlopen(req, timeout=300) as r:
            dest.write_bytes(r.read())
        total = log_cost(film, f"Veo 3.1 {a.model} ({model})", f"clip shot {s}{a.tag}" + (f" (last frame = shot {a.last})" if a.last else "") + f" -> clips/{dest.name}",
                         f"{SECONDS} s 1080p", SECONDS * rate)
        print(f"shot {s}: {dest} ({dest.stat().st_size // 1024} KB), running total {total:.2f} USD")


if __name__ == "__main__":
    main()
