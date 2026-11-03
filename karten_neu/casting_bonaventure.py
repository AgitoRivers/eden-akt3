# -*- coding: utf-8 -*-
r"""Casting Captain Bonaventure (Duc 01.11.2026 ueber die Story-Sitzung): Look "Der Koenig ohne Land", drei Spielarten, je 2 Seeds, nur Dialog-Sprite. Eigenes Set.
Fotorealistisch wie alle Eden-Sprites, das Komische kommt aus den Proportionen. Kein Rot, Weiss, Schwarz oder Dunkelblau als Hauptfarbe.

    casting_bonaventure.py   -> output\expressions\_casting_bonaventure\<1|2|3>\neutral(-1).png

Laeuft ueber studio.build_graph, die Studio-Einstellungen bleiben unberuehrt.
"""
import json, sys, time, urllib.request

sys.path.insert(0, r"X:\AI\PromptStudio")
ORDNER = "_casting_bonaventure"
PS, COMFY = "http://127.0.0.1:8301", "http://127.0.0.1:8189"
MODELL = {"unet": "krea2_turbo_fp8_scaled.safetensors", "clip": "qwen3vl_4b_fp8_scaled.safetensors"}
LORAS = [{"name": "Krea_Real3.safetensors", "strength": 0.7}, {"name": "Krea_Lenovo.safetensors", "strength": 0.7},
         {"name": "Krea_Redux.safetensors", "strength": 0.5}]
SEEDS = (193377, 458820)
KOERPER = ("a comically huge round barrel belly on very thin long legs, a larger-than-life cartoonish silhouette, big broad chest, "
           "the belly much wider than his hips, thin bony knees")
MANTEL = ("an enormous royal purple captain's coat with wide gold trim, hanging open over his belly, oversized gold epaulettes sticking far out from his shoulders, "
          "a blue and white striped sailor shirt stretched over the belly and tucked in, tight khaki canvas breeches covering his thin legs from the belt down into the boots, tall glossy boots in dark brown leather, a broad curved cutlass in a scabbard at his hip, "
          "a royal purple tricorn hat, and sitting crooked on top of the hat a homemade crown cut from a tin can with jagged points, "
          "a thin wooden pole strapped to his back rising above his head with a small purple flag on it")
# Variante: (Gesicht, Bart, Haar)
VARIANTEN = {
    "1": ("Bonaventure, a 45-year-old Marseille sea captain, a broad round sun-tanned face, a big fleshy nose, small bright eyes, a huge proud grin showing all his teeth",
          "a very large proud curled moustache twisted up into two points",
          "wild curly dark brown hair under the hat"),
    "2": ("Bonaventure, a 55-year-old Marseille sea captain, a long weathered sun-tanned face, a hooked nose, bushy grey eyebrows raised very high, a wide delighted grin with one gold tooth",
          "a giant grey curled moustache twisted up into two long points that reach past his cheeks",
          "long grey hair tied back under the hat"),
    "3": ("Bonaventure, a 38-year-old Marseille sea captain, a wide square sun-tanned face, a strong chin with a dimple, huge shining eyes full of certainty, a beaming heroic grin with his chin held high",
          "a very wide ginger-brown handlebar moustache curled up at both ends",
          "thick ginger-brown hair sticking out under the hat"),
}


def prompt(v):
    gesicht, bart, haar = VARIANTEN[v]
    return ("photorealistic, front view, direct gaze, Shot on an iPhone, grainy amateur photo, realistic smartphone photography, full body shot from head to feet, one single man alone in the frame, "
            "his whole body in full view, hat, flag and boots inside the frame,\nSubject: %s,\nBody: %s,\nHair: %s,\nFace: %s,\nWearing: %s,\nScene: Plain beige background, He stands square to the camera, chest out, "
            "both fists on his hips, feet apart, like a king greeting his people,\nHe is completely serious about all of this." % (gesicht, KOERPER, haar, bart, MANTEL))


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
        c = dict(cfg, loras=LORAS, mode="sprite", sprite_src="t2i", width=1104, height=1408, negative_prompt="", st_set="%s/%s" % (ORDNER, v), st_rembg=True, st_crop=False, **MODELL)
        for s in SEEDS:
            wart.append(post(COMFY + "/prompt", {"prompt": studio.build_graph(c, prompt(v), "neutral", s)})["prompt_id"])
    print("eingereiht", len(wart), flush=True)
    ende = time.time() + 280
    while wart and time.time() < ende:
        time.sleep(3)
        for i in list(wart):
            with urllib.request.urlopen(COMFY + "/history/" + i, timeout=30) as f:
                h = json.loads(f.read()).get(i)
            if h:
                wart.remove(i)
    print("offen", len(wart))


if __name__ == "__main__":
    main()
