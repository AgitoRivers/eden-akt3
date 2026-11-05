# -*- coding: utf-8 -*-
"""Dichte des Akt-3-Kalenders (Duc 05.11.2026): je Tag und Phase alle Pflicht-Events, die dort laufen KOENNEN
(Fenster passt, Bedingung nicht ausgewertet). Leiter-Szenen (Freundschaften) zaehlen hoechstens eine am Tag.
Ausgabe: Tabelle; Exit 0. Schwelle fuer "voll": 3 oder mehr Pflicht-Szenen in einer Phase, ohne Varianten derselben Szene."""
import json, os, re, sys
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHASEN = ["fruehstueck", "tag", "nachmittag", "dinner", "abend", "nacht"]
ev = json.load(open(os.path.join(BASE, "module", "eden_rise", "ereignisse.json"), encoding="utf-8"))["events"]


def stamm(eid):
    """Varianten einer Szene (a3_probefahrt / a3_probefahrt_petru, ..._kai) zaehlen einmal."""
    for gruppe in ("a3_dank_", "mo_a_", "a3_mitternacht", "mo_halsbaender", "mo_schlafgranate"):
        if eid.startswith(gruppe):           # je Tag hoechstens eine davon (einmalig, je Haus/Tier/Frau)
            return gruppe.rstrip("_") + "*"
    if eid in ("a3_bibi_idee", "a3_lea_idee"):
        return "a3_idee*"
    if eid in ("a3_schiene", "a3_sandru_alon"):
        return "a3_schiene*"
    return re.sub(r"_(petru|kai|deal|ohne|mit|allein)$", "", eid)


def tabelle(tage=range(24, 36)):
    out = {}
    for t in tage:
        for p in PHASEN:
            ids, leiter = set(), False
            for e in ev:
                w = e.get("wann") or {}
                if not w.get("pflicht") or e.get("art") == "ort":
                    continue
                a, b = (w.get("tage") or [0, 99])[:2]
                if not (a <= t <= b) or p not in (w.get("phasen") or []):
                    continue
                if w.get("leiter"):
                    leiter = True
                    continue
                if e["id"].startswith(("bl_", "hy_")):
                    continue
                ids.add(stamm(e["id"]))
            out[(t, p)] = (sorted(ids), leiter)
    return out


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for (t, p), (ids, leiter) in tabelle().items():
        n = len(ids) + (1 if leiter else 0)
        if n:
            print("Tag %d %-11s %d%s  %s%s" % (t, p, n, " VOLL" if n >= 3 else "", ", ".join(ids), " + Freundschaft" if leiter else ""))
