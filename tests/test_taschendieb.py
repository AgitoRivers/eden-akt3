# -*- coding: utf-8 -*-
"""Die Brueder Ricci (Duc + Brain Trust 29.10.2026, kern/taschendieb.py): Zufallskampf bei Alva/Petru, ab Tag 3, hoechstens
alle 2 Tage, baut sich auf (1 -> Brueder -> Bande), klaut 1/2/3 Verbrauchsgegenstaende (sonst Geld), gibt bei Sieg das
zuletzt Gestohlene zurueck, stichelt vertont.

  python tests\\test_taschendieb.py
"""
import json, os, sys, tempfile

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import lauf_test as L  # noqa: E402

E = L.eden


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def besuchen_bis_dieb(z, laden="alva", max_besuche=400):
    for _ in range(max_besuche):
        bid = E.taschendieb.ausloesen(z, laden)
        if bid:
            return bid
    return None


def kampf_ende(z, modul, defs, bid, art):
    E.kampf.starten(z, defs, bid)
    k = z["kampf"]
    E.kampf._finish(z, modul, k, art)
    if art == "niederlage":                         # Try again (Duc 03.11.2026): erst nach der Wahl wird abgerechnet
        pruefen(k["ergebnis"]["nochmal"] and E.taschendieb.nach_kampf(z, modul) == [] and not k.get("ricci_abgerechnet"),
                "vor der Wahl klauen die Riccis nichts")
        E.kampf.niederlage_annehmen(z, modul)
    zeilen = E.taschendieb.nach_kampf(z, modul)
    E.kampf.schliessen(z)
    return zeilen


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    L.vorbereiten("eden_rise", tempfile.mkdtemp(prefix="eden_ricci_"))
    z = E.aktion("neu", {"modus": "ironman"})
    z = E.aktion("persona", {"index": 0})
    if z["status"] == "prolog":
        z = E.aktion("prolog", {})
    modul = E.modul_laden()
    defs = E.kampf.daten(E.moddir("eden_rise"))
    T = E.taschendieb
    z["status"] = "wahl"

    z["tag"] = 2
    pruefen(besuchen_bis_dieb(z) is None, "vor Tag 3 keine Diebe")
    z["tag"] = 3
    pruefen(besuchen_bis_dieb(z, "lola") is None, "nur bei Alva und Petru")
    besuche_vorher = T.stand(z)["besuche"]
    bid = besuchen_bis_dieb(z)
    n = T.stand(z)["besuche"] - besuche_vorher
    pruefen(bid in T.STUFEN[1], "Stufe 1: ein Bruder allein (%s, nach %d Besuchen)" % (bid, n))
    pruefen(besuchen_bis_dieb(z) is None, "am selben Tag nicht nochmal")
    z["tag"] = 4
    pruefen(besuchen_bis_dieb(z) is None, "am naechsten Tag auch nicht (Abstand 2 Tage)")

    z["inventar"] = ["plaster", "plaster", "holm_compass", "espresso_single"]
    zeilen = kampf_ende(z, modul, defs, bid, "niederlage")
    pruefen(len(T.stand(z)["beute"]) == 1 and "holm_compass" in z["inventar"] and len(z["inventar"]) == 3,
            "verloren: genau 1 Verbrauchsgegenstand weg, das Andenken bleibt %s" % zeilen)
    pruefen(T.stand(z)["stufe"] == 1 and "ricci_1" in z["flags"], "Stufe 1 erledigt")

    z["tag"] = 5
    bid = besuchen_bis_dieb(z, "petru")
    pruefen(bid == "hafen_ricci_2", "naechste Begegnung: die Brueder")
    z["inventar"] = ["holm_compass", "espresso_single"]
    konto = z["konto"] = 100
    zeilen = kampf_ende(z, modul, defs, bid, "flucht")
    pruefen(z["inventar"] == ["holm_compass"] and z["konto"] == konto - 20,
            "Stufe 2: zwei Dinge - eins aus der Tasche, fuer das fehlende 20 EUR %s" % zeilen)

    z["tag"] = 7
    bid = besuchen_bis_dieb(z)
    pruefen(bid == "hafen_ricci_3", "danach: die Bande")
    beute = list(T.stand(z)["beute"])
    zeilen = kampf_ende(z, modul, defs, bid, "ko")
    pruefen(beute[-1] in z["inventar"] and T.stand(z)["beute"] == beute[:-1],
            "Sieg: das zuletzt Gestohlene kommt zurueck %s" % zeilen)
    pruefen(any("Elsa" in x for x in zeilen), "nach der Bande der Hinweis auf Elsa")
    z["tag"] = 20
    pruefen(besuchen_bis_dieb(z) is None, "nach Stufe 3 keine Diebe mehr")

    # Sprueche: erst start, dann runde; am Ende verliert/gewinnt - vertont als kampf.<gegner>.<art>.<n>
    E.kampf.starten(z, defs, "hafen_ricci_2")
    schluessel = []
    for _ in range(4):
        E.kampf.zug(z, modul, "verteidigen", parade=None)        # wie der Client: Zug und Parade getrennt
        schluessel += [e["schluessel"] for e in z["kampf"].get("events") or [] if e["art"] == "stimme"]
        if z["kampf"].get("ergebnis"):
            break
        while z["kampf"]["phase"] == "parade":                   # Gruppe: jeder Angreifer will pariert werden
            E.kampf.parade_aufloesen(z, modul, "ausweichen" if z["kampf"]["parade"].get("nur_ausweichen") else "gut")
    pruefen(schluessel[:3] == ["kampf.ricci_brueder.start.0", "kampf.ricci_brueder.start.1", "kampf.ricci_brueder.runde.0"],
            "Sticheleien der Reihe nach %s" % schluessel[:3])
    tags = {t["text"] for t in json.load(open(os.path.join(E.moddir("eden_rise"), "stimme_tags.json"), encoding="utf-8"))["zeilen"]}
    alle = [h for g in list(defs["enemies"].values()) + list(defs["encounters"].values())
            for liste in (g.get("sprueche") or {}).values() for h in liste]
    pruefen(alle and all(h["text"] in tags for h in alle), "jeder Spruch hat Turbo-Tags (%d)" % len(alle))
    pruefen(all(defs["encounters"][b]["level"] == "duc" for bs in T.STUFEN.values() for b in bs), "Level relativ zu Duc")
    print("OK")


if __name__ == "__main__":
    main()
