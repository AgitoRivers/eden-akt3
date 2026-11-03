# -*- coding: utf-8 -*-
"""Automatischer Showrunner (16.10.2026) - baut jeden Tagesplan selbst aus geschriebenem Inhalt.

Fuer das Release darf kein Mensch und keine Cloud die Tage planen. Deshalb: alle Szenen sind vorab
geschrieben (module\\<modul>\\szenen.json, gebaut aus werkzeuge\\szenen_<modul>.py), und dieser Spielleiter
stellt daraus jeden Tag den Plan zusammen - abhaengig vom Spielstand:
  - feste Wendepunkte (Bibel arc.md) mit Varianten je Stand (wer steht ihm am naechsten, welche Wahrheit),
  - Pflicht-Phasen: die passendste Szene, Wahl-Phasen: 2-3 Optionen mit Abwechslung (verschiedene Frauen,
    Plot und Herz gemischt),
  - Bewertung: naechste Stufe eines Bogens, wer lange nicht dran war, Uhren, die hinterherhinken,
  - Grenzen (wie weit sie geht) aus Begehren/Vertrauen, Geheimnisse aus den Steckbriefen,
  - Tagesende: Wetter, Strom, Uhren nach der Bibel.
Ein handgeschriebener plaene\\tag<N>.json hat Vorrang (z. B. Tag 1). Das Sprachmodell spielt nur die Szenen.
Phasen, deren Inhalt erst am Abend feststeht (Finale, Nacht vor dem Ende), werden beim Betreten gefuellt."""
import copy, json, os, random, re

from . import figurenrahmen, plan as planmod, regeln, rollen

_CACHE = {}
GRENZEN = [
    "No touching beyond a brief, accidental contact.",
    "No touching beyond a brief, accidental contact.",
    "A touch on the arm or the hand at most; she is the one who pulls back.",
    "A held hand, a long hug, at most one kiss - then she stops it herself.",
    "Kissing and closeness are possible if the moment is right; she stops before it goes further unless they are alone behind a locked door.",
    "Anything she wants, if they are alone and it feels right to her.",
]


# ------------------------------------------------------------------ Grundlagen
# Module mit Hauptstory (eden_rise) haben keinen Szenen-Vorrat - nur Missionen (missionen.json, alle im Modul selbst;
# bis 18.10.2026 kamen die Dorf-Missionen zur Laufzeit aus dem alten Modul Gestrandet).
def vorrat(moddir):
    pfad = os.path.join(moddir, "szenen.json")
    if not os.path.exists(pfad):
        return _nur_missionen(moddir)
    st = os.path.getmtime(pfad)
    if _CACHE.get(pfad, (None,))[0] != st:
        _CACHE[pfad] = (st, json.load(open(pfad, encoding="utf-8")))
    return _CACHE[pfad][1]


def _nur_missionen(moddir):
    pfad = os.path.join(moddir, "missionen.json")
    if not os.path.exists(pfad):
        return None
    st = os.path.getmtime(pfad)
    if _CACHE.get(pfad, (None,))[0] != st:
        jobs = list(json.load(open(pfad, encoding="utf-8")).get("missionen", []))
        _CACHE[pfad] = (st, {"jobs": jobs, "_nur_missionen": True})
    return _CACHE[pfad][1]


def frauen(modul):
    return [pid for pid, p in modul["personen"].items() if p.get("romanzierbar")]


def nahe(z, pid):
    return z["werte"].get("vertrauen." + pid, 0) + z["werte"].get("begehren." + pid, 0)


def rang(z, modul, rng):
    fs = frauen(modul)
    zufall = {f: rng.random() for f in fs}
    return sorted(fs, key=lambda f: (-nahe(z, f), zufall[f]))


def herz_partner(z, modul, V):
    s = V.get("herz_schwelle", {"vertrauen": 4, "begehren": 4})
    kand = [f for f in frauen(modul) if z["werte"].get("vertrauen." + f, 0) >= s["vertrauen"]
            and z["werte"].get("begehren." + f, 0) >= s["begehren"]
            and not rollen.vergeben(z, modul, f)]
    zeit = {f: sum(1 for h in z.get("verlauf", []) + z.get("heute", []) if f in h.get("anwesend", [])) for f in kand}
    # Gleichstand: erst Begehren, dann mit wem Duc mehr Szenen verbracht hat (nicht die Listenreihenfolge)
    return sorted(kand, key=lambda f: (-nahe(z, f), -z["werte"].get("begehren." + f, 0), -zeit[f]))


def gespielt(z):
    """Ids der Szenen, die in diesem Durchlauf schon gespielt wurden (alle Tage + heute)."""
    return {h.get("szene") for h in z.get("verlauf", []) + z.get("heute", [])}


def tage_seit(z, pid):
    tage = [h["tag"] for h in z.get("verlauf", []) if pid in h.get("anwesend", [])]
    if any(pid in h.get("anwesend", []) for h in z.get("heute", [])):
        return 0
    return z["tag"] - max(tage) if tage else z["tag"]


def stufe(z, V, frau):
    seen = gespielt(z) | set(z.get("gesehene_storylets", []))
    return max([e["stufe"] for e in V["pool"] if e.get("frau") == frau and e.get("stufe") and
                (e["id"] in seen or (e.get("storylet") or "") in seen)] + [0])


def gilt(b, z, kontext=None):
    """regeln.gilt plus "wahrheit" (nur der Showrunner darf die Wahrheit kennen)."""
    if not b:
        return True
    b = dict(b)
    w = b.pop("wahrheit", None)
    if w is not None and (z["wahrheit"] != w if isinstance(w, str) else z["wahrheit"] not in w):
        return False
    return regeln.gilt(b, z, kontext)


def fuellen(text, werte):
    class Sicher(dict):
        def __missing__(self, k):
            return "{" + k + "}"
    return text.format_map(Sicher(werte)) if isinstance(text, str) else text


def texte_fuellen(o, werte):
    if isinstance(o, str):
        return fuellen(o, werte)
    if isinstance(o, list):
        return [texte_fuellen(x, werte) for x in o]
    if isinstance(o, dict):
        return {k: texte_fuellen(v, werte) for k, v in o.items()}
    return o


# ------------------------------------------------------------------ Szene bauen
def verbirgt(z, modul, V, pid):
    t = V.get("verbirgt", {}).get(pid, "")
    schuld = V.get("schuld", {}).get(z["wahrheit"])
    if schuld == pid and "wahrheit_geloest" not in z["flags"]:
        if z["tag"] >= modul["wahrheit"]["vorrat"][z["wahrheit"]].get("enthuellung_ab_tag", 4):
            t += " She caused the blackout: " + modul["wahrheit"]["vorrat"][z["wahrheit"]]["kern"] + " She is terrified it comes out."
        else:
            t += " " + V.get("schuld_vage", "She has a private reason to feel guilty about the blackout that she won't say.")
    return t.strip()


def grenze(z, modul, pid, gruppe, privat):
    lvl = min(z["werte"].get("begehren." + pid, 0), z["werte"].get("vertrauen." + pid, 0) + 1)
    if rollen.vergeben(z, modul, pid):
        lvl = min(lvl, 3)
    if gruppe:
        lvl = min(lvl, 2)
    elif privat < 4:
        lvl = min(lvl, 3)
    return GRENZEN[max(0, min(5, lvl))]


def figuren_fuellen(z, modul, V, s):
    anwesend = [p for p in s.get("anwesend", []) if not p.startswith("$")]
    gruppe = len([p for p in anwesend if modul["personen"][p].get("romanzierbar")]) > 1
    privat = modul["raeume"][s["ort"]].get("privat", 1)
    f = s.setdefault("figuren", {})
    for pid in [p for p in f if p != "*" and p not in anwesend]:      # Varianten tauschen Figuren aus
        del f[pid]
    for pid in anwesend:
        a = {"will": f[pid]} if isinstance(f.get(pid), str) else dict(f.get(pid) or {})
        a.setdefault("will", V.get("will_standard", {}).get(pid, "Be part of the scene in %s own way." % (
            "his" if modul["personen"][pid].get("pronomen") == "er" else "her")))
        extra = a.get("verbirgt", "")
        a["verbirgt"] = (verbirgt(z, modul, V, pid) + (" " + extra if extra else "")).strip() or "Nothing important."
        if modul["personen"][pid].get("romanzierbar"):
            a.setdefault("grenze", grenze(z, modul, pid, gruppe, privat))
        else:
            a.setdefault("grenze", "Stays in character; never touches Duc beyond a handshake.")
        f[pid] = a
    if any(p.startswith("$") for p in s.get("anwesend", [])):
        stern = dict(f.get("*") or {})
        stern.setdefault("will", "Stay a little longer than she should.")
        stern.setdefault("verbirgt", "Whatever she has hidden all day.")
        stern.setdefault("grenze", "Nothing beyond a kiss, if that.")
        f["*"] = stern
    return s


def anwenden(basis, var):
    s = copy.deepcopy(basis)
    for k, v in var.items():
        if k == "figuren" and isinstance(v, dict):
            s.setdefault("figuren", {}).update(copy.deepcopy(v))
        else:
            s[k] = copy.deepcopy(v)
    return s


def szene_aus(z, modul, V, e, werte):
    s = copy.deepcopy(e["szene"])
    for var in e.get("varianten", []):
        if gilt(var.get("wenn"), z):
            s = anwenden(s, var.get("szene", {}))
            break
    s["id"] = e["id"]
    if e.get("storylet"):
        s["storylet"] = e["storylet"]
    else:
        s["storylet"], s["improvisiert"] = None, True
    s.setdefault("ereignis", None)
    s.setdefault("ausgaenge", [])
    s.setdefault("max_zuege", 8)
    s = texte_fuellen(s, werte)
    return figuren_fuellen(z, modul, V, s)


# ------------------------------------------------------------------ Auswahl
def moeglich(z, modul, V, e, phase):
    tag = z["tag"]
    if e.get("phase") != phase or not (e["tage"][0] <= tag <= e["tage"][1]) or e.get("art") == "fix":
        return False
    if e.get("einmalig", True) and (e["id"] in gespielt(z) or (e.get("storylet") or "") in z.get("gesehene_storylets", [])):
        return False
    if e.get("frau") and e.get("stufe") and e["stufe"] > stufe(z, V, e["frau"]) + 1:
        return False                                # Boegen nie ueberspringen
    s = e["szene"]
    anwesend = [p for p in s.get("anwesend", []) if not p.startswith("$")]
    if any(p not in modul["personen"] for p in anwesend):
        return False
    kontext = {"anwesend": anwesend, "phase": phase}
    if not gilt(e.get("bedingung"), z, kontext):
        return False
    if e.get("storylet") and not regeln.gilt(modul["storylets"][e["storylet"]].get("bedingung"), z, kontext):
        return False
    status, _ = regeln.zugang(modul["raeume"][s["ort"]], z, kontext)
    return status == "offen"


MESSE = "crew_mess"


def nebenfiguren(modul, e):
    return [p for p in e["szene"].get("anwesend", []) if not p.startswith("$") and p in modul["personen"]
            and not modul["personen"][p].get("romanzierbar") and not modul["personen"][p].get("keine_nebenfigur")]


def an_land(modul, e):
    return modul["raeume"].get(e["szene"]["ort"], {}).get("bereich") == "land"


def punkte(z, V, e, rng, modul=None, heute=None):
    tag, g = z["tag"], float(e.get("gewicht", 1.0))
    if e.get("frau"):
        if e.get("stufe") and e["stufe"] == stufe(z, V, e["frau"]) + 1:
            g += 2.5
        g += min(3.0, 0.6 * tage_seit(z, e["frau"]))
    if modul is not None:                           # Abwechslung (17.10.2026): Messe selten, Nebenfiguren oft
        heute = heute or {}
        if e["szene"]["ort"] == MESSE and heute.get("messe"):
            g -= 3.0
        npc = nebenfiguren(modul, e)               # bewusst kleiner als der Bogen-Bonus (+2.5): die Regeln in
        if npc and not heute.get("npc"):            # waehlen/plan_bauen sichern die Mischung, die Frauen bleiben vorn
            g += 1.0
        g += sum(min(0.8, 0.25 * tage_seit(z, p)) for p in npc)
    soll = V.get("uhr_soll", {"reparatur": 1.3, "rettung": 0.9})
    u = e.get("uhr")
    if u in soll:
        rueckstand = soll[u] * (tag - 1) - z["uhren"].get(u, 0)
        if rueckstand > 0:
            g += min(2.5, 0.8 * rueckstand)
    if e.get("art") == "hinweis" and tag <= 3:
        g += 2.0
    return g + rng.random() * 0.8


def ersetzen(gewaehlt, kand, passt, anzahl):
    """Fehlt in der Auswahl eine Option, die passt, ersetzt die beste passende die schwaechste Nicht-Plot-Option."""
    if any(passt(x) for x in gewaehlt):
        return
    neu = next((e for e in kand if passt(e) and e not in gewaehlt), None)
    if not neu:
        return
    weg = next((x for x in reversed(gewaehlt) if x.get("art") not in ("plot", "hinweis")), None)
    if len(gewaehlt) < anzahl:
        gewaehlt.append(neu)
    elif weg:
        gewaehlt[gewaehlt.index(weg)] = neu


def waehlen(z, modul, V, phase, rng, anzahl, heute=None):
    kand = [e for e in V["pool"] if moeglich(z, modul, V, e, phase)]
    wert = {e["id"]: punkte(z, V, e, rng, modul, heute) for e in kand}
    kand.sort(key=lambda e: -wert[e["id"]])
    normal = [e for e in kand if e.get("art") != "reserve"]
    if len(normal) >= min(anzahl, 2):          # Reserve-Szenen nur, wenn sonst zu wenig zur Wahl steht
        kand = normal
    if anzahl == 1:
        return kand[:1]
    gewaehlt = []
    for e in kand:                                   # erst: verschiedene Frauen
        if len(gewaehlt) >= anzahl:
            break
        if e.get("frau") and any(x.get("frau") == e["frau"] for x in gewaehlt):
            continue
        gewaehlt.append(e)
    if not any(x.get("art") in ("plot", "hinweis") for x in gewaehlt):       # mindestens eine Plot-Option
        plot = next((e for e in kand if e.get("art") in ("plot", "hinweis") and e not in gewaehlt), None)
        if plot:
            gewaehlt = gewaehlt[:anzahl - 1] + [plot]
    job = next((e for e in kand if e.get("art") == "job" and e not in gewaehlt), None)
    if job and anzahl > 1 and not any(x.get("art") == "job" for x in gewaehlt) and rng.random() < 0.5:
        # Geld verdienen soll regelmaessig zur Wahl stehen (16.10.2026) - ersetzt die schwaechste Nicht-Plot-Option
        weg = next((x for x in reversed(gewaehlt) if x.get("art") not in ("plot", "hinweis")), None)
        if weg and len(gewaehlt) >= anzahl:
            gewaehlt[gewaehlt.index(weg)] = job
        elif len(gewaehlt) < anzahl:
            gewaehlt.append(job)
    # Abwechslung (17.10.2026): hoechstens eine Messe-Option, ab Tag 2 mindestens eine Option an Land
    # Plot-/Hinweis-Szenen bleiben stehen (die "mindestens eine Plot-Option" von oben); ersetzt wird eine andere Messe
    messe = sorted([x for x in gewaehlt if x["szene"]["ort"] == MESSE], key=lambda x: x.get("art") in ("plot", "hinweis"))
    for x in messe[:-1]:
        if x.get("art") in ("plot", "hinweis"):
            continue
        neu = next((e for e in kand if e["szene"]["ort"] != MESSE and e not in gewaehlt), None)
        if neu:
            gewaehlt[gewaehlt.index(x)] = neu
    if z["tag"] >= 2:
        ersetzen(gewaehlt, kand, lambda e: an_land(modul, e), anzahl)
    for e in kand:                                   # notfalls auffuellen
        if len(gewaehlt) >= 2:
            break
        if e not in gewaehlt:
            gewaehlt.append(e)
    return gewaehlt


# ------------------------------------------------------------------ Wendepunkte (Code baut aus Vorlagen)
def vorlage(V, *pfad):
    o = V["vorlagen"]
    for p in pfad:
        o = o[p]
    return copy.deepcopy(o)


def fix_szenen(z, modul, V, phase, rng, werte):
    tag, schl = z["tag"], "%d/%s" % (z["tag"], phase)
    art = V.get("fixplan", {}).get(schl)
    if not art:
        return None
    reihe = rang(z, modul, rng)
    if art == "sturm":
        w = reihe[0]
        return [szene_roh(z, modul, V, vorlage(V, "sturm", w), "storm_night_" + w, werte, storylet="storm_night")]
    if art == "konfrontation":
        return [konfrontation(z, modul, V, rng, werte)]
    if art == "festa":
        return [szene_roh(z, modul, V, vorlage(V, "festa", w), "festa_" + w, werte, storylet="la_festa") for w in reihe[:3]]
    if art == "ponr":
        return [ponr(z, modul, V, werte)]
    return None


def szene_roh(z, modul, V, s, sid, werte, storylet=None):
    s["id"] = sid
    s["storylet"] = storylet
    if not storylet:
        s["improvisiert"] = True
    s.setdefault("ereignis", None)
    s.setdefault("ausgaenge", [])
    s.setdefault("max_zuege", 8)
    return figuren_fuellen(z, modul, V, texte_fuellen(s, werte))


def konfrontation(z, modul, V, rng, werte):
    k = vorlage(V, "konfrontation")
    s = k["szene"]
    richtig = z["wahrheit"]
    falsch = [x for x in k["optionen"] if x != richtig]
    rng.shuffle(falsch)
    wahl = [richtig] + falsch[:2]
    rng.shuffle(wahl)
    optionen = []
    for key in wahl:
        o = dict(k["optionen"][key])
        if key == richtig:
            o["folgen"] = [{"flag": "wahrheit_geloest"}, {"codex": k["aufloesung"][key]}] + k["belohnung"][key]
        else:
            o["folgen"] = k["strafe"][key] + [{"codex": "Falscher Verdacht: " + o["text"]}]
        optionen.append(o)
    optionen.append(dict(k["schweigen"], folgen=[{"flag": "geschwiegen"}]))
    s["wahlmoment"] = {"nach_zug": 2, "frage": k["frage"], "optionen": optionen}
    return szene_roh(z, modul, V, s, "who_did_it", werte)


def ponr(z, modul, V, werte):
    s = vorlage(V, "ponr")
    diesel = z["werte"].get("diesel", 0)
    o = s["wahlmoment"]["optionen"]
    if diesel < 1:            # kein Diesel mehr: Unit-01 nur mit Petrus Kanister - kostet Ruf statt Diesel
        o[0] = vorlage(V, "ponr_ohne_diesel")
    return szene_roh(z, modul, V, s, "point_of_no_return", werte)


def verabredung_verschieben(z, modul, v):
    """Dieser Abend ist besetzt: Die Zusage gilt weiter, am naechsten Abend ohne anderes Date."""
    belegt = {x["tag"] for x in z["verabredungen"] if x is not v and x["phase"] == v["phase"]}
    v["tag"] = z["tag"] + 1
    while v["tag"] in belegt:
        v["tag"] += 1
    wann = "tomorrow evening" if v["tag"] == z["tag"] + 1 else "the evening of day %d" % v["tag"]
    z["meldungen"].append({"titel": "📅 %s moves your date" % modul["personen"][v["pid"]]["name"].split()[0],
                           "kurz": "Tonight is taken. She says: %s instead." % wann, "folgen": []})


def verabredung_versetzt(z, modul):
    """Phasenende: Ein Date stand zur Wahl und wurde nicht gespielt - egal ob andere Szene, Ausflug oder Phase beendet."""
    from . import chronik, zustand
    inhalt = ((z.get("plan") or {}).get("phasen") or {}).get(z["phase"]) or {}
    gespielt = {h.get("szene") for h in z["heute"] if h.get("phase") == z["phase"]}
    for s in inhalt.get("szenen") or []:
        sid = s.get("id") or ""
        if not sid.startswith("date_") or sid in gespielt or s.get("versetzt") or sid[5:] not in modul["personen"]:
            continue
        s["versetzt"] = True
        pid = sid[5:]
        n = modul["personen"][pid]["name"].split()[0]
        zeilen = zustand.folgen_anwenden(z, modul, [{"wert": "vertrauen." + pid, "delta": -1}])
        satz, wichtig, dauer = chronik.MOMENTE["stood_up"]
        chronik.eintragen(z, modul, "moment", satz.format(n=n), wer=[pid], dabei=[], wichtig=wichtig, dauer=dauer,
                          moment="stood_up")
        z["meldungen"].append({"titel": "📅 %s waited for you" % n, "kurz": "You stood her up.", "folgen": zeilen})


def verabredung_einbauen(z, modul, phase, inhalt):
    """Eine angenommene Einladung (Geste) garantiert eine Szene mit ihr (16.10.2026). Live-Spieltest 31.10.2026: Bis dahin
    verschwand die Zusage still, wenn sie an dem Abend ohnehin in einer Szene war."""
    z["verabredungen"] = [v for v in z.get("verabredungen", []) if v["tag"] >= z["tag"]]    # Reste aus alten Spielstaenden
    offen = [v for v in z["verabredungen"] if v["tag"] == z["tag"] and v["phase"] == phase]
    for v in offen:
        pid = v["pid"]
        if inhalt.get("dynamisch") or inhalt.get("szenen") is None or \
                any(pid in s.get("anwesend", []) and not s.get("frei") for s in inhalt["szenen"]):
            verabredung_verschieben(z, modul, v)
            continue
        z["verabredungen"].remove(v)
        p = modul["personen"][pid]
        kontext = {"anwesend": [pid], "phase": phase}
        # Von Duc gewaehlter Ort (17.10.2026, Karte im Handy): eine bestandene Probe gilt weiter, nur "gesperrt" faellt
        # zurueck (z. B. Gegenstand inzwischen verkauft). Ohne Wahl wie bisher: ihr Abend-Ort oder das Sonnendeck.
        ort = v.get("ort")
        gewaehlt = bool(ort in modul["raeume"] and regeln.zugang(modul["raeume"][ort], z, kontext)[0] != "gesperrt")
        if not gewaehlt:
            ort = (p.get("ablauf") or {}).get(phase) or "sun_deck"
            if ort not in modul["raeume"] or regeln.zugang(modul["raeume"][ort], z, kontext)[0] != "offen":
                ort = "sun_deck"
        lieb = gewaehlt and ort in (p.get("lieblingsorte") or [])
        n = p["name"].split()[0]
        raum = re.sub(r"\s*\([^)]*\)", "", modul["raeume"][ort]["label"]).strip()
        if raum.split()[0].endswith("'s"):              # "Alva's bar" ohne Artikel
            pass
        elif raum.startswith("The ") or raum.startswith("VIP"):
            raum = "the " + raum[4:] if raum.startswith("The ") else "the " + raum
        else:
            raum = "the " + raum[0].lower() + raum[1:]
        lage = "Duc asked %s to spend the evening with him, just the two of them - and she said yes." % n
        if gewaehlt:
            lage += " He picked the place himself: %s." % raum
            if lieb:
                lage += " It is one of her favourite places, and he knew it."
        lage += " Now she is here, a little early, pretending she isn't."
        will = "Have this evening with Duc and find out what it means."
        if lieb:
            will += " He chose one of her favourite places for it - that touches her more than she shows at first."
        s = {"id": "date_%s" % pid, "titel": "An evening with %s" % n, "ort": ort, "anwesend": [pid], "zeit": "21:30",
             "ausgangslage": lage,
             "frage": "What does the evening become?",
             "figuren": {pid: {"will": will}},
             "ausgaenge": [{"wenn": "They have a good evening together.", "folgen": [{"wert": "vertrauen." + pid, "delta": 1}]}],
             "max_zuege": 8, "begruendung_ort": "Duc chose this place for the date." if gewaehlt else "Duc invited her for the evening.",
             "storylet": None, "improvisiert": True}
        if lieb:        # kleiner Bonus (+4/+4, ein Erlebnis waeren 8) am Szenenende ohne Richter - ohne Deckel, denn
            # eingeladen wird ab Vertrauen 2, da stehen Gespraeche oft schon am Deckel von Stufe 3
            s["immer"] = [{"punkte": "vertrauen." + pid, "n": 4}, {"punkte": "begehren." + pid, "n": 4}]
        if figurenrahmen.gilt(modul, pid):               # der Abend zaehlt fest, kein Richter (Duc 31.10.2026)
            s["ausgaenge"] = []
            s["immer"] = s.get("immer", []) + [{"wert": "vertrauen." + pid, "delta": 1}]
        s = figuren_fuellen(z, modul, vorrat(z["plan"]["_moddir"]) if z.get("plan", {}).get("_moddir") else {}, s)
        karten = inhalt["szenen"]
        frei = [i for i, x in enumerate(karten) if x.get("frei")]
        eigene = [i for i in frei if pid in karten[i].get("anwesend", [])]
        if eigene:                                       # das Date ersetzt ihre freie Karte, sonst die letzte freie
            karten[eigene[0]] = s
        elif len(karten) >= 3 and frei:
            karten[frei[-1]] = s
        else:
            karten.append(s)


def phase_fuellen(z, modul, phase):
    """Fuer dynamische Phasen: Inhalt erst beim Betreten bauen (Finale, Nacht vor dem Ende)."""
    V = vorrat(z["plan"]["_moddir"])
    rng = random.Random("%s-%d-%s" % (z["id"], z["tag"], phase))
    werte = werte_fuer(z, modul, V)
    art = V["dynamisch"]["%d/%s" % (z["tag"], phase)]
    reihe = rang(z, modul, rng)
    partner = herz_partner(z, modul, V)
    if art == "nacht6":
        feuer = z["uhren"].get("katastrophe", 0) >= 5 or (
            z["wahrheit"] in ("wette", "yasin") and "wahrheit_geloest" not in z["flags"] and z["werte"].get("strom", 0) <= 2)
        if feuer:
            z["flags"].append("feuer")
            s = szene_roh(z, modul, V, vorlage(V, "feuer"), "battery_fire", werte)
        else:
            w = reihe[0]
            s = szene_roh(z, modul, V, vorlage(V, "nacht6", w), "last_quiet_night_" + w, werte)
    elif art == "finale":
        ausgang = next((u for u in [f[4:-5] for f in z["flags"] if f.startswith("uhr_") and f.endswith("_voll")]
                        if u in ("reparatur", "rettung", "katastrophe")), V.get("standard_ausgang", "rettung"))
        if "feuer" in z["flags"]:                    # Batteriefeuer schlaegt alles: das Boot ist verloren
            ausgang = "katastrophe"
        z["flags"].append("ende_" + ausgang)
        dabei = (partner[:1] or reihe[:1]) + [w for w in reihe if w not in partner[:1]][:1]
        s = vorlage(V, "finale", ausgang)
        s["anwesend"] = dabei
        s = szene_roh(z, modul, V, s, "last_night_" + ausgang, dict(werte, partner=modul["personen"][dabei[0]]["name"]))
    elif art == "epilog":
        if partner:
            z["flags"].append("herz_" + partner[0])
            s = szene_roh(z, modul, V, vorlage(V, "epilog", partner[0]), "epilogue_" + partner[0], werte)
        else:
            z["flags"].append("herz_allein")
            s = szene_roh(z, modul, V, vorlage(V, "epilog", "allein"), "epilogue_alone", werte)
        opt = vorlage(V, "persona_wahl")
        if not partner:
            opt["optionen"] = [o for o in opt["optionen"] if not o.get("nur_mit_partner")]
        for o in opt["optionen"]:
            o.pop("nur_mit_partner", None)
        s["wahlmoment"] = opt
    else:
        raise ValueError("Unbekannte dynamische Phase %s" % art)
    z["plan"]["phasen"][phase] = {"dynamisch": True, "szenen": [s]}
    return s


# ------------------------------------------------------------------ Tagesplan
def werte_fuer(z, modul, V):
    return {"strom": z["werte"].get("strom", 0), "diesel": z["werte"].get("diesel", 0), "tag": z["tag"],
            "wetter": (z.get("plan") or {}).get("wetter_text", "")}


def tagesende(z, V, rng):
    tag = z["tag"]
    wetter = "sturm" if tag == V.get("sturm_tag", 3) else ("klar" if rng.random() < 0.6 else "bewoelkt")
    t = V.get("takt", {})
    regeln_ende = [{"wert": "strom", "delta": t.get("strom", {}).get(wetter, 0)},
                   {"wert": "energie", "delta": 2},
                   {"flag": "siri_frei", "wenn": {"flag": "uhr_siri_marke_voll"}},       # Uhr voll = Schluss mit Yasin
                   {"wert": "ruf", "delta": -2, "flag": "video_folge", "codex": "Yasin's video is online: 'STRANDED ON A BILLIONAIRE YACHT'.",
                    "wenn": {"alle": [{"flag": "uhr_yasin_video_voll"}, {"nicht": {"flag": "video_folge"}}]}},
                   {"uhr": "katastrophe", "delta": 1, "wenn": {"wert": ["strom", "<=", 2]}},
                   {"wert": "moral", "delta": -1, "wenn": {"wert": ["strom", "<=", 1]}}]
    if tag % 2 == 0:          # Yasin dreht jeden zweiten Tag - voll wird die Uhr nur, wenn Duc ihm hilft
        regeln_ende.insert(2, {"uhr": "yasin_video", "delta": 1, "wenn": {"nicht": {"flag": "video_gestoppt"}}})
    if tag == 6:
        regeln_ende.append({"uhr": "katastrophe", "delta": 6, "wenn": {"flag": "feuer"}})
    return wetter, regeln_ende


def plan_bauen(z, modul, moddir):
    V = vorrat(moddir)
    if not V or V.get("_nur_missionen"):
        return None
    tag = z["tag"]
    rng = random.Random("%s-%d" % (z["id"], tag))
    wetter, ende = tagesende(z, V, rng)
    tg = V.get("tage", {}).get(str(tag), {})
    p = {"_showrunner": "auto (kern/showrunner.py)", "_moddir": moddir, "tag": tag, "wetter": wetter,
         "wetter_text": V.get("wetter_text", {}).get(wetter, ""),
         "spannung": tg.get("spannung", ""), "spannung_spieler": (tg.get("spieler", "") + " " +
                                                                  V.get("wetter_spieler", {}).get(wetter, "")).strip(),
         "tagesende": ende, "phasen": {}}
    z_tmp = dict(z, plan=p)
    werte = werte_fuer(z_tmp, modul, V)
    zr = modul["zeitraster"]
    heute = {"messe": False, "npc": False}            # was der Tag bisher schon bietet (Abwechslung, 17.10.2026)
    for ph in zr["phasen"]:
        if "%d/%s" % (tag, ph) in V.get("dynamisch", {}):
            p["phasen"][ph] = {"dynamisch": True, "szenen": []}
            continue
        fix = fix_szenen(z, modul, V, ph, rng, werte)
        if fix:
            p["phasen"][ph] = {"szenen": fix, "fix": True}      # Wendepunkt: keine Kabine statt dessen
            continue
        anzahl = 1 if ph in zr["pflicht"] else 3
        es = waehlen(z, modul, V, ph, rng, anzahl, heute)
        if ph == "abend" and tag >= 2 and not heute["npc"] and anzahl > 1:
            # mindestens eine Nebenfigur pro Tag: spaetestens am Abend steht eine zur Wahl
            kand = sorted([e for e in V["pool"] if moeglich(z, modul, V, e, ph) and e not in es],
                          key=lambda e: -punkte(z, V, e, rng, modul, heute))
            ersetzen(es, kand, lambda e: bool(nebenfiguren(modul, e)), anzahl)
        for e in es:                                 # schon eine Messe im Angebot -> spaeter moeglichst keine mehr
            heute["messe"] |= e["szene"]["ort"] == MESSE
            heute["npc"] |= bool(nebenfiguren(modul, e))
        p["phasen"][ph] = {"szenen": [szene_aus(z, modul, V, e, werte) for e in es]}
    fehler, warn = planmod.pruefe(p, modul, z)
    # Szenen, an denen die Pruefung scheitert, fliegen raus (Wahl-Phase behaelt mind. 2) - Rest wird gemeldet.
    for _ in range(3):
        if not fehler:
            break
        weg = {f.split(":")[0] for f in fehler if "/" in f.split(":")[0]}
        for ph, inhalt in p["phasen"].items():
            if inhalt.get("dynamisch"):
                continue
            rest = [s for s in inhalt["szenen"] if "%s/%s" % (ph, s["id"]) not in weg]
            if len(rest) >= (1 if ph in zr["pflicht"] else 2):
                inhalt["szenen"] = rest
        fehler, warn = planmod.pruefe(p, modul, z)
    p["_fehler"], p["_warnungen"] = fehler, warn
    try:
        ordner = os.path.join(moddir, "plaene_auto")
        os.makedirs(ordner, exist_ok=True)
        json.dump(p, open(os.path.join(ordner, "%s_tag%d.json" % (z["id"], tag)), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
    except OSError:
        pass
    return p
