# -*- coding: utf-8 -*-
r"""Prompt-Studio-Presets fuer Bibi und Charly (Duc 29.10.2026, Abnahme Red Trio: Bibi C1, Charly A1).

Wie Yacht_Ligeia: Haar, Koerper, Haut und Makeup kommen als Tags, der Subject-Satz traegt nur Gesicht und Charakter.
Fehlende Tags (geflochtene Zoepfe, blond mit rosa Spitzen, Bob mit Pony) werden in Prompt Studio angelegt.
Das aktive Preset bleibt unveraendert; die beiden Presets nur speichern, Duc feilt selbst.

    presets_bibi_charly.py          Probelauf
    presets_bibi_charly.py --los    Tags + Presets Yacht_Bibi, Yacht_Charly anlegen
"""
import io, json, sys, time, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, r"X:\AI\DucCommon")
import duc_common as dc  # noqa: E402

PS = "http://127.0.0.1:8301"
F_PRESETS = r"X:\AI\PromptStudio\presets.json"
JETZT = time.strftime("%Y-%m-%d %H:%M")
LOS = "--los" in sys.argv
LORAS = [{"name": "Krea_Real3.safetensors", "strength": 0.7}, {"name": "Krea_Lenovo.safetensors", "strength": 0.7},
         {"name": "Krea_Redux.safetensors", "strength": 0.5}]
HAUT = "natural skin texture with visible pores, slight natural asymmetry in the face, a real individual face"

# neue Tags: (Name, cat, Prompt, Vorbild fuer grp/sec)
NEUE_TAGS = [
    ("Style: Braided Pigtails", "hairstyle", "two long braided pigtails hanging over her shoulders", "Style: Double Braids"),
    ("Color: Blonde Pink Tips", "haircolor", "her hair is bleached blonde with the ends dyed bubblegum pink", "Color: blonde"),
    ("Style: Bob Bangs", "hairstyle", "a perfectly straight chin-length bob with blunt bangs", "Style: Bob"),
]

SPRITE = ("{tags_action}, Shot on an iPhone, grainy amateur photo, realistic smartphone photography, full body shot "
          "from head to knees, direct gaze, one single woman alone in the frame, her whole body in full view, head and "
          "knees inside the frame,\nSubject: %s, " + HAUT + ",\nBody: {tags_body},\nHair: {tags_haircolor}, "
          "{tags_hairstyle}, {tags_hair}\nSkin: {tags_skin},\nMakeup: {tags_face}\nWearing: {outfit},\n"
          "Scene: {setting}, {st},\n{expression},\nLook: {look},\n{tags_photo}")

PRESETS = {
    "Yacht_Bibi": {
        "name": "Bibi", "karte": "bibi_C",
        "subject": "Bibi, a 26-year-old French woman, a red agent of A.V. Estates who badly wants to be a real villain, "
                   "a sharp pretty face with a tiny scar on her chin, warm brown eyes, a gleeful dramatic villain smile",
        "tags": ["View: Front", "Color: Blonde Pink Tips", "Style: Braided Pigtails", "Body: Athletic", "Winged Liner"]},
    "Yacht_Charly": {
        "name": "Charly", "karte": "charly_A",
        "subject": "Charly, a 26-year-old French woman, a red agent of A.V. Estates and the dry, sleepy brain of the trio, "
                   "a calm heart-shaped face, sleepy half-closed grey eyes, a completely deadpan expression, tall",
        "tags": ["View: Front", "Color: Black", "Style: Bob Bangs", "Body: Slender", "Clean Girl"]},
}


def ps(pfad, daten=None):
    req = urllib.request.Request(PS + pfad, data=None if daten is None else json.dumps(daten).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def main():
    for pn, p in PRESETS.items():
        print("%-13s Outfit %-9s Tags: %s" % (pn, p["karte"], ", ".join(p["tags"])))
    if not LOS:
        print("Probelauf - nichts geschrieben. Mit --los anlegen.")
        return
    tags = ps("/api/state")["cfg"]["tags"]
    da = {t["name"]: t for t in tags}
    for name, cat, prompt, vorbild in NEUE_TAGS:
        if name in da:
            da[name]["prompt"] = prompt
        else:
            v = da[vorbild]
            tags.append({"name": name, "prompt": prompt, "on": False, "cat": cat, "grp": v.get("grp"), "sec": v.get("sec")})
    ps("/api/config", {"tags": tags})
    presets = dc.load_json(F_PRESETS, None, "Studio")
    for pn, p in PRESETS.items():
        alt = presets.get(pn, {})
        presets[pn] = dict(alt, sprite_prompt=SPRITE % p["subject"], loras=LORAS, ref_image="", ref_image_b="",
                           negative_prompt="", tags_on=sorted(p["tags"]), sp_char=pn, sp_stchar=p["name"],
                           sp_k1="Standard", sp_kost=["Standard"], st_set="%s/Standard/roh" % pn,
                           cards_on={"outfit": [p["karte"]], "setting": ["A Sprite Background"], "st": ["neutral"]},
                           created=alt.get("created", JETZT), updated=JETZT)
    dc.save_json(F_PRESETS, presets, "Studio")
    print("Tags + Presets angelegt: %s" % ", ".join(PRESETS))


if __name__ == "__main__":
    main()
