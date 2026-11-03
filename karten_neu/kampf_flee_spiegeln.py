# -*- coding: utf-8 -*-
r"""Kampf-Sprites: flee.png horizontal spiegeln (19.10.2026). Krea zeichnet alle Gegner nach links gewandt (zu Duc);
gespiegelt laeuft der Gegner nach rechts weg und schaut ueber die Schulter zurueck zu Duc.
Unit1 bleibt ungespiegelt (sonst stuende "UNIT-01" in Spiegelschrift). Eine Markierungsdatei _flee_gespiegelt.txt
verhindert doppeltes Spiegeln.

    kampf_flee_spiegeln.py          Probelauf
    kampf_flee_spiegeln.py --los    spiegelt
"""
import io, os, sys
from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
LOS = "--los" in sys.argv
E = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions\combat"
AUSNAHMEN = {"Unit1"}
for n in sorted(os.listdir(E)):
    d = os.path.join(E, n)
    f, mark = os.path.join(d, "flee.png"), os.path.join(d, "_flee_gespiegelt.txt")
    if n.endswith("_TEST") or not os.path.exists(f):
        continue
    if n in AUSNAHMEN or os.path.exists(mark):
        print("%-11s bleibt" % n)
        continue
    print("%-11s wird gespiegelt" % n)
    if LOS:
        Image.open(f).transpose(Image.FLIP_LEFT_RIGHT).save(f)
        open(mark, "w").write("flee.png horizontal gespiegelt (laeuft nach rechts weg)\n")
print("gespiegelt" if LOS else "PROBELAUF")
