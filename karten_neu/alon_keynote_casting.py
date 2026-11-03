# -*- coding: utf-8 -*-
r"""Alon fuer die Keynote (Duc 02.11.2026, Cliffhanger Akt 2): vier Looks als Casting und zwei Buehnenbilder fuer die Pressekonferenz.
Gesicht und Koerper wie seine Kampf-Sprites (output\expressions\combat\Alon), statt Ruestung ein Keynote-Look. Eine schmale schwarze
Schiene am Handgelenk deutet das Exoskelett gegen seine Krankheit an (Wiki figuren/alon.md).

    alon_keynote_casting.py   -> output\expressions\_alon_keynote\<look>.png, buehne_<n>.png
"""
import json, sys, time, urllib.request

sys.path.insert(0, r"X:\AI\PromptStudio")
PS, COMFY = "http://127.0.0.1:8301", "http://127.0.0.1:8189"
ORDNER = "_alon_keynote"
LORAS = [{"name": "Krea_Real3.safetensors", "strength": 0.7}, {"name": "Krea_Lenovo.safetensors", "strength": 0.7},
         {"name": "Krea_Redux.safetensors", "strength": 0.5}]
KOPF = ("8k, photorealistic picture, front view, direct gaze, frontal view, realistic smartphone photography, full body shot from head "
        "to feet, one single man alone in the frame, his whole body in full view, head and feet inside the frame")
WER = ("a smug fictional tech billionaire in his early fifties with a short grey buzz cut and a friendly, cocky grin, clean-shaven, "
       "a soft middle-aged body with a small round belly and narrow shoulders, slightly pale under a light tan, aviator sunglasses "
       "pushed up on his head")
SCHIENE = "a thin piano-black metal brace around his right wrist, half hidden under the cuff"
LOOKS = {
    "a_pullover": "a soft heather-grey cashmere jumper with the sleeves pushed up, dark slim jeans, clean white sneakers, " + SCHIENE,
    "b_rollkragen": "a black merino turtleneck, charcoal chinos, black leather sneakers, " + SCHIENE,
    "c_bomber": "an unzipped navy technical bomber jacket over a plain charcoal T-shirt, dark jeans, grey running shoes, " + SCHIENE,
    "d_ruestung": "a dark grey hoodie with the front half open, and under it a glimpse of glossy piano-black armour plating across his "
                  "chest, dark jeans, white sneakers, " + SCHIENE,
}
HALTUNG = "He stands relaxed on a plain beige background, one hand open towards the viewer as if he is presenting something, a calm product-launch smile"
BUEHNE = ("a huge dark keynote stage in a modern conference hall, present-day contemporary, one gigantic curved LED screen glowing with a soft "
          "blue sky gradient, a thin ring of white light on the black stage floor, a small transparent glass lectern, rows of empty "
          "seats fading into darkness in the foreground, cool blue spotlights cutting through light haze, not a single person is in the "
          "shot, richly detailed")
SEEDS = (510233, 884107)


def post(url, daten):
    req = urllib.request.Request(url, data=json.dumps(daten).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())


def main():
    import studio
    with urllib.request.urlopen(PS + "/api/state", timeout=30) as f:
        cfg = dict(json.loads(f.read())["cfg"])
    wart = []
    for k, anzug in LOOKS.items():
        p = "%s,\nSubject: %s,\nWearing: %s,\nScene: Plain beige background,\n%s." % (KOPF, WER, anzug, HALTUNG)
        c = dict(cfg, loras=LORAS, mode="sprite", sprite_src="t2i", width=880, height=1328, negative_prompt="", st_set=ORDNER,
                 st_rembg=False, st_crop=False)
        wart.append(post(COMFY + "/prompt", {"prompt": studio.build_graph(c, p, k, SEEDS[0])})["prompt_id"])
    for n, seed in enumerate(SEEDS, 1):
        c = dict(cfg, loras=LORAS, mode="sprite", sprite_src="t2i", width=1536, height=864, negative_prompt="", st_set=ORDNER,
                 st_rembg=False, st_crop=False)
        wart.append(post(COMFY + "/prompt", {"prompt": studio.build_graph(c, "8k, photorealistic wide establishing shot of " + BUEHNE + ".", "buehne_%d" % n, seed)})["prompt_id"])
    print("eingereiht", len(wart), flush=True)
    fehler, ende = 0, time.time() + 1500
    while wart and time.time() < ende:
        time.sleep(3)
        for i in list(wart):
            with urllib.request.urlopen(COMFY + "/history/" + i, timeout=30) as f:
                r = json.loads(f.read()).get(i)
            if r:
                fehler += r.get("status", {}).get("status_str") != "success"
                wart.remove(i)
    print("offen", len(wart), "fehler", fehler)


if __name__ == "__main__":
    main()
