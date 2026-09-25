#!/usr/bin/env python3
"""
Flag lexicon entries that could override an ordinary English word.

A lower case entry (say "plane" for the Greek planē) would also change the
English word wherever it is spoken. This lists every lexicon key that misaki's
English dictionary also knows, with a few spoken contexts, so each can be kept,
narrowed to case "exact", or dropped.

    .venv/bin/python names/audit.py
"""
import glob
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE.parent))
import generate_audio as ga  # noqa: E402
from misaki import en  # noqa: E402

golds = en.G2P(trf=False, british=False, fallback=None).lexicon.golds
lex = json.loads((HERE / "lexicon.json").read_text(encoding="utf-8"))["entries"]
risky = {w: e for w, e in lex.items() if w.lower() in golds and (w[0].islower() or e.get("case") == "any")}

texts = []
for f in sorted(glob.glob(str(ROOT / "src/content/studies/*/*.json"))):
    doc = json.loads(Path(f).read_text(encoding="utf-8"))
    texts += [s["text"] for s in ga.build_segments(doc, "both", {})]
blob = "\n".join(texts)
for w, e in sorted(risky.items()):
    flags = 0 if e.get("case") == "exact" else re.IGNORECASE
    hits = [m for m in re.finditer(rf"(?<![\w]){re.escape(w)}(?![\w])", blob, flags)]
    print(f"\n{w}  ({e.get('case')}, {e.get('say')})  {len(hits)} spoken")
    for m in hits[:4]:
        print("    ...", blob[max(0, m.start() - 60):m.end() + 40].replace("\n", " "))
