# -*- coding: utf-8 -*-
"""Taktik-Karte der Belagerung (Duc 31.10.2026, E-102): Trupps schieben wie in Fire Emblem. Status "taktik".

Ablauf: aufstellen -> Welle (Spielerzug, Gegnerzug) -> Szene. Sechs Wellen auf drei Tage (Duc 01.11.2026, E-114): Im Kalender ist jede Welle eine eigene Karte, dazwischen
gilt der Stand aus kern/belagerung.py, ohne Kalender (Vorschau, Tests) laufen sie am Stueck. Die letzte beginnt mit Pascals Verrat.
Crew-Kaempfe sind fest berechnet und werden vorher angezeigt (Staerken-Tabelle aus kern/kampf.py), Duc kaempft im echten Kampfbildschirm.
Die Kirche hat 3 Leben, jeder Schlag zieht 1 ab. Faellt sie oder Duc, startet die aktuelle Welle neu.
Daten: module/eden_rise/taktik.json (werkzeuge/eden_rise/taktik_eden_rise.py). Wiki: docs/wiki/systeme/taktik.md. Test: tests/test_taktik.py."""
import copy, heapq, json, os
from collections import deque

from . import belagerung, kampf

_CACHE = {}
GEBIET_MAXWELL = (37, 14, 43, 17)                  # Mole und Yacht: dort schlaegt Mr. Maximum doppelt zurueck
GEBIET_YACHT = (39, 15, 43, 16)
GEBIET_KAI = ((20, 17, 27, 18), GEBIET_MAXWELL)    # dorthin reicht Lolas Hilfe
HILFE_PLAETZE = 3
BOT_ERLAUBT = False                                  # tests/lauf_test.py und der Spieltest kuerzen die Schlacht ab


def daten(moddir):
    pfad = os.path.join(moddir, "taktik.json")
    t = os.path.getmtime(pfad)
    if _CACHE.get(pfad, (None,))[0] != t:
        _CACHE[pfad] = (t, json.load(open(pfad, encoding="utf-8")))
    return _CACHE[pfad][1]


def aktiv(z):
    return bool(z.get("taktik"))


def _einheit(eid, typ, seite, d, x, y, **extra):
    e = {"id": eid, "typ": typ, "seite": seite, "name": d["name"], "x": x, "y": y, "lp": d.get("lp", 0), "lp_max": d.get("lp", 0), "angriff": d.get("angriff", 0),
         "abwehr": d.get("abwehr", 0), "bewegung": d.get("bewegung", 0), "reichweite": d.get("reichweite", 1), "art": d.get("art"), "klasse": d.get("klasse", "mensch"),
         "figur": d.get("figur"), "rolle": d.get("rolle"), "ki": d.get("ki"), "text": d.get("text"), "kann": d.get("kann"), "gang": d.get("gang", "fuss"), "fliegt": bool(d.get("fliegt")), "boss": bool(d.get("boss")), "pirat": bool(d.get("pirat")), "fest": False, "gezogen": False, "fertig": False, "kampf": d.get("kampf")}
    e.update(extra)
    return e


def _figur(z, d):
    """Welches Blatt: Duc nach seiner Jacke, Chiara mit den Dress Whites nur, wenn sie sie hat (Duc 01.11.2026)."""
    if d.get("figur_jacke"):
        return d["figur_jacke"].get(kampf.equipment(z).get("armor"), d["figur"])
    q = d.get("figur_flag")
    return q["figur"] if q and q["flag"] in z.get("flags", []) else d.get("figur")


def _bed(z, b):
    """Kleine Bedingung der Vorbereitung: {"flag": name} oder {"wert": name, "min": n}."""
    if "flag" in b:
        return b["flag"] in z.get("flags", [])
    return z.get("werte", {}).get(b["wert"], 0) >= b["min"]


def vorbereitung(z, D):
    """Wie stark kommt Alon: Start 100 %, jede Vorbereitung zieht ab, nie unter den Boden (Duc 30.10. und 01.11.2026)."""
    q = D["vorbereitung"]
    zeilen = [{"text": v["text"], "abzug": v["abzug"]} for v in q["punkte"] if _bed(z, v["bed"])]
    return {"prozent": max(q["boden"], 100 - sum(v["abzug"] for v in zeilen)), "zeilen": zeilen}


def _faktor(prozent):
    """Feinde bei 60 % wie auf der Karte ohne Vorbereitung, bei 100 % rund ein Drittel staerker, beim Boden gut ein Fuenftel schwaecher."""
    return 1 + (prozent - 60) / 130


def beginnen(z, moddir, art=None):
    """Status taktik, Aufstellung nach Holms Vorschlag. art: None (Vorschau), "manoever" (Tag 19), "echt" (eine Welle ab Tag 21), "bericht" und "flicken" (der Morgen danach)."""
    D = daten(moddir)
    morgen = art in ("bericht", "flicken")
    einheiten = [_einheit(tid, tid, "blau", d, d["start"][0], d["start"][1], figur=_figur(z, d)) for tid, d in D["trupps"].items()]
    einheiten += [_einheit(tid, tid, "blau", d, d["start"][0], d["start"][1], fest=True) for tid, d in D["wehr"].items()]
    z["taktik"] = {"phase": "aufstellen", "welle": 0, "runde": 0, "kirche": D["kirche"]["lp"], "einheiten": einheiten, "szene": [], "nach_szene": None, "log": [],
                   "barrikade": True, "zaehler": 0, "gesehen": [], "kampf_gegen": None, "sicherung": None, "kampfszene": None,
                   "hilfe": [hid for hid, q in D["hilfe"].items() if q.get("fest")], "hilfe_genutzt": {}, "meldung": None, "yacht": D["yacht_lp"], "rueck": [], "rueckspruenge": D["rueckspruenge"], "zaehler_macht": 0, "cutin": None, "duo_gesehen": []}
    z["taktik"]["art"] = art
    if art == "echt" or morgen:
        z["taktik"]["vorbereitung"] = vorbereitung(z, D)
        if z.get("werte", {}).get("vertrauen.anghjulu", 0) >= 3:    # Don Anghjulu laeutet nuechtern: ein viertes Leben
            z["taktik"]["kirche"] += 1
    z["taktik"]["kirche_max"] = z["taktik"]["kirche"]
    z["status"] = "taktik"
    if (art == "echt" or morgen) and _weiter_aus_stand(z, D, z["taktik"]):
        _don_glocke(z, z["taktik"])
    else:
        kampf.lp_auffuellen(z)
    if art == "echt":
        _posten_anpassen(z["taktik"], D)
        z["taktik"]["batu_warnt"] = z.get("werte", {}).get("vertrauen.batu", 0) >= 3
        z["taktik"]["dorf_rudert"] = _rudert(z, D, z["taktik"])
        briefing_setzen(z, D)
    if morgen:
        t = z["taktik"]
        t.update(art="bestand", phase="bestand", flicken=art == "flicken")
        if art == "bericht":
            belagerung.notration(z, D)


BEHALTEN = ("kirche", "kirche_max", "yacht", "haeuser", "hilfe", "hilfe_genutzt", "gesehen", "duo_gesehen", "vorbereitung", "rueckspruenge", "don_glocke")


def _sprecher(wer):
    """Wessen Gesicht zu einer Zeile gehoert."""
    return {"Mr. Maximum": "maxwell", "Mr. White": "mrwhite", "Totò": "toto", "Ligeia": "sirene", "Buenaventura": "bonaventure", "Duc": None, "": None}.get(wer, wer.lower())


STIMME = {"Mr. Maximum": "maxwell", "Mr. White": "mrwhite", "Totò": "toto", "Ligeia": "sirene", "": None, "Duc": None, "Buenaventura": None}


def _stimme(wer):
    """Wessen Stimme eine Zeile spricht (eden-config.json stimmen.eden_rise). Erzaehlung, Duc und Buenaventura bleiben stumm."""
    return STIMME.get(wer, wer.lower())


def _mit_zid(x, zid, gefuehl=None):
    """Gesprochene Zeilen tragen ihre feste Kennung, damit die Karte die vorab vertonte Datei spielt (Duc 02.11.2026)."""
    if gefuehl and not x.get("gefuehl"):
        x["gefuehl"] = gefuehl
    if _stimme(x.get("wer", "")) and x.get("art") not in ("titel", "wahl"):
        x["zid"] = zid
    return x


def alle_zeilen(moddir):
    """[(schluessel, pid, text)] aller festen Saetze der Karte: Szenen, Wahl-Folgen, Briefings, Appell. Fuer werkzeuge/eden_rise/vertonen_eden_rise.py."""
    D = daten(moddir)
    out = []
    def dazu(zid, wer, text):
        if _stimme(wer) and text:
            out.append((zid, _stimme(wer), text))
    for sid, zeilen in D["szenen"].items():
        for i, x in enumerate(zeilen):
            extra = x[2] if len(x) > 2 else {}
            if extra.get("art") == "wahl":
                for k, o in enumerate(extra["optionen"]):
                    for j, y in enumerate(o.get("dann", [])):
                        dazu("tk.%s.%d.w%d.%d" % (sid, i, k, j), y[0], y[1])
            elif extra.get("art") != "titel":
                dazu("tk.%s.%d" % (sid, i), x[0], x[1])
    for nr, q in D["briefing"].items():
        for i, x in enumerate(q["zeilen"]):
            dazu("tk.br.%s.%d" % (nr, i), x.get("wer", ""), x.get("text"))
            if x.get("sonst"):
                dazu("tk.br.%s.%d.s" % (nr, i), x["sonst"]["wer"], x["sonst"]["text"])
    a = D["appell"]
    dazu("tk.ap.start", "Holm", a["start"])
    dazu("tk.ap.ende", "Holm", a["ende"])
    dazu("tk.ap.lola", "Lola", a["lola"])
    for pid, text in a["zeilen"].items():
        name = (D["trupps"].get(pid) or D["reserve"].get(pid) or {}).get("name", pid.capitalize())
        dazu("tk.ap.%s" % pid, name, text)
        dazu("tk.ap.n.%s" % pid, "Holm", name + ".")
    for pid in a["gefallen"]:
        dazu("tk.ap.n.%s" % pid, "Holm", D["wehr"][pid]["name"] + ".")
    return out


def zeile(moddir, zid):
    """(pid, text) einer festen Zeile der Karte, sonst (None, None)."""
    for k, pid, text in alle_zeilen(moddir):
        if k == zid:
            return pid, text
    return None, None


def briefing_setzen(z, D):
    """Vor der Aufstellung sagen sie, was kommt (Duc 02.11.2026, Vorbild Fire Emblem). Die letzte Welle hat keins, dort kommt erst der Verrat."""
    t = z["taktik"]
    q = D["briefing"].get(str(t.get("welle_vorher", 0) + 1))
    t["briefing"] = []
    for x in (q or {}).get("zeilen", []):
        if x.get("wenn") and not _reserve_frei(z, D, x["wenn"]):
            x = dict(x, **x["sonst"])
        zid = "tk.br.%d.%d" % (t.get("welle_vorher", 0) + 1, len(t["briefing"])) + (".s" if x.get("wenn") and not _reserve_frei(z, D, x["wenn"]) else "")
        t["briefing"].append(_mit_zid({k: v for k, v in x.items() if k not in ("wenn", "sonst")}, zid))


def _vorschau_feinde(z, D, t):
    """Wer in der naechsten Welle kommt und wo, solange aufgestellt wird. in: Runden bis zur Landung. Was erst die Wende bringt, bleibt verborgen."""
    if t.get("art") != "echt" or t["phase"] != "aufstellen":
        return []
    nr = t.get("welle_vorher", 0) + 1
    aus = [(ty, p, 0) for ty, p in _welle_feinde(z, D, t, nr)] + [(ty, p, n["runde"] - 1) for n in _nachschub_liste(D, t, nr) for ty, p in n["feinde"]]
    sicht = []
    for i, (ty, p, spaeter) in enumerate(aus):
        d = D["feinde"][ty]
        if d.get("boss") or (D["wellen"][nr - 1].get("finale") and list(p) in [list(f) for f in D["fronten"]["North"]]):
            continue
        e = _einheit("vor%d" % i, ty, "schwarz", d, p[0], p[1])
        _staerke_setzen(t, e)
        sicht.append({k: e.get(k) for k in ("id", "typ", "seite", "name", "x", "y", "lp", "lp_max", "reichweite", "art", "klasse", "angriff", "abwehr", "bewegung", "figur", "rolle", "text")})
        sicht[-1]["in"] = spaeter
    return sicht


def _welle(D, t):
    return D["wellen"][t["welle"] - 1] if t["welle"] else {}


def _fronten(D, t):
    """Von wo die Welle kommt, um die es gerade geht. Beim Manoever und in der Vorschau alle (Duc 01.11.2026)."""
    if t.get("art") not in ("echt",):
        return set(D["fronten"])
    w = D["wellen"][(t["welle"] or t.get("welle_vorher", 0) + 1) - 1]
    felder = [p for _, p in w["feinde"]] + [p for n in w.get("nachschub", []) for _, p in n["feinde"]]
    return {f for f, fs in D["fronten"].items() if any(list(p) in [list(x) for x in fs] for p in felder)}


def _plaetze(D, t):
    """Nur die Posten an den Fronten dieser Welle und an der Kirche."""
    fronten = _fronten(D, t)
    return [p for p in D["plaetze"] if p["front"] == "Church" or p["front"] in fronten]


def _trupps_max(D, t):
    """Ohne die Front zur See reichen weniger Trupps."""
    return D["trupps_max"] if t.get("art") != "echt" or "Yacht" in _fronten(D, t) else D["trupps_klein"]


def _posten_anpassen(t, D):
    """Holms Plan fuer diese Welle: wer auf einem ruhigen Posten steht, geht dorthin, wo noch niemand ist. Zu viele Trupps gehen auf die Bank. Kommen wieder Boote, geht die Besatzung zurueck an die Mole."""
    while len(_im_einsatz(t)) > _trupps_max(D, t):
        rest = [e for e in _im_einsatz(t) if e["id"] in D["reserve"]]
        if not rest:
            break
        t["einheiten"].remove(rest[-1])
    finale = D["wellen"][min(t.get("welle_vorher", 0), len(D["wellen"]) - 1)].get("finale")
    for e in t["einheiten"]:                         # Minicu steht bei Pascal im Norden, erst zum Verrat schickt Pascal ihn ans Tor (Duc 02.11.2026)
        q = D["wehr"].get(e["id"]) if e["fest"] else None
        if q and q.get("start_finale"):
            e["x"], e["y"] = q["start_finale"] if finale else q["start"]
    frei = _plaetze(D, t)
    feld = {(p["x"], p["y"]): p["front"] for p in frei}
    trupps = _im_einsatz(t)
    if "Yacht" in feld.values() and not any(feld.get((e["x"], e["y"])) == "Yacht" for e in trupps):
        for e in trupps:
            start = D["trupps"].get(e["id"], {}).get("start")
            if start and feld.get(tuple(start)) == "Yacht":
                e["x"], e["y"] = start
    belegt = {(e["x"], e["y"]) for e in trupps if (e["x"], e["y"]) in feld}
    for e in trupps:
        if (e["x"], e["y"]) in feld:
            continue
        leer = [f for f in feld if f not in belegt]
        if not leer:
            break
        besetzt = {feld[f] for f in belegt}
        ziel = min(leer, key=lambda f: (feld[f] in besetzt, feld[f] == "Church", abs(f[0] - e["x"]) + abs(f[1] - e["y"])))
        e["x"], e["y"] = ziel
        belegt.add(ziel)


def _hilfe_nutzen(D, t, hid):
    """Warum diese Hilfe in dieser Welle nichts bringt, sonst None. Der Spieler soll das sehen, bevor er sie mitnimmt (Duc 01.11.2026)."""
    if t.get("art") != "echt":
        return None
    w = D["wellen"][(t["welle"] or t.get("welle_vorher", 0) + 1) - 1]
    if hid == "lea" and "Yacht" not in _fronten(D, t):
        return "No boats come by sea this wave, so she has nothing to do."
    if hid == "lola" and t.get("yacht", 1) <= 0:
        return "Her galley went down with the yacht."
    if hid == "ligeia" and not any(D["feinde"][ty].get("pirat") for ty, _ in w["feinde"] + [x for n in w.get("nachschub", []) for x in n["feinde"]]):
        return "No pirates this wave, so nobody would listen."
    if hid == "danzel" and w.get("finale"):
        return "He will not stay for Mr. White."
    return None


def _sichern(z, D, t):
    """Welle vorbei: Was bis zur naechsten bleibt (Duc 01.11.2026)."""
    b = belagerung.stand(z)
    b.update(fertig=t["welle"], tag=z.get("tag"), t={k: copy.deepcopy(t[k]) for k in BEHALTEN if t.get(k) is not None},
             einheiten={e["id"]: {"lp": e["lp"], "macht": e.get("macht", 0), "ko": bool(e.get("ko"))} for e in t["einheiten"] if e["seite"] == "blau" and e["id"] not in D["hilfe"]},
             reserve=[e["id"] for e in t["einheiten"] if e["id"] in D["reserve"]], aufstellung=t.get("aufstellung") or b.get("aufstellung") or {})
    f = z.setdefault("flags", [])
    for hid, s in (t.get("haeuser") or {}).items():   # Was verloren ging, merkt sich die Story
        if s["status"] == "verloren" and "tk_haus_weg_" + hid not in f:
            f.append("tk_haus_weg_" + hid)
    if t.get("yacht", 1) <= 0 and "tk_yacht_weg" not in f:
        f.append("tk_yacht_weg")


def _don_glocke(z, t):
    """Auftrag Kirche (Tag 23 morgens): Bleibt Don Anghjulu bei den Kindern (bl_kirche_don), laeutet er nuechtern, und die Kirche haelt
    einen Schlag mehr aus, einmal fuer den Rest der Belagerung (Drehbuch Finale, Duc 04.11.2026). Das vierte Leben ab Vertrauen 3 bleibt davon getrennt."""
    if "bl_kirche_don" in z.get("flags", []) and not t.get("don_glocke"):
        t["kirche"] += 1
        t["kirche_max"] = t.get("kirche_max", t["kirche"] - 1) + 1
        t["don_glocke"] = True


def _weiter_aus_stand(z, D, t):
    """Naechste Welle der Belagerung: Stand zurueckholen. Am neuen Tag sind alle wieder auf den Beinen. -> False vor der ersten Welle."""
    b = z.get("belagerung")
    if not b or not b.get("t"):
        return False
    t.update({k: copy.deepcopy(v) for k, v in b["t"].items()})
    t["kaputt"] = list(b["kaputt"])
    neuer_tag = b.get("tag") != z.get("tag")
    if neuer_tag:
        t["rueckspruenge"] = D["rueckspruenge"]
    t["einheiten"] += [_einheit(rid, rid, "blau", D["reserve"][rid], 0, 0) for rid in b.get("reserve", [])]
    for e in t["einheiten"]:
        s = b["einheiten"].get(e["id"])
        if s and not neuer_tag:
            e.update(lp=s["lp"], ko=s["ko"])
        if s:
            e["macht"] = s["macht"]
        if e["id"] in b["aufstellung"]:
            e["x"], e["y"] = b["aufstellung"][e["id"]]
    t["welle_vorher"] = b["fertig"]
    return True


def _t(z):
    if not z.get("taktik"):
        raise ValueError("Gerade laeuft keine Taktik-Karte.")
    return z["taktik"]


def _e(t, eid):
    for e in t["einheiten"]:
        if e["id"] == eid:
            return e
    raise ValueError("Unbekannte Einheit: %s" % eid)


def lebend(t, seite=None):
    return [e for e in t["einheiten"] if not e.get("ko") and (seite is None or e["seite"] == seite)]


def _ausschnitt(D, t):
    """Was von der Karte offen ist, (x0, y0, x1, y1): Im Kalender zeigt jede Welle nur ihre Fronten (Duc 02.11.2026). Niemand verlaesst ihn."""
    if t.get("art") == "echt":
        return D["wellen"][(t.get("welle") or t.get("welle_vorher", 0) + 1) - 1]["ausschnitt"]
    return D["ausschnitt"]


def _im_bild(D, t, x, y):
    a = _ausschnitt(D, t)
    return a[0] <= x <= a[2] and a[1] <= y <= a[3]


def _frei(D, t, x, y, fliegt=False):
    if not _im_bild(D, t, x, y):
        return False
    if fliegt:
        return True
    return D["raster"][y][x] in D["gang"]["fuss"] or (not t["barrikade"] and [x, y] in D["barrikade"])


def _kosten(D, t, e, x, y):
    """Laufkosten fuer e auf dieses Feld oder None, wenn es gesperrt ist (Gangarten, Duc 31.10.2026)."""
    if not _im_bild(D, t, x, y):
        return None
    if e["fliegt"]:
        return 1
    if not t["barrikade"] and [x, y] in D["barrikade"]:
        return 1
    return D["gang"][e["gang"]].get(D["raster"][y][x])


def _gelaende(D, e):
    return {} if e["fliegt"] else D["gelaende"].get(D["raster"][e["y"]][e["x"]], {})


def _getarnt(D, e):
    return e["seite"] == "blau" and bool(_gelaende(D, e).get("tarnung"))


def _sichtbar(D, feind, g):
    """Der Wald versteckt Trupps vor allem, was weiter als 2 Felder weg ist. Drohnen sehen von oben alles."""
    return feind["fliegt"] or not _getarnt(D, g) or _abstand(feind, g) <= 2


def _belegt(t, ohne=None):
    return {(e["x"], e["y"]): e for e in lebend(t) if e is not ohne}


def erreichbar(D, t, e):
    """Felder im Bewegungsradius. Eigene Einheiten darf man durchqueren, Feinde nicht."""
    bel = _belegt(t, e)
    weg = {(e["x"], e["y"]): 0}
    q = [(0, e["x"], e["y"])]
    while q:
        n, x, y = heapq.heappop(q)
        if n > weg[(x, y)]:
            continue
        for a, b in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            k = _kosten(D, t, e, a, b)
            if k is None or n + k > e["bewegung"] or n + k >= weg.get((a, b), 9999):
                continue
            s = bel.get((a, b))
            if s and (s["seite"] == "blau") != (e["seite"] == "blau"):      # Schwarz und Weiss gehoeren zusammen
                continue
            weg[(a, b)] = n + k
            heapq.heappush(q, (n + k, a, b))
    return {f: n for f, n in weg.items() if f == (e["x"], e["y"]) or f not in bel}


def _abstand(a, b):
    return abs(a["x"] - b["x"]) + abs(a["y"] - b["y"])


SCHLAEGT = {"schnell": "fern", "fern": "schwer", "schwer": "schnell"}   # Stein, Schere, Papier auf der Karte, gilt in beide Richtungen (Duc 31.10.2026)


def _rollen_faktor(a, b):
    ra, rb = a.get("rolle"), b.get("rolle")
    if not ra or not rb or ra == rb:
        return 1.0
    return 1.25 if SCHLAEGT[ra] == rb else 0.8


def staerke(a, b):
    """Faktor fuer Angreifer a gegen Ziel b: das Dreieck der Rollen, bei Trupps dazu die Staerken-Tabelle der Waffen (Feinde haben eine Klasse)."""
    f = _rollen_faktor(a, b)
    art = a.get("art")
    if not art or b["seite"] == "blau":
        return f
    if b["klasse"] in kampf.STRONG.get(art, ()):
        return f * 1.5
    if b["klasse"] in kampf.WEAK.get(art, ()):
        return f * 0.67
    return f


def schaden(a, b, D=None):
    if b.get("boss"):
        return 0                                    # nur Duc kann Mr. White stoppen
    abwehr = 0 if a["id"] == "rosi" and b["klasse"] == "maschine" else b["abwehr"]   # Rosi weiss, wo Roboter brechen
    return max(1, int(round(a["angriff"] * staerke(a, b))) - abwehr - (_gelaende(D, b).get("abwehr", 0) if D else 0))


def _schussfrei(D, a, b):
    """Haeuser und Felsen halten Schuesse auf, Drohnen schiessen und fliegen darueber (Duc 31.10.2026)."""
    if D is None or a.get("fliegt") or b.get("fliegt") or _abstand(a, b) <= 1:
        return True
    x, y, x1, y1 = a["x"], a["y"], b["x"], b["y"]
    dx, dy = abs(x1 - x), abs(y1 - y)
    n = max(dx, dy)
    for i in range(1, n):
        cx, cy = int(round(x + (x1 - x) * i / n)), int(round(y + (y1 - y) * i / n))
        if D["raster"][cy][cx] == "#":
            return False
    return True


def reichweite_felder(D, e):
    """Die Felder, die dieser Trupp von hier aus treffen kann."""
    r = e["reichweite"]
    aus = []
    for dx in range(-r, r + 1):
        for dy in range(-(r - abs(dx)), r - abs(dx) + 1):
            x, y = e["x"] + dx, e["y"] + dy
            if (dx or dy) and 0 <= x < D["spalten"] and 0 <= y < D["zeilen"] and _schussfrei(D, e, {"x": x, "y": y}):
                aus.append([x, y])
    return aus


def _kontert(b, a, D=None):
    """Wer aus der Ferne kaempft, wehrt sich direkt daneben nicht (Duc 31.10.2026)."""
    d = _abstand(a, b)
    return bool(b["angriff"]) and d <= b["reichweite"] and not (b["reichweite"] > 1 and d <= 1) and _schussfrei(D, b, a)


def _betaeubt(a, b):
    """Chiaras Taser: Wer getroffen wird, setzt eine Runde aus. Roboter und Mr. White nicht. Bibi kennt das von Ark: nur Tiere (Duc 01.11.2026)."""
    return (a.get("art") == "taser" and b["klasse"] != "maschine" and not b.get("boss")) or (a.get("id") == "bibi" and b["klasse"] == "tier")


SPIELER = ("duc", "maxwell")                         # Ihre Angriffe oeffnen den echten Kampf (Duc 01.11.2026)


def _doppel(z, D, t, a, b):
    """Doppelangriff: ein Trupp, der das Ziel auch erreicht, schlaegt mit. Halber Schaden, drei Viertel ab Vertrauen 3. Kostet ihn nichts."""
    if b.get("boss"):
        return None, 0
    frei = [h for h in lebend(t, "blau") if h is not a and h["id"] not in SPIELER and not h["fest"] and _abstand(h, b) <= h["reichweite"] and _schussfrei(D, h, b)]
    if not frei:
        return None, 0
    h = max(frei, key=lambda h: (schaden(h, b, D), h["id"]))
    faktor = 0.75 if z.get("werte", {}).get("vertrauen." + h["id"], 0) >= 3 else 0.5
    return h, max(1, int(schaden(h, b, D) * faktor))


def _doppel_feind(z, D, t, a, b, log):
    """Auch die Feinde schlagen zu zweit (Duc 01.11.2026): Ein zweiter, der das Ziel erreicht, schlaegt mit halbem Schaden mit, jeder hoechstens einmal je Runde. Mr. White nicht."""
    frei = [h for h in lebend(t, "schwarz") if h is not a and not h["boss"] and h.get("mitgeschlagen") != t["runde"] and not _haelt(t, h) and h["angriff"] > 0
            and _abstand(h, b) <= h["reichweite"] and _sichtbar(D, h, b) and _schussfrei(D, h, b)]
    if not frei or b.get("ko"):
        return
    if b["id"] == "duc":
        h = max(frei, key=lambda h: (_duc_verlust(z, D, h, b), h["id"]))
        verlust = max(1, int(_duc_verlust(z, D, h, b) * 0.5))
        h["mitgeschlagen"] = t["runde"]
        z["lp"] = max(1 if t.get("art") == "manoever" else 0, kampf.lp(z) - verlust)
        log.append({"von": h["id"], "an": "duc", "schaden": verlust})
        return
    h = max(frei, key=lambda h: (schaden(h, b, D), h["id"]))
    h["mitgeschlagen"] = t["runde"]
    _treffer(t, h, b, max(1, int(schaden(h, b, D) * 0.5)), log)


def vorschau(a, b, D=None, mit=0):
    """Was passiert, wenn a b angreift: fest berechnet, ohne Wuerfel. Break: Wer im Vorteil trifft, bekommt keinen Gegenschlag."""
    s = schaden(a, b, D)
    v = {"schaden": s, "lp_danach": max(0, b["lp"] - s - mit), "staerke": staerke(a, b), "zurueck": 0, "break": staerke(a, b) > 1, "betaeubt": _betaeubt(a, b)}
    if v["lp_danach"] > 0 and not v["break"] and _kontert(b, a, D):
        v["zurueck"] = schaden(b, a, D)
    return v


def ziele(t, e, D=None):
    if (e["angriff"] <= 0 and e["id"] != "duc") or e.get("nur_ziehen"):
        return []
    return [g for g in lebend(t) if g["seite"] != e["seite"] and 1 <= _abstand(e, g) <= e["reichweite"] and not (g["boss"] and not white_frei(t)) and _schussfrei(D, e, g)]


def white_frei(t):
    """Mr. White bleibt unbesiegbar, bis Minicu am Tor gefallen ist, sonst wuerde das Drama uebersprungen (Duc 31.10.2026, Figur getauscht 01.11.)."""
    return "minicu_faellt" in t["gesehen"]


def _staerke_setzen(t, e):
    """Je besser vorbereitet, desto schwaecher kommen sie."""
    f = _faktor(t["vorbereitung"]["prozent"])
    e.update(lp=max(1, round(e["lp"] * f)), lp_max=max(1, round(e["lp_max"] * f)), angriff=max(1, round(e["angriff"] * f)))
    _milde_anwenden(t, e)


def _milde_anwenden(t, e):
    """Nach einer Niederlage kommen sie angeschlagen: weniger Leben als voll und schwaecherer Schlag, auch im echten Kampf."""
    f = t.get("milde")
    if f:
        e.update(lp=max(1, round(e["lp"] * f)), angriff=max(1, round(e["angriff"] * f)))


def _spawn(D, t, feinde):
    bel = _belegt(t)
    for typ, pos in feinde:
        d = D["feinde"][typ]
        x, y = pos
        while (x, y) in bel or not _frei(D, t, x, y, d.get("fliegt")):     # besetzt: daneben auftauchen
            x, y = x + 1 if x < D["spalten"] - 1 else 0, y
        t["zaehler"] += 1
        front = next((f for f, felder in D["fronten"].items() if pos in felder), None)
        e = _einheit("g%d" % t["zaehler"], typ, "weiss" if d.get("boss") else "schwarz", d, x, y, front=front, seit=t["runde"])
        if t.get("art") == "echt" and not d.get("boss"):
            _staerke_setzen(t, e)
        if front == "Yacht" and "lea" in t["hilfe"]:   # Lea bremst die Boote: Feinde von See setzen die erste Runde aus
            e["haelt"] = t["runde"]
        if t.get("art") == "echt" and front in D["bestand"]["barrikaden"] and front not in t.get("kaputt", []):   # Eine heile Barrikade kostet sie eine Runde
            e["haelt"] = t["runde"]
        t["einheiten"].append(e)
        bel[(x, y)] = e


def _sicherung(z, t):
    s = copy.deepcopy({k: v for k, v in t.items() if k not in ("sicherung", "rueck")})
    t["sicherung"] = {"t": s, "lp": kampf.lp(z)}


def _welle_start(z, D, t, nr):
    t.update(welle=nr, runde=1, phase="spieler")
    if nr > 1:                                       # kurze Pause zwischen den Wellen: Lola versorgt Duc
        m = kampf.lp_max_duc(z)
        z["lp"] = min(m, kampf.lp(z) + int(m * 0.6))
        for e in t["einheiten"]:                     # Die Crew rappelt sich auf: Gefallene kommen mit der Haelfte zurueck, die anderen bekommen 40 %
            if e["seite"] == "blau" and not e["fest"] and e["lp_max"]:
                e["lp"] = e["lp_max"] // 2 if e.get("ko") else min(e["lp_max"], e["lp"] + int(e["lp_max"] * 0.4))
                e["ko"] = False
        t.pop("tasche_maxwell", None)                # Er ist auf dem Schiff und packt nach (Duc 01.11.2026)
        verband = next((f[len("bl_verband_"):] for f in z.get("flags", []) if f.startswith("bl_verband_")), None)
        if nr == 2 and verband == "duc":             # Lolas letzter guter Verband (Drehbuch, Tag 21 Dinner)
            kampf.lp_auffuellen(z)
        elif nr == 2 and verband:
            for e in t["einheiten"]:
                if e["id"] == verband and e["seite"] == "blau":
                    e["lp"] = e["lp_max"]
    w = D["wellen"][nr - 1] if t.get("art") != "manoever" else {}
    if w.get("finale"):
        t["barrikade"] = False
        t["jana_schutz"] = "bl_kirche_jana" in z.get("flags", [])
        pascal = _e(t, "pascal")
        pascal["seite"] = "schwarz"
        pascal["fest"] = False
        pascal["bewegung"] = 0
        for e in lebend(t, "blau"):
            if e["id"] == "danzel":                  # Sobald Mr. White da ist, rennt er (Duc 01.11.2026)
                e.update(ko=True, geflohen=True)
    _spawn(D, t, _welle_feinde(z, D, t, nr))
    if w.get("feuer"):                               # Was schon abgebrannt ist, brennt nicht noch einmal
        alt = t.get("haeuser") or {}
        t["haeuser"] = {h["id"]: alt[h["id"]] if alt.get(h["id"], {}).get("status") == "verloren" else {"lunte": h["lunte"], "status": "brennt"} for h in D["haeuser"]}
    t["start"] = {"kirche": t["kirche"], "yacht": t.get("yacht", 0), "haeuser_weg": [h for h, s in (t.get("haeuser") or {}).items() if s["status"] == "verloren"]}
    if t.get("art") == "echt" and nr in (1, 3, 5):    # erste Welle des Tages: die Nacht davor
        _nacht_folgen(z, D, t)
    if t.get("art") == "echt":
        heil = [f for f in D["bestand"]["barrikaden"] if f not in t.get("kaputt", [])]
        t["meldung"] = "The %s barricade holds: they lose a round there." % " and ".join(f.lower() for f in heil) if heil else "No barricade is standing. They walk straight in."
    _sicherung(z, t)
    _zug_frisch(z, t)
    _beats(z, D, t)


def _welle_feinde(z, D, t, nr):
    """Wer in dieser Welle kommt. Beim Manoever die Uebung, an Tag 21 mit den Folgen der Story (belagerung.md)."""
    if t.get("art") == "manoever":
        return D["manoever"]["feinde"]
    feinde = list(D["wellen"][nr - 1]["feinde"])
    if t.get("art") == "echt":
        if nr == 1 and "gr_kiste_abgegeben" in z.get("flags", []):      # Alons Halsbaender sind wieder im Umlauf
            feinde += [("hund", D["fronten"]["West"][4]), ("hund", D["fronten"]["West"][5])]
        if D["wellen"][nr - 1].get("finale") and "rt_white_agenten" in z.get("flags", []):        # Einen Teil seiner Leute hat Duc schon geschlagen
            weg = [f for f in feinde if f[0] == "agent"][:2]
            feinde = [f for f in feinde if f not in weg]
    return feinde


def beenden(z, sofort=False, moddir=None):
    """Karte schliessen und die Folgen eintragen. sofort: nur fuer die Test-Bots, die die Schlacht nicht ausspielen."""
    t = _t(z)
    if sofort and not BOT_ERLAUBT:
        raise ValueError("Das geht nur im Test.")
    if t.get("art") == "manoever":
        z.setdefault("flags", []).append("manoever_fertig")
        kampf.lp_auffuellen(z)
    elif t.get("art") == "echt" and (sofort or t["phase"] == "gewonnen"):
        D = daten(moddir)
        if sofort and not t["welle"]:                # Der Bot spielt die Welle nicht, er zaehlt sie nur
            t["welle"] = t.get("welle_vorher", 0) + 1
            t["runde"] = 1
        _sichern(z, D, t)
        belagerung.schaeden_eintragen(z, D, t)
        if t["welle"] >= len(D["wellen"]):
            z.setdefault("flags", []).append("belagerung_gewonnen")
            if "elsa_kampfuniform" in z["flags"]:    # Die Uniform kommt zurueck in den Spind
                z["flags"].remove("elsa_kampfuniform")
            z.setdefault("werte", {})["belagerung_prozent"] = t["vorbereitung"]["prozent"]
    z["taktik"], z["status"] = None, "wahl"


def _zug_frisch(z, t):
    t["gehandelt"] = False
    for e in lebend(t, "blau"):
        e.update(gezogen=False, fertig=e["fest"], von=[e["x"], e["y"]], nur_ziehen=False)
    t.setdefault("rueck", []).append({"t": copy.deepcopy({k: v for k, v in t.items() if k not in ("sicherung", "rueck")}), "lp": kampf.lp(z)})
    t["rueck"] = t["rueck"][-5:]


def rueckspringen(z):
    """Rethink (Duc 31.10.2026): Bis zum ersten Angriff der Runde setzt es alle Zuege gratis zurueck. Danach zurueck zum Rundenbeginn, und ist dort nichts passiert, eine Runde
    weiter, das kostet einen von drei Ruecksprüngen je Schlacht (Divine Pulse)."""
    t = _t(z)
    if t["phase"] not in ("spieler", "verloren"):
        raise ValueError("Es geht nicht weiter zurueck.")
    if _rethink_frei(t):
        r = t["rueck"][-1]
        neu = copy.deepcopy(r["t"])
        neu.update(sicherung=t.get("sicherung"), rueck=t["rueck"], rueckspruenge=t.get("rueckspruenge", 0), phase="spieler", szene=[], nach_szene=None, cutin=None, anim=None, anim_n=t.get("anim_n", 0))
        z["taktik"] = neu
        z["lp"] = r["lp"]
        return
    if t.get("rueckspruenge", 0) <= 0:
        raise ValueError("Es geht nicht weiter zurueck.")
    anders = ("sicherung", "rueck", "rueckspruenge", "cutin", "meldung", "anim", "anim_n")
    jetzt = {k: v for k, v in t.items() if k not in anders}
    stapel = list(t.get("rueck") or [])
    while stapel and {k: v for k, v in stapel[-1]["t"].items() if k not in anders} == jetzt:
        stapel.pop()
    if not stapel:
        raise ValueError("Es geht nicht weiter zurueck.")
    r = stapel[-1]                                   # bleibt liegen: Auch danach gilt er als Beginn dieser Runde
    neu = copy.deepcopy(r["t"])
    neu.update(sicherung=t.get("sicherung"), rueck=stapel, rueckspruenge=t["rueckspruenge"] - 1, phase="spieler", szene=[], nach_szene=None, cutin=None, anim=None, anim_n=t.get("anim_n", 0))
    z["taktik"] = neu
    z["lp"] = r["lp"]
    z["status"] = "taktik"


def _rethink_frei(t):
    """Noch nichts Endgueltiges in dieser Runde, aber schon jemand bewegt?"""
    if t["phase"] != "spieler" or t.get("gehandelt") or not t.get("rueck"):
        return False
    anders = ("sicherung", "rueck", "rueckspruenge", "cutin", "meldung", "anim", "anim_n")
    return {k: v for k, v in t["rueck"][-1]["t"].items() if k not in anders} != {k: v for k, v in t.items() if k not in anders}


def _macht_plus(e, n):
    if e["seite"] == "blau" and not e["fest"]:
        e["macht"] = min(100, e.get("macht", 0) + n)


def macht_einsetzen(z, moddir, eid):
    """Der grosse Moment eines Truppenfuehrers, wenn seine Leiste voll ist."""
    t, D = _t(z), daten(moddir)
    e = _e(t, eid)
    q = D["macht"].get(eid)
    if t["phase"] != "spieler" or e["seite"] != "blau" or not q or e.get("macht", 0) < 100:
        raise ValueError("Die Leiste ist noch nicht voll.")
    art, log = q["art"], []
    feinde = lebend(t, "schwarz")
    def treffe(ziele, faktor):
        if not ziele:
            raise ValueError("Niemand in Reichweite.")
        for g in ziele:
            _treffer(t, e, g, max(1, int(schaden(e, g, D) * faktor)), log)
    if e["fertig"] and art not in ("sammeln", "nochmal"):
        raise ValueError("Dieser Trupp hat schon gehandelt.")
    if art == "rundum":
        treffe([g for g in feinde if _abstand(e, g) <= 1], 1.5)
    elif art == "weit":
        treffe([g for g in feinde if _abstand(e, g) <= 2], 1)
    elif art == "drohnen":
        ziele = [g for g in feinde if g["klasse"] == "flieger" and _abstand(e, g) <= 6]
        if not ziele:
            raise ValueError("Niemand in Reichweite.")
        for g in ziele:
            _treffer(t, e, g, g["lp"], log)
    elif art == "roboter":
        treffe([g for g in feinde if g["klasse"] == "maschine" and _abstand(e, g) <= 3], 2)
    elif art == "schnitt":
        ziele = [g for g in feinde if _abstand(e, g) <= e["reichweite"]]
        treffe(sorted(ziele, key=lambda g: (-g["lp"], g["id"]))[:1], 2.5)
    elif art == "sammeln":
        for g in _im_einsatz(t):
            if g["id"] != "duc" and not g.get("ko"):
                g["lp"] = min(g["lp_max"], g["lp"] + g["lp_max"] // 4)
        m = kampf.lp_max_duc(z)
        z["lp"] = min(m, kampf.lp(z) + m // 4)
    elif art == "nochmal":
        e.update(gezogen=False, fertig=False, von=[e["x"], e["y"]])
    elif art == "lachen":                            # Bibis Angstlachen zieht die Feinde in der Naehe auf sie (Duc 01.11.2026)
        t["lachen"] = {"id": eid, "runde": t["runde"]}
    if art not in ("sammeln", "nochmal"):
        e["fertig"] = True
    e["macht"] = 0
    t["gehandelt"] = True
    t["zaehler_macht"] = t.get("zaehler_macht", 0) + 1
    t["cutin"] = {"n": t["zaehler_macht"], "id": eid, "titel": q["titel"], "ruf": q["ruf"]}
    t["letzter_zug"] = log
    _anim(t, log)
    _pruefen(z, D, t)


def _szene(t, D, sid, danach):
    t["szene"] = [_mit_zid(dict({"wer": x[0], "text": x[1]}, **(x[2] if len(x) > 2 else {})), "tk.%s.%d" % (sid, i)) for i, x in enumerate(D["szenen"].get(sid, []))]
    for i, x in enumerate(t["szene"]):                # Die Wahl merkt sich, woher sie kommt, fuer die Kennung ihrer Folgezeilen
        if x.get("art") == "wahl":
            x["basis"] = "tk.%s.%d" % (sid, i)
    t["nach_szene"] = danach
    t["phase"] = "szene"
    if sid not in t["gesehen"]:
        t["gesehen"].append(sid)


def _reserve_frei(z, D, rid):
    q = D["reserve"][rid]
    if q.get("flag") in z.get("flags", []):          # Verdient per Flag: Bibi nach der Versoehnung, Elsa nach ihrem Angebot an Tag 20
        return True
    return "vertrauen" in q and z.get("werte", {}).get("vertrauen." + rid, 0) >= q["vertrauen"]


def _im_einsatz(t):
    return [e for e in t["einheiten"] if e["seite"] == "blau" and not e["fest"]]


def auf_bank(z, moddir, eid):
    """Ein verdienter Trupp geht von der Karte zurueck."""
    t, D = _t(z), daten(moddir)
    if t["phase"] != "aufstellen" or eid not in D["reserve"]:
        raise ValueError("Dieser Trupp bleibt.")
    t["einheiten"].remove(_e(t, eid))


def aufstellen(z, moddir, eid, x, y):
    t, D = _t(z), daten(moddir)
    if t["phase"] != "aufstellen":
        raise ValueError("Die Aufstellung ist vorbei.")
    if eid in D["reserve"] and not any(e["id"] == eid for e in t["einheiten"]):
        if not _reserve_frei(z, D, eid):
            raise ValueError("Diesen Trupp gibt es noch nicht.")
        if not any(p["x"] == x and p["y"] == y for p in _plaetze(D, t)):
            raise ValueError("Dorthin kann dieser Trupp nicht.")
        dort = next((o for o in t["einheiten"] if (o["x"], o["y"]) == (x, y)), None)
        if dort and dort["id"] not in D["reserve"]:
            raise ValueError("Dieser Platz ist besetzt.")
        if dort:
            t["einheiten"].remove(dort)
        elif len(_im_einsatz(t)) >= _trupps_max(D, t):
            raise ValueError("Mehr Trupps gehen in dieser Welle nicht.")
        t["einheiten"].append(_einheit(eid, eid, "blau", D["reserve"][eid], x, y))
        return
    e = _e(t, eid)
    if e["fest"] or not any(p["x"] == x and p["y"] == y for p in _plaetze(D, t)):   # nur auf die eckigen Plaetze (Duc 31.10.2026)
        raise ValueError("Dorthin kann dieser Trupp nicht.")
    for o in t["einheiten"]:                          # besetzter Platz: die beiden Trupps tauschen
        if o is not e and (o["x"], o["y"]) == (x, y):
            o.update(x=e["x"], y=e["y"])
    e.update(x=x, y=y)


def _hilfe_frei(z, D, hid):
    """Verdient? Holm immer, die anderen ueber Vertrauen."""
    q = D["hilfe"][hid]
    if q.get("flags"):
        return any(f in z.get("flags", []) for f in q["flags"])
    return bool(q.get("fest")) or z.get("werte", {}).get("vertrauen." + q.get("pid", hid), 0) >= q.get("vertrauen", 0)


def hilfe_waehlen(z, moddir, hid):
    """Aufstellung: rein oder raus aus den drei Support-Plaetzen."""
    t, D = _t(z), daten(moddir)
    if t["phase"] != "aufstellen" or hid not in D["hilfe"] or not _hilfe_frei(z, D, hid):
        raise ValueError("Diese Hilfe gibt es gerade nicht.")
    if hid in t["hilfe"]:
        if D["hilfe"][hid].get("fest"):
            raise ValueError("Holm bleibt auf der Bruecke.")
        t["hilfe"].remove(hid)
    elif len(t["hilfe"]) >= HILFE_PLAETZE:
        raise ValueError("Alle Support-Plaetze sind besetzt.")
    else:
        t["hilfe"].append(hid)


def _hilfe_marke(t, takt):
    return {"runde": "w%dr%d" % (t["welle"], t["runde"]), "welle": "w%d" % t["welle"], "schlacht": "ganz"}[takt]


def _hilfe_bereit(D, t, hid):
    takt = D["hilfe"][hid]["takt"]
    if hid == "lola" and t.get("yacht", 1) <= 0:      # Ihre Kombuese liegt auf der Yacht
        return False
    if hid == "danzel" and _welle(D, t).get("finale"):   # Er ist bei Whites Auftritt geflohen
        return False
    return bool(takt) and t["phase"] == "spieler" and t["hilfe_genutzt"].get(hid) != _hilfe_marke(t, takt)


def _im_gebiet(e, gebiete):
    return any(g[0] <= e["x"] <= g[2] and g[1] <= e["y"] <= g[3] for g in gebiete)


def _am_wasser(D, e):
    return any(D["raster"][y][x] in "~S" for y in range(max(0, e["y"] - 2), min(D["zeilen"], e["y"] + 3))
               for x in range(max(0, e["x"] - 2), min(D["spalten"], e["x"] + 3)) if abs(x - e["x"]) + abs(y - e["y"]) <= 2)


def _haelt(t, e):
    return e.get("haelt") == t["runde"] or e.get("schlaeft", 0) >= t["runde"]


def _hilfe_ziele(z, D, t, hid):
    """Trupps oder Fronten, auf die diese Hilfe gerade wirken kann."""
    if hid == "holm":
        return [e["id"] for e in lebend(t, "blau") if not e["fest"] and (e["fertig"] or e["gezogen"])]
    if hid == "lola":
        return [e["id"] for e in lebend(t, "blau") if not e["fest"] and _im_gebiet(e, GEBIET_KAI) and
                (kampf.lp(z) < kampf.lp_max_duc(z) if e["id"] == "duc" else e["lp"] < e["lp_max"])]
    if hid == "danzel":
        return [e["id"] for e in lebend(t, "blau") if not e["fest"] and e["id"] != "duc" and e.get("futter") != t["runde"]]
    if hid == "siri":
        return sorted({e["front"] for e in lebend(t, "schwarz") if e.get("front") and not _haelt(t, e)})
    return []


def hilfe_einsetzen(z, moddir, hid, ziel=None):
    t, D = _t(z), daten(moddir)
    if hid not in t["hilfe"] or not _hilfe_bereit(D, t, hid):
        raise ValueError("Diese Hilfe geht gerade nicht.")
    if hid == "ligeia":
        feinde = [e for e in lebend(t, "schwarz") if e.get("pirat") and _am_wasser(D, e) and not _haelt(t, e)]
        if not feinde:
            raise ValueError("Am Wasser steht gerade kein Pirat.")
        for e in feinde:                             # Sie schlafen zwei Runden, Roboter sind immun (Duc 01.11.2026)
            e["schlaeft"] = t["runde"] + 1
        text = "Ligeia sings. %d pirates fall asleep on the sand." % len(feinde)
        if "ligeia_singt" not in t["gesehen"]:
            _szene(t, D, "ligeia_singt", {})
    elif ziel not in _hilfe_ziele(z, D, t, hid):
        raise ValueError("Dieses Ziel geht nicht.")
    elif hid == "danzel":
        e = _e(t, ziel)
        e["futter"] = t["runde"]
        text = "Danzel sews a plate into %s's coat." % e["name"]
    elif hid == "holm":
        e = _e(t, ziel)
        e.update(gezogen=False, fertig=False, von=[e["x"], e["y"]])
        text = "Holm: %s, go again." % e["name"]
    elif hid == "lola":
        e = _e(t, ziel)
        if e["id"] == "duc":
            m = kampf.lp_max_duc(z)
            z["lp"] = min(m, kampf.lp(z) + int(m * 0.25))
        else:
            e["lp"] = min(e["lp_max"], e["lp"] + int(e["lp_max"] * 0.4))
        text = "Lola patches up %s." % e["name"]
    else:
        feinde = [e for e in lebend(t, "schwarz") if e.get("front") == ziel]
        text = "Siri's stream is live. The %s front stops to watch." % ziel
    if hid == "siri":
        for e in feinde:
            e["haelt"] = t["runde"]
    t["hilfe_genutzt"][hid] = _hilfe_marke(t, D["hilfe"][hid]["takt"])
    t["gehandelt"] = True
    t["meldung"] = text


def start_schlacht(z, moddir):
    t, D = _t(z), daten(moddir)
    if t["phase"] != "aufstellen":
        raise ValueError("Die Schlacht laeuft schon.")
    for hid in t["hilfe"]:                           # Danzel kaempft an der Kirchentuer mit (Duc 01.11.2026)
        q = D["hilfe"][hid].get("einheit")
        if q:
            t["einheiten"].append(_einheit(hid, hid, "blau", q, q["start"][0], q["start"][1], fest=True))
    if t.get("art") == "echt":                       # Was die Story bewirkt hat
        t["batu_warnt"] = z.get("werte", {}).get("vertrauen.batu", 0) >= 3
        t["dorf_rudert"] = _rudert(z, D, t)
        _nachtwache_stellen(z, D, t)
        t["aufstellung"] = {e["id"]: [e["x"], e["y"]] for e in t["einheiten"] if e["seite"] == "blau" and not e["fest"]}
    nr = t.get("welle_vorher", 0) + 1
    if t.get("art") == "manoever":
        _szene(t, D, "manoever_start", {"welle": 1})
    elif t.get("art") == "echt" and str(nr) in D["briefing"]:      # Gesagt ist alles schon, es geht los
        t["briefing"] = []
        _welle_start(z, D, t, nr)
    else:
        _welle_szene(t, D, nr)


def _welle_szene(t, D, nr):
    """Die Szene vor einer Welle, dann die Welle. Vor der letzten rennt Danzel, wenn er noch da ist."""
    w = D["wellen"][nr - 1]
    flieht = w.get("finale") and any(e["id"] == "danzel" for e in lebend(t, "blau"))
    _szene(t, D, w["szene"], {"szene": "danzel_flieht", "dann": {"welle": nr}} if flieht else {"welle": nr})


def szene_waehlen(z, moddir, i):
    """Eine Wahl mitten in einer Szene (Drehbuch Finale, Duc 02.11.2026): Ducs Antwort und was folgt. Nur fuer die Chronik, keine Punkte."""
    t = _t(z)
    if t["phase"] != "szene" or not t["szene"] or t["szene"][0].get("art") != "wahl":
        raise ValueError("Gerade gibt es nichts zu waehlen.")
    o = t["szene"][0]["optionen"][int(i)]
    if o.get("flag") and o["flag"] not in z.setdefault("flags", []):
        z["flags"].append(o["flag"])
    k = t["szene"][0]["optionen"].index(o)
    basis = t["szene"][0].get("basis", "tk.wahl")
    t["szene"] = [_mit_zid(dict({"wer": x[0], "text": x[1]}, **(x[2] if len(x) > 2 else {})), "%s.w%d.%d" % (basis, k, j)) for j, x in enumerate(o.get("dann", []))] + t["szene"][1:]
    if not t["szene"]:
        t["szene"] = [{"wer": "", "text": "..."}]
    return None


def szene_ueberspringen(z, moddir):
    """Skip: bis zur letzten Zeile der Szene, das Briefing ganz. Beim dritten Durchlauf will das niemand mehr hoeren."""
    t = _t(z)
    if t.get("briefing"):
        t["briefing"] = []
    elif t["phase"] == "szene":
        t["szene"] = t["szene"][-1:]
        szene_weiter(z, moddir)


def szene_weiter(z, moddir):
    t, D = _t(z), daten(moddir)
    if t.get("briefing"):
        t["briefing"].pop(0)
        return None
    if t["phase"] != "szene":
        raise ValueError("Gerade laeuft keine Szene.")
    if t["szene"] and t["szene"][0].get("art") == "wahl":       # Weiter ohne Klick nimmt die ruhige Antwort
        return szene_waehlen(z, moddir, t["szene"][0].get("standard", 0))
    if len(t["szene"]) > 1:
        t["szene"].pop(0)
        return None
    t["szene"] = []
    n = t["nach_szene"] or {}
    t["nach_szene"] = None
    t["phase"] = "spieler"
    if n.get("welle"):
        _welle_start(z, D, t, n["welle"])
    elif n.get("szene"):
        _szene(t, D, n["szene"], n.get("dann"))
    elif n.get("appell"):
        _appell(t, D, n.get("dann"))
    elif n.get("pruefen"):
        _pruefen(z, D, t)
    elif n.get("gegner"):
        gegner_zug(z, moddir)
    elif n.get("ende"):
        t["phase"] = n["ende"]
    return None


def bewegen(z, moddir, eid, x, y):
    t, D = _t(z), daten(moddir)
    if t["phase"] != "spieler":
        raise ValueError("Du bist gerade nicht dran.")
    e = _e(t, eid)
    if e["seite"] != "blau" or e["fest"] or e["fertig"] or e["gezogen"]:
        raise ValueError("Dieser Trupp kann nicht mehr ziehen.")
    if (x, y) not in erreichbar(D, t, e):
        raise ValueError("Zu weit weg.")
    e.update(x=x, y=y, gezogen=True)
    if e.get("nur_ziehen"):                          # Hit and Run: Der Angriff war schon, das Weglaufen beendet den Zug
        e.update(nur_ziehen=False, fertig=True)
    _casanova_pruefen(z, D, t)


def zuruecknehmen(z, eid):
    t = _t(z)
    e = _e(t, eid)
    if t["phase"] != "spieler" or e["fertig"] or not e["gezogen"]:
        raise ValueError("Das geht gerade nicht zurueck.")
    e.update(x=e["von"][0], y=e["von"][1], gezogen=False)


def warten(z, eid):
    t = _t(z)
    if t["phase"] != "spieler":
        raise ValueError("Du bist gerade nicht dran.")
    _e(t, eid)["fertig"] = True


def _treffer(t, a, b, s, log):
    if b.get("futter") == t["runde"]:                # Danzels Platte im Futter (Duc 01.11.2026)
        s = max(1, s // 2)
    b["lp"] = max(0, b["lp"] - s)
    _macht_plus(a, s)                                # rund einmal je Welle voll, eingesteckter Schaden laedt doppelt
    _macht_plus(b, s * 2)
    log.append({"von": a["id"], "an": b["id"], "schaden": s, "stark": staerke(a, b) > 1})
    if b["lp"] <= 0 and b["lp_max"]:
        b["ko"] = True


def _zurueck_schlagen(t, a, b, log, D=None):
    """b schlaegt zurueck, wenn er noch steht, a in Reichweite ist und kein Break sitzt."""
    if b.get("ko") or staerke(a, b) > 1 or not _kontert(b, a, D) or b["id"] == "duc":
        return
    n = 1
    x0, y0, x1, y1 = GEBIET_MAXWELL
    if b["id"] == "maxwell" and x0 <= b["x"] <= x1 and y0 <= b["y"] <= y1:
        n = 2                                       # Hold the Gangway
    for _ in range(n):
        if not a.get("ko"):
            if a["id"] == "duc":
                continue
            _treffer(t, b, a, schaden(b, a, D), log)


def angreifen(z, moddir, eid, ziel):
    """Crew: Schnellkampf. Duc: Antwort {"kampf": bid} heisst, eden.py startet den echten Kampf."""
    t, D = _t(z), daten(moddir)
    if t["phase"] != "spieler":
        raise ValueError("Du bist gerade nicht dran.")
    a, b = _e(t, eid), _e(t, ziel)
    if a["seite"] != "blau" or a["fertig"] or a["fest"] or b not in ziele(t, a, D):
        raise ValueError("Dieses Ziel geht nicht.")
    a["fertig"] = True
    t["gehandelt"] = True
    if a["id"] == "maxwell" and b.get("boss"):
        raise ValueError("Nur Duc kann ihn stoppen.")
    if a["id"] in SPIELER:
        t["kampf_gegen"], t["kampf_held"] = b["id"], a["id"]
        h, mit = _doppel(z, D, t, a, b)                # Ein Trupp daneben schlaegt zuerst zu: Der echte Kampf beginnt mit einem angeschlagenen Gegner
        t["kampf_doppel"] = {"von": h["name"], "anteil": mit / max(1, b["lp_max"])} if h else None
        return {"kampf": b["kampf"]}
    if b.get("boss"):
        raise ValueError("Nur Duc kann ihn stoppen.")
    log = []
    h, mit = _doppel(z, D, t, a, b)
    _treffer(t, a, b, schaden(a, b, D), log)
    if h and not b.get("ko"):
        _treffer(t, h, b, mit, log)
        if _betaeubt(h, b):
            b["haelt"] = t["runde"]
        paar = "+".join(sorted((a["id"], h["id"])))
        if paar in D["duo"] and paar not in t.setdefault("duo_gesehen", []):
            t["duo_gesehen"].append(paar)
            t["meldung"] = D["duo"][paar]
    if _betaeubt(a, b) and not b.get("ko"):
        b["haelt"] = t["runde"]
        t["meldung"] = ("%s is blind and soaked. It stops for one round." if a["id"] == "bibi" else "%s is down and twitching. It stops for one round.") % b["name"]
    _zurueck_schlagen(t, a, b, log, D)
    if a["id"] == "yamamoto" and b.get("ko") and not a.get("ko") and a.get("schnitt") != t["runde"]:   # Clean Cut
        a.update(schnitt=t["runde"], fertig=False, gezogen=False, von=[a["x"], a["y"]])
        t["meldung"] = "Clean cut. Yamamoto is not finished."
    t["kampfszene"] = {"a": a["id"], "b": b["id"], "log": log}
    _anim(t, log)
    _pruefen(z, D, t)
    return {}


def doppel_im_kampf(z):
    """Nach kampf.starten: Der Gegner bringt seine Wunden von der Karte mit (Duc 02.11.2026) und hat den Schlag des Trupps daneben schon abbekommen. Die Karte zaehlt andere LP als der echte Kampf, darum der Anteil. Mr. White beginnt immer voll."""
    t = z.get("taktik") or {}
    d = t.pop("kampf_doppel", None)
    if not z.get("kampf") or not t.get("kampf_gegen"):
        return
    e = _e(t, t["kampf_gegen"])
    if e.get("boss"):
        return
    g = z["kampf"]["gegner"][0]
    anteil = e["lp"] / max(1, e["lp_max"]) - (min(0.5, d["anteil"]) if d else 0)
    g["lp"] = max(1, min(g["lp"], int(round(g["lp_max"] * anteil))))


def held_start(z, moddir):
    """Kaempft gerade Maxwell statt Duc? -> Angaben fuer kampf.starten (Duc 01.11.2026), sonst None."""
    t = _t(z)
    hid = t.get("kampf_held")
    if not hid or hid == "duc":
        return None
    e = _e(t, hid)
    return {"id": hid, "lp_anteil": e["lp"] / max(1, e["lp_max"]), "tasche": t.get("tasche_" + hid)}


def _held_ende(z, D, t, hid, gegner, ergebnis):
    """Maxwell kommt aus dem echten Kampf zurueck. Faellt er, ist er bis zur naechsten Welle weg, die Welle laeuft weiter."""
    e, zur = _e(t, hid), z.pop("held_zurueck", None) or {}
    t["tasche_" + hid] = zur.get("tasche", [])
    z["status"] = "taktik"
    if ergebnis in ("ko", "aufgabe", "entkommen") and gegner:
        gegner["ko"] = True
        gegner["lp"] = 0
        _macht_plus(e, 25)
        e["lp"] = max(1, int(round(e["lp_max"] * zur.get("lp_anteil", 1))))
        _pruefen(z, D, t)
    else:
        if gegner and zur.get("gegner_anteil") is not None:   # Was er dem Gegner angetan hat, bleibt auf der Karte
            gegner["lp"] = max(1, int(round(gegner["lp_max"] * zur["gegner_anteil"])))
        e["ko"], e["lp"] = True, 0
        t["meldung"] = "%s is down. He is out until the next wave." % e["name"]


def kampf_ort(D, x, y):
    """Wo auf der Karte gekaempft wird, zuerst die festen Gebiete, dann das Gelaende. Wege gehoeren zum Dorf, zum Hafen, zum Strand oder in die Macchia."""
    feld = {"x": x, "y": y}
    if _im_gebiet(feld, (GEBIET_YACHT,)):
        return "yacht"
    if _im_gebiet(feld, (GEBIET_MAXWELL,)):
        return "mole"
    if _im_gebiet(feld, (GEBIET_KAI[0],)) or (x >= 36 and y <= 18):
        return "hafen"
    g = D["raster"][y][x]
    if g == "S" or (y >= 18 and x <= 18):
        return "strand"
    if g == "B":
        return "felsen"
    if g == "W" or not (16 <= x <= 35 and 8 <= y <= 19):
        return "macchia"
    return "kirchplatz" if g == "T" or (22 <= x <= 29 and 14 <= y <= 16) else "dorf"


def kampf_defs(z, moddir):
    """kaempfe.json plus die Begegnungen der Karte, nur zur Laufzeit."""
    D = daten(moddir)
    defs = dict(kampf.daten(moddir))
    defs["encounters"] = dict(defs["encounters"], **D["begegnungen"])
    defs["enemies"] = dict(defs["enemies"])
    for vid, q in D["vorlagen"].items():
        w = copy.deepcopy(defs["enemies"][q["vorlage"]])
        w.update({k: v for k, v in q.items() if k != "vorlage"})
        defs["enemies"][vid] = w
    t = z.get("taktik") or {}
    gegner = _e(t, t["kampf_gegen"]) if t.get("kampf_gegen") else next((e for e in lebend(t, "weiss") if e["boss"]), None) if t.get("einheiten") else None
    if gegner and gegner.get("kampf") in D["begegnungen"]:   # Der Kampf spielt dort, wo der Gegner steht (Duc 01.11.2026)
        bild = D["orte"][kampf_ort(D, gegner["x"], gegner["y"])]
        defs["encounters"][gegner["kampf"]] = dict(D["begegnungen"][gegner["kampf"]], image=bild, bild=bild)
    return defs


def kampf_ende(z, moddir, ergebnis):
    """Duc kommt aus dem echten Kampf zurueck."""
    t, D = _t(z), daten(moddir)
    gegner = _e(t, t["kampf_gegen"]) if t.get("kampf_gegen") else None
    t["kampf_gegen"] = None
    hid = t.pop("kampf_held", None)
    if hid and hid != "duc":
        _held_ende(z, D, t, hid, gegner, ergebnis)
        return
    z["status"] = "taktik"
    if ergebnis in ("ko", "aufgabe", "entkommen") and gegner:
        gegner["ko"] = True
        _macht_plus(_e(t, "duc"), 25)
        gegner["lp"] = 0
        if gegner.get("boss"):
            for hid, s in t.get("haeuser", {}).items():   # Was verloren ging, merkt sich die Story
                if s["status"] == "verloren" and "tk_haus_weg_" + hid not in z.setdefault("flags", []):
                    z["flags"].append("tk_haus_weg_" + hid)
            if t.get("yacht", 1) <= 0 and "tk_yacht_weg" not in z.setdefault("flags", []):
                z["flags"].append("tk_yacht_weg")
            _szene(t, D, "sieg", {"ende": "gewonnen"})
            return
        _pruefen(z, D, t)
    elif t.get("art") == "manoever":                 # Das Manoever kann man nicht verlieren: wieder aufstehen und weiter
        kampf.lp_auffuellen(z)
    elif gegner and gegner.get("boss"):              # Mr. White: der Kampf beginnt direkt neu (Duc 31.10.2026)
        kampf.lp_auffuellen(z)
        t["phase"] = "white_neu"
        t["kampf_gegen"] = gegner["id"]
    else:
        _szene(t, D, "verloren_duc", {"ende": "verloren"})


def white_neu(z):
    t = _t(z)
    if t["phase"] != "white_neu":
        raise ValueError("Gerade nicht.")
    t["phase"] = "spieler"
    return {"kampf": "tk_white"}


def _nachschub_liste(D, t, nr=None):
    """Die Boote dieser Welle. Ba Tu warnt: Sie kommen eine Runde spaeter. Der Ruf im Dorf stoppt den letzten Schub der zweiten Welle."""
    nr = nr or t["welle"]
    if not nr or t.get("art") in ("manoever", "bestand"):
        return []
    aus = [dict(n) for n in D["wellen"][nr - 1].get("nachschub", [])]
    if t.get("batu_warnt"):
        for n in aus:
            n["runde"] += 1
    if t.get("dorf_rudert") and D["wellen"][nr - 1].get("kapitaen"):
        aus = aus[:-1]
    return aus


def _nachschub_offen(D, t):
    return [n for n in _nachschub_liste(D, t) if n["runde"] > t["runde"]]


def _nachschub(D, t):
    """Neue Boote kommen an (XCOM-Druck: Sie stehen vorher sichtbar auf der Karte)."""
    for n in _nachschub_liste(D, t):
        if n["runde"] == t["runde"]:
            _spawn(D, t, n["feinde"])


def _haeuser_brennen(D, t):
    """Jede Runde brennt die Lunte herunter, ein Brandtrupp daneben macht es schneller."""
    for h in D["haeuser"]:
        s = t.get("haeuser", {}).get(h["id"])
        if not s or s["status"] != "brennt":
            continue
        s["lunte"] -= 1 + sum(1 for e in lebend(t, "schwarz") if e["typ"] == "brand" and abs(e["x"] - h["x"]) + abs(e["y"] - h["y"]) <= 2)
        if s["lunte"] <= 0:
            s["status"] = "verloren"
            t["meldung"] = "%s is gone." % h["name"]


def retten(z, moddir, eid, hid):
    """Ein Trupp neben einem brennenden Haus holt die Leute heraus, das kostet seine Aktion."""
    t, D = _t(z), daten(moddir)
    e = _e(t, eid)
    h = next((h for h in D["haeuser"] if h["id"] == hid), None)
    s = t.get("haeuser", {}).get(hid)
    if t["phase"] != "spieler" or e["seite"] != "blau" or e["fest"] or e["fertig"] or not h or not s or s["status"] != "brennt" or abs(e["x"] - h["x"]) + abs(e["y"] - h["y"]) > 1:
        raise ValueError("Hier kann dieser Trupp niemanden retten.")
    s["status"] = "gerettet"
    e["fertig"] = True
    t["gehandelt"] = True
    t["meldung"] = "%s gets everyone out of %s." % (e["name"], h["name"])


def loeschen(z, moddir, eid, hid):
    """Bibis Wassergranate: Ein brennendes Haus in Reichweite brennt langsamer, das kostet ihre Aktion (Duc 01.11.2026)."""
    t, D = _t(z), daten(moddir)
    e = _e(t, eid)
    h = next((h for h in D["haeuser"] if h["id"] == hid), None)
    s = t.get("haeuser", {}).get(hid)
    if t["phase"] != "spieler" or eid != "bibi" or e["fertig"] or not h or not s or s["status"] != "brennt" or abs(e["x"] - h["x"]) + abs(e["y"] - h["y"]) > e["reichweite"]:
        raise ValueError("Hier kann sie nicht loeschen.")
    s["lunte"] += 3
    e["fertig"] = True
    t["gehandelt"] = True
    t["meldung"] = "Bibi's water grenade buys %s three more rounds." % h["name"]


def _bonaventure_pruefen(D, t):
    """Faellt der Kapitaen, geben seine Maenner auf: We do not burn grandmothers (Duc 01.11.2026)."""
    if not _welle(D, t).get("kapitaen") or "bonaventure_gibt_auf" in t["gesehen"] or not any(e["typ"] == "bonaventure" and e.get("ko") for e in t["einheiten"]):
        return False
    for e in lebend(t, "schwarz"):
        if e.get("pirat"):
            e.update(lp=0, ko=True)
    _szene(t, D, "bonaventure_gibt_auf", {"pruefen": True})
    return True


def _pruefen(z, D, t):
    """Welle geschafft?"""
    if t["phase"] != "spieler" or not t["welle"] or (t.get("art") != "manoever" and _welle(D, t).get("finale")) or _bonaventure_pruefen(D, t):
        return
    if t.get("art") == "manoever":
        if t["welle"] and not lebend(t, "schwarz"):
            _szene(t, D, "manoever_ende", {"ende": "gewonnen"})
        return
    if not lebend(t, "schwarz") and not lebend(t, "weiss") and not _nachschub_offen(D, t):
        for s in t.get("haeuser", {}).values():      # Keine Feinde mehr: Das Dorf loescht den Rest selbst
            if s["status"] == "brennt":
                s["status"] = "gerettet"
        w = _welle(D, t)
        if t.get("art") == "echt":                   # Im Kalender ist die Karte hier zu, die naechste Welle kommt als eigenes Ereignis
            if w.get("feuer") and t.get("haeuser", {}).get(D["ruder_haus"], {}).get("status") != "verloren" and "bl_werkstatt_heil" not in z.setdefault("flags", []):
                z["flags"].append("bl_werkstatt_heil")       # Petrus Ruder (Drehbuch, Aufbau-Pause)
            nach = w.get("nach_ende")
            if nach and _bed_ok(z, t, nach.get("bed", {})):     # Whites Angebot an Pascal, nur mit dem Auftrag Funk (Drehbuch Welle 5)
                _szene(t, D, w["ende"], {"szene": nach["szene"], "dann": {"ende": "gewonnen"}})
            else:
                _szene(t, D, w["ende"], {"ende": "gewonnen"})
            return
        nr = t["welle"] + 1
        d = D["wellen"][nr - 1]
        flieht = d.get("finale") and any(e["id"] == "danzel" for e in lebend(t, "blau"))
        _szene(t, D, w["ende"], {"szene": d["szene"], "dann": {"szene": "danzel_flieht", "dann": {"welle": nr}} if flieht else {"welle": nr}})


def _white_warnung(z, t):
    """Wer warnt Duc vor Mr. White: Danzel, wenn er nach der Quest im Dorf ist und steht, sonst Holm mit Megans Akte (Duc 02.11.2026)."""
    danzel = next((e for e in t["einheiten"] if e["id"] == "danzel"), None)
    if any(f in z.get("flags", []) for f in ("rt_ausgang_alle", "rt_ausgang_getrennt")) and not (danzel and danzel.get("ko") and not danzel.get("geflohen")):   # Geflohen kommt er zur Warnung zurueck
        return "white_warnung_danzel"
    return "white_warnung_holm"


def _casanova_pruefen(z, D, t):
    """Duc erreicht White: Casanova kommt aus der Kirche, einmal."""
    w = [e for e in lebend(t, "weiss") if e["boss"]]
    d = next((e for e in lebend(t, "blau") if e["id"] == "duc"), None)
    if not w or not d or "casanova" in t["gesehen"] or not white_frei(t) or _abstand(w[0], d) > 3:
        return
    kampf.lp_auffuellen(z)                           # der letzte Verbandskasten
    _szene(t, D, _white_warnung(z, t), {"appell": True, "dann": {"szene": "casanova", "dann": {"weiter": True}}})     # Drehbuch: Warnung, Appell, Casanova


def _kirche_tuer(D, e):
    return [e["x"], e["y"]] in D["kirche"]["tueren"]


def _wege(D, t, e):
    """Wegkosten zum Ziel ab e, ohne Bewegungsgrenze. Einheiten sperren nicht, damit Staus nicht festfahren."""
    return _dijkstra(D, t, e, (e["x"], e["y"]))


def _dijkstra(D, t, e, start):
    weg = {start: 0}
    q = [(0, start[0], start[1])]
    while q:
        n, x, y = heapq.heappop(q)
        if n > weg[(x, y)]:
            continue
        for a, b in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            k = _kosten(D, t, e, a, b)
            if k is not None and n + k < weg.get((a, b), 9999):
                weg[(a, b)] = n + k
                heapq.heappush(q, (n + k, a, b))
    return weg


def _yacht_abstand(g):
    x0, y0, x1, y1 = GEBIET_YACHT
    return max(x0 - g["x"], 0, g["x"] - x1) + max(y0 - g["y"], 0, g["y"] - y1)


def _zerlegt_yacht(t, e):
    """Roboter an Bord bleiben und zerlegen die Yacht, solange kein Trupp bis 3 Felder an der Yacht steht (Duc 31.10.2026)."""
    return e["klasse"] == "maschine" and t.get("yacht", 0) > 0 and _im_gebiet(e, (GEBIET_YACHT,)) and not any(_yacht_abstand(g) <= 3 for g in lebend(t, "blau"))


def _absicht(D, t, e):
    """Wohin will der Feind: Kirche, wenn kein Trupp naeher ist. Mr. White will nur zur Kirche."""
    if _zerlegt_yacht(t, e):
        return {"art": "yacht", "feld": (e["x"], e["y"])}
    weg = _wege(D, t, e)
    tueren = [tuple(p) for p in D["kirche"]["tueren"] if tuple(p) in weg]
    beste = min(tueren, key=lambda p: weg[p]) if tueren else None
    n_tuer = weg[beste] if beste else 9999
    if e["boss"]:
        return {"art": "kirche", "feld": beste}
    ki = e.get("ki")
    ziele_ = [g for g in lebend(t, "blau") if (g["x"], g["y"]) in weg and _sichtbar(D, e, g)]
    lacht = t.get("lachen")
    if lacht and lacht["runde"] == t["runde"]:
        g = next((g for g in ziele_ if g["id"] == lacht["id"]), None)
        if g and _abstand(e, g) <= 5:
            return {"art": "trupp", "ziel": g["id"], "feld": (g["x"], g["y"])}
    if ki == "wache" and t["runde"] < e.get("seit", 0) + 3 and not any(_abstand(e, g) <= e["bewegung"] + e["reichweite"] for g in ziele_):
        return {"art": "halten", "feld": (e["x"], e["y"])}
    if ki == "brecher" and beste:
        return {"art": "kirche", "feld": beste}
    if ki == "brand":
        brennt = [h for h in D["haeuser"] if t.get("haeuser", {}).get(h["id"], {}).get("status") == "brennt"]
        if brennt:
            h = min(brennt, key=lambda h: (abs(h["x"] - e["x"]) + abs(h["y"] - e["y"]), h["id"]))
            return {"art": "haus", "feld": (h["x"], h["y"])}
    if ziele_ and ki == "jaeger":
        nah = [g for g in ziele_ if weg[(g["x"], g["y"])] <= e["bewegung"] * 2] or ziele_
        g = min(nah, key=lambda g: (g["lp"] if g["id"] != "duc" else 999, weg[(g["x"], g["y"])], g["id"]))
        return {"art": "trupp", "ziel": g["id"], "feld": (g["x"], g["y"])}
    if ziele_ and ki == "schwaeche":
        g = min(ziele_, key=lambda g: (g["abwehr"], weg[(g["x"], g["y"])], g["id"]))
        return {"art": "trupp", "ziel": g["id"], "feld": (g["x"], g["y"])}
    if ziele_:
        g = min(ziele_, key=lambda g: (weg[(g["x"], g["y"])], g["lp"], g["id"]))
        if weg[(g["x"], g["y"])] <= n_tuer:
            return {"art": "trupp", "ziel": g["id"], "feld": (g["x"], g["y"])}
    return {"art": "kirche", "feld": beste}


def _zum_ziel(D, t, e, feld, reichweite):
    """Feld im Radius, das dem Ziel am naechsten kommt."""
    felder = erreichbar(D, t, e)
    von_ziel = _dijkstra(D, t, e, tuple(feld))
    return min(felder, key=lambda f: (abs(von_ziel.get(f, 999) - reichweite) if von_ziel.get(f, 999) >= reichweite else 500 + von_ziel.get(f, 0), felder[f], f))


def _duc_verlust(z, D, e, duc):
    return max(1, int(kampf.max_lp(kampf.progress(z)["level"]) * max(1, e["angriff"] - _gelaende(D, duc).get("abwehr", 0) * 2) / 200))


def _plan(z, D, t):
    """Was jeder Feind in diesem Gegnerzug tut (Into the Breach): Der echte Zug laeuft auf einer Kopie, also stimmen Ziel und Schaden."""
    kopie = copy.deepcopy({k: v for k, v in t.items() if k != "sicherung"})
    log = []
    _feinde_handeln(dict(z), D, kopie, log)
    plan = []
    for e in sorted(lebend(t, "schwarz") + lebend(t, "weiss"), key=lambda u: u["id"]):
        if _haelt(t, e) or not e["bewegung"] or (e["boss"] and t.get("mochi_runde") == t["runde"]):
            continue
        ab = _absicht(D, t, e)
        if ab.get("feld") is None:
            continue
        p = {"von": e["id"], "x": ab["feld"][0], "y": ab["feld"][1], "art": ab["art"], "von_x": e["x"], "von_y": e["y"], "trifft": False, "schaden": 0, "an": None}
        plan.append(p)
        for i, l in enumerate(x for x in log if x["von"] == e["id"]):   # Schlaegt er auch bei einem anderen mit, zeigt die Vorschau beide Schlaege
            ziel = D["kirche"]["tueren"][0] if l["an"] == "kirche" else (GEBIET_YACHT[0] + 2, GEBIET_YACHT[1]) if l["an"] == "yacht" else (lambda g: (g["x"], g["y"]))(_e(t, l["an"]))
            q = dict(p) if i else p
            q.update(trifft=True, an=l["an"], schaden=l["schaden"], x=ziel[0], y=ziel[1])
            if i:
                plan.append(q)
    return plan


def _gefahr(D, t, e):
    """Alle Felder, die dieser Feind im naechsten Zug treffen kann."""
    felder = set()
    for x, y in erreichbar(D, t, e):
        for dx in range(-e["reichweite"], e["reichweite"] + 1):
            for dy in range(-(e["reichweite"] - abs(dx)), e["reichweite"] - abs(dx) + 1):
                felder.add((x + dx, y + dy))
    return [list(f) for f in felder if 0 <= f[0] < D["spalten"] and 0 <= f[1] < D["zeilen"]]


def _feinde_handeln(z, D, t, log):
    """Alle Feinde ziehen und schlagen. False, wenn die Schlacht dabei verloren geht."""
    gehalten = "mochi_runde" in t and t["mochi_runde"] == t["runde"]
    for e in sorted(lebend(t, "schwarz") + lebend(t, "weiss"), key=lambda u: u["id"]):
        if e["bewegung"] <= 0 and not e["angriff"]:
            continue
        if (e["boss"] and gehalten) or _haelt(t, e):
            continue
        ab = _absicht(D, t, e)
        if ab.get("feld") is None:
            continue
        if ab["art"] == "yacht":                     # hoechstens ein Schaden je Runde, egal wie viele an Bord sind. Sinken kann sie erst am letzten Tag, die Crew schlaeft dort
            if t["yacht"] > (1 if t.get("art") == "echt" and not _welle(D, t).get("yacht_sinkt") else 0) and not any(l["an"] == "yacht" for l in log):
                t["yacht"] -= 1
                log.append({"von": e["id"], "an": "yacht", "schaden": 1})
                t["meldung"] = "Robots are tearing the yacht apart." if t["yacht"] else "The yacht is lost. Lola's galley went down with it."
            continue
        r = 0 if ab["art"] == "kirche" else 1 if e.get("naeher") or ab["art"] == "haus" else e["reichweite"]
        if e["bewegung"] and ab["art"] != "halten":
            neu = _zum_ziel(D, t, e, ab["feld"], r)
            e["x"], e["y"] = neu
        # Elsas Overwatch: einmal je Runde schiesst sie zuerst, wenn ein Feind in Reichweite kommt
        elsa = next((x for x in lebend(t, "blau") if x["id"] == "elsa"), None)
        if elsa and elsa.get("wache") != t["runde"] and _abstand(elsa, e) <= elsa["reichweite"] and not e["boss"] and _schussfrei(D, elsa, e):
            elsa["wache"] = t["runde"]
            _treffer(t, elsa, e, schaden(elsa, e, D), log)
            if e.get("ko"):
                continue
        if _kirche_tuer(D, e) or (e["boss"] and min(abs(e["x"] - p[0]) + abs(e["y"] - p[1]) for p in D["kirche"]["tueren"]) <= 1):
            if t.pop("jana_schutz", False):          # Jana ist bei den Kindern: der erste Schlag an die Tuer bringt niemanden in Panik (Drehbuch Tag 23)
                t["meldung"] = "Jana keeps the children calm. The church holds."
                continue
            t["kirche"] -= 0 if t.get("art") == "manoever" else 1      # Das Manoever kann man nicht verlieren
            log.append({"von": e["id"], "an": "kirche", "schaden": 1})
            if t["kirche"] <= 0:
                _log(t, log)
                _szene(t, D, "verloren_kirche", {"ende": "verloren"})
                return False
            continue
        g = ([_e(t, ab["ziel"])] if ab["art"] == "trupp" and _abstand(e, _e(t, ab["ziel"])) <= e["reichweite"] and _schussfrei(D, e, _e(t, ab["ziel"])) else []) or \
            [x for x in lebend(t, "blau") if _abstand(e, x) <= e["reichweite"] and _sichtbar(D, e, x) and _schussfrei(D, e, x)]
        e["naeher"] = not g and ab["art"] == "trupp"  # Haus im Weg: naechstes Mal bis dicht heran, statt ewig vor der Mauer zu stehen
        if not g:
            continue
        ziel = g[0]
        if ziel["id"] == "duc":
            verlust = _duc_verlust(z, D, e, ziel)
            _macht_plus(ziel, 8)
            z["lp"] = max(1 if t.get("art") == "manoever" else 0, kampf.lp(z) - verlust)
            log.append({"von": e["id"], "an": "duc", "schaden": verlust})
            _doppel_feind(z, D, t, e, ziel, log)
            if z["lp"] <= 0:
                _log(t, log)
                _szene(t, D, "verloren_duc", {"ende": "verloren"})
                return False
            continue
        if ziel["id"] == "wolff" and ziel.get("erstschlag") != t["runde"]:     # First Strike, einmal je Runde
            ziel["erstschlag"] = t["runde"]
            _treffer(t, ziel, e, schaden(ziel, e, D), log)
            if e.get("ko"):
                continue
        _treffer(t, e, ziel, schaden(e, ziel, D), log)
        _zurueck_schlagen(t, e, ziel, log, D)
        _doppel_feind(z, D, t, e, ziel, log)
    return True


def gegner_zug(z, moddir):
    """Alle Feinde ziehen und schlagen, danach wehrt sich die Buergerwehr, dann das Drehbuch der Runde."""
    t, D = _t(z), daten(moddir)
    log = []
    t["meldung"] = None
    if not _feinde_handeln(z, D, t, log):
        return
    for w in lebend(t, "blau"):
        if w["fest"]:
            g = [x for x in lebend(t, "schwarz") if _abstand(w, x) <= w["reichweite"] and _schussfrei(D, w, x)]
            if g:
                _treffer(t, w, g[0], schaden(w, g[0], D), log)
    _log(t, log)
    _anim(t, log)
    t["runde"] += 1
    t["phase"] = "spieler"
    _haeuser_brennen(D, t)
    _nachschub(D, t)
    _zug_frisch(z, t)
    if _welle(D, t).get("finale"):
        _drehbuch(z, D, t)
    else:
        _beats(z, D, t)
    _pruefen(z, D, t)


def _anim(t, zeilen):
    """Was der Bildschirm einmal abspielt: Wer hat wen wie hart getroffen."""
    t["anim_n"] = t.get("anim_n", 0) + 1
    t["anim"] = {"n": t["anim_n"], "log": zeilen}


def _log(t, zeilen):
    t["log"] = (t["log"] + zeilen)[-30:]
    t["letzter_zug"] = zeilen


def _bed_ok(z, t, bed):
    """Bedingung eines Beats: flag, nicht_flag, t (Wert im Kartenstand), nicht_t, einheit (steht noch auf der Karte)."""
    fl = z.get("flags", [])
    return (("flag" not in bed or bed["flag"] in fl) and ("nicht_flag" not in bed or bed["nicht_flag"] not in fl)
            and ("t" not in bed or bool(t.get(bed["t"]))) and ("nicht_t" not in bed or not t.get(bed["nicht_t"]))
            and ("einheit" not in bed or any(e["id"] == bed["einheit"] for e in lebend(t, "blau"))))


def _kette(t, D, sids, danach=None):
    """Mehrere Szenen hintereinander, danach weiter wie angegeben."""
    n = danach or {}
    for sid in reversed(sids[1:]):
        n = {"szene": sid, "dann": n}
    _szene(t, D, sids[0], n)


def _beats(z, D, t):
    """Das Drehbuch einer Welle (Duc 02.11.2026, drehbuch_finale.md): Beats je Runde, jede Szene einmal. Zuerst der Funk von letzter Nacht."""
    if t.get("art") != "echt" or t["phase"] != "spieler":
        return
    faellig = [t.pop("funk_offen")] if t.get("funk_offen") else []
    for b in _welle(D, t).get("beats", []):
        if t["runde"] >= b["runde"] and b["szene"] not in t["gesehen"] and b["szene"] not in faellig and _bed_ok(z, t, b.get("bed", {})):
            faellig.append(b["szene"])
    if faellig:
        _kette(t, D, faellig)


def _nacht_folgen(z, D, t):
    """Die Frau der letzten Nacht funkt in der ersten Welle des Tages, und Duc hat heute 10 % mehr Leben (Duc 02.11.2026). Stufe nach dem kleineren Wert."""
    n = z.get("nacht_bei") or {}
    pid = n.get("pid")
    if n.get("tag") != z.get("tag", 0) - 1 or pid not in D["funk"]:
        return
    if (z.get("lp_plus") or {}).get("tag") != z.get("tag"):
        voll = kampf.lp(z) >= kampf.lp_max_duc(z)
        z["lp_plus"] = {"tag": z.get("tag"), "faktor": D["funk_lp"]}
        if voll:
            kampf.lp_auffuellen(z)
    w = z.get("werte", {})
    stufe = min(w.get("vertrauen." + pid, 0), w.get("begehren." + pid, 0))
    i = 0 if stufe <= 2 else 1 if stufe == 3 else 2
    if D["funk_voraus"].get(pid) and D["funk_voraus"][pid] not in z.get("flags", []):
        i = 0
    t["funk_offen"] = "funk_%s_%d" % (pid, i + 1)


def _rudert(z, D, t):
    """Das Dorf rudert hinaus (Ruf). Ist Petrus Werkstatt aus Welle 3 heil, reicht ein Punkt weniger: Petru rudert mit dem Ruder seines Grossvaters (Duc 02.11.2026).
    Ist Petru am Mittag von Tag 22 mit Mina an jede Tuer gegangen (Auftrag Tueren, bl_tueren_petru), reicht noch ein Punkt weniger (Drehbuch Finale, Duc 04.11.2026)."""
    ruder = (t.get("haeuser") or {}).get(D["ruder_haus"], {}).get("status") in ("gerettet", "brennt")
    tueren = "bl_tueren_petru" in z.get("flags", [])
    return z.get("werte", {}).get("ruf", 0) >= D["ruf_rudert"] - (1 if ruder else 0) - (1 if tueren else 0)


def _nachtwache_stellen(z, D, t):
    """Wer Tag 22 nachts im Norden Wache hielt, steht in der letzten Welle schon neben Minicu am Tor (Drehbuch Tag 22 Abend)."""
    if not D["wellen"][min(t.get("welle_vorher", 0), len(D["wellen"]) - 1)].get("finale"):
        return
    for e in _im_einsatz(t):
        if e["id"] in D["nachtwache"]["wer"] and "bl_nachtwache_" + e["id"] in z.get("flags", []):
            e["x"], e["y"] = D["nachtwache"]["feld"]
            return


def _appell(t, D, danach):
    """Holm ruft alle auf (Drehbuch Abschnitt 7): Wer steht, antwortet, wer gefallen ist, bekommt Stille. Lola antwortet immer aus der Kombuese."""
    a = D["appell"]
    g = a.get("gefuehl", {})
    zeilen = [dict(_mit_zid({"wer": "Holm", "text": a["start"]}, "tk.ap.start", g.get("start")), ton="funk_rauschen")]
    for e in t["einheiten"]:
        if e["seite"] == "blau" and not e["fest"] and e["id"] in a["zeilen"]:
            if e.get("ko"):
                zeilen += [_mit_zid({"wer": "Holm", "text": e["name"] + "."}, "tk.ap.n." + e["id"], g.get("name")), {"wer": "", "text": a["stille"]}]
            else:
                zeilen.append(_mit_zid({"wer": e["name"], "text": a["zeilen"][e["id"]]}, "tk.ap." + e["id"], (g.get("zeilen") or {}).get(e["id"])))
    zeilen.append(_mit_zid({"wer": "Lola", "text": a["lola"]}, "tk.ap.lola", g.get("lola")))
    for pid in a["gefallen"]:
        e = next((e for e in t["einheiten"] if e["id"] == pid), None)
        if e and e.get("ko"):
            zeilen += [_mit_zid({"wer": "Holm", "text": e["name"] + "."}, "tk.ap.n." + pid, g.get("name")), {"wer": "", "text": a["stille"]}]
    zeilen.append(_mit_zid({"wer": "Holm", "text": a["ende"]}, "tk.ap.ende", g.get("ende")))
    for x in zeilen:
        x["pid"] = _sprecher(x["wer"]) if x["wer"] else None
    t["szene"] = zeilen
    t["nach_szene"] = danach
    t["phase"] = "szene"
    if "appell" not in t["gesehen"]:
        t["gesehen"].append("appell")


def _drehbuch(z, D, t):
    """Das Drama der letzten Welle (Duc 31.10.2026, 02.11.). Runde 2: Pascal versteckt sich, er kommt erst zu Minicus Sturz wieder. Runde 3: Alvas Trupp faellt. Runde 4: Mochi, Bibi nur nach der Versoehnung.
    Runde 5: Minicu faellt, danach ist White angreifbar. Frueher als zuvor, damit er auch faellt, wenn es an der Kirche eng wird."""
    r = t["runde"]
    if r >= 2 and "pascal_geht" not in t["gesehen"]:
        _e(t, "pascal").update(lp=0, ko=True)
        _szene(t, D, "pascal_geht", {"weiter": True})
        if "bl_nachtwache_niemand" in z.get("flags", []):   # Niemand hielt Wache (Drehbuch Tag 22 Abend)
            t["szene"] += [_mit_zid({"wer": x[0], "text": x[1]}, "tk.holm_ohne_wache.%d" % i) for i, x in enumerate(D["szenen"]["holm_ohne_wache"])]
    elif r >= 3 and "alva_faellt" not in t["gesehen"]:
        a = _e(t, "alva")
        a.update(lp=0, ko=True)
        _szene(t, D, "alva_faellt", {"weiter": True})
    elif r >= 4 and "mochi" not in t["gesehen"] and "mochi_allein" not in t["gesehen"] and "kl_loewe_frei" in z.get("flags", []):
        t["mochi_runde"] = r                         # White steht in diesem Gegnerzug still
        _szene(t, D, "mochi" if "rt_ausgang_alle" in z.get("flags", []) else "mochi_allein", {"weiter": True})
    elif r >= 5 and "minicu_faellt" not in t["gesehen"]:
        _e(t, "minicu").update(lp=0, ko=True)
        _szene(t, D, "minicu_faellt", {"weiter": True})
        m = D["nachtwache"]["feld"]
        if any(e["id"] in D["nachtwache"]["wer"] and abs(e["x"] - m[0]) + abs(e["y"] - m[1]) <= 2 and "bl_nachtwache_" + e["id"] in z.get("flags", []) for e in lebend(t, "blau")):
            t["szene"][1:1] = [_mit_zid({"wer": x[0], "text": x[1]}, "tk.minicu_nachtwache.%d" % i) for i, x in enumerate(D["szenen"]["minicu_nachtwache"])]
    if r >= 4 and "kevin_fliegt" not in t["gesehen"]:      # Kevin fliegt vom Tor (Drehbuch Runde 4). Er haengt sich an, was gerade laeuft, damit Minicu bei Runde 5 bleibt
        t["gesehen"].append("kevin_fliegt")
        if t["phase"] == "szene":
            t["szene"] += [_mit_zid(dict({"wer": x[0], "text": x[1]}, **(x[2] if len(x) > 2 else {})), "tk.kevin_fliegt.%d" % i) for i, x in enumerate(D["szenen"]["kevin_fliegt"])]
        else:
            _szene(t, D, "kevin_fliegt", {"weiter": True})


def runde_beenden(z, moddir):
    t = _t(z)
    if t["phase"] != "spieler":
        raise ValueError("Du bist gerade nicht dran.")
    gegner_zug(z, moddir)


def neustart_welle(z, moddir):
    """Niederlage: zurueck zum Beginn der Welle (Duc 31.10.2026). Mit nur einem Leben der Kirche waere das kaum zu schaffen, also nageln sie die Tuer wieder zu."""
    t = _t(z)
    if t["phase"] != "verloren" or not t.get("sicherung"):
        raise ValueError("Es gibt nichts neu zu starten.")
    s = t["sicherung"]
    neu = copy.deepcopy(s["t"])
    if neu.get("art") == "echt":
        s["t"]["kirche"] = neu["kirche"] = max(neu["kirche"], min(2, neu.get("kirche_max", 2)))
    neu["sicherung"] = s
    if neu.get("art") == "echt":                     # Jeder neue Versuch: 15 % schwaecher (Duc 02.11.2026), Mr. White und Pascal nicht
        D = daten(moddir)
        s["versuch"] = s.get("versuch", 0) + 1
        neu["milde"] = (1 - D["neustart_milde"]) ** min(s["versuch"], D["neustart_milde_max"])
        for e in lebend(neu, "schwarz"):
            if e["typ"] in D["feinde"]:
                _milde_anwenden(neu, e)
        q = D["briefing"].get(str(neu["welle"]))
        neu["meldung"] = "Holm: They paid for that too, so they come back weaker." + (" " + q["kurz"] if q else "")
    z["taktik"] = neu
    z["lp"] = s["lp"]
    z["status"] = "taktik"


def _sicht(z, D, t, e, aktiv_):
    v = {k: e.get(k) for k in ("id", "typ", "seite", "name", "x", "y", "lp", "lp_max", "reichweite", "art", "klasse", "boss", "fest", "gezogen", "fertig", "angriff", "abwehr", "bewegung", "figur", "rolle", "text", "kann", "nur_ziehen")}
    v["haelt"] = _haelt(t, e)
    v["macht"] = e.get("macht", 0)
    if e["seite"] == "blau" and e["id"] in D["macht"]:
        v["power"] = D["macht"][e["id"]]
    v["getarnt"] = _getarnt(D, e)
    if aktiv_ and e["seite"] == "blau" and not e["fest"] and not e["fertig"]:
        v["retten"] = [h["id"] for h in D["haeuser"] if t.get("haeuser", {}).get(h["id"], {}).get("status") == "brennt" and abs(e["x"] - h["x"]) + abs(e["y"] - h["y"]) <= 1]
        if e["id"] == "bibi":
            v["loeschen"] = [h["id"] for h in D["haeuser"] if t.get("haeuser", {}).get(h["id"], {}).get("status") == "brennt" and abs(e["x"] - h["x"]) + abs(e["y"] - h["y"]) <= e["reichweite"]]
    if aktiv_ and e["seite"] != "blau" and e["bewegung"]:
        v["gefahr"] = _gefahr(D, t, e)
    if aktiv_ and e["seite"] == "blau" and not e["fest"] and not e["fertig"]:
        if not e["gezogen"]:
            v["felder"] = [list(f) for f in erreichbar(D, t, e)]
        v["reich"] = reichweite_felder(D, e)
        v["ziele"] = []
        for g in ziele(t, e, D):
            if g.get("boss") and e["id"] != "duc":
                continue
            if e["id"] in SPIELER:
                h, mit = _doppel(z, D, t, e, g)
                v["ziele"].append({"id": g["id"], "echter_kampf": True, "mit": h["name"] if h else None})
                continue
            h, mit = _doppel(z, D, t, e, g)
            v["ziele"].append(dict(vorschau(e, g, D, mit), id=g["id"], mit=h["name"] if h else None, mit_schaden=mit))
    return v


def ansicht(z, moddir, modul=None):
    t, D = _t(z), daten(moddir)
    dran = t["phase"] == "spieler"
    einheiten = [_sicht(z, D, t, e, dran) for e in lebend(t)]
    absichten, spaeter = [], []
    if dran:
        for e in lebend(t, "schwarz") + lebend(t, "weiss"):
            if _haelt(t, e):
                continue
            ab = _absicht(D, t, e)
            if ab.get("feld") and e["bewegung"] and ab["art"] not in ("halten", "yacht"):
                if "sophia" in t["hilfe"]:             # Sophia: wo der Feind in zwei Runden steht
                    r = 0 if ab["art"] == "kirche" else e["reichweite"]
                    dort = _zum_ziel(D, t, e, ab["feld"], r)
                    dort = _zum_ziel(D, t, dict(e, x=dort[0], y=dort[1]), ab["feld"], r)
                    spaeter.append({"von": e["id"], "x": dort[0], "y": dort[1]})
    if dran:
        absichten = _plan(z, D, t)
    hilfe = [{"id": hid, "name": q["name"], "kann": q["kann"], "text": q["text"], "pid": q.get("pid", hid), "set": D.get("sets", {}).get(q.get("pid", hid)), "fest": bool(q.get("fest")), "takt": q["takt"], "gewaehlt": hid in t["hilfe"],
              "bereit": _hilfe_bereit(D, t, hid), "nutzlos": _hilfe_nutzen(D, t, hid), "ziele": _hilfe_ziele(z, D, t, hid) if dran and hid in t["hilfe"] else []}
             for hid, q in D["hilfe"].items() if _hilfe_frei(z, D, hid)]
    d = next((e for e in t["einheiten"] if e["id"] == "duc"), None)
    waffen = kampf.daten(moddir)                         # Das Sprite zeigt immer den Saebel, das Symbol die angelegte Waffe (Duc 01.11.2026)
    wid = kampf.aktive_waffe(z, waffen)
    karten = []
    for tid, q in list(D["trupps"].items()) + [(r, q) for r, q in D["reserve"].items() if _reserve_frei(z, D, r)] + list(D["wehr"].items()):
        karten.append({"id": tid, "rolle": q.get("rolle"), "reserve": tid in D["reserve"], "im_einsatz": any(e["id"] == tid for e in t["einheiten"]), "name": q["name"], "text": q["text"], "art": q.get("art"), "kann": q.get("kann"), "lp": q.get("lp"), "angriff": q.get("angriff"), "abwehr": q.get("abwehr"),
                       "bewegung": q.get("bewegung"), "reichweite": q.get("reichweite", 1), "fest": tid in D["wehr"],
                       "set": q["figur_flag"]["set"] if q.get("figur_flag", {}).get("flag") in z.get("flags", []) else D.get("sets", {}).get(tid)})
    aus = {"art": t.get("art"), "vorbereitung": t.get("vorbereitung"), "phase": t["phase"], "welle": t["welle"], "wellen": 1 if t.get("art") == "manoever" else len(D["wellen"]), "runde": t["runde"], "kirche": t["kirche"], "kirche_max": t.get("kirche_max", D["kirche"]["lp"]), "spalten": D["spalten"], "zeilen": D["zeilen"], "ausschnitt": _ausschnitt(D, t),
            "einheiten": einheiten, "absichten": absichten, "spaeter": spaeter, "hilfe": hilfe, "hilfe_plaetze": HILFE_PLAETZE, "meldung": t.get("meldung"), "szene": t["szene"][0] if t["szene"] else None, "szene_rest": max(0, len(t["szene"]) - 1), "karten": karten,
            "gehandelt": bool(t.get("gehandelt")), "rethink_frei": _rethink_frei(t), "anim": t.get("anim"), "yacht": t.get("yacht", 0), "yacht_max": D["yacht_lp"], "cutin": t.get("cutin"), "rueckspruenge": t.get("rueckspruenge", 0), "plaetze": _plaetze(D, t), "trupps_max": _trupps_max(D, t), "white_frei": white_frei(t),
            "haeuser": [dict(h, **t["haeuser"][h["id"]]) for h in D["haeuser"] if h["id"] in t.get("haeuser", {})],
            "ankunft": [{"x": p[0], "y": p[1], "in": n["runde"] - t["runde"], "typ": ty} for n in _nachschub_offen(D, t) for ty, p in n["feinde"]],
            "raster": D["raster"], "gelaende": D["gelaende"], "tueren": D["kirche"]["tueren"], "barrikade": D["barrikade"] if t["barrikade"] else [], "kampfszene": t.get("kampfszene"), "letzter_zug": t.get("letzter_zug") or [],
            "barrikaden": _barrikaden(D, t), "barrikade_bild": _barrikade_bild(moddir, D, t), "bild": D["bilder"]["kampf" if t["welle"] >= 1 or t.get("art") == "echt" else "ruhig"], "duc_lp": kampf.lp(z), "duc_lp_max": kampf.lp_max_duc(z), "duc_steht": bool(d and not d.get("ko")), "duc_waffe": {"id": wid, "name": waffen["weapons"].get(wid, {}).get("label", wid)},
            "kampf_gegen": t.get("kampf_gegen")}
    aus["feind_start"] = _vorschau_feinde(z, D, t)
    if t.get("briefing"):                                # Fuer den Client ist das Briefing eine Szene, die Aufstellung kommt danach
        aus.update(phase="szene", szene=t["briefing"][0], szene_rest=len(t["briefing"]) - 1, szene_id="welle_%d" % (t.get("welle_vorher", 0) + 1))
    elif t["szene"]:                                     # Welche Szene laeuft: der Client spielt dazu den Ton
        zeile = [t["szene"][0]["wer"], t["szene"][0]["text"]]
        aus["szene_id"] = next((sid for sid in reversed(t["gesehen"]) if zeile in [list(x)[:2] for x in D["szenen"].get(sid, [])]), None)
    if aus["szene"]:
        pid = _sprecher(aus["szene"].get("wer", ""))
        aus["szene"] = dict(aus["szene"], pid=pid, set=D.get("sets", {}).get(pid))   # Belagerungs-Outfit (Holm im Hemd, 03.11.2026)
    if t["phase"] == "bestand":
        aus["bestand"] = belagerung.ansicht(z, D, modul, bool(t.get("flicken")))
    return aus


def _barrikade_bild(moddir, D, t):
    """Die Barrikade im Norden als Bild auf der Karte (Duc 02.11.2026): zu bis zum Verrat, danach zur Seite geschoben. Ohne Bild bleibt das rote Feld."""
    q = D.get("barrikade_bild")
    datei = q and q["zu" if t["barrikade"] else "offen"]
    if not datei or not os.path.isfile(os.path.join(moddir, "taktik", datei)):
        return None
    return {"box": q["box"], "datei": datei}


def _barrikaden(D, t):
    """Wo sie stehen und ob sie halten, nur an den echten Tagen."""
    if t.get("art") not in ("echt", "bestand"):
        return []
    return [{"front": f, "x": q["feld"][0], "y": q["feld"][1], "name": q["name"], "kaputt": f in t.get("kaputt", [])} for f, q in D["bestand"]["barrikaden"].items()]
