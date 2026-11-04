# -*- coding: utf-8 -*-
r"""Akt 3, Paket C: Zeugen und Festa-Lose (werkzeuge/eden_rise/ereignisse_akt3_lose.py, Drehbuch Akt 3 4.2 und 4.3).

  python tests/test_akt3_lose.py
"""
import json, os, sys

EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, EDEN)
sys.path.insert(0, os.path.join(EDEN, "werkzeuge", "eden_rise"))
from kern import regeln  # noqa: E402
MOD = os.path.join(EDEN, "module", "eden_rise")
EV = {e["id"]: e for e in json.load(open(os.path.join(MOD, "ereignisse.json"), encoding="utf-8"))["events"]}
ORTE = json.load(open(os.path.join(MOD, "auftraege.json"), encoding="utf-8"))["orte"]


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def folgen(o):
    return o["folgen"]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    import ereignisse_akt3_lose as L
    pruefen(len(L.LOSE) == 13 and len(L.WELLE1) == 8 and len(L.WELLE2) == 5, "13 Lose: 8 ab der Tafel, 5 nach dem ersten Haus")
    for lid in L.LOSE:
        e = EV["a3_los_" + lid]
        wahl = [o for o in e["optionen"] if any(f.get("flag") == "a3_los_" + lid for f in folgen(o))]
        pruefen(e["art"] == "ort" and 2 <= len(wahl) <= 3 and any("weiter" in f for f in folgen(e["optionen"][-1])),
                "Los %s: eine Person, %d Entscheidungen, weiter zum naechsten Los" % (lid, len(wahl)))
        pruefen(all(any(f.get("flag", "").startswith("a3_los_%s_" % lid) for f in folgen(o)) for o in wahl), "Los %s: jede Wahl hat ihr Flag" % lid)
    bauen = [l for l in L.LOSE if any("aufbau_stufe" in f for o in EV["a3_los_" + l]["optionen"] for f in folgen(o))]
    pruefen(sorted(bauen) == ["buehne", "tafel"], "Bauen-Lose geben dem Dorf eine Stufe")
    roh = json.dumps([EV["a3_los_" + l] for l in L.LOSE]).lower()
    pruefen('"geld"' not in roh and "rohstoffe" not in roh, "keine Einkaufsliste: Lose kosten kein Geld und kein Material")

    z = {"flags": ["a3_festa_tafel"], "werte": {}, "tag": 26}
    pruefen(regeln.gilt(L.los_offen("tafel"), z) and not regeln.gilt(L.los_offen("garten"), z), "Welle 2 haengt erst nach dem ersten Haus")
    z["flags"].append("aufbau_fertig_post")
    pruefen(regeln.gilt(L.los_offen("garten"), z), "nach dem ersten Haus: Garten haengt")
    pruefen(not regeln.gilt(L.los_offen("lichter"), z) and regeln.gilt(L.los_offen("lichter"), dict(z, flags=z["flags"] + ["a3_scrap_field"])),
            "Lichter: Zugang ueber Stahl (Scrap Field), keine Menge")
    pruefen(not regeln.gilt(L.los_offen("tafel"), dict(z, flags=z["flags"] + ["a3_los_tafel"])), "erledigtes Los haengt nicht mehr")
    pruefen("a3_los_capra" in EV and "rt_bibi_bleibt" in json.dumps(EV["a3_los_capra"]["wann"]), "Bonus-Los Capra nur mit Bibi")

    for pid in L.ZEUGEN:
        e = EV["a3_frage_" + pid]
        ueberzeugt = [o for o in e["optionen"] if any(f.get("flag") == "a3_zeuge_" + pid for f in folgen(o))]
        pruefen(len(ueberzeugt) == 3, "Zeuge %s: jede der drei Haltungen ueberzeugt" % pid)
    z = {"flags": ["a3_zeugen_auftrag", "bl_tueren_petru"], "werte": {}}
    pruefen(regeln.gilt(L._frage_offen("petru"), z) and not regeln.gilt(L._frage_offen("casanova"), z), "Tueren: Petru offen, Casanova noch zu")
    pruefen(not regeln.gilt(L._frage_offen("petru"), dict(z, flags=z["flags"] + ["a3_zeuge_petru"])), "gefragter Zeuge kommt nicht wieder")
    for oid in ("a3_zeugen", "a3_lose"):
        pruefen(oid in ORTE and all(EV[s["id"]]["art"] == "ort" for s in ORTE[oid]["start"]), "Karte %s" % oid)
    # Umbau nach dem Review: Lose beim Besuch (ohne Phase) und Rundgang mit bis zu drei Losen je Phase
    from kern import akt3
    md = os.path.join(EDEN, "module", "eden_rise")
    z = {"status": "wahl", "flags": ["akt2_ende", "a3_festa_tafel"], "werte": {}, "tag": 27}
    pruefen(akt3.los_besuch(z, md, "petru") == "a3_los_tafel" and akt3.los_besuch(z, md, "angeln") == "a3_los_fang", "Petrus Tafel beim Werkstattbesuch, The Catch beim Angeln")
    pruefen(akt3.los_besuch(dict(z, status="szene"), md, "petru") is None, "nur aus der freien Wahl heraus")
    pruefen(akt3.los_besuch(dict(z, flags=z["flags"] + ["a3_los_tafel"]), md, "petru") is None, "erledigtes Los kommt nicht wieder")
    pruefen(akt3.los_besuch(z, md, "nonna") is None, "Garten erst nach dem ersten Haus (Welle 2)")
    pruefen(akt3.los_besuch(dict(z, flags=z["flags"] + ["a3_los_topf"]), md, "kochen") == "a3_los_menue", "Kochen: erst der Topf, dann das Menue")
    pruefen(all(L.BESUCH[l] for l in L.BESUCH) and set(L.BESUCH) <= set(L.LOSE), "Besuchs-Lose sind Lose der Tafel")
    pruefen(regeln.gilt({"ort_schritte": ["<", 5]}, {"ort_weg": ["a", "b", "c", "d"]}) and not regeln.gilt({"ort_schritte": ["<", 5]}, {"ort_weg": list("abcdef")}),
            "Rundgang: hoechstens drei Lose je Phase")
    for lid in L.LOSE:
        wahl = [o for o in EV["a3_los_" + lid]["optionen"] if any(f.get("flag") == "a3_los_" + lid for f in folgen(o))]
        pruefen(all(any("a3_los_weiter" in json.dumps(f.get("weiter", "")) for f in folgen(o)) for o in wahl), "Los %s: nach der Wahl geht der Rundgang weiter" % lid)
    tafel = json.dumps(EV["a3_los_tafel"])
    pruefen("a3_los_tafel_holm" in tafel and '"direkt"' in tafel and "holm_zurueck" in tafel, "Tafel: mit Holm folgt ihr Takt (Ausflug und Besuch)")
    pruefen(all(any(f.get("flag", "").startswith("a3_los_tafel_holm_") for f in folgen(o)) for o in EV["a3_los_tafel_holm"]["optionen"]),
            "Holms Streifen: jede Wahl hat ihr Flag")
    pruefen(all(k in json.dumps(EV["a3_festa_bauen"]) for k in ("a3_los_tafel_holm_streifen", "a3_los_tafel_holm_saison", "a3_los_tafel_holm_petru")),
            "die Festa zeigt Holms Wahl")
    festa = json.dumps([EV[i] for i in ("a3_festa_bauen", "a3_festa_essen", "a3_festa_schmuck")])
    fehlt = [f for l in L.LOSE for o in EV["a3_los_" + l]["optionen"] for f in [x.get("flag", "") for x in folgen(o)]
             if f.startswith("a3_los_%s_" % l) and '"%s"' % f not in festa]
    pruefen(not fehlt, "die Festa zeigt jede Los-Wahl (%s)" % ", ".join(fehlt))
    print("Alle Pruefungen gruen.")


if __name__ == "__main__":
    main()
