# -*- coding: utf-8 -*-
r"""Abbau-Werkzeuge neu (Duc 29.10.2026): Axt und Spitzhacke alle gleich ausgerichtet (hochkant, Kopf oben, Axtklinge nach
rechts), Forester's Axe mit braunem Stiel und groesserer Klinge, die Spitzen der Spitzhacke werden je Stufe groesser.
Dazu eine Korkeiche VOR dem Schaelen (volle Rinde) als Kandidat - im Spiel steht bisher nur die geschaelte.

    python werkzeuge\abbau_werkzeug_neu.py            rendern -> docs\abnahme\werkzeug_neu\<id>.png
    python werkzeug\abbau_werkzeug_neu.py --einbauen  Werkzeuge -> module\eden_rise\items\<id>.webp

Erst nach Ducs Abnahme einbauen. Rendering wie abbau_bilder.py (Leinen-Look, Krea2 Port 8189)."""
import os, random, sys, time

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import kochen_bilder as K  # noqa: E402

IB = K.IB
ORDNER = os.path.join(K.EDEN, "docs", "abnahme", "werkzeug_neu")
HOCH = ("standing upright vertically in the centre of the frame, the handle pointing straight down and the head at the top, "
        "the whole tool fills about four fifths of the frame height, fully visible with a margin of linen around it")
MOTIVE = {
    "axe_1": "an old small hatchet with a worn smooth ash-wood handle and a dull dark iron head, the blade facing to the right, " + HOCH,
    "axe_2": "a well-balanced forester's axe with a warm brown hickory handle and a large polished bronze head with a warm golden-brown sheen and a broad sharp blade facing to the right, " + HOCH,
    "axe_3": 'a master-forged felling axe with a very large broad head made entirely of gleaming polished sterling silver, bright white-silver like a new silver spoon from the eye to the edge, a wide crescent-shaped edge facing to the right, a dark leather-wrapped handle, ' + HOCH,
    "pickaxe_1": "an old pickaxe with a worn ash-wood handle and a dull dark iron head with two short blunt points to the left "
                 "and right, " + HOCH,
    "pickaxe_2": "a sturdy quarryman's pickaxe with a dark walnut-brown wooden handle and a medium-sized polished bronze head with a warm golden-brown sheen and two sharp points of medium length, " + HOCH,
    "pickaxe_3": 'a master-forged pickaxe with a dark leather-wrapped handle and a head of polished bright silver steel, shining white-silver, with two very long, large, brightly honed points sweeping to the left and right, ' + HOCH,
}
KORK = ("cork_oak_rinde", "a young cork oak tree with its full thick natural cork bark, deeply furrowed pale grey-brown cork "
        "ridges covering the whole trunk from the roots to the branches, a rounded crown of grey-green leaves")


def rendern():
    os.makedirs(ORDNER, exist_ok=True)
    bg = IB.HINTERGRUENDE[IB.HINTERGRUND]
    offen = {}
    for iid, motiv in MOTIVE.items():
        g = IB.graph(IB.STIL.format(motiv=motiv, hintergrund=bg), ORDNER, iid, random.randint(1, 2 ** 31), False)
        offen[iid] = IB.post("/prompt", {"prompt": g})["prompt_id"]
    name, motiv = KORK
    stil = ("Photograph of {motiv}, the whole tree from the roots to the top of the crown, standing upright, fully inside the "
            "frame with a wide empty margin on all sides, the tree fills about two thirds of the frame height, {grund}, "
            "photorealistic, sharp detail, no text")
    g = K.graph_mit_freistellung(stil.format(motiv=motiv, grund=K.GRUND), ORDNER, name, random.randint(1, 2 ** 31))
    g["6"]["inputs"].update({"width": 896, "height": 1152})
    offen[name] = IB.post("/prompt", {"prompt": g})["prompt_id"]
    t0 = time.time()
    while offen and time.time() - t0 < 60 * 20:
        time.sleep(2)
        for k, pid in list(offen.items()):
            h = IB.get("/history/" + pid)
            if pid in h and h[pid].get("status", {}).get("completed"):
                if k == name:
                    K.sprite_fertig(ORDNER, name, os.path.join(ORDNER, name + "_sprite.png"))
                print("fertig", k, flush=True)
                offen.pop(k)
    print("offen:", ", ".join(offen) or "nichts")


def einbauen():
    for iid in MOTIVE:
        with Image.open(os.path.join(ORDNER, iid + ".png")) as im:
            im = im.convert("RGB")
            im.thumbnail((IB.THUMB, IB.THUMB), Image.LANCZOS)
            im.save(os.path.join(K.MOD, "items", iid + ".webp"), "WEBP", quality=85, method=6)
    print("eingebaut:", ", ".join(MOTIVE))


if __name__ == "__main__":
    einbauen() if "--einbauen" in sys.argv else rendern()
