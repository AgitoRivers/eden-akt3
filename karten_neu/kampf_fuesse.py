# -*- coding: utf-8 -*-
r"""Kampf-Posen ohne Fuesse neu erzeugen (Duc 30.10.2026): Krea-Edit mit der eigenen Pose als Vorlage, die Figur steht klein auf heller Leinwand mit
Platz nach unten. Graph aus Prompt Studio (build_graph), Studio-Einstellungen bleiben unberuehrt. Schreibt nur in den Testordner, nie ins Spiel.

    python karten_neu\kampf_fuesse.py --test             Grundposen von Mr. White, Paparazzo, Yasin
    python karten_neu\kampf_fuesse.py --alle             alle POSEN, ohne die schon vorhandenen
    --varianten 3

Ablage: output\expressions\_fuesse_neu\<Name>\<pose>.png, <pose>-1.png ... und Abnahme docs\abnahme\fuesse\spec.json.
Regeln: X:\AI\PromptStudio\KREA_LEITFADEN.md, Abschnitt 6.
"""
import io, json, os, random, sys, time, urllib.request
from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, r"X:\AI\PromptStudio")
EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = r"X:\AI\ComfyUI_krea2\ComfyUI\output"
EXPR = os.path.join(OUT, "expressions")
ORDNER = "_fuesse_neu"
PS, COMFY = "http://127.0.0.1:8301", "http://127.0.0.1:8189"
W, H, SKALA = 1024, 1328, 0.6
POSEN = {"AgentAlpha": "idle,enraged,guard,heavy_attack,hurt,victory,weakened", "YasinDrone": "attack,enraged,heavy_attack,victory,weakened,windup",
         "Paparazzo": "idle,enraged,hurt,victory,weakened", "MaxwellSteward": "enraged,heavy_attack,hurt,victory", "Alon": "enraged,victory,weakened",
         "ThiefAlpha": "enraged,guard", "Bibi": "guard", "Heinrich": "enraged"}
TEST = {"AgentAlpha": "idle", "Paparazzo": "idle", "YasinDrone": "attack"}
WER = {"AgentAlpha": "silver-haired man with thin slim black leather dress gloves (never boxing gloves) in a sharp white tailored suit, black shirt, white tie, white suit trousers and polished black leather shoes",
       "YasinDrone": "dark-haired man in an open white linen shirt, beige linen shorts, bare legs and white sneakers, holding a drone remote control. A dark grey quadcopter drone hovers near him exactly as in the reference, solid, opaque and sharply in focus, the whole drone inside the image",
       "Paparazzo": "middle-aged man with a moustache in a black leather jacket, grey t-shirt, press badge, blue jeans and brown leather shoes, holding a camera",
       "MaxwellSteward": "tall muscular bald black man in a white polo shirt, navy shorts, bare legs and white sneakers",
       "Alon": "man in black futuristic body armour, black trousers and white sneakers, holding a white ray gun",
       "ThiefAlpha": "man with a shaved head in a black leather jacket, black hoodie, black jeans and black boots, holding a crowbar",
       "Bibi": "young blonde woman in a red jacket, black top, red shorts with a grenade belt, bare legs and black lace-up combat boots",
       "Heinrich": "tanned man in an open white shirt, cream shorts, bare legs and white loafers"}
PROMPT = ("Edit this photo. Keep exactly the same {wer}, with the same face, the same outfit, the same colours and exactly the same pose as in the reference. "
          "Complete the figure: The camera is further away, so the whole body is visible from the top of the head down to the soles of BOTH shoes, with both feet complete and on the ground. "
          "Wide empty floor below the feet and wide empty space all around, nothing touches the image edges. Plain light background, soft even light. "
          "There is only ONE single figure in the image. No glow, no fire, no sparks, no motion streaks.")


def post(url, d):
    r = urllib.request.Request(url, data=json.dumps(d).encode(), headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(r, timeout=60) as f:
        return json.loads(f.read())


def vorlage(name, pose):
    q = Image.open(os.path.join(EXPR, "combat", name, pose + ".png")).convert("RGBA")
    q = q.crop(q.getchannel("A").getbbox())
    q.thumbnail((int(W * SKALA), int(H * SKALA)))
    bild = Image.new("RGBA", (W, H), (232, 228, 220, 255))
    bild.alpha_composite(q, ((W - q.width) // 2, int(H * 0.04)))     # oben, damit unten Platz fuer die Beine bleibt
    d = os.path.join(OUT, "kampf_ref")
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, "fuss_%s_%s.png" % (name, pose))
    bild.convert("RGB").save(p)
    return p


def main():
    import studio
    n_var = int(sys.argv[sys.argv.index("--varianten") + 1]) if "--varianten" in sys.argv else 3
    with urllib.request.urlopen(PS + "/api/state", timeout=30) as f:
        cfg = dict(json.loads(f.read())["cfg"])
    plan = TEST if "--test" in sys.argv else POSEN
    jobs = [(n, p) for n, ps in plan.items() for p in ps.split(",")]
    wart, spec = {}, []
    for name, pose in jobs:
        ziel = os.path.join(EXPR, ORDNER, name)
        schon = [f for f in os.listdir(ziel) if f.startswith(pose) and f.endswith(".png")] if os.path.isdir(ziel) else []
        ref = vorlage(name, pose)
        c = dict(cfg, loras=[], mode="sprite", sprite_src="i2i", ref_image=ref, ref_mode="full", ref_boost_mode="off", ref_boost_value=4, width=W, height=H,
                 st_set=ORDNER + "\\" + name, st_rembg=True, st_crop=True)
        for k in range(max(0, n_var - len(schon))):
            g = studio.build_graph(c, PROMPT.format(wer=WER[name]), pose, random.randint(1, 2 ** 31))
            wart[post(COMFY + "/prompt", {"prompt": g})["prompt_id"]] = (name, pose)
    print("in der Warteschlange:", len(wart))
    ende = time.time() + 3000
    fehler = 0
    while wart and time.time() < ende:
        time.sleep(5)
        for i, j in list(wart.items()):
            with urllib.request.urlopen(COMFY + "/history/" + i, timeout=30) as f:
                h = json.loads(f.read()).get(i)
            if h:
                ok = h.get("status", {}).get("status_str")
                if ok != "success":
                    fehler += 1
                    print("FEHLER", j, ok)
                del wart[i]
    print("offen:", len(wart), "Fehler:", fehler)
    for name, pose in jobs:
        ziel = os.path.join(EXPR, ORDNER, name)
        for f in sorted(os.listdir(ziel)) if os.path.isdir(ziel) else []:
            if f == pose + ".png" or (f.startswith(pose + "-") and f.endswith(".png")):
                spec.append({"id": "%s_%s" % (name, f[:-4]), "titel": "%s: %s" % (name, f[:-4]), "bild": os.path.join(ziel, f),
                             "vergleich": os.path.join(EXPR, "combat", name, pose + ".png"), "soll": "Beide Füße da, Pose und Gesicht wie im Original"})
    d = os.path.join(EDEN, "docs", "abnahme", "fuesse")
    os.makedirs(d, exist_ok=True)
    json.dump({"id": "fuesse", "titel": "Posen ohne Füße", "hinweis": "Je Pose bis zu drei Varianten, daneben das Original. Eine je Pose auswählen.", "items": spec},
              open(os.path.join(d, "spec.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Spec:", len(spec))


if __name__ == "__main__":
    main()
