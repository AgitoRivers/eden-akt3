# -*- coding: utf-8 -*-
"""Gag einer Person - 30 Events: eine Person tut etwas, das andere trifft (Buehne, Betroffene oben rechts)."""
from ereignisse_basis import *  # noqa: F401,F403


def P1(handelnd, *betroffen, fern=False):
    p = {"handelnd": handelnd, "betroffen": [{"id": b[0], "ton": b[1], "was": b[2]} for b in betroffen]}
    if fern:
        p["fern"] = True
    return p


TAG = ["fruehstueck", "tag"]
EVENTS = [
    E("g1_pfannkuchen", "gag1", "witzig", "Pancake Portraits", WANN((2, 5), ["fruehstueck"]), "crew_mess",
      P1("lola", ("chiara", "-", "her face is burnt"), ("rosi", "+", "hers is beautiful"), ("toto", "+", "wants seconds")),
      "Lola has baked a pancake portrait of everyone on board, and she was obviously high while doing it. Rosi's "
      "pancake is beautiful. Chiara's face is a slightly burnt circle with a syrup frown.",
      [Z("lola", "I made all of you, out of love and flour! Chiara, yours is very accurate, actually.", "joy"),
       Z("chiara", "Is that supposed to be my face?", "annoyance")],
      [O("Praises Chiara's pancake.", [V("chiara", 4), V("lola", 4)]),
       O("Eats his own portrait first.", [W("moral", 1), V("lola", 6)], zeile=Z("lola", "You ate my heart, Boss. Literally.", "love")),
       O("Asks Lola for a second portrait of Chiara.", [], probe=P("empathy", 11), erfolg=[V("chiara", 6), V("lola", 4)],
         fehlschlag=[V("chiara", -4), V("lola", -4)])],
      sets={"lola": "Galley", "chiara": "Uniform", "rosi": "Engine Room"}),

    E("g1_drohne", "gag1", "witzig", "Megan's Drone", WANN((3, 4), TAG, bed={"nicht": {"flag": "megan_besuch"}}), "aft_deck",
      P1("megan", ("toto", "-", "is being chased"), ("lea", "+", "has a landing net"), ("chiara", "-", "is mortified"), fern=True),
      "A black Eden Group drone is flying an inspection. Megan's voice comes out of its speaker. The drone is "
      "chasing Totò, because he ran off with a crate.",
      [Z("megan", "Mister Esposito. What's in the box? No, don't run. Running is a confession.", "amusement"),
       Z("toto", "It's FISH, signora! Confidential fish!", "fear")],
      [O("Covers for Totò: “It's fish.”", [], probe=P("cunning", 13), erfolg=[V("toto", 6), V("megan", -4)],
         fehlschlag=[V("toto", 4), V("megan", -6), KR(10)]),
       O("Lea catches the drone with the landing net.", [], probe=P("courage", 12), erfolg=[V("lea", 6), W("moral", 1), V("megan", 4), I("drohnen_propeller")],
         fehlschlag=[V("lea", 4), W("moral", 1)], zeile=Z("megan", "Impressive. Give that girl a raise, but not a big one.", "approval")),
       O("Shows the drone what's in the crate.", [V("megan", 6), V("toto", -8), V("chiara", 4), W("moral", -1)])],
      sets={"lea": "Deck", "chiara": "Uniform"}),

    E("g1_reissverschluss", "gag1", "frech", "The Zip", WANN((3, 6), TAG, bed={"wert": ["begehren.rosi", ">=", 3]}),
      "generator_room", P1("rosi", ("toto", "?", "is about to bring coffee"), ("chiara", "-", "doesn't knock")),
      "Rosi is stuck head first in a service hatch. The zip of her coverall has caught. As she crawls back out, the "
      "coverall slides down to her hips. Underneath she's only wearing an old sports bra, and it's sitting crooked.",
      [Z("rosi", "Don't say anything, just pull me out. By the hips. No, the HIPS, Officer.", "embarrassment"),
       Z("rosi", "You're staring, and that's good, because I was starting to think you only liked the engine.", "desire"),
       Z("toto", "Comandante, I bring the coffee and— ah. I bring nothing. I was never here.", "surprise")],
      [O("Pulls her coverall back up, the perfect gentleman.", [V("rosi", 6), B("rosi", 2)]),
       O("Sends everyone out, shuts the door and fixes the zip.", [], probe=P("charm", 12),
         erfolg=[B("rosi", 8), NK("rosi"), EN(-1), MO("undressed", ["rosi"]), GAG("chiara_klopft")], fehlschlag=[B("rosi", 4), GAG("chiara_klopft")],
         zeile=Z("rosi", "It's fixed? Good, then leave it, because I don't think I'm putting it back on. Come here.", "desire")),
       O("“I didn't see a thing.” With a look.", [B("rosi", 4), KL("rosi", "toto", "Duc and Rosi in the generator room")])],
      sets={"rosi": "Engine Room"}, knistern=True,
      nachklang_text="Oil on your fingers, her laugh in the generator room. At breakfast Rosi is wearing a new "
                     "coverall and grinning into her coffee."),

    E("g1_unit01_klonk", "gag1", "witzig", "Rosi vs. Unit-01", WANN((2, 5), TAG), "galley",
      P1("rosi", ("lea", "-", "covered in soot"), ("lola", "-", "cake in danger"), ("chiara", "?", "on her way")),
      "Unit-01 coughed. In front of Totò. Rosi gives the housing one loving whack with her ring spanner. Unit-01 "
      "coughs back: a black cloud of soot through the ventilation shaft, straight into the galley. Lea is standing "
      "there covered in soot, holding half a cake.",
      [Z("rosi", "Unit-01 coughed at me. COUGHED, in front of Totò, so now this is personal.", "anger"),
       Z("lea", "Um. Rosi? There's soot. On me. On the cake. The cake is a chimney now.", "nervousness")],
      [O("“Again. Harder.”", [], probe=P("cunning", 11), erfolg=[V("rosi", 6), GAG("rosi_vs_unit01")],
         fehlschlag=[V("rosi", 4), W("moral", 1), GAG("rosi_vs_unit01")]),
       O("Takes the spanner off her.", [V("rosi", -2), V("chiara", 2), GAG("rosi_vs_unit01")],
         zeile=Z("rosi", "Fine. But she started it.", "annoyance")),
       O("Wipes the soot off Lea and rescues the cake.", [V("lea", 4), W("moral", 1), GAG("rosi_vs_unit01")])],
      gag="rosi_vs_unit01", sets={"rosi": "Engine Room", "lea": "Deck", "lola": "Galley"}),

    E("g1_unit01_staendchen", "gag1", "witzig", "A Serenade for Unit-01", WANN((3, 6), TAG, bed={"flag": "gag_rosi_vs_unit01_1"}),
      "generator_room", P1("rosi", ("toto", "+", "is filming in secret"), ("lea", "+", "sings along")),
      "Rosi has changed tactics. She's singing Unit-01 a Sicilian lullaby, one hand on the housing. She claims "
      "machines listen.",
      [Z("rosi", "My nonna sang this to tractors, and those tractors never died. Shh, she's listening.", "caring"),
       Z("lea", "Can I join in? I know the tune. I don't know the words. I'll make up the words.", "excitement")],
      [O("Sings along.", [V("rosi", 6), V("lea", 4), W("moral", 1), GAG("rosi_vs_unit01")]),
       O("Keeps a straight face and doesn't disturb Rosi.", [V("rosi", 4), GAG("rosi_vs_unit01")]),
       O("Takes Totò's phone before he can film this.", [V("rosi", 6), V("toto", -2), GAG("rosi_vs_unit01")],
         zeile=Z("rosi", "Thank you. If that video exists, Totò, you'll be sleeping in the anchor locker.", "anger"))],
      gag="rosi_vs_unit01", sets={"rosi": "Off Duty", "lea": "Off Duty"}),

    E("g1_kevin_butter", "gag1", "witzig", "Lea Feeds the Seagull", WANN((2, 4), TAG), "sun_deck",
      P1("lea", ("lola", "-", "that was the last butter"), ("toto", "?", "smells a business opportunity")),
      "Lea gave the butter to a fat seagull. The last butter. The seagull is now sitting on the railing, checking "
      "whether there's more.",
      [Z("lea", "He looked so hungry! And now he loves me. Look at him. I'm calling him Kevin.", "joy"),
       Z("lola", "That was the LAST butter, and now Kevin is eating my croissants. Kevin is dead to me.", "anger")],
      [O("“Kevin's part of the crew now.”", [V("lea", 6), V("lola", -4), GAG("kevin")]),
       O("Buys more butter at the village shop.", [G(-15), V("lola", 4), GAG("kevin")]),
       O("Shoos Kevin away.", [], probe=P("courage", 10), erfolg=[V("lola", 4), V("lea", -4), GAG("kevin")],
         fehlschlag=[GAG("kevin"), W("moral", 1)], zeile=Z("lea", "He'll be back. He knows where we live now.", "amusement"))],
      gag="kevin", sets={"lea": "Leopard Bikini", "lola": "Galley"}),

    E("g1_blaskapelle", "gag1", "witzig", "Casanova's Brass Band", WANN((3, 5), ["fruehstueck"]), "foredeck",
      P1("casanova", ("chiara", "-", "still in her pyjamas"), ("siri", "+", "laughs and films"), ("rosi", "-", "has a headache")),
      "Seven in the morning. A fishing boat pulls up alongside the yacht. On it stands Madame Casanova with the "
      "village brass band. They're playing the anthem of Cala d'Orsu. Loudly.",
      [Z("casanova", "Good morning, heroes of the sea! A welcome song! All four verses! Maestro, again from the top!", "excitement"),
       Z("rosi", "It's seven. It's seven in the morning, and I will throw that tuba into the sea.", "anger")],
      [O("Applauds.", [V("casanova", 6), W("ruf", 1), V("rosi", -2), GAG("casanova_kapelle")]),
       O("Sings along, badly but loudly.", [], probe=P("courage", 11), erfolg=[V("casanova", 8), W("moral", 1), GAG("casanova_kapelle"), I("goldfisch")],
         fehlschlag=[W("moral", 1), V("chiara", -2), GAG("casanova_kapelle")]),
       O("Politely asks for a shorter version.", [V("casanova", -2), V("rosi", 4), GAG("casanova_kapelle")])],
      gag="casanova_kapelle", sets={"chiara": "Cabin Night", "siri": "Morning Ritual", "rosi": "Off Duty"}),

    E("g1_fiona_muetze", "gag1", "witzig", "Fiona Eats a Cap", WANN((2, 6), TAG, bed={"flag": "ziege_an_bord"}), "aft_deck",
      P1("toto", ("chiara", "-", "her uniform cap"), ("lola", "+", "thinks it's cute")),
      "Fiona the goat is eating Chiara's uniform cap. Totò is standing next to her, trying to distract her with a "
      "croissant. It isn't working. Fiona wants the cap.",
      [Z("toto", "Fiona, cara, look, a croissant! Butter! Leave the hat! The hat is not food, the hat is a uniform!", "nervousness"),
       Z("chiara", "That goat is eating my career.", "anger")],
      [O("Pulls the cap out of Fiona's mouth.", [], probe=P("courage", 11), erfolg=[V("chiara", 6), GAG("toto_cousin")],
         fehlschlag=[V("chiara", 2), W("moral", 1), GAG("toto_cousin")]),
       O("Promises Chiara a new cap.",
         [VER("chiara", "Duc gets Chiara a new cap", 2, {"item": "eden_cap"}), V("chiara", 4), GAG("toto_cousin")], art="versprechen"),
       O("Lets Fiona eat the cap.", [V("lola", 4), V("toto", 2), V("chiara", -6), GAG("toto_cousin")])],
      gag="toto_cousin", sets={"chiara": "Uniform", "lola": "Off Duty"}),

    E("g1_siri_tanz", "gag1", "wholesome", "Siri Teaches Everyone a Dance", WANN((2, 6), ["tag"], bed={"nicht": {"flag": "yasin_an_deck"}}),
      "sun_deck", P1("siri", ("lea", "+", "learns fast"), ("rosi", "-", "two left feet"), ("toto", "+", "dances surprisingly well")),
      "Yasin is asleep. Siri has put on some music and is teaching the crew a dance. No camera. She laughs out loud, "
      "the way nobody has heard her laugh before.",
      [Z("siri", "Left, left, turn, shoulder. Rosi, the other left. No, the other other left.", "amusement"),
       Z("rosi", "My feet are Sicilian. They don't take orders from Norway.", "annoyance")],
      [O("Dances along.", [V("siri", 6), W("moral", 1), U("siri_marke", 1)]),
       O("Helps Rosi find her other left.", [V("rosi", 4), V("siri", 4)]),
       O("Pays Siri a compliment when she laughs.", [], probe=P("charm", 11), erfolg=[V("siri", 6), B("siri", 4), I("siris_haarband")],
         fehlschlag=[V("siri", 2)]),
       O("Films it for Yasin's channel. He pays well.", [G(100), V("yasin", 4), V("siri", -6), W("moral", -1)])],
      sets={"siri": "Riviera Swim", "lea": "Deck", "rosi": "Swim"}),

    E("g1_chiara_inspektion", "gag1", "witzig", "White Glove Inspection", WANN((2, 6), ["tag"]), "duc_cabin",
      P1("chiara", ("lola", "-", "has hidden crumbs"), ("lea", "-", "sand in her bed")),
      "Chiara is inspecting the crew cabins in white gloves. She has reached your cabin, and she has found something "
      "under the pillow.",
      [Z("chiara", "Crew cabin inspection, and that includes officers. Especially officers. What's this under your pillow?", "curiosity"),
       Z("chiara", "Is this poetry? Did you write poetry about the sea? You rhymed sea with me.", "amusement")],
      [O("“That's not mine.”", [], probe=P("cunning", 13), erfolg=[V("chiara", 2)], fehlschlag=[V("chiara", 4), W("moral", 1)]),
       O("“Read it out loud, if you dare.”", [V("chiara", 6), B("chiara", 2)],
         zeile=Z("chiara", "The sea is wide, the sea is free, and someone should come back to me. Oh no. That's actually sweet.", "embarrassment")),
       O("Hands her the poem from under the pillow.", [V("chiara", 6), I("ducs_gedicht")])],
      sets={"chiara": "Uniform"}),

    E("g1_toto_pizza", "gag1", "witzig", "The Pizza War", WANN((2, 6), ["dinner"]), "aft_deck",
      P1("toto", ("lola", "-", "pineapple ban"), ("rosi", "+", "Sicily vs. Naples"), ("siri", "+", "is hungry")),
      "Totò is baking Neapolitan pizza on the grill. Lola has brought a pineapple. Totò is shielding the grill with "
      "his body.",
      [Z("toto", "Over my dead body. Over my cold, dead, Neapolitan body. No pineapple touches this dough.", "anger"),
       Z("lola", "It's sweet and salty, mate, so it's balance, like yin and yang. Like you and a shower.", "amusement")],
      [O("“Totò's right, Lola. No pineapple on his dough.”", [V("toto", 6), V("lola", -2), V("rosi", 2)]),
       O("A pineapple pizza for Lola, in secret.", [], probe=P("cunning", 11), erfolg=[V("lola", 6), W("moral", 1)],
         fehlschlag=[V("toto", -6), W("moral", 1)]),
       O("“Bake two pizzas, one each, and let a jury decide.”", [W("moral", 1), V("toto", 2), V("lola", 2), V("siri", 2)])],
      sets={"lola": "Off Duty", "rosi": "Off Duty", "siri": "Saint-Tropez '69"}),

    E("g1_yasin_geste", "gag1", "ernst", "Yasin's Grand Gesture", WANN((3, 5), ["abend"], bed={"nicht": {"flag": "siri_frei"}}),
      "sun_deck", P1("yasin", ("siri", "-", "freezes"), ("sophia", "?", "watches closely"), ("lea", "-", "looks away")),
      "Yasin has set out candles in a heart shape on the sun deck. He's filming live. He wants to tell Siri in front "
      "of his followers how much he loves her. Siri stands there and doesn't move.",
      [Z("yasin", "Babe, look at the camera. Two hundred thousand people are watching us. Say you love me back.", "pride"),
       Z("siri", "Yasin. Please. Not like this. Can we just… turn it off?", "fear")],
      [O("Steps between Siri and the camera.", [V("siri", 6), V("yasin", -8), U("siri_marke", 1)], zeile=Z("siri", "Thank you. I couldn't move.", "gratitude")),
       O("Does nothing; that's their business.", [V("yasin", 2), V("siri", -2)]),
       O("Gives Siri a way out: “Siri, Chiara needs you in the pantry.”", [], probe=P("cunning", 11),
         erfolg=[V("siri", 8), U("siri_marke", 1)], fehlschlag=[V("siri", 4), V("yasin", -4)])],
      sets={"siri": "Silver Night", "sophia": "Concierge", "lea": "Off Duty"}),

    E("g1_elsa_schwimmwesten", "gag1", "witzig", "Elsa and the Life Jackets", WANN((3, 6), ["tag"]), "swim_platform",
      P1("elsa", ("toto", "-", "flip-flops, no life jacket"), ("lea", "-", "no life jacket either"), ("chiara", "+", "told them so")),
      "Elsa's patrol boat comes alongside. Totò and Lea are out in the tender. Without life jackets. Elsa holds up "
      "her ticket book and smiles thinly.",
      [Z("elsa", "Two people, one tender, zero life jackets. That's either a crime or a very small miracle.", "amusement"),
       Z("toto", "Lieutenant, the jackets are in our hearts. Spiritually, we are wearing them.", "nervousness")],
      [O("Pays the fine.", [G(-90), V("elsa", 6), V("chiara", 4)]),
       O("Offers Elsa a coffee and talks to her.", [], probe=P("charm", 12), erfolg=[V("elsa", 6), V("toto", 4)],
         fehlschlag=[G(-90), V("elsa", 2)]),
       O("Announces a ship's rule: life jackets are mandatory.", [V("elsa", 8), V("chiara", 4), V("toto", -2), R(3), W("moral", -1)])],
      sets={"lea": "Deck", "chiara": "Uniform"}),

    E("g1_petru_fisch", "gag1", "wholesome", "Petru's Tuna", WANN((3, 6), ["fruehstueck", "tag"], bed={"wert": ["vertrauen.petru", ">=", 1]}),
      "aft_deck", P1("petru", ("lola", "+", "is crying with joy"), ("lea", "-", "can't watch")),
      "Petru comes alongside in his boat and, without a word, throws a tuna onto the deck. A big one. Then he points "
      "at you, and at a knife. He wants you to gut it.",
      [Z("petru", "You. Take the knife. I show you once.", "neutral"),
       Z("lola", "A whole tuna. A WHOLE TUNA. Petru, I love you, marry me. Or just come for dinner.", "joy")],
      [O("Guts the tuna himself, with Petru watching.", [], probe=P("perception", 11), erfolg=[V("petru", 8), W("moral", 1), I("petrus_messer")],
         fehlschlag=[V("petru", 4), W("moral", 1)], zeile=Z("petru", "Good. Not good. But good.", "approval")),
       O("Hands the knife to Lola.", [V("lola", 6), V("petru", 2)]),
       O("Offers Petru money.", [V("petru", -4)], zeile=Z("petru", "Money is for tourists.", "disapproval"))],
      sets={"lola": "Galley", "lea": "Deck"}),

    # 18.10.2026 (neue Tageszaehlung: Party = Tag 1, Holm fliegt am Morgen von Tag 2 aus): Chiara statt Holm
    E("g1_chiara_tender", "gag1", "ernst", "Chiara's Tender Test", WANN((2, 3), ["tag"]), "tender_garage",
      P1("chiara", ("rosi", "?", "is watching"), ("lea", "?", "holds the line"), ("toto", "?", "holds his breath")),
      "Since Holm left, Chiara acts as if she runs the place. She tosses you the keys to the tender. You're to "
      "reverse it into the garage, in front of the crew and without help. She folds her arms and waits.",
      [Z("chiara", "Holm made me do this on my first day. Now it's your turn. Back her in, no help, everybody watching.", "neutral"),
       Z("lea", "You've got this! Probably! I'll hold the line. Mostly.", "nervousness")],
      [O("Takes the keys and reverses the tender in, calm and slow.", [], probe=P("perception", 12), erfolg=[V("chiara", 8), R(5)], fehlschlag=[V("chiara", 2), F("tender_kratzer")],
         zeile=Z("chiara", "Hm. Not bad. Holm would have said that too. Then she'd have found a scratch anyway.", "approval")),
       O("Asks Lea to guide him in.", [V("lea", 6), V("chiara", 4), R(3)],
         zeile=Z("chiara", "Asking for help in front of the crew. Holm would have liked that, and so do I.", "approval")),
       O("Throws the keys back: “Show me, Chiara.”", [], probe=P("courage", 13), erfolg=[V("chiara", 6), B("chiara", 4), W("moral", 1)],
         fehlschlag=[V("chiara", -4)])],
      sets={"chiara": "Uniform", "rosi": "Engine Room", "lea": "Deck"}),

    E("g1_holm_kaffee", "gag1", "wholesome", "A Coffee with Holm", WANN((2, 2), ["fruehstueck"],
      bed={"nicht": {"flag": "holm_evakuiert"}}), "bridge",
      P1("holm", ("chiara", "+", "is secretly pleased")),
      "Holm stands on the bridge with two mugs and hands you one. For a long time she says nothing. She looks out at "
      "the water. Her hand rests on her stomach, as if it hurts.",
      [Z("holm", "Thirty years at sea. You learn to hear a boat. This one sounds tired.", "neutral"),
       Z("holm", "You're good with people, Frankfurt. Be careful. Being liked is not the same as being followed.", "caring")],
      [O("“What would you do differently?”", [V("holm", 6), F("holm_rat")]),
       O("Drinks the coffee in silence.", [V("holm", 4)]),
       O("“You don't look well, Captain.”", [V("holm", 4), F("holm_schmerzen_bemerkt")],
         zeile=Z("holm", "Mind your boat, not my stomach. …Takk.", "embarrassment"))],
      sets={"holm": "Bridge"}),

    E("g1_kalte_dusche", "gag1", "witzig", "The Cold Shower", WANN((2, 6), ["fruehstueck", "tag"]), "crew_corridor",
      P1("rosi", ("siri", "-", "was in the shower"), ("yasin", "-", "complains"), ("lea", "+", "laughs")),
      "Rosi turned off the hot water to save power. Siri was in the shower at the time. The scream echoes through "
      "the whole yacht.",
      [Z("rosi", "Hot water costs power and power is life, but cold water builds character. You're welcome.", "pride"),
       Z("siri", "ROSI! I had conditioner in! I have conditioner in my soul now!", "anger")],
      [O("Hot water on for five minutes.", [V("siri", 4), V("rosi", -2), GAG("kalte_dusche")]),
       O("“Rosi's right, Siri. Cold water it is.”", [V("rosi", 6), V("siri", -4), GAG("kalte_dusche"), W("moral", -1)]),
       O("Brings Siri a towel and tea.", [V("siri", 6), GAG("kalte_dusche")])],
      gag="kalte_dusche", sets={"rosi": "Engine Room", "lea": "Deck"}),

    E("g1_chiara_pause", "gag1", "frech", "Chiara Takes a Break", WANN((3, 6), ["tag"], bed={"wert": ["begehren.chiara", ">=", 2]}),
      "swim_platform", P1("chiara", ("lea", "+", "cheers"), ("toto", "?", "stares"), ("sophia", "+", "grins")),
      "For the first time, Chiara takes a break. She dives off the stern in a white swimsuit. When she climbs back "
      "up, half the crew is staring. She only notices one of them.",
      [Z("chiara", "What? Officers are allowed to swim. Stop staring, all of you. Not you. You can stare.", "embarrassment"),
       Z("sophia", "Chiara has legs. Who knew. Somebody write this down.", "amusement")],
      [O("Dives in after her.", [B("chiara", 6), V("chiara", 4), NK("chiara")],
         zeile=Z("chiara", "Race you to the buoy, and the loser gets dunked. I don't lose.", "desire")),
       O("Holds her towel and looks her in the eye.", [B("chiara", 4), V("chiara", 4)]),
       O("Tells the crew to get back to work.", [V("chiara", 6), R(3), W("moral", -1)])],
      sets={"chiara": "Swim", "lea": "Deck", "sophia": "Swim"}, knistern=True,
      nachklang_text="Water on her skin, her laugh at the buoy. At breakfast Chiara asks, far too matter-of-factly, "
                     "whether you slept well."),

    E("g1_siri_pullover", "gag1", "wholesome", "Siri in a Jumper", WANN((3, 6), ["fruehstueck"], bed={"wert": ["vertrauen.siri", ">=", 3]}),
      "crew_mess", P1("siri", ("yasin", "-", "recognises the jumper"), ("sophia", "+", "sees everything")),
      "Siri comes to breakfast in a grey jumper that's far too big for her. It's your jumper. She took it off the "
      "chair last night and acts as if that were normal.",
      [Z("siri", "It was cold and it was on the chair, and it smells like the sea and coffee. So I'm keeping it.", "embarrassment"),
       Z("sophia", "Interesting choice of knitwear, darling. Very… officer-adjacent.", "amusement")],
      [O("“It looks better on you than on me.”", [V("siri", 6), B("siri", 4), NK("siri"), V("yasin", -4)]),
       O("Acts as if nothing's up.", [V("siri", 4)]),
       O("“I want that back. In person.”", [], probe=P("charm", 12), erfolg=[B("siri", 6), NK("siri")], fehlschlag=[V("siri", 2)],
         zeile=Z("siri", "Come and get it, then. Tonight. If you dare.", "desire"))],
      sets={"siri": "Dad's Sweater", "sophia": "Concierge"}, knistern=True,
      nachklang_text="Your jumper on her. All day you keep finding grey wool fluff on your sleeve, and you smile "
                     "about it."),

    E("g1_sophia_liest_vor", "gag1", "frech", "A Page from Sophia's Notebook", WANN((3, 6), ["abend"]), "main_salon",
      P1("sophia", ("chiara", "-", "recognises herself"), ("rosi", "+", "wants to hear more"), ("lola", "+", "is fanning herself")),
      "Lola has found a loose page from Sophia's notebook and is reading it out to the crew in her most dramatic "
      "voice. A love scene. A strict officer and a first officer on a stranded yacht. It gets very hot, very fast. "
      "Halfway through, Sophia walks in.",
      [Z("lola", "“She pushed him against the chart table. The charts slid to the floor. Nobody cared.” Oh my god. "
                   "Who wrote this?", "desire"),
       Z("chiara", "Stop reading, stop reading right now. Why does the officer have my haircut?", "anger")],
      [O("“Keep reading.”", [V("sophia", 6), B("sophia", 4), V("chiara", -4), W("moral", 1)]),
       O("Takes the page from Lola and gives it back to Sophia.", [V("chiara", 6), V("sophia", -2)]),
       O("Later, alone with Sophia: “How does it end?”", [B("sophia", 6), NK("sophia")],
         zeile=Z("sophia", "Badly for the charts, and very well for everyone else. …It's nothing, darling, just ideas. Come by later, and I'll read you the ending.", "desire"))],
      sets={"sophia": "Writing Night", "chiara": "Service", "rosi": "Off Duty", "lola": "Off Duty"}),

    E("g1_helikopter", "gag1", "witzig", "Megan Lands", WANN((5, 5), ["tag"], bed={"flag": "megan_besuch"}), "sun_deck",
      P1("megan", ("lola", "-", "her towel flies off"), ("chiara", "-", "her hair"), ("toto", "+", "salutes")),
      "The Eden Group helicopter lands on the sun deck. The downdraught rips the towel off Lola, the hairdo off "
      "Chiara and very nearly the shorts off Totò. Megan steps out. Not one hair moves.",
      [Z("megan", "Good afternoon. I see the welcome committee is wearing less than expected. Charming.", "amusement"),
       Z("lola", "My towel! My towel's in Sardinia now! Hi, I'm Lola, I'm the cook, I'm naked.", "embarrassment")],
      [O("Greets Megan formally.", [V("megan", 6), V("chiara", 4), W("moral", -1)]),
       O("Gives Lola his jacket.", [V("lola", 6), V("megan", 4), GAG("megan_lacht")],
         zeile=Z("megan", "A gentleman. How rare. I'll write it in my diary— no, I won't. Ahaha.", "amusement")),
       O("“Welcome to the most beautiful dead yacht in the fleet.”", [], probe=P("charm", 13), erfolg=[V("megan", 8), GAG("megan_lacht")],
         fehlschlag=[V("megan", -4)])],
      sets={"megan": "Inspection", "lola": "Off Duty", "chiara": "Uniform"}),

    E("g1_megan_schach", "gag1", "witzig", "Megan Challenges You", WANN((5, 6), ["abend"], bed={"flag": "megan_besuch"}), "main_salon",
      P1("megan", ("sophia", "+", "bets on you"), ("rosi", "+", "doesn't understand the rules"), ("chiara", "-", "nervous")),
      "Megan sets up a glass chessboard in the salon and challenges you. The crew gathers. Megan has never lost. She "
      "says so three times.",
      [Z("megan", "Chess. You and me. If you win, I owe you a favour. If I win, you owe me one. I always win.", "pride"),
       Z("megan", "Check. No, wait. Not check. You're cleverer than you look. I hate that. I love that.", "surprise")],
      [O("Plays Megan and tries to win.", [], probe=P("cunning", 14), erfolg=[V("megan", 8), F("megan_gefallen"), GAG("megan_lacht")],
         fehlschlag=[V("megan", 4), F("duc_schuldet_megan")]),
       O("Plays Megan and loses on purpose.", [W("moral", -1)], probe=P("cunning", 12), erfolg=[V("megan", 4)], fehlschlag=[V("megan", -6)],
         zeile=Z("megan", "You let me win. Never do that again, I want to beat you properly.", "anger")),
       O("Offers his seat to Sophia.", [V("sophia", 6), V("megan", 4)])],
      sets={"megan": "Inspection", "sophia": "Concierge", "rosi": "Off Duty", "chiara": "Uniform"}),

    E("g1_cousin_schlauchboot", "gag1", "witzig", "The Cousin Comes at Night", WANN((3, 6), ["nacht"], bed={"flag": "gag_toto_cousin_1"}),
      "swim_platform", P1("toto", ("elsa", "?", "has binoculars"), ("lea", "+", "helps carry"), ("chiara", "-", "wakes up")),
      "Totò's cousin comes alongside at night in a rubber dinghy with no lights and starts unloading crates. On the shore "
      "something flashes: Elsa's binoculars.",
      [Z("toto", "Gennaro, piano, piano! Quiet! The whole bay can hear you. And put the goat down, it's not part of the delivery!", "nervousness"),
       Z("lea", "Is this smuggling? Is this real smuggling? Can I carry something?", "excitement")],
      [O("Stows the crates below deck, fast.", [], probe=P("cunning", 12), erfolg=[V("toto", 6), I("cuban_rum"), GAG("toto_cousin")],
         fehlschlag=[V("elsa", -6), V("toto", 4), GAG("toto_cousin"), KR(10)]),
       O("Sends the cousin away.", [V("toto", -4), V("elsa", 2), GAG("toto_cousin")]),
       O("Flashes a torch back at Elsa.", [V("elsa", 4), W("moral", 1), GAG("toto_cousin")],
         zeile=Z("toto", "Why are you signalling the police? Are you flirting with the police? Comandante!", "fear"))],
      gag="toto_cousin", sets={"lea": "Off Duty", "chiara": "Cabin Night"}),

    E("g1_katerfruehstueck", "gag1", "witzig", "Hangover Breakfast", WANN((2, 6), ["fruehstueck"], bed={"flag": "lola_kater"}), "crew_mess",
      P1("lola", ("chiara", "-", "the omelette is salty"), ("rosi", "+", "drinks Lola's coffee"), ("sophia", "?", "watches")),
      "Lola is cooking breakfast in sunglasses. Indoors. She's moving very slowly and speaking very quietly. The "
      "omelette is oversalted. Very.",
      [Z("lola", "Shhh. Everything is loud, the eggs are loud, your face is loud. I love you all. Quietly.", "sadness"),
       Z("chiara", "This omelette has more salt than the Mediterranean.", "disgust")],
      [O("Gives Lola water and quiet, and cooks breakfast himself.", [V("lola", 6), EN(-1), W("moral", 1)]),
       O("Bravely eats the omelette.", [V("lola", 4), V("chiara", -2)], zeile=Z("lola", "You ate it, you're a hero. I'll name a sauce after you.", "gratitude")),
       O("“If you party, you still cook.”", [V("chiara", 4), V("lola", -2), R(3)])],
      sets={"lola": "Galley", "chiara": "Uniform", "rosi": "Engine Room", "sophia": "Concierge"}),

    # Rosis Werkstatt geht wieder auf (25.10.2026, Duc, E-065): Pflicht-Event am Tag 8 (Beginn Akt 2). Die Werkstatt brannte
    # bei der Explosion (E-049); bis hierher ist der Raum gesperrt (modul_eden_rise.py). Setzt "werkstatt_offen" und
    # schaltet in der Kabine "Für Rosi" frei (kern/kampf.py, WERKSTATT in kaempfe_eden_rise.py).
    E("rosi_werkstatt_offen", "gag1", "wholesome", "Rosi's Workshop Is Open Again", WANN((8, 8), ["tag"], pflicht=True),
      "workshop",
      P1("rosi", ("lea", "+", "wants to weld something right now"), ("toto", "-", "is clearing out his crates")),
      "Day eight. For a week Rosi has welded, sanded and sworn behind a tarpaulin. This morning the tarpaulin is gone. "
      "The workshop door stands open, the benches are clean, and on the door there's a strip of red tape with crooked "
      "letters on it: “Open. Mostly.” She holds out a key to you and acts as if it were nothing.",
      [Z("rosi", "It works again, Officer. Every bench, every light, every drawer. The fire took the old one, so I built "
                 "a better one. Don't touch the drawers.", "pride"),
       Z("toto", "I only stored a few boxes in there, Comandante. Temporarily. For years. They're out now. Mostly.",
         "embarrassment"),
       # Chips (Items 25.10., docs/wiki/systeme/aufruestung.md): ab werkstatt_offen nutzbar; jeder Spieler hat nach dem Hafenkampf
       # mindestens einen (Pflichtkaempfe mit Neustart), deshalb ohne Bedingung
       Z("rosi", "And those strange chips you brought back from the harbour, give them here. …See that? There's a "
                 "transmitter in every one. Somebody wanted to steer those animals from very far away.", "realization"),
       Z("rosi", "Not any more. I've cut the transmitters out, so now they only listen to you, and you can pull them out "
                 "whenever you like. That part matters to me.", "pride"),
       # Scout-Chip (26.10.2026, Duc): Rosi hat einen Halsband-Sender umgebaut und naeht ihn gleich in die Jacke
       Z("rosi", "One more thing. I rebuilt one of the collar senders. It doesn't give orders any more, it eavesdrops. "
                 "It's in your jacket now, so out there you'll know who's waiting before they know you're coming.", "pride"),
       Z("rosi", "Bring me your jacket, your weapons and the chips, one piece a night, and I'll text you when it's done. "
                 "And if you want to say thank you, say it fast. I hate it.", "embarrassment")],
      [O("Takes the key and thanks her, fast.", [F("werkstatt_offen"), {"chip": ["scout", 1, "jacke"]}, V("rosi", 6)],
         zeile=Z("rosi", "Good, fast is good. Now go away, I have a bench to christen.", "joy")),
       O("Leaves the key with her: “You rebuilt it. It's yours.”", [F("werkstatt_offen"), {"chip": ["scout", 1, "jacke"]}, V("rosi", 8)],
         zeile=Z("rosi", "…Idiot. Thank you. Now bring me something to fix, I'm already bored.", "gratitude")),
       O("Helps Totò carry his crates out.", [F("werkstatt_offen"), {"chip": ["scout", 1, "jacke"]}, V("rosi", 4), V("toto", 4)],
         zeile=Z("toto", "Comandante, careful, that one is fragile. And that one. They are all fragile. Don't ask.",
                 "nervousness"))],
      sets={"rosi": "Engine Room"}),

]

item("drohnen_propeller", "Propeller von Megans Drohne", "andenken", text="A trophy. Megan wants it back. Never.")
item("ducs_gedicht", "Duc's Poem About the Sea", "geschenk", text="Rhymes sea with me. Chiara loves it, secretly.")
item("petrus_messer", "Petrus altes Fischermesser", "gluecksbringer", effekt={"vorteil": "perception"},
     text="Once a day: advantage on Perception.")
item("goldfisch", "Goldfish in a Water Bag", "geschenk", text="Casanova gives it to “the heroine of the bay”. "
                                                                  "Lea loves it, Chiara hates it.")
item("siris_haarband", "Siris Haarband", "andenken", text="She tucked it into your hair while you were dancing. "
                                                          "Visible in the epilogue.")
