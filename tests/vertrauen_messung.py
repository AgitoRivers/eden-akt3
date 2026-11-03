# -*- coding: utf-8 -*-
r"""Vertrauens-Messung (29.10.2026, Abschaltung der Schnelljobs): Vertrauen je Figur und Tag, erste Stufe 5, Energie morgens,
Geld, Favours, Werte am Ende. Nutzt den 'normal'-Bot aus tests/geld_messung.py (8 Seeds, bis Tag 15).

  python testsertrauen_messung.py messen <ausgabe.json> [seeds]   Messung schreiben
  python testsertrauen_messung.py bericht <ausgabe.json> ...      Zahlen anzeigen
Umgebung: FV_NACH=1 schaltet im Lauf die Schnelljobs ab (modul["schnelljobs"] = False) - fuer Vergleiche gegen einen
Stand, in dem sie noch an sind; FV_VAR=T2|C60|X16 spielt Varianten durch (zwei Favours am Tag / 60 % Chance / Vertrauen x1,6),
nichts davon ist eingebaut."""
import json, os, statistics, sys

EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(EDEN, "tests"))
sys.path.insert(0, EDEN)
os.environ.setdefault("PYTHONHASHSEED", "0")
import geld_messung as G  # noqa: E402
import lauf_test as L  # noqa: E402

PERSONEN = ["petru", "lola", "alva", "elsa", "rosi", "chiara", "lea", "siri", "sophia", "toto", "casanova", "yasin"]
SNAP = {}
_orig = G.tagesarbeit_normal


def wrapper(z, protokoll):
    SNAP[z["tag"]] = {"energie": z["werte"].get("energie"), "konto": z["konto"],
                      "v": {p: z["werte"].get("vertrauen." + p, 0) for p in PERSONEN}}
    return _orig(z, protokoll)


G.tagesarbeit_normal = wrapper
LETZTER = {}
_laufen = L.laufen


def laufen_merken(modul, seed):
    e = _laufen(modul, seed)
    LETZTER["ende"] = e["ende"]
    return e


L.laufen = laufen_merken

VAR = os.environ.get("FV_VAR", "")
if VAR:                                              # Varianten fuer den Vorschlag (nichts davon ist eingebaut)
    from kern import ereignisse as _ev
    if "T2" in VAR:                                  # zwei Bitten am Tag
        _ev.FAVOUR_MAX_JE_TAG = 2
    if "C60" in VAR:                                 # haeufiger: 60 % je Phase
        _ev.FAVOUR_CHANCE = {k: 0.6 for k in _ev.FAVOUR_CHANCE}
    if "X16" in VAR:                                 # Vertrauen aus Favours x1,6 (Erfolg 8, Finale 10)
        _anw = _ev.anwenden

        def anwenden_x(z, modul, ev, folgen):
            if ev["personen"].get("favour"):
                folgen = [dict(f, vertrauen=[f["vertrauen"][0], round(f["vertrauen"][1] * 1.6)]) if "vertrauen" in f else f for f in folgen]
            return _anw(z, modul, ev, folgen)
        _ev.anwenden = anwenden_x

if os.environ.get("FV_NACH") == "1":                 # nachher: Schnelljobs aus (modul["schnelljobs"] = False)
    _vorb = L.vorbereiten

    def vorbereiten_aus(*a, **k):
        r = _vorb(*a, **k)
        L.eden.modul_laden()["schnelljobs"] = False
        return r

    L.vorbereiten = vorbereiten_aus


def lauf(seed):
    SNAP.clear()
    r = G.messen("normal", seed)
    tage = sorted(SNAP)
    erste = {}
    for p in PERSONEN:
        erste[p] = next((t for t in tage if SNAP[t]["v"][p] >= 5), None)
    e = LETZTER["ende"]
    fav = e.get("favours") or []
    return {"tag_ende": e["tag"], "werte_ende": {k: v for k, v in e["werte"].items() if k.startswith("vertrauen.") or k in ("energie", "ruf", "moral", "strom", "diesel")},
            "favours": len(fav), "favours_ok": sum(1 for f in fav if f["ausgang"] == "ok"),
            "favours_ab": sum(1 for f in fav if f["ausgang"] == "abgelehnt"), "dank": sum(1 for f in fav if f["id"].endswith("_dank")),
            "jobs": len(e.get("jobs_erledigt", [])), "reparatur": e["uhren"].get("reparatur"), "auftraege_fertig": len(e.get("auftraege_fertig", [])),
            "seed": seed, "ende_konto": r["ende"], "einnahmen": dict(r["einnahmen"]), "ausgaben": dict(r["ausgaben"]),
            "erste_stufe5": erste, "snap": {str(t): SNAP[t] for t in tage}}
    return {"seed": seed, "ende_konto": r["ende"], "einnahmen": dict(r["einnahmen"]), "ausgaben": dict(r["ausgaben"]),
            "erste_stufe5": erste, "snap": {str(t): SNAP[t] for t in tage}}


def bericht(dateien):
    def med(xs):
        xs = [x for x in xs if x is not None]
        return statistics.median(xs) if xs else None
    for name in dateien:
        d = json.load(open(name, encoding="utf-8"))
        print("==", name, "(%d Seeds)" % len(d))
        print("Konto am Ende (Median):", med(r["ende_konto"] for r in d))
        print("Jobs erledigt:", [r["jobs"] for r in d], " Favours:", [r["favours"] for r in d], " Dank:", [r["dank"] for r in d])
        for p in PERSONEN:
            v = [r["werte_ende"].get("vertrauen." + p, 0) for r in d]
            e = [r["erste_stufe5"][p] for r in d]
            print("  %-9s Ende %s (min %s max %s)  Stufe 5 erreicht: %d/%d" % (p, med(v), min(v), max(v), sum(1 for x in e if x), len(e)))
        for k in ("ruf", "moral", "strom", "diesel"):
            print("  %-6s Ende (Median) %s" % (k, med(r["werte_ende"].get(k) for r in d)))
        en = [s["energie"] for r in d for s in r["snap"].values()]
        print("Energie morgens: Anteil 3 von 3 = %.0f %%, Anteil 0 = %.0f %%" % (
            100 * sum(1 for e in en if e == 3) / len(en), 100 * sum(1 for e in en if e == 0) / len(en)))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if sys.argv[1] == "bericht":
        bericht(sys.argv[2:])
    else:
        out = sys.argv[2]
        n = int(sys.argv[3]) if len(sys.argv) > 3 else 8
        erg = [lauf(s) for s in range(1, n + 1)]
        json.dump(erg, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("fertig", out)
