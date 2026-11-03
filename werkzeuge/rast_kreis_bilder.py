# -*- coding: utf-8 -*-
r"""Rundbilder fuer die Kreise an Rastplaetzen und neue Item-Bilder fuer Stein und Holz (Duc 30.10.2026).

    python werkzeuge\rast_kreis_bilder.py         alle Kandidaten erzeugen, Abnahme-Spec + Seite schreiben

Kandidaten liegen in docs\abnahme\rast_kreise\ und ueberschreiben nichts im Spiel. Duc: "Steine sollen bewusst grob sein und Holz ein
Holz Stack". Positiv formuliert (Krea CFG 1: Verneinungen wirken nicht)."""
import json, os, random, sys, time

from PIL import Image, ImageDraw

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import item_bilder as IB  # noqa: E402

EDEN = os.path.dirname(HIER)
ZIEL = os.path.join(EDEN, "docs", "abnahme", "rast_kreise")
ITEMS = os.path.join(EDEN, "module", "eden_rise", "items")
SPEC = os.path.join(EDEN, "docs", "abnahme", "rast_kreise.json")
SEEDS = 2

RUND_STIL = ("Photograph of {motiv}, close view, the subject centered and filling the frame, soft warm late-afternoon light, shallow "
             "depth of field, photorealistic, high detail, no text")
RUND = {
    "kreis_cork_oak": ("Kreis · Korkeiche", "the trunk of a cork oak tree in sunlit Mediterranean scrubland, the lower trunk freshly "
                       "harvested and glowing a warm rusty red-orange, thick pale ridged cork bark above it"),
    "kreis_holm_oak": ("Kreis · Steineiche", "the sturdy trunk and low branches of an old holm oak tree, dark grey furrowed bark, dense "
                       "small dark evergreen leaves around it"),
    "kreis_granite": ("Kreis · Granit", "a weathered grey granite outcrop on a Corsican mountainside, a fresh split face with a deep "
                      "crack, speckled crystalline stone, soft green moss at its foot"),
    "kreis_schist": ("Kreis · Schiefer", "a layered slate-grey schist rock face, flat stacked layers with clean sharp edges, a little "
                     "dry golden grass at its foot"),
}

SCHRAEG = ("seen from a slight three-quarter angle, standing on smooth folded cream linen fabric, soft even daylight, calm, minimal, "
           "lots of empty space around the object")
STEIN = {
    "stone_a": ("Stein A · Bruchstein-Haufen", "a rough pile of freshly broken field stones, jagged angular fragments with sharp fractured "
                "edges, matte dusty grey-brown surfaces"),
    "stone_b": ("Stein B · Granitbrocken", "a heap of coarse split granite chunks, sharp angular faces, rough speckled grey crystalline "
                "matte stone"),
    "stone_c": ("Stein C · Terrassensteine", "a rough stack of flat angular quarry stones from a dry stone terrace wall, irregular broken "
                "edges, matte ochre-grey stone flecked with lichen"),
    "stone_d": ("Stein D · Grobe Blöcke", "three large jagged rough-hewn blocks of grey fieldstone, crude chisel marks, sharp corners, "
                "matte dusty surface"),
}
HOLZ = {
    "timber_a": ("Holz A · Scheite", "a neat stack of split oak firewood logs in crossing layers, pale triangular split faces, rough dark "
                 "bark on the outer side"),
    "timber_b": ("Holz B · Holzstoß", "a small woodpile of stacked round logs, the cut ends facing forward with visible growth rings, "
                 "warm honey-brown wood, rough bark"),
    "timber_c": ("Holz C · Balken", "a crisscross stack of rough-sawn square timber beams, pale pine wood with axe marks and saw marks"),
    "timber_d": ("Holz D · Pyramide", "a pyramid stack of cut chestnut logs, warm reddish-brown wood, rough bark, pale round cut ends"),
}


def jobs():
    out = []
    for iid, (titel, motiv) in RUND.items():
        out.append((iid, titel, RUND_STIL.format(motiv=motiv), "rund", None))
    for iid, (titel, motiv) in STEIN.items():
        out.append((iid, titel, IB.STIL.format(motiv=motiv, hintergrund=SCHRAEG), "item", os.path.join(ITEMS, "stone.webp")))
    for iid, (titel, motiv) in HOLZ.items():
        out.append((iid, titel, IB.STIL.format(motiv=motiv, hintergrund=SCHRAEG), "item", os.path.join(ITEMS, "timber.webp")))
    return out


def rund_vorschau(gross, ziel):
    """So sieht es im Spiel aus: runder Ausschnitt mit Goldrand auf dunklem Grund."""
    with Image.open(gross) as im:
        im = im.convert("RGB").resize((280, 280), Image.LANCZOS)
    bild = Image.new("RGB", (320, 320), (16, 16, 22))
    maske = Image.new("L", (280, 280), 0)
    ImageDraw.Draw(maske).ellipse((0, 0, 279, 279), fill=255)
    bild.paste(im, (20, 20), maske)
    ImageDraw.Draw(bild).ellipse((17, 17, 302, 302), outline=(216, 189, 134), width=3)
    bild.save(ziel)


def erzeugen():
    os.makedirs(ZIEL, exist_ok=True)
    for _ in range(90):
        try:
            IB.get("/system_stats")
            break
        except Exception:
            time.sleep(2)
    offen, items = {}, []
    for iid, titel, prompt, typ, vergleich in jobs():
        for n in range(1, SEEDS + 1):
            name = "%s_%d" % (iid, n)
            offen[name] = (IB.post("/prompt", {"prompt": IB.graph(prompt, ZIEL, name, random.randint(1, 2 ** 31))})["prompt_id"], typ)
            it = {"id": name, "titel": "%s · Seed %d" % (titel, n),
                  "bild": os.path.join(ZIEL, name + ("_vorschau.png" if typ == "rund" else ".webp")),
                  "soll": ("Rundbild für den Kreis am Rastplatz, zeigt den runden Ausschnitt wie im Spiel." if typ == "rund"
                           else "Item-Bild: bewusst grob und kantig." if iid.startswith("stone") else "Item-Bild: ein Holzstapel.")}
            if vergleich:
                it.update(vergleich=vergleich, vergleich_titel="Aktuelles Bild")
            items.append(it)
    print("eingereiht: %d" % len(offen), flush=True)
    t0 = time.time()
    while offen and time.time() - t0 < 60 * 40:
        time.sleep(2)
        for name, (pid, typ) in list(offen.items()):
            h = IB.get("/history/" + pid)
            if not (pid in h and h[pid].get("status", {}).get("completed")):
                continue
            gross = os.path.join(ZIEL, name + ".png")
            IB.thumbnail(ZIEL, ZIEL, name)
            if typ == "rund":
                rund_vorschau(gross, os.path.join(ZIEL, name + "_vorschau.png"))
            print("fertig: %s" % name, flush=True)
            offen.pop(name)
    print("offen: %s" % (", ".join(offen) or "nichts"), flush=True)
    json.dump({"id": "rast_kreise_v1", "titel": "Rastplatz-Kreise, Stein und Holz",
               "hinweis": "Je Motiv das beste Bild mit OK markieren, den Rest mit Neu oder einer Notiz.",
               "items": items}, open(SPEC, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Spec: %s (%d Bilder)" % (SPEC, len(items)), flush=True)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    erzeugen()
