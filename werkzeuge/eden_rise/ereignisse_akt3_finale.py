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
      [JE(G("petru", "[clear throat] I saw the torches at my workshop. And I saw who stayed. And the village rowed out. Like in 1924.", "neutral"), "petru",
          {"alle": [ZG("petru"), FL("bl_dorf_rudert")]}),
       JE(G("petru", "[clear throat] I saw the torches at my workshop. And I saw who stayed.", "neutral"), "petru", ZG("petru")),
       JE(G("mina", "[sigh] I knocked on every door that day, when the phones were dead. I saw who opened, and who didn't.", "nervousness"), "mina", ZG("mina")),
       JE(G("batu", "[clear throat] Men in white. They asked me twice for the north road. I told Duc then. Now I tell you.", "neutral"), "batu", ZG("batu")),
       JE(G("alva", "[sigh] From the square I saw the north barricade open. Then men in white came through. I saw that with my own eyes.", "neutral"), "alva", ZG("alva")),
       JE(G("sandru", "[clear throat] My name is Iskander. I carried Alva out of the rubble. And the next week, A.V. switched off my legs.", "neutral"), "sandru",
          {"alle": [ZG("sandru"), FL("sandru_herkunft")]}),
       JE(G("sandru", "[clear throat] My name is Sandru. I carried Alva out of the rubble. And the next week, A.V. switched off my legs.", "neutral"), "sandru", ZG("sandru")),
       JE(G("anghjulu", "[clear throat] I saw the gate open. I was sober. Write that down too. It doesn't happen often.", "neutral"), "don",
          {"alle": [ZG("anghjulu"), FL("bl_kirche_don")]}),
       JE(G("anghjulu", "[sigh] I was asleep on the church steps, my son. But I saw the gate open before I fell asleep.", "remorse"), "don",
          {"alle": [ZG("anghjulu"), FL("bl_kirche_don_schlaeft")]}),
       JE(G("anghjulu", "[sigh] I was outside the church door all night. I saw the gate open.", "neutral"), "don", ZG("anghjulu")),
       JE(G("casanova", "[clear throat] Every night someone left his paper on my church steps. I kept all of it. Here it is.", "pride"), "casanova", ZG("casanova")),
       G("bonaventure", "[clear throat] A man named White paid me in clean money, like a bank. I gave the order to burn. I gave the order to stop. "
                        "I am Captain Buenaventura of The Eventually.", "remorse"),
       JE(G("riscossore", "[chuckle] He's telling the truth. It's in my book, page forty-one. A man in prison pays nobody, so I'd like him to stay out.", "neutral"),
          "risc", FL("a3_riscossore_kommt"))],
      [O("Watches the clerk write.", [F("a3_zeuge_bonaventure"), DIREKT("a3_kom_minicu")])]),
    E("a3_kom_minicu", "gag1", "ernst", "The Big Man", FRAME(), "village_harbour", P1("anghjulu"),
      "The older commissioner looks at his list.",
      [G("anghjulu", "[sigh] The man at the gate? The big one? He can't come today.", "sadness")],
      [O("Says nothing. Nobody on the quay asks what that means.", [DIREKT("a3_kom_beweise")])],
      sets={"anghjulu": "anghjulu_standard"}),
    E("a3_kom_beweise", "gag1", "ernst", "Paper", FRAME(), "village_harbour", P1("elsa"),
      "Then the paper. Elsa lays out everything the village has, one piece after the other.",
      [JE(G("elsa", "[clear throat] White's orders from the villa cellar. Day 22, phase 3: torches, houses.", "neutral"), "feuer", FL("a3_beweis_feuer")),
       JE(G("elsa", "[clear throat] A crate of collars from the grotto. Totò kept it for this day.", "neutral"), "kiste", FL("alon_kiste_genutzt")),
       JE(G("siri", "[sigh] My video. No filter, no music. Just what we saw.", "neutral"), "siri", FL("a3_siri_post")),
       JE(G("sophia", "[clear throat] Darling, I wrote down every time and every word I heard on the radio that night. I didn't know why. Now I do.", "neutral"), "sophia", FL("sophia_notizen")),
       JE(G("charly", "[sigh] Twenty-one forty. He said 'tonight'. Seven out of ten for clarity.", "neutral"), "funk", {"eine": [FL("bl_funk_white"), FL("bl_funk_charly")]}),
       JE(G("elsa", "[clear throat] The radio log. Three o'clock, the night of the twenty-second. Two words.", "neutral"), "wache", FL("bl_wache_gesehen")),
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
      P1("casanova", ("alva", "?", "is standing at the back")),
      "The piazza. Lights over the square, tables full anyway. Everything the village made for the festa is here: whatever was "
      "built, cooked and hung up these last days. Madame Casanova climbs onto the stage.",
      [JE(G("bonaventure", "[laugh] The stage holds! I built it myself. Mostly my men.", "pride"), "buehne", FL("a3_los_buehne")),
       JE(G("batu", "[chuckle] The pot is too small. I knew it.", "amusement"), "topf", FL("a3_los_topf")),
       JE(G("alva", "[chuckle] One drink on every table. Don't get used to it.", "amusement"), "drink", FL("a3_los_getraenk")),
       JE(G("lea", "[gasp] Did you know she's here? Ligeia. She's singing from the rocks!", "excitement"), "ligeia", FL("a3_ligeia_festa")),
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
       JE(G("holm", "[chuckle] Mamma, this is Petru. He's the one who taught me to sit still.", "love"), "holm", FL("a3_paar_holm")),
       JE(G("charly", "[sigh] Ten.", "love"), "charly", FL("a3_paar_charly")),
       JE(G("danzel", "[gasp] In public?!", "love"), "danzel", FL("a3_paar_charly")),
       JE(G("charly", "[chuckle] Eleven.", "love"), "charly2", FL("a3_paar_charly")),
       JE(G("bibi", "[laugh] Finally! I had a bet with myself. I won.", "joy"), "bibi", {"alle": [FL("a3_paar_charly"), FL("rt_bibi_bleibt")]}),
       JE(G("mina", "[sniff] I opened it. Dumè's letter. ...He says come and visit. I think I'll stay. I think I'll visit.", "joy"), "mina",
          {"eine": [FL("a3_paar_lea_zusammen"), FL("a3_paar_lea_festa")]})],
      [O("Dances.", [F("a3_festa_fertig")]),
       O("Sits down at the long table and watches everyone.", [F("a3_festa_fertig")])]),
]

# ------------------------------------------------------------------ Mitternacht (Tag 35, Nacht)
MITTERNACHT_ZEILE = {
    "chiara": ("[sigh] Ten. That's a ten, First Officer. Don't let it go to your head. ...Let it go to your head a little.", "love"),
    "alva": ("[chuckle] Only you. Don't tell anyone. They'd never believe it.", "love"),
    "lea": ("[sigh] The Azores can wait one more night. Two fingers?", "love"),
    "sophia": ("[chuckle] I've lost the bet. Best ten euros I ever lost.", "love"),
    "rosi": ("[sigh] ...Captain. There. I said it. Don't make a face.", "love"),
    "lola": ("[laugh] One song. Mostly one. Sit down, Boss. Properly.", "love"),
    "siri": ("[sigh] No camera. Just this.", "love"),
    "bibi": ("[chuckle] I'm a mess, and you came anyway. Good.", "love"),
    "megan": ("[sigh] We never speak of this. ...Stay a bit.", "desire"),
}
MITTERNACHT = [
    E("a3_mitternacht_" + pid, "gag1", "wholesome", "After Midnight",
      PFL(35, "nacht", {"alle": [NICHT(DEAL), FL("a3_mitternacht_" + pid)]}), "village_harbour", P1(pid),
      "After midnight. The music from the piazza is quieter down here on the mole. She is already there.",
      [G(pid, MITTERNACHT_ZEILE[pid][0], MITTERNACHT_ZEILE[pid][1])],
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
