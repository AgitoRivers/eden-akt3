# -*- coding: utf-8 -*-
r"""Konter-Pose (Duc 01.11.2026): der Angriff nach der perfekten Parade, Waffe weit nach vorn, Seed wie Ducs Wahl.
Erste Runde liegt in _casting_duc_konter (Speer, Flinte und ErdeSword hat Duc behalten). Zweite Runde: Schlaeger, Saebel, Schrubber und alle Messer mit angewinkelten Knien.

    kampf_duc_konter.py [--nur DucErdeBat,DucLuftKnife]   -> output\expressions\_casting_duc_konter2\<Sprite>\konter.png

Laeuft ueber studio.build_graph, die Studio-Einstellungen bleiben unberuehrt. Nichts wird ins Spiel kopiert.
"""
import json, os, sys, time, urllib.request

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
ARGS = sys.argv[1:]
sys.argv = [sys.argv[0]]
import kampf_duc_tauch as t  # noqa: E402

SEED = 266041
LISTE = [("DucCyberBat", "Bat"), ("DucErdeBat", "Bat"), ("DucFeuerBat", "Bat"), ("DucLuftBat", "Bat"), ("DucWasserBat", "Bat"), ("DucErdeMop", "Mop"),
         ("DucCyberSword", "Sword"), ("DucFeuerSword", "Sword"), ("DucLuftSword", "Sword"), ("DucWasserSword", "Sword"),
         ("DucErdeKnife", "Knife"), ("DucWasserKnife", "Knife"), ("DucFeuerKnife", "Knife"), ("DucLuftKnife", "Knife"), ("DucCyberKnife", "Knife"), ("DucTauchKnife", "Knife")]
EINE = "his left arm swung back behind him for balance, that hand bare, open and empty; there is exactly one %s in the whole image"
# Duc: mit angewinkelten Knien, sonst fliegt er. Er ist gerade abgesprungen und in der Luft
SPRUNG = ("he has just pushed off the floor and jumps forward to the left in a devastating counter strike, both feet off the floor, his front knee bent and pulled up high in front of him, "
          "his rear knee bent with the rear foot behind him, his body upright and not stretched out, ")
FERN = "; seen from a distance, the figure fills only the middle two thirds of the image height, with wide empty floor below his boots, the entire weapon inside the image."
TEXTE = {
    "Sword": SPRUNG + "his right arm stretched far forward to the left, the sabre continuing in one straight line from his forearm, the blade pointing straight to the left, the tip furthest from his body, " + EINE % "sabre" + FERN,
    "Bat": SPRUNG + "his right arm stretched far forward to the left, the bat continuing in one straight line from his forearm, its thick end pointing straight to the left and furthest from his body, " + EINE % "bat" + FERN,
    "Knife": SPRUNG + "his right arm stretched far forward to the left, the knife continuing in one straight line from his forearm, the blade pointing straight to the left, the tip furthest from his body, " + EINE % "knife" + FERN,
    "Mop": SPRUNG + "both arms driving the deck scrubber straight forward to the left like a spear, its handle horizontal, the brush block furthest from his body, exactly one scrubber in the whole image" + FERN,
}


def main():
    import studio
    nur = ARGS[ARGS.index("--nur") + 1].split(",") if "--nur" in ARGS else None
    with urllib.request.urlopen(t.PS + "/api/state", timeout=30) as f:
        st = json.loads(f.read())
    cfg = dict(st["cfg"])
    vorlage = json.load(open(t.F_PRESETS, encoding="utf-8"))[t.VORLAGE]
    basis = dict(cfg, loras=vorlage["loras"], mode="sprite", sprite_src="t2i", negative_prompt="", st_rembg=True, st_crop=True, width=1104, height=1104, **t.MODELLE["biglove"])
    karten = {c["name"]: c["prompt"] for c in st["decks"]["outfit"]}
    wart = []
    for name, waffe in LISTE:
        if nur and name not in nur:
            continue
        p = t.prompt(cfg, vorlage, "heavy_attack", TEXTE[waffe] + " Plain smooth seamless beige studio floor.")
        if name != "DucTauchKnife":
            alt = p.split("Wearing: ")[1].split(",\nScene:")[0]
            p = p.replace(alt, karten["kampf_" + name.lower()].rstrip(" ,"))
        c = dict(basis, st_set="_casting_duc_konter2/" + name)
        wart.append(t.post(t.COMFY + "/prompt", {"prompt": studio.build_graph(c, p, "konter", SEED)})["prompt_id"])
    print("eingereiht", len(wart), flush=True)
    fehler, ende = 0, time.time() + 560
    while wart and time.time() < ende:
        time.sleep(3)
        for i in list(wart):
            with urllib.request.urlopen(t.COMFY + "/history/" + i, timeout=30) as f:
                r = json.loads(f.read()).get(i)
            if r:
                fehler += r.get("status", {}).get("status_str") != "success"
                wart.remove(i)
    print("offen", len(wart), "fehler", fehler)


if __name__ == "__main__":
    main()
