# -*- coding: utf-8 -*-
"""Go somewhere private und Abstand fuer Dates (Duc 02.11.2026)."""
import json, os, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
from kern import gesten, szene

MODUL = json.load(open(os.path.join(BASE, "module", "eden_rise", "modul.json"), encoding="utf-8"))
G = gesten.gesten(MODUL)


def test_geste_da():
    g = G["privat_gehen"]
    assert g["art"] == "gross" and g["schwelle"] == {"vertrauen": 3, "begehren": 3} and not g.get("privat")


def test_gesperrt():
    z = {"werte": {"vertrauen.chiara": 3, "begehren.chiara": 3}, "tag": 5, "flags": []}
    allein = {"figuren": ["chiara"], "def": {"ort": "main_salon"}}
    assert gesten.gesperrt(z, MODUL, allein, G["privat_gehen"], "chiara") is None
    assert "alone" in gesten.gesperrt(z, MODUL, {"figuren": ["chiara", "lea"], "def": {"ort": "main_salon"}}, G["privat_gehen"], "chiara")
    assert "already" in gesten.gesperrt(z, MODUL, {"figuren": ["chiara"], "def": {"ort": "duc_cabin"}}, G["privat_gehen"], "chiara")


def test_raum_wechsel():
    sz = {"def": {"ort": "main_salon"}, "log": [], "figuren": ["chiara"]}
    gesten.raum_wechseln({"phase": "abend"}, MODUL, sz, "duc_cabin", "x")
    assert sz["def"]["ort"] == "duc_cabin" and sz["bild"].startswith("/bg/") and sz["log"][-1]["art"] == "ereignis"


def test_dates_halten_abstand():
    assert not szene.story_frei({"id": "date_chiara_t3"}) and not szene.story_frei({"id": "frei_rosi_t2_tag"})
    assert not szene.story_frei({"id": "x", "art": "intim"}) and szene.story_frei({"id": "rm_e_rosi_1"})


if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"):
            f()
            print("ok", n)
