# -*- coding: utf-8 -*-
"""Jacken-Charms (Duc 28.10.2026): ein Anhaenger je wichtiger Figur, ein runder Platz an jeder Jacke.

Regel der Engine: der CODE entscheidet und bucht, Texte stehen fest in module\\<modul>\\charms.json (Builder
werkzeuge\\eden_rise\\charms_eden_rise.py). Uebergabe ueber Handy-Events (ereignisse_charms.py, Folge {"charm": id}).
  * Bekommen: Vertrauen 5 bei der Figur (Event), Fredericos Loewe ueber die volle Farm (Flag farm_voll),
    A Mazzera's Hunting Charm als Unikat der Berge (Folge {"charm": "mazzera"} im Fund).
  * Tragen: je Jacke ein Charm, ein Charm haengt immer nur an einer Jacke (wie die Chips); geht auch vor Rosis Werkstatt.
  * Wirken: nur der Charm an der getragenen Jacke. Attribut-Boni gelten ueberall (Kampf, Szenen, Events, Jobs) und
    duerfen ueber 5 gehen; Kampfwerte laufen ueber kampf.chips_aktiv (dieselben Namen wie bei den Erweiterungen)."""
import json, os

_CACHE = {}
BASIS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def daten(mid):
    """{charm_id: {...}} aus module\\<mid>\\charms.json (nach Aenderungszeit zwischengespeichert); ohne Datei: leer."""
    pfad = os.path.join(BASIS, "module", mid or "", "charms.json")
    try:
        mt = os.path.getmtime(pfad)
    except OSError:
        return {}
    c = _CACHE.get(pfad)
    if c and c[0] == mt:
        return c[1]
    try:
        d = json.load(open(pfad, encoding="utf-8")).get("charms", {})
    except (OSError, ValueError):
        d = {}
    _CACHE[pfad] = (mt, d)
    return d


def stand(z):
    """{"besitz": [ids], "an": {jacken_id: charm_id}} im Spielstand (wird erst beim ersten Charm angelegt)."""
    return z.get("charms") or {"besitz": [], "an": {}}


def _jacke(z):
    from . import kampf
    return (z.get("equipment") or {}).get("armor") or kampf.START_ARMOR


def geben(z, cid):
    """Charm in den Besitz; haengt ihn gleich an die getragene Jacke, wenn dort noch keiner ist -> Anzeigezeile."""
    d = daten(z.get("modul"))
    c = d.get(cid)
    if not c:
        return []
    s = z.setdefault("charms", {"besitz": [], "an": {}})
    if cid in s["besitz"]:
        return []
    s["besitz"].append(cid)
    if "charm_" + cid not in z.setdefault("flags", []):
        z["flags"].append("charm_" + cid)          # sperrt die zweite Uebergabe (ereignisse_charms.py)
    jacke = _jacke(z)
    if not s["an"].get(jacke):
        s["an"][jacke] = cid
        return ["🧸 %s – on your jacket (%s)" % (c["label"], c["wirkung_text"])]
    return ["🧸 %s – in your cabin (%s)" % (c["label"], c["wirkung_text"])]


def einsetzen(z, jacke, cid):
    s = stand(z)
    if cid not in s["besitz"]:
        raise ValueError("You don't have that charm.")
    s = z.setdefault("charms", s)
    for j, c in list(s["an"].items()):
        if c == cid:
            del s["an"][j]
    s["an"][jacke] = cid


def entfernen(z, jacke, cid):
    s = stand(z)
    if s["an"].get(jacke) != cid:
        raise ValueError("That charm isn't on this jacket.")
    del z["charms"]["an"][jacke]


def getragen(z):
    """Definition des Charms an der getragenen Jacke oder None."""
    cid = stand(z)["an"].get(_jacke(z))
    c = daten(z.get("modul")).get(cid) if cid else None
    return dict(c, id=cid) if c else None


def attribut(z, att):
    """Bonus des getragenen Charms auf ein Attribut (0 ohne)."""
    c = getragen(z)
    return int(((c or {}).get("wirkung") or {}).get("attribute", {}).get(att, 0))


def boni(z, att):
    """Fuer die Wuerfelanzeige: [("Lola's Kangaroo", 1)] oder []."""
    n = attribut(z, att)
    return [(getragen(z)["label"], n)] if n else []


def kampfwerte(z):
    """{stat: wert} des getragenen Charms fuer kampf.chips_aktiv (ohne Attribute)."""
    c = getragen(z)
    return dict(((c or {}).get("wirkung") or {}).get("kampf") or {})


def ansicht(z):
    """Fuer das Upgrade-Fenster: eigene Charms mit Bild, Wirkung und Jacke."""
    d, s = daten(z.get("modul")), stand(z)
    ort = {c: j for j, c in s["an"].items()}
    return [{"id": cid, "label": d[cid]["label"], "figur": d[cid].get("figur"), "text": d[cid]["text"],
             "wirkung": d[cid]["wirkung_text"], "bild": "/itembild/%s" % d[cid]["bild"], "an": ort.get(cid),
             "seltenheit": d[cid].get("seltenheit", "normal")} for cid in s["besitz"] if cid in d]
