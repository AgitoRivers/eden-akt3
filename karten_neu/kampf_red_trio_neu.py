# -*- coding: utf-8 -*-
r"""Red Trio Kampf-Sprites nachrendern (Duc 29.10.2026, Abnahme red_trio_kampf: "Danzel defeated, heavy_attack, hurt
und Charly alle neu rendern. Zudem ist sowohl bei Bibi als auch bei Charly die Fuesse weg. Wenn der Fokus zu stark auf
das Make-up ist, kannst du es auch rausnehmen").

Aenderungen gegenueber kampf_red_trio.py:
- Kampf_Bibi / Kampf_Charly: Make-up-Tags raus (Instagirl Soft Glam, Winged Liner, Blush), Kopfzeile verlangt die ganze
  Figur bis zu den Schuhen mit Boden darunter (Krea CFG 1: nur positiv formuliert).
- Charly: Studio-Hintergrund ausdruecklich (der Louisa-LoRA zieht sonst einen Flur ins Bild), LoRA 0.8 -> 0.7.
- Danzel: eigene Texte fuer hurt und heavy_attack (starrer Stab ohne Kabel), defeated mit genau einem Kopf, sauberer Boden.
Alte Bilder wandern vorher nach output\_expressions_papierkorb\combat\red_trio_<Zeit>.

    kampf_red_trio_neu.py          Probelauf
    kampf_red_trio_neu.py --los    Presets anpassen, alte Bilder verschieben, Auftraege einreihen
    kampf_red_trio_neu.py --los --karten "Bibi=idle,windup;Charly=hurt"   nur diese Posen (Runde 2 usw.)
Runde 2 (29.10. 23:20): Bibi hatte Fliesen/Zimmerwand und abgeschnittene Fuesse (enraged), Charly und Danzel Flecken
am Boden -> Studio-Zeile jetzt auch fuer Bibi, mit sauberem Boden.
"""
import os, shutil, sys, time

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
LOS = "--los" in sys.argv
KARTEN = sys.argv[sys.argv.index("--karten") + 1] if "--karten" in sys.argv else None
import kampf_red_trio as KR  # noqa: E402   (liest argv beim Import, setzt stdout auf UTF-8)

dc, sk = KR.dc, KR.sk
C = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions\combat"
KORB = r"X:\AI\ComfyUI_krea2\ComfyUI\output\_expressions_papierkorb\combat\red_trio_" + time.strftime("%Y%m%d_%H%M")
MAKEUP = {"Instagirl Soft Glam", "Winged Liner", "Blush"}
GANZ_ALT = "one single woman alone in the frame, her whole body in full view,"
GANZ_NEU = ("one single woman alone in the frame, her whole body in full view from the top of her head down to her "
            "shoes, both feet standing on the floor inside the image, the camera far back with empty floor below her "
            "feet,")
STUDIO_ALT = "Scene: {setting},"
STUDIO_NEU = ("Scene: {setting}, an empty photo studio with a seamless plain beige paper backdrop that curves down "
              "onto a clean spotless floor,")
STUDIO_R1 = ("Scene: {setting}, an empty photo studio with a seamless plain beige paper backdrop that curves down "
             "onto the floor,")
LIEGT_DANZEL = ("knocked out cold, lying flat on his back on a clean beige studio floor, a single man with one head, "
                "his head turned to the side, both arms limp, the baton lying loose beside his open hand, eyes closed, "
                "mouth slightly open, the whole body fully horizontal across the image, alone in the frame")
DANZEL = {
    "heavy_attack": "charging forward to the left with the short rigid black metal baton held out straight like a "
                    "sword, a solid stick in his gloved hand, screaming, his coat flapping behind him, motion blur",
    "hurt": "hit by a heavy blow, recoiling backwards off balance, head snapped back, his free hand clutching his "
            "chest, the baton slipping loosely from his other hand, face twisted in pain, eyes squeezed shut, the "
            "beige studio floor clean and spotless around his shoes",
}
# Duc 30.10.: Bibis Granaten sind schwarz. "hand grenade" zieht die gruene Ananas-Form ins Bild, Kugeln wurden zu Bowlingkugeln
# und Boxhandschuhen, also die Dosenform der Spiel-Granaten in Schwarz (Stand der Karte: auch noch mit Kugel-Text).
DOSE_ALT = "small matte black cylindrical canister grenade the size of a soda can with a metal lever and a pull ring on top"
DOSEN_ALT = "small matte black cylindrical canister grenades the size of soda cans, each with a metal lever and a pull ring on top"
DOSE = "small cylindrical canister grenade painted entirely jet black, the size of a soda can, with a jet black lever and a jet black pull ring on top"
DOSEN = "small cylindrical canister grenades painted entirely jet black, the size of soda cans, each with a jet black lever and pull ring on top"
KUGEL = "smooth matte black metal sphere the size of an orange with a small silver ring on top"
KUGEL_N = "smooth matte black metal spheres the size of oranges, each with a small silver ring on top"
LOEWE = "a small plush lion keychain that is entirely jet black, black face, black paws, black mane, hanging from her belt on her right hip, on the left side of the image"
KARTE_BIBI = [("several round black grenades", "several " + DOSEN), ("a round black hand grenade", "a " + DOSE),
              (KUGEL_N, DOSEN), (KUGEL, DOSE), (DOSEN_ALT, DOSEN), (DOSE_ALT, DOSE),
              ("a small plush boar keychain", LOEWE), ("a small plush black lion keychain with a dark mane", LOEWE)]   # Mochi, Duc 30.10.
for _k, _t in KR.TRIO["Bibi"][4].items():
    KR.TRIO["Bibi"][4][_k] = (_t.replace("two round black grenades", "two " + DOSEN)
                              .replace("a round black grenade in each hand", "a " + DOSE + " in each hand")
                              .replace("a round black grenade", "a " + DOSE)
                              .replace("the grenades at her belt", "the black canisters at her belt"))
KR.TRIO["Bibi"][4]["guard"] = ("standing with her body facing the camera, knees bent, both forearms raised in front of her "
                               "face to block, squinting past them to the left, the belt and the keychain on her right hip "
                               "in full view on the left side of the image")   # Duc 30.10.: Loewe links
NEU = {"Danzel": ["heavy_attack", "hurt", "defeated"], "Bibi": None, "Charly": None}   # None = alle 13
if KARTEN:                       # vor dem Import gelesen: kampf_red_trio setzt sys.argv zurueck
    NEU = {n: k.split(",") for n, k in (x.split("=") for x in KARTEN.split(";"))}


def presets_anpassen():
    presets = dc.load_json(sk.F_PRESETS, None, "Studio")
    sets = dc.load_json(sk.F_SETS, None, "Studio")
    for name in ("Bibi", "Charly"):
        p = presets["Kampf_" + name]
        p["tags_on"] = [t for t in p["tags_on"] if t not in MAKEUP]
        if GANZ_NEU not in p["sprite_prompt"]:
            assert GANZ_ALT in p["sprite_prompt"], name
            p["sprite_prompt"] = p["sprite_prompt"].replace(GANZ_ALT, GANZ_NEU)
        s = sets["Kampf_%s|Kampf" % name]
        s["tags"] = [t for t in s["tags"] if t not in MAKEUP]
        print("  Kampf_%s Tags: %s" % (name, ", ".join(p["tags_on"])))
        if STUDIO_NEU not in p["sprite_prompt"]:
            alt = STUDIO_R1 if STUDIO_R1 in p["sprite_prompt"] else STUDIO_ALT
            assert alt in p["sprite_prompt"], name
            p["sprite_prompt"] = p["sprite_prompt"].replace(alt, STUDIO_NEU)
    ch = presets["Kampf_Charly"]
    for l in ch["loras"]:
        if l["name"] == "Krea_LouisaV2.safetensors":
            l["strength"] = 0.7
    if LOS:
        dc.save_json(sk.F_PRESETS, presets, "Studio")
        dc.save_json(sk.F_SETS, sets, "Studio")
        d = KR.ps("/api/state")["decks"]
        for c in d["outfit"]:
            if c["name"] == "kampf_bibi":
                for alt, neu in KARTE_BIBI:
                    c["prompt"] = c["prompt"].replace(alt, neu)
        KR.ps("/api/decks", d)


def main():
    st = KR.ps("/api/state")
    kern = [c["name"] for c in st["decks"]["kampf"] if c.get("on", True) and c.get("tag") == "kern"]
    plan = {n: (k or kern) for n, k in NEU.items()}
    for n, k in plan.items():
        print("%-7s %s" % (n, ", ".join(k)))
    presets_anpassen()
    if not LOS:
        print("Probelauf - nichts geaendert")
        return
    os.makedirs(KORB, exist_ok=True)
    for n, karten in plan.items():
        os.makedirs(os.path.join(KORB, n), exist_ok=True)
        for k in karten:
            f = os.path.join(C, n, k + ".png")
            if os.path.isfile(f):
                shutil.move(f, os.path.join(KORB, n, k + ".png"))
    print("alte Bilder ->", KORB)
    alt_preset = st["cfg"].get("preset_active")
    try:
        for n, karten in plan.items():
            texte = DANZEL if n == "Danzel" else KR.TRIO[n][4]
            liegt = LIEGT_DANZEL if n == "Danzel" else KR.LIEGT % ("her", "her")
            eigen = {k: t for k, t in texte.items() if k in karten}
            if eigen:
                KR.mit_text(n, eigen)
            rest = [k for k in karten if k not in texte and k != "defeated"]
            if rest:
                KR.lauf(n, rest)
            if "defeated" in karten:
                KR.mit_text(n, {"defeated": liegt}, quer=True)
    finally:
        if alt_preset:
            KR.ps("/api/presets", {"action": "load", "name": alt_preset})
    print("fertig eingereiht")


if __name__ == "__main__":
    main()
