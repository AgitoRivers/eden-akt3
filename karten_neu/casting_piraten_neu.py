# -*- coding: utf-8 -*-
r"""Zwei neue Piraten im Kampf (Duc 01.11.2026): PirateBrawler (Nahkampf, nach seinem Pixel-Blatt) und PirateGunner (Fernkampf, Look wie PirateAlpha, Steinschlosspistole).
Je 3 Varianten, je 2 Seeds. Der hagere Pirate und PirateAlpha bleiben unberuehrt, U Riscossore nutzt PirateAlpha weiter.

    casting_piraten_neu.py [--nur b1,g2]   -> output\expressions\_casting_piraten_neu\<b1..b3|g1..g3>\idle(-1).png
"""
import json, os, sys, time, urllib.request

sys.path.insert(0, r"X:\AI\PromptStudio")
OUT = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions"
ORDNER = "_casting_piraten_neu"
PS, COMFY = "http://127.0.0.1:8301", "http://127.0.0.1:8189"
MODELL = {"unet": "krea2_turbo_fp8_scaled.safetensors", "clip": "qwen3vl_4b_fp8_scaled.safetensors"}
LORAS = [{"name": "Krea_Real3.safetensors", "strength": 0.7}, {"name": "Krea_Lenovo.safetensors", "strength": 0.7},
         {"name": "Krea_Redux.safetensors", "strength": 0.5}]
SEEDS = (240611, 977031)
KOPF = ("photorealistic picture, full body, three-quarter view, the body angled to the left, looking to the left, alone in the frame, Shot on an iPhone, grainy amateur photo, "
        "realistic smartphone photography, full body shot, one single man alone in the frame, his whole body in full view, the camera far back, both feet completely inside the image")
HAUT = "sun-browned weathered skin, natural skin texture with visible pores, slight natural asymmetry in the face, a real individual face"
BRAWLER_KLEID = ("a blue-and-white horizontally striped sleeveless sailor shirt, frayed at the shoulders and open at the neck, a thick frayed yellow rope belt tied in a knot with the ends hanging down, "
                 "torn dirty brown knee-length trousers with patches, barefoot")
GUNNER_KLEID = ("a black tricorn hat over a red bandana, a long bordeaux red coat with tarnished gold buttons, a light shirt, a wide leather belt with a striped red-and-white sash, dark trousers, high dark boots")
PISTOLE = "exactly one antique flintlock pistol with a long steel barrel and a curved wooden grip"
FIGUR = {
    "b1": ("a broad muscular Irish pirate in his thirties with long wavy vivid fiery copper-red hair past his shoulders, a short thick vivid copper-red beard, heavy red eyebrows, a square jaw, a broken nose",
           "his only weapon exactly one curved sabre with a clean bright polished silver steel blade in his right fist with the blade held forward and low to the left, his left hand an empty fist, in a ready fighting stance, weight low, focused hostile stare"),
    "b2": ("a huge barrel-chested Scottish pirate in his forties with long tangled vivid fiery copper-red hair, a wide bushy vivid copper-red beard, small angry green eyes, a scar across the cheek, thick arms",
           "his only weapon exactly one curved sabre with a clean bright polished silver steel blade in his right fist with the blade raised beside his head, his left hand an empty fist, in a ready fighting stance, weight low, focused hostile stare"),
    "b3": ("a young stocky muscular Irish pirate in his late twenties with long wild vivid fiery copper-red curls blown back, a short messy vivid copper-red beard, freckles, a wide grinning mouth with a missing tooth",
           "his only weapon exactly one curved sabre with a clean bright polished silver steel blade in his right fist with the blade pointing forward to the left at chest height, his left arm back with an empty fist, in a ready fighting stance, weight low, cocky hostile grin"),
    "g1": ("a grizzled Portuguese pirate captain in his late fifties with a weathered face, a long grey braided beard and a black eyepatch over one eye",
           "his only weapon %s held in his right hand with the arm stretched straight forward to the left at shoulder height, aiming at the enemy, his left hand on his hip, standing side-on, cold hostile stare" % PISTOLE),
    "g2": ("a grizzled Portuguese pirate captain in his late fifties with a weathered face, a long grey braided beard and a black eyepatch over one eye",
           "his only weapon %s held low at his right hip and pointing forward to the left, his left hand an empty fist, knees bent, in a ready stance, cold hostile stare" % PISTOLE),
    "g3": ("a grizzled Portuguese pirate captain in his late fifties with a weathered face, a long grey braided beard and a black eyepatch over one eye",
           "his only weapon %s held up beside his head with the barrel pointing at the sky, his left arm forward with an empty open hand, ready to bring it down, cold hostile stare" % PISTOLE),
}


def prompt(key):
    wer, stand = FIGUR[key]
    kleid = BRAWLER_KLEID if key[0] == "b" else GUNNER_KLEID
    return "%s,\nSubject: %s, %s,\nWearing: %s,\nScene: Plain beige background,\n%s, the whole weapon inside the image." % (KOPF, wer, HAUT, kleid, stand)


def post(url, d):
    r = urllib.request.Request(url, data=json.dumps(d).encode(), headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(r, timeout=60) as f:
        return json.loads(f.read())


def main():
    import studio
    nur = sys.argv[sys.argv.index("--nur") + 1].split(",") if "--nur" in sys.argv else None
    with urllib.request.urlopen(PS + "/api/state", timeout=30) as f:
        cfg = dict(json.loads(f.read())["cfg"])
    wart = []
    for key in FIGUR:
        if nur and key not in nur:
            continue
        c = dict(cfg, loras=LORAS, mode="sprite", sprite_src="t2i", width=1232, height=1232, negative_prompt="", st_set="%s/%s" % (ORDNER, key), st_rembg=True, st_crop=False, **MODELL)
        for s in SEEDS:
            wart.append(post(COMFY + "/prompt", {"prompt": studio.build_graph(c, prompt(key), "idle", s)})["prompt_id"])
    print("eingereiht", len(wart), flush=True)
    ende = time.time() + 400
    while wart and time.time() < ende:
        time.sleep(3)
        for i in list(wart):
            with urllib.request.urlopen(COMFY + "/history/" + i, timeout=30) as f:
                h = json.loads(f.read()).get(i)
            if h:
                print(h.get("status", {}).get("status_str"), flush=True)
                wart.remove(i)
    print("offen", len(wart))


if __name__ == "__main__":
    main()
