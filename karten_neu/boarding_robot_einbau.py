# -*- coding: utf-8 -*-
r"""Boarding Robots in die Kampf-Quellen legen (Duc 01.11.2026). flee wird einmal gespiegelt, Gegner fliehen nach rechts.

    boarding_robot_einbau.py   -> output\expressions\combat\<BoardingRobot|BoardingRobotHeavy>\<pose>.png, danach kampf_bilder.py --gegner <Name>
"""
import os, shutil
from PIL import Image

W = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions"
POSEN = "idle windup attack heavy_windup heavy_attack guard hurt enraged weakened defeated surrender flee victory".split()
for quelle, name in (("normal", "BoardingRobot"), ("schwer", "BoardingRobotHeavy")):
    ziel = os.path.join(W, "combat", name)
    if os.path.exists(ziel):
        raise SystemExit("Ziel existiert schon: " + ziel)
    os.makedirs(ziel)
    for p in POSEN:
        shutil.copy2(os.path.join(W, "_boarding_robot_satz", quelle, p + ".png"), os.path.join(ziel, p + ".png"))
    Image.open(os.path.join(ziel, "flee.png")).transpose(Image.FLIP_LEFT_RIGHT).save(os.path.join(ziel, "flee.png"))
    open(os.path.join(ziel, "_flee_gespiegelt.txt"), "w").write("flee ist gespiegelt\n")
    print(name, len(POSEN))
