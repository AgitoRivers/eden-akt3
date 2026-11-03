# -*- coding: utf-8 -*-
r"""Bar-Sets fuer "Mochi's" (Duc 30.10.2026): Kostuem "Bikini" von Charly und Bibi mit dem SFW-Posensatz.

    bar_sets.py Yacht_Charly                                  Probelauf
    bar_sets.py Yacht_Charly --los                            alle SFW-Posen nach <Figur>\Bikini\roh
    bar_sets.py Yacht_Bibi --los --test t1 --karten a,b,c     nur diese Posen nach <Figur>\Bikini_t1\roh
        --text "..."          eigener Kartentext (neue Karte sling_<test>, die gemeinsame Karte sling_red bleibt)
        --weg Huge            Tag aus dem Set nehmen
        --dazu Busty          Tag dazunehmen
    bar_sets.py Yacht_Bibi --los --nach a,b [--rand]          diese Posen im fertigen Set neu, alte Bilder in den Papierkorb
        --rand                Kamera weiter weg (abgeschnittene Haende)
        --back "..."          Rueckansicht der Karte neu schreiben
        --quer                Querformat 1552 x 1024 (Arme zur Seite passen ins Bild, der Freisteller schneidet den Rest weg)
"""
import glob, io, json, os, shutil, sys, time, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
PS = "http://127.0.0.1:8301"
KOST = "Bikini"
EXPR = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions"
KORB = r"X:\AI\ComfyUI_krea2\ComfyUI\output\_expressions_papierkorb"
EINER = "one single woman alone in the frame,"
RAND = ("one single woman alone in the frame, the camera far back, she fills only the middle of the image, her whole figure with both legs, both hands, elbows and hair fully "
        "inside the image, both hands well away from the edges, wide empty space on all sides,")


def arg(name, vor=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else vor


def ps(pfad, daten=None):
    req = urllib.request.Request(PS + pfad, data=None if daten is None else json.dumps(daten).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def main():
    preset = sys.argv[1]
    test, nur, text = arg("--test"), arg("--karten") or arg("--nach"), arg("--text")
    st_set = "%s/%s/roh" % (preset, KOST + ("_" + test if test else ""))
    st = ps("/api/state")
    alt_preset, vis = st["cfg"].get("preset_active"), st["cfg"].get("decks_visible") or {}
    ps("/api/presets", {"action": "load", "name": preset})
    kp = ps("/api/set_preset_laden", {"char": preset, "kost": KOST})
    st = ps("/api/state")
    d = st["decks"]
    posen = set(st["cfg"].get("sfw_posen") or [])
    an = [c["name"] for c in d["st"] if c.get("on", True) and c["name"] in posen]
    if nur:
        an = [c for c in an if c in nur.split(",")]
        assert len(an) == len(nur.split(",")), an
    karte = (kp.get("outfit") or ["sling_red"])[0]
    k = next(c for c in d["outfit"] if c["name"] == karte)
    if text:
        karte = "sling_" + test
        neu = next((c for c in d["outfit"] if c["name"] == karte), None)
        if not neu:
            neu = dict(k, name=karte)
            d["outfit"].append(neu)
        neu["prompt"] = text
        k = neu
    if arg("--back"):
        k["back_prompt"] = arg("--back")
    sets = (set(kp.get("tags") or []) - {arg("--weg")}) | ({arg("--dazu")} if arg("--dazu") else set())
    print("%d Posen -> %s\nKarte %s: %s\nTags: %s" % (len(an), st_set, karte, k["prompt"], ", ".join(sorted(sets))))
    if "--los" not in sys.argv:
        if alt_preset:
            ps("/api/presets", {"action": "load", "name": alt_preset})
        sys.exit("PROBELAUF - mit --los einstellen")
    if arg("--nach"):
        ziel = os.path.join(KORB, "%s_Bikini_%s" % (preset, time.strftime("%Y%m%d_%H%M%S")))
        os.makedirs(ziel, exist_ok=True)
        for c in an:
            for f in glob.glob(os.path.join(EXPR, preset, KOST, "roh", c + ".png")):
                shutil.move(f, ziel)
    try:
        tags = st["cfg"]["tags"]
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
        if "--rand" in sys.argv:
            assert EINER in st["cfg"]["sprite_prompt"]
            extra["sprite_prompt"] = st["cfg"]["sprite_prompt"].replace(EINER, RAND)
        if "--quer" in sys.argv:
            extra.update(width=1552, height=1024, aspect="1552x1024", fire_aspect="1552x1024",
                         mode_aspect_auto=dict(st["cfg"].get("mode_aspect_auto") or {}, sprite="1552x1024"))
        ps("/api/config", {**extra, "tags": tags, "mode": "sprite", "st_set": st_set, "view_pro_karte": True, "combine_mode": "all",
                           "st_rembg": True, "st_crop": True, "decks_visible": dict(vis, kampf=False)})
        ps("/api/decks", d)
        print("eingereiht:", ps("/api/queue", {"cfg": {}, "decks": d, "max_auftraege": len(an)}).get("queued", 0))
    finally:
        ps("/api/config", {"view_pro_karte": False, **({"width": 880, "height": 1328, "aspect": "880x1328", "fire_aspect": "880x1328",
                                                       "mode_aspect_auto": dict(st["cfg"].get("mode_aspect_auto") or {}, sprite="880x1328")}
                                                       if "--quer" in sys.argv else {})})
        if alt_preset:
            ps("/api/presets", {"action": "load", "name": alt_preset})


if __name__ == "__main__":
    main()
