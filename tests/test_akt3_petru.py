# -*- coding: utf-8 -*-
r"""Akt 3: mehr Petru (ereignisse_akt3_petru.py): Netz beim Werkstattbesuch, Brief an Laetitia mit Folge auf der Festa,
weniger nacktes "Hm.".

  python tests/test_akt3_petru.py
"""
import json, os, sys

EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, EDEN)
from kern import akt3  # noqa: E402
EV = {e["id"]: e for e in json.load(open(os.path.join(EDEN, "module", "eden_rise", "ereignisse.json"), encoding="utf-8"))["events"]}


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    for i in ("a3_petru_netz", "a3_petru_bastianu", "a3_petru_eintopf", "a3_petru_brief"):
        pruefen(i in EV, "Szene %s" % i)
    z = {"status": "wahl", "flags": ["akt2_ende"], "tag": 25}
    pruefen(akt3.szene_besuch(z, "petru") == "a3_petru_netz", "Petrus Netz beim Werkstattbesuch ab Tag 25")
    pruefen(akt3.szene_besuch(dict(z, tag=24), "petru") is None and akt3.szene_besuch(dict(z, flags=z["flags"] + ["a3_petru_netz"]), "petru") is None,
            "nicht vor Tag 25, nur einmal")
    pruefen("a3_petru_netz" in json.dumps(EV["a3_festa_bauen"]), "die Festa zeigt das Netz mit den Namen")
    bild = json.dumps(EV["a3_festa_bild"])
    pruefen(all("a3_petru_brief_" + k in bild for k in ("brauche", "festa", "marie")), "jede Brief-Wahl hat ihre Folge auf der Festa")
    zeilen = [z for e in EV.values() if e["id"].startswith("a3_") for z in e["zeilen"] + [o["zeile"] for o in e["optionen"] if o.get("zeile")] if z["wer"] == "petru"]
    hm = [z for z in zeilen if z["text"].strip() in ("Hm.", "Hm. Good.", "Hm. Beer.")]
    pruefen(len(zeilen) >= 40 and len(hm) <= 2, "Petru spricht mehr (%d Zeilen), nacktes Hm. hoechstens zweimal (%d)" % (len(zeilen), len(hm)))
    print("Alle Pruefungen gruen.")


if __name__ == "__main__":
    main()
