# -*- coding: utf-8 -*-
"""Album im Beziehungsmenue (Duc 31.10.2026): Was mit einer Frau passiert ist, chronologisch, mit Notizen in ihrer Handschrift.

Quellen: Selfies und Leiter-Szenen merkt sich merken() beim Ziehen, der erste Kuss usw. steht schon in der Chronik.
Favours bleiben draussen, die sind ein eigenes Geheimnis. Spielstaende von vor dem 31.10. zeigen nur die Chronik-Momente."""
import json, os, re

BASIS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOMENTE = {"kiss": "The first kiss", "confession": "When you said it", "intimate": "The first night"}
_LEITER = re.compile(r"rm_([a-z])(\d)(_[a-z])?$")
_CACHE = {}


def daten(mid):
    """Inhalt von module\\<mid>\\album.json (nach Aenderungszeit zwischengespeichert); ohne Datei leer."""
    pfad = os.path.join(BASIS, "module", mid or "", "album.json")
    try:
        mt = os.path.getmtime(pfad)
    except OSError:
        return {}
    c = _CACHE.get(pfad)
    if c and c[0] == mt:
        return c[1]
    try:
        d = json.load(open(pfad, encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    _CACHE[pfad] = (mt, d)
    return d


def merken(z, ev, selfie=None):
    """Beim Ziehen eines Events: Selfie oder Leiter-Szene ins Album. Andere Events zaehlen nicht."""
    a = daten(z.get("modul"))
    if selfie:
        s = ev["personen"]["selfie"]
        z.setdefault("album", []).append({"art": "selfie", "wer": s["frau"], "tag": z["tag"], "titel": ev.get("titel", ""),
                                          "bild": selfie, "stufe": s.get("stufe")})
        return
    t = _LEITER.match(ev["id"])
    wer = (a.get("leiter") or {}).get(t.group(1)) if t else None
    if not wer or "rm_%s%s" % (t.group(1), t.group(2)) in (a.get("ohne") or []):
        return
    stufe = int(t.group(2))
    if any(e["art"] == "szene" and e["wer"] == wer and e.get("stufe") == stufe for e in z.get("album") or []):
        return                                       # dieselbe Stufe in anderem Rahmen (rm_r1_b) ist kein neues Blatt
    z.setdefault("album", []).append({"art": "szene", "wer": wer, "tag": z["tag"], "titel": ev.get("titel", ""), "stufe": stufe})


def _notiz(notizen, e):
    n = notizen.get(e["wer"]) or {}
    if e["art"] in MOMENTE:
        return n.get(e["art"])
    return (n.get(e["art"]) or {}).get(str(e.get("stufe")))


def ansicht(z, modul):
    """[{id, name, eintraege: [{art, tag, titel, notiz, bild}]}], je Frau nach Tagen; ohne Eintraege faellt sie weg."""
    notizen = daten(z.get("modul")).get("notizen") or {}
    alle = [dict(e) for e in z.get("album") or []]
    erste = set()
    for e in z.get("chronik") or []:                 # nur das erste Mal zaehlt, sonst besteht das Album aus Wiederholungen
        if e.get("moment") in MOMENTE and e.get("wer"):
            k = (e["wer"][0], e["moment"])
            if k not in erste:
                erste.add(k)
                alle.append({"art": e["moment"], "wer": e["wer"][0], "tag": e["tag"], "titel": MOMENTE[e["moment"]]})
    aus = []
    for pid in sorted({e["wer"] for e in alle}):
        if pid not in modul["personen"]:
            continue
        liste = sorted((e for e in alle if e["wer"] == pid), key=lambda e: e["tag"])
        aus.append({"id": pid, "name": modul["personen"][pid]["name"].split()[0],
                    "eintraege": [{"art": e["art"], "tag": e["tag"], "titel": e["titel"], "notiz": _notiz(notizen, e),
                                   "bild": "/selfie/%s.webp" % e["bild"] if e.get("bild") else None} for e in liste]})
    return aus
