# -*- coding: utf-8 -*-
r"""Mr. Maximum, Steel Mop nach Ducs Pixel-Sprite (01.11.2026): grosser Stahlwuerfel, kurzer flauschiger Borstenring ums Rohr auf dem Wuerfel. Hemd ausgefranst, keine Brille.

    casting_maximum_wuerfel.py   -> output\expressions\_casting_maximum_wuerfel_2\<boden|schulter|bereit>\idle(-1).png
"""
import json, sys, time, urllib.request, os

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, r"X:\AI\PromptStudio")
import casting_maximum_steelmop as cm  # noqa: E402

ORDNER = "_casting_maximum_wuerfel_2"
WAFFE = ("a giant hammer made from one long straight plain dark steel pipe with a rounded cap at the handle end, at its other end one huge solid cube of smooth dark steel as big as a beer crate, "
         "the pipe goes straight into the middle of one face of the cube, and on that same face a low thick fluffy wreath of white scrubbing bristles hugs the pipe all the way around where it enters the cube, "
         "the wreath smaller than the cube, nothing else attached to the cube, all other faces of the cube plain and smooth, the cube fully visible")
HALTUNG = {
    "boden": "standing with his legs apart, facing left, the steel cube resting on the floor beside his front foot, the pipe rising upward from the cube, his right hand gripping the top of the pipe at chest height, his left arm hanging with a clenched fist, a calm hard stare",
    "schulter": "walking to the left with a long step, the pipe resting on his right shoulder with the steel cube behind his head high up on the right, his right hand holding the pipe in front of his shoulder, his left arm swinging with a clenched fist",
    "bereit": "in a ready fighting stance, weight low, facing left, focused hostile stare, gripping the pipe with both hands, the pipe slanting upward and the steel cube raised high to the upper left in front of him",
}


def prompt(h):
    p = cm.kampf("3")
    a = p.index("in a ready fighting stance")
    return p[:a] + "%s, %s, the whole weapon inside the image." % (h, WAFFE)


def main():
    import studio
    with urllib.request.urlopen(cm.PS + "/api/state", timeout=30) as f:
        cfg = dict(json.loads(f.read())["cfg"])
    wart = []
    for n, h in HALTUNG.items():
        c = dict(cfg, loras=cm.LORAS, mode="sprite", sprite_src="t2i", width=1232, height=1232, negative_prompt="", st_set="%s/%s" % (ORDNER, n), st_rembg=True, st_crop=False, **cm.MODELL)
        for s in cm.SEEDS:
            wart.append(cm.post(cm.COMFY + "/prompt", {"prompt": studio.build_graph(c, prompt(h), "idle", s)})["prompt_id"])
    ende = time.time() + 300
    while wart and time.time() < ende:
        time.sleep(3)
        for i in list(wart):
            with urllib.request.urlopen(cm.COMFY + "/history/" + i, timeout=30) as f:
                r = json.loads(f.read()).get(i)
            if r:
                print(r.get("status", {}).get("status_str"), flush=True)
                wart.remove(i)
    print("offen", len(wart))


if __name__ == "__main__":
    main()
