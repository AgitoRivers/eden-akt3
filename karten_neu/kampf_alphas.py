# -*- coding: utf-8 -*-
r"""Alpha-Varianten (22.10.2026, Duc: "alles übernehmen"): seltene Elite-Gegner, +2 Level, Totenkopf, seltene Beute.
Nur für häufige Gegner (Tiere, namenlose Menschen), nie für Einzelfiguren. Jede Alpha übernimmt Preset und Set-Preset
ihres Grundgegners (Identität, Tags, Format) und bekommt eine eigene Outfit-/Merkmal-Karte "kampf_<name>alpha".
Bewusst ohne Rattenkönig und Stachelhalsband (Trypophobie).

    kampf_alphas.py          Probelauf
    kampf_alphas.py --los    Karten, Presets und Set-Presets anlegen (Prompt Studio muss laufen)
"""
import copy, json, os, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
# studio_kampf_gegner/duc_common are imported only when run as a script: other scripts import ALPHAS/GROUPS from here
# and studio_kampf_gegner rewraps stdout on import (double wrapping breaks their output)

PS = "http://127.0.0.1:8301"
# Alon's zoo animals (not native to Corsica) all wear the same collar - Duc 22.10.2026; used by kampf_neue_gegner_5.py
# first wording gave leather collars with buckle and ring (wolf, bear, goat) and 2-3 lights (lion); only the panther
# came out right - so the shape is spelled out positively (Krea runs with CFG 1, negatives do nothing)
ZOO_COLLAR = ("a wide smooth band collar made of shiny polished chrome-silver metal, closed all around its neck like a "
              "solid metal ring, plain and seamless, with exactly one single small round glowing red light set flush "
              "into the metal band in the middle of the front, the rest of the band smooth and empty")
# Duc 22.10.: zoo predators must look hostile, not like calm nature photos
ZOO_ANGRY = ("snarling furiously with bared teeth, ears flattened back, hackles raised, a menacing hostile glare "
             "straight ahead, ")
# alpha name: (base enemy, group for poses: mensch/tier/flug, look card text)
ALPHAS = {
    "RatAlpha": ("Rat", "tier", "an unusually huge old harbour rat, scarred grey-brown fur, a torn ear, a long scarred "
                 "pink tail, small fierce black eyes, long yellow front teeth, pink paws"),
    "DogAlpha": ("Dog", "tier", "a huge muscular fighting dog, short dark brindle fur marked with old scars, a thick plain "
                 "black leather collar, a broad heavy head, one torn ear, drooling jaws"),
    "SeagullAlpha": ("Seagull", "flug", "an enormous fat seagull wearing a battered tiny captain's cap tilted on its "
                     "head, ruffled white and grey feathers, a yellow beak with a red spot, fierce beady eyes"),
    "PigeonAlpha": ("Pigeon", "flug", "a very fat grand old city pigeon, puffed-up grey feathers with an iridescent green "
                    "and purple neck, a shiny gold ring on one leg, a self-important stare"),
    "BatAlpha": ("Bat", "flug", "a large vampire bat with wings spread, dark grey-black leathery wings, deep red eyes, "
                 "large pointed ears, sharp white fangs"),
    "SnakeAlpha": ("Snake", "tier", "an enormous ancient king cobra, hood spread wide, smooth dark olive and black "
                   "scales, old pale scars along its body, a forked tongue"),
    "ApeAlpha": ("Ape", "tier", "a huge silverback ape, dark fur with a broad silver-grey back, massive long arms, a "
                 "scarred leathery face, a torn zoo ear tag, a battered black pirate tricorn hat with a white skull on "
                 "its head (the captain's cap gag of the normal ape, one step further), " + ZOO_ANGRY + ZOO_COLLAR),
    "LionAlpha": ("Lion", "tier", "a rare huge melanistic black lion with jet-black fur all over its whole body and a huge thick jet-black mane, glowing amber eyes, many old pale scars on its muzzle, a torn "
                  "ear, powerful paws, " + ZOO_ANGRY + ZOO_COLLAR),
    "WolfAlpha": ("Wolf", "tier", "a huge old pack leader wolf, dark grey almost black fur with a silver streak on the "
                  "back, scarred muzzle, one torn ear, burning yellow eyes, " + ZOO_ANGRY + ZOO_COLLAR),
    "PantherAlpha": ("Panther", "tier", "a huge muscular black panther, glossy jet-black fur, old pale claw scars "
                     "across its face, piercing green eyes, long white fangs, " + ZOO_ANGRY + ZOO_COLLAR),
    "GrizzlyAlpha": ("Grizzly", "tier", "an enormous old grizzly bear, grizzled silver-tipped dark fur, a scarred "
                     "face, one clouded eye, huge yellowed claws, " + ZOO_ANGRY + ZOO_COLLAR),
    "SharkAlpha": ("Shark", "tier", "an enormous great white shark covered in long old scars, a torn dorsal fin, grey "
                   "back and white belly, half out of the water"),
    "PirateAlpha": ("Pirate", "mensch", "a long dark red pirate captain's coat with tarnished gold buttons, a black "
                    "tricorn hat, a white shirt, a wide leather belt, high black boots, a long curved cutlass"),
    "ThiefAlpha": ("Thief", "mensch", "a worn black leather jacket over a dark hoodie with the hood down, black jeans, "
                   "heavy black boots, a thick silver chain necklace, a short steel crowbar"),
    "BruteAlpha": ("Brute", "mensch", "a ripped black tank top, grey work trousers, heavy steel-toe boots, a heavy iron "
                   "chain wrapped around one fist, taped knuckles"),
    "AgentAlpha": ("Agent", "mensch", "a sharp white tailored suit, a black shirt, a white tie, an earpiece with a "
                   "coiled wire, black sunglasses pushed up into his hair, black gloves"),
}
# Duc 22.10.2026: human alphas are different people - own face (subject) and body tags, not the base enemy's face
FACES = {
    "PirateAlpha": ("a grizzled Portuguese pirate captain in his late fifties with a weathered face, a long grey braided "
                    "beard and a black eyepatch over one eye", ["M Body: Dad Bod", "M Beard: Full", "M Tan: Deep",
                                                               "M Scar: Face"]),
    "ThiefAlpha": ("a sharp-featured Eastern European gang boss in his late thirties with a shaved head, a cold stare "
                   "and a thin scar through one eyebrow", ["M Body: Lean", "M Hair: Buzz Cut", "M Beard: Stubble"]),
    "BruteAlpha": ("a towering Samoan dock boss in his forties with a broad face and a thick black beard",
                   ["M Body: Bodybuilder", "M Beard: Full", "M Tattoos: Arms", "M Tall"]),
    "AgentAlpha": ("a silver-haired Scandinavian agent chief in his fifties with a hard narrow face and a small scar on "
                   "his chin", ["M Body: Lean", "M Hair: Slicked Back", "M Face: Clean-Shaven"]),
}
GROUPS = {g: [a for a, v in ALPHAS.items() if v[1] == g] for g in ("mensch", "tier", "flug")}


def ps(path, data=None):
    req = urllib.request.Request(PS + path, data=None if data is None else json.dumps(data).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


if __name__ == "__main__":
    GO = "--los" in sys.argv
    sys.argv = [sys.argv[0]]
    import studio_kampf_gegner as sk  # noqa: E402  (sets stdout to UTF-8)
    import duc_common as dc  # noqa: E402
    for a, (base, group, look) in ALPHAS.items():
        print("%-13s <- %-8s %-6s %s" % (a, base, group, look[:60]))
    if not GO:
        sys.exit("PROBELAUF")
    presets, sets = dc.load_json(sk.F_PRESETS, None, "Studio"), dc.load_json(sk.F_SETS, None, "Studio")
    tag_names = {t["name"] for t in dc.load_json(sk.F_CFG, None, "Studio")["tags"]}
    d = ps("/api/state")["decks"]
    out = {c["name"]: c for c in d["outfit"]}
    for a, (base, group, look) in ALPHAS.items():
        if "Kampf_" + base not in presets:
            sys.exit("Grundgegner fehlt im Prompt Studio: Kampf_" + base)
        card = "kampf_" + a.lower()
        if card in out:
            out[card]["prompt"] = look
        else:
            d["outfit"].append({"name": card, "prompt": look, "on": True, "tag": "kampf", "sel": False, "back_prompt": ""})
        p = copy.deepcopy(presets["Kampf_" + base])
        p.update({"st_set": "combat/%s" % a, "sp_char": "Kampf_" + a, "sp_stchar": a,
                  "st_src": os.path.join(sk.EXPR, "combat", a), "st_dst": os.path.join(sk.EXPR, "combat", a),
                  "cards_on": dict(p.get("cards_on") or {}, outfit=[card]), "created": sk.JETZT, "updated": sk.JETZT})
        if a in FACES:                            # own person: new subject in all prompts, own body/face tags
            subject, tags = FACES[a]
            missing = [t for t in tags if t not in tag_names]
            if missing:
                sys.exit("%s: Tag fehlt im Prompt Studio: %s" % (a, missing))
            p["sprite_prompt"], p["base_prompt"], p["fashion_prompt"] = sk.prompts("mann", subject)
            p["tags_on"] = ["View: Kampf"] + tags
        presets["Kampf_" + a] = p
        s = copy.deepcopy(sets.get("Kampf_%s|Kampf" % base) or {"setting": ["A Sprite Background"], "tags": ["View: Kampf"]})
        s["outfit"] = [card]
        if a in FACES:
            s["tags"] = ["View: Kampf"] + FACES[a][1]
        sets["Kampf_%s|Kampf" % a] = s
    ps("/api/decks", d)
    dc.save_json(sk.F_PRESETS, presets, "Studio")
    dc.save_json(sk.F_SETS, sets, "Studio")
    print("eingetragen: %d Alphas" % len(ALPHAS))
