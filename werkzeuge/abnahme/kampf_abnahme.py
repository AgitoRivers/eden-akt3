# -*- coding: utf-8 -*-
"""Abnahme-Boegen: je Gegner eine Zeile mit idle + Angriffsposen + weiteren Posen auf Schachbrett, Randmessung im Titel.
  kampf_abnahme.py Thief,Pirate,...  [--ziel name]"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

Q = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions\combat"
ZIEL = r"Y:\AI\mission-control\entwuerfe\kampf_ui_bilder"
POSEN = ["idle", "windup", "attack", "heavy_windup", "heavy_attack", "hurt", "enraged", "flee", "surrender", "defeated",
         "victory", "weakened"]
W, H, KOPF = 220, 320, 26


def rand(im, schwelle=24):
    a = im.getchannel("A")
    w, h = im.size
    r = {"L": sum(1 for y in range(0, h, 2) if a.getpixel((0, y)) > schwelle),
         "R": sum(1 for y in range(0, h, 2) if a.getpixel((w - 1, y)) > schwelle),
         "O": sum(1 for x in range(0, w, 2) if a.getpixel((x, 0)) > schwelle)}
    return {k: v for k, v in r.items() if v > 2}


def schach(w, h, g=20):
    b = Image.new("RGB", (w, h), (120, 120, 120))
    d = ImageDraw.Draw(b)
    for y in range(0, h, g):
        for x in range(0, w, g):
            if (x // g + y // g) % 2:
                d.rectangle((x, y, x + g - 1, y + g - 1), fill=(160, 160, 160))
    return b


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    namen = sys.argv[1].split(",")
    name = sys.argv[sys.argv.index("--ziel") + 1] if "--ziel" in sys.argv else "abnahme"
    f, fk = ImageFont.truetype("segoeui.ttf", 18), ImageFont.truetype("segoeui.ttf", 14)
    bogen = Image.new("RGB", (W * len(POSEN), (H + KOPF) * len(namen)), (14, 15, 19))
    d = ImageDraw.Draw(bogen)
    for r, n in enumerate(namen):
        y0 = r * (H + KOPF)
        d.text((4, y0 + 3), n, fill=(243, 238, 228), font=f)
        for i, p in enumerate(POSEN):
            pfad = os.path.join(Q, n, p + ".png")
            if not os.path.exists(pfad):
                d.text((i * W + 80, y0 + 5), p + " –", fill=(110, 110, 110), font=fk)
                continue
            im = Image.open(pfad).convert("RGBA")
            rr = rand(im)
            d.text((i * W + 80, y0 + 5), p + (" ✗" + "".join(rr) if rr else ""), fill=(217, 161, 152) if rr else (216, 189, 134), font=fk)
            if rr:
                print("%-14s %-13s Rand %s" % (n, p, rr))
            im.thumbnail((W - 6, H - 6))
            feld = schach(W - 4, H - 4)
            feld.paste(im, ((W - 4 - im.width) // 2, H - 4 - im.height), im)
            bogen.paste(feld, (i * W + 2, y0 + KOPF + 2))
    ziel = os.path.join(ZIEL, name + ".png")
    bogen.save(ziel)
    print(ziel)


if __name__ == "__main__":
    main()
