# -*- coding: utf-8 -*-
"""Late-Game-Paket (Duc 05.11.2026, docs/brain_trust/LATE_GAME.md): Warnung an Tag 31, Kommission als Echo der Anhoerung,
Baustoff-Hinweise ohne Laden, Enden im Titelbild."""
import json, os, sys
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
from kern import aufbau, kommission, regeln

M = os.path.join(BASE, "module", "eden_rise")
ev = {e["id"]: e for e in json.load(open(os.path.join(M, "ereignisse.json"), encoding="utf-8"))["events"]}

# 1) Warnung: Tag 31 Nacht, Pflicht; Holm nennt offene Romanzen, sonst die Zeile "keiner"
w = ev["a3_zwei_tage"]
assert w["wann"]["tage"] == [31, 31] and w["wann"]["phasen"] == ["nacht"] and w["wann"]["pflicht"]
def sichtbar(z):
    return [x.get("gruppe") for x in w["zeilen"] if x.get("wenn") is None or regeln.gilt(x["wenn"], z)]
leer = sichtbar({"flags": ["akt2_ende"], "tag": 31})
assert "keiner" in leer and not any(g and g.startswith("offen_") for g in leer), leer
mit = sichtbar({"flags": ["akt2_ende", "rm_c4"], "tag": 31})
assert "offen_chiara" in mit and "keiner" not in mit, mit
fertig = sichtbar({"flags": ["akt2_ende", "rm_c4", "a3_schluss_chiara"], "tag": 31})
assert "offen_chiara" not in fertig and "keiner" in fertig, fertig

# 2) Kommission: Megan erinnert an die Anhoerung, gleich am Anfang
d = kommission.daten(M)
z = {"flags": []}
kommission.beginnen(z, d)
assert any(e["wer"] == "megan" and "hearing" in e["text"] for e in z["kommission"]["log"][:4])

# 3) Baustoffe: jeder Stoff hat einen Fundort, keiner nennt einen Laden
for roh in {k for st in aufbau.STUFEN.values() for s in st for k in s}:
    assert aufbau.WO.get(roh), roh
    assert "shop" not in aufbau.WO[roh].lower() and "buy" not in aufbau.WO[roh].lower(), roh
# 5) Megan warnt selbst an Tag 29 Nacht (ihre Karte endet an Tag 30); Romanzen-Leiter enden in Akt 3 an Tag 33
m = ev["a3_megan_tuer"]["wann"]
assert m["tage"] == [29, 29] and m["phasen"] == ["nacht"] and "megan_funke" in json.dumps(m["bedingung"])
for e in ev.values():
    w = e.get("wann") or {}
    if w.get("leiter") and w.get("akt2"):
        assert w["akt2"][1] <= 33, e["id"]
# Bibis Handgriffe an der Station enden an Tag 33 (kein Handgriff am Villa- oder Kommissionstag)
for eid in ("mo_a_zaun", "mo_a_dach", "mo_schlafgranate"):
    assert ev[eid]["wann"]["tage"][1] <= 33, eid
print("ok test_akt3_spaet")
