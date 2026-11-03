# -*- coding: utf-8 -*-
r"""Pixel-Figuren der Taktik-Karte (Duc 31.10.2026, zwei Reihen seit 01.11.2026): schneidet ein Blatt mit 6 Bildern Stehen und 6 Bildern Laufen.

    python werkzeuge\eden_rise\taktik_figuren.py

Quelle: module/eden_rise/taktik/quellen/<name>.png (oben Stehen, unten Laufen).
Ziel: module/eden_rise/taktik/fig_<name>_stand.webp und fig_<name>.webp, alle Bilder nebeneinander, dazu figuren.json fuer taktik_eden_rise.py.
Die KI-Blaetter haben einen farbigen Saum ausserhalb der schwarzen Kontur, und die Figuren stehen nicht im gleichen Raster.
"""
import glob
import json
import os
from collections import deque

import numpy as np
from PIL import Image

BASIS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ORDNER = os.path.join(BASIS, "module", "eden_rise", "taktik")
ZIEL_HOEHE = 192                                    # scharf bis weit ueber 1440p, im Spiel rund 36 bis 68 px hoch
HOEHE_BASIS, FIGUR_HOCH = 175, 340                  # eine Figur von 340 px im Blatt steht mit 175 % der Feldhoehe auf der Karte
FIGUR_FLAECHE = 1500                                # ab hier ist es eine Figur, kleinere Stuecke (Flamme, Rotor, Dose) gehoeren zur naechsten


def saum_weg(rgba):
    """Schaelt von aussen alles ab, was nicht zur schwarzen Kontur gehoert."""
    a = rgba[..., 3] > 128
    hell = rgba[..., :3].max(axis=2) > 48
    for _ in range(8):
        rand = a & ~(np.roll(a, 1, 0) & np.roll(a, -1, 0) & np.roll(a, 1, 1) & np.roll(a, -1, 1))
        weg = rand & hell
        if not weg.any():
            break
        a &= ~weg
    return a


def stuecke(maske, mindest):
    """Zusammenhaengende Flaechen, von links nach rechts."""
    h, w = maske.shape
    gesehen = np.zeros_like(maske)
    aus = []
    for y0, x0 in zip(*np.nonzero(maske)):
        if gesehen[y0, x0]:
            continue
        q, ys, xs = deque([(y0, x0)]), [], []
        gesehen[y0, x0] = True
        while q:
            y, x = q.popleft()
            ys.append(y)
            xs.append(x)
            for b, a in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                if 0 <= b < h and 0 <= a < w and maske[b, a] and not gesehen[b, a]:
                    gesehen[b, a] = True
                    q.append((b, a))
        if len(ys) >= mindest:
            aus.append((np.array(ys), np.array(xs)))
    return sorted(aus, key=lambda s: s[1].min())


def figuren(maske):
    """Die Figuren eines Blatts. Kleine Stuecke kommen zur Figur, deren Rand ihnen am naechsten liegt."""
    alle = stuecke(maske, 20)
    gross = [s for s in alle if len(s[0]) >= FIGUR_FLAECHE]
    teile = [[s] for s in gross]
    for s in alle:
        if len(s[0]) >= FIGUR_FLAECHE:
            continue
        cy, cx = s[0].mean(), s[1].mean()
        i = min(range(len(gross)), key=lambda k: max(gross[k][1].min() - cx, 0, cx - gross[k][1].max()) + max(gross[k][0].min() - cy, 0, cy - gross[k][0].max()))
        teile[i].append(s)
    return [(np.concatenate([s[0] for s in t]), np.concatenate([s[1] for s in t])) for t in teile]


def streifen(rgba, teile, ziel):
    """Legt die Bilder einer Reihe auf Fuesse und Mitte genau uebereinander. Die Mitte ist der Median der Figur, Waffen verschieben sie kaum."""
    bilder = []
    for ys, xs in teile:
        bild = np.zeros_like(rgba)
        bild[ys, xs] = rgba[ys, xs]
        bild[ys, xs, 3] = 255
        bilder.append((bild, int(np.median(xs)), int(np.percentile(ys, 99.5)), int(ys.min()), int(ys.max()), int(xs.min()), int(xs.max())))
    links = rechts = max(max(b[1] - b[5], b[6] - b[1]) for b in bilder)
    ueber = max(b[2] - b[3] for b in bilder)
    unter = max(b[4] - b[2] for b in bilder)
    breit, hoehe = links + rechts + 1 + 4, ueber + unter + 1 + 2
    bahn = Image.new("RGBA", (breit * len(bilder), hoehe))
    for i, (bild, mitte, fuss, *_) in enumerate(bilder):
        bahn.paste(Image.fromarray(bild).crop((mitte - links - 2, fuss - ueber - 1, mitte - links - 2 + breit, fuss + unter + 2)), (i * breit, 0))
    faktor = ZIEL_HOEHE / hoehe
    fertig = bahn.resize((round(breit * faktor) * len(bilder), ZIEL_HOEHE), Image.LANCZOS)
    fertig.save(ziel, "WEBP", lossless=True)
    return {"bild": os.path.basename(ziel), "bilder": len(bilder), "seite": round(round(breit * faktor) / ZIEL_HOEHE, 4), "hoehe": round(HOEHE_BASIS * hoehe / FIGUR_HOCH)}


def blatt(name):
    rgba = np.array(Image.open(os.path.join(ORDNER, "quellen", name + ".png")).convert("RGBA"))
    teile = figuren(saum_weg(rgba))
    assert len(teile) == 12, (name, "Figuren gefunden", len(teile), "erwartet 12")
    mitte = rgba.shape[0] / 2
    oben = sorted((t for t in teile if t[0].mean() < mitte), key=lambda t: t[1].min())
    unten = sorted((t for t in teile if t[0].mean() >= mitte), key=lambda t: t[1].min())
    assert len(oben) == 6 and len(unten) == 6, (name, len(oben), len(unten))
    lauf = streifen(rgba, unten, os.path.join(ORDNER, "fig_%s.webp" % name))
    lauf["stand"] = streifen(rgba, oben, os.path.join(ORDNER, "fig_%s_stand.webp" % name))
    print(name, "Laufen", lauf["seite"], lauf["hoehe"], "Stehen", lauf["stand"]["seite"], lauf["stand"]["hoehe"])
    return lauf


if __name__ == "__main__":
    tabelle = {os.path.splitext(os.path.basename(p))[0]: None for p in sorted(glob.glob(os.path.join(ORDNER, "quellen", "*.png")))}
    for n in tabelle:
        tabelle[n] = blatt(n)
    json.dump(tabelle, open(os.path.join(ORDNER, "figuren.json"), "w", encoding="utf-8"), indent=1)
