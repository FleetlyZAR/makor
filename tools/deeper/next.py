#!/usr/bin/env python3
"""
Print the next studies still needing a Go deeper rewrite, in canonical order.

A study counts as done when tools/deeper/check.py passes it, so this needs no
bookkeeping: whatever passed last run is skipped automatically.

    python3 tools/deeper/next.py 8          # the next 8 unfinished studies
    python3 tools/deeper/next.py 8 --json   # as groups of 4, for agents
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import check  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
queue = json.loads((Path(__file__).parent / "queue.json").read_text())["chunks"]
n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 8
todo = []
for c in queue:
    for f in c["files"]:
        if len(todo) >= n:
            break
        if not check.check((ROOT / f).resolve())["ok"]:
            todo.append(f)
if "--json" in sys.argv:
    print(json.dumps([todo[i:i + 4] for i in range(0, len(todo), 4)]))
else:
    print("\n".join(todo))
