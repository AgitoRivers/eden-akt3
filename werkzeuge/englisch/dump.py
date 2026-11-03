# -*- coding: utf-8 -*-
r"""Read-only: all player-visible texts of one event builder file, with their fixed keys (for the English rewrite).

    python werkzeuge\englisch\dump.py ereignisse_bordrat        -> prints  key | who/feeling | text
"""
import importlib, json, os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(os.path.dirname(HIER))
sys.path.insert(0, os.path.join(EDEN, "werkzeuge", "eden_rise"))


def ids_aus(modulname):
    m = importlib.import_module(modulname)
    return [e["id"] for e in m.EVENTS]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ids = set(ids_aus(sys.argv[1]))
    d = json.load(open(os.path.join(EDEN, "module", "eden_rise", "ereignisse.json"), encoding="utf-8"))
    for e in d["events"]:
        if e["id"] not in ids:
            continue
        k = e["id"]
        print("\n## %s  [%s, %s, %s]" % (k, e["art"], e["ton"], "/".join(str(x) for x in e["wann"]["tage"])))
        print("%s.titel | %s" % (k, e["titel"]))
        print("%s.lage | %s" % (k, e["lage"]))
        for b in e["personen"].get("betroffen", []):
            print("%s.betroffen.%s | %s" % (k, b["id"], b["was"]))
        for i, z in enumerate(e["zeilen"]):
            print("%s#z%d | %s/%s | %s" % (k, i, z["wer"], z["gefuehl"], z["text"]))
        for i, o in enumerate(e["optionen"]):
            print("%s.o%d | %s" % (k, i, o["text"]))
            if o.get("zeile"):
                print("%s#o%d | %s/%s | %s" % (k, i, o["zeile"]["wer"], o["zeile"]["gefuehl"], o["zeile"]["text"]))


if __name__ == "__main__":
    main()
