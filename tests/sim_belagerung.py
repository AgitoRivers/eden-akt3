# -*- coding: utf-8 -*-
"""Simuliert die sechs Wellen wie im Kalender: drei Tage, Stand bleibt, morgens geflickt. python tests/sim_belagerung.py [Laeufe]

Kein Gate, nur zum Balancing (Duc 02.11.2026). Der echte Kampf ist geschaetzt, Support spielt nicht mit, die Zahlen zeigen also nur die Richtung."""
import os, random, sys
EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, EDEN)
sys.path.insert(0, os.path.join(EDEN, "tests"))
os.chdir(EDEN)
import copy, json  # noqa
import test_taktik as TT  # noqa
from kern import kampf, taktik  # noqa

M = TT.M
TAG = {1: 21, 2: 21, 3: 22, 4: 22, 5: 23, 6: 23}
taktik.BOT_ERLAUBT = True
_ende = taktik.kampf_ende
LAUF = {}


def kampf_ende(z, moddir, ergebnis):
    """Der echte Kampf kostet LP, je nach Gegner und Koennen. Wer nicht mehr genug hat, faellt."""
    t = z["taktik"]
    g = taktik._e(t, t["kampf_gegen"]) if t.get("kampf_gegen") else None
    held = t.get("kampf_held") or "duc"
    if g and not g.get("boss"):
        r = LAUF["rng"]
        last = 0.20 * (g["lp"] / max(1, g["lp_max"])) * (g["angriff"] / 9) * LAUF["koennen"] * r.uniform(.7, 1.3)
        if held == "maxwell":
            e = taktik._e(t, "maxwell")
            rest = e["lp"] / max(1, e["lp_max"]) - last
            z["held_zurueck"] = {"lp_anteil": max(.02, rest), "tasche": [], "gegner_anteil": .5}
            ergebnis = "ko" if rest > 0 else "niederlage"
            LAUF["maxwell"] += 1
        else:
            m = kampf.max_lp(kampf.progress(z)["level"])
            z["lp"] = kampf.lp(z) - int(m * last)
            ergebnis = "ko" if z["lp"] > 0 else "niederlage"
            if z["lp"] <= 0:
                z["lp"] = 1
            LAUF["duc"] += 1
    else:
        LAUF["duc"] += 1
    return _ende(z, moddir, ergebnis)


taktik.kampf_ende = kampf_ende


def wuerfeln(t, r):
    """Andere Aufstellung je Lauf: zwei Trupps tauschen die Posten."""
    tr = [e for e in taktik.lebend(t, "blau") if not e["fest"]]
    if len(tr) >= 2 and r.random() < .7:
        a, b = r.sample(tr, 2)
        a["x"], a["y"], b["x"], b["y"] = b["x"], b["y"], a["x"], a["y"]


def warte(z, e):
    if z["taktik"]["phase"] == "spieler":
        taktik.warten(z, e["id"])


def szenen(z):
    while z["taktik"]["phase"] == "szene":
        taktik.szene_weiter(z, M)
    if z["taktik"]["phase"] == "white_neu":
        taktik.white_neu(z)
        kampf_ende_echt(z, "ko")
        szenen(z)


def kampf_ende_echt(z, erg):
    z["status"] = "kampf"
    taktik.kampf_ende(z, M, erg)


def wert(z, D, t, e, g, klug):
    """Wie lohnend ist dieses Ziel? Der Anfaenger nimmt den Naechsten, der normale Spieler denkt nach."""
    tuer = D["kirche"]["tueren"][0]
    if not klug:
        return -abs(g["x"] - e["x"]) - abs(g["y"] - e["y"])
    n = 0
    s = taktik.staerke(e, g)
    n += 25 if s > 1 else -25 if s < 1 else 0
    if e["id"] not in taktik.SPIELER and taktik.schaden(e, g, D) >= g["lp"]:
        n += 40
    n += 20 * (1 - g["lp"] / max(1, g["lp_max"]))
    if abs(g["x"] - tuer[0]) + abs(g["y"] - tuer[1]) <= 6:
        n += 25
    if g["id"] in t.get("_tuer", []):
        n += 80
    if g["boss"]:
        n += 500
    if taktik._zerlegt_yacht(t, g):
        n += 30
    if g.get("ki") == "brand" or g.get("typ") == "brand":
        n += 15
    if g.get("typ") == "bonaventure":
        n += 20
    return n - (abs(g["x"] - e["x"]) + abs(g["y"] - e["y"])) * .5


def schwach(z, t, e):
    if e["id"] == "duc":
        return kampf.lp(z) / kampf.max_lp(kampf.progress(z)["level"]) < .35
    return e["id"] == "maxwell" and e["lp"] / max(1, e["lp_max"]) < .3


def trupp_zug(z, D, t, e, klug):
    felder = taktik.erreichbar(D, t, e)
    if klug:                                            # zuerst Leute aus dem Haus holen
        hs = sorted((h for h in D["haeuser"] if t.get("haeuser", {}).get(h["id"], {}).get("status") == "brennt"), key=lambda h: t["haeuser"][h["id"]]["lunte"])
        for h in hs:
            if t["haeuser"][h["id"]]["lunte"] > 3:
                continue
            nah = [f for f in felder if abs(f[0] - h["x"]) + abs(f[1] - h["y"]) <= 1]
            if nah and e["id"] not in taktik.SPIELER:
                taktik.bewegen(z, M, e["id"], *nah[0])
                try:
                    taktik.retten(z, M, e["id"], h["id"])
                    return
                except ValueError:
                    pass
                felder = taktik.erreichbar(D, t, e)
                break
    feinde = taktik.lebend(t, "schwarz") + [g for g in taktik.lebend(t, "weiss") if e["id"] == "duc" and taktik.white_frei(t)]
    if e["id"] != "duc":
        feinde = [g for g in feinde if not g["boss"]]
    if not feinde:
        if not e["fertig"]:
            warte(z, e)
        return
    duc_white = [g for g in feinde if g["boss"]]
    if schwach(z, t, e) and not duc_white:              # Wer kaum noch LP hat, geht in Deckung
        tuer = D["kirche"]["tueren"][0]
        taktik.bewegen(z, M, e["id"], *min(felder, key=lambda f: (abs(f[0] - tuer[0]) + abs(f[1] - tuer[1]), f)))
        if not e["fertig"]:
            warte(z, e)
        return
    beste = None
    if klug:                                            # Die Vorschau zeigt, wer die Kirche trifft: den zuerst
        t["_tuer"] = [p["von"] for p in taktik._plan(dict(z), D, t) if p["an"] == "kirche"]
    for g in sorted(feinde, key=lambda g: not g["boss"]):
        if beste and beste[1]["boss"]:
            break
        for f in felder:
            d = abs(f[0] - g["x"]) + abs(f[1] - g["y"])
            if d > e["reichweite"] or (d == 0):
                continue
            x, y = e["x"], e["y"]
            e["x"], e["y"] = f
            kann = g in taktik.ziele(t, e, D)
            e["x"], e["y"] = x, y
            if kann:
                w = wert(z, D, t, e, g, klug) - (taktik._gelaende(D, dict(e, x=f[0], y=f[1])).get("abwehr", 0) * -1)
                if beste is None or w > beste[0]:
                    beste = (w, g, f)
                break
    if beste:
        _, g, f = beste
        taktik.bewegen(z, M, e["id"], *f)
        szenen(z)
        if t["phase"] == "spieler" and z["taktik"] is t:
            r = taktik.angreifen(z, M, e["id"], g["id"])
            if r.get("kampf"):
                kampf_ende_echt(z, "ko")
        return
    ziel = max(feinde, key=lambda g: wert(z, D, t, e, g, klug))         # nichts in Reichweite: hingehen
    wege = taktik._dijkstra(D, t, e, (ziel["x"], ziel["y"]))
    f = min(felder, key=lambda f: (wege.get(f, 999), f))
    taktik.bewegen(z, M, e["id"], *f)
    if not e["fertig"]:
        warte(z, e)


def spielen(z, klug, max_runden=30):
    D = taktik.daten(M)
    runden = 0
    while runden < max_runden:
        szenen(z)
        t = z["taktik"]
        if t["phase"] in ("gewonnen", "verloren"):
            return t["phase"]
        if klug:
            for e in list(taktik.lebend(t, "blau")):
                if e.get("macht", 0) >= 100:
                    try:
                        taktik.macht_einsetzen(z, M, e["id"])
                        szenen(z)
                    except ValueError:
                        pass
        for e in list(taktik.lebend(t, "blau")):
            t = z["taktik"]
            if t["phase"] != "spieler":
                break
            if e["fest"] or e["fertig"] or e.get("ko"):
                continue
            trupp_zug(z, D, t, e, klug)
            szenen(z)
        szenen(z)
        if z["taktik"]["phase"] == "spieler":
            taktik.runde_beenden(z, M)
            runden += 1
    return "abbruch"


def eine_welle(z, nr, klug, r):
    versuche = 0
    taktik.beginnen(z, M, art="echt")
    t = z["taktik"]
    D = taktik.daten(M)
    for rid in LAUF.get("reserve", ()):                 # Verdiente Trupps kommen mit, solange Platz ist
        if len(taktik._im_einsatz(t)) >= taktik._trupps_max(D, t) or any(e["id"] == rid for e in t["einheiten"]):
            continue
        belegt = {(e["x"], e["y"]) for e in taktik.lebend(t, "blau")}
        frei = [q for q in taktik._plaetze(D, t) if (q["x"], q["y"]) not in belegt]
        if frei:
            q = frei[0]
            taktik.aufstellen(z, M, rid, q["x"], q["y"])
    wuerfeln(t, r)
    taktik.start_schlacht(z, M)
    while True:
        versuche += 1
        erg = spielen(z, klug)
        t = z["taktik"]
        if erg == "gewonnen":
            return versuche, t
        g = "abbruch" if erg == "abbruch" else ("duc" if kampf.lp(z) <= 1 else "kirche" if t["kirche"] <= 0 else "sonst")
        LAUF.setdefault("gruende", {}).setdefault(nr, {})
        LAUF["gruende"][nr][g] = LAUF["gruende"][nr].get(g, 0) + 1
        if versuche >= 4 or erg == "abbruch":
            return None, t
        taktik.neustart_welle(z, M)
        z["lp"] = max(kampf.lp(z), kampf.max_lp(kampf.progress(z)["level"]))
        while z["taktik"]["phase"] == "szene":
            taktik.szene_weiter(z, M)


def lauf(prozent, klug, koennen, seed, variante):
    r = random.Random(seed)
    LAUF.update(rng=r, koennen=koennen)
    z = {"flags": list(LAUF.get("flags", ())), "status": "wahl", "tag": 21, "werte": dict(LAUF.get("werte", {}))}
    taktik.vorbereitung = lambda z_, D_: {"prozent": prozent, "zeilen": []}
    aus = []
    for nr in range(1, 7):
        z["tag"] = TAG[nr]
        if nr in (3, 5):                               # Morgen: alles Wichtige geflickt, Kirche und Yacht je +1, alle ausgeruht
            b = z.get("belagerung") or {}
            b["kaputt"] = []
            s = b.get("t") or {}
            if s:
                s["kirche"] = min(s.get("kirche_max", 3), s.get("kirche", 3) + 1)
                s["yacht"] = min(3, s.get("yacht", 3) + 1)
            kampf.lp_auffuellen(z)
        LAUF.update(duc=0, maxwell=0)
        v, t = eine_welle(z, nr, klug, r)
        fest = t.get("start") or {}
        zeile = {"welle": nr, "versuche": v or 9, "fail": v is None, "runden": t["runde"], "par": taktik.daten(M)["wellen"][nr - 1].get("par", 0),
                 "kirche": fest.get("kirche", t["kirche"]) - t["kirche"], "yacht": fest.get("yacht", t.get("yacht", 0)) - t.get("yacht", 0),
                 "haeuser": sum(1 for h, s in (t.get("haeuser") or {}).items() if s["status"] == "verloren" and h not in fest.get("haeuser_weg", [])),
                 "ko": sum(1 for e in t["einheiten"] if e["seite"] == "blau" and not e["fest"] and e.get("ko") and not e.get("geflohen")),
                 "duc": LAUF["duc"] / max(1, v or 4), "maxwell": LAUF["maxwell"] / max(1, v or 4), "duc_lp": round(kampf.lp(z) / kampf.max_lp(kampf.progress(z)["level"]), 2)}
        aus.append(zeile)
        if v is None:                                  # hier kaeme ein Spieler nicht weiter: fuer den Rest der Rechnung durchwinken
            t["phase"] = "gewonnen"
            for e in taktik.lebend(t, "schwarz") + taktik.lebend(t, "weiss"):
                e["ko"] = True
        taktik.beenden(z, moddir=M)
    return aus


def tabelle(erg):
    print("  W | erst% | Vers | fest | Rd/Par | Kirche | Yacht | Haus | KO  | Duc-K | Max-K | Duc-LP")
    for nr in range(1, 7):
        zs = [l[nr - 1] for l in erg]
        n = len(zs)
        m = lambda k: sum(z[k] for z in zs) / n
        print("  %d | %4d%% | %4.1f | %3d%% | %4.1f/%d | %6.2f | %5.2f | %4.2f | %3.1f | %5.1f | %5.1f | %5.2f" % (
            nr, 100 * sum(z["versuche"] == 1 for z in zs) / n, sum(min(z["versuche"], 4) for z in zs) / n, 100 * sum(z["fail"] for z in zs) / n, m("runden"), zs[0]["par"], m("kirche"), m("yacht"), m("haeuser"), m("ko"), m("duc"), m("maxwell"), m("duc_lp")))


if __name__ == "__main__":
    name = "jetzt"
    seeds = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    alle = {"flags": ["elsa_hilft", "rt_ausgang_alle"], "werte": {"vertrauen.rosi": 3, "vertrauen.yamamoto": 3}}
    for titel, klug, koennen, pr, res in (("Anfaenger, 100 %, keine Reserve", False, 1.3, 100, ()), ("Anfaenger, 80 %, Elsa", False, 1.3, 80, ("elsa",)), ("Normal, 70 %, Rosi+Elsa", True, 1.0, 70, ("rosi", "elsa")), ("Stark, 40 %, Rosi+Yamamoto", True, .7, 40, ("rosi", "yamamoto"))):
        LAUF.update(reserve=res, **alle)
        erg = []
        for s in range(seeds):
            erg.append(lauf(pr, klug, koennen, s * 31 + 7, name))
        print("== %s: %s, %d Laeufe" % (name, titel, seeds), flush=True)
        tabelle(erg)
        print("  Niederlagen:", LAUF.pop("gruende", {}))
