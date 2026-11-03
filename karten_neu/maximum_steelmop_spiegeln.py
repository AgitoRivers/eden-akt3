# -*- coding: utf-8 -*-
r"""Kampf-Posen MaxwellSteelMop nach rechts spiegeln (Duc 01.11.2026): Duc steuert Maxwell, er steht auf Ducs Seite wie dessen eigene Saetze.
flee laeuft danach vom Gegner weg nach links. Die Marke verhindert doppeltes Spiegeln, _flee_gespiegelt.txt bleibt fuer kampf_flee_spiegeln.py liegen.
Die nach links schauenden Originale liegen weiter in expressions\_maximum_steelmop_satz\kampf (flee ungespiegelt).

    maximum_steelmop_spiegeln.py --los
Danach: python werkzeuge\kampf_bilder.py --gegner MaxwellSteelMop
"""
import glob, os, sys

from PIL import Image

D = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions\combat\MaxwellSteelMop"
MARKE = os.path.join(D, "_nach_rechts_gespiegelt.txt")
assert not os.path.exists(MARKE), "schon gespiegelt"
dat = sorted(glob.glob(os.path.join(D, "*.png")))
assert len(dat) == 13, len(dat)
if "--los" not in sys.argv:
    sys.exit("PROBELAUF - %d Posen" % len(dat))
for p in dat:
    Image.open(p).transpose(Image.FLIP_LEFT_RIGHT).save(p)
with open(MARKE, "w", encoding="utf-8") as f:
    f.write("alle Posen nach rechts gespiegelt (Duc steuert Maxwell)\n")
print(len(dat), "gespiegelt")
