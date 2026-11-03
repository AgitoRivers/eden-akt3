# -*- coding: utf-8 -*-
"""Die Tage der Belagerung (Duc 01.11.2026, E-114): was nach einer Welle kaputt ist und wie es wieder heil wird.

Sechs Wellen auf drei Tage (kern/taktik.py). Stand zwischen den Wellen in z["belagerung"]. Je mehr in einer Welle schiefging, desto mehr
geht kaputt. Am Morgen zeigt die Bestandsaufnahme die Liste, am Tag wird geflickt: mit Holz und Stein aus dem Vorrat, im Ring-Minispiel vom
Abbauen (client/plugins/eden-abbau, Sitzung in z["abbau"] mit bau=True) oder gegen Aufschlag durch Petrus Trupp. Das Dorf bringt jeden Morgen
eine kleine Notration, damit niemand haengen bleibt. Daten: taktik.json "bestand". Wiki: docs/wiki/systeme/taktik.md, docs/wiki/welt/belagerung.md."""
from . import kuechen

STEIN = ("slate", "granite")


def stand(z):
    return z.setdefault("belagerung", {"fertig": 0, "kaputt": [], "fehler_heute": {}, "t": {}})


def _vorrat(z):
    r = kuechen.rohstoffe(z)
    return {"timber": r.get("timber", 0), "stein": sum(r.get(s, 0) for s in STEIN)}


def _hat(z, kosten):
    v = _vorrat(z)
    return all(v.get(k, 0) >= n for k, n in kosten.items())


def _nehmen(z, kosten):
    """Stein ist Stein: erst Slate, dann Granite. -> was wirklich genommen wurde, fuer die Rueckgabe."""
    if not _hat(z, kosten):
        raise ValueError("You're short of materials for that.")
    r, weg = kuechen.rohstoffe(z), {}
    for k, n in kosten.items():
        if k == "stein":
            for s in STEIN:
                m = min(n, r.get(s, 0))
                if m:
                    weg[s] = m
                    n -= m
        else:
            weg[k] = n
    kuechen.rohstoffe_nehmen(z, weg)
    return weg


def _geben(z, was):
    for k, n in was.items():
        if n:
            kuechen.rohstoff_add(z, k, n)


# ------------------------------------------------------------------ nach einer Welle
def fehler(z, D, t):
    """Wie schlecht lief die Welle: Treffer auf Kirche und Yacht, gefallene Trupps, verlorene Haeuser, zu viele Runden."""
    w, st = D["wellen"][t["welle"] - 1], t.get("start") or {}
    n = max(0, st.get("kirche", t["kirche"]) - t["kirche"]) + max(0, st.get("yacht", t["yacht"]) - t["yacht"])
    n += sum(1 for e in t["einheiten"] if e["seite"] == "blau" and not e["fest"] and e.get("ko") and not e.get("geflohen"))
    n += sum(1 for h, s in (t.get("haeuser") or {}).items() if s["status"] == "verloren" and h not in st.get("haeuser_weg", []))
    return n + max(0, t["runde"] - w.get("par", 6))


def _druck(D, w):
    """Die Fronten mit Barrikade, an denen diese Welle am staerksten kam, die staerkste zuerst."""
    zahl = {f: 0 for f in D["bestand"]["barrikaden"]}
    for _, pos in w["feinde"]:
        for f in zahl:
            if pos in D["fronten"][f]:
                zahl[f] += 1
    return sorted(zahl, key=lambda f: (-zahl[f], f))


def schaeden_eintragen(z, D, t):
    """Welle vorbei: Je mehr schiefging, desto mehr Barrikaden brechen. Kirche, Yacht und Haeuser zeigen ihren Schaden selbst."""
    b, n = stand(z), fehler(z, D, t)
    tag = str(z.get("tag", 0))
    b["fehler_heute"] = {tag: b["fehler_heute"].get(tag, 0) + n}
    brechen = 2 if n >= D["bestand"]["fehler_zwei"] else 1 if n >= D["bestand"]["fehler_eine"] else 0
    for f in _druck(D, D["wellen"][t["welle"] - 1])[:brechen]:
        if f not in b["kaputt"]:
            b["kaputt"].append(f)
    return n


# ------------------------------------------------------------------ was offen ist
def offen(z, D):
    """Die Baustellen dieses Morgens. Alles wird aus dem Stand abgeleitet, also gibt es nichts doppelt zu pflegen."""
    b, q, s = stand(z), D["bestand"], stand(z)["t"]
    aus = [dict(id="barrikade_" + f, typ="barrikade", name=q["barrikaden"][f]["name"], text=q["texte"]["barrikade"], kosten=q["kosten"]["barrikade"]) for f in b["kaputt"]]
    if s.get("kirche", 0) < s.get("kirche_max", 0):
        aus.append(dict(id="kirche", typ="kirche", name="Church Door", text=q["texte"]["kirche"], kosten=q["kosten"]["kirche"]))
    if 0 < s.get("yacht", 0) < D["yacht_lp"]:
        aus.append(dict(id="yacht", typ="yacht", name="The Yacht", text=q["texte"]["yacht"], kosten=q["kosten"]["yacht"]))
    for h in D["haeuser"]:
        if (s.get("haeuser") or {}).get(h["id"], {}).get("status") == "verloren" and "tk_haus_geflickt_" + h["id"] not in z.get("flags", []):
            aus.append(dict(id="haus_" + h["id"], typ="haus", name=h["name"], text=q["texte"]["haus"], kosten=q["kosten"]["haus"]))
    return aus


def _baustelle(z, D, bid):
    x = next((o for o in offen(z, D) if o["id"] == bid), None)
    if not x:
        raise ValueError("That doesn't need mending.")
    return x


def _wirkung(z, D, x):
    b = stand(z)
    if x["typ"] == "barrikade":
        b["kaputt"].remove(x["id"].split("_", 1)[1])
    elif x["typ"] == "kirche":
        b["t"]["kirche"] += 1
    elif x["typ"] == "yacht":
        b["t"]["yacht"] += 1
    else:
        z.setdefault("flags", []).append("tk_haus_geflickt_" + x["id"].split("_", 1)[1])
    t = z.get("taktik")
    if t:                                            # Die Kopfzeile der Karte zeigt es sofort
        t.update(kirche=b["t"].get("kirche", t["kirche"]), yacht=b["t"].get("yacht", t["yacht"]))


def notration(z, D):
    """Das Dorf bringt jeden Morgen, was es entbehren kann. Einmal je Tag."""
    b = stand(z)
    if b.get("notration_tag") == z["tag"]:
        return
    b["notration_tag"] = z["tag"]
    q = D["bestand"]["notration"]
    kuechen.rohstoff_add(z, "timber", q["timber"])
    kuechen.rohstoff_add(z, "slate", q["stein"])


def _minis_heute(z):
    b = stand(z)
    if b.get("mini_tag") != z["tag"]:
        b["mini_tag"], b["mini_n"] = z["tag"], 0
    return b["mini_n"]


def _mit_aufschlag(D, kosten):
    return dict(kosten, timber=kosten.get("timber", 0) + D["bestand"]["crew_aufschlag"])


def _kosten_sicht(z, modul, kosten):
    v, roh = _vorrat(z), kuechen.daten(modul)["rohstoffe"]
    return [{"id": k, "label": "Stone" if k == "stein" else roh[k]["label"], "n": n, "hast": v.get(k, 0)} for k, n in kosten.items()]


def ansicht(z, D, modul, darf_flicken):
    q, n = D["bestand"], sum(stand(z)["fehler_heute"].values())
    gestern = "gut" if n < q["fehler_eine"] else "schlecht" if n >= q["fehler_zwei"] else "mittel"
    frei = q["mini_max"] - _minis_heute(z)
    liste = []
    for x in offen(z, D):
        crew = _mit_aufschlag(D, x["kosten"])
        liste.append({"id": x["id"], "typ": x["typ"], "name": x["name"], "text": x["text"], "kosten": _kosten_sicht(z, modul, x["kosten"]), "crew": _kosten_sicht(z, modul, crew),
                      "geht": darf_flicken and frei > 0 and _hat(z, x["kosten"]), "crew_geht": darf_flicken and _hat(z, crew)})
    v = _vorrat(z)
    return {"flicken": darf_flicken, "offen": liste, "minis_frei": frei, "holm": q["holm"][gestern], "notration": q["notration"], "vorrat": {"timber": v["timber"], "stein": v["stein"]}}


# ------------------------------------------------------------------ flicken
def crew(z, D, bid):
    """Petrus Trupp macht es ohne Minispiel, das kostet mehr Holz."""
    x = _baustelle(z, D, bid)
    _nehmen(z, _mit_aufschlag(D, x["kosten"]))
    _wirkung(z, D, x)
    return "Petru's crew mends %s." % x["name"]


def starten(z, D, bid):
    """Ins Ring-Minispiel. Das Material ist bezahlt, sobald es losgeht, ein Abbruch gibt es zurueck."""
    x = _baustelle(z, D, bid)
    if _minis_heute(z) >= D["bestand"]["mini_max"]:
        raise ValueError("You've got no strength left today. Petru's crew can do the rest.")
    z["abbau"] = {"bau": True, "id": bid, "typ": x["typ"], "name": x["name"], "bezahlt": _nehmen(z, x["kosten"]), "noetig": D["bestand"]["treffer"], "treffer": 0, "perfekt": 0, "fehl": 0, "geschafft": [], "zurueck": "taktik"}
    z["status"] = "abbau"


def schlag(z, D, ergebnis):
    s = z["abbau"]
    if s["geschafft"]:
        raise ValueError("That part is done.")
    if ergebnis == "daneben":
        s["fehl"] += 1
        return
    if ergebnis not in ("perfekt", "gut"):
        raise ValueError("Unknown swing.")
    s["treffer"] += 1
    s["perfekt"] += ergebnis == "perfekt"
    if s["treffer"] < s["noetig"]:
        return
    x = _baustelle(z, D, s["id"])
    zurueck = min(s["perfekt"], D["bestand"]["perfekt_spart"], s["bezahlt"].get("timber", 0))     # Sauberes Arbeiten spart Holz (Duc 01.11.2026)
    _geben(z, {"timber": zurueck})
    _wirkung(z, D, x)
    stand(z)["mini_n"] = _minis_heute(z) + 1
    s["geschafft"].append({"typ": s["typ"], "label": x["name"], "perfekt": s["perfekt"] >= s["noetig"], "ertrag": [{"id": "timber", "label": "Timber saved", "n": zurueck}] if zurueck else [], "liegen": []})


def ende(z):
    """Zurueck zur Liste. Wer abbricht, bekommt sein Material zurueck und hat nichts verbraucht."""
    s = z.pop("abbau")
    z["status"] = s["zurueck"]
    if s["geschafft"]:
        return "%s is mended." % s["name"]
    _geben(z, s["bezahlt"])
    return None


def bau_ansicht(z, D, modul):
    """Dieselbe Form wie kern/abbau.ansicht, der Client spielt denselben Ring."""
    s, ring = z["abbau"], kuechen.daten(modul)["abbau"]["ring"]
    plus = max(0, min(3, ((z.get("persona") or {}).get("attribute") or {}).get("strength", 2) - 2))
    return {"bau": True, "art": "bau", "typ": s["typ"], "label": s["name"], "platz": s["id"], "frame": None, "noetig": s["noetig"], "direkt": False, "treffer": s["treffer"], "nr": len(s["geschafft"]),
            "werkzeug": {"id": "hammer", "label": "Hammer and nails", "stufe": 1, "bild": ""}, "knoten": [{"typ": s["typ"], "bild": None, "label": s["name"], "sprite": None}], "geschafft": s["geschafft"], "fehl": s["fehl"], "voll": False,
            "ring": {"dauer": ring["dauer"], "schneller": ring["schneller"], "gut_ms": ring["gut_ms"], "perfekt_ms": ring["perfekt_ms"] + ring["kraft_ms"] * plus}, "rohstoffe": kuechen.rohstoffe_ansicht(z, modul),
            "bild": D["bestand"]["bilder"].get(s["typ"])}
