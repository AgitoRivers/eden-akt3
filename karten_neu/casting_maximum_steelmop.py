# -*- coding: utf-8 -*-
r"""Casting Mr. Maximum mit Steel Mop (Duc 01.11.2026): je 3 Varianten fuer Dialog (ohne Waffe) und Kampf (Maehne aus Mopp-Fransen unter dem Hammerkopf), je 2 Seeds. Eigenes Set, die alten Sets bleiben.

    casting_maximum_steelmop.py [--nur d1,k2]   -> output\expressions\_casting_maximum_steelmop_3\<d1..d3|k1..k3>\pose(-1).png

Gesicht und Koerper aus Yacht_Maximum und seinen Tags. Laeuft ueber studio.build_graph, die Studio-Einstellungen bleiben unberuehrt.
"""
import json, os, sys, time, urllib.request

sys.path.insert(0, r"X:\AI\PromptStudio")
OUT = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions"
ORDNER = "_casting_maximum_steelmop_3"
PS, COMFY = "http://127.0.0.1:8301", "http://127.0.0.1:8189"
MODELL = {"unet": "krea2_turbo_fp8_scaled.safetensors", "clip": "qwen3vl_4b_fp8_scaled.safetensors"}
LORAS = [{"name": "Krea_Real3.safetensors", "strength": 0.7}, {"name": "Krea_Lenovo.safetensors", "strength": 0.7},
         {"name": "Krea_Redux.safetensors", "strength": 0.5}]
SEEDS = (240611, 977031)
FOTO = "Shot on an iPhone, grainy amateur photo, realistic smartphone photography"
WER = ("Mr. Maximum, a big strong 35-year-old South African man with dark brown eyes, bodybuilder arms,\nBody: a massive bodybuilder physique, broad rounded shoulders, huge arms, "
       "a thick chest and neck, thick veins on his forearms and biceps, very tall, towering over everyone around him,\nHair: a smooth shaved bald head with a light shine,\n"
       "Skin: smooth deep brown skin,\nFace: a short neat goatee")
HOSE = "a clean black bow tie at his collar, dark navy blue uniform trousers with a sharp crease and no belt, polished black dress shoes"
MAEHNE = "directly below the block a big shaggy mane of thick white mop strands hanging down all around the pipe like the mane of a lion, the steel block fully visible above the mane"

# Variante: (Hemd, Brille, Kopf des Mops)
VARIANTEN = {
    "1": ("a white steward uniform shirt with the sleeves torn off at the shoulders, neatly buttoned, stretched tight over his chest", "",
          "one solid heavy square hammer head of smooth dark steel, %s" % MAEHNE),
    "2": ("a white steward uniform shirt with the sleeves torn off at the shoulders, neatly buttoned, stretched tight over his chest",
          "Oakley Sutro sunglasses with blue mirror glass, ",
          "one solid long rectangular sledgehammer head of smooth dark steel, %s" % MAEHNE),
    "3": ("a white steward uniform shirt with the sleeves ripped off roughly, frayed threads at the shoulders, the top of the shirt straining over his chest", "",
          "one huge solid round drum-shaped hammer head of smooth dark steel, %s" % MAEHNE),
}


def mop(v):
    return "a steel mop made from one long straight plain steel pipe, at its end %s, smooth solid metal surfaces" % VARIANTEN[v][2]


def dialog(v):
    hemd, brille, _ = VARIANTEN[v]
    return ("photorealistic, front view, direct gaze, %s, full body shot from head to feet, one single man alone in the frame, his whole body in full view, head and shoes inside the frame,\n"
            "Subject: %s,\nWearing: %s%s, %s,\nScene: Plain beige background, He stands square to the camera, both arms loose at his sides, both hands empty, feet shoulder-width apart, legs straight,\n"
            "Calm settled face with the faintest hint of a smile." % (FOTO, WER, brille, hemd, HOSE))


def kampf(v):
    hemd, brille, _ = VARIANTEN[v]
    return ("photorealistic picture, full body, three-quarter view, the body angled to the left, looking to the left, alone in the frame, %s, full body shot, one single man alone in the frame, "
            "his whole body in full view,\nSubject: %s,\nWearing: %s%s, %s,\nScene: Plain beige background,\nin a ready fighting stance, weight low, facing left, focused hostile stare, "
            "gripping with both hands %s, its heavy head raised to the left in front of him, the whole weapon inside the image." % (FOTO, WER, brille, hemd, HOSE, mop(v)))


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
    for v in VARIANTEN:
        for art, prompt, pose, frei, b, h in (("d", dialog(v), "neutral", False, 880, 1328), ("k", kampf(v), "idle", True, 1232, 1232)):
            if nur and art + v not in nur:
                continue
            c = dict(cfg, loras=LORAS, mode="sprite", sprite_src="t2i", width=b, height=h, negative_prompt="", st_set="%s/%s%s" % (ORDNER, art, v),
                     st_rembg=frei, st_crop=False, **MODELL)
            for s in SEEDS:
                wart.append(post(COMFY + "/prompt", {"prompt": studio.build_graph(c, prompt, pose, s)})["prompt_id"])
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


if __name__ == "__main__":
    main()
