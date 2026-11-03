# -*- coding: utf-8 -*-
r"""Ligeias freigegebene Sprites ins Spiel (Duc 30.10.2026, Abnahme ligeia_sfw): roh -> Sorted ueber Prompt Studio, dann den
blassen Felsen-Schatten aus der Maske und nach module\eden_rise\figuren\The Siren. Kein Nachbelichten, kein Zuschnitt: Alle Posen
behalten dieselbe Leinwand, damit sie zwischen den Gefuehlen nicht springt. Die alten Bilder wandern in den Papierkorb.

    ligeia_einbau.py          Probelauf
    ligeia_einbau.py --los
"""
import glob, json, os, shutil, sys, time, urllib.request

from PIL import Image

ROH = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions\Yacht_Ligeia\Standard\roh"
SRT = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions\Yacht_Ligeia\Standard\Sorted"
FIG = r"X:\AI\Eden\module\eden_rise\figuren\The Siren"
KORB = r"X:\AI\ComfyUI_krea2\ComfyUI\output\_expressions_papierkorb\figuren_The_Siren_" + time.strftime("%Y%m%d_%H%M")


def ps(pfad, daten):
    req = urllib.request.Request("http://127.0.0.1:8301" + pfad, data=json.dumps(daten).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def schatten_raus(f):
    im = Image.open(f).convert("RGBA")
    im.putalpha(im.getchannel("A").point(lambda v: 0 if v < 110 else (255 if v > 170 else round((v - 110) * 255 / 60))))
    im.save(f)


def main():
    q = [{"kost": "Standard", "src": ROH}]
    print("geplant:", ps("/api/sprites", {"quellen": q, "move": False}).get("planned"))
    if "--los" not in sys.argv:
        sys.exit("PROBELAUF - mit --los einbauen")
    r = ps("/api/sprites", {"quellen": q, "move": False, "apply": True})
    print("sortiert:", r.get("done"), "Fehler:", r.get("errors"))
    neu = glob.glob(os.path.join(SRT, "*.png"))
    if len(neu) != 52:
        raise SystemExit("Erwartet 52 Bilder in Sorted, gefunden %d - Figuren-Ordner bleibt unberuehrt" % len(neu))
    for f in neu:
        schatten_raus(f)
    os.makedirs(KORB, exist_ok=True)
    for f in glob.glob(os.path.join(FIG, "*.png")) + [os.path.join(FIG, "_prompt.txt")]:
        if os.path.isfile(f):
            shutil.move(f, KORB)
    for f in neu:
        shutil.copy2(f, FIG)
    karte = next(c for c in ps_state()["decks"]["outfit"] if c["name"] == "ligeia_standard")
    with open(os.path.join(FIG, "_prompt.txt"), "w", encoding="utf-8") as fh:
        fh.write("Wearing: %s\nScene: Plain beige background\n" % karte["prompt"])
    print("Figuren:", len(glob.glob(os.path.join(FIG, "*.png"))), "alt in", KORB)


def ps_state():
    with urllib.request.urlopen("http://127.0.0.1:8301/api/state", timeout=60) as r:
        return json.loads(r.read())


if __name__ == "__main__":
    main()
