# -*- coding: utf-8 -*-
"""Toepfe je Quelle (Duc 02.11.2026): jede Quelle bringt nur bis zu ihrem Topf, keine erreicht allein 100."""
import json, os, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
from kern import zustand

MODUL = json.load(open(os.path.join(BASE, "module", "eden_rise", "modul.json"), encoding="utf-8"))


def stand(p=0, tag=99):
    return {"werte": {"vertrauen.rosi": zustand.stufe_aus(p), "begehren.rosi": zustand.stufe_aus(p)},
            "punkte": {"vertrauen.rosi": p, "begehren.rosi": p}, "tag": tag, "stufe_tag": {}, "flags": []}


def test_summe_und_keine_quelle_allein():
    for pid, t in MODUL["toepfe"].items():
        for i, achse in enumerate(zustand.PUNKTE_ACHSEN):
            summe = sum(t[q][i] for q in zustand.QUELLEN)
            if summe:
                assert summe > 100, (pid, achse, summe)
                assert max(t[q][i] for q in zustand.QUELLEN) < 100, (pid, achse)


def test_topf_begrenzt_nur_seine_quelle():
    z = stand(40)
    for _ in range(40):
        zustand.punkte_add(z, MODUL, "vertrauen.rosi", 4, quelle="geschenke", frei=True)
    assert zustand.punkte(z, "vertrauen.rosi") == 50          # Rosi: Geschenke 10
    zustand.punkte_add(z, MODUL, "vertrauen.rosi", 4, quelle="szenen", frei=True)
    assert zustand.punkte(z, "vertrauen.rosi") == 54


def test_gespraech_nicht_ueber_stufe_3_aber_danach_weiter():
    z = stand(33)
    zustand.punkte_add(z, MODUL, "vertrauen.rosi", 6, deckel=zustand.GESPRAECH_DECKEL, quelle="szenen")
    assert zustand.punkte(z, "vertrauen.rosi") == 35
    assert zustand.punkte_add(z, MODUL, "vertrauen.rosi", 6, deckel=zustand.GESPRAECH_DECKEL, quelle="szenen") == []
    zustand.punkte_add(z, MODUL, "vertrauen.rosi", 8, frei=True)
    zustand.punkte_add(z, MODUL, "vertrauen.rosi", 4, deckel=zustand.GESPRAECH_DECKEL, quelle="szenen")
    assert zustand.punkte(z, "vertrauen.rosi") == 47


def test_minus_gibt_nichts_frei():
    z = stand(40)
    zustand.punkte_add(z, MODUL, "vertrauen.rosi", 10, quelle="geschenke", frei=True)
    zustand.punkte_add(z, MODUL, "vertrauen.rosi", -8)
    assert zustand.topf_platz(z, MODUL, "vertrauen.rosi", "geschenke") == 0


def test_sprung_zaehlt_wird_aber_nicht_begrenzt():
    z = stand(0)
    z.setdefault("topf", {})["vertrauen.rosi"] = {"events": 45}
    zustand.punkte_add(z, MODUL, "vertrauen.rosi", 36, roh=True)
    assert zustand.punkte(z, "vertrauen.rosi") == 36


def test_nebenfigur_ohne_topf():
    assert zustand.topf_platz({"topf": {}}, MODUL, "vertrauen.maxwell", "szenen") is None


if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"):
            f()
            print("ok", n)
