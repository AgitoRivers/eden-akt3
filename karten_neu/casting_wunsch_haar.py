# -*- coding: utf-8 -*-
r"""Casting Frisuren zu den Wunsch-Outfits (Duc 31.10.2026): die von Duc gemochten Outfits mit einer Frisur, die anders aussieht als sonst.
Neue Frisuren kommen als Tags in den Studio-Katalog, die Haarfarbe bleibt die der Figur.

    casting_wunsch_haar.py          Probelauf
    casting_wunsch_haar.py --los    Presets Yacht_<Figur>_<Art>_Haar, je 1 Portrait -> output\expressions\_casting_wunsch_haar
"""
import json, os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, r"X:\AI\DucCommon")
LOS = "--los" in sys.argv
import casting_wunsch_outfits as cw  # noqa: E402
cd, dc = cw.cd, cw.dc

ORDNER, SEED = "_casting_wunsch_haar", int(os.environ.get("HAAR_SEED", 240611))
NEUE_TAGS = {
    "Style: Hollywood Waves": "long glossy old Hollywood waves with a deep side part, all brushed over one shoulder",
    "Style: Finger Waves": "a glossy chin-length 1930s finger wave bob, pinned flat on one side",
    "Style: Helmet Shake": "long thick hair just shaken out of a helmet, flat at the crown, tousled and loose at the ends, falling over one shoulder",
    "Style: Low Chignon": "a centre parting and a smooth low chignon at the nape, Andalusian style",
    "Style: Flamenco Mane": "very long thick loose hair falling to her waist from under the hat, heavy glossy waves with a centre parting, one thin braid running through the loose hair on one side",
    "Style: Hime Cut": "very long straight hair with blunt straight bangs and straight side locks cut at cheek height",
}
# (Figur, Art): (Frisur, Zustand oder None). Art "Whites" = Chis Dress Whites aus casting_dress_whites.py
LOOKS = {
    ("Lea", "D"): ("Style: Hollywood Waves", None),
    ("Sophia", "W"): ("Style: Finger Waves", None),
    ("Rosi", "W"): ("Style: Helmet Shake", None),
    ("Rosi", "A"): ("Style: Blowout", None),
    ("Siri", "K"): ("Style: Double Braids", None),
    ("Siri", "D"): ("Style: Sleek Bun", None),
    ("Alva", "W"): ("Style: Flamenco Mane", None),
    ("Alva", "K"): ("Style: Bun", "State: Tendrils"),
    ("Megan", "W"): ("Style: Hime Cut", None),
    ("Megan", "D"): ("Style: Sleek Ponytail", None),
    ("Chiara", "Whites"): ("Style: Sleek Bun", None),
}


def main():
    st = cd.ps("/api/state")
    tags = st["cfg"]["tags"]
    kat = {t["name"]: t for t in tags}
    vorlage = kat["Style: Bob"]
    fehlen = [f for f, _ in LOOKS.values() if f not in kat and f not in NEUE_TAGS]
    if fehlen:
        raise SystemExit("Tags fehlen: %s" % fehlen)
    presets = dc.load_json(cd.F_PRESETS, None, "Studio")
    d = st["decks"]
    da = {c["name"]: c for c in d["outfit"]}
    neu = {}
    for (figur, art), (frisur, zustand) in LOOKS.items():
        if cw.NUR and "%s_%s" % (figur, art) not in cw.NUR:
            continue
        quelle = "Yacht_Chiara_Whites_5" if art == "Whites" else "Yacht_%s_%s" % (figur, art)
        p = json.loads(json.dumps(presets[quelle]))
        rest = [t for t in p["tags_on"] if not t.startswith(("Style:", "State:")) or t == "State: Dirty"]
        p["tags_on"] = rest + [frisur] + ([zustand] if zustand else [])
        p.update({"st_set": "%s/%s_%s" % (ORDNER, figur, art), "created": cd.JETZT, "updated": cd.JETZT})
        if art != "Whites":
            kn = "wunsch_%s_%s" % (figur.lower(), art)
            outfit = cw.OUTFITS[figur][art]
            da[kn]["prompt"] = outfit
            da[kn]["back_prompt"] = outfit + ", seen from behind"
        neu["Yacht_%s_%s_Haar" % (figur, art)] = p
    print({k: p["tags_on"] for k, p in neu.items()})
    if not LOS:
        print("Probelauf - nichts geschrieben.")
        return
    for name, prompt in NEUE_TAGS.items():
        if name not in kat:
            tags.append(dict(vorlage, name=name, prompt=prompt, on=False))
    cd.ps("/api/config", {"tags": tags})
    cd.ps("/api/decks", d)
    presets.update(neu)
    dc.save_json(cd.F_PRESETS, presets, "Studio")
    st = cd.ps("/api/state")
    alt = {k: st["cfg"].get(k) for k in ("sprite_prompt", "loras", "st_set", "sprite_src", "tags", "unet", "clip", "seed")}
    alt_preset = st["cfg"].get("preset_active")
    n = 0
    try:
        for pn, p in neu.items():
            kn = p["cards_on"]["outfit"][0]
            cd.ps("/api/presets", {"action": "load", "name": pn})
            cfg = cd.ps("/api/state")["cfg"]
            cd.ps("/api/config", dict(tags=cfg["tags"], mode="sprite", sprite_src="t2i", combine_mode="all", view_pro_karte=False, st_rembg=False, st_crop=False,
                                      seed=SEED, st_set=p["st_set"], loras=p["loras"], sprite_prompt=p["sprite_prompt"]))
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
