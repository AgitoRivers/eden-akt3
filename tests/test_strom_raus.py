# -*- coding: utf-8 -*-
"""Strom und Diesel ausgebaut (Duc 30.10.2026, E-082): das Modul kennt die Werte nicht mehr, kein Event, keine Bordregel,
kein Laden und kein Szenen-Fund bewegt sie, der Bordstatus fuers Modell nennt keine Batterie - und ein alter Spielstand,
der noch Strom/Diesel in z["werte"] traegt, laeuft ohne Fehler weiter (Folgen darauf werden ignoriert).

  python tests\\test_strom_raus.py
"""
import json, os, sys, tempfile

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import lauf_test as L  # noqa: E402

E = L.eden
WEG = ("strom", "diesel")
WAREN = ("diesel_canister", "used_battery", "panel_cleaner")


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def werte_in(x):
    """Alle Wert-Namen, die irgendwo als Folge oder Bedingung vorkommen."""
    if isinstance(x, dict):
        for k, v in x.items():
            if k == "wert" and isinstance(v, str):
                yield v
            elif k == "wert" and isinstance(v, list) and v and isinstance(v[0], str):
                yield v[0]
            yield from werte_in(v)
    elif isinstance(x, list):
        for v in x:
            yield from werte_in(v)


def main():
    L.vorbereiten("eden_rise", tempfile.mkdtemp(prefix="eden_stromraus_"))
    modul = E.modul_laden("eden_rise")
    md = E.moddir("eden_rise")
    pruefen(not any(w in modul["werte"] for w in WEG), "Modul hat keine Werte Strom/Diesel")
    ev = json.load(open(os.path.join(md, "ereignisse.json"), encoding="utf-8"))
    pruefen(not any(w in WEG for w in werte_in(ev)), "kein Event bewegt oder prueft Strom/Diesel")
    pruefen(not any(w in WEG for w in werte_in(modul.get("bordregeln") or {})), "keine Bordregel gibt Strom")
    for lid, l in modul["laeden"].items():
        pruefen(not any(i in WAREN for i in l.get("immer", [])) and not any(i in WAREN for i in l.get("aufschlag", {})),
                "Laden %s fuehrt keine Strom/Diesel-Ware" % lid)
    for i in WAREN:
        pruefen(modul["items"][i].get("pausiert") and not modul["items"][i].get("wirkung"), "%s ruht ohne Wirkung" % i)

    L.random.seed(5)
    z = E.aktion("neu", {"modus": "ironman"})
    pruefen(not any(w in z["werte"] for w in WEG), "neues Spiel startet ohne Strom/Diesel")
    z["werte"].update(strom=4, diesel=2)                     # alter Spielstand
    zeilen = E.zustand.folgen_anwenden(z, modul, [{"wert": "strom", "delta": 1}, {"wert": "diesel", "delta": -1}])
    pruefen(zeilen == [] and z["werte"]["strom"] == 4, "Folgen auf Strom/Diesel werden still ignoriert")
    status = E.szene.bordstatus(z, modul)
    pruefen("Battery" not in status and "diesel" not in status.lower(), "Bordstatus fuers Modell ohne Batterie/Diesel")
    a = E.ansicht(z)
    pruefen(a is not None, "Ansicht mit altem Strom/Diesel im Spielstand laeuft")
    print("\nalle Strom-raus-Tests bestanden")


if __name__ == "__main__":
    main()
