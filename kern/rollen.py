# -*- coding: utf-8 -*-
"""Rollen und Sonderregeln einzelner Figuren - aus den Moduldaten statt fest im Kern (18.10.2026).

Der Kern kennt keine Figurennamen. Was eine Figur besonders macht, steht im Modul; fehlt es, gibt es die Regel dort
einfach nicht (ein Modul ohne "haendler" hat keinen Draht, keine Hehlerei, keinen Ankauf).

  modul["rollen"] = {
    "haendler": "toto",              # Hehler: Draht (Wert "draht") zaehlt als sein Vertrauen, Preise nach Draht,
                                     #   Ankauf, Sonderangebot; sein Laden hat dieselbe ID wie er
    "dorfohr": "alva",               # erfaehrt alles, was an Land passiert, und plaudert fast immer
    "tratsch": ["alva", "toto"],     # erzaehlen weiter, was sie wissen - auch ueber sich selbst
    "crew": [...],                   # Kern-Crew fuer Gruppenreaktionen (zwei davon in einer Szene = Crew-Szene)
    "nicht_crew": ["toto"],          # zaehlt bei Versprechen an "die Crew" nicht mit
    "nicht_in_crew_szene": [...],    # wird in Ereignis-Szenen "mit der Crew" nicht dazugesetzt
    "freie_zeit_extra": [...],       # Nebenfiguren, die in freien Phasen wie die Frauen angeboten werden
    "isst_mit": ["lola"],            # isst beim Crew-Essen mit, ohne romanzierbar zu sein
    "partner_standard": "chiara",    # Ersatz, wenn ein Ereignis "die Partnerin" will und es keine gibt
    "nur_anruf": {"vogel": "Katrin Vogel"},   # Anrufer ohne Personeneintrag: ID -> Anzeigename
  }
  modul["migration"] = {"ersetzt": {alt: neu}, "umbenannt": [[alt, neu], ...]}   # alte Spielstaende
  modul["ermittlung"] = {"verdacht": [...], "verdacht_ohne_fall": [...], "ersatz": pid, "schwelle": {pid: n}}

  Personen-Felder (modul["personen"][pid]):
    von_bord_ab_tag      ab diesem Tag nicht mehr auf der Buehne
    immer_erreichbar     zaehlt fuer Ereignisse als anwesend (Anruf/Bedingung regelt den Rest)
    keine_nebenfigur     wird in Szenen nicht als Nebenfigur gefuehrt
    romanze_flags        [flag, ...] - erst mit allen Flags romanzierbar, Begehren entsteht dann (romanze_abgleichen)
    vergeben             {"bis_flag": flag, "grund": text} - bis zum Flag keine intimen Gesten/Geschenke, Grenze 3
    technik              Zeit mit ihr bei der Arbeit zaehlt immer als Reparatur
    bestechung           {"ab": Warenwert, "regie": Satz mit %s} - lehnt Wertvolles als Bestechung ab
    geschenk_reaktion    [wert, text] - Regie-Satz zum Geschenk; ohne Vertrauenswert zaehlt "draht"/"ruf"/null
    ruft_nicht_an_wenn   Bedingung (regeln.gilt) - solange sie gilt, kommen keine Handy-Ereignisse von ihr

  Laden-Felder (modul["laeden"][lid]): wechselnd, immer, sonderangebot, essen, zweites_essen_ab, handel_punkte,
    tageslimit {item: schluessel},
    haendler_zeilen, haendler_gefuehl, hintergrund,
    rabatt_ab_vertrauen [stufe, faktor], rabatt_je_stufe [prozent, ab_stufe], aufschlag {item: faktor}
"""

# Wert-Aliase fuer regeln.gilt (das ohne Modul aufgerufen wird): "vertrauen.<haendler>" liest auch den Draht.
# Gesetzt bei jedem Laden des Moduls (eden.modul_laden) - wie szene.CFG ein Spiegel des aktiven Moduls.
ALIAS = {}


def anmelden(modul):
    ALIAS.clear()
    h = rolle(modul, "haendler")
    if h:
        ALIAS["vertrauen." + h] = "draht"


def rolle(modul, name, standard=None):
    return (modul.get("rollen") or {}).get(name, standard)


def liste(modul, name):
    return list(rolle(modul, name) or [])


def ist(modul, name, pid):
    r = rolle(modul, name)
    if pid is None or r is None:
        return False
    return pid == r if isinstance(r, str) else pid in r


def person(modul, pid, feld, standard=None):
    return (modul["personen"].get(pid) or {}).get(feld, standard)


def vergeben(z, modul, pid):
    """Grund (Text), solange die Figur noch vergeben ist - sonst ''."""
    v = person(modul, pid, "vergeben")
    return v["grund"] if v and v["bis_flag"] not in z["flags"] else ""


def romanze_abgleichen(z, modul):
    """Figur mit "romanze_flags" gilt erst als Romanze, wenn alle Flags gesetzt sind, und bekommt dann ihr Begehren (Bibi, Duc 02.11.2026).
    Das Modul ist je Prozess ein Objekt und es laeuft je Prozess ein Spielstand, darum wird es hier gesetzt statt an jeder Lesestelle."""
    for pid, p in modul["personen"].items():
        if p.get("romanze_flags"):
            p["romanzierbar"] = all(f in z.get("flags", []) for f in p["romanze_flags"])
            if p["romanzierbar"]:
                z["werte"].setdefault("begehren." + pid, 1)


def haendler_vertrauen(z, modul, pid, wert):
    """Beim Haendler zaehlt der hoehere von Vertrauen und Draht."""
    return max(wert, z["werte"].get("draht", 0)) if ist(modul, "haendler", pid) else wert


def laden(modul, lid):
    return (modul.get("laeden") or {}).get(lid) or {}
