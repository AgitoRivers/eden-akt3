# -*- coding: utf-8 -*-
"""Missionsregeln aus Paket 1 (18.10.2026) mit festen Wuerfeln: Fehlschlag -> morgen noch einmal, zweiter Fehlschlag
halber Lohn und vorbei; Wege einer Gruppe; nach= auf Gruppe; Abgabe; Werkzeug; persoenlich -> Begehren.
Missionsausbau (18.10.2026): Teile nur fuer offene Auftraege, Besorgungstasche (3), Auftrag bleibt offen, Kette.

  python tests\\test_missionen.py
"""
import copy, os, sys, tempfile

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import lauf_test as L  # noqa: E402

E = L.eden
H = E.handel


def basis():
    L.vorbereiten("eden_rise", tempfile.mkdtemp(prefix="eden_mis_"))
    E.modul_laden()["schnelljobs"] = True        # eden_rise hat die Schnelljobs abgeschaltet (29.10.2026); hier wird die Mechanik geprueft
    L.random.seed(11)
    protokoll = {"schritte": [], "erledigt": {}}
    z = E.aktion("neu", {"modus": "ironman"})
    while not (z["tag"] >= 3 and z["status"] == "wahl"):
        a = L.schritt(z, protokoll)
        if a[0] != "_tagesarbeit":
            L.versuch(a, protokoll)
        z = E.aktiv()
    return z


def wuerfel_fest(*werte):
    """Naechste W20-Wuerfe festlegen (danach wieder zufaellig)."""
    liste = list(werte)
    alt = E.wuerfel.random.randint
    E.wuerfel.random.randint = lambda a, b: liste.pop(0) if liste else alt(a, b)


def angebot(z, *ids):
    jobs = E.showrunner.vorrat(E.moddir())["jobs"]
    out = []
    for jid in ids:
        g = next(j.get("gruppe") for j in jobs if j["id"] == jid)
        out += [j["id"] for j in jobs if j["id"] == jid or (g and j.get("gruppe") == g)]
    z["jobs_tag"] = {"tag": z["tag"], "ids": list(dict.fromkeys(out))}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    z0 = basis()                                  # zuerst: L.vorbereiten leert den Cache, das Modul wird neu geladen
    modul, V = E.modul_laden(), E.showrunner.vorrat(E.moddir())

    # 1) Fehlschlag: heute weg, morgen wieder; zweiter Fehlschlag halber Lohn und vorbei
    z = copy.deepcopy(z0)
    z["jobs_erfolg"] = z.get("jobs_erfolg", []) + ["nets"]
    z["werte"]["energie"] = 3
    angebot(z, "alva_kassenbuch")
    k0 = z["konto"]
    wuerfel_fest(2)
    r = H.job_machen(z, modul, V, "alva_kassenbuch")
    assert not r["ok"] and z["konto"] == k0, "erster Fehlschlag: kein Lohn"
    assert "alva_kassenbuch" not in [j["id"] for j in H.jobs_heute(z, modul, V)], "heute nicht mehr"
    z["tag"] += 1
    z["werte"]["energie"] = 3
    angebot(z, "alva_kassenbuch")
    j = next(j for j in H.jobs_heute(z, modul, V) if j["id"] == "alva_kassenbuch")
    assert j["versuch"] == 2, j["versuch"]
    wuerfel_fest(2)
    r = H.job_machen(z, modul, V, "alva_kassenbuch")
    assert not r["ok"] and z["konto"] == k0 + 60 and "alva_kassenbuch" in z["jobs_erledigt"], "zweiter: halber Lohn, vorbei"
    print("OK Fehlschlag -> morgen noch einmal -> halber Lohn")

    # 2) Kette laeuft nach einem Fehlschlag weiter
    z = copy.deepcopy(z0)
    z["jobs_erfolg"] = z.get("jobs_erfolg", []) + ["nets"]
    z["werte"]["energie"] = 3
    angebot(z, "petru_motor_1")
    wuerfel_fest(2, 2)
    H.job_machen(z, modul, V, "petru_motor_1")
    z["tag"] += 1
    z["werte"]["energie"] = 3
    angebot(z, "petru_motor_1")
    wuerfel_fest(19, 19)
    assert H.job_machen(z, modul, V, "petru_motor_1")["ok"]
    angebot(z, "petru_motor_2")
    assert "petru_motor_2" in [j["id"] for j in H.jobs_heute(z, modul, V)], "Teil 2 nach Erfolg im zweiten Anlauf"
    print("OK Kette nach Fehlschlag")

    # 3) Gruppe: Wege zusammen, Fehlschlag laesst andere offen, Erfolg schliesst sie; nach= auf Gruppe
    z = copy.deepcopy(z0)
    z["werte"]["energie"] = 3
    z["konto"] = 500
    angebot(z, "alva_kuehlung_reparatur")
    wege = [j["id"] for j in H.jobs_heute(z, modul, V) if j.get("gruppe") == "alva_kuehlung"]
    assert len(wege) == 4, wege
    wuerfel_fest(2, 2)
    H.job_machen(z, modul, V, "alva_kuehlung_reparatur")
    offen = [j["id"] for j in H.jobs_heute(z, modul, V) if j.get("gruppe") == "alva_kuehlung"]
    assert offen == ["alva_kuehlung_eis", "alva_kuehlung_toto", "alva_kuehlung_relais"], offen
    r = H.job_machen(z, modul, V, "alva_kuehlung_eis")
    assert r["ok"] and r["probe"] is None and z["konto"] == 440, "Eis: sicher, kostet 60"
    assert not [j for j in H.jobs_heute(z, modul, V) if j.get("gruppe") == "alva_kuehlung"], "Gruppe geschlossen"
    alva_diesel = next(j for j in V["jobs"] if j["id"] == "alva_diesel")
    assert H.job_frei(dict(z, tag=4), modul, alva_diesel), "nach=alva_kuehlung offen"
    print("OK Wege einer Gruppe")

    # 4) Abgabe: ohne Gegenstand gesperrt, mit Gegenstand sicher und ohne Energie
    z = copy.deepcopy(z0)
    z["werte"]["energie"] = 0
    angebot(z, "rosi_ersatzbatterie")
    try:
        H.job_machen(z, modul, V, "rosi_ersatzbatterie")
        raise AssertionError("ohne Batterie haette es nicht gehen duerfen")
    except ValueError:
        pass
    H.tasche(z).append("ersatzzellen")
    r = H.job_machen(z, modul, V, "rosi_ersatzbatterie")
    assert r["ok"] and "ersatzzellen" not in H.tasche(z), "Abgabe ohne Energie, aus der Besorgungstasche"
    print("OK Abgabe")

    # 4b) Teile: nur fuer offene Auftraege kaufbar, landen in der Tasche (3 Plaetze), Auftrag bleibt offen
    z = copy.deepcopy(z0)
    z["konto"] = 2000
    z.pop("jobs_tag", None)
    z["auftraege"] = []
    teil_bei = lambda lid: [w["id"] for w in (H.sortiment(z, modul, lid) or []) if w["art"] == "teil"]
    assert "ersatzzellen" not in teil_bei("toto"), "ohne Auftrag kein Teil im Laden"
    angebot(z, "rosi_ersatzbatterie")
    H.annehmen(z, modul, V, ["rosi_ersatzbatterie"])
    assert "ersatzzellen" in teil_bei("toto"), "mit offenem Auftrag im Laden"
    zeilen = H.kaufen(z, modul, "toto", "ersatzzellen")
    assert "ersatzzellen" in H.tasche(z) and "ersatzzellen" not in z["inventar"], "Teil in die Tasche"
    assert "ersatzzellen" not in teil_bei("toto"), "nicht doppelt kaufbar"
    z["jobs_tag"] = {"tag": z["tag"] + 1, "ids": []}
    z2 = dict(z, tag=z["tag"] + 1)
    assert "rosi_ersatzbatterie" in [j["id"] for j in H.jobs_heute(z2, modul, V)], "Auftrag bleibt am naechsten Tag offen"
    z["tasche"] = ["relais", "tonerde", "safran"]
    try:
        z["auftraege"] += ["petru_schild_1"]
        z["bekannt"] = list(set(z.get("bekannt", [])) | {"petru"})
        H.kaufen(z, modul, "alva", "eichenbrett")
        raise AssertionError("volle Tasche haette sperren muessen")
    except ValueError:
        pass
    print("OK Teile (nur mit Auftrag, Tasche 3, bleibt offen)")

    # 4c) Kette: nach Erfolg ist die Fortsetzung ein offener Auftrag
    z = copy.deepcopy(z0)
    z["bekannt"] = list(set(z.get("bekannt", [])) | {"petru"})
    z["auftraege"] = []
    angebot(z, "petru_schild_1")
    H.tasche(z).append("eichenbrett")
    assert H.job_machen(z, modul, V, "petru_schild_1")["ok"]
    assert "petru_schild_2" in z["auftraege"], "Fortsetzung offen"
    assert "petru_schild_2" in [j["id"] for j in H.jobs_heute(z, modul, V)], "Fortsetzung im Angebot"
    print("OK Kette")

    # 5) Werkzeug: Vorteil bzw. +2 obendrauf
    z = copy.deepcopy(z0)
    z["jobs_erfolg"] = z.get("jobs_erfolg", []) + ["nets"]
    angebot(z, "petru_motor_1")
    ohne = next(j for j in H.jobs_heute(z, modul, V) if j["id"] == "petru_motor_1")
    z["inventar"].append("multitool")
    mit = next(j for j in H.jobs_heute(z, modul, V) if j["id"] == "petru_motor_1")
    assert mit["werkzeug_da"] == "multitool" and mit["chance"] > ohne["chance"], (ohne["chance"], mit["chance"])
    assert mit["werkzeug_bonus"] == (2 if ohne["vorteil"] else 0)
    print("OK Werkzeug (%d %% -> %d %%)" % (ohne["chance"], mit["chance"]))

    # 6) persoenlich: Begehren nur dann
    for jid, soll in (("siri_photos", True), ("chiara_coldroom", False)):
        z = copy.deepcopy(z0)
        z["werte"]["energie"] = 3
        z.get("bekannt", []).append(next(j["von"] for j in V["jobs"] if j["id"] == jid))
        angebot(z, jid)
        pid = next(j["von"] for j in V["jobs"] if j["id"] == jid)
        b0 = E.zustand.punkte(z, "begehren." + pid)
        v0 = E.zustand.punkte(z, "vertrauen." + pid)
        wuerfel_fest(19, 19)
        assert H.job_machen(z, modul, V, jid)["ok"]
        stieg = E.zustand.punkte(z, "begehren." + pid) > b0
        assert stieg == soll, "%s: Begehren %s" % (jid, stieg)
        assert E.zustand.punkte(z, "vertrauen." + pid) > v0, "Vertrauen immer"
        print("OK %s: Vertrauen ja, Begehren %s" % (jid, "ja" if soll else "nein"))
    print("OK")


if __name__ == "__main__":
    main()
