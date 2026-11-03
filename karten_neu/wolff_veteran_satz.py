# -*- coding: utf-8 -*-
r"""Voller Satz Wolff "Der Veteran" (Duc 01.11.2026, Wahl d3 + k3 auf docs/abnahme/wolff_veteran.json). Gleiches Modell und gleicher Seed wie die Wahl.

    wolff_veteran_satz.py [--nur neutral,idle] [--neu TEXT]   -> output\expressions\_wolff_veteran_satz\<dialog|kampf>\<pose>.png

Laeuft ueber studio.build_graph, die Studio-Einstellungen bleiben unberuehrt. Nichts wird ins Spiel kopiert.
"""
import json, os, re, sys, time, urllib.request

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, r"X:\AI\PromptStudio")
import casting_wolff_veteran as cv  # noqa: E402
import kampf_volllauf_texte as kt  # noqa: E402

ORDNER = "_wolff_veteran_satz"
SEED = cv.SEEDS[0]
NPC = ["neutral", "caring", "joy", "sadness", "anger", "fear_2", "surprise", "disgust", "amusement", "annoyance", "confusion",
       "curiosity", "pride", "approval", "gratitude", "nervousness", "disapproval", "disappointment", "excitement_2",
       "embarrassment_2", "admiration_2", "love_2"]
HOCH = {"admiration_2", "love_2"}
EIGEN = {"disappointment": "He stands with sagging shoulders, arms hanging at his sides, both legs straight. Flat deflated face, dull eye, mouth pulled down at the corners.",
         "fear_2": "He crouches with both knees bent and his hands raised defensively in front of his chest, shoulders hunched tight, the camera far back, both boots completely inside the image with empty floor below them. Terrified face, wide eye, mouth trembling open, brows shot high.",
         "admiration_2": "He stands with one hand raised to his cheek in amazement and the other resting on his hip, head tilted to one side, head to feet. Impressed admiring look, lips parted.",
         "love_2": "Standing head to feet with both arms open at hip height, palms toward the viewer, shoulders relaxed. Warm affectionate smile."}
K_SCHWERT = "his only weapon exactly one long straight steel sword gripped in his right fist, the whole sword inside the image"
K_BEIDE = "his only weapon exactly one long straight steel sword gripped with both hands, the whole sword inside the image"
K_LEER = "both hands empty, a worn black scabbard at his left hip"
K_WINDUP = "his only weapon exactly one long straight steel sword raised in his right fist behind his head, his left hand an empty open hand stretched forward, the whole sword inside the image"
LIEGT = ("seen from the side at floor level, he lies stretched out flat on his back, resting on the floor, his body perfectly horizontal and level, his back, hips, legs and heels all touching the floor, arms limp at his sides, knocked out, his one head with the beret on the RIGHT side of the image, eye closed; "
         "exactly one man with one head, the whole man fully inside the image with empty space around")
WUT = "furious and shouting with his mouth wide open and his teeth bared, leaning forward, the tendons in his neck tense, the sword thrust forward, the camera far back, the whole sword and both boots completely inside the image with wide empty floor below them"
GUARD = "taking a defensive stance, body pulled back and low, the sword held across his body to block an attack from the left, the camera far back, both boots completely inside the image with empty floor below them"
# Pose: (Text oder None = Karte, Waffe, Breite, Hoehe)
KAMPF = {"idle": (None, cv.VARIANTEN["3"][4], 880, 1328), "windup": (kt.T["windup"], K_WINDUP, 1232, 1232), "attack": (kt.T["attack"], K_SCHWERT, 1232, 1232),
         "heavy_windup": (kt.T["heavy_windup"], K_BEIDE, 1232, 1232), "heavy_attack": (kt.T["heavy_attack"], K_BEIDE, 1232, 1232), "guard": (GUARD, K_SCHWERT, 1232, 1232),
         "hurt": (None, K_SCHWERT, 1104, 1408), "enraged": (WUT, K_SCHWERT, 1232, 1232),
         "weakened": ("exhausted and worn out, swaying on unsteady legs, panting heavily, barely able to stand", K_SCHWERT, 880, 1328),
         "defeated": (LIEGT, K_LEER, 1328, 880), "surrender": (None, K_LEER, 880, 1328), "flee": (None, K_SCHWERT, 880, 1328), "victory": (None, K_SCHWERT, 1104, 1408)}


def mann(t):
    return re.sub(r"\bherself\b", "himself", re.sub(r"\bher\b", "his", re.sub(r"\bShe\b", "He", t)))


def dialog(v, text):
    return cv.dialog(v).split("He stands square")[0] + mann(text)


def kampf(v, pose, karte):
    text, waffe, _, _ = KAMPF[pose]
    voll = cv.kampf(v).replace(cv.VARIANTEN[v][4], waffe)
    if pose == "idle":
        return voll
    return voll.replace("in a ready fighting stance, weight low, facing left, focused hostile stare, the whole sword inside the image.", (text or karte) + ".")


def main():
    import studio
    nur = sys.argv[sys.argv.index("--nur") + 1].split(",") if "--nur" in sys.argv else None
    neu = sys.argv[sys.argv.index("--neu") + 1] if "--neu" in sys.argv else ""
    with urllib.request.urlopen(cv.PS + "/api/state", timeout=30) as f:
        st = json.loads(f.read())
    cfg, st_k, k_k = dict(st["cfg"]), {c["name"]: c["prompt"] for c in st["decks"]["st"]}, {c["name"]: c["prompt"] for c in st["decks"]["kampf"]}
    wart = []
    for pose in NPC:
        if nur and pose not in nur:
            continue
        p = cv.dialog("3") if pose == "neutral" else dialog("3", EIGEN.get(pose) or st_k[pose])
        b, h = (1104, 1408) if pose in HOCH else (880, 1328)
        c = dict(cfg, loras=cv.LORAS, mode="sprite", sprite_src="t2i", width=b, height=h, negative_prompt="", st_set=ORDNER + "/dialog", st_rembg=True, st_crop=True, **cv.MODELL)
        wart.append(cv.post(cv.COMFY + "/prompt", {"prompt": studio.build_graph(c, p + neu, pose, SEED)})["prompt_id"])
    for pose, (_, _, b, h) in KAMPF.items():
        if nur and pose not in nur:
            continue
        c = dict(cfg, loras=cv.LORAS, mode="sprite", sprite_src="t2i", width=b, height=h, negative_prompt="", st_set=ORDNER + "/kampf", st_rembg=True, st_crop=True, **cv.MODELL)
        wart.append(cv.post(cv.COMFY + "/prompt", {"prompt": studio.build_graph(c, kampf("3", pose, k_k.get(pose, "")) + neu, pose, SEED)})["prompt_id"])
    print("eingereiht", len(wart), flush=True)
    fehler, ende = 0, time.time() + 1200
    while wart and time.time() < ende:
        time.sleep(3)
        for i in list(wart):
            with urllib.request.urlopen(cv.COMFY + "/history/" + i, timeout=30) as f:
                h = json.loads(f.read()).get(i)
            if h:
                fehler += h.get("status", {}).get("status_str") != "success"
                wart.remove(i)
    print("offen", len(wart), "fehler", fehler)
    for w, _, dat in os.walk(os.path.join(cv.OUT, ORDNER)):
        print(w, len(dat), sorted(dat))


if __name__ == "__main__":
    main()
