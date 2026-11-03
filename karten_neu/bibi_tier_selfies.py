# -*- coding: utf-8 -*-
r"""Bibis Selfies mit den geretteten Tieren (Duc 02.11.2026, Wiki systeme/tierstation.md): Probe mit drei Tieren, je zwei Seeds.
Look 1:1 wie ihr Station-Set (figuren/Bibi/set3, Jen-LoRA), Tiere wie ihre Frei-Sprites, ohne Halsband.

    bibi_tier_selfies.py [hund,capybara,wolf]   -> output\expressions\_bibi_tier_selfies\<tier>_<n>.png
"""
import json, os, sys, time, urllib.request

sys.path.insert(0, r"X:\AI\PromptStudio")
PS, COMFY = "http://127.0.0.1:8301", "http://127.0.0.1:8189"
ORDNER = "_bibi_tier_selfies"
SEEDS = (240211, 771903)
LORAS = [{"name": "Krea_Real3.safetensors", "strength": 0.7}, {"name": "Krea_Lenovo.safetensors", "strength": 0.7},
         {"name": "Krea_Redux.safetensors", "strength": 0.5}, {"name": "Krea_Jen.safetensors", "strength": 0.85}]
KOPF = ("8k, Jenx, photorealistic, a candid selfie she takes herself at arm's length with a smartphone, realistic amateur iPhone photo, "
        "slightly grainy, natural light, one single woman, her face and upper body in the frame, one arm reaching towards the camera")
WER = ("A 25-year-old adult French woman, a sharp pretty face, light blue eyes, natural skin texture a real individual face, lightly sun-tanned "
       "skin from a Corsican summer, an athletic toned build, her hair is blonde, very long straight hair with blunt straight bangs and "
       "straight side locks cut at cheek height, soft natural summer makeup, glossy nude pink lips")
ANZUG = ("an open oversized black short-sleeved shirt with a big lion print worn over a metallic golden cropped top, black choker, round "
         "sunglasses pushed up in her hair, black fingerless combat gloves")
ORT = ("an old dry-stone sheep pen with half a wooden roof on a dry Corsican hillside high above a deep blue bay, straw on the ground, "
       "warm late afternoon sun, present-day contemporary")
TIERE = {
    "hund": "Right beside her face a big brindle mastiff-type dog with a broad black face, folded ears and a pink tongue is licking her ear, "
            "the dog's neck bare with smooth short fur. She squeezes one eye shut and laughs with her mouth open",
    "capybara": "A large calm reddish-brown capybara with a blunt square nose lies across her shoulders and the back of her head like a "
                "heavy fur scarf, its eyes half closed. She looks straight into the camera with a deadpan face and a tiny smile",
    "wolf": "Behind her in the straw a big grey wolf with a pale chest and a dark back lies fast asleep, curled up, its mouth a little open "
            "so the long teeth show. She leans towards the camera and grins nervously, eyebrows raised",
}


def post(url, daten):
    req = urllib.request.Request(url, data=json.dumps(daten).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())


def prompt(tid):
    return "%s,\nSubject: %s,\nWearing: %s,\nScene: %s,\n%s." % (KOPF, WER, ANZUG, ORT, TIERE[tid])


def main():
    import studio
    nur = sys.argv[1].split(",") if len(sys.argv) > 1 else list(TIERE)
    with urllib.request.urlopen(PS + "/api/state", timeout=30) as f:
        cfg = dict(json.loads(f.read())["cfg"])
    wart = []
    for tid in nur:
        for n, seed in enumerate(SEEDS, 1):
            c = dict(cfg, loras=LORAS, mode="sprite", sprite_src="t2i", width=896, height=1152, negative_prompt="", st_set=ORDNER,
                     st_rembg=False, st_crop=False)
            wart.append(post(COMFY + "/prompt", {"prompt": studio.build_graph(c, prompt(tid), "%s_%d" % (tid, n), seed)})["prompt_id"])
    print("eingereiht", len(wart), flush=True)
    fehler, ende = 0, time.time() + 1200
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
