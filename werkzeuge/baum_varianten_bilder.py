# -*- coding: utf-8 -*-
r"""Drei weitere Baum-Sprites und die Item-Bilder Schiefer und Stahl (Duc 30.10.2026).

    python werkzeuge\baum_varianten_bilder.py     Kandidaten in docs\abnahme\baum_varianten\, Spec docs\abnahme\baum_varianten.json

Ueberschreibt nichts im Spiel. Positiv formuliert (Krea CFG 1: Verneinungen wirken nicht)."""
import json, os, random, sys, time

from PIL import Image

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import abbau_bilder as A  # noqa: E402
import rast_kreis_bilder as RK  # noqa: E402

K, IB = A.K, A.IB
ZIEL = os.path.join(K.EDEN, "docs", "abnahme", "baum_varianten")
SPEC = os.path.join(K.EDEN, "docs", "abnahme", "baum_varianten.json")
SEEDS = 2
BAEUME = {
    "holm_oak_2": ("Steineiche, alt und breit", "an old broad holm oak tree, a short thick gnarled trunk with dark grey furrowed bark, a wide "
                   "spreading low crown of small dark evergreen leaves"),
    "holm_oak_3": ("Steineiche, schlank mit zwei Stämmen", "a slender holm oak tree with two trunks rising from one base, dark grey bark, "
                   "a tall narrow oval crown of small dark evergreen leaves"),
    "cork_oak_2_vorher": ("Korkeiche, knorrig (mit Rinde)", "a gnarled old cork oak tree, one thick straight lower trunk fully covered in "
                          "thick pale ridged cork bark, a crooked fork high up and a broad open crown of grey-green leaves"),
}
ITEMS = {
    "slate_a": ("Schiefer A · Platten", "a rough stack of thin dark blue-grey slate slabs, layered split plates with sharp broken edges, matte stone"),
    "slate_b": ("Schiefer B · Bruch", "a heap of jagged broken dark charcoal-grey slate shards, flat layered pieces with sharp corners, matte stone"),
    "steel_a": ("Stahl A · Stangen", "a small stack of rough forged steel bars, dull blue-grey metal with hammer marks and dark mill scale"),
    "steel_b": ("Stahl B · Barren", "three plain rectangular steel ingots stacked on each other, brushed dull grey metal with rough cast edges"),
}


def erzeugen():
    os.makedirs(ZIEL, exist_ok=True)
    IB.get("/system_stats")

    def einreihen(name, prompt, sprite):
        seed = random.randint(1, 2 ** 31)
        g = K.graph_mit_freistellung(prompt, ZIEL, name, seed) if sprite else IB.graph(prompt, ZIEL, name, seed)
        if sprite:
            g["6"]["inputs"].update({"width": 896, "height": 1152})
        return IB.post("/prompt", {"prompt": g})["prompt_id"]

    offen, items = {}, []
    for iid, (titel, motiv) in BAEUME.items():
        prompt = A.BAUM_STIL.format(motiv=motiv, grund=K.GRUND)
        for n in range(1, SEEDS + 1):
            name = "%s_s%d" % (iid, n)
            offen[name] = (einreihen(name, prompt, True), prompt, True, 1)
            items.append({"id": name, "titel": "%s · Seed %d" % (titel, n), "bild": os.path.join(ZIEL, name + "_fertig.png"),
                          "soll": "Freigestellter Baum fürs Minispiel, ganz im Bild, deutlich anders als die Bestehenden.",
                          "vergleich": os.path.join(A.ZIEL, "cork_oak_vorher.png" if "cork" in iid else "holm_oak.png"),
                          "vergleich_titel": "Bestehender Baum"})
    for iid, (titel, motiv) in ITEMS.items():
        prompt = IB.STIL.format(motiv=motiv, hintergrund=RK.SCHRAEG)
        for n in range(1, SEEDS + 1):
            name = "%s_s%d" % (iid, n)
            offen[name] = (einreihen(name, prompt, False), prompt, False, 1)
            items.append({"id": name, "titel": "%s · Seed %d" % (titel, n), "bild": os.path.join(ZIEL, name + ".webp"),
                          "soll": "Item-Bild im Leinen-Look, bewusst grob."})
    print("eingereiht: %d" % len(offen), flush=True)
    t0 = time.time()
    while offen and time.time() - t0 < 60 * 40:
        time.sleep(2)
        for name, (pid, prompt, sprite, versuch) in list(offen.items()):
            h = IB.get("/history/" + pid)
            if not (pid in h and h[pid].get("status", {}).get("completed")):
                continue
            if sprite:
                ziel = os.path.join(ZIEL, name + "_fertig.png")
                if not K.sprite_fertig(ZIEL, name, ziel, letzter=versuch >= K.VERSUCHE) and versuch < K.VERSUCHE:
                    offen[name] = (einreihen(name, prompt, True), prompt, True, versuch + 1)
                    print("angeschnitten, Versuch %d: %s" % (versuch + 1, name), flush=True)
                    continue
            else:
                IB.thumbnail(ZIEL, ZIEL, name)
            print("fertig: %s" % name, flush=True)
            offen.pop(name)
    print("offen: %s" % (", ".join(offen) or "nichts"), flush=True)
    json.dump({"id": "baum_varianten_v1", "titel": "Drei neue Bäume, Schiefer und Stahl",
               "hinweis": "Je Motiv das beste Bild mit OK markieren.", "items": items},
              open(SPEC, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Spec: %s (%d Bilder)" % (SPEC, len(items)), flush=True)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    erzeugen()
