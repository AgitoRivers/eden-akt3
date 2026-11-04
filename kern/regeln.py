# -*- coding: utf-8 -*-
"""Bedingungssprache - EINE Sprache fuer Raeume, Storylets, Ereignisse, Dialogoptionen und Enden.

Bausteine (mehrere Schluessel in einem Objekt = alle muessen gelten):
  {"wert": ["vertrauen.lea", ">=", 3]}   {"uhr": ["gutachten", ">=", 2]}   {"flag": "voss_an_bord"}
  {"item": "master_key"}   {"persona": "first_officer"}   {"tag_ab": 3}   {"phase": "nacht"}
  {"vertrauen": ["chiara", 3]} (Kurzform)   {"begleitung": "chiara"} (nur mit Szenen-Kontext)
  {"gesehen": "wreck_dive"}               {"alle": [...]}  {"eine": [...]}  {"nicht": {...}}
  {"flag_seit": ["bg_baer_frei", 2]}  (Flag aus der Folge {"flag_datiert": ...}, mindestens 2 Tage her)
  {"flags_anzahl": ["rt_t_still_", ">=", 5]}  (wie viele Flags mit diesem Anfang gesetzt sind)
  {"wurf": ["cunning", 14], "risiko": "..."}  -> kein Muss, sondern ein eigener Weg mit Probe
"""
import operator

from . import rollen

# Modell B (24.10.2026): "tag" ist der Mittag, "nachmittag" kam dazu. Wo es fuer den Nachmittag keine eigene Angabe
# gibt (Tagesablauf, Event-Phasen, Set-Regeln, Bedingungen), gilt er wie der Mittag.
PHASE_WIE = {"nachmittag": "tag"}


def phase_wie(ph):
    return PHASE_WIE.get(ph, ph)


def phase_passt(ph, liste):
    """Steht die Phase (oder die Phase, wie die sie gilt) in der Liste?"""
    return ph in liste or phase_wie(ph) in liste


OPS = {">=": operator.ge, "<=": operator.le, ">": operator.gt, "<": operator.lt, "==": operator.eq, "!=": operator.ne}
NUR_TEXT = ("risiko", "label", "hinweis")


def gilt(b, z, kontext=None):
    """b = Bedingung, z = Spielstand (zustand.py), kontext = {"anwesend": [...], "phase": ...}."""
    if not b:
        return True
    kontext = kontext or {}
    for k, v in b.items():
        if k in NUR_TEXT:
            continue
        if k == "alle":
            ok = all(gilt(x, z, kontext) for x in v)
        elif k == "eine":
            ok = any(gilt(x, z, kontext) for x in v)
        elif k == "nicht":
            ok = not gilt(v, z, kontext)
        elif k == "wert":
            wert = z["werte"].get(v[0], 0)
            if v[0] == "megan_haltung":                 # Hauptstory (B4): aus Ducs Handeln berechnet, kein Wert
                from . import ermittlung
                wert = ermittlung.megan_haltung(z)
            if v[0] in rollen.ALIAS:                    # Draht des Haendlers ist sein Vertrauen (rollen.py)
                wert = max(wert, z["werte"].get(rollen.ALIAS[v[0]], 0))
            ok = OPS[v[1]](wert, v[2])
        elif k == "uhr":
            ok = OPS[v[1]](z["uhren"].get(v[0], 0), v[2])
        elif k == "vertrauen":
            ok = z["werte"].get("vertrauen." + v[0], 0) >= v[1]
        elif k == "flag":
            ok = v in z["flags"]
        elif k == "flags_anzahl":
            ok = OPS[v[1]](sum(1 for f in z["flags"] if f.startswith(v[0])), v[2])
        elif k == "item":
            ok = v in z["inventar"] or v in z.get("truhe", [])    # die Truhe zaehlt mit: dorthin geht, was nicht mehr in die Tasche passt
        elif k == "persona":            # Rolle der Persona (alle Personas eines Moduls koennen dieselbe Rolle haben)
            ok = bool(z.get("persona")) and v in (z["persona"].get("rolle"), z["persona"].get("id"))
        elif k == "jacke_verbaut":      # eine Jacke ist bei Rosi aufgeruestet (Red Trio, Platte in der Jacke)
            stufen = ((z.get("combat") or {}).get("werkstatt") or {}).get("stufen") or {}
            ok = any(st >= 1 and ("jacket_" in s or "cyber_armor" in s) for s, st in stufen.items())
        elif k == "tag_ab":
            ok = z["tag"] >= v
        elif k == "moment_offen":       # Romanzen-Leiter (31.10.2026): {"moment_offen": ["rosi", ["kiss"]]}, noch nicht aufgegriffen
            from . import chronik
            ok = chronik.moment_offen(z, v[0], v[1])
        elif k == "moment_zahl":        # {"moment_zahl": ["rosi", "intimate", ">=", 2]}
            from . import chronik
            ok = OPS[v[2]](chronik.moment_zahl(z, v[0], v[1]), v[3])
        elif k == "heute_gekaempft":    # Duc kommt heute aus einem Kampf
            ok = (z.get("kampf_tag") == z["tag"]) == bool(v)
        elif k == "bekannt":            # Duc hat die Person kennengelernt (Favours, 29.10.2026)
            ok = v in (z.get("bekannt") or [])
        elif k == "mochi":              # {"mochi": "geier"}: dieses Tier ist in Bibis Station gerettet (Akt 3, Bones)
            ok = v in ((z.get("mochis") or {}).get("tiere") or {})
        elif k == "anzahl":             # {"anzahl": [[bed, bed, ...], ">=", 4]}: wie viele der Bedingungen gelten (Akt 3: Zeugen, Beweise)
            n = sum(1 for x in v[0] if gilt(x, z, kontext))
            ok = OPS[v[1]](n, v[2])
        elif k == "versprochen":        # {"versprochen": ["toto", "crate"]}: Duc hat ihr/ihm etwas versprochen, Text enthaelt das Wort (Akt 3, 04.11.2026)
            ok = any(x.get("an") == v[0] and v[1].lower() in x.get("text", "").lower()
                     for x in ((z.get("ev") or {}).get("versprechen") or []))
        elif k == "flag_seit":          # {"flag_seit": ["bg_baer_frei", 2]}: Flag mit Datum, mindestens n Tage her
            ok = v[0] in z["flags"] and z["tag"] - z.get("flag_tag", {}).get(v[0], z["tag"]) >= v[1]
        elif k == "ort_ruhe":           # {"ort_ruhe": ["macchia", 3]}: Ort offen und Duc seit n Tagen nicht dort (02.11.2026)
            seit = (z.get("ort_offen_seit") or {}).get(v[0])
            ok = seit is not None and z["tag"] - max(seit, (z.get("ort_zuletzt") or {}).get(v[0], seit)) >= v[1]
        elif k in ("phase", "nur_phase"):
            ok = phase_passt(kontext.get("phase", z.get("phase")), [v])
        elif k == "begleitung":
            ok = v in kontext.get("anwesend", [])
        elif k == "gesehen":
            ok = v in z.get("gesehene_storylets", [])
        elif k == "wurf":
            ok = False      # ein Wurf ist kein "gilt", sondern ein eigener Weg (siehe zugang)
        elif k in ("kennt", "kennt_gesichert", "kette_bekannt", "angst"):    # Hauptstory-Ermittlung (B3, 17.10.2026)
            from . import ermittlung
            if k == "kennt":
                ok = ermittlung.kennt(z, v)
            elif k == "kette_bekannt" and isinstance(v, list):     # Anzahl belegter Glieder, z. B. [">=", 1]
                ok = OPS[v[0]](sum(1 for g in ermittlung.glieder_status(z) if g["belegt"]), v[1])
            elif k == "kette_bekannt":
                ok = ermittlung.kette_bekannt(z) == bool(v)
            else:
                ist = ermittlung.kennt_gesichert(z) if k == "kennt_gesichert" else ermittlung.angst(z)
                ok = OPS[v[0]](ist, v[1])
        else:
            raise ValueError("Unbekannter Bedingungs-Baustein: %r" % k)
        if not ok:
            return False
    return True


def zugang(raum, z, kontext=None):
    """("offen"|"wurf"|"gesperrt", weg). Jede Tuer soll mindestens zwei Wege haben."""
    wege = raum.get("zugang") or []
    if not wege:
        return "offen", None
    for w in wege:
        if "wurf" not in w and gilt(w, z, kontext):
            return "offen", w
    for w in wege:
        if "wurf" in w and gilt({k: v for k, v in w.items() if k != "wurf"}, z, kontext):
            return "wurf", w
    return "gesperrt", None
