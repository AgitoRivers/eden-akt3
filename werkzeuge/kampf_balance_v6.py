# -*- coding: utf-8 -*-
r"""Jacken-Balance v6 (24.10.2026): setzt auf v5 (Level, 4 Pfade, 16 Spezialangriffe, Brennen) auf und prueft die fuenf
Jacken mit ihren festen Eigenschaften. Nicht von der Engine benutzt - liefert Zahlen fuer docs\wiki\systeme\aufruestung.md.

Jacken (Schutz je Akt: Akt 1 = 2, Akt 2 = 3 (Stufe 1), Akt 3 = 4 (Stufe 2); Cyber 5):
  terra      Terra Scura  Standfest:  Verteidigen gibt in der Runde Schutz +2, Duc wird nie erschuettert
  meramie    Meramie      Fliessend:  Parade-Fenster +10 %, Konter nach perfekter Parade x1,25
  incendio   Incendio     Glut:       Duc schlaegt je Brandstufe am Gegner +1 staerker
  zephyr     Zephyr       Leicht:     Ausdauer-Maximum +1 (Start voll)
  citadelle  Citadelle    Alles-in-einem: erster Treffer pro Kampf nur halb, Parade-Fenster -10 % (schwere Ruestung), Schutz 5

    python kampf_balance_v6.py            Tabelle je Gegner (Sieg % und Ø Verlust an LP), Zusammenfassung, Urteil
    python kampf_balance_v6.py --n 120    mehr Kaempfe je Zelle
"""
import inspect, os, random, statistics, sys, zlib

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ARGS = list(sys.argv)
N = int(ARGS[ARGS.index("--n") + 1]) if "--n" in ARGS else 80
sys.argv = [sys.argv[0]]
import kampf_balance_v5 as v5  # noqa: E402

v4, kb, kt = v5.v4, v5.kb, v5.kt
JACKETS = ["terra", "meramie", "incendio", "zephyr", "citadelle"]
NAMES = {"terra": "Terra Scura", "meramie": "Meramie", "incendio": "Incendio", "zephyr": "Zéphyr", "citadelle": "Citadelle"}
PATHS = ["Kämpfer", "Schmuggler", "Schütze", "Berserker"]


def knob(name, std):
    return float(ARGS[ARGS.index("--" + name) + 1]) if "--" + name in ARGS else std


K = {"terra_prot": knob("terra-prot", 0.0), "terra_guard": knob("terra-guard", 2.0),
     "mer_fenster": knob("mer-fenster", 1.10), "mer_konter": knob("mer-konter", 1.25),
     "zeph_st": int(knob("zeph-st", 1)), "glut": knob("glut", 1.0),
     "cit_prot": int(knob("cit-prot", 5)), "cit_first": knob("cit-first", 0.5)}
CUR = {"jacket": "terra"}


def prot_for(level):
    return 2 if level <= 4 else 3 if level <= 7 else 4          # Akt 1 / Akt 2 (Stufe 1) / Akt 3 (Stufe 2)


def jackets(p):
    out = {j: (p, set(), False, 0) for j in JACKETS}
    out["terra"] = (p + K["terra_prot"], set(), False, 0)
    out["citadelle"] = (K["cit_prot"], set(), True, 0)                      # Cyber: eigener Wert, schwere Ruestung (Fenster -10 %)
    return out


# ------------------------------------------------------------------ Eigenschaften in die v5-Simulation haengen
v5.regeln(True)
v4.set_curve(55, 1.10, 19.0, 0.6)
v4.CFG.update(gap=0.25, workshop=True, kitchen=True, infuse=True)

ORIG_HIT = v5.hit


def hit_v6(d, en, es, rng, factor=1.0, extra=0, *a, **k):
    if getattr(d, "armor", None) == "incendio":                  # Glut: +1 je Brandstufe am Gegner
        extra += round(es.get("brennend", 0) * K["glut"])
    return ORIG_HIT(d, en, es, rng, factor, extra, *a, **k)


v5.hit = kb.hit = hit_v6

src = inspect.getsource(v5.fight)
PATCH = [
    ('armor = 0 if d.st_.get("erschuettert") or effect == "pierce" else 2 + prot',
     'armor = 0 if (d.st_.get("erschuettert") and d.armor != "terra") or effect == "pierce" else '
     '2 + prot + (%s if (d.armor == "terra" and d.st_.get("guard")) else 0)' % K["terra_guard"]),
    ('if effect and effect_rounds and effect not in immune:',
     'if effect and effect_rounds and effect not in immune and not (effect == "erschuettert" and d.armor == "terra"):'),
    ('f *= 0.9 if heavy_armor else 1',
     'f *= 0.9 if heavy_armor else 1\n                f *= %s if d.armor == "meramie" else 1' % K["mer_fenster"]),
    ('c = hit(d, en, es, rng, proc=True)',
     'c = hit(d, en, es, rng, %s if d.armor == "meramie" else 1.0, proc=True)' % K["mer_konter"]),
    ('                d.lp -= dmg\n',
     ('                if d.armor == "citadelle" and not getattr(d, "_c1", False):\n'
      '                    dmg = max(1, int(dmg * %s)); d._c1 = True\n' % K["cit_first"])
     + '                d.lp -= dmg\n'),
]
for alt, neu in PATCH:
    if src.count(alt) != 1:
        raise SystemExit("Patch passt nicht (%d x): %s" % (src.count(alt), alt[:60]))
    src = src.replace(alt, neu)
exec(compile(src, "fight_v6", "exec"), v5.__dict__)
kb.fight = v5.fight

_init = kb.Duc.__init__


def init_v6(self, level, path, skill):
    _init(self, level, path, skill)
    self.armor = CUR["jacket"]
    if self.armor == "zephyr":                                   # Leicht: Ausdauer-Maximum +1
        self.st_max += K["zeph_st"]
        self.st = self.st_max


kb.Duc.__init__ = init_v6


def run(enemy, jacket, n):
    level = kb.E[enemy][3]
    v4.STATE["diff"] = 0
    v4.set_gear(level)
    kb.A.clear()
    kb.A.update(jackets(prot_for(level)))
    CUR["jacket"] = jacket
    rng = random.Random(zlib.crc32(enemy.encode()))
    wins, loss = [], []
    for path in PATHS:
        for _ in range(max(1, n // len(PATHS))):
            w, _r, l = kb.fight(enemy, level, level, path, "Normal", rng)
            wins.append(w)
            loss.append(l)
            BYPATH.setdefault((jacket, path), []).append(l)
            BYCLASS.setdefault((jacket, kb.E[enemy][1]), []).append(l)
    return sum(wins) / len(wins), statistics.mean(loss)


BYPATH, BYCLASS = {}, {}


def kurz(enemies, res):
    """Kurzansicht: Ø Verlust je Jacke (alle, nach Pfad, nach Gegnerart) - nur Lederjacken und Citadelle ab Level 8."""
    print("Ø LP-Verlust in %% (kleiner ist besser), alle Gegner, Level 1–10:")
    for j in JACKETS[:4]:
        p = "  ".join("%s %2.0f" % (pa[:3], 100 * statistics.mean(BYPATH[(j, pa)])) for pa in PATHS)
        c = "  ".join("%s %2.0f" % (cl[:4], 100 * statistics.mean(BYCLASS[(j, cl)]))
                      for cl in ("mensch", "tier", "flieger", "monster", "maschine"))
        print("  %-12s Ø %2.0f | Pfad: %s | Art: %s" % (NAMES[j], 100 * statistics.mean(res[e][j][1] for e in enemies), p, c))
    sel = [e for e in enemies if kb.E[e][3] >= 8]
    print("  Level 8+: " + " | ".join("%s %.0f" % (NAMES[j], 100 * statistics.mean(res[e][j][1] for e in sel))
                                      for j in JACKETS))
    ms = {j: statistics.mean(res[e][j][1] for e in enemies) for j in JACKETS[:4]}
    print("  Abstand beste/schlechteste Lederjacke: %.1f Punkte" % ((max(ms.values()) - min(ms.values())) * 100))


def main():
    enemies = sorted(kb.E, key=lambda e: (kb.E[e][3], e))
    res = {e: {j: run(e, j, N) for j in JACKETS} for e in enemies}
    if "--kurz" in ARGS:
        kurz(enemies, res)
        return
    print("Jacken-Balance v6 · %d Kämpfe je Zelle (4 Pfade, Normal), Gegner auf Ducs Level" % N)
    print("Zahl = Ø Verlust an LP in %% (kleiner ist besser) · in Klammern Sieg %%\n")
    print("  %-15s %-8s %-9s Lv  %s" % ("Gegner", "Art", "Element", "".join("%-17s" % NAMES[j] for j in JACKETS)))
    best_count = {j: 0 for j in JACKETS}
    for e in enemies:
        el, cls, tier, lv, _ = kb.E[e]
        row = res[e]
        leather = {j: row[j][1] for j in JACKETS[:4]}
        best = min(leather.values())
        cells = []
        for j in JACKETS:
            mark = "*" if j in leather and leather[j] <= best + 0.02 else " "
            cells.append("%s%4.0f (%3.0f)      " % (mark, row[j][1] * 100, row[j][0] * 100))
            if mark == "*":
                best_count[j] += 1
        print("  %-15s %-8s %-9s %2d  %s" % (e, cls, el or "-", lv, "".join(cells)))
    print("\n  * = beste Lederjacke bei diesem Gegner (bis 2 Punkte Abstand zählt als gleichauf)")
    print("\nZusammenfassung (Ø über alle Gegner; Citadelle nur ab Level 8, vergleichbar mit den Jacken ab Level 8):")
    for label, sel in (("alle Gegner", enemies), ("Level 1–4 (Akt 1)", [e for e in enemies if kb.E[e][3] <= 4]),
                       ("Level 5–7 (Akt 2)", [e for e in enemies if 5 <= kb.E[e][3] <= 7]),
                       ("Level 8+ (Akt 3)", [e for e in enemies if kb.E[e][3] >= 8])):
        if not sel:
            continue
        line = []
        for j in JACKETS:
            if j == "citadelle" and label in ("alle Gegner", "Level 1–4 (Akt 1)", "Level 5–7 (Akt 2)"):
                continue
            line.append("%s Verlust %.0f%% Sieg %.0f%%" % (NAMES[j], 100 * statistics.mean(res[e][j][1] for e in sel),
                                                          100 * statistics.mean(res[e][j][0] for e in sel)))
        print("  %-20s %s" % (label, " | ".join(line)))
    print("\nBeste Lederjacke bei: " + ", ".join("%s %d von %d Gegnern" % (NAMES[j], best_count[j], len(enemies))
                                                  for j in JACKETS[:4]))
    ms = {j: statistics.mean(res[e][j][1] for e in enemies) for j in JACKETS[:4]}
    spread = (max(ms.values()) - min(ms.values())) * 100
    print("Abstand zwischen bester und schlechtester Lederjacke im Ø: %.1f Punkte LP-Verlust" % spread)


if __name__ == "__main__":
    main()
