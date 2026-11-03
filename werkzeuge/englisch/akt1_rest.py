# -*- coding: utf-8 -*-
"""English rewrite · Act 1 story events, Yamamoto, Maxwell training, odd events
(ereignisse_akt1.py, ereignisse_yamamoto.py, ereignisse_verrueckt.py), 25.10.2026."""

NEU = {
    # ------------------------------------------------------------------ Megan's daily voice messages
    "mg_tag2.titel": "Voice Message from Megan (1)",
    "mg_tag2.lage": "A voice message, 23:58. In the background, the office in Monaco: every light switched off except "
                    "hers.",
    "mg_tag2#z0": "First Officer. It is midnight. I am still in the office. Do you know why? Because my yacht is sitting "
                  "in a bay with no engine and no explanation.",
    "mg_tag2#z1": "Five days. Then I want a name. Goodnight. I won't sleep. Neither should you.",
    "mg_tag2.o0": "Texts back: “Understood.”",
    "mg_tag2.o1": "Plays it to Rosi.",
    "mg_tag2#o1": "No engine. She said no engine. It's an inverter! Somebody tell Monaco it's an inverter!",
    "mg_tag2.o2": "Deletes it and goes to bed.",

    "mg_tag3.titel": "Voice Message from Megan (2)",
    "mg_tag3.lage": "A voice message, 06:02. Megan has been up since four. You can hear it.",
    "mg_tag3#z0": "Good morning. I made a spreadsheet. It has one column. The column says: who.",
    "mg_tag3#z1": "It is empty, First Officer. EMPTY. Four days.",
    "mg_tag3.o0": "Texts back: “The column is filling up.”",
    "mg_tag3.o1": "Sends her a photo of the sunrise.",
    "mg_tag3#o1": "Is that a sunrise? Did you send me a SUNRISE? I am adding a second column.",
    "mg_tag3.o2": "Doesn't answer.",

    "mg_tag4.titel": "Voice Message from Megan (3)",
    "mg_tag4.lage": "A voice message, 07:15. Megan has just come out of a board meeting. In the background, a coffee "
                    "machine rattles very loudly.",
    "mg_tag4#z0": "I just told the board the Eden Bay Weekend is still a success. I said it with a smile. My face still "
                  "hurts.",
    "mg_tag4#z1": "Three days. And tell your cook to stop sending me pictures of breakfast. They look good. It is "
                  "unacceptable.",
    "mg_tag4.o0": "Passes it on to Lola.",
    "mg_tag4#o0": "She said they look good? Boss, she said they look GOOD. I'm framing this.",
    "mg_tag4.o1": "Texts back: “You'll get your name.”",
    "mg_tag4.o2": "Texts back: “You'll get the truth.”",

    "mg_tag5.titel": "Voice Message from Megan (4)",
    "mg_tag5.lage": "A voice message, 07:40. Rotor noise. Megan is shouting over a helicopter.",
    "mg_tag5#z0": "I am in a helicopter. I hate helicopters. I hate them less than your reports.",
    "mg_tag5#z1": "Landing at eleven. I want coffee, a clean deck, and nobody smiling at me. Two days.",
    "mg_tag5.o0": "Lets Chiara know.",
    "mg_tag5#o0": "Eleven. Coffee. Clean deck. No smiling. I can do three of those.",
    "mg_tag5.o1": "Lets Maxwell know.",
    "mg_tag5#o1": "A helicopter? Mr. Maximum will greet it. From behind the anchor locker. Very respectfully.",
    "mg_tag5.o2": "Texts back: “Coffee will be ready.”",

    "mg_tag6.titel": "Voice Message from Megan (5)",
    "mg_tag6.lage": "A voice message, 06:30. Sender: the VIP cabin. One deck above you.",
    "mg_tag6#z0": "I am one deck above you. This is a voice message because if I walk down those stairs, I will fire "
                  "someone on the way.",
    "mg_tag6#z1": "Tomorrow. Eleven o'clock. The salon. Bring proof. Not feelings.",
    "mg_tag6.o0": "Goes up the stairs and knocks.",
    "mg_tag6#o0": "You came up. Nobody comes up. …Sit. You have four minutes.",
    "mg_tag6.o1": "Texts back: “Eleven o'clock.”",
    "mg_tag6.o2": "Plays the message to Totò.",
    "mg_tag6#o2": "Comandante, I run a book. Odds she fires somebody before lunch: two to one. You want in?",

    "mg_tag7.titel": "Voice Message from Megan (6)",
    "mg_tag7.lage": "A voice message, 07:00. No shouting. That's worse.",
    "mg_tag7#z0": "Good morning. Today I listen. Only today.",
    "mg_tag7#z1": "Make it count, First Officer.",
    "mg_tag7.o0": "Takes a deep breath.",
    "mg_tag7.o1": "Texts back: “I will.”",

    # ------------------------------------------------------------------ Maxwell's training
    "mx_jana_bewundert.titel": "Jana Is Watching",
    "mx_jana_bewundert.lage": "Your tenth win against Maxwell. Down at the railing stands Jana with two bottles of water, "
                              "forgetting that one of them was meant for Maxwell. She turns red when you look at her.",
    "mx_jana_bewundert.betroffen.maxwell": "grins",
    "mx_jana_bewundert.betroffen.chiara": "raises an eyebrow",
    "mx_jana_bewundert#z0": "Sorry, I– that was really– you just– I brought water. For you. Both. Both are for you.",
    "mx_jana_bewundert#z1": "Mr. Maximum sees everything, little sister. Mr. Maximum also sees that Mr. Maximum gets no "
                            "water.",
    "mx_jana_bewundert.o0": "Takes a bottle and winks at her.",
    "mx_jana_bewundert#o0": "Na geh… okay. Okay. I'm going to go and stand somewhere else now.",
    "mx_jana_bewundert.o1": "Offers to let her join the next training session.",
    "mx_jana_bewundert#o1": "Me? Fighting? …Will you show me how to stand like that?",
    "mx_jana_bewundert.o2": "Gives Maxwell the second bottle.",
    "mx_jana_bewundert#o2": "THANK you, brother. Jana, Mr. Maximum forgives you.",

    "mx_chiara_lacht.titel": "Chiara Was Watching",
    "mx_chiara_lacht.lage": "Your third defeat. You're lying on the teak, looking up at the sky. A shadow falls over "
                            "you: Chiara, arms folded, uniform immaculate. She saw everything.",
    "mx_chiara_lacht.betroffen.maxwell": "wants to mediate",
    "mx_chiara_lacht#z0": "First Officer. You are aware that he's on our side? He was going easy on you. I could tell.",
    "mx_chiara_lacht#z1": "Mr. Maximum was NOT going easy. Mr. Maximum was going… medium.",
    "mx_chiara_lacht.o0": "“Then you show me how it's done.”",
    "mx_chiara_lacht#o0": "In this uniform? Absolutely not. …Tomorrow. Seven. Don't be late.",
    "mx_chiara_lacht.o1": "Stays lying there and laughs along.",
    "mx_chiara_lacht#o1": "…Fine. That was funny. Now get up, you're lying on my clean deck.",
    "mx_chiara_lacht.o2": "Gets up, offended.",
    "mx_chiara_lacht#o2": "Oh no. I hurt the First Officer's feelings. I'll put it in the log.",

    # ------------------------------------------------------------------ Lola's rungs, Chiara's stars
    "ak_lola_vorkoster.titel": "The Taster",
    "ak_lola_vorkoster.lage": "Lola holds out a spoon to you before the food goes out. There's a sticker on the cooker "
                              "hood: NO TWEEZERS. She looks at you as if a verdict were about to fall.",
    "ak_lola_vorkoster.betroffen.rosi": "sniffs the air",
    "ak_lola_vorkoster.betroffen.maxwell": "waits with a plate",
    "ak_lola_vorkoster#z0": "Okay, Boss. Taste. Be honest. No, don't be honest. Yes, be honest.",
    "ak_lola_vorkoster#z1": "Mr. Maximum volunteers as second taster. Mr. Maximum is very brave.",
    "ak_lola_vorkoster.o0": "Praises it loudly in front of the whole crew.",
    "ak_lola_vorkoster#o0": "Did you hear that? Everybody hear that? Okay. Okay. I'm fine. I'm not crying, it's the "
                            "onions.",
    "ak_lola_vorkoster.o1": "Quietly: “That's really good.”",
    "ak_lola_vorkoster#o1": "…Yeah? Okay. Okay, cool. Cool cool cool.",
    "ak_lola_vorkoster.o2": "Critiques it like a star chef.",
    "ak_lola_vorkoster#o2": "Yes, Chef. …Sorry. Habit. Old kitchen. Forget it.",

    "ak_lola_service.titel": "“Service!”",
    "ak_lola_service.lage": "Megan claps her hands in the galley: dinner for four, right now, like in a restaurant. "
                            "Someone shouts “Service!” Lola stands still, the spoon in her hand. She isn't breathing.",
    "ak_lola_service.betroffen.lola": "freezes",
    "ak_lola_service.betroffen.chiara": "holds the plates",
    "ak_lola_service#z0": "Service! Four plates, now. Chop chop. This is a yacht, not a hippie commune.",
    "ak_lola_service#z1": "Yes, Chef. Yes, Chef. Yes, Chef.",
    "ak_lola_service.o0": "“I'll take over.”",
    "ak_lola_service#o0": "…Thanks, Boss. I just need a minute. Just a minute.",
    "ak_lola_service.o1": "“Lola, pull yourself together.”",
    "ak_lola_service#o1": "Yes, Chef.",
    "ak_lola_service.o2": "“Everybody out. Lola, breathe.”",
    "ak_lola_service#o2": "…Sydney. It was a kitchen in Sydney. Nobody ever said it was good. Not once. Can I tell you "
                          "later? When she's gone?",

    "ak_chiara_sternzettel.titel": "A Page Full of Stars",
    "ak_chiara_sternzettel.lage": "On the chart table lies a sheet of paper covered in tiny writing: angles, times, and "
                                  "one circled word – Polaris. Chiara's handwriting. Lola leans over to you.",
    "ak_chiara_sternzettel.betroffen.lola": "whispers",
    "ak_chiara_sternzettel#z0": "Psst. Light on the bridge wing, two in the morning, every night. Somebody's studying. "
                                "You didn't hear it from me.",
    "ak_chiara_sternzettel#z1": "That's mine. That's nothing. That's… a shopping list.",
    "ak_chiara_sternzettel.o0": "Hands the page back without asking.",
    "ak_chiara_sternzettel#o0": "…Thank you.",
    "ak_chiara_sternzettel.o1": "“A shopping list with Polaris on it?”",
    "ak_chiara_sternzettel#o1": "Polaris is a very popular brand of… rice. Goodbye.",

    "ak_chiara_brueckennock.titel": "The Bridge Wing at Night",
    "ak_chiara_brueckennock.lage": "Two in the morning. A torch is burning on the bridge wing. Chiara is measuring the "
                                   "sky with an old sextant, her lips moving. She hasn't seen you yet.",
    "ak_chiara_brueckennock.betroffen.lea": "is asleep on deck",
    "ak_chiara_brueckennock#z0": "Thirty-nine… no. Forty-one. Again.",
    "ak_chiara_brueckennock#z1": "How long have you been standing there? Don't answer that.",
    "ak_chiara_brueckennock.o0": "“I didn't see anything.”",
    "ak_chiara_brueckennock#o0": "Good. Neither did I. Goodnight, First Officer.",
    "ak_chiara_brueckennock.o1": "“Do you want some help?”",
    "ak_chiara_brueckennock#o1": "I don't need help. I need… nothing. Goodnight.",
    "ak_chiara_brueckennock.o2": "“Will you show me how you do that?”",
    "ak_chiara_brueckennock#o2": "…You want to learn? From me? Fine. That's Polaris. And I failed the theory exam in "
                                 "April. Don't tell anyone.",

    # ------------------------------------------------------------------ Yamamoto and the rare bird
    "yk_vogel.titel": "The Rare Bird",
    "yk_vogel.lage": "Jana is wringing out lines on the swim platform in her red-white-red bikini, the tip of her tongue "
                     "between her teeth. Two decks up, Yamamoto-san is hanging over the railing with a camera whose lens "
                     "is as long as a forearm. He has binoculars and a notebook too, and he's being very busy.",
    "yk_vogel.betroffen.jana": "sunbathes and suspects nothing",
    "yk_vogel.betroffen.maxwell": "isn't here yet",
    "yk_vogel#z0": "Officer-san. Shhh. A very rare bird. Only visible at the swim platform. Between ten and noon.",
    "yk_vogel#z1": "Sir! Hi! Sorry, am I in the way? I'm only doing the lines. Jessas, the water is cold.",
    "yk_vogel.o0": "Asks Yamamoto what kind of bird it is.",
    "yk_vogel#o0": "Latin name: Avis kitsune. Very shy. Very red and white. So sorry, I cannot say more.",
    "yk_vogel.o1": "Brings Jana a jumper.",
    "yk_vogel.o2": "Watches quietly to see what happens.",

    "yk_schatten.titel": "Maxwell's Shadow",
    "yk_schatten.lage": "Yamamoto is lying on the sun deck, just about to take a picture. Suddenly it goes dark. Behind "
                        "him stands Maxwell, two metres wide, arms folded, casting a shadow like a wardrobe.",
    "yk_schatten.betroffen.yamamoto": "freezes mid-click",
    "yk_schatten.betroffen.jana": "waves from below",
    "yk_schatten#z0": "Mr. Maximum sees a rare bird too. The bird is on the camera's side of the lens. Mr. Maximum has a "
                      "question.",
    "yk_schatten#z1": "So sorry. The bird is gone now. Very fast bird.",
    "yk_schatten.o0": "Lets Maxwell handle it.",
    "yk_schatten.o1": "Covers for Yamamoto: “He's photographing clouds.”",
    "yk_schatten#o1": "Yes. Clouds. Beautiful clouds. Very low clouds. Very red clouds.",
    "yk_schatten.o2": "Invites them both for an iced tea.",

    "yk_ausrede.titel": "Cloud Studies",
    "yk_ausrede.lage": "Yamamoto has changed his approach. Now he is clearly only photographing the sky. The lens, "
                       "however, points down and slightly to the left, where Jana is polishing the railing. Maxwell "
                       "stands next to him, looking up at the sky and down at the camera, in turns.",
    "yk_ausrede.betroffen.maxwell": "is looking for the catch",
    "yk_ausrede.betroffen.jana": "is polishing the railing",
    "yk_ausrede#z0": "A cumulus. Very low. Very close. Very interesting.",
    "yk_ausrede#z1": "Mr. Maximum looks up. No cloud. Mr. Maximum looks down. The cloud has a ponytail.",
    "yk_ausrede.o0": "Turns Yamamoto's lens up to the sky.",
    "yk_ausrede.o1": "Shows Maxwell where the cloud is.",
    "yk_ausrede.o2": "Talks clouds with Yamamoto, expert to expert.",

    "yk_falle.titel": "Maxwell's Trap",
    "yk_falle.lage": "On the swim platform, Maxwell has dressed a dummy made of towels in a red-white-red bikini and tied "
                     "it to a deckchair with a line. He's hiding behind the fenders and waving you over. Two decks up, "
                     "the clicking starts.",
    "yk_falle.betroffen.yamamoto": "walks into the trap",
    "yk_falle.betroffen.jana": "knows nothing",
    "yk_falle#z0": "Number One, Mr. Maximum has a plan. The towel is the bait. The bird always comes back.",
    "yk_falle#z1": "Ah. Beautiful. Very still bird. Finally, a bird that does not fly away.",
    "yk_falle.o0": "Lets the trap spring.",
    "yk_falle.o1": "Warns Yamamoto.",
    "yk_falle.o2": "Fetches Jana so she can see the dummy.",
    "yk_falle#o2": "Sorry, why am I made of towels? Is it a surprise? Jessas, it's a good bikini.",

    "yk_jana_merkt.titel": "Jana Plays Along",
    "yk_jana_merkt.lage": "Jana has finally worked out what's clicking up there. She goes red and waves up anyway. Then "
                          "she strikes a pose, too loud and a step too far. Yamamoto bows so deeply that the camera "
                          "slips out of his hands and sails towards the water.",
    "yk_jana_merkt.betroffen.yamamoto": "goes red to the ears",
    "yk_jana_merkt.betroffen.maxwell": "is on his way",
    "yk_jana_merkt#z0": "Hallo, Yamamoto-san! Sorry! I'm the bird! Servus! Is this the good side? Jessas, this is so "
                        "embarrassing.",
    "yk_jana_merkt#z1": "So sorry, so sorry. The bird is very beautiful. The camera is very wet.",
    "yk_jana_merkt.o0": "Fishes the camera out of the water.",
    "yk_jana_merkt.o1": "Praises Jana: “That was brave.”",
    "yk_jana_merkt#o1": "I was brave? Sorry. I mean, thank you. I didn't know I could be brave in a bikini.",
    "yk_jana_merkt.o2": "Hands Yamamoto a towel.",

    "yk_erwischt.titel": "Maxwell Catches Him",
    "yk_erwischt.lage": "This time Yamamoto is sitting on the foredeck with his lens trained on the swim platform. "
                        "Maxwell comes up silently behind him, takes him by the collar and lifts him a hand's breadth off "
                        "the deck. Jana stands by with her hands over her mouth.",
    "yk_erwischt#z0": "Caught! Mr. Maximum catches the bird! Number One, what happens to a bird that gets caught?",
    "yk_erwischt#z1": "So sorry. I am a quiet bird. I only look. I never touch. This is my promise.",
    "yk_erwischt.o0": "Lets Maxwell decide: the photos get deleted.",
    "yk_erwischt.o1": "Yamamoto may keep one photo.",
    "yk_erwischt.o2": "Ten push-ups for the bird.",
    "yk_erwischt#o2": "For the joke! Ten push-ups! Mr. Maximum counts in Zulu! Kunye, kubili, kuthathu!",

    "yk_liste.titel": "The Last Item on the List",
    "yk_liste.lage": "Yamamoto has opened his notebook: a list of things he wants to do once in his life. The last item "
                     "reads: photograph a real bird. Maxwell reads along, and so does Jana. Then Maxwell sets him on the "
                     "mat, and Jana hands him a towel.",
    "yk_liste.betroffen.maxwell": "signs the list",
    "yk_liste.betroffen.jana": "draws a tick",
    "yk_liste#z0": "Mr. Maximum signs the list. Mr. Maximum will take you to a real bird. After push-ups. Many push-ups.",
    "yk_liste#z1": "A bird, and a friend with a very large hand. Thirty years of overtime, and this is my holiday.",
    "yk_liste#z2": "I'll draw the tick, Yamamoto-san. And a little bird next to it. Sorry, a very little bird.",
    "yk_liste.o0": "Joins them on the mat.",
    "yk_liste.o1": "Ticks the item off yourself.",
    "yk_liste.o2": "Takes a photo of all three of them.",

    # ------------------------------------------------------------------ morning training
    "mt_erste.titel": "06:30 with Mr. Maximum",
    "mt_erste.lage": "Half past six on the aft deck. Maxwell, in his neon-orange training top, stands in front of Jana, "
                     "hair in a plait, still half asleep. Totò sits on a bollard and watches, his coffee mug held like a "
                     "ticket.",
    "mt_erste.betroffen.jana": "hangs on the ropes, panting",
    "mt_erste.betroffen.toto": "watches with coffee",
    "mt_erste#z0": "Mr. Maximum does not say good morning. Mr. Maximum says: burpees! One joke, one burpee. Go!",
    "mt_erste#z1": "Sorry, sorry. Is it already time? Na geh. Okay. One. Two. Servus, legs.",
    "mt_erste.o0": "Joins in.",
    "mt_erste.o1": "Cheers Jana on.",
    "mt_erste#o1": "Thank you, Sir. I can do ten. Maybe six. Okay, three.",
    "mt_erste.o2": "Steals Totò's coffee and watches.",

    "mt_nicht_aufhoeren.titel": "Not at “I Can't”",
    "mt_nicht_aufhoeren.lage": "Jana is holding a plank, her arms trembling, her face bright red. Maxwell crouches in "
                               "front of her, calm as a rock. Lea comes past with two mugs and joins in counting.",
    "mt_nicht_aufhoeren.betroffen.jana": "is shaking in the plank",
    "mt_nicht_aufhoeren.betroffen.lea": "counts out loud",
    "mt_nicht_aufhoeren#z0": "Mr. Maximum does not hear “I can't”. Mr. Maximum hears “not yet”. Say it with Mr. Maximum.",
    "mt_nicht_aufhoeren#z1": "Not… yet. Not yet. Jessas. Not yet! Sorry, my arms are shaking.",
    "mt_nicht_aufhoeren.o0": "Counts with her.",
    "mt_nicht_aufhoeren.o1": "Reins Maxwell in: “That's enough.”",
    "mt_nicht_aufhoeren.o2": "Lets Maxwell handle it.",

    "mt_zehn.titel": "Ten Push-Ups",
    "mt_zehn.lage": "Jana is in the starting position. Maxwell counts without blinking. At five she's shaking, at seven "
                    "she swears in Viennese, at ten she collapses onto the mat, beaming. Maxwell turns away and wipes his "
                    "face.",
    "mt_zehn.betroffen.maxwell": "cries with pride and calls it an allergy",
    "mt_zehn.betroffen.toto": "applauds",
    "mt_zehn#z0": "Ten! TEN! Did you see? Servus, Sir! Sorry! I did ten!",
    "mt_zehn#z1": "Mr. Maximum has no tears. Mr. Maximum has an allergy. To very good push-ups. Number One, look away.",
    "mt_zehn.o0": "Gives Jana a hand and pulls her up.",
    "mt_zehn.o1": "Hands Maxwell a tissue.",
    "mt_zehn#o1": "Thank you, Number One. This is not a tissue. This is a push-up towel.",
    "mt_zehn.o2": "Invites everyone to breakfast.",

    # ------------------------------------------------------------------ odd events
    "g1_casanova_nebel.titel": "The Dress Rehearsal",
    "g1_casanova_nebel.lage": "Madame Casanova is rehearsing her festa entrance. In a flamenco dress, on a fishing boat, "
                              "with a hired fog machine. The fog is thicker than planned. The whole harbour has gone "
                              "white. Somewhere in it, Elsa's patrol boat is sounding its horn.",
    "g1_casanova_nebel.betroffen.elsa": "her boat is lost in the fog",
    "g1_casanova_nebel.betroffen.toto": "is selling seats",
    "g1_casanova_nebel.betroffen.petru": "saw nothing",
    "g1_casanova_nebel#z0": "Behold! The mayor rises from the mists of Corsica! …Is it working? I can't see anything. "
                            "Perfect.",
    "g1_casanova_nebel#z1": "Madame. I can't see my own bow. Turn. It. Off.",
    "g1_casanova_nebel#z2": "Front row in the fog, ten euros! Second row, five! You see nothing, but you see nothing "
                            "first!",
    "g1_casanova_nebel.o0": "Fixes the fog machine so it doses properly.",
    "g1_casanova_nebel#o0": "A gentle mist! A mysterious mist! You have given me the gift of drama, Monsieur!",
    "g1_casanova_nebel.o1": "Applauds loudly until she bows.",
    "g1_casanova_nebel#o1": "The people love me! Even the ones I cannot see!",
    "g1_casanova_nebel.o2": "Guides Elsa back to her boat.",
    "g1_casanova_nebel#o2": "…Thank you. Tell her the fog machine is now evidence.",

    "g1_petru_oktopus.titel": "Petru's Lodger",
    "g1_petru_oktopus.lage": "Petru left a bucket on board when he made his delivery. In the bucket was an octopus he's "
                             "been feeding for weeks and calls Bastianu. Now the bucket is empty. Lola is standing in the "
                             "galley with a wooden spoon, swearing she only had a look. An arm waves from the sink.",
    "g1_petru_oktopus.betroffen.petru": "is looking for his friend",
    "g1_petru_oktopus.betroffen.chiara": "ink on her uniform",
    "g1_petru_oktopus.betroffen.toto": "smells calamari",
    "g1_petru_oktopus#z0": "Okay, so, in my defence, he looked hungry. And then he looked at the garlic. And then he was "
                           "GONE.",
    "g1_petru_oktopus#z1": "Bastianu. Come here.",
    "g1_petru_oktopus#z2": "Comandante, think about it. The garlic is already here. Destiny is calling.",
    "g1_petru_oktopus.o0": "Gently coaxes Bastianu back into the bucket.",
    "g1_petru_oktopus#o0": "…Grazie. He likes you. He never likes anybody.",
    "g1_petru_oktopus.o1": "Makes it clear to Totò: you don't eat friends.",
    "g1_petru_oktopus#o1": "Fine! Fine. I will eat my feelings. Also not octopus.",
    "g1_petru_oktopus.o2": "Lets Lola draw the octopus until Petru collects him.",
    "g1_petru_oktopus#o2": "Look, I gave him eyebrows. He's thrilled. He's not thrilled. He's an octopus.",

    "gv_elsa_kiste.titel": "Potatoes That Meow",
    "gv_elsa_kiste.lage": "Elsa has stopped one of Totò's crates on the quay. The crate says “Potatoes”. The crate "
                          "meows. Totò claims they're very young potatoes. Elsa has already pulled out her notebook.",
    "gv_elsa_kiste#z0": "Monsieur Esposito. Potatoes do not purr.",
    "gv_elsa_kiste#z1": "Corsican potatoes, Lieutenant. Very emotional. It's the soil.",
    "gv_elsa_kiste#z2": "Open it. If it's a cat, I'm keeping it. If it's potatoes, I'm keeping those too.",
    "gv_elsa_kiste.o0": "Backs Elsa: open it.",
    "gv_elsa_kiste#o0": "A kitten. Three kittens. Esposito, you are smuggling kittens.",
    "gv_elsa_kiste.o1": "Covers for Totò: “Those are my potatoes.”",
    "gv_elsa_kiste#o1": "Comandante! A man of honour! …They are kittens, by the way. For my nonna.",
    "gv_elsa_kiste.o2": "Suggests giving the kittens to the village.",
    "gv_elsa_kiste#o2": "The official cats of the festa! I declare it! Somebody write it down!",

    "hy_megan_dinner.titel": "Megan Joins Dinner",
    "hy_megan_dinner.lage": "Megan calls during the crew dinner and demands to be put on a chair. “Team building.” Lola "
                            "puts a napkin in front of the laptop and serves Megan a plate of pasta that nobody will eat.",
    "hy_megan_dinner#z0": "Put me at the head of the table. Yes. There. Now everyone may look at me while they eat.",
    "hy_megan_dinner#z1": "Mwahaha. That was a laugh. I'm told laughing builds trust. Is it working?",
    "hy_megan_dinner.o0": "Raises a toast to Megan.",
    "hy_megan_dinner#o0": "To me. How thoughtful. I'm writing it in your file. The nice part of your file.",
    "hy_megan_dinner.o1": "Lets her “taste” the pasta.",
    "hy_megan_dinner#o1": "…Don't tell anyone I laughed. If this leaks, I'll know it was you.",
    "hy_megan_dinner.o2": "Politely hangs up so the crew can eat in peace.",

    "ab_casanova_flamenco.titel": "Flamenco with the Mayor",
    "ab_casanova_flamenco.lage": "The piazza is empty, the festa lights still strung up. Madame Casanova stands by the "
                                 "fountain in a red flamenco dress, an old portable radio at her feet. She summoned you "
                                 "“for a lesson on behalf of the municipality”. Then she switches on the radio and "
                                 "stops being the mayor.",
    "ab_casanova_flamenco#z0": "Tonight there is no mayor. No festa. No speeches. …Well. Maybe one speech. A short one.",
    "ab_casanova_flamenco#z1": "Flamenco is not dancing, Monsieur. It is a conversation where nobody is allowed to lie.",
    "ab_casanova_flamenco#z2": "Give me your hand. If you want to stop, you stop. If you don't… we'll see where the "
                               "music goes.",
    "ab_casanova_flamenco.o0": "Takes her hand and lets her lead.",
    "ab_casanova_flamenco#o0": "Good. Now listen to the guitar. Your feet will lie. Your hands won't.",
    "ab_casanova_flamenco.o1": "Dances with her, just dances.",
    "ab_casanova_flamenco#o1": "Only dancing. Yes. That is also a conversation. A beautiful one.",
    "ab_casanova_flamenco.o2": "“Not tonight, Madame.”",
    "ab_casanova_flamenco#o2": "Then the music waits. The way the whole village waits for me. Patiently. Dramatically.",
}
