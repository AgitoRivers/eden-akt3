# -*- coding: utf-8 -*-
r"""Kampf-Gegner Runde 4 (22.10.2026): Wildschwein (Erde, Tier, Macchia, Zutatenquelle für 8 Gerichte) und
der Keiler als Elite-Variante "Alpha". Aufbau wie kampf_neue_gegner_3.py.

    kampf_neue_gegner_4.py          Probelauf
    kampf_neue_gegner_4.py --los    Karten über die Studio-API, Presets/Set-Presets per DucCommon
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
NEW = {   # Duc 22.10.: three sizes - small, medium, scarred tusker
    "WildschweinKlein": ("wesen", "a young Corsican wild boar, half grown and lean",
                         "", "reddish-brown bristly fur, a short snout, small round ears, no tusks yet, quick thin legs",
                         "quer", None),
    "Wildschwein": ("wesen", "a sturdy Corsican wild boar",
                    "", "coarse dark brown bristly fur, a ridge of longer bristles along the back, small dark eyes, "
                    "two short curved white tusks, a muddy snout, strong short legs", "quer", None),
    "WildschweinKeiler": ("wesen", "a huge old Corsican wild boar tusker, the leader of the herd",
                          "", "massive shoulders, coarse grey-black bristly fur with a silver ridge along the back, long "
                          "curved yellowed tusks, a long old scar across the snout and one eye, one torn ear, small "
                          "fierce eyes", "quer", None),
}


def ps(path, data=None):
    req = urllib.request.Request(PS + path, data=None if data is None else json.dumps(data).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


for n, (kind, subject, tags, look, fmt, loras) in NEW.items():
    print("%-17s %-5s %s" % (n, kind, subject))
if not GO:
    sys.exit("PROBELAUF")
presets, sets = dc.load_json(sk.F_PRESETS, None, "Studio"), dc.load_json(sk.F_SETS, None, "Studio")
d = ps("/api/state")["decks"]
out = {c["name"]: c for c in d["outfit"]}
for n, (kind, subject, tags, look, fmt, loras) in NEW.items():
    tags = list(tags) if tags else []
    card = "kampf_" + n.lower()
    if card in out:
        out[card]["prompt"] = look
    else:
        d["outfit"].append({"name": card, "prompt": look, "on": True, "tag": "kampf", "sel": False, "back_prompt": ""})
    p = sk.preset(n, kind, subject, tags, fmt)
    if loras is not None:
        p["loras"] = loras
    presets["Kampf_" + n] = p
    sets["Kampf_%s|Kampf" % n] = {"outfit": [card], "setting": ["A Sprite Background"], "tags": ["View: Kampf"] + tags}
ps("/api/decks", d)
dc.save_json(sk.F_PRESETS, presets, "Studio")
dc.save_json(sk.F_SETS, sets, "Studio")
print("eingetragen:", ", ".join("Kampf_" + n for n in NEW))
