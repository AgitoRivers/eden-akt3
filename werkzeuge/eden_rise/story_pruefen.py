# -*- coding: utf-8 -*-
"""Prüft module/eden_rise/story.json (Hauptstory, Phase A) – spoilerfrei.

Ausgabe nennt nur Fall-Nummern, neutrale IDs und Zahlen, nie Inhalte, Namen von Verantwortlichen oder Motive.
Prüft: Struktur und Verweise, Fairness (jedes Kettenglied auf zwei Wegen, nichts nur hinter Sex, jede Gegenhandlung
mit Spur und Umweg, kein vollständiger Beweisverlust), Lösbarkeit in mehreren Spielweisen, Holms Wissen am Morgen von Tag 2,
Alibis der Unschuldigen, gleiche Oberfläche in allen Fällen, zweite Wahrheit, Wochenbogen und die Zeitfenster der
Events (Holm, Megan, Lola, Alva) gegen die Hauptstory.
Aufruf: python werkzeuge\\eden_rise\\story_pruefen.py        Rückgabe 1 bei Fehlern.
"""
import collections, json, os, re, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
EDEN = os.path.dirname(os.path.dirname(HIER))    # werkzeuge\eden_rise -> Eden
STORY = os.path.join(EDEN, "module", "eden_rise", "story.json")
EVENTS = os.path.join(EDEN, "module", "eden_rise", "ereignisse.json")

from story_basis import (PERSONEN, WISSENDE_OK, VERDAECHTIGE, RAEUME, PHASEN, ZUVERLAESSIG, BEWEISKRAFT, FAKT_ARTEN,
                         WEG_ARTEN, SYSTEMQUELLEN, GLIEDER, AUSFALL_FENSTER, minuten, pms)

ID_FAKT = re.compile(r"^(r|z|h|f[1-5])_\d\d$")
BED_SCHLUESSEL = {"wert", "uhr", "flag", "item", "persona", "tag_ab", "phase", "gesehen", "alle", "eine", "nicht",
                  "kennt_gesichert", "kette_bekannt", "angst"}
FEHLER, WARN = [], []


def fehler(t):
    FEHLER.append(t)


def warn(t):
    WARN.append(t)


# ------------------------------------------------------------------ Bedingungen
def bed_pruefen(b, wo):
    if not isinstance(b, dict) or len(b) != 1:
        fehler("%s: Bedingung muss genau einen Schlüssel haben" % wo)
        return
    k, v = next(iter(b.items()))
    if k not in BED_SCHLUESSEL:
        fehler("%s: unbekannte Bedingung %s" % (wo, k))
    if k in ("alle", "eine"):
        for x in v:
            bed_pruefen(x, wo)
    elif k == "nicht":
        bed_pruefen(v, wo)
    elif k == "wert" and (len(v) != 3 or v[1] not in (">=", "<=", "==", ">", "<")):
        fehler("%s: wert-Bedingung %s" % (wo, v))


def bed_vertrauen(b):
    """Mindestvertrauen, das die Bedingung im günstigsten Fall verlangt."""
    if not b:
        return 0
    k, v = next(iter(b.items()))
    if k == "wert" and str(v[0]).startswith("vertrauen.") and v[1] in (">=", ">"):
        return v[2] + (1 if v[1] == ">" else 0)
    if k == "alle":
        return max([bed_vertrauen(x) for x in v] or [0])
    if k == "eine":
        return min([bed_vertrauen(x) for x in v] or [0])
    return 0


def bed_flags(b):
    """Flags, die im günstigsten Zweig unvermeidlich gebraucht werden."""
    if not b:
        return set()
    k, v = next(iter(b.items()))
    if k == "flag":
        return {v}
    if k == "alle":
        return set().union(*[bed_flags(x) for x in v]) if v else set()
    if k == "eine":
        zweige = [bed_flags(x) for x in v]
        return min(zweige, key=len) if zweige else set()
    return set()


# ------------------------------------------------------------------ Erreichbarkeit
class Szenario:
    def __init__(self, name, max_tag=7, max_v=5, ohne_intim=False, ohne_gruppen=(), ohne_personen=(), gh_bis=7,
                 ohne_flag_teil=()):
        self.name, self.max_tag, self.max_v, self.ohne_intim = name, max_tag, max_v, ohne_intim
        self.ohne_gruppen, self.ohne_personen = set(ohne_gruppen), set(ohne_personen)
        self.gh_bis, self.ohne_flag_teil = gh_bis, tuple(ohne_flag_teil)


def weg_ok(w, sz, blockiert):
    if w["id"] in blockiert or w["tage"][0] > sz.max_tag:
        return False
    if sz.ohne_intim and w.get("intim"):
        return False
    if w["gruppe"] in sz.ohne_gruppen or w.get("person") in sz.ohne_personen:
        return False
    b = w.get("bedingung")
    if b:
        if bed_vertrauen(b) > sz.max_v:
            return False
        if any(t in f for f in bed_flags(b) for t in sz.ohne_flag_teil):
            return False
    return True


def bekannt(fakten, sz, gh):
    blockiert = set()
    for g in gh:
        if g["tag"] <= sz.gh_bis:
            blockiert |= set(g["blockiert"])
    wissen = set()
    while True:
        neu = False
        for fid, f in fakten.items():
            if fid in wissen:
                continue
            for w in f["wege"]:
                if weg_ok(w, sz, blockiert) and all(b in wissen for b in w.get("braucht", [])):
                    wissen.add(fid)
                    neu = True
                    break
        if not neu:
            return wissen


def kette_loesbar(fall, wissen):
    offen = []
    for g in fall["glieder"]:
        if not any(set(s) <= wissen for s in g["beweis_saetze"]):
            offen.append(g["id"])
    return offen


# ------------------------------------------------------------------ Struktur
def fakt_pruefen(f, alle_ids, wo):
    fid = f["id"]
    if not ID_FAKT.match(fid):
        fehler("%s: Fakt-ID %s nicht neutral" % (wo, fid))
    if f["art"] not in FAKT_ARTEN:
        fehler("%s: %s art %s" % (wo, fid, f["art"]))
    if f["zuverlaessigkeit"] not in ZUVERLAESSIG:
        fehler("%s: %s Zuverlässigkeit %s" % (wo, fid, f["zuverlaessigkeit"]))
    try:
        minuten(f["zeit"])
    except ValueError:
        fehler("%s: %s Zeit %s" % (wo, fid, f["zeit"]))
    if "zeit_pms" in f and f["zeit_pms"] != pms(f["zeit"]):
        fehler("%s: %s PMS-Zeit passt nicht zur Schiffszeit" % (wo, fid))
    if f["quelle"] not in SYSTEMQUELLEN and f["quelle"] not in WISSENDE_OK:
        fehler("%s: %s Quelle %s" % (wo, fid, f["quelle"]))
    for p in f["wissende"]:
        if p not in WISSENDE_OK:
            fehler("%s: %s wissende %s" % (wo, fid, p))
    for u in f.get("uebermittlung", []):
        if u["an"] not in WISSENDE_OK:
            fehler("%s: %s Übermittlung an %s" % (wo, fid, u["an"]))
        minuten(u["zeit"])
    if not f["wege"]:
        fehler("%s: %s hat keinen Weg" % (wo, fid))
    if not f["wahr"]:
        gegen = f.get("widerlegt_durch", [])
        if not gegen:
            fehler("%s: %s ist unwahr, aber nichts widerlegt es" % (wo, fid))
        for g in gegen:
            if g not in alle_ids:
                fehler("%s: %s widerlegt durch unbekanntes %s" % (wo, fid, g))
        if not any(alle_ids.get(g, {}).get("zuverlaessigkeit") in BEWEISKRAFT for g in gegen):
            fehler("%s: %s wird nur durch Aussagen widerlegt" % (wo, fid))
    if f["zuverlaessigkeit"] == "geruecht":
        fehler("%s: %s ist ein Gerücht – Tratsch gehört in tipps, nicht in Fakten" % (wo, fid))
    for w in f["wege"]:
        wid = w.get("id", "?")
        if w["art"] not in WEG_ARTEN:
            fehler("%s: %s Weg-Art %s" % (wo, wid, w["art"]))
        a, b = w["tage"]
        if not (1 <= a <= b <= 7):
            fehler("%s: %s Tage %s" % (wo, wid, w["tage"]))
        if w.get("ort") and w["ort"] not in RAEUME:
            fehler("%s: %s Ort %s" % (wo, wid, w["ort"]))
        if w.get("person") and w["person"] not in PERSONEN:
            fehler("%s: %s Person %s" % (wo, wid, w["person"]))
        for ph in w.get("phasen", []):
            if ph not in PHASEN:
                fehler("%s: %s Phase %s" % (wo, wid, ph))
        if w.get("bedingung"):
            bed_pruefen(w["bedingung"], "%s %s" % (wo, wid))
        for x in w.get("braucht", []):
            if x not in alle_ids:
                fehler("%s: %s braucht unbekanntes %s" % (wo, wid, x))
        if not w.get("gruppe"):
            fehler("%s: %s ohne Gruppe" % (wo, wid))


def fall_pruefen(fall, zw_fakten):
    n = fall["nr"]
    wo = "Fall %d" % n
    eigene = {f["id"]: f for f in fall["fakten"]}
    if len(eigene) != len(fall["fakten"]):
        fehler("%s: doppelte Fakt-IDs" % wo)
    alle = dict(eigene)
    alle.update(zw_fakten)
    for f in fall["fakten"]:
        fakt_pruefen(f, alle, wo)
    weg_ids = collections.Counter(w["id"] for f in fall["fakten"] for w in f["wege"])
    for wid, c in weg_ids.items():
        if c > 1:
            fehler("%s: Weg-ID %s doppelt" % (wo, wid))
    alle_wege = {w["id"]: w for f in list(fall["fakten"]) + list(zw_fakten.values()) for w in f["wege"]}

    # Kette
    if [g["id"] for g in fall["glieder"]] != list(GLIEDER):
        fehler("%s: Kettenglieder weichen von der gemeinsamen Oberfläche ab" % wo)
    for g in fall["glieder"]:
        if g["frage"] != GLIEDER.get(g["id"]):
            fehler("%s: Frage zu Glied %s weicht ab" % (wo, g["id"]))
        if len(g["beweis_saetze"]) < 2:
            fehler("%s: Glied %s hat nur einen Beweissatz" % (wo, g["id"]))
        for i, s in enumerate(g["beweis_saetze"], 1):
            for x in s:
                if x not in alle:
                    fehler("%s: Glied %s Satz %d – unbekannter Fakt %s" % (wo, g["id"], i, x))
            if not any(alle.get(x, {}).get("zuverlaessigkeit") in BEWEISKRAFT for x in s):
                fehler("%s: Glied %s Satz %d enthält nur Aussagen" % (wo, g["id"], i))
            if any(not alle.get(x, {}).get("wahr", True) for x in s):
                fehler("%s: Glied %s Satz %d stützt sich auf eine Unwahrheit" % (wo, g["id"], i))

    # Widersprüche
    if not fall["widersprueche"]:
        fehler("%s: kein Widerspruch für \"Das passt zeitlich nicht\"" % wo)
    for ws in fall["widersprueche"]:
        for x in [ws["aussage"], ws["nachfragen"]] + ws["gegen"] + ws["braucht"]:
            if x not in alle:
                fehler("%s: Widerspruch %s – unbekannter Fakt %s" % (wo, ws["id"], x))
        if alle.get(ws["aussage"], {}).get("art") != "aussage":
            fehler("%s: Widerspruch %s – Ausgang ist keine Aussage" % (wo, ws["id"]))
        if ws["beschuldigen"].get("markiert_wahrheit"):
            fehler("%s: Widerspruch %s markiert eine Beschuldigung als Wahrheit" % (wo, ws["id"]))

    # Gegenhandlungen
    tage = collections.Counter(g["tag"] for g in fall["gegenhandlungen"])
    for t, c in tage.items():
        if c > 1:
            fehler("%s: %d Gegenhandlungen an Tag %d (höchstens 1)" % (wo, c, t))
    alle_blockiert = set(x for g in fall["gegenhandlungen"] for x in g["blockiert"])
    for g in fall["gegenhandlungen"]:
        if g["spur"] not in alle:
            fehler("%s: %s ohne gültige Spur" % (wo, g["id"]))
        else:
            if min(w["tage"][0] for w in alle[g["spur"]]["wege"]) < g["tag"]:
                fehler("%s: %s – Spur ist vor der Gegenhandlung sichtbar" % (wo, g["id"]))
        for x in g["blockiert"] + g["umweg"]:
            if x not in alle_wege:
                fehler("%s: %s – unbekannter Weg %s" % (wo, g["id"], x))
        for x in g["umweg"]:
            if x in alle_blockiert:
                fehler("%s: %s – Umweg %s wird selbst blockiert" % (wo, g["id"], x))
        if g["blockiert"] and not g["umweg"]:
            fehler("%s: %s blockiert, nennt aber keinen Umweg" % (wo, g["id"]))
        if not g["blockiert"] and not g.get("notiz"):
            fehler("%s: %s ohne Gegenmittel-Notiz" % (wo, g["id"]))
        for x in g["blockiert"]:
            fid = x.rsplit("_w", 1)[0]
            rest = [w for w in alle[fid]["wege"] if w["id"] not in alle_blockiert]
            if not rest:
                fehler("%s: %s – Fakt %s verliert jeden Weg" % (wo, g["id"], fid))

    # Geständnis
    ge = fall["gestaendnis"]
    if not {"intim", "geschenk"} <= set(ge["nie_durch"]):
        fehler("%s: Geständnis darf nicht über Intimität/Geschenk laufen" % wo)
    if not (ge["kernsatz"].get("de") and ge["kernsatz"].get("en")):
        fehler("%s: Kernsatz unvollständig" % wo)
    if (fall["verantwortlich"] is None) == ge["moeglich"]:
        fehler("%s: Geständnis-Möglichkeit passt nicht zur Verantwortung" % wo)
    if fall["verantwortlich"] is not None and fall["verantwortlich"] not in VERDAECHTIGE:
        fehler("%s: Verantwortung außerhalb der Verdächtigen" % wo)
    for fw in ge["freiwillig"]:
        bed_pruefen(fw["bedingung"], wo + " Geständnis")
        if fw["ab_tag"] < 3:
            fehler("%s: freiwilliges Geständnis vor Tag 3" % wo)

    # Holm am Morgen von Tag 2 (persoenlich), danach Telefon
    h = fall["holm_tag1"]
    if len(h["weiss"]) < 2:
        fehler("%s: Holm weiß am Morgen von Tag 2 zu wenig" % wo)
    for x in h["weiss"] + list(h.get("auf_nachfrage", {}).values()):
        f = alle.get(x)
        if not f:
            fehler("%s: Holm-Wissen %s unbekannt" % (wo, x))
            continue
        tag1 = any(w.get("person") == "holm" and w["tage"][0] == 2 and w.get("phasen") == ["fruehstueck"]
                   and w["art"] != "handy" for w in f["wege"])     # persoenlich: Morgen von Tag 2, vor dem Abflug
        spaeter = any(w.get("person") == "holm" and w["art"] == "handy" and w["tage"][0] >= 2 for w in f["wege"])
        if not (tag1 and spaeter):
            fehler("%s: Holm-Wissen %s nicht am Morgen von Tag 2 UND per Telefon erreichbar" % (wo, x))

    # Tratsch
    if len(fall["tipps"]) < 2:
        fehler("%s: weniger als zwei Tratsch-Hinweise" % wo)
    gh_ids = {g["id"]: g for g in fall["gegenhandlungen"]}
    for t in fall["tipps"]:
        if t["wer"] not in ("lola", "alva"):
            fehler("%s: Tipp %s von %s" % (wo, t["id"], t["wer"]))
        if t["beweis"] or t["zuverlaessigkeit"] != "geruecht":
            fehler("%s: Tipp %s darf kein Beweis sein" % (wo, t["id"]))
        if t["zeigt_auf"] not in alle_wege:
            fehler("%s: Tipp %s zeigt auf unbekannten Weg" % (wo, t["id"]))
        else:
            w = alle_wege[t["zeigt_auf"]]
            if w["art"] in ("erinnerung", "freiwillig"):
                fehler("%s: Tipp %s zeigt auf einen Weg, den Duc nicht selbst gehen kann" % (wo, t["id"]))
            if w["tage"][1] < t["ab_tag"]:
                fehler("%s: Tipp %s kommt erst, wenn der Weg schon zu ist" % (wo, t["id"]))
        if t.get("nach"):
            if t["nach"] not in gh_ids:
                fehler("%s: Tipp %s nach unbekannter Gegenhandlung" % (wo, t["id"]))
            elif t["ab_tag"] <= gh_ids[t["nach"]]["tag"]:
                fehler("%s: Tipp %s kommt vor der Gegenhandlung" % (wo, t["id"]))

    # Auftakt-Erinnerungen
    if set(fall["auftakt"]) != {"chiara", "rosi", "siri"}:
        fehler("%s: Auftakt-Erinnerungen unvollständig" % wo)
    for pid, fid in fall["auftakt"].items():
        f = alle.get(fid)
        if not f or not any(w["art"] == "erinnerung" and w.get("bedingung") == {"flag": "auftakt_hilfe_%s" % pid}
                            for w in f["wege"]):
            fehler("%s: Auftakt-Erinnerung für Hilfe %s fehlt oder ist falsch verdrahtet" % (wo, "abc"[
                ["chiara", "rosi", "siri"].index(pid)] if pid in ("chiara", "rosi", "siri") else "?"))

    # Passage und Zeitleiste
    p = fall["passage"]
    a, aus, holm, anker = (minuten(p[k]) for k in ("abfahrt", "ausfall", "holm_bruecke_ab", "ankern"))
    if not (holm < a < aus < anker):
        fehler("%s: Passage-Zeiten in falscher Reihenfolge" % wo)
    if not (minuten(AUSFALL_FENSTER[0]) <= aus <= minuten(AUSFALL_FENSTER[1])):
        fehler("%s: Ausfall außerhalb des gemeinsamen Fensters (Oberfläche wäre verschieden)" % wo)
    for suffix in ("_01", "_02"):
        f = eigene.get("f%d%s" % (n, suffix))
        if not f or minuten(f["zeit"]) != aus:
            fehler("%s: Ausfall-Fakt %s passt nicht zur Passage" % (wo, suffix))
    zl = [minuten(z["zeit"]) for z in fall["zeitleiste"]]
    if zl != sorted(zl):
        fehler("%s: Zeitleiste nicht sortiert" % wo)
    return eigene, alle


def loesbarkeit(fall, alle):
    wo = "Fall %d" % fall["nr"]
    gh = fall["gegenhandlungen"]
    szenarien = [
        Szenario("Standard"),
        Szenario("spät, ohne Romanze, Vertrauen höchstens 2", max_tag=6, max_v=2, ohne_intim=True),
        Szenario("bis Tag 4, Vertrauen höchstens 3", max_tag=4, max_v=3, gh_bis=4),
        Szenario("ohne Gespräch mit Holm", ohne_personen=["holm"]),
        Szenario("ohne gesicherten Streifen", ohne_gruppen=["streifen"]),
        Szenario("ohne Auftakt-Erinnerung", ohne_gruppen=["auftakt"]),
        Szenario("ohne Geständnis-Freigaben", ohne_flag_teil=["gestanden"]),
        Szenario("ohne Intimität", ohne_intim=True),
    ]
    ergebnis = []
    for sz in szenarien:
        offen = kette_loesbar(fall, bekannt(alle, sz, gh))
        ergebnis.append((sz.name, not offen))
        if offen:
            fehler("%s: nicht lösbar (%s) – offen: %s" % (wo, sz.name, ", ".join(offen)))
    # Jede Quelle verzichtbar (alle Gegenhandlungen ausgeführt)
    gruppen = sorted(set(w["gruppe"] for f in alle.values() for w in f["wege"]) - {"start"})
    kritisch = []
    for g in gruppen:
        offen = kette_loesbar(fall, bekannt(alle, Szenario("ohne " + g, ohne_gruppen=[g]), gh))
        if offen:
            kritisch.append("%s (%s)" % (g, ",".join(offen)))
    if kritisch:
        fehler("%s: einzelne Quelle unverzichtbar: %s" % (wo, "; ".join(kritisch)))
    ergebnis.append(("jede Quelle verzichtbar (%d)" % len(gruppen), not kritisch))
    # Alibis
    wissen = bekannt(alle, Szenario("Standard"), gh)
    for pid in VERDAECHTIGE:
        if pid == fall["verantwortlich"]:
            continue
        if not any(f.get("alibi_fuer") == pid and f["wahr"] and f["id"] in wissen for f in alle.values()):
            fehler("%s: eine unschuldige Verdächtige hat kein erreichbares Alibi" % wo)
    if fall["verantwortlich"] is None:
        for x in fall["gestaendnis"].get("entlastung_suendenbock", []):
            if x not in wissen:
                fehler("%s: Entlastung des Sündenbocks unvollständig erreichbar" % wo)
    return ergebnis


# ------------------------------------------------------------------ Zweite Wahrheit, Wochenbogen, Events
def zweite_wahrheit_pruefen(zw):
    fakten = {f["id"]: f for f in zw["fakten"]}
    for f in zw["fakten"]:
        fakt_pruefen(f, dict(fakten, r_14={"zuverlaessigkeit": "gesichert"}), "Zweite Wahrheit")
    # Akt 1 (seit 24.10.2026): nur Hinweise auf Alons Geraet, Aufloesung in Akt 3 - keine Routen, keine Kettenfunktion
    if zw.get("akt") != 3:
        fehler("Zweite Wahrheit: gehört in Akt 3 (akt = 3)")
    if zw.get("routen"):
        fehler("Zweite Wahrheit: Akt 1 hat keine Routen mehr")
    for f in zw["fakten"]:
        if "alon" in (f["inhalt"] + " " + f["codex"]).lower():
            fehler("Zweite Wahrheit: %s nennt Alon schon in Akt 1" % f["id"])
        if any(p in VERDAECHTIGE for p in f["wissende"]):
            fehler("Zweite Wahrheit: %s – ein Hinweis darf keine Verdächtige betreffen" % f["id"])
    if zw["megan_haltung"].get("zufall") is not False:
        fehler("Zweite Wahrheit: Megans Haltung darf nicht ausgewürfelt werden")
    return fakten


def wochenbogen_pruefen(wb, besuche, neben):
    ids = collections.Counter()
    gesetzt = {}
    exklusiv = set()
    for tag, d in wb.items():
        if tag not in [str(i) for i in range(1, 8)]:          # 7 Tage: Party (1) + 6 Krisentage
            fehler("Wochenbogen: Tag %s" % tag)
        for ph, szenen in d["phasen"].items():
            if ph not in PHASEN:
                fehler("Wochenbogen: Tag %s Phase %s" % (tag, ph))
            for s in szenen:
                ids[s["id"]] += 1
                if not s["titel"]:
                    fehler("Wochenbogen: Szene ohne Titel (Tag %s)" % tag)
                for fl in s["setzt"]:
                    gesetzt.setdefault(fl, (int(tag), ph))
                if s["exklusiv"]:
                    exklusiv.add("T%s %s" % (tag, ph))
                if s.get("bedingung"):
                    bed_pruefen(s["bedingung"], "Wochenbogen %s" % s["id"])
                for p in s["personen"]:
                    if p not in PERSONEN:
                        fehler("Wochenbogen: %s Person %s" % (s["id"], p))
                if s.get("ort") and s["ort"] not in RAEUME:
                    fehler("Wochenbogen: %s Ort %s" % (s["id"], s["ort"]))
    for sid, c in ids.items():
        if c > 1:
            fehler("Wochenbogen: Szene %s doppelt" % sid)
    soll = {"holm_evakuiert": (2, "fruehstueck"), "megan_angekuendigt": (4, "abend"), "megan_besuch": (5, "fruehstueck"),
            "megan_abgereist": (7, "abend"), "uhrzeit_widerspruch_gehoert": (1, "nacht"),
            "auftakt_gesehen": (1, "abend"), "cold_open_gesehen": (1, "fruehstueck"), "explosion": (1, "nacht"),
            "megan_ultimatum": (2, "fruehstueck"), "anhoerung_gehalten": (7, "tag"), "akt1_ende": (7, "nacht")}
    alt = {"festa", "bericht", "endfassung", "auslaufen", "zukunft", "schlussbild", "wendung", "der_satz", "brand",
           "technischer_weg", "megan_entwurf", "megan_abflug", "was_schreibst_du"}
    for sid in sorted(alt & set(ids)):
        fehler("Wochenbogen: %s gehört nicht mehr in Akt 1" % sid)
    for fl, wann in soll.items():
        if gesetzt.get(fl) != wann:
            fehler("Wochenbogen: Flag %s wird nicht an der vorgesehenen Stelle gesetzt" % fl)
    for pflicht in ("T1 fruehstueck", "T1 abend", "T1 nacht", "T5 nacht", "T7 tag", "T7 nacht"):
        if pflicht not in exklusiv:
            fehler("Wochenbogen: %s sollte eine exklusive Hauptszene haben" % pflicht)
    if neben["lola"]["freischaltung_tag"] != 3 or neben["alva"]["freischaltung_tag"] != 4:
        fehler("Nebenbögen: Freischaltung Lola Tag 3 / Alva Tag 4")
    if not neben["regeln"].get("nie_in_exklusiv"):
        fehler("Nebenbögen: dürfen exklusive Hauptszenen nicht verdrängen")
    return exklusiv


def phase_index(t, ph):
    return int(t) * 5 + PHASEN.index(ph)


def events_pruefen(story):
    if not os.path.exists(EVENTS):
        warn("ereignisse.json fehlt – Event-Abgleich übersprungen")
        return 0
    ev = json.load(open(EVENTS, encoding="utf-8"))["events"]
    m = story["besuche"]["megan"]
    von = phase_index(5, "tag")
    bis = phase_index(7, "abend")            # Akt 1: Megan bleibt bis zur Anhörung, fliegt nach dem Urteil
    abw = collections.Counter()
    for e in ev:
        w = e["wann"]
        roh = json.dumps(w.get("bedingung", {}))
        phasen = w.get("phasen") or PHASEN
        slots = [phase_index(t, ph) for t in range(w["tage"][0], w["tage"][1] + 1) for ph in phasen]
        if "megan_besuch" in json.dumps([o.get("folgen") for o in e["optionen"]]):
            fehler("Events: ein Event setzt megan_besuch selbst (das steuert die Hauptstory)")
        if '"flag": "megan_besuch"' in roh and '"nicht"' not in roh:
            if any(not (von <= s <= bis) for s in slots):
                abw["megan_fenster"] += 1
            text = (e["lage"] + " " + " ".join(z["text"] for z in e["zeilen"])).lower()
            if any(s >= phase_index(7, "abend") for s in slots) and ("morgen" in text or "tomorrow" in text):
                abw["megan_morgen_nach_abflug"] += 1
        if '"flag": "megan_angekuendigt"' in roh and "megan_besuch" not in roh:
            if any(s >= von for s in slots):
                abw["megan_ankuendigung_nach_landung"] += 1
            text = (e["lage"] + " " + " ".join(z["text"] for z in e["zeilen"])).lower()
            if "übermorgen" in text or "day after tomorrow" in text:
                abw["megan_ankuendigung_tag"] += 1
        teilnehmer = [v for k, v in e["personen"].items() if isinstance(v, str)]
        if "holm" in teilnehmer and e["art"] == "handy" and w["tage"][0] < 2:
            abw["holm_telefon_vor_evakuierung"] += 1
        if e["id"] in story["nebenboegen"]["lola"]["events"] and w["tage"][0] < 3:
            abw["lola_zu_frueh"] += 1
        if e["id"] in story["nebenboegen"]["alva"]["events"] and w["tage"][0] < 4:
            abw["alva_zu_frueh"] += 1
    if m["ankunft_event"] not in {e["id"] for e in ev}:
        fehler("Events: Ankunfts-Event für Megans Besuch fehlt")
    for k, c in abw.items():
        warn("Event-Zeitfenster gegen Hauptstory: %d × %s" % (c, k))
    return sum(abw.values())


# ------------------------------------------------------------------ Hauptteil
def main():
    sys.stdout.reconfigure(encoding="utf-8")
    story = json.load(open(STORY, encoding="utf-8"))
    print("Prüfung Hauptstory eden_rise (spoilerfrei)")
    zw = zweite_wahrheit_pruefen(story["zweite_wahrheit"])
    zeilen = []
    oberflaeche = set()
    for fall in story["faelle"]:
        eigene, alle = fall_pruefen(fall, zw)
        erg = loesbarkeit(fall, alle)
        oberflaeche.add((tuple(g["id"] for g in fall["glieder"]), tuple(sorted(fall["auftakt"])),
                         tuple(sorted(fall["holm_tag1"]))))
        zeilen.append("Fall %d: %d Fakten, %d Wege · %s" % (
            fall["nr"], len(fall["fakten"]), sum(len(f["wege"]) for f in fall["fakten"]),
            " · ".join("%s %s" % (n, "✓" if ok else "✗") for n, ok in erg)))
    if len(oberflaeche) != 1:
        fehler("Oberfläche: Fälle unterscheiden sich in sichtbarer Struktur")
    nrs = sorted(f["nr"] for f in story["faelle"])
    if nrs != [1, 2, 3, 4, 5]:
        fehler("Fälle: Nummern %s" % nrs)
    if any(f["verantwortlich"] is None for f in story["faelle"]):    # Fall 6 "niemand" am 27.10.2026 gestrichen
        fehler("Fälle: jeder Fall braucht eine Verantwortliche")
    exklusiv = wochenbogen_pruefen(story["wochenbogen"], story["besuche"], story["nebenboegen"])
    abw = events_pruefen(story)
    for z in zeilen:
        print(z)
    an = story.get("anhoerung") or {}
    if story.get("akt") == 1 and (an.get("tag") != 7 or an.get("richterin") != "megan" or len(an.get("ablauf", [])) != 7):
        fehler("Anhörung: Tag 7, Richterin Megan, sieben Schritte erwartet")
    print("Zweite Wahrheit (Akt 3): %d Hinweise in Akt 1, keine Routen" % len(zw))
    print("Wochenbogen: %d Tage, %d Szenen, exklusiv: %s" % (
        len(story["wochenbogen"]), sum(len(v) for t in story["wochenbogen"].values() for v in t["phasen"].values()),
        ", ".join(sorted(exklusiv, key=lambda s: (int(s[1]), PHASEN.index(s.split()[1]))))))
    print("Event-Zeitfenster gegen Hauptstory: %s" % ("passt" if not abw else "%d Abweichungen" % abw))
    for w in WARN:
        print("WARNUNG", w)
    for f in FEHLER:
        print("FEHLER", f)
    print("Ergebnis: %d Fehler, %d Warnungen" % (len(FEHLER), len(WARN)))
    sys.exit(1 if FEHLER else 0)


if __name__ == "__main__":
    main()
