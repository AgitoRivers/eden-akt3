# -*- coding: utf-8 -*-
r"""Skorpion hurt: aufgebaeumt durch Drehen, Krea haelt den Koerper immer waagerecht (Duc 01.11.2026).

    robot_flink_hurt.py   -> output\expressions\_robot_flink_satz\skorpion\hurt.png
"""
from PIL import Image

W = r"X:\AI\ComfyUI_krea2\ComfyUI\output"
Q = W + r"\_expressions_papierkorb\_robot_flink_satz_r8\skorpion\hurt-1.png"
GRAD = 30  # im Uhrzeigersinn: der Kopf links geht hoch

q = Image.open(Q).convert("RGBA").rotate(-GRAD, resample=Image.BICUBIC, expand=True)
q = q.crop(q.getchannel("A").point(lambda v: 255 if v > 128 else 0).getbbox())  # einzelne schwache Pixel zaehlen nicht
rand = 24
b = Image.new("RGBA", (q.width + 2 * rand, q.height + 2 * rand), (0, 0, 0, 0))
b.paste(q, (rand, rand), q)
b.save(W + r"\expressions\_robot_flink_satz\skorpion\hurt.png")
print(b.size)
