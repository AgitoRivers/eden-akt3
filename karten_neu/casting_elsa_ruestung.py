# -*- coding: utf-8 -*-
r"""Elsa, Kampfruestung fuer die Belagerung (Duc 01.11.2026 ueber die Story-Sitzung): drei Richtungen, je 2 Seeds. Eigenes Set, im Spiel aendert sich nichts.
Chiara bleibt hell mit fliegendem Pferdeschwanz, Elsa soll dunkel und kantig wirken und auch als Silhouette anders sein. Nicht ganz in Schwarz wie Mr. Whites Agenten.
Gesicht, Haar und LoRAs aus Yacht_Elsa (Set Standard).

    casting_elsa_ruestung.py   -> output\expressions\_casting_elsa_ruestung\<a|b|c>\neutral(-1).png

Laeuft ueber studio.build_graph, die Studio-Einstellungen bleiben unberuehrt.
"""
import json, sys, time, urllib.request

sys.path.insert(0, r"X:\AI\PromptStudio")
ORDNER = "_casting_elsa_ruestung"
PS, COMFY = "http://127.0.0.1:8301", "http://127.0.0.1:8189"
MODELL = {"unet": "krea2_turbo_fp8_scaled.safetensors", "clip": "qwen3vl_4b_fp8_scaled.safetensors"}
LORAS = [{"name": "Krea_Real3.safetensors", "strength": 0.7}, {"name": "Krea_Lenovo.safetensors", "strength": 0.7},
         {"name": "Krea_Redux.safetensors", "strength": 0.5}]
SEEDS = (521903, 704416)
UNTEN = "dark navy cargo uniform trousers tucked into black lace-up tactical boots, a black duty belt with a radio clipped to it, a black service pistol in a closed holster on her right thigh"
# Variante: (Haar sichtbar, Kleidung)
VARIANTEN = {
    # Entwurf der Story-Sitzung: Einsatzhelm, unter dem die Haare fast ganz verschwinden
    "a": ("almost all of her hair hidden under the helmet, only a few honey blonde strands at her temples",
          "a matte black full-cut tactical helmet with a chin strap, a black protective vest with a small gold badge on the chest, a long-sleeved dark navy uniform shirt, black gloves, black knee pads, " + UNTEN),
    # Die Vorschrift als Silhouette: Kepi und langer Mantel, ganz anders als Chiara
    "b": ("her honey blonde hair pinned tightly under the kepi, none of it loose",
          "a stiff dark navy gendarmerie kepi with a flat round top and a gold band, a long heavy dark navy double-breasted greatcoat reaching below her knees, buttoned to the neck, wide squared shoulders with gold epaulettes, a wide black belt worn over the coat, black gloves, " + UNTEN),
    # Kantig und breit: Entermontur der Kuestenwache mit harten Platten
    "c": ("her honey blonde hair in a tight flat bun at the nape of her neck, none of it loose",
          "a dark navy beret with a small gold badge, a dark navy coast guard boarding suit with a high rigid collar, large square hard navy plates on both shoulders, a boxy square navy armour plate over the chest and stomach with a small gold badge, navy forearm guards, black gloves, navy knee plates, " + UNTEN),
}


def prompt(v):
    haar, kleidung = VARIANTEN[v]
    return ("photorealistic, front view, direct gaze, Shot on an iPhone, grainy amateur photo, realistic smartphone photography, full body shot from head to feet, one single woman alone in the frame, "
            "her whole body in full view, head and boots inside the frame,\nSubject: 1girl, blue eyes,\nHair: %s,\nWearing: %s,\nScene: Plain beige background, She stands square to the camera with both arms "
            "loose at her sides, feet shoulder-width apart, legs straight, standing at attention,\nA serious composed face, jaw set, a woman who follows every rule." % (haar, kleidung))


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
                h = json.loads(f.read()).get(i)
            if h:
                wart.remove(i)
    print("offen", len(wart))


if __name__ == "__main__":
    main()
