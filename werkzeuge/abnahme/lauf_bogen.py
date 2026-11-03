# -*- coding: utf-8 -*-
"""Raster-Bogen eines Lauf-Ordners: lauf_bogen.py <ordner> <ziel> [spalten]"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

ZIEL = r"Y:\AI\mission-control\entwuerfe\kampf_ui_bilder"
d, ziel = sys.argv[1], sys.argv[2]
sp = int(sys.argv[3]) if len(sys.argv) > 3 else 10
W, H, K = 180, 270, 18
dateien = sorted(f for f in os.listdir(d) if f.endswith(".png"))
zeilen = (len(dateien) + sp - 1) // sp
bogen = Image.new("RGB", (W * sp, (H + K) * zeilen), (14, 15, 19))
dr = ImageDraw.Draw(bogen)
f = ImageFont.truetype("segoeui.ttf", 12)
for i, datei in enumerate(dateien):
    x, y = (i % sp) * W, (i // sp) * (H + K)
    dr.text((x + 4, y + 2), datei[:-4], fill=(216, 189, 134), font=f)
    im = Image.open(os.path.join(d, datei)).convert("RGBA")
    im.thumbnail((W - 4, H - 4))
    feld = Image.new("RGB", (W - 2, H - 2), (128, 128, 128))
    feld.paste(im, ((W - 2 - im.width) // 2, H - 2 - im.height), im)
    bogen.paste(feld, (x + 1, y + K + 1))
bogen.save(os.path.join(ZIEL, ziel + ".png"))
print(os.path.join(ZIEL, ziel + ".png"), len(dateien))
