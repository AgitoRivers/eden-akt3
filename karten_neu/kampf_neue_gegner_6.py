# -*- coding: utf-8 -*-
r"""Kevin, der Kakadu (23.10.2026, Duc): Bord-Maskottchen und Erzfeind statt der Möwe - weißer Kakadu mit rosa Haube und
rosa Bäckchen, redet und klaut. Kampfposen per kampf_nachbessern.py. Aufbau wie kampf_neue_gegner_4.py.

    kampf_neue_gegner_6.py          Probelauf
    kampf_neue_gegner_6.py --los    Karte über die Studio-API, Preset/Set-Preset per DucCommon
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
NEW = {
    # Duc 23.10. evening: Kevin is the white cockatoo (talks, steals) with pink blush and pink crest feathers;
    # the magpie stays available as "Elster"
    "Kevin": ("wesen", "a cheeky white cockatoo",
              "", "fluffy pure white feathers, a tall crest raised up on its head made of soft bubblegum pink feathers (pink like candy floss, not orange), "
              "round rosy pink blush patches on both cheeks, a curved dark grey beak, big clever dark eyes, a cheeky "
              "talkative look, cute and mischievous", "quer", None),
    # Elster, Adler, Falke and the yellow-crested Papagei were tested on 23.10. and dropped by Duc
    # (removed from Prompt Studio again; Kevin is the pink cockatoo above)
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
    p = sk.preset(n, kind, subject, [], fmt)
    if loras is not None:
        p["loras"] = loras
    presets["Kampf_" + n] = p
    sets["Kampf_%s|Kampf" % n] = {"outfit": [card], "setting": ["A Sprite Background"], "tags": ["View: Kampf"]}
ps("/api/decks", d)
dc.save_json(sk.F_PRESETS, presets, "Studio")
dc.save_json(sk.F_SETS, sets, "Studio")
print("eingetragen:", ", ".join("Kampf_" + n for n in NEW))
