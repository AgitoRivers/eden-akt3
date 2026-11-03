# -*- coding: utf-8 -*-
r"""Mina Orsoni als Tag-Preset (Duc 30.10.2026: "in Prompt Studio so gut es geht mit Tags").

Basis ist die gewaehlte Fassung Mina_A1. Koerper, Haar, Haut und Make-up kommen aus den Studio-Tags wie bei den Heldinnen,
im Subject-Satz steht nur noch, was kein Tag ausdruecken kann. Kein Gesichts-LoRA, sie ist nicht romanzierbar.

    casting_mina_tags.py            Probelauf
    casting_mina_tags.py --los      Preset Yacht_Mina anlegen, 3 Testbilder -> expressions\_casting_dorf\Yacht_Mina
"""
import os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, r"X:\AI\DucCommon")
LOS = "--los" in sys.argv
sys.argv = [sys.argv[0]] + (["--los"] if LOS else [])
import castings_danzel as cd  # noqa: E402
_HALTEN = [sys.stdout]         # das Modul wickelt stdout neu ein; ohne Referenz schliesst der alte Wrapper den Puffer

PRESET = "Yacht_Mina"
ORDNER = "_casting_dorf"
KARTE = "mina_A"
TAGS = ["View: Front", "Body: Slender", "Body: Long Legs", "B - Soft", "Color: dark brown", "Style: Bob", "State: Messy",
        "Skin: Olive Tan", "Freckles", "Summer"]
LORAS = [{"name": "Krea_Real3.safetensors", "strength": 0.7}, {"name": "Krea_Lenovo.safetensors", "strength": 0.7},
         {"name": "Krea_Redux.safetensors", "strength": 0.5}]
SEEDS = [240611, 771203, 90817]
PROMPT = ("{tags_action}, Shot on an iPhone, grainy amateur photo, realistic smartphone photography, full body shot from "
          "head to knees, direct gaze, one single woman alone in the frame, her whole body in full view, head and knees "
          "inside the frame,\n"
          "Subject: Mina Orsoni, a 24-year-old adult woman, a Corsican courier with deeply sun-tanned skin, a cheeky wide "
          "grin, bright dark eyes, a real individual face with slight natural asymmetry,\n"
          "Body: {tags_body},\n"
          "Hair: {tags_haircolor}, {tags_hairstyle}, {tags_hair}\n"
          "Skin: {tags_skin},\n"
          "Makeup: {tags_face}\n"
          "Wearing: {outfit},\n"
          "Scene: {setting}, {st},\n{expression},\nLook: {look},\n{tags_photo}")


def main():
    print("Tags:", ", ".join(TAGS))
    if not LOS:
        print("Probelauf - nichts geschrieben. Mit --los anlegen und 3 Testbilder rendern.")
        return
    st = cd.ps("/api/state")
    fehlt = sorted(set(TAGS) - {t["name"] for t in st["cfg"]["tags"]})
    if fehlt:
        sys.exit("Tags fehlen im Studio: %s" % fehlt)
    presets = cd.dc.load_json(cd.F_PRESETS, None, "Studio")
    presets[PRESET] = {"sprite_prompt": PROMPT, "loras": LORAS, "ref_image": "", "ref_image_b": "", "negative_prompt": "",
                       "tags_on": TAGS, "sp_stchar": "Mina Orsoni",
                       "cards_on": {"outfit": [KARTE], "setting": ["A Sprite Background"], "st": [cd.POSE]},
                       "st_set": "%s/%s" % (ORDNER, PRESET), "created": cd.JETZT, "updated": cd.JETZT}
    cd.dc.save_json(cd.F_PRESETS, presets, "Studio")
    alt = {k: st["cfg"].get(k) for k in ("sprite_prompt", "loras", "st_set", "sprite_src", "tags", "unet", "clip", "seed")}
    alt_preset = st["cfg"].get("preset_active")
    n = 0
    try:
        cd.ps("/api/presets", {"action": "load", "name": PRESET})
        cfg = cd.ps("/api/state")["cfg"]
        for t in cfg["tags"]:
            t["on"] = t["name"] in TAGS
        for s in SEEDS:
            cd.ps("/api/config", dict(cd.MODELL, tags=cfg["tags"], mode="sprite", sprite_src="t2i", combine_mode="all",
                                      view_pro_karte=False, st_rembg=True, st_crop=True, seed=s,
                                      st_set="%s/%s" % (ORDNER, PRESET), loras=LORAS, sprite_prompt=PROMPT))
            dk = cd.ps("/api/state")["decks"]
            for kk in dk:
                wahl = {"outfit": {KARTE}, "setting": {"A Sprite Background"}, "st": {cd.POSE}}.get(kk, set())
                for x in dk[kk]:
                    x["sel"] = x["name"] in wahl
            n += cd.ps("/api/queue", {"cfg": {"combine_mode": "all"}, "decks": dk}).get("queued", 0)
    finally:
        if alt_preset:
            cd.ps("/api/presets", {"action": "load", "name": alt_preset})
        cd.ps("/api/config", {k: v for k, v in alt.items() if v is not None})
    print("%d Testbilder in der Warteschlange -> expressions\\%s\\%s" % (n, ORDNER, PRESET))


if __name__ == "__main__":
    main()
