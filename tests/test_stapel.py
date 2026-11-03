# -*- coding: utf-8 -*-
"""Stapeln (Duc 28.10.2026): Stapelgroessen nach Stufe, Plaetze je Stapel, Kaufen in offene Stapel, Truhe, Ernte unterwegs in
der Tasche (Rohstoffe 10, Fische 3 je Art), Beute nach Anzahl (Doppelfund), Niederlage behaelt einen Platz, Heimkehr packt aus.

Laeuft ohne Modell, Stimme und Netz.

  python tests\\test_stapel.py
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(HERE)
sys.path.insert(0, EDEN)
from kern import abbau, angeln, expedition, handel, kabine, kuechen, zustand  # noqa: E402

MODUL = json.load(open(os.path.join(EDEN, "module", "eden_rise", "modul.json"), encoding="utf-8"))
D = kuechen.daten(MODUL)
GESCHENK = next(i for i, it in MODUL["items"].items() if it.get("art") == "geschenk")
P = zustand.inventar_plaetze({}, MODUL)          # Start-Tasche (8 seit 29.10.2026)
MEHR = ["smaragd", "rubin", "saphir", "opal"][:P - 6]   # fuellt die Plaetze ueber den alten 6 auf


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def fehler(fn, *a):
    try:
        fn(*a)
    except ValueError as e:
        return str(e)
    return None


def neues_spiel(sid="s1"):
    z = zustand.neu(MODUL, "entspannt")
    zustand.persona_setzen(z, MODUL, MODUL["personas"][0])
    z["tag"], z["phase"], z["status"], z["id"] = 9, "tag", "wahl", sid
    z["inventar"] = []
    return z


def groessen_pruefen():
    g = {i: zustand.stapel(MODUL, i) for i in ("plaster", "cooling_spray", "fairy_bread", "bandage", "grenade_fire", "steel_plate",
                                                "jade", "antidote", "grenade_shrapnel", "saphir", "megaphone", GESCHENK)}
    pruefen(g["plaster"] == g["cooling_spray"] == g["fairy_bread"] == 5, "gewöhnlich stapelt 5 (Pflaster, Kühlspray, Snacks)")
    pruefen(g["bandage"] == g["grenade_fire"] == g["steel_plate"] == g["jade"] == 3, "gut stapelt 3 (Bandage, Granate, Platte, Stufe-1-Stein)")
    pruefen(g["antidote"] == g["grenade_shrapnel"] == g["saphir"] == 1, "selten stapelt nicht (Gegengift, Splittergranate, Saphir)")
    pruefen(g[GESCHENK] == 1 and g["megaphone"] == 1, "Geschenke und Einzelstücke bleiben einzeln")
    pruefen(not any(it.get("stapel") for it in MODUL["items"].values() if it.get("art") in
                    ("geschenk", "einzigartig", "gluecksbringer", "attribut", "schmuggel", "andenken", "quest", "schluessel")),
            "nichts mit Geschichte hat ein Stapel-Feld")
    pruefen(D["abbau"]["stapel"] == {"rohstoff": 10, "fisch": 3}, "Ernte: Rohstoffe 10, Fische 3 je Art")


def plaetze_pruefen():
    z = neues_spiel()
    z["inventar"] = ["plaster"] * 7 + ["bandage"] + [GESCHENK]
    pruefen(zustand.belegt(z, MODUL) == 4, "7 Pflaster = 2 Plätze, dazu Bandage und Geschenk = 4")
    pruefen(zustand.stapel_liste(MODUL, z["inventar"])[:2] == [("plaster", 5), ("plaster", 2)], "Stapel-Liste: 5 + 2")
    z["inventar"] += ["bandage", "bandage", "jade", "kupfer"] + MEHR
    pruefen(zustand.belegt(z, MODUL) == P, "volle Tasche (%d Plätze)" % P)
    pruefen(zustand.platz_fuer(z, MODUL, "plaster", 3) and not zustand.platz_fuer(z, MODUL, "plaster", 4),
            "offener Pflaster-Stapel nimmt noch 3, das vierte bräuchte einen Platz")
    pruefen(not zustand.platz_fuer(z, MODUL, "bandage"), "Bandagen-Stapel ist voll (3/3)")
    pruefen(zustand.platz_fuer(z, MODUL, next(i for i, it in MODUL["items"].items() if it.get("art") == "andenken")),
            "Andenken brauchen keinen Platz")
    h = handel.ansicht(z, MODUL, {}, [])
    kacheln = [(w["id"], w["n"]) for w in h["inventar_info"]]
    pruefen(kacheln[:2] == [("plaster", 5), ("plaster", 2)] and ("bandage", 3) in kacheln and h["belegt"] == P,
            "Inventar-Ansicht: eine Kachel je Stapel mit Anzahl")


def kaufen_pruefen():
    alt = handel.sortiment
    handel.sortiment = lambda z, modul, laden: [{"id": "plaster", "preis": 10}, {"id": GESCHENK, "preis": 10}]
    try:
        z = neues_spiel()
        z["konto"] = 500
        handel.kaufen(z, MODUL, "toto", "plaster")
        handel.kaufen(z, MODUL, "toto", "plaster")
        pruefen(z["inventar"].count("plaster") == 2 and zustand.belegt(z, MODUL) == 1, "zweites Pflaster landet im selben Platz")
        handel.kaufen(z, MODUL, "toto", GESCHENK)
        pruefen(fehler(handel.kaufen, z, MODUL, "toto", GESCHENK) is not None, "ein Geschenk gibt es weiter nur einmal")
        z["inventar"] += ["jade", "kupfer", "steel_plate", "topas"] + MEHR
        pruefen(zustand.belegt(z, MODUL) == P, "Tasche voll")
        handel.kaufen(z, MODUL, "toto", "plaster")
        pruefen(z["inventar"].count("plaster") == 3, "volle Tasche, aber offener Stapel: Kauf geht")
        z["inventar"] += ["plaster", "plaster"]
        pruefen(fehler(handel.kaufen, z, MODUL, "toto", "plaster") is not None, "Stapel voll und kein Platz: Kauf geht nicht")
    finally:
        handel.sortiment = alt


def truhe_pruefen():
    z = neues_spiel()
    z["status"], z["kabine"] = "kabine", {"ort": "kabine"}
    z["inventar"] = ["plaster"] * 4
    z["truhe"] = []
    kabine.truhe(z, MODUL, "plaster", "rein", 4)
    pruefen(z["truhe"] == ["plaster"] * 4 and not z["inventar"], "ein Klick legt den ganzen Stapel in die Truhe")
    z["inventar"] = ["jade", "kupfer", "steel_plate", "topas", "aquamarin", "plaster"] + MEHR
    z["truhe"].append("plaster")
    kabine.truhe(z, MODUL, "plaster", "raus", 5)
    pruefen(z["inventar"].count("plaster") == 5 and z["truhe"] == ["plaster"],
            "heraus nur, soweit der offene Stapel reicht (4 + 1 = 5, eins bleibt in der Truhe)")


def expedition_spiel():
    z = neues_spiel("s2")
    z["inventar"] = ["plaster"] + MEHR
    zustand.folgen_anwenden(z, MODUL, [{"expedition": "kloster"}])
    z["status"] = "ereignis"
    return z


def ernte_pruefen():
    z = expedition_spiel()
    pruefen(expedition.ernte_roh(z, MODUL, "timber", 12) == 12 and "rohstoffe" not in z.get("kueche", {}),
            "unterwegs geht Holz in die Tasche, nicht in den Zähler")
    pruefen(zustand.belegt(z, MODUL) == 3 + len(MEHR), "12 Timber = 2 Plätze, dazu das Pflaster")
    for s in (3, 2, 2, 3):
        expedition.ernte_fisch(z, MODUL, "pike", s)
    pruefen(zustand.belegt(z, MODUL) == 5 + len(MEHR), "4 Hechte = 2 Plätze (3 je Art)")
    pruefen(expedition.ernte_frei(z, MODUL, "roh", "timber") == 8 + 10, "noch 8 in den offenen Holzstapel, 10 auf den letzten Platz")
    pruefen(expedition.ernte_roh(z, MODUL, "slate", 25) == 10 and zustand.belegt(z, MODUL) == P, "Schiefer: nur ein Platz frei, 10 passen")
    pruefen(expedition.ernte_roh(z, MODUL, "timber", 9) == 8, "der offene Holzstapel nimmt noch 8, der Rest bleibt liegen")
    pruefen(expedition.ernte_fisch(z, MODUL, "pike", 3) and expedition.ernte_fisch(z, MODUL, "pike", 3)
            and not expedition.ernte_fisch(z, MODUL, "pike", 3), "der zweite Hecht-Stapel nimmt noch zwei, dann ist Schluss")
    pruefen(not expedition.ernte_fisch(z, MODUL, "barbel", 2), "neue Fischart ohne freien Platz: schwimmt davon")
    kacheln = [(w["id"], w["n"]) for w in handel.ansicht(z, MODUL, {}, [])["inventar_info"]]
    pruefen(("roh:timber", 10) in kacheln and kacheln.count(("fisch:pike", 3)) == 2, "Tasche zeigt Holz- und Fischstapel")
    zeilen = zustand.folgen_anwenden(z, MODUL, [{"expedition": "ende"}])
    pruefen(kuechen.rohstoffe(z) == {"timber": 20, "slate": 10} and kuechen.vorrat_menge(z, "pike_roh") == 6,
            "Heimkehr packt aus: 20 Timber, 10 Slate, 6 Hechte in die Küche")
    pruefen(any("Unpacked" in str(x) for x in zeilen) and zustand.belegt(z, MODUL) == 1 + len(MEHR), "Meldung und freie Plätze danach")


def niederlage_pruefen():
    z = expedition_spiel()
    z["inventar"] += ["plaster", "plaster", "bandage"]
    expedition.ernte_roh(z, MODUL, "timber", 12)
    expedition.ernte_fisch(z, MODUL, "pike", 2)
    expedition.ernte_fisch(z, MODUL, "pike", 3)
    b = {x["id"]: x for x in expedition.beute(z, MODUL, {})}
    pruefen(b["item:plaster"]["n"] == 2, "Doppelfund zählt als Beute (ein Pflaster war schon dabei)")
    pruefen(b["roh:timber"]["halten"] == 10 and b["fisch:pike"]["label"] == "Northern Pike ×2", "Ernte ist Beute, ein Platz = 10 Holz")
    expedition.behalten(z, MODUL, {}, "roh:timber")
    zeilen = expedition.scheitern(z, MODUL, {})
    pruefen(sorted(z["inventar"]) == sorted(["plaster"] + MEHR) and kuechen.rohstoffe(z) == {"timber": 10} and not kuechen.vorrat_menge(z, "pike_roh"),
            "Niederlage: das mitgebrachte Pflaster bleibt, 10 Timber kommen heim, alles andere ist weg")
    pruefen("You still have: Timber ×10." in zeilen and any("Timber ×2" in x and MODUL["items"]["plaster"]["label"] + " ×2" in x for x in zeilen),
            "Meldung: was bleibt, was verloren ist")
    z = expedition_spiel()
    for s in (2, 3, 3, 2):
        expedition.ernte_fisch(z, MODUL, "pike", s)
    expedition.behalten(z, MODUL, {}, "fisch:pike")
    expedition.scheitern(z, MODUL, {})
    pruefen(kuechen.vorrat_menge(z, "pike_roh", 3) == 2 and kuechen.vorrat_menge(z, "pike_roh") == 3,
            "ein Fischstapel: die drei besten Hechte bleiben")


def abbau_pruefen():
    z = expedition_spiel()
    kuechen.kueche(z)["werkzeug"] = {"axe": 3}
    z["inventar"] += ["jade", "kupfer", "steel_plate", "topas"]
    expedition.ernte_roh(z, MODUL, "timber", 9)
    pruefen(zustand.belegt(z, MODUL) == P, "Tasche voll, Holzstapel 9/10")
    abbau.starten(z, MODUL, "kl_bachufer", "holz")
    z["abbau"]["knoten"] = ["holm_oak", "cork_oak", "holm_oak", "holm_oak"]
    r = abbau.schlag(z, MODUL, "perfekt")
    pruefen(r["eintrag"]["ertrag"] == [{"id": "timber", "label": "Timber", "n": 1}] and r["voll"]
            and {x["label"]: x["n"] for x in r["eintrag"]["liegen"]} == {"Timber": 3},
            "Steineiche: 1 Timber passt noch, 3 bleiben liegen, Tasche voll")
    zeilen = abbau.ende(z, MODUL)
    pruefen(any("Left behind" in x for x in zeilen) and z["status"] == "ereignis", "Ende: Meldung 'Left behind', zurück ans Feuer")
    c = {x["art"]: x for x in abbau.quellen_ansicht(z, MODUL, "kl_bachufer")}
    pruefen(c["holz"]["voll"] and c["wasser"]["voll"] and c["holz"]["rest"] == 3, "Chips zeigen 'bag full'")
    pruefen("full" in (fehler(abbau.starten, z, MODUL, "kl_bachufer", "holz") or "")
            and "full" in (fehler(angeln.starten, z, MODUL, "kl_bachufer", "kl_bachufer") or ""),
            "volle Tasche: weder Abbauen noch Angeln startet")
    z2 = neues_spiel("s3")
    z2["status"] = "ereignis"
    kuechen.kueche(z2)["werkzeug"] = {"axe": 3}
    abbau.starten(z2, MODUL, "kl_bachufer", "holz")
    abbau.schlag(z2, MODUL, "perfekt")
    pruefen(kuechen.rohstoffe(z2).get("timber", 0) >= 2 and zustand.belegt(z2, MODUL) == 0,
            "ohne laufende Expedition geht der Ertrag wie bisher direkt in den Zähler")


def angeln_pruefen():
    z = expedition_spiel()
    angeln.starten(z, MODUL, "kl_bachufer", "kl_bachufer")
    f = angeln.auswerfen(z, MODUL)
    while f["art"] != "fisch":                  # Fundsachen ueberspringen
        angeln.ergebnis(z, MODUL, False, grund="abbruch")
        f = angeln.auswerfen(z, MODUL)
    e = angeln.ergebnis(z, MODUL, True, 0)
    pruefen(e["tasche"] and not e.get("frei") and not kuechen.vorrat_menge(z, f["id"] + "_roh")
            and any(w["id"] == "fisch:" + f["id"] for w in expedition.ernte_ansicht(z, MODUL)),
            "Fang am Rastplatz liegt in der Tasche, nicht in der Küche")
    angeln.ende(z, MODUL)
    z2 = neues_spiel("s4")
    angeln.starten(z2, MODUL, "boot")
    f = angeln.auswerfen(z2, MODUL)
    while f["art"] != "fisch":
        angeln.ergebnis(z2, MODUL, False, grund="abbruch")
        f = angeln.auswerfen(z2, MODUL)
    e = angeln.ergebnis(z2, MODUL, True, 0)
    pruefen(not e["tasche"] and kuechen.vorrat_menge(z2, f["id"] + "_roh") == 1, "am Boot direkt in den Vorrat")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    groessen_pruefen()
    plaetze_pruefen()
    kaufen_pruefen()
    truhe_pruefen()
    ernte_pruefen()
    niederlage_pruefen()
    abbau_pruefen()
    angeln_pruefen()
    print("ALLES OK")
