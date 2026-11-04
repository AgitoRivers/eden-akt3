# -*- coding: utf-8 -*-
"""Folgen der Belagerung und Akt-3-Start (Duc 04.11.2026): Die drei Auftraege, die vorher nichts bewirkten, wirken jetzt,
und Akt 3 beginnt fuer Schneider, Lesung, Holms Revanche, Rosis grosse Tasche und das Ende der Sperre an Tag 24.

    python tests/test_akt2_folgen.py

Laeuft ohne Sprites und ohne eden-config.json (Taktik-Daten aus module/eden_rise/taktik.json)."""
import json, os, sys, unittest

HIER = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(HIER)
sys.path.insert(0, EDEN)
from kern import ereignisse, schiessen, taktik  # noqa: E402

M = os.path.join(EDEN, "module", "eden_rise")
MODUL = json.load(open(os.path.join(M, "modul.json"), encoding="utf-8"))
EV = {e["id"]: e for e in json.load(open(os.path.join(M, "ereignisse.json"), encoding="utf-8"))["events"]}
D = taktik.daten(M)


def rudert(ruf, flags, werkstatt=None):
    t = {"haeuser": {D["ruder_haus"]: {"status": werkstatt}} if werkstatt else {}}
    return taktik._rudert({"werte": {"ruf": ruf}, "flags": flags}, D, t)


class Tueren(unittest.TestCase):
    """Auftrag Tueren (Tag 22 mittags): Mit Petru rudert das Dorf schon ab Ruf 4 (Drehbuch Finale)."""

    def test_ohne_petru_ab_ruf_5(self):
        self.assertFalse(rudert(4, []))
        self.assertTrue(rudert(5, []))

    def test_mit_petru_ab_ruf_4(self):
        self.assertTrue(rudert(4, ["bl_tueren_petru"]))
        self.assertFalse(rudert(3, ["bl_tueren_petru"]))

    def test_lola_und_mina_aendern_nichts(self):
        self.assertFalse(rudert(4, ["bl_tueren_lola"]))
        self.assertFalse(rudert(4, ["bl_tueren_mina"]))

    def test_ruder_und_petru_zusammen(self):
        self.assertTrue(rudert(3, ["bl_tueren_petru"], "gerettet"))
        self.assertFalse(rudert(2, ["bl_tueren_petru"], "gerettet"))


class Kirche(unittest.TestCase):
    """Auftrag Kirche (Tag 23 morgens): Don bei den Kindern gibt der Kirche einmal ein Leben mehr."""

    def test_don_gibt_ein_leben(self):
        t = {"kirche": 3, "kirche_max": 4}
        taktik._don_glocke({"flags": ["bl_kirche_don"]}, t)
        self.assertEqual((t["kirche"], t["kirche_max"], t["don_glocke"]), (4, 5, True))

    def test_nur_einmal(self):
        t = {"kirche": 3, "kirche_max": 4}
        z = {"flags": ["bl_kirche_don"]}
        taktik._don_glocke(z, t)
        taktik._don_glocke(z, t)
        self.assertEqual(t["kirche"], 4)

    def test_ohne_don_nichts(self):
        for f in ([], ["bl_kirche_jana"], ["bl_kirche_casanova"]):
            t = {"kirche": 3, "kirche_max": 4}
            taktik._don_glocke({"flags": f}, t)
            self.assertEqual(t, {"kirche": 3, "kirche_max": 4})

    def test_bleibt_ueber_die_wellen(self):
        self.assertIn("don_glocke", taktik.BEHALTEN)


class AlvasRunde(unittest.TestCase):
    """Tag 22 Abend: Mit bl_alva_runde zahlt Duc die Runde, sonst geht sie aufs Haus."""

    def test_zwei_fassungen(self):
        a, b = EV["bl_bar"], EV["bl_bar_runde"]
        self.assertEqual(a["wann"]["bedingung"], {"nicht": {"flag": "bl_alva_runde"}})
        self.assertEqual(b["wann"]["bedingung"], {"flag": "bl_alva_runde"})
        self.assertEqual(a["wann"]["tage"], b["wann"]["tage"])

    def test_nur_mit_versprechen_zahlt_duc(self):
        geld = lambda e: [f for o in e["optionen"] for f in o["folgen"] if "geld" in f]
        self.assertEqual(geld(EV["bl_bar"]), [])
        self.assertTrue(geld(EV["bl_bar_runde"]))
        self.assertTrue(all(any("geld" in f for f in o["folgen"]) for o in EV["bl_bar_runde"]["optionen"]))

    def test_ohne_versprechen_kein_versprechen_im_text(self):
        self.assertNotIn("promised", EV["bl_bar"]["zeilen"][0]["text"])
        self.assertIn("promised", EV["bl_bar_runde"]["zeilen"][0]["text"])


class Akt3AbTag24(unittest.TestCase):
    def test_sperre_endet_nach_tag_23(self):
        self.assertEqual(MODUL["sperre"].get("bis"), 23)
        z = lambda tag: {"tag": tag}
        self.assertEqual(ereignisse.gesperrt_durch_story(z(23), MODUL, "abend"), "bl_")
        self.assertIsNone(ereignisse.gesperrt_durch_story(z(24), MODUL, "fruehstueck"))

    def test_schneider_und_lesung_ab_tag_24(self):
        for eid in ("sn_apron", "ol_wunsch"):
            self.assertEqual(EV[eid]["wann"].get("akt2"), [24, 35], eid)

    def test_station_beweis_auch_in_akt_3(self):
        for eid in ("mo_schlafgranate", "mo_halsbaender"):
            self.assertEqual(EV[eid]["wann"].get("akt2"), [24, 35], eid)

    def test_holm_und_tasche(self):
        self.assertEqual(schiessen.HOLM_TAG, 24)
        self.assertEqual(MODUL["tasche"]["stufen"][1]["ab_tag"], 24)


if __name__ == "__main__":
    unittest.main(verbosity=2)
