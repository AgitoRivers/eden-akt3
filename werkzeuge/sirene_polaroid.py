# -*- coding: utf-8 -*-
r"""Polaroids der Flaschenpost (Duc 30.10.2026): jede Vertrauensstufe 2-5 und der Dank der Kette bringen zwei Bilder, eine Szene aus
ihrer Welt mit handschriftlicher Zeile und ein Selfie von ihr ohne Kamera. Rahmen und Schrift kommen hier dazu, nicht aus Krea,
das Schrift nicht kann. Duc will die Inhalte nicht vorab sehen: Die Bilder prueft die Hauptsitzung.

    python sirene_polaroid.py rendern 2 [sirene_t2,...]      Varianten -> %TEMP%\sirene_polaroid (bogen.jpg)
    python sirene_polaroid.py waehlen sirene_t2 SZENE SELFIE setzt beide nach module\eden_rise\favours\fv_sirene_t2.webp
"""
import os, random, re, sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "eden_rise"))
import item_bilder as ib

TMP = os.path.join(os.environ["TEMP"], "sirene_polaroid")
ZIEL = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "module", "eden_rise", "favours")
SCHRIFT = r"C:\Windows\Fonts\Inkfree.ttf"
STIL = (" Instant film snapshot, cold washed-out colours, a little crooked, soft focus, amateur photo, fills the whole image, "
        "no border, no text, no people")
# id: (Szene, Zeile Szene, Zeile Selfie)
BILDER = {
    "sirene": ("Taken underwater at night, the bow of a sunken wooden sailing ship on the sea bed seen from below, covered in weed, "
               "a shaft of pale moonlight through dark green water, small silver fish around it.", "here the sea keeps what it loves,\nand does not ask it to wake.",
               "no lamp has found this room.\nI come here to be forgotten, and fail."),
    "sirene_t2": ("Taken from underwater looking straight up, the moon seen through a narrow jagged crack in a black rock cave roof, "
                  "the surface of the water silver and rippling.", "the moon, as the drowned see her:\na coin no one can spend.",
                  "the old ones still know my name.\nthey sing it slower than you would."),
    "sirene_t3": ("Three black wet rocks in a row rising from a flat low-tide sea at dusk, seen from the water, seaweed on them, grey "
                  "pink sky, nobody around.", "two of us sleep. one stone waits.\nthe tide reads it every night.",
                  "I have sung worse storms than this\nto sleep, and never once been thanked."),
    "sirene_t4": ("Close-up of a wet open palm in moonlight holding a small empty silver pearl setting on a thin dark leather cord, "
                  "black water behind, only the hand in the picture.", "a hollow keeps its shape\nlonger than what it held.",
                  "where the sun has never been\nthe small things make their own."),
    "sirene_t5": ("A long emerald fish tail fin breaking the surface of a flat dark sea at first light, far from any shore, drops of "
                  "water flying from it, pale horizon.", "past your lamps the dark is kind.\nit does not need you to see.",
                  "and still they come when I call.\nthis once, I only called to watch."),
}
PAPIER, TISCH, TINTE = (238, 233, 220), (22, 26, 30), (32, 40, 62)


ARM = ("A single thick orange octopus arm with pale round suckers, curling, isolated on a plain pure white background, nothing else "
       "in the picture, studio photo, sharp, photorealistic")
OHNE_ARM = re.compile(r",? ?a separate thick orange octopus arm.*?her body,")


def arm_rendern(n):
    os.makedirs(TMP, exist_ok=True)
    ib.NSFW_PROFIL["loras"] = [("Krea_Real3.safetensors", 0.7)]
    auf = []
    for k in range(1, n + 1):
        g = ib.graph(ARM, TMP, "arm_%d" % k, random.randint(1, 2 ** 31), True)
        g["6"]["inputs"].update({"width": 1024, "height": 1024})
        auf.append((str(k), ib.post("/prompt", {"prompt": g})["prompt_id"]))
    ib.warten(auf, lambda v: None)


def arm_setzen(bild, k, links):
    """Arm freistellen (weisser Grund), leicht unscharf wie nah an der Kamera, an den Bildrand. Die Haelfte ragt aus dem Bild."""
    a = np.asarray(Image.open(os.path.join(TMP, "arm_%s.png" % k)).convert("RGB")).astype(float)
    alpha = np.clip((245 - a.min(axis=2)) * 8, 0, 255)
    inseln, m = ndimage.label(alpha > 40)
    g = ndimage.sum(alpha > 40, inseln, range(1, m + 1))
    alpha = alpha * (inseln == (np.argmax(g) + 1))
    arm = Image.open(os.path.join(TMP, "arm_%s.png" % k)).convert("RGB")
    arm.putalpha(Image.fromarray(alpha.astype("uint8")).filter(ImageFilter.GaussianBlur(1.5)))
    arm = arm.crop(arm.getchannel("A").getbbox()).filter(ImageFilter.GaussianBlur(2.5))
    w, h = bild.size
    f = 0.40 * h / max(arm.size)
    arm = arm.resize((round(arm.width * f), round(arm.height * f)), Image.LANCZOS)
    if links:
        arm = arm.transpose(Image.FLIP_LEFT_RIGHT)
    x = -arm.width // 2 if links else w - arm.width // 2
    o = bild.convert("RGBA")
    o.paste(arm, (x, h - arm.height + arm.height // 4), arm)
    return o.convert("RGB")


def rendern(n, ids):
    os.makedirs(TMP, exist_ok=True)
    ib.NSFW_PROFIL["loras"] = [("Krea_Real3.safetensors", 0.7)]
    auf = []
    for i in ids:
        for k in range(1, n + 1):
            if "--nur-selfies" in sys.argv:
                continue
            g = ib.graph(BILDER[i][0] + STIL, TMP, "szene_%s_%d" % (i, k), random.randint(1, 2 ** 31), True)
            g["6"]["inputs"].update({"width": 1024, "height": 1024})
            auf.append(("%s %d" % (i, k), ib.post("/prompt", {"prompt": g})["prompt_id"]))
    ib.warten(auf, lambda v: None)
    import favour_fotos as FF
    if "--ohne-arm" in sys.argv:
        for i in ids:
            f = FF.FV.FOTOS[i]
            f["ersetzen"] = [(f["ersetzen"][0][0], OHNE_ARM.sub(",", f["ersetzen"][0][1]))]
            assert "octopus" not in f["ersetzen"][0][1]
    FF.ROH = TMP
    FF.W = FF.H = 1104                     # quadratisch: das Polaroid zeigt sie ganz (Duc: weiter rauszoomen)
    FF.rendern(ids, n)
    s = Image.new("RGB", (280 * n + 360 * n, 360 * len(ids)), "white")
    for z, i in enumerate(ids):
        for k in range(1, n + 1):
            a = Image.open(os.path.join(TMP, "szene_%s_%d.png" % (i, k))).convert("RGB").resize((280, 280))
            b = Image.open(os.path.join(TMP, "fv_%s_r%d.png" % (i, k))).convert("RGB").resize((360, 360))
            s.paste(a, ((k - 1) * 280, z * 360))
            s.paste(b, (280 * n + (k - 1) * 360, z * 360))
    s.save(os.path.join(TMP, "bogen.jpg"), quality=86)
    print(TMP)


def karte(bild, zeile, seite=760):
    rand, unten = 44, 210
    w, h = bild.size
    m = min(w, h)
    o = max(0, (h - m) // 3)
    q = bild.crop(((w - m) // 2, o, (w - m) // 2 + m, o + m)).resize((seite, seite), Image.LANCZOS)
    k = Image.new("RGB", (seite + 2 * rand, seite + rand + unten), PAPIER)
    k.paste(q, (rand, rand))
    d = ImageDraw.Draw(k)
    g = 58
    zeilen = zeile.split("\n")                                 # kleine Gedichte: Duc sieht ihre Unterschriften als Kunstform
    while max(d.textlength(z, font=ImageFont.truetype(SCHRIFT, g)) for z in zeilen) > k.width - 70:
        g -= 2
    f = ImageFont.truetype(SCHRIFT, g)
    y = seite + rand + (unten - len(zeilen) * (g + 12)) // 2
    for z in zeilen:
        d.text(((k.width - d.textlength(z, font=f)) / 2, y), z, font=f, fill=TINTE)
        y += g + 12
    return k.convert("RGBA")


def waehlen(i, a, b, arm=None, seite="r"):
    _, z1, z2 = BILDER[i]
    links = karte(Image.open(os.path.join(TMP, "szene_%s_%s.png" % (i, a))).convert("RGB"), z1).rotate(2.5, expand=True, resample=Image.BICUBIC)
    selfie = Image.open(os.path.join(TMP, "fv_%s_r%s.png" % (i, b))).convert("RGB")
    if arm:
        selfie = arm_setzen(selfie, arm, seite == "l")
    rechts = karte(selfie, z2).rotate(-3, expand=True, resample=Image.BICUBIC)
    s = Image.new("RGB", (links.width + rechts.width + 60, max(links.height, rechts.height) + 40), TISCH)
    s.paste(links, (20, 20), links)
    s.paste(rechts, (links.width + 40, 20), rechts)
    s.thumbnail((1500, 1500), Image.LANCZOS)
    s.save(os.path.join(ZIEL, "fv_%s.webp" % i), "WEBP", quality=88, method=6)
    print("->", i)


if __name__ == "__main__":
    if sys.argv[1] == "rendern":
        rendern(int(sys.argv[2]), sys.argv[3].split(",") if len(sys.argv) > 3 and not sys.argv[3].startswith("-") else list(BILDER))
    elif sys.argv[1] == "arm":
        arm_rendern(int(sys.argv[2]))
    else:
        waehlen(*sys.argv[2:])
