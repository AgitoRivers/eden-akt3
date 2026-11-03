# -*- coding: utf-8 -*-
"""Angeln (27.10.2026; seit 28.10. an Quellen ohne Zeitpreis): Orte (Boot + Rastplaetze mit Wasser), Bestand und Nachwuchs,
Sitzung, Wurf (Fisch/Fundsache, Stufen), Drill-Werte, Fang mit Qualitaet, Journal, Sammel-Bonus, Ende.

Laeuft ohne Modell, Stimme und Netz.

  python tests\\test_angeln.py
"""
import collections, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(HERE)
sys.path.insert(0, EDEN)
from kern import abbau, angeln, kuechen, zustand  # noqa: E402

MODUL = json.load(open(os.path.join(EDEN, "module", "eden_rise", "modul.json"), encoding="utf-8"))
A = kuechen.daten(MODUL)["angeln"]
A_BILDER = kuechen.daten(MODUL)["abbau"]["angel_bilder"]


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


def neues_spiel(sid="t1"):
    z = zustand.neu(MODUL, "entspannt")
    zustand.persona_setzen(z, MODUL, MODUL["personas"][0])
    z["tag"], z["phase"], z["status"], z["id"] = 5, "tag", "wahl", sid
    z["persona"]["attribute"]["perception"] = 2
    return z


def orte_pruefen():
    z = neues_spiel()
    o = {x["id"]: x for x in angeln.orte(z, MODUL)}
    pruefen(list(o) == ["boot"] and o["boot"]["rest"] == 4 and o["boot"]["bild"].endswith("eden_rise_angeln_boot.png"),
            "freie Wahl: nur das Boot, 4 Würfe Bestand")
    pruefen("angeln" not in z and "kueche" not in z, "Lesen legt keine Schlüssel an")
    pruefen(fehler(angeln.starten, z, MODUL, "kl_bachufer") is not None, "Bach nur unterwegs, nicht aus der freien Wahl")
    pruefen(fehler(angeln.starten, z, MODUL, "kl_huette") is not None, "an der Hütte gibt es kein Wasser")
    z["status"] = "ereignis"
    pruefen(fehler(angeln.starten, z, MODUL, "kl_bachufer", "kl_huette") is not None, "am falschen Frame kein Bach")
    angeln.starten(z, MODUL, "kl_bachufer", "kl_bachufer")
    pruefen(z["status"] == "angeln" and z["angeln"]["zurueck"] == "ereignis", "am Rastplatz-Frame mit Wasser geht es los")
    pruefen(angeln.ende(z, MODUL) == [] and z["status"] == "ereignis", "Einpacken ohne Wurf: zurück an den Rastplatz")
    z["status"] = "szene"
    pruefen(fehler(angeln.starten, z, MODUL, "boot") is not None, "nicht mitten in einer Szene")


def sitzung_pruefen():
    z = neues_spiel()
    angeln.starten(z, MODUL, "boot")
    pruefen(z["status"] == "angeln" and z["angeln"]["wurf"] == 0, "Sitzung läuft")
    w1 = angeln.auswerfen(z, MODUL)
    pruefen(angeln.auswerfen(z, MODUL) is w1 or angeln.auswerfen(z, MODUL) == w1, "Neuladen wirft nicht neu (gleicher Wurf)")
    dr = A["drill"][str(w1["stufe"])]
    pruefen(w1["treffer"] == dr["treffer"] and w1["zone"] == dr["zone"] and w1["tempo"] == dr["tempo"], "Drill-Werte nach Stufe (%s)" % w1)
    pruefen(1.4 <= w1["biss"]["warten"] <= 3.6 and w1["biss"]["fenster"] == A["biss"]["fenster"], "Biss: Wartezeit und Fenster")
    v = angeln.ansicht(z, MODUL)
    meer = A_BILDER["boot"]                    # Duc 29.10.: das Boot zieht nur die 5 Yacht-Bilder
    pruefen(v["aktiv"]["nr"] == 1 and v["wuerfe"] == 4 and v["bild"][len("/bg/"):] in meer and len(v["journal"]["fische"]) == 20,
            "Ansicht: Wurf 1/4, Hintergrund aus den Yacht-Bildern, Journal mit 20 Fischen")
    pruefen(not set(A_BILDER["boot"]) & set(A_BILDER["meer"]) and len(A_BILDER["boot"]) == len(A_BILDER["meer"]) == 5,
            "Meer geteilt: 5 Yacht-Bilder fürs Boot, 5 Küstenbilder für die Rastplätze")
    zz = neues_spiel("bilder")
    folge = []
    for _ in range(12):                       # Wechselbilder (28.10.): nie zweimal hintereinander dasselbe am selben Platz
        angeln.starten(zz, MODUL, "boot")
        folge.append(zz["angeln"]["bild"])
        angeln.ende(zz, MODUL)
    pruefen(all(b in meer for b in folge) and all(a != b for a, b in zip(folge, folge[1:])) and len(set(folge)) >= 4,
            "Wechselbilder: 12 Gänge am Boot, nie zweimal dasselbe hintereinander (%d verschiedene)" % len(set(folge)))
    zk = neues_spiel("kueste")
    zk["status"] = "ereignis"
    kueste = []
    for _ in range(6):                        # Rastplatz am Meer (Drowned Beach): nur Kuestenbilder
        angeln.starten(zk, MODUL, "gr_strand", "gr_strand")
        kueste.append(zk["angeln"]["bild"])
        angeln.ende(zk, MODUL)
    pruefen(all(b in A_BILDER["meer"] for b in kueste), "Rastplatz am Meer zieht nur Küstenbilder (%s)" % ", ".join(sorted(set(kueste))))
    # Fang ohne Fehlklick: 3 Sterne
    z["angeln"]["aktiv"] = dict(w1, art="fisch", id="sea_bass", stufe=1)
    e = angeln.ergebnis(z, MODUL, True, 0, False)
    pruefen(e["ok"] and e["stern"] == 3 and e["neu"] and kuechen.vorrat_menge(z, "sea_bass_roh", 3) == 1, "perfekter Drill: Rohform mit 3 Sternen, neu im Journal")
    pruefen(fehler(angeln.ergebnis, z, MODUL, True, 0, False) is not None, "kein zweites Ergebnis ohne neuen Wurf")
    w2 = angeln.auswerfen(z, MODUL)
    z["angeln"]["aktiv"] = dict(w2, art="fisch", id="sea_bass", stufe=1)
    e = angeln.ergebnis(z, MODUL, True, 2, False)
    pruefen(e["stern"] == 2 and not e["neu"] and z["kueche"]["fischbuch"]["sea_bass"] == {"n": 2, "bester": 3}, "mit Fehlklicks 2 Sterne, Journal zählt")
    w3 = angeln.auswerfen(z, MODUL)
    z["angeln"]["aktiv"] = dict(w3, art="fisch", id="sardine", stufe=1)
    e = angeln.ergebnis(z, MODUL, True, 0, True)
    pruefen(e["stern"] == 2, "entspannter Modus: höchstens 2 Sterne")
    w4 = angeln.auswerfen(z, MODUL)
    z["angeln"]["aktiv"] = dict(w4, art="fund", id="driftwood", stufe=0)
    e = angeln.ergebnis(z, MODUL, True, 0, False)
    pruefen(kuechen.rohstoffe(z).get("timber") == 1 and e["rohstoffe"][0]["label"] == "Timber", "Fundsache Treibholz: +1 Timber")
    pruefen(fehler(angeln.auswerfen, z, MODUL) is not None, "nach 4 Würfen ist Schluss")
    zeilen = angeln.ende(z, MODUL)
    pruefen(z["status"] == "wahl" and "angeln" not in z and "4 casts" in zeilen[0], "Ende: Zusammenfassung, zurück zur Wahl (%s)" % zeilen[0])
    # Bestand: leer, 3 Tage Pause, dann wieder voll
    pruefen(abbau.stand(z, MODUL, "boot", "wasser") == (0, 8) and fehler(angeln.starten, z, MODUL, "boot") is not None,
            "Quelle leer: erst an Tag 8 wieder")
    pruefen(angeln.orte(z, MODUL)[0]["in_tagen"] == 3, "Karte zeigt: in 3 Tagen")
    z["tag"] = 8
    pruefen(abbau.stand(z, MODUL, "boot", "wasser") == (4, None), "nach 3 Tagen nachgewachsen")
    # angefangene Quelle behaelt ihren Rest
    z2 = neues_spiel()
    angeln.starten(z2, MODUL, "boot")
    angeln.auswerfen(z2, MODUL)
    angeln.ergebnis(z2, MODUL, False, 0, False, "riss")
    angeln.ende(z2, MODUL)
    angeln.starten(z2, MODUL, "boot")
    pruefen(z2["angeln"]["wuerfe"] == 3, "nach einem Wurf und Einpacken: noch 3 Würfe")
    # Fehlschlag
    z3 = neues_spiel()
    angeln.starten(z3, MODUL, "boot")
    angeln.auswerfen(z3, MODUL)
    e = angeln.ergebnis(z3, MODUL, False, 0, False, "biss")
    pruefen(not e["ok"] and e["grund"] == "biss", "Biss verpasst: kein Fang")


def verteilung_pruefen():
    zaehler, orte = collections.Counter(), collections.Counter()
    meer = {f["id"] for f in kuechen.daten(MODUL)["fische"] if f["ort"] == "meer"}
    for i in range(1500):
        z = neues_spiel("v%d" % i)
        angeln.starten(z, MODUL, "boot")
        w = angeln.auswerfen(z, MODUL)
        zaehler[w["stufe"]] += 1
        if w["art"] == "fisch":
            orte[w["id"] in meer] += 1
    n = sum(zaehler.values())
    pruefen(0.10 <= zaehler[0] / n <= 0.20, "Fundsachen ~15 %% (%.0f %%)" % (100 * zaehler[0] / n))
    fische = n - zaehler[0]
    pruefen(0.52 <= zaehler[1] / fische <= 0.68 and 0.22 <= zaehler[2] / fische <= 0.38 and 0.05 <= zaehler[3] / fische <= 0.15,
            "Stufen ~60/30/10 (%s)" % dict(zaehler))
    pruefen(orte[False] == 0, "am Boot beißen nur Meeresfische")


def wahrnehmung_und_bonus_pruefen():
    z = neues_spiel()
    z["persona"]["attribute"]["perception"] = 5
    angeln.starten(z, MODUL, "boot")
    w = angeln.auswerfen(z, MODUL)
    dr = A["drill"][str(w["stufe"])]
    pruefen(abs(w["zone"] - (dr["zone"] + 3 * A["wahrnehmung_zone"])) < 1e-9 and w["biss"]["fenster"] > A["biss"]["fenster"],
            "Wahrnehmung 5: Zone und Biss-Fenster größer")
    # alle 10 Meeresfische -> Sammel-Bonus
    z2 = neues_spiel()
    angeln.starten(z2, MODUL, "boot")
    meer = [f["id"] for f in kuechen.daten(MODUL)["fische"] if f["ort"] == "meer"]
    bonus = None
    for fid in meer:
        z2["angeln"]["wurf"] = 0
        z2.get("kueche", {}).pop("quellen", None)          # Bestand fuer den Test immer voll
        w = angeln.auswerfen(z2, MODUL)
        z2["angeln"]["aktiv"] = dict(w, art="fisch", id=fid)
        bonus = angeln.ergebnis(z2, MODUL, True, 1, False).get("bonus") or bonus
    pruefen(bonus and bonus["label"] == "Lea's Lucky Lure" and z2["kueche"]["angel_boni"] == ["meer"], "alle 10 Meeresfische: Lea's Lucky Lure")
    j = angeln.journal(z2, MODUL)
    pruefen(j["gefangen"] == 10 and [b["frei"] for b in j["boni"]] == [True, False], "Journal: 10/20, Meer-Bonus frei")
    z2["angeln"]["wurf"] = 0
    w = angeln.auswerfen(z2, MODUL)
    dr = A["drill"][str(w["stufe"])]
    pruefen(abs(w["zone"] - (dr["zone"] + A["sammel_bonus"]["meer"]["zone"])) < 1e-9, "Bonus macht die Zone dauerhaft größer")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    orte_pruefen()
    sitzung_pruefen()
    verteilung_pruefen()
    wahrnehmung_und_bonus_pruefen()
    print("ALLES OK")
