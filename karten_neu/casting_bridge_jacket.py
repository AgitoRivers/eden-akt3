# -*- coding: utf-8 -*-
r"""Casting Bridge Jacket (Duc 30.10.2026, systeme/schneider.md): Chiaras Massstueck von Danzel, Pilot fuer neue Outfits.

    casting_bridge_jacket.py          Probelauf
    casting_bridge_jacket.py --los    Presets Yacht_Chiara_Bridge_1..3, je 2 Portraits -> output\expressions\_casting_bridge_jacket

Yacht_Chiara bleibt unberuehrt: Tags, Subject und LoRAs kommen live aus dem Preset, nur die Outfit-Karte und der Zielordner sind neu.
"""
import json, os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, r"X:\AI\DucCommon")
LOS = "--los" in sys.argv
sys.argv = [sys.argv[0]] + (["--los"] if LOS else [])
import castings_danzel as cd  # noqa: E402
import duc_common as dc  # noqa: E402

BASIS, ORDNER, TAG = "Yacht_Chiara", "_casting_bridge_jacket", "eden_bridge_jacket"
OUTFITS = {
    "1": "a fitted navy wool double-breasted officer's jacket with perfectly level squared shoulders and large plain red coral buttons, worn open over a white "
         "low-cut crew blouse unbuttoned with deep cleavage, a tight navy pencil skort ending high on her thighs, a slim gold watch, white deck sneakers",
    "2": "a cropped navy wool jacket with sharply tailored level shoulders and two plain red coral buttons, cut short above the waist, worn over a fitted white tank top "
         "with a deep neckline, high-waisted white sailor shorts, a slim gold watch, white deck sneakers",
    "3": "a long navy wool tailored jacket cinched tight at the waist with one single red coral button, a deep V neckline with nothing visible beneath it, sharply level "
         "squared shoulders, worn as a very short jacket dress ending high on her thighs, a slim gold watch, white deck sneakers",
}


def main():
    print(BASIS, "/".join(OUTFITS))
    if not LOS:
        print("Probelauf - nichts geschrieben.")
        return
    presets = dc.load_json(cd.F_PRESETS, None, "Studio")
    st = cd.ps("/api/state")
    d = st["decks"]
    da = {c["name"]: c for c in d["outfit"]}
    for nr, outfit in OUTFITS.items():
        kn = "chiara_bridge_%s" % nr
        if kn in da:
            da[kn]["prompt"] = outfit
        else:
            d["outfit"].append({"name": kn, "prompt": outfit, "on": True, "tag": TAG, "sel": False, "back_prompt": outfit + ", seen from behind"})
    cd.ps("/api/decks", d)
    neu = {}
    for nr in OUTFITS:
        p = json.loads(json.dumps(presets[BASIS]))
        p.update({"cards_on": {"outfit": ["chiara_bridge_%s" % nr], "setting": ["A Sprite Background"], "st": ["neutral"]},
                  "st_set": "%s/%s_Bridge_%s" % (ORDNER, BASIS, nr), "created": cd.JETZT, "updated": cd.JETZT})
        neu["%s_Bridge_%s" % (BASIS, nr)] = p
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
