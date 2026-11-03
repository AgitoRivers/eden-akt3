# -*- coding: utf-8 -*-
"""Mehrere Gegner in einem Kampf (Duc 29.10.2026, wie Final Fantasy): bis zu 3, Zielwahl, jeder mit eigener Absicht
und eigenen Zustaenden, sie handeln der Reihe nach (jeder Angriff eine Parade), Flaeche (Mistral, Lame de Fond, alle
Granaten), Einschuechtern schreckt die anderen, Fliehen mit dem schwersten Fluchtwert, Erfahrung fuer alle Besiegten.
Einzelkaempfe bleiben unveraendert (tests/test_kampf.py).

  python tests\\test_mehrgegner.py
"""
import copy, os, sys, unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import test_kampf as T  # noqa: E402  (Wegwerf-Spielstand, feste Wuerfel, alte Regelwerte)

kampf, DEFS, MODUL = T.kampf, T.DEFS, T.MODUL
DEFS["encounters"]["rudel3"] = dict(copy.deepcopy(DEFS["encounters"]["hafen_dieb_test"]), enemy="ratte",
                                    enemies=["ratte", "ratte", "ratte"], level=1, flee_allowed=True)
DEFS["encounters"]["paar"] = dict(copy.deepcopy(DEFS["encounters"]["hafen_dieb_test"]), enemy="ratte",
                                  enemies=["ratte", "taschendieb"], level=1)


def neu(bid="rudel3", **kw):
    return T.new(bid, **kw)


def K(z):
    return z["kampf"]


class Aufbau(unittest.TestCase):
    def test_drei_ratten_mit_buchstaben(self):
        z = neu()
        g = K(z)["gegner"]
        self.assertEqual([x["name"] for x in g], ["Rat A", "Rat B", "Rat C"])
        self.assertEqual([x["schritt"] for x in g], [0, 1, 2])                # versetzt: nicht alle gleichzeitig
        self.assertEqual(len({x["instanz"] for x in g}), 3)

    def test_ansicht_zeigt_alle_und_das_ziel(self):
        z = neu()
        kampf.ziel_waehlen(z, 2)
        v = kampf.ansicht(z, MODUL)
        self.assertEqual(len(v["gegner"]), 3)
        self.assertEqual(v["zielgegner"], 2)
        self.assertEqual(len(v["zugfolge"]), 3)
        self.assertEqual(v["zugfolge"][0]["wer"], "Rat A")

    def test_einzelkampf_unveraendert(self):
        z = T.new()
        v = kampf.ansicht(z, MODUL)
        self.assertEqual((len(v["gegner"]), v["zielgegner"]), (1, 0))
        self.assertNotIn("wer", v["zugfolge"][0])


class Ziel(unittest.TestCase):
    def test_angriff_trifft_nur_das_ziel(self):
        z = neu()
        T.zug(z, "angriff", gegner=1)
        g = K(z)["gegner"]
        self.assertEqual([x["lp"] < x["lp_max"] for x in g], [False, True, False])

    def test_besiegter_geht_kampf_laeuft_weiter(self):
        z = neu()
        g = K(z)["gegner"]
        g[0]["lp"] = 1
        T.zug(z, "angriff", gegner=0)
        g = K(z)["gegner"]
        self.assertEqual(g[0]["aus"], "ko")
        self.assertIsNone(K(z)["ergebnis"])
        self.assertIs(kampf.ziel_gegner(K(z)), g[1])                         # das Ziel springt weiter
        with self.assertRaises(ValueError):
            kampf.ziel_waehlen(z, 0)

    def test_alle_besiegt_sieg_mit_erfahrung_aller(self):
        z = neu()
        for x in K(z)["gegner"]:
            x["lp"] = 1
        K(z)["spieler"]["lp"] = K(z)["spieler"]["lp_max"] = 500           # hier zaehlt die Erfahrung, nicht die Balance
        xp_einer = kampf.xp_for(1, kampf.progress(z)["level"])
        for i in range(3):
            if K(z)["ergebnis"]:
                break
            T.zug(z, "angriff", gegner=i)
            while K(z)["phase"] == "parade":                                  # mehrere Angreifer: jede Parade
                kampf.parade_aufloesen(z, MODUL, "gut", rng=T.NO)
        self.assertEqual(K(z)["ergebnis"]["art"], "ko")
        self.assertEqual(K(z)["ergebnis"]["xp"], 3 * xp_einer)


class Reihenfolge(unittest.TestCase):
    def test_jeder_angriff_eine_parade(self):
        z = neu()
        for x in K(z)["gegner"]:
            x["absicht"] = "n"                                               # alle greifen an
        T.zug(z, "verteidigen", parade=None)
        k = K(z)
        self.assertEqual((k["phase"], k["parade"]["gegner"]), ("parade", 0))
        kampf.parade_aufloesen(z, MODUL, "gut", rng=T.NO)
        self.assertEqual((K(z)["phase"], K(z)["parade"]["gegner"]), ("parade", 1))
        kampf.parade_aufloesen(z, MODUL, "gut", rng=T.NO)
        self.assertEqual(K(z)["parade"]["gegner"], 2)
        runde = K(z)["runde"]
        kampf.parade_aufloesen(z, MODUL, "gut", rng=T.NO)
        self.assertEqual((K(z)["phase"], K(z)["runde"]), ("spieler_wahl", runde + 1))   # erst danach Rundenende

    def test_konter_trifft_den_angreifer(self):
        z = neu()
        for x in K(z)["gegner"]:
            x["absicht"] = "n"
        T.zug(z, "verteidigen", parade=None)
        kampf.parade_aufloesen(z, MODUL, "verfehlt", rng=T.NO)               # Ratte A ist durch
        kampf.parade_aufloesen(z, MODUL, "perfekt", rng=T.NO)                # Ratte B: Konter
        g = K(z)["gegner"]
        self.assertTrue(g[1]["lp"] < g[1]["lp_max"] and g[0]["lp"] == g[0]["lp_max"])


class Flaeche(unittest.TestCase):
    def test_mistral_trifft_alle(self):
        z = neu(skills=["K3"])
        T.F(z, "mistral")
        self.assertTrue(all(x["lp"] < x["lp_max"] and x["states"].get("erschuettert") for x in K(z)["gegner"]))

    def test_granate_trifft_alle(self):
        z = neu(inv=["grenade_fire"])
        T.zug(z, "gegenstand", "grenade_fire")
        self.assertTrue(all(x["lp"] < x["lp_max"] for x in K(z)["gegner"]))

    def test_einschuechtern_schreckt_die_anderen(self):
        z = neu("paar")
        fass = [x["fassung"] for x in K(z)["gegner"]]
        T.F(z, "einschuechtern", ergebnis="erfolg", parade=None)
        g = K(z)["gegner"]
        self.assertTrue(g[0]["states"].get("geschwaecht"))
        self.assertEqual(g[1]["fassung"], fass[1] - kampf.SCHRECK_ANDERE)


class Flucht(unittest.TestCase):
    def test_schwerster_fluchtwert(self):
        z = neu("paar")
        self.assertEqual(kampf._flucht_sg(K(z)), max(kampf.FLEE_DC[x["def"]["tier"]] for x in K(z)["gegner"]))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    unittest.main(verbosity=1, warnings="ignore")
