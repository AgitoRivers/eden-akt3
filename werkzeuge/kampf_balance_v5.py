# -*- coding: utf-8 -*-
r"""Overall balance v5 (23.10.2026): v4 + Duc's decisions of 22./23.10.:

  * burning stacks 1-5 (3 % max LP per stack and round, bosses half), fades by 1 only in a round without a new
    stack; wet removes all stacks; shock adds a stack (instead of doubling); same rules on Duc (guard removes a
    stack, firefighter jacket immune)
  * the 5s answer EVERY announced enemy special: full against a strong one, reduced against a weak one
  * K7 Windruestung is defensive: 2 rounds half damage, a perfect parade shakes the enemy
  * "erschoepft" counts rounds, not hits (multi-hits no longer eat it)
  * L5 sure crit hitting L9 Gnadenstoss: crit x3.5 instead of x2.5; L9 counts at most 4 states (burn stacks single)
  * new path Berserker (courage): M3 Glutschlag, M5 Rachefeuer, M7 Flammenrausch, M9 Feuersturm
    (one hit per burn stack at 60 %, ignores protection, uses up the stacks, then Duc skips a round)
  * Yamamoto's katana: every second hit adds a stack

Not used by the engine - it produces numbers for docs\wiki\systeme\kampf.md. Code ids keep the game names (mistral ...).

    python kampf_balance_v5.py           comparison v4 rules (3 paths) vs v5 rules (4 paths) + use of each special
    python kampf_balance_v5.py --n 60    more fights per cell (steadier, slower)
    python kampf_balance_v5.py --builds  all free skill mixes (1 point at Lv 3/5/7/9, 2 at Lv 10, tier needs the one below)
    variants: --boss-burn 0.5 · --ohne-w5-konter · --w5-faktor 0.75 · --l5 halb|stark

Result 23.10.2026 (n 80): see docs\wiki\systeme\kampf.md once Duc has approved. Simulated player: answers a weak special
only if it hurts, uses L5 against a weak one only with stamina to spare, never takes Rachefeuer below half LP.
"""
import collections, random, statistics, sys, os

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ARGS = list(sys.argv)
N = int(ARGS[ARGS.index("--n") + 1]) if "--n" in ARGS else 30
sys.argv = [sys.argv[0]]
import kampf_balance_v4 as v4  # noqa: E402  (patches v3 with growth, gear upgrades, kitchen)
kb, kt = v4.kb, v4.kt

ORIG = {k: getattr(kb, k) for k in ("apply_state", "hit", "tick", "duc_turn", "fight", "exhausted")}
ORIG_INIT = kb.Duc.__init__

BURN_PER_STACK, BURN_MAX, BOSS_BURN = 0.03, 5, 0.75      # bosses 3/4 (with 1/2 the Berserker collapses at Albtraum)
M9_FACTOR, M7_FACTOR = 0.6, 1.3
STATE_CAP_L9 = 4
M9_OHNE_ERSCHOEPFT = "--m9-ohne-erschoepft" in ARGS
W_SKALIERUNG = "--ohne-w-skalierung" not in ARGS   # W skills full only with Wahrnehmung >= 4 (else W3 until the next own turn, W5 half)
M9_AB = int(ARGS[ARGS.index("--m9-ab") + 1]) if "--m9-ab" in ARGS else 4      # sim player fires M9 from n stacks
W3_FAKTOR = float(ARGS[ARGS.index("--w3") + 1]) if "--w3" in ARGS else 0.0   # W3 Zielmarke as a real shot
L5_WEAK = ARGS[ARGS.index("--l5") + 1] if "--l5" in ARGS else "krit"   # L5 vs weak special: "krit" or "halb"
# W5 Ruhepuls also strikes back (x1.0, against a weak special x0.5) - without it the Schütze drops ~20 points at Lv 7
W5_KONTER = "--ohne-w5-konter" not in ARGS
# L7 Blutschnitt: instant hit at 30 % before the bleed (50 % before knives struck with List)
L7_FAKTOR = float(ARGS[ARGS.index("--l7") + 1]) if "--l7" in ARGS else 0.3
W5_FAKTOR = float(ARGS[ARGS.index("--w5-faktor") + 1]) if "--w5-faktor" in ARGS else 1.0
W7_PRO_PUNKT = float(ARGS[ARGS.index("--w7") + 1]) if "--w7" in ARGS else 0.15   # skip chance per Wahrnehmung < 4
M5_KOSTEN = int(ARGS[ARGS.index("--m5-kosten") + 1]) if "--m5-kosten" in ARGS else 2
# M5 counter factors: parade made / made against a strong special / parade missed (Duc 24.10.: only damage tuned)
M5_MULT = [float(x) for x in ARGS[ARGS.index("--m5-mult") + 1].split(",")] if "--m5-mult" in ARGS else [1.5, 2.0, 0.5]
M5_UNGEDECKT = "--m5-ungedeckt" in ARGS                 # while charged Duc is exposed (+3 against him)
M5_FENSTER = float(ARGS[ARGS.index("--m5-fenster") + 1]) if "--m5-fenster" in ARGS else 1.0   # parade window
M5_PAUSE = int(ARGS[ARGS.index("--m5-pause") + 1]) if "--m5-pause" in ARGS else 0    # rounds between two charges
MESSER_LIST = "--ohne-messer-list" not in ARGS          # knives strike with List (23.10.2026)
L3_FAKTOR = float(ARGS[ARGS.index("--l3") + 1]) if "--l3" in ARGS else 0.7        # L3 Doppelschnitt per cut
HARMLESS = {"heal3", "heal5", "buff4", "buff3x2", "buff4x2", "armor2x2", "armor3x2", "wall", "dodge"}
if "--boss-burn" in ARGS:
    BOSS_BURN = float(ARGS[ARGS.index("--boss-burn") + 1])
USE = collections.defaultdict(list)          # (path, special) -> damage dealt by that action


# ------------------------------------------------------------------ burning (stacks)
def burn_add(holder, n=1):
    """holder: enemy state dict or Duc state dict. Returns new stack count."""
    holder["brennend"] = min(BURN_MAX, holder.get("brennend", 0) + n)
    holder["burn_new"] = 1
    return holder["brennend"]


def apply_state(es, en, state, rounds=2):
    if state == "blutend" and en["cls"] == "maschine":
        return 0
    extra = 0
    if state == "strom" and es.get("nass"):
        es.pop("nass"); es["skip"] = es.get("skip", 0) + 1
        return int(0.08 * en["max"])
    if state == "nass" and es.get("strom"):
        es.pop("strom"); es["skip"] = es.get("skip", 0) + 1
        return int(0.08 * en["max"])
    if state == "nass" and es.get("brennend"):                 # steam: wet puts out ALL stacks
        es.pop("brennend"); es.pop("burn_new", None); es["blind"] = 1
        return 0
    if state == "brennend" and es.get("nass"):
        es.pop("nass"); es["blind"] = 1
        return 0
    if state == "brennend":
        if es.get("blutend"):                                   # bursting: bleed turns into damage at once
            extra = int(0.05 * en["max"]) * es.pop("blutend")
        burn_add(es, 2 if rounds >= 3 else 1)                    # rounds 3 = Rosi's sword signature -> 2 stacks
        return extra
    if state == "strom" and es.get("brennend"):
        burn_add(es, 1)
    if state == "erschuettert" and es.get("nass"):
        es["schlamm"] = 1
    es[state] = max(es.get(state, 0), rounds + (1 if state == "blutend" else 0))
    return extra


def hit(d, en, es, rng, factor=1.0, extra=0, force_crit=False, crit_mult=kb.CRIT_MULT, proc=False, pierce=False):
    dmg, wel, wt, sig = kb.W[d.weapon]
    attr = max(d.kraft, d.mut) if d.path == "Berserker" else d.kraft
    if MESSER_LIST and wt == "messer":                          # knives strike with List (like the Berserker with Mut)
        attr = max(attr, d.list)
    raw = 6 + attr + dmg + extra - (kb.WEAK_MALUS if d.st_.get("geschwaecht") else 0)
    if kb.exhausted(es) and not (pierce and M9_OHNE_ERSCHOEPFT):   # M9: ignores protection, no exhausted bonus
        raw += kb.KNIFE_EXHAUSTED_BONUS if wt == "messer" else kb.EXHAUSTED_BONUS
    if d.rausch > 0:
        factor *= M7_FACTOR
    armor = 0 if (pierce or es.get("erschuettert")) else en["armor"]
    if es.get("wall"):
        es.pop("wall"); return 0
    val = max(1, round(raw * kb.mult(d.weapon, en) * factor) - armor)
    crit_p = kb.CRIT_BASE + kb.CRIT_PER_LIST * d.list + (0.05 if wt == "messer" else 0) + (0.05 if d.acc == "falke" else 0)
    crit = force_crit or d.sure_crit or rng.random() < crit_p
    if crit:
        val = int(-(-val * crit_mult // 1))
    d.sure_crit = False
    if es.get("dodge"):
        es.pop("dodge"); val //= 2
    # erschoepft is NOT used up by hits any more (counts rounds, see tick)
    d.hits += 1
    state = kb.STATE_OF.get(wel) if wel else ("blutend" if wt in ("klinge", "messer") else "geschwaecht")
    if sig == "every_burn":
        if d.hits % 2 == 0:                                     # katana: every second hit
            val += apply_state(es, en, "brennend")
    elif sig == "every_strom":
        val += apply_state(es, en, "strom")
    elif sig == "every_quake":
        val += apply_state(es, en, "erschuettert")
    if d.rausch > 0:                                            # M7: every hit adds a stack
        val += apply_state(es, en, "brennend")
    if crit or proc:
        if sig == "crit_wet_quake":
            val += apply_state(es, en, "nass"); val += apply_state(es, en, "erschuettert")
        elif state == "geschwaecht":
            es["geschwaecht"] = 1
        else:
            val += apply_state(es, en, state, 3 if (sig == "burn3" and state == "brennend") else 2)
    return val


def tick(es, en, d):
    dmg = 0
    if es.get("brennend"):
        dmg += int(BURN_PER_STACK * en["max"] * es["brennend"] * (BOSS_BURN if en["tier"] == "albtraum" else 1))
        if not es.pop("burn_new", None):
            es["brennend"] -= 1
            if es["brennend"] <= 0:
                es.pop("brennend")
    if es.get("blutend"):
        dmg += int(0.05 * en["max"])
    for k in list(es):
        if k in ("blutend", "nass", "strom", "erschuettert", "blind", "schlamm", "armor_up", "buff", "silence_d",
                 "erschoepft"):
            es[k] -= 1
            if es[k] <= 0:
                es.pop(k)
    return dmg


def n_states(es):
    n = sum(1 for k in ("blutend", "nass", "strom", "erschuettert", "geschwaecht", "erschoepft") if es.get(k))
    n += es.get("brennend", 0)                                  # burn stacks count one by one ...
    return min(STATE_CAP_L9, n)                                 # ... but at most 4 states


# ------------------------------------------------------------------ Duc: skills (free choice, step by step)
LETTER = {"Kämpfer": "K", "Schmuggler": "L", "Schütze": "W", "Berserker": "M"}
PATH_OF = {v: k for k, v in LETTER.items()}
TIERS = (3, 5, 7, 9)


def skills_for(path, level):
    """Pure path: the path's specials up to the level (Lv 3/5/7/9)."""
    return {LETTER[path] + str(t) for t in TIERS if level >= t}


def build_skills(depths):
    """depths: {"K": 2, "M": 4, ...} -> skill set; a tier needs the tier below in the same path."""
    return {p + str(TIERS[i]) for p, n in depths.items() for i in range(n)}


def duc_init(self, level, path, skill):
    """path: a path name (pure build) or a tuple (main path, skill set) for a mixed build. The main path decides
    weapon, accessory, path quirk and which attribute grows (assumption until attribute points are decided)."""
    if isinstance(path, tuple):
        main, skills = path
    else:
        main, skills = path, skills_for(path, level)
    ORIG_INIT(self, level, main if main != "Berserker" else "Kämpfer", skill)
    self.path, self.skills = main, set(skills)
    a = min(5, 2 + level // 2)
    if main == "Berserker":
        self.kraft = 2
        self.mut = min(5, a + (1 if v4.CFG["kitchen"] else 0))
        self.acc = "salamander"
    else:
        self.mut = 2
    self.hits, self.rausch, self.wind = 0, 0, 0
    self.m5_frei = 0                                            # round from which M5 can be charged again
    self.st_max = self.st


def stam(d, n):
    d.st = min(d.st_max, d.st + n)


def duc_turn(d, en, es, rng, rnd, nxt):
    """nxt: (is_special, is_strong, hurts) of the enemy's announced next action. Skill-based: works for pure paths
    and mixed builds. Order = what a sensible player does: finale if ready, answer a special, set up, damage.
    A weak special is only answered if it hurts (no point in countering a heal or a buff)."""
    sa, strong, hurts = nxt
    sa = strong or (sa and hurts)
    has, st = d.skills.__contains__, d.st
    if d.st_.get("aussetzen"):
        d.st_.pop("aussetzen"); return "aussetzen"
    if d.st_.get("betaeubt"):
        d.st_.pop("betaeubt"); return "stun"
    if d.st_.get("strom") and rng.random() < 0.25:
        return "lost"
    if d.lp < d.max * 0.35 and d.heals:
        d.heals -= 1; d.lp = min(d.max, d.lp + kb.MEDKIT); return "heal"
    if d.st_.get("silence", 0) <= 0:
        stacks = es.get("brennend", 0)
        # ---- finales
        if has("M9") and st >= 4 and stacks and (stacks >= M9_AB or en["lp"] < en["max"] * 0.3):
            d.st -= 4                                          # can always be started - pays off only with stacks
            for _ in range(stacks):
                en["lp"] -= hit(d, en, es, rng, M9_FACTOR, pierce=True)
            es.pop("brennend", None); es.pop("burn_new", None)
            d.st_["aussetzen"] = 1
            return "vulcano"
        if has("K9") and st >= 4 and kb.exhausted(es):
            d.st -= 4
            en["lp"] -= hit(d, en, es, rng, 3.0 if es.get("erschuettert") else 2.0); return "lame"
        if has("L9") and st >= 4 and kb.exhausted(es):
            mult = 3.5 if d.sure_crit else 2.5
            d.st -= 4; en["lp"] -= hit(d, en, es, rng, 1 + 0.25 * n_states(es), force_crit=True, crit_mult=mult)
            return "omerta"
        if has("W9") and st >= 4:
            d.st -= 4
            for _ in range(3):
                en["lp"] -= hit(d, en, es, rng, 1.0 if en["cls"] == "flieger" else kb.PLUIE, proc=True)
            return "pluie"
        # ---- prepare the own finale first (bleed / exhaust), then answer
        if (has("K9") or has("L9")) and not kb.exhausted(es):
            if has("L7") and st >= 3 + 4 * 0 and not es.get("blutend") and en["cls"] != "maschine":
                d.st -= 3
                if L7_FAKTOR:
                    en["lp"] -= hit(d, en, es, rng, L7_FAKTOR)
                apply_state(es, en, "blutend"); return "vendetta"
            if has("W3") and st >= 2 and (not W_SKALIERUNG or d.wahr >= 4 or not (has("K3") or has("L7"))):
                d.st -= 2
                if W3_FAKTOR:
                    en["lp"] -= hit(d, en, es, rng, W3_FAKTOR)
                es["erschoepft"] = kb.MIRE_ROUNDS if (not W_SKALIERUNG or d.wahr >= 4) else 2; return "mire"
        # ---- answers to an announced special (best first)
        if sa:
            w_voll = not W_SKALIERUNG or d.wahr >= 4
            # a weak W5 (no Wahrnehmung) only comes after the own path's answers
            if has("W5") and st >= 2 and (w_voll or not (has("M5") or has("K5") or has("L5"))):
                voll = strong and w_voll
                d.st -= 2; d.st_["bonaccia"] = "voll" if voll else "halb"; return "bonaccia"
            if has("W7") and st >= 3 and strong:                 # W7 is not a 5: only against a strong special
                d.st -= 3
                if not W_SKALIERUNG or d.wahr >= 4:
                    es["skip"] = es.get("skip", 0) + (2 if es.get("strom") else 1)
                else:                       # below Wahrnehmung 4: blinds, skips only with x % per Wahrnehmung point
                    es["blind"] = max(es.get("blind", 0), 1)
                    if rng.random() < W7_PRO_PUNKT * d.wahr:
                        es["skip"] = es.get("skip", 0) + 1
                return "phare"
            if has("M5") and st >= M5_KOSTEN and not d.st_.get("rache") and rnd >= d.m5_frei:   # charge skill (24.10.)
                d.st -= M5_KOSTEN; d.st_["rache"] = True; d.m5_frei = rnd + 1 + M5_PAUSE
                if M5_UNGEDECKT:
                    d.st_["ungedeckt"] = 1                       # the glowing weapon leaves Duc open
                return "retour"
            if has("K5") and st >= 3:
                d.st -= 3; en["lp"] -= hit(d, en, es, rng, 2.0 if es.get("nass") else 1.0)
                if strong:
                    es["geschwaecht"] = 1
                return "ressac"
            if has("L5") and st >= 2 and (strong or (L5_WEAK != "stark" and st >= 5)):
                d.st -= 2; d.halve_next = d.halve_next or strong or L5_WEAK == "halb"
                d.sure_crit = True if (strong or L5_WEAK == "krit") else d.sure_crit
                return "sotto"
            if has("K7") and st >= 2 and d.wind <= 0:
                d.st -= 2; d.wind = 2; return "libeccio"
        # ---- set-ups
        finisher_needs_exhaust = has("K9") or has("L9")
        if has("W3") and st >= 2 and not es.get("erschoepft") and (rnd % 3 == 1 or
                                                                   (finisher_needs_exhaust and not kb.exhausted(es))):
            d.st -= 2
            if W3_FAKTOR:
                en["lp"] -= hit(d, en, es, rng, W3_FAKTOR)
            es["erschoepft"] = kb.MIRE_ROUNDS if (not W_SKALIERUNG or d.wahr >= 4) else 2; return "mire"
        if has("L7") and st >= 3 and not es.get("blutend") and en["cls"] != "maschine":
            d.st -= 3
            if L7_FAKTOR:
                en["lp"] -= hit(d, en, es, rng, L7_FAKTOR)
            apply_state(es, en, "blutend"); return "vendetta"
        if has("M7") and st >= 3 and d.rausch <= 0:
            d.st -= 3; d.rausch = 2
            if "brennend" not in kb.A[d.armor][1]:
                burn_add(d.st_, 1)
            en["lp"] -= hit(d, en, es, rng); return "furia"
        cost = 2 if d.acc == "gorilla" else 3
        if has("K3") and st >= cost and not es.get("erschuettert"):
            d.st -= cost; en["lp"] -= hit(d, en, es, rng, extra=4); es["erschuettert"] = 2; return "mistral"
        if has("M3") and st >= 3:
            d.st -= 3; en["lp"] -= hit(d, en, es, rng, extra=4); apply_state(es, en, "brennend")
            d.st_["ungedeckt"] = 1; return "scirocco"
        if has("L3") and st >= 3:
            d.st -= 3; en["lp"] -= hit(d, en, es, rng, L3_FAKTOR); en["lp"] -= hit(d, en, es, rng, L3_FAKTOR)
            return "doppio"
    if sa and d.st < 3 and d.rausch <= 0:
        stam(d, 2); d.st_["guard"] = 1
        if d.st_.get("brennend"):
            d.st_["brennend"] -= 1
            if d.st_["brennend"] <= 0:
                d.st_.pop("brennend")
        return "guard"
    en["lp"] -= hit(d, en, es, rng); stam(d, 1); return "attack"


def fight(name, level, d_level, path, skill, rng):
    d = kb.Duc(d_level, path, skill)
    path = path[0] + "*" if isinstance(path, tuple) else path     # key for USE; the quirks read d.path
    en = kb.enemy_stats(name, level)
    es = {}
    tempo = kb.TEMPO[en["tier"]]
    pat = kb.PATTERN[en["tier"]]
    step, rnd, buff_atk, armor_up = 0, 0, 0, 0
    if kb.W[d.weapon][2] == "fern":
        en["lp"] -= hit(d, en, es, rng)
        if kb.W[d.weapon][3] == "first_strom":
            apply_state(es, en, "strom")
    while rnd < 40:
        rnd += 1
        key = pat[step % len(pat)]
        is_sa = key != "n" and key in en["sp"]
        hurts = is_sa and (en["sp"][key][0] > 0 or en["sp"][key][1] not in HARMLESS)
        before = en["lp"]
        act = duc_turn(d, en, es, rng, rnd, (is_sa, is_sa and key.startswith("s"), hurts))
        USE[(path, act)].append(before - en["lp"])
        if d.rausch > 0 and act != "furia":
            d.rausch -= 1
        if en["lp"] <= 0:
            return True, rnd, 1 - d.lp / d.max
        step += 1
        if es.get("skip"):
            es["skip"] -= 1
        elif es.get("strom") and rng.random() < 0.25:
            pass
        else:
            bonus, effect, dodge_only = (0, None, False) if not is_sa else en["sp"][key]
            heavy = key.startswith("s") and is_sa
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
                prot, immune, heavy_armor, bite = kb.A[d.armor]
                atk = en["atk"] + bonus + (4 if heavy else 0) + (buff_atk if es.get("buff") else 0)
                atk -= kb.WEAK_MALUS if es.get("geschwaecht") else 0
                atk -= kb.REACH if kb.W[d.weapon][2] == "stange" else 0
                armor = 0 if d.st_.get("erschuettert") or effect == "pierce" else 2 + prot
                dmg = max(1, round(atk) - armor + (kb.EXPOSED_BONUS if d.st_.get("ungedeckt") else 0))
                if effect == "scent" and d.st_.get("blutend"):
                    dmg += 5
                if bite and en["cls"] in ("tier", "monster"):
                    dmg = max(1, round(dmg * (1 - bite)))
                if es.get("blind") or d.halve_next:
                    dmg = max(1, dmg // 2); d.halve_next = False
                if d.st_.get("guard") or d.wind > 0:
                    dmg = max(1, dmg // 2)
                b = d.st_.pop("bonaccia", None)
                if b == "voll":
                    dmg = 0
                elif b == "halb":
                    dmg = max(1, dmg // 2)
                if b and W5_KONTER and (not W_SKALIERUNG or d.wahr >= 4):   # counter needs Wahrnehmung 4
                    c = hit(d, en, es, rng, W5_FAKTOR * (0.5 if b == "halb" else 1.0))
                    en["lp"] -= c
                    USE[(path, "bonaccia")].append(c)
                perf, good = kb.SKILL[skill][tempo]
                f = 1 + 0.03 * d.wahr
                f *= 1.5 if d.st_.get("guard") else 1
                f *= 0.8 if heavy else 1
                f *= 0.9 if heavy_armor else 1
                f *= 0.8 if (d.st_.get("nass") or d.st_.get("geblendet")) else 1
                f *= 0.9 if d.path == "Berserker" else 1               # path quirk: smaller parade window
                f *= M5_FENSTER if d.st_.get("rache") else 1            # charged M5: optionally narrower window
                if es.get("nass"):
                    f *= 1.3 * (1.2 if d.acc == "robbe" else 1)
                perf, good = min(0.95, perf * f), min(0.95, good * f)
                if perf + good > 0.97:
                    good = 0.97 - perf
                rache = d.st_.pop("rache", None)                   # M5 charged: a counter follows this attack
                r = rng.random()
                d.st_.pop("ungedeckt", None)
                if r < perf:
                    dmg = 0
                    stam(d, 1)
                    if not dodge_only and not rache:                # with M5 charged the charged counter replaces it
                        c = hit(d, en, es, rng, proc=True)
                        if kb.W[d.weapon][3] == "counter15":
                            c = int(c * 1.5)
                        en["lp"] -= c
                        es["erschoepft"] = max(es.get("erschoepft", 0), 2)
                        if d.wind > 0:
                            es["erschuettert"] = max(es.get("erschuettert", 0), 2)
                    effect_rounds = 0
                elif r < perf + good:
                    dmg = max(1, dmg // 2); effect_rounds = 1
                else:
                    effect_rounds = 2
                d.lp -= dmg
                if d.path == "Berserker" and dmg > 0:
                    stam(d, 1)                                       # path quirk: +1 stamina when hit
                if rache:                                           # parade made: x1.5 (+burn), x2 against a strong SA
                    geschafft = r < perf + good
                    c = hit(d, en, es, rng, (M5_MULT[1] if heavy else M5_MULT[0]) if geschafft else M5_MULT[2])
                    en["lp"] -= c
                    USE[(path, "retour")].append(c)
                    if geschafft:
                        apply_state(es, en, "brennend")
                        if r < perf:
                            es["erschoepft"] = max(es.get("erschoepft", 0), 2)
                if effect == "drain":
                    en["lp"] = min(en["max"], en["lp"] + dmg)
                if effect and effect_rounds and effect not in immune:
                    if effect in ("brennend", "brennend3"):
                        if "brennend" not in immune:
                            burn_add(d.st_, 2 if effect == "brennend3" else 1)
                    elif effect in ("nass", "blutend", "erschuettert", "strom", "geschwaecht", "geblendet",
                                    "ungedeckt", "betaeubt"):
                        d.st_[effect] = 1 if effect in ("ungedeckt", "betaeubt", "geschwaecht") else effect_rounds
                        if effect == "nass":
                            d.st_.pop("brennend", None); d.st_.pop("burn_new", None)
                    elif effect == "geblendet2":
                        d.st_["geblendet"] = effect_rounds
                    elif effect == "silence":
                        d.st_["silence"] = 2
                    elif effect == "stamina":
                        d.st = max(0, d.st - 1)
                if heavy:
                    es["erschoepft"] = max(es.get("erschoepft", 0), 2)
            if es.get("armor_up"):
                en["armor"] = 1 + level // 3 + armor_up
        if d.wind > 0:
            d.wind -= 1
        en["lp"] -= tick(es, en, d)
        if d.st_.get("brennend"):
            d.lp -= int(BURN_PER_STACK * d.max * d.st_["brennend"])
            if not d.st_.pop("burn_new", None):
                d.st_["brennend"] -= 1
                if d.st_["brennend"] <= 0:
                    d.st_.pop("brennend")
        if d.st_.get("blutend"):
            d.lp -= int(0.05 * d.max)
        for k in list(d.st_):
            if k in ("guard",):
                d.st_.pop(k); continue
            if k in ("nass", "blutend", "erschuettert", "strom", "geblendet", "silence"):
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


def exhausted(es):
    return es.get("erschoepft", 0) > 0 or es.get("blutend", 0) > 0 or (es.get("nass", 0) and es.get("schlamm", 0))


def regeln(v5):
    if v5:
        kb.apply_state, kb.hit, kb.tick, kb.duc_turn, kb.fight, kb.exhausted = apply_state, hit, tick, duc_turn, fight, exhausted
        kb.Duc.__init__ = duc_init
        kb.PATHS = {"Kämpfer": "kraft", "Schmuggler": "list", "Schütze": "wahrnehmung", "Berserker": "mut"}
        kb.GEAR["Berserker"] = dict(kb.GEAR["Kämpfer"])
    else:
        for k, f in ORIG.items():
            setattr(kb, k, f)
        kb.Duc.__init__ = v4.duc_init
        kb.PATHS = {"Kämpfer": "kraft", "Schmuggler": "list", "Schütze": "wahrnehmung"}


def path_rates(path, d_level, skill, n):
    out = []
    for diff in (0, 1, 2):
        v4.STATE["diff"] = diff
        v4.set_gear(d_level)
        lv = d_level + diff
        rng = random.Random(1000 * d_level + 10 * diff + len(path))
        names = kt.ROSTER[kt.tier_for(lv)]
        w = [kb.fight(nm, lv, d_level, path, skill, rng)[0] for nm in names for _ in range(n)]
        out.append(sum(w) / len(w))
    return out


def report(n):
    v4.set_curve(55, 1.10, 19.0, 0.6)                          # curve from docs\wiki\systeme\kampf.md (v4 result)
    v4.CFG.update(gap=0.25, workshop=True, kitchen=True, infuse=True)
    for label, flag in (("v4-Regeln, 3 Pfade (zum Vergleich)", False), ("v5-Regeln, 4 Pfade", True)):
        regeln(flag)
        USE.clear()
        print("\n== %s ==  Sieg %% grün / orange / Totenkopf" % label)
        for skill in ("Normal", "Geübt"):
            print("  %s" % skill)
            for d_level in (3, 5, 7, 9, 10):
                cells = []
                for path in kb.PATHS:
                    r = path_rates(path, d_level, skill, n)
                    cells.append("%-10s %3.0f/%3.0f/%3.0f" % (path, *(x * 100 for x in r)))
                print("    Lv %2d  %s" % (d_level, "  |  ".join(cells)))
        if flag:
            print("\n  Einsatz der Spezialangriffe (alle Läufe oben): Anzahl · Ø Schaden des Zugs")
            names = {"mistral": "K3 Erschütterer", "ressac": "K5 Konterwelle", "libeccio": "K7 Windrüstung",
                     "lame": "K9 Riesenwelle", "doppio": "L3 Doppelschnitt", "sotto": "L5 Abtauchen",
                     "vendetta": "L7 Blutschnitt", "omerta": "L9 Gnadenstoß", "mire": "W3 Zielmarke",
                     "bonaccia": "W5 Ruhepuls", "phare": "W7 Leuchtfeuer", "pluie": "W9 Sternsalve",
                     "scirocco": "M3 Glutschlag", "retour": "M5 Rachefeuer", "furia": "M7 Flammenrausch",
                     "vulcano": "M9 Feuersturm", "attack": "Angriff"}
            for path in kb.PATHS:
                row = []
                for act, nm in names.items():
                    xs = USE.get((path, act))
                    if xs and (nm[0] == path[0] or act == "attack" or (path == "Schmuggler" and nm[0] == "L")
                               or (path == "Schütze" and nm[0] == "W") or (path == "Berserker" and nm[0] == "M")):
                        row.append("%s %d · %.0f" % (nm, len(xs), statistics.mean(xs)))
                print("   %-10s %s" % (path, " | ".join(row)))


POINTS = {3: 1, 5: 2, 7: 3, 9: 4, 10: 6}        # free choice: 1 skill point at Lv 3/5/7/9, 2 at Lv 10


def all_builds(points):
    """Every legal mix: depth per path (a tier needs the one below), depths add up to the points."""
    out = []
    for k in range(5):
        for l in range(5):
            for w in range(5):
                m = points - k - l - w
                if 0 <= m <= 4:
                    out.append({"K": k, "L": l, "W": w, "M": m})
    return out


def build_name(dp):
    return " ".join("%s%d" % (p, n) for p, n in dp.items() if n) or "-"


def build_report(n):
    """Mixed builds at Lv 7 / 9 / 10, Normal player. Main path = deepest path (decides weapon, quirk, attribute)."""
    v4.set_curve(55, 1.10, 19.0, 0.6)
    v4.CFG.update(gap=0.25, workshop=True, kitchen=True, infuse=True)
    regeln(True)
    for d_level in (7, 9, 10):
        rows = []
        for dp in all_builds(POINTS[d_level]):
            main = PATH_OF[max(dp, key=lambda p: (dp[p], "MKLW".index(p) * -1))]
            r = path_rates((main, build_skills(dp)), d_level, "Normal", n)
            rows.append((statistics.mean(r), r, dp, main))
        rows.sort(key=lambda x: -x[0])
        rein = [x for x in rows if max(x[2].values()) == min(4, POINTS[d_level]) and
                sum(1 for v in x[2].values() if v) == (1 if POINTS[d_level] <= 4 else 2)]
        print("\n== Lv %d · %d Skillpunkte · %d Builds · Normal, Sieg %% grün/orange/Totenkopf (Ø)" %
              (d_level, POINTS[d_level], len(rows)))
        print("  stärkste:")
        for s, r, dp, main in rows[:8]:
            print("    %-16s Haupt %-10s %3.0f/%3.0f/%3.0f  (Ø %2.0f)" % (build_name(dp), main, *(x * 100 for x in r), s * 100))
        print("  schwächste:")
        for s, r, dp, main in rows[-4:]:
            print("    %-16s Haupt %-10s %3.0f/%3.0f/%3.0f  (Ø %2.0f)" % (build_name(dp), main, *(x * 100 for x in r), s * 100))
        print("  reine Pfade (bis zum Finale):")
        for s, r, dp, main in rein[:12]:
            print("    %-16s %3.0f/%3.0f/%3.0f  (Ø %2.0f, Rang %d von %d)" % (build_name(dp), *(x * 100 for x in r), s * 100,
                                                                        rows.index((s, r, dp, main)) + 1, len(rows)))


if __name__ == "__main__":
    build_report(N) if "--builds" in ARGS else report(N)
