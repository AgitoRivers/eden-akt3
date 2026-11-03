# -*- coding: utf-8 -*-
r"""Dank-Fotos der Favours (Duc 29.10.2026): je Kette ein Foto, das die Figur nach dem geglückten Finale schickt.
Prompts in werkzeuge\eden_rise\ereignisse_favours.py (FOTOS), LoRAs und Aussehen aus dem Prompt-Studio-Preset (nur
lesend, wie andenken_fotos.py). Duc will die Favours nicht vorab sehen - die Auswahl trifft die Hauptsitzung.

    favour_fotos.py                  4 Varianten je Kette -> module\eden_rise\favours\_roh\fv_<kette>_r<n>.png
    favour_fotos.py lola petru       nur diese Ketten
    favour_fotos.py --prompt lola    Prompt zeigen, nichts rendern
    favour_fotos.py --waehle lola 2  Variante 2 -> favours\fv_lola.webp (896 x 1152, ausgeliefert, in Git)
"""
import json, os, random, sys, time, urllib.request

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, os.path.join(HIER, "eden_rise"))
import andenken_fotos as AF  # noqa: E402
import ereignisse_favours as FV  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
ZIEL = os.path.join(AF.EDEN, "module", "eden_rise", "favours")
ROH = os.path.join(ZIEL, "_roh")
W, H = 896, 1152
OHNE_TAGS = ("Pubic", "Sheen", "Tan Lines", "View:", "Large")  # bekleidete Alltagsfotos: nur Aussehen
OHNE_LORAS = ("Krea_Nsfw2.safetensors",)
GANZ = ("full body shot from head to knees, ", "full body shot, ", "his whole body in full view, head and knees inside "
        "the frame,", "her whole body in full view, head and knees inside the frame,")


def prompt(kid):
    f = FV.FOTOS[kid]
    pre = AF.lesen("presets.json")[f["preset"]]
    tags = {t["name"]: t for t in AF.lesen("studio-config.json")["tags"]}
    an = [tags[n] for n in pre.get("tags_on") or [] if n in tags and not any(x in n for x in OHNE_TAGS)]
    teil = lambda cat: ", ".join(t["prompt"].rstrip(", ") for t in an if t.get("cat") == cat)
    p = pre["sprite_prompt"]
    for a, b in f.get("ersetzen", []):
        assert a in p, (kid, a)
        p = p.replace(a, b)
    for a in GANZ:
        p = p.replace(a, "")
    werte = {"tags_action": "", "tags_body": teil("body"), "tags_haircolor": teil("haircolor"),
             "tags_hairstyle": f.get("frisur") or teil("hairstyle"), "tags_hair": teil("hair"), "tags_skin": teil("skin"),
             "tags_face": teil("face"), "outfit": f["kleidung"], "setting": f["szene"] + ", " + f["ausdruck"],
             "st": "", "expression": "", "look": "", "tags_photo": ""}
    for k, v in werte.items():
        p = p.replace("{%s}" % k, v)
    zeilen = [z.strip(" ,").replace(": , ", ": ").replace(" , ", ", ") for z in p.split("\n")]
    p = "\n".join(z for z in zeilen if z and not z.endswith(":"))
    loras = [(l["name"], l["strength"]) for l in pre["loras"] if l["name"] not in OHNE_LORAS]
    for t in an:
        loras += [(l["name"], l["strength"]) for l in t.get("loras") or [] if l["name"] not in dict(loras)]
    staerke = f.get("lora_staerke") or {}             # Ducs Vorgabe je Foto, z. B. Jana: Emma_D 1.0 (29.10.2026)
    loras = [(n, staerke.get(n, s)) for n, s in loras]
    return p, pre["negative_prompt"], loras


def rendern(ids, n=4):
    os.makedirs(ROH, exist_ok=True)
    offen = {}
    for kid in ids:
        p, neg, loras = prompt(kid)
        for k in range(1, n + 1):
            name = "fv_%s_r%d" % (kid, k)
            g = AF.graph(p, neg, loras, W, H, name, random.randint(1, 2 ** 31))
            g["9"]["inputs"]["save_path"] = ROH
            req = urllib.request.Request(AF.COMFY + "/prompt", headers={"Content-Type": "application/json"},
                                         data=json.dumps({"prompt": g}).encode())
            offen[name] = json.loads(urllib.request.urlopen(req, timeout=30).read())["prompt_id"]
    print("%d Bilder eingereiht" % len(offen), flush=True)
    while offen:
        time.sleep(3)
        for name, pid in list(offen.items()):
            h = json.loads(urllib.request.urlopen(AF.COMFY + "/history/" + pid, timeout=30).read())
            if pid in h and h[pid].get("status", {}).get("completed"):
                print("fertig:", name, flush=True)
                offen.pop(name)


def waehlen(kid, n):
    from PIL import Image
    Image.open(os.path.join(ROH, "fv_%s_r%s.png" % (kid, n))).convert("RGB").save(
        os.path.join(ZIEL, "fv_%s.webp" % kid), "WEBP", quality=88, method=6)
    print("gewaehlt:", kid, n)


def main():
    a = [x for x in sys.argv[1:] if not x.startswith("-")]
    if "--waehle" in sys.argv:
        waehlen(a[0], a[1])
        return
    ids = a or list(FV.FOTOS)
    if "--prompt" in sys.argv:
        for kid in ids:
            p, _, loras = prompt(kid)
            print("== %s %s\n%s\n" % (kid, loras, p))
        return
    rendern(ids)


if __name__ == "__main__":
    main()
