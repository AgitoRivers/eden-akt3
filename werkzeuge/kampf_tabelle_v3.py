# -*- coding: utf-8 -*-
r"""Calibrate a per-level enemy table (LP, attack) for kampf_balance_v3.py against the threat-colour targets
(20.10.2026). Coordinate descent over levels 1-12; every Duc level 1-10 fights level +0 / +1 / +2 enemies.

    python kampf_tabelle_v3.py            prints the table and the resulting win rates
"""
import json, os, random, statistics, sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.argv = [sys.argv[0]]
import kampf_balance_v3 as kb  # noqa: E402

N = 50
TARGET = {("Normal", 0): 0.85, ("Normal", 1): 0.55, ("Normal", 2): 0.20,
          ("Geübt", 0): 0.97, ("Geübt", 1): 0.85, ("Geübt", 2): 0.50}
LP = {lv: 40 + 10 * lv for lv in range(1, 13)}
ATK = {lv: 11.0 + 1.2 * lv for lv in range(1, 13)}


def tier_for(level):
    return "lästig" if level <= 3 else "gefährlich" if level <= 6 else "tödlich" if level <= 8 else "albtraum"


def stats(name, level):
    el, cls, _tier, _lv, specials = kb.E[name]
    tier = tier_for(level)
    sp = specials if kb.E[name][2] == tier else {}
    return {"name": name, "el": el, "cls": cls, "tier": tier, "lp": int(LP[level]), "max": int(LP[level]),
            "atk": ATK[level], "armor": 1 + level // 3, "sp": sp}


kb.enemy_stats = stats
ROSTER = {t: [x for x in kb.E if kb.E[x][2] == t] for t in ("lästig", "gefährlich", "tödlich", "albtraum")}


def cell(d_level, diff, skill, n=N):
    lv = d_level + diff
    names = ROSTER[tier_for(lv)]
    rng = random.Random(d_level * 100 + diff * 10 + (skill == "Geübt"))
    wins = []
    for path in kb.PATHS:
        for name in names:
            res = [kb.fight(name, lv, d_level, path, skill, rng)[0] for _ in range(max(4, n // len(names)))]
            wins.append(sum(res) / len(res))
    return statistics.mean(wins)


def error_for(level):
    err = 0
    for diff in (0, 1, 2):
        d_level = level - diff
        if 1 <= d_level <= 10:
            for skill in ("Normal", "Geübt"):
                err += (cell(d_level, diff, skill) - TARGET[(skill, diff)]) ** 2
    return err


for sweep in range(4 if __name__ == "__main__" else 0):
    for lv in range(1, 13):
        best = (error_for(lv), LP[lv], ATK[lv])
        for f_lp in (0.8, 0.9, 1.1, 1.25):
            for d_atk in (-2, -1, 0, 1, 2):
                old = LP[lv], ATK[lv]
                LP[lv], ATK[lv] = int(old[0] * f_lp), old[1] + d_atk
                e = error_for(lv)
                if e < best[0]:
                    best = (e, LP[lv], ATK[lv])
                LP[lv], ATK[lv] = old
        LP[lv], ATK[lv] = best[1], best[2]
    print("sweep %d: %s" % (sweep, ", ".join("%d:%d/%.0f" % (l, LP[l], ATK[l]) for l in LP)))

if __name__ == "__main__":
    json.dump({"lp": LP, "atk": ATK}, open(os.path.join(HERE, "kampf_tabelle_v3.json"), "w"), indent=1)
    print("\nWin rates (Normal | Geübt) for Duc level vs enemy +0 / +1 / +2:")
    for d_level in range(1, 11):
        row = []
        for skill in ("Normal", "Geübt"):
            row.append(" ".join("%3.0f%%" % (cell(d_level, diff, skill, 150) * 100) for diff in (0, 1, 2)))
        print("  Lv %2d   %s   |   %s" % (d_level, row[0], row[1]))
