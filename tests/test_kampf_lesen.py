# -*- coding: utf-8 -*-
"""Lesen statt rechnen (Duc 03.11.2026, Sekiro/Clair Obscur): Der Spieler gewinnt durch Paraden, nie durch Schadenswissen.

Prueft die Antwort ueber dem Gegner (parieren / ausweichen / keine / flucht), das Bestiarium nach der ersten Parade einer
Art (Rhythmus ohne Zahlen) und die Finten je Gegnerart (Daten aus kaempfe.json, gleiche Finte je Absicht, damit man sie lernt).
Der Client darf fuer Gegnerangriffe keine Schadenszahl zeigen.

  python tests\\test_kampf_lesen.py
"""
import os, re, sys, unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import test_kampf as T  # noqa: E402  (Wegwerf-Spielstand, feste Wuerfel)

kampf, DEFS, MODUL = T.kampf, T.DEFS, T.MODUL
EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ECHT = kampf.daten(os.path.join(EDEN, "module", "eden_rise"))


class Antwort(unittest.TestCase):
    def test_normaler_schlag_heisst_parieren(self):
        z = T.new()
        T.set_intent(z, "n")
        a = kampf.ansicht(z, MODUL)["gegner"][0]["absicht"]
        self.assertEqual(a["antwort"], "parieren")

    def test_nur_ausweichen_und_harmlos(self):
        g = {"def": {"parade": "sprite"}}
        self.assertEqual(kampf.antwort(g, {"art": "angriff", "dodge_only": True}), "ausweichen")
        self.assertEqual(kampf.antwort(g, {"art": "angriff", "effect": "heal3"}), "keine")
        self.assertEqual(kampf.antwort(g, {"art": "flucht"}), "flucht")
        self.assertEqual(kampf.antwort(g, {"art": "angriff", "effect": "buff4", "bonus": 2}), "parieren")

    def test_jede_echte_absicht_hat_eine_antwort(self):
        for eid, e in ECHT["enemies"].items():
            g = {"def": e}
            for key, it in kampf._intents(e).items():
                self.assertIn(kampf.antwort(g, it), kampf.ANTWORT, (eid, key))


class Bestiarium(unittest.TestCase):
    def test_erst_nach_einer_parade(self):
        z = T.new()
        T.set_intent(z, "n")
        T.zug(z, "verteidigen", parade="verfehlt")
        self.assertFalse(z.get("bestiarium"))
        T.set_intent(z, "n")
        T.zug(z, "verteidigen", parade="perfekt")
        self.assertEqual(z["bestiarium"]["taschendieb"]["paraden"], 1)
        self.assertIn("bestiarium", [e["art"] for e in z["kampf"]["events"]])

    def test_zweite_parade_kein_neues_ereignis(self):
        z = T.new()
        for _ in range(2):
            T.set_intent(z, "n")
            T.zug(z, "verteidigen", parade="gut")
        self.assertEqual(z["bestiarium"]["taschendieb"]["paraden"], 2)
        self.assertNotIn("bestiarium", [e["art"] for e in z["kampf"]["events"]])

    def test_rhythmus_ohne_zahlen(self):
        for eid, e in ECHT["enemies"].items():
            for zeile in kampf.rhythmus(e):
                self.assertFalse(re.search(r"\d", zeile), (eid, zeile))

    def test_gleiche_art_gleicher_name_einmal(self):
        z = {"bestiarium": {"wolf": {"paraden": 1}, "mo_wolf": {"paraden": 2}}}
        b = kampf.bestiarium(z, ECHT)
        namen = [x["name"] for x in b]
        if kampf.rhythmus(ECHT["enemies"]["wolf"]) == kampf.rhythmus(ECHT["enemies"]["mo_wolf"]):
            self.assertEqual(namen.count("Collared Wolf"), 1)
            self.assertEqual(b[0]["paraden"], 3)


class Finten(unittest.TestCase):
    def test_finten_sind_gueltig(self):
        n = 0
        for eid, e in ECHT["enemies"].items():
            for key, it in kampf._intents(e).items():
                f = it.get("finte")
                if not f:
                    continue
                n += 1
                self.assertIn(f["art"], kampf.FINTE_TEXT, (eid, key))
                self.assertFalse(it.get("dodge_only"), (eid, key))
                self.assertNotEqual(e.get("parade"), "ring", eid)
        self.assertGreater(n, 20)

    def test_erste_gegner_ohne_finte(self):
        for eid in ("ratte", "moewe", "pirat", "taschendieb", "maxwell"):
            self.assertFalse(any(it.get("finte") for it in kampf._intents(ECHT["enemies"][eid]).values()), eid)

    def test_finte_geht_an_den_client(self):
        z = T.new()
        T.G(z)["intents"]["n"]["finte"] = {"art": "zoegern", "bei": 0.7, "halt": 450}
        T.set_intent(z, "n")
        T.zug(z, "verteidigen", parade=None)
        self.assertEqual(z["kampf"]["parade"]["finte"]["art"], "zoegern")
        self.assertTrue(kampf.ansicht(z, MODUL)["gegner"][0]["absicht"]["finte"] is not None)

    def test_zweites_mal_markiert(self):
        z = T.new()
        T.G(z)["intents"]["n"]["finte"] = {"art": "taeuschung", "bei": 0.8, "zurueck": 0.55}
        T.set_intent(z, "n")
        T.zug(z, "verteidigen", parade=None)
        self.assertFalse(z["kampf"]["parade"]["finte_bekannt"])          # first time: no hint
        kampf.parade_aufloesen(z, MODUL, "verfehlt", rng=T.NO)
        self.assertEqual(z["finten_gesehen"]["taschendieb:n"], 1)
        T.set_intent(z, "n")
        T.zug(z, "verteidigen", parade=None)
        self.assertTrue(z["kampf"]["parade"]["finte_bekannt"])           # second time: the bar marks it

    def test_finte_steht_im_rhythmus(self):
        e = ECHT["enemies"]["loewe_schwarz"]
        self.assertTrue(any("fakes a swing" in r for r in kampf.rhythmus(e)))


class Taunts(unittest.TestCase):
    def test_jede_art_hat_taunt(self):
        for eid, e in ECHT["enemies"].items():
            t = e.get("taunt") or {}
            self.assertTrue(t.get("sfx") or t.get("zeilen"), eid)

    def test_zoegern_hat_immer_taunt(self):
        for eid, e in ECHT["enemies"].items():
            for key, it in kampf._intents(e).items():
                if (it.get("finte") or {}).get("art") == "zoegern":
                    self.assertTrue(e.get("taunt"), (eid, key))

    def test_tiere_reden_nicht(self):
        for eid, e in ECHT["enemies"].items():
            if e["cls"] in ("tier", "flieger") and eid != "sirene":
                self.assertFalse((e.get("taunt") or {}).get("zeilen"), eid)

    def test_zeilen_loesen_auf(self):
        for gid, g in ECHT["taunts"].items():
            for z in g.get("zeilen") or []:
                wer, text = kampf.zeile(ECHT, z["id"])
                self.assertEqual((wer, text), ("stimme:" + g["stimme"], z["text"]))
                self.assertLess(len(text.split()), 9, text)
        self.assertEqual(kampf.zeile(ECHT, "kampf.taunt.agent.99"), (None, None))
        self.assertEqual(kampf.zeile(ECHT, "kampf.x"), (None, None))
        h = ECHT["enemies"]["sirene"].get("untouchable_hinweise") or []
        if h:
            self.assertEqual(kampf.zeile(ECHT, "kampf.sirene.0")[1], h[0]["text"])

    def test_taunt_nur_beim_zoegern(self):
        z = T.new()
        T.G(z)["def"]["taunt"] = {"gruppe": "dieb", "sfx": "x"}
        T.set_intent(z, "n")
        T.zug(z, "verteidigen", parade=None)
        self.assertIsNone(z["kampf"]["parade"]["taunt"])


class Rueckmeldung(unittest.TestCase):
    def test_serie_in_den_paradedaten(self):
        z = T.new()
        T.set_intent(z, "n")
        T.zug(z, "verteidigen", parade=None)
        p = z["kampf"]["parade"]
        self.assertEqual((p["serie"], p["serie_max"]), (0, kampf.PARADE_SERIE))

    def test_klaenge_im_katalog(self):
        import json
        d = json.load(open(os.path.join(EDEN, "module", "eden_rise", "sfx.json"), encoding="utf-8"))
        sfx = {x["id"]: x for x in d["sfx"]}
        for sid in ("kampf_warnung", "kampf_kette_2", "kampf_kette_3", "kampf_finte", "kampf_konter_kette"):
            self.assertIn(sid, sfx)
            for n in sfx[sid]["wahl"]:
                self.assertTrue(os.path.isfile(os.path.join(EDEN, "module", "eden_rise", "sfx", "%s_%d.mp3" % (sid, n))), (sid, n))
        for sid in ("wuerfel_erfolg", "wuerfel_fehlschlag"):            # one voice for the die, everywhere (Duc 03.11.2026)
            self.assertEqual(sfx[sid]["wahl"], 5, sid)
            self.assertTrue(os.path.isfile(os.path.join(EDEN, "module", "eden_rise", "sfx", "%s_5.mp3" % sid)))

    def test_client_nutzt_die_klaenge(self):
        js = open(os.path.join(EDEN, "client", "plugins", "eden-combat", "eden-combat.js"), encoding="utf-8").read()
        for sid in ("kampf_warnung", "kampf_kette_2", "kampf_kette_3", "kampf_finte", "kampf_konter_kette"):
            self.assertIn('"%s"' % sid, js)


class KeineSchadensvorschau(unittest.TestCase):
    def test_client_zeigt_keinen_gegnerschaden(self):
        js = open(os.path.join(EDEN, "client", "plugins", "eden-combat", "eden-combat.js"), encoding="utf-8").read()
        for muster in (r"a\.schaden", r"x\.x\.schaden", r"p\.schaden"):
            self.assertFalse(re.search(muster, js), muster)


if __name__ == "__main__":
    unittest.main()
