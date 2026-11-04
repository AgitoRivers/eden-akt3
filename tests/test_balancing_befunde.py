# -*- coding: utf-8 -*-
"""Belege fuer den Balancing-Bericht (docs/uebergabe/balancing_bericht.md, Cloud-Sitzung 04.11.2026).

Jeder Test beschreibt das Verhalten, das Wiki oder Drehbuch versprechen. Wo der Code heute anders rechnet, ist der Test als
expectedFailure markiert: Er laeuft gruen, solange der Befund besteht, und meldet sich ("unexpected success"), sobald jemand
den Code anpasst. Nichts hier aendert Spieldaten.

    python tests/test_balancing_befunde.py
"""
import copy, json, os, sys, unittest

HIER = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(HIER)
sys.path.insert(0, EDEN)
from kern import kampf, taktik, zustand  # noqa: E402

M = os.path.join(EDEN, "module", "eden_rise")
MODUL = json.load(open(os.path.join(M, "modul.json"), encoding="utf-8"))


def _duc(level):
    defs = taktik.kampf_defs({"flags": [], "werte": {}}, M)
    z = zustand.neu(MODUL)
    zustand.persona_setzen(z, MODUL, copy.deepcopy(MODUL["personas"][0]))
    kampf.test_setup(z, defs, level=level, skills=[], weapon="sword", armor="jacket_earth")
    return z, defs


class WhiteAbstand(unittest.TestCase):
    """taktik_eden_rise.py: tk_white = begegnung(..., 4): Mr. White steht vier Level ueber Duc. kampf.starten klemmt auf LEVEL_MAX."""

    def abstand(self, duc_level):
        z, defs = _duc(duc_level)
        k = kampf.starten(z, defs, "tk_white")
        return k["gegner"][0]["level"] - duc_level

    def test_abstand_bei_niedrigem_level(self):
        self.assertEqual(self.abstand(4), 4)

    @unittest.expectedFailure
    def test_abstand_bleibt_bei_hohem_level(self):
        """Bei Duc Level 7 und hoeher schrumpft der Abstand (10 - Level), bei Level 10 ist White gleich stark wie ein normaler Gegner."""
        self.assertGreaterEqual(self.abstand(9), 3)


class TuerenRudern(unittest.TestCase):
    """drehbuch_finale.md, Tag 22 Mittag, Auftrag Tueren: Mit Petru rudert das Dorf schon ab Ruf 4."""

    def rudert(self, ruf, flags):
        D = taktik.daten(M)
        return taktik._rudert({"werte": {"ruf": ruf}, "flags": flags}, D, {"haeuser": {}})

    def test_ohne_petru_ab_ruf_5(self):
        self.assertFalse(self.rudert(4, []))
        self.assertTrue(self.rudert(5, []))

    @unittest.expectedFailure
    def test_mit_petru_ab_ruf_4(self):
        """kern/taktik.py _rudert liest bl_tueren_petru nicht."""
        self.assertTrue(self.rudert(4, ["bl_tueren_petru"]))


class KleineRoboter(unittest.TestCase):
    """Kobra und Skorpion sind auf der Karte eigene Gegner (schnell, Jaeger, Schwaeche). Im echten Kampf bauen beide auf
    der Vorlage unit01 auf: gleicher Schlag, gleiche Ruestung, gleiches Muster wie der Boarding Robot, nur etwas weniger Leben."""

    def test_gleiche_werte_wie_boarding_robot(self):
        z, defs = _duc(6)
        werte = {}
        for bid in ("tk_kobra", "tk_skorpion", "tk_roboter"):
            z2 = copy.deepcopy(z)
            g = kampf.starten(z2, defs, bid)["gegner"][0]
            werte[bid] = (g["lp_max"], round(g["atk"], 1), g["armor"], g["pattern"])
        for klein in ("tk_kobra", "tk_skorpion"):
            self.assertEqual(werte[klein][1:], werte["tk_roboter"][1:])
            self.assertLessEqual(werte[klein][0], werte["tk_roboter"][0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
