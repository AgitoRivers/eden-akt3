# -*- coding: utf-8 -*-
r"""Nachtfassung eines vorhandenen Hintergrunds per Krea2-Edit (25.10.2026): gleiche Komposition, andere Beleuchtung.

    python kabine_nacht.py 4          4 Varianten -> ST\backgrounds\_varianten\eden_rise_duc_cabin_night_v1..4.png
    python kabine_nacht.py --waehle 2 Variante 2 -> ST\backgrounds\eden_rise_duc_cabin_night.png

Quelle ist der Tag-Hintergrund eden_rise_duc_cabin.png. Graph wie Prompt Studio i2i (Krea2EditModelPatch +
Krea2EditGroundedEncode), Referenz ueber LoadImage aus dem ComfyUI-input-Ordner."""
import os, random, shutil, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import item_bilder as ib

ST_BG = r"X:\AI\SillyTavern3\SillyTavern-Launcher\SillyTavern\data\default-user\backgrounds"
QUELLE = os.path.join(ST_BG, "eden_rise_duc_cabin.png")
INPUT = r"X:\AI\ComfyUI_krea2\ComfyUI\input"
DATEI = "eden_rise_duc_cabin_night"
PROMPT = ("Change this exact room to night. Keep the room, the furniture, the boxing gloves, the sea chest, the bed, the "
          "desk, the map and every object exactly where they are. Only change the lighting: the two portholes now show "
          "a dark night sea under a black starry sky, the ceiling light is off, the room is lit only by the warm glow of "
          "the desk lamp and the blue glow of the smartphone on the desk, deep soft shadows, cosy and quiet night "
          "atmosphere, photorealistic")


def graph(seed, ordner, name):
    p = ib.NSFW_PROFIL
    g = {
        "1": {"class_type": "UNETLoader", "inputs": {"unet_name": p["unet"], "weight_dtype": "default"}},
        "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": p["clip"], "type": "krea2", "device": "default"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": ib.VAE}},
        "10": {"class_type": "EmptySD3LatentImage", "inputs": {"width": 1664, "height": 928, "batch_size": 1}},
        "20": {"class_type": "LoadImage", "inputs": {"image": os.path.basename(QUELLE)}},
        "21": {"class_type": "ImageScale", "inputs": {"upscale_method": "area", "width": 1664, "height": 928,
                                                      "crop": "center", "image": ["20", 0]}},
        "22": {"class_type": "VAEEncode", "inputs": {"pixels": ["21", 0], "vae": ["3", 0]}},
    }
    model, clip = ["1", 0], ["2", 0]
    for i, (lora, st) in enumerate(p["loras"]):
        k = "L%d" % i
        g[k] = {"class_type": "LoraLoader", "inputs": {"model": model, "clip": clip, "lora_name": lora,
                                                       "strength_model": st, "strength_clip": st}}
        model, clip = [k, 0], [k, 1]
    g["23"] = {"class_type": "Krea2EditModelPatch", "inputs": {"model": model, "source_latent": ["22", 0], "vae": ["3", 0],
                                                               "source_image": ["21", 0], "ref_boost": 1.0}}
    enc = {"clip": clip, "image": ["21", 0], "grounding_px": 768}
    g["24"] = {"class_type": "Krea2EditGroundedEncode", "inputs": dict(enc, prompt=PROMPT)}
    g["25"] = {"class_type": "Krea2EditGroundedEncode", "inputs": dict(enc, prompt="")}
    g["26"] = {"class_type": "KSamplerAdvanced", "inputs": {
        "add_noise": "enable", "noise_seed": seed, "steps": p["steps"], "cfg": 1.0, "sampler_name": "euler",
        "scheduler": "simple", "start_at_step": 0, "end_at_step": 10000, "return_with_leftover_noise": "disable",
        "model": ["23", 0], "positive": ["24", 0], "negative": ["25", 0], "latent_image": ["10", 0]}}
    g["30"] = {"class_type": "VAEDecode", "inputs": {"samples": ["26", 0], "vae": ["3", 0]}}
    g["9"] = {"class_type": "DucSave", "inputs": {"images": ["30", 0], "save_path": ordner, "filename_prefix": name,
                                                  "use_input_filename": False, "image_format": "PNG", "jpg_quality": 95,
                                                  "counter_style": "NONE", "show_preview": False, "overwrite": True}}
    return g


def main():
    var = os.path.join(ST_BG, "_varianten")
    os.makedirs(var, exist_ok=True)
    if "--waehle" in sys.argv:
        k = sys.argv[sys.argv.index("--waehle") + 1]
        shutil.copy2(os.path.join(var, "%s_v%s.png" % (DATEI, k)), os.path.join(ST_BG, DATEI + ".png"))
        print("uebernommen: Variante %s -> %s.png" % (k, DATEI))
        return
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    shutil.copy2(QUELLE, os.path.join(INPUT, os.path.basename(QUELLE)))
    ib.NSFW_PROFIL["loras"] = [("Krea_Real3.safetensors", 0.7)]
    auftraege = [("v%d" % k, ib.post("/prompt", {"prompt": graph(random.randint(1, 2 ** 31), var, "%s_v%d" % (DATEI, k))})["prompt_id"])
                 for k in range(1, n + 1)]
    ib.warten(auftraege, lambda v: print("fertig:", v))
    print("Varianten in", var)


if __name__ == "__main__":
    main()
