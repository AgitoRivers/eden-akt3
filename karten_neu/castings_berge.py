# -*- coding: utf-8 -*-
r"""Casting fuer das Ortskapitel Berge (Story-Auftrag 27.10.2026): Sergent Kaspar Wolff (Fremdenlegion), Ghjuvan
Santucci (Hirte) und Dumenica (Mazzera). Gleiches Verfahren wie castings_akt1.py.

    castings_berge.py          Probelauf
    castings_berge.py --los    Outfit-Karten + Casting-Presets Yacht_<Name>_A/_B, je Figur 4 Portraits
                               -> output\expressions\_casting_berge\<Preset>_<A|B>
Danach Abnahme-Seite, Duc waehlt je Figur eine Fassung; erst dann Sprites.
Runde 2 Ghjuvan (Duc 27.10.): zerzaustes Haar -> --nur Yacht_Ghjuvan.
"""
import io, json, sys, time, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, r"X:\AI\DucCommon")
import duc_common as dc  # noqa: E402

PS = "http://127.0.0.1:8301"
F_PRESETS = r"X:\AI\PromptStudio\presets.json"
JETZT = time.strftime("%Y-%m-%d %H:%M")
LOS = "--los" in sys.argv
NUR = sys.argv[sys.argv.index("--nur") + 1] if "--nur" in sys.argv else None      # z. B. --nur Yacht_Nonna
MODELL = {"unet": "krea2_turbo_fp8_scaled.safetensors", "clip": "qwen3vl_4b_fp8_scaled.safetensors"}
LORAS = [{"name": "Krea_Real3.safetensors", "strength": 0.7}, {"name": "Krea_Lenovo.safetensors", "strength": 0.7},
         {"name": "Krea_Redux.safetensors", "strength": 0.5}]
ORDNER = "_casting_berge"
POSE = "neutral"
SEEDS = (240611, 977031)
HAUT = "natural skin texture with visible pores, slight natural asymmetry in the face, a real individual face"

# (Preset, ST-Name, Mann?, {Fassung: Gesicht}, Outfit-Karte, Outfit)
FIGUREN = [
    ("Yacht_Wolff", "Kaspar Wolff", True, {
        "A": "Sergent Kaspar Wolff, a 48-year-old German soldier of the French Foreign Legion, an angular weathered "
             "face with deep lines, short shaved grey hair, a thick grey moustache, narrow steel-grey eyes, a strong jaw, "
             "broad and wiry",
        "B": "Sergent Kaspar Wolff, a 47-year-old German soldier of the French Foreign Legion from Hamburg, a long hard "
             "face burnt brown by the sun, a grey buzz cut, a neatly trimmed grey moustache, pale blue eyes under heavy "
             "brows, a deep crease between the brows, lean and upright"},
     "wolff_standard", "a green camouflage combat uniform of the French Foreign Legion, sleeves neatly rolled, a green "
                       "beret pulled low on his forehead, a black radio clipped to his chest, a webbing belt, black "
                       "combat boots"),
    ("Yacht_Ghjuvan", "Ghjuvan Santucci", True, {
        "A": "Ghjuvan Santucci, a 58-year-old Corsican shepherd from the high mountains, a sun-beaten deeply lined "
             "face, wild tousled grey hair sticking out in all directions, grey stubble beard, tired dark eyes with heavy lids, a big hooked nose, thick grey eyebrows, "
             "rough hands, slightly stooped",
        "B": "Ghjuvan Santucci, a 57-year-old Corsican shepherd, a broad leathery face, short grey stubble, sad "
             "brown eyes, a heavy brow, sunken cheeks, thick unkempt tousled grey hair windblown and messy, wiry and worn out"},
     "ghjuvan_standard", "worn brown corduroy trousers, a dark wool waistcoat over a faded checked flannel shirt, an old "
                         "shepherd's crook in his right hand, an old double-barrelled shotgun slung over his shoulder, "
                         "dusty leather boots"),
    ("Yacht_Dumenica", "Dumenica", False, {
        "A": "Dumenica, a Corsican woman of 78 from a mountain village, a mazzera, a narrow face with skin like thin "
             "parchment, deep lines, very alert pale grey eyes, a sharp nose, thin lips, a small calm knowing smile",
        "B": "Dumenica, an old Corsican woman of 77, a small round wrinkled face, sun-darkened skin like old paper, "
             "strikingly bright light-blue eyes wide awake, white eyebrows, a firm chin, small and upright"},
     "dumenica_standard", "a long plain black dress, a black headscarf tied under her chin, a wooden rosary wound "
                          "around her gnarled hands, worn black shoes"),
]


def sprite_prompt(gesicht, mann):
    wer = "one single man alone in the frame, his whole body" if mann else "one single woman alone in the frame, her whole body"
    return ("{tags_action}, Shot on an iPhone, grainy amateur photo, realistic smartphone photography, full body shot "
            "from head to knees, direct gaze, %s in full view, head and knees inside the frame,\nSubject: %s, %s,\n"
            "Wearing: {outfit},\nScene: {setting}, {st},\n{expression},\nLook: {look},\n{tags_photo}" % (wer, gesicht, HAUT))


def ps(pfad, daten=None):
    req = urllib.request.Request(PS + pfad, data=None if daten is None else json.dumps(daten).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.loads(r.read())


def main():
    global FIGUREN
    if NUR:
        FIGUREN = [f for f in FIGUREN if f[0] == NUR]
    for preset, name, mann, fassungen, karte, outfit in FIGUREN:
        print("%-15s %-19s %s · Fassungen %s · Outfit %s" % (preset, name, "Mann" if mann else "Frau", "/".join(fassungen), karte))
    if not LOS:
        print("Probelauf - nichts geschrieben. Mit --los anlegen und in die Warteschlange stellen.")
        return
    st = ps("/api/state")
    d = st["decks"]
    da = {c["name"]: c for c in d["outfit"]}
    for _, _, _, _, karte, outfit in FIGUREN:
        if karte in da:
            da[karte]["prompt"] = outfit
        else:
            d["outfit"].append({"name": karte, "prompt": outfit, "on": True, "tag": "eden_berge", "sel": False,
                                "back_prompt": outfit + ", seen from behind"})
    ps("/api/decks", d)
    presets = dc.load_json(F_PRESETS, None, "Studio")
    for preset, name, mann, fassungen, karte, _ in FIGUREN:
        for k, gesicht in fassungen.items():
            presets["%s_%s" % (preset, k)] = {
                "sprite_prompt": sprite_prompt(gesicht, mann), "loras": LORAS, "ref_image": "", "ref_image_b": "",
                "negative_prompt": "", "tags_on": ["View: Front"], "sp_stchar": name,
                "cards_on": {"outfit": [karte], "setting": ["A Sprite Background"], "st": [POSE]},
                "st_set": "%s/%s_%s" % (ORDNER, preset, k), "created": JETZT, "updated": JETZT}
    dc.save_json(F_PRESETS, presets, "Studio")
    alt = {k: st["cfg"].get(k) for k in ("sprite_prompt", "loras", "st_set", "sprite_src", "tags", "unet", "clip", "seed")}
    alt_preset = st["cfg"].get("preset_active")
    n = 0
    try:
        for preset, name, mann, fassungen, karte, _ in FIGUREN:
            for k in fassungen:
                pn = "%s_%s" % (preset, k)
                ps("/api/presets", {"action": "load", "name": pn})
                cfg = ps("/api/state")["cfg"]
                for t in cfg["tags"]:
                    t["on"] = t["name"] == "View: Front"
                for s in SEEDS:
                    ps("/api/config", dict(MODELL, tags=cfg["tags"], mode="sprite", sprite_src="t2i", combine_mode="all",
                                           view_pro_karte=False, st_rembg=True, st_crop=True, seed=s,
                                           st_set="%s/%s" % (ORDNER, pn), loras=LORAS,
                                           sprite_prompt=presets[pn]["sprite_prompt"]))
                    dk = ps("/api/state")["decks"]
                    for kk in dk:
                        wahl = {"outfit": {karte}, "setting": {"A Sprite Background"}, "st": {POSE}}.get(kk, set())
                        for x in dk[kk]:
                            x["sel"] = x["name"] in wahl
                    n += ps("/api/queue", {"cfg": {"combine_mode": "all"}, "decks": dk}).get("queued", 0)
    finally:
        if alt_preset:
            ps("/api/presets", {"action": "load", "name": alt_preset})
        ps("/api/config", {k: v for k, v in alt.items() if v is not None})
    print("%d Portraits in der Warteschlange -> expressions\\%s" % (n, ORDNER))


if __name__ == "__main__":
    main()
