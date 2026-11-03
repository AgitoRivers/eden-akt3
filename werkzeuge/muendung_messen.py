# -*- coding: utf-8 -*-
r"""Wo in den Kampfbildern die Waffe endet (Duc 01.11.2026): Mündungsfeuer sitzt so genau am Lauf, ohne Handarbeit je Pose.

    python werkzeuge\muendung_messen.py   -> module\eden_rise\muendung.json {sprite: {pose: [x, y]}}, Anteile am Bild

Gegner schauen nach links, Ducs Sätze nach rechts: Der Lauf ist der äußerste Punkt der Figur in Blickrichtung, gemessen in attack und heavy_attack
(dort ist der Arm gestreckt). Danach kaempfe_eden_rise.py laufen lassen, es trägt die Tabelle in kaempfe.json ein.
"""
import json, os, sys

import numpy as np
from PIL import Image

EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KAMPF = os.path.join(EDEN, "module", "eden_rise", "kampf")
GEGNER = ("PirateGunner", "AgentGunman")
POSEN = ("attack", "heavy_attack", "konter")
BREITE = 14


def spitze(pfad, nach_links):
    a = np.array(Image.open(pfad).convert("RGBA"))[..., 3] > 128
    h, w = a.shape
    spalten = np.where(a.sum(0) >= 2)[0]
    if not len(spalten):
        return None
    x = int(spalten[0] if nach_links else spalten[-1])
    streifen = a[:, x:x + BREITE] if nach_links else a[:, max(0, x - BREITE + 1):x + 1]
    zeilen = np.where(streifen.sum(1) > 0)[0]
    return [round(x / w, 4), round(float(zeilen.mean()) / h, 4)]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    namen = [(n, True) for n in GEGNER] + [(n, False) for n in sorted(os.listdir(KAMPF)) if n.startswith("Duc") and n.endswith("Gun")]
    aus = {}
    for name, links in namen:
        for pose in POSEN:
            p = os.path.join(KAMPF, name, pose + ".webp")
            if os.path.isfile(p):
                aus.setdefault(name, {})[pose] = spitze(p, links)
    with open(os.path.join(EDEN, "module", "eden_rise", "muendung.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(aus, f, ensure_ascii=False, indent=1)
    print(len(aus), "Sätze:", ", ".join(aus))


if __name__ == "__main__":
    main()
