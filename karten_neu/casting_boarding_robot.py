# -*- coding: utf-8 -*-
r"""Casting Boarding Robots (Duc 01.11.2026): BoardingRobot nach Ducs Karten-Blatt und BoardingRobotHeavy als staerkere Stufe. Je 3 Varianten, je 2 Seeds.
Nur glatte, massive Panzerplatten (Ducs Trypophobie), darum sind die Flaechen im Prompt ausdruecklich beschrieben.

    casting_boarding_robot.py   -> output\expressions\_casting_boarding_robot_2\<n1..n3|h1..h3>\idle(-1).png
"""
import json, os, sys, time, urllib.request

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, r"X:\AI\PromptStudio")
import casting_piraten_neu as cp  # noqa: E402

ORDNER = "_casting_boarding_robot_2"
KOPF = ("photorealistic picture, full body, three-quarter view, the body angled to the left, looking to the left, alone in the frame, Shot on an iPhone, grainy amateur photo, realistic smartphone photography, "
        "full body shot, one single machine alone in the frame, its whole body in full view, the camera far back, both feet completely inside the image")
GLATT = ("every surface is one seamless smooth solid armour plate with clean bevelled corners, each plate plain and closed and completely uniform, a real heavy industrial machine of painted steel, solid and opaque and sharply in focus")
GESICHT = "very stocky squat proportions like a heavy toy: the torso is as wide as it is tall and takes up most of the body, the legs are very short thick stumps no longer than a third of the torso, the arms are short and thick and end at the hips, no visible thin joints or cables, a small head block sunk into the shoulders with one single round glowing red light as its face"
STAND = "standing firm with its legs apart and its big clamp hands hanging at its sides, ready to attack, facing left"
FIGUR = {
    "n1": "a short wide walking robot with a boxy dark graphite steel torso, thick angular shoulder blocks, short stubby legs and big blocky clamp hands, %s, a few thin white painted edges along the plates" % GESICHT,
    "n2": "a short squat walking robot with a broad rounded dark graphite steel torso with softly rounded corners, thick rounded shoulder blocks, short stubby legs and big clamp hands, %s, thin white painted edges along the chest plate" % GESICHT,
    "n3": "a short wide walking robot with a boxy glossy dark graphite steel torso with a shiny polished finish, thick angular shoulder blocks, very short stubby legs and huge blocky clamp hands, %s, a few bright white edges along the plates" % GESICHT,
    "h1": "a huge massive walking robot of the same series as a short boarding robot but much bigger and bulkier, a giant boxy dark graphite steel torso, double-thick armour plates, enormous angular shoulder blocks, thick legs, giant clamp hands, %s, bright yellow warning edges along the shoulders and the chest" % GESICHT,
    "h2": "a huge massive walking robot, a giant wide dark graphite steel torso like a safe, very thick layered armour plates, enormous shoulder blocks that rise above the head, thick short legs, giant clamp hands, %s, solid bright yellow warning stripes painted on the shoulders and the chest" % GESICHT,
    "h3": "a huge top-heavy walking robot, an enormous dark graphite steel chest much wider than its hips, very thick armour plates, gigantic shoulder blocks, heavy legs, oversized clamp hands, %s, wide bright yellow painted edges along the shoulders and the chest plate" % GESICHT,
}


def prompt(key, stand=STAND):
    return "%s,\nSubject: %s,\nFeatures: %s,\nScene: Plain beige background,\n%s." % (KOPF, FIGUR[key], GLATT, stand)


def main():
    import studio
    with urllib.request.urlopen(cp.PS + "/api/state", timeout=30) as f:
        cfg = dict(json.loads(f.read())["cfg"])
    wart = []
    for key in FIGUR:
        c = dict(cfg, loras=cp.LORAS, mode="sprite", sprite_src="t2i", width=1232, height=1232, negative_prompt="", st_set="%s/%s" % (ORDNER, key), st_rembg=True, st_crop=False, **cp.MODELL)
        for s in cp.SEEDS:
            wart.append(cp.post(cp.COMFY + "/prompt", {"prompt": studio.build_graph(c, prompt(key), "idle", s)})["prompt_id"])
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
    b = Image.new("RGB", (6 * 400, 2 * 400), (226, 204, 176))
    for y, art in enumerate("nh"):
        i = 0
        for v in "123":
            for n in ("idle", "idle-1"):
                q = Image.open(os.path.join(cp.OUT, ORDNER, art + v, n + ".png")).convert("RGBA").resize((400, 400))
                b.paste(q, (i * 400, y * 400), q)
                ImageDraw.Draw(b).text((i * 400 + 6, y * 400 + 6), art + v + " " + n, fill=(200, 0, 0))
                i += 1
    b.save(r"C:\Users\DucNg\AppData\Local\Temp\claude\C--Users-DucNg\32bd1786-2635-4dfe-bf70-e4ff6a4f89ba\scratchpad\rob2.png")


if __name__ == "__main__":
    main()
