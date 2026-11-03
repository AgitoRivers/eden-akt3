# -*- coding: utf-8 -*-
r"""Casting fuer die Akt-1-Ortskapitel (Nacht 24.10.2026): Nonna Fiora (Kloster San Martinu), Laetitia Albertini
(Petrus Tochter) und Caporal Adrien Morel (Fremdenlegion) - docs\wiki\welt\orte.md / docs/wiki/welt/orte_drehbuch.md.

    castings_akt1.py --los --nur Yacht_Nonna   nur eine Figur neu
    castings_akt1.py          Probelauf: zeigt, was angelegt wuerde, schreibt nichts
    castings_akt1.py --los    legt Outfit-Karten + Casting-Presets Yacht_Nonna_A/_B, Yacht_Laetitia_A/_B, Yacht_Adrien_A/_B an und stellt
                              je Figur 4 Portraits in die Warteschlange (2 Gesichtsfassungen x 2 Seeds)
                              -> output\expressions\_casting_akt1\<Preset>_<A|B>

Wie castings.py (Runde 2 ff.): Basis Real3 0.7 + Lenovo 0.7 + Redux 0.5, Krea2 fp8, t2i, Sprite-Modus, keine
Identitaets-LoRA (Dorf-NPCs wie Petru). Gesichter individuell beschrieben (Name, Alter, Herkunft, Gesichtsform, ein
Erkennungsmerkmal), keine Pauschal-Schoenheitswoerter. Krea2 laeuft mit CFG 1: nur positiv formulieren.
Danach: Abnahme-Seite (docs\abnahme\casting_akt1.json), Duc waehlt je Figur eine Fassung; erst dann Sprites.
Braucht Prompt Studio (8301) und ComfyUI Krea2 (8189). Die Studio-Einstellungen werden danach zurueckgesetzt.
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
ORDNER = "_casting_akt1"
POSE = "neutral"
SEEDS = (240611, 977031)
HAUT = "natural skin texture with visible pores, slight natural asymmetry in the face, a real individual face"

# (Preset, ST-Name, Mann?, {Fassung: Gesicht}, Outfit-Karte, Outfit)
FIGUREN = [
    # Runde 2 (Duc 24.10. morgens): A/B zu stereotyp und zu alt -> "etwas juenger und schoener, eine schoen gealterte
    # Frau, weniger Nonna-Klischee". Kochloeffel bleibt (ihr Erkennungszeichen), Kopftuch und Schwarz fallen weg.
    ("Yacht_Nonna", "Nonna Fiora", False, {
        "C": "Nonna Fiora, a Corsican woman of 62 from the mountain village above Cala d'Orsu, beautifully aged, a "
             "fine oval face with high cheekbones, warm olive skin with soft fine lines around her eyes, dark lively "
             "eyes with a mischievous glint, elegant dark eyebrows, a generous smile, thick silver hair worn long and "
             "loosely pinned up with a few strands falling free, a graceful upright posture",
        "D": "Nonna Fiora, a Corsican woman of 60 from the mountain village above Cala d'Orsu, a striking face with a "
             "strong straight nose and full lips, sun-kissed skin with laugh lines, deep brown eyes, salt-and-pepper "
             "hair in a long thick braid over one shoulder, small gold hoop earrings, a confident amused expression, "
             "slim and strong"},
     "nonna_standard", "a rust-coloured linen blouse with the sleeves rolled up, a long dark green cotton skirt, a "
                       "natural linen apron tied at the waist, a long wooden cooking spoon in her right hand, simple "
                       "leather sandals"),
    ("Yacht_Laetitia", "Laetitia Albertini", False, {
        "A": "Laetitia Albertini, a 24-year-old Corsican woman from Cala d'Orsu, an oval sun-tanned face, straight dark "
             "eyebrows, warm dark brown eyes, a slightly crooked nose, full lips, a small pale scar on her chin, thick "
             "dark curly hair tied back loosely, slim and athletic",
        "B": "Laetitia Albertini, a 24-year-old Corsican woman from Cala d'Orsu, a long face with high cheekbones, "
             "freckles across her nose, hazel eyes, a determined mouth, wavy chestnut hair in one thick braid over her "
             "shoulder, slim and athletic"},
     "laetitia_standard", "a faded red bandana tied around her neck, a loose white linen shirt with rolled sleeves, "
                          "olive hiking trousers, worn brown leather hiking boots, a small canvas backpack"),
    ("Yacht_Adrien", "Adrien Morel", True, {
        "A": "Caporal Adrien Morel, a 31-year-old French Foreign Legion soldier from Lyon, a lean angular face, a buzz "
             "cut, three days of dark stubble, tired grey-green eyes, a once broken nose, a thin scar through his left "
             "eyebrow, tall and lean",
        "B": "Caporal Adrien Morel, a 31-year-old French Foreign Legion soldier from Lyon, a square jaw, close-cropped "
             "fair hair, sunburnt skin, pale blue eyes, a strong chin with a cleft, broad shoulders"},
     "adrien_standard", "a dusty camouflage combat uniform of the French Foreign Legion with the sleeves rolled up, a "
                        "green beret tucked under his shoulder strap, a white bandage around his left thigh over the "
                        "trousers, worn black combat boots"),
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
            d["outfit"].append({"name": karte, "prompt": outfit, "on": True, "tag": "eden_akt1", "sel": False,
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
