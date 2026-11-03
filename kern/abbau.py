# -*- coding: utf-8 -*-
"""Quellen an Rastplaetzen und Abbauen (Duc 28.10.2026): Holz, Stein und Wasser an den Rastplaetzen der Expeditionen.

Regel der Engine: der CODE entscheidet, was dort steht (Baumart, Fels), und bucht den Ertrag; das Ring-Minispiel laeuft im Client
(client/plugins/eden-abbau) und meldet je Schlag nur perfekt/gut/daneben. Daten in kuechen.json (abbau, werkzeuge; Builder
werkzeuge/eden_rise/kochen_eden_rise.py aus kochen_daten.py).

  * Quelle: je Platz (ein oder mehrere Frames desselben Ortes) und Art (holz, stein, wasser) ein Bestand von `menge` Baeumen/
    Felsen bzw. Wuerfen. Kein Zeitpreis: man baut ab, bis sie leer ist; dann ist sie `pause` Tage erschoepft und waechst nach.
    Stand in z["kueche"]["quellen"][platz][art] = {"rest": n} oder {"leer_tag": t}.
  * Werkzeug (Petrus Werkstatt ab Tag 2): Axt fuer Holz, Spitzhacke fuer Stein, Stufe 0-3 in z["kueche"]["werkzeug"].
    Stufe 1 = 3 Ring-Treffer je Baum/Fels, Stufe 2 = 1 Treffer, Stufe 3 = direkt (ein Klick, zaehlt als perfekt).
  * Ertrag je Knoten (Steineiche 2 Timber, Korkeiche 2 Timber + 1 Cork, Fels 2 Stone); perfekter letzter Schlag +1 auf den ersten
    Rohstoff. Kraft ueber 2 verbreitert das Perfekt-Fenster (Client, Wert kommt von hier).
  * Angeln an einem Wasser-Platz laeuft ueber kern/angeln.py und zieht je Wurf eins vom Bestand (nehmen).
  * Stapeln (Duc 28.10.2026): auf der Expedition geht der Ertrag in die Tasche (kern/expedition.py ernte, Rohstoffe 10 je
    Platz); was nicht mehr passt, bleibt liegen. Ist kein Platz fuer den Hauptrohstoff, zeigt der Chip "bag full".
Spielstaende ohne Kueche bekommen beim Lesen keinen neuen Schluessel."""
import os

from . import kuechen

ARTEN = ("holz", "stein", "wasser")
ERGEBNISSE = ("perfekt", "gut", "daneben")
ART_WERKZEUG = {"holz": "axe", "stein": "pickaxe"}


def _d(modul):
    return kuechen.daten(modul).get("abbau") or {}


def platz(modul, pid):
    return (_d(modul).get("quellen") or {}).get(pid)


def platz_von_frame(modul, frame):
    """Rastplatz-Frame -> Platz-ID (oder None, wenn der Frame keine Quelle hat)."""
    return next((pid for pid, q in (_d(modul).get("quellen") or {}).items() if frame in q["frames"]), None)


def menge(modul, art):
    return kuechen.daten(modul)["angeln"]["wuerfe"] if art == "wasser" else _d(modul)["menge"]


def stand(z, modul, pid, art):
    """-> (rest, wieder_am_tag): rest > 0 = abbaubar; sonst der Tag, an dem die Quelle nachgewachsen ist. Nur lesen."""
    q = (((z.get("kueche") or {}).get("quellen") or {}).get(pid) or {}).get(art)
    if not q:
        return menge(modul, art), None
    if q.get("leer_tag") is not None:
        wieder = q["leer_tag"] + _d(modul)["pause"]
        return (menge(modul, art), None) if z["tag"] >= wieder else (0, wieder)
    return q["rest"], None


def nehmen(z, modul, pid, art, n=1):
    """Eins (oder n) vom Bestand; leer -> erschoepft ab heute."""
    rest, wieder = stand(z, modul, pid, art)
    if rest < n:
        raise ValueError("There's nothing left to gather here right now.")
    qs = kuechen.kueche(z).setdefault("quellen", {}).setdefault(pid, {})
    qs[art] = {"rest": rest - n} if rest - n > 0 else {"leer_tag": z["tag"]}


def werkzeug_stufe(z, wid):
    return ((z.get("kueche") or {}).get("werkzeug") or {}).get(wid, 0)


def _kraft(z):
    return ((z.get("persona") or {}).get("attribute") or {}).get("strength", 2)


def haupt_rohstoff(modul, art):
    """Der erste Ertrag der Knoten dieser Art (holz -> timber, stein -> granite)."""
    return next(iter(next(k for k in _d(modul)["knoten"].values() if k["art"] == art)["ertrag"]))


def tasche_voll(z, modul, art):
    """Unterwegs kein Platz mehr fuer das, was hier herauskommt (holz/stein: keiner der Rohstoffe passt, wasser: irgendein Fisch)?"""
    from . import expedition
    if not expedition.unterwegs(z):
        return False
    if art == "wasser":
        return not expedition.fisch_platz(z, modul)
    ids = {r for k in _d(modul)["knoten"].values() if k["art"] == art for r in k["ertrag"]}
    return all(expedition.ernte_frei(z, modul, "roh", r) < 1 for r in ids)


def quellen_ansicht(z, modul, frame):
    """Chips am Rastplatz: je Art Bestand, Nachwuchs-Tage oder fehlendes Werkzeug. [] ohne Quelle."""
    pid = platz_von_frame(modul, frame)
    if not pid:
        return []
    q, w = platz(modul, pid), kuechen.daten(modul).get("werkzeuge") or {}
    out = []
    for art in ARTEN:
        if not q.get(art):
            continue
        rest, wieder = stand(z, modul, pid, art)
        c = {"art": art, "platz": pid, "rest": rest, "menge": menge(modul, art), "in_tagen": (wieder - z["tag"]) if wieder else 0,
             "wasser": q["wasser"] if art == "wasser" else None, "voll": tasche_voll(z, modul, art),
             # Kreis am Rastplatz (Duc 30.10.2026): das Angelbild des Platzes bzw. was hier am meisten steht
             "bild": "/bg/%s" % q.get("angel_bild_datei") if art == "wasser" else "/farm/abbau/kreis_%s.png" % max(q[art], key=q[art].get)}
        wid = ART_WERKZEUG.get(art)
        if wid and not werkzeug_stufe(z, wid):
            c["fehlt"] = w[wid]["label"]
        elif wid:
            c["werkzeug"] = {"id": wid, "stufe": werkzeug_stufe(z, wid), "label": w[wid]["stufen"][werkzeug_stufe(z, wid) - 1]["label"]}
        out.append(c)
    return out


# ------------------------------------------------------------------ Abbau-Sitzung
def _knoten(z, modul, pid, art, n):
    """Was an diesem Platz steht (fest je Tag und Platz, Neuladen aendert nichts)."""
    mix = platz(modul, pid)[art]
    r = kuechen.rng(z, "abbau", pid, art)
    arten = list(mix)
    return [r.choices(arten, weights=[mix[k] for k in arten])[0] for _ in range(n)][-n:]


def _sitzung(z):
    s = z.get("abbau")
    if not s or z.get("status") != "abbau":
        raise ValueError("You aren't gathering anything right now.")
    return s


def starten(z, modul, frame, art):
    """Am offenen Rastplatz-Frame (Status ereignis) mit Axt oder Spitzhacke beginnen."""
    if z.get("status") != "ereignis":
        raise ValueError("You can only gather at a rest site.")
    if art not in ART_WERKZEUG:
        raise ValueError("You can't gather that.")
    pid = platz_von_frame(modul, frame)
    q = platz(modul, pid) if pid else None
    if not q or not q.get(art):
        raise ValueError("There's none of that here.")
    wid = ART_WERKZEUG[art]
    st = werkzeug_stufe(z, wid)
    if not st:
        raise ValueError("You need a tool for that first – Petru has some.")
    rest, _ = stand(z, modul, pid, art)
    if not rest:
        raise ValueError("Nothing more to gather here for a few days.")
    if tasche_voll(z, modul, art):
        raise ValueError("Your bag is full – no room for more %s." % kuechen.daten(modul)["rohstoffe"][haupt_rohstoff(modul, art)]["label"])
    wz = kuechen.daten(modul)["werkzeuge"][wid]["stufen"][st - 1]
    z["abbau"] = {"platz": pid, "art": art, "frame": frame, "werkzeug": wid, "stufe": st, "noetig": max(1, wz["treffer"]),
                  "direkt": wz["treffer"] == 0, "knoten": _knoten(z, modul, pid, art, rest), "nr": 0, "treffer": 0,
                  "fehl": 0, "geschafft": [], "zurueck": z["status"]}
    z["status"] = "abbau"


def schlag(z, modul, ergebnis):
    """Ein Schlag im Ring: perfekt / gut / daneben. Der letzte noetige Treffer faellt den Baum bzw. bricht den Fels und bucht den
    Ertrag (perfekt: +1; unterwegs in die Tasche, der Rest bleibt liegen).
    -> {"fertig": bool, "eintrag": {...} oder None, "voll": Tasche danach voll}"""
    from . import expedition
    s = _sitzung(z)
    if ergebnis not in ERGEBNISSE:
        raise ValueError("Unknown swing.")
    if s["nr"] >= len(s["knoten"]):
        raise ValueError("There's nothing left standing here.")
    if s["direkt"]:
        ergebnis = "perfekt"                           # Stufe 3: der Baum faellt einfach
    if ergebnis == "daneben":
        s["fehl"] += 1
        return {"fertig": False, "eintrag": None}
    s["treffer"] += 1
    if s["treffer"] < s["noetig"]:
        return {"fertig": False, "eintrag": None}
    d = _d(modul)
    typ = s["knoten"][s["nr"]]
    kn = d["knoten"][typ]
    ertrag = dict(kn["ertrag"])
    if ergebnis == "perfekt":
        erster = next(iter(kn["ertrag"]))
        ertrag[erster] += d["perfekt_plus"]
    roh = kuechen.daten(modul)["rohstoffe"]
    genommen, liegen = {}, []
    for rid, n in ertrag.items():
        genommen[rid] = expedition.ernte_roh(z, modul, rid, n)
        if genommen[rid] < n:
            liegen.append({"id": rid, "label": roh[rid]["label"], "n": n - genommen[rid]})
    nehmen(z, modul, s["platz"], s["art"])
    e = {"typ": typ, "label": kn["label"], "perfekt": ergebnis == "perfekt",
         "ertrag": [{"id": rid, "label": roh[rid]["label"], "n": n} for rid, n in genommen.items() if n], "liegen": liegen}
    s["geschafft"].append(e)
    s["nr"] += 1
    s["treffer"] = 0
    return {"fertig": True, "eintrag": e, "voll": tasche_voll(z, modul, s["art"])}


def ende(z, modul):
    """Zurueck an den Rastplatz. -> Zeilen fuer die Meldung (leer, wenn nichts gefallen ist)."""
    s = _sitzung(z)
    z.pop("abbau", None)
    z["status"] = s.get("zurueck") or "ereignis"
    if not s["geschafft"]:
        return []
    summe, weg = {}, {}
    for e in s["geschafft"]:
        for r in e["ertrag"]:
            summe[r["label"]] = summe.get(r["label"], 0) + r["n"]
        for r in e.get("liegen") or []:
            weg[r["label"]] = weg.get(r["label"], 0) + r["n"]
    was = {"holz": ("tree", "trees"), "stein": ("rock", "rocks")}[s["art"]]
    n = len(s["geschafft"])
    zeilen = ["%d %s %s – %s." % (n, was[0] if n == 1 else was[1], "worked" if s["art"] == "holz" else "down", ", ".join("+%d %s" % (v, k) for k, v in summe.items()) or "nothing fit in the bag")]
    if weg:
        zeilen.append("Left behind, the bag was full: %s." % ", ".join("%d %s" % (v, k) for k, v in weg.items()))
    return zeilen


def _knoten_bild(modul, t, d, bild):
    """Sprite eines Knotens. Gibt es <bild>_vorher.png (Korkeiche mit voller Rinde, Duc 29.10.2026), steht der Baum so da und
    wechselt beim letzten Treffer auf <bild>.png (geschaelt, deckungsgleich, werkzeuge/kork_rinde_bild.py)."""
    k = {"typ": t, "bild": bild, "label": d["knoten"][t]["label"], "sprite": "/farm/abbau/%s.png" % bild}
    vorher = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "module", modul.get("id", ""),
                          "farm", "abbau", bild + "_vorher.png")
    if os.path.isfile(vorher):                         # Rinde: faellt beim letzten Hieb herunter (Duc 30.10.2026)
        k.update(sprite="/farm/abbau/%s_vorher.png" % bild, sprite_nach=k["sprite"] + "?v=2", sprite_rinde="/farm/abbau/%s_rinde.png" % bild)
    return k


def _knoten_bilder(z, modul, s, d):
    """Welches Bild jeder Knoten zeigt (Duc 30.10.2026): fest je Tag und Platz, gleiche Art wechselt der Reihe nach durch ihre Bilder."""
    r = kuechen.rng(z, "abbau_bild", s["platz"], s["art"])
    start, gezaehlt, out = {}, {}, []
    for t in s["knoten"]:
        bilder = d["knoten"][t].get("bilder") or [t]
        versatz = start.setdefault(t, r.randrange(len(bilder)))
        gezaehlt[t] = gezaehlt.get(t, 0) + 1
        out.append(_knoten_bild(modul, t, d, bilder[(versatz + gezaehlt[t] - 1) % len(bilder)]))
    return out


def ansicht(z, modul, bild_fn=None):
    s = z.get("abbau")
    if not s:
        return None
    d = _d(modul)
    w = kuechen.daten(modul)["werkzeuge"][s["werkzeug"]]
    ring = d["ring"]
    plus = max(0, min(3, _kraft(z) - 2))
    return {"platz": s["platz"], "label": platz(modul, s["platz"])["label"], "art": s["art"], "frame": s["frame"],
            "werkzeug": {"id": s["werkzeug"], "label": w["stufen"][s["stufe"] - 1]["label"], "stufe": s["stufe"],
                         "bild": "/itembild/%s_%d" % (s["werkzeug"], s["stufe"])},
            "noetig": s["noetig"], "direkt": s["direkt"], "treffer": s["treffer"], "nr": s["nr"],
            "knoten": _knoten_bilder(z, modul, s, d),
            "geschafft": s["geschafft"], "fehl": s["fehl"], "voll": tasche_voll(z, modul, s["art"]),
            "ring": {"dauer": ring["dauer"], "schneller": ring["schneller"], "gut_ms": ring["gut_ms"],
                     "perfekt_ms": ring["perfekt_ms"] + ring["kraft_ms"] * plus},
            "rohstoffe": kuechen.rohstoffe_ansicht(z, modul)}


# ------------------------------------------------------------------ Petrus Werkstatt: Werkzeuge
def petru_kalt(z):
    """Nach Weg B in den Bergen (29.10.2026): Petru hat Duc aus der Werkstatt geworfen - der Laden bleibt offen, aber kalt,
    bis Laetitias Karte und die Versoehnung kommen (Flag petru_versoehnt)."""
    f = z.get("flags") or []
    return "petru_werkstatt_zu_duc" in f and "petru_versoehnt" not in f


def petru_offen(z, modul):
    return z.get("tag", 1) >= (kuechen.daten(modul).get("petru") or {}).get("ab_tag", 2)


def _fisch_key(z, fid):
    """Vorrats-Schluessel eines gefangenen Fisches (Rohform), schlechteste Qualitaet zuerst - oder None."""
    v = (z.get("kueche") or {}).get("vorrat") or {}
    keys = sorted((k for k, n in v.items() if n > 0 and kuechen.zerlegen(k)[0] == fid + "_roh"), key=lambda k: kuechen.zerlegen(k)[1])
    return keys[0] if keys else None


def _gesperrt(z, s):
    if s.get("rosi") and "werkstatt_offen" not in (z.get("flags") or []):
        return "Rosi has to harden the steel, and her workshop isn't running yet."
    if s.get("vertrauen") and z["werte"].get("vertrauen.petru", 0) < s["vertrauen"]:
        return "Petru only forges this for someone he trusts (trust %d)." % s["vertrauen"]
    return None


def werkzeug_ansicht(z, modul):
    d = kuechen.daten(modul)
    if not d.get("werkzeuge"):
        return None
    roh, fische = kuechen.rohstoffe(z), {f["id"]: f for f in d["fische"]}
    out = []
    for wid, w in d["werkzeuge"].items():
        st = werkzeug_stufe(z, wid)
        x = {"id": wid, "label": w["label"], "art": w["art"], "stufe": st,
             "jetzt": dict(w["stufen"][st - 1], bild="/itembild/%s_%d" % (wid, st)) if st else None, "naechste": None}
        if st < len(w["stufen"]):
            s = w["stufen"][st]
            f = fische.get(s["fisch"]) if s["fisch"] else None
            x["naechste"] = {"stufe": st + 1, "label": s["label"], "text": s["text"], "treffer": s["treffer"], "geld": s["geld"],
                             "bild": "/itembild/%s_%d" % (wid, st + 1),
                             "rohstoffe": [{"id": r, "label": d["rohstoffe"][r]["label"], "n": n, "hast": roh.get(r, 0)}
                                           for r, n in s["rohstoffe"].items()],
                             "fisch": {"id": f["id"], "label": f["label"], "hast": bool(_fisch_key(z, f["id"]))} if f else None,
                             "gesperrt": _gesperrt(z, s)}
            n = x["naechste"]
            n["geht"] = (not n["gesperrt"] and z["konto"] >= s["geld"] and all(r["hast"] >= r["n"] for r in n["rohstoffe"])
                         and (not f or n["fisch"]["hast"]))
        out.append(x)
    return out


def werkzeug_kaufen(z, modul, wid):
    """Naechste Stufe bei Petru: Geld, Rohstoffe und (ab Stufe 2) der Wunschfisch aus dem Vorrat - alles oder nichts.
    -> (Zeilen, Zeilen-Gruppe fuer Petrus Uebergabesatz)"""
    d = kuechen.daten(modul)
    if not petru_offen(z, modul):
        raise ValueError("Petru's workshop isn't open yet.")
    w = (d.get("werkzeuge") or {}).get(wid)
    if not w:
        raise ValueError("That tool doesn't exist.")
    st = werkzeug_stufe(z, wid)
    if st >= len(w["stufen"]):
        raise ValueError("It doesn't get any better than this.")
    s = w["stufen"][st]
    grund = _gesperrt(z, s)
    if grund:
        raise ValueError(grund)
    if z["konto"] < s["geld"]:
        raise ValueError("You don't have enough money.")
    if any(kuechen.rohstoffe(z).get(r, 0) < n for r, n in s["rohstoffe"].items()):
        raise ValueError("You're short of materials for that.")
    fkey = _fisch_key(z, s["fisch"]) if s["fisch"] else None
    if s["fisch"] and not fkey:
        raise ValueError("Petru wants a fish for this that you don't have.")
    kuechen.rohstoffe_nehmen(z, s["rohstoffe"])
    if fkey:
        kuechen.vorrat_nehmen(z, fkey)
    if s["geld"]:
        z["konto"] -= s["geld"]
        z.setdefault("buchungen", []).append({"text": "Petru: %s" % s["label"], "betrag": -s["geld"], "tag": z["tag"]})
    kuechen.kueche(z).setdefault("werkzeug", {})[wid] = st + 1
    treffer = {3: "three good blows", 1: "one good blow", 0: "a single swing"}[s["treffer"]]
    ziel = "tree" if w["art"] == "holz" else "rock"
    return (["%s: %s. Each %s now takes %s." % (w["label"], s["label"], ziel, treffer)],
            "kalt_kauf" if petru_kalt(z) else "kauf_%s_%d" % (wid, st + 1))


# ------------------------------------------------------------------ Petru kauft Fisch (Brain Trust, Duc 28.10.2026)
# Reiter "Sell Fish" ab dem ersten Fang. Preis = Rohpreis x Anteil je Seltenheit (kuechen.json petru.fisch_anteil)
# + 5 % je Vertrauensstufe Petru, dazu der Kuechen-Bonus "ankauf". Beim ERSTEN Verkauf einer Art sagt Petru seinen Satz
# (Zeilen-Gruppe fisch_<id> in laeden.json); danach steht er als Notiz im Journal (kern/angeln.py journal).
def fisch_offen(z, modul):
    return petru_offen(z, modul) and bool((z.get("kueche") or {}).get("fischbuch"))


def erzaehlt(z):
    """Fischarten, zu denen Petru schon etwas gesagt hat - nur lesen."""
    return list((z.get("kueche") or {}).get("petru_erzaehlt") or [])


def fisch_preis(z, modul, fid):
    d = kuechen.daten(modul)
    f = next(x for x in d["fische"] if x["id"] == fid)
    anteil = float(((d.get("petru") or {}).get("fisch_anteil") or {}).get(str(d["angeln"]["stufe"][fid]), 0.5))
    vt = max(0, min(5, int(z["werte"].get("vertrauen.petru", 0))))
    kalt = 0.8 if petru_kalt(z) else 1.0                       # nach Weg B: "I'll give you less. You know why."
    return max(1, int(round(f["preis"] * (anteil + 0.05 * vt) * kalt * (100 + kuechen.bonus(z, "ankauf")) / 100.0)))


def fisch_ansicht(z, modul):
    if not fisch_offen(z, modul):
        return None
    d, schon = kuechen.daten(modul), erzaehlt(z)
    return [{"id": f["id"], "label": f["label"], "n": kuechen.vorrat_menge(z, f["roh"]), "preis": fisch_preis(z, modul, f["id"]),
             "stufe": d["angeln"]["stufe"][f["id"]], "bild": "/farm/fische/%s.png" % f["id"], "neu": f["id"] not in schon}
            for f in d["fische"] if kuechen.vorrat_menge(z, f["roh"])]


def fisch_verkaufen(z, modul, fid, alle=False):
    """Eine (oder alle) Fische einer Art aus dem Vorrat an Petru, schlechteste Qualitaet zuerst.
    -> (Zeilen, Zeilen-Gruppe fisch_<id> beim ersten Verkauf dieser Art, sonst None)"""
    if not fisch_offen(z, modul):
        raise ValueError("Petru isn't buying fish yet.")
    f = next((x for x in kuechen.daten(modul)["fische"] if x["id"] == fid), None)
    if not f or not _fisch_key(z, fid):
        raise ValueError("Davon hast du keinen im Vorrat.")
    preis, n = fisch_preis(z, modul, fid), 0
    while _fisch_key(z, fid) and (alle or not n):
        kuechen.vorrat_nehmen(z, _fisch_key(z, fid))
        n += 1
    z["konto"] += preis * n
    z.setdefault("buchungen", []).append({"text": "Petru: %d× %s" % (n, f["label"]), "betrag": preis * n, "tag": z["tag"]})
    gruppe = None
    if petru_kalt(z):                                          # keine Geschichten, solange er kalt ist - die kommen danach
        return ["You sell %d× %s to Petru for %d €." % (n, f["label"], preis * n)], "kalt_fisch"
    if fid not in erzaehlt(z):
        kuechen.kueche(z).setdefault("petru_erzaehlt", []).append(fid)
        gruppe = "fisch_" + fid
    return ["You sell %d× %s to Petru for %d €." % (n, f["label"], preis * n)], gruppe
