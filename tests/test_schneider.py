# -*- coding: utf-8 -*-
r"""Danzels Auftraege (Duc 30.10.2026, Wiki systeme/schneider.md): Material bringen, Uebergabe am naechsten Tag, jeder dritte
Auftrag gibt ein Schnittmuster, das Massstueck schaltet Chiaras Outfit frei.

  python tests\test_schneider.py
"""
import json, os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HIER))
from kern import buehne, handel, kuechen, regeln, schneider, zustand  # noqa: E402

MOD = os.path.join(os.path.dirname(HIER), "module", "eden_rise")
MODUL = json.load(open(os.path.join(MOD, "modul.json"), encoding="utf-8"))
MODUL["_kuechen_pfad"] = MOD
EV = {e["id"]: e for e in json.load(open(os.path.join(MOD, "ereignisse.json"), encoding="utf-8"))["events"]}


def fehler_text(fn, *a):
    try:
        fn(*a)
    except ValueError as e:
        return str(e)
    return None


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def spiel(tag=16, trio=True):
    z = zustand.neu(MODUL, "entspannt")
    zustand.persona_setzen(z, MODUL, MODUL["personas"][0])
    z["tag"], z["heute"], z["konto"] = tag, [{"ort": "alvas_bar"}], 500
    z["bekannt"] = list(MODUL["personen"])
    if trio:
        z["flags"] += ["rt_ausgang_alle", "rt_ende_tag"]
        z.setdefault("flag_tag", {})["rt_ende_tag"] = 12
    handel.init(z, MODUL)
    return z


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    d = MODUL["schneider"]
    pruefen(len(d["auftraege"]) == 8 and all("sn_" + a["id"] in EV for a in d["auftraege"]), "acht Auftraege, jeder mit Uebergabe-Event")
    roh = kuechen.daten(MODUL)["rohstoffe"]
    pruefen(all(k in roh for a in d["auftraege"] + d["massstuecke"] for k in a["material"]), "alles Material gibt es als Rohstoff")
    pruefen(all("sn_%s_fertig" % a["id"] in json.dumps(EV["sn_" + a["id"]]["optionen"]) for a in d["auftraege"] + [m for m in d["massstuecke"] if not m.get("quest")]),
            "jede Wahl beendet den Auftrag")

    pruefen(schneider.ansicht(spiel(trio=False), MODUL) is None, "ohne Laden keine Auftraege")
    z = spiel()
    v = schneider.ansicht(z, MODUL)
    pruefen(len(v["auftraege"]) == 2 and not v["auftraege"][0]["geht"], "zwei Bestellungen haengen aus, ohne Material geht nichts")
    try:
        schneider.bringen(z, MODUL, "apron")
        raise AssertionError("ohne Material darf es nicht gehen")
    except ValueError:
        print("OK ohne Material keine Abgabe")

    kuechen.rohstoff_add(z, "cloth", 2)
    schneider.bringen(z, MODUL, "apron")
    pruefen(kuechen.rohstoffe(z).get("cloth", 0) == 0 and "sn_apron" in z["flags"], "Material ist weg, Auftrag laeuft")
    bed = EV["sn_apron"]["wann"]["bedingung"]
    pruefen(not regeln.gilt(bed, z), "heute noch keine Uebergabe")
    z["tag"] += 1
    pruefen(regeln.gilt(bed, z), "am naechsten Tag die Uebergabe")
    pruefen(EV["sn_apron"]["wann"]["pflicht"], "die Uebergabe kommt von selbst")

    # Massstueck
    z = spiel()
    z["werte"]["vertrauen.chiara"] = 2
    pruefen(not schneider.ansicht(z, MODUL)["massstuecke"], "unter Vertrauen 3 kein Massstueck")
    z["werte"]["vertrauen.chiara"] = 3
    kuechen.rohstoff_add(z, "wool", 3)
    pruefen(not schneider.ansicht(z, MODUL)["massstuecke"][0]["geht"], "ohne Schnittmuster geht es nicht")
    z["flags"] += ["sn_%s_fertig" % a["id"] for a in d["auftraege"][:3]]
    pruefen(schneider.muster(z, MODUL) == 1, "drei fertige Auftraege geben ein Schnittmuster")
    konto = z["konto"]
    pruefen(not schneider.ansicht(z, MODUL)["massstuecke"][0]["geht"], "ohne Aquamarin geht es nicht")
    pruefen(fehler_text(schneider.bringen, z, MODUL, "dress_whites"), "ohne Aquamarin nimmt Danzel nichts an")
    z["inventar"].append("aquamarin")
    schneider.bringen(z, MODUL, "dress_whites")
    pruefen("aquamarin" not in z["inventar"], "der Stein ist weg")
    pruefen(z["konto"] == konto - 110 and schneider.muster(z, MODUL) == 0, "Massstueck kostet Geld und das Schnittmuster")

    # Outfit: neue Standardkleidung, sobald das Set existiert; ohne Set bleibt alles beim Alten
    alt = {"Uniform": 1, "Dress Whites": 1, "Swim": 1}
    _sets = buehne.sets
    buehne.sets = lambda c, m, p: alt
    z["flags"].append("sn_dress_whites_fertig")
    pruefen(buehne.set_waehlen({}, MODUL, "chiara", {"ort": "main_salon"}, "tag", None, z) == "Dress Whites", "danach traegt sie die Jacke")
    pruefen(buehne.set_waehlen({}, MODUL, "chiara", {"ort": "swim_platform"}, "tag", None, z) == "Swim", "am Pool bleibt der Badeanzug")
    buehne.sets = lambda c, m, p: {"Uniform": 1}
    pruefen(buehne.set_waehlen({}, MODUL, "chiara", {"ort": "main_salon"}, "tag", None, z) == "Uniform", "ohne gerendertes Set bleibt die Uniform")
    buehne.sets = _sets

    # Stoff
    z = spiel()
    pruefen("cloth_bolt" in {w["id"] for w in handel.sortiment(z, MODUL, "toto")}, "Totò verkauft Stoff, sobald der Laden offen ist")
    pruefen("import_wool" in {w["id"] for w in handel.sortiment(z, MODUL, "toto")}, "ohne Ghjuvan gibt es teure Importwolle")
    z["flags"].append("bg_ghjuvan_getroffen")
    pruefen("corsican_wool" in {w["id"] for w in handel.sortiment(z, MODUL, "danzel")}, "Ghjuvans Wolle gibt es bei Danzel")
    pruefen("import_wool" not in {w["id"] for w in handel.sortiment(z, MODUL, "toto")}, "dann keine Importwolle")
    handel.kaufen(z, MODUL, "toto", "cloth_bolt")
    pruefen(kuechen.rohstoffe(z).get("cloth") == 1, "gekaufter Stoff landet bei den Rohstoffen")
    z = spiel(tag=2, trio=False)
    pruefen("cloth_bolt" not in {w["id"] for w in handel.sortiment(z, MODUL, "toto")}, "vorher keine Stoffballen bei Totò")
    print("Alles gut.")


if __name__ == "__main__":
    main()
