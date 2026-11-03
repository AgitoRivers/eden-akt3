# -*- coding: utf-8 -*-
r"""Casting Bonaventure, zweite Runde (Duc 01.11.2026: Farben in Ordnung, aber zu sehr Anime). Echte Maenner in Purpur und Gold, das Komische kommt aus dem Ernst, nur die Blechkrone bleibt uebertrieben.

    casting_bonaventure_2.py   -> output\expressions\_casting_bonaventure_2\<a|b|c>\neutral(-1).png

Laeuft ueber studio.build_graph, die Studio-Einstellungen bleiben unberuehrt.
"""
import json, sys, time, urllib.request

sys.path.insert(0, r"X:\AI\PromptStudio")
ORDNER = "_casting_bonaventure_2"
PS, COMFY = "http://127.0.0.1:8301", "http://127.0.0.1:8189"
MODELL = {"unet": "krea2_turbo_fp8_scaled.safetensors", "clip": "qwen3vl_4b_fp8_scaled.safetensors"}
LORAS = [{"name": "Krea_Real3.safetensors", "strength": 0.7}, {"name": "Krea_Lenovo.safetensors", "strength": 0.7},
         {"name": "Krea_Redux.safetensors", "strength": 0.5}]
SEEDS = (193377, 458820)
UNTEN = "a blue and white striped sailor shirt, worn khaki canvas breeches, tall black leather boots, a plain broad cutlass in a worn scabbard at his hip, a small purple flag folded and tucked into his belt"
# Duc 01.11.: Wahl C2, keine Blechkrone, schwarze Stiefel, alte Goldmuenze als Amulett
KRONE = "a faded purple tricorn hat, an old worn gold coin on a thin leather cord as an amulet around his neck, resting on the striped shirt"
# Variante: (Wer, Koerper, Gesicht, Mantel)
VARIANTEN = {
    # Der Hochstapler: ein normaler dicker Mann in einem Mantel, den er selbst flickt
    "a": ("Bonaventure, a 50-year-old Marseille boat captain", "a stocky man of average height with a real heavy belly, thick forearms, ordinary proportions",
          "a broad sun-tanned weathered face, a big fleshy nose, tired proud dark eyes, a large thick dark moustache with grey in it, a few days of stubble",
          "a worn royal purple velvet frock coat with faded gold trim, mended in several places with visible stitching, tarnished gold epaulettes of normal size"),
    # Der Don Quixote: lang und duenn, das Gegenteil von Minicu
    "b": ("Bonaventure, a 58-year-old Marseille sea captain", "a very tall gaunt thin man with long limbs, narrow shoulders, big bony hands, ordinary human proportions",
          "a long hollow sun-tanned face, a high forehead, a thin hooked nose, deep-set bright eyes, a thin curled grey moustache and a small pointed grey beard",
          "a worn royal purple velvet frock coat with faded gold trim, a size too wide and hanging loose on his thin frame, tarnished gold epaulettes of normal size"),
    # Der Schauspieler: gut aussehend und ueber seinen Zenit, spielt seine Rolle immer
    "c": ("Bonaventure, a 44-year-old Marseille sea captain", "a tall broad-shouldered man going a little soft around the middle, ordinary proportions",
          "a handsome sun-tanned face past its best, a strong nose, theatrical bright eyes, a neat curled dark moustache with waxed tips, long dark curls with some grey",
          "a well-cut royal purple velvet frock coat with bright polished gold trim, carefully brushed, gold epaulettes of normal size"),
}


def prompt(v):
    wer, koerper, gesicht, mantel = VARIANTEN[v]
    return ("photorealistic, front view, direct gaze, Shot on an iPhone, grainy amateur photo, realistic smartphone photography, full body shot from head to feet, one single man alone in the frame, "
            "his whole body in full view, head and boots inside the frame, a real person,\nSubject: %s,\nBody: %s,\nFace: %s,\nSkin: deep sun-tanned Mediterranean skin,\nWearing: %s, %s, %s,\n"
            "Scene: Plain beige background, He stands square to the camera, chest out, one hand resting on the hilt of the cutlass, the other arm loose, feet shoulder-width apart, legs straight,\n"
            "A dignified, completely serious face, a man who believes he is a king." % (wer, koerper, gesicht, KRONE, mantel, UNTEN))


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
        c = dict(cfg, loras=LORAS, mode="sprite", sprite_src="t2i", width=880, height=1328, negative_prompt="", st_set="%s/%s" % (ORDNER, v), st_rembg=True, st_crop=False, **MODELL)
        for s in SEEDS:
            wart.append(post(COMFY + "/prompt", {"prompt": studio.build_graph(c, prompt(v), "neutral", s)})["prompt_id"])
    print("eingereiht", len(wart), flush=True)
    ende = time.time() + 280
    while wart and time.time() < ende:
        time.sleep(3)
        for i in list(wart):
            with urllib.request.urlopen(COMFY + "/history/" + i, timeout=30) as f:
                if json.loads(f.read()).get(i):
                    wart.remove(i)
    print("offen", len(wart))


if __name__ == "__main__":
    main()
