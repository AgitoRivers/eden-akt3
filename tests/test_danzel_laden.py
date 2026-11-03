# -*- coding: utf-8 -*-
r"""Danzels Laden an der Piazza (Duc 30.10.2026): gibt es in beiden Ausgaengen der Quest (E-112), ab dem 3. Tag nach dem Quest-Ende. Dann
liegt alle Kleidung bei ihm; vorher und ohne Laden bleibt sie bei den alten Haendlern.

  python tests\test_danzel_laden.py
"""
import json, os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HIER))
from kern import handel, zustand  # noqa: E402

MOD = os.path.join(os.path.dirname(HIER), "module", "eden_rise")
MODUL = json.load(open(os.path.join(MOD, "modul.json"), encoding="utf-8"))
KLEIDUNG = MODUL["laeden"]["danzel"]["uebernimmt"]
for _l in MODUL["laeden"].values():
    _l["wechselnd"] = False                          # die ganze Ware pruefen, nicht den Ausschnitt des Tages


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def spiel(tag, flags=()):
    z = zustand.neu(MODUL, "entspannt")
    zustand.persona_setzen(z, MODUL, MODUL["personas"][0])
    z["tag"], z["heute"] = tag, [{"ort": "alvas_bar"}]
    z["flags"].extend(flags)
    handel.init(z, MODUL)
    return z


def ids(z, laden):
    return {w["id"] for w in handel.sortiment(z, MODUL, laden) or []}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    pruefen(len(KLEIDUNG) == 6 and all("danzel" in MODUL["items"][i]["wo"] for i in KLEIDUNG), "sechs Stueck Kleidung gehoeren zum Laden")
    pruefen(all(len(MODUL["items"][i]["wo"]) == 2 for i in KLEIDUNG), "jedes Stueck hat seinen alten Haendler behalten")

    z = spiel(9)
    pruefen(handel.sortiment(z, MODUL, "danzel") is None, "ohne Red Trio kein Laden")
    weg = handel._umgezogen(z, MODUL, "alva")
    pruefen(not weg and {"wool_socks", "wollmuetze", "flamenco_dessous"} <= ids(z, "alva"), "ohne Laden verkauft Alva weiter")

    # Quest an Tag 13 beendet: flag_seit zaehlt ab dem Tag, an dem rt_ende_tag gesetzt wurde
    z = spiel(14, ["rt_ausgang_alle", "rt_ende_tag"])
    z.setdefault("flag_tag", {})["rt_ende_tag"] = 13
    pruefen(handel.sortiment(z, MODUL, "danzel") is None, "einen Tag nach der Quest noch zu")
    z["tag"] = 16
    pruefen(ids(z, "danzel") == set(KLEIDUNG), "drei Tage danach offen, alle sechs Stueck da (%s)" % sorted(ids(z, "danzel")))
    pruefen(not ({"wool_socks", "wollmuetze", "flamenco_dessous"} & ids(z, "alva")), "Alva verkauft keine Kleidung mehr")
    pruefen(not (set(KLEIDUNG) & ids(z, "toto")), "Toto verkauft keine Kleidung mehr")
    pruefen("danzel" in {k for k, l in MODUL["laeden"].items() if handel.laden_offen(z, l)}, "Laden steht im Handel")

    z = spiel(16, ["rt_ausgang_getrennt", "rt_ende_tag"])
    z.setdefault("flag_tag", {})["rt_ende_tag"] = 13
    pruefen(ids(z, "danzel") == set(KLEIDUNG) and "wool_socks" not in ids(z, "alva"), "getrennt: Laden offen, Alva verkauft keine Kleidung mehr")
    z["tag"] = 14
    pruefen(handel.sortiment(z, MODUL, "danzel") is None, "getrennt: einen Tag nach der Quest noch zu")
    laden = json.load(open(os.path.join(MOD, "laeden.json"), encoding="utf-8"))["laeden"]["danzel"]
    pruefen(len(laden["zeilen"]["gruss_allein"]) == 3 and "gruss_allein" not in laden["gruss_stufen"] and laden.get("text_allein"), "getrennt: eigene knappe Begruessungen")
    print("Alles gut.")


if __name__ == "__main__":
    main()
