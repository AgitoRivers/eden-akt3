# -*- coding: utf-8 -*-
"""Angeln (Duc 27.10.2026, E-079; seit 28.10.2026 an Quellen): Der CODE entscheidet, was beisst, und bucht den Fang; das Minispiel
laeuft im Client (client/plugins/eden-angeln) und meldet nur, ob der Drill geklappt hat.

  * Orte: das Boot (Swim Platform, freie Wahl) und jeder Rastplatz mit Wasser (kern/abbau.py, Quellen in kuechen.json abbau).
    Kein Zeitpreis mehr (Duc 28.10.): man angelt, bis die Quelle leer ist (je Wurf eins vom Bestand), dann 3 Tage Pause.
    Am Rastplatz laeuft die Sitzung ueber dem Expeditions-Bildschirm und kehrt danach dorthin zurueck.
  * Wurf: mit FUND_CHANCE eine Fundsache (Treibholz, Ankerkette, Flusskiesel: Rohstoffe fuer die Staelle), sonst ein Fisch nach Stufe
    (1 haeufig 60 %, 2 30 %, 3 selten 10 %) aus dem Gewaesser des Ortes.
  * Drill (Duc): ein Punkt huepft im senkrechten Balken auf und ab; treffen, solange er in der goldenen Zone ist (wie eine Parade).
    3-4 Treffer = gefangen. Die Zone schrumpft die ganze Zeit, ein Fehlklick nimmt ein Stueck mehr; ist sie weg, reisst die Leine.
    Niedrige Stufe: langsamer Punkt, grosse Zone. Wahrnehmung macht Zone und Biss-Fenster etwas groesser.
  * Qualitaet: Drill ohne Fehlklick = 3 Sterne, sonst 2. Der entspannte Modus (Client) gibt hoechstens 2 Sterne.
  * Fisch-Journal: z["kueche"]["fischbuch"]; alle 10 Fische eines Gewaessers = dauerhaft groessere Zone (Sammel-Bonus).
  * Stapeln (Duc 28.10.2026): am Rastplatz geht der Fang in die Tasche (kern/expedition.py ernte, 3 je Fischart); ist kein Platz,
    schwimmt der Fisch wieder davon (das Journal zaehlt ihn trotzdem). Am Boot geht er wie bisher direkt in den Vorrat.
  * Spielstaende ohne Angeln bekommen keinen neuen Schluessel.
  * Moewe (Duc 29.10.2026): am Meer schnappt mit MOEWE_CHANCE eine Moewe den frisch gelandeten Fisch, hoechstens einmal je
    Gang. Sofort folgt ein kurzer Kampf (Begegnung MOEWE_KAMPF, Gegner "moewe" aus dem Fruehstueckskampf). Sieg oder
    Aufgabe: der Fisch kommt zurueck (Tasche bzw. Vorrat). Niederlage, Flucht oder sie entkommt: der Fisch ist weg; im
    Journal steht er trotzdem. Danach geht der Angelgang weiter."""
from . import abbau, expedition, koeder, kuechen

GRUENDE = ("biss", "riss", "abbruch")
MOEWE_CHANCE = {"meer": 0.15}
MOEWE_KAMPF = "angel_moewe"
MOEWE_FEDERN = 2            # Beute fuer Sieg oder Aufgabe: Moewenfedern fuer Petrus Koeder (30.10.2026)


def _d(modul):
    return kuechen.daten(modul).get("angeln") or {}


def _wahrnehmung(z):
    return ((z.get("persona") or {}).get("attribute") or {}).get("perception", 2)


def _bonus_zone(z, modul, wasser):
    if wasser in ((z.get("kueche") or {}).get("angel_boni") or []):
        return _d(modul)["sammel_bonus"][wasser]["zone"]
    return 0


def ort(modul, oid):
    """Angelplatz: das Boot (angeln.orte) oder ein Rastplatz mit Wasser (abbau.quellen). -> dict oder None."""
    q = abbau.platz(modul, oid)
    if not q or not q.get("wasser"):
        return None
    o = (_d(modul).get("orte") or {}).get(oid) or {}
    return {"id": oid, "label": o.get("label") or q["label"], "text": o.get("text", ""), "wasser": q["wasser"], "pose": q["pose"],
            "bild": q.get("angel_bild_datei") or o.get("bild"), "heim": not q["frames"]}


def orte(z, modul):
    """Angelplaetze fuer die freie Wahl (nur das Boot; die anderen liegen an Rastplaetzen). Nur lesen."""
    out = []
    for oid in (_d(modul).get("orte") or {}):
        o = ort(modul, oid)
        if o:
            rest, wieder = abbau.stand(z, modul, oid, "wasser")
            out.append(dict(o, bild="/bg/" + o["bild"], frei=True, rest=rest, menge=abbau.menge(modul, "wasser"),
                            in_tagen=(wieder - z["tag"]) if wieder else 0))
    return out


def _sitzung(z):
    s = z.get("angeln")
    if not s or z.get("status") != "angeln":
        raise ValueError("You aren't fishing right now.")
    return s


def starten(z, modul, oid, frame=None):
    """Am Boot aus der freien Wahl oder am offenen Rastplatz-Frame (Status ereignis) mit Wasser."""
    o = ort(modul, oid)
    if not o:
        raise ValueError("That fishing spot doesn't exist.")
    if z.get("status") == "wahl":
        if not o["heim"]:
            raise ValueError("You can only get there on an expedition.")
    elif z.get("status") == "ereignis":
        if abbau.platz_von_frame(modul, frame) != oid:
            raise ValueError("There's no water to fish here.")
    else:
        raise ValueError("You can fish in your free time at the boat or at a rest site with water.")
    rest, _ = abbau.stand(z, modul, oid, "wasser")
    if not rest:
        raise ValueError("Nothing will bite here for a few days.")
    if z.get("status") == "ereignis" and abbau.tasche_voll(z, modul, "wasser"):
        raise ValueError("Your bag is full – no room for a fish.")
    z["angeln"] = {"ort": oid, "wurf": 0, "wuerfe": rest, "faenge": [], "aktiv": None, "zurueck": z["status"],
                   "bild": _bild_waehlen(z, modul, o)}
    z["status"] = "angeln"


def _bild_waehlen(z, modul, o):
    """Hintergrund des Angelgangs (Duc 28.10.2026: alle 20 nutzen, wechselnd je Gewaesser): zufaellig aus den 10 Bildern des
    Gewaessers, nie dasselbe wie beim letzten Mal an diesem Platz. Fest fuer den Gang (steht in der Sitzung)."""
    bilder = abbau._d(modul).get("angel_bilder") or {}
    # Duc 29.10.: das Boot (heim) zieht nur die Yacht-Bilder, Rastplaetze ihr Gewaesser (Meer = Kuestenbilder)
    pool = (bilder.get("boot") if o["heim"] else None) or bilder.get(o["wasser"]) or [o["bild"]]
    k = kuechen.kueche(z)
    letzt = k.setdefault("angel_bild_letzt", {})
    gang = k["angel_gaenge"] = k.get("angel_gaenge", 0) + 1
    wahl = kuechen.rng(z, "angelbild", o["id"], gang).choice([b for b in pool if b != letzt.get(o["id"])] or pool)
    letzt[o["id"]] = wahl
    return wahl


def _fische(modul, wasser):
    return [f for f in kuechen.daten(modul)["fische"] if f["ort"] == wasser]


def auswerfen(z, modul):
    """Was beisst diesmal? Bleibt stehen, bis das Ergebnis gemeldet ist (Neuladen wirft nicht neu)."""
    s = _sitzung(z)
    if s["aktiv"]:
        return s["aktiv"]
    a = _d(modul)
    if s["wurf"] >= s.get("wuerfe", 4):
        raise ValueError("Nothing will bite here for a few days.")
    if s.get("zurueck") == "ereignis" and abbau.tasche_voll(z, modul, "wasser"):
        raise ValueError("Your bag is full – no room for a fish.")
    w = ort(modul, s["ort"])["wasser"]
    r = kuechen.rng(z, "angeln", s["ort"], s["wurf"], z.get("phase"))
    kw = koeder.wirkung(z, modul)                                        # Koeder (30.10.2026): Zone, Seltenheit, Wartezeit
    if r.random() < a["fund_chance"]:
        fund = r.choice(a["fundsachen"][w])
        fang, stufe = {"art": "fund", "id": fund["id"]}, 0
    else:
        stufen = [int(k) for k in a["gewicht"]]
        gew = {k: a["gewicht"][str(k)] for k in stufen}
        for k, plus in kw["selten"].items():                             # seltenere Fische: Punkte wandern von Stufe 1 weg
            gew[int(k)] += plus
            gew[1] = max(1, gew[1] - plus)
        stufe = r.choices(stufen, weights=[gew[k] for k in stufen])[0]
        kandidaten = [f["id"] for f in _fische(modul, w) if a["stufe"][f["id"]] == stufe]
        fang = {"art": "fisch", "id": r.choice(kandidaten)}
    dr = a["drill"][str(stufe)]
    plus = max(0, min(3, _wahrnehmung(z) - 2))
    s["aktiv"] = dict(fang, nr=s["wurf"] + 1, stufe=stufe, treffer=dr["treffer"], tempo=dr["tempo"], schwund=dr["schwund"],
                      zone=round(dr["zone"] + a["wahrnehmung_zone"] * plus + _bonus_zone(z, modul, w) + kw["zone"], 3),
                      fehler=a["fehler"], tempo_je_treffer=a["tempo_je_treffer"],
                      biss={"warten": round(r.uniform(*a["biss"]["warten"]) * kw["warten"], 2),
                            "fenster": round(a["biss"]["fenster"] + a["biss"]["fenster_wahrnehmung"] * plus, 2)},
                      start=round(r.random(), 3))
    return s["aktiv"]


def ergebnis(z, modul, gefangen, fehler=0, leicht=False, grund=""):
    """Der Client meldet den Drill: gefangen (bool), Fehlklicks, entspannter Modus, Grund bei Misserfolg (biss/riss/abbruch).
    -> Eintrag fuer die Fangliste."""
    s = _sitzung(z)
    f = s["aktiv"]
    if not f:
        raise ValueError("There's nothing on the line right now.")
    a = _d(modul)
    s["wurf"] += 1
    s["aktiv"] = None
    abbau.nehmen(z, modul, s["ort"], "wasser")        # jeder Wurf zieht eins vom Bestand der Quelle
    tasche = s.get("zurueck") == "ereignis" and expedition.unterwegs(z)   # am Rastplatz: in die Tasche (Stapeln, 28.10.2026)
    e = {"nr": f["nr"], "art": f["art"], "id": f["id"], "ok": bool(gefangen), "stufe": f["stufe"], "tasche": tasche}
    if not gefangen:
        e["grund"] = grund if grund in GRUENDE else "riss"
    elif f["art"] == "fund":
        w = ort(modul, s["ort"])["wasser"]
        fund = next(x for x in a["fundsachen"][w] if x["id"] == f["id"])
        genommen = {rid: expedition.ernte_roh(z, modul, rid, n, tasche) for rid, n in fund["rohstoffe"].items()}
        roh = kuechen.daten(modul)["rohstoffe"]
        e.update(label=fund["label"], text=fund["text"],
                 rohstoffe=[{"id": rid, "label": roh[rid]["label"], "n": n} for rid, n in genommen.items() if n],
                 liegen=[{"id": rid, "label": roh[rid]["label"], "n": n - genommen[rid]}
                         for rid, n in fund["rohstoffe"].items() if genommen[rid] < n])
    else:
        stern = 3 if int(fehler or 0) == 0 and not leicht else 2
        fisch = next(x for x in kuechen.daten(modul)["fische"] if x["id"] == f["id"])
        r = kuechen.rng(z, "moewe", s["ort"], s["wurf"], z.get("phase"))
        if not s.get("moewe_war") and r.random() < MOEWE_CHANCE.get(fisch["ort"], 0):
            s["moewe_war"] = True                      # die Moewe schnappt ihn, gleich folgt der Kampf (eden.py)
            s["moewe"] = {"nr": f["nr"], "id": f["id"], "stern": stern, "tasche": tasche}
            e["moewe"] = "klaut"
        elif not expedition.ernte_fisch(z, modul, f["id"], stern, tasche):
            e["frei"] = True                           # kein Platz in der Tasche: er schwimmt davon
        k = kuechen.kueche(z)
        buch = k.setdefault("fischbuch", {})
        e["neu"] = f["id"] not in buch
        b = buch.setdefault(f["id"], {"n": 0, "bester": 0})
        b["n"] += 1
        b["bester"] = max(b["bester"], stern)
        e.update(label=fisch["label"], roh=fisch["roh_label"], text=fisch["text"], stern=stern, wasser=fisch["ort"])
        w = fisch["ort"]
        boni = k.setdefault("angel_boni", [])
        if w not in boni and all(x["id"] in buch for x in _fische(modul, w)):
            boni.append(w)
            e["bonus"] = a["sammel_bonus"][w]
    s["faenge"].append(e)
    return e


def moewe_offen(z):
    """Hat gerade eine Moewe einen Fisch geschnappt und der Kampf steht noch aus? -> Begegnungs-ID oder None."""
    s = z.get("angeln") or {}
    return MOEWE_KAMPF if (s.get("moewe") and z.get("status") == "angeln") else None


def moewe_nach_kampf(z, modul):
    """Sobald der Moewen-Kampf entschieden ist: Fisch zurueck (Sieg/Aufgabe) oder weg. Zeilen auf die Ergebniskarte."""
    k = z.get("kampf") or {}
    e = k.get("ergebnis")
    s = z.get("angeln") or {}
    m = s.get("moewe")
    if k.get("definition") != MOEWE_KAMPF or not e or e.get("nochmal") or not m or k.get("moewe_abgerechnet"):
        return []
    k["moewe_abgerechnet"] = True
    s.pop("moewe", None)
    fang = next((x for x in s.get("faenge", []) if x.get("nr") == m["nr"]), {})
    label = fang.get("label") or m["id"]
    zeilen = []
    if e["art"] in ("ko", "aufgabe"):
        if expedition.ernte_fisch(z, modul, m["id"], m["stern"], m["tasche"]):
            fang["moewe"], zeile = "zurueck", "You get your %s back." % label
        else:
            fang.update(moewe="zurueck", frei=True)
            zeile = "You get your %s back – but there's no room in your bag, so it goes back into the water." % label
        zeilen.append(zeile)
        if expedition.ernte_roh(z, modul, "feather", MOEWE_FEDERN, m["tasche"]):         # Federn fuer Petrus Koeder (30.10.2026)
            zeilen.append("The gull leaves %d feathers behind. Petru would like those." % MOEWE_FEDERN)
    else:
        fang["moewe"] = "weg"
        zeilen.append("The gull got away with your %s." % label)
    e.setdefault("zeilen", []).extend(zeilen)
    return zeilen


def ende(z, modul):
    """Sitzung beenden, zurueck an Deck bzw. an den Rastplatz. -> Zeilen fuer die Meldung (leer ohne einen Wurf). Kostet keine Zeit."""
    s = _sitzung(z)
    z.pop("angeln", None)
    z["status"] = s.get("zurueck") or "wahl"
    if not s["faenge"]:
        return []
    zeilen = []
    for e in s["faenge"]:
        if not e["ok"]:
            zeilen.append({"biss": "Missed the bite.", "riss": "The line snapped.", "abbruch": "You let it go."}[e["grund"]])
        elif e["art"] == "fund":
            zeilen.append("%s: %s" % (e["label"], ", ".join("+%d %s" % (r["n"], r["label"]) for r in e["rohstoffe"])
                                      or "no room in the bag"))
        elif e.get("moewe") == "weg":
            zeilen.append("%s %s · a gull took it" % (e["label"], "★" * e["stern"]))
        else:
            zeilen.append("%s %s%s%s%s" % (e["label"], "★" * e["stern"], " · new in your journal" if e.get("neu") else "",
                                           " · won back from a gull" if e.get("moewe") == "zurueck" else "",
                                           " · no room in the bag, you let it go" if e.get("frei") else ""))
    return ["%s – %d of %d casts landed something." % (ort(modul, s["ort"])["label"], sum(1 for e in s["faenge"] if e["ok"]),
                                                        len(s["faenge"]))] + zeilen


def journal(z, modul):
    buch = (z.get("kueche") or {}).get("fischbuch") or {}
    a = _d(modul)
    notiz = (kuechen.daten(modul).get("petru") or {}).get("fisch_notiz") or {}      # Petrus Satz nach dem ersten Verkauf (28.10.)
    erzaehlt = (z.get("kueche") or {}).get("petru_erzaehlt") or []
    fische = [{"id": f["id"], "label": f["label"], "wasser": f["ort"], "stufe": a["stufe"][f["id"]], "text": f["text"],
               "sprite": "/farm/fische/%s.png" % f["id"], "n": (buch.get(f["id"]) or {}).get("n", 0),
               "bester": (buch.get(f["id"]) or {}).get("bester", 0),
               "petru": notiz.get(f["id"]) if f["id"] in erzaehlt else None} for f in kuechen.daten(modul)["fische"]]
    boni = (z.get("kueche") or {}).get("angel_boni") or []
    return {"fische": fische, "gefangen": sum(1 for f in fische if f["n"]),
            "boni": [dict(a["sammel_bonus"][w], wasser=w, frei=w in boni) for w in ("meer", "fluss")]}


def ansicht(z, modul):
    s = z.get("angeln")
    if not s:
        return None
    o = ort(modul, s["ort"])
    aktiv = dict(s["aktiv"]) if s["aktiv"] else None
    if aktiv:
        aktiv["sprite"] = "/farm/fische/%s.png" % aktiv["id"] if aktiv["art"] == "fisch" else None
    faenge = [dict(e, sprite="/farm/fische/%s.png" % e["id"] if e["art"] == "fisch" else None) for e in s["faenge"]]
    return {"ort": s["ort"], "label": o["label"], "text": o["text"], "bild": "/bg/" + (s.get("bild") or o["bild"]),   # Wechselbild (28.10.)
            "wasser": o["wasser"], "pose": o.get("pose") or [50, 62], "koeder": koeder.aktiv_ansicht(z, modul),   # Schwimmer (30.10.2026)
            "wurf": s["wurf"], "wuerfe": s.get("wuerfe", 4), "aktiv": aktiv, "faenge": faenge, "journal": journal(z, modul),
            "voll": s.get("zurueck") == "ereignis" and abbau.tasche_voll(z, modul, "wasser")}     # Tasche voll: nicht mehr werfen
