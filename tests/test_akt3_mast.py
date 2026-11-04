# -*- coding: utf-8 -*-
r"""Akt 3: Quest "The Red Light" (ereignisse_akt3_mast.py, kaempfe_akt3.py): Charly oder Rosi nach Kanon, Gegner mit Stahl,
Raetsel mit Hinweisen vom Rastplatz, Wahl mit Preis auf beiden Seiten, Folgen in Kommission, Zeugen, Festa und Ende 2b.

  python tests/test_akt3_mast.py
"""
import json, os, sys

EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, EDEN)
sys.path.insert(0, os.path.join(EDEN, "werkzeuge", "eden_rise"))
from kern import abschluss, akt3, auftraege, regeln  # noqa: E402
MD = os.path.join(EDEN, "module", "eden_rise")
EV = {e["id"]: e for e in json.load(open(os.path.join(MD, "ereignisse.json"), encoding="utf-8"))["events"]}
ORTE = json.load(open(os.path.join(MD, "auftraege.json"), encoding="utf-8"))["orte"]
KAEMPFE = json.load(open(os.path.join(MD, "kaempfe.json"), encoding="utf-8"))
KOM = json.load(open(os.path.join(MD, "kommission.json"), encoding="utf-8"))
MODUL = json.load(open(os.path.join(MD, "modul.json"), encoding="utf-8"))


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def folgen(e):
    return [f for o in e["optionen"] for f in o["folgen"]]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    import ereignisse_akt3_mast as M
    o = ORTE["a3_mast"]
    z = lambda *f: {"flags": ["akt2_ende"] + list(f), "werte": {}, "tag": 25}
    pruefen(regeln.gilt(o["wenn"], z("rt_charly_bleibt")) and regeln.gilt(o["wenn"], z()), "Karte mit Charly, sonst mit Rosi")
    pruefen(not regeln.gilt(o["wenn"], z("gefeuert_rosi")) and not regeln.gilt(o["wenn"], dict(z(), tag=29)), "ohne beide keine Quest; nur Tag 24 bis 28")
    pruefen(auftraege.AKT3_VORRANG.index("a3_mast") == 1, "Rang 2 nach der Baustelle (Grenze von drei Karten)")
    weg = [f["weiter"] for f in folgen(EV["a3_mast_macchia"]) if "weiter" in f][0]
    pruefen(weg[0]["id"] == "a3_mast_c_rast" and weg[1]["id"] == "a3_mast_r_rast", "Charlys oder Rosis Fassung")

    # Gegner: Agenten, Drohnen, Kobras, am Ende der Waechter; Maschinen geben Stahl
    enc = KAEMPFE["encounters"]
    for bid in ("a3_mast_strasse", "a3_mast_kobra", "a3_mast_alarm", "a3_mast_waechter"):
        pruefen(bid in enc, "Kampf %s" % bid)
    gegner = {g for b in ("a3_mast_strasse", "a3_mast_kobra", "a3_mast_alarm", "a3_mast_waechter") for g in enc[b]["enemies"]}
    pruefen({"agent", "hirtendrohne", "a3_kobra", "a3_waechter", "a3_skorpion"} <= gegner, "Agenten, Drohnen, Kobra-Roboter, Skorpion, Waechter")
    pruefen(all(KAEMPFE["enemies"][g]["cls"] == "maschine" for g in ("a3_kobra", "a3_skorpion", "a3_waechter")), "Roboter sind Maschinen: Stahl")
    pruefen(KAEMPFE["enemies"]["a3_waechter"]["boss"] and not enc["a3_mast_waechter"]["flee_allowed"], "der Waechter ist der Endkampf")
    pruefen(KAEMPFE["enemies"]["a3_kobra"]["sprite"] == "RobotCobra", "Sprites aus der Belagerung")
    from kern import aufbau
    pruefen(all("steel" in s[-1] for s in aufbau.STUFEN.values()), "jedes Haus braucht Stahl in der letzten Stufe")

    # Raetsel: Hinweise am Rastplatz, falsche Antwort = Alarm-Kampf und dieselbe Frage nochmal
    rast = json.dumps(EV["a3_mast_c_rast"])
    pruefen("R-7" in rast and "under her desk" in rast.lower(), "Charlys Hinweise kommen am Rastplatz")
    for n in (1, 2):
        e = EV["a3_mast_c_frage_%d" % n]
        falsch = [o for o in e["optionen"] if any(f.get("kampf") == "a3_mast_alarm" for f in o["folgen"])]
        pruefen(len(falsch) == 2 and all({"weiter": "a3_mast_c_frage_%d" % n} in o["folgen"] for o in falsch), "Frage %d: falsch = Alarm, nochmal" % n)
    f3 = json.dumps(EV["a3_mast_c_frage_3"])
    pruefen("a3_mast_mutter_antwort" in f3 and "a3_mast_eigene_antwort" in f3, "letzte Frage: ihre Antwort oder die der Mutter")
    pruefen("Lot 14" in json.dumps(EV["a3_mast_r_kasten"]) and "Old Lady" in json.dumps(EV["a3_mast_r_old_lady"]), "Rosis Fassung: Papas Strasse, Old Lady")
    pruefen("You're cold" in json.dumps(EV["a3_mast_c_anruf"]), "der Anruf der Mutter")

    # Wahl und Folgen
    w = json.dumps(EV["a3_mast_wahl"])
    pruefen("a3_mast_aus" in w and "a3_mast_an" in w, "Wahl: abschalten oder weiterlaufen lassen")
    from ereignisse_akt3_lose import TUER
    batu = TUER["batu"]
    pruefen(regeln.gilt(batu, z("tk_haus_weg_batu", "a3_mast_aus")) and not regeln.gilt(batu, z("a3_mast_an")), "Ba Tu: Mast aus = Mut, Mast an = nur mit Haus")
    pruefen(any(c["id"] == "mast" and c["wenn"] == {"flag": "a3_mast_an"} for c in KOM["karten"]), "Kommissions-Karte nur, wenn der Mast weiterlaeuft")
    pruefen("a3_mast_an" in akt3.BEWEISE, "der Mitschnitt zaehlt als Beweis")
    bild = json.dumps(EV["a3_festa_bild"])
    pruefen("a3_mast_aus" in bild and "a3_mast_an" in bild, "Festa: Ghjuvan schlaeft, oder Charly winkt dem Licht")
    pruefen("a3_mast_fertig" in json.dumps(EV["a3_charly_geld"]), "Borrowed: Folge vom Kamm")
    zz = {"flags": ["akt2_ende", "a3_festa_fertig", "a3_mast_aus"], "werte": {}}
    akt3_ende = akt3.ende
    akt3.ende = lambda z: "2b"
    try:
        karte = abschluss.akt3_ende(zz, dict(MODUL, akt3_spielbar=True))
    finally:
        akt3.ende = akt3_ende
    pruefen("stays dark" in karte["absaetze"][0]["text"], "Ende 2b: mit abgeschaltetem Mast bleibt der Kamm dunkel")
    print("Alle Pruefungen gruen.")


if __name__ == "__main__":
    main()
