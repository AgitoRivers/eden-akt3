# -*- coding: utf-8 -*-
r"""Kampf-Sprites Captain Bonaventure (Duc 01.11.2026): 13 Posen mit Entermesser, schaut nach links wie alle Gegner. Der Humor steckt in den Posen, der Koerper bleibt echt. Nichts wird ins Spiel kopiert.

    kampf_bonaventure.py [--nur idle,defeated]   -> output\expressions\combat\Bonaventure\<pose>.png
"""
import json, os, sys, time, urllib.request

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, r"X:\AI\PromptStudio")
import casting_bonaventure_2 as cb  # noqa: E402

SEED = int(sys.argv[sys.argv.index("--seed") + 1]) if "--seed" in sys.argv else cb.SEEDS[0]
SAEBEL = "the single broad curved cutlass gripped in his right fist"
LEER = "his left hand empty"
FERN = ", the camera far back, the whole figure, the hat and both boots inside the image with empty space around"
POSEN = {
    "idle": "in a ready duelling stance, facing left, chest out, chin high, %s pointing forward to the left, %s and resting on his hip, a proud smile" % (SAEBEL, LEER),
    "guard": "standing in a dramatic defensive stance, facing left, his right arm bent, the one curved cutlass held upright in front of his chest with its point up and its single blade above his fist, ready to block, his empty left hand behind his back, the scabbard empty and hanging behind his left leg",
    "windup": "swinging back for a grand theatrical strike, facing left, %s raised behind his shoulder, %s stretched forward, eyes locked to the left" % (SAEBEL, LEER),
    "attack": "lunging forward to the left in a long stage fencing lunge, %s fully extended, the blade pointing straight to the left, the tip furthest from his body, %s thrown back behind him" % (SAEBEL, LEER),
    "heavy_windup": "raising the cutlass high above his head with one arm like a hero on a poster, facing left, head thrown back, shouting to the sky, %s on his chest" % LEER,
    "heavy_attack": "bringing the cutlass down in a huge overhead chop to the left, deep lunge, his coat flying behind him, slight motion blur on the blade, %s" % LEER,
    "hurt": "hit by a heavy blow, recoiling backwards, his hat knocked crooked, one hand clutching his chest as if on a stage, mouth open in outrage, %s" % SAEBEL,
    "enraged": "furious and shouting at the sky, moustache bristling, leaning forward, shaking his raised empty left fist, %s" % SAEBEL,
    "weakened": "exhausted, swaying, panting, leaning on the cutlass like a walking stick with its point on the floor, still holding his chin high",
    "surrender": "down on both knees with both open empty hands raised, chin still held high as if he were the one accepting a surrender, the cutlass lying flat on the floor beside him",
    "flee": "running away to the left in panic, looking back over his shoulder, holding his hat on his head with his left hand, %s, coat flying" % SAEBEL,
    "victory": "triumphant pose, one boot forward, chest out, %s raised straight up above his head, %s on his hip, a huge delighted grin, singing" % (SAEBEL, LEER),
    "defeated": "one single man lying flat on his back on a plain beige floor, seen from the side and from far away, his body perfectly horizontal, one arm flung out like a tragic stage hero and the other on his chest, eyes closed, his one hat still crooked on his head and nothing on his chest, both hands empty, the head and both boots completely inside the image with wide empty floor to the left and to the right of him",
}
QUER = {"defeated"}


def prompt(pose):
    p = cb.prompt("c").replace("front view, direct gaze", "three-quarter view, the body angled to the left, looking to the left")
    return p.split("He stands square")[0] + POSEN[pose] + (FERN if pose not in QUER else "") + ". He is completely serious about all of this."


def main():
    import studio
    nur = sys.argv[sys.argv.index("--nur") + 1].split(",") if "--nur" in sys.argv else None
    with urllib.request.urlopen(cb.PS + "/api/state", timeout=30) as f:
        cfg = dict(json.loads(f.read())["cfg"])
    wart = []
    for pose in POSEN:
        if nur and pose not in nur:
            continue
        b, h = (1328, 880) if pose in QUER else (1232, 1232)
        c = dict(cfg, loras=cb.LORAS, mode="sprite", sprite_src="t2i", width=b, height=h, negative_prompt="", st_set=sys.argv[sys.argv.index("--set") + 1] if "--set" in sys.argv else "combat/Bonaventure", st_rembg=True, st_crop=True, **cb.MODELL)
        wart.append(cb.post(cb.COMFY + "/prompt", {"prompt": studio.build_graph(c, prompt(pose), pose, SEED)})["prompt_id"])
    print("eingereiht", len(wart), flush=True)
    fehler, ende = 0, time.time() + 280
    while wart and time.time() < ende:
        time.sleep(3)
        for i in list(wart):
            with urllib.request.urlopen(cb.COMFY + "/history/" + i, timeout=30) as f:
                r = json.loads(f.read()).get(i)
            if r:
                fehler += r.get("status", {}).get("status_str") != "success"
                wart.remove(i)
    print("offen", len(wart), "fehler", fehler)


if __name__ == "__main__":
    main()
