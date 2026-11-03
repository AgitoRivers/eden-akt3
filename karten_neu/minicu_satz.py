# -*- coding: utf-8 -*-
r"""NPC-Satz Minicu (Duc 01.11.2026, Wahl 1b auf docs/abnahme/minicu_casting.json): 22 Posen, nur Front, ohne desire_2. Nichts wird ins Spiel kopiert.

    minicu_satz.py [--nur neutral,joy] [--seed N]   -> output\expressions\_minicu_satz\<pose>.png

Laeuft ueber studio.build_graph, die Studio-Einstellungen bleiben unberuehrt.
"""
import json, os, re, sys, time, urllib.request

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, r"X:\AI\PromptStudio")
import casting_minicu as cm  # noqa: E402

OUT = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions"
ORDNER = "_minicu_satz"
SEED = cm.SEEDS[1]
# NPC-Satz wie karten_neu/dorf_sets.py, ohne desire_2 (nicht romanzierbar)
NPC = ["neutral", "caring", "joy", "sadness", "anger", "fear_2", "surprise", "disgust", "amusement", "annoyance", "confusion",
       "curiosity", "pride", "approval", "gratitude", "nervousness", "disapproval", "disappointment", "excitement_2",
       "embarrassment_2", "admiration_2", "love_2"]
HOCH = {"love_2", "admiration_2"}
EIGEN = {"disappointment": "He stands with sagging shoulders, arms hanging at his sides, both legs straight. Flat deflated face, dull eyes, mouth pulled down at the corners.",
         # 01.11.: bei der Karte standen die Beine ueberkreuzt, das wirkt fuer ihn zu laessig
         "annoyance": "He stands with both feet flat on the floor, shoulder-width apart, legs straight, both big arms folded across his chest. A small grumpy frown, mouth pressed shut, looking a little to one side.",
         "surprise": "He stands with both feet flat on the floor, shoulder-width apart, legs straight, both big hands raised beside his face with open palms. Eyes wide, eyebrows high, mouth open in a round O.",
         "love_2": "Standing head to feet with both arms open at hip height, palms toward the viewer, shoulders relaxed. Warm affectionate smile."}


def mann(t):
    return re.sub(r"\bherself\b", "himself", re.sub(r"\bher\b", "his", re.sub(r"\bShe\b", "He", t)))


def dialog(text):
    return cm.prompt("1").split("He stands square")[0] + mann(text)


def main():
    import studio
    nur = sys.argv[sys.argv.index("--nur") + 1].split(",") if "--nur" in sys.argv else None
    seed = int(sys.argv[sys.argv.index("--seed") + 1]) if "--seed" in sys.argv else SEED
    with urllib.request.urlopen(cm.PS + "/api/state", timeout=30) as f:
        st = json.loads(f.read())
    cfg = dict(st["cfg"])
    karten = {c["name"]: c["prompt"] for c in st["decks"]["st"]}
    wart = []
    for pose in NPC:
        if nur and pose not in nur:
            continue
        p = cm.prompt("1") if pose == "neutral" else dialog(EIGEN.get(pose) or karten[pose])
        b, h = (1104, 1408) if pose in HOCH else (880, 1328)
        c = dict(cfg, loras=cm.LORAS, mode="sprite", sprite_src="t2i", width=b, height=h, negative_prompt="", st_set=ORDNER, st_rembg=True, st_crop=True, **cm.MODELL)
        wart.append(cm.post(cm.COMFY + "/prompt", {"prompt": studio.build_graph(c, p, pose, seed)})["prompt_id"])
    print("eingereiht", len(wart), flush=True)
    fehler, ende = 0, time.time() + 560
    while wart and time.time() < ende:
        time.sleep(3)
        for i in list(wart):
            with urllib.request.urlopen(cm.COMFY + "/history/" + i, timeout=30) as f:
                r = json.loads(f.read()).get(i)
            if r:
                fehler += r.get("status", {}).get("status_str") != "success"
                wart.remove(i)
    print("offen", len(wart), "fehler", fehler)


if __name__ == "__main__":
    main()
