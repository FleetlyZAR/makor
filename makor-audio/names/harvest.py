#!/usr/bin/env python3
"""
Harvest every name and transliterated word Makor speaks, and record how Kokoro
(misaki G2P) would pronounce each one today.

Sources: the exact spoken text of every study (generate_audio.build_segments,
so it covers passage, teaching, go deeper, notes and questions), every lexicon
lemma, and the whole BSB from tools/scripture/makor-scripture.db so future
studies are covered too.

Output: names/candidates.json, one row per word:
  word, kind (name | ambiguous | translit), count, dict (gold | silver | none, where none
  means misaki does not know it and falls back to espeak),
  current_us, current_gb (misaki phonemes today), example (a short context)

Run with the audio venv:  .venv/bin/python names/harvest.py
"""
import glob
import json
import re
import sqlite3
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE.parent))
import generate_audio as ga  # noqa: E402

WORD = re.compile(r"[A-Za-z][A-Za-z'’]*[A-Za-z]|[A-Za-z]")


def g2p_engine(british=False):
    from misaki import en, espeak
    return en.G2P(trf=False, british=british, fallback=espeak.EspeakFallback(british=british))


def main():
    g2p = g2p_engine()
    g2p_gb = g2p_engine(british=True)
    from misaki import en
    known = en.G2P(trf=False, british=False, fallback=None)
    golds, silvers = g2p.lexicon.golds, g2p.lexicon.silvers

    def in_lexicon(w):
        """True when misaki resolves the word itself (dictionary or stemming)."""
        return "❓" not in known(w)[0]

    cap_mid = Counter()     # capitalised, not sentence initial
    any_case = Counter()
    lower_seen = set()
    example = {}
    lemma_words = set()

    def feed(text):
        for sent in re.split(r"(?<=[.!?;:])\s+|[\"“”‘]", text):
            toks = list(WORD.finditer(sent))
            for i, m in enumerate(toks):
                w = m.group().replace("’", "'")
                w = re.sub(r"'s$", "", w)
                if not w:
                    continue
                any_case[w] += 1
                if w[0].islower():
                    lower_seen.add(w.lower())
                elif i > 0:
                    cap_mid[w] += 1
                if w not in example:
                    s = max(0, m.start() - 50)
                    example[w] = sent[s:m.end() + 50].strip()

    for f in sorted(glob.glob(str(ROOT / "src/content/studies/*/*.json"))):
        doc = json.loads(Path(f).read_text(encoding="utf-8"))
        for seg in ga.build_segments(doc, "both", {}):
            feed(seg["text"])
        for e in (doc.get("lexicon") or {}).values():
            for w in WORD.findall(ga.clean(e.get("lemma", ""))):
                lemma_words.add(w.lower())

    db = sqlite3.connect(str(ROOT / "tools/scripture/makor-scripture.db"))
    for (t,) in db.execute("select text from verse"):
        feed(ga.clean(t))

    rows = {}
    def dict_of(w):
        if w in golds or w.lower() in golds:
            return "gold"
        if w in silvers or w.lower() in silvers:
            return "silver"
        return "none"

    # Names: seen capitalised mid sentence and never as an ordinary lower case word.
    for w, n in cap_mid.items():
        if w.lower() in lower_seen or len(w) < 3 or w.isupper():
            continue
        rows[w] = {"word": w, "kind": "name", "count": any_case[w]}
    # Ambiguous: capitalised mid sentence in the BSB at least twice but also an
    # ordinary word (Job, Lot, Dan, Gad, Hur). Reviewers keep only real names.
    for w, n in cap_mid.items():
        if w in rows or w.isupper() or len(w) < 2 or w.lower() not in lower_seen:
            continue
        if n >= 2 and w not in ("I", "God", "Lord", "Christ"):
            rows[w] = {"word": w, "kind": "ambiguous", "count": any_case[w]}
    # Transliterations: lexicon lemma words, plus lower case words no dictionary knows.
    for w in lower_seen:
        if w in rows or len(w) < 3:
            continue
        if w in lemma_words or not in_lexicon(w):
            rows[w] = {"word": w, "kind": "translit", "count": any_case[w]}

    out = []
    for w, r in sorted(rows.items(), key=lambda kv: (-kv[1]["count"], kv[0])):
        r["dict"] = dict_of(w) if in_lexicon(w) else "none"
        r["current_us"] = g2p(w)[0]
        r["current_gb"] = g2p_gb(w)[0]
        r["example"] = example.get(w, "")
        out.append(r)
    (HERE / "candidates.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    # Review batches of about 200 words, most frequent first. Batches already
    # written are kept as they are, since names/reviewed matches them by file
    # name; only words not in any batch yet go into new batches after the last.
    bdir = HERE / "batches"
    bdir.mkdir(exist_ok=True)
    seen, last = set(), 0
    for bf in sorted(bdir.glob("batch-*.json")):
        seen |= {r["word"] for r in json.loads(bf.read_text(encoding="utf-8"))}
        last = max(last, int(bf.stem.split("-")[1]))
    fresh = [r for r in out if r["word"] not in seen]
    size = 200
    for i in range(0, len(fresh), size):
        last += 1
        (bdir / f"batch-{last:02d}.json").write_text(
            json.dumps(fresh[i:i + size], ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(fresh)} new words in new batches")
    c = Counter((r["kind"], r["dict"]) for r in out)
    print(len(out), "candidates", dict(c))


if __name__ == "__main__":
    main()
