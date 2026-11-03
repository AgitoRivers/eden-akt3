# -*- coding: utf-8 -*-
"""Farm bei Nonna (Duc 27.10.2026, E-079): Garten und drei Staelle (Chicken, Pig, Cow) - das Spiel rechnet, die Zahlen stehen in
module\\<modul>\\kuechen.json (Builder werkzeuge\\eden_rise\\kochen_eden_rise.py), Vorrat und Laden in kern/kuechen.py.
  * Garten: 4 Beete, pflanzen (Saatgeld) kostet keine Phase; Ernte am naechsten Morgen in den Vorrat, Qualitaet 3 (selbst angebaut).
  * Staelle: je Art ein Stall (Upgrade, Einmalpreis), Tiere als Babys kaufen. Stufen: 1 Baby, 2 erwachsen (Maennchen/Weibchen),
    3 alt - nach Alter in Tagen. Stufe 2 liefert (Huehner: Eier vom Weibchen, Schweine: Trueffel, Kuehe: Milch vom Weibchen),
    Stufe 3 liefert nichts mehr und kann geschlachtet werden (Fleisch, Qualitaet 3). Ein erwachsenes Paar bekommt nach der
    Zuchtzeit ein Baby, solange im Stall Platz ist. Neue Tiere kann man benennen.
  * Ablauf: kern/plan -> eden.weiter (Tageswechsel) ruft tagesbeginn(); Spielstaende ohne Farm bekommen keinen neuen Schluessel."""
import re

from . import kuechen

NAME_MAX = 16
NAME_MUSTER = re.compile(r"^[A-Za-z][A-Za-z '\-]{0,15}$")


def _garten(z, modul):
    k = kuechen.kueche(z)
    if k["garten"] is None:
        k["garten"] = [None] * kuechen.daten(modul)["beete"]
    return k["garten"]


def _bezahlen(z, preis, text):
    if z["konto"] < preis:
        raise ValueError("You don't have enough money.")
    z["konto"] -= preis
    z.setdefault("buchungen", []).append({"text": text, "betrag": -preis, "tag": z["tag"]})


def _offen(z, modul):
    if not kuechen.nonna_offen(z, modul):
        raise ValueError("Nonna isn't open yet.")


# ------------------------------------------------------------------ Garten
def garten_pflanzen(z, modul, beet, pflanze):
    d = kuechen.daten(modul)
    _offen(z, modul)
    if pflanze not in d["pflanzen"] or (d["pflanzen"][pflanze].get("flag") and d["pflanzen"][pflanze]["flag"] not in z["flags"]):
        raise ValueError("That doesn't grow here.")
    g = _garten(z, modul)
    if not 0 <= beet < len(g):
        raise ValueError("That bed doesn't exist.")
    if g[beet]:
        raise ValueError("Something is already growing in that bed.")
    p = d["pflanzen"][pflanze]
    _bezahlen(z, p["preis"], "Seeds: %s" % d["zutaten"][pflanze]["label"])
    g[beet] = {"pflanze": pflanze, "tag": z["tag"]}
    if p.get("merkt"):                                      # Zitronengras: Nonna merkt es am naechsten Tag (Szene g1_zg_zitronengras)
        if p["merkt"] not in z["flags"]:
            z["flags"].append(p["merkt"])
        z.setdefault("flag_tag", {}).setdefault(p["merkt"], z["tag"])


def garten_ansicht(z, modul):
    d = kuechen.daten(modul)
    g = (z.get("kueche") or {}).get("garten") or [None] * d["beete"]
    out = []
    for i, b in enumerate(g):
        if not b:
            out.append({"beet": i, "leer": True})
            continue
        p = d["pflanzen"][b["pflanze"]]
        rest = max(0, b["tag"] + p["tage"] - z["tag"])
        out.append({"beet": i, "leer": False, "pflanze": b["pflanze"], "label": d["zutaten"][b["pflanze"]]["label"],
                    "rest": rest, "ertrag": p["ertrag"]})
    return out


def _ernten(z, modul):
    d = kuechen.daten(modul)
    zeilen = []
    g = (z.get("kueche") or {}).get("garten")
    for i, b in enumerate(g or []):
        if b and z["tag"] >= b["tag"] + d["pflanzen"][b["pflanze"]]["tage"]:
            p = d["pflanzen"][b["pflanze"]]
            kuechen.vorrat_add(z, b["pflanze"], 3, p["ertrag"])
            zeilen.append("Garden: %d × %s are ready, in your pantry." % (p["ertrag"], d["zutaten"][b["pflanze"]]["label"]))
            g[i] = None
    return zeilen


# ------------------------------------------------------------------ Tiere
def stufe(t, tier, tag):
    alter = tag - tier["geboren"]
    return 1 if alter < t["baby_tage"] else 2 if alter < t["baby_tage"] + t["erwachsen_tage"] else 3


def variante(t, tier, tag):
    s = stufe(t, tier, tag)
    return "baby" if s == 1 else ("adult_" if s == 2 else "old_") + tier["geschlecht"]


def _stall(z, art):
    return ((z.get("kueche") or {}).get("staelle") or {}).get(art)


def stufe_def(d, art, stall):
    """Werte der aktuellen Stall-Stufe (1-3): Plaetze, +Menge je Produkt, Zucht schneller."""
    st = d["stall_stufen"][art]
    s = st[min(len(st), (stall or {}).get("stufe", 1)) - 1]
    return {"plaetze": s["plaetze"], "menge_plus": s.get("menge_plus", 0), "zucht_minus": s.get("zucht_minus", 0)}


def _bauen(z, d, art, stufe, text):
    s = d["stall_stufen"][art][stufe - 1]
    if z["konto"] < s["geld"]:
        raise ValueError("You don't have enough money.")
    kuechen.rohstoffe_nehmen(z, s["rohstoffe"])                 # alles oder nichts, vor dem Bezahlen geprueft
    _bezahlen(z, s["geld"], text)


def stall_kaufen(z, modul, art):
    d = kuechen.daten(modul)
    _offen(z, modul)
    if art not in d["tiere"]:
        raise ValueError("That shed doesn't exist.")
    if _stall(z, art):
        raise ValueError("You already have that shed.")
    _bauen(z, d, art, 1, "Nonna: %s shed" % d["tiere"][art]["label"].lower())
    kuechen.kueche(z)["staelle"][art] = {"tiere": [], "naechste_id": 1, "letzte_geburt": z["tag"], "stufe": 1}


def stall_ausbauen(z, modul, art):
    """Naechste Stufe (2, dann 3): Geld + Rohstoffe. -> neue Stufe."""
    d = kuechen.daten(modul)
    _offen(z, modul)
    s = _stall(z, art)
    if not s:
        raise ValueError("You need the shed first.")
    neu = s.get("stufe", 1) + 1
    if neu > len(d["stall_stufen"][art]):
        raise ValueError("The shed is already fully upgraded.")
    _bauen(z, d, art, neu, "Nonna: %s shed, level %d" % (d["tiere"][art]["label"].lower(), neu))
    s["stufe"] = neu
    if all((_stall(z, a) or {}).get("stufe", 0) >= len(d["stall_stufen"][a]) for a in d["tiere"]) \
            and "farm_voll" not in z.setdefault("flags", []):
        z["flags"].append("farm_voll")                # alle Staelle voll ausgebaut: Fredericos Loewe (Charm, 28.10.2026)
    return neu


def _name_vorschlag(t, stall):
    benutzt = {x["name"] for x in stall["tiere"]}
    frei = [n for n in t["namen"] if n not in benutzt]
    return frei[0] if frei else "%s %d" % (t["label"], stall["naechste_id"])


def _neues_tier(z, t, art, stall, geschlecht):
    tier = {"id": stall["naechste_id"], "art": art, "name": _name_vorschlag(t, stall), "geschlecht": geschlecht,
            "geboren": z["tag"], "neu": True}
    stall["naechste_id"] += 1
    stall["tiere"].append(tier)
    return tier


def tier_kaufen(z, modul, art):
    d = kuechen.daten(modul)
    _offen(z, modul)
    s = _stall(z, art)
    if not s:
        raise ValueError("You need the shed first.")
    t = d["tiere"][art]
    if len(s["tiere"]) >= stufe_def(d, art, s)["plaetze"]:
        raise ValueError("The shed is full.")
    _bezahlen(z, t["baby_preis"], "Nonna: baby %s" % t["label"].lower())
    w = sum(1 for x in s["tiere"] if x["geschlecht"] == "f")
    return _neues_tier(z, t, art, s, "f" if w <= len(s["tiere"]) - w else "m")        # ausgleichen, erstes Tier ein Weibchen


def tier_finden(z, art, tid):
    s = _stall(z, art)
    tier = next((x for x in (s or {}).get("tiere", []) if x["id"] == tid), None)
    if not tier:
        raise ValueError("That animal doesn't exist.")
    return s, tier


def tier_benennen(z, modul, art, tid, name):
    name = (name or "").strip()
    if not NAME_MUSTER.match(name):
        raise ValueError("Ein Name hat 1 bis 16 Buchstaben.")
    _, tier = tier_finden(z, art, tid)
    tier["name"], tier["neu"] = name, False


def tier_schlachten(z, modul, art, tid):
    d = kuechen.daten(modul)
    s, tier = tier_finden(z, art, tid)
    t = d["tiere"][art]
    if stufe(t, tier, z["tag"]) != 3:
        raise ValueError("Only old animals can be slaughtered.")
    s["tiere"].remove(tier)
    f = t["fleisch"]
    kuechen.vorrat_add(z, f["art"], 3, f["menge"])
    return ["%s is gone. %d × %s in your pantry." % (tier["name"], f["menge"], d["zutaten"][f["art"]]["label"])]


# ------------------------------------------------------------------ Tageswechsel
def tagesbeginn(z, modul):
    """Neuer Morgen: Ernte, Eier/Trueffel/Milch der erwachsenen Tiere, Geburten. -> Zeilen fuer die Tagesmeldung."""
    d = kuechen.daten(modul)
    if not d or not z.get("kueche"):
        return []
    zeilen = _ernten(z, modul)
    for art, s in (z["kueche"].get("staelle") or {}).items():
        t = d["tiere"][art]
        pr = t["produkt"]
        sd = stufe_def(d, art, s)
        for tier in s["tiere"]:
            tage2 = (z["tag"] - tier["geboren"]) - t["baby_tage"]
            if stufe(t, tier, z["tag"]) == 2 and tage2 >= 1 and tage2 % pr["alle_tage"] == 0 and (pr["wer"] == "alle" or tier["geschlecht"] == "f"):
                menge = pr["menge"] + sd["menge_plus"]
                kuechen.vorrat_add(z, pr["art"], 3, menge)
                zeilen.append("%s (%s) gave %d × %s." % (tier["name"], t["label"].lower(), menge, d["zutaten"][pr["art"]]["label"]))
        erw = [x for x in s["tiere"] if stufe(t, x, z["tag"]) == 2]
        if (any(x["geschlecht"] == "m" for x in erw) and any(x["geschlecht"] == "f" for x in erw)
                and len(s["tiere"]) < sd["plaetze"] and z["tag"] - s["letzte_geburt"] >= max(1, t["zucht_tage"] - sd["zucht_minus"])):
            geschlecht = "f" if kuechen.rng(z, art, "geburt").random() < 0.5 else "m"
            baby = _neues_tier(z, t, art, s, geschlecht)
            s["letzte_geburt"] = z["tag"]
            zeilen.append("A baby %s was born! Give %s a name." % (t["label"].lower(), "her" if geschlecht == "f" else "him"))
    return zeilen


# ------------------------------------------------------------------ Ansicht
def ansicht(z, modul):
    """Alles fuer das Farm-Fenster (nur lesen). None, wenn Nonna noch nicht offen ist."""
    d = kuechen.daten(modul)
    if not d or not kuechen.nonna_offen(z, modul):
        return None
    staelle = []
    for art, t in d["tiere"].items():
        s = _stall(z, art)
        tiere = []
        for tier in (s or {}).get("tiere", []):
            st = stufe(t, tier, z["tag"])
            v = variante(t, tier, z["tag"])
            tiere.append({"id": tier["id"], "name": tier["name"], "geschlecht": tier["geschlecht"], "stufe": st, "variante": v,
                          "sprite": "/farm/tiere/%s_%s.png" % (art, v), "groesse": d["tier_groesse"][art][v],
                          "schlachtbar": st == 3, "neu": bool(tier.get("neu")),
                          "bringt": st == 2 and (t["produkt"]["wer"] == "alle" or tier["geschlecht"] == "f")})
        stufen = d["stall_stufen"][art]
        stall_stufe = (s or {}).get("stufe", 1) if s else 0
        roh = kuechen.rohstoffe(z)

        def kosten(i):                                     # Stufe i (1-3) -> Anzeige mit "reicht es?"
            k = stufen[i - 1]
            return {"stufe": i, "geld": k["geld"], "text": k["text"], "plaetze": k["plaetze"],
                    "rohstoffe": [{"id": r, "label": d["rohstoffe"][r]["label"], "n": n, "hast": roh.get(r, 0)} for r, n in k["rohstoffe"].items()],
                    "geht": z["konto"] >= k["geld"] and all(roh.get(r, 0) >= n for r, n in k["rohstoffe"].items())}
        staelle.append({"art": art, "label": t["label"], "rasse": t["rasse"], "gekauft": bool(s), "stufe": stall_stufe, "stufe_max": len(stufen),
                        "baby_preis": t["baby_preis"], "plaetze": stufe_def(d, art, s)["plaetze"] if s else stufen[0]["plaetze"],
                        "tiere": tiere, "laut": d["tier_laut"][art],
                        "naechste": kosten(stall_stufe + 1) if stall_stufe < len(stufen) else None,
                        "produkt": d["zutaten"][t["produkt"]["art"]]["label"], "fleisch": d["zutaten"][t["fleisch"]["art"]]["label"]})
    return {"garten": garten_ansicht(z, modul), "staelle": staelle, "konto": z["konto"], "rohstoffe": kuechen.rohstoffe_ansicht(z, modul),
            "pflanzen": [{"id": i, "label": d["zutaten"][i]["label"], "preis": p["preis"], "ertrag": p["ertrag"], "tage": p["tage"]}
                         for i, p in d["pflanzen"].items() if not p.get("flag") or p["flag"] in z["flags"]]}
