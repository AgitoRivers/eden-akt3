# -*- coding: utf-8 -*-
"""Jobkarte ohne Energie (Duc 29.10.2026): Schnelljobs mit Probe zeigen gleich, dass Energie fehlt (energie_fehlt) und woher
sie kommt (energie_tipp), statt erst nach dem Klick abzusagen. Jobs ohne Probe bleiben frei. Kein Joker, Energie bleibt.

  python tests\\test_energie_hinweis.py
"""
import os, sys, tempfile

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import lauf_test as L  # noqa: E402

E = L.eden
H = E.handel


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def basis():
    L.vorbereiten("eden_rise", tempfile.mkdtemp(prefix="eden_energie_"))
    E.modul_laden()["schnelljobs"] = True        # eden_rise hat die Schnelljobs abgeschaltet (29.10.2026); hier wird die Mechanik geprueft
    L.random.seed(11)
    protokoll = {"schritte": [], "erledigt": {}}
    z = E.aktion("neu", {"modus": "ironman"})
    while not (z["tag"] >= 3 and z["status"] == "wahl"):
        a = L.schritt(z, protokoll)
        if a[0] != "_tagesarbeit":
            L.versuch(a, protokoll)
        z = E.aktiv()
    return z


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    z = basis()
    modul = E.modul_laden()
    V = E.showrunner.vorrat(E.moddir())
    z["werte"]["energie"] = 1
    jobs = H.jobs_heute(z, modul, V)
    pruefen(jobs and all(j["energie_fehlt"] == 0 for j in jobs), "mit Energie fehlt nichts (%d Jobs)" % len(jobs))
    z["werte"]["energie"] = 0
    jobs = H.jobs_heute(z, modul, V)
    mit = [j for j in jobs if j["mit_probe"]]
    ohne = [j for j in jobs if not j["mit_probe"]]
    pruefen(mit and all(j["energie_fehlt"] == 1 for j in mit), "ohne Energie: jeder Job mit Probe meldet 'needs 1 energy'")
    pruefen(all(j["energie_fehlt"] == 0 for j in ohne), "Jobs ohne Probe bleiben frei (%d)" % len(ohne))
    z["inventar"] = [i for i in z["inventar"] if i not in ("espresso", "energieriegel")]
    pruefen("espresso" in H.energie_tipp(z, modul).lower() and "tomorrow" in H.energie_tipp(z, modul),
            "Tipp ohne passendes Item: espresso, relaxed hour, tomorrow")
    z["inventar"].append("energieriegel")
    pruefen(modul["items"]["energieriegel"]["label"] in H.energie_tipp(z, modul), "Tipp nennt das Energie-Item in der Tasche")
    try:
        H.job_machen(z, modul, V, mit[0]["id"])
        pruefen(False, "Absage ohne Energie")
    except ValueError as e:
        pruefen("running on empty" in str(e), "der Server sagt weiterhin ab (Sicherung hinter der grauen Karte)")
    h = H.ansicht(z, modul, V, [])
    pruefen(h["energie_tipp"] and any(j["energie_fehlt"] for j in h["jobs"]), "Handel-Ansicht liefert Tipp und Markierung an den Client")
    print("ALLES OK")


if __name__ == "__main__":
    main()
