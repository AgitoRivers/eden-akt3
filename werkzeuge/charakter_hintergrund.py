# -*- coding: utf-8 -*-
r"""Element backdrops for the character screen (26.10.2026): a real photographed wall per jacket element, rendered
separately from the sprite (Duc: sprite and backdrop apart, the backdrop slightly darkened by the menu).

    python werkzeuge\charakter_hintergrund.py            2 variants each -> docs\abnahme\charakter\bg\Bg<Element>_v1..2.png
    python werkzeuge\charakter_hintergrund.py --waehle Erde 1    variant 1 -> module\eden_rise\charakter\BgErde.webp

No people, no LoRAs, same model set as the portraits. Positive wording only (Krea at CFG 1 ignores negatives).
"""
import json, os, random, sys, time

sys.stdout.reconfigure(encoding="utf-8")
HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import charakter_bild as cb  # noqa: E402

BG = os.path.join(cb.EDEN, "docs", "abnahme", "charakter", "bg")
STIL = ("Cinematic photograph of {szene}, no people, no figures, nothing in the foreground, the centre of the frame calm and "
        "open, deep moody low-key lighting, shallow depth of field, rich dark tones, vertical composition")
ELEMENTE = {
    "Erde": "a massive dark rough-hewn granite cliff face with broad horizontal layers, smooth weathered stone, a few ledges "
            "with moss and small ferns, warm amber light raking across the stone from the side, deep shadows",
    "Wasser": "a towering wall of dark teal sea water at the moment a huge wave rises, glassy and translucent with light "
              "shining through it from above, a fine mist of spray in the air, deep blue and turquoise tones",
    "Feuer": "a huge wall of roaring orange and red flames filling the frame, glowing embers drifting upward in the dark "
             "air, thick dark smoke above, intense warm light and deep black shadows",
    "Luft": "an endless vertical wall of towering pale storm clouds, soft streaks of wind-swept mist, shafts of cool "
            "silver light breaking through, a deep slate-blue sky, smooth flowing cloud forms",
}


# Duc 26.10.: four DIFFERENT backdrops per element (a = the first set above, b-d are new motifs); files Bg<Element>_<b|c|d>.png
MEHR = {
    "Erde": {"b": "an ancient dark forest at dusk, enormous moss-covered tree trunks and thick roots, golden light falling "
                  "in slanted beams through the canopy, a soft haze between the trunks",
             "c": "a tall layered red sandstone canyon wall in the last warm sunset light, smooth wind-carved bands of "
                  "orange and brown rock, a deep blue sky strip far above",
             "d": "a weathered moss-covered stone ruin wall overgrown with dark green ivy, huge smooth fitted stone blocks, "
                  "warm lantern light from the side, deep shadows"},
    "Wasser": {"b": "deep clear blue ocean seen from underneath, long shafts of sunlight falling through the water from the "
                    "surface far above, drifting particles, a smooth gradient from bright turquoise to deep navy",
               "c": "a tall waterfall pouring down a dark mossy rock gorge, fine mist rising, cool blue light, glossy wet "
                    "black rock on both sides",
               "d": "a rain-lashed harbour quay at night, shining wet cobblestones reflecting warm lamp light, dark water, "
                    "heavy rain streaking the air, a stormy dark sky"},
    "Feuer": {"b": "a river of glowing molten lava flowing through a dark volcanic landscape at night, a volcano glowing "
                   "orange in the distance, drifting embers and a red-lit smoky sky",
              "c": "the inside of a huge old blacksmith's forge, a furnace glowing white-orange, a wall of hot glowing "
                   "iron, showers of golden sparks, deep black shadows, thick warm haze",
              "d": "a sky blazing with deep orange and crimson sunset clouds over black mountain silhouettes, glowing "
                   "embers drifting in the air, an intense red light"},
    "Luft": {"b": "a high mountain ridge above a sea of clouds at dawn, rose and gold light on the peaks, thin crisp air, "
                  "a vast soft sky",
             "c": "a bright blue sky with huge towering white cumulus clouds lit by the sun, wind-streaked cirrus, "
                  "crisp light, an open airy feeling",
             "d": "a lone windswept grassy cliff top, tall grass bending flat in a strong wind, a huge dramatic sky "
                  "of racing clouds, cool silver light, a hint of the sea far below"},
}


# Duc 26.10. (Abnahme): Erde "Granit frontal", Wasser "Schlucht etwas heller" - two new takes each, files Bg<Element>_e|f
NEU = {
    "Erde": {"e": "a straight-on frontal view of a massive flat granite rock wall filling the whole frame, broad smooth slabs "
                  "with fine natural cracks and pale lichen, a few ferns at the very bottom, warm amber light raking "
                  "across the stone, deep shadows",
             "f": "a straight-on frontal view of a weathered dark granite cliff wall with broad horizontal bands, a mossy "
                  "ledge near the bottom, soft golden side light, calm and monumental"},
    "Wasser": {"e": "a tall waterfall pouring down a mossy rock gorge in soft bright daylight, light blue-green mist, "
                    "sunbeams falling through, lush green ferns, glossy wet grey rock, a fresh clear atmosphere",
               "f": "a tall narrow waterfall in a lush green gorge lit by warm afternoon sun, shimmering white water, "
                    "turquoise pool at the foot, wet rock with bright moss, a luminous misty atmosphere"},
}


# Duc 26.10.: Wasser lieber Meer und Kueste - files BgWasser_g..j
MEER = {"g": "a calm turquoise Mediterranean cove at golden hour, smooth rocky cliffs on both sides, gentle clear water "
             "with soft light shimmering on it, a warm glow on the horizon, peaceful and cinematic",
        "h": "the open sea at dusk seen from low above the water, a gently rolling dark blue swell, a glowing pink and "
             "gold horizon, soft clouds, a wide quiet atmosphere",
        "i": "a rugged rocky coast with waves rolling onto smooth dark rocks in soft morning light, light turquoise "
             "water, a thin sea mist, a bright pale sky",
        "j": "a sunlit stretch of clear shallow turquoise sea over pale sand with a soft white shoreline, tall dark "
             "limestone cliffs rising behind, bright midday light, fresh and airy"}


# Citadelle (Cyber): cool technical wall, files BgCyber_a|b
CYBER = {"a": "a vast clean futuristic laboratory wall of brushed dark steel panels and tall frosted glass, thin cyan light "
              "strips running down it, a cool teal glow, sleek and calm",
         "b": "a high-tech command deck seen from inside, a huge dark glass window with a night city of cyan lights far "
              "below, smooth black metal surfaces, cool cyan reflections, a quiet futuristic atmosphere"}


# Duc 26.10.: Citadelle = the island is saved, so a bright, proud backdrop (s = sunrise ridge, f = village festival)
SIEG = {
    "s1": "a view from a high grassy ridge at sunrise over a small saved Mediterranean island, the village and a harbour "
          "with a white yacht glowing in the first golden light far below, a clear soft sky, the sea sparkling, warm hopeful mood",
    "s2": "a hilltop overlooking a sunny Mediterranean bay at early morning, terracotta rooftops and a calm turquoise sea "
          "with a white yacht anchored, long golden light, a pale blue sky with thin clouds, a proud peaceful mood",
    "f1": "the village square of a Mediterranean island town at dusk during a joyful festival, strings of warm lanterns "
          "overhead, colourful confetti in the air, stone houses glowing orange, a warm festive mood",
    "f2": "a lively harbour promenade at golden dusk with hundreds of hanging fairy lights and paper lanterns, bunting "
          "between the old stone houses, warm light and a soft turquoise sky above, a celebrating atmosphere",
}


def waehlen(k, v):
    from PIL import Image
    os.makedirs(cb.SPIEL, exist_ok=True)
    with Image.open(os.path.join(BG, "Bg%s_%s.png" % (k, ("v%d" % v) if str(v).isdigit() else v))) as im:
        im.convert("RGB").save(os.path.join(cb.SPIEL, "Bg%s.webp" % k), "WEBP", quality=86, method=6)
    print("uebernommen:", k, "Variante", v)


def mehr(cfg):
    auftraege = {}
    for k, d in MEHR.items():
        for v, szene in d.items():
            name = "Bg%s_%s" % (k, v)
            g = cb.graph(STIL.format(szene=szene), name, random.randint(1, 2 ** 31), cfg, [])
            auftraege[name] = cb.post("/prompt", {"prompt": g})["prompt_id"]
    return auftraege


def main():
    if "--waehle" in sys.argv:
        i = sys.argv.index("--waehle")
        return waehlen(sys.argv[i + 1], sys.argv[i + 2])
    cfg = json.load(open(cb.STUDIO_CFG, encoding="utf-8-sig"))
    os.makedirs(BG, exist_ok=True)
    cb.ZIEL = BG
    if "--sieg" in sys.argv:
        auftraege = {}
        for v, szene in SIEG.items():
            name = "BgCyber_%s" % v
            auftraege[name] = cb.post("/prompt", {"prompt": cb.graph(STIL.format(szene=szene), name, random.randint(1, 2 ** 31), cfg, [])})["prompt_id"]
    elif "--cyber" in sys.argv:
        auftraege = {}
        for v, szene in CYBER.items():
            name = "BgCyber_%s" % v
            auftraege[name] = cb.post("/prompt", {"prompt": cb.graph(STIL.format(szene=szene), name, random.randint(1, 2 ** 31), cfg, [])})["prompt_id"]
    elif "--meer" in sys.argv:
        auftraege = {}
        for v, szene in MEER.items():
            name = "BgWasser_%s" % v
            auftraege[name] = cb.post("/prompt", {"prompt": cb.graph(STIL.format(szene=szene), name, random.randint(1, 2 ** 31), cfg, [])})["prompt_id"]
    elif "--neu" in sys.argv:
        auftraege = {}
        for k, d in NEU.items():
            for v, szene in d.items():
                name = "Bg%s_%s" % (k, v)
                auftraege[name] = cb.post("/prompt", {"prompt": cb.graph(STIL.format(szene=szene), name, random.randint(1, 2 ** 31), cfg, [])})["prompt_id"]
        ELEM = {}
    else:
        auftraege = mehr(cfg) if "--mehr" in sys.argv else {}
        ELEM = None
    for k, szene in ({} if ("--mehr" in sys.argv or "--neu" in sys.argv or "--meer" in sys.argv or "--cyber" in sys.argv or "--sieg" in sys.argv) else ELEMENTE).items():
        for v in (1, 2):
            name = "Bg%s_v%d" % (k, v)
            g = cb.graph(STIL.format(szene=szene), name, random.randint(1, 2 ** 31), cfg, [])
            auftraege[name] = cb.post("/prompt", {"prompt": g})["prompt_id"]
        print("eingereiht:", k)
    t0 = time.time()
    while auftraege and time.time() - t0 < 1800:
        time.sleep(3)
        for name, pid in list(auftraege.items()):
            h = cb.get(cb.COMFY + "/history/" + pid)
            if pid in h and h[pid].get("status", {}).get("completed"):
                print("fertig:", name, flush=True)
                auftraege.pop(name)
    print("alle fertig" if not auftraege else "offen: " + ", ".join(auftraege))


if __name__ == "__main__":
    main()
