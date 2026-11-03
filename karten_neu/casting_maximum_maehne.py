# -*- coding: utf-8 -*-
r"""Mr. Maximum, Steel Mop als Kranz ums Rohr direkt hinter dem Stahlkopf (Duc 01.11.2026: "wie einer Loewenmaehne").

    casting_maximum_maehne.py   -> output\expressions\_casting_maximum_maehne\<1|2>\idle(-1).png
"""
import json, os, sys, time, urllib.request

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, r"X:\AI\PromptStudio")
import casting_maximum_steelmop as cm  # noqa: E402

ORDNER = "_casting_maximum_maehne"
KRANZ = ("a thick shaggy collar of white mop strands fixed all the way around the pipe directly behind the head, spreading out in every direction like the mane around a lion's face, "
         "the steel head in the middle of the mane like the lion's face, the mane attached to the head and not hanging separately")
KOPF = {"1": "one solid heavy square hammer head of smooth dark steel", "2": "one solid long rectangular sledgehammer head of smooth dark steel"}


def prompt(v):
    p = cm.kampf(v).replace(cm.VARIANTEN[v][2], "%s, %s" % (KOPF[v], KRANZ))
    alt = "its heavy head raised to the left in front of him"
    assert alt in p
    return p.replace(alt, "the pipe slanting upward, its heavy head with the mane raised high to the upper left in front of him")


def main():
    import studio
    with urllib.request.urlopen(cm.PS + "/api/state", timeout=30) as f:
        cfg = dict(json.loads(f.read())["cfg"])
    wart = []
    for v in KOPF:
        c = dict(cfg, loras=cm.LORAS, mode="sprite", sprite_src="t2i", width=1232, height=1232, negative_prompt="", st_set="%s/%s" % (ORDNER, v), st_rembg=True, st_crop=False, **cm.MODELL)
        for s in cm.SEEDS:
            wart.append(cm.post(cm.COMFY + "/prompt", {"prompt": studio.build_graph(c, prompt(v), "idle", s)})["prompt_id"])
    ende = time.time() + 300
    while wart and time.time() < ende:
        time.sleep(3)
        for i in list(wart):
            with urllib.request.urlopen(cm.COMFY + "/history/" + i, timeout=30) as f:
                h = json.loads(f.read()).get(i)
            if h:
                print(h.get("status", {}).get("status_str"), flush=True)
                wart.remove(i)
    print("offen", len(wart))


if __name__ == "__main__":
    main()
