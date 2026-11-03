# -*- coding: utf-8 -*-
r"""Kampf-Gegner: Variante Unit-01 in Weiss-Beige, angelaufen (19.10.2026, Duc).
Kopie von Kampf_Unit1 (gleiche Form, gleicher Sprite-Prompt), eigene Merkmal-Karte kampf_unit1white,
Kostuem-Preset Kampf_Unit1White|Kampf, Ausgabe combat/Unit1White. Keine Gitter: alles wird positiv beschrieben
(Krea laeuft mit CFG 1, der Negativ-Prompt wirkt nicht).

    kampf_unit1_weiss.py          Probelauf
    kampf_unit1_weiss.py --los    traegt ein (Merkmal-Karte ueber die Studio-API, Presets per DucCommon)
"""
import copy, io, json, os, sys, time, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, r"X:\AI\DucCommon")
import duc_common as dc  # noqa: E402

LOS = "--los" in sys.argv
PS = "http://127.0.0.1:8301"
F_PRESETS, F_SETS = r"X:\AI\PromptStudio\presets.json", r"X:\AI\PromptStudio\set_presets.json"
EXPR = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions"
KARTE = "kampf_unit1white"
MERKMAL = ("a boxy dented off-white and beige painted steel cabinet body, the paint weathered and tarnished with "
           "yellowed edges, grime streaks and faint rust stains, every side smooth flat painted sheet metal with big "
           "rivets, a broad faded yellow-and-black hazard stripe band around the middle, a riveted hatch with a chunky "
           "handle, a red fire extinguisher strapped to its back, two thick hydraulic legs in the same weathered "
           "off-white, two exhaust pipes on top belching black smoke, loose sparking cables hanging like arms, one round "
           "red warning light as its single eye, black stencil letters UNIT-01 on its side")


def ps(pfad, daten=None):
    req = urllib.request.Request(PS + pfad, data=None if daten is None else json.dumps(daten).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


presets, sets = dc.load_json(F_PRESETS, None, "Studio"), dc.load_json(F_SETS, None, "Studio")
print("Merkmal:", MERKMAL)
if not LOS:
    sys.exit("PROBELAUF")
p = copy.deepcopy(presets["Kampf_Unit1"])
p.update({"st_set": "combat/Unit1White", "sp_char": "Kampf_Unit1White", "sp_stchar": "Unit1White",
          "st_src": os.path.join(EXPR, "combat", "Unit1White"), "st_dst": os.path.join(EXPR, "combat", "Unit1White"),
          "cards_on": {"outfit": [KARTE], "setting": ["A Sprite Background"]},
          "created": time.strftime("%Y-%m-%d %H:%M"), "updated": time.strftime("%Y-%m-%d %H:%M")})
presets["Kampf_Unit1White"] = p
s = copy.deepcopy(sets["Kampf_Unit1|Kampf"])
s["outfit"] = [KARTE]
sets["Kampf_Unit1White|Kampf"] = s
d = ps("/api/state")["decks"]
alt = next((c for c in d["outfit"] if c["name"] == KARTE), None)
if alt:
    alt["prompt"] = MERKMAL
else:
    d["outfit"].append({"name": KARTE, "prompt": MERKMAL, "on": True, "tag": "kampf", "sel": False, "back_prompt": ""})
ps("/api/decks", d)
dc.save_json(F_PRESETS, presets, "Studio")
dc.save_json(F_SETS, sets, "Studio")
print("eingetragen: Kampf_Unit1White")
