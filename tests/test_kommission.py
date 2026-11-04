# -*- coding: utf-8 -*-
r"""Kommission als Verhandlung (kern/kommission.py, module/eden_rise/kommission.json): Ace-Attorney-Regeln, Geduld,
Festlegen durch Press, Plaedoyer, Flags fuer die Saeule Wahrheit.

  python tests/test_kommission.py
"""
import json, os, re, sys

EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, EDEN)
sys.path.insert(0, os.path.join(EDEN, "werkzeuge", "eden_rise"))
from kern import akt3, kommission  # noqa: E402
MD = os.path.join(EDEN, "module", "eden_rise")
D = kommission.daten(MD)
TAGS = {(z["wer"], z["text"]): z["gesprochen"] for z in json.load(open(os.path.join(MD, "stimme_tags.json"), encoding="utf-8"))["zeilen"]}


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def z_mit(*flags):
    return {"flags": ["buenaventura_schwur"] + list(flags), "werte": {}}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    import kommission_akt3 as K
    pruefen(not K.pruefe(D), "Daten stimmig: jede Karte widerlegt nur falsche Saetze, jeder falsche Satz hat eine Karte")
    pruefen(len(D["runden"]) == 3 and all(len(r["saetze"]) == 3 for r in D["runden"]), "drei Runden mit je drei Saetzen")
    pruefen(kommission.AN is False, "Schalter aus, bis das Plugin gebaut ist")
    immer = {c["id"] for c in kommission.karten(z_mit(), D)}
    pruefen(immer == {"buenaventura", "riscossore"}, "ohne Zeugen und Beweise: Buenaventura und der Riscossore (Kanon)")

    # Perfekter Lauf: Feuer mit Buenaventura, Tor erst nach Press mit Alva, Geld mit dem Riscossore
    z = z_mit("a3_zeuge_alva")
    kommission.beginnen(z, D)
    kommission.vorlegen(z, D, 0, "buenaventura")
    pruefen(z["kommission"]["runden"]["feuer"] == "gewonnen" and z["kommission"]["runde"] == 1, "Runde 1 gewonnen")
    kommission.vorlegen(z, D, 0, "alva")
    pruefen(z["kommission"]["geduld"] == 2 and "tor" not in z["kommission"]["runden"], "zu frueh: erst festlegen lassen (Press), sonst Geduld -1")
    kommission.press(z, D, 0)
    kommission.vorlegen(z, D, 0, "alva")
    pruefen(z["kommission"]["runden"]["tor"] == "gewonnen", "nach Press: Alva widerlegt das Tor")
    kommission.vorlegen(z, D, 0, "riscossore")
    pruefen(z["kommission"]["geduld"] == 1 and any(e["art"] == "spott" for e in z["kommission"]["log"]), "ein wahrer Satz: der Anwalt spottet, Geduld -1")
    kommission.vorlegen(z, D, 1, "riscossore")
    pruefen(z["kommission"]["schritt"] == "plaedoyer", "nach drei Runden: das Plaedoyer (Pascals Kassenbuch)")
    kommission.plaedoyer(z, D, "alles")
    f = z["flags"]
    pruefen(all(x in f for x in ("a3_kom_feuer", "a3_kom_tor", "a3_kom_geld", "a3_kom_runden_3", "a3_kassenbuch_alles", "a3_kommission_fertig")),
            "Ergebnis als Flags")
    pruefen(akt3.saeulen(z)["wahrheit"], "zwei oder drei gewonnene Runden tragen die Saeule Wahrheit")

    # Geduld weg: die uebrigen Runden sind verloren
    z = z_mit()
    kommission.beginnen(z, D)
    for _ in range(3):
        kommission.vorlegen(z, D, 2, "riscossore")
    k = z["kommission"]
    pruefen(k["geduld"] == 0 and k["schritt"] == "plaedoyer" and set(k["runden"].values()) == {"verloren"}, "Geduld 0: Rest verloren, gleich das Plaedoyer")
    # Nichts sagen
    z = z_mit()
    kommission.beginnen(z, D)
    kommission.nichts(z, D)
    pruefen(z["kommission"]["runden"]["feuer"] == "verloren" and z["kommission"]["geduld"] == 3, "keine Antwort: Runde verloren, Geduld bleibt")
    try:
        kommission.vorlegen(z, D, 0, "alva")
        raise AssertionError("fremde Karte")
    except ValueError:
        print("OK nur eigene Karten")
    a = kommission.ansicht(z, D)
    pruefen(a and len(a["aussage"]) == 3 and a["karten"] and a["geduld_max"] == 3, "Ansicht fuer das Plugin")

    # Jede Zeile vertont mit Turbo-Tag, nie im Spieltext
    alle = [s for r in D["runden"] for s in [r["ansage"], r["treffer"], r["anwalt_wackelt"], r["dorf"]] + [x["text"] for x in r["saetze"]] + [x["press"] for x in r["saetze"]]]
    turbo = re.compile(r"\[(laugh|chuckle|sigh|gasp|cough|clear throat|sniff|shush)\]")
    pruefen(all(not turbo.search(s["text"]) and turbo.search(TAGS.get((s["wer"], s["text"]), "")) for s in alle), "alle %d Zeilen mit Turbo-Tag" % len(alle))
    print("Alle Pruefungen gruen.")


if __name__ == "__main__":
    main()
