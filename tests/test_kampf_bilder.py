# -*- coding: utf-8 -*-
r"""Kampfbilder neuer Gegner (Duc 30.10.2026): Jede Figur braucht ein Gesicht fuer die Zugfolge, jedes Tier eine Groesse.
Ob das Gesicht im Ausschnitt sitzt, sieht nur ein Mensch: Neue Avatare auf dem Bogen ansehen (Wiki systeme/kampf.md).

  python tests\test_kampf_bilder.py
"""
import json, os, sys

EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(EDEN, "werkzeuge"))
import kampf_bilder as B  # noqa: E402

FREI = {"Kevin"}                                         # der Kakadu ist absichtlich zu gross


def main():
    M = os.path.join(EDEN, "module", "eden_rise")
    d = json.load(open(os.path.join(M, "kaempfe.json"), encoding="utf-8"))
    fehlt, ohne, kopflos = [], [], []
    for gid, g in d["enemies"].items():
        s = g.get("sprite")
        if s and not os.path.isfile(os.path.join(M, "kampf", s, "avatar.webp")):
            fehlt.append(s)
        if s and g.get("cls") in ("tier", "flieger") and s not in B.GROESSE and s not in FREI:
            ohne.append(s)
        if s and g.get("cls") == "mensch" and s not in B.KOPF:
            kopflos.append(s)
    assert not fehlt, "Kein Gesicht fuer die Zugfolge: %s" % sorted(set(fehlt))
    assert not ohne, "Tier ohne Groesse in kampf_bilder.GROESSE: %s" % sorted(set(ohne))
    assert not kopflos, "Mensch ohne gemessenen Kopf in kampf_bilder.KOPF: %s" % sorted(set(kopflos))
    print("OK")


if __name__ == "__main__":
    main()
