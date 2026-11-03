# -*- coding: utf-8 -*-
r"""Overall balance v4 (21.10.2026): v3 (levels, paths, states, enemy specials) + Duc growth (LP +5 per level,
stamina 7 from Lv 5 / 8 from Lv 9) + level gap + Schütze fixes + Rosi's workshop (+1/+2/+3 with master perk,
element infusion) + a cooking buff. Compares "without" and "with" workshop/kitchen and refits the enemy curve.

    python kampf_balance_v4.py
"""
import itertools, random, statistics, sys, os

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.argv = [sys.argv[0]]
import kampf_balance_v3 as kb  # noqa: E402
import kampf_tabelle_v3 as kt  # noqa: E402

TARGET = kt.TARGET
BASE_W = dict(kb.W)
BASE_A = dict(kb.A)
CFG = {"gap": 0.2, "workshop": False, "kitchen": False, "infuse": False}
STATE = {"diff": 0}

# Schütze fixes from the v3 round
kb.PLUIE, kb.MIRE_ROUNDS = 0.85, 3
BASE_W["elektro_harpune"] = (9, "luft", "fern", "first_strom")
BASE_W["doppelflinte"] = (7, "feuer", "fern", None)
kb.WEAK["fern"] = set()

_init = kb.Duc.__init__


def upgrade_level(level):
    return 0 if level <= 2 else 1 if level <= 5 else 2 if level <= 8 else 3


def duc_init(self, level, path, skill):
    _init(self, level, path, skill)
    self.max = 36 + 5 * (level - 1)
    self.st = kb.STAMINA + (1 if level >= 5 else 0) + (1 if level >= 9 else 0)
    if CFG["kitchen"]:                     # a combat dish the evening before: path attribute +1, Max-LP +4
        self.max += 4
        if path == "Kämpfer":
            self.kraft = min(5, self.kraft + 1)
        elif path == "Schmuggler":
            self.list = min(5, self.list + 1)
        else:
            self.wahr = min(5, self.wahr + 1)
    self.lp = self.max


kb.Duc.__init__ = duc_init
_stats = kt.stats


def stats(name, level):
    s = _stats(name, level)
    f = 1 + CFG["gap"] * STATE["diff"]
    s["lp"] = s["max"] = int(s["lp"] * f)
    s["atk"] *= f
    return s


kb.enemy_stats = stats


def set_gear(d_level):
    u = upgrade_level(d_level) if CFG["workshop"] else 0
    kb.W.clear()
    for k, (dmg, el, t, sig) in BASE_W.items():
        kb.W[k] = (dmg + u, el, t, sig)
    kb.A.clear()
    for k, (prot, imm, heavy, bite) in BASE_A.items():
        kb.A[k] = (prot + u, imm, heavy, bite)
    # master perk (+3): crit +5 % for all paths as a simple stand-in; infusion: no element disadvantage
    kb.CRIT_BASE = 0.05 + (0.05 if CFG["workshop"] and u == 3 else 0)
    kb.ELEM_DIS = 1.0 if CFG["infuse"] else 0.85


def cell(d_level, diff, skill, n):
    STATE["diff"] = diff
    set_gear(d_level)
    return kt.cell(d_level, diff, skill, n)


def set_curve(a, g, c, d):
    for lv in range(1, 13):
        kt.LP[lv] = int(a * g ** lv)
        kt.ATK[lv] = c + d * lv


def table(label, n=120):
    print("\n== %s ==" % label)
    print("Sieg (Normal: grün orange Totenkopf | Geübt: grün orange Totenkopf)")
    for d_level in range(1, 11):
        row = [" ".join("%3.0f%%" % (cell(d_level, diff, skill, n) * 100) for diff in (0, 1, 2))
               for skill in ("Normal", "Geübt")]
        print("  Lv %2d   %s   |   %s" % (d_level, row[0], row[1]))


def per_path(n=60):
    print("\nPro Pfad (Normal, grün/orange/Totenkopf):")
    for d_level in (3, 6, 9, 10):
        out = []
        for path in kb.PATHS:
            vals = []
            for diff in (0, 1, 2):
                STATE["diff"] = diff
                set_gear(d_level)
                lv = d_level + diff
                rng = random.Random(7)
                w = [kb.fight(nm, lv, d_level, path, "Normal", rng)[0] for nm in kt.ROSTER[kt.tier_for(lv)] for _ in range(n)]
                vals.append(sum(w) / len(w))
            out.append("%s %s" % (path[:6], "/".join("%2.0f" % (v * 100) for v in vals)))
        print("  Lv %2d  %s" % (d_level, "  |  ".join(out)))


def error(n):
    e = 0
    for d_level in range(1, 11):
        for diff in (0, 1, 2):
            for skill in ("Normal", "Geübt"):
                e += (cell(d_level, diff, skill, n) - TARGET[(skill, diff)]) ** 2
    return e


if __name__ == "__main__":
    set_curve(50, 1.10, 15.0, 0.6)
    table("A) alte Kurve, OHNE Werkstatt und Küche")
    CFG.update(workshop=True, kitchen=True, infuse=True)
    table("B) alte Kurve, MIT Werkstatt (+1/+2/+3, Perk, Veredeln) und Kampfgericht")
    best = None
    for a, g, c, d, gap in itertools.product((55, 65, 75), (1.10, 1.13), (15.0, 17.0, 19.0), (0.6, 1.0), (0.2, 0.25)):
        set_curve(a, g, c, d)
        CFG["gap"] = gap
        e = error(16)
        if best is None or e < best[0]:
            best = (e, a, g, c, d, gap)
            print("best %.3f a=%s g=%s c=%s d=%s gap=%s" % best)
    _, a, g, c, d, gap = best
    set_curve(a, g, c, d)
    CFG["gap"] = gap
    print("\nNeue Kurve:")
    print("Level:  " + " ".join("%5d" % lv for lv in range(1, 13)))
    print("LP:     " + " ".join("%5d" % kt.LP[lv] for lv in range(1, 13)))
    print("Angriff:" + " ".join("%5.0f" % kt.ATK[lv] for lv in range(1, 13)))
    table("C) NEUE Kurve, MIT Werkstatt und Küche")
    per_path()
    CFG.update(workshop=False, kitchen=False, infuse=False)
    table("D) NEUE Kurve, aber OHNE Werkstatt und Küche (wer sie ignoriert)")
