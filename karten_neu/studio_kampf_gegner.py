# -*- coding: utf-8 -*-
r"""Prompt Studio: Kampf-Deck (14 Karten) und 15 Gegner-Templates anlegen (19.10.2026).

    studio_kampf_gegner.py          Probelauf: zeigt, was eingetragen wuerde, schreibt nichts
    studio_kampf_gegner.py --los    traegt ein - nur bei GESCHLOSSENEM Prompt Studio (sonst schreibt ein offener
                                    Browser-Tab seinen alten Stand zurueck)

Entwurf: Y:\AI\mission-control\entwuerfe\kampf-deck-gegner.md (von Duc freigegeben). Voraussetzung: Prompt Studio
kennt das Deck "kampf" (Commit d28fc13).
- Tags: "View: Kampf" (action) + 9 Maenner-Tags (Gruppe "Maenner").
- decks.json: Deck kampf (13 x Tag kern, death mit Tag kreatur) + je Gegner eine Outfit-/Merkmal-Karte kampf_<name>.
- presets.json: Kampf_<Name> (Sprite-Prompt mit {kampf}, st_set combat/<Name>), set_presets.json: Kampf_<Name>|Kampf.
- studio-config.json: Deck kampf standardmaessig ausgeblendet (sonst kombiniert es in T2I/I2I mit allen 14 Karten).
Vorhandene Eintraege gleichen Namens werden nicht ueberschrieben. Sicherungen *.vor-kampf-<Zeit>.json.
"""
import io, os, shutil, sys, time, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, r"X:\AI\DucCommon")
import duc_common as dc  # noqa: E402

LOS = "--los" in sys.argv
PS = r"X:\AI\PromptStudio"
F_CFG, F_DECKS = os.path.join(PS, "studio-config.json"), os.path.join(PS, "decks.json")
F_PRESETS, F_SETS = os.path.join(PS, "presets.json"), os.path.join(PS, "set_presets.json")
EXPR = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions"
JETZT = time.strftime("%Y-%m-%d %H:%M")


def mt(name, cat, prompt):
    return {"name": name, "prompt": prompt, "on": False, "cat": cat, "grp": "Männer", "sec": "Body"}


TAGS = [
    {"name": "View: Kampf", "prompt": "photorealistic picture, full body, three-quarter view, the body angled to the "
     "left, looking to the left, alone in the frame", "on": False, "cat": "action", "grp": "Action",
     "sec": "General"},
    mt("M Beard: Full", "face", "a thick unkempt full beard"),
    mt("M Beard: Stubble", "face", "dark stubble"),
    mt("M Hair: Long Greasy", "hairstyle", "long greasy tangled hair"),
    mt("M Hair: Slicked Back", "hairstyle", "hair slicked back with gel"),
    mt("M Hair: Buzz Cut", "hairstyle", "a short buzz cut"),
    mt("M Scar: Face", "face", "a long scar across one cheek"),
    mt("M Tattoos: Arms", "skin", "faded tattoos covering both arms"),
    mt("M Body: Lean", "body", "a lean wiry build"),
    mt("M Tan: Deep", "skin", "deeply tanned leathery skin"),
]

KAMPF = [
    ("idle", "kern", "in a ready fighting stance, weight low, facing left, focused hostile stare"),
    ("windup", "kern", "winding up to strike, body coiled and pulled back, eyes locked to the left"),
    ("attack", "kern", "mid-attack, lunging forward to the left and striking with full force, fierce snarl"),
    ("heavy_windup", "kern", "gathering all its strength for a devastating blow, every muscle tensed, trembling with "
     "power, eyes glowing with intent"),
    ("heavy_attack", "kern", "unleashing a devastating all-out attack to the left, explosive motion, dust and spray flying"),
    ("guard", "kern", "defensive guard, braced and shielding itself, watching warily over its cover"),
    ("hurt", "kern", "hit by a heavy blow, recoiling backwards off balance, head snapped back, one hand or paw clutching its chest where it was struck, the other arm flung up, face twisted in pain, eyes squeezed shut"),
    ("enraged", "kern", "enraged and furious, bristling, baring teeth, a dark menacing aura of rage"),
    ("weakened", "kern", "exhausted and worn out, swaying on unsteady legs, panting heavily, slumped and sweaty, barely able to stand"),
    ("defeated", "kern", "knocked out cold, lying flat on its back on the ground, the whole body fully horizontal and stretched out, limp, eyes closed, alone in the frame"),
    ("surrender", "kern", "giving up, cowering low, backing away, pleading, submissive"),
    ("flee", "kern", "running away in panic, looking back over its shoulder in fear"),
    ("victory", "kern", "triumphant victory pose, gloating, chest out, looking down to the left"),
    ("death", "kreatur", "dead, lying motionless flat on its back on the ground, the whole body fully horizontal and stretched out, eyes closed, peaceful and clean, alone in the frame"),
]

# key: (Art, Subject, Tags, Merkmal/Outfit, Format)  Art: mann / frau / wesen
GEGNER = {
    "Pirate": ("mann", "a weathered pirate in his forties",
               ["M Body: Lean", "M Beard: Full", "M Hair: Long Greasy", "M Scar: Face", "M Tan: Deep", "M Tattoos: Arms"],
               "torn rags, a faded striped shirt, a red bandana, a rope belt, a rusty cutlass, barefoot", "hoch"),
    "Thief": ("mann", "a young thief", ["M Body: Lean", "M Face: Clean-Shaven"],
              "black jeans, a black hoodie with the hood up, a black face mask over nose and mouth, black-rimmed "
              "glasses, black sneakers, a crowbar", "hoch"),
    "Brute": ("mann", "a hulking dock thug", ["M Body: Bodybuilder", "M Hair: Buzz Cut", "M Beard: Stubble",
                                               "M Tattoos: Arms"],
              "a stained white tank top, grey work trousers, heavy boots, taped knuckles", "hoch"),
    "Heinrich": ("mann", "Heinrich, a sleazy German boat playboy in his fifties",
                 ["M Body: Dad Bod", "M Hair: Slicked Back", "M Tan: Deep", "M Face: Thin Moustache"],
                 "a white linen shirt open to the navel, a thick gold chain, white shorts, white loafers, mirrored "
                 "sunglasses, a champagne glass", "hoch"),
    "Agent": ("mann", "a cold corporate agent", ["M Body: Lean", "M Hair: Slicked Back", "M Face: Clean-Shaven"],
              "a black tailored suit, a white shirt, a black tie, an earpiece with a coiled wire, black sunglasses, "
              "black gloves", "hoch"),
    "Vampire": ("frau", "a beautiful female vampire", ["Pale skin", "Color: Black", "Style: Long Layered", "Goth"],
                "a long black gothic gown with a high collar, a red velvet cloak, long black nails, fangs, glowing red "
                "eyes", "hoch"),
    "Alien": ("wesen", "a grey-skinned humanoid alien with large black eyes", [],
              "a sleek white space suit with silver seams, a cracked glass helmet visor, a glowing blue chest light, "
              "a ray gun", "hoch"),
    "Lion": ("wesen", "a male lion", [], "a huge golden mane, a scarred muzzle, powerful paws", "quer"),
    "Snake": ("wesen", "a giant king cobra", [],
              "hood spread wide, olive and black scales, a forked tongue, venom dripping from its fangs", "quer"),
    "Unit1": ("wesen", "Unit-01, a ship's diesel generator come to life", [],
              "a dented steel diesel generator on mechanical legs, exhaust pipes belching black smoke, sparking "
              "cables, a red warning light as its single eye, the stencil UNIT-01 on its side", "hoch"),
    "Seagull": ("wesen", "a fat aggressive seagull", [],
                "ruffled white and grey feathers, a yellow beak with a red spot, beady eyes, a stolen french fry in "
                "its beak", "quer"),
    "Dog": ("wesen", "a big scruffy guard dog", [],
            "a muscular mixed-breed body, short brindle fur, a spiked collar, drooling jaws", "quer"),
    "Shark": ("wesen", "a great white shark", [],
              "grey back and white belly, rows of jagged teeth, scars along its flank, half out of the water, "
              "splashing", "quer"),
    "SeaMonster": ("wesen", "a sea monster from the deep", [],
                   "smooth slimy dark green skin, smooth writhing tentacles without suckers, glowing yellow eyes, dripping seaweed, rising "
                   "out of the water", "quer"),
    "Ape": ("wesen", "a large mischievous ape", [],
            "dark shaggy fur, long powerful arms, a leathery face, a stolen captain's cap on its head", "hoch"),
}

NEG = ("oversaturated, deep fried colors, anime, 3d render, three arms, extra arm, extra limb, duplicated limbs, "
       "disconnected hand, malformed hands, extra fingers, selfie, phones, text, watermark,"
       " barnacles, clustered holes, holes in skin, pores, honeycomb texture, lotus pod, coral holes, trypophobia, suction cups, suckers,"
       " blood, gore, bleeding, open wounds, two heads, extra head, duplicate head,")
NEG_ART = {"mann": " woman, female, breasts,", "frau": "", "wesen": " human, person, man, woman,"}
LORAS = [{"name": "Krea_Real3.safetensors", "strength": 0.7}, {"name": "Krea_Lenovo.safetensors", "strength": 0.7},
         {"name": "Krea_Redux.safetensors", "strength": 0.5}]
FORMAT = {"hoch": ("880x1328", 880, 1328), "quer": ("1328x880", 1328, 880)}
KOPF = "{tags_action}, Shot on an iPhone, grainy amateur photo, realistic smartphone photography, full body shot, "


def prompts(art, subject):
    if art == "wesen":
        wer = "one single creature alone in the frame, its whole body in full view"
        block = "Subject: %s,\nFeatures: {outfit},\n" % subject
    else:
        wer = ("one single man alone in the frame, his whole body in full view" if art == "mann" else
               "one single woman alone in the frame, her whole body in full view")
        block = ("Subject: %s,\nBody: {tags_body},\nHair: {tags_haircolor}, {tags_hairstyle}, {tags_hair}\n"
                 "Skin: {tags_skin},\n%s: {tags_face}\nWearing: {outfit},\n"
                 % (subject, "Face" if art == "mann" else "Makeup"))
    sprite = KOPF + wer + ",\n" + block + "Scene: {setting},\n{kampf},\n{tags_photo}"
    base = KOPF + wer + ",\n" + block + "Scene: {setting}\n{kampf}\n{tags_photo}"
    fashion = ("{tags_action}, full body shot, standing in full view, beige plain background,\n" + block
               + "{kampf},\n{tags_photo}")
    return sprite, base, fashion


def preset(name, art, subject, tags, fmt):
    sprite, base, fashion = prompts(art, subject)
    a, w, h = FORMAT[fmt]
    mo = {m: {"ref_mode": "face", "face_context": 2.4, "aspect": a, "width": w, "height": h,
              "ref_boost_mode": "off", "ref_boost_value": 4} for m in ("sprite", "fashion", "i2i")}
    mo["setting"] = dict(mo["sprite"], aspect="2:3", width=832, height=1216)
    p = "Kampf_" + name
    return {
        "base_prompt": base, "sprite_prompt": sprite, "fashion_prompt": fashion,
        "negative_prompt": NEG + NEG_ART[art], "loras": LORAS, "ref_image": "", "ref_image_b": "",
        "st_set": "combat/%s" % name, "save_path": r"X:\AI\ComfyUI_krea2\ComfyUI\output\studio\SET1",
        "sp_char": p, "sp_stchar": name, "sp_k1": "Kampf", "sp_k2": "", "sp_aktiv": 1, "sp_kost": ["Kampf"],
        "sv_char": "", "sv_set1": "", "sv_set2": "", "sv_sets": [],
        "st_src": os.path.join(EXPR, "combat", name), "st_dst": os.path.join(EXPR, "combat", name),
        "mode_opts": mo, "tags_on": ["View: Kampf"] + tags,
        "cards_on": {"outfit": ["kampf_" + name.lower()], "setting": ["A Sprite Background"]},
        "created": JETZT, "updated": JETZT,
    }


def studio_laeuft():
    try:
        urllib.request.urlopen("http://127.0.0.1:8301/", timeout=2)
        return True
    except OSError:
        return False


def main():
    cfg, decks = dc.load_json(F_CFG, None, "Studio"), dc.load_json(F_DECKS, None, "Studio")
    presets, sets = dc.load_json(F_PRESETS, None, "Studio"), dc.load_json(F_SETS, None, "Studio")
    fehler = []
    tag_namen = {t["name"] for t in cfg["tags"]}
    neue_tags = [t for t in TAGS if t["name"] not in tag_namen]
    alle_tags = tag_namen | {t["name"] for t in neue_tags}
    kampf_alt = {c["name"] for c in decks.get("kampf", [])}
    neue_kampf = [{"name": n, "prompt": p, "on": True, "tag": t, "sel": False} for n, t, p in KAMPF if n not in kampf_alt]
    out_namen = {o["name"] for o in decks["outfit"]}
    neue_out, neue_presets, neue_sets = [], {}, {}
    if "A Sprite Background" not in {c.get("name") for c in decks.get("setting", [])}:
        fehler.append("Setting 'A Sprite Background' fehlt")
    for name, (art, subject, tags, merkmal, fmt) in GEGNER.items():
        karte = "kampf_" + name.lower()
        if karte not in out_namen:
            neue_out.append({"name": karte, "prompt": merkmal, "on": True, "tag": "kampf", "sel": False,
                             "back_prompt": ""})
        for t in tags:
            if t not in alle_tags:
                fehler.append("%s: Tag fehlt: %s" % (name, t))
        p = "Kampf_" + name
        if p in presets:
            print("  übersprungen (gibt es schon): Preset", p)
        else:
            neue_presets[p] = preset(name, art, subject, tags, fmt)
        if p + "|Kampf" not in sets:
            neue_sets[p + "|Kampf"] = {"outfit": [karte], "setting": ["A Sprite Background"],
                                       "tags": ["View: Kampf"] + tags}
    print("Tags neu: %d · Kampf-Karten neu: %d · Merkmal-Karten neu: %d · Presets neu: %d · Set-Presets neu: %d"
          % (len(neue_tags), len(neue_kampf), len(neue_out), len(neue_presets), len(neue_sets)))
    for n in ("Kampf_Pirate", "Kampf_Vampire", "Kampf_Lion"):
        if n in neue_presets:
            print("\n== %s (%s)\n   %s" % (n, neue_presets[n]["mode_opts"]["sprite"]["aspect"],
                                         neue_presets[n]["sprite_prompt"].replace("\n", "\n   ")))
    if fehler:
        print("\nFEHLER:\n  " + "\n  ".join(fehler))
        sys.exit(1)
    if not LOS:
        print("\nProbelauf - nichts geschrieben. Mit --los eintragen (Prompt Studio vorher schliessen).")
        return
    if studio_laeuft():
        sys.exit("Prompt Studio laeuft - bitte erst schliessen, dann noch einmal mit --los.")
    stempel = time.strftime("%Y%m%d_%H%M%S")
    for pfad in (F_CFG, F_DECKS, F_PRESETS, F_SETS):
        shutil.copy2(pfad, pfad.replace(".json", ".vor-kampf-%s.json" % stempel))
    cfg["tags"].extend(neue_tags)
    cfg.setdefault("decks_visible", {}).setdefault("kampf", False)
    decks.setdefault("kampf", []).extend(neue_kampf)
    decks["outfit"].extend(neue_out)
    presets.update(neue_presets)
    sets.update(neue_sets)
    dc.save_json(F_CFG, cfg, "Studio")
    dc.save_json(F_DECKS, decks, "Studio")
    dc.save_json(F_PRESETS, presets, "Studio")
    dc.save_json(F_SETS, sets, "Studio")
    print("\nEingetragen. Sicherungen: *.vor-kampf-%s.json" % stempel)


if __name__ == "__main__":
    main()
