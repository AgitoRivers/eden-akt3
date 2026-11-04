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
    pruefen(regeln.gilt(W._mn_bereit("chiara"), z_mit(vertrauen_chiara=4, begehren_chiara=4))
            and not regeln.gilt(W._mn_bereit("chiara"), z_mit(vertrauen_chiara=3, begehren_chiara=5)), "Einladung ab Vertrauen 4 und Begehren 4")
    pruefen(not regeln.gilt(W._mn_bereit("rosi"), z_mit("gefeuert_rosi", vertrauen_rosi=5, begehren_rosi=5)), "gefeuerte Frauen laden nicht ein")
    pruefen(regeln.gilt(W._mn_bereit("megan"), z_mit("megan_funke", vertrauen_megan=4)), "Megan mit megan_funke und Vertrauen 4")
    pruefen(all("a3_einl_%s" % p in EV and "a3_einl_%s_spaet" % p in EV for p, _n in W.MN_FRAUEN), "je Frau eine Einladung und eine ehrliche Absage")
    pruefen(all(len(EV["a3_einl_" + p]["optionen"]) == 2 for p, _n in W.MN_FRAUEN), "Duc muss jeder antworten: Ja oder Nein")
    ziel = [f["direkt"] for o in EV["a3_einl_chiara"]["optionen"] for f in o["folgen"] if "direkt" in f][0]
    pruefen(ziel[0]["id"] == "a3_einl_alva_spaet" and ziel[1]["id"] == "a3_einl_alva" and ziel[-1]["id"] == "a3_einl_ende_nein",
            "nach einem Ja kommt bei der naechsten die ehrliche Absage")
    pruefen("Looks for" not in json.dumps(EV["a3_mn_start"]), "keine Liste aller Frauen mehr (E-060)")

    # Villa: Deal oder Endkampf, Kampf-Ausgaenge setzen Flags
    ziel = [f["direkt"] for o in EV["a3_villa_ende"]["optionen"] for f in o["folgen"] if "direkt" in f][0]
    pruefen(ziel[0]["id"] == "a3_villa_lange" and ziel[1] == {"wenn": {"flag": "a3_deal"}, "id": "a3_villa_deal"} and ziel[2]["id"] == "a3_villa_kampf",
            "★ vor Deal, Deal fuehrt zu Ende 1, sonst Endkampf")
    st = W.STERN
    voll = z_mit("meta_ende_1", *W.BEWEISE[:3], *["a3_zeuge_" + p for p in W.ZEUGEN[:5]], vertrauen_yamamoto=5)
    pruefen(regeln.gilt(st, voll) and not regeln.gilt(st, dict(voll, flags=[f for f in voll["flags"] if f != "meta_ende_1"])),
            "★ nur, wenn Ende 1 in einem frueheren Durchlauf gesehen wurde")
    k = KAEMPFE["encounters"]["a3_alon"]
    pruefen(k["enemy"] == "alon_exo" and k["level"] == 10 and not k["flee_allowed"], "Endkampf gegen Alon im Exoskelett, Level 10, keine Flucht")
    pruefen(k["outcomes"]["ko"]["folgen"] == [{"flag": "a3_alon_besiegt"}] and k["outcomes"]["niederlage"]["folgen"] == [{"flag": "a3_alon_niederlage"}],
            "Ausgang des Endkampfs als Flag")
    from kern import regeln as R
    def helfer(*flags):
        z = {"flags": list(flags), "werte": {}}
        v = next((x["aktionen"] for x in k["beistand"] if R.gilt(x.get("wenn"), z)), None)
        return sorted(a["wer"] for a in (v or []) if a)
    pruefen(helfer() == [] and helfer("elsa_hilft") == ["Elsa"], "Endkampf: nur wer da ist, greift ein")
    pruefen(helfer("a3_villa_mit_rosi", "elsa_hilft", "bl_verband_wolff", "holm_zurueck", "buenaventura_schwur")
            == sorted(["Rosi and Unit-01", "Elsa", "Wolff", "Holm", "Buenaventura"]), "Endkampf: alle Verbuendeten zusammen")
    pruefen(k["beistand"][0]["aktionen"][0] is None and k["lp_faktoren"] == [0.8], "Hilfe ab Runde 2, Kampf kuerzer (80 %)")
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
