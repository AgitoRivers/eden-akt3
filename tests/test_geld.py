# -*- coding: utf-8 -*-
"""Geld-Balancing (Duc 28./29.10.2026, beute.md 3, Brain Trust): Gage 125 EUR, Geld nur von Menschen je Gefahrenstufe,
Rosi 150/400 EUR, Megans Probezeit-Satz in ihrer ersten Sprachnachricht.

  python tests\\test_geld.py
"""
import copy, json, os, sys

EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, EDEN)
from kern import ereignisse, handel, kampf, zustand  # noqa: E402

MOD = os.path.join(EDEN, "module", "eden_rise")
MODUL = json.load(open(os.path.join(MOD, "modul.json"), encoding="utf-8"))
DEFS = copy.deepcopy(kampf.daten(MOD))


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def kampf_fuer(eid):
    z = zustand.neu(MODUL, "entspannt")
    zustand.persona_setzen(z, MODUL, MODUL["personas"][0])
    z["tag"], z["phase"] = 3, "tag"
    bid = next(b for b, e in DEFS["encounters"].items() if e.get("enemy") == eid and not e.get("training"))
    kampf.starten(z, DEFS, bid)
    return z


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    pruefen(MODUL["geld"]["honorar"] == 125, "Gage 125 EUR am Tag")
    pruefen([s["geld"] for s in DEFS["werkstatt"]["stufen"]] == [150, 400], "Rosi 150 / 400 EUR")
    cfg = DEFS["geld_drop"]
    pruefen(cfg["klassen"] == ["mensch"], "Geld nur von Menschen")

    menschen = [e for e, d in DEFS["enemies"].items() if d.get("cls") == "mensch"]
    andere = [e for e, d in DEFS["enemies"].items() if d.get("cls") != "mensch"]
    fertig = 0
    for eid in menschen + andere:
        try:
            z = kampf_fuer(eid)
        except StopIteration:
            continue
        k, g = z["kampf"], z["kampf"]["gegner"][0]
        n = kampf.geld_drop(z, k, g)
        span = cfg["spanne"].get(g["def"]["tier"])
        if eid in menschen:
            pruefen(span and span[0] <= n <= span[1], "%s (%s): %d EUR in %s" % (eid, g["def"]["tier"], n, span))
            pruefen(n == kampf.geld_drop(z, k, g), "%s: Betrag fest je Kampf" % eid)
        else:
            pruefen(n == 0, "%s (%s): kein Geld" % (eid, g["def"]["cls"]))
        fertig += 1
    pruefen(fertig >= 10, "genug Gegner geprueft (%d)" % fertig)

    # Tasche 8 / 12 / 16 bei Rosi (Duc 29.10.2026): je Akt ein Upgrade, nur Geld
    z = zustand.neu(MODUL, "entspannt")
    zustand.persona_setzen(z, MODUL, MODUL["personas"][0])
    pruefen(zustand.inventar_plaetze(z, MODUL) == 8, "Start-Tasche 8 Plaetze")
    z["tag"], z["konto"] = 8, 5000
    pruefen(handel.tasche_ansicht(z, MODUL)["naechste"]["fehlt"], "Werkstatt zu: keine Tasche")
    z["flags"].append("werkstatt_offen")
    z["tag"] = 7
    pruefen(handel.tasche_ansicht(z, MODUL)["naechste"]["fehlt"], "Tag 7: Diving Bag noch nicht")
    z["tag"] = 8
    titel, satz, zeilen = handel.tasche_kaufen(z, MODUL)
    pruefen(z["konto"] == 4600 and zustand.inventar_plaetze(z, MODUL) == 12 and satz, "%s: 400 EUR, 12 Plaetze" % titel)
    try:
        handel.tasche_kaufen(z, MODUL)
        pruefen(False, "Expedition Pack vor Akt 3")
    except ValueError as e:
        pruefen(True, "Expedition Pack vor Akt 3 gesperrt (%s)" % e)
    z["tag"], z["konto"] = 23, 5000
    pruefen(handel.tasche_ansicht(z, MODUL)["naechste"]["fehlt"], "Tag 23 (Belagerung): Expedition Pack noch nicht")
    z["tag"], z["konto"] = 24, 799                   # Akt 3 beginnt an Tag 24 (E-114, fix-akt2)
    pruefen("1 €" in (handel.tasche_ansicht(z, MODUL)["naechste"]["fehlt"] or ""), "799 EUR: 1 EUR fehlt")
    z["konto"] = 800
    titel, satz, zeilen = handel.tasche_kaufen(z, MODUL)
    pruefen(z["konto"] == 0 and zustand.inventar_plaetze(z, MODUL) == 16, "%s: 800 EUR, 16 Plaetze" % titel)
    pruefen(handel.tasche_ansicht(z, MODUL)["naechste"] is None, "Tasche voll ausgebaut")

    ev = ereignisse.daten(MOD)["_index"]["mg_tag2"]
    pruefen(any("probation rate" in zl["text"] for zl in ev["zeilen"]), "Megan begruendet die halbe Gage (mg_tag2)")
    print("alle Geld-Tests gruen")


if __name__ == "__main__":
    main()
