# -*- coding: utf-8 -*-
r"""Bilder fuer den Kuechenkreis (Duc 27.10.2026, E-079): Tier-Sprites, Fisch-Sprites, Rohformen und Tierprodukte als Items.

    Kochen_Bilder.bat                    alles, was noch fehlt
    Kochen_Bilder.bat tiere              nur Tiere (3 Arten x 5 Varianten: baby, adult_m, adult_f, old_m, old_f)
    Kochen_Bilder.bat fische sea_bass    nur diese Fische (neu, ueberschreibt)
    Kochen_Bilder.bat roh | produkte     Rohformen der Fische bzw. Eier, Milch, Trueffel, Fleisch (Item-Bilder, 320er WebP)
    Kochen_Bilder.bat zutaten            Basis, Garten, Wuerze und Vorschlaege aus der Annahme-Liste (Item-Bilder)
Angeschnittene Sprites werden bis zu VERSUCHE-mal mit neuem Seed wiederholt.
    Kochen_Bilder.bat --liste            nur zeigen, was fehlt

Braucht ComfyUI Krea2 (Port 8189) mit dem easy-use-Knoten "imageRemBg" (BEN2). Sprites entstehen auf hellem Grund und werden
freigestellt (RGBA-PNG, hoechstens 640 px): module\eden_rise\farm\tiere\<art>_<variante>.png, farm\fische\<id>.png. Items:
module\eden_rise\items\<id>.webp (wie item_bilder.py, Leinen-Look). Motive stehen in module\eden_rise\kuechen.json (Builder
werkzeuge\eden_rise\kochen_eden_rise.py / kochen_daten.py). Gleicher Look wie die uebrigen Gegenstaende: Krea 2 mit dem LoRA-Profil
aus item_bilder.py (positiv formuliert, CFG 1: kein Negativ-Prompt wirkt)."""
import json, os, random, sys, time

from PIL import Image

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import item_bilder as IB  # noqa: E402

EDEN = IB.EDEN
MOD = os.path.join(EDEN, "module", "eden_rise")
MAXPX = 640
GRUND = "on a plain pale grey studio background, soft even light, a single subject, nothing else in the frame"
TIER_STIL = "Photograph of {motiv}, full body, standing, seen from the side in a slight three-quarter view, {grund}, photorealistic, sharp detail, no text"
FISCH_STIL = ("Photograph of {motiv}, the entire animal seen from the side, horizontal, fully inside the frame with a wide empty margin on all "
              "sides so that head, tail and fins are completely visible, the animal fills only about two thirds of the frame width, {grund}, "
              "photorealistic, sharp detail, no text")
# Babys: ein eigenes Motiv (das Modell macht aus "a baby" sonst ein erwachsenes Tier in klein)
BABY = {"chicken": "a fluffy yellow baby chick, tiny, with small orange legs and a round soft body",
        "pig": "a small piglet, tiny, pink with black patches and floppy ears, short legs",
        "cow": "a small newborn Pisana calf with a smooth rounded hornless head, leggy with large soft ears, a solid very dark chestnut coat that looks almost black"}
PRODUKTE = {
    "eggs": "six fresh brown eggs in a small wire basket",
    "milk": "a glass bottle of fresh whole milk with a wooden stopper beside a small white jug",
    "truffle": "two black truffles with a small brush, the earthy rough skin showing",
    "chicken_meat": "a plucked raw whole chicken on a sheet of white butcher paper",
    "pork": "a raw piece of marbled dark pork shoulder on a sheet of white butcher paper",
    "beef": "a thick raw beef steak on a sheet of white butcher paper",
    "salmon_steak": "two thick raw salmon steaks on a sheet of white butcher paper",
    # Baumaterial fuer die Staelle (27.10.2026)
    "timber": "a neat stack of split oak firewood logs in crossing layers, pale triangular split faces, rough dark bark on the outer side",
    "slate": "a rough stack of thin dark blue-grey slate slabs, layered split plates with sharp broken edges, matte stone",
    "granite": "a heap of coarse split granite chunks, sharp angular faces, rough speckled grey crystalline matte stone",
    "iron": "a handful of old forged iron hinges, brackets and square nails on a piece of sackcloth",
}
# Zutaten ohne Bild (Duc 28.10.2026, Annahme-Liste): Basis, Garten, Wuerze, Tofu und die Vorschlaege. Positiv formuliert.
ZUTATEN = {
    "rice": "a small linen sack of white long-grain rice with a wooden scoop, a few grains spilled on the cloth",
    "noodles": "a loose bundle of dried golden wheat noodles tied with kitchen string",
    "flour": "a small ceramic bowl full of white flour with a wooden scoop, a light dusting of flour around it",
    "potatoes": "a handful of fresh yellow potatoes with a little dry soil on their smooth skins",
    "cabbage": "a whole fresh green savoy cabbage with crinkled outer leaves",
    "zucchini": "three fresh green zucchini, one still with its yellow blossom attached",
    "chilis": "a small pile of fresh glossy red chillies with green stems",
    "wildkraeuter": "a loose bunch of fresh wild herbs, rosemary, thyme and wild fennel, tied with twine",
    "zitronen": "three fresh Amalfi lemons with their green leaves still attached",
    "tomaten": "a vine of ripe glossy red cherry tomatoes",
    "knoblauch": "two whole bulbs of purple-skinned garlic and a few loose cloves",
    "sojasauce": "a small glass bottle of dark soy sauce beside a little shallow white dish of soy sauce",
    "tofu": "a block of fresh smooth white tofu on a small wooden board, one clean slice cut off",
    "mushrooms": "a handful of fresh porcini mushrooms with thick pale stems and brown caps",
    "aubergine": "two glossy dark purple aubergines with green caps",
    "pumpkin": "a small whole orange pumpkin with a ridged skin and a short curly stem",
    "leek": "two fresh leeks with long white stems and dark green tops",
    "beetroot": "three whole fresh beetroots with their red-veined leafy stems",
    "mussels": "a heap of fresh blue-black mussels with closed glossy shells",
    "sausages": "a coil of fresh raw Italian pork sausages on a sheet of white butcher paper",
    "wild_boar": "a raw piece of dark red wild boar meat with a sprig of rosemary on a sheet of white butcher paper",
    "pasta": "a loose nest of fresh golden tagliatelle lightly dusted with flour",
    "rice_paper": "a short stack of round thin translucent rice paper sheets",
    "onion": "two golden brown onions and one red onion",
    "saffron": "a small glass jar of deep red saffron threads with a few threads beside it",
    "bay_leaf": "a small sprig of fresh dark green bay leaves",
    "dill": "a fresh bunch of feathery green dill tied with twine",
    "fish_sauce": "a small glass bottle of clear amber fish sauce beside a little white dish of it",
    "butter": "a block of pale yellow butter on greaseproof paper with a small butter knife",
    "cream": "a small glass jug of fresh thick white cream",
    "vinegar": "a small glass bottle of red wine vinegar with a cork stopper",
}
# Fisch-Sprites ohne Eintrag in kuechen.json (der Lachs steht seit 28.10. als Fisch in kochen_daten.py)
EXTRA_FISCHE = {}
DREHEN = {"river_crab": 90}       # Grad gegen den Uhrzeigersinn (Duc 28.10.: Scheren nach oben wie die Rohform)
VERSUCHE = 3                      # angeschnittene Sprites so oft mit neuem Seed neu erzeugen


def daten():
    return json.load(open(os.path.join(MOD, "kuechen.json"), encoding="utf-8"))


def aufgaben(d, art, nur):
    """-> [(ziel_pfad, prompt, typ)] fuer Sprites ("sprite") und Items ("item")."""
    out = []
    if art in ("tiere", "alles"):
        for tid, t in d["tiere"].items():
            for v in d["tier_varianten"]:
                wer = {"baby": "a baby", "adult_m": "an adult male", "adult_f": "an adult female", "old_m": "an old male with a weathered look",
                       "old_f": "an old female with a weathered look"}[v]
                motiv = BABY[tid] if v == "baby" else t["motiv"].replace("a ", wer + " ", 1) if t["motiv"].startswith("a ") else wer + " " + t["motiv"]
                out.append((os.path.join(MOD, "farm", "tiere", "%s_%s.png" % (tid, v)), TIER_STIL.format(motiv=motiv, grund=GRUND), "sprite"))
    if art in ("fische", "alles"):
        for f in d["fische"]:
            out.append((os.path.join(MOD, "farm", "fische", f["id"] + ".png"), FISCH_STIL.format(motiv=f["motiv"], grund=GRUND), "sprite"))
        for fid, motiv in EXTRA_FISCHE.items():
            out.append((os.path.join(MOD, "farm", "fische", fid + ".png"), FISCH_STIL.format(motiv=motiv, grund=GRUND), "sprite"))
    if art in ("zutaten", "alles"):
        for iid, motiv in ZUTATEN.items():
            out.append((os.path.join(MOD, "items", iid + ".webp"), IB.STIL.format(motiv=motiv, hintergrund=IB.HINTERGRUENDE[IB.HINTERGRUND]), "item"))
    if art in ("roh", "alles"):
        for f in d["fische"]:
            out.append((os.path.join(MOD, "items", f["roh"] + ".webp"), IB.STIL.format(motiv=f["motiv_roh"], hintergrund=IB.HINTERGRUENDE[IB.HINTERGRUND]), "item"))
    if art in ("produkte", "alles"):
        for iid, motiv in PRODUKTE.items():
            out.append((os.path.join(MOD, "items", iid + ".webp"), IB.STIL.format(motiv=motiv, hintergrund=IB.HINTERGRUENDE[IB.HINTERGRUND]), "item"))
    if nur:
        out = [a for a in out if os.path.splitext(os.path.basename(a[0]))[0] in nur]
    return out


def graph_mit_freistellung(prompt, ordner, name, seed):
    """Krea-2-Graph aus item_bilder plus BEN2-Freistellung: speichert <name>.png (RGB) und <name>_maske.png."""
    g = IB.graph(prompt, ordner, name, seed, IB.nsfw_an(name))
    g["10"] = {"class_type": "easy imageRemBg", "inputs": {"images": ["8", 0], "rem_mode": "BEN2", "image_output": "Hide", "save_prefix": "cut",
                                                            "torchscript_jit": False, "add_background": "none", "refine_foreground": False}}
    g["11"] = {"class_type": "MaskToImage", "inputs": {"mask": ["10", 1]}}
    g["12"] = {"class_type": "DucSave", "inputs": {"images": ["11", 0], "save_path": ordner, "filename_prefix": name + "_maske",
                                                   "use_input_filename": False, "image_format": "PNG", "jpg_quality": 95,
                                                   "counter_style": "NONE", "show_preview": False, "overwrite": True}}
    return g


def angeschnitten(maske):
    """True, wenn das Motiv den Bildrand beruehrt (Tier oder Fisch ist angeschnitten und sollte neu erzeugt werden)."""
    px = maske.point(lambda v: 255 if v > 60 else 0)
    w, h = px.size
    return any(px.crop(box).getbbox() for box in ((0, 0, w, 1), (0, h - 1, w, h), (0, 0, 1, h), (w - 1, 0, w, h)))


def sprite_fertig(ordner, name, ziel, letzter=True):
    """RGB + Maske -> RGBA, auf das Motiv zugeschnitten, hoechstens MAXPX. -> False, wenn angeschnitten (dann nur beim letzten
    Versuch trotzdem speichern)."""
    rgb = Image.open(os.path.join(ordner, name + ".png")).convert("RGB")
    maske = Image.open(os.path.join(ordner, name + "_maske.png")).convert("L")
    ok = not angeschnitten(maske)
    if not ok and not letzter:
        return False
    if not ok:
        print("ACHTUNG angeschnitten: %s - neu erzeugen: Kochen_Bilder.bat %s" % (name, name))
    rgba = rgb.copy()
    rgba.putalpha(maske)
    box = maske.point(lambda v: 255 if v > 24 else 0).getbbox()
    if box:
        rgba = rgba.crop(box)
    if name in DREHEN:
        rgba = rgba.rotate(DREHEN[name], expand=True)
    rgba.thumbnail((MAXPX, MAXPX), Image.LANCZOS)
    os.makedirs(os.path.dirname(ziel), exist_ok=True)
    rgba.save(ziel, "PNG", optimize=True)
    return ok


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    d = daten()
    arten = ("tiere", "fische", "roh", "produkte", "zutaten")
    ziele = [a for a in sys.argv[1:] if a in arten]
    art = ziele[0] if ziele else "alles"
    nur = {a for a in sys.argv[1:] if not a.startswith("-") and a not in arten}
    jobs = aufgaben(d, art, nur)
    fehlt = [a for a in jobs if nur or not os.path.exists(a[0])]
    if "--liste" in sys.argv:
        print("%d von %d Bildern fehlen:" % (len(fehlt), len(jobs)))
        for a in fehlt:
            print("  ", os.path.relpath(a[0], EDEN))
        return
    if not fehlt:
        print("Alle %d Bilder sind da. (Einzelne neu: Kochen_Bilder.bat <art> <id>)" % len(jobs))
        return
    try:
        IB.get("/system_stats")
    except Exception:
        sys.exit("ComfyUI Krea2 laeuft nicht (Port 8189) - erst starten, dann nochmal.")
    gross = os.path.join(MOD, "farm", "_gross")
    os.makedirs(gross, exist_ok=True)
    def einreihen(name, prompt, typ):
        seed = random.randint(1, 2 ** 31)
        g = graph_mit_freistellung(prompt, gross, name, seed) if typ == "sprite" else IB.graph(prompt, gross, name, seed, IB.nsfw_an(name))
        return IB.post("/prompt", {"prompt": g})["prompt_id"]

    auftraege = {}
    for ziel, prompt, typ in fehlt:
        name = os.path.splitext(os.path.basename(ziel))[0] + ("" if typ == "sprite" else "_item")
        auftraege[name] = (einreihen(name, prompt, typ), ziel, typ, prompt, 1)
        print("eingereiht: %-26s %s" % (name, prompt[:60]))
    offen, t0 = dict(auftraege), time.time()
    while offen and time.time() - t0 < 60 * 45:
        time.sleep(2)
        for name, (pid, ziel, typ, prompt, versuch) in list(offen.items()):
            h = IB.get("/history/" + pid)
            if pid in h and h[pid].get("status", {}).get("completed"):
                try:
                    if typ == "sprite":
                        if not sprite_fertig(gross, name, ziel, letzter=versuch >= VERSUCHE) and versuch < VERSUCHE:
                            offen[name] = (einreihen(name, prompt, typ), ziel, typ, prompt, versuch + 1)
                            print("angeschnitten, Versuch %d: %s" % (versuch + 1, name))
                            continue
                    else:
                        with Image.open(os.path.join(gross, name + ".png")) as im:
                            im = im.convert("RGB")
                            im.thumbnail((IB.THUMB, IB.THUMB), Image.LANCZOS)
                            im.save(ziel, "WEBP", quality=85, method=6)
                    print("fertig:     %s" % os.path.relpath(ziel, EDEN))
                except Exception as e:
                    print("FEHLER %s: %s" % (name, e))
                offen.pop(name)
    print("%d Bilder fertig%s" % (len(auftraege) - len(offen), (", noch offen: " + ", ".join(offen)) if offen else ""))


if __name__ == "__main__":
    main()
