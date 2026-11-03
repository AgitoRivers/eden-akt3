# -*- coding: utf-8 -*-
r"""Duc im Neoprenanzug mit dem Kampfmesser fuer den Tauchgang (Duc 01.11.2026). Eigener Look DucTauch, nur eine Waffe:
Lea raet von allem Klobigen ab. Posen aus kampf_duc_waffen.py, LoRAs wie Kampf_DucWasserKnife. Laeuft ueber
studio.build_graph, die Studio-Einstellungen bleiben unberuehrt.

    kampf_duc_tauch.py probe          -> output\expressions\_casting_duc_tauch\<modell>\idle(-1).png
    kampf_duc_tauch.py lauf [posen]   -> output\expressions\combat\DucTauchKnife\<pose>.png
Danach (nach Abnahme): kampf_duc_spiegeln.py DucTauchKnife --los
"""
import json, os, sys, time, urllib.request

HIER = os.path.dirname(os.path.abspath(__file__))
ARGS = sys.argv[1:]
sys.argv = [sys.argv[0]]
sys.path.insert(0, HIER)
sys.path.insert(0, r"X:\AI\PromptStudio")
import kampf_duc_waffen as w  # noqa: E402

PS, COMFY = "http://127.0.0.1:8301", "http://127.0.0.1:8189"
F_PRESETS = r"X:\AI\PromptStudio\presets.json"
VORLAGE = "Kampf_DucWasserKnife"
# Leitfaden: Einteiler ohne die Woerter jacket und trousers, sonst zerfaellt er
LOOK = ("a seamless one-piece black neoprene wetsuit covering him from the neck to the ankles, a single long zip in the centre of "
        "the chest, a clearly navy blue panel unbroken from shoulder to wrist on each arm, matte black neoprene dive boots, the chest and "
        "arms plain smooth neoprene with no print at all, bold black wraparound sunglasses with dark mirrored lenses on his face, his neck bare of any straps")   # Duc 01.11.: Running Gag, immer Sonnenbrille
LAECHELN = {"idle", "victory"}   # 01.11.: der Subject-Satz liess ihn auch getroffen und erschoepft laecheln
# 01.11.: die Karte allein gab einen schmalen Dolch mit Ring am Griff; so sieht es aus wie Sussurro in den anderen Looks
HELD = ("holding one single medium-sized combat knife in his right hand: a broad single-edged steel blade about one and a half times "
        "as long as his hand with a clipped point and a flat back, a small brass hand guard, and a plain black grip")
MODELLE = {"biglove": {"unet": "BigLoveKreaEdit1_bf16.safetensors", "clip": "qwen3vl_4b_bf16.safetensors"},
           "turbo": {"unet": "krea2_turbo_fp8_scaled.safetensors", "clip": "qwen3vl_4b_fp8_scaled.safetensors"}}
SEEDS = (415201, 882347)


# 01.11. Duc: etwas gepanzert, drei Varianten. Nichts Klobiges (Lea), alles liegt eng am Anzug
# Zweite Runde (Duc): kein Mittelalter, eine schwarze Combat Suit ueber dem Neopren. Die erste Runde a-c liegt in _casting_duc_tauch_panzer
PANZER = {"d": "over the wetsuit a modern matte black tactical combat suit: a fitted hard-shell chest and back protector, slim padded shoulder guards, black forearm guards and black knee guards, all matte black modern ballistic material, the neoprene wetsuit visible at the neck, the wrists and between the guards",
          "e": "over the wetsuit a slim modern matte black tactical vest with a high collar and a few flat closed pouches, black padded shoulder guards and black knee pads, the neoprene wetsuit visible on the arms and legs, a special forces combat diver's look",
          "f": "over the wetsuit a full matte black modern combat suit of tough woven ballistic fabric covering his torso, arms and legs, with moulded hard black panels on the chest, shoulders, forearms and shins, only the neoprene collar and neoprene cuffs of the wetsuit showing underneath"}


BRUST = ("a large moulded hard black armour plate covering his whole chest and stomach in every view, held by wide black shoulder straps, "
         "a wide black belt around his waist, a black pouch strapped to his right thigh")


BRILLE = "bold black wraparound sunglasses with dark mirrored lenses on his face, his neck bare of any straps"


def post(url, d):
    r = urllib.request.Request(url, data=json.dumps(d).encode(), headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(r, timeout=60) as f:
        return json.loads(f.read())


def pose_texte():
    t = w.texte("Knife")
    t["defeated"] = t["defeated"].replace("his clothes clean and neat", "his wetsuit clean")
    # 01.11.: attack und guard hatten je ein zweites Messer
    t["attack"] = t["attack"].replace("the knife arm fully extended", "his right arm fully extended holding the only knife, his rear arm swung back behind him for balance, that rear hand bare and wide open with all five fingers spread and nothing in it; there is exactly one knife in the whole image, the empty palm of the rear hand is visible")
    t["guard"] = t["guard"].replace("like a shield,", "like a shield, his left hand an empty fist,")
    assert "empty palm" in t["attack"] and "empty fist" in t["guard"]
    # 01.11.: zweites Messer in enraged und heavy_attack, in victory wurde die Klinge zum Schwert
    frei = " His left hand is bare and wide open with all five fingers spread and nothing in it; there is exactly one knife in the whole image."
    t["enraged"] += frei
    t["heavy_attack"] += frei
    t["victory"] += " The knife in his raised hand is short, its blade only one and a half times as long as his hand."
    t["heavy_windup"] += " The camera is far back, both boots completely inside the image with empty floor below them."
    t["defeated"] += " Both boots and both feet are completely inside the image, with wide empty space to the right of them."
    return t


def prompt(cfg, vorlage, pose, karte):
    tags = {x["name"]: x for x in cfg["tags"]}
    aktion = tags.get("View: Kampf", {}).get("prompt", "").strip(" ,")
    # Duc 01.11.: Wahl F, erstes Bild. Ohne BRUST fehlte die Platte in acht von dreizehn Posen
    anzug = LOOK + ", " + PANZER["f"] + ", " + BRUST
    wearing = anzug if pose in w.OHNE_WAFFE else anzug + ", " + HELD
    p = vorlage["sprite_prompt"]
    for a, b in (("{tags_action}", aktion), ("{outfit}", wearing), ("{setting}", "Plain beige background"), ("{kampf}", karte)):
        p = p.replace(a, b)
    weg = ("Body: {tags_body},\n", "Hair: {tags_haircolor}, {tags_hairstyle}, {tags_hair}\n", "Skin: {tags_skin},\n", "Face: {tags_face}\n", ",\n{tags_photo}")
    for x in weg:
        p = p.replace(x, "")
    assert "{" not in p, p
    if pose not in LAECHELN:
        assert "a warm confident half smile, " in p
        p = p.replace("a warm confident half smile, ", "")
    return p


def warten(wart):
    ende = time.time() + 900
    while wart and time.time() < ende:
        time.sleep(3)
        for i in list(wart):
            with urllib.request.urlopen(COMFY + "/history/" + i, timeout=30) as f:
                h = json.loads(f.read()).get(i)
            if h:
                print(h.get("status", {}).get("status_str"), flush=True)
                wart.remove(i)
    print("offen", len(wart))


def main():
    import studio
    with urllib.request.urlopen(PS + "/api/state", timeout=30) as f:
        cfg = dict(json.loads(f.read())["cfg"])
    vorlage = json.load(open(F_PRESETS, encoding="utf-8"))[VORLAGE]
    basis = dict(cfg, loras=vorlage["loras"], mode="sprite", sprite_src="t2i", negative_prompt="", st_rembg=True, st_crop=True)
    texte, wart = pose_texte(), []
    if ARGS[:1] == ["probe"]:
        for name, modell in MODELLE.items():
            c = dict(basis, width=880, height=1328, st_set="_casting_duc_tauch/" + name, **modell)
            for s in SEEDS:
                wart.append(post(COMFY + "/prompt", {"prompt": studio.build_graph(c, prompt(cfg, vorlage, "idle", texte["idle"]), "idle", s)})["prompt_id"])
    elif ARGS[:1] == ["panzer"]:
        modell, grund = MODELLE["biglove"], prompt(cfg, vorlage, "idle", texte["idle"])
        for name, text in PANZER.items():
            c = dict(basis, width=880, height=1328, st_set="_casting_duc_tauch_panzer/" + name, **modell)
            p = grund.replace(LOOK + ", " + PANZER["f"], LOOK + ", " + text)
            for s in SEEDS:
                wart.append(post(COMFY + "/prompt", {"prompt": studio.build_graph(c, p, "idle", s)})["prompt_id"])
    elif ARGS[:1] == ["lauf"]:
        modell = MODELLE[ARGS[ARGS.index("--modell") + 1]] if "--modell" in ARGS else MODELLE["biglove"]
        rest = [a for a in ARGS[1:] if a != "--modell" and a not in MODELLE]
        posen = rest[0].split(",") if rest else w.POSEN
        ordner = os.path.join(w.EXPR, "DucTauchKnife")
        for p in posen:
            alt = os.path.join(ordner, p + ".png")
            if os.path.exists(alt):
                os.makedirs(os.path.join(ordner, "_test"), exist_ok=True)
                os.replace(alt, os.path.join(ordner, "_test", "%s_%s.png" % (p, time.strftime("%H%M%S"))))
            b, h = (1328, 880) if p in w.QUER else (1104, 1104) if p in w.QUADRAT["messer"] else (880, 1328)
            c = dict(basis, width=b, height=h, st_set="combat/DucTauchKnife", **modell)
            wart.append(post(COMFY + "/prompt", {"prompt": studio.build_graph(c, prompt(cfg, vorlage, p, texte[p]), p, SEEDS[0] if p == "attack" else SEEDS[1])})["prompt_id"])
    else:
        print(prompt(cfg, vorlage, "idle", texte["idle"]))
        sys.exit("PROBELAUF - probe / lauf [posen] [--modell biglove|turbo]")
    print("eingereiht", len(wart), flush=True)
    warten(wart)


if __name__ == "__main__":
    main()
