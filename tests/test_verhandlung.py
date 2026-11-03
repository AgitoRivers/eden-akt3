# -*- coding: utf-8 -*-
"""Spielbare Anhoerung (Variante B, 25.10.2026): Status 'verhandlung' startet mit der Szene 'anhoerung', drei Runden
(Present/Press/Bluff/Joker/Aufgeben), Megans Adern, danach Rolle/Plaedoyer/Urteil wie bisher. Spoilerfrei: gibt keine
Namen oder Fakten aus.

  python tests\\test_verhandlung.py
"""
import copy, os, sys, tempfile

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import lauf_test as L  # noqa: E402

E = L.eden
A = E.anhoerung


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def falsch_satz(z):
    return next(i for i, s in enumerate(z["verhandlung"]["aussage"]["saetze"]) if s["falsch"])


def richtige_karte(z, r):
    s = z["verhandlung"]["aussage"]["saetze"][falsch_satz(z)]
    return next(f for f in sorted(E.ermittlung.stand(z)["bekannt"])
                if A._karte_passt(z, r, f) == "ja" and (not s.get("widerlegt") or f in s["widerlegt"]))


def beweisen(z, r):
    """Present bis der Punkt entschieden ist (seit 26.10. zwei Aussagen je Punkt, wenn der Fall nachbessert)."""
    runde = z["verhandlung"]["runde"]
    for _ in range(3):
        z = E.aktion("verhandlung", {"was": "present", "fid": richtige_karte(z, r), "satz": falsch_satz(z)})
        if z["verhandlung"]["runde"] != runde or z["verhandlung"]["schritt"] != "aussage" or z["verhandlung"]["fertig"]:
            break
        pruefen(z["verhandlung"]["aussage"].get("stufe") == 1 and any(e["art"] == "nachbessern" for e in
                z["verhandlung"]["log"][-6:]), "Punkt %s: erster Treffer - der Zeuge bessert nach" % r)
    return z


def fall_durchspielen(z0, modul, nr):
    """Fall nr an einer Kopie: Duc kennt jede Spur, beweist je Punkt beide Aussagen mit den Gegenbeweisen der Falldaten,
    klagt die Verantwortliche an - am Ende stehen drei bewiesene Punkte und ihr Gestaendnis (spoilerfrei)."""
    k = copy.deepcopy(z0)
    k["wahrheit"] = "fall_%d" % nr
    k["ermittlung"]["gestaendnis"] = None              # ein Gestaendnis aus der Bot-Woche (Fall 1) gilt nicht fuer Fall nr
    for fid in E.ermittlung.fakten(k):
        E.ermittlung._lernen(k, fid, "test")
    A.verhandlung_beginnen(k, modul)
    v = k["verhandlung"]
    treffer = 0
    for _ in range(12):
        if v["fertig"] or v["schritt"] == "rolle":
            break
        if v["schritt"] == "anklage":
            A.verhandlung_anklage(k, modul, E.ermittlung.fall(k)["verantwortlich"])
            continue
        r = A._runde(v)
        s = v["aussage"]["saetze"][falsch_satz(k)]
        fid = next(f for f in s["widerlegt"] if A._karte_passt(k, r, f) == "ja")
        A.verhandlung_present(k, modul, fid, falsch_satz(k))
        treffer += 1
    pruefen(v["schritt"] == "rolle" and treffer == 6 and all(x == "beweis" for x in v["runden"].values())
            and sum(1 for e in v["log"] if e["art"] == "gestaendnis") >= 4,
            "Fall %d: sechs Gegenbeweise, drei Punkte bewiesen, Gestaendnis" % nr)


# Ablehnung mit Grund (28.10.2026): Pauschale oder eine der drei Kategorien bzw. der eigene Satz aus den Falldaten
ABLEHNUNG = ("falsche_karte", "anderer_punkt", "nur_aussage", "andere_behauptung", "warum_nicht")


def falsche_karte(z, r):
    return next(f for f in sorted(E.ermittlung.stand(z)["bekannt"]) if A._karte_passt(z, r, f) == "nein")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    L.vorbereiten("eden_rise", tempfile.mkdtemp(prefix="eden_verh_"))
    L.random.seed(11)
    prot = {"schritte": [], "erledigt": {}}
    z = E.aktion("neu", {"modus": "ironman"})
    z["wahrheit"] = "fall_1"                           # Fall mit eigenen Aussagen (anhoerung_aussagen.json)
    E.sichern(z)
    for _ in range(3000):
        if z["status"] == "verhandlung":
            break
        a = L.schritt(z, prot)
        if a is None:
            break
        if a[0] == "_tagesarbeit":
            L.tagesarbeit(z, prot)
        else:
            L.versuch(a, prot)
        z = E.aktiv()
    pruefen(z["status"] == "verhandlung" and z["tag"] == 7, "Tag 7: die Anhörungs-Szene startet die Verhandlung")
    modul = E.modul_laden()
    v = E.ansicht(z)["z"]["verhandlung"]
    pruefen(v and v["runde"] == 0 and v["adern"] >= 2 and v["log"], "Ansicht: Runde 1, Adern, Megans erste Aussage")

    # Duc kennt fuer den Test jede Spur (Abkuerzung, keine Ausgabe der Inhalte)
    for fid in E.ermittlung.fakten(z):
        E.ermittlung._lernen(z, fid, "test")
    E.sichern(z)

    # --- Nebenpfade an einer Kopie: Bluff gelingt / misslingt, Joker, Aufgeben, Adern auf 0
    k = copy.deepcopy(z)
    w = E.wuerfel.probe
    E.wuerfel.probe = lambda att, sg, boni, vorteil=False: {"ergebnis": "erfolg", "wurf": 15, "summe": 18, "boni": boni}
    A.verhandlung_bluff(k, modul)
    pruefen(k["verhandlung"]["runden"]["handlung"] == "bluff" and k["verhandlung"]["schritt"] == "anklage",
            "gelungener Bluff gewinnt die Runde, weiter zur Anklage")
    k2 = copy.deepcopy(z)
    E.wuerfel.probe = lambda att, sg, boni, vorteil=False: {"ergebnis": "fehlschlag", "wurf": 3, "summe": 5, "boni": boni}
    a0 = k2["verhandlung"]["adern"]
    A.verhandlung_bluff(k2, modul)
    pruefen(k2["verhandlung"]["runden"]["handlung"] == "verloren" and k2["verhandlung"]["adern"] == a0 - 2,
            "misslungener Bluff: Runde verloren, −2 Adern")
    E.wuerfel.probe = w
    k3 = copy.deepcopy(z)
    k3["verhandlung"]["adern"] = 1
    A.verhandlung_present(k3, modul, falsche_karte(k3, "handlung"), falsch_satz(k3))
    pruefen(k3["verhandlung"]["fertig"] and set(k3["verhandlung"]["runden"].values()) == {"verloren"},
            "letzte Ader weg: Megan bricht ab, alle offenen Runden verloren")
    k4 = copy.deepcopy(z)
    item = next(iter(modul["items"]))
    modul["items"][item]["anhoerung_ader"] = 1
    k4["inventar"].append(item)
    a0 = k4["verhandlung"]["adern"]
    A.verhandlung_joker(k4, modul, item)
    pruefen(k4["verhandlung"]["adern"] == a0 + 1 and item not in k4["inventar"], "Joker: +1 Ader, Gegenstand verbraucht")
    del modul["items"][item]["anhoerung_ader"]
    k5 = copy.deepcopy(z)                              # Teilbeweis: Zettel gehoert dazu, der Rest fehlt -> keine Ader
    A._aussage_bauen(k5, modul, k5["verhandlung"], "handlung", stufe=1)   # nachgebesserte Aussage (Tuer offen)
    bek = E.ermittlung.stand(k5)["bekannt"]
    for fid in ("f1_05", "f1_02"):
        bek.pop(fid, None)
    a0 = k5["verhandlung"]["adern"]
    A.verhandlung_present(k5, modul, "f1_06", falsch_satz(k5))
    pruefen(k5["verhandlung"]["adern"] == a0 and k5["verhandlung"]["runde"] == 0
            and k5["verhandlung"]["log"][-1]["art"] == "luecke", "Teilbeweis: Megan fragt nach, keine Ader")
    for nr in (2, 3, 4, 5):                            # seit 27.10.2026 hat jeder Fall eigene Aussagen
        fall_durchspielen(z, modul, nr)

    # --- Hauptpfad ueber die echte Aktion: falsche Karte (−1), Press, richtige Karten, richtige Person
    pruefen(len(E.ansicht(z)["z"]["verhandlung"]["aussage"]["saetze"]) == 3, "Runde 1: Aussage aus drei Zeilen")
    wahr = next(i for i, s in enumerate(z["verhandlung"]["aussage"]["saetze"]) if not s["falsch"])
    z = E.aktion("verhandlung", {"was": "press", "satz": wahr})
    pruefen(z["verhandlung"]["log"][-1]["art"] == "bestaetigt", "Ask auf eine wahre Zeile: 'fits your note'")
    a0 = z["verhandlung"]["adern"]
    z = E.aktion("verhandlung", {"was": "present", "fid": richtige_karte(z, "handlung"), "satz": wahr})
    pruefen(z["verhandlung"]["adern"] == a0 - 1 and z["verhandlung"]["log"][-1]["art"] == "satz_haelt",
            "richtiger Zettel, aber wahre Zeile: −1 Ader, Megan sagt, die Zeile stimmt")
    z = E.aktion("verhandlung", {"was": "present", "fid": falsche_karte(z, "handlung"), "satz": falsch_satz(z)})
    pruefen(z["verhandlung"]["adern"] == a0 - 2 and z["verhandlung"]["log"][-1]["art"] in ABLEHNUNG,
            "falsche Zeile erkannt, falscher Zettel: −1 Ader, Megan nennt die Zeile")
    z = E.aktion("verhandlung", {"was": "press", "satz": falsch_satz(z)})
    pruefen(z["verhandlung"]["log"][-1]["art"] == "gedanke" and E.ansicht(z)["z"]["verhandlung"]["tipp_stapel"],
            "Press auf die falsche Zeile: Duc stutzt, ein Stapel leuchtet")
    z = beweisen(z, "handlung")
    pruefen(z["verhandlung"]["schritt"] == "anklage", "richtige Karte: Runde gewonnen, jetzt die Anklage")
    v_ok = (E.ermittlung.fall(z) or {}).get("verantwortlich") or A.NIEMAND
    z = E.aktion("verhandlung", {"was": "anklage", "pid": v_ok})
    if z["verhandlung"]["runden"].get("person") != "gestaendnis":
        pruefen(z["verhandlung"]["aussage"]["sprecher"] == v_ok, "Runde 2: die Angeklagte sagt selbst aus")
        arten = [e["art"] for e in z["verhandlung"]["log"]]
        pruefen("titel" in arten[-11:] and (v_ok not in A.REAKTION or "reaktion" in arten[-11:]),
                "Punkt 2: Reaktion und Titelkarte 'Testimony of …' vor der Aussage")
        z = E.aktion("verhandlung", {"was": "press", "satz": falsch_satz(z)})
        if v_ok in A.NERVOES:
            pruefen(any(e["art"] == "nervoes" for e in z["verhandlung"]["log"][-3:]),
                    "Punkt 2: Nachhaken bei der falschen Zeile macht die Angeklagte nervoes")
        z = beweisen(z, "person")
        if v_ok in A.ZUSAMMENBRUCH:
            pruefen(sum(1 for e in z["verhandlung"]["log"] if e["art"] == "zusammenbruch") == 2,
                    "Punkt 2: OBJECTION! - die Angeklagte bricht zusammen")
    if z["verhandlung"]["runden"].get("folge") != "gestaendnis" and not z["verhandlung"]["fertig"]:
        pruefen(any(e["art"] == "kette" and e.get("zustand") == "auf" for e in z["verhandlung"]["log"]),
                "Punkt 3: das Kettenbrett zeigt die zwei bewiesenen Punkte")
        z = beweisen(z, "folge")
    pruefen(z["verhandlung"]["schritt"] == "rolle" and all(x in ("beweis", "gestaendnis") for x in
                                                            z["verhandlung"]["runden"].values()),
            "alle drei Runden bewiesen, Megan fragt nach Ducs Rolle")
    log = z["verhandlung"]["log"]
    pruefen(any(e["art"] == "kette" and e.get("zustand") == "zu" for e in log) and log[-2]["text"] == "The Verdict",
            "Kette schliesst sich, dann Titelkarte 'The Verdict'")
    arten = [e["art"] for e in log]
    pruefen("tratsch" in arten and "ruhe" in arten, "die Crew tratscht zwischen den Phasen, Megan sorgt fuer Ruhe")
    if A._aussagen_daten(z).get("gestaendnis") and z["verhandlung"]["angeklagt"] == v_ok:
        # >= : seit 28.10.2026 kann der Bot schon in der Woche gestehen lassen (Kernbeweise) - das ersetzt Punkt 2 mit
        # einem eigenen Gestaendnis-Eintrag
        pruefen(arten.count("gestaendnis") >= len(A._aussagen_daten(z)["gestaendnis"]) and "warum" in arten,
                "nach der Kette erklaert die Ueberfuehrte, warum")
    z = E.aktion("verhandlung", {"was": "rolle", "ehrlich": True})
    pruefen(z["verhandlung"]["schritt"] == "plaedoyer" and A.stand(z).get("rolle_ehrlich")
            and len(E.ansicht(z)["z"]["verhandlung"]["plaedoyer"]) == 3, "Rolle ehrlich, dann drei Plaedoyer-Karten")
    z = E.aktion("verhandlung", {"was": "plaedoyer", "art": "gnade"})
    pruefen(z["verhandlung"]["fertig"] and "verhandlung_urteil" in z["flags"] and A.stand(z).get("urteil")
            and z["verhandlung"]["log"][-1]["text"] == "The hearing is closed",
            "Urteil in der Anhoerung gesprochen (%s), Schluss-Titelkarte" % A.stand(z).get("urteil"))
    alle = {k for k, _, _ in A.alle_zeilen(E.modul_laden(), E.moddir())}
    fehlt = [e["key"] for e in log if e.get("key") and e["key"] not in alle]
    pruefen(not fehlt, "jede Stimme im Protokoll ist vertonbar %s" % fehlt[:3])
    z = E.aktion("verhandlung", {"was": "schliessen"})
    pruefen(z["status"] == "szene" and A.belegt(z), "zurück in die Szene, Kette gilt vor Megan als belegt")
    gespielt = []
    for _ in range(200):                               # bis zum Abend: Rollen-/Urteilsszene entfallen (26.10.2026)
        if z["status"] == "ende" or z["phase"] not in ("tag",) or z["tag"] > 7:
            break
        if z.get("szene"):
            gespielt.append(z["szene"]["def"]["id"])
        a = L.schritt(z, prot)
        if a is None:
            break
        if a[0] == "_tagesarbeit":
            L.tagesarbeit(z, prot)
        else:
            L.versuch(a, prot)
        z = E.aktiv()
    pruefen(not {"anhoerung_rolle", "anhoerung_urteil"} & set(gespielt),
            "keine Rollen-/Urteilsszene mehr nach der Anhoerung (%s)" % sorted(set(gespielt)))
    u = E.ermittlung.stand(z).get("urteil")
    pruefen(u in ("aufgeklaert", "erbarmen", "entlastet"), "Urteil nach bewiesener Verhandlung: %s" % u)
    print("OK")


if __name__ == "__main__":
    main()
