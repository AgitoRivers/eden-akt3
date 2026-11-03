# -*- coding: utf-8 -*-
"""Events fuer Akt 1 (Nacht 24.10.2026, Scheibe 5): Megans taegliche Sprachnachricht und Figuren-Momente aus der
Figuren-Runde (docs/wiki/START.md).

Megan (Duc 22.10.): "Taeglich Megans Handy-Nachricht, jeden Tag wuetender, vorgeneriert und als Sprachnachricht
vertont." Tag 1 ist die Party (exklusiv), das Ultimatum ist der Anruf an Tag 2 - die Nachrichten laufen Tag 2 bis 7
als Pflicht-Events (WANN pflicht=True: kommen garantiert, sobald die Phase beginnt; kern/ereignisse.py). Ab Tag 5
ist Megan an Bord und schickt die Nachricht trotzdem - aus der VIP-Kabine, ein Deck ueber Duc.
Momente: Lola Sprosse 1 (Vorkoster, Lob-Mechanik) und Stufe 2 ihres Bogens ("Service!"), Chiara Stolz-Mechanik
Stufe 1 (Spur: Sternzettel) und Stufe 2 ("Brueckennock bei Nacht")."""
from ereignisse_basis import *  # noqa: F401,F403

H = lambda anrufer, ort: {"anrufer": anrufer, "anrufer_ort": ort, "art": "video"}


def P1(handelnd, *betroffen):
    return {"handelnd": handelnd, "betroffen": [{"id": b[0], "ton": b[1], "was": b[2]} for b in betroffen]}


AN_BORD = {"flag": "megan_besuch"}

EVENTS = [
    # ------------------------------------------------------------------ Megans Sprachnachrichten (Tag 2-7)
    E("mg_tag2", "handy", "witzig", "Voice Message from Megan (1)", WANN((2, 2), ["nacht"], pflicht=True), ORT_DUC,
      H("megan", "megan_office"), "A voice message, 23:58. In the background, the office in Monaco: every light "
                                  "switched off except hers.",
      [Z("megan", "First Officer. It is midnight. I am still in the office. Do you know why? Because my yacht is sitting "
                  "in a bay with no engine and no explanation.", "anger"),
       Z("megan", "And before you check your account: probation rate, First Officer. Half the fee, until you prove "
                  "you're worth the other half.", "annoyance"),       # Gage 125 EUR (Duc 29.10.2026, Brain Trust)
       Z("megan", "Five days. Then I want a name. Goodnight. I won't sleep. Neither should you.", "annoyance")],
      [O("Texts back: “Understood.”", [V("megan", 2)]),
       O("Plays it to Rosi.", [V("rosi", 2), W("moral", 1)],
         zeile=Z("rosi", "No engine. She said no engine. It's an inverter! Somebody tell Monaco it's an inverter!",
                 "annoyance")),
       O("Deletes it and goes to bed.", [EN(1)])],
      sets={"megan": "Boardroom"}),

    E("mg_tag3", "handy", "witzig", "Voice Message from Megan (2)", WANN((3, 3), ["fruehstueck"], pflicht=True), ORT_DUC,
      H("megan", "megan_office"), "A voice message, 06:02. Megan has been up since four. You can hear it.",
      [Z("megan", "Good morning. I made a spreadsheet. It has one column. The column says: who.", "annoyance"),
       Z("megan", "It is empty, First Officer. EMPTY. Four days.", "anger")],
      [O("Texts back: “The column is filling up.”", [V("megan", 2)]),
       O("Sends her a photo of the sunrise.", [V("megan", -2), W("moral", 1)],
         zeile=Z("megan", "Is that a sunrise? Did you send me a SUNRISE? I am adding a second column.", "anger")),
       O("Doesn't answer.", [])],
      sets={"megan": "Boardroom"}),

    E("mg_tag4", "handy", "witzig", "Voice Message from Megan (3)", WANN((4, 4), ["fruehstueck"], pflicht=True), ORT_DUC,
      H("megan", "megan_office"), "A voice message, 07:15. Megan has just come out of a board meeting. In the "
                                  "background, a coffee machine rattles very loudly.",
      [Z("megan", "I just told the board the Eden Bay Weekend is still a success. I said it with a smile. My face "
                  "still hurts.",
         "anger"),
       Z("megan", "Three days. And tell your cook to stop sending me pictures of breakfast. They look good. It is "
                  "unacceptable.", "annoyance")],
      [O("Passes it on to Lola.", [V("lola", 4), V("megan", -2)],
         zeile=Z("lola", "She said they look good? Boss, she said they look GOOD. I'm framing this.", "joy")),
       O("Texts back: “You'll get your name.”", [V("megan", 2), R(-2)]),
       O("Texts back: “You'll get the truth.”", [V("megan", 4), R(2)])],
      sets={"megan": "Boardroom"}),

    E("mg_tag5", "handy", "witzig", "Voice Message from Megan (4)", WANN((5, 5), ["fruehstueck"], pflicht=True), ORT_DUC,
      H("megan", "megan_office"), "A voice message, 07:40. Rotor noise. Megan is shouting over a helicopter.",
      [Z("megan", "I am in a helicopter. I hate helicopters. I hate them less than your reports.", "anger"),
       Z("megan", "Landing at eleven. I want coffee, a clean deck, and nobody smiling at me. Two days.", "annoyance")],
      [O("Lets Chiara know.", [V("chiara", 2), R(2)],
         zeile=Z("chiara", "Eleven. Coffee. Clean deck. No smiling. I can do three of those.", "nervousness")),
       O("Lets Maxwell know.", [V("maxwell", 2), W("moral", 1)],
         zeile=Z("maxwell", "A helicopter? Mr. Maximum will greet it. From behind the anchor locker. Very "
                            "respectfully.", "pride")),
       O("Texts back: “Coffee will be ready.”", [V("megan", 2)])],
      sets={"megan": "Boardroom"}),

    E("mg_tag6", "handy", "witzig", "Voice Message from Megan (5)", WANN((6, 6), ["fruehstueck"], bed=AN_BORD, pflicht=True),
      ORT_DUC, H("megan", "vip_cabin"), "A voice message, 06:30. Sender: the VIP cabin. One deck above you.",
      [Z("megan", "I am one deck above you. This is a voice message because if I walk down those stairs, I will fire "
                  "someone on the way.", "anger"),
       Z("megan", "Tomorrow. Eleven o'clock. The salon. Bring proof. Not feelings.", "annoyance")],
      [O("Goes up the stairs and knocks.", [V("megan", 4)], probe=P("courage", 12), erfolg=[V("megan", 6), R(2)],
         fehlschlag=[V("megan", -2)],
         zeile=Z("megan", "You came up. Nobody comes up. …Sit. You have four minutes.", "curiosity")),
       O("Texts back: “Eleven o'clock.”", [V("megan", 2)]),
       O("Plays the message to Totò.", [V("toto", 2), W("moral", 1)],
         zeile=Z("toto", "Comandante, I run a book. Odds she fires somebody before lunch: two to one. You want in?",
                 "amusement"))],
      sets={"megan": "Inspection"}),

    E("mg_tag7", "handy", "ernst", "Voice Message from Megan (6)", WANN((7, 7), ["fruehstueck"], bed=AN_BORD, pflicht=True),
      ORT_DUC, H("megan", "vip_cabin"), "A voice message, 07:00. No shouting. That's worse.",
      [Z("megan", "Good morning. Today I listen. Only today.", "neutral"),
       Z("megan", "Make it count, First Officer.", "neutral")],
      [O("Takes a deep breath.", [EN(1)]),
       O("Texts back: “I will.”", [V("megan", 2)])],
      sets={"megan": "Inspection"}),

    # ------------------------------------------------------------------ Maxwell: erste Lektion (Tag 2) und Training
    E("mx_tutorial", "gag1", "witzig", "Lesson One", WANN((2, 2), ["nachmittag"], pflicht=True),
      "sun_deck", P1("maxwell", ("lea", "+", "cheers you on"), ("toto", "?", "takes bets")),
      "Maxwell stands at the top of the sun deck with towels over his shoulders, waving you up. Half the crew is "
      "hanging over the railing to watch.",
      [Z("maxwell", "Number One! The sea took our engine, brother, but not our muscles. Mr. Maximum is going to "
                    "teach you to fight, and lesson one starts right now!",
         "excitement"),
       Z("toto", "Two to one on the gigante. Comandante, please don't make me rich.", "amusement")],
      [O("“Show me, Mr. Maximum.”", [V("maxwell", 2), {"kampf": "maxwell_tutorial"}],
         zeile=Z("maxwell", "MAXIMUM! That's the spirit, brother!", "joy")),
       O("Joins his warm-up push-ups first.", [V("maxwell", 4), W("moral", 1), {"kampf": "maxwell_tutorial"}],
         zeile=Z("maxwell", "Ten for you, twenty for Mr. Maximum! Now we fight!", "pride"))],
      sets={"lea": "Deck"}),

    E("mx_jana_bewundert", "gag1", "frech", "Jana Is Watching", WANN((3, 6), ["tag", "nachmittag", "dinner"],
                                                                 bed={"flag": "training_siege_10"}),
      "sun_deck", P1("jana", ("maxwell", "+", "grins"), ("chiara", "?", "raises an eyebrow")),
      "Your tenth win against Maxwell. Down at the railing stands Jana with two bottles of water, forgetting that "
      "one of them was meant for Maxwell. She turns red when you look at her.",
      [Z("jana", "Sorry, I– that was really– you just– I brought water. For you. Both. Both are for you.", "embarrassment"),
       Z("maxwell", "Mr. Maximum sees everything, little sister. Mr. Maximum also sees that Mr. Maximum gets no "
                    "water.", "amusement")],
      [O("Takes a bottle and winks at her.", [V("jana", 4), F("jana_bewundert")],
         zeile=Z("jana", "Na geh… okay. Okay. I'm going to go and stand somewhere else now.", "joy")),
       O("Offers to let her join the next training session.", [V("jana", 6), V("maxwell", 2)],
         zeile=Z("jana", "Me? Fighting? …Will you show me how to stand like that?", "excitement")),
       O("Gives Maxwell the second bottle.", [V("maxwell", 4), W("moral", 1)],
         zeile=Z("maxwell", "THANK you, brother. Jana, Mr. Maximum forgives you.", "joy"))]),

    E("mx_chiara_lacht", "gag1", "witzig", "Chiara Was Watching", WANN((3, 6), ["tag", "nachmittag", "dinner"],
                                                                     bed={"flag": "training_niederlagen_3"}),
      "sun_deck", P1("chiara", ("maxwell", "?", "wants to mediate")),
      "Your third defeat. You're lying on the teak, looking up at the sky. A shadow falls over you: Chiara, arms "
      "folded, uniform immaculate. She saw everything.",
      [Z("chiara", "First Officer. You are aware that he's on our side? He was going easy on you. I could tell.", "amusement"),
       Z("maxwell", "Mr. Maximum was NOT going easy. Mr. Maximum was going… medium.", "nervousness")],
      [O("“Then you show me how it's done.”", [V("chiara", 2), B("chiara", 2)],
         zeile=Z("chiara", "In this uniform? Absolutely not. …Tomorrow at seven, and don't be late.", "pride")),
       O("Stays lying there and laughs along.", [V("chiara", 4), W("moral", 1)],
         zeile=Z("chiara", "…Fine, that was funny. Now get up, you're lying on my clean deck.", "joy")),
       O("Gets up, offended.", [V("chiara", -2)],
         zeile=Z("chiara", "Oh no. I hurt the First Officer's feelings. I'll put it in the log.", "amusement"))]),

    # ------------------------------------------------------------------ Lola: Sprosse 1 (Vorkoster) und „Service!“
    E("ak_lola_vorkoster", "gag1", "wholesome", "The Taster", WANN((3, 5), ["dinner"], bed={"wert": ["vertrauen.lola", ">=", 1]}),
      "galley", P1("lola", ("rosi", "?", "sniffs the air"), ("maxwell", "+", "waits with a plate")),
      "Lola holds out a spoon to you before the food goes out. There's a sticker on the cooker hood: NO TWEEZERS. "
      "She looks at you as if a verdict were about to fall.",
      [Z("lola", "Okay, Boss. Taste. Be honest. No, don't be honest. Yes, be honest.", "nervousness"),
       Z("maxwell", "Mr. Maximum volunteers as second taster. Mr. Maximum is very brave.", "pride")],
      [O("Praises it loudly in front of the whole crew.", [V("lola", 4), B("lola", 4), W("moral", 1)],
         zeile=Z("lola", "Did you hear that? Everybody hear that? Okay. Okay. I'm fine. I'm not crying, it's the onions.",
                 "joy")),
       O("Quietly: “That's really good.”", [V("lola", 4), B("lola", 2)],
         zeile=Z("lola", "…Yeah? Okay. Okay, cool. Cool cool cool.", "love")),
       O("Critiques it like a star chef.", [V("lola", -4)],
         zeile=Z("lola", "Yes, Chef. …Sorry. Habit. Old kitchen. Forget it.", "fear"))],
      sets={"lola": "Galley"}),

    E("ak_lola_service", "gag1", "ernst", "“Service!”", WANN((5, 6), ["dinner"], bed=AN_BORD),
      "galley", P1("megan", ("lola", "-", "freezes"), ("chiara", "?", "holds the plates")),
      "Megan claps her hands in the galley: dinner for four, right now, like in a restaurant. Someone shouts "
      "“Service!” Lola stands still, the spoon in her hand. She isn't breathing.",
      [Z("megan", "Service! Four plates, now. Chop chop. This is a yacht, not a hippie commune.", "annoyance"),
       Z("lola", "Yes, Chef. Yes, Chef. Yes, Chef.", "fear")],
      [O("“I'll take over.”", [V("megan", 2), R(1)],
         zeile=Z("lola", "…Thanks, Boss. I just need a minute. Just a minute.", "relief")),
       O("“Lola, pull yourself together.”", [V("lola", -2), W("moral", -1)],
         zeile=Z("lola", "Yes, Chef.", "fear")),
       O("“Everybody out. Lola, breathe.”", [V("lola", 6), V("megan", -2), F("lola_bogen")],
         zeile=Z("lola", "…Sydney. It was a kitchen in Sydney. Nobody ever said it was good. Not once. Can I tell you "
                         "later? When she's gone?", "grief"))],
      sets={"lola": "Galley", "megan": "Inspection", "chiara": "Service"}),

    # ------------------------------------------------------------------ Chiara: Stolz-Mechanik Stufe 1 und 2
    E("ak_chiara_sternzettel", "gag1", "wholesome", "A Page Full of Stars", WANN((3, 5), ["fruehstueck"]),
      "bridge", P1("chiara", ("lola", "?", "whispers")),
      "On the chart table lies a sheet of paper covered in tiny writing: angles, times, and one circled word – "
      "Polaris. Chiara's handwriting. Lola leans over to you.",
      [Z("lola", "Psst. Light on the bridge wing, two in the morning, every night. Somebody's studying. You didn't "
                 "hear it from me.", "curiosity"),
       Z("chiara", "That's mine. That's nothing. That's… a shopping list.", "embarrassment")],
      [O("Hands the page back without asking.", [V("chiara", 4), F("chiara_lernt_bekannt")],
         zeile=Z("chiara", "…Thank you.", "relief")),
       O("“A shopping list with Polaris on it?”", [B("chiara", 2), F("chiara_lernt_bekannt")],
         zeile=Z("chiara", "Polaris is a very popular brand of… rice. Goodbye.", "embarrassment"))],
      sets={"chiara": "Uniform", "lola": "Galley"}),

    E("ak_chiara_brueckennock", "gag1", "wholesome", "The Bridge Wing at Night",
      WANN((4, 6), ["nacht"], bed={"alle": [{"flag": "chiara_lernt_bekannt"}, {"wert": ["vertrauen.chiara", ">=", 3]}]}),
      "bridge", P1("chiara", ("lea", "?", "is asleep on deck")),
      "Two in the morning. A torch is burning on the bridge wing. Chiara is measuring the sky with an old sextant, "
      "her lips moving. She hasn't seen you yet.",
      [Z("chiara", "Thirty-nine… no. Forty-one. Again.", "annoyance"),
       Z("chiara", "How long have you been standing there? Don't answer that.", "embarrassment")],
      [O("“I didn't see anything.”", [V("chiara", 2)],
         zeile=Z("chiara", "Good. Neither did I. Goodnight, First Officer.", "relief")),
       O("“Do you want some help?”", [B("chiara", 2)],
         zeile=Z("chiara", "I don't need help. I need… nothing. Goodnight.", "annoyance")),
       O("“Will you show me how you do that?”", [V("chiara", 6), B("chiara", 2), F("chiara_bogen")],
         zeile=Z("chiara", "…You want to learn? From me? Fine. That's Polaris. And I failed the theory exam in "
                           "April. Don't tell anyone.", "love"))],
      sets={"chiara": "Bridge Night"}, knistern=True,
      nachklang_text="In the morning the page of stars is lying at your place in the mess. At the bottom she has "
                     "added something: “Night 2?”"),
]
