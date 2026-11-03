# -*- coding: utf-8 -*-
"""Koeder bei Petru (Duc 30.10.2026, kern/koeder.py): dauerhaft, 3 Stufen, je Stufe 2 Looks (jederzeit umschaltbar), der beste
gebaute Koeder gilt; Wirkung im Angeln (Zone, seltenere Fische, kuerzere Wartezeit); Moewenfedern als Material.

Laeuft ohne Modell, Stimme und Netz.

  python tests\\test_koeder.py
"""
import copy, json, os, sys

EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, EDEN)
from kern import angeln, kampf, koeder, kuechen, zustand  # noqa: E402

MOD = os.path.join(EDEN, "module", "eden_rise")
MODUL = json.load(open(os.path.join(MOD, "modul.json"), encoding="utf-8"))
D = kuechen.daten(MODUL)
DEFS = copy.deepcopy(kampf.daten(MOD))


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


def spiel(sid, tag=5):
    z = zustand.neu(MODUL, "entspannt")
    zustand.persona_setzen(z, MODUL, MODUL["personas"][0])
    z["tag"], z["phase"], z["status"], z["id"] = tag, "tag", "wahl", sid
    return z


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    k = D["koeder"]
    pruefen(sorted(x["stufe"] for x in k.values()) == [1, 2, 3] and all(len(x["looks"]) == 2 for x in k.values()),
            "drei Stufen, je zwei Looks")
    pruefen(all(os.path.isfile(os.path.join(MOD, "farm", "koeder", lk["id"] + ".png")) for x in k.values() for lk in x["looks"]),
            "alle 6 abgenommenen Looks liegen als Bild da")
    pruefen("feather" in D["rohstoffe"] and any(f["id"] == "gull_feather" for f in D["angeln"]["fundsachen"]["meer"]),
            "Moewenfeder ist ein Rohstoff und eine Fundsache am Meer")
    laden = json.load(open(os.path.join(MOD, "laeden.json"), encoding="utf-8"))["laeden"]["petru"]["zeilen"]
    pruefen(all("kauf_koeder_%d" % i in laden for i in (1, 2, 3)), "Petru hat je Stufe eine Uebergabe-Zeile (wird vertont)")

    # vor Tag 2 ist die Werkstatt zu, danach: Reiter, ohne Material nichts
    z = spiel("k1", tag=1)
    pruefen(koeder.ansicht(z, MODUL) is None and fehler(koeder.bauen, z, MODUL, "cork_float") is not None, "Tag 1: Werkstatt zu, kein Reiter")
    z["tag"], z["konto"] = 2, 500
    a = {x["id"]: x for x in koeder.ansicht(z, MODUL)}
    pruefen(list(a) == ["cork_float", "balsa_float", "wooden_lure"] and not any(x["gebaut"] or x["geht"] for x in a.values()),
            "Reiter zeigt alle drei, nichts gebaut, ohne Material nichts baubar")
    pruefen(fehler(koeder.bauen, z, MODUL, "cork_float") == "You're short of materials for that." and z["konto"] == 500,
            "zu wenig Material: nichts passiert, kein Geld weg")
    pruefen("kueche" not in z or "koeder" not in z["kueche"], "Lesen und Fehlversuch legen keinen Schluessel an")

    # Stufe 1 bauen: Geld + Kork + Timber, Look waehlbar
    for rid, n in {"cork": 2, "timber": 1}.items():
        kuechen.rohstoff_add(z, rid, n)
    pruefen(koeder.ansicht(z, MODUL)[0]["geht"], "mit 2 Cork und 1 Timber baubar")
    pruefen(fehler(koeder.bauen, z, MODUL, "cork_float", "koeder_2_3") is not None, "ein fremder Look wird abgelehnt")
    zeilen, gruppe = koeder.bauen(z, MODUL, "cork_float", "koeder_1_4")
    pruefen(gruppe == "kauf_koeder_1" and z["konto"] == 470 and kuechen.rohstoffe(z)["cork"] == 0 and kuechen.rohstoffe(z)["timber"] == 0
            and z["buchungen"][-1]["betrag"] == -30, "gebaut: Geld und Material weg, Petrus Zeile kauf_koeder_1")
    pruefen(koeder.besitz(z) == {"cork_float": "koeder_1_4"} and koeder.aktiv(z, MODUL)[0] == "cork_float", "Look steht fest, Koeder ist aktiv")
    pruefen(fehler(koeder.bauen, z, MODUL, "cork_float") is not None, "zweimal bauen geht nicht")

    # Look jederzeit umschalten, kostenlos
    k0 = z["konto"]
    koeder.look_waehlen(z, MODUL, "cork_float", "koeder_1_1")
    koeder.look_waehlen(z, MODUL, "cork_float", "koeder_1_4")
    koeder.look_waehlen(z, MODUL, "cork_float", "koeder_1_1")
    pruefen(koeder.besitz(z)["cork_float"] == "koeder_1_1" and z["konto"] == k0, "Look beliebig oft umschaltbar, kostet nichts")
    pruefen(fehler(koeder.look_waehlen, z, MODUL, "balsa_float", "koeder_2_3") is not None
            and fehler(koeder.look_waehlen, z, MODUL, "cork_float", "koeder_3_1") is not None, "ungebaut oder falscher Look: Fehler")

    # Wirkung im Angeln: Zone, Wartezeit, Seltenheit; der beste Koeder gilt
    def wurf(zz, i):
        zz["status"] = "wahl"
        zz.pop("angeln", None)
        angeln.starten(zz, MODUL, "boot")
        zz["angeln"]["wurf"], zz["angeln"]["wuerfe"] = i, 10 ** 6
        return angeln.auswerfen(zz, MODUL)
    ohne = copy.deepcopy(z)                       # derselbe Spielstand (gleicher Zufall), nur ohne Koeder
    ohne["kueche"].pop("koeder")
    # gleiche Wuerfe, nur mit/ohne Koeder: die Zone ist um genau die Koeder-Zone breiter
    for i in range(12):
        a, b = wurf(ohne, i), wurf(z, i)
        if a["art"] == "fisch" and b["art"] == "fisch":
            pruefen(abs(b["zone"] - a["zone"] - 0.03) < 1e-6 and a["biss"]["warten"] == b["biss"]["warten"],
                    "Stufe 1: Zone +0,03, Wartezeit unveraendert (Wurf %d)" % i)
            break

    # Stufe 2 + 3: Federn, besserer Koeder gilt, seltener, schneller
    for rid, n in {"cork": 2, "feather": 5, "iron": 3, "timber": 2}.items():
        kuechen.rohstoff_add(z, rid, n)
    z["konto"] = 500
    koeder.bauen(z, MODUL, "balsa_float", "koeder_2_4")
    pruefen(koeder.aktiv(z, MODUL)[0] == "balsa_float" and koeder.aktiv_ansicht(z, MODUL)["bild"] == "/farm/koeder/koeder_2_4.png",
            "Stufe 2 gebaut: sie gilt, ihr Look ist der Schwimmer")
    pruefen(koeder.ansicht(z, MODUL)[1]["aktiv"] and not koeder.ansicht(z, MODUL)[0]["aktiv"] and koeder.ansicht(z, MODUL)[0]["gebaut"],
            "Stufe 1 bleibt gebaut, ist aber nicht mehr auf der Leine")
    zeilen, gruppe = koeder.bauen(z, MODUL, "wooden_lure")
    pruefen(gruppe == "kauf_koeder_3" and koeder.besitz(z)["wooden_lure"] == "koeder_3_1" and z["konto"] == 500 - 70 - 130,
            "Stufe 3 gebaut, ohne Look-Angabe der erste Look")
    w = koeder.wirkung(z, MODUL)
    pruefen(w == {"zone": 0.07, "selten": {"2": 9, "3": 6}, "warten": 0.75}, "Wirkung der besten Stufe")
    pruefen(kuechen.rohstoffe(z)["feather"] == 0, "Federn verbraucht (2 + 3)")

    # Statistik: mit Stufe 3 beissen mehr seltene Fische und die Wartezeit ist kuerzer
    stufen = {"ohne": [], "lure": []}
    warten = {"ohne": [], "lure": []}
    for i in range(300):
        for name, zz in (("ohne", ohne), ("lure", z)):
            f = wurf(zz, i)
            if f["art"] == "fisch":
                stufen[name].append(f["stufe"])
            warten[name].append(f["biss"]["warten"])
    selten = {n: sum(1 for s in v if s >= 2) / len(v) for n, v in stufen.items()}
    pruefen(selten["lure"] > selten["ohne"] + 0.08, "Stufe 3: mehr seltene Fische (%.0f %% statt %.0f %%)" % (100 * selten["lure"], 100 * selten["ohne"]))
    pruefen(sum(warten["lure"]) / 300 < 0.85 * sum(warten["ohne"]) / 300, "Stufe 3: Biss kommt frueher")
    ans = angeln.ansicht(z, MODUL)
    pruefen(ans["koeder"]["id"] == "wooden_lure" and ans["koeder"]["bild"] == "/farm/koeder/koeder_3_1.png", "Angel-Ansicht traegt den Schwimmer")
    pruefen(angeln.ansicht(ohne, MODUL)["koeder"]["bild"] == "/farm/koeder/koeder_0_4.png", "ohne Koeder: Standard-Korken mit Feder (03.11.)")

    # Moewenfedern: Sieg und Aufgabe geben 2, Niederlage nichts
    angeln.MOEWE_CHANCE["meer"] = 1.0
    try:
        for art, feder in (("ko", 2), ("aufgabe", 2), ("flucht", 0), ("niederlage", 0)):
            g = spiel("m_" + art)
            angeln.starten(g, MODUL, "boot")
            while True:
                x = angeln.auswerfen(g, MODUL)
                e = angeln.ergebnis(g, MODUL, x["art"] == "fisch", 0)
                if e["ok"]:
                    break
            kampf.starten(g, DEFS, angeln.moewe_offen(g), rueckkehr={"status": g["status"]})
            g["kampf"]["ergebnis"] = {"art": art, "zeilen": []}
            zeilen = angeln.moewe_nach_kampf(g, MODUL)
            pruefen(kuechen.rohstoffe(g).get("feather", 0) == feder and (feder == 0 or "feathers" in zeilen[-1]),
                    "Moewe %s: %d Federn" % (art, feder))
    finally:
        angeln.MOEWE_CHANCE["meer"] = 0.15
    print("\nALLES OK")


if __name__ == "__main__":
    main()
