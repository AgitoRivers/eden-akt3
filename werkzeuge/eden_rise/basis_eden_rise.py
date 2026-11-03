# -*- coding: utf-8 -*-
r"""Grundgeruest fuer eden_rise: Welt, Raeume, Personen, Persona, Gesten, Kabine, Laden-Grundgeruest, Job-Zeilen.
Schreibt selbst nichts - modul_eden_rise.py liest MODUL/R/PERSONA_BERATER und baut daraus module\eden_rise\modul.json.

Herkunft (18.10.2026): Kopie von modul_gestrandet.py, als Gestrandet ins Archiv ging (archiv\werkzeuge\). Was nur
Gestrandet betraf (Uhren, Storylets, Wahrheit), ueberschreibt modul_eden_rise.py; Aufraeumen ist ein eigener Schritt.

Entscheidungen von damals (Duc hat sie Claude ueberlassen, 13.10.2026): natuerlich und mit spuerbarer Progression.
- Plot-Druck kommt aus drei Uhren (Reparatur / Rettung / Katastrophe), Alltagsdruck aus Strom & Diesel.
- Jede Frau hat einen Bogen in drei Stufen; die naechste Stufe oeffnet sich erst mit genug Vertrauen
  (Storylets mit Bedingung). Naehe entsteht Schritt fuer Schritt, nie auf Knopfdruck.
- Spielerfigur: Ducs echte Persona (ESG-Berater im Sabbatical, Handwerk und Kueche). Weitere Personas = spaetere Freischaltung.
"""
FRAUEN = ["chiara", "sophia", "lea", "rosi", "siri"]

MODUL = {
    "_hinweis": "Hauptplot Eden Rise: Gestrandet (13.10.2026). Durchlauf 1 = Hafenstaedtchen Cala d'Orsu. "
                "Gebaut aus werkzeuge\\modul_gestrandet.py - dort aendern, nicht hier.",
    "id": "eden_yacht_gestrandet",
    "titel": "Eden Rise – Gestrandet",
    "untertitel": "Sieben Tage gestrandet vor Korsika. Bis Sonntag muss sie in Calvi sein.",
    "titelbild": "yacht_solar_deck.png",
    "ort_des_durchlaufs": "hafenstaedtchen",
    "karten_ordner": r"X:\AI\RoleplayGen\cards\Eden Yacht",
    "attribute": ["charm", "empathy", "perception", "cunning", "courage", "strength"],
    "zeitraster": {"tage": 7, "phasen": ["fruehstueck", "tag", "dinner", "abend", "nacht"],
                   # Dinner ist seit 17.10.2026 eine Wahl (an Bord, an Land, zu zweit) - weniger Essen in der Messe
                   "pflicht": ["fruehstueck", "nacht"], "wahl": ["tag", "dinner", "abend"]},
    "start_flags": ["gestrandet"],
    "start_inventar": [],
}

MODUL["welt"] = (
    "M/Y Eden Rise, a 62-metre solar-powered superyacht owned by the Eden Group: a hardtop of solar panels, battery "
    "banks, silent electric drive, and one diesel emergency generator the ETO calls Unit-01. On a night passage to "
    "Calvi the electric drive died: inverter three burnt out. The boat drifted into the bay of Cala d'Orsu, a fishing "
    "village of three hundred people on the west coast of Corsica, and lies at anchor out in the bay - the fishing "
    "harbour is far too shallow for her, so there is no shore power and no fuel dock; the shore is a tender ride away. "
    "Everything aboard runs on the batteries: anchor light and anchor alarm, bilge pumps, the cold rooms with food for "
    "thirteen people, the watermaker (the only fresh water), the toilets, the radio. The sun refills about a third on a "
    "clear day; without saving, the batteries are empty in a day and a half. Diesel for Unit-01 is scarce. "
    "Captain Marit Holm was flown out by helicopter with appendicitis; Duc, the First Officer, has command. "
    "The Eden Group's ultimatum: the Eden Rise must be at the shipyard in Calvi in seven days. Under her own power it is "
    "a repair. If not, the Group sends a tug from Ajaccio - eighty thousand euros, taken from the crew's season bonus. "
    "Two charter guests are still aboard, influencer Siri Lindvik and her boyfriend Yasin Benali, because the next ferry "
    "from the village is in a week.")

MODUL["ziel"] = "Bis Tag 7 in Calvi – aus eigener Kraft oder am Haken (80.000 € von der Crew-Prämie)."
MODUL["prolog"] = [
    "Last night, halfway to Calvi, the Eden Rise went dark. A smell of burnt plastic from the power room, then silence: "
    "no drive, half the lights gone. She drifted for hours and came to rest in the bay of Cala d'Orsu, a fishing "
    "village on the west coast of Corsica.",
    "The harbour is too shallow for a 62-metre yacht, so she lies at anchor out in the bay. No shore power. No fuel dock. "
    "Everything aboard - the anchor alarm, the bilge pumps, the cold rooms, the fresh water - runs on the batteries. "
    "They stand at forty percent. Without saving, that is a day and a half.",
    "At dawn Captain Holm collapsed. Appendicitis. The rescue helicopter is on its way, and with her gone, the "
    "command is yours. Before they strapped her to the stretcher, she pressed her old brass compass into your hand.",
    "Then the Eden Group called. Seven days. By Sunday the Eden Rise must be at the shipyard in Calvi. If she gets "
    "there under her own power, it is a repair. If not, a tug from Ajaccio tows her there - eighty thousand euros, "
    "paid out of the crew's season bonus.",
    "Thirteen people. Seven days. One First Officer.",
]

# Ducs Spielfigur (17.10.2026, Duc): ESG-Berater mit Handwerksgeschick - nie "Tueftler". Vier Staerken gleich verteilt:
# Koepfchen (Perception 3), Charme (Charm 3), Handwerk und Kueche (je ein Vorteil). Alte Spielstaende tragen noch die
# id "tueftler" in ihrer eigenen Persona-Kopie; handel.py behandelt sie wie "handwerk".
PERSONA_BERATER = {
    "id": "berater",
    "rolle": "first_officer",
    "titel": "The ESG consultant on sabbatical",
    "oeffentlich": "the new First Officer, aboard since Antibes",
    "vorgeschichte": "An ESG consultant from Frankfurt, 33, on a sabbatical: one season at sea as First Officer, "
                     "Yachtmaster for years. He reads a balance sheet as well as he reads a room, and years of client "
                     "meetings taught him to win one. He is good with his hands and would rather fix a thing than "
                     "replace it. In the galley he cooks European and Southeast Asian home cooking, from bun rieu to "
                     "bouillabaisse. He thinks in plans, plan B and plan C.",
    "geheimnis": "A management position at European level is waiting for his answer by the end of this week. It means "
                 "pressure, an office, no sea. Everyone aboard thinks he is staying at sea.",
    "attribute": {"charm": 3, "empathy": 2, "perception": 3, "cunning": 2, "courage": 2, "strength": 2},
    "vorteile": ["handwerk", "kueche", "koepfchen", "charme"],
    "vorteil": "Craft and kitchen: advantage on every repair and building check, and on every cooking check. Head and charm show in a fight: he spots weak points for free and talks with advantage.",
    "schwaeche": "Plan for everything: when something goes off-plan he wants to solve it alone. Accepting help is his growth.",
    "start_items": ["multitool", "holm_compass"],
}
MODUL["personas"] = [PERSONA_BERATER]

MODUL["werte"] = {
    # Labels Englisch seit 28.10.2026 (Duc: alles Spieler-Sichtbare Englisch); "Trust Chiara" entsteht in zustand.wert_label
    "vertrauen": {"label": "Trust", "bereich": [0, 5], "je": FRAUEN,
                  "start": {"chiara": 1, "sophia": 1, "lea": 2, "rosi": 1, "siri": 1}},
    "begehren": {"label": "Desire", "bereich": [0, 5], "je": FRAUEN,
                 "start": {"chiara": 1, "sophia": 2, "lea": 2, "rosi": 1, "siri": 1}},
    "rivalitaet": {"label": "Tension", "bereich": [0, 5], "paare": ["chiara_siri", "rosi_siri", "chiara_sophia"],
                 "start": {"chiara_siri": 2, "rosi_siri": 2, "chiara_sophia": 1}},
    "draht": {"label": "Trust Totò", "bereich": [0, 5], "start": 1},
    "moral": {"label": "Crew Mood", "bereich": [0, 5], "start": 3},
    "ruf": {"label": "Village Reputation", "bereich": [0, 5], "start": 1},
    "energie": {"label": "Energy", "bereich": [0, 3], "start": 3},
}

MODUL["uhren"] = {
    "reparatur": {"label": "Repairs", "segmente": 8, "voll": "The Eden Rise runs under her own power again."},
    "rettung": {"label": "Rescue", "segmente": 6, "voll": "A tug from Ajaccio is on its way."},
    "katastrophe": {"label": "Disaster", "segmente": 6, "verdeckt": True, "voll": "The battery bank is on fire."},
    "siri_marke": {"label": "Siri pulls away", "segmente": 6, "voll": "Siri breaks up with Yasin."},
    "yasin_video": {"label": "Yasin's video", "segmente": 5, "verdeckt": True,
                    "voll": "Yasin's video 'STRANDED ON A BILLIONAIRE YACHT' is online."},
}

MODUL["wahrheit"] = {"fest": None, "vorrat": {
    "defekt": {"kern": "A plain defect: an inverter module from a faulty production batch burned out. Nobody is to blame, and nobody believes that.",
               "enthuellung_ab_tag": 4, "verrat_woerter": ["faulty batch", "production batch", "recall"],
               "hinweise": ["scorched contacts on inverter three", "a serial number that doesn't match the logbook",
                            "Petru has read about a recall"]},
    "chiara": {"kern": "Chiara was practising on the bridge at night and bridged the battery protection to keep the chart plotter alive. It overloaded the drive.",
               "enthuellung_ab_tag": 4, "verrat_woerter": ["bridged the battery", "battery protection", "on the bridge that night"],
               "hinweise": ["the power log shows a load on the bridge at 02:10", "the 'ghost' was seen that night",
                            "Chiara avoids the bridge since the blackout"]},
    "lea": {"kern": "Lea secretly set a detour to her grandfather's Margot coordinates. The batteries were never meant for the extra miles.",
            "enthuellung_ab_tag": 4, "verrat_woerter": ["detour", "Margot coordinates", "changed the course"],
            "hinweise": ["the GPS track has a bend toward the Esterel", "Lea's logbook is wet and she won't open it",
                         "Lea asks too often how far the batteries reach"]},
    "sophia": {"kern": "Sophia arranged the stop in Cala d'Orsu as a favour for her publisher's research, and pushed the passage at night to make it. The batteries ran low too early.",
               "enthuellung_ab_tag": 4, "verrat_woerter": ["publisher", "favour for", "arranged the stop"],
               "hinweise": ["Alva greets Sophia by name", "a call from Paris that Sophia takes outside",
                            "the passage plan was changed by hand"]},
    "wette": {"kern": "Somebody from the engine room 'helped' the betting board along: a breaker pulled so the officer would be stuck with the crew. It went much further than intended.",
              "enthuellung_ab_tag": 4, "verrat_woerter": ["pulled the breaker", "for the bet", "helped the board"],
              "hinweise": ["a breaker labelled in Rosi's handwriting", "the betting odds changed the day before",
                           "an engineer won't look at Duc"]},
    "yasin": {"kern": "Yasin plugged a heavy charging rig for his camera gear into the guest socket. The short circuit took the drive with it, and he hid the burnt cable.",
              "enthuellung_ab_tag": 4, "verrat_woerter": ["charging rig", "burnt cable", "short circuit in the VIP"],
              "hinweise": ["a smell of burnt plastic in the VIP cabin", "Yasin lies about where his charger is",
                           "the guest circuit tripped first"]},
}}

MODUL["fixpunkte"] = [
    {"tag": 1, "phase": "fruehstueck", "titel": "Blackout", "beschreibung": "The morning after the blackout: Holm leaves by helicopter, Duc has command."},
    {"tag": 3, "phase": "nacht", "titel": "Storm night", "beschreibung": "A summer storm. Power runs low, the crew moves together, cabins are shared."},
    {"tag": 4, "phase": "fruehstueck", "titel": "Who did it?", "beschreibung": "The cause can be uncovered from today. A confrontation is offered: accuse someone, or stay silent."},
    {"tag": 5, "phase": "abend", "titel": "La Festa", "beschreibung": "The village festival. Who goes with Duc?"},
    {"tag": 6, "phase": "fruehstueck", "titel": "Point of no return", "beschreibung": "The last diesel for Unit-01 (repair) or the radio and the coast guard (rescue). Unresolved causes and low power can start a battery fire in the night."},
    {"tag": 7, "phase": "abend", "titel": "Last night", "beschreibung": "The clock that is full decides: repair, rescue or catastrophe. And who stands next to him."},
]

MODUL["geld"] = {"start": 200, "honorar": 300, "honorar_text": "Tagesgage Eden Group"}
MODUL["laeden"] = {
    "toto": {"name": "Totò's Locker", "wer": "toto", "sortiment": 8, "ankauf": 0.4,
             "text": "Ein abgeschlossener Spind im Lagerraum. Totò hat alles – fast. Preise je nach Draht zu ihm."},
    "dorf": {"name": "Dorfladen Cala d'Orsu", "nur_an_land": True,
             "text": "Bäcker, Eisenwaren, Tabak und ein Regal mit allem. Nur offen, wenn du heute an Land warst."},
}
# Yacht-Ware bei Toto entfernt (Duc 29.10.2026, Brain Trust): die eine Hehlerei-Entscheidung ist das Bordrat-Event
# br_crew_kasse (ereignisse_bordrat.py), nicht ein Knopf im Laden.
MODUL["schmuggel_risiko"] = 0.2      # je Tagesende und Schmuggelware im Inventar: Elsa (Kuestenwache) findet sie

# ---------------------------------------------------------------- Gesten (16.10.2026)
# bereich: reden / naehe / mutig / intim. art: klein = +4 Punkte bis Stufe 3; gross = Erlebnis (+1 Stufe = 8 Punkte),
# hoechstens eine grosse Geste je Frau und Tag. schwelle = Mindest-Stufen. privat = niemand sonst da und Raum privat >= 4.
# moment = Chronik-Eintrag bei Erfolg. handlung = was Duc tut (englisch, {n} = ihr Name).
G = lambda gid, bereich, label, handlung, attr, sg, art, achse, schwelle=None, privat=False, moment=None, **kw: dict(
    {"id": gid, "bereich": bereich, "label": label, "handlung": handlung, "attribut": attr, "sg": sg, "art": art,
     "achse": achse, "schwelle": schwelle or {}, "privat": privat, "moment": moment}, **kw)
MODUL["gesten"] = [
    G("kompliment", "reden", "Compliment", "He pays {n} a sincere, specific compliment.", "charm", 10, "klein", ["begehren"]),
    G("fragen", "reden", "Ask something real", "He asks {n} something real about herself - and actually listens.",
      "empathy", 10, "klein", ["vertrauen"]),
    G("necken", "reden", "Tease", "He teases {n}, light and playful.", "charm", 11, "klein", ["begehren"],
      {"vertrauen": 1}),
    G("troesten", "reden", "Comfort", "He notices something weighs on {n} and comforts her.", "empathy", 10, "klein",
      ["vertrauen"]),
    G("entschuldigen", "reden", "Apologise", "He apologises to {n}, honestly, without excuses.", "empathy", 9,
      "klein", ["vertrauen"], moment_wenn_streit="apology"),
    G("geheimnis", "reden", "Share your secret", "He tells {n} what he hasn't told anyone aboard: a firm in Frankfurt "
      "wants his answer by the end of this week, and he doesn't know what to say.", "empathy", 11, "gross",
      ["vertrauen"], {"vertrauen": 3}, moment="duc_secret"),
    G("hand", "naehe", "Take her hand", "He takes {n}'s hand.", "charm", 10, "klein", ["begehren"],
      {"vertrauen": 2, "begehren": 2}),
    G("umarmen", "naehe", "Hug", "He pulls {n} into a hug.", "empathy", 10, "klein", ["vertrauen", "begehren"],
      {"vertrauen": 2}),
    G("haar", "naehe", "Brush her hair back", "He brushes a strand of hair from {n}'s face.", "charm", 11, "klein",
      ["begehren"], {"begehren": 3}),
    G("kuessen", "naehe", "Kiss", "He leans in and kisses {n}.", "courage", 12, "gross", ["begehren"],
      {"vertrauen": 3, "begehren": 3}, moment="kiss"),
    G("massage", "naehe", "Massage", "He offers {n} a massage and works the tension out of her shoulders.", "charm", 11,
      "klein", ["begehren"], {"vertrauen": 3, "begehren": 3}, privat=True, vorteil_items=["massage_oil", "massage_candle"]),
    G("einladen", "mutig", "Ask her out tonight", "He asks {n} to spend the evening with him - just the two of them.",
      "charm", 11, "gross", ["vertrauen"], {"vertrauen": 2}, verabredung=True),
    G("gestehen", "mutig", "Confess your feelings", "He tells {n} plainly that he has feelings for her.", "courage", 13, "gross",
      ["vertrauen", "begehren"], {"vertrauen": 3, "begehren": 3}, moment="confession"),
    G("eifersucht", "mutig", "Talk about jealousy", "He asks {n} straight out whether something about him and the "
      "others is bothering her.", "empathy", 12, "klein", ["vertrauen"]),
    G("versprechen", "mutig", "Make a promise", "He makes {n} a serious promise about what comes after this week.",
      "courage", 10, "gross", ["vertrauen"], {"vertrauen": 3}, moment="promise"),
    # Duc 02.11.2026: der Weg vom Gespraech in die intime Szene. Bei Ja geht die Szene in Ducs Kabine weiter, bei Nein
    # sagt sie ihre feste Absage (figurenrahmen.json absage.privat), das Modell spielt kein Nein.
    G("privat_gehen", "mutig", "Go somewhere private", "He quietly asks {n} to come with him somewhere they can be alone.",
      "charm", 12, "gross", ["begehren"], {"vertrauen": 3, "begehren": 3}),
    G("ausziehen", "intim", "Undress her", "He slowly starts to undress {n}.", "charm", 11, "klein", ["begehren"],
      {"vertrauen": 3, "begehren": 3}, privat=True),
    G("vorspiel", "intim", "Foreplay", "He draws {n} close and starts touching her, slow and deliberate.", "charm", 10,
      "klein", ["begehren"], {"vertrauen": 3, "begehren": 4}, privat=True),
    G("schlafen", "intim", "Sleep with her", "He and {n} end up in bed together.", "charm", 10, "gross",
      ["vertrauen", "begehren"], {"vertrauen": 4, "begehren": 5}, privat=True, moment="intimate", intim_aktiv=True),
]
# Je Frau drei Lieblingsgesten ("zeit" = Zeit zusammen): +2 auf die Probe, im Menue mit Herz markiert.
MODUL["lieblingsgesten"] = {
    "rosi": ["zeit", "necken", "entschuldigen"], "chiara": ["kompliment", "fragen", "versprechen"],
    "sophia": ["necken", "geheimnis", "einladen"], "lea": ["zeit", "hand", "umarmen"],
    "siri": ["fragen", "troesten", "haar"],
}
# Intim-Vorlieben (Eintraege der ST-Weltbuecher "Position: ..." / "Act: ..."): mag = nimmt sie gern an,
# nein = lehnt sie im Charakter ab und schlaegt etwas anderes vor; alles andere = offen. Erster Vorschlag - frei anpassbar.
MODUL["intim_vorlieben"] = {
    "rosi": {"mag": ["Position: Cowgirl", "Position: Reverse Cowgirl", "Act: Grinding", "Position: Against the Wall"],
             "nein": ["Act: Spanking"]},
    "chiara": {"mag": ["Position: Missionary", "Position: Standing Missionary", "Act: Massage", "Position: Bent Over Desk"],
               "nein": ["Act: Anal"]},
    "sophia": {"mag": ["Position: Lotus", "Act: Anal", "Position: Face-Sitting", "Act: Edging"], "nein": []},
    "lea": {"mag": ["Position: Spooning", "Position: Shower", "Position: Missionary", "Act: Kissing"],
            "nein": ["Act: Spanking", "Act: Hair Pulling", "Act: Anal"]},
    "siri": {"mag": ["Position: Spooning", "Position: Cowgirl", "Act: Caressing", "Position: Lotus"],
             "nein": ["Act: Facefuck"]},
}
# Welche Akte ab welcher Begehren-Stufe (Stellungen: Stufe 5 und erst nach "Mit ihr schlafen").
MODUL["intim_stufen"] = {
    3: ["Act: Kissing", "Act: Caressing", "Act: Undressing", "Act: Massage"],
    4: ["Act: Nipple Play", "Act: Fingering", "Act: Cunnilingus", "Act: Handjob", "Act: Blowjob", "Act: Titjob",
        "Act: Grinding"],
    5: ["Act: Anal", "Act: Spanking", "Act: Hair Pulling", "Act: Edging", "Act: Her Climax", "Act: His Climax"],
}

MODUL["arc"] = "arc.md"      # Showrunner-Bibel: Akte, Tagesgeruest, Ressourcen-Takt, Herz-Takt, Enden
MODUL["enden"] = {
    "ausgang": {"reparatur": "The Eden Rise sails out of Cala d'Orsu under her own power.",
                "rettung": "A tug from Ajaccio takes her in tow. Honourable, but not under her own power.",
                "katastrophe": "A battery fire in the last night. Everyone off, everyone hurt, nobody dead. The boat is lost.",
                "standard": "rettung"},
    "herz_schwelle": {"vertrauen": 4, "begehren": 4},
    "persona": ["back to Frankfurt", "one more season at sea", "with her"],
}

MODUL["items"] = {
    "multitool": {"label": "Multitool", "art": "gluecksbringer", "effekt": {"vorteil": "cunning"}, "text": "einmal pro Tag Vorteil auf Cunning"},
    # --- Andenken (16.10.2026): feste Gegenstaende im Bogen, dauerhaft +1, belegen keinen der 6 Plaetze, unverkaeuflich
    "holm_compass": {"label": "Holms Messingkompass", "art": "andenken", "effekt": {"bonus": ["courage", 1]},
                     "text": "Sie hat ihn dir beim Abschied in die Hand gedrückt. Courage +1."},
    # 26.10.2026 (Duc): die Andenken aus Gestrandet ohne Quelle in Eden Rise sind raus (Ringschluessel, Sternkarte,
    # Notizbuchseite, Muschel, Knotenarmband, Festa-Medaille)
    "petru_key": {"label": "Schlüssel zu Petrus Werkstatt", "art": "schluessel"},
    "festa_invite": {"label": "Einladung der Bürgermeisterin zur Festa", "art": "schluessel"},
    "spare_inverter": {"label": "Wechselrichter-Modul (gebraucht)", "art": "ressource", "preis": 600, "wo": ["toto"], "einmalig": True,
                       "wirkung": [{"uhr": "reparatur", "delta": 2}], "text": "Passt fast. Reparatur +2."},
    "diesel_canister": {"label": "Kanister Diesel", "art": "ressource", "preis": 120, "wo": ["toto", "dorf"],
                        "preise": {"toto": 100, "dorf": 140}, "wirkung": [{"wert": "diesel", "delta": 1}], "text": "Diesel +1."},
    # --- Waren (16.10.2026): Geschenke, Gluecksbringer, Ressourcen, Verbrauch, Schmuggel. geschenk = Geschmack je Frau
    #     (2 Lieblingsgeschenk, 1 freut sie, 0 egal, -1 daneben), "*" = alle anderen.
    "manga": {"label": "Manga-Band (italienisch)", "art": "geschenk", "preis": 25, "wo": ["toto"],
              "geschenk": {"rosi": 2, "lea": 1, "*": 0}, "text": "Totòs Neffe liest so was."},
    "arancini": {"label": "Arancini vom Bäcker", "art": "geschenk", "preis": 15, "wo": ["dorf"],
                 "geschenk": {"rosi": 2, "*": 1}, "text": "Noch warm. Riecht nach Sizilien."},
    "torque_wrench": {"label": "Profi-Drehmomentschlüssel", "art": "geschenk", "preis": 90, "wo": ["toto"],
                      "geschenk": {"rosi": 2, "*": 0}, "text": "Für jemanden, der Werkzeug ernst nimmt."},
    "olive_oil": {"label": "Korsisches Olivenöl", "art": "geschenk", "preis": 35, "wo": ["dorf"],
                  "geschenk": {"chiara": 2, "sophia": 1, "*": 0}, "text": "Kaltgepresst, vom Hof oberhalb des Dorfs."},
    "almanac": {"label": "Nautischer Almanach", "art": "geschenk", "preis": 60, "wo": ["toto"],
                "geschenk": {"chiara": 2, "lea": 1, "*": 0}, "text": "Gezeiten, Gestirne, Prüfungsstoff."},
    "fountain_pen": {"label": "Füllfederhalter", "art": "geschenk", "preis": 70, "wo": ["toto"],
                     "geschenk": {"sophia": 2, "chiara": 1, "*": 0}, "text": "Schwarz, schwer, schreibt wie Samt."},
    "notebook": {"label": "Notizbuch aus Leder", "art": "geschenk", "preis": 40, "wo": ["dorf"],
                 "geschenk": {"sophia": 2, "*": 0}, "text": "Leere Seiten für ein ganzes Buch."},
    "dive_torch": {"label": "Tauchlampe", "art": "geschenk", "preis": 80, "wo": ["dorf"],
                   "geschenk": {"lea": 2, "rosi": 1, "*": 0}, "text": "Hell genug für ein Wrack bei Nacht."},
    "old_chart": {"label": "Alte Seekarte der Westküste", "art": "geschenk", "preis": 120, "wo": ["toto"],
                  "geschenk": {"lea": 2, "sophia": 1, "*": 0}, "text": "Von 1931. Mit Wracks eingezeichnet."},
    "wool_socks": {"label": "Handgestrickte Wollsocken", "art": "geschenk", "preis": 20, "wo": ["dorf"],
                   "geschenk": {"siri": 2, "*": 0}, "text": "Von der Großmutter am Hafen. Nichts Teures."},
    "designer_perfume": {"label": "Designerparfum", "art": "geschenk", "preis": 140, "wo": ["toto"],
                         "geschenk": {"siri": -1, "chiara": 1, "sophia": 1, "*": 0}, "text": "Luxus. Kommt nicht bei jeder gut an."},
    "myrtle": {"label": "Myrtenlikör", "art": "geschenk", "preis": 30, "wo": ["dorf"],
               "geschenk": {"sophia": 1, "chiara": 1, "*": 1}, "text": "Der Schnaps der Insel."},
    # --- Dating-Sim (16.10.2026): von romantisch bis eindeutig. "intim" = ab welcher Naehe es ankommt.
    "candles": {"label": "Duftkerzen „Maquis“", "art": "geschenk", "preis": 25, "wo": ["dorf"],
                "geschenk": {"sophia": 2, "siri": 1, "*": 1}, "text": "Myrte, Zistrose, Meersalz. Riecht nach der Insel bei Nacht."},
    "massage_oil": {"label": "Massageöl mit Neroli", "art": "geschenk", "preis": 35, "wo": ["dorf"],
                    "geschenk": {"chiara": 2, "siri": 2, "*": 1}, "intim": {"vertrauen": 2},
                    "text": "Für Schultern nach einer Saison voller Tabletts. Oder für mehr."},
    "silk_blindfold": {"label": "Seidene Augenbinde", "art": "geschenk", "preis": 45, "wo": ["toto"],
                       "geschenk": {"sophia": 2, "chiara": 1, "lea": 1, "*": 0}, "intim": {"begehren": 3},
                       "text": "Schwarze Maulbeerseide. Sophia würde sagen: zu Recherchezwecken."},
    "pretty_shell": {"label": "Schöne Muschel", "art": "geschenk", "preis": 12, "wo": ["dorf"],
                     "geschenk": {"lea": 2, "siri": 1, "*": 1}, "text": "Eine Tritonmuschel vom Fischmarkt, groß wie eine Hand. Man hört das Meer."},
    "pink_pearl": {"label": "Rosa Perle an feiner Kette", "art": "geschenk", "preis": 150, "wo": ["toto"],
                   "geschenk": {"siri": 2, "chiara": 2, "sophia": 1, "*": 1}, "text": "Eine einzelne rosa Perle. Schlicht genug für Siri, edel genug für Chiara."},
    "shell_anklet": {"label": "Fußkettchen mit Muschel", "art": "geschenk", "preis": 30, "wo": ["dorf"],
                     "geschenk": {"lea": 2, "siri": 2, "*": 1}, "intim": {"vertrauen": 2},
                     "text": "Silber, eine winzige Kaurimuschel. Von der Großmutter am Hafen geknüpft."},
    "silk_kimono": {"label": "Seidenkimono", "art": "geschenk", "preis": 95, "wo": ["toto"],
                    "geschenk": {"sophia": 2, "siri": 2, "*": 0}, "intim": {"begehren": 2},
                    "text": "Nachtblau, mit Kranichen. Für den Morgen danach – oder eine lange Schreibnacht."},
    "massage_candle": {"label": "Massagekerze mit Wärmeöl", "art": "geschenk", "preis": 40, "wo": ["toto"],
                       "geschenk": {"rosi": 2, "chiara": 2, "*": 0}, "intim": {"begehren": 3},
                       "text": "Die Kerze schmilzt zu warmem Öl. Nach einer Nachtschicht im Maschinenraum genau richtig."},
    "stockings": {"label": "Halterlose Strümpfe mit Spitzenrand", "art": "geschenk", "preis": 55, "wo": ["toto"],
                  "geschenk": {"chiara": 2, "sophia": 2, "rosi": -1, "*": 0}, "intim": {"vertrauen": 3, "begehren": 3},
                  "text": "Schwarz, hauchdünn, breiter Spitzenrand. Rosi würde sie als Ölfilter benutzen."},
    "satin_ties": {"label": "Satin-Fesselband fürs Bett", "art": "geschenk", "preis": 50, "wo": ["toto"],
                   "geschenk": {"sophia": 2, "rosi": 2, "*": 0}, "intim": {"vertrauen": 4, "begehren": 4},
                   "text": "Weinroter Satin, vier Bänder, nichts, was wehtut. Vertrauen zuerst."},
    "nipple_clamps": {"label": "Nippelklemmen mit Kettchen", "art": "geschenk", "preis": 45, "wo": ["toto"],
                      "geschenk": {"sophia": 2, "siri": -1, "lea": -1, "*": 0}, "intim": {"vertrauen": 4, "begehren": 5},
                      "text": "Feines Gold, ein Kettchen dazwischen. Nur für ganz Vertraute – und nicht für jede."},
    "lingerie": {"label": "Spitzen-Dessous in Champagner", "art": "geschenk", "preis": 120, "wo": ["toto"],
                 "geschenk": {"sophia": 2, "chiara": 2, "siri": -1, "*": 0}, "intim": {"vertrauen": 3, "begehren": 3},
                 "text": "Französische Spitze, Seidenbänder. Bei der Falschen wirkt es wie ein Katalog."},
    "plush_cuffs": {"label": "Plüsch-Handschellen", "art": "geschenk", "preis": 40, "wo": ["toto"],
                    "geschenk": {"rosi": 2, "sophia": 1, "*": 0}, "intim": {"vertrauen": 3, "begehren": 4},
                    "text": "Rosa Plüsch, echter Stahl. Wer gewinnt, entscheidet, wer sie trägt."},
    "eden_wave": {"label": "Vibrator „Eden Wave“", "art": "geschenk", "preis": 90, "wo": ["toto"],
                  "geschenk": {"rosi": 2, "sophia": 1, "*": 0}, "intim": {"vertrauen": 3, "begehren": 4},
                  "text": "Flüsterleise, wasserdicht, lädt mit Sonnenlicht. Eine Ingenieurin schätzt gute Technik."},
    "jeweled_plug": {"label": "Butt Plug mit Schmuckstein", "art": "geschenk", "preis": 60, "wo": ["toto"],
                     "geschenk": {"sophia": 2, "lea": 1, "rosi": -1, "*": 0}, "intim": {"vertrauen": 4, "begehren": 5},
                     "text": "Poliertes Metall, ein rosa Stein in Herzform, im Samtkästchen. Nur für ganz Vertraute."},
    "binoculars": {"label": "Fernglas", "art": "gluecksbringer", "preis": 220, "wo": ["toto"],
                   "effekt": {"vorteil": "perception"}, "text": "Einmal pro Tag Vorteil auf Perception."},
    "aftershave": {"label": "Rasierwasser „Bastia“", "art": "gluecksbringer", "preis": 150, "wo": ["dorf"],
                   "effekt": {"vorteil": "charm"}, "text": "Einmal pro Tag Vorteil auf Charm."},
    "lockpicks": {"label": "Dietrich-Set", "art": "gluecksbringer", "preis": 180, "wo": ["toto"],
                  "effekt": {"vorteil": "cunning"}, "text": "Einmal pro Tag Vorteil auf Cunning."},
    "lucky_coin": {"label": "Glücksmünze von Alva", "art": "gluecksbringer", "preis": 120, "wo": ["dorf"],
                   "effekt": {"vorteil": "courage"}, "text": "Einmal pro Tag Vorteil auf Courage."},
    "tarot": {"label": "Tarotkarten", "art": "gluecksbringer", "preis": 100, "wo": ["toto"],
              "effekt": {"vorteil": "empathy"}, "text": "Einmal pro Tag Vorteil auf Empathy."},
    "used_battery": {"label": "Gebrauchte Bootsbatterie", "art": "ressource", "preis": 250, "wo": ["toto"],
                     "wirkung": [{"wert": "strom", "delta": 2}], "text": "Strom +2. Frag nicht, von welchem Boot."},
    "panel_cleaner": {"label": "Paneel-Reiniger", "art": "ressource", "preis": 60, "wo": ["dorf"],
                      "wirkung": [{"wert": "strom", "delta": 1}], "text": "Salz runter, Sonne rein. Strom +1."},
    "espresso": {"label": "Doppelter Espresso", "art": "verbrauch", "preis": 5, "wo": ["toto", "dorf"],
                 "wirkung": [{"wert": "energie", "delta": 1}], "text": "Energie +1."},
    "sat_data": {"label": "Satelliten-Datenpaket", "art": "schmuggel", "preis": 300, "wo": ["toto"],
                 "benutzen": [{"uhr": "rettung", "delta": 1}, {"codex": "Mit Totòs Datenpaket nach draußen gefunkt."}],
                 "text": "Ein Anruf nach draußen, an allen Ämtern vorbei. Rettung +1 beim Benutzen."},
    "cuban_rum": {"label": "Kubanischer Rum", "art": "schmuggel", "preis": 120, "wo": ["toto"],
                  "benutzen": [{"wert": "moral", "delta": 2}], "geschenk": {"rosi": 1, "chiara": 1, "*": 1},
                  "text": "Für die Crew: Moral +2 beim Benutzen. Oder als Geschenk."},
    "cigars": {"label": "Cohiba-Zigarren", "art": "schmuggel", "preis": 150, "wo": ["toto"],
               "benutzen": [{"wert": "ruf", "delta": 2}], "text": "Für die Alten am Hafen: Ruf +2 beim Benutzen."},
    "serial_mismatch": {"label": "Serial number that doesn't match the logbook", "art": "beweis"},
    "power_log": {"label": "Power log: load on the bridge at 02:10", "art": "beweis"},
    "gps_track": {"label": "GPS track with a detour towards the Esterel", "art": "beweis"},
    "paris_call": {"label": "Sophia's call from Paris", "art": "beweis"},
    "breaker_note": {"label": "Fuse with Rosi's handwriting", "art": "beweis"},
    "burnt_cable": {"label": "Charred charging cable from the VIP cabin", "art": "beweis"},
}

R = lambda label, tag, nacht=None, privat=1, zugang=None: {"label": label, "zugang": zugang or [], "privat": privat,
                                                          "bild": dict({"tag": tag}, **({"nacht": nacht} if nacht else {}))}
MODUL["raeume"] = {
    "crew_mess": R("Crew mess (below deck)", "yacht_crew_mess.png", privat=1),
    "crew_corridor": R("Crew corridor", "yacht_crew_corridor.png", privat=1),
    "galley": R("Galley", "yacht_galley.png", privat=2),
    # 17.10.2026: neue Kabine passend zur Kabinen-Mechanik (Seekiste, Schreibtisch mit Handy, Trainingsecke), Tag/Nacht gleicher Raum
    "duc_cabin": R("Duc's cabin (the only single cabin, door locks)", "eden_rise_duc_cabin.png", "eden_rise_duc_cabin_night.png", privat=5),
    "bridge": R("Bridge", "yacht_bridge_day_v2.png", "yacht_bridge_night.png", privat=2, zugang=[{"persona": "first_officer"}]),
    "main_salon": R("Main salon (guest area)", "yacht_main_salon.png", privat=1),
    "aft_deck": R("Aft deck (dining table)", "yacht_aft_deck_dining.png", privat=1),
    "sun_deck": R("Sun deck", "yacht_sun_deck.png", "yacht_sun_deck_night.png", privat=3),
    "solar_deck": R("Solar deck (top deck under the panels)", "yacht_solar_deck.png", "eden_rise_solar_deck_nacht.png", privat=4),
    "foredeck": R("Foredeck", "yacht_foredeck_sunrise.png", "eden_rise_foredeck_nacht.png", privat=3),
    "swim_platform": R("Swim platform", "yacht_swim_platform.png", privat=3),
    "tender_garage": R("Tender garage", "yacht_tender_garage.png", privat=4),
    "power_room": R("Power room (batteries, inverters, electric drive)", "yacht_power_room.png", "yacht_power_room_night.png", privat=3),
    "generator_room": R("Generator room (Unit-01)", "yacht_generator_room.png", privat=5,
                        zugang=[{"vertrauen": ["rosi", 2]}, {"begleitung": "rosi"},
                                {"wurf": ["cunning", 13], "risiko": "Rosi merkt es (vertrauen.rosi -1)"}]),
    "workshop": R("Engineers' workshop", "yacht_workshop.png", privat=4,
                  zugang=[{"vertrauen": ["rosi", 1]}, {"begleitung": "rosi"}]),
    "vip_cabin": R("VIP cabin (Siri and Yasin)", "yacht_vip_cabin.png", privat=5,
                   zugang=[{"vertrauen": ["siri", 4]}, {"begleitung": "siri"},
                           {"wurf": ["cunning", 15], "risiko": "Yasin erwischt Duc"}]),
    "village_harbour": R("Harbour of Cala d'Orsu (ashore)", "corsican_village_harbour.png", "corsican_village_harbour_night_v2.png", privat=1),
    "alvas_bar": R("Alva's bar (ashore)", "corsican_village_bar.png", privat=2),
    # Dorf-Figuren (Duc 30.10.2026, docs/wiki/welt/dorf_figuren.md): oeffnen mit ihrer ersten Szene
    "batu_shop": R("B\u00e0 T\u01b0's shop", "eden_rise_batu_shop.png", privat=2, zugang=[{"flag": "batu_laden"}]),
    "av_market": R("A.V. Market", "eden_rise_av_market_exterior.png", privat=1, zugang=[{"flag": "a2_sandru"}]),
    "church": R("The church of Cala d'Orsu", "eden_rise_church_interior.png", privat=2, zugang=[{"flag": "a2_messe"}]),
    "mochis": R("Mochi's", "eden_rise_mochis_station_voll.png", privat=1, zugang=[{"flag": "mochis_offen"}]),   # Red Trio: Bibis Tierstation
    # Zimmer und Orte fuer Zweisamkeit (Duc 02.11.2026, kern/orte.py, welt/wohnen.md): nur ueber Go somewhere private, nicht auf der Karte
    "crew_kabine_1": dict(R("Crew cabin (Sophia and Lea)", "eden_rise_crew_kabine_1.png", privat=4), versteckt=True),
    "crew_kabine_2": dict(R("Crew cabin (Lola and Jana)", "eden_rise_crew_kabine_2.png", privat=4), versteckt=True),
    "crew_kabine_3": dict(R("Crew cabin (Chiara and Rosi)", "eden_rise_crew_kabine_3.png", privat=4), versteckt=True),
    "spare_cabin": dict(R("The spare cabin (by the laundry)", "eden_rise_waescherei_kabine_tag.png", "eden_rise_waescherei_kabine_nacht.png", privat=5), versteckt=True),
    "alvas_hinterzimmer": dict(R("Alva's flat above the bar (ashore)", "eden_rise_alva_wohnung_tag.png", "eden_rise_alva_wohnung_nacht.png", privat=5), versteckt=True),
    "bibi_haeuschen": dict(R("Bibi's cottage at Mochi's (ashore)", "eden_rise_bibi_haeuschen_tag.png", "eden_rise_bibi_haeuschen_nacht.png", privat=5, zugang=[{"flag": "mochis_offen"}]), versteckt=True),
    # Alons Keynote-Buehne im Cliffhanger Akt 2 (Duc 02.11.2026): nur Szenenbild, nie auf der Karte
    "alon_keynote": dict(R("Alon's keynote (on every phone)", "eden_rise_alon_keynote_nah.png", privat=0), versteckt=True),
    "tenderboot": dict(R("The tender at anchor", "eden_rise_tenderboot_nacht.png", privat=5), versteckt=True),
    "mochis_bucht": dict(R("The cove below Mochi's (ashore)", "eden_rise_mochis_bucht_abend.png", privat=4, zugang=[{"flag": "mochis_offen"}]), versteckt=True),
    "kuehlraum": dict(R("The cold room behind the galley", "eden_rise_kuehlraum.png", privat=4), versteckt=True),
    "genueser_turm": dict(R("Top of the Genoese tower (ashore)", "eden_rise_genueser_turm_nacht.png", privat=4), versteckt=True),
    "megan_kabine": dict(R("Megan's VIP cabin (port side)", "eden_rise_megan_kabine.png", "eden_rise_megan_kabine_nacht.png", privat=5), versteckt=True),
    "crew_dusche": dict(R("The crew shower room", "eden_rise_crew_dusche.png", privat=5), versteckt=True),
    "yacht_toilette": dict(R("The crew toilet", "eden_rise_yacht_toilette.png", privat=5), versteckt=True),
    "petru_workshop": R("Petru's boat workshop (ashore)", "corsican_fisherman_workshop.png", privat=3,
                        zugang=[{"item": "petru_key"}, {"wert": ["ruf", ">=", 2]}, {"begleitung": "rosi"}]),
    "village_piazza": R("The piazza of Cala d'Orsu", "corsican_village_festa.png", privat=2,
                        zugang=[{"tag_ab": 5}, {"item": "festa_invite"}]),
}
# Karte im Handy als "Wohin?" (17.10.2026): Gruppen in dieser Reihenfolge, Namen deutsch fuer die Anzeige.
MODUL["bereiche"] = {"unterdeck": "Unter Deck", "deck": "An Deck", "technik": "Technik", "land": "An Land"}
for _b, _ids in {"unterdeck": ["crew_mess", "crew_corridor", "galley", "duc_cabin", "vip_cabin"],
                 "deck": ["main_salon", "bridge", "aft_deck", "sun_deck", "solar_deck", "foredeck", "swim_platform",
                          "tender_garage"],
                 "technik": ["power_room", "generator_room", "workshop"],
                 "land": ["village_harbour", "alvas_bar", "batu_shop", "av_market", "church", "mochis", "petru_workshop", "village_piazza"]}.items():
    for _r in _ids:
        MODUL["raeume"][_r]["bereich"] = _b

# Kabine statt Szene (kern/kabine.py, 17.10.2026): Leuchtpunkte in % auf eden_rise_duc_cabin(_night).png.
# Holm steht bewusst nicht in anruf_orte - Tag 1 ist sie an Bord, ab Tag 2 meldet kabine.wo "far away from the boat".
MODUL["kabine"] = {"ort": "duc_cabin",
                   # Truhe: Sea Chest im offenen Kasten, Keepsake Box auf dem Deckel (26.10.2026, Duc)
                   "hotspots": {"truhe": [32, 86], "andenken": [30, 68], "handy": [66, 51], "handschuhe": [84, 30],
                                "koje": [27, 50]},
                   "kein_handy": ["petru"],
                   "schmuggel_faktor": 0.5}

STIMMEN = {"chiara": "86DPV1zNth30lTeo94q1", "sophia": "njBRrH42VRvVJwg7VZLZ", "lea": "bYNVonNheU7TZMAR50LQ"}
MODUL["personen"] = {
    "chiara": {"name": "Chiara Sonnberg", "karte": "Chiara Sonnberg", "romanzierbar": True, "schaetzt": ["courage", "perception"],
               "ablauf": {"fruehstueck": "crew_mess", "tag": "main_salon", "dinner": "crew_mess", "abend": "aft_deck", "nacht": "bridge"},
               "set_standard": "Uniform",
               "set_regeln": [{"ort": "swim_platform", "set": "Swim"}, {"ort": "bridge", "phase": "nacht", "set": "Bridge Night"},
                              {"ort": "village_piazza", "set": "Harbor Night"}, {"ort": "alvas_bar", "phase": "abend", "set": "Harbor Night"},
                              {"ort": "duc_cabin", "phase": "nacht", "set": "Cabin Night"}, {"phase": "dinner", "set": "Service"},
                              {"phase": "nacht", "set": "Cabin Night"}]},
    "sophia": {"name": "Sophia Moore", "karte": "Sophia Moore", "romanzierbar": True, "schaetzt": ["perception", "cunning"],
               "ablauf": {"fruehstueck": "crew_mess", "tag": "village_harbour", "dinner": "crew_mess", "abend": "alvas_bar", "nacht": "crew_mess"},
               "set_standard": "Concierge",
               "set_regeln": [{"ort": "swim_platform", "set": "Swim"}, {"ort": "village_harbour", "set": "Shore Leave"},
                              {"ort": "alvas_bar", "set": "Shore Leave"}, {"ort": "village_piazza", "set": "Crew Party"},
                              {"phase": "nacht", "set": "Writing Night"}]},
    "lea": {"name": "Lea Moore", "karte": "Lea Moore", "romanzierbar": True, "schaetzt": ["empathy", "courage"],
            "ablauf": {"fruehstueck": "tender_garage", "tag": "swim_platform", "dinner": "crew_mess", "abend": "sun_deck", "nacht": "swim_platform"},
            "set_standard": "Deck",
            "set_regeln": [{"ort": "swim_platform", "phase": "tag", "set": "Dive"}, {"ort": "swim_platform", "phase": "abend", "set": "Leopard Bikini"},
                           {"ort": "village_harbour", "set": "Expedition"}, {"ort": "petru_workshop", "set": "Expedition"},
                           {"ort": "village_piazza", "set": "Crew Party"}, {"phase": "abend", "set": "Off Duty"},
                           {"phase": "nacht", "set": "Off Duty"}]},
    "rosi": {"name": "Rosi Scuderi", "karte": "Rosi Scuderi", "romanzierbar": True, "schaetzt": ["cunning", "courage"],
             "ablauf": {"fruehstueck": "power_room", "tag": "power_room", "dinner": "crew_mess", "abend": "workshop", "nacht": "generator_room"},
             "set_standard": "Engine Room",
             "set_regeln": [{"ort": "swim_platform", "set": "Swim"}, {"ort": "village_harbour", "set": "Vespa Sunday"},
                            {"ort": "alvas_bar", "phase": "abend", "set": "Crew Party"}, {"ort": "village_piazza", "set": "Festa"},
                            {"ort": "crew_mess", "phase": "abend", "set": "Off Duty"}, {"ort": "duc_cabin", "set": "Off Duty"}]},
    "siri": {"name": "Siri Lindvik", "karte": "Siri Lindvik", "romanzierbar": True, "schaetzt": ["empathy", "charm"],
             "ablauf": {"fruehstueck": "foredeck", "tag": "sun_deck", "dinner": "aft_deck", "abend": "main_salon", "nacht": "solar_deck"},
             "set_standard": "Sea Siren",
             "set_regeln": [{"ort": "foredeck", "set": "Morning Ritual"}, {"ort": "swim_platform", "set": "Riviera Swim"},
                            {"ort": "village_harbour", "set": "Saint-Tropez '69"}, {"ort": "alvas_bar", "set": "Saint-Tropez '69"},
                            {"ort": "village_piazza", "set": "Silver Night"}, {"phase": "dinner", "set": "Silver Night"},
                            {"phase": "nacht", "set": "Dad's Sweater"}]},          # Outfits (Duc 29.10.2026): nachts im Pullover
    "toto": {"name": "Salvatore 'Totò' Esposito", "stimme": "Toto Esposito", "kurz": "Totò", "romanzierbar": False, "st_ordner": "Toto Esposito",
             "set_standard": "toto_standard", "set_regeln": [{"phase": "abend", "set": "toto_Shirt"},     # Outfits (Duc 29.10.2026)
                                                             {"phase": "dinner", "set": "toto_Shirt"}],
             "beschreibung": "the bosun, 47, from Naples; gold chain, flip-flops, always eating something; calls Duc "
                             "'Comandante'; a cousin in Bastia who comes by rubber boat at night; sells anything from a "
                             "locked locker in the lazarette and never asks where things come from - 'Nothing fell off a "
                             "truck, Comandante. It fell off a boat.' Warm-hearted, funny, loyal to the crew, allergic "
                             "to paperwork. Runs the betting board in the engine room.",
             "ablauf": {"*": "crew_mess"}},
    "yasin": {"name": "Yasin Benali", "stimme": "Yasin Benali", "kurz": "Yasin", "romanzierbar": False,
              "beschreibung": "Siri's boyfriend, 29, from Paris, sells online trading courses; expensive watch, cash for every tip, a phone always filming; flirts with every woman of the crew, calls the crew 'my team', treats Siri like a prop. Stranded, he is furious and bored.",
              "ablauf": {"*": "main_salon", "tag": "sun_deck", "nacht": "vip_cabin"}},
    "holm": {"name": "Captain Marit Holm", "kurz": "Holm", "romanzierbar": False,
             "beschreibung": "the captain, 56, Norwegian, thirty years at sea, dry, fair, impossible to fool; in pain from appendicitis and furious that she has to leave her boat",
             "ablauf": {"*": "bridge"}},
    "elsa": {"name": "Elsa Ferrandi", "stimme": "Elsa Ferrandi", "kurz": "Elsa", "romanzierbar": False,
             "beschreibung": "lieutenant of the maritime gendarmerie, 29, Corsican, runs the small coast-guard post at the "
                             "harbour of Cala d'Orsu and a fast patrol boat; dry humour, sharp eyes, never breaks a rule but "
                             "loves bending one; coordinates salvage and towing with Ajaccio; hunts smugglers and has had "
                             "her eye on Toto since the day the yacht arrived; money offered to her is an insult, respect "
                             "and competence are not",
             "ablauf": {"*": "village_harbour"}},
    "alva": {"name": "Alva Santoni", "stimme": "Alva Santoni", "kurz": "Alva", "romanzierbar": False,
             "beschreibung": "owner of the only bar in Cala d'Orsu, 35, took the bar over from her father; knows everything that happens in the village, sells diesel under the counter, flirts with everyone and means it with nobody, calls everyone 'o figliolu'",
             "ablauf": {"*": "alvas_bar"}},
    "petru": {"name": "Petru Albertini", "stimme": "Petru Albertini", "kurz": "Petru", "romanzierbar": False,
              "beschreibung": "old fisherman, seventies, with his own boat workshop; speaks little, repairs everything, has heard every legend of the coast",
              "ablauf": {"*": "petru_workshop"}},
    "casanova": {"name": "Madame Casanova", "stimme": "Madame Casanova", "kurz": "the mayor", "romanzierbar": False,
                 "beschreibung": "mayor of Cala d'Orsu, 40, a whirlwind with anime-style humour: dramatic poses, exaggerated gasps, fist pumps and sudden speeches, treats every village event like a season finale; wants the stranded superyacht as the big attraction of the festa",
                 "ablauf": {"*": "village_harbour"}},
}

# Lieblingsorte (17.10.2026): eine Verabredung dort freut sie sichtbar und bringt einen kleinen Bonus
# (+4 Vertrauen und +4 Begehren, halb so viel wie ein Erlebnis). Die Karte im Handy zeigt sie mit Herz.
for _pid, _orte in {"chiara": ["bridge", "sun_deck"], "sophia": ["alvas_bar", "aft_deck"],
                    "lea": ["swim_platform", "tender_garage"], "rosi": ["workshop", "petru_workshop"],
                    "siri": ["foredeck", "solar_deck"]}.items():
    MODUL["personen"][_pid]["lieblingsorte"] = _orte
# Pronomen fuer feste Texte (Vorlieben, 18.10.2026); ohne Eintrag gilt "sie"
for _pid in ("toto", "yasin", "petru"):
    MODUL["personen"][_pid]["pronomen"] = "er"

# Storylets: Gruppenszenen + je Frau ein Bogen in drei Stufen (Stufe 2/3 erst mit Vertrauen).
S = lambda phase, titel, wer, ort, kern, bed=None: {"phase": phase, "titel": titel, "wer": wer, "ort": ort, "bedingung": bed or {}, "kern": kern}
MODUL["storylets"] = {
    # Gruppe / Alltag
    "briefing": S("fruehstueck", "Morning briefing", ["chiara", "sophia", "lea", "rosi"], "crew_mess",
                  "Duc gives the day's orders. Who goes ashore, who works on the drive, how much power the day may cost."),
    "power_council": S("dinner", "Power council", ["chiara", "rosi", "sophia"], "crew_mess",
                       "Dinner by headlamp. What gets power tonight: fridge, watermaker, radio, or the guests' air conditioning?"),
    "guest_dinner": S("dinner", "Dinner with the guests", ["siri", "yasin", "chiara"], "aft_deck",
                      "Chiara serves a perfect dinner from nothing. Yasin complains, Siri apologises for him."),
    "alvas_bar": S("abend", "Alva's bar", ["sophia", "lea"], "alvas_bar",
                   "Evening in the village bar. Alva knows things, and sells diesel under the counter to people she likes.",
                   {"tag_ab": 2}),
    # Rosi: Rivalitaet -> Seite an Seite -> Werkstatt
    "rosi_diagnose": S("tag", "Inverter three", ["rosi"], "power_room",
                       "Rosi has opened the inverter cabinets. She wants nobody's help, least of all the officer's."),
    "rosi_night_shift": S("nacht", "Night shift", ["rosi"], "generator_room",
                          "Unit-01 coughs at three in the morning. Rosi lets Duc stay, and stops counting for a minute.",
                          {"vertrauen": ["rosi", 2]}),
    "rosi_workshop_name": S("abend", "The name of the workshop", ["rosi"], "workshop",
                            "Rosi tells Duc the name of her father's workshop in Catania. Then she asks for help, out loud.",
                            {"alle": [{"vertrauen": ["rosi", 4]}, {"gesehen": "rosi_night_shift"}]}),
    # Siri: kein Netz -> Knoten -> der Anruf
    "siri_no_signal": S("tag", "No signal", ["siri", "yasin"], "sun_deck",
                        "There is no internet aboard. Yasin panics about his content; Siri is quietly relieved and ashamed of it."),
    "siri_knots": S("tag", "The bowline", ["siri"], "swim_platform",
                    "Duc needs hands for the lines. Siri ties a perfect bowline without thinking, and remembers her father's pier.",
                    {"vertrauen": ["siri", 2]}),
    "siri_the_call": S("nacht", "The call", ["siri"], "solar_deck",
                       "One in the morning, her father's sweater, the call button. Duc is there when she presses it, or doesn't.",
                       {"alle": [{"vertrauen": ["siri", 4]}, {"uhr": ["siri_marke", ">=", 4]}]}),
    # Chiara: Kommando -> Kartentisch -> die Pruefung
    "chiara_command": S("tag", "Who has command", ["chiara"], "bridge",
                        "Holm gave command to the new man, not to Chiara after six seasons. She tests him, loudly, in front of the crew."),
    "chiara_chart_night": S("nacht", "Chart table", ["chiara"], "bridge",
                            "Chiara comes up at two with two coffees and a 'hypothetical' question about drift and current.",
                            {"vertrauen": ["chiara", 2]}),
    "chiara_exam": S("abend", "The retake", ["chiara"], "solar_deck",
                     "Chiara says it out loud: she failed the Yachtmaster theory. And asks Duc to teach her.",
                     {"alle": [{"vertrauen": ["chiara", 4]}, {"gesehen": "chiara_chart_night"}]}),
    # Sophia: Dorf -> Gefallen -> Manuskript
    "sophia_village": S("tag", "Cala d'Orsu", ["sophia"], "village_harbour",
                        "Sophia goes ashore to find diesel, parts and allies, and the village already seems to know her."),
    "sophia_favours": S("abend", "The book of favours", ["sophia"], "alvas_bar",
                        "Sophia trades favours for diesel and shows Duc how. Her notebook stays closed. Almost.",
                        {"vertrauen": ["sophia", 2]}),
    "sophia_manuscript": S("nacht", "M. J. Penrose", ["sophia"], "crew_mess",
                           "Two in the morning, a laptop, a manuscript. Sophia lets Duc read the first page.",
                           {"alle": [{"vertrauen": ["sophia", 4]}, {"gesehen": "sophia_favours"}]}),
    # Lea: Petru -> Rumpf -> Margot
    "lea_petru": S("tag", "The old fisherman", ["lea"], "village_harbour",
                   "Lea has found an old fisherman who knows the coast. She wants Duc to meet him, now."),
    "lea_hull_dive": S("nacht", "Night dive", ["lea"], "swim_platform",
                       "Lea wants to check the drive pods under the hull at night. Alone is against the rules. With Duc it isn't.",
                       {"vertrauen": ["lea", 3]}),
    "lea_margot": S("tag", "Petru's story", ["lea"], "petru_workshop",
                    "Petru tells the story of the Margot, and Lea goes very quiet.",
                    {"alle": [{"vertrauen": ["lea", 4]}, {"gesehen": "lea_petru"}]}),
    # Wendepunkte
    "storm_night": S("nacht", "Storm night", ["chiara", "sophia", "lea", "rosi", "siri"], "crew_corridor",
                     "A summer storm. The batteries are low, the watermaker is off, the crew moves together. Cabins are shared.",
                     {"tag_ab": 3}),
    "la_festa": S("abend", "La Festa", ["chiara", "sophia", "lea", "rosi", "siri"], "village_piazza",
                  "The village festival. The whole village, the whole crew. Who does Duc go with?", {"tag_ab": 5}),
}

MODUL["ereignisse"] = {
    "squall": {"text": "A squall comes over the hills. Lines, fenders, everyone on deck, and the panels give nothing for an hour.", "bedingung": {}},
    "yasin_live": {"text": "Yasin starts a livestream on the sun deck with the last mobile data in the bay.", "bedingung": {"nicht": {"uhr": ["yasin_video", ">=", 5]}}},
    "village_kids": {"text": "Three kids from the village row out in a dinghy and stare at the yacht.", "bedingung": {"tag_ab": 2}},
    "petru_fish": {"text": "Petru ties up alongside with a crate of fish and doesn't want money.", "bedingung": {"wert": ["ruf", ">=", 2]}},
    "elsa_visit": {"text": "Lieutenant Ferrandi's patrol boat comes alongside for an inspection.", "bedingung": {}},
}

# ======================================================================== MISSIONEN (17.10.2026)
# Wen Duc von Anfang an kennt (Crew und Gaeste, alle im Hangar an Tag 0 kennengelernt). Alle anderen - das Dorf - werden erst
# durch eine gemeinsame Szene "bekannt" und schalten dann ihre Missionen frei.
MODUL["bekannt_start"] = ["chiara", "sophia", "lea", "rosi", "siri", "toto", "yasin", "holm"]

# Feste Saetze der Auftraggeber (englisch, vertont wie Toto): [Gefuehl des Sprites, Satz].
# angebot = Mission vorstellen, erfolg/fehlschlag je 5 Varianten, patzer = natuerliche 1. Saetze passen zu JEDER
# Mission dieser Figur - die Einzelheiten stehen im deutschen Auftragstext darunter.
MODUL["job_zeilen"] = {
    "rosi": {
        "angebot": [["curiosity", "You've got clever hands, officer. Lend them to me for an hour - I'll owe you one. Maybe."],
                    ["neutral", "I need a second pair of eyes that doesn't faint at a wiring diagram. You're it."],
                    ["amusement", "Papa always said: never work alone, the machine gets ideas. Come. Help me."]],
        "erfolg": [["approval", "Look at that. Clean work. Papa would have offered you a job."],
                   ["joy", "Brava - bravo, sorry. You did it. I'm not crying, it's oil."],
                   ["admiration", "Hm. You're better at this than you let on, officer. Suspicious."],
                   ["amusement", "Fine. I'll call it a draw. You did eighty percent and I did the important twenty."],
                   ["gratitude", "Grazie. Really. I wasn't going to make it alone tonight."]],
        "fehlschlag": [["annoyance", "No, no, no - you don't hit it, you listen to it. Give me that."],
                       ["disappointment", "Half done is not done. But fine. Tomorrow."],
                       ["confusion", "How did you even make it worse? Never mind. I'll fix it."],
                       ["sadness", "It's not you. This boat is tired. So am I."],
                       ["disapproval", "Next time you ask before you improvise, capito?"]],
        "patzer": [["anger", "Madonna! You shorted it! Out. Out of my room, now."],
                   ["embarrassment", "...I'll pretend I didn't see that. You pretend too."]]},
    "chiara": {
        "angebot": [["excitement", "Duc! Perfect timing. I need someone with authority and two free hands. Go!"],
                    ["neutral", "Thirteen people, no power, and a list as long as the gangway. Take a piece of it?"],
                    ["amusement", "You look bored. That's dangerous. Here - make yourself useful."]],
        "erfolg": [["joy", "YES! That's how it's done! Somebody write this down!"],
                   ["pride", "See? Give me one competent officer and this boat runs itself."],
                   ["approval", "Done, and done properly. I'm almost impressed. Almost."],
                   ["admiration", "Okay, that was smooth. Don't let it go to your head, First Officer."],
                   ["gratitude", "Thank you. I mean it. You just saved my whole evening."]],
        "fehlschlag": [["annoyance", "Seriously? Fine. FINE. I'll do it myself, like always."],
                       ["disappointment", "That's... not what I asked for. But okay. We'll live."],
                       ["disapproval", "Rule one on my deck: you don't half-do things. Remember it."],
                       ["confusion", "Wait - how? It was a ten-minute job!"],
                       ["sadness", "Don't worry. Today nothing works. Not even you."]],
        "patzer": [["anger", "Are you KIDDING me?! Out of my way. Now."],
                   ["embarrassment", "Okay. Nobody saw this. Nobody. Understood?"]]},
    "sophia": {
        "angebot": [["curiosity", "I have a little problem, and you look like a man who enjoys little problems."],
                    ["amusement", "Come here. I'll tell you a secret - and then you'll do me a favour."],
                    ["neutral", "This needs someone they'll trust on sight. That would be you, not me."]],
        "erfolg": [["approval", "Beautifully done. You'd make a decent villain in one of my books."],
                   ["amusement", "Look at you. Charming the whole coast. I may have to steal that scene."],
                   ["admiration", "I watched you do it. Quietly. I'm keeping notes, you know."],
                   ["gratitude", "Thank you, Duc. That was worth more than you think."],
                   ["joy", "Ha! Perfect. Better than I planned it - and I always plan it."]],
        "fehlschlag": [["disappointment", "Hm. Not your finest chapter. We'll write a better one."],
                       ["confusion", "Odd. That should have worked. Someone's playing a different game."],
                       ["annoyance", "Well. Now they know we wanted it. That makes it harder."],
                       ["sadness", "Never mind. Some doors only open on the second knock."],
                       ["disapproval", "You were too direct. People here like to be asked twice."]],
        "patzer": [["embarrassment", "Oh dear. The whole village will have heard by dinner."],
                   ["anger", "Duc. That was the one thing I asked you not to do."]]},
    "lea": {
        "angebot": [["excitement", "Duc! I have an idea and it's either brilliant or really stupid. Want to find out?"],
                    ["curiosity", "Have you ever done this before? Me neither! Come on, it'll be fun!"],
                    ["joy", "Grab a mask and fins - or a screwdriver - I'm not sure yet which one we need."]],
        "erfolg": [["excitement", "We did it! We actually did it! High five - no, both hands!"],
                   ["joy", "That was the best hour of my whole week. Can we do it again tomorrow?"],
                   ["admiration", "You were amazing. Like, really. I'm telling Grandpa about you."],
                   ["gratitude", "Thank you for not laughing at me when I panicked for a second."],
                   ["pride", "Look at us. Proper sailors. Write it in the logbook!"]],
        "fehlschlag": [["sadness", "Oh no. It's okay. It's... mostly okay."],
                       ["confusion", "Wait, which way was it supposed to go? I'm so confused."],
                       ["disappointment", "Aw. I really thought we had it this time."],
                       ["nervousness", "Please don't tell Chiara. She'll make the face."],
                       ["optimism", "Okay! Failure is just practice with a sad ending. Next time!"]],
        "patzer": [["fear", "Duc! Are you okay?! Don't scare me like that!"],
                   ["embarrassment", "That... that was my fault too. Let's never speak of it."]]},
    "siri": {
        "angebot": [["neutral", "Can I ask you for something? Just us. No camera, no Yasin."],
                    ["curiosity", "You seem like someone who doesn't need an audience. I need one of those today."],
                    ["caring", "Would you help me? It's small. But it matters to me."]],
        "erfolg": [["joy", "Thank you. This is the first thing this week that felt like mine."],
                   ["gratitude", "You didn't have to do that. You did it anyway. I won't forget it."],
                   ["admiration", "You're good at this. At being... steady. It's rare."],
                   ["relief", "It worked. God. I can breathe again."],
                   ["amusement", "Look at us, doing something real. My followers would be so confused."]],
        "fehlschlag": [["sadness", "It's fine. Really. I'm used to things not working out."],
                       ["disappointment", "Oh. Well. It was a silly idea anyway."],
                       ["nervousness", "If Yasin hears about this, he'll make it a story. Please don't tell him."],
                       ["confusion", "I don't understand what went wrong. Do you?"],
                       ["caring", "Hey. Don't look like that. You tried. That's more than most."]],
        "patzer": [["fear", "Duc - your hand! Let me see. Don't move."],
                   ["embarrassment", "Okay, that's going on nobody's story. Ever."]]},
    "toto": {
        "angebot": [["amusement", "Comandante! A small job, a small envelope. Nobody asks questions. Va bene?"],
                    ["joy", "I have work, you have hands. God is a businessman, eh?"],
                    ["neutral", "Shh. Come closer. This is between you, me, and the potatoes."]],
        "erfolg": [["joy", "Bravissimo! You see? You were born on the wrong side of the law, Comandante."],
                   ["approval", "Clean like a church on Sunday. Here - your envelope."],
                   ["amusement", "My cousin will hear about you. He says nice things. Rarely."],
                   ["gratitude", "Grazie, fratello. I owe you a plate of my mother's genovese."],
                   ["pride", "That's how we do it in Napoli. Fast, quiet, and with style."]],
        "fehlschlag": [["nervousness", "Mamma mia... okay, okay. Nobody panics. I panic for both of us."],
                       ["disappointment", "Half job, half envelope. Business is business, eh?"],
                       ["annoyance", "Comandante, I said quietly. Quietly is the whole job."],
                       ["sadness", "My cousin will cry. Not for you. For the merchandise."],
                       ["confusion", "How? HOW? It was potatoes. Nobody looks at potatoes."]],
        "patzer": [["fear", "The Lieutenant's boat! Hide - no, act normal! Normal!"],
                   ["anger", "You want to send me back to Naples in handcuffs?!"]]},
    "yasin": {
        "angebot": [["pride", "Hey, First Officer! I'm making you an offer. Cash. Don't say I never support my team."],
                    ["amusement", "You want to earn some real money for once? Watch and learn, bro."],
                    ["neutral", "Quick job. I pay, you do it, everyone's happy. That's business."]],
        "erfolg": [["approval", "Respect, bro. That's the energy I'm looking for. Here, take it."],
                   ["joy", "Yes! Content! I filmed that, you're welcome."],
                   ["pride", "Told you. I only work with winners."],
                   ["amusement", "Not bad for a guy on a salary."],
                   ["joy", "Perfect. Siri, did you see? THAT's a team player."]],
        "fehlschlag": [["annoyance", "Seriously? I pay for results, not effort."],
                       ["disapproval", "This is why I don't hire locals. Or crew."],
                       ["disappointment", "Half the money. That's still more than you deserve."],
                       ["anger", "Bro. You had ONE job."],
                       ["confusion", "How do you mess that up? Genuinely asking."]],
        "patzer": [["disgust", "Ugh. Don't touch anything else. Ever."],
                   ["anger", "Do you know what that cost?! Do you?!"]]},
    "elsa": {
        "angebot": [["neutral", "Officer. I have a task, a budget, and no patience. Interested?"],
                    ["curiosity", "They say you can fix things. Let's see if that's true."],
                    ["approval", "You're useful. That's the highest thing I say about anyone. Here."]],
        "erfolg": [["approval", "Good. That goes in my report. The good part."],
                   ["admiration", "Efficient. I like efficient. Don't tell anyone I said that."],
                   ["amusement", "You did that faster than Ajaccio answers an email. Impressive."],
                   ["gratitude", "Merci. You made my day shorter. That's a gift."],
                   ["pride", "See? Rules work. When competent people follow them."]],
        "fehlschlag": [["disapproval", "That's not how it's done. There's a manual. Read it."],
                       ["annoyance", "Now I have to write that down. I hate writing things down."],
                       ["disappointment", "I expected better. Half pay, and we don't talk about it."],
                       ["confusion", "Explain to me what you just did. Slowly."],
                       ["neutral", "Fine. It's half done. Half is a number I can work with."]],
        "patzer": [["anger", "That's government property, officer. Was."],
                   ["disgust", "I'm writing you up. Mentally. In red."]]},
    "alva": {
        "angebot": [["joy", "O figliolu! Come, come, sit. I have a little something for you to do."],
                    ["amusement", "Everybody in Cala d'Orsu owes me something. Now it's your turn, handsome."],
                    ["curiosity", "You look like a man with free hands. Alva needs free hands."]],
        "erfolg": [["joy", "Bravu! A drink on the house - and a story about you all over the village by tonight."],
                   ["admiration", "Look at him! If you weren't a sailor, I'd keep you."],
                   ["gratitude", "Grazie, o figliolu. Alva remembers who helps her."],
                   ["amusement", "My father would have liked you. He liked everyone who worked for free."],
                   ["approval", "Perfect. Now the whole bar knows you're good with your hands."]],
        "fehlschlag": [["amusement", "Ahah, never mind! Half the men here can't do it either."],
                       ["disappointment", "Eh. Half done, half paid. That's Corsica."],
                       ["confusion", "Mamma, what did you do to it? It never made that noise before."],
                       ["caring", "Don't make that face. Sit, eat something, try again tomorrow."],
                       ["annoyance", "Now I have to call my cousin. He talks for an hour, every time."]],
        "patzer": [["anger", "Basta! Out, before you break the whole bar!"],
                   ["embarrassment", "Everybody saw. Everybody. You're famous now, o figliolu."]]},
    "petru": {
        "angebot": [["neutral", "Work."],
                    ["curiosity", "You. Come. Bring your eyes."],
                    ["approval", "The young one says you are not useless. We see."]],
        "erfolg": [["approval", "Good."],
                   ["admiration", "Hm. My father would have said: this one stays."],
                   ["gratitude", "Thank you. Take fish. Don't argue."],
                   ["joy", "Ha. Good. Very good."],
                   ["pride", "Like the old days. Good hands."]],
        "fehlschlag": [["disapproval", "No."],
                       ["disappointment", "Tomorrow. Again."],
                       ["neutral", "The sea is patient. Be like the sea."],
                       ["annoyance", "Too fast. Always too fast, you people."],
                       ["sadness", "Hm. It happens. Also to me."]],
        "patzer": [["anger", "Out of my workshop."],
                   ["disgust", "Sixty years. Nobody ever did that."]]},
    "casanova": {
        "angebot": [["excitement", "Officer! Destiny has chosen you! Also, I have nobody else. Will you help?!"],
                    ["pride", "A task worthy of a hero! Or at least of a man with two hands!"],
                    ["joy", "My village needs you! Dramatic pause! ...It's a small thing, actually."]],
        "erfolg": [["excitement", "MAGNIFICENT! The village will sing of this! Possibly! I'll write the song!"],
                   ["joy", "Victory! I knew it! I always know it, I'm the mayor!"],
                   ["admiration", "You have the soul of a festa! I am almost moved to tears!"],
                   ["gratitude", "Thank you, brave officer! You'll get a medal. A small one. Made of cardboard."],
                   ["pride", "Cala d'Orsu wins again! With your help! Mostly with mine!"]],
        "fehlschlag": [["sadness", "Noooo! Tragedy! ...Okay, a small tragedy. A season-two tragedy."],
                       ["disappointment", "The plot twist nobody wanted! But every hero falls once!"],
                       ["confusion", "Wait. That's not how it was supposed to go in my head."],
                       ["optimism", "Fear not! Every great story needs a setback in episode three!"],
                       ["annoyance", "The grandchildren will talk about this. Badly."]],
        "patzer": [["fear", "AAAH! Everybody stay calm! I am calm! I am VERY calm!"],
                   ["anger", "This is an outrage! A betrayal! ...Are you hurt, at least?"]]},
}
# Missionsausbau 18.10.2026: Lola (Aussie-Slang, warm, verpeilt) und Megan (Anime-Bosswoman, Schach, Haie, Feuer)
MODUL["job_zeilen"]["lola"] = {
    "angebot": [["excitement", "Captain! I've got a plan. It's mostly vibes, but the vibes are strong. You in?"],
                ["curiosity", "Okay, don't laugh, but I need help with something and you've got the competent face."],
                ["joy", "Heaps of good news: I have an idea. Bad news: it needs someone who reads instructions. That's you."]],
    "erfolg": [["joy", "YES! Captain! That's the best thing that's happened all week, and somebody found my phone today!"],
               ["admiration", "Mate. You're unreal. I'd marry you, but I'd lose the ring by Tuesday."],
               ["gratitude", "Thanks, Captain. Really. I'd have stuffed that up completely. Like, completely."],
               ["amusement", "We're a team now. Lola and the Captain. No, Captain and Lola. No - Lola and the Captain."],
               ["love", "Come here. Hug. No arguing. You earned a hug and a muffin. The muffin's mostly okay."]],
    "fehlschlag": [["amusement", "Okay, so that went sideways. Like, properly sideways. Tomorrow, yeah?"],
                   ["disappointment", "Aw. Nah, it's fine. It's fine! It's a bit not fine. Tomorrow."],
                   ["confusion", "Wait, was that my fault or yours? Doesn't matter. Probably mine. Tomorrow."],
                   ["optimism", "No worries, Captain. The second go is always the good one. Ask my last three jobs."],
                   ["embarrassment", "Let's just... never tell Chiara about this. Deal? Deal."]],
    "patzer": [["fear", "Oh no. Oh no no no. Is it on fire? It's a bit on fire. Okay. Okay!"],
               ["amusement", "That's the funniest disaster I've ever seen, and I've seen me cook drunk."]]}
MODUL["job_zeilen"]["megan"] = {
    "angebot": [["neutral", "First Officer. I have a task. You have a deadline. Shall we skip the part where you complain?"],
                ["amusement", "A little job for you. Think of it as a chess problem. White to move. You're white."],
                ["pride", "I need someone competent. Statistically, that's you this week. Don't let it go to your head."]],
    "erfolg": [["amusement", "Annoyingly good. I'll have to find something harder for you. Mwahaha. That was a joke."],
               ["approval", "Checkmate. Clean, quick, no blood on the carpet. I approve."],
               ["admiration", "Well, well. The shark has teeth. Noted, First Officer. Noted."],
               ["pride", "That's the kind of work I can put in front of a board. Don't tell them it was you."],
               ["gratitude", "Thank you. I don't say that often. Remember the date."]],
    "fehlschlag": [["disapproval", "That was a pawn sacrifice without a plan, First Officer. Try again."],
                   ["annoyance", "Disappointing. Not fatal. Disappointing. Tomorrow I expect better."],
                   ["disappointment", "Hm. I've seen interns do worse. Not many."],
                   ["neutral", "We'll call that a test run. The real one is tomorrow. No pressure. Some pressure."],
                   ["amusement", "Oh, that's adorable. You tried. Now do it properly, aye?"]],
    "patzer": [["anger", "Dinnae... Do NOT ever send me a result like that again. Ever. Is that clear?"],
               ["amusement", "Spectacular. I'm framing this as a warning for the whole fleet."]]}
for _pid, _z in MODUL["job_zeilen"].items():
    assert len(_z["erfolg"]) == 5 and len(_z["fehlschlag"]) == 5, _pid
