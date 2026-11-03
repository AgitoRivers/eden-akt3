# -*- coding: utf-8 -*-
"""Bordrat - 30 Events, nachts zwischen den Tagen ("tage" = der Tag, der gerade endet).
Eine Person stellt das Problem vor (sprecher), zwei vertreten Positionen (links/rechts) mit je einer Kachel."""
from ereignisse_basis import *  # noqa: F401,F403

N = ["nacht"]
EVENTS = [
    # 18.10.2026 (neue Tageszaehlung): erste Nacht ohne Holm, Rosi findet den Vorrat
    E("br_lolas_notvorrat", "bordrat", "witzig", "Lola's Emergency Stash", WANN((2, 2), N), "galley",
      {"sprecher": "rosi", "links": "chiara", "rechts": "toto"}, "Clearing out the galley freezer to save power, "
                                                                 "Rosi found a kilo of weed. Neatly vacuum-packed "
                                                                 "and labelled “BASIL ♥”. She drops the bag on the "
                                                                 "table in front of you and folds her arms.",
      [Z("rosi", "Found this behind the fish. Holm's gone, so it's your crew now, Officer. Let's see what you do "
                 "with it.", "annoyance"),
       Z("chiara", "Overboard, tonight. If the coast guard finds that, we lose the boat and every licence we've got.", "anger"),
       Z("toto", "Comandante, overboard is a crime against nature. I keep it safe, nobody knows, and Lola stays "
                 "happy. Everybody wins.", "amusement")],
      [O("“Chiara's right. The bag goes overboard tonight.”", [V("chiara", 6), V("rosi", 4), R(5), V("lola", -8), W("moral", -1), REG("kein_gras_an_bord")], von="chiara"),
       O("Pushes the bag over to Totò. “Keep it safe, and nobody knows.”", [V("lola", 6), V("toto", 4), V("chiara", -4), KR(10)], von="toto"),
       O("Ship's rule: only after duty, never on deck.", [REG("gras_nur_nach_dienst")], probe=P("empathy", 12),
         erfolg=[V("chiara", 4), V("toto", 4), V("rosi", 4), R(5)], fehlschlag=[V("rosi", -4)], art="dritter_weg",
         zeile=Z("rosi", "Hm. Diplomatic. Holm would have thrown it at the moon. We'll see if your rule holds.", "approval")),
       O("Promise to Chiara: “From tomorrow I'll check the galley myself.”",
         [VER("chiara", "Duc checks the galley himself", 2, {"flag": "kombuese_kontrolliert"}), V("chiara", 2)], art="versprechen")],
      sets={"rosi": "Off Duty", "chiara": "Uniform"}),

    E("br_drei_minuten", "bordrat", "wholesome", "Three Minutes of Water", WANN((2, 5), N),
      "crew_mess", {"sprecher": "sophia", "links": "chiara", "rechts": "siri"},
      "The watermaker can't keep up with thirteen people. Sophia has drawn a shower schedule on a napkin. At the "
      "bottom there's a sad face.",
      [Z("sophia", "Thirteen people, one watermaker. Someone's going to cry in a cold shower tomorrow, darling. We "
                   "just have to decide who.", "amusement"),
       Z("chiara", "Three minutes each, on a schedule, and guests go first. That's the job.", "neutral"),
       Z("siri", "Give my minutes to the crew. Honestly, it's fine. I can wash my hair in the sea, I grew up doing "
                 "that.", "caring")],
      [O("Ship's rule: the three-minute shower.", [REG("drei_minuten_dusche"), W("moral", -1), V("chiara", 4)], von="chiara"),
       O("Takes Siri's side. “The guests give their shower minutes to the crew.”", [V("siri", 6), W("moral", 1), V("yasin", -8)], von="siri"),
       O("Lea builds a saltwater shower on the swim platform.", [], probe=P("courage", 10),
         erfolg=[W("moral", 1), V("lea", 4), GAG("kalte_dusche")], fehlschlag=[GAG("kalte_dusche")], art="dritter_weg")],
      sets={"sophia": "Concierge", "chiara": "Service", "siri": "Dad's Sweater"}),

    E("br_gaestekabinen", "bordrat", "ernst", "The Guest Cabins", WANN((2, 4), N), "main_salon",
      {"sprecher": "chiara", "links": "sophia", "rechts": "siri"},
      "Megan has written: the guest cabins are to be stripped and the minibars counted. Today. Chiara reads the "
      "message out without moving a muscle in her face.",
      [Z("chiara", "Megan wants the guest cabins stripped and the minibars counted tonight. She calls it cost discipline, and I call it humiliating.", "annoyance"),
       Z("sophia", "Do half, darling. Count the minibars, leave the cabins. She gets her numbers and nobody loses "
                   "face.", "neutral"),
       Z("siri", "I'm still sleeping in one of those cabins. Just so everyone remembers that.", "disappointment")],
      [O("“Count the minibars and leave the cabins, like Sophia says.”", [V("sophia", 6), V("megan", 4), V("siri", -4)], von="sophia"),
       O("“No stripping and no counting. The guest cabins stay as they are.”", [V("siri", 6), V("megan", -6), R(3)], von="siri"),
       O("Ship's rule: the guest area stays the guest area.", [REG("gaestebereich"), V("chiara", 4), V("megan", -4)], art="bordregel"),
       O("Picks up the phone. “I'll call Megan myself.”", [], probe=P("charm", 14), erfolg=[V("megan", 6), V("chiara", 4), F("megan_umgestimmt")],
         fehlschlag=[V("megan", -6), R(-3)], art="dritter_weg")],
      sets={"chiara": "Uniform", "sophia": "Concierge", "siri": "Silver Night"}),

    E("br_yasins_angebot", "bordrat", "ernst", "Yasin's Offer", WANN((2, 5), N, bed={"nicht": {"flag": "siri_frei"}}),
      "main_salon", {"sprecher": "sophia", "links": "yasin", "rechts": "chiara"},
      "Yasin is offering five hundred euros if the crew plays along in his video tomorrow. “Stranded with an "
      "Influencer”, with laughs, drama and bikinis. Sophia puts the envelope on the table.",
      [Z("sophia", "Five hundred euros in cash, darling. He wants the crew in his video tomorrow, with smiles, drama and swimwear.", "neutral"),
       Z("yasin", "It's free publicity, bro. My people love a shipwreck. You'll be famous. Small famous, but famous.", "pride"),
       Z("chiara", "We are not his props. We work here, and some of us would like to keep working here.", "anger")],
      [O("Takes the envelope. “Everyone plays along in Yasin's video tomorrow.”", [G(500), V("yasin", 6), V("chiara", -6), R(-5), U("yasin_video", 1)], von="yasin"),
       O("Pushes the envelope back. “We are not your props, Yasin.”", [V("chiara", 6), V("yasin", -6), R(3)], von="chiara"),
       O("“Whoever wants to be in the video can be. Nobody has to.”", [G(250), V("yasin", 2), V("lea", 4), V("chiara", -2)], probe=P("cunning", 12),
         erfolg=[R(3)], fehlschlag=[R(-3)], art="dritter_weg"),
       O("Ship's rule: cameras off after ten.", [REG("kamera_aus_22"), V("yasin", -4), V("siri", 4)], art="bordregel")],
      sets={"sophia": "Concierge", "chiara": "Uniform"}),

    E("br_festa_auftritt", "bordrat", "witzig", "The Crew as a Festa Attraction", WANN((3, 4), N), "crew_mess",
      {"sprecher": "rosi", "links": "lea", "rechts": "chiara"},
      "Madame Casanova wants the crew on a stage at the festa, in sailor costumes, with a song. Rosi holds up the "
      "letter and can't stop laughing.",
      [Z("rosi", "The mayor wants us on stage in sailor costumes, singing, and she drew a picture, Officer. There's an actual picture.", "amusement"),
       Z("lea", "Yes! Yes yes yes. I can do the dance. I already know a dance, I've known it for years.", "excitement"),
       Z("chiara", "Absolutely not. We are a professional crew, not a cruise-ship cabaret.", "disgust")],
      [O("“We'll do the mayor's show. Costumes, song, everything.”", [W("ruf", 1), V("lea", 6), V("casanova", 6), V("chiara", -4), GAG("casanova_kapelle")], von="lea"),
       O("“Thank the mayor for us, and tell her no.”", [V("chiara", 6), V("casanova", -4), W("moral", -1)], von="chiara"),
       O("“Nobody else has to do it. I'll sing for the mayor, alone.”", [], probe=P("courage", 13), erfolg=[W("ruf", 2), W("moral", 1), V("casanova", 8)],
         fehlschlag=[W("moral", 1), V("chiara", 2), GAG("casanova_kapelle")], art="dritter_weg",
         zeile=Z("rosi", "Oh no. Oh, this I have to see.", "amusement"))],
      sets={"rosi": "Off Duty", "lea": "Off Duty", "chiara": "Uniform"}),

    E("br_nachtwache", "bordrat", "wholesome", "Who Keeps Watch?", WANN((2, 6), N), "crew_mess",
      {"sprecher": "chiara", "links": "rosi", "rechts": "lea"},
      "Someone has to watch the anchor until sunrise. Rosi has barely slept, but she says she can do it. Lea "
      "volunteers so fast she nearly falls off her chair.",
      [Z("chiara", "Someone has to watch the anchor until sunrise, and Rosi has slept four hours since we got here.", "caring"),
       Z("rosi", "I'm fine, I'm Sicilian. We don't sleep, we just close our eyes angrily for a while.", "pride"),
       Z("lea", "Me! Let me. I've never done a real night watch. I'll be so awake. Look how awake I am already.", "excitement")],
      [O("Gives the night watch to Rosi. “You're Sicilian. Close your eyes angrily up there.”", [V("rosi", 4), EN(-1), F("rosi_muede")], von="rosi"),
       O("Gives the night watch to Lea. “Stay awake, and wake me if the anchor moves.”", [V("lea", 6), V("rosi", 2)], von="lea"),
       O("Keeps the night watch himself. “Go to bed, both of you.”", [EN(-1), R(5), V("chiara", 4)], art="dritter_weg"),
       O("Ship's rule: quiet hours from midnight, and a watch rota.", [REG("nachtruhe"), V("chiara", 4)], art="bordregel")],
      sets={"chiara": "Bridge Night", "rosi": "Engine Room", "lea": "Off Duty"}),

    E("br_petrus_boot", "bordrat", "wholesome", "Petru's Morning Catch", WANN((2, 5), N, bed={"wert": ["vertrauen.petru", ">=", 2]}),
      "aft_deck", {"sprecher": "lea", "links": "lea", "rechts": "rosi"},
      "Petru will take two of the crew fishing at dawn. Whoever goes is gone until noon. Lea already has her boots "
      "on.",
      [Z("lea", "Petru's taking two of us fishing at dawn. Real fishing! With nets! I'm going. Who else?", "excitement"),
       Z("lea", "And he says if we catch enough, Alva buys the rest. Money and dinner, Duc!", "joy"),
       Z("rosi", "I need hands here tomorrow, not on a fishing boat. But fine, go on, abandon me.", "annoyance")],
      [O("Goes with Lea and Petru at dawn. “Back by noon, Rosi.”", [V("lea", 6), V("petru", 6), W("moral", 1), G(80), V("rosi", -2), I("frischer_fang")], von="lea"),
       O("“Nobody goes, Lea. Rosi needs every hand here tomorrow.”", [V("rosi", 4), U("reparatur", 1), W("moral", -1)], von="rosi"),
       O("“Lea and Totò go with Petru. I stay here.”", [], probe=P("cunning", 11), erfolg=[G(120), V("toto", 4), V("lea", 4)],
         fehlschlag=[G(20), V("toto", 2)], art="dritter_weg")],
      sets={"lea": "Expedition", "rosi": "Engine Room"}),

    E("br_elsas_kontrolle", "bordrat", "ernst", "Elsa Comes Tomorrow", WANN((2, 6), N), "crew_mess",
      {"sprecher": "sophia", "links": "toto", "rechts": "chiara"},
      "Lieutenant Ferrandi has announced an inspection for tomorrow. Totò goes pale and glances towards the "
      "storeroom. Chiara sees it.",
      [Z("sophia", "Lieutenant Ferrandi inspects us tomorrow at ten. She asked, very politely, whether we have "
                   "anything to declare.", "neutral"),
       Z("toto", "Comandante, a few boxes take a little boat trip tonight, and they're back tomorrow evening. Nobody sees nothing.", "nervousness"),
       Z("chiara", "Or we declare everything and stop being a floating flea market.", "disapproval")],
      [O("Nods at Totò. “Take the crates out tonight, and have them back tomorrow evening.”", [V("toto", 6), V("chiara", -4), KR(-10)], probe=P("cunning", 13),
         erfolg=[F("kontrolle_sauber")], fehlschlag=[V("elsa", -8), W("ruf", -1), F("schmuggel_gefunden")], von="toto"),
       O("Sides with Chiara. “We declare everything to Elsa.”", [V("chiara", 6), V("elsa", 6), V("toto", -8), F("kontrolle_sauber")], von="chiara"),
       O("Call Elsa today and talk to her honestly.", [], probe=P("charm", 13), erfolg=[V("elsa", 6), V("toto", 2), F("elsa_vorgewarnt")],
         fehlschlag=[V("elsa", -2), V("toto", -2)], art="dritter_weg")],
      sets={"sophia": "Concierge", "chiara": "Uniform"}),

    E("br_dorfkinder", "bordrat", "wholesome", "The Village Kids", WANN((2, 6), N), "aft_deck",
      {"sprecher": "lea", "links": "chiara", "rechts": "siri"},
      "Every day three kids from the village row out to the yacht and stare. Today they held up a sign: “Tour "
      "please?” Lea took a photo of it.",
      [Z("lea", "They made a sign, Duc. A sign! “Tour please.” With a drawing of us. I'm the one with the big hair.", "joy"),
       Z("chiara", "Children on a superyacht with no power? The insurance would die, and then I would die.", "nervousness"),
       Z("siri", "Let them come. I'll show them the sea turtles on my phone. They don't care about the gold taps anyway.", "caring")],
      [O("“Chiara's right. No kids on board, it's too risky.”", [V("chiara", 4), V("lea", -4), W("moral", -1)], von="chiara"),
       O("“Let the kids come for a tour in the afternoon.”", [W("ruf", 1), V("siri", 6), V("lea", 4), V("casanova", 4), V("chiara", -2), I("muschelkette_kinder")], von="siri"),
       O("Lea only shows them the swim platform, in life jackets.", [], probe=P("perception", 10),
         erfolg=[W("ruf", 1), V("lea", 6), V("chiara", 2)], fehlschlag=[W("ruf", 1), V("chiara", -4)], art="dritter_weg")],
      sets={"lea": "Deck", "chiara": "Uniform", "siri": "Morning Ritual"}),

    E("br_siris_geburtstag", "bordrat", "wholesome", "Siri's Birthday", WANN((2, 6), N), "galley",
      {"sprecher": "lola", "links": "sophia", "rechts": "yasin"},
      "Lola found Siri's passport in the laundry. It's her birthday tomorrow, and she hasn't told anyone. Yasin "
      "knew, but he has other plans.",
      [Z("lola", "It's Siri's birthday tomorrow and she didn't tell anyone. That's the saddest thing I've ever "
                 "heard, mate.", "sadness"),
       Z("sophia", "Something small, breakfast on the foredeck with no cameras, just us. I'll organise it.", "caring"),
       Z("yasin", "Bro, I have a whole concept. Drone shot, champagne, a sponsored cake. It's content. She loves content.", "pride")],
      # Siris Dank (26.10.2026, Duc): zugleich das Echo der Dankeskarte in der Keepsake Box
      [O("“Sophia organises a small breakfast on the foredeck, with no cameras.”", [V("siri", 8), V("sophia", 4), V("yasin", -4), U("siri_marke", 1), I("siris_karte")], von="sophia",
         zeile=Z("siri", "Thank you for my first birthday without a camera. I mean it. Don't make it weird.", "joy")),
       O("Lets Yasin have his way. “Drone, champagne, sponsored cake. Do it.”", [V("yasin", 6), V("siri", -4), U("yasin_video", 1), W("moral", -1)], von="yasin"),
       O("Lola bakes something, and only the crew sings.", [], probe=P("empathy", 10), erfolg=[V("siri", 6), V("lola", 6), W("moral", 1)],
         fehlschlag=[V("lola", 4)], art="dritter_weg")],
      sets={"lola": "Galley", "sophia": "Writing Night"}),

    E("br_crew_kasse", "bordrat", "frech", "Yacht Stuff for the Crew Fund?", WANN((3, 6), N), "crew_mess",
      {"sprecher": "sophia", "links": "toto", "rechts": "chiara"},
      "Totò has made a list. Two crates of champagne, four bathrobes, a spare propeller. All Eden Group property, "
      "all easy to sell.",
      [Z("sophia", "Totò made a list of things nobody would miss. It's a long list. It's a very confident list.", "amusement"),
       Z("toto", "Two crates of champagne, Comandante. The Group writes it off as breakage, and we eat for a week.", "joy"),
       Z("chiara", "That is theft, with a list, in handwriting.", "disgust")],
      [O("Nods at Totò's list. “Sell it all. We have to eat.”", [G(400), V("toto", 6), V("chiara", -8), F("yachtware_verkauft"), KR(10)], von="toto"),
       O("Hands the list back to Totò. “No. That's stealing from the Group.”", [V("chiara", 6), V("toto", -4)], von="chiara"),
       O("“Sell the champagne, but only to Alva. The rest stays on board.”", [G(200), V("alva", 4), V("toto", 4), V("chiara", -4)], probe=P("cunning", 12),
         erfolg=[], fehlschlag=[KL("duc", "alva", "Duc sold the yacht's champagne")], art="dritter_weg")],
      sets={"sophia": "Concierge", "chiara": "Service"}),

    E("br_lola_krank", "bordrat", "witzig", "Who Cooks Tomorrow?", WANN((2, 6), N), "galley",
      {"sprecher": "chiara", "links": "rosi", "rechts": "sophia"},
      "Lola is lying in her bunk with sunstroke, mumbling recipes. So someone else cooks tomorrow. Rosi has already "
      "tied on an apron. That scares everyone.",
      [Z("chiara", "Lola has sunstroke and is reciting risotto in her sleep. Someone else cooks tomorrow.", "neutral"),
       Z("rosi", "I'll cook, how hard can it be? It's just chemistry with garlic.", "pride"),
       Z("sophia", "Or we order from Alva, darling, and nobody gets poisoned. Just a thought.", "amusement")],
      [O("“All right, Rosi. You cook tomorrow.”", [], probe=P("courage", 12), erfolg=[V("rosi", 8), W("moral", 1)],
         fehlschlag=[W("moral", -1), V("rosi", 4)], von="rosi",
         zeile=Z("rosi", "If anyone says the word “burnt”, they sleep on deck.", "anger")),
       O("Sides with Sophia. “We order from Alva, and nobody gets poisoned.”", [G(-90), V("alva", 4), W("moral", 1)], von="sophia"),
       O("Takes the apron off Rosi. “I'll cook tomorrow.”", [EN(-1), V("lola", 4), V("chiara", 4), W("moral", 1)], art="dritter_weg")],
      sets={"chiara": "Service", "rosi": "Off Duty", "sophia": "Concierge"}),

    E("br_kevin_nest", "bordrat", "witzig", "Kevin Builds a Nest", WANN((3, 6), N, bed={"flag": "gag_kevin_1"}), "solar_deck",
      {"sprecher": "rosi", "links": "lea", "rechts": "toto"},
      "Kevin the seagull has built a nest on the solar deck. Right on top of a panel. He makes a mess of anything he "
      "doesn't like. He doesn't like anything.",
      [Z("rosi", "Kevin built a nest on panel four. Panel four now makes eight percent less power and one hundred percent more poop.", "anger"),
       Z("lea", "You can't move a nest! What if there are eggs? What if Kevin's a mum?", "fear"),
       Z("toto", "In Napoli we have a word for a fat seagull, Comandante. The word is dinner.", "amusement")],
      [O("“Leave the nest. Kevin can stay on panel four.”", [V("lea", 6), V("rosi", -4), GAG("kevin")], von="lea"),
       O("“The nest goes, and so does Kevin. Sorry, Lea.”", [V("toto", 4), V("lea", -8), V("rosi", 2)], von="toto",
         zeile=Z("lea", "I will never forgive you. Ever. Maybe tomorrow.", "sadness")),
       O("Move the nest carefully to the railing.", [], probe=P("courage", 12), erfolg=[V("lea", 6), V("rosi", 4), GAG("kevin")],
         fehlschlag=[V("lea", 2), GAG("kevin"), W("moral", 1)], art="dritter_weg")],
      gag="kevin", sets={"rosi": "Engine Room", "lea": "Deck"}),

    E("br_singen_ohne_strom", "bordrat", "wholesome", "Singing Without Power", WANN((2, 6), N), "aft_deck",
      {"sprecher": "lola", "links": "siri", "rechts": "yasin"},
      "Lola wants to sing on the aft deck tomorrow night. Just a guitar, candles and everyone. Siri would sing "
      "along, but only if nobody films it. Yasin has already unpacked his tripod.",
      [Z("lola", "Tomorrow night: candles, my guitar, everyone sings. No speakers, no power, just vibes.", "joy"),
       Z("siri", "I'd sing, really, I would, but only if nobody films it. Not one second.", "nervousness"),
       Z("yasin", "Babe, unplugged content performs insane. It's authentic. I'll just film a little bit.", "neutral")],
      [O("Takes Siri's side. “No phones and no cameras tomorrow night. That means you, Yasin.”", [V("siri", 8), V("lola", 4), V("yasin", -6), W("moral", 1), U("siri_marke", 1)], von="siri"),
       O("Yasin can film. He pays for the footage.", [V("yasin", 6), V("siri", -6), U("yasin_video", 1), G(120), W("moral", -1)], von="yasin"),
       O("Ship's rule: cameras off after ten.", [REG("kamera_aus_22"), V("siri", 4), V("yasin", -4), W("moral", 1)], art="bordregel")],
      sets={"lola": "Off Duty", "siri": "Dad's Sweater"}),

    E("br_ein_tisch", "bordrat", "wholesome", "One Table for Everyone", WANN((2, 5), N), "aft_deck",
      {"sprecher": "sophia", "links": "chiara", "rechts": "lola"},
      "Until now the guests have eaten in the salon and the crew in the mess. Lola thinks that's silly now that "
      "everyone's in the same boat. Chiara doesn't think etiquette is silly.",
      [Z("sophia", "Guests in the salon, crew in the mess. Lola wants one table for everyone. Chiara wants a word with Lola.", "amusement"),
       Z("chiara", "There are rules for a reason. Guests pay for distance, even stranded guests.", "neutral"),
       Z("lola", "We're all stuck in the same bay, mate, so let's eat like a family. A weird family, with a seagull.", "joy")],
      [O("“Chiara's right. Guests in the salon, crew in the mess.”", [V("chiara", 6), V("lola", -4), W("moral", -1)], von="chiara"),
       O("Sides with Lola. “One table for everyone, guests and crew.”", [V("lola", 6), W("moral", 1), V("siri", 4), V("chiara", -4)], von="lola"),
       O("“One evening a week, we all eat together.”", [], probe=P("charm", 11), erfolg=[V("chiara", 4), V("lola", 4), W("moral", 1)],
         fehlschlag=[V("chiara", -2), V("lola", 2)], art="dritter_weg")],
      sets={"sophia": "Concierge", "chiara": "Service", "lola": "Galley"}),

    E("br_megan_kommt", "bordrat", "witzig", "The Boss Is Coming", WANN((4, 4), N, bed={"flag": "megan_angekuendigt"}), "main_salon",
      {"sprecher": "chiara", "links": "chiara", "rechts": "rosi"},
      "Megan lands tomorrow by helicopter. Chiara wants to polish all night. Rosi wants to show Megan how broken "
      "everything is, with a sign.",
      [Z("chiara", "Megan lands tomorrow, and I want this boat to shine, every brass handle and every glass.", "nervousness"),
       Z("chiara", "If she sees one fingerprint, she'll mention it in front of everyone. Slowly.", "fear"),
       Z("rosi", "Or we let her see the truth. I'll make a sign that says broken, in three languages.", "amusement")],
      [O("“Chiara's right. We polish the whole boat tonight, every handle and every glass.”", [EN(-1), V("chiara", 6), V("megan", 4), W("moral", -1)], von="chiara"),
       O("“Make your sign, Rosi. Let Megan see the truth.”", [V("rosi", 6), V("megan", -2), GAG("megan_lacht")], von="rosi",
         zeile=Z("rosi", "Broken, kaputt, rotto, and a little drawing underneath. She'll love it.", "joy")),
       O("“We polish the salon and nothing else.”", [], probe=P("perception", 11), erfolg=[V("chiara", 4), V("megan", 4)],
         fehlschlag=[V("megan", -2)], art="dritter_weg")],
      sets={"chiara": "Uniform", "rosi": "Engine Room"}),

    E("br_nacktbaden", "bordrat", "frech", "Skinny Dipping, with Consequences", WANN((2, 6), N), "swim_platform",
      {"sprecher": "sophia", "links": "lea", "rechts": "chiara"},
      "Lea and Siri went skinny dipping last night. Elsa's patrol boat came past at exactly that moment. With a "
      "searchlight.",
      [Z("sophia", "So. Lea and Siri went skinny dipping. And Lieutenant Ferrandi's patrol boat has a searchlight. A "
                   "very good one.", "amusement"),
       Z("lea", "It was romantic! The plankton was glowing! And then a boat was glowing. At us.", "embarrassment"),
       Z("chiara", "The coast guard has now seen half our crew naked, so I need a rule. I need several rules.", "annoyance")],
      [O("Shrugs at Chiara. “Nothing happened, really. Two people went for a swim.”", [V("lea", 6), V("siri", 4), V("chiara", -4), V("elsa", -2)], von="lea"),
       O("“Chiara gets her rule. From now on, swimwear only.”", [V("chiara", 6), V("lea", -2), W("moral", -1)], von="chiara"),
       O("Send Elsa a letter of apology, with Lola's cake.", [], probe=P("charm", 11),
         erfolg=[V("elsa", 6), V("lea", 4)], fehlschlag=[V("elsa", 2), GAG("toto_cousin")], art="dritter_weg")],
      sets={"sophia": "Writing Night", "lea": "Leopard Bikini", "chiara": "Bridge Night"}),

    E("br_rosi_ueberstunden", "bordrat", "ernst", "Rosi Works Too Much", WANN((3, 6), N), "power_room",
      {"sprecher": "sophia", "links": "rosi", "rechts": "chiara"},
      "For three days Rosi has worked more than sixteen hours a day. Today she fell asleep standing up in the engine "
      "room. Chiara wants you to forbid it.",
      [Z("sophia", "Rosi fell asleep standing up today, darling. With a screwdriver in her mouth.", "caring"),
       Z("rosi", "I'm fine. One more day, then I sleep. Promise. Maybe. Don't look at me like that.", "annoyance"),
       Z("chiara", "Order her to rest. She won't listen to me, but she listens to you, apparently.", "caring")],
      [O("“All right, Rosi. One more day, then you sleep.”", [V("rosi", 4), U("reparatur", 1), EN(-1), F("rosi_muede"), W("moral", -1)], von="rosi"),
       O("“You take tomorrow off, Rosi. That's an order.”", [V("chiara", 4), V("rosi", -2), F("rosi_frei")], von="chiara",
         zeile=Z("rosi", "Fine. Fine! I'll rest. Aggressively.", "anger")),
       O("Promise to Rosi: “I'll take your late shift tomorrow.”",
         [VER("rosi", "Duc takes Rosi's late shift", 1, {"flag": "rosi_schicht_uebernommen"}), V("rosi", 6)], art="versprechen")],
      sets={"sophia": "Concierge", "rosi": "Engine Room", "chiara": "Uniform"}),

    E("br_netze_flicken", "bordrat", "wholesome", "Petru's Price", WANN((3, 6), N, bed={"wert": ["vertrauen.petru", ">=", 1]}),
      "village_harbour", {"sprecher": "lea", "links": "rosi", "rechts": "lea"},
      "Petru won't take money for his fish. He wants something else: tomorrow morning two of the crew mend his nets. "
      "Three hours, in the sun, with an old man who doesn't talk.",
      [Z("lea", "Petru won't take money for the fish. He wants two of us to mend his nets tomorrow. Three hours.", "neutral"),
       Z("rosi", "Three hours I don't have. Pay the man in euros, like a normal person.", "annoyance"),
       Z("lea", "He said euros are for tourists, nets are for friends. I think that's beautiful, honestly.", "admiration")],
      [O("Sides with Rosi. “We pay Petru in euros for the fish.”", [G(-60), V("rosi", 2), V("petru", -2)], von="rosi"),
       O("“Lea and I will mend his nets tomorrow.”", [EN(-1), V("petru", 8), V("lea", 6), I("netzknoten")], von="lea"),
       O("“Send Totò to Petru instead, with a bottle of wine.”", [], probe=P("cunning", 11), erfolg=[V("petru", 4), V("toto", 2)],
         fehlschlag=[V("petru", -4), V("toto", 2)], art="dritter_weg")],
      sets={"rosi": "Vespa Sunday", "lea": "Expedition"}),

    E("br_siri_umzug", "bordrat", "ernst", "Siri Wants to Move", WANN((2, 6), N, bed={"nicht": {"flag": "siri_frei"}}),
      "crew_corridor", {"sprecher": "sophia", "links": "siri", "rechts": "yasin"},
      "Siri asked Sophia whether there's a free bunk in one of the crew cabins. Just for a few nights. Yasin has "
      "found out, and now he's standing in the corridor.",
      [Z("sophia", "Siri asked if a crew bunk is free, just for a few nights. Yasin found out, and now he's in the corridor.", "neutral"),
       Z("siri", "I just need a bit of space. To sleep. To think. That's all. Please don't make this a thing.", "sadness"),
       Z("yasin", "Bro, she's my girlfriend. She sleeps in the VIP cabin. With me. That's not a crew decision.", "anger")],
      [O("“Give Siri the crew bunk, Sophia. That's my decision, Yasin.”", [V("siri", 8), V("yasin", -8), U("siri_marke", 1)], von="siri",
         zeile=Z("siri", "Thank you. Really. You didn't have to.", "gratitude")),
       O("Stays out of it. “You two sort this out yourselves.”", [V("yasin", 4), V("siri", -4)], von="yasin"),
       O("“It's Siri's choice. If she moves, the crew helps her.”", [], probe=P("empathy", 12), erfolg=[V("siri", 6), U("siri_marke", 1), R(3)],
         fehlschlag=[V("siri", 2), V("yasin", -4)], art="dritter_weg")],
      sets={"sophia": "Writing Night", "siri": "Dad's Sweater"}),

    E("br_trinkgeld", "bordrat", "ernst", "An Envelope for Lea", WANN((2, 6), N), "crew_mess",
      {"sprecher": "lea", "links": "lea", "rechts": "toto"},
      "Yasin gave Lea an envelope with two hundred and fifty euros in it. “For you, sweetheart. You can thank me later.” Lea "
      "holds it between two fingers, as if it were wet.",
      [Z("lea", "Yasin gave me this. Two hundred and fifty euros. He said I could thank him later. I don't want to thank him later.", "disgust"),
       Z("lea", "I just want to give it back. But then he'll be weird about it. Weirder.", "nervousness"),
       Z("toto", "Two-fifty is two-fifty, cara. Put it in the crew box. He can thank himself in the mirror.", "neutral")],
      [O("Takes the envelope from Lea. “I'll give it back and talk to Yasin.”", [V("lea", 8), V("yasin", -8), R(5)], von="lea"),
       O("“Totò's right, Lea. Put it in the crew box.”", [G(250), V("toto", 4), V("lea", -4), V("yasin", 2), W("moral", -1)], von="toto"),
       O("Back to Yasin, in front of everyone at breakfast.", [], probe=P("courage", 13), erfolg=[V("lea", 8), R(8), V("yasin", -10), V("siri", 4)],
         fehlschlag=[V("lea", 4), V("yasin", -6)], art="dritter_weg")],
      sets={"lea": "Off Duty"}),

    E("br_ehrenbuerger", "bordrat", "witzig", "Honorary Citizen of Cala d'Orsu", WANN((21, 21), N), "crew_mess",   # Akt 3
      {"sprecher": "rosi", "links": "lea", "rechts": "chiara"},
      "Madame Casanova wants to make you an honorary citizen at the festa. With a sash, a crown of shells and a "
      "speech. She has already made the crown. Rosi has a photo.",
      [Z("rosi", "The mayor made you a crown out of shells, Officer. There's glitter on it. So much glitter.", "amusement"),
       Z("lea", "You have to! You'd be a prince! A shell prince! I'll carry your train!", "excitement"),
       Z("chiara", "The First Officer will not wear a shell crown in public. I forbid it on behalf of the uniform.", "disapproval")],
      [O("“Tell the mayor yes. I'll wear the crown.”", [W("ruf", 2), V("casanova", 8), V("lea", 4), V("chiara", -4), GAG("casanova_kapelle"), I("muschelkrone")], von="lea"),
       O("Sides with Chiara. “No shell crown for me. Thank the mayor kindly.”", [V("chiara", 6), V("casanova", -6)], von="chiara"),
       O("Accept, but Chiara gives the speech.", [], probe=P("charm", 13), erfolg=[W("ruf", 2), V("chiara", 6), V("casanova", 6)],
         fehlschlag=[V("chiara", -4), V("casanova", 4)], art="dritter_weg")],
      sets={"rosi": "Off Duty", "lea": "Crew Party", "chiara": "Uniform"}),

    E("br_investoren_dinner", "bordrat", "ernst", "Megan's Investor Dinner", WANN((5, 5), N, bed={"flag": "megan_besuch"}),
      "main_salon", {"sprecher": "sophia", "links": "megan", "rechts": "chiara"},
      "Megan is on board and wants to host a dinner for two investors tomorrow. On the dead yacht, by candlelight. "
      "The crew is to serve as if everything were normal.",
      [Z("sophia", "Megan wants a dinner tomorrow, darling, with two investors, eight courses and candles, on our dead boat. With a smile.", "nervousness"),
       Z("megan", "A stranded yacht is a story, First Officer, and I sell stories. Your crew will serve. Beautifully. Or else.", "pride"),
       Z("chiara", "We have rice, tins and one bottle of champagne, and my people are exhausted. This is madness.", "anger")],
      [O("Nods to Megan. “Eight courses and candles, as you want it. The crew will serve.”", [V("megan", 8), EN(-1), W("moral", -1), V("chiara", -4), G(300)], von="megan"),
       O("Looks at Megan. “No dinner. This crew is exhausted.”", [V("chiara", 6), V("megan", -8), R(5)], von="chiara"),
       O("Lola cooks, and the crew eats at the table too.", [], probe=P("charm", 14), erfolg=[V("megan", 6), V("chiara", 4), V("lola", 6), W("moral", 1), GAG("megan_lacht")],
         fehlschlag=[V("megan", -4), W("moral", 1)], art="dritter_weg",
         zeile=Z("megan", "The crew at the table, with my investors. You're either a genius or insane, and I'm intrigued.", "curiosity"))],
      sets={"sophia": "Concierge", "megan": "Inspection", "chiara": "Uniform"}),

    E("br_abschiedsfest", "bordrat", "wholesome", "One Last Night", WANN((6, 6), N), "aft_deck",
      {"sprecher": "lola", "links": "lola", "rechts": "chiara"},
      "Tomorrow everything gets decided. Lola wants a party tonight. Chiara wants everyone asleep. They're both a "
      "little bit right.",
      [Z("lola", "Whatever happens tomorrow, tonight we dance, barefoot on the aft deck, and that means everyone.", "joy"),
       Z("lola", "I saved a bottle and a cake, and a joint, but that's just for me. Mostly.", "amusement"),
       Z("chiara", "Tomorrow we need clear heads, so everyone's in their bunk by midnight. Please.", "caring")],
      [O("Sides with Lola. “We dance tonight, and that means everyone.”", [W("moral", 2), V("lola", 6), EN(-1), V("chiara", -2)], von="lola"),
       O("“Chiara's right. Everyone in their bunk by midnight.”", [V("chiara", 6), W("energie", 1), V("lola", -2)], von="chiara"),
       O("“We dance until midnight, then I send everyone to bed.”", [], probe=P("charm", 12), erfolg=[W("moral", 2), V("chiara", 4), V("lola", 4), R(5)],
         fehlschlag=[W("moral", 1), EN(-1)], art="dritter_weg")],
      sets={"lola": "Off Duty", "chiara": "Harbor Night"}),
]

item("lolas_pesto", "Lola's “Special Pesto”", "verbrauch",                 # Duc 27.10.: Konsum gibt keine Moral
     text="A jar of green pesto. Very green. It lifts the mood, Lola says.")
item("muschelkrone", "Festa Shell Crown", "andenken", text="Glitter, shells and dignity. Visible in the "
                                                                "epilogue.")
item("muschelkette_kinder", "Homemade Shell Necklace with Beads", "geschenk", text="A thank-you from the village kids. "
                                                                                       "Siri loves it.")
item("frischer_fang", "Frischer Fang", "verbrauch", text="A bucket of fish. Lola turns it into "
                                                                                  "a feast.")
item("siris_karte", "Siris Dankeskarte", "andenken", text="“Thank you for my first birthday without a camera.” "
                                                          "Visible in the epilogue.")
item("netzknoten", "Petrus Netzknoten", "gluecksbringer", effekt={"vorteil": "empathy"}, text="Once a day: advantage on Empathy.")
