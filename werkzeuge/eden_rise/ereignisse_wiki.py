# -*- coding: utf-8 -*-
"""Wiki events (Duc 25.10.2026): 28 new events that replace the weakest slots of the event ranking
(docs/brain_trust/EVENT_RANKING.md, verdicts 'schärfen'/'umbauen'). Each one is built on wiki knowledge
(docs/wiki/figuren/*.md) that no event used before: family, past, small secrets, quirks.

Slots: same art, roughly the same window and people as the event they replace, so the daily mix stays.
Mechanics travel along: tipp_vorliebe, the Yasin/Siri clocks, sat_data, festa_invite/festa_eingeladen,
lea_rosi_streit (feeds gv_versoehnung), the camera gag chain (yk_*), ship's rules essen_geteilt and kein_alkohol_deck.
Reserved and left alone: Sophia's pen name, Lea's Azores application, the Margot, Chiara's licence, Holm's Bergen
night, Alva's jukebox, Totò's secret (romance steps, endings, story).
"""
from ereignisse_basis import *  # noqa: F401,F403
from ereignisse_yamamoto import YK, Y_HAWAII, M_STEWARD, J_DECK, nach


def H(anrufer, ort, art="video"):
    return {"anrufer": anrufer, "anrufer_ort": ort, "art": art}


def P1(handelnd, *betroffen):
    return {"handelnd": handelnd, "betroffen": [{"id": b[0], "ton": b[1], "was": b[2]} for b in betroffen]}


def PV(links, rechts, *zuschauer):
    return {"links": links, "rechts": rechts, "zuschauer": list(zuschauer)}


def RAT(sprecher, links, rechts):
    return {"sprecher": sprecher, "links": links, "rechts": rechts}


def VL(figur, iid):
    """Discovered preference (kern/vorlieben.aus_folge)."""
    return {"vorliebe": {"figur": figur, "item": iid, "reaktion": "mag"}}


N = ["nacht"]
TAG = ["tag"]

EVENTS = [
    # ================================================================== Handy
    E("hy_chiara_jonas", "handy", "frech", "Four Stripes", WANN((3, 6), N, bed={"wert": ["vertrauen.chiara", ">=", 2]}),
      "duc_cabin", H("chiara", "bridge"),
      "Past midnight your phone lights up. Chiara, on video, out on the bridge wing in her grandfather's old jacket. "
      "She holds the phone as if it might bite.",
      [Z("chiara", "Sorry, were you asleep? Don't answer that. My brother just sent the family a photo. Jonas. Four "
                   "stripes on his shoulders, his own ship, a feeder out of Hamburg.", "nervousness"),
       Z("chiara", "Everyone's sending fireworks. I've typed congratulations nine times and deleted it nine times. "
                   "What do I write?", "confusion")],
      [O("“Write congratulations. Then tell me what you'd write if nobody else could read it.”",
         [V("chiara", 6), B("chiara", 4), EN(-1)],
         zeile=Z("chiara", "That I'm proud of him. And that it should have been me first, and I hate that I even think "
                           "that. …Okay. He gets the first part. You get the rest.", "relief")),
       O("Looks at her, not at the phone. “Write: congratulations, keep the bridge warm, I'm coming for it.”", [],
         probe=P("charm", 12), erfolg=[B("chiara", 8), V("chiara", 4), NK("chiara"), EN(-1)],
         fehlschlag=[V("chiara", 2)],
         zeile=Z("chiara", "Ha! He'll hate it. He'll frame it and hate it. Sending. …Thank you, Duc.", "amusement")),
       O("“Send him a thumbs up. It's half past one.”", [V("chiara", -4)],
         zeile=Z("chiara", "A thumbs up. Right. Goodnight, First Officer.", "disappointment"))],
      sets={"chiara": "Bridge Night"}, knistern=True),

    # (25.10.: statt der Kastagnetten - die gehoeren der Missionskette alva_kastagnetten_*)
    E("hy_alva_sevilla", "handy", "frech", "Thirteen Years",
      WANN((3, 6), N, bed={"wert": ["vertrauen.alva", ">=", 3]}), "duc_cabin", H("alva", "alvas_bar"),
      "After midnight. Alva, on video, behind her dark bar. The chairs are up on the tables. Her phone lies face down "
      "next to a full glass she hasn't touched.",
      [Z("alva", "My mother rang. From Seville. She does it every year when the season ends. The bar has had you for "
                 "thirteen years, Alva, when do I get you back?", "sadness"),
       Z("alva", "I told her the bar needs me. That's what I always tell her. So, o figliolu. Tell me something that "
                 "isn't about the bar.", "desire")],
      [O("Leans closer to the screen. “Then let me be the thing that isn't about the bar. Tomorrow night, after "
         "closing.”", [], probe=P("charm", 12), erfolg=[V("alva", 8), B("alva", 8), NK("alva"), EN(-1)],
         fehlschlag=[V("alva", 4)]),
       O("“What would you do in Seville, if you went?”", [V("alva", 6), B("alva", 2)],
         zeile=Z("alva", "Dance. Badly at first. My grandmother's way, until the floor shakes. …Nobody has asked me "
                         "that in thirteen years.", "gratitude")),
       O("“Alva, it's half past one.”", [V("alva", -2)],
         zeile=Z("alva", "So it is. Sleep well, Officer.", "annoyance"))],
      sets={"alva": "alva_flamenco_noche"}, knistern=True),

    E("hy_alva_tafel", "handy", "frech", "Forty Years of Chalk",
      WANN((3, 6), ["tag", "abend"], bed={"wert": ["vertrauen.alva", ">=", 2]}), ORT_DUC, H("alva", "alvas_bar", "nachricht"),
      "A photo from Alva: the chalkboard behind her bar, smudged with forty years of chalk. Next to every name in the "
      "village, what they order. Underneath, a message.",
      [Z("alva", "My father kept this board for forty years. The whole village is on it. Do you want to know what the "
                 "people you're trying to impress actually eat? The first lesson is free. 🍷", "amusement")],
      [O("“Tell me.”", [V("alva", 4), F("tipp_vorliebe"), VL("petru", "fish_pie"), VL("casanova", "bouillabaisse")],
         zeile=Z("alva", "Petru, fish pie, every week since his Marie died, and every week he says it isn't as good as "
                         "hers. Madame Casanova, bouillabaisse, as long as she thinks nobody's counting the saffron.",
                 "caring")),
       O("“And what does it say next to my name?”", [], probe=P("charm", 11), erfolg=[V("alva", 6), B("alva", 4)],
         fehlschlag=[V("alva", 2)],
         zeile=Z("alva", "Nothing yet. That's the interesting part. 😏", "desire")),
       O("“I'd rather find out myself.”", [V("alva", 2)])]),

    E("hy_megan_anime", "handy", "witzig", "Pollen Season", WANN((3, 4), N), ORT_DUC, H("megan", "megan_office"),
      "One in the morning. Your phone buzzes: Megan, video. You answer. She isn't looking at the camera. Behind her a "
      "laptop is playing an anime with the sound off, and her eyes are wet.",
      [Z("megan", "This is a pocket call. I'm hanging up. …Why are you still there?", "embarrassment"),
       Z("megan", "It's an allergy. Monaco is full of pollen. If you tell a single living soul, First Officer, I will "
                  "have you reassigned to a pedalo.", "annoyance")],
      [O("“Which episode? No, really. Which one does that to you?”", [], probe=P("charm", 13),
         erfolg=[V("megan", 8), GAG("megan_lacht")], fehlschlag=[V("megan", -2)],
         zeile=Z("megan", "The last one. The robot finally gets to see the sea. …Don't. Don't you dare smile, Duc.",
                 "sadness")),
       O("“I didn't see a thing. Goodnight, Mac.”", [V("megan", 6)],
         zeile=Z("megan", "It's Megan now. …Goodnight.", "gratitude")),
       O("“Pollen. At one in the morning. In an office.”", [V("megan", -4)],
         zeile=Z("megan", "Pedalo, First Officer. Pink one. With a swan's head.", "anger")),
       O("Hangs up at once.", [V("megan", 2)], art="auflegen")],
      sets={"megan": "Boardroom"}),

    E("hy_siri_caption", "handy", "ernst", "The Caption", WANN((2, 5), TAG, bed={"nicht": {"flag": "siri_frei"}}), ORT_DUC,
      H("yasin", "sun_deck"),
      "Yasin, on video from the sun deck, sunglasses on, very excited. Behind him Siri sits on a lounger reading "
      "something on her phone. She doesn't look excited at all.",
      [Z("yasin", "First Officer! Big one. Siri's management closed a deal. Nordic salmon, premium farms, huge "
                  "budget. You're the sustainability guy, so ten seconds on camera: this is the future of fish. Easy.",
         "excitement"),
       Z("siri", "Yasin, my dad fights those farms. On the island council, every single winter. Did you even read the "
                 "caption? I didn't write it. I never write them.", "sadness")],
      [O("“I don't put my name on fish farms. Not for anyone.”", [V("yasin", -6), V("siri", 4)]),
       O("Takes part, but keeps Siri out of the shot.", [V("yasin", 4), I("sat_data"), U("yasin_video", 1)],
         zeile=Z("yasin", "That's business, bro. And you get my satellite data pack, all week. Winners help winners.",
                 "pride")),
       O("“Siri, write your own caption. I'll check every word with you.”", [], probe=P("courage", 12),
         erfolg=[V("siri", 6), V("yasin", -8), U("siri_marke", 1)], fehlschlag=[V("yasin", -4)],
         zeile=Z("siri", "My own? …I don't think I've written one in six years. Okay. Okay, give me a minute. Sorry. "
                         "Give me ten.", "nervousness"))]),

    E("hy_megan_foto", "handy", "wholesome", "The Silver Tray", WANN((3, 4), TAG), ORT_DUC, H("megan", "eden_lobby"),
      "Megan, on video, in the lobby of the Eden Group. She holds a framed photograph at arm's length, as if it were "
      "evidence.",
      [Z("megan", "Marketing is making an anniversary book. They found this in the archive. A young stewardess with a "
                  "silver tray and a very unfortunate haircut. Guess.", "annoyance"),
       Z("megan", "I had a degree in naval architecture and a navigation certificate, and they gave me a tray. I "
                  "carried it for four years. I learned more about ships in the pantry than on the bridge. Don't repeat "
                  "that.", "pride")],
      [O("“Put it in the book. Big. Front page.”", [], probe=P("charm", 13), erfolg=[V("megan", 6), GAG("megan_lacht")],
         fehlschlag=[V("megan", -4)],
         zeile=Z("megan", "Front page. Of course you'd say that. …I'll consider page two.", "amusement")),
       O("“Does Chiara know?”", [V("megan", 4), F("megan_foto_chiara")],
         zeile=Z("megan", "Nobody on that boat knows, and that's how it stays. She'd be insufferable about it. She'd "
                          "also be right.", "caring")),
       O("“The haircut really is unfortunate.”", [V("megan", -2)],
         zeile=Z("megan", "It was a very windy year. Goodbye, First Officer.", "annoyance"))],
      sets={"megan": "Boardroom"}),

    E("hy_casanova_konfetti", "handy", "wholesome", "With Ceremony",
      WANN((3, 5), TAG, bed={"nicht": {"flag": "festa_eingeladen"}}), ORT_DUC, H("casanova", "village_piazza"),
      "Madame Casanova, on video from the piazza. Behind her stands a confetti cannon the size of a small car. She "
      "holds a remote in one hand and an envelope in the other.",
      [Z("casanova", "Monsieur! The Eden Rise is officially invited to the festa of Cala d'Orsu. And I want to do this "
                     "properly. With ceremony. Three. Two.", "excitement"),
       Z("casanova", "…It is not supposed to do that. It is not supposed to point at me. Monsieur, I need a moment. And "
                     "a broom.", "embarrassment"),
       Z("pascal", "I have the broom, Madame. I brought two. It went much better at eleven o'clock, Duc, you should have "
                   "seen it.", "amusement")],
      [O("“We accept. With ceremony.”", [V("casanova", 6), I("festa_invite"), F("festa_eingeladen")]),
       O("Applauds slowly. “Again, please. With the cannon facing the other way.”", [], probe=P("charm", 12),
         erfolg=[V("casanova", 6), I("festa_invite"), W("moral", 1), F("festa_eingeladen")],
         fehlschlag=[V("casanova", 2), I("festa_invite"), F("festa_eingeladen")],
         zeile=Z("casanova", "Again! Yes! THIS. IS. THE. FESTA! …Everybody duck.", "joy"))]),

    # ================================================================== Bordrat
    E("br_satellit_sonntag", "bordrat", "wholesome", "Forty Minutes", WANN((3, 6), N), "crew_mess",
      RAT("rosi", "lola", "jana"),
      "Rosi has worked it out on a napkin. With the power you have, the satellite link holds for about forty minutes "
      "tomorrow, and tomorrow is Sunday. Lola rings her Nan every Sunday. Jana rings her mum every Sunday. Both calls "
      "tend to run long.",
      [Z("rosi", "Forty minutes, Officer, not one more, or Unit-01 starts coughing. I'm not splitting it. You are.",
         "annoyance"),
       Z("lola", "Nan's ninety-one, Boss. If I don't ring, she rings the coast guard. She's done it before. Ask anyone "
                 "in my family, they still talk about it.", "nervousness"),
       Z("jana", "It's fine, Sir, honestly. I only tell Mama that everything is super. That takes two minutes. …Maybe "
                 "twenty. She asks a lot of questions.", "embarrassment")],
      [O("Gives the long call to Lola. “Ring your Nan. Jana, you'll have to keep yours short.”", [V("lola", 6), V("jana", -2), F("br_satellit")], von="lola"),
       O("“Take the long call, Jana, your mama has questions. Lola, keep yours short.”", [V("jana", 6), V("lola", -2), F("br_satellit")], von="jana"),
       O("Twenty minutes each, and he takes Unit-01 down to half load himself.", [F("br_satellit")], probe=P("cunning", 12, "handwerk"),
         erfolg=[V("lola", 4), V("jana", 4), V("rosi", 4), W("moral", 1)], fehlschlag=[V("rosi", -2)],
         zeile=Z("rosi", "Fine. Twenty and twenty. If Unit-01 so much as sneezes, I'm hanging up on both grannies.",
                 "amusement"), art="dritter_weg")],
      sets={"rosi": "Off Duty", "lola": "Off Duty", "jana": "jana_deck_a"}),

    E("br_jana_tender", "bordrat", "ernst", "Four Hundred Metres", WANN((2, 6), N), "tender_garage",
      RAT("toto", "jana", "chiara"),
      "For once Totò has a request that isn't about a crate. Jana wants to take the tender into the harbour "
      "tomorrow, alone, for the first time. Chiara says no before he has finished the sentence.",
      [Z("toto", "Comandante, the piccola ties a better bowline than me now. Don't tell anybody. One day she wants my "
                 "job, and I'm getting old, so let her start.", "pride"),
       Z("jana", "Only to the harbour and back, Sir. Four hundred metres. I've counted. I've counted them a lot, "
                 "actually.", "nervousness"),
       Z("chiara", "She's had her boat licence for six weeks. If she scratches the tender, it's my inventory. If she "
                   "scratches herself, it's my fault. No.", "disapproval")],
      [O("“Take the tender, Jana. Alone, to the harbour and back.”", [V("jana", 8), V("toto", 4), V("chiara", -4), F("jana_tender_solo")], von="jana"),
       O("Sides with Chiara. “Not yet, Jana. Six weeks is too short.”", [V("chiara", 6), V("jana", -4)], von="chiara"),
       O("Sits in the bow himself and keeps his hands in his pockets the whole way.", [], probe=P("courage", 12),
         erfolg=[V("jana", 6), V("chiara", 4), V("toto", 2), F("jana_tender_solo")], fehlschlag=[V("jana", 2)],
         zeile=Z("jana", "You didn't touch anything. Not once. Sir, did you see the docking? Did you see it?",
                 "excitement"), art="dritter_weg")],
      sets={"chiara": "Uniform", "jana": "jana_deck_a"}),

    E("br_holm_paket", "bordrat", "wholesome", "A Parcel for the Captain", WANN((3, 6), N), "crew_mess",
      RAT("siri", "lola", "chiara"),
      "Elsa's patrol boat runs to Ajaccio in the morning, and she has offered to take a parcel for the Captain. The "
      "mess table is covered in candidates. Siri has pushed a small envelope to the very edge, as if it might not "
      "count.",
      [Z("lola", "Thermos of coffee, Boss. Hot. Don't look at me like that. She pours it cold to look tough, but I've "
                 "seen her drink the hot one when she thinks the galley's empty.", "amusement"),
       Z("chiara", "She'll want the watch lists, because she always signs them. She'll want to sign them.", "pride"),
       Z("siri", "And this is, sorry, it's nothing. A card. I wrote two words on it in Norwegian. It's silly. She "
                 "might not even want it.", "embarrassment")],
      [O("Puts Lola's thermos of hot coffee on top of the parcel.", [V("lola", 6), V("holm", 4)], von="lola"),
       O("Puts Chiara's watch lists on top of the parcel. “She'll want to sign them.”", [V("chiara", 6), V("holm", 2)], von="chiara"),
       O("Puts Siri's card on top and asks her to sign it with her whole name.", [], probe=P("empathy", 11),
         erfolg=[V("siri", 8), V("holm", 6), W("moral", 1)], fehlschlag=[V("siri", 4)],
         zeile=Z("siri", "My whole name? Then she'll know it was me. …Okay. Okay, good. She should know.", "nervousness"),
         art="dritter_weg")],
      sets={"lola": "Galley", "chiara": "Uniform", "siri": "Morning Ritual"}),

    E("br_fish_pie", "bordrat", "wholesome", "Marie's Pie", WANN((2, 6), N), "galley",
      RAT("lola", "toto", "chiara"),
      "Petru has fixed the davit, two hinges and Lola's blender, and he won't take a cent. Lola wants to thank him with "
      "his favourite dish. Chiara has heard what his favourite dish is.",
      [Z("lola", "Fish pie, Boss, a proper one with mash on top, all crispy. He'll cry, in a good way, I reckon. Mostly the crust.", "excitement"),
       Z("toto", "Do it. A man alone eats standing at the sink. I know. Feed him sitting down.", "caring"),
       Z("chiara", "His wife made that pie for forty years. You don't walk into a widower's kitchen with his wife's "
                   "pie.", "disapproval")],
      [O("“Bake the fish pie, Lola. Petru should eat sitting down for once.”", [V("lola", 6), V("petru", 4), V("chiara", -2)], von="toto"),
       O("Sides with Chiara. “Not his wife's pie, Lola. Cook him something else.”", [V("chiara", 6), V("lola", -4)], von="chiara"),
       O("Walks down to the harbour and asks Petru himself, quietly.", [], probe=P("empathy", 12),
         erfolg=[V("petru", 8), V("lola", 4), V("chiara", 4), W("moral", 1), F("petru_rezept")],
         fehlschlag=[V("petru", 2)],
         zeile=Z("petru", "Hm. She put the bay leaf in the milk. Nobody knows that. …Now you know.", "caring"),
         art="dritter_weg"),
       O("Ship's rule: whoever helps us eats with us. Food is shared, not hoarded.", [REG("essen_geteilt"),
                                                                                    V("petru", 4), V("toto", -4)],
         art="bordregel")],
      sets={"lola": "Galley", "chiara": "Service"}),

    E("br_toto_stand", "bordrat", "wholesome", "A Stamp for Totò", WANN((3, 6), N), "crew_mess",
      RAT("toto", "lola", "chiara"),
      "Totò stands at the head of the mess table with a form from the town hall. A market stall on the quay, all "
      "legal. He has filled in every box but one: the yacht has to agree. Lola has already promised him a crate of "
      "chilli jam and two bottles of Alva's myrtle liqueur.",
      [Z("toto", "Comandante, in Napoli my whole family sells things. Nobody ever sold anything with a stamp. I want a "
                 "stamp. One table, market day, Lola's jars, Rosi's radios. Nothing from a truck.", "nervousness"),
       Z("lola", "People queue for my chilli jam, Boss! Well. Totò queues. But he'd be queueing in public.", "excitement"),
       Z("chiara", "The Eden Rise is not a flea market. If a guest sees our bosun selling liqueur on the quay, it's in a "
                   "review by lunch.", "disapproval")],
      [O("Signs the form for Totò. “One table, on market day.”", [V("toto", 8), V("lola", 4), V("chiara", -4), F("toto_stand")], von="lola"),
       O("Pushes the form back. “Not under the yacht's name, Totò.”", [V("chiara", 6), V("toto", -4)], von="chiara"),
       O("Signs it for Eden Consulting, not for the Eden Rise.", [], probe=P("cunning", 12),
         erfolg=[V("toto", 6), V("chiara", 4), W("ruf", 1), F("toto_stand")], fehlschlag=[V("toto", 2)],
         zeile=Z("toto", "A stamp. A real one, with a name on it. Madonna, Comandante. My mother will think I'm in "
                         "trouble.", "joy"), art="dritter_weg"),
       O("Ship's rule: no alcohol on deck. The stall sells jam, not liqueur.", [REG("kein_alkohol_deck"), V("toto", 2),
                                                                              V("chiara", 2)], art="bordregel")],
      sets={"lola": "Off Duty", "chiara": "Uniform"}),

    E("br_handtuecher", "bordrat", "witzig", "Jenna", WANN((3, 6), N), "crew_mess",
      RAT("chiara", "jana", "siri"),
      "Chiara has called a short meeting. The subject: since Antibes, Jana has been carrying Siri's towels, sun cream "
      "and water bottle around. Nobody asked her to. Siri still calls her Jenna.",
      [Z("chiara", "She's crew. Crew are not a guest's personal assistant. If she carries one more towel for Siri "
                   "instead of coiling lines, I'm laminating a sign.", "annoyance"),
       Z("jana", "I don't mind, Sir! Honestly. I've followed her since I was sixteen. It's like carrying towels for a "
                 "lighthouse.", "nervousness"),
       Z("siri", "I never asked her, I promise. Sorry, Jenna. Jana! Jana. Sorry. I'm so bad with names, it's not you, "
                 "it's my whole brain.", "embarrassment")],
      [O("“Jana can carry what she likes, Chiara. It's her choice.”", [V("jana", 6), V("siri", 2), V("chiara", -4)], von="jana"),
       O("“Chiara's right, Jana. Crew is crew, so no more towels for Siri.”", [V("chiara", 6), V("jana", -4)], von="chiara"),
       O("“Siri, tomorrow you coil one of Jana's lines. Then you're even.”", [], probe=P("charm", 12),
         erfolg=[V("jana", 6), V("siri", 6), V("chiara", 2), W("moral", 1)], fehlschlag=[V("siri", -2)],
         zeile=Z("siri", "Me? A rope? …Okay. Yes. Jana, show me. I'll learn the knot and your name, both.", "joy"),
         von="siri", art="dritter_weg")],
      sets={"chiara": "Uniform", "jana": "jana_deck_a", "siri": "Riviera Swim"}),

    # ================================================================== Gags mit einer Figur
    E("g1_alva_tim_tams", "gag1", "witzig", "Contraband from Sydney",
      WANN((3, 6), ["tag", "abend"], bed={"wert": ["vertrauen.alva", ">=", 2]}), "swim_platform",
      P1("alva", ("lola", "+", "recognises the box from ten metres"), ("chiara", "-", "has smelled the jar")),
      "Alva comes alongside in a borrowed dinghy with a cardboard box on her lap. It has come from Australia, by three "
      "ferries and a cousin. Lola recognises it from ten metres and makes a sound you have never heard a person make.",
      [Z("alva", "Tim Tams, two packets. And one jar of the black stuff, which I refuse to name. Your cook has been "
                 "ordering it through my bar for weeks. Alva remembers who drinks her coffee.", "amusement"),
       Z("lola", "Vegemite! Boss, real Vegemite! I'm going to cry, I'm already crying. Mostly the Tim Tams.", "joy"),
       Z("chiara", "That smells like a ship's engine, and it's going in my galley fridge?", "disgust")],
      [O("Helps Alva aboard and carries the box himself.", [V("alva", 6), B("alva", 4), V("lola", 4)]),
       O("Lets Lola teach him the Tim Tam slam, right there on the platform.", [V("lola", 6), B("lola", 4),
                                                                              W("moral", 1)],
         zeile=Z("lola", "Bite both ends, suck the coffee through, and then you've got about two seconds before – yes! "
                         "Yes! He's one of us now!", "excitement")),
       O("Finds the jar a shelf of its own, far away from Chiara.", [V("chiara", 4), V("lola", 2)],
         zeile=Z("chiara", "Bottom shelf, behind the fish sauce, with the lid taped. Merci.", "approval"))],
      sets={"alva": "alva_standard", "lola": "Off Duty", "chiara": "Uniform"}),

    E("g1_lea_nachttauchen", "gag1", "ernst", "Six Metres", WANN((2, 6), N, bed={"wert": ["vertrauen.lea", ">=", 2]}),
      "swim_platform",
      P1("lea", ("elsa", "-", "holds the searchlight"), ("toto", "?", "is smoking where he shouldn't")),
      "Past midnight a searchlight sweeps across the swim platform. Elsa's patrol boat idles twenty metres off. In "
      "the beam, a single snorkel. Lea surfaces, sees the light, and salutes.",
      [Z("elsa", "First Officer. Your deckhand is diving alone, at night, without a dive computer. I'm not writing "
                 "that down. I'm telling you, so that I never have to write it down.", "disapproval"),
       Z("lea", "Only six metres! There were squid, Duc. Proper glowing ones, the little ones that only come up at "
                "night – okay. I can hear it. I'm coming out.", "embarrassment")],
      [O("“Out. Now. We'll talk in the morning.”", [V("elsa", 6), V("lea", -2)]),
       O("Kicks off his shoes. “Next time, wake me. I'll hold the torch.”", [V("lea", 6), B("lea", 4), NK("lea"), F("lea_weck_mich"),
                                                                           V("elsa", 2)],
         zeile=Z("lea", "You'd come? At night? …Okay. Deal. I'll knock. Quietly. I'm very good at quiet.", "joy")),
       O("“Lieutenant, would you check her gear once a week?”", [V("elsa", 4), V("lea", 2), W("moral", 1)],
         zeile=Z("elsa", "Once a week. I'll bring figs. And TOTÒ, I can see your cigarette from here.", "amusement"))],
      sets={"lea": "Dive"}, knistern=True),

    E("g1_sophia_zweitbesetzung", "gag1", "wholesome", "The Understudy", WANN((2, 6), ["dinner"]), "aft_deck",
      P1("sophia", ("lea", "+", "started it"), ("lola", "+", "wants a song"), ("rosi", "?", "has never been to a theatre")),
      "Dinner on the aft deck. Lea mentions, very casually, that her sister spent two years in the West End. Every "
      "head turns. Sophia keeps buttering her bread as if nobody had spoken.",
      [Z("lea", "Two years! Understudy for the lead. She knew every single line. I used to test her on the train "
                "home.", "pride"),
       Z("sophia", "Darling, an understudy learns every line and then catches the last train home. Two years. Not one "
                   "night on stage. Pass the salt, would you.", "neutral")],
      [O("“One line. Just one. For us.”", [], probe=P("charm", 13), erfolg=[V("sophia", 6), B("sophia", 4), W("moral", 1)],
         fehlschlag=[V("sophia", -2)],
         zeile=Z("sophia", "…The last train has gone, and I find I don't mind at all. There. Act two. Nobody ever heard "
                           "it. Now you have.", "caring")),
       O("Changes the subject before anyone can ask again.", [V("sophia", 6), V("lea", -2)],
         zeile=Z("sophia", "Thank you. …You're dangerous, you know. You notice things.", "gratitude")),
       O("“Two years and never once on? That's rough.”", [V("sophia", -4)],
         zeile=Z("sophia", "Isn't it. Salt, darling.", "annoyance"))],
      sets={"sophia": "Concierge", "lea": "Off Duty", "rosi": "Off Duty"}),

    E("g1_petru_netze", "gag1", "ernst", "The Most Mended Net in Corsica", WANN((2, 6), ["tag", "abend"], an_land=True),
      "petru_workshop",
      P1("petru", ("toto", "?", "whispers"), ("lea", "?", "watches from the quay")),
      "Late afternoon at Petru's workshop. The radio is playing Corsican football. Petru is mending a net. You can't "
      "see a single hole in it. He has been mending it since you arrived.",
      [Z("toto", "Comandante, don't say anything. That net is perfect. He mends it every afternoon, since Marie. Five "
                 "years. It's the most mended net in Corsica.", "sadness"),
       Z("petru", "Hm. The sea doesn't hurry.", "neutral")],
      [O("Sits down beside him and takes the other end of the net.", [V("petru", 8), W("moral", 1)],
         zeile=Z("petru", "Hm. Not like that. …Like that. Yes.", "approval")),
       O("“Petru, there's no hole in that net.”", [V("petru", -2), V("toto", 2)],
         zeile=Z("petru", "No. Not in the net.", "sadness")),
       O("Fetches two coffees from Alva's and says nothing at all.", [V("petru", 6), V("toto", 4)])],
      sets={"lea": "Off Duty"}),

    E("g1_lola_strandkueche", "gag1", "wholesome", "The Napkin Kitchen", WANN((2, 6), ["fruehstueck"]), "foredeck",
      P1("lola", ("chiara", "-", "is waiting for breakfast"), ("rosi", "+", "wants to know about the wiring")),
      "Early morning on the foredeck. Lola sits cross-legged with a coffee and a napkin, drawing. A shack, a counter, "
      "a sign. She hides it when she sees you, then decides not to.",
      [Z("lola", "Don't laugh, it's a kitchen on a beach. Four stools, one stove and no head chef, and nobody yells. If somebody yells, they're out.", "nervousness"),
       Z("lola", "Got a name and everything. Well, half a name. I keep crossing it out.", "embarrassment")],
      [O("Takes her pen and draws a fifth stool.", [V("lola", 6), B("lola", 6)],
         zeile=Z("lola", "That one's a bit close to the stove, Boss. …I'll move it. Just for you.", "joy")),
       O("“Where's the steamer for the bao?”", [], probe=P("perception", 12, "kueche"),
         erfolg=[V("lola", 8), W("moral", 1)], fehlschlag=[V("lola", 4)],
         zeile=Z("lola", "You'd know about the steamer. Right here, next to the stove. Nobody's ever asked about the "
                         "steamer.", "love")),
       O("“Nice. Shouldn't breakfast be on by now?”", [V("lola", -2), V("chiara", 2), W("moral", -1)])],
      sets={"lola": "Off Duty", "chiara": "Uniform", "rosi": "Off Duty"}),

    E("g1_lola_delfin", "gag1", "frech", "Gerald", WANN((2, 6), ["abend"]), "crew_mess",
      P1("lola", ("lea", "-", "turns red"), ("rosi", "+", "takes notes")),
      "Evening in the crew mess. Lola puts a warm plate in front of Lea, who has just come up from a dive. Then she "
      "announces her theory to the whole table.",
      [Z("lola", "Every evening, same dolphin, same spot off the point, and she comes back all pink and smiley. I'm not "
                 "saying it's love. I'm saying I've seen less obvious on Bondi Beach.", "amusement"),
       Z("lea", "He's a bottlenose! He's a research subject! You can't fall in love with a research subject, that's "
                "the first rule of marine biology!", "embarrassment"),
       Z("rosi", "What's his name?", "curiosity"),
       Z("lea", "…Gerald. Shut up. All of you.", "embarrassment")],
      [O("Backs Lola's theory with a straight face.", [V("lola", 6), B("lola", 4), V("lea", -2)]),
       O("“Lea is the only one on this boat doing actual science.”", [V("lea", 6), B("lea", 4), V("lola", -2)]),
       O("Asks Lea to introduce him to Gerald tomorrow.", [], probe=P("cunning", 12),
         erfolg=[V("lea", 6), V("lola", 4), W("moral", 1)], fehlschlag=[V("lea", 2)],
         zeile=Z("lea", "You want to meet Gerald? …He's very shy. Bring a fish. A fresh one, he's got standards.",
                 "joy"))],
      sets={"lola": "Off Duty", "lea": "Off Duty", "rosi": "Off Duty"}),

    E("yk_hana", "gag1", "wholesome", "Hana Asks About the Birds", WANN((3, 5), TAG, bed=nach(YK, 2)), "foredeck",
      P1("yamamoto", ("maxwell", "?", "is in every photo"), ("jana", "?", "polishes the railing in the background")),
      "Yamamoto is on the foredeck with a tablet at arm's length. His daughter Hana is on video from Tokyo, and she "
      "has asked to see his bird photographs. He is scrolling very, very slowly.",
      [Z("yamamoto", "Hana-chan, this is a seagull. A very rare seagull. …Yes. It does look like a large man. The "
                     "light was difficult.", "embarrassment"),
       Z("yamamoto", "Officer-san. Please. My daughter booked this voyage because my heart made a small complaint. If "
                     "she thinks I only follow Maxwell-san with a camera, she will book another one. Help me.",
         "nervousness")],
      [O("Takes the tablet and tells Hana her father has made a lot of friends on board.",
         [V("yamamoto", 6), V("maxwell", 2), GAG(YK)]),
       O("Waves Maxwell over to say hello.", [V("maxwell", 6), V("yamamoto", -2), GAG(YK)],
         zeile=Z("maxwell", "Howzit, Hana! Mr. Maximum is the bird! Mr. Maximum is a very rare bird!", "joy")),
       O("Points the tablet at the sky, just as a cormorant flies past.", [], probe=P("perception", 12),
         erfolg=[V("yamamoto", 8), W("moral", 1), GAG(YK)], fehlschlag=[V("yamamoto", 2), GAG(YK)])],
      gag=YK, sets={"yamamoto": Y_HAWAII, "maxwell": M_STEWARD, "jana": J_DECK}),

    # ================================================================== Versus
    E("gv_elsa_roman", "gagv", "frech", "The Captain's Forbidden Treasure", WANN((2, 6), ["tag", "abend"], an_land=True),
      "village_harbour", PV("elsa", "toto", "lola", "jana"),
      "Elsa's patrol jacket lies on a bollard. Next to it, face down, a paperback with a shirtless pirate on the "
      "cover. Totò has seen it. Elsa has seen Totò see it.",
      [Z("toto", "Comandante, look. The law of Cala d'Orsu reads The Captain's Forbidden Treasure. Chapter twelve. I "
                 "am a witness. I am a free man now.", "amusement"),
       Z("elsa", "That's evidence. I confiscated it from a tourist. This morning. Totò, if that photo goes anywhere, "
                 "you get a ticket for every crate in your locker, and I have counted them.", "embarrassment")],
      [O("Picks up the book and reads the back cover aloud.", [V("toto", 6), V("elsa", -4)], von="toto",
         zeile=Z("elsa", "Chapter twelve is the good one, for the record. TOTÒ, PUT THE PHONE AWAY.", "annoyance")),
       O("Hands it back with a straight face. “Confiscated evidence, Lieutenant. Very dangerous.”",
         [V("elsa", 6), V("toto", -2)], von="elsa",
         zeile=Z("elsa", "Thank you, First Officer. I'll file it under pending, for a while.", "gratitude")),
       O("“I've got one like that too. Mine has a lighthouse keeper.”", [], probe=P("empathy", 12),
         erfolg=[V("elsa", 8), V("toto", 2), W("moral", 1)], fehlschlag=[V("elsa", 2)],
         zeile=Z("elsa", "A lighthouse keeper. …Does he brood? He has to brood. Never mind, I'm not asking. Lend it to "
                         "me.", "curiosity"))],
      sets={"lola": "Off Duty", "jana": "jana_deck_a"}),

    E("gv_unit01_bild", "gagv", "wholesome", "Portrait of a Lady", WANN((2, 6), TAG), "generator_room",
      PV("lea", "rosi", "siri", "lola"),
      "Lea is sitting cross-legged in front of Unit-01 with her sketchbook, drawing. The old generator has a face now, "
      "and tentacles. Rosi has just seen the tentacles.",
      [Z("lea", "Look, she's got a face! The intake's the mouth and the exhaust is, okay, I gave her tentacles. Sea "
                "monsters need tentacles. That's basically biology.", "excitement"),
       Z("rosi", "She is not a monster. She's thirty-one years old, she's survived two owners and one explosion, and she "
                 "has never once had tentacles. Draw her properly or don't draw her.", "annoyance")],
      [O("“The tentacles stay.”", [V("lea", 6), V("rosi", -4), F("lea_rosi_streit")], von="lea"),
       O("“Rosi's right. No tentacles.”", [V("rosi", 6), V("lea", -4), F("lea_rosi_streit")], von="rosi"),
       O("“Draw her as a sea monster that guards the ship.”", [], probe=P("empathy", 12),
         erfolg=[V("lea", 4), V("rosi", 4), B("lea", 2), B("rosi", 2), W("moral", 1)], fehlschlag=[W("moral", 1)],
         zeile=Z("rosi", "A guardian. With tentacles. Fine. Give her the amber eye and I'll hang it in the workshop "
                         "when it's rebuilt. Don't tell anyone I said that.", "pride"))],
      sets={"lea": "Off Duty", "rosi": "Engine Room", "siri": "Morning Ritual", "lola": "Off Duty"}),

    E("gv_rotes_kleid", "gagv", "frech", "The Red Dress", WANN((21, 21), ["abend"]), "village_piazza",
      PV("jana", "chiara", "lola", "rosi", "maxwell"),
      "The festa is in full swing when Jana steps onto the piazza in a red dress. It fits her almost perfectly. It's "
      "Chiara's. Chiara is standing right next to you, holding a glass of wine very, very still.",
      [Z("jana", "Sir! Do I look – sorry. Hello. I didn't ask. I was going to ask. Then it was eight o'clock and the "
                 "dress was just hanging there, looking at me.", "nervousness"),
       Z("chiara", "That's my dress. That's my dress, and she's doing my walk. Duc. She's doing my walk.", "surprise")],
      [O("“It suits her, Chiara. Let her have tonight.”", [V("jana", 6), V("chiara", -4)], von="jana"),
       O("“Jana. Back to the boat, change, then come back and dance.”", [V("chiara", 6), V("jana", -4)], von="chiara"),
       O("Raises his glass to both of them. “Two women in red. Cala d'Orsu won't survive it.”", [],
         probe=P("charm", 13), erfolg=[V("chiara", 4), V("jana", 4), W("moral", 1)], fehlschlag=[V("chiara", -2)],
         zeile=Z("chiara", "…Fine. She keeps the dress for tonight. But she gives back the walk.", "amusement"))],
      sets={"jana": "pencil_shortsleeves_red", "chiara": "Harbor Night", "lola": "Off Duty", "rosi": "Festa",
            "maxwell": "maximum_party_b"}),

    E("gv_holm_baer", "gagv", "witzig", "One Kilometre, One Shot", WANN((2, 6), TAG), "foredeck",
      PV("toto", "maxwell", "jana", "lea"),
      "There's a bet on the foredeck. The stake is a week of washing up. The subject is the Captain. Years ago, so "
      "the story goes, up north: a bear, one kilometre, one shot.",
      [Z("toto", "One shot, Comandante. One kilometre. The Capitana told it to a harbour master in Monaco, he told my "
                 "cousin, and my cousin never lies about bears.", "excitement"),
       Z("maxwell", "Eish, brother. Mr. Maximum respects the Captain. Mr. Maximum also respects physics. One kilometre "
                    "is very far for a bear, and very far for a bullet.", "confusion")],
      [O("Bets with Totò: she made that shot.", [V("toto", 6), V("maxwell", -2)], von="toto"),
       O("Bets with Maxwell: nobody makes that shot.", [V("maxwell", 6), V("toto", -2)], von="maxwell"),
       O("“Ask yourselves why she never tells it herself.”", [], probe=P("perception", 12),
         erfolg=[V("maxwell", 4), V("toto", 4), W("moral", 1), F("holm_baer_frage")], fehlschlag=[W("moral", 1)],
         zeile=Z("jana", "Maybe because it was two kilometres. Sorry. I'm only saying. She's very modest.",
                 "amusement"))],
      sets={"maxwell": "maximum_steward_a", "jana": "jana_deck_a", "lea": "Deck"}),

    E("gv_chiara_italienisch", "gagv", "frech", "Olivetti", WANN((3, 6), ["abend"], an_land=True,
      bed={"wert": ["vertrauen.alva", ">=", 2]}), "alvas_bar", PV("chiara", "alva", "lola", "toto"),
      "Chiara has decided to order in Italian tonight. Loudly and proudly. Alva has decided to answer only in "
      "Corsican. The whole bar is listening.",
      [Z("chiara", "Buonasera! Vorrei un bicchiere di vino rosso, per favore, and also – how do you say olives? Olivas. "
                   "Olivetti!", "pride"),
       Z("alva", "Olivetti is a typewriter, cara. You've just ordered a glass of red and a typewriter. I could help. "
                 "I'm enjoying this far too much to help.", "amusement")],
      [O("“She wants olives, Alva. A lot of olives.”", [V("chiara", 6), V("alva", -2)], von="chiara"),
       O("“I'll take a typewriter too, Alva.”", [V("alva", 6), B("alva", 2), V("chiara", -4)], von="alva"),
       O("Orders the next round in French, just as badly.", [], probe=P("charm", 12),
         erfolg=[V("chiara", 6), V("alva", 4), B("chiara", 2), W("moral", 1)], fehlschlag=[V("chiara", 2), W("moral", 1)],
         zeile=Z("lola", "Oh no. There's two of them now. Somebody call the language police.", "joy"))],
      sets={"chiara": "Harbor Night", "alva": "alva_standard", "lola": "Off Duty"}),

    E("gv_tuersteher", "gagv", "frech", "After Closing", WANN((3, 6), ["abend"], an_land=True), "alvas_bar",
      PV("maxwell", "yasin", "alva", "toto"),
      "Closing time at Alva's. Yasin wants one more shot inside, golden hour but at night. Alva has said no. Maxwell "
      "has quietly taken up position in the doorway with his arms folded. He is exactly as wide as the door.",
      [Z("yasin", "Bro. Bro, one minute. Thirty seconds. Do you know who I am? Four hundred thousand followers.",
         "annoyance"),
       Z("maxwell", "Mr. Maximum stood at the door of the loudest club in Cape Town for six years, my friend. Mr. "
                    "Maximum has met four hundred thousand people. Not one of them got in after closing.", "pride")],
      [O("Stands next to Maxwell. “Closing time, Yasin.”", [V("maxwell", 6), V("alva", 4), V("yasin", -4)], von="maxwell"),
       O("Backs Yasin: one shot, then out.", [V("yasin", 6), V("alva", -4), U("yasin_video", 1)], von="yasin"),
       O("“Yasin, film the door. Turned away by the strongest man in Corsica. That's content.”", [],
         probe=P("cunning", 12), erfolg=[V("yasin", 4), V("maxwell", 4), W("moral", 1)], fehlschlag=[V("yasin", -2)],
         zeile=Z("maxwell", "Mr. Maximum approves of this content. Mr. Maximum would like his left side, please.",
                 "joy"))],
      sets={"maxwell": "maximum_party_b", "alva": "alva_standard"}),

    E("gv_kaffee_rosi", "gagv", "witzig", "Seven O'Clock Coffee", WANN((2, 6), ["fruehstueck"]), "power_room",
      PV("siri", "rosi", "lea", "lola"),
      "Seven in the morning. For the third day running Siri knocks at the power room with a coffee for Rosi. For the "
      "third day running Rosi pretends she doesn't drink coffee.",
      [Z("siri", "Sorry, it's me again. Sorry. Oat milk, one sugar, I asked Lola. You said I was useless, so I thought, "
                 "okay, then I'll be useful at seven.", "nervousness"),
       Z("rosi", "I said useless on day one. Day one doesn't count, everybody's useless on day one. I don't need a "
                 "coffee. …Is that cardamom?", "embarrassment")],
      [O("“Take the coffee, Rosi.”", [V("siri", 6), V("rosi", -2)], von="siri"),
       O("“Rosi drinks it when she wants to.”", [V("rosi", 6), V("siri", -2)], von="rosi"),
       O("Takes the cup, sips, and hands it to Rosi. “Not poisoned. Good, actually.”", [], probe=P("empathy", 12),
         erfolg=[V("siri", 4), V("rosi", 4), W("moral", 1)], fehlschlag=[W("moral", 1)],
         zeile=Z("rosi", "Fine. Fine! Tomorrow, same time. Not because I like it, but because the generator likes it when I'm awake.", "joy"))],
      sets={"siri": "Morning Ritual", "rosi": "Engine Room", "lea": "Deck", "lola": "Galley"}),

    E("gv_seestueck", "gagv", "wholesome", "A Sky in Four Tries", WANN((2, 6), TAG), "crew_mess",
      PV("lea", "sophia", "lola", "siri"),
      "A parcel from Falmouth has made it all the way to Cala d'Orsu. Inside, wrapped in a Cornish newspaper, is a "
      "small seascape: a grey harbour, a red boat, a sky that took four tries. Their mother painted it. Lea wants it on "
      "the wall of the mess. Sophia wants it in a drawer.",
      [Z("lea", "It's Falmouth! That's Grandad's boat, the red one, see? Mum did it from memory. It belongs where "
                "everyone can see it, proper.", "excitement"),
       Z("sophia", "Mum painted that instead of paying the electricity, darling. Twice. I'll keep it safe. Somewhere "
                   "dark, where it can't cost anyone anything.", "sadness")],
      [O("“It goes on the wall.”", [V("lea", 6), V("sophia", -4)], von="lea"),
       O("“It goes in Sophia's drawer.”", [V("sophia", 6), V("lea", -4)], von="sophia"),
       O("“On the wall, but Sophia picks the spot.”", [], probe=P("empathy", 13),
         erfolg=[V("sophia", 6), V("lea", 6), W("moral", 1)], fehlschlag=[V("lea", 2), V("sophia", 2)],
         zeile=Z("sophia", "By the door, then. Where you see it last, not first. …It's a good sky. She always got the "
                           "sky right.", "caring"))],
      sets={"lea": "Off Duty", "sophia": "Concierge", "lola": "Galley", "siri": "Morning Ritual"}),
]
