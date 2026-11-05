# -*- coding: utf-8 -*-
"""Minas Fahrt nach Bastia (Akt 3, Drehbuch docs/wiki/welt/drehbuch_akt3.md 4.1, Wirkpunkt der Post; Mina-Dossier 05.11.2026).

In a3_dank_post verspricht Mina: "Every day I go to Bastia anyway. What do you need? I'll bring it." Hier wirkt das:
  * Offen ab der wieder aufgebauten Post (aufbau_fertig_post, Dank-Szene am Morgen danach) oder, wenn die Post nie
    abgebrannt ist, nach der Szene "Second Gear" (Flag a3_post_bastia). Keine Phase, ein Kreis im Reiter "Village".
  * Wahl aus drei fuer den naechsten Morgen: ein Baustoff (der, der an der Baustelle am meisten fehlt), eine Zutat aus
    Bastia oder "Mina's choice" (Ueberraschung: doppelter Baustoff oder eine Zutat mit drei Sternen).
  * Waehlt Duc nichts, waehlt Mina selbst ("I don't read them. I just know."): den fehlenden Baustoff. Kein Zwang, keine Liste.
  * Mit der reparierten Vespa (mina_vespa_heil, Szene "Second Gear") bringt sie von Baustoff und Zutat das Doppelte.
  * Stahl bringt sie nie (WO in kern/aufbau.py: Stahl gibt es nur in den Maschinen).
Lieferungen an den Morgen von Tag 26 bis 34; bestellt wird am Vortag."""
from . import aufbau, kuechen

LIEFERTAGE = (26, 34)
FLAG_AN = "a3_post_bastia"          # Second Gear, wenn die Post nie abgebrannt ist
VESPA = "mina_vespa_heil"
HART = ("slate", "granite", "cork", "iron")       # was man im Dorf schwer findet; Holz gibt es in der Macchia genug
ZUTATEN = ("fish_sauce", "tofu", "rice_paper", "salmon_steak")   # Bastia hat einen Markt und einen Asia-Grossmarkt
NAME = {"timber": "Timber", "slate": "Slate", "granite": "Granite", "cork": "Cork", "iron": "Iron Fittings",
        "fish_sauce": "Fish Sauce", "tofu": "Tofu", "rice_paper": "Rice Paper", "salmon_steak": "Salmon Steak"}


def _f(z):
    return z.get("flags", [])


def offen(z):
    """Kann Mina heute bestellen (fuer morgen)?"""
    f = _f(z)
    if "akt2_ende" not in f or not (LIEFERTAGE[0] - 1 <= z.get("tag", 0) <= LIEFERTAGE[1] - 1):
        return False
    return "aufbau_fertig_post" in f or FLAG_AN in f


def _stand(z):
    return z.setdefault("post", {"bestellt": None, "geliefert": 0})


def _fehlt(z):
    """Baustoff, der an begonnenen Baustellen am meisten fehlt (ohne Stahl), sonst der seltenste harte."""
    roh = kuechen.rohstoffe(z)
    luecke = {}
    for hid, s in aufbau.baustellen(z).items():
        if not s["begonnen"] or s["geliefert"]:
            continue
        for k, n in aufbau.braucht(z, hid).items():
            if k != "steel" and roh.get(k, 0) < n:
                luecke[k] = luecke.get(k, 0) + n - roh.get(k, 0)
    if luecke:
        return max(sorted(luecke), key=lambda k: luecke[k])
    return min(HART, key=lambda k: (roh.get(k, 0), HART.index(k)))


def _zutat(z):
    return ZUTATEN[z.get("tag", 0) % len(ZUTATEN)]


def angebot(z):
    """Die drei Wahlen fuer morgen. Jede mit id, Text (englisch, fuer den Kreis) und dem, was kommt."""
    n = 2 if VESPA in _f(z) else 1
    bau, zt = _fehlt(z), _zutat(z)
    return [
        {"id": "bau", "text": "%d × %s for the building site" % (n, NAME[bau]), "was": ("roh", bau, n, None)},
        {"id": "kueche", "text": "%d × %s from the market in Bastia" % (n, NAME[zt]), "was": ("zutat", zt, n, 2)},
        {"id": "mina", "text": "Mina's choice. She just knows.", "was": None},
    ]


def bestellen(z, wahl):
    if not offen(z):
        raise ValueError("Mina isn't going to Bastia tomorrow.")
    if wahl not in ("bau", "kueche", "mina"):
        raise ValueError("Mina doesn't know what you mean.")
    _stand(z)["bestellt"] = wahl


def ansicht(z):
    if not offen(z):
        return None
    st = _stand(z)
    return {"bestellt": st.get("bestellt"), "vespa": VESPA in _f(z),
            "wahl": [{"id": w["id"], "text": w["text"]} for w in angebot(z)]}


def _ueberraschung(z):
    r = kuechen.rng(z, "post")
    if r.random() < 0.6:
        return ("roh", _fehlt(z), 2, None)
    return ("zutat", ZUTATEN[r.randrange(len(ZUTATEN))], 1, 3)


def morgen(z, modul=None):
    """Lieferung am neuen Morgen (z["tag"] ist schon der neue Tag). -> Zeilen fuer "Day X is over"."""
    f = _f(z)
    tag = z.get("tag", 0)
    if "akt2_ende" not in f or not LIEFERTAGE[0] <= tag <= LIEFERTAGE[1]:
        return []
    if "aufbau_fertig_post" not in f and FLAG_AN not in f:
        return []
    z["tag"] = tag - 1                         # Angebot und Zufall gehoeren zum Tag der Bestellung
    try:
        st = _stand(z)
        selbst = not st.get("bestellt")        # nichts gewaehlt: Mina waehlt selbst den fehlenden Baustoff
        wahl = st.get("bestellt") or "bau"
        was = _ueberraschung(z) if wahl == "mina" else next(w["was"] for w in angebot(z) if w["id"] == wahl)
    finally:
        z["tag"] = tag
    art, wid, n, stern = was
    if art == "roh":
        kuechen.rohstoff_add(z, wid, n)
    else:
        kuechen.vorrat_add(z, wid, stern, n)
    st["bestellt"] = None
    st["geliefert"] = st.get("geliefert", 0) + 1
    ding = "%d × %s%s" % (n, NAME[wid], " ★★★" if stern == 3 else "")
    if wahl == "mina":
        return ["Mina honks twice at the quay and throws you a parcel from Bastia: %s. “Don't ask. I just know.”" % ding]
    if selbst:
        return ["Mina honks twice at the quay. You didn't tell her what you need, so she brought it anyway: %s." % ding]
    return ["Mina honks twice at the quay. From Bastia: %s." % ding]
