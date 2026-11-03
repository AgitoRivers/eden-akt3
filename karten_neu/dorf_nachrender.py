# -*- coding: utf-8 -*-
r"""Dorf-Sets nachrendern (Duc 30.10.2026): love_2 und abgeschnittene Haende im Querformat, Pascal disappointment im Stehen. Karten
und Config werden danach zurueckgesetzt, alte Bilder wandern in den Papierkorb.

    dorf_nachrender.py --los
"""
import json, os, shutil, sys, time, urllib.request

PS = "http://127.0.0.1:8301"
E = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions"
KORB = r"X:\AI\ComfyUI_krea2\ComfyUI\output\_expressions_papierkorb\dorf_nachrender_" + time.strftime("%Y%m%d_%H%M")
# Preset: {Karte: (Querformat, Kartentext oder None)}
GANZ = (" The camera is far back, her or his whole body is in the picture from the head down to the shoes, both feet on the floor, "
        "wide empty space on all sides.")
PLAN = {
    "Yacht_Pascal": {"admiration_2": (True, GANZ), "love_2": (True, GANZ)},
    "Yacht_Anghjulu": {"love_2": (True, GANZ)},
}
KEYS = ("sprite_prompt", "st_set", "tags", "decks_visible", "mode_opts", "aspect", "width", "height")


def ps(pfad, daten=None):
    req = urllib.request.Request(PS + pfad, data=None if daten is None else json.dumps(daten).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def main():
    if "--los" not in sys.argv:
        sys.exit("PROBELAUF - mit --los einstellen")
    st = ps("/api/state")
    alt_cfg = {k: st["cfg"].get(k) for k in KEYS}
    alt_preset = st["cfg"].get("preset_active")
    os.makedirs(KORB, exist_ok=True)
    alt = {c["name"]: c["prompt"] for c in st["decks"]["st"]}
    n = 0
    try:
        for preset, karten in PLAN.items():
            ps("/api/presets", {"action": "load", "name": preset})
            kp = ps("/api/set_preset_laden", {"char": preset, "kost": "Standard"})
            for karte, (quer, text) in karten.items():
                f = os.path.join(E, preset, "Standard", "roh", karte + ".png")
                if os.path.isfile(f):
                    os.makedirs(os.path.join(KORB, preset), exist_ok=True)
                    shutil.move(f, os.path.join(KORB, preset, karte + ".png"))
                s = ps("/api/state")
                tags = s["cfg"]["tags"]
                an = set(kp.get("tags") or [])
                for t in tags:
                    t["on"] = t["name"] in an
                a, b = (1392, 1392) if quer else (1104, 1408)   # quadratisch: Arme und Beine passen beide ins Bild
                mo = dict(s["cfg"].get("mode_opts") or {})
                mo["sprite"] = dict(mo.get("sprite") or {}, aspect="%dx%d" % (a, b), width=a, height=b)
                ganz = s["cfg"]["sprite_prompt"].replace("head to knees", "head to feet").replace("head and knees", "head and feet")   # Beine im Bild
                ps("/api/config", {"sprite_prompt": ganz, "tags": tags, "mode": "sprite", "st_set": preset + "/Standard/roh", "view_pro_karte": False,
                                   "combine_mode": "all", "mode_opts": mo, "aspect": "%dx%d" % (a, b), "width": a, "height": b,
                                   "st_rembg": True, "st_crop": True})
                d = ps("/api/state")["decks"]
                for deck in ("outfit", "setting", "st", "kampf"):
                    for c in d[deck]:
                        c["sel"] = False
                for c in d["outfit"]:
                    c["sel"] = c["name"] in set(kp.get("outfit") or [])
                for c in d["setting"]:
                    c["sel"] = c["name"] in set(kp.get("setting") or [])
                for c in d["st"]:
                    if c["name"] == karte:
                        c["sel"] = True
                        if text:
                            c["prompt"] = text if text.startswith("He stands") else alt[karte] + text
                ps("/api/decks", d)
                n += ps("/api/queue", {"cfg": {}, "decks": d, "max_auftraege": 1}).get("queued", 0)
                print(preset, karte, "quer" if quer else "hoch")
    finally:
        d = ps("/api/state")["decks"]
        for c in d["st"]:
            c["prompt"] = alt.get(c["name"], c["prompt"])
        ps("/api/decks", d)
        if alt_preset:
            ps("/api/presets", {"action": "load", "name": alt_preset})
        ps("/api/config", {k: v for k, v in alt_cfg.items() if v is not None})
    print("eingereiht:", n, "alt in", KORB)


if __name__ == "__main__":
    main()
