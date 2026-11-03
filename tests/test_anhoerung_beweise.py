# -*- coding: utf-8 -*-
"""Anhoerung Option A (Duc 28.10.2026): garantierte Kernbeweise What/Why, Fall-Tafel, Notizen gegen falsche Zeilen
(Beweissatz + beruehrt), Ablehnung mit Grund. Spoilerfrei: gibt keine Namen, Fakten oder Saetze aus.

  python tests\\test_anhoerung_beweise.py
"""
import copy, os, sys, tempfile

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import lauf_test as L  # noqa: E402

E = L.eden
A = E.anhoerung
M = E.ermittlung
ABLEHNUNG = ("falsche_karte", "anderer_punkt", "nur_aussage", "andere_behauptung", "warum_nicht")


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def fall_stand(z0, nr, tag, phase="abend"):
    k = copy.deepcopy(z0)
    k["wahrheit"] = "fall_%d" % nr
    k["ermittlung"] = {}
    k["tag"], k["phase"] = tag, phase
    return k


def glied(k, gid):
    return next(g for g in M.glieder_status(k) if g["id"] == gid)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    L.vorbereiten("eden_rise", tempfile.mkdtemp(prefix="eden_beweise_"))
    z0 = E.aktion("neu", {"modus": "ironman"})
    modul = E.modul_laden()

    # 1) What und Why ohne eine einzige freiwillige Aktion belegbar - in jedem Fall; Who nie geschenkt
    for nr in range(1, 6):
        k = fall_stand(z0, nr, 4)
        zeilen = M.pflicht_beweise(k, {"def": {"id": "reparaturschritt"}})
        pruefen(glied(k, "handlung")["belegt"] and zeilen and all(z.startswith("📌") for z in zeilen),
                "Fall %d: Tag 4, Rosis Whiteboard belegt What" % nr)
        k["tag"], k["phase"] = 5, "fruehstueck"
        M.pflicht_beweise(k, {"def": {"id": "megan_kommt"}})
        pruefen(glied(k, "folge")["belegt"] and not glied(k, "person")["belegt"],
                "Fall %d: Tag 5, Megans Mappe belegt Why - Who bleibt offen" % nr)

    # 2) verpasste Szene: am naechsten Tag nachgeliefert, am Tag selbst nur in der Szene
    k = fall_stand(z0, 1, 4)
    pruefen(not M.pflicht_beweise(k, None), "Tag 4 ohne Rosis Szene: noch nichts")
    k["tag"] = 5
    M.pflicht_beweise(k, None)
    pruefen(glied(k, "handlung")["belegt"], "Szene verpasst: What kommt am Tag danach")

    # 3) nichts doppelt: ist der Punkt schon belegt, liefert der Pflicht-Moment nichts
    k = fall_stand(z0, 2, 4)
    g = next(g for g in M.fall(k)["glieder"] if g["id"] == "handlung")
    anderer = [s for i, s in enumerate(g["beweis_saetze"]) if i != g.get("kern")]
    if anderer:
        for fid in anderer[0]:
            M._lernen(k, fid, "test")
        vorher = len(M.stand(k)["bekannt"])
        M.pflicht_beweise(k, {"def": {"id": "reparaturschritt"}})
        pruefen(len(M.stand(k)["bekannt"]) == vorher, "Punkt schon belegt: keine Pflicht-Notiz zusaetzlich")

    # 4) Fall-Tafel: Open -> Partly -> Proven, nur Kategorie-Saetze, ein Proven-Hinweis genau einmal
    k = fall_stand(z0, 1, 3)
    erlaubt = {s for paar in M.TAFEL_STAPEL.values() for s in paar}
    t = M.tafel(k, modul)
    pruefen(len(t) == 3 and all(x["stand"] == "open" and x["fehlt"] and set(x["fehlt"]) <= erlaubt for x in t),
            "Tafel ohne Notizen: drei offene Fragen, nur Kategorie-Saetze")
    g = next(g for g in M.fall(k)["glieder"] if g["id"] == "folge")
    kern = g["beweis_saetze"][g["kern"]]
    if len(kern) > 1:
        M._lernen(k, kern[0], "test")
        x = next(x for x in M.tafel(k, modul) if x["id"] == "folge")
        pruefen(x["stand"] == "partly" and x["x"] >= 1 and x["y"] >= 2, "ein Teil gefunden: Partly x von y")
    for fid in kern:
        M._lernen(k, fid, "test")
    pruefen(next(x for x in M.tafel(k, modul) if x["id"] == "folge")["stand"] == "proven", "Beweissatz komplett: Proven")
    meld = M.belegt_melden(k)
    pruefen(meld and all(m.startswith("✔") for m in meld) and not M.belegt_melden(k), "Sprung auf Proven: Meldung genau einmal")
    pruefen(A.tafel_tipp(k, modul, "folge") and A.tafel_tipp(k, modul, "person"), "derselbe Tipp vor jedem Punkt")

    # 5) Notizen gegen falsche Zeilen: Beweissatz + beruehrt zaehlt, sonst Grund statt Pauschale
    daten = A._aussagen_daten(dict(fall_stand(z0, 1, 7), wahrheit="fall_1"))
    beruehrte, gruende = 0, 0
    for r, runde in daten["runden"].items():
        for nb, liste in ((0, runde["saetze"]), (1, (runde.get("nachbessern") or {}).get("saetze", []))):
            for s in liste:
                if not s["falsch"]:
                    continue
                for fid in s.get("beruehrt", []):
                    beruehrte += 1
                    pruefen(A._beruehrt(s, fid, "luecke"), "beruehrte Notiz zaehlt (Fall 1, %s)" % r)
                for fid in s.get("warum_nicht", {}):
                    gruende += 1
                    pruefen(not A._beruehrt(s, fid, "luecke"), "Notiz mit eigenem Grund zaehlt nicht (Fall 1, %s)" % r)
    pruefen(beruehrte and gruende, "Fall 1 hat beruehrte Notizen und eigene Gruende")

    # 6) Ablehnung ueber die echte Verhandlung: eigener Grund bzw. Kategorie, je -1 Ader
    k = fall_stand(z0, 1, 7)
    for fid in M.fakten(k):
        M._lernen(k, fid, "test")
    A.verhandlung_beginnen(k, modul)
    v = k["verhandlung"]
    i = next(j for j, s in enumerate(v["aussage"]["saetze"]) if s["falsch"])
    s = v["aussage"]["saetze"][i]
    fremd = next(f for f in sorted(M.stand(k)["bekannt"]) if A._karte_passt(k, "handlung", f) == "nein"
                 and "handlung" not in A.themen(k, f, M.fakten(k)[f]))
    a0 = v["adern"]
    A.verhandlung_present(k, modul, fremd, i)
    pruefen(v["adern"] == a0 - 1 and v["log"][-1]["art"] == "anderer_punkt", "Notiz zu einem anderen Punkt: Grund 'other point'")
    beruehrt = next((f for f in s.get("beruehrt", []) if f not in s["widerlegt"]), None)
    if beruehrt:
        k2 = copy.deepcopy(k)
        a1 = k2["verhandlung"]["adern"]
        A.verhandlung_present(k2, modul, beruehrt, i)
        pruefen(k2["verhandlung"]["adern"] == a1 and k2["verhandlung"]["log"][-1]["art"] != "anderer_punkt",
                "beruehrte Notiz statt der eingetragenen: zaehlt (kein Aderverlust)")

    # 7) Gefuehrte erste Zeile (29.10.2026): die Ansicht nennt nur in Punkt 1, erste Aussage, die Zeile fuer die Fuehrung
    k = fall_stand(z0, 1, 7)
    k["persona"] = k.get("persona") or {"attribute": {}}
    for fid in M.fakten(k):
        M._lernen(k, fid, "test")
    A.verhandlung_beginnen(k, modul)
    ans = A.verhandlung_ansicht(k, modul, lambda pid, g: None)
    falsch = next(i for i, s in enumerate(k["verhandlung"]["aussage"]["saetze"]) if s["falsch"])
    pruefen(ans["fuehrung"] == falsch, "Punkt 1: die Fuehrung zeigt auf die falsche Zeile")
    s = k["verhandlung"]["aussage"]["saetze"][falsch]
    A.verhandlung_present(k, modul, next(f for f in s["widerlegt"] if A._karte_passt(k, "handlung", f) == "ja"), falsch)
    pruefen(A.verhandlung_ansicht(k, modul, lambda pid, g: None)["fuehrung"] is None,
            "nach dem ersten Treffer (nachgebesserte Aussage): keine Fuehrung mehr")
    print("OK")


if __name__ == "__main__":
    main()
