# -*- coding: utf-8 -*-
r"""Kampf-Gegner Runde 5 (22.10.2026, Duc): Tiere aus Alons ausgebrochenem Zoo tragen alle DASSELBE Halsband -
poliertes Silber mit einem kleinen roten Licht (die "Behaviour Control Unit" aus docs/wiki/welt/orte.md). Auf Korsika
nicht heimisch: Löwe, Affe (bestehend, bekommen das Halsband), neu Wolf, Schwarzer Panther, Grizzly - je mit Alpha
(Alphas in kampf_alphas.py). Dazu die Ziege als zwei Einzel-Sprites ohne Kampfposen: ohne und mit Halsband (Spur
am Bach / Capra).

    kampf_neue_gegner_5.py          Probelauf
    kampf_neue_gegner_5.py --los    Karten über die Studio-API, Presets/Set-Presets per DucCommon
"""
import json, os, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))   # stdout is set to UTF-8 by studio_kampf_gegner on import
sys.path.insert(0, HERE)
GO = "--los" in sys.argv
sys.argv = [sys.argv[0]]
import studio_kampf_gegner as sk  # noqa: E402
import duc_common as dc  # noqa: E402

PS = "http://127.0.0.1:8301"
# one wording for every zoo animal, so the collar looks the same everywhere
from kampf_alphas import ZOO_COLLAR as COLLAR, ZOO_ANGRY as ANGRY  # noqa: E402
# key: (kind, subject, tags, look, format, loras or None = default)
NEW = {
    "Wolf": ("wesen", "a lean grey wolf", "",
             "thick grey and white fur, yellow eyes, a long muzzle with bared fangs, " + ANGRY + COLLAR, "quer", None),
    "Panther": ("wesen", "a sleek black panther", "",
                "glossy jet-black fur, bright green eyes, long white fangs, a long tail, " + ANGRY + COLLAR, "quer", None),
    "Grizzly": ("wesen", "a huge brown grizzly bear", "",
                "shaggy dark brown fur with lighter tips, a big shoulder hump, long curved claws, small dark eyes, "
                + ANGRY + COLLAR, "quer", None),
    # Duc 22.10.: a cute little white baby goat, not a grown mountain goat
    "Ziege": ("wesen", "a cute little baby goat kid", "",
              "fluffy pure white fur, tiny nub horns, big round dark eyes, soft floppy ears, a sweet curious look, a "
              "small brass bell on a thin leather strap around its neck", "quer", None),
    "ZiegeHalsband": ("wesen", "a cute little baby goat kid", "",
                      "fluffy pure white fur, tiny nub horns, big round dark eyes, soft floppy ears, a sweet curious "
                      "look, " + COLLAR, "quer", None),
}
# existing zoo animals: their outfit cards get the collar and the hostile look too (Duc 22.10.: "auch angry")
BESTEHEND = {"kampf_lion": "a huge golden mane, a scarred muzzle, powerful paws, " + ANGRY + COLLAR,
             "kampf_ape": "dark shaggy fur, long powerful arms, a leathery face, a stolen captain's cap on its head, "
                          + ANGRY + COLLAR}


def ps(path, data=None):
    req = urllib.request.Request(PS + path, data=None if data is None else json.dumps(data).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


for n, (kind, subject, tags, look, fmt, loras) in NEW.items():
    print("%-14s %-5s %s" % (n, kind, subject))
if not GO:
    sys.exit("PROBELAUF")
presets, sets = dc.load_json(sk.F_PRESETS, None, "Studio"), dc.load_json(sk.F_SETS, None, "Studio")
d = ps("/api/state")["decks"]
out = {c["name"]: c for c in d["outfit"]}
for card, text in BESTEHEND.items():
    if card in out:
        out[card]["prompt"] = text
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
print("eingetragen:", ", ".join("Kampf_" + n for n in NEW), "| Halsband in:", ", ".join(BESTEHEND))
