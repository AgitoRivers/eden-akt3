# -*- coding: utf-8 -*-
r"""Inventar-Menue zeigt die echte Taschengroesse (fix-akt2): Start 8, nach Rosis Stufen 12 und 16. Vorher stand im Menue fest "x/6".

  python tests\test_inventar_plaetze.py
"""
import json, os, re, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HIER))
from kern import handel, zustand  # noqa: E402

WURZEL = os.path.dirname(HIER)
MODUL = json.load(open(os.path.join(WURZEL, "module", "eden_rise", "modul.json"), encoding="utf-8"))
MENU = os.path.join(WURZEL, "client", "plugins", "eden-menu", "eden-menu.js")


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    z = zustand.neu(MODUL, "entspannt")
    zustand.persona_setzen(z, MODUL, MODUL["personas"][0])
    handel.init(z, MODUL)
    erwartet = [MODUL["tasche"]["start"]] + [s["plaetze"] for s in MODUL["tasche"]["stufen"]]
    pruefen(erwartet == [8, 12, 16], "Taschenstufen im Modul: 8 / 12 / 16")
    for stufe, n in enumerate(erwartet):
        z["tasche_stufe"] = stufe
        h = handel.ansicht(z, MODUL, {}, [])
        pruefen(h["plaetze"] == n == zustand.inventar_plaetze(z, MODUL), "Stufe %d: Ansicht meldet %d Plaetze" % (stufe, n))
    js = open(MENU, encoding="utf-8").read()
    bag = re.search(r"<h3>Bag .*?</section>", js)
    pruefen(bag is not None, "Bag-Abschnitt im Menue gefunden")
    pruefen("/6<" not in bag.group(0) and "leer(6" not in bag.group(0), "Bag-Abschnitt ohne feste 6")
    pruefen("h.plaetze" in js, "Menue liest h.plaetze vom Server")
    print("\nalles gruen")


if __name__ == "__main__":
    main()
