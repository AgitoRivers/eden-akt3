# -*- coding: utf-8 -*-
r"""Ligeias Kampf-Sprites vor dem Import saeubern (Duc 30.10.2026, Abnahme kampf_ligeia): Maske schaerfen und kleine Inseln neben der
Figur entfernen (Spritzer, Flecken am Boden). Danach Kampf_Bilder.bat --gegner Siren.
"""
import glob, os, shutil, time

import numpy as np
from PIL import Image
from scipy import ndimage

C = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions\combat\Siren"
KORB = r"X:\AI\ComfyUI_krea2\ComfyUI\output\_expressions_papierkorb\combat\siren_vor_saeubern_" + time.strftime("%Y%m%d_%H%M")
os.makedirs(KORB, exist_ok=True)
POSEN = ("idle", "windup", "attack", "heavy_windup", "heavy_attack", "guard", "hurt", "weakened", "enraged", "flee", "surrender",
         "victory", "defeated", "death")
for p in POSEN:
    f = os.path.join(C, p + ".png")
    shutil.copy2(f, KORB)
    im = Image.open(f).convert("RGBA")
    a = np.asarray(im.getchannel("A")).astype(float)
    a = np.clip((a - 110) * 255 / 60, 0, 255)
    inseln, n = ndimage.label(a > 0)
    if n:
        groesse = ndimage.sum(a > 0, inseln, range(1, n + 1))
        behalten = np.isin(inseln, np.flatnonzero(groesse >= groesse.max() * 0.02) + 1)
        a = a * behalten
    im.putalpha(Image.fromarray(a.astype("uint8")))
    im.save(f)
    print(p, "Inseln:", n)
print("Vorlagen in", KORB)
