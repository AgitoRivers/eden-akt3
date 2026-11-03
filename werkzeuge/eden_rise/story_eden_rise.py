# -*- coding: utf-8 -*-
"""Hauptstory eden_rise -> module/eden_rise/story.json (17.10.2026, Phase A).

VERTRAULICH: story.json enthält die Auflösung aller fünf Fälle (Fall 6 am 27.10.2026 gestrichen). Dieser Builder gibt nur Zahlen aus.
Bausteine: story_basis.py · Fakten und Fälle: story_faelle.py · Prüfung: story_pruefen.py
Hier: Schaltplan der Bordsysteme, zweite Wahrheit (Akt 1 nur Hinweise auf Alons Geraet), Wochenbogen Akt 1 (Tag 1-7:
Cold Open, Party als Rueckblende, Strandung, Bucht, Spuren, Megan an Bord + Sturm, Lagerfeuer, Anhoerung + Cliffhanger;
Umbau 24.10.2026), Anhoerung (Daten), Ende Akt 1, Fairness- und Sprachmodell-Regeln, Prueffaelle.
"""
import copy, json, os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
EDEN = os.path.dirname(os.path.dirname(HIER))    # werkzeuge\eden_rise -> Eden
ZIEL = os.path.join(EDEN, "module", "eden_rise", "story.json")

from story_basis import (F, W, V, FLAG, ALLE, EINE, NICHT, TIPP, GLIEDER, WEG_ARTEN, PMS_VERSATZ_MIN, AUSFALL_FENSTER,
                         VERDAECHTIGE, ZUVERLAESSIG, minuten)
import story_faelle

# ================================================================== SCHALTPLAN (fiktiv, in allen Fällen gleich)
SCHALTPLAN = {
    "hinweis": "Simplified, fictional power grid of the Eden Rise. Applies in all five cases. Clues show events in "
               "this grid, never, as if by magic, a person's morals.",
    "knoten": {
        "solar": {"label": "Solardach (Hardtop)", "art": "quelle",
                  "regel": "charges both banks; a clear day about a third, cloudy a little, a storm nothing"},
        "bank_a": {"label": "Batteriebank A (Fahrbatterie)", "art": "speicher", "versorgt": ["umrichter"],
                   "regel": "below the reserve threshold the controller goes into reserve mode (uses profile R2)"},
        "bank_b": {"label": "Batteriebank B (Hotelbatterie)", "art": "speicher", "versorgt": ["hotel_wr"]},
        "querkupplung": {"label": "Querkupplung A–B", "art": "schalter",
                         "regel": "closed while under way, B supports A; on overload it opens (protection). If it is "
                                  "closed again under load, the controller switches to profile R2 - that is not in "
                                  "the ship's manual."},
        "pms": {"label": "Energiesteuerung (PMS)", "art": "steuerung",
                "regel": "logs every event with its time; its clock is %d minutes slow" % PMS_VERSATZ_MIN},
        "umrichter": {"label": "Antriebs-Umrichter", "art": "wandler", "module": ["lm1", "lm2", "lm3"]},
        "lm3": {"label": "Leistungsmodul LM3", "art": "bauteil", "typ": "PX-480", "charge": "22-B",
                "zustand": "thermally pre-damaged by a foreign component (unknown on board, Act 3)"},
        "r2": {"label": "Fallback profile R2", "art": "betriebsart",
               "doku": "Ship's manual p. 4-17 describes R2 as a permitted emergency profile with reset via \"End "
                       "diagnosis\". According to a manufacturer notice it is not approved for the PX-480; \"End "
                       "diagnosis\" does not reset it.",
               "wird_aktiv_bei": ["manually at the bridge maintenance switch after a protective abort",
                                  "Reservebetrieb (Bank A unter Reserveschwelle)",
                                  "automatische Umschaltung A→B unter Service-Sperre",
                                  "closing the bus tie again under load"],
               "wirkung": "carries on with a shifted load distribution; LM3 carries the peak load - thermal overload "
                          "for a pre-damaged PX-480"},
        "motor": {"label": "E-motor and shaft", "art": "antrieb"},
        "hotel_wr": {"label": "Hotel-Wechselrichter", "art": "wandler",
                     "regel": "after a propulsion failure, island mode: bank B only supplies the reduced hotel load"},
        "hotelnetz": {"label": "Hotelnetz", "art": "verbraucher",
                      "verbraucher": ["Cold rooms", "Wassermacher", "Toiletten", "Galley", "Licht", "Klima",
                                      "Ladestation Crew-Messe (2 kW)", "Heckverteiler"]},
        "heckverteiler": {"label": "Heckverteiler (Tendergarage)", "art": "verteiler", "lastgrenze_kw": 2,
                          "regel": "own clock in ship's time; stores trips and manual reconnections"},
        "notversorgung": {"label": "24 V emergency supply with its own battery", "art": "unabhaengig",
                          "versorgt": ["UKW/DSC-Funk", "Seenotbake", "Ankerlicht", "Ankeralarm", "Bilgepumpen",
                                       "Notbeleuchtung"],
                          "regel": "independent of A and B. No decision in the game switches it off or trades it for "
                                   "something."},
        "unit01": {"label": "Unit-01 (Diesel-Notgenerator)", "art": "quelle",
                   "kann": ["Bank B laden", "Wassermacher direkt", "Diagnostic run of the propulsion (repair work)",
                            "Bow thruster for manoeuvres"],
                   "kostet": "1 Diesel je Einsatz"},
        "wartungsschalter": {"label": "Bridge maintenance switch (key)", "art": "bedienung",
                             "schluessel": ["holm", "duc", "rosi", "chiara"]},
        "servicekarten": {"label": "Servicekarten", "art": "bedienung",
                          "karten": {"1": "Captain (Duc from day 2)", "2": "Engineering – hangs on the hook in the "
                                                                           "engine control room", "3": "Yard/Office – drawer in the ship's office"}},
        "servicesperre": {"label": "Service-Sperre", "art": "betriebsart",
                          "regel": "according to the manual: function test before the next cold start. In reality "
                                   "the controller also treats the automatic switchover A→B like a cold start and "
                                   "goes into R2."},
        "plotter": {"label": "Chart plotter with GPS track", "art": "navigation", "regel": "GPS-Zeit = Schiffszeit"},
        "drucker": {"label": "Printer in the ship's office", "art": "buero", "regel": "stores jobs with user and time"},
        "buero_pc": {"label": "Office PC", "art": "buero", "regel": "voyage plans, route plans, file versions"},
        "servicegeraet_alt": {"label": "Old service device (power room)", "art": "messgeraet",
                              "regel": "stores every log created with it"},
    },
    "kanten": [["solar", "bank_a"], ["solar", "bank_b"], ["bank_a", "querkupplung"], ["bank_b", "querkupplung"],
               ["bank_a", "umrichter"], ["umrichter", "motor"], ["pms", "umrichter"], ["pms", "querkupplung"],
               ["pms", "bank_a"], ["bank_b", "hotel_wr"], ["hotel_wr", "hotelnetz"], ["hotelnetz", "heckverteiler"],
               ["unit01", "bank_b"], ["unit01", "umrichter"], ["wartungsschalter", "pms"],
               ["servicekarten", "pms"]],
    "grundsaetze": [
        "A failed propulsion doesn't mean there's no power: hotel load in island mode, emergency supply independent.",
        "A small consumer never destroys a propulsion system on its own: every chain runs through the shared weak "
        "spot (pre-damaged LM3 + badly documented R2).",
        "The normal protection would have limited most triggers - that's why the second truth (Alon's component on "
        "LM3) is real in every case.",
        "Failure and bang are two moments: the failure lies between 06:11 and 06:35 depending on the case, the bang "
        "in the inverter is always at 06:35 (the foreign component drives LM3 into runaway after the failure).",
        "No forced diesel-versus-radio decision. Repair and towing compete for time, material, weather windows and "
        "hands.",
    ],
    "uhren": {"schiffszeit": "Reference: bridge clock, phones, camera, GPS, engine log, stern distribution board",
              "pms": "geht %d Minuten nach" % PMS_VERSATZ_MIN},
    "technische_wege": {
        "reparatur": "Replace or bridge LM3: spare module (Megan/Petru), diagnostic runs with Unit-01 (diesel), "
                     "weather window, Rosi and Petru as hands.",
        "schlepp": "Salvage window through Elsa or Megan; a professional rescue is never morally inferior.",
        "isolation": "Isolate LM3 properly: fire risk eliminated, afterwards only slow or no motoring under her own "
                     "power.",
        "warnzeichen": ["Heat on the inverter casing", "Smell of hot plastic", "steigende Messwerte",
                        "wiederkehrende Warnungen"],
        "brand": "Not in Act 1: LM3 exploded in the cold open (06:35), the inverter is destroyed.",
    },
}

# ================================================================== ZWEITE WAHRHEIT (Akt 1: nur Hinweise, Aufloesung Akt 3)
# Umbau Akt 1 (Nacht 24.10.2026, Brain Trust 6): Herstellermeldung, Megans Mitzeichnung, Routen, Wendung und Bericht
# entfallen. Die zweite Wahrheit ist jetzt Alons Geraet; in Akt 1 gibt es nur unscheinbare Beobachtungen ohne
# Kettenfunktion. Keine davon betrifft den Ausloeser der Nacht, keine nennt Alon (Toto ist kein Verdaechtiger).
ZW_FAKTEN = [
    F("z_01", "beobachtung", "Behind the burnt-out inverter a small red light is blinking. There is no component at "
                             "this spot in the wiring diagram.", "T2 11:30", "lm3", "beobachtet", wissende=["toto"],
      codex="Red blinking light behind the inverter - not in the wiring diagram",
      wege=[W("untersuchen", "Shine a light behind the burnt-out inverter", ort="power_room", tage=(2, 7),
              auffaellig=False, g="rotes_licht")]),
    F("z_02", "beobachtung", "Totò avoids the corner with the red light. When Duc shows it to him, he turns grey and "
                             "changes the subject.", "T2 12:00", "toto", "beobachtet", wissende=["toto"],
      codex="Totò avoids the red light",
      wege=[W("untersuchen", "Watch who avoids the red light in the propulsion room", ort="power_room",
              tage=(2, 7), braucht=["z_01"], auffaellig=False, g="rotes_licht_blick")]),
    F("z_03", "aussage", "Megan, looking at the damage: \"A PX-480 doesn't just burn.\" Then she carries on writing as "
                         "if she hadn't said anything.", "T5 11:30", "megan", "aussage", wissende=["megan"],
      codex="Megan: \"A PX-480 doesn't just burn.\"",
      wege=[W("befragen", "Ask Megan about the damage", person="megan", tage=(5, 7), g="megan_schaden")]),
    F("z_04", "aussage", "Megan demands a cause report and a hearing on board by the end of the week. Without "
                         "someone to blame she fires the whole crew; the season bonus is her leverage.", "T2 09:10", "megan", "aussage",
      wissende=["megan", "holm"],
      codex="Megan's ultimatum: report and hearing in seven days - otherwise the whole crew is out",
      wege=[W("handy", "Megans erster Anruf", person="megan", tage=(2, 2), g="megan_anruf")]),
    F("z_05", "beobachtung", "Megan is quietly on the phone on deck and says \"A.V.\" twice. Asked about it: \"A buyer "
                             "from Monaco. Not your problem.\"", "T5 19:40", "telefon", "beobachtet", wissende=["megan"],
      codex="Megan on the phone: \"A.V.\" twice - \"a buyer from Monaco\"",
      wege=[W("befragen", "Ask Megan about the phone call", person="megan", tage=(5, 7), g="megan_telefonat")]),
    F("z_06", "dokument", "Totò's betting book: since the party night he's been paying out unusually high winnings. "
                          "And he's wearing a new gold chain.", "T3 10:00", "wettbuch", "belastbar", wissende=["toto"],
      codex="Totò has been paying out big winnings since the party night, new gold chain",
      wege=[W("untersuchen", "Take a look at Totò's betting book", ort="crew_mess", tage=(3, 7), auffaellig=False,
              g="wettbuch_geld")]),
]

# Lolas Tratsch zur zweiten Wahrheit (Duc 23.10.: "zaehlt nachts Geld", nur Wegweiser) - in allen Faellen gleich
ZW_TIPP = TIPP("z_t1", "lola", 2, "Totò counts money at night. A lot of money. Since the party. Don't ask me where "
                                  "it's from.",
               "z_06_w1", ab_tag=4)

ZWEITE_WAHRHEIT = {
    "akt": 3,
    "kern": "Alon's agent bought Totò through his cousin Gennaro (€20,000, \"nobody gets hurt\"); one night in Antibes "
            "Totò fitted a foreign component to LM3. It thermally pre-damaged the module and drove it into runaway "
            "after the failure - hence the bang at 06:35 in every case. The trigger from the case only gave it the "
            "final push. Alon's motive: a disaster instead of an advertisement for the bay, bad press, a low price.",
    "hafen": "For decades the Eden Group has owned the commercial harbour quarter of Cala d'Orsu (quay, warehouses, "
             "the land under Alva's bar). Megan is supposed to sell it; the buyer is A.V. Estates (she only knows "
             "the company name), and her promotion depends on the price. The Eden Bay Weekend (sunrise, Siri posts, "
             "Yasin films) is meant to drive the price up; the bang at 06:35 is Alon's countermove. The sale is not "
             "revealed before Act 2.",
    "alon_korsika": "A: remote and yet close (empty mountains, Monaco one night away, the Legion in Calvi -> "
                    "Adrien's unit). B: the harbour is his logistics (cages, animals and equipment can't come over "
                    "the mountain road; the resort is a pretext for cranes, warehouses and supply boats) -> he needs "
                    "exactly the harbour quarter, cheaply. C: as a child he spent summers with his grandmother in "
                    "Cala d'Orsu, before the diagnosis; as a boy he stood outside the Casanovas' house. The collars "
                    "are a precursor to a nerve control meant to save his own body first and then patch humanity. "
                    "The illness is no excuse.",
    "bedeutung": "Act 1 judges the trigger, Act 3 judges Alon. Totò's statements about the party night stay true; he "
                 "only lies about the device. No Act 1 clue becomes false through the betrayal.",
    "akt1_hinweise": "Only observations without a chain function: red light (z_01), Totò dodges (z_02), Megan's "
                     "hesitation (z_03), \"A.V.\" (z_05), Totò's money (z_06). Lola's gossip \"counts money at night\" "
                     "is only a signpost. Evidence in the propulsion room only from Act 2.",
    "fakten": ZW_FAKTEN,
    "routen": {},
    "megan_haltung": {
        "start": 0, "zufall": False, "kooperiert_ab": 1,
        "plus": [["vertrauen_megan_3", 1, "Vertrauen Megan mindestens 3"],
                 ["inspektion_offen", 1, "Duc shows Megan everything during the inspection, including what speaks "
                                         "against the crew"],
                 ["sturm_bestanden", 1, "The crew holds at least four storm posts on Day 5 (kern/sturm.py)"]],
        "minus": [["inspektion_beschoenigt", -1, "Duc holds something back during the inspection"],
                  ["anschuldigung_ohne_beleg", -1, "public accusation without evidence (against whoever)"],
                  ["drohung_presse", -1, "Duc threatens with the press or the clip"],
                  ["sturm_chaos", -1, "The crew loses at least three storm posts on Day 5 (kern/sturm.py)"]],
        "kooperiert": "In the hearing she lets Duc finish and listens to the plea to the end.",
        "druck": "In the hearing she loses patience faster (disc 3).",
    },
}

# ================================================================== WOCHENBOGEN
def S(sid, titel, art, kern, pflicht=True, exklusiv=False, personen=(), setzt=(), bed=None, fall=None, ort=None,
      wahl=None, event=None, uebergang=False):
    """uebergang=True (Modell B, 24.10.2026): kurzer Story-Moment vor der Phase - hat die Phase sonst keine
    Story-Szene, ist sie danach frei (kern/hauptstory.py, Vorspiel)."""
    s = {"id": sid, "titel": titel, "art": art, "pflicht": pflicht, "exklusiv": exklusiv, "kern": kern,
         "personen": list(personen), "setzt": list(setzt)}
    if uebergang:
        s["uebergang"] = True
    if bed:
        s["bedingung"] = bed
    if fall:
        s["fall"] = fall           # was aus dem gezogenen Fall eingesetzt wird
    if ort:
        s["ort"] = ort
    if wahl:
        s["wahl"] = wahl
    if event:
        s["event"] = event
    return s


WOCHENBOGEN = {
    # Akt 1 · Wer war's? (Duc 22.10.2026, Umbau Nacht 24.10.): Cold Open 06:35 -> Party als Rückblende -> Nachtfahrt
    # und Knall -> Strandung + Megans Ultimatum -> die Bucht -> Spuren -> Megan an Bord + Sturm -> letzte Spuren +
    # Lagerfeuer -> Anhörung + Cliffhanger. Der Ausfall liegt je Fall zwischen 06:11 und 06:35, der Knall immer 06:35.
    "1": {"titel": "One More Minute of Light", "kommando": "holm", "nur_story": True, "phasen": {
        # Tag 0 (24.10.2026): Cold Open am Morgen, danach "The day before" - die Begegnungen im Hangar von Antibes
        # laufen als Prolog-Events in der Tag-Phase (ereignisse_tag0.py), Ueberfahrt ohne freie Zeit, abends die Party.
        "fruehstueck": [S("cold_open", "06:35", "fix", exklusiv=True, ort="power_room", personen=["rosi"],
                          kern="Cold open without explanation: 06:35, a bang in the propulsion room, smoke, sparks, "
                               "Rosi's hand on the emergency stop. One breath, then black screen: \"The day before. "
                               "Antibes.\" Nobody is recognised, nothing is explained, no guilt is hinted at.",
                          setzt=["cold_open_gesehen"])],
        "abend": [S("auftakt_party", "One More Minute of Light", "fix", exklusiv=True, ort="aft_deck",
                    personen=["chiara", "rosi", "siri", "lea", "sophia", "holm", "toto", "lola", "yasin", "maxwell"],
                    kern="Party in the evening light, no cast list - and the first scene of the crime: what Duc sees "
                         "here counts later as an observation. First: who do you help? Then moments: Lea claims the "
                         "sea might glow tonight; Rosi calls Unit-01 the only guest who brings its own power; Sophia "
                         "quietly separates Lea and Rosi; Holm has stomach pain and waves it off; Maxwell does a "
                         "push-up for every joke; Chiara has an unused place cleared away (an image, don't explain). "
                         "Group photo at 21:32 - Duc may be missing from it.",
                    wahl={"frage": "Who do you help first?",
                          "optionen": {"chiara": "Chiara is a pair of hands short at the service",
                                       "rosi": "Rosi needs someone for a test in the control room",
                                       "siri": "Siri would like a short break from a shoot"},
                          "folgen": "Flag auftakt_hilfe_<id>, trust +2; the person remembers it specifically. No "
                                    "hidden guilt, no option prevents a deed."},
                    setzt=["auftakt_gesehen"], fall="Auftakt-Erinnerung je Hilfe (fall.auftakt)")],
        "nacht": [S("blackout", "The Silence", "fix", exklusiv=True, ort="galley", personen=["lola"],
                    kern="Afterparty until half past three; Duc can't sleep and sits with Lola in the galley, who is "
                         "baking for the sunrise breakfast. First the music stops. Then Lola says \"Duc?\". Only then "
                         "the alarm. Don't name a time - exactly when it went quiet differs from case to case.",
                    setzt=["blackout"]),
                  S("explosion", "06:35", "fix", ort="power_room",
                    personen=["maxwell", "toto", "lea", "rosi", "holm", "sophia", "lola"],
                    kern="Totò and Lea run to the propulsion room after the alarm. At 06:35 (the same in every case) "
                         "the inverter goes bang. Maxwell catches the debris with his back and saves Totò and Lea - "
                         "just a scratch, he turns it into a pose. Sophia's charm drops when Lea is lying under the "
                         "debris. Rosi runs in, hits the emergency stop and then sits still in front of the inverter "
                         "for longer than ten seconds (only Duc sees it). Unit-01 keeps running. Everyone says "
                         "\"motor\", Rosi corrects them: \"It's not a motor. It's an inverter.\" Totò stares briefly at "
                         "something behind the inverter and turns grey - don't explain. Holm asks whether everyone "
                         "is okay, looks after Lola and then collapses herself.",
                    setzt=["explosion"]),
                  S("wache_mit_holm", "Who Do You Call?", "fix", ort="bridge", personen=["holm"],
                    kern="Holm has dragged herself to the bridge and won't be relieved. The yacht drifts until she "
                         "lies at anchor off Cala d'Orsu at 07:50. Holm, pale with pain, doesn't ask for his heroic "
                         "biography but: \"Who do you call when you don't know what to do next?\" The answer comes "
                         "back (farewell). At the end she mentions that her logbook and the log show different times.",
                    wahl={"frage": "Who do you call when you don't know what to do next?",
                          "optionen": {"holm": "Dich.", "crew": "Meine Leute hier an Bord.",
                                       "niemand": "Nobody. I'll do it myself.",
                                       "frankfurt": "Jemanden in Frankfurt."},
                          "folgen": "antwort_wache = <id>"},
                    setzt=["uhrzeit_widerspruch_gehoert"])]}},
    "2": {"titel": "Stranded", "kommando": "holm", "kommando_wechsel": "fruehstueck", "phasen": {
        "fruehstueck": [S("lage_mit_holm", "Briefing", "fix", ort="bridge",
                          personen=["holm", "rosi", "chiara", "sophia"],
                          kern="Holm leads one last time and doesn't quite take Duc seriously yet. Rosi explains the "
                               "concrete constraint (inverter destroyed, hotel load in island mode, emergency supply "
                               "independent, Unit-01 running), Chiara the people's needs, Sophia the company's "
                               "message. Duc decides on a noticeable cut in comfort - a later scene shows the "
                               "reaction.",
                          wahl={"frage": "Worauf verzichtet ihr zuerst?",
                                "optionen": {"dusche": "kalte Duschen", "kuehlung": "half cooling",
                                             "aufnahme": "Yasins Aufnahmen bleiben aus"},
                                "folgen": "Flag komfort_<id>; an image of it in the evening or on day 3"}),
                        S("megan_erster_anruf", "Megan's Ultimatum", "anruf", personen=["megan", "holm"],
                          kern="Video conference on the bridge screen. Megan explodes like an anime boss: too loud, "
                               "too fast, a coffee cup flies out of frame: \"You were supposed to be my postcard!\" "
                               "(the Eden Bay Weekend has fallen through). Then, ice-cold, the ultimatum: in seven "
                               "days a cause report and a hearing on board, and she will judge. Without someone to "
                               "blame the whole crew is out. Holm pushes back as well as she still can.",
                          setzt=["megan_ultimatum"], fall="z_04"),
                        S("holm_ansprechbar", "Holm Has a Moment", "wahl", pflicht=False, personen=["holm"],
                          kern="Before the helicopter comes, Holm has a moment. Whoever asks precisely gets precise "
                               "answers (fall.holm_tag1). After that only by phone.",
                          fall="holm_tag1"),
                        S("holm_abschied", "Farewell to the Captain", "fix", ort="sun_deck", personen=["holm"],
                          kern="Holm is evacuated by rescue helicopter (appendix) - a medical matter, not a clue. "
                               "She hands Duc service card 1 and the command and picks up his answer from the night. "
                               "Petru stands on the quay and watches the helicopter go.",
                          setzt=["holm_evakuiert", "kommando_duc"]),
                        S("der_freie_platz", "The Empty Seat", "fix", ort="crew_mess", personen=["chiara"],
                          kern="After take-off there are too many cups on the table. Chiara wants to take one away. "
                               "A small character choice, not a moral test.",
                          wahl={"optionen": {"stehen": "Leave it.", "selbst": "Clear it away yourself",
                                             "lage": "Gleich zur Lage"}})],
        "tag": [S("erste_ermittlung", "What Happened in the Night", "fix",
                  kern="Three ways, one of them now: secure the event record of the power management system (it "
                       "doesn't answer the who yet), talk to one person about the night, or organise the supplies "
                       "first. A copy of the log is available later through the service access - but then it costs a "
                       "phase.",
                  wahl={"optionen": {"streifen": "Ereignisstreifen sichern", "gespraech": "Mit jemandem reden",
                                     "versorgung": "Versorgung organisieren"}},
                  fall="Ways from the groups streifen / befragen"),
                S("uhrzeiten_abgleichen", "Matching the Clocks", "aktion", pflicht=False,
                  kern="An explicitly offered action after Holm's hint from the night (way groups abgleich_*): the "
                       "photo, the logbook or the clock in the control room.", fall="r_12")],
        "abend": [S("widerspruch", "That Doesn't Fit the Timeline", "fix",
                    kern="In a conversation the first sentence comes up that contradicts another statement "
                         "(fall.widersprueche). The interface allows \"That doesn't fit the timeline\" without marking "
                         "anyone as guilty. Whoever accuses straight away meets resistance; whoever asks follow-up "
                         "questions gets a new, checkable detail.", fall="widersprueche")]}},
    "3": {"titel": "The Bay", "kommando": "duc", "phasen": {
        "fruehstueck": [S("etwas_anders", "Something Is Different", "fix", pflicht=False, uebergang=True,
                          kern="Only if a counteraction happened during the night: something already examined has "
                               "changed (a page missing, a measurement replaced, an access note, a list on the "
                               "board). Today the concrete event can be checked.", fall="gegenhandlungen.spur"),
                        S("sonnenaufgang", "Sunrise over Cala d'Orsu", "fix", ort="foredeck", uebergang=True,
                          kern="Make the player fall in love with the bay: the first quiet morning. Light on the "
                               "water, fishing boats, bells from the village, Kevin the seagull on the railing. No "
                               "problem, no investigation - a still moment, alone or with the person closest to Duc.")],
        "tag": [S("landgang", "Cala d'Orsu", "fix", ort="village_harbour",
                  personen=["alva", "elsa", "petru", "casanova"],
                  kern="The village opens up - people know Duc from the harbour fight yesterday. Alva knows the "
                       "supply routes. Elsa wants a factual status report. Petru wants to know exactly what has "
                       "already been checked. Casanova sits at the harbour, promises help and is already planning "
                       "the yacht as a backdrop for the festa at the end of the summer - an oversized presentation "
                       "that Elsa ends by asking about the permitted number of people. Two of three plans: one now, "
                       "one in the evening.",
                  wahl={"vorhaben": {"material": "Material organisieren (Alva, Petru)",
                                     "spur": "Check a lead ashore (case: ways ashore)",
                                     "versprechen": "Keep a personal promise"},
                        "regel": "The missed plan isn't lost, but later it needs help or another way in."},
                  setzt=["alva_kennengelernt", "elsa_kennengelernt", "petru_kennengelernt"])],
        "dinner": [S("landgang_2", "The Second Plan", "wahl", pflicht=False, kern="The second of the three plans.")],
        "abend": [S("gemeinsames_essen", "Lola's First Meal in the Bay", "fix", ort="aft_deck",
                    personen=["lola", "lea", "rosi"],
                    kern="For the first time Lola cooks with what the village has to offer - and it's the best meal "
                         "in days. Candles because of the power, a view of the bay. Someone laughs for the first "
                         "time since the silence. Whoever says publicly here \"We don't know yet\" sets "
                         "oeffentlich_noch_offen.")],
        "nacht": [S("naehe", "A Safe Room", "naehe", pflicht=False,
                    kern="A person Duc trusts sits with him in a safe room. Sexual escalation is welcome (Lola "
                         "stoned: very horny and filthy). It ends with conversation, touch, a kiss or falling asleep "
                         "together; the character decides too; a no leaves the relationship intact. Dialogue core: "
                         "\"Tomorrow you'll ask me about that night again.\" - Yes / Only if you want to talk / evade. "
                         "Lola's invitation (side arc) may fill this slot.",
                    wahl={"optionen": {"ja": "Ja.", "nur_wenn": "Only if you want to talk.", "ausweichen": "…"}}),
                  S("nachtende", "Just Before Dawn", "nachricht", pflicht=False,
                    kern="A concrete message confirms or refutes an alibi (fall.nachtende). If Duc already knows, "
                         "then - if the conditions are right - the invitation to a voluntary confession comes "
                         "instead. No redundant surprise.", fall="nachtende")]}},
    "4": {"titel": "Traces", "kommando": "duc", "phasen": {
        "abend": [S("reparaturschritt", "Rosi vs. Officer", "fix", ort="power_room", personen=["rosi"],
                    kern="The whiteboard \"Rosi vs. Officer\" in the propulsion room: securing emergency power and the "
                         "propulsion room, the first step of the repair in Act 1. A step succeeds or fails based on "
                         "the work so far (material from the village helps). The person responsible can contribute "
                         "decisively without becoming retroactively innocent."),
                  S("megan_ankuendigung", "I'm Coming Tomorrow", "anruf", personen=["megan"], uebergang=True,
                    kern="Megan calls, calmer than on the first day and therefore scarier: tomorrow she'll come "
                         "aboard herself and stay until the hearing. She wants to see the ship, not read reports.",
                    setzt=["megan_angekuendigt"])]}},
    "5": {"titel": "Pressure in Person", "kommando": "duc", "phasen": {
        "fruehstueck": [S("megan_kommt", "A Visit from Head Office", "fix", personen=["megan"],
                          kern="At the end of breakfast the main story sets megan_besuch. The landing itself is "
                               "played by the event g1_helikopter (day phase, mandatory).",
                          setzt=["megan_besuch"])],
        "tag": [S("megan_inspektion", "The Inspection", "fix", ort="power_room", personen=["megan", "rosi"],
                  event="g1_helikopter",
                  kern="Megan walks the ship. She studied navigation and naval architecture and can see from the "
                       "damage that overload alone isn't enough - she doesn't say so. Duc decides whether he shows "
                       "her everything, including what speaks against the crew (zweite_wahrheit.megan_haltung).",
                  wahl={"optionen": {"offen": "Alles zeigen", "beschoenigt": "Hold something back"},
                        "folgen": "Flag inspektion_offen / inspektion_beschoenigt"})],
        "dinner": [S("sturmvorbereitung", "Before the Storm", "fix",
                     kern="In the evening a storm comes. Clear division of work: lines and anchor, saving power, "
                          "securing the galley, securing the tender, checking the makeshift fix. Duc can't go with "
                          "every person; those he sends out do traceable tasks and report with what they actually "
                          "know. Megan watches and takes notes.",
                     setzt=["sturm_vorbereitet"])],
        "abend": [S("leises_telefonat", "A Quiet Phone Call", "fix", ort="sun_deck", personen=["megan"], uebergang=True,
                    kern="Foreshadowing: Duc hears Megan quietly on the phone on deck; she says \"A.V.\" twice and "
                         "something about \"the buyer from Monaco\". She notices him, hangs up and becomes the boss "
                         "again. Don't explain who A.V. is; Megan herself doesn't know what she is working for.", fall="z_05")],
        "nacht": [S("sturmnacht", "What You Hear in the Dark", "fix", exklusiv=True,
                    kern="Storm: the power drops hard. An unchecked makeshift fix fails (a consequence, not a "
                         "punishment roll); a prepared procedure prevents it and is played as teamwork. Megan sees "
                         "the crew at work for the first time.")]}},
    "6": {"titel": "Last Traces", "kommando": "duc", "phasen": {
        "abend": [S("lagerfeuer", "Bonfire on the Beach", "fix", ort="swim_platform",
                    personen=["lola", "lea", "rosi", "maxwell", "toto"],
                    kern="Mandatory breather after the storm: a fire on the little beach next to the yacht, Lola "
                         "grills, Maxwell tells a story in the third person, Totò takes bets on who falls asleep "
                         "first. The hearing is tomorrow - tonight nobody talks about it, until someone does.")],
        "nacht": [S("letzte_naehe", "An Evening of Your Choosing", "naehe", pflicht=False,
                    kern="A shared evening, deliberately chosen, before the hearing. A love scene is possible, not a "
                         "mandatory climax and no reward for a cover-up. The decisive statement can come afterwards "
                         "or in an equivalent friendship scene: a promise the person wants to keep themselves.")]}},
    "7": {"titel": "The Hearing", "kommando": "duc", "phasen": {
        "tag": [S("anhoerung", "The Hearing", "fix", exklusiv=True, ort="main_salon", personen=["megan"],
                  kern="Megan judges in the salon. Sequence: accusation -> two witnesses -> objection with evidence "
                       "-> truth -> Duc's own role -> plea -> verdict (story anhoerung, kern/anhoerung.py). The "
                       "hearing always takes place, even empty-handed. Here: accusation, witnesses, objections.",
                  setzt=["anhoerung_gehalten"], fall="kette, gestaendnis, zeugen"),
                S("anhoerung_rolle", "And You, First Officer?", "fix", ort="main_salon", personen=["megan"],
                  kern="Duc's own role in the night: honest or kept quiet (counts towards mercy).",
                  fall="gestaendnis.duc_eigene_rolle"),
                S("anhoerung_urteil", "The Verdict", "fix", ort="main_salon", personen=["megan"],
                  kern="Plea (ask for mercy / share the blame / demand punishment) and verdict. Megan hesitates over "
                       "the engine report: \"A PX-480 doesn't just burn.\" Her gut feeling makes mercy possible if the "
                       "code allows it.")],
        "abend": [S("nach_dem_urteil", "After the Verdict", "fix", ort="crew_mess", personen=["megan"],
                    kern="The crew after the verdict. Megan flies out; from now on only by phone again. Whoever was "
                         "wrongly suspected is waiting for a word from Duc. The outcome of the hearing colours the "
                         "room but explains nothing new.",
                    setzt=["megan_abgereist"])],
        "nacht": [S("cliffhanger", "Red Light in the Mountains", "fix", exklusiv=True, ort="foredeck",
                    kern="Night, everyone is asleep. High in the mountains above the bay a red light is blinking, in "
                         "the same rhythm as the one behind the inverter. Then a howl from the macchia, not a dog. "
                         "Black screen: end of Act 1. Don't explain.",
                    setzt=["akt1_ende"])]}},
}

BESUCHE = {
    "holm": {"an_bord_bis": "T2 fruehstueck", "flag_weg": "holm_evakuiert", "telefon_ab": "T2 abend", "persoenlich_bis": "T2 fruehstueck",
             "regel": "Holm is on board on the party day (day 1) and the morning after (in command) and is evacuated "
                      "at the end of breakfast on day 2. What she knows in each case is in fall.holm_tag1; after "
                      "that she can be reached by phone from the hospital."},
    "megan": {"modus": "Phone and video conference", "einmaliger_besuch": True, "angekuendigt": "T4 abend",
              "flag": "megan_besuch", "an_bord_von": "T5 tag", "an_bord_bis": "T7 abend", "abflug": "T7 abend",
              "ankunft_event": "g1_helikopter",
              "regel": "Exactly once, by helicopter; she stays until the hearing (as judge) and flies out after the "
                       "verdict. The main story sets the flag, no event sets it itself."},
}

NEBENBOEGEN = {
    "regeln": {
        "konkurriert_nicht": "Lola's and Alva's personal stories take no main scene's place and cost no phase (an "
                             "interlude after the phase).",
        "zustellung": "Invitation or call by phone.",
        "keine_zeit": "As in BG3: \"Not right now\" postpones the scene; the invitation comes back on the next "
                      "suitable evening. No loss of trust for postponing.",
        "nie_in_exklusiv": True,
        "tratsch": "Lola's gossip (on board) and Alva's gossip (ashore) only show where to look - never evidence on "
                   "their own.",
    },
    "lola": {"rolle": "on board: galley, morale, ship's gossip", "freischaltung_tag": 3,
             "events": ["ab_lola_klopft", "ab_lola_handy"], "darf_fuellen": ["T3 nacht naehe"]},
    "alva": {"rolle": "ashore: bar, supply routes, village gossip; all shore roles from the dossier", "freischaltung_tag": 4,
             "events": ["ab_alva_barabend", "ab_alva_handy"], "darf_fuellen": []},
}

# Anhoerung (Duc 22.10., alle 5 Team-Verbesserungen): Daten hier, Logik kern/anhoerung.py (Scheibe 3)
ANHOERUNG = {
    "tag": 7, "phase": "tag", "ort": "main_salon", "richterin": "megan",
    "ablauf": ["anklage", "zeugen", "einspruch", "wahrheit", "ducs_rolle", "plaedoyer", "urteil"],
    "geduld": {"adern": 3, "regel": "Only guessing costs a vein (evidence that fits nothing; an accusation without "
                                    "proof). Any logically fitting evidence counts, no matter how Duc found it."},
    "zeugen": {"anzahl": 2, "regel": "Earned beforehand (trust, statements). Witnesses have their own loyalties and "
                                     "can lie to protect someone; an objection with evidence exposes the lie."},
    "plaedoyer": {"gnade": "Gnade erbitten", "teilen": "Schuld teilen", "strafe": "Strafe fordern",
                  "erbarmen_wenn": ["richtige Person", "volle Kette", "Motiv bekannt", "Duc honest about his own role"]},
    "loyal": {"lea": ["sophia"], "sophia": ["lea"], "chiara": ["holm"], "rosi": ["lola"], "yasin": ["siri"]},
    "entschuldigung": "People who were wrongly suspected are offered an apology after the verdict.",
    "immer": "The hearing always takes place, even empty-handed; then Megan judges on her own (dismissal as a "
             "roguelike consequence, not game over).",
    "zoegern": "Megan hesitates over the engine report: \"A PX-480 doesn't just burn.\" (gut feeling -> mercy)",
}

ENDE = {
    "akt": 1,
    "titel": "Ende von Akt 1",
    "absaetze": ["The Hearing", "Die Crew", "Was bleibt"],
    "regel": "No overall ending: Act 1 closes with the verdict, the state of the crew and the cliffhanger. Endings "
             "for the women, the bay and the epilogues only come at the end of Act 3.",
}

REGELN = {
    "fall_wahl": "Drawn evenly from 1-5 before the opening, stored internally as a number, never in plain text in "
                 "logs or output. No choosing afterwards. Player actions change what Duc finds out, not the cause.",
    "verhindern": "The triggers lie outside Duc's options (no opening option prevents a deed).",
    "fakten": "Every important fact has content, time, source, reliability, who knows it and how it was passed on. "
              "Inner monologue is never another character's knowledge.",
    "angst": "The hidden fear of discovery only rises when the person learns about the investigation (ways with "
             "auffaellig=true, conversations, rumours). Searching in secret changes nothing.",
    "gegenhandlungen": "At most one per day. Each leaves a trace and has a way around it. No complete loss of "
                       "evidence without an alternative way.",
    "anklage": "Confrontation only with a proven chain (one piece of evidence per link). Public accusations are "
               "possible but never marked as the truth while unproven. A public false accusation needs a public "
               "correction.",
    "codex": "Short, factual entries, split into log, statement and \"Your suspicion\". The character list gives "
             "nothing away through sorting or missing options (all suspects have the same options).",
    "intim": "No central clue exclusively behind sex. A gift or a sex scene heals no breach of trust. A love scene "
             "is no reward for a cover-up. Erotic privacy only becomes a rumour through an established witness or a "
             "voluntary disclosure.",
    "sprachmodell": "The model shapes dialogue and atmosphere within the facts. It invents no deed, no exclusive "
                    "piece of evidence, no secret surveillance and no choosing the culprit afterwards. Characters "
                    "only know what is in wissende/uebermittlung. New claims are claims and are checked against the "
                    "facts.",
    "notversorgung": "Radio, emergency beacon, anchor light and bilge pumps are never part of a trade.",
    "spoiler": "Cases are only called case 1-5; fact IDs are neutral; check and build output only names numbers.",
}

PRUEFFAELLE = [
    "früh richtige Vermutung ohne Belege", "spätes vollständiges Ermitteln", "keine Romanze",
    "Romanze mit der verantwortlichen Person", "Romanze mit einer Unschuldigen",
    "öffentlich falsche Anschuldigung mit Korrektur", "öffentlich falsche Anschuldigung ohne Korrektur",
    "verweigerte Intimität", "fehlender Einzelhinweis", "frühes freiwilliges Geständnis", "Megan kooperiert",
    "Megan übt Druck aus", "Anhörung mit leeren Händen", "Anhörung mit lügendem Zeugen", "Erbarmen erreicht",
]

# Wer schickt kurz vor Morgen (Tag 3) die Nachricht, und welche Fakten kann sie liefern (erster unbekannter zuerst)
NACHTENDE = {1: ("toto", ["f1_09", "f1_10"]), 2: ("petru", ["f2_06"]), 3: ("alva", ["f3_08", "f3_07"]),
             4: ("toto", ["f4_08", "f4_07"]), 5: ("toto", ["f5_08"]), 6: ("chiara", ["h_16"])}


# ================================================================== Bau
def fall_bauen(fall):
    n = fall["nr"]
    ersatz = {"@ausfall": "f%d_01" % n, "@logbuch": "f%d_02" % n}
    fakten = []
    for f in story_faelle.RAHMEN:
        f = copy.deepcopy(f)
        for w in f["wege"]:
            if "braucht" in w:
                w["braucht"] = [ersatz.get(b, b) for b in w["braucht"]]
        fakten.append(f)
    fakten += [copy.deepcopy(h) for h in story_faelle.HARMLOS if n not in h["nicht_in"]]
    fakten += copy.deepcopy(fall["fakten"])
    absender, liste = NACHTENDE[n]
    nach_id = {f["id"]: f for f in fakten}
    for fid in liste:
        f = nach_id[fid]
        w = W("handy", "A message just before dawn", person=absender, tage=(3, 3), phasen=["nacht"],
              auffaellig=False, g="nachtende")
        w["id"] = "%s_w%d" % (fid, len(f["wege"]) + 1)
        f["wege"].append(w)
    for f in fakten:
        f.pop("nicht_in", None)
    out = {k: v for k, v in fall.items() if k != "fakten"}
    out["zeitleiste"] = sorted(fall["zeitleiste"], key=lambda z: minuten(z["zeit"]))
    out["tipps"] = list(fall["tipps"]) + [copy.deepcopy(ZW_TIPP)]
    out["fakten"] = fakten
    out["nachtende"] = {"absender": absender, "fakten": liste,
                        "sonst": "Invitation to a voluntary confession, if fall.gestaendnis.freiwillig applies"}
    out["glieder"] = [{"id": g["id"], "frage": GLIEDER[g["id"]], "beweis_saetze": g["beweis_saetze"]}
                      for g in fall["kette"]]
    out.pop("kette")
    kern_vergeben(out)
    return out


# Garantierte Kernbeweise (Duc 28.10.2026, Anhoerung Option A): What und Why bekommt jeder Fall ueber einen
# Pflicht-Moment der Woche, Who bleibt Ermittlung (sonst stuende der Taeter ohne Ermittlung fest). Kern = der
# kleinste Beweissatz des Glieds, bei Gleichstand der, dessen Notizen am besten zur Quelle passen (Rosis Whiteboard:
# Bordsysteme; Megans Mappe: Papiere). Die Engine liefert ihn nur, solange das Glied noch nicht belegt ist.
PFLICHT = {"handlung": ("reparaturschritt", 4, "On Rosi's whiteboard in the propulsion room", "systems"),
           "folge": ("megan_kommt", 5, "In the folder Megan brought from head office", "papers")}


def _quelle_art(f):
    q = f.get("quelle") or ""
    if q == "duc" or f.get("art") == "abgeleitet":
        return "own"
    if q in ("holm_logbuch", "maschinenbuch", "bordhandbuch", "notizbuch", "wettbuch", "reservierungsbuch",
             "dokumentenmappe", "herstellerunterlagen", "eden_hq", "aushang", "telefon"):
        return "papers"
    if q in VERDAECHTIGE or q in ("holm", "rosi", "toto", "petru", "alva", "lola", "megan", "elsa", "siri", "maxwell"):
        return "people"
    return "systems"


def kern_vergeben(fall):
    nach_id = {f["id"]: f for f in fall["fakten"]}
    for g in fall["glieder"]:
        if g["id"] not in PFLICHT:
            continue
        szene, tag, text, passt = PFLICHT[g["id"]]
        saetze = [s for s in g["beweis_saetze"] if all(x in nach_id for x in s)]
        kern = min(saetze, key=lambda s: (len(s), sum(_quelle_art(nach_id[x]) != passt for x in s)))
        g["kern"] = g["beweis_saetze"].index(kern)
        for fid in kern:
            f = nach_id[fid]
            if any(w["art"] == "pflicht" for w in f["wege"]):
                continue
            w = W("pflicht", text, tage=(tag, 7), auffaellig=False, g="pflicht:" + szene)
            w.update(id="%s_w%d" % (fid, len(f["wege"]) + 1), szene=szene, glied=g["id"])
            f["wege"].append(w)


def bauen():
    faelle = [fall_bauen(f) for f in story_faelle.FAELLE]
    daten = {
        "_hinweis": "CONFIDENTIAL - contains the solution. Built from werkzeuge\\eden_rise\\story_*.py; change it "
                    "there, then run story_eden_rise.py and story_pruefen.py. Never edit by hand.",
        "stand": "2026-10-24", "phase": "A", "akt": 1, "sturm_tag": 5,
        "regeln": REGELN,
        "zeit": {"referenz": "Schiffszeit", "pms_versatz_min": PMS_VERSATZ_MIN, "ausfall_fenster": list(AUSFALL_FENSTER),
                 "format": "T<day> HH:MM (T1 = party day, the party night after midnight is T2)"},
        "zuverlaessigkeit": ZUVERLAESSIG,
        "weg_arten": WEG_ARTEN,
        "glieder": GLIEDER,
        "verdaechtige": VERDAECHTIGE,
        "schaltplan": SCHALTPLAN,
        "zweite_wahrheit": ZWEITE_WAHRHEIT,
        "faelle": faelle,
        "wochenbogen": WOCHENBOGEN,
        "besuche": BESUCHE,
        "nebenboegen": NEBENBOEGEN,
        "anhoerung": ANHOERUNG,
        "ende": ENDE,
        "prueffaelle": PRUEFFAELLE,
    }
    os.makedirs(os.path.dirname(ZIEL), exist_ok=True)
    json.dump(daten, open(ZIEL, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    fakten = sum(len(f["fakten"]) for f in faelle)
    wege = sum(len(x["wege"]) for f in faelle for x in f["fakten"])
    szenen = sum(len(v) for t in WOCHENBOGEN.values() for v in t["phasen"].values())
    print("story.json written: %d cases, %d facts (per case %s), %d ways, %d scenes in the week arc, %d facts of the "
          "second truth" % (len(faelle), fakten, "/".join(str(len(f["fakten"])) for f in faelle), wege,
                                         szenen, len(ZW_FAKTEN)))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    bauen()
