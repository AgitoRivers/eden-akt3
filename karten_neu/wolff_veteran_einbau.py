# -*- coding: utf-8 -*-
r"""Wolff "Der Veteran" ins Spiel (Duc 01.11.2026, Abnahme wolff_veteran_satz + guard Fassung 1). Alte Bilder wandern vorher in den Papierkorb, die Sicherung wird nie ueberschrieben.

    wolff_veteran_einbau.py          Probelauf
    wolff_veteran_einbau.py --los    Figuren + combat-Quelle tauschen, flee spiegeln, Presets und Karten auf den neuen Look
Danach: python werkzeuge\kampf_bilder.py --gegner Wolff  und  python -X utf8 werkzeuge\gesichter_messen.py --neu
"""
import glob, json, os, shutil, sys, urllib.request

from PIL import Image

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, r"X:\AI\DucCommon")
import casting_wolff_veteran as cv  # noqa: E402
import duc_common as dc  # noqa: E402

E = cv.OUT
SATZ = os.path.join(E, "_wolff_veteran_satz")
GUARD = os.path.join(E, "_wolff_veteran_guard", "1", "guard.png")
FIG = r"X:\AI\Eden\module\eden_rise\figuren\Kaspar Wolff"
COMBAT = os.path.join(E, "combat", "Wolff")
KAMPF = r"X:\AI\Eden\module\eden_rise\kampf\Wolff"
KORB = r"X:\AI\ComfyUI_krea2\ComfyUI\output\_expressions_papierkorb\wolff_alt_20261101"
F_PRESETS = r"X:\AI\PromptStudio\presets.json"
MODELL_NAME = "Krea2 fp8 (krea2_turbo_fp8_scaled + qwen3vl_4b_fp8)"
GESICHT = cv.gesicht("3")
RUESTUNG = cv.VARIANTEN["3"][1]
K_DIALOG = "%s, %s, %s" % (cv.BARETT, RUESTUNG, cv.VARIANTEN["3"][2])
K_KAMPF = "%s, %s, his only weapon exactly one long straight steel sword gripped in his right fist, the whole sword inside the image" % (cv.BARETT, RUESTUNG)


def ps(pfad, daten=None):
    req = urllib.request.Request(cv.PS + pfad, data=None if daten is None else json.dumps(daten).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def main():
    if "--nur-presets" in sys.argv:          # erster Lauf (01.11.) brach nach dem Bildertausch ab, der darf nicht wiederholt werden
        return presets_und_karten()
    dialog = sorted(glob.glob(os.path.join(SATZ, "dialog", "*.png")))
    kampf = [p for p in sorted(glob.glob(os.path.join(SATZ, "kampf", "*.png"))) if os.path.basename(p) != "guard.png"]
    print("Dialog %d, Kampf %d + guard, Sicherung %s" % (len(dialog), len(kampf), KORB))
    assert len(dialog) == 22 and len(kampf) == 12 and os.path.isfile(GUARD)
    assert not os.path.exists(KORB), "Sicherung existiert schon, Abbruch"
    if "--los" not in sys.argv:
        sys.exit("PROBELAUF - mit --los einbauen")
    shutil.copytree(FIG, os.path.join(KORB, "figuren"))
    shutil.copytree(COMBAT, os.path.join(KORB, "combat"))
    shutil.copytree(KAMPF, os.path.join(KORB, "kampf"))
    for f in glob.glob(os.path.join(FIG, "*.png")) + glob.glob(os.path.join(COMBAT, "*.png")):
        os.remove(f)
    for p in dialog:
        shutil.copy2(p, os.path.join(FIG, os.path.basename(p).replace("_2.png", ".png")))
    for p in kampf:
        shutil.copy2(p, COMBAT)
    shutil.copy2(GUARD, COMBAT)
    flee = os.path.join(COMBAT, "flee.png")
    Image.open(flee).transpose(Image.FLIP_LEFT_RIGHT).save(flee)           # die Marke _flee_gespiegelt.txt liegt schon im Ordner
    alt_tod = os.path.join(KAMPF, "death.webp")
    if os.path.isfile(alt_tod):                                            # Menschen haben keine death-Pose, die alte zeigt noch das Messer
        os.remove(alt_tod)
    with open(os.path.join(FIG, "_prompt.txt"), "w", encoding="utf-8") as f:
        f.write("Wearing: %s\nScene: Plain beige background\n" % K_DIALOG)
    presets_und_karten()


def presets_und_karten():
    presets = dc.load_json(F_PRESETS, None, "Studio")
    y = presets["Yacht_Wolff"]
    y["sprite_prompt"] = ("{tags_action}, %s, full body shot from head to feet, direct gaze, one single man alone in the frame, his whole body in full view, head and boots inside the frame,\n"
                          "Subject: %s,\nWearing: {outfit},\nScene: {setting}, {st},\n{expression},\nLook: {look},\n{tags_photo}" % (cv.FOTO, GESICHT))
    y["modell"] = MODELL_NAME
    k = presets["Kampf_Wolff"]
    alt = "Sergent Kaspar Wolff, a 48-year-old soldier of the French Foreign Legion, an angular weathered face with deep lines, short shaved grey hair, a thick grey moustache, narrow steel-grey eyes, a strong jaw"
    for feld in ("base_prompt", "sprite_prompt", "fashion_prompt"):
        assert alt in k[feld], feld
        k[feld] = k[feld].replace(alt, GESICHT)
    k["modell"] = MODELL_NAME
    dc.save_json(F_PRESETS, presets, "Studio")
    d = ps("/api/state")["decks"]
    karten = {c["name"]: c for c in d["outfit"]}
    karten["wolff_standard"]["prompt"] = K_DIALOG
    karten["kampf_wolff"]["prompt"] = K_KAMPF
    ps("/api/decks", d)
    print("Figur", len(glob.glob(os.path.join(FIG, "*.png"))), "Bilder, combat", len(glob.glob(os.path.join(COMBAT, "*.png"))), "Bilder, Presets und Karten neu")


if __name__ == "__main__":
    main()
