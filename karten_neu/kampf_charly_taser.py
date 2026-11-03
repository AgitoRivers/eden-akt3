# -*- coding: utf-8 -*-
r"""Charly: Taser ganz schwarz (Duc 30.10.2026, Abnahme red_trio_kampf: heavy_attack, surrender, victory). Die neongelbe
Spitze kam auch daher, dass die Outfit-Karte einen zweiten Taser im Holster nannte. Karte bleibt dauerhaft korrigiert,
alte Bilder wandern nach output\_expressions_papierkorb\combat\red_trio_<Zeit>.

    kampf_charly_taser.py          Probelauf
    kampf_charly_taser.py --los
"""
import os, shutil, sys, time

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
LOS = "--los" in sys.argv
import kampf_red_trio as KR  # noqa: E402   (liest argv beim Import, setzt stdout auf UTF-8)

C = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions\combat\Charly"
KORB = r"X:\AI\ComfyUI_krea2\ComfyUI\output\_expressions_papierkorb\combat\red_trio_" + time.strftime("%Y%m%d_%H%M")
ALT = ["a plain matte black handheld taser"]
WAFFE = "a plain matte black pistol-shaped handheld taser"
NUR = ("heavy_attack",)   # Runde 3: Text wie attack, das hatte den Funken; surrender und victory passten
TEXTE = {
    "heavy_attack": "firing her taser to the left with one straight arm, two thin wires shooting out with a big blue "
                    "electric spark and forked lightning in the air in front of the muzzle, her hair lifting from the "
                    "static, her face still completely deadpan",
    "surrender": "kneeling on the floor with both knees and both shins flat on the ground, raising both hands above her "
                 "head, head bowed in defeat, her right hand holding the black pistol-shaped taser by its grip with the "
                 "barrel pointing at the ceiling; the floor around her is completely clean and empty",
    "victory": "a quiet victory pose, chest out, looking down to the left with a dry unimpressed look, the plain black "
               "taser resting against her shoulder in her right hand",
}


def main():
    print("Karten:", ", ".join(TEXTE))
    if not LOS:
        print("Probelauf - nichts geaendert.")
        return
    d = KR.ps("/api/state")["decks"]
    karte = next(c for c in d["outfit"] if c["name"] == "kampf_charly")
    p = karte["prompt"]
    karte["prompt"] = p.replace(ALT[0], WAFFE)
    KR.ps("/api/decks", d)
    os.makedirs(KORB, exist_ok=True)
    for k in NUR:
        shutil.move(os.path.join(C, k + ".png"), os.path.join(KORB, "Charly_%s.png" % k))
    alt_preset = KR.ps("/api/state")["cfg"].get("preset_active")
    try:
        KR.mit_text("Charly", {k: TEXTE[k] for k in NUR})
    finally:
        if alt_preset:
            KR.ps("/api/presets", {"action": "load", "name": alt_preset})
    print("eingereiht. Alte Bilder:", KORB)


if __name__ == "__main__":
    main()
