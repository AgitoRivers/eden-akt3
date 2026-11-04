# -*- coding: utf-8 -*-
r"""Akt 3, Paket F: Kommission, Festa mit Minicu, Mitternacht, Festa-Schalter, Saeulen und Enden
(werkzeuge/eden_rise/ereignisse_akt3_finale.py, kern/akt3.py, kern/abschluss.py).

  python tests/test_akt3_finale.py
"""
import json, os, sys

EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, EDEN)
from kern import abschluss, akt3  # noqa: E402
MOD = os.path.join(EDEN, "module", "eden_rise")
EV = {e["id"]: e for e in json.load(open(os.path.join(MOD, "ereignisse.json"), encoding="utf-8"))["events"]}
MODUL = json.load(open(os.path.join(MOD, "modul.json"), encoding="utf-8"))
REIHE = [e["id"] for e in json.load(open(os.path.join(MOD, "ereignisse.json"), encoding="utf-8"))["events"]]


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def z_mit(*flags, **werte):
    return {"flags": list(flags), "werte": {k.replace("_", "."): v for k, v in werte.items()}, "tag": 35}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    k = EV["a3_kommission"]["wann"]
    pruefen(k["tage"] == [35, 35] and k["phasen"] == ["tag"] and k.get("pflicht"), "Kommission Tag 35, Phase tag (wie mo_kommission)")
    pruefen(REIHE.index("mo_kommission") < REIHE.index("a3_kommission"), "mo_kommission eroeffnet, a3_kommission schliesst an (F-25)")
    pruefen('"gesehen": "mo_kommission"' in json.dumps(EV["a3_kommission"]), "keine zweite Ansage nach mo_kommission")
    pruefen(EV["a3_festa"]["wann"]["tage"] == [35, 35] and EV["a3_festa"]["wann"]["phasen"] == ["abend"], "Festa ist die Schlussszene am Abend von Tag 35")
    for i in ("br_ehrenbuerger", "ab_casanova_flamenco", "gv_rotes_kleid"):
        w = EV[i]["wann"]
        pruefen(w["tage"] == [35, 35] and w["phasen"] == ["abend"] and w.get("pflicht") and EV[i]["bild"] == "village_piazza"
                and "akt3_festa" in json.dumps(w), "Festa-Schalter: %s an Tag 35 auf der Piazza (F-22)" % i)
    pruefen("a3_deal" in json.dumps(EV["br_ehrenbuerger"]["wann"]), "kein Ehrenbuerger im Deal")
    # Minicu (Entscheid c): erst auf der Festa, in allen Enden zu sehen
    vor = [i for i, e in EV.items() if i.startswith("a3_") and i not in ("a3_festa_minicu",)
           and any(z["wer"] == "minicu" for z in e["zeilen"] + [o["zeile"] for o in e["optionen"] if o.get("zeile")])]
    pruefen(not vor, "Minicu spricht nur auf der Festa")
    pruefen("minicu" in json.dumps(EV["a3_festa_minicu"]["personen"]) and "Minicu" in EV["a3_festa_deal"]["lage"], "Minicu in jedem Ende im Bild")
    pruefen(all("a3_mitternacht_" + p in EV for p in ("chiara", "alva", "lea", "sophia", "rosi", "lola", "siri", "bibi", "megan")), "Mitternacht fuer jede Frau")

    # Saeulen und Enden
    alle = z_mit("a3_beweis_feuer", "alon_kiste_genutzt", "a3_siri_post", "a3_megan_wende", "a3_alon_besiegt",
                 *["a3_zeuge_" + p for p in ("petru", "mina", "batu", "alva", "casanova")])
    pruefen(akt3.ende(alle) == "3", "alle vier Saeulen: Ende 3")
    pruefen(akt3.ende(dict(alle, flags=alle["flags"] + ["a3_deal"])) == "1", "Angebot angenommen: Ende 1, immer moeglich")
    pruefen(akt3.ende(z_mit()) == "0", "keine Saeule: Ende 0")
    ohne_geld = dict(alle, flags=[f for f in alle["flags"] if f != "a3_megan_wende"])
    pruefen(akt3.ende(ohne_geld) == "2.5a", "alle ausser Geld: 2½a")
    pruefen(akt3.ende(dict(ohne_geld, werte={"vertrauen.yamamoto": 5})) == "3", "Geld auch ueber Yamamoto 5 (Entscheid g)")
    pruefen(akt3.ende(z_mit("a3_beweis_feuer", "alon_kiste_genutzt", "a3_kassenbuch_alles", "a3_alon_festgenommen")) == "2c",
            "2 Beweise mit Kassenbuch 'alles' = Wahrheit; Festnahme = Staerke: 2c")
    vier = z_mit(*["a3_zeuge_" + p for p in ("petru", "mina", "batu", "alva")])
    pruefen(not akt3.saeulen(vier)["gemeinschaft"] and akt3.saeulen(dict(vier, flags=vier["flags"] + ["a3_kassenbuch_teil"]))["gemeinschaft"],
            "4 Zeugen tragen nur mit Kassenbuch 'teil'")
    pruefen(akt3.saeulen(dict(vier, werte={"ruf": 5}))["gemeinschaft"], "Ruf ab 5 zaehlt wie ein Zeuge")
    karte = abschluss.berechnen(dict(alle, flags=alle["flags"] + ["akt2_ende", "a3_festa_fertig"]), dict(MODUL, akt3_spielbar=True))
    pruefen(karte["akt"] == 3 and karte["ende"] == "3" and "Rewritten" in karte["titel"], "Schlusskarte zeigt das Ende")
    pruefen(any("Pascal" in a["text"] for a in karte["absaetze"]) and any("Sign here" in a["text"] for a in karte["absaetze"]),
            "Pascal in jedem Ende, Minas Einschreiben als Epilog")
    print("Alle Pruefungen gruen.")


if __name__ == "__main__":
    main()
