# -*- coding: utf-8 -*-
r"""Teich der Sirene: Mondlicht von oben (Duc 30.10.2026). Der Riss in der Decke steht schon im Kanon (lg_drei: "the crack in
the roof where the moon comes through"). Neu erzeugt wird nur die Spalte ueber dem Felsen; danach ein weicher Lichtkegel auf dem
Stein per Bildbearbeitung. Quelle ist Felsen-Variante 3, das Original der Flut-Nacht bleibt.

    python siren_pool_mond.py [Anzahl]     -> ST\backgrounds\_varianten\eden_rise_siren_pool_mond_v1..n.png
"""
import os, random, shutil, sys

from PIL import Image, ImageChops, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import item_bilder as ib

ST_BG = r"X:\AI\SillyTavern3\SillyTavern-Launcher\SillyTavern\data\default-user\backgrounds"
VAR = os.path.join(ST_BG, "_varianten")
QUELLE = os.path.join(VAR, "eden_rise_siren_pool_v3.png")
EINGABE = r"X:\AI\ComfyUI_krea2\ComfyUI\input"
BOX = (400, 0, 780, 690)            # Spalte ueber dem Felsen; die Hoehlenoeffnung rechts bleibt
KEGEL = [(585, 0), (455, 760), (820, 760)]
PROMPT = ("Wide photograph inside a dark sea cave at night. High in the black rock ceiling there is a narrow jagged crack open "
          "to the night sky, and a single soft shaft of cold silver moonlight falls straight down from it through the dark "
          "air, faint mist in the beam, black wet rock walls, photorealistic, no people, no text")


def maske():
    m = Image.new("L", Image.open(QUELLE).size, 0)
    ImageDraw.Draw(m).rectangle(BOX, fill=255)
    return m.filter(ImageFilter.GaussianBlur(26))


def kegel(bild):
    """Kaltes Licht auf Felsen und Luft: aufhellen nur unter dem Riss, nach unten breiter und weicher."""
    m = Image.new("L", bild.size, 0)
    ImageDraw.Draw(m).polygon(KEGEL, fill=70)
    m = m.filter(ImageFilter.GaussianBlur(38))
    licht = Image.merge("RGB", [m.point(lambda v, f=f: round(v * f)) for f in (0.82, 0.92, 1.0)])
    return ImageChops.screen(bild, licht)


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    m = maske()
    shutil.copy2(QUELLE, os.path.join(EINGABE, "siren_pool_mond_quelle.png"))
    m.save(os.path.join(EINGABE, "siren_pool_mond_maske.png"))
    ib.NSFW_PROFIL["loras"] = [("Krea_Real3.safetensors", 0.7)]
    auftraege = []
    for k in range(1, n + 1):
        name = "eden_rise_siren_pool_mond_roh_v%d" % k
        g = ib.graph(PROMPT, VAR, name, random.randint(1, 2 ** 31), True)
        g["20"] = {"class_type": "LoadImage", "inputs": {"image": "siren_pool_mond_quelle.png"}}
        g["21"] = {"class_type": "LoadImageMask", "inputs": {"image": "siren_pool_mond_maske.png", "channel": "red"}}
        g["22"] = {"class_type": "VAEEncode", "inputs": {"pixels": ["20", 0], "vae": ["3", 0]}}
        g["23"] = {"class_type": "SetLatentNoiseMask", "inputs": {"samples": ["22", 0], "mask": ["21", 0]}}
        del g["6"]
        g["7"]["inputs"]["latent_image"] = ["23", 0]
        auftraege.append((name, ib.post("/prompt", {"prompt": g})["prompt_id"]))
    ib.warten(auftraege, lambda v: print("fertig:", v))
    alt = Image.open(QUELLE).convert("RGB")
    for k in range(1, n + 1):
        roh = os.path.join(VAR, "eden_rise_siren_pool_mond_roh_v%d.png" % k)
        neu = Image.open(roh).convert("RGB")
        if neu.size != alt.size:
            neu = neu.resize(alt.size, Image.LANCZOS)
        kegel(Image.composite(neu, alt, m)).save(os.path.join(VAR, "eden_rise_siren_pool_mond_v%d.png" % k))
        os.remove(roh)
    print("Varianten in", VAR)


if __name__ == "__main__":
    main()
