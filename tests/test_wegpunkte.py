# -*- coding: utf-8 -*-
"""Schnellreise in Ortskapiteln (Duc + Brain Trust 29.10.2026, kern/wegpunkte.py): am Eingang zu Fuss oder zu einem
schon entdeckten Rastplatz, am Rastplatz weiter zu einem anderen - nie zurueck hinter eine Entscheidung (sperre).

  python tests\\test_wegpunkte.py
"""
import os, sys, tempfile

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import lauf_test as L  # noqa: E402

E = L.eden


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def ansicht():
    return (E.ansicht(E.aktiv())["z"].get("ereignis") or {})


def ziele():
    r = ansicht().get("reisen")
    return [w["id"] for w in r["ziele"]] if r else []


def betreten(gefunden):
    z = E.aktiv()
    E.ort_aufraeumen(z)
    z.pop("expedition", None)
    z["status"], z["phase"], z["event"] = "wahl", "tag", None
    z["flags"] = [f for f in z["flags"] if f != "kloster_fertig"] + ["kloster_angenommen"]
    z["rast_gefunden"] = list(gefunden)
    z.setdefault("plan", {}).pop("aktionen", None)
    E.sichern(z)
    return E.aktion("ort_betreten", {"id": "macchia"})


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    L.vorbereiten("eden_rise", tempfile.mkdtemp(prefix="eden_wegpunkte_"))
    z = E.aktion("neu", {"modus": "ironman"})
    z = E.aktion("persona", {"index": 0})
    if z["status"] == "prolog":
        z = E.aktion("prolog", {})
    z["tag"] = 5
    E.sichern(z)

    z = betreten([])
    pruefen(z["event"]["id"] == "kl_start" and not ansicht().get("reisen"), "erster Besuch: nur zu Fuss, kein Wegpunkt")

    z = betreten(["kl_bachufer", "kl_huette", "kl_lager", "kl_kueche"])
    r = ansicht()["reisen"]
    pruefen(r["von"] == "eingang" and ziele() == ["kl_bachufer", "kl_huette", "kl_kueche", "kl_lager"],
            "Eingang: die entdeckten Rastplaetze in Wegreihenfolge %s" % ziele())
    kampf_bis = {w["id"]: w["kaempfe"] for w in r["ziele"]}
    pruefen(kampf_bis["kl_bachufer"] == 1 and kampf_bis["kl_lager"] > kampf_bis["kl_huette"],
            "jede Karte sagt, wie viele Kaempfe der Sprung auslaesst %s" % kampf_bis)
    pruefen(all(w["bild"] and w["bild"].startswith("/bg/eden_rise_") for w in r["ziele"]), "jede Karte hat ihr Bild")
    with_fehler = False
    try:
        E.aktion("ort_reisen", {"id": "kl_schluchtfeuer"})
    except ValueError:
        with_fehler = True
    pruefen(with_fehler, "nicht entdeckte Rastplaetze sind kein Ziel")

    z = E.aktion("ort_reisen", {"id": "kl_huette"})
    pruefen(z["event"]["id"] == "kl_huette" and z["status"] == "ereignis", "Sprung zur Huette")
    pruefen((z.get("expedition") or {}).get("id") == "kloster", "der Sprung startet die Expedition wie der erste Schritt")
    pruefen(z["ort_weg"] == ["kl_huette"] and not ansicht().get("zurueck"), "neue Spur ab dem Ziel, kein Go back zum Eingang")
    pruefen(set(ziele()) == {"kl_bachufer", "kl_kueche", "kl_lager"}, "am Rastplatz: weiter zu den anderen %s" % ziele())

    z = E.aktion("ort_reisen", {"id": "kl_lager"})          # das Lager ist eine Entscheidung (sperre)
    pruefen(z["event"]["id"] == "kl_lager", "weiter zum Lager")
    pruefen(ziele() == [], "hinter der Entscheidung am Lager geht keine Reise zurueck")
    z["rast_gefunden"].append("kl_schluchtfeuer")
    E.sichern(z)
    pruefen(ziele() == ["kl_schluchtfeuer"], "vorwaerts zum Schluchtfeuer geht es")

    betreten(["kl_bachufer"])
    z = E.aktiv()
    z["ort_weg"].append("kl_bachufer")                     # einen Schritt gegangen: der Eingang bietet nichts mehr an
    E.sichern(z)
    pruefen(not ansicht().get("reisen") or ansicht()["reisen"]["von"] != "eingang", "nach dem ersten Schritt kein Eingangs-Wegpunkt mehr")
    print("OK")


if __name__ == "__main__":
    main()
