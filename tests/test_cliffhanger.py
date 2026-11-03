# -*- coding: utf-8 -*-
"""Cliffhanger Ende Akt 2 (Duc 02.11.2026): Kette nach dem Bericht, Siris Variante, Schlusskarte der Beta."""
import json, os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HIER))
sys.stdout.reconfigure(encoding="utf-8")
from kern import abschluss  # noqa: E402

MOD = os.path.join(os.path.dirname(HIER), "module", "eden_rise")
EV = {e["id"]: e for e in json.load(open(os.path.join(MOD, "ereignisse.json"), encoding="utf-8"))["events"]}


def main():
    start = EV["bl_cliff_netz"]
    assert start["wann"]["tage"] == [23, 23] and start["wann"]["phasen"] == ["nacht"] and start["wann"].get("pflicht"), start["wann"]
    assert "belagerung_bericht" in json.dumps(start["wann"]["bedingung"])
    ziel = start["optionen"][0]["folgen"][-1]["direkt"]
    assert ziel[0] == {"wenn": {"flag": "siri_darf_posten"}, "id": "bl_cliff_alon_siri"} and ziel[1]["id"] == "bl_cliff_alon", ziel
    texte = lambda eid: " ".join(z["text"] for z in EV[eid]["zeilen"])
    assert "anyone can make a video" in texte("bl_cliff_alon_siri") and "anyone can make a video" not in texte("bl_cliff_alon")
    assert "Welcome to the team" in texte("bl_cliff_team")
    # Alon spricht selbst auf seiner Buehne, die Reaktionen kommen auf dem Kirchplatz
    for eid in ("bl_cliff_alon", "bl_cliff_alon_siri", "bl_cliff_team"):
        assert EV[eid]["bild"] == "alon_keynote" and EV[eid]["sets"] == {"alon": "alon_standard"}, eid
        assert all(z["wer"] == "alon" for z in EV[eid]["zeilen"]), eid
    siri = [z for z in EV["bl_cliff_platz"]["zeilen"] if z["wer"] == "siri"]
    assert siri and siri[0]["wenn"] == {"flag": "siri_darf_posten"}, siri
    assert {"flag": "akt2_ende"} in EV["bl_cliff_megan"]["optionen"][0]["folgen"]
    # Schlusskarte: nur nach dem Cliffhanger, ohne Fall und ohne Frauen, mit dem Dank an die Tester
    k = abschluss.berechnen({"flags": ["akt2_ende"]}, {})
    assert k["titel"] == "End of Act 2" and k["fall"] is None and k["frauen"] == []
    assert any("Beta release" in a["text"] for a in k["absaetze"])
    print("test_cliffhanger ok")


if __name__ == "__main__":
    main()
