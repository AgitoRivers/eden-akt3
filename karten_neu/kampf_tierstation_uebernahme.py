# -*- coding: utf-8 -*-
r"""Abgenommene Tierstation-Saetze uebernehmen (Duc 01.11.2026): je Pose wird die neueste Fassung zu <pose>.png, aeltere Fassungen gehen in den Papierkorb,
flee wird gespiegelt, das Stationsbild landet als combat\<Name>Frei\idle.png. Bricht ab, wenn der Sicherungsordner schon existiert. Danach kampf_bilder.py --gegner.

    kampf_tierstation_uebernahme.py          Probelauf
    kampf_tierstation_uebernahme.py --los
"""
import glob, os, re, shutil, sys, time
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
LOS = "--los" in sys.argv
AUS = r"X:\AI\ComfyUI_krea2\ComfyUI\output"
K = os.path.join(AUS, "expressions", "combat")
SICHER = os.path.join(AUS, "_expressions_papierkorb", "tierstation_" + time.strftime("%H%M%S"))
TIERE = "RussianBlue Capybara Tortoise BeardedVulture RedPanda SnowLeopard Komodo".split()
FREI = TIERE + "Dog ArkHyena Wolf Panther Grizzly".split()
POSEN = "idle windup attack heavy_windup heavy_attack guard hurt enraged weakened surrender flee victory defeated death".split()
if os.path.exists(SICHER):
    sys.exit("Sicherung existiert schon: " + SICHER)
for n in TIERE:
    d = os.path.join(K, n)
    for p in POSEN:
        fs = sorted((f for f in glob.glob(os.path.join(d, p + "*.png")) if re.fullmatch(p + r"(-\d)?\.png", os.path.basename(f))), key=os.path.getmtime)
        if not fs:
            sys.exit("%s/%s fehlt" % (n, p))
        neu, alte = fs[-1], fs[:-1]
        print(n, p, "<-", os.path.basename(neu), "alt:", len(alte))
        if not LOS:
            continue
        ziel = os.path.join(SICHER, n)
        os.makedirs(ziel, exist_ok=True)
        for a in alte:
            shutil.move(a, os.path.join(ziel, os.path.basename(a)))
        if os.path.basename(neu) != p + ".png":
            os.rename(neu, os.path.join(d, p + ".png"))
    if LOS and not os.path.exists(os.path.join(d, "_flee_gespiegelt.txt")):
        f = os.path.join(d, "flee.png")
        Image.open(f).transpose(Image.FLIP_LEFT_RIGHT).save(f)
        open(os.path.join(d, "_flee_gespiegelt.txt"), "w").write("flee.png horizontal gespiegelt (laeuft nach rechts weg)\n")
for n in FREI:
    q = max(glob.glob(os.path.join(K, n + "Frei_TEST", "idle*.png")), key=os.path.getmtime)
    print(n + "Frei", "<-", os.path.basename(q))
    if LOS:
        os.makedirs(os.path.join(K, n + "Frei"), exist_ok=True)
        shutil.copy2(q, os.path.join(K, n + "Frei", "idle.png"))
print("uebernommen, Sicherung: " + SICHER if LOS else "PROBELAUF")
