# -*- coding: utf-8 -*-
"""Wiederaufbau in Akt 3 (Duc 01.11.2026, Fundament, noch ohne Oberflaeche und ohne Kalender).

Was bei der Belagerung abbrennt, setzt ein Flag tk_haus_weg_<id>. Daraus entstehen Baustellen. Duc bringt Material, Buenaventuras
Maenner tragen nach ihrem Schwur (buenaventura_schwur) je Tag einen Schritt von selbst. Daten: AUFTRAEGE unten. Wiki: docs/wiki/welt/akt3.md.
"""

ORTE = {"post": "Post Office", "batu": "Ba Tu's Shop", "bar": "Alva's Bar", "werkstatt": "Petru's Workshop"}
# Baustoffe gibt es schon (Nonna, Petru): Stufen des Wiederaufbaus. Jede Stufe kostet Material, die letzte oeffnet den Ort wieder.
STUFEN = ({"timber": 4}, {"slate": 3, "timber": 2}, {"iron": 2})


def _stand(z):
    return z.setdefault("aufbau", {})


def baustellen(z):
    """Alle abgebrannten Orte mit ihrem Stand. Neue kommen dazu, Fertiges bleibt."""
    st = _stand(z)
    for hid in ORTE:
        if "tk_haus_weg_" + hid in z.get("flags", []) and hid not in st:
            st[hid] = {"stufe": 1 if "tk_haus_geflickt_" + hid in z.get("flags", []) else 0}   # Was im Morgen der Belagerung notduerftig geflickt wurde
    return st


def ansicht(z):
    return [{"id": hid, "name": ORTE[hid], "stufe": s["stufe"], "stufen": len(STUFEN), "fertig": s["stufe"] >= len(STUFEN),
             "braucht": STUFEN[s["stufe"]] if s["stufe"] < len(STUFEN) else {}} for hid, s in baustellen(z).items()]


def bauen(z, hid, inventar):
    """Eine Stufe bauen. inventar: dict Baustoff -> Menge, wird veraendert. -> True, wenn der Ort damit fertig ist."""
    s = baustellen(z).get(hid)
    if not s or s["stufe"] >= len(STUFEN):
        raise ValueError("Hier gibt es nichts zu bauen.")
    braucht = STUFEN[s["stufe"]]
    if any(inventar.get(k, 0) < n for k, n in braucht.items()):
        raise ValueError("Dafuer fehlt Material.")
    for k, n in braucht.items():
        inventar[k] -= n
    return _fertig(z, hid, s)


def _fertig(z, hid, s):
    s["stufe"] += 1
    if s["stufe"] >= len(STUFEN):
        f = "aufbau_fertig_" + hid
        if f not in z.setdefault("flags", []):
            z["flags"].append(f)
        return True
    return False


def tag_vorbei(z):
    """Buenaventuras Maenner tragen Steine: Nach ihrem Schwur kommt die am weitesten fortgeschrittene Baustelle je Tag einen Schritt voran."""
    if "buenaventura_schwur" not in z.get("flags", []):
        return None
    offen = [(s["stufe"], hid) for hid, s in baustellen(z).items() if s["stufe"] < len(STUFEN)]
    if not offen:
        return None
    _, hid = max(offen)
    _fertig(z, hid, _stand(z)[hid])
    return hid
