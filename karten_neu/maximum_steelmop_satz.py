# -*- coding: utf-8 -*-
r"""Voller Satz Mr. Maximum mit Steel Mop (Duc 01.11.2026, Wahl d3 + Schulter auf docs/abnahme/maximum_steelmop_3.json). Eigener Satz, die alten bleiben.

    maximum_steelmop_satz.py [--nur neutral,idle] [--seed N]   -> output\expressions\_maximum_steelmop_satz\<dialog|kampf>\<pose>.png

Dialog ohne Waffe. Laeuft ueber studio.build_graph, die Studio-Einstellungen bleiben unberuehrt. Nichts wird ins Spiel kopiert.
"""
import json, os, re, sys, time, urllib.request

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, r"X:\AI\PromptStudio")
import casting_maximum_steelmop as cm  # noqa: E402
import casting_maximum_wuerfel as cw  # noqa: E402
import kampf_volllauf_texte as kt  # noqa: E402

ORDNER = "_maximum_steelmop_satz"
SEED = cm.SEEDS[1]                 # d3 neutral-1 und schulter idle-1
OHNE = {"submissive", "worshipful"}   # wie die alten Sets: nur Front, ohne diese Karten
HOCH = {"love", "admiration"}
EIGEN = {"disappointment": "He stands with sagging shoulders, arms hanging at his sides, both legs straight. Flat deflated face, dull eyes, mouth pulled down at the corners.",
         "love": "Standing head to feet with both arms open at hip height, palms toward the viewer, shoulders relaxed. Warm affectionate smile."}
FERN = " The camera is far back, both shoes completely inside the image with empty floor below them."      # Runde 2: Schuhe abgeschnitten
EIGEN["embarrassment"] = "He stands with one hand rubbing the back of his neck and the other arm hanging at his side, shoulders hunched up. Flustered embarrassed smile, eyes glancing away."
ZU = ", the pipe ends inside the cube and nothing comes out of the other side of the cube, the wreath of bristles only around the pipe, all faces of the cube closed, plain and smooth"     # Runde 2: Stummel und Loch am Wuerfel
# Runde 3 (Duc: der Kranz muss immer unter dem Hammer sein): Waffe von der Seite, feste Reihenfolge entlang des Rohrs
WAFFE = ("a giant hammer seen exactly from the side in profile, the steel head never pointing at the camera. Along the weapon in this exact order: the rounded handle end of a long straight dark steel pipe, his hands on the pipe, "
         "then a fluffy white ball-shaped wreath of scrubbing bristles around the pipe, then directly after it one huge solid closed cube of smooth dark steel at the very end of the pipe. "
         "The wreath is always between his hands and the cube, under the hammer head, narrower than the cube, and the far side of the cube is plain, with nothing behind it")
BEIDE = "gripping the pipe with both hands"
RECHTS = "gripping the pipe in his right fist, his left hand an empty fist"
LEER = "both hands empty, no weapon anywhere"
LIEGT = ("seen from the side at floor level, he lies stretched out flat on his back, resting on the floor, his body perfectly horizontal and level, arms limp at his sides, knocked out, "
         "his one head on the RIGHT side of the image, eyes closed; exactly one man with one head, the whole man fully inside the image with empty space around")
# Pose: (Haltung, Griff, mit Waffe, Breite, Hoehe)
KAMPF = {"idle": (cw.HALTUNG["schulter"], "", True, 1232, 1232),
         "windup": (kt.T["windup"], BEIDE, True, 1232, 1232), "attack": ("swinging the hammer forward to the left with full force in a long lunging step, the steel cube far out on the LEFT side of the image in front of him, the handle end of the pipe on the right near his hip, fierce snarl", BEIDE, True, 1232, 1232),
         "heavy_windup": (kt.T["heavy_windup"], BEIDE, True, 1232, 1232), "heavy_attack": (kt.T["heavy_attack"], BEIDE, True, 1232, 1232),
         "guard": ("taking a defensive stance, body pulled back and low, the pipe held across the front of his body with both hands to block an attack from the left, the camera far back, both shoes completely inside the image", "", True, 1232, 1232),
         "hurt": ("hit by a heavy blow, recoiling backwards off balance, head snapped back, face twisted in pain, eyes squeezed shut", RECHTS, True, 1232, 1232),
         "enraged": ("furious and shouting with his mouth wide open and his teeth bared, leaning forward, the tendons in his neck tense, the camera far back, both shoes completely inside the image", BEIDE, True, 1232, 1232),
         "weakened": ("exhausted and worn out, swaying on unsteady legs, panting heavily, barely able to stand, the steel cube resting on the floor in front of him", RECHTS, True, 1232, 1232),
         "defeated": (LIEGT, LEER, False, 1328, 880),
         "surrender": ("he drops to both knees and raises both open hands above his head, head bowed in defeat; the floor around him is completely clean and empty", LEER, False, 1104, 1408),
         "flee": ("running away in panic, looking back over his shoulder in fear, the camera far back, both shoes inside the image", RECHTS, True, 1232, 1232),
         "victory": ("triumphant victory pose, gloating, chest out, the weapon raised high above his head in his right fist, his head and the whole weapon inside the image", "", True, 1232, 1408)}


def mann(t):
    return re.sub(r"\bherself\b", "himself", re.sub(r"\bher\b", "his", re.sub(r"\bShe\b", "He", t)))


def dialog(text):
    return cm.dialog("3").split("He stands square")[0] + mann(text)


def kampf(pose):
    haltung, griff, waffe, _, _ = KAMPF[pose]
    teile = [haltung] + ([griff] if griff else []) + (["his only weapon " + WAFFE, "the whole weapon inside the image"] if waffe else [])
    p = cm.kampf("3")
    return p[:p.index("in a ready fighting stance")] + ", ".join(teile) + "."


def main():
    import studio
    nur = sys.argv[sys.argv.index("--nur") + 1].split(",") if "--nur" in sys.argv else None
    seed = int(sys.argv[sys.argv.index("--seed") + 1]) if "--seed" in sys.argv else SEED
    with urllib.request.urlopen(cm.PS + "/api/state", timeout=30) as f:
        st = json.loads(f.read())
    cfg = dict(st["cfg"])
    karten = {c["name"]: c["prompt"] for c in st["decks"]["st"]}
    posen = [p for p in cfg["sfw_posen"] if p not in OHNE and not p.endswith("_back")]
    wart = []
    for pose in posen:
        if nur and pose not in nur:
            continue
        p = cm.dialog("3") if pose == "neutral" else dialog(EIGEN.get(pose) or karten[pose] + (FERN if pose in ("joy", "remorse") else ""))
        b, h = (1104, 1408) if pose in HOCH else (880, 1328)
        c = dict(cfg, loras=cm.LORAS, mode="sprite", sprite_src="t2i", width=b, height=h, negative_prompt="", st_set=ORDNER + "/dialog", st_rembg=True, st_crop=True, **cm.MODELL)
        wart.append(cm.post(cm.COMFY + "/prompt", {"prompt": studio.build_graph(c, p, pose, seed)})["prompt_id"])
    for pose, (_, _, _, b, h) in KAMPF.items():
        if nur and pose not in nur:
            continue
        c = dict(cfg, loras=cm.LORAS, mode="sprite", sprite_src="t2i", width=b, height=h, negative_prompt="", st_set=ORDNER + "/kampf", st_rembg=True, st_crop=True, **cm.MODELL)
        wart.append(cm.post(cm.COMFY + "/prompt", {"prompt": studio.build_graph(c, kampf(pose), pose, seed)})["prompt_id"])
    print("eingereiht", len(wart), flush=True)
    fehler, ende = 0, time.time() + 1500
    while wart and time.time() < ende:
        time.sleep(3)
        for i in list(wart):
            with urllib.request.urlopen(cm.COMFY + "/history/" + i, timeout=30) as f:
                r = json.loads(f.read()).get(i)
            if r:
                fehler += r.get("status", {}).get("status_str") != "success"
                wart.remove(i)
    print("offen", len(wart), "fehler", fehler)
    for w, _, dat in os.walk(os.path.join(cm.OUT, ORDNER)):
        print(w, len(dat))


if __name__ == "__main__":
    main()
