# -*- coding: utf-8 -*-
"""Ortswahl bei Ereignissen mit "ort_waehlen" (18.10.2026): Lolas und Alvas Handy-Abende fuehren in eine Szene am
gewaehlten Ort - frueher stuerzte die Engine dort ab (Ort "frei"). Prueft: Ortsliste, Wahl, Ersatzort, Szenenstart.

  python tests\\test_ortswahl.py
"""
import os, sys, tempfile

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import lauf_test as L  # noqa: E402  (Stubs: kein Modell, kein Netz)

E = L.eden


def lauf_bis_tag(tag):
    """Wegwerf-Durchlauf bis zum Morgen von <tag> (Bot aus lauf_test), Spielstand zurueck."""
    L.vorbereiten("eden_rise", tempfile.mkdtemp(prefix="eden_ort_"))
    L.random.seed(5)
    protokoll = {"schritte": [], "erledigt": {}}
    z = E.aktion("neu", {"modus": "ironman"})
    while z["tag"] < tag and z["status"] != "ende":
        a = L.schritt(z, protokoll)
        if a[0] == "_tagesarbeit":
            L.tagesarbeit(z, protokoll)
        else:
            L.versuch(a, protokoll)
        z = E.aktiv()
    return z


def ereignis_erzwingen(z, eid, werte, flags):
    """Voraussetzungen setzen und das Ereignis direkt oeffnen (nur im Test)."""
    z["werte"].update(werte)
    z["flags"] += [f for f in flags if f not in z["flags"]]
    z["event"] = {"id": eid, "tag": z["tag"], "phase": z["phase"], "ergebnis": None,
                  "weiter": "wahl", "status_vorher": "wahl"}
    z["status"] = "ereignis"
    E.sichern(z)


def pruefen(eid, pid, flags):
    z = lauf_bis_tag(5)
    modul = E.modul_laden()
    ereignis_erzwingen(z, eid, {"vertrauen." + pid: 4}, flags)
    ev = E.ereignisse.daten(E.moddir())["_index"][eid]
    i = next(k for k, o in enumerate(ev["optionen"]) if o.get("art") == "ort_waehlen")
    orte = E.ereignisse.ort_auswahl(z, modul, pid)
    assert orte, "keine Orte zur Wahl"
    ansicht = E.ansicht(E.aktiv())["z"]["ereignis"]
    assert ansicht["optionen"][i]["orte"] == orte, "Anzeige zeigt andere Orte als die Engine"
    ziel = orte[-1]["id"]
    E.aktion("event_wahl", {"index": i, "ort": ziel})
    z = E.aktion("event_schliessen", {})
    assert z["status"] == "szene", z["status"]
    assert z["szene"]["def"]["ort"] == ziel, (z["szene"]["def"]["ort"], ziel)
    # ohne/ungueltiger Ort: Ersatz statt Absturz
    z = lauf_bis_tag(5)
    ereignis_erzwingen(z, eid, {"vertrauen." + pid: 4}, flags)
    E.aktion("event_wahl", {"index": i, "ort": "gibt_es_nicht"})
    z = E.aktion("event_schliessen", {})
    assert z["status"] == "szene" and z["szene"]["def"]["ort"] in modul["raeume"]
    print("OK %s: %d Orte, gewaehlt %s, Ersatz %s" % (eid, len(orte), ziel, z["szene"]["def"]["ort"]))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    pruefen("ab_lola_handy", "lola", ["lola_abend"])
    pruefen("ab_alva_handy", "alva", ["alva_abend"])
    print("OK")
