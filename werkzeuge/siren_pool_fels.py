# -*- coding: utf-8 -*-
r"""Teich der Sirene mit kleinem Felsen (Duc 30.10.2026): Der Freisteller entfernt den gerenderten Stein unter Ligeia, also
kommt ein niedriger Felsen ins Hintergrundbild. Nur die Maskenflaeche wird neu erzeugt (SetLatentNoiseMask), der Rest des
Bildes bleibt pixelgenau. Das Original eden_rise_underground_pool_tide.png wird nicht angefasst: Die Flut-Nacht nutzt es weiter.

    python siren_pool_fels.py [Anzahl]     Varianten -> ST\backgrounds\_varianten\eden_rise_siren_pool_v1..n.png
"""
import os, random, shutil, sys

from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import item_bilder as ib

ST_BG = r"X:\AI\SillyTavern3\SillyTavern-Launcher\SillyTavern\data\default-user\backgrounds"
QUELLE = os.path.join(ST_BG, "eden_rise_underground_pool_tide.png")
VAR = os.path.join(ST_BG, "_varianten")
EINGABE = r"X:\AI\ComfyUI_krea2\ComfyUI\input"
BOX = (320, 680, 1000, 928)         # Felsen unten links der Mitte, dort sitzt Ligeia
PROMPT = ("Wide photograph of a dark sea cave at night, black still water lit by cold moonlight. In the lower middle of the "
          "frame a single low flat-topped boulder of black wet rock rises out of the water, its broad top smooth enough to "
          "sit on, glistening with the same wet highlights as the rocks around it, small ripples at its base, seamless "
          "with the cave, photorealistic, no people, no text")


def maske():
    m = Image.new("L", Image.open(QUELLE).size, 0)
    ImageDraw.Draw(m).ellipse((BOX[0], BOX[1], BOX[2], BOX[3] + 180), fill=255)
    return m.filter(ImageFilter.GaussianBlur(14))


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    os.makedirs(VAR, exist_ok=True)
    m = maske()
    shutil.copy2(QUELLE, os.path.join(EINGABE, "siren_pool_quelle.png"))
    m.save(os.path.join(EINGABE, "siren_pool_maske.png"))
    ib.NSFW_PROFIL["loras"] = [("Krea_Real3.safetensors", 0.7)]
    auftraege = []
    for k in range(1, n + 1):
        name = "eden_rise_siren_pool_roh_v%d" % k
        g = ib.graph(PROMPT, VAR, name, random.randint(1, 2 ** 31), True)
        g["20"] = {"class_type": "LoadImage", "inputs": {"image": "siren_pool_quelle.png"}}
        g["21"] = {"class_type": "LoadImageMask", "inputs": {"image": "siren_pool_maske.png", "channel": "red"}}
        g["22"] = {"class_type": "VAEEncode", "inputs": {"pixels": ["20", 0], "vae": ["3", 0]}}
        g["23"] = {"class_type": "SetLatentNoiseMask", "inputs": {"samples": ["22", 0], "mask": ["21", 0]}}
        del g["6"]
        g["7"]["inputs"]["latent_image"] = ["23", 0]
        auftraege.append((name, ib.post("/prompt", {"prompt": g})["prompt_id"]))
    ib.warten(auftraege, lambda v: print("fertig:", v))
    alt = Image.open(QUELLE).convert("RGB")
    for k in range(1, n + 1):
        roh = os.path.join(VAR, "eden_rise_siren_pool_roh_v%d.png" % k)
        neu = Image.open(roh).convert("RGB")
        if neu.size != alt.size:
            neu = neu.resize(alt.size, Image.LANCZOS)
        Image.composite(neu, alt, m).save(os.path.join(VAR, "eden_rise_siren_pool_v%d.png" % k))
        os.remove(roh)
    print("Varianten in", VAR)


if __name__ == "__main__":
    main()
