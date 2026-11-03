# -*- coding: utf-8 -*-
r"""Two new costumes for Alva (23.10.2026, Duc): "Festa" (public flamenco stage dress for the Festa scene, romance
step 5) and "Morgen" (silk kimono for romance step 4, the morning with her father's photo). Plain colours, no dots
or small repeating patterns (trypophobia). Writes outfit cards via the Studio API and the costume presets via
DucCommon; no rendering.

    alva_outfits_festa_morgen.py          dry run
    alva_outfits_festa_morgen.py --los    enter cards + costume presets
"""
import io, json, os, sys, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, r"X:\AI\DucCommon")
import duc_common as dc  # noqa: E402

PS = "http://127.0.0.1:8301"
F_PRESETS, F_SETS = r"X:\AI\PromptStudio\presets.json", r"X:\AI\PromptStudio\set_presets.json"
EXPR = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions\Yacht_Alva"
CHAR = "Yacht_Alva"
NEW = {
    "Festa": ("alva_festa",
              "a long floor-length red flamenco dress with tiers of solid red ruffles flaring at the hem, a fitted bodice "
              "with a sweetheart neckline, a cream silk shawl with long fringes over her shoulders, a large red rose in "
              "her hair, red flamenco shoes, a pair of castanets in her hands, golden necklace with golden rose"),
    "Morgen": ("alva_morgen",
               "a loosely tied deep red silk kimono robe with a few large painted white cranes, bare legs, barefoot, her "
               "hair down and slightly tousled, holding a small cup of espresso, golden necklace with golden rose"),
}


def ps(path, data=None):
    req = urllib.request.Request(PS + path, data=None if data is None else json.dumps(data).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


sets = dc.load_json(F_SETS, None, "Studio")
base_tags = sets[CHAR + "|Standard"]["tags"]
for kost, (card, prompt) in NEW.items():
    print("%-7s %-12s %s" % (kost, card, prompt))
if "--los" not in sys.argv:
    sys.exit("PROBELAUF - mit --los eintragen")

d = ps("/api/state")["decks"]
cards = {c["name"]: c for c in d["outfit"]}
for kost, (card, prompt) in NEW.items():
    if card in cards:
        cards[card]["prompt"] = prompt
    else:
        d["outfit"].append({"name": card, "prompt": prompt, "on": True, "tag": "eden-npc", "sel": False,
                            "back_prompt": ""})
ps("/api/decks", d)

presets = dc.load_json(F_PRESETS, None, "Studio")
p = presets[CHAR]
for kost, (card, _) in NEW.items():
    sets["%s|%s" % (CHAR, kost)] = {"outfit": [card], "setting": ["A Sprite Background"], "tags": list(base_tags)}
    if kost not in p["sp_kost"]:
        p["sp_kost"].append(kost)
    folder = os.path.join(EXPR, kost, "Sorted")
    if folder not in p["sv_sets"]:
        p["sv_sets"].append(folder)
dc.save_json(F_SETS, sets, "Studio")
dc.save_json(F_PRESETS, presets, "Studio")
print("eingetragen: %s, Kostueme jetzt: %s" % (", ".join(NEW), ", ".join(p["sp_kost"])))
