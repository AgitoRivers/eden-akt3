# -*- coding: utf-8 -*-
r"""Casting Minicu (Duc 01.11.2026): der sanfte Riese am Hafen von Cala d'Orsu, nur Dialog-Sprite, je 2 Seeds. Eigenes Set.
Maxwell ist kahl und Bodybuilder: Minicu ist weich, schwer und behaart, damit man beide nicht verwechselt.

    casting_minicu.py   -> output\expressions\_casting_minicu\<1|2|3>\neutral(-1).png

Laeuft ueber studio.build_graph, die Studio-Einstellungen bleiben unberuehrt.
"""
import json, os, sys, time, urllib.request

sys.path.insert(0, r"X:\AI\PromptStudio")
ORDNER = "_casting_minicu"
PS, COMFY = "http://127.0.0.1:8301", "http://127.0.0.1:8189"
MODELL = {"unet": "krea2_turbo_fp8_scaled.safetensors", "clip": "qwen3vl_4b_fp8_scaled.safetensors"}
LORAS = [{"name": "Krea_Real3.safetensors", "strength": 0.7}, {"name": "Krea_Lenovo.safetensors", "strength": 0.7},
         {"name": "Krea_Redux.safetensors", "strength": 0.5}]
SEEDS = (310771, 640129)
FOTO = "Shot on an iPhone, grainy amateur photo, realistic smartphone photography"
KOERPER = ("a giant of a man, enormously tall and wide, heavy soft rounded shoulders, thick soft arms, a big round belly, huge broad hands, thick legs, "
           "his head looks small on top of his huge body, not muscular like a bodybuilder")
HAUT = "deep sun-tanned Mediterranean skin, weathered by years on a harbour"
# Variante: (Gesicht, Haar, Kleidung)
VARIANTEN = {
    "1": ("a long broad gentle face, a wide flat nose, small kind brown eyes under heavy eyebrows, a soft shy mouth, a full untidy dark beard",
          "long shaggy dark brown hair falling to his shoulders",
          "a faded heavy cream cotton work shirt with the sleeves rolled up, worn brown canvas overalls with wide straps, big scuffed leather work boots"),
    "2": ("a big round soft face with full cheeks, a small round nose, wide gentle dark eyes that look a little puzzled, a small shy smile, clean-shaven with a light shadow",
          "short thick black hair cut unevenly, as if somebody kind cut it for him at home",
          "a washed-out navy blue t-shirt, too small for him, faded dark blue dungarees with one strap twisted, big scuffed leather work boots"),
    "3": ("a square gentle face, a nose that was broken long ago, calm grey-brown eyes, thick eyebrows, a patient mouth, a short curly dark beard",
          "short tight dark curls",
          "a faded blue docker's work shirt with the sleeves rolled up, a thick dark leather carrying apron over dark work trousers tied with rope, a coil of rope on one shoulder, big scuffed leather work boots"),
}


def prompt(v):
    gesicht, haar, kleidung = VARIANTEN[v]
    wer = ("Minicu, a 34-year-old Corsican dock worker from Cala d'Orsu,\nBody: %s,\nHair: %s,\nSkin: %s,\nFace: %s" % (KOERPER, haar, HAUT, gesicht))
    return ("photorealistic, front view, direct gaze, %s, full body shot from head to feet, one single man alone in the frame, his whole body in full view, head and boots inside the frame,\n"
            "Subject: %s,\nWearing: %s,\nScene: Plain beige background, He stands square to the camera, both arms loose at his sides, both huge hands empty, feet shoulder-width apart, legs straight,\n"
            "A calm patient face with the faintest hint of a smile." % (FOTO, wer, kleidung))


def post(url, d):
    r = urllib.request.Request(url, data=json.dumps(d).encode(), headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(r, timeout=60) as f:
        return json.loads(f.read())


def main():
    import studio
    with urllib.request.urlopen(PS + "/api/state", timeout=30) as f:
        cfg = dict(json.loads(f.read())["cfg"])
    wart = []
    for v in VARIANTEN:
        c = dict(cfg, loras=LORAS, mode="sprite", sprite_src="t2i", width=880, height=1328, negative_prompt="", st_set="%s/%s" % (ORDNER, v), st_rembg=False, st_crop=False, **MODELL)
        for s in SEEDS:
            wart.append(post(COMFY + "/prompt", {"prompt": studio.build_graph(c, prompt(v), "neutral", s)})["prompt_id"])
    print("eingereiht", len(wart), flush=True)
    ende = time.time() + 540
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
