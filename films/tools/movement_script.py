#!/usr/bin/env python3
"""Shared generator for Makor movement film scripts.

A film's script/movement.py defines CHAPTERS (the beats) and calls build(). Scripture
is never typed in a film script: every verse comes from the study JSON and is split
into speaker lines automatically. The build stops if any verse is missing, repeated,
out of order or changed, if a quotation of other Scripture is not verbatim in the
study JSON, or if a dash appears.

Beats:
  ("V", "2:4", "2:7")          verses, split into READER, GOD (and any SPEAKERS override)
  ("GUIDE", text, source)      Makor's words, from the named study field
  ("Q", text, ref, speaker)    quotation of other Scripture, verbatim from the study JSON
  ("PIC", text)                what is on screen
  ("BEAT", seconds, text)      music or silence with no voice
  ("CARD", text)               on screen text

Speech detection: a quotation that follows an intro matching SPEECH (for example
"said," "commanded him,") is speech. Its speaker is GOD unless the intro names a
different subject listed in SUBJECTS (for example "the man said" -> "MAN"); then the
film's VOICE_MAP decides which voice reads it (Makor rule: anyone other than God is
read by the READER unless a film decides otherwise). Quoted single words such as
names ("day," "woman,") stay with the READER.
"""
import json, pathlib, re

WPM = {"READER": 185, "GOD": 140, "GUIDE": 155}
GAP = 0.6
SPEECH = re.compile(r"(said|said to them|commanded him|commanded them)[,:]\s*$")
SUBJECTS = {r"\bthe man said\b": "MAN", r"\bthe woman said\b": "WOMAN", r"\bthe serpent said\b": "SERPENT"}
PLAIN = lambda t: re.sub(r"\{\{[^|}]+\|([^}]+)\}\}", r"\1", t)


def tc(s):
    return f"{int(s // 60)}:{int(s % 60):02d}"


class Film:
    def __init__(self, here, study, voice_map=None):
        self.here = pathlib.Path(here)
        self.d = json.loads(pathlib.Path(study).read_text())
        self.study_text = json.dumps(self.d, ensure_ascii=False)
        self.verses = [(f"{v['chapter']}:{v['n']}", PLAIN(v["text"])) for u in self.d["text"]["units"]
                       for v in u["verses"]]
        self.vmap = dict(self.verses)
        self.voice_map = {"GOD": "GOD", "READER": "READER", **(voice_map or {})}
        durs = self.here / "movement-durations.json"
        self.real = json.loads(durs.read_text()) if durs.exists() else {}

    # ---------------------------------------------------------------- verses
    def speaker_of(self, intro):
        for pat, who in SUBJECTS.items():
            if re.search(pat, intro):
                return who
        return "GOD"

    def split_range(self, a, b, state):
        keys = [k for k, _ in self.verses]
        out = []
        for key in keys[keys.index(a): keys.index(b) + 1]:
            text, segs, i = self.vmap[key], [], 0
            if state.get("carry"):   # a speech carried over from the previous verse
                j = text.find("”")
                segs.append((state["carry"], text[: j + 1].strip())); i = j + 1; state["carry"] = None
            while i < len(text):
                j = text.find("“", i)
                if j < 0:
                    segs.append(("READER", text[i:].strip())); break
                before = text[i:j]
                k = text.find("”", j)
                intro = before if before.strip() else (segs[-1][1] if segs and segs[-1][0] == "READER" else "")
                if SPEECH.search(intro):
                    who = self.voice_map.get(self.speaker_of(intro), "READER")
                    if before.strip():
                        segs.append(("READER", before.strip()))
                    if k < 0:
                        segs.append((who, text[j:].strip())); state["carry"] = who; i = len(text)
                    else:
                        segs.append((who, text[j: k + 1].strip())); i = k + 1
                else:   # a quoted name stays with the READER
                    end = k + 1 if k >= 0 else len(text)
                    nxt = text.find("“", end)
                    stop = nxt if nxt >= 0 else len(text)
                    segs.append(("READER", text[i:stop].strip())); i = stop
            merged = []
            for sp, t in [s for s in segs if s[1]]:
                if merged and merged[-1][0] == sp == "READER":
                    merged[-1] = (sp, merged[-1][1] + " " + t)
                else:
                    merged.append((sp, t))
            assert " ".join(t for _, t in merged) == text, f"split changed {key}: {merged}"
            out.append((key, merged))
        return out

    def secs(self, speaker, text, lid=None):
        if lid in self.real:
            return self.real[lid] + GAP
        return len(re.findall(r"[\w']+", text)) / WPM.get(speaker, 170) * 60 + GAP

    # ---------------------------------------------------------------- build
    def build(self, chapters, header, footer="", book="Genesis"):
        state, t, used, body, spoken, events, chs = {}, 0.0, [], [], [], [], []
        words = {}

        def line(chapter, speaker, text, ref):
            lid = f"m{len(spoken) + 1:03d}"
            spoken.append({"id": lid, "chapter": chapter, "speaker": speaker, "text": text, "ref": ref})
            return lid

        for title, beats in chapters:
            chs.append((t, title))
            body.append(f"\n## {tc(t)}  {title}\n")
            for b in beats:
                k = b[0]
                ev = lambda kind, **kw: events.append({"t": round(t, 3), "kind": kind, "chapter": title, **kw})
                if k == "PIC":
                    body.append(f"*Picture:* {b[1]}\n"); ev("pic", text=b[1])
                elif k == "BEAT":
                    body.append(f"*{b[1]} s, no voice:* {b[2]}\n"); ev("beat", dur=b[1], text=b[2]); t += b[1]
                elif k == "CARD":
                    body.append(f"`ON SCREEN` {b[1]}\n"); ev("card", text=b[1])
                elif k == "GUIDE":
                    lid = line(title, "GUIDE", b[1], b[2]); ev("line", id=lid, speaker="GUIDE", text=b[1])
                    body.append(f"**GUIDE** {b[1]}  <sub>[{b[2]}] {lid}</sub>\n")
                    t += self.secs("GUIDE", b[1], lid); words["GUIDE"] = words.get("GUIDE", 0) + len(b[1].split())
                elif k == "Q":
                    assert b[1] in self.study_text, f"quotation not verbatim in study JSON: {b[1]}"
                    lid = line(title, b[3], b[1], b[2]); ev("line", id=lid, speaker=b[3], text=b[1], ref=b[2])
                    body.append(f"**{b[3]}** {b[1]}  <sub>({b[2]}, quoted verbatim from the study) {lid}</sub>\n")
                    t += self.secs(b[3], b[1], lid); words[b[3]] = words.get(b[3], 0) + len(b[1].split())
                elif k == "V":
                    for key, segs in self.split_range(b[1], b[2], state):
                        used.append(key)
                        ids = [line(title, sp, tx, f"{book} {key}") for sp, tx in segs]
                        body.append(f"<sub>{book} {key}</sub>  " + "  ".join(f"**{sp}** {tx}" for sp, tx in segs)
                                    + f"  <sub>{' '.join(ids)}</sub>\n")
                        for (sp, tx), lid in zip(segs, ids):
                            ev("line", id=lid, speaker=sp, text=tx, ref=f"{book} {key}")
                            t += self.secs(sp, tx, lid); words[sp] = words.get(sp, 0) + len(tx.split())
        allkeys = [k for k, _ in self.verses]
        assert used == allkeys, f"verses missing, repeated or out of order: {set(allkeys) ^ set(used)}"
        text = "".join(body)
        assert "–" not in text and "—" not in text, "dash found"
        # (the banned word list applies to image prompts, not narration; see films/STYLE-BIBLE.md)
        basis = "from the rendered voice track" if self.real else "estimated from word counts"
        head = header.format(total=tc(t), basis=basis, n=len(allkeys),
                             words=", ".join(f"{k} {v}" for k, v in sorted(words.items())),
                             chapters="\n".join(f"{tc(s)} {name}" for s, name in chs))
        (self.here / "movement-script.md").write_text(head + text + footer)
        (self.here / "movement-lines.json").write_text(json.dumps(spoken, indent=1, ensure_ascii=False))
        (self.here / "movement-timeline.json").write_text(json.dumps(
            {"total": round(t, 3), "gap": GAP, "chapters": [[round(a, 3), n] for a, n in chs], "events": events},
            indent=1, ensure_ascii=False))
        print(f"wrote movement-script.md: {len(allkeys)} verses verified, runtime {tc(t)} ({basis}); {words}")
