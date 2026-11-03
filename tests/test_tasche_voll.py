# -*- coding: utf-8 -*-
r"""Full bag (Duc 31.10.2026): what the story hands over waits in the cabin chest, item conditions count the chest, item_weg takes
from it. Combat loot and everything during an expedition still stays behind.

  python tests\test_tasche_voll.py
"""
import json, os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HIER))
from kern import regeln, zustand  # noqa: E402

MODUL = json.load(open(os.path.join(HIER, "..", "module", "eden_rise", "modul.json"), encoding="utf-8"))
FEHLER = []
GESCHENK = "megan_crewkarte"


def pruefen(ok, text):
    print(("OK    " if ok else "FEHLER") + " " + text)
    if not ok:
        FEHLER.append(text)


def volle_tasche():
    """A state with a full bag of single-slot items that are not the ones under test."""
    z = {"inventar": [], "werte": {}, "flags": [], "uhren": {}, "codex": [], "tag": 9, "phase": "tag"}
    kandidaten = [i for i, it in MODUL["items"].items() if it.get("art") == "geschenk" and i != GESCHENK]
    for i in kandidaten:
        if not zustand.platz_fuer(z, MODUL, i):
            break
        z["inventar"].append(i)
    pruefen(not zustand.platz_fuer(z, MODUL, GESCHENK), "Vorbereitung: Tasche ist voll")
    return z


def story_pruefen():
    z = volle_tasche()
    vorher = list(z["inventar"])
    zeilen = zustand.folgen_anwenden(z, MODUL, [{"item": GESCHENK}])
    pruefen(z["truhe"] == [GESCHENK] and z["inventar"] == vorher, "Story-Gegenstand landet in der Truhe, Tasche unverändert")
    pruefen(any("cabin chest" in s for s in zeilen) and not any("stays behind" in s for s in zeilen), "Meldung nennt die Truhe")
    pruefen(regeln.gilt({"item": GESCHENK}, z), "Bedingung sieht die Truhe")
    zustand.folgen_anwenden(z, MODUL, [{"item_weg": GESCHENK}])
    pruefen(z["truhe"] == [], "item_weg nimmt auch aus der Truhe")


def mehrere_pruefen():
    z = volle_tasche()
    zeilen = zustand.folgen_anwenden(z, MODUL, [{"item": "plaster", "n": 3}])
    pruefen(z["truhe"] == ["plaster"] * 3, "mehrere Stück: alle in der Truhe")
    pruefen(any("×3" in s and "cabin chest" in s for s in zeilen), "Meldung nennt die Zahl")


def ausnahmen_pruefen():
    z = volle_tasche()
    zeilen = zustand.folgen_anwenden(z, MODUL, [{"item": GESCHENK, "beute": True}])
    pruefen(not z.get("truhe") and any("stays behind" in s for s in zeilen), "Kampf-Beute bleibt liegen")
    z = volle_tasche()
    z["expedition"] = {"id": "berge", "inventar": list(z["inventar"]), "chips": {}, "behalten": None}
    zeilen = zustand.folgen_anwenden(z, MODUL, [{"item": GESCHENK}])
    pruefen(not z.get("truhe") and any("stays behind" in s for s in zeilen), "auf Expedition bleibt es liegen")


def platz_pruefen():
    z = {"inventar": [], "werte": {}, "flags": [], "uhren": {}, "codex": [], "tag": 9, "phase": "tag"}
    zustand.folgen_anwenden(z, MODUL, [{"item": GESCHENK}])
    pruefen(z["inventar"] == [GESCHENK] and "truhe" not in z, "mit Platz: in die Tasche, Truhe bleibt unberührt")


if __name__ == "__main__":
    story_pruefen()
    mehrere_pruefen()
    ausnahmen_pruefen()
    platz_pruefen()
    print("FEHLER: %d" % len(FEHLER) if FEHLER else "Alles gut.")
    sys.exit(1 if FEHLER else 0)
