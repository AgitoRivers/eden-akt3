# -*- coding: utf-8 -*-
r"""Elsas Ruestung C als Kostuem im Prompt Studio (Duc 01.11.2026: C2 mit Tags ablegen, er optimiert selbst). Preset Yacht_Elsa bleibt, dazu Karte elsa_ruestung_c und Set "Yacht_Elsa|Ruestung C"."""
import json, os, sys, urllib.request

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, r"X:\AI\DucCommon")
import casting_elsa_ruestung as ce  # noqa: E402
import duc_common as dc  # noqa: E402

F_SETS = r"X:\AI\PromptStudio\set_presets.json"
KARTE, SET = "elsa_ruestung_c", "Yacht_Elsa|Ruestung C"
TAGS = ["Color: Honey blonde", "Style: Bun", "View: Front"]


def ps(pfad, daten=None):
    req = urllib.request.Request(ce.PS + pfad, data=None if daten is None else json.dumps(daten).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


st = ps("/api/state")
vorhanden = {t["name"] for t in st["cfg"]["tags"]}
assert all(t in vorhanden for t in TAGS)
text = ce.VARIANTEN["c"][1]
d = st["decks"]
assert not any(c["name"] == KARTE for c in d["outfit"]), "Karte gibt es schon"
d["outfit"].append({"name": KARTE, "prompt": text, "on": True, "tag": "eden_dorf", "sel": False, "back_prompt": text + ", seen from behind"})
ps("/api/decks", d)
sets = dc.load_json(F_SETS, None, "Studio")
sets[SET] = {"outfit": [KARTE], "setting": ["A Sprite Background"], "tags": TAGS}
dc.save_json(F_SETS, sets, "Studio")
print("angelegt:", SET, "|", KARTE)
print(text)
print("Tags:", TAGS, "Seed C2:", ce.SEEDS[0])
