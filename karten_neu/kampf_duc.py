# -*- coding: utf-8 -*-
r"""Duc's own combat sprites (23.10.2026): five looks = four leather jackets (one per element) + full-body cyber armor.
Duc: the leather jacket is his style; each look gets its own shirt and sunglasses so the face reads at small size.
Identity: subject sentence + Duc's real photo as face reference (refs\Duc_Foto.jpg). Build like kampf_yamamoto_samurai.py.

    kampf_duc.py          dry run
    kampf_duc.py test     enter cards/presets/set presets, queue one test image per look (outfit_check)

CAUTION (24.10.): Duc tunes the look cards kampf_duc* directly in Prompt Studio since then - LOOKS below is outdated
and any run overwrites his cards. Weapon sprites: kampf_duc_waffen.py (reads the cards live).
"""
import json, os, shutil, subprocess, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))   # stdout is set to UTF-8 by studio_kampf_gegner on import
sys.path.insert(0, HERE)
MODE = sys.argv[1].lower() if len(sys.argv) > 1 else ""
STRENGTH = sys.argv[2] if len(sys.argv) > 2 else ""
sys.argv = [sys.argv[0]]
import studio_kampf_gegner as sk  # noqa: E402
import duc_common as dc  # noqa: E402

PS = "http://127.0.0.1:8301"
REF = r"X:\AI\PromptStudio\refs\Duc_Foto.jpg"
SUBJECT = ("Ducx, an Asian man in his early thirties, black hair with a clean side part slicked back, "
           "light stubble, dark brown eyes, a warm confident half smile, slim athletic build")
# 24.10.: identity LoRA trained from Duc's photos (trigger "Ducx"); replaces the face reference
LORA = {"name": "Krea_Ducx.safetensors", "strength": 1.0}
# 24.10. strength test: "kampf_duc.py test 0.8" (at 1.0 every look got Duc's own round brown sunglasses)
if STRENGTH:
    LORA["strength"] = float(STRENGTH)
# 24.10. Duc: 2 dark navy turtleneck, 3 burgundy shirt, 4 like a Formula 1 race suit with matching trousers,
# 5 darker. Sunglasses described in more detail so they stay distinct per look.
LOOKS = {   # name: (element, outfit card text)
    "DucErde": ("Erde", "a black leather biker jacket with an asymmetric zip and bronze zippers and buckles, a plain white "
                        "crew-neck t-shirt, black slim jeans, dark brown leather boots, large teardrop aviator sunglasses "
                        "with thin bronze metal frames and dark green lenses"),
    "DucWasser": ("Wasser", "a smooth shiny dark navy leather double-breasted jacket in a short pea coat cut with two rows "
                            "of dark buttons, a dark navy blue turtleneck sweater, charcoal trousers, black leather boots, "
                            "bold rectangular sunglasses with thick black frames and black lenses"),
    "DucFeuer": ("Feuer", "a bordeaux red leather cafe racer jacket with a short band collar and a front zip, a burgundy "
                          "button-down shirt, black slim jeans, black leather boots, small perfectly round sunglasses "
                          "with thin black wire frames"),
    "DucLuft": ("Luft", "a white Formula 1 racing suit style outfit: a white fireproof racing jacket with a high zipped "
                        "racing collar, gold and burgundy stripes across the chest and down the sleeves, a gold EDEN logo "
                        "on the chest, matching white racing suit trousers with gold and burgundy stripes down the side "
                        "of the legs, white racing shoes, sporty wraparound sunglasses with gold mirrored lenses"),
    "DucCyber": ("alle", "a full-body dark gunmetal and black chrome cyber armor suit covering him from neck to feet, "
                         "large smooth darkened armored plates on the chest, shoulders, arms, legs and boots, flexible "
                         "black segments at the joints, thin glowing blue lines along the plate edges, no helmet so his "
                         "face and hair stay visible, large teardrop aviator sunglasses with thin bronze metal frames"),
}
# Test-fight sprite (23.10., Duc): look 1 with a sabre, full pose run for simulated fights (until the Duc LoRA exists)
LOOKS["DucErdeSword"] = ("Erde", LOOKS["DucErde"][1] + ", holding one single curved steel cavalry sabre with a brass "
                                                       "hand guard in his right hand")
VOLL = ["DucErdeSword"]


def ps(path, data=None):
    req = urllib.request.Request(PS + path, data=None if data is None else json.dumps(data).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


for n, (el, look) in LOOKS.items():
    print("%-10s %-6s %s" % (n, el, look[:90]))
if not os.path.exists(REF):
    sys.exit("Referenzfoto fehlt: " + REF)
if MODE not in ("test", "idle", "voll"):
    sys.exit("PROBELAUF - test (Testbilder) / idle (Idle je Look) / voll (Posen-Lauf fuer %s)" % ", ".join(VOLL))

presets, sets = dc.load_json(sk.F_PRESETS, None, "Studio"), dc.load_json(sk.F_SETS, None, "Studio")
d = ps("/api/state")["decks"]
cards = {c["name"]: c for c in d["outfit"]}
for n, (el, look) in LOOKS.items():
    card = "kampf_" + n.lower()
    if card in cards:
        cards[card]["prompt"] = look
    else:
        d["outfit"].append({"name": card, "prompt": look, "on": True, "tag": "kampf", "sel": False, "back_prompt": ""})
    p = sk.preset(n, "mann", SUBJECT, [], "hoch")
    p["loras"] = [LORA] + p["loras"]        # identity LoRA first, then the usual realism LoRAs
    presets["Kampf_" + n] = p
    sets["Kampf_%s|Kampf" % n] = {"outfit": [card], "setting": ["A Sprite Background"], "tags": ["View: Kampf"]}
ps("/api/decks", d)
dc.save_json(sk.F_PRESETS, presets, "Studio")
dc.save_json(sk.F_SETS, sets, "Studio")
print("eingetragen:", ", ".join("Kampf_" + n for n in LOOKS))
if MODE == "voll":
    subprocess.run([sys.executable, os.path.join(HERE, "kampf_volllauf_runde3.py"), "--los", "--gegner",
                    ",".join(VOLL)], check=True)
    print("Posen eingereiht:", ", ".join(VOLL))
else:
    subprocess.run([sys.executable, os.path.join(HERE, "kampf_test.py"), "--karten",
                    "outfit_check" if MODE == "test" else "idle", "--gegner",
                    ",".join(n for n in LOOKS if n not in VOLL)], check=True)
    print("eingereiht -> output\\expressions\\combat\\Duc*")
