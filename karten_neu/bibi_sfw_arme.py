# -*- coding: utf-8 -*-
r"""Bibi optimism_2 und relief_2 mit niedrigeren Armen (Duc 30.10.2026, Abnahme bibi_sfw). Die Kartentexte gelten nur fuer
diesen Lauf und gehen danach zurueck: Die Karten teilen sich alle Figuren.

    bibi_sfw_arme.py --los
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bibi_sfw_neu as B  # noqa: E402

TEXTE = {"optimism_2": "She stands upright on tiptoes with both hands clasped in front of her chest, elbows close to her body, "
                       "chest lifted, head tilted slightly up. Hopeful bright-eyed face, wide easy smile, brows lifted with "
                       "anticipation.",
         "relief_2": "She stands with both knees slightly bent and her shoulders dropping, one hand resting flat on her chest, "
                     "the other arm hanging loose at her side. Relieved unwinding face, eyes closed, a long breathy smile."}


def main():
    st = B.ps("/api/state")
    alt_preset = st["cfg"].get("preset_active")
    B.ps("/api/presets", {"action": "load", "name": B.PRESET})
    kp = B.ps("/api/set_preset_laden", {"char": B.PRESET, "kost": B.KOST})
    st = B.ps("/api/state")
    d = st["decks"]
    alt = {c["name"]: c["prompt"] for c in d["st"]}
    for k in TEXTE:
        f = os.path.join(B.ROH, k + ".png")
        if os.path.isfile(f):
            os.makedirs(B.KORB, exist_ok=True)
            B.shutil.move(f, B.KORB)
    try:
        sets = set(kp.get("tags") or [])
        tags = st["cfg"]["tags"]
        for t in tags:
            t["on"] = t["name"] in sets
        for deck in ("outfit", "setting", "st", "kampf"):
            for c in d[deck]:
                c["sel"] = False
        for c in d["outfit"]:
            c["sel"] = c["name"] == B.KARTE
        for c in d["setting"]:
            c["sel"] = c["name"] in set(kp.get("setting") or [])
        for c in d["st"]:
            if c["name"] in TEXTE:
                c["prompt"], c["sel"] = TEXTE[c["name"]], True
        B.ps("/api/config", {"tags": tags, "mode": "sprite", "st_set": B.ST_SET, "view_pro_karte": True, "combine_mode": "all",
                             "st_rembg": True, "st_crop": True})
        B.ps("/api/decks", d)
        print("eingereiht:", B.ps("/api/queue", {"cfg": {}, "decks": d, "max_auftraege": len(TEXTE)}).get("queued", 0))
    finally:
        d = B.ps("/api/state")["decks"]
        for c in d["st"]:
            if c["name"] in TEXTE:
                c["prompt"] = alt[c["name"]]
        B.ps("/api/decks", d)
        B.ps("/api/config", {"view_pro_karte": False})
        if alt_preset:
            B.ps("/api/presets", {"action": "load", "name": alt_preset})


if __name__ == "__main__":
    main()
