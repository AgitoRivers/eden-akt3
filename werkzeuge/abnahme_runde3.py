# -*- coding: utf-8 -*-
r"""Approval spec for round 3 of the combat sprites (22.10.2026): the 19 re-rendered poses next to idle, plus one
size strip per enemy (all poses as exported to the module, side by side on the combat canvas) to check that the
size no longer jumps between poses and that the species sizes fit together.

    python abnahme_runde3.py     -> docs\abnahme\kampf_runde3.json (+ strips in docs\abnahme\groesse\)
"""
import json, os, sys

from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions\combat"
MOD = os.path.join(EDEN, "module", "eden_rise", "kampf")
OUT = os.path.join(EDEN, "docs", "abnahme")
STRIPS = os.path.join(OUT, "groesse")
POSEN = ("idle", "guard", "hurt", "windup", "attack", "heavy_attack", "flee", "victory", "defeated", "death")
JOBS = [("Brute", "guard"), ("BruteAlpha", "guard"), ("DrunkCasanova", "guard"), ("Thief", "guard"),
        ("ThiefArab", "guard"), ("Alon", "hurt"), ("Alon", "heavy_windup"), ("AgentAlpha", "attack"),
        ("ApeAlpha", "guard"), ("ApeAlpha", "hurt"), ("ApeAlpha", "enraged"),
        ("Lion", "defeated"), ("Lion", "death"), ("WolfAlpha", "defeated"), ("WolfAlpha", "death"),
        ("Panther", "defeated"), ("Panther", "death"), ("PantherAlpha", "defeated"), ("PantherAlpha", "death")]
SOLL = {
    "guard": "Schutzpose, ganz im Bild bis zu den Schuhen, nichts abgeschnitten",
    "hurt": "getroffen, ganz im Bild",
    "heavy_windup": "holt mit beiden Händen weit aus, ganz im Bild",
    "attack": "Faustschlag nach links, ganz im Bild bis zu den Schuhen",
    "enraged": "brüllt wütend, Piratenhut, ganz im Bild",
    "defeated": "liegt bewusstlos, Kopf rechts, ganz im Bild",
    "death": "liegt tot und friedlich, Kopf rechts, ganz im Bild",
}
EXTRA = {("Thief", "guard"): " – ohne Brecheisen", ("ThiefArab", "guard"): " – ohne Brecheisen",
         ("Brute", "guard"): " – aus der Alpha-Pose umgestellt: passt das Gesicht (Bart?)"}


def strip(name):
    H = 220
    W = int(H * 1170 / 1000)
    files = [(p, os.path.join(MOD, name, p + ".webp")) for p in POSEN if os.path.isfile(os.path.join(MOD, name, p + ".webp"))]
    img = Image.new("RGB", (len(files) * (W + 4), H + 18), (52, 47, 40))
    d = ImageDraw.Draw(img)
    for i, (p, f) in enumerate(files):
        im = Image.open(f).convert("RGBA").resize((W, H))
        cell = Image.new("RGB", (W, H), (96, 90, 80))
        cell.paste(im, (0, 0), im)
        img.paste(cell, (i * (W + 4), 18))
        d.text((i * (W + 4) + 4, 3), p, fill=(239, 230, 214))
    os.makedirs(STRIPS, exist_ok=True)
    path = os.path.join(STRIPS, name + ".png")
    img.save(path)
    return path


def main():
    items = []
    for n, p in JOBS:
        items.append({"id": "%s/%s" % (n, p), "titel": "%s · %s" % (n, p),
                      "bild": os.path.join(SRC, n, p + ".png"), "soll": SOLL[p] + EXTRA.get((n, p), ""),
                      "vergleich": os.path.join(SRC, n, "idle.png"), "vergleich_titel": "idle"})
    for n in sorted(os.listdir(MOD)):
        if os.path.isdir(os.path.join(MOD, n)) and os.path.isfile(os.path.join(MOD, n, "idle.webp")):
            items.append({"id": "Größe/" + n, "titel": "Größe · " + n, "bild": strip(n),
                          "soll": "alle Posen gleich groß (so stehen sie im Kampfbildschirm); Art passend groß"})
    spec = {"id": "kampf_runde3", "titel": "Kampf-Sprites: Runde 3 + Größen",
            "hinweis": "Oben die 19 neu gerechneten Posen (rechts die Idle-Pose zum Vergleich). Darunter je Gegner ein "
                       "Größen-Streifen mit allen Posen, wie sie im Spiel stehen. Neu = nochmal machen bzw. Größe ändern "
                       "(gern mit Notiz: größer/kleiner).",
            "items": items}
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "kampf_runde3.json")
    json.dump(spec, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(path, len(items), "Einträge")


if __name__ == "__main__":
    main()
