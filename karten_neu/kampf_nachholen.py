# -*- coding: utf-8 -*-
r"""Nachholen der Kampf-Sprites (22.10.2026): Yasin wütend, Maxwell Steward im Polo mit Kragen, Alon in der glänzend
schwarzen Cyber-Armor mit Strahlenpistole, Wildschwein in drei Größen. Gestartet über Kampf_Nachholen.bat.

    kampf_nachholen.py test     Presets eintragen, je Figur ein Testbild (outfit_check)
    kampf_nachholen.py voll     alte Posen in den Papierkorb-Ordner, kompletter Posen-Lauf (nach Duc's OK zum Test)
    kampf_nachholen.py fertig   wenn alles gerechnet ist: Flucht-Pose spiegeln, Wildschweine verkleinern
"""
import io, os, shutil, subprocess, sys, time, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
COMBAT = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions\combat"
TRASH = r"X:\AI\ComfyUI_krea2\ComfyUI\output\_expressions_papierkorb\combat"
sys.path.insert(0, HERE)
from kampf_alphas import ALPHAS   # noqa: E402
WHO = ["YasinDrone", "MaxwellSteward", "Alon", "WildschweinKlein", "Wildschwein", "WildschweinKeiler"] + list(ALPHAS)


def up(url):
    try:
        urllib.request.urlopen(url, timeout=5)
        return True
    except Exception:
        return False


def run(*args):
    print(">", " ".join(args[1:]))
    subprocess.run([PY, *args], check=True, cwd=HERE)


def to_trash(name, only=None):
    src = os.path.join(COMBAT, name)
    if not os.path.isdir(src):
        return 0
    dst = os.path.join(TRASH, name, time.strftime("%Y-%m-%d_%H%M%S"))
    n = 0
    for f in os.listdir(src):
        if f.endswith(".png") and (only is None or f == only) or (only is None and f == "_flee_gespiegelt.txt"):
            os.makedirs(dst, exist_ok=True)
            shutil.move(os.path.join(src, f), dst)
            n += 1
    return n


mode = (sys.argv[1] if len(sys.argv) > 1 else "test").lower()
if mode in ("test", "voll"):
    if not up("http://127.0.0.1:8301/") or not up("http://127.0.0.1:8189/system_stats"):
        sys.exit("Bitte erst Prompt Studio (8301) und ComfyUI Krea2 (8189) starten, dann nochmal.")
    run(os.path.join(HERE, "kampf_neue_gegner_3.py"), "--los")
    run(os.path.join(HERE, "kampf_neue_gegner_4.py"), "--los")
    run(os.path.join(HERE, "kampf_alphas.py"), "--los")
if mode == "test":
    for n in WHO:
        to_trash(n, only="outfit_check.png")
    run(os.path.join(HERE, "kampf_test.py"), "--karten", "outfit_check", "--gegner", ",".join(WHO))
    print("\nTestbilder eingereiht. Wenn sie fertig sind, sagt Duc Claude Bescheid.")
elif mode == "voll":
    moved = sum(to_trash(n) for n in WHO)
    print("%d alte Bilder in den Papierkorb-Ordner verschoben" % moved)
    run(os.path.join(HERE, "kampf_volllauf_runde3.py"), "--los", "--gegner", ",".join(WHO))
    print("\nPosen eingereiht. Wenn ComfyUI fertig ist: Kampf_Nachholen.bat -> fertig")
elif mode == "fertig":
    run(os.path.join(HERE, "kampf_flee_spiegeln.py"), "--los")
    run(os.path.join(HERE, "kampf_klein.py"), "--los")
else:
    sys.exit(__doc__)
