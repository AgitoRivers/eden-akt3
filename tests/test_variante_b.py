# -*- coding: utf-8 -*-
"""Variante B (25.10.2026): Ermittlung per Handy ausserhalb einer Szene kostet 1 Aktion, Abgleichen bleibt gratis.

  python tests\\test_variante_b.py
"""
import os, sys, tempfile

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import lauf_test as L  # noqa: E402

E = L.eden


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def bis_handy():
    """Spielt mit dem Bot, bis in einer freien Wahl-Phase eine Handy-Ermittlung angeboten wird."""
    prot = {"schritte": [], "erledigt": {}}
    z = E.aktion("neu", {"modus": "ironman"})
    for _ in range(3000):
        if z["status"] == "wahl" and not E.plan.aktionen(z):
            modul = E.modul_laden()
            hs = [m for m in E.ermittlung.moeglich(z, modul) if m["art"] == "handy" and not m.get("sperre")]
            if hs:
                return z, modul, hs[0]
        a = L.schritt(z, prot)
        if a[0] != "_tagesarbeit":
            L.versuch(a, prot)
        z = E.aktiv()
        if z["status"] == "ende":
            break
    raise AssertionError("keine Handy-Ermittlung gefunden")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    L.vorbereiten("eden_rise", tempfile.mkdtemp(prefix="eden_varb_"))
    L.random.seed(5)
    z, modul, h = bis_handy()
    pruefen("1 Aktion" in h["kosten"] or "1 action" in h["kosten"], "Handy-Ermittlung zeigt 'kostet 1 Aktion' (%s)" % h["kosten"])
    tag, phase = z["tag"], z["phase"]
    z = E.aktion("ermitteln", {"weg": h["weg"]})
    pruefen((z["tag"], z["phase"]) == (tag, phase) and E.plan.aktionen(z) == 1,
            "Handy-Ermittlung verbraucht 1 Aktion, die Phase laeuft weiter")
    ab = [m for m in E.ermittlung.moeglich(z, modul) if m["art"] == "abgleichen"]
    if ab:
        z = E.aktion("ermitteln", {"weg": ab[0]["weg"]})
        pruefen(E.plan.aktionen(z) == 1, "Abgleichen bleibt gratis")
    print("OK")


if __name__ == "__main__":
    main()
