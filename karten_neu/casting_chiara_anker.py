# -*- coding: utf-8 -*-
r"""Test Chis Dress Whites mit goldenem Anker-Pin und offenen, gestylten Haaren (Duc 31.10.2026).
Outfit ist Look 5 (Aquamarin) plus Pin. Zwei Frisuren, je zwei Seeds.

    casting_chiara_anker.py          Probelauf
    casting_chiara_anker.py --los    Presets Yacht_Chiara_Whites_Anker_<a|b>, 4 Portraits -> output\expressions\_casting_chiara_anker
"""
import json, os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, r"X:\AI\DucCommon")
LOS = "--los" in sys.argv
sys.argv = [sys.argv[0]] + (["--los"] if LOS else [])
import castings_danzel as cd  # noqa: E402
import duc_common as dc  # noqa: E402

BASIS, QUELLE, ORDNER, KARTE = "Yacht_Chiara_Whites_Anker", "Yacht_Chiara_Whites_5", "_casting_chiara_anker", "chiara_whites_6"
SEEDS = (240611, 977031)
NEUE_TAGS = {"Style: Open Sculpted Waves": "long open hair with a deep side part, smooth sculpted glossy waves falling behind her shoulders, her chest and jacket in clear view"}
FRISUREN = {"a": "Style: Open Sculpted Waves", "b": "Style: Blowout"}
PIN = ", a small solid gold anchor pin on the jacket, on the right side of her chest"


def main():
    st = cd.ps("/api/state")
    d = st["decks"]
    da = {c["name"]: c for c in d["outfit"]}
    outfit = da["chiara_whites_5"]["prompt"] + PIN
    print(outfit)
    print(FRISUREN)
    if not LOS:
        print("Probelauf - nichts geschrieben.")
        return
    tags = st["cfg"]["tags"]
    kat = {t["name"]: t for t in tags}
    for name, prompt in NEUE_TAGS.items():
        if name not in kat:
            tags.append(dict(kat["Style: Bob"], name=name, prompt=prompt, on=False))
    cd.ps("/api/config", {"tags": tags})
    if KARTE in da:
        da[KARTE]["prompt"] = outfit
    else:
        d["outfit"].append({"name": KARTE, "prompt": outfit, "on": True, "tag": "eden_dress_whites", "sel": False, "back_prompt": outfit + ", seen from behind"})
    cd.ps("/api/decks", d)
    presets = dc.load_json(cd.F_PRESETS, None, "Studio")
    neu = {}
    for k, frisur in FRISUREN.items():
        p = json.loads(json.dumps(presets[QUELLE]))
        p["tags_on"] = [t for t in p["tags_on"] if not t.startswith(("Style:", "State:"))] + [frisur]
        p.update({"cards_on": {"outfit": [KARTE], "setting": ["A Sprite Background"], "st": ["neutral"]},
                  "st_set": "%s/%s" % (ORDNER, k), "created": cd.JETZT, "updated": cd.JETZT})
        neu["%s_%s" % (BASIS, k)] = p
    presets.update(neu)
    dc.save_json(cd.F_PRESETS, presets, "Studio")
    st = cd.ps("/api/state")
    alt = {k: st["cfg"].get(k) for k in ("sprite_prompt", "loras", "st_set", "sprite_src", "tags", "unet", "clip", "seed")}
    alt_preset = st["cfg"].get("preset_active")
    n = 0
    try:
        for pn, p in neu.items():
            cd.ps("/api/presets", {"action": "load", "name": pn})
            cfg = cd.ps("/api/state")["cfg"]
            for s in SEEDS:
                cd.ps("/api/config", dict(tags=cfg["tags"], mode="sprite", sprite_src="t2i", combine_mode="all", view_pro_karte=False, st_rembg=False, st_crop=False,
                                          seed=s, st_set=p["st_set"], loras=p["loras"], sprite_prompt=p["sprite_prompt"]))
                dk = cd.ps("/api/state")["decks"]
                for kk in dk:
                    wahl = {"outfit": {KARTE}, "setting": {"A Sprite Background"}, "st": {"neutral"}}.get(kk, set())
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
