# -*- coding: utf-8 -*-
r"""Bilder fuers Abbauen an Rastplaetzen (Duc 28.10.2026): Baum- und Felsen-Sprites, Werkzeug-Icons und das Kork-Item.

    python werkzeuge\abbau_bilder.py              fehlende Bilder erzeugen + Abnahme-Spec schreiben
    python werkzeuge\abbau_bilder.py holm_oak     nur diese (neu, ueberschreibt)
    python werkzeuge\abbau_bilder.py --spec       nur docs\abnahme\abbau_bilder.json schreiben

Sprites (freigestellt wie kochen_bilder.py): module\eden_rise\farm\abbau\<typ>.png - der Baum faellt, der Fels bricht im Minispiel
(client/plugins/eden-abbau). Items (Leinen-Look wie item_bilder.py): module\eden_rise\items\<id>.webp fuer axe_1..3, pickaxe_1..3,
cork. Positiv formuliert (Krea CFG 1: Verneinungen wirken nicht)."""
import json, os, random, sys, time

from PIL import Image

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import kochen_bilder as K  # noqa: E402

IB = K.IB
ZIEL = os.path.join(K.MOD, "farm", "abbau")
ITEMS = os.path.join(K.MOD, "items")
SPEC = os.path.join(K.EDEN, "docs", "abnahme", "abbau_bilder.json")

BAUM_STIL = ("Photograph of {motiv}, the whole tree from the roots to the top of the crown, standing upright, fully inside the frame "
             "with a wide empty margin on all sides, the tree fills about two thirds of the frame height, {grund}, photorealistic, "
             "sharp detail, no text")
FELS_STIL = ("Photograph of {motiv}, the whole rock seen from the front, fully inside the frame with a wide empty margin on all "
             "sides, the rock fills about two thirds of the frame width, {grund}, photorealistic, sharp detail, no text")
SPRITES = {   # typ: (Titel, Stil, Motiv, Breite, Hoehe)
    "holm_oak": ("Steineiche", BAUM_STIL, "a young holm oak tree, a straight sturdy trunk with dark grey bark, a dense rounded crown of "
                 "small dark evergreen leaves", 896, 1152),
    "cork_oak": ("Korkeiche (geschält)", BAUM_STIL, "a young cork oak tree, the lower half of the trunk freshly harvested and glowing a warm "
                 "rusty red-orange, smooth thick pale cork bark in soft ridges above it, a rounded crown of grey-green leaves", 896, 1152),
    "granite": ("Granitfels", FELS_STIL, "a large weathered grey granite boulder with smooth rounded edges and a few soft green moss "
                "patches at its base", 1152, 896),
    "schist": ("Schieferfels", FELS_STIL, "a large layered slate-grey schist rock with flat stacked layers and clean sharp edges, a "
               "little dry grass at its base", 1152, 896),
}
ITEM_MOTIVE = {   # id: (Titel, Motiv)
    "axe_1": ("Axt Stufe 1 · Old Hatchet", "an old small hatchet with a worn smooth ash-wood handle and a dull dark iron head"),
    "axe_2": ("Axt Stufe 2 · Forester's Axe", "a well-balanced forester's axe with a new pale hickory handle and a freshly forged bright "
              "steel head with a sharp edge"),
    # Duc 28.10. (Abnahme): Stufe 3 ganz im Bild, Quarry Pick mit dunklem Holzstiel
    "axe_3": ("Axt Stufe 3 · Tempered Axe", "a master-forged axe with a hardened blue-black steel head, a mirror-bright honed edge and a "
              "dark leather-wrapped handle, the whole axe lying diagonally and small in the frame, head and handle end fully visible "
              "with a wide empty margin of linen on all sides"),
    "pickaxe_1": ("Spitzhacke Stufe 1 · Old Pick", "an old pickaxe with a worn ash-wood handle and a dull dark iron head"),
    "pickaxe_2": ("Spitzhacke Stufe 2 · Quarry Pick", "a sturdy quarryman's pickaxe with a dark walnut-brown wooden handle, oiled and "
                  "smooth, and a freshly forged bright steel head with sharp points"),
    "pickaxe_3": ("Spitzhacke Stufe 3 · Tempered Pick", "a master-forged pickaxe with a hardened blue-black steel head, bright honed "
                  "points and a dark leather-wrapped handle, the whole pickaxe lying diagonally and small in the frame, both points and "
                  "the handle end fully visible with a wide empty margin of linen on all sides"),
    "cork": ("Kork (Rohstoff)", "two curved slabs of fresh natural cork bark, pale tan outside and warm golden-brown inside, smooth and "
             "light, tied with a strip of raffia"),
}


def jobs(nur):
    out = []
    for typ, (_, stil, motiv, b, h) in SPRITES.items():
        out.append((typ, os.path.join(ZIEL, typ + ".png"), stil.format(motiv=motiv, grund=K.GRUND), "sprite", (b, h)))
    for iid, (_, motiv) in ITEM_MOTIVE.items():
        out.append((iid, os.path.join(ITEMS, iid + ".webp"), IB.STIL.format(motiv=motiv, hintergrund=IB.HINTERGRUENDE[IB.HINTERGRUND]),
                    "item", None))
    return [j for j in out if not nur or j[0] in nur]


def erzeugen(nur):
    gross = os.path.join(K.MOD, "farm", "_gross")
    os.makedirs(gross, exist_ok=True)
    os.makedirs(ZIEL, exist_ok=True)

    def einreihen(name, prompt, typ, groesse):
        seed = random.randint(1, 2 ** 31)
        g = K.graph_mit_freistellung(prompt, gross, name, seed) if typ == "sprite" else IB.graph(prompt, gross, name, seed, False)
        if groesse:
            g["6"]["inputs"].update({"width": groesse[0], "height": groesse[1]})
        return IB.post("/prompt", {"prompt": g})["prompt_id"]

    offen = {}
    for name, ziel, prompt, typ, groesse in jobs(nur):
        if nur or not os.path.exists(ziel):
            key = name + ("" if typ == "sprite" else "_item")
            offen[key] = (einreihen(key, prompt, typ, groesse), ziel, prompt, typ, groesse, 1)
    print("eingereiht: %d" % len(offen), flush=True)
    t0 = time.time()
    while offen and time.time() - t0 < 60 * 30:
        time.sleep(2)
        for key, (pid, ziel, prompt, typ, groesse, versuch) in list(offen.items()):
            h = IB.get("/history/" + pid)
            if not (pid in h and h[pid].get("status", {}).get("completed")):
                continue
            if typ == "sprite":
                if not K.sprite_fertig(gross, key, ziel, letzter=versuch >= K.VERSUCHE) and versuch < K.VERSUCHE:
                    offen[key] = (einreihen(key, prompt, typ, groesse), ziel, prompt, typ, groesse, versuch + 1)
                    print("angeschnitten, Versuch %d: %s" % (versuch + 1, key), flush=True)
                    continue
            else:
                with Image.open(os.path.join(gross, key + ".png")) as im:
                    im = im.convert("RGB")
                    im.thumbnail((IB.THUMB, IB.THUMB), Image.LANCZOS)
                    im.save(ziel, "WEBP", quality=85, method=6)
            print("fertig: %s" % os.path.relpath(ziel, K.EDEN), flush=True)
            offen.pop(key)
    print("offen: %s" % (", ".join(offen) or "nichts"))


def spec():
    items = [{"id": typ, "titel": "Sprite · " + t[0], "bild": os.path.join(ZIEL, typ + ".png"),
              "soll": "Ganzes Motiv freigestellt, nichts angeschnitten. Im Minispiel fällt der Baum bzw. bricht der Fels."}
             for typ, t in SPRITES.items()]
    items += [{"id": iid, "titel": t[0], "bild": os.path.join(ITEMS, iid + ".webp"),
               "soll": "Icon bei Petru und in der Werkzeug-Anzeige. Stufen sollen sich klar unterscheiden." if iid != "cork"
               else "Rohstoff-Icon für Kork (Beiprodukt der Korkeiche)."} for iid, t in ITEM_MOTIVE.items()]
    json.dump({"id": "abbau_bilder", "titel": "Abbauen – Bäume, Felsen, Werkzeuge",
               "hinweis": "Sprites fürs Minispiel an den Rastplätzen und die Icons in Petrus Werkstatt. OK oder Notiz je Bild.",
               "items": items}, open(SPEC, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Spec: %s (%d Bilder)" % (SPEC, len(items)))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    nur = {a for a in sys.argv[1:] if not a.startswith("-")}
    if "--spec" not in sys.argv:
        IB.get("/system_stats")
        erzeugen(nur)
    spec()
