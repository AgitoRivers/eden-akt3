# -*- coding: utf-8 -*-
r"""NPC-Satz Alon im Keynote-Look (Duc 02.11.2026, Abnahme alon_keynote: Rollkragen mit Gesicht „Falke“, Seed 1). 22 Posen, nur Front,
ohne desire_2 (nicht romanzierbar). Nichts wird ins Spiel kopiert, das macht alon_einbau.py nach Ducs Abnahme.

    alon_satz.py [--nur neutral,joy]   -> output\expressions\_alon_satz\<pose>.png
"""
import json, re, sys, time, urllib.request

sys.path.insert(0, r"X:\AI\Eden\karten_neu")
sys.path.insert(0, r"X:\AI\PromptStudio")
import alon_keynote_casting as K  # noqa: E402
import alon_gesicht as G  # noqa: E402

ORDNER = "_alon_satz"
SEED = K.SEEDS[0]                     # Falke 1
NPC = ["neutral", "caring", "joy", "sadness", "anger", "fear_2", "surprise", "disgust", "amusement", "annoyance", "confusion",
       "curiosity", "pride", "approval", "gratitude", "nervousness", "disapproval", "disappointment", "excitement_2",
       "embarrassment_2", "admiration_2", "love_2"]
HOCH = {"love_2", "admiration_2"}
GRUND = ("%s,\nSubject: %s, %s,\nWearing: %s,\nScene: Plain beige background, the camera further back, his whole body from the top of the head down "
         "to the soles of BOTH shoes inside the image, wide empty floor below his feet,\n" % (K.KOPF, G.GESICHTER["falke"], G.KOERPER, G.ANZUG))
EIGEN = {"neutral": "He stands relaxed and upright, both arms loose at his sides, a calm, friendly, confident face.",
         # Keynote: Stolz ist seine Praesentations-Geste aus dem Casting
         "pride": K.HALTUNG + ", chin up, very pleased with himself.",
         "disappointment": "He stands with sagging shoulders, arms hanging at his sides, both legs straight. A flat, cool face, mouth pulled down at the corners.",
         # 02.11. erster Lauf: hockte bei Angst und Trauer, Beine ueberkreuzt bei Aerger und Verlegenheit
         "fear_2": "He stands upright with both feet flat on the floor, legs straight, leaning back a little, both hands raised in front of his chest with open palms. Wide frightened eyes, mouth open.",
         "sadness": "He stands upright with sagging shoulders, both feet flat on the floor, legs straight, arms hanging at his sides. Sad eyes looking down, mouth turned down.",
         "annoyance": "He stands with both feet flat on the floor, shoulder-width apart, legs straight, arms folded across his chest. A small irritated frown, mouth pressed shut.",
         "embarrassment_2": "He stands with both feet flat on the floor, legs straight, one hand rubbing the back of his neck, an awkward, sheepish smile, eyes looking away.",
         "disgust": "He stands upright with both feet flat on the floor, legs straight, leaning his head back, one hand raised palm out as if to keep something away. Nose wrinkled, lip curled.",
         "nervousness": "He stands upright with both feet flat on the floor, legs straight, rubbing his hands together in front of his chest, a tight, too-wide smile, eyes darting to the side.",
         "amusement": "He stands upright with both feet flat on the floor, shoulder-width apart, legs straight, one hand on his stomach, laughing with his head tipped back a little.",
         "love_2": "Standing head to feet with both arms open at hip height, palms toward the viewer, shoulders relaxed. A warm, practised smile."}


def mann(t):
    return re.sub(r"\bherself\b", "himself", re.sub(r"\bher\b", "his", re.sub(r"\bShe\b", "He", re.sub(r"\bshe\b", "he", t))))


def main():
    import studio
    nur = sys.argv[sys.argv.index("--nur") + 1].split(",") if "--nur" in sys.argv else None
    with urllib.request.urlopen(K.PS + "/api/state", timeout=30) as f:
        st = json.loads(f.read())
    cfg = dict(st["cfg"])
    karten = {c["name"]: c["prompt"] for c in st["decks"]["st"]}
    wart = []
    for pose in NPC:
        if nur and pose not in nur:
            continue
        p = GRUND + mann(EIGEN.get(pose) or karten[pose]) + "."
        b, h = (1104, 1408) if pose in HOCH else (880, 1328)
        c = dict(cfg, loras=K.LORAS, mode="sprite", sprite_src="t2i", width=b, height=h, negative_prompt="", st_set=ORDNER,
                 st_rembg=True, st_crop=True)
        wart.append(K.post(K.COMFY + "/prompt", {"prompt": studio.build_graph(c, p, pose, SEED)})["prompt_id"])
    print("eingereiht", len(wart), flush=True)
    fehler, ende = 0, time.time() + 1500
    while wart and time.time() < ende:
        time.sleep(3)
        for i in list(wart):
            with urllib.request.urlopen(K.COMFY + "/history/" + i, timeout=30) as f:
                r = json.loads(f.read()).get(i)
            if r:
                fehler += r.get("status", {}).get("status_str") != "success"
                wart.remove(i)
    print("offen", len(wart), "fehler", fehler)


if __name__ == "__main__":
    main()
