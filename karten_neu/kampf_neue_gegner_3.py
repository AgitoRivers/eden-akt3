# -*- coding: utf-8 -*-
r"""Kampf-Gegner, dritte Runde nach Ducs Element-/Stufen-Konzept (19.10.2026):
Pirat mit Fackel (F,M), arabischer Dieb (N,L), Taube (A,L), Fledermaus (A,L), Alon mit Jetpack (A,H),
Yasin mit Drohne (A,H), Maxwell in drei Stufen: Steward (N,L), Sport (N,M), Maximum (N,Ex).
Ratte (E,L) statt Spinne (Trypophobie-Risiko); Pirat mit Fackel ist Jamaikaner.

    kampf_neue_gegner_3.py          Probelauf
    kampf_neue_gegner_3.py --los    Karten ueber die Studio-API, Presets/Set-Presets per DucCommon

Aufbau wie kampf_neue_gegner_2.py. Alon ist ein erfundener Tech-Milliardaer ohne Aehnlichkeit zu einer echten
Person. Kein Leuchten ausser der Fackelflamme (Teil der Waffe).
"""
import json, os, sys, urllib.request

HIER = os.path.dirname(os.path.abspath(__file__))   # stdout stellt studio_kampf_gegner beim Import auf UTF-8
sys.path.insert(0, HIER)
LOS = "--los" in sys.argv
sys.argv = [sys.argv[0]]
import studio_kampf_gegner as sk  # noqa: E402
import duc_common as dc  # noqa: E402

PS = "http://127.0.0.1:8301"
M_MAX = ["M Body: Bodybuilder", "M Abs", "M Veins", "M Tall", "M Skin: Deep Brown", "M Hair: Bald Shine",
         "M Face: Goatee"]
MAX_SUBJ = "Mr. Maximum, a 35-year-old South African bodybuilder with dark brown eyes"

# key: (Art, Subject, Tags, Merkmal/Outfit, Format, LoRAs oder None = Standard)
NEU = {
    "PirateTorch": ("mann", "a weathered Jamaican pirate in his forties with long black dreadlocks tied back, a short "
                    "black beard, a gold hoop earring and a scar across one cheek",
                    ["M Body: Lean", "M Skin: Deep Brown", "M Tattoos: Arms"],
                    "a torn faded red-and-white striped shirt with ripped-off sleeves, a dark red bandana, a frayed rope "
                    "belt, ragged brown knee-length trousers, barefoot, a burning wooden torch in his right hand",
                    "hoch", None),
    "ThiefArab": ("mann", "a skinny young Arab thief in his early twenties with a thin moustache",
                  ["M Body: Lean"],
                  "a black hoodie with the hood pulled up, a black cloth mask covering nose and mouth, slim black "
                  "jeans, black sneakers with white soles, a small black backpack, a short steel crowbar in his right "
                  "hand", "hoch", None),
    "Pigeon": ("wesen", "a plump scruffy city pigeon",
               "", "grey feathers with an iridescent green and purple neck, orange eyes, pink feet, one bent tail "
               "feather, a crumb of bread in its beak", "quer", None),
    "Bat": ("wesen", "a large fruit bat with wings spread",
            "", "dark brown leathery wings, a furry golden-brown body, big dark eyes, small pointed ears, tiny "
            "white fangs", "quer", None),
    "Rat": ("wesen", "a big brown harbour rat",
            "", "glossy dark brown fur, a long pink tail, beady black eyes, long whiskers, sharp yellow front teeth, "
            "pink paws", "quer", None),
    "Alon": ("mann", "a smug fictional tech billionaire in his fifties with a short buzz cut and a cocky grin",
             ["M Body: Dad Bod", "M Face: Clean-Shaven"],
             # 22.10.2026: same armor as the item cyber_armor (v8, Duc's pick): glossy piano-black, sculpted plates
             "wearing a glossy piano-black cyber armor torso shell with sculpted chest plates and segmented shoulder "
             "guards like a superhero suit, high-gloss black lacquer surfaces with sharp reflections, dark jeans, white "
             "sneakers, aviator sunglasses, a chunky chrome jetpack strapped to his back with two exhaust nozzles, a "
             "sleek white-and-black futuristic ray gun in his right hand",       # Duc 22.10.: Strahlenpistole
             "hoch", None),
    "YasinDrone": ("mann", "Yasin, a handsome 29-year-old Arab man from Paris with a short black skin-fade haircut, "
                   "a neatly trimmed black beard, furrowed brows and a furious angry scowl, glaring with clenched jaw",
                   ["M Body: Lean"],
                   "an open white linen shirt over a bare chest, a thin gold chain, beige linen shorts, white designer "
                   "sneakers, a heavy gold watch, a drone remote control in both hands, a large solid matte black quadcopter drone with four "
                   "black propellers hovering clearly visible at head height beside him", "hoch", None),
    "MaxwellSteward": ("mann", MAX_SUBJ, M_MAX,
                       # 22.10.2026 (Duc): white polo with a real collar, not a crew neck
                       "a white short-sleeved polo shirt with a folded-down collar and a three-button placket, "
                       "stretched tight over his chest and arms, a small golden anchor logo on the left chest, a black "
                       "name badge reading MR. MAXIMUM, navy tailored shorts, white deck sneakers, orange mirrored "
                       "wraparound sport sunglasses over his eyes", "hoch", None),   # Duc 22.10.: Brille fehlte
    "MaxwellSports": ("mann", MAX_SUBJ, M_MAX,
                      "a neon orange sleeveless tank top, black compression shorts, black training shoes, a white "
                      "sweatband on his forehead, a towel around his neck", "hoch", None),
    "MaxwellMaximum": ("mann", MAX_SUBJ, M_MAX + ["M Skin: Oiled"],
                       "shirtless, small shiny gold bodybuilding posing trunks, a huge golden championship belt "
                       "around his waist, black boxing wraps on his hands, barefoot", "hoch", None),
}


def ps(pfad, daten=None):
    req = urllib.request.Request(PS + pfad, data=None if daten is None else json.dumps(daten).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


for n, (art, subject, tags, merkmal, fmt, loras) in NEU.items():
    print("%-15s %-5s %s" % (n, art, subject))
if not LOS:
    sys.exit("PROBELAUF")
presets, sets = dc.load_json(sk.F_PRESETS, None, "Studio"), dc.load_json(sk.F_SETS, None, "Studio")
tag_namen = {t["name"] for t in dc.load_json(sk.F_CFG, None, "Studio")["tags"]}
d = ps("/api/state")["decks"]
out = {c["name"]: c for c in d["outfit"]}
for n, (art, subject, tags, merkmal, fmt, loras) in NEU.items():
    tags = list(tags) if tags else []
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
print("eingetragen:", ", ".join("Kampf_" + n for n in NEU))
