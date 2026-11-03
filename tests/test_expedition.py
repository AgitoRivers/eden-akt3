# -*- coding: utf-8 -*-
"""Expedition rule (26.10.2026, Duc): on a defeat Duc keeps ONE piece of the loot found on the way, the rest is lost;
what he brought stays, LP are refilled, the snapshot is dropped. Plus the Kloster fights exist and follow the rule.

  python tests\\test_expedition.py
"""
import copy, json, os, sys, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(HERE)
sys.path.insert(0, EDEN)
from kern import expedition, kampf, zustand  # noqa: E402

MODDIR = os.path.join(EDEN, "module", "eden_rise")
MODUL = json.load(open(os.path.join(MODDIR, "modul.json"), encoding="utf-8"))
DEFS = copy.deepcopy(kampf.daten(MODDIR))
KLOSTER = [b for b in DEFS["encounters"] if b.startswith("kloster_")]


def new():
    z = zustand.neu(MODUL)
    zustand.persona_setzen(z, MODUL, copy.deepcopy(MODUL["personas"][0]))
    z["inventar"] = ["multitool"]
    return z


class Expedition(unittest.TestCase):
    def test_start_by_folge(self):
        z = new()
        zustand.folgen_anwenden(z, MODUL, [{"expedition": "kloster"}])
        self.assertEqual(expedition.aktiv(z)["inventar"], ["multitool"])
        zustand.folgen_anwenden(z, MODUL, [{"expedition": "ende"}])
        self.assertIsNone(expedition.aktiv(z))

    def test_defeat_keeps_one_piece(self):
        z = new()
        kampf.chip_pool(z)["pool"]["wucht"] = 1                   # brought along: stays
        expedition.starten(z, "kloster")
        z["inventar"] += ["holm_compass", "petru_key"]              # found on the way
        kampf.chip_pool(z)["pool"]["wucht"] = 2                    # upgraded on the way
        kampf.chip_pool(z)["pool"]["technik"] = 1                  # new on the way
        ids = [b["id"] for b in expedition.beute(z, MODUL, DEFS)]
        self.assertEqual(sorted(ids), sorted(["item:holm_compass", "item:petru_key", "chip:wucht", "chip:technik"]))
        expedition.behalten(z, MODUL, DEFS, "chip:technik")
        z["lp"] = 3
        zeilen = expedition.scheitern(z, MODUL, DEFS)
        self.assertEqual(z["inventar"], ["multitool"])
        self.assertEqual(kampf.chip_pool(z)["pool"], {"wucht": 1, "technik": 1})
        self.assertEqual(z["lp"], kampf.max_lp(kampf.progress(z)["level"]))
        self.assertIn("expedition_kloster_gescheitert", z["flags"])
        self.assertIsNone(expedition.aktiv(z))
        self.assertTrue(any("You wake up on the ship" in t for t in zeilen))

    def test_keep_only_from_loot(self):
        z = new()
        expedition.starten(z, "kloster")
        with self.assertRaises(ValueError):
            expedition.behalten(z, MODUL, DEFS, "item:multitool")

    def test_keep_nothing(self):
        z = new()
        expedition.starten(z, "kloster")
        z["inventar"].append("holm_compass")
        expedition.behalten(z, MODUL, DEFS, None)
        expedition.scheitern(z, MODUL, DEFS)
        self.assertEqual(z["inventar"], ["multitool"])

    def test_chip_folge(self):
        z = new()
        zustand.folgen_anwenden(z, MODUL, [{"chip": ["konter", 3]}])
        self.assertEqual(kampf.chip_pool(z)["pool"].get("konter"), 3)

    def test_scout_reveals_only_from_worn_jacket(self):
        # Items 26.10.2026: kampf.aufklaerung counts the chip in the worn jacket; level I hears collars only
        z = new()
        bild = lambda sprite, pose: "/kampfbild/%s/%s.webp" % (sprite, pose)
        ratte = {"folgen": [{"kampf": "kloster_1_ratte"}, {"weiter": "kl_bruecke"}]}
        keiler = {"folgen": [{"kampf": "kloster_2_keiler"}]}
        self.assertFalse(expedition.wahl_info(z, DEFS, keiler, bild)["kampf"]["bekannt"])
        z["flags"].append(DEFS["werkstatt"]["flag"])                          # Rosi's workshop is open
        kampf.chip_pool(z)["pool"]["scout"] = 1
        self.assertFalse(expedition.wahl_info(z, DEFS, keiler, bild)["kampf"]["bekannt"])      # only in the pool
        kampf.chip_in_jacke(z, DEFS, "scout")
        self.assertEqual(expedition.wahl_info(z, DEFS, keiler, bild)["kampf"]["name"], "Alpha Boar")
        self.assertEqual(expedition.wahl_info(z, DEFS, ratte, bild)["kampf"]["name"], "Animal")
        self.assertNotIn("level", expedition.wahl_info(z, DEFS, keiler, bild)["kampf"])
        kampf.chip_pool(z)["pool"]["scout"] = 2
        info = expedition.wahl_info(z, DEFS, ratte, bild)["kampf"]
        self.assertEqual((info["name"], info["level"]), ("Rat", 1))
        self.assertTrue(expedition.wahl_info(z, DEFS, {"folgen": []}, bild)["ende"])

    def test_rest_call_rotation(self):
        # Duc 26.10.2026: top 3 by trust; after the first comes the second, then the third, then the first again
        z = new()
        for pid, pts in (("lola", 40), ("toto", 30), ("rosi", 20), ("holm", 5)):
            zustand.punkte_add(z, MODUL, "vertrauen." + pid, pts)
        reihe = []
        for _ in range(4):
            pid = expedition.rast_anrufer(z)
            z["rast_anruf_letzt"] = pid
            reihe.append(pid)
        self.assertEqual(reihe, ["lola", "toto", "rosi", "lola"])

    def test_rest_heals_respawns_and_calls(self):
        z = new()
        zustand.punkte_add(z, MODUL, "vertrauen.lola", 40, quelle="szenen")   # Events-Topf (30) bleibt frei fuer den Anruf
        stufe = str(z["werte"]["vertrauen.lola"])
        texte = {"lola": {stufe: [{"text": "Are you eating?", "antworten": [{"text": "a", "ton": "warm"}, {"text": "b", "ton": "frech"}]}]}}
        z["lp"], z["ort_frame"], z["ort_besiegt"] = 3, "kl_huette", ["kl_start", "kl_bruecke"]
        orig = expedition.rast_texte
        expedition.rast_texte = lambda moddir: texte
        try:
            expedition.rasten(z, MODDIR)
        finally:
            expedition.rast_texte = orig
        self.assertEqual(z["lp"], kampf.max_lp(kampf.progress(z)["level"]))
        self.assertEqual(z["ort_besiegt"], [])
        self.assertEqual(z["rast_anruf"]["pid"], "lola")
        abstand, zustand.STUFEN_ABSTAND = zustand.STUFEN_ABSTAND, 0      # hier zaehlt der Anruf, nicht der Stufen-Abstand
        self.addCleanup(setattr, zustand, "STUFEN_ABSTAND", abstand)
        vorher = zustand.punkte(z, "vertrauen.lola")
        expedition.rast_antwort(z, MODUL, 0)
        self.assertEqual(zustand.punkte(z, "vertrauen.lola"), vorher + zustand.PUNKTE_JE_STUFE)
        self.assertIsNone(z["rast_anruf"])

    def test_kloster_fights(self):
        self.assertEqual(len(KLOSTER), 9)
        for bid in KLOSTER:
            b = DEFS["encounters"][bid]
            self.assertTrue(b["expedition_niederlage"], bid)
            self.assertEqual(b["weapon"], "bat", bid)
            self.assertEqual(DEFS["enemies"][b["enemy"]]["element"], "erde", bid)
            self.assertIn("goes black", b["outcomes"]["niederlage"]["text"], bid)
        levels = [DEFS["encounters"][b]["level"] for b in KLOSTER]
        self.assertEqual(levels, sorted(levels))
        self.assertEqual((min(levels), max(levels)), (1, 3))                    # Balancing 26.10.2026: flach 1-3


if __name__ == "__main__":
    unittest.main()
