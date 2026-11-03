# -*- coding: utf-8 -*-
r"""Foto-Andenken mit den echten Figuren (26.10.2026, Duc: "Holm soll auf dem Bild sein", "nimm ihren Prompt").

Rendert das Foto selbst mit dem Prompt-Studio-Preset der Figur (sprite_prompt, Tags des Sets, Identitaets-LoRA, Tag-LoRAs)
direkt ueber ComfyUI - Prompt Studio wird nur gelesen, nie umgestellt (andere Sitzungen arbeiten darin). Danach legt
--montieren das Foto als Abzug (Holm) oder auf ein Handy-Display (Rosi, Megan) auf den Leinen-Look der Item-Bilder.

    andenken_fotos.py                  4 Fotos je Andenken -> module\eden_rise\items\_gross\_roh\<id>_r<k>.png
    andenken_fotos.py --montieren      daraus <id>_v<k>.png (1024er, Leinen) + Thumbnails in items\_varianten
    andenken_fotos.py holms_foto ...   nur diese
Uebernehmen wie immer: Item_Bilder_EdenRise.bat <id> --waehle <k>.
"""
import json, os, random, sys, time, urllib.request

from PIL import Image, ImageDraw, ImageFilter

sys.stdout.reconfigure(encoding="utf-8")
EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PS = r"X:\AI\PromptStudio"
COMFY = "http://127.0.0.1:8189"
ITEMS = os.path.join(EDEN, "module", "eden_rise", "items")
GROSS = os.path.join(ITEMS, "_gross")
ROH = os.path.join(GROSS, "_roh")
VAR = os.path.join(ITEMS, "_varianten")
FILM = "an old faded film photograph from the 1990s, grainy colour film, slightly washed-out warm colours"
POLAROID = "an instant Polaroid photo taken with a harsh direct flash, soft faded instant-film colours, slight vignette"

FOTOS = {
    "holms_foto": {
        "preset": "Yacht_Holm", "set": "Night Watch", "outfit": "holm_night_watch", "form": "abzug", "w": 1216, "h": 832,
        "ersetzen": [("Shot on an iPhone, grainy amateur photo, realistic smartphone photography", FILM),
                     ("full body shot from head to knees, direct gaze", "medium shot from the thighs up, looking into the camera"),
                     ("her whole body in full view, head and knees inside the frame", "a ship's mast and the fjord behind her"),
                     ("Subject: female", "Subject: a woman in her early thirties")],
        "setting": "standing on the rusty deck of an old red cargo freighter moored in a grey Norwegian fjord harbour at "
                   "Bergen, low clouds over dark green mountains, a worn ship's railing and a crane behind her",
        "expression": "a proud, slightly nervous smile of a brand-new young captain",
    },
    # Runde 4 (Duc 26.10.2026): nur die LoRA-Einstellungen der Presets, eigener natuerlicher Prompt nach der Story,
    # das Bild ist selbst das Selfie bzw. der Screenshot (kein Rahmen)
    "rosis_foto": {
        "preset": "Yacht_Rosi", "form": "roh", "w": 1024, "h": 1024,
        # Runde 5 (Duc 26.10.2026): mehr Dekollete, fast nackt
        "prompt": "A real amateur mirror selfie taken with a smartphone in a tiny steamy crew bathroom on a yacht. A young "
                  "Italian woman with light blue eyes, wet dark brown hair with straight bangs, fresh out of the shower, "
                  "holds her phone up in front of a fogged-up mirror with a wiped clear patch. She is almost naked, only "
                  "a small white towel held loosely at her hips with one hand, her bare breasts with deep cleavage "
                  "barely half covered by her forearm, water drops running down her chest and stomach, a cheeky "
                  "embarrassed grin, cheeks flushed. Small ceiling lamp, tiled wall, a red bandana hanging on a hook. "
                  "Realistic iPhone photo, slightly grainy, natural skin texture, no makeup.",
    },
    "megan_screenshot": {
        "preset": "Yacht_Megan", "form": "roh", "w": 1024, "h": 1024,
        # Runde 5 (Duc 26.10.2026): Event wird umgeschrieben - Megan schickt ein Nackt-Spiegelselfie aus dem Schlafzimmer
        "prompt": "A real amateur mirror selfie taken with a smartphone in an elegant bedroom of a penthouse above "
                  "Monaco at night. Female woman actress Megan Fox with light green eyes, very pale skin, long layered "
                  "chestnut-red hair falling past her shoulders, stands naked in front of a tall mirror, holding her "
                  "phone at chest height, wearing nothing but a thin gold chain with a small golden anchor pendant. "
                  "A dark wood bed with rumpled silk sheets behind her, a warm bedside lamp, the harbour lights of "
                  "Port Hercule through the window. A confident half smile, one eyebrow raised. Realistic iPhone "
                  "photo, slightly grainy, natural skin texture.",
    },
}
ALT_RUNDE3 = {
    # Runde 3 (verworfen 26.10.2026, passte nicht zur Story): Rosi oben ohne im Maschinenraum, Megan Domina beim Maskenball
    "rosis_foto": {
        "preset": "Yacht_Rosi", "set": "Nude", "form": "polaroid", "w": 1024, "h": 1024,
        # "overall" zieht das Modell immer zur Latzhose mit Traegern - deshalb nur Arbeitshose
        "outfit_text": "topless, bare naked breasts with nipples fully exposed, her chest and shoulders completely bare, "
                       "wearing only low-slung navy work trousers with a black leather tool belt, a red bandana tied on "
                       "top of her head, oil smudges on her skin and breasts",
        "ersetzen": [("Shot on an iPhone, grainy amateur photo, realistic smartphone photography", POLAROID),
                     ("full body shot from head to knees", "shot from the hips up"),
                     ("her whole body in full view, head and knees inside the frame", "")],
        "setting": "in a cramped yacht engine room, pipes and a big diesel generator behind her, warm yellow work light",
        "expression": "a cheeky embarrassed grin, biting her lower lip, cheeks flushed",
    },
    "megan_screenshot": {
        "preset": "Yacht_Megan", "set": "Domina", "outfit": "goth_vinyl_white", "form": "polaroid", "w": 1024, "h": 1024,
        "outfit_zusatz": ", an ornate golden Venetian masquerade mask with gold filigree covering her upper face, her green "
                         "eyes visible through it",
        "ersetzen": [("Shot on an iPhone, grainy amateur photo, realistic smartphone photography", POLAROID),
                     ("full body shot from head to knees", "shot from the thighs up"),
                     ("her whole body in full view, head and knees inside the frame", "")],
        "setting": "at a glamorous masquerade ball in a Monaco palace hall, crystal chandeliers and candle light, other "
                   "masked guests blurred far behind her",
        "expression": "a knowing red-lipped smile",
    },
}


def lesen(name):
    return json.load(open(os.path.join(PS, name), encoding="utf-8"))


def prompt_bauen(f):
    preset = lesen("presets.json")[f["preset"]]
    if f.get("prompt"):                          # freier Prompt: nur die LoRA-Einstellungen des Presets
        return f["prompt"], preset["negative_prompt"], [(l["name"], l["strength"]) for l in preset["loras"]]
    sp = lesen("set_presets.json")["%s|%s" % (f["preset"], f["set"])]
    tags = {t["name"]: t for t in lesen("studio-config.json")["tags"]}
    karten = {c["name"]: c["prompt"] for c in lesen("decks.json")["outfit"]}
    an = [tags[n] for n in sp["tags"] if n in tags]
    teil = lambda cat: ", ".join(t["prompt"].rstrip(", ") for t in an if t.get("cat") == cat)
    outfit = f.get("outfit_text") or karten[f["outfit"]].rstrip(", ")
    p = preset["sprite_prompt"]
    for a, b in f["ersetzen"]:
        assert a in p, (f["preset"], a)
        p = p.replace(a, b)
    werte = {"tags_action": "", "tags_body": teil("body"), "tags_haircolor": teil("haircolor"),
             "tags_hairstyle": teil("hairstyle"), "tags_hair": teil("hair"), "tags_skin": teil("skin"),
             "tags_face": teil("face"), "outfit": outfit + f.get("outfit_zusatz", ""), "setting": f["setting"], "st": "",
             "expression": f["expression"], "look": "", "tags_photo": teil("photo")}
    for k, v in werte.items():
        p = p.replace("{%s}" % k, v)
    loras = [(l["name"], l["strength"]) for l in preset["loras"]]
    for t in an:
        loras += [(l["name"], l["strength"]) for l in t.get("loras") or [] if l["name"] not in dict(loras)]
    return p, preset["negative_prompt"], loras


def graph(prompt, negativ, loras, w, h, name, seed):
    cfg = lesen("studio-config.json")
    g = {"1": {"class_type": "UNETLoader", "inputs": {"unet_name": cfg["unet"], "weight_dtype": "default"}},
         "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": cfg["clip"], "type": "krea2", "device": "default"}},
         "3": {"class_type": "VAELoader", "inputs": {"vae_name": cfg["vae"]}}}
    model, clip = ["1", 0], ["2", 0]
    for i, (lora, st) in enumerate(loras):
        g["L%d" % i] = {"class_type": "LoraLoader", "inputs": {"model": model, "clip": clip, "lora_name": lora,
                                                              "strength_model": st, "strength_clip": st}}
        model, clip = ["L%d" % i, 0], ["L%d" % i, 1]
    g.update({
        "4": {"class_type": "CLIPTextEncode", "inputs": {"text": prompt, "clip": clip}},
        "5": {"class_type": "CLIPTextEncode", "inputs": {"text": negativ, "clip": clip}},
        "6": {"class_type": "EmptySD3LatentImage", "inputs": {"width": w, "height": h, "batch_size": 1}},
        "7": {"class_type": "KSampler", "inputs": {"seed": seed, "steps": cfg["steps"], "cfg": cfg["cfg"],
                                                   "sampler_name": cfg["sampler"], "scheduler": cfg["scheduler"],
                                                   "denoise": 1.0, "model": model, "positive": ["4", 0],
                                                   "negative": ["5", 0], "latent_image": ["6", 0]}},
        "8": {"class_type": "VAEDecode", "inputs": {"samples": ["7", 0], "vae": ["3", 0]}},
        "9": {"class_type": "DucSave", "inputs": {"images": ["8", 0], "save_path": ROH, "filename_prefix": name,
                                                  "use_input_filename": False, "image_format": "PNG", "jpg_quality": 95,
                                                  "counter_style": "NONE", "show_preview": False, "overwrite": True}}})
    return g


def rendern(ids, n=4):
    os.makedirs(ROH, exist_ok=True)
    offen = {}
    for iid in ids:
        f = FOTOS[iid]
        p, neg, loras = prompt_bauen(f)
        print("%s: %s\n   LoRAs %s" % (iid, p.replace("\n", " ")[:400], loras))
        for k in range(1, n + 1):
            req = urllib.request.Request(COMFY + "/prompt", headers={"Content-Type": "application/json"}, data=json.dumps(
                {"prompt": graph(p, neg, loras, f["w"], f["h"], "%s_r%d" % (iid, k), random.randint(1, 2 ** 31))}).encode())
            offen["%s_r%d" % (iid, k)] = json.loads(urllib.request.urlopen(req, timeout=30).read())["prompt_id"]
    while offen:
        time.sleep(3)
        for name, pid in list(offen.items()):
            h = json.loads(urllib.request.urlopen(COMFY + "/history/" + pid, timeout=30).read())
            if pid in h and h[pid].get("status", {}).get("completed"):
                print("fertig:", name, flush=True)
                offen.pop(name)


# ------------------------------------------------------------------ Montage auf Leinen
def leinen():
    """Leerer Leinen-Hintergrund im Look der Item-Bilder (einmal erzeugt, dann wiederverwendet)."""
    return Image.open(os.path.join(ROH, "leinen.png")).convert("RGB").resize((1024, 1024), Image.LANCZOS)


def schatten(grund, maske, versatz=(10, 16), weich=18, staerke=110):
    s = Image.new("L", grund.size, 0)
    s.paste(maske, versatz, maske)
    s = s.filter(ImageFilter.GaussianBlur(weich)).point(lambda v: v * staerke // 255)
    grund.paste(Image.new("RGB", grund.size, (40, 32, 24)), (0, 0), s)


def abzug(foto, grund, winkel):
    b = 560
    foto = foto.resize((b, round(b * foto.height / foto.width)), Image.LANCZOS)
    rand = 26
    karte = Image.new("RGB", (foto.width + 2 * rand, foto.height + 2 * rand + 18), (238, 232, 218))
    karte.paste(foto, (rand, rand))
    # vergilbt und leicht verblasst wie ein alter Abzug
    karte = Image.blend(karte, Image.new("RGB", karte.size, (226, 210, 170)), 0.12)
    maske = Image.new("L", karte.size, 255)
    karte, maske = karte.rotate(winkel, Image.BICUBIC, expand=True), maske.rotate(winkel, Image.BICUBIC, expand=True)
    pos = ((1024 - karte.width) // 2, (1024 - karte.height) // 2)
    sm = Image.new("L", (1024, 1024), 0)
    sm.paste(maske, pos)
    schatten(grund, sm.crop((0, 0, 1024, 1024)), weich=14, staerke=90)
    grund.paste(karte, pos, maske)
    return grund


def polaroid(foto, grund, winkel):
    s, rand, unten = 470, 30, 120
    seite = min(foto.size)
    foto = foto.crop(((foto.width - seite) // 2, 0, (foto.width - seite) // 2 + seite, seite)).resize((s, s), Image.LANCZOS)
    karte = Image.new("RGB", (s + 2 * rand, s + rand + unten), (241, 238, 230))
    karte.paste(foto, (rand, rand))
    maske = Image.new("L", karte.size, 255)
    karte, maske = karte.rotate(winkel, Image.BICUBIC, expand=True), maske.rotate(winkel, Image.BICUBIC, expand=True)
    pos = ((1024 - karte.width) // 2, (1024 - karte.height) // 2)
    sm = Image.new("L", (1024, 1024), 0)
    sm.paste(maske, pos)
    schatten(grund, sm, weich=14, staerke=95)
    grund.paste(karte, pos, maske)
    return grund


def handy(foto, grund, winkel):
    bw, bh, r, rahmen = 420, 860, 58, 16
    koerper = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    d = ImageDraw.Draw(koerper)
    d.rounded_rectangle([0, 0, bw - 1, bh - 1], r, fill=(22, 22, 26, 255), outline=(70, 70, 78, 255), width=3)
    sw, sh = bw - 2 * rahmen, bh - 2 * rahmen
    q = foto.width / foto.height
    if q > sw / sh:
        neu = foto.resize((round(sh * q), sh), Image.LANCZOS)
        neu = neu.crop(((neu.width - sw) // 2, 0, (neu.width - sw) // 2 + sw, sh))
    else:
        neu = foto.resize((sw, round(sw / q)), Image.LANCZOS)
        neu = neu.crop((0, 0, sw, sh))
    sm = Image.new("L", (sw, sh), 0)
    ImageDraw.Draw(sm).rounded_rectangle([0, 0, sw - 1, sh - 1], r - rahmen, fill=255)
    koerper.paste(neu, (rahmen, rahmen), sm)
    d.rounded_rectangle([bw // 2 - 52, rahmen + 12, bw // 2 + 52, rahmen + 40], 14, fill=(8, 8, 10, 255))   # Kamera-Insel
    glanz = Image.new("L", (bw, bh), 0)
    ImageDraw.Draw(glanz).polygon([(0, 0), (bw * 0.55, 0), (0, bh * 0.45)], fill=34)
    koerper.paste(Image.new("RGBA", (bw, bh), (255, 255, 255, 255)), (0, 0), Image.composite(glanz, Image.new("L", (bw, bh), 0), koerper.split()[3]))
    koerper = koerper.rotate(winkel, Image.BICUBIC, expand=True)
    pos = ((1024 - koerper.width) // 2, (1024 - koerper.height) // 2)
    sm = Image.new("L", (1024, 1024), 0)
    sm.paste(koerper.split()[3], pos)
    schatten(grund, sm, weich=20, staerke=120)
    grund.paste(koerper, pos, koerper)
    return grund


def montieren(ids):
    os.makedirs(VAR, exist_ok=True)
    for iid in ids:
        f = FOTOS[iid]
        for k in range(1, 5):
            quelle = os.path.join(ROH, "%s_r%d.png" % (iid, k))
            if not os.path.exists(quelle):
                continue
            foto = Image.open(quelle).convert("RGB")
            winkel = (-5, 4, -2, 6)[k - 1]
            if f["form"] == "roh":
                bild = foto.resize((1024, 1024), Image.LANCZOS)
            else:
                bild = {"abzug": abzug, "polaroid": polaroid, "handy": handy}[f["form"]](foto, leinen(), winkel)
            ziel = "%s_v%d" % (iid, k)
            bild.save(os.path.join(GROSS, ziel + ".png"))
            t = bild.copy()
            t.thumbnail((320, 320), Image.LANCZOS)
            t.save(os.path.join(VAR, ziel + ".webp"), "WEBP", quality=85, method=6)
            print("montiert:", ziel)


if __name__ == "__main__":
    ids = [a for a in sys.argv[1:] if not a.startswith("-")] or list(FOTOS)
    if "--montieren" in sys.argv:
        montieren(ids)
    elif "--prompt" in sys.argv:
        for iid in ids:
            print(iid, prompt_bauen(FOTOS[iid]))
    else:
        rendern(ids)
