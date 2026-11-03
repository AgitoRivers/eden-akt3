# -*- coding: utf-8 -*-
"""Chase them off (Duc 02.11.2026, Brain Trust "Kampf-Tiefe"): Gegner klar unter Ducs Level verjagt er auf der
Expeditions-Karte mit einem Klick statt mit einem Kampf. Halbe Erfahrung, keine Beute, danach ist der Weg bis zur
naechsten Rast ruhig. Nie fuer Bosse, seltene Gegner, Banden mit Spruechen oder Kaempfe ohne Flucht.

  python tests\\test_verjagen.py
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


def ereignis():
    return (E.ansicht(E.aktiv())["z"].get("ereignis") or {})


def betreten(level):
    z = E.aktiv()
    E.ort_aufraeumen(z)
    z.pop("expedition", None)
    z["status"], z["phase"], z["event"] = "wahl", "tag", None
    z["flags"] = [f for f in z["flags"] if f != "kloster_fertig"] + ["kloster_angenommen"]
    z.setdefault("plan", {}).pop("aktionen", None)
    E.kampf.progress(z).update(level=level, xp=0)
    E.sichern(z)
    return E.aktion("ort_betreten", {"id": "macchia"})


def zum_kampf():
    """Walk the Kloster frames (first option without a roll) until a choice leads straight into a fight."""
    for _ in range(12):
        ev = ereignis()
        for i, o in enumerate(ev.get("optionen") or []):
            x = o.get("exp") or {}
            if x.get("kampf") is not None and not x.get("kampf_nur_fehlschlag"):
                return i, o
        i = next(i for i, o in enumerate(ev["optionen"]) if not o.get("probe") and (o.get("exp") or {}).get("weiter"))
        E.aktion("event_wahl", {"index": i})
        E.aktion("event_schliessen", {})
    raise AssertionError("kein Kampf auf dem Weg gefunden")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    L.vorbereiten("eden_rise", tempfile.mkdtemp(prefix="eden_verjagen_"))
    z = E.aktion("neu", {"modus": "ironman"})
    z = E.aktion("persona", {"index": 0})
    if z["status"] == "prolog":
        z = E.aktion("prolog", {})
    z["tag"] = 6
    E.sichern(z)
    defs = E.kampf.daten(E.moddir(z["modul"]))

    # Regel ohne Spielstand-Weg: Level-Abstand, Bosse, Kaempfe ohne Flucht, Banden, Training
    z = E.aktiv()
    E.kampf.progress(z).update(level=3)
    pruefen(E.kampf.verjagbar(z, defs, "kloster_1_ratte"), "Level 3 gegen Ratten auf Level 1: verjagbar")
    pruefen(not E.kampf.verjagbar(z, defs, "kloster_3_hund"), "Level 3 gegen Hund auf Level 2: kämpfen")
    E.kampf.progress(z).update(level=10)
    pruefen(not E.kampf.verjagbar(z, defs, "kloster_8_loewe"), "der Löwe ist Boss: nie verjagbar")
    pruefen(not E.kampf.verjagbar(z, defs, "kloster_2_keiler"), "der Keiler lässt keine Flucht zu: nie verjagbar")
    pruefen(not E.kampf.verjagbar(z, defs, "maxwell_training"), "Training ist nie verjagbar")
    banden = [b for b, x in defs["encounters"].items() if x.get("sprueche")]
    pruefen(banden and not any(E.kampf.verjagbar(z, defs, b) for b in banden), "Banden mit Sprüchen (Riccis) nie verjagbar")

    # Auf der Karte: zu nah dran -> keine zweite Wahl
    betreten(level=2)
    i, o = zum_kampf()
    pruefen(not o["exp"].get("verjagbar"), "Level 2 gegen Level 1: keine Wahl „Chase them off“")
    try:
        E.aktion("event_wahl", {"index": i, "verjagen": True})
        geblockt = False
    except ValueError:
        geblockt = True
    pruefen(geblockt, "der Server lehnt das Verjagen ab, wo die Karte es nicht anbietet")

    # Klar überlegen -> verjagen statt kämpfen
    betreten(level=4)
    i, o = zum_kampf()
    pruefen(o["exp"].get("verjagbar"), "Level 4 gegen Level 1: die Karte bietet „Chase them off“ an")
    z = E.aktiv()
    frame, xp0, inv0 = z["ort_frame"], E.kampf.progress(z)["xp"], list(z.get("inventar", []))
    E.aktion("event_wahl", {"index": i, "verjagen": True})
    z = E.aktion("event_schliessen", {})
    pruefen(z["status"] != "kampf" and not z.get("kampf"), "kein Kampfbildschirm")
    m = next((x for x in z["meldungen"] if x.get("titel") == "🏃 Chased off"), None)
    pruefen(m and m["folgen"][0].startswith("You step forward with"), "Meldung mit Satz: %s" % (m or {}).get("folgen"))
    pruefen(E.kampf.progress(z)["xp"] > xp0, "kleiner Lohn: Erfahrung %d -> %d" % (xp0, E.kampf.progress(z)["xp"]))
    pruefen(z.get("inventar", []) == inv0, "keine Beute")
    pruefen(frame in z.get("ort_besiegt", []), "der Ort ist bis zur nächsten Rast ruhig")
    pruefen("ev_verjagen" not in z and "ev_kampf" not in z, "keine Reste im Spielstand")
    print("OK")


if __name__ == "__main__":
    main()
