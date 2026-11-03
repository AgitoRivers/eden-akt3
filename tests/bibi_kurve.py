# -*- coding: utf-8 -*-
r"""Beziehungskurve fuer Bibi (Duc 02.11.2026): Die Bots spielen das Red Trio nicht mit dem Ausgang, den ihre Romanze braucht.
Darum setzt dieser Lauf am Ende von Tag QUEST_ENDE den guten Ausgang (Mochi frei, Trio versoehnt, Bibi bleibt) wie die Quest
und spielt dann wie spieltest_kurve einen Spieler, der sich nur auf sie konzentriert. Obergrenze, nicht ein Mensch.

  python tests\bibi_kurve.py [seeds] [quest_ende]
"""
import json, os, statistics, subprocess, sys, tempfile

HIER = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HIER)
FLAGS = ["kl_loewe_frei", "kloster_fertig", "red_trio_fertig", "rt_ausgang_alle", "rt_bibi_bleibt", "mochis_offen", "rt_gestartet"]


def ein_lauf(seed, quest_ende, pfad):
    sys.path.insert(0, HIER)
    import spieltest_bot as B
    E = B.E
    tage, org = {}, E.plan.tagesende

    def tagesende(z, modul):
        if z["tag"] == quest_ende and "rt_bibi_bleibt" not in z["flags"]:
            z["flags"] += [f for f in FLAGS if f not in z["flags"]]
            z.setdefault("flag_tag", {})["rt_ende_tag"] = z["tag"]
            z["flags"].append("rt_ende_tag")
            z["werte"]["vertrauen.bibi"] = max(z["werte"].get("vertrauen.bibi", 0), 3)     # Tisch Basis 2-3, Idee +4 Punkte
            if "bibi" not in (z.get("bekannt") or []):
                z.setdefault("bekannt", []).append("bibi")
            E.rollen.romanze_abgleichen(z, modul)
        tage[z["tag"]] = {k: v for k, v in z["werte"].items() if k.endswith(".bibi")}
        return org(z, modul)
    E.plan.tagesende = tagesende
    lauf = B.Lauf("naomi", seed)
    org_geste, org_wahl = B.geste_waehlen, lauf.wahl_treffen

    def geste_waehlen(p, gesten, rng, ziel=None, verabredet=()):
        nur = [dict(g, je={k: v for k, v in g.get("je", {}).items() if k == "bibi"}) for g in gesten]
        return org_geste(p, nur, rng, ziel="bibi", verabredet=verabredet)

    def wahl_treffen(z, optionen, orte):
        eigene = [s for s in optionen if s == "date_bibi" or s.startswith("frei_bibi_")]
        return ("szene", eigene[0]) if eigene else org_wahl(z, optionen, orte)
    B.geste_waehlen = geste_waehlen
    lauf.wahl_treffen = wahl_treffen
    lauf.partner = lambda z: "bibi"
    m = lauf.spielen()
    json.dump({"tage": tage, "events": m.get("events") or {}, "ende": m.get("ende"), "rest": {k: m[k] for k in m if k not in ("events",) and not isinstance(m[k], (dict, list))}, "abgebrochen": m.get("abgebrochen"), "fehler": (m.get("fehler") or [])[:3], "listen": {k: str(m[k])[-600:] for k in m if isinstance(m[k], list)}}, open(pfad, "w", encoding="utf-8"))


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--lauf":
        return ein_lauf(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
    seeds = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    quest_ende = int(sys.argv[2]) if len(sys.argv) > 2 else 13
    ordner = tempfile.mkdtemp(prefix="bibi_kurve_")
    laeufe = []
    for s in range(1, seeds + 1):
        pfad = os.path.join(ordner, "l%d.json" % s)
        subprocess.run([sys.executable, os.path.abspath(__file__), "--lauf", str(s), str(quest_ende), pfad], cwd=BASE,
                       env=dict(os.environ, PYTHONUTF8="1", PYTHONHASHSEED="0"), capture_output=True, timeout=2400)
        if os.path.exists(pfad):
            laeufe.append(json.load(open(pfad, encoding="utf-8")))
        print("Seed", s, "fertig" if os.path.exists(pfad) else "ABGEBROCHEN", flush=True)
    sys.stdout.reconfigure(encoding="utf-8")
    letzter = max(int(t) for l in laeufe for t in l["tage"])
    for achse in ("vertrauen", "begehren"):
        print("%-10s" % achse, " ".join("%2d" % t for t in range(quest_ende, letzter + 1)))
        for i, l in enumerate(laeufe, 1):
            print("  Seed %d   " % i, " ".join("%2s" % l["tage"].get(str(t), {}).get("%s.bibi" % achse, "·") for t in range(quest_ende, letzter + 1)))
    for l in laeufe:
        print("Events Bibi:", sorted(e for e in l["events"] if e.startswith(("rm_b", "mo_a_", "sf_bibi"))))


if __name__ == "__main__":
    main()
