# -*- coding: utf-8 -*-
r"""Akt 3 beginnt an Tag 24 (E-114, fix-akt2): Die Belagerung laeuft Tag 21-23. Vorher stand Akt 3 im Code an Tag 22, und die
Belagerungs-Sperre (ab Tag 21 Nachmittag nur bl_-Events) hatte kein Ende: Alle Akt-3-Fenster waren tot.

  python tests/test_akt3_beginn.py
"""
import json, os, re, sys

HIER = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(HIER)
sys.path.insert(0, EDEN)
from kern import ereignisse  # noqa: E402

MOD = os.path.join(EDEN, "module", "eden_rise")
WZ = os.path.join(EDEN, "werkzeuge", "eden_rise")
MODUL = json.load(open(os.path.join(MOD, "modul.json"), encoding="utf-8"))
KUECHE = json.load(open(os.path.join(MOD, "kuechen.json"), encoding="utf-8"))
EV = {e["id"]: e for e in json.load(open(os.path.join(MOD, "ereignisse.json"), encoding="utf-8"))["events"]}
AKT3_AB = 24


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    quelle = open(os.path.join(WZ, "ereignisse_basis.py"), encoding="utf-8").read()
    pruefen(re.search(r"^AKT3_AB = 24\b", quelle, re.M), "ereignisse_basis.AKT3_AB = 24")
    for datei in ("ereignisse_outfit_quest.py", "ereignisse_schneider.py", "ereignisse_romanzen.py", "ereignisse_dorf.py", "kochen_daten.py", "modul_eden_rise.py"):
        roh = open(os.path.join(WZ, datei), encoding="utf-8").read()
        pruefen("[22, 35]" not in roh and '"ab_tag": 22' not in roh, "%s: kein Akt-3-Beginn an Tag 22" % datei)

    # Sperre: Tag 21 Nachmittag bis Tag 23 nur bl_, ab Tag 24 wieder alles
    pruefen(MODUL["sperre"].get("bis_tag") == AKT3_AB, "modul.sperre.bis_tag = %d" % AKT3_AB)
    for tag, phase, soll in ((21, "tag", None), (21, "nachmittag", "bl_"), (22, "fruehstueck", "bl_"), (23, "nacht", "bl_"),
                             (24, "fruehstueck", None), (30, "abend", None), (35, "tag", None)):
        ist = ereignisse.gesperrt_durch_story({"tag": tag}, MODUL, phase)
        pruefen(ist == soll, "Tag %d %s: Sperre %s" % (tag, phase, soll))

    # Zweite Fenster (wann.akt2) fuer Akt 3 beginnen an Tag 24
    spaet = {i: e["wann"]["akt2"] for i, e in EV.items() if e["wann"].get("akt2") and e["wann"]["akt2"][0] > 8}
    pruefen(spaet and all(w == [AKT3_AB, 35] for w in spaet.values()), "%d Akt-3-Fenster, alle [24, 35]" % len(spaet))
    pruefen(not any(e["wann"]["tage"][0] == 22 for i, e in EV.items() if not i.startswith("bl_")), "kein Nicht-bl_-Event startet an Tag 22")

    # Daten: Rosis groesste Tasche und Stahl aus Maschinen erst in Akt 3
    pruefen(MODUL["tasche"]["stufen"][-1]["ab_tag"] == AKT3_AB, "Rosi's Expedition Pack ab Tag 24 (nach der Belagerung)")
    pruefen(KUECHE["stahl_kampf"]["ab_tag"] == AKT3_AB, "Stahl aus Kaempfen ab Tag 24")

    # Ein Akt-3-Event zieht an Tag 24, waehrend der Belagerung nicht (Halsband-Kiste, Fix 2)
    z = lambda tag: {"tag": tag, "phase": "tag", "flags": ["rt_ende_tag", "mo_halsband_3"], "flag_tag": {"rt_ende_tag": 11}, "werte": {}, "inventar": []}
    pruefen(not ereignisse.passt(z(22), MODUL, EV["mo_halsbaender"], "tag", pflicht=True), "Halsband-Kiste an Tag 22 gesperrt (Belagerung)")
    pruefen(ereignisse.passt(z(24), MODUL, EV["mo_halsbaender"], "tag", pflicht=True), "Halsband-Kiste an Tag 24 frei")
    print("\nalles gruen")


if __name__ == "__main__":
    main()
