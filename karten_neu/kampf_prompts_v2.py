# -*- coding: utf-8 -*-
r"""Kampf-Gegner, Prompts v2 (19.10.2026): feste Erkennungsmerkmale je Gegner, damit Krea ueber alle Posen dieselbe
Figur zeichnet (Duc: je klarer der Prompt, desto konsistenter). Keine Loecher-Cluster (Duc hat Trypophobie):
keine Seepocken, Saugnaepfe, Lueftungsgitter.

    kampf_prompts_v2.py          Probelauf
    kampf_prompts_v2.py --los    Merkmal-Karten live ueber die Studio-API, Subject-Zeile in presets.json

Subject = WER (Identitaet, Gesicht, Koerperbau-Anker); Karte kampf_<name> = Kleidung/Merkmale/Requisit.
Kein Gesichtsausdruck hier - den liefert die Kampf-Karte.
"""
import io, json, re, sys, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, r"X:\AI\DucCommon")
import duc_common as dc  # noqa: E402

LOS = "--los" in sys.argv
PS = "http://127.0.0.1:8301"
F_PRESETS = r"X:\AI\PromptStudio\presets.json"

V2 = {
    "Pirate": ("a gaunt weathered Irish pirate in his forties with a wild red beard, freckles, a black eyepatch over his left eye and a gold front tooth",
               "a torn faded red-and-white striped shirt with ripped-off sleeves, a dark red bandana, a frayed rope belt, "
               "ragged brown knee-length trousers, barefoot, a rusty curved cutlass in his right hand"),
    "Thief": ("a skinny young Korean thief in his early twenties",
              "a black hoodie with the hood pulled up, a black cloth mask covering nose and mouth, round black-rimmed "
              "glasses, slim black jeans, black sneakers with white soles, a small black backpack, a short steel "
              "crowbar in his right hand"),
    "Brute": ("a hulking Samoan dock thug with a thick neck, clean unmarked skin and traditional Samoan tattoos on his arms and shoulders",
              "a sweat-stained white ribbed tank top, grey cargo work trousers, black steel-toe boots, knuckles wrapped "
              "in white tape, a heavy iron chain wrapped around his left fist"),
    "Heinrich": ("Heinrich, a sleazy German boat playboy in his fifties with a gold earring",
                 "a white linen shirt unbuttoned to the navel, a thick gold chain on a hairy chest, tight white shorts, "
                 "white leather loafers without socks, gold aviator sunglasses, a gold watch, a champagne flute in his "
                 "left hand"),
    "Agent": ("a tall clean-cut Black British corporate agent in his thirties with a square jaw and a short fade haircut",
              "a black tailored suit, a crisp white shirt, a slim black tie, a clear earpiece with a coiled wire behind "
              "his right ear, black sunglasses, black leather gloves, polished black shoes, a black stun baton in his "
              "right hand"),
    "Vampire": ("a tall elegant female vampire with porcelain skin, glowing red eyes and long sharp fangs",
                "a floor-length black velvet gown with a high Victorian collar and long sleeves, a black cape lined with "
                "crimson silk, a ruby pendant on a black velvet choker, long pointed black nails"),
    "Alien": ("a slender grey-skinned humanoid alien with a large smooth bald head and huge glossy black almond eyes",
              "a sleek white space suit with silver seams and one glowing blue circle on the chest, a silver helmet "
              "ring around the neck without a helmet, white boots and gloves, a small silver ray gun in its right hand"),
    "Lion": ("a massive adult male lion",
             "a thick dark brown and golden mane, a pale scar across the bridge of its nose, amber eyes, huge paws "
             "with extended claws, a long tail with a black tuft"),
    "Snake": ("a giant king cobra rearing upright",
              "its hood spread wide with a pale band pattern, glossy smooth olive-brown scales, a cream belly, a forked "
              "black tongue, two long fangs"),
    "Unit1": ("Unit-01, a clunky walking robot built from a boxy orange steel cabinet",
              "a boxy dented orange-painted steel cabinet body, every side smooth flat painted sheet metal with big rivets, a broad yellow-and-black hazard stripe band around the middle, a riveted hatch with a chunky handle, a red fire extinguisher strapped to its back, two thick hydraulic legs, two exhaust pipes on top belching black smoke, loose sparking cables hanging like arms, one round red warning light as its single eye, black stencil letters UNIT-01 on its side"),
    "Seagull": ("a fat aggressive herring gull",
                "a white head and belly, light grey wings with black wingtips, a thick yellow beak with a red spot, "
                "pale yellow eyes with a mean stare, pink webbed feet, a stolen golden french fry in its beak"),
    "Dog": ("a big muscular guard dog, a brindle mastiff mix",
            "short brindle fur, a broad head with heavy jowls, cropped ears, a black spiked leather collar, drool "
            "hanging from its jaws"),
    "Shark": ("a great white shark",
              "a slate-grey back and a white belly, one jagged scar along its left flank, rows of serrated teeth, black "
              "eyes, its upper body bursting out of the water with splashing spray"),
    "SeaMonster": ("a hulking amphibious sea monster from the deep, half giant fish, half lizard",
                   "smooth slimy dark green skin with large smooth scales, a long crocodile-like jaw with jagged teeth, "
                   "a row of orange fins along its back and tail, glowing yellow eyes, no tentacles, dripping seaweed, "
                   "rising out of the water"),
    "Ape": ("a big adult chimpanzee",
            "shaggy black fur, long powerful arms, a wrinkled leathery face, a stolen white captain's cap with a gold "
            "anchor on its head"),
}


def ps(pfad, daten=None):
    req = urllib.request.Request(PS + pfad, data=None if daten is None else json.dumps(daten).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


presets = dc.load_json(F_PRESETS, None, "Studio")
d = ps("/api/state")["decks"]
karten = {c["name"]: c for c in d["outfit"]}
for name, (subject, merkmal) in V2.items():
    p = presets["Kampf_" + name]
    k = karten["kampf_" + name.lower()]
    print("%-11s Subject: %s\n            Karte:   %s" % (name, subject, merkmal[:100]))
    if LOS:
        for feld in ("sprite_prompt", "base_prompt", "fashion_prompt"):
            p[feld] = re.sub(r"Subject: [^\n]*,\n", lambda m: "Subject: %s,\n" % subject, p[feld], count=1)
        k["prompt"] = merkmal
if LOS:
    dc.save_json(F_PRESETS, presets, "Studio")
    ps("/api/decks", d)
    print("geschrieben")
else:
    print("PROBELAUF")
