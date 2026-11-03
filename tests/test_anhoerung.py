# -*- coding: utf-8 -*-
"""Anhoerung Akt 1 (Scheibe 3, 24.10.2026): Urteile in allen sechs Faellen, ohne Oberflaeche und ohne Sprachmodell.

Je Fall: Erbarmen (richtig, Kette, Motiv, ehrlich, Gnade) · Ehrlichkeit fehlt -> aufgeklaert · Strafe -> Bewaehrung ·
ohne Kette -> unbelegt · falsche Person -> falsch · kein Name -> offen · Fall ohne Verantwortliche: "niemand allein"
mit Kette -> entlastet. Dazu Megans Adern (nur Raten kostet) und die Loyalitaet der Schwestern.
Ausgaben nennen nur Fallnummern und Urteile (spoilerfrei).

  python tests\\test_anhoerung.py
"""
import json, os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(HIER)
sys.path.insert(0, EDEN)
from kern import anhoerung, ermittlung, abschluss  # noqa: E402

MODUL = json.load(open(os.path.join(EDEN, "module", "eden_rise", "modul.json"), encoding="utf-8"))
STORY = json.load(open(os.path.join(EDEN, "module", "eden_rise", "story.json"), encoding="utf-8"))
VERDACHT = STORY["verdaechtige"]


def zustand(nr, kette=False, vertrauen=None):
    z = {"id": "test-%d" % nr, "modul": "eden_rise", "wahrheit": "fall_%d" % nr, "tag": 7, "phase": "tag",
         "werte": {"moral": 3, "rueckhalt": 50}, "flags": []}
    for p, v in (vertrauen or {}).items():
        z["werte"]["vertrauen." + p] = v
    e = ermittlung.stand(z)
    if kette:
        for g in ermittlung.fall(z)["glieder"]:
            for fid in g["beweis_saetze"][0]:
                e["bekannt"][fid] = {"tag": 6, "phase": "tag", "weg": "test"}
    return z


def spielen(z, angeklagt, ehrlich, art):
    anhoerung.anklagen(z, MODUL, angeklagt)
    anhoerung.rolle(z, MODUL, ehrlich)
    folgen, hinweis, zeilen = anhoerung.plaedoyer(z, MODUL, art)
    assert hinweis and zeilen, "Hinweis und Zeilen fehlen"
    return anhoerung.stand(z)["urteil"], folgen


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    for fall in STORY["faelle"]:
        nr, v = fall["nr"], fall["verantwortlich"]
        unschuldig = next(p for p in VERDACHT if p != v)
        if v:
            u, f = spielen(zustand(nr, True, {v: 3}), v, True, "gnade")
            pruefen(u == "erbarmen", "Fall %d: Erbarmen erwartet, %s" % (nr, u))
            pruefen({"wert": "vertrauen." + v, "delta": 2} in f, "Fall %d: Erbarmen ohne Vertrauen +2" % nr)
            u, _ = spielen(zustand(nr, True, {v: 3}), v, False, "gnade")
            pruefen(u == "aufgeklaert", "Fall %d: ohne Ehrlichkeit kein Erbarmen, %s" % (nr, u))
            u, _ = spielen(zustand(nr, True, {v: 0}), v, True, "gnade")
            pruefen(u == "aufgeklaert", "Fall %d: ohne Motiv kein Erbarmen, %s" % (nr, u))
            u, f = spielen(zustand(nr, True, {v: 3}), v, True, "strafe")
            pruefen(u == "aufgeklaert" and {"flag": "gefeuert_" + v} in f and {"flag": "bewaehrung_" + v} not in f,
                    "Fall %d: volle Strafe -> gefeuert (Duc 26.10.2026)" % nr)
            pruefen(any(x.get("geld") == anhoerung.PRAEMIE for x in f), "Fall %d: Praemie bei bewiesener Kette" % nr)
            z = zustand(nr, True, {v: 3})
            ermittlung.stand(z)["gestaendnis"] = 5
            u, f = spielen(z, v, True, "strafe")
            pruefen({"flag": "verrat_" + v} in f, "Fall %d: Gestaendnis + Feuern = Verrat" % nr)
            u, f = spielen(zustand(nr, True, {v: 3}), v, False, "teilen")
            pruefen({"wert": "vertrauen.megan", "delta": -1} in f and {"wert": "moral", "delta": 1} in f,
                    "Fall %d: Schuld teilen kostet Megan-Vertrauen, hebt die Moral" % nr)
            u, f = spielen(zustand(nr, True, {v: 3}), unschuldig, True, "strafe")
            pruefen(u == "falsch" and {"wert": "moral", "delta": -1} in f, "Fall %d: Strafe gegen Unschuldige kostet Moral" % nr)
            u, f = spielen(zustand(nr, True, {v: 3}), unschuldig, True, "gnade")
            pruefen({"wert": "vertrauen." + unschuldig, "delta": -1} in f, "Fall %d: Gnade fuer Unschuldige mildert" % nr)
            z = zustand(nr, False, {v: 3})
            u, _ = spielen(z, v, True, "gnade")
            pruefen(u == "unbelegt", "Fall %d: ohne Kette unbelegt, %s" % (nr, u))
            pruefen(anhoerung.stand(z)["adern"] == 2, "Fall %d: Raten kostet genau eine Ader" % nr)
            z = zustand(nr, True, {v: 3})
            spielen(z, v, True, "gnade")
            pruefen(anhoerung.stand(z)["adern"] == 3, "Fall %d: belegte Anklage kostet keine Ader" % nr)
        else:
            u, _ = spielen(zustand(nr, True), "niemand", True, "gnade")
            pruefen(u == "entlastet", "Fall %d: niemand allein mit Kette -> entlastet, %s" % (nr, u))
            u, _ = spielen(zustand(nr, False), "niemand", True, "gnade")
            pruefen(u == "offen", "Fall %d: niemand allein ohne Kette -> offen, %s" % (nr, u))
        z = zustand(nr, True)
        u, f = spielen(z, unschuldig, True, "gnade")
        pruefen(u == "falsch", "Fall %d: falsche Person -> falsch, %s" % (nr, u))
        pruefen(any(x["pid"] == unschuldig and x["oeffentlich"] for x in ermittlung.stand(z)["vorwuerfe"]),
                "Fall %d: Anklage zählt als öffentlicher Vorwurf (Entschuldigung danach)" % nr)
        u, f = spielen(zustand(nr, True), None, True, "gnade")
        pruefen(u == "offen" and {"flag": "kuendigung_angedroht"} in f, "Fall %d: kein Name -> offen" % nr)
        ende = abschluss.berechnen(z, MODUL)
        pruefen(ende["titel"] == "End of Act 1" and ende["dimensionen"]["urteil"] == "falsch" and not ende["frauen"],
                "Fall %d: Schlusskarte Akt 1" % nr)
        anwesend = ["megan"] + ermittlung.besetzung(zustand(nr), MODUL, "$fall3", "anhoerung")
        opt = anhoerung.anklage_optionen(zustand(nr), MODUL, anwesend)
        pids = [o["anhoerung"]["pid"] for o in opt]
        pruefen(2 <= len(opt) <= 4 and pids[-1] == "niemand", "Fall %d: Anklage-Optionen 2-4, niemand zuletzt" % nr)
        pruefen(not v or v in pids, "Fall %d: die Verantwortliche ist anklagbar" % nr)
        print("OK Fall %d" % nr)

    # Loyalitaet: eine Schwester gibt der angeklagten Schwester ein Alibi - nur wenn diese es war und Duc ihr
    # wenig vertraut; mit belegtem Glied "person" entlarvt der Einspruch es.
    for fall in STORY["faelle"]:
        v = fall["verantwortlich"]
        if v not in ("lea", "sophia"):
            continue
        schwester = "sophia" if v == "lea" else "lea"
        z = zustand(fall["nr"], True, {schwester: 1})
        anhoerung.anklagen(z, MODUL, v)
        w = next(x for x in anhoerung.stand(z)["zeugen"] if x["pid"] == schwester)
        pruefen(w["luegt"] and w["entlarvt"], "Fall %d: Alibi der Schwester entlarvt" % fall["nr"])
        z = zustand(fall["nr"], True, {schwester: 3})
        anhoerung.anklagen(z, MODUL, v)
        w = next(x for x in anhoerung.stand(z)["zeugen"] if x["pid"] == schwester)
        pruefen(not w["luegt"], "Fall %d: bei Vertrauen 3 lügt die Schwester nicht" % fall["nr"])
        z = zustand(fall["nr"], False, {schwester: 1})
        anhoerung.anklagen(z, MODUL, v)
        w = next(x for x in anhoerung.stand(z)["zeugen"] if x["pid"] == schwester)
        pruefen(w["luegt"] and not w["entlarvt"], "Fall %d: ohne Beleg hält das Alibi" % fall["nr"])
        print("OK Loyalität Fall %d" % fall["nr"])
    print("OK")


if __name__ == "__main__":
    main()
