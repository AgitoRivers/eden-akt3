# -*- coding: utf-8 -*-
r"""Ducs Schlag-Animation in den Kampf holen (Duc 03.11.2026).

Duc hat je Jacke x Waffe sechs Bilder einer Schlagbewegung geliefert (vom Ausholen bis zum Durchschwung), 512 x 512,
transparent, Ordner je Kampf-Sprite (DucErdeBat, ...). Der Kampf zeigt Duc aber als 1053 x 900 grosses Bild mit den
Fuessen auf Hoehe 882. Dieses Werkzeug bringt jede Folge auf denselben Massstab wie die vorhandenen Posen:

- Ein Massstab je Folge (die sechs Bilder sind zusammen erzeugt, sie passen untereinander). Er kommt aus dem Vergleich
  der letzten Bildes mit der Pose heavy_attack, und wenn das erste Bild nicht am Rand klebt, auch aus dem ersten Bild
  mit heavy_windup (Mittelwert).
- Die Fuesse stehen auf der Bodenlinie der Posen (882), waagerecht steht der Koerper wie in heavy_attack.

- Farbe (Duc 03.11.2026: "Kontrast und Schwarzpunkt anpassen"): Die gelieferten Bilder hatten angehobenes Schwarz,
  hellere Mitten und weniger Saettigung als die Posen. Je Folge eine Kurve pro Farbkanal, die die Verteilung der
  sechs Bilder auf die der vier Posen (idle, attack, heavy_windup, heavy_attack) legt (Quantile, nur deckende Pixel).
  Dieselbe Kurve fuer alle sechs Bilder, damit nichts flackert. --ohne-farbe schaltet es ab.

Ergebnis: module/eden_rise/kampf/<Sprite>/schwung_a.webp ... schwung_f.webp. Der Client spielt sie bei "Attack" und
beim Konter nach einer perfekten Parade ab (eden-combat.js, SCHWUNG_MS), der Server meldet sie in duc_bilder.

    python werkzeuge\kampf_schwung.py S:\VR\Gallery\Downloads\eden-duc-heavy-20261103-v1
    python werkzeuge\kampf_schwung.py <ordner> --nur DucErdeBat --vorschau     (Kontaktbogen nach docs/abnahme/kampf_schwung/)
"""
import argparse, os, sys
import numpy as np
from PIL import Image

BASIS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KAMPF = os.path.join(BASIS, "module", "eden_rise", "kampf")
NAMEN = ["schwung_%s" % c for c in "abcdef"]
ALPHA = 40


def box(im):
    return im.getchannel("A").point(lambda a: 255 if a > ALPHA else 0).getbbox()


def massstab(frames, windup, attack):
    """One scale per set: last frame vs heavy_attack, first frame vs heavy_windup if it does not touch the edge."""
    f6, oa = box(frames[-1]), box(attack)
    werte = [(oa[3] - oa[1]) / float(f6[3] - f6[1])]
    f1, ow = box(frames[0]), box(windup)
    if f1[1] > 2 and f1[3] < frames[0].height - 2:
        werte.append((ow[3] - ow[1]) / float(f1[3] - f1[1]))
    return sum(werte) / len(werte), werte


def setzen(frames, ziel_gr, s, attack):
    """All frames with the same scale; feet of the last frame on the pose baseline, centre like heavy_attack."""
    oa, f6 = box(attack), box(frames[-1])
    boden, mitte = oa[3], (oa[0] + oa[2]) / 2.0
    dx = mitte - s * (f6[0] + f6[2]) / 2.0
    dy = boden - s * f6[3]
    out = []
    for f in frames:
        g = f.resize((round(f.width * s), round(f.height * s)), Image.LANCZOS)
        leer = Image.new("RGBA", ziel_gr, (0, 0, 0, 0))
        leer.paste(g, (round(dx), round(dy)), g)          # paste also takes offsets outside the canvas
        out.append(leer)
    return out


DECKT = 200
REFERENZ = ("idle", "attack", "heavy_windup", "heavy_attack")


def _pixel(bilder):
    return np.concatenate([np.asarray(b)[..., :3][np.asarray(b)[..., 3] > DECKT] for b in bilder])


def farbkurven(frames, posen):
    """One monotone curve per channel: quantiles of the frames -> quantiles of the poses."""
    q = np.linspace(0, 100, 201)
    quelle, ziel = _pixel(frames).astype(float), _pixel(posen).astype(float)
    kurven = []
    for c in range(3):
        x, y = np.percentile(quelle[:, c], q), np.percentile(ziel[:, c], q)
        x = np.maximum.accumulate(x + np.arange(len(x)) * 1e-6)          # strictly rising for interp
        kurven.append(np.clip(np.round(np.interp(np.arange(256), x, y)), 0, 255).astype(np.uint8).tolist())
    return kurven


def farbe_anwenden(im, kurven):
    r, g, b, a = im.split()
    return Image.merge("RGBA", (r.point(kurven[0]), g.point(kurven[1]), b.point(kurven[2]), a))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("quelle")
    ap.add_argument("--nur", nargs="*")
    ap.add_argument("--vorschau", action="store_true")
    ap.add_argument("--ohne-farbe", action="store_true")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    sets = sorted(d for d in os.listdir(a.quelle) if d.startswith("Duc") and os.path.isdir(os.path.join(a.quelle, d)))
    if a.nur:
        sets = [d for d in sets if d in a.nur]
    bogen = []
    for name in sets:
        q, z = os.path.join(a.quelle, name), os.path.join(KAMPF, name)
        if not os.path.isdir(z):
            print("FEHLT im Spiel:", name)
            continue
        frames = [Image.open(os.path.join(q, "frame-%02d.png" % i)).convert("RGBA") for i in range(1, 7)]
        windup = Image.open(os.path.join(z, "heavy_windup.webp")).convert("RGBA")
        attack = Image.open(os.path.join(z, "heavy_attack.webp")).convert("RGBA")
        s, werte = massstab(frames, windup, attack)
        fertig = setzen(frames, attack.size, s, attack)
        roh_e = fertig[4]
        if not a.ohne_farbe:
            posen = [Image.open(os.path.join(z, p + ".webp")).convert("RGBA") for p in REFERENZ]
            kurven = farbkurven(fertig, posen)
            fertig = [farbe_anwenden(im, kurven) for im in fertig]
        for n, im in zip(NAMEN, fertig):
            im.save(os.path.join(z, n + ".webp"), "WEBP", quality=88, method=6)
        print("%-16s Massstab %.3f (%s)" % (name, s, ", ".join("%.3f" % w for w in werte)))
        if a.vorschau:
            bogen.append((name, [Image.open(os.path.join(z, "idle.webp")).convert("RGBA")] + fertig))
            bogen.append((name + "_farbe", [attack, roh_e, fertig[4]]))     # Pose · Bild e vorher · nachher
    if bogen:
        ziel = os.path.join(BASIS, "docs", "abnahme", "kampf_schwung")
        os.makedirs(ziel, exist_ok=True)
        for name, bilder in bogen:
            w, h = bilder[0].size
            b = Image.new("RGB", (w * len(bilder) // 3, h // 3), (24, 26, 32))
            for i, im in enumerate(bilder):
                k = im.resize((w // 3, h // 3), Image.LANCZOS)
                b.paste(k, (i * w // 3, 0), k)
            b.save(os.path.join(ziel, name + ".jpg"), quality=85)
        print("Kontaktboegen:", ziel)


if __name__ == "__main__":
    main()
