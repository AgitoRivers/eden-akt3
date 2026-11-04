# -*- coding: utf-8 -*-
"""Akt 3, kleine Morgen-Vignetten ohne Phase (Drehbuch docs/wiki/welt/drehbuch_akt3.md, Abschnitt 3 und 4.1).

Am Ende jeder Nacht (eden.py, Tagesende) kommen hoechstens drei Zeilen in die Meldung "Day X is over":
  * Kevin auf dem Kirchendach (Tag 25-34, ausser Tag 26: da sitzt er auf Casanovas Tafel). Damit niemand Minicu vergisst.
  * Dank eines Hauses, das nicht abgebrannt ist (Tag 25-28, je Morgen eins). Ohne Frage, gefragt wird spaeter.
  * Die Legion baut einen Tag mit (bl_verband_wolff): einmal eine Stufe an der begonnenen Baustelle, die am weitesten ist.
Alles nur nach dem Cliffhanger (akt2_ende)."""
from . import aufbau

KEVIN = "Kevin is on the church roof again, above the back room. He hasn't moved."
DANK = {
    "post": "Mina rides past on her bicycle and honks twice. The post office came through the fire. She waves a letter at you: “Not a bill!”",
    "batu": "There is a tin of biscuits on the step of Bà Tư's shop, with your name on it. Her shop came through the fire.",
    "bar": "Alva has written one word on Papa's board, under all the names: OPEN. Her bar came through the fire.",
    "werkstatt": "Petru's rudder still hangs over his workshop door, not burned. He nods at you once when you walk past.",
}
LEGION = "Wolff and two men of the Legion carried beams all day. Wolff: “You gave me the good bandage, the only one. The Legion pays its debts.”"


def morgen(z):
    """Zeilen fuer den neuen Morgen (z["tag"] ist schon der neue Tag)."""
    f = z.get("flags", [])
    if "akt2_ende" not in f or not 25 <= z.get("tag", 0) <= 35:
        return []
    tag, zeilen = z["tag"], []
    if tag <= 34 and tag != 26:
        zeilen.append(KEVIN)
    if tag <= 28:
        heil = [h for h in aufbau.ORTE if "tk_haus_weg_" + h not in f and "a3_dank_heil_" + h not in f]
        if heil:
            f.append("a3_dank_heil_" + heil[0])
            zeilen.append(DANK[heil[0]])
    if "bl_verband_wolff" in f and "a3_legion" not in f:
        st = aufbau.baustellen(z)
        offen = [(s["stufe"], h) for h, s in st.items() if s["begonnen"] and s["stufe"] < len(aufbau.STUFEN[h])]
        if offen:
            f.append("a3_legion")
            zeilen.append(LEGION)
            zeilen += aufbau.stufe_geschenkt(z, max(offen)[1])
    return zeilen
