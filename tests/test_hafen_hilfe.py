# -*- coding: utf-8 -*-
r"""Rosi's help in the harbour fight (Duc 30.10.2026): after the first defeat once a voiced hint, 3 plasters, a water and a shock
grenade; the wave restarts with full life, a second defeat restarts it without her; water + shock on one animal is a short circuit.

  python tests\test_hafen_hilfe.py
"""
import os, sys, tempfile

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import lauf_test as L  # noqa: E402

E = L.eden


def bis_zur_welle():
    L.vorbereiten("eden_rise", tempfile.mkdtemp(prefix="eden_hafenhilfe_"), 7)
    L.random.seed(7)
    prot = {"schritte": [], "erledigt": {}}
    E.aktion("neu", {"modus": "ironman"})
    for _ in range(L.MAX_SCHRITTE):
        z = E.aktiv()
        if z["status"] == "kampf" and z["kampf"].get("definition") == "hafen_ratten":
            return z
        a = L.schritt(z, prot)
        assert a is not None, "Bot-Lauf endete vor dem Hafen"
        L.tagesarbeit(z, prot) if a[0] == "_tagesarbeit" else L.versuch(a, prot)
    raise AssertionError("Hafen nicht erreicht")


def verlieren():
    """Duc takes every blow with one life left, then the fight is closed."""
    for _ in range(60):
        z = E.aktiv()
        k = z["kampf"]
        if k["phase"] == "ende":
            assert k["ergebnis"]["art"] == "niederlage", k["ergebnis"]["art"]
            E.aktion("kampf_schliessen", {})
            return
        k["spieler"]["lp"] = 1
        E.sichern(z)
        if k["phase"] == "parade":
            E.aktion("kampf_parade", {"ergebnis": "verfehlt", "revision": k["revision"]})
        elif k["phase"] == "spieler_wahl":
            E.aktion("kampf_zug", {"befehl": "verteidigen", "ziel": None, "revision": k["revision"]})
        else:
            E.aktion("kampf_zug", {"befehl": "aussetzen", "ziel": None, "revision": k["revision"]})
    raise AssertionError("Kampf endet nicht")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    z = bis_zur_welle()
    pflaster_vorher = z["inventar"].count("plaster")
    verlieren()
    z = E.aktiv()
    assert z["status"] == "ereignis" and z["event"]["id"] == "hk_tipp_ratten", (z["status"], z.get("event"))
    v = E.ansicht(z)["z"]["ereignis"]
    assert len(v["zeilen"]) == 4 and v["bild"], "Rosis Szene unvollstaendig"
    E.aktion("event_wahl", {"index": 0})
    E.aktion("event_schliessen", {})
    z = E.aktiv()
    assert z["status"] == "kampf" and z["kampf"]["definition"] == "hafen_ratten", "Welle startet nicht neu: %s" % z["status"]
    assert z["kampf"]["spieler"]["lp"] == z["kampf"]["spieler"]["lp_max"], "keine vollen Leben"
    assert z["inventar"].count("plaster") == pflaster_vorher + 3, "drei Pflaster fehlen"
    assert z["inventar"].count("grenade_water") == 1 and z["inventar"].count("grenade_shock") == 1, "Granaten fehlen"
    assert "hafen_hilfe_bekommen" in z["flags"]

    # the combination Rosi explains really works and the enemy skips
    k = z["kampf"]
    E.aktion("kampf_zug", {"befehl": "gegenstand", "ziel": "grenade_water", "revision": k["revision"]})
    for _ in range(12):
        z = E.aktiv()
        k = z["kampf"]
        if k["phase"] == "spieler_wahl":
            break
        E.aktion("kampf_parade", {"ergebnis": "perfekt", "revision": k["revision"]}) if k["phase"] == "parade" else None
    lp_vor = sum(g["lp"] for g in k["gegner"])
    E.aktion("kampf_zug", {"befehl": "gegenstand", "ziel": "grenade_shock", "revision": k["revision"]})
    z = E.aktiv()
    k = z["kampf"]
    text = " ".join(str(x) for x in k.get("log", []))
    assert "short circuit" in text.lower() or "kurzschluss" in text.lower(), "kein Kurzschluss im Kampflog"
    assert sum(g["lp"] for g in k["gegner"]) < lp_vor

    # a second defeat: straight back into the wave, Rosi only helps once
    verlieren()
    z = E.aktiv()
    assert z["status"] == "kampf" and z["kampf"]["definition"] == "hafen_ratten", "zweite Niederlage: %s" % z["status"]
    assert not z.get("event"), "Rosi kommt ein zweites Mal"

    # winning the wave still leads to the next frame of the chain
    for _ in range(200):
        z = E.aktiv()
        if z["status"] != "kampf":
            break
        k = z["kampf"]
        if k["phase"] == "ende":
            E.aktion("kampf_schliessen", {})
        elif k["phase"] == "parade":
            E.aktion("kampf_parade", {"ergebnis": "perfekt", "revision": k["revision"]})
        else:
            E.aktion("kampf_zug", {"befehl": "angriff", "ziel": None, "revision": k["revision"]})
    z = E.aktiv()
    assert (z.get("event") or {}).get("id") == "hk_petru", z.get("event")
    print("OK Rosis Hilfe im Hafen: einmalig, volle Leben, 3 Pflaster + 2 Granaten, Kurzschluss, Kette laeuft weiter")


if __name__ == "__main__":
    main()
