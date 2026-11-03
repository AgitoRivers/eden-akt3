# -*- coding: utf-8 -*-
r"""Kobra und Skorpion in die Kampf-Quellen legen (Duc 01.11.2026). flee wird einmal gespiegelt, Gegner fliehen nach rechts.

    robot_flink_einbau.py   -> output\expressions\combat\<RobotCobra|RobotScorpion>\<pose>.png, danach kampf_bilder.py --gegner <Name>
"""
import os, shutil
from PIL import Image

W = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions"
POSEN = "idle windup attack heavy_windup heavy_attack guard hurt enraged weakened defeated surrender flee victory".split()
for quelle, name in (("kobra", "RobotCobra"), ("skorpion", "RobotScorpion")):
    ziel = os.path.join(W, "combat", name)
    os.makedirs(ziel, exist_ok=True)
    for p in POSEN:
        shutil.copy2(os.path.join(W, "_robot_flink_satz", quelle, p + ".png"), os.path.join(ziel, p + ".png"))
    Image.open(os.path.join(ziel, "flee.png")).transpose(Image.FLIP_LEFT_RIGHT).save(os.path.join(ziel, "flee.png"))
    open(os.path.join(ziel, "_flee_gespiegelt.txt"), "w").write("flee ist gespiegelt\n")
    print(name, len(POSEN))
