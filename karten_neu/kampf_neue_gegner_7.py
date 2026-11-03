# -*- coding: utf-8 -*-
r"""BearCub (Story-Auftrag Ortskapitel Berge, 27.10.2026): junger Braunbaer mit blinkendem rotem Halsband. Gebraucht
vor allem flee, dazu idle, hurt und avatar. Aufbau wie kampf_neue_gegner_6.py.
Dazu Sergent Kaspar Wolff (Fremdenlegion) mit Legionsmesser, Gesicht wie Yacht_Wolff (Casting A, Duc 27.10.).

    kampf_neue_gegner_7.py          Probelauf
    kampf_neue_gegner_7.py --los    Karte ueber die Studio-API, Preset/Set-Preset per DucCommon
"""
import json, os, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))   # stdout is set to UTF-8 by studio_kampf_gegner on import
sys.path.insert(0, HERE)
GO = "--los" in sys.argv
sys.argv = [sys.argv[0]]
import studio_kampf_gegner as sk  # noqa: E402
import duc_common as dc  # noqa: E402

PS = "http://127.0.0.1:8301"
# key: (kind, subject, tags, look, format, loras or None = default)
from kampf_alphas import ZOO_COLLAR as COLLAR  # noqa: E402
NEW = {
    # Ortskapitel Berge (Story-Auftrag 27.10.2026): junger Braunbaer mit dem roten Halsband, flieht vor allem
    "BearCub": ("wesen", "a young brown bear cub", "",
                "fluffy dark brown fur, round ears, a small light muzzle, big round dark eyes, clumsy oversized paws, "
                "scared and wary, not dangerous, " + COLLAR, "quer", None),
    "Wolff": ("mann", "Sergent Kaspar Wolff, a 48-year-old soldier of the French Foreign Legion, an angular weathered "
              "face with deep lines, short shaved grey hair, a thick grey moustache, narrow steel-grey eyes, a strong "
              "jaw", ["M Body: Lean"],
              "a green camouflage combat uniform of the French Foreign Legion, sleeves neatly rolled, a small "
              "blue-white-red French flag patch on the upper sleeve, a green beret pulled low over his brow, a black "
              "radio clipped to his chest, a webbing belt, black combat boots, his only weapon a short black "
              "legion combat knife gripped in his right fist, his left hand empty", "hoch", None),
}


def ps(path, data=None):
    req = urllib.request.Request(PS + path, data=None if data is None else json.dumps(data).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


for n, (kind, subject, tags, look, fmt, loras) in NEW.items():
    print("%-8s %-5s %s" % (n, kind, subject))
if not GO:
    sys.exit("PROBELAUF")
presets, sets = dc.load_json(sk.F_PRESETS, None, "Studio"), dc.load_json(sk.F_SETS, None, "Studio")
d = ps("/api/state")["decks"]
out = {c["name"]: c for c in d["outfit"]}
for n, (kind, subject, tags, look, fmt, loras) in NEW.items():
    card = "kampf_" + n.lower()
    if card in out:
        out[card]["prompt"] = look
    else:
        d["outfit"].append({"name": card, "prompt": look, "on": True, "tag": "kampf", "sel": False, "back_prompt": ""})
    p = sk.preset(n, kind, subject, list(tags or []), fmt)
    if loras is not None:
        p["loras"] = loras
    presets["Kampf_" + n] = p
    sets["Kampf_%s|Kampf" % n] = {"outfit": [card], "setting": ["A Sprite Background"], "tags": ["View: Kampf"] + list(tags or [])}
ps("/api/decks", d)
dc.save_json(sk.F_PRESETS, presets, "Studio")
dc.save_json(sk.F_SETS, sets, "Studio")
print("eingetragen:", ", ".join("Kampf_" + n for n in NEW))
