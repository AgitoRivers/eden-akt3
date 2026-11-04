# -*- coding: utf-8 -*-
r"""Akt 3, Paket E: Schluss-Szenen der Romanzen und die Freundschaften und Paare (ereignisse_akt3_romanzen.py, Drehbuch 6 und 7).

  python tests/test_akt3_romanzen.py
"""
import json, os, sys

EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, EDEN)
sys.path.insert(0, os.path.join(EDEN, "werkzeuge", "eden_rise"))
from kern import regeln  # noqa: E402
MOD = os.path.join(EDEN, "module", "eden_rise")
EV = {e["id"]: e for e in json.load(open(os.path.join(MOD, "ereignisse.json"), encoding="utf-8"))["events"]}
ORTE = json.load(open(os.path.join(MOD, "auftraege.json"), encoding="utf-8"))["orte"]
FRAUEN = ["chiara", "alva", "lea", "sophia", "rosi", "lola", "siri", "bibi", "megan"]


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    import ereignisse_akt3_romanzen as R
    for pid in FRAUEN:
        o = ORTE.get("a3_schluss_" + pid)
        pruefen(o and EV[o["start"][0]["id"]]["art"] == "ort" and len(EV["a3_schluss_" + pid]["optionen"]) == 3,
                "Schluss-Szene %s als Karte mit drei Antworten" % pid)
        pruefen("tag_ab\": 34" in json.dumps(o["wenn"]), "%s: vor der Villa" % pid)
    pruefen('"tag_ab": 32' in json.dumps(ORTE["a3_schluss_chiara"]["wenn"]), "Chiaras Blackout ab Tag 32")
    pruefen(regeln.gilt(R.oben("chiara"), {"flags": ["rm_c4"]}) and not regeln.gilt(R.oben("chiara"), {"flags": ["rm_c3"]}), "Leiter oben = Stufe 4")
    pruefen(regeln.gilt(R.romanze("lea"), {"flags": ["rm_l3"]}) and not regeln.gilt(R.romanze("lea"), {"flags": []}), "Romanze = Leiter-Stufe 3")

    paare = {i: e for i, e in EV.items() if i.startswith("a3_paar_")}
    pruefen(all(e["wann"].get("leiter") and e["wann"].get("pflicht") for e in paare.values()), "Paar-Szenen ueber die Leiter: hoechstens eine am Tag")
    pruefen(all(26 <= e["wann"]["tage"][0] and e["wann"]["tage"][1] <= 33 for e in paare.values()), "Paar-Szenen Tag 26 bis 33")
    pruefen(EV["a3_paar_bones"]["wann"]["tage"][1] <= 29 and '"mochi": "geier"' in json.dumps(EV["a3_paar_bones"]["wann"]),
            "Bones vor Maxwells Flug, nur wenn Bones gerettet ist")
    for frau, mann in (("lola", None), ("chiara", None), ("sophia", None), ("lea", None)):
        voll, duc = json.dumps(EV["a3_paar_" + frau]["wann"]), json.dumps(EV["a3_paar_%s_duc" % frau]["wann"])
        pruefen('"nicht"' in voll and "rm_" in duc, "%s: zwei Fassungen nach Romanze" % frau)
    for i, e in paare.items():
        if i.startswith(("a3_paar_holm", "a3_paar_charly")):
            continue
        gef = {z["gefuehl"] for z in e["zeilen"] + [o["zeile"] for o in e["optionen"] if o.get("zeile")]}
        pruefen(not gef & {"love", "desire"}, "%s: Freundschaft, keine Verliebtheit" % i)
    pruefen(any(z["gefuehl"] == "love" for z in EV["a3_paar_charly"]["zeilen"]), "Charly und Danzel werden ein Paar")
    pruefen(all(any(f.get("flag", "").startswith("a3_paar_") for f in o["folgen"]) for e in paare.values() for o in e["optionen"]),
            "jede Duc-Wahl wirkt im Festbild (Flag)")
    print("Alle Pruefungen gruen.")


if __name__ == "__main__":
    main()
