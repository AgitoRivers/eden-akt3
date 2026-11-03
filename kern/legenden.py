# -*- coding: utf-8 -*-
"""Das Dorf, das redet (Duc 30.10.2026, Brain Trust zu Mundi, Option B).

Eine grosse Tat (Missions-Flag, z. B. sirene_fertig) wird ueber Nacht zur Legende. Sie waechst in drei Stufen:
  Stufe 0 (ab dem Morgen danach): was wirklich geschah, wer dabei war erzaehlt es
  Stufe 1 (2 Tage nach der Tat):  uebertrieben - das Dorf hat nachgelegt
  Stufe 2 (4 Tage nach der Tat):       voellig verdreht - und Duc hoert die Fassung, die keiner mehr korrigieren kann
Die Saetze stehen fest im Builder (werkzeuge/eden_rise/ereignisse_legenden.py -> legenden.json), das Modell erfindet
nichts dazu (Spoilerschutz). Duc hoert sie an drei Stellen:
  - "zeit":  erste Zeile, wenn er Zeit mit der Figur verbringt (in ihr Gedaechtnis gewoben, das Modell spinnt weiter)
  - "laden": Begruessung beim Betreten ihres Ladens (statt des normalen Grusses)
  - Handy:   eine Figur fragt nach ("Is it true…?") - gewoehnliche Handy-Events mit Bedingung flag_seit leg_<tat>
Jede Zeile hoert Duc einmal; je Figur hoechstens eine Legenden-Zeile am Tag.

Ruf im Dorf: eine gute Legende gibt beim Wachsen auf Stufe 1 und 2 je Ruf +1. Bewegt sich der Ruf 4 Tage nicht, sinkt
er alle 2 Tage um 1 - wer im Dorf nichts tut, wird wieder unbekannt (wie in Mundi, dort nach 7 Tagen).
"""
import json
import os

from . import regeln

STUFE_TAGE = (1, 2, 4)            # Tage nach der Tat, ab denen Stufe 0 / 1 / 2 gilt (Kalender endet noch an Tag 14)
RUF_RUHE, RUF_TAKT = 4, 2         # Verblassen: nach 4 ruhigen Tagen alle 2 Tage -1
RUF_WORTE = ["a stranger", "barely known", "known", "respected", "well liked", "a legend"]

_CACHE = {}


def daten(moddir):
    pfad = os.path.join(moddir, "legenden.json")
    if not os.path.exists(pfad):
        return {"taten": {}, "zeilen": {}, "familie": []}
    mt = os.path.getmtime(pfad)
    if _CACHE.get(pfad, (None,))[0] != mt:
        _CACHE[pfad] = (mt, json.load(open(pfad, encoding="utf-8")))
    return _CACHE[pfad][1]


def flag(tat):
    return "leg_" + tat


def stufe(z, tat):
    """Aktuelle Stufe der Legende (0-2) oder None, solange sie noch nicht die Runde macht."""
    ab = (z.get("flag_tag") or {}).get(flag(tat))
    if ab is None or flag(tat) not in z["flags"]:
        return None
    seit = z["tag"] - ab
    st = None
    for i, t in enumerate(STUFE_TAGE):
        if seit >= t:
            st = i
    return st


def gehoert(z):
    return z.setdefault("legenden_gehoert", [])


def zeile_fuer(z, moddir, pid, wo):
    """Die naechste ungehoerte Legenden-Zeile dieser Figur fuer diesen Einstieg ("zeit"/"laden") - oder None.
    Bevorzugt die hoechste erreichte Stufe und die frischeste Tat; je Figur hoechstens eine am Tag."""
    tage = z.setdefault("legenden_tag", {})
    if tage.get(pid) == z["tag"]:
        return None
    d, schon = daten(moddir), set(gehoert(z))
    kand = []
    for zid, l in d["zeilen"].items():
        if l["wer"] != pid or l["wo"] != wo or zid in schon or not regeln.gilt(l.get("wenn"), z):
            continue
        st = stufe(z, l["tat"])
        if st is None or l["stufe"] > st:
            continue
        kand.append((l["stufe"], z["flag_tag"][flag(l["tat"])], zid))
    if not kand:
        return None
    _, _, zid = max(kand)
    return dict(d["zeilen"][zid], id=zid)


def markieren(z, zl):
    gehoert(z).append(zl["id"])
    z.setdefault("legenden_tag", {})[zl["wer"]] = z["tag"]


def tagesende(z, modul, moddir, folgen_anwenden):
    """Nach Tagesende (z["tag"] ist schon der neue Tag): neue Taten werden Legenden, gewachsene geben Ruf, stiller Ruf
    verblasst. -> Zeilen fuer die Tagesmeldung."""
    d, zeilen = daten(moddir), []
    for tid, t in d["taten"].items():
        f = flag(tid)
        if t["flag"] in z["flags"] and f not in z["flags"]:
            z["flags"].append(f)
            z.setdefault("flag_tag", {})[f] = z["tag"] - 1          # die Tat geschah am Tag, der gerade endete
        st = stufe(z, tid)
        for s in (1, 2):
            marke = "%s_ruf%d" % (f, s)
            if st is not None and st >= s and t.get("ruf") and marke not in z["flags"] and regeln.gilt(t.get("ruf_wenn"), z):
                z["flags"].append(marke)
                zeilen.append("🗣 The village is talking: %s" % t["titel"])
                zeilen += folgen_anwenden(z, modul, [{"wert": "ruf", "delta": t["ruf"]}])
    if "ruf" in modul["werte"]:
        ruhe = z["tag"] - z.setdefault("ruf_tag", z["tag"])
        if z["werte"].get("ruf", 0) > 0 and ruhe >= RUF_RUHE and (ruhe - RUF_RUHE) % RUF_TAKT == 0:
            schutz = modul.get("ruf_schutz") or {}
            if schutz.get("bekannt") in (z.get("bekannt") or []) and schutz["flag"] not in z["flags"]:
                z["flags"].append(schutz["flag"])           # einmal je Lauf haelt jemand die Geschichte am Leben
                zeilen.append(schutz["text"])
            else:
                z["werte"]["ruf"] -= 1
                zeilen.append("The village has other things to talk about. %s %d" % (modul["werte"]["ruf"]["label"], -1))
    return zeilen


def ruf_wort(wert):
    return RUF_WORTE[max(0, min(len(RUF_WORTE) - 1, int(wert)))]


def zeile(moddir, zid):
    """'leg.<id>' -> (wer, text) fuer die Vertonung."""
    l = daten(moddir)["zeilen"].get(zid[4:] if zid.startswith("leg.") else zid)
    return (l["wer"], l["text"]) if l else (None, None)


def alle_zeilen(moddir):
    """[(schluessel, figur, text)] fuer werkzeuge/eden_rise/vertonen_eden_rise.py."""
    return [("leg." + zid, l["wer"], l["text"]) for zid, l in sorted(daten(moddir)["zeilen"].items())]
