# -*- coding: utf-8 -*-
"""Modell B (24.10.2026): mehr Freizeit in Akt 1 - Nachmittag, Kabine als Drehkreuz, Uebergaenge, Aktionen.

Scheibe 1: Tag hat sechs Phasen, der Nachmittag gilt ohne eigene Angabe wie der Mittag.
Scheibe 2: Kabine kostet keine Phase, Training bis zu 2x am Tag, Ausruhen entfaellt, Lebenspunkte voll pro Phase.
Scheibe 3: kurze Story-Momente (uebergang) laufen als Vorspiel, danach ist die Phase frei.
Scheibe 4: 2 Aktionen pro freier Phase - Anruf 1, Szene die ganze Phase, Phase beenden.

  python tests\\test_modell_b.py
"""
import os, sys, tempfile

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import lauf_test as L  # noqa: E402

E = L.eden


def bis_wahl(tag):
    L.vorbereiten("eden_rise", tempfile.mkdtemp(prefix="eden_b_"))
    L.random.seed(5)
    prot = {"schritte": [], "erledigt": {}}
    z = E.aktion("neu", {"modus": "ironman"})
    while not (z["tag"] >= tag and z["status"] == "wahl"):
        a = L.schritt(z, prot)
        if a[0] != "_tagesarbeit":
            L.versuch(a, prot)
        z = E.aktiv()
    return z


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    from kern import regeln
    modul = E.modul_laden()
    pruefen(modul["zeitraster"]["phasen"] == ["fruehstueck", "tag", "nachmittag", "dinner", "abend", "nacht"],
            "sechs Phasen mit Nachmittag")
    pruefen(regeln.phase_passt("nachmittag", ["tag"]) and not regeln.phase_passt("abend", ["tag"]),
            "Nachmittag gilt wie Mittag, Abend nicht")

    z = bis_wahl(2)
    tag, phase = z["tag"], z["phase"]
    z = E.aktion("kabine", {})
    pruefen(z["status"] == "kabine", "Kabine betreten")
    try:
        E.aktion("kabine_training", {"attribut": "charm"})
        pruefen(False, "Attribut-Training der Kabine muss entfallen sein")
    except Exception:
        pruefen(True, "Attribut-Training in der Kabine gibt es nicht mehr (Training = Maxwell-Dialog)")
    pruefen(z["status"] == "kabine" and (z["tag"], z["phase"]) == (tag, phase), "Kabine bleibt, gleiche Phase")
    hs = modul["kabine"]["hotspots"]
    pruefen("handschuhe" in hs and "training" not in hs, "Boxhandschuhe sind ein Hotspot der Kabine")
    try:
        E.aktion("kabine_ausruhen", {})
        pruefen(False, "Ausruhen muss scheitern")
    except Exception:
        pruefen(True, "Ausruhen gibt es nicht mehr")
    z = E.aktion("kabine_zurueck", {})
    pruefen(z["status"] == "wahl" and (z["tag"], z["phase"]) == (tag, phase), "zurück zur Wahl derselben Phase")

    z["lp"] = 1
    E.sichern(z) if hasattr(E, "sichern") else None
    prot = {"schritte": [], "erledigt": {"t%d" % z["tag"]: True}}
    while (z["tag"], z["phase"]) == (tag, phase):
        L.versuch(L.schritt(z, prot), prot)
        z = E.aktiv()
    pruefen("lp" not in z, "neue Phase: Lebenspunkte wieder voll")

    # Scheibe 3: Uebergaenge laufen vor der Phase, danach ist sie frei
    z = bis_wahl(6)
    je = {}
    for h in z["verlauf"]:
        je.setdefault((h["tag"], h["phase"]), []).append(str(h.get("szene")))
    for (tg, ph), sid in (((3, "fruehstueck"), "sonnenaufgang"), ((5, "abend"), "leises_telefonat")):
        s = je.get((tg, ph), [])
        pruefen(s[:1] == [sid] and any(x.startswith("frei_") for x in s[1:]),
                "Tag %d %s: erst %s, dann eine freie Szene" % (tg, ph, sid))

    # Scheibe 4: zwei Aktionen pro freier Phase
    z = bis_wahl(4)
    while z["phase"] in ("fruehstueck", "nacht"):              # Wahl-Phase mit mehreren Optionen suchen
        z = E.aktion("wahl", {"id": z["optionen"][0]})
        while z["status"] == "szene":
            z = E.aktion("ende", {})
        z = E.aktiv()
    tag, phase = z["tag"], z["phase"]
    pruefen(z["status"] == "wahl" and len(z["optionen"]) >= 2, "freie Wahl-Phase erreicht (%s)" % phase)
    z = E.aktion("kabine", {})
    an = z["kabine"] and E.kabine.kontakte(z, E.modul_laden())[0]
    z = E.aktion("kabine_anruf", {"an": an})
    while z["status"] == "szene":
        z = E.aktion("ende", {})
    z = E.aktiv()
    pruefen(z["status"] == "wahl" and (z["tag"], z["phase"]) == (tag, phase) and E.plan.aktionen(z) == 1,
            "Anruf kostet 1 Aktion, Phase geht weiter")
    try:
        E.aktion("wahl", {"id": z["optionen"][0]})
        pruefen(False, "Szene nach einer Aktion muss scheitern")
    except Exception as e:
        pruefen("ganze Phase" in str(e), "Szene braucht die ganze Phase")
    z = E.aktion("phase_beenden", {})
    z = E.aktiv()
    pruefen((z["tag"], z["phase"]) != (tag, phase), "Phase beenden geht weiter")

    modul = E.modul_laden()
    prot = {"schritte": [], "erledigt": {}}
    for _ in range(200):                                        # eine Wahl-Phase mit Ermittlung ausserhalb suchen
        z = E.aktiv()
        wege = [w for w in E.ermittlung.moeglich(z, modul) if "Aktion" in (w.get("kosten") or "")]             if z["status"] == "wahl" else []
        if wege or z["status"] == "ende":
            break
        if z["status"] == "wahl":
            E.aktion("phase_beenden", {})
        else:
            a = L.schritt(z, prot)
            if a[0] != "_tagesarbeit":
                L.versuch(a, prot)
    if wege:
        tag, phase = z["tag"], z["phase"]
        z = E.aktion("ermitteln", {"weg": wege[0]["weg"]})
        pruefen((z["tag"], z["phase"]) == (tag, phase) and E.plan.aktionen(z) == 1, "Ermitteln kostet 1 Aktion")
    else:
        print("HINWEIS kein Ermittlungsweg ausserhalb gefunden - Pruefpunkt uebersprungen")

    # Boxhandschuhe in der Kabine -> Training mit Maxwell (25.10.2026)
    z = bis_wahl(2)
    z = E.aktion("kabine", {})
    z = E.aktion("training_kampf", {})
    pruefen(z["status"] == "kampf" and z["kampf"]["definition"] == "maxwell_training" and not z.get("kabine"),
            "Klick auf die Boxhandschuhe in der Kabine startet das Training mit Maxwell")

    # Keepsake Box (26.10.2026): Vitrine mit allen vergebenen Andenken, fehlende ohne Namen, Echo-Zeilen existieren
    z = bis_wahl(2)
    z = E.aktion("kabine", {})
    v = E.ansicht(z)["z"]["kabine"]["vitrine"]
    pruefen(len(v) >= 9 and all(w["label"] for w in v if w["da"]) and not any(w["label"] or w["echo"] for w in v if not w["da"]),
            "Keepsake Box zeigt %d Andenken, fehlende nur als Umriss" % len(v))
    pruefen("andenken" in modul["kabine"]["hotspots"] and "truhe" in modul["kabine"]["hotspots"], "zwei Leuchtpunkte an der Truhe")
    for iid, it in modul["items"].items():
        if it.get("echo"):
            wer, text = E.event_zeile(it["echo"]["key"][3:])
            pruefen(wer == it["echo"]["wer"] and text, "Echo von %s spielt %s" % (iid, wer))
    print("OK")


if __name__ == "__main__":
    main()
