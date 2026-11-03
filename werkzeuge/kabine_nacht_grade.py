# -*- coding: utf-8 -*-
r"""Nachtbild dunkler und waermer machen (25.10.2026, Duc: "kuschelig"). Reine Farbkorrektur, kein neuer Render.

    python kabine_nacht_grade.py 3        -> _varianten\eden_rise_duc_cabin_night_v3_warm.png + Vorher/Nachher-Bild
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ST_BG = r"X:\AI\SillyTavern3\SillyTavern-Launcher\SillyTavern\data\default-user\backgrounds"
VAR = os.path.join(ST_BG, "_varianten")
GAMMA = 1.18                    # > 1 = Mitteltoene dunkler
HELL = 0.86                     # Gesamthelligkeit
WARM = np.array([1.07, 0.98, 0.84])     # R, G, B multiplikativ (Weissabgleich-Charakter)
SAETTIGUNG = 1.08


def grade(img):
    a = np.asarray(img.convert("RGB"), dtype=np.float32) / 255.0
    a = np.power(a, GAMMA) * HELL * WARM
    grau = a.mean(axis=2, keepdims=True)
    a = grau + (a - grau) * SAETTIGUNG
    return Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8))


def main():
    k = sys.argv[1]
    quelle = Image.open(os.path.join(VAR, "eden_rise_duc_cabin_night_v%s.png" % k))
    neu = grade(quelle)
    ziel = os.path.join(VAR, "eden_rise_duc_cabin_night_v%s_warm.png" % k)
    neu.save(ziel)
    W, H = 832, 464
    bogen = Image.new("RGB", (W * 2 + 30, H + 20), (20, 20, 20))
    d = ImageDraw.Draw(bogen)
    font = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 40)
    for i, (b, text) in enumerate([(quelle, "vorher"), (neu, "nachher")]):
        x = 10 + i * (W + 10)
        bogen.paste(b.convert("RGB").resize((W, H), Image.LANCZOS), (x, 10))
        d.rectangle([x + 12, 22, x + 190, 76], fill=(0, 0, 0))
        d.text((x + 22, 22), text, fill=(255, 220, 120), font=font)
    bogen.save(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "abnahme",
                            "kabine_nacht_warm_vergleich.jpg"), quality=90)
    print("geschrieben:", ziel)


if __name__ == "__main__":
    main()
