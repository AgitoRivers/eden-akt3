# -*- coding: utf-8 -*-
r"""Re-render single Yamamoto-san combat poses with a pose text for this run only (23.10.2026, Duc).
The old pose image moves to combat\YamamotoSamurai\_test\<pose>_v1.png first; the kampf card text is restored after.

    kampf_yamamoto_nachbessern.py attack           re-render these poses (comma separated)
"""
import io, json, os, shutil, subprocess, sys, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
PS = "http://127.0.0.1:8301"
HERE = os.path.dirname(os.path.abspath(__file__))
NAME = "YamamotoSamurai"
DIR = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions\combat\YamamotoSamurai"
TEXT = {
    "attack": "striking forward to the left with full force, both hands on the katana, the sword fully extended forward, "
              "a long lunging step forward; the whole figure and the entire katana blade including its tip are fully "
              "inside the image with wide empty space to the left of the blade tip",
    "heavy_windup": "gathering all his strength for a devastating blow, both hands gripping the katana raised high above "
                    "his head, the blade pointing up and back over his head, body coiled, teeth clenched; the whole "
                    "katana blade is clearly visible above him and fully inside the image",
    "heavy_attack": "unleashing a devastating two-handed downward slash forward to the left, both hands on the katana, "
                    "the long blade swinging down in front of his body and clearly visible from hilt to tip, deep lunge; "
                    "the whole figure and the entire blade are fully inside the image with empty space around them",
    "enraged":"furious, face red with rage, teeth clenched and bared, glasses askew, shouting, gripping the katana "
               "with both hands raised high, the whole body tense and shaking with anger",
    "weakened": "exhausted, down on one knee, leaning heavily on the katana planted point-down in the floor, head "
                "hanging, panting, sweat on his face, the headband slipping",
    "victory": "triumphant, standing tall, the katana raised high above his head with one arm, the other fist on his "
               "hip, chin up, a proud satisfied smile",
    "defeated": "one single man lying flat on his back on the ground, knocked out, the whole body fully horizontal, "
                "arms spread, eyes closed, glasses crooked, the katana lying on the floor beside his open hand; he is "
                "the only person in the image, nobody else standing",
}
QUER = {"defeated"}   # lying poses of upright figures render in landscape
CARD = "kampf_yamamotosamurai"
# The outfit card says "holding one katana with both hands" - for lying poses that made Krea add a second, standing
# figure (23.10. twice). For these poses the card is swapped for the run only.
LOOK_OVERRIDE = {
    "defeated": "traditional black and red samurai armor made of large smooth black lacquered plates with red silk "
                "cords and red trim, a white headband, small round glasses; his single katana lies on the floor next "
                "to him",
}


def ps(path, data=None):
    req = urllib.request.Request(PS + path, data=None if data is None else json.dumps(data).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


poses = sys.argv[1].split(",") if len(sys.argv) > 1 else []
unknown = [p for p in poses if p not in TEXT]
if not poses or unknown:
    sys.exit("Posen: %s" % ", ".join(TEXT))
os.makedirs(os.path.join(DIR, "_test"), exist_ok=True)
for p in poses:
    src = os.path.join(DIR, p + ".png")
    if os.path.exists(src):
        shutil.move(src, os.path.join(DIR, "_test", p + "_v1.png"))
st = ps("/api/state")["decks"]
original = {c["name"]: c["prompt"] for c in st["kampf"]}
original_look = {c["name"]: c["prompt"] for c in st["outfit"] if c["name"] == CARD}
try:
    for p in poses:
        d = ps("/api/state")["decks"]
        for c in d["kampf"]:
            if c["name"] == p:
                c["prompt"] = TEXT[p]
        for c in d["outfit"]:
            if c["name"] == CARD:
                c["prompt"] = LOOK_OVERRIDE.get(p, original_look.get(CARD, c["prompt"]))
        ps("/api/decks", d)
        cmd = [sys.executable, os.path.join(HERE, "kampf_test.py"), "--karten", p, "--gegner", NAME]
        if p in QUER:
            cmd.insert(2, "--quer")
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
        print("eingereiht:", p)
finally:
    d = ps("/api/state")["decks"]
    for c in d["kampf"]:
        if c["name"] in original:
            c["prompt"] = original[c["name"]]
    for c in d["outfit"]:
        if c["name"] in original_look:
            c["prompt"] = original_look[c["name"]]
    ps("/api/decks", d)
    print("Kartentexte zurückgesetzt")
