# -*- coding: utf-8 -*-
"""Orte fuer Zweisamkeit (Duc 02.11.2026): Wahl, eigener Ort, Risiko, Vorschlag."""
import json, os, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
from kern import figurenrahmen, gesten, orte

MODUL = json.load(open(os.path.join(BASE, "module", "eden_rise", "modul.json"), encoding="utf-8"))
MODUL["figurenrahmen"] = json.load(open(os.path.join(BASE, "module", "eden_rise", "figurenrahmen.json"), encoding="utf-8"))


def z(v=4, b=3, phase="nacht", flags=()):
    return {"id": "t", "tag": 9, "phase": phase, "flags": list(flags), "werte": {"vertrauen.chiara": v, "begehren.chiara": b,
            "vertrauen.rosi": v, "begehren.rosi": b}, "punkte": {}, "chronik": [], "persona": {"id": "first_officer", "attribute": {}},
            "inventar": [], "truhe": []}


def test_daten_passen_zu_raeumen_und_texten():
    o = MODUL["orte"]
    for ort in o["risiko"]:
        assert 0 <= o["risiko"][ort].get("*", 0) <= 3
    for pid, e in o["eigen"].items():
        assert MODUL["personen"][pid]["romanzierbar"] or pid == "bibi", pid
        assert figurenrahmen.figur(MODUL, pid).get("ort_vorschlag"), pid


def test_eigener_ort_ab_vertrauen_4_und_tageszeit():
    assert orte.eigen(z(4), MODUL, "chiara") == "bridge"
    assert orte.eigen(z(3), MODUL, "chiara") is None
    assert orte.eigen(z(4, phase="tag"), MODUL, "chiara") is None
    assert orte.eigen(z(4), MODUL, "lea") is None          # Tenderboot: noch kein Bild, also kein Raum


def test_wahl_und_bonus():
    sz = {"def": {"ort": "main_salon"}, "figuren": ["chiara"], "log": []}
    w = orte.wahl(z(4), MODUL, sz, "chiara")
    ids = [o["id"] for o in w]
    assert ids[0] == "bridge" and "duc_cabin" in ids and "vip_cabin" not in ids
    assert orte.bonus(z(4), MODUL, sz, "chiara", "bridge") == [("Her place", orte.EIGEN_BONUS)]
    sz["ort_vorschlag"] = {"chiara": "bridge"}
    assert orte.bonus(z(4), MODUL, sz, "chiara", "bridge")[0][1] == orte.VORSCHLAG_BONUS


def test_ihr_zimmer():
    from kern import orte as O
    assert O.zimmer(z(4), MODUL, "sophia") == "crew_kabine_1"
    assert O.zimmer(z(4, flags=["kabine_sophia"]), MODUL, "sophia") == "spare_cabin"
    assert O.zimmer(z(4), MODUL, "bibi") is None and O.zimmer(z(4, flags=["mochis_offen"]), MODUL, "bibi") == "bibi_haeuschen"
    sz = {"def": {"ort": "main_salon"}, "figuren": ["chiara"], "log": []}
    assert any(o["id"] == "crew_kabine_3" and o["zimmer"] for o in O.wahl(z(4), MODUL, sz, "chiara"))
    assert all(not r.get("versteckt") or r["bild"] for r in MODUL["raeume"].values())


def test_gewaehlter_ort_ist_privat_bis_peinlich():
    sz = {"def": {"ort": "sun_deck"}, "figuren": ["chiara"], "privat_stufe": orte.PRIVAT_STUFE}
    assert gesten.privat(MODUL, sz, "chiara")
    sz["intim_gesperrt"] = True
    assert not gesten.privat(MODUL, sz, "chiara")


def test_ankommen_ohne_risiko_und_erster_besuch():
    zz, sz, zeilen = z(4), {"def": {"ort": "bridge"}, "figuren": ["chiara"], "log": []}, []
    orte.ankommen(zz, MODUL, sz, "chiara", "duc_cabin", lambda p, t, g: zeilen.append(t))
    assert not zeilen and not sz.get("erwischt")
    orte.ankommen(zz, MODUL, sz, "chiara", "bridge", lambda p, t, g: zeilen.append(t))
    assert "ort_besucht_chiara" in zz["flags"] and zeilen


def test_risiko_erwischt_irgendwann():
    folgen = set()
    for tag in range(1, 80):
        zz, sz = z(4), {"def": {"ort": "galley"}, "figuren": ["chiara"], "log": []}
        zz["tag"] = tag
        orte.ankommen(zz, MODUL, sz, "chiara", "kuehlraum" if "kuehlraum" in MODUL["raeume"] else "galley", lambda p, t, g: None)
        folgen.update(sz.get("erwischt") or [])
    assert folgen, "bei Risiko 3 muss in 80 Tagen jemand hereinplatzen"


if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"):
            f()
            print("ok", n)
