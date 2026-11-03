# -*- coding: utf-8 -*-
"""Combat consumables (Duc + Brain Trust 27.10.2026, docs/wiki/systeme/kampf.md "Gegenstände"): one rule per item,
quick items cost no turn (one per round), weapon care from the inventory before the fight.

    python tests\\test_kampf_gegenstaende.py
"""
import os, sys, unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import test_kampf as T  # noqa: E402  (helpers and the fixed rule numbers)
from kern import handel, kampf  # noqa: E402

S, G, zug, new = T.S, T.G, T.zug, T.new


class Gegenstaende(unittest.TestCase):
    def test_first_aid_kit_heals_percent_and_stops_bleeding(self):
        z = new(inv=["verbandskasten"])
        S(z)["lp"], S(z)["states"]["blutend"] = 10, 2
        zug(z, "gegenstand", "verbandskasten", parade=None)
        self.assertEqual(S(z)["lp"], 10 + 14)                       # 40 % of 36, before the enemy's blow
        self.assertNotIn("blutend", S(z)["states"])
        self.assertNotIn("verbandskasten", z["inventar"])

    def test_quick_item_keeps_the_turn_once_per_round(self):
        z = new(inv=["plaster", "espresso_single"])
        S(z)["lp"], S(z)["ausdauer"] = 20, 2
        runde = z["kampf"]["runde"]
        zug(z, "gegenstand", "plaster", parade=None)
        self.assertEqual(z["kampf"]["phase"], "spieler_wahl")       # no enemy turn
        self.assertEqual(z["kampf"]["runde"], runde)
        self.assertEqual(S(z)["lp"], 24)
        g = {x["id"]: x for x in kampf.gegenstaende(z, T.MODUL)}
        self.assertEqual(g["espresso_single"]["gesperrt"], "One quick item per round.")
        zug(z, "angriff", parade="verfehlt")
        self.assertIsNone({x["id"]: x for x in kampf.gegenstaende(z, T.MODUL)}["espresso_single"]["gesperrt"])

    def test_megaphone_and_dog_food_depend_on_the_enemy(self):
        z = new(inv=["dog_food", "megaphone"])                      # the pickpocket is a human
        g = {x["id"]: x for x in kampf.gegenstaende(z, T.MODUL)}
        self.assertIn("isn't interested", g["dog_food"]["gesperrt"])
        f = G(z)["fassung"]
        zug(z, "gegenstand", "megaphone", parade="verfehlt")
        self.assertEqual(G(z)["fassung"], f - 5)
        z = new(bid="akt1_ratte", inv=["dog_food"])
        zug(z, "gegenstand", "dog_food", parade=None)
        self.assertNotEqual(z["kampf"]["phase"], "parade")          # the rat eats instead of biting
        self.assertIn("skips a round", " ".join(z["kampf"]["log"][-1]["zeilen"]))

    def test_smoke_pot_dodges_the_next_attack_and_frees_the_escape(self):
        z = new(inv=["smoke_pot"])
        lp = S(z)["lp"]
        zug(z, "gegenstand", "smoke_pot", parade=None)
        self.assertNotEqual(z["kampf"]["phase"], "parade")
        self.assertEqual(S(z)["lp"], lp)
        zug(z, "fliehen")
        self.assertEqual(z["kampf"]["ergebnis"]["art"] if isinstance(z["kampf"]["ergebnis"], dict) else z["kampf"]["ergebnis"],
                         "flucht")

    def test_weapon_care_matches_the_weapon_kind(self):
        z = new(inv=["whetstone_blue", "spikes"])                   # test weapon "faust" is blunt
        g = {x["id"]: x for x in kampf.gegenstaende(z, T.MODUL)}
        self.assertTrue(g["whetstone_blue"]["gesperrt"].startswith("Not for"))
        roh = kampf.raw_hit(S(z), G(z))
        zug(z, "gegenstand", "spikes", parade="verfehlt")
        self.assertEqual(kampf.raw_hit(S(z), G(z)), roh + 3)
        self.assertEqual(S(z)["pflege"]["runden"], 4)               # 5 rounds, one is over

    def test_weapon_care_before_the_fight(self):
        z = new(inv=["spikes"], start=False)
        handel.benutzen(z, T.MODUL, "spikes")
        self.assertEqual(z["waffenpflege"]["art"], "stumpf")
        kampf.starten(z, T.DEFS, "hafen_dieb_test", rng=T.NO)
        self.assertEqual(S(z)["pflege"]["bonus"], 3)
        self.assertNotIn("waffenpflege", z)

    def test_cooling_spray_antidote_tea_tape(self):
        z = new(inv=["cooling_spray", "antidote", "green_tea", "duct_tape"])
        S(z)["states"].update(brennend=2, burn_new=1)
        zug(z, "gegenstand", "cooling_spray", parade=None)
        self.assertNotIn("brennend", S(z)["states"])
        kampf._duc_state(T.ctx(z), "brennend", 2)
        self.assertNotIn("brennend", S(z)["states"])                # immune for 2 rounds
        S(z)["states"].update(nass=2, geblendet=1, ungedeckt=1)
        zug(z, "gegenstand", "antidote", parade="verfehlt")
        self.assertFalse(set(S(z)["states"]) & set(kampf.DUC_BAD))
        T.set_intent(z, "n")
        ohne = kampf._parade_data(T.ctx(z), "n", G(z)["intents"]["n"])["fenster"]["faktor"]
        zug(z, "gegenstand", "green_tea", parade=None)
        self.assertAlmostEqual(kampf._parade_data(T.ctx(z), "n", G(z)["intents"]["n"])["fenster"]["faktor"], ohne * 1.15, 1)
        prot = S(z)["armor"]["prot"]
        zug(z, "gegenstand", "duct_tape", parade=None)
        self.assertEqual(z["kampf"]["phase"], "parade")             # tape is not quick: the enemy attacks
        self.assertEqual(S(z)["armor"]["prot"], prot + 2)

    def test_gras_cakes_stamina_and_hangover(self):
        z = new(inv=["brownie_calm"])
        z["werte"]["moral"] = 0
        zug(z, "gegenstand", "brownie_calm", parade="verfehlt")
        self.assertEqual(S(z)["koffein"][0], 1)                     # +1 stamina per round (5 rounds, one ticked)
        self.assertEqual(z["werte"]["moral"], 0)                    # eating it yourself never lifts the crew (Duc)
        self.assertEqual(z["kater_tag"], z["tag"])                  # hangover tomorrow morning

    def test_grenades_hit_through_armour_and_set_the_element(self):
        z = new(inv=["grenade_fire", "grenade_water", "grenade_shock"])
        G(z)["lp"] = G(z)["lp_max"] = S(z)["lp"] = S(z)["lp_max"] = 200   # both must survive three rounds
        lp, mx = G(z)["lp"], G(z)["lp_max"]
        zug(z, "gegenstand", "grenade_fire", parade=None)           # before the round ends (no burn tick yet)
        self.assertEqual(G(z)["lp"], lp - round(mx * 0.12))
        self.assertEqual(G(z)["states"].get("brennend"), 2)
        kampf.entdeckungen(z, T.DEFS)                               # the codex reads the grenade's hit event too (live crash 27.10.)
        self.assertTrue(any(e["art"] == "gegenstand" and e.get("granate") == "brennend" for e in z["kampf"]["events"]))
        kampf.parade_aufloesen(z, T.MODUL, "verfehlt", rng=T.NO)
        self.assertNotIn("grenade_fire", z["inventar"])
        G(z)["states"].clear()
        zug(z, "gegenstand", "grenade_water", parade="verfehlt")
        self.assertTrue(G(z)["states"].get("nass"))
        lp = G(z)["lp"]
        zug(z, "gegenstand", "grenade_shock", parade=None)
        self.assertIn("Short Circuit", " ".join(z["kampf"]["log"][-1]["zeilen"]))
        self.assertLess(G(z)["lp"], lp - round(mx * 0.12) + 1)
        self.assertNotIn("nass", G(z)["states"])

    def test_flash_and_shrapnel(self):
        z = new(inv=["grenade_flash", "grenade_shrapnel"])
        lp = G(z)["lp"]
        zug(z, "gegenstand", "grenade_flash", parade=None)
        self.assertEqual(G(z)["lp"], lp)                            # no damage, only light
        self.assertEqual(G(z)["states"].get("geblendet"), 1)
        g = {x["id"]: x for x in kampf.gegenstaende(z, T.MODUL)}
        self.assertIsNone(g["grenade_shrapnel"]["gesperrt"])
        self.assertEqual(g["grenade_shrapnel"]["zahl"], "%d dmg" % round(G(z)["lp_max"] * 0.18))
        G(z)["def"] = dict(G(z)["def"], cls="maschine")
        g = {x["id"]: x for x in kampf.gegenstaende(z, T.MODUL)}
        self.assertEqual(g["grenade_shrapnel"]["gesperrt"], "Shrapnel does nothing to a machine.")

    def test_grenades_hit_bosses_for_less_and_sit_in_rosis_shop(self):
        z = new(inv=["grenade_concussion"])
        G(z)["def"] = dict(G(z)["def"], boss=True)
        lp, mx = G(z)["lp"], G(z)["lp_max"]
        zug(z, "gegenstand", "grenade_concussion", parade=None)
        self.assertEqual(G(z)["lp"], lp - round(mx * 0.12 * kampf.BOSS_BURN))
        self.assertTrue(G(z)["states"].get("erschuettert"))
        z = new(start=False)
        kampf.progress(z).pop("test", None)                         # the test setup opens the workshop like the preview
        ids = lambda: {w["id"] for w in handel.sortiment(z, T.MODUL, "rosi") or []}
        self.assertIn("spikes", ids())                              # weapon care from the start ...
        self.assertFalse({i for i in ids() if i.startswith("grenade")})     # ... grenades only once the workshop is open
        z["flags"] = list(z.get("flags") or []) + ["werkstatt_offen"]
        self.assertTrue({"grenade_fire", "grenade_shrapnel", "grenade_flash"} <= ids())

    def test_isabelles_pharmacy_only_once_met(self):
        z = new(start=False)
        self.assertNotIn("isabelle", handel.ansicht(z, T.MODUL, None, [])["laeden"])
        self.assertIsNone(handel.sortiment(z, T.MODUL, "isabelle"))      # and nothing to buy there either
        z["bekannt"] = list(z.get("bekannt") or []) + ["isabelle"]
        self.assertIn("isabelle", handel.ansicht(z, T.MODUL, None, [])["laeden"])


if __name__ == "__main__":
    unittest.main()
