# -*- coding: utf-8 -*-
r"""Casting fuer das Ortskapitel Grotte (Story-Auftrag 27.10.2026): Gennaro Esposito (Totos Cousin), Matteu Pinelli
(Fischersohn), Chloe Marchal (Schatzsucherin) und U Riscossore (Geldeintreiber). Gleiches Verfahren wie castings_berge.py.
Runde 2 U Riscossore (Duc 28.10.): als Schwarzer Mann neu gecastet, Orange bleibt.

    castings_grotte.py          Probelauf
    castings_grotte.py --los    Outfit-Karten + Casting-Presets Yacht_<Name>_A/_B, je Figur 4 Portraits
                                -> output\expressions\_casting_grotte\<Preset>_<A|B>
Danach Abnahme-Seite, Duc waehlt je Figur eine Fassung; erst dann Sprites.
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
ORDNER = "_casting_grotte"
POSE = "neutral"
SEEDS = (240611, 977031)
HAUT = "natural skin texture with visible pores, slight natural asymmetry in the face, a real individual face"

# (Preset, ST-Name, Mann?, {Fassung: Gesicht}, Outfit-Karte, Outfit)
FIGUREN = [
    ("Yacht_Gennaro", "Gennaro Esposito", True, {
        "A": "Gennaro Esposito, a 42-year-old Italian man from Bastia, a round charming face, a big bushy black "
             "moustache, one gold front tooth flashing in a nervous grin, a dark purple bruise around his left eye, "
             "a split lower lip, curly black hair going grey at the temples, restless dark eyes",
        "B": "Gennaro Esposito, a 41-year-old Italian man from Bastia, a fleshy friendly face with a huge black "
             "handlebar moustache, a gold tooth in an anxious smile, a swollen black eye, a cut on his lower lip, "
             "slicked-back black hair, sweat on his brow, eyebrows raised in a hopeful plea"},
     "gennaro_standard", "a crumpled short-sleeved white shirt open at the collar and stained with dust, a thin gold "
                         "chain, wrinkled navy chinos, scuffed brown loafers"),
    ("Yacht_Matteu", "Matteu Pinelli", True, {
        "A": "Matteu Pinelli, a 19-year-old Corsican fisherman's son, a thin young face, wet tousled black hair, "
             "dark serious eyes, a stubborn set jaw, sun-browned skin, a lean swimmer's build",
        "B": "Matteu Pinelli, a 19-year-old Corsican young man, a narrow shy face, short damp dark curls, big dark "
             "eyes looking up from under his brows, a few freckles on his nose, tight lips, lean and wiry"},
     "matteu_standard", "a black diving wetsuit torn open at one knee and the elbow, a diving mask pushed up on his "
                        "forehead, barefoot, a small diving knife strapped to his calf"),
    ("Yacht_Chloe", "Chloe Marchal", False, {
        "A": "Chloe Marchal, a 30-year-old French woman from Marseille, a lively heart-shaped face smudged with dirt, "
             "quick bright hazel eyes, dark brown hair in a messy ponytail, a determined mouth, athletic",
        "B": "Chloe Marchal, a 30-year-old French woman from Marseille, an angular clever face with dust on her "
             "cheeks, sharp green eyes, short dark curly hair, thick eyebrows, a tense half smile, slim and strong"},
     "chloe_standard", "dirty khaki expedition trousers with many pockets, a mud-stained olive field shirt with "
                       "rolled sleeves, a headlamp strapped around her forehead, worn hiking boots, scraped red "
                       "fingertips with dried blood on her hands"),
    ("Yacht_Riscossore", "U Riscossore", True, {
        "A": "U Riscossore, a 64-year-old Black Corsican debt collector of West African descent, dark brown skin, "
             "a long calm face with deep lines, heavy-lidded patient dark eyes, short neatly trimmed grey hair, a "
             "thin grey moustache, a faint polite smile",
        "B": "U Riscossore, a 66-year-old Black man living in Corsica, very dark skin, a gaunt still face, high "
             "cheekbones, cold steady dark eyes that do not blink, white hair cut very short, a short white beard, "
             "thin lips, unhurried and quiet"},
     "riscossore_standard", "an old cream linen suit with jacket cuffs gone yellow, a pale blue shirt buttoned to the "
                            "top without a tie, polished brown leather shoes, peeling an orange with a small folding "
                            "knife in his hands"),
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
            d["outfit"].append({"name": karte, "prompt": outfit, "on": True, "tag": "eden_grotte", "sel": False,
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
