# -*- coding: utf-8 -*-
r"""Ligeia-Sprites fuer den Teich nachbearbeiten (Duc 30.10.2026). BEN2 laesst vom gerenderten Felsen einen blassen Schatten
stehen; der fliegt raus, damit die Figur zugeschnitten werden kann. Die Buehne setzt jede Figur mittig, der Felsen im Bild
eden_rise_siren_pool.png liegt aber links davon: Der Rand rechts schiebt sie auf den Stein. Die Buehne zeigt jedes Sprite fast
bildschirmhoch (index.html .fig): Rand oben und unten halten sie klein genug fuer den Stein. Licht an das Mondlicht angleichen.

    ligeia_freistellen.py QUELLE ZIEL [--ohne-licht]
"""
import sys

from PIL import Image, ImageEnhance

SCHIEBEN = 0.18       # Anteil der Figurenbreite, um den sie links vom Mittelpunkt des Bildes sitzt
FIGUR, UNTEN = 0.777, 0.0565  # Anteil der Spritehoehe: Figur und Rand unten (.fig ragt 4vh unter den Bildschirm)
HELL, FARBE = 0.72, 0.86
KUEHL = (0.93, 0.97, 1.06)


def bearbeiten(im, licht=True):
    im = im.convert("RGBA")
    a = im.getchannel("A").point(lambda v: 0 if v < 110 else (255 if v > 170 else round((v - 110) * 255 / 60)))
    im.putalpha(a)
    im = im.crop(a.getbbox())
    if licht:
        rgb = ImageEnhance.Color(ImageEnhance.Brightness(im.convert("RGB")).enhance(HELL)).enhance(FARBE)
        r, g, b = rgb.split()
        rgb = Image.merge("RGB", [k.point(lambda v, f=f: min(255, round(v * f))) for k, f in zip((r, g, b), KUEHL)])
        rgb.putalpha(im.getchannel("A"))
        im = rgb
    w = round(im.width * SCHIEBEN)
    h = round(im.height / FIGUR)
    neu = Image.new("RGBA", (im.width + w * 2, h), (0, 0, 0, 0))
    neu.paste(im, (w * 2, h - im.height - round(h * UNTEN)))
    return neu


if __name__ == "__main__":
    bearbeiten(Image.open(sys.argv[1]), "--ohne-licht" not in sys.argv).save(sys.argv[2])
    print(sys.argv[2])
