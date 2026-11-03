# -*- coding: utf-8 -*-
r"""Re-render single poses of Duc's sabre test sprite (DucErdeSword, 23.10.2026). Same mechanics as
kampf_yamamoto_nachbessern.py: pose text (and for lying poses the outfit card) only for this run, old image to _test.

    kampf_duc_nachbessern.py defeated,hurt,weakened,attack,windup
"""
import io, json, os, shutil, subprocess, sys, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
PS = "http://127.0.0.1:8301"
HERE = os.path.dirname(os.path.abspath(__file__))
NAME = "DucErdeSword"
CARD = "kampf_ducerdesword"
DIR = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions\combat\DucErdeSword"
# 23.10.: "no debris, no splashes ..." made Krea paint exactly that (CFG 1, words in the prompt get drawn).
CLEAN = " He stands on a plain smooth seamless beige studio floor."
TEXT = {
    "guard": "standing upright in a firm defensive stance, knees slightly bent, facing left, the sabre held across his "
             "body with the blade angled up in front of his chest to block, his left hand raised as a guard, focused "
             "stare; the whole figure and the entire blade are fully inside the image." + CLEAN,
    "attack": "striking forward to the left with full force, the sabre in his right hand fully extended forward, a long "
              "lunging step; the whole figure and the entire sabre blade including its tip are fully inside the image "
              "with wide empty space to the left of the tip." + CLEAN,
    "windup": "winding up a strike, the single sabre in his right hand pulled far back behind his head, upper body "
              "leaning back, weight on the back leg, eyes locked to the left; he holds exactly one sabre." + CLEAN,
    "hurt": "hit by a heavy blow, recoiling backwards off balance, head snapped back, his left hand clutching his chest, "
            "the sabre still in his right hand, face twisted in pain." + CLEAN,
    "weakened": "exhausted and worn out, swaying on unsteady legs, panting heavily, slumped, the sabre hanging low in "
                "his right hand." + CLEAN,
    "defeated": "one single man lying flat on his back on a plain smooth seamless beige studio floor, knocked out "
                "like in a cartoon, the whole body fully horizontal, both empty hands resting on his chest, eyes "
                "closed, sunglasses crooked, a calm face, his clothes clean and neat",
}
QUER = {"defeated"}
LOOK_OVERRIDE = {   # without "holding a sabre", otherwise Krea adds a second, standing figure (Yamamoto, 23.10.)
    "defeated": "a black leather biker jacket with an asymmetric zip and bronze zippers and buckles, a plain white "
                "crew-neck t-shirt, black slim jeans, dark brown leather boots, aviator sunglasses with bronze frames",
}
# 23.10.: with the sabre in the defeated pose Krea twice added a blood pool -> no weapon in this pose


def ps(path, data=None):
    req = urllib.request.Request(PS + path, data=None if data is None else json.dumps(data).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


poses = sys.argv[1].split(",") if len(sys.argv) > 1 else []
if not poses or any(p not in TEXT for p in poses):
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
