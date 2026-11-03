# -*- coding: utf-8 -*-
r"""Kampf-Gegner, zweite Runde (19.10.2026, Duc): Paparazzo (Tuerke), Sirene (oben ohne), Pantomime, Drunk Casanova (ein betrunkener
Schoenling, der Alva an der Bar bedraengt - NICHT Madame Casanova). Dazu die Karte outfit_check (Tag "check",
gehoert nicht zu den Kernposen) zum Pruefen der Outfits.

    kampf_neue_gegner_2.py          Probelauf
    kampf_neue_gegner_2.py --los    Karten ueber die Studio-API, Presets/Set-Presets per DucCommon

Aufbau wie studio_kampf_gegner.py (dessen preset() wird wiederverwendet). Keine Loecher-Muster; Sperren nur
positiv (Krea laeuft mit CFG 1).
"""
import io, json, os, sys, urllib.request

HIER = os.path.dirname(os.path.abspath(__file__))   # stdout stellt studio_kampf_gegner beim Import auf UTF-8
sys.path.insert(0, HIER)
LOS = "--los" in sys.argv
sys.argv = [sys.argv[0]]
import studio_kampf_gegner as sk  # noqa: E402
import duc_common as dc  # noqa: E402

PS = "http://127.0.0.1:8301"
CHECK = ("outfit_check", "check", "standing relaxed and upright, full body clearly visible from head to feet, arms "
         "held slightly away from the body, calm neutral face, turned slightly to the left")

# key: (Art, Subject, Tags, Merkmal/Outfit, Format, LoRAs oder None = Standard)
NEU = {
    "Paparazzo": ("mann", "a pushy Turkish paparazzo in his forties with deeply tanned leathery skin, greasy slicked-back black hair, "
                  "a thick black moustache and dark stubble",
                  ["M Body: Dad Bod", "M Hair: Slicked Back", "M Tan: Deep", "M Color: Black Grey Temples"],
                  "an open black leather jacket over a plain grey t-shirt, blue jeans, white sneakers, a red lanyard with a press "
                  "badge, a big black camera with a huge telephoto lens in both hands", "hoch", None),
    "Siren": ("frau", "a beautiful siren, a mermaid with long flowing red hair and sea-green eyes",
              ["Color: Red", "Style: Long Wet Hair", "Huge", "Pale skin"],
              "a long shimmering emerald-green fish tail instead of legs, topless, "
              "a string of pearls around her neck, wet glistening skin, resting upright on a smooth wet rock", "hoch",
              [{"name": "Krea_Real3.safetensors", "strength": 0.7}]),
    "Mime": ("mann", "a lanky French street mime in his thirties with a white painted face, black painted lips and "
             "drawn-on black teardrops", ["M Body: Lean", "M Face: Clean-Shaven"],
             "a black-and-white horizontally striped long-sleeved shirt, black suspenders, baggy black trousers, a black "
             "beret, white gloves, black lace-up shoes, a red scarf around his neck", "hoch", None),
    "DrunkCasanova": ("mann", "a drunk sleazy Spanish lothario in his thirties with slicked-back black hair, flushed "
                      "red cheeks and a few pink lipstick kiss prints on his cheek",
                      ["M Body: Lean", "M Beard: Stubble", "M Hair: Slicked Back"],
                      # 22.10.2026 (Duc): the rose often came out with a bloom on both ends, the open bottle spilled red
                      "a wrinkled burgundy velvet blazer, a black silk shirt half unbuttoned, tight black trousers, "
                      "pointed brown shoes, ONE single red rose between his teeth with ONE bloom on one side and only a "
                      "bare green stem on the other, a corked bottle of red wine in his hand", "hoch",
                      None),
}


def ps(pfad, daten=None):
    req = urllib.request.Request(PS + pfad, data=None if daten is None else json.dumps(daten).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


for n, (art, subject, tags, merkmal, fmt, loras) in NEU.items():
    print("%-14s %-5s %s\n               Tags: %s | LoRAs: %s" % (n, art, subject, ", ".join(tags),
                                                                  "Standard" if loras is None else loras))
if not LOS:
    sys.exit("PROBELAUF")
presets, sets = dc.load_json(sk.F_PRESETS, None, "Studio"), dc.load_json(sk.F_SETS, None, "Studio")
tag_namen = {t["name"] for t in dc.load_json(sk.F_CFG, None, "Studio")["tags"]}
d = ps("/api/state")["decks"]
if CHECK[0] not in {c["name"] for c in d["kampf"]}:
    d["kampf"].append({"name": CHECK[0], "prompt": CHECK[2], "on": True, "tag": CHECK[1], "sel": False})
out = {c["name"]: c for c in d["outfit"]}
for n, (art, subject, tags, merkmal, fmt, loras) in NEU.items():
    fehlt = [t for t in tags if t not in tag_namen]
    if fehlt:
        sys.exit("%s: Tag fehlt: %s" % (n, fehlt))
    karte = "kampf_" + n.lower()
    if karte in out:
        out[karte]["prompt"] = merkmal
    else:
        d["outfit"].append({"name": karte, "prompt": merkmal, "on": True, "tag": "kampf", "sel": False,
                            "back_prompt": ""})
    p = sk.preset(n, art, subject, tags, fmt)
    if loras is not None:
        p["loras"] = loras
    presets["Kampf_" + n] = p
    sets["Kampf_%s|Kampf" % n] = {"outfit": [karte], "setting": ["A Sprite Background"],
                                  "tags": ["View: Kampf"] + tags}
ps("/api/decks", d)
dc.save_json(sk.F_PRESETS, presets, "Studio")
dc.save_json(sk.F_SETS, sets, "Studio")
print("eingetragen:", ", ".join("Kampf_" + n for n in NEU), "+ Karte outfit_check")
