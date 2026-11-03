# -*- coding: utf-8 -*-
r"""Bibis Sprites neu mit dem 😇-SFW-Satz (Duc 30.10.2026: "starte ihre NPC Poses neu aber mit Engel SFW Poses"). Die Karte
bibi_A bekommt denselben Stand wie der Kampf: schwarze Dosen und ein ganz schwarzer Loewe statt Keiler. Alte Bilder wandern
nach output\_expressions_papierkorb\Yacht_Bibi_<Zeit>.

    bibi_sfw_neu.py          Probelauf
    bibi_sfw_neu.py --los    Karte speichern, alte Bilder verschieben, Auftraege einreihen
    bibi_sfw_neu.py --los --karten a,b   nur diese Posen, mit mehr Rand (Abnahme: "abgeschnitten")
"""
import glob, io, json, os, shutil, sys, time, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
PS = "http://127.0.0.1:8301"
PRESET, KOST, KARTE = "Yacht_Bibi", "Standard", "bibi_A"
ST_SET = "Yacht_Bibi/Standard/roh"
ROH = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions\Yacht_Bibi\Standard\roh"
KORB = r"X:\AI\ComfyUI_krea2\ComfyUI\output\_expressions_papierkorb\Yacht_Bibi_" + time.strftime("%Y%m%d_%H%M")
ERSATZ = [("several round black grenades", "several small cylindrical canister grenades painted entirely jet black, the size "
           "of soda cans, each with a jet black lever and pull ring on top"),
          ("a small plush boar keychain on her belt", "a small plush lion keychain that is entirely jet black, black face, black "
           "paws, black mane, hanging from her belt on her right hip, on the left side of the image")]


NUR = sys.argv[sys.argv.index("--karten") + 1].split(",") if "--karten" in sys.argv else None
EINER = "one single woman alone in the frame,"
RAND = ("one single woman alone in the frame, the camera further back, her whole figure with both hands, elbows and hair fully "
        "inside the image, wide empty space on all sides,")


def ps(pfad, daten=None):
    req = urllib.request.Request(PS + pfad, data=None if daten is None else json.dumps(daten).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def main():
    st = ps("/api/state")
    alt_preset, vis = st["cfg"].get("preset_active"), st["cfg"].get("decks_visible") or {}
    ps("/api/presets", {"action": "load", "name": PRESET})
    kp = ps("/api/set_preset_laden", {"char": PRESET, "kost": KOST})
    st = ps("/api/state")
    posen = set(st["cfg"].get("sfw_posen") or [])
    d = st["decks"]
    an = [c["name"] for c in d["st"] if c.get("on", True) and c["name"] in posen]
    print("%d SFW-Posen, Set: %s, Tags: %s" % (len(an), ST_SET, ", ".join(kp.get("tags") or [])))
    k = next(c for c in d["outfit"] if c["name"] == KARTE)
    for alt, neu in ERSATZ:
        k["prompt"] = k["prompt"].replace(alt, neu)
    print(k["prompt"])
    if NUR:
        an = [c for c in an if c in NUR]
        assert len(an) == len(NUR), an
    alte = [os.path.join(ROH, c + ".png") for c in an] if NUR else glob.glob(os.path.join(ROH, "*.png"))
    alte = [f for f in alte if os.path.isfile(f)]
    print("%d alte Bilder" % len(alte))
    if "--los" not in sys.argv:
        if alt_preset:
            ps("/api/presets", {"action": "load", "name": alt_preset})
        sys.exit("PROBELAUF - mit --los einstellen")
    os.makedirs(KORB, exist_ok=True)
    for f in alte:
        shutil.move(f, KORB)
    print("alte Bilder ->", KORB)
    try:
        tags = st["cfg"]["tags"]
        sets = set(kp.get("tags") or [])
        for t in tags:
            t["on"] = t["name"] in sets
        for deck in ("outfit", "setting", "st", "kampf"):
            for c in d[deck]:
                c["sel"] = False
        k["sel"] = True
        for c in d["setting"]:
            c["sel"] = c["name"] in set(kp.get("setting") or [])
        for c in d["st"]:
            c["sel"] = c["name"] in an
        extra = {}
        if NUR:
            assert EINER in st["cfg"]["sprite_prompt"]
            extra["sprite_prompt"] = st["cfg"]["sprite_prompt"].replace(EINER, RAND)
        ps("/api/config", {**extra, "tags": tags, "mode": "sprite", "st_set": ST_SET, "view_pro_karte": True, "combine_mode": "all",
                           "st_rembg": True, "st_crop": True, "decks_visible": dict(vis, kampf=False)})
        ps("/api/decks", d)
        n = ps("/api/queue", {"cfg": {}, "decks": d, "max_auftraege": len(an)}).get("queued", 0)
        print("eingereiht:", n)
    finally:
        ps("/api/config", {"view_pro_karte": False})
        if alt_preset:
            ps("/api/presets", {"action": "load", "name": alt_preset})


if __name__ == "__main__":
    main()
