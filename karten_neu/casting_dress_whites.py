# -*- coding: utf-8 -*-
r"""Casting Dress Whites (Duc 31.10.2026, systeme/schneider.md): Chiaras Wunsch-Massstueck von Danzel, weiss, leere Aermel. Vier Varianten.

    casting_dress_whites.py          Probelauf
    casting_dress_whites.py --los    Presets Yacht_Chiara_Whites_1..4, je 2 Portraits -> output\expressions\_casting_dress_whites

Yacht_Chiara bleibt unberuehrt: Tags, Subject und LoRAs kommen live aus dem Preset, nur die Outfit-Karte und der Zielordner sind neu.
"""
import json, os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, r"X:\AI\DucCommon")
LOS = "--los" in sys.argv
NUR = [a for a in sys.argv[1:] if a.isdigit()]   # nur diese Looks rendern
sys.argv = [sys.argv[0]] + (["--los"] if LOS else [])
import castings_danzel as cd  # noqa: E402
import duc_common as dc  # noqa: E402

BASIS, ORDNER, TAG = "Yacht_Chiara", "_casting_dress_whites", "eden_dress_whites"
OUTFITS = {
    "1": "a short fitted bright white wool double-breasted mess jacket with crisp level shoulders, red coral buttons and completely plain smooth white cuffs, worn open over a thin white silk camisole with a deep neckline, high-waisted wide-leg white sailor trousers with a slim gold belt, white deck sneakers, a slim gold watch",
    "2": "a bright white tailored double-breasted officer's jacket buttoned tight at the waist with red coral buttons, a deep plunging V neckline with nothing visible beneath it, crisp level shoulders and completely plain smooth white cuffs, high-waisted wide-leg white sailor trousers with a double row of coral buttons at the front, white deck sneakers, a slim gold watch",
    "3": "a bright white fitted short-sleeve captain's shirt with blank white shoulder boards and red coral buttons, unbuttoned low with deep cleavage and knotted at the waist showing her midriff, high-waisted wide-leg white sailor trousers with a slim gold belt, white deck sneakers, a slim gold watch",
    "4": "a bright white wool officer's jacket with red coral buttons, crisp level shoulders and completely plain smooth white cuffs, draped over her shoulders like a cape with her arms free, over a sleeveless white halter jumpsuit with a deep plunging neckline, a cinched waist and wide legs, a slim gold belt, white deck sneakers",
    "5": "a bright white tailored double-breasted officer's jacket buttoned tight at the waist with pale blue-green aquamarine gemstone buttons, a deep plunging V neckline with nothing visible beneath it, crisp level shoulders and completely plain smooth white cuffs, high-waisted wide-leg white sailor trousers with a double row of pale blue-green aquamarine buttons at the front, white deck sneakers, a slim gold watch",
}


def main():
    for k in [k for k in OUTFITS if NUR and k not in NUR]:
        del OUTFITS[k]
    print(BASIS, "/".join(OUTFITS))
    if not LOS:
        print("Probelauf - nichts geschrieben.")
        return
    presets = dc.load_json(cd.F_PRESETS, None, "Studio")
    st = cd.ps("/api/state")
    d = st["decks"]
    da = {c["name"]: c for c in d["outfit"]}
    for nr, outfit in OUTFITS.items():
        kn = "chiara_whites_%s" % nr
        if kn in da:
            da[kn]["prompt"] = outfit
        else:
            d["outfit"].append({"name": kn, "prompt": outfit, "on": True, "tag": TAG, "sel": False, "back_prompt": outfit + ", seen from behind"})
    cd.ps("/api/decks", d)
    neu = {}
    for nr in OUTFITS:
        p = json.loads(json.dumps(presets[BASIS]))
        p.update({"cards_on": {"outfit": ["chiara_whites_%s" % nr], "setting": ["A Sprite Background"], "st": ["neutral"]},
                  "st_set": "%s/%s_Whites_%s" % (ORDNER, BASIS, nr), "created": cd.JETZT, "updated": cd.JETZT})
        neu["%s_Whites_%s" % (BASIS, nr)] = p
    presets.update(neu)
    dc.save_json(cd.F_PRESETS, presets, "Studio")
    alt = {k: st["cfg"].get(k) for k in ("sprite_prompt", "loras", "st_set", "sprite_src", "tags", "unet", "clip", "seed")}
    alt_preset = st["cfg"].get("preset_active")
    n = 0
    try:
        for pn, p in neu.items():
            kn = p["cards_on"]["outfit"][0]
            cd.ps("/api/presets", {"action": "load", "name": pn})
            cfg = cd.ps("/api/state")["cfg"]
            print(pn, "Tags an:", [t["name"] for t in cfg["tags"] if t.get("on")])
            for s in cd.SEEDS:
                cd.ps("/api/config", dict(tags=cfg["tags"], mode="sprite", sprite_src="t2i", combine_mode="all", view_pro_karte=False, st_rembg=False, st_crop=False,
                                          seed=s, st_set=p["st_set"], loras=p["loras"], sprite_prompt=p["sprite_prompt"]))
                dk = cd.ps("/api/state")["decks"]
                for kk in dk:
                    wahl = {"outfit": {kn}, "setting": {"A Sprite Background"}, "st": {"neutral"}}.get(kk, set())
                    for x in dk[kk]:
                        x["sel"] = x["name"] in wahl
                n += cd.ps("/api/queue", {"cfg": {"combine_mode": "all"}, "decks": dk}).get("queued", 0)
    finally:
        if alt_preset:
            cd.ps("/api/presets", {"action": "load", "name": alt_preset})
        cd.ps("/api/config", {k: v for k, v in alt.items() if v is not None})
    print("%d Portraits in der Warteschlange -> expressions\\%s" % (n, ORDNER))


if __name__ == "__main__":
    main()
