#!/usr/bin/env python3
"""
Build names/lexicon.json from the reviewed batches, and validate every entry.

Each names/reviewed/batch-NN.json is a list of decisions, one per word in the
matching names/batches/batch-NN.json:

  {"word": "Zerubbabel", "action": "fix", "us": "zəɹˈʌbəbᵊl", "gb": "zəɹˈʌbəbəl",
   "say": "zuh-RUB-uh-bel", "lang": "Hebrew", "case": "exact"}
  {"word": "Moses", "action": "ok"}       misaki already says it right
  {"word": "believers", "action": "skip"} an ordinary English word

Only "fix" rows reach the lexicon. Run:  .venv/bin/python names/build.py
Add --check to validate without writing.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
# misaki's own phoneme sets, plus the fricatives the Kokoro model also accepts.
US = set("AIOWYbdfhijklmnpstuvwzæðŋɑɔəɛɜɡɪɹɾʃʊʌʒʤʧˈˌθᵊᵻʔTx")
GB = set("AIQWYabdfhijklmnpstuvwzðŋɑɒɔəɛɜɡɪɹʃʊʌʒʤʧˈˌːθᵊx")
VOWELS = set("AIOQWYaeiouæɑɒɔəɛɜɪʊʌᵊᵻ")


def problems(r):
    out = []
    for acc, allowed in (("us", US), ("gb", GB)):
        ps = r.get(acc) or ""
        if not ps:
            out.append(f"missing {acc}")
            continue
        bad = sorted(set(ps) - allowed)
        if bad:
            out.append(f"{acc} has symbols outside the set: {''.join(bad)}")
        if "ˈ" not in ps and len([c for c in ps if c in VOWELS]) > 1:
            out.append(f"{acc} has no primary stress")
        if not any(c in VOWELS for c in ps):
            out.append(f"{acc} has no vowel")
    if r.get("case") not in ("exact", "any"):
        out.append("case must be exact or any")
    return out


def main():
    check_only = "--check" in sys.argv
    entries, issues, missing = {}, [], []
    counts = {"fix": 0, "ok": 0, "skip": 0}
    for bf in sorted((HERE / "batches").glob("batch-*.json")):
        want = [r["word"] for r in json.loads(bf.read_text(encoding="utf-8"))]
        rf = HERE / "reviewed" / bf.name
        if not rf.exists():
            missing.append(bf.name)
            continue
        got = {r["word"]: r for r in json.loads(rf.read_text(encoding="utf-8"))}
        for w in want:
            if w not in got:
                issues.append(f"{bf.name}: no decision for {w}")
        for w, r in got.items():
            a = r.get("action")
            if a not in counts:
                issues.append(f"{bf.name}: {w}: bad action {a!r}")
                continue
            counts[a] += 1
            if a == "fix":
                for p in problems(r):
                    issues.append(f"{bf.name}: {w}: {p}")
                entries[w] = {k: r[k] for k in ("us", "gb", "say", "lang", "case", "avoid") if r.get(k)}
    # A match-any-case entry must never override a capitalised word that was
    # reviewed on its own (asher must not change the tribe name Asher).
    reviewed_words = set()
    for rf in (HERE / "reviewed").glob("batch-*.json"):
        reviewed_words |= {r["word"] for r in json.loads(rf.read_text(encoding="utf-8"))}
    for w, e in entries.items():
        if e.get("case") == "any" and w[:1].upper() + w[1:] in reviewed_words and w[:1].islower():
            e["case"] = "exact"
    # Hand overrides.
    ov = HERE / "overrides.json"
    if ov.exists():
        for w, o in json.loads(ov.read_text(encoding="utf-8")).get("entries", {}).items():
            if o.get("drop"):
                entries.pop(w, None)
                continue
            merged = {**entries.get(w, {}), **o}
            for p in problems(merged) if "us" in o or w not in entries else []:
                issues.append(f"overrides.json: {w}: {p}")
            entries[w] = merged
    print(f"decisions: {counts}; lexicon entries: {len(entries)}")
    if missing:
        print(f"not yet reviewed: {', '.join(missing)}")
    for i in issues[:200]:
        print("  ", i)
    if issues:
        print(f"{len(issues)} issues")
    if not check_only and not issues:
        (HERE / "lexicon.json").write_text(json.dumps(
            {"about": "Spoken forms for Makor audio. Built by names/build.py from names/reviewed. "
                      "us and gb are misaki phonemes; say is a readable guide.",
             "entries": dict(sorted(entries.items(), key=lambda kv: kv[0].lower()))},
            ensure_ascii=False, indent=1), encoding="utf-8")
        print("wrote names/lexicon.json")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
