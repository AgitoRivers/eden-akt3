# -*- coding: utf-8 -*-
r"""Casting fuer die Macchia-Nebenquest "Red Trio" (Duc 29.10.2026): Danzel (der Agent aus der Felsnische) und seine
zwei Freundinnen Bibi und Charly in roten Agentenanzuegen. Gleiches Verfahren wie castings_grotte.py, aber drei
Fassungen (A/B/C) je Figur und je Fassung ein eigenes Outfit.

    castings_danzel.py          Probelauf
    castings_danzel.py --los    Outfit-Karten + Casting-Presets Yacht_<Name>_A/_B/_C, je Fassung 2 Portraits
                                -> output\expressions\_casting_danzel\<Preset>_<A|B|C>
Danach Abnahme-Seite, Duc waehlt je Figur eine Fassung; erst dann Sprites.
Weiss bleibt Mr. White vorbehalten: kein weisser Anzug, nur Danzels Haar ist weiss.
"""
import io, json, sys, time, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, r"X:\AI\DucCommon")
import duc_common as dc  # noqa: E402

PS = "http://127.0.0.1:8301"
F_PRESETS = r"X:\AI\PromptStudio\presets.json"
JETZT = time.strftime("%Y-%m-%d %H:%M")
LOS = "--los" in sys.argv
NUR = sys.argv[sys.argv.index("--nur") + 1] if "--nur" in sys.argv else None      # z. B. --nur Yacht_Bibi
MODELL = {"unet": "krea2_turbo_fp8_scaled.safetensors", "clip": "qwen3vl_4b_fp8_scaled.safetensors"}
LORAS = [{"name": "Krea_Real3.safetensors", "strength": 0.7}, {"name": "Krea_Lenovo.safetensors", "strength": 0.7},
         {"name": "Krea_Redux.safetensors", "strength": 0.5}]
ORDNER = "_casting_danzel"
POSE = "neutral"
SEEDS = (240611, 977031)
HAUT = "natural skin texture with visible pores, slight natural asymmetry in the face, a real individual face"

# (Preset, ST-Name, Mann?, {Fassung: (Gesicht, Outfit)})
FIGUREN = [
    ("Yacht_Danzel", "Danzel", True, {
        "A": ("Danzel, a 29-year-old French-Vietnamese man, a slim boyish face with soft features, bright white hair "
              "slicked straight back with shiny gel, thin dark eyebrows, nervous dark eyes trying to look cool, a "
              "forced confident smirk, slender build",
              "an extravagant tailored crimson red agent suit with exaggerated padded shoulders and a long cut jacket, "
              "gold buttons, a black shirt, a thin black tie, red-tinted narrow sunglasses pushed up into his white "
              "hair, a small manga paperback sticking out of his breast pocket, pointed black shoes"),
        "B": ("Danzel, a 31-year-old Japanese-French man, a long elegant face with high cheekbones, silver-white hair "
              "slicked back in a dramatic swept wave, a small silver earring, slightly droopy eyes that give away his "
              "fear, one eyebrow raised in an attempt at menace, tall and lanky",
              "a flamboyant scarlet double-breasted agent suit with wide pointed lapels and a red silk lining, a "
              "black turtleneck under the jacket, round dark sunglasses, black leather gloves, an anime keychain "
              "dangling from his belt, glossy black shoes"),
        "C": ("Danzel, a 28-year-old Korean-French man, a friendly round face with a soft jaw, platinum white hair "
              "slicked back but with one loose strand falling on his forehead, wide anxious eyes, a big hopeful grin "
              "showing slightly crooked teeth, average build with narrow shoulders",
              "a slightly too big bright red agent suit with sharp exaggerated shoulder pads and a high stiff collar, "
              "a red-and-black patterned shirt, a gold chain, aviator sunglasses hanging from his collar, a "
              "telescopic baton he holds awkwardly like he has never used it, red sneakers"),
    }),
    ("Yacht_Bibi", "Bibi", False, {
        "A": ("Bibi, a 25-year-old French woman from Marseille, a lively round face with freckles, big bright green "
              "eyes, copper red hair in two high bouncy pigtails, a wide fierce grin trying to look evil, petite and "
              "energetic",
              "a fitted red agent suit jacket with rolled-up sleeves over a black top, short red suit trousers, a "
              "black utility belt with several round grenades, black combat boots, a small plush lion keychain that "
              "is entirely jet black on her belt"),
        "B": ("Bibi, a 24-year-old French woman of Algerian descent, an expressive oval face, dark sparkling eyes, "
              "thick black curly hair tied in two big puffy buns, thick eyebrows, a mischievous over-the-top grin, "
              "athletic and short",
              "a cropped red agent jacket with gold buttons over a black turtleneck, red cargo trousers tucked into "
              "black boots, a bandolier of round grenades across her chest, fingerless black gloves, a sticker of a "
              "cartoon boar on her jacket"),
        "C": ("Bibi, a 26-year-old French woman, a sharp pretty face with a tiny scar on her chin, warm brown eyes, "
              "bleached blonde hair with pink tips in two long braided pigtails, a gleeful dramatic villain smile, "
              "compact and strong",
              "a red agent suit with the jacket worn open over a black tank top, a red pleated skirt over black "
              "leggings, a heavy belt hung with round grenades, red-framed goggles pushed up on her head, chunky "
              "black boots"),
    }),
    ("Yacht_Charly", "Charly", False, {
        "A": ("Charly, a 26-year-old French woman, a calm heart-shaped face, sleepy half-closed grey eyes, a "
              "perfectly straight black chin-length bob with blunt bangs, a completely deadpan expression, tall and "
              "slim",
              "a neat red agent suit with a long jacket and straight trousers, a black shirt buttoned up, a "
              "headset with a small microphone around her neck, a taser in a holster, a bag of crisps sticking out "
              "of her jacket pocket, flat black shoes"),
        "B": ("Charly, a 25-year-old French woman of Vietnamese descent, a small delicate face, unimpressed dark "
              "eyes behind large round glasses, a sleek dark bob with one side tucked behind her ear, a flat bored "
              "mouth, slim",
              "an oversized red agent blazer over a black hoodie, red suit trousers, black sneakers, a tablet in one "
              "hand, a coiled taser cable on her belt, a lollipop stick in the corner of her mouth"),
        "C": ("Charly, a 27-year-old Senegalese-French woman, a long serene face, dark skin, heavy-lidded dark eyes "
              "with a dry look, short natural hair cut in a sharp tapered style, a tiny unamused smirk, tall and "
              "lean",
              "a sharp red agent suit with a short tailored jacket and cropped trousers, a black polo shirt, a tool "
              "belt with a taser and a small net launcher, wireless earbuds, a thermos cup in her hand, black ankle "
              "boots"),
    }),
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


def karte(preset, k):
    return "%s_%s" % (preset.split("_", 1)[1].lower(), k)       # danzel_A, bibi_B, ...


def main():
    global FIGUREN
    if NUR:
        FIGUREN = [f for f in FIGUREN if f[0] == NUR]
    for preset, name, mann, fassungen in FIGUREN:
        print("%-13s %-7s %s · Fassungen %s" % (preset, name, "Mann" if mann else "Frau", "/".join(fassungen)))
    if not LOS:
        print("Probelauf - nichts geschrieben. Mit --los anlegen und in die Warteschlange stellen.")
        return
    st = ps("/api/state")
    d = st["decks"]
    da = {c["name"]: c for c in d["outfit"]}
    for preset, _, _, fassungen in FIGUREN:
        for k, (_, outfit) in fassungen.items():
            kn = karte(preset, k)
            if kn in da:
                da[kn]["prompt"] = outfit
            else:
                d["outfit"].append({"name": kn, "prompt": outfit, "on": True, "tag": "eden_danzel", "sel": False,
                                    "back_prompt": outfit + ", seen from behind"})
    ps("/api/decks", d)
    presets = dc.load_json(F_PRESETS, None, "Studio")
    for preset, name, mann, fassungen in FIGUREN:
        for k, (gesicht, _) in fassungen.items():
            presets["%s_%s" % (preset, k)] = {
                "sprite_prompt": sprite_prompt(gesicht, mann), "loras": LORAS, "ref_image": "", "ref_image_b": "",
                "negative_prompt": "", "tags_on": ["View: Front"], "sp_stchar": name,
                "cards_on": {"outfit": [karte(preset, k)], "setting": ["A Sprite Background"], "st": [POSE]},
                "st_set": "%s/%s_%s" % (ORDNER, preset, k), "created": JETZT, "updated": JETZT}
    dc.save_json(F_PRESETS, presets, "Studio")
    alt = {k: st["cfg"].get(k) for k in ("sprite_prompt", "loras", "st_set", "sprite_src", "tags", "unet", "clip", "seed")}
    alt_preset = st["cfg"].get("preset_active")
    n = 0
    try:
        for preset, name, mann, fassungen in FIGUREN:
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
                        wahl = {"outfit": {karte(preset, k)}, "setting": {"A Sprite Background"}, "st": {POSE}}.get(kk, set())
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
