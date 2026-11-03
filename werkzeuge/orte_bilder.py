# -*- coding: utf-8 -*-
r"""Location backgrounds for the two location chapters (21.10.2026, docs\wiki\welt\orte_drehbuch.md).

    python orte_bilder.py --cards            add/update the setting cards in Prompt Studio (deck "setting", tag "eden_orte")
    python orte_bilder.py --queue [names]    queue 4 variants each in ComfyUI Krea2 (front of the queue)
    python orte_bilder.py --pick name=k ...  copy the chosen variant to the SillyTavern backgrounds as eden_rise_<name>.png

Same render path as werkzeuge\hintergrund_bild.py (BigLove + Real3, 1664x928, no people); the prompt wraps the card
text like Prompt Studio's setting mode ("<card>, a contemporary scene, richly detailed").
"""
import json, os, random, re, shutil, sys, urllib.request

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import item_bilder as ib  # noqa: E402

DOC = os.path.join(os.path.dirname(HERE), "docs", "EDEN_ORTE_DREHBUCH.md")
ST_BG = r"X:\AI\SillyTavern3\SillyTavern-Launcher\SillyTavern\data\default-user\backgrounds"
VAR = os.path.join(ST_BG, "_varianten", "eden_rise_orte")
PS = "http://127.0.0.1:8301"
SUFFIX = (", a contemporary scene, richly detailed, photorealistic, wide angle, natural colours, "
          "no people, no animals, no text")
NEGATIV = "people, person, man, woman, animal, hands, text, watermark, logo, blurry, cartoon, anime, 3d render"


def cards():
    """Setting cards from the image list at the end of the screenplay."""
    text = open(DOC, encoding="utf-8").read()
    part = text[text.index("# Bildliste"):]
    return dict(re.findall(r"^\| `([a-z_]+)` \| (.+?) \|$", part, re.M))


def ps(path, data=None):
    req = urllib.request.Request(PS + path, data=None if data is None else json.dumps(data).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def add_cards():
    c = cards()
    d = ps("/api/state")["decks"]
    have = {x["name"]: x for x in d["setting"]}
    for name, prompt in c.items():
        if name in have:
            have[name]["prompt"] = prompt
        else:
            d["setting"].append({"name": name, "prompt": prompt, "on": True, "tag": "eden_orte", "sel": False})
    ps("/api/decks", d)
    print("%d Setting-Karten im Prompt Studio (Tag eden_orte)" % len(c))


def queue(only):
    ib.NEGATIV = NEGATIV
    ib.NSFW_PROFIL["loras"] = [("Krea_Real3.safetensors", 0.7)]
    os.makedirs(VAR, exist_ok=True)
    n = 0
    for name, prompt in cards().items():
        if only and name not in only:
            continue
        for k in range(1, 5):
            g = ib.graph(prompt + SUFFIX, VAR, "%s_v%d" % (name, k), random.randint(1, 2 ** 31), True)
            g["6"]["inputs"].update({"width": 1664, "height": 928})
            ib.post("/prompt", {"prompt": g, "front": True})
            n += 1
    print("%d Aufträge eingereiht -> %s" % (n, VAR))


def pick(pairs):
    for p in pairs:
        name, k = p.split("=")
        shutil.copy2(os.path.join(VAR, "%s_v%s.png" % (name, k)), os.path.join(ST_BG, "eden_rise_%s.png" % name))
        print("übernommen:", name, k)


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--cards" in a:
        add_cards()
    elif "--queue" in a:
        queue([x for x in a if not x.startswith("-")])
    elif "--pick" in a:
        pick([x for x in a if "=" in x])
    else:
        print(__doc__)
