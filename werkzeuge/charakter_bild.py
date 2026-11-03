# -*- coding: utf-8 -*-
r"""Duc's character-screen portraits (25.10.2026): front view, full body, every jacket look x weapon class, on the
sunny aft deck, always grinning or laughing (Duc).

Same identity as the combat sprites: Prompt Studio's model set, the LoRAs of the preset Kampf_Duc<Look> and the look
card kampf_duc<look> (read live from Prompt Studio, port 8301, only read). Weapon and pose come from WAFFEN below.

    python werkzeuge\charakter_bild.py Erde Bat            2 variants -> docs\abnahme\charakter\DucErdeBat_v1..2.png
    python werkzeuge\charakter_bild.py alle                all 26 combinations (5 looks x 5 weapons + Erde x Mop)
    python werkzeuge\charakter_bild.py alle --n 3          more variants
    python werkzeuge\charakter_bild.py --waehle DucErdeBat 2   variant 2 -> module\eden_rise\charakter\DucErdeBat.webp

Needs ComfyUI Krea2 (8189) and Prompt Studio (8301).
"""
import json, os, random, shutil, sys, time, urllib.request

sys.stdout.reconfigure(encoding="utf-8")
EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMFY, PS = "http://127.0.0.1:8189", "http://127.0.0.1:8301"
PRESETS = r"X:\AI\PromptStudio\presets.json"
STUDIO_CFG = r"X:\AI\PromptStudio\studio-config.json"
ZIEL = os.path.join(EDEN, "docs", "abnahme", "charakter")
SPIEL = os.path.join(EDEN, "module", "eden_rise", "charakter")      # chosen images, served at /charakterbild/<name>
W, H = 880, 1328

LOOKS = ["Erde", "Wasser", "Feuer", "Luft", "Cyber"]   # jacket_earth, jacket_water, jacket_fire, jacket_air, cyber_armor
# weapon class: pose with the weapon (the bat on the shoulder, the rest in their own pose (Duc 25.10.))
WAFFEN = {
    # Duc 25.10.: the bat stays on the shoulder (the first test), the other weapons get their own poses
    "Bat": "holding one single long matte black wooden bat with a thick rounded barrel in his right hand, the bat "
           "resting casually on his right shoulder, his left thumb hooked into the front pocket of his jeans",
    "Sword": "holding one single curved steel cavalry sabre with a brass hand guard point down in his right hand, the tip "
             "resting on the deck in front of his right boot, his left hand on his hip",
    # Duc 26.10.: pose 2 of the four proposals (reverse grip, forearm across the chest) is the knife pose for every jacket
    "Knife": "holding one single medium-sized combat knife with a single-edged steel blade and a black grip in a reverse "
             "grip in his right hand, the forearm crossed in front of his chest and the blade pointing down along his arm, "
             "the steel catching the light, his left hand on his hip",
    "Spear": "holding one single boar spear upright in his right hand with its butt planted on the deck beside his "
             "boot: a long dark wooden shaft taller than him, a broad leaf-shaped steel spearhead and a short steel "
             "crossbar high above his head, his left hand on his hip",
    "Gun": "holding one single closed double-barrel shotgun with side-by-side steel barrels and a dark wooden stock "
           "diagonally across his body in both hands at waist height, the barrels pointing up to the left, the gun "
           "kept closed in one straight rigid line",
    "Mop": "leaning with both hands on the top of one single T-shaped wooden deck scrubber standing upright in front "
           "of him: a long plain wooden handle with a wide rectangular wooden brush block fixed crosswise at its end on "
           "the deck, a thick dense row of white bristles",
}
# Duc 26.10.: the knife should be shown off - four pose proposals (python charakter_bild.py Erde Knife --messer --matt)
MESSER = [
    "holding one single medium-sized combat knife with a single-edged steel blade and a black grip up in front of his chest "
    "in his right hand, the blade held horizontally across his body with its flat side facing the viewer so the whole blade "
    "is clearly visible, his left hand relaxed at his side",
    "holding one single medium-sized combat knife with a single-edged steel blade and a black grip in a reverse grip in his "
    "right hand, the forearm crossed in front of his chest and the blade pointing down along his arm, the steel catching "
    "the light, his left hand on his hip",
    "holding one single medium-sized combat knife with a single-edged steel blade and a black grip up beside his face in "
    "his right hand, the blade pointing straight up, looking sideways at the blade with a confident grin, his left hand "
    "in his jeans pocket",
    "in a wide ready stance with his weight low, holding one single medium-sized combat knife with a single-edged steel "
    "blade and a black grip stretched out in front of him in his right hand, the blade pointing diagonally forward at the "
    "viewer, his left hand open behind it",
]
LAUNE = ["a big genuine wide grin showing his teeth", "a cool confident wide grin, one eyebrow slightly raised"]    # grin, never laughing (Duc 26.10.)
# background tests (Duc 25.10.: the sunny deck did not feel immersive) - python charakter_bild.py Erde Bat --orte
ORTE = {
    "Bruecke": "standing on the dimly lit bridge of a luxury motor yacht at golden hour, dark mahogany and brass instrument "
               "consoles, a large navigation screen glowing softly, a ship's wheel behind him, the tall front windows full "
               "of deep orange sunset light over the coast, warm light rim-lighting his jacket, a calm moody atmosphere",
    "Nacht": "standing on the aft deck of a luxury motor yacht at blue hour just after sunset, a deep blue sky, warm golden "
             "light spilling from the open lounge doors behind him, strings of small warm lights above, the glowing lights "
             "of a harbour town across calm dark water, a soft evening glow on his face and jacket",
    "Werkstatt": "standing in the cluttered engine workshop below deck of a luxury yacht, a wooden workbench with tools "
                 "behind him, a wall of hanging tools, polished steel machinery, warm tungsten work lamps, a few golden "
                 "sparks glowing in the air, smoky warm light, a lived-in and slightly rough atmosphere",
    "Kabine": "standing in his small private cabin on a luxury yacht, a neatly made bunk with a dark blue blanket, a wooden "
              "sea chest, a round porthole with warm evening light, a reading lamp glowing, a few personal belongings on "
              "a shelf, honey-coloured wood panelling, a calm cosy atmosphere",
}
# --matt: studio cut-out like the game sprites (plain backdrop, soft matte light, BEN2 cut-out as alpha), only grinning
SZENE_MATT = ("standing on a plain smooth seamless warm beige studio floor in front of a plain beige studio backdrop, soft "
              "diffuse even studio light from the front, matte, no harsh highlights, no sunlight, no shiny reflections, "
              "no strong shadows")
ZIEL_MATT = os.path.join(EDEN, "docs", "abnahme", "charakter", "matt")
SZENE = ("standing on the sunny aft deck of a luxury motor yacht, warm honey-coloured teak deck planks, polished "
         "white railings and a stainless steel rail behind him, the bright turquoise Mediterranean sea and a clear blue "
         "sky beyond, brilliant warm sunshine, crisp summer light")
VORLAGE = ("Shot on an iPhone, realistic photography, full body shot, one single man alone in the frame, his whole body "
           "in full view from head to boots, straight front view facing the viewer,\nSubject: Ducx, an Asian man in his "
           "early thirties, black hair with a clean side part slicked back, light stubble, dark brown eyes, slim "
           "athletic build, {laune},\nPose: standing upright in a relaxed cool confident pose, {waffe},\nWearing: "
           "{outfit},\nScene: {szene}")


# --gefuehle: Duc's SFW expressions for dialogues (Duc 03.11.2026), per jacket, no weapon, studio cut-out like --matt.
# Poses are the 😇 cards of Prompt Studio's ST deck without back views and without the two cards made for women;
# the cards are written for women, so pronouns are switched and a few cards get a version for Duc.
# The sunglasses always stay on his face - a running gag that should become cult (Duc 03.11.2026).
#   python werkzeuge\charakter_bild.py Erde --gefuehle      -> docs\abnahme\charakter\gefuehle\DucErde\<pose>.png
ZIEL_GEF = os.path.join(EDEN, "docs", "abnahme", "charakter", "gefuehle")
GEF_OHNE = {"submissive", "worshipful"}
GEF_DUC = {
    "admiration": "He stands with one hand pressed flat to his cheek and the other laid across his chest, leaning back a "
                  "little, his weight on one leg, the other leg angled. Starstruck admiring face, warm shining eyes, lips "
                  "parted in a soft wow, brows lifted.",
    "love": "He stands with his hands clasped behind his back, leaning slightly forward, his weight on one leg. Melting "
            "affectionate face, soft warm eyes, a warm closed-lip smile.",
    "approval": "Warm approving grin, relaxed crinkled eyes, one corner of his mouth pulled higher. He stands giving a thumbs "
                "up toward the camera with one hand, the other resting on his hip, weight on one leg.",
    "annoyance": "He stands with his arms crossed tight, his weight on one leg, one foot tapping, his head turned back over "
                 "his shoulder. Irritated flat stare, one eyebrow arched, lips pressed into a line, jaw shifted to one side.",
    "surprise": "He stands with his weight rocked back onto one heel mid-flinch, both hands flying up beside his face. "
                "Jolted startled face, brows shot up, mouth dropped open in a gasp.",
    "embarrassment": "He stands with his shoulders raised, one hand rubbing the back of his neck, the other hand in his "
                     "jeans pocket, glancing slightly away. Mortified flustered face, natural flush across his cheeks, "
                     "brows raised, a tight awkward smile.",
    "grief_2": "He sits collapsed on the floor with his knees drawn up to his chest, both arms wrapped around his legs, face "
               "lifted slightly toward the camera. Grief-stricken face, eyes red and swollen, mouth trembling open in a "
               "silent sob, brows crumpled.",
    # Duc's first run 03.11.: words that lower the body make him sit (KREA_LEITFADEN), the kicked-out leg left the frame
    "disappointment": "He stands with sagging shoulders, arms hanging heavy at his sides, head turned toward the camera, "
                      "both legs straight. Flat deflated face, dull eyes, mouth pulled down at the corners, slack brows.",
    "sadness": "He stands upright and hugs himself tightly with both arms, shoulders curled forward, both legs straight. "
               "Glassy brimming eyes, trembling chin, corners of his mouth pulled down, brows pinched in the middle.",
    "annoyance_2": "He stands with both hands planted on his hips, elbows out wide, head tipped back in an exasperated "
                   "exhale, his weight on one leg. Exasperated flat stare, eyes half-rolled, lips pressed into a thin "
                   "unimpressed line.",
    "joy_2": "He jumps straight up with both arms flung up and his head thrown back, both knees bent beneath him, his "
             "whole body in the middle of the frame, his clothes caught mid-motion. Unrestrained joyful laugh, mouth wide "
             "open in delight.",
    # the card leans against a wall that the studio does not have: he sat on the floor and left the frame
    "relief_2": "He stands with one hand pressed flat to his forehead, the other arm hanging loose, shoulders visibly "
                "dropping, both legs straight. Relieved unwinding face, a long breathy smile.",
}
VORLAGE_GEF = ("Shot on an iPhone, realistic photography, full body shot, one single man alone in the frame, his whole body "
               "in full view from head to boots,\nSubject: Ducx, an Asian man in his early thirties, black hair with a clean "
               "side part slicked back, light stubble, dark brown eyes, slim athletic build, always wearing his sunglasses "
               "on his face, the feeling shows in his mouth, brows and body,\nPose: {pose} He carries no weapon.\n"
               "Wearing: {outfit},\nScene: {szene}")
SZENE_GEF = SZENE_MATT.replace("standing on a plain", "on a plain")       # some feelings sit or kneel


def er(text):
    """ST card text (written for women) -> Duc."""
    import re
    wort = {"She": "He", "she": "he", "Her": "His", "her": "his", "hers": "his", "herself": "himself", "Herself": "Himself"}
    return re.sub(r"\b(She|she|Her|her|hers|herself|Herself)\b", lambda m: wort[m.group(1)], text)


def gefuehle(look, cfg, presets, decks):
    import re
    karten = {c["name"]: c["prompt"] for c in decks["outfit"]}
    outfit = karten.get("kampf_duc" + look.lower())
    if not outfit:
        print("Outfit-Karte kampf_duc%s fehlt" % look.lower())
        return {}
    erlaubt = cfg.get("sfw_posen")
    posen = [c for c in decks["st"] if c.get("on") is not False and (erlaubt is None or c["name"] in erlaubt)
             and c["name"] not in GEF_OHNE and not c["name"].endswith("_back")]
    loras = presets["Kampf_Duc" + look]["loras"]
    ordner = os.path.join(ZIEL_GEF, "Duc" + look)
    os.makedirs(ordner, exist_ok=True)
    auftraege = {}
    for c in posen:
        if "--neu" not in sys.argv and os.path.exists(os.path.join(ordner, c["name"] + ".png")):
            continue
        pose = GEF_DUC.get(c["name"]) or er(c["prompt"]).strip().rstrip(",")
        pose = re.sub(r"^([a-z])", lambda m: "He " + m.group(1), pose)
        prompt = VORLAGE_GEF.format(pose=pose if pose.endswith(".") else pose + ".", outfit=outfit.rstrip(" ,"), szene=SZENE_GEF)
        g = graph(prompt, c["name"], random.randint(1, 2 ** 31), cfg, loras, matt=True)
        g["9"]["inputs"]["save_path"] = ordner
        auftraege["Duc%s/%s" % (look, c["name"])] = post("/prompt", {"prompt": g})["prompt_id"]
    print("eingereiht: Duc%s, %d Posen" % (look, len(auftraege)))
    return auftraege


def gefuehle_uebernehmen(looks):
    """--gefuehle-uebernehmen: accepted feelings -> module\\eden_rise\\charakter\\gefuehle\\Duc<Look>\\<pose>.webp
    (Duc 03.11.2026: all accepted). eden.duc_bild picks them for Duc's lines by the jacket he wears."""
    from PIL import Image
    for look in looks:
        quelle, ziel = os.path.join(ZIEL_GEF, "Duc" + look), os.path.join(SPIEL, "gefuehle", "Duc" + look)
        os.makedirs(ziel, exist_ok=True)
        n = 0
        for f in sorted(os.listdir(quelle)):
            if f.endswith(".png"):
                with Image.open(os.path.join(quelle, f)) as im:
                    im.convert("RGBA").save(os.path.join(ziel, f[:-4] + ".webp"), "WEBP", quality=90, method=6)
                n += 1
        print("uebernommen: Duc%s, %d Gefuehle" % (look, n))


def get(url):
    return json.loads(urllib.request.urlopen(url, timeout=60).read())


def post(pfad, daten):
    req = urllib.request.Request(COMFY + pfad, data=json.dumps(daten).encode(), headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=60).read())


def graph(prompt, name, seed, cfg, loras, matt=False):
    g = {"1": {"class_type": "UNETLoader", "inputs": {"unet_name": cfg["unet"], "weight_dtype": "default"}},
         "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": cfg["clip"], "type": "krea2", "device": "default"}},
         "3": {"class_type": "VAELoader", "inputs": {"vae_name": cfg["vae"]}}}
    model, clip = ["1", 0], ["2", 0]
    for i, l in enumerate(loras):
        k = "L%d" % i
        g[k] = {"class_type": "LoraLoader", "inputs": {"model": model, "clip": clip, "lora_name": l["name"],
                                                       "strength_model": l["strength"], "strength_clip": l["strength"]}}
        model, clip = [k, 0], [k, 1]
    g.update({
        "4": {"class_type": "CLIPTextEncode", "inputs": {"text": prompt, "clip": clip}},
        "5": {"class_type": "CLIPTextEncode", "inputs": {"text": "", "clip": clip}},
        "6": {"class_type": "EmptySD3LatentImage", "inputs": {"width": W, "height": H, "batch_size": 1}},
        "7": {"class_type": "KSampler", "inputs": {"seed": seed, "steps": cfg["steps"], "cfg": cfg["cfg"],
                                                    "sampler_name": cfg["sampler"], "scheduler": cfg["scheduler"],
                                                    "denoise": 1.0, "model": model, "positive": ["4", 0],
                                                    "negative": ["5", 0], "latent_image": ["6", 0]}},
        "8": {"class_type": "VAEDecode", "inputs": {"samples": ["7", 0], "vae": ["3", 0]}},
        "9": {"class_type": "DucSave", "inputs": {"images": ["8", 0], "save_path": ZIEL_MATT if matt else ZIEL, "filename_prefix": name,
                                                  "use_input_filename": False, "image_format": "PNG", "jpg_quality": 95,
                                                  "counter_style": "NONE", "show_preview": False, "overwrite": True}},
    })
    if matt:       # same cut-out as Prompt Studio's sprite mode: BEN2 mask becomes the alpha channel
        g["10"] = {"class_type": "easy imageRemBg", "inputs": {"images": ["8", 0], "rem_mode": "BEN2", "image_output": "Hide",
                                                                "save_prefix": "ComfyUI", "torchscript_jit": False,
                                                                "add_background": "none", "refine_foreground": False}}
        g["9"]["inputs"]["alpha_mask"] = ["10", 1]
    return g


def kombis(args):
    if args[:1] == ["elemente"]:                  # test run: the four leather jackets with the bat
        return [(l, "Bat") for l in LOOKS[:4]]
    if args[:1] == ["alle"]:                      # "alle Bat": every look with one weapon
        alle = [(l, w) for l in LOOKS for w in WAFFEN if w != "Mop"] + [("Erde", "Mop")]
        return [k for k in alle if len(args) < 2 or k[1] == args[1]]
    return [tuple((args + ["Erde", "Bat"])[:2])]


def waehlen(basis, k):
    from PIL import Image
    os.makedirs(SPIEL, exist_ok=True)
    k = ("v%d" % k) if str(k).isdigit() else k
    quelle = os.path.join(ZIEL_MATT, "%s_%s.png" % (basis, k))
    matt = "--matt" in sys.argv and os.path.exists(quelle)
    with Image.open(quelle if matt else os.path.join(ZIEL, "%s_%s.png" % (basis, k))) as im:
        im.convert("RGBA" if matt else "RGB").save(os.path.join(SPIEL, basis + ".webp"), "WEBP", quality=90, method=6)
    print("uebernommen:", basis, "Variante", k)


def main():
    if "--waehle" in sys.argv:
        i = sys.argv.index("--waehle")
        return waehlen(sys.argv[i + 1], sys.argv[i + 2])
    if "--gefuehle-uebernehmen" in sys.argv:          # python werkzeuge\charakter_bild.py alle --gefuehle-uebernehmen
        wahl = [a for a in sys.argv[1:] if not a.startswith("--")]
        return gefuehle_uebernehmen(LOOKS if wahl[:1] in ([], ["alle"]) else wahl[:1])
    args = [a for i, a in enumerate(sys.argv[1:], 1) if not a.startswith("--") and sys.argv[i - 1] != "--n"]
    n = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 2
    matt = "--matt" in sys.argv
    orte = [("", SZENE_MATT if matt else SZENE)] if "--orte" not in sys.argv else [("_" + k, v) for k, v in ORTE.items()]
    if "--orte" in sys.argv:
        n = 1
    cfg = json.load(open(STUDIO_CFG, encoding="utf-8-sig"))
    presets = json.load(open(PRESETS, encoding="utf-8-sig"))
    decks = get(PS + "/api/state")["decks"]
    karten = {c["name"]: c["prompt"] for c in decks["outfit"]}
    os.makedirs(ZIEL, exist_ok=True)
    auftraege = {}
    if "--gefuehle" in sys.argv:
        for look in (LOOKS if args[:1] == ["alle"] else args[:1] or ["Erde"]):
            auftraege.update(gefuehle(look, cfg, presets, decks))
    for look, waffe in ([] if "--gefuehle" in sys.argv else kombis(args)):
        basis = "Duc%s%s" % (look, waffe)
        outfit = karten.get("kampf_duc" + look.lower())
        if not outfit:
            print("Outfit-Karte kampf_duc%s fehlt - uebersprungen" % look.lower())
            continue
        loras = (presets.get("Kampf_" + basis) or presets["Kampf_Duc" + look])["loras"]
        if matt and "--neu" not in sys.argv and "--messer" not in sys.argv and os.path.exists(os.path.join(ZIEL_MATT, basis + "_v1.png")):
            print("vorhanden, uebersprungen:", basis)          # --neu renders it again
            continue
        messer = "--messer" in sys.argv and waffe == "Knife"
        for ort, szene in orte:
            for k in range(1, (len(MESSER) if messer else (1 if waffe == "Mop" else n)) + 1):       # the scrubber only until Terremoto arrives: one image (Duc 26.10.)
                prompt = VORLAGE.format(laune=LAUNE[0 if messer else (k - 1) % len(LAUNE)], waffe=MESSER[k - 1] if messer else WAFFEN[waffe], outfit=outfit.rstrip(" ,"), szene=szene)
                name = "%s%s_%s%d" % (basis, ort, "p" if messer else "v", k)
                auftraege[name] = post("/prompt", {"prompt": graph(prompt, name, random.randint(1, 2 ** 31), cfg, loras, matt)})["prompt_id"]
        print("eingereiht:", basis)
    t0 = time.time()
    while auftraege and time.time() - t0 < 3 * 3600:
        time.sleep(4)
        for name, pid in list(auftraege.items()):
            h = get(COMFY + "/history/" + pid)
            if pid in h and h[pid].get("status", {}).get("completed"):
                print("fertig:", name, flush=True)
                auftraege.pop(name)
    print("alle fertig" if not auftraege else "offen: " + ", ".join(auftraege))


if __name__ == "__main__":
    main()
