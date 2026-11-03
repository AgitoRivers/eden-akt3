# -*- coding: utf-8 -*-
r"""Korkeiche ohne Rinde aus dem Bild MIT Rinde rechnen (Duc 30.10.2026): beide Sprites muessen deckungsgleich sein, sonst springt der
ganze Baum beim Schaelen. Nur der untere Stamm wird rostrot, die Krone bleibt pixelgleich.

    python werkzeuge\kork_rinde_bild.py [baum]    <baum>.png (geschaelt) + <baum>_rinde.png (nur die Rinde, faellt im Minispiel)

Quelle bleibt <baum>_vorher.png. Ohne Angabe alle Korkeichen."""
import math, os, sys

import numpy as np
from PIL import Image, ImageFilter

HIER = os.path.dirname(os.path.abspath(__file__))
ORDNER = os.path.join(os.path.dirname(HIER), "module", "eden_rise", "farm", "abbau")
# je Baum: Oberkante der Schaelung (Pixel, knapp unter dem Astknoten), darunter bleiben die Wurzeln, wie sie sind
BAEUME = {"cork_oak": (398, 586), "cork_oak_2": (432, 562)}
ROST_HELL, ROST_DUNKEL = np.array([232, 126, 62.0]), np.array([120, 46, 20.0])


def rechnen(baum, OBEN, UNTEN):
    bild = Image.open(os.path.join(ORDNER, baum + "_vorher.png")).convert("RGBA")
    a = np.array(bild).astype(float)
    h, b = a.shape[:2]
    kante = np.array([OBEN + 7 * math.sin(x / 6.5) + 4 * math.sin(x / 2.3) for x in range(b)])
    yy = np.arange(h)[:, None]
    maske = (yy >= kante[None, :]) & (a[..., 3] > 40)
    # unten weich auslaufen, die Wurzeln behalten ihre Rinde
    auslauf = np.clip((UNTEN - yy) / 26.0, 0, 1) * np.ones((h, b))
    staerke = maske * auslauf
    # Helligkeit des Stamms geglaettet: die Rindenfurchen verschwinden, ein paar Laengsrillen bleiben
    hell = np.array(bild.convert("L").filter(ImageFilter.GaussianBlur(5))).astype(float) / 255
    fein = np.array(bild.convert("L").filter(ImageFilter.GaussianBlur(1.2))).astype(float) / 255
    # Stamm als Rundung: an den Raendern dunkler, in der Mitte hell
    rund = np.zeros((h, b))
    for y in range(h):
        xs = np.where(staerke[y] > 0)[0]
        if len(xs) > 2:
            rund[y, xs[0]:xs[-1] + 1] = 1 - np.abs(np.linspace(-1, 1, xs[-1] - xs[0] + 1))
    rund = np.array(Image.fromarray((rund * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3))).astype(float) / 255
    wert = np.clip(0.12 + 0.95 * rund ** 0.7 + 1.6 * (fein - hell), 0, 1)[..., None]
    rost = ROST_DUNKEL + (ROST_HELL - ROST_DUNKEL) * wert
    neu = a.copy()
    neu[..., :3] = a[..., :3] * (1 - staerke[..., None]) + rost * staerke[..., None]
    # dunkle Schnittkante unter der stehengebliebenen Rinde
    kantenband = maske & (yy < kante[None, :] + 4)
    neu[..., :3][kantenband] *= 0.55
    Image.fromarray(neu.astype(np.uint8)).save(os.path.join(ORDNER, baum + ".png"), optimize=True)
    rinde = np.zeros_like(a)
    rinde[..., :3] = a[..., :3]
    rinde[..., 3] = a[..., 3] * (staerke > 0.5)
    Image.fromarray(rinde.astype(np.uint8)).save(os.path.join(ORDNER, baum + "_rinde.png"), optimize=True)
    print("fertig: " + baum)


def main():
    for baum in sys.argv[1:] or BAEUME:
        rechnen(baum, *BAEUME[baum])


if __name__ == "__main__":
    main()
