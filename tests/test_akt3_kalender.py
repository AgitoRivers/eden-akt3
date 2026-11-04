# -*- coding: utf-8 -*-
r"""Akt 3, Paket A (Drehbuch docs/wiki/welt/drehbuch_akt3.md, Abschnitt 12): Kalender-Schalter, Gags bis Tag 31,
Ereignis-Dichte je Woche, Yacht in Reparatur, Flag bl_dorf_rudert, Holms Revanche ab Tag 24.

  python tests/test_akt3_kalender.py
"""
import json, os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(HIER)
sys.path.insert(0, EDEN)
sys.path.insert(0, os.path.join(EDEN, "werkzeuge", "eden_rise"))
from kern import abschluss, ereignisse, schiessen, taktik  # noqa: E402
import ereignisse_fenster  # noqa: E402

MOD = os.path.join(EDEN, "module", "eden_rise")
MODUL = json.load(open(os.path.join(MOD, "modul.json"), encoding="utf-8"))
EV = {e["id"]: e for e in json.load(open(os.path.join(MOD, "ereignisse.json"), encoding="utf-8"))["events"]}
TAKTIK = json.load(open(os.path.join(MOD, "taktik.json"), encoding="utf-8"))


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def main():
    sys.stdout.reconfigure(encoding="utf-8")

    # Schalter: bis die Akt-3-Events gebaut sind, endet die Beta nach Tag 23
    spielbar = MODUL.get("akt3_spielbar")
    pruefen(spielbar is False, "modul.akt3_spielbar = false (Paket A)")
    pruefen(MODUL["zeitraster"]["tage"] == (35 if spielbar else 23), "zeitraster.tage passt zum Schalter")
    z = {"flags": ["akt2_ende"], "tag": 24}
    pruefen(abschluss.berechnen(z, MODUL)["akt"] == 2, "ohne Schalter: Beta-Schluss Akt 2")
    pruefen(abschluss.berechnen(z, dict(MODUL, akt3_spielbar=True))["akt"] == 3, "mit Schalter: Platzhalter Akt 3")

    # Gags: bis Tag 31, mit Maxwell bis 29, Handy ungeprueft bis 21, Leiter und Abende bis 35
    for i in ereignisse_fenster.OEFFNEN:
        e = EV.get(i)
        if not e:
            continue
        a2 = e["wann"]["akt2"]
        if i.startswith(("sf_", "sfn_")) or e["art"] == "abend":
            soll = [8, 35]
        elif i.startswith("hy_"):
            soll = [8, 21]
        elif "maxwell" in json.dumps(e, ensure_ascii=False).lower():
            soll = [8, 29]
        else:
            soll = [8, 31]
        if a2 != soll:
            raise AssertionError("%s: akt2 %s, erwartet %s" % (i, a2, soll))
    pruefen(EV["gv_quiz"]["wann"]["akt2"] == [8, 31], "freier Gag gv_quiz bis Tag 31")
    pruefen(EV["mt_zehn"]["wann"]["akt2"] == [8, 29], "Maxwell-Gag mt_zehn bis Tag 29")
    gag = EV["gv_quiz"]
    pruefen(not ereignisse.passt({"tag": 32, "flags": []}, MODUL, gag, "abend"), "Tag 32 gagfrei")

    # Dichte: Woche 4 atmet (0,6), Woche 5 und Akt 2 bei 0,45
    f = ereignisse._akt2_faktor
    pruefen(f({"tag": 20}, "zufall") == 0.45 and f({"tag": 24}, "zufall") == 0.6 and f({"tag": 28}, "zufall") == 0.6
            and f({"tag": 29}, "zufall") == 0.45 and f({"tag": 26}, "handy") == 0.6, "Ereignis-Dichte je Woche")

    # Yacht in Reparatur: Gags an Bord ruhen, an Land nicht, Leiter-Szenen nicht
    kaputt = {"tag": 26, "flags": ["tk_yacht_weg"]}
    pruefen(ereignisse.yacht_in_reparatur(kaputt), "tk_yacht_weg ab Tag 24: Reparatur")
    pruefen(not ereignisse.yacht_in_reparatur({"tag": 26, "flags": ["tk_yacht_weg", "a3_yacht_repariert"]}), "nach Reparatur frei")
    pruefen(not ereignisse.yacht_in_reparatur({"tag": 22, "flags": ["tk_yacht_weg"]}), "in der Belagerung keine Reparatur")
    pruefen(ereignisse.an_bord(MODUL, gag) and not ereignisse.an_bord(MODUL, EV["auf_karaoke"]), "main_salon an Bord, Bar an Land")
    da = ereignisse._da
    ereignisse._da = lambda z, m, p: True            # Anwesenheit hier nicht pruefen, nur die Reparatur-Regel
    try:
        def geht(e, flags):
            ph = e["wann"]["phasen"][0]
            return ereignisse.passt({"tag": 26, "flags": flags, "werte": {}, "phase": ph}, MODUL, e, ph)
        pruefen(geht(gag, []) and not geht(gag, ["tk_yacht_weg"]), "Gag an Bord ruht waehrend der Reparatur")
        pruefen(geht(gag, ["tk_yacht_weg", "a3_yacht_repariert"]), "Gag an Bord nach der Reparatur wieder da")
        land = EV["auf_karaoke"]
        pruefen(geht(land, ["tk_yacht_weg"]), "Gag an Land bleibt erlaubt")
    finally:
        ereignisse._da = da

    # Rudern: Flag nur in einer Kapitaens-Welle mit rudernden Booten
    kap = [n + 1 for n, w in enumerate(TAKTIK["wellen"]) if w.get("kapitaen")]
    pruefen(kap, "taktik.json hat eine Kapitaens-Welle")
    z = {"flags": []}
    taktik.rudern_merken(z, TAKTIK, {"dorf_rudert": True, "welle": kap[0]})
    pruefen("bl_dorf_rudert" in z["flags"], "bl_dorf_rudert nach Kapitaens-Welle")
    taktik.rudern_merken(z, TAKTIK, {"dorf_rudert": True, "welle": kap[0]})
    pruefen(z["flags"].count("bl_dorf_rudert") == 1, "Flag nur einmal")
    z = {"flags": []}
    taktik.rudern_merken(z, TAKTIK, {"dorf_rudert": False, "welle": kap[0]})
    andere = [n for n in range(1, len(TAKTIK["wellen"]) + 1) if n not in kap][0]
    taktik.rudern_merken(z, TAKTIK, {"dorf_rudert": True, "welle": andere})
    pruefen(not z["flags"], "kein Flag ohne Rudern oder ausserhalb der Kapitaens-Welle")

    pruefen(schiessen.HOLM_TAG == 24, "Holms Revanche ab Tag 24")
    from kern import auftraege, kabine
    pruefen(kabine.ort(MODUL, {"tag": 26, "flags": ["tk_yacht_weg"]}) == "church" and kabine.ort(MODUL, {"tag": 32, "flags": ["tk_yacht_weg", "a3_yacht_repariert"]}) != "church",
            "Ducs Kabine ist bei kaputter Yacht das Feldbett in der Kirche, bis zur Reparatur")
    o = [{"id": i} for i in ["macchia", "a3_alva", "a3_siri", "a3_lose", "a3_scrap", "a3_baustellen", "a3_schluss_lea", "a3_zeugen"]]
    ids = [x["id"] for x in auftraege._akt3_begrenzen(o)]
    pruefen(sorted(i for i in ids if i.startswith("a3_") and not i.startswith("a3_schluss")) == ["a3_baustellen", "a3_lose", "a3_zeugen"]
            and "macchia" in ids and "a3_schluss_lea" in ids, "hoechstens drei Akt-3-Karten, Vorrang Baustelle, Zeugen, Tafel; Romanzen extra")
    print("Alle Pruefungen gruen.")


if __name__ == "__main__":
    main()
