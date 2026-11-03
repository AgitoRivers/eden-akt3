# -*- coding: utf-8 -*-
"""Jacken-Charms (28.10.2026): Daten und Bilder, Uebergabe bei Vertrauen 5 (Vorrang, nur einmal), Fredericos Loewe
ueber die volle Farm, Platz je Jacke, Attribut-Boni ueberall (auch ueber 5), Kampfwerte und die drei neuen Werte.

  python tests\\test_charms.py
"""
import copy, json, os, sys

EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, EDEN)
from kern import charms, ereignisse, farm, kampf, kuechen, zustand  # noqa: E402

MOD = os.path.join(EDEN, "module", "eden_rise")
MODUL = json.load(open(os.path.join(MOD, "modul.json"), encoding="utf-8"))
DEFS = copy.deepcopy(kampf.daten(MOD))


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def spiel(tag=3, phase="abend"):
    z = zustand.neu(MODUL, "entspannt")
    zustand.persona_setzen(z, MODUL, MODUL["personas"][0])
    z["tag"], z["phase"], z["status"] = tag, phase, "szene"
    for k in [k for k in z["werte"] if k.startswith("begehren.")]:
        z["werte"][k] = 0                            # keine Selfies dazwischen
    return z


def ziehen(z, d):
    e = ereignisse.stand(z)
    e["heute"] = {}
    return ereignisse._handy_ziehen(z, MODUL, d, e)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    c = charms.daten("eden_rise")
    pruefen(len(c) == 21, "21 Charms (%d)" % len(c))
    fehlt = [x["bild"] for x in c.values() if not os.path.isfile(os.path.join(MOD, "items", x["bild"] + ".webp"))]
    pruefen(not fehlt, "alle Bilder da %s" % (fehlt or ""))
    d = ereignisse.daten(MOD)
    ue = [e for e in d["events"] if e["personen"].get("charm")]
    pruefen(len(ue) == 40 and {e["personen"]["charm"] for e in ue} == set(c) - {"mazzera"}, "20 Uebergaben in 2 Fenstern")

    # Vertrauen 4: nichts; Vertrauen 5: Lolas Uebergabe kommt vor allem anderen, mit Foto
    z = spiel()
    z["werte"]["vertrauen.lola"] = 4
    x = ziehen(z, d)
    pruefen(not x or not x["personen"].get("charm"), "Vertrauen 4: keine Uebergabe")
    z = spiel()
    z["werte"]["vertrauen.lola"] = 5
    x = ziehen(z, d)
    pruefen(x and x["personen"].get("charm") == "lola", "Vertrauen 5: Lolas Kaenguru kommt (%s)" % (x and x["id"]))
    pruefen(z["event"].get("foto") == "/itembild/charm_lola", "Foto des Charms im Chat")
    zeilen, _ = ereignisse.anwenden(z, MODUL, x, x["optionen"][0]["folgen"])
    pruefen("lola" in charms.stand(z)["besitz"] and "charm_lola" in z["flags"], "Charm im Besitz, Flag gesetzt")
    jacke = kampf.equipment(z)["armor"]
    pruefen(charms.stand(z)["an"].get(jacke) == "lola", "haengt an der getragenen Jacke")
    z["event"] = None
    pruefen(not any(e["personen"].get("charm") == "lola" for e in
                    [ziehen(z, d) for _ in range(3)] if e), "kommt nur einmal")
    pruefen(charms.geben(z, "lola") == [], "zweites Geben ohne Wirkung")

    # Attribut ueberall, auch ueber 5
    z["persona"]["attribute"]["strength"] = 5
    pruefen(kampf.attributes(z, DEFS)["strength"] == 6, "Kampf: Strength 5 + Charm = 6")
    pruefen(charms.boni(z, "strength") == [("Lola's Kangaroo", 1)], "Wuerfelanzeige nennt den Charm")
    z["flags"].append("jacke_jacket_water")              # zweite Jacke im Besitz
    kampf.ausruesten(z, DEFS, "armor", "jacket_water")
    pruefen(kampf.attributes(z, DEFS)["strength"] == 5, "andere Jacke: kein Bonus")
    kampf.chip_einsetzen(z, DEFS, "armor", "jacket_water", "charm:lola")
    pruefen(charms.stand(z)["an"] == {"jacket_water": "lola"}, "umgehaengt: nur an einer Jacke")
    kampf.chip_entfernen(z, "armor", "jacket_water", "charm:lola")
    pruefen(not charms.stand(z)["an"], "abgenommen")

    # Kampfwerte: Holm Schutz, Maxwell Spezial +20 %, Casanova Serie 2, Elsa Vorteil, Mazzera Ausdauer
    for cid, st, v in (("holm", "schutz", 1), ("maxwell", "spezial_schaden", 20), ("casanova", "parade_serie", 1),
                       ("mazzera", "ausdauer_max", 1), ("petru", "parade", 10), ("isabelle", "heil_kampf", 3)):
        charms.geben(z, cid)
        kampf.chip_einsetzen(z, DEFS, "armor", "jacket_water", "charm:" + cid)
        agg = kampf.chips_aktiv(z, DEFS, kampf.aktive_waffe(z, DEFS), "jacket_water")
        pruefen(agg[st] == v, "%s: %s %s" % (cid, st, v))
    charms.geben(z, "elsa")
    kampf.chip_einsetzen(z, DEFS, "armor", "jacket_water", "charm:elsa")
    pruefen("einschuechtern" in kampf.chips_aktiv(z, DEFS, kampf.aktive_waffe(z, DEFS), "jacket_water")["vorteil"],
            "Elsa: Vorteil auf Intimidate")
    kampf.chip_einsetzen(z, DEFS, "armor", "jacket_water", "charm:mazzera")
    kampf.starten(z, DEFS, "akt1_ratte")
    sp = z["kampf"]["spieler"]
    pruefen(sp["ausdauer_max"] == kampf.max_stamina(kampf.progress(z)["level"]) + 1, "Mazzera: Ausdauer +1 im Kampf")
    z.pop("kampf")
    kampf.chip_einsetzen(z, DEFS, "armor", "jacket_water", "charm:elsa")
    kampf.starten(z, DEFS, "akt1_pirat")
    pruefen(kampf.skill_info(z, z["kampf"], "einschuechtern")["vorteil"], "Elsa: Intimidate im Kampf mit Vorteil")
    z.pop("kampf")

    # Frederico: erst mit allen Staellen auf voller Stufe
    z = spiel(tag=10)
    pruefen(not any((ziehen(z, d) or {}).get("personen", {}).get("charm") == "frederico" for _ in range(2)),
            "ohne volle Farm kein Loewe")
    k = kuechen.kueche(z)
    dd = kuechen.daten(MODUL)
    for art in dd["tiere"]:
        k["staelle"][art] = {"tiere": [], "naechste_id": 1, "letzte_geburt": 1, "stufe": len(dd["stall_stufen"][art])}
    k["staelle"]["cow"]["stufe"] -= 1
    z["konto"] = 99999
    k["rohstoffe"] = dict(dd["stall_stufen"]["cow"][-1]["rohstoffe"])
    kuechen.nonna_offen = lambda z_, m_: True          # Oeffnung (Tag/Flag) ist nicht Gegenstand dieses Tests
    farm.stall_ausbauen(z, MODUL, "cow")
    pruefen("farm_voll" in z["flags"], "letzter Stall voll ausgebaut setzt farm_voll")
    z["event"] = None
    x = ziehen(z, d)
    pruefen(x and x["personen"].get("charm") == "frederico", "Fredericos Loewe kommt (%s)" % (x and x["id"]))
    print("alle Charm-Tests gruen")


if __name__ == "__main__":
    main()
