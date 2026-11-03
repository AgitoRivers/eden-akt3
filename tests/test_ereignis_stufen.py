# -*- coding: utf-8 -*-
r"""Event-Stufen je Phase (25.10.2026): Bordrat in 3 von 4 freien Naechten, sonst die Meldung "ruhige Nacht"; Handy als
eigene Spur (hoechstens zwei Zufalls-Nachrichten am Tag, Megans Pflicht-Nachrichten extra). Ein voller Bot-Lauf je Seed.

  python tests\test_ereignis_stufen.py
"""
import collections, os, sys, tempfile

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import lauf_test as L  # noqa: E402

E = L.eden


def lauf(seed):
    L.vorbereiten("eden_rise", tempfile.mkdtemp(prefix="eden_stufen_"), seed)
    L.random.seed(seed)
    prot = {"schritte": [], "erledigt": {}}
    z = E.aktion("neu", {"modus": "ironman"})
    naechte = {}                                  # Tag -> "bordrat" | "ruhig"
    handy = collections.Counter()
    gemeldet = 0
    for _ in range(L.MAX_SCHRITTE):
        a = L.schritt(z, prot)
        if a is None:
            break
        L.tagesarbeit(z, prot) if a[0] == "_tagesarbeit" else L.versuch(a, prot)
        z = E.aktiv()
        ev = z.get("event") or {}
        if ev.get("id"):
            art = E.ereignisse.daten(E.moddir())["_index"][ev["id"]]["art"]
            if art == "bordrat":
                naechte[z["tag"]] = "bordrat"
            pflicht = E.ereignisse.daten(E.moddir())["_index"][ev["id"]]["wann"].get("pflicht")
            if art == "handy" and not pflicht and (ev["id"], z["tag"]) not in handy:
                handy[(ev["id"], z["tag"])] = 1
        ruhig = sum(1 for m in z.get("meldungen", []) if m.get("titel") == "A Quiet Night")
        if ruhig > gemeldet:
            gemeldet = ruhig
            naechte.setdefault(z["tag"], "ruhig")
    je_tag = collections.Counter(t for _, t in handy)
    return naechte, je_tag


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    for seed in (1, 2, 3):
        naechte, je_tag = lauf(seed)
        ruhig = [t for t, x in naechte.items() if x == "ruhig"]
        rat = [t for t, x in naechte.items() if x == "bordrat"]
        assert ruhig, "Seed %d: keine ruhige Nacht gemeldet %s" % (seed, naechte)
        assert len(rat) >= len(ruhig), "Seed %d: mehr ruhige Naechte als Bordraete %s" % (seed, naechte)
        assert all(n <= 2 for n in je_tag.values()), "Seed %d: mehr als zwei Handy-Events an einem Tag %s" % (seed, je_tag)
        print("OK Seed %d: Bordrat an Tag %s, ruhige Nacht an Tag %s, Handy je Tag %s" % (seed, rat, ruhig, dict(je_tag)))


if __name__ == "__main__":
    main()
