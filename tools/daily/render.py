# -*- coding: utf-8 -*-
"""Render the two cards and the landing page for dailies.

  python render.py              render every verse whose card or page is missing
  python render.py SLUG [...]   (re)render just these
  python render.py --all        re-render everything (rarely needed)

Outputs per slug, all under public/daily/:
  <slug>.png          vertical status card 1080x1920
  <slug>-share.png    landscape share card 1200x630 (og:image)
  <slug>/index.html   landing page
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib
import gen_cards as gc

TEMPLATE = open(os.path.join(lib.HERE, "page_template.html"), encoding="utf-8").read()


def esc_attr(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


def esc_html(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def outputs(slug):
    return (os.path.join(lib.PUBLIC, f"{slug}.png"),
            os.path.join(lib.PUBLIC, f"{slug}-share.png"),
            os.path.join(lib.PUBLIC, slug, "index.html"))


def writeup_html(story):
    return "".join(f"<p>{esc_html(p)}</p>" for p in story)


def render(v):
    slug, ref, verse = v["slug"], v["ref"], v["verse"]
    for s in [verse, ref] + v["story"]:
        if any(c in s for c in lib.DASHES):
            raise SystemExit(f"{slug}: em or en dash found, fix the verse file first")
    vpng, spng, page = outputs(slug)
    os.makedirs(os.path.dirname(page), exist_ok=True)
    gc.render_vertical(verse, ref).save(vpng, optimize=True)
    gc.render_share(verse, ref).save(spng, optimize=True)
    html = TEMPLATE.format(
        ref=esc_attr(ref), verse=esc_attr(verse), slug=slug,
        study_url=lib.SITE + v["studyUrl"],
        writeup_html=writeup_html(v["story"]),
        share_text_js=json.dumps('"' + verse + '" (' + ref + ')'),
    )
    with open(page, "w", encoding="utf-8") as f:
        f.write(html)


def main(argv):
    verses = lib.load_all_verses()
    if "--all" in argv:
        todo = list(verses)
    elif argv:
        todo = argv
    else:
        todo = [s for s in verses if not all(os.path.exists(p) for p in outputs(s))]
    for s in todo:
        if s not in verses:
            raise SystemExit(f"no verse file for {s}")
        if not verses[s].get("story"):
            print(f"skip {s}: no write-up yet")
            continue
        render(verses[s])
        print(f"rendered {s}")
    print(f"{len(todo)} rendered")


if __name__ == "__main__":
    main(sys.argv[1:])
