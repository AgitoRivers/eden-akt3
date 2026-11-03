# -*- coding: utf-8 -*-
"""Album (Duc 31.10.2026): Selfies und Leiter-Szenen werden gemerkt, nur der erste Moment zaehlt, Favours bleiben draussen."""
import json, os, re, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HIER))
sys.stdout.reconfigure(encoding="utf-8")
from kern import album  # noqa: E402

MOD = os.path.join(os.path.dirname(HIER), "module", "eden_rise")


def main():
    modul = {"personen": {"rosi": {"name": "Rosi Scuderi"}, "lea": {"name": "Lea Moore"}}}
    z = {"modul": "eden_rise", "tag": 4, "chronik": [
        {"moment": "kiss", "wer": ["rosi"], "tag": 2}, {"moment": "kiss", "wer": ["rosi"], "tag": 3},
        {"moment": "fight", "wer": ["rosi"], "tag": 3}]}
    album.merken(z, {"id": "rm_r1", "titel": "Nothing's Broken", "personen": {}})
    album.merken(z, {"id": "rm_r1_b", "titel": "Nothing's Broken", "personen": {}})
    album.merken(z, {"id": "rm_l3", "titel": "Sweet", "personen": {}})      # spielt mit Sophia
    album.merken(z, {"id": "gv_keks", "titel": "Cookie", "personen": {}})
    album.merken(z, {"id": "fv_x_1", "titel": "Favour", "personen": {"favour": {"foto": "x"}}})
    album.merken(z, {"id": "sf_rosi_3_x", "titel": "Grease", "personen": {"selfie": {"frau": "rosi", "stufe": 3}}}, "rosi_x_1")
    a = album.ansicht(z, modul)
    assert [p["id"] for p in a] == ["rosi"], a
    e = a[0]["eintraege"]
    assert [x["art"] for x in e] == ["kiss", "szene", "selfie"], e
    assert e[0]["tag"] == 2 and e[0]["notiz"], e[0]
    assert e[1]["notiz"] and e[2]["notiz"] and e[2]["bild"] == "/selfie/rosi_x_1.webp", e

    # Alte Spielstaende ohne Album-Liste laufen weiter
    assert album.ansicht({"modul": "eden_rise", "tag": 1}, modul) == []

    # Jede Leiter-Szene im Spiel hat eine Notiz, und jede Selfie-Stufe auch
    ev = json.load(open(os.path.join(MOD, "ereignisse.json"), encoding="utf-8"))["events"]
    d = album.daten("eden_rise")
    for x in ev:
        t = re.fullmatch(r"rm_([a-z])(\d)", x["id"])
        if t and x["id"] not in d["ohne"]:
            n = d["notizen"][d["leiter"][t.group(1)]]
            assert n["szene"].get(t.group(2)), x["id"]
        s = x["personen"].get("selfie") if isinstance(x.get("personen"), dict) else None
        if s and s.get("stufe") and s["frau"] in d["notizen"]:
            assert d["notizen"][s["frau"]]["selfie"].get(str(s["stufe"])), x["id"]
    print("test_album ok")


if __name__ == "__main__":
    main()
