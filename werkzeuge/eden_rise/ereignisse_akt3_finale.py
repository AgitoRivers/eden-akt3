# -*- coding: utf-8 -*-
"""Akt 3, Paket F: Kommission (Tag 35 Tag), Festa mit Minicu (Tag 35 Abend), Mitternacht (Tag 35 Nacht).
Drehbuch docs/wiki/welt/drehbuch_akt3.md 5.25, 5.27, Abschnitt 8. Die Enden rechnet kern/akt3.py (saeulen, ende) und zeigt
kern/abschluss.py (Feinschliff der Texte: Duc, ganz am Ende).

mo_kommission (Bibis Tier-Beweis) steht in der Event-Liste vorher und eroeffnet, wenn es kommt (F-25); a3_kommission schliesst
dann ohne zweite Ansage an. Die drei gebauten Festa-Szenen (br_ehrenbuerger, ab_casanova_flamenco, gv_rotes_kleid) stellt
ereignisse_basis.bauen() auf Tag 35, Abend, Piazza um (F-22); sie warten auf akt3_festa, das a3_festa setzt."""
from ereignisse_basis import *  # noqa: F401,F403
from ereignisse_gag1 import P1  # noqa: E402
from ereignisse_ligeia import G  # noqa: E402
from ereignisse_akt3_woche4 import FL, NICHT, DA, AKT3, JE, PFL, FRAME, DIREKT, tags_fuer  # noqa: E402
from ereignisse_akt3_woche5 import MN_FRAUEN  # noqa: E402

DEAL = FL("a3_deal")
LOSW = lambda lid, wahl: FL("a3_los_%s_%s" % (lid, wahl))
LOSE_ALLE = ["tafel", "buehne", "topf", "menue", "fang", "getraenk", "girlande", "glocke", "lichter", "system", "garten", "kleider", "bilder"]
ZG = lambda p: FL("a3_zeuge_" + p)

# ------------------------------------------------------------------ 5.25 Die Kommission
KOMMISSION = [
    E("a3_kommission", "gag1", "ernst", "The Commission", PFL(35, "tag", NICHT(DEAL)), "village_harbour",
      P1("elsa", ("casanova", "?", "stands very straight")),
      "Day 35. Sunday. Two men from Ajaccio sit behind a folding table on the quay. A clerk with a lot of paper. "
      "Half the village stands behind them. Kevin is on the church roof.",
      [JE(G("elsa", "[clear throat] The animals are done. Now the people.", "neutral"), "an", {"gesehen": "mo_kommission"}),
       JE(G("elsa", "[clear throat] Gentlemen. Thank you for coming. Finally.", "neutral"), "an", None),
       G("elsa", "[sigh] They are asking what happened in this bay on the twenty-first, twenty-second and twenty-third. "
                 "And who saw it with their own eyes.", "neutral")],
      [O("Steps back, so the village can speak.", [DIREKT("a3_kom_zeugen")]),
       O("Stands next to Elsa.", [V("elsa", 2), DIREKT("a3_kom_zeugen")])],
      sets={"elsa": "Standard"}),
    E("a3_kom_zeugen", "gag1", "ernst", "Who Saw It?", FRAME(), "village_harbour", P1("casanova"),
      "One by one, people step up to the folding table. The clerk writes down every name.",
      [JE(G("petru", "[clear throat] I saw the burning torches at my workshop. And I saw who stayed. And the village rowed out. Like in 1924.", "neutral"), "petru",
          {"alle": [ZG("petru"), FL("bl_dorf_rudert")]}),
       JE(G("petru", "[clear throat] I saw the burning torches at my workshop. He asked me to say it. So I say it.", "neutral"), "petru", FL("a3_zeuge_petru_kalt")),
       JE(G("petru", "[clear throat] I saw the burning torches at my workshop, and who stayed. And I'm not afraid of a letter from Monaco.", "pride"), "petru", FL("a3_zeuge_petru_ehrlich")),
       JE(G("petru", "[clear throat] I saw the burning torches at my workshop. And I saw who stayed.", "neutral"), "petru", ZG("petru")),
       JE(G("mina", "[sigh] I knocked on every door that day, when the phones were dead. I saw who opened, and who didn't. I'm scared. I'm saying it anyway.", "pride"), "mina", FL("a3_zeuge_mina_ehrlich")),
       JE(G("mina", "[sigh] I knocked on every door that day, when the phones were dead. I saw who opened, and who didn't.", "nervousness"), "mina", ZG("mina")),
       JE(G("batu", "[chuckle] Men in white. Twice they asked me for the north road. The crew buys all my rice now, so I can say it.", "neutral"), "batu", FL("a3_zeuge_batu_kauf")),
       JE(G("batu", "[clear throat] Men in white. They asked me twice for the north road. I told Duc then. Now I tell you.", "neutral"), "batu", ZG("batu")),
       JE(G("alva", "[sniff] From the square I saw the north barricade open. Then men in white came through. Papa would say: tell them, then pour them a drink. So I tell you.", "sadness"), "alva", FL("a3_zeuge_alva_papa")),
       JE(G("alva", "[sigh] From the square I saw the north barricade open. Then men in white came through. I saw that with my own eyes.", "neutral"), "alva", ZG("alva")),
       JE(G("sandru", "[clear throat] My name is Iskander. I carried Alva out of the rubble. And eleven days later, A.V. switched off my legs.", "neutral"), "sandru",
          {"alle": [ZG("sandru"), FL("sandru_herkunft")]}),
       JE(G("sandru", "[clear throat] My name is Sandru. I carried Alva out of the rubble. And eleven days later, A.V. switched off my legs.", "neutral"), "sandru", ZG("sandru")),
       JE(G("anghjulu", "[clear throat] I saw the gate open. I was sober. Write that down too. It doesn't happen often.", "neutral"), "don",
          {"alle": [ZG("anghjulu"), FL("bl_kirche_don")]}),
       JE(G("anghjulu", "[sigh] I was asleep on the church steps, my son. But I saw the gate open before I fell asleep.", "remorse"), "don",
          {"alle": [ZG("anghjulu"), FL("bl_kirche_don_schlaeft")]}),
       JE(G("anghjulu", "[clear throat] Only what my eyes saw, not my ears: the gate opened. I was outside the church door all night.", "neutral"), "don", FL("a3_zeuge_anghjulu_ehrlich")),
       JE(G("anghjulu", "[sigh] I was outside the church door all night. I saw the gate open.", "neutral"), "don", ZG("anghjulu")),
       JE(G("casanova", "[sigh] Every night, Alon's people left a letter on my church steps, in that neat handwriting. I kept all of them. I'm giving them to you for the festa. A terrible reason, but it's mine.", "embarrassment"), "casanova", FL("a3_zeuge_casanova_festa")),
       JE(G("casanova", "[clear throat] Every night, Alon's people left a letter on my church steps, in that neat handwriting. I kept all of them. Here they are.", "pride"), "casanova", ZG("casanova")),
       G("bonaventure", "[clear throat] A man named White paid me in clean money, like a bank. I gave the order to burn. I gave the order to stop. "
                        "I am Captain Buenaventura of The Eventually.", "remorse"),
       JE(G("riscossore", "[chuckle] He's telling the truth. It's in my book, page forty-one. A man in prison pays nobody, so I'd like him to stay out.", "neutral"),
          "risc", FL("a3_riscossore_kommt")),
       JE(G("riscossore", "[clear throat] Nobody believes a pirate. Fine. Believe my book. Page forty-one: what a man named White offered the captain. "
                          "A man in prison pays nobody.", "neutral"), "risc", None)],
      [O("Watches the clerk write.", [F("a3_zeuge_bonaventure"), DIREKT("a3_kom_minicu")])]),
    E("a3_kom_minicu", "gag1", "ernst", "The Big Man", FRAME(), "village_harbour", P1("anghjulu"),
      "The older commissioner looks at his list and asks: “The man at the gate? The big one?”",
      [G("anghjulu", "[sigh] He can't come today, Commissioner.", "sadness")],
      [O("Says nothing. Nobody on the quay asks what that means.", [DIREKT("a3_kom_beweise")])],
      sets={"anghjulu": "anghjulu_standard"}),
    E("a3_kom_beweise", "gag1", "ernst", "Paper", FRAME(), "village_harbour", P1("elsa"),
      "Then the paper. Elsa lays out everything the village has, one piece after the other.",
      [JE(G("elsa", "[clear throat] White's orders from the villa cellar. Day 22, phase 3: fire, houses.", "neutral"), "feuer", FL("a3_beweis_feuer")),
       JE(G("elsa", "[clear throat] A crate of collars from the grotto. Totò kept it for this day.", "neutral"), "kiste", FL("alon_kiste_genutzt")),
       JE(G("siri", "[sigh] My video. No filter, no music. Just what we saw.", "neutral"), "siri", FL("a3_siri_post")),
       JE(G("sophia", "[clear throat] Darling, I wrote down every time and every word I heard on the radio that night. I didn't know why. Now I do.", "neutral"), "sophia", FL("sophia_notizen")),
       JE(G("charly", "[sigh] Twenty-one forty. He said 'tonight'. Seven out of ten for clarity.", "neutral"), "funk", {"eine": [FL("bl_funk_white"), FL("bl_funk_charly")]}),
       JE(G("elsa", "[clear throat] The radio log. Three o'clock, the night of the twenty-second, from the north road. Two words: 'Not yet.'", "neutral"), "wache", FL("bl_wache_gesehen")),
       G("elsa", "[clear throat] And Pascal's book, from his locked drawer. First Officer. All of it, or only Alon's part?", "neutral")],
      [O("“All of it.”", [F("a3_kassenbuch_alles"), DIREKT("a3_kom_ende")],
         zeile=G("casanova", "[sigh] Yes. Me too.", "neutral")),
       O("“Only Alon's part.”", [F("a3_kassenbuch_teil"), DIREKT("a3_kom_ende")],
         zeile=G("elsa", "[sigh] For the record: understood.", "neutral"))],
      sets={"elsa": "Standard"}),
    E("a3_kom_ende", "gag1", "ernst", "The Commission", FRAME(), "village_harbour", P1("elsa"),
      "The clerk closes his folder. The older commissioner stands up and puts on his hat.",
      [G("elsa", "[sigh] He says: Thank you. We have what we need. Or we don't. You'll know tonight.", "neutral")],
      [O("Goes to help with the festa.", [F("a3_kommission_fertig")])],
      sets={"elsa": "Standard"}),
    E("a3_kommission_deal", "gag1", "ernst", "The Commission", PFL(35, "tag", DEAL), "village_harbour", P1("casanova"),
      "Two men from Ajaccio sit behind a folding table on the quay. Nobody steps forward. You are not down there. You are up at the villa, "
      "watching it on a screen.",
      [G("casanova", "[sigh] Nobody saw anything, gentlemen. Nobody.", "sadness")],
      [O("Turns off the screen.", [F("a3_kommission_fertig")])]),
]

# ------------------------------------------------------------------ 5.27 Die Festa (Tag 35, Abend)
FESTA = [
    E("a3_festa", "gag1", "wholesome", "The Festa", PFL(35, "abend", NICHT(DEAL)), "village_piazza",
      P1("casanova", ("petru", "+", "is still carrying a bench")),
      "The piazza on the evening of day 35. Everything the village made these last days is here. Madame Casanova takes your arm "
      "before her speech.",
      [G("casanova", "[clear throat] Walk with me, Monsieur. Once around the square. I want to see it with you first.", "pride")],
      [O("Walks with her.", [DIREKT("a3_festa_bauen")])]),
    E("a3_festa_bauen", "gag1", "wholesome", "The Festa: Building", FRAME(), "village_piazza", P1("casanova"),
      "First the things people built: the tables, the stage, the lights over the square.",
      [JE(G("petru", "[sniff] Stella. Marie's boat. Five years on blocks, and tonight she holds the whole village. Marie always fed too many people.", "pride"), "tafel", LOSW("tafel", "boot")),
       JE(G("petru", "[clear throat] Black wood. Last week it was a house. Now people eat on it. That's the sea's way too.", "pride"), "tafel", LOSW("tafel", "asche")),
       JE(G("holm", "[clear throat] Look at the head of the table, Frankfurt. Four gold stripes, nailed into the wood. I sleep on land now.", "pride"), "holmtafel", FL("a3_los_tafel_holm_streifen")),
       JE(G("holm", "[clear throat] My stripes are still on my shoulders. One more season. Then we see. Petru says he'll wait. Petru is good at waiting.", "neutral"), "holmtafel", FL("a3_los_tafel_holm_saison")),
       JE(G("holm", "[chuckle] Petru said one word in the workshop: stay. One word. From him that's a speech.", "love"), "holmtafel", FL("a3_los_tafel_holm_petru")),
       JE(G("petru", "[sigh] And over the table: the net. Every name that spoke is in a knot. Tie well, and the sea keeps it.", "pride"), "netz",
          {"alle": [FL("a3_petru_netz"), {"anzahl": [[FL("a3_zeuge_" + p) for p in ("petru", "mina", "batu", "alva", "anghjulu", "casanova", "sandru")], ">=", 1]}]}),
       JE(G("bonaventure", "[sigh] The stage stands where the fire was. It's the right place.", "remorse"), "buehne", LOSW("buehne", "post")),
       JE(G("bonaventure", "[laugh] In front of the church, where the people are! Look at them all!", "pride"), "buehne", LOSW("buehne", "kirche")),
       JE(G("rosi", "[chuckle] White light. That's your chip up there, Officer.", "pride"), "licht", {"alle": [LOSW("lichter", "chip"), DA("rosi")]}),
       JE(G("rosi", "[laugh] Amber, like Unit-01's eye. Alon's collars are lighting our festa.", "pride"), "licht", {"alle": [LOSW("lichter", "halsband"), DA("rosi")]}),
       JE(G("casanova", "[sigh] Half the lights work. The tables are full anyway.", "neutral"), "licht", NICHT(FL("a3_los_lichter"))),
       JE(G("sandru", "[chuckle] They counted every sweet at the market. Now we eat them. Ha.", "pride"), "system", LOSW("system", "markt")),
       JE(G("sandru", "[sigh] My mother's recipes. Only for us. Try the chebakia.", "caring"), "system", LOSW("system", "festa"))],
      [O("Walks on to the food.", [DIREKT("a3_festa_essen")])]),
    E("a3_festa_essen", "gag1", "wholesome", "The Festa: Food", FRAME(), "village_piazza", P1("casanova"),
      "Then the food. It smells of fish, wild herbs and too much garlic.",
      [JE(G("batu", "[chuckle] My way. Too much, like always.", "pride"), "topf", LOSW("topf", "batu")),
       JE(G("batu", "[sniff] Your mother's way, con. I think she would like it.", "caring"), "topf", LOSW("topf", "mutter")),
       JE(G("lola", "[laugh] Auntie said yes, so the menu is perfect. Official.", "joy"), "menue", LOSW("menue", "batu")),
       JE(G("lola", "[chuckle] The mayor gave my menu a speech. Eleven minutes.", "amusement"), "menue", LOSW("menue", "casanova")),
       JE(G("lola", "[laugh] The Boss tasted it first, and he's still alive!", "joy"), "menue", LOSW("menue", "duc")),
       JE(G("bonaventure", "[laugh] Many small fish from the reef. Enough for everyone!", "joy"), "fang", LOSW("fang", "riff")),
       JE(G("bonaventure", "[laugh] The Señor's big fish! It's on the grill, and it's bigger than Paco.", "joy"), "fang", LOSW("fang", "meer")),
       JE(G("alva", "[sniff] Papa's berry liqueur. One glass on every table.", "sadness"), "drink", LOSW("getraenk", "papa")),
       JE(G("alva", "[laugh] 'The Eventually.' The pirates are crying into it.", "amusement"), "drink", LOSW("getraenk", "eventually")),
       JE(G("alva", "[chuckle] 'Fresh Bread.' Sandru knows why. Nobody else has to.", "embarrassment"), "drink", LOSW("getraenk", "brot")),
       JE(G("nonna", "[chuckle] Herbs on the long table. For everyone.", "caring"), "garten", LOSW("garten", "tafel")),
       JE(G("nonna", "[chuckle] Herbs in Bà Tư's pot. She says it's too much. It's never too much.", "amusement"), "garten", LOSW("garten", "topf")),
       JE(G("nonna", "[chuckle] Basil on the church steps. Don says he doesn't like it. He smells it every time he walks past.", "amusement"), "garten", LOSW("garten", "kirche"))],
      [O("Walks on to the decorations.", [DIREKT("a3_festa_schmuck")])]),
    E("a3_festa_schmuck", "gag1", "wholesome", "The Festa: Decoration", FRAME(), "village_piazza", P1("casanova"),
      "And over everything: what people hung up, painted and sewed.",
      [JE(G("mina", "[chuckle] Every letter nobody could deliver. Now everybody can read them.", "joy"), "girlande", LOSW("girlande", "alle")),
       JE(G("mina", "[sigh] All the letters, except his.", "neutral"), "girlande", LOSW("girlande", "ohne")),
       JE(G("mina", "[chuckle] Flowers. My mother would be proud of me.", "joy"), "girlande", LOSW("girlande", "blumen")),
       JE(G("anghjulu", "[laugh] The bell rings in time! You won the cards, I won the bell.", "joy"), "glocke", LOSW("glocke", "gewinnen")),
       JE(G("anghjulu", "[chuckle] The bell rings in time. You let me win, I know.", "gratitude"), "glocke", LOSW("glocke", "verlieren")),
       JE(G("anghjulu", "[chuckle] We played until the bell was fixed. It is fixed.", "joy"), "glocke", LOSW("glocke", "niemand")),
       JE(G("danzel", "[gasp] My dress, on the dance floor! Nobody spill anything on it!", "nervousness"), "kleid", LOSW("kleider", "crew")),
       JE(G("danzel", "[gasp] Red! The mayor in red! I'm going to faint.", "joy"), "kleid", LOSW("kleider", "casanova")),
       JE(G("jana", "[sniff] The pictures are on the church door. The door the children hid behind.", "caring"), "bilder", LOSW("bilder", "tuer")),
       JE(G("jana", "[laugh] Everybody can see the pictures! The children are so proud.", "joy"), "bilder", LOSW("bilder", "buehne")),
       JE(G("bibi", "[laugh] Capra is wearing a flower crown. She's eating it. It's her festa too.", "joy"), "capra", FL("a3_los_capra_ja")),
       JE(G("casanova", "[laugh] Every name on my board. Every single one. Monsieur, I could kiss you. I won't.", "joy"), "summe",
          {"anzahl": [[FL("a3_los_" + l) for l in LOSE_ALLE], ">=", 11]}),
       JE(G("casanova", "[sigh] Half the board is still empty. It's still our festa.", "neutral"), "summe",
          {"anzahl": [[FL("a3_los_" + l) for l in LOSE_ALLE], "<", 6]})],
      [O("Goes with her to the stage.", [DIREKT("a3_festa_rede")])]),
    E("a3_festa_rede", "gag1", "wholesome", "The Festa", FRAME(), "village_piazza", P1("casanova", ("alva", "?", "is standing at the back")),
      "Madame Casanova climbs onto the stage. The square goes quiet.",
      [JE(G("lea", "[gasp] Did you know she's here? Ligeia. She's singing from the rocks!", "excitement"), "ligeia", FL("a3_ligeia_festa")),
       G("casanova", "[clear throat] Cala d'Orsu has stood on this rock for four hundred years. Pirates came. Tax men came. "
                     "A man with a satellite came. And tonight...", "pride")],
      [O("Waits for the end of her sentence.", [F("akt3_festa"), DIREKT("a3_festa_minicu")])]),
    E("a3_festa_minicu", "gag1", "wholesome", "Minicu", FRAME(), "village_piazza", P1("minicu", ("jana", "+", "screams his name")),
      "Silence. Nobody claps. Then Alva does, slowly. Then a second pair of hands, much too loud. The church door is open. "
      "Minicu stands there with a bandage around his head, and Don holds him up. Kevin lands on his head.",
      [G("jana", "[gasp] Jessas... MINICU!", "surprise"),
       JE(G("lola", "[sniff] Oh, mate. I saved you the leftovers. Twelve days of leftovers.", "joy"), "lola", DA("lola")),
       G("minicu", "[chuckle] Does it hurt? The noise? I can clap quieter.", "joy"),
       G("casanova", "[sniff] ...Thank you. Thank you, Alva. Thank you, Minicu.", "gratitude"),
       G("alva", "[chuckle] Don't get used to it.", "amusement"),
       JE(G("minicu", "[sigh] You came first, when I was on the ground. Before Pascal. I heard you.", "gratitude"), "zuerst", FL("bl_minicu_duc_zuerst")),
       G("minicu", "[clear throat] Is Pascal coming?", "curiosity")],
      [O("“No, Minicu.”", [F("a3_minicu_lebt"), DIREKT("a3_festa_bild")],
         zeile=G("minicu", "[sigh] Okay. Then I stay with you.", "sadness")),
       O("Puts a hand on his shoulder and doesn't answer.", [F("a3_minicu_lebt"), DIREKT("a3_festa_bild")]),
       O("“Not tonight.”", [F("a3_minicu_lebt"), DIREKT("a3_festa_bild")],
         zeile=G("minicu", "[chuckle] Tomorrow, then. I'll wait. I'm good at waiting.", "joy"))],
      sets={"minicu": "minicu_standard", "jana": "jana_deck_a"}),
    E("a3_festa_bild", "gag1", "wholesome", "The Festa", FRAME(), "village_piazza", P1("holm", ("petru", "+", "brings two glasses")),
      "The music starts. The bell rings for the dance.",
      [JE(G("siri", "[sniff] Now I can post it. He's standing.", "joy"), "siri", FL("a3_siri_festa")),
       JE(G("jana", "[chuckle] Madame, sorry, the children want the end of the long story. The one from the church.", "joy"), "casa", FL("bl_kirche_casanova")),
       JE(G("holm", "[chuckle] Mamma, this is Petru. He's the one who taught me to sit still. ...Frankfurt, you can sit with us. At the far end.", "love"), "holm", FL("a3_paar_holm_bank")),
       JE(G("holm", "[chuckle] Mamma, this is Petru. He's the one who taught me to sit still. Frankfurt walked past us once and said nothing. Smart man.", "love"), "holm", FL("a3_paar_holm_still")),
       JE(G("holm", "[chuckle] Mamma, this is Petru. He's the one who taught me to sit still.", "love"), "holm", FL("a3_paar_holm")),
       JE(G("charly", "[sigh] Ten.", "love"), "charly", FL("a3_paar_charly")),
       JE(G("danzel", "[gasp] In public?!", "love"), "danzel", FL("a3_paar_charly")),
       JE(G("charly", "[chuckle] Eleven.", "love"), "charly2", FL("a3_paar_charly")),
       JE(G("bibi", "[laugh] Finally! I had a bet with myself. I won.", "joy"), "bibi", {"alle": [FL("a3_paar_charly"), FL("rt_bibi_bleibt")]}),
       JE(G("danzel", "[gasp] Duc! She gave me a nine, because you said so. Tonight: eleven. Nobody is humble here!", "joy"), "danzel2", FL("a3_paar_charly_neun")),
       JE(G("danzel", "[sniff] You said it was the best ten you ever heard. It still is.", "love"), "danzel2", FL("a3_paar_charly_zehn")),
       JE(G("danzel", "[sniff] You left us alone in the shop. Thank you. I cried into a curtain. It's a good curtain.", "love"), "danzel2", FL("a3_paar_charly_allein")),
       JE(G("laetitia", "[sniff] Papa. You wrote 'I need you'. All my life you never said it.", "love"), "laetitia",
          {"alle": [FL("a3_petru_brief_brauche"), {"eine": [FL("bg_weg_c"), FL("petru_versoehnt")]}]}),
       JE(G("laetitia", "[chuckle] Papa. You asked me to come. So I came. Is there fish pie?", "joy"), "laetitia",
          {"alle": [FL("a3_petru_brief_festa"), {"eine": [FL("bg_weg_c"), FL("petru_versoehnt")]}]}),
       JE(G("laetitia", "[sniff] Papa. A bay leaf in the milk. You remembered Mama's secret. I'm here.", "love"), "laetitia",
          {"alle": [FL("a3_petru_brief_marie"), {"eine": [FL("bg_weg_c"), FL("petru_versoehnt")]}]}),
       JE(G("mina", "[clear throat] Petru! A postcard from the mountains, just now. One line: Me too, Papa.", "joy"), "laetitia", FL("a3_petru_brief")),
       JE(G("ghjuvan", "[sigh] Ghjuvan, from the hills. The red light on the ridge went out. I slept for the first time in a month. So did my sheep.", "relief"), "mast",
          {"alle": [FL("a3_mast_aus"), NICHT(FL("bg_ghjuvan_tot"))]}),
       JE(G("charly", "[clear throat] ...Up there it's still blinking. She's watching. Let her watch this.", "pride"), "mast",
          {"alle": [FL("a3_mast_an"), {"flag": "rt_charly_bleibt"}]}),
       JE(G("lola", "[laugh] Nan's on the phone! Say hello to the whole village, Nan!", "joy"), "nan", FL("a3_paar_lola_nan")),
       JE(G("batu", "[chuckle] She said yes before I changed my mind. I never change my mind. Eat, Lola.", "caring"), "nan", FL("a3_paar_lola_ja")),
       JE(G("batu", "[chuckle] Two plates. One for Lola, one for the Boss. Later is now.", "caring"), "nan", {"eine": [FL("a3_paar_lola_teller"), FL("a3_paar_lola_spaeter")]}),
       JE(G("alva", "[sniff] Come on, Hamburg. Dance. ...She said it to me, you know. Out loud. Ten.", "caring"), "chiara", FL("a3_paar_chiara_sag")),
       JE(G("chiara", "[laugh] A nine, the First Officer said. Best friend at twenty-nine. Dance with me, Alva.", "joy"), "chiara", FL("a3_paar_chiara_neun")),
       JE(G("alva", "[laugh] Hamburg is dancing! Badly! Somebody film this. No, don't.", "joy"), "chiara", {"eine": [FL("a3_paar_chiara_gut"), FL("a3_paar_chiara_alle"), FL("a3_paar_chiara_still")]}),
       JE(G("isabelle", "[chuckle] Rosemary. For your coat, Sophia. ...My first friend outside the walls.", "caring"), "isabelle", FL("a3_paar_sophia_freundin")),
       JE(G("isabelle", "[chuckle] Rosemary. For your coat, Sophia. You told me where you went. I wrote it down.", "caring"), "isabelle", FL("a3_paar_sophia_frag")),
       JE(G("isabelle", "[chuckle] Rosemary. For your coat, Sophia. You said: do it anyway. I'm dancing. Anyway.", "joy"), "isabelle", FL("a3_paar_sophia_ja")),
       JE(G("isabelle", "[chuckle] Rosemary. For your coat, Sophia.", "caring"), "isabelle", FL("a3_paar_sophia")),
       JE(G("maxwell", "[laugh] Bones is on the roof! Number One said a plane is nicer. Number One was right. Mr. Maximum waves.", "joy"), "bones", FL("a3_paar_bones_gleich")),
       JE(G("maxwell", "[laugh] Bones is on the roof! Bones bites, a plane doesn't. Mr. Maximum knows the difference now.", "joy"), "bones", FL("a3_paar_bones_sicher")),
       JE(G("maxwell", "[laugh] Bones is on the roof! Two brave men fed him once. Brother!", "joy"), "bones", FL("a3_paar_bones_hand")),
       JE(G("alva", "[chuckle] Look at Papa's board. ALVA, and next to it: stays. I wonder who wrote that.", "love"), "alva", FL("a3_schluss_alva_0")),
       JE(G("sophia", "[laugh] I'm reading at the festa tonight. My first reading with a yes in my pocket.", "joy"), "sophia", FL("a3_schluss_sophia_0")),
       JE(G("siri", "[sigh] I wrote my own caption tonight. Three words. You don't get to read it.", "caring"), "siri2", FL("a3_schluss_siri_1")),
       JE(G("mina", "[sniff] I opened it. Dumè's letter. ...He says come and visit. I think I'll stay. I think I'll visit.", "joy"), "mina",
          {"eine": [FL("a3_paar_lea_zusammen"), FL("a3_paar_lea_festa")]}),
       JE(G("lea", "[gasp] Did you know Mina will drive to the Azores on a Vespa? She says she's fast. She isn't.", "joy"), "lea2", FL("a3_paar_lea_frei")),
       JE(G("lea", "[laugh] Mina says you're slow on purpose. I told everyone. Sorry. I'm not really sorry.", "joy"), "lea2", {"eine": [FL("a3_paar_lea_langsam"), FL("a3_paar_lea_finger")]})],
      [O("Dances.", [F("a3_festa_fertig")]),
       O("Sits down at the long table and watches everyone.", [F("a3_festa_fertig")])]),
]

# ------------------------------------------------------------------ Mitternacht (Tag 35, Nacht)
MITTERNACHT_ZEILE = {
    "chiara": ("[sigh] Ten. That's a ten, First Officer. Don't let it go to your head. ...Let it go to your head a little.", "love"),
    "alva": ("[chuckle] Only you. Not to everyone. They'd never believe it.", "love"),
    "lea": ("[sigh] The Azores can wait one more night. Two fingers?", "love"),
    "sophia": ("[chuckle] I've lost the bet. Best ten euros I ever lost.", "love"),
    "rosi": ("[sigh] ...Captain. There. I said it. Don't make a face.", "love"),
    "lola": ("[laugh] One song. Mostly one. Sit down, Boss. Properly.", "love"),
    "siri": ("[sigh] No camera. Just this.", "love"),
    "bibi": ("[chuckle] I'm a mess, and you came anyway. Good.", "love"),
    "megan": ("[sigh] We never speak of this. ...Stay a bit.", "desire"),
}
SCHLUSS_ECHO = {'chiara': ['The flashlight, and you let me find the breaker myself.', 'The red one, second row. Show-off.', 'We found it together. In the dark.'], 'alva': ["You wrote 'stays' next to my name. In chalk. Chalk is forever, in my bar.", 'You left the space empty, so I could choose. I chose.', "You gave me the chalk. I wrote it myself. Don't ask what."], 'lea': ["Not fast, but yes. I'm holding you to that.", "You said stay. I'm thinking about it. Very hard.", "Two fingers. That's still an answer."], 'sophia': ["You gave me the letter. It said yes. I'm still shaking.", 'You read the first line out loud. I heard it in your voice. Better.', "It's still closed, in my notebook. Later. Together. Now?"], 'rosi': ["Captain. I said it once. That's the limit.", "Duc. It's still harder than Captain.", "A draw. Nobody won. I can live with that."], 'lola': ['You put your phone away. Nobody does that for me.', "You made me sit down too. I'm sitting. Look.", 'You stirred. Badly. Perfect.'], 'siri': ['No caption. Still none.', 'Siri, in her own words. Here they are.', "You took my hand and didn't answer. Do it again."], 'bibi': ['You let me cut the last collar. Mine.', 'We did it together. His head was so heavy.', 'You gave me the knife without a word. I love that. Still.'], 'megan': ['You already did. Off the record. Still.', 'Duc. There. I said it twice now.', 'You nodded and stayed. Stay again.']}
# Echo-Tags je Zeile (Textpruefung Nr. 77): froehliche Echos lachen, der Rest seufzt
ECHO_TAG = {"The red one, second row. Show-off.": "[chuckle]", "You gave me the knife without a word. I love that. Still.": "[laugh]",
            "You stirred. Badly. Perfect.": "[chuckle]", "Duc. There. I said it twice now.": "[chuckle]",
            "Two fingers. That's still an answer.": "[chuckle]", "A draw. Nobody won. I can live with that.": "[chuckle]",
            "You made me sit down too. I'm sitting. Look.": "[laugh]", "You gave me the chalk. I wrote it myself. Don't ask what.": "[chuckle]"}
MITTERNACHT = [
    E("a3_mitternacht_" + pid, "gag1", "wholesome", "After Midnight",
      PFL(35, "nacht", {"alle": [NICHT(DEAL), FL("a3_mitternacht_" + pid)] + ([FL("megan_zurueck")] if pid == "megan" else [])}), "village_harbour", P1(pid),
      "After midnight. The music from the piazza is quieter down here on the mole. She is already there.",
      [JE(G(pid, ECHO_TAG.get(SCHLUSS_ECHO[pid][n], "[sigh]") + " " + SCHLUSS_ECHO[pid][n], "love" if pid != "megan" else "desire"), "echo", FL("a3_schluss_%s_%d" % (pid, n))) for n in range(3)]
      + [G(pid, MITTERNACHT_ZEILE[pid][0], MITTERNACHT_ZEILE[pid][1])],
      [O("Stays.", [F("a3_mitternacht_fertig")])]) for pid, _n in MN_FRAUEN
] + [
    E("a3_mitternacht_allein", "gag1", "wholesome", "After Midnight", PFL(35, "nacht", {"alle": [NICHT(DEAL), FL("a3_mitternacht_niemand")]}),
      "village_harbour", P1("mina"),
      "After midnight. The mole is empty, and that's fine. Behind you the whole village is still dancing.",
      [G("mina", "[chuckle] Yacht! You're missing the best part. Come back up!", "joy")],
      [O("Goes back up to the piazza.", [F("a3_mitternacht_fertig")])]),
    E("a3_festa_deal", "gag1", "ernst", "The Festa", PFL(35, "abend", DEAL), "village_piazza", P1("casanova"),
      "The festa happens under a white banner with two letters on it. Alon raises a glass from a hologram over the stage. "
      "Rosi doesn't say a word all evening. Minicu carries crates at the harbour, for A.V., and doesn't ask.",
      [G("casanova", "[sigh] ...Cheers, Monsieur.", "sadness")],
      [O("Raises his glass.", [F("a3_festa_fertig"), F("akt3_festa")])]),
]

EVENTS = KOMMISSION + FESTA + MITTERNACHT


def tags_schreiben():
    return tags_fuer(EVENTS, "akt3_finale")
