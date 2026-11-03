# -*- coding: utf-8 -*-
r"""Casting Wunsch-Outfits (Duc 31.10.2026): je Frau vier Varianten fuer ihr alternatives Outfit bei Danzel:
W = ihr Wunsch, A = aesthetisch, K = Korsika-Urlaub, D = Danzels Fashion-Seite. Bei Chiara steht W schon (casting_dress_whites.py).

    casting_wunsch_outfits.py          Probelauf
    casting_wunsch_outfits.py --los [Figur ...]   Presets Yacht_<Figur>_<W|A|K|D>, je 2 Portraits -> output\expressions\_casting_wunsch

Die Basis-Presets bleiben unberuehrt: Tags, Subject und LoRAs kommen live aus dem Preset, nur Outfit-Karte und Zielordner sind neu.
"""
import json, os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, r"X:\AI\DucCommon")
LOS = "--los" in sys.argv
NUR = [a for a in sys.argv[1:] if not a.startswith("-")]
sys.argv = [sys.argv[0]] + (["--los"] if LOS else [])
import castings_danzel as cd  # noqa: E402
import duc_common as dc  # noqa: E402

ORDNER, TAG = "_casting_wunsch", "eden_wunsch"
OUTFITS = {
    "Lea": {
        "W": "a short shimmering bronze-gold sea silk slip dress that fits her perfectly, thin straps and a deep neckline, tiny hand-embroidered squid along the hem, barefoot",
        "A": "a soft seafoam green silk sundress with thin straps and a deep neckline, a flowing skirt to the knee, a thin silver chain, flat white sandals",
        "K": "a navy and white striped Breton crop top with a wide neck, faded coral cotton shorts, a straw bucket hat, rope espadrilles",
        "D": "a deep red silk one-shoulder cocktail dress with one sculpted fabric shoulder shaped like a seashell, a wide black satin sash at the waist, black strappy heels",
    },
    "Sophia": {
        "W": "a belted camel 1930s trench coat worn open over a low-cut cream silk blouse and a dark pencil skirt, a slim felt hat tilted to one side, a pencil behind her ear, dark heels",
        "A": "a pale sage green silk slip top with a deep neckline, matching wide silk trousers and a long sage silk duster coat, thin gold earrings, nude sandals",
        "K": "a white linen halter top with a deep neckline tied at the neck, a long sunflower yellow wrap skirt with a high slit, a wide straw hat, gold sandals",
        "D": "a black velvet tuxedo dress with wide red satin lapels cut down to the waist, a sharply structured shoulder, one long red leather glove, black heels",
    },
    "Rosi": {
        "W": "a seamless one-piece leather racing jumpsuit in a very dark burgundy wine colour, 1950s motorcycle racer style, a single long zip in the centre, zipped closed from her crotch up to the middle of her chest and open above that, the leather smooth and plain with a wide belt-free waist, two thin cream stripes running unbroken from each shoulder to each wrist and from each hip to each ankle, black boots",
        "A": "a dusty rose satin camisole with a deep neckline, high-waisted cream wide-leg trousers, a thin gold necklace with a shell, flat sandals",
        "K": "a fitted olive green tank top with a deep neckline, white cotton shorts, a red silk scarf tied in her hair, round sunglasses, tan leather sandals",
        "D": "a red leather corset with polished brass hinges down both sides like a piece of sculpted armour, black high-waisted cigarette trousers, black ankle boots, thin black gloves",
    },
    "Lola": {
        "W": "sun-faded terracotta linen dungaree shorts worn over a bright white bikini top, half a name hand-stitched on the bib, a white shell necklace, gold hoop earrings, barefoot",
        "A": "a butter yellow linen wrap top with a deep neckline and a long matching linen skirt, a white shell necklace, gold hoop earrings, barefoot",
        "K": "a bright orange cotton bikini top, a long tangerine sarong knotted at the hip, a white shell necklace, gold hoop earrings, a wide straw hat, barefoot",
        "D": "a short red satin kimono dress cinched with a wide black sash tied in a huge sculptural bow at the back, a deep neckline, a white shell necklace, gold hoop earrings, black sandals",
    },
    "Siri": {
        "W": "bright yellow fisherman's oilskin bib trousers with the straps over a thin white tank top with a deep neckline, tall dark green rubber boots, her hair a little wind-blown",
        "A": "a long soft lilac silk gown draped from one shoulder with a deep neckline and a slit, a fine silver bracelet, silver sandals",
        "K": "a blue and white striped cotton sundress with thin straps and a deep neckline, tied at the waist, a wide straw hat, white rope espadrilles",
        "D": "a long blood red column gown with a tall standing collar that frames her face, a deep narrow plunge down the front, a long train, thin black gloves",
    },
    "Alva": {
        "W": "a black Andalusian traje corto: a short fitted black leather bolero jacket worn open over a black buttoned crop shirt with a deep neckline, her bare midriff showing, high-waisted black riding trousers, a flat wide-brimmed black Cordobes hat, black boots",
        "A": "a long ivory bias-cut silk dress with thin straps and a deep neckline, a heavy amber necklace, gold sandals",
        "K": "a terracotta off-the-shoulder linen blouse with a low neckline, a long white cotton skirt, big gold hoop earrings, tan leather sandals, a straw bag on one shoulder, both arms relaxed at her sides",
        "D": "an asymmetric black and red cape dress with one dramatic sleeve and one bare shoulder, a deep neckline, a tight black skirt with a red lining showing at the slit, black heels",
    },
    "Elsa": {
        "W": "a blue and white checked cotton summer dress with a deep neckline, a fitted waist and two very large front pockets, a small ticket book in one pocket, white canvas shoes, a silver whistle on a thin chain",
        "A": "a powder blue silk blouse with the top buttons open and a deep neckline, a high-waisted cream pencil skirt, thin gold earrings, nude heels",
        "K": "a white cotton crop top with a deep neckline, red cotton shorts, a straw sun hat pushed back, round sunglasses, white sneakers",
        "D": "a sharply tailored oxblood skirt suit with high peaked lapels and nothing visible beneath the jacket, thin black leather gloves, a small black pillbox hat, black heels",
    },
    "Megan": {
        "W": "a floor-length crimson commander's greatcoat with a tall stiff collar and gold shoulder boards, worn open over a black bustier, black leather gloves, black over-the-knee boots, the look of the final boss of an anime",
        "A": "a long liquid champagne satin bias-cut dress with thin straps and a deep neckline, black leather gloves, a small gold anchor pin, gold heels",
        "K": "a black one-piece swimsuit with a deep neckline, a white linen sarong, huge dark sunglasses, a very wide black straw hat, black leather gloves, gold sandals",
        "D": "a black sculpted bustier gown with structured shoulder plates in stiff black silk and a red-lined cape falling from them, a deep neckline, black leather gloves, black heels",
    },
    "Jana": {
        "W": "a white cotton wrap dress held together only by thick real sailor's rope knots at the shoulders and the waist, a deep neckline, a small silver bosun's whistle on a chain, white canvas shoes",
        "A": "a soft mint pleated mini dress with a small white collar and a low neckline, a thin gold necklace, white ballet flats",
        "K": "a white cotton sundress with a lemon print and thin straps, a low neckline, a straw boater hat with a yellow ribbon, flat rope sandals",
        "D": "a short red velvet coat dress with a huge sculpted collar and a low neckline, long black opera gloves, black ankle boots, a little too bold for her and she knows it",
    },
    "Chiara": {
        "A": "soft dove grey silk wide-leg trousers and a matching silk halter top with a deep neckline, a slim gold watch, silver sandals",
        "K": "a coral red linen halter top with a deep neckline, white high-waisted cotton shorts, a slim gold watch, rope espadrilles, a straw hat in her hand",
        "D": "a long oxblood velvet captain's frock coat with a black collar and brass buttons worn open over a black corset and black leather shorts, black boots",
    },
}


def main():
    plan = {f: o for f, o in OUTFITS.items() if not NUR or f in NUR}
    print({f: "".join(o) for f, o in plan.items()})
    if not LOS:
        print("Probelauf - nichts geschrieben.")
        return
    presets = dc.load_json(cd.F_PRESETS, None, "Studio")
    st = cd.ps("/api/state")
    d = st["decks"]
    da = {c["name"]: c for c in d["outfit"]}
    neu = {}
    for figur, looks in plan.items():
        for art, outfit in looks.items():
            kn = "wunsch_%s_%s" % (figur.lower(), art)
            if kn in da:
                da[kn]["prompt"] = outfit
            else:
                d["outfit"].append({"name": kn, "prompt": outfit, "on": True, "tag": TAG, "sel": False, "back_prompt": outfit + ", seen from behind"})
            pn = "Yacht_%s_%s" % (figur, art)
            p = json.loads(json.dumps(presets["Yacht_" + figur]))
            p.update({"cards_on": {"outfit": [kn], "setting": ["A Sprite Background"], "st": ["neutral"]},
                      "st_set": "%s/%s" % (ORDNER, pn), "created": cd.JETZT, "updated": cd.JETZT})
            neu[pn] = p
    cd.ps("/api/decks", d)
    presets.update(neu)
    dc.save_json(cd.F_PRESETS, presets, "Studio")
    alt = {k: st["cfg"].get(k) for k in ("sprite_prompt", "loras", "st_set", "sprite_src", "tags", "unet", "clip", "seed")}
    alt_preset = st["cfg"].get("preset_active")
    n = 0
    try:
        for pn, p in neu.items():
            kn = p["cards_on"]["outfit"][0]
            cd.ps("/api/presets", {"action": "load", "name": pn})
            cfg = cd.ps("/api/state")["cfg"]
            for s in cd.SEEDS:
                cd.ps("/api/config", dict(tags=cfg["tags"], mode="sprite", sprite_src="t2i", combine_mode="all", view_pro_karte=False, st_rembg=False, st_crop=False,
                                          seed=s, st_set=p["st_set"], loras=p["loras"], sprite_prompt=p["sprite_prompt"]))
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
