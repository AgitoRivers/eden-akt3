# -*- coding: utf-8 -*-
"""Combat rules stage 4a (24.10.2026) with fixed dice: formula and the Lv-9 example of docs\\wiki\\systeme\\kampf.md, crits,
burn stacks, reactions, "erschoepft" counting rounds, the 16 specials (gates and effects, M5 as charge skill), the 4 basic
skills, level/xp/skill points, equipment, enemy intents ("tut weh"), parade, all five ends, revision, reload.
Runs without server, language model and save games (throwaway state from modul.json).

  python tests\\test_kampf.py
"""
import copy, json, os, sys, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(HERE)
sys.path.insert(0, EDEN)
from kern import kampf, zustand  # noqa: E402

MODDIR = os.path.join(EDEN, "module", "eden_rise")
MODUL = json.load(open(os.path.join(MODDIR, "modul.json"), encoding="utf-8"))
DEFS = copy.deepcopy(kampf.daten(MODDIR))
# 26.10.2026: these are rule tests with hand-checked numbers - they keep the balance from before the Kloster balancing
# (Duc 36 LP / base 6, enemies 55/19, +25 % per level, no catch-breath, old parry windows). The new values: class Balance.
NEU = {n: getattr(kampf, n) for n in ("LP_BASE", "BASE_ATTACK", "ENEMY_LP", "ENEMY_ATK", "LEVEL_GAP", "TEMPO")}
kampf.LP_BASE, kampf.BASE_ATTACK, kampf.ENEMY_LP, kampf.ENEMY_ATK, kampf.LEVEL_GAP = 36, 6, 55, 19.0, 0.25
kampf.TEMPO = {"leicht": {"gut": 220, "perf": 90, "dauer": 1150}, "mittel": {"gut": 160, "perf": 60, "dauer": 1000},
               "stark": {"gut": 110, "perf": 40, "dauer": 850}}
# test dummy: neutral against blades (flieger, no element), so the docs example works with x1.0
DEFS["enemies"]["puppe"] = {"name": "Puppe", "sprite": "Thief", "cls": "flieger", "element": None, "tier": "toedlich",
                            "attack": {"label": "Schlag", "icon": "🗡"},
                            "specials": {"w1": {"label": "Kreischen", "icon": "📢", "bonus": 0, "effect": "buff4",
                                                "dodge_only": False},
                                         "w2": {"label": "Stoß", "icon": "🗡", "bonus": 2, "effect": None,
                                                "dodge_only": False},
                                         "s1": {"label": "Hammer", "icon": "🗡🗡", "bonus": 8, "effect": None,
                                                "dodge_only": False}},
                            "weakness": "courage", "immune": {}, "parade": "sprite"}
DEFS["encounters"]["puppe9"] = dict(copy.deepcopy(DEFS["encounters"]["hafen_dieb_test"]), enemy="puppe", level=9)
# 24.10.2026: the common weapons left the game (fixed weapons bat/knife/gun/spear/sword instead) - the mechanics tests
# keep them as test-only weapons, so their numbers stay meaningful (faust = 0 damage baseline)
for _wid, _w in {"faust": (0, None, "stumpf", 1), "taschenmesser": (1, None, "messer", 1),
                 "schraubenschluessel": (2, "erde", "stumpf", 1), "tauchermesser": (2, "wasser", "messer", 1),
                 "sportbogen": (3, "luft", "fern", 2)}.items():
    DEFS["weapons"][_wid] = {"label": _wid, "dmg": _w[0], "element": _w[1], "kind": _w[2], "slots": _w[3],
                             "rarity": "gewoehnlich", "sig": None, "price": None, "source": "test"}
# the eight story weapons and the old armors are gone too (docs\wiki\systeme\aufruestung.md); tests that need their numbers get them here
DEFS["weapons"]["rosis_flammenschwert"] = dict(DEFS["weapons"]["taschenmesser"], label="rosis", dmg=9, element="feuer",
                                               kind="klinge", sig="burn3")
DEFS["weapons"]["feuerwehraxt"] = dict(DEFS["weapons"]["taschenmesser"], label="axt", dmg=6, element="feuer", kind="klinge")
for _aid, _a in {"keine": (0, None), "feuerwehrjacke": (2, "feuer")}.items():            # "keine" = old "no armor" baseline
    DEFS["armors"][_aid] = {"label": _aid, "prot": _a[0], "resist": _a[1], "heavy": False, "bite": 0.0, "bonus": {},
                            "rarity": "gewoehnlich", "sig": None, "eigenschaft": None, "source": "test"}


class R:
    """Fixed rng: random() always v (0.99 = no crit, no current failure), randint from a list (default 10)."""
    def __init__(self, v=0.99, ints=()):
        self.v, self.ints = v, list(ints)

    def random(self):
        return self.v

    def randint(self, a, b):
        return self.ints.pop(0) if self.ints else 10


NO = R()


class Wurf:
    """probe_fn with a fixed result; remembers whether it rolled with advantage."""
    def __init__(self, ergebnis):
        self.ergebnis, self.vorteil = ergebnis, None

    def __call__(self, att, sg, boni, vorteil=False):
        self.vorteil = vorteil
        return {"attribut": att, "sg": sg, "wurf": 10, "boni": boni, "summe": 10, "ergebnis": self.ergebnis,
                "text": self.ergebnis}


def new(bid="hafen_dieb_test", level=1, skills=(), weapon=None, armor=None, attrs=None, inv=(), vorteile=None,
        start=True):
    z = zustand.neu(MODUL)
    p = copy.deepcopy(MODUL["personas"][0])
    if vorteile is not None:
        p["vorteile"] = list(vorteile)
    p["attribute"].update(attrs or {})
    zustand.persona_setzen(z, MODUL, p)
    z["inventar"] = list(inv)
    kampf.test_setup(z, DEFS, level=level, skills=kampf.by_code(DEFS, skills), weapon=weapon or "faust",
                     armor=armor or "keine")
    if start:
        kampf.starten(z, DEFS, bid, rng=NO)
    return z


def zug(z, befehl, ziel=None, parade="verfehlt", rng=NO, **kw):
    return kampf.zug(z, MODUL, befehl, ziel, parade=parade, rng=rng, **kw)


def F(z, sid, parade="verfehlt", ergebnis=None, rng=NO):
    return zug(z, "faehigkeit", sid, parade=parade, rng=rng, probe_fn=Wurf(ergebnis) if ergebnis else None)


def G(z):
    return z["kampf"]["gegner"][0]


def S(z):
    return z["kampf"]["spieler"]


def ctx(z, rng=NO):
    return kampf._ctx(z["kampf"], rng)


def set_intent(z, key):
    G(z)["absicht"] = key


class Formula(unittest.TestCase):
    def test_start_values(self):
        z = new()
        sp, g = S(z), G(z)
        self.assertEqual((sp["lp"], sp["lp_max"], sp["ausdauer"]), (36, 36, 6))
        self.assertEqual((g["lp"], g["fassung"], g["armor"], g["sg"]), (60, 14, 1, 11))   # 55 x 1.1, 12 + 2 x Lv
        self.assertEqual(g["absicht"], "n")
        self.assertEqual(g["bedrohung"]["id"], "gefaehrlich")

    def test_attack_and_enemy_hit(self):
        z = new()
        zug(z, "angriff", parade=None)
        self.assertEqual(G(z)["lp"], 53)                          # 6 + Kraft 2 + Faust 0 - Schutz 1
        self.assertEqual(z["kampf"]["phase"], "parade")
        self.assertEqual(z["kampf"]["parade"]["schaden"], 18)     # round(19.6) - Duc 2
        kampf.parade_aufloesen(z, MODUL, "verfehlt", rng=NO)
        self.assertEqual(S(z)["lp"], 18)
        self.assertEqual(z["lp"], 18)

    def test_docs_example_level9(self):
        """docs: Kraft 3, Rosis Schwert 9, 129 LP, Schutz 4 -> 14 · erschöpft 18 · K3 18 -> K9 66 · W3 -> W9 3 x 15."""
        z = new("puppe9", level=9, weapon="rosis_flammenschwert", attrs={"strength": 3})
        g, sp = G(z), S(z)
        self.assertEqual((g["lp_max"], g["armor"]), (129, 4))
        self.assertEqual(kampf.hit_preview(sp, g), 14)
        g["states"]["erschoepft"] = 2
        self.assertEqual(kampf.hit_preview(sp, g), 18)
        z = new("puppe9", level=9, weapon="rosis_flammenschwert", attrs={"strength": 3}, skills=["K3", "K9"])
        S(z)["attrs"]["strength"] = 3                              # the docs example keeps Kraft 3 (no growth)
        F(z, "mistral")
        self.assertEqual(129 - G(z)["lp"], 18)
        G(z)["lp"] = 129
        G(z)["states"]["erschoepft"] = 2
        S(z)["ausdauer"] = 8
        F(z, "lame_de_fond")
        self.assertEqual(129 - G(z)["lp"], 66)
        z = new("puppe9", level=9, weapon="rosis_flammenschwert", attrs={"strength": 3}, skills=["W3", "W9"])
        F(z, "point_de_mire")
        before = G(z)["lp"]
        c = ctx(z)
        dmg = [kampf._hit(c, kampf.W9_FACTOR, proc=True) for _ in range(3)]
        self.assertEqual(dmg, [15, 15, 15])
        self.assertEqual(before - G(z)["lp"], 45)

    def test_crit_and_knife(self):
        z = new()
        zug(z, "angriff", rng=R(0.0))
        self.assertEqual(G(z)["lp"], 60 - 11)                     # ceil(7 x 1.5)
        z = new(weapon="taschenmesser", attrs={"cunning": 4})
        self.assertAlmostEqual(kampf.crit_chance(S(z)), 0.05 + 0.12 + 0.05)
        self.assertEqual(kampf.hit_preview(S(z), G(z)), round((6 + 4 + 1) * 1.25) - 1)   # knife strikes with List
        G(z)["states"]["erschoepft"] = 2
        self.assertEqual(kampf.hit_preview(S(z), G(z)), round((6 + 4 + 1 + 5) * 1.25) - 1)

    def test_type_and_element(self):
        z = new("akt1_pirat", weapon="schraubenschluessel")       # erde vs wasser: neither beats the other
        self.assertEqual(kampf._mult(S(z)["weapon"], G(z)), 1.0)
        z = new("akt1_fackelpirat", weapon="tauchermesser")        # messer vs mensch 1.25, wasser > feuer 1.2
        self.assertAlmostEqual(kampf._mult(S(z)["weapon"], G(z)), 1.25 * 1.2)
        z = new("akt1_moewe", weapon="schraubenschluessel")        # stumpf vs flieger 0.8, erde > luft 1.2
        self.assertAlmostEqual(kampf._mult(S(z)["weapon"], G(z)), 0.8 * 1.2)

    def test_shaken_removes_protection(self):
        z = new()
        G(z)["states"]["erschuettert"] = 2
        self.assertEqual(kampf.hit_preview(S(z), G(z)), 8)

    def test_level_gap(self):
        z = new("akt1_fackelpirat")                                 # Lv 4 against Lv 1: +75 %
        self.assertEqual(G(z)["lp_max"], int(int(55 * 1.1 ** 4) * 1.75))
        self.assertEqual(G(z)["bedrohung"]["id"], "albtraum")


class Burn(unittest.TestCase):
    def test_stacks_cap_and_tick(self):
        z = new()
        c = ctx(z)
        for _ in range(7):
            kampf._apply_state(c, "brennend")
        self.assertEqual(G(z)["states"]["brennend"], 5)
        zug(z, "verteidigen")
        self.assertEqual(G(z)["lp"], 60 - int(0.03 * 60 * 5))      # new stack this round: no fading yet
        self.assertEqual(G(z)["states"]["brennend"], 5)
        zug(z, "verteidigen")
        self.assertEqual(G(z)["states"]["brennend"], 4)            # round without a new stack: -1

    def test_burn_on_duc_guard_and_jacket(self):
        z = new("akt1_fackelpirat", level=4)
        set_intent(z, "s1")
        zug(z, "angriff")
        self.assertEqual(S(z)["states"]["brennend"], 1)
        zug(z, "verteidigen")
        self.assertNotIn("brennend", S(z)["states"])
        z = new("akt1_fackelpirat", level=4, armor="feuerwehrjacke")
        set_intent(z, "s1")
        zug(z, "angriff")
        self.assertNotIn("brennend", S(z)["states"])


class Reactions(unittest.TestCase):
    def names(self, c):
        return [e["name"] for e in c["events"] if e["art"] == "reaktion"]

    def test_steam(self):
        z = new()
        c = ctx(z)
        kampf._apply_state(c, "brennend")
        kampf._apply_state(c, "brennend")
        kampf._apply_state(c, "nass")
        self.assertEqual(self.names(c), ["Steam"])
        self.assertNotIn("brennend", G(z)["states"])
        self.assertTrue(G(z)["states"]["geblendet"])

    def test_short_circuit(self):
        z = new()
        c = ctx(z)
        kampf._apply_state(c, "nass")
        kampf._apply_state(c, "strom")
        self.assertEqual(self.names(c), ["Short Circuit"])
        self.assertEqual(G(z)["lp"], 60 - int(0.08 * 60))
        self.assertEqual(G(z)["states"]["skip"], 1)

    def test_short_circuit_on_duc(self):                           # water grenade + taser at the ridge (28.10.)
        z = new()
        c = ctx(z)
        sp = S(z)
        lp = sp["lp"]
        kampf._duc_state(c, "nass", 3)
        kampf._duc_state(c, "strom", 2)
        self.assertEqual(self.names(c), ["Short Circuit"])
        self.assertEqual(sp["lp"], lp - int(0.08 * sp["lp_max"]))
        self.assertNotIn("nass", sp["states"])
        self.assertNotIn("strom", sp["states"])
        self.assertTrue(kampf.must_skip(sp))

    def test_burst_sparks_mud(self):
        z = new()
        c = ctx(z)
        kampf._apply_state(c, "blutend")                           # 3 rounds
        kampf._apply_state(c, "brennend")
        self.assertEqual(G(z)["lp"], 60 - 3 * 3)                   # 5 % of 60 = 3, x 3 rounds
        self.assertNotIn("blutend", G(z)["states"])
        kampf._apply_state(c, "strom")
        self.assertEqual(G(z)["states"]["brennend"], 2)
        kampf._apply_state(c, "nass")                              # current + wet: short circuit (burn stays)
        kampf._apply_state(c, "nass")                              # wet on burning: steam
        kampf._apply_state(c, "nass")
        kampf._apply_state(c, "erschuettert")
        self.assertEqual(self.names(c), ["Burst", "Sparks", "Short Circuit", "Steam", "Mud"])
        self.assertTrue(kampf.exhausted(G(z)))

    def test_machines_do_not_bleed(self):
        z = new()
        G(z)["def"]["cls"] = "maschine"
        kampf._apply_state(ctx(z), "blutend")
        self.assertNotIn("blutend", G(z)["states"])


class Exhausted(unittest.TestCase):
    def test_counts_rounds_not_hits(self):
        z = new(skills=["L3"])
        G(z)["states"]["erschoepft"] = 2
        F(z, "doppio_gioco")
        self.assertEqual(60 - G(z)["lp"], 2 * (round(12 * 0.7) - 1))   # both cuts with +4
        self.assertEqual(G(z)["states"].get("erschoepft"), 1)

    def test_heavy_special_exhausts(self):
        z = new("akt1_fackelpirat")
        set_intent(z, "s1")
        zug(z, "verteidigen")
        self.assertTrue(kampf.exhausted(G(z)))


class Healer(unittest.TestCase):
    """Fifth path H (Empathy, Duc + Brain Trust 26.10.2026)."""
    def test_elicriso_heals_and_soothes(self):
        z = new("puppe9", level=9, skills=["H3"])
        sp = S(z)
        sp["lp"] = 10
        sp["states"]["brennend"] = 2
        F(z, "elicriso")
        self.assertNotIn("brennend", S(z)["states"])
        self.assertTrue(any("You heal" in l for e in z["kampf"]["log"] for l in e["zeilen"]))

    def test_ponente_heals_each_round_and_widens_parry(self):
        z = new(skills=["H3", "H5"])
        sp = S(z)
        sp["lp"] = 5
        F(z, "ponente", parade="perfekt")
        self.assertEqual(S(z)["ponente"], kampf.H5_ROUNDS - 1)
        self.assertEqual(S(z)["lp"], 5 + round(S(z)["lp_max"] * kampf.H5_HEAL))
        self.assertIn("still blowing", kampf.skill_info(z, z["kampf"], "ponente")["gesperrt"])

    def test_risveglio_once_per_fight(self):
        z = new(skills=["H3", "H5", "H7"], level=9)
        S(z)["lp"], S(z)["ausdauer"] = 5, 8
        F(z, "risveglio", parade="perfekt")
        self.assertGreaterEqual(S(z)["lp"], 5 + int(S(z)["lp_max"] * kampf.H7_HEAL) - 1)
        S(z)["ausdauer"] = 8
        self.assertIn("once per fight", kampf.skill_info(z, z["kampf"], "risveglio")["gesperrt"].lower())

    def test_arcangelo_rises_once(self):
        z = new("puppe9", level=9, skills=["H3", "H5", "H7", "H9"])
        S(z)["ausdauer"] = 8
        set_intent(z, "s1")
        S(z)["lp"] = 1
        F(z, "arcangelo")                                          # the hammer would kill him - he rises again
        self.assertIsNone(z["kampf"].get("ergebnis"))
        self.assertEqual(S(z)["lp"], round(S(z)["lp_max"] * kampf.H9_LP))
        self.assertFalse(S(z).get("arcangelo"))
        self.assertIn("once per fight", kampf.skill_info(z, z["kampf"], "arcangelo")["gesperrt"].lower())

    def test_nonna_teaches_elicriso(self):
        z = new(start=False)
        zustand.folgen_anwenden(z, MODUL, [{"beibringen": "elicriso"}])
        self.assertIn("elicriso", kampf.known(z))
        self.assertEqual(kampf.progress(z)["skills"], [])          # taught, no skill point

    def test_healer_path_in_profile(self):
        z = new(skills=["H3"], start=False)
        p = kampf.profil(z, DEFS)
        self.assertIn("H", [x["id"] for x in p["pfade"]])
        self.assertEqual(kampf.main_path(DEFS, ["elicriso"]), "H")


class Specials(unittest.TestCase):
    def test_answer_gate_and_hint(self):
        z = new(skills=["K3", "K5"])
        info = kampf.skill_info(z, z["kampf"], "ressac")
        self.assertIn("answer", info["gesperrt"])
        set_intent(z, "w1")
        self.assertIsNone(kampf.skill_info(z, z["kampf"], "ressac")["gesperrt"])
        z = new("maxwell_training", skills=["K3", "K5"])
        set_intent(z, "w1")                                         # buff: does not hurt
        self.assertIn("won't hurt", kampf.skill_info(z, z["kampf"], "ressac")["hinweis"])

    def test_finisher_gate(self):
        z = new(skills=["L3", "L5", "L7", "L9"])
        self.assertIn("exhausted", kampf.skill_info(z, z["kampf"], "omerta")["gesperrt"])
        G(z)["states"]["blutend"] = 2
        self.assertIsNone(kampf.skill_info(z, z["kampf"], "omerta")["gesperrt"])

    def test_ressac_wet_double_and_weaken(self):
        z = new("puppe9", level=9, skills=["K3", "K5"])
        set_intent(z, "s1")
        G(z)["states"]["nass"] = 2
        sp, g = S(z), G(z)
        expect = max(1, round(kampf.raw_hit(sp, g) * kampf._mult(sp["weapon"], g) * 2.0) - 4)
        F(z, "ressac", parade=None)
        self.assertEqual(G(z)["lp_max"] - G(z)["lp"], expect)
        self.assertTrue(G(z)["states"].get("geschwaecht"))
        weakened = z["kampf"]["parade"]["schaden"]
        self.assertEqual(weakened, kampf.incoming(S(z), G(z), "s1"))
        kampf.parade_aufloesen(z, MODUL, "verfehlt", rng=NO)
        self.assertFalse(G(z)["states"].get("geschwaecht"))         # used up by his attack

    def test_libeccio_halves_and_shakes(self):
        z = new(skills=["K3", "K5", "K7"])
        F(z, "libeccio")
        self.assertEqual(S(z)["lp"], 36 - 9)                        # 18 halved
        F(z, "mistral", parade="perfekt")                           # wind round 2: perfect parade shakes
        self.assertTrue(G(z)["states"].get("erschuettert"))

    def test_sotto_voce_sure_crit(self):
        z = new(skills=["L3", "L5"])
        set_intent(z, "w1")
        F(z, "sotto_voce")
        self.assertTrue(S(z)["sure_crit"])
        before = G(z)["lp"]
        zug(z, "angriff")
        self.assertEqual(before - G(z)["lp"], 11)

    def test_vendetta_and_omerta(self):
        z = new(skills=["L3", "L5", "L7", "L9"], level=9)
        F(z, "vendetta")
        self.assertEqual(G(z)["states"]["blutend"], 2)              # 3 rounds, one ticked
        before = G(z)["lp"]
        sp, g = S(z), G(z)
        n = kampf.n_states(g)
        plain = max(1, round(kampf.raw_hit(sp, g) * kampf._mult(sp["weapon"], g) * (1 + 0.25 * n)) - g["armor"])
        S(z)["ausdauer"] = 8
        F(z, "omerta")
        self.assertEqual(before - G(z)["lp"], int(-(-plain * 2.5 // 1)) + int(0.05 * 60))   # + bleed tick

    def test_point_de_mire_scaling(self):
        z = new(skills=["W3"], attrs={"perception": 3})             # Lv 1: perception stays 3 -> until next turn
        F(z, "point_de_mire")
        self.assertEqual(G(z)["states"]["erschoepft"], 1)
        z = new(skills=["W3"], attrs={"perception": 4})
        F(z, "point_de_mire")
        self.assertEqual(G(z)["states"]["erschoepft"], 2)

    def test_bonaccia(self):
        z = new("puppe9", level=9, skills=["W3", "W5"], attrs={"perception": 5})
        set_intent(z, "s1")
        F(z, "bonaccia")
        self.assertEqual(S(z)["lp"], S(z)["lp_max"])                # perception 5: fully blocked
        self.assertLess(G(z)["lp"], G(z)["lp_max"])                 # ... and strikes back
        z = new(skills=["W3", "W5"], attrs={"perception": 3})
        set_intent(z, "w1")
        F(z, "bonaccia")
        self.assertEqual(S(z)["lp"], 36 - 10)                       # (20 + 2 - 2) halved, no counter below 4
        self.assertEqual(G(z)["lp"], 60)

    def test_phare(self):
        z = new("puppe9", level=9, skills=["W3", "W5", "W7"], attrs={"perception": 5})
        set_intent(z, "w2")
        self.assertIn("strong", kampf.skill_info(z, z["kampf"], "phare")["gesperrt"])
        set_intent(z, "s1")
        F(z, "phare")
        self.assertEqual(S(z)["lp"], S(z)["lp_max"])                # he skipped
        self.assertIn("skips", " ".join(z["kampf"]["log"][-1]["zeilen"]))

    def test_scirocco_and_furia(self):
        z = new(skills=["M3", "M5", "M7"], level=7)
        F(z, "scirocco", parade=None)
        self.assertEqual(G(z)["states"]["brennend"], 1)
        self.assertTrue(S(z)["states"]["ungedeckt"])
        self.assertEqual(z["kampf"]["parade"]["schaden"], kampf.incoming(S(z), G(z), "n"))
        kampf.parade_aufloesen(z, MODUL, "verfehlt", rng=NO)
        self.assertNotIn("ungedeckt", S(z)["states"])
        S(z)["ausdauer"] = 7
        F(z, "furia")
        self.assertEqual(S(z)["states"]["brennend"], 1)             # Duc caught fire this round: no fading yet
        self.assertEqual(G(z)["states"]["brennend"], 2)             # Scirocco stack + Furia hit stack
        self.assertIn("Furia", kampf.pruefen(z, MODUL, "verteidigen"))

    def test_retour_charge(self):
        for erg, f, burn in (("gut", 1.5, 1), ("verfehlt", 0.5, 0)):
            z = new(skills=["M3", "M5"], level=5)
            F(z, "retour", parade=None)
            self.assertTrue(z["kampf"]["parade"]["aufgeladen"])
            sp, g = S(z), G(z)
            expect = max(1, round(kampf.raw_hit(sp, g) * f) - 1)
            kampf.parade_aufloesen(z, MODUL, erg, rng=NO)
            self.assertEqual(60 - G(z)["lp"] - (int(0.03 * 60) if burn else 0), expect)
            self.assertEqual(G(z)["states"].get("brennend", 0), burn)
            self.assertFalse(S(z).get("charged"))

    def test_retour_strong_and_no_double_counter(self):
        z = new("akt1_fackelpirat", skills=["M3", "M5"], level=5)
        set_intent(z, "s1")
        F(z, "retour", parade=None)
        sp, g = S(z), G(z)
        expect = max(1, round(kampf.raw_hit(sp, g) * kampf._mult(sp["weapon"], g) * 2.0) - g["armor"])
        before = g["lp"]
        kampf.parade_aufloesen(z, MODUL, "perfekt", rng=NO)
        dealt = before - G(z)["lp"] - int(0.03 * G(z)["lp_max"])     # minus the burn tick
        self.assertEqual(dealt, expect)                              # only the charged counter, x2

    def test_vulcano(self):
        z = new(skills=["M3", "M5", "M7", "M9"], level=9)
        self.assertIn("aren't burning", kampf.skill_info(z, z["kampf"], "vulcano")["gesperrt"])
        c = ctx(z)
        for _ in range(5):
            kampf._apply_state(c, "brennend")
        sp, g = S(z), G(z)
        one = max(1, round(kampf.raw_hit(sp, g) * kampf._mult(sp["weapon"], g) * 0.6))
        F(z, "vulcano")
        self.assertEqual(60 - G(z)["lp"], 5 * one)
        self.assertNotIn("brennend", G(z)["states"])
        self.assertTrue(kampf.must_skip(S(z)))
        self.assertEqual([b["id"] for b in kampf.befehle(z, MODUL)], ["aussetzen"])
        zug(z, "aussetzen")
        self.assertFalse(kampf.must_skip(S(z)))


class Basic(unittest.TestCase):
    def test_basic_skills(self):
        z = new()                                                    # 29.10.2026: Spot Weakness removed
        self.assertEqual([f["id"] for f in kampf.faehigkeiten(z)], ["reden", "einschuechtern"])

    def test_taught_special(self):
        # 26.10.2026: Maxwell teaches Mistral - usable, no skill point, no main path, counts for the next tier
        z = new()
        kampf.beibringen(z, "mistral")
        c = kampf.progress(z)
        self.assertEqual(c["skills"], [])
        self.assertEqual(kampf.free_points(z), kampf.skill_points(c["level"]))
        self.assertEqual(kampf.learn_reason(z, DEFS, "mistral"),
                         "Already learned.")

    def test_talk_on_weakness_with_advantage(self):
        z = new()
        w = Wurf("erfolg")
        zug(z, "faehigkeit", "reden", probe_fn=w)
        self.assertTrue(w.vorteil)
        self.assertEqual(G(z)["fassung"], 14 - 10)                  # 6 + weakness 4
        self.assertTrue(kampf.exhausted(G(z)))

    def test_animals_do_not_talk_but_fear(self):
        z = new("akt1_ratte")
        self.assertIn("Animals", kampf.skill_info(z, z["kampf"], "reden")["gesperrt"])
        F(z, "einschuechtern", ergebnis="kritisch")
        self.assertEqual(G(z)["fassung"], 14 - 10)                  # crit 6 + weakness 4

    def test_fumble_exposes(self):
        z = new()
        F(z, "einschuechtern", ergebnis="patzer", parade=None)
        self.assertEqual(z["kampf"]["parade"]["schaden"], 18 + 3)

    def test_koepfchen_sees_weakness_and_crit_range(self):
        self.assertTrue(G(new(vorteile=["koepfchen"]))["schwaeche_bekannt"])     # 29.10.2026: instead of Spot Weakness
        self.assertFalse(G(new(vorteile=[]))["schwaeche_bekannt"])
        self.assertEqual(kampf.crit_from({"cunning": 2}), 19)
        self.assertEqual(kampf.chance(0, 30, krit_ab=19), 10)

    def test_real_dice_crit_range(self):
        z = new(attrs={"cunning": 4})                              # crit from 18
        zug(z, "faehigkeit", "einschuechtern", rng=R(0.99, [18]))
        self.assertEqual(z["kampf"]["letzte_probe"]["ergebnis"], "kritisch")


class Progress(unittest.TestCase):
    def test_xp_curve_and_threat(self):
        self.assertEqual(kampf.xp_for(1, 1), 20)
        self.assertEqual(kampf.xp_for(2, 1), 60)                    # orange x1.5
        self.assertEqual(kampf.xp_for(5, 3), 200)                   # skull x2
        self.assertEqual(kampf.xp_for(1, 3), 10)                    # grey x0.5

    def test_level_up_points_lp(self):
        z = new(start=False)
        z["lp"] = 30
        lines = kampf.award_xp(z, 60 + 120 + 1)
        self.assertEqual(kampf.progress(z)["level"], 3)
        self.assertEqual(kampf.progress(z)["xp"], 1)
        self.assertEqual(z["lp"], 40)
        self.assertEqual(kampf.free_points(z), 1)
        self.assertIn("Level 3! +1 attribute point · +1 skill point", lines)
        self.assertEqual(kampf.progress(z)["attributpunkte"], 2)               # one per level (26.10.2026)
        self.assertEqual([kampf.skill_points(lv) for lv in (2, 3, 5, 7, 9, 10)], [0, 1, 2, 3, 4, 6])

    def test_attribute_points(self):
        z = new(start=False)
        c = kampf.progress(z)
        with self.assertRaises(ValueError):
            kampf.attribut_steigern(z, "strength")                  # no point yet
        c["attributpunkte"] = 4
        vorher = kampf.attributes(z, DEFS)["perception"]
        kampf.attribut_steigern(z, "perception")
        self.assertEqual(kampf.attributes(z, DEFS)["perception"], vorher + 1)
        self.assertEqual(c["attributpunkte"], 3)
        z["persona"]["attribute"]["courage"] = 5
        with self.assertRaises(ValueError):
            kampf.attribut_steigern(z, "courage")                   # max 5
        with self.assertRaises(ValueError):
            kampf.attribut_steigern(z, "luck")
        self.assertEqual(kampf.profil(z, DEFS)["attributpunkte"], 3)

    def test_old_save_gets_path_growth_as_points(self):
        z = new(start=False, level=9, skills=["K3", "M3", "M5"])
        c = kampf.progress(z)
        c.pop("attributpunkte")
        self.assertEqual(kampf.progress(z)["attributpunkte"], 3)    # min(5, 2 + 9 // 2) - 2

    def test_learn_needs_tier_below(self):
        z = new(start=False, level=5)
        self.assertIn("M3", kampf.learn_reason(z, DEFS, "retour"))
        kampf.lernen(z, DEFS, "scirocco")
        kampf.lernen(z, DEFS, "retour")
        self.assertEqual(kampf.learn_reason(z, DEFS, "mistral"), "No free skill point.")

    def test_main_path_and_stamina(self):
        # 26.10.2026: the main path no longer raises its attribute - the player spends attribute points instead
        z = new(start=False, level=9, skills=["K3", "M3", "M5"])
        self.assertEqual(kampf.main_path(DEFS, kampf.progress(z)["skills"]), "M")
        self.assertEqual(kampf.attributes(z, DEFS)["courage"], 2)
        self.assertEqual(kampf.attributes(z, DEFS)["strength"], 2)
        self.assertEqual((kampf.max_lp(9), kampf.max_stamina(9), kampf.max_stamina(5)), (76, 8, 7))
        self.assertEqual(kampf.main_path(DEFS, kampf.by_code(DEFS, ["K3", "M3"])), "M")    # tie: M first

    def test_equipment_needs_ownership(self):
        z = new(start=False)
        kampf.progress(z)["test"] = False
        with self.assertRaises(ValueError):
            kampf.ausruesten(z, DEFS, "weapon", "feuerwehraxt")                   # not owned
        kampf.freischalten(z, DEFS, "weapon", "feuerwehraxt")
        kampf.ausruesten(z, DEFS, "weapon", "feuerwehraxt")
        self.assertEqual(kampf.equipment(z)["weapon"], "feuerwehraxt")
        with self.assertRaises(ValueError):                                        # the jacket cannot be taken off
            kampf.ausruesten(z, DEFS, "armor", None)
        with self.assertRaises(ValueError):                                        # Citadelle is not owned yet
            kampf.ausruesten(z, DEFS, "armor", "cyber_armor")
        kampf.freischalten(z, DEFS, "armor", "cyber_armor")
        kampf.ausruesten(z, DEFS, "armor", "cyber_armor")
        self.assertEqual(kampf.equipment(z)["armor"], "cyber_armor")

    def test_training_uses_mop(self):
        z = new("maxwell_training")                                               # Maxwell hands out the scrubber
        self.assertEqual(S(z)["weapon"]["id"], "mop")
        self.assertTrue(DEFS["weapons"]["mop"].get("training_only"))

    def test_start_weapon_replaces_faust(self):
        live = kampf.daten(MODDIR)                                                 # without the test weapons
        self.assertEqual(kampf.equipment({})["weapon"], kampf.START_WEAPON)       # new game
        z = {"equipment": {"weapon": "faust", "armor": None}, "inventar": []}     # old save
        self.assertEqual(kampf._weapon_id(z["equipment"], live), kampf.START_WEAPON)
        with self.assertRaises(ValueError):                                        # weapon slot is never empty
            kampf.ausruesten(z, DEFS, "weapon", None)
        z["equipment"]["weapon"] = "piratensaebel"                                 # weapon removed from the game
        self.assertEqual(kampf._weapon_id(z["equipment"], live), kampf.START_WEAPON)
        self.assertEqual(kampf._armor_id({"armor": "lederjacke"}, live), kampf.START_ARMOR)   # old armor -> Terra Scura
        self.assertEqual(kampf.equipment({})["armor"], kampf.START_ARMOR)

    def test_xp_on_win_and_training_keeps_lp(self):
        z = new()
        G(z)["lp"] = 1
        zug(z, "angriff")
        self.assertEqual(z["kampf"]["ergebnis"]["xp"], 20)
        z = new("maxwell_training")
        zug(z, "angriff")
        G(z)["lp"] = 1
        zug(z, "angriff")
        self.assertEqual(z["kampf"]["ergebnis"]["art"], "ko")
        self.assertEqual(z["kampf"]["ergebnis"]["xp"], 5)           # 20 x 1 x 0.25
        self.assertEqual(z["lp"], 36)


class Ends(unittest.TestCase):
    def test_surrender_escape_flee_defeat(self):
        z = new()
        G(z)["fassung"] = 4
        F(z, "reden", ergebnis="erfolg")
        self.assertEqual(z["kampf"]["ergebnis"]["art"], "aufgabe")
        z = new()
        G(z)["lp"] = 15                                             # flee_at 25 % of 60
        zug(z, "verteidigen")
        self.assertEqual(G(z)["absicht"], "flucht")
        zug(z, "verteidigen")
        self.assertEqual(z["kampf"]["ergebnis"]["art"], "entkommen")
        z = new()
        zug(z, "fliehen", probe_fn=Wurf("erfolg"))
        self.assertEqual(z["kampf"]["ergebnis"]["art"], "flucht")
        z = new()
        zug(z, "fliehen", probe_fn=Wurf("fehlschlag"))
        self.assertIsNone(z["kampf"]["ergebnis"])
        self.assertEqual(S(z)["lp"], 18)
        z = new()
        S(z)["lp"] = 5
        zug(z, "verteidigen")
        self.assertEqual(z["kampf"]["ergebnis"]["art"], "niederlage")
        self.assertEqual(z["lp"], 12)

    def test_flee_not_allowed(self):
        z = new("akt1_pirat")
        self.assertIn("yacht", kampf.pruefen(z, MODUL, "fliehen"))

    def test_folgen_once_and_close(self):
        z = new()
        G(z)["lp"] = 1
        zug(z, "angriff")
        self.assertIn("kampftest_tasche_zurueck", z["flags"])
        self.assertIsNone(kampf.schliessen(z))
        self.assertIsNone(z["kampf"])


class Flow(unittest.TestCase):
    def test_invalid_changes_nothing_and_revision(self):
        z = new()
        before = copy.deepcopy(z["kampf"])
        with self.assertRaises(ValueError):
            zug(z, "faehigkeit", "mistral")
        self.assertEqual(z["kampf"], before)
        rev = z["kampf"]["revision"]
        zug(z, "angriff", parade=None, revision=rev)
        with self.assertRaises(ValueError):
            zug(z, "angriff", revision=rev)

    def test_reload_mid_fight(self):
        z = new()
        zug(z, "angriff", parade=None)
        z2 = json.loads(json.dumps(z))
        kampf.parade_aufloesen(z2, MODUL, "gut", rng=NO)
        self.assertEqual(z2["kampf"]["spieler"]["lp"], 36 - 9)

    def test_parade_results(self):
        z = new()
        zug(z, "verteidigen", parade="gut")
        self.assertEqual(S(z)["lp"], 36 - 4)                        # 18 guarded 9, parried 4
        z = new()
        zug(z, "verteidigen", parade="perfekt")
        self.assertEqual(S(z)["lp"], 36)
        self.assertEqual(G(z)["lp"], 60 - 7)
        self.assertTrue(kampf.exhausted(G(z)))
        z = new("akt1_moewe")
        set_intent(z, "w1")
        zug(z, "verteidigen", parade=None)
        self.assertEqual(z["kampf"]["parade"]["modus"], "ring")
        with self.assertRaises(ValueError):
            kampf.parade_aufloesen(z, MODUL, "perfekt", rng=NO)
        kampf.parade_aufloesen(z, MODUL, "ausweichen", rng=NO)
        z = new()
        with self.assertRaises(ValueError):
            zug(z, "angriff", parade="wuerfeln")

    def test_series_breaks_composure(self):
        z = new()
        for _ in range(3):
            zug(z, "verteidigen", parade="perfekt")
        self.assertEqual(G(z)["fassung"], 14 - 4)

    def test_parade_window(self):
        z = new(skills=["M3"])
        zug(z, "verteidigen", parade=None)
        self.assertEqual(z["kampf"]["parade"]["fenster"]["faktor"], round(1.09 * 1.5 * 0.9, 2))

    def test_intents_hurt_flag(self):
        z = new("maxwell_training")
        v = kampf.zugfolge(z["kampf"], 4)
        self.assertEqual([x["id"] for x in v], ["n", "w1", "n", "s1"])
        self.assertFalse(v[1]["tut_weh"])
        self.assertIsNone(v[1]["schaden"])
        self.assertTrue(v[3]["tut_weh"] and v[3]["stark"])
        zug(z, "verteidigen")
        zug(z, "verteidigen")                                       # buff: no parade, round ends
        self.assertEqual(G(z)["states"]["buff"], 1)

    def test_strom_on_duc_can_waste_turn(self):
        z = new()
        S(z)["states"]["strom"] = 2
        zug(z, "angriff", rng=R(0.1))
        self.assertEqual(G(z)["lp"], 60)

    def test_ranged_first_strike(self):
        z = new(weapon="sportbogen")
        self.assertLess(G(z)["lp"], 60)
        self.assertEqual(z["kampf"]["log"][0]["befehl"], "erstschlag")

    def test_items(self):
        z = new(inv=["verbandskasten"])
        S(z)["lp"] = 10
        zug(z, "gegenstand", "verbandskasten")
        self.assertNotIn("verbandskasten", z["inventar"])
        self.assertEqual(S(z)["lp"], 10 + 14 - 18)                  # 27.10.2026: 40 % of 36 LP instead of 12

    def test_view(self):
        z = new(skills=["K3"])
        v = kampf.ansicht(z, MODUL, lambda s, p: "/kampfbild/%s/%s.webp" % (s, p))
        self.assertEqual(v["gegner"][0]["bilder"]["idle"], "/kampfbild/Thief/idle.webp")
        self.assertEqual(v["spieler"]["angriff"], 7)
        self.assertIn("mistral", [f["id"] for f in v["faehigkeiten"]])
        self.assertFalse(v["gegner"][0]["absicht"]["sa"])
        kampf._apply_state(ctx(z), "brennend")
        v = kampf.ansicht(z, MODUL)
        self.assertEqual(v["gegner"][0]["brand"], 1)
        self.assertIn({"id": "brennend", "label": "burning", "wert": 1}, v["gegner"][0]["zustaende"])


class Jackets(unittest.TestCase):
    """The five jackets (docs\\wiki\\systeme\\aufruestung.md): every one has a signature that changes the fight."""

    def test_five_jackets_exist(self):
        live = kampf.daten(MODDIR)
        self.assertEqual(sorted(live["armors"]), ["cyber_armor", "jacket_air", "jacket_earth", "jacket_fire", "jacket_water"])
        self.assertEqual(sorted(w for w, d in live["weapons"].items() if not d.get("training_only")),
                         ["bat", "gun", "knife", "spear", "sword"])
        self.assertEqual(live["start_armor"], "jacket_earth")

    def test_terra_standfest(self):
        z = new(armor="jacket_earth")
        c = ctx(z)
        kampf._duc_state(c, "erschuettert", 2)
        self.assertNotIn("erschuettert", S(z)["states"])                      # never shaken
        S(z)["states"]["erschuettert"] = 2                                    # even if shaken, the armor still counts
        it = G(z)["intents"]["n"]
        shaken = kampf._enemy_damage(S(z), G(z), "n", it)[0]
        S(z)["states"].pop("erschuettert")
        self.assertEqual(shaken, kampf._enemy_damage(S(z), G(z), "n", it)[0])
        plain = kampf._enemy_damage(S(z), G(z), "n", it)[0]
        S(z)["states"]["guard"] = 1
        self.assertLess(kampf._enemy_damage(S(z), G(z), "n", it)[0], plain)  # guard: +2 armor and half damage

    def test_meramie_fliessend(self):
        z1, z2 = new(armor="keine"), new(armor="jacket_water")
        w1 = kampf._parade_data(ctx(z1), "n", G(z1)["intents"]["n"])["fenster"]["faktor"]
        w2 = kampf._parade_data(ctx(z2), "n", G(z2)["intents"]["n"])["fenster"]["faktor"]
        self.assertAlmostEqual(w2 / w1, 1.05, places=1)

    def test_incendio_glut(self):
        def dealt(armor):
            z = new("akt1_pirat", armor=armor)
            G(z)["states"]["brennend"] = 3
            before = G(z)["lp"]
            kampf._hit(ctx(z))
            return before - G(z)["lp"]
        self.assertEqual(dealt("jacket_fire") - dealt("keine"), 6)            # +2 per burn stack

    def test_zephyr_leicht(self):
        z = new(armor="jacket_air")
        self.assertEqual((S(z)["ausdauer"], S(z)["ausdauer_max"]), (8, 8))
        z0 = new(armor="keine")
        self.assertEqual(S(z0)["ausdauer"], 6)

    def test_citadelle_alles(self):
        z = new("akt1_fackelpirat", level=4, armor="cyber_armor")
        set_intent(z, "n")
        first = None
        for n in range(2):
            lp0 = S(z)["lp"]
            zug(z, "angriff", parade=None)
            kampf.parade_aufloesen(z, MODUL, "verfehlt", rng=NO)
            d = lp0 - S(z)["lp"]
            if n == 0:
                first = d
        self.assertLess(first, d)                                             # first hit counts half, the second does not
        info = kampf._enemy_damage(S(z), G(z), "n", G(z)["intents"]["n"])
        self.assertIn("resistance", info[1])                                  # fire enemy, "alle" resists every element


class Workshop(unittest.TestCase):
    """Rosi's workshop: closed until the repair event sets the flag, one piece per night, +1 per upgrade."""

    def setUp(self):
        self.z = new(start=False)
        kampf.progress(self.z)["test"] = False                              # live rules, not the preview switch
        self.z["konto"], self.z["inventar"] = 500, ["aquamarin"]               # Riposte's first upgrade stone
        kampf.freischalten(self.z, DEFS, "weapon", "bat")                    # Duc starts with Terra Scura only; Terremoto from Rosi
        kampf.freischalten(self.z, DEFS, "weapon", "sword")
        kampf.freischalten(self.z, DEFS, "armor", "jacket_water")

    def test_closed_until_event(self):
        with self.assertRaisesRegex(ValueError, "wrecked"):
            kampf.abgeben(self.z, DEFS, "weapon", "sword")
        self.assertFalse(kampf.profil(self.z, DEFS)["werkstatt"]["offen"])

    def test_upgrade_overnight(self):
        z = self.z
        z["flags"].append("werkstatt_offen")
        kampf.ausruesten(z, DEFS, "weapon", "bat")
        with self.assertRaisesRegex(ValueError, "wearing"):                  # the equipped piece stays with Duc
            kampf.abgeben(z, DEFS, "weapon", "bat")
        kampf.abgeben(z, DEFS, "weapon", "sword")
        self.assertEqual((z["konto"], z["inventar"]), (500 - DEFS["werkstatt"]["stufen"][0]["geld"], []))   # money + the stone paid, the stone is gone
        with self.assertRaisesRegex(ValueError, "One piece a night"):
            kampf.abgeben(z, DEFS, "armor", "jacket_water")
        with self.assertRaisesRegex(ValueError, "workshop"):               # not wearable while Rosi has it
            kampf.ausruesten(z, DEFS, "weapon", "sword")
        self.assertEqual(kampf.stufe_von(z, "weapon", "sword"), 0)
        done = kampf.werkstatt_morgen(z, DEFS)
        self.assertEqual((done["id"], done["stufe"]), ("sword", 1))
        self.assertEqual(done["text"], DEFS["werkstatt"]["texte"]["sword"][0])
        self.assertIsNone(kampf.werkstatt_morgen(z, DEFS))                  # only once
        kampf.ausruesten(z, DEFS, "weapon", "sword")
        self.assertEqual(kampf.profil(z, DEFS)["waffe"]["schaden"], 6)      # Riposte 5 + 1
        kampf.test_setup(z, DEFS, level=1)
        kampf.progress(z)["test"] = False
        kampf.starten(z, DEFS, "akt1_pirat", rng=NO)
        self.assertEqual(S(z)["weapon"]["dmg"], 6)

    def test_second_upgrade_needs_plaque_and_money(self):
        z = self.z
        z["flags"].append("werkstatt_offen")
        kampf.werkstatt(z)["stufen"]["armor:jacket_water"] = 1
        with self.assertRaisesRegex(ValueError, "Titanium"):
            kampf.abgeben(z, DEFS, "armor", "jacket_water")
        z["inventar"] = ["titanium_plate"]
        preis = DEFS["werkstatt"]["stufen"][1]["geld"]
        z["konto"] = preis - 40
        with self.assertRaisesRegex(ValueError, "40 €"):
            kampf.abgeben(z, DEFS, "armor", "jacket_water")
        z["konto"] = preis
        kampf.abgeben(z, DEFS, "armor", "jacket_water")
        kampf.werkstatt_morgen(z, DEFS)
        self.assertEqual(kampf.stufe_von(z, "armor", "jacket_water"), 2)
        with self.assertRaisesRegex(ValueError, "any further"):
            kampf.abgeben(z, DEFS, "armor", "jacket_water")

    def test_every_piece_has_texts(self):
        w = kampf.daten(MODDIR)["werkstatt"]
        for gid in list(DEFS["weapons"]) + list(DEFS["armors"]):
            d = DEFS["weapons"].get(gid, DEFS["armors"].get(gid))
            if d.get("source") != "test" and not d.get("training_only"):             # the mop is never upgraded
                self.assertEqual(len(w["texte"][gid]), 2, gid)


class StartGear(unittest.TestCase):
    def test_elements_and_start(self):
        live = kampf.daten(MODDIR)
        self.assertEqual({w: d["element"] for w, d in live["weapons"].items() if not d.get("training_only")},
                         {"sword": "wasser", "bat": "erde", "knife": "luft", "spear": "feuer", "gun": None})
        z = {"flags": []}
        own = kampf.besitz(z, live)
        self.assertEqual((own["weapons"], own["armors"]), ([], ["jacket_earth"]))      # Terremoto comes from Rosi (flag waffe_bat)
        self.assertEqual(kampf.aktive_waffe(z, live), "mop")                           # fights before that: the deck scrubber
        z["flags"].append("waffe_bat")
        self.assertEqual(kampf.aktive_waffe(z, live), "bat")
        z["flags"].remove("waffe_bat")
        with self.assertRaises(ValueError):                                    # spear not yet given
            kampf.ausruesten(z, live, "weapon", "spear")
        z["flags"].append("waffe_spear")                                       # Casanova's gift sets this flag
        kampf.ausruesten(z, live, "weapon", "spear")
        self.assertEqual(kampf.equipment(z)["weapon"], "spear")


class Discoveries(unittest.TestCase):
    """Nothing is announced beforehand; what a hit shows is written to the codex once (25.10.2026)."""

    def test_element_hit_feedback_and_codex(self):
        z = new("akt1_ratte", weapon="spear")
        c = ctx(z)
        kampf._hit(c)
        t = [e for e in c["events"] if e["art"] == "treffer"][0]
        self.assertEqual((t["wirkung"], t["tags"]), ("stark", ["elem:feuer>erde"]))     # fire beats earth (rat)
        z["kampf"]["events"] = c["events"]
        neu = kampf.entdeckungen(z, DEFS)
        self.assertEqual(neu, ["Combat: Fire beats Earth."])
        self.assertIn("Combat: Fire beats Earth.", z["codex"])
        z["kampf"]["events"] = c["events"]
        self.assertEqual(kampf.entdeckungen(z, DEFS), [])                              # only the first time

    def test_neutral_hit_has_no_effect_text(self):
        z = new("akt1_ratte", weapon="faust")
        c = ctx(z)
        kampf._hit(c)
        t = [e for e in c["events"] if e["art"] == "treffer"][0]
        self.assertIsNone(t["wirkung"])


class Twin(unittest.TestCase):
    """Gemelli (no element, no stone): both barrels on the first shot and on every counter (25.10.2026)."""

    def test_first_shot_and_counter_hit_twice(self):
        live = kampf.daten(MODDIR)
        self.assertEqual((live["weapons"]["gun"]["sig"], live["weapons"]["gun"]["element"]), ("twin", None))
        DEFS["weapons"]["gun"] = live["weapons"]["gun"]
        z = new("akt1_ratte", weapon="gun")
        shots = [e for e in z["kampf"]["events"] if e["art"] == "treffer"]
        self.assertEqual(len(shots), 2)                                          # first shot: two barrels
        zug(z, "angriff", parade=None)
        kampf.parade_aufloesen(z, MODUL, "perfekt", rng=NO)
        counters = [e for e in z["kampf"]["events"] if e["art"] == "treffer"]
        self.assertEqual(len(counters), 2)                                       # perfect parade: counter with both barrels


class Chips(unittest.TestCase):
    """Erweiterungen (chips): finds replace worse levels, work only with Rosi's workshop, effects in the fight (25.10.2026)."""

    def setUp(self):
        self.z = new(start=False)
        kampf.progress(self.z)["test"] = False
        self.z["konto"] = 0
        for sl, i in (("weapon", "sword"), ("weapon", "gun"), ("armor", "jacket_water")):
            kampf.freischalten(self.z, DEFS, sl, i)

    def open(self):
        self.z["flags"].append("werkstatt_offen")

    def test_find_replaces_and_sells(self):
        z = self.z
        self.assertEqual(kampf.chip_finden(z, DEFS, "wucht", 1)["art"], "neu")
        self.assertEqual(kampf.chip_finden(z, DEFS, "wucht", 3)["art"], "besser")        # skipping a level is fine
        self.assertEqual(kampf.chip_pool(z)["pool"]["wucht"], 3)
        r = kampf.chip_finden(z, DEFS, "wucht", 2)
        self.assertEqual((r["art"], r["geld"], z["konto"]), ("schlechter", 20, 20))     # worse find: sold, level stays
        self.assertEqual(kampf.chip_pool(z)["pool"]["wucht"], 3)
        self.assertEqual(kampf.chip_finden(z, DEFS, "wucht", 3)["art"], "gleich")

    def test_unidentified_until_workshop(self):
        z = self.z
        r = kampf.chip_finden(z, DEFS, "praezision", 1)
        self.assertIn("strange chip", r["text"])                                        # no name before Rosi
        with self.assertRaisesRegex(ValueError, "Rosi has to check"):
            kampf.chip_einsetzen(z, DEFS, "weapon", "sword", "praezision")
        self.open()
        kampf.chip_einsetzen(z, DEFS, "weapon", "sword", "praezision")

    def test_slots_and_rules(self):
        z = self.z
        self.open()
        for f in ("wucht", "praezision", "schutz", "element_feuer", "element_wasser"):
            kampf.chip_finden(z, DEFS, f, 1)
        kampf.chip_einsetzen(z, DEFS, "weapon", "sword", "wucht")                       # level 0: one slot
        with self.assertRaisesRegex(ValueError, "slot is taken"):
            kampf.chip_einsetzen(z, DEFS, "weapon", "sword", "praezision")
        kampf.werkstatt(z)["stufen"]["weapon:sword"] = 2                                # level 2: three slots
        kampf.chip_einsetzen(z, DEFS, "weapon", "sword", "praezision")
        with self.assertRaisesRegex(ValueError, "doesn't fit"):                         # jacket chip on a weapon
            kampf.chip_einsetzen(z, DEFS, "weapon", "sword", "schutz")
        with self.assertRaisesRegex(ValueError, "Gemelli"):                             # element chips only for Gemelli
            kampf.chip_einsetzen(z, DEFS, "weapon", "sword", "element_feuer")
        kampf.werkstatt(z)["stufen"]["weapon:gun"] = 2
        kampf.chip_einsetzen(z, DEFS, "weapon", "gun", "element_feuer")
        with self.assertRaisesRegex(ValueError, "one element"):                         # only one element at a time
            kampf.chip_einsetzen(z, DEFS, "weapon", "gun", "element_wasser")
        kampf.chip_einsetzen(z, DEFS, "weapon", "gun", "wucht")                         # moves: only one of each
        self.assertNotIn("wucht", kampf.chip_pool(z)["plaetze"]["weapon:sword"])
        kampf.chip_entfernen(z, "weapon", "gun", "wucht")

    def test_effects_in_the_fight(self):
        z = self.z
        self.open()
        for f, st in (("wucht", 3), ("schutz", 2), ("abwehr_brennend", 3), ("zustand_nass", 3)):
            kampf.chip_finden(z, DEFS, f, st)
        kampf.werkstatt(z)["stufen"]["weapon:bat"] = 2
        kampf.freischalten(z, DEFS, "weapon", "bat")
        kampf.ausruesten(z, DEFS, "weapon", "bat")
        kampf.ausruesten(z, DEFS, "armor", "jacket_earth")
        kampf.werkstatt(z)["stufen"]["armor:jacket_earth"] = 2
        kampf.chip_einsetzen(z, DEFS, "weapon", "bat", "wucht")
        kampf.chip_einsetzen(z, DEFS, "weapon", "bat", "zustand_nass")
        kampf.chip_einsetzen(z, DEFS, "armor", "jacket_earth", "schutz")
        kampf.chip_einsetzen(z, DEFS, "armor", "jacket_earth", "abwehr_brennend")
        kampf.starten(z, DEFS, "akt1_ratte", rng=NO)
        sp = S(z)
        base = DEFS["weapons"]["bat"]["dmg"] + 2                                        # Rosi level 2
        self.assertEqual(sp["weapon"]["dmg"], base + 4)                                 # Hammerfall +4
        self.assertEqual(sp["armor"]["prot"], DEFS["armors"]["jacket_earth"]["prot"] + 2 + 2)   # level 2 + Iron Coat
        c = ctx(z)
        kampf._duc_state(c, "brennend", 2)
        self.assertNotIn("brennend", sp["states"])                                      # Frozen Heart: immune to burning

    def test_drop_after_a_win(self):
        z = self.z
        z["kampf"] = {"gegner": [{"typ": "keiler"}], "ergebnis": {"art": "ko", "zeilen": []}, "def": {}}
        r = kampf.chip_drop_anwenden(z, DEFS)
        self.assertEqual((r["art"], kampf.chip_pool(z)["pool"]), ("neu", {"wucht": 1}))
        self.assertIsNone(kampf.chip_drop_anwenden(z, DEFS))                            # only once per fight

    def test_scout_gift_sits_in_the_worn_jacket(self):
        # Scout (26.10.2026): Rosi fits level I into the worn jacket herself; it counts only while fitted
        z = self.z
        self.open()
        kampf.ausruesten(z, DEFS, "armor", "jacket_earth")                              # what Duc wears on day 8
        self.assertEqual(kampf.aufklaerung(z, DEFS), 0)
        kampf.chip_finden(z, DEFS, "scout", 1)
        self.assertEqual(kampf.aufklaerung(z, DEFS), 0)                                 # in the pool only: no effect
        self.assertTrue(kampf.chip_in_jacke(z, DEFS, "scout"))
        self.assertEqual(kampf.aufklaerung(z, DEFS), 1)
        kampf.chip_finden(z, DEFS, "scout", 2)
        self.assertEqual(kampf.aufklaerung(z, DEFS), 2)                                 # the better find replaces it in place
        kampf.ausruesten(z, DEFS, "armor", "jacket_water")
        self.assertEqual(kampf.aufklaerung(z, DEFS), 0)                                 # other jacket: nothing


class Balance(unittest.TestCase):
    def test_kloster_balancing_values(self):
        # Kloster balancing 26.10.2026 (werkzeuge/kampf_sim_kette.py): Duc 46 LP / base 8, enemies 40/14, +15 %,
        # half the LP back after a win, parry windows +10 %
        self.assertEqual((NEU["LP_BASE"], NEU["BASE_ATTACK"], NEU["ENEMY_LP"], NEU["ENEMY_ATK"]), (46, 8, 40, 14.0))
        self.assertEqual(NEU["LEVEL_GAP"], 0.15)
        self.assertFalse(hasattr(kampf, "CATCH_BREATH"))           # Verschnaufen wieder raus (Duc 26.10.2026)
        self.assertEqual(NEU["TEMPO"]["mittel"]["gut"], 211)        # 160 x 1.1 x 1.2 (Duc 29.10.2026: Parade +20 %)
        self.assertEqual(NEU["TEMPO"]["stark"]["perf"], 58)         # 40 x 1.1 x 1.2 x 1.1 (Duc 03.11.2026: perfekt +10 %)


class Anzeige(unittest.TestCase):
    """Play test 28.10.2026 (hafen_keiler, Duc Lv1): what the screen shows has to match what happens."""
    def test_immune_skills_show_no_odds(self):
        z = new("hafen_keiler")
        fs = {f["id"]: f for f in kampf.faehigkeiten(z)}
        for sid in ("reden", "einschuechtern"):
            self.assertTrue(fs[sid]["gesperrt"])
            self.assertIsNone(fs[sid]["chance"])
        self.assertIn("most animals", fs["einschuechtern"]["text"])

    def test_intimidate_weakens_two_attacks(self):
        # 29.10.2026 (Kloster simulation): one weakened blow wasn't worth a turn - now two; other sources stay at one
        z = new()
        set_intent(z, "n")
        F(z, "einschuechtern", ergebnis="erfolg", parade=None)
        self.assertEqual(G(z)["states"].get("geschwaecht"), kampf.WEAKEN_ATTACKS)
        self.assertIn("next 2 attacks", json.dumps(z["kampf"]["log"], ensure_ascii=False))
        kampf.parade_aufloesen(z, MODUL, "verfehlt", rng=NO)
        self.assertEqual(G(z)["states"].get("geschwaecht"), 1)          # one attack used up, one left
        set_intent(z, "n")
        zug(z, "angriff")                                               # resolves his next attack
        self.assertFalse(G(z)["states"].get("geschwaecht"))

    def test_defeat_card_shows_zero_then_comeback(self):
        z = new("hafen_keiler")
        k = z["kampf"]
        k["spieler"]["lp"] = -3
        kampf._finish(z, MODUL, k, "niederlage")
        self.assertEqual(k["ergebnis"]["wieder_auf"], kampf.LP_AFTER_DEFEAT)
        self.assertEqual(k["spieler"]["lp"], kampf.LP_AFTER_DEFEAT)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    unittest.main(verbosity=1, warnings="ignore")
