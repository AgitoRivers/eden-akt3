# -*- coding: utf-8 -*-
r"""Buehnenfassung der Hauptstory eden_rise -> module\eden_rise\buehne.json (Phase B2, 17.10.2026).

story.json (vertraulich) sagt, WAS in einer Szene passiert (kern = Regie-Notiz, nur fuers Sprachmodell).
Hier steht, wie die Szene auf die Buehne kommt - alles, was Duc sieht oder was die Figuren spielen:
  zeit, ort, anwesend, ausgangslage (englisch, spoilerfrei, kurze Saetze), frage, will je Figur, max_zuege,
  wahl (Entscheidung mit festen Folgen) und immer (Folgen am Szenenende, z. B. Flags aus story "setzt").
Fallabhaengige Einschuebe (Wissen, Widersprueche, Gegenhandlungen) kommen in B3/B4 aus story.json dazu - hier nie.
Szenen ohne Eintrag hier spielt kern\hauptstory.py nicht (z. B. reine Ermittlungs-Aktionen, B3).

    python story_buehne.py      schreibt module\eden_rise\buehne.json
"""
import json, os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
ZIEL = os.path.join(os.path.dirname(os.path.dirname(HIER)), "module", "eden_rise", "buehne.json")


def F(flag):
    return {"flag": flag}


def V(pid, d=1):
    return {"wert": "vertrauen." + pid, "delta": d}


def O(text, handlung, *folgen):
    return {"text": text, "handlung": handlung, "folgen": list(folgen)}


def WM(frage, *optionen, nach=1):
    return {"nach_zug": nach, "frage": frage, "optionen": list(optionen)}


B = {}

# ======================================================================== Tag 1 - Cold Open und Party
B["cold_open"] = dict(
    zeit="06:35", ort="power_room", bild="yacht_power_room_smoke.png", anwesend=["rosi"], max_zuege=2,
    ausgangslage="06:35. A bang somewhere below deck. Smoke, sparks, an alarm that will not stop. A hand slams down on "
                 "a red button. Then darkness - and a line of white text: the day before. Antibes.",
    frage="The day before. Antibes.",
    will={"rosi": "Stop it. Now."})

B["auftakt_party"] = dict(
    zeit="20:30", ort="aft_deck", anwesend=["chiara", "rosi", "siri"], max_zuege=8,     # max. 3 Figuren: die drei der Wahl
    ausgangslage="The last night of the charter season. Lanterns on the aft deck, music, the sun sinking behind "
                 "Corsica. A banner over the bar reads EDEN BAY WEEKEND: tonight the Eden Rise sails for the bay of Cala "
                 "d'Orsu, to arrive at sunrise - Megan's idea. Siri will post the sunrise, Yasin will film the arrival "
                 "with his drone, and then it is on to the winter shipyard in Calvi. Lola swears the sea will glow "
                 "tonight. Captain Holm holds a glass she does not drink from and calls the whole thing Megan's little "
                 "photo stop. Everyone needs something from the new First Officer at once.",
    frage="Who do you help first - and what else do you notice tonight?",
    will={"holm": "Enjoy the last night of her season and not show that her stomach hurts.",
          "chiara": "Run a perfect party service, one pair of hands short.",
          "rosi": "Get somebody to help with a quick test in the control room before she can party.",
          "siri": "Escape Yasin's camera for five minutes.",
          "lola": "Feed everyone and tell Duc about the glowing sea."},
    wahl=WM("Who do you help first?",
            O("Chiara – she is a pair of hands short at the service.", "He takes a tray and helps Chiara with the service.",
              F("auftakt_hilfe_chiara"), V("chiara")),
            O("Rosi – she needs someone for a quick test in the control room.",
              "He goes down with Rosi to help with her test in the control room.", F("auftakt_hilfe_rosi"), V("rosi")),
            O("Siri – she wants out of the recording for a moment.",
              "He gives Siri an excuse to step away from the camera for a moment.", F("auftakt_hilfe_siri"), V("siri"))))

B["blackout"] = dict(
    zeit="05:50", ort="galley", anwesend=["lola"], max_zuege=4,
    ausgangslage="The afterparty ended at half past three. Duc cannot sleep. He sits in the galley with Lola, who is "
                 "baking for a sunrise breakfast and humming along to the music from the deck. The yacht is under way "
                 "towards the bay of Cala d'Orsu, to be there by sunrise. Then the music stops.",
    frage="What does Duc do in the first minute?",
    will={"lola": "Finish her bread - until something is very wrong, and then not be alone with it."})

B["explosion"] = dict(
    zeit="06:35", ort="power_room", bild="yacht_power_room_smoke.png", anwesend=["maxwell", "rosi", "holm"],
    max_zuege=6,
    ausgangslage="06:35. Totò and Lea ran down to see what stopped. Then the bang - right here, in the inverter. "
                 "Something heavy comes loose. When the smoke clears, Maxwell is standing over Totò and Lea, debris on "
                 "his back, grinning. Rosi hits the emergency stop. Unit-01 keeps humming. Everyone is saying "
                 "\"the motor\".",
    frage="What does Duc do first?",
    will={"maxwell": "Turn the scare into a pose and make sure his little brothers and sisters are fine.",
          "rosi": "Stop the damage - and then sit with her machine a moment longer than anyone should see.",
          "holm": "Count every head, look after Lola, and not show how much it hurts - until she cannot any more."},
    immer=[F("explosion")])

B["wache_mit_holm"] = dict(
    zeit="06:50", ort="bridge", anwesend=["holm"], max_zuege=6,
    ausgangslage="The bridge in grey morning light. Holm collapsed below and came back up anyway. No drive. The Eden "
                 "Rise drifts towards the coast while Holm, pale with pain, gives quiet orders. Then she drops the anchor in a bay with a small fishing village. "
                 "For a moment it is just the two of them.",
    frage="What does Duc answer when the captain asks the real question?",
    will={"holm": "Get her ship safe at anchor, find out who her First Officer really is, and not admit how bad the "
                  "pain is."},
    wahl=WM("Who do you call when you don't know what to do next?",
            O("\"You.\"", "He says: \"You.\"", F("antwort_wache_holm")),
            O("\"My people here on board.\"", "He says: \"My people here on board.\"", F("antwort_wache_crew")),
            O("\"Nobody. I'll do it on my own.\"", "He says: \"Nobody. I'll do it on my own.\"", F("antwort_wache_niemand")),
            O("\"Somebody in Frankfurt.\"", "He says: \"Somebody in Frankfurt.\"", F("antwort_wache_frankfurt")), nach=2))

# ======================================================================== Tag 2 - Gestrandet
B["lage_mit_holm"] = dict(
    zeit="08:30", ort="bridge", anwesend=["holm", "rosi", "chiara"], max_zuege=6,
    ausgangslage="The morning after. The Eden Rise lies at anchor in the bay of Cala d'Orsu. The inverter is wrecked, the "
                 "drive is dead; the hotel side runs on the batteries. Holm calls a briefing on the bridge, one hand pressed to her side. "
                 "Rosi has the numbers, Chiara has thirteen people to look after. The company has already called twice.",
    frage="What do you give up first to save power?",
    will={"holm": "Run one last briefing and see what her First Officer is made of.",
          "rosi": "Make everyone understand what still works and what does not.",
          "chiara": "Keep thirteen people fed, clean and calm.",
          "sophia": "Pass on the company's message without starting a panic."},
    wahl=WM("What do you give up first?",
            O("Cold showers for everyone.", "He decides: cold showers for everyone until further notice.", F("komfort_dusche")),
            O("Half the cooling.", "He decides: the cold rooms run at half power.", F("komfort_kuehlung")),
            O("No more recordings for Yasin.", "He decides: Yasin's recording gear stays off.", F("komfort_aufnahme")), nach=2))

B["megan_erster_anruf"] = dict(
    zeit="09:10", ort="bridge", anwesend=["megan", "holm"], max_zuege=5,
    ausgangslage="A video call on the big bridge screen. Megan McAllister, Fleet Director of the Eden Group, is "
                 "furious - too loud, too fast, a coffee cup flies out of frame. \"You were supposed to be my "
                 "postcard!\" Then she goes ice cold and sets her terms.",
    frage="How does Duc meet the Fleet Director?",
    will={"megan": "Seven days: a report on the cause and a hearing on board with her as judge. No culprit, no crew - "
                   "she fires all of them.",
          "holm": "Hand over without being pushed aside, and stand up for her crew one last time."},
    immer=[F("megan_ultimatum")])

B["holm_ansprechbar"] = dict(
    zeit="09:40", ort="bridge", anwesend=["holm"], max_zuege=4,
    ausgangslage="The helicopter is twenty minutes out. Holm sits in the captain's chair one last time. She has a "
                 "moment for questions - if Duc asks the right ones.",
    frage="What does Duc want to know from the captain?",
    will={"holm": "Leave her ship in good hands and answer exactly what she is asked."})

B["holm_abschied"] = dict(
    zeit="10:05", ort="sun_deck", bild="yacht_sun_deck_helicopter.png", anwesend=["holm"], max_zuege=4,
    ausgangslage="The rescue helicopter hovers over the sun deck. Appendicitis. Holm is strapped to a stretcher and "
                 "still giving orders. Before they lift her, she looks for Duc one last time.",
    frage="What does Duc say to her before she goes?",
    will={"holm": "Hand over her ship and remind Duc of his answer from last night."},
    immer=[F("holm_evakuiert"), F("kommando_duc")])        # Kompass ab Holms Vertrauen 2 (kern/ermittlung.py)

B["der_freie_platz"] = dict(
    zeit="10:30", ort="crew_mess", anwesend=["chiara"], max_zuege=4,
    ausgangslage="The crew mess after the helicopter. There are too many cups on the table. Chiara reaches for "
                 "the one that belonged to the captain.",
    frage="What does Duc do?",
    will={"chiara": "Keep the room tidy, because tidy feels like control."},
    wahl=WM("The extra cup",
            O("\"Leave it there.\"", "He says quietly: \"Leave it there.\"", F("freier_platz_stehen")),
            O("Clear it away yourself.", "He picks up the cup and puts it away himself.", F("freier_platz_selbst")),
            O("Get straight to the situation.", "He moves straight on to the situation.", F("freier_platz_lage"))))

B["erste_ermittlung"] = dict(
    zeit="11:30", ort="power_room", anwesend=["rosi"], max_zuege=6,
    ausgangslage="Command is Duc's now. Rosi has the power room open, cables everywhere, the burnt smell still in the "
                 "air. There is so much to do and only one morning.",
    frage="Where does Duc start?",
    will={"rosi": "Understand her machine and not be told how to do her job."},
    wahl=WM("Where do you start?",
            O("Secure the event log of the power control.", "He asks Rosi to secure the event log of the power control "
              "before anything is changed.", F("erste_streifen")),
            O("Talk to someone about the night.", "He sits down with Rosi and asks her about the night.", F("erste_gespraech")),
            O("Get the supply organised first.", "He decides the supply comes first: water, cooling, food.",
              F("erste_versorgung"), {"wert": "moral", "delta": 1})))

B["widerspruch"] = dict(                     # Besetzung je Fall ($fall3, kern/ermittlung.besetzung), gemischt
    zeit="21:00", ort="crew_mess", anwesend=["$fall3"], max_zuege=6,
    ausgangslage="Back on board. Dinner by headlamp. People talk about the night, each from where they were. "
                 "Somewhere in all of it, something does not add up.",
    frage="What does Duc do with what he hears?",
    will={"*": "Talk about the night from where you were - in your own way."})

# ======================================================================== Tag 3 - Die Bucht
B["sonnenaufgang"] = dict(
    zeit="06:20", ort="foredeck", anwesend=["$naehe"], max_zuege=4,
    ausgangslage="The first quiet morning. The sun comes up over Cala d'Orsu: fishing boats, church bells from the "
                 "village, the water turning from grey to gold. A seagull with an attitude sits on the rail. Nothing "
                 "needs fixing for ten minutes.",
    frage="What does Duc do with ten quiet minutes?",
    will={"*": "Share the sunrise with Duc without talking about the night."})

B["landgang"] = dict(
    zeit="11:00", ort="village_harbour", anwesend=["alva", "elsa", "casanova"], max_zuege=8,
    ausgangslage="The tender to Cala d'Orsu. Three hundred people saw the yacht drift in - and yesterday they saw Duc "
                 "drive the animals off their quay. The faces from that chaos are waiting: Alva from the only bar, "
                 "Lieutenant Ferrandi from the coast guard, old Petru who says nothing, and the mayor, who already has "
                 "plans. Duc has time for one thing now and one tonight.",
    frage="What does Duc do first in the village?",
    will={"alva": "Find out who these people are and what they will need.",
          "elsa": "Get a factual report on the state of the yacht.",
          "petru": "Find out what exactly they have already checked.",
          "casanova": "Win the stranded superyacht for her festa - with a big presentation."},
    wahl=WM("One thing now",
            O("Organise material (Alva, Petru).", "He asks Alva and Petru for help with parts and supplies.",
              F("vorhaben_material")),
            O("Check a lead ashore.", "He follows up on something he wants to check ashore.", F("vorhaben_spur")),
            O("Keep a personal promise.", "He keeps a promise he made to someone on board.", F("vorhaben_versprechen")), nach=2),
    immer=[F("alva_kennengelernt"), F("elsa_kennengelernt"), F("petru_kennengelernt")])


B["landgang_2"] = dict(
    zeit="19:30", ort="alvas_bar", anwesend=["alva"], max_zuege=5,
    ausgangslage="Alva's bar at dinner time. Fishermen at the counter, an old song on the radio. Duc has one more thing he "
                 "wanted to do today.",
    frage="What does Duc use the evening for?",
    will={"alva": "Close the bar late and hear everything."},
    wahl=WM("The second thing",
            O("Organise material.", "He uses the evening to organise material.", F("vorhaben_material")),
            O("Check a lead ashore.", "He uses the evening to check a lead.", F("vorhaben_spur")),
            O("Keep a personal promise.", "He uses the evening to keep a promise.", F("vorhaben_versprechen"))))

B["gemeinsames_essen"] = dict(
    zeit="21:00", ort="aft_deck", anwesend=["lola", "lea", "rosi"], max_zuege=6,
    ausgangslage="Lola's first dinner in the bay, cooked with whatever the village had - and somehow it is the best "
                 "thing anyone has eaten in days. Candles because of the power, the lights of Cala d'Orsu across the "
                 "water. Somebody laughs for the first time since the music stopped.",
    frage="What does Duc say when someone asks what really happened?",
    will={"lola": "Make everyone eat and laugh.", "lea": "Ask the question nobody else asks.",
          "rosi": "Eat and pretend she is not worried."})

B["naehe"] = dict(
    zeit="23:30", ort="duc_cabin", anwesend=["$naehe"], max_zuege=8,
    ausgangslage="The first evening in the bay is over. The yacht is quiet. Someone did not want to be alone tonight "
                 "and is sitting with Duc where nobody will walk in.",
    frage="How close do you let this night get?",
    will={"*": "Not be alone tonight - and decide for herself how far it goes."},
    wahl=WM("\"Tomorrow you'll ask me about tonight again.\"",
            O("\"Yes.\"", "He says: \"Yes.\"", F("naehe_ja")),
            O("\"Only if you want to talk.\"", "He says: \"Only if you want to talk.\"", F("naehe_nur_wenn")),
            O("…", "He doesn't answer.", F("naehe_ausweichen")), nach=4))

# ======================================================================== Tag 4 - Spuren
B["reparaturschritt"] = dict(
    zeit="18:00", ort="power_room", anwesend=["rosi"], max_zuege=6,
    ausgangslage="The whiteboard in the power room says ROSI VS. OFFICER in big letters. Today: emergency power and "
                 "the power room itself. Rosi has everything laid out. What they did in the last days decides "
                 "whether this works.",
    frage="Does the step work?",
    will={"rosi": "Make the machine do what she tells it to - and win the whiteboard."})

B["megan_ankuendigung"] = dict(
    zeit="21:30", ort="duc_cabin", anwesend=["megan"], max_zuege=4,
    ausgangslage="A video call in Duc's cabin. Megan is calm tonight, which is worse. Tomorrow she will come aboard "
                 "herself, and she will stay until the hearing.",
    frage="What does Duc tell her before she comes?",
    will={"megan": "Announce her visit and hear whether Duc is ready."},
    immer=[F("megan_angekuendigt")])

# ======================================================================== Tag 5 - Druck in Person
B["sturmvorbereitung"] = dict(
    zeit="18:00", ort="aft_deck", bild="yacht_aft_deck_storm_coming.png", anwesend=["chiara", "rosi", "lea"], max_zuege=7,
    ausgangslage="A storm is coming tonight, gusts to forty knots. Megan is aboard and watching. Lines and anchor, power, galley, tender, and "
                 "the makeshift supply that was rigged yesterday. Duc cannot be everywhere. He has to send people.",
    frage="Who does Duc send where - and what does he check himself?",
    will={"chiara": "Get a clear job and do it perfectly.", "rosi": "Save every amp for the night.",
          "lea": "Be trusted with something real."},
    immer=[F("sturm_vorbereitet")])

B["sturmnacht"] = dict(
    zeit="23:30", ort="aft_deck", bild="yacht_aft_deck_storm_night.png", anwesend=["chiara", "rosi", "lea"], max_zuege=8,
    ausgangslage="The storm hits after midnight. The yacht pitches at anchor, rain hammers the windows, the power "
                 "drops hard. Everyone has a place - if Duc gave them one.",
    frage="How does the crew get through the night?",
    will={"chiara": "Hold her post.", "rosi": "Keep the power alive.", "lea": "Watch the anchor and not be afraid."})

B["megan_kommt"] = dict(
    zeit="08:30", ort="crew_mess", anwesend=["chiara", "lola"], max_zuege=4,
    ausgangslage="Breakfast in a hurry. Chiara has the crew in uniform, Lola has baked as if for royalty. Somewhere "
                 "over the hills a helicopter is coming.",
    frage="How does Duc prepare the crew for the visit?",
    will={"chiara": "Make the yacht look perfect.", "lola": "Impress the boss with breakfast."},
    immer=[F("megan_besuch")])

B["megan_inspektion"] = dict(
    zeit="11:00", ort="power_room", anwesend=["megan", "rosi"], max_zuege=7,
    ausgangslage="Megan McAllister in white, a clipboard, no small talk. She walks the yacht and ends up in the "
                 "power room, where Rosi refuses to stand to attention.",
    frage="What does Duc show the Fleet Director - and what does he ask her?",
    will={"megan": "See the damage for herself and keep control of the story - and keep quiet about what she sees.",
          "rosi": "Explain her machine and not be blamed for it."},
    wahl=WM("What do you show her?",
            O("Everything - even what speaks against the crew.", "He shows Megan everything, even what speaks against "
              "his own crew.", F("inspektion_offen")),
            O("Hold something back.", "He keeps one thing back from Megan.", F("inspektion_beschoenigt")), nach=3))

B["leises_telefonat"] = dict(
    zeit="19:40", ort="sun_deck", anwesend=["megan"], max_zuege=4,
    ausgangslage="Wind is picking up. On the sun deck Megan is on the phone, half turned away, voice low. Duc hears "
                 "two letters, twice: \"A.V.\" and something about \"the buyer from Monaco\". Then she sees him.",
    frage="What does Duc do?",
    will={"megan": "End the call, become the boss again, and not explain."})

# ======================================================================== Gegenhandlung (Tag 3+, B4)
# Nur am Morgen nach einer Gegenhandlung mit sichtbarer Spur; Ort = wo sich etwas veraendert hat ($spur).
B["etwas_anders"] = dict(
    zeit="07:10", ort="$spur", anwesend=[], max_zuege=3,
    ausgangslage="Early morning, before breakfast. Duc passes a place he has already looked at closely. Something "
                 "is not the way he left it.",
    frage="What does Duc do about it?",
    will={})

# ======================================================================== Tag 6 - Letzte Spuren
B["lagerfeuer"] = dict(
    zeit="20:30", ort="swim_platform", bild="eden_rise_strand_lagerfeuer.png", anwesend=["lola", "maxwell", "toto"], max_zuege=8,
    ausgangslage="A fire on the little beach next to the yacht, the storm gone, the sky washed clean. Lola grills, "
                 "Maxwell tells a story about Maxwell, Totò takes bets on who falls asleep first. Tomorrow is the "
                 "hearing. Nobody talks about it - until somebody does.",
    frage="What does Duc share by the fire?",
    will={"lola": "Feed everyone and keep the mood up.",
          "maxwell": "Make everyone laugh and do push-ups for every joke.",
          "toto": "Run his book and not look at the hills."})

B["letzte_naehe"] = dict(
    zeit="22:30", ort="duc_cabin", anwesend=["$naehe"], max_zuege=8,
    ausgangslage="The last quiet evening before the hearing. Duc chose who to spend it with, and she came.",
    frage="What is said tonight?",
    will={"*": "Spend the evening with him and say one thing she means."})

# ======================================================================== Tag 7 - Die Anhoerung (Logik: Scheibe 3)
# Drei Szenen mit je einem Wahlmoment; die Optionen tragen "anhoerung" -> kern/anhoerung.py wertet aus.
# Anklage: die drei Anwesenden ($fall3, gemischt wie beim Widerspruch) plus "niemand allein" (= auch "kein Name");
# kern/hauptstory.py setzt die Optionen beim Bau der Szene ein (Wahlmoment hoechstens 4 Optionen).


def A(text, handlung, schritt, *folgen):
    o = O(text, handlung, *folgen)
    o["anhoerung"] = schritt
    return o


B["anhoerung"] = dict(
    zeit="11:00", ort="main_salon", bild="eden_rise_salon_anhoerung.png", anwesend=["megan", "$fall3"], max_zuege=8,
    ausgangslage="The main salon, rearranged into a courtroom by Chiara at dawn. Megan sits where the captain should. "
                 "The crew on the sofas, two chairs for witnesses. Whatever Duc has found, now is when it counts.",
    frage="Who does Duc name before the judge?",
    will={"megan": "Hear one name and the proof for it - and not admit that something about this bothers her.",
          "*": "Get through the hearing - and see who Duc names."},
    wahl=dict(WM("Who do you name?", nach=2), optionen_aus="anklage"),
    immer=[F("anhoerung_gehalten")])

B["anhoerung_rolle"] = dict(
    zeit="11:40", ort="main_salon", bild="eden_rise_salon_anhoerung.png", anwesend=["megan"], max_zuege=4,
    ausgangslage="The witnesses have spoken. Megan turns a page. \"And you, First Officer? Where were you, and what "
                 "did you sign that night?\"",
    frage="Does Duc tell the truth about his own part?",
    will={"megan": "Know whether the man in front of her lies to her too."},
    wahl=WM("Your own part",
            A("Tell her everything - including what I did wrong.", "He tells Megan honestly what he himself did and "
              "failed to do that night.", {"schritt": "rolle", "ehrlich": True}),
            A("Keep it to myself.", "He keeps his own part to himself.", {"schritt": "rolle", "ehrlich": False}),
            nach=1))

B["anhoerung_urteil"] = dict(
    zeit="12:10", ort="main_salon", bild="eden_rise_salon_anhoerung.png", anwesend=["megan"], max_zuege=5,
    ausgangslage="Megan closes the folder. Before she speaks, she looks at Duc one last time. \"Anything else?\"",
    frage="What does Duc ask for?",
    will={"megan": "Pass a verdict she can live with."},
    wahl=WM("Your plea",
            A("Ask for mercy.", "He asks Megan for mercy.", {"schritt": "plaedoyer", "art": "gnade"}),
            A("Share the blame.", "He offers to carry part of the blame himself.", {"schritt": "plaedoyer", "art": "teilen"}),
            A("Demand the full penalty.", "He demands the full penalty.", {"schritt": "plaedoyer", "art": "strafe"}),
            nach=1))

B["nach_dem_urteil"] = dict(
    zeit="18:00", ort="crew_mess", anwesend=["megan", "chiara", "lola"], max_zuege=6,
    ausgangslage="After the verdict. The helicopter is waiting on the sun deck. The crew mess is too quiet, and "
                 "somebody who was suspected all week is waiting for a word from Duc.",
    frage="What does Duc say now that it is decided?",
    will={"megan": "Leave with the last word.", "chiara": "Put the room back in order.",
          "lola": "Cook something, because that is what you do after."},
    immer=[F("megan_abgereist")])

B["cliffhanger"] = dict(
    zeit="02:00", ort="foredeck", bild="eden_rise_berge_rotes_licht.png", anwesend=[], max_zuege=2,
    ausgangslage="Night. Everyone is asleep. High up in the hills above the bay a red light is blinking - the same "
                 "slow rhythm as the light behind the inverter. Then a howl from the macchia. It is not a dog.",
    frage="End of Act 1.",
    will={},
    immer=[F("akt1_ende")])

# ======================================================================== Freie Phasen
# Phasen ohne Hauptszene: Zeit mit einer Person an ihrem Ort (Tagesablauf), dazu die Kabine.
# Je Phase mehrere Fassungen (28.10.2026, Spieltest: drei Karten mit demselben Satz); die Engine waehlt je Figur fest.
FREI = {
    "fruehstueck": ["Breakfast time, the bay still quiet. {name} is at {ort}, same as every morning.",
                    "Coffee, toast, the bay still grey. {name} is at {ort} and has saved you a seat, more or less.",
                    "The first light comes in low over the water. {name} is already up, at {ort}."],
    "tag": ["A free hour around midday. {name} could use some company - or some help.",
            "Midday heat. {name} is at {ort}, pretending to be busy.",
            "Nobody needs you for an hour. {name} is at {ort}."],
    "nachmittag": ["The long afternoon. {name} is at {ort} and in no hurry at all.",
                   "The afternoon drags on in the bay. {name} is at {ort} and wouldn't say no to a distraction.",
                   "Sun, salt, a slow afternoon. You find {name} at {ort}."],
    "dinner": ["Dinner time. {name} is eating at {ort} and there is a free chair.",
               "Something smells good. {name} has a plate at {ort} and nods at the seat opposite.",
               "Dinner, more or less. {name} is at {ort} with a plate that hasn't been touched yet."],
    "abend": ["A quiet evening. {name} is at {ort}, not quite ready to call it a day.",
              "The light goes orange over Corsica. {name} is at {ort}, watching it.",
              "Evening in the bay, and nothing left to do today. {name} is at {ort}."],
    "nacht": ["Late. The yacht creaks at anchor. {name} is still up, at {ort}.",
              "Almost everyone is asleep. Almost. {name} is at {ort}.",
              "Night, the anchor light, water slapping against the hull. {name} can't sleep either - you find them at {ort}."],
}


# Stimmungsrahmen (Duc 29.10.2026, STIL "Sprite passt zur Lage"): In diesen Szenen waehlt der Richter das Gefuehl fuer
# den Sprite nur aus der Liste - er bleibt fuer die Feinheit zustaendig (wer ist wuetend, wer traurig), kann aber nicht
# mehr aus der Lage fallen (kein "amusement" im Alarm, keine Flirt-Pose beim Abschied). Lockere Szenen bleiben frei.
STIMMUNG = {
    "krise": ["fear", "nervousness", "anger", "annoyance", "confusion", "sadness", "surprise", "realization", "disapproval"],
    "abschied": ["sadness", "grief", "caring", "gratitude", "pride", "remorse", "admiration", "relief", "neutral"],
    "ernst": ["neutral", "nervousness", "annoyance", "disapproval", "disappointment", "sadness", "caring", "pride",
              "realization", "confusion", "fear", "anger"],
    "sturm": ["fear", "nervousness", "anger", "annoyance", "confusion", "sadness", "surprise", "realization", "caring",
              "pride", "relief"],
    "anhoerung": ["neutral", "nervousness", "fear", "anger", "annoyance", "disapproval", "disappointment", "pride", "sadness",
                  "confusion", "realization", "remorse", "relief", "grief", "surprise"],
}
STIMMUNG_SZENE = {
    "cold_open": "krise", "explosion": "krise", "wache_mit_holm": "krise", "cliffhanger": "krise",
    "lage_mit_holm": "ernst", "megan_inspektion": "ernst",
    "holm_ansprechbar": "abschied", "holm_abschied": "abschied", "der_freie_platz": "abschied",
    "sturmvorbereitung": "sturm", "sturmnacht": "sturm",
    "anhoerung": "anhoerung", "anhoerung_rolle": "anhoerung", "anhoerung_urteil": "anhoerung",
}
for _sid, _name in STIMMUNG_SZENE.items():
    B[_sid]["stimmung"] = {"name": _name, "erlaubt": list(STIMMUNG[_name])}


def main():
    daten = {"_hinweis": "Gebaut aus werkzeuge\\eden_rise\\story_buehne.py - dort aendern. Spoilerfrei: nur Buehne, nie Fall-Inhalte.",
             "szenen": B, "frei": FREI}
    json.dump(daten, open(ZIEL, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("buehne.json geschrieben: %d Szenen, %d freie Vorlagen" % (len(B), len(FREI)))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
