# -*- coding: utf-8 -*-
r"""SFW-Posensatz fuer die Wunsch-Outfits (Duc 31.10.2026, gewaehlt auf docs/abnahme/wunsch_final.json).
Quelle sind die Presets Yacht_<Figur>_<Art>_Haar aus casting_wunsch_haar.py: Outfit, Frisur und LoRAs bleiben, nur die Posen kommen dazu.

    wunsch_sets.py                  Probelauf
    wunsch_sets.py --los [Name ...] je Look alle SFW-Posen -> output\expressions\_wunsch_sets\<Name>\roh
"""
import json, os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, r"X:\AI\DucCommon")
LOS = "--los" in sys.argv
POSEN = next((a[8:].split(",") for a in sys.argv if a.startswith("--posen=")), None)   # nur diese Posen neu
import casting_wunsch_outfits as cw  # noqa: E402
cd = cw.cd

ORDNER = "_wunsch_sets"
# Name: (Preset, Seed des gewaehlten Bilds, Anlass)
SETS = {
    "Sophia_Reading": ("Yacht_Sophia_W_Haar", 240611, "Buchlesung"),
    "Rosi_Workshop": ("Yacht_Rosi_W_Haar", 977031, "neues Werkstatt-Outfit, wenn man will"),
    "Rosi_Festa": ("Yacht_Rosi_A_Haar", 240611, "Festa"),
    "Siri_Morning": ("Yacht_Siri_K_Haar", 240611, "neuer Morgen-Look"),
    "Siri_Festa": ("Yacht_Siri_D_Haar", 240611, "Festa"),
    "Alva_Bar": ("Yacht_Alva_W_Haar", 240611, "neuer Bar-Look"),
    "Chiara_Whites": ("Yacht_Chiara_Whites_Anker_b", 240611, "Dress Whites mit Anker-Pin, Blowout"),
}
# Duc hat bei Rosi das Bild mit den schwarzen Schultern gewaehlt, das kam nur vom Seed und muss darum in die Karte.
# Bei Chiara kam die Goldkette nach dem Test dazu.
ZUSATZ = {"Rosi_Workshop": ", black leather panels on both shoulders", "Chiara_Whites": ", a thin gold chain necklace"}
# Ausschnitt und Pin in der Karte drehen Chiara trotz "from behind" nach vorn, die Rueckansicht bekommt darum einen eigenen Text
RUECKEN = {"Chiara_Whites": "a bright white tailored officer's jacket seen from behind, its back smooth and plain with crisp level shoulders, high-waisted wide-leg white sailor trousers, white deck sneakers, a slim gold watch"}


def main():
    plan = {n: s for n, s in SETS.items() if not cw.NUR or n in cw.NUR}
    st = cd.ps("/api/state")
    alt = {k: st["cfg"].get(k) for k in ("sprite_prompt", "loras", "st_set", "sprite_src", "tags", "unet", "clip", "seed", "view_pro_karte", "st_rembg", "st_crop")}
    alt_preset = st["cfg"].get("preset_active")
    posen = list(st["cfg"].get("sfw_posen") or [])
    d = st["decks"]
    an = [c["name"] for c in d["st"] if c.get("on", True) and c["name"] in posen and (not POSEN or c["name"] in POSEN)]
    print("%d Posen, %d Looks, %d Bilder" % (len(an), len(plan), len(an) * len(plan)))
    presets = cw.dc.load_json(cd.F_PRESETS, None, "Studio")
    for n, (pn, seed, anlass) in plan.items():
        print(n, "|", anlass, "| Seed", seed, "|", presets[pn]["cards_on"]["outfit"], "|", presets[pn]["loras"][-1])
    if not LOS:
        print("Probelauf - nichts eingestellt.")
        return
    gesamt = 0
    try:
        for n, (pn, seed, _) in plan.items():
            cd.ps("/api/presets", {"action": "load", "name": pn})
            st = cd.ps("/api/state")
            cfg, dk = st["cfg"], st["decks"]
            kn = presets[pn]["cards_on"]["outfit"][0]
            for kk in dk:
                wahl = {"outfit": {kn}, "setting": {"A Sprite Background"}, "st": set(an)}.get(kk, set())
                for x in dk[kk]:
                    x["sel"] = x["name"] in wahl
            karte = next(c for c in dk["outfit"] if c["name"] == kn)
            if n in ZUSATZ and ZUSATZ[n] not in karte["prompt"]:
                karte["prompt"] += ZUSATZ[n]
                karte["back_prompt"] = karte["prompt"] + ", seen from behind"
            if n in RUECKEN:
                karte["back_prompt"] = RUECKEN[n]
            cd.ps("/api/decks", dk)
            cd.ps("/api/config", dict(tags=cfg["tags"], mode="sprite", sprite_src="t2i", combine_mode="all", view_pro_karte=True, st_rembg=True, st_crop=True,
                                      seed=seed, st_set="%s/%s/roh" % (ORDNER, n), loras=presets[pn]["loras"], sprite_prompt=presets[pn]["sprite_prompt"]))
            k = cd.ps("/api/queue", {"cfg": {}, "decks": dk, "max_auftraege": len(an)}).get("queued", 0)
            print(n, "eingereiht", k)
            gesamt += k
    finally:
        if alt_preset:
            cd.ps("/api/presets", {"action": "load", "name": alt_preset})
        cd.ps("/api/config", {k: v for k, v in alt.items() if v is not None})
    print("Gesamt %d Bilder -> expressions\\%s" % (gesamt, ORDNER))


if __name__ == "__main__":
    main()
