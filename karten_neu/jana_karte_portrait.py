# -*- coding: utf-8 -*-
r"""Jana Maihoff (19.10.2026): Char-Builder-Karte speichern und das Kartenbild (Portrait) einstellen.

    jana_karte_portrait.py          Probelauf
    jana_karte_portrait.py --los    Karte nach cards\Eden Yacht\Jana Maihoff.json, Portrait ans ENDE der Queue

Wie vorschau_erzeugen(nur=[], portrait=True), aber OHNE nach_vorn: das zoege alle wartenden Jana-Sprites vor
die anderen Figuren. Nur Jana geht nach SillyTavern (Duc: keine Maenner in ST); der PNG-Export (st_export)
folgt, wenn Portrait und Sprites fertig sind.
"""
import io, os, random, sys, time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, r"X:\AI\CharCreator")
LOS = "--los" in sys.argv
sys.argv = ["creator.py", "--no-browser"]
import creator as c  # noqa: E402

f = c.fig_laden("16f8e9cf3e9b")
k1 = f["kostueme"][0]
bg = c.portrait_hintergruende(f)
print("Jana: Karte -> %s\\%s\\%s.json | Portrait mit Kostuem %s, Posen %s, Hintergruende %s"
      % (c.cfg()["cards_dir"], f["welt"], c.karten_name(f), k1, c.PORTRAIT_ZUFALL, bg[:4]))
if LOS:
    c.karte_schreiben(f)
    c.ps_ungespeichert_sperre()
    c.sprites_einrichten(f)
    c.abgleich_pruefen(f, [k1])
    alt = c.portrait_pfad(f)
    if alt:
        os.replace(alt, os.path.join(os.path.dirname(alt), "_alt_" + os.path.basename(alt)))
    c.ps_tags_fuer_kost(f, k1)
    d = c.ps_decks(f, k1, c.PORTRAIT_ZUFALL, bg)
    r = c.ps("/api/queue", {"cfg": {}, "decks": d, "portrait": True, "seed": random.randint(1, 2 ** 31 - 1)})
    c.ps_kostuem_anwenden(f, k1)
    f["vorschau_seit"] = time.time()
    c.fig_speichern(f)
    print("Karte gespeichert: %s | Portrait eingestellt: %s" % (f["karte_datei"], r.get("queued")))
print("geschrieben" if LOS else "PROBELAUF")
