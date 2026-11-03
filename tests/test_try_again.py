# -*- coding: utf-8 -*-
"""Try again (Duc 03.11.2026): Nach einer Niederlage darf Duc denselben Kampf einmal neu versuchen, mit den LP und der
Tasche vom Kampfbeginn. Die Folgen der Niederlage warten auf die Wahl. Eine zweite Niederlage oder "Accept the defeat"
bringt die normalen Folgen. Nicht im Training, nicht bei den Hafen-Wellen, nicht in der Belagerung.

  python tests\\test_try_again.py
"""
import os, sys, tempfile, unittest

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import lauf_test as L  # noqa: E402

E = L.eden
K = E.kampf


def durchlauf():
    L.vorbereiten("eden_rise", tempfile.mkdtemp(prefix="eden_try_"))
    z = E.aktion("neu", {"modus": "ironman"})
    z = E.aktion("persona", {"index": 0})
    if z["status"] == "prolog":
        z = E.aktion("prolog", {})
    return z


def verlieren():
    """Duc auf 1 LP setzen und den Gegnerschlag voll nehmen, bis der Kampf verloren ist."""
    for _ in range(20):
        z = E.aktiv()
        k = z["kampf"]
        if k.get("ergebnis"):
            return z
        if k["phase"] == "parade":
            E.aktion("kampf_parade", {"ergebnis": "verfehlt", "revision": k["revision"]})
        else:
            k["spieler"]["lp"] = 1
            E.sichern(z)
            E.aktion("kampf_zug", {"befehl": "verteidigen", "revision": k["revision"]})
    raise AssertionError("Kampf ging nicht verloren")


class TryAgain(unittest.TestCase):
    def starten(self, bid):
        z = durchlauf()
        z["inventar"] = ["plaster", "bandage"]
        z["lp"] = 40
        E.kampf_starten(z, E.modul_laden(), bid)
        E.sichern(z)
        return E.aktiv()

    def test_einmal_neu_dann_niederlage(self):
        self.starten("hafen_dieb_test")
        z = verlieren()
        e = z["kampf"]["ergebnis"]
        self.assertEqual(e["art"], "niederlage")
        self.assertTrue(e["nochmal"], "erste Niederlage bietet Try again an")
        self.assertNotIn("kampftest_niederlage", z["flags"], "Folgen warten auf die Wahl")
        z["inventar"] = []                                   # im Kampf verbraucht
        E.sichern(z)
        z = E.aktion("kampf_nochmal", {})
        k = z["kampf"]
        self.assertEqual(z["status"], "kampf")
        self.assertFalse(k.get("ergebnis"), "der Kampf läuft neu")
        self.assertTrue(k["nochmal_genutzt"])
        self.assertEqual(k["spieler"]["lp"], 40, "LP wie beim ersten Start")
        self.assertEqual(z["inventar"], ["plaster", "bandage"], "Tasche wie beim ersten Start")
        self.assertEqual(k["gegner"][0]["lp"], k["gegner"][0]["lp_max"], "Gegner wieder voll (gleiche Bedingungen)")
        z = verlieren()
        e = z["kampf"]["ergebnis"]
        self.assertFalse(e["nochmal"], "kein drittes Mal")
        self.assertIn("kampftest_niederlage", z["flags"], "zweite Niederlage: normale Folgen")
        with self.assertRaises(ValueError):
            E.aktion("kampf_nochmal", {})
        z = E.aktion("kampf_schliessen", {})
        self.assertIsNone(z["kampf"])

    def test_niederlage_annehmen(self):
        self.starten("hafen_dieb_test")
        verlieren()
        z = E.aktion("kampf_nochmal", {"annehmen": True})
        e = z["kampf"]["ergebnis"]
        self.assertFalse(e["nochmal"])
        self.assertIn("kampftest_niederlage", z["flags"], "angenommen: Folgen genau jetzt")
        with self.assertRaises(ValueError):
            E.aktion("kampf_nochmal", {})
        z = E.aktion("kampf_schliessen", {})
        self.assertEqual(z["flags"].count("kampftest_niederlage"), 1, "Folgen genau einmal")

    def test_weiter_ohne_wahl_heisst_annehmen(self):
        self.starten("hafen_dieb_test")
        verlieren()
        z = E.aktion("kampf_schliessen", {})
        self.assertIsNone(z["kampf"])
        self.assertEqual(z["flags"].count("kampftest_niederlage"), 1, "Continue ohne Wahl wendet die Folgen einmal an")

    def test_ausnahmen(self):
        self.assertFalse(K.nochmal_moeglich({"def": {"training": True}}), "Training")
        self.assertFalse(K.nochmal_moeglich({"def": {"neustart_bei_niederlage": True}}), "Hafen-Wellen starten ohnehin neu")
        self.assertFalse(K.nochmal_moeglich({"def": {}, "rueckkehr": {"status": "taktik"}}), "Belagerung")
        self.assertFalse(K.nochmal_moeglich({"def": {}, "held": {"id": "maxwell"}}), "Maxwell als Kämpfer")
        self.assertFalse(K.nochmal_moeglich({"def": {}, "nochmal_genutzt": True}), "nur einmal")
        self.assertTrue(K.nochmal_moeglich({"def": {"expedition_niederlage": True}}), "Expeditionen ja")


if __name__ == "__main__":
    unittest.main()
