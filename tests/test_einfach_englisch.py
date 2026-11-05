# -*- coding: utf-8 -*-
"""Einfaches Englisch in allen Akt-3-Texten (Duc 05.11.2026): Lage, Zeilen, Chips und Antworten der a3_-Events,
die Kommission und die Legenden zu Akt-3-Taten. Woerterliste: werkzeuge/eden_rise/einfach_englisch.py."""
import json, os, sys
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "werkzeuge", "eden_rise"))
import einfach_englisch as EE

M = os.path.join(BASE, "module", "eden_rise")


def texte():
    out = []
    for e in json.load(open(os.path.join(M, "ereignisse.json"), encoding="utf-8"))["events"]:
        if not e["id"].startswith("a3_"):
            continue
        out.append((e["id"], e.get("lage", "")))
        out.append((e["id"], e.get("titel", "")))
        for z in e.get("zeilen") or []:
            out.append((e["id"], z.get("text", "")))
        for o in e.get("optionen") or []:
            out.append((e["id"], o.get("text", "")))
            if isinstance(o.get("zeile"), dict):
                out.append((e["id"], o["zeile"].get("text", "")))
    k = json.load(open(os.path.join(M, "kommission.json"), encoding="utf-8"))
    def alle(x, stelle):
        if isinstance(x, dict):
            for v in x.values():
                alle(v, stelle)
        elif isinstance(x, list):
            for v in x:
                alle(v, stelle)
        elif isinstance(x, str) and " " in x:
            out.append((stelle, x))
    for teil in ("texte", "runden", "karten", "plaedoyer"):
        alle(k.get(teil), "kommission." + teil)
    leg = json.load(open(os.path.join(M, "legenden.json"), encoding="utf-8"))
    for zid, z in leg["zeilen"].items():
        if z.get("tat") in ("schwur", "anwalt", "mast"):
            out.append(("legende." + zid, z.get("text", "")))
    return out


funde = EE.pruefen(texte())
for stelle, wort, vorschlag in funde:
    print("%s: \"%s\" -> %s" % (stelle, wort, vorschlag))
assert not funde, "%d Stellen in schwerem Englisch" % len(funde)
print("ok test_einfach_englisch (%d Texte)" % len(texte()))
