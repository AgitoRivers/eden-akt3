# -*- coding: utf-8 -*-
"""Hauptstory eden_rise - Bausteine, Kataloge und Zeitrechnung (17.10.2026).

VERTRAULICH: Die Daten, die mit diesen Bausteinen gebaut werden, enthalten die Aufloesung aller fuenf Faelle.
Ausgaben, Logs und Dateinamen bleiben spoilerfrei: Faelle heissen nur "Fall 1-5", Fakten tragen neutrale IDs
(r_ Rahmen, z_ zweite Wahrheit, h_ harmlose Privatsachen, f<N>_ Fall N), nie Namen von Verantwortlichen.

Faktenmodell (Dossier Kap. 7): jeder Fakt hat Inhalt, Zeit (Schiffszeit), Quelle, Zuverlaessigkeit, Wissende
(Stand Tag 2 morgens), optional Uebermittlungen (wer erfaehrt es wann wie) und Wege (wie Duc es erfaehrt).
Zuverlaessigkeit:
  gesichert   technische Aufzeichnung oder Sachspur (Protokoll, Speicher, Bauteil)
  belastbar   Dokument mit Urheber und Zeit (Plan, Notiz, Wettbuch, Nachricht)
  beobachtet  Ducs eigene Beobachtung (z. B. auf der Party)
  aussage     Behauptung einer Figur - kann falsch sein (wahr=False)
  geruecht    Tratsch (Lola/Alva) - zeigt nur, WO man suchen sollte, nie Beweis
Uhren: Schiffszeit ist die Referenz (Bruecke, Handys, Kamera, GPS, Maschinenbuch). Die Energiesteuerung (PMS)
geht 14 Minuten nach; PMS-Zeiten werden hier aus der Schiffszeit berechnet, nie von Hand eingetragen.
"""
import re

FRAUEN = ["chiara", "sophia", "lea", "rosi", "siri"]
NEBEN = ["toto", "yasin", "holm", "elsa", "alva", "petru", "casanova", "lola", "megan", "maxwell", "jana", "yamamoto"]
PERSONEN = FRAUEN + NEBEN
WISSENDE_OK = set(PERSONEN) | {"duc"}
VERDAECHTIGE = ["chiara", "lea", "sophia", "rosi", "yasin"]
RAEUME = ["crew_mess", "crew_corridor", "galley", "duc_cabin", "bridge", "main_salon", "aft_deck", "sun_deck",
          "solar_deck", "foredeck", "swim_platform", "tender_garage", "power_room", "generator_room", "workshop",
          "vip_cabin", "village_harbour", "alvas_bar", "petru_workshop", "village_piazza"]
AN_LAND = ["village_harbour", "alvas_bar", "petru_workshop", "village_piazza"]
PHASEN = ["fruehstueck", "tag", "nachmittag", "dinner", "abend", "nacht"]
ZUVERLAESSIG = ["gesichert", "belastbar", "beobachtet", "aussage", "geruecht"]
BEWEISKRAFT = {"gesichert", "belastbar", "beobachtet"}
FAKT_ARTEN = ["ereignis", "dokument", "messung", "gegenstand", "beobachtung", "aussage", "nachricht", "abgeleitet"]
WEG_ARTEN = {
    "sichern": "Day 2: secure the event record of the power management system (becomes evidence)",
    "untersuchen": "Examine a place or object (costs the phase)",
    "befragen": "Talk to a person (the answer depends on trust or a condition)",
    "handy": "Call or message (Holm in hospital, Petru, Elsa, Megan)",
    "abgleichen": "zwei bekannte Fakten zusammenlegen (z. B. Uhrzeiten) - kostet keine Phase",
    "anordnen": "Command order (from day 2, Duc leads) - costs trust or backing",
    "freiwillig": "The character offers it of their own accord once the condition is met",
    "tausch": "Trade - real information, but a new dependency",
    "erinnerung": "Duc's own memory of the opening (only if he was there)",
    "pflicht": "Guaranteed core evidence (Duc 28.10.2026): a mandatory story moment hands it over (What: Rosi's "
               "whiteboard day 4, Why: Megan's folder day 5) - only if that point isn't proven yet",
}
SYSTEMQUELLEN = ["pms", "plotter", "drucker", "buero_pc", "maschinenbuch", "holm_logbuch", "heckverteiler",
                 "servicegeraet_alt", "wettbuch", "kamera", "bordhandbuch", "lm3", "unit01_zaehler",
                 "reservierungsbuch", "aushang", "telefon", "herstellerunterlagen", "eden_hq", "notizbuch",
                 "dokumentenmappe"]
PMS_VERSATZ_MIN = 14
AUSFALL_FENSTER = ("T2 06:00", "T2 06:50")      # alle Faelle: Ausfall in diesem Fenster (gleiche Oberflaeche)
GLIEDER = {  # sichtbare Fragen im Codex - in allen Faellen gleich, damit die Oberflaeche nichts verraet
    "handlung": "What happened to the system during the night?",
    "person": "Who triggered it - and did this person know what they were doing?",
    "folge": "Did exactly that cause the failure?",
}

# ------------------------------------------------------------------ Zeit
_ZEIT = re.compile(r"^T(-?\d+) (\d\d):(\d\d)$")


def minuten(t):
    m = _ZEIT.match(t)
    if not m:
        raise ValueError("Zeitformat 'T<tag> HH:MM' erwartet: %r" % t)
    return int(m.group(1)) * 1440 + int(m.group(2)) * 60 + int(m.group(3))


def zeit(mn):
    tag, rest = divmod(mn, 1440)
    return "T%d %02d:%02d" % (tag, rest // 60, rest % 60)


def pms(t):
    """Schiffszeit -> Anzeige der Energiesteuerung (geht 14 min nach)."""
    return zeit(minuten(t) - PMS_VERSATZ_MIN)


def uhr(t):
    return t.split(" ")[1]


# ------------------------------------------------------------------ Bausteine
def W(art, text, ort=None, person=None, tage=(2, 7), bed=None, kosten=None, intim=False, braucht=None,
      auffaellig=True, phasen=None, g=None, setzt=None):
    """Ein Weg, auf dem Duc einen Fakt erfahren kann. text = Optionstext fuer Duc (spoilerfrei formulieren).
    g = Gruppe: Wege derselben Gruppe sind EINE Handlung bzw. EINE Quelle (Pruefung "faellt eine Quelle weg")."""
    w = {"art": art, "text": text, "tage": list(tage), "gruppe": g or "%s:%s" % (art, person or ort or "-")}
    if ort:
        w["ort"] = ort
    if person:
        w["person"] = person
    if bed:
        w["bedingung"] = bed
    if kosten:
        w["kosten"] = kosten
    if intim:
        w["intim"] = True
    if braucht:
        w["braucht"] = list(braucht)
    if not auffaellig:
        w["auffaellig"] = False     # die Verantwortliche bekommt es nicht mit (keine Angst-Stufe)
    if phasen:
        w["phasen"] = phasen
    if setzt:
        w["setzt"] = setzt          # Flag, das die Engine beim Gehen dieses Weges setzt (Gegenhandlungs-Ausloeser)
    return w


def F(fid, art, inhalt, zeit_, quelle, zuv, wissende=(), codex=None, wahr=True, wege=(), uebermittlung=(),
      person=None, ort=None, notiz=None, pms_zeit=False, widerlegt=None):
    """Ein Fakt. zeit_ = Schiffszeit des Geschehens. pms_zeit=True: Codex zeigt die PMS-Uhr (14 min nach).
    wahr=False (Luege/irrefuehrendes Papier) braucht widerlegt = Fakten, die es widerlegen."""
    f = {"id": fid, "art": art, "inhalt": inhalt, "zeit": zeit_, "quelle": quelle, "zuverlaessigkeit": zuv,
         "wahr": wahr, "wissende": list(wissende), "codex": codex or inhalt, "wege": [dict(w) for w in wege]}
    if widerlegt:
        f["widerlegt_durch"] = list(widerlegt)
    if pms_zeit:
        f["zeit_pms"] = pms(zeit_)
    if uebermittlung:
        f["uebermittlung"] = list(uebermittlung)
    if person:
        f["person"] = person
    if ort:
        f["ort"] = ort
    if notiz:
        f["notiz"] = notiz
    for i, w in enumerate(f["wege"], 1):
        w["id"] = "%s_w%d" % (fid, i)
    return f


def UE(an, zeit_, wie):
    """Uebermittlung: wer erfaehrt den Fakt wann wie (innerer Monolog ist nie Wissen anderer)."""
    return {"an": an, "zeit": zeit_, "wie": wie}


def V(pid, op, n):
    return {"wert": ["vertrauen.%s" % pid, op, n]}


def FLAG(name):
    return {"flag": name}


def ALLE(*b):
    return {"alle": list(b)}


def EINE(*b):
    return {"eine": list(b)}


def NICHT(b):
    return {"nicht": b}


def ZL(zeit_, was, wer=(), sichtbar=()):
    """Zeitleisten-Eintrag (intern). sichtbar = wer es mitbekommt."""
    return {"zeit": zeit_, "zeit_pms": pms(zeit_), "was": was, "wer": list(wer), "sichtbar_fuer": list(sichtbar)}


def WS(wid, tag_ab, aussage, gegen, codex, nachfragen, braucht=()):
    """Widerspruch: "Das passt zeitlich nicht" - markiert niemanden als schuldig.
    nachfragen = Fakt-ID der neuen, ueberpruefbaren Angabe. Sofort beschuldigen = Widerstand."""
    return {"id": wid, "tag_ab": tag_ab, "aussage": aussage, "gegen": list(gegen), "braucht": list(braucht),
            "codex": codex, "nachfragen": nachfragen,
            "beschuldigen": {"folgen": "The person's trust -2; they stay silent for the rest of the day",
                             "markiert_wahrheit": False}}


def GH(gid, tag, phase, ausloeser, was, spur, blockiert=(), umweg=(), sichtbar_ab=None, notiz=None):
    """Gegenhandlung der verantwortlichen Seite. Hoechstens eine pro Tag; jede hinterlaesst eine Spur (Fakt)
    und laesst einen Umweg (Wege-IDs, die keine Gegenhandlung blockiert)."""
    g = {"id": gid, "tag": tag, "phase": phase, "ausloeser": ausloeser, "was": was, "spur": spur,
         "blockiert": list(blockiert), "umweg": list(umweg), "sichtbar_ab": sichtbar_ab or "T%d frühstück" % (tag + 1)}
    if notiz:
        g["notiz"] = notiz
    return g


def TIPP(tid, wer, ab_vertrauen, text, zeigt_auf, ab_tag=1, nach=None):
    """Tratsch: zeigt nur, wo man nachsehen sollte (Weg-ID), ist nie selbst Beweis.
    nach = Gegenhandlung, die vorher passiert sein muss (sonst gibt es nichts zu tratschen)."""
    t = {"id": tid, "wer": wer, "ab_vertrauen": ab_vertrauen, "ab_tag": ab_tag, "text": text, "zeigt_auf": zeigt_auf,
         "zuverlaessigkeit": "geruecht", "beweis": False}
    if nach:
        t["nach"] = nach
    return t
