# -*- coding: utf-8 -*-
"""Meramie nach den Bergen (Duc 29.10.2026): Petru gibt seine alte Jacke in jedem Weg - C warm (bg_c_jacke, abends),
A kuehl als Bezahlung (bg_a_jacke), B ueber die Versoehnung (test_petru_weg_b.py). Jedes Mal genau einmal, immer ueber
das Flag jacke_jacket_water, und danach ist die Jacke wirklich im Besitz.

  python tests\\test_petru_jacke.py
"""
import json, os, sys, tempfile

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import lauf_test as L  # noqa: E402

E = L.eden


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    L.vorbereiten("eden_rise", tempfile.mkdtemp(prefix="eden_petru_jacke_"))
    modul = E.modul_laden()
    ev = {e["id"]: e for e in json.load(open(os.path.join(E.moddir("eden_rise"), "ereignisse.json"),
                                             encoding="utf-8"))["events"]}
    regeln, zustand, kampf = E.regeln, E.zustand, E.kampf
    defs = kampf.daten(E.moddir("eden_rise"))
    for eid, weg in (("bg_c_jacke", "bg_weg_c_gewonnen"), ("bg_a_jacke", "bg_adrien_verhaftet")):
        z = E.aktion("neu", {"modus": "ironman"})
        z["tag"] = 12
        e = ev[eid]
        bed = e["wann"]["bedingung"]
        pruefen(not regeln.gilt(bed, z, {}), "%s: nicht ohne die Berge" % eid)
        z["flags"] += [weg]
        pruefen(not regeln.gilt(bed, z, {}), "%s: erst wenn die Berge vorbei sind" % eid)
        z["flags"] += ["berge_fertig"]
        pruefen(regeln.gilt(bed, z, {}), "%s: nach Weg %s" % (eid, weg))
        anderer = "bg_c_jacke" if eid == "bg_a_jacke" else "bg_a_jacke"
        pruefen(not regeln.gilt(ev[anderer]["wann"]["bedingung"], z, {}), "%s: der andere Weg bleibt zu" % eid)
        pruefen(not regeln.gilt(ev["bg_b_versoehnung"]["wann"]["bedingung"], z, {}), "%s: keine Weg-B-Versoehnung" % eid)
        pruefen(all({"flag": "jacke_jacket_water"} in o["folgen"] for o in e["optionen"]), "%s: jede Antwort gibt die Jacke" % eid)
        zustand.folgen_anwenden(z, modul, e["optionen"][0]["folgen"])
        pruefen("jacket_water" in kampf.besitz(z, defs)["armors"], "%s: Meramie im Besitz" % eid)
        pruefen(not regeln.gilt(bed, z, {}), "%s: kommt nur einmal" % eid)
    print("OK")


if __name__ == "__main__":
    main()
