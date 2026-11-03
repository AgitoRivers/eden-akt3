# -*- coding: utf-8 -*-
r"""Volle Kampf-Saetze BoardingRobot (Wahl n2) und BoardingRobotHeavy (h2, rote Lackierung statt gelb, Duc 01.11.2026).

    boarding_robot_satz.py [--nur normal:hurt,schwer:guard]   -> output\expressions\_boarding_robot_satz\<normal|schwer>\<pose>.png

Laeuft ueber studio.build_graph, die Studio-Einstellungen bleiben unberuehrt. Nichts wird ins Spiel kopiert.
"""
import json, os, sys, time, urllib.request

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, r"X:\AI\PromptStudio")
import casting_boarding_robot as cb  # noqa: E402
import casting_piraten_neu as cp  # noqa: E402

ORDNER = "_boarding_robot_satz"
SEED = cp.SEEDS[0]
ROT = cb.FIGUR["h2"].replace("solid bright yellow warning stripes painted on the shoulders and the chest", "solid deep red warning stripes painted on the shoulders and the chest, no yellow anywhere")
assert ROT != cb.FIGUR["h2"]
FIGUR = {"normal": cb.FIGUR["n2"], "schwer": ROT}
ZWEI = "exactly two arms and two clamp hands"
FERN = "the camera far back, the whole machine and both feet completely inside the image with wide empty floor below them"
RUHIG = "no glow around the body, no fire, no sparks, no motion streaks"
POSEN = {
    "windup": ("%s, winding up a punch, its right arm pulled far back behind the body, the upper body twisted, weight on the back leg, facing left, %s, %s" % (ZWEI, FERN, RUHIG), 1232, 1232),
    "attack": ("%s, punching forward to the left with full force, its right arm fully stretched straight out to the left with the big clamp hand closed, a long step forward, %s, %s" % (ZWEI, FERN, RUHIG), 1232, 1232),
    "heavy_windup": ("%s, both arms raised high above the head block with the clamp hands together, the whole body coiled, facing left, %s, %s" % (ZWEI, FERN, RUHIG), 1232, 1232),
    "heavy_attack": ("%s, slamming both clamp hands together down and forward to the left in a deep lunge, both arms fully stretched, facing left, %s, %s" % (ZWEI, FERN, RUHIG), 1232, 1232),
    "guard": ("%s, in a defensive stance, both thick forearms raised and crossed in front of the head block and chest as a shield, body pulled back and low, facing left, %s, %s" % (ZWEI, FERN, RUHIG), 1232, 1232),
    "hurt": ("%s, hit by a heavy blow, tilted backwards off balance, the head block knocked to one side, one arm flung out, one foot lifted, facing left, %s, %s" % (ZWEI, FERN, RUHIG), 1232, 1232),
    "enraged": ("%s, leaning forward aggressively, both arms spread wide with the clamp hands open, the red light burning bright, facing left, %s, no fire, no sparks, no motion streaks" % (ZWEI, FERN), 1232, 1232),
    "weakened": ("%s, damaged and sagging, the upper body slumped forward, both arms hanging heavy, the red light dim, both legs straight, facing left, %s, %s" % (ZWEI, FERN, RUHIG), 1232, 1232),
    "defeated": ("seen from the side at floor level, the machine has fallen and lies flat on its back on the floor, its body perfectly horizontal and level, arms limp at its sides, its one head block on the RIGHT side of the image, the red light off; exactly one machine with one head, the whole machine fully inside the image with empty space around, %s" % RUHIG, 1328, 880),
    "surrender": ("the machine has sunk down on both knees and raises both open clamp hands above its head block, head bowed, the floor around it is completely clean and empty, %s, %s" % (FERN, RUHIG), 1104, 1408),
    "flee": ("walking away fast in a clumsy heavy run, its body turned away and its head block looking back over its shoulder, facing left, %s, %s" % (FERN, RUHIG), 1232, 1232),
    "victory": ("%s, standing tall with both arms raised high in triumph and both clamp hands closed, chest out, facing left, %s, %s" % (ZWEI, FERN, RUHIG), 1232, 1232),
}


def prompt(name, haltung):
    return "%s,\nSubject: %s,\nFeatures: %s,\nScene: Plain beige background,\n%s." % (cb.KOPF, FIGUR[name], cb.GLATT, haltung)


def main():
    import studio
    nur = sys.argv[sys.argv.index("--nur") + 1].split(",") if "--nur" in sys.argv else None
    with urllib.request.urlopen(cp.PS + "/api/state", timeout=30) as f:
        cfg = dict(json.loads(f.read())["cfg"])
    wart = []
    for name in FIGUR:
        for pose, (haltung, b, h) in dict(POSEN, idle=(cb.STAND, 1232, 1232)).items():
            if nur and "%s:%s" % (name, pose) not in nur:
                continue
            c = dict(cfg, loras=cp.LORAS, mode="sprite", sprite_src="t2i", width=b, height=h, negative_prompt="", st_set="%s/%s" % (ORDNER, name), st_rembg=True, st_crop=True, **cp.MODELL)
            wart.append(cp.post(cp.COMFY + "/prompt", {"prompt": studio.build_graph(c, prompt(name, haltung), pose, SEED)})["prompt_id"])
    print("eingereiht", len(wart), flush=True)
    fehler, ende = 0, time.time() + 1500
    while wart and time.time() < ende:
        time.sleep(3)
        for i in list(wart):
            with urllib.request.urlopen(cp.COMFY + "/history/" + i, timeout=30) as f:
                r = json.loads(f.read()).get(i)
            if r:
                fehler += r.get("status", {}).get("status_str") != "success"
                wart.remove(i)
    print("offen", len(wart), "fehler", fehler)


if __name__ == "__main__":
    main()
