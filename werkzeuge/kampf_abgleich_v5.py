# -*- coding: utf-8 -*-
r"""Engine vs simulation (stage 4a, 24.10.2026): checks kern\kampf.py against werkzeuge\kampf_balance_v5.py.

  1. single hits: the same weapon, enemy and state in both - damage must be identical (no crit)
  2. win rates: a simple bot plays the engine with the simulation's parade odds ("Normal") against the act-1 enemies
     at Duc's level +0 / +1 / +2 - plausibility only (other roster, simpler player than the simulation)

    python werkzeuge\kampf_abgleich_v5.py [--n 200]
"""
import copy, json, os, random, statistics, sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(HERE)
sys.path.insert(0, EDEN)
sys.path.insert(0, HERE)
N = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 200
ARGV = list(sys.argv)
from kern import kampf, zustand  # noqa: E402
import kampf_balance_v5 as v5  # noqa: E402
sys.argv = ARGV

MODDIR = os.path.join(EDEN, "module", "eden_rise")
MODUL = json.load(open(os.path.join(MODDIR, "modul.json"), encoding="utf-8"))
DEFS = kampf.daten(MODDIR)
kb = v5.kb


class NoCrit:
    def random(self):
        return 0.99

    def randint(self, a, b):
        return 10


def fresh(level=1, weapon="faust", armor=None, attrs=None, skills=(), bid="hafen_dieb_test", defs=DEFS):
    z = zustand.neu(MODUL)
    p = copy.deepcopy(MODUL["personas"][0])
    p["attribute"].update(attrs or {})
    zustand.persona_setzen(z, MODUL, p)
    kampf.test_setup(z, defs, level=level, skills=list(skills), weapon=weapon, armor=armor or "")
    kampf.starten(z, defs, bid, rng=NoCrit())
    return z


# ------------------------------------------------------------------ 1. single hits
def single_hits():
    v5.regeln(True)
    rows, bad = [], 0
    cases = [("faust", "taschendieb", {}, {}), ("feuerwehraxt", "taschendieb", {}, {}),
             ("tauchermesser", "fackelpirat", {"cunning": 4}, {}), ("schraubenschluessel", "moewe", {}, {}),
             ("rosis_flammenschwert", "pirat", {"strength": 4}, {"erschoepft": 2}),
             ("legionaersmesser", "ratte", {"cunning": 3}, {"erschoepft": 2}),
             ("spitzhacke", "maxwell", {"strength": 3}, {"erschuettert": 2})]
    for wid, eid, attrs, states in cases:
        defs = copy.deepcopy(DEFS)
        b = dict(copy.deepcopy(defs["encounters"]["hafen_dieb_test"]), enemy=eid, level=4)
        defs["encounters"]["abgleich"] = b
        z = fresh(4, wid, attrs=attrs, bid="abgleich", defs=defs)
        k = z["kampf"]
        g, sp = k["gegner"][0], k["spieler"]
        g["states"].update(states)
        c = kampf._ctx(k, NoCrit())
        before = g["lp"]
        kampf._hit(c)
        engine = before - g["lp"]
        w = defs["weapons"][wid]
        kb.W["_x"] = (w["dmg"], w["element"], w["kind"], None)
        d = kb.Duc.__new__(kb.Duc)
        d.kraft, d.mut, d.list, d.wahr = sp["attrs"]["strength"], sp["attrs"]["courage"], sp["attrs"]["cunning"], 3
        d.path, d.weapon, d.acc, d.st_, d.sure_crit, d.rausch, d.hits = "Kämpfer", "_x", None, {}, False, 0, 0
        en = {"cls": g["def"]["cls"], "el": g["def"]["element"], "armor": g["armor"], "max": g["lp_max"], "tier": "x"}
        es = dict(states)
        rng = random.Random(0)
        rng.random = lambda: 0.99
        sim = kb.hit(d, en, es, rng)
        rows.append("  %-22s gegen %-12s %-16s Engine %3d  Simulation %3d  %s" % (
            w["label"][:22], g["name"], ",".join(states) or "-", engine, sim, "ok" if engine == sim else "ABWEICHUNG"))
        bad += engine != sim
    print("1. Einzeltreffer (ohne Krit, Duc Lv 4, Gegner Lv 4):")
    print("\n".join(rows))
    print("   %s" % ("alle gleich" if not bad else "%d Abweichungen" % bad))


# ------------------------------------------------------------------ 2. win rates with a simple bot
PERF_GOOD = {"leicht": (0.35, 0.45), "mittel": (0.25, 0.45), "stark": (0.15, 0.40)}   # simulation "Normal"
PRIORITY = ["vulcano", "lame_de_fond", "omerta", "pluie_d_etoiles", "bonaccia", "phare", "retour", "ressac",
            "sotto_voce", "libeccio", "point_de_mire", "vendetta", "furia", "mistral", "scirocco", "doppio_gioco"]
GEAR = {"K": "schraubenschluessel", "L": "tauchermesser", "W": "sportbogen", "M": "schraubenschluessel"}
GEAR_S = {"K": "feuerwehraxt", "L": "legionaersmesser", "W": "doppelflinte", "M": "feuerwehraxt"}


def bot_choice(z):
    k = z["kampf"]
    sp, g = k["spieler"], k["gegner"][0]
    if kampf.must_skip(sp):
        return "aussetzen", None
    infos = {f["id"]: f for f in kampf.faehigkeiten(z) if not f["gesperrt"]}
    it = g["intents"][g["absicht"]]
    sa_hurts = kampf.is_special(g["absicht"]) and kampf.hurts(it)
    for sid in PRIORITY:
        f = infos.get(sid)
        if not f or f.get("hinweis"):
            continue
        if sid == "vulcano" and g["states"].get("brennend", 0) < 4 and g["lp"] > 0.3 * g["lp_max"]:
            continue
        if sid in ("bonaccia", "phare", "retour", "ressac", "sotto_voce") and not sa_hurts:
            continue
        if sid == "retour" and sp["lp"] < sp["lp_max"] / 2:
            continue
        if sid == "mistral" and g["states"].get("erschuettert"):
            continue
        if sid == "point_de_mire" and (kampf.exhausted(g) or (k["runde"] % 3 != 1 and not infos.keys() & {"lame_de_fond", "omerta"})):
            continue                                            # like the simulation: every third round or for a finale
        return "faehigkeit", sid
    if sa_hurts and sp["ausdauer"] < 3 and sp.get("rausch", 0) <= 0:
        return "verteidigen", None
    return "angriff", None


def parade_result(k, rng):
    p = k["parade"]
    perf, good = PERF_GOOD[p["tempo"]]
    f = p["fenster"]["faktor"]
    perf, good = min(0.95, perf * f), min(0.95, good * f)
    if perf + good > 0.97:
        good = 0.97 - perf
    r = rng.random()
    if p["nur_ausweichen"]:
        return "ausweichen" if r < perf + good else "verfehlt"
    return "perfekt" if r < perf else "gut" if r < perf + good else "verfehlt"


def fight(level, path, eid, diff, rng):
    defs = copy.deepcopy(DEFS)
    defs["encounters"]["abgleich"] = dict(copy.deepcopy(defs["encounters"]["hafen_dieb_test"]), enemy=eid,
                                          level=level + diff, flee_allowed=False)
    skills = [s for s, d in defs["specials"].items() if d["path"] == path and d["tier"] <= level]
    weapon = GEAR[path] if level <= 2 else GEAR_S[path]
    z = fresh(level, weapon, "lederjacke", skills=skills, bid="abgleich", defs=defs)
    z["inventar"] = ["verbandskasten"]
    rounds = 0
    while not z["kampf"]["ergebnis"] and rounds < 40:
        rounds += 1
        k = z["kampf"]
        sp = k["spieler"]
        if sp["lp"] < 0.35 * sp["lp_max"] and "verbandskasten" in z["inventar"]:
            cmd, target = "gegenstand", "verbandskasten"
        else:
            cmd, target = bot_choice(z)
        kampf.zug(z, MODUL, cmd, target, rng=rng)
        if z["kampf"]["phase"] == "parade":
            kampf.parade_aufloesen(z, MODUL, parade_result(z["kampf"], rng), rng=rng)
    return (z["kampf"]["ergebnis"] or {}).get("art") in ("ko", "aufgabe")


def win_rates(n):
    print("\n2. Siegquote eines einfachen Bots in der Engine (Parade „Normal“ wie die Simulation), Gegner Akt 1,")
    print("   Gegnerlevel = Duc +0 / +1 / +2 (grün / orange / Totenkopf), ohne Werkstatt und Küche:")
    roster = {"laestig": ["taschendieb", "ratte", "pirat", "moewe"], "gefaehrlich": ["fackelpirat", "maxwell"]}
    for level in (1, 3, 5):
        cells = []
        for path in "KLWM":
            rates = []
            for diff in (0, 1, 2):
                tier = "laestig" if level + diff <= 3 else "gefaehrlich"
                rng = random.Random(100 * level + 10 * diff + "KLWM".index(path))
                wins = [fight(level, path, e, diff, rng) for e in roster[tier] for _ in range(max(1, n // len(roster[tier])))]
                rates.append(100 * sum(wins) / len(wins))
            cells.append("%s %3.0f/%3.0f/%3.0f" % (kampf.PATH_NAME[path][:7], *rates))
        print("   Lv %d  %s" % (level, "  |  ".join(cells)))
    print("   Ziel laut Doku ≈ 85 / 55 / 20; Simulation v5 Lv 3: K 100/79/48 · L 100/85/60 · W 99/58/26 · M 99/81/54")


if __name__ == "__main__":
    single_hits()
    win_rates(N)
