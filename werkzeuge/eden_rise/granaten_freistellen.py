# -*- coding: utf-8 -*-
r"""Granaten freistellen fuer den Wurf (Duc 28.10.2026): das Item-Bild (Granate auf Stoff) wird mit RMBG-2.0 vom
Hintergrund getrennt, auf die Granate zugeschnitten und als kleine webp mit Alpha nach client\plugins\eden-combat\fx
gelegt (wurf_<item-id>.webp). Der Kampf laesst genau dieses Bild drehend im Bogen fliegen (eden-combat-effects.js).

    X:\AI\ComfyUI_windows_portable_0.5.1_v2\python_embeded\python.exe werkzeuge\eden_rise\granaten_freistellen.py

Braucht torch + transformers aus dieser ComfyUI-Installation; das Modell liegt dort unter models\rembg\RMBG-2.0."""
import os, sys
import torch
from PIL import Image
from torchvision import transforms
from transformers import AutoModelForImageSegmentation

EDEN = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
QUELLE = os.path.join(EDEN, "module", "eden_rise", "items", "_gross")
ZIEL = os.path.join(EDEN, "client", "plugins", "eden-combat", "fx")
MODELL = r"X:\AI\ComfyUI_windows_portable_0.5.1_v2\ComfyUI\models\rembg\RMBG-2.0"
GRANATEN = ["grenade_fire", "grenade_water", "grenade_shock", "grenade_flash", "grenade_concussion", "grenade_shrapnel", "grenade_sleep"]
HOEHE = 192          # Zielhoehe in px (fliegt mit ~64 px, doppelt fuer scharfe Kanten)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    geraet = "cuda" if torch.cuda.is_available() else "cpu"
    m = AutoModelForImageSegmentation.from_pretrained(MODELL, trust_remote_code=True).to(geraet).eval()
    vor = transforms.Compose([transforms.Resize((1024, 1024)), transforms.ToTensor(),
                              transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])
    for gid in GRANATEN:
        bild = Image.open(os.path.join(QUELLE, gid + ".png")).convert("RGB")
        with torch.no_grad():
            maske = m(vor(bild).unsqueeze(0).to(geraet))[-1].sigmoid().cpu()[0].squeeze()
        alpha = transforms.ToPILImage()(maske).resize(bild.size)
        alpha = alpha.point(lambda v: 0 if v < 24 else (255 if v > 232 else v))     # Stoffreste weg, Kante weich
        frei = bild.copy(); frei.putalpha(alpha)
        frei = frei.crop(alpha.getbbox())
        b = round(frei.width * HOEHE / frei.height)
        frei = frei.resize((b, HOEHE), Image.LANCZOS)
        aus = os.path.join(ZIEL, "wurf_%s.webp" % gid)
        frei.save(aus, "WEBP", quality=90, method=6)
        print("%s -> %s (%dx%d)" % (gid, os.path.basename(aus), b, HOEHE))


if __name__ == "__main__":
    main()
