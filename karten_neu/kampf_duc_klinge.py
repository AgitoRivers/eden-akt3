# -*- coding: utf-8 -*-
r"""Klinge nach vorn (Duc 01.11.2026, Abnahme duc_tauch): attack, heavy_attack und victory im Neopren, heavy_attack auch im Navy-Look. Je 3 Seeds, eigenes Set.

    kampf_duc_klinge.py   -> output\expressions\_casting_duc_klinge\<look>_<pose>\<pose>(-1,-2).png

Laeuft ueber studio.build_graph, die Studio-Einstellungen bleiben unberuehrt.
"""
import json, os, sys, time, urllib.request

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.argv = [sys.argv[0]]
import kampf_duc_tauch as t  # noqa: E402

SEEDS = (415201, 882347, 266041)
VORN = ("his right arm stretched far forward to the left, the knife gripped in his right fist so that the blade continues in one straight line from his forearm, "
        "the blade pointing away from his body straight to the left, the tip of the blade is the point furthest from his body and the grip end touches nothing")
FREI = "his left arm swung back behind him for balance, that hand bare, open and empty; there is exactly one knife in the whole image"
TEXTE = {"attack": "stabbing forward to the left in a fast lunge with both boots on the floor, the blade perfectly horizontal and level like the arm, %s, %s; the whole figure and the entire knife are fully inside the image with wide empty space to the left." % (VORN, FREI),
         "heavy_attack": "leaping forward to the left with a devastating thrust, %s, %s, deep lunge, slight motion blur on the arm; seen from a distance, the figure fills only the middle two thirds of the image height, with wide empty floor below his boots." % (VORN, FREI),
         # Duc: die Klinge ragte oben und unten aus der Faust
         "victory": "triumphant victory pose, gloating, chest out, his right fist raised high above his head, the short knife standing straight up out of the top of his fist, the steel blade only above his fist and nothing below his fist except the short black grip end, his left hand an empty fist, looking down to the left."}
# Duc 01.11.: dieselbe Klinge in den anderen Looks, Seed wie seine Wahl bei Navy
NUR = (("erde", "heavy_attack"), ("feuer", "heavy_attack"), ("luft", "heavy_attack"), ("cyber", "heavy_attack"))
TEXTE["attack"] = ("a deep lunge to the left with both boots on the floor, front knee bent, back leg straight, his right arm straight out at shoulder height, the short broad combat knife with its small brass guard held out in front of him as if pointing with it, his thumb on top of the grip, "
                   "the blade level with the floor and pointing straight to the left at the height of his shoulder, the tip furthest from his body, " + FREI + "; the whole figure and the entire knife are fully inside the image with wide empty space to the left.")
# dritte Runde: mit erhobener Klinge kam sie immer oben und unten aus der Faust, darum hebt er die leere Faust
TEXTE["victory"] = ("triumphant victory pose, gloating, chest out, his left fist raised high above his head and empty, his right arm down at his side, the knife in his right hand with the blade pointing at the floor, looking down to the left; exactly one knife in the whole image.")


def main():
    import studio
    with urllib.request.urlopen(t.PS + "/api/state", timeout=30) as f:
        st = json.loads(f.read())
    cfg = dict(st["cfg"])
    vorlage = json.load(open(t.F_PRESETS, encoding="utf-8"))[t.VORLAGE]
    basis = dict(cfg, loras=vorlage["loras"], mode="sprite", sprite_src="t2i", negative_prompt="", st_rembg=True, st_crop=True, **t.MODELLE["biglove"])
    karten = {c["name"]: c["prompt"] for c in st["decks"]["outfit"]}
    wart = []
    for look, pose in NUR:
        p = t.prompt(cfg, vorlage, pose, TEXTE[pose] + " He stands on a plain smooth seamless beige studio floor.")
        if look != "tauch":
            alt = p.split("Wearing: ")[1].split(",\nScene:")[0]
            p = p.replace(alt, karten["kampf_duc%sknife" % look].rstrip(" ,"))
        b, h = (1104, 1104) if pose == "heavy_attack" else (880, 1328)
        c = dict(basis, width=b, height=h, st_set="_casting_duc_klinge/%s_%s" % (look, pose))
        for s in SEEDS[2:]:
            wart.append(t.post(t.COMFY + "/prompt", {"prompt": studio.build_graph(c, p, pose, s)})["prompt_id"])
    print("eingereiht", len(wart), flush=True)
    ende = time.time() + 280
    while wart and time.time() < ende:
        time.sleep(3)
        for i in list(wart):
            with urllib.request.urlopen(t.COMFY + "/history/" + i, timeout=30) as f:
                if json.loads(f.read()).get(i):
                    wart.remove(i)
    print("offen", len(wart))


if __name__ == "__main__":
    main()
