# -*- coding: utf-8 -*-
r"""Wolff "Der Veteran", guard neu (Duc 01.11.2026: "hier bitte schwert defensiv halten"): 3 Vorschlaege.

    wolff_veteran_guard.py   -> output\expressions\_wolff_veteran_guard\<1|2|3>\guard.png
"""
import json, os, sys, time, urllib.request

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, r"X:\AI\PromptStudio")
import casting_wolff_veteran as cv  # noqa: E402

ORDNER = "_wolff_veteran_guard"
RAHMEN = "the camera far back, the whole sword and both boots completely inside the image with wide empty floor below them, eye on the threat to the left"
VORSCHLAEGE = {
    "1": ("his only weapon exactly one long straight steel sword gripped with both hands in front of his chest, the blade pointing straight up close to his face",
          "in a defensive guard, body pulled back and low, the upright blade shielding his face and chest from an attack from the left"),
    "2": ("his only weapon exactly one long straight steel sword gripped in his right fist at head height, the blade held level across the front of his body above his head, his left hand supporting the flat of the blade",
          "blocking a blow from above, knees bent, the level blade held up as a shield over his head"),
    "3": ("his only weapon exactly one long straight steel sword gripped with both hands low at his right hip, the blade slanting up and across the front of his body",
          "in a defensive guard, weight on the back leg, the slanted blade held across his whole body to parry an attack from the left"),
}


def main():
    import studio
    with urllib.request.urlopen(cv.PS + "/api/state", timeout=30) as f:
        cfg = dict(json.loads(f.read())["cfg"])
    alt = "in a ready fighting stance, weight low, facing left, focused hostile stare, the whole sword inside the image."
    wart = []
    for nr, (waffe, stand) in VORSCHLAEGE.items():
        p = cv.kampf("3").replace(cv.VARIANTEN["3"][4], waffe).replace(alt, "%s, %s." % (stand, RAHMEN))
        c = dict(cfg, loras=cv.LORAS, mode="sprite", sprite_src="t2i", width=1232, height=1232, negative_prompt="", st_set="%s/%s" % (ORDNER, nr), st_rembg=True, st_crop=True, **cv.MODELL)
        wart.append(cv.post(cv.COMFY + "/prompt", {"prompt": studio.build_graph(c, p, "guard", cv.SEEDS[0])})["prompt_id"])
    ende = time.time() + 300
    while wart and time.time() < ende:
        time.sleep(3)
        for i in list(wart):
            with urllib.request.urlopen(cv.COMFY + "/history/" + i, timeout=30) as f:
                h = json.loads(f.read()).get(i)
            if h:
                print(h.get("status", {}).get("status_str"), flush=True)
                wart.remove(i)
    print("offen", len(wart))


if __name__ == "__main__":
    main()
