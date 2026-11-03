# -*- coding: utf-8 -*-
r"""Abnahme der Bar-Sets (Duc 30.10.2026): Charly und Bibi Kostuem Bikini, Danzel Kostuem Bath -> docs\abnahme\bar_sets\spec.json."""
import glob, json, os

EXPR = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions"
ZIEL = r"X:\AI\Eden\docs\abnahme\bar_sets\spec.json"
SETS = [("Yacht_Bibi", "Bikini", "Bibi", "Stoff deckt die Brust, Haende im Bild"),
        ("Yacht_Charly", "Bikini", "Charly", "Haende im Bild, Top-Knot, Hibiskus"),
        ("Yacht_Danzel", "Bath", "Danzel", "Badehose, offenes Hemd, Hibiskus in der Tasche")]
items = []
for char, kost, name, soll in SETS:
    for f in sorted(glob.glob(os.path.join(EXPR, char, kost, "roh", "*.png"))):
        pose = os.path.basename(f)[:-4]
        items.append({"id": "%s_%s" % (name, pose), "titel": "%s: %s" % (name, pose), "bild": f, "soll": soll})
os.makedirs(os.path.dirname(ZIEL), exist_ok=True)
json.dump({"id": "bar_sets", "titel": "Bar-Sets Mochi's", "hinweis": "Bibi: curiosity_back und embarrassment_back fehlen absichtlich, dort lag der Stoff nicht. "
           "Bei Bibi drueckt sich der Stoff in manchen Posen durch: Neu markieren, wo es dich stoert.", "items": items},
          open(ZIEL, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(items))
