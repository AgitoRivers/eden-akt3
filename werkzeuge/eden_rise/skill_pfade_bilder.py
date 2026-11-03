# -*- coding: utf-8 -*-
r"""Mood strips for the five skill paths (Duc 27.10.2026: Krea scenes instead of the effect-lab materials).

    python skill_pfade_bilder.py 3            3 variants per path (skill_pfade_bilder.py 3 LM 4: more for L and M) -> docs\abnahme\skill_pfade\<P>_v1..3.png + approval spec
    python skill_pfade_bilder.py --waehle K 2 variant 2 of Fighter -> client\plugins\eden-skills\paths\K.png (1200 px wide)

Very wide 2048x640 (Krea2 needs 1-2 MP, divisible by 16): the rows of the skill tree are flat strips. The subject sits in
the right half, the left stays calm and dark (path name and the first skills sit there). BigLove + Real3 like the scene
backgrounds (hintergrund_bild.py)."""
import json, os, random, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import item_bilder as ib

EDEN = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VAR = os.path.join(EDEN, "docs", "abnahme", "skill_pfade")
SPEC = os.path.join(EDEN, "docs", "abnahme", "skill_pfade.json")
ZIEL = os.path.join(EDEN, "client", "plugins", "eden-skills", "paths")
RAHMEN = ("Ultra-wide cinematic panorama photograph. The left half of the frame is calm, dark and nearly empty, fading "
          "into deep shadow; the subject sits in the right half. Moody low-key light, rich colour, photorealistic, "
          "no people, no animals, no text")
MOTIVE = {
    "K": ("Fighter · Wind & Water",
          "Huge waves breaking against dark granite rocks on the wild coast of Corsica, white spray thrown high into "
          "the air, a stormy blue-grey sky with torn clouds, wind streaking foam across the turquoise sea"),
    "L": ("Smuggler · Cunning & Precision",
          "A hidden smugglers' hideout in a rough rock cave under an old harbour town, heavy iron-bound wooden treasure "
          "chests and barrels stacked against the damp stone walls, a worn rug and a small wooden table with a map and "
          "candles, dark water of an underground canal glinting at the side. Mysterious purple light glows from a "
          "crack deep in the cave and tints the rock violet, mixed with the warm amber of a few oil lanterns"),
    "W": ("Marksman · Focus & Control",
          "A white stone lighthouse on a rocky Corsican headland at blue hour, its bright beam sweeping in a long clean "
          "straight line across the calm sea, a clear deep teal sky with the first stars, a thin line of sunset glow on "
          "the horizon"),
    "M": ("Berserker · Embers & Release",
          "A dark volcano erupting in the far background at night, glowing rivers of red lava running down its slope, "
          "fountains of orange lava sparks and glowing embers flying high into the black smoky sky, a dark rocky "
          "plain of cooled black lava in the foreground lit red from above, deep orange and crimson tones"),
    "H": ("Healer · Herbs & Grace",
          "The quiet herb garden of an old Corsican stone monastery at dawn, soft golden rays of morning light falling "
          "through a gnarled olive tree, beds of yellow immortelle flowers, rosemary and lavender with dew, a weathered "
          "stone wall and an arched cloister in soft haze, gentle green and gold tones"),
}
NEGATIV = "people, person, man, woman, hands, animals, text, watermark, logo, blurry, cartoon, anime, 3d render"


def erzeugen(n, pfade=None, ab=1):
    """pfade: only these paths (e.g. "LM"); ab: first variant number - new variants are added to the approval spec."""
    os.makedirs(VAR, exist_ok=True)
    ib.NEGATIV = NEGATIV
    ib.NSFW_PROFIL["loras"] = [("Krea_Real3.safetensors", 0.7)]          # scenery: realism yes, no NSFW LoRA
    auftraege = []
    neu = [(p, k) for p in (pfade or MOTIVE) for k in range(ab, ab + n)]
    for p, k in neu:
        g = ib.graph(MOTIVE[p][1] + ". " + RAHMEN, VAR, "%s_v%d" % (p, k), random.randint(1, 2 ** 31), True)
        g["6"]["inputs"].update({"width": 2048, "height": 640})
        auftraege.append(("%s_v%d" % (p, k), ib.post("/prompt", {"prompt": g})["prompt_id"]))
    alt = json.load(open(SPEC, encoding="utf-8"))["items"] if ab > 1 and os.path.isfile(SPEC) else []
    spec = {"id": "skill_pfade", "titel": "Skill Tree · Stimmungsbilder je Pfad",
            "hinweis": "Je Pfad eine Variante OK geben (die anderen Neu oder leer). Das Bild läuft blass hinter der Reihe, "
                       "links ausgeblendet: wichtig ist die Stimmung rechts.",
            "items": alt + [{"id": "%s_v%d" % (p, k), "titel": "%s · Variante %d" % (MOTIVE[p][0], k),
                             "bild": os.path.join(VAR, "%s_v%d.png" % (p, k)), "soll": MOTIVE[p][1]} for p, k in neu]}
    with open(SPEC, "w", encoding="utf-8") as f:
        json.dump(spec, f, ensure_ascii=False, indent=1)
    ib.warten(auftraege, lambda v: print("fertig:", v))
    print("Varianten in", VAR)


def waehlen(p, k):
    from PIL import Image
    os.makedirs(ZIEL, exist_ok=True)
    im = Image.open(os.path.join(VAR, "%s_v%s.png" % (p, k))).convert("RGB")
    im = im.resize((1200, round(1200 * im.height / im.width)), Image.LANCZOS)
    im.save(os.path.join(ZIEL, p + ".png"), optimize=True)
    print("uebernommen: %s Variante %s" % (p, k))


if __name__ == "__main__":
    if sys.argv[1] == "--waehle":
        waehlen(sys.argv[2], sys.argv[3])
    else:                                      # skill_pfade_bilder.py 3 [LM 4]  -> L_v4..6, M_v4..6
        erzeugen(int(sys.argv[1]), sys.argv[2] if len(sys.argv) > 2 else None, int(sys.argv[3]) if len(sys.argv) > 3 else 1)
