# -*- coding: utf-8 -*-
"""Tagesplan des Showrunners: laden, pruefen, Phasen ablaufen lassen, Tagesende.

Ein Plan liegt als module\\<modul>\\plaene\\tag<N>.json (Showrunner im Chat) - spaeter liefert ihn die Claude-API.
Pruefen = Fehler (Plan darf so nicht gespielt werden) und Warnungen (spielbar, aber pruefenswert).
Anwesende duerfen Platzhalter enthalten: "$abend" = dieselben Figuren wie die heute gewaehlte Abend-Szene."""
import json, os

from . import regeln, zustand


def texte(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from texte(v)
    elif isinstance(o, list):
        for v in o:
            yield from texte(v)


def werte_namen(modul):
    ok = set()
    for name, w in modul["werte"].items():
        for x in w.get("je", []) + w.get("paare", []):
            ok.add("%s.%s" % (name, x))
        if not w.get("je") and not w.get("paare"):
            ok.add(name)
    return ok


def pruefe(plan, modul, z):
    fehler, warn = [], []
    zr = modul["zeitraster"]
    wahrheit = modul["wahrheit"]["vorrat"][z["wahrheit"]]
    werte_ok = werte_namen(modul)
    if plan.get("tag") != z["tag"]:
        fehler.append("Plan ist fuer Tag %s, Spielstand steht auf Tag %d" % (plan.get("tag"), z["tag"]))
    for ph in zr["phasen"]:
        if ph not in plan.get("phasen", {}) and not plan.get("_hauptstory"):   # Hauptstory: Tag 1 beginnt am Abend
            fehler.append("Phase fehlt: " + ph)
    for ph, inhalt in plan.get("phasen", {}).items():
        szenen = inhalt.get("szenen", [])
        if inhalt.get("dynamisch") and not szenen:
            continue        # wird erst beim Betreten gefuellt (showrunner.phase_fuellen) und dann geprueft
        # "fest": eine Wahl-Phase mit genau einer Szene (Tag 1: Dinner = Strom-Rat, seit Dinner Wahl ist, 17.10.2026)
        # "folge": Hauptstory spielt alle Szenen der Phase nacheinander (kern/hauptstory.py, 17.10.2026)
        wahl_n = len([s for s in szenen if s.get("id") not in (inhalt.get("vorspiel") or [])])   # Modell B: ohne Vorspiel
        if ph in zr["wahl"] and not 2 <= wahl_n <= 3 and not inhalt.get("dynamisch") and not inhalt.get("folge")                 and not (inhalt.get("fest") and len(szenen) == 1):
            fehler.append("%s: Wahl-Phase braucht 2-3 Optionen, hat %d" % (ph, wahl_n))
        if ph in zr["pflicht"] and not szenen:
            fehler.append("%s: Pflicht-Phase ohne Szene" % ph)
        for s in szenen:
            sid = "%s/%s" % (ph, s.get("id", "?"))
            anwesend = [p for p in s.get("anwesend", []) if not p.startswith("$")]
            kontext = {"anwesend": anwesend, "phase": ph}
            raum = modul["raeume"].get(s.get("ort"))
            if not raum:
                fehler.append("%s: unbekannter Raum %r" % (sid, s.get("ort")))
            else:
                status, weg = regeln.zugang(raum, z, kontext)
                if status == "gesperrt":
                    fehler.append("%s: Raum %s ist gesperrt" % (sid, s["ort"]))
                elif status == "wurf":
                    warn.append("%s: Raum %s nur mit Wurf %s erreichbar" % (sid, s["ort"], weg["wurf"]))
            for p in anwesend:
                if p not in modul["personen"]:
                    fehler.append("%s: unbekannte Person %r" % (sid, p))
                    continue
                ablauf = modul["personen"][p].get("ablauf", {})
                normal = ablauf.get(ph, ablauf.get(regeln.phase_wie(ph), ablauf.get("*")))
                if normal and normal != s.get("ort") and not s.get("begruendung_ort"):
                    warn.append("%s: %s ist laut Tagesablauf in %s, nicht in %s" % (sid, p, normal, s.get("ort")))
            for p in s.get("anwesend", []):
                if p.startswith("$") and p[1:] not in zr["phasen"]:
                    fehler.append("%s: Platzhalter %s verweist auf keine Phase" % (sid, p))
            for p, f in (s.get("figuren") or {}).items():
                if p not in anwesend and p != "*":
                    fehler.append("%s: Figurenauftrag fuer %s, die nicht anwesend ist" % (sid, p))
                if modul["personen"].get(p, {}).get("romanzierbar"):
                    for k in ("will", "verbirgt", "grenze"):
                        if not f.get(k):
                            fehler.append("%s: %s ohne %r" % (sid, p, k))
            st = s.get("storylet")
            if st:
                d = modul["storylets"].get(st)
                if not d:
                    fehler.append("%s: unbekanntes Storylet %r" % (sid, st))
                else:
                    if d["phase"] != ph:
                        fehler.append("%s: Storylet %s gehoert in Phase %s" % (sid, st, d["phase"]))
                    if not regeln.gilt(d.get("bedingung"), z, kontext):
                        fehler.append("%s: Bedingung von %s nicht erfuellt: %s" % (sid, st, d.get("bedingung")))
                    if st in z.get("gesehene_storylets", []):
                        warn.append("%s: Storylet %s schon gesehen" % (sid, st))
            elif not s.get("improvisiert"):
                fehler.append("%s: weder Storylet noch als improvisiert markiert" % sid)
            ev = s.get("ereignis")
            if ev and ev.get("id"):
                e = modul["ereignisse"].get(ev["id"])
                if not e:
                    fehler.append("%s: unbekanntes Ereignis %r" % (sid, ev["id"]))
                elif not regeln.gilt(e.get("bedingung"), z, kontext):
                    fehler.append("%s: Ereignis %s - Bedingung nicht erfuellt" % (sid, ev["id"]))
            for a in s.get("ausgaenge", []):
                fehler += folgen_pruefen(sid, a.get("folgen", []), modul, werte_ok)
            wm = s.get("wahlmoment")
            if wm:
                if not 2 <= len(wm.get("optionen", [])) <= 4:
                    fehler.append("%s: Wahlmoment braucht 2-4 Optionen" % sid)
                for o in wm.get("optionen", []):
                    fehler += folgen_pruefen(sid, o.get("folgen", []) + o.get("folgen_fehlschlag", []), modul, werte_ok)
                    if o.get("check") and o["check"][0] not in modul["attribute"]:
                        fehler.append("%s: Wahlmoment-Probe mit unbekanntem Attribut %r" % (sid, o["check"][0]))
            alles = " ".join(texte(s)).lower()
            if z["tag"] < wahrheit["enthuellung_ab_tag"]:
                for wort in wahrheit.get("verrat_woerter", []):
                    if wort.lower() in alles:
                        fehler.append("%s: verraet die Wahrheit vor Tag %d (%r)" % (sid, wahrheit["enthuellung_ab_tag"], wort))
            if s.get("hinweis_wahrheit") and s["hinweis_wahrheit"] not in wahrheit["hinweise"]:
                warn.append("%s: Hinweis %r steht nicht im Hinweis-Vorrat" % (sid, s["hinweis_wahrheit"]))
    for e in plan.get("tagesende", []):
        fehler += folgen_pruefen("tagesende", [e], modul, werte_ok)
    for fx in modul.get("fixpunkte", []):
        if fx["tag"] == z["tag"] and not plan.get("phasen", {}).get(fx["phase"], {}).get("dynamisch"):
            titel = " ".join(s.get("titel", "") for s in plan.get("phasen", {}).get(fx["phase"], {}).get("szenen", []))
            if fx["titel"].lower() not in titel.lower():
                fehler.append("Fixpunkt heute fehlt: %s (%s)" % (fx["titel"], fx["phase"]))
    return fehler, warn


def folgen_pruefen(sid, folgen, modul, werte_ok):
    fehler = []
    for f in folgen:
        if "wert" in f:
            if f["wert"] not in werte_ok:
                fehler.append("%s: unbekannter Wert %r" % (sid, f["wert"]))
            if abs(f.get("delta", 0)) > 2:
                fehler.append("%s: Aenderung %s um %s zu gross (max. 2)" % (sid, f["wert"], f["delta"]))
        if "uhr" in f and f["uhr"] not in modul["uhren"]:
            fehler.append("%s: unbekannte Uhr %r" % (sid, f["uhr"]))
        if "item" in f and f["item"] not in modul["items"]:
            fehler.append("%s: unbekannter Gegenstand %r" % (sid, f["item"]))
    return fehler


def plan_laden(z, modul, moddir):
    """Handgeschriebener Plan (plaene/tag<N>.json) hat Vorrang; sonst baut ihn der automatische Showrunner
    aus dem Szenen-Vorrat (szenen.json) - so ist das Spiel ohne Menschen/Cloud spielbar (16.10.2026)."""
    pfad = os.path.join(moddir, "plaene", "tag%d.json" % z["tag"])
    from . import hauptstory
    if hauptstory.aktiv(moddir):                      # Modul mit Hauptstory (eden_rise): Wochenbogen statt Vorrat
        plan = hauptstory.plan_bauen(z, modul, moddir)
    elif os.path.exists(pfad):
        plan = json.load(open(pfad, encoding="utf-8"))
    else:
        from . import showrunner
        plan = showrunner.plan_bauen(z, modul, moddir)
        if plan is None:
            z["status"], z["plan_fehler"] = "warte_auf_plan", ["Noch kein Plan fuer Tag %d (%s)" % (z["tag"], pfad)]
            return False
    fehler, warn = pruefe(plan, modul, z)
    if fehler:
        z["status"], z["plan_fehler"] = "plan_fehler", fehler + ["(Warnung) " + w for w in warn]
        return False
    z["plan"], z["plan_fehler"] = plan, ["(Warnung) " + w for w in warn]
    z["phase"] = plan.get("erste_phase") or modul["zeitraster"]["phasen"][0]
    z["heute"] = []
    return True


def szenen_der_phase(z):
    return (z["plan"]["phasen"].get(z["phase"]) or {}).get("szenen", [])


def naechste_folge(z):
    """Folge-Phase (Hauptstory): naechste noch nicht gespielte Szene, deren Bedingung jetzt gilt - oder None."""
    inhalt = z["plan"]["phasen"].get(z["phase"]) or {}
    if not inhalt.get("folge"):
        return None
    gespielt = {h.get("szene") for h in z["heute"] if h.get("phase") == z["phase"]}
    for s in inhalt["szenen"]:
        if s["id"] not in gespielt and (not s.get("bedingung") or regeln.gilt(s["bedingung"], z)):
            return s["id"]
    return None


def szene_nach_id(z, sid):
    for s in szenen_der_phase(z):
        if s["id"] == sid:
            return s
    raise KeyError(sid)


MAX_FIGUREN = 3        # 17.10.2026 (Duc): hoechstens 3 Figuren in einer Szene (Duc zaehlt nicht mit)


def _kappen(z, out, modul):
    """Mehr als MAX_FIGUREN: die Frau mit der kleinsten Summe aus Vertrauen+Begehren faellt weg (bei Gleichstand die
    zuletzt genannte). Nebenfiguren (Yasin, Elsa, Petru ...) bleiben, solange noch eine Frau zum Streichen da ist -
    sie tragen meist die Szene."""
    out = list(out)
    while len(out) > MAX_FIGUREN:
        frauen = [p for p in out if modul and modul["personen"].get(p, {}).get("romanzierbar")]
        kand = frauen or out
        weg = min(reversed(kand), key=lambda p: z["werte"].get("vertrauen." + p, 0) + z["werte"].get("begehren." + p, 0))
        out.remove(weg)
    return out


def anwesende(z, s, modul=None):
    """Platzhalter aufloesen: "$abend" -> Figuren der heute gewaehlten Abend-Szene. Hoechstens MAX_FIGUREN."""
    out = []
    for p in s.get("anwesend", []):
        if p.startswith("$"):
            for h in z["heute"]:
                if h["phase"] == p[1:]:
                    out += [x for x in h["anwesend"] if x not in out and (not modul or modul["personen"].get(x, {}).get("romanzierbar"))]
        elif p not in out:
            out.append(p)
    return _kappen(z, out, modul)


# Modell B (24.10.2026): Eine freie Phase hat 2 Aktionen. Ermittlung ausserhalb von Szenen und ein Anruf kosten 1,
# eine Szene ("Zeit mit ...") braucht die ganze Phase. Kochen, Training, Truhe und Auftraege kosten keine Aktion.
AKTIONEN_PRO_PHASE = 2


def aktionen(z):
    """Heute in dieser Phase schon verbrauchte Aktionen."""
    a = z.get("aktionen") or {}
    return a.get("n", 0) if (a.get("tag"), a.get("phase")) == (z["tag"], z["phase"]) else 0


def aktion_verbrauchen(z, n=1):
    """-> True, wenn danach noch eine Aktion in dieser Phase uebrig ist (die Phase geht weiter)."""
    genutzt = aktionen(z) + n
    z["aktionen"] = {"tag": z["tag"], "phase": z["phase"], "n": genutzt}
    return genutzt < AKTIONEN_PRO_PHASE


def _vorspiel_offen(z):
    """Modell B: Phase mit Vorspiel (Uebergangs-Szenen), in der noch keine freie Szene gespielt wurde?"""
    inhalt = z["plan"]["phasen"].get(z["phase"]) or {}
    vor = inhalt.get("vorspiel") or []
    if not vor:
        return False
    frei = [s["id"] for s in inhalt.get("szenen", []) if s["id"] not in vor]
    gespielt = {h.get("szene") for h in z["heute"] if h.get("phase") == z["phase"]}
    return bool(frei) and not (gespielt - set(vor))


def naechste_phase(z, modul):
    """Nach einer Szene: naechste Phase oder Tagesende. Liefert 'wahl', 'szene:<id>', 'tagesende'."""
    nxt = naechste_folge(z)
    if nxt:                                           # Folge-Phase: erst die restlichen Szenen dieser Phase
        return "szene:" + nxt
    if _vorspiel_offen(z):                            # nach dem Vorspiel: dieselbe Phase, jetzt frei
        return phase_beginnen(z)
    from . import showrunner as _showrunner
    _showrunner.verabredung_versetzt(z, modul)
    if (z.get("plan") or {}).get("_hauptstory"):      # Phasenende in der Hauptstory (B4): Gegenwehr, Warnzeichen ...
        from . import ermittlung
        sichtbar = ermittlung.phase_ende(z, modul)
        if sichtbar:
            z["meldungen"].append({"titel": "In the night" if z["phase"] == "nacht" else "Meanwhile", "kurz": "",
                                   "folgen": sichtbar})
    phasen = modul["zeitraster"]["phasen"]
    i = phasen.index(z["phase"])
    if i + 1 >= len(phasen):
        return "tagesende"
    z["phase"] = phasen[i + 1]
    z.pop("lp", None)                                 # Modell B: jede neue Phase fuellt Lebenspunkte auf (kampf.lp)
    inhalt = z["plan"]["phasen"].get(z["phase"], {})
    if z["phase"] in modul["zeitraster"]["wahl"] and z.get("verabredungen"):
        from . import showrunner
        showrunner.verabredung_einbauen(z, modul, z["phase"], inhalt)
    if inhalt.get("dynamisch") and not inhalt.get("szenen"):
        from . import showrunner
        showrunner.phase_fuellen(z, modul, z["phase"])
        fehler, _ = pruefe(z["plan"], modul, z)
        # nur die gerade gefuellte Phase zaehlt - frueh am Tag gespielte Szenen duerfen inzwischen "veraltet" sein
        fehler = [f for f in fehler if f.startswith((z["phase"] + "/", z["phase"] + ":"))]
        if fehler:
            z.setdefault("plan_fehler", []).extend("(Phase %s) %s" % (z["phase"], f) for f in fehler)
    return phase_beginnen(z)


def phase_beginnen(z):
    """-> 'szene:<id>', 'wahl' oder 'leer' (Phase ohne spielbare Szene: der Aufrufer geht zur naechsten)."""
    inhalt = z["plan"]["phasen"].get(z["phase"]) or {}
    if inhalt.get("folge"):
        nxt = naechste_folge(z)
        return "szene:" + nxt if nxt else "leer"
    if inhalt.get("vorspiel"):                        # Modell B: Uebergaenge zuerst, dann die freie Wahl
        gespielt = {h.get("szene") for h in z["heute"] if h.get("phase") == z["phase"]}
        for sid in inhalt["vorspiel"]:
            if sid not in gespielt:
                return "szene:" + sid
        szenen = [s for s in szenen_der_phase(z) if s["id"] not in inhalt["vorspiel"]]
        if not szenen:
            return "leer"
        if len(szenen) == 1 and not aktionen(z):      # nach einer Aktion: Wahl zeigen statt Szene starten
            return "szene:" + szenen[0]["id"]
        z["status"], z["optionen"] = "wahl", [s["id"] for s in szenen]
        return "wahl"
    szenen = szenen_der_phase(z)
    if not szenen:
        return "leer"
    if len(szenen) == 1 and not aktionen(z):          # nach einer Aktion: Wahl zeigen statt Szene starten
        return "szene:" + szenen[0]["id"]
    z["status"], z["optionen"] = "wahl", [s["id"] for s in szenen]
    return "wahl"


def tagesende(z, modul):
    zeilen = []
    for e in (z["plan"] or {}).get("tagesende", []):
        if regeln.gilt(e.get("wenn"), z):
            zeilen += zustand.folgen_anwenden(z, modul, [e])
    z["verlauf"] += [dict(h, tag=z["tag"]) for h in z["heute"]]
    z["tag"] += 1
    z.pop("lp", None)                                 # neuer Tag = neue Phase: Lebenspunkte voll (Modell B)
    z["plan"], z["optionen"], z["szene"] = None, [], None
    grenze = modul.get("probefahrt_tage") or modul["zeitraster"]["tage"]
    z["status"] = "ende" if z["tag"] > grenze else "warte_auf_plan"
    return zeilen
