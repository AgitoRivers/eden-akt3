# -*- coding: utf-8 -*-
"""Gag mehrerer Personen - 30 Events: zwei gegeneinander (links/rechts), Zuschauer in der Mitte (Versus)."""
from ereignisse_basis import *  # noqa: F401,F403


def PV(links, rechts, *zuschauer):
    return {"links": links, "rechts": rechts, "zuschauer": list(zuschauer)}


TAG = ["tag"]
EVENTS = [
    E("gv_ocean_glitter", "gagv", "wholesome", "Order in the Galley", WANN((2, 6), ["tag", "dinner"]), "galley",
      PV("chiara", "lola", "rosi", "toto"),
      "Chiara has labelled everything in the galley. Overnight, Lola relabelled every single jar. The salt is now "
      "called “ocean glitter”, the flour “cloud dust”.",
      [Z("chiara", "Where is the salt, Lola. Where. Is. The. Salt.", "anger"),
       Z("lola", "It's ocean glitter, Chi, second shelf. It's all about energy.", "amusement")],
      [O("Sides with Chiara. “Salt is called salt. Change them back.”", [V("chiara", 6), V("lola", -4), F("bordregel_kombuese_angeboten"), W("moral", -1)], von="chiara"),
       O("Sides with Lola. “Ocean glitter stays. I like it.”", [V("lola", 6), V("chiara", -4), W("moral", 1)], von="lola"),
       O("“You two are cooking together today.”", [], probe=P("empathy", 12), erfolg=[V("chiara", 4), V("lola", 4), I("lolas_gewuerz")],
         fehlschlag=[W("moral", -1)]),
       O("Sits down with popcorn and watches them argue.", [W("moral", 1), GAG("ocean_glitter")])],
      gag="ocean_glitter", sets={"chiara": "Service", "lola": "Galley", "rosi": "Engine Room"}),

    E("gv_strip_poker", "gagv", "frech", "Strip Poker for a Canister", WANN((4, 6), ["abend"], an_land=True,
      bed={"wert": ["vertrauen.alva", ">=", 3]}), "alvas_bar", PV("alva", "sophia", "toto", "lola"),
      "Alva has one canister of diesel left, and she'll only part with it if someone beats her at poker. They're "
      "playing for clothes. Three rounds in, Alva has lost her scarf and Sophia her blouse. Sophia hasn't blinked "
      "once all night. Both of them look at you.",
      [Z("alva", "O figliolu, your concierge cheats like a Corsican. I like her. I still win.", "amusement"),
       Z("sophia", "I never cheat, darling. Two years in the wings of a West End theatre teaches you to watch faces. "
                   "Duc, tell her which card she's hiding under her garter.", "desire"),
       Z("lola", "This is the best night of my LIFE.", "excitement")],
      [O("Helps Sophia: gives away Alva's card.", [], probe=P("perception", 13), erfolg=[B("sophia", 6), V("alva", -4)],
         fehlschlag=[V("alva", 4), B("sophia", 2)], von="sophia"),
       O("Warns Alva. “She's reading your face.”", [V("alva", 6), V("sophia", -4), I("alvas_rose")], von="alva",
         zeile=Z("alva", "Alva remembers who helps her, o figliolu. Here. A rose, and the canister stays mine.", "desire")),
       O("Sits down and joins the game.", [], probe=P("cunning", 14), erfolg=[B("sophia", 4), B("alva", 4)],
         fehlschlag=[W("moral", 1), KL("duc", "lola", "Duc lost his shirt at poker in Alva's bar")]),
       O("Leaves the table.", [], zeile=Z("lola", "Boooo.", "disappointment"))],
      sets={"alva": "alva_festa", "sophia": "Shore Leave", "lola": "Off Duty"}),

    E("gv_kevin_auktion", "gagv", "witzig", "Who Gets Kevin?", WANN((3, 6), TAG, bed={"flag": "gag_kevin_1"}), "sun_deck",
      PV("lea", "toto", "siri", "rosi"),
      "Kevin the seagull is sitting on the railing between Lea and Totò, calmly eating a croissant. Lea wants to "
      "save him. Totò wants to catch him and auction him off to tourists.",
      [Z("lea", "He's family now! You can't sell family! Kevin, come to mummy!", "fear"),
       Z("toto", "A seagull that steals butter? On Instagram that's money. I catch, we auction, everybody eats.", "pride")],
      [O("Sides with Lea. “Nobody sells Kevin.”", [V("lea", 6), V("toto", -4), GAG("kevin")], von="lea"),
       O("Helps Totò catch Kevin for the auction.", [G(60), V("toto", 6), V("lea", -6), GAG("kevin"), W("moral", -1)], von="toto"),
       O("Dives for Kevin himself.", [], probe=P("courage", 12), erfolg=[W("moral", 1), V("lea", 4), GAG("kevin")],
         fehlschlag=[W("moral", 2), GAG("kevin")], zeile=Z("siri", "He's in the water. Kevin is dry. Kevin won.", "amusement")),
       O("Sits down with popcorn and watches the chase.", [W("moral", 1), GAG("kevin")])],
      gag="kevin", sets={"lea": "Deck", "siri": "Riviera Swim", "rosi": "Swim"}),

    E("gv_wer_fuehrt", "gagv", "ernst", "Who's in Charge Below Deck?", WANN((2, 6), TAG), "crew_corridor",
      PV("chiara", "rosi", "lea", "sophia"),
      "Chiara assigned Rosi's people to interior duty. Rosi took them back without asking. Now the two of them are "
      "standing in the corridor, and neither will step aside.",
      [Z("chiara", "The interior crew is mine and I assign it. You don't just take my people because you need hands.", "anger"),
       Z("rosi", "Without my hands there is no interior. There's a dark, warm box that smells of fish. Your choice.", "anger")],
      [O("“Chiara's right, Rosi. The interior crew is hers to assign.”", [V("chiara", 6), V("rosi", -6), R(3)], von="chiara"),
       O("“Rosi needs those hands more, Chiara. The repairs come first.”", [V("rosi", 6), V("chiara", -6), U("reparatur", 1)], von="rosi"),
       O("“You two make a plan together, right here, right now.”", [], probe=P("empathy", 13), erfolg=[V("chiara", 4), V("rosi", 4), R(5)],
         fehlschlag=[V("chiara", -2), V("rosi", -2)])],
      sets={"chiara": "Uniform", "rosi": "Engine Room", "lea": "Deck", "sophia": "Concierge"}),

    E("gv_siri_yasin", "gagv", "ernst", "Siri vs. Yasin", WANN((3, 6), ["dinner", "abend"], bed={"nicht": {"flag": "siri_frei"}}),
      "aft_deck", PV("siri", "yasin", "sophia", "lea", "lola"),
      "At dinner Yasin filmed Siri without asking, with her mouth full. Siri stands up. For the first time, she says "
      "no out loud in front of everyone.",
      [Z("siri", "Delete it. Now. I'm not your content when I'm eating. I'm not your content when I'm crying. I'm a person.", "anger"),
       Z("yasin", "Babe, relax, it's cute. People love real moments. You love real moments.", "annoyance")],
      [O("Stands next to Siri and says nothing.", [V("siri", 8), V("yasin", -8), U("siri_marke", 1)], von="siri",
         zeile=Z("siri", "Thank you. I needed someone to just stand there, that's all.", "gratitude")),
       O("Mediates: “Not at dinner.”", [V("siri", 4), V("yasin", -2)], von="yasin"),
       O("Stays quiet and lets Siri decide.", [], probe=P("empathy", 12), erfolg=[V("siri", 6), U("siri_marke", 1)],
         fehlschlag=[V("siri", 2)])],
      sets={"siri": "Silver Night", "sophia": "Concierge", "lea": "Off Duty", "lola": "Off Duty"}),

    E("gv_arancini_duell", "gagv", "witzig", "The Arancini Duel", WANN((3, 6), ["abend"], an_land=True), "alvas_bar",
      PV("lola", "alva", "petru", "rosi", "casanova"),
      "Lola claims her arancini are the best in the Mediterranean. Alva has opinions about that. The whole village "
      "is watching. You're the jury.",
      [Z("lola", "Mine have a secret ingredient, and it's love and three kinds of cheese. Mostly the cheese.", "pride"),
       Z("alva", "Mine have my grandmother's recipe. My grandmother would spit on your love.", "amusement")],
      [O("Raises Lola's hand. “Lola's arancini win.”", [V("lola", 6), V("alva", -4)], von="lola"),
       O("“Alva wins. You can taste forty years of this bar.”", [V("alva", 6), V("lola", -4), W("ruf", 1)], von="alva"),
       O("“A draw. I need more samples.”", [], probe=P("charm", 12), erfolg=[V("lola", 4), V("alva", 4), W("moral", 1)],
         fehlschlag=[V("lola", -2), V("alva", -2)], zeile=Z("casanova", "A draw! A diplomatic triumph! I declare a "
                                                                        "festival!", "joy"))],
      sets={"lola": "Galley", "alva": "alva_standard", "rosi": "Vespa Sunday"}),

    E("gv_megan_sophia", "gagv", "witzig", "Sophia Negotiates with Megan", WANN((5, 6), TAG, bed={"flag": "megan_besuch"}),
      "main_salon", PV("sophia", "megan", "chiara", "rosi"),
      "Sophia wants an afternoon off for the crew. Megan wants results. They sit across the table from each other, "
      "smiling as if each were about to poison the other.",
      [Z("sophia", "One afternoon off, because the crew works better rested. It's in all the studies. I'll send you the studies.", "neutral"),
       Z("megan", "Darling, I invented the studies. They get half a day, and they wear Eden caps while they relax.", "amusement")],
      [O("Sides with Sophia. “They get the afternoon off.”", [V("sophia", 6), V("megan", -2), W("moral", 1)], von="sophia"),
       O("Sides with Megan. “No afternoon off. We need results.”", [V("megan", 6), V("sophia", -4), G(150), W("moral", -1)], von="megan"),
       O("“A whole day, and I'll wear the cap.”", [], probe=P("charm", 13), erfolg=[W("moral", 2), V("megan", 6), V("sophia", 4), GAG("megan_lacht")],
         fehlschlag=[V("megan", 2), W("moral", 1)])],
      sets={"sophia": "Concierge", "megan": "Inspection", "chiara": "Uniform", "rosi": "Engine Room"}),

    E("gv_toto_elsa", "gagv", "witzig", "Totò Defends His Locker", WANN((3, 6), TAG, bed={"flag": "elsa_an_bord"}), "crew_mess",
      PV("toto", "elsa", "chiara", "lola"),
      "Elsa wants to look inside Totò's locker. Totò stands in front of it with his arms spread wide, like a "
      "goalkeeper facing a penalty.",
      [Z("toto", "Lieutenant, this locker is my bedroom. My church. My grandmother is in there. Spiritually.", "fear"),
       Z("elsa", "Then your grandmother won't mind if I say hello. Step aside, Mister Esposito.", "amusement")],
      [O("Stands beside Totò. “That locker is private, Lieutenant.”", [], probe=P("cunning", 13), erfolg=[V("toto", 8), V("elsa", -4)], fehlschlag=[V("toto", 4), V("elsa", -8), F("schmuggel_gefunden")],
         von="toto"),
       O("Steps aside. “Go ahead, Lieutenant, open it.”", [V("elsa", 6), V("toto", -6), V("chiara", 4)], von="elsa"),
       O("Waves Lola over to distract Elsa with cake.", [], probe=P("charm", 11), erfolg=[V("lola", 4), V("elsa", 2), V("toto", 4)],
         fehlschlag=[V("elsa", -2)], zeile=Z("lola", "Lieutenant! Cake! It's a normal cake! Please eat it before I explain it.", "nervousness"))],
      sets={"chiara": "Uniform", "lola": "Galley"}),

    E("gv_festa_kleid", "gagv", "wholesome", "A Dress for Chiara", WANN((19, 20), TAG), "vip_cabin",
      PV("siri", "chiara", "sophia", "lea"),
      "Siri wants to lend Chiara a dress for the festa. Silver, backless, very expensive. Chiara wants to go in "
      "uniform. Siri holds up the dress and won't let it go.",
      [Z("siri", "You have the shoulders for this. I've wanted to say that for days. Try it on. Five minutes.", "caring"),
       Z("chiara", "I'm an officer. Officers don't wear silver. Officers wear navy and responsibility.", "embarrassment")],
      [O("Sides with Siri. “Try it on, Chiara.”", [V("siri", 6), V("chiara", 2), F("chiara_festa_kleid")], von="siri",
         zeile=Z("chiara", "Fine. Five minutes. Nobody look. Okay, you can look. Is it too much? It's too much.", "embarrassment")),
       O("Sides with Chiara. “The uniform is fine.”", [V("chiara", 6), V("siri", -2)], von="chiara"),
       O("“You look good in anything, but this…”", [], probe=P("charm", 12), erfolg=[B("chiara", 6), V("siri", 4), F("chiara_festa_kleid")],
         fehlschlag=[V("chiara", -2)])],
      sets={"siri": "Silver Night", "chiara": "Uniform", "sophia": "Crew Party", "lea": "Crew Party"}),

    # 18.10.2026: Chiara statt Holm an der Gangway (Holm ist ab dem Morgen von Tag 2 im Krankenhaus)
    E("gv_casanova_chiara", "gagv", "witzig", "The Mayor Wants to Come Aboard", WANN((3, 4), TAG), "swim_platform",
      PV("casanova", "chiara", "toto", "lea"),
      "Madame Casanova wants to board the yacht ceremonially, with a sash and a photographer. Chiara is standing at "
      "the gangway and isn't letting anyone past. The mayor already has one foot on the ladder.",
      [Z("casanova", "Mademoiselle! The village welcomes you! With speeches! Three speeches! May I come aboard?", "excitement"),
       Z("chiara", "No. Our captain is in hospital and this boat is not a stage. Come back when we're not sinking "
                   "quite so politely.", "annoyance")],
      [O("Holds the ladder for Madame Casanova.", [V("casanova", 6), V("chiara", -4), W("ruf", 1)], von="casanova"),
       O("Stands with Chiara. “Not today, Madame.”", [V("chiara", 6), V("casanova", -4)], von="chiara"),
       O("Lets the mayor give one short speech on the jetty.", [], probe=P("charm", 12), erfolg=[V("casanova", 4), V("chiara", 4), W("ruf", 1)],
         fehlschlag=[V("chiara", -2), GAG("casanova_kapelle")])],
      sets={"chiara": "Uniform", "lea": "Deck"}),

    E("gv_armdruecken", "gagv", "witzig", "Arm Wrestling in the Mess", WANN((2, 6), ["abend"]), "crew_mess",
      PV("rosi", "toto", "lea", "lola", "chiara"),
      "Totò claimed that women can't arm-wrestle. Rosi has rolled up her sleeves. The crew is drumming on the table.",
      [Z("rosi", "Say it again, Totò. Say it again while I break your wrist.", "anger"),
       Z("toto", "Rosi, cara, it was a joke, a Neapolitan joke. We say it to everyone, even to men.", "nervousness")],
      [O("Bets on Rosi.", [V("rosi", 6), V("toto", -2), W("moral", 1)], von="rosi"),
       O("Bets on Totò.", [V("toto", 4), V("rosi", -4), W("moral", -1)], von="toto"),
       O("Takes on the winner.", [], probe=P("courage", 13), erfolg=[V("rosi", 4), B("rosi", 4), W("moral", 1), I("rosis_handschuhe")],
         fehlschlag=[W("moral", 1)], zeile=Z("rosi", "Don't you dare let me win. I'll know.", "desire"))],
      sets={"rosi": "Off Duty", "lea": "Off Duty", "lola": "Off Duty", "chiara": "Service"}),

    E("gv_aussenborder", "gagv", "wholesome", "Petru vs. Rosi", WANN((3, 6), TAG, bed={"wert": ["vertrauen.petru", ">=", 2]}),
      "petru_workshop", PV("petru", "rosi", "lea"),
      "The tender's outboard is sputtering. Petru wants to fix it with a hammer and a feel for it. Rosi wants a "
      "multimeter and a laptop. Each thinks the other one's method is superstition.",
      [Z("petru", "Listen. The engine talks. The hammer answers.", "neutral"),
       Z("rosi", "The engine does not talk, Petru. The engine has a fault code. I'm reading it. Please put the hammer down.", "annoyance")],
      [O("Nods at the hammer. “Go on, Petru. Let's hear what the engine says.”", [], probe=P("courage", 11), erfolg=[V("petru", 8), V("rosi", -2)], fehlschlag=[V("petru", 4), V("rosi", 4)], von="petru"),
       O("“Put the hammer down, Petru. Rosi reads the fault code.”", [V("rosi", 6), V("petru", -2)], von="rosi"),
       O("Rosi measures first, then Petru's hammer.", [], probe=P("empathy", 12), erfolg=[V("petru", 6), V("rosi", 6), I("petrus_hammer")],
         fehlschlag=[V("petru", 2), V("rosi", 2)], zeile=Z("petru", "Good. Science first, then the hammer. Like my "
                                                                    "father did.", "approval"))],
      sets={"rosi": "Vespa Sunday", "lea": "Expedition"}),

    E("gv_oktopus", "gagv", "wholesome", "The Octopus", WANN((2, 6), TAG), "swim_platform",
      PV("lea", "siri", "toto", "rosi"),
      "While snorkelling, Lea found a small octopus and brought it back. Siri wants to return it to the sea at once. "
      "She knows a surprising amount about octopuses.",
      [Z("lea", "Look at him! He held my finger! Can we keep him? Just for today? In the ice bucket?", "joy"),
       Z("siri", "He's scared, Lea. They're smarter than half of Instagram. He needs a dark rock, not an ice bucket.", "caring")],
      [O("Sides with Lea. “He can stay in the ice bucket, just for today.”", [V("lea", 6), V("siri", -4)], von="lea"),
       O("Sides with Siri. “He goes back in the sea, Lea.”", [V("siri", 6), V("lea", -2), U("siri_marke", 1), I("seeglas")], von="siri"),
       O("Takes him back together, with Siri explaining.", [], probe=P("empathy", 10), erfolg=[V("siri", 6), V("lea", 4), F("siri_meeresbio")],
         fehlschlag=[V("siri", 2), V("lea", 2)], zeile=Z("siri", "Three hearts and blue blood. He'll remember you, Lea, because they remember faces.", "admiration"))],
      sets={"lea": "Dive", "siri": "Sea Siren", "rosi": "Swim"}),

    E("gv_casanova_alva", "gagv", "witzig", "The VIP Lounge", WANN((3, 5), TAG, an_land=True), "alvas_bar",
      PV("casanova", "alva", "petru", "elsa", "pascal"),
      "Madame Casanova wants to turn Alva's bar into a VIP lounge for the festa, with a velvet rope. Alva wants her "
      "bar to stay the way it is: loud, full, and for everyone. Behind them Pascal walks along the wall with a tape "
      "measure, his hat pushed back.",
      [Z("casanova", "A velvet rope! Gold chairs! A VIP list! With the yacht crew as the main VIPs!", "excitement"),
       Z("alva", "My bar has had one rule for forty years: everybody drinks, fishermen, mayors and dogs. No rope.", "annoyance"),
       Z("pascal", "Four metres eighty, Madame. It's for the rope, Alva, only the rope. Don't look at me like that, I just "
                   "hold the tape.", "amusement")],
      [O("Sides with Casanova. “One velvet rope, just for the festa.”", [V("casanova", 6), V("alva", -4), W("ruf", 1)], von="casanova"),
       O("Sides with Alva. “Her bar stays as it is.”", [V("alva", 6), V("casanova", -4)], von="alva"),
       O("“Fine, a VIP lounge. All the fishermen are VIPs.”", [], probe=P("charm", 12), erfolg=[V("alva", 4), V("casanova", 4), W("ruf", 1)],
         fehlschlag=[V("casanova", -2)], zeile=Z("elsa", "A VIP list where everyone is a VIP. Very Corsican. I "
                                                         "approve.", "amusement"))],
      sets={"alva": "alva_standard"}),

    E("gv_megan_chiara", "gagv", "ernst", "Megan's Inspection", WANN((5, 6), TAG, bed={"flag": "megan_besuch"}), "main_salon",
      PV("megan", "chiara", "sophia", "lola"),
      "Megan runs a white glove along the bar in the salon and holds her finger up to Chiara. A tiny grey smudge. "
      "Chiara goes red, then white.",
      [Z("megan", "Dust, on my bar, on my boat. Explain it to me as if I were an investor.", "disapproval"),
       Z("chiara", "We have no power, no water and no sleep. We have dust. I accept the dust. I will not apologise for it.", "anger")],
      [O("Nods at Megan. “Not good enough, Chiara.”", [V("megan", 6), V("chiara", -8), W("moral", -1)], von="megan"),
       O("Stands next to Chiara. “This ship is clean, Megan.”", [V("chiara", 8), V("megan", -4), R(5)], von="chiara"),
       O("Takes the glove and wipes the smudge off himself.", [], probe=P("charm", 13), erfolg=[V("megan", 4), V("chiara", 6), GAG("megan_lacht")],
         fehlschlag=[V("megan", -2), V("chiara", 4)], zeile=Z("megan", "The First Officer cleans. Interesting. Ahaha— don't look at me.", "amusement"))],
      sets={"megan": "Inspection", "chiara": "Uniform", "sophia": "Concierge", "lola": "Galley"}),

    E("gv_keks", "gagv", "witzig", "Megan and the Cookie", WANN((5, 6), TAG, bed={"flag": "megan_besuch"}), "galley",
      PV("lola", "megan", "rosi", "toto"),
      "Lola holds out a cookie to Megan. Megan doesn't eat cookies. Megan hasn't eaten sugar since 2019. Lola just "
      "keeps holding out the cookie and smiling.",
      [Z("lola", "It's a normal cookie, ninety percent normal. Just one, love, you look like you need a hug in food form.", "caring"),
       Z("megan", "I don't eat cookies. I don't eat joy. I eat results. …Is that chocolate?", "curiosity")],
      [O("Smiles at Megan. “Just one bite. It won't kill you.”", [V("lola", 6), V("megan", 4), GAG("megan_lacht")], von="lola",
         zeile=Z("megan", "Oh no. That's good. That's very good. Why is the room warm. Why am I happy.", "joy")),
       O("Gently lowers Lola's hand. “She said no, Lola.”", [V("megan", 4), V("lola", -2)], von="megan"),
       O("Takes a cookie himself, so Lola isn't left standing there.", [], probe=P("courage", 10), erfolg=[V("megan", 6), V("lola", 4), W("moral", 1)],
         fehlschlag=[W("moral", 1), EN(-1)])],
      sets={"lola": "Galley", "megan": "Inspection", "rosi": "Engine Room"}),

    E("gv_versoehnung", "gagv", "wholesome", "Peace Cake", WANN((3, 6), TAG, bed={"flag": "lea_rosi_streit"}), "galley",
      PV("lea", "rosi", "lola", "chiara"),
      "Lea and Rosi had a fight. Now both of them are baking a peace cake to apologise, at the same time, in the "
      "same galley. It escalates.",
      [Z("lea", "Mine has strawberries. Because I'm sorry. And because strawberries are sorry too.", "sadness"),
       Z("rosi", "Mine has Sicilian almonds in it, which means I'm more sorry. Scientifically.", "pride")],
      [O("Tries Lea's cake first.", [V("lea", 6), V("rosi", 2), F("lea_rosi_versoehnt")], von="lea"),
       O("Tries Rosi's cake first.", [V("rosi", 6), V("lea", 2), F("lea_rosi_versoehnt")], von="rosi"),
       O("Puts both cakes on one plate and eats them together.", [], probe=P("empathy", 10), erfolg=[V("lea", 6), V("rosi", 6), W("moral", 1), F("lea_rosi_versoehnt")],
         fehlschlag=[V("lea", 2), V("rosi", 2), F("lea_rosi_versoehnt")], zeile=Z("lola", "Strawberry almond! You two just invented a cake, and I'm crying.", "joy"))],
      sets={"lea": "Off Duty", "rosi": "Off Duty", "lola": "Galley", "chiara": "Service"}),

    E("gv_elsa_alva", "gagv", "witzig", "Diesel Under the Bar", WANN((3, 6), TAG, an_land=True), "alvas_bar",
      PV("elsa", "alva", "petru", "casanova"),
      "Elsa is sitting at Alva's bar, drinking an espresso. Under the counter stand four diesel canisters. Everyone "
      "knows. Elsa looks at Alva for a long time.",
      [Z("elsa", "Alva. That smell. Is it diesel, or is it your perfume?", "amusement"),
       Z("alva", "It's my perfume, Lieutenant. It's called Fisherman's Dream. Very exclusive. Another espresso?", "desire")],
      [O("Sniffs the air. “That's diesel, Alva.”", [V("elsa", 6), V("alva", -6)], von="elsa"),
       O("Leans on the bar. “Nice perfume, Alva. Very exclusive.”", [], probe=P("cunning", 12), erfolg=[V("alva", 6)], fehlschlag=[V("alva", 4), V("elsa", -4)], von="alva"),
       O("Buys a canister from Alva, with a receipt.", [G(-120), V("elsa", 2), V("alva", 4)],
         zeile=Z("elsa", "An official purchase with a receipt, in this village. I might frame it.", "amusement"))],
      sets={"alva": "alva_standard"}),

    E("gv_festa_outfits", "gagv", "wholesome", "Who Dresses the Crew?", WANN((19, 20), TAG), "crew_corridor",
      PV("chiara", "sophia", "lea", "rosi", "lola"),
      "The crew needs outfits for the festa. Chiara wants matching white shirts. Sophia wants everyone to wear what "
      "she finds beautiful. The pile of clothes in the corridor keeps growing.",
      [Z("chiara", "White shirts and navy trousers, because we represent the yacht. We look like a crew, not a festival.", "neutral"),
       Z("sophia", "It IS a festival, darling, so let them shine. Rosi has a dress she's never worn. Let her wear it.", "caring")],
      [O("“Chiara's right. White shirts and navy trousers for everyone.”", [V("chiara", 6), V("sophia", -2), R(3), W("moral", -1)], von="chiara"),
       O("Sides with Sophia. “Let them shine. Everyone wears what they like.”", [V("sophia", 6), V("rosi", 4), W("moral", 1)], von="sophia"),
       O("“One matching detail, and the rest is up to you.”", [], probe=P("charm", 11), erfolg=[V("chiara", 4), V("sophia", 4), W("moral", 1)],
         fehlschlag=[V("chiara", -2)], zeile=Z("lola", "A red flower for everyone! I'll nick them from the mayor.", "joy"))],
      sets={"chiara": "Uniform", "sophia": "Concierge", "lea": "Crew Party", "rosi": "Festa", "lola": "Off Duty"}),


    # Reibung in der Crew (Duc 27.10.2026, Crew-Moral Variante C): zwei aus der Crew gegeneinander, Duc entscheidet.
    # Eine Seite ist verlockend (Geld, Reparatur, Energie, Vertrauen) und kostet Moral; die andere hebt sie.
    E("gv_dienstplan", "gagv", "ernst", "The Rota", WANN((3, 6), TAG), "crew_mess",
      PV("chiara", "sophia", "lea", "rosi"),
      "Chiara has pinned a new rota to the mess door. Double shifts for everyone until Megan's inspection. Sophia has "
      "crossed out tomorrow afternoon in red and written FREE across it.",
      [Z("chiara", "Megan does not care that we're tired. Megan cares that the brass shines. Two shifts. Everyone.", "annoyance"),
       Z("sophia", "Darling, they've polished brass for a week. One afternoon in the sea, or I start hearing mutiny in the walls.", "caring")],
      [O("Takes Chiara's side. “The rota stays.”", [V("chiara", 6), V("sophia", -4), R(3), W("moral", -1)], von="chiara"),
       O("Takes Sophia's side. “Tomorrow afternoon is free.”", [V("sophia", 6), V("chiara", -4), W("moral", 1)], von="sophia"),
       O("“Mornings Chiara's way, afternoons free.”", [], probe=P("charm", 12), erfolg=[V("chiara", 4), V("sophia", 4), W("moral", 1)],
         fehlschlag=[V("chiara", -2), W("moral", -1)],
         zeile=Z("lea", "Free afternoon! I'm getting my fins before anybody changes their mind.", "joy"))],
      sets={"chiara": "Service", "sophia": "Concierge", "lea": "Deck", "rosi": "Engine Room"}),

    E("gv_trinkgeld_topf", "gagv", "frech", "The Tip Jar", WANN((3, 6), ["dinner", "abend"]), "crew_mess",
      PV("lola", "rosi", "lea", "chiara"),
      "The village left tips after Lola's dinner on the quay. Three hundred euros in a jam jar. Lola wants to split "
      "it. Rosi wants a new fuel pump.",
      [Z("lola", "Split it six ways, Boss, and everyone buys something stupid. That's the whole point of tips.", "joy"),
       Z("rosi", "Something stupid like a fuel pump? The old one is held together with prayers and my hairband.", "annoyance")],
      [O("“The money goes to Rosi's fuel pump.”", [V("rosi", 6), V("lola", -4), U("reparatur", 1), W("moral", -1)], von="rosi"),
       O("“Lola's right. Split it six ways.”", [V("lola", 6), V("rosi", -2), W("moral", 1)], von="lola"),
       O("“It goes in the ship's account, for emergencies.”", [G(150),
                                                       V("chiara", 2), W("moral", -1)])],
      sets={"lola": "Off Duty", "rosi": "Engine Room", "lea": "Off Duty", "chiara": "Service"}),

    E("gv_musik_nachts", "gagv", "wholesome", "After Midnight", WANN((2, 6), ["abend", "nacht"]), "foredeck",
      PV("lea", "chiara", "sophia", "rosi"),
      "Lea has put a speaker on the foredeck, and three people are dancing around it. It's half past one. Chiara is "
      "standing in the hatch in her dressing gown. She has the early watch.",
      [Z("chiara", "Some of us are on the bridge at five, so turn it off, Lea. Now, please.", "annoyance"),
       Z("lea", "It's one song! Okay, it was four songs. But this one's really good, Chiara, listen-", "excitement")],
      [O("“Lights out. Chiara's right.”", [V("chiara", 6), V("lea", -4), EN(1), W("moral", -1)], von="chiara"),
       O("“Let them dance, Chiara. One more song.”", [V("lea", 6), V("chiara", -4), W("moral", 1)], von="lea"),
       O("Buys everyone headphones in the village tomorrow.", [G(-40),
                                                              V("lea", 2), V("chiara", 2), W("moral", 1)])],
      sets={"lea": "Crew Party", "chiara": "Uniform", "sophia": "Writing Night", "rosi": "Off Duty"}),

    E("gv_gute_kabine", "gagv", "witzig", "The Good Cabin", WANN((3, 6), TAG), "crew_corridor",
      PV("sophia", "lola", "lea", "rosi"),
      "There's a spare crew cabin by the laundry. It has a real porthole and a door that locks. Sophia has put her "
      "books on the bunk. Lola has put her pillow on top of the books.",
      [Z("sophia", "I need quiet to write, darling. Lola needs quiet like a fish needs a bicycle.", "pride"),
       Z("lola", "I snore, Boss, everyone knows I snore, so a door that shuts is basically charity.", "amusement")],
      [O("Gives the cabin to Sophia. “You need the quiet to write.”", [V("sophia", 6), V("lola", -4), F("kabine_sophia")], von="sophia"),
       O("“The cabin is Lola's. We all need a door between us and that snoring.”", [V("lola", 6), V("sophia", -4), F("kabine_lola")], von="lola"),
       O("Yasin wants it for his camera gear. He pays.", [G(120),
                                                         V("yasin", 4), W("moral", -1), F("kabine_yasin")]),
       O("Holds out his hat. “You two draw lots.”", [V("sophia", 2), V("lola", 2), W("moral", 1), F("kabine_lola")],
         zeile=Z("lola", "Lola wins! Lola always wins. Sophia, you can visit, but bring biscuits.", "joy"))],
      sets={"sophia": "Writing Night", "lola": "Off Duty", "lea": "Off Duty", "rosi": "Off Duty"}),

    E("gv_ruhetag", "gagv", "ernst", "Sunday", WANN((4, 6), ["fruehstueck", "tag"]), "crew_mess",
      PV("rosi", "lea", "chiara", "lola"),
      "It's Sunday, if anyone is counting. Lea has packed towels and a cool box for the cove. Rosi has packed a "
      "toolbox. Both bags are on the mess table, waiting.",
      [Z("lea", "One day, Officer. One beach, one swim. Then we fix the whole world on Monday, promise.", "excitement"),
       Z("rosi", "The batteries don't know it's Sunday. If we stop now, she cools down and we start from zero.", "annoyance")],
      [O("“Everyone works. Rosi's right.”", [V("rosi", 6), V("lea", -4), U("reparatur", 1), W("moral", -1)], von="rosi"),
       O("“Beach day. Everyone.”", [V("lea", 6), V("rosi", -2), W("moral", 1)], von="lea"),
       O("“Work till noon, then the cove.”", [], probe=P("empathy", 12),
         erfolg=[U("reparatur", 1), V("rosi", 2), V("lea", 2), W("moral", 1)], fehlschlag=[V("rosi", -2), W("moral", -1)],
         zeile=Z("rosi", "Fine, noon. But if the cove has a generator, I'm fixing it.", "amusement"))],
      sets={"rosi": "Engine Room", "lea": "Deck", "chiara": "Service", "lola": "Galley"}),

    E("gv_einkaufsliste", "gagv", "witzig", "Lola's Shopping List", WANN((2, 6), TAG), "galley",
      PV("lola", "chiara", "rosi", "lea"),
      "Lola has written a shopping list for the village. It's two pages long and has saffron on it. Chiara has "
      "written a shorter one. It says: tins.",
      [Z("lola", "You can't feed a crew on tins, Chi, that's how mutinies start. I read about it.", "amusement"),
       Z("chiara", "We have a budget, Lola, and the budget does not include saffron. The budget barely includes us.", "disapproval")],
      [O("Takes Chiara's list. “Tins. We stay on budget.”", [G(60), V("chiara", 6), V("lola", -4),
                                    W("moral", -1)], von="chiara"),
       O("Takes Lola's two pages. “Buy all of it, saffron too.”", [G(-80), V("lola", 6), V("chiara", -2),
                                     W("moral", 1)], von="lola"),
       O("Goes fishing with Petru instead.", [], probe=P("perception", 11),
         erfolg=[V("lola", 4), I("frischer_fang"), W("moral", 1)], fehlschlag=[V("lola", 2)],
         zeile=Z("lola", "Look at that, fresh fish and no saffron needed! Boss, you're a genius. A smelly genius.", "joy"))],
      sets={"lola": "Galley", "chiara": "Service", "rosi": "Off Duty", "lea": "Off Duty"}),
]

item("alvas_rose", "Alvas Rose", "geschenk", text="A red rose from Alva's hair. Lola and Siri love it.")
item("petrus_hammer", "Petrus kleiner Hammer", "attribut", effekt={"bonus": ["courage", 1]},
     text="+1 Courage while carried. “Science, then hammer.”")
item("leas_taucherbrille", "Leas alte Taucherbrille", "attribut", effekt={"bonus": ["perception", 1]},
     text="+1 Perception while carried. Smells of salt and sun cream.")
item("rosis_handschuhe", "Rosis Werkstatthandschuhe", "attribut", effekt={"bonus": ["cunning", 1]},
     text="+1 Cunning while carried. Too small, but she wanted you to have them.")
item("plektrum", "Lolas Plektrum", "gluecksbringer", effekt={"vorteil": "charm"}, text="Once a day: advantage on Charm.")
item("messing_anker", "Brass Anchor Keyring", "geschenk", text="Rusty, fished out of the bay. Holm "
                                                                              "would love it.")
item("seeglas", "Green Sea Glass", "geschenk", text="Worn smooth by the sea. Siri loves it.")
