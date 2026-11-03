# -*- coding: utf-8 -*-
r"""Chip-Balance (25.10.2026): misst, wie stark jede Erweiterungs-Familie im ECHTEN Kampf (kern\kampf.py) ist - mit Spezialangriffen.

Ein Bot spielt die echte Engine: Spezialangriff, wenn einer geht (hoechster Schaden), sonst Heftiger Angriff oder Angriff,
verteidigt bei wenig Leben; die Parade wird nach der Fenstergroesse des Kampfes gewuerfelt. Je Pfad (Kaempfer K, Schmuggler L,
Schuetze W, Berserker M) und Akt (Level 3 / 6 / 9, Rosis Stufe 0 / 1 / 2, Chip-Stufe 1 / 2 / 3) laeuft eine Basis ohne Chips und
jede Familie einzeln (Chip auf passender Waffe oder Jacke) gegen fuenf Gegner des Spiels. Gemessen werden Siegquote und LP-Verlust.

    python kampf_balance_chips.py                 volle Tabelle (dauert, nutzt alle Kerne)
    python kampf_balance_chips.py --n 6           weniger Kaempfe je Gegner
    python kampf_balance_chips.py --kombi         zusaetzlich die staerksten Mehr-Chip-Builds je Pfad und Akt
"""
import copy, json, multiprocessing as mp, os, random, statistics, sys, time

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(HERE)
sys.path.insert(0, EDEN)
from kern import kampf, zustand  # noqa: E402

MODDIR = os.path.join(EDEN, "module", "eden_rise")
MODUL = json.load(open(os.path.join(MODDIR, "modul.json"), encoding="utf-8"))
DEFS = copy.deepcopy(kampf.daten(MODDIR))
ARGS = sys.argv[1:]
if os.environ.get("EDEN_CHIP_TUNE"):                    # Varianten testen: {"id": {"stat": ..., "wert": ...}} ueberschreibt die Wirkung
    for _id, _w in json.loads(os.environ["EDEN_CHIP_TUNE"]).items():
        DEFS["erweiterungen"][_id]["wirkung"].update(_w)
N = int(ARGS[ARGS.index("--n") + 1]) if "--n" in ARGS else 10
ENEMIES = ["pirat", "fackelpirat", "keiler", "moewe", "hund_alpha"]
PATHS = {"K": ("bat", "K"), "L": ("knife", "L"), "W": ("gun", "W"), "M": ("spear", "M")}
LEVELS = {3: (0, 1), 6: (1, 2), 9: (2, 3)}               # Duc level -> (Rosi's level, chip level)
FAMILIEN = []
for _e in DEFS["erweiterungen"].values():
    if _e["stufe"] == 1:
        FAMILIEN.append((_e["familie"], _e["gruppe"], _e["kategorie"]))


def codes(path, level):
    tiers = ["%s%d" % (path, t) for t in (3, 5, 7, 9)]
    return tiers[:kampf.skill_points(level)]


def aufbau(path, level, chips, seed):
    waffe, p = PATHS[path]
    rosi, _ = LEVELS[level]
    z = zustand.neu(MODUL)
    pers = copy.deepcopy(MODUL["personas"][0])
    zustand.persona_setzen(z, MODUL, pers)
    kampf.test_setup(z, DEFS, level=level, skills=kampf.by_code(DEFS, codes(p, level)), weapon=waffe, armor="jacket_earth")
    kampf.werkstatt(z)["stufen"]["weapon:" + waffe] = rosi
    kampf.werkstatt(z)["stufen"]["armor:jacket_earth"] = rosi
    pool, plaetze = kampf.chip_pool(z)["pool"], kampf.chip_pool(z)["plaetze"]
    for familie, stufe, ziel in chips:
        pool[familie] = stufe
        plaetze.setdefault(ziel, []).append(familie)
    return z


def parade_wurf(k, rng):
    if k["parade"].get("nur_ausweichen"):                 # dodge-only strikes (gull dive): dodge or take it
        return "ausweichen" if rng.random() < 0.55 else "verfehlt"
    fe = k["parade"]["fenster"]
    p_perf = min(0.6, fe["perf"] / 400)
    p_gut = min(0.9 - p_perf, max(0, (fe["gut"] - fe["perf"]) / 300))
    r = rng.random()
    return "perfekt" if r < p_perf else "gut" if r < p_perf + p_gut else "verfehlt"


def waehlen(z, rng):
    k = z["kampf"]
    sp = k["spieler"]
    if sp["lp"] < sp["lp_max"] * 0.3 and kampf.pruefen(z, MODUL, "verteidigen") is None and rng.random() < 0.5:
        return "verteidigen", None
    fs = [f for f in kampf.skills_view(z, k) if not f["gesperrt"]]
    spezial = [f for f in fs if f["art"] == "spezial"]
    if spezial:
        f = max(spezial, key=lambda x: (x.get("schaden") or 0, x["kosten"]))
        return "faehigkeit", f["id"]
    if any(f["id"] == "mistral" for f in fs) and sp["ausdauer"] >= sp["ausdauer_max"] - 1:
        return "faehigkeit", "mistral"
    return "angriff", None


def kampf_lauf(path, level, chips, enemy, seed):
    rng = random.Random(seed)
    z = aufbau(path, level, chips, seed)
    b = copy.deepcopy(DEFS["encounters"]["akt1_pirat"])
    b.update(enemy=enemy, level=level, flee_allowed=False)
    DEFS["encounters"]["_sim"] = b
    kampf.starten(z, DEFS, "_sim", rng=rng)
    for _ in range(160):
        k = z["kampf"]
        if k.get("ergebnis"):
            break
        if k["phase"] == "parade":
            kampf.parade_aufloesen(z, MODUL, parade_wurf(k, rng), rng=rng)
            continue
        if kampf.must_skip(k["spieler"]):
            kampf.zug(z, MODUL, "aussetzen", rng=rng)
            continue
        befehl, ziel = waehlen(z, rng)
        try:
            kampf.zug(z, MODUL, befehl, ziel, rng=rng)
        except ValueError:
            kampf.zug(z, MODUL, "angriff", rng=rng)
    k = z["kampf"]
    sp = k["spieler"]
    art = (k.get("ergebnis") or {}).get("art")
    return art in ("ko", "aufgabe"), 1 - sp["lp"] / sp["lp_max"], k["runde"]


def aufgabe(t):
    path, level, name, chips, n, base_seed = t
    sieg, verlust, runden = [], [], []
    for i, e in enumerate(ENEMIES):
        for j in range(n):
            s, v, r = kampf_lauf(path, level, chips, e, base_seed + 100 * i + j)
            sieg.append(s)
            verlust.append(v)
            runden.append(r)
    return (path, level, name), (sum(sieg) / len(sieg), statistics.mean(verlust), statistics.mean(runden))


def chips_fuer(path, level, familie, gruppe, kategorie, stufe):
    waffe, _ = PATHS[path]
    if kategorie == "element" and waffe != "gun":
        return None
    ziel = "weapon:" + waffe if gruppe == "waffe" else "armor:jacket_earth"
    return [(familie, stufe, ziel)]


def main():
    t0 = time.time()
    aufgaben = []
    for path in PATHS:
        for level, (_, stufe) in LEVELS.items():
            aufgaben.append((path, level, "Basis", [], N, 1000))
            for familie, gruppe, kat in FAMILIEN:
                c = chips_fuer(path, level, familie, gruppe, kat, stufe)
                if c:
                    aufgaben.append((path, level, familie, c, N, 1000))
    print("%d Aufgaben, %d Kämpfe je Aufgabe" % (len(aufgaben), N * len(ENEMIES)), flush=True)
    with mp.Pool(max(1, mp.cpu_count() - 4)) as pool:
        erg = dict(pool.imap_unordered(aufgabe, aufgaben, chunksize=2))
    json.dump({"|".join(map(str, k)): v for k, v in erg.items()}, open(os.path.join(HERE, "kampf_balance_chips.json"), "w"))
    print("fertig in %.0f s" % (time.time() - t0))
    ausgabe(erg)
    if "--kombi" in ARGS:
        kombi(erg)


def ausgabe(erg):
    for level in LEVELS:
        print("\n=== Level %d (Rosi %d, Chip-Stufe %d) ===" % (level, LEVELS[level][0], LEVELS[level][1]))
        print("%-26s %s" % ("Familie", "  ".join("%-14s" % ("Pfad " + p) for p in PATHS)))
        basis = {p: erg[(p, level, "Basis")] for p in PATHS}
        print("%-26s %s" % ("Basis (Sieg %, Verlust %)", "  ".join("%3.0f %%  %3.0f %%   " % (basis[p][0] * 100, basis[p][1] * 100) for p in PATHS)))
        for familie, _, _ in FAMILIEN:
            zeile = []
            for p in PATHS:
                r = erg.get((p, level, familie))
                if r is None:
                    zeile.append("%-14s" % "-")
                else:
                    zeile.append("%+4.0f / %+4.0f %%  " % ((r[0] - basis[p][0]) * 100, (r[1] - basis[p][1]) * 100))
            print("%-26s %s" % (familie, "  ".join(zeile)))
    print("\nLesart: Veränderung gegenüber der Basis (Siegquote in Punkten / LP-Verlust in Punkten; Verlust kleiner ist besser).")


def kombi(erg):
    """Staerkste Mehr-Chip-Builds: je Pfad und Akt die besten Einzel-Familien bis alle Plaetze (1 + Rosi-Stufe) je Stueck voll sind."""
    gruppe = {f: g for f, g, _ in FAMILIEN}
    kat = {f: k for f, _, k in FAMILIEN}
    aufgaben = []
    for path in PATHS:
        waffe, _ = PATHS[path]
        for level, (rosi, stufe) in LEVELS.items():
            basis = erg[(path, level, "Basis")]
            rang = sorted((f for f, _, _ in FAMILIEN if (path, level, f) in erg),
                          key=lambda f: -(erg[(path, level, f)][0] - basis[0]))
            build, n_w, n_j, element = [], 0, 0, False
            for f in rang:
                if gruppe[f] == "waffe" and n_w < 1 + rosi and not (kat[f] == "element" and element):
                    build.append((f, stufe, "weapon:" + waffe))
                    n_w += 1
                    element = element or kat[f] == "element"
                elif gruppe[f] == "jacke" and n_j < 1 + rosi:
                    build.append((f, stufe, "armor:jacket_earth"))
                    n_j += 1
            aufgaben.append((path, level, "KOMBI: " + ", ".join(b[0] for b in build), build, N, 1000))
    with mp.Pool(max(1, mp.cpu_count() - 4)) as pool:
        res = dict(pool.imap_unordered(aufgabe, aufgaben))
    print()
    print("=== Stärkste Mehr-Chip-Builds (je Pfad und Akt) ===")
    for (path, level, name), (sieg, verlust, runden) in sorted(res.items()):
        b = erg[(path, level, "Basis")]
        print("Pfad %s Lv %d: Sieg %3.0f %% (Basis %3.0f %%), Verlust %3.0f %% (Basis %3.0f %%) | %s" % (
            path, level, sieg * 100, b[0] * 100, verlust * 100, b[1] * 100, name[7:]))


if __name__ == "__main__":
    mp.freeze_support()
    main()
