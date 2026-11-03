# -*- coding: utf-8 -*-
r"""NPC-Sets der Dorf-Figuren und Adrien ins Spiel (Duc 30.10.2026, Abnahme sets_vorschau und sets_dorf): roh -> Sorted ueber Prompt
Studio, dann nach module\eden_rise\figuren\<Ordner>. Alte Bilder im Ordner wandern vorher in den Papierkorb.

    dorf_einbau.py          Probelauf
    dorf_einbau.py --los
"""
import glob, json, os, shutil, sys, time, urllib.request

PS = "http://127.0.0.1:8301"
E = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions"
FIG = r"X:\AI\Eden\module\eden_rise\figuren"
KORB = r"X:\AI\ComfyUI_krea2\ComfyUI\output\_expressions_papierkorb\figuren_dorf_" + time.strftime("%Y%m%d_%H%M")
# Preset: (Ordner im Spiel, Set-Name)
SETS = {"Yacht_Pascal": ("Pascal Leca", "pascal_standard"), "Yacht_BaTu": ("Ba Tu", "batu_standard"),
        "Yacht_Sandru": ("Sandru Amrani", "sandru_av"), "Yacht_Anghjulu": ("Don Anghjulu", "anghjulu_standard"),
        "Yacht_AdrienNeu": ("Adrien Morel", "adrien_standard")}


def ps(pfad, daten=None):
    req = urllib.request.Request(PS + pfad, data=None if daten is None else json.dumps(daten).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def main():
    st = ps("/api/state")
    karten = {c["name"]: c["prompt"] for c in st["decks"]["outfit"]}
    sets = json.load(open(r"X:\AI\PromptStudio\set_presets.json", encoding="utf-8"))
    for preset, (ordner, name) in SETS.items():
        roh = os.path.join(E, preset, "Standard", "roh")
        n = len(glob.glob(os.path.join(roh, "*.png")))
        plan = ps("/api/sprites", {"quellen": [{"kost": "Standard", "src": roh}], "move": False})
        print("%-16s %-16s %-18s roh %d, geplant %s" % (preset, ordner, name, n, plan.get("planned")))
        assert n == 22, preset
    if "--los" not in sys.argv:
        sys.exit("PROBELAUF - mit --los einbauen")
    os.makedirs(KORB, exist_ok=True)
    for preset, (ordner, name) in SETS.items():
        roh = os.path.join(E, preset, "Standard", "roh")
        srt = os.path.join(E, preset, "Standard", "Sorted")
        r = ps("/api/sprites", {"quellen": [{"kost": "Standard", "src": roh}], "move": False, "apply": True})
        neu = glob.glob(os.path.join(srt, "*.png"))
        assert r.get("done") == 22 and len(neu) == 22, (preset, r.get("done"), len(neu))
        ziel = os.path.join(FIG, ordner)
        if os.path.isdir(ziel):
            shutil.copytree(ziel, os.path.join(KORB, ordner))           # Sicherung, auch _name und _prompt
            for f in glob.glob(os.path.join(ziel, "*.png")):
                os.remove(f)
        os.makedirs(ziel, exist_ok=True)
        for f in neu:
            shutil.copy2(f, ziel)
        with open(os.path.join(ziel, "_name.txt"), "w", encoding="utf-8") as fh:
            fh.write(name)
        outfit = (sets.get(preset + "|Standard") or {}).get("outfit") or []
        prompt = karten.get(outfit[0], "") if outfit else ""
        with open(os.path.join(ziel, "_prompt.txt"), "w", encoding="utf-8") as fh:
            fh.write("Wearing: %s\nScene: Plain beige background\n" % prompt)
        print(ordner, "->", len(glob.glob(os.path.join(ziel, "*.png"))), "Bilder; Outfit:", prompt[:60])
    print("Sicherung in", KORB)


if __name__ == "__main__":
    main()
