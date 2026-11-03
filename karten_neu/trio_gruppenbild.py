# -*- coding: utf-8 -*-
r"""Gruppenbild Red Trio (Duc 31.10.2026): Foto fuer die Wand in Danzels Laden. Krea-Edit aus einer Collage ihrer Sprites, damit die Gesichter bleiben.

    trio_gruppenbild.py [anzahl]   -> output\expressions\_trio_gruppe\gruppe(-N).png
"""
import json, os, random, sys, time, urllib.request

from PIL import Image

sys.path.insert(0, r"X:\AI\PromptStudio")
FIG = r"X:\AI\Eden\module\eden_rise\figuren"
OUT = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions"
ORDNER = "_trio_gruppe"
PS, COMFY = "http://127.0.0.1:8301", "http://127.0.0.1:8189"
W, H = 1536, 864
PROMPT = ("Edit this photo. Keep exactly the same three people from left to right with the same faces, the same hair and the same clothes: "
          "the young blonde woman in a red jacket, black top and red shorts with the small black plush lion on her belt, "
          "the silver-haired man with round red sunglasses, cross earrings, a dark red double-breasted suit and black leather gloves, "
          "and the young dark-haired woman in a dark red suit with black shirt, with her headset around her neck. "
          "They are three close friends in one casual group photograph, standing shoulder to shoulder, the man in the middle with one arm around each woman, "
          "all three laughing and looking straight at the camera. Warm late afternoon sun on an old stone piazza in a Corsican village behind them, "
          "present-day contemporary, a real snapshot from a phone. Exactly three people in the image, their heads and shoulders fully inside the frame.")


def post(url, d):
    r = urllib.request.Request(url, data=json.dumps(d).encode(), headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(r, timeout=60) as f:
        return json.loads(f.read())


def collage():
    bild = Image.new("RGB", (W, H), (226, 204, 176))
    for i, name in enumerate(("Bibi", "Danzel", "Charly")):
        q = Image.open(os.path.join(FIG, name, "joy.png")).convert("RGB")
        q = q.resize((int(q.width * H / q.height), H), Image.LANCZOS)
        rand = (q.width - W // 3) // 2
        bild.paste(q.crop((rand, 0, rand + W // 3, H)), (i * W // 3, 0))
    d = os.path.join(OUT, ORDNER, "_ref")
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, "collage.png")
    bild.save(p)
    return p


def main():
    import studio
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    with urllib.request.urlopen(PS + "/api/state", timeout=30) as f:
        cfg = dict(json.loads(f.read())["cfg"])
    ref = collage()
    c = dict(cfg, loras=[], mode="sprite", sprite_src="i2i", ref_image=ref, ref_mode="full", ref_boost_mode="off", ref_boost_value=4, width=W, height=H,
             st_set=ORDNER, st_rembg=False, st_crop=False)
    wart = [post(COMFY + "/prompt", {"prompt": studio.build_graph(c, PROMPT, "gruppe", random.randint(1, 2 ** 31))})["prompt_id"] for _ in range(n)]
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
    print("offen", len(wart), sorted(os.listdir(os.path.join(OUT, ORDNER))))


if __name__ == "__main__":
    main()
