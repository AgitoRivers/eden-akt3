# -*- coding: utf-8 -*-
"""W20 wie BG3: sichtbarer Schwierigkeitsgrad, aufgelistete Boni, Vorteil = zweimal wuerfeln.
Natuerliche 20 = kritisch, natuerliche 1 = Patzer."""
import random
from . import wuerfel_anzeige

SG = {"easy": 8, "medium": 12, "hard": 16, "very_hard": 20}
ERGEBNIS_DE = {"kritisch": "Critical success", "erfolg": "Success", "fehlschlag": "Failure", "patzer": "Fumble"}   # Name bleibt, Text Englisch seit 28.10.2026
ERGEBNIS_EN = {"kritisch": "a CRITICAL SUCCESS - better than hoped",
               "erfolg": "a SUCCESS",
               "fehlschlag": "a FAILURE - it does not work, and that has a small consequence",
               "patzer": "a FUMBLE - it goes wrong in a way that costs him something"}


def probe(attribut, sg, boni, vorteil=False):
    """boni = [(label, wert)]. Liefert dict fuer Anzeige und Erzaehlauftrag."""
    w1 = random.randint(1, 20)
    w2 = random.randint(1, 20) if vorteil else None
    wurf = max(w1, w2) if vorteil else w1
    summe = wurf + sum(b for _, b in boni)
    if wurf == 20:
        erg = "kritisch"
    elif wurf == 1:
        erg = "patzer"
    else:
        erg = "erfolg" if summe >= sg else "fehlschlag"
    p = {"attribut": attribut, "sg": sg, "wuerfe": [w for w in (w1, w2) if w], "wurf": wurf,
         "boni": boni, "summe": summe, "ergebnis": erg, "text": ERGEBNIS_DE[erg]}
    wuerfel_anzeige.merken(p)
    return p


def verdeckt(bonus, sg):
    w = random.randint(1, 20)
    return {"wurf": w, "bonus": bonus, "summe": w + bonus, "sg": sg, "erfolg": w == 20 or w + bonus >= sg}
