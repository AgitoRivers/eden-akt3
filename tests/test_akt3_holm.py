# -*- coding: utf-8 -*-
"""Duc 05.11.2026 (E-132): Holm ist in Akt 3 immer zurueck; die Probefahrt gibt es mit Rosi oder mit Petru."""
import json, os, sys
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
from kern import akt3

z = {"tag": 24, "flags": ["akt2_ende"]}
akt3.morgen(z)
assert "holm_zurueck" in z["flags"], "Holm muss ab Tag 24 zurueck sein"
z2 = {"tag": 20, "flags": []}
akt3.morgen(z2)
assert "holm_zurueck" not in z2["flags"], "vor Akt 3 nichts setzen"

ev = json.load(open(os.path.join(BASE, "module", "eden_rise", "ereignisse.json"), encoding="utf-8"))
ev = ev["events"]
ids = {e["id"]: e for e in ev} if isinstance(ev, list) else ev
for eid, mit in (("a3_probefahrt", "rosi"), ("a3_probefahrt_petru", "petru")):
    assert eid in ids, eid
    assert mit in json.dumps(ids[eid], ensure_ascii=False), (eid, mit)
assert "gefeuert_rosi" in json.dumps(ids["a3_probefahrt_petru"]), "Petru-Fassung nur ohne Rosi"
print("ok test_akt3_holm")
