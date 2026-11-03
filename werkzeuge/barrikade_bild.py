# -*- coding: utf-8 -*-
r"""Barrikade im Norden der Taktik-Karte (Duc 02.11.2026): Krea-Edit auf einem Ausschnitt der Kampfkarte, je Zustand drei Varianten.
Zu: Holz und Karren quer ueber dem Weg, Waelle 1-5. Offen: zur Seite geschoben, Welle 6 nach dem Verrat.

    python werkzeuge\barrikade_bild.py            erzeugt die Varianten und die Abnahme docs\abnahme\barrikade\spec.json
    python werkzeuge\barrikade_bild.py --aus-zu zu.png   offen neu aus dem gewaehlten "zu" (Duc 02.11.: dieselben Teile, kein Wagen), Abnahme spec_offen.json
    python werkzeuge\barrikade_bild.py --rand            offen von der leeren Karte, nur Faesser, Balken, Steine am Wegrand (offen_rand), Abnahme spec_offen.json
    python werkzeuge\barrikade_bild.py --bruch           wie --rand, Steine kleiner, Faesser gebrochen (offen_bruch)
    python werkzeuge\barrikade_bild.py --fertig zu=1 offen=0
                                                  legt die gewaehlten Varianten als Overlay ins Spiel: module\eden_rise\taktik\barrikade_<zustand>.webp

Das Overlay ist der Ausschnitt mit weichem Rand, nur um den Weg herum deckend, damit die Naht zur Karte nicht auffaellt.
Regeln: X:\AI\PromptStudio\KREA_LEITFADEN.md (positiv formulieren, Edit als Anweisung)."""
import io, json, os, random, sys, time, urllib.request
from PIL import Image, ImageDraw, ImageFilter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, r"X:\AI\PromptStudio")
EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KARTE = os.path.join(EDEN, "module", "eden_rise", "taktik", "karte_kampf.webp")
OUT = r"X:\AI\ComfyUI_krea2\ComfyUI\output"
ORDNER = "_barrikade"
PS, COMFY = "http://127.0.0.1:8301", "http://127.0.0.1:8189"
SP, ZE = 48, 32                     # Raster der Karte
BOX = (24.5, 5.75, 31.5, 11.75)     # Ausschnitt in Feldern: Mitte auf dem Weg bei der Barrikade (27,8)-(28,8)
FAKTOR = 2
GEMEINSAM = ("Edit this image. Keep the whole picture exactly the same: the same painted map style, the same houses, roofs, trees, rocks, stairs, "
             "the same warm evening light and the same colours, seen from the same high angle. ")
PROMPT = {
    "zu": GEMEINSAM + "Only add one thing: in the very centre of the image, a rough village barricade blocks the dirt road where it reaches the first houses. "
          "It is built from an old wooden cart tipped on its side, stacked wine barrels, crossed timber beams and a few heavy stones, "
          "a solid wall of wood from one house to the other, painted in the same style as the rest of the map.",
    "offen": GEMEINSAM + "Only add one thing: in the very centre of the image, the dirt road is open, and the parts of a broken village barricade lie pushed to both "
             "sides of the road: an old wooden cart tipped on its side, a few wine barrels and loose timber beams. The middle of the road is free. "
             "Painted in the same style as the rest of the map.",
}
# Duc 02.11.2026: Offen soll aus denselben Teilen bestehen wie zu (Fässer, Balken, Steine), ohne Wagen. Vorlage ist darum das gewählte Bild "zu".
PROMPT_AUS_ZU = {
    "offen_neu": GEMEINSAM + "Only change the barricade in the centre: it has been pulled apart and the dirt road is open. The same wine barrels, timber beams "
                 "and heavy stones now lie at both edges of the road, a few barrels rolled into the grass. The middle of the road is free, bare brown earth. "
                 "Painted in the same style as the rest of the map.",
}
# Der Edit auf "zu" aendert fast nichts (02.11.). Darum von der leeren Karte aus, nur die Teile beschrieben, die auch "zu" hat.
PROMPT_RAND = {
    "offen_rand": GEMEINSAM + "Only add one thing: in the very centre of the image, where the dirt road reaches the first houses, the road is open and free. "
                  "On both edges of the road lie the remains of a pulled-apart barricade: stacked wooden wine barrels on the left edge, crossed timber beams "
                  "and a few heavy pale stones on the right edge. Bare brown earth in the middle of the road. Painted in the same style as the rest of the map.",
}
# Duc 02.11.2026 zu offen_rand-1: Steine kleiner, Faesser gebrochen
PROMPT_BRUCH = {
    "offen_bruch": GEMEINSAM + "Only add one thing: in the very centre of the image, where the dirt road reaches the first houses, the road is open and free. "
                   "On both edges of the road lie the remains of a smashed barricade: broken wooden wine barrels with split staves and loose iron hoops on the "
                   "left edge, splintered timber beams and a scatter of small pale stones, each no bigger than a loaf of bread, on the right edge. "
                   "Bare brown earth in the middle of the road. Painted in the same style as the rest of the map.",
}


def post(url, d):
    r = urllib.request.Request(url, data=json.dumps(d).encode(), headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(r, timeout=60) as f:
        return json.loads(f.read())


def ausschnitt():
    k = Image.open(KARTE).convert("RGB")
    fx, fy = k.width / SP, k.height / ZE
    box = tuple(int(round(v)) for v in (BOX[0] * fx, BOX[1] * fy, BOX[2] * fx, BOX[3] * fy))
    return k, box


def vorlage():
    k, box = ausschnitt()
    a = k.crop(box)
    a = a.resize((a.width * FAKTOR // 16 * 16, a.height * FAKTOR // 16 * 16), Image.LANCZOS)
    d = os.path.join(OUT, "kampf_ref")
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, "barrikade_vorlage.png")
    a.save(p)
    return p, a.size


def erzeugen(n_var=3, aus_zu=None):
    """aus_zu: Dateiname des gewaehlten Bilds "zu" als Vorlage, dann nur die Prompts aus PROMPT_AUS_ZU."""
    import studio
    with urllib.request.urlopen(PS + "/api/state", timeout=30) as f:
        cfg = dict(json.loads(f.read())["cfg"])
    ref, (w, h) = vorlage()
    prompts = {"rand": PROMPT_RAND, "bruch": PROMPT_BRUCH}.get(aus_zu, PROMPT)
    if aus_zu and aus_zu not in ("rand", "bruch"):
        ref, prompts = os.path.join(OUT, "expressions", ORDNER, aus_zu), PROMPT_AUS_ZU
    c = dict(cfg, loras=[], mode="sprite", sprite_src="i2i", ref_image=ref, ref_mode="full", ref_boost_mode="off", ref_boost_value=4, width=w, height=h,
             st_set=ORDNER, st_rembg=False, st_crop=False)
    wart = {}
    for zustand, prompt in prompts.items():
        for _ in range(n_var):
            g = studio.build_graph(c, prompt, zustand, random.randint(1, 2 ** 31))
            wart[post(COMFY + "/prompt", {"prompt": g})["prompt_id"]] = zustand
    print("in der Warteschlange:", len(wart))
    ende = time.time() + 1800
    while wart and time.time() < ende:
        time.sleep(5)
        for i in list(wart):
            with urllib.request.urlopen(COMFY + "/history/" + i, timeout=30) as f:
                h_ = json.loads(f.read()).get(i)
            if h_:
                if h_.get("status", {}).get("status_str") != "success":
                    print("FEHLER", wart[i], h_.get("status"))
                del wart[i]
    print("offen:", len(wart))
    ziel = os.path.join(OUT, "expressions", ORDNER)
    spec = []
    for zustand in prompts:
        for f in sorted(os.listdir(ziel)):
            if f == zustand + ".png" or (f.startswith(zustand + "-") and f.endswith(".png")):
                spec.append({"id": f[:-4], "titel": ("Closed" if zustand == "zu" else "Open") + " " + f[:-4], "bild": os.path.join(ziel, f), "vergleich": os.path.join(ziel, "zu.png") if aus_zu else ref,
                             "vergleich_titel": "Zu (gewaehlt)" if aus_zu else "Karte heute",
                             "soll": "Barrikade quer ueber dem Weg, Karte sonst gleich" if zustand == "zu" else "Weg frei, dieselben Teile wie zu an der Seite, kein Wagen"})
    d = os.path.join(EDEN, "docs", "abnahme", "barrikade")
    os.makedirs(d, exist_ok=True)
    name = "spec_offen.json" if aus_zu else "spec.json"
    json.dump({"id": "barrikade_offen" if aus_zu else "barrikade", "titel": "Barrikade im Norden" + (", offen" if aus_zu else ""),
               "hinweis": "Links die gewaehlte Barrikade, rechts aufgeschoben. Eine waehlen." if aus_zu else "Links die Karte heute, rechts mit Barrikade. Je eine fuer zu und offen waehlen.", "items": spec},
              open(os.path.join(d, name), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Spec:", len(spec))


def overlay(quelle, ziel):
    """Ausschnitt zurueck auf Kartengroesse, Alpha als weiche Ellipse um den Weg, damit nur die Barrikade die Karte ueberdeckt."""
    k, box = ausschnitt()
    w, h = box[2] - box[0], box[3] - box[1]
    b = Image.open(quelle).convert("RGB").resize((w, h), Image.LANCZOS)
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).ellipse((w * 0.12, h * 0.12, w * 0.88, h * 0.88), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(min(w, h) * 0.08))
    b.putalpha(m)
    b.save(ziel, "WEBP", quality=90)
    return box, k.size


def fertig(wahl):
    taktik = os.path.join(EDEN, "module", "eden_rise", "taktik")
    for zustand, nr in wahl.items():
        name = (zustand + ("" if nr == "0" else "-" + nr) if nr.isdigit() else nr) + ".png"     # offen=offen_neu-1 nimmt die Datei direkt
        box, groesse = overlay(os.path.join(OUT, "expressions", ORDNER, name), os.path.join(taktik, "barrikade_%s.webp" % zustand))
        print(zustand, name, "->", box, "von", groesse)


if __name__ == "__main__":
    if "--fertig" in sys.argv:
        fertig(dict(a.split("=") for a in sys.argv[sys.argv.index("--fertig") + 1:]))
    elif "--rand" in sys.argv:
        erzeugen(aus_zu="rand")
    elif "--bruch" in sys.argv:
        erzeugen(aus_zu="bruch")
    elif "--aus-zu" in sys.argv:
        erzeugen(aus_zu=sys.argv[sys.argv.index("--aus-zu") + 1])
    else:
        erzeugen()
