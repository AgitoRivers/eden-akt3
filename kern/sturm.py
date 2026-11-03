# -*- coding: utf-8 -*-
"""Sturmnacht an Tag 5 als gescriptetes Ereignis im Stil der Anhoerung (Duc 27.10.2026, Brain Trust).

Zwei Teile, beide ueber Status "sturm" (die Szene bleibt dabei offen, wie bei der Anhoerung):
  - "vorbereitung" (Szene sturmvorbereitung, Dinner): Megan, Bitten der Crew, Duc teilt fuenf Posten ein
    (sechs Chips inkl. Duc, wer uebrig bleibt, ruht), Zusagen, Megans Kommentar, Tratsch.
  - "nacht" (Szene sturmnacht): sechs Krisen; die erste Boe gelingt immer, dann je Posten ✓/≈/✕ nach Eignung.
    Bleibt Duc frei, darf er einmal hinrennen (Sprint) und einen verlorenen Posten retten.
Folgen (fest, kein Wuerfeln): Megans Haltung (Flag sturm_bestanden/sturm_chaos -> Adern in der Anhoerung),
Vertrauen fuer gehaltene Wunschposten, Geld/Moral fuer verlorene Posten, Ruhe-Bonus, Rueckbezug am Lagerfeuer.
Daten: module/eden_rise/sturm.json (werkzeuge/eden_rise/sturm_eden_rise.py), Wiki docs/wiki/systeme/sturm.md."""
import json, os, random

from . import chronik, zustand

SZENEN = {"sturmvorbereitung": "vorbereitung", "sturmnacht": "nacht"}
_CACHE = {}


def daten(moddir):
    pfad = os.path.join(moddir, "sturm.json")
    if not os.path.exists(pfad):
        return None
    t = os.path.getmtime(pfad)
    if _CACHE.get(pfad, (None,))[0] != t:
        _CACHE[pfad] = (t, json.load(open(pfad, encoding="utf-8")))
    return _CACHE[pfad][1]


def _name(modul, pid):
    return "You" if pid == "duc" else (modul["personen"].get(pid) or {}).get("name", pid).split(" ")[0]


# Sprite passt zur Lage (Duc 29.10.2026): wer im Sturm ruhen soll, reagiert trocken, nicht mit Schock-Pose
RUHE_GEFUEHL = {"chiara": "caring", "rosi": "annoyance", "lea": "confusion", "lola": "caring"}


def _moment(v, art, text, wer="megan", key=None, gefuehl=None, warte=False, effekt=None, sub=None, **extra):
    e = dict(extra, wer=wer, text=text, art=art, moment=True)
    for k, x in (("key", key), ("gefuehl", gefuehl), ("effekt", effekt), ("sub", sub)):
        if x:
            e[k] = x
    if warte:
        e["warte"] = True
    v["log"].append(e)


def _wahl(v, n):
    return random.Random(len(v["log"]) * 17 + len(v.get("ergebnis", {}))).randrange(n)


def _megan(v, D, schl, **kw):
    liste = D["megan"][schl]
    i = _wahl(v, len(liste))
    _moment(v, "megan", liste[i], key="st.megan.%s.%d" % (schl, i), **kw)


def _crew(z, modul, D):
    """Wer heute an Bord ist und mitmachen kann (Personen ohne Sprite/Karte fallen nicht heraus, nur Abwesende)."""
    out = []
    for p in D["crew"]:
        d = modul["personen"].get(p) or {}
        if not d or (d.get("von_bord_ab_tag") and z["tag"] >= d["von_bord_ab_tag"]) or (
                d.get("weg_flag") and d["weg_flag"] in z.get("flags", [])):
            continue
        out.append(p)
    return out


def _tratsch(z, modul, v, zeilen, schl, ohne=(), art="tratsch"):
    da = [(i, p, s) for i, (p, s) in enumerate(zeilen) if p in v["crew"] and p not in ohne]
    if len(da) < 2:
        return
    gruppe = [p for _, p, _ in da]
    for n, (i, p, s) in enumerate(da):
        _moment(v, art, s, wer=p, key="%s.%d" % (schl, i), gruppe=gruppe, gefuehl="surprise" if n == 0 else None)


def _log(z, art, text, wer=None):
    sz = z.get("szene")
    if sz is not None:                                 # fuer Kurzfassung und Gedaechtnis am Szenenende (kern/szene.py)
        e = {"art": art, "text": text}
        if wer:
            e.update(wer=wer, gezeigt=text)            # wie Figurenzeilen der Szene (Anzeige liest "gezeigt")
        sz["log"].append(e)


# ------------------------------------------------------------------ Start
def beginnen(z, modul, moddir, sid):
    D = daten(moddir)
    teil = SZENEN.get(sid)
    if not D or not teil:
        return False
    st = z.setdefault("sturm", {})
    st["zaehler"] = st.get("zaehler", 0) + 1          # Client erkennt daran einen neuen Durchlauf (Neustart)
    v = {"teil": teil, "log": [], "crew": _crew(z, modul, D), "fertig": False, "lauf": st["zaehler"]}
    st["laufend"] = v
    if teil == "vorbereitung":
        st.pop("plan", None)
        _moment(v, "titel", "Before the Storm", sub="Day 5 · 18:00 · the aft deck · Megan is watching", warte=True,
                effekt="funk_rauschen")
        _megan(v, D, "auftakt", gefuehl="neutral")
        for p in v["crew"]:
            _moment(v, "bitte", D["bitte"][p], wer=p, key="st.bitte." + p, gruppe=list(v["crew"]),
                    posten=D["wunsch"][p], gefuehl="joy" if p in ("lola", "maxwell") else "neutral")
        _megan(v, D, "auftrag", warte=True, sub="Assign the posts")
        v["schritt"] = "einteilen"
    else:
        plan = st.get("plan") or {"posten": {}, "ruhe": None}
        v.update(plan=plan, krisen=list(D["krisen_folge"]), ergebnis={}, sprint=None,
                 sprint_frei="duc" not in plan["posten"].values())
        _moment(v, "titel", "What You Hear in the Dark", sub="Day 5 · 23:30 · the storm hits", warte=True,
                effekt="sturm_nacht")
        _megan(v, D, "nacht", gefuehl="neutral")
        v["schritt"] = "nacht"
        _weiter(z, modul, D, v)
    return True


def aktiv(z):
    return (z.get("sturm") or {}).get("laufend")


# ------------------------------------------------------------------ Vorbereitung: einteilen
def einteilen(z, modul, moddir, posten):
    """posten = {posten_id: pid|"duc"|None}. Jede Person hoechstens einmal; wer fehlt, ruht."""
    D, v = daten(moddir), aktiv(z)
    if not v or v["teil"] != "vorbereitung" or v.get("schritt") != "einteilen":
        raise ValueError("Gerade wird nichts eingeteilt.")
    plan = {}
    for po in D["posten"]:
        p = (posten or {}).get(po)
        if p and p not in v["crew"] + ["duc"]:
            raise ValueError("Unbekannte Person: %s" % p)
        if p and p in plan.values():
            raise ValueError("%s kann nur einen Posten übernehmen." % _name(modul, p))
        if p:
            plan[po] = p
    ruhe = [p for p in v["crew"] if p not in plan.values()]
    z["sturm"]["plan"] = {"posten": plan, "ruhe": ruhe[0] if len(ruhe) == 1 else None, "ruhen": ruhe}
    _log(z, "duc", "Duc assigns the storm posts: %s." % "; ".join(
        "%s - %s" % (D["posten"][po]["titel"], _name(modul, p)) for po, p in plan.items()) + (
        " %s rests." % ", ".join(_name(modul, p) for p in ruhe) if ruhe else ""))
    for po in D["posten"]:                             # jede Einteilung wird kommentiert (Zusage oder Zoegern)
        p = plan.get(po)
        if not p or p == "duc":
            continue
        e = D["eignung"][p][po]
        _moment(v, "zusage", D["zusage"][p][po], wer=p, key="st.zusage.%s.%s" % (p, po), posten=po,
                gefuehl="pride" if e == 3 else ("neutral" if e == 2 else "nervousness"), effekt="chip_einrasten")
        _log(z, "figur", D["zusage"][p][po], p)
    for p in ruhe:
        _moment(v, "ruhe", D["ruhe"][p], wer=p, key="st.ruhe." + p, gefuehl=RUHE_GEFUEHL.get(p, "confusion"))
    stark = sum(1 for po, p in plan.items() if D["eignung"][p][po] == 3)
    _megan(v, D, "plan_stark" if stark >= 4 else ("plan_gemischt" if stark >= 2 else "plan_schwach"),
           gefuehl="pride" if stark >= 4 else ("neutral" if stark >= 2 else "disapproval"))
    _megan(v, D, "selbst" if "duc" in plan.values() else "frei", gefuehl="neutral")
    lea = plan.get("anker") == "lea"
    schl = "lea_anker" if lea else ("lea_nicht" if "lea" in plan.values() else ("ruhe" if ruhe else "standard"))
    _tratsch(z, modul, v, D["tratsch_plan"][schl], "st.tratsch.plan." + schl, ohne=ruhe)
    _megan(v, D, "los", warte=True, sub="To the posts")
    v["schritt"], v["fertig"] = "fertig", True
    chronik.eintragen(z, modul, "entscheidung", "Duc assigned the crew to the storm posts in front of Megan.", wichtig=2)


# ------------------------------------------------------------------ Nacht
def _eignung(D, p, po):
    return D["eignung"].get(p, {}).get(po, 1) if p else 0


def _weiter(z, modul, D, v):
    """Spielt Krisen ab, bis eine Sprint-Entscheidung ansteht oder die Nacht vorbei ist."""
    while v["krisen"]:
        po = v["krisen"][0]
        k = D["krise"][po]
        if po == "boee":
            v["krisen"].pop(0)
            _moment(v, "krise", k["titel"], wer="erzaehler", sub=k["text"], zeit=k["zeit"], effekt=k["effekt"])
            for i, (p, s) in enumerate(D["boee"]):
                if p in v["crew"]:
                    _moment(v, "ruf", s, wer=p, key="st.boee.%d" % i, gruppe=[x for x, _ in D["boee"] if x in v["crew"]],
                            gefuehl="surprise")
            _moment(v, "erzaehlung", k["ok"], wer="erzaehler", ausgang="ok")
            _log(z, "ereignis", k["text"] + " " + k["ok"])
            continue
        if v.get("offen") != po:                       # Krise einleiten (einmal)
            _moment(v, "krise", k["titel"], wer="erzaehler", sub=k["text"], zeit=k["zeit"], effekt=k["effekt"],
                    posten=po, dunkel=bool(k.get("dunkel")))
            _log(z, "ereignis", k["text"])
        p = v["plan"]["posten"].get(po)
        e = _eignung(D, p, po)
        if p == "duc":
            aus = "ok" if e == 3 else ("knapp" if e == 2 else "weg")
            if aus != "weg":
                _moment(v, "erzaehlung", k["duc_" + aus], wer="erzaehler", posten=po, ausgang=aus)
                _log(z, "ereignis", k["duc_" + aus])
            _abschliessen(z, modul, D, v, po, aus)
            continue
        if e >= 2:
            schl = "%s.%s" % (p, po)
            text = (D["ok"] if e == 3 else D["knapp"])[schl]
            aus = "ok" if e == 3 else "knapp"
            _moment(v, "posten_ruf", text, wer=p, key="st.%s.%s" % (aus, schl), posten=po, ausgang=aus,
                    gefuehl="pride" if e == 3 else "nervousness")
            _log(z, "figur", text, p)
            _abschliessen(z, modul, D, v, po, aus)
            continue
        # Eignung 1 oder leer: Panik, dann darf Duc (wenn frei und noch nicht gerannt) hinrennen
        if v.get("offen") != po:
            v["offen"] = po
            if p:
                _moment(v, "panik", D["panik"][p], wer=p, key="st.panik." + p, posten=po, gefuehl="fear")
                _log(z, "figur", D["panik"][p], p)
            if v["sprint_frei"] and not v["sprint"]:
                v["schritt"] = "sprint"
                return
        _abschliessen(z, modul, D, v, po, "weg")
    _morgen(z, modul, D, v)


def sprint(z, modul, moddir, rennen):
    D, v = daten(moddir), aktiv(z)
    if not v or v.get("schritt") != "sprint":
        raise ValueError("Gerade gibt es nichts zu entscheiden.")
    po = v["offen"]
    k = D["krise"][po]
    v["schritt"] = "nacht"
    if rennen:
        v["sprint"] = po
        p = v["plan"]["posten"].get(po)
        _moment(v, "erzaehlung", k["sprint"], wer="erzaehler", posten=po, effekt="schritte_kies")
        _log(z, "duc", "Duc runs to %s." % D["posten"][po]["titel"].lower())
        if p:
            _moment(v, "hilfe", D["hilfe"][p], wer=p, key="st.hilfe." + p, posten=po, gefuehl="relief")
        aus = "ok" if _eignung(D, "duc", po) == 3 else "knapp"
        _moment(v, "erzaehlung", k["duc_" + aus], wer="erzaehler", posten=po, ausgang=aus)
        _log(z, "ereignis", k["duc_" + aus])
        _abschliessen(z, modul, D, v, po, aus, megan="sprint")
    else:
        _log(z, "duc", "Duc stays where he is and lets %s go." % D["posten"][po]["titel"].lower())
        _abschliessen(z, modul, D, v, po, "weg")
    _weiter(z, modul, D, v)


def _abschliessen(z, modul, D, v, po, aus, megan=None):
    v["krisen"].pop(0)
    v["offen"] = None
    v["ergebnis"][po] = aus
    k = D["krise"][po]
    if aus == "weg":
        _moment(v, "erzaehlung", k["weg"], wer="erzaehler", posten=po, ausgang="weg", effekt="wuerfel_fehlschlag")
        _log(z, "ereignis", k["weg"])
    elif aus == "ok" and po == "strom":
        v["log"][-1]["effekt2"] = "strom_zurueck"
    _megan(v, D, megan or aus, gefuehl={"ok": "pride", "knapp": "neutral", "weg": "disapproval"}.get(aus, "neutral"))
    if po == "strom":                                 # nach dem Stromausfall rufen alle durcheinander
        _tratsch(z, modul, v, D["rufe"], "st.rufe", ohne=v["plan"].get("ruhen") or [], art="ruf")


def _morgen(z, modul, D, v):
    erg = v["ergebnis"]
    ok = sum(1 for a in erg.values() if a == "ok")
    stufe = "gut" if ok >= D["megan_ergebnis"]["bestanden"] else ("schlecht" if ok <= D["megan_ergebnis"]["chaos"] else
                                                                   "mittel")
    _moment(v, "titel", "Morning", sub="06:10 · the storm has passed", warte=True, effekt="tag_beginnt")
    ruhen = v["plan"].get("ruhen") or []
    _tratsch(z, modul, v, D["tratsch_morgen"][stufe], "st.tratsch.morgen." + stufe)
    for p in ruhen:
        if p in v["crew"]:
            _moment(v, "morgen", D["morgen"][p], wer=p, key="st.morgen." + p, gefuehl="relief")
    _megan(v, D, "ende_" + stufe, gefuehl={"gut": "pride", "mittel": "neutral", "schlecht": "disapproval"}[stufe])
    _moment(v, "notiz", "Megan writes something down.", wer="erzaehler", warte=True, effekt="auftrag_feder")
    # Folgen (fest)
    folgen, zeilen = [], []
    if stufe == "gut":
        folgen.append({"flag": "sturm_bestanden"})
        zeilen.append("Megan saw a crew that works: her stance towards you +1")
    elif stufe == "schlecht":
        folgen.append({"flag": "sturm_chaos"})
        zeilen.append("Megan saw chaos: her stance towards you −1")
    for po, aus in erg.items():
        if aus == "weg" and po in D["folge_weg"]:
            f = dict(D["folge_weg"][po])
            zeilen.append(f.pop("text"))
            if "wert" in f:
                f["moral_art"] = "genau"
            if "geld" in f:
                f["text"] = "Storm damage: " + D["posten"][po]["titel"]
            folgen.append(f)
    for po, p in v["plan"]["posten"].items():
        if p in D["wunsch"] and D["wunsch"][p] == po and erg.get(po) in ("ok", "knapp"):
            folgen.append({"wert": "vertrauen." + p, "delta": 1})
            zeilen.append("%s held the post they asked for: trust +1" % _name(modul, p))
    if any(p in v["crew"] for p in ruhen):
        folgen.append({"wert": "moral", "delta": 1, "moral_art": "genau"})
        zeilen.append("%s rested and looked after everyone at dawn: crew morale +1" % " and ".join(
            _name(modul, p) for p in ruhen if p in v["crew"]))
    zustand.folgen_anwenden(z, modul, folgen)
    folgen_flags = ["sturm_%s_%s" % (po, aus) for po, aus in erg.items()]
    z["flags"] += [f for f in folgen_flags if f not in z["flags"]]
    z["sturm"]["ergebnis"] = {"posten": dict(erg), "stufe": stufe, "ok": ok, "sprint": v.get("sprint"),
                             "plan": v["plan"]["posten"], "ruhen": ruhen}
    v["bilanz"] = {"stufe": stufe, "zeilen": zeilen}
    v["schritt"], v["fertig"] = "fertig", True
    text = {"gut": "The crew held through the storm on Day 5 - Megan saw them work together.",
            "mittel": "The crew got through the storm on Day 5, not cleanly.",
            "schlecht": "The storm on Day 5 went badly - Megan watched it happen."}[stufe]
    chronik.eintragen(z, modul, "ausgang", text, wichtig=3)
    for po, p in v["plan"]["posten"].items():
        if p in v["crew"]:
            zustand.gedaechtnis_add(z, p, "In the storm Duc put %s on %s; it %s." % (
                "her" if p != "maxwell" else "him", D["posten"][po]["titel"].lower(),
                {"ok": "held well", "knapp": "held, barely", "weg": "went wrong"}[erg.get(po, "weg")]))


def schliessen(z):
    v = aktiv(z)
    if not v or not v["fertig"]:
        raise ValueError("Der Sturm läuft noch.")
    z["sturm"].pop("laufend", None)
    return v["teil"]


# ------------------------------------------------------------------ Lagerfeuer (Tag 6): Rueckbezug auf die Nacht
def lagerfeuer_hinweise(z, modul, moddir):
    """Hinweise fuer die Figuren am Lagerfeuer: die Nacht einmal ansprechen (Brain Trust #7)."""
    e = (z.get("sturm") or {}).get("ergebnis")
    sz = z.get("szene")
    D = daten(moddir)
    if not e or not sz or not D:
        return
    teile = []
    for po, aus in e["posten"].items():
        if po == "boee":
            continue
        p = e["plan"].get(po)
        wer = "Duc himself" if p == "duc" else (_name(modul, p) if p else "nobody")
        teile.append("%s on %s - %s" % (wer, D["posten"][po]["titel"].lower(),
                                        {"ok": "held", "knapp": "held barely", "weg": "lost"}[aus]))
    if e.get("sprint"):
        teile.append("Duc ran to %s himself" % D["posten"][e["sprint"]]["titel"].lower())
    satz = ("[Callback - last night's storm] %s. Bring it up once, in your own words - who did well, a joke about who "
            "panicked, or quiet thanks - without listing it all." % "; ".join(teile))
    h = sz.setdefault("chronik_hinweise", {})
    for pid in sz.get("figuren", []):
        if pid in modul["personen"]:
            h.setdefault(pid, []).append(satz)


# ------------------------------------------------------------------ Ansicht
def ansicht(z, modul, moddir, sprite):
    v = aktiv(z)
    D = daten(moddir)
    if not v or not D:
        return None
    namen = {p: _name(modul, p) for p in v["crew"] + ["megan"]}
    namen["duc"] = "You"
    plan = (v.get("plan") or z["sturm"].get("plan") or {}).get("posten", {})
    out = {"teil": v["teil"], "lauf": v.get("lauf"), "schritt": v.get("schritt"), "fertig": v["fertig"], "namen": namen,
           "posten": [{"id": po, "titel": d["titel"], "text": d["text"], "wer": plan.get(po),
                       "ergebnis": (v.get("ergebnis") or {}).get(po)} for po, d in D["posten"].items()],
           "crew": [{"id": p, "name": namen[p], "sprite": sprite(p, "neutral"), "wunsch": D["wunsch"][p]}
                    for p in v["crew"]] + [{"id": "duc", "name": "You", "sprite": sprite("duc", "neutral"), "wunsch": None}],
           "megan": sprite("megan", "neutral"),
           "log": [dict(e, n=i, sprite=sprite(e["wer"], e.get("gefuehl") or "neutral")
                        if e["wer"] in modul["personen"] or e["wer"] == "duc" else None,
                        **({"gruppe_bilder": [{"id": p, "name": namen.get(p, p), "sprite": sprite(p, "neutral")}
                                              for p in e["gruppe"]]} if e.get("gruppe") else {}))
                   for i, e in enumerate(v["log"])][-40:],
           "sprint": {"posten": v["offen"], "titel": D["posten"][v["offen"]]["titel"],
                      "wer": plan.get(v["offen"])} if v.get("schritt") == "sprint" else None,
           "sprint_frei": bool(v.get("sprint_frei")) and not v.get("sprint"),
           "bilanz": v.get("bilanz"),
           # Stromausfall: ab der Krise "Power" Notlicht, bis Rosi/Duc den Strom wirklich zurueckholen (✓)
           "dunkel": v["teil"] == "nacht" and any(e.get("art") == "krise" and e.get("posten") == "strom" for e in v["log"])
           and (v.get("ergebnis") or {}).get("strom") != "ok"}
    return out


# ------------------------------------------------------------------ Vertonung (/api/zeile, vertonen_eden_rise.py)
def alle_zeilen(moddir):
    """-> [(schluessel, sprecher, text)] - alles, was im Sturm gesprochen wird."""
    D = daten(moddir)
    if not D:
        return []
    out = [("st.megan.%s.%d" % (k, i), "megan", s) for k, liste in D["megan"].items() for i, s in enumerate(liste)]
    out += [("st.bitte." + p, p, s) for p, s in D["bitte"].items()]
    out += [("st.zusage.%s.%s" % (p, po), p, s) for p, d in D["zusage"].items() for po, s in d.items()]
    out += [("st.ruhe." + p, p, s) for p, s in D["ruhe"].items()]
    for k, liste in D["tratsch_plan"].items():
        out += [("st.tratsch.plan.%s.%d" % (k, i), p, s) for i, (p, s) in enumerate(liste)]
    out += [("st.boee.%d" % i, p, s) for i, (p, s) in enumerate(D["boee"])]
    out += [("st.rufe.%d" % i, p, s) for i, (p, s) in enumerate(D["rufe"])]
    for art in ("ok", "knapp"):
        out += [("st.%s.%s" % (art, k), k.split(".")[0], s) for k, s in D[art].items()]
    out += [("st.panik." + p, p, s) for p, s in D["panik"].items()]
    out += [("st.hilfe." + p, p, s) for p, s in D["hilfe"].items()]
    for k, liste in D["tratsch_morgen"].items():
        out += [("st.tratsch.morgen.%s.%d" % (k, i), p, s) for i, (p, s) in enumerate(liste)]
    out += [("st.morgen." + p, p, s) for p, s in D["morgen"].items()]
    return out


def zeile(zid, moddir):
    for k, wer, text in alle_zeilen(moddir):
        if k == zid:
            return wer, text
    return None, None
