# -*- coding: utf-8 -*-
"""Lob fuer Attributsteigerungen (Duc 27.10.2026, Skyrim-Prinzip: "Du hast aber starke Arme bekommen").

Regel der Engine: der CODE entscheidet und bucht, die Zeilen sind fest geschrieben (module\\<modul>\\lob.json, Builder
werkzeuge\\eden_rise\\lob_eden_rise.py) und tragen Chatterbox-Turbo-Tags in stimme_tags.json - das Modell schreibt hier nichts.
  * Vormerken: bringt Duc ein Attribut auf 3, 4 oder 5 (kampf.attribut_steigern), merkt sich das Spiel einen Kommentar.
    Pro Attribut gilt nur der hoechste offene Wert (mehrere Punkte auf einmal werden gebuendelt).
  * Ausspielen in einer freien Szene (szene.starten): sagt eine anwesende Figur, die dieses Attribut schaetzt
    (personen.<id>.schaetzt), ihren Satz ein einziges Mal direkt nach der Eroeffnung. Wer am laengsten nichts gesagt hat,
    kommt zuerst; dann entscheidet ein Seed.
  * Fallback: wartet ein Kommentar seit WARTE_PHASEN Phasen, kommt er als Handy-Nachricht (Figur ohne ST-Karte: nur lesen).
  * Hoechstens ein Kommentar je Phase, jeder Meilenstein wird genau einmal gesagt. Events mit festem Text sind aussen vor."""
import json, os, random

MEILENSTEINE = (3, 4, 5)
WARTE_PHASEN = 2
PHASEN = ("fruehstueck", "tag", "nachmittag", "dinner", "abend", "nacht")
_CACHE = {}


def daten(modul):
    """module\\<modul>\\lob.json (nach Aenderungszeit zwischengespeichert); ohne Datei: leer."""
    pfad = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "module", modul.get("id", ""), "lob.json")
    try:
        mt = os.path.getmtime(pfad)
    except OSError:
        return {}
    c = _CACHE.get(pfad)
    if c and c[0] == mt:
        return c[1]
    try:
        d = json.load(open(pfad, encoding="utf-8")).get("zeilen", {})
    except (OSError, ValueError):
        d = {}
    _CACHE[pfad] = (mt, d)
    return d


def _jetzt(z):
    """Laufende Nummer der Phase (Tag * 10 + Position), damit 'seit N Phasen' und 'am laengsten still' rechenbar sind."""
    return z["tag"] * 10 + (PHASEN.index(z["phase"]) if z.get("phase") in PHASEN else 0)


def _stand(z):
    return z.setdefault("lob", {"offen": {}, "gesagt": [], "zuletzt": {}, "phase": None})


def zeile(modul, pid, att, wert):
    return ((daten(modul).get(pid) or {}).get(att) or {}).get(str(wert))


def vormerken(z, att, wert):
    """Duc hat `att` auf `wert` gebracht (kampf.attribut_steigern). Nur Meilensteine zaehlen."""
    if wert not in MEILENSTEINE:
        return
    s = _stand(z)
    alt = s["offen"].get(att)
    if not alt or wert > alt["wert"]:
        s["offen"][att] = {"wert": wert, "seit": _jetzt(z)}


def _optionen(z, modul, pids):
    """[(att, wert, pid)] - wer von `pids` einen offenen Kommentar hat und ihn noch nicht gesagt hat."""
    s = _stand(z)
    out = []
    for att, o in sorted(s["offen"].items()):
        for pid in pids:
            schaetzt = (modul["personen"].get(pid) or {}).get("schaetzt") or []
            if att in schaetzt and zeile(modul, pid, att, o["wert"]) and "%s.%s.%d" % (pid, att, o["wert"]) not in s["gesagt"]:
                out.append((att, o["wert"], pid))
    return out


def _waehlen(z, modul, optionen, salz):
    s = _stand(z)
    rng = random.Random("%s-%d-%s-%s" % (z["id"], z["tag"], z.get("phase"), salz))
    att, wert, pid = min(optionen, key=lambda o: (s["zuletzt"].get(o[2], -1), rng.random()))
    return {"pid": pid, "att": att, "wert": wert, "text": zeile(modul, pid, att, wert)}


def _frei(z):
    return _stand(z)["phase"] != [z["tag"], z.get("phase")]


def _nichts_offen(z):
    """Lesende Vorpruefung: ohne Vormerkung entsteht gar kein z["lob"] (der Spielstand bleibt, wie er war)."""
    return not (z.get("lob") or {}).get("offen")


def waehlen(z, modul, anwesend):
    """Szenenstart: -> {"pid", "att", "wert", "text"} oder None. Danach gebucht() aufrufen."""
    if _nichts_offen(z) or not _frei(z):
        return None
    opt = _optionen(z, modul, anwesend)
    return _waehlen(z, modul, opt, "szene") if opt else None


def gebucht(z, wahl):
    """Der Kommentar ist gesagt: Meilenstein verbraucht, Phase belegt, Figur merkt sich, wann sie zuletzt sprach."""
    s = _stand(z)
    s["gesagt"].append("%s.%s.%d" % (wahl["pid"], wahl["att"], wahl["wert"]))
    s["offen"].pop(wahl["att"], None)
    s["zuletzt"][wahl["pid"]] = _jetzt(z)
    s["phase"] = [z["tag"], z.get("phase")]


def handy_faellig(z, modul):
    """Phasenbeginn: wartet ein Kommentar seit WARTE_PHASEN Phasen, schreibt ihn eine passende Figur aufs Handy.
    -> Meldungszeilen (leer, wenn nichts faellig)."""
    if _nichts_offen(z):
        return []
    from . import chronik, handy
    s = _stand(z)
    if not _frei(z):
        return []
    faellig = [a for a, o in s["offen"].items() if _jetzt(z) - o["seit"] >= WARTE_PHASEN]
    if not faellig:
        return []
    opt = [o for o in _optionen(z, modul, list(modul["personen"])) if o[0] in faellig]
    if not opt:
        return []
    wahl = _waehlen(z, modul, opt, "handy")
    pid = wahl["pid"]
    f = handy.faden_von(z, pid)
    f["tag"], f["phase"], f["gelesen"], f["chips"] = z["tag"], z["phase"], False, []
    f["verlauf"].append(handy._zeile(z, pid, wahl["text"]))
    chronik.eintragen(z, modul, "handy", "%s texted Duc: \"%s\"" % (modul["personen"][pid]["name"].split()[0], wahl["text"]),
                      wer=[pid], dabei=[], wichtig=1, ort="handy")
    gebucht(z, wahl)
    return ["📱 Message from %s" % modul["personen"][pid]["name"].split()[0]]
