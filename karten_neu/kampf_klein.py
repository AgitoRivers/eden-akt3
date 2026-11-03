# -*- coding: utf-8 -*-
r"""Kampf-Sprites kleiner Tiere nachtraeglich verkleinern, damit die Proportionen zu den Menschen stimmen
(19.10.2026, Duc). Das Bild behaelt seine Leinwandgroesse; die Figur wird um den Faktor kleiner und bleibt unten
auf ihrer Standlinie, mittig unter ihrer alten Position. Das Original wandert nach <Gegner>\_gross\.
Bereits verkleinerte Dateien stehen in <Gegner>\_verkleinert.json und werden nicht doppelt verkleinert -
das Skript kann also nach jedem neuen Lauf erneut aufgerufen werden.

    kampf_klein.py          Probelauf
    kampf_klein.py --los    verkleinert
"""
import io, json, os, shutil, sys
from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
LOS = "--los" in sys.argv
E = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions\combat"
FAKTOR = {"Seagull": 0.5, "Pigeon": 0.4, "Bat": 0.5, "Rat": 0.4,
          "WildschweinKlein": 0.5, "Wildschwein": 0.7, "WildschweinKeiler": 0.85,
          "RatAlpha": 0.55, "SeagullAlpha": 0.65, "PigeonAlpha": 0.5, "BatAlpha": 0.6}   # Wildschwein: Duc 22.10.

for name, f in FAKTOR.items():
    d = os.path.join(E, name)
    if not os.path.isdir(d):
        print("%-8s fehlt noch" % name)
        continue
    mark = os.path.join(d, "_verkleinert.json")
    erledigt = json.load(open(mark, encoding="utf-8")) if os.path.exists(mark) else {}
    neu = [x for x in sorted(os.listdir(d)) if x.lower().endswith(".png") and x not in erledigt]
    print("%-8s Faktor %.2f | neu zu verkleinern: %s" % (name, f, ", ".join(neu) or "-"))
    if not LOS:
        continue
    os.makedirs(os.path.join(d, "_gross"), exist_ok=True)
    for x in neu:
        p = os.path.join(d, x)
        shutil.copy2(p, os.path.join(d, "_gross", x))
        im = Image.open(p).convert("RGBA")
        bb = im.getchannel("A").getbbox()
        if not bb:
            continue
        fig = im.crop(bb)
        fig = fig.resize((max(1, int(fig.width * f)), max(1, int(fig.height * f))), Image.LANCZOS)
        mitte = (bb[0] + bb[2]) // 2
        neu_bild = Image.new("RGBA", im.size, (0, 0, 0, 0))
        neu_bild.paste(fig, (mitte - fig.width // 2, bb[3] - fig.height), fig)
        neu_bild.save(p)
        erledigt[x] = f
    json.dump(erledigt, open(mark, "w", encoding="utf-8"), indent=1)
print("verkleinert" if LOS else "PROBELAUF")
