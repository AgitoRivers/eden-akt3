# -*- coding: utf-8 -*-
"""F-37 und F-38 (Duc 05.11.2026): Funken an den Tagen und in der Phase aus dem Wiki (beziehungen.md);
Auftrag "Funk" wirkt in Welle 3 (Holm hoert die Fackeln eine Runde frueher, Nachschub eine Runde spaeter)."""
import json, os, sys
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
from kern import taktik

M = os.path.join(BASE, "module", "eden_rise")
ev = {e["id"]: e for e in json.load(open(os.path.join(M, "ereignisse.json"), encoding="utf-8"))["events"]}
WIKI = {"fk_chiara_frage": "nacht", "fk_sophia_wette": "abend", "fk_lea_schulter": "nacht", "fk_rosi_schicht": "nacht", "fk_siri_foto": "abend"}
for eid, ph in WIKI.items():
    w = ev[eid]["wann"]
    assert w["tage"] == [4, 6] and w["phasen"] == [ph], (eid, w["tage"], w["phasen"])

D = json.load(open(os.path.join(M, "taktik.json"), encoding="utf-8"))
assert any(b["szene"] == "w3_funk" and b.get("bed") == {"t": "funk_warnt"} for b in D["wellen"][2]["beats"])
assert "w3_funk" in D["szenen"]
assert taktik._funk_warnt({"flags": ["bl_funk_white"]}) and taktik._funk_warnt({"flags": ["bl_funk_charly"]})
assert not taktik._funk_warnt({"flags": []})
t = {"welle": 3, "art": "echt"}
ohne = [n["runde"] for n in taktik._nachschub_liste(D, t)]
mit = [n["runde"] for n in taktik._nachschub_liste(D, dict(t, funk_warnt=True))]
assert mit == [r + 1 for r in ohne], (ohne, mit)
assert [n["runde"] for n in taktik._nachschub_liste(D, {"welle": 2, "art": "echt", "funk_warnt": True})] == \
       [n["runde"] for n in taktik._nachschub_liste(D, {"welle": 2, "art": "echt"})], "nur Welle 3"
print("ok test_f37_f38")
