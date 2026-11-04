# -*- coding: utf-8 -*-
"""Wiederaufbau in Akt 3 (Duc 01.11.2026, Umbau 04.11.2026 nach Drehbuch Akt 3 Abschnitt 4.1, E-123, E-125).

Was bei der Belagerung abbrennt, setzt ein Flag tk_haus_weg_<id>. Daraus entstehen Baustellen.
  1. Duc setzt den ersten Stein (Karte "Lend a Hand", Folge {"aufbau_beginnen": id}). Erst dann tragen die Piraten dort.
  2. Duc liefert die Baustoffe der naechsten Stufe (Nonnas Fenster, Reiter "Village", keine Phase): liefern().
  3. Nachts tragen Buenaventuras Maenner (nach buenaventura_schwur) an jeder begonnenen Baustelle mit Lieferung eine Stufe.
  4. Ein Bauen-Los der Festa ({"aufbau_stufe": id oder "*"}) setzt eine Stufe ohne Baustoffe.
Jedes Haus braucht eigene Baustoffe und schickt Duc damit zu einer anderen Mechanik (Macchia, Steinbruch, Angeln, Kampf).
Charlys Geld (a3_charly_geld): jede offene Stufe kostet 20 % weniger, je Posten abgerundet, mindestens 1.
Wiki: docs/wiki/welt/drehbuch_akt3.md 4.1 und 12a."""
from . import kuechen

ORTE = {"post": "Post Office", "batu": "Ba Tu's Shop", "bar": "Alva's Bar", "werkstatt": "Petru's Workshop"}
BESITZER = {"post": "mina", "batu": "batu", "bar": "alva", "werkstatt": "petru"}
# Drei Stufen je Haus (Duc 04.11.2026 bestaetigt): Geruest aus Holz, Dach, zuletzt das Eisen. Die letzte oeffnet den Ort wieder.
STUFEN = {
    # Duc 04.11.2026: der Stahl der Roboter (The Red Light, Scrap Field, Villa) gehoert in jede letzte Stufe
    "post": ({"timber": 4}, {"slate": 3, "cork": 2}, {"cork": 2, "iron": 1, "steel": 1}),
    "batu": ({"timber": 3, "granite": 2}, {"slate": 3}, {"granite": 4, "steel": 1}),
    "bar": ({"timber": 4}, {"timber": 2, "slate": 2}, {"iron": 2, "steel": 1}),
    "werkstatt": ({"timber": 5}, {"timber": 2, "slate": 3}, {"iron": 2, "steel": 2}),
}
RABATT = 0.8                       # Charlys Geld (E-125)
CHARLY = "a3_charly_geld"


def _stand(z):
    return z.setdefault("aufbau", {})


def baustellen(z):
    """Alle abgebrannten Orte mit ihrem Stand. Neue kommen dazu, Fertiges bleibt."""
    st = _stand(z)
    for hid in ORTE:
        if "tk_haus_weg_" + hid in z.get("flags", []) and hid not in st:
            st[hid] = {"stufe": 1 if "tk_haus_geflickt_" + hid in z.get("flags", []) else 0,   # notduerftig geflickt am Morgen der Belagerung
                       "begonnen": False, "geliefert": False}
    for s in st.values():          # alte Staende ohne die neuen Felder
        s.setdefault("begonnen", False)
        s.setdefault("geliefert", False)
    return st


def fertig(z, hid):
    s = baustellen(z).get(hid)
    return bool(s) and s["stufe"] >= len(STUFEN[hid])


def braucht(z, hid):
    """Baustoffe der naechsten Stufe (mit Charlys Rabatt). {} wenn fertig."""
    s = baustellen(z).get(hid)
    if not s or s["stufe"] >= len(STUFEN[hid]):
        return {}
    roh = STUFEN[hid][s["stufe"]]
    if CHARLY in z.get("flags", []):
        return {k: max(1, int(n * RABATT)) for k, n in roh.items()}
    return dict(roh)


def ansicht(z):
    roh = kuechen.rohstoffe(z)
    out = []
    for hid, s in baustellen(z).items():
        b = braucht(z, hid)
        out.append({"id": hid, "name": ORTE[hid], "besitzer": BESITZER[hid], "stufe": s["stufe"], "stufen": len(STUFEN[hid]),
                    "fertig": s["stufe"] >= len(STUFEN[hid]), "begonnen": s["begonnen"], "geliefert": s["geliefert"],
                    "braucht": [{"id": k, "n": n, "hast": roh.get(k, 0)} for k, n in b.items()],
                    "geht": s["begonnen"] and not s["geliefert"] and bool(b) and all(roh.get(k, 0) >= n for k, n in b.items()),
                    "rabatt": CHARLY in z.get("flags", [])})
    return out


def beginnen(z, hid):
    """Duc setzt den ersten Stein. -> Zeilen."""
    s = baustellen(z).get(hid)
    if not s or s["begonnen"]:
        return []
    s["begonnen"] = True
    f = "aufbau_begonnen_" + hid
    if f not in z.setdefault("flags", []):
        z["flags"].append(f)
    return ["Building site: %s. The first stone is yours." % ORTE[hid]]


def liefern(z, hid):
    """Baustoffe der naechsten Stufe abgeben. Die Piraten bauen sie in der Nacht."""
    s = baustellen(z).get(hid)
    if not s:
        raise ValueError("There is nothing to build here.")
    if not s["begonnen"]:
        raise ValueError("Lay the first stone there first.")
    if s["geliefert"]:
        raise ValueError("The materials are already there. The pirates build tonight.")
    b = braucht(z, hid)
    if not b:
        raise ValueError("This house is finished.")
    kuechen.rohstoffe_nehmen(z, b)                 # alles oder nichts
    s["geliefert"] = True


def _stufe_hoch(z, hid, s):
    s["stufe"] += 1
    s["geliefert"] = False
    if s["stufe"] >= len(STUFEN[hid]):
        f = "aufbau_fertig_" + hid
        if f not in z.setdefault("flags", []):
            z["flags"].append(f)
            z.setdefault("flag_tag", {}).setdefault(f, z.get("tag", 0))   # fuer flag_seit: Dank-Szene am Morgen danach
        return True
    return False


def stufe_geschenkt(z, hid="*"):
    """Bauen-Los: eine Stufe ohne Baustoffe, am genannten Haus oder (\"*\") am weitesten begonnenen offenen. -> Zeilen."""
    st = baustellen(z)
    if hid == "*":
        offen = [(s["begonnen"], s["stufe"], h) for h, s in st.items() if s["stufe"] < len(STUFEN[h])]
        if not offen:
            return []
        hid = max(offen)[2]
    s = st.get(hid)
    if not s or s["stufe"] >= len(STUFEN[hid]):
        return []
    fertig_jetzt = _stufe_hoch(z, hid, s)
    return ["%s: %s" % (ORTE[hid], "finished!" if fertig_jetzt else "one stage further")]


def tag_vorbei(z):
    """Nachts: Buenaventuras Maenner bauen jede gelieferte Stufe an begonnenen Baustellen. -> Zeilen."""
    if "buenaventura_schwur" not in z.get("flags", []):
        return []
    zeilen = []
    for hid, s in baustellen(z).items():
        if s["begonnen"] and s["geliefert"] and s["stufe"] < len(STUFEN[hid]):
            zeilen.append("The pirates worked all night at %s: %s" % (ORTE[hid], "finished!" if _stufe_hoch(z, hid, s) else "one stage further"))
    return zeilen
