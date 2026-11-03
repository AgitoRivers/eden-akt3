# -*- coding: utf-8 -*-
"""Hauptstory eden_rise - Rahmen-Fakten, harmlose Privatsachen und die sechs Faelle (17.10.2026).

VERTRAULICH - enthaelt die Aufloesung. Nie Inhalte ausgeben; Pruefung und Bau melden nur Zahlen.
Grundlage: Autoren-Dossier (Kap. 2-4, 7) plus Ducs Entscheidungen vom 17.10. (Party Tag 1, Holm bis Tag-2-Morgen an Bord - 7-Tage-Woche seit 17.10. spaet,
Lola an Bord / Alva an Land, Megan per Telefon + einmal per Hubschrauber, Nebenbogen Lola/Alva).
Schiffszeit ueberall; PMS-Zeiten werden mit pms() berechnet (geht 14 min nach).
"""
from story_basis import (F, W, UE, V, FLAG, ALLE, EINE, NICHT, ZL, WS, GH, TIPP, pms, uhr)

# ------------------------------------------------------------------ Standard-Wege
def STREIFEN():
    return W("sichern", "Secure the event record of the power management system", ort="power_room", tage=(2, 2),
             g="streifen")


def SERVICEKOPIE():
    return W("untersuchen", "Pull a copy of the controller log through the service access", ort="power_room",
             tage=(2, 7), kosten={"phase": 1}, g="servicekopie")


def ROSI_LIEST():
    return W("befragen", "Have Rosi read out the fault messages", person="rosi", ort="power_room", g="befragen:rosi")


def LOGBUCH():
    return W("untersuchen", "Read the bridge logbook", ort="bridge", g="logbuch")


def HOLM():
    return W("befragen", "Ask Holm about the night", person="holm", ort="bridge", tage=(2, 2), phasen=["fruehstueck"], g="holm")


def HOLM_HANDY():
    return W("handy", "Call Holm in hospital", person="holm", tage=(2, 7), g="holm_handy")


def PETRU_UNTERLAGEN(braucht=("r_14",)):
    return W("handy", "Ask Petru for the manufacturer's documents on the module type", person="petru", tage=(3, 7),
             braucht=braucht, g="petru_unterlagen")


def ROSI_TEST(text, tage=(2, 7), braucht=None, bed=None):
    return W("befragen", text, person="rosi", ort="power_room", tage=tage, braucht=braucht, bed=bed,
             kosten={"phase": 1}, g="rosi_test")


def PMS_F(fid, t, text, wissende=(), extra_wege=(), mit_streifen=True):
    """Eintrag im Steuerungsprotokoll: Codex zeigt die PMS-Uhr."""
    wege = ([STREIFEN()] if mit_streifen else []) + [SERVICEKOPIE()] + list(extra_wege)
    return F(fid, "ereignis", text % uhr(pms(t)), t, "pms", "gesichert", wissende=wissende,
             codex="Log " + text % uhr(pms(t)), wege=wege, pms_zeit=True)


def AUSFALL(n, t, zusatz=""):
    return PMS_F("f%d_01" % n, t, "%%s: LM3 failed, propulsion stopped, hotel load in island mode%s" % zusatz,
                 extra_wege=[ROSI_LIEST()])


def LOGBUCH_F(n, t, text, wissende=("holm",)):
    return F("f%d_02" % n, "dokument", text, t, "holm_logbuch", "belastbar", wissende=wissende,
             codex="Logbook (Holm, bridge clock): " + text, wege=[LOGBUCH(), HOLM(), HOLM_HANDY()])


# ================================================================== RAHMEN (in allen Faellen gleich)
RAHMEN = [
    F("r_01", "dokument", "Reiseplan v1 (Holm, T-5): Abfahrt Tag 2 um 07:00, direkt nach Calvi.", "T-5 10:00",
      "buero_pc", "belastbar", wissende=["holm", "duc", "sophia", "chiara"],
      codex="Travel plan v1: departure day 2, 07:00, direct to Calvi",
      wege=[W("untersuchen", "Look through the voyage plans on the office PC", ort="bridge", g="buero_pc"), HOLM()]),
    F("r_02", "dokument", "Voyage plan v2 has applied since Day 1, 15:30: night passage after the party, morning "
                          "stop in Cala d'Orsu (guests' wish: sunrise), submitted through Sophia, approved by Holm.", "T1 15:30", "buero_pc",
      "belastbar", wissende=["duc", "holm", "sophia", "chiara", "rosi", "lea", "toto", "lola", "yasin", "siri"],
      codex="Voyage plan v2: night passage, morning stop at Cala d'Orsu (guests' wish), submitted through Sophia",
      wege=[W("erinnerung", "Duc knows the valid plan", g="start")]),
    F("r_03", "dokument", "Load limit on the stern distribution board: 2 kW maximum, only the onboard charging "
                          "station, no multi-socket adapters. Receipt signed by Yasin.", "T1 11:00", "dokumentenmappe", "belastbar",
      wissende=["holm", "yasin", "rosi"], codex="Load limit on the aft distribution panel 2 kW, no multi-plug adapters - receipt "
      "signed (Yasin)",
      wege=[W("untersuchen", "Look through the bridge folder with the guest documents", ort="bridge", g="brueckenmappe"),
            W("befragen", "Ask Rosi about the power rules for guests", person="rosi", g="befragen:rosi"),
            HOLM()]),
    F("r_04", "ereignis", "Holm hands Lea the route planning for the night passage as an exercise.", "T1 14:00",
      "holm", "belastbar", wissende=["holm", "lea", "duc"], codex="Route planning: Lea (exercise, assigned by Holm)",
      wege=[W("erinnerung", "Duc war dabei", g="start")]),
    F("r_05", "dokument", "Duc zeichnet Leas Routenplan ab.", "T1 17:40", "buero_pc", "belastbar",
      wissende=["duc", "lea", "holm"], codex="Du hast Leas Routenplan um 17:40 abgezeichnet",
      wege=[W("erinnerung", "Deine eigene Unterschrift", g="start")]),
    F("r_06", "dokument", "Group photo in the main salon. Camera time 21:32; the power management display in the "
                          "background shows %s." % uhr(pms("T1 21:32")), "T1 21:32", "kamera", "gesichert",
      wissende=["duc", "chiara", "sophia", "lea", "rosi", "siri", "toto", "yasin", "lola", "holm"],
      codex="Group photo 21:32 (camera time) - power management display in the background",
      wege=[W("handy", "Look at the group photo in the crew chat", g="foto")]),
    F("r_07", "ereignis", "The guest party ends at 00:30; the crew afterparty in the mess and on the aft deck goes "
                          "on until about 03:30, with music from Lola's speaker.", "T2 00:30", "duc", "beobachtet", wissende=["duc", "lola", "toto"],
      wege=[W("erinnerung", "Duc war dabei", g="start")]),
    F("r_08", "aussage", "Holm locks the bridge at 00:45 and lies down.", "T2 00:45", "holm", "aussage",
      wissende=["holm"], codex="Holm: bridge locked at 00:45", wege=[HOLM(), HOLM_HANDY()]),
    F("r_09", "dokument", "Maschinenbuch: \"01:40 Rundgang o. B.\" (Rosi).", "T2 01:40", "maschinenbuch",
      "belastbar", wissende=["rosi"], codex="Maschinenbuch: 01:40 Rundgang ohne Befund (Rosi)",
      wege=[W("untersuchen", "Read the engine log", ort="power_room", g="maschinenbuch"),
            W("befragen", "Ask Rosi about her rounds", person="rosi", g="befragen:rosi")]),
    F("r_10", "ereignis", "Duc can't sleep and sits with Lola in the galley; she is baking for the sunrise "
                          "breakfast. Blackout: first the music stops, then Lola says \"Duc?\", then the alarm.",
      "T2 05:50", "duc", "beobachtet", wissende=["duc", "lola"],
      codex="Galley before sunrise: first the music stops, then your name, then the alarm",
      wege=[W("erinnerung", "Duc war dabei", g="start")]),
    F("r_11", "ereignis", "Holm brings the Eden Rise into the bay of Cala d'Orsu on the bow thruster and Unit-01 and "
                          "drops anchor.", "T2 07:50", "holm", "beobachtet", wissende=["holm", "duc", "toto", "rosi"],
      codex="07:50 at anchor in the bay of Cala d'Orsu", wege=[W("erinnerung", "Duc war dabei", g="start")]),
    F("r_12", "abgeleitet", "The clock of the power management system is 14 minutes slow (ship's time = display + "
                            "14).",
      "T2 08:00", "pms", "gesichert", wissende=["rosi"],
      codex="Clock check: the energy management system runs 14 minutes slow",
      wege=[W("abgleichen", "Match the times: the photo against the display in the background", tage=(2, 7), braucht=["r_06"],
              g="abgleich_foto"),
            W("abgleichen", "Compare the clocks: logbook against the system log", tage=(2, 7),
              braucht=["@ausfall", "@logbuch"], g="abgleich_logbuch"),
            W("untersuchen", "Compare the power management clock with your phone", ort="power_room", tage=(2, 7),
              g="abgleich_direkt")]),
    F("r_13", "dokument", "Ship's manual p. 4-17: fallback profile R2 as a permitted emergency profile after a "
                          "protective abort, activated at the maintenance switch; reset via \"End diagnosis\".", "T-400 12:00",
      "bordhandbuch", "belastbar", wissende=["rosi", "holm", "chiara"],
      codex="Ship's manual 4-17: fallback profile R2 after a protective abort, reset via \"End diagnosis\"",
      wege=[W("untersuchen", "Look it up in the ship's manual", ort="bridge", g="bordhandbuch"),
            W("befragen", "Ask Rosi about the fallback profile", person="rosi", g="befragen:rosi")]),
    F("r_14", "gegenstand", "Typenschild LM3: Leistungsmodul PX-480, Charge 22-B.", "T-400 12:00", "lm3", "gesichert",
      wissende=["rosi"], codex="Type plate on LM3: PX-480, batch 22-B",
      wege=[W("untersuchen", "Look at the rating plate on LM3", ort="power_room", g="typenschild"),
            W("befragen", "Ask Rosi about the failed module", person="rosi", g="befragen:rosi")]),
    F("r_15", "dokument", "Service cards: card 1 Captain (Duc from day 2), card 2 Engineering - hangs on the hook in "
                          "the engine control room, card 3 Yard/Office - drawer in the ship's office.", "T-30 12:00", "dokumentenmappe",
      "belastbar", wissende=["holm", "rosi", "chiara", "duc"],
      codex="Service cards: 1 Captain, 2 Engineering (hook in the control room), 3 Office (drawer)",
      wege=[W("befragen", "Ask Rosi about the service cards", person="rosi", g="befragen:rosi"),
            W("untersuchen", "Check the control room", ort="power_room", g="kontrollraum")]),
    F("r_16", "dokument", "Holm, Duc, Rosi and Chiara (on her big bunch) have keys to the bridge maintenance switch.", "T-30 12:00", "dokumentenmappe", "belastbar", wissende=["holm", "duc", "rosi", "chiara"],
      codex="Maintenance switch keys: Holm, you, Rosi, Chiara",
      wege=[W("erinnerung", "Du hast selbst einen", g="start"), HOLM()]),
    F("r_17", "dokument", "Totò's betting book \"Arrival Calvi\": every bet with time, stake and odds.",
      "T1 12:00", "wettbuch", "belastbar", wissende=["toto"], codex="Totos Wettbuch: Ankunft Calvi",
      wege=[W("befragen", "Get Totò to show you his betting book", person="toto", g="wettbuch")]),
    F("r_18", "nachricht", "Petru writes Lea the Margot search area off the Punta d'Orsu, with coordinates.",
      "T-6 18:00", "telefon", "belastbar", wissende=["lea", "petru"],
      codex="Petru's message to Lea: Margot search area off the Punta d'Orsu (coordinates)",
      wege=[W("befragen", "Ask Petru about Lea", person="petru", ort="petru_workshop", tage=(2, 7), g="petru"),
            W("befragen", "Ask Lea about the fisherman who texts her", person="lea", bed=V("lea", ">=", 2),
              g="befragen:lea")]),
    F("r_19", "beobachtung", "At the party Holm visibly has stomach pain and waves it off (medical, not a clue).",
      "T1 20:00", "duc", "beobachtet", wissende=["duc", "lola", "chiara"],
      wege=[W("erinnerung", "Duc saw it", g="start")]),
]

# ================================================================== HARMLOSE PRIVATSACHEN (nicht_in = Faelle,
# in denen die Person die Verantwortliche ist bzw. der Fakt durch einen Fallfakt ersetzt wird)
def H(fid, person, nicht_in, *a, alibi=False, **k):
    """alibi=True: entlastet die Person zeitlich (Pruefung: jede unschuldige Verdaechtige hat ein Alibi)."""
    f = F(fid, *a, person=person, **k)
    f["nicht_in"] = list(nicht_in)
    if alibi:
        f["alibi_fuer"] = person
    return f


HARMLOS = [
    H("h_01", "chiara", [1], "aussage", "Chiara studied in the mess from 01:30 to 02:45 for her Yachtmaster Offshore "
                                        "exam, which nobody is supposed to know about.", "T2 01:30", "chiara", "aussage", wissende=["chiara"],
      codex="Chiara: studied in the mess until quarter to three",
      alibi=True, wege=[W("befragen", "Ask Chiara about the night", person="chiara")]),
    H("h_02", "chiara", [1], "aussage", "Lola: Chiara sat at the mess table with her binder from half past one to "
                                        "quarter to three.", "T2 01:30", "lola", "aussage", wissende=["lola"],
      codex="Lola: Chiara sat studying at the mess table until quarter to three",
      alibi=True, wege=[W("befragen", "Ask Lola who was in the mess and when", person="lola")]),
    H("h_03", "chiara", [1], "dokument", "Printer in the ship's office: job Day 1, 16:10, \"Collision Regulations ch. "
                                         "3\", user C. Sonnberg.", "T1 16:10", "drucker", "belastbar", wissende=["chiara"],
      codex="Printer memory: 16:10 \"Collision Regulations ch. 3\" (C. Sonnberg)",
      wege=[W("untersuchen", "Look at the printer memory in the ship's office", ort="bridge", g="drucker")]),
    H("h_04", "holm", [1, 3], "aussage", "Holm: at 02:40 the bridge was locked, everything as usual.", "T2 02:40",
      "holm", "aussage", wissende=["holm"], codex="Holm: found the bridge locked at 02:40",
      wege=[HOLM(), HOLM_HANDY()]),
    H("h_05", "lea", [2], "messung", "Chart plotter history: at 01:10 a section off the Punta d'Orsu was opened "
                                     "(Margot area); Holm found it still open at 02:40.", "T2 01:10", "plotter", "gesichert",
      wissende=["lea", "holm"], codex="Plotter history 01:10: chart section off the Punta d'Orsu",
      alibi=True, wege=[W("untersuchen", "Look at the chart plotter history", ort="bridge", g="plotter")]),
    H("h_06", "lea", [], "aussage", "Siri: she and Lea sat on the foredeck from 02:00 to 03:30 watching the sea glow.", "T2 02:00", "siri", "aussage", wissende=["siri", "lea"],
      codex="Siri: with Lea on the foredeck from 02:00 to 03:30",
      alibi=True, wege=[W("befragen", "Ask Siri about the night", person="siri")]),
    H("h_07", "lea", [2], "dokument", "Route plan (Lea): direct line, 34 nm, standard distance off the coast.",
      "T1 16:30", "buero_pc", "belastbar", wissende=["lea", "duc", "holm"],
      codex="Routenplan: direkte Linie, 34 sm",
      wege=[W("untersuchen", "Look at Lea's route plan on the office PC", ort="bridge", g="buero_pc")]),
    H("h_08", "lea", [2], "messung", "The GPS track of the night follows the planned line without deviation.", "T2 06:00",
      "plotter", "gesichert", wissende=["holm"], codex="GPS track: on the planned line, no deviation",
      wege=[W("untersuchen", "Look at the night's track on the plotter", ort="bridge", g="plotter")]),
    H("h_09", "sophia", [3], "aussage", "From 02:30 to 03:10 Sophia was on the phone on the sun deck, in French, "
                                        "with her editor Helene Marchal, about her manuscript. No meeting was "
                                        "planned.", "T2 02:30", "sophia",
      "aussage", wissende=["sophia"], codex="Sophia: on the phone on the sun deck at night (private)",
      alibi=True, wege=[W("befragen", "Ask Sophia about her phone call", person="sophia", bed=V("sophia", ">=", 2))]),
    H("h_10", "sophia", [3], "aussage", "Siri saw Sophia on the phone on the sun deck around quarter to three when "
                                        "she went to fetch a blanket.", "T2 02:45", "siri", "aussage", wissende=["siri"],
      codex="Siri: Sophia on the phone on the sun deck at quarter to three",
      alibi=True, wege=[W("befragen", "Ask Siri who she saw at night", person="siri")]),
    H("h_11", "sophia", [3], "dokument", "Voyage plan v2 in detail: departure 03:00, Unit-01 charging run from 01:00 "
                                         "to 02:50, arrival Cala d'Orsu 07:15, stop until 09:30, 8 kn. File created "
                                         "Day 1, 13:30 after Yasin's request.",
      "T1 13:30", "buero_pc", "belastbar", wissende=["sophia", "holm"],
      codex="Travel plan v2: departure 03:00, charging run 01:00-02:50, arrival 07:15, stop until 09:30 (file T1 13:30)",
      wege=[W("untersuchen", "Look at the plan file on the office PC", ort="bridge", g="buero_pc")]),
    H("h_12", "yasin", [3], "aussage", "Yasin: \"I wanted the sunrise for the drone. I asked Sophia at lunchtime.\"", "T1 12:50", "yasin", "aussage", wissende=["yasin", "sophia"],
      codex="Yasin: Sonnenaufgang war sein Wunsch (mittags bei Sophia angefragt)",
      wege=[W("befragen", "Ask Yasin about the morning stop", person="yasin")]),
    H("h_13", "alva", [3], "aussage", "Alva: \"Sophia? Don't know her. Nobody from your boat booked a table with "
                                      "me.\"",
      "T2 07:30", "alva", "aussage", wissende=["alva"], codex="Alva: no reservation from the yacht",
      wege=[W("befragen", "Ask Alva about the crew", person="alva", ort="alvas_bar", tage=(2, 7))]),
    H("h_14", None, [3], "messung", "Unit-01 hour meter: charging run during the night from 01:00 to 02:50.",
      "T2 01:00", "unit01_zaehler", "gesichert", wissende=["rosi"],
      codex="Unit-01 meter: charging run 01:00-02:50",
      wege=[W("untersuchen", "Read the Unit-01 meter", ort="generator_room", g="unit01_zaehler")]),
    H("h_15", "rosi", [4], "dokument", "Totò's betting book: Rosi, €5 on \"4 to 6 pm\" (Day 1, 23:10); odds "
                                       "unchanged.", "T1 23:10", "wettbuch", "belastbar", wissende=["toto", "rosi"],
      codex="Betting book: Rosi €5 on 4-6 pm, odds unchanged",
      wege=[W("befragen", "Get Totò to show you his betting book", person="toto", g="wettbuch")]),
    H("h_16", "rosi", [], "aussage", "Chiara heard Rosi snoring through the cabin wall at quarter to three.",
      "T2 02:45", "chiara", "aussage", wissende=["chiara"],
      codex="Chiara: Rosi schnarchte um Viertel vor drei in ihrer Kabine",
      alibi=True, wege=[W("befragen", "Ask Chiara about the night in the crew corridor", person="chiara")]),
    H("h_17", "rosi", [4], "dokument", "Rosis Diagnoseprotokoll Tag 2: LM3 ausgefallen, Ursache offen.", "T2 09:30",
      "servicegeraet_alt", "belastbar", wissende=["rosi"], codex="Rosi's log, day 2: LM3 failed, cause unknown",
      wege=[W("untersuchen", "Look at Rosi's log binder in the power room", ort="power_room", g="protokollordner")]),
    H("h_18", "yasin", [5], "messung", "Hotel load list: charging station in the mess 1.8 kW from 05:30 to 06:40 "
                                       "(Yasin's devices); the stern distribution board did not trip.", "T2 05:30", "pms", "gesichert", wissende=["rosi"],
      codex="Hotel load: charging station in the mess 1.8 kW 05:30-06:40, stern board did not trip",
      alibi=True, wege=[SERVICEKOPIE(), W("befragen", "Have Rosi show you the consumption list", person="rosi", g="befragen:rosi")]),
    H("h_19", "yasin", [5], "dokument", "Yasin's clips: dawn from the sun deck from 05:30, without a break.",
      "T2 05:30", "kamera", "belastbar", wissende=["yasin", "siri"],
      codex="Yasin's clips: from 05:30, continuously from the sun deck",
      alibi=True, wege=[W("befragen", "Yasin seine Morgen-Clips zeigen lassen", person="yasin")]),
    H("h_20", "toto", [], "aussage", "Totò: his cousin came alongside the swim platform in a dinghy from 01:50 to "
                                     "02:20 (goods). That's why he was on deck.", "T2 01:50", "toto", "aussage", wissende=["toto"],
      codex="Totò: at the swim platform at night (a visit from his cousin)",
      wege=[W("befragen", "Ask Totò why he was on deck at night", person="toto",
              bed=EINE(V("toto", ">=", 2), FLAG("toto_diskretion")))]),
    H("h_21", "lola", [], "aussage", "Lola: afterparty until half past three, then a smoke at the stern, baking in "
                                     "the galley from quarter to five.", "T2 03:30", "lola", "aussage", wissende=["lola"],
      codex="Lola: afterparty until 03:30, galley from 04:45",
      wege=[W("befragen", "Ask Lola about her night", person="lola")]),
    # Auftakt-Erinnerungen (je Helfer-Wahl; Fall-Erinnerungen ersetzen sie)
    H("h_22", "chiara", [1], "beobachtung", "At the party: Chiara's binder in the pantry, tab \"Collision "
                                            "Regulations\". She snaps it shut quickly.", "T1 19:30", "duc", "beobachtet", wissende=["duc"],
      codex="Memory: Chiara's binder, tab Collision Regulations",
      wege=[W("erinnerung", "You helped Chiara with the service", bed=FLAG("auftakt_hilfe_chiara"),
              g="auftakt")]),
    H("h_23", "rosi", [4, 6], "beobachtung", "At the party, in the control room: all displays green. Rosi proudly "
                                             "shows off Unit-01.", "T1 20:10", "duc", "beobachtet", wissende=["duc"],
      codex="Memory: control room at 20:10, everything green",
      wege=[W("erinnerung", "You helped Rosi with the test", bed=FLAG("auftakt_hilfe_rosi"), g="auftakt")]),
    H("h_24", "siri", [2, 3, 5], "beobachtung", "At the party: Siri takes a breather on the aft deck. Yasin's "
                                                "devices are charging at the charging station in the mess.", "T1 20:40", "duc", "beobachtet", wissende=["duc"],
      codex="Memory: Yasin's devices at the charging station in the mess",
      wege=[W("erinnerung", "You got Siri out of the shoot", bed=FLAG("auftakt_hilfe_siri"), g="auftakt")]),
]

# ================================================================== FAELLE
FAELLE = []


def FALL(nr, verantwortlich, kurz, kern, passage, zeitleiste, fakten, kette, widersprueche, uhr_relevanz,
         gegenhandlungen, gestaendnis, holm_tag1, tipps, auftakt, angst, wiedergutmachung, sonder=None):
    FAELLE.append({"nr": nr, "id": "fall_%d" % nr, "verantwortlich": verantwortlich, "kurz": kurz, "kern": kern,
                   "passage": passage, "zeitleiste": zeitleiste, "fakten": fakten, "kette": kette,
                   "widersprueche": widersprueche, "uhr_relevanz": uhr_relevanz, "gegenhandlungen": gegenhandlungen,
                   "gestaendnis": gestaendnis, "holm_tag1": holm_tag1, "tipps": tipps, "auftakt": auftakt,
                   "angst": angst, "wiedergutmachung": wiedergutmachung, "sonder": sonder or {}})


ANGST_STANDARD = {
    "start": 0,
    "steigt_bei": ["befragt_zur_nacht", "spur_in_gegenwart_gesichert", "geruecht_erreicht_sie",
                   "widerspruch_vorgehalten", "oeffentliche_andeutung"],
    "sinkt_bei": ["privates_gespraech_ohne_vorwurf_ab_vertrauen_3"],
    "regel": "Only rises when the person learns about the investigation. Searching in secret changes nothing.",
}


def KETTE(handlung, person, folge):
    return [{"id": "handlung", "beweis_saetze": handlung},
            {"id": "person", "beweis_saetze": person},
            {"id": "folge", "beweis_saetze": folge}]


def GEST(freiwillig, kernsatz_de, kernsatz_en, moeglich=True, konfrontation_ab=4, extra=None):
    g = {"moeglich": moeglich, "freiwillig": freiwillig,
         "konfrontation": {"ab_tag": konfrontation_ab, "braucht": "alle drei Glieder belegt",
                           "ohne_belege": "denies it; fear +1; Duc may suspect, the game confirms nothing"},
         "ersetzt_glied": "person", "pruefung": ["handlung", "folge"],
         "nie_durch": ["intim", "geschenk", "einzelner_charme_wurf"],
         "kernsatz": {"de": kernsatz_de, "en": kernsatz_en}}
    if extra:
        g.update(extra)
    return g


# ------------------------------------------------------------------ Fall 1
T = "T2 02:24"
FALL(1, "chiara", "Practice on the Bridge",
     "After the party Chiara secretly practises a diagnostic routine for her exam, activates the documented-looking "
     "but unapproved fallback profile R2 after a protective abort, and believes she reset it with \"End diagnosis\". "
     "R2 stays active; the already damaged LM3 fails under the sustained load of the passage.",
     {"abfahrt": "T2 03:00", "holm_bruecke_ab": "T2 02:40", "ladelauf": True, "fahrt_kn": 8.0,
      "ausfall": "T2 06:12", "ankern": "T2 07:50"},
     [ZL("T1 16:10", "Chiara prints exercise 4-17 (diagnosis procedure, protective abort, R2)", ["chiara"]),
      ZL("T1 19:30", "Binder with tab 4-17 in the pantry", ["chiara"], ["duc"]),
      ZL("T2 01:55", "Chiara leaves the afterparty (\"have to study\")", ["chiara"], ["lola"]),
      ZL("T2 02:02", "Bunch of keys with a little bell at the bridge door", ["chiara"], ["toto"]),
      ZL("T2 02:05", "Diagnostic routine started at the maintenance switch", ["chiara"]),
      ZL("T2 02:22", "Protective abort LM3 overtemperature", ["chiara"]),
      ZL(T, "Fallback profile R2 activated", ["chiara"]),
      ZL("T2 02:26", "\"End diagnosis\" - R2 stays active; the exercise sheet is left lying on the console", ["chiara"]),
      ZL("T2 02:30", "Chiara back in the mess, tea, bunk at 02:45", ["chiara"], ["lola"]),
      ZL("T2 02:40", "Holm: door open, display \"PROFILE R2 READY\", sheet into the logbook folder", ["holm"]),
      ZL("T2 03:00", "Departure in profile R2", ["holm"]),
      ZL("T2 06:12", "LM3 fails under sustained load", [], ["duc", "lola", "holm"])],
     [AUSFALL(1, "T2 06:12", " (Profil R2 aktiv)"),
      LOGBUCH_F(1, "T2 06:12", "06:12 Antrieb aus. Anzeige vorher: PROFIL R2 BEREIT (?)"),
      PMS_F("f1_03", "T2 02:05", "%s: diagnostic routine started (bridge maintenance switch)"),
      PMS_F("f1_04", "T2 02:22", "%s: protective abort of diagnostic routine - LM3 overtemperature"),
      PMS_F("f1_05", T, "%s: fallback profile R2 activated (bridge maintenance switch)"),
      F("f1_06", "aussage", "Holm: at 02:40 the bridge door was open although she had locked it at 00:45; the "
                            "display read \"PROFILE R2 READY\". She took it for a yard setting.", "T2 02:40", "holm",
        "aussage", wissende=["holm"], codex="Holm: door open at 02:40, display \"PROFILE R2 READY\"",
        wege=[HOLM(), HOLM_HANDY()]),
      F("f1_07", "gegenstand", "Exercise sheet \"Procedure 4-17\" with pencil notes \"2:05 / 2:22 / 2:24\" in Chiara's "
                               "handwriting. It was lying on the maintenance console; Holm put it in the logbook "
                               "folder.", "T2 02:26", "dokumentenmappe",
        "belastbar", wissende=["holm"], uebermittlung=[UE("lola", "T2 08:30", "Over coffee Holm mentions a note on "
                                                                              "the console")],
        codex="Exercise sheet 4-17 with pencil times 2:05 / 2:22 / 2:24",
        wege=[W("untersuchen", "Go through the logbook folder", ort="bridge", tage=(2, 3), g="logbuchmappe"),
              W("befragen", "Ask Chiara to show you her exam binder", person="chiara", tage=(4, 7),
                bed=V("chiara", ">=", 2), g="pruefungsordner"),
              W("anordnen", "Order the locker opened, as commander", person="chiara", ort="crew_corridor",
                tage=(4, 7), kosten={"vertrauen": ["chiara", -3], "rueckhalt": -1}, g="pruefungsordner_befehl")]),
      F("f1_17", "aussage", "Holm: there was a note on the maintenance console, \"Procedure 4-17\", with pencilled "
                            "times. She put it in the logbook folder.", "T2 02:40", "holm", "aussage", wissende=["holm"],
        uebermittlung=[UE("lola", "T2 08:30", "beim Kaffee")],
        codex="Holm: there was a note \"Procedure 4-17\" on the console – now in the logbook folder",
        wege=[W("befragen", "Ask Holm whether anything was lying on the console that night", person="holm", ort="bridge", tage=(2, 2),
                phasen=["fruehstueck"], g="holm"), HOLM_HANDY()]),
      F("f1_08", "dokument", "Printer memory: job Day 1, 16:10, \"Exercise_4-17.pdf\", 2 pages, user C. Sonnberg. The "
                             "file is still on the office PC.", "T1 16:10", "drucker", "belastbar",
        wissende=["chiara"], codex="Printer memory: 16:10 \"Exercise_4-17\" (C. Sonnberg)",
        wege=[W("untersuchen", "Look at the printer memory in the ship's office", ort="bridge", g="drucker"),
              W("untersuchen", "Look at the last printed files on the office PC", ort="bridge", g="buero_pc")]),
      F("f1_09", "aussage", "Totò: after the party ended, around two, he heard Chiara's bunch of keys with the "
                            "little bell at the bridge door.", "T2 02:02", "toto", "aussage", wissende=["toto"],
        codex="Totò: heard Chiara's keys at the bridge door around two",
        wege=[W("befragen", "Ask Totò what he heard at night", person="toto",
                bed=EINE(V("toto", ">=", 2), FLAG("toto_diskretion")))]),
      F("f1_10", "aussage", "Lola: Chiara left shortly before two (\"have to study\") and came back at half past two, "
                            "made tea and went to bed.", "T2 01:55", "lola", "aussage", wissende=["lola"],
        codex="Lola: Chiara left shortly before two, back at half past two",
        wege=[W("befragen", "Ask Lola who was in the mess and when", person="lola")]),
      F("f1_11", "aussage", "Chiara: \"I studied in the mess until half past two, then I went to bed.\"",
        "T2 01:30", "chiara", "aussage", wahr=False, wissende=["chiara"],
        codex="Chiara: studied in the mess until half past two",
        widerlegt=['f1_10', 'f1_09', 'f1_07', 'f1_08'], wege=[W("befragen", "Ask Chiara about the night", person="chiara")]),
      F("f1_12", "aussage", "Chiara (when pressed): \"I was outside for a moment. Fresh air.\"", "T2 02:00", "chiara",
        "aussage", wahr=False, wissende=["chiara"], codex="Chiara: was outside for a moment, fresh air",
        widerlegt=['f1_09', 'f1_07', 'f1_05'], wege=[W("befragen", "Nachfragen", person="chiara", tage=(2, 7), braucht=["f1_11", "f1_10"])]),
      F("f1_13", "messung", "\"End diagnosis\" does not reset R2. Under sustained load in R2 a PX-480 overheats - "
                            "exactly what the curve shows up to the failure.", "T2 06:12", "herstellerunterlagen", "gesichert",
        wissende=[], codex="Engineering: \"End diagnosis\" does not reset R2; R2 overloads LM3",
        wege=[ROSI_TEST("Have Rosi re-enact the procedure at the maintenance console", braucht=["r_13"]),
              PETRU_UNTERLAGEN()]),
      F("f1_14", "beobachtung", "At the party: Chiara's binder in the pantry, tab \"4-17 Fallback profile\".",
        "T1 19:30", "duc", "beobachtet", wissende=["duc"],
        codex="Memory: Chiara's binder, tab 4-17 Fallback profile",
        wege=[W("erinnerung", "You helped Chiara with the service", bed=FLAG("auftakt_hilfe_chiara"),
                g="auftakt")]),
      F("f1_15", "dokument", "Notice on the bridge door: \"Access for command and engineering only - safety after the "
                             "incident. C. Sonnberg\"", "T2 23:00", "aushang", "belastbar", wissende=["chiara"],
        codex="Notice on the bridge door: access for command/engineering only (signed C. Sonnberg)",
        wege=[W("untersuchen", "The bridge door", ort="bridge", tage=(3, 7), auffaellig=False, g="aushang")]),
      F("f1_16", "gegenstand", "In the logbook folder, the sleeve with the exercise sheet is empty.", "T3 23:30",
        "dokumentenmappe", "gesichert", wissende=["chiara"], codex="Logbook folder: one sleeve is empty",
        wege=[W("untersuchen", "Go through the logbook folder", ort="bridge", tage=(4, 7), auffaellig=False,
                g="logbuchmappe"),
              W("handy", "Ask Holm about the note from the console", person="holm", tage=(4, 7), g="holm_handy")])],
     KETTE(handlung=[["f1_05"], ["f1_06", "f1_02"]],
           person=[["f1_07", "f1_05", "r_12"], ["f1_08", "f1_09", "f1_10", "f1_05", "r_12"],
                   ["f1_14", "f1_09", "f1_10", "f1_05", "r_12"]],
           folge=[["f1_01", "f1_05", "f1_13"], ["f1_02", "f1_06", "f1_13"]]),
     [WS("f1_ws1", 2, "f1_11", ["f1_10"], "Statement: studied in the mess until half past two - Lola: left shortly "
                                          "before two, came back at half past two", "f1_12")],
     "Without matching the clocks, the start of the diagnosis (display %s) comes before Chiara left at 01:55 - with "
     "the clocks matched (02:05) it falls right in her absence. The pencil times on the sheet only fit once the "
     "clocks are matched."
     % uhr(pms("T2 02:05")),
     [GH("f1_gh1", 2, "nacht", {"angst": [">=", 1]}, "Restricts access to the bridge with a matter-of-fact safety "
                                                     "reason.", "f1_15",
         notiz="No evidence is lost; counter: Duc lifts the notice as commander."),
      GH("f1_gh2", 3, "nacht", {"angst": [">=", 2]}, "Takes her exercise sheet out of the logbook folder, not the "
                                                     "log - the sleeve stays empty, the sheet ends up in her exam "
                                                     "binder.", "f1_16",
         blockiert=["f1_07_w1"], umweg=["f1_07_w2", "f1_07_w3", "f1_08_w1", "f1_08_w2"])],
     GEST([{"ab_tag": 3, "bedingung": ALLE(V("chiara", ">=", 3), {"kette_bekannt": [">=", 1]}),
            "form": "She asks for a private talk herself."}],
          "For once I didn't want to be the one bringing the coffee while other people decide.",
          "Just once I didn't want to be the one bringing the coffee while everyone else decides."),
     {"weiss": ["f1_06", "f1_02", "f1_17", "r_08"],
      "sagt_von_sich": "The door was open. I'd locked it at quarter to one.",
      "auf_nachfrage": {"anzeige": "f1_06", "lag_da_was": "f1_17"},
      "vermutung": "The yard changed something at the last service.",
      "haltung": "kurz angebunden; antwortet genau, wenn Duc genau fragt"},
     [TIPP("f1_t1", "lola", 2, "Chiara's been carrying her fat binder everywhere since yesterday. Normally it lives "
                               "in her locker.",
           "f1_07_w2", ab_tag=4, nach="f1_gh2"),
      TIPP("f1_t2", "lola", 2, "Over coffee Holm said she put a note in the logbook folder that night.", "f1_07_w1")],
     {"chiara": "f1_14", "rosi": "h_23", "siri": "h_24"},
     ANGST_STANDARD,
     "She enters the incident in the report herself and works on under verifiable responsibilities. No command "
     "handed to her, no qualification handed to her.")

# ------------------------------------------------------------------ Fall 2
FALL(2, "lea", "The Leg That Wasn't in the Plan",
     "During her route exercise Lea puts WP4 on the Margot search area and makes the extra distance look small by "
     "measuring it against last year's longer route (+1.8 instead of +11.2 nm). Duc signs it off. The autopilot "
     "holds the arrival time and runs at 10.6 instead of 8 kn; under the sustained load the already damaged LM3 "
     "fails.",
     {"abfahrt": "T2 03:00", "holm_bruecke_ab": "T2 02:40", "ladelauf": True, "fahrt_kn": 10.6,
      "ausfall": "T2 06:35", "ankern": "T2 07:50"},
     [ZL("T-6 18:00", "Petru writes Lea the Margot search area", ["petru", "lea"]),
      ZL("T1 16:30", "Lea sets WP4 on the Margot coordinates, extra distance \"+1.8 nm\"", ["lea"]),
      ZL("T1 17:40", "Duc zeichnet ab", ["duc"]),
      ZL("T1 20:40", "Lea to Siri: \"Tomorrow morning we'll go right over it.\"", ["lea"], ["siri", "duc"]),
      ZL("T2 03:00", "Departure; arrival time 07:15 -> autopilot runs at 10.6 kn", ["holm"]),
      ZL("T2 06:15", "Lea on the bridge, asks about WP4", ["lea"], ["holm"]),
      ZL("T2 06:35", "LM3-Ausfall 0,6 sm vor WP4", [], ["duc", "lola", "holm"])],
     [AUSFALL(2, "T2 06:35", " (Sollfahrt 10,6 kn)"),
      LOGBUCH_F(2, "T2 06:35", "06:15 Lea on the bridge (asks about WP4). 06:35 propulsion off."),
      F("f2_03", "messung", "GPS track: course via WP4 in the Margot area, up to 9.4 nm seaward of the direct line; "
                            "speed 10.6 kn; failure 0.6 nm before WP4.", "T2 06:35", "plotter", "gesichert", wissende=["holm"],
        codex="GPS track: via WP4, 9.4 nm seaward of the direct line, 10.6 kn",
        wege=[W("untersuchen", "Look at the night's track on the plotter", ort="bridge", g="plotter"),
              W("befragen", "Have Rosi pull the plotter backup", person="rosi", tage=(2, 7), g="plotter_backup")]),
      F("f2_04", "dokument", "Route plan (Lea, Day 1, 16:30): WP4 \"distance off the coast\", extra distance \"+1.8 "
                             "nm\", signed off by Duc at 17:40.", "T1 16:30", "buero_pc", "belastbar", wissende=["lea", "duc", "holm"],
        codex="Lea's route plan: WP4 \"distance off the coast\", extra distance +1.8 nm (signed off by you)",
        wege=[W("untersuchen", "Look at Lea's route plan on the office PC", ort="bridge", g="buero_pc"),
              W("untersuchen", "The signed paper copy in the bridge folder", ort="bridge",
                g="brueckenmappe"),
              W("befragen", "Have Lea explain the plan", person="lea")]),
      F("f2_05", "abgeleitet", "The extra distance in the plan is measured against last year's route; against the "
                               "direct line it's +11.2 nm.", "T1 16:30", "buero_pc", "gesichert", wissende=["lea"],
        codex="Recalculated: against the direct line +11.2 nm (the plan measures against last year's route)",
        wege=[W("abgleichen", "Recalculate plan and track", tage=(2, 7), braucht=["f2_04", "f2_03"],
                g="abgleich_strecke"),
              W("handy", "Have Holm recalculate it over the phone", person="holm", tage=(2, 7), braucht=["f2_04"],
                g="holm_handy"),
              W("befragen", "Have Rosi recalculate the distance", person="rosi", tage=(2, 7), braucht=["f2_04"],
                g="befragen:rosi")]),
      F("f2_06", "aussage", "Petru: WP4 lies exactly in the search area he sent Lea.", "T-6 18:00",
        "petru", "aussage", wissende=["petru"], codex="Petru: WP4 lies in the search area he sent Lea",
        wege=[W("befragen", "Show Petru the coordinates", person="petru", ort="petru_workshop", tage=(2, 7),
                braucht=["f2_04"], g="petru"),
              W("handy", "Send Petru the coordinates", person="petru", tage=(3, 7), braucht=["f2_04"],
                g="petru_handy")]),
      F("f2_07", "aussage", "Holm: Lea came onto the bridge at quarter past six and wanted to know how far it still "
                            "was to WP4. WP4 lay further out than Holm would have planned it - but Duc had signed it "
                            "off.",
        "T2 06:15", "holm", "aussage", wissende=["holm"], codex="Holm: Lea on the bridge at 06:15, asked about WP4",
        wege=[HOLM(), HOLM_HANDY()]),
      F("f2_08", "aussage", "Lea: \"WP4 was just distance off the coast. It wasn't even two miles extra.\"", "T1 16:30",
        "lea", "aussage", wahr=False, wissende=["lea"], codex="Lea: WP4 only distance off the coast, not even two "
                                                              "miles",
        widerlegt=['f2_05', 'f2_03'], wege=[W("befragen", "Ask Lea about WP4", person="lea", setzt="duc_fragt_strecke")]),
      F("f2_09", "aussage", "Lea: \"I only came onto the bridge after the alarm.\"", "T2 06:35", "lea", "aussage",
        wahr=False, wissende=["lea"], codex="Lea: only on the bridge after the alarm",
        widerlegt=['f2_02', 'f2_07'], wege=[W("befragen", "Ask Lea about the night", person="lea")]),
      F("f2_10", "aussage", "Lea (when pressed): \"I only wanted to see if we were on time.\"", "T2 06:15", "lea",
        "aussage", wahr=False, wissende=["lea"], codex="Lea: only wanted to see if we were on time",
        widerlegt=['f2_02', 'f2_07'], wege=[W("befragen", "Nachfragen", person="lea", tage=(2, 7), braucht=["f2_09", "f2_02"])]),
      F("f2_11", "messung", "At a sustained 10.6 kn LM3 is well above its rated load; at 8 kn it would have stayed "
                            "in the normal range.", "T2 06:35", "herstellerunterlagen", "gesichert", wissende=[],
        codex="Engineering: at 10.6 kn LM3 over rated load, at 8 kn in the normal range",
        wege=[ROSI_TEST("Have Rosi analyse the night's load curve", braucht=["f2_01"]), PETRU_UNTERLAGEN()]),
      F("f2_12", "aussage", "Lea: her grandfather searched for the Margot all his life; she wanted to see the spot "
                            "herself once.", "T-6 18:00", "lea", "aussage", wissende=["lea", "siri"],
        codex="Lea: her grandfather searched for the Margot",
        wege=[W("befragen", "Ask Lea about her grandfather", person="lea", bed=V("lea", ">=", 2))]),
      F("f2_13", "beobachtung", "At the party: Lea says to Siri, \"Tomorrow morning we'll go right over it.\" Yasin's "
                                "devices are charging at the charging station in the mess.", "T1 20:40", "duc", "beobachtet", wissende=["duc"],
        codex="Memory: Lea to Siri - \"Tomorrow morning we'll go right over it\"",
        wege=[W("erinnerung", "You got Siri out of the shoot", bed=FLAG("auftakt_hilfe_siri"),
                g="auftakt")]),
      F("f2_14", "dokument", "Navigation corner: three notes with distance calculations by Lea from the night before "
                             "day 3, all measured against last year's route.", "T3 02:00", "notizbuch", "belastbar", wissende=["lea"],
        codex="Navigation corner: Lea's night-time distance calculations (reference: last year's route)",
        wege=[W("untersuchen", "Look at the nav corner", ort="bridge", tage=(3, 7), auffaellig=False,
                g="navi_ecke")]),
      F("f2_15", "dokument", "Lea's new distance sheet: \"+1.9 nm\" - in small print at the top, the reference \"last "
                             "year's route\".",
        "T3 12:00", "notizbuch", "belastbar", wahr=False, wissende=["lea"], codex="Lea's distance sheet: +1.9 nm "
                                                                                  "(reference in small print: last "
                                                                                  "year's route)",
        widerlegt=['f2_05', 'f2_03'], wege=[W("freiwillig", "Lea brings you a new calculation", person="lea", tage=(3, 7), auffaellig=False,
                g="befragen:lea")])],
     KETTE(handlung=[["f2_03"], ["f2_04", "f2_05"]],
           person=[["f2_04", "f2_05", "r_18"], ["f2_04", "f2_05", "f2_06"], ["f2_04", "f2_05", "f2_07", "f2_02"],
                   ["f2_04", "f2_05", "f2_13"]],
           folge=[["f2_01", "f2_11"], ["f2_02", "f2_03", "f2_11"]]),
     [WS("f2_ws1", 2, "f2_09", ["f2_02", "f2_07"], "Statement: only on the bridge after the alarm - logbook: 06:15, "
                                                   "twenty minutes before the failure", "f2_10")],
     "The display reports the failure at %s - that looks like \"right after Lea's visit\". With the clocks matched "
     "(06:35) there are twenty minutes in between: the visit wasn't an intervention; the question about WP4 is the "
     "lead."
     % uhr(pms("T2 06:35")),
     [GH("f2_gh1", 2, "nacht", {"angst": [">=", 1]}, "Volunteers for anchor watch and repair dives, secretly "
                                                     "recalculates at night and hides how exhausted she is.", "f2_14",
         notiz="No evidence is lost. Counter: Duc raises her exhaustion (flag lea_erschöpfung_angesprochen); "
               "otherwise she makes a mistake during the storm preparation."),
      GH("f2_gh2", 3, "tag", ALLE({"angst": [">=", 2]}, FLAG("duc_fragt_strecke")), "When asked about the distance she "
                                                                                    "goes along with a second untruth: a "
                                                                                    "new distance sheet, again measured "
                                                                                    "against last year's route.",
         "f2_15", notiz="Counter: GPS track and recalculation (f2_05).")],
     GEST([{"ab_tag": 3, "bedingung": ALLE(V("lea", ">=", 3), EINE(FLAG("lea_erschoepfung_angesprochen"),
                                                                    {"kette_bekannt": [">=", 1]})),
            "form": "She comes to the navigation corner at night while Duc is there and tells him about the Margot."}],
          "I thought if I really found it, it wouldn't just be his story any more.",
          "I thought if I actually found it, it wouldn't just be his story anymore.",
          extra={"duc_eigene_rolle": "Duc's sign-off at 17:40 belongs in the complete report."}),
     {"weiss": ["f2_07", "f2_02", "r_08"],
      "sagt_von_sich": "Wir sind schneller gefahren, als mir lieb war. Der Plan wollte um Viertel nach sieben da sein.",
      "auf_nachfrage": {"wp4": "f2_07", "logbuch": "f2_02"},
      "vermutung": "The boat wasn't up to the passage. The yard.",
      "haltung": "curt; reminds Duc that he signed it off"},
     [TIPP("f2_t1", "lola", 2, "Lea sat in the navigation corner half the night. Calculator, three notes.",
           "f2_14_w1", ab_tag=3, nach="f2_gh1"),
      TIPP("f2_t2", "lola", 2, "Lea's been talking about her grandad and a ship for days. Ask the fisherman who "
                               "keeps texting her.", "f2_06_w1", ab_tag=2)],
     {"chiara": "h_22", "rosi": "h_23", "siri": "f2_13"},
     ANGST_STANDARD,
     "She hands over the coordinates and accepts that a later search will be prepared and accompanied. Her "
     "grandfather stays a connection, not an informant.")

# ------------------------------------------------------------------ Fall 3
FALL(3, "sophia", "Der Gefallen",
     "Sophia has arranged a meeting with her editor at Alva's bar at 07:30 on day 2 (a chance at a contract for her "
     "book, which nobody knows about). She invents the guests' wish for a sunrise, pushes through a 01:30 departure "
     "without a charging run of Unit-01 (\"guests don't want to hear diesel at night\") and overrules Holm's doubts "
     "with Megan's name. The night passage drains bank A; in reserve mode the controller switches to profile R2; LM3 "
     "fails.",
     {"abfahrt": "T2 01:30", "holm_bruecke_ab": "T2 01:15", "ladelauf": False, "fahrt_kn": 6.8,
      "ausfall": "T2 06:20", "ankern": "T2 07:50"},
     [ZL("T-4 22:10", "Sophia drafts the plan (night departure, stop 06:30-12:00)", ["sophia"]),
      ZL("T-4 21:00", "Sophia reserviert bei Alva: Tag 2, 07:30, zwei Personen", ["sophia"], ["alva"]),
      ZL("T-3 10:00", "Message from the editor: Tuesday 7:30, Bar Santoni, draft contract", ["sophia"]),
      ZL("T1 13:10", "Sophia suggests the sunrise to Yasin", ["sophia", "yasin"]),
      ZL("T1 13:20", "Yasin to Siri: \"Sophia says sunrise in Cala d'Orsu would be gold\"", ["yasin"], ["siri"]),
      ZL("T1 15:30", "Plan v2 active: departure 01:30, without a charging run; Holm has doubts, approves", ["sophia", "holm"]),
      ZL("T2 01:30", "Abfahrt, Bank A 58 Prozent, 6,8 kn", ["holm"]),
      ZL("T2 02:50", "Sophia to the editor: \"We're arriving early, 7:30 works.\"", ["sophia"]),
      ZL("T2 06:05", "Bank A reserve threshold, reserve mode in profile R2", ["holm"]),
      ZL("T2 06:20", "LM3 failure 1.1 nm before the bay", [], ["duc", "lola", "holm"]),
      ZL("T2 08:15", "The editor leaves; a note for Sophia at Alva's", ["alva"])],
     [AUSFALL(3, "T2 06:20", " (Reservebetrieb, Profil R2)"),
      LOGBUCH_F(3, "T2 06:20", "06:05 Reserve Bank A, Reservebetrieb. 06:20 Antrieb aus."),
      PMS_F("f3_03", "T2 06:05", "%s: bank A reserve threshold - reserve mode, profile R2 (departure at 58 percent)"),
      F("f3_04", "messung", "Unit-01 hour meter: no run during the night; last run Day 1, 11:00.",
        "T1 11:00", "unit01_zaehler", "gesichert", wissende=["rosi"], codex="Unit-01 meter: no run during the night",
        wege=[W("untersuchen", "Read the Unit-01 meter", ort="generator_room", g="unit01_zaehler"),
              W("befragen", "Ask Rosi about Unit-01 during the night", person="rosi", g="befragen:rosi")]),
      F("f3_05", "dokument", "Voyage plan v2 in detail: departure 01:30, arrival Cala d'Orsu 06:30, stop until "
                             "12:00, charging run removed (\"guests want a quiet night\"), submitted by Sophia.", "T1 15:30", "buero_pc",
        "belastbar", wissende=["sophia", "holm"],
        codex="Travel plan v2: departure 01:30, no charging run, stop 06:30-12:00 (filed by Sophia)",
        wege=[W("untersuchen", "Look at the plan file on the office PC", ort="bridge", tage=(2, 3), g="buero_pc"),
              W("untersuchen", "Holm's printed plan in the bridge folder", ort="bridge", g="brueckenmappe"),
              W("handy", "Ask Megan for the plan as it reached Eden", person="megan", tage=(2, 7),
                g="megan_handy")]),
      F("f3_06", "messung", "File version on the office PC: draft plan v2 created four days before the party at "
                            "22:10 (user S.), changed Day 1, 15:30.", "T-4 22:10", "buero_pc", "gesichert", wissende=["sophia"],
        codex="File version: draft plan v2 created four days before departure",
        wege=[W("untersuchen", "Look at the file versions on the office PC", ort="bridge", tage=(2, 3), g="buero_pc"),
              W("handy", "Have Megan pull the file history from the company server", person="megan", tage=(2, 7),
                g="megan_server")]),
      F("f3_07", "dokument", "Alvas Reservierungsbuch: \"Tag 2, 07:30, 2 Pers., Sophia - tel. T-4\".", "T-4 21:00",
        "reservierungsbuch", "belastbar", wissende=["alva", "sophia"],
        codex="Alva's reservation book: Day 2, 07:30, two people, Sophia (booked four days earlier)",
        wege=[W("befragen", "Ask Alva about the crew", person="alva", ort="alvas_bar", tage=(2, 7), g="alva"),
              W("handy", "Alva anrufen", person="alva", tage=(3, 7), bed=FLAG("alva_kennengelernt"),
                g="alva_handy")]),
      F("f3_08", "gegenstand", "Note at Alva's for Sophia (Day 2, 08:15): \"Had to leave. Write to me. H. M.\" - Alva: "
                               "a Frenchwoman, Madame Marchal, waited an hour.", "T2 08:15", "reservierungsbuch",
        "belastbar", wissende=["alva"], codex="Notiz bei Alva: \"Musste los. Schreiben Sie mir. H. M.\"",
        wege=[W("befragen", "Ask Alva about the crew", person="alva", ort="alvas_bar", tage=(2, 7),
                braucht=["f3_07"], g="alva"),
              W("handy", "Alva anrufen", person="alva", tage=(3, 7), bed=FLAG("alva_kennengelernt"),
                g="alva_handy")]),
      F("f3_09", "nachricht", "Messages on Sophia's phone: editor (three days before the party) \"Tuesday 7:30, Bar "
                              "Santoni, I'll bring the draft contract\"; Sophia (Day 2, 02:50) \"We're arriving early, "
                              "7:30 works.\"", "T-3 10:00",
        "telefon", "belastbar", wissende=["sophia"], codex="Sophias Nachrichten: Termin 7:30 Bar Santoni, "
        "Vertragsentwurf",
        wege=[W("freiwillig", "Sophia shows you the messages", person="sophia", tage=(3, 7),
                bed=EINE(V("sophia", ">=", 4), FLAG("sophia_gestanden")), g="sophia_handy")]),
      F("f3_10", "aussage", "Yasin: \"Der Sonnenaufgang war Sophias Idee. Ich fand's gut.\"", "T1 13:10", "yasin",
        "aussage", wissende=["yasin"], codex="Yasin: the sunrise was Sophia's idea",
        wege=[W("befragen", "Ask Yasin about the morning stop", person="yasin")]),
      F("f3_11", "nachricht", "Chat Yasin to Siri (Day 1, 13:20): \"Sophia says sunrise in Cala d'Orsu would be "
                              "gold.\"", "T1 13:20", "telefon", "belastbar", wissende=["yasin", "siri"],
        codex="Chat Yasin to Siri 13:20: \"Sophia says sunrise ... would be gold\"",
        wege=[W("freiwillig", "Siri shows you the chat", person="siri", bed=V("siri", ">=", 2), g="siri"),
              W("befragen", "Have Yasin show you the chat", person="yasin", bed=V("yasin", ">=", 2), g="yasin")]),
      F("f3_12", "aussage", "Holm: she didn't want to leave at night without a charging run. Sophia said the guests "
                            "didn't want to hear diesel and that Megan wanted happy guests. Holm let herself be "
                            "talked into it.", "T1 15:00", "holm",
        "aussage", wissende=["holm", "sophia"], codex="Holm: wanted the charging run; Sophia pushed through the 01:30",
        wege=[HOLM(), HOLM_HANDY()]),
      F("f3_13", "aussage", "Sophia: \"Yasin absolutely wanted the sunrise. I changed the plan on Sunday at lunchtime "
                            "when he asked.\"", "T1 13:00", "sophia", "aussage", wahr=False, wissende=["sophia"],
        codex="Sophia: Yasin's wish, plan changed on Sunday at lunchtime",
        widerlegt=['f3_06', 'f3_07', 'f3_10', 'f3_11'], wege=[W("befragen", "Ask Sophia about the morning stop", person="sophia")]),
      F("f3_14", "aussage", "Sophia (when pressed): \"I'd prepared the stop in case guests asked. That's my job.\"", "T-4 22:10", "sophia", "aussage", wahr=False, wissende=["sophia"],
        codex="Sophia: stop prepared in case guests asked",
        widerlegt=['f3_07', 'f3_08', 'f3_09'], wege=[W("befragen", "Nachfragen", person="sophia", tage=(2, 7), braucht=["f3_13"])]),
      F("f3_15", "abgeleitet", "With a charging run (bank A ~90 percent) and departure at 03:00, the reserve would "
                               "have lasted until after 08:00; R2 would never have become active.", "T2 06:05", "pms", "gesichert", wissende=[],
        codex="Recalculated: with a charging run the reserve would have lasted until after 08:00",
        wege=[ROSI_TEST("Have Rosi work out the night's energy balance", braucht=["f3_03"]),
              W("handy", "Have Holm recalculate it over the phone", person="holm", tage=(2, 7), braucht=["f3_03", "f3_04"],
                g="holm_handy")]),
      F("f3_16", "aussage", "Sophia: \"I saw Rosi in the engine corridor at night, just before everything went off.\" "
                            "(She did see her - but at 01:40, not before the failure.)", "T2 01:40", "sophia", "aussage", wahr=False,
        wissende=["sophia"], codex="Sophia: saw Rosi in the engine corridor at night",
        widerlegt=['r_09', 'f3_17'], wege=[W("freiwillig", "Sophia tells you something", person="sophia", tage=(3, 7), auffaellig=False,
                g="befragen:sophia")]),
      F("f3_17", "aussage", "Lola: Sophia came into the mess from the crew corridor at quarter to two.", "T2 01:45", "lola",
        "aussage", wissende=["lola"], codex="Lola: Sophia came out of the crew corridor at 01:45",
        wege=[W("befragen", "Ask Lola when Sophia was in the mess", person="lola", tage=(3, 7))]),
      F("f3_18", "messung", "Office PC: plan file v2 overwritten on Day 3 at 23:40 (stop now 07:45-09:30, charging "
                            "run back in); the old creation date is gone.", "T3 23:40", "buero_pc", "gesichert", wissende=["sophia"],
        codex="Office PC: plan file overwritten after the incident (Day 3, 23:40)",
        wege=[W("untersuchen", "Look at the plan file on the office PC", ort="bridge", tage=(4, 7), auffaellig=False,
                g="buero_pc")]),
      F("f3_19", "beobachtung", "At the party Siri says Yasin has been raving about the sunrise since lunchtime - "
                                "ever since he was with Sophia. Yasin's devices are charging at the charging station "
                                "in the mess.", "T1 20:40", "duc", "beobachtet",
        wissende=["duc"], codex="Memory: Siri - Yasin's sunrise idea came after a talk with Sophia",
        wege=[W("erinnerung", "You got Siri out of the shoot", bed=FLAG("auftakt_hilfe_siri"),
                g="auftakt")]),
      F("f3_20", "aussage", "Holm: when she came onto the bridge for departure at 01:15, it was locked, everything "
                            "as usual.", "T2 01:15", "holm", "aussage", wissende=["holm"], codex="Holm: found the bridge locked at 01:15", wege=[HOLM(), HOLM_HANDY()])],
     KETTE(handlung=[["f3_03", "f3_04"], ["f3_02", "f3_05", "f3_04"]],
           person=[["f3_06", "f3_05", "f3_12"], ["f3_07", "f3_08", "f3_05", "f3_12"],
                   ["f3_10", "f3_11", "f3_12", "f3_05"], ["f3_19", "f3_07", "f3_05"]],
           folge=[["f3_01", "f3_03", "f3_15"], ["f3_02", "f3_04", "f3_15"]]),
     [WS("f3_ws1", 2, "f3_13", ["f3_06", "f3_07"], "Statement: plan changed on Sunday at lunchtime - file version "
                                                   "and reservation: four days earlier", "f3_14")],
     "The display reports the departure at %s, the crew remembers \"half past one\" - only with the clocks matched do "
     "both fit. Logbook and log show the same sequence with no intervention during the night; the cause lies in the "
     "plan, not at a switch." % uhr(pms("T2 01:30")),
     [GH("f3_gh1", 2, "nacht", {"angst": [">=", 1]}, "Supplies a true observation about another person in the wrong "
                                                     "context.", "f3_16",
         notiz="Counter: check the time (engine log 01:40, Lola 01:45). From trust 3 she corrects herself the next "
               "morning (flag sophia_korrigiert)."),
      GH("f3_gh2", 3, "nacht", {"angst": [">=", 2]}, "Overwrites the plan file on the office PC.", "f3_18",
         blockiert=["f3_05_w1", "f3_06_w1"], umweg=["f3_05_w2", "f3_05_w3", "f3_07_w1", "f3_10_w1"])],
     GEST([{"ab_tag": 3, "bedingung": ALLE(V("sophia", ">=", 3), {"kette_bekannt": [">=", 1]}),
            "form": "She corrects herself before Duc pins her down - without charm, as a request for a talk."}],
          "Arranging favours for other people is my job. Doing it for myself suddenly made it a lie.",
          "Arranging favours for other people is my job. Doing it for myself, it suddenly became a lie."),
     {"weiss": ["f3_12", "f3_02", "f3_20"],
      "sagt_von_sich": "I shouldn't have given in. Leaving at night without a charging run - that wasn't my idea.",
      "auf_nachfrage": {"wer_wollte_01_30": "f3_12", "tuer": "f3_20"},
      "vermutung": "I shouldn't have given in.",
      "haltung": "takes the blame on herself; only names Sophia if Duc asks about the plan"},
     [TIPP("f3_t1", "lola", 2, "Last week Sophia asked me if the bar in Cala d'Orsu takes table reservations for the "
                               "morning. Last week!", "f3_07_w1"),
      TIPP("f3_t2", "lola", 2, "The night before last Sophia was still at the office PC. At midnight.", "f3_18_w1", ab_tag=4, nach="f3_gh2")],
     {"chiara": "h_22", "rosi": "h_23", "siri": "f3_19"},
     ANGST_STANDARD,
     "She speaks to the affected group without any charming detour. The risk is rewarded; the responsibility stays.",
     sonder={"kontakt": "Helene Marchal, editor at a Paris publishing house (exists in every case as Sophia's "
                        "contact; only here is there a meeting). Her identity comes only through conversation or a "
                        "message Sophia shares, never by reading someone else's phone."})

# ------------------------------------------------------------------ Fall 4
FALL(4, "rosi", "The Harmless Delay",
     "After her round Rosi sets a service lock with card 2, which she assumes will only force a short, supervised "
     "function test after anchoring. That would have delayed the arrival in Calvi (the bet) and given her a morning "
     "with Duc. But the controller treats the automatic switchover A->B like a cold start and goes into R2; "
     "protective stop; Holm presses the offered restart; LM3 fails.",
     {"abfahrt": "T2 03:00", "holm_bruecke_ab": "T2 02:40", "ladelauf": True, "fahrt_kn": 8.0,
      "ausfall": "T2 06:11", "ankern": "T2 07:50"},
     [ZL("T2 00:50", "Rosi bets €50 on \"after 6 pm\"; Totò cuts the odds from 6:1 to 2:1", ["rosi"], ["toto"]),
      ZL("T2 01:40", "Rundgang (Maschinenbuch)", ["rosi"]),
      ZL("T2 01:44", "Service lock with card 2, expiry 08:00", ["rosi"]),
      ZL("T2 01:50", "Diagnosis draft: function test after anchoring, with Duc", ["rosi"]),
      ZL("T2 06:05", "Umschaltung A->B unter Sperre: Profil R2, Schutzstopp", ["holm"]),
      ZL("T2 06:10", "Holm presses \"Restart\"", ["holm"]),
      ZL("T2 06:11", "LM3-Ausfall", [], ["duc", "lola", "holm"]),
      ZL("T2 07:50", "Rosi lifts the lock (card 2), alone in the control room", ["rosi"], ["lola"]),
      ZL("T2 09:30", "Rosi's diagnostic log with the old service device (lock history included)", ["rosi"])],
     [AUSFALL(4, "T2 06:11", " (after restart)"),
      LOGBUCH_F(4, "T2 06:11", "06:05 Anzeige SERVICE-SPERRE, Schutzstopp. 06:10 Wiederanlauf. 06:11 Antrieb aus."),
      PMS_F("f4_03", "T2 01:44", "%s: service lock set (card 2), expiry 08:00 - function test before next cold start"),
      PMS_F("f4_04", "T2 06:05", "%s: switchover A->B under service lock - profile R2; protective stop; restart from "
                                 "the bridge"),
      PMS_F("f4_05", "T2 07:50", "%s: Service-Sperre aufgehoben (Karte 2)"),
      F("f4_06", "aussage", "Holm: at six minutes past six it read SERVICE LOCK ACTIVE, then protective stop. The "
                            "display offered a restart. She pressed it. After that it was over.", "T2 06:10", "holm", "aussage", wissende=["holm"],
        codex="Holm: service lock display, protective stop, she pressed restart", wege=[HOLM(), HOLM_HANDY()]),
      F("f4_07", "dokument", "Totò's betting book: Day 2, 00:50 Rosi, €50 on \"after 6 pm\"; odds cut from 6:1 to "
                             "2:1.", "T2 00:50", "wettbuch", "belastbar", wissende=["toto", "rosi"],
        codex="Betting book: 00:50 Rosi €50 on \"after 6 pm\", odds 6:1 -> 2:1",
        wege=[W("befragen", "Get Totò to show you his betting book", person="toto", g="wettbuch"),
              W("untersuchen", "The drawer under the mess counter", ort="crew_mess", auffaellig=False,
                g="messe_schublade")]),
      F("f4_08", "aussage", "Totò: \"Shortly before one Rosi put fifty on 'after six'. So I cut the odds. She knows "
                            "something.\"", "T2 00:50", "toto", "aussage", wissende=["toto"],
        codex="Totò: Rosi bet €50 on late - he cut the odds",
        wege=[W("befragen", "Ask Totò about the bets", person="toto")]),
      F("f4_09", "dokument", "Rosi's notebook (Day 2, 01:50): \"After anchoring: function test after lock, cold start "
                             "approx. 20 min - with Duc.\"", "T2 01:50", "notizbuch", "belastbar", wissende=["rosi"],
        codex="Rosi's notebook 01:50: function test after lock, after anchoring, with you",
        wege=[W("untersuchen", "Rosi's notebook on her makeshift workbench", ort="power_room", g="notizbuch"),
              W("freiwillig", "Rosi shows you her notes", person="rosi", tage=(3, 7), bed=V("rosi", ">=", 3),
                g="rosi_freiwillig")]),
      F("f4_10", "aussage", "Lola: at quarter to eight Rosi went into the control room alone with a coffee.", "T2 07:45",
        "lola", "aussage", wissende=["lola"], codex="Lola: Rosi alone into the control room at 07:45",
        wege=[W("befragen", "Ask Lola about the morning", person="lola")]),
      F("f4_11", "aussage", "Rosi: \"After my round at 01:40 I went straight to my bunk.\"", "T2 01:40", "rosi",
        "aussage", wahr=False, wissende=["rosi"], codex="Rosi: straight to her bunk after her round at 01:40",
        widerlegt=['f4_03', 'r_12', 'f4_09'], wege=[W("befragen", "Ask Rosi about the night", person="rosi")]),
      F("f4_12", "aussage", "Rosi (when pressed): \"I only checked the status at the terminal.\"", "T2 01:44",
        "rosi", "aussage", wahr=False, wissende=["rosi"], codex="Rosi: only checked the status at the terminal",
        widerlegt=['f4_03'], wege=[W("befragen", "Nachfragen", person="rosi", tage=(2, 7), braucht=["f4_11", "f4_03"])]),
      F("f4_13", "dokument", "Original diagnostic log, day 2 (old service device): \"Lock 01:44-07:50 (card 2), "
                             "switchover in R2, restart 06:10.\"", "T2 09:30", "servicegeraet_alt", "gesichert",
        wissende=["rosi"], codex="Old service device: lock 01:44-07:50, switchover in R2, restart 06:10",
        wege=[W("untersuchen", "Look at Rosi's log binder in the power room", ort="power_room", tage=(2, 2),
                g="protokollordner"),
              W("handy", "Have Petru read out the old service device", person="petru", tage=(3, 7),
                braucht=["f4_14"], g="petru_servicegeraet"),
              W("freiwillig", "Rosi fetches the old device herself", person="rosi", tage=(3, 7), bed=V("rosi", ">=", 3),
                g="rosi_freiwillig")]),
      F("f4_14", "dokument", "Since Day 2, 22:40 there has been a new measurement in the log binder (a different "
                             "device, without lock history); the old service device has been tidied away into the "
                             "spare-parts crate in the power room.", "T2 22:40", "servicegeraet_alt",
        "belastbar", wissende=["rosi"], codex="Log binder: measurement from Day 2, 22:40 replaces the one from the "
                                              "morning; old device in the crate",
        wege=[W("untersuchen", "Rosi's log binder and the crate in the power room", ort="power_room", tage=(3, 7),
                auffaellig=False, g="protokollordner")]),
      F("f4_15", "messung", "According to the manual the lock only applies to the next cold start; in reality the "
                            "controller treats the automatic switchover like a cold start and goes into R2. The "
                            "restart from R2 overloads LM3.", "T2 06:05", "herstellerunterlagen", "gesichert", wissende=[],
        codex="Engineering: switchover under lock goes into R2; restart from R2 overloads LM3",
        wege=[PETRU_UNTERLAGEN(),
              ROSI_TEST("Have Rosi explain what the lock does during the switchover", bed=V("rosi", ">=", 2),
                        braucht=["f4_04"])]),
      F("f4_16", "beobachtung", "At the party, in the control room: all green. Rosi winks: \"If we're late into Calvi "
                                "tomorrow, I'm rich.\"", "T1 20:10", "duc", "beobachtet", wissende=["duc"],
        codex="Memory: Rosi - \"If we're late into Calvi tomorrow, I'm rich\"",
        wege=[W("erinnerung", "You helped Rosi with the test", bed=FLAG("auftakt_hilfe_rosi"), g="auftakt")])],
     KETTE(handlung=[["f4_03", "f4_04"], ["f4_02", "f4_06", "f4_13"]],
           person=[["r_09", "f4_03", "r_12", "f4_09"], ["f4_05", "f4_10", "f4_03", "f4_09"],
                   ["f4_07", "f4_08", "r_09", "f4_03", "r_12"], ["f4_13", "f4_10", "f4_05"],
                   ["f4_16", "f4_07", "r_09", "f4_03", "r_12"]],
           folge=[["f4_04", "f4_01", "f4_15"], ["f4_13", "f4_15"], ["f4_02", "f4_06", "f4_15"]]),
     [WS("f4_ws1", 2, "f4_11", ["f4_03"], "Statement: straight to her bunk after her round - log: service lock at %s "
                                          "(display time)" % uhr(pms("T2 01:44")), "f4_12", braucht=["r_12"])],
     "The display reports the lock at %s - seemingly BEFORE Rosi's round (01:40, engine log). With the clocks "
     "matched it's 01:44: during her round." % uhr(pms("T2 01:44")),
     [GH("f4_gh1", 2, "nacht", {"angst": [">=", 1]}, "On her own authority replaces the morning's diagnostic log "
                                                     "with a new measurement and tidies the old service device away.", "f4_14",
         blockiert=["f4_13_w1"], umweg=["f4_13_w2", "f4_13_w3"],
         notiz="Afterwards she works too long and takes corrections personally (behaviour, no further counteraction).")],
     GEST([{"ab_tag": 3, "bedingung": ALLE(V("rosi", ">=", 3), EINE(FLAG("gemeinsam_rekonstruiert"),
                                                                     {"kette_bekannt": [">=", 2]})),
            "form": "When you work on the propulsion together, she stops repairing in the middle of a sentence."}],
          "Ich wollte einen Morgen. Nicht diese Woche.", "I wanted one morning. Not this week.",
          extra={"holm_rolle": "Holm's restart belongs in the report - she followed the display, she is not at fault."}),
     {"weiss": ["f4_06", "f4_02", "r_08"],
      "sagt_von_sich": "I broke it by pressing. The display offered a restart, and I pressed it.",
      "auf_nachfrage": {"anzeige": "f4_06"},
      "vermutung": "Who sets a lock at night? Ask engineering. And me - I pressed the button.",
      "haltung": "blames herself; takes Duc more seriously if he clears her"},
     [TIPP("f4_t1", "lola", 2, "Rosi and Totò were arguing about odds yesterday. Totò has this book.",
           "f4_07_w1"),
      TIPP("f4_t2", "lola", 2, "In the middle of the night Rosi put an old measuring device away in the crate in the "
                               "power room.", "f4_14_w1", ab_tag=3, nach="f4_gh1")],
     {"chiara": "h_22", "rosi": "f4_16", "siri": "h_24"},
     ANGST_STANDARD,
     "An open confession and help with the reconstruction. A romance may break over it; a gift or a sex scene does "
     "not heal the breach of trust.")

# ------------------------------------------------------------------ Fall 5
FALL(5, "yasin", "The Shot That Was Meant to Stay",
     "For the sunrise shoot Yasin charges six drone batteries, LED panels and a laptop through a multi-socket "
     "adapter on the stern distribution board, against the 2 kW limit he signed. The branch trips and opens the bus "
     "tie; Totò refuses, so Yasin closes it again himself. The bus tie closes under load, the controller goes into "
     "R2, LM3 fails. His camera is running the whole time.",
     {"abfahrt": "T2 03:00", "holm_bruecke_ab": "T2 02:40", "ladelauf": True, "fahrt_kn": 8.0,
      "ausfall": "T2 06:28", "ankern": "T2 07:50"},
     [ZL("T1 11:00", "Yasin signs the load limit", ["yasin", "holm"]),
      ZL("T1 20:40", "Chargers on the red multi-socket adapter in the tender garage", ["yasin"], ["duc", "siri"]),
      ZL("T2 05:30", "Batteries, panels, laptop via adapter YB-CREW 3 on the stern distribution board (~4.6 kW); "
                     "camera running",
         ["yasin"]),
      ZL("T2 05:40", "Totò gets the tender ready for the shoot", ["toto"]),
      ZL("T2 06:22", "Schutzabschaltung Abzweig Heck, Querkupplung getrennt", [], ["holm"]),
      ZL("T2 06:23", "Yasin bittet Toto, wieder einzulegen; Toto: \"Frag Rosi\"", ["yasin", "toto"]),
      ZL("T2 06:25", "Yasin closes it again himself -> bus tie under load, profile R2", ["yasin"], ["toto"]),
      ZL("T2 06:28", "LM3-Ausfall", [], ["duc", "lola", "holm"]),
      ZL("T2 06:40", "Adapter scorched, ends up in the waste bin of the tender garage", ["yasin"]),
      ZL("T2 07:10", "Yasin sends Siri the raw clip for her story selection", ["yasin"], ["siri"])],
     [AUSFALL(5, "T2 06:28", " (Profil R2)"),
      LOGBUCH_F(5, "T2 06:28", "06:22 Schutzabschaltung Heck. 06:25 wieder drin (?). 06:28 Antrieb aus."),
      PMS_F("f5_03", "T2 06:22", "%s: protective trip of the stern branch (overload), bus tie opened; three minutes "
                                 "later manually reconnected at the stern distribution board, profile R2"),
      F("f5_04", "messung", "Stern distribution board memory (own clock, ship's time): tripped at 06:22 at 4.6 kW; "
                            "manually reconnected at 06:25.", "T2 06:25", "heckverteiler", "gesichert", wissende=[],
        codex="Stern distribution board: tripped at 06:22 at 4.6 kW, manually reconnected at 06:25",
        wege=[W("untersuchen", "Read out the stern distribution board memory", ort="tender_garage", g="heckverteiler"),
              W("befragen", "Have Rosi read out the stern distribution board", person="rosi", g="befragen:rosi")]),
      F("f5_05", "gegenstand", "Roter Mehrfachadapter, Etikett \"YB-CREW 3\", verschmort.", "T2 06:40", "heckverteiler",
        "gesichert", wissende=["yasin"], codex="Verschmorter Mehrfachadapter, Etikett YB-CREW 3",
        wege=[W("untersuchen", "The waste bin in the tender garage", ort="tender_garage", tage=(2, 3), g="abfallkorb"),
              W("anordnen", "Order Yasin's camera case opened, as commander", person="yasin", tage=(4, 7),
                kosten={"vertrauen": ["yasin", -3], "ruf": -1}, g="kamerakiste")]),
      F("f5_06", "gegenstand", "Yasin's equipment carries labels \"YB-CREW 1-6\".", "T1 12:00", "kamera",
        "gesichert", wissende=["yasin", "siri"], codex="Yasin's equipment: labels YB-CREW 1-6",
        wege=[W("untersuchen", "Look at Yasin's equipment on deck", ort="aft_deck", g="ausruestung"),
              W("befragen", "Ask Siri about the labels", person="siri", g="siri")]),
      F("f5_07", "dokument", "Yasin's raw clip: the light flickers (protective trip), Yasin reconnects at the stern "
                             "distribution board (\"Come on...\"), three minutes later blackout.", "T2 06:25", "kamera", "belastbar",
        wissende=["yasin", "siri"], uebermittlung=[UE("siri", "T2 07:10", "Yasin sends her the raw clip")],
        codex="Raw clip: Yasin reconnects the stern distribution board, three minutes later blackout",
        wege=[W("befragen", "Ask Siri for her copy", person="siri", tage=(2, 7), bed=V("siri", ">=", 3),
                g="siri_kopie"),
              W("tausch", "Yasins Angebot annehmen", person="yasin", tage=(4, 7), bed=FLAG("yasin_angebot"),
                kosten={"flag": "duc_schuldet_yasin"}, g="yasin_tausch")]),
      F("f5_08", "aussage", "Totò: Yasin wanted him to push the switch back in at the stern distribution board. Totò "
                            "refused (\"Ask Rosi\"). Yasin did it himself, shortly before everything went off.", "T2 06:25", "toto",
        "aussage", wissende=["toto"], codex="Totò: Yasin reconnected the stern distribution board himself",
        wege=[W("befragen", "Ask Totò about the morning in the tender garage", person="toto")]),
      F("f5_09", "aussage", "Totò: \"He had this red five-way plug. It stank afterwards.\"",
        "T2 06:40", "toto", "aussage", wissende=["toto"], codex="Totò: red five-way plug, stank",
        wege=[W("befragen", "Ask Totò about Yasin's charging gear", person="toto", braucht=["f5_08"])]),
      F("f5_10", "aussage", "Yasin: \"I only charged at the charging station in the mess. When the light flickered, I "
                            "was up on deck.\"", "T2 06:22", "yasin", "aussage", wahr=False, wissende=["yasin"],
        codex="Yasin: only charged at the charging station in the mess, on deck when it flickered",
        widerlegt=['f5_12', 'f5_08', 'f5_04'], wege=[W("befragen", "Ask Yasin about the morning", person="yasin")]),
      F("f5_11", "aussage", "Yasin (when pressed): \"At the stern board I only unplugged my batteries.\"",
        "T2 06:25", "yasin", "aussage", wahr=False, wissende=["yasin"], codex="Yasin: only unplugged at the stern "
                                                                              "distribution board",
        widerlegt=['f5_04'], wege=[W("befragen", "Nachfragen", person="yasin", tage=(2, 7), braucht=["f5_10"], setzt="duc_fragt_original")]),
      F("f5_12", "messung", "Hotel load list: no charging at the charging station in the mess between 05:30 and "
                            "06:30.",
        "T2 05:30", "pms", "gesichert", wissende=["rosi"], codex="Hotelnetz: Ladestation Messe 05:30-06:30 ohne Last",
        wege=[SERVICEKOPIE(), W("befragen", "Have Rosi show you the consumption list", person="rosi",
                                g="befragen:rosi")]),
      F("f5_13", "messung", "Closing the bus tie under load forces the controller into R2; LM3 carries the peak load "
                            "and fails.", "T2 06:25", "herstellerunterlagen", "gesichert", wissende=[],
        codex="Engineering: bus tie under load -> R2 -> LM3 overloaded",
        wege=[ROSI_TEST("Have Rosi trace the sequence in the control room", braucht=["f5_03"]),
              PETRU_UNTERLAGEN()]),
      F("f5_14", "beobachtung", "At the party: Yasin's devices are charging on a red multi-socket adapter at the "
                                "service socket in the tender garage.", "T1 20:40", "duc", "beobachtet", wissende=["duc"],
        codex="Memory: Yasin's chargers on the red multi-socket adapter in the tender garage",
        wege=[W("erinnerung", "You got Siri out of the shoot", bed=FLAG("auftakt_hilfe_siri"),
                g="auftakt")]),
      F("f5_15", "dokument", "Shortened clip online: Duc laughing at the afterparty, cut, blackout - \"First Officer "
                             "parties while the yacht dies\". The timestamp jumps from 03:02 to 06:28.", "T2 23:00",
        "kamera", "belastbar", wissende=["yasin"], codex="Clip online: the cut jumps from 03:02 to 06:28",
        wege=[W("handy", "Watch the clip online", tage=(3, 7), auffaellig=False, g="clip_online")]),
      F("f5_16", "gegenstand", "The waste bin in the tender garage is empty.", "T3 23:00", "heckverteiler", "gesichert",
        wissende=["yasin"], codex="Tendergarage: Abfallkorb leer",
        wege=[W("untersuchen", "The waste bin in the tender garage", ort="tender_garage", tage=(4, 7),
                auffaellig=False, g="abfallkorb")]),
      F("f5_17", "nachricht", "Yasin offers the original - in exchange for the wording \"faulty charging station\" in "
                              "the report.", "T4 12:00", "telefon", "belastbar", wissende=["yasin"],
        codex="Yasin's offer: the original in exchange for a wording in the report",
        wege=[W("freiwillig", "Yasin texts you", person="yasin", tage=(4, 7), auffaellig=False,
                bed=FLAG("yasin_angebot"), g="yasin_tausch")])],
     KETTE(handlung=[["f5_03"], ["f5_04", "f5_02"]],
           person=[["f5_05", "f5_06", "f5_04", "r_03"], ["f5_08", "f5_04", "r_03", "f5_12"], ["f5_07", "r_03"],
                   ["f5_14", "f5_08", "f5_04", "r_03"]],
           folge=[["f5_03", "f5_01", "f5_13"], ["f5_04", "f5_02", "f5_13"], ["f5_07", "f5_13"]]),
     [WS("f5_ws1", 2, "f5_10", ["f5_08", "f5_12"], "Statement: only charged at the charging station, up on deck when "
                                                   "it flickered - Totò: was at the stern distribution board; the "
                                                   "charging station shows no charging", "f5_11")],
     "The stern distribution board shows 06:25 (ship's time), the controller %s - only with the clocks matched is it "
     "the same minute."
     % uhr(pms("T2 06:25")),
     [GH("f5_gh1", 2, "nacht", {"angst": [">=", 1]}, "Publishes a shortened excerpt that makes Duc look "
                                                     "irresponsible (reputation -1, Megan calls).", "f5_15",
         notiz="Kein Beweis geht verloren (Rohclip, Heckverteiler, Toto). Ruf-Schaden bleibt bis zur Richtigstellung."),
      GH("f5_gh2", 3, "nacht", {"angst": [">=", 2]}, "Takes the adapter out of the waste bin and hides it in his "
                                                     "camera case.", "f5_16", blockiert=["f5_05_w1"], umweg=["f5_05_w2", "f5_08_w1", "f5_04_w1"]),
      GH("f5_gh3", 4, "tag", ALLE({"angst": [">=", 2]}, FLAG("duc_fragt_original")), "Ties handing over the original to an "
                                                                                     "advantage (flag yasin_angebot).", "f5_17",
         notiz="Whoever agrees gets real information and a new dependency (duc_schuldet_yasin). No second exclusive "
               "original is invented after that.")],
     GEST([], "You need an explanation. I need my people to still believe me. We could both get what we need.",
          "You need an explanation. I need my people to still believe me. We could both get what we need.",
          extra={"hinweis": "No voluntary confession; with a complete chain he admits what is proven. The key "
                            "sentence comes with the offer (f5_gh3)."}),
     {"weiss": ["f5_02", "r_08"],
      "sagt_von_sich": "At twenty past six it tripped at the stern, three minutes later it was back on. I shouted "
                       "into the tender garage. Nobody answered.",
      "auf_nachfrage": {"heck": "f5_02"},
      "vermutung": "Somebody was messing about at the stern. Ask Totò, he was down there.",
      "haltung": "zeigt Richtung Tendergarage, nennt keinen Namen"},
     [TIPP("f5_t1", "lola", 2, "Yasin put something scorched in his camera case. Smelled like burnt toast.",
           "f5_05_w2", ab_tag=4, nach="f5_gh2"),
      TIPP("f5_t2", "lola", 2, "Siri has the whole video. She just doesn't talk about it.", "f5_07_w1")],
     {"chiara": "h_22", "rosi": "h_23", "siri": "f5_14"},
     ANGST_STANDARD,
     "Siri's self-determination is kept apart from his guilt: she may leave him in every case; her freedom is not a "
     "reward for the right suspicion.")
