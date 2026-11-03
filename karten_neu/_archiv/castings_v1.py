# -*- coding: utf-8 -*-
r"""Zehn Castings fuer neue Eden-Frauen (20.10.2026, Duc: "10 verschiedene Personen mit admiration; Stil-LoRAs:
3x Hegre, 3x Ersties, 4x je 2 andere; keine Asiatinnen; Babes").

    castings.py            Probelauf: zeigt, was eingetragen wuerde
    castings.py --los      Presets Casting_01..10 + Outfit-Karten eintragen und je 1 Bild "admiration" (t2i) erzeugen
                           -> output\expressions\_casting\Casting_NN\admiration.png

Nur Stil-LoRAs, keine Personen-LoRAs (erfundene Gesichter). Basis: Krea_Real3 0.7 + Krea_Nsfw2 0.7.
Wer gewaehlt wird, bekommt danach einen richtigen Namen, Outfits und Laeufe; die uebrigen Castings werden geloescht.
"""
import io, json, os, sys, time, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, r"X:\AI\DucCommon")
import duc_common as dc  # noqa: E402

LOS = "--los" in sys.argv
V3 = "--v3" in sys.argv          # Duc 20.10.: wie v2, aber Basismodell BigLoveKreaLife1 -> _casting_v3
V2 = "--v2" in sys.argv or V3    # Duc 20.10.: Hegre<->Ersties tauschen, Rest nur Insta -> _casting_v2
ORDNER = "_casting_v3" if V3 else "_casting_v2" if V2 else "_casting"
LIFE = {"unet": "BigLoveKreaLife1_bf16.safetensors", "clip": "qwen3vl_4b_bf16.safetensors"}
PS = "http://127.0.0.1:8301"
F_PRESETS = r"X:\AI\PromptStudio\presets.json"
JETZT = time.strftime("%Y-%m-%d %H:%M")
BASIS = [{"name": "Krea_Real3.safetensors", "strength": 0.7}, {"name": "Krea_Nsfw2.safetensors", "strength": 0.7}]


def L(*paare):
    return BASIS + [{"name": "Krea_%s.safetensors" % n if not n.startswith("Krea") else n + ".safetensors",
                     "strength": s} for n, s in paare]


BABE = ("a gorgeous glamorous grown adult woman in her mid to late twenties with a mature adult face, stunning model "
        "looks, full lips")
# (Herkunft/Gesicht, Stil-LoRAs, Tags, Outfit)
CASTINGS = [
    ("a Swedish woman from Stockholm with ice-blue eyes and high cheekbones", L(("Hegre", 0.8)),
     ["Color: Platinum", "Style: Long Layered", "Body: Curvy", "Large", "Instagirl Soft Glam", "Glossy Lips"],
     "a white cropped ribbed tank top, light blue high-waisted denim shorts, white sneakers"),
    ("an Irish woman from Cork with green eyes, very pale porcelain skin, freckles and long wavy bright copper-red hair", L(("Hegre", 0.8)),
     ["Color: Red", "Pale skin", "Freckles", "Style: Waves", "Body: Curvy", "Busty", "Full Glam", "Glossy Lips"],
     "a fitted black off-shoulder knit top, a tight black leather mini skirt, black ankle boots"),
    ("a Ukrainian woman from Kyiv with grey-green eyes and a soft heart-shaped face", L(("Hegre", 0.8)),
     ["Color: Honey blonde", "Style: Blowout", "Body: Curvy", "Large", "Smokey Eye", "Nude Lips"],
     "a tight beige ribbed knit midi dress, nude heels"),
    ("a Brazilian woman from Rio de Janeiro with sun-kissed tan skin and long dark brown wavy hair", L(("Ersties", 0.8)),
     ["Color: dark brown", "Style: Long Wet Hair", "Body: Curvy", "Thick", "Large", "Summer", "Sheen"],
     "a tiny yellow crop top, a white denim mini skirt, gold hoop earrings, flat sandals"),
    ("an Italian woman from Naples with dark brown eyes, olive skin and long glossy black hair", L(("Ersties", 0.8)),
     ["Color: Black", "Style: Straight", "Body: Curvy", "Busty", "Winged Liner", "Glossy Lips"],
     "a tight red bodycon dress with thin straps, black strappy heels"),
    ("an Australian surfer woman from the Gold Coast with sun-bleached honey blonde beach waves and a light tan",
     L(("Ersties", 0.8)),
     ["Color: Honey blonde", "Style: Waves", "Body: Athletic", "Body: Curvy", "Large", "Summer", "Tan Lines"],
     "a white tied-up linen shirt over a small turquoise bikini top, frayed denim shorts, barefoot"),
    ("a Colombian woman from Medellin with warm caramel skin, honey-brown eyes and long voluminous brunette hair",
     L(("Insta", 0.6), ("Photo", 0.6)),
     ["Color: Brunette", "Style: Blowout", "Body: Curvy", "Thick", "Busty", "Full Glam", "Glossy Lips"],
     "a black square-neck corset top, tight high-waisted black jeans, black heels"),
    ("a Lebanese woman from Beirut with dark almond-shaped eyes, thick brows and long straight black hair",
     L(("Raw", 0.6), ("Grain", 0.5)),
     ["Color: Black", "Style: Long Layered", "Body: Curvy", "Large", "Smokey Eye", "Winged Liner"],
     "a fitted emerald satin camisole, cream wide-leg trousers, gold jewellery, nude heels"),
    ("a French Caribbean woman from Martinique with deep brown skin, dark eyes and long curly black hair",
     L(("Phone", 0.6), ("Krea-realism-V2", 0.6)),
     ["Color: Black", "Style: Long Layered", "Body: Curvy", "Busty", "Party Glitter Glam", "Glossy Lips"],
     "a tight white ribbed mini dress, gold hoop earrings, white sandals"),
    ("a Spanish woman from Seville with warm brown eyes, olive skin and long thick brunette waves",
     L(("Real2", 0.6), ("Krea-realism-V2", 0.6)),
     ["Color: Brunette", "Style: Waves", "Body: Curvy", "Large", "Boudoir Glam", "Glossy Lips"],
     "a black lace-trimmed silk slip top, a high-waisted flowing black mini skirt, black heels"),
]


if V2:
    _tausch = {"Krea_Hegre.safetensors": "Krea_Ersties.safetensors", "Krea_Ersties.safetensors": "Krea_Hegre.safetensors"}
    for _i, _c in enumerate(CASTINGS):
        if _i < 6:
            _l = [dict(x, name=_tausch.get(x["name"], x["name"])) for x in _c[1]]
        else:
            _l = BASIS + [{"name": "Krea_Insta.safetensors", "strength": 0.8}]
        CASTINGS[_i] = (_c[0], _l) + tuple(_c[2:])


def ps(pfad, daten=None):
    req = urllib.request.Request(PS + pfad, data=None if daten is None else json.dumps(daten).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.loads(r.read())


def sprite_prompt(subject):
    return ("{tags_action}, Shot on an iPhone, realistic smartphone photography, full body shot from head to knees, "
            "direct gaze, one single woman alone in the frame, her whole body in full view, head and knees inside the "
            "frame,\nSubject: %s,\nBody: {tags_body},\nHair: {tags_haircolor}, {tags_hairstyle}, {tags_hair}\n"
            "Skin: {tags_skin},\nMakeup: {tags_face}\nWearing: {outfit},\nScene: {setting}, {st},\n{expression},\n"
            "Look: {look},\n{tags_photo}" % subject)


def main():
    st = ps("/api/state")
    tag_namen = {t["name"] for t in st["cfg"]["tags"]}
    fehler = [t for c in CASTINGS for t in c[2] if t not in tag_namen]
    loras = {x for c in CASTINGS for x in (l["name"] for l in c[1])}
    print("Tags fehlen:", fehler or "-")
    print("LoRAs:", ", ".join(sorted(loras)))
    if fehler or not LOS:
        print("Probelauf - nichts geschrieben." if not fehler else "Abbruch.")
        return
    # Outfit-Karten ueber die API (der Browser-Tab schreibt decks.json sonst zurueck)
    d = ps("/api/state")["decks"]
    da = {c["name"] for c in d["outfit"]}
    for i, c in enumerate(CASTINGS, 1):
        n = "casting_%02d" % i
        if n not in da:
            d["outfit"].append({"name": n, "prompt": c[3], "on": True, "tag": "casting", "sel": False,
                                "back_prompt": c[3] + ", seen from behind"})
    ps("/api/decks", d)
    presets = dc.load_json(F_PRESETS, None, "Studio")
    for i, c in enumerate(CASTINGS, 1):
        presets["Casting_%02d" % i] = {
            "sprite_prompt": sprite_prompt("%s, %s" % (BABE, c[0])), "negative_prompt": "", "loras": c[1],
            "ref_image": "", "ref_image_b": "", "tags_on": ["View: Front"] + c[2],
            "cards_on": {"outfit": ["casting_%02d" % i], "setting": ["A Sprite Background"], "st": ["admiration"]},
            "st_set": ORDNER + "/Casting_%02d" % i, "created": JETZT, "updated": JETZT}
    dc.save_json(F_PRESETS, presets, "Studio")
    n = 0
    alt = {k: st["cfg"].get(k) for k in ("sprite_prompt", "loras", "st_set", "sprite_src", "tags", "unet", "clip")}
    alt_preset = st["cfg"].get("preset_active")
    try:
        n = queue_all(presets)
    finally:
        if alt_preset:
            ps("/api/presets", {"action": "load", "name": alt_preset})
        ps("/api/config", {k: v for k, v in alt.items() if v is not None})
    print("Castings in der Warteschlange:", n)


NUR = [int(x) for x in sys.argv[sys.argv.index("--nur") + 1].split(",")] if "--nur" in sys.argv else None


def queue_all(presets):
    n = 0
    for i, c in enumerate(CASTINGS, 1):
        if NUR and i not in NUR:
            continue
        name = "Casting_%02d" % i
        ps("/api/presets", {"action": "load", "name": name})
        st = ps("/api/state")
        an = set(["View: Front"] + c[2])
        tags = st["cfg"]["tags"]
        for t in tags:
            t["on"] = t["name"] in an
        if V3:
            ps("/api/config", LIFE)
        ps("/api/config", {"tags": tags, "mode": "sprite", "sprite_src": "t2i", "combine_mode": "all",
                           "view_pro_karte": False, "st_rembg": True, "st_crop": True,
                           "st_set": ORDNER + "/" + name + ("b" if NUR else ""), "loras": c[1], "sprite_prompt": presets[name]["sprite_prompt"]})
        d = ps("/api/state")["decks"]
        for k, wahl in (("outfit", {"casting_%02d" % i}), ("setting", {"A Sprite Background"}), ("st", {"admiration"})):
            for x in d[k]:
                x["sel"] = x["name"] in wahl
        for k in d:
            if k not in ("outfit", "setting", "st"):
                for x in d[k]:
                    x["sel"] = False
        n += ps("/api/queue", {"cfg": {"combine_mode": "all"}, "decks": d}).get("queued", 0)
    return n


if __name__ == "__main__":
    main()
