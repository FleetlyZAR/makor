#!/usr/bin/env python3
"""
Validate the Go deeper level of Makor studies against DEEPER-HANDOFF.md.

    python3 tools/deeper/check.py <study.json> [...]
    python3 tools/deeper/check.py --book genesis
    python3 tools/deeper/check.py --all --summary     # also writes progress.json

A study passes when every Go deeper field meets its minimum depth, no field
restates the basic paragraph, every Scripture reference exists in the BSB, the
house rules hold, and nothing outside the Go deeper keys changed from git HEAD.
Exit code 1 if any study fails.
"""
import argparse
import json
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STUDIES = ROOT / "src" / "content" / "studies"
DB = ROOT / "tools" / "scripture" / "makor-scripture.db"

MIN_WORDS = {
    ("context", "literary"): 150, ("context", "historical"): 150, ("context", "canonical"): 150,
    ("hermeneutics", "authorIntent"): 120, ("hermeneutics", "descriptionVsPrescription"): 100,
    ("originalLanguages",): 350, ("christ",): 300, ("god",): 300, ("oneStory",): 250,
}
BASIC_OF = {"context": "context", "hermeneutics": "hermeneutics", "originalLanguages": "originalLanguages",
            "typology": "typology", "christ": "christ", "god": "god",
            "crossReferences": "crossReferences", "oneStory": "oneStory"}
DEEP_KEYS = set(BASIC_OF)
# Keys a deepening pass may not change (compared with git HEAD). translationNotes
# and meta are excluded so separate clean ups do not trip this check.
FROZEN_TOP = ("schemaVersion", "book", "section", "text", "lexicon", "quiz", "questions")
MAX_FIELD_OVERLAP = 0.30
MAX_SENTENCE_SIM = 0.60

STOP = set("""a an and the of to in is it its that this these those for on with by as at be are was were
from or not but who whom whose which what when where why how all any each every he she they them his her
their him we us our you your i me my so than then there here into onto upon out up down over under also
only even just very more most much many such can could would should will shall may might must do does did
has have had been being if because while though although yet both either neither nor no one two three
god lord lords jesus christ own same other another through toward towards about again""".split())
WORD = re.compile(r"[A-Za-z][A-Za-z']+")


def words(text):
    return WORD.findall(text or "")


def content(text):
    return {w.lower().strip("'") for w in words(text) if w.lower() not in STOP and len(w) > 2}


def sentences(text):
    return [s for s in re.split(r"(?<=[.!?;])\s+", text or "") if len(words(s)) >= 6]


def flat(x):
    if isinstance(x, str):
        return x
    if isinstance(x, dict):
        return " ".join(flat(v) for v in x.values())
    if isinstance(x, list):
        return " ".join(flat(v) for v in x)
    return ""


# ---------------------------------------------------------------- references
BOOKS = {}
VERSES = {}


def load_db():
    if VERSES:
        return
    c = sqlite3.connect(str(DB))
    for bid, common, name in c.execute("select id, commonName, name from book"):
        BOOKS[common.lower()] = bid
        BOOKS[name.lower()] = bid
    BOOKS.update({"psalm": "PSA", "song of solomon": "SNG", "canticles": "SNG"})
    for bid, ch, n in c.execute("select bookId, chapter, max(verse) from verse group by bookId, chapter"):
        VERSES[(bid, ch)] = n


BOOK_RE = r"(?:[123] )?(?:Song of Solomon|Song of Songs|[A-Z][a-z]+)"
REF = re.compile(rf"\b({BOOK_RE}) (\d+):(\d+)(?:-(\d+)(?::(\d+))?)?")


def bad_refs(text):
    load_db()
    out = []
    for m in REF.finditer(text or ""):
        book, ch, v1, v2, v3 = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4), m.group(5)
        bid = BOOKS.get(book.lower())
        if not bid:
            continue  # not a book name (for example "Verse 3:4" never occurs); ignore
        if (bid, ch) not in VERSES:
            out.append(m.group(0))
            continue
        last = VERSES[(bid, ch)]
        if v1 > last:
            out.append(m.group(0))
        elif v2 and not v3 and int(v2) > last:
            out.append(m.group(0))
        elif v3 and ((bid, int(v2)) not in VERSES or int(v3) > VERSES[(bid, int(v2))]):
            out.append(m.group(0))
    return out


# ---------------------------------------------------------------- checks
def head_version(path):
    rel = path.resolve().relative_to(ROOT).as_posix()
    r = subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=ROOT, capture_output=True, text=True)
    return json.loads(r.stdout) if r.returncode == 0 else None


def check(path):
    fails, warns = [], []
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        return {"file": str(path), "ok": False, "fails": [f"invalid JSON: {e}"], "warns": []}
    s = doc.get("study", {}) or {}
    basic = s.get("basic", {}) or {}

    head = head_version(path)
    if head:
        for k in FROZEN_TOP:
            if head.get(k) != doc.get(k):
                fails.append(f"changed frozen key {k}")
        hs = head.get("study", {}) or {}
        for k in set(hs) | set(s):
            if k not in DEEP_KEYS and hs.get(k) != s.get(k):
                fails.append(f"changed frozen key study.{k}")

    for keys, minimum in MIN_WORDS.items():
        v = s
        for k in keys:
            v = (v or {}).get(k) if isinstance(v, dict) else None
        n = len(words(v if isinstance(v, str) else ""))
        if n < minimum:
            fails.append(f"{'.'.join(keys)}: {n} words, needs {minimum}")

    typ = s.get("typology") or []
    if len(typ) < 3:
        fails.append(f"typology: {len(typ)} entries, needs 3")
    for i, t in enumerate(typ):
        n = len(words(t.get("fulfillment", "")))
        if n < 60:
            fails.append(f"typology[{i}] fulfillment: {n} words, needs 60")
    xr = s.get("crossReferences") or []
    if len(xr) < 8:
        fails.append(f"crossReferences: {len(xr)} entries, needs 8")
    for i, c in enumerate(xr):
        n = len(words(c.get("note", "")))
        if n < 30:
            fails.append(f"crossReferences[{i}] ({c.get('ref','')}) note: {n} words, needs 30")
        if not REF.search(c.get("ref", "")) and not re.search(r"\d", c.get("ref", "")):
            warns.append(f"crossReferences[{i}] ref not a verse reference: {c.get('ref','')}")
    debates = (s.get("hermeneutics") or {}).get("debates") or []
    if len(debates) < 1:
        fails.append("hermeneutics.debates: none")
    elif len(debates) < 2:
        warns.append("hermeneutics.debates: only one (add a second where a real one exists)")

    for key, bkey in BASIC_OF.items():
        deep = flat(s.get(key))
        base = flat(basic.get(bkey))
        if not deep or not base:
            continue
        dc, bc = content(deep), content(base)
        if dc:
            ov = len(dc & bc) / len(dc)
            if ov > MAX_FIELD_OVERLAP:
                fails.append(f"{key}: overlap with basic {ov:.2f} (max {MAX_FIELD_OVERLAP})")
        bsents = [content(x) for x in sentences(base)]
        for sent in sentences(deep):
            sc = content(sent)
            for b in bsents:
                if sc and b and len(sc & b) / len(sc | b) > MAX_SENTENCE_SIM:
                    fails.append(f"{key}: restates basic: {sent[:90]}")
                    break

    deep_text = " ".join(flat(s.get(k)) for k in DEEP_KEYS)
    if re.search("[—–]", deep_text):
        fails.append("em or en dash in Go deeper")
    if "{{" in deep_text:
        fails.append("lexicon token {{..}} in Go deeper")
    if re.search("[֐-׿Ͱ-Ͽἀ-῿]", deep_text):
        fails.append("original script in Go deeper (transliterate instead)")
    if re.search(r"\bdash(es)?\b|house style|punctuat", deep_text, re.I):
        fails.append("mentions dashes or punctuation")
    refs = bad_refs(deep_text + " " + " ".join(c.get("ref", "") for c in xr))
    for r in sorted(set(refs)):
        fails.append(f"reference does not exist in the BSB: {r}")

    return {"file": path.relative_to(ROOT).as_posix(), "ok": not fails, "fails": fails, "warns": warns,
            "words": len(words(deep_text))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--book")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--summary", action="store_true", help="counts only, and write progress.json")
    args = ap.parse_args()
    if args.all:
        paths = sorted(STUDIES.glob("*/*.json"))
    elif args.book:
        paths = sorted((STUDIES / args.book).glob("*.json"))
    else:
        paths = [Path(f) for f in args.files]
    results = [check(p.resolve()) for p in paths]
    bad = [r for r in results if not r["ok"]]
    if args.summary:
        from collections import Counter
        books = Counter(r["file"].split("/")[3] for r in results)
        good = Counter(r["file"].split("/")[3] for r in results if r["ok"])
        prog = {b: {"done": good[b], "total": books[b]} for b in sorted(books)}
        if args.all:
            (Path(__file__).parent / "progress.json").write_text(json.dumps(
                {"passed": len(results) - len(bad), "total": len(results), "books": prog}, indent=1))
        for b in sorted(books):
            print(f"{b:18} {good[b]:3}/{books[b]}")
    else:
        for r in results:
            print(("PASS " if r["ok"] else "FAIL ") + r["file"] + (f"  ({r.get('words',0)} deep words)" if r["ok"] else ""))
            for f in r["fails"]:
                print("   x", f)
            for w in r["warns"]:
                print("   ~", w)
    print(f"\n{len(results) - len(bad)} of {len(results)} pass")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
