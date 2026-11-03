# -*- coding: utf-8 -*-
"""Maxwell-Tutorial (24.10.2026): Tag 2 nachmittags laedt Maxwell zum ersten Kampf ein, erklaert Schritt fuer Schritt,
danach gibt es das Training auf dem Sonnendeck fuer 1 Aktion; Zaehler fuer die Events Jana/Chiara.

  python tests\\test_tutorial.py
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


def kaempfen(z, parade="perfekt", befehl="angriff"):
    """Kampf bis zum Ende spielen; liefert die gesehenen Tutorial-Schritte."""
    gesehen = []
    for _ in range(80):
        k = z["kampf"]
        t = E.tutorial.ansicht(z)
        if t and t["id"] not in gesehen:
            gesehen.append(t["id"])
        if k["phase"] == "ende":
            break
        if k["phase"] == "parade":
            z = E.aktion("kampf_parade", {"ergebnis": parade, "revision": k["revision"]})
        else:
            z = E.aktion("kampf_zug", {"befehl": befehl, "ziel": None, "revision": k["revision"]})
    t = E.tutorial.ansicht(z)
    if t and t["id"] not in gesehen:
        gesehen.append(t["id"])
    return z, gesehen


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    L.vorbereiten("eden_rise", tempfile.mkdtemp(prefix="eden_tut_"))
    L.random.seed(3)
    prot = {"schritte": [], "erledigt": {}}
    z = E.aktion("neu", {"modus": "ironman"})
    for _ in range(3000):
        if z["status"] == "ereignis" and (z.get("event") or {}).get("id") == "mx_tutorial":
            break
        a = L.schritt(z, prot)
        if a[0] != "_tagesarbeit":
            L.versuch(a, prot)
        z = E.aktiv()
        if (z["tag"], z["phase"]) > (2, "zzz") and z["tag"] > 2:
            break
    pruefen(z["status"] == "ereignis" and z["event"]["id"] == "mx_tutorial" and (z["tag"], z["phase"]) == (2, "nachmittag"),
            "Tag 2 nachmittags lädt Maxwell zur ersten Lektion ein")
    z = E.aktion("event_wahl", {"index": 0})
    z = E.aktion("event_schliessen", {})
    pruefen(z["status"] == "kampf" and z["kampf"]["definition"] == "maxwell_tutorial", "erster Kampf startet")
    pruefen(E.tutorial.ansicht(z)["id"] == "l1_angriff", "Schritt 1: Angriff")
    z, gesehen = kaempfen(z)
    print("   gesehen:", ", ".join(gesehen))
    for sid in ("l1_angriff", "l1_absicht", "l1_parade", "l1_ausdauer", "l1_ende"):
        pruefen(sid in gesehen, "Lektion 1 zeigt %s" % sid)
    pruefen(gesehen.index("l1_absicht") < gesehen.index("l1_parade"), "Absicht vor Parade")
    phase = z["phase"]
    z = E.aktion("kampf_schliessen", {})
    pruefen(z["status"] == "ereignis" and z["event"]["id"] == "hk_hilfe",
            "nach der Lektion geht es direkt in den Hafen (Kette Hafenkampf, E-044)")
    for _ in range(200):                              # Hafen-Kette durchspielen: Events und drei Wellen
        if z["status"] not in ("ereignis", "kampf"):
            break
        L.versuch(L.schritt(z, prot), prot)
        z = E.aktiv()
    pruefen(z["status"] == "wahl" and (phase, z["phase"]) == ("nachmittag", "dinner") and E.plan.aktionen(z) == 0,
            "nach Lektion und Hafenkampf zurück zur Wahl: die Ortskette kostet den Nachmittag (E-078), sonst keine Aktion")
    pruefen("kloster_faden" in z["flags"], "Hafen-Kette bis zur Ziege gelaufen")
    pruefen("tutorial_maxwell" in z["flags"] and z["tutorial"]["lektion"] == 2, "Lektion 1 abgeschlossen")

    kraft = z["persona"]["attribute"].get("strength", 0)
    z = E.aktion("training_kampf", {})
    pruefen(z["status"] == "kampf" and z["kampf"]["definition"] == "maxwell_training", "Training startet")
    pruefen("mistral" in E.kampf.known(z), "Maxwell hat Mistral beigebracht (Lektion 1)")
    pruefen(E.tutorial.ansicht(z)["id"] == "l2_mistral", "Lektion 2 beginnt mit Mistral")
    pruefen((z["kampf"].get("aufgabe") or {}).get("id") in E.tutorial.AUFGABE
            and z["kampf"]["def"]["goal"].startswith("Maxwell's task"), "erstes Training des Tages stellt eine Aufgabe")
    z, _ = kaempfen(z)
    st = z["kampf"].get("stat") or {}
    pruefen(st.get("serie_max", 0) >= 1 and "erfuellt" in z["kampf"]["aufgabe"],
            "der Kampf zählt perfekte Paraden mit und wertet die Aufgabe (%s)" % st)
    sieg = (z["kampf"].get("ergebnis") or {}).get("art") in ("ko", "aufgabe")
    z = E.aktion("kampf_schliessen", {})
    z = E.aktiv()
    pruefen(E.plan.aktionen(z) == 1 or z["phase"] != phase, "Training kostet 1 Aktion")
    if sieg:
        pruefen(z["persona"]["attribute"].get("strength", 0) == min(5, kraft + 1), "erster Sieg im Akt: Kraft +1")
    tr = z.get("training_kampf") or {}
    pruefen(tr.get("siege", 0) + tr.get("niederlagen", 0) >= (1 if sieg else 0), "Trainingszähler läuft mit")
    pruefen(tr.get("aufgabe_tag") == z["tag"], "das erste Training am Tag hatte eine Aufgabe (Duc 02.11.2026)")

    # Aufgabe des Tages (Duc 02.11.2026): jedes weitere Training am selben Tag ist eine Extrarunde ohne Erfahrung
    if z["status"] == "wahl" and E.tutorial.training_verfuegbar(z):
        xp0 = (z["combat"]["level"], z["combat"]["xp"])
        z = E.aktion("training_kampf", {})
        k = z["kampf"]
        pruefen(k["aufgabe"] == {"id": None} and k["def"]["goal"] == E.tutorial.EXTRA_TEXT and k["def"]["xp_factor"] == 0,
                "zweites Training am selben Tag: Extrarunde, Ziel sagt es ehrlich")
        z, _ = kaempfen(z)
        pruefen(z["kampf"]["ergebnis"]["xp"] == 0, "Extrarunde bringt keine Erfahrung")
        z = E.aktion("kampf_schliessen", {})
        pruefen((z["combat"]["level"], z["combat"]["xp"]) == xp0, "Level und Erfahrung unverändert")

    # Prüfung der fünf Aufgaben ohne Kampf (feste Zähler)
    T = E.tutorial
    def k_mit(aid, **kw):
        k = {"aufgabe": {"id": aid}, "stat": {}, "spieler": {"lp": 50, "lp_max": 50}, "lp_start": 50, "runde": 6}
        for key, v in kw.items():
            k[key] = dict(k[key], **v) if isinstance(v, dict) and key in k else v
        return k
    faelle = [("serie", {"stat": {"serie_max": 3}}, {"stat": {"serie_max": 2}}),
              ("erschoepft", {"stat": {"spezial_erschoepft": True}}, {}),
              ("konter", {"stat": {"sieg_konter": True}}, {}),
              ("wenig", {"spieler": {"lp": 40}}, {"spieler": {"lp": 39}}),
              ("schnell", {"runde": 4}, {"runde": 5})]
    for aid, gut, schlecht in faelle:
        pruefen(T.aufgabe_werten(k_mit(aid, **gut), "aufgabe") == T.XP_AUFGABE, "Aufgabe %s geschafft: doppelte Erfahrung" % aid)
        pruefen(T.aufgabe_werten(k_mit(aid, **schlecht), "ko") == T.XP_OHNE, "Aufgabe %s verfehlt: alte Erfahrung" % aid)
        pruefen(T.aufgabe_werten(k_mit(aid, **gut), "niederlage") == T.XP_OHNE, "Aufgabe %s zählt nur mit Sieg" % aid)
    pruefen(set(T.AUFGABE) == {a for a, _, _ in faelle}, "alle fünf Aufgaben geprüft")
    print("OK")


if __name__ == "__main__":
    main()
