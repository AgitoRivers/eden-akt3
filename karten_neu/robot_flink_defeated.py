# -*- coding: utf-8 -*-
r"""defeated der flinken Roboter: Licht aus (Duc 01.11.2026). Krea laesst das Licht immer an.

Kobra: gespiegelte alte surrender-Pose, Krea malte beim Liegen immer einen zweiten Kopf. Skorpion: die eigene defeated-Pose.

    robot_flink_defeated.py [--nur kobra|skorpion]   -> output\expressions\_robot_flink_satz\<name>\defeated.png
"""
import os, sys
import numpy as np
from PIL import Image

W = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions\_robot_flink_satz"
# Quelle ist die alte surrender-Pose, Duc hat dieses Ergebnis abgenommen
KOBRA = r"X:\AI\ComfyUI_krea2\ComfyUI\output\_expressions_papierkorb\_robot_flink_satz_r4\kobra\surrender.png"


def licht_aus(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    # Rot und der helle Kern des Lichts werden dunkles Graphit, der Rest bleibt
    rot = np.clip((r - np.maximum(g, b) - 25) / 60, 0, 1)
    kern = np.zeros(rot.shape, bool)
    ys, xs = np.nonzero(rot > 0.5)
    kern[ys.min():ys.max() + 1, xs.min():xs.max() + 1] = True
    hell = np.clip((np.minimum(np.minimum(r, g), b) - 150) / 60, 0, 1) * kern
    m = np.maximum(rot, hell)
    for k in range(3):
        a[..., k] = a[..., k] * (1 - m) + 34 * m
    return a, int((m > 0.5).sum())


nur = sys.argv[sys.argv.index("--nur") + 1] if "--nur" in sys.argv else None
if nur in (None, "kobra"):
    a, n = licht_aus(np.array(Image.open(KOBRA).convert("RGBA"))[:, ::-1].astype(float))
    Image.fromarray(a.astype("uint8")).save(os.path.join(W, "kobra", "defeated.png"))
    print("kobra", n)
if nur in (None, "skorpion"):
    p = os.path.join(W, "skorpion", "defeated.png")
    a, n = licht_aus(np.array(Image.open(p).convert("RGBA")).astype(float))
    Image.fromarray(a.astype("uint8")).save(p)
    print("skorpion", n)
