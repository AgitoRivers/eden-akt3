# -*- coding: utf-8 -*-
"""English rewrite · package 3: story and cases (story_faelle.py, story_eden_rise.py, story_basis.py), 25.10.2026.

CONFIDENTIAL like story.json: contains the case solutions. No approval page for Duc (spoilers); Claude checks the
canon against docs/wiki. Texts are addressed by file + line of the German literal (several literals on one line =
list in column order), so the German originals never have to be retyped. Run it before the source files change:

    python werkzeuge\\englisch\\story_paket.py     -> docs\\abnahme\\englisch_story.json (spec for uebernehmen.py)

Terms: Energiesteuerung = power management system, Protokoll = log, Ereignisstreifen = event record,
Rückfallprofil = fallback profile, Querkupplung = bus tie, Heckverteiler = stern distribution board,
Wartungsschalter = maintenance switch, Servicekarte = service card, Hotelnetz = hotel load, sm = nm, T1 = Day 1.
"""
import ast, json, os, re, sys

HIER = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(os.path.dirname(HIER))
QUELLE = os.path.join(EDEN, "werkzeuge", "eden_rise")

DE = re.compile(r"[äöüßÄÖÜ]|\b(und|der|die|das|nicht|ist|ein|eine|mit|auf|für|ich|du|sie|wir|noch|schon|auch|wird|hat|"
                r"zu|im|am|vom|zum|den|dem|des)\b")
EN = re.compile(r"\b(the|and|you|is|of|to|with|a|in|on|it)\b")

# Literals that stay German on purpose: condition keys, internal time format, QA scenario labels
BLEIBT = {"eine", "nicht", "T%d frühstück", "früh richtige Vermutung ohne Belege", "spätes vollständiges Ermitteln",
          "Romanze mit der verantwortlichen Person", "Romanze mit einer Unschuldigen",
          "öffentlich falsche Anschuldigung mit Korrektur", "öffentlich falsche Anschuldigung ohne Korrektur",
          "verweigerte Intimität", "frühes freiwilliges Geständnis", "Megan übt Druck aus",
          "Anhörung mit leeren Händen", "Anhörung mit lügendem Zeugen"}

# Short German literals the line scan does not catch
EXTRA = {"Protokoll ": "Log "}

NEU = {
    "story_basis.py": {
        35: "Day 2: secure the event record of the power management system (becomes evidence)",
        36: "Examine a place or object (costs the phase)",
        37: "Talk to a person (the answer depends on trust or a condition)",
        38: "Call or message (Holm in hospital, Petru, Elsa, Megan)",
        40: "Command order (from day 2, Duc leads) - costs trust or backing",
        41: "The character offers it of their own accord once the condition is met",
        42: "Trade - real information, but a new dependency",
        43: "Duc's own memory of the opening (only if he was there)",
        52: "What happened to the system during the night?",
        53: "Who triggered it - and did this person know what they were doing?",
        54: "Did exactly that cause the failure?",
        167: "The person's trust -2; they stay silent for the rest of the day",
    },
    "story_faelle.py": {
        13: "Secure the event record of the power management system",
        18: "Pull a copy of the controller log through the service access",
        23: "Have Rosi read out the fault messages",
        27: "Read the bridge logbook",
        31: "Ask Holm about the night",
        35: "Call Holm in hospital",
        39: "Ask Petru for the manufacturer's documents on the module type",
        56: "%%s: LM3 failed, propulsion stopped, hotel load in island mode%s",
        62: "Logbook (Holm, bridge clock): ",
        70: "Look through the voyage plans on the office PC",
        71: "Voyage plan v2 has applied since Day 1, 15:30: night passage after the party, morning stop in Cala d'Orsu "
            "(guests' wish: sunrise), submitted through Sophia, approved by Holm.",
        74: "Voyage plan v2: night passage, morning stop at Cala d'Orsu (guests' wish), submitted through Sophia",
        75: "Duc knows the valid plan",
        76: "Load limit on the stern distribution board: 2 kW maximum, only the onboard charging station, no "
            "multi-socket adapters. Receipt signed by Yasin.",
        80: "Look through the bridge folder with the guest documents",
        81: "Ask Rosi about the power rules for guests",
        83: "Holm hands Lea the route planning for the night passage as an exercise.",
        84: "Route planning: Lea (exercise, assigned by Holm)",
        89: "Group photo in the main salon. Camera time 21:32; the power management display in the background shows %s.",
        92: "Group photo 21:32 (camera time) - power management display in the background",
        93: "Look at the group photo in the crew chat",
        94: "The guest party ends at 00:30; the crew afterparty in the mess and on the aft deck goes on until about "
            "03:30, with music from Lola's speaker.",
        97: "Holm locks the bridge at 00:45 and lies down.",
        98: "Holm: bridge locked at 00:45",
        103: "Duc can't sleep and sits with Lola in the galley; she is baking for the sunrise breakfast. Blackout: first "
             "the music stops, then Lola says \"Duc?\", then the alarm.",
        106: "Galley before sunrise: first the music stops, then your name, then the alarm",
        108: "Holm brings the Eden Rise into the bay of Cala d'Orsu on the bow thruster and Unit-01 and drops anchor.",
        110: "07:50 at anchor in the bay of Cala d'Orsu",
        111: "The clock of the power management system is 14 minutes slow (ship's time = display + 14).",
        114: "Match the times: the photo against the display in the background",
        118: "Compare the power management clock with your phone",
        120: "Ship's manual p. 4-17: fallback profile R2 as a permitted emergency profile after a protective abort, "
             "activated at the maintenance switch; reset via \"End diagnosis\".",
        123: "Ship's manual 4-17: fallback profile R2 after a protective abort, reset via \"End diagnosis\"",
        125: "Ask Rosi about the fallback profile",
        129: "Ask Rosi about the failed module",
        130: "Service cards: card 1 Captain (Duc from day 2), card 2 Engineering - hangs on the hook in the engine "
             "control room, card 3 Yard/Office - drawer in the ship's office.",
        133: "Service cards: 1 Captain, 2 Engineering (hook in the control room), 3 Office (drawer)",
        134: "Ask Rosi about the service cards",
        136: "Holm, Duc, Rosi and Chiara (on her big bunch) have keys to the bridge maintenance switch.",
        138: "Maintenance switch keys: Holm, you, Rosi, Chiara",
        140: "Totò's betting book \"Arrival Calvi\": every bet with time, stake and odds.",
        143: "Petru writes Lea the Margot search area off the Punta d'Orsu, with coordinates.",
        145: "Petru's message to Lea: Margot search area off the Punta d'Orsu (coordinates)",
        147: "Ask Lea about the fisherman who texts her",
        149: "At the party Holm visibly has stomach pain and waves it off (medical, not a clue).",
        151: "Duc saw it",
        166: "Chiara studied in the mess from 01:30 to 02:45 for her Yachtmaster Offshore exam, which nobody is "
             "supposed to know about.",
        168: "Chiara: studied in the mess until quarter to three",
        169: "Ask Chiara about the night",
        170: "Lola: Chiara sat at the mess table with her binder from half past one to quarter to three.",
        172: "Lola: Chiara sat studying at the mess table until quarter to three",
        173: "Ask Lola who was in the mess and when",
        174: "Printer in the ship's office: job Day 1, 16:10, \"Collision Regulations ch. 3\", user C. Sonnberg.",
        176: "Printer memory: 16:10 \"Collision Regulations ch. 3\" (C. Sonnberg)",
        177: "Look at the printer memory in the ship's office",
        178: "Holm: at 02:40 the bridge was locked, everything as usual.",
        179: "Holm: found the bridge locked at 02:40",
        181: "Chart plotter history: at 01:10 a section off the Punta d'Orsu was opened (Margot area); Holm found it "
             "still open at 02:40.",
        183: "Plotter history 01:10: chart section off the Punta d'Orsu",
        184: "Look at the chart plotter history",
        185: "Siri: she and Lea sat on the foredeck from 02:00 to 03:30 watching the sea glow.",
        187: "Siri: with Lea on the foredeck from 02:00 to 03:30",
        188: "Ask Siri about the night",
        189: "Route plan (Lea): direct line, 34 nm, standard distance off the coast.",
        192: "Look at Lea's route plan on the office PC",
        193: "The GPS track of the night follows the planned line without deviation.",
        194: "GPS track: on the planned line, no deviation",
        195: "Look at the night's track on the plotter",
        196: "From 02:30 to 03:10 Sophia was on the phone on the sun deck, in French, with her editor Helene Marchal, "
             "about her manuscript. No meeting was planned.",
        198: "Sophia: on the phone on the sun deck at night (private)",
        200: "Siri saw Sophia on the phone on the sun deck around quarter to three when she went to fetch a blanket.",
        202: "Siri: Sophia on the phone on the sun deck at quarter to three",
        203: "Ask Siri who she saw at night",
        204: "Voyage plan v2 in detail: departure 03:00, Unit-01 charging run from 01:00 to 02:50, arrival Cala d'Orsu "
             "07:15, stop until 09:30, 8 kn. File created Day 1, 13:30 after Yasin's request.",
        208: "Look at the plan file on the office PC",
        209: "Yasin: \"I wanted the sunrise for the drone. I asked Sophia at lunchtime.\"",
        212: "Ask Yasin about the morning stop",
        213: "Alva: \"Sophia? Don't know her. Nobody from your boat booked a table with me.\"",
        214: "Alva: no reservation from the yacht",
        215: "Ask Alva about the crew",
        216: "Unit-01 hour meter: charging run during the night from 01:00 to 02:50.",
        218: "Unit-01 meter: charging run 01:00-02:50",
        219: "Read the Unit-01 meter",
        220: "Totò's betting book: Rosi, €5 on \"4 to 6 pm\" (Day 1, 23:10); odds unchanged.",
        222: "Betting book: Rosi €5 on 4-6 pm, odds unchanged",
        224: "Chiara heard Rosi snoring through the cabin wall at quarter to three.",
        227: "Ask Chiara about the night in the crew corridor",
        230: "Look at Rosi's log binder in the workshop",
        231: "Hotel load list: charging station in the mess 1.8 kW from 05:30 to 06:40 (Yasin's devices); the stern "
             "distribution board did not trip.",
        233: "Hotel load: charging station in the mess 1.8 kW 05:30-06:40, stern board did not trip",
        234: "Have Rosi show you the consumption list",
        235: "Yasin's clips: dawn from the sun deck from 05:30, without a break.",
        237: "Yasin's clips: from 05:30, continuously from the sun deck",
        239: "Totò: his cousin came alongside the swim platform in a dinghy from 01:50 to 02:20 (goods). That's why he "
             "was on deck.",
        241: "Totò: at the swim platform at night (a visit from his cousin)",
        244: "Lola: afterparty until half past three, then a smoke at the stern, baking in the galley from quarter to "
             "five.",
        246: "Lola: afterparty until 03:30, galley from 04:45",
        249: "At the party: Chiara's binder in the pantry, tab \"Collision Regulations\". She snaps it shut quickly.",
        251: "Memory: Chiara's binder, tab Collision Regulations",
        254: "At the party, in the control room: all displays green. Rosi proudly shows off Unit-01.",
        256: "Memory: control room at 20:10, everything green",
        258: "At the party: Siri takes a breather on the aft deck. Yasin's devices are charging at the charging station "
             "in the mess.",
        260: "Memory: Yasin's devices at the charging station in the mess",
        261: "You got Siri out of the shoot",
        282: "Only rises when the person learns about the investigation. Searching in secret changes nothing.",
        295: "denies it; fear +1; Duc may suspect, the game confirms nothing",
        306: "Practice on the Bridge",
        307: "After the party Chiara secretly practises a diagnostic routine for her exam, activates the "
             "documented-looking but unapproved fallback profile R2 after a protective abort, and believes she reset "
             "it with \"End diagnosis\". R2 stays active; the already damaged LM3 fails under the sustained load of the "
             "passage.",
        312: "Chiara prints exercise 4-17 (diagnosis procedure, protective abort, R2)",
        313: "Binder with tab 4-17 in the pantry",
        314: "Chiara leaves the afterparty (\"have to study\")",
        315: "Bunch of keys with a little bell at the bridge door",
        316: "Diagnostic routine started at the maintenance switch",
        317: "Protective abort LM3 overtemperature",
        318: "Fallback profile R2 activated",
        319: "\"End diagnosis\" - R2 stays active; the exercise sheet is left lying on the console",
        320: "Chiara back in the mess, tea, bunk at 02:45",
        321: "Holm: door open, display \"PROFILE R2 READY\", sheet into the logbook folder",
        322: "Departure in profile R2",
        323: "LM3 fails under sustained load",
        326: "%s: diagnostic routine started (bridge maintenance switch)",
        327: "%s: protective abort of diagnostic routine - LM3 overtemperature",
        328: "%s: fallback profile R2 activated (bridge maintenance switch)",
        329: "Holm: at 02:40 the bridge door was open although she had locked it at 00:45; the display read "
             "\"PROFILE R2 READY\". She took it for a yard setting.",
        331: "Holm: door open at 02:40, display \"PROFILE R2 READY\"",
        333: "Exercise sheet \"Procedure 4-17\" with pencil notes \"2:05 / 2:22 / 2:24\" in Chiara's handwriting. It was "
             "lying on the maintenance console; Holm put it in the logbook folder.",
        335: "Over coffee Holm mentions a note on the console",
        337: "Exercise sheet 4-17 with pencil times 2:05 / 2:22 / 2:24",
        339: "Ask Chiara to show you her exam binder",
        341: "Order the locker opened, as commander",
        343: "Holm: there was a note on the maintenance console, \"Procedure 4-17\", with pencilled times. She put it in "
             "the logbook folder.",
        346: "Holm: there was a note \"Procedure 4-17\" on the console – now in the logbook folder",
        347: "Ask Holm whether anything was lying on the console that night",
        349: "Printer memory: job Day 1, 16:10, \"Exercise_4-17.pdf\", 2 pages, user C. Sonnberg. The file is still on "
             "the office PC.",
        351: "Printer memory: 16:10 \"Exercise_4-17\" (C. Sonnberg)",
        353: "Look at the last printed files on the office PC",
        354: "Totò: after the party ended, around two, he heard Chiara's bunch of keys with the little bell at the "
             "bridge door.",
        356: "Totò: heard Chiara's keys at the bridge door around two",
        357: "Ask Totò what he heard at night",
        359: "Lola: Chiara left shortly before two (\"have to study\") and came back at half past two, made tea and went "
             "to bed.",
        361: "Lola: Chiara left shortly before two, back at half past two",
        363: "Chiara: \"I studied in the mess until half past two, then I went to bed.\"",
        365: "Chiara: studied in the mess until half past two",
        367: "Chiara (when pressed): \"I was outside for a moment. Fresh air.\"",
        368: "Chiara: was outside for a moment, fresh air",
        370: "\"End diagnosis\" does not reset R2. Under sustained load in R2 a PX-480 overheats - exactly what the curve "
             "shows up to the failure.",
        372: "Engineering: \"End diagnosis\" does not reset R2; R2 overloads LM3",
        373: "Have Rosi re-enact the procedure at the maintenance console",
        375: "At the party: Chiara's binder in the pantry, tab \"4-17 Fallback profile\".",
        377: "Memory: Chiara's binder, tab 4-17 Fallback profile",
        380: "Notice on the bridge door: \"Access for command and engineering only - safety after the incident. "
             "C. Sonnberg\"",
        382: "Notice on the bridge door: access for command/engineering only (signed C. Sonnberg)",
        383: "The bridge door",
        384: "In the logbook folder, the sleeve with the exercise sheet is empty.",
        385: "Logbook folder: one sleeve is empty",
        388: "Ask Holm about the note from the console",
        393: "Statement: studied in the mess until half past two - Lola: left shortly before two, came back at half past "
             "two",
        395: "Without matching the clocks, the start of the diagnosis (display %s) comes before Chiara left at 01:55 - "
             "with the clocks matched (02:05) it falls right in her absence. The pencil times on the sheet only fit "
             "once the clocks are matched.",
        398: "Restricts access to the bridge with a matter-of-fact safety reason.",
        400: "No evidence is lost; counter: Duc lifts the notice as commander.",
        401: "Takes her exercise sheet out of the logbook folder, not the log - the sleeve stays empty, the sheet ends up "
             "in her exam binder.",
        405: "She asks for a private talk herself.",
        406: "For once I didn't want to be the one bringing the coffee while other people decide.",
        409: "The door was open. I'd locked it at quarter to one.",
        411: "The yard changed something at the last service.",
        413: "Chiara's been carrying her fat binder everywhere since yesterday. Normally it lives in her locker.",
        415: "Over coffee Holm said she put a note in the logbook folder that night.",
        419: "She enters the incident in the report herself and works on under verifiable responsibilities. No command "
             "handed to her, no qualification handed to her.",
        423: "The Leg That Wasn't in the Plan",
        424: "During her route exercise Lea puts WP4 on the Margot search area and makes the extra distance look small "
             "by measuring it against last year's longer route (+1.8 instead of +11.2 nm). Duc signs it off. The "
             "autopilot holds the arrival time and runs at 10.6 instead of 8 kn; under the sustained load the already "
             "damaged LM3 fails.",
        429: "Petru writes Lea the Margot search area",
        430: "Lea sets WP4 on the Margot coordinates, extra distance \"+1.8 nm\"",
        432: "Lea to Siri: \"Tomorrow morning we'll go right over it.\"",
        433: "Departure; arrival time 07:15 -> autopilot runs at 10.6 kn",
        434: "Lea on the bridge, asks about WP4",
        437: "06:15 Lea on the bridge (asks about WP4). 06:35 propulsion off.",
        438: "GPS track: course via WP4 in the Margot area, up to 9.4 nm seaward of the direct line; speed 10.6 kn; "
             "failure 0.6 nm before WP4.",
        440: "GPS track: via WP4, 9.4 nm seaward of the direct line, 10.6 kn",
        442: "Have Rosi pull the plotter backup",
        443: "Route plan (Lea, Day 1, 16:30): WP4 \"distance off the coast\", extra distance \"+1.8 nm\", signed off by "
             "Duc at 17:40.",
        445: "Lea's route plan: WP4 \"distance off the coast\", extra distance +1.8 nm (signed off by you)",
        447: "The signed paper copy in the bridge folder",
        449: "Have Lea explain the plan",
        450: "The extra distance in the plan is measured against last year's route; against the direct line it's "
             "+11.2 nm.",
        452: "Recalculated: against the direct line +11.2 nm (the plan measures against last year's route)",
        453: "Recalculate plan and track",
        455: "Have Holm recalculate it over the phone",
        457: "Have Rosi recalculate the distance",
        459: "Petru: WP4 lies exactly in the search area he sent Lea.",
        460: "Petru: WP4 lies in the search area he sent Lea",
        461: "Show Petru the coordinates",
        463: "Send Petru the coordinates",
        465: "Holm: Lea came onto the bridge at quarter past six and wanted to know how far it still was to WP4. WP4 lay "
             "further out than Holm would have planned it - but Duc had signed it off.",
        467: "Holm: Lea on the bridge at 06:15, asked about WP4",
        469: "Lea: \"WP4 was just distance off the coast. It wasn't even two miles extra.\"",
        470: "Lea: WP4 only distance off the coast, not even two miles",
        472: "Lea: \"I only came onto the bridge after the alarm.\"",
        473: "Lea: only on the bridge after the alarm",
        474: "Ask Lea about the night",
        475: "Lea (when pressed): \"I only wanted to see if we were on time.\"",
        476: "Lea: only wanted to see if we were on time",
        478: "At a sustained 10.6 kn LM3 is well above its rated load; at 8 kn it would have stayed in the normal range.",
        480: "Engineering: at 10.6 kn LM3 over rated load, at 8 kn in the normal range",
        481: "Have Rosi analyse the night's load curve",
        482: "Lea: her grandfather searched for the Margot all his life; she wanted to see the spot herself once.",
        484: "Lea: her grandfather searched for the Margot",
        485: "Ask Lea about her grandfather",
        486: "At the party: Lea says to Siri, \"Tomorrow morning we'll go right over it.\" Yasin's devices are charging "
             "at the charging station in the mess.",
        488: "Memory: Lea to Siri - \"Tomorrow morning we'll go right over it\"",
        491: "Navigation corner: three notes with distance calculations by Lea from the night before day 3, all measured "
             "against last year's route.",
        493: "Navigation corner: Lea's night-time distance calculations (reference: last year's route)",
        496: "Lea's new distance sheet: \"+1.9 nm\" - in small print at the top, the reference \"last year's route\".",
        497: "Lea's distance sheet: +1.9 nm (reference in small print: last year's route)",
        499: "Lea brings you a new calculation",
        505: "Statement: only on the bridge after the alarm - logbook: 06:15, twenty minutes before the failure",
        507: "The display reports the failure at %s - that looks like \"right after Lea's visit\". With the clocks matched "
             "(06:35) there are twenty minutes in between: the visit wasn't an intervention; the question about WP4 is "
             "the lead.",
        510: "Volunteers for anchor watch and repair dives, secretly recalculates at night and hides how exhausted she "
             "is.",
        512: "No evidence is lost. Counter: Duc raises her exhaustion (flag lea_erschöpfung_angesprochen); otherwise she "
             "makes a mistake during the storm preparation.",
        514: "When asked about the distance she goes along with a second untruth: a new distance sheet, again measured "
             "against last year's route.",
        516: "Counter: GPS track and recalculation (f2_05).",
        519: "She comes to the navigation corner at night while Duc is there and tells him about the Margot.",
        520: "I thought if I really found it, it wouldn't just be his story any more.",
        522: "Duc's sign-off at 17:40 belongs in the complete report.",
        526: "The boat wasn't up to the passage. The yard.",
        527: "curt; reminds Duc that he signed it off",
        528: "Lea sat in the navigation corner half the night. Calculator, three notes.",
        530: "Lea's been talking about her grandad and a ship for days. Ask the fisherman who keeps texting her.",
        534: "She hands over the coordinates and accepts that a later search will be prepared and accompanied. Her "
             "grandfather stays a connection, not an informant.",
        539: "Sophia has arranged a meeting with her editor at Alva's bar at 07:30 on day 2 (a chance at a contract for "
             "her book, which nobody knows about). She invents the guests' wish for a sunrise, pushes through a 01:30 "
             "departure without a charging run of Unit-01 (\"guests don't want to hear diesel at night\") and overrules "
             "Holm's doubts with Megan's name. The night passage drains bank A; in reserve mode the controller switches "
             "to profile R2; LM3 fails.",
        546: "Sophia drafts the plan (night departure, stop 06:30-12:00)",
        548: "Message from the editor: Tuesday 7:30, Bar Santoni, draft contract",
        549: "Sophia suggests the sunrise to Yasin",
        550: "Yasin to Siri: \"Sophia says sunrise in Cala d'Orsu would be gold\"",
        551: "Plan v2 active: departure 01:30, without a charging run; Holm has doubts, approves",
        553: "Sophia to the editor: \"We're arriving early, 7:30 works.\"",
        554: "Bank A reserve threshold, reserve mode in profile R2",
        555: "LM3 failure 1.1 nm before the bay",
        556: "The editor leaves; a note for Sophia at Alva's",
        559: "%s: bank A reserve threshold - reserve mode, profile R2 (departure at 58 percent)",
        560: "Unit-01 hour meter: no run during the night; last run Day 1, 11:00.",
        561: "Unit-01 meter: no run during the night",
        563: "Ask Rosi about Unit-01 during the night",
        564: "Voyage plan v2 in detail: departure 01:30, arrival Cala d'Orsu 06:30, stop until 12:00, charging run "
             "removed (\"guests want a quiet night\"), submitted by Sophia.",
        569: "Holm's printed plan in the bridge folder",
        570: "Ask Megan for the plan as it reached Eden",
        572: "File version on the office PC: draft plan v2 created four days before the party at 22:10 (user S.), "
             "changed Day 1, 15:30.",
        574: "File version: draft plan v2 created four days before departure",
        575: "Look at the file versions on the office PC",
        576: "Have Megan pull the file history from the company server",
        584: "Note at Alva's for Sophia (Day 2, 08:15): \"Had to leave. Write to me. H. M.\" - Alva: a Frenchwoman, "
             "Madame Marchal, waited an hour.",
        591: "Messages on Sophia's phone: editor (three days before the party) \"Tuesday 7:30, Bar Santoni, I'll bring "
             "the draft contract\"; Sophia (Day 2, 02:50) \"We're arriving early, 7:30 works.\"",
        595: "Sophia shows you the messages",
        598: "Yasin: the sunrise was Sophia's idea",
        600: "Chat Yasin to Siri (Day 1, 13:20): \"Sophia says sunrise in Cala d'Orsu would be gold.\"",
        602: "Chat Yasin to Siri 13:20: \"Sophia says sunrise ... would be gold\"",
        603: "Siri shows you the chat",
        604: "Have Yasin show you the chat",
        605: "Holm: she didn't want to leave at night without a charging run. Sophia said the guests didn't want to hear "
             "diesel and that Megan wanted happy guests. Holm let herself be talked into it.",
        607: "Holm: wanted the charging run; Sophia pushed through the 01:30",
        609: "Sophia: \"Yasin absolutely wanted the sunrise. I changed the plan on Sunday at lunchtime when he asked.\"",
        611: "Sophia: Yasin's wish, plan changed on Sunday at lunchtime",
        612: "Ask Sophia about the morning stop",
        613: "Sophia (when pressed): \"I'd prepared the stop in case guests asked. That's my job.\"",
        615: "Sophia: stop prepared in case guests asked",
        617: "With a charging run (bank A ~90 percent) and departure at 03:00, the reserve would have lasted until after "
             "08:00; R2 would never have become active.",
        619: "Recalculated: with a charging run the reserve would have lasted until after 08:00",
        620: "Have Rosi work out the night's energy balance",
        623: "Sophia: \"I saw Rosi in the engine corridor at night, just before everything went off.\" (She did see her - "
             "but at 01:40, not before the failure.)",
        625: "Sophia: saw Rosi in the engine corridor at night",
        626: "Sophia tells you something",
        628: "Lola: Sophia came into the mess from the crew corridor at quarter to two.",
        629: "Lola: Sophia came out of the crew corridor at 01:45",
        630: "Ask Lola when Sophia was in the mess",
        631: "Office PC: plan file v2 overwritten on Day 3 at 23:40 (stop now 07:45-09:30, charging run back in); the "
             "old creation date is gone.",
        633: "Office PC: plan file overwritten after the incident (Day 3, 23:40)",
        636: "At the party Siri says Yasin has been raving about the sunrise since lunchtime - ever since he was with "
             "Sophia. Yasin's devices are charging at the charging station in the mess.",
        638: "Memory: Siri - Yasin's sunrise idea came after a talk with Sophia",
        641: "Holm: when she came onto the bridge for departure at 01:15, it was locked, everything as usual.",
        642: "Holm: found the bridge locked at 01:15",
        648: "Statement: plan changed on Sunday at lunchtime - file version and reservation: four days earlier",
        650: "The display reports the departure at %s, the crew remembers \"half past one\" - only with the clocks matched "
             "do both fit. Logbook and log show the same sequence with no intervention during the night; the cause "
             "lies in the plan, not at a switch.",
        653: "Supplies a true observation about another person in the wrong context.",
        655: "Counter: check the time (engine log 01:40, Lola 01:45). From trust 3 she corrects herself the next morning "
             "(flag sophia_korrigiert).",
        657: "Overwrites the plan file on the office PC.",
        660: "She corrects herself before Duc pins her down - without charm, as a request for a talk.",
        661: "Arranging favours for other people is my job. Doing it for myself suddenly made it a lie.",
        664: "I shouldn't have given in. Leaving at night without a charging run - that wasn't my idea.",
        666: "I shouldn't have given in.",
        667: "takes the blame on herself; only names Sophia if Duc asks about the plan",
        668: "Last week Sophia asked me if the bar in Cala d'Orsu takes table reservations for the morning. Last week!",
        670: "The night before last Sophia was still at the office PC. At midnight.",
        673: "She speaks to the affected group without any charming detour. The risk is rewarded; the responsibility "
             "stays.",
        675: "Helene Marchal, editor at a Paris publishing house (exists in every case as Sophia's contact; only here is "
             "there a meeting). Her identity comes only through conversation or a message Sophia shares, never by "
             "reading someone else's phone.",
        680: "The Harmless Delay",
        681: "After her round Rosi sets a service lock with card 2, which she assumes will only force a short, "
             "supervised function test after anchoring. That would have delayed the arrival in Calvi (the bet) and "
             "given her a morning with Duc. But the controller treats the automatic switchover A->B like a cold start "
             "and goes into R2; protective stop; Holm presses the offered restart; LM3 fails.",
        687: "Rosi bets €50 on \"after 6 pm\"; Totò cuts the odds from 6:1 to 2:1",
        689: "Service lock with card 2, expiry 08:00",
        690: "Diagnosis draft: function test after anchoring, with Duc",
        692: "Holm presses \"Restart\"",
        694: "Rosi lifts the lock (card 2), alone in the control room",
        695: "Rosi's diagnostic log with the old service device (lock history included)",
        698: "%s: service lock set (card 2), expiry 08:00 - function test before next cold start",
        700: "%s: switchover A->B under service lock - profile R2; protective stop; restart from the bridge",
        703: "Holm: at six minutes past six it read SERVICE LOCK ACTIVE, then protective stop. The display offered a "
             "restart. She pressed it. After that it was over.",
        705: "Holm: service lock display, protective stop, she pressed restart",
        706: "Totò's betting book: Day 2, 00:50 Rosi, €50 on \"after 6 pm\"; odds cut from 6:1 to 2:1.",
        708: "Betting book: 00:50 Rosi €50 on \"after 6 pm\", odds 6:1 -> 2:1",
        710: "The drawer under the mess counter",
        712: "Totò: \"Shortly before one Rosi put fifty on 'after six'. So I cut the odds. She knows something.\"",
        714: "Totò: Rosi bet €50 on late - he cut the odds",
        715: "Ask Totò about the bets",
        716: "Rosi's notebook (Day 2, 01:50): \"After anchoring: function test after lock, cold start approx. 20 min - "
             "with Duc.\"",
        718: "Rosi's notebook 01:50: function test after lock, after anchoring, with you",
        719: "Rosi's notebook on the workbench",
        722: "Lola: at quarter to eight Rosi went into the control room alone with a coffee.",
        723: "Lola: Rosi alone into the control room at 07:45",
        724: "Ask Lola about the morning",
        725: "Rosi: \"After my round at 01:40 I went straight to my bunk.\"",
        726: "Rosi: straight to her bunk after her round at 01:40",
        727: "Ask Rosi about the night",
        728: "Rosi (when pressed): \"I only checked the status at the terminal.\"",
        729: "Rosi: only checked the status at the terminal",
        731: "Original diagnostic log, day 2 (old service device): \"Lock 01:44-07:50 (card 2), switchover in R2, "
             "restart 06:10.\"",
        733: "Old service device: lock 01:44-07:50, switchover in R2, restart 06:10",
        736: "Have Petru read out the old service device",
        738: "Rosi fetches the old device herself",
        740: "Since Day 2, 22:40 there has been a new measurement in the log binder (a different device, without lock "
             "history); the old service device has been tidied away into the workshop crate.",
        742: "Log binder: measurement from Day 2, 22:40 replaces the one from the morning; old device in the crate",
        744: "Rosi's log binder and the workshop crate",
        746: "According to the manual the lock only applies to the next cold start; in reality the controller treats the "
             "automatic switchover like a cold start and goes into R2. The restart from R2 overloads LM3.",
        749: "Engineering: switchover under lock goes into R2; restart from R2 overloads LM3",
        751: "Have Rosi explain what the lock does during the switchover",
        753: "At the party, in the control room: all green. Rosi winks: \"If we're late into Calvi tomorrow, I'm rich.\"",
        755: "Memory: Rosi - \"If we're late into Calvi tomorrow, I'm rich\"",
        762: "Statement: straight to her bunk after her round - log: service lock at %s (display time)",
        764: "The display reports the lock at %s - seemingly BEFORE Rosi's round (01:40, engine log). With the clocks "
             "matched it's 01:44: during her round.",
        766: "On her own authority replaces the morning's diagnostic log with a new measurement and tidies the old "
             "service device away.",
        769: "Afterwards she works too long and takes corrections personally (behaviour, no further counteraction).",
        773: "When you work on the propulsion together, she stops repairing in the middle of a sentence.",
        775: "Holm's restart belongs in the report - she followed the display, she is not at fault.",
        777: "I broke it by pressing. The display offered a restart, and I pressed it.",
        779: "Who sets a lock at night? Ask engineering. And me - I pressed the button.",
        780: "blames herself; takes Duc more seriously if he clears her",
        781: "Rosi and Totò were arguing about odds yesterday. Totò has this book.",
        783: "In the middle of the night Rosi put an old measuring device away in the crate in the workshop.",
        787: "An open confession and help with the reconstruction. A romance may break over it; a gift or a sex scene "
             "does not heal the breach of trust.",
        791: "The Shot That Was Meant to Stay",
        792: "For the sunrise shoot Yasin charges six drone batteries, LED panels and a laptop through a multi-socket "
             "adapter on the stern distribution board, against the 2 kW limit he signed. The branch trips and opens "
             "the bus tie; Totò refuses, so Yasin closes it again himself. The bus tie closes under load, the "
             "controller goes into R2, LM3 fails. His camera is running the whole time.",
        798: "Yasin signs the load limit",
        799: "Chargers on the red multi-socket adapter in the tender garage",
        800: "Batteries, panels, laptop via adapter YB-CREW 3 on the stern distribution board (~4.6 kW); camera running",
        802: "Totò gets the tender ready for the shoot",
        805: "Yasin closes it again himself -> bus tie under load, profile R2",
        807: "Adapter scorched, ends up in the waste bin of the tender garage",
        808: "Yasin sends Siri the raw clip for her story selection",
        811: "%s: protective trip of the stern branch (overload), bus tie opened; three minutes later manually "
             "reconnected at the stern distribution board, profile R2",
        813: "Stern distribution board memory (own clock, ship's time): tripped at 06:22 at 4.6 kW; manually reconnected "
             "at 06:25.",
        815: "Stern distribution board: tripped at 06:22 at 4.6 kW, manually reconnected at 06:25",
        816: "Read out the stern distribution board memory",
        817: "Have Rosi read out the stern distribution board",
        820: "The waste bin in the tender garage",
        821: "Order Yasin's camera case opened, as commander",
        823: "Yasin's equipment carries labels \"YB-CREW 1-6\".",
        824: "Yasin's equipment: labels YB-CREW 1-6",
        825: "Look at Yasin's equipment on deck",
        826: "Ask Siri about the labels",
        827: "Yasin's raw clip: the light flickers (protective trip), Yasin reconnects at the stern distribution board "
             "(\"Come on...\"), three minutes later blackout.",
        829: "Yasin sends her the raw clip",
        830: "Raw clip: Yasin reconnects the stern distribution board, three minutes later blackout",
        835: "Totò: Yasin wanted him to push the switch back in at the stern distribution board. Totò refused (\"Ask "
             "Rosi\"). Yasin did it himself, shortly before everything went off.",
        837: "Totò: Yasin reconnected the stern distribution board himself",
        838: "Ask Totò about the morning in the tender garage",
        839: "Totò: \"He had this red five-way plug. It stank afterwards.\"",
        840: "Totò: red five-way plug, stank",
        842: "Yasin: \"I only charged at the charging station in the mess. When the light flickered, I was up on deck.\"",
        844: "Yasin: only charged at the charging station in the mess, on deck when it flickered",
        845: "Ask Yasin about the morning",
        846: "Yasin (when pressed): \"At the stern board I only unplugged my batteries.\"",
        847: "Yasin: only unplugged at the stern distribution board",
        849: "Hotel load list: no charging at the charging station in the mess between 05:30 and 06:30.",
        853: "Closing the bus tie under load forces the controller into R2; LM3 carries the peak load and fails.",
        855: "Engineering: bus tie under load -> R2 -> LM3 overloaded",
        856: "Have Rosi trace the sequence in the control room",
        858: "At the party: Yasin's devices are charging on a red multi-socket adapter at the service socket in the "
             "tender garage.",
        860: "Memory: Yasin's chargers on the red multi-socket adapter in the tender garage",
        863: "Shortened clip online: Duc laughing at the afterparty, cut, blackout - \"First Officer parties while the "
             "yacht dies\". The timestamp jumps from 03:02 to 06:28.",
        865: "Clip online: the cut jumps from 03:02 to 06:28",
        866: "Watch the clip online",
        867: "The waste bin in the tender garage is empty.",
        871: "Yasin offers the original - in exchange for the wording \"faulty charging station\" in the report.",
        873: "Yasin's offer: the original in exchange for a wording in the report",
        880: "Statement: only charged at the charging station, up on deck when it flickered - Totò: was at the stern "
             "distribution board; the charging station shows no charging",
        882: "The stern distribution board shows 06:25 (ship's time), the controller %s - only with the clocks matched "
             "is it the same minute.",
        884: "Publishes a shortened excerpt that makes Duc look irresponsible (reputation -1, Megan calls).",
        887: "Takes the adapter out of the waste bin and hides it in his camera case.",
        889: "Ties handing over the original to an advantage (flag yasin_angebot).",
        891: "Whoever agrees gets real information and a new dependency (duc_schuldet_yasin). No second exclusive "
             "original is invented after that.",
        893: "You need an explanation. I need my people to still believe me. We could both get what we need.",
        896: "No voluntary confession; with a complete chain he admits what is proven. The key sentence comes with the "
             "offer (f5_gh3).",
        899: "At twenty past six it tripped at the stern, three minutes later it was back on. I shouted into the tender "
             "garage. Nobody answered.",
        902: "Somebody was messing about at the stern. Ask Totò, he was down there.",
        904: "Yasin put something scorched in his camera case. Smelled like burnt toast.",
        906: "Siri has the whole video. She just doesn't talk about it.",
        909: "Siri's self-determination is kept apart from his guilt: she may leave him in every case; her freedom is not "
             "a reward for the right suspicion.",
        914: "The already damaged LM3 fails in normal operation; the warning came in the afternoon before the party. "
             "Several people are hiding private things whose times don't add up. Under pressure the crew looks for a "
             "scapegoat; Megan pushes the quick human explanation.",
        924: "Petition against Rosi on the mess board",
        925: "; no switchover during the night, no profile change, no service action",
        926: "06:40 propulsion off. No prior warning on the bridge.",
        928: "%s: LM3 temperature rises steadily until the failure, at normal load (8 kn)",
        929: "Holm: in the afternoon before the party LM3 showed a temperature warning. She acknowledged it - the yard was "
             "going to look at it in Calvi anyway.",
        931: "Holm: LM3 temperature warning in the afternoon, acknowledged",
        933: "Manufacturer's documents on the PX-480 (through Petru's contact): known thermal pre-damage in certain "
             "batches, failure possible even in normal operation.",
        936: "PX-480 manufacturer's documents: failure in normal operation possible with pre-damage",
        940: "Independent test (Rosi measures according to the manufacturer's documents, Petru documents it): thermal "
             "pre-damage to LM3, failure without an external trigger.",
        942: "Independent test: LM3 pre-damaged, no external trigger",
        943: "Have Rosi measure according to the manufacturer's documents",
        944: "Ask Elsa for an inspector from the port authority",
        946: "At the party, in the control room, \"LM3 TEMP\" was lit yellow. Rosi: \"The yard can look at that in "
             "Calvi.\"",
        950: "Totò: \"Rosi was in the engine room at three, I saw the light.\"",
        951: "Totò: light in the engine room at three - Rosi",
        952: "Ask Totò about the night",
        953: "Timer: the night lighting in the engine room switches on automatically at 03:00.",
        955: "Timer: night light in the engine room switches on at 03:00",
        956: "Look at the night-light timer",
        958: "Ask Rosi about the light in the engine room",
        960: "Totò (when pressed): \"I only saw a light. Not her.\"",
        961: "Totò: only saw a light, not Rosi",
        963: "Petition on the mess board: \"We believe it was Rosi - she was in the engine room at 01:40.\" Signed by "
             "Totò, Yasin, Chiara, Lola.",
        967: "The board in the mess",
        969: "Megan's draft report: \"Cause: operating error by a crew member (engine room, 01:40)\" - without the "
             "temperature warning from the afternoon.",
        976: "Statement: Rosi in the engine room at three - timer: the night light comes on at three; Chiara heard Rosi "
             "snoring at quarter to three",
        978: "The warning is in the log at %s, Holm remembers \"in the afternoon, before the party\" - with the clocks "
             "matched, exactly 17:20. Rosi's round (01:40, engine log) is five hours before the failure.",
        980: "The crew picks its own scapegoat: a petition against Rosi.",
        982: "Counter: a public correction with evidence (engine log, timer, log without intervention). If Duc says "
             "publicly \"We don't know yet\" before the late dinner on day 2, the list never appears.",
        984: "Megan pushes the quick human explanation: her draft names an operating error.",
        986: "Counter: independent test (f6_07), Holm's warning, log 17:20.",
        987: "You said I could tell you anything. You didn't say you could make anything you liked out of it.",
        990: "No confession possible. The key sentence belongs to the person Duc wrongly accuses (dynamic).",
        992: "A public false accusation needs a public correction (flag öffentliche_korrektur). Innocence creates no "
             "romance bonus.",
        997: "That thing was already moody yesterday afternoon. Temperature. I acknowledged it.",
        999: "The yard, I'm telling you. That module was sick before we ever left.",
        1000: "dry; thinks investigating the crew is a waste of time",
        1001: "Yesterday afternoon Holm was swearing about some LM or other on the bridge. Loudly.",
        1003: "The list with the signatures? Totò passed it round. I signed because everyone signed. I'm sorry.",
        1007: "A public false accusation needs a public correction. Duc can stand in front of the crew with evidence - "
              "that is the amends in this case.",
    },
    "story_eden_rise.py": {
        23: "Simplified, fictional power grid of the Eden Rise. Applies in all six cases. Clues show events in this "
            "grid, never, as if by magic, a person's morals.",
        27: "charges both banks; a clear day about a third, cloudy a little, a storm nothing",
        29: "below the reserve threshold the controller goes into reserve mode (uses profile R2)",
        32: "closed while under way, B supports A; on overload it opens (protection). If it is closed again under load, "
            "the controller switches to profile R2 - that is not in the ship's manual.",
        36: "logs every event with its time; its clock is %d minutes slow",
        39: "thermally pre-damaged by a foreign component (unknown on board, Act 3)",
        40: "Fallback profile R2",
        41: "Ship's manual p. 4-17 describes R2 as a permitted emergency profile with reset via \"End diagnosis\". "
            "According to a manufacturer notice it is not approved for the PX-480; \"End diagnosis\" does not reset it.",
        44: "manually at the bridge maintenance switch after a protective abort",
        47: "closing the bus tie again under load",
        48: "carries on with a shifted load distribution; LM3 carries the peak load - thermal overload for a pre-damaged "
            "PX-480",
        50: "E-motor and shaft",
        52: "after a propulsion failure, island mode: bank B only supplies the reduced hotel load",
        54: ["Cold rooms", "Galley"],
        57: "own clock in ship's time; stores trips and manual reconnections",
        58: "24 V emergency supply with its own battery",
        61: "independent of A and B. No decision in the game switches it off or trades it for something.",
        64: "Diagnostic run of the propulsion (repair work)",
        65: "Bow thruster for manoeuvres",
        67: "Bridge maintenance switch (key)",
        70: ["Captain (Duc from day 2)", "Engineering – hangs on the hook in the engine control room"],
        71: "Yard/Office – drawer in the ship's office",
        73: "according to the manual: function test before the next cold start. In reality the controller also treats "
            "the automatic switchover A→B like a cold start and goes into R2.",
        76: "Chart plotter with GPS track",
        77: ["Printer in the ship's office", "stores jobs with user and time"],
        78: ["Office PC", "voyage plans, route plans, file versions"],
        79: "Old service device (workshop)",
        80: "stores every log created with it",
        88: "A failed propulsion doesn't mean there's no power: hotel load in island mode, emergency supply independent.",
        90: "A small consumer never destroys a propulsion system on its own: every chain runs through the shared weak "
            "spot (pre-damaged LM3 + badly documented R2).",
        92: "The normal protection would have limited most triggers - that's why the second truth (Alon's component on "
            "LM3) is real in every case.",
        94: "Failure and bang are two moments: the failure lies between 06:11 and 06:35 depending on the case, the bang "
            "in the inverter is always at 06:35 (the foreign component drives LM3 into runaway after the failure).",
        96: "No forced diesel-versus-radio decision. Repair and towing compete for time, material, weather windows and "
            "hands.",
        99: "Reference: bridge clock, phones, camera, GPS, engine log, stern distribution board",
        102: "Replace or bridge LM3: spare module (Megan/Petru), diagnostic runs with Unit-01 (diesel), weather window, "
             "Rosi and Petru as hands.",
        104: "Salvage window through Elsa or Megan; a professional rescue is never morally inferior.",
        105: "Isolate LM3 properly: fire risk eliminated, afterwards only slow or no motoring under her own power.",
        106: ["Heat on the inverter casing", "Smell of hot plastic"],
        108: "Not in Act 1: LM3 exploded in the cold open (06:35), the inverter is destroyed.",
        117: "Behind the burnt-out inverter a small red light is blinking. There is no component at this spot in the "
             "wiring diagram.",
        119: "Red blinking light behind the inverter - not in the wiring diagram",
        120: "Shine a light behind the burnt-out inverter",
        122: "Totò avoids the corner with the red light. When Duc shows it to him, he turns grey and changes the subject.",
        124: "Totò avoids the red light",
        125: "Watch who avoids the red light in the propulsion room",
        127: "Megan, looking at the damage: \"A PX-480 doesn't just burn.\" Then she carries on writing as if she hadn't "
             "said anything.",
        129: "Megan: \"A PX-480 doesn't just burn.\"",
        130: "Ask Megan about the damage",
        131: "Megan demands a cause report and a hearing on board by the end of the week. Without someone to blame she "
             "fires the whole crew; the season bonus is her leverage.",
        134: "Megan's ultimatum: report and hearing in seven days - otherwise the whole crew is out",
        136: "Megan is quietly on the phone on deck and says \"A.V.\" twice. Asked about it: \"A buyer from Monaco. Not "
             "your problem.\"",
        138: "Megan on the phone: \"A.V.\" twice - \"a buyer from Monaco\"",
        139: "Ask Megan about the phone call",
        140: "Totò's betting book: since the party night he's been paying out unusually high winnings. And he's wearing "
             "a new gold chain.",
        142: "Totò has been paying out big winnings since the party night, new gold chain",
        148: "Totò counts money at night. A lot of money. Since the party. Don't ask me where it's from.",
        153: "Alon's agent bought Totò through his cousin Gennaro (€20,000, \"nobody gets hurt\"); one night in Antibes "
             "Totò fitted a foreign component to LM3. It thermally pre-damaged the module and drove it into runaway "
             "after the failure - hence the bang at 06:35 in every case. The trigger from the case only gave it the "
             "final push. Alon's motive: a disaster instead of an advertisement for the bay, bad press, a low price.",
        157: "For decades the Eden Group has owned the commercial harbour quarter of Cala d'Orsu (quay, warehouses, the "
             "land under Alva's bar). Megan is supposed to sell it; the buyer is A.V. Estates (she only knows the "
             "company name), and her promotion depends on the price. The Eden Bay Weekend (sunrise, Siri posts, Yasin "
             "films) is meant to drive the price up; the bang at 06:35 is Alon's countermove. The sale is not revealed "
             "before Act 2.",
        162: "A: remote and yet close (empty mountains, Monaco one night away, the Legion in Calvi -> Adrien's unit). "
             "B: the harbour is his logistics (cages, animals and equipment can't come over the mountain road; the "
             "resort is a pretext for cranes, warehouses and supply boats) -> he needs exactly the harbour quarter, "
             "cheaply. C: as a child he spent summers with his grandmother in Cala d'Orsu, before the diagnosis; as a "
             "boy he stood outside the Casanovas' house. The collars are a precursor to a nerve control meant to save "
             "his own body first and then patch humanity. The illness is no excuse.",
        169: "Act 1 judges the trigger, Act 3 judges Alon. Totò's statements about the party night stay true; he only "
             "lies about the device. No Act 1 clue becomes false through the betrayal.",
        171: "Only observations without a chain function: red light (z_01), Totò dodges (z_02), Megan's hesitation "
             "(z_03), \"A.V.\" (z_05), Totò's money (z_06). Lola's gossip \"counts money at night\" is only a "
             "signpost. Evidence in the propulsion room only from Act 2.",
        179: "Duc shows Megan everything during the inspection, including what speaks against the crew",
        180: "Duc holds something back during the inspection",
        181: "public accusation without evidence (against whoever)",
        182: "Duc threatens with the press or the clip",
        183: "In the hearing she lets Duc finish and listens to the plea to the end.",
        184: "In the hearing she loses patience faster (disc 3).",
        214: "One More Minute of Light",
        218: "Cold open without explanation: 06:35, a bang in the propulsion room, smoke, sparks, Rosi's hand on the "
             "emergency stop. One breath, then black screen: \"The day before. Antibes.\" Nobody is recognised, "
             "nothing is explained, no guilt is hinted at.",
        224: "Party in the evening light, no cast list - and the first scene of the crime: what Duc sees here counts "
             "later as an observation. First: who do you help? Then moments: Lea claims the sea might glow tonight; "
             "Rosi calls Unit-01 the only guest who brings its own power; Sophia quietly separates Lea and Rosi; Holm "
             "has stomach pain and waves it off; Maxwell does a push-up for every joke; Chiara has an unused place "
             "cleared away (an image, don't explain). Group photo at 21:32 - Duc may be missing from it.",
        230: "Who do you help first?",
        231: "Chiara is a pair of hands short at the service",
        232: "Rosi needs someone for a test in the control room",
        233: "Siri would like a short break from a shoot",
        234: "Flag auftakt_hilfe_<id>, trust +2; the person remembers it specifically. No hidden guilt, no option "
             "prevents a deed.",
        238: "Afterparty until half past three; Duc can't sleep and sits with Lola in the galley, who is baking for the "
             "sunrise breakfast. First the music stops. Then Lola says \"Duc?\". Only then the alarm. Don't name a "
             "time - exactly when it went quiet differs from case to case.",
        244: "Totò and Lea run to the propulsion room after the alarm. At 06:35 (the same in every case) the inverter "
             "goes bang. Maxwell catches the debris with his back and saves Totò and Lea - just a scratch, he turns it "
             "into a pose. Sophia's charm drops when Lea is lying under the debris. Rosi runs in, hits the emergency "
             "stop and then sits still in front of the inverter for longer than ten seconds (only Duc sees it). "
             "Unit-01 keeps running. Everyone says \"motor\", Rosi corrects them: \"It's not a motor. It's an "
             "inverter.\" Totò stares briefly at something behind the inverter and turns grey - don't explain. Holm "
             "asks whether everyone is okay, looks after Lola and then collapses herself.",
        253: "Who Do You Call?",
        254: "Holm has dragged herself to the bridge and won't be relieved. The yacht drifts until she lies at anchor "
             "off Cala d'Orsu at 07:50. Holm, pale with pain, doesn't ask for his heroic biography but: \"Who do you "
             "call when you don't know what to do next?\" The answer comes back (farewell). At the end she mentions "
             "that her logbook and the log show different times.",
        259: "Who do you call when you don't know what to do next?",
        261: "Nobody. I'll do it myself.",
        268: "Holm leads one last time and doesn't quite take Duc seriously yet. Rosi explains the concrete constraint "
             "(inverter destroyed, hotel load in island mode, emergency supply independent, Unit-01 running), Chiara "
             "the people's needs, Sophia the company's message. Duc decides on a noticeable cut in comfort - a later "
             "scene shows the reaction.",
        274: "half cooling",
        276: "Flag komfort_<id>; an image of it in the evening or on day 3",
        278: "Video conference on the bridge screen. Megan explodes like an anime boss: too loud, too fast, a coffee cup "
             "flies out of frame: \"You were supposed to be my postcard!\" (the Eden Bay Weekend has fallen through). "
             "Then, ice-cold, the ultimatum: in seven days a cause report and a hearing on board, and she will judge. "
             "Without someone to blame the whole crew is out. Holm pushes back as well as she still can.",
        284: "Holm Has a Moment",
        285: "Before the helicopter comes, Holm has a moment. Whoever asks precisely gets precise answers "
             "(fall.holm_tag1). After that only by phone.",
        288: "Farewell to the Captain",
        289: "Holm is evacuated by rescue helicopter (appendix) - a medical matter, not a clue. She hands Duc service "
             "card 1 and the command and picks up his answer from the night. Petru stands on the quay and watches the "
             "helicopter go.",
        294: "After take-off there are too many cups on the table. Chiara wants to take one away. A small character "
             "choice, not a moral test.",
        296: ["Leave it.", "Clear it away yourself"],
        298: "What Happened in the Night",
        299: "Three ways, one of them now: secure the event record of the power management system (it doesn't answer "
             "the who yet), talk to one person about the night, or organise the supplies first. A copy of the log is "
             "available later through the service access - but then it costs a phase.",
        305: "Ways from the groups streifen / befragen",
        307: "An explicitly offered action after Holm's hint from the night (way groups abgleich_*): the photo, the "
             "logbook or the clock in the control room.",
        309: "That Doesn't Fit the Timeline",
        310: "In a conversation the first sentence comes up that contradicts another statement (fall.widersprueche). The "
             "interface allows \"That doesn't fit the timeline\" without marking anyone as guilty. Whoever accuses "
             "straight away meets resistance; whoever asks follow-up questions gets a new, checkable detail.",
        315: "Something Is Different",
        316: "Only if a counteraction happened during the night: something already examined has changed (a page "
             "missing, a measurement replaced, an access note, a list on the board). Today the concrete event can be "
             "checked.",
        319: "Sunrise over Cala d'Orsu",
        320: "Make the player fall in love with the bay: the first quiet morning. Light on the water, fishing boats, "
             "bells from the village, Kevin the seagull on the railing. No problem, no investigation - a still moment, "
             "alone or with the person closest to Duc.",
        325: "The village opens up - people know Duc from the harbour fight yesterday. Alva knows the supply routes. "
             "Elsa wants a factual status report. Petru wants to know exactly what has already been checked. Casanova "
             "sits at the harbour, promises help and is already planning the yacht as a backdrop for the festa at the "
             "end of the summer - an oversized presentation that Elsa ends by asking about the permitted number of "
             "people. Two of three plans: one now, one in the evening.",
        331: "Check a lead ashore (case: ways ashore)",
        332: "Keep a personal promise",
        333: "The missed plan isn't lost, but later it needs help or another way in.",
        336: "The second of the three plans.",
        337: "Lola's First Meal in the Bay",
        339: "For the first time Lola cooks with what the village has to offer - and it's the best meal in days. Candles "
             "because of the power, a view of the bay. Someone laughs for the first time since the silence. Whoever "
             "says publicly here \"We don't know yet\" sets oeffentlich_noch_offen.",
        342: "A Safe Room",
        343: "A person Duc trusts sits with him in a safe room. Sexual escalation is welcome (Lola stoned: very horny "
             "and filthy). It ends with conversation, touch, a kiss or falling asleep together; the character decides "
             "too; a no leaves the relationship intact. Dialogue core: \"Tomorrow you'll ask me about that night "
             "again.\" - Yes / Only if you want to talk / evade. Lola's invitation (side arc) may fill this slot.",
        348: "Only if you want to talk.",
        350: "A concrete message confirms or refutes an alibi (fall.nachtende). If Duc already knows, then - if the "
             "conditions are right - the invitation to a voluntary confession comes instead. No redundant surprise.",
        355: "The whiteboard \"Rosi vs. Officer\" in the propulsion room: securing emergency power and the propulsion "
             "room, the first step of the repair in Act 1. A step succeeds or fails based on the work so far "
             "(material from the village helps). The person responsible can contribute decisively without becoming "
             "retroactively innocent.",
        359: "I'm Coming Tomorrow",
        360: "Megan calls, calmer than on the first day and therefore scarier: tomorrow she'll come aboard herself and "
             "stay until the hearing. She wants to see the ship, not read reports.",
        364: "A Visit from Head Office",
        365: "At the end of breakfast the main story sets megan_besuch. The landing itself is played by the event "
             "g1_helikopter (day phase, mandatory).",
        370: "Megan walks the ship. She studied navigation and naval architecture and can see from the damage that "
             "overload alone isn't enough - she doesn't say so. Duc decides whether he shows her everything, including "
             "what speaks against the crew (zweite_wahrheit.megan_haltung).",
        373: "Hold something back",
        375: "Before the Storm",
        376: "In the evening a storm comes. Clear division of work: lines and anchor, saving power, securing the galley, "
             "securing the tender, checking the makeshift fix. Duc can't go with every person; those he sends out do "
             "traceable tasks and report with what they actually know. Megan watches and takes notes.",
        382: "Foreshadowing: Duc hears Megan quietly on the phone on deck; she says \"A.V.\" twice and something about "
             "\"the buyer from Monaco\". She notices him, hangs up and becomes the boss again. Don't explain who A.V. "
             "is; Megan herself doesn't know what she is working for.",
        386: "What You Hear in the Dark",
        387: "Storm: the power drops hard. An unchecked makeshift fix fails (a consequence, not a punishment roll); a "
             "prepared procedure prevents it and is played as teamwork. Megan sees the crew at work for the first time.",
        391: "Bonfire on the Beach",
        393: "Mandatory breather after the storm: a fire on the little beach next to the yacht, Lola grills, Maxwell "
             "tells a story in the third person, Totò takes bets on who falls asleep first. The hearing is tomorrow - "
             "tonight nobody talks about it, until someone does.",
        396: "An Evening of Your Choosing",
        397: "A shared evening, deliberately chosen, before the hearing. A love scene is possible, not a mandatory climax "
             "and no reward for a cover-up. The decisive statement can come afterwards or in an equivalent friendship "
             "scene: a promise the person wants to keep themselves.",
        401: "The Hearing",
        403: "Megan judges in the salon. Sequence: accusation -> two witnesses -> objection with evidence -> truth -> "
             "Duc's own role -> plea -> verdict (story anhoerung, kern/anhoerung.py). The hearing always takes place, "
             "even empty-handed. Here: accusation, witnesses, objections.",
        408: "Duc's own role in the night: honest or kept quiet (counts towards mercy).",
        411: "Plea (ask for mercy / share the blame / demand punishment) and verdict. Megan hesitates over the engine "
             "report: \"A PX-480 doesn't just burn.\" Her gut feeling makes mercy possible if the code allows it.",
        414: "After the Verdict",
        415: "The crew after the verdict. Megan flies out; from now on only by phone again. Whoever was wrongly suspected "
             "is waiting for a word from Duc. The outcome of the hearing colours the room but explains nothing new.",
        419: "Red Light in the Mountains",
        420: "Night, everyone is asleep. High in the mountains above the bay a red light is blinking, in the same rhythm "
             "as the one behind the inverter. Then a howl from the macchia, not a dog. Black screen: end of Act 1. "
             "Don't explain.",
        428: "Holm is on board on the party day (day 1) and the morning after (in command) and is evacuated at the end "
             "of breakfast on day 2. What she knows in each case is in fall.holm_tag1; after that she can be reached "
             "by phone from the hospital.",
        431: "Phone and video conference",
        434: "Exactly once, by helicopter; she stays until the hearing (as judge) and flies out after the verdict. The "
             "main story sets the flag, no event sets it itself.",
        440: "Lola's and Alva's personal stories take no main scene's place and cost no phase (an interlude after the "
             "phase).",
        442: "Invitation or call by phone.",
        443: "As in BG3: \"Not right now\" postpones the scene; the invitation comes back on the next suitable evening. "
             "No loss of trust for postponing.",
        446: "Lola's gossip (on board) and Alva's gossip (ashore) only show where to look - never evidence on their own.",
        449: "on board: galley, morale, ship's gossip",
        451: "ashore: bar, supply routes, village gossip; all shore roles from the dossier",
        459: "Only guessing costs a vein (evidence that fits nothing; an accusation without proof). Any logically fitting "
             "evidence counts, no matter how Duc found it.",
        461: "Earned beforehand (trust, statements). Witnesses have their own loyalties and can lie to protect someone; "
             "an objection with evidence exposes the lie.",
        464: "Duc honest about his own role",
        467: "People who were wrongly suspected are offered an apology after the verdict.",
        468: "The hearing always takes place, even empty-handed; then Megan judges on her own (dismissal as a roguelike "
             "consequence, not game over).",
        470: "Megan hesitates over the engine report: \"A PX-480 doesn't just burn.\" (gut feeling -> mercy)",
        477: "No overall ending: Act 1 closes with the verdict, the state of the crew and the cliffhanger. Endings for "
             "the women, the bay and the epilogues only come at the end of Act 3.",
        482: "Drawn evenly from 1-6 before the opening, stored internally as a number, never in plain text in logs or "
             "output. No choosing afterwards. Player actions change what Duc finds out, not the cause.",
        484: "The triggers lie outside Duc's options (no opening option prevents a deed).",
        486: "Every important fact has content, time, source, reliability, who knows it and how it was passed on. Inner "
             "monologue is never another character's knowledge.",
        488: "The hidden fear of discovery only rises when the person learns about the investigation (ways with "
             "auffaellig=true, conversations, rumours). Searching in secret changes nothing.",
        490: "At most one per day. Each leaves a trace and has a way around it. No complete loss of evidence without an "
             "alternative way.",
        492: "Confrontation only with a proven chain (one piece of evidence per link). Public accusations are possible "
             "but never marked as the truth while unproven. A public false accusation needs a public correction.",
        495: "Short, factual entries, split into log, statement and \"Your suspicion\". The character list gives nothing "
             "away through sorting or missing options (all suspects have the same options).",
        497: "No central clue exclusively behind sex. A gift or a sex scene heals no breach of trust. A love scene is no "
             "reward for a cover-up. Erotic privacy only becomes a rumour through an established witness or a "
             "voluntary disclosure.",
        500: "The model shapes dialogue and atmosphere within the facts. It invents no deed, no exclusive piece of "
             "evidence, no secret surveillance and no choosing the culprit afterwards. Characters only know what is in "
             "wissende/uebermittlung. New claims are claims and are checked against the facts.",
        504: "Radio, emergency beacon, anchor light and bilge pumps are never part of a trade.",
        505: "Cases are only called case 1-6; fact IDs are neutral; check and build output only names numbers.",
        549: "Invitation to a voluntary confession, if fall.gestaendnis.freiwillig applies",
        559: "CONFIDENTIAL - contains the solution. Built from werkzeuge\\eden_rise\\story_*.py; change it there, then "
             "run story_eden_rise.py and story_pruefen.py. Never edit by hand.",
        564: "T<day> HH:MM (T1 = party day, the party night after midnight is T2)",
        584: "story.json written: %d cases, %d facts (per case %s), %d ways, %d scenes in the week arc, %d facts of the "
             "second truth",
    },
}


def deutsch(s):
    if len(s) < 4 or not re.search(r"[A-Za-zÄÖÜäöü]", s):
        return False
    de = len(DE.findall(s))
    return bool(de) and de >= len(EN.findall(s))


def literale(pfad):
    """{line: [German literals in column order]} - same filter as the dump, docstrings excluded."""
    baum = ast.parse(open(pfad, encoding="utf-8").read())
    doc = {id(k.body[0].value) for k in ast.walk(baum)
           if isinstance(k, (ast.Module, ast.FunctionDef, ast.ClassDef)) and k.body
           and isinstance(k.body[0], ast.Expr) and isinstance(getattr(k.body[0], "value", None), ast.Constant)}
    out = {}
    for k in ast.walk(baum):
        if isinstance(k, ast.Constant) and isinstance(k.value, str) and id(k) not in doc and deutsch(k.value):
            out.setdefault(k.lineno, []).append((k.col_offset, k.value))
    return {z: [v for _, v in sorted(l)] for z, l in out.items()}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    items, fehler, offen = [], [], []
    for datei, zeilen in NEU.items():
        lit = literale(os.path.join(QUELLE, datei))
        for z, neu in zeilen.items():
            neu = neu if isinstance(neu, list) else [neu]
            alt = lit.get(z, [])
            if len(alt) != len(neu):
                fehler.append("%s:L%d erwartet %d Literal(e), gefunden %d %s" % (datei, z, len(neu), len(alt), alt))
                continue
            for i, (a, n) in enumerate(zip(alt, neu)):
                if a.count("%") != n.count("%"):
                    fehler.append("%s:L%d Platzhalter passen nicht: %r -> %r" % (datei, z, a, n))
                items.append({"key": "%s:L%d.%d" % (datei, z, i), "alt": a, "neu": n})
        gesehen = set()
        for z, alt in sorted(lit.items()):
            for a in alt:
                if z not in zeilen and a not in BLEIBT and a not in gesehen:
                    offen.append("%s:L%d %r" % (datei, z, a[:80]))
                gesehen.add(a)
    items += [{"key": "extra.%d" % i, "alt": a, "neu": n} for i, (a, n) in enumerate(EXTRA.items())]
    for f in fehler:
        print("FEHLER", f)
    erledigt = {it["alt"] for it in items}
    offen = [o for o in offen if eval(o.split(" ", 1)[1]) not in erledigt] if offen else offen
    for o in offen:
        print("OFFEN", o)
    if fehler:
        sys.exit(1)
    ziel = os.path.join(EDEN, "docs", "abnahme", "englisch_story.json")
    json.dump({"id": "englisch_story", "titel": "Englisch · Paket 3: Story und Fälle (VERTRAULICH)",
               "gruppen": [{"titel": "Story", "items": items}]},
              open(ziel, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("geschrieben:", ziel, len(items), "Texte; offen:", len(offen))


if __name__ == "__main__":
    main()
