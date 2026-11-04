# -*- coding: utf-8 -*-
r"""Simulation der Akt-3-Enden (kern/akt3.saeulen und ende): tausende Laeufe mit zufaelligen, aber typischen Entscheidungen,
je Spielertyp. Kein Test, ein Werkzeug fuer die Balance (Review: Ende 3 etwa jedes dritte Mal bei engagierten Spielern).

  python tests/sim_enden_akt3.py [--n 20000] [--kommission] [--streng]

Annahmen je Spielertyp (Wahrscheinlichkeit je Baustein) stehen in PROFILE. --kommission: die Verhandlung ist an
(kern/kommission), gewonnene Runden ersetzen dann fehlende Beweise fuer die Saeule Wahrheit."""
import collections, os, random, sys

EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, EDEN)
from kern import akt3  # noqa: E402

PROFILE = {
    "gelegentlich": {"zeuge": 0.35, "sandru": 0.3, "kiste": 0.2, "siri": 0.4, "sophia": 0.3, "funk": 0.3, "wache": 0.3, "rt": 0.2,
                     "ark": 0.2, "mast": 0.3, "yama5": 0.1, "kampf": 0.5, "elsa": 0.3, "deal": 0.05, "ruf5": 0.2, "runde": 0.4},
    "engagiert": {"zeuge": 0.6, "sandru": 0.5, "kiste": 0.35, "siri": 0.5, "sophia": 0.4, "funk": 0.4, "wache": 0.4, "rt": 0.35,
                  "ark": 0.4, "mast": 0.6, "yama5": 0.25, "kampf": 0.7, "elsa": 0.5, "deal": 0.03, "ruf5": 0.4, "runde": 0.6},
    "alles": {"zeuge": 0.9, "sandru": 0.8, "kiste": 0.5, "siri": 0.6, "sophia": 0.5, "funk": 0.5, "wache": 0.5, "rt": 0.5,
              "ark": 0.6, "mast": 0.9, "yama5": 0.4, "kampf": 0.85, "elsa": 0.7, "deal": 0.02, "ruf5": 0.6, "runde": 0.8},
}
DORF = ["petru", "mina", "batu", "alva", "anghjulu", "casanova"]


def lauf(p, rng, kommission=False, streng=False):
    f, w = ["a3_beweis_feuer", "a3_zeuge_bonaventure"], {}
    f += ["a3_zeuge_" + x for x in DORF if rng.random() < p["zeuge"]]
    if rng.random() < p["sandru"]:
        f.append("a3_zeuge_sandru")
    for key, flag in (("kiste", "alon_kiste_genutzt"), ("siri", "a3_siri_post"), ("sophia", "sophia_notizen"), ("funk", "bl_funk_white"),
                      ("wache", "bl_wache_gesehen"), ("rt", "rt_ausgang_alle"), ("ark", "mo_ark_beweis")):
        if rng.random() < p[key]:
            f.append(flag)
    if rng.random() < p["mast"]:
        f.append("a3_mast_an" if rng.random() < 0.5 else "a3_mast_aus")
    if rng.random() < p["yama5"]:
        w["vertrauen.yamamoto"] = 5
    if rng.random() < p["ruf5"]:
        w["ruf"] = 5
    z = {"flags": f, "werte": w}
    zeugen = len(akt3.zeugen(z))                         # Monaco ist Tag 31: Whites Plan aus der Villa (Tag 34) gibt es noch nicht
    beweise = len([b for b in akt3.beweise(z) if b != "a3_beweis_feuer"])
    if (zeugen >= 4 and beweise >= 2 if streng else zeugen >= 4 or beweise >= 2) or w.get("vertrauen.yamamoto", 0) >= 5:
        f.append("a3_megan_wende")
    f.append("a3_kassenbuch_alles" if rng.random() < 0.5 else "a3_kassenbuch_teil")
    if rng.random() < p["kampf"]:
        f.append("a3_alon_besiegt")
    if rng.random() < p["elsa"]:
        f.append("a3_alon_festgenommen")
    if kommission:
        n = sum(1 for _ in range(3) if rng.random() < p["runde"])
        f.append("a3_kom_runden_%d" % n)
    if rng.random() < p["deal"]:
        f.append("a3_deal")
    if streng:                                           # Vorschlag: Wahrheit braucht 4 Beweise oder 3 mit "alles"
        nb = len(akt3.beweise(z))
        ok = nb >= 4 or (nb >= 3 and "a3_kassenbuch_alles" in f) or "a3_kom_runden_3" in f
        if not ok:
            f[:] = [x for x in f if not x.startswith("a3_kom_runden_")]
            z["_wahrheit_aus"] = True
    sa = akt3.saeulen(z)
    if z.get("_wahrheit_aus"):
        sa["wahrheit"] = False
    return _ende(z, sa), sa


def _ende(z, s):
    if "a3_deal" in z["flags"]:
        return "1"
    n = sum(s.values())
    if n == 4:
        return "3"
    if n == 3:
        return "2.5a" if not s["geld"] else "2.5b" if not s["gemeinschaft"] else "2.5c" if not s["staerke"] else "0"
    if n == 2 and s["wahrheit"]:
        return "2a" if s["geld"] else "2b" if s["gemeinschaft"] else "2c"
    return "0"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    n = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 20000
    kom = "--kommission" in sys.argv
    streng = "--streng" in sys.argv
    rng = random.Random(4112026)
    print("Laeufe je Typ: %d, Kommission als Verhandlung: %s, strengere Regeln: %s" % (n, "an" if kom else "aus", "ja" if streng else "nein"))
    for typ, p in PROFILE.items():
        enden, s = collections.Counter(), collections.Counter()
        for _ in range(n):
            e, sa = lauf(p, rng, kom, streng)
            enden[e] += 1
            s.update(k for k, v in sa.items() if v)
        print("\n%s" % typ)
        print("  Saeulen: " + ", ".join("%s %d %%" % (k, round(100 * s[k] / n)) for k in ("wahrheit", "geld", "gemeinschaft", "staerke")))
        print("  Enden:   " + ", ".join("%s %s %d %%" % (e, akt3.ENDEN[e], round(100 * c / n)) for e, c in enden.most_common()))


if __name__ == "__main__":
    main()
