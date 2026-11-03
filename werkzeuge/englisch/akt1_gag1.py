# -*- coding: utf-8 -*-
"""English rewrite · single-character gag events (ereignisse_gag1.py), 25.10.2026.

SPRECHER: speaker changes the AST takeover cannot do (done by hand): key -> new speaker.
"""

SPRECHER = {"g1_sophia_liest_vor#z0": "lola"}       # K7: Sophia's writing stays secret, Lola reads a stolen page

NEU = {
    "g1_pfannkuchen.titel": "Pancake Portraits",
    "g1_pfannkuchen.lage": "Lola has baked a pancake portrait of everyone on board, and she was obviously high while "
                           "doing it. Rosi's pancake is beautiful. Chiara's face is a slightly burnt circle with a "
                           "syrup frown.",
    "g1_pfannkuchen.betroffen.chiara": "her face is burnt",
    "g1_pfannkuchen.betroffen.rosi": "hers is beautiful",
    "g1_pfannkuchen.betroffen.toto": "wants seconds",
    "g1_pfannkuchen#z0": "I made all of you! Out of love! And flour! Chiara, yours is very accurate, actually.",
    "g1_pfannkuchen#z1": "Is that supposed to be my face?",
    "g1_pfannkuchen.o0": "Praises Chiara's pancake.",
    "g1_pfannkuchen.o1": "Eats your own first.",
    "g1_pfannkuchen#o1": "You ate my heart, Boss. Literally.",
    "g1_pfannkuchen.o2": "Asks Lola for a second portrait of Chiara.",

    "g1_drohne.titel": "Megan's Drone",
    "g1_drohne.lage": "A black Eden Group drone is flying an inspection. Megan's voice comes out of its speaker. The "
                      "drone is chasing Totò, because he ran off with a crate.",
    "g1_drohne.betroffen.toto": "is being chased",
    "g1_drohne.betroffen.lea": "has a landing net",
    "g1_drohne.betroffen.chiara": "is mortified",
    "g1_drohne#z0": "Mister Esposito. What's in the box? No, don't run. Running is a confession.",
    "g1_drohne#z1": "It's FISH, signora! Confidential fish!",
    "g1_drohne.o0": "Covers for Totò: “It's fish.”",
    "g1_drohne.o1": "Lea catches the drone with the landing net.",
    "g1_drohne#o1": "Impressive. Give that girl a raise. Not a big one.",
    "g1_drohne.o2": "Shows the drone what's in the crate.",

    "g1_reissverschluss.titel": "The Zip",
    "g1_reissverschluss.lage": "Rosi is stuck head first in a service hatch. The zip of her coverall has caught. As "
                               "she crawls back out, the coverall slides down to her hips. Underneath she's only "
                               "wearing an old sports bra, and it's sitting crooked.",
    "g1_reissverschluss.betroffen.toto": "is about to bring coffee",
    "g1_reissverschluss.betroffen.chiara": "doesn't knock",
    "g1_reissverschluss#z0": "Don't. Say. Anything. Just pull me out. By the hips. No, the HIPS, Officer.",
    "g1_reissverschluss#z1": "You're staring. Good. I was starting to think you only liked the engine.",
    "g1_reissverschluss#z2": "Comandante, I bring the coffee and— ah. I bring nothing. I was never here.",
    "g1_reissverschluss.o0": "Pulls her coverall back up, the perfect gentleman.",
    "g1_reissverschluss.o1": "Sends everyone out, shuts the door and fixes the zip.",
    "g1_reissverschluss#o1": "It's fixed? Good. Leave it. I don't think I'm putting it back on. Come here.",
    "g1_reissverschluss.o2": "“I didn't see a thing.” With a look.",

    "g1_unit01_klonk.titel": "Rosi vs. Unit-01",
    "g1_unit01_klonk.lage": "Unit-01 coughed. In front of Totò. Rosi gives the housing one loving whack with her ring "
                            "spanner. Unit-01 coughs back: a black cloud of soot through the ventilation shaft, straight "
                            "into the galley. Lea is standing there covered in soot, holding half a cake.",
    "g1_unit01_klonk.betroffen.lea": "covered in soot",
    "g1_unit01_klonk.betroffen.lola": "cake in danger",
    "g1_unit01_klonk.betroffen.chiara": "on her way",
    "g1_unit01_klonk#z0": "Unit-01 coughed at me. COUGHED. In front of Totò. This is personal now.",
    "g1_unit01_klonk#z1": "Um. Rosi? There's soot. On me. On the cake. The cake is a chimney now.",
    "g1_unit01_klonk.o0": "“Again. Harder.”",
    "g1_unit01_klonk.o1": "Takes the spanner off her.",
    "g1_unit01_klonk#o1": "Fine. But he started it.",
    "g1_unit01_klonk.o2": "Wipes the soot off Lea and rescues the cake.",

    "g1_unit01_staendchen.titel": "A Serenade for Unit-01",
    "g1_unit01_staendchen.lage": "Rosi has changed tactics. She's singing Unit-01 a Sicilian lullaby, one hand on "
                                 "the housing. She claims machines listen.",
    "g1_unit01_staendchen.betroffen.toto": "is filming in secret",
    "g1_unit01_staendchen.betroffen.lea": "sings along",
    "g1_unit01_staendchen#z0": "My nonna sang this to tractors. The tractors never died. Shh. He's listening.",
    "g1_unit01_staendchen#z1": "Can I join in? I know the tune. I don't know the words. I'll make up the words.",
    "g1_unit01_staendchen.o0": "Sings along.",
    "g1_unit01_staendchen.o1": "Keeps a straight face and doesn't disturb Rosi.",
    "g1_unit01_staendchen.o2": "Takes Totò's phone away.",
    "g1_unit01_staendchen#o2": "Thank you. If that video exists, Totò, you'll be sleeping in the anchor locker.",

    "g1_kevin_butter.titel": "Lea Feeds the Seagull",
    "g1_kevin_butter.lage": "Lea gave the butter to a fat seagull. The last butter. The seagull is now sitting on the "
                            "railing, checking whether there's more.",
    "g1_kevin_butter.betroffen.lola": "that was the last butter",
    "g1_kevin_butter.betroffen.toto": "smells a business opportunity",
    "g1_kevin_butter#z0": "He looked so hungry! And now he loves me. Look at him. I'm calling him Kevin.",
    "g1_kevin_butter#z1": "That was the LAST butter. Kevin is eating my croissants. Kevin is dead to me.",
    "g1_kevin_butter.o0": "“Kevin's part of the crew now.”",
    "g1_kevin_butter.o1": "Buys more butter at the village shop.",
    "g1_kevin_butter.o2": "Shoos Kevin away.",
    "g1_kevin_butter#o2": "He'll be back. He knows where we live now.",

    "g1_blaskapelle.titel": "Casanova's Brass Band",
    "g1_blaskapelle.lage": "Seven in the morning. A fishing boat pulls up alongside the yacht. On it stands Madame "
                           "Casanova with the village brass band. They're playing the anthem of Cala d'Orsu. Loudly.",
    "g1_blaskapelle.betroffen.chiara": "still in her pyjamas",
    "g1_blaskapelle.betroffen.siri": "laughs and films",
    "g1_blaskapelle.betroffen.rosi": "has a headache",
    "g1_blaskapelle#z0": "Good morning, heroes of the sea! A welcome song! All four verses! Maestro, again from the "
                         "top!",
    "g1_blaskapelle#z1": "It's seven. It's seven in the morning. I will throw that tuba into the sea.",
    "g1_blaskapelle.o0": "Applauds.",
    "g1_blaskapelle.o1": "Sings along, badly but loudly.",
    "g1_blaskapelle.o2": "Politely asks for a shorter version.",

    "g1_fiona_muetze.titel": "Fiona Eats a Cap",
    "g1_fiona_muetze.lage": "Fiona the goat is eating Chiara's uniform cap. Totò is standing next to her, trying to "
                            "distract her with a croissant. It isn't working. Fiona wants the cap.",
    "g1_fiona_muetze.betroffen.chiara": "her uniform cap",
    "g1_fiona_muetze.betroffen.lola": "thinks it's cute",
    "g1_fiona_muetze#z0": "Fiona, cara, look, a croissant! Butter! Leave the hat! The hat is not food, the hat is a "
                          "uniform!",
    "g1_fiona_muetze#z1": "That goat is eating my career.",
    "g1_fiona_muetze.o0": "Rescues the cap.",
    "g1_fiona_muetze.o1": "Promises Chiara a new cap.",
    "g1_fiona_muetze.o2": "Lets Fiona have it.",

    "g1_lola_yoga.titel": "Sunrise Yoga",
    "g1_lola_yoga.lage": "Lola is doing yoga on the foredeck. At sunrise. In a bikini made of roughly three strings. "
                         "Suddenly the crew has a great deal to do on the foredeck.",
    "g1_lola_yoga.betroffen.rosi": "drops her coffee",
    "g1_lola_yoga.betroffen.chiara": "sees everything",
    "g1_lola_yoga.betroffen.toto": "is praying",
    "g1_lola_yoga#z0": "Morning, lovelies! Downward dog! It opens the heart chakra. And the hamstrings. Mostly the "
                       "hamstrings.",
    "g1_lola_yoga#z1": "Lola. Clothes. The coast guard has binoculars.",
    "g1_lola_yoga.o0": "Joins in.",
    "g1_lola_yoga#o0": "Look at you bending! Boss, you've got hidden depths.",
    "g1_lola_yoga.o1": "Brings Lola a towel.",
    "g1_lola_yoga.o2": "Enjoys the coffee in peace and watches.",

    "g1_siri_tanz.titel": "Siri Teaches Everyone a Dance",
    "g1_siri_tanz.lage": "Yasin is asleep. Siri has put on some music and is teaching the crew a dance. No camera. "
                         "She laughs out loud, the way nobody has heard her laugh before.",
    "g1_siri_tanz.betroffen.lea": "learns fast",
    "g1_siri_tanz.betroffen.rosi": "two left feet",
    "g1_siri_tanz.betroffen.toto": "dances surprisingly well",
    "g1_siri_tanz#z0": "Left, left, turn, shoulder. Rosi, the other left. No, the other other left.",
    "g1_siri_tanz#z1": "My feet are Sicilian. They don't take orders from Norway.",
    "g1_siri_tanz.o0": "Dances along.",
    "g1_siri_tanz.o1": "Helps Rosi.",
    "g1_siri_tanz.o2": "Pays Siri a compliment when she laughs.",

    "g1_chiara_inspektion.titel": "White Glove Inspection",
    "g1_chiara_inspektion.lage": "Chiara is inspecting the crew cabins. In white gloves. She has reached your cabin. "
                                 "She has found something under the pillow.",
    "g1_chiara_inspektion.betroffen.lola": "has hidden crumbs",
    "g1_chiara_inspektion.betroffen.lea": "sand in her bed",
    "g1_chiara_inspektion#z0": "Crew cabin inspection. Officers included. Especially officers. What's this under your "
                               "pillow?",
    "g1_chiara_inspektion#z1": "Is this poetry? Did you write poetry? About the sea? You rhymed sea with me.",
    "g1_chiara_inspektion.o0": "“That's not mine.”",
    "g1_chiara_inspektion.o1": "“Read it out loud, if you dare.”",
    "g1_chiara_inspektion#o1": "The sea is wide, the sea is free, and someone should come back to me. Oh no. That's "
                               "actually sweet.",
    "g1_chiara_inspektion.o2": "Gives her the poem.",

    "g1_sophia_tischordnung.titel": "Sophia's Seating Plan",
    "g1_sophia_tischordnung.lage": "Sophia did the place cards. Purely by chance, you're sitting between two women who "
                                   "can't stand each other when it comes to you. Sophia smiles very innocently.",
    "g1_sophia_tischordnung.betroffen.chiara": "is suddenly next to you",
    "g1_sophia_tischordnung.betroffen.lea": "on your other side",
    "g1_sophia_tischordnung.betroffen.rosi": "at the far end",
    "g1_sophia_tischordnung#z0": "The seating is purely logistical, darling. I would never. Please, sit. Enjoy. Be "
                                 "charming. In both directions.",
    "g1_sophia_tischordnung#z1": "Why am I at the end, next to the bread basket? What did the bread basket do?",
    "g1_sophia_tischordnung.o0": "Charming in both directions.",
    "g1_sophia_tischordnung.o1": "Goes and sits with Rosi at the end.",
    "g1_sophia_tischordnung.o2": "Confronts Sophia: “What's this about?”",
    "g1_sophia_tischordnung#o2": "Research. Purely sociological. You're my favourite subject. Don't let it go to your "
                                 "head.",

    "g1_qualle.titel": "Lea and the Jellyfish",
    "g1_qualle.lage": "Lea caught a jellyfish in a bucket to show everyone. Totò looked in. Too close. Now he has a red "
                      "welt across his nose and is swearing in Neapolitan.",
    "g1_qualle.betroffen.toto": "got stung",
    "g1_qualle.betroffen.lola": "knows a home remedy",
    "g1_qualle#z0": "She's beautiful, right? Look how she glows! Totò, not so close— oh. Oh no.",
    "g1_qualle#z1": "My NOSE! She kissed my nose with fire! Somebody, vinegar! Lemon! A priest!",
    "g1_qualle.o0": "Fetches vinegar.",
    "g1_qualle.o1": "Asks Lola.",
    "g1_qualle#o1": "Old Aussie remedy: we pee on it. No? Okay, vinegar. Boring, but okay.",
    "g1_qualle.o2": "Takes the jellyfish back to the sea with Lea.",

    "g1_toto_pizza.titel": "The Pizza War",
    "g1_toto_pizza.lage": "Totò is baking Neapolitan pizza on the grill. Lola has brought a pineapple. Totò is shielding "
                          "the grill with his body.",
    "g1_toto_pizza.betroffen.lola": "pineapple ban",
    "g1_toto_pizza.betroffen.rosi": "Sicily vs. Naples",
    "g1_toto_pizza.betroffen.siri": "is hungry",
    "g1_toto_pizza#z0": "Over my dead body. Over my cold, dead, Neapolitan body. No pineapple touches this dough.",
    "g1_toto_pizza#z1": "It's sweet and salty, mate. It's balance. Like yin and yang. Like you and a shower.",
    "g1_toto_pizza.o0": "Totò's right.",
    "g1_toto_pizza.o1": "A pineapple pizza for Lola, in secret.",
    "g1_toto_pizza.o2": "Two pizzas and a jury.",

    "g1_yasin_geste.titel": "Yasin's Grand Gesture",
    "g1_yasin_geste.lage": "Yasin has set out candles in a heart shape on the sun deck. He's filming live. He wants to "
                           "tell Siri in front of his followers how much he loves her. Siri stands there, frozen.",
    "g1_yasin_geste.betroffen.siri": "freezes",
    "g1_yasin_geste.betroffen.sophia": "watches closely",
    "g1_yasin_geste.betroffen.lea": "looks away",
    "g1_yasin_geste#z0": "Babe, look at the camera. Two hundred thousand people are watching us. Say you love me back.",
    "g1_yasin_geste#z1": "Yasin. Please. Not like this. Can we just… turn it off?",
    "g1_yasin_geste.o0": "Steps in.",
    "g1_yasin_geste#o0": "Thank you. I couldn't move.",
    "g1_yasin_geste.o1": "Does nothing; that's their business.",
    "g1_yasin_geste.o2": "Gives Siri a way out: “Siri, Chiara needs you in the pantry.”",

    "g1_elsa_schwimmwesten.titel": "Elsa and the Life Jackets",
    "g1_elsa_schwimmwesten.lage": "Elsa's patrol boat comes alongside. Totò and Lea are out in the tender. Without "
                                  "life jackets. Elsa holds up her ticket book and smiles thinly.",
    "g1_elsa_schwimmwesten.betroffen.toto": "flip-flops, no life jacket",
    "g1_elsa_schwimmwesten.betroffen.lea": "no life jacket either",
    "g1_elsa_schwimmwesten.betroffen.chiara": "told them so",
    "g1_elsa_schwimmwesten#z0": "Two people, one tender, zero life jackets. That's either a crime or a very small "
                                "miracle.",
    "g1_elsa_schwimmwesten#z1": "Lieutenant, the jackets are in our hearts. Spiritually, we are wearing them.",
    "g1_elsa_schwimmwesten.o0": "Pays the fine.",
    "g1_elsa_schwimmwesten.o1": "Offers Elsa a coffee and talks to her.",
    "g1_elsa_schwimmwesten.o2": "Announces a ship's rule: life jackets are mandatory.",

    "g1_petru_fisch.titel": "Petru's Tuna",
    "g1_petru_fisch.lage": "Petru comes alongside in his boat and, without a word, throws a tuna onto the deck. A big "
                           "one. Then he points at you, and at a knife. He wants you to gut it.",
    "g1_petru_fisch.betroffen.lola": "is crying with joy",
    "g1_petru_fisch.betroffen.lea": "can't watch",
    "g1_petru_fisch#z0": "You. Take the knife. I show you once.",
    "g1_petru_fisch#z1": "A whole tuna. A WHOLE TUNA. Petru, I love you. Marry me. Or just come for dinner.",
    "g1_petru_fisch.o0": "Guts it under Petru's eye.",
    "g1_petru_fisch#o0": "Good. Not good. But good.",
    "g1_petru_fisch.o1": "Lets Lola do it.",
    "g1_petru_fisch.o2": "Offers Petru money.",
    "g1_petru_fisch#o2": "Money is for tourists.",

    "g1_chiara_tender.titel": "Chiara's Tender Test",
    "g1_chiara_tender.lage": "Since Holm left, Chiara acts as if she runs the place. She tosses you the keys to the "
                             "tender. You're to reverse it into the garage. In front of the crew. Without help. She "
                             "folds her arms and waits.",
    "g1_chiara_tender.betroffen.rosi": "is watching",
    "g1_chiara_tender.betroffen.lea": "holds the line",
    "g1_chiara_tender.betroffen.toto": "holds his breath",
    "g1_chiara_tender#z0": "Holm made me do this on my first day. Now it's your turn. Back her in, no help, everybody "
                           "watching.",
    "g1_chiara_tender#z1": "You've got this! Probably! I'll hold the line. Mostly.",
    "g1_chiara_tender.o0": "Calm and slow.",
    "g1_chiara_tender#o0": "Hm. Not bad. Holm would have said that too. Then she'd have found a scratch anyway.",
    "g1_chiara_tender.o1": "Asks Lea to guide you in.",
    "g1_chiara_tender#o1": "Asking for help in front of the crew. Holm would have liked that. So do I.",
    "g1_chiara_tender.o2": "Throws the keys back: “Show me, Chiara.”",

    "g1_holm_kaffee.titel": "A Coffee with Holm",
    "g1_holm_kaffee.lage": "Holm stands on the bridge with two mugs and hands you one. For a long time she says "
                           "nothing. She looks out at the water. Her hand rests on her stomach, as if it hurts.",
    "g1_holm_kaffee.betroffen.chiara": "is secretly pleased",
    "g1_holm_kaffee#z0": "Thirty years at sea. You learn to hear a boat. This one sounds tired.",
    "g1_holm_kaffee#z1": "You're good with people, Frankfurt. Be careful. Being liked is not the same as being followed.",
    "g1_holm_kaffee.o0": "“What would you do differently?”",
    "g1_holm_kaffee.o1": "Drinks the coffee in silence.",
    "g1_holm_kaffee.o2": "“You don't look well, Captain.”",
    "g1_holm_kaffee#o2": "Mind your boat, not my stomach. …Takk.",

    "g1_alva_besuch.titel": "Alva Rows By",
    "g1_alva_besuch.lage": "Alva rows a small boat up to the swim platform. A bottle of wine, two glasses, a dress with "
                           "very little back. She calls out for you, loudly. Chiara is standing right next to you.",
    "g1_alva_besuch.betroffen.chiara": "jealous",
    "g1_alva_besuch.betroffen.lola": "wants wine",
    "g1_alva_besuch#z0": "O figliolu! I was just passing. With wine. And two glasses. Completely by accident.",
    "g1_alva_besuch#z1": "She rowed. Half a mile. By accident.",
    "g1_alva_besuch.o0": "Has a glass with Alva.",
    "g1_alva_besuch.o1": "Invites Alva aboard, for everyone.",
    "g1_alva_besuch.o2": "“Not tonight, Alva.”",
    "g1_alva_besuch#o2": "Tonight, then. I'll leave the light on.",

    "g1_kalte_dusche.titel": "The Cold Shower",
    "g1_kalte_dusche.lage": "Rosi turned off the hot water to save power. Siri was in the shower at the time. The scream "
                            "echoes through the whole yacht.",
    "g1_kalte_dusche.betroffen.siri": "was in the shower",
    "g1_kalte_dusche.betroffen.yasin": "complains",
    "g1_kalte_dusche.betroffen.lea": "laughs",
    "g1_kalte_dusche#z0": "Hot water costs power. Power is life. Cold water builds character. You're welcome.",
    "g1_kalte_dusche#z1": "ROSI! I had conditioner in! I have conditioner in my soul now!",
    "g1_kalte_dusche.o0": "Hot water on for five minutes.",
    "g1_kalte_dusche.o1": "Rosi's right.",
    "g1_kalte_dusche.o2": "Brings Siri a towel and tea.",

    "g1_chiara_pause.titel": "Chiara Takes a Break",
    "g1_chiara_pause.lage": "For the first time, Chiara takes a break. She dives off the stern in a white swimsuit. "
                            "When she climbs back up, half the crew is staring. She only notices one of them.",
    "g1_chiara_pause.betroffen.lea": "cheers",
    "g1_chiara_pause.betroffen.toto": "stares",
    "g1_chiara_pause.betroffen.sophia": "grins",
    "g1_chiara_pause#z0": "What? Officers are allowed to swim. Stop staring, all of you. Not you. You can stare.",
    "g1_chiara_pause#z1": "Chiara has legs. Who knew. Somebody write this down.",
    "g1_chiara_pause.o0": "Dives in after her.",
    "g1_chiara_pause#o0": "Race you to the buoy. Loser gets dunked. I don't lose.",
    "g1_chiara_pause.o1": "Holds her towel and looks her in the eye.",
    "g1_chiara_pause.o2": "Tells the crew to get back to work.",

    "g1_lea_sonnenbrand.titel": "Aloe Vera",
    "g1_lea_sonnenbrand.lage": "Lea fell asleep in the sun. Her back is bright red. She's lying on her stomach with "
                               "her bikini top undone, holding out a tube of aloe vera to you.",
    "g1_lea_sonnenbrand.betroffen.siri": "offers to help",
    "g1_lea_sonnenbrand.betroffen.toto": "gets sent away",
    "g1_lea_sonnenbrand#z0": "I fell asleep. My back is a tomato. Can you… the aloe. Please. Gently. Very gently.",
    "g1_lea_sonnenbrand#z1": "Okay, that's nice. That's very nice. You can keep doing that. For science.",
    "g1_lea_sonnenbrand.o0": "Puts it on very carefully.",
    "g1_lea_sonnenbrand.o1": "Slowly, until she turns over.",
    "g1_lea_sonnenbrand#o1": "Wait. Don't stop. My front's burnt too. Probably. Check.",
    "g1_lea_sonnenbrand.o2": "Asks Siri to do it.",

    "g1_siri_pullover.titel": "Siri in a Jumper",
    "g1_siri_pullover.lage": "Siri comes to breakfast in a grey jumper that's far too big for her. It's your jumper. "
                             "She took it off the chair last night and acts as if that were normal.",
    "g1_siri_pullover.betroffen.yasin": "recognises the jumper",
    "g1_siri_pullover.betroffen.sophia": "sees everything",
    "g1_siri_pullover#z0": "It was cold. It was on the chair. It smells like the sea and coffee. I'm keeping it.",
    "g1_siri_pullover#z1": "Interesting choice of knitwear, darling. Very… officer-adjacent.",
    "g1_siri_pullover.o0": "“It looks better on you than on me.”",
    "g1_siri_pullover.o1": "Acts as if nothing's up.",
    "g1_siri_pullover.o2": "“I want that back. In person.”",
    "g1_siri_pullover#o2": "Come and get it, then. Tonight. If you dare.",

    "g1_sophia_liest_vor.titel": "A Page from Sophia's Notebook",
    "g1_sophia_liest_vor.lage": "Lola has found a loose page from Sophia's notebook and is reading it out to the crew "
                                "in her most dramatic voice. A love scene. A strict officer and a first officer on a "
                                "stranded yacht. It gets very hot, very fast. Halfway through, Sophia walks in.",
    "g1_sophia_liest_vor.betroffen.chiara": "recognises herself",
    "g1_sophia_liest_vor.betroffen.rosi": "wants to hear more",
    "g1_sophia_liest_vor.betroffen.lola": "is fanning herself",
    "g1_sophia_liest_vor#z0": "“She pushed him against the chart table. The charts slid to the floor. Nobody cared.” "
                              "Oh my god. Who wrote this?",
    "g1_sophia_liest_vor#z1": "Stop reading. Stop reading right now. Why does the officer have my haircut?",
    "g1_sophia_liest_vor.o0": "“Keep reading.”",
    "g1_sophia_liest_vor.o1": "Takes the page from Lola and gives it back to Sophia.",
    "g1_sophia_liest_vor.o2": "Later, alone with Sophia: “How does it end?”",
    "g1_sophia_liest_vor#o2": "Badly for the charts. Very well for everyone else. …It's nothing, darling. Just ideas. "
                              "Come by later, and I'll read you the ending.",

    "g1_lola_massage.titel": "Lola's Massage Parlour",
    "g1_lola_massage.lage": "Lola has opened a massage parlour in the mess. A mat, candles, an oil that smells of "
                            "neroli and something else. Totò is groaning. Loudly. Everyone pretends not to hear.",
    "g1_lola_massage.betroffen.rosi": "is nearly asleep",
    "g1_lola_massage.betroffen.toto": "groans too loudly",
    "g1_lola_massage.betroffen.chiara": "doesn't want to hear this",
    "g1_lola_massage#z0": "Next! Boss, you're next. Shirt off, lie down, trust the process. And the oil. Mostly the "
                          "oil.",
    "g1_lola_massage#z1": "Comandante, this woman has magic hands. I think I can see my grandmother.",
    "g1_lola_massage.o0": "Lies down.",
    "g1_lola_massage#o0": "Oh, you're so tense. Let me fix that. All of it. Every bit.",
    "g1_lola_massage.o1": "Gives Lola a massage instead.",
    "g1_lola_massage.o2": "Decline.",

    "g1_helikopter.titel": "Megan Lands",
    "g1_helikopter.lage": "The Eden Group helicopter lands on the sun deck. The downdraught rips the towel off Lola, "
                          "the hairdo off Chiara and very nearly the shorts off Totò. Megan steps out. Not one hair "
                          "moves.",
    "g1_helikopter.betroffen.lola": "her towel flies off",
    "g1_helikopter.betroffen.chiara": "her hair",
    "g1_helikopter.betroffen.toto": "salutes",
    "g1_helikopter#z0": "Good afternoon. I see the welcome committee is wearing less than expected. Charming.",
    "g1_helikopter#z1": "My towel! My towel's in Sardinia now! Hi, I'm Lola, I'm the cook, I'm naked.",
    "g1_helikopter.o0": "Greets Megan formally.",
    "g1_helikopter.o1": "Gives Lola your jacket.",
    "g1_helikopter#o1": "A gentleman. How rare. I'll write it in my diary— no, I won't. Ahaha.",
    "g1_helikopter.o2": "“Welcome to the most beautiful dead yacht in the fleet.”",

    "g1_megan_schach.titel": "Megan Challenges You",
    "g1_megan_schach.lage": "Megan sets up a glass chessboard in the salon and challenges you. The crew gathers. Megan "
                            "has never lost. She says so three times.",
    "g1_megan_schach.betroffen.sophia": "bets on you",
    "g1_megan_schach.betroffen.rosi": "doesn't understand the rules",
    "g1_megan_schach.betroffen.chiara": "nervous",
    "g1_megan_schach#z0": "Chess. You and me. If you win, I owe you a favour. If I win, you owe me one. I always win.",
    "g1_megan_schach#z1": "Check. No, wait. Not check. You're cleverer than you look. I hate that. I love that.",
    "g1_megan_schach.o0": "Plays seriously.",
    "g1_megan_schach.o1": "Loses on purpose.",
    "g1_megan_schach#o1": "You let me win. Never do that again. I want to beat you properly.",
    "g1_megan_schach.o2": "Lets Sophia play.",

    "g1_cousin_schlauchboot.titel": "The Cousin Comes at Night",
    "g1_cousin_schlauchboot.lage": "Totò's cousin comes alongside at night in a rubber dinghy. No lights. He's unloading "
                                   "crates. On the shore something flashes. Elsa's binoculars.",
    "g1_cousin_schlauchboot.betroffen.elsa": "has binoculars",
    "g1_cousin_schlauchboot.betroffen.lea": "helps carry",
    "g1_cousin_schlauchboot.betroffen.chiara": "wakes up",
    "g1_cousin_schlauchboot#z0": "Gennaro, piano, piano! Quiet! The whole bay can hear you. And put the goat down, "
                                 "it's not part of the delivery!",
    "g1_cousin_schlauchboot#z1": "Is this smuggling? Is this real smuggling? Can I carry something?",
    "g1_cousin_schlauchboot.o0": "Stows everything, fast.",
    "g1_cousin_schlauchboot.o1": "Sends the cousin away.",
    "g1_cousin_schlauchboot.o2": "Flashes a torch back at Elsa.",
    "g1_cousin_schlauchboot#o2": "Why are you signalling the police? Are you flirting with the police? Comandante!",

    "g1_katerfruehstueck.titel": "Hangover Breakfast",
    "g1_katerfruehstueck.lage": "Lola is cooking breakfast in sunglasses. Indoors. She's moving very slowly and "
                                "speaking very quietly. The omelette is oversalted. Very.",
    "g1_katerfruehstueck.betroffen.chiara": "the omelette is salty",
    "g1_katerfruehstueck.betroffen.rosi": "drinks Lola's coffee",
    "g1_katerfruehstueck.betroffen.sophia": "watches",
    "g1_katerfruehstueck#z0": "Shhh. Everything is loud. The eggs are loud. Your face is loud. I love you all. "
                              "Quietly.",
    "g1_katerfruehstueck#z1": "This omelette has more salt than the Mediterranean.",
    "g1_katerfruehstueck.o0": "Gives Lola water and quiet, and cooks yourself.",
    "g1_katerfruehstueck.o1": "Bravely eats the omelette.",
    "g1_katerfruehstueck#o1": "You ate it. You're a hero. I'll name a sauce after you.",
    "g1_katerfruehstueck.o2": "“If you party, you still cook.”",

    "rosi_werkstatt_offen.titel": "Rosi's Workshop Is Open Again",
    "rosi_werkstatt_offen.lage": "For days Rosi has welded, sanded and sworn. Now she stands in front of the workshop, "
                                 "the door open, the benches clean, a sign above it in crooked letters: “Open. "
                                 "Mostly.” She holds out a key to you and acts as if it were nothing.",
    "rosi_werkstatt_offen.betroffen.lea": "wants to weld something right now",
    "rosi_werkstatt_offen.betroffen.toto": "is clearing out his crates",
    "rosi_werkstatt_offen#z0": "The workshop works again. Every bench, every light, every drawer. Don't touch the "
                               "drawers.",
    "rosi_werkstatt_offen#z1": "I only stored a few boxes in there, Comandante. Temporarily. For years.",
    "rosi_werkstatt_offen.o0": "Takes the key and thanks her.",
    "rosi_werkstatt_offen#o0": "You can bring me your jackets and your weapons. One piece a night. I'll text you when "
                               "it's done.",
    "rosi_werkstatt_offen.o1": "Leaves the key with her: “You fixed it. It's yours.”",
    "rosi_werkstatt_offen#o1": "…Idiot. Thank you. Now bring me something to fix, I'm already bored.",
    "rosi_werkstatt_offen.o2": "Helps Totò carry his crates.",

    "casanova_saufeder.titel": "Le Large",
    "casanova_saufeder.lage": "Madame Casanova has caught you at the edge of the piazza. Behind her, the path into the "
                              "macchia begins. She holds out an old boar spear, the shaft wrapped in leather, the tip "
                              "freshly sharpened. She isn't smiling, and that's unusual for her.",
    "casanova_saufeder.betroffen.lea": "wants to come along right away",
    "casanova_saufeder.betroffen.toto": "was going to sell that spear",
    "casanova_saufeder#z0": "You saved my village, Monsieur. Now listen: nobody walks into the macchia alone. Not since "
                            "Brother Ambrosius, and not while Nonna Fiora is still waiting up there.",
    "casanova_saufeder#z1": "Take Le Large. It has hunted boar for three generations. In the brush, fire is what the "
                            "beasts fear. Make it glow.",
    "casanova_saufeder#z2": "Comandante, I was going to sell that. For a very fair price. To you. Today.",
    "casanova_saufeder.o0": "Accepts the spear and thanks her.",
    "casanova_saufeder#o0": "Good. Bring it back with a story. And bring yourself back with it.",
    "casanova_saufeder.o1": "Asks her what happened to Brother Ambrosius.",
    "casanova_saufeder#o1": "Walk with me. Not here. The brush has ears, and the ears have cousins.",
    "casanova_saufeder.o2": "Wants to take Lea along.",
    "casanova_saufeder#o2": "She would follow you into a volcano. Fine. But she carries nothing sharp.",
}
