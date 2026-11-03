# -*- coding: utf-8 -*-
r"""Casting leichter flinker Roboter (Duc 01.11.2026): 10 freie Varianten. Gleiche Baureihe wie BoardingRobot (Graphit, rotes Licht), nur glatte Platten.

    casting_robot_flink.py   -> output\expressions\_casting_robot_flink\<f01..f10>\idle.png
"""
import json, os, sys, time, urllib.request

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, r"X:\AI\PromptStudio")
import casting_boarding_robot as cb  # noqa: E402
import casting_piraten_neu as cp  # noqa: E402

ORDNER = "_casting_robot_flink"
LICHT = "one single round glowing red light as its face"
FARBE = "dark graphite steel plates with a few thin white painted edges"
FIGUR = {
    "f01": ("Strauss", "a tall slim running robot on two long thin backward-bending legs like an ostrich, a small narrow torso, a long thin neck, %s, one slim blade fixed to each short arm, %s" % (LICHT, FARBE), "leaning far forward in a sprint start, one foot lifted"),
    "f02": ("Windhund", "a sleek four-legged robot shaped like a greyhound, a long narrow chest, long thin legs, a small wedge-shaped head with %s, %s" % (LICHT, FARBE), "crouched low and ready to spring forward"),
    "f03": ("Spinne", "a small low robot with a round flat body and six long thin curved legs like a harvestman spider, %s in the middle of the body, %s" % (LICHT, FARBE), "the body held high on the legs, two front legs raised"),
    "f04": ("Einrad", "a slim robot balancing on one single large thin wheel, a narrow upright torso leaning forward, two long thin arms with one small blade each, a small head with %s, %s" % (LICHT, FARBE), "leaning forward at speed, arms swept back"),
    "f05": ("Fechter", "a slender humanoid robot as thin as a fencer, narrow waist, long thin arms and legs, a small oval head with %s, one long thin rapier arm instead of a right hand, %s" % (LICHT, FARBE), "in a low fencing lunge stance with the rapier arm pointing to the left"),
    "f06": ("Schlange", "a low snake-like robot made of a long chain of smooth rounded segments, raised in an S-curve like a cobra, a wedge-shaped head with %s, two small blades folded at the neck, %s" % (LICHT, FARBE), "the front raised high and ready to strike to the left"),
    "f07": ("Heuschrecke", "a small light robot shaped like a grasshopper, a slim body, two huge folded jumping legs, two small front arms with hooks, a small head with %s, %s" % (LICHT, FARBE), "crouched on its folded legs, about to jump"),
    "f08": ("Ninja", "a small slim child-sized humanoid robot, smooth round joints, a pointed narrow head with %s, a short thin blade in each hand, a thin red strip of cloth tied around its neck and streaming behind it, %s" % (LICHT, FARBE), "crouched low on the balls of its feet, both blades ready"),
    "f09": ("Skorpion", "a small light robot shaped like a scorpion, a flat narrow body on six thin legs, two small pincers, a long curved segmented tail with one blade raised over its back, %s on the front of the body, %s" % (LICHT, FARBE), "low to the ground, tail raised, pincers forward"),
    "f10": ("Schwebe", "a slim robot with no legs, hovering just above the floor on a small round smooth base with a soft shadow below it, a narrow torso, two long thin blade arms, a small flat head with %s, %s" % (LICHT, FARBE), "hovering forward and leaning to the left, blade arms spread"),
}


def prompt(key):
    _, wer, stand = FIGUR[key]
    return "%s,\nSubject: %s,\nFeatures: %s,\nScene: Plain beige background,\n%s, facing left, no glow around the body, no fire, no sparks, no motion streaks." % (cb.KOPF, wer, cb.GLATT, stand)


def main():
    import studio
    with urllib.request.urlopen(cp.PS + "/api/state", timeout=30) as f:
        cfg = dict(json.loads(f.read())["cfg"])
    wart = []
    for key in FIGUR:
        c = dict(cfg, loras=cp.LORAS, mode="sprite", sprite_src="t2i", width=1232, height=1232, negative_prompt="", st_set="%s/%s" % (ORDNER, key), st_rembg=True, st_crop=False, **cp.MODELL)
        wart.append(cp.post(cp.COMFY + "/prompt", {"prompt": studio.build_graph(c, prompt(key), "idle", cp.SEEDS[0])})["prompt_id"])
    print("eingereiht", len(wart), flush=True)
    ende = time.time() + 400
    while wart and time.time() < ende:
        time.sleep(3)
        for i in list(wart):
            with urllib.request.urlopen(cp.COMFY + "/history/" + i, timeout=30) as f:
                if json.loads(f.read()).get(i):
                    wart.remove(i)
    print("offen", len(wart))
    from PIL import Image, ImageDraw
    b = Image.new("RGB", (5 * 420, 2 * 420), (226, 204, 176))
    for i, key in enumerate(FIGUR):
        p = os.path.join(cp.OUT, ORDNER, key, "idle.png")
        if os.path.isfile(p):
            q = Image.open(p).convert("RGBA").resize((420, 420))
            b.paste(q, (i % 5 * 420, i // 5 * 420), q)
        ImageDraw.Draw(b).text((i % 5 * 420 + 6, i // 5 * 420 + 6), key + " " + FIGUR[key][0], fill=(200, 0, 0))
    b.save(r"C:\Users\DucNg\AppData\Local\Temp\claude\C--Users-DucNg\32bd1786-2635-4dfe-bf70-e4ff6a4f89ba\scratchpad\flink.png")


if __name__ == "__main__":
    main()
