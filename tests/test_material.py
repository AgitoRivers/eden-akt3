# -*- coding: utf-8 -*-
"""Baustoffe (Duc 30.10.2026): Stein ist Schiefer + Granit, Stahl faellt ab Tag 22 aus Maschinen-Gegnern, Rezepte je Stall-Stufe.

  python tests\\test_material.py
"""
import copy, json, os, sys

EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, EDEN)
from kern import kampf, kuechen, zustand  # noqa: E402

MOD = os.path.join(EDEN, "module", "eden_rise")
MODUL = json.load(open(os.path.join(MOD, "modul.json"), encoding="utf-8"))
DEFS = copy.deepcopy(kampf.daten(MOD))
D = kuechen.daten(MODUL)


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def sieg(tag, gegner):
    """Einen Kampf gegen diesen Gegner gewinnen. -> Spielstand, Zeilen"""
    z = zustand.neu(MODUL, "entspannt")
    zustand.persona_setzen(z, MODUL, MODUL["personas"][0])
    z["tag"], z["phase"] = tag, "tag"
    bid = next(b for b, e in DEFS["encounters"].items() if e.get("enemy") == gegner and not e.get("training"))
    kampf.starten(z, DEFS, bid)
    k = z["kampf"]
    for g in k["gegner"]:
        g["lp"] = 0
    kampf._finish(z, MODUL, k, "ko")
    return z, k["ergebnis"]["zeilen"] if k.get("ergebnis") else []


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    pruefen("stone" not in D["rohstoffe"] and {"slate", "granite", "steel"} <= set(D["rohstoffe"]), "Stein weg, Schiefer, Granit, Stahl da")
    pruefen(set(D["nonna_rohstoffe"]) == {"timber", "slate", "iron"}, "Nonna verkauft Holz, Schiefer, Eisen, aber Granit, Kork und Stahl nicht")
    for art, st in D["stall_stufen"].items():
        pruefen(set(st[0]["rohstoffe"]) == {"timber", "slate"}, "%s Stufe 1: Holz + Schiefer" % art)
        pruefen(set(st[1]["rohstoffe"]) == {"timber", "cork", "slate", "granite"}, "%s Stufe 2: Holz, Kork, Schiefer, Granit" % art)
        pruefen(set(st[2]["rohstoffe"]) == {"timber", "granite", "iron", "steel"}, "%s Stufe 3: Holz, Granit, Eisen, Stahl" % art)
    pruefen(D["abbau"]["knoten"]["granite"]["ertrag"] == {"granite": 2} and D["abbau"]["knoten"]["schist"]["ertrag"] == {"slate": 2},
            "Jeder Fels gibt sein eigenes Material")
    for rid in ("slate", "granite", "steel"):
        pruefen(os.path.isfile(os.path.join(MOD, "items", rid + ".webp")), "Bild für %s" % rid)

    z = zustand.neu(MODUL, "entspannt")
    kuechen.rohstoff_add(z, "stone", 5)
    kuechen.rohstoff_add(z, "slate", 1)
    zustand.angleichen(z, MODUL)
    pruefen(kuechen.rohstoffe(z) == {"slate": 6}, "Alter Spielstand: Stein wird Schiefer")

    menschen = [e for e, x in DEFS["enemies"].items() if x.get("cls") in DEFS["geld_drop"]["klassen"]
                and x.get("tier") in DEFS["geld_drop"]["spanne"]
                and any(b.get("enemy") == e and not b.get("training") for b in DEFS["encounters"].values())]
    z, zeilen = sieg(21, "unit01")
    pruefen("steel" not in kuechen.rohstoffe(z), "Tag 21: die Maschine gibt noch keinen Stahl")
    z, zeilen = sieg(22, "unit01")
    pruefen(kuechen.rohstoffe(z).get("steel") == 1, "Tag 22: 1 Stahl aus der Maschine")
    z, zeilen = sieg(22, menschen[0])
    pruefen("steel" not in kuechen.rohstoffe(z), "Tag 22: Menschen tragen Geld, aber keinen Stahl")
    z, zeilen = sieg(22, "moewe")
    pruefen("steel" not in kuechen.rohstoffe(z), "Tag 22: die Möwe trägt keinen Stahl")
    print("alle Material-Tests gruen")


if __name__ == "__main__":
    main()
