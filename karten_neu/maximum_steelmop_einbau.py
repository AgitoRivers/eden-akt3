# -*- coding: utf-8 -*-
r"""Mr. Maximum mit Steel Mop ins Spiel (Duc 01.11.2026, Abnahme maximum_steelmop_satz + maximum_steelmop_kampf). Eigene Sets, die alten bleiben unberuehrt.

    maximum_steelmop_einbau.py          Probelauf
    maximum_steelmop_einbau.py --los    figuren\Maxwell Ndlovu\setN (maximum_steelmop) + combat\MaxwellSteelMop, Presets und Karten
Danach: python werkzeuge\kampf_bilder.py --gegner MaxwellSteelMop  und  python -X utf8 werkzeuge\gesichter_messen.py --nur maxwell
"""
import glob, json, os, re, shutil, sys, tempfile, urllib.request

from PIL import Image

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, r"X:\AI\DucCommon")
import duc_common as dc  # noqa: E402
import casting_maximum_steelmop as cm  # noqa: E402
import maximum_steelmop_satz as ms  # noqa: E402

SATZ = os.path.join(cm.OUT, "_maximum_steelmop_satz")
FIG = r"X:\AI\Eden\module\eden_rise\figuren\Maxwell Ndlovu"
COMBAT = os.path.join(cm.OUT, "combat", "MaxwellSteelMop")
NAME = "maximum_steelmop"
F_PRESETS, F_SETS = r"X:\AI\PromptStudio\presets.json", r"X:\AI\PromptStudio\set_presets.json"
MODELL_NAME = "Krea2 fp8 (krea2_turbo_fp8_scaled + qwen3vl_4b_fp8)"
HEMD = cm.VARIANTEN["3"][0]
K_DIALOG = "%s, %s" % (HEMD, cm.HOSE)
K_KAMPF = "%s, %s, his only weapon %s" % (HEMD, cm.HOSE, ms.WAFFE)


def ps(pfad, daten=None):
    req = urllib.request.Request(cm.PS + pfad, data=None if daten is None else json.dumps(daten).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def main():
    dialog, kampf = sorted(glob.glob(os.path.join(SATZ, "dialog", "*.png"))), sorted(glob.glob(os.path.join(SATZ, "kampf", "*.png")))
    assert len(dialog) == 44 and len(kampf) == 13, (len(dialog), len(kampf))
    for d in [FIG] + glob.glob(os.path.join(FIG, "set*")):
        assert open(os.path.join(d, "_name.txt"), encoding="utf-8").read().strip() != NAME, "Set gibt es schon: " + d
    assert not os.path.exists(COMBAT), "combat-Ordner gibt es schon"
    nr = 1 + max(int(m.group(1)) for m in (re.fullmatch(r"set(\d+)", x) for x in os.listdir(FIG)) if m)
    ziel = os.path.join(FIG, "set%d" % nr)
    print("Dialog %d -> %s, Kampf %d -> %s" % (len(dialog), ziel, len(kampf), COMBAT))
    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, "roh")
        os.makedirs(src)
        for f in dialog:
            shutil.copy2(f, src)
        print("geplant", ps("/api/sprites", {"quellen": [{"kost": NAME, "src": src}], "move": False}).get("planned"))
        if "--los" not in sys.argv:
            sys.exit("PROBELAUF - mit --los einbauen")
        r = ps("/api/sprites", {"quellen": [{"kost": NAME, "src": src}], "move": False, "apply": True})
        neu = glob.glob(os.path.join(tmp, "Sorted", "*.png"))
        assert r.get("done") == 44 and len(neu) == 44, (r.get("done"), len(neu))
        os.makedirs(ziel)
        for f in neu:
            shutil.copy2(f, ziel)
    with open(os.path.join(ziel, "_name.txt"), "w", encoding="utf-8") as f:
        f.write(NAME)
    with open(os.path.join(ziel, "_prompt.txt"), "w", encoding="utf-8") as f:
        f.write("Wearing: %s\nScene: Plain beige background\n" % K_DIALOG)
    os.makedirs(COMBAT)
    for p in kampf:
        shutil.copy2(p, COMBAT)
    flee = os.path.join(COMBAT, "flee.png")
    Image.open(flee).transpose(Image.FLIP_LEFT_RIGHT).save(flee)
    with open(os.path.join(COMBAT, "_flee_gespiegelt.txt"), "w", encoding="utf-8") as f:
        f.write("flee.png horizontal gespiegelt (laeuft nach rechts weg)\n")
    with open(os.path.join(COMBAT, "_outfit_meta.json"), "w", encoding="utf-8") as f:
        json.dump({"karten": ["kampf_maxwellsteelmop"], "kategorien": ["kampf"]}, f, indent=1)
    d = ps("/api/state")["decks"]
    da = {c["name"]: c for c in d["outfit"]}
    for kn, text, tag in (("maximum_steelmop", K_DIALOG, "eden_maximum"), ("kampf_maxwellsteelmop", K_KAMPF, "kampf")):
        if kn in da:
            da[kn]["prompt"] = text
        else:
            d["outfit"].append({"name": kn, "prompt": text, "on": True, "tag": tag, "sel": False, "back_prompt": text + ", seen from behind"})
    ps("/api/decks", d)
    presets, sets = dc.load_json(F_PRESETS, None, "Studio"), dc.load_json(F_SETS, None, "Studio")
    k = json.loads(json.dumps(presets["Kampf_MaxwellMaximum"]))
    k.update({"cards_on": {"outfit": ["kampf_maxwellsteelmop"], "setting": ["A Sprite Background"]}, "st_set": "combat/MaxwellSteelMop", "sp_char": "Kampf_MaxwellSteelMop",
              "sp_stchar": "MaxwellSteelMop", "st_src": COMBAT, "st_dst": COMBAT, "modell": MODELL_NAME, "tags_on": [t for t in k["tags_on"] if t not in ("M Abs", "M Skin: Oiled")]})
    presets["Kampf_MaxwellSteelMop"] = k
    sets["Kampf_MaxwellSteelMop|Kampf"] = {"outfit": ["kampf_maxwellsteelmop"], "setting": ["A Sprite Background"], "tags": k["tags_on"]}
    sets["Yacht_Maximum|SteelMop"] = {"outfit": ["maximum_steelmop"], "setting": ["A Sprite Background"], "tags": ["M Body: Bodybuilder", "M Face: Goatee", "M Hair: Bald Shine", "M Skin: Deep Brown", "M Tall", "M Veins", "View: Front"]}
    if "SteelMop" not in presets["Yacht_Maximum"].get("sp_kost", []):
        presets["Yacht_Maximum"].setdefault("sp_kost", []).append("SteelMop")
    dc.save_json(F_PRESETS, presets, "Studio")
    dc.save_json(F_SETS, sets, "Studio")
    print(len(glob.glob(os.path.join(ziel, "*.png"))), "Bilder in", ziel, "|", len(glob.glob(os.path.join(COMBAT, "*.png"))), "in", COMBAT)


if __name__ == "__main__":
    main()
