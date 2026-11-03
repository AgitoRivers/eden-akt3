# -*- coding: utf-8 -*-
"""Red Trio im Kampf (Duc 30.10.2026): Bibis Wasser plus Charlys Full Charge im selben Zug ergibt den Kurzschluss, in
beiden Kaempfen; allein wirft Bibi die Splittergranate statt Wasser.

  python tests\\test_red_trio_kombo.py
"""
import json, os, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
sys.path.insert(0, os.path.join(BASE, "tests"))
DEFS = json.load(open(os.path.join(BASE, "module", "eden_rise", "kaempfe.json"), encoding="utf-8"))


def absichten(bid, runden):
    """Plan aus Muster und Startversatz, wie kern/kampf.py ihn laeuft: {instanz-typ: [absicht je Runde]}."""
    ids = DEFS["encounters"][bid]["enemies"]
    return {e: [DEFS["enemies"][e]["pattern"][(i + r) % len(DEFS["enemies"][e]["pattern"])] for r in range(runden)]
            for i, e in enumerate(ids) if e in ("rt_bibi", "rt_charly")}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    for bid in ("rt_1_bibi_charly", "rt_3_trio"):
        ids = DEFS["encounters"][bid]["enemies"]
        assert ids.index("rt_bibi") + 1 == ids.index("rt_charly"), "%s: Bibi muss direkt vor Charly stehen" % bid
        p = absichten(bid, 8)
        treffer = [r for r in range(8) if p["rt_bibi"][r] == "w2" and p["rt_charly"][r] == "s1"]
        assert len(treffer) == 2, (bid, p)
        assert not [r for r in range(8) if p["rt_charly"][r] == "s1" and p["rt_bibi"][r] != "w2"], (bid, p)
        print("OK %s: Kombo in den Runden %s" % (bid, treffer))
    b, c = DEFS["enemies"]["rt_bibi"], DEFS["enemies"]["rt_charly"]
    assert b["specials"]["w2"]["effect"] == "nass" and c["specials"]["s1"]["effect"] == "strom"
    allein = b["pattern_allein"]
    assert "w2" not in allein and "s2" in allein and b["specials"]["s2"]["bonus"] > 0 and not b["specials"]["s2"]["effect"]
    print("OK Allein wirft Bibi Splitter statt Wasser")

    # Echter Lauf durch die Engine: Muster greift, und faellt Charly, wechselt Bibi
    import test_kampf as T
    from kern import kampf
    z = T.new("rt_1_bibi_charly")
    k = z["kampf"]
    assert [g["pattern"] for g in k["gegner"]] == [b["pattern"], c["pattern"]]
    # Kurzschluss: das Engine-Ergebnis der beiden Effekte auf Duc
    ctx = T.ctx(z)
    sp = k["spieler"]
    sp["states"]["nass"] = 2
    lp = sp["lp"]
    ctx["g"] = k["gegner"][1]
    kampf._duc_state(ctx, "strom", 2)
    assert "nass" not in sp["states"] and "strom" not in sp["states"] and sp["states"].get("betaeubt") and sp["lp"] < lp
    print("OK Engine: eigene Muster, Wasser plus Strom loest den Kurzschluss aus")
    k["gegner"][1]["aus"] = "ko"
    k["gegner"][1]["lp"] = 0
    for g in kampf.lebend(k):
        if len(kampf.lebend(k)) == 1 and g["def"].get("pattern_allein"):
            g["pattern"] = g["def"]["pattern_allein"]
    assert k["gegner"][0]["pattern"] == allein
    print("OK Faellt Charly, gilt Bibis Muster fuer allein")

    # Phase 2: Eigenheiten
    z = T.new("rt_1_bibi_charly")
    k = z["kampf"]
    assert k["gegner"][0]["armor"] == kampf.enemy_stats(b, k["gegner"][0]["level"], k["spieler"]["level"])["armor"] + 1
    bibi = k["gegner"][0]
    bibi["absicht"] = "s1"
    f0 = bibi["fassung"]
    ctx = T.ctx(z)
    ctx["g"] = bibi
    kampf._hit(ctx)
    assert bibi["absicht"] == "n" and bibi["fassung"] == f0 - kampf.UNTERBROCHEN_FASSUNG
    print("OK Danzels Einlagen +1 Schutz; ein Treffer unterbricht Nervous Laugh")

    z = T.new("rt_4a_mufflon")
    g = z["kampf"]["gegner"][0]
    assert kampf._mult({"kind": "stumpf"}, g) > 1 > kampf._mult({"kind": "klinge"}, g)
    print("OK Panzer-Mufflon: Wucht stark, Klinge schwach")

    z = T.new("rt_4b_hyaenen")
    k = z["kampf"]
    ctx = T.ctx(z)
    ctx["g"] = k["gegner"][0]
    k["gegner"][0]["absicht"] = "w1"
    kampf._enemy_turn(ctx)
    assert all(x["states"].get("buff_atk") for x in k["gegner"][1:]) and not k["gegner"][0]["states"].get("buff_atk")
    print("OK Alpha heult: der Rest des Rudels trifft haerter")

    # Beistand: versoehnt Wasser, Taser, Platte; getrennt nur alle 3 Runden die Platte
    for flags, erwartet in ((["rt_ausgang_alle"], ("Bibi", "Charly", "Danzel")), ([], (None, None, "Danzel"))):
        z = T.new(start=False)
        z["flags"] += flags
        kampf.starten(z, T.DEFS, "rt_7a_garten", rng=T.NO)
        k = z["kampf"]
        assert [(x or {}).get("wer") for x in k["def"]["beistand"]] == list(erwartet), k["def"]["beistand"]
    z = T.new(start=False)
    z["flags"].append("rt_ausgang_alle")
    kampf.starten(z, T.DEFS, "rt_7a_garten", rng=T.NO)
    k = z["kampf"]
    ziel = kampf.ziel_gegner(k)
    lp0 = ziel["lp"]
    ctx = T.ctx(z)
    kampf._beistand(ctx)
    assert ziel["states"].get("nass") and ziel["lp"] < lp0
    k["runde"] = 2
    ctx = T.ctx(z)
    kampf._beistand(ctx)
    assert ziel["states"].get("skip") and not ziel["states"].get("nass"), ziel["states"]
    k["runde"] = 3
    ctx = T.ctx(z)
    kampf._beistand(ctx)
    assert k["spieler"]["halve_next"]
    print("OK Beistand: Wasser, Taser = Kurzschluss, Platte; getrennt nur die Platte")
    print("OK")


if __name__ == "__main__":
    main()
