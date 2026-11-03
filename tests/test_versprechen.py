# -*- coding: utf-8 -*-
"""Versprechen (18.10.2026): mit Bedingung zaehlt nur die Bedingung - eine gemeinsame Szene reicht nicht mehr.
Ohne Bedingung (vage Zusage) reicht weiterhin Zeit mit der Person.

  python tests\\test_versprechen.py
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kern import ereignisse  # noqa: E402

MODUL = {"personen": {"alva": {"name": "Alva Santoni"}}}


def stand(flags, mit_szene):
    heute = [{"phase": "abend", "szene": "x", "anwesend": ["alva"]}] if mit_szene else []
    return {"tag": 4, "flags": list(flags), "werte": {}, "uhren": {}, "inventar": [], "verlauf": [], "heute": heute}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    konkret = {"an": "alva", "text": "Duc kommt morgen zu Alva", "seit": 3, "bis": 4, "gehalten_wenn": {"flag": "alva_besucht"}}
    vage = {"an": "alva", "text": "Ich bin für dich da", "seit": 3, "bis": 4}
    faelle = [
        ("konkret, Szene mit ihr, Bedingung fehlt", konkret, stand([], True), False),
        ("konkret, Bedingung erfüllt", konkret, stand(["alva_besucht"], False), True),
        ("vage, Szene mit ihr", vage, stand([], True), True),
        ("vage, keine Zeit mit ihr", vage, stand([], False), False),
    ]
    for titel, v, z, soll in faelle:
        ist = ereignisse.versprechen_gehalten(z, MODUL, v)
        assert ist == soll, "%s: %s statt %s" % (titel, ist, soll)
        print("OK", titel, "->", "gehalten" if ist else "offen")
    print("OK")


if __name__ == "__main__":
    main()
