# -*- coding: utf-8 -*-
r"""Ba Tus Laden mit schoenerem Boden (Duc 31.10.2026): Seed und Bildaufbau von Variante 1, nur der Boden wechselt.
Ergebnis: ST\backgrounds\_varianten\eden_rise_batu_shop_v4..6.png, nichts im Spiel.

    batu_boden.py
"""
import os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, r"X:\AI\DucCommon")
sys.path.insert(0, os.path.join(os.path.dirname(HIER), "werkzeuge"))
sys.argv = [sys.argv[0], "--los"]
import casting_dorf as cdorf  # noqa: E402
import item_bilder as ib  # noqa: E402
import hintergrund_bild as hb  # noqa: E402

SEED = 1825493394   # Variante 1
ALT = "Clean white square floor tiles"
BOEDEN = {
    4: "Beautiful old patterned encaustic cement floor tiles with a faded floral pattern in terracotta red, ochre and cream, worn smooth by decades of feet",
    5: "Warm old square terracotta floor tiles in honey and rust tones, hand-made and uneven, worn smooth and softly polished by decades of feet",
    6: "Beautiful old patterned encaustic cement floor tiles with a faded geometric star pattern in sage green, mustard and cream, worn smooth by decades of feet",
}


def main():
    var = os.path.join(cdorf.ST_BG, "_varianten")
    ib.NEGATIV = hb.NEGATIV
    ib.NSFW_PROFIL["loras"] = [("Krea_Real3.safetensors", 0.7)]
    assert ALT in cdorf.HG["batu_shop"]
    for k, boden in BOEDEN.items():
        g = ib.graph(cdorf.HG["batu_shop"].replace(ALT, boden), var, "eden_rise_batu_shop_v%d" % k, SEED, True)
        g["6"]["inputs"].update({"width": 1664, "height": 928})
        print(k, ib.post("/prompt", {"prompt": g}).get("prompt_id"))


if __name__ == "__main__":
    main()
