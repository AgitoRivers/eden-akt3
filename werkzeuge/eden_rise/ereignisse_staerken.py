# -*- coding: utf-8 -*-
"""Ducs Staerken (17.10.2026, Duc: ESG-Berater mit Koepfchen, Kueche, Charme und Handwerk; Geheimnis = Angebot fuer eine
Management-Position auf Europa-Ebene, alle glauben, er bleibt auf See).

13 Events: 7 Duelle (Duc gegen eine Person, die Crew schaut zu), 1 Bordrat, 1 Gag mehrerer, 3 Auftritte, 2 Anrufe aus
(Das Koeln-Jobangebot wurde am 25.10.2026 gestrichen, Duc: passt nicht zum Founder im Sabbatical.)
Die Missionen dazu stehen in missionen_eden_rise.py.

Balance (Check 17.10.2026): Proben mit Persona-Vorteil haben SG 13-15 (sonst fast sicher), Belohnungen wie die
uebrigen Events (+4/+6, Erlebnis +8 nur bei echten Momenten); die Auswahl staerkt die bisher seltenen Figuren
Sophia, Siri, Petru, Elsa und Yasin. Kein Event beruehrt die Faelle; "Woher du kommst" erfindet nichts ueber Ducs
Familie - Duc erzaehlt selbst (szene_gespraech, keine Probe)."""
from ereignisse_basis import *  # noqa: F401,F403


def DU(gegner, staerke, *zuschauer):
    return {"gegner": gegner, "staerke": staerke, "zuschauer": list(zuschauer)}


def AUF(staerke, *publikum, partner=None):
    p = {"staerke": staerke, "publikum": list(publikum)}
    if partner:
        p["partner"] = partner
    return p


TAG, ABEND = ["tag"], ["abend"]
EVENTS = [
    # ------------------------------------------------------------------ Kueche
    E("du_koch_lola", "duell", "witzig", "Cook-Off: The Galley", WANN((2, 6), ["tag", "dinner"]), "galley",
      DU("lola", "kueche", "chiara", "rosi", "toto", "lea"),
      "Lola has heard that you can cook. Now she's standing in front of the stove with her arms folded. Two burners, "
      "one hour, the crew as the jury. Lola already has a spoon in her hand and is pointing it at you.",
      [Z("lola", "Right. My galley, my rules. One hour, one plate each, the crew votes. Loser does the dishes for a "
                 "week.", "excitement"),
       Z("toto", "I put twenty euros on the Comandante. Don't look at me like that, Lola, it's business.", "amusement"),
       Z("lola", "Boss, I once made a whole dinner party out of a tin of beans and a lime. Bring it.", "pride")],
      [O("Cooks his best dish, and cooks to win.", [], probe=P("perception", 14, "kueche"),
         erfolg=[V("lola", 6), W("moral", 1), KL("duc", "toto", "Duc beat Lola in her own galley")],
         fehlschlag=[V("lola", 4), W("energie", -1)],
         zeile=Z("lola", "Okay. OKAY. That's annoyingly good, so rematch tomorrow, and you're still doing the dishes.", "surprise")),
       O("“Let's cook one dish together.”", [V("lola", 6), B("lola", 4), I("lolas_gewuerz")],
         zeile=Z("lola", "Together? That's not a showdown, that's a date with knives. I love it.", "joy")),
       O("Lets her win.", [V("lola", 4), W("moral", 1)],
         zeile=Z("lola", "You let me win, I saw that. I'm keeping the trophy anyway.", "amusement"))],
      sets={"lola": "Galley", "chiara": "Service", "rosi": "Engine Room", "lea": "Deck"}),

    E("du_koch_alva", "duell", "witzig", "Cook-Off: Corsica vs. Saigon", WANN((3, 6), ABEND, an_land=True), "alvas_bar",
      DU("alva", "kueche", "petru", "casanova", "sophia", "toto"),
      "Alva has pushed the tables together. On one side stand her fiadone and her wild boar pâté, on the other your "
      "street kitchen of two camping stoves. Half the village is here. Madame Casanova has brought a microphone.",
      [Z("casanova", "Mesdames et messieurs! Corsica against Saigon! Forty years of tradition against one handsome sailor!", "excitement"),
       Z("alva", "In this bar, o figliolu, the food is older than your country's flag. Cook. Impress me.", "pride"),
       Z("petru", "Hm.", "neutral")],
      [O("Puts his thịt kho up against her pâté.", [], probe=P("perception", 15, "kueche"),
         erfolg=[V("alva", 6), W("ruf", 1), V("petru", 4), KL("duc", "casanova", "The First Officer beat Alva at cooking")],
         fehlschlag=[V("alva", 4), W("ruf", 1)],
         zeile=Z("alva", "Sweet pork and eggs, like a grandmother made it. Which grandmother, eh? You'll tell me one day.", "admiration")),
       O("Puts both dishes on one plate, half Corsican and half Vietnamese.", [], probe=P("cunning", 13, "kueche"),
         erfolg=[V("alva", 6), B("alva", 4), W("ruf", 1)], fehlschlag=[W("moral", 1), KL("duc", "toto", "Duc's fusion cooking confused the "
                                                                                                        "village")],
         zeile=Z("alva", "Brocciu with fish sauce. I hate that I like it. Don't tell my grandmother. She's in "
                         "Seville and she'd still find out.", "amusement")),
       O("Lets the village decide who wins.", [W("ruf", 1), V("casanova", 4)],
         zeile=Z("casanova", "Democracy! The village votes for everyone! Nobody loses, everybody eats, and I give a "
                             "speech!", "joy"))],
      sets={"alva": "alva_standard", "sophia": "Shore Leave"}),

    E("du_koch_toto", "duell", "witzig", "Cook-Off: Ragù vs. Thịt Kho", WANN((2, 6), ["dinner", "abend"]), "crew_mess",
      DU("toto", "kueche", "rosi", "yasin", "siri", "lola"),
      "Totò has a pot of ragù on that has been simmering for six hours. He claims the recipe is older than Naples "
      "itself. You have a clay pot of caramelised pork belly. Rosi is handing out forks like weapons.",
      [Z("toto", "Comandante, this is my nonna's ragù, six hours on the fire. If you lose, you say on camera that Napoli is the centre of the world.", "pride"),
       Z("rosi", "And if the Officer wins, you say Sicily is better than Napoli, on camera. Yasin, film it.", "amusement"),
       Z("yasin", "Already rolling. This is going to do numbers.", "excitement")],
      [O("Sets his thịt kho down next to Totò's ragù. “Forks ready, Rosi.”", [], probe=P("perception", 14, "kueche"),
         erfolg=[V("toto", 6), V("rosi", 4), V("yasin", 4), GAG("toto_cousin")],
         fehlschlag=[V("toto", 4), W("moral", 1)],
         zeile=Z("toto", "Caramel and pork and egg. Madonna. My nonna would have married you. Don't tell Rosi I said Sicily.", "admiration")),
       O("“Let's swap recipes.”", [V("toto", 6), I("frischer_fang")],
         zeile=Z("toto", "A recipe swap? You know what that's worth in Naples? Everything. Here's my cousin's fish, fresh. Don't ask.", "gratitude")),
       O("Gives him the win and praises Naples.", [V("toto", 4), V("rosi", -4)],
         zeile=Z("rosi", "Traitor. You'll sleep in the engine room with Unit-01.", "annoyance"))],
      sets={"rosi": "Off Duty", "siri": "Silver Night", "lola": "Off Duty"}),

    E("br_lola_flach", "bordrat", "wholesome", "Lola's Down: You Cook for Thirteen", WANN((2, 6), ["nacht"]), "crew_mess",
      {"sprecher": "chiara", "links": "rosi", "rechts": "sophia"},
      "Lola ate a bad mussel and is lying green in her bunk. Tomorrow thirteen people need feeding. Chiara is "
      "staring at the empty meal plan. Rosi wants tins and to save power. Sophia wants it to look like a yacht "
      "anyway.",
      [Z("chiara", "Lola is out. Thirteen people, one galley, zero cooks. Somebody has to stand at that stove tomorrow.", "nervousness"),
       Z("rosi", "Cold tins, and that's all. No oven and no hotplate marathon, because every kilowatt goes to the batteries and not to a soufflé.", "annoyance"),
       Z("sophia", "If the guests eat beans out of a tin, they'll talk about it for a year. One proper meal, "
                   "darling. That's all I ask.", "caring")],
      [O("“Rosi's right. Cold tins tomorrow, and we save the power.”", [V("rosi", 4), V("sophia", -2)], von="rosi"),
       O("Sides with Sophia. “One proper meal. I'll cook it.”", [], probe=P("perception", 13, "kueche"), von="sophia",
         erfolg=[W("moral", 1), V("sophia", 4), R(1)], fehlschlag=[W("moral", -1)]),
       O("A third way: bún riêu in one big pot. One course, little power.", [], probe=P("cunning", 14, "kueche"),
         erfolg=[W("moral", 1), V("rosi", 4), V("sophia", 4), V("lola", 4), R(1)], fehlschlag=[W("moral", -1)], art="dritter_weg",
         zeile=Z("chiara", "One pot for thirteen. If that works, I'll write it on the whiteboard in gold.", "optimism")),
       O("Promise: tomorrow Lola gets the first bowl of soup, in bed.",
         [VER("lola", "Duc bringt Lola Suppe ans Bett", 1, {"flag": "lola_suppe"}), V("lola", 4)], art="versprechen")],
      sets={"chiara": "Uniform", "rosi": "Off Duty", "sophia": "Concierge"}),

    # ------------------------------------------------------------------ Handwerk
    E("du_reparatur_rosi", "duell", "witzig", "Repair Duel: Lola's Blender",
      WANN((8, 14), TAG, bed={"flag": "werkstatt_offen"}), "workshop",            # erst nach der Wiedereroeffnung (E-065)
      DU("rosi", "handwerk", "lola", "lea", "toto"),
      "Lola's blender is dead. Rosi has cleared two workbenches and set up a stopwatch. Whoever gets it running "
      "first gets the first glass of Lola's mango smoothie. Lola is standing by with a glass as if it were a trophy.",
      [Z("rosi", "One blender, two engineers, one stopwatch. If you beat me in my own workshop, I'll call you "
                 "Maestro for a day.", "excitement"),
       Z("lola", "Whoever wins gets the first smoothie. The loser gets the one with the bits.", "amusement"),
       Z("lea", "I'm timing! Ready, steady, wait, which button is start, okay, GO!", "excitement")],
      [O("Races Rosi against the stopwatch to fix the blender.", [], probe=P("cunning", 15, "handwerk"),
         erfolg=[V("rosi", 6), B("rosi", 4), V("lola", 4)], fehlschlag=[V("rosi", 4), GAG("rosi_vs_unit01")],
         zeile=Z("rosi", "Maestro. Ugh. For one day only, so don't get used to it. Okay, maybe a little.", "admiration")),
       O("Fixes the blender with Rosi, her right hand and his left.", [V("rosi", 6), B("rosi", 4), MO("zusammen_geschraubt", ["rosi"], ["lola", "lea"])],
         zeile=Z("rosi", "Your left hand, my right hand. It works. It shouldn't work. Don't look at me like that.", "embarrassment")),
       O("Lets Rosi win and hands her the smoothie.", [V("rosi", 4), V("lola", 2)],
         zeile=Z("rosi", "You let me win. That's stupid, but it's sweet. Drink half.", "amusement"))],
      sets={"rosi": "Engine Room", "lola": "Galley", "lea": "Deck"}),

    E("du_harpune_chiara", "duell", "frech", "Speargun Assembly Against the Clock", WANN((2, 6), TAG), "swim_platform",
      DU("chiara", "handwerk", "lea", "siri", "yasin"),
      "Two dismantled spearguns are lying on towels. Chiara has started a bet. Whoever assembles theirs faster and "
      "hits the buoy decides who does the washing-up tonight. She ties her hair up and smiles at you.",
      [Z("chiara", "Eight parts, one buoy, thirty metres. I've done this blindfolded on a charter in Phuket. You're "
                   "going down, First Officer.", "pride"),
       Z("yasin", "Can you two do this in slow motion? For the algorithm. Chiara, hair flip, please.", "excitement"),
       Z("chiara", "Yasin, one more word and the buoy is you.", "annoyance")],
      [O("Builds his speargun as fast as he can and shoots at the buoy.", [], probe=P("courage", 14, "handwerk"),
         erfolg=[V("chiara", 4), B("chiara", 6), KL("duc", "lea", "Duc beat Chiara in the speargun race")],
         fehlschlag=[V("chiara", 4), B("chiara", 2)],
         zeile=Z("chiara", "Okay, that was fast. That was annoyingly hot and fast. The dishes are mine, so don't gloat.", "desire")),
       O("Helps Chiara with the last part so they finish together.", [], probe=P("charm", 13),
         erfolg=[V("chiara", 6), B("chiara", 4)], fehlschlag=[V("chiara", -2)],
         zeile=Z("chiara", "A tie. You planned that, and nobody plans a tie. Who are you?", "curiosity")),
       O("Nudges Yasin's camera into the water, discreetly.", [V("chiara", 4), V("siri", 4), V("yasin", -6), W("moral", 1)],
         zeile=Z("yasin", "My GoPro! That's a business expense! Siri, stop laughing!", "anger"))],
      sets={"chiara": "Swim", "lea": "Leopard Bikini", "siri": "Riviera Swim"}),

    # ------------------------------------------------------------------ Koepfchen
    E("du_tiere_lea", "duell", "wholesome", "Guess the Animal", WANN((2, 6), ["tag", "abend"]), "foredeck",
      DU("lea", "koepfchen", "siri", "petru"),
      "Lea has brought her field guide up on deck. The game: she describes a sea creature, you have to guess it. "
      "Then the other way round. Siri keeps score. Petru sits on the railing mending a net and pretends not to "
      "listen.",
      [Z("lea", "Okay! It's got eight arms, three hearts, blue blood, and it can taste with its skin. Go!", "excitement"),
       Z("siri", "I'm keeping score. Lea's winning, but only because she reads under the blanket at night.", "amusement"),
       Z("petru", "Too easy.", "neutral")],
      [O("Guesses cleverly, then sets her a hard one.", [], probe=P("perception", 13),
         erfolg=[V("lea", 6), B("lea", 4), V("petru", 4)], fehlschlag=[V("lea", 4)],
         zeile=Z("lea", "A sea pig? That's a real thing? You're making that up. Petru, is he making that up?", "surprise")),
       O("Guesses as badly as he can, on purpose. “A seagull?”", [V("lea", 4), W("moral", 1)],
         zeile=Z("lea", "A seagull is NOT a fish, Duc. Kevin would be so offended.", "amusement")),
       O("Turns to the railing. “Petru, you know this sea. Your turn.”", [], probe=P("empathy", 12),
         erfolg=[V("petru", 6), V("lea", 4), V("siri", 4)], fehlschlag=[V("petru", -2)],
         zeile=Z("petru", "A big grouper under the harbour wall, fifty years old. I call him Napoleon.", "pride"))],
      sets={"lea": "Off Duty", "siri": "Dad's Sweater"}),

    E("gv_quiz", "gagv", "witzig", "Quiz Night: You're the Host", WANN((3, 6), ABEND), "main_salon",
      {"links": "toto", "rechts": "sophia", "zuschauer": ["lea", "rosi", "chiara", "lola", "siri"]},
      "You've set up a quiz night. Two teams, a bell from the galley, you as the host. After three rounds it's a "
      "draw. Totò is suspiciously often right, and there's a search engine glowing on his phone.",
      [Z("toto", "The capital of Mongolia? Ulaanbaatar, obviously. I know these things. I am a cultured man.", "pride"),
       Z("sophia", "Duc. Darling. His phone is under the table and it's glowing. I'm not saying anything. I'm just noticing.", "amusement"),
       Z("lola", "CHEATER! Ring the bell! Ring the cheating bell!", "excitement")],
      [O("Rings the bell. “Phone under the table, Totò. You're disqualified.”", [V("sophia", 6), V("toto", -4), W("moral", 1)], von="sophia",
         zeile=Z("toto", "Disqualified? In Naples this is called research!", "anger")),
       O("Gives Totò a penalty round: a question about his nonna.", [V("toto", 6), V("sophia", 2), W("moral", 1)], von="toto",
         zeile=Z("toto", "My nonna's birthday? The fourth of March. You see? Some things I don't need a phone for.", "love")),
       O("“Bonus question, and only the host knows the answer.”", [], probe=P("charm", 13),
         erfolg=[W("moral", 1), R(1), V("sophia", 4), V("toto", 4)], fehlschlag=[KL("duc", "lola", "The quizmaster didn't know the answer "
                                                                                                   "to his own question")],
         zeile=Z("sophia", "A question only the host can answer. That's clever, and I'm keeping that one.", "admiration"))],
      sets={"sophia": "Crew Party", "lea": "Crew Party", "rosi": "Crew Party", "chiara": "Service", "lola": "Off Duty",
            "siri": "Silver Night"}),

    # ------------------------------------------------------------------ Charme
    E("du_poetry_sophia", "duell", "frech", "Poetry Slam: “Ode to Lola's Fridge”", WANN((3, 6), ABEND), "aft_deck",
      DU("sophia", "charme", "lola", "chiara", "lea", "rosi"),
      "Sophia has called a poetry slam. Lola drew the topic out of a hat: her fridge. Sophia went first, four "
      "verses, and Chiara cried laughing. Now it's your turn. Sophia looks at you over her glass.",
      [Z("sophia", "O fridge, cold keeper of Lola's sins, you hum all night like a lover who knows too much. Your turn, Duc.", "amusement"),
       Z("lola", "That's my fridge she's talking about! It's a good fridge, it's emotionally available!", "excitement"),
       Z("sophia", "Make me feel something for an appliance, darling. I dare you.", "desire")],
      [O("Stands up and reads a cheeky, warm poem about the fridge.", [], probe=P("charm", 14),
         erfolg=[V("sophia", 6), B("sophia", 6), I("ducs_gedicht")], fehlschlag=[V("sophia", 4), W("moral", 1)],
         zeile=Z("sophia", "That last line. You didn't write that about a fridge. Did you.", "desire")),
       O("Reads a poem about the fridge that only Sophia will understand.", [], probe=P("empathy", 13),
         erfolg=[B("sophia", 8), NK("sophia"), MO("gedicht_fuer_sophia", ["sophia"], ["lola", "chiara", "lea", "rosi"])],
         fehlschlag=[V("sophia", 2)],
         zeile=Z("sophia", "Everyone else heard a fridge. I heard something else. Walk me to my cabin later. Just walk.", "love")),
       O("Speaks as the fridge, in the fridge's own voice.", [W("moral", 1), V("lola", 6), V("sophia", 4)],
         zeile=Z("lola", "He did the VOICE. He did the fridge's VOICE, I'm going to cry.", "joy"))],
      sets={"sophia": "Crew Party", "lola": "Off Duty", "chiara": "Service", "lea": "Crew Party", "rosi": "Crew Party"},
      knistern=True, nachklang_text="Sophia copied your poem onto a napkin. In the morning the napkin is folded in "
                                    "your jacket pocket."),

    E("auf_karaoke", "auftritt", "frech", "Karaoke at Alva's", WANN((3, 6), ABEND, an_land=True), "alvas_bar",
      AUF("charme", "alva", "toto", "lea", "siri", "chiara", "casanova"),
      "Alva found a nineties karaoke machine in her cellar. The microphone crackles, the lyrics scroll across an old "
      "tube TV. Half the crew is here. Madame Casanova has already signed up for three songs. Then Alva calls your "
      "name.",
      [Z("alva", "Next on stage, the First Officer! He sings, or he buys a round for the whole bar. Those are the "
                 "rules. I just made them up.", "amusement"),
       Z("casanova", "A duet! He must sing a duet! I volunteer! I have already volunteered!", "excitement"),
       Z("siri", "Pick someone who can't sing, it's more fun. Pick Chiara.", "amusement")],
      [O("Holds out the second microphone and picks a partner.", [PARTNER("siri", "chiara", "lea", "alva"), W("moral", 1), R(1)],
         zeile=Z("alva", "A duet, good. Everyone in Corsica falls in love during a duet. It's the law.", "joy")),
       O("Takes the microphone alone and gives it everything.", [], probe=P("charm", 14),
         erfolg=[V("alva", 4), B("siri", 4), W("ruf", 1), R(1)], fehlschlag=[W("moral", 1), KL("duc", "toto", "Duc sang at Alva's. Loudly. Very loudly.")],
         zeile=Z("toto", "Comandante! Like Pavarotti, if Pavarotti had been hit by a boat! Bravo!", "amusement")),
       O("Gives Madame Casanova her duet.", [V("casanova", 6), W("ruf", 1)],
         zeile=Z("casanova", "Mon capitaine! Hold my hand for the high note! There is no high note! I'll make one!", "joy"))],
      sets={"alva": "alva_festa", "lea": "Crew Party", "siri": "Silver Night", "chiara": "Harbor Night"}),

    E("auf_gitarre", "auftritt", "wholesome", "Guitar on Deck", WANN((2, 6), ["nacht"]), "sun_deck",
      AUF("charme", "siri", "lea", "rosi", "sophia", "lola"),
      "It's warm, and there's just enough power for a single string of fairy lights. You've fetched the old guitar "
      "from the salon. At first only Lea is sitting there, then Rosi and Lola come with blankets. Siri stops at the "
      "top of the stairs, and then comes closer after all.",
      [Z("lea", "Play something everyone knows! Or something nobody knows! Either! Both!", "excitement"),
       Z("siri", "Can you play something quiet? Something that isn't for a camera.", "caring"),
       Z("lola", "I brought Tim Tams for the vibes. Don't ask where I hid them.", "amusement")],
      [O("Plays something everyone can sing along to.", [W("moral", 1), R(1), V("lea", 4), V("lola", 4)],
         zeile=Z("rosi", "Okay, I'm singing, but nobody films this, and I mean it. Yasin, I mean you, wherever you are.", "joy")),
       O("Plays something quiet, just for Siri.", [], probe=P("empathy", 13),
         erfolg=[V("siri", 6), B("siri", 6), NK("siri"), I("plektrum")], fehlschlag=[V("siri", 4)],
         zeile=Z("siri", "My dad used to play like that. Badly, and with his whole heart. Don't stop.", "love")),
       O("Passes the guitar on.", [], probe=P("charm", 12),
         erfolg=[V("rosi", 4), V("sophia", 4), W("moral", 1)], fehlschlag=[W("moral", 1)],
         zeile=Z("sophia", "Rosi can play? Rosi can PLAY? Why does nobody on this boat tell me anything?", "surprise"))],
      sets={"siri": "Dad's Sweater", "lea": "Off Duty", "rosi": "Off Duty", "sophia": "Writing Night", "lola": "Off Duty"},
      knistern=True, nachklang_text="The fairy lights flicker, the guitar leans against the railing. For a while "
                                    "Siri rested her head on your shoulder."),

    # ------------------------------------------------------------------ Herz
    E("auf_herkunft", "auftritt", "ernst", "Where You Come From", WANN((3, 6), ["abend", "nacht"]), "aft_deck",
      AUF("herz", "chiara", "sophia", "lea", "rosi", "siri", "lola"),
      "No power for music, just candles on the aft deck. Someone asked where you actually come from. It goes quiet. "
      "Everyone waits. Nobody pushes. Lola holds out a mug of tea to you.",
      [Z("lola", "You don't have to, Boss. But if you want to, we're all here and nobody's going anywhere. Literally, we're stranded.", "caring"),
       Z("chiara", "You always ask about us, but you never talk about you. Where does the First Officer come from?", "curiosity")],
      [O("Tells his story: family, flight, the long way up.",
         [GESPRAECH("crew", "aft_deck",
                    "Duc tells the crew where he comes from, in his own words: his parents fled Vietnam after the war and "
                    "built a new life in Germany; he grew up in a migrant working-class family and worked his way up. Do "
                    "not invent details he has not said. The women listen and react in "
                    "character, each in her own way: questions, silence, a hand on his arm. No one turns it into pity.", 8),
          R(2), W("moral", 1), F("herkunft_erzaehlt"), MO("herkunft", ["chiara", "sophia", "lea", "rosi", "siri", "lola"])],
         zeile=Z("chiara", "Take your time. We've got all night and nowhere to be.", "caring")),
       O("Tells only one person, later, in private.",
         [GESPRAECH("wahl", "aft_deck",
                    "Later, alone with one person of Duc's choice, he tells her where he comes from, in his own words. Do not "
                    "invent details. She listens, asks honest questions, and keeps it between them.", 6),
          PARTNER("chiara", "sophia", "lea", "rosi", "siri", "lola"), F("herkunft_erzaehlt")],
         zeile=Z("lola", "Okay. Whoever he picks, the rest of us are going to bed and absolutely not listening at the door.", "amusement")),
       O("Waves it off: “Another time.”", [],
         zeile=Z("chiara", "Okay, the offer stays open. That's how it works on a boat.", "caring"))],
      sets={"chiara": "Harbor Night", "sophia": "Writing Night", "lea": "Off Duty", "rosi": "Off Duty", "siri": "Dad's Sweater",
            "lola": "Off Duty"}),
]
