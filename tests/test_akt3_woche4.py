# -*- coding: utf-8 -*-
r"""Akt 3, Woche 4 (Paket B, werkzeuge/eden_rise/ereignisse_akt3_woche4.py, Drehbuch Akt 3 Abschnitt 3 und 5):
Kalender der Pflicht-Szenen, Ducs Entscheide (Yacht-Gags erst ab Tag 25, Megan Tag 25, Minicu nicht vor der Festa),
Turbo-Tags, Karten und Wirkpunkte.

  python tests/test_akt3_woche4.py
"""
import json, os, re, sys

EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, EDEN)
MOD = os.path.join(EDEN, "module", "eden_rise")
EV = {e["id"]: e for e in json.load(open(os.path.join(MOD, "ereignisse.json"), encoding="utf-8"))["events"]}
ORTE = json.load(open(os.path.join(MOD, "auftraege.json"), encoding="utf-8"))["orte"]
TAGS = json.load(open(os.path.join(MOD, "stimme_tags.json"), encoding="utf-8"))
A3 = {i: e for i, e in EV.items() if i.startswith("a3_")}
TURBO = re.compile(r"\[(laugh|chuckle|sigh|gasp|cough|clear throat|sniff|shush)\]")


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def zeilen(e):
    return e["zeilen"] + [o["zeile"] for o in e["optionen"] if o.get("zeile")]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    pruefen(len(A3) >= 30, "%d Akt-3-Events der Woche 4" % len(A3))

    # Kalender: feste Pflicht-Szenen (Drehbuch Abschnitt 3)
    soll = {"a3_morgen": (24, "fruehstueck"), "a3_schwur": (24, "tag"), "a3_uhr": (25, "fruehstueck"),
            "a3_megan_landet": (25, "dinner"), "a3_festa_tafel": (26, "fruehstueck"), "a3_sonntag": (28, "tag"),
            "a3_berichte": (29, "abend")}
    for i, (tag, ph) in soll.items():
        w = A3[i]["wann"]
        pruefen(w.get("pflicht") and w["tage"] == [tag, tag] and w["phasen"] == [ph], "%s Pflicht an Tag %d (%s)" % (i, tag, ph))
    woche4 = [i for i, e in A3.items() if e["wann"].get("pflicht") and e["wann"]["tage"][0] == e["wann"]["tage"][1] and 24 <= e["wann"]["tage"][0] <= 28]
    pruefen(len(woche4) == 6, "Woche 4 atmet: 6 feste Pflicht-Szenen (%s)" % ", ".join(sorted(woche4)))
    pruefen(not any(e["wann"].get("pflicht") and e["wann"]["tage"] == [27, 27] for e in A3.values()), "Tag 27 ganz frei")
    gezogen = [e for e in A3.values() if e["art"] != "ort" and e["wann"]["tage"] != [24, 35]]
    pruefen(all("akt2_ende" in json.dumps(e["wann"].get("bedingung") or {}) for e in gezogen), "alle gezogenen Szenen erst nach dem Cliffhanger")

    # Ducs Entscheide (E-122)
    yacht = [i for i in A3 if i.startswith("a3_yacht_")]
    pruefen(yacht and all(A3[i]["wann"]["tage"][0] >= 25 for i in yacht), "Yacht-Gags erst ab Tag 25 (Tag 24 gehoert Buenaventura)")
    pruefen(A3["a3_megan_landet"]["wann"]["tage"] == [25, 25], "Megan kommt an Tag 25")
    pruefen(not any("minicu" in json.dumps(e["personen"]) or any(z["wer"] == "minicu" for z in zeilen(e)) for e in A3.values()),
            "Minicu tritt vor der Festa nicht auf")
    roh = json.dumps(A3, ensure_ascii=False).lower()
    pruefen(not re.search(r"(takes off|removes|pushes up|lifts) (his )?sunglasses", roh), "Duc nimmt die Sonnenbrille nie ab")
    maxwell = [i for i, e in A3.items() if "maxwell" in json.dumps(e["personen"])]
    pruefen(all(A3[i]["wann"]["tage"][1] <= 29 or A3[i]["wann"]["tage"][0] >= 33 for i in maxwell), "Maxwell nicht an Tag 30 bis 32")

    # Turbo-Tags: jede gesprochene Zeile hat einen Eintrag mit Tag, der Spieltext keinen
    gesprochen = {(z["wer"], z["text"]): z["gesprochen"] for z in TAGS["zeilen"] if (z.get("quelle") or "").startswith("akt3")}
    for e in A3.values():
        for zl in zeilen(e):
            if TURBO.search(zl["text"]) or "[" in zl["text"]:
                raise AssertionError("%s: Tag im Spieltext: %s" % (e["id"], zl["text"]))
            g = gesprochen.get((zl["wer"], zl["text"]))
            if not g or not TURBO.search(g) or "[groan]" in g:
                raise AssertionError("%s: gesprochene Zeile ohne Turbo-Tag: %s" % (e["id"], zl["text"]))
    pruefen(True, "alle %d Zeilen mit Turbo-Tag, keiner im Spieltext" % len(gesprochen))

    # Karten (Orte): Start-Frames sind Ort-Frames, Lend a Hand setzt den ersten Stein
    for oid in ("a3_baustellen", "a3_alva", "a3_siri", "a3_nonna"):
        pruefen(oid in ORTE and all(EV[s["id"]]["art"] == "ort" for s in ORTE[oid]["start"]), "Karte %s" % oid)
    for hid in ("post", "batu", "bar", "werkstatt"):
        f = [fo for o in A3["a3_bau_" + hid]["optionen"] for fo in o["folgen"]]
        pruefen(sum(1 for fo in f if fo.get("aufbau_beginnen") == hid) == 3, "Lend a Hand %s: drei Helfer-Wahlen setzen den ersten Stein" % hid)

    # Wirkpunkte: Zeugen-Tueren aus den Dank-Szenen, Rudern, Alvas Runde, Totos Versprechen, Charly
    for p in ("mina", "batu", "alva", "petru"):
        pruefen(any(fo.get("flag") == "a3_zeuge_" + p for o in EV[{"mina": "a3_dank_post", "batu": "a3_dank_batu", "alva": "a3_dank_bar", "petru": "a3_dank_werkstatt"}[p]]["optionen"] for fo in o["folgen"]),
                "Dank-Szene oeffnet die Zeugen-Tuer von %s" % p)
    pruefen(any(z.get("wenn") == {"flag": "bl_dorf_rudert"} for z in A3["a3_morgen_petru"]["zeilen"]), "Petru liest bl_dorf_rudert")
    pruefen(any(z.get("wenn") == {"flag": "bl_alva_runde"} for z in A3["a3_dank_bar"]["zeilen"]), "Alvas Tafel liest bl_alva_runde")
    ziel = [fo["direkt"] for o in A3["a3_uhr"]["optionen"] for fo in o["folgen"] if "direkt" in fo][0]
    pruefen(ziel[0]["id"] == "a3_uhr_toto" and "versprochen" in json.dumps(ziel[0]["wenn"]), "Totos Kiste nur mit Versprechen")
    pruefen(all(any(fo.get("flag") == "a3_charly_geld" for fo in o["folgen"]) for o in A3["a3_charly_geld"]["optionen"]), "Charlys Geld wirkt in jeder Wahl")
    pruefen("rt_charly_weg" in json.dumps(A3["a3_charly_geld"]["wann"]), "Charlys Geld nur, wenn sie nicht verloren ist")
    from kern import akt3, aufbau, regeln
    # Morgen-Vignetten: Kevin (nicht Tag 26), Dank heiler Haeuser je Morgen eins, Legion einmal
    z = {"tag": 25, "flags": ["akt2_ende", "tk_haus_weg_post", "bl_verband_wolff", "buenaventura_schwur"], "kueche": {"rohstoffe": {}}}
    pruefen(akt3.morgen({"tag": 25, "flags": []}) == [], "Vignetten erst nach dem Cliffhanger")
    zl = akt3.morgen(z)
    pruefen(akt3.KEVIN in zl and any("came through the fire" in x for x in zl), "Tag 25: Kevin und ein heiles Haus")
    pruefen(akt3.KEVIN not in akt3.morgen(dict(z, tag=26)), "Tag 26 sitzt Kevin auf der Tafel")
    pruefen(akt3.KEVIN not in akt3.morgen(dict(z, tag=35)), "Tag 35: keine Kevin-Zeile mehr")
    aufbau.beginnen(z, "post")
    z["tag"] = 27
    zl = akt3.morgen(z)
    pruefen(akt3.LEGION in zl and aufbau.baustellen(z)["post"]["stufe"] == 1, "Legion baut einmal eine Stufe")
    pruefen(akt3.LEGION not in akt3.morgen(dict(z, tag=28)), "Legion nur einmal")
    pruefen("bl_nachtwache_pascal" in json.dumps(EV["bl_nachtwache"]) and "bl_nachtwache_pascal" in json.dumps(A3["a3_revanche"]),
            "Holms Vorwurf nur nach 'Nobody. Pascal has it.'")
    pruefen(A3["a3_nonna_mina"]["wann"]["tage"] == [31, 31] and "a3_nonna_kiste" in json.dumps(A3["a3_nonna_mina"]["wann"]), "Mina bringt den Schluessel, wenn Duc nicht kam")
    z = {"flags": [], "ev": {"versprechen": [{"an": "toto", "text": "Make the crate count against Alon"}]}}
    pruefen(regeln.gilt({"versprochen": ["toto", "crate"]}, z) and not regeln.gilt({"versprochen": ["rosi", "crate"]}, z), "Bedingung versprochen")
    print("Alle Pruefungen gruen.")


if __name__ == "__main__":
    main()
