# -*- coding: utf-8 -*-
"""Kuechenkreis (Duc 27.10.2026, E-079): Vorrat, Baukasten (1 Haupt + 1 Akzent + 1 Basis), Tagesbonus, Nonnas Laden.

Regel der Engine: der CODE rechnet und bucht, die Daten stehen in module\\<modul>\\kuechen.json (Builder
werkzeuge\\eden_rise\\kochen_eden_rise.py). Der Garten und die Tiere stehen in kern/farm.py.
  * Vorrat: z["kueche"]["vorrat"] = {"<zutat>|<stern>": Menge}. Stern 1 gekauft, 2 gefangen/gepfluckt, 3 angebaut/gezuechtet;
    Faktor auf den Akzent-Bonus x1 / x1,5 / x2. Spielstaende ohne Kueche bekommen keinen neuen Schluessel (nur lesen).
  * Baukasten: Haupt bestimmt, wer es mag (Kategorie gegen den Geschmack der Person), Akzent den Tagesbonus (6 Effekte), Basis
    Sattigung und Heilung. Kochen laeuft ueber handel.kochen (Probe mit Kuechen-Vorteil, ein Essen am Tag, Crew-Moral +1).
  * Tagesbonus: ein Bonus gleichzeitig, gilt bis zum naechsten Dinner (Wirkpunkte: handel.preis/ankauf, kampf.attributes/
    award_xp/crit_chance).
  * Nonna: Grundzutaten dauerhaft, tierische Zutaten als knapper, teurerer Tagesvorrat; Einkauf kommt erst beim Verlassen
    des Ladens an (Frederico, feste Saetze fred.<n>)."""
import json, os, random

_CACHE = {}
STERN_FAKTOR = {1: 1.0, 2: 1.5, 3: 2.0}
PHASEN = ("fruehstueck", "tag", "nachmittag", "dinner", "abend", "nacht")
AUFSCHLAG_NONNA = 1.0           # Preise in kuechen.json gelten schon fuer Nonnas Laden (teurer als eigene Zucht)


def daten(modul):
    """module\\<modul>\\kuechen.json (nach Aenderungszeit zwischengespeichert); ohne Datei: leer."""
    pfad = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "module", modul.get("id", ""), "kuechen.json")
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
        d = {}
    _CACHE[pfad] = (mt, d)
    return d


def kueche(z):
    """Schreibender Zugriff (legt den Stand an)."""
    return z.setdefault("kueche", {"vorrat": {}, "garten": None, "staelle": {}, "bonus": None, "nonna": {}})


def _jetzt(z):
    return z["tag"] * 10 + (PHASEN.index(z["phase"]) if z.get("phase") in PHASEN else 0)


def rng(z, *salz):
    return random.Random("|".join(str(x) for x in (z.get("id"), z.get("tag")) + salz))


# ------------------------------------------------------------------ Vorrat
def schluessel(zid, stern):
    return "%s|%d" % (zid, stern)


def zerlegen(key):
    zid, _, stern = key.partition("|")
    return zid, int(stern or 1)


def vorrat_add(z, zid, stern, n=1):
    v = kueche(z)["vorrat"]
    k = schluessel(zid, stern)
    v[k] = v.get(k, 0) + n


def vorrat_menge(z, zid=None, stern=None):
    v = (z.get("kueche") or {}).get("vorrat") or {}
    return sum(n for k, n in v.items() if (zid is None or zerlegen(k)[0] == zid) and (stern is None or zerlegen(k)[1] == stern))


def vorrat_nehmen(z, key, n=1):
    v = kueche(z)["vorrat"]
    if v.get(key, 0) < n:
        raise ValueError("You don't have any of that left.")
    v[key] -= n
    if v[key] <= 0:
        del v[key]


def vorrat_ansicht(z, modul):
    d = daten(modul)
    out = []
    for key, n in sorted(((z.get("kueche") or {}).get("vorrat") or {}).items()):
        zid, stern = zerlegen(key)
        zt = (d.get("zutaten") or {}).get(zid)
        if zt:
            out.append({"key": key, "id": zid, "stern": stern, "n": n, "label": zt["label"], "rolle": zt["rolle"], "kat": zt["kat"],
                        "effekt": zt["effekt"], "text": zt["text"]})
    return out


def fang(z, modul, fid, n=1, stern=2):
    """Angeln (kern/angeln.py): ein gefangener Fisch wird zur Rohform im Vorrat, Qualitaet 2 (gefangen) oder 3 (perfekter Drill)."""
    f = next((x for x in daten(modul).get("fische", []) if x["id"] == fid), None)
    if not f:
        raise ValueError("That fish doesn't exist.")
    vorrat_add(z, f["roh"], stern, n)
    return f


# ------------------------------------------------------------------ Rohstoffe (Stall-Stufen, kern/farm.py)
def rohstoffe(z):
    """{id: Menge} - nur lesen."""
    return dict((z.get("kueche") or {}).get("rohstoffe") or {})


def rohstoff_add(z, rid, n=1):
    r = kueche(z).setdefault("rohstoffe", {})
    r[rid] = r.get(rid, 0) + n


def rohstoffe_nehmen(z, bedarf):
    """bedarf = {id: Menge}; alles oder nichts."""
    r = kueche(z).setdefault("rohstoffe", {})
    if any(r.get(k, 0) < n for k, n in bedarf.items()):
        raise ValueError("You're short of materials for that.")
    for k, n in bedarf.items():
        r[k] -= n


def rohstoffe_ansicht(z, modul):
    d = daten(modul)
    r = rohstoffe(z)
    return [{"id": k, "label": v["label"], "text": v["text"], "n": r.get(k, 0)} for k, v in (d.get("rohstoffe") or {}).items()]


# ------------------------------------------------------------------ Tagesbonus
def bonus(z, effekt):
    """Wert des aktiven Tagesbonus fuer diesen Effekt (0, wenn keiner oder abgelaufen). Nur lesen."""
    b = (z.get("kueche") or {}).get("bonus")
    if not b or b["effekt"] != effekt or _jetzt(z) > b["bis"]:
        return 0
    return b["wert"]


def bonus_ansicht(z, modul):
    b = (z.get("kueche") or {}).get("bonus")
    if not b or _jetzt(z) > b["bis"]:
        return None
    return {"effekt": b["effekt"], "wert": b["wert"], "label": (daten(modul).get("effekte") or {}).get(b["effekt"], {}).get("label", "") % b["wert"],
            "text": b.get("text", "")}


def _wert(effekt, basis, stern):
    return int(basis * STERN_FAKTOR[stern] + 0.5)          # immer ganzzahlig, damit die Anzeige stimmt (7,5 -> 8)


# ------------------------------------------------------------------ Baukasten
def gerichtname(d, basis, haupt, akzent):
    z = d["zutaten"]
    return "%s with %s on %s" % (z[haupt]["label"].replace(", raw", ""), z[akzent]["label"], z[basis]["label"])


def vorschau(z, modul, basis_key, haupt_key, akzent_key, anwesend):
    """Was kommt heraus? Nur lesen: Name, SG, Heilung, Bonus, wer es mag (Geschmack des Haupts) - fuer die Anzeige vor dem Kochen."""
    d = daten(modul)
    zt = d.get("zutaten") or {}
    (b, bs), (h, hs), (a, as_) = zerlegen(basis_key), zerlegen(haupt_key), zerlegen(akzent_key)
    if not (b in zt and h in zt and a in zt) or zt[b]["rolle"] != "basis" or zt[h]["rolle"] != "haupt" or zt[a]["rolle"] != "akzent":
        raise ValueError("Ein Gericht braucht genau eine Basis, ein Haupt und einen Akzent.")
    kat = zt[h]["kat"]
    mag = [p for p in anwesend if kat in (d["geschmack"].get(p) or {}).get("mag", [])]
    nicht = [p for p in anwesend if kat in (d["geschmack"].get(p) or {}).get("mag_nicht", [])]
    ef = zt[a]["effekt"]
    if ef == "umami":                                       # Fischsauce: niemand lehnt den Teller ab (Wirkpunkt hier, gilt nur fuer dieses Gericht)
        nicht = []
    ew = _wert(ef, d["effekte"][ef]["wert"], as_)
    label = d["effekte"][ef]["label"]
    from . import handel
    return {"name": gerichtname(d, b, h, a), "sg": zt[b]["sg"] + zt[h]["sg"], "heilt": int(zt[b]["heilt"] * STERN_FAKTOR[bs] + 0.5),
            "bonus": label % ew if "%" in label else label, "effekt": ef, "wert": ew, "mag": mag, "mag_nicht": nicht, "kat": kat,
            "mag_namen": [handel.anzeigename(modul, p) for p in mag], "mag_nicht_namen": [handel.anzeigename(modul, p) for p in nicht]}


def kochen_baukasten(z, modul, regeln, basis_key, haupt_key, akzent_key, fuer, anwesend):
    """Duc kocht aus dem Vorrat. fuer = Person-ID oder "crew" (anwesend = die Crew-Tafel bzw. die Person). -> (Titel, Zeilen)."""
    from . import chronik, handel, kampf, zustand
    for key in (basis_key, haupt_key, akzent_key):
        zid, stern = zerlegen(key)
        if vorrat_menge(z, zid, stern) < 1:
            raise ValueError("That ingredient isn't in your pantry.")
    if len({basis_key, haupt_key, akzent_key}) != 3:
        raise ValueError("Drei verschiedene Zutaten.")
    ziele = list(anwesend) if fuer == "crew" else [fuer]
    v = vorschau(z, modul, basis_key, haupt_key, akzent_key, ziele)
    item = {"id": "baukasten", "label": v["name"], "liebt": [], "mag": v["mag"], "mag_nicht": v["mag_nicht"], "hasst": [],
            "wirkung": {"sg": v["sg"]}}
    r = handel.kochen(z, modul, item, regeln, fuer, ziele if fuer == "crew" else ())
    for key in (basis_key, haupt_key, akzent_key):            # erst nach dem Kochen: bei "heute schon gegessen" bleibt alles im Vorrat
        vorrat_nehmen(z, key)
    p = r["probe"]
    kopf = {"kritisch": "A masterpiece.", "erfolg": "Well done.", "fehlschlag": "Not your day.", "patzer": "Burnt."}[p["ergebnis"]]
    zeilen = ["D20 %s + %d = %d vs DC %d · %s" % (p["wurf"], sum(b for _, b in p["boni"]), p["summe"], p["sg"], kopf)]
    lob = {"gut": "likes it", "normal": "enjoys it", "fade": "eats without much joy", "ekel": "won't touch it", "crew": "eats with you"}
    zeilen += ["%s %s" % (handel.anzeigename(modul, pid), lob.get(st, st)) for pid, st in r["stufen"].items()]
    if v["heilt"]:
        c = kampf.progress(z)
        z["lp"] = min(kampf.lp_max_duc(z), z.get("lp", kampf.lp_max_duc(z)) + v["heilt"])
        zeilen.append("Duc: +%d Life" % v["heilt"])
    if v["effekt"] == "vertrauen":                          # sofort: bei allen, die mitessen (Wirkpunkt hier)
        for pid in r["stufen"]:
            zeilen += zustand.punkte_add(z, modul, "vertrauen." + pid, v["wert"], deckel=None, quelle="geschenke")
    elif v["effekt"] != "umami":                            # die Fischsauce hat schon beim Probieren gewirkt, kein Tagesbonus
        kueche(z)["bonus"] = {"effekt": v["effekt"], "wert": v["wert"], "bis": (z["tag"] + 1) * 10 + PHASEN.index("dinner"),
                              "text": v["name"]}
        zeilen.append("Bonus until the next dinner: " + v["bonus"])
    chronik.eintragen(z, modul, "moment", "Duc cooked %s for %s." % (v["name"], "the crew" if fuer == "crew" else
                                                                      modul["personen"][fuer]["name"].split()[0]),
                      wer=list(r["stufen"]), dabei=[], wichtig=1)
    return "You cook: " + v["name"], zeilen + r["zeilen"]


# ------------------------------------------------------------------ Nonnas Laden
def nonna_offen(z, modul):
    return z.get("tag", 1) >= ((daten(modul).get("nonna") or {}).get("ab_tag", 99))


def _nonna_tag(z, modul):
    """Tagesvorrat von heute (wird beim ersten Zugriff des Tages neu gefuellt)."""
    n = kueche(z)["nonna"]
    if n.get("tag") != z["tag"]:
        n["tag"] = z["tag"]
        n["vorrat"] = dict(daten(modul)["nonna"]["tagesvorrat"], **(daten(modul).get("nonna_rohstoffe") or {}))
    return n


def _ware(d, iid):
    """Zutat oder Rohstoff aus Nonnas Laden -> (Art, Eintrag)."""
    if iid in (d.get("rohstoffe") or {}):
        return "rohstoff", d["rohstoffe"][iid]
    return "zutat", d["zutaten"][iid]


def nonna_ansicht(z, modul):
    d = daten(modul)
    if not d or not nonna_offen(z, modul):
        return None
    n = (z.get("kueche") or {}).get("nonna") or {}
    heute = n.get("vorrat") if n.get("tag") == z["tag"] else dict(d["nonna"]["tagesvorrat"], **(d.get("nonna_rohstoffe") or {}))
    waren = []
    for i in d["nonna"]["dauerhaft"]:
        w = d["zutaten"][i]
        waren.append({"id": i, "art": "zutat", "label": w["label"], "preis": w["preis"], "n": None, "text": w["text"]})
    for i, m in heute.items():
        art, w = _ware(d, i)
        waren.append({"id": i, "art": art, "label": w["label"], "preis": w["preis"], "n": m, "text": w["text"]})
    return {"waren": waren, "lieferung": [{"id": i, "n": m, "label": _ware(d, i)[1]["label"]} for i, m in (n.get("lieferung") or {}).items()]}


def nonna_kaufen(z, modul, zid, n=1):
    """Einkauf: zahlt sofort, die Ware kommt beim Verlassen des Ladens (nonna_verlassen)."""
    d = daten(modul)
    if not nonna_offen(z, modul):
        raise ValueError("Nonna isn't open yet.")
    cfg = d["nonna"]
    n = max(1, int(n))
    begrenzt = set(cfg["tagesvorrat"]) | set(d.get("nonna_rohstoffe") or {})
    if zid not in cfg["dauerhaft"] and zid not in begrenzt:
        raise ValueError("Nonna doesn't sell that.")
    st = _nonna_tag(z, modul)
    if zid in begrenzt and st["vorrat"].get(zid, 0) < n:
        raise ValueError("Nonna has none of that left today.")
    ware = _ware(d, zid)[1]
    preis = int(ware["preis"] * AUFSCHLAG_NONNA * n)
    if z["konto"] < preis:
        raise ValueError("You don't have enough money.")
    z["konto"] -= preis
    z.setdefault("buchungen", []).append({"text": "Nonna: %s x%d" % (ware["label"], n), "betrag": -preis, "tag": z["tag"]})
    if zid in begrenzt:
        st["vorrat"][zid] -= n
    l = st.setdefault("lieferung", {})
    l[zid] = l.get(zid, 0) + n
    return preis


def nonna_verlassen(z, modul):
    """Duc verlaesst den Laden: Frederico bringt den Einkauf rueber. -> Index des Satzes (fred.<n>) oder None."""
    n = (z.get("kueche") or {}).get("nonna") or {}
    if not n.get("lieferung"):
        return None
    roh = daten(modul).get("rohstoffe") or {}
    for zid, m in n["lieferung"].items():
        if zid in roh:
            rohstoff_add(z, zid, m)                       # Holz, Steine, Eisen fuer die Staelle
        else:
            vorrat_add(z, zid, 1, m)
    n["lieferung"] = {}
    saetze = daten(modul).get("frederico") or []
    if not saetze:
        return None
    i = rng(z, "fred", n.get("zaehler", 0)).randrange(len(saetze))
    n["zaehler"] = n.get("zaehler", 0) + 1
    return i


def zeile(modul, zid):
    """'fred.<n>' -> (frederico, Klartext) fuer die Vertonung (nur feste Saetze) oder (None, None)."""
    t = zid.split(".")
    s = (daten(modul).get("frederico") or [])
    if len(t) != 2 or t[0] != "fred" or not t[1].isdigit() or int(t[1]) >= len(s):
        return None, None
    return "frederico", s[int(t[1])]["text"]
