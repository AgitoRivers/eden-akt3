# -*- coding: utf-8 -*-
r"""Casting Nebenfiguren-Outfits (Duc 01.11.2026): je Figur vier Varianten fuer ein alternatives Outfit bei Danzel:
W = ihr Wunsch, A = aesthetisch, K = Korsika-Urlaub, D = Danzels Fashion-Seite. Gleiches Verfahren wie casting_wunsch_outfits.py.

    casting_neben_outfits.py          Probelauf
    casting_neben_outfits.py --los [Figur ...]   Presets Neben_<Figur>_<W|A|K|D>, je 2 Portraits -> output\expressions\_casting_neben

Isabelle: Basis Yacht_Isabelle_A plus Krea_Chloe (Kanon, Leitfaden). Duc: Basis Kampf_DucErde mit Krea_Ducx, Rahmung wie die Yacht-Presets.
Kein Weiss bei Bibi, Charly und Duc: Weiss gehoert Mr. White. Casanova und Isabelle bleiben hochgeschlossen.
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

ORDNER, TAG = "_casting_neben", "eden_neben"
# Bibi und Charly: _Nach_1 hat dieselbe Figur mit Kamera auf Brusthoehe und Kopf bis Fuss; die Basis-Presets fotografieren von oben und zu nah
BASIS = {"Isabelle": "Yacht_Isabelle_A", "Casanova": "Yacht_Casanova", "Bibi": "Yacht_Bibi_Nach_1", "Charly": "Yacht_Charly_Nach_1", "Duc": "Kampf_DucErde", "Holm": "Yacht_Holm"}
OUTFITS = {
    "Isabelle": {
        "W": "a long grey-blue linen work dress with a high neck and rolled sleeves, a big canvas apothecary apron with bulging pockets full of herb bundles and one small scorch mark on the corner, small glass vials on a leather belt, sturdy brown lace-up boots",
        "A": "a long sage green cotton dress with long sleeves and a modest square neckline, a braided cord belt, a thin silver cross on a chain, flat tan sandals",
        "K": "a long pale blue cotton summer dress with short sleeves and a modest round neckline, a wide straw hat, a wicker basket of wild herbs on one arm, rope espadrilles",
        "D": "a dramatic floor-length midnight blue velvet coat dress inspired by a nun's habit, buttoned to the neck with rows of tiny brass buttons, a wide stiff cream collar, a narrow belt with a brass mortar charm, black boots",
    },
    "Casanova": {
        "W": "a fitted emerald green skirt suit with gold braid on the shoulders, a high-necked cream blouse, a wide blue, white and red French mayor's sash from shoulder to hip, one huge gold medal, red heels",
        "A": "a long terracotta silk dress with long sleeves and a high boat neck, a heavy gold necklace, gold sandals",
        "K": "a navy blue linen shirt dress buttoned at the collar and belted at the waist, a very wide straw hat, big round sunglasses, a red folding fan in one hand, gold sandals",
        "D": "a black and gold matador bolero jacket with heavy gold embroidery over a high-necked black blouse, high-waisted long black trousers, a long red cape over one shoulder, black heels",
    },
    "Bibi": {
        "W": "a sand-coloured safari shirt with rolled sleeves and many pockets, knotted at the waist, olive cargo shorts, worn brown hiking boots, a leather satchel, a small plush lion keychain that is entirely jet black on her belt",
        "A": "a bright coral silk wrap top and matching wide silk trousers, gold hoop earrings, tan sandals",
        "K": "an open oversized black short-sleeved shirt with a big lion print worn over a cropped top of thick opaque shiny metallic gold satin, tight short black shorts that hug her hips, round sunglasses, canvas sneakers, her skin and clothes completely dry and clean, soft matte skin",
        "D": "a red satin jacket with huge puffed shoulders and a dramatic collar of layered black silk ruffles like a lion's mane, a fitted black top, high-waisted red trousers, black boots",
    },
    "Charly": {
        "W": "an oversized black hoodie printed with three tiny red pixel-art figures, loose charcoal joggers, black sneakers, a headset around her neck, a bag of crisps in one hand",
        "A": "a charcoal grey tailored waistcoat buttoned over a burgundy silk shirt, matching wide-leg charcoal trousers, a slim gold watch, black loafers",
        "K": "a navy and red striped short-sleeved Breton T-shirt with a high round neck, navy linen shorts, oversized dark sunglasses, a tan canvas tote bag on one shoulder, red espadrilles",
        "D": "a long asymmetric scarlet tuxedo coat with black satin lapels and sharply pointed shoulders, a high-necked black top, narrow black trousers, pointed black boots, a small gold number 10 pin on the lapel",
    },
    "Duc": {
        "W": "a relaxed dark navy linen blazer with the sleeves pushed up over a charcoal T-shirt, slim stone-coloured chinos, brown leather boat shoes, a steel diver's watch, a small gold anchor pin on the lapel",
        "A": "a soft sage green linen shirt open at the collar, dark olive tailored trousers, tan suede loafers, a brown leather belt",
        "K": "a faded terracotta short-sleeved linen shirt, navy swim shorts, rope sandals, sunglasses hanging from the collar, a blue striped kitchen towel over one shoulder",
        "D": "a deep emerald velvet double-breasted suit with wide peaked black satin lapels and gold buttons, a black silk shirt open at the neck, polished black shoes",
    },
    # Ersatz fuer Night Watch (Leder und Schal, zu warm fuer Korsika): N = dunkle Sommeruniform, K = Tropen-Khaki, P = Arbeitsuniform. Kein Kompass: den gibt sie bei der Uebergabe an Duc weiter
    "Holm": {
        "N": "a dark navy short-sleeved captain's uniform shirt buttoned to the collar with plain clean sleeves, black shoulder epaulettes with exactly four gold stripes each, long dark navy uniform trousers with a brown leather belt, binoculars hanging around her neck, black leather boat shoes",
        "K": "a sand khaki short-sleeved officer's uniform shirt with two chest pockets and plain clean sleeves, black shoulder epaulettes with exactly four gold stripes each, long pressed sand khaki uniform trousers with a brown leather belt, brown leather boat shoes",
        "M": "a clean, freshly washed, softly wrinkled warm cream-beige cotton blouse, open at the top with the sleeves rolled up to the elbows and plain clean sleeves, black shoulder tabs with exactly four gold stripes each, a plain solid navy tank top underneath, clean long navy uniform trousers tucked into old brown leather ankle boots, a brown leather belt",
        "P": "a dark navy short-sleeved polo shirt with four small straight horizontal gold bars embroidered on the chest, tailored knee-length sand khaki uniform shorts with a brown leather belt, a steel diver's watch, binoculars hanging around her neck, brown leather deck shoes",
    },
}
DUC_RAHMEN = ("{tags_action}, Shot on an iPhone, grainy amateur photo, realistic smartphone photography, full body shot from head to knees, direct gaze, "
              "one single man alone in the frame, his whole body in full view, head and knees inside the frame,")
CHLOE = {"name": "Krea_Chloe.safetensors", "strength": 0.9}
HOLM_SUBJEKT = ("Subject: Captain Rosamund, a 52-year-old Norwegian woman, tall with strong shoulders, a weathered sun-tanned face with fine lines around the eyes, "
                "dark brown hair with the first grey strands, light blue eyes, dry matte skin,")


def basis_preset(presets, figur):
    p = json.loads(json.dumps(presets[BASIS[figur]]))
    if figur == "Isabelle" and not any(l["name"] == CHLOE["name"] for l in p["loras"]):
        p["loras"].append(dict(CHLOE))
    if figur == "Bibi":                  # Sheen macht im Casting nasse Haut und Tropfen auf der Kleidung
        p["tags_on"] = [t for t in p["tags_on"] if t != "Sheen"]
    if figur == "Holm":                  # das Preset sagt nur "female with light blue eyes" und liefert eine Mittzwanzigerin; Trigger und Figur wie in ihren Sprites, Alter und Haar aus dem Wiki
        p["sprite_prompt"] = p["sprite_prompt"].replace("{tags_action},", "RosamundPike, {tags_action},", 1).replace("Subject: female with light blue eyes,", HOLM_SUBJEKT)
    if figur == "Duc":
        zeilen = p["sprite_prompt"].split("\n")
        zeilen[0] = DUC_RAHMEN
        text = "\n".join(zeilen).replace("Scene: {setting},\n{kampf},", "Scene: {setting}, {st},\n{expression},\nLook: {look},")
        p.update({"sprite_prompt": text, "tags_on": ["View: Front"], "sp_stchar": "Duc"})
    return p


def main():
    plan = {f: {a: t for a, t in o.items() if not NUR or f in NUR or "%s:%s" % (f, a) in NUR} for f, o in OUTFITS.items()}      # Figur oder Figur:Art, z. B. Bibi:K
    plan = {f: o for f, o in plan.items() if o}
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
            kn = "neben_%s_%s" % (figur.lower(), art)
            if kn in da:
                da[kn]["prompt"] = outfit
            else:
                d["outfit"].append({"name": kn, "prompt": outfit, "on": True, "tag": TAG, "sel": False, "back_prompt": outfit + ", seen from behind"})
            pn = "Neben_%s_%s" % (figur, art)        # nicht Yacht_*: Yacht_Isabelle_A ist Isabelles echtes Preset (Kollision 01.11.)
            p = basis_preset(presets, figur)
            if (figur, art) == ("Holm", "M"):    # Duc 01.11.: erschoepft, offene zerzauste Haare statt Hochsteckfrisur
                p["tags_on"] = [t for t in p["tags_on"] if t != "Style: Updo"]
                p["sprite_prompt"] = p["sprite_prompt"].replace("{tags_hairstyle}", "long loose messy tousled dry hair falling over her shoulders, a few strands across her face").replace(
                    "dry matte skin,", "dry matte skin, tired eyes with faint shadows under them,").replace(      # "worn out" brachte Dreck, Flecken und Schweiss (erste Runde)
                    "from head to knees", "from head to feet").replace("head and knees inside", "head and both boots inside")      # Stiefel gehoeren zum Look
            p.update({"cards_on": {"outfit": [kn], "setting": ["A Sprite Background"], "st": ["neutral"]},
                      "st_set": "%s/%s" % (ORDNER, pn), "created": cd.JETZT, "updated": cd.JETZT})
            neu[pn] = p
    cd.ps("/api/decks", d)
    presets.update(neu)
    dc.save_json(cd.F_PRESETS, presets, "Studio")
    alt = {k: st["cfg"].get(k) for k in ("sprite_prompt", "loras", "st_set", "sprite_src", "tags", "unet", "clip", "seed", "st_rembg", "st_crop", "aspect", "width", "height")}
    alt_preset = st["cfg"].get("preset_active")
    n = 0
    try:
        for pn, p in neu.items():
            kn = p["cards_on"]["outfit"][0]
            cd.ps("/api/presets", {"action": "load", "name": pn})
            cfg = cd.ps("/api/state")["cfg"]
            for s in cd.SEEDS:
                cd.ps("/api/config", dict(tags=cfg["tags"], mode="sprite", sprite_src="t2i", combine_mode="all", view_pro_karte=False, st_rembg=False, st_crop=False, aspect="880x1328", width=880, height=1328,
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
