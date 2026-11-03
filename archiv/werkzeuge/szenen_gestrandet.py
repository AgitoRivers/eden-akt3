# -*- coding: utf-8 -*-
r"""Szenen-Vorrat fuer eden_yacht_gestrandet (16.10.2026) -> module\eden_yacht_gestrandet\szenen.json.

Der automatische Showrunner (kern\showrunner.py) baut daraus jeden Tag den Plan. Hier steht NUR Inhalt:
- pool:      waehlbare Szenen mit Phase, Tagen, Bedingung, Gewicht, Bogen-Stufe, Uhr
- vorlagen:  Wendepunkte, die der Code je Stand zusammensetzt (Sturm, Konfrontation, Festa, Point of no return,
             letzte Nacht, Feuer, Finale, Epilog)
- Steuerung: Tagestexte, Wetter, Ressourcen-Takt, Geheimnisse, Standard-Wuensche
Grenzen ("wie weit sie geht") und Geheimnisse fuellt der Showrunner selbst; Szenen geben nur, was sie wollen.
Platzhalter in Texten: {strom} {diesel} {wetter} {partner}.

    python szenen_gestrandet.py     schreibt szenen.json (alte als .bak-<Zeit>)
"""
import json, os, shutil, time

ZIEL = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "module", "eden_yacht_gestrandet", "szenen.json")
CREW = ["chiara", "sophia", "lea", "rosi"]


def A(wenn, *folgen):
    return {"wenn": wenn, "folgen": list(folgen)}


def W(wert, d):
    return {"wert": wert, "delta": d}


def U(uhr, d=1):
    return {"uhr": uhr, "delta": d}


def C(text):
    return {"codex": text}


def F(flag):
    return {"flag": flag}


def I(item):
    return {"item": item}


def S(id, phase, tage, titel, ort, anwesend, zeit, lage, frage, figuren, ausgaenge, art="alltag", frau=None, stufe=None,
      storylet=None, bed=None, gewicht=1.0, uhr=None, einmalig=True, max_zuege=8, wahlmoment=None, begruendung=None,
      varianten=None):
    s = {"titel": titel, "ort": ort, "anwesend": anwesend, "zeit": zeit, "ausgangslage": lage, "frage": frage,
         "figuren": figuren, "ausgaenge": ausgaenge, "max_zuege": max_zuege}
    if begruendung:
        s["begruendung_ort"] = begruendung
    if wahlmoment:
        s["wahlmoment"] = wahlmoment
    e = {"id": id, "phase": phase, "tage": tage, "art": art, "szene": s, "einmalig": einmalig, "gewicht": gewicht}
    for k, v in (("frau", frau), ("stufe", stufe), ("storylet", storylet), ("bedingung", bed), ("uhr", uhr),
                 ("varianten", varianten)):
        if v is not None:
            e[k] = v
    return e


def WM(frage, *optionen, nach=2):
    return {"nach_zug": nach, "frage": frage, "optionen": list(optionen)}


def O(text, handlung, folgen, check=None, fehl=None):
    o = {"text": text, "handlung": handlung, "folgen": folgen}
    if check:
        o["check"], o["folgen_fehlschlag"] = check, fehl or []
    return o


POOL = []

# ======================================================================== PFLICHT: Fruehstueck
POOL += [
    S("morning_bay", "fruehstueck", [2, 2], "Morning in the bay", "crew_mess", ["chiara", "sophia", "lea", "rosi"], "07:30",
      "Day two in the bay of Cala d'Orsu. Coffee comes from a camping stove, because the induction hob eats too much power. Rosi reads out the battery level like a weather report: {strom} out of ten. Sophia wants to go ashore for diesel. Lea already has the tender keys in her hand. Chiara wants a schedule, on paper, now.",
      "Who does Duc send ashore - and who stays with him on the boat?",
      {"chiara": "Get a proper plan for the day and be the one who writes it down.",
       "sophia": "Go ashore today and come back with diesel and a friend in the village.",
       "lea": "Drive the tender, see the village, be useful.",
       "rosi": "Keep everyone away from her inverters and get coffee."},
      [A("Duc sends Sophia and Lea ashore with the tender.", W("vertrauen.lea", 1), W("ruf", 1)),
       A("Duc keeps Rosi with him on the drive.", W("vertrauen.rosi", 1), U("reparatur", 1)),
       A("Duc lets Chiara write the schedule.", W("vertrauen.chiara", 1), W("moral", 1))], max_zuege=6),
    S("storm_warning", "fruehstueck", [3, 3], "Storm warning", "bridge", ["chiara", "rosi", "lea"], "07:00",
      "The bridge, seven in the morning. The VHF crackles: a summer storm from the west, tonight, gusts up to forty knots. The sky over the hills is still blue and innocent. Chiara has the forecast printed out. Rosi shakes her head at the battery curve. Lea is excited and trying very hard not to show it.",
      "How does Duc prepare the boat - and the crew - for the night?",
      {"chiara": "Turn the storm into a drill she can run perfectly.",
       "rosi": "Save every amp for tonight. No discussion.",
       "lea": "Get the job of checking the anchor chain, with Duc."},
      [A("Duc puts a second anchor out.", U("katastrophe", -1), W("vertrauen.lea", 1)),
       A("Duc orders everything off except the anchor alarm.", W("strom", 1), W("vertrauen.rosi", 1)),
       A("Duc gives each of them a clear job for the storm.", W("moral", 1), W("vertrauen.chiara", 1))], max_zuege=6,
      gewicht=10.0),     # Plot: bereitet die Sturmnacht vor - schlaegt die wechselnden Fruehstuecke (17.10.2026)
    S("mayors_visit", "fruehstueck", [5, 5], "The mayor's visit", "aft_deck", ["chiara", "sophia", "casanova"], "08:30",
      "Madame Casanova, mayor of Cala d'Orsu, comes aboard in a straw hat with two village kids carrying her folders. Tonight is the festa. She wants the Eden Rise lit up in the bay as the attraction of the year, every light on, photos for the regional paper. Chiara offers coffee. Sophia already smells a deal.",
      "What does Duc give the mayor - and what does he get for it?",
      {"chiara": "Keep the boat presentable and the mayor happy without promising the impossible.",
       "sophia": "Turn the mayor's wish into diesel, help and goodwill for the crew.",
       "casanova": "Get the lit-up yacht for her festa, and the photo for the paper."},
      [A("Duc agrees to light up the yacht for the festa.", W("ruf", 2), W("strom", -2), I("festa_invite")),
       A("Duc offers a smaller show: deck lights only, if the village helps with diesel.", W("ruf", 1), W("diesel", 1), W("vertrauen.sophia", 1), I("festa_invite")),
       A("Duc declines.", W("ruf", -1))], max_zuege=6, gewicht=10.0),     # Plot: Festa-Einladung
    S("last_morning", "fruehstueck", [7, 7], "Last morning", "crew_mess", ["chiara", "sophia", "lea", "rosi"], "07:00",
      "The seventh morning. Everyone knows today decides it. Nobody says it. Chiara made real coffee, on the last good power, and rates it a ten for the first time all season. Rosi has oil on her face and hasn't slept. Lea has drawn the bay in her logbook, every boat, every house. Sophia just looks at them all, as if memorising.",
      "What does Duc say to his crew on the last morning?",
      {"chiara": "Pretend this is a normal morning, and fail.",
       "sophia": "Remember this, exactly, for later.",
       "lea": "Show Duc the drawing of the bay.",
       "rosi": "Hear that today the plan is hers too."},
      [A("Duc thanks the crew, honestly.", W("moral", 2)),
       A("Duc gives a clear plan for the last day.", W("moral", 1), W("vertrauen.chiara", 1))], max_zuege=6),
]

# ======================================================================== PFLICHT: Dinner
POOL += [
    S("petrus_fish", "dinner", [2, 2], "Petru's fish", "crew_mess", ["chiara", "lea", "rosi"], "20:00",
      "An old fisherman tied up alongside at sunset and left a crate of red mullet without asking for money. Chiara grills it on the deck barbecue, the only cooking that costs no power. The crew mess smells of fish and lemon. Rosi says the fridge can hold half of it. Lea wants to take the other half back to the village as thanks.",
      "What does Duc do with the fish - and with the evening?",
      {"chiara": "Make the best dinner of the season out of nothing, and get a ten from someone.",
       "lea": "Take half the fish back to the village, tonight, with Duc.",
       "rosi": "Eat. Then guard the fridge's power budget."},
      [A("Duc sends half the fish back to the village as thanks.", W("ruf", 1), W("vertrauen.lea", 1)),
       A("Duc praises Chiara's cooking.", W("vertrauen.chiara", 1)),
       A("Duc keeps the fridge running for the fish.", W("strom", -1), W("moral", 1))], max_zuege=6),
    S("before_the_storm", "dinner", [3, 3], "Before the storm", "crew_mess", ["chiara", "rosi", "sophia"], "20:00",
      "Cold dinner: bread, cheese, the last tomatoes. Everything is stowed, the portholes are screwed shut, the wind is already singing in the rigging. The lights are off to save power; three headlamps on the table. Sophia tells a ghost story about the bridge wing. Chiara tells her to stop, too quickly.",
      "Does Duc keep the crew calm - and who needs it most?",
      {"chiara": "Stay in control and make sure nobody notices she hates storms.",
       "rosi": "Check the battery app every two minutes.",
       "sophia": "Keep everyone laughing until it starts."},
      [A("Duc tells a calm, true story from another storm.", W("moral", 1)),
       A("Duc notices Chiara is afraid and says nothing in front of the others.", W("vertrauen.chiara", 1))], max_zuege=6),
    S("quiet_table", "dinner", [4, 4], "The quiet table", "crew_mess", ["chiara", "sophia", "lea"], "20:00",
      "The day after the storm, the day of the accusation. The crew mess is too quiet. Everyone is polite. Lea is sanding salt off a fender at the table instead of eating. Sophia keeps refilling glasses that are already full. Chiara rates nothing at all.",
      "Can Duc bring the crew back together tonight?",
      {"chiara": "Get through dinner without saying what she thinks of this morning.",
       "sophia": "Fix the mood, the way she always fixes everything.",
       "lea": "Ask out loud the question everyone avoids."},
      [A("Duc names the tension and asks for one honest word from everyone.", W("moral", 2)),
       A("Duc makes them laugh.", W("moral", 1), W("begehren.sophia", 1))], max_zuege=6,
      varianten=[{"wenn": {"flag": "geschwiegen"}, "szene": {"ausgangslage": "The day after the storm. Duc chose to accuse nobody this morning, and the cause of the blackout is still a ghost in the room. Everyone is polite. Lea sands salt off a fender at the table instead of eating. Sophia refills full glasses. Chiara rates nothing at all."}}]),
    S("getting_ready", "dinner", [5, 5], "Getting ready", "crew_corridor", ["chiara", "lea", "siri"], "19:30",
      "The narrow crew corridor has become a dressing room. Chiara irons a dress on a towel on the floor. Lea has never been to a festa and asks what people wear. Siri, the guest, the influencer, sits on the stairs with a make-up bag and does Lea's eyeliner, very carefully, tongue between her teeth. Duc has to get past all of them.",
      "Does Duc get through the corridor - and with what promise for tonight?",
      {"chiara": "Look perfect tonight and make sure Duc sees it.",
       "lea": "Find out if she looks good, from Duc, without asking.",
       "siri": "Be one of the girls for an evening, not a brand."},
      [A("Duc tells Lea she looks great.", W("vertrauen.lea", 1)),
       A("Duc tells Chiara she looks stunning.", W("begehren.chiara", 1)),
       A("Duc thanks Siri for helping the crew.", W("vertrauen.siri", 1), W("rivalitaet.chiara_siri", -1))], max_zuege=6),
    S("last_supper", "dinner", [6, 6], "The last supper", "aft_deck", ["chiara", "sophia", "siri"], "20:30",
      "The long table on the aft deck, set as if guests were coming. Nobody is. Chiara did it anyway, with candles instead of lights. Sophia is quiet. Siri sits with the crew for once, not with Yasin. Tomorrow is the last day, whatever happens.",
      "What does each of them want from Duc before tomorrow?",
      {"chiara": "One last perfect evening, rated honestly.",
       "sophia": "Say something true, for once, without a joke around it.",
       "siri": "Sit with real people one more evening."},
      [A("Duc asks each of them what they will do after this week.", W("moral", 1), W("vertrauen.sophia", 1)),
       A("Duc raises a glass to the crew and the guests.", W("moral", 1), W("vertrauen.siri", 1))], max_zuege=6),
    S("last_dinner", "dinner", [7, 7], "The last dinner", "crew_mess", ["chiara", "rosi", "lea"], "19:30",
      "Last dinner before the last night. Nobody is hungry. Rosi eats cereal from the box at the table and nobody tells her off. Lea counts the days in her logbook again: seven. Chiara stands up, sits down, stands up again.",
      "Who does Duc want next to him tonight?",
      {"chiara": "Say something that matters before it is too late, and not manage it.",
       "rosi": "Not talk about anything. Be near the officer.",
       "lea": "Ask Duc what happens to all of them after this."},
      [A("Duc tells the crew he would sail with them again.", W("moral", 2)),
       A("Duc sits down next to Rosi and steals her cereal.", W("begehren.rosi", 1))], max_zuege=6),
]

# ======================================================================== PFLICHT: Nacht (Wachen; Bogen-Naechte konkurrieren)
POOL += [
    S("second_watch", "nacht", [2, 2], "Second watch", "bridge", ["$abend"], "02:00",
      "Bridge, two in the morning. The anchor alarm glows green, the bay is black glass. Battery: {strom} out of ten. Whoever Duc spent the evening with comes up the stairs with two cups of tea and the excuse that she couldn't sleep.",
      "Does Duc let her stay until the watch ends?",
      {"*": {"will": "Stay a little longer than she should and find out what the commander is really like."}},
      [A("She stays until the end of the watch.", W("energie", -1)),
       A("Duc tells her something true about himself.", W("energie", 0))],
      begruendung="Whoever Duc spent the evening with comes up to the bridge during his watch."),
    S("watch_after", "nacht", [4, 4], "Watch after the storm", "bridge", ["$abend"], "01:30",
      "The bridge after the storm and after the accusation. The sea is calm again, too calm. Whoever Duc spent the evening with comes up without an excuse this time. She just sits down in the captain's chair, as if it were hers.",
      "What does she need from Duc tonight?",
      {"*": {"will": "Talk about the morning, or about anything but the morning."}},
      [A("She stays until the end of the watch.", W("energie", -1))],
      begruendung="Whoever Duc spent the evening with comes to the bridge."),
    S("after_the_festa", "nacht", [5, 5], "After the festa", "solar_deck", ["$abend"], "01:00",
      "One in the morning. The festa music still drifts over the water from the village. Duc and the woman he went with came back in the tender, the last of the crew. Now they are up on the solar deck under the dark panels, shoes in hand, salt on the skin.",
      "Does the evening end here?",
      {"*": {"will": "Not let the evening end yet."}},
      [A("They kiss.", W("energie", -1)),
       A("She stays the night.", W("energie", -1))],
      begruendung="The woman Duc went to the festa with comes up to the solar deck with him."),
]

# ======================================================================== BOEGEN der fuenf Frauen (Storylets aus modul.json)
POOL += [
    # Rosi
    S("rosi_diagnose", "tag", [1, 7], "Inverter three", "power_room", ["rosi"], "10:00",
      "Power room. Every inverter cabinet is open, cables hang out like guts. Rosi lies half inside cabinet three with a headlamp, coverall tied at the waist. A smell of hot plastic in the air. She hears Duc come in and does not slide out.",
      "Does Rosi let Duc work next to her - or send him away?",
      {"rosi": "Find the fault alone and prove the drive is her territory; test whether the officer knows anything."},
      [A("Duc works next to Rosi as an equal and lets her lead.", W("vertrauen.rosi", 1), U("reparatur", 1)),
       A("Duc finds something Rosi missed and doesn't gloat.", W("begehren.rosi", 1), U("reparatur", 1))],
      art="herz", frau="rosi", stufe=1, storylet="rosi_diagnose", uhr="reparatur"),
    S("rosi_night_shift", "nacht", [2, 6], "Night shift", "generator_room", ["rosi"], "03:00",
      "Three in the morning. A cough from the generator room. Rosi kneels in front of Unit-01, coverall tied at the waist, bandana crooked, talking to it. 'Don't you dare die on me.' She hears Duc and doesn't turn around. 'Pass me the thirteen.'",
      "Does Rosi let Duc stay - and stop counting for a minute?",
      {"rosi": "Keep Unit-01 alive tonight; let the officer stay without admitting she wants him to."},
      [A("Duc stays and works with her until the generator runs clean.", W("vertrauen.rosi", 1), U("reparatur", 1)),
       A("Rosi talks about her father.", W("begehren.rosi", 1))],
      art="herz", frau="rosi", stufe=2, storylet="rosi_night_shift", uhr="reparatur", gewicht=1.5),
    S("rosi_workshop_name", "abend", [3, 7], "The name of the workshop", "workshop", ["rosi"], "22:30",
      "The workshop, one lamp, the whiteboard with the score. Rosi sits on the workbench and isn't reading her manga. She says the name of her father's workshop in Catania out loud, for the first time on this boat. Then she asks Duc for help with the drive. Out loud. Without calling it a draw.",
      "What does Duc do with the first time Rosi asks for help?",
      {"rosi": "Ask for help without losing, and see what he does with it."},
      [A("Duc helps her and lets her keep the lead.", W("vertrauen.rosi", 1), U("reparatur", 2), F("rosi_stufe3")),
       A("Rosi admits the rivalry was never about the repairs.", W("begehren.rosi", 2))],
      art="herz", frau="rosi", stufe=3, storylet="rosi_workshop_name", uhr="reparatur", gewicht=1.5),
    # Siri
    S("siri_no_signal", "tag", [1, 7], "No signal", "sun_deck", ["siri", "yasin"], "13:00",
      "Sun deck. No internet aboard, the satellite link is off to save power. Yasin walks in circles holding his phone to the sky and swears in French. Siri sits on a sunbed, phone face down, looking at the bay. Duc comes up to check the panels.",
      "Does Siri admit she is relieved - and does Yasin notice?",
      {"siri": "Apologise for Yasin and not show how good it feels that nobody can post anything.",
       "yasin": "Get the satellite link back on for his content, today."},
      [A("Duc refuses to switch the satellite link on for Yasin.", W("vertrauen.siri", 1), U("yasin_video", 1)),
       A("Siri says something true about herself.", U("siri_marke", 1), W("begehren.siri", 1))],
      art="herz", frau="siri", stufe=1, storylet="siri_no_signal"),
    S("siri_knots", "tag", [2, 7], "The bowline", "swim_platform", ["siri"], "15:00",
      "Swim platform, the stern lines need doubling before the wind turns. Duc is short of hands and Siri is the only one there. She takes the rope without thinking, and her fingers tie a perfect bowline. She stares at it. 'Pappa taught me that. On the pier. I was six.'",
      "What does Duc make of the island girl under the brand?",
      {"siri": "Be useful with her hands for once, and not cry about her father in front of him."},
      [A("Duc lets her do the lines with him.", W("vertrauen.siri", 1), U("siri_marke", 1)),
       A("Siri talks about the island and her father.", W("begehren.siri", 1), U("siri_marke", 1))],
      art="herz", frau="siri", stufe=2, storylet="siri_knots"),
    S("siri_the_call", "nacht", [3, 7], "The call", "solar_deck", ["siri"], "01:00",
      "One in the morning, the solar deck. Siri sits under the dark panels in her father's chunky wool sweater with the blue stars, wool socks, hair in a loose braid, no make-up. Her phone glows: 'Pappa', the call button untouched. She doesn't hide it when Duc comes up.",
      "Does Siri press the button - and is Duc there when she does?",
      {"siri": "Find the courage to call her father, and maybe to end it with Yasin."},
      [A("Siri calls her father.", W("vertrauen.siri", 2), U("siri_marke", 2), F("vater_angerufen")),
       A("Siri decides to end it with Yasin.", F("siri_frei"), U("siri_marke", 2))],
      art="herz", frau="siri", stufe=3, storylet="siri_the_call", gewicht=1.5),
    # Chiara
    S("chiara_command", "tag", [2, 7], "Who has command", "bridge", ["chiara"], "11:00",
      "The bridge. Chiara comes up with a clipboard and a list of eleven things that are wrong with Duc's plan, out loud. Six seasons on this boat. Holm gave the command to the new man. She is testing him, and both of them know it.",
      "Does Duc pass Chiara's test - without beating her down?",
      {"chiara": "Find out if he deserves the command; get one of her points accepted."},
      [A("Duc takes one of Chiara's points and changes his plan.", W("vertrauen.chiara", 1), W("moral", 1)),
       A("Duc asks Chiara to run the boat with him, not under him.", W("begehren.chiara", 1))],
      art="herz", frau="chiara", stufe=1, storylet="chiara_command"),
    S("chiara_chart_night", "nacht", [2, 6], "Chart table", "bridge", ["chiara"], "02:00",
      "Two in the morning. Chiara comes up with two coffees nobody ordered and an old navy jacket far too big for her. She puts one cup next to the chart. 'Hypothetically. Current sets east at two knots, the boat drifts for six hours. Where are we?'",
      "Does Duc answer the hypothetical question - and see what's behind it?",
      {"chiara": "Learn what she failed without saying that she failed."},
      [A("Duc works the drift problem with her, step by step.", W("vertrauen.chiara", 1)),
       A("Chiara stays until dawn.", W("begehren.chiara", 1), W("energie", -1))],
      art="herz", frau="chiara", stufe=2, storylet="chiara_chart_night", gewicht=1.5),
    S("chiara_exam", "abend", [3, 7], "The retake", "solar_deck", ["chiara"], "22:30",
      "The solar deck, the boat dark. Chiara sits with her grandfather's brass sextant in her lap and says it, flat, without a score: 'I failed the theory. April. Nobody knows.' Then, very quietly: 'Teach me. Please.'",
      "What does Duc do with Chiara's secret?",
      {"chiara": "Say it out loud once, ask for help once, and survive it."},
      [A("Duc promises to teach her and starts right now with a star sight.", W("vertrauen.chiara", 2)),
       A("Chiara lets him hold her.", W("begehren.chiara", 1))],
      art="herz", frau="chiara", stufe=3, storylet="chiara_exam", gewicht=1.5),
    # Sophia
    S("sophia_village", "tag", [1, 7], "Cala d'Orsu", "village_harbour", ["sophia", "elsa"], "11:30",
      "The harbour of Cala d'Orsu. Sophia walks Duc along the quay, linen and a headscarf, greeting people she cannot possibly know yet. At the coast-guard post, Lieutenant Elsa Ferrandi leans against her patrol boat, sunglasses on, a clipboard under her arm: a yacht without a drive is a hazard in her waters.",
      "Does Duc win the lieutenant over - and how much of it is Sophia's work?",
      {"sophia": "Get anchoring permission, a name for diesel and a friend in the village by lunch.",
       "elsa": "Do it by the book, test the new commander, and find out who on that yacht smuggles."},
      [A("Elsa grants anchoring permission.", W("ruf", 1), W("vertrauen.sophia", 1)),
       A("Elsa mentions Alva's bar for diesel.", C("Elsa: Für Diesel fragt man Alva, in der Bar am Hafen – aber das hast du nicht von mir."))],
      art="herz", frau="sophia", stufe=1, storylet="sophia_village"),
    S("sophia_favours", "abend", [2, 7], "The book of favours", "alvas_bar", ["sophia", "alva"], "22:00",
      "Alva's bar, the only one in the village. Sophia drinks myrtle liqueur with Alva as if they were cousins, and somewhere between the second and third glass she trades a favour against a canister of diesel. She shows Duc how, without showing him anything. Her brown leather notebook stays closed. Almost.",
      "Does Duc learn Sophia's trick - or see what's in the notebook?",
      {"sophia": "Get diesel, teach Duc the game, keep the notebook closed.",
       "alva": "Sell diesel only to people she likes, and find out if she likes this officer."},
      [A("Alva sells them diesel.", W("diesel", 1), W("ruf", 1)),
       A("Sophia lets Duc see a page of the notebook.", W("vertrauen.sophia", 1), W("begehren.sophia", 1))],
      art="herz", frau="sophia", stufe=2, storylet="sophia_favours"),
    S("sophia_manuscript", "nacht", [3, 7], "M. J. Penrose", "crew_mess", ["sophia"], "02:00",
      "Two in the morning, the crew mess, one lamp. Sophia in silk pyjamas and reading glasses, a laptop open. She doesn't close it when Duc comes in. On the screen: Chapter One, by M. J. Penrose. 'Fourteen rejections,' she says. 'Read the first page. Then lie to me.'",
      "Does Duc read - and tell her the truth?",
      {"sophia": "Let one person see who she is, and survive the verdict."},
      [A("Duc reads the page and tells her honestly what he thinks.", W("vertrauen.sophia", 2), F("manuskript_gelesen")),
       A("Sophia lets him stay.", W("begehren.sophia", 1))],
      art="herz", frau="sophia", stufe=3, storylet="sophia_manuscript", gewicht=1.5),
    # Lea
    S("lea_petru", "tag", [2, 7], "The old fisherman", "village_harbour", ["lea", "petru"], "10:30",
      "The harbour. Lea runs up to Duc, out of breath, logbook under her arm. She has found an old fisherman who knows every rock on this coast and has a workshop full of parts. Petru stands behind her, says nothing, and looks at Duc like he is weighing a fish.",
      "Does Duc win Petru over - with Lea's help?",
      {"lea": "Make Duc and Petru like each other, now.",
       "petru": "Find out if this young officer is worth his time."},
      [A("Petru offers the key to his workshop.", I("petru_key"), W("ruf", 1)),
       A("Duc lets Lea do the talking.", W("vertrauen.lea", 1))],
      art="herz", frau="lea", stufe=1, storylet="lea_petru", uhr="reparatur"),
    S("lea_hull_dive", "nacht", [2, 6], "Night dive", "swim_platform", ["lea"], "23:30",
      "Swim platform, near midnight. Lea is already in her wetsuit, a torch on her wrist. She wants to check the drive pods under the hull, now, while the water is calm. Alone is against the rules. With Duc, it isn't.",
      "Does Duc dive with her - and what do they find down there?",
      {"lea": "Dive tonight, with him, and show him the sea at night."},
      [A("Duc dives with Lea and they check the pods together.", W("vertrauen.lea", 1), U("reparatur", 1)),
       A("Lea tells Duc about her grandfather's wreck.", W("begehren.lea", 1))],
      art="herz", frau="lea", stufe=2, storylet="lea_hull_dive", gewicht=1.5),
    S("lea_margot", "tag", [3, 7], "Petru's story", "petru_workshop", ["lea", "petru"], "14:00",
      "Petru's workshop, dust in the light. While he fixes something for the Eden Rise, the old man tells the story of the Margot, the schooner that sank off the Esterel in 1924 with a strongbox. Lea goes very quiet. Then she opens her logbook and shows him her grandfather's handwriting.",
      "What does Lea dare to say - and what does Petru know?",
      {"lea": "Find out if her grandfather was right, and not cry in front of two men.",
       "petru": "Decide whether this girl deserves what he knows."},
      [A("Petru marks a place on Lea's chart.", F("margot_hinweis"), W("vertrauen.lea", 1)),
       A("Lea hugs Duc.", W("begehren.lea", 1))],
      art="herz", frau="lea", stufe=3, storylet="lea_margot", gewicht=1.5),
]

# ======================================================================== PLOT: Reparatur, Rettung, Diesel, Strom
POOL += [
    S("petru_parts", "tag", [2, 7], "Spare parts", "petru_workshop", ["rosi", "petru"], "13:00",
      "Petru's workshop. Rosi walks in, sees the shelves of old parts, and forgets to be rude. The old fisherman and the young engineer circle each other like two cats. Somewhere on these shelves is an inverter part that might fit.",
      "Do Rosi and Petru find the part - and does Duc keep the peace?",
      {"rosi": "Find a part that fits and not admit an old fisherman knows things.",
       "petru": "See whether this girl knows her trade."},
      [A("They find a part that fits.", U("reparatur", 2)),
       A("Rosi and Petru end up laughing together.", W("vertrauen.rosi", 1), W("ruf", 1))],
      art="plot", uhr="reparatur", gewicht=1.2),
    S("unit01_trial", "tag", [3, 7], "Unit-01 under load", "generator_room", ["rosi"], "15:00",
      "The generator room. Rosi wants to test the repaired drive under real load with Unit-01, and that costs diesel. {diesel} canister(s) left. She has her hand on the start switch and looks at Duc.",
      "Does Duc spend the diesel on the test?",
      {"rosi": "Run the test, now, with him there."},
      [A("They run the test and the drive turns.", U("reparatur", 2), W("diesel", -1)),
       A("Duc saves the diesel for later.", W("vertrauen.rosi", -1))],
      art="plot", uhr="reparatur", bed={"alle": [{"uhr": ["reparatur", ">=", 4]}, {"wert": ["diesel", ">=", 1]}]}, gewicht=1.4),
    S("drive_trial", "tag", [5, 7], "The first metres", "bridge", ["rosi", "chiara"], "11:00",
      "The bridge. Rosi on the radio from the power room, Chiara at the throttle, Duc between them. The drive is together again, more or less. One test: lift the anchor, ten metres forward, ten back.",
      "Does the Eden Rise move under her own power?",
      {"rosi": "Prove the drive works, with the whole crew watching.",
       "chiara": "Steer the first metres herself."},
      [A("The Eden Rise moves under her own power.", U("reparatur", 2), W("moral", 2)),
       A("Duc lets Chiara steer.", W("vertrauen.chiara", 1))],
      art="plot", uhr="reparatur", bed={"uhr": ["reparatur", ">=", 6]}, gewicht=1.8),
    S("radio_ajaccio", "abend", [2, 6], "Radio to Ajaccio", "bridge", ["chiara"], "21:00",
      "The bridge. The long-range radio costs power by the minute. Chiara sits at it with the headset on, calling the harbour office in Ajaccio again: a tug, any tug. Static, a bored voice, a form. She looks at Duc: keep trying, or save the battery?",
      "Does Duc keep the radio on?",
      {"chiara": "Get a yes from Ajaccio tonight, and not let anyone hear her beg."},
      [A("Ajaccio confirms they will look for a tug.", U("rettung", 1), W("strom", -1)),
       A("Duc takes over the radio and talks to Ajaccio himself.", U("rettung", 1), W("vertrauen.chiara", -1))],
      art="plot", uhr="rettung", gewicht=1.1),
    S("elsa_salvage", "tag", [2, 6], "The salvage report", "village_harbour", ["sophia", "elsa"], "10:00",
      "The coast-guard post, a fan turning slowly, a chart of the bay on the wall. Elsa has the salvage report for Ajaccio ready: crew list, damage, position, three signatures. She also wants to inspect the yacht herself - every cabin, every locker. Especially the lazarette.",
      "Does Duc get the tow request through Elsa - and what does she find aboard?",
      {"sophia": "Charm the lieutenant, which is harder than it looks.",
       "elsa": "Get the report right, and get a look inside the yacht's lockers."},
      [A("Elsa files the salvage report with Ajaccio.", U("rettung", 1), W("ruf", 1)),
       A("Duc invites Elsa aboard for an inspection.", W("ruf", 1), W("draht", -1))],
      art="plot", uhr="rettung"),
    S("starlink_deal", "tag", [2, 6], "Yasin's dish", "sun_deck", ["siri", "yasin"], "12:00",
      "Yasin has a portable satellite dish in his luggage, for content. It could make an emergency call to the Eden group, tonight. He will lend it, for a price: he films the crew, everything, for his video. Siri looks at the deck, not at anyone.",
      "Does Duc take Yasin's deal?",
      {"siri": "Not be the reason the crew gets filmed, and not say so.",
       "yasin": "Get the content he came for."},
      [A("Duc takes the deal.", U("rettung", 2), U("yasin_video", 1)),
       A("Duc refuses the deal.", W("vertrauen.siri", 1), U("siri_marke", 1))],
      art="plot", uhr="rettung", bed={"nicht": {"flag": "video_gestoppt"}}),
    S("solar_salt", "tag", [2, 7], "Salt on the panels", "solar_deck", ["lea", "rosi"], "16:00",
      "The solar deck. A crust of salt on the panels steals a third of the sun. Lea has buckets and a squeegee and turns it into a game; Rosi has a multimeter and wants it done properly. The sun is hot, the deck is wet.",
      "Do the panels get clean - and who ends up soaked?",
      {"lea": "Make the work fun and soak someone.",
       "rosi": "Get the numbers up. Measure everything."},
      [A("The panels are clean.", W("strom", 2)),
       A("Rosi ends up soaked and laughing.", W("moral", 1), W("begehren.rosi", 1))],
      art="plot", einmalig=True),
]

# ======================================================================== HINWEISE zur Wahrheit (Varianten je Wahrheit)
def spur(id, phase, tage, basis, varianten):
    e = S(id, phase, tage, basis["titel"], basis["ort"], basis["anwesend"], basis["zeit"], basis["lage"], basis["frage"],
          basis["figuren"], basis["ausgaenge"], art="hinweis", gewicht=1.2)
    e["varianten"] = [{"wenn": {"wahrheit": w}, "szene": v} for w, v in varianten.items()]
    return e


POOL += [spur("first_trace", "tag", [2, 3],
    {"titel": "The first trace", "ort": "power_room", "anwesend": ["rosi"], "zeit": "14:00",
     "lage": "Power room. Rosi has found something and doesn't like it.", "frage": "What does the trace mean?",
     "figuren": {"rosi": "Show Duc what she found without accusing anyone."},
     "ausgaenge": [A("Duc looks at the trace closely.", C("Eine erste Spur zur Ursache des Ausfalls."))]},
    {"defekt": {"ausgangslage": "Power room. Rosi holds up a burnt module from inverter three: scorched contacts, and a serial number that doesn't match the logbook. 'Somebody changed this part. Or the factory lied.'",
                "ausgaenge": [A("Duc looks at the module closely.", I("serial_mismatch"))]},
     "chiara": {"ausgangslage": "Power room. Rosi shows Duc her monitor: the night of the blackout, at 02:10, the bridge drew power it should not have drawn. 'Somebody was up there. Doing something.'",
                "ausgaenge": [A("Duc looks at the power log closely.", I("power_log"))]},
     "lea": {"ort": "bridge", "anwesend": ["chiara"], "figuren": {"chiara": "Show Duc the track and not say what she thinks."},
             "ausgangslage": "The bridge. Chiara has the GPS track of the night passage on the plotter. Halfway to Calvi the line bends south-west, towards the Esterel, for almost an hour. 'That's not the course I gave.'",
             "ausgaenge": [A("Duc looks at the track closely.", I("gps_track"))]},
     "sophia": {"ort": "alvas_bar", "anwesend": ["sophia", "alva"], "zeit": "13:00",
                "figuren": {"sophia": "Have a quiet coffee and not be greeted like an old friend.", "alva": "Welcome Sophia back, loudly."},
                "ausgangslage": "Alva's bar at noon. When Sophia walks in, Alva opens her arms: 'Sophia! Back again, o figliola?' Sophia laughs too quickly and orders coffee for two.",
                "ausgaenge": [A("Duc notices that Alva knows Sophia.", C("Alva begrüßt Sophia wie eine alte Bekannte - war sie schon einmal in Cala d'Orsu?"))]},
     "wette": {"anwesend": ["lea"], "figuren": {"lea": "Show Duc what she found and not get anyone into trouble."},
               "ausgangslage": "Power room. Lea, helping out, has found a breaker that was switched off by hand, with a label on it in Rosi's handwriting. She holds it up, confused. 'Is this... supposed to be off?'",
               "ausgaenge": [A("Duc looks at the breaker closely.", I("breaker_note"))]},
     "yasin": {"ort": "main_salon", "anwesend": ["siri"], "figuren": {"siri": "Tell Duc about the smell without blaming anyone."},
               "ausgangslage": "The main salon. Siri stops Duc on his way through. Since the night of the blackout, the VIP cabin smells of burnt plastic, she says, and Yasin keeps the wardrobe locked. 'It's probably nothing. Is it nothing?'",
               "ausgaenge": [A("Duc listens to Siri.", C("Seit der Nacht des Ausfalls riecht die VIP-Kabine nach verschmortem Plastik."))]}}),
    spur("second_trace", "abend", [3, 3],
    {"titel": "The second trace", "ort": "crew_mess", "anwesend": ["chiara"], "zeit": "21:30",
     "lage": "Crew mess. Someone remembers something about the night of the blackout.", "frage": "Who saw what?",
     "figuren": {"chiara": "Tell Duc what she saw, carefully."},
     "ausgaenge": [A("Duc listens.", C("Eine zweite Spur zur Ursache des Ausfalls."))]},
    {"defekt": {"ort": "petru_workshop", "anwesend": ["petru", "rosi"], "zeit": "17:00",
                "figuren": {"petru": "Tell what he read, in few words.", "rosi": "Not believe an old fisherman, then believe him."},
                "ausgangslage": "Petru's workshop. The old man looks at the burnt module Rosi brought and grunts. He has read about this inverter series on a forum for fishing boats: they burn, all of them, one after the other.",
                "ausgaenge": [A("Duc listens to Petru.", C("Petru: Diese Wechselrichter-Serie brennt durch, eine nach der anderen."))]},
     "chiara": {"ort": "sun_deck", "anwesend": ["lea"], "figuren": {"lea": "Tell Duc about the ghost, half joking, half not."},
                "ausgangslage": "Sun deck at dusk. Lea, whispering: on the night of the blackout she saw the ghost again, on the bridge wing, holding something brass. Just before the lights went out.",
                "ausgaenge": [A("Duc listens to Lea.", C("Lea hat in der Nacht des Ausfalls das 'Gespenst' auf der Brückennock gesehen."))]},
     "lea": {"ort": "swim_platform", "anwesend": ["siri"], "figuren": {"siri": "Tell Duc what she saw, worried about Lea."},
             "ausgangslage": "Swim platform at dusk. Siri tells Duc she found Lea crying on the platform the morning after the blackout, holding a soaking wet logbook against her chest like a child.",
             "ausgaenge": [A("Duc listens to Siri.", C("Siri fand Lea am Morgen nach dem Ausfall weinend, mit einem nassen Logbuch."))]},
     "sophia": {"anwesend": ["chiara"], "figuren": {"chiara": "Show Duc the passage plan and not believe what she sees."},
                "ausgangslage": "Crew mess. Chiara puts the paper passage plan on the table. The night passage was moved forward by six hours, by hand. The handwriting is Sophia's.",
                "ausgaenge": [A("Duc looks at the passage plan.", I("paris_call"))]},
     "wette": {"figuren": {"chiara": "Tell Duc about the board, and pretend she has never looked at it."},
               "ausgangslage": "Crew mess. Chiara, too casually: the odds on the engine room board changed the day before the blackout. Somebody bet big on 'stranded with the officer'.",
               "ausgaenge": [A("Duc listens to Chiara.", C("Die Quoten an der Wett-Tafel änderten sich am Tag vor dem Ausfall."))]},
     "yasin": {"ort": "vip_cabin", "anwesend": ["siri"], "figuren": {"siri": "Show Duc what she found and decide what it means for her."},
               "ausgangslage": "The VIP cabin. Siri has unlocked Yasin's wardrobe while he is ashore. Inside, wrapped in a T-shirt: a charred charger lead, melted at the plug. She holds it out to Duc with shaking hands.",
               "ausgaenge": [A("Duc takes the charger lead.", I("burnt_cable"), U("siri_marke", 1))]}}),
]

# ======================================================================== DRAMA und Crew
POOL += [
    S("too_much_rose", "abend", [2, 6], "Too much rosé", "swim_platform", ["siri", "yasin"], "18:30",
      "Swim platform at sunset. Yasin and Siri have been drinking rosé since noon, the last bottles from the guest bar. Yasin films her and his hand slides to the string of her bikini top. 'Come on. For the story.' She shoves him away, hard. He slips, almost into the sea, and gets loud.",
      "Does Duc step in - and what does Siri need afterwards?",
      {"siri": "Not cry in front of anyone, and not be rescued like a damsel.",
       "yasin": "Get his content and his pride back."},
      [A("Duc steps between them.", W("vertrauen.siri", 1), U("siri_marke", 1)),
       A("Siri tells Yasin to leave her alone.", U("siri_marke", 1), W("begehren.siri", 1))],
      art="drama", gewicht=1.1),
    S("two_out_of_ten", "abend", [3, 6], "Two out of ten", "aft_deck", ["chiara", "siri", "yasin"], "22:30",
      "The aft deck after dinner. Yasin, three whiskies in, leans on the bar towards Chiara. 'When do you finish? I'll show you Paris.' Chiara smiles her perfect smile: 'Monsieur Benali, I finish when you're asleep. Tonight that should be early.' Yasin reaches for the tender key. The hook is empty: it's in Duc's pocket.",
      "What does Duc do with the humiliated guest - and with Siri, left alone at the table?",
      {"chiara": "Keep perfect service and let the guest know exactly what she thinks of him.",
       "siri": "Sit with dignity while her boyfriend flirts with the crew.",
       "yasin": "Get to the village, a bar, anywhere; win."},
      [A("Duc refuses Yasin the tender.", W("vertrauen.chiara", 1), U("siri_marke", 1)),
       A("Duc sits down with Siri.", W("vertrauen.siri", 1), W("rivalitaet.chiara_siri", 1))],
      art="drama", gewicht=1.1),
    S("chicken_fight", "tag", [2, 7], "Chicken fight", "swim_platform", ["lea", "rosi"], "16:30",
      "Afternoon, the water flat and warm. Lea challenges Rosi to a chicken fight off the swim platform: one sits on someone's shoulders, the other team tries to knock them off. Rosi refuses, then hears the word 'scared', then points at Duc. 'Him. I'm on him.'",
      "Who wins the chicken fight?",
      {"lea": "Win, loudly, and get the crew laughing.",
       "rosi": "Win. Only win. And be on his shoulders, which is purely tactical."},
      [A("Duc and Rosi win.", W("begehren.rosi", 1), W("moral", 1)),
       A("Lea and her team win.", W("begehren.lea", 1), W("moral", 1))],
      art="drama"),
    S("village_kids", "tag", [2, 6], "Visitors in a dinghy", "village_harbour", ["lea", "casanova"], "11:00",
      "Three kids from the village row out in a leaking dinghy to stare at the yacht, and the mayor shouts at them from the quay. Lea is already waving them over. Madame Casanova looks at Duc: is the famous yacht friendly to her village?",
      "Does Duc show the village kids the yacht?",
      {"lea": "Show the kids everything, the fish book, the tender, the stars on the plotter.",
       "casanova": "Find out what kind of man commands the yacht in her bay."},
      [A("Duc shows the kids around the yacht.", W("ruf", 2), W("vertrauen.lea", 1))],
      art="drama"),
    S("jealous_chiara_siri", "abend", [3, 6], "The lipstick", "crew_corridor", ["chiara", "siri"], "22:00",
      "The crew corridor. Siri, a guest, below deck again, bringing Duc a coffee he didn't ask for. Chiara blocks the corridor with a laundry basket. 'Guests stay upstairs. House rules.' Two smiles, both perfect, both sharp.",
      "Whose side is Duc on - and does he notice what this is really about?",
      {"chiara": "Keep the guest where guests belong, and not say why it bothers her.",
       "siri": "Bring the coffee to Duc anyway."},
      [A("Duc calms both of them without choosing.", W("moral", 1)),
       A("Duc takes Siri's coffee.", W("begehren.siri", 1), W("rivalitaet.chiara_siri", 1)),
       A("Duc backs Chiara's rule.", W("vertrauen.chiara", 1), W("rivalitaet.chiara_siri", 1))],
      art="drama", bed={"alle": [{"vertrauen": ["chiara", 3]}, {"vertrauen": ["siri", 3]}]}, gewicht=1.4),
    S("jealous_rosi_siri", "abend", [3, 6], "Coffee in the power room", "power_room", ["rosi", "siri"], "21:30",
      "The power room. Siri has brought Rosi her morning coffee again, this time at night, and this time two cups: one for Rosi, one for Duc. Rosi looks at the second cup like it's a short circuit.",
      "Does Duc notice what's going on between the engineer and the guest?",
      {"rosi": "Throw the influencer out and not be the kind of person who throws people out.",
       "siri": "Make friends with the one woman on the boat who doesn't like her."},
      [A("Duc makes them laugh together.", W("moral", 1), W("rivalitaet.rosi_siri", -1)),
       A("Duc takes Rosi's side.", W("vertrauen.rosi", 1), W("rivalitaet.rosi_siri", 1))],
      art="drama", bed={"alle": [{"vertrauen": ["rosi", 3]}, {"vertrauen": ["siri", 3]}]}, gewicht=1.4),
    S("tally_war", "abend", [2, 6], "The tally", "crew_mess", ["chiara", "sophia"], "21:00",
      "The crew mess. The tally on the fridge is disputed again: Chiara says the village kids count, Sophia says children laugh at everything. They both turn to Duc. He is the commander. He decides.",
      "Who wins the tally tonight?",
      {"chiara": "Win the point and make Sophia admit it.",
       "sophia": "Win the point and make it look effortless."},
      [A("Duc gives the point to Chiara.", W("vertrauen.chiara", 1), W("rivalitaet.chiara_sophia", 1)),
       A("Duc gives the point to Sophia.", W("vertrauen.sophia", 1), W("rivalitaet.chiara_sophia", 1)),
       A("Duc refuses to decide and makes them both laugh.", W("moral", 1), W("rivalitaet.chiara_sophia", -1))],
      art="drama"),
]

# ======================================================================== JOBS (16.10.2026: Geld verdienen)
def G(betrag, text):
    return {"geld": betrag, "text": text}


# Grosse Jobs: eine Wahl-Phase statt einer Romanze - Geld gegen Zeit mit den Frauen.
POOL += [
    S("job_elsa_boat", "tag", [2, 6], "The patrol boat", "village_harbour", ["elsa"], "10:30",
      "The quay. Elsa's patrol boat has a starboard engine that coughs and dies, and Ajaccio wants three weeks and a "
      "form to send a mechanic. She stands beside it, arms crossed, sunglasses up. 'They say you fix things, First "
      "Officer. Two hundred and fifty, from my own pocket. If Ajaccio asks, you were never here.'",
      "Can Duc get the patrol boat running - and win the lieutenant?",
      {"elsa": "Get her boat running without admitting she needs help from a man with a smuggler in his crew."},
      [A("The engine runs again.", G(250, "Elsa: Patrouillenboot repariert"), W("ruf", 1)),
       A("Elsa is impressed and says so, in her dry way.", W("ruf", 1))],
      art="job", gewicht=1.1),
    S("job_festa_lights", "tag", [3, 5], "Lights for the festa", "village_piazza", ["casanova", "lea"], "15:00",
      "The piazza. Madame Casanova has eighty metres of festoon lights, a fuse box from 1970 and a festa in two days. "
      "Lea is already up a ladder, holding a cable she should not be holding. The mayor pays three hundred euros if the "
      "lights are on by the evening.",
      "Do the lights come on - and does anyone get a shock?",
      {"casanova": "Get her festa lit, on time, by the famous yacht.", "lea": "Help, climb things, and be near him."},
      [A("The lights come on over the piazza.", G(300, "Casanova: Lichterketten für die Festa"), W("ruf", 1), I("festa_invite")),
       A("Lea and Duc work as a team.", W("vertrauen.lea", 1))],
      art="job", gewicht=1.1),
    S("job_yasin_shoot", "tag", [2, 6], "Content day", "sun_deck", ["yasin", "siri"], "12:00",
      "The sun deck. Yasin wants the 'stranded captain' shoot: Duc at the helm, Siri in the background, drone overhead. "
      "Three hundred and fifty euros, cash, right now. Siri sits on a sunbed and looks at anything but the camera.",
      "Does Duc take Yasin's money - and what does it cost Siri?",
      {"yasin": "Get his content and pay for it like a boss.", "siri": "Not be a prop again, without making a scene."},
      [A("Duc does the shoot.", G(350, "Yasin: Content-Shooting"), U("yasin_video", 1)),
       A("Duc stops the shoot when Yasin pushes Siri.", W("vertrauen.siri", 1), U("siri_marke", 1))],
      art="job", gewicht=1.0, bed={"nicht": {"flag": "video_gestoppt"}}),
    S("job_toto_cove", "abend", [2, 6], "The cove at night", "swim_platform", ["toto"], "23:00",
      "Swim platform, eleven at night. Totò in a black hoodie, the tender ready, no lights. His cousin from Bastia waits in "
      "the next cove with 'some boxes, Comandante, nothing interesting'. Four hundred euros for one hour and no questions. "
      "Across the bay, the coast-guard post still has a light on.",
      "Does Duc drive Totò's boxes - and does anyone see them?",
      {"toto": "Get the boxes across with the Comandante at the wheel, and make him laugh doing it."},
      [A("They bring the boxes across unseen.", G(400, "Totò: nächtliche Überfahrt"), W("draht", 1)),
       A("Elsa's searchlight catches the tender in the dark.", W("ruf", -1))],
      art="job", gewicht=1.0, begruendung="Totò takes the tender out from the swim platform at night."),
    S("job_alva_coldroom", "abend", [2, 6], "Alva's cold room", "alvas_bar", ["alva", "sophia"], "21:00",
      "Alva's bar. The cold room compressor died this afternoon, with the whole festa stock inside. Alva pours myrtle "
      "liqueur for Sophia and looks at Duc over the glass. 'Fix it, and you get two hundred euros. And diesel. Maybe.'",
      "Does Duc save Alva's cold room - and what does Sophia trade on the side?",
      {"alva": "Save her stock and find out if this officer is worth liking.", "sophia": "Turn a favour into diesel and a friend."},
      [A("The compressor runs again.", G(200, "Alva: Kühlraum repariert"), W("ruf", 1)),
       A("Alva adds a canister of diesel.", W("diesel", 1), W("vertrauen.sophia", 1))],
      art="job", gewicht=1.1),
]

# Schnelljobs: im Handy, kosten 1 Energie, W20-Probe; Fehlschlag = halber Lohn. reparatur=True -> Vorteil Handwerk,
# kochen=True -> Vorteil Kueche (Persona-Vorteile, handel.persona_vorteil).
JOBS = [
    {"id": "ice_machine", "von": "alva", "titel": "Eismaschine in Alvas Bar", "tage": [2, 7], "attribut": "cunning", "sg": 12,
     "lohn": 120, "reparatur": True, "folgen": [{"wert": "ruf", "delta": 1}],
     "text": "Die Eismaschine tropft und brummt. Alva zahlt, wenn sie bis heute Abend wieder Eis macht.",
     "erfolg": "Die Maschine läuft. Alva stellt dir einen Myrtenlikör hin.", "fehlschlag": "Sie läuft – halb. Alva zahlt halb."},
    {"id": "nets", "von": "petru", "titel": "Petrus Netze flicken", "tage": [2, 7], "attribut": "perception", "sg": 10,
     "lohn": 60, "folgen": [{"wert": "ruf", "delta": 1}],
     "text": "Petru zeigt auf einen Haufen Netze und sagt nichts. Das ist ein Angebot.",
     "erfolg": "Petru nickt einmal. Bei ihm ist das ein Orden.", "fehlschlag": "Zwei Löcher übersehen. Petru zahlt trotzdem etwas."},
    {"id": "radio_elsa", "von": "elsa", "titel": "Funkgerät im Küstenwache-Posten", "tage": [2, 6], "attribut": "cunning", "sg": 11,
     "lohn": 90, "reparatur": True, "folgen": [{"wert": "ruf", "delta": 1}],
     "text": "Elsas Funkgerät nach Ajaccio rauscht. Ohne Funk keine Bergung – sie zahlt bar und hasst es, fragen zu müssen.",
     "erfolg": "Klarer Empfang. Elsa nickt einmal – das ist bei ihr ein Orden.", "fehlschlag": "Es rauscht weniger. Elsa zahlt die Hälfte."},
    {"id": "english_kids", "von": "casanova", "titel": "Englisch für die Enkel der Bürgermeisterin", "tage": [2, 6],
     "attribut": "charm", "sg": 10, "lohn": 70, "folgen": [{"wert": "ruf", "delta": 1}],
     "text": "Zwei Enkel, eine Stunde, ein Schulbuch. Madame Casanova zahlt bar und erzählt es dem ganzen Dorf.",
     "erfolg": "Die Kinder lachen und können „anchor“ sagen. Das Dorf redet gut über dich.", "fehlschlag": "Chaos, aber herzlich. Halber Lohn."},
    {"id": "drone", "von": "yasin", "titel": "Yasins Drohne aus dem Wasser holen", "tage": [2, 6], "attribut": "courage",
     "sg": 13, "lohn": 150, "folgen": [],
     "text": "Yasins Drohne ist neben dem Anker ins Wasser gefallen. Sechs Meter tief. Er zahlt bar, in Scheinen.",
     "erfolg": "Du tauchst sie hoch. Yasin zahlt und filmt dich dabei.", "fehlschlag": "Du findest nur den Akku. Yasin zahlt widerwillig die Hälfte."},
    {"id": "toto_box", "von": "toto", "titel": "Eine Kiste für Totò umladen", "tage": [2, 6], "attribut": "cunning", "sg": 13,
     "lohn": 120, "folgen": [], "folgen_fehlschlag": [{"wert": "ruf", "delta": -1}],
     "text": "„Nicht reinschauen, Comandante. Einfach vom Beiboot in den Lagerraum. Und wenn die Leutnantin fragt: Kartoffeln.“",
     "erfolg": "Niemand hat etwas gesehen. Totò küsst dich auf beide Wangen.", "fehlschlag": "Elsa hat etwas gesehen. Totò zahlt trotzdem halb – und schwitzt."},
    {"id": "outboard", "von": "petru", "titel": "Außenborder eines Fischers", "tage": [3, 7], "attribut": "cunning", "sg": 12,
     "lohn": 140, "reparatur": True, "folgen": [{"wert": "ruf", "delta": 1}],
     "text": "Petrus Nachbar hat einen Außenborder, der stottert. Petru hat dich empfohlen. Das ist neu.",
     "erfolg": "Er schnurrt wie neu. Der Fischer zahlt und bringt morgen Fisch.", "fehlschlag": "Er läuft, aber laut. Halber Lohn."},
    {"id": "guest_breakfast", "von": "yasin", "titel": "Frühstück für die Gäste zaubern", "tage": [2, 7], "attribut": "charm",
     "sg": 12, "lohn": 80, "kochen": True, "folgen": [{"wert": "moral", "delta": 1}],
     "text": "Yasin will Eggs Benedict ohne Strom. Er zahlt Trinkgeld, wenn es klappt. Viel Trinkgeld.",
     "erfolg": "Campingkocher, Charme und gutes Timing. Yasin gibt großzügig Trinkgeld.", "fehlschlag": "Die Eier sind hart. Das Trinkgeld auch."},
]
# Missionen der Frauen und Ketten (17.10.2026). Frauen zahlen nicht - Erfolg bringt Naehe (Code: handel.job_machen,
# +6 Vertrauen/+4 Begehren, eine Wirkung je Frau und Tag) und oft einen kleinen Nutzen fuers Schiff.
# nach = erst nach ERFOLG dieser Mission; ab_vertrauen = Mindest-Stufe bei der Auftraggeberin.
JOBS += [
    {"id": "rosi_cells", "von": "rosi", "titel": "Batteriezellen durchmessen", "tage": [2, 7], "attribut": "perception", "sg": 11,
     "lohn": 0, "reparatur": True, "folgen": [{"wert": "strom", "delta": 1}],
     "text": "Vierundzwanzig Zellen, ein Multimeter, eine Taschenlampe. Rosi liest vor, du misst – irgendwo ist eine faul."},
    {"id": "rosi_bleed", "von": "rosi", "titel": "Unit-01 entlüften", "tage": [3, 7], "attribut": "cunning", "sg": 12,
     "lohn": 0, "reparatur": True, "nach": "rosi_cells", "ab_vertrauen": 2, "folgen": [{"uhr": "reparatur", "delta": 1}],
     "text": "Luft in der Dieselleitung des Notgenerators. Rosi hält die Lampe und flucht leise auf Sizilianisch."},
    {"id": "chiara_coldroom", "von": "chiara", "titel": "Kühlraum-Inventur", "tage": [2, 7], "attribut": "perception", "sg": 10,
     "lohn": 0, "folgen": [{"wert": "moral", "delta": 1}],
     "text": "Was hält noch, was muss heute weg? Chiara will eine Liste, bevor der Kühlraum warm wird."},
    {"id": "chiara_complaint", "von": "chiara", "titel": "Gästebeschwerde abfangen", "tage": [3, 7], "attribut": "charm", "sg": 12,
     "lohn": 0, "nach": "chiara_coldroom", "ab_vertrauen": 2, "folgen": [{"wert": "moral", "delta": 1}],
     "text": "Yasin droht mit einer Ein-Stern-Bewertung für die ganze Crew. Chiara braucht jemanden, der ihn freundlich ausbremst."},
    {"id": "sophia_papers", "von": "sophia", "titel": "Papiere zur Küstenwache bringen", "tage": [2, 6], "attribut": "charm", "sg": 10,
     "lohn": 0, "folgen": [{"wert": "ruf", "delta": 1}],
     "text": "Ankererlaubnis, Crewliste, ein Stempel fehlt. Sophia hat die Mappe sortiert – bringen sollst du sie."},
    {"id": "sophia_diesel", "von": "sophia", "titel": "Einen Diesel-Gefallen einfädeln", "tage": [3, 7], "attribut": "charm", "sg": 12,
     "lohn": 0, "nach": "sophia_papers", "ab_vertrauen": 2, "folgen": [{"wert": "diesel", "delta": 1}],
     "text": "Sophia kennt jemanden, der jemanden kennt, der einen Kanister übrig hat. Sie braucht nur dein Gesicht dazu."},
    {"id": "lea_chain", "von": "lea", "titel": "Ankerkette tauchend prüfen", "tage": [2, 7], "attribut": "courage", "sg": 11,
     "lohn": 0, "folgen": [{"wert": "moral", "delta": 1}],
     "text": "Lea will sehen, ob der Anker wirklich hält. Sieben Meter, klares Wasser, ein Seeigel-Feld."},
    {"id": "lea_wreck", "von": "lea", "titel": "Großvaters Karte entziffern", "tage": [3, 7], "attribut": "perception", "sg": 12,
     "lohn": 0, "nach": "lea_chain", "ab_vertrauen": 2,
     "folgen": [{"codex": "Leas Karte: Großvater hat ein Kreuz vor dem Esterel gemacht – dort soll die Margot liegen."}],
     "text": "Eine vergilbte Seekarte aus Leas Koffer, mit Bleistift-Kreuzen. Sie traut sich nicht allein, sie zu lesen."},
    {"id": "siri_photos", "von": "siri", "titel": "Fotos ohne Yasin", "tage": [2, 7], "attribut": "charm", "sg": 11,
     "lohn": 0, "folgen": [],
     "text": "Siri will Bilder, auf denen sie nicht posiert. Nur Licht, Wasser und sie. Du hältst die Kamera."},
    {"id": "siri_samples", "von": "siri", "titel": "Meeresproben sammeln", "tage": [3, 7], "attribut": "perception", "sg": 11,
     "lohn": 0, "nach": "siri_photos", "ab_vertrauen": 2,
     "folgen": [{"codex": "Siri hat Seegras-Proben gesammelt – sie will Meeresbiologie studieren. Sie hat es noch niemandem gesagt."}],
     "text": "Glasröhrchen, ein Notizbuch, die Badeplattform. Siri erklärt dir Seegras, als wäre es das Spannendste der Welt."},
    # Ketten im Dorf: die zweite Mission erst nach Erfolg bei der ersten
    {"id": "alva_diesel", "von": "alva", "titel": "Diesel unter der Theke", "tage": [3, 7], "attribut": "cunning", "sg": 12,
     "lohn": 0, "nach": "ice_machine", "folgen": [{"wert": "diesel", "delta": 1}],
     "text": "Alva hat da „etwas im Keller“. Abholen musst du es selbst, und zwar so, dass die Leutnantin es nicht sieht."},
    {"id": "petru_wreck", "von": "petru", "titel": "Petrus Wrack-Geschichte", "tage": [3, 7], "attribut": "empathy", "sg": 11,
     "lohn": 0, "nach": "nets",
     "folgen": [{"codex": "Petru: Vor dem Esterel liegt ein altes Boot. Sein Vater hat den Namen gekannt – Margot."}],
     "text": "Petru flickt schweigend weiter. Wer zuhört, ohne zu drängen, bekommt vielleicht eine Geschichte."},
    {"id": "elsa_report", "von": "elsa", "titel": "Bericht für Ajaccio", "tage": [3, 7], "attribut": "perception", "sg": 11,
     "lohn": 80, "nach": "radio_elsa", "folgen": [{"uhr": "rettung", "delta": 1}],
     "text": "Elsa braucht einen technischen Lagebericht über die Eden Rise. Ohne Bericht keine Bergungsplanung."},
    {"id": "casanova_banner", "von": "casanova", "titel": "Festa-Banner aufhängen", "tage": [3, 5], "attribut": "courage", "sg": 10,
     "lohn": 60, "nach": "english_kids", "folgen": [{"wert": "ruf", "delta": 1}, {"item": "festa_invite"}],
     "text": "Zwanzig Meter Stoff, ein Kirchturm, eine Leiter von 1962. Madame Casanova spendiert dafür eine Einladung zur Festa."},
    {"id": "toto_night", "von": "toto", "titel": "Nachtfahrt mit Totòs Cousin", "tage": [3, 6], "attribut": "courage", "sg": 13,
     "lohn": 200, "nach": "toto_box", "folgen": [], "folgen_fehlschlag": [{"wert": "ruf", "delta": -1}],
     "text": "Ein Schlauchboot aus Bastia, keine Lichter, eine Stunde nach Mitternacht. „Du steuerst nur, Comandante.“"},
]

# ======================================================================== ABWECHSLUNG (17.10.2026)
# Duc: "mehr Beimischung mit den anderen NPCs und weniger Essen in der Yacht". Dinner ist jetzt eine Wahl-Phase;
# neue Fruehstuecke wechseln sich an Tag 2 und 7 ab (3/5 sind Plot, 4/6 Wendepunkte); gemischte Szenen
# Frau + Nebenfigur, die zugleich die Leute im Dorf "bekannt" machen (schaltet ihre Missionen frei).
POOL += [
    # ---------------- Fruehstueck
    S("siri_ritual", "fruehstueck", [2, 7], "Morning ritual", "foredeck", ["siri"], "06:45",
      "The foredeck at sunrise. Siri sits on a towel with her eyes closed. No phone, no make-up. Yasin is still asleep. She hears Duc and does not open her eyes. \"You can stay,\" she says. \"If you're quiet.\"",
      "Does Duc stay quiet with her - or does he ask what she is hiding from?",
      {"siri": "Have ten minutes that belong to nobody but her."},
      [A("Duc sits with her in silence.", W("vertrauen.siri", 1)),
       A("Siri tells Duc something true about herself.", W("begehren.siri", 1))], max_zuege=5),
    S("elsa_coffee", "fruehstueck", [2, 6], "Inspection with coffee", "aft_deck", ["elsa", "chiara"], "08:00",
      "The patrol boat ties up at the stern. Lieutenant Ferrandi comes aboard with a clipboard. Chiara has coffee ready before Elsa can say no. Elsa checks the life jackets, the logbook, the anchor light. She drinks the coffee anyway.",
      "Does the Eden Rise pass the inspection - and who charms whom?",
      {"elsa": "Find something wrong. Hope she doesn't.",
       "chiara": "Pass with zero remarks, and get Elsa to admit the coffee is good."},
      [A("Elsa finds nothing to write down.", W("ruf", 1)),
       A("Elsa and Chiara end up laughing together.", W("moral", 1), W("vertrauen.chiara", 1))], max_zuege=5),
    S("petru_dawn", "fruehstueck", [2, 6], "Fish at dawn", "swim_platform", ["petru", "lea"], "06:30",
      "A small wooden boat comes out of the mist. Petru ties up at the swim platform with a crate of fish. Lea is already there in her pyjamas, barefoot, asking about every fish by name. Petru answers each question with one word.",
      "What does Duc give Petru for the fish?",
      {"petru": "Give the fish and leave before anyone thanks him.",
       "lea": "Learn every name and get Petru to take her out once."},
      [A("Petru promises to take Lea out fishing.", W("vertrauen.lea", 1), W("ruf", 1)),
       A("Duc and Petru talk about the engine.", U("reparatur", 1))], max_zuege=5),
    S("toto_espresso", "fruehstueck", [2, 7], "Totò's espresso", "galley", ["toto", "rosi", "lea"], "07:15",
      "The galley smells of coffee. Totò has a moka pot on a camping stove and a bag of real Neapolitan beans. \"Smuggled,\" he says proudly. Rosi wants a cup and pretends she doesn't. Lea has already had three.",
      "Does Duc let the morning be fun - or does he start the day's work?",
      {"toto": "Make the best coffee on the boat and get the Comandante to admit it.",
       "rosi": "Get her coffee without being nice to Totò.",
       "lea": "Get a fourth cup."},
      [A("Everyone laughs together over coffee.", W("moral", 1)),
       A("Totò and Rosi agree on something.", W("vertrauen.rosi", 1), W("draht", 1))], max_zuege=5),
    S("quay_cafe", "fruehstueck", [2, 7], "Café on the quay", "village_harbour", ["sophia", "alva"], "08:00",
      "Duc and Sophia take the tender in early. Alva has two chairs out on the quay and fresh bread from the baker. She knows already what the yacht had for dinner last night. Sophia wants to know how.",
      "What does Alva tell them - and what does she want for it?",
      {"sophia": "Find out who in the village talks to Alva, and why.",
       "alva": "Find out everything about the yacht, and give a little back."},
      [A("Alva tells them something useful.", W("ruf", 1), W("vertrauen.sophia", 1)),
       A("Alva offers a favour.", W("diesel", 1))], max_zuege=5),
    S("yasin_brunch", "fruehstueck", [2, 5], "Brunch shoot", "sun_deck", ["yasin", "siri", "chiara"], "09:00",
      "Yasin wants a brunch shoot on the sun deck. Fruit, champagne, golden light. Chiara has to carry everything up. Siri has to smile on command. Yasin directs like a film director, and nobody asked him to.",
      "Does Duc let Yasin have his show - or does he end it?",
      {"yasin": "Get the perfect brunch content, no matter who has to carry it.",
       "siri": "Survive the shoot without crying in front of the crew.",
       "chiara": "Protect her crew from this man without losing her job."},
      [A("Duc ends the shoot.", W("vertrauen.chiara", 1), W("vertrauen.siri", 1)),
       A("Duc plays along to keep the peace.", W("moral", -1), U("yasin_video", 1))], art="drama", max_zuege=5),
    S("rosi_breakfast", "fruehstueck", [2, 7], "Breakfast in the power room", "power_room", ["rosi"], "06:30",
      "The power room at half past six. Rosi has not slept. She eats cold pasta out of the pot between the batteries and offers Duc the second fork. The cells hum. She reads the numbers to him like a love letter.",
      "Does Duc sit down with her - and what does he really ask?",
      {"rosi": "Have one person who understands the numbers like she does."},
      [A("Duc eats with her and listens.", W("vertrauen.rosi", 1)),
       A("They find a small gain in the battery plan.", W("strom", 1))], max_zuege=5),

    # ---------------- Dinner (Wahl-Phase)
    S("alvas_table", "dinner", [2, 7], "Alva's table", "alvas_bar", ["sophia", "alva"], "20:00",
      "Alva has pushed two tables together in the bar. Figatellu, bread, a red wine without a label. Sophia orders for both of them in Corsican, badly. Alva corrects her and gives her a second glass anyway.",
      "What does the village learn about the crew tonight - and the other way round?",
      {"sophia": "Get Alva on their side for good.",
       "alva": "Find out if this crew is worth helping."},
      [A("Alva says the crew is welcome in her bar.", W("ruf", 1)),
       A("Sophia and Duc walk back to the tender together.", W("begehren.sophia", 1))], max_zuege=6),
    S("petru_grill", "dinner", [2, 6], "Fish on the stones", "village_harbour", ["petru", "lea"], "20:00",
      "Petru grills fish on flat stones at the end of the quay. No plates, just bread and lemons. Lea sits next to him and asks about the sea. For once, Petru answers in full sentences.",
      "What does Petru tell them by the fire?",
      {"petru": "Share his fish and maybe one old story.",
       "lea": "Get Petru to talk about the wrecks off this coast."},
      [A("Petru tells a story about the old wrecks.", W("vertrauen.lea", 1)),
       A("Petru offers help with the engine.", U("reparatur", 1))], max_zuege=6),
    S("toto_genovese", "dinner", [2, 7], "Totò's genovese", "galley", ["toto", "rosi"], "19:30",
      "Totò has cooked onions for four hours on the last gas bottle. \"Genovese,\" he says. \"My mother's.\" Rosi says Sicilian food is better. Totò says nothing and fills her plate twice.",
      "Does Duc settle the war between Naples and Sicily?",
      {"toto": "Make Rosi admit the genovese is perfect.",
       "rosi": "Eat everything and never admit it."},
      [A("Rosi admits it is good.", W("moral", 1), W("draht", 1)),
       A("Rosi tells a story about her father's kitchen.", W("vertrauen.rosi", 1))], max_zuege=6),
    S("chiara_bridge_picnic", "dinner", [2, 7], "Picnic on the bridge", "bridge", ["chiara"], "20:30",
      "Chiara has carried two plates up to the bridge. Bread, cheese, the last tomatoes. \"Officers eat on the bridge,\" she says. \"Tonight I'm an officer.\" She sits in the captain's chair and grins at him.",
      "What does Chiara want to hear from Duc tonight?",
      {"chiara": "Be taken seriously as a sailor - and maybe a little more."},
      [A("Duc lets Chiara take the chair.", W("vertrauen.chiara", 1)),
       A("Chiara admits she has a Yachtmaster licence.", W("begehren.chiara", 1))],
      art="herz", bed={"vertrauen": ["chiara", 2]}, max_zuege=6),
    S("siri_foredeck_dinner", "dinner", [2, 7], "Dinner on the foredeck", "foredeck", ["siri"], "20:30",
      "Siri has taken two plates from the galley and a blanket. Yasin is on a call with Paris. \"He won't notice,\" she says. The foredeck is dark. Only the anchor light and the village behind them.",
      "What does Siri tell Duc when nobody is filming?",
      {"siri": "Have one dinner where she is not a prop."},
      [A("Siri talks about her father and the islands.", W("vertrauen.siri", 1), U("siri_marke", 1)),
       A("Siri leans against Duc's shoulder.", W("begehren.siri", 1))],
      art="herz", bed={"vertrauen": ["siri", 2]}, max_zuege=6),
    S("mayor_invites", "dinner", [3, 4], "The mayor invites", "village_harbour", ["casanova", "chiara"], "20:00",
      "Madame Casanova has set a long table on the quay for \"the brave crew of the Eden Rise\". Village kids, a guitar, too much wine. She gives a speech with three dramatic pauses. Chiara whispers that she wants to steal her energy.",
      "What does Duc promise the mayor in front of the whole village?",
      {"casanova": "Get the yacht's crew to star in her festa.",
       "chiara": "Enjoy one evening as a guest, not a stewardess."},
      [A("Duc promises the crew will help with the festa.", W("ruf", 1), I("festa_invite")),
       A("Chiara dances with the village kids.", W("moral", 1), W("vertrauen.chiara", 1))], max_zuege=6),

    # ---------------- Gemischt: Frau + Nebenfigur (Tag / Abend)
    S("lea_patrol_boat", "tag", [2, 6], "The patrol boat", "village_harbour", ["lea", "elsa"], "11:00",
      "Lea has been staring at the patrol boat for ten minutes. Lieutenant Ferrandi notices. \"You want to see it?\" Lea nods so fast her sunglasses fall off. Elsa looks at Duc. \"She's yours. You're responsible.\"",
      "Does Duc get Lea a ride - and what does Elsa want in return?",
      {"lea": "Ride the patrol boat, at full speed.",
       "elsa": "Show off her boat a little, and size up the First Officer."},
      [A("Elsa takes them out on the patrol boat.", W("vertrauen.lea", 1), W("ruf", 1)),
       A("Elsa tells Duc what Ajaccio plans for the yacht.", U("rettung", 1))], max_zuege=6),
    S("siri_petru_seagrass", "tag", [3, 7], "The seagrass", "village_harbour", ["siri", "petru"], "15:00",
      "Siri kneels on the quay over a bucket of seagrass. Petru watches her from his boat. Then he climbs out and shows her where the seahorses live. Siri forgets to take a photo.",
      "What does Siri discover - about the sea and about herself?",
      {"siri": "Learn something real from someone who knows the sea.",
       "petru": "See if this city girl actually listens."},
      [A("Petru shows Siri the seahorses.", W("vertrauen.siri", 1), U("siri_marke", 1)),
       A("Siri tells Duc she wants to study the sea.", W("begehren.siri", 1))], max_zuege=6),
    S("chiara_alva_menu", "abend", [2, 6], "The recipe", "alvas_bar", ["chiara", "alva"], "21:00",
      "Chiara wants Alva's recipe for fiadone. Alva says it has been in the family for a hundred years. Chiara offers her a tour of the yacht. Alva thinks about it. Two women who both run the room, sizing each other up.",
      "Who gets what - and what does Duc have to do with it?",
      {"chiara": "Get the recipe, and maybe a friend.",
       "alva": "Get a tour of the yacht, and a look at the First Officer up close."},
      [A("Alva gives Chiara the recipe.", W("vertrauen.chiara", 1), W("ruf", 1)),
       A("Alva flirts with Duc and Chiara notices.", W("begehren.chiara", 1))], max_zuege=6),
    S("chiara_elsa_rules", "tag", [2, 5], "Rule against rule", "village_harbour", ["chiara", "elsa"], "10:00",
      "The tender is tied up in the wrong place. Elsa says so. Chiara says the harbour master said it was fine. Elsa says there is no harbour master. Two women with clipboards, both right, neither giving an inch.",
      "Does Duc take a side - or find the way out?",
      {"chiara": "Win this, in front of Duc.",
       "elsa": "Make the rules clear to this crew, once."},
      [A("Duc finds a solution both accept.", W("ruf", 1), W("vertrauen.chiara", 1)),
       A("Chiara and Elsa end up respecting each other.", W("moral", 1))], max_zuege=5),
    S("siri_festa_prep", "tag", [3, 5], "Festa preparations", "village_harbour", ["siri", "casanova"], "14:00",
      "Madame Casanova has found out that Siri has followers. She wants a festa video. Siri wants to say no. The mayor gasps dramatically, takes her hand and calls her \"the star of season two\".",
      "Does Siri help the village - on her own terms?",
      {"casanova": "Get Siri to film the festa preparations.",
       "siri": "Do something for the village that isn't for Yasin."},
      [A("Siri films the village her way, without Yasin.", W("vertrauen.siri", 1), W("ruf", 1), U("siri_marke", 1)),
       A("The mayor gives Duc a festa invitation.", I("festa_invite"))], max_zuege=6),
    S("toto_betting", "abend", [2, 6], "Totò's betting board", "crew_mess", ["toto", "rosi", "chiara"], "21:30",
      "Totò has a chalkboard. On it: \"Who fixes the drive first? Rosi 2:1, Petru 5:1, a miracle 50:1.\" Rosi is offended. Chiara puts ten euros on the miracle. Totò looks at Duc. \"Comandante? You bet?\"",
      "Does Duc bet - and on whom?",
      {"toto": "Take everyone's money with a smile.",
       "rosi": "Make them all bet on her.",
       "chiara": "Win something, for once."},
      [A("Duc bets on Rosi and wins.", {"geld": 80, "text": "Totòs Wettbuch"}, W("vertrauen.rosi", 1)),
       A("Duc loses his bet.", {"geld": -40, "text": "Totòs Wettbuch"}),
       A("Everyone laughs together.", W("moral", 1), W("draht", 1))], art="job", max_zuege=6),
    S("toto_smuggle_evening", "abend", [3, 6], "Boxes in the tender garage", "tender_garage", ["toto", "lea"], "22:30",
      "The tender garage, late. Totò is moving boxes. Lea is helping, because nobody told her not to. One box says \"potatoes\" and clinks. Totò smiles at Duc a little too widely.",
      "Does Duc ask what is in the boxes?",
      {"toto": "Finish before anyone asks questions.",
       "lea": "Help, and find out what the secret is."},
      [A("Duc lets it go and helps.", W("draht", 1), {"geld": 50, "text": "Totòs Dank"}),
       A("Duc stops it and sends Lea to bed.", W("vertrauen.lea", 1), W("draht", -1))], max_zuege=6),
    S("alva_karaoke", "abend", [2, 6], "Karaoke at Alva's", "alvas_bar", ["alva", "chiara", "lea"], "22:00",
      "Alva has found an old karaoke machine. The village fishermen sing Corsican songs. Lea wants to sing ABBA. Chiara says she will never sing in public. Then she takes the microphone.",
      "Does Duc sing - and with whom?",
      {"alva": "Make this the loudest night of the summer.",
       "chiara": "Sing once, and pretend she didn't.",
       "lea": "Get everyone to sing with her."},
      [A("Duc sings a duet.", W("moral", 1), W("begehren.chiara", 1)),
       A("The whole bar sings together.", W("ruf", 1), W("vertrauen.lea", 1))], max_zuege=6),
]

# ======================================================================== RESERVE (wiederholbar, nur wenn sonst zu wenig da ist)
POOL += [
    S("reserve_morning", "fruehstueck", [2, 7], "Morning briefing", "crew_mess", ["chiara", "rosi", "sophia"], "07:30",
      "Crew mess, coffee from the camping stove. Battery: {strom} out of ten, diesel: {diesel}. Everyone waits for the day's orders.",
      "What does Duc put first today?",
      {"chiara": "Get a clear plan for the day.", "rosi": "Get time and power for the drive.", "sophia": "Get sent ashore."},
      [A("Duc gives clear orders for the day.", W("moral", 1)),
       A("Duc lets Rosi have the morning for the drive.", U("reparatur", 1))],
      art="reserve", einmalig=False, max_zuege=5),
    S("reserve_deck", "tag", [2, 7], "Deck work", "sun_deck", ["lea", "rosi"], "14:00",
      "Sun deck in the heat. Salt on everything, a list of small jobs as long as Rosi's arm. Lea has already started, badly.",
      "Does Duc get his hands dirty with them?",
      {"lea": "Make the work fun.", "rosi": "Get it done properly."},
      [A("The jobs get done.", W("strom", 1)), A("They laugh while they work.", W("moral", 1))],
      art="reserve", einmalig=False, max_zuege=6),
    S("reserve_shore", "tag", [2, 7], "Errands ashore", "village_harbour", ["sophia"], "11:00",
      "The quay of Cala d'Orsu. Sophia has a list: bread, ice, a spare fuse, and a favour to ask at the coast-guard post.",
      "What does Duc get done in the village?",
      {"sophia": "Get through her list and a little time with him."},
      [A("They get everything on the list.", W("ruf", 1)), A("Sophia enjoys the walk with him.", W("vertrauen.sophia", 1))],
      art="reserve", einmalig=False, max_zuege=6),
    S("reserve_dinner", "dinner", [2, 7], "Crew dinner", "crew_mess", ["chiara", "lea", "rosi"], "20:00",
      "Dinner by headlamp. Pasta again. Battery: {strom} out of ten. Somebody has to say something about tomorrow.",
      "How does Duc end the day with his crew?",
      {"chiara": "Get one evening without bad news.", "lea": "Talk about tomorrow.", "rosi": "Eat and go back to work."},
      [A("Duc keeps the mood up.", W("moral", 1))],
      art="reserve", einmalig=False, max_zuege=5),
    S("reserve_cards", "abend", [2, 7], "Cards in the crew mess", "crew_mess", ["lea", "rosi"], "22:00",
      "Crew mess, one lamp, a pack of cards with the queen of hearts missing. Lea deals. Rosi counts every point out loud.",
      "Who wins tonight?",
      {"lea": "Win, loudly.", "rosi": "Win, and keep score."},
      [A("Duc wins a round.", W("moral", 1)), A("Duc lets the women win.", W("vertrauen.lea", 1))],
      art="reserve", einmalig=False, max_zuege=6),
    S("reserve_aft", "abend", [2, 7], "Wine on the aft deck", "aft_deck", ["sophia", "chiara"], "22:30",
      "Aft deck, the last bottle of guest wine nobody will miss, the village lights across the water.",
      "What do they talk about when nobody is listening?",
      {"sophia": "Hear what he is really thinking.", "chiara": "Rate the day honestly, for once."},
      [A("They talk late into the night.", W("moral", 1))],
      art="reserve", einmalig=False, max_zuege=6),
    S("reserve_watch", "nacht", [2, 7], "Night watch", "bridge", ["$abend"], "02:00",
      "Bridge, two in the morning. The anchor alarm glows green. Battery: {strom} out of ten. Whoever Duc spent the evening with comes up with tea.",
      "Does she stay until the watch ends?",
      {"*": {"will": "Stay a little longer than she should."}},
      [A("She stays until the end of the watch.", W("energie", -1))],
      art="reserve", einmalig=False, max_zuege=6, begruendung="Whoever Duc spent the evening with comes up to the bridge."),
]

# ======================================================================== KUERZER: Nebenszenen hoechstens 6 Zuege (16.10.2026)
for _e in POOL:
    if _e.get("art") in ("plot", "drama", "job", "hinweis", "reserve") and _e["szene"].get("max_zuege", 8) > 6:
        _e["szene"]["max_zuege"] = 6

# ======================================================================== ANDENKEN: feste Gegenstaende an Bogen-Stufe 3
ANDENKEN = {"rosi_workshop_name": "rosi_spanner", "chiara_exam": "chiara_starchart", "sophia_manuscript": "sophia_page",
            "lea_margot": "lea_shell", "siri_the_call": "siri_knot"}
for _e in POOL:
    if _e["id"] in ANDENKEN:
        _e["szene"]["immer"] = [I(ANDENKEN[_e["id"]])]

# ======================================================================== VORLAGEN fuer Wendepunkte
def V(titel, ort, anwesend, zeit, lage, frage, figuren, ausgaenge, max_zuege=8, begruendung=None, wahlmoment=None):
    s = {"titel": titel, "ort": ort, "anwesend": anwesend, "zeit": zeit, "ausgangslage": lage, "frage": frage,
         "figuren": figuren, "ausgaenge": ausgaenge, "max_zuege": max_zuege}
    if begruendung:
        s["begruendung_ort"] = begruendung
    if wahlmoment:
        s["wahlmoment"] = wahlmoment
    return s


NAH = [A("She stays close all night.", W("vertrauen.%s", 1), W("begehren.%s", 1))]


def nah(pid, *mehr):
    return [A(a["wenn"], *[dict(f, wert=f["wert"] % pid) if "wert" in f else f for f in a["folgen"]]) for a in NAH] + list(mehr)


STURM = {
    "chiara": V("Storm night", "duc_cabin", ["chiara"], "01:00",
        "The storm hits at midnight. Forty knots, the boat swinging on two anchors, rain like gravel on the deck. Chiara knocks on Duc's door in her old football shirt, a torch in her hand: her cabin porthole leaks, her bunk is soaked. She says it like a report. She is shaking, and not from the cold.",
        "Does Duc let Chiara stay - and does she admit she hates storms?",
        {"chiara": "Sleep somewhere dry. That's all. That is absolutely all."}, nah("chiara"), begruendung="Chiara's cabin leaks; Duc's single cabin is the only dry one."),
    "sophia": V("Storm night", "duc_cabin", ["sophia"], "01:00",
        "The storm hits at midnight. The boat groans on its anchors. Sophia knocks on Duc's door in silk pyjamas, a bottle of wine and two glasses in her hands. 'The crew cabins are a drum in this. Yours has the only thick door. I'm told.'",
        "Does Duc let Sophia stay - and see what's under the charm tonight?",
        {"sophia": "Get through the storm with company, and make it look like a whim."}, nah("sophia"), begruendung="Sophia escapes the noisy crew cabins to Duc's cabin."),
    "lea": V("Storm night", "duc_cabin", ["lea"], "01:00",
        "The storm hits at midnight. Lea has been on deck in her foul-weather jacket for an hour, checking the anchor chain, soaking and thrilled. When she finally comes below she knocks on Duc's door, dripping. 'The chain held. I counted every jerk. Can I tell you about it? I can't sleep. Not tonight.'",
        "Does Duc let Lea stay - and what is under the excitement?",
        {"lea": "Share the storm with him, every second of it."}, nah("lea"), begruendung="Lea comes off deck and knocks on Duc's door."),
    "rosi": V("Storm night", "duc_cabin", ["rosi"], "01:00",
        "The storm hits at midnight. The batteries drop by the minute. Rosi comes to Duc's door with her tablet and the battery curve, wet hair, coverall over a tank top. 'Your cabin has the only working monitor. I need to watch the curve. All night.' She sits down on his floor and does not leave.",
        "Does Duc stay up with Rosi - and does she admit she's scared for the boat?",
        {"rosi": "Watch the batteries all night, near him, for purely technical reasons."}, nah("rosi"), begruendung="Rosi needs the monitor in Duc's cabin to watch the battery curve."),
    "siri": V("Storm night", "duc_cabin", ["siri"], "01:00",
        "The storm hits at midnight. Yasin sleeps through it, drunk. Siri doesn't. She comes down the crew stairs, where guests never go, in her father's wool sweater, and knocks on Duc's door. 'I'm sorry. I know I'm not allowed down here. I just... don't want to be alone in this.'",
        "Does Duc let Siri stay - guest, rules, and Yasin upstairs?",
        {"siri": "Not be alone in the storm; not break anything she can't fix."}, nah("siri", A("Siri tells Duc about the nightmare she keeps having.", U("siri_marke", 1))), begruendung="Siri comes below deck to Duc's cabin in the storm."),
}

FESTA = {}
for pid, (lage, will) in {
    "chiara": ("The piazza of Cala d'Orsu, festoon lights, a band, the whole village. Chiara in champagne silk with her hair down for once, and for once not organising anything. She takes Duc's arm as if she had always done it. 'Rate the festa. Out loud. I want to hear you do it.'",
               "Be at a party she didn't organise, with him, and enjoy it."),
    "sophia": ("The piazza of Cala d'Orsu, festoon lights, accordion music. Sophia knows half the village already and introduces Duc to all of them. Then she pulls him away into a side street where the music is softer. 'I have spent the whole evening being charming. I'd like five minutes of not.'",
               "Have five minutes with him where she doesn't perform."),
    "lea": ("The piazza of Cala d'Orsu. Lea's first festa ever. She tries everything: the chestnut cake, the myrtle liqueur, the dance with the old men. Then she grabs Duc's hand and pulls him into the circle. 'I don't know the steps. Nobody does. Come on!'",
            "Dance, laugh, and have this night with him."),
    "rosi": ("The piazza of Cala d'Orsu. Rosi in a lemon-yellow dress, hair down, no bandana, no tool belt, looking like she wants to hide behind a generator. 'Don't. Say. Anything.' A band starts a tarantella, the music of her childhood. Her foot is already tapping.",
             "Survive being seen in a dress, and dance once, with him."),
    "siri": ("The piazza of Cala d'Orsu. Siri came without Yasin, without her phone, in a silver dress she says she'll never wear again. Nobody here knows Siri Sea. A grandmother tells her she's too thin and gives her cake. She laughs, a real laugh. 'Nobody is filming. Dance with me before I remember who I am.'",
             "Be nobody for one night, with him."),
}.items():
    FESTA[pid] = V("La Festa", "village_piazza", [pid], "22:00", lage, "How does the night of the festa end?",
                   {pid: will}, [A("They dance.", W("begehren.%s" % pid, 1), W("ruf", 1)),
                                 A("She kisses Duc.", W("begehren.%s" % pid, 1), W("vertrauen.%s" % pid, 1))])
for _pid in FESTA:
    FESTA[_pid]["immer"] = [I("festa_medal")]
FESTA["siri"]["ausgaenge"].append(A("Siri says she is going to end it with Yasin.", F("siri_frei"), U("siri_marke", 2)))

NACHT6 = {}
for pid, (ort, lage, will) in {
    "chiara": ("bridge", "The night before the last day. The bridge, the sextant on the chart table, the stars sharp after the storm. Chiara takes a perfect sight on her own and checks it against the GPS. It's right. She doesn't say anything. She just turns around and looks at Duc.", "Have this night, without a single score."),
    "sophia": ("duc_cabin", "The night before the last day. Sophia comes to Duc's cabin without wine, without a joke, with her notebook. She puts it on his bunk. 'Read the last page. It's about you. Then decide what to do with me.'", "Be seen, all of her, once."),
    "lea": ("swim_platform", "The night before the last day. The water glows with every movement. Lea, in the water already, holds out her hand from the swim ladder. 'One last swim. The sea is lit up tonight. You have to see it from inside.'", "Have one perfect night before everything changes."),
    "rosi": ("generator_room", "The night before the last day. The generator room, Unit-01 humming loud enough to cover anything. Rosi takes off the bandana. 'Nobody comes down here at night. Nobody.' She doesn't call it a duel tonight.", "Stop counting. For one night."),
    "siri": ("solar_deck", "The night before the last day. The solar deck, no phone, no ring light. Siri in her father's sweater, barefoot, sitting so close her shoulder touches Duc's. 'Tomorrow I'm Siri Sea again. Or I'm not. Tonight I'm just me. Is that enough?'", "Have one night as herself, with him."),
}.items():
    NACHT6[pid] = V("The night before", ort, [pid], "00:30", lage, "How far does the last quiet night go?",
                    {pid: will}, [A("They spend the night together.", W("begehren.%s" % pid, 2), W("vertrauen.%s" % pid, 1))])

FEUER = V("Fire", "crew_corridor", ["rosi", "chiara", "lea"], "03:10",
    "Ten past three. The battery alarm, then a sound no alarm makes: a crack, a hiss, then smoke from the power room, thick and chemical. Rosi is already running towards it with an extinguisher. Chiara is banging on every cabin door. Lea has the life raft bag on her shoulder. The Eden Rise is on fire.",
    "Does everyone get off the boat - and what does Duc save?",
    {"rosi": "Fight the fire. Her batteries, her boat. Not leave.",
     "chiara": "Get every single person off the boat, in order, now.",
     "lea": "Get the life raft in the water and the crew into it."},
    [A("Duc orders everyone off the boat.", W("moral", 1)),
     A("Duc pulls Rosi away from the fire.", W("vertrauen.rosi", 2))], max_zuege=6)

FINALE = {
    "reparatur": V("Last night", "bridge", [], "20:00",
        "The last evening. The anchor comes up, chain rattling. On the radio, Rosi from the power room: 'Drive is live. Officer. It's live.' The Eden Rise turns on her own power for the first time in a week, bow towards Calvi, the season bonus safe, and on the quay of Cala d'Orsu the whole village is waving: Elsa on her patrol boat with the sunglasses pushed up, Alva with a bottle, Petru on his boat. {partner} stands next to Duc on the bridge.",
        "What does Duc say as the Eden Rise leaves the bay under her own power?",
        {}, [A("Duc thanks the crew over the PA.", W("moral", 2))], max_zuege=6),
    "rettung": V("Last night", "aft_deck", [], "20:00",
        "The last evening. A tug from Ajaccio appears around the point, orange and ugly and beautiful. The crew lines the rail. It is not the ending anyone wanted: eighty thousand euros, the whole season bonus, gone. Everyone is relieved anyway. The tow line comes over. {partner} stands next to Duc at the stern as the Eden Rise starts to move behind a stranger's boat.",
        "What does Duc say as they are towed out of the bay?",
        {}, [A("Duc tells the crew they did everything they could.", W("moral", 2))], max_zuege=6),
    "katastrophe": V("Last night", "village_harbour", [], "20:00",
        "The last evening, on the quay of Cala d'Orsu. Bandages, borrowed clothes, Alva's blankets. Out in the bay the Eden Rise is a black, smoking hull. Everyone got off. Everyone is hurt. Nobody is dead. Petru brought them in on his fishing boat in the dark. {partner} sits next to Duc on the harbour wall, wrapped in a blanket that smells of fish.",
        "What is left when the boat is gone?",
        {}, [A("Duc tells the crew that they are what mattered.", W("moral", 2))], max_zuege=6),
}

EPILOG = {
    "chiara": V("Morning after", "bridge", ["chiara"], "06:30", "Dawn after the last night. Chiara stands at the helm in her grandfather's jacket. Duc put her there. She hasn't said anything for ten minutes, which is a record. Then: 'Ten. For the record. The week. Ten.'", "What happens to them now?", {"chiara": "Ask him what happens next, and be brave about the answer."}, []),
    "sophia": V("Morning after", "aft_deck", ["sophia"], "06:30", "Dawn. Sophia sits at the long table with her laptop and a coffee. A new file, open: Chapter One. The first sentence is about a man who wanted to fix everything alone. She turns the screen to Duc. 'May I?'", "What happens to them now?", {"sophia": "Ask him if he will be in the book, and in her life."}, []),
    "lea": V("Morning after", "foredeck", ["lea"], "06:30", "Dawn on the foredeck. Lea has Petru's chart in her lap, a cross drawn off the Esterel. 'Next season,' she says. 'Will you come diving? Just once. I want you there when I find it.'", "What happens to them now?", {"lea": "Ask him to come back, without asking him to stay."}, []),
    "rosi": V("Morning after", "workshop", ["rosi"], "06:30", "Dawn in the workshop. On the whiteboard the score has been wiped clean, and in its place, in Rosi's handwriting: DRAW. She hands Duc a coffee and doesn't look at him. 'Papa's workshop. Catania. Four more seasons. Or three, if someone helps.'", "What happens to them now?", {"rosi": "Find out if the officer is in her plan."}, []),
    "siri": V("Morning after", "solar_deck", ["siri"], "06:30", "Dawn on the solar deck. Siri in her father's sweater, her phone switched off, a ferry ticket to Trondheim in her hand. 'Pappa said I can come home. He said bring the man who fixes things.' She laughs and cries at once.", "What happens to them now?", {"siri": "Ask Duc if he would come to the island."}, []),
    "allein": V("Morning after", "solar_deck", ["rosi"], "06:30", "Dawn. Duc sits alone on the solar deck. Footsteps: Rosi, coverall, bandana, a box of cereal. She sits down a metre away, holds out the box without looking at him. 'Three pieces. I'm counting.'", "What happens next for Duc?", {"rosi": "Keep him company without making it a thing."}, []),
}

KONFRONTATION = {
    "szene": V("Who did it?", "crew_mess", ["chiara", "sophia", "lea", "rosi"], "07:30",
        "The morning after the storm. The crew mess, the clues on the table: everything Duc has found about the blackout. Everyone knows why they are here. Nobody touches the coffee. Duc is the commander. Today he says what he thinks happened - or doesn't.",
        "Who does Duc accuse - and is he right?",
        {"chiara": "Get through this morning with her dignity.",
         "sophia": "Keep the crew from tearing itself apart.",
         "lea": "Know the truth, whatever it costs.",
         "rosi": "Defend her boat and her crew."}, [], max_zuege=8),
    "frage": "Everyone is looking at you. Who caused the blackout?",
    "optionen": {
        "defekt": {"text": "Nobody. The inverter was faulty.", "handlung": "He says it was a faulty part, nobody's fault, and shows the evidence."},
        "chiara": {"text": "Chiara. She was on the bridge that night.", "handlung": "He says Chiara was on the bridge that night and caused it."},
        "lea": {"text": "Lea. She changed the course.", "handlung": "He says Lea changed the course that night and drained the batteries."},
        "sophia": {"text": "Sophia. She rushed the passage.", "handlung": "He says Sophia moved the passage forward for her own reasons."},
        "wette": {"text": "Someone from the engine room, for the bet.", "handlung": "He says someone switched off a breaker for the betting board."},
        "yasin": {"text": "Yasin. His charger in the VIP cabin.", "handlung": "He says Yasin's charging gear in the VIP cabin caused the short."}},
    "schweigen": {"text": "Accuse nobody. Not yet.", "handlung": "He says he won't accuse anyone without proof, not today."},
    "aufloesung": {
        "defekt": "Aufgelöst: ein fehlerhaftes Bauteil, niemand ist schuld. Petru kennt einen Händler in Ajaccio.",
        "chiara": "Aufgelöst: Chiara hat nachts auf der Brücke geübt und dafür den Batterieschutz überbrückt.",
        "lea": "Aufgelöst: Lea hat heimlich Kurs auf die Margot-Koordinaten gesetzt.",
        "sophia": "Aufgelöst: Sophia hat den Halt in Cala d'Orsu für ihren Verlag eingefädelt.",
        "wette": "Aufgelöst: Rosi hat für die Wette eine Sicherung gezogen - es ging viel weiter als gedacht.",
        "yasin": "Aufgelöst: Yasins Ladegerät hat den Kurzschluss ausgelöst."},
    "belohnung": {
        "defekt": [U("reparatur", 2)],
        "chiara": [U("reparatur", 1), W("vertrauen.chiara", 1)],
        "lea": [U("reparatur", 1), F("margot_koordinaten")],
        "sophia": [U("rettung", 2), W("vertrauen.sophia", 1)],
        "wette": [U("reparatur", 2), W("begehren.rosi", 1)],
        "yasin": [F("video_gestoppt"), U("siri_marke", 2)]},
    "strafe": {
        "defekt": [W("moral", -1)],
        "chiara": [W("vertrauen.chiara", -2), W("moral", -1)],
        "lea": [W("vertrauen.lea", -2), W("moral", -1)],
        "sophia": [W("vertrauen.sophia", -2), W("moral", -1)],
        "wette": [W("vertrauen.rosi", -2), W("moral", -1)],
        "yasin": [W("vertrauen.siri", -1), W("moral", -1)]},
}

PONR = V("Point of no return", "crew_mess", ["chiara", "rosi", "sophia"], "07:00",
    "Day six. One canister of diesel, maybe enough for one real run of Unit-01. The battery barely holds through the night. Rosi wants everything for the drive. Sophia says Ajaccio is close to sending a tug if someone keeps the radio warm. Chiara wants Duc to decide, now, so she can organise it.",
    "Where does Duc put the last resources: repair or rescue?",
    {"chiara": "Get a decision she can organise.",
     "rosi": "Get the diesel for Unit-01 and the drive.",
     "sophia": "Get the radio and the tug."}, [], max_zuege=6,
    wahlmoment=WM("The last diesel, the last good power. Where does it go?",
        O("Unit-01 and the drive. We sail out ourselves.", "He decides: the last diesel goes into Unit-01 and the drive.", [W("diesel", -1), U("reparatur", 2), W("vertrauen.rosi", 1)]),
        O("The radio. We get the tug.", "He decides: the power goes into the radio, they get the tug.", [W("strom", -1), U("rettung", 2), W("vertrauen.sophia", 1)]),
        O("Split it. Half and half.", "He decides to split it: a little for the drive, a little for the radio.", [U("reparatur", 1), U("rettung", 1)])))
PONR_OHNE_DIESEL = O("Unit-01 on Petru's last canister.", "He asks Petru for his last canister of diesel for Unit-01.", [W("ruf", -1), U("reparatur", 1), W("vertrauen.rosi", 1)])

PERSONA_WAHL = {"nach_zug": 1, "frage": "Frankfurt wants an answer today. What do you tell them?", "optionen": [
    {"text": "I'm coming back.", "handlung": "He calls Frankfurt and says he is coming back.", "folgen": [F("persona_frankfurt")]},
    {"text": "One more season at sea.", "handlung": "He tells Frankfurt no: one more season at sea.", "folgen": [F("persona_see")]},
    {"text": "Wherever she goes.", "handlung": "He tells Frankfurt no, and tells her he is staying with her.", "folgen": [F("persona_mit_ihr")], "nur_mit_partner": True}]}

# ======================================================================== Steuerung
INHALT = {
    "_hinweis": "Gebaut aus werkzeuge\\szenen_gestrandet.py (16.10.2026) - dort aendern.",
    "pool": POOL,
    "jobs": JOBS,
    "vorlagen": {"sturm": STURM, "festa": FESTA, "nacht6": NACHT6, "feuer": FEUER, "finale": FINALE, "epilog": EPILOG,
                 "konfrontation": KONFRONTATION, "ponr": PONR, "ponr_ohne_diesel": PONR_OHNE_DIESEL,
                 "persona_wahl": PERSONA_WAHL},
    "fixplan": {"3/nacht": "sturm", "4/fruehstueck": "konfrontation", "5/abend": "festa", "6/fruehstueck": "ponr"},
    "dynamisch": {"6/nacht": "nacht6", "7/abend": "finale", "7/nacht": "epilog"},
    "standard_ausgang": "rettung",
    "herz_schwelle": {"vertrauen": 4, "begehren": 4},
    "uhr_soll": {"reparatur": 1.3, "rettung": 0.9},
    "takt": {"strom": {"klar": 1, "bewoelkt": -1, "sturm": -2}},
    "wetter_text": {"klar": "a clear, hot day", "bewoelkt": "a grey, cloudy day", "sturm": "a storm coming in from the west"},
    "wetter_spieler": {"klar": "Wetter: klar, die Paneele laden.", "bewoelkt": "Wetter: bewölkt, kaum Sonnenstrom.", "sturm": "Wetter: Sturm am Abend."},
    "tage": {
        "2": {"spannung": "Tag 2 - Cala d'Orsu. Das Dorf wird zur Lebensader: Diesel, Teile, Erlaubnis. Erste Spur zur Ursache.",
              "spieler": "Tag 2: Cala d'Orsu. Ihr braucht Diesel, Teile und Freunde im Dorf. Noch 6 Tage bis Calvi."},
        "3": {"spannung": "Tag 3 - Sturmnacht. Vorbereiten am Tag, zusammenrücken in der Nacht.",
              "spieler": "Tag 3: Für heute Nacht ist ein Sturm angesagt. Noch 5 Tage bis Calvi."},
        "4": {"spannung": "Tag 4 - Wer war es? Die Konfrontation am Morgen, danach Aufräumen in jeder Hinsicht.",
              "spieler": "Tag 4: Heute sagst du, was du über den Ausfall denkst. Noch 4 Tage bis Calvi."},
        "5": {"spannung": "Tag 5 - La Festa. Das Dorf feiert, die Crew darf atmen. Wer geht mit wem?",
              "spieler": "Tag 5: Heute Abend ist Festa im Dorf. Noch 3 Tage bis Calvi."},
        "6": {"spannung": "Tag 6 - Point of no return. Die letzten Ressourcen, die letzte ruhige Nacht.",
              "spieler": "Tag 6: Der letzte Diesel. Aus eigener Kraft nach Calvi oder der Schlepper?"},
        "7": {"spannung": "Tag 7 - Letzte Nacht. Was voll ist, entscheidet. Dann: wer steht neben ihm.",
              "spieler": "Tag 7: Der letzte Tag in Cala d'Orsu. Heute entscheidet sich, wie ihr nach Calvi kommt."}},
    "verbirgt": {
        "chiara": "She failed the Yachtmaster theory exam in April and studies at night on the bridge with her grandfather's sextant; and she expected Holm to give her the command.",
        "sophia": "She writes crime novels at night as M. J. Penrose (fourteen rejections) and turned down Chiara's job last winter without telling her.",
        "lea": "She dives alone at night, searching for her grandfather's wreck, the Margot, and has secretly applied for an Azores expedition.",
        "rosi": "She wrote her own name at the bottom of the betting board, forty to one, and saves every euro to buy back her father's workshop in Catania.",
        "siri": "She is no longer sure she wants any of it - the brand, the boyfriend, the life - and carries her father's sweater everywhere.",
        "yasin": "His money is thinner than it looks; this charter is on credit."},
    "schuld": {"chiara": "chiara", "lea": "lea", "sophia": "sophia", "wette": "rosi", "yasin": "yasin"},
    "schuld_vage": "She has a private reason to feel guilty about the night of the blackout, and she won't say it.",
    "will_standard": {
        "chiara": "Keep the boat and the crew running and be taken seriously by the new commander.",
        "sophia": "Make things happen for the crew, and find out who this officer really is.",
        "lea": "Be useful, see everything, and be near him.",
        "rosi": "Keep her machines alive, save the season bonus, and win against the officer.",
        "siri": "Be polite, be useful, and not be Siri Sea for a moment.",
        "yasin": "Get his content and his comfort, and be the most important man aboard.",
        "elsa": "Do it by the book, bend a rule if it is worth it, and catch Toto at something.", "alva": "Know everything and like the right people.",
        "petru": "Say little and fix things.", "casanova": "Get the best for her village."},
}


def main():
    if os.path.exists(ZIEL):
        shutil.copy2(ZIEL, ZIEL + ".bak-" + time.strftime("%Y%m%d_%H%M%S"))
    json.dump(INHALT, open(ZIEL, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("geschrieben: %s | %d Pool-Szenen | Vorlagen: %s" % (ZIEL, len(POOL), ", ".join(INHALT["vorlagen"])))


if __name__ == "__main__":
    main()
