# -*- coding: utf-8 -*-
r"""Casting Sergent Kaspar Wolff neu (Duc 01.11.2026, Option A "Der Veteran"): je 3 Varianten fuer Dialog und Kampf, je 2 Seeds.

    casting_wolff_veteran.py [--nur d1,k2] [--neu TEXT]   -> output\expressions\_casting_wolff_veteran\<d1..d3|k1..k3>\pose(-1).png

Laeuft ueber studio.build_graph, die Studio-Einstellungen und Yacht_Wolff/Kampf_Wolff bleiben unberuehrt. Den vollen Satz erst nach Ducs Wahl.
"""
import json, os, sys, time, urllib.request

sys.path.insert(0, r"X:\AI\PromptStudio")
OUT = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions"
ORDNER = "_casting_wolff_veteran_2"
PS, COMFY = "http://127.0.0.1:8301", "http://127.0.0.1:8189"
MODELL = {"unet": "krea2_turbo_fp8_scaled.safetensors", "clip": "qwen3vl_4b_fp8_scaled.safetensors"}
LORAS = [{"name": "Krea_Real3.safetensors", "strength": 0.7}, {"name": "Krea_Lenovo.safetensors", "strength": 0.7},
         {"name": "Krea_Redux.safetensors", "strength": 0.5}]
SEEDS = (240611, 977031)
FOTO = "Shot on an iPhone, grainy amateur photo, realistic smartphone photography"
HAUT = "sun-browned Mediterranean-tanned skin, natural skin texture with visible pores, slight natural asymmetry in the face, a real individual face"
BARETT = "a clearly green wool beret of the French Foreign Legion, rich forest green like a fir tree and not black, with a small brass badge, pulled low over his brow"
KLAPPE = "a plain black eye patch over his left eye, its thin black strap running across his forehead under the beret, one narrow steel-grey right eye"

# Variante: (Gesicht, Ruestung, Schwert im Dialog, Hand im Dialog, Schwert und Stand im Kampf)
VARIANTEN = {
    "1": ("a gaunt long face with hollow cheeks and deep lines, a short cropped grey beard, thin lips, gaunt and battle-hardened",
          "dark grey matte tactical combat armour with flat hard plates on his chest and shoulders over a dark grey long-sleeved combat suit, "
          "a black webbing harness across the chest with a few flat pouches, dark grey combat trousers, black combat boots",
          "exactly one long straight sword in a plain black scabbard strapped across his back, only its hilt visible above his right shoulder",
          "both arms loose at his sides, both hands empty",
          "his only weapon exactly one long straight steel sword gripped in his right fist, the blade held forward and low, his left hand an empty fist"),
    "2": ("a sharp angular face with high cheekbones and a hard jaw, a close-trimmed grey full beard, a thin pale old scar through the eyebrow above the eye patch",
          "a close-fitting dark grey tactical body suit with segmented hard plates on the chest and shoulders, a slim black harness and belt, "
          "black gloves, black combat boots laced high",
          "exactly one long straight sword in a plain black scabbard hanging at his left hip",
          "both arms loose at his sides, both hands empty",
          "his only weapon exactly one long straight steel sword gripped with both hands at chest height, the blade angled up and forward"),
    "3": ("a broad weathered face with a heavy brow and deep lines around the mouth, a short thick grey beard with white in it, lean and wiry",
          "scuffed dark grey tactical combat armour with heavy thick plates on the chest and big shoulder plates, worn paint and old scratches on the plates, "
          "a black webbing harness, a faded olive scarf at his neck, dark grey combat trousers, black combat boots",
          "exactly one long straight sword in a worn black scabbard hanging at his left hip",
          "his left hand resting on the hilt of the sword, his right arm loose at his side",
          "his only weapon exactly one long straight steel sword gripped in his right fist, the blade held low behind him, his left arm forward with the hand an empty fist"),
}


def gesicht(v):
    return "Sergent Kaspar Wolff, a 56-year-old German soldier of the French Foreign Legion, %s, %s, %s" % (VARIANTEN[v][0], KLAPPE, HAUT)


def dialog(v):
    _, ruestung, schwert, hand, _ = VARIANTEN[v]
    return ("photorealistic, front view, direct gaze, %s, full body shot from head to feet, one single man alone in the frame, his whole body in full view, "
            "head and boots inside the frame,\nSubject: %s,\nWearing: %s, %s, %s,\nScene: Plain beige background, He stands square to the camera, %s, "
            "feet shoulder-width apart, legs straight, natural resting posture,\nCalm settled face, relaxed jaw." % (FOTO, gesicht(v), BARETT, ruestung, schwert, hand))


def kampf(v):
    _, ruestung, _, _, stand = VARIANTEN[v]
    return ("photorealistic picture, full body, three-quarter view, the body angled to the left, looking to the left, alone in the frame, %s, full body shot, "
            "one single man alone in the frame, his whole body in full view,\nSubject: %s,\nBody: a lean wiry build,\nWearing: %s, %s, %s,\n"
            "Scene: Plain beige background,\nin a ready fighting stance, weight low, facing left, focused hostile stare, the whole sword inside the image." % (FOTO, gesicht(v), BARETT, ruestung, stand))


def post(url, d):
    r = urllib.request.Request(url, data=json.dumps(d).encode(), headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(r, timeout=60) as f:
        return json.loads(f.read())


def main():
    import studio
    nur = sys.argv[sys.argv.index("--nur") + 1].split(",") if "--nur" in sys.argv else None
    neu = sys.argv[sys.argv.index("--neu") + 1] if "--neu" in sys.argv else ""
    with urllib.request.urlopen(PS + "/api/state", timeout=30) as f:
        cfg = dict(json.loads(f.read())["cfg"])
    wart = []
    for v in VARIANTEN:
        for art, prompt, pose, frei in (("d", dialog(v), "neutral", False), ("k", kampf(v), "idle", True)):
            if nur and art + v not in nur:
                continue
            c = dict(cfg, loras=LORAS, mode="sprite", sprite_src="t2i", width=880, height=1328, negative_prompt="", st_set="%s/%s%s" % (ORDNER, art, v),
                     st_rembg=frei, st_crop=False, **MODELL)
            for s in SEEDS:
                wart.append(post(COMFY + "/prompt", {"prompt": studio.build_graph(c, prompt + neu, pose, s)})["prompt_id"])
    print("eingereiht", len(wart), flush=True)
    ende = time.time() + 600
    while wart and time.time() < ende:
        time.sleep(3)
        for i in list(wart):
            with urllib.request.urlopen(COMFY + "/history/" + i, timeout=30) as f:
                h = json.loads(f.read()).get(i)
            if h:
                print(h.get("status", {}).get("status_str"), flush=True)
                wart.remove(i)
    print("offen", len(wart))
    for w, _, dat in os.walk(os.path.join(OUT, ORDNER)):
        print(w, sorted(dat))


if __name__ == "__main__":
    main()
