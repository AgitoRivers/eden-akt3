# -*- coding: utf-8 -*-
"""Schnelljobs abgeschaltet (Duc 29.10.2026, die Favours ersetzen sie): modul["schnelljobs"] = False. Der Job-Code und
missionen.json bleiben (test_missionen.py prueft die Mechanik mit eingeschaltetem Schalter). Hier: nichts davon ist mehr
zu sehen, und was an den Jobs hing, ist umgehaengt - die zwoelf einzigartigen Geschenke liegen fest bei Totò (ab Vertrauen 3),
die Crew-Karte kommt als Dank von Lolas Favour-Kette.

  python tests\\test_schnelljobs_aus.py
"""
import json, os, sys, tempfile

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import lauf_test as L  # noqa: E402

E = L.eden
H = E.handel

FEST = ["chiara_tasse", "rosi_schild", "sophia_fueller", "lea_tauchcomputer", "siri_ratgeber", "lola_vegemite",
        "alva_kastagnetten", "toto_gennaro", "yasin_goldbrille", "elsa_strafzettelblock", "petru_tabak", "casanova_kanone"]


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def basis():
    L.vorbereiten("eden_rise", tempfile.mkdtemp(prefix="eden_jobsaus_"))
    L.random.seed(11)
    protokoll = {"schritte": [], "erledigt": {}}
    z = E.aktion("neu", {"modus": "ironman"})
    while not (z["tag"] >= 3 and z["status"] == "wahl"):
        a = L.schritt(z, protokoll)
        if a[0] != "_tagesarbeit":
            L.versuch(a, protokoll)
        z = E.aktiv()
    return z


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    z = basis()
    modul, V = E.modul_laden(), E.showrunner.vorrat(E.moddir())
    pruefen(modul.get("schnelljobs") is False, "Modul eden_rise: schnelljobs = False")
    pruefen(len(V["jobs"]) == 68, "missionen.json bleibt vollstaendig (68 Missionen) - umkehrbar")

    # Nichts davon ist zu sehen
    pruefen(H.jobs_heute(z, modul, V) == [], "Handy: kein Job im Angebot")
    pruefen(H.jobs_angebot(z, modul, V) == [], "kein Tagesangebot, nichts wird festgeschrieben")
    pruefen(not z.get("jobs_tag"), "Spielstand: kein jobs_tag")
    h = H.ansicht(z, modul, V, [])
    pruefen(h["jobs"] == [] and h["jobs_aktiv"] is False and h["tasche"] == [], "Ansicht: jobs_aktiv False, Jobs und Besorgungstasche leer")
    z["auftraege"] = ["petru_schild_1"]                  # selbst ein offener Auftrag aus einem alten Stand zeigt nichts mehr
    pruefen(H.offene_auftraege(z, modul, V) == [] and H.teile_gebraucht(z, modul, V) == {}, "alte offene Besorgungen: keine Teile gebraucht")
    z["auftraege"] = []
    teile = [i for i, it in modul["items"].items() if it.get("art") == "teil"]
    gesehen = [w["id"] for k in modul["laeden"] for w in (H.sortiment(z, modul, k) or []) if w["id"] in teile]
    pruefen(not gesehen, "kein Laden bietet Besorgungs-Teile an (%d Teile im Modul)" % len(teile))
    try:
        H.job_machen(z, modul, V, "alva_kassenbuch")
        pruefen(False, "job_machen muss ablehnen")
    except ValueError:
        pruefen(True, "job_machen lehnt ab (nicht im Angebot)")

    # Totòs feste Ware: die zwoelf einzigartigen Geschenke, ab Vertrauen 3, ausserhalb der Rotation
    z["werte"]["draht"] = z["werte"]["vertrauen.toto"] = 2   # Totòs Laden prueft Vertrauen und Draht (kern/handel.sortiment)
    ware2 = H.sortiment(z, modul, "toto") or []
    pruefen(not [w for w in ware2 if w["id"] in FEST], "Totò Vertrauen 2: keine einzigartigen Geschenke")
    z["werte"]["draht"] = z["werte"]["vertrauen.toto"] = 3
    for tag in (3, 4, 5, 6):                            # jeden Tag da, egal wie die Rotation fallt
        z["tag"] = tag
        ware = H.sortiment(z, modul, "toto") or []
        ids = [w["id"] for w in ware]
        pruefen(all(i in ids for i in FEST), "Totò Vertrauen 3, Tag %d: alle zwoelf einzigartigen Geschenke im Angebot" % tag)
        rest = [w for w in ware if w["id"] not in FEST]
        pruefen(len(rest) <= modul["laeden"]["toto"]["sortiment"] and "espresso" in ids,
                "  Rotation bleibt (%d weitere Waren, Espresso immer)" % len(rest))
    preise = {w["id"]: w["preis"] for w in ware if w["id"] in FEST}
    pruefen(all(50 <= p <= 190 for p in preise.values()), "Preise 50-190 € (Totòs Draht-Faktor eingerechnet: %s)" % sorted(preise.values()))
    for iid in FEST:
        it = modul["items"][iid]
        pruefen(it["art"] == "geschenk" and it.get("nur_fuer") and it["geschenk"][it["nur_fuer"]] == 2, "  %s: Geschenk nur fuer %s" % (iid, it.get("nur_fuer")))
        break
    z["konto"] = 500
    inv = len(z["inventar"])
    H.kaufen(z, modul, "toto", "lola_vegemite")
    pruefen("lola_vegemite" in z["inventar"] and z["konto"] < 500, "Kauf: Vegemite im Inventar, Geld abgebucht")

    # Crew-Karte: Dank von Lolas Favour-Kette, nicht kaeuflich
    pruefen(modul["items"]["megan_crewkarte"].get("wo") is None, "megan_crewkarte ist nicht kaeuflich")
    d = E.ereignisse.daten(E.moddir())
    dank = d["_index"]["fv_lola_dank"]
    pruefen(all({"item": "megan_crewkarte"} in o["folgen"] for o in dank["optionen"]), "Lolas Dank gibt die Crew-Karte (beide Antworten)")

    # Was frueher an den Jobs hing, ist anderswo abgedeckt
    ev = json.load(open(os.path.join(E.moddir(), "ereignisse.json"), encoding="utf-8"))["events"]
    gegeben = {f["item"] for e in ev for o in e["optionen"] for f in o["folgen"] + o.get("bei_erfolg", []) + o.get("bei_fehlschlag", []) if "item" in f}
    pruefen({"festa_invite", "petrus_hammer"} <= gegeben, "festa_invite und petrus_hammer vergeben auch Events (nicht nur Jobs)")
    j_items = {f["item"] for j in V["jobs"] for f in j.get("folgen", []) if "item" in f}
    ohne = sorted(i for i in j_items if i not in gegeben and i not in FEST and i != "megan_crewkarte")
    pruefen(not ohne, "jedes Item der alten Jobs ist erreichbar %s" % (ohne or ""))
    print("\nalle Schnelljob-aus-Tests bestanden")


if __name__ == "__main__":
    main()
