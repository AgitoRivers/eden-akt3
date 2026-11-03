# -*- coding: utf-8 -*-
r"""Beziehungskurve: Welche Stufe hat jede Frau an jedem Spieltag? Offline-Bot, ohne Modell und ohne Grafikkarte.
Spielt die Review-Profile und je Frau einen Spieler, der sich auf sie konzentriert. Bots nutzen jede Chance, die
Zahlen sind also eine Obergrenze fuer das, was ein Mensch erreicht.

  python tests\spieltest_kurve.py                       schreibt docs\brain_trust\BEZIEHUNGSKURVE.md
  python tests\spieltest_kurve.py --seeds 2 --jobs 4
  python tests\spieltest_kurve.py --abstand 0        rechnet mit einem anderen Stufen-Abstand als das Spiel, 0 = ohne,
                                                     nur in dieser Rechnung (zustand.STUFEN_ABSTAND)

Laeufe in einem eigenen Worktree auf festem Commit starten: Andere Sitzungen bauen modul.json laufend neu.
"""
import argparse, concurrent.futures, json, os, statistics, subprocess, sys, tempfile

HIER = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HIER)
ZIEL = os.path.join(BASE, "docs", "brain_trust", "BEZIEHUNGSKURVE.md")
PROFILE = ["naomi", "lenny", "mia", "mateo", "tandi"]
FOKUS_BASIS = "naomi"
STUFEN = (3, 4, 5)


def ein_lauf(typ, seed, fokus, pfad, abstand=None):
    sys.path.insert(0, HIER)
    import spieltest_bot as B
    E = B.E
    if abstand is not None:
        E.zustand.STUFEN_ABSTAND = abstand
    if os.environ.get("KURVE_FOKUS"):                  # Vergleich: Gewicht fuer die eigenen Frauen (1 = aus)
        E.ereignisse.FOKUS_FAKTOR = int(os.environ["KURVE_FOKUS"])
    if os.environ.get("KURVE_FOKUS"):                  # Vergleich: Gewicht fuer die eigenen Frauen (1 = aus)
        E.ereignisse.FOKUS_FAKTOR = int(os.environ["KURVE_FOKUS"])
    tage, org = {}, E.plan.tagesende

    def tagesende(z, modul):
        tage[z["tag"]] = {k: v for k, v in z["werte"].items() if k.startswith(("vertrauen.", "begehren."))}
        return org(z, modul)
    E.plan.tagesende = tagesende
    lauf = B.Lauf(typ, seed)
    if fokus:
        org_geste, org_wahl = B.geste_waehlen, lauf.wahl_treffen

        def geste_waehlen(p, gesten, rng, ziel=None, verabredet=()):
            nur = [dict(g, je={k: v for k, v in g.get("je", {}).items() if k == fokus}) for g in gesten]
            return org_geste(p, nur, rng, ziel=fokus, verabredet=verabredet)

        def wahl_treffen(z, optionen, orte):
            eigene = [s for s in optionen if s == "date_" + fokus or s.startswith("frei_%s_" % fokus)]
            return ("szene", eigene[0]) if eigene else org_wahl(z, optionen, orte)
        B.geste_waehlen = geste_waehlen
        lauf.wahl_treffen = wahl_treffen
        lauf.partner = lambda z: fokus
    m = lauf.spielen()
    json.dump({"tage": tage, "ende": m.get("ende"), "abgebrochen": m.get("abgebrochen"), "events": m.get("events") or {}},
              open(pfad, "w", encoding="utf-8"))


def starten(auftrag):
    name, typ, seed, fokus, ordner, abstand = auftrag
    pfad = os.path.join(ordner, "%s_%d.json" % (name, seed))
    r = subprocess.run([sys.executable, os.path.abspath(__file__), "--lauf", typ, str(seed), fokus or "-", pfad, str(abstand)], cwd=BASE,
                       env=dict(os.environ, PYTHONUTF8="1", PYTHONHASHSEED="0"), capture_output=True, encoding="utf-8",
                       errors="replace", timeout=1800)
    if not os.path.exists(pfad):
        raise RuntimeError("%s/%d: %s" % (name, seed, (r.stdout + r.stderr)[-800:]))
    print(" ", name, seed, "fertig", flush=True)
    return name, seed, json.load(open(pfad, encoding="utf-8"))


def stufe(lauf, tag, schluessel):
    t = lauf["tage"].get(str(tag))
    return t.get(schluessel, 0) if t else None


def median_tag(werte):
    """Erster Tag einer Stufe ueber die Seeds: Median, nur wenn die Mehrheit sie erreicht."""
    da = sorted(w for w in werte if w is not None)
    return int(statistics.median_low(da)) if len(da) * 2 > len(werte) else None


def erster_tag(laeufe, schluessel, st):
    out = []
    for l in laeufe:
        tage = sorted(int(t) for t in l["tage"])
        out.append(next((t for t in tage if l["tage"][str(t)].get(schluessel, 0) >= st), None))
    return median_tag(out)


def geschrieben(w, ev):
    """Ein geschriebener Moment mit ihr: Leiter, Echo, Selfie oder Flirt-Event, in dem sie vorkommt."""
    if ev["id"].startswith("sfn_"):
        return False
    wer = json.dumps(ev["personen"])
    return '"%s"' % w in wer and (ev["id"].startswith(("rm_", "sf_")) or bool(ev.get("knistern")))


def stille(lauf, w, idx, letzter):
    """Laengste Strecke in Spieltagen ohne geschriebenen Moment mit ihr, ab Tag 2 bis zum letzten Tag."""
    tage = sorted(t for e, t in lauf.get("events", {}).items() if e in idx and geschrieben(w, idx[e]))
    grenzen = [1] + tage + [letzter + 1]
    return max(b - a - 1 for a, b in zip(grenzen, grenzen[1:])), len(tage)


def geschrieben(w, ev):
    """Ein geschriebener Moment mit ihr: Leiter, Echo, Selfie oder Flirt-Event, in dem sie vorkommt."""
    if ev["id"].startswith("sfn_"):
        return False
    wer = json.dumps(ev["personen"])
    return '"%s"' % w in wer and (ev["id"].startswith(("rm_", "sf_")) or bool(ev.get("knistern")))


def stille(lauf, w, idx, letzter):
    """Laengste Strecke in Spieltagen ohne geschriebenen Moment mit ihr, ab Tag 2 bis zum letzten Tag."""
    tage = sorted(t for e, t in lauf.get("events", {}).items() if e in idx and geschrieben(w, idx[e]))
    grenzen = [1] + tage + [letzter + 1]
    return max(b - a - 1 for a, b in zip(grenzen, grenzen[1:])), len(tage)


def bericht(erg, frauen, seeds):
    letzter = max(int(t) for l in sum(erg.values(), []) for t in l["tage"])
    z = ["# Beziehungskurve", "",
         "Erzeugt von `tests/spieltest_kurve.py`: %d Seeds je Spieler, offline ohne Modell, gebaut bis Tag %d." % (seeds, letzter), "",
         "**So lesen:** Die Bots nutzen jede Chance, die Zahlen sind also eine Obergrenze. Ein Mensch ist langsamer. Der Bot wählt "
         "Event-Antworten nach dem sichtbaren Text, auch der Ein-Frau-Spieler sammelt dabei Punkte bei den anderen. "
         "Werte: Median über die Seeds, „–“ = in der Mehrheit der Läufe nicht erreicht.", "",
         "## Erster Tag je Stufe", ""]
    namen = {"naomi": "Naomi (Romantik, alle Frauen)", "lenny": "Lenny (Fanservice, alle Frauen)", "mia": "Mia (Mischung)",
             "mateo": "Mateo (Sammler)", "tandi": "Tandi (lädt nie ein)"}
    kopf = "| Frau | V3 | V4 | V5 | B3 | B4 | B5 |\n|---|---|---|---|---|---|---|"
    f = lambda x: str(x) if x is not None else "–"     # noqa: E731
    z += ["### Spieler, der sich auf eine Frau konzentriert", "", kopf]
    for w in frauen:
        l = erg.get("fokus_" + w, [])
        z.append("| %s | %s |" % (w.capitalize(), " | ".join(f(erster_tag(l, "%s.%s" % (a, w), s))
                                                              for a in ("vertrauen", "begehren") for s in STUFEN)))
    for p in PROFILE:
        z += ["", "### " + namen[p], "", kopf]
        for w in frauen:
            z.append("| %s | %s |" % (w.capitalize(), " | ".join(f(erster_tag(erg[p], "%s.%s" % (a, w), s))
                                                                  for a in ("vertrauen", "begehren") for s in STUFEN)))
    idx = {e["id"]: e for e in json.load(open(os.path.join(BASE, "module", "eden_rise", "ereignisse.json"), encoding="utf-8"))["events"]}
    z += ["", "## Längste Stille", "", "Längste Strecke in Spieltagen ohne geschriebenen Moment mit dieser Frau (Leiter, Echo, Selfie, Flirt-Event), "
          "beim Spieler, der sich auf sie konzentriert. Ziel: höchstens 3 Tage. Freie Szenen zählen nicht. Median über die Seeds.", "",
          "| Frau | Längste Stille | Momente im Lauf |", "|---|---|---|"]
    for w in frauen:
        je = [stille(x, w, idx, letzter) for x in erg.get("fokus_" + w, [])]
        if je:
            z.append("| %s | %d | %d |" % (w.capitalize(), statistics.median_low([a for a, _ in je]), statistics.median_low([b for _, b in je])))
    idx = {e["id"]: e for e in json.load(open(os.path.join(BASE, "module", "eden_rise", "ereignisse.json"), encoding="utf-8"))["events"]}
    z += ["", "## Längste Stille", "", "Längste Strecke in Spieltagen ohne geschriebenen Moment mit dieser Frau (Leiter, Echo, Selfie, Flirt-Event), "
          "beim Spieler, der sich auf sie konzentriert. Ziel: höchstens 3 Tage. Freie Szenen zählen nicht. Median über die Seeds.", "",
          "| Frau | Längste Stille | Momente im Lauf |", "|---|---|---|"]
    for w in frauen:
        je = [stille(x, w, idx, letzter) for x in erg.get("fokus_" + w, [])]
        if je:
            z.append("| %s | %d | %d |" % (w.capitalize(), statistics.median_low([a for a, _ in je]), statistics.median_low([b for _, b in je])))
    z += ["", "## Stufe je Spieltag", ""]
    spalten = list(range(1, letzter + 1))
    kopf2 = "| Frau | " + " | ".join(str(t) for t in spalten) + " |\n|---|" + "---|" * len(spalten)

    def zeile(l, w, achse):
        werte = []
        for t in spalten:
            da = [stufe(x, t, "%s.%s" % (achse, w)) for x in l]
            da = [d for d in da if d is not None]
            werte.append(str(int(statistics.median_low(da))) if da else "·")
        return "| %s | %s |" % (w.capitalize(), " | ".join(werte))
    for achse, titel in (("vertrauen", "Vertrauen"), ("begehren", "Begehren")):
        z += ["### %s: Ein-Frau-Spieler (jede Zeile ein eigener Lauf, nur auf diese Frau konzentriert)" % titel, "", kopf2]
        z += [zeile(erg.get("fokus_" + w, []), w, achse) for w in frauen] + [""]
        for p in PROFILE:
            z += ["### %s: %s" % (titel, namen[p]), "", kopf2] + [zeile(erg[p], w, achse) for w in frauen] + [""]
    z += ["## Wie viele Frauen stehen auf Vertrauen 5?", "", kopf2.replace("| Frau |", "| Spieler |")]
    for p in PROFILE:
        reihe = []
        for t in spalten:
            je = [sum(1 for w in frauen if (stufe(x, t, "vertrauen." + w) or 0) >= 5) for x in erg[p]]
            reihe.append(str(int(statistics.median_low(je))))
        z.append("| %s | %s |" % (p.capitalize(), " | ".join(reihe)))
    return "\n".join(z) + "\n"


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--lauf":
        typ, seed, fokus, pfad, abstand = sys.argv[2:7]
        return ein_lauf(typ, int(seed), None if fokus == "-" else fokus, pfad, None if abstand == "None" else int(abstand))
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=3)
    ap.add_argument("--jobs", type=int, default=max(2, (os.cpu_count() or 4) // 2))
    ap.add_argument("--abstand", type=int, default=None, help="Stufen-Abstand in Tagen statt dem des Spiels, 0 = ohne (nur Rechnung)")
    a = ap.parse_args()
    ziel = ZIEL.replace(".md", "_ABSTAND_%d.md" % a.abstand) if a.abstand is not None else ZIEL
    modul = json.load(open(os.path.join(BASE, "module", "eden_rise", "modul.json"), encoding="utf-8"))
    frauen = sorted(p for p, x in modul["personen"].items() if x.get("romanzierbar"))
    ordner = tempfile.mkdtemp(prefix="eden_kurve_")
    auftraege = [(p, p, s, None, ordner, a.abstand) for p in PROFILE for s in range(1, a.seeds + 1)]
    auftraege += [("fokus_" + w, FOKUS_BASIS, s, w, ordner, a.abstand) for w in frauen for s in range(1, a.seeds + 1)]
    erg = {}
    print(len(auftraege), "Läufe,", a.jobs, "gleichzeitig", flush=True)
    with concurrent.futures.ThreadPoolExecutor(a.jobs) as ex:
        for name, seed, d in ex.map(starten, auftraege):
            erg.setdefault(name, []).append(d)
    abgebrochen = [(n, l["ende"]) for n, ls in erg.items() for l in ls if l.get("abgebrochen")]
    if abgebrochen:
        print("ABGEBROCHEN:", abgebrochen)
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=BASE, capture_output=True, encoding="utf-8").stdout.strip()
    stand = "Commit %s, Stufen-Abstand %s. Erzeugt von" % (commit, "wie im Spiel" if a.abstand is None else "%d Tage" % a.abstand)
    open(ziel, "w", encoding="utf-8").write(bericht(erg, frauen, a.seeds).replace("Erzeugt von", stand, 1))
    json.dump(erg, open(ziel.replace(".md", ".json").replace(os.path.join("docs", "brain_trust"), os.path.join("tests", "spieltest_ergebnis")),
                        "w", encoding="utf-8"))
    print("Geschrieben:", ziel)


if __name__ == "__main__":
    main()
