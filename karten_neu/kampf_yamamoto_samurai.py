# -*- coding: utf-8 -*-
r"""Combat enemy Yamamoto-san in black/red samurai armor (23.10.2026, Duc): the worthiness duel after Jana's rescue.
Duc: keep it simple so Krea recognises the clothes - samurai armor, white headband, round glasses, sword.
Identity tags come from the preset Yacht_Yamamoto (without sunglasses). Same build as kampf_neue_gegner_4.py.

    kampf_yamamoto_samurai.py          dry run
    kampf_yamamoto_samurai.py test     enter card/preset/set preset, queue one test image (outfit_check)
    kampf_yamamoto_samurai.py voll     full pose run (after Duc's OK to the test image; 23.10.: v3 black/red)
    kampf_yamamoto_samurai.py fertig   mirror the flee pose when everything is rendered
"""
import json, os, subprocess, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))   # stdout is set to UTF-8 by studio_kampf_gegner on import
sys.path.insert(0, HERE)
MODE = sys.argv[1].lower() if len(sys.argv) > 1 else ""
sys.argv = [sys.argv[0]]
import studio_kampf_gegner as sk  # noqa: E402
import duc_common as dc  # noqa: E402

PS = "http://127.0.0.1:8301"
NAME = "YamamotoSamurai"
SUBJECT = "Yamamoto-san, a 52-year-old Japanese banker with dark brown eyes"
LOOK = ("traditional black and red samurai armor made of large smooth black lacquered plates with red silk cords and "
        "red trim, a white headband tied around his forehead, small round glasses, holding one single katana with both "
        "hands in front of him, the katana is the only sword he carries")
# v1: lacing slots + studs, second sword · v2 (white, smooth): Duc 23.10. "white looks odd" -> traditional black/red
SKIP_TAGS = {"M Glasses: Sun Glasses", "View: Front"}


def ps(path, data=None):
    req = urllib.request.Request(PS + path, data=None if data is None else json.dumps(data).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


presets, sets = dc.load_json(sk.F_PRESETS, None, "Studio"), dc.load_json(sk.F_SETS, None, "Studio")
tags = [t for t in presets["Yacht_Yamamoto"].get("tags_on", []) if t not in SKIP_TAGS]
print("%s  mann  %s\n  look: %s\n  tags: %s" % (NAME, SUBJECT, LOOK, ", ".join(tags)))
if MODE == "fertig":
    subprocess.run([sys.executable, os.path.join(HERE, "kampf_flee_spiegeln.py"), "--los"], check=True)
    sys.exit(0)
if MODE not in ("test", "voll"):
    sys.exit("PROBELAUF - test / voll / fertig")

d = ps("/api/state")["decks"]
card = "kampf_" + NAME.lower()
cards = {c["name"]: c for c in d["outfit"]}
if card in cards:
    cards[card]["prompt"] = LOOK
else:
    d["outfit"].append({"name": card, "prompt": LOOK, "on": True, "tag": "kampf", "sel": False, "back_prompt": ""})
ps("/api/decks", d)
presets["Kampf_" + NAME] = sk.preset(NAME, "mann", SUBJECT, tags, "hoch")
sets["Kampf_%s|Kampf" % NAME] = {"outfit": [card], "setting": ["A Sprite Background"], "tags": ["View: Kampf"] + tags}
dc.save_json(sk.F_PRESETS, presets, "Studio")
dc.save_json(sk.F_SETS, sets, "Studio")
print("eingetragen: Kampf_" + NAME)
if MODE == "test":
    subprocess.run([sys.executable, os.path.join(HERE, "kampf_test.py"), "--karten", "outfit_check", "--gegner", NAME],
                   check=True)
    print("Testbild eingereiht -> output\\expressions\\combat\\%s\\outfit_check.png" % NAME)
else:
    subprocess.run([sys.executable, os.path.join(HERE, "kampf_volllauf_runde3.py"), "--los", "--gegner", NAME],
                   check=True)
    print("Posen eingereiht. Wenn ComfyUI fertig ist: Kampf_Yamamoto.bat -> fertig")
