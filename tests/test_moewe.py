# -*- coding: utf-8 -*-
"""Moewe beim Angeln (Duc 29.10.2026, kern/angeln.py): am Meer schnappt eine Moewe den gelandeten Fisch (hoechstens einmal je
Gang), dann folgt der Kampf angel_moewe. Sieg: Fisch zurueck. Niederlage/Flucht: weg, das Journal zaehlt ihn trotzdem.

  python tests\\test_moewe.py
"""
import copy, json, os, sys

EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, EDEN)
from kern import angeln, kampf, kuechen, zustand  # noqa: E402

MOD = os.path.join(EDEN, "module", "eden_rise")
MODUL = json.load(open(os.path.join(MOD, "modul.json"), encoding="utf-8"))
DEFS = copy.deepcopy(kampf.daten(MOD))


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def gang(sid):
    """Angelgang am Boot bis zum ersten gelandeten Fisch (Fundsachen werden losgelassen)."""
    z = zustand.neu(MODUL, "entspannt")
    zustand.persona_setzen(z, MODUL, MODUL["personas"][0])
    z["tag"], z["phase"], z["status"], z["id"] = 5, "tag", "wahl", sid
    angeln.starten(z, MODUL, "boot")
    while True:
        w = angeln.auswerfen(z, MODUL)
        e = angeln.ergebnis(z, MODUL, w["art"] == "fisch", 0)
        if e["ok"]:
            return z, e


def kampf_ende(z, art):
    """Der Moewen-Kampf startet wie in eden.py und endet mit art (ko, aufgabe, flucht, niederlage, entkommen)."""
    kampf.starten(z, DEFS, angeln.moewe_offen(z), rueckkehr={"status": z["status"]})
    z["kampf"]["ergebnis"] = {"art": art, "zeilen": []}
    return angeln.moewe_nach_kampf(z, MODUL)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    alt = dict(angeln.MOEWE_CHANCE)
    pruefen(DEFS["encounters"]["angel_moewe"]["enemy"] == "moewe" and DEFS["enemies"]["moewe"]["sprite"] == "Seagull",
            "Kampf angel_moewe mit der Moewe (Sprite Seagull)")
    pruefen(alt == {"meer": 0.15}, "Moewe nur am Meer, 15 % je gelandetem Fisch")

    angeln.MOEWE_CHANCE["meer"] = 0.0
    z, e = gang("ohne")
    pruefen(not e.get("moewe") and angeln.moewe_offen(z) is None, "ohne Moewe: Fisch landet normal")

    angeln.MOEWE_CHANCE["meer"] = 1.0
    try:
        z, e = gang("sieg")
        roh = next(f for f in kuechen.daten(MODUL)["fische"] if f["id"] == e["id"])["roh"]
        vorher = kuechen.vorrat_menge(z, roh)
        pruefen(e["moewe"] == "klaut" and angeln.moewe_offen(z) == "angel_moewe", "Moewe schnappt den Fisch, Kampf steht an")
        pruefen(e["id"] in z["kueche"]["fischbuch"], "im Journal steht er trotzdem")
        zeilen = kampf_ende(z, "ko")
        pruefen(e["moewe"] == "zurueck" and kuechen.vorrat_menge(z, roh) == vorher + 1 and "back" in zeilen[0],
                "Sieg: Fisch zurueck in den Vorrat (%s)" % zeilen[0])
        pruefen(kampf_ende(z, "ko") == [] if angeln.moewe_offen(z) else True, "nur einmal abgerechnet")
        w = angeln.auswerfen(z, MODUL)
        e2 = angeln.ergebnis(z, MODUL, w["art"] == "fisch", 0)
        pruefen(not e2.get("moewe"), "hoechstens eine Moewe je Angelgang")

        z, e = gang("weg")
        roh = next(f for f in kuechen.daten(MODUL)["fische"] if f["id"] == e["id"])["roh"]
        vorher = kuechen.vorrat_menge(z, roh)
        zeilen = kampf_ende(z, "flucht")
        pruefen(e["moewe"] == "weg" and kuechen.vorrat_menge(z, roh) == vorher and "got away" in zeilen[0],
                "Flucht: der Fisch ist weg")
        pruefen(any("a gull took it" in x for x in angeln.ende(z, MODUL)), "Angel-Meldung nennt die Moewe")
    finally:
        angeln.MOEWE_CHANCE.clear()
        angeln.MOEWE_CHANCE.update(alt)
    print("alle Moewen-Tests gruen")


if __name__ == "__main__":
    main()
