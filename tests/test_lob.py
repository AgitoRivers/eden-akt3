# -*- coding: utf-8 -*-
"""Lob fuer Attributsteigerungen (27.10.2026): Daten, Vormerken, Auswahl, Grenzen, Szenenstart, Handy-Fallback.

Laeuft ohne Modell, Stimme und Netz.

  python tests\\test_lob.py
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(HERE)
sys.path.insert(0, EDEN)
from kern import handy, kampf, llm, lob, stimme, szene, zustand  # noqa: E402

MODUL = json.load(open(os.path.join(EDEN, "module", "eden_rise", "modul.json"), encoding="utf-8"))
ATTRIBUTE = ["charm", "empathy", "perception", "cunning", "courage", "strength"]
SPRECHER = {"chiara", "sophia", "lea", "rosi", "siri", "alva", "lola", "megan", "maxwell", "jana", "toto", "yasin", "yamamoto"}
OHNE_LOB = {"bibi"}   # schaetzt Attribute fuer die Bewunderung (4fb3fa08), Lob-Zeilen fehlen noch (offen in testing.md)


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def neues_spiel(tag=3, phase="tag"):
    z = zustand.neu(MODUL, "entspannt")
    zustand.persona_setzen(z, MODUL, MODUL["personas"][0])
    z["tag"], z["phase"], z["status"] = tag, phase, "wahl"
    z["heute"] = []
    return z


def daten_pruefen():
    d = lob.daten(MODUL)
    pruefen(set(d) == SPRECHER, "13 Sprecher, Holm nicht dabei (%s)" % sorted(set(d) ^ SPRECHER))
    wer_schaetzt = {p for p, v in MODUL["personen"].items() if v.get("schaetzt")}
    pruefen(wer_schaetzt == SPRECHER | OHNE_LOB, "die 13 und %s schaetzen Attribute im Modul (%s)" % (sorted(OHNE_LOB), sorted(wer_schaetzt ^ (SPRECHER | OHNE_LOB))))
    for p in SPRECHER:
        s = MODUL["personen"][p]["schaetzt"]
        pruefen(len(s) == 2 and set(s) <= set(ATTRIBUTE) and sorted(d[p]) == sorted(s), "%s: zwei Attribute, Zeilen dazu" % p)
        for att in s:
            pruefen(sorted(d[p][att]) == ["3", "4", "5"], "%s.%s: Zeilen fuer 3/4/5" % (p, att))
    anzahl = {a: sum(a in v["schaetzt"] for v in MODUL["personen"].values() if v.get("schaetzt")) for a in ATTRIBUTE}
    pruefen(min(anzahl.values()) >= 4, "jedes Attribut hat mindestens 4 Sprecher: %s" % anzahl)
    tags = {z["text"]: z["gesprochen"] for z in json.load(open(stimme.TAGS_DATEI, encoding="utf-8"))["zeilen"]}
    fehler = []
    for p, atts in d.items():
        for att, st in atts.items():
            for w, t in st.items():
                g = tags.get(t)
                if not g or not stimme.TAG_MUSTER.search(g) or stimme.ohne_tags(g).replace("  ", " ") != t:
                    fehler.append("%s.%s.%s" % (p, att, w))
                if stimme.getaggt(t) != g or stimme.TAG_MUSTER.search(t) or set('"*_~\n') & set(t):
                    fehler.append("%s.%s.%s (Anzeige/Stimme)" % (p, att, w))
    pruefen(not fehler, "alle 78 Zeilen: Anzeige ohne Tag, Stimme mit Tag %s" % fehler[:3])


def vormerken_pruefen():
    z = neues_spiel()
    lob.vormerken(z, "strength", 2)
    pruefen(not z.get("lob", {}).get("offen"), "Wert 2 ist kein Meilenstein")
    lob.vormerken(z, "strength", 3)
    lob.vormerken(z, "strength", 4)
    lob.vormerken(z, "courage", 3)
    pruefen(z["lob"]["offen"]["strength"]["wert"] == 4 and z["lob"]["offen"]["courage"]["wert"] == 3,
            "mehrere Punkte werden gebuendelt: je Attribut zaehlt der hoechste Wert")
    z = neues_spiel()
    z.setdefault("fortschritt", {})
    c = kampf.progress(z)
    c["attributpunkte"] = 2
    z["persona"]["attribute"]["strength"] = 2
    kampf.attribut_steigern(z, "strength")
    pruefen(z["lob"]["offen"]["strength"]["wert"] == 3, "ein ausgegebener Attributpunkt (2 -> 3) merkt den Kommentar vor")
    z["persona"]["attribute"]["charm"] = 3
    kampf.attribut_steigern(z, "charm")
    pruefen(z["lob"]["offen"]["charm"]["wert"] == 4, "charm 3 -> 4 ebenfalls")


def auswahl_pruefen():
    z = neues_spiel()
    lob.vormerken(z, "strength", 4)
    pruefen(lob.waehlen(z, MODUL, ["chiara", "lola", "siri"]) is None, "niemand Passendes da: nichts wird gesagt")
    w = lob.waehlen(z, MODUL, ["chiara", "maxwell"])
    pruefen(w and w["pid"] == "maxwell" and w["att"] == "strength" and w["wert"] == 4, "Maxwell kommentiert Staerke")
    pruefen(w["text"] == lob.daten(MODUL)["maxwell"]["strength"]["4"], "es ist die feste Zeile")
    lob.gebucht(z, w)
    pruefen("strength" not in z["lob"]["offen"], "Meilenstein ist verbraucht")
    lob.vormerken(z, "courage", 3)
    pruefen(lob.waehlen(z, MODUL, ["chiara", "maxwell"]) is None, "hoechstens ein Kommentar je Phase")
    z["phase"] = "dinner"
    w2 = lob.waehlen(z, MODUL, ["chiara", "maxwell"])
    pruefen(w2 and w2["pid"] in ("chiara", "maxwell") and w2["att"] == "courage", "naechste Phase: der naechste darf")
    pruefen(w2["pid"] == "chiara", "Maxwell hat gerade gesprochen, Chiara war laenger still")
    lob.gebucht(z, w2)
    z["phase"] = "abend"
    lob.vormerken(z, "strength", 4)                       # derselbe Meilenstein ein zweites Mal geht nicht an dieselbe Figur
    pruefen(lob.waehlen(z, MODUL, ["maxwell"]) is None, "dieselbe Figur sagt denselben Wert nie zweimal")
    pruefen(lob.waehlen(z, MODUL, ["maxwell", "jana", "toto"])["pid"] in ("jana", "toto"), "andere Staerke-Freunde duerfen")
    pruefen(lob.waehlen(neues_spiel(), MODUL, ["maxwell"]) is None, "ohne Vormerkung kein Kommentar")
    z = neues_spiel()
    lob.vormerken(z, "strength", 3)
    pruefen(lob.waehlen(z, MODUL, ["holm"]) is None, "Holm sagt nichts")


def szenenstart_pruefen():
    z = neues_spiel()
    lob.vormerken(z, "courage", 4)
    szene.CFG = {}
    ruf = []
    echt = szene.sprechen
    szene.sprechen = lambda z, modul, sz, pid, duc, extra="", nachschlag=False: ruf.append(pid) or sz["log"].append(
        {"art": "figur", "wer": pid, "name": pid, "text": "Opening.", "gezeigt": "Opening."})
    echt_buehne = (szene.buehne.set_waehlen, szene.buehne.sprite, szene.buehne.szenenbild)
    szene.buehne.set_waehlen = lambda *a, **k: None
    szene.buehne.sprite = lambda *a, **k: None
    szene.buehne.szenenbild = lambda *a, **k: "bild"
    s = {"id": "t_lob", "titel": "Test", "ort": next(iter(MODUL["raeume"])), "anwesend": ["chiara"], "ausgangslage": "x"}
    z["plan"] = {"phasen": {}}
    try:
        sz = szene.starten(z, MODUL, s)
    finally:
        szene.sprechen = echt
        szene.buehne.set_waehlen, szene.buehne.sprite, szene.buehne.szenenbild = echt_buehne
    figuren = [e for e in sz["log"] if e["art"] == "figur"]
    pruefen(len(figuren) == 2 and figuren[0]["text"] == "Opening.", "erst die Eroeffnung der Szene ...")
    soll = lob.daten(MODUL)["chiara"]["courage"]["4"]
    pruefen(figuren[1]["wer"] == "chiara" and figuren[1]["gezeigt"] == '"%s"' % soll, "... dann Chiaras Lob als feste Zeile")
    pruefen(stimme.getaggt(stimme.vorlesen(figuren[1]["gezeigt"])) != soll, "die Stimme liest die Fassung mit Turbo-Tag")
    pruefen(not z["lob"]["offen"] and z["lob"]["phase"] == [3, "tag"], "gebucht: Meilenstein verbraucht, Phase belegt")


def handy_pruefen():
    z = neues_spiel()
    lob.vormerken(z, "strength", 5)
    pruefen(lob.handy_faellig(z, MODUL) == [], "frisch vorgemerkt: noch keine Nachricht (erst Szene abwarten)")
    z["phase"] = "nachmittag"
    pruefen(lob.handy_faellig(z, MODUL) == [], "nach einer Phase noch nicht")
    z["phase"] = "dinner"                                  # 2 Phasen spaeter (tag -> nachmittag -> dinner)
    zeilen = lob.handy_faellig(z, MODUL)
    pruefen(len(zeilen) == 1 and zeilen[0].startswith("📱 Message from "), "nach zwei Phasen kommt sie aufs Handy: %s" % zeilen)
    f = z["handy"][-1]
    wer = f["von"]
    pruefen(wer in ("megan", "maxwell", "jana", "toto") and f["verlauf"][-1]["text"] == lob.daten(MODUL)[wer]["strength"]["5"],
            "Staerke-Freund schreibt die feste Zeile (%s)" % wer)
    pruefen(f["gelesen"] is False and not z["lob"]["offen"], "ungelesen, Meilenstein verbraucht")
    sperre = handy.gesperrt(z, MODUL, wer)
    pruefen((sperre is None) == bool(MODUL["personen"][wer].get("karte")), "Figur ohne ST-Karte: nur lesen, keine Antwort (%s)" % sperre)
    lob.vormerken(z, "charm", 3)
    z["phase"] = "abend"
    pruefen(lob.handy_faellig(z, MODUL) == [], "neu vorgemerkt: wartet erst wieder zwei Phasen")
    z["tag"], z["phase"] = 4, "tag"
    lob.vormerken(z, "perception", 3)
    z["phase"] = "nacht"
    z["lob"]["offen"]["perception"]["seit"] -= 3
    z["lob"]["phase"] = [z["tag"], z["phase"]]            # in dieser Phase sprach schon jemand
    pruefen(lob.handy_faellig(z, MODUL) == [], "in derselben Phase nie zwei")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    llm.json_chat = lambda *a, **k: ({}, 0.0)
    llm.chat = lambda *a, **k: ("", 0.0)
    daten_pruefen()
    vormerken_pruefen()
    auswahl_pruefen()
    szenenstart_pruefen()
    handy_pruefen()
    print("ALLES OK")


if __name__ == "__main__":
    main()
