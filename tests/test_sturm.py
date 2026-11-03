# -*- coding: utf-8 -*-
"""Sturm an Tag 5 (27.10.2026, kern/sturm.py): Einteilen, Krisen, Sprint, Folgen, Vertonung.

  python tests\\test_sturm.py
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import eden as E  # noqa: E402
from kern import sturm, zustand, ermittlung  # noqa: E402

FEHLER = []
MOD = E.moddir("eden_rise")


def pruefen(ok, text):
    print(("✓ " if ok else "✗ ") + text)
    if not ok:
        FEHLER.append(text)


def zustand_tag5(modul):
    z = zustand.neu(modul, "ironman")
    z["tag"], z["phase"] = 5, "dinner"
    z["szene"] = {"def": {"id": "sturmvorbereitung", "titel": "Before the Storm"}, "log": [], "figuren": ["chiara", "rosi", "lea"]}
    return z


def nacht(z, modul, rennen=True):
    z["phase"] = "nacht"
    z["szene"] = {"def": {"id": "sturmnacht", "titel": "What You Hear in the Dark"}, "log": [], "figuren": ["chiara"]}
    sturm.beginnen(z, modul, MOD, "sturmnacht")
    while sturm.aktiv(z)["schritt"] == "sprint":
        sturm.sprint(z, modul, MOD, rennen)
    return sturm.aktiv(z)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    modul = E.modul_laden("eden_rise")
    D = sturm.daten(MOD)

    # Bester Plan: Duc prueft die Notloesung selbst, jede Person auf ihrem besten Posten, Lea ruht
    z = zustand_tag5(modul)
    pruefen(sturm.beginnen(z, modul, MOD, "sturmvorbereitung"), "Vorbereitung startet")
    v = sturm.aktiv(z)
    pruefen(v["schritt"] == "einteilen" and sum(1 for e in v["log"] if e["art"] == "bitte") == 5,
            "fünf Bitten, dann einteilen")
    sturm.einteilen(z, modul, MOD, {"anker": "chiara", "strom": "rosi", "kombuese": "lola", "beiboot": "maxwell",
                                    "notloesung": "duc"})
    arten = [e["art"] for e in v["log"]]
    pruefen(arten.count("zusage") == 4 and "ruhe" in arten and "tratsch" in arten,
            "jede Einteilung kommentiert, Lea ruht, Crew tuschelt")
    pruefen(any(e.get("key") == "st.megan.selbst.0" for e in v["log"]), "Megan kommentiert, dass Duc selbst einen Posten nimmt")
    pruefen(v["fertig"] and sturm.schliessen(z) == "vorbereitung", "Vorbereitung schließt")
    v = nacht(z, modul)
    e = z["sturm"]["ergebnis"]
    pruefen(e["stufe"] == "gut" and e["ok"] == 5, "bester Plan: alle fünf Posten ✓")
    pruefen("sturm_bestanden" in z["flags"], "Flag sturm_bestanden für Megans Haltung")
    vor = ermittlung.megan_haltung(z) if ermittlung.aktiv(z) else None
    pruefen(vor is None or vor >= 1, "Megans Haltung steigt (%s)" % vor)
    pruefen(z["werte"].get("vertrauen.chiara", 0) > 0 or any("Chiara held" in s for s in v["bilanz"]["zeilen"]),
            "Chiara hielt ihren Wunschposten: Vertrauen")
    pruefen(any("rested" in s for s in v["bilanz"]["zeilen"]), "Ruhe-Bonus am Morgen")
    pruefen(not any(x["art"] == "panik" for x in v["log"]), "keine Panik bei gutem Plan")

    # Schlechter Plan, Duc frei: Panik, Sprint rettet einen Posten
    z = zustand_tag5(modul)
    sturm.beginnen(z, modul, MOD, "sturmvorbereitung")
    sturm.einteilen(z, modul, MOD, {"anker": "lola", "strom": "lea", "kombuese": "rosi", "beiboot": "chiara",
                                    "notloesung": "maxwell"})
    sturm.schliessen(z)
    konto = z.get("konto", 0)
    z["phase"] = "nacht"
    z["szene"] = {"def": {"id": "sturmnacht"}, "log": [], "figuren": []}
    sturm.beginnen(z, modul, MOD, "sturmnacht")
    v = sturm.aktiv(z)
    pruefen(v["schritt"] == "sprint" and v["offen"] == "kombuese", "erste Krise ohne Eignung: Duc darf hinrennen")
    sturm.sprint(z, modul, MOD, False)
    pruefen(v["schritt"] == "sprint" and v["offen"] == "strom", "nicht gerannt: Sprint bleibt für später")
    sturm.sprint(z, modul, MOD, True)
    pruefen(v["ergebnis"]["strom"] == "knapp" and v["sprint"] == "strom", "Sprint rettet den Strom knapp")
    pruefen(v["fertig"] and v["schritt"] == "fertig", "nach dem Sprint läuft die Nacht ohne weitere Wahl durch")
    e = z["sturm"]["ergebnis"]
    pruefen(e["stufe"] == "schlecht" and "sturm_chaos" in z["flags"], "schlechter Plan: Megan sieht Chaos")
    pruefen(z.get("konto", 0) < konto, "verlorene Posten kosten Geld")
    pruefen(any(x["art"] == "ruf" for x in v["log"]), "nach dem Stromausfall rufen alle durcheinander")

    # Doppelt eingeteilt ist ein Fehler
    z = zustand_tag5(modul)
    sturm.beginnen(z, modul, MOD, "sturmvorbereitung")
    try:
        sturm.einteilen(z, modul, MOD, {"anker": "lea", "beiboot": "lea"})
        pruefen(False, "eine Person auf zwei Posten wird abgelehnt")
    except ValueError:
        pruefen(True, "eine Person auf zwei Posten wird abgelehnt")

    # Ohne Vorbereitung (Testsprung in die Nacht): alles leer, Nacht läuft trotzdem
    z = zustand_tag5(modul)
    v = nacht(z, modul, rennen=False)
    pruefen(v["fertig"] and z["sturm"]["ergebnis"]["ok"] == 0, "Nacht ohne Plan läuft durch")

    # Vertonung: jeder Schlüssel im Log ist bekannt, jede Zeile hat Turbo-Tags
    zeilen = {k: (w, t) for k, w, t in sturm.alle_zeilen(MOD)}
    pruefen(len(zeilen) > 100, "%d vertonte Sturm-Zeilen" % len(zeilen))
    unbekannt = [x["key"] for x in v["log"] if x.get("key") and x["key"] not in zeilen]
    pruefen(not unbekannt, "alle Schlüssel vertonbar %s" % unbekannt[:3])
    import json
    tags = {(t["wer"], t["text"]) for t in json.load(open(os.path.join(MOD, "stimme_tags.json"), encoding="utf-8"))["zeilen"]}
    fehlt = [k for k, (w, t) in zeilen.items() if (w, t) not in tags]
    pruefen(not fehlt, "Turbo-Tags für jede Sturm-Zeile (fehlend: %d)" % len(fehlt))
    pruefen(all(D["eignung"][p][po] in (1, 2, 3) for p in D["eignung"] for po in D["posten"]), "Eignungstabelle vollständig")

    print("\n%s" % ("Alles grün." if not FEHLER else "%d Fehler." % len(FEHLER)))
    sys.exit(1 if FEHLER else 0)


if __name__ == "__main__":
    main()
