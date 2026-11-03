# -*- coding: utf-8 -*-
"""Bibis Tierstation (Duc 31.10.2026, Wiki systeme/tierstation.md): Status, Koeder, Rettung, Tor, Begleiter, Fund. Aufruf: python tests/test_mochis.py"""
import json, os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HIER))
sys.stdout.reconfigure(encoding="utf-8")
from kern import buehne, kampf, mochis, regeln  # noqa: E402

MOD = os.path.join(os.path.dirname(HIER), "module", "eden_rise")
MODUL = json.load(open(os.path.join(MOD, "modul.json"), encoding="utf-8"))
MODUL.setdefault("_kuechen", None)


def stand(tag=15):
    return {"id": "test", "tag": tag, "phase": "tag", "status": "wahl", "konto": 100, "flags": ["mochis_offen", "rt_ausgang_alle", "rt_ende_tag"], "flag_tag": {"rt_ende_tag": 11},
            "meldungen": [], "buchungen": [], "werte": {"vertrauen.bibi": 0, "ruf": 0}, "kueche": {"vorrat": {"pork|1": 2}, "rohstoffe": {}}}


def test_spur_und_koeder():
    z = stand()
    a = mochis.ansicht(z, MODUL)
    assert next(k for k in a["karten"] if k["id"] == "hyaene")["status"] == "spur"
    assert next(k for k in a["karten"] if k["id"] == "wolf")["status"] == "nicht_da"       # Spur erst 7 Tage nach dem Quest-Ende
    assert next(k for k in mochis.ansicht(dict(z, tag=18), MODUL)["karten"] if k["id"] == "wolf")["status"] == "spur"
    assert mochis.spur_start(z, MODUL, "hyaene", False) == "mo_hyaene_spur"
    try:
        mochis.spur_start(z, MODUL, "hyaene", False)
        raise AssertionError("zweite Spur am selben Tag")
    except ValueError:
        pass
    z["tag"] += 1
    mochis.spur_start(z, MODUL, "hyaene", True)
    assert z["kueche"]["vorrat"]["pork|1"] == 1 and z["mochis"]["koeder"] == "hyaene"


def _gerettet(z, tid):
    assert mochis.kampf_ende(z, MODUL, {"definition": "mochis_" + tid}, "aufgabe") is not None
    assert tid in z["mochis"]["tiere"]


def test_nur_die_granate_rettet():
    z = stand()
    for art in ("ko", "entkommen", "niederlage", "flucht"):
        mochis.kampf_ende(z, MODUL, {"definition": "mochis_hund"}, art)
    assert "hund" not in (z.get("mochis") or {}).get("tiere", {})
    _gerettet(z, "hund")
    assert z["mochis"]["halsbaender"] == 1                 # jedes Tier traegt ein Halsband (Duc 01.11.2026)


def test_schlaf_chance():
    w = {"schlaf": {"sicher": 0.10, "boden": 0.05}}
    g = lambda lp, f=1: {"lp": lp, "lp_max": 100, "def": {"schlaf_faktor": f}}
    assert kampf.schlaf_chance(g(10), w) == 1.0 and kampf.schlaf_chance(g(5, 0.7), w) == 1.0
    assert 1.0 > kampf.schlaf_chance(g(11), w) > kampf.schlaf_chance(g(50), w) > kampf.schlaf_chance(g(100), w) == 0.05
    assert kampf.schlaf_chance(g(30, 0.7), w) < kampf.schlaf_chance(g(30), w)


def test_restliche_granaten_gehen_zurueck():
    z = dict(stand(), inventar=["grenade_sleep", "plaster", "grenade_sleep"])
    mochis.kampf_ende(z, MODUL, {"definition": "mochis_hund"}, "flucht")
    assert z["inventar"] == ["plaster"]


def test_besuch():
    z = stand()
    _gerettet(z, "hund")
    z["mochis"]["tiere"]["hund"]["gesund_ab"] = z["tag"]
    mochis.besuchen(z, MODUL, "hund")
    mochis.besuchen(z, MODUL, "hund")
    x = z["mochis"]["tiere"]["hund"]
    assert x["besuche"] == 2 and x["kaempfe"] == 1         # Bindung nur einmal am Tag


def test_drei_halsbaender():
    z = stand()
    for tid in ("hyaene", "mufflon", "affe"):
        _gerettet(z, tid)
    assert z["mochis"]["halsbaender"] == 3 and "mo_halsband_3" in z["flags"]


def test_bild_waechst_mit():
    z = stand()
    assert mochis.bild(z, MODUL) == MODUL["mochis"]["bild_anfang"]
    for tid in list(MODUL["mochis"]["tiere"])[:MODUL["mochis"]["ausbau_ab"]]:
        _gerettet(z, tid)
    assert mochis.bild(z, MODUL) == MODUL["mochis"]["bild_voll"]


def test_beweis_stand():
    z = stand()
    assert mochis.beweis_stand(z) == "keiner"
    z["flags"].append("mo_ark_beweis")
    assert mochis.beweis_stand(z) == "fraglich"
    z["flags"].append("mo_beweis_bei_elsa")
    assert mochis.beweis_stand(z) == "sicher"


def test_epilog_nur_gerettete():
    """Der Epilog geht nur durch die geretteten Tiere, in fester Reihenfolge, und endet immer im Schluss-Frame."""
    ev = {e["id"]: e for e in json.load(open(os.path.join(MOD, "ereignisse.json"), encoding="utf-8"))["events"]}
    z = stand()
    _gerettet(z, "wolf")
    _gerettet(z, "waran")
    assert "mo_tier_da" in z["flags"] and "mo_tier_wolf" in z["flags"]
    ziel = lambda folgen, schluessel: next(x["id"] for f in folgen if schluessel in f for x in f[schluessel] if not x.get("wenn") or regeln.gilt(x["wenn"], z))
    weg = [ziel(ev["mo_frei_start"]["optionen"][0]["folgen"], "direkt")]
    while weg[-1] != "mo_frei_ende":
        weg.append(ziel(ev[weg[-1]]["optionen"][0]["folgen"], "weiter"))
    assert weg == ["mo_frei_wolf", "mo_frei_waran", "mo_frei_ende"]
    assert ev["mo_frei_wolf"]["tier_bild"] == "/kampfbild/WolfFrei/idle.webp"


def test_fang_stufen():
    """Erster Fang = Overlay, zweiter = Handy mit Gesellschaft und Fakt 2, mehr gibt es nicht."""
    z = stand()
    _gerettet(z, "geier")
    assert z["mochis_brief"] == {"tier": "geier"} and "mo_fang_heute" in z["flags"] and not z.get("handy")
    z["mochis"]["tiere"]["geier"]["gesund_ab"] = z["tag"]
    karte = lambda: next(k for k in mochis.ansicht(z, MODUL)["karten"] if k["id"] == "geier")
    assert karte()["fakten"] == [MODUL["mochis"]["tiere"]["geier"]["fakt"]] and karte()["fakt_fehlt"] == "zweites"
    z.pop("mochis_brief")
    mochis.kampf_ende(z, MODUL, {"definition": "mochis_geier"}, "aufgabe")
    assert "mochis_brief" not in z and z["mochis"]["tiere"]["geier"]["anzahl"] == 2 and z["mochis"]["halsbaender"] == 2
    assert [v["text"] for v in z["handy"][-1]["verlauf"]] == MODUL["mochis"]["tiere"]["geier"]["zweit"]
    assert len(karte()["fakten"]) == 2 and karte()["fakt_fehlt"] is None
    z["tag"] += 30
    assert "wieder" not in karte()                         # nach dem zweiten Tier kommt keine Spur mehr
    try:
        mochis.spur_start(z, MODUL, "geier", False)
        raise AssertionError("dritte Spur")
    except ValueError:
        pass


def test_spur_kommt_wieder():
    z = stand()
    _gerettet(z, "hund")
    z["mochis"]["tiere"]["hund"]["gesund_ab"] = z["tag"]
    karte = lambda: next(k for k in mochis.ansicht(z, MODUL)["karten"] if k["id"] == "hund")
    assert "wieder" not in karte()
    z["tag"] += MODUL["mochis"]["wieder_tage"]
    assert karte()["wieder"]["geht"]
    assert mochis.spur_start(z, MODUL, "hund", False) == "mo_hund_wieder"
    assert "mo_fang_heute" not in z["flags"] and not karte()["wieder"]["geht"]


def test_einzelgaenger():
    """Madame, Duchess, Sunday, Rusty und Ghost bleiben allein: keine zweite Spur, der zweite Fakt kommt mit dem ersten Besuch."""
    z = stand()
    _gerettet(z, "madame")
    z["mochis"]["tiere"]["madame"]["gesund_ab"] = z["tag"]
    z["tag"] += 30
    karte = lambda: next(k for k in mochis.ansicht(z, MODUL)["karten"] if k["id"] == "madame")
    assert "wieder" not in karte() and karte()["fakt_fehlt"] == "besuch" and len(karte()["fakten"]) == 1
    assert any("Field Book" in x for x in mochis.besuchen(z, MODUL, "madame"))
    assert karte()["fakt_fehlt"] is None and len(karte()["fakten"]) == 2


def test_zweites_tier_findet_mit():
    z = stand()
    _gerettet(z, "hund")
    z["mochis"]["tiere"]["hund"].update(gesund_ab=z["tag"], anzahl=2)
    assert len(mochis.einsammeln(z, MODUL)) == 2


def test_alle_tiere_vollstaendig():
    ev = {e["id"] for e in json.load(open(os.path.join(MOD, "ereignisse.json"), encoding="utf-8"))["events"]}
    allein = {tid for tid, t in MODUL["mochis"]["tiere"].items() if t.get("allein")}
    assert allein == {"madame", "mufflon", "wolf", "rotpanda", "schneeleopard"}
    for tid, t in MODUL["mochis"]["tiere"].items():
        assert t["zeilen"] and t["fakt"] and t["fakt2"] and t["szene"], tid
        assert bool(t.get("zweit")) != (tid in allein) and ("mo_%s_wieder" % tid in ev) != (tid in allein), tid
        assert {"mo_%s_spur" % tid, "mo_%s_weg" % tid} <= ev and "mo_%s_ruhig" % tid not in ev, tid
        assert mochis.zeile(MODUL, "mochis.%s.0" % tid)[1] == t["zeilen"][0][1]
    assert mochis.zeile(MODUL, "mochis.hund.99") == (None, None)


def test_selfie_szene():
    """Bibis Selfie je Tier ist eine Mini-Szene (Duc 02.11.2026): zwei Bilder A, B mit Polaroid-Titel, dazu Nachricht und Field-Book-Notiz."""
    z = stand()
    z["mochis"] = {"tiere": {"hund": {"seit": 15}}}
    for tid, t in MODUL["mochis"]["tiere"].items():
        assert len(t.get("selfie_titel") or []) == 2 and all(t["selfie_titel"]) and t.get("log"), tid
        for teil in "ab":
            assert os.path.isfile(os.path.join(MOD, "selfies", "bibi_fang_%s_%s.webp" % (tid, teil))), (tid, teil)
    s = next(k for k in mochis.ansicht(z, MODUL)["karten"] if k["id"] == "hund")["selfie"]
    assert [b["bild"] for b in s["bilder"]] == ["/selfie/bibi_fang_hund_a.webp", "/selfie/bibi_fang_hund_b.webp"]
    assert s["bilder"][0]["titel"] == MODUL["mochis"]["tiere"]["hund"]["selfie_titel"][0] and s["log"] and s["text"]


def test_outfit_der_leiterin():
    """Bibi traegt ab mochis_offen das Set Mochis, in freien Szenen und in jedem Event der Station. Vorher und ohne Station bleibt bibi_A."""
    assert buehne.set_waehlen({"st_daten": ""}, MODUL, "bibi", {"ort": "mochis"}, "tag", None, {"flags": []}) == "bibi_A"
    assert buehne.set_waehlen({"st_daten": ""}, MODUL, "bibi", {"ort": "mochis"}, "tag", None, {"flags": ["mochis_offen"]}) == "Mochis"
    assert mochis.FANG_SET["bibi"] == "Mochis"
    assert json.load(open(os.path.join(MOD, "laeden.json"), encoding="utf-8"))["laeden"]["mochis"]["set"] == "Mochis"
    for e in json.load(open(os.path.join(MOD, "ereignisse.json"), encoding="utf-8"))["events"]:
        if "bibi" not in e.get("sets", {}):
            continue
        station = e["id"].startswith("mo_") or "mochis_offen" in json.dumps(e.get("wann", ""))
        assert e["sets"]["bibi"] == ("Mochis" if station else "bibi_A"), e["id"]


if __name__ == "__main__":
    for name, f in list(globals().items()):
        if name.startswith("test_"):
            f()
            print("ok", name)
