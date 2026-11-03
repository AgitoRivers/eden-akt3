# -*- coding: utf-8 -*-
r"""Kloster-Figuren und Tag-Umbau (24.10.2026, Duc: "die Beschreibung so weit es geht in Tags abbilden").

    kloster_figuren.py          Probelauf: zeigt, was angelegt wuerde
    kloster_figuren.py --los    1) neue Tags "Color: Chestnut" und "Skin: Olive Tan"
                                2) Yacht_Laetitia auf Tags umstellen (Subject nur noch Name/Alter/Gesicht/Augen)
                                3) Isabelle (Novizin) als Casting Yacht_Isabelle_A/_B, je 2 Seeds, tag-basiert
                                4) Frederico (Waisenjunge) fest als Yacht_Frederico + Casting _A/_B, je 2 Seeds
                                -> output\expressions\_casting_akt1\<Preset>_<A|B>

Prompt-Geruest wie Yacht_Petru (base/sprite/fashion); bei tag-basierten Figuren ersetzt der Block
Subject/Body/Hair/Skin/Makeup die feste Subject-Zeile. Basis-LoRAs Real3/Lenovo/Redux, Krea2 fp8, CFG 1 -> positiv.
Braucht Prompt Studio (8301) und Krea2 (8189); die Studio-Einstellungen werden danach zurueckgesetzt.
"""
import copy, io, json, re, sys, time, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, r"X:\AI\DucCommon")
import duc_common as dc  # noqa: E402

PS = "http://127.0.0.1:8301"
F_PRESETS = r"X:\AI\PromptStudio\presets.json"
JETZT = time.strftime("%Y-%m-%d %H:%M")
LOS = "--los" in sys.argv
NUR = sys.argv[sys.argv.index("--nur") + 1] if "--nur" in sys.argv else None      # nur eine Casting-Figur
MODELL = {"unet": "krea2_turbo_fp8_scaled.safetensors", "clip": "qwen3vl_4b_fp8_scaled.safetensors"}
LORAS = [{"name": "Krea_Real3.safetensors", "strength": 0.7}, {"name": "Krea_Lenovo.safetensors", "strength": 0.7},
         {"name": "Krea_Redux.safetensors", "strength": 0.5}]
ORDNER = "_casting_akt1"
POSE = "neutral"
SEEDS = (240611, 977031)
HAUT = "natural skin texture with visible pores, slight natural asymmetry in the face, a real individual face"
EXPR = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions"

NEUE_TAGS = [
    {"name": "Color: Chestnut", "prompt": "her hair is warm chestnut brown", "on": False, "cat": "haircolor",
     "grp": "Haare", "sec": "Head"},
    {"name": "Skin: Olive Tan", "prompt": "her skin is sun-kissed olive", "on": False, "cat": "skin", "grp": "Skin",
     "sec": "Body"},
]
TAG_BLOCK = ("Body: {tags_body},\nHair: {tags_haircolor}, {tags_hairstyle}, {tags_hair}\nSkin: {tags_skin},\n"
             "Makeup: {tags_face}\n")

LAETITIA = ("Laetitia Albertini, a 24-year-old Corsican woman from Cala d'Orsu, a long face with high cheekbones, hazel "
            "eyes, a determined mouth")
LAETITIA_TAGS = ["View: Front", "Body: Athletic", "Color: Chestnut", "Style: Side Braid", "Freckles", "Skin: Olive Tan"]

# (Preset, ST-Name, wer, {Fassung: Gesicht}, Tags oder None (fest), Outfit-Karte, Outfit)
CASTING = [
    ("Yacht_Isabelle", "Isabelle", "woman", {
        # Runde 2: Runde 1 wirkte kindlich (Brille + Dutt + kurzes Kleid) -> ausdruecklich erwachsen, gross, lang
        "A": "Isabelle, a grown adult woman of 25, a French novice from Provence living at the monastery of San "
             "Martinu, tall, with a mature friendly face, defined cheekbones, big green eyes behind round wire glasses sliding down her nose, a small upturned nose, a "
             "shy crooked smile",
        "B": "Isabelle, a grown adult woman of 25, a French novice from Provence living at the monastery of San "
             "Martinu, tall, with a mature heart-shaped face, wide-set grey-green eyes behind round wire glasses, rosy cheeks, a dimple in her left "
             "cheek, a curious open expression"},
     ["View: Front", "Body: Slender", "Color: Light Brown", "Style: Bun", "Pale skin", "Freckles"],
     "isabelle_standard", "a plain ankle-length light grey novice's habit with long sleeves, a short white veil over her hair, a "
                          "linen apron with green herb stains, a canvas satchel stuffed with herbs, simple leather sandals"),
    ("Yacht_Frederico", "Frederico", "boy", {
        "A": "Frederico, a 9-year-old Corsican orphan boy, a small round face, big dark brown eyes, dark curly hair, a "
             "gap in his front teeth, sun-tanned skin, a cheeky bright smile",
        "B": "Frederico, a 9-year-old Corsican orphan boy, a narrow face with big ears, long dark eyelashes, short "
             "tousled black hair, a scraped knee, a shy hopeful smile"},
     None,
     "frederico_standard", "an oversized patched beige linen shirt with the sleeves rolled up, brown short trousers "
                           "held up by a rope belt, worn leather sandals, a small carved wooden goat in his hand"),
]
WER = {"woman": "one single woman alone in the frame, her whole body",
       "boy": "one single boy alone in the frame, his whole body",
       "man": "one single man alone in the frame, his whole body"}


def prompts(vorlage, gesicht, wer, mit_tags):
    """base/sprite/fashion aus der Petru-Vorlage: Subject-Zeile ersetzen, Person anpassen."""
    out = {}
    for f in ("base_prompt", "sprite_prompt", "fashion_prompt"):
        block = "Subject: %s, %s,\n%s" % (gesicht, HAUT, TAG_BLOCK if mit_tags else "")
        t = re.sub(r"Subject: [^\n]*\n", lambda m: block, vorlage[f])
        out[f] = t.replace(WER["man"], WER[wer])
    return out


def ps(pfad, daten=None):
    req = urllib.request.Request(PS + pfad, data=None if daten is None else json.dumps(daten).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.loads(r.read())


def eintrag(vorlage, preset, name, wer, gesicht, tags, karte):
    x = copy.deepcopy(vorlage)
    x.update(prompts(vorlage, gesicht, wer, bool(tags)))
    if wer == "woman":
        x["negative_prompt"] = x["negative_prompt"].replace("woman, female, breasts,", "man, male, beard,")
    pfad = "%s\\%s" % (EXPR, preset)
    x.update({"st_set": "%s/Standard/roh" % preset, "sp_char": preset, "sp_stchar": name, "sp_k1": "Standard",
              "sp_k2": "Set2", "sp_kost": ["Standard"], "sv_char": name, "sv_set1": pfad + r"\Standard\Sorted",
              "sv_set2": pfad + r"\Set2\Sorted", "sv_sets": [pfad + r"\Standard\Sorted"],
              "st_src": pfad + r"\Standard\roh", "st_dst": pfad + r"\Standard\Sorted", "loras": LORAS,
              "tags_on": tags or ["View: Front"],
              "cards_on": {"outfit": [karte], "setting": ["A Sprite Background"], "st": [POSE]},
              "created": JETZT, "updated": JETZT})
    return x


def main():
    global CASTING
    if NUR:
        CASTING = [c for c in CASTING if c[0] == NUR]
    print("Neue Tags:", ", ".join(t["name"] for t in NEUE_TAGS))
    print("Yacht_Laetitia -> Tags:", ", ".join(LAETITIA_TAGS))
    for preset, name, wer, fass, tags, karte, _ in CASTING:
        print("%-16s %-10s %s · Fassungen %s · %s" % (preset, name, wer, "/".join(fass),
                                                       "Tags " + ", ".join(tags) if tags else "fest"))
    if not LOS:
        print("Probelauf - nichts geschrieben.")
        return
    st = ps("/api/state")
    alt = {k: st["cfg"].get(k) for k in ("sprite_prompt", "loras", "st_set", "sprite_src", "tags", "unet", "clip", "seed")}
    alt_preset = st["cfg"].get("preset_active")
    tags = st["cfg"]["tags"]
    namen = {t["name"] for t in tags}
    tags += [dict(t) for t in NEUE_TAGS if t["name"] not in namen]
    ps("/api/config", {"tags": tags})
    alt["tags"] = tags                                  # neue Tags bleiben auch nach dem Zuruecksetzen
    fehlen = [t for _, _, _, _, tt, _, _ in CASTING for t in (tt or [])] + LAETITIA_TAGS
    fehlen = sorted({t for t in fehlen if t not in {x["name"] for x in tags}})
    if fehlen:
        sys.exit("Tags fehlen: %s" % fehlen)
    d = st["decks"]
    da = {c["name"]: c for c in d["outfit"]}
    for _, _, _, _, _, karte, outfit in CASTING:
        if karte in da:
            da[karte]["prompt"] = outfit
        else:
            d["outfit"].append({"name": karte, "prompt": outfit, "on": True, "tag": "eden_akt1", "sel": False,
                                "back_prompt": outfit + ", seen from behind"})
    ps("/api/decks", d)
    presets = dc.load_json(F_PRESETS, None, "Studio")
    vorlage = presets["Yacht_Petru"]
    lae = presets["Yacht_Laetitia"]
    lae.update(prompts(vorlage, LAETITIA, "woman", True))
    lae.update({"tags_on": LAETITIA_TAGS, "updated": JETZT})
    for preset, name, wer, fass, tg, karte, _ in CASTING:
        for k, gesicht in fass.items():
            e = eintrag(vorlage, preset, name, wer, gesicht, tg, karte)
            e["st_set"] = "%s/%s_%s" % (ORDNER, preset, k)
            presets["%s_%s" % (preset, k)] = e
        if preset == "Yacht_Frederico" and not presets.get(preset):                 # Duc: Frederico fest anlegen (Fassung A, bis er waehlt)
            presets[preset] = eintrag(vorlage, preset, name, wer, fass["A"], tg, karte)
    dc.save_json(F_PRESETS, presets, "Studio")
    n = 0
    try:
        for preset, name, wer, fass, tg, karte, _ in CASTING:
            for k in fass:
                pn = "%s_%s" % (preset, k)
                ps("/api/presets", {"action": "load", "name": pn})
                cfg = ps("/api/state")["cfg"]
                an = set(tg or ["View: Front"])
                for t in cfg["tags"]:
                    t["on"] = t["name"] in an
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
