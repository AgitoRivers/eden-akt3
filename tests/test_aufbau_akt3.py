# -*- coding: utf-8 -*-
r"""Wiederaufbau Akt 3 (kern/aufbau.py, Drehbuch Akt 3 4.1, E-123, E-125): erster Stein, Baustoffe je Haus, Piraten
bauen nachts nur Geliefertes an begonnenen Baustellen, Bauen-Los, Charlys Rabatt.

  python tests/test_aufbau_akt3.py
"""
import os, sys

EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, EDEN)
from kern import aufbau, zustand  # noqa: E402


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def z_neu(*flags):
    return {"flags": ["tk_haus_weg_post", "tk_haus_weg_werkstatt", "buenaventura_schwur"] + list(flags),
            "kueche": {"rohstoffe": {"timber": 20, "slate": 10, "cork": 4, "iron": 4, "granite": 6, "steel": 0}}}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    pruefen(set(aufbau.STUFEN) == set(aufbau.ORTE) and all(len(s) == 3 for s in aufbau.STUFEN.values()), "vier Haeuser, je drei Stufen")
    pruefen(len({str(s) for s in aufbau.STUFEN.values()}) == 4, "jedes Haus braucht eigene Baustoffe")
    pruefen(all("timber" in s[0] for s in aufbau.STUFEN.values()), "Stufe 1 ist immer ein Holzgeruest")

    z = z_neu()
    pruefen(set(aufbau.baustellen(z)) == {"post", "werkstatt"}, "nur abgebrannte Haeuser sind Baustellen")
    try:
        aufbau.liefern(z, "post")
        raise AssertionError("liefern ohne ersten Stein")
    except ValueError:
        print("OK ohne ersten Stein keine Lieferung")
    pruefen(aufbau.tag_vorbei(z) == [] and aufbau.baustellen(z)["post"]["stufe"] == 0, "Piraten bauen nicht ohne ersten Stein")

    zustand.folgen_anwenden(z, {"werte": {}}, [{"aufbau_beginnen": "post"}])
    pruefen(aufbau.baustellen(z)["post"]["begonnen"] and "aufbau_begonnen_post" in z["flags"], "Folge aufbau_beginnen setzt den ersten Stein")
    pruefen(aufbau.tag_vorbei(z) == [], "begonnen, aber nichts geliefert: keine Stufe")
    aufbau.liefern(z, "post")
    pruefen(z["kueche"]["rohstoffe"]["timber"] == 16, "Lieferung nimmt die Baustoffe (4 Timber)")
    try:
        aufbau.liefern(z, "post")
        raise AssertionError("zweimal liefern")
    except ValueError:
        print("OK je Nacht nur eine Lieferung")
    pruefen(len(aufbau.tag_vorbei(z)) == 1 and aufbau.baustellen(z)["post"]["stufe"] == 1, "nachts eine Stufe")
    pruefen(aufbau.braucht(z, "post") == {"slate": 3, "cork": 2}, "Post Stufe 2: Schiefer und Kork")

    z2 = z_neu()
    z2["kueche"]["rohstoffe"]["timber"] = 3
    zustand.folgen_anwenden(z2, {"werte": {}}, [{"aufbau_beginnen": "post"}])
    try:
        aufbau.liefern(z2, "post")
        raise AssertionError("liefern mit zu wenig Holz")
    except ValueError:
        print("OK alles oder nichts")
    pruefen(z2["kueche"]["rohstoffe"]["timber"] == 3, "nichts abgezogen bei fehlendem Material")

    # Charlys Rabatt: 20 %, abgerundet, mindestens 1
    z3 = z_neu("a3_charly_geld")
    pruefen(aufbau.braucht(z3, "post") == {"timber": 3}, "Charly: 4 Timber werden 3")
    aufbau.baustellen(z3)["werkstatt"]["stufe"] = 2
    pruefen(aufbau.braucht(z3, "werkstatt") == {"iron": 1, "steel": 1}, "Charly: 2 werden 1, nie 0")

    # Bauen-Los: eine Stufe ohne Baustoffe
    z4 = z_neu()
    vorher = dict(z4["kueche"]["rohstoffe"])
    zustand.folgen_anwenden(z4, {"werte": {}}, [{"aufbau_stufe": "*"}])
    pruefen(sum(s["stufe"] for s in aufbau.baustellen(z4).values()) == 1 and z4["kueche"]["rohstoffe"] == vorher, "Los gibt eine Stufe gratis")

    # Bis zum Ende: Flag aufbau_fertig_<id>
    z5 = z_neu()
    z5["kueche"]["rohstoffe"].update({"steel": 2, "iron": 2})
    zustand.folgen_anwenden(z5, {"werte": {}}, [{"aufbau_beginnen": "werkstatt"}])
    for _ in range(3):
        aufbau.liefern(z5, "werkstatt")
        aufbau.tag_vorbei(z5)
    pruefen(aufbau.fertig(z5, "werkstatt") and "aufbau_fertig_werkstatt" in z5["flags"], "drei Naechte: Werkstatt fertig, Flag gesetzt")
    pruefen(all("braucht" in x and "geht" in x for x in aufbau.ansicht(z5)), "Ansicht fuer den Client")

    z6 = z_neu()
    z6["flags"].remove("buenaventura_schwur")
    zustand.folgen_anwenden(z6, {"werte": {}}, [{"aufbau_beginnen": "post"}])
    aufbau.liefern(z6, "post")
    pruefen(aufbau.tag_vorbei(z6) == [], "ohne Schwur tragen die Piraten nichts")
    print("Alle Pruefungen gruen.")


if __name__ == "__main__":
    main()
