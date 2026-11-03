# -*- coding: utf-8 -*-
"""Danzels Auftraege (Duc 30.10.2026, Wiki systeme/schneider.md): Das Dorf bestellt bei Le Theatre Rouge, Duc bringt das Material,
Danzel naeht ueber Nacht, am naechsten Tag kommt die Uebergabe als Event (ereignisse_schneider.py). Jeder dritte fertige Auftrag gibt
ein Schnittmuster; damit naeht Danzel einer Frau ein Massstueck, das ihr neues Outfit freischaltet (personen.<id>.set_frei).
Outfit-Quests (E-104): Ein Massstueck mit "quest" braucht kein Schnittmuster und steht im Laden, sobald seine Bedingung "wenn" gilt.
Keine Aktion, keine Phase. Stand nur in Flags: sn_<id> (datiert) = gebracht, sn_<id>_fertig = uebergeben."""
from . import handel, kuechen, regeln, zustand

MAX_OFFEN = 2                    # hoechstens zwei Bestellungen haengen gleichzeitig am Laden
MUSTER_JE = 3                    # jeder dritte fertige Dorfauftrag gibt ein Schnittmuster
AB_VERTRAUEN = 3                 # ab hier kann Duc ihre Masse erfragen


def _d(modul):
    return modul.get("schneider") or {}


def offen(z, modul):
    """Ist Danzels Laden da?"""
    l = (modul.get("laeden") or {}).get("danzel")
    return bool(l and _d(modul) and handel.laden_offen(z, l))


def muster(z, modul):
    """Schnittmuster, die Duc noch frei hat."""
    fertig = sum(1 for a in _d(modul)["auftraege"] if "sn_%s_fertig" % a["id"] in z["flags"])
    genutzt = sum(1 for m in _d(modul)["massstuecke"] if not m.get("quest") and "sn_%s" % m["id"] in z["flags"])
    return fertig // MUSTER_JE - genutzt


def _hat_item(z, iid):
    return (z.get("inventar") or []).count(iid) + (z.get("truhe") or []).count(iid)


def _material(z, modul, bedarf, items=None):
    """Rohstoffe und Gegenstaende aus der Tasche (Massstueck: Aquamarin fuer die Knoepfe)."""
    roh, da = kuechen.daten(modul).get("rohstoffe") or {}, kuechen.rohstoffe(z)
    return ([{"id": k, "label": roh[k]["label"], "n": n, "hat": da.get(k, 0)} for k, n in sorted(bedarf.items())] +
            [{"id": k, "label": modul["items"][k]["label"], "n": n, "hat": _hat_item(z, k)} for k, n in sorted((items or {}).items())])


def _status(z, a):
    if "sn_%s_fertig" % a["id"] in z["flags"]:
        return "fertig"
    return "laeuft" if "sn_%s" % a["id"] in z["flags"] else "neu"


def _auftraege(z, modul):
    """Laufende zuerst, dann die naechsten neuen, deren Kunde Duc kennt, zusammen hoechstens MAX_OFFEN."""
    alle = [a for a in _d(modul)["auftraege"] if a["kunde"] in (z.get("bekannt") or [])]
    laeuft = [a for a in alle if _status(z, a) == "laeuft"]
    neu = [a for a in alle if _status(z, a) == "neu"]
    return (laeuft + neu)[:MAX_OFFEN]


def _massstuecke(z, modul):
    return [m for m in _d(modul)["massstuecke"]
            if z["werte"].get("vertrauen." + m["frau"], 0) >= AB_VERTRAUEN and "gefeuert_" + m["frau"] not in z["flags"]
            and _status(z, m) != "fertig" and regeln.gilt(m.get("wenn"), z)]


def ansicht(z, modul):
    if not offen(z, modul):
        return None
    def zeile(a, art):
        status, mat = _status(z, a), _material(z, modul, a["material"], a.get("items"))
        kosten = a.get("geld", 0)
        geht = status == "neu" and all(m["hat"] >= m["n"] for m in mat) and z["konto"] >= kosten and (art != "mass" or a.get("quest") or muster(z, modul) > 0)
        return {"id": a["id"], "label": a["label"], "text": a["text"], "kunde": handel.anzeigename(modul, a.get("kunde") or a["frau"]),
                "material": mat, "lohn": a.get("lohn", 0), "geld": kosten, "status": status, "geht": geht}
    return {"auftraege": [zeile(a, "dorf") for a in _auftraege(z, modul)],
            "massstuecke": [zeile(m, "mass") for m in _massstuecke(z, modul)],
            "muster": muster(z, modul), "fertig": sum(1 for a in _d(modul)["auftraege"] if _status(z, a) == "fertig"),
            "muster_je": MUSTER_JE}


def bringen(z, modul, aid):
    """Material abgeben (Massstueck: dazu Geld und ein Schnittmuster). Zeilen fuer die Tagesmeldung."""
    if not offen(z, modul):
        raise ValueError("Danzel's shop isn't open.")
    a = next((x for x in _auftraege(z, modul) if x["id"] == aid), None)
    mass = next((x for x in _massstuecke(z, modul) if x["id"] == aid), None)
    a = a or mass
    if not a or _status(z, a) != "neu":
        raise ValueError("That order isn't open.")
    if mass and not mass.get("quest") and muster(z, modul) <= 0:
        raise ValueError("You don't have a pattern for that yet.")
    if z["konto"] < a.get("geld", 0):
        raise ValueError("You can't afford that.")
    if any(_hat_item(z, k) < n for k, n in (a.get("items") or {}).items()):
        raise ValueError("You're short of materials for that.")
    kuechen.rohstoffe_nehmen(z, a["material"])
    folgen = [{"flag_datiert": "sn_" + aid}, {"flag": "sn_" + aid}]
    folgen += [{"item_weg": k} for k, n in (a.get("items") or {}).items() for _ in range(n)]
    if a.get("geld"):
        folgen.append({"geld": -a["geld"], "text": a["label"]})
    return ["Danzel takes the materials: %s. It will be ready tomorrow." % a["label"]] + zustand.folgen_anwenden(z, modul, folgen)
