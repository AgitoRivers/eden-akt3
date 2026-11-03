# -*- coding: utf-8 -*-
r"""Danzel volles Sprite-Set (Duc 29.10.2026, Abnahme Red Trio: Danzel B2 = Fassung B, Seed 977031).

    danzel_sprites.py          Probelauf
    danzel_sprites.py --los    1) Preset Yacht_Danzel (fest, aus Yacht_Danzel_B) + 23 NPC-Ausdruecke (wie der
                                  Prompt-Studio-Knopf, nur Front, gleicher Seed wie die Abnahme)
                                  -> output\expressions\Yacht_Danzel\Standard\roh
                               2) Preset Kampf_Danzel + Kostuem Kampf_Danzel|Kampf (Karte kampf_danzel), alle
                                  Kernkarten des Decks kampf ueber kampf_test.py -> output\expressions\combat\Danzel
Danach Abnahme-Seite; erst nach Ducs OK nach module\eden_rise\figuren\Danzel bzw. Kampf_Bilder.bat --gegner Danzel.
Prompt Studio wird danach auf das vorher aktive Preset zurueckgesetzt.
"""
import io, json, os, subprocess, sys, time, urllib.request

_HALTEN = []                     # beide Module wickeln stdout neu ein - alte Wrapper festhalten, sonst schliesst GC den Puffer
HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, r"X:\AI\DucCommon")
LOS = "--los" in sys.argv
sys.argv = [sys.argv[0]]
import duc_common as dc  # noqa: E402
_HALTEN.append(sys.stdout)
import castings_danzel as cd  # noqa: E402
_HALTEN.append(sys.stdout)
import studio_kampf_gegner as sk  # noqa: E402

PS = "http://127.0.0.1:8301"
PY = r"X:\AI\ComfyUI_krea2\python_embeded\python.exe"
JETZT = time.strftime("%Y-%m-%d %H:%M")
SEED = 977031
EXPR = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions"
NPC = ['neutral', 'caring', 'joy', 'sadness', 'anger', 'fear_2', 'surprise', 'disgust', 'amusement', 'annoyance',
       'confusion', 'curiosity', 'pride', 'approval', 'gratitude', 'nervousness', 'disapproval', 'disappointment',
       'excitement_2', 'embarrassment_2', 'admiration_2', 'love_2', 'desire_2']      # = NPC_STANDARD in ui.html
GESICHT, OUTFIT = cd.FIGUREN[0][3]["B"]
# Kampf: gleiche Figur, Waffe = Teleskopschlagstock, den er haelt, als haette er ihn nie benutzt
KAMPF_OUTFIT = (OUTFIT + ", a black telescopic baton held in his right hand a little too tightly, his left hand "
                "empty")


def ps(pfad, daten=None):
    req = urllib.request.Request(PS + pfad, data=None if daten is None else json.dumps(daten).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.loads(r.read())


def main():
    st = ps("/api/state")
    kern = [c["name"] for c in st["decks"]["kampf"] if c.get("on", True) and c.get("tag") == "kern"]
    print("Yacht_Danzel: %d NPC-Ausdruecke, Seed %d, Outfit danzel_B" % (len(NPC), SEED))
    print("Kampf_Danzel: %d Kernkarten (%s)" % (len(kern), ", ".join(kern)))
    fehlt = [k for k in NPC if k not in {c["name"] for c in st["decks"]["st"]}]
    if fehlt:
        sys.exit("ST-Karten fehlen: %s" % fehlt)
    if not LOS:
        print("Probelauf - nichts geschrieben.")
        return
    alt_preset = st["cfg"].get("preset_active")
    alt = {k: st["cfg"].get(k) for k in ("sprite_prompt", "loras", "st_set", "sprite_src", "tags", "unet", "clip",
                                         "seed", "decks_visible")}
    presets = dc.load_json(sk.F_PRESETS, None, "Studio")
    sets = dc.load_json(sk.F_SETS, None, "Studio")
    pfad = os.path.join(EXPR, "Yacht_Danzel")
    presets["Yacht_Danzel"] = dict(presets["Yacht_Danzel_B"], **{
        "st_set": "Yacht_Danzel/Standard/roh", "sp_char": "Yacht_Danzel", "sp_stchar": "Danzel", "sp_k1": "Standard",
        "sp_kost": ["Standard"], "sv_char": "Danzel", "sv_sets": [pfad + r"\Standard\Sorted"],
        "st_src": pfad + r"\Standard\roh", "st_dst": pfad + r"\Standard\Sorted", "created": JETZT, "updated": JETZT})
    presets["Kampf_Danzel"] = sk.preset("Danzel", "mann", GESICHT, [], "hoch")
    sets["Kampf_Danzel|Kampf"] = {"outfit": ["kampf_danzel"], "setting": ["A Sprite Background"], "tags": ["View: Kampf"]}
    d = st["decks"]
    out = {c["name"]: c for c in d["outfit"]}
    if "kampf_danzel" in out:
        out["kampf_danzel"]["prompt"] = KAMPF_OUTFIT
    else:
        d["outfit"].append({"name": "kampf_danzel", "prompt": KAMPF_OUTFIT, "on": True, "tag": "kampf", "sel": False,
                            "back_prompt": ""})
    ps("/api/decks", d)
    dc.save_json(sk.F_PRESETS, presets, "Studio")
    dc.save_json(sk.F_SETS, sets, "Studio")
    n = 0
    try:
        ps("/api/presets", {"action": "load", "name": "Yacht_Danzel"})
        cfg = ps("/api/state")["cfg"]
        for t in cfg["tags"]:
            t["on"] = t["name"] == "View: Front"
        ps("/api/config", dict(cd.MODELL, tags=cfg["tags"], mode="sprite", sprite_src="t2i", combine_mode="all",
                               view_pro_karte=False, st_rembg=True, st_crop=True, seed=SEED,
                               st_set="Yacht_Danzel/Standard/roh", loras=cd.LORAS,
                               sprite_prompt=presets["Yacht_Danzel"]["sprite_prompt"]))
        dk = ps("/api/state")["decks"]
        for kk in dk:
            wahl = {"outfit": {"danzel_B"}, "setting": {"A Sprite Background"}, "st": set(NPC)}.get(kk, set())
            for x in dk[kk]:
                x["sel"] = x["name"] in wahl
        n = ps("/api/queue", {"cfg": {"combine_mode": "all"}, "decks": dk}).get("queued", 0)
        print("Yacht_Danzel: %d Auftraege -> expressions\\Yacht_Danzel\\Standard\\roh" % n)
        subprocess.run([PY, os.path.join(HIER, "kampf_test.py"), "--karten", ",".join(kern), "--gegner", "Danzel"],
                       check=True)
    finally:
        if alt_preset:
            ps("/api/presets", {"action": "load", "name": alt_preset})
        ps("/api/config", {k: v for k, v in alt.items() if v is not None})


if __name__ == "__main__":
    main()
