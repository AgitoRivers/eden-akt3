# -*- coding: utf-8 -*-
"""Bogen: je Figur eine Zeile mit allen PNGs eines Unterordners (z. B. _probe, _test)."""
import os, sys
from PIL import Image, ImageDraw, ImageFont

E = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions"
ZIEL = r"Y:\AI\mission-control\entwuerfe\kampf_ui_bilder"


def main():
    namen, ordner, ziel = sys.argv[1].split(","), sys.argv[2], sys.argv[3]
    W, H, K = 300, 450, 26
    reihen = []
    for n in namen:
        d = os.path.join(E, n, ordner)
        reihen.append((n, sorted(f for f in os.listdir(d) if f.endswith(".png")) if os.path.isdir(d) else []))
    spalten = max(len(r[1]) for r in reihen) or 1
    bogen = Image.new("RGB", (W * spalten, (H + K) * len(reihen)), (14, 15, 19))
    dr = ImageDraw.Draw(bogen)
    f = ImageFont.truetype("segoeui.ttf", 16)
    for r, (n, dateien) in enumerate(reihen):
        y = r * (H + K)
        for i, datei in enumerate(dateien):
            dr.text((i * W + 6, y + 4), "%s · %s" % (n.replace("Yacht_", ""), datei[:-4]), fill=(216, 189, 134), font=f)
            im = Image.open(os.path.join(E, n, ordner, datei)).convert("RGBA")
            im.thumbnail((W - 6, H - 6))
            feld = Image.new("RGB", (W - 4, H - 4), (128, 128, 128))
            feld.paste(im, ((W - 4 - im.width) // 2, H - 4 - im.height), im)
            bogen.paste(feld, (i * W + 2, y + K + 2))
    bogen.save(os.path.join(ZIEL, ziel + ".png"))
    print(os.path.join(ZIEL, ziel + ".png"))


if __name__ == "__main__":
    main()
