# -*- coding: utf-8 -*-
"""Aussagen fuer die spielbare Anhoerung (Duc 25.10.2026: "null intuitiv, was man sagen soll").

Prinzip wie Ace Attorney: Jede Runde ist eine Aussage aus 3 konkreten Saetzen; genau einer ist falsch und wird von
bestimmten Fakten widerlegt. Duc klickt den Satz an, den er anzweifelt, und legt den Zettel, der ihn widerlegt.
Dazu je Fakt ein Klartext-Satz fuer den Notizzettel (der Codex-Text steht klein darunter).

SPOILER: Diese Datei enthaelt Fall-Aufloesungen (wie story_faelle.py). Nie im Chat oder Wiki zitieren.

Aufbau je Fall:
  "einleitung": {runde: Megans Satz zu Beginn der Runde}
  "runden": {runde: {"sprecher": "megan" | "<pid>", "saetze": [{"text", "press", "falsch", "widerlegt": [fakt-ids]}]}}
      runde "person" gilt nur, wenn Duc die verantwortliche Person anklagt (sonst allgemeine, wahre Aussage im Code).
  "klartext": {fakt-id: Satz fuer den Notizzettel}
  "tratsch": [[sprecher, satz], ...]  Crew nach bewiesenem Punkt 1 (2-3 Saetze, Duc 26.10.: "die Crew soll tratschen")
  "gestaendnis": [[satz, gefuehl], ...]  die Ueberfuehrte erklaert nach der Kette, WARUM (4-6 Saetze)
  runden.<r>.nachbessern: {"auftakt": Satz, "gefuehl", "saetze": [...]}  Duc 26.10.: nach dem ersten Treffer bessert
      der Zeuge nach (Ace Attorney "revised testimony"); erst der zweite Treffer beweist den Punkt. Die widerlegenden
      Fakten der beiden Aussagen teilen sich die Beweissaetze des Glieds auf.
Spieltext englisch (docs/wiki/STIL.md). Fall 1 = Vorlage von Character Design; die Faelle 2-6 schreibt Story.

  python werkzeuge\\eden_rise\\anhoerung_aussagen.py      -> module/eden_rise/anhoerung_aussagen.json
"""
import json, os

HIER = os.path.dirname(os.path.abspath(__file__))
ZIEL = os.path.join(os.path.dirname(os.path.dirname(HIER)), "module", "eden_rise", "anhoerung_aussagen.json")


def S(text, press, falsch=False, widerlegt=(), stuetzt=(), gedanke=None):
    """stuetzt: Fakten, die eine WAHRE Zeile bestaetigen - Ask zeigt dann "fits your note" (Ausschlussverfahren).
    gedanke: Ducs Frage im Kopf nach Ask auf die FALSCHE Zeile - eine Frage, die keine Notiz beim Namen nennt."""
    d = {"text": text, "press": press, "falsch": falsch, "widerlegt": list(widerlegt), "stuetzt": list(stuetzt)}
    if gedanke:
        d["gedanke"] = gedanke
    return d


FAELLE = {
    1: {
        "runden": {
            "handlung": {"sprecher": "megan", "saetze": [
                S("Captain Holm locked the bridge at a quarter to one, the way she does every night.",
                  "It's in her log at 00:45. Holm doesn't make mistakes with keys.", stuetzt=["r_08", "f1_06"]),
                S("The drive ran on its normal settings all night. Nobody changed anything.",
                  "Nobody logged a change, and the yard assumes standard settings. Why would anyone touch them at "
                  "two in the morning?", True, ["f1_05"],
                  gedanke="Didn't one of the ship's systems record a change that night?"),
                S("A little before six the inverter module gave up, and the drive went dark.",
                  "The curve climbs for hours and then drops. Our engineers call it wear and tear.",
                  stuetzt=["f1_01", "r_10"]),
            ], "nachbessern": {"auftakt": "All right. The yard has sent a second version – after your objection.",
                               "gefuehl": "annoyance", "saetze": [
                S("Fine: at ten past two the drive was switched to backup profile R2.",
                  "The yard accepts that now. The computer logged it.", stuetzt=["f1_05"]),
                S("Nobody was on the bridge that night. The door stayed locked until Holm's morning round.",
                  "Holm locked it at a quarter to one. Locked is locked.", True, ["f1_06"],
                  gedanke="Wasn't that door found open in the middle of the night?"),
                S("At 02:08 the safety system stopped a test because the module was too hot.",
                  "That's in the log too. The system did its job.", stuetzt=["f1_04"]),
            ]}},
            "person": {"sprecher": "chiara", "plaedoyer": [
                "Six seasons on this boat. I know every cabin, every guest, every crack in the paint.",
                "Whatever you think you found – I was studying that night. That's all I did."], "saetze": [
                S("After the party I went down to the crew mess to study for my exam.",
                  "Yes, I'm retaking the Yachtmaster in Nice. Is that a crime now?", stuetzt=["r_07"]),
                S("I stayed in the mess until half past two. I never went near the bridge.",
                  "I had my books and a pot of tea. Ask anyone – I was right there the whole time.", True,
                  ["f1_10"], gedanke="Didn't somebody see her leave the mess?"),
                S("I'm the one who put the notice on the bridge door: command and engineering only.",
                  "Rules are rules. I wrote that one myself – ask anyone who walked past it.", stuetzt=["f1_15"]),
            ], "nachbessern": {"auftakt": "Fine! Fine. I wasn't in the mess the whole time. I went out for some air – "
                                          "that's all.", "gefuehl": "annoyance", "saetze": [
                S("I left the mess a little before two. My head was full of procedures.",
                  "Exam nerves. Ask anyone who's ever sat the Yachtmaster.", stuetzt=["f1_10", "f1_12"]),
                S("I only walked along the aft deck. I never set foot on the bridge.",
                  "The aft deck. Fresh air, sea, stars. That's it.", True, ["f1_07", "f1_09"],
                  gedanke="Then who was at the bridge door around two?"),
                S("I was back in the mess at half past two.",
                  "Lola saw me come back. She'll tell you.", stuetzt=["f1_10"]),
            ]}},
            "folge": {"sprecher": "megan", "saetze": [
                S("Fine – say someone switched a profile at two. Ending the diagnosis puts everything back to normal.",
                  "That's what the button says, isn't it? \"End diagnosis.\" One press and you're done.", True,
                  ["f1_01", "f1_02"], gedanke="What did the screens show when the drive died?"),
                S("After that the drive kept running for more than three hours, until just before six.",
                  "Three hours of quiet. Nobody saw anything wrong until the very end.", stuetzt=["f1_05"]),
                S("The module in there is a PX-480 – the type every Eden yacht uses.",
                  "Standard parts, standard manual. Nothing exotic about it.", stuetzt=["r_14"]),
            ], "nachbessern": {"auftakt": "So R2 stayed on. Fine. The yard says that changes nothing.",
                               "gefuehl": "annoyance", "saetze": [
                S("Profile R2 was still running when the module failed just before six.",
                  "The logs agree. Nobody switched it back.", stuetzt=["f1_01", "f1_02"]),
                S("R2 is a backup profile. A few hours in R2 can't hurt a PX-480.",
                  "It's built for emergencies. That's what backups are for.", True, ["f1_13"],
                  gedanke="What does the manufacturer actually say about running in R2?"),
                S("The heat built up slowly – the curve climbs for hours before it drops.",
                  "Our engineers saw the same curve.", stuetzt=["f1_01", "r_10"]),
            ]}},
        },
        "tratsch": [
            ["lola", "A profile switched at two in the morning? Who's even awake at two?"],
            ["toto", "Someone who knows the bridge, mate. Someone with a key."],
            ["rosi", "Or someone who knew where Holm keeps hers."],
        ],
        "gestaendnis": [
            ["I've been studying for the Yachtmaster for two years. Two years, Duc.", "sadness"],
            ["Procedure 4-17 is on the exam. I'd never done it on a real bridge. Only on paper.", "embarrassment"],
            ["The bridge was empty. The night was quiet. I thought – just once, for practice. I'd end the diagnosis "
             "and nobody would ever know.", "nervousness"],
            ["Just once I didn't want to be the one bringing the coffee while everyone else decides.", "anger"],
            ["I never thought the drive would burn. I'm sorry. I'm so sorry.", "remorse"],
        ],
        "klartext": {
            "f1_01": "Ship's computer, 05:58: the inverter module failed – and profile R2 was still switched on.",
            "f1_02": "Holm's logbook: when the drive died at 06:12, the display still read \"PROFILE R2 READY\".",
            "f1_03": "Ship's computer, 01:51: someone started a test routine on the bridge maintenance switch.",
            "f1_04": "Ship's computer, 02:08: the test was stopped by the safety system – the module was too hot.",
            "f1_05": "Ship's computer, 02:10: someone switched the drive to backup profile R2 – from the bridge.",
            "f1_06": "Holm found the bridge door open at 02:40, although she had locked it. The screen read "
                     "\"PROFILE R2 READY\".",
            "f1_07": "An exercise sheet, \"Procedure 4-17\", in Chiara's handwriting, with the times 2:05 / 2:22 / "
                     "2:24 – left on the bridge console.",
            "f1_08": "The printer remembers: on Day 1 at 16:10 Chiara printed \"Exercise 4-17\".",
            "f1_09": "Totò heard Chiara's keys – the ones with the little bell – at the bridge door around two.",
            "f1_10": "Lola: Chiara left the mess shortly before two (\"have to study\") and came back at half past two.",
            "f1_11": "Chiara says she studied in the crew mess until half past two.",
            "f1_12": "Chiara, when pressed: she was \"outside for a moment, for fresh air\".",
            "f1_13": "Manufacturer's manual: \"End diagnosis\" does NOT switch R2 off. Running long in R2 overheats "
                     "a PX-480.",
            "f1_14": "You remember: at the party, Chiara's binder lay open at the tab \"4-17 Fallback profile\".",
            "r_12": "The power system's clock runs 14 minutes slow – add 14 minutes to its times.",
            "r_07": "The guests' party ended at 00:30; the crew kept going in the mess and on the aft deck until "
                    "about half past three.",
            "r_08": "Holm locked the bridge at a quarter to one.",
            "r_10": "Before sunrise in the galley: first the music stopped, then someone called your name, then the "
                    "alarm went off.",
            "r_13": "Ship's manual, 4-17: after a safety stop the drive switches to backup profile R2; \"End "
                    "diagnosis\" is meant to reset it.",
            "r_14": "Type plate on the inverter module: PX-480, batch 22-B.",
            "f1_15": "Notice on the bridge door: access for command and engineering only – signed by Chiara.",
            "f1_16": "In the logbook folder one sleeve is empty.",
            "f1_17": "Holm: a sheet \"Procedure 4-17\" lay on the console – she put it in the logbook folder.",
        },
    },
    2: {
        "runden": {
            "handlung": {"sprecher": "megan", "saetze": [
                S("The night passage left at three, bound for the bay of Cala d'Orsu.",
                  "Departure at three, arrival a quarter past seven. That's the plan the captain approved.",
                  stuetzt=["r_02", "h_11"]),
                S("The yacht took the direct line along the coast, as planned.",
                  "It's the shortest way. Why would anyone take a yacht out to sea in the middle of the night?", True,
                  ["f2_03"], gedanke="Did anyone actually check where the ship went that night?"),
                S("Just after half past six the drive stopped and the hotel load switched to island mode, on batteries alone.",
                  "The power system logged it. Lights stayed on, the drive didn't.", stuetzt=["f2_01"]),
            ], "nachbessern": {"auftakt": "The yard has looked at the track again. They now concede a detour – a small "
                                          "one, they say.", "gefuehl": "annoyance", "saetze": [
                S("The route went out to a waypoint off the coast, WP4, and back in towards the bay.",
                  "It's in the route plan and on the plotter. Nobody hid it.", stuetzt=["f2_03", "f2_04"]),
                S("The plan says it itself: that waypoint added less than two miles.",
                  "Plus one point eight. It's written right there, in black and white.", True, ["f2_05"],
                  gedanke="Plus one point eight – compared to what, exactly?"),
                S("The First Officer signed that plan off at twenty to six the evening before.",
                  "His signature, his time stamp. I'm only reading what's there.", stuetzt=["r_05", "f2_04"]),
            ]}},
            "person": {"sprecher": "lea", "plaedoyer": [
                "I plan routes. I don't break engines – I wouldn't even know how.",
                "I was out on the foredeck half the night. Ask Siri. Please."], "saetze": [
                S("Captain Holm gave me the route planning as an exercise. I was really proud of it.",
                  "My first real passage plan. Holm said I could do it on my own.", stuetzt=["r_04"]),
                S("I didn't go up to the bridge that morning. Not until the alarm went.",
                  "Why would I? I was asleep, and then everything went dark and I ran up like everyone else.", True,
                  ["f2_02", "f2_07"], gedanke="Didn't the bridge have an early visitor that morning?"),
                S("From two until half past three I sat on the foredeck with Siri and watched the sea glow.",
                  "The water was full of light. Siri took about a hundred photos.", stuetzt=["h_06"]),
            ], "nachbessern": {"auftakt": "Okay. Okay! I went up at quarter past six. I only wanted to know if we "
                                          "were on time.", "gefuehl": "embarrassment", "saetze": [
                S("I asked the captain how far it still was to WP4. That's all I asked.",
                  "She was busy. She told me, and I went back down.", stuetzt=["f2_07", "f2_02"]),
                S("WP4 was only there for distance off the coast. There was nothing out there I wanted to see.",
                  "It's just sea out there. Empty sea. Why would I care about a bit of empty sea?", True,
                  ["r_18", "f2_06", "f2_13"], gedanke="Was WP4 really just empty sea – to her?"),
                S("The First Officer signed my plan off. He saw every waypoint.",
                  "I'm not blaming him. I'm just saying – he saw it.", stuetzt=["r_05", "f2_04"]),
            ]}},
            "folge": {"sprecher": "megan", "saetze": [
                S("The voyage plan set eight knots and an arrival at a quarter past seven.",
                  "Eight knots, comfortable for the guests. It's in the plan.", stuetzt=["h_11"]),
                S("The autopilot held those eight knots the whole way.",
                  "Eight knots is in the plan. Why would the autopilot do anything else?", True, ["f2_01", "f2_03"],
                  gedanke="What speed did the ship's own records show that night?"),
                S("The module gave out a little short of the waypoint, and Holm took her into the bay on the thruster.",
                  "At anchor by ten to eight. Holm did well, I'll give her that.", stuetzt=["r_11"]),
            ], "nachbessern": {"auftakt": "Ten point six knots, then. Fine. The yard says that changes nothing.",
                               "gefuehl": "annoyance", "saetze": [
                S("The detour cost time, so the autopilot went faster to keep the arrival time.",
                  "That's what an autopilot does. It keeps its promise.", stuetzt=["h_11", "f2_03"]),
                S("A few hours at ten point six knots is nothing a module like that can't take.",
                  "These boats are built to run hard. That's what the yard says.", True, ["f2_11"],
                  gedanke="What does engineering say that module can take for hours on end?"),
                S("The failure came after three and a half hours at that speed, not before.",
                  "The heat built up slowly. Nobody on the bridge saw it coming.", stuetzt=["f2_01", "f2_03"]),
            ]}},
        },
        "tratsch": [
            ["siri", "Nine miles out to sea? At night? Who plans a route like that?"],
            ["toto", "Someone who wanted to see something out there, cara."],
            ["lola", "Or someone who wanted to be there at sunrise. Bit romantic, eh?"],
        ],
        "gestaendnis": [
            ["My grandad looked for the Margot his whole life. Every summer, the same bit of sea.", "sadness"],
            ["Petru sent me the search area. I just… put the waypoint on it. One line on a chart.", "embarrassment"],
            ["Then I measured the detour against last year's route, so it would look small. That part I knew. I knew it "
             "was wrong.", "remorse"],
            ["I thought if I actually found it, it wouldn't just be his story anymore.", "grief"],
            ["I never once thought about the speed. Not once. I'm so sorry, Duc. You signed it because you trusted me.",
             "remorse"],
        ],
        "klartext": {
            "f2_01": "Power system log, 06:21 on its own clock: LM3, the inverter module, failed, the drive stopped – set speed 10.6 knots.",
            "f2_02": "Holm's logbook, bridge clock: 06:15 Lea on the bridge, asking about WP4. 06:35 drive off.",
            "f2_03": "GPS track: out via WP4, up to 9.4 miles seaward of the direct line, at 10.6 knots. The drive "
                     "failed 0.6 miles before WP4.",
            "f2_04": "Lea's route plan: WP4 marked \"distance off the coast\", extra distance \"+1.8 nm\" – signed off "
                     "by you.",
            "f2_05": "Your own recalculation: against the direct line the detour is +11.2 miles. The +1.8 compares it "
                     "with last year's longer route.",
            "f2_06": "Petru: WP4 lies right inside the search area he sent Lea.",
            "f2_07": "Holm: Lea came up at quarter past six and asked how far it still was to WP4. Holm would have "
                     "planned it closer in.",
            "f2_08": "Lea says WP4 was only for distance off the coast – \"not even two miles extra\".",
            "f2_09": "Lea says she only came onto the bridge after the alarm.",
            "f2_10": "Lea, when pressed: she only wanted to see if they were on time.",
            "f2_11": "Engineering: at a steady 10.6 knots the inverter module LM3 runs well over its rated load. At 8 knots it would have "
                     "stayed normal.",
            "f2_12": "Lea: her grandfather searched for the wreck of the Margot all his life.",
            "f2_13": "You remember the party: Lea told Siri, \"Tomorrow morning we'll go right over it.\"",
            "f2_14": "In the navigation corner: three of Lea's night-time distance sums, all measured against last "
                     "year's route.",
            "f2_15": "Lea's new distance sheet says +1.9 miles – the small print measures against last year's route.",
            "r_02": "Voyage plan v2: night passage after the party, morning stop in Cala d'Orsu for the sunrise.",
            "r_04": "Holm gave Lea the route planning for the night passage as an exercise.",
            "r_05": "You signed off Lea's route plan at 17:40.",
            "r_11": "07:50: Holm brought the yacht into the bay of Cala d'Orsu on the thruster and anchored.",
            "r_12": "The power system's clock runs 14 minutes slow – add 14 minutes to its times.",
            "r_18": "Petru's message to Lea, a week before: the Margot search area off the Punta d'Orsu, with "
                    "coordinates.",
            "h_06": "Siri: she and Lea sat on the foredeck from two until half past three, watching the sea glow.",
            "h_11": "Voyage plan v2 in detail: departure 03:00, arrival Cala d'Orsu 07:15, at 8 knots.",
        },
    },
    3: {
        "runden": {
            "handlung": {"sprecher": "megan", "saetze": [
                S("The batteries left port at fifty-eight percent, and the yacht ran at six point eight knots.",
                  "Slow and quiet, for the guests. The power system logged both.", stuetzt=["f3_03"]),
                S("Before departure, Unit-01 did its usual charging run and topped the batteries up.",
                  "Every night passage starts with a charging run. That's routine on every Eden yacht.", True,
                  ["f3_04"], gedanke="Did the generator actually run that night?"),
                S("Shortly after six, bank A hit its reserve threshold and the system switched to reserve mode.",
                  "Reserve mode is a safety feature. It did what it was built to do.", stuetzt=["f3_03", "f3_02"]),
            ], "nachbessern": {"auftakt": "The yard concedes the generator never ran. They say it didn't need to – "
                                          "the plan left plenty of margin.", "gefuehl": "annoyance", "saetze": [
                S("Unit-01 hadn't run since eleven in the morning the day before.",
                  "The hour meter says so. The yard accepts it.", stuetzt=["f3_04"]),
                S("The voyage plan had the yacht leave at three, so the batteries only needed to last a few hours.",
                  "A short passage, a full night's charge in reserve. Plenty of margin.", True, ["f3_05"],
                  gedanke="When did the plan really have the yacht leave – and what did it leave out?"),
                S("The captain logged the switch to reserve mode at five past six.",
                  "Holm writes everything down. Thank God for Holm.", stuetzt=["f3_02"]),
            ]}},
            "person": {"sprecher": "sophia", "plaedoyer": [
                "I've spent four seasons making this crew look better than it is. Plans, guests, favours – that's my "
                "job.", "Doing my job well isn't a crime, Duc. Not even on this boat."], "saetze": [
                S("I submitted the new voyage plan, and Captain Holm approved it.",
                  "Through the proper channels, darling. Signed and approved.", stuetzt=["f3_05", "f3_12"]),
                S("Yasin wanted the sunrise. I changed the plan on Sunday at lunchtime, when he asked.",
                  "A guest asks, I deliver. Same day, usually within the hour.", True, ["f3_06", "f3_07"],
                  gedanke="When was that plan really first put together?"),
                S("At quarter to two I came into the mess from the crew corridor.",
                  "I'd been checking the guest cabins. Somebody has to.", stuetzt=["f3_17"]),
            ], "nachbessern": {"auftakt": "Very well. I'd drafted it a few days earlier – in case the guests asked. "
                                          "Preparing is my job.", "gefuehl": "nervousness", "saetze": [
                S("Holm had doubts about leaving at night. I told her the guests wanted a quiet night.",
                  "Nobody wants to hear a diesel under their bed at two in the morning.", stuetzt=["f3_12"]),
                S("The sunrise was the guests' wish, not mine. I only passed it on.",
                  "I don't have wishes on charter, darling. I have guests.", True, ["f3_10", "f3_11", "f3_19"],
                  gedanke="Whose idea did the sunrise really start as?"),
                S("I took the charging run out of the plan.",
                  "Yes. For the guests. I'd do it again – well. I'd have done it again.", stuetzt=["f3_05"]),
            ]}},
            "folge": {"sprecher": "megan", "saetze": [
                S("The yacht left at half past one, without a charging run.",
                  "That's established now. Go on.", stuetzt=["f3_05", "f3_04"]),
                S("The drive never ran in reserve mode. Profile R2 had nothing to do with it.",
                  "Reserve mode and R2 are just labels on a screen. The yard calls it wear and tear.", True,
                  ["f3_01", "f3_02"], gedanke="What mode was the drive running in when it died?"),
                S("A quarter of an hour after reserve mode began, the module failed – a mile short of the bay.",
                  "Fifteen minutes. That's how long it lasted.", stuetzt=["f3_03"]),
            ], "nachbessern": {"auftakt": "Reserve mode, then. The yard says it would have come to that with any plan.",
                               "gefuehl": "annoyance", "saetze": [
                S("In reserve mode the controller switches the drive to profile R2.",
                  "Automatically. Nobody touched a switch that night.", stuetzt=["f3_03", "f3_01"]),
                S("Even with a charging run, the batteries would have hit reserve before the bay.",
                  "Batteries are batteries. Long passage, low batteries.", True, ["f3_15"],
                  gedanke="What would the batteries have looked like with a charging run and a later start?"),
                S("Holm brought her into the bay on the thruster and anchored at ten to eight.",
                  "Late, slow, but at anchor.", stuetzt=["r_11"]),
            ]}},
        },
        "tratsch": [
            ["lola", "No generator all night? Then what was keeping the lights on?"],
            ["rosi", "The batteries. Until they weren't."],
            ["toto", "Who sends a boat out at half past one on half a battery? Madonna."],
        ],
        "gestaendnis": [
            ["I've written a book. Nobody here knows. Four years of nights, after the guests had gone to bed.",
             "embarrassment"],
            ["An editor wanted to meet me. Half past seven, at Alva's bar. One chance, Duc. One.", "nervousness"],
            ["So I gave Yasin a sunrise to want, and I took the generator out, because nobody questions a quiet night.",
             "remorse"],
            ["Holm had doubts. I used Megan's name to make them go away.", "embarrassment"],
            ["Arranging favours for other people is my job. Doing it for myself, it suddenly became a lie.",
             "sadness"],
            ["She waited an hour for me, you know. Then she left a note.", "grief"],
        ],
        "klartext": {
            "f3_01": "Power system log, 06:06 on its own clock: LM3, the inverter module, failed, the drive stopped – running in reserve "
                     "mode, profile R2.",
            "f3_02": "Holm's logbook, bridge clock: 06:05 bank A at reserve, reserve mode. 06:20 drive off.",
            "f3_03": "Power system log, 05:51 on its own clock: bank A hit its reserve threshold – reserve mode, "
                     "profile R2. It had left with 58 percent.",
            "f3_04": "Unit-01 hour meter: no run during the night. The last run was on Day 1 at 11:00.",
            "f3_05": "Voyage plan v2: departure 01:30, arrival 06:30, stop until noon – charging run removed (\"guests "
                     "want a quiet night\"). Submitted by Sophia.",
            "f3_06": "Office PC file history: the draft of plan v2 was created four days before the party, at 22:10, "
                     "by user S.",
            "f3_07": "Alva's reservation book: \"Day 2, 07:30, two people, Sophia\" – booked by phone four days "
                     "earlier.",
            "f3_08": "A note left at Alva's for Sophia on Day 2: \"Had to leave. Write to me. H. M.\" A Frenchwoman "
                     "waited an hour.",
            "f3_09": "Sophia's phone: the editor's \"Tuesday 7:30, Bar Santoni, I'll bring the draft contract\" – and "
                     "Sophia at 02:50: \"We're arriving early, 7:30 works.\"",
            "f3_10": "Yasin: \"The sunrise was Sophia's idea. I just liked it.\"",
            "f3_11": "Yasin's chat to Siri, Day 1, 13:20: \"Sophia says sunrise in Cala d'Orsu would be gold.\"",
            "f3_12": "Holm wanted a charging run before leaving. Sophia said the guests didn't want to hear a diesel, "
                     "and that Megan wanted happy guests. Holm gave in.",
            "f3_13": "Sophia says Yasin wanted the sunrise and she changed the plan on Sunday at lunchtime.",
            "f3_14": "Sophia, when pressed: she had the stop ready \"in case guests asked\".",
            "f3_15": "Recalculated: with a charging run and a three o'clock start, the reserve would have lasted past "
                     "08:00 – R2 would never have come on.",
            "f3_16": "Sophia says she saw Rosi in the engine corridor \"just before everything went off\".",
            "f3_17": "Lola: Sophia came into the mess from the crew corridor at quarter to two.",
            "f3_18": "Office PC: the plan file was overwritten on Day 3 at 23:40. The old creation date is gone.",
            "f3_19": "You remember the party: Siri said Yasin had been raving about the sunrise ever since lunch with "
                     "Sophia.",
            "f3_20": "Holm: the bridge was locked when she came up for departure at 01:15.",
            "r_11": "07:50: Holm brought the yacht into the bay of Cala d'Orsu on the thruster and anchored.",
            "r_12": "The power system's clock runs 14 minutes slow – add 14 minutes to its times.",
        },
    },
    4: {
        "runden": {
            "handlung": {"sprecher": "megan", "saetze": [
                S("The yacht left at three after a full charging run, at eight knots.",
                  "Textbook. Charging run first, then a calm passage.", stuetzt=["h_11", "h_14"]),
                S("Nobody touched the power system during the night. No locks, no settings, nothing.",
                  "The yard found no trace of anyone. A quiet night in the engine room.", True, ["f4_03"],
                  gedanke="Did the power system really go untouched all night?"),
                S("Rosi did her round at twenty to two and found nothing wrong.",
                  "\"Round, no findings.\" It's in the engine log in her own hand.", stuetzt=["r_09"]),
            ], "nachbessern": {"auftakt": "The yard now concedes a service lock was set. Routine, they say – it only "
                                          "applies to a cold start, and there wasn't one.", "gefuehl": "annoyance",
                               "saetze": [
                S("The lock was set with card 2, the engineering card.",
                  "Card 2 hangs in the control room. It's in the log.", stuetzt=["f4_03", "r_15"]),
                S("When the drive switched from bank A to bank B, it simply carried on as normal.",
                  "A switchover is not a cold start. The lock never came into play.", True,
                  ["f4_02", "f4_06", "f4_13"], gedanke="What did the bridge display show when the banks switched?"),
                S("That switchover came just after six in the morning.",
                  "Bank A was due. Bank B took over. Routine.", stuetzt=["f4_04"]),
            ]}},
            "person": {"sprecher": "rosi", "plaedoyer": [
                "Nobody on this boat knows that drive like I do. Nobody.",
                "So it broke on my watch, and now it's the engineer. Of course it is. That's easy."], "saetze": [
                S("I did my round at twenty to two. Nothing wrong. It's in the engine log.",
                  "I write down every round. Every single one.", stuetzt=["r_09"]),
                S("After my round I went straight to my bunk.",
                  "I was dead on my feet. Party, round, bed. That's my night.", True, ["f4_03", "f4_09"],
                  gedanke="What did the power system record while she was down there – by the right clock?"),
                S("Card 2 hangs on its hook in the control room. Anyone in engineering can reach it.",
                  "It's not locked away. It's a card on a hook.", stuetzt=["r_15"]),
            ], "nachbessern": {"auftakt": "Fine. I checked the status at the terminal on my way out. Two minutes. "
                                          "That's not a crime.", "gefuehl": "annoyance", "saetze": [
                S("I bet on the arrival like half the crew did. Totò takes everyone's money.",
                  "Fifty euros. Lola bet more on the cake.", stuetzt=["f4_07", "f4_08"]),
                S("I never touched that lock. In the morning everything was as it should be.",
                  "I came in, I made coffee, I looked at the screens. That's all.", True,
                  ["f4_05", "f4_10", "f4_13"], gedanke="Who was in the control room when the lock came off?"),
                S("Holm pressed the restart. I wasn't even on the bridge.",
                  "Ask her. She'll tell you herself.", stuetzt=["f4_06"]),
            ]}},
            "folge": {"sprecher": "megan", "saetze": [
                S("Just after six the switchover from bank A to bank B triggered a protective stop.",
                  "The system stopped itself. That's what it's for.", stuetzt=["f4_04"]),
                S("The restart brought everything back to normal. The module failed on its own, some time later.",
                  "A restart is a restart. Whatever happened after that is wear and tear.", True, ["f4_01", "f4_02"],
                  gedanke="How long after the restart did the drive actually die?"),
                S("Holm pressed the restart the display offered her. She followed the screen.",
                  "She did exactly what the screen told her to do.", stuetzt=["f4_06"]),
            ], "nachbessern": {"auftakt": "Straight after the restart, then. The yard says a restart can't hurt a "
                                          "healthy module.", "gefuehl": "annoyance", "saetze": [
                S("Under the lock, the switchover sent the drive into profile R2.",
                  "The old service device logged it.", stuetzt=["f4_04", "f4_13"]),
                S("A restart from profile R2 is perfectly safe. The manual allows it.",
                  "If the manual allows it, the yard is not responsible.", True, ["f4_15"],
                  gedanke="What does engineering say actually happens when you restart from R2?"),
                S("Holm brought her into the bay on the thruster and anchored at ten to eight.",
                  "Late, but in one piece.", stuetzt=["r_11"]),
            ]}},
        },
        "tratsch": [
            ["lola", "A service lock? In the middle of the night? Who even has the card for that?"],
            ["toto", "Engineering. Card two. On the hook, Lola."],
            ["siri", "Wait, so the boat basically locked itself? That's terrifying."],
        ],
        "gestaendnis": [
            ["I set the lock on my round. A function test after anchoring – twenty minutes, nothing more.",
             "nervousness"],
            ["Calvi a few hours late. Fifty euros in Totò's book.", "embarrassment"],
            ["And a morning in the control room with you, Duc. Just the two of us and a cold start.", "embarrassment"],
            ["I didn't know the switchover counts as a cold start. I should have. Knowing that is my whole job.",
             "remorse"],
            ["Holm only pressed what the screen offered her. That one's on me, not on her.", "sadness"],
            ["I wanted one morning. Not this week.", "grief"],
        ],
        "klartext": {
            "f4_01": "Power system log, 05:57 on its own clock: LM3, the inverter module, failed, the drive stopped – right after a restart.",
            "f4_02": "Holm's logbook, bridge clock: 06:05 display SERVICE LOCK, protective stop. 06:10 restart. 06:11 "
                     "drive off.",
            "f4_03": "Power system log, 01:30 on its own clock: service lock set with card 2, valid until 08:00 – "
                     "function test before the next cold start.",
            "f4_04": "Power system log, 05:51 on its own clock: switchover A to B under the service lock – profile R2, "
                     "protective stop, restart from the bridge.",
            "f4_05": "Power system log, 07:36 on its own clock: service lock lifted with card 2.",
            "f4_06": "Holm: at six past six the screen read SERVICE LOCK ACTIVE, then protective stop. It offered a "
                     "restart. She pressed it, and that was the end.",
            "f4_07": "Totò's betting book, Day 2, 00:50: Rosi, €50 on \"after 6 pm\". Odds cut from 6:1 to 2:1.",
            "f4_08": "Totò: \"Just before one Rosi put fifty on 'after six'. So I cut the odds. She knows something.\"",
            "f4_09": "Rosi's notebook, Day 2, 01:50: \"After anchoring: function test after lock, cold start approx. "
                     "20 min – with Duc.\"",
            "f4_10": "Lola: at quarter to eight Rosi went into the control room alone, with a coffee.",
            "f4_11": "Rosi says she went straight to her bunk after her round at 01:40.",
            "f4_12": "Rosi, when pressed: she only checked the status at the terminal.",
            "f4_13": "Rosi's original diagnostic log on the old service device: \"Lock 01:44–07:50 (card 2), "
                     "switchover in R2, restart 06:10.\"",
            "f4_14": "The log binder holds a new measurement from Day 2, 22:40 – the old service device is tucked away "
                     "in the spare-parts crate.",
            "f4_15": "Engineering: under the lock the controller treats the switchover like a cold start and goes into "
                     "R2. A restart from R2 overloads the inverter module LM3.",
            "f4_16": "You remember the party: Rosi winked – \"If we're late into Calvi tomorrow, I'm rich.\"",
            "r_09": "Engine log: \"01:40 round, no findings\" (Rosi).",
            "r_11": "07:50: Holm brought the yacht into the bay of Cala d'Orsu on the thruster and anchored.",
            "r_12": "The power system's clock runs 14 minutes slow – add 14 minutes to its times.",
            "r_15": "Service cards: card 1 Captain, card 2 Engineering (on the hook in the control room), card 3 "
                    "Yard/Office.",
            "h_11": "Voyage plan v2 in detail: departure 03:00 after a charging run from 01:00 to 02:50, at 8 knots.",
            "h_14": "Unit-01 hour meter: a charging run during the night, from 01:00 to 02:50.",
        },
    },
    5: {
        "runden": {
            "handlung": {"sprecher": "megan", "saetze": [
                S("The yacht left at three after a full charging run, at eight knots.",
                  "A normal night passage. Batteries full, nothing unusual.", stuetzt=["h_11", "h_14"]),
                S("The power system ran without a single interruption until the drive failed.",
                  "The yard found a clean night. No trips, no switching, nothing.", True, ["f5_03"],
                  gedanke="Did the power system really never hiccup before the end?"),
                S("Just before half past six the drive stopped, and the hotel load went to island mode, on batteries alone.",
                  "Lights on, drive dead. The usual picture.", stuetzt=["f5_01", "f5_02"]),
            ], "nachbessern": {"auftakt": "The yard concedes a protective trip at the stern. Harmless, they say – the "
                                          "board reset itself.", "gefuehl": "annoyance", "saetze": [
                S("Just after twenty past six the stern branch tripped on an overload, and the bus tie, the link between the power boards, opened.",
                  "A safety trip. That's what it's there for.", stuetzt=["f5_03", "f5_02"]),
                S("A few minutes later the stern board switched itself back on, automatically, as designed.",
                  "Modern boards reset themselves. Nobody has to touch anything.", True, ["f5_04"],
                  gedanke="Did that board really close again all by itself?"),
                S("Three minutes after the bus tie closed again, the drive was dead.",
                  "Bad luck, the yard says. A coincidence.", stuetzt=["f5_03", "f5_02"]),
            ]}},
            "person": {"sprecher": "yasin", "plaedoyer": [
                "I'm a guest, bro. I film things. I don't fix boats.",
                "Four hundred thousand people watch my stuff. You think I'd wreck my own sunrise?"], "saetze": [
                S("All my gear is labelled. YB-CREW, one to six. I'm a professional.",
                  "Everything's numbered so nothing gets lost. Ask Siri.", stuetzt=["f5_06"]),
                S("I only charged my gear at the charging station in the mess.",
                  "That's what it's for, right? I plugged in where they told me to.", True,
                  ["f5_12", "f5_05", "f5_14"], gedanke="Where was his gear really plugged in that morning?"),
                S("The light flickered just after twenty past six. Everybody saw it.",
                  "Flicker, flicker, then a few minutes later – boom. Dark.", stuetzt=["f5_02"]),
            ], "nachbessern": {"auftakt": "Okay, bro, okay. I was at the stern board. I went to unplug my batteries "
                                          "when the light went funny.", "gefuehl": "nervousness", "saetze": [
                S("I signed the load limit for the stern board. Two kilowatts. I know the rules.",
                  "I read it. I signed it. Holm was standing right there.", stuetzt=["r_03"]),
                S("At the stern board I only unplugged my batteries. I never touched a switch.",
                  "Unplug, walk away. That's it. I don't touch switches on somebody else's boat.", True,
                  ["f5_07", "f5_08"], gedanke="Did anyone see – or film – what he did at that board?"),
                S("Three minutes after the flicker everything went dark.",
                  "And then everybody was running around. Me too.", stuetzt=["f5_03", "f5_02"]),
            ]}},
            "folge": {"sprecher": "megan", "saetze": [
                S("When the stern branch tripped, it was drawing four point six kilowatts.",
                  "The board remembers. More than twice the limit.", stuetzt=["f5_04"]),
                S("The drive failed long after the stern board was back. The two have nothing to do with each other.",
                  "Different times, different systems. The yard keeps them apart.", True, ["f5_01", "f5_02"],
                  gedanke="How far apart were the reconnect and the failure – on the same clock?"),
                S("Right after the bus tie closed, the controller put the drive into profile R2.",
                  "That's in the power system log.", stuetzt=["f5_03"]),
            ], "nachbessern": {"auftakt": "Three minutes apart, then. The yard says closing a bus tie is a normal "
                                          "switching operation.", "gefuehl": "annoyance", "saetze": [
                S("The bus tie was closed again by hand, at the stern board.",
                  "That much the yard accepts now.", stuetzt=["f5_03"]),
                S("Closing a bus tie under load is routine. The drive doesn't even notice.",
                  "Engineers do it every day. It's a switch.", True, ["f5_13"],
                  gedanke="What does engineering say happens when you close the bus tie under load?"),
                S("Holm brought her into the bay on the thruster and anchored at ten to eight.",
                  "On the thruster again. She's getting good at it.", stuetzt=["r_11"]),
            ]}},
        },
        "tratsch": [
            ["lola", "The stern board? Who plugs anything into the stern board at six in the morning?"],
            ["toto", "Someone with a lot of batteries, Lola. A lot."],
            ["sophia", "Two kilowatts. It's written on the board, darlings. In red."],
        ],
        "gestaendnis": [
            ["Fine. Six batteries, the panels, the laptop. On one plug. The light was perfect, bro.", "annoyance"],
            ["It tripped. Totò wouldn't touch it. So I pushed it back in myself. It's a switch. Everybody knows how a "
             "switch works.", "nervousness"],
            ["Then everything went dark – and my camera was still running.", "fear"],
            ["So I cut the clip. Made it look like you were partying. People believe what they see.", "embarrassment"],
            ["You need an explanation. I need my people to still believe me. We could both get what we need.",
             "neutral"],
        ],
        "klartext": {
            "f5_01": "Power system log, 06:14 on its own clock: LM3, the inverter module, failed, the drive stopped – in profile R2.",
            "f5_02": "Holm's logbook, bridge clock: 06:22 protective trip at the stern. 06:25 back in (?). 06:28 drive "
                     "off.",
            "f5_03": "Power system log, 06:08 on its own clock: the stern branch tripped on overload and the bus tie, the link between the power boards, "
                     "opened. Three minutes later it was closed again by hand at the stern board – profile R2.",
            "f5_04": "The stern board's own memory (ship's time): tripped at 06:22 at 4.6 kW, closed again by hand at "
                     "06:25.",
            "f5_05": "A scorched red multi-socket adapter, labelled \"YB-CREW 3\".",
            "f5_06": "Yasin's equipment carries labels \"YB-CREW 1–6\".",
            "f5_07": "Yasin's raw clip: the light flickers, Yasin pushes the switch back in at the stern board (\"Come "
                     "on…\"), three minutes later blackout.",
            "f5_08": "Totò: Yasin wanted him to push the switch back in at the stern board. Totò said \"Ask Rosi\". "
                     "Yasin did it himself.",
            "f5_09": "Totò: \"He had this red five-way plug. It stank afterwards.\"",
            "f5_10": "Yasin says he only charged at the charging station in the mess, and was on deck when the light "
                     "flickered.",
            "f5_11": "Yasin, when pressed: at the stern board he \"only unplugged his batteries\".",
            "f5_12": "Hotel load list: nothing was charging at the mess charging station between 05:30 and 06:30.",
            "f5_13": "Engineering: closing the bus tie under load forces the controller into R2 – the inverter module LM3 takes the peak "
                     "and fails.",
            "f5_14": "You remember the party: Yasin's chargers on a red multi-socket adapter in the tender garage.",
            "f5_15": "Clip online: you laughing at the afterparty, cut, blackout – the timestamp jumps from 03:02 to "
                     "06:28.",
            "f5_16": "The waste bin in the tender garage is empty.",
            "f5_17": "Yasin offers the original clip – if the report says \"faulty charging station\".",
            "r_03": "Load limit for the stern board: 2 kW, charging station only, no multi-socket adapters – signed by "
                    "Yasin.",
            "r_11": "07:50: Holm brought the yacht into the bay of Cala d'Orsu on the thruster and anchored.",
            "r_12": "The power system's clock runs 14 minutes slow – add 14 minutes to its times.",
            "h_11": "Voyage plan v2 in detail: departure 03:00 after a charging run from 01:00 to 02:50, at 8 knots.",
            "h_14": "Unit-01 hour meter: a charging run during the night, from 01:00 to 02:50.",
        },
    },
}


# Falsche Zeilen (Duc/Luise 28.10.2026): eine Notiz zaehlt, wenn sie zum Beweissatz des Punkts gehoert UND die
# Behauptung der Zeile beruehrt. "widerlegt" = die Notizen, fuer die die Zeile geschrieben ist; "beruehrt" = weitere
# Notizen des Punkts, die dieselbe Behauptung treffen. "warum_nicht" = Megans Grund fuer naheliegende Fehlgriffe
# (Notiz gehoert zum Punkt, trifft aber nicht diese Behauptung) - englisch, trocken, vertont unter
# vh.f<nr>.<runde>[.n].<i>.wn.<fakt>. Schluessel: (fall, runde, nachgebessert 0/1, zeile).
WER = "Your note doesn't say who."
FALSCHE_ZEILEN = {
    (1, "handlung", 0, 1): {"beruehrt": ["f1_02", "f1_06"]},
    (1, "handlung", 1, 1): {"beruehrt": ["f1_05"],
                            "warum_nicht": {"f1_02": "That's what the screen said at six. It doesn't put anyone on the bridge."}},
    (1, "person", 0, 1): {"beruehrt": ["f1_07", "f1_09"],
                          "warum_nicht": {"f1_05": "Someone was on the bridge at ten past two. " + WER,
                                          "f1_08": "She printed an exercise the day before. That puts her at a printer, not on the bridge."}},
    (1, "person", 1, 1): {"beruehrt": [],
                          "warum_nicht": {"f1_10": "She left the mess. Your note doesn't say where she went.",
                                          "f1_05": "Someone was on the bridge at ten past two. " + WER}},
    (1, "folge", 0, 0): {"beruehrt": ["f1_13"],
                         "warum_nicht": {"f1_05": "That's when it was switched on. Not whether anything switched it off again."}},
    (1, "folge", 1, 1): {"beruehrt": ["f1_01", "f1_02"]},
    (2, "handlung", 0, 1): {"beruehrt": ["f2_04", "f2_05"]},
    (2, "handlung", 1, 1): {"beruehrt": ["f2_03"],
                            "warum_nicht": {"f2_04": "That's the plan's own number. It's exactly what she's quoting."}},
    (2, "person", 0, 1): {"beruehrt": [],
                          "warum_nicht": {"f2_04": "A route plan doesn't say where she was that morning.",
                                          "f2_06": "That's about the waypoint, First Officer. Not about the bridge."}},
    (2, "person", 1, 1): {"beruehrt": ["f2_05"],
                          "warum_nicht": {"f2_02": "Asking how far a waypoint is isn't wanting something there.",
                                          "f2_07": "Asking how far a waypoint is isn't wanting something there."}},
    (2, "folge", 0, 1): {"beruehrt": [],
                         "warum_nicht": {"f2_11": "That's what ten point six knots would do. It doesn't say she went that fast."}},
    (2, "folge", 1, 1): {"beruehrt": ["f2_01", "f2_03"]},
    (3, "handlung", 0, 1): {"beruehrt": ["f3_05", "f3_03"]},
    (3, "handlung", 1, 1): {"beruehrt": [],
                            "warum_nicht": {"f3_04": "No charging run, yes. That says nothing about when she left."}},
    (3, "person", 0, 1): {"beruehrt": ["f3_10", "f3_11", "f3_19"]},
    (3, "person", 1, 1): {"beruehrt": [],
                          "warum_nicht": {"f3_06": "The file shows when the plan was drafted. Not whose wish it was.",
                                          "f3_12": "That's about the diesel, not the sunrise."}},
    (3, "folge", 0, 1): {"beruehrt": ["f3_03"]},
    (3, "folge", 1, 1): {"beruehrt": [],
                         "warum_nicht": {"f3_03": "That's what happened without a charging run. The line is about one with it."}},
    (4, "handlung", 0, 1): {"beruehrt": ["f4_02", "f4_04", "f4_06", "f4_13"]},
    (4, "handlung", 1, 1): {"beruehrt": ["f4_04"]},
    (4, "person", 0, 1): {"beruehrt": ["f4_13"],
                          "warum_nicht": {"f4_05": "That's the morning. She's talking about the night.",
                                          "f4_10": "Quarter to eight is the morning. She's talking about after her round."}},
    (4, "person", 1, 1): {"beruehrt": ["f4_09"],
                          "warum_nicht": {"f4_03": "Card two hangs on a hook. Your note doesn't say whose hand took it.",
                                          "f4_07": "A bet isn't a lock, First Officer.",
                                          "f4_08": "A bet isn't a lock, First Officer."}},
    (4, "folge", 0, 1): {"beruehrt": ["f4_15", "f4_06"]},
    (4, "folge", 1, 1): {"beruehrt": ["f4_01", "f4_02", "f4_06"]},
    (5, "handlung", 0, 1): {"beruehrt": ["f5_02", "f5_04"]},
    (5, "handlung", 1, 1): {"beruehrt": ["f5_03"]},
    (5, "person", 0, 1): {"beruehrt": [],
                          "warum_nicht": {"f5_07": "That puts him at the stern board. It doesn't say where he charged.",
                                          "f5_04": "Something drew four point six kilowatts. Your note doesn't say what."}},
    (5, "person", 1, 1): {"beruehrt": [],
                          "warum_nicht": {"f5_04": "The board was closed by hand. Your note doesn't say whose.",
                                          "f5_05": "That's an adapter, not a switch."}},
    (5, "folge", 0, 1): {"beruehrt": ["f5_13", "f5_03", "f5_07"]},
    (5, "folge", 1, 1): {"beruehrt": ["f5_03", "f5_01", "f5_07"]},
}


def falsche_zeilen_anwenden(faelle):
    """FALSCHE_ZEILEN in die Saetze schreiben; jede Zeile muss falsch sein und jede Notiz zum Punkt gehoeren."""
    for (nr, r, nb, i), extra in FALSCHE_ZEILEN.items():
        runde = faelle[nr]["runden"][r]
        s = (runde["nachbessern"]["saetze"] if nb else runde["saetze"])[i]
        assert s["falsch"], (nr, r, nb, i)
        if extra.get("beruehrt"):
            s["beruehrt"] = list(extra["beruehrt"])
        if extra.get("warum_nicht"):
            s["warum_nicht"] = dict(extra["warum_nicht"])
    for nr, f in faelle.items():
        for r, runde in f.get("runden", {}).items():
            for nb, liste in ((0, runde.get("saetze", [])), (1, (runde.get("nachbessern") or {}).get("saetze", []))):
                for i, s in enumerate(liste):
                    assert not s.get("falsch") or (nr, r, nb, i) in FALSCHE_ZEILEN, ("ohne Eintrag", nr, r, nb, i)


def main():
    falsche_zeilen_anwenden(FAELLE)
    daten = {"_hinweis": "erzeugt von werkzeuge/eden_rise/anhoerung_aussagen.py - nicht von Hand aendern",
             "faelle": {str(k): v for k, v in FAELLE.items()}}
    with open(ZIEL, "w", encoding="utf-8") as fh:
        json.dump(daten, fh, ensure_ascii=False, indent=1)
    print("geschrieben:", ZIEL, "|", len(FAELLE), "Fall/Faelle")


if __name__ == "__main__":
    main()
