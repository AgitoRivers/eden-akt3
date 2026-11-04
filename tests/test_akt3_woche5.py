# -*- coding: utf-8 -*-
r"""Akt 3, Woche 5 (Paket D, werkzeuge/eden_rise/ereignisse_akt3_woche5.py, kaempfe_akt3.py): Kalender, Megans Wende,
Sandrus Weg, Nach Mitternacht, Villa mit Endkampf, Scrap Field.

  python tests/test_akt3_woche5.py
"""
import json, os, sys

EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, EDEN)
sys.path.insert(0, os.path.join(EDEN, "werkzeuge", "eden_rise"))
from kern import regeln  # noqa: E402
MOD = os.path.join(EDEN, "module", "eden_rise")
EV = {e["id"]: e for e in json.load(open(os.path.join(MOD, "ereignisse.json"), encoding="utf-8"))["events"]}
KAEMPFE = json.load(open(os.path.join(MOD, "kaempfe.json"), encoding="utf-8"))
ORTE = json.load(open(os.path.join(MOD, "auftraege.json"), encoding="utf-8"))["orte"]


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def z_mit(*flags, **werte):
    return {"flags": list(flags), "werte": {k.replace("_", "."): v for k, v in werte.items()}, "tag": 31}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    import ereignisse_akt3_woche5 as W
    fest = [i for i, e in EV.items() if i.startswith("a3_") and e["wann"].get("pflicht") and e["wann"]["tage"][0] == e["wann"]["tage"][1]
            and 29 <= e["wann"]["tage"][0] <= 34]
    pruefen(len(fest) >= 14, "Woche 5 zieht an: %d feste Pflicht-Szenen" % len(fest))
    for i, (t, ph) in {"a3_villa_plan": (34, "fruehstueck"), "a3_villa_keller": (34, "tag"), "a3_villa_dinner": (34, "dinner"),
                       "a3_villa_ende": (34, "abend"), "a3_switched_off": (32, "nachmittag"), "a3_megan_monaco": (31, "dinner"),
                       "a3_maxwell_flug": (30, "fruehstueck"), "a3_einladung": (33, "tag")}.items():
        pruefen(EV[i]["wann"]["tage"] == [t, t] and EV[i]["wann"]["phasen"] == [ph], "%s an Tag %d (%s)" % (i, t, ph))
    pruefen("Join me. Name your price." in json.dumps(EV["a3_villa_dinner"]), "Alons letztes Angebot im Wortlaut")

    # Megans Wende: 4 Zeugen ODER 2 Beweise ODER Yamamoto Bindung 5 (Entscheid g: ohne Margot erreichbar)
    w = W.MEGAN_WENDE
    pruefen(not regeln.gilt(w, z_mit("a3_zeuge_petru", "a3_zeuge_mina", "a3_zeuge_batu")), "3 Zeugen reichen nicht")
    pruefen(regeln.gilt(w, z_mit("a3_zeuge_petru", "a3_zeuge_mina", "a3_zeuge_batu", "a3_zeuge_alva")), "4 Zeugen reichen")
    pruefen(not regeln.gilt(w, z_mit("a3_zeuge_petru_ehrlich", "a3_zeuge_mina_frei", "a3_zeuge_tuer_don", "a3_zeuge_tuer_casanova")),
            "Haltungs- und Tuer-Flags zaehlen nicht als Zeugen")
    pruefen(regeln.gilt(w, z_mit("alon_kiste_genutzt", "a3_siri_post")), "2 Beweise reichen")
    pruefen(regeln.gilt(w, z_mit(vertrauen_yamamoto=5)), "Yamamoto Bindung 5 reicht")

    # Sandru: Schiene oder Alons Schienen, nie beides
    g = W.GEKUEMMERT
    pruefen(regeln.gilt(g, z_mit("sandru_surren")) and not regeln.gilt(g, z_mit()), "gekuemmert: Summen, Herkunft oder Vertrauen 3")
    pruefen("a3_zeuge_sandru" in json.dumps(EV["a3_schiene"]) and "a3_zeuge_sandru" not in json.dumps(EV["a3_sandru_alon"]),
            "nur mit der Schiene sagt Sandru aus")

    # Nach Mitternacht: wer nicht bereit ist, hat nicht gefragt
    pruefen(regeln.gilt(W._mn_bereit("chiara"), z_mit(begehren_chiara=4)) and not regeln.gilt(W._mn_bereit("chiara"), z_mit(begehren_chiara=3)),
            "Chiara fragt ab Begehren 4")
    pruefen(not regeln.gilt(W._mn_bereit("rosi"), z_mit("gefeuert_rosi", begehren_rosi=5)), "gefeuerte Frauen fragen nicht")
    pruefen(regeln.gilt(W._mn_bereit("megan"), z_mit("megan_funke")), "Megan mit megan_funke")
    pruefen(all("a3_mn_%s" % p in EV for p, _n in W.MN_FRAUEN) and "a3_mn_nein" in EV, "neun Fragen und ein Nein")

    # Villa: Deal oder Endkampf, Kampf-Ausgaenge setzen Flags
    ziel = [f["direkt"] for o in EV["a3_villa_ende"]["optionen"] for f in o["folgen"] if "direkt" in f][0]
    pruefen(ziel[0] == {"wenn": {"flag": "a3_deal"}, "id": "a3_villa_deal"} and ziel[1]["id"] == "a3_villa_kampf", "Deal fuehrt zu Ende 1, sonst Endkampf")
    k = KAEMPFE["encounters"]["a3_alon"]
    pruefen(k["enemy"] == "alon_exo" and k["level"] == 10 and not k["flee_allowed"], "Endkampf gegen Alon im Exoskelett, Level 10, keine Flucht")
    pruefen(k["outcomes"]["ko"]["folgen"] == [{"flag": "a3_alon_besiegt"}] and k["outcomes"]["niederlage"]["folgen"] == [{"flag": "a3_alon_niederlage"}],
            "Ausgang des Endkampfs als Flag")
    e = KAEMPFE["enemies"]["alon_exo"]
    pruefen(e["element"] == "luft" and e["tier"] == "toedlich" and e.get("boss"), "Alon: Luft, toedlich, Boss")
    pruefen("a3_beweis_feuer" in json.dumps(EV["a3_villa_ordner"]), "Whites Einsatzplan ist ein Beweis")

    # Scrap Field: Maschinen geben Stahl ab Tag 24
    for bid in ("a3_scrap_drohne", "a3_scrap_paar"):
        gegner = KAEMPFE["encounters"][bid].get("enemies") or [KAEMPFE["encounters"][bid]["enemy"]]
        pruefen(all(KAEMPFE["enemies"][g]["cls"] == "maschine" for g in gegner), "%s: Maschinen (Stahl)" % bid)
    for oid in ("a3_orange", "a3_lot14", "a3_scrap"):
        pruefen(oid in ORTE and all(EV[s["id"]]["art"] == "ort" for s in ORTE[oid]["start"]), "Karte %s" % oid)
    print("Alle Pruefungen gruen.")


if __name__ == "__main__":
    main()
