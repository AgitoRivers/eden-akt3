# -*- coding: utf-8 -*-
r"""Casting "nach der Mission" (Duc 30.10.2026): was Bibi, Charly und Danzel nach der Red-Trio-Quest tragen.

    casting_nach_mission.py          Probelauf
    casting_nach_mission.py --los    Casting-Presets Yacht_Bibi_Nach_1..5, Yacht_Charly_Nach_1..5, Yacht_Danzel_Nach_1..3,
                                     je 2 Portraits -> output\expressions\_casting_nach_mission\<Preset>

Bestehende Presets und Sets (Yacht_Bibi, Yacht_Charly, Yacht_Danzel, Kampf_*) bleiben unberuehrt: Subject, Tags und LoRAs werden
live aus dem jeweiligen Yacht_-Preset gelesen und in ein neues Preset kopiert, nur Outfit-Karte, Rahmung (ganzer Koerper bis zu
den Schuhen) und Zielordner sind anders. Alle Figuren sind erwachsen und bekleidet, normale Haltung.
"""
import json, os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, r"X:\AI\DucCommon")
LOS = "--los" in sys.argv
NR = sys.argv[sys.argv.index("--nr") + 1].split(",") if "--nr" in sys.argv else None      # nur diese Nummern
NUR = sys.argv[sys.argv.index("--nur") + 1] if "--nur" in sys.argv else None      # z. B. --nur Yacht_Danzel
_HALTEN = []
sys.argv = [sys.argv[0]] + (["--los"] if LOS else [])
import castings_danzel as cd  # noqa: E402
import duc_common as dc  # noqa: E402
_HALTEN.append(sys.stdout)

ORDNER = "_casting_nach_mission"
TAG = "eden_nach_mission"
LOEWE = "a small completely black plush lion keychain clipped to "

# (Basis-Preset, Kurzname, {Nr: Outfit}, Alterstext alt -> neu)
BIBI = {
    "1": "a khaki cropped tank top, short khaki shorts with a brown leather belt, sturdy brown lace-up boots with rolled socks, a red-and-white bandana tied around her hair, " + LOEWE + "her belt",
    "2": "khaki bib overalls with short legs worn over a fitted white tank top, the straps buckled, brown work boots, a green bandana tied loosely around her neck, " + LOEWE + "the bib pocket",
    "3": "an olive green tank top with a knot at the hem, khaki cargo shorts with big pockets, black rubber boots, a sand-coloured bandana in her hair, " + LOEWE + "her belt loop",
    "4": "a sand-coloured short-sleeved shirt knotted at the waist over a fitted black tank top, denim shorts, tan boots, a blue patterned bandana around her wrist, " + LOEWE + "her belt loop",
    "5": "a khaki short-legged utility jumpsuit with the sleeves cut off and a zip open at the collar, a thin brown belt, olive green work boots, a yellow bandana around her neck, " + LOEWE + "her belt",
}
CHARLY = {
    "1": "a fitted gray tank top with oil stains, a dark blue mechanic's overall unzipped with the top half tied around her waist, black work boots, a bag of crisps sticking out of the overall pocket",
    "2": "a black tank top smudged with grease, short canvas work shorts with tool loops, a leather tool belt, black sneakers, a bag of crisps tucked into her back pocket",
    "3": "a charcoal mechanic's overall worn open over a white tank top, sleeves rolled up, black oil smudges on the fabric and her forearms, sturdy boots, a half-eaten bag of crisps in her hand",
    "4": "a sleeveless khaki work shirt tied at the front over a tank top, short dark work trousers with oil stains, safety goggles pushed up on her forehead, work boots, a bag of crisps sticking out of her pocket",
    "5": "a short-legged olive bib overall over a fitted black tank top, grease-stained, a rag hanging from her pocket, scuffed black boots, a bag of crisps in one hand",
}
DANZEL = {
    "1": "a crimson silk shirt with an open collar tucked into elegantly tailored cream-white trousers with a sharp crease, a thin brown belt, tan leather loafers, a tape measure around his neck",
    "2": "a deep red linen shirt with the sleeves rolled to the elbows, elegantly cut wide-leg cream-white trousers, a small gold chain, light brown suede shoes",
    "3": "a crimson silk shirt with an open collar tucked into elegantly tailored pure bright white trousers with a sharp crease, a thin brown belt, tan leather loafers, round red sunglasses worn on his face, nothing hanging around his neck",
}
FIGUREN = [("Yacht_Bibi", "Bibi", BIBI, ("A young", "A 25-year-old adult")),
           ("Yacht_Charly", "Charly", CHARLY, None),
           ("Yacht_Danzel", "Danzel", DANZEL, ("a young Japanese-French man", "a 30-year-old Japanese-French man with smooth youthful skin"))]


if NUR:
    FIGUREN = [f for f in FIGUREN if f[0] == NUR]
if NR:
    FIGUREN = [(b, n, {k: v for k, v in o.items() if k in NR}, a) for b, n, o, a in FIGUREN]


def kname(basis, nr):
    return "%s_Nach_%s" % (basis, nr)


EXTRA = {"Yacht_Danzel": [("white hair", "very light platinum blond hair")]}      # Runde 2: Haar wie im Kampf-Casting (JUNG)


def prompt_fuer(basis_preset, alt_neu, basis=None):
    p = basis_preset["sprite_prompt"]
    p = p.replace("from head to knees", "from head to feet, camera at chest height, straight-on eye-level view, natural body proportions").replace("head and knees inside", "head and feet inside")
    if alt_neu:
        assert alt_neu[0] in p, alt_neu
        p = p.replace(alt_neu[0], alt_neu[1], 1)
    for a, b in EXTRA.get(basis, []):
        p = p.replace(a, b)
    return p


def main():
    presets = dc.load_json(cd.F_PRESETS, None, "Studio")
    for basis, name, outfits, _ in FIGUREN:
        print("%-13s %s" % (basis, "/".join(outfits)))
    if not LOS:
        print("Probelauf - nichts geschrieben.")
        return
    st = cd.ps("/api/state")
    d = st["decks"]
    da = {c["name"]: c for c in d["outfit"]}
    for basis, name, outfits, _ in FIGUREN:
        for nr, outfit in outfits.items():
            kn = "%s_nach_%s" % (name.lower(), nr)
            if kn in da:
                da[kn]["prompt"] = outfit
            else:
                d["outfit"].append({"name": kn, "prompt": outfit, "on": True, "tag": TAG, "sel": False,
                                    "back_prompt": outfit + ", seen from behind"})
    cd.ps("/api/decks", d)
    neu = {}
    for basis, name, outfits, alt_neu in FIGUREN:
        b = presets[basis]
        for nr in outfits:
            pn = kname(basis, nr)
            kn = "%s_nach_%s" % (name.lower(), nr)
            p = json.loads(json.dumps(b))
            p.update({"sprite_prompt": prompt_fuer(b, alt_neu, basis),
                      "cards_on": {"outfit": [kn], "setting": ["A Sprite Background"], "st": ["neutral"]},
                      "st_set": "%s/%s" % (ORDNER, pn), "created": cd.JETZT, "updated": cd.JETZT})
            neu[pn] = p
    presets.update(neu)
    dc.save_json(cd.F_PRESETS, presets, "Studio")
    alt = {k: st["cfg"].get(k) for k in ("sprite_prompt", "loras", "st_set", "sprite_src", "tags", "unet", "clip", "seed")}
    alt_preset = st["cfg"].get("preset_active")
    n = 0
    try:
        for basis, name, outfits, _ in FIGUREN:
            for nr in outfits:
                pn = kname(basis, nr)
                kn = "%s_nach_%s" % (name.lower(), nr)
                cd.ps("/api/presets", {"action": "load", "name": pn})
                cfg = cd.ps("/api/state")["cfg"]
                print(pn, "Tags an:", [t["name"] for t in cfg["tags"] if t.get("on")])
                for s in cd.SEEDS:
                    cd.ps("/api/config", dict(cd.MODELL, tags=cfg["tags"], mode="sprite", sprite_src="t2i", combine_mode="all",
                                              view_pro_karte=False, st_rembg=True, st_crop=True, seed=s,
                                              st_set="%s/%s" % (ORDNER, pn), loras=neu[pn]["loras"],
                                              sprite_prompt=neu[pn]["sprite_prompt"]))
                    dk = cd.ps("/api/state")["decks"]
                    for kk in dk:
                        wahl = {"outfit": {kn}, "setting": {"A Sprite Background"}, "st": {"neutral"}}.get(kk, set())
                        for x in dk[kk]:
                            x["sel"] = x["name"] in wahl
                    n += cd.ps("/api/queue", {"cfg": {"combine_mode": "all"}, "decks": dk}).get("queued", 0)
    finally:
        if alt_preset:
            cd.ps("/api/presets", {"action": "load", "name": alt_preset})
        cd.ps("/api/config", {k: v for k, v in alt.items() if v is not None})
    print("%d Portraits in der Warteschlange -> expressions\\%s" % (n, ORDNER))


if __name__ == "__main__":
    main()
