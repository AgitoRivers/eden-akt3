# -*- coding: utf-8 -*-
r"""Red Trio Phase 0, Runde 2 (Duc 30.10.2026, Abnahme red_trio_phase0): volle Saetze fuer die freigegebenen Fassungen.

    red_trio_sets.py          Probelauf
    red_trio_sets.py --los    1) Hintergruende + Bar mit schwarzem Schild -> ST\backgrounds\eden_rise_<name>.png
                              2) Yacht_MrWhite (Fassung A, Seed 240611) + 23 NPC-Ausdruecke -> expressions\Yacht_MrWhite\Standard\roh
                              3) Kampf_<Gegner> aus der gewaehlten Fassung, idle von der Abnahme uebernommen, Rest neu
                                 -> expressions\combat\<Gegner>
Danach Abnahme; erst nach Ducs OK module\eden_rise\figuren\MrWhite bzw. Kampf_Bilder.bat.
"""
import os, shutil, subprocess, sys, time

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
LOS = "--los" in sys.argv
sys.argv = [sys.argv[0]]
import casting_red_trio as cr  # noqa: E402

cd, dc, sk = cr.cd, cr.dc, cr.sk
ps = cd.ps
PY = cr.PY
JETZT = time.strftime("%Y-%m-%d %H:%M")
EXPR = sk.EXPR
SEED = 240611           # MrWhite_A2 = neutral.png, Seed 240611
NPC = ['neutral', 'caring', 'joy', 'sadness', 'anger', 'fear_2', 'surprise', 'disgust', 'amusement', 'annoyance',
       'confusion', 'curiosity', 'pride', 'approval', 'gratitude', 'nervousness', 'disapproval', 'disappointment',
       'excitement_2', 'embarrassment_2', 'admiration_2', 'love_2', 'desire_2']      # = NPC_STANDARD in ui.html
HG = {"macchia_three_ways": 3, "charcoal_road": 3, "charcoal_hut": 1, "bone_gorge": 3, "antenna_ridge": 3}
BAR = os.path.join(os.environ["TEMP"], "claude", "C--Users-DucNg", "6e22881a-09d8-467b-b268-1d468b76ce2c", "scratchpad", "bar_schwarz.png")
GEGNER = {"LionPlated": "B", "PlatedMouflon": "C", "ArkHyena": "B", "ShepherdDrone": "B"}


def hintergruende():
    for name, k in HG.items():
        shutil.copy2(os.path.join(cr.ST_BG, "_varianten", "eden_rise_%s_v%d.png" % (name, k)),
                     os.path.join(cr.ST_BG, "eden_rise_%s.png" % name))
    shutil.copy2(BAR, os.path.join(cr.ST_BG, "eden_rise_village_beach_bar.png"))
    print("Hintergruende uebernommen:", len(HG) + 1)


def mr_white(st):
    presets = dc.load_json(sk.F_PRESETS, None, "Studio")
    pfad = os.path.join(EXPR, "Yacht_MrWhite")
    presets["Yacht_MrWhite"] = dict(presets["Yacht_MrWhite_A"], **{
        "st_set": "Yacht_MrWhite/Standard/roh", "sp_char": "Yacht_MrWhite", "sp_stchar": "MrWhite", "sp_k1": "Standard",
        "sp_kost": ["Standard"], "sv_char": "MrWhite", "sv_sets": [pfad + r"\Standard\Sorted"],
        "st_src": pfad + r"\Standard\roh", "st_dst": pfad + r"\Standard\Sorted", "created": JETZT, "updated": JETZT})
    dc.save_json(sk.F_PRESETS, presets, "Studio")
    ps("/api/presets", {"action": "load", "name": "Yacht_MrWhite"})
    cfg = ps("/api/state")["cfg"]
    for t in cfg["tags"]:
        t["on"] = t["name"] == "View: Front"
    ps("/api/config", dict(cd.MODELL, tags=cfg["tags"], mode="sprite", sprite_src="t2i", combine_mode="all",
                           view_pro_karte=False, st_rembg=True, st_crop=True, seed=SEED,
                           st_set="Yacht_MrWhite/Standard/roh", loras=cd.LORAS,
                           sprite_prompt=presets["Yacht_MrWhite"]["sprite_prompt"]))
    dk = ps("/api/state")["decks"]
    for kk in dk:
        wahl = {"outfit": {"mrwhite_A"}, "setting": {"A Sprite Background"}, "st": set(NPC)}.get(kk, set())
        for x in dk[kk]:
            x["sel"] = x["name"] in wahl
    print("Yacht_MrWhite:", ps("/api/queue", {"cfg": {"combine_mode": "all"}, "decks": dk}).get("queued", 0), "Auftraege")


def gegner(st):
    d = ps("/api/state")["decks"]
    da = {c["name"]: c for c in d["outfit"]}
    karten = [c["name"] for c in d["kampf"] if c.get("on", True) and c.get("tag") in ("kern", "kreatur") and c["name"] != "idle"]
    presets, sets = dc.load_json(sk.F_PRESETS, None, "Studio"), dc.load_json(sk.F_SETS, None, "Studio")
    for name, k in GEGNER.items():
        art, subj, look, fmt = cr.GEGNER[name][k]
        karte = "kampf_" + name.lower()
        if karte in da:
            da[karte]["prompt"] = look
        else:
            d["outfit"].append({"name": karte, "prompt": look, "on": True, "tag": "kampf", "sel": False, "back_prompt": ""})
        presets["Kampf_" + name] = sk.preset(name, art, subj, [], fmt)
        sets["Kampf_%s|Kampf" % name] = {"outfit": [karte], "setting": ["A Sprite Background"], "tags": ["View: Kampf"]}
        ziel = os.path.join(EXPR, "combat", name)
        os.makedirs(ziel, exist_ok=True)
        shutil.copy2(os.path.join(EXPR, "combat", "%s_%s" % (name, k), "idle.png"), os.path.join(ziel, "idle.png"))
    ps("/api/decks", d)
    dc.save_json(sk.F_PRESETS, presets, "Studio")
    dc.save_json(sk.F_SETS, sets, "Studio")
    subprocess.run([PY, os.path.join(HIER, "kampf_test.py"), "--karten", ",".join(karten), "--gegner", ",".join(GEGNER)], check=True)


def main():
    print("Hintergruende:", ", ".join(HG), "+ Bar · Mr. White 23 · Gegner:", GEGNER)
    if not LOS:
        print("Probelauf - nichts geschrieben.")
        return
    hintergruende()
    st = ps("/api/state")
    alt_preset = st["cfg"].get("preset_active")
    alt = {k: st["cfg"].get(k) for k in ("sprite_prompt", "loras", "st_set", "sprite_src", "tags", "unet", "clip", "seed", "decks_visible")}
    try:
        mr_white(st)
        gegner(st)
    finally:
        if alt_preset:
            ps("/api/presets", {"action": "load", "name": alt_preset})
        ps("/api/config", {k: v for k, v in alt.items() if v is not None})


if __name__ == "__main__":
    main()
