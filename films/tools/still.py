#!/usr/bin/env python3
"""Generate keyframe stills for a Makor film with Nano Banana Pro.

Reads each shot's image prompt from the film's script markdown, calls the Gemini
Interactions API (model gemini-3-pro-image, 9:16, 2K), saves the image, and logs
the paid call in the film's COSTS.md.

The API key comes only from the macOS Keychain (service makor-gemini). It is
never printed or written to disk.

    python3 films/tools/still.py films/genesis/01-the-seven-days 3 4 6 --out stills/test
"""
import argparse, base64, datetime, json, pathlib, re, subprocess, sys, urllib.request

MODEL = "gemini-3-pro-image"
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/interactions"
PRICE = 0.134  # USD per 1K or 2K image, Gemini API pricing page
BANNED = ["deity", "god figure", "divine being", "halo", "glowing man", "angel", "temple", "idol"]


def key():
    return subprocess.run(["security", "find-generic-password", "-s", "makor-gemini", "-w"],
                          capture_output=True, text=True, check=True).stdout.strip()


def prompts(script: pathlib.Path) -> dict[int, str]:
    out, shot = {}, None
    lines = script.read_text().splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"### Shot (\d+):", line)
        if m:
            shot = int(m.group(1))
        if shot and line.startswith("- Image prompt") and i + 1 < len(lines):
            out[shot] = lines[i + 1].strip().lstrip(">").strip()
    return out


def log_cost(film: pathlib.Path, what: str, cost: float):
    f = film / "COSTS.md"
    text = f.read_text()
    rows = [l for l in text.splitlines() if re.match(r"\| \d+ \|", l)]
    total = sum(float(l.split("|")[6]) for l in rows) + cost
    row = (f"| {len(rows) + 1} | {datetime.date.today()} | Nano Banana Pro ({MODEL}) | {what} "
           f"| 1 image 2K | {cost:.3f} | {total:.3f} |")
    text = re.sub(r"\nRunning total: [\d.]+", "", text).rstrip("\n")
    f.write_text(text + "\n" + row + f"\n\nRunning total: {total:.2f}\n")
    return total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("film")
    ap.add_argument("shots", nargs="+", type=int)
    ap.add_argument("--out", default="stills")
    ap.add_argument("--script", default="script/day-01-script.md")
    ap.add_argument("--tag", default="", help="suffix for the file name, e.g. b for a retry")
    a = ap.parse_args()
    film = pathlib.Path(a.film)
    ps = prompts(film / a.script)
    k = key()
    for s in a.shots:
        p = ps[s]
        bad = [w for w in BANNED if w in p.lower()]
        if bad:
            sys.exit(f"shot {s}: banned words in prompt: {bad}")
        body = {"model": MODEL, "input": [{"type": "text", "text": p}],
                "response_format": {"type": "image", "aspect_ratio": "9:16", "image_size": "2K"}}
        req = urllib.request.Request(ENDPOINT, data=json.dumps(body).encode(), method="POST",
                                     headers={"x-goog-api-key": k, "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                res = json.load(r)
        except urllib.error.HTTPError as e:
            sys.exit(f"shot {s}: HTTP {e.code}: {e.read().decode()[:800]}")
        imgs = [c for st in res.get("steps", []) for c in (st.get("content") or [])
                if c.get("type") == "image" and c.get("data")]
        if not imgs:
            redacted = json.dumps(res)[:1500]
            sys.exit(f"shot {s}: no image in response (status {res.get('status')}): {redacted}")
        ext = {"image/png": "png", "image/jpeg": "jpg", "image/webp": "webp"}.get(imgs[0].get("mime_type"), "png")
        dest = film / a.out / f"shot-{s:02d}{a.tag}.{ext}"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(base64.b64decode(imgs[0]["data"]))
        total = log_cost(film, f"still shot {s}{a.tag} -> {dest.relative_to(film)}", PRICE)
        print(f"shot {s}: {dest} ({dest.stat().st_size // 1024} KB), running total {total:.2f} USD")


if __name__ == "__main__":
    main()
