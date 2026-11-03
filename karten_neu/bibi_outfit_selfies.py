# -*- coding: utf-8 -*-
r"""Bibis vier neue Outfits im Tier-Selfie (Duc 02.11.2026): Arbeitstag, Anime-Abend, Festa-Kleid, Pitch-Tag, je mit Biscuit,
Monday und Sunday auf dem Seed, den Duc in der Probe gewaehlt hat. Legt die Outfits auch als Karten mit Tag bibi_selfie ins Prompt Studio.

    bibi_outfit_selfies.py   -> output\expressions\_bibi_outfit_selfies\<outfit>_<tier>.png
"""
import json, os, shutil, sys, time, urllib.request

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, r"X:\AI\PromptStudio")
import bibi_tier_selfies as T  # noqa: E402

ORDNER = "_bibi_outfit_selfies"
OUTFITS = {
    "arbeit": "faded old denim dungarees over a red-and-navy striped long-sleeved top, her hair pulled up in a messy bun with a pencil "
              "stuck through it, a smear of dry mud on one cheek, black fingerless combat gloves",
    "anime": "an oversized faded black T-shirt with a big printed cartoon villain laughing on the front, soft grey sleep shorts, her hair "
             "loose and a little messy, no makeup, a cosy evening look",
    "festa": "a black summer dress made by hand by her friend, with a big ruffled collar shaped like a golden lion's mane around her neck and shoulders, fine gold stitching along the hem, a thin red ribbon belt and a small red flower in her hair, small gold earrings, her hair half up with loose strands",
    "pitch": "a borrowed navy blazer far too big for her with the sleeves rolled up three times, worn over an open black short-sleeved "
             "shirt with a lion print, black choker, a stack of crumpled paper bills held against her chest",
}
WAHL = {"hund": T.SEEDS[0], "capybara": T.SEEDS[1], "wolf": T.SEEDS[0]}      # Probe-Abnahme: Biscuit 1, Monday 2, Sunday 1


def karten_ins_studio():
    stamp = time.strftime("%Y%m%d_%H%M")
    shutil.copyfile(r"X:\AI\PromptStudio\decks.json", r"X:\AI\PromptStudio\decks.vor-bibi-outfits-%s.json" % stamp)
    with urllib.request.urlopen(T.PS + "/api/state", timeout=30) as f:
        decks = json.loads(f.read())["decks"]
    neu = [{"name": "bibi_" + k, "tag": "bibi_selfie", "on": True, "sel": False, "prompt": v} for k, v in OUTFITS.items()]
    namen = {k["name"] for k in neu}
    decks["outfit"] = [c for c in decks["outfit"] if c["name"] not in namen] + neu
    req = urllib.request.Request(T.PS + "/api/decks", data=json.dumps(decks).encode(), headers={"Content-Type": "application/json", "X-Tab": "skript"})
    urllib.request.urlopen(req, timeout=30).read()


def main():
    import studio
    karten_ins_studio()
    with urllib.request.urlopen(T.PS + "/api/state", timeout=30) as f:
        cfg = dict(json.loads(f.read())["cfg"])
    wart = []
    for ok, anzug in OUTFITS.items():
        for tid, seed in WAHL.items():
            p = "%s,\nSubject: %s,\nWearing: %s,\nScene: %s,\n%s." % (T.KOPF, T.WER, anzug, T.ORT, T.TIERE[tid])
            c = dict(cfg, loras=T.LORAS, mode="sprite", sprite_src="t2i", width=896, height=1152, negative_prompt="", st_set=ORDNER,
                     st_rembg=False, st_crop=False)
            wart.append(T.post(T.COMFY + "/prompt", {"prompt": studio.build_graph(c, p, "%s_%s" % (ok, tid), seed)})["prompt_id"])
    print("eingereiht", len(wart), flush=True)
    fehler, ende = 0, time.time() + 1800
    while wart and time.time() < ende:
        time.sleep(3)
        for i in list(wart):
            with urllib.request.urlopen(T.COMFY + "/history/" + i, timeout=30) as f:
                r = json.loads(f.read()).get(i)
            if r:
                fehler += r.get("status", {}).get("status_str") != "success"
                wart.remove(i)
    print("offen", len(wart), "fehler", fehler)


if __name__ == "__main__":
    main()
