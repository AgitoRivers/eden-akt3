# -*- coding: utf-8 -*-
"""Auftraege (E-074, 26.10.2026) - die grossen Missionen neben den Schnelljobs (handel.py).

Ein Auftrag hat eine Auftraggeberin, einen Ort, Schritte und einen Abschluss mit Uebergabe. Sein Stand steht nur in
Flags (angenommen/fertig, Schritte als Bedingungen) - die Frames des Orts setzen sie. Daten: module\\<id>\\auftraege.json,
gebaut aus werkzeuge\\eden_rise\\auftraege_eden_rise.py.

  orte:      {id: {"label", "text", "bild", "phasen", "wenn", "start": [{"wenn", "id"}, ..., {"id"}]}}
  auftraege: {id: {"titel", "von", "ort", "text", "angenommen", "fertig", "schritte": [{"text", "erledigt"}],
                   "grau": [{"text", "wahl": {flag: Text}}], "belohnung", "romanze": bool}}

Romanze (E-074 Punkt 4): Wer den Auftrag einer Frau mit Begehren abschliesst, hebt ihr Begehren auf die naechste Stufe.
"""
import json
import os

from . import regeln, zustand

_CACHE = {}


def daten(moddir):
    pfad = os.path.join(moddir, "auftraege.json")
    if not os.path.exists(pfad):
        return None
    st = os.path.getmtime(pfad)
    if _CACHE.get(pfad, (None,))[0] != st:
        _CACHE[pfad] = (st, json.load(open(pfad, encoding="utf-8")))
    return _CACHE[pfad][1]


def status(z, a):
    if a["fertig"] in z["flags"]:
        return "fertig"
    if a["angenommen"] in z["flags"]:
        return "aktiv"
    return None


def orte_frei(z, moddir):
    """Orte, die Duc in dieser freien Phase besuchen kann -> [{"id", "label", "text", "bild"}]."""
    d = daten(moddir)
    if not d:
        return []
    return [{"id": oid, "label": o["label"], "text": ort_text(z, o), "bild": "/bg/" + o["bild"] if o["bild"].endswith(".png") else "/bg/eden_rise_%s.png" % o["bild"]}
            for oid, o in d["orte"].items()
            if regeln.phase_passt(z["phase"], o["phasen"]) and regeln.gilt(o.get("wenn"), z) and start(z, moddir, oid)]


def ort_text(z, o):
    """Die Karte beschreibt die Lage: Der aktuelle Startpunkt darf einen eigenen Text haben (Duc 31.10.2026, der Spieler vergisst)."""
    s = next((s for s in o["start"] if regeln.gilt(s.get("wenn"), z)), None)
    return (s or {}).get("text") or o["text"]


def tagesbeginn(z, moddir):
    """Merkt sich je Ort den ersten Tag, an dem er offen war (z["ort_offen_seit"]). Zusammen mit z["ort_zuletzt"]
    (eden.ort_betreten) ergibt das die Bedingung ort_ruhe: so lange war Duc nicht dort (Erinnerung, Duc 02.11.2026)."""
    d = daten(moddir)
    if not d:
        return
    seit = z.setdefault("ort_offen_seit", {})
    for oid, o in d["orte"].items():
        if oid not in seit and regeln.gilt(o.get("wenn"), z):
            seit[oid] = z["tag"]


def start(z, moddir, oid):
    """Erster Frame beim Betreten (erster Besuch oder Wiederkommen) oder None."""
    o = daten(moddir)["orte"].get(oid)
    if not o:
        return None
    return next((s["id"] for s in o["start"] if regeln.gilt(s.get("wenn"), z)), None)


def pruefen(z, modul, moddir):
    """Nach jedem geschlossenen Event: frisch abgeschlossene Auftraege melden, Romanzen-Stufe vergeben -> Zeilen."""
    d = daten(moddir)
    if not d:
        return []
    zeilen = []
    for aid, a in d["auftraege"].items():
        if aid in z.get("auftraege_fertig", []) or status(z, a) != "fertig":
            continue
        z.setdefault("auftraege_fertig", []).append(aid)
        zeilen.append("📜 Auftrag abgeschlossen: " + a["titel"])
        key = "begehren." + a["von"]
        if a.get("romanze") and key in z["werte"] and z["werte"][key] < 5:
            ziel = zustand.STUFEN_AB[z["werte"][key] + 1]
            zeilen += zustand.punkte_add(z, modul, key, ziel - zustand.punkte(z, key), roh=True)
    return zeilen


def journal(z, modul, moddir, sprite_fn):
    """Journal im Menue (Taste N): angenommene und erledigte Auftraege, neueste zuerst; erledigte am Ende."""
    d = daten(moddir)
    if not d:
        return []
    out = []
    for aid, a in d["auftraege"].items():
        st = status(z, a)
        if not st:
            continue
        if st == "aktiv" and a.get("bis_tag") and z["tag"] >= a["bis_tag"]:
            st = "verpasst"                              # Frist vorbei (z. B. Kevins Seite bis Tag 14), 29.10.2026
        # optionale Schritte (Umwege, 29.10.2026): "optional" zaehlt nie als naechster Schritt, "wenn" blendet sie erst ein,
        # wenn Duc den Abzweig kennt (kein Spoiler); ein schon erledigter Schritt bleibt immer sichtbar
        schritte = [{"text": s["text"], "erledigt": regeln.gilt(s["erledigt"], z), "optional": bool(s.get("optional"))}
                    for s in a["schritte"] if regeln.gilt(s["erledigt"], z) or regeln.gilt(s.get("wenn"), z)]
        naechster = next((s["text"] for s in schritte if not s["erledigt"] and not s["optional"]), None)
        rueckblick = next((s["rueckblick"] for s in reversed(a["schritte"]) if s.get("rueckblick") and regeln.gilt(s["erledigt"], z)), None)
        grau = [{"text": g["text"], "entschieden": next((t for f, t in g["wahl"].items() if f in z["flags"]), None)}
                for g in a.get("grau", [])]
        p = modul["personen"].get(a["von"]) or {}
        out.append({"id": aid, "titel": a["titel"], "von": a["von"], "von_name": p.get("name", a["von"]),
                    "sprite": sprite_fn(a["von"]) if p else None, "status": st, "text": a["text"],
                    "ort": d["orte"].get(a["ort"], {}).get("label", ""), "naechster": naechster if st == "aktiv" else None,
                    "zeiten": d["orte"].get(a["ort"], {}).get("phasen", []),       # Tageszeiten, zu denen der Ort offen ist
                    "frist": a["bis_tag"] - 1 if a.get("bis_tag") else None,        # letzter Tag (bis_tag = erster verpasster)
                    "schritte": schritte, "grau": grau, "belohnung": a.get("belohnung", ""),
                    "rueckblick": rueckblick if st == "aktiv" else None,      # "Last time": der Spieler vergisst (31.10.2026)
                    "neben": bool(a.get("neben"))})               # Journal: Haupt- und Neben-Auftraege getrennt (29.10.2026)
    out.sort(key=lambda x: x["status"] != "aktiv")
    return out
