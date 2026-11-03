# -*- coding: utf-8 -*-
"""Petru nach Weg B in den Bergen (Duc + Brain Trust 29.10.2026): dunkler Laden (kalte Zeilen, Fisch -20 %, keine
Geschichten), Laetitias Karte frühestens 3 Tage nach dem Rauswurf, Versöhnung mit Meramie - danach wieder normal.

  python tests\\test_petru_weg_b.py
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
    L.vorbereiten("eden_rise", tempfile.mkdtemp(prefix="eden_petru_b_"))
    z = E.aktion("neu", {"modus": "ironman"})
    modul = E.modul_laden()
    mid = z["modul"]
    abbau, regeln, zustand = E.abbau, E.regeln, E.zustand
    z["tag"] = 12
    fisch = json.load(open(os.path.join(E.moddir(mid), "kuechen.json"), encoding="utf-8"))["fische"][0]["id"]
    normal_preis = abbau.fisch_preis(z, modul, fisch)
    normal = E.laden_auftritt(z, modul, mid, "petru")

    # Rauswurf (bg_hafen_b): datiertes Flag
    zustand.folgen_anwenden(z, modul, [{"flag_datiert": "petru_werkstatt_zu_duc"}])
    pruefen(abbau.petru_kalt(z), "nach Weg B ist Petru kalt")
    kalt = E.laden_auftritt(z, modul, mid, "petru")
    pruefen(kalt["gruss"]["id"].startswith("laden.petru.kalt_gruss") and kalt["text"] != normal["text"],
            "dunkler Laden: kalte Begruessung und eigene Lage (Radio aus)")
    pruefen(abbau.fisch_preis(z, modul, fisch) < normal_preis, "Fisch bringt weniger")

    ev = {e["id"]: e for e in json.load(open(os.path.join(E.moddir(mid), "ereignisse.json"), encoding="utf-8"))["events"]}
    karte, vers = ev["bg_b_postkarte"], ev["bg_b_versoehnung"]
    pruefen(not regeln.gilt(karte["wann"]["bedingung"], z, {}), "Karte nicht sofort")
    z["tag"] += 3
    pruefen(regeln.gilt(karte["wann"]["bedingung"], z, {}), "Karte nach drei Tagen")
    pruefen(not regeln.gilt(vers["wann"]["bedingung"], z, {}), "Versoehnung erst mit der Karte")
    zustand.folgen_anwenden(z, modul, karte["optionen"][1]["folgen"])          # erst behalten
    pruefen(not regeln.gilt(vers["wann"]["bedingung"], z, {}), "behaltene Karte: noch keine Versoehnung")
    z["tag"] += 2
    pruefen(regeln.gilt(vers["wann"]["bedingung"], z, {}), "behaltene Karte: Versoehnung nach zwei Tagen")
    vt = z["werte"].get("vertrauen.petru", 0)
    zustand.folgen_anwenden(z, modul, vers["optionen"][0]["folgen"])
    pruefen(not abbau.petru_kalt(z) and "jacke_jacket_water" in z["flags"], "Versoehnung: Laden wieder normal, Meramie frei")
    pruefen(E.laden_auftritt(z, modul, mid, "petru")["gruss"]["id"].startswith("laden.petru.gruss."), "wieder die alte Begruessung")
    pruefen(not regeln.gilt(karte["wann"]["bedingung"], z, {}) and not regeln.gilt(vers["wann"]["bedingung"], z, {}),
            "Karte und Versoehnung kommen nur einmal")
    pruefen(z["werte"].get("vertrauen.petru", 0) == vt, "die -40 Vertrauen bleiben (Versoehnung schenkt nichts zurueck)")
    print("OK")


if __name__ == "__main__":
    main()
