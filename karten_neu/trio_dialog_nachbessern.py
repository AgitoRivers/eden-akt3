# -*- coding: utf-8 -*-
r"""Dialog-Sprites Bibi und Charly nachbessern (Duc 30.10.2026, QA): Charlys Rueckansichten hatten schwarze Hosen, weil
back_prompt der Karte charly_A keine Farbe nannte; Bibis Rueckansichten waren frontal (Sprite-Prompt "frontal view, direct
gaze"), eine davon offen; abgeschnittene Haende und Ausschnitt-Reste. Alte Bilder -> output\_expressions_papierkorb.

    trio_dialog_nachbessern.py          Probelauf
    trio_dialog_nachbessern.py --los
"""
import json, os, shutil, sys, time, urllib.request

PS = "http://127.0.0.1:8301"
OUT = r"X:\AI\ComfyUI_krea2\ComfyUI\output"
KORB = os.path.join(OUT, "_expressions_papierkorb", "trio_dialog_" + time.strftime("%H%M"))
LOS = "--los" in sys.argv
# Figur: (Outfit-Karte, Rueckansichten, Haende/Reste)
LISTE = {          # Runde 2: Charlys Hosen stimmen, offen sind nur noch diese
    "Yacht_Charly": ("charly_A", [], ["caring", "joy_2", "optimism_2"]),
    "Yacht_Bibi": ("bibi_A", ["curiosity_back", "embarrassment_back", "nervousness_back"], ["caring", "joy_2", "optimism_2", "nervousness"]),
}
BIBI_BACK = ("Red blazer back showing shoulder seams and upper back, sleeves rolled up, black blouse visible below the blazer hem, black "
             "utility belt, she is fully dressed in her red shorts, the red shorts fully cover her whole seat and hips, black combat "
             "boots below, red fingerless gloves on both hands")
# Weite Armposen laufen aus dem Bild: nur fuer diesen Lauf naeher am Koerper
TEXTE = {
    "caring": "She takes a small step forward with one knee bent, both hands held out in front of her waist close to her body, palms open. "
              "Soft empathetic face, gentle reassuring smile, warm relaxed eyes, brows slightly tilted up.",
    "joy_2": "bouncing on her toes with both fists pressed up beside her cheeks, elbows close to her body, her clothes caught mid-motion. "
             "Unrestrained joyful laugh, eyes crinkled shut, mouth wide open in delight.",
    "optimism_2": "She stands on tiptoes with both hands clasped under her chin, elbows close to her body, chest lifted, head tilted upward "
                  "toward the horizon. Hopeful bright-eyed face, wide easy smile, brows lifted with anticipation.",
    "curiosity_back": "She stands with her back and the seat of her red shorts facing the camera, leaning forward up on her toes, hands "
                      "clasped behind her, tilting her head around over her shoulder. Keenly interested face, eyebrows lifted, a small intrigued smile.",
}
CHARLY_BACK = ("Red cropped blazer back with visible shoulder seams, the same red straight suit trousers as the blazer fitting smoothly "
               "over buttocks and thighs, black flat shoes, headset band across the back of neck with microphone wire visible, "
               "taser holster clipped at lower back.")
RAND = "both hands and both arms completely inside the image with wide empty space on every side, "
ZU = ["frontal perspective, ", "frontal view, ", "direct gaze, "]


def ps(p, d=None):
    q = urllib.request.Request(PS + p, data=None if d is None else json.dumps(d).encode(), headers={"Content-Type": "application/json", "X-Tab": "skript"})
    return json.loads(urllib.request.urlopen(q, timeout=300).read())


def lauf(preset, outfit, karten, back):
    ps("/api/presets", {"action": "load", "name": preset})
    cfg = ps("/api/state")["cfg"]
    an = {t["name"] for t in cfg["tags"] if t["on"]} - {"View: Front", "View: Back"}
    an.add("View: Back" if back else "View: Front")
    for t in cfg["tags"]:
        t["on"] = t["name"] in an
    sp = cfg["sprite_prompt"]
    if back:
        for z in ZU:
            sp = sp.replace(z, "")
        sp = sp.replace("full body shot", "seen from behind, her back to the camera, full body shot", 1)
    else:
        sp = sp.replace("full body shot from head to knees, ", "full body shot from head to knees, " + RAND, 1)
    ps("/api/config", {"tags": cfg["tags"], "mode": "sprite", "sprite_src": "t2i", "combine_mode": "all", "view_pro_karte": False, "st_rembg": True,
                       "st_crop": True, "seed": int(time.time()) % 900000, "st_set": "%s/Standard/roh" % preset, "sprite_prompt": sp})
    d = ps("/api/state")["decks"]
    for k in d:
        w = {"outfit": {outfit}, "setting": {"A Sprite Background"}, "st": set(karten)}.get(k, set())
        for x in d[k]:
            x["sel"] = x["name"] in w
    return ps("/api/queue", {"cfg": {"combine_mode": "all"}, "decks": d}).get("queued", 0)


def main():
    for p, (o, b, h) in LISTE.items():
        print(p, o, "Rueck:", b, "Rest:", h)
    if not LOS:
        print("Probelauf")
        return
    st = ps("/api/state")
    alt = st["cfg"].get("preset_active")
    d = st["decks"]
    for c in d["outfit"]:
        if c["name"] == "charly_A":
            c["back_prompt"] = CHARLY_BACK
        if c["name"] == "bibi_A":
            c["back_prompt"] = BIBI_BACK
    orig = {c["name"]: c["prompt"] for c in d["st"] if c["name"] in TEXTE}
    for c in d["st"]:
        if c["name"] in TEXTE:
            c["prompt"] = TEXTE[c["name"]]
    ps("/api/decks", d)
    os.makedirs(KORB, exist_ok=True)
    try:
        for p, (o, b, h) in LISTE.items():
            roh = os.path.join(OUT, "expressions", p, "Standard", "roh")
            for k in b + h:
                f = os.path.join(roh, k + ".png")
                if os.path.exists(f):
                    shutil.move(f, os.path.join(KORB, "%s_%s.png" % (p, k)))
            print(p, "Rueck", lauf(p, o, b, True) if b else 0, "Rest", lauf(p, o, h, False))
    finally:
        d = ps("/api/state")["decks"]
        for c in d["st"]:
            if c["name"] in orig:
                c["prompt"] = orig[c["name"]]
        ps("/api/decks", d)
        if alt:
            ps("/api/presets", {"action": "load", "name": alt})
    print("Alte Bilder:", KORB)


if __name__ == "__main__":
    main()
