# -*- coding: utf-8 -*-
r"""Prompt Studio: drei neue Frauen fuer die Eden-Yacht-Welt (20.10.2026, Duc: "Erstelle 3 Frauen in Prompt Studio,
eine rothaarig, Irin; je 3 Outfits; 2x SFW, 1x Volllauf fuer das knappe Outfit; Real, Lenovo, Redux, NSFW").

    studio_neue_frauen.py          Probelauf: zeigt, was eingetragen wuerde
    studio_neue_frauen.py --los    traegt ein (Sicherungen *.vor-neue-frauen-<Zeit>.json)

Bewusst OHNE Identitaets-LoRA: die freien Charakter-LoRAs sind (laut Metadaten teils nachweislich) auf echte
Personen trainiert, und der Volllauf erzeugt explizite Posen. Die drei sind erfundene Gesichter: Aussehen aus Subject
und Tags, Identitaet in den Sprites ueber ein erzeugtes Referenzportraet (sprite_src i2i, ref_mode face) -
siehe frauen_laeufe.py. LoRAs: Krea_Real3 0.7, Krea_Lenovo 0.7, Krea_Redux 0.5, Krea_Nsfw2 0.7.
Vorhandene Eintraege gleichen Namens werden nicht ueberschrieben.
"""
import io, os, shutil, sys, time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, r"X:\AI\DucCommon")
import duc_common as dc  # noqa: E402

LOS = "--los" in sys.argv
PS = r"X:\AI\PromptStudio"
F_CFG, F_DECKS = os.path.join(PS, "studio-config.json"), os.path.join(PS, "decks.json")
F_PRESETS, F_SETS = os.path.join(PS, "presets.json"), os.path.join(PS, "set_presets.json")
EXPR = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions"
JETZT = time.strftime("%Y-%m-%d %H:%M")


def oc(name, prompt, back):
    return {"name": name, "prompt": prompt, "on": True, "tag": "eden-npc", "sel": False, "back_prompt": back}


OUTFITS = [
    # Saoirse Gallagher - irische Fiddlerin in Alvas Bar
    oc("saoirse_pub_a",
       "a moss green chunky knit cardigan over a cream lace-trimmed blouse, a short dark green tartan skirt, black opaque "
       "tights, brown leather ankle boots, a silver Claddagh ring",
       "moss green chunky knit cardigan from behind, short dark green tartan skirt, black opaque tights, brown ankle boots"),
    oc("saoirse_session_a",
       "an emerald green velvet wrap dress with long sleeves and a deep V-neck, a thin gold necklace with a small Celtic "
       "knot pendant, black heeled ankle boots",
       "emerald green velvet wrap dress from behind, the tie bow at her waist, black heeled ankle boots"),
    oc("saoirse_lace_a",
       "a skimpy emerald green lace lingerie set: a lace balconette bra, high-cut lace panties, a lace garter belt with "
       "sheer black stockings, a black velvet choker",
       "emerald green lace bra straps on her bare back, high-cut lace panties, garter straps, sheer black stockings"),
    # Kaori Mizuno - Schiffbauingenieurin der Werft in Calvi
    oc("kaori_werft_a",
       "a fitted navy work coverall with the top half unzipped and tied around her waist, a white ribbed tank top, a "
       "black tool belt, steel-toe work boots, a white hard hat under her arm",
       "white ribbed tank top from behind, navy coverall sleeves tied around her waist, tool belt, steel-toe work boots"),
    oc("kaori_office_a",
       "a charcoal grey pencil skirt, a crisp white blouse with the sleeves rolled up, a thin black belt, black low "
       "heels, an ID badge on a blue lanyard",
       "white blouse tucked into a charcoal grey pencil skirt from behind, thin black belt, black low heels"),
    oc("kaori_silk_a",
       "a short black silk kimono-style robe hanging open over a black satin bralette and matching high-cut panties, "
       "sheer black thigh-high stockings, black high heels",
       "short black silk robe sliding off her shoulders from behind, black satin panties, sheer thigh-high stockings, "
       "black high heels"),
    # Imani Dubois - Skipperin eines Konkurrenz-Katamarans in der Bucht
    oc("imani_skipper_a",
       "a white short-sleeved skipper polo shirt with navy epaulettes, navy sailing shorts, a navy baseball cap, black "
       "fingerless sailing gloves, white boat shoes",
       "white skipper polo from behind, navy sailing shorts, navy cap, white boat shoes"),
    oc("imani_evening_a",
       "a gold satin slip dress with thin straps and a cowl neckline, large gold hoop earrings, strappy gold sandals",
       "gold satin slip dress with thin crossed straps on her bare back, strappy gold sandals"),
    oc("imani_bikini_a",
       "a skimpy white string bikini with tiny triangle cups and high-cut ties at the hips, a thin gold body chain "
       "around her waist, barefoot",
       "white string bikini with ties at her back and hips, thin gold body chain around her waist, barefoot"),
]


def prompts(subject):
    wer = "one single woman alone in the frame, her whole body in full view"
    block = ("Subject: %s,\nBody: {tags_body},\nHair: {tags_haircolor}, {tags_hairstyle}, {tags_hair}\n"
             "Skin: {tags_skin},\nMakeup: {tags_face}\n" % subject)
    sprite = ("{tags_action}, Shot on an iPhone, grainy amateur photo, realistic smartphone photography, "
              "full body shot from head to knees, direct gaze, %s, head and knees inside the frame,\n%s"
              "Wearing: {outfit},\nScene: {setting}, {st},\n{expression},\nLook: {look},\n{tags_photo}" % (wer, block))
    base = ("{tags_action}, full body shot from head to knees, solo, %s, head and knees inside the frame,\n%s"
            "Wearing: {outfit},\nPose: {pose}\nScene: {setting}\n{st}\n{expression}\nLook: {look}\n{tags_photo}"
            % (wer, block))
    fashion = ("{tags_action}, front view, full body shot from head to knees, standing in full view, beige plain "
               "background,\n%sWearing: {outfit},\nPose: {pose},\n{st},\n{tags_photo}" % block)
    return sprite, base, fashion


NEG = ("oversaturated, deep fried colors, anime, 3d render, three arms, extra arm, extra limb, duplicated limbs, "
       "disconnected hand, malformed hands, extra fingers, selfie, phones, child, teen, underage,")
LORAS = [{"name": "Krea_Real3.safetensors", "strength": 0.7}, {"name": "Krea_Lenovo.safetensors", "strength": 0.7},
         {"name": "Krea_Redux.safetensors", "strength": 0.5}, {"name": "Krea_Nsfw2.safetensors", "strength": 0.7}]
MODE_OPTS = {m: {"ref_mode": "face", "face_context": 2.4, "aspect": a, "width": w, "height": h,
                 "ref_boost_mode": "off", "ref_boost_value": 4}
             for m, a, w, h in (("sprite", "880x1328", 880, 1328), ("setting", "2:3", 832, 1216),
                                ("fashion", "2:3", 832, 1216), ("i2i", "880x1328", 880, 1328))}

S_BASIS = ["View: Front", "Color: Red", "Style: Waves", "Freckles", "Pale skin", "Body: Slender", "B - Soft"]
K_BASIS = ["View: Front", "Color: Black", "Style: Bob", "Style: Bangs", "Glasses", "Body: Slender"]
I_BASIS = ["View: Front", "Color: Black", "Style: Braided Ponytail", "Body: Athletic", "Body: Curvy", "Large"]

FIGUREN = {
    "Yacht_Saoirse": {
        "st_name": "Saoirse Gallagher",
        "subject": "Saoirse Gallagher, a 27-year-old Irish woman from Galway with bright green eyes, a light dusting of "
                   "freckles across her nose and cheeks and long curly copper-red hair",
        "kost": ["Pub", "Session", "Lace"],
        "sets": {"Pub": ("saoirse_pub_a", S_BASIS + ["State: Messy", "Clean Girl", "Blush"]),
                 "Session": ("saoirse_session_a", S_BASIS + ["Instagirl Soft Glam", "Glossy Lips"]),
                 "Lace": ("saoirse_lace_a", S_BASIS + ["State: Messy", "Boudoir Glam", "Sheen"])}},
    "Yacht_Kaori": {
        "st_name": "Kaori Mizuno",
        "subject": "Kaori Mizuno, a 31-year-old Japanese woman from Yokohama with dark brown eyes, a sleek chin-length "
                   "black bob with straight bangs and thin black-rimmed glasses",
        "kost": ["Werft", "Office", "Silk"],
        "sets": {"Werft": ("kaori_werft_a", K_BASIS + ["Sport Athleisure", "Sweat"]),
                 "Office": ("kaori_office_a", K_BASIS + ["Office Polish", "Nude Lips"]),
                 "Silk": ("kaori_silk_a", K_BASIS + ["State: Sleeked", "Smokey Eye", "Glossy Lips", "Sheen"])}},
    "Yacht_Imani": {
        "st_name": "Imani Dubois",
        "subject": "Imani Dubois, a 29-year-old French-Senegalese woman from Marseille with smooth deep brown skin, warm "
                   "dark brown eyes, full lips and long black box braids",
        "kost": ["Skipper", "Evening", "Bikini"],
        "sets": {"Skipper": ("imani_skipper_a", I_BASIS + ["Summer", "Sheen"]),
                 "Evening": ("imani_evening_a", I_BASIS + ["Full Glam", "Glossy Lips", "Hoop Earrings"]),
                 "Bikini": ("imani_bikini_a", I_BASIS + ["Summer", "Wet", "Sheen"])}},
}


def preset(name, f):
    sprite, base, fashion = prompts(f["subject"])
    k = f["kost"]
    roh = lambda kost: os.path.join(EXPR, name, kost, "roh")
    srt = lambda kost: os.path.join(EXPR, name, kost, "Sorted")
    return {
        "base_prompt": base, "sprite_prompt": sprite, "fashion_prompt": fashion, "negative_prompt": NEG,
        "loras": LORAS, "ref_image": "", "ref_image_b": "",
        "st_set": "%s/%s/roh" % (name, k[0]),
        "save_path": r"X:\AI\ComfyUI_krea2\ComfyUI\output\studio\SET1",
        "sp_char": name, "sp_stchar": f["st_name"], "sp_k1": k[0], "sp_k2": k[1], "sp_aktiv": 1, "sp_kost": k,
        "sv_char": f["st_name"], "sv_set1": srt(k[0]), "sv_set2": srt(k[1]), "sv_sets": [srt(x) for x in k],
        "st_src": roh(k[0]), "st_dst": srt(k[0]), "mode_opts": MODE_OPTS, "tags_on": f["sets"][k[0]][1],
        "cards_on": {"outfit": [f["sets"][k[0]][0]], "setting": ["A Sprite Background"], "st": ["neutral"]},
        "created": JETZT, "updated": JETZT,
    }


def main():
    cfg, decks = dc.load_json(F_CFG, None, "Studio"), dc.load_json(F_DECKS, None, "Studio")
    presets, sets = dc.load_json(F_PRESETS, None, "Studio"), dc.load_json(F_SETS, None, "Studio")
    tag_namen = {t["name"] for t in cfg["tags"]}
    out_namen = {o["name"] for o in decks["outfit"]}
    neue_out = [o for o in OUTFITS if o["name"] not in out_namen]
    fehler, neue_presets, neue_sets = [], {}, {}
    for name, f in FIGUREN.items():
        for kost, (outfit, tags) in f["sets"].items():
            fehler += ["%s|%s: Tag fehlt: %s" % (name, kost, t) for t in tags if t not in tag_namen]
            if outfit not in out_namen | {o["name"] for o in neue_out}:
                fehler.append("%s|%s: Outfit fehlt: %s" % (name, kost, outfit))
            key = "%s|%s" % (name, kost)
            if key not in sets:
                neue_sets[key] = {"outfit": [outfit], "setting": ["A Sprite Background"], "tags": tags}
        if name not in presets:
            neue_presets[name] = preset(name, f)
        else:
            print("  übersprungen (gibt es schon): Preset", name)
    print("Outfit-Karten neu: %d · Presets neu: %s · Kostüm-Presets neu: %d"
          % (len(neue_out), ", ".join(neue_presets) or "-", len(neue_sets)))
    if fehler:
        print("FEHLER:\n  " + "\n  ".join(fehler))
        sys.exit(1)
    if not LOS:
        print("Probelauf - nichts geschrieben. Mit --los eintragen.")
        return
    stempel = time.strftime("%Y%m%d_%H%M%S")
    for pfad in (F_CFG, F_DECKS, F_PRESETS, F_SETS):
        shutil.copy2(pfad, pfad.replace(".json", ".vor-neue-frauen-%s.json" % stempel))
    decks["outfit"].extend(neue_out)
    presets.update(neue_presets)
    sets.update(neue_sets)
    dc.save_json(F_DECKS, decks, "Studio")
    dc.save_json(F_PRESETS, presets, "Studio")
    dc.save_json(F_SETS, sets, "Studio")
    print("Eingetragen. Sicherungen: *.vor-neue-frauen-%s.json" % stempel)


if __name__ == "__main__":
    main()
