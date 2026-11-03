# -*- coding: utf-8 -*-
r"""Bibis Loewen-Anhaenger einheitlich schwarz (Duc 30.10.2026: "alle Loewen schwarz mit Gesicht"). Die freigegebenen Posen
bleiben: Nur der Ausschnitt um den Loewen wird vergroessert, innerhalb einer Maske neu erzeugt und weich zurueckgesetzt. Der
Alpha-Kanal bleibt. Die Vorlagen liegen danach in output\_expressions_papierkorb\combat.

    python bibi_loewe_schwarz.py [pose,pose]     ohne Angabe alle in BOXEN
"""
import os, random, shutil, sys, time

from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, r"X:\AI\Eden\werkzeuge")
import item_bilder as ib

C = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions\combat\Bibi"
KORB = r"X:\AI\ComfyUI_krea2\ComfyUI\output\_expressions_papierkorb\combat\bibi_vor_loewe_" + time.strftime("%Y%m%d_%H%M")
EINGABE = r"X:\AI\ComfyUI_krea2\ComfyUI\input"
TMP = os.path.join(os.environ["TEMP"], "bibi_loewe")
SEITE = 1024
PROMPT = ("Close-up photo of a small plush lion toy keychain hanging on a metal ring, the whole toy is jet black: black fur, "
          "black face, black muzzle, black nose, black paws, a fluffy black mane, small shiny black bead eyes, no white and "
          "no brown anywhere on the toy, soft flash light, photorealistic")
# Pose: Loewe im Vollbild (x0, y0, x1, y1), abgelesen aus dem Pruefbogen
BOXEN = {"idle": (352, 804, 466, 967), "windup": (268, 899, 396, 1053), "attack": (429, 855, 550, 1016),
         "hurt": (341, 723, 462, 862), "weakened": (290, 734, 392, 877), "enraged": (264, 877, 407, 1064),
         "flee": (194, 833, 308, 1002), "surrender": (246, 877, 363, 1005), "victory": (150, 804, 304, 1009),
         "defeated": (790, 545, 936, 682)}


def main():
    posen = sys.argv[1].split(",") if len(sys.argv) > 1 else list(BOXEN)
    os.makedirs(KORB, exist_ok=True)
    os.makedirs(TMP, exist_ok=True)
    ib.NSFW_PROFIL["loras"] = [("Krea_Real3.safetensors", 0.7)]
    plan, auftraege = {}, []
    for p in posen:
        f = os.path.join(C, p + ".png")
        shutil.copy2(f, os.path.join(KORB, p + ".png"))
        im = Image.open(f).convert("RGBA")
        x0, y0, x1, y1 = BOXEN[p]
        s = max(x1 - x0, y1 - y0) + 120
        cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
        ax = min(max(0, cx - s // 2), im.width - s)
        ay = min(max(0, cy - s // 2), im.height - s)
        crop = im.convert("RGB").crop((ax, ay, ax + s, ay + s))
        k = SEITE / s
        crop.resize((SEITE, SEITE), Image.LANCZOS).save(os.path.join(EINGABE, "bibi_l_%s.png" % p))
        m = Image.new("L", (SEITE, SEITE), 0)
        ImageDraw.Draw(m).ellipse(((x0 - ax - 14) * k, (y0 - ay - 14) * k, (x1 - ax + 14) * k, (y1 - ay + 14) * k), fill=255)
        m = m.filter(ImageFilter.GaussianBlur(16))
        m.save(os.path.join(EINGABE, "bibi_lm_%s.png" % p))
        plan[p] = (im, ax, ay, s, m)
        g = ib.graph(PROMPT, TMP, "l_" + p, random.randint(1, 2 ** 31), True)
        g["20"] = {"class_type": "LoadImage", "inputs": {"image": "bibi_l_%s.png" % p}}
        g["21"] = {"class_type": "LoadImageMask", "inputs": {"image": "bibi_lm_%s.png" % p, "channel": "red"}}
        g["22"] = {"class_type": "VAEEncode", "inputs": {"pixels": ["20", 0], "vae": ["3", 0]}}
        g["23"] = {"class_type": "SetLatentNoiseMask", "inputs": {"samples": ["22", 0], "mask": ["21", 0]}}
        del g["6"]
        g["7"]["inputs"]["latent_image"] = ["23", 0]
        auftraege.append((p, ib.post("/prompt", {"prompt": g})["prompt_id"]))
    ib.warten(auftraege, lambda v: print("fertig:", v))
    for p, (im, ax, ay, s, m) in plan.items():
        neu = Image.open(os.path.join(TMP, "l_%s.png" % p)).convert("RGB").resize((s, s), Image.LANCZOS)
        rgb = im.convert("RGB")
        rgb.paste(neu, (ax, ay), m.resize((s, s), Image.LANCZOS))
        rgb.putalpha(im.getchannel("A"))
        rgb.save(os.path.join(C, p + ".png"))
        os.remove(os.path.join(TMP, "l_%s.png" % p))
    print("Vorlagen in", KORB)


if __name__ == "__main__":
    main()
