# -*- coding: utf-8 -*-
r"""Combat balance simulation v3 (20.10.2026): levels 1-10, enemy levels and threat colour, the three paths
(Kämpfer / Schmuggler / Schütze) with their specials, element states and reactions, item signatures, armor
immunities and the enemy specials. Not used by the engine - it produces numbers for docs\wiki\systeme\kampf.md.

    python kampf_balance_v3.py                full report
    python kampf_balance_v3.py --runs 400     steadier numbers
    python kampf_balance_v3.py --tune         search enemy level formula for the targets
"""
import random, statistics, sys

sys.stdout.reconfigure(encoding="utf-8")
RUNS = int(sys.argv[sys.argv.index("--runs") + 1]) if "--runs" in sys.argv else 200

# ------------------------------------------------------------------ enemy level formula (tunable)
F = {"lp_a": 42, "lp_b": 12, "atk_c": 13.0, "atk_d": 1.6, "boss_lp": 1.2}

# ------------------------------------------------------------------ constants
STAMINA, MEDKIT = 6, 12
PLUIE, MIRE_ROUNDS = 0.6, 2
CRIT_BASE, CRIT_PER_LIST, CRIT_MULT = 0.05, 0.03, 1.5
EXHAUSTED_BONUS, KNIFE_EXHAUSTED_BONUS, WEAK_MALUS, EXPOSED_BONUS, REACH = 4, 5, 3, 3, 1
TYPE_ADV, TYPE_DIS, ELEM_ADV, ELEM_DIS = 1.25, 0.8, 1.2, 0.85
BEATS = {"wasser": "feuer", "feuer": "erde", "erde": "luft", "luft": "wasser"}
STATE_OF = {"feuer": "brennend", "wasser": "nass", "erde": "erschuettert", "luft": "strom"}
STRONG = {"klinge": {"mensch", "tier"}, "stumpf": {"maschine", "monster"}, "messer": {"mensch", "tier"},
          "stange": {"monster", "flieger"}, "fern": {"flieger"}}
WEAK = {"klinge": {"maschine"}, "stumpf": {"flieger"}, "messer": {"monster"}, "stange": {"maschine"},
        "fern": {"monster"}}
TEMPO = {"lästig": "leicht", "gefährlich": "mittel", "tödlich": "stark", "albtraum": "stark"}
SKILL = {"Normal": {"leicht": (0.35, 0.45), "mittel": (0.25, 0.45), "stark": (0.15, 0.40)},
         "Geübt": {"leicht": (0.55, 0.35), "mittel": (0.45, 0.40), "stark": (0.30, 0.45)}}
PATTERN = {"lästig": ["n", "n", "w1"], "gefährlich": ["n", "w1", "n", "s1"],
           "tödlich": ["n", "w1", "n", "w2", "s1"], "albtraum": ["w1", "n", "s1", "w2", "n", "s2"]}

# ------------------------------------------------------------------ enemies: element, class, tier, level, specials
# special: (bonus damage, effect, dodge_only)
E = {
    "Pirate": ("wasser", "mensch", "lästig", 2, {"w1": (0, "nass", False)}),
    "Thief": (None, "mensch", "lästig", 1, {"w1": (2, None, False)}),
    "ThiefArab": (None, "mensch", "lästig", 2, {"w1": (0, "geblendet", False)}),
    "Snake": ("erde", "tier", "lästig", 2, {"w1": (2, "geschwaecht", False)}),
    "Seagull": ("luft", "flieger", "lästig", 1, {"w1": (3, None, True)}),
    "Paparazzo": (None, "mensch", "lästig", 1, {"w1": (0, "geblendet", False)}),
    "Pigeon": ("luft", "flieger", "lästig", 1, {"w1": (0, "geblendet", False)}),
    "Bat": ("luft", "flieger", "lästig", 2, {"w1": (2, "heal3", False)}),
    "Rat": ("erde", "tier", "lästig", 1, {"w1": (2, None, False)}),
    "MaxwellSteward": (None, "mensch", "lästig", 3, {"w1": (0, "buff4", False)}),
    "PirateTorch": ("feuer", "mensch", "gefährlich", 4, {"w1": (3, None, False), "s1": (6, "brennend", False)}),
    "Brute": ("erde", "mensch", "gefährlich", 5, {"w1": (0, "geschwaecht", False), "s1": (8, "erschuettert", False)}),
    "Heinrich": (None, "mensch", "gefährlich", 4, {"w1": (0, "heal5", False), "s1": (6, "blutend", False)}),
    "Dog": ("erde", "tier", "gefährlich", 4, {"w1": (0, "geschwaecht", False), "s1": (0, "blutend", False)}),
    "Ape": ("erde", "tier", "gefährlich", 5, {"w1": (0, "buff3x2", False), "s1": (7, "erschuettert", False)}),
    "Agent": (None, "mensch", "gefährlich", 5, {"w1": (0, "armor2x2", False), "s1": (5, "strom", False)}),
    "Siren": ("wasser", "monster", "gefährlich", 5, {"w1": (0, "ungedeckt", False), "s1": (8, "nass", True)}),
    "DrunkCasanova": ("feuer", "mensch", "gefährlich", 4, {"w1": (0, "heal5", False), "s1": (6, "brennend", False)}),
    "MaxwellSports": (None, "mensch", "gefährlich", 6, {"w1": (0, "buff3x2", False), "s1": (9, "stamina", False)}),
    "Lion": ("erde", "tier", "tödlich", 7, {"w1": (0, "geschwaecht", False), "w2": (0, "buff4", False),
                                           "s1": (10, "blutend", False)}),
    "Unit1": ("feuer", "maschine", "tödlich", 7, {"w1": (0, "geblendet", False), "w2": (0, "buff4x2", False),
                                                 "s1": (8, "brennend", True)}),
    "Shark": ("wasser", "monster", "tödlich", 8, {"w1": (0, "armor2x2", False), "w2": (0, "scent", False),
                                                 "s1": (12, "blutend", True)}),
    "Vampire": ("feuer", "monster", "tödlich", 7, {"w1": (0, "ungedeckt", False), "w2": (3, None, True),
                                                  "s1": (8, "drain", False)}),
    "Mime": (None, "mensch", "tödlich", 8, {"w1": (0, "wall", False), "w2": (0, None, False),
                                           "s1": (6, "silence", False)}),
    "Alon": ("luft", "flieger", "tödlich", 8, {"w1": (0, "dodge", False), "w2": (0, "geschwaecht", False),
                                              "s1": (10, "strom", False)}),
    "YasinDrone": ("luft", "flieger", "tödlich", 7, {"w1": (0, "ungedeckt", False), "w2": (0, "buff3x2", False),
                                                    "s1": (10, "strom", True)}),
    "SeaMonster": ("wasser", "monster", "albtraum", 10, {"w1": (0, "geblendet2", False), "w2": (4, None, False),
                                                        "s1": (12, "nass", True), "s2": (10, "erschuettert", False)}),
    "Alien": ("feuer", "monster", "albtraum", 10, {"w1": (0, "pierce", False), "w2": (0, "stamina", False),
                                                  "s1": (10, "brennend3", False), "s2": (0, "betaeubt", False)}),
    "MaxwellMaximum": (None, "mensch", "albtraum", 9, {"w1": (0, "buff4x2", False), "w2": (0, "armor3x2", False),
                                                      "s1": (12, "erschuettert", False), "s2": (8, "betaeubt", False)}),
}

# ------------------------------------------------------------------ items
W = {  # damage, element, type, signature
    "faust": (0, None, "stumpf", None), "schraubenschluessel": (2, "erde", "stumpf", None),
    "tauchermesser": (2, "wasser", "messer", None), "sportbogen": (3, "luft", "fern", None),
    "elsas_taser": (2, "luft", "stumpf", "every_strom"),
    "feuerwehraxt": (6, "feuer", "klinge", None), "spitzhacke": (6, "erde", "stumpf", None),
    "legionaersmesser": (4, None, "messer", None), "vendetta_messer": (4, None, "messer", None),
    "doppelflinte": (6, "feuer", "fern", None), "luftgewehr": (4, "luft", "fern", None),
    "saufeder": (5, "erde", "stange", None), "fischerspeer": (4, "wasser", "stange", None),
    "rosis_flammenschwert": (9, "feuer", "klinge", "burn3"), "goldener_streitkolben": (7, "erde", "stumpf", "every_quake"),
    "lolas_kochmesser": (7, "feuer", "messer", None), "elektro_harpune": (7, "luft", "fern", "first_strom"),
    "tritons_dreizack": (7, "wasser", "stange", "crit_wet_quake"), "holms_marinesaebel": (8, None, "klinge", "counter15"),
    "yamamotos_katana": (13, "feuer", "klinge", "every_burn"),
}
A = {  # protection, immune states, heavy, bite reduction
    "lederjacke": (1, set(), False, 0), "feuerwehrjacke": (2, {"brennend"}, False, 0),
    "neoprenjacke": (1, {"nass"}, False, 0), "eden_racing_jacke": (3, {"blutend"}, False, 0),
    "haischutz_kettenhemd": (3, set(), True, 0.25), "stichschutzweste": (4, set(), True, 0),
    "cyber_armor": (4, {"strom"}, False, 0),
}
PATHS = {"Kämpfer": "kraft", "Schmuggler": "list", "Schütze": "wahrnehmung"}
GEAR = {  # path -> stage -> weapon
    "Kämpfer": {"G": "schraubenschluessel", "S": "feuerwehraxt", "E": "rosis_flammenschwert", "L": "yamamotos_katana"},
    "Schmuggler": {"G": "tauchermesser", "S": "legionaersmesser", "E": "lolas_kochmesser", "L": "lolas_kochmesser"},
    "Schütze": {"G": "sportbogen", "S": "doppelflinte", "E": "elektro_harpune", "L": "elektro_harpune"},
}
ACC = {"Kämpfer": "gorilla", "Schmuggler": "falke", "Schütze": "robbe"}


def stage(level):
    return "G" if level <= 2 else "S" if level <= 5 else "E" if level <= 8 else "L"


def armor_for(level):
    return "lederjacke" if level <= 2 else "feuerwehrjacke" if level <= 5 else "haischutz_kettenhemd" if level <= 8 else "cyber_armor"


def enemy_stats(name, level):
    el, cls, tier, _lv, specials = E[name]
    lp = F["lp_a"] + F["lp_b"] * level
    if tier == "albtraum":
        lp *= F["boss_lp"]
    return {"name": name, "el": el, "cls": cls, "tier": tier, "lp": int(lp), "max": int(lp),
            "atk": F["atk_c"] + F["atk_d"] * level, "armor": 1 + level // 3, "sp": specials}


class Duc:
    def __init__(self, level, path, skill):
        self.level, self.path, self.skill = level, path, skill
        self.max = 36 + 3 * (level - 1)
        self.lp = self.max
        self.st = STAMINA
        a = min(5, 2 + level // 2)
        self.kraft = a if path == "Kämpfer" else 2
        self.list = a if path == "Schmuggler" else 2
        self.wahr = a if path == "Schütze" else 3
        self.weapon = GEAR[path][stage(level)]
        self.armor = armor_for(level)
        self.acc = ACC[path]
        self.heals = 1
        self.st_ = {}           # duc states: name -> rounds
        self.buff = 0           # libeccio rounds
        self.sure_crit = False
        self.halve_next = False


def mult(weapon, en):
    dmg, wel, wt, _s = W[weapon]
    m = 1.0
    if en["cls"] in STRONG[wt]:
        m *= TYPE_ADV
    elif en["cls"] in WEAK[wt]:
        m *= TYPE_DIS
    if wel and en["el"]:
        if BEATS[wel] == en["el"]:
            m *= ELEM_ADV
        elif BEATS[en["el"]] == wel:
            m *= ELEM_DIS
    return m


def exhausted(es):
    return es.get("erschoepft", 0) > 0 or es.get("blutend", 0) > 0 or (es.get("nass", 0) and es.get("schlamm", 0))


def apply_state(es, en, state, rounds=2):
    """state on the enemy, with reactions."""
    if state == "blutend" and en["cls"] == "maschine":
        return 0
    extra = 0
    if state == "strom" and es.get("nass"):
        es.pop("nass"); es["skip"] = es.get("skip", 0) + 1; extra = int(0.08 * en["max"])
        return extra
    if state == "nass" and es.get("strom"):
        es.pop("strom"); es["skip"] = es.get("skip", 0) + 1; extra = int(0.08 * en["max"])
        return extra
    if state == "nass" and es.get("brennend"):
        es.pop("brennend"); es["blind"] = 1
        return 0
    if state == "brennend" and es.get("nass"):
        es.pop("nass"); es["blind"] = 1
        return 0
    if state == "brennend" and es.get("blutend"):
        extra = int(0.05 * en["max"]) * es.pop("blutend")
    if state == "strom" and es.get("brennend"):
        es["brennend"] += 1; es["burn_x2"] = 1
    if state == "erschuettert" and es.get("nass"):
        es["schlamm"] = 1
    es[state] = max(es.get(state, 0), rounds + (1 if state == "blutend" else 0))
    return extra


def hit(d, en, es, rng, factor=1.0, extra=0, force_crit=False, crit_mult=CRIT_MULT, proc=False):
    dmg, wel, wt, sig = W[d.weapon]
    raw = 6 + d.kraft + dmg + extra + (4 if d.buff > 0 else 0) - (WEAK_MALUS if d.st_.get("geschwaecht") else 0)
    if exhausted(es):
        raw += KNIFE_EXHAUSTED_BONUS if wt == "messer" else EXHAUSTED_BONUS
    armor = 0 if es.get("erschuettert") else en["armor"]
    if es.get("wall"):
        es.pop("wall"); return 0
    val = max(1, round(raw * mult(d.weapon, en) * factor) - armor)
    crit_p = CRIT_BASE + CRIT_PER_LIST * d.list + (0.05 if wt == "messer" else 0) + (0.05 if d.acc == "falke" else 0)
    crit = force_crit or d.sure_crit or rng.random() < crit_p
    d.sure_crit = False
    if crit:
        val = int(-(-val * crit_mult // 1))
    if es.get("dodge"):
        es.pop("dodge"); val //= 2
    if es.get("erschoepft"):
        es["erschoepft"] -= 1
    # states from the weapon
    state = STATE_OF.get(wel) if wel else ("blutend" if wt in ("klinge", "messer") else "geschwaecht")
    if sig == "every_burn":
        val += apply_state(es, en, "brennend")
    elif sig == "every_strom":
        val += apply_state(es, en, "strom")
    elif sig == "every_quake":
        val += apply_state(es, en, "erschuettert")
    if crit or proc:
        if sig == "crit_wet_quake":
            val += apply_state(es, en, "nass"); val += apply_state(es, en, "erschuettert")
        elif state == "geschwaecht":
            es["geschwaecht"] = 1
        else:
            val += apply_state(es, en, state, 3 if (sig == "burn3" and state == "brennend") else 2)
    return val


def tick(es, en, d):
    """damage over time at the end of a round."""
    dmg = 0
    if es.get("brennend"):
        dmg += int(0.05 * en["max"]) * (2 if es.get("burn_x2") else 1)
    if es.get("blutend"):
        dmg += int(0.05 * en["max"])
    for k in list(es):
        if k in ("brennend", "blutend", "nass", "strom", "erschuettert", "blind", "schlamm", "burn_x2", "armor_up",
                 "buff", "silence_d"):
            es[k] -= 1
            if es[k] <= 0:
                es.pop(k)
    return dmg


def duc_turn(d, en, es, rng, rnd, nxt_strong):
    lv, p, st = d.level, d.path, d.st
    if d.st_.get("betaeubt"):
        d.st_.pop("betaeubt"); return "stun"
    if d.st_.get("strom") and rng.random() < 0.25:
        return "lost"
    silenced = d.st_.get("silence", 0) > 0
    if d.lp < d.max * 0.35 and d.heals:
        d.heals -= 1; d.lp = min(d.max, d.lp + MEDKIT); return "heal"
    if p == "Schütze" and lv >= 3 and not silenced and st >= 2 and not es.get("erschoepft") and rnd % 3 == 1:
        d.st -= 2; es["erschoepft"] = MIRE_ROUNDS; return "mire"
    if not silenced:
        if p == "Kämpfer":
            if lv >= 9 and st >= 4 and exhausted(es):
                d.st -= 4
                en["lp"] -= hit(d, en, es, rng, 3.0 if es.get("erschuettert") else 2.0); return "lame"
            cost = 2 if d.acc == "gorilla" else 3
            if lv >= 3 and st >= cost and not es.get("erschuettert"):
                d.st -= cost; en["lp"] -= hit(d, en, es, rng, extra=4); es["erschuettert"] = 2; return "mistral"
            if lv >= 7 and st >= 2 and d.buff <= 0 and not nxt_strong:
                d.st -= 2; d.buff = 2; d.st_["ungedeckt"] = 1
                if es.get("brennend"):
                    es["brennend"] += 1
                return "libeccio"
            if lv >= 5 and st >= 3 and nxt_strong:
                d.st -= 3; en["lp"] -= hit(d, en, es, rng, 2.0 if es.get("nass") else 1.0); es["geschwaecht"] = 1
                return "ressac"
        elif p == "Schmuggler":
            if lv >= 9 and st >= 4 and exhausted(es):
                n = sum(1 for k in ("brennend", "blutend", "nass", "strom", "erschuettert", "geschwaecht", "erschoepft") if es.get(k))
                d.st -= 4; en["lp"] -= hit(d, en, es, rng, 1 + 0.25 * n, force_crit=True, crit_mult=2.5); return "omerta"
            if lv >= 7 and st >= 3 and not es.get("blutend") and en["cls"] != "maschine":
                d.st -= 3; apply_state(es, en, "blutend"); return "vendetta"
            if lv >= 5 and st >= 2 and nxt_strong:
                d.st -= 2; d.halve_next = True; d.sure_crit = True; return "sotto"
            if lv >= 3 and st >= 3:
                d.st -= 3; en["lp"] -= hit(d, en, es, rng, 0.7); en["lp"] -= hit(d, en, es, rng, 0.7); return "doppio"
        else:
            if lv >= 9 and st >= 4:
                d.st -= 4
                for _ in range(3):
                    en["lp"] -= hit(d, en, es, rng, 1.0 if en["cls"] == "flieger" else PLUIE, proc=True)
                return "pluie"
            if lv >= 7 and st >= 3 and nxt_strong:
                d.st -= 3; es["skip"] = es.get("skip", 0) + (2 if es.get("strom") else 1); return "phare"
            if lv >= 5 and st >= 2 and nxt_strong:
                d.st -= 2; d.st_["bonaccia"] = 1; return "bonaccia"
    if nxt_strong and d.st < 3:
        d.st = min(STAMINA, d.st + 2); d.st_["guard"] = 1; return "guard"
    en["lp"] -= hit(d, en, es, rng); d.st = min(STAMINA, d.st + 1); return "attack"


def fight(name, level, d_level, path, skill, rng):
    d = Duc(d_level, path, skill)
    en = enemy_stats(name, level)
    es = {}
    tempo = TEMPO[en["tier"]]
    pat = PATTERN[en["tier"]]
    step, rnd, buff_atk, armor_up = 0, 0, 0, 0
    if W[d.weapon][2] == "fern":
        en["lp"] -= hit(d, en, es, rng)
        if W[d.weapon][3] == "first_strom":
            apply_state(es, en, "strom")
    while rnd < 40:
        rnd += 1
        key = pat[step % len(pat)]
        nxt_strong = key.startswith("s")
        duc_turn(d, en, es, rng, rnd, nxt_strong)
        if d.buff > 0:
            d.buff -= 1
        if en["lp"] <= 0:
            return True, rnd, 1 - d.lp / d.max
        # enemy action
        step += 1
        if es.get("skip"):
            es["skip"] -= 1
        elif es.get("strom") and rng.random() < 0.25:
            pass
        else:
            bonus, effect, dodge_only = (0, None, False) if key == "n" else en["sp"][key]
            heavy = key.startswith("s")
            if effect in ("heal3", "heal5"):
                en["lp"] = min(en["max"], en["lp"] + (3 if effect == "heal3" else 5))
            elif effect in ("buff4", "buff3x2", "buff4x2"):
                buff_atk = 4 if "4" in effect else 3
                es["buff"] = 2 if "x2" in effect else 1
            elif effect in ("armor2x2", "armor3x2"):
                armor_up = 2 if "2x2" in effect else 3; es["armor_up"] = 2
            elif effect == "wall":
                es["wall"] = 1
            elif effect == "dodge":
                es["dodge"] = 1
            if effect not in ("heal3", "heal5", "buff4", "buff3x2", "buff4x2", "armor2x2", "armor3x2", "wall", "dodge") \
                    or bonus:
                prot, immune, heavy_armor, bite = A[d.armor]
                atk = en["atk"] + bonus + (4 if heavy else 0) + (buff_atk if es.get("buff") else 0)
                atk -= WEAK_MALUS if es.get("geschwaecht") else 0
                atk -= REACH if W[d.weapon][2] == "stange" else 0
                armor = 0 if d.st_.get("erschuettert") or effect == "pierce" else 2 + prot
                dmg = max(1, round(atk) - armor + (EXPOSED_BONUS if d.st_.get("ungedeckt") else 0))
                if effect == "scent" and d.st_.get("blutend"):
                    dmg += 5
                if bite and en["cls"] in ("tier", "monster"):
                    dmg = max(1, round(dmg * (1 - bite)))
                if es.get("blind") or d.halve_next:
                    dmg = max(1, dmg // 2); d.halve_next = False
                if d.st_.get("guard"):
                    dmg = max(1, dmg // 2)
                perf, good = SKILL[skill][tempo]
                f = 1 + 0.03 * d.wahr
                f *= 1.5 if d.st_.get("guard") else 1
                f *= 0.8 if heavy else 1
                f *= 0.9 if heavy_armor else 1
                f *= 0.8 if (d.st_.get("nass") or d.st_.get("geblendet")) else 1
                if d.st_.get("bonaccia"):
                    f *= 1.5 * (1.3 if es.get("nass") else 1)
                if es.get("nass"):
                    f *= 1.3 * (1.2 if d.acc == "robbe" else 1)
                perf, good = min(0.95, perf * f), min(0.95, good * f)
                if perf + good > 0.97:
                    good = 0.97 - perf
                r = rng.random()
                d.st_.pop("ungedeckt", None)
                if r < perf:
                    dmg = 0
                    d.st = min(STAMINA, d.st + 1)
                    if not dodge_only:
                        c = hit(d, en, es, rng, proc=True)
                        if d.st_.get("bonaccia"):
                            c *= 2
                        if W[d.weapon][3] == "counter15":
                            c = int(c * 1.5)
                        en["lp"] -= c
                        es["erschoepft"] = max(es.get("erschoepft", 0), 1)
                    effect_rounds = 0
                elif r < perf + good:
                    dmg = max(1, dmg // 2); effect_rounds = 1
                else:
                    effect_rounds = 2
                d.lp -= dmg
                if effect == "drain":
                    en["lp"] = min(en["max"], en["lp"] + dmg)
                if effect and effect_rounds and effect not in immune:
                    if effect in ("nass", "brennend", "blutend", "erschuettert", "strom", "geschwaecht", "geblendet",
                                  "ungedeckt", "betaeubt"):
                        d.st_[effect] = 1 if effect in ("ungedeckt", "betaeubt", "geschwaecht") else effect_rounds
                    elif effect == "brennend3":
                        if "brennend" not in immune:
                            d.st_["brennend"] = effect_rounds + 1
                    elif effect == "geblendet2":
                        d.st_["geblendet"] = effect_rounds
                    elif effect == "silence":
                        d.st_["silence"] = 2
                    elif effect == "stamina":
                        d.st = max(0, d.st - 1)
                if heavy:
                    es["erschoepft"] = max(es.get("erschoepft", 0), 1)
            if es.get("armor_up"):
                en["armor"] = 1 + level // 3 + armor_up
        # end of round: damage over time and state timers
        en["lp"] -= tick(es, en, d)
        for k in ("brennend", "blutend"):
            if d.st_.get(k):
                d.lp -= int(0.05 * d.max)
        for k in list(d.st_):
            if k in ("guard", "bonaccia"):
                d.st_.pop(k); continue
            if k in ("nass", "brennend", "blutend", "erschuettert", "strom", "geblendet", "silence"):
                d.st_[k] -= 1
                if d.st_[k] <= 0:
                    d.st_.pop(k)
        if not es.get("armor_up"):
            en["armor"] = 1 + level // 3
        if en["lp"] <= 0:
            return True, rnd, 1 - max(0, d.lp) / d.max
        if d.lp <= 0:
            return False, rnd, 1.0
    return False, rnd, 1 - max(0, d.lp) / d.max


def run(name, e_level, d_level, path, skill, n=RUNS):
    rng = random.Random(hash((name, e_level, d_level, path, skill)) & 0xffffffff)
    res = [fight(name, e_level, d_level, path, skill, rng) for _ in range(n)]
    return sum(r[0] for r in res) / n, statistics.mean(r[1] for r in res), statistics.mean(r[2] for r in res)


BANDS = {2: "lästig", 4: "gefährlich", 7: "tödlich", 9: "albtraum"}
DIFF = {-1: "Lästig (grau)", 0: "Gefährlich (grün)", 1: "Tödlich (orange)", 2: "Albtraum (Totenkopf)"}


def matrix(n=RUNS):
    out = {}
    for path in PATHS:
        for skill in SKILL:
            for d_level, tier in BANDS.items():
                names = [x for x in E if E[x][2] == tier]
                for diff in DIFF:
                    lv = max(1, min(12, d_level + diff))
                    r = [run(x, lv, d_level, path, skill, n) for x in names]
                    out[(path, skill, d_level, diff)] = (statistics.mean(a[0] for a in r), statistics.mean(a[1] for a in r),
                                                         statistics.mean(a[2] for a in r))
    return out


def report():
    m = matrix()
    print("Sieg % / LP-Verlust % (Ø über die Gegner der Stufe). Ausrüstung passend zu Ducs Level, Pfad rein.\n")
    for skill in SKILL:
        print("== %s ==" % skill)
        print("%-11s %-4s" % ("Pfad", "Lv") + "".join("%22s" % DIFF[x] for x in DIFF))
        for path in PATHS:
            for d_level in BANDS:
                cells = ["%3.0f%% / %3.0f%%" % (m[(path, skill, d_level, x)][0] * 100, m[(path, skill, d_level, x)][2] * 100)
                         for x in DIFF]
                print("%-11s %-4d" % (path, d_level) + "".join("%22s" % c for c in cells))
        print()
    print("Einzelgegner, grün (gleiches Level), Normal, Schnitt der drei Pfade (Ausreißer):")
    for name, (el, cls, tier, lv, _s) in E.items():
        d_level = {"lästig": 2, "gefährlich": 4, "tödlich": 7, "albtraum": 9}[tier]
        r = [run(name, d_level, d_level, p, "Normal") for p in PATHS]
        per = " ".join("%s %3.0f%%" % (p[:4], x[0] * 100) for p, x in zip(PATHS, r))
        print("  %-15s %-10s %-8s %-7s Ø %3.0f%%  | %s" % (name, tier, cls, el or "-", statistics.mean(x[0] for x in r) * 100, per))


TARGET = {("Normal", 0): 0.85, ("Normal", 1): 0.55, ("Normal", 2): 0.20,
          ("Geübt", 0): 0.97, ("Geübt", 1): 0.85, ("Geübt", 2): 0.50}


def tune():
    best = None
    for a in (30, 42, 54):
        for b in (12, 16, 20):
            for c in (12.0, 15.0, 18.0):
                for dd in (1.6, 2.2, 2.8):
                    F.update(lp_a=a, lp_b=b, atk_c=c, atk_d=dd)
                    m = matrix(60)
                    err = 0
                    for (sk, diff), t in TARGET.items():
                        vals = [m[(p, sk, lv, diff)][0] for p in PATHS for lv in BANDS]
                        err += (statistics.mean(vals) - t) ** 2
                    if best is None or err < best[0]:
                        best = (err, a, b, c, dd)
                        print("best so far", best)
    print("BEST", best)


if __name__ == "__main__":
    tune() if "--tune" in sys.argv else report()
