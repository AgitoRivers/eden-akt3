# -*- coding: utf-8 -*-
r"""Fertige Wunsch-Sets ins Spiel (Duc 31.10.2026): roh -> Sorted ueber Prompt Studio, dann als neuer Set-Ordner setN in die ST-Karte der Figur.
Vorhandene Sets bleiben unberuehrt, ein schon angelegter Set-Name bricht ab. Bilder mit Fehler (WEG) kommen nicht mit.

    wunsch_einbau.py <Satz>          Probelauf
    wunsch_einbau.py <Satz> --los
"""
import glob, json, os, re, shutil, sys, tempfile, urllib.request

PS = "http://127.0.0.1:8301"
SATZ = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions\_wunsch_sets"
ST = r"X:\AI\SillyTavern3\SillyTavern-Launcher\SillyTavern\data\default-user\characters"
# Satz: (ST-Karte, Set-Name, Outfit-Karte, Bilder, die wegen Bildfehlern nicht mitkommen)
SAETZE = {"Sophia_Reading": ("Sophia Moore", "Book Reading", "wunsch_sophia_W", {"caring_2", "joy_2", "optimism_2"}),
          "Chiara_Whites": ("Chiara Sonnberg", "Dress Whites", "chiara_whites_6", set())}


def ps(pfad, daten=None):
    req = urllib.request.Request(PS + pfad, data=None if daten is None else json.dumps(daten).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def main():
    satz = sys.argv[1]
    karte, name, outfit, weg = SAETZE[satz]
    basis = os.path.join(ST, karte)
    for d in [basis] + glob.glob(os.path.join(basis, "set*")):
        if open(os.path.join(d, "_name.txt"), encoding="utf-8").read().strip() == name:
            sys.exit("Set %s gibt es schon: %s" % (name, d))
    nr = 1 + max(int(m.group(1)) for m in (re.fullmatch(r"set(\d+)", x) for x in os.listdir(basis)) if m)
    ziel = os.path.join(basis, "set%d" % nr)
    roh = os.path.join(SATZ, satz, "roh")
    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, "roh")
        os.makedirs(src)
        for f in glob.glob(os.path.join(roh, "*.png")):
            if os.path.basename(f)[:-4] not in weg:
                shutil.copy2(f, src)
        n = len(os.listdir(src))
        print(satz, "->", ziel, name, "| Bilder", n, "| ohne", sorted(weg))
        plan = ps("/api/sprites", {"quellen": [{"kost": name, "src": src}], "move": False})
        print("geplant", plan.get("planned"))
        if "--los" not in sys.argv:
            sys.exit("PROBELAUF - mit --los einbauen")
        r = ps("/api/sprites", {"quellen": [{"kost": name, "src": src}], "move": False, "apply": True})
        srt = os.path.join(tmp, "Sorted")
        neu = glob.glob(os.path.join(srt, "*.png"))
        assert r.get("done") == n and len(neu) == n, (r.get("done"), len(neu), n)
        os.makedirs(ziel)
        for f in neu:
            shutil.copy2(f, ziel)
    with open(os.path.join(ziel, "_name.txt"), "w", encoding="utf-8") as fh:
        fh.write(name)
    karten = {c["name"]: c["prompt"] for c in ps("/api/state")["decks"]["outfit"]}
    with open(os.path.join(ziel, "_prompt.txt"), "w", encoding="utf-8") as fh:
        fh.write("Wearing: %s\nScene: Plain beige background\n" % karten[outfit])
    print(len(glob.glob(os.path.join(ziel, "*.png"))), "Bilder in", ziel)


if __name__ == "__main__":
    main()
