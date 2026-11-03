# -*- coding: utf-8 -*-
r"""Granaten-Einschlaege (Duc 27.10.2026): echte EmberGen-/LiquiGen-Bildfolgen aus dem Effektlabor spielfertig machen.

    python werkzeuge\eden_rise\granaten_fx.py

Quelle: docs\effekt-auswahl\status-labor\assets (bleibt unveraendert). Ziel: client\plugins\eden-combat\fx\<name>.webp
(Bildbogen, Zeilen von links nach rechts) und fx.json mit Spalten, Zeilen, Bildern und Zellgroesse - das liest
eden-combat-effects.js. Die Laborboegen sind bis 17 MB gross; hier werden Zellen verkleinert und leere Bilder entfernt."""
import json, os, sys
from PIL import Image

EDEN = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LAB = os.path.join(EDEN, "docs", "effekt-auswahl", "status-labor", "assets")
ZIEL = os.path.join(EDEN, "client", "plugins", "eden-combat", "fx")

# name: (Quelle, Spalten, Zeilen, Zielzelle, jedes n-te Bild, Grau[, (erstes, letztes+1 Bild)])
JANGA = "../quellen/granaten-jangafx-20261027/"                           # Ducs JangaFX-Exporte 27.10. (8x8 a 512 px)
BOEGEN = {
    "explosion": ("berserker-v2/explosion.png", 8, 8, 240, 1, False),     # EmberGen: Feuerball -> Rauch
    "druckstoss": ("druckstoss.png", 4, 4, 320, 1, False),                # EmberGen: Knall mit Funken -> Rauchpilz
    "brand": ("feuer.png", 8, 8, 192, 2, False),                          # Nachbrennen am Boden
    "fontaene": ("native-v6/ausbruch.png", 8, 8, 256, 1, False),          # LiquiGen: Wasserausbruch
    "strom": ("strom.png", 8, 8, 192, 2, False),
    "staub": ("staub_frei.png", 8, 8, 192, 2, False),
    "ring": ("omerta-shockwave-gold-v1.png", 8, 8, 256, 1, True),         # Druckwelle, entfaerbt (Farbe gibt der Code)
    "feuerball": (JANGA + "aerial-explosion-2/aerial_explosion_2_render_all.png", 8, 8, 256, 1, False),       # Feuerball -> Rauch
    "bodenexplosion": (JANGA + "artillery-explosion-1/artillery_explosion_1_render_all.png", 8, 8, 256, 1, False),  # Kuppel -> Staubpilz
    # press-splash verworfen (28.10.): Pressplatte sichtbar, Strahl am Zellrand abgeschnitten -> Wasser bleibt bei "fontaene"
    "rauchring": (JANGA + "smoke-shockwave-2/smoke_shockwave_2_render_all.png", 8, 8, 256, 1, True),          # Rauchring, entfaerbt
    # Ducs LiquiGen-Export 28.10.: Wasserball faellt, platzt am Boden, breitet sich aus; ab dem Aufprall (Bild 12),
    # die Granate selbst ist der fallende Ball
    "wasserball": (JANGA + "wasserball-boden/wasserball-boden-flipbook.png", 8, 8, 320, 1, False, (12, 64)),
}
# nur ein Ausschnitt jeder Zelle (links, oben, rechts, unten in Quellpixeln): der Wasserball nutzt nur die obere Haelfte,
# der unsichtbare Boden liegt bei y ~ 277 von 512
SCHNITT = {"wasserball": (0, 0, 512, 288)}
EINZEL = {"flare": ("realismus-v3/kenney-flare_01.png", 256), "spur": ("realismus-v3/kenney-trace_04.png", 192)}


def grau(im):
    a = im.getchannel("A")
    g = im.convert("L").point(lambda v: min(255, int(v * 1.25)))
    return Image.merge("RGBA", (g, g, g, a))


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    os.makedirs(ZIEL, exist_ok=True)
    meta = {}
    for name, (quelle, sp, ze, zelle, schritt, entfaerben, *bereich) in BOEGEN.items():
        im = Image.open(os.path.join(LAB, quelle)).convert("RGBA")
        cw, ch = im.width // sp, im.height // ze
        s = SCHNITT.get(name, (0, 0, cw, ch))
        h = round(zelle * (s[3] - s[1]) / (s[2] - s[0]))
        bilder = []
        von, bis = bereich[0] if bereich else (0, sp * ze)
        for i in range(von, bis, schritt):
            x, y = i % sp * cw, i // sp * ch
            b = im.crop((x + s[0], y + s[1], x + s[2], y + s[3]))
            if not b.getchannel("A").getbbox():
                continue                                                     # leeres Bild (vor dem Knall / nach dem Rauch)
            b = b.resize((zelle, h), Image.LANCZOS)
            bilder.append(grau(b) if entfaerben else b)
        spalten = 8
        zeilen = (len(bilder) + spalten - 1) // spalten
        bogen = Image.new("RGBA", (spalten * zelle, zeilen * h), (0, 0, 0, 0))
        for i, b in enumerate(bilder):
            bogen.paste(b, (i % spalten * zelle, i // spalten * h))
        pfad = os.path.join(ZIEL, name + ".webp")
        bogen.save(pfad, "WEBP", quality=82, method=6)
        meta[name] = {"spalten": spalten, "zeilen": zeilen, "bilder": len(bilder), "w": zelle, "h": h, "quelle": quelle}
        print("%-10s %2d Bilder  %dx%d  %4d KB" % (name, len(bilder), bogen.width, bogen.height, os.path.getsize(pfad) // 1024))
    for name, (quelle, groesse) in EINZEL.items():
        im = Image.open(os.path.join(LAB, quelle)).convert("RGBA").resize((groesse, groesse), Image.LANCZOS)
        pfad = os.path.join(ZIEL, name + ".webp")
        im.save(pfad, "WEBP", quality=85, method=6)
        meta[name] = {"spalten": 1, "zeilen": 1, "bilder": 1, "w": groesse, "h": groesse, "quelle": quelle}
        print("%-10s einzeln  %4d KB" % (name, os.path.getsize(pfad) // 1024))
    json.dump(meta, open(os.path.join(ZIEL, "fx.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
