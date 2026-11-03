# -*- coding: utf-8 -*-
r"""Prompt Studio: Mr. Maximum, Yamamoto-san und Jana Maihoff anlegen (19.10.2026).

    studio_maximum_yamamoto_jana.py          Probelauf: zeigt, was eingetragen wuerde, schreibt nichts
    studio_maximum_yamamoto_jana.py --los    traegt ein (Prompt Studio muss AUS sein)

Entwurf: Y:\AI\mission-control\entwuerfe\prompt-studio-maximum-yamamoto.md
- 19 Maenner-Tags in EINER Gruppe "Maenner" (studio-config.json -> tags); cat je Tag verschieden (Prompt-Zeile).
- Outfit-Karten (decks.json -> outfit, tag eden-npc), Presets (presets.json), Set-Presets (set_presets.json).
- Prinzip wie Megans Sprite-Prompt: kurzes Subject, Aussehen ueber Tags; Tag-Platzhalter in ALLEN drei Prompts
  (Sprite/Fashion verwerfen sonst die Tags).
- Vorhandene Eintraege gleichen Namens werden NICHT ueberschrieben (uebersprungen und gemeldet).
- Sicherungen: <datei>.vor-maximum-yamamoto-jana-<Zeit>.json
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

# ------------------------------------------------------------------ Maenner-Tags
def mt(name, cat, prompt):
    return {"name": name, "prompt": prompt, "on": False, "cat": cat, "grp": "Männer", "sec": "Body"}

TAGS = [
    mt("M Body: Bodybuilder", "body", "a massive bodybuilder physique, broad rounded shoulders, huge arms, a thick chest and neck"),
    mt("M Body: Dad Bod", "body", "a soft middle-aged body with a small round belly and narrow shoulders"),
    mt("M Abs", "body", "a shredded six-pack"),
    mt("M Veins", "body", "thick veins on his forearms and biceps"),
    mt("M Tall", "body", "very tall, towering over everyone around him"),
    mt("M Short", "body", "short, about one metre sixty-five"),
    mt("M Skin: Deep Brown", "skin", "smooth deep brown skin"),
    mt("M Skin: Fair Warm", "skin", "fair skin with a warm undertone"),
    mt("M Skin: Oiled", "skin", "oiled glistening skin, every muscle catching the light"),
    mt("M Sweat", "skin", "a light sheen of sweat on his skin and forehead"),
    mt("M Flush: Drunk", "skin", "bright red flushed cheeks and nose"),
    mt("M Hair: Bald Shine", "hairstyle", "a smooth shaved bald head with a light shine"),
    mt("M Hair: Side Part", "hairstyle", "short neatly combed hair with a razor-sharp side part"),
    mt("M Hair: Messed Up", "hair", "his neat hair messed up, strands sticking out in all directions"),
    mt("M Color: Black Grey Temples", "haircolor", "black hair greying at the temples"),
    mt("M Face: Clean-Shaven", "face", "clean-shaven"),
    mt("M Face: Goatee", "face", "a short neat goatee"),
    mt("M Face: Thin Moustache", "face", "a thin neat moustache"),
    mt("M Glasses: Rimless", "face", "thin rimless rectangular glasses"),
]

# ------------------------------------------------------------------ Outfit-Karten
def oc(name, prompt, back):
    return {"name": name, "prompt": prompt, "on": True, "tag": "eden-npc", "sel": False, "back_prompt": back}

OUTFITS = [
    # Mr. Maximum
    oc("maximum_steward_a",
       "a white short-sleeved crew steward shirt with gold epaulettes, stretched to bursting over his chest and arms, the buttons straining, a small golden anchor logo on the right chest, a black name badge reading MR. MAXIMUM, navy tailored shorts, white deck sneakers",
       "white steward shirt stretched tight across his broad back, gold epaulettes on the shoulders, navy tailored shorts, white deck sneakers"),
    oc("maximum_steward_b",
       "a fitted navy crew polo shirt with a small golden anchor logo on the right chest, the sleeves rolled up over his biceps, a white towel over one shoulder, beige chino shorts, white deck sneakers, a silver whistle on a lanyard",
       "navy crew polo stretched across his back, white towel hanging down from one shoulder, beige chino shorts, white deck sneakers"),
    oc("maximum_training_a",
       "a black ribbed stringer tank top with deep armholes, grey jogger shorts, a black leather lifting belt, white high-top training shoes, black wrist wraps",
       "black stringer tank top with a racer back showing his back muscles, black lifting belt, grey jogger shorts, white high-top training shoes"),
    oc("maximum_training_b",
       "a neon yellow sleeveless gym shirt printed with MR. MAXIMUM in bold black letters, black compression shorts, black training shoes, a white sweatband on his forehead, a towel around his neck",
       "neon yellow sleeveless gym shirt with MAXIMUM printed across the back, black compression shorts, black training shoes, towel ends hanging down his chest"),
    oc("maximum_party_a",
       "a lilac linen suit with the jacket open over his bare chest, a white pocket square, white loafers without socks, gold-rimmed sunglasses",
       "lilac linen suit jacket stretched across his back, lilac trousers, white loafers"),
    oc("maximum_party_b",
       "a white tuxedo jacket, a black bow tie, black dress trousers, a red rose in the lapel, polished black shoes",
       "white tuxedo jacket tight across his shoulders, black dress trousers, polished black shoes"),
    oc("maximum_posing_a", "small shiny gold bodybuilding posing trunks, barefoot",
       "small shiny gold posing trunks seen from behind, barefoot"),
    oc("maximum_posing_b",
       "black square-cut swim trunks, mirrored sport sunglasses, a white towel draped over his shoulders, black slides",
       "black square-cut swim trunks, white towel over his shoulders, black slides"),
    # Yamamoto-san
    oc("yamamoto_hawaii_a",
       "a loud red Hawaiian shirt with white hibiscus flowers buttoned to the top, beige shorts pulled up high with a brown belt, white socks in brown sandals, a straw panama hat, a big camera around his neck",
       "red Hawaiian shirt with white hibiscus flowers across his back, beige shorts with a brown belt, white socks in brown sandals, straw panama hat"),
    oc("yamamoto_hawaii_b",
       "a turquoise Hawaiian shirt with yellow pineapples, open to the chest, a pink flower lei, pink swim shorts, flip-flops, sunglasses pushed up on his forehead",
       "turquoise Hawaiian shirt with yellow pineapples across his back, pink swim shorts, flip-flops"),
    oc("yamamoto_badeanzug_a",
       "a vintage 1920s red and white horizontally striped one-piece men's bathing suit with short legs and a scoop neck, a matching striped swim cap, round swim goggles pushed up on his forehead, a yellow rubber duck under his arm",
       "red and white striped vintage one-piece bathing suit from behind, short legs, striped swim cap, goggle strap at the back of his head"),
    oc("yamamoto_badeanzug_b",
       "tiny bright red speedo swim briefs, a white headband, a striped beach towel around his neck, flip-flops",
       "tiny bright red speedo swim briefs from behind, white headband knot at the back of his head, striped towel around his neck, flip-flops"),
    oc("yamamoto_leder_a",
       "a black glossy leather fetish suit covering his whole body, a black leather full-face mask with a zipper mouth and eye holes, his rimless glasses worn over the mask, black leather gloves, black leather boots",
       "black glossy leather suit covering his whole back, laces of the leather mask at the back of his head, black leather boots"),
    oc("yamamoto_leder_b",
       "a black leather harness over his bare chest, tight black leather trousers, a black leather mask covering the upper half of his face, studded wristbands, his red Hawaiian shirt tied around his waist",
       "black leather harness straps crossing his bare back, tight black leather trousers, red Hawaiian shirt knotted around his waist"),
    oc("yamamoto_business_a",
       "a charcoal three-piece business suit, a crisp white shirt, a navy silk tie, a perfectly folded white pocket square, polished black oxford shoes, a slim silver watch",
       "charcoal suit jacket from behind, matching trousers, polished black oxford shoes"),
    oc("yamamoto_business_b",
       "a navy blazer over a white shirt buttoned to the very top without a tie, grey wool trousers, black loafers, a black leather briefcase in his hand",
       "navy blazer from behind, grey wool trousers, black loafers, briefcase at his side"),
    oc("yamamoto_party_a",
       "his red Hawaiian shirt unbuttoned and sliding off one shoulder, a necktie tied around his forehead like a headband, pink swim shorts, only one flip-flop",
       "red Hawaiian shirt sliding off one shoulder, necktie knot at the back of his head, pink swim shorts, one bare foot"),
    oc("yamamoto_party_b",
       "a shiny gold sequin jacket over his bare chest, white trousers, a karaoke microphone in his hand, a flower lei",
       "shiny gold sequin jacket from behind, white trousers"),
    # Jana Maihoff
    oc("jana_deck_a",
       "a white crew polo shirt with a small golden anchor logo on the right chest tucked into navy shorts, a black belt with a walkie-talkie clipped to it, work gloves sticking out of her back pocket, white deck shoes",
       "white crew polo tucked into navy shorts, walkie-talkie on the belt at her back, work gloves in her back pocket, white deck shoes"),
    oc("jana_deck_b",
       "a navy crew polo shirt one size too big with a small golden anchor logo on the right chest, beige cargo shorts, white deck sneakers, a white sun visor, a coil of rope over one shoulder",
       "oversized navy crew polo from behind, beige cargo shorts, white deck sneakers, rope coil over one shoulder"),
    oc("jana_bikini_a", "a red-white-red striped triangle bikini, a white baseball cap worn backwards, flip-flops",
       "red-white-red striped bikini with ties at her back and hips, white cap worn backwards, flip-flops"),
    oc("jana_bikini_b", "a black sporty bikini with thin straps, a white crew polo tied around her waist, barefoot",
       "black sporty bikini with crossed straps on her back, white polo knotted around her waist, barefoot"),
    oc("jana_partydress_a",
       "a light blue summer dirndl dress with a white puff-sleeve blouse and a pink apron, the apron bow tied on her left side, white sneakers",
       "light blue dirndl dress from behind, apron strings tied at the waist, white puff-sleeve blouse, white sneakers"),
    oc("jana_partydress_b",
       "a short black slip dress borrowed from Chiara, a little too big for her, a thin gold necklace, white sneakers",
       "short black slip dress with thin crossed straps on her bare back, white sneakers"),
    oc("jana_kitty_a",
       "a skimpy black cat costume: black cat-ear headband, a black lace bralette, black high-cut panties with a long black cat tail, a black velvet collar with a small golden bell, black fingerless lace gloves, black thigh-high stockings, black heels",
       "black lace bralette straps on her bare back, long black cat tail from the high-cut panties, black thigh-high stockings, black heels, cat-ear headband"),
    oc("jana_kitty_b",
       "a skimpy white cat costume: fluffy white cat ears, a white faux-fur bandeau top, white faux-fur micro shorts with a white tail, a pink collar with a silver bell, white paw mittens, white knee socks",
       "white faux-fur bandeau and micro shorts from behind, white tail, pink collar bow at her nape, white knee socks"),
]

# ------------------------------------------------------------------ Prompts
def prompts(subject, mann):
    wer = "one single man alone in the frame, his whole body in full view" if mann else \
          "one single woman alone in the frame, her whole body in full view"
    gesicht = "Face" if mann else "Makeup"
    block = ("Subject: %s,\nBody: {tags_body},\nHair: {tags_haircolor}, {tags_hairstyle}, {tags_hair}\n"
             "Skin: {tags_skin},\n%s: {tags_face}\n" % (subject, gesicht))
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
       "disconnected hand, malformed hands, extra fingers, selfie, phones,")
BASIS_LORAS = [{"name": "Krea_Real3.safetensors", "strength": 0.7}, {"name": "Krea_Lenovo.safetensors", "strength": 0.7},
               {"name": "Krea_Redux.safetensors", "strength": 0.5}]
MODE_OPTS = {m: {"ref_mode": "face", "face_context": 2.4, "aspect": a, "width": w, "height": h,
                 "ref_boost_mode": "off", "ref_boost_value": 4}
             for m, a, w, h in (("sprite", "880x1328", 880, 1328), ("setting", "2:3", 832, 1216),
                                ("fashion", "2:3", 832, 1216), ("i2i", "880x1328", 880, 1328))}

M_MAX = ["View: Front", "M Body: Bodybuilder", "M Abs", "M Veins", "M Tall", "M Skin: Deep Brown",
         "M Hair: Bald Shine", "M Face: Clean-Shaven"]
M_YAM = ["View: Front", "M Body: Dad Bod", "M Short", "M Skin: Fair Warm", "M Hair: Side Part",
         "M Color: Black Grey Temples", "M Face: Thin Moustache", "M Glasses: Rimless"]
J_BASIS = ["View: Front", "Body: Slender", "B - Soft", "Color: Light Brown", "Blush"]

FIGUREN = {
    "Yacht_Maximum": {
        "st_name": "Maxwell Ndlovu", "mann": True,
        "subject": "Mr. Maximum, a 35-year-old South African man with dark brown eyes",
        "loras": BASIS_LORAS, "tags_on": M_MAX,
        "kost": ["Steward", "Training", "Party"],
        "sets": {"Steward": ("maximum_steward_a", M_MAX),
                 "Training": ("maximum_training_a", M_MAX + ["M Sweat"]),
                 "Party": ("maximum_party_a", M_MAX),
                 "Posing": ("maximum_posing_a", M_MAX + ["M Skin: Oiled"])}},
    "Yacht_Yamamoto": {
        "st_name": "Yamamoto-san", "mann": True,
        "subject": "Yamamoto-san, a 52-year-old Japanese banker with dark brown eyes",
        "loras": BASIS_LORAS, "tags_on": M_YAM,
        "kost": ["Hawaii", "Badeanzug", "Leder"],
        "sets": {"Hawaii": ("yamamoto_hawaii_a", M_YAM),
                 "Badeanzug": ("yamamoto_badeanzug_a", M_YAM),
                 "Leder": ("yamamoto_leder_a", M_YAM),
                 "Business": ("yamamoto_business_a", M_YAM),
                 "Party": ("yamamoto_party_a", M_YAM + ["M Flush: Drunk", "M Hair: Messed Up", "M Sweat"])}},
    "Yacht_Jana": {
        "st_name": "Jana Maihoff", "mann": False,
        "subject": "Jana Maihoff, a 21-year-old Austrian deckhand with hazel brown eyes",
        "loras": BASIS_LORAS + [{"name": "Krea_Nsfw2.safetensors", "strength": 0.7},
                                {"name": "Krea_Emma_D.safetensors", "strength": 1}],
        "tags_on": J_BASIS + ["Style: Ponytail", "Clean Girl"],
        "kost": ["Deck", "Bikini", "Party Dress", "Kitty"],
        "sets": {"Deck": ("jana_deck_a", J_BASIS + ["Style: Ponytail", "Clean Girl", "Sweat"]),
                 "Bikini": ("jana_bikini_a", J_BASIS + ["Style: Straight", "Summer", "Tan Lines"]),
                 "Party Dress": ("jana_partydress_a", J_BASIS + ["Style: Long Layered", "Instagirl Soft Glam"]),
                 "Kitty": ("jana_kitty_a", J_BASIS + ["Style: Straight", "State: Messy", "E-Girl", "Glossy Lips"])}},
}


def preset(name, f):
    sprite, base, fashion = prompts(f["subject"], f["mann"])
    k = f["kost"]
    roh = lambda kost: os.path.join(EXPR, name, kost, "roh")
    srt = lambda kost: os.path.join(EXPR, name, kost, "Sorted")
    return {
        "base_prompt": base, "sprite_prompt": sprite, "fashion_prompt": fashion,
        "negative_prompt": NEG + (" woman, female, breasts," if f["mann"] else ""),
        "loras": f["loras"], "ref_image": "", "ref_image_b": "",
        "st_set": "%s/%s/roh" % (name, k[0]),
        "save_path": r"X:\AI\ComfyUI_krea2\ComfyUI\output\studio\SET1",
        "sp_char": name, "sp_stchar": f["st_name"], "sp_k1": k[0], "sp_k2": k[1] if len(k) > 1 else "",
        "sp_aktiv": 1, "sp_kost": k,
        "sv_char": f["st_name"], "sv_set1": srt(k[0]), "sv_set2": srt(k[1]) if len(k) > 1 else "",
        "sv_sets": [srt(x) for x in k], "st_src": roh(k[0]), "st_dst": srt(k[0]),
        "mode_opts": MODE_OPTS, "tags_on": f["tags_on"],
        "cards_on": {"outfit": [f["sets"][k[0]][0]], "setting": ["A Sprite Background"], "st": ["neutral"]},
        "created": JETZT, "updated": JETZT,
    }


def main():
    cfg, decks = dc.load_json(F_CFG, None, "Studio"), dc.load_json(F_DECKS, None, "Studio")
    presets, sets = dc.load_json(F_PRESETS, None, "Studio"), dc.load_json(F_SETS, None, "Studio")
    fehler = []

    tag_namen = {t["name"] for t in cfg["tags"]}
    neue_tags = [t for t in TAGS if t["name"] not in tag_namen]
    alle_tags = tag_namen | {t["name"] for t in neue_tags}
    out_namen = {o["name"] for o in decks["outfit"]}
    neue_out = [o for o in OUTFITS if o["name"] not in out_namen]
    alle_out = out_namen | {o["name"] for o in neue_out}
    st_namen = {c.get("name") for c in decks.get("st", [])}
    set_namen = {c.get("name") for c in decks.get("setting", [])}
    if "neutral" not in st_namen:
        fehler.append("st-Karte 'neutral' fehlt")
    if "A Sprite Background" not in set_namen:
        fehler.append("Setting 'A Sprite Background' fehlt")

    neue_presets, neue_sets = {}, {}
    for name, f in FIGUREN.items():
        for t in f["tags_on"]:
            if t not in alle_tags:
                fehler.append("%s: Tag fehlt: %s" % (name, t))
        for kost, (outfit, tags) in f["sets"].items():
            if outfit not in alle_out:
                fehler.append("%s|%s: Outfit fehlt: %s" % (name, kost, outfit))
            for t in tags:
                if t not in alle_tags:
                    fehler.append("%s|%s: Tag fehlt: %s" % (name, kost, t))
            key = "%s|%s" % (name, kost)
            if key in sets:
                print("  übersprungen (gibt es schon): Set-Preset", key)
            else:
                neue_sets[key] = {"outfit": [outfit], "setting": ["A Sprite Background"], "tags": tags}
        if name in presets:
            print("  übersprungen (gibt es schon): Preset", name)
        else:
            neue_presets[name] = preset(name, f)

    print("Tags neu: %d (von %d)" % (len(neue_tags), len(TAGS)))
    print("Outfit-Karten neu: %d (von %d)" % (len(neue_out), len(OUTFITS)))
    print("Presets neu:", ", ".join(neue_presets) or "-")
    print("Set-Presets neu:", ", ".join(neue_sets) or "-")
    for name, p in neue_presets.items():
        print("\n== %s  (%s) Kostüme: %s" % (name, p["sp_stchar"], ", ".join(p["sp_kost"])))
        print("   LoRAs:", ", ".join("%s %s" % (l["name"].replace(".safetensors", ""), l["strength"]) for l in p["loras"]))
        print("   Tags:", ", ".join(p["tags_on"]))
        print("   --- sprite_prompt ---\n   " + p["sprite_prompt"].replace("\n", "\n   "))
    if fehler:
        print("\nFEHLER:\n  " + "\n  ".join(fehler))
        sys.exit(1)
    if not LOS:
        print("\nProbelauf - nichts geschrieben. Mit --los eintragen.")
        return

    stempel = time.strftime("%Y%m%d_%H%M%S")
    for pfad in (F_CFG, F_DECKS, F_PRESETS, F_SETS):
        shutil.copy2(pfad, pfad.replace(".json", ".vor-maximum-yamamoto-jana-%s.json" % stempel))
    cfg["tags"].extend(neue_tags)
    if isinstance(cfg.get("_rev"), int):
        cfg["_rev"] += 1
    decks["outfit"].extend(neue_out)
    presets.update(neue_presets)
    sets.update(neue_sets)
    dc.save_json(F_CFG, cfg, "Studio")
    dc.save_json(F_DECKS, decks, "Studio")
    dc.save_json(F_PRESETS, presets, "Studio")
    dc.save_json(F_SETS, sets, "Studio")
    print("\nEingetragen. Sicherungen: *.vor-maximum-yamamoto-jana-%s.json" % stempel)


if __name__ == "__main__":
    main()
