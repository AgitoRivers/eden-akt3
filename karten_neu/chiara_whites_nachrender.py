# -*- coding: utf-8 -*-
r"""Fuenf Posen im Satz Chiara_Whites neu (Duc 01.11.2026). Gleiche LoRAs und gleiche Outfit-Karte, nur die Haltung aendert sich:
bei joy_2 und optimism_2 liefen die Arme aus dem Bild, bei fear_2, grief_2 und remorse_2 hockte sie breitbeinig am Boden.
Die Posen-Texte gelten nur fuer diesen Lauf, das Deck wird danach zurueckgestellt. Alte Bilder -> Chiara_Whites\_alt_r1.
"""
import os, shutil, sys, time, urllib.request

NUR = next((a[6:].split(",") for a in sys.argv if a.startswith("--nur=")), None)   # vor den Importen lesen, die aendern sys.argv
ALT = next((a[6:] for a in sys.argv if a.startswith("--alt=")), "_alt_r1")
HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import wunsch_sets as ws  # noqa: E402
cd = ws.cd

NAME = "Chiara_Whites"
BASIS = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions\_wunsch_sets\Chiara_Whites"
POSEN = {
    "joy_2": "She stands with both feet on the floor, bouncing with joy, both elbows bent and both fists held up at shoulder height close to her body, head tipped back. Unrestrained joyful laugh, eyes crinkled, mouth wide open in delight.",
    "optimism_2": "She stands upright with both legs straight, both elbows close to her waist, both hands clasped together in front of her chest, the whole of both arms inside the frame, chin lifted toward the horizon. Hopeful bright-eyed face, wide easy smile, brows lifted with anticipation.",
    "fear_2": "She stands with her back against the wall, both legs straight, her hands raised defensively in front of her chest, shoulders tight. Terrified face, eyes wide, mouth trembling open, brows shot high.",
    "grief_2": "She stands with both legs straight, both arms wrapped around her own waist, shoulders drawn in, her face toward the camera. Grief-stricken face, eyes red and swollen, tears on her cheeks, mouth trembling open in a silent sob, brows crumpled.",
    "remorse_2": "She stands with both legs straight and close together, her shoulders drawn in, her fingertips pressed to her lips with both hands, her face toward the camera. Anguished remorseful face, brows pinched, eyes wet.",
}
# chiara_whites_nachrender.py --nur=optimism_2 --alt=_alt_r2   nur diese Posen, alte Bilder in diesen Ordner
if NUR:
    POSEN = {k: v for k, v in POSEN.items() if k in NUR}


def warten(n):
    ende = time.time() + 300
    while time.time() < ende:
        with urllib.request.urlopen("http://127.0.0.1:8189/queue", timeout=10) as r:
            q = cd.json.loads(r.read())
        if not q["queue_running"] and not q["queue_pending"]:
            return True
        time.sleep(5)
    return False


def main():
    st = cd.ps("/api/state")
    alt = {k: st["cfg"].get(k) for k in ("sprite_prompt", "loras", "st_set", "sprite_src", "tags", "unet", "clip", "seed", "view_pro_karte", "st_rembg", "st_crop", "mode", "combine_mode")}
    alt_preset = st["cfg"].get("preset_active")
    pn, seed, _ = ws.SETS[NAME]
    presets = ws.cw.dc.load_json(cd.F_PRESETS, None, "Studio")
    roh = os.path.join(BASIS, "roh")
    weg = os.path.join(BASIS, ALT)
    os.makedirs(weg, exist_ok=True)
    for p in POSEN:
        q, z = os.path.join(roh, p + ".png"), os.path.join(weg, p + ".png")
        if os.path.exists(q):
            if os.path.exists(z):
                sys.exit("Sicherung gibt es schon: " + z)
            shutil.move(q, z)
    alte_texte = {}
    try:
        cd.ps("/api/presets", {"action": "load", "name": pn})
        st = cd.ps("/api/state")
        cfg, dk = st["cfg"], st["decks"]
        kn = presets[pn]["cards_on"]["outfit"][0]
        for kk in dk:
            wahl = {"outfit": {kn}, "setting": {"A Sprite Background"}, "st": set(POSEN)}.get(kk, set())
            for x in dk[kk]:
                x["sel"] = x["name"] in wahl
        karte = next(c for c in dk["outfit"] if c["name"] == kn)
        assert ws.ZUSATZ[NAME] in karte["prompt"], "Goldkette fehlt in der Karte"
        for c in dk["st"]:
            if c["name"] in POSEN:
                alte_texte[c["name"]] = c["prompt"]
                c["prompt"] = POSEN[c["name"]]
        cd.ps("/api/config", dict(tags=cfg["tags"], mode="sprite", sprite_src="t2i", combine_mode="all", view_pro_karte=True, st_rembg=True, st_crop=True,
                                  seed=seed, st_set="%s/%s/roh" % (ws.ORDNER, NAME), loras=presets[pn]["loras"], sprite_prompt=presets[pn]["sprite_prompt"]))
        k = cd.ps("/api/queue", {"cfg": {}, "decks": dk, "max_auftraege": len(POSEN)}).get("queued", 0)
        print("eingereiht", k)
    finally:
        st = cd.ps("/api/state")
        dk = st["decks"]
        for c in dk["st"]:
            if c["name"] in alte_texte:
                c["prompt"] = alte_texte[c["name"]]
        cd.ps("/api/decks", dk)
        if alt_preset:
            cd.ps("/api/presets", {"action": "load", "name": alt_preset})
        cd.ps("/api/config", {k: v for k, v in alt.items() if v is not None})
    print("fertig" if warten(k) else "ZEITLIMIT")
    for p in POSEN:
        print(p, os.path.exists(os.path.join(roh, p + ".png")))
    print(sorted(f for f in os.listdir(roh) if "-" in f))


if __name__ == "__main__":
    main()
