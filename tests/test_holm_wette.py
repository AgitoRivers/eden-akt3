# -*- coding: utf-8 -*-
"""Holm kommt zurueck und die Wette um Gemelli (30.10.2026): Zeilen je Flag (eine je Gruppe), Pflicht-Reihenfolge,
drei Gegner, Sieg ueber Wolff gibt die Waffe, Niederlage kostet nichts, Deckel, Uebergabe, Holm-Challenge mit Geschenken.

  python tests\\test_holm_wette.py
"""
import json, os, sys, tempfile

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import lauf_test as L  # noqa: E402

E = L.eden
from kern import ereignisse, kampf, schiessen  # noqa: E402

EDEN = os.path.dirname(HIER)
EVENTS = {e["id"]: e for e in json.load(open(os.path.join(EDEN, "module", "eden_rise", "ereignisse.json"),
                                             encoding="utf-8"))["events"]}


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def saetze(flags):
    return [zl for _, zl in ereignisse.zeilen_aktiv(EVENTS["hb_megan"], {"flags": flags})]


def gruppe(flags, g):
    t = [zl["text"] for zl in saetze(flags) if zl.get("gruppe") == g]
    pruefen(len(t) == 1, "genau ein Satz in Gruppe %s bei %s" % (g, flags))
    return t[0]


def zeilen_test():
    ohne = {zl["text"] for e in EVENTS.values() if not e["id"].startswith("hb_") for zl in e["zeilen"]}
    # Gruppen sind seit 31.10. allgemein (nach_nacht, ruf, ...): geprueft wird nur, dass keine Zeile tot ist, also
    # keine Gruppen-Zeile hinter einer Zeile ohne "wenn" derselben Gruppe steht (die erste passende gewinnt)
    tot = []
    for e in EVENTS.values():
        frei = set()
        for zl in e["zeilen"]:
            g = zl.get("gruppe")
            if g and g in frei:
                tot.append((e["id"], g))
            if g and not zl.get("wenn"):
                frei.add(g)
    pruefen(not tot, "keine Gruppen-Zeile hinter dem Rueckfall ihrer Gruppe %s" % tot)
    pruefen(len(saetze([])) == 5, "Einleitung, 3 Saetze, Belagerung")
    pruefen("still waiting" in gruppe([], "macchia"), "Macchia offen")
    pruefen("did not come back" in gruppe(["kloster_frederico_tot"], "macchia"), "Frederico tot")
    pruefen("brought the boy Frederico" in gruppe(["kloster_frederico_lebt"], "macchia"), "Frederico lebt")
    pruefen("left alone" in gruppe([], "berge"), "Berge offen")
    pruefen("sergeant" in gruppe(["bg_adrien_bergerie"], "berge"), "Weg C")
    pruefen("for a while" in gruppe(["bg_weg_b", "petru_versoehnt"], "berge"), "Weg B versoehnt")
    pruefen("fix that" in gruppe(["bg_weg_b"], "berge"), "Weg B kalt")
    pruefen("legal thing" in gruppe(["bg_adrien_verhaftet"], "berge"), "Weg A")
    pruefen("still owe" in gruppe([], "grotte"), "Grotte offen")
    pruefen("cold water" in gruppe(["gr_bastien_tot", "grotte_fertig"], "grotte"), "Bastien tot geht vor")
    pruefen("fingers" in gruppe(["gr_gennaro_haende", "grotte_fertig"], "grotte"), "Gennaros Finger gehen vor")
    pruefen("came back with him" in gruppe(["grotte_fertig", "red_trio_fertig"], "grotte"), "Grotte fertig")
    pruefen("red suits" in gruppe(["red_trio_fertig"], "grotte"), "Red Trio als Ersatz")
    dank = lambda fl: [zl["text"] for _, zl in ereignisse.zeilen_aktiv(EVENTS["hb_zurueck"], {"flags": fl})]
    pruefen(len(dank([])) == 1 and "All here" in dank([])[0], "alle da")
    pruefen(len(dank(["gefeuert"])) == 1 and "One short" in dank(["gefeuert"])[0], "jemand gefeuert")
    ev = {"zeilen": [{"wer": "a", "text": "x"}, {"wer": "a", "text": "y"}]}
    pruefen([i for i, _ in ereignisse.zeilen_aktiv(ev, {"flags": []})] == [0, 1], "Zeilen ohne Gruppe bleiben alle, Index stabil")


def wann_test():
    pruefen(EVENTS["hb_zurueck"]["wann"]["pflicht"] and EVENTS["hb_megan"]["wann"]["bedingung"] == {"flag": "holm_zurueck"}
            and EVENTS["hb_koffer"]["wann"]["bedingung"] == {"flag": "holm_koffer"}, "drei Pflicht-Events in Folge")
    for eid, opts in (("hb_zurueck", "holm_zurueck"), ("hb_megan", "holm_koffer"), ("hb_koffer", "holm_wette_offen")):
        pruefen(all({"flag": opts} in o["folgen"] or opts in json.dumps(o["folgen"]) for o in EVENTS[eid]["optionen"]),
                "%s: jede Antwort setzt %s" % (eid, opts))
    pruefen(EVENTS["hb_sieg"]["wann"]["bedingung"] == {"flag": "hb_nie"} == EVENTS["hb_nochmal"]["wann"]["bedingung"],
            "Uebergabe und Nochmal-Zeile werden nie gezogen")


RUNDEN = lambda du, bot: [{"du": du, "bot": bot}] * 3


def intro_durch(z, eid):
    pruefen(z["status"] == "ereignis" and z["event"]["id"] == eid, "Szene " + eid)
    z = E.aktion("event_wahl", {"index": 0})
    z = E.aktion("event_schliessen", {})
    pruefen(z["status"] == "wahl" and z.get("schiessen_folgt"), "danach startet das Spiel")
    z = E.aktion("schiessen_start", {})
    pruefen(z["status"] == "schiessen" and "schiessen_folgt" not in z, "Spiel laeuft")
    return z


def wette_test():
    L.vorbereiten("eden_rise", tempfile.mkdtemp(prefix="eden_holm_"))
    L.random.seed(3)
    prot = {"schritte": [], "erledigt": {}}
    z = E.aktion("neu", {"modus": "ironman"})
    for _ in range(3000):
        if z["status"] == "wahl" and z.get("persona"):
            break
        a = L.schritt(z, prot)
        if a[0] != "_tagesarbeit":
            L.versuch(a, prot)
        z = E.aktiv()
    pruefen(z["status"] == "wahl", "freie Wahl erreicht")
    defs = kampf.daten(E.moddir("eden_rise"))
    pruefen("gun" not in kampf.besitz(z, defs)["weapons"], "Gemelli fehlt noch")
    pruefen("schiessen" not in z and "schiessen_verloren" not in z, "kein neuer Schluessel ohne Wette")
    try:
        E.aktion("schiessen_start", {})
        raise AssertionError("Start ohne Angebot")
    except ValueError:
        print("OK ohne Angebot kein Start")
    phase = z["phase"]
    z = E.aktiv()
    z["flags"].append("holm_wette_offen")
    E.sichern(z)
    pruefen(schiessen.gegner(z) == "rosi", "ohne Weg C zuerst Rosi")
    pruefen(schiessen.gegner({"flags": ["holm_wette_offen", "bg_adrien_bergerie"]}) == "adrien", "auf Weg C zuerst Adrien")
    z = intro_durch(E.aktion("schiessen_start", {}), "hb_g_rosi")
    pruefen(z["phase"] == phase, "Szene kostet keine Zeit")
    ans = E.ansicht(z)["z"]["schiessen"]
    pruefen(ans["bot"] == [5, 6, 7] and ans["gegner"]["name"] == "Rosi" and ans["gegner"]["avatare"]["vorn"] and len(ans["texte"]) == 2 and not ans["wind"] and not ans["granate"], "Ansicht fuer das Plugin: erster Gegner ohne Wind und Granate")
    z = E.aktion("schiessen_ergebnis", {"runden": [{"du": 5, "bot": 5}, {"du": 6, "bot": 6}, {"du": 7, "bot": 7}]})
    pruefen(not z["schiessen"]["letztes"]["sieg"], "Gleichstand ist kein Sieg")
    pruefen(z["schiessen_verloren"]["rosi"] == 1, "Niederlage gezaehlt")
    z = E.aktion("schiessen_ergebnis", {"runden": RUNDEN(0, 9)})
    z = E.aktion("schiessen_ergebnis", {"runden": RUNDEN(0, 9)})
    pruefen(schiessen.bot_plan(z, "rosi") == [4, 5, 6], "nach 3 Niederlagen trifft der Bot einen weniger")
    z = E.aktion("schiessen_ergebnis", {"runden": RUNDEN(999, 0)})
    letztes = z["schiessen"]["letztes"]
    pruefen(letztes["du"] == 3 * schiessen.TREFFER_MAX and letztes["sieg"], "Treffer sind gedeckelt, Blendung senkt den Bot")
    z = E.aktion("schiessen_ende", {})
    pruefen(z["status"] == "wahl" and z["phase"] == phase and "schiessen" not in z and schiessen.gegner(z) == "elsa", "weiter zu Elsa")
    z = intro_durch(E.aktion("schiessen_start", {}), "hb_g_elsa")
    z = E.aktion("schiessen_ergebnis", {"runden": RUNDEN(10, 5)})
    z = E.aktion("schiessen_ende", {})
    pruefen(schiessen.gegner(z) == "wolff" and "waffe_gun" not in z["flags"], "Elsa geschlagen, Waffe fehlt noch")
    z = intro_durch(E.aktion("schiessen_start", {}), "hb_g_wolff")
    z = E.aktion("schiessen_ergebnis", {"runden": RUNDEN(11, 9)})
    pruefen("waffe_gun" in z["flags"] and "holm_wette_gewonnen" in z["flags"], "Wolff geschlagen: Waffe")
    pruefen("gun" in kampf.besitz(z, defs)["weapons"], "Gemelli gehoert Duc")
    z = E.aktion("schiessen_ende", {})
    pruefen(z["status"] == "ereignis" and z["event"]["id"] == "hb_sieg", "Uebergabe-Szene")
    z = E.aktion("event_wahl", {"index": 0})
    z = E.aktion("event_schliessen", {})
    pruefen(z["phase"] == phase, "Uebergabe kostet keine Zeit")
    pruefen(not schiessen.offen(z), "vor Akt 3 ist die Wette zu")
    try:
        E.aktion("schiessen_start", {})
        raise AssertionError("Start nach Sieg")
    except ValueError:
        print("OK nach dem Sieg keine neue Wette")
    holm_test()


def holm_test():
    z = E.aktiv()
    # Tag 21-23 ist die Belagerung (E-114) mit Pflicht-Events in jeder Phase: die Szene erst am ersten freien Tag danach,
    # am Nachmittag (abends zieht der Sprung sonst Szenen der Fall-Kette nach)
    z["tag"], z["phase"] = 24, "nachmittag"
    E.sichern(z)
    pruefen(schiessen.gegner(dict(z, tag=schiessen.HOLM_TAG)) == "holm" and schiessen.gegner(z) == "holm", "ab Tag 22 Holm")
    z = intro_durch(E.aktion("schiessen_start", {}), "hb_g_holm")
    ans = E.ansicht(z)["z"]["schiessen"]
    pruefen(not ans["relaxed_erlaubt"] and ans["dauer"] == 9.5, "gegen Holm kein Relaxed")
    vorher = list(z["inventar"])
    z = E.aktion("schiessen_ergebnis", {"runden": [{"du": 9, "bot": 8}, {"du": 0, "bot": 9}, {"du": 0, "bot": 10}]})
    l = z["schiessen"]["letztes"]
    pruefen(not l["sieg"] and [g["runde"] for g in l["geschenke"]] == [1], "Runde 1 gewonnen, Spiel verloren: Geschenk 1")
    pruefen(z["inventar"].count("steel_plate") == vorher.count("steel_plate") + 1, "Stahlplatte im Inventar")
    z = E.aktion("schiessen_ergebnis", {"runden": [{"du": 9, "bot": 8}, {"du": 10, "bot": 9}, {"du": 0, "bot": 10}]})
    l = z["schiessen"]["letztes"]
    pruefen([g["runde"] for g in l["geschenke"]] == [2] and "aquamarin" in z["inventar"], "jedes Geschenk nur einmal")
    z = E.aktion("schiessen_ergebnis", {"runden": [{"du": 0, "bot": 8}, {"du": 0, "bot": 9}, {"du": 11, "bot": 10}]})
    pruefen("kupfer" in z["inventar"], "Kupfer")
    z = E.aktion("schiessen_ende", {})
    pruefen(z["status"] == "wahl" and not schiessen.offen(z), "alle Geschenke vergeben: Challenge zu")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    zeilen_test()
    wann_test()
    wette_test()


if __name__ == "__main__":
    main()
