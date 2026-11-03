# -*- coding: utf-8 -*-
r"""Bibis Dosen schwarz nachfaerben (Duc 30.10.2026): "grenade" zieht trotz "jet black" Armee-Oliv ins Bild. Oliv kommt in
ihren Kampf-Sprites sonst nirgends vor (Anzug rot, Hintergrund beige), also wird genau dieser Farbton entsaettigt und
abgedunkelt. Der Alpha-Kanal bleibt. Die unbearbeiteten Bilder liegen danach in output\_expressions_papierkorb\combat.

    kampf_bibi_schwarz.py [pose,pose]     ohne Angabe alle PNG in combat\Bibi
"""
import colorsys, os, shutil, sys, time

from PIL import Image

C = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions\combat\Bibi"
KORB = r"X:\AI\ComfyUI_krea2\ComfyUI\output\_expressions_papierkorb\combat\bibi_vor_schwarz_" + time.strftime("%Y%m%d_%H%M")
H_VON, H_BIS, S_MIN = 45 / 360, 170 / 360, 0.10     # Oliv bis Graugruen; Beige (um 35 Grad) und Rot bleiben draussen
LUT = {}


def farbe(r, g, b):
    k = (r >> 2, g >> 2, b >> 2)
    if k not in LUT:
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        LUT[k] = None if not (H_VON <= h <= H_BIS and s >= S_MIN) else min(v, 1) ** 1.3 * 0.42
    return LUT[k]


def main():
    posen = sys.argv[1].split(",") if len(sys.argv) > 1 else [f[:-4] for f in os.listdir(C) if f.endswith(".png")]
    os.makedirs(KORB, exist_ok=True)
    for p in posen:
        f = os.path.join(C, p + ".png")
        shutil.copy2(f, os.path.join(KORB, p + ".png"))
        im = Image.open(f).convert("RGBA")
        px = im.load()
        n = 0
        for y in range(im.height):
            for x in range(im.width):
                r, g, b, a = px[x, y]
                if a and (w := farbe(r, g, b)) is not None:
                    v = round(w * 255)
                    px[x, y] = (v, v, v, a)
                    n += 1
        im.save(f)
        print("%-13s %d Pixel" % (p, n))
    print("Original in", KORB)


if __name__ == "__main__":
    main()
