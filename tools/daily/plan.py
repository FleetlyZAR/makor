# -*- coding: utf-8 -*-
"""What the next run should write.

  python plan.py           human readable
  python plan.py --json    machine readable

Lists every open date from today to today + HORIZON_DAYS - 1, with its church
season hint, plus the books used on the days either side (never repeat a book on
consecutive days) and the references already in the library (never reuse one).
"""
import datetime as dt
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib


def main(argv):
    cal = lib.load_calendar()
    verses = lib.load_all_verses()
    t = lib.today()
    open_dates = []
    for i in range(lib.HORIZON_DAYS):
        d = t + dt.timedelta(days=i)
        if lib.iso(d) not in cal:
            nb = []
            for k in (-1, 1):
                s = cal.get(lib.iso(d + dt.timedelta(days=k)))
                if s and s in verses:
                    nb.append(lib.book_folder(lib.parse_ref(verses[s]["ref"])[0]))
            open_dates.append({"date": lib.iso(d), "weekday": d.strftime("%A"),
                               "season": lib.season(d), "avoid_books": nb})
    recent = [verses[cal[k]]["ref"] for k in sorted(cal)[-30:] if cal[k] in verses]
    data = {"today": lib.iso(t), "open": open_dates,
            "recent_refs": recent,
            "library_refs": sorted(v["ref"] for v in verses.values())}
    if "--json" in argv:
        print(json.dumps(data, indent=1))
        return
    print(f"today {data['today']}; {len(open_dates)} open dates in the next {lib.HORIZON_DAYS} days")
    for o in open_dates:
        print(f"  {o['date']} {o['weekday']:<9} {o['season'] or '-':<50} avoid: {', '.join(o['avoid_books']) or '-'}")
    print(f"last 30 on the calendar: {', '.join(recent)}")


if __name__ == "__main__":
    main(sys.argv[1:])
