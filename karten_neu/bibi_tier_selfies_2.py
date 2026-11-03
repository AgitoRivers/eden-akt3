# -*- coding: utf-8 -*-
r"""Bibis Tier-Selfies, Runde 2 (Duc 02.11.2026): Basis ist das Studio-Preset Bibi_Selfie (Prompt, LoRAs), Outfits aus den
Karten bibi_nach_1..5 und bibi_arbeit, Hintergrund bibi_selfie_pen, Tier-Posen bibi_selfie_<tier>. Je Selfie eine andere Frisur.
Fuenf Tiere, je vier Seeds.

    bibi_tier_selfies_2.py   -> ComfyUI\output\expressions\_bibi_tier_selfies_2\<tier>_<n>.png
"""
import json, os, re, sys, time, urllib.request

sys.path.insert(0, r"X:\AI\PromptStudio")
PS, COMFY = "http://127.0.0.1:8301", "http://127.0.0.1:8189"
ORDNER = "_bibi_tier_selfies_3"
SEEDS = (240211, 771903, 518447, 90391)
HAAR_ALT = ("her hair is blonde, very long straight hair with blunt straight bangs and straight side locks cut at cheek height")
# Tier (Pose-Karte), Outfit-Karte, Frisur (Pony bleibt, er ist ihr Erkennungszeichen). Runde 3 (Duc 02.11.2026): fashion_prompt des
# Presets, damit die aktiven Tags (tags_on) in ihre Platzhalter kommen - nur diese, nicht alle Tags des Studios.
AUFTRAG = [
    ("monsieur", "bibi_nach_2", "her hair is blonde, half up half down with a small knot on top, soft face-framing tendrils loose at her "
                                "temples, blunt straight bangs, the rest long and straight down her back"),
    ("madame", "bibi_nach_4", "her hair is blonde, very long, sleek and perfectly straight, glossy and smooth, with blunt straight bangs"),
    ("rusty", "bibi_nach_3", "her hair is blonde, pulled up into a high bouncy ponytail with blunt straight bangs and a few loose strands"),
    ("monday", "bibi_nach_5", "her hair is blonde, in two long loose braids over her shoulders, with blunt straight bangs"),
    ("pudding", "bibi_arbeit", "her hair is blonde with blunt straight bangs"),
]


def post(url, daten):
    req = urllib.request.Request(url, data=json.dumps(daten).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())


def main():
    import studio
    decks = json.load(open(r"X:\AI\PromptStudio\decks.json", encoding="utf-8"))
    karte = lambda kat, name: next(c["prompt"] for c in decks[kat] if c["name"] == name)
    preset = json.load(open(r"X:\AI\PromptStudio\presets.json", encoding="utf-8"))["Bibi_Selfie"]
    basis = preset["fashion_prompt"]
    with urllib.request.urlopen(PS + "/api/state", timeout=30) as f:
        alle_tags = {x["name"]: x for x in json.loads(f.read())["cfg"].get("tags", [])}
    aktiv = [alle_tags[n] for n in preset.get("tags_on", []) if n in alle_tags]
    kat = lambda c: ", ".join(x["prompt"].strip().rstrip(",") for x in aktiv if (x.get("cat") or "").lower() == c and x.get("prompt", "").strip())

    def zusammen(tier, outfit, haar):
        p = basis
        for c in ("body", "skin", "haircolor", "hair", "face", "photo", "action"):
            p = p.replace("{tags_%s}" % c, kat(c))
        p = p.replace("{tags_hairstyle}", haar.replace("her hair is blonde, ", ""))
        p = p.replace("{outfit}", karte("outfit", outfit)).replace("{setting}", karte("setting", "bibi_selfie_pen"))
        p = p.replace("{st}", "").replace("{expression}", karte("pose", "bibi_selfie_" + tier)).replace("Look: {look},\n", "").replace("{look}", "")
        p = re.sub(r",\s*,", ",", p)
        p = re.sub(r", +\n", ",\n", p)
        return p

    with urllib.request.urlopen(PS + "/api/state", timeout=30) as f:
        cfg = dict(json.loads(f.read())["cfg"])
    wart = []
    for tier, outfit, haar in AUFTRAG:
        p = zusammen(tier, outfit, haar)
        if tier == AUFTRAG[0][0]:
            print(p, flush=True)
        for n, seed in enumerate(SEEDS, 1):
            c = dict(cfg, loras=preset["loras"], mode="sprite", sprite_src="t2i", width=896, height=1152, negative_prompt="", st_set=ORDNER,
                     st_rembg=False, st_crop=False)
            wart.append(post(COMFY + "/prompt", {"prompt": studio.build_graph(c, p, "%s_%d" % (tier, n), seed)})["prompt_id"])
    print("eingereiht", len(wart), flush=True)
    fehler, ende = 0, time.time() + 1800
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
