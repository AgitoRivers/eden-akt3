# -*- coding: utf-8 -*-
r"""Taktik-Karte (Duc 31.10.2026): Raster, Regeln und ein Bot, der alle sechs Wellen spielt. Ohne Sprachmodell, ohne Client.

  python tests\test_taktik.py
"""
import os, sys
from collections import deque

EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, EDEN)
from kern import belagerung, kampf, kuechen, taktik  # noqa: E402

M = os.path.join(EDEN, "module", "eden_rise")
MODUL = __import__("json").load(open(os.path.join(M, "modul.json"), encoding="utf-8"))


def als_crew(f):
    """Regeln des Schnellkampfs: Maxwell steht hier fuer einen beliebigen Crew-Trupp, seit 01.11.2026 kaempft er selbst echt."""
    def lauf():
        alt = taktik.SPIELER
        taktik.SPIELER = ("duc",)
        try:
            f()
        finally:
            taktik.SPIELER = alt
    lauf.__name__ = f.__name__
    return lauf


def echt_fertig(z, ergebnis):
    """Kampf einer Spielfigur abschliessen, wie eden.py es tut."""
    z["status"] = "kampf"
    taktik.kampf_ende(z, M, ergebnis)


def neu(flags=()):
    z = {"flags": list(flags), "status": "wahl"}
    taktik.beginnen(z, M)
    return z


def erreicht(D, t, start, ziel):
    q, seen = deque([tuple(start)]), {tuple(start)}
    while q:
        x, y = q.popleft()
        if (x, y) == tuple(ziel):
            return True
        for f in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if f not in seen and taktik._frei(D, t, f[0], f[1]):
                seen.add(f)
                q.append(f)
    return False


def test_raster():
    D = taktik.daten(M)
    z = neu()
    t = z["taktik"]
    for w in D["wellen"]:
        for typ, pos in w["feinde"]:
            if not D["feinde"][typ].get("fliegt"):
                t["barrikade"] = w["id"] != 3
                assert taktik._frei(D, t, *pos), ("Spawn gesperrt", typ, pos)
                assert erreicht(D, t, pos, D["kirche"]["tueren"][0]), ("Kein Weg zur Kirche", typ, pos)
    t["barrikade"] = True
    for e in t["einheiten"]:
        assert taktik._frei(D, t, e["x"], e["y"]), ("Start gesperrt", e["id"], e["x"], e["y"])
        assert erreicht(D, t, (e["x"], e["y"]), D["kirche"]["tueren"][0]), ("Trupp abgeschnitten", e["id"])


def test_plaetze():
    """Eckige Plaetze: nur dorthin, besetzt heisst tauschen, Holms Vorschlag steht schon darauf."""
    D = taktik.daten(M)
    z = neu()
    t = z["taktik"]
    plaetze = [(p["x"], p["y"]) for p in D["plaetze"]]
    assert len(set(plaetze)) == len(plaetze)
    for f in plaetze:
        assert taktik._frei(D, t, *f) and erreicht(D, t, f, D["kirche"]["tueren"][0]), ("Platz gesperrt", f)
    for tid in D["trupps"]:
        assert tuple(D["trupps"][tid]["start"]) in plaetze, ("Start nicht auf einem Platz", tid)
    for w in D["wehr"]:
        assert tuple(D["wehr"][w]["start"]) not in plaetze, ("Buergerwehr steht auf einem Platz", w)
    mx, wo = taktik._e(t, "maxwell"), taktik._e(t, "wolff")
    a, b = (mx["x"], mx["y"]), (wo["x"], wo["y"])
    taktik.aufstellen(z, M, "maxwell", *b)
    assert (mx["x"], mx["y"]) == b and (wo["x"], wo["y"]) == a, "Besetzter Platz: tauschen"
    frei = next(f for f in plaetze if not any((e["x"], e["y"]) == f for e in t["einheiten"]))
    taktik.aufstellen(z, M, "chiara", *frei)
    for args in (("maxwell", 30, 18), ("pascal", *frei)):
        try:
            taktik.aufstellen(z, M, *args)
        except ValueError:
            continue
        raise AssertionError("haette abgelehnt werden muessen")


def test_hilfe_wahl():
    """Holm fest, zwei Plaetze frei, verdient ueber Vertrauen."""
    z = neu()
    t = z["taktik"]
    assert t["hilfe"] == ["holm"]
    for hid in ("lola", "holm"):
        try:
            taktik.hilfe_waehlen(z, M, hid)
        except ValueError:
            continue
        raise AssertionError("haette abgelehnt werden muessen: " + hid)
    z["werte"] = {"vertrauen." + p: 5 for p in ("sophia", "lola", "lea", "siri", "sirene")}
    taktik.hilfe_waehlen(z, M, "lola")
    taktik.hilfe_waehlen(z, M, "lea")
    assert t["hilfe"] == ["holm", "lola", "lea"]
    try:
        taktik.hilfe_waehlen(z, M, "siri")
    except ValueError:
        pass
    else:
        raise AssertionError("Nur drei Plaetze")
    taktik.hilfe_waehlen(z, M, "lea")
    assert t["hilfe"] == ["holm", "lola"]
    assert len(taktik.ansicht(z, M)["hilfe"]) == 6


def schlacht_mit(hilfe):
    z = neu()
    z["werte"] = {"vertrauen." + p: 5 for p in ("sophia", "lola", "lea", "siri", "sirene")}
    for h in hilfe:
        taktik.hilfe_waehlen(z, M, h)
    taktik.start_schlacht(z, M)
    while z["taktik"]["phase"] == "szene":
        taktik.szene_weiter(z, M)
    return z, z["taktik"]


def nie(fn, *args):
    try:
        fn(*args)
    except ValueError:
        return
    raise AssertionError("haette abgelehnt werden muessen")


def test_hilfe_wirkung():
    # Holm: einmal je Runde zieht ein Trupp nochmal
    z, t = schlacht_mit([])
    mx = taktik._e(t, "maxwell")
    nie(taktik.hilfe_einsetzen, z, M, "holm", "maxwell")
    taktik.warten(z, "maxwell")
    taktik.hilfe_einsetzen(z, M, "holm", "maxwell")
    assert not mx["fertig"] and t["meldung"]
    taktik.warten(z, "maxwell")
    nie(taktik.hilfe_einsetzen, z, M, "holm", "maxwell")
    taktik.runde_beenden(z, M)
    assert "Holm" not in (z["taktik"]["meldung"] or ""), "Die Meldung gilt nur fuer eine Runde"
    # Lola: nur am Kai, nur Verwundete, einmal je Welle
    z, t = schlacht_mit(["lola"])
    mx = taktik._e(t, "maxwell")
    nie(taktik.hilfe_einsetzen, z, M, "lola", "maxwell")
    mx["lp"] = 10
    taktik.hilfe_einsetzen(z, M, "lola", "maxwell")
    assert mx["lp"] > 10
    mx["lp"] = 10
    nie(taktik.hilfe_einsetzen, z, M, "lola", "maxwell")
    # Lea: Feinde von See setzen die erste Runde aus, wandern danach los
    z, t = schlacht_mit(["lea"])
    taktik._welle_start(z, taktik.daten(M), t, 2)
    see = [e for e in taktik.lebend(t, "schwarz") if e["front"] == "Yacht"]
    assert see
    vorher = [(e["x"], e["y"]) for e in see]
    assert not any(a["von"] == see[0]["id"] for a in taktik.ansicht(z, M)["absichten"]), "Wer aussetzt, hat keine Absicht"
    taktik.runde_beenden(z, M)
    assert [(e["x"], e["y"]) for e in see] == vorher
    # Siri: eine Front haelt eine Runde, einmal je Welle, Mr. White nie
    z, t = schlacht_mit(["siri"])
    west = [e for e in taktik.lebend(t, "schwarz") if e["front"] == "West"]
    vorher = [(e["x"], e["y"]) for e in west]
    taktik.hilfe_einsetzen(z, M, "siri", "West")
    nie(taktik.hilfe_einsetzen, z, M, "siri", "South")
    taktik.runde_beenden(z, M)
    assert [(e["x"], e["y"]) for e in west] == vorher
    # Ligeia: einmal in der ganzen Schlacht, auch nach einem Neustart der Welle bleibt der Gesang verbraucht
    z, t = schlacht_mit(["ligeia"])
    t["welle"] = 2
    t["hilfe_genutzt"]["ligeia"] = "ganz"
    nie(taktik.hilfe_einsetzen, z, M, "ligeia")
    # Ligeias Lied: Piraten am Wasser schlafen zwei Runden, Roboter nicht
    z, t = schlacht_mit(["ligeia"])
    D = taktik.daten(M)
    nie(taktik.hilfe_einsetzen, z, M, "ligeia")
    pirat, robo = feind(D, t, "brand", 12, 22, "p"), feind(D, t, "roboter", 43, 15, "r")
    taktik.hilfe_einsetzen(z, M, "ligeia")
    assert taktik._haelt(t, pirat) and not taktik._haelt(t, robo)
    t["runde"] += 1
    assert taktik._haelt(t, pirat), "Zwei Runden"
    t["runde"] += 1
    assert not taktik._haelt(t, pirat)
    # Danzel naeht eine Platte ein: halber Schaden bis zur naechsten Runde, nur mit versoehntem Trio
    z = neu(["rt_ausgang_alle"])
    t = z["taktik"]
    taktik.hilfe_waehlen(z, M, "danzel")
    t["phase"], t["welle"], t["runde"] = "spieler", 1, 1
    wo = taktik._e(t, "wolff")
    taktik.hilfe_einsetzen(z, M, "danzel", "wolff")
    vorher, log = wo["lp"], []
    taktik._treffer(t, feind(D, t, "agent", 1, 1, "x"), wo, 10, log)
    assert wo["lp"] == vorher - 5, "Halber Schaden"
    nie(taktik.hilfe_einsetzen, z, M, "danzel", "chiara")
    z = neu()
    nie(taktik.hilfe_waehlen, z, M, "danzel")
    # Sophia zeigt Felder in zwei Runden
    z, t = schlacht_mit(["sophia"])
    assert taktik.ansicht(z, M)["spaeter"]
    z, t = schlacht_mit([])
    assert not taktik.ansicht(z, M)["spaeter"]


def test_gelaende():
    """Gangarten, Schutz und Tarnung (Duc 31.10.2026)."""
    D = taktik.daten(M)
    z = neu()
    t = z["taktik"]
    raster = D["raster"]
    wald = next((x, y) for y, r in enumerate(raster) for x, c in enumerate(r) if c == "W" and taktik._im_bild(D, t, x, y))
    fels = next((x, y) for y, r in enumerate(raster) for x, c in enumerate(r) if c == "B" and taktik._im_bild(D, t, x, y))
    agent = taktik._einheit("a", "agent", "schwarz", D["feinde"]["agent"], 0, 0)
    rob = taktik._einheit("r", "roboter", "schwarz", D["feinde"]["roboter"], 0, 0)
    drohne = taktik._einheit("d", "drohne", "schwarz", D["feinde"]["drohne"], 0, 0)
    assert taktik._kosten(D, t, agent, *wald) == 2 and taktik._kosten(D, t, rob, *wald) == 3 and taktik._kosten(D, t, drohne, *wald) == 1
    assert taktik._kosten(D, t, rob, *fels) is None and taktik._kosten(D, t, agent, *fels) == 3 and taktik._kosten(D, t, drohne, *fels) == 1
    assert drohne["bewegung"] > agent["bewegung"] > rob["bewegung"], "Flieger am weitesten, Roboter am langsamsten"
    assert rob["abwehr"] > agent["abwehr"] > drohne["abwehr"], "Roboter ist der Tank, Flieger halten nichts aus"
    # Roboter kommen von ihrem Start auf eigenen Wegen bis zur Kirche
    for w in D["wellen"]:
        for typ, pos in w["feinde"]:
            e = taktik._einheit("x", typ, "schwarz", D["feinde"][typ], pos[0], pos[1])
            t["barrikade"] = w["id"] != 3
            assert any(tuple(p) in taktik._wege(D, t, e) for p in D["kirche"]["tueren"]), ("Kein Weg zur Kirche", typ, pos)
    t["barrikade"] = True
    # Der Wald schuetzt und versteckt, die Drohne sieht alles
    wo = taktik._e(t, "wolff")
    frei = taktik.schaden(agent, wo, D) if D["raster"][wo["y"]][wo["x"]] == "." else None
    wo["x"], wo["y"] = wald
    assert frei is None or taktik.schaden(agent, wo, D) == max(1, frei - 1)
    agent["x"], agent["y"] = wald[0] + 6, wald[1]
    drohne["x"], drohne["y"] = wald[0] + 6, wald[1]
    assert taktik._getarnt(D, wo) and not taktik._sichtbar(D, agent, wo) and taktik._sichtbar(D, drohne, wo)
    agent["x"] = wald[0] + 2
    assert taktik._sichtbar(D, agent, wo)


@als_crew
def test_break_und_doppel():
    D = taktik.daten(M)
    z = neu()
    t = z["taktik"]
    mx, wo = taktik._e(t, "maxwell"), taktik._e(t, "wolff")
    rob = taktik._einheit("r", "roboter", "schwarz", D["feinde"]["roboter"], mx["x"] + 1, mx["y"])
    t["einheiten"].append(rob)
    t["phase"] = "spieler"
    v = taktik.vorschau(mx, rob, D)
    assert v["break"] and v["zurueck"] == 0, "Stark heisst kein Gegenschlag"
    assert taktik.vorschau(wo, rob, D)["zurueck"] == 0 or not taktik.vorschau(wo, rob, D)["break"]
    assert taktik._doppel(z, D, t, mx, rob) == (None, 0), "Wolff steht zu weit weg"
    wo["x"], wo["y"] = rob["x"] + 1, rob["y"]
    h, mit = taktik._doppel(z, D, t, mx, rob)
    assert h is wo and mit >= 1
    z["werte"] = {"vertrauen.wolff": 3}
    ag = taktik._einheit("a", "agent", "schwarz", D["feinde"]["agent"], rob["x"], rob["y"] + 1)
    wo["x"], wo["y"] = ag["x"], ag["y"] + 1
    mx["x"], mx["y"] = ag["x"] - 1, ag["y"]
    t["einheiten"].append(ag)
    _, viel = taktik._doppel(z, D, t, mx, ag)
    z["werte"] = {}
    _, wenig = taktik._doppel(z, D, t, mx, ag)
    assert viel > wenig, "Vertrauen macht den Doppelangriff staerker"
    lp = rob["lp"]
    mx["gezogen"] = mx["fertig"] = False
    mx["x"], mx["y"] = rob["x"] - 1, rob["y"]
    wo["x"], wo["y"] = rob["x"] + 1, rob["y"]
    taktik.angreifen(z, M, "maxwell", rob["id"])
    assert rob["lp"] < lp - taktik.schaden(mx, rob, D) + 1 and not wo["fertig"], "Der Mitschlag kostet Wolff nichts"


def test_maxwell_echter_kampf():
    """Duc steuert Maxwell wie sich selbst (01.11.2026): echter Kampf, eigene Werte, eigene Tasche, Ducs Stand bleibt unberuehrt."""
    D = taktik.daten(M)
    z = neu()
    z["inventar"] = ["bandage"]
    t = z["taktik"]
    mx = taktik._e(t, "maxwell")
    rob = taktik._einheit("r", "roboter", "schwarz", D["feinde"]["roboter"], mx["x"] + 1, mx["y"])
    t["einheiten"].append(rob)
    t["phase"] = "spieler"
    duc_lp = kampf.lp(z)
    assert taktik.ansicht(z, M)["einheiten"] and taktik.angreifen(z, M, "maxwell", rob["id"])["kampf"] == rob["kampf"]
    mx["lp"] = mx["lp_max"] // 2
    defs = taktik.kampf_defs(z, M)
    h = taktik.held_start(z, M)
    assert h["id"] == "maxwell" and h["lp_anteil"] == mx["lp"] / mx["lp_max"]
    kampf.starten(z, defs, rob["kampf"], rueckkehr={"status": "taktik"}, held=h)
    k = z["kampf"]
    sp = k["spieler"]
    assert k["held"]["sprite"] == "MaxwellSteelMop" and set(k["specials"]) == {"parry_the_dirt", "maximum", "approves"}
    assert sp["lp_max"] > kampf.max_lp(kampf.progress(z)["level"]), "Mehr LP als Duc"
    assert sp["lp"] == round(sp["lp_max"] * h["lp_anteil"]), "Sein Stand von der Karte"
    assert z["inventar"].count("verbandskasten") == 3 and z["inventar"].count("espresso_single") == 3
    assert sum(1 for i in z["inventar"] if i.startswith("grenade_")) == 2 and "bandage" not in z["inventar"]
    z["kampf"]["ergebnis"] = {"art": "ko"}
    z["inventar"].remove("verbandskasten")
    z["lp"] = 3
    kampf._finish(z, MODUL, k, "ko")
    assert "bandage" in z["inventar"], "Beute und Ducs Sachen wieder in Ducs Tasche"
    assert kampf.schliessen(z)["status"] == "taktik" and z["lp"] == duc_lp, "Ducs LP unberuehrt"
    taktik.kampf_ende(z, M, "ko")
    assert rob["ko"] and not mx.get("ko") and z["status"] == "taktik"
    assert t["tasche_maxwell"].count("verbandskasten") == 2, "Verbrauchtes bleibt weg bis zur naechsten Welle"
    # Faellt er, ist er bis zur naechsten Welle weg, und die Welle laeuft weiter
    rob2 = taktik._einheit("r2", "roboter", "schwarz", D["feinde"]["roboter"], mx["x"] + 1, mx["y"])
    t["einheiten"].append(rob2)
    t["phase"], mx["fertig"] = "spieler", False
    taktik.angreifen(z, M, "maxwell", rob2["id"])
    z["held_zurueck"] = {"id": "maxwell", "lp_anteil": 0, "tasche": []}
    taktik.kampf_ende(z, M, "niederlage")
    assert mx["ko"] and not rob2.get("ko") and t["phase"] == "spieler", "Nur Ducs Fall startet die Welle neu"
    t["phase"] = "spieler"
    taktik._welle_start(z, D, t, 2)
    assert not mx["ko"] and "tasche_maxwell" not in t, "Naechste Welle: wieder da, Tasche voll"
    white = taktik._einheit("w", "white", "weiss", D["feinde"]["white"], mx["x"] + 1, mx["y"])
    white["boss"] = True
    t["einheiten"].append(white)
    assert white["id"] not in [q["id"] for q in taktik.ziele(t, mx, D) if not q["boss"]]


def test_plan_stimmt():
    """Die angezeigte Bedrohung ist genau das, was im Gegnerzug passiert."""
    z = neu()
    taktik.start_schlacht(z, M)
    while z["taktik"]["phase"] == "szene":
        taktik.szene_weiter(z, M)
    for _ in range(6):
        t = z["taktik"]
        if t["phase"] != "spieler":
            return
        D = taktik.daten(M)
        vorher = {e["id"]: (e["x"], e["y"]) for e in taktik.lebend(t)}
        plan = taktik._plan(z, D, t)
        assert vorher == {e["id"]: (e["x"], e["y"]) for e in taktik.lebend(t)}, "Die Vorschau darf nichts bewegen"
        kirche = t["kirche"]
        taktik.runde_beenden(z, M)
        t = z["taktik"]
        if t["phase"] == "spieler":
            assert kirche - t["kirche"] == sum(1 for p in plan if p["an"] == "kirche"), ("Kirche", plan)
            for l in t["letzter_zug"]:
                if l["an"] not in ("kirche", "duc", "yacht") and taktik._e(t, l["an"])["seite"] == "blau":
                    assert any(p["von"] == l["von"] and p["an"] == l["an"] and p["schaden"] == l["schaden"] for p in plan), ("Schlag ohne Vorhersage", l)


def test_white_gesperrt():
    """Mr. White bleibt unbesiegbar, bis Petrus Trupp gefallen ist."""
    z = neu()
    D = taktik.daten(M)
    t = z["taktik"]
    t["welle"], t["runde"], t["phase"] = 5, 99, "spieler"
    taktik._pruefen(z, D, t)
    while z["taktik"]["phase"] == "szene":
        taktik.szene_weiter(z, M)
    t = z["taktik"]
    w = next(e for e in taktik.lebend(t, "weiss"))
    d = taktik._e(t, "duc")
    d["x"], d["y"] = w["x"], w["y"] + 1
    assert w not in taktik.ziele(t, d)
    taktik._casanova_pruefen(z, D, t)
    assert "casanova" not in t["gesehen"], "Casanova erst nach Petru"
    t["gesehen"].append("minicu_faellt")
    assert w in taktik.ziele(t, d)


def test_nachschub_und_haeuser():
    z = neu()
    D = taktik.daten(M)
    taktik.start_schlacht(z, M)
    while z["taktik"]["phase"] == "szene":
        taktik.szene_weiter(z, M)
    t = z["taktik"]
    zahl = len(t["einheiten"])
    assert taktik.ansicht(z, M)["ankunft"][0]["in"] == 2
    taktik.runde_beenden(z, M)
    taktik.runde_beenden(z, M)
    t = z["taktik"]
    assert len(t["einheiten"]) > zahl, "Runde 3: Nachschub"
    # Eine leere Karte ist erst geschafft, wenn kein Boot mehr aussteht
    z = neu()
    t = z["taktik"]
    t["welle"], t["runde"], t["phase"] = 3, 1, "spieler"
    taktik._pruefen(z, D, t)
    assert t["phase"] == "spieler", "Boote stehen noch aus"
    t["runde"] = 5
    taktik._pruefen(z, D, t)
    assert t["phase"] == "szene"
    # Welle 4: Haeuser brennen herunter, Trupp daneben rettet
    while z["taktik"]["phase"] == "szene":
        taktik.szene_weiter(z, M)
    t = z["taktik"]
    assert t["welle"] == 4 and all(s["status"] == "brennt" for s in t["haeuser"].values())
    w = taktik._e(t, "wolff")
    h = D["haeuser"][0]
    w["x"], w["y"] = h["x"] + 1, h["y"]
    taktik.retten(z, M, "wolff", h["id"])
    assert t["haeuser"][h["id"]]["status"] == "gerettet" and w["fertig"]
    nie(taktik.retten, z, M, "chiara", D["haeuser"][1]["id"])
    for _ in range(9):
        taktik.runde_beenden(z, M)
        if z["taktik"]["phase"] != "spieler":
            break
    t = z["taktik"]
    assert t["haeuser"][D["haeuser"][1]["id"]]["status"] == "verloren", "Ohne Hilfe brennt es ab"


def test_reserve():
    D = taktik.daten(M)
    z = neu()
    t = z["taktik"]
    frei = [(p["x"], p["y"]) for p in D["plaetze"] if not any((e["x"], e["y"]) == (p["x"], p["y"]) for e in t["einheiten"])]
    nie(taktik.aufstellen, z, M, "elsa", *frei[0])
    z["werte"] = {"vertrauen.elsa": 2, "vertrauen.rosi": 2, "vertrauen.yamamoto": 2}
    z["flags"] = ["rt_ausgang_alle"]
    for rid, f in zip(("elsa", "rosi"), frei):
        taktik.aufstellen(z, M, rid, *f)
    assert len(taktik._im_einsatz(t)) == 6
    nie(taktik.aufstellen, z, M, "yamamoto", *frei[2])
    taktik.aufstellen(z, M, "yamamoto", *frei[0])
    assert not any(e["id"] == "elsa" for e in t["einheiten"]), "Tausch mit Reserve"
    nie(taktik.aufstellen, z, M, "bibi", taktik._e(t, "maxwell")["x"], taktik._e(t, "maxwell")["y"])
    taktik.auf_bank(z, M, "rosi")
    assert len(taktik._im_einsatz(t)) == 5
    nie(taktik.auf_bank, z, M, "wolff")
    assert {k["id"] for k in taktik.ansicht(z, M)["karten"] if k["reserve"]} == {"elsa", "rosi", "yamamoto", "bibi"}


@als_crew
def test_macht():
    z = neu()
    D = taktik.daten(M)
    taktik.start_schlacht(z, M)
    while z["taktik"]["phase"] == "szene":
        taktik.szene_weiter(z, M)
    t = z["taktik"]
    taktik._welle_start(z, taktik.daten(M), t, 2)
    mx = taktik._e(t, "maxwell")
    nie(taktik.macht_einsetzen, z, M, "maxwell")
    rob = next(e for e in taktik.lebend(t, "schwarz") if e["typ"] == "roboter")
    mx["x"], mx["y"] = rob["x"] - 1, rob["y"]
    v = rob["lp"]
    taktik.angreifen(z, M, "maxwell", rob["id"])
    assert 0 < mx["macht"] < 100 and rob["lp"] < v, "Treffer laden die Leiste"
    mx["macht"], mx["fertig"] = 100, False
    v = rob["lp"]
    taktik.macht_einsetzen(z, M, "maxwell")
    t = z["taktik"]
    assert rob["lp"] < v and mx["macht"] == 0 and mx["fertig"] and t["cutin"]["titel"] == "Maximum Force"
    wo = taktik._e(t, "wolff")
    wo["macht"], wo["fertig"], wo["gezogen"] = 100, True, True
    taktik.macht_einsetzen(z, M, "wolff")
    assert not wo["fertig"] and not wo["gezogen"], "Legion Drill: nochmal"
    du = taktik._e(t, "duc")
    du["macht"] = 100
    wo["lp"], z["lp"] = 1, 1
    taktik.macht_einsetzen(z, M, "duc")
    assert wo["lp"] > 1 and z["lp"] > 1, "Rally heilt alle"
    sicht = taktik.ansicht(z, M)["cutin"]
    assert sicht["n"] == 3


@als_crew
def test_rueckspringen():
    z = neu()
    taktik.start_schlacht(z, M)
    while z["taktik"]["phase"] == "szene":
        taktik.szene_weiter(z, M)
    t = z["taktik"]
    taktik._welle_start(z, taktik.daten(M), t, 2)
    feind = next(e for e in taktik.lebend(t, "schwarz"))
    x, y = feind["x"], feind["y"]
    mx = taktik._e(t, "maxwell")
    mx0 = mx["x"], mx["y"]
    taktik.bewegen(z, M, "maxwell", *next(f for f in taktik.erreichbar(taktik.daten(M), t, mx) if f != mx0))
    assert taktik.ansicht(z, M)["rethink_frei"]
    taktik.rueckspringen(z)
    t = z["taktik"]
    assert (taktik._e(t, "maxwell")["x"], taktik._e(t, "maxwell")["y"]) == mx0 and t["rueckspruenge"] == 2 and t["runde"] == 1, "Bis zum ersten Angriff ist Rethink gratis"
    assert not taktik.ansicht(z, M)["rethink_frei"], "Ohne Zug gibt es nichts gratis zurueckzusetzen"
    # Nach einem Angriff kostet es einen Ruecksprung
    rob = next(e for e in taktik.lebend(t, "schwarz") if e["typ"] == "roboter")
    mx = taktik._e(t, "maxwell")
    mx["x"], mx["y"] = rob["x"] - 1, rob["y"]
    lp = rob["lp"]
    taktik.angreifen(z, M, "maxwell", rob["id"])
    assert rob["lp"] < lp and not taktik.ansicht(z, M)["rethink_frei"]
    taktik.rueckspringen(z)
    t = z["taktik"]
    assert t["rueckspruenge"] == 1 and next(e for e in t["einheiten"] if e["id"] == rob["id"])["lp"] == lp, "Der Angriff ist zurueckgenommen"
    taktik.runde_beenden(z, M)
    t = z["taktik"]
    assert t["runde"] == 2
    taktik.rueckspringen(z)                          # in Runde 2 ist noch nichts passiert: eine weiter zurueck
    t = z["taktik"]
    assert t["rueckspruenge"] == 0 and (t["runde"], next(e for e in t["einheiten"] if e["id"] == feind["id"])["x"]) == (1, x), "Alle Feinde wieder am Start"
    nie(taktik.rueckspringen, z)                     # weiter zurueck gibt es nichts
    assert z["taktik"]["rueckspruenge"] == 0, "Das kostet keinen Ruecksprung"


def test_schusslinie():
    """Haeuser halten Schuesse auf, Drohnen nicht. Feinde gehen dann naeher ran."""
    D = taktik.daten(M)
    z = neu()
    t = z["taktik"]
    t["phase"] = "spieler"
    # Eine Hauswand finden, vor der zwei freie Felder liegen
    r = D["raster"]
    x, y = next((x, y) for y in range(1, 30) for x in range(1, 46) if r[y][x] == "#" and r[y][x - 1] in "." and r[y][x + 1] in ".")
    ch = taktik._e(t, "chiara")
    ch["x"], ch["y"] = x - 1, y
    ag = taktik._einheit("a", "agent", "schwarz", D["feinde"]["agent"], x + 1, y)
    t["einheiten"].append(ag)
    assert not taktik._schussfrei(D, ch, ag) and ag not in taktik.ziele(t, ch, D), "Das Haus steht im Weg"
    nie(taktik.angreifen, z, M, "chiara", "a")
    assert [x + 1, y] not in taktik.reichweite_felder(D, ch), "Die Reichweite zeigt das Feld hinter dem Haus nicht"
    assert ag in taktik.ziele(t, ch), "Ohne Karte zaehlt nur der Abstand"
    dr = taktik._einheit("d", "drohne", "schwarz", D["feinde"]["drohne"], x + 1, y)
    t["einheiten"].append(dr)
    assert taktik._schussfrei(D, ch, dr), "Auf Drohnen geht es darueber hinweg"


def test_fernkampf():
    """Schuetze und Chiaras Taser: Direkt daneben kommt kein Gegenschlag, Roboter sind immun."""
    z = neu()
    D = taktik.daten(M)
    t = z["taktik"]
    t["phase"] = "spieler"
    wo, ch = taktik._e(t, "wolff"), taktik._e(t, "chiara")
    sch = taktik._einheit("s", "schuetze", "schwarz", D["feinde"]["schuetze"], wo["x"] + 1, wo["y"])
    t["einheiten"].append(sch)
    assert sch["reichweite"] == 3 and sch["abwehr"] < D["feinde"]["agent"]["abwehr"]
    assert not taktik._kontert(sch, wo), "Direkt daneben wehrt er sich nicht"
    sch["x"] = wo["x"] + 3
    assert taktik._kontert(sch, wo), "Aus der Ferne schiesst er zurueck"
    ch["x"], ch["y"] = 37, 15                        # freie Linie auf der Mole
    sch["x"], sch["y"] = 39, 15
    sch["lp"] = 99
    assert taktik.vorschau(ch, sch, D)["betaeubt"]
    taktik.angreifen(z, M, "chiara", sch["id"])
    t = z["taktik"]
    assert taktik._haelt(t, sch), "Der Taser haelt ihn eine Runde auf"
    assert not any(p["von"] == sch["id"] for p in taktik._plan(z, D, t)), "Wer aussetzt, plant nichts"
    x = sch["x"], sch["y"]
    taktik.runde_beenden(z, M)
    assert (sch["x"], sch["y"]) == x
    rob = taktik._einheit("r", "roboter", "schwarz", D["feinde"]["roboter"], 0, 0)
    assert not taktik._betaeubt(ch, rob), "Roboter sind immun"


def test_yacht():
    """Roboter an Bord zerlegen die Yacht, ein Trupp in der Naehe bindet sie, verloren ist nur die Yacht."""
    z = neu(["waffe_bat"])
    D = taktik.daten(M)
    t = z["taktik"]
    z["werte"] = {"vertrauen.lola": 2}
    taktik.hilfe_waehlen(z, M, "lola")
    taktik.start_schlacht(z, M)
    while z["taktik"]["phase"] == "szene":
        taktik.szene_weiter(z, M)
    t = z["taktik"]
    taktik._welle_start(z, D, t, 2)
    assert t["yacht"] == 3
    robo = [e for e in taktik.lebend(t, "schwarz") if e["typ"] == "roboter"]
    assert robo
    mx, ch = taktik._e(t, "maxwell"), taktik._e(t, "chiara")
    mx["x"], mx["y"], ch["x"], ch["y"] = 26, 16, 24, 16     # weg von der Yacht
    pos = [(e["x"], e["y"]) for e in robo]
    assert any(p["an"] == "yacht" for p in taktik._plan(z, D, t)), "Die Vorschau zeigt den Schaden"
    taktik.runde_beenden(z, M)
    t = z["taktik"]
    assert t["yacht"] == 2, "Ein Schaden je Runde, egal wie viele Roboter"
    assert [(e["x"], e["y"]) for e in robo] == pos, "Sie bleiben an Bord"
    # Ein Trupp in der Naehe bindet sie
    mx["x"], mx["y"] = 40, 16
    taktik.runde_beenden(z, M)
    t = z["taktik"]
    assert t["yacht"] == 2, "Mr. Maximum haelt sie auf"
    # Ohne Yacht gehen sie zur Kirche, Lola faellt aus, die Schlacht laeuft weiter
    mx["x"], mx["y"] = 26, 16
    for e in robo:
        e["x"], e["y"] = 41, 15 + robo.index(e)
    t["yacht"] = 1
    taktik.runde_beenden(z, M)
    t = z["taktik"]
    assert t["yacht"] == 0 and t["phase"] == "spieler" and not taktik._hilfe_bereit(D, t, "lola")
    alt = [(e["x"], e["y"]) for e in robo if not e.get("ko")]
    taktik.runde_beenden(z, M)
    assert [(e["x"], e["y"]) for e in robo if not e.get("ko")] != alt, "Sie ziehen weiter"


def test_echte_kaempfe():
    """Jeder Feind fuehrt zu einem echten Kampf, den es auch gibt. Der Brandtrupp sind Fackelpiraten."""
    D = taktik.daten(M)
    z = neu()
    defs = taktik.kampf_defs(z, M)
    for typ, q in D["feinde"].items():
        b = defs["encounters"][q["kampf"]]
        for gegner in b["enemies"]:
            assert gegner in defs["enemies"], (typ, gegner)
    assert defs["encounters"][D["feinde"]["brand"]["kampf"]]["enemies"] == ["fackelpirat", "pirat"]
    assert D["feinde"]["roboter_schwer"]["lp"] > D["feinde"]["roboter"]["lp"] and D["feinde"]["roboter_schwer"]["bewegung"] < D["feinde"]["roboter"]["bewegung"], "Zwei Roboter, verschieden stark"
    assert defs["enemies"]["tk_robot_schwer"]["name"] == "Heavy Boarding Robot"
    for typ in ("gunner", "brawler", "bonaventure"):
        assert defs["encounters"][D["feinde"][typ]["kampf"]]["enemies"][1] == "pirat", "Der einfache Pirat kommt immer dazu"


def test_figuren():
    """Jede Pixel-Figur in den Daten hat ihr Bild, Breite und Hoehe passen zur Angabe."""
    from PIL import Image
    D = taktik.daten(M)
    z = neu()
    alle = list(D["trupps"].values()) + list(D["reserve"].values()) + list(D["wehr"].values()) + list(D["feinde"].values())
    assert all(q.get("figur") for q in alle), [q["name"] for q in alle if not q.get("figur")]
    figuren = [q["figur"] for q in alle] + list(D["trupps"]["duc"]["figur_jacke"].values()) + [D["hilfe"]["danzel"]["einheit"]["figur"], D["trupps"]["chiara"]["figur_flag"]["figur"]]
    figuren += [f["stand"] for f in figuren]
    for f in figuren:
        b = Image.open(os.path.join(M, "taktik", f["bild"]))
        assert b.mode == "RGBA" and b.width % f["bilder"] == 0, f
        assert abs(b.width / f["bilder"] / b.height - f["seite"]) < 0.01, f
    assert taktik.ansicht(z, M)["einheiten"][1]["figur"]["bilder"] == 6
    # Duc nach seiner Jacke, Chiara nur mit den Dress Whites in Weiss
    z = {"flags": ["sn_dress_whites_fertig"], "status": "wahl", "equipment": {"armor": "jacket_fire"}}
    taktik.beginnen(z, M)
    t = z["taktik"]
    assert taktik._e(t, "duc")["figur"]["bild"] == "fig_duc_feuer.webp"
    assert taktik._e(t, "chiara")["figur"]["bild"] == "fig_chiara_whites.webp"


@als_crew
def test_anim():
    """Jeder Angriff und jeder Gegnerzug meldet dem Bildschirm, was er zeigen soll."""
    z = neu()
    taktik.start_schlacht(z, M)
    while z["taktik"]["phase"] == "szene":
        taktik.szene_weiter(z, M)
    t = z["taktik"]
    taktik._welle_start(z, taktik.daten(M), t, 2)
    assert taktik.ansicht(z, M)["anim"] is None
    mx = taktik._e(t, "maxwell")
    rob = next(e for e in taktik.lebend(t, "schwarz") if e["typ"] == "roboter")
    mx["x"], mx["y"] = rob["x"] - 1, rob["y"]
    taktik.angreifen(z, M, "maxwell", rob["id"])
    a = taktik.ansicht(z, M)["anim"]
    assert a["n"] == 1 and a["log"][0]["von"] == "maxwell" and a["log"][0]["an"] == rob["id"]
    taktik.runde_beenden(z, M)
    assert z["taktik"]["anim"]["n"] == 2
    taktik.rueckspringen(z)
    t = z["taktik"]
    assert t["anim"] is None and t["anim_n"] == 2, "Nach dem Zuruecknehmen wird nichts wiederholt"


def feind(D, t, typ, x, y, eid=None):
    e = taktik._einheit(eid or typ, typ, "schwarz", D["feinde"][typ], x, y, seit=t["runde"])
    t["einheiten"].append(e)
    return e


def alle_weg(t, *lassen):
    """Nur die genannten Einheiten bleiben auf dem Feld, damit ein Verhalten allein pruefbar ist."""
    for e in t["einheiten"]:
        if e["id"] not in lassen:
            e["ko"] = True


def test_dreieck():
    """Schnell schlaegt Fernkampf, Fernkampf schlaegt Schwer, Schwer schlaegt Schnell, in beide Richtungen."""
    D = taktik.daten(M)
    z = neu()
    t = z["taktik"]
    mx, wo, ch = taktik._e(t, "maxwell"), taktik._e(t, "wolff"), taktik._e(t, "chiara")
    ag, sch, rob = (feind(D, t, n, 0, 0) for n in ("agent", "schuetze", "roboter"))
    assert taktik.staerke(ag, ch) == 1.25 and taktik.staerke(ch, rob) == 1.25 and taktik.staerke(sch, mx) == 1.25 and taktik.staerke(rob, wo) == 1.25, "Feinde haben jetzt auch Vorteile"
    assert taktik.staerke(ag, mx) == 0.8, "Und Nachteile"
    assert taktik.staerke(mx, wo) == 1.25 and taktik.staerke(ch, ch) == 1.0
    # Ein Feind im Vorteil verhindert den Gegenschlag
    rob["x"], rob["y"], wo["x"], wo["y"] = 30, 15, 31, 15
    assert taktik.schaden(rob, wo, D) > max(1, rob["angriff"] - wo["abwehr"]), "Der Roboter trifft Wolff haerter"
    log = []
    taktik._zurueck_schlagen(t, rob, wo, log, D)
    assert not log, "Kein Gegenschlag gegen den Vorteil"


def test_verhalten():
    D = taktik.daten(M)
    z = neu()
    t = z["taktik"]
    t["phase"], t["welle"], t["runde"] = "spieler", 1, 1
    wo, mx, ch = taktik._e(t, "wolff"), taktik._e(t, "maxwell"), taktik._e(t, "chiara")
    # Der Schuetze haelt die Stellung, bis jemand kommt oder drei Runden um sind
    sch = feind(D, t, "schuetze", 33, 15)
    alle_weg(t, "wolff", "schuetze")
    wo["x"], wo["y"] = 14, 15
    assert taktik._absicht(D, t, sch)["art"] == "halten"
    wo["x"] = 31
    assert taktik._absicht(D, t, sch)["art"] == "trupp", "Kommt jemand nah, wehrt er sich"
    wo["x"] = 14
    t["runde"] = 4
    assert taktik._absicht(D, t, sch)["art"] != "halten", "Nach drei Runden kommt er"
    # Der Hund jagt den Verwundeten, nicht den Naechsten
    z = neu()
    t = z["taktik"]
    t["phase"], t["runde"] = "spieler", 1
    h = feind(D, t, "hund", 30, 15)
    wo, mx = taktik._e(t, "wolff"), taktik._e(t, "maxwell")
    alle_weg(t, "wolff", "maxwell", "hund")
    wo["x"], wo["y"], mx["x"], mx["y"] = 33, 15, 28, 15
    mx["lp"], wo["lp"] = 5, 30
    assert taktik._absicht(D, t, h)["ziel"] == "maxwell"
    # Der Brute geht zur Kirche, auch wenn ein Trupp naeher steht
    b = feind(D, t, "brute", 30, 15)
    assert taktik._absicht(D, t, b)["art"] == "kirche"
    # Die Drohne sucht die duennste Ruestung
    d = feind(D, t, "drohne", 30, 15)
    ch = taktik._e(t, "chiara")
    ch.update(ko=False, x=40, y=16)
    assert taktik._absicht(D, t, d)["ziel"] == "chiara"
    # Der Brandtrupp laeuft zum brennenden Haus
    t["haeuser"] = {x["id"]: {"lunte": 5, "status": "brennt"} for x in D["haeuser"]}
    f = feind(D, t, "brand", 16, 18)
    ab = taktik._absicht(D, t, f)
    assert ab["art"] == "haus" and any((x["x"], x["y"]) == ab["feld"] for x in D["haeuser"])
    alt = (f["x"], f["y"])
    alle_weg(t, "maxwell", "brand")
    taktik.runde_beenden(z, M)
    assert (f["x"], f["y"]) != alt, "Er laeuft wirklich los"


def test_eigenschaften():
    D = taktik.daten(M)
    # Elsa: schiesst einmal je Runde zuerst
    z = neu()
    z["werte"] = {"vertrauen.elsa": 2, "vertrauen.rosi": 2, "vertrauen.yamamoto": 2}
    z["flags"] = ["rt_ausgang_alle"]
    t = z["taktik"]
    frei = [(p["x"], p["y"]) for p in D["plaetze"] if not any((e["x"], e["y"]) == (p["x"], p["y"]) for e in t["einheiten"])]
    taktik.aufstellen(z, M, "elsa", *frei[0])
    t["phase"], t["welle"], t["runde"] = "spieler", 1, 1
    el = taktik._e(t, "elsa")
    alle_weg(t, "elsa")
    el["x"], el["y"] = 30, 15
    ag = feind(D, t, "agent", 34, 15)
    ag2 = feind(D, t, "agent", 34, 15, "a2")
    ag2["x"], ag2["y"] = 35, 15
    ag["lp"] = ag2["lp"] = 40
    taktik.runde_beenden(z, M)
    assert [ag["lp"] < 40, ag2["lp"] < 40].count(True) >= 1 and el.get("wache") == 1, "Overwatch"
    getroffen = [l for l in z["taktik"]["letzter_zug"] if l["von"] == "elsa"]
    assert len([l for l in getroffen]) <= 3
    # Rosi: Ruestung der Roboter zaehlt nicht
    z = neu()
    z["werte"] = {"vertrauen.rosi": 2, "vertrauen.yamamoto": 2}
    z["flags"] = ["rt_ausgang_alle"]
    t = z["taktik"]
    frei = [(p["x"], p["y"]) for p in D["plaetze"] if not any((e["x"], e["y"]) == (p["x"], p["y"]) for e in t["einheiten"])]
    for rid, f in zip(("rosi", "yamamoto"), frei):
        taktik.aufstellen(z, M, rid, *f)
    t["phase"], t["welle"], t["runde"] = "spieler", 1, 1
    ro, ya, mx = taktik._e(t, "rosi"), taktik._e(t, "yamamoto"), taktik._e(t, "maxwell")
    rob = feind(D, t, "roboter", 40, 15)
    assert taktik.schaden(ro, rob, D) > ro["angriff"] - rob["abwehr"] + 6, "Ruestung zaehlt nicht"
    # Yamamoto: Sieg heisst nochmal, einmal je Runde
    ya["x"], ya["y"] = 30, 15
    op = feind(D, t, "agent", 31, 15, "op")
    op["lp"] = 1
    taktik.angreifen(z, M, "yamamoto", "op")
    assert not ya["fertig"] and not ya["gezogen"], "Clean Cut"
    op2 = feind(D, t, "agent", 29, 15, "op2")
    op2["lp"] = 1
    taktik.angreifen(z, M, "yamamoto", "op2")
    assert ya["fertig"], "Nur einmal je Runde"
    # Bibi: Trifft sie einen Hund, setzt er aus. Ihr Lachen zieht die Feinde auf sie, ihre Wassergranate bremst ein Haus
    z = neu()
    z["flags"] = ["rt_ausgang_alle"]
    t = z["taktik"]
    frei = [(p["x"], p["y"]) for p in D["plaetze"] if not any((e["x"], e["y"]) == (p["x"], p["y"]) for e in t["einheiten"])]
    taktik.aufstellen(z, M, "bibi", *frei[0])
    t["phase"], t["welle"], t["runde"] = "spieler", 4, 1
    bi = taktik._e(t, "bibi")
    bi["x"], bi["y"] = 30, 15
    g = feind(D, t, "hund", 31, 15, "g")
    g["lp"] = 99
    taktik.angreifen(z, M, "bibi", "g")
    assert taktik._haelt(t, g), "Licht und Wasser"
    assert not taktik._betaeubt(bi, feind(D, t, "agent", 32, 15, "a"))
    bi["fertig"] = False
    bi["macht"] = 100
    taktik.macht_einsetzen(z, M, "bibi")
    a = feind(D, t, "agent", 33, 15, "a2")
    assert taktik._absicht(D, t, a).get("ziel") == "bibi", "Das Lachen zieht ihn an"
    h = D["haeuser"][0]
    t["haeuser"] = {h["id"]: {"lunte": 5, "status": "brennt"}}
    bi.update(x=h["x"] + 2, y=h["y"], fertig=False)
    assert h["id"] in taktik._sicht(z, D, t, bi, True)["loeschen"]
    taktik.loeschen(z, M, "bibi", h["id"])
    assert t["haeuser"][h["id"]]["lunte"] == 8 and bi["fertig"]
    nie(taktik.loeschen, z, M, "bibi", h["id"])


def test_staerke():
    D = taktik.daten(M)
    z = neu()
    t = z["taktik"]
    mx, wo = taktik._e(t, "maxwell"), taktik._e(t, "wolff")
    rob = taktik._einheit("r", "roboter", "schwarz", D["feinde"]["roboter"], 0, 0)
    ag = taktik._einheit("a", "agent", "schwarz", D["feinde"]["agent"], 0, 0)
    assert taktik.schaden(mx, rob) > taktik.schaden(wo, rob), "Maxwell soll gegen Roboter glaenzen"
    assert taktik.schaden(wo, ag) > taktik.schaden(mx, ag)
    w = taktik._einheit("w", "white", "weiss", D["feinde"]["white"], 0, 0)
    assert taktik.schaden(mx, w) == 0, "Nur Duc stoppt Mr. White"


def test_fehler_und_zurueck():
    z = neu()
    taktik.start_schlacht(z, M)
    while z["taktik"]["phase"] == "szene":
        taktik.szene_weiter(z, M)
    t = z["taktik"]
    assert t["phase"] == "spieler" and t["welle"] == 1
    mx = taktik._e(t, "maxwell")
    x, y = mx["x"], mx["y"]
    D = taktik.daten(M)
    f = next(f for f in taktik.erreichbar(D, t, mx) if f != (x, y))
    taktik.bewegen(z, M, "maxwell", *f)
    taktik.zuruecknehmen(z, "maxwell")
    assert (mx["x"], mx["y"]) == (x, y) and not mx["gezogen"]
    for fn, args in ((taktik.bewegen, (z, M, "pascal", 28, 10)), (taktik.bewegen, (z, M, "maxwell", 0, 0))):
        try:
            fn(*args)
        except ValueError:
            continue
        raise AssertionError("haette abgelehnt werden muessen")


def bot(z, duc_gewinnt=True, tun=True, max_runden=80, duc_wartet=False):
    """Spielt schlicht: jeder Trupp greift an, was erreichbar ist. Duc gewinnt oder verliert seine echten Kaempfe nach Vorgabe."""
    D = taktik.daten(M)
    runden = 0
    while runden < max_runden:
        t = z["taktik"]
        if t["phase"] == "szene":
            taktik.szene_weiter(z, M)
            continue
        if t["phase"] == "white_neu":
            taktik.white_neu(z)
            taktik.kampf_ende(z, M, "ko")
            continue
        if t["phase"] in ("gewonnen", "verloren"):
            return t["phase"], runden
        if not tun:
            taktik.runde_beenden(z, M)
            runden += 1
            continue
        for e in list(taktik.lebend(t, "blau")):
            if z["taktik"]["phase"] != "spieler":
                break
            if e["fest"] or e["fertig"]:
                continue
            feinde = taktik.lebend(t, "schwarz") + taktik.lebend(t, "weiss")
            if duc_wartet:                                        # alle halten den Platz und kaempfen nur, was nah kommt
                tuer = D["kirche"]["tueren"][0]
                feinde = [g for g in feinde if abs(g["x"] - tuer[0]) + abs(g["y"] - tuer[1]) <= 13]
            if e["id"] != "duc":
                feinde = [g for g in feinde if not g["boss"]]
            if not feinde:
                if duc_wartet and abs(e["x"] - tuer[0]) + abs(e["y"] - tuer[1]) > 5:
                    fs = taktik.erreichbar(D, t, e)
                    taktik.bewegen(z, M, e["id"], *min(fs, key=lambda f: (abs(f[0] - tuer[0]) + abs(f[1] - tuer[1]), f)))
                continue
            felder = taktik.erreichbar(D, t, e)
            if duc_wartet and e["id"] != "duc":                         # kluger Spieler: nur Gegner, gegen die der Trupp nicht schwach ist, sonst die Kirchentuer sperren
                # zuerst Leute aus dem Haus holen, wenn der Trupp schon daneben steht oder hinkommt
                hs = [h for h in D["haeuser"] if t.get("haeuser", {}).get(h["id"], {}).get("status") == "brennt"]
                if hs:
                    h = min(hs, key=lambda h: t["haeuser"][h["id"]]["lunte"])
                    naechst = [f for f in felder if abs(f[0] - h["x"]) + abs(f[1] - h["y"]) <= 1]
                    if naechst:
                        taktik.bewegen(z, M, e["id"], *naechst[0])
                        taktik.retten(z, M, e["id"], h["id"])
                        continue
                # kluger Spieler: Wer im Vorteil ist, sucht sich dieses Ziel, auch weit weg. Mr. Maximum nimmt also die Roboter.
                stark = [g for g in taktik.lebend(t, "schwarz") if not g["boss"] and taktik.staerke(e, g) >= 1.25]
                gut = stark or [g for g in feinde if not g["boss"] and taktik.staerke(e, g) >= 1]
                if not gut:
                    tuer = D["kirche"]["tueren"][0 if e["id"] == "wolff" else 1]
                    f = min(felder, key=lambda f: (abs(f[0] - tuer[0]) + abs(f[1] - tuer[1]), f))
                    taktik.bewegen(z, M, e["id"], *f)
                    while z["taktik"]["phase"] == "szene":
                        taktik.szene_weiter(z, M)
                    ziele = [g for g in taktik.ziele(t, e, D) if not g["boss"]]
                    if ziele and z["taktik"]["phase"] == "spieler":
                        if taktik.angreifen(z, M, e["id"], max(ziele, key=lambda g: taktik.schaden(e, g, D))["id"]).get("kampf"):
                            echt_fertig(z, "ko" if duc_gewinnt else "niederlage")
                    elif not e["fertig"]:
                        taktik.warten(z, e["id"])
                    continue
                feinde = gut
            an_tuer = [g for g in taktik.lebend(t, "schwarz") if duc_wartet and [g["x"], g["y"]] in D["kirche"]["tueren"]]   # nach Mr. White zuerst, wer die Kirche trifft
            g = next((g for g in feinde if g["boss"] and taktik.white_frei(t)), None) or (an_tuer[0] if an_tuer else None) or min(feinde, key=lambda g: min(abs(g["x"] - f[0]) + abs(g["y"] - f[1]) for f in felder))
            wege = taktik._dijkstra(D, t, e, (g["x"], g["y"]))           # echter Weg, nicht Luftlinie: Mauern und Wald zaehlen
            f = min(felder, key=lambda f: (abs(wege.get(f, 999) - e["reichweite"]), f))
            taktik.bewegen(z, M, e["id"], *f)
            if z["taktik"]["phase"] != "spieler":
                while z["taktik"]["phase"] == "szene":
                    taktik.szene_weiter(z, M)
            erreichbare = [x for x in taktik.ziele(t, e, D) if e["id"] == "duc" or not x["boss"]]
            if g not in erreichbare and erreichbare and z["taktik"]["phase"] == "spieler":   # versperrt jemand den Weg, ist er das Ziel
                g = erreichbare[0]
            if g in erreichbare and z["taktik"]["phase"] == "spieler":
                r = taktik.angreifen(z, M, e["id"], g["id"])
                if r.get("kampf"):
                    z["status"] = "kampf"
                    taktik.kampf_ende(z, M, "ko" if duc_gewinnt else "niederlage")
            elif not e["fertig"]:
                taktik.warten(z, e["id"])
        if z["taktik"]["phase"] == "spieler":
            taktik.runde_beenden(z, M)
            runden += 1
    return "abbruch", runden


def test_nichts_tun_verliert():
    z = neu()
    taktik.start_schlacht(z, M)
    erg, runden = bot(z, tun=False)
    assert erg == "verloren", erg


def test_durchspielen():
    z = neu()
    taktik.start_schlacht(z, M)
    erg, runden = bot(z)
    t = z["taktik"]
    print("  Bot:", erg, "Runden", runden, "Welle", t["welle"], "Kirche", t["kirche"], "gesehen", t["gesehen"])
    assert t["welle"] >= 2, "Mindestens die zweite Welle muss erreichbar sein"
    if erg == "verloren":
        taktik.neustart_welle(z, M)
        t = z["taktik"]
        assert t["phase"] == "spieler" and t["runde"] == 1, "Neustart ab Beginn der Welle"
    taktik.ansicht(z, M)


def test_gewinnbar():
    """Wer Duc klug an der Kirche haelt, kann die Belagerung gewinnen."""
    z = neu()
    taktik.start_schlacht(z, M)
    erg, runden = bot(z, duc_wartet=True)
    t = z["taktik"]
    print("  Kluger Bot:", erg, "Runden", runden, "Welle", t["welle"], "Kirche", t["kirche"], "Duc", kampf.lp(z), "gesehen", t["gesehen"])
    assert erg == "gewonnen", erg


def test_vorbereitung_zahlt():
    """Mit sechs Trupps steht die Kirche besser als mit den vier von Anfang."""
    ohne = neu()
    taktik.start_schlacht(ohne, M)
    bot(ohne, duc_wartet=True)
    mit = neu()
    mit["werte"] = {"vertrauen.elsa": 2, "vertrauen.rosi": 2, "vertrauen.lea": 2, "vertrauen.sophia": 2}
    D = taktik.daten(M)
    t = mit["taktik"]
    frei = [(p["x"], p["y"]) for p in D["plaetze"] if not any((e["x"], e["y"]) == (p["x"], p["y"]) for e in t["einheiten"])]
    taktik.aufstellen(mit, M, "elsa", *frei[-1])
    taktik.aufstellen(mit, M, "rosi", *frei[-2])
    taktik.hilfe_waehlen(mit, M, "lea")
    taktik.start_schlacht(mit, M)
    erg, runden = bot(mit, duc_wartet=True)
    t = mit["taktik"]
    print("  Vorbereitet:", erg, "Runden", runden, "Welle", t["welle"], "Kirche", t["kirche"], "Haeuser", {k: v["status"] for k, v in t.get("haeuser", {}).items()})
    assert erg == "gewonnen", erg


def test_verrat():
    z = neu()
    D = taktik.daten(M)
    t = z["taktik"]
    t["welle"], t["runde"], t["phase"] = 5, 99, "spieler"
    taktik._pruefen(z, D, t)
    while z["taktik"]["phase"] == "szene":
        taktik.szene_weiter(z, M)
    t = z["taktik"]
    assert t["welle"] == 6 and not t["barrikade"]
    assert taktik._e(t, "pascal")["seite"] == "schwarz", "Pascal wechselt die Seite"
    assert any(e["boss"] for e in taktik.lebend(t, "weiss")), "Mr. White erscheint"
    assert "verrat" in t["gesehen"]
    for _ in range(2):
        taktik.runde_beenden(z, M)
        while z["taktik"]["phase"] == "szene":
            taktik.szene_weiter(z, M)
    t = z["taktik"]
    assert taktik._e(t, "pascal").get("ko") and "pascal_geht" in t["gesehen"], "Pascal geht nach der ersten Runde"
    assert taktik._e(t, "alva").get("ko") and "alva_faellt" in t["gesehen"], "Alvas Trupp faellt"
    assert not any(z_[0] == "Alva" for z_ in D["szenen"]["sieg"]), "Dass Sandru sie gerettet hat, erfaehrt der Spieler erst in Akt 3"


def test_mochi_und_casanova():
    z = neu(["kl_loewe_frei", "rt_ausgang_alle"])
    D = taktik.daten(M)
    t = z["taktik"]
    t["welle"], t["runde"], t["phase"] = 5, 99, "spieler"
    taktik._pruefen(z, D, t)
    while z["taktik"]["phase"] == "szene":
        taktik.szene_weiter(z, M)
    t = z["taktik"]
    for e in t["einheiten"]:                     # Der Test prueft das Drehbuch, nicht die Kirche
        if e["seite"] == "schwarz" and e["id"] != "pascal":
            e["ko"] = True
    w = next(e for e in taktik.lebend(t, "weiss"))
    w["bewegung"] = 0
    for _ in range(3):
        taktik.runde_beenden(z, M)
        while z["taktik"]["phase"] == "szene":
            taktik.szene_weiter(z, M)
        for e in z["taktik"]["einheiten"]:
            if e["seite"] == "schwarz" and e["id"] != "pascal":
                e["ko"] = True
    t = z["taktik"]
    assert "mochi" in t["gesehen"], t["gesehen"]
    w["bewegung"] = 7
    w = next(e for e in taktik.lebend(t, "weiss"))
    x, y = w["x"], w["y"]
    taktik.runde_beenden(z, M)
    assert (w["x"], w["y"]) == (x, y) or z["taktik"]["phase"] != "spieler", "Mochi haelt ihn eine Runde auf"
    z["lp"] = 1
    t = z["taktik"]
    t["gesehen"].append("minicu_faellt")
    while t["phase"] == "szene":
        taktik.szene_weiter(z, M)
    if t["phase"] == "spieler":
        d = taktik._e(t, "duc")
        w = next(e for e in taktik.lebend(t, "weiss"))
        d["x"], d["y"] = w["x"] + 2, w["y"]
        taktik._casanova_pruefen(z, D, t)
        assert z["lp"] == kampf.max_lp(kampf.progress(z)["level"]), "Casanovas Verbandskasten"


def test_waffen_symbol():
    """Die Karte nennt die angelegte Waffe, das Sprite bleibt gleich."""
    z = neu()
    w = taktik.ansicht(z, M)["duc_waffe"]
    assert w["id"] and w["name"], w


def test_bonaventure():
    """Faellt der Kapitaen, geben alle Piraten auf. Die Agenten kaempfen weiter."""
    D = taktik.daten(M)
    z = neu()
    t = z["taktik"]
    t["phase"], t["welle"], t["runde"] = "spieler", 4, 1
    k, p, a = feind(D, t, "bonaventure", 1, 1, "k"), feind(D, t, "gunner", 2, 1, "p"), feind(D, t, "agent", 3, 1, "a")
    k.update(ko=True, lp=0)
    taktik._pruefen(z, D, t)
    assert t["phase"] == "szene" and p.get("ko") and not a.get("ko")
    while t["phase"] == "szene":
        taktik.szene_weiter(z, M)
    assert t["phase"] == "spieler" and t["welle"] == 4
    a.update(ko=True, lp=0)
    t["runde"] = 9                               # kein Nachschub mehr offen
    taktik._pruefen(z, D, t)
    assert "ende_4" in t["gesehen"], "Danach endet die Welle wie immer"
    assert all(e[0] != "brand" for w in D["wellen"][4:] for e in w["feinde"]), "Nach seiner Aufgabe kommen keine Piraten mehr"


def test_danzel_flieht():
    """Als Support kaempft Danzel an der Kirchentuer mit. Bei Whites Auftritt flieht er, zur Warnung kommt er zurueck."""
    D = taktik.daten(M)
    z = neu(["rt_ausgang_alle"])
    taktik.hilfe_waehlen(z, M, "danzel")
    taktik.start_schlacht(z, M)
    t = z["taktik"]
    while t["phase"] == "szene":
        taktik.szene_weiter(z, M)
    da = taktik._e(t, "danzel")
    assert da["fest"] and (da["x"], da["y"]) == (27, 15)
    g = feind(D, t, "agent", 28, 15, "g")
    vorher = g["lp"]
    taktik._treffer(t, da, g, taktik.schaden(da, g, D), [])
    assert g["lp"] < vorher, "Er trifft normale Gegner"
    assert taktik._hilfe_bereit(D, t, "danzel")
    for e in taktik.lebend(t, "schwarz"):
        e.update(ko=True, lp=0)
    t["welle"], t["runde"] = 5, 9
    taktik._pruefen(z, D, t)
    while t["phase"] == "szene":
        taktik.szene_weiter(z, M)
    assert t["welle"] == 6 and "danzel_flieht" in t["gesehen"] and da.get("ko") and da.get("geflohen")
    assert not taktik._hilfe_bereit(D, t, "danzel"), "Geflohen naeht er nichts mehr"
    assert taktik._white_warnung(z, t) == "white_warnung_danzel", "Zur Warnung kommt er zurueck"
    # Auch wenn das Trio zerbrochen ist, bleibt Danzel im Dorf. Bibi ist dann weg.
    z = neu(["rt_ausgang_getrennt"])
    taktik.hilfe_waehlen(z, M, "danzel")
    assert taktik._white_warnung(z, z["taktik"]) == "white_warnung_danzel"
    assert not taktik._reserve_frei(z, D, "bibi")
    # Ohne ihn als Support steht er nicht auf der Karte und flieht auch nicht
    z = neu(["rt_ausgang_alle"])
    taktik.start_schlacht(z, M)
    t = z["taktik"]
    assert not any(e["id"] == "danzel" for e in t["einheiten"])


def test_angriff_ohne_bewegung():
    """Wer schon gut steht, greift an, ohne sich zu bewegen. Auch Maxwell."""
    D = taktik.daten(M)
    z = neu()
    t = z["taktik"]
    t["phase"], t["welle"], t["runde"] = "spieler", 1, 1
    wo, mx = taktik._e(t, "wolff"), taktik._e(t, "maxwell")
    g = feind(D, t, "agent", wo["x"] + 1, wo["y"], "g")
    r = feind(D, t, "roboter", mx["x"] + 1, mx["y"], "r")
    assert not wo["gezogen"] and taktik._sicht(z, D, t, wo, True)["reich"]
    assert any(x["id"] == "g" for x in taktik._sicht(z, D, t, wo, True)["ziele"])
    taktik.angreifen(z, M, "wolff", "g")
    assert wo["fertig"] and g["lp"] < g["lp_max"]
    assert taktik.angreifen(z, M, "maxwell", "r")["kampf"] == r["kampf"], "Maxwell oeffnet den echten Kampf"


def test_vorbereitung_prozent():
    """Start 100 %, Vorbereitung zieht ab, nie unter 30 %. Vorschau und Manoever bleiben ohne Aufschlag."""
    D = taktik.daten(M)
    z = {"flags": [], "status": "wahl", "werte": {}}
    assert taktik.vorbereitung(z, D)["prozent"] == 100
    z["flags"] = ["manoever_fertig", "rt_ausgang_alle"]
    assert taktik.vorbereitung(z, D)["prozent"] == 85
    z["werte"] = {"vertrauen." + p: 5 for p in ("elsa", "rosi", "yamamoto", "batu", "anghjulu")}
    z["werte"]["ruf"] = 9
    z["flags"] += ["rt_white_agenten", "gr_kiste_genommen", "holm_zurueck", "steel_mop", "elsa_hilft"]
    assert taktik.vorbereitung(z, D)["prozent"] == 30, "Der Boden"
    # Unvorbereitet kommen sie staerker, gut vorbereitet schwaecher
    def agent(z):
        taktik.beginnen(z, M, art="echt")
        taktik.start_schlacht(z, M)
        while z["taktik"]["phase"] == "szene":
            taktik.szene_weiter(z, M)
        return next(e for e in z["taktik"]["einheiten"] if e["typ"] == "agent")
    stark, schwach = agent({"flags": [], "status": "wahl", "werte": {}}), agent(z)
    assert stark["lp"] > D["feinde"]["agent"]["lp"] > schwach["lp"]
    assert z["taktik"]["kirche"] == 4 and z["taktik"]["batu_warnt"] and z["taktik"]["dorf_rudert"], "Don, Ba Tu und das Dorf wirken"
    assert all(n["runde"] == 4 for n in taktik._nachschub_liste(D, dict(z["taktik"], welle=1))), "Die Boote kommen eine Runde spaeter"
    assert len(taktik._nachschub_liste(D, dict(z["taktik"], welle=4))) == 1, "Das Dorf stoppt den letzten Schub"
    # Die Folgen der Grotte und des Red Trio
    t = {"art": "echt"}
    assert sum(f[0] == "hund" for f in taktik._welle_feinde({"flags": ["gr_kiste_abgegeben"]}, D, t, 1)) == sum(f[0] == "hund" for f in taktik._welle_feinde({"flags": []}, D, t, 1)) + 2
    assert sum(f[0] == "agent" for f in taktik._welle_feinde({"flags": ["rt_white_agenten"]}, D, t, 6)) == sum(f[0] == "agent" for f in taktik._welle_feinde({"flags": []}, D, t, 6)) - 2


def test_elsa_angebot():
    """Elsas Angebot an Tag 20 macht sie zum Trupp, auch ohne Vertrauen. Nach der Belagerung kommt die Uniform in den Spind."""
    D = taktik.daten(M)
    z = {"flags": [], "status": "wahl", "werte": {}}
    assert not taktik._reserve_frei(z, D, "elsa")
    z["flags"] = ["elsa_hilft", "elsa_kampfuniform"]
    assert taktik._reserve_frei(z, D, "elsa") and not taktik._reserve_frei(z, D, "bibi")
    taktik.beginnen(z, M, art="echt")
    z["taktik"].update(phase="gewonnen", welle=5)
    taktik.beenden(z, moddir=M)
    assert "elsa_kampfuniform" in z["flags"], "Sie traegt sie, bis alles vorbei ist"
    taktik.beginnen(z, M, art="echt")
    z["taktik"].update(phase="gewonnen", welle=6)
    taktik.beenden(z, moddir=M)
    assert "elsa_kampfuniform" not in z["flags"] and "elsa_hilft" in z["flags"]


def test_manoever():
    """Das Manoever kann man nicht verlieren, und am Ende steht manoever_fertig."""
    D = taktik.daten(M)
    z = {"flags": [], "status": "wahl", "werte": {}}
    taktik.beginnen(z, M, art="manoever")
    taktik.start_schlacht(z, M)
    t = z["taktik"]
    while t["phase"] == "szene":
        taktik.szene_weiter(z, M)
    assert len(taktik.lebend(t, "schwarz")) == len(D["manoever"]["feinde"])
    z["lp"] = 1
    for _ in range(12):                          # Der Gegner darf ruhig zuschlagen: Kirche und Duc bleiben heil
        if t["phase"] != "spieler":
            break
        taktik.runde_beenden(z, M)
        while t["phase"] == "szene":
            taktik.szene_weiter(z, M)
    assert t["kirche"] == D["kirche"]["lp"] and z["lp"] >= 1, "Nichts geht verloren"
    for e in taktik.lebend(t, "schwarz"):
        e.update(ko=True, lp=0)
    taktik._pruefen(z, D, t)
    while t["phase"] == "szene":
        taktik.szene_weiter(z, M)
    assert t["phase"] == "gewonnen", t["phase"]
    taktik.beenden(z)
    assert z["status"] == "wahl" and "manoever_fertig" in z["flags"] and not z["taktik"]


def test_aufbau():
    """Wiederaufbau (Umbau 04.11.2026, E-123/E-125): abgebrannte Haeuser werden Baustellen, Duc setzt den ersten Stein und
    liefert, nach dem Schwur bauen die Piraten nachts. Ausfuehrlich: tests/test_aufbau_akt3.py."""
    from kern import aufbau
    z = {"flags": ["tk_haus_weg_bar"], "kueche": {"rohstoffe": {"timber": 4}}}
    assert [b["id"] for b in aufbau.ansicht(z)] == ["bar"]
    nie(aufbau.liefern, z, "bar")                   # ohne ersten Stein
    aufbau.beginnen(z, "bar")
    aufbau.liefern(z, "bar")
    assert z["kueche"]["rohstoffe"]["timber"] == 0
    nie(aufbau.liefern, z, "bar")
    assert aufbau.tag_vorbei(z) == [], "Ohne Schwur tragen sie nichts"
    z["flags"].append("buenaventura_schwur")
    assert len(aufbau.tag_vorbei(z)) == 1 and aufbau.baustellen(z)["bar"]["stufe"] == 1
    assert aufbau.tag_vorbei(z) == []



def _tag_lauf(z, kluger, stats=None):
    """Eine Welle wie im Kalender: eigene Karte, Bot spielt, Karte zu."""
    taktik.beginnen(z, M, art="echt")
    taktik.start_schlacht(z, M)
    erg, runden = bot(z, duc_wartet=kluger)
    t = z["taktik"]
    if stats is not None:
        stats.append((t["welle"], erg, runden, t["kirche"], t["yacht"], len(belagerung.stand(z)["kaputt"])))
    return erg


def test_drei_tage():
    """Sechs Wellen im Kalender: Der Stand bleibt zwischen den Karten, am neuen Tag sind alle wieder fit (Duc 01.11.2026)."""
    D = taktik.daten(M)
    assert len(D["wellen"]) == 6 and D["wellen"][-1]["finale"] and D["wellen"][3]["kapitaen"]
    z = {"flags": [], "status": "wahl", "werte": {}, "tag": 21}
    taktik.beginnen(z, M, art="echt")
    t = z["taktik"]
    taktik.aufstellen(z, M, "wolff", D["plaetze"][4]["x"], D["plaetze"][4]["y"])
    platz = (taktik._e(t, "wolff")["x"], taktik._e(t, "wolff")["y"])
    taktik.start_schlacht(z, M)
    while z["taktik"]["phase"] == "szene":
        taktik.szene_weiter(z, M)
    t = z["taktik"]
    assert t["welle"] == 1
    t["kirche"] -= 1
    taktik._e(t, "chiara").update(lp=3)
    taktik._e(t, "wolff").update(lp=0, ko=True)
    for e in taktik.lebend(t, "schwarz"):
        e.update(ko=True, lp=0)
    t["runde"] = 9
    taktik._pruefen(z, D, t)
    while z["taktik"]["phase"] == "szene":
        taktik.szene_weiter(z, M)
    assert z["taktik"]["phase"] == "gewonnen"
    taktik.beenden(z, moddir=M)
    assert z["taktik"] is None and "belagerung_gewonnen" not in z["flags"]
    b = z["belagerung"]
    assert b["fertig"] == 1 and b["t"]["kirche"] == 2 and b["kaputt"], "Viel schiefgegangen: Eine Barrikade ist hin"
    # Zweite Welle am selben Tag: Aufstellung und Verletzungen bleiben, die Pause heilt etwas
    taktik.beginnen(z, M, art="echt")
    t = z["taktik"]
    assert t["kirche"] == 2 and (taktik._e(t, "wolff")["x"], taktik._e(t, "wolff")["y"]) == platz and taktik._e(t, "chiara")["lp"] == 3
    taktik.start_schlacht(z, M)
    while z["taktik"]["phase"] == "szene":
        taktik.szene_weiter(z, M)
    t = z["taktik"]
    assert t["welle"] == 2 and 3 < taktik._e(t, "chiara")["lp"] < taktik._e(t, "chiara")["lp_max"] and not taktik._e(t, "wolff").get("ko")
    t.update(phase="gewonnen")
    taktik.beenden(z, moddir=M)
    # Neuer Tag: alle fit, Rethink wieder voll
    z["tag"] = 22
    taktik.beginnen(z, M, art="echt")
    t = z["taktik"]
    assert taktik._e(t, "chiara")["lp"] == taktik._e(t, "chiara")["lp_max"] and t["kirche"] == 2 and t["rueckspruenge"] == D["rueckspruenge"]


def test_barrikade_haelt():
    """Eine heile Barrikade kostet die Front eine Runde, eine kaputte nicht."""
    D = taktik.daten(M)
    z = {"flags": [], "status": "wahl", "werte": {}, "tag": 21}
    taktik.beginnen(z, M, art="echt")
    t = z["taktik"]
    t["kaputt"] = ["West"]
    taktik.start_schlacht(z, M)
    while z["taktik"]["phase"] == "szene":
        taktik.szene_weiter(z, M)
    t = z["taktik"]
    sued = [e for e in taktik.lebend(t, "schwarz") if e["front"] == "South"]
    west = [e for e in taktik.lebend(t, "schwarz") if e["front"] == "West"]
    assert sued and west and all(taktik._haelt(t, e) for e in sued) and not any(taktik._haelt(t, e) for e in west)
    assert "south" in t["meldung"] and taktik.ansicht(z, M)["barrikaden"]


def _flick_z():
    z = {"flags": [], "status": "taktik", "werte": {}, "tag": 22, "kueche": {"rohstoffe": {"timber": 20, "slate": 2, "granite": 3}}}
    belagerung.stand(z).update(kaputt=["South"], fertig=2, tag=21, t={"kirche": 2, "kirche_max": 3, "yacht": 2, "haeuser": {"bar": {"status": "verloren"}, "post": {"status": "gerettet"}}, "hilfe": [], "hilfe_genutzt": {}, "gesehen": [], "duo_gesehen": [], "rueckspruenge": 0, "vorbereitung": {"prozent": 100, "zeilen": []}},
                               einheiten={}, reserve=[], aufstellung={})
    return z


def test_flicken():
    """Der Morgen danach: Liste, Notration, Minispiel und Petrus Trupp (Duc 01.11.2026)."""
    D = taktik.daten(M)
    z = _flick_z()
    taktik.beginnen(z, M, art="bericht")
    t = z["taktik"]
    assert t["phase"] == "bestand" and not t["flicken"] and z["status"] == "taktik"
    assert kuechen.rohstoffe(z)["timber"] == 24 and kuechen.rohstoffe(z)["slate"] == 4, "Einmal am Tag bringt das Dorf etwas"
    taktik.beenden(z, moddir=M)
    taktik.beginnen(z, M, art="flicken")
    assert kuechen.rohstoffe(z)["timber"] == 24, "Nicht noch einmal"
    ids = sorted(o["id"] for o in belagerung.offen(z, D))
    assert ids == ["barrikade_South", "haus_bar", "kirche", "yacht"], ids
    # Selbst: Drei gute Schlaege, perfekte sparen Holz, Abbruch gibt alles zurueck
    belagerung.starten(z, D, "barrikade_South")
    assert z["status"] == "abbau" and kuechen.rohstoffe(z)["timber"] == 20
    assert belagerung.ende(z) is None and kuechen.rohstoffe(z)["timber"] == 24 and z["status"] == "taktik"
    belagerung.starten(z, D, "barrikade_South")
    belagerung.schlag(z, D, "daneben")
    belagerung.schlag(z, D, "perfekt")
    belagerung.schlag(z, D, "perfekt")
    assert "South" in z["belagerung"]["kaputt"]
    belagerung.schlag(z, D, "gut")
    assert "South" not in z["belagerung"]["kaputt"] and kuechen.rohstoffe(z)["timber"] == 22, "Zwei perfekte sparen zwei Holz"
    assert belagerung.ende(z) == "South Barricade is mended." and z["status"] == "taktik"
    # Kirche: ein Leben, Stein erst Slate, dann Granite
    belagerung.starten(z, D, "kirche")
    for _ in range(3):
        belagerung.schlag(z, D, "gut")
    belagerung.ende(z)
    assert z["belagerung"]["t"]["kirche"] == 3 and z["taktik"]["kirche"] == 3 and kuechen.rohstoffe(z)["slate"] == 2
    # Petrus Trupp kostet mehr Holz, geht ohne Minispiel und ohne Grenze
    holz = kuechen.rohstoffe(z)["timber"]
    belagerung.crew(z, D, "yacht")
    assert z["belagerung"]["t"]["yacht"] == 3 and kuechen.rohstoffe(z)["timber"] == holz - 3 - D["bestand"]["crew_aufschlag"]
    # Das Haus: geflickt heisst Vorsprung im Wiederaufbau
    belagerung.starten(z, D, "haus_bar")
    for _ in range(3):
        belagerung.schlag(z, D, "gut")
    belagerung.ende(z)
    assert "tk_haus_geflickt_bar" in z["flags"] and not belagerung.offen(z, D)
    from kern import aufbau
    z["flags"].append("tk_haus_weg_bar")
    assert aufbau.baustellen(z)["bar"]["stufe"] == 1
    # Drei Minispiele am Morgen, danach nur noch der Trupp
    z = _flick_z()
    z["belagerung"]["mini_tag"], z["belagerung"]["mini_n"] = 22, 3
    nie(belagerung.starten, z, D, "kirche")
    # Ohne Material kein Flicken
    z = _flick_z()
    z["kueche"]["rohstoffe"] = {"timber": 1}
    nie(belagerung.starten, z, D, "barrikade_South")
    nie(belagerung.crew, z, D, "barrikade_South")


def test_sperre():
    """Ab dem Angriff an Tag 21 laufen nur noch Szenen der Belagerung."""
    from kern import ereignisse
    def laeuft(eid, tag, phase):
        ev = {"id": eid, "art": "gag1", "personen": {}, "wann": {"tage": [1, 30], "phasen": [phase], "holt_leute": True}}
        return ereignisse.passt({"tag": tag, "flags": [], "werte": {}}, MODUL, ev, phase)
    assert laeuft("sf_x", 21, "tag") and laeuft("bl_x", 21, "tag")
    assert not laeuft("sf_x", 21, "nachmittag") and not laeuft("sf_x", 21, "nacht") and not laeuft("sf_x", 22, "fruehstueck")
    assert laeuft("bl_x", 21, "abend") and laeuft("bl_x", 22, "fruehstueck")


def test_flinke_roboter():
    """Kobra und Skorpion: im echten Kampf mit ihren Sprites, kein Boss, kommen als Nachschub ueber Land, und der Taser wirkt nicht."""
    z = {"flags": [], "status": "wahl", "werte": {}, "tag": 21}
    D = taktik.daten(M)
    defs = taktik.kampf_defs(z, M)
    for fid, kid, sprite in (("roboter_kobra", "tk_kobra", "RobotCobra"), ("roboter_skorpion", "tk_skorpion", "RobotScorpion")):
        assert D["feinde"][fid]["kampf"] == kid and D["feinde"][fid]["klasse"] == "maschine"
        e = defs["enemies"][kid]
        assert e["sprite"] == sprite and not e.get("boss") and "Unit-01" not in str(e)
        assert os.path.isfile(os.path.join(M, "kampf", sprite, "idle.webp")), sprite
        kz = neu()
        kampf.starten(kz, taktik.kampf_defs(kz, M), kid, rueckkehr={"status": "taktik"})   # Der echte Kampf muss starten koennen
        assert kz["kampf"]["gegner"][0]["name"] == e["name"]
    kommen = [ty for w in D["wellen"] for n in w.get("nachschub", []) for ty, _ in n["feinde"]]
    assert kommen.count("roboter_kobra") == 5 and kommen.count("roboter_skorpion") == 3


def test_kampf_ort():
    """Der Hintergrund des Kampfs passt zum Feld: Strand, Macchia, Felsen, Yacht, Mole, Hafen, Dorf."""
    D = taktik.daten(M)
    for (x, y), ort in {(6, 21): "strand", (9, 22): "strand", (5, 20): "strand", (0, 0): "macchia", (0, 9): "macchia", (20, 0): "felsen", (41, 15): "yacht", (37, 15): "mole",
                        (22, 17): "hafen", (38, 8): "hafen", (24, 16): "kirchplatz", (28, 13): "dorf"}.items():
        assert taktik.kampf_ort(D, x, y) == ort, (x, y, D["raster"][y][x], taktik.kampf_ort(D, x, y), ort)
    z = neu()
    taktik.start_schlacht(z, M)
    t = z["taktik"]
    e = taktik._einheit("probe", "roboter", "schwarz", D["feinde"]["roboter"], 41, 15)
    t["einheiten"].append(e)
    t["kampf_gegen"] = "probe"
    assert taktik.kampf_defs(z, M)["encounters"]["tk_roboter"]["bild"] == D["orte"]["yacht"]
    e["x"], e["y"] = 6, 21
    assert taktik.kampf_defs(z, M)["encounters"]["tk_roboter"]["bild"] == D["orte"]["strand"]
    b = r"X:\AI\SillyTavern3\SillyTavern-Launcher\SillyTavern\data\default-user\backgrounds"
    if os.path.isdir(b):
        for bild in D["orte"].values():
            assert os.path.isfile(os.path.join(b, bild)), bild


def test_posten_je_welle():
    """Welle 1 kommt nur aus Sueden und Westen: keine Posten an der Yacht, nur vier Trupps, und alle stehen auf einem echten Posten."""
    z = {"flags": [], "status": "wahl", "werte": {}, "tag": 21}
    D = taktik.daten(M)
    taktik.beginnen(z, M, art="echt")
    v = taktik.ansicht(z, M, MODUL)
    assert {p["front"] for p in v["plaetze"]} == {"West", "South", "Church"} and v["trupps_max"] == 4
    felder = {(p["x"], p["y"]) for p in v["plaetze"]}
    trupps = [e for e in z["taktik"]["einheiten"] if e["seite"] == "blau" and not e["fest"]]
    assert all((e["x"], e["y"]) in felder for e in trupps) and len({(e["x"], e["y"]) for e in trupps}) == len(trupps)
    assert {p["front"] for p in v["plaetze"] if (p["x"], p["y"]) in {(e["x"], e["y"]) for e in trupps}} >= {"West", "South"}
    assert next(h for h in v["hilfe"] if h["id"] == "lea")["nutzlos"] if any(h["id"] == "lea" for h in v["hilfe"]) else True
    assert "No boats" in taktik._hilfe_nutzen(D, z["taktik"], "lea")
    y = next(p for p in D["plaetze"] if p["front"] == "Yacht")
    try:
        taktik.aufstellen(z, M, "duc", y["x"], y["y"])
        assert False, "Posten an der Yacht ist in Welle 1 gesperrt"
    except ValueError:
        pass
    z["taktik"]["welle_vorher"] = 1
    v = taktik.ansicht(z, M, MODUL)
    assert "Yacht" in {p["front"] for p in v["plaetze"]} and v["trupps_max"] == 6 and taktik._hilfe_nutzen(D, z["taktik"], "lea") is None
    taktik._posten_anpassen(z["taktik"], D)
    assert any((p["x"], p["y"]) == (e["x"], e["y"]) and p["front"] == "Yacht" for p in D["plaetze"] for e in z["taktik"]["einheiten"]), "Kommen Boote, geht jemand an die Mole"


def test_ausschnitt_je_welle():
    """Jede Welle hat ihren Ausschnitt: Alle Feinde, Posten, Haeuser und Trupps liegen darin, und niemand laeuft hinaus (Duc 02.11.2026)."""
    D = taktik.daten(M)
    for i, w in enumerate(D["wellen"]):
        z = {"flags": [], "status": "wahl", "belagerung": {"t": {}, "kaputt": [], "fertig": i, "einheiten": {}, "reserve": [], "aufstellung": {}}} if i else {"flags": [], "status": "wahl"}
        if i:
            z["belagerung"]["t"] = {"kirche": 3}
        taktik.beginnen(z, M, art="echt")
        t = z["taktik"]
        a = taktik._ausschnitt(D, t)
        assert a == w["ausschnitt"], i
        drin = lambda x, y: a[0] <= x <= a[2] and a[1] <= y <= a[3]
        for typ, p in w["feinde"] + [f for n in w.get("nachschub", []) for f in n["feinde"]]:
            assert drin(*p) and taktik._frei(D, t, p[0], p[1], D["feinde"][typ].get("fliegt")), (i, typ, p)
        for p in taktik._plaetze(D, t):
            assert drin(p["x"], p["y"]), (i, p)
        for e in taktik.lebend(t, "blau"):
            assert drin(e["x"], e["y"]), (i, e["id"], e["x"], e["y"])
        for x, y in D["kirche"]["tueren"]:
            assert drin(x, y)
        if w.get("feuer"):
            assert all(drin(h["x"], h["y"]) for h in D["haeuser"]), i
        for e in taktik.lebend(t, "blau"):
            assert all(drin(*f) for f in taktik.erreichbar(D, t, e)), (i, e["id"])
    assert D["wellen"][0]["ausschnitt"][2] < D["wellen"][1]["ausschnitt"][2] and D["wellen"][5]["ausschnitt"][1] < D["wellen"][4]["ausschnitt"][1]


def test_wunden_im_echten_kampf():
    """Wer auf der Karte angeschlagen ist, ist es auch im echten Kampf, und was Maxwell austeilt, bleibt, auch wenn er faellt (Duc 02.11.2026)."""
    z = neu()
    taktik.start_schlacht(z, M)
    while z["taktik"]["phase"] == "szene":
        taktik.szene_weiter(z, M)
    t, D = z["taktik"], taktik.daten(M)
    t["einheiten"] = [e for e in t["einheiten"] if e["seite"] == "blau" and e["id"] in ("duc", "maxwell")]
    mw = taktik._e(t, "maxwell")
    g = taktik._einheit("probe", "agent", "schwarz", D["feinde"]["agent"], mw["x"] + 1, mw["y"])
    g2 = taktik._einheit("rest", "agent", "schwarz", D["feinde"]["agent"], mw["x"] + 9, mw["y"])
    t["einheiten"] += [g, g2]
    g["lp"] = g["lp_max"] // 2
    assert taktik.angreifen(z, M, "maxwell", "probe")["kampf"] == g["kampf"]
    kampf.starten(z, taktik.kampf_defs(z, M), g["kampf"], rueckkehr={"status": "taktik"}, held=taktik.held_start(z, M))
    taktik.doppel_im_kampf(z)
    kg = z["kampf"]["gegner"][0]
    assert abs(kg["lp"] / kg["lp_max"] - 0.5) < 0.1, (kg["lp"], kg["lp_max"])
    kg["lp"] = kg["lp_max"] // 4
    z["kampf"]["ergebnis"] = {"art": "niederlage"}
    kampf.schliessen(z)
    taktik.kampf_ende(z, M, "niederlage")
    assert mw.get("ko") and not g.get("ko")
    assert abs(g["lp"] / g["lp_max"] - 0.25) < 0.1, (g["lp"], g["lp_max"])
    z2 = neu()
    taktik.start_schlacht(z2, M)
    while z2["taktik"]["phase"] == "szene":
        taktik.szene_weiter(z2, M)
    t2 = z2["taktik"]
    w = taktik._einheit("boss", "agent", "schwarz", D["feinde"]["agent"], 1, 1)
    w["boss"], w["lp"] = True, w["lp_max"] // 2
    t2["einheiten"].append(w)
    t2["kampf_gegen"] = "boss"
    kampf.starten(z2, taktik.kampf_defs(z2, M), w["kampf"], rueckkehr={"status": "taktik"})
    taktik.doppel_im_kampf(z2)
    assert z2["kampf"]["gegner"][0]["lp"] == z2["kampf"]["gegner"][0]["lp_max"]


def test_doppel_beide_seiten():
    """Duc und Maxwell bekommen den Schlag des Trupps daneben in den echten Kampf mit, Feinde schlagen auch zu zweit."""
    z = neu()
    taktik.start_schlacht(z, M)
    while z["taktik"]["phase"] == "szene":
        taktik.szene_weiter(z, M)
    t, D = z["taktik"], taktik.daten(M)
    du, wo = taktik._e(t, "duc"), taktik._e(t, "wolff")
    wo["x"], wo["y"] = du["x"] + 1, du["y"] + 1
    g = taktik._einheit("probe", "agent", "schwarz", D["feinde"]["agent"], du["x"] + 1, du["y"])
    t["einheiten"].append(g)
    h, mit = taktik._doppel(z, D, t, du, g)
    assert h is wo and mit >= 1
    assert taktik.angreifen(z, M, "duc", "probe")["kampf"] == g["kampf"]
    kampf.starten(z, taktik.kampf_defs(z, M), g["kampf"], rueckkehr={"status": "taktik"})
    voll = z["kampf"]["gegner"][0]["lp"]
    taktik.doppel_im_kampf(z)
    assert z["kampf"]["gegner"][0]["lp"] < voll and z["kampf"]["gegner"][0]["lp"] > 0
    z2 = neu()
    taktik.start_schlacht(z2, M)
    while z2["taktik"]["phase"] == "szene":
        taktik.szene_weiter(z2, M)
    t2 = z2["taktik"]
    t2["einheiten"] = [e for e in t2["einheiten"] if e["seite"] == "blau"]
    wo2 = taktik._e(t2, "wolff")
    a1 = taktik._einheit("a1", "agent", "schwarz", D["feinde"]["agent"], wo2["x"] + 1, wo2["y"])
    a2 = taktik._einheit("a2", "agent", "schwarz", D["feinde"]["agent"], wo2["x"] - 1, wo2["y"])
    t2["einheiten"] += [a1, a2]
    log, vor = [], wo2["lp"]
    taktik._doppel_feind(z2, D, t2, a1, wo2, log)
    assert log and log[0]["von"] == "a2" and wo2["lp"] < vor
    log2 = []
    taktik._doppel_feind(z2, D, t2, a1, wo2, log2)
    assert not log2, "Jeder schlaegt hoechstens einmal je Runde mit"


def test_szene_id():
    """Der Client spielt die Toene nach Szene: Glocke zur Welle, Tor beim Verrat, Loewe bei Mochi."""
    z = {"flags": [], "status": "wahl", "werte": {}, "tag": 21}
    taktik.beginnen(z, M, art="echt")
    assert taktik.ansicht(z, M, MODUL)["szene_id"] == "welle_1"
    taktik.start_schlacht(z, M)
    t, D = z["taktik"], taktik.daten(M)
    for sid in ("verrat", "mochi_allein", "mochi"):
        taktik._szene(t, D, sid, {"weiter": True})
        assert taktik.ansicht(z, M, MODUL)["szene_id"] == sid, sid


def test_balancing():
    """Duc 02.11.2026 nach Simulation: Soll-Runden, flinke Roboter von allen Seiten, Nordposten, mehr Heilung, jeder Versuch leichter."""
    D = taktik.daten(M)
    assert [w.get("par") for w in D["wellen"]] == [5, 8, 7, 9, 9, None]
    assert [len(w["feinde"]) + sum(len(n["feinde"]) for n in w["nachschub"]) for w in D["wellen"]] == [7, 8, 8, 11, 10, 10]
    def kommt(nr, typ, front):
        w = D["wellen"][nr - 1]
        return any(ty == typ and list(p) in [list(x) for x in D["fronten"][front]] for ty, p in w["feinde"] + [x for n in w["nachschub"] for x in n["feinde"]])
    assert kommt(2, "roboter_kobra", "South") and kommt(3, "roboter_skorpion", "West") and kommt(4, "roboter_kobra", "South") and kommt(4, "roboter_skorpion", "West")
    assert kommt(5, "roboter_kobra", "South") and kommt(5, "roboter_kobra", "North") and kommt(5, "roboter_skorpion", "West") and kommt(6, "roboter_kobra", "North") and kommt(6, "roboter_skorpion", "West")
    for nr, norden in ((1, False), (2, False), (3, False), (4, False), (5, True), (6, True)):      # Der Nordposten nur, wenn von dort etwas kommt
        t = {"art": "echt", "welle": nr}
        assert any(p["front"] == "North" for p in taktik._plaetze(D, t)) == norden, nr
    z = {"flags": [], "status": "wahl", "werte": {}, "tag": 22}
    taktik.beginnen(z, M, art="echt")
    taktik.start_schlacht(z, M)
    while z["taktik"]["phase"] == "szene":
        taktik.szene_weiter(z, M)
    g = taktik.lebend(z["taktik"], "schwarz")[0]
    gid, lp, voll, schlag = g["id"], g["lp"], g["lp_max"], g["angriff"]
    for versuch, f in ((1, .85), (2, .85 ** 2), (3, .85 ** 3), (4, .85 ** 3)):                     # Mehr als drei Stufen gibt es nicht
        z["taktik"]["phase"] = "verloren"
        taktik.neustart_welle(z, M)
        t = z["taktik"]
        g = taktik._e(t, gid)
        assert g["lp"] == max(1, round(lp * f)) and g["lp_max"] == voll and g["angriff"] == max(1, round(schlag * f)), (versuch, g["lp"], g["angriff"])
    taktik._spawn(D, t, [("agent", D["fronten"]["West"][5])])                                      # Auch der Nachschub kommt schwaecher
    n = taktik.lebend(t, "schwarz")[-1]
    assert n["lp"] < n["lp_max"]
    m = kampf.max_lp(kampf.progress(z)["level"])
    z["lp"] = 1
    taktik._welle_start(z, D, t, 2)
    assert z["lp"] == min(m, 1 + int(m * .6))
    assert "milde" not in taktik.BEHALTEN                                                          # Die naechste Welle kommt wieder voll


def test_briefing():
    """Duc 02.11.2026: Vor der Aufstellung sagen sie, was kommt, und man sieht es. Die letzte Welle hat keins, dort kommt erst der Verrat."""
    D = taktik.daten(M)
    for nr in range(1, 6):
        q, w = D["briefing"][str(nr)], D["wellen"][nr - 1]
        assert q["zeilen"][0]["art"] == "titel" and q["kurz"] and not q["zeilen"][-1].get("zu"), nr
        kommen = {ty for ty, _ in w["feinde"] + [x for n in w["nachschub"] for x in n["feinde"]]}
        a = w["ausschnitt"]
        for x in q["zeilen"]:
            assert set(x.get("zeigt", [])) <= kommen, (nr, x)                  # Niemand warnt vor etwas, das nicht kommt
            assert not x.get("zu") or (a[0] <= x["zu"][0] <= a[2] and a[1] <= x["zu"][1] <= a[3]), (nr, x)
            assert "Megan" not in (x.get("wer") or "")
    assert "6" not in D["briefing"]
    for sid, zeilen in D["szenen"].items():                                    # Ab dem Kriegsrat ist Megan nicht erreichbar, sie kommt erst in Akt 3 zurueck
        assert sid.startswith("manoever") or all(x[0] != "Megan" for x in zeilen), sid
    z = {"flags": [], "status": "wahl", "werte": {}, "tag": 21}
    taktik.beginnen(z, M, art="echt")
    a = taktik.ansicht(z, M, MODUL)
    assert a["phase"] == "szene" and a["szene"]["art"] == "titel" and a["szene_id"] == "welle_1" and a["bild"] == D["bilder"]["kampf"]
    assert len(a["feind_start"]) == 7 and [f["in"] for f in a["feind_start"]].count(2) == 2
    taktik.szene_weiter(z, M)
    b = taktik.ansicht(z, M, MODUL)
    assert b["szene"]["wer"] == "Holm" and b["szene"]["pid"] == "holm" and b["szene_rest"] == len(D["briefing"]["1"]["zeilen"]) - 2
    taktik.szene_weiter(z, M)
    assert taktik.ansicht(z, M, MODUL)["szene"]["zeigt"], "Die Feinde, von denen Holm spricht, leuchten"
    taktik.szene_ueberspringen(z, M)
    b = taktik.ansicht(z, M, MODUL)
    assert b["phase"] == "aufstellen" and not b["szene"] and len(b["feind_start"]) == 7        # Aufstellen mit Blick auf die Feinde
    taktik.start_schlacht(z, M)
    b = taktik.ansicht(z, M, MODUL)
    assert b["phase"] == "szene" and b["szene"]["wer"] == "Wolff" and b["welle"] == 1, "Runde 1: die Legion kommt (Drehbuch)"
    taktik.szene_weiter(z, M)
    b = taktik.ansicht(z, M, MODUL)
    assert b["phase"] == "spieler" and b["welle"] == 1 and not b["feind_start"]
    taktik.beginnen(z, M, art="echt")                                          # Wer schon handelt, ueberspringt es
    taktik.start_schlacht(z, M)
    assert z["taktik"]["phase"] in ("spieler", "szene") and not z["taktik"].get("briefing")      # szene: der Beat der ersten Runde
    z = {"flags": [], "status": "wahl", "werte": {}, "tag": 21}                # Wer fehlt, den vertritt Maxwell
    taktik.beginnen(z, M, art="echt")
    z["taktik"]["welle_vorher"] = 1
    taktik.briefing_setzen(z, D)
    assert z["taktik"]["briefing"][2]["wer"] == "Mr. Maximum"
    z["werte"]["vertrauen.rosi"] = 3
    taktik.briefing_setzen(z, D)
    assert z["taktik"]["briefing"][2]["wer"] == "Rosi" and "sonst" not in z["taktik"]["briefing"][2]
    z = {"flags": [], "status": "wahl", "werte": {}, "tag": 23}                # Letzte Welle: stumm aufstellen, und nichts verraet den Norden
    taktik.beginnen(z, M, art="echt")
    t = z["taktik"]
    t["welle_vorher"] = 5
    taktik.briefing_setzen(z, D)
    a = taktik.ansicht(z, M, MODUL)
    assert a["phase"] == "aufstellen" and a["feind_start"]
    assert not any(f["typ"] == "white" or [f["x"], f["y"]] in [list(p) for p in D["fronten"]["North"]] for f in a["feind_start"])
    taktik.start_schlacht(z, M)
    arten = []
    while t["phase"] == "szene":
        arten.append(t["szene"][0].get("art"))
        taktik.szene_weiter(z, M)
    assert "titel" in arten


def test_neustart_kirche():
    """Mit nur einem Leben waere die Welle kaum zu schaffen: Beim Neustart hat die Kirche mindestens zwei."""
    z = {"flags": [], "status": "wahl", "werte": {}, "tag": 22}
    taktik.beginnen(z, M, art="echt")
    t = z["taktik"]
    t["kirche"] = 1
    taktik.start_schlacht(z, M)
    while z["taktik"]["phase"] == "szene":
        taktik.szene_weiter(z, M)
    z["taktik"]["phase"] = "verloren"
    taktik.neustart_welle(z, M)
    assert z["taktik"]["kirche"] == 2 and z["taktik"]["phase"] == "spieler"


def test_schaeden_nach_leistung():
    """Je besser gespielt, desto weniger kaputt."""
    D = taktik.daten(M)
    for fehler_n, n_kaputt in ((0, 0), (2, 1), (5, 2)):
        z = {"flags": [], "status": "wahl", "werte": {}, "tag": 21}
        t = {"welle": 1, "runde": 1, "kirche": 3, "yacht": 3, "einheiten": [], "start": {"kirche": 3 + fehler_n, "yacht": 3}}
        belagerung.schaeden_eintragen(z, D, t)
        assert len(z["belagerung"]["kaputt"]) == n_kaputt, (fehler_n, z["belagerung"]["kaputt"])


def test_kalender_bot():
    """Alle sechs Wellen als eigene Karten: Beide Bots kommen durch, ausser die Kirche faellt. Zahlen fuer den Abgleich."""
    for name, kluger, flags, werte in (("schlicht", False, [], {}), ("klug", True, [], {}), ("vorbereitet", True, ["elsa_hilft", "manoever_fertig", "holm_zurueck", "steel_mop", "rt_ausgang_alle"], {"vertrauen.rosi": 3, "vertrauen.yamamoto": 3, "ruf": 5, "vertrauen.lola": 3})):
        z = {"flags": list(flags), "status": "wahl", "werte": dict(werte), "tag": 21}
        stats, neustarts = [], 0
        for nr in range(1, 7):
            if nr in (3, 5):
                z["tag"] += 1
            erg = _tag_lauf(z, kluger, stats)
            while erg == "verloren" and neustarts < 12:
                neustarts += 1
                taktik.neustart_welle(z, M)
                erg = bot(z, duc_wartet=kluger)[0]
                stats.append(("neu", z["taktik"]["welle"], erg))
            assert erg == "gewonnen", (name, nr, erg, stats)
            taktik.beenden(z, moddir=M)
        print("  ", name, "Neustarts", neustarts, stats)
        assert "belagerung_gewonnen" in z["flags"]


def test_white_warnung():
    """Danzel warnt vor Mr. White, ohne ihn Megan. Beide nennen den dritten Gurt."""
    D = taktik.daten(M)
    z = neu()
    assert taktik._white_warnung(z, z["taktik"]) == "white_warnung_holm"
    z = neu(["rt_ausgang_alle"])
    assert taktik._white_warnung(z, z["taktik"]) == "white_warnung_danzel"
    z["taktik"]["einheiten"].append({"id": "danzel", "ko": True})
    assert taktik._white_warnung(z, z["taktik"]) == "white_warnung_holm", "Wer am Boden liegt, warnt nicht"
    for sid in ("white_warnung_danzel", "white_warnung_holm"):
        assert any("Six Sigma" in x[1] for x in D["szenen"][sid]), sid


def test_drehbuch_finale():
    """Drehbuch "Hold the Line" (Duc 02.11.2026, docs/wiki/welt/drehbuch_finale.md): Beats je Runde, Funk nach der Nacht mit mehr Leben,
    Petrus Ruder, Minicus Szene mit Ducs Wahl, Appell, Whites Angebot, Nachtwache am Tor."""
    D = taktik.daten(M)
    for w in D["wellen"]:
        for b in w.get("beats", []):
            assert b["szene"] in D["szenen"], b
    assert all(x[0] != "Minicu" or not x[1].startswith("Minicu ") for zeilen in D["szenen"].values() for x in zeilen), "Minicu spricht in der ersten Person"
    # Welle 1: Beats in Runde 1 bis 3, jede Szene einmal
    z = {"flags": [], "status": "wahl", "werte": {}, "tag": 21}
    taktik.beginnen(z, M, art="echt")
    taktik.start_schlacht(z, M)
    t = z["taktik"]
    assert t["phase"] == "szene" and t["szene"][0]["wer"] == "Wolff"
    while t["phase"] == "szene":
        taktik.szene_weiter(z, M)
    for e in taktik.lebend(t, "schwarz"):           # der Test prueft das Drehbuch, nicht den Kampf
        e["haelt"] = 99
    for _ in range(2):
        taktik.runde_beenden(z, M)
        while t["phase"] == "szene":
            taktik.szene_weiter(z, M)
    assert {"w1_legion", "w1_hund", "w1_boote"} <= set(t["gesehen"]), t["gesehen"]
    # Funk nach der Nacht: Lola funkt zuerst, Duc hat heute 10 % mehr Leben
    z = {"flags": [], "status": "wahl", "werte": {"vertrauen.lola": 3, "begehren.lola": 4}, "tag": 21, "nacht_bei": {"pid": "lola", "tag": 20}}
    basis = kampf.max_lp(kampf.progress(z)["level"])
    taktik.beginnen(z, M, art="echt")
    taktik.start_schlacht(z, M)
    t = z["taktik"]
    assert t["szene"][0]["wer"] == "Lola" and t["szene"][0]["text"] == D["funk"]["lola"][1], t["szene"][0]
    assert kampf.lp_max_duc(z) == int(basis * 1.1) and kampf.lp(z) == kampf.lp_max_duc(z)
    z["tag"] = 22
    assert kampf.lp_max_duc(z) == basis, "nur fuer diesen einen Tag"
    z = {"flags": [], "status": "wahl", "werte": {}, "tag": 21, "nacht_bei": {"pid": "lea", "tag": 19}}
    taktik.beginnen(z, M, art="echt")
    taktik.start_schlacht(z, M)
    assert z["taktik"]["szene"][0]["wer"] == "Wolff" and kampf.lp_max_duc(z) == basis, "Eine Nacht von vorgestern zaehlt nicht"
    # Petrus Ruder: Werkstatt heil, dann rudert das Dorf schon mit einem Punkt weniger Ruf
    t = {"haeuser": {"werkstatt": {"status": "gerettet"}}}
    assert taktik._rudert({"werte": {"ruf": D["ruf_rudert"] - 1}}, D, t)
    assert not taktik._rudert({"werte": {"ruf": D["ruf_rudert"] - 1}}, D, {"haeuser": {"werkstatt": {"status": "verloren"}}})
    # Letzte Welle: Nachtwache am Tor, Minicus Szene mit Wahl, Appell
    z = neu(["bl_nachtwache_wolff"])
    t = z["taktik"]
    t["welle"], t["runde"], t["phase"] = 5, 99, "spieler"
    taktik._pruefen(z, D, t)
    while z["taktik"]["phase"] == "szene":
        taktik.szene_weiter(z, M)
    t = z["taktik"]
    taktik._e(t, "wolff").update(x=D["nachtwache"]["feld"][0], y=D["nachtwache"]["feld"][1])
    for e in t["einheiten"]:
        if e["seite"] == "schwarz" and e["id"] != "pascal":
            e["ko"] = True
    next(e for e in taktik.lebend(t, "weiss"))["bewegung"] = 0
    t["runde"] = 4
    t["gesehen"] += ["pascal_geht", "alva_faellt", "mochi", "mochi_allein"]
    taktik._drehbuch(z, D, t)
    t["runde"] = 5
    taktik._drehbuch(z, D, t)
    assert t["szene"][1]["text"] == "You came. Thank you.", "Die Nachtwache steht neben ihm"
    while t["szene"][0].get("art") != "wahl":
        taktik.szene_weiter(z, M)
    taktik.szene_waehlen(z, M, 0)
    assert "bl_minicu_duc_zuerst" in z["flags"] and t["szene"][0]["wer"] == "Duc" and t["szene"][1]["text"] == "...He did."
    taktik._appell(t, D, {"weiter": True})
    wer = [x["wer"] for x in t["szene"]]
    assert wer[0] == "Holm" and "Lola" in wer and "Wolff" in wer and t["szene"][-1]["text"] == D["appell"]["ende"]
    assert any(x["text"] == "Minicu." for x in t["szene"]), "Minicu bekommt Stille"
    # Stimme: Jede gesprochene Zeile hat eine Kennung, die das Vertonungs-Skript kennt (Duc 02.11.2026)
    alle = {k: (pid, text) for k, pid, text in taktik.alle_zeilen(M)}
    assert len(alle) == len(taktik.alle_zeilen(M)), "Kennungen eindeutig"
    for x in t["szene"]:
        if x.get("zid"):
            assert alle[x["zid"]][1] == x["text"], x
    assert taktik.zeile(M, "tk.minicu_faellt.4") == ("minicu", "Then I'm sorry for you.")
    assert taktik.zeile(M, "tk.minicu_faellt.13.w0.1") == ("pascal", "...He did.")
    # Welle 5: Whites Angebot nur mit dem Auftrag Funk
    for flags, soll in (([], False), (["bl_funk_white"], True)):
        z = {"flags": flags, "status": "wahl", "werte": {}, "tag": 23}
        taktik.beginnen(z, M, art="echt")
        t = z["taktik"]
        t.update(welle=5, runde=9, phase="spieler")
        for e in t["einheiten"]:
            if e["seite"] != "blau":
                e["ko"] = True
        t["einheiten"] = [e for e in t["einheiten"] if e["seite"] == "blau"]
        taktik._pruefen(z, D, t)
        assert (t["nach_szene"] or {}).get("szene") == ("white_angebot" if soll else None), (flags, t["nach_szene"])


def main():
    for f in (test_balancing, test_briefing, test_drei_tage, test_barrikade_haelt, test_flicken, test_sperre, test_flinke_roboter, test_kampf_ort, test_posten_je_welle, test_ausschnitt_je_welle, test_wunden_im_echten_kampf, test_doppel_beide_seiten, test_szene_id, test_neustart_kirche, test_schaeden_nach_leistung, test_kalender_bot, test_maxwell_echter_kampf, test_raster, test_plaetze, test_hilfe_wahl, test_hilfe_wirkung, test_gelaende, test_break_und_doppel, test_plan_stimmt, test_white_gesperrt, test_nachschub_und_haeuser, test_reserve, test_macht, test_rueckspringen, test_schusslinie, test_fernkampf, test_yacht, test_echte_kaempfe, test_figuren, test_anim, test_dreieck, test_verhalten, test_eigenschaften, test_staerke, test_fehler_und_zurueck, test_nichts_tun_verliert, test_durchspielen, test_gewinnbar, test_vorbereitung_zahlt, test_verrat, test_mochi_und_casanova, test_vorbereitung_prozent, test_elsa_angebot, test_manoever, test_aufbau, test_white_warnung, test_angriff_ohne_bewegung, test_danzel_flieht, test_bonaventure, test_waffen_symbol, test_drehbuch_finale):
        f()
        print("ok", f.__name__)
    print("OK")


if __name__ == "__main__":
    main()
