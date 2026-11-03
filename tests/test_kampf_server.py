# -*- coding: utf-8 -*-
"""Kampf ueber die Engine-Aktionen (Etappe 3, 19.10.2026): Status "kampf" als Unterbrechung, kampf_zug -> Parade-Phase ->
kampf_parade, Ansicht mit Bildern und Zugfolge, Ende und kampf_schliessen zurueck in den vorherigen Status.
Ohne Sprachmodell (lauf_test-Umgebung), Wegwerf-Spielstaende.

  python tests\\test_kampf_server.py
"""
import os, sys, tempfile, unittest

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import lauf_test as L  # noqa: E402

E = L.eden


def durchlauf():
    L.vorbereiten("eden_rise", tempfile.mkdtemp(prefix="eden_kampf_"))
    z = E.aktion("neu", {"modus": "ironman"})
    z = E.aktion("persona", {"index": 0})
    if z["status"] == "prolog":
        z = E.aktion("prolog", {})
    return z


class KampfServer(unittest.TestCase):
    def test_ablauf(self):
        z = durchlauf()
        vorher = z["status"]
        E.kampf_starten(z, E.modul_laden(), "hafen_dieb_test")
        E.sichern(z)
        self.assertEqual(E.aktiv()["status"], "kampf")
        v = E.ansicht(E.aktiv())
        k = v["z"]["kampf"]
        self.assertEqual(k["phase"], "spieler_wahl")
        self.assertTrue(k["gegner"][0]["bilder"]["idle"].startswith("/kampfbild/Thief/idle.webp"))
        self.assertEqual(v["z"]["hintergrund"], "/bg/corsican_village_harbour.png")
        with self.assertRaises(ValueError):
            E.aktion("zug", {"text": "hallo"})                   # keine Szene im Kampf
        z = E.aktion("kampf_zug", {"befehl": "angriff", "revision": k["revision"]})
        self.assertEqual(z["kampf"]["phase"], "parade")
        rev = z["kampf"]["revision"]
        with self.assertRaises(ValueError):                        # Doppelklick mit alter Revision
            E.aktion("kampf_zug", {"befehl": "angriff", "revision": k["revision"]})
        z = E.aktion("kampf_parade", {"ergebnis": "perfekt", "revision": rev})
        self.assertEqual(z["kampf"]["letzte_parade"], "perfekt")
        with self.assertRaises(ValueError):
            E.aktion("kampf_parade", {"ergebnis": "perfekt", "revision": rev})
        z = E.aktion("kampf_zug", {"befehl": "fliehen", "revision": z["kampf"]["revision"]})
        self.assertEqual(z["kampf"]["ergebnis"]["art"], "flucht")
        z = E.aktion("kampf_schliessen", {})
        self.assertIsNone(z["kampf"])
        self.assertEqual(z["status"], vorher)
        self.assertIn("kampftest_tasche_weg", z["flags"])
        self.assertTrue(z["meldungen"][-1]["titel"].startswith("⚔"))

    def test_kein_kampf(self):
        durchlauf()
        with self.assertRaises(ValueError):
            E.aktion("kampf_zug", {"befehl": "angriff"})


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    unittest.main(verbosity=1, warnings="ignore")
