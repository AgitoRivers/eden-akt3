# -*- coding: utf-8 -*-
"""English rewrite, pilot package (25.10.2026): Tag 0 (hangar), the harbour fight, Maxwell's first lesson.

NEU maps a fixed text key to its new English text. Keys:
    <event>.titel / <event>.lage / <event>.betroffen.<pid> / <event>.o<n>   (shown text, not voiced)
    <event>#z<n> / <event>#o<n>                                             (spoken lines, voiced)
    kampf.<encounter>.<field> / kampf.<encounter>.out.<end>                (fight texts)
    gegner.<enemy>.<field>                                                  (enemy labels)
    tut.<step>.en (voiced) / tut.<step>.hint (on-screen hint)
NEUE_EVENTS are events that do not exist yet (Rosi throws Terremoto, E-049), one per Tag-0 chip.
Style: docs/wiki/STIL.md · voices: docs/wiki/figuren/*.md
"""

WAHL_ZIELE = {"moore": "Visit the Moore sisters", "jana": "Visit Jana", "siri": "Visit Siri and Yasin",
              "yamamoto": "Visit Yamamoto-san"}

NEU = {
    # ------------------------------------------------------------------ Maxwell's first lesson (Tag 2 afternoon)
    "mx_tutorial.titel": "Lesson One",
    "mx_tutorial.lage": "Maxwell stands at the top of the sun deck with towels over his shoulders, waving you up. Half "
                        "the crew is hanging over the railing to watch.",
    "mx_tutorial.betroffen.lea": "cheers you on",
    "mx_tutorial.betroffen.toto": "takes bets",
    "mx_tutorial#z0": "Number One! The sea took our engine, brother, but not our muscles. Mr. Maximum is going to teach "
                      "you to fight, and lesson one starts right now!",
    "mx_tutorial#z1": "Two to one on the gigante. Comandante, please don't make me rich.",
    "mx_tutorial.o0": "“Show me, Mr. Maximum.”",
    "mx_tutorial#o0": "MAXIMUM! That's the spirit, brother!",
    "mx_tutorial.o1": "Joins his warm-up push-ups first.",
    "mx_tutorial#o1": "Ten for you, twenty for Mr. Maximum! Now we fight!",

    # ------------------------------------------------------------------ Tag 0 · the limousine
    "t0_limousine.titel": "Antibes, 06:10",
    "t0_limousine.lage": "The hangar doors stand open. Pallets, low sun, and outside the white bow of the Eden Rise. A "
                         "black stretch limousine rolls into the hall, and the loading stops.",
    "t0_limousine.betroffen.toto": "stares",
    "t0_limousine.betroffen.lea": "wants a ride",
    "t0_limousine.betroffen.rosi": "rolls her eyes",
    "t0_limousine.betroffen.chiara": "does the maths",
    "t0_limousine.betroffen.lola": "raises an eyebrow",
    "t0_limousine#z0": "Number One has arrived! Mr. Maximum salutes the limousine!",
    "t0_limousine#z1": "Madonna, six windows. Comandante, I like you already. I've already put money on you.",
    "t0_limousine#z2": "Is that a real limo? Can I sit in it? Not now, obviously. Later? Please?",
    "t0_limousine#z3": "That's the founder of Eden Consulting, darlings. Be charming. Not you, Lea. Me.",
    "t0_limousine#z4": "Great. A consultant, and he came in a hearse.",
    "t0_limousine#z5": "Six windows. We're thirteen people with no budget for napkins, and he has six windows.",
    "t0_limousine#z6": "Mate. Who turns up to a boat in a limo?",
    "t0_limousine.o0": "“Morning, everyone. I'll carry my own bag.”",
    "t0_limousine#o0": "…Noted. That's a first.",
    "t0_limousine.o1": "“The CEO insisted on the car. I'd have taken the bus.”",
    "t0_limousine#o1": "The bus. Sure you would, Boss. Alright, I like you a little.",
    "t0_limousine.o2": "“Hi. I'm Duc.”",
    "t0_limousine.o3": "“Careful with the bags, they're Louis Vuitton.”",
    "t0_limousine#o3": "See? I told you. A hearse.",

    # ------------------------------------------------------------------ Tag 0 · Mac
    "t0_megan.titel": "Mac",
    "t0_megan.lage": "A woman with a clipboard walks out of the glare. Ten years, and she still walks the same way.",
    "t0_megan.betroffen.chiara": "watches",
    "t0_megan#z0": "Duc.",
    "t0_megan.o0": "“It's good to see you, Meg.”",
    "t0_megan#o0": "…It's Megan now. Fleet Director Megan.",
    "t0_megan.o1": "“Fleet Director? Did you yell your way to the top?”",
    "t0_megan#o1": "I did. And I'll yell you right back down if I have to.",
    "t0_megan.o2": "“And you still look so gorgeous, Mac. It feels like time didn't pass.”",
    "t0_megan#o2": "…Time passed, Duc. The gangway's that way.",
    "t0_megan.o3": "“Ms McAllister.”",
    "t0_megan#o3": "First Officer. Good. Let's keep it like that.",

    # ------------------------------------------------------------------ Tag 0 · Holm
    "t0_holm.titel": "The Captain",
    "t0_holm.lage": "Megan leads you to the gangway. At the top stands a woman with a mug of cold coffee, looking at you "
                    "the way she would look at the weather. For a second her hand goes to her side. Then back to the "
                    "coffee.",
    "t0_holm.betroffen.megan": "introduces her",
    "t0_holm#z0": "Captain Marit Holm. Eleven seasons on this boat. She doesn't like consultants. She doesn't like "
                  "anyone, really.",
    "t0_holm#z1": "So you're the CEO's consultant. Can you tie a bowline?",
    "t0_holm.o0": "Ties a bowline one-handed. “Behind my back, if you like.”",
    "t0_holm#o0": "…Hm. Takk. Don't let it go to your head.",
    "t0_holm.o1": "“I can tie a tie. Does that count?”",
    "t0_holm#o1": "On my bridge, no. At the party, maybe.",
    "t0_holm.o2": "“I have my Yachtmaster. It's in the papers.”",
    "t0_holm#o2": "Papers don't float, Frankfurt.",
    "t0_holm.o3": "“Can't the crew do the knots?”",
    "t0_holm#o3": "The crew does what I do. My coffee's cold, and so is this conversation.",

    # ------------------------------------------------------------------ Tag 0 · Chiara
    "t0_chiara.titel": "The Chief Stew",
    "t0_chiara.lage": "At the foot of the gangway: a uniform without a single crease, a clipboard, and a look that "
                      "finds dust.",
    "t0_chiara.betroffen.megan": "checks on her",
    "t0_chiara#z0": "Chiara Sonnberg, Chief Stew. The best in the fleet. Chiara, have you eaten?",
    "t0_chiara#z1": "Yes.",
    "t0_chiara#z2": "Liar.",
    "t0_chiara#z3": "Welcome aboard, First Officer. Your cabin is ready. It used to be mine.",
    "t0_chiara.o0": "“Then you know what's wrong with it. What would you change?”",
    "t0_chiara#o0": "…The shower, and that bell. Thank you for asking. Nobody ever asks.",
    "t0_chiara.o1": "“Then I'll take good care of it. And of the one who had it before.”",
    "t0_chiara#o1": "…That was almost charming. Don't do it on duty.",
    "t0_chiara.o2": "“Thank you.”",
    "t0_chiara#o2": "You're welcome. Breakfast is at seven, and I mean seven.",
    "t0_chiara.o3": "“Great. Is there a bigger one?”",
    "t0_chiara#o3": "No, First Officer. There's a smaller one. Mine. As of now.",

    # ------------------------------------------------------------------ Tag 0 · Rosi
    "t0_rosi.titel": "The Engineer",
    "t0_rosi.lage": "Two legs in work trousers stick out from under the stern. Next to them, a small diesel generator "
                    "hums away happily.",
    "t0_rosi.betroffen.megan": "warns you",
    "t0_rosi#z0": "Rosi Scuderi, our ETO. Brilliant. She bites.",
    "t0_rosi#z1": "If you're here to look at the motor, don't touch anything.",
    "t0_rosi.o0": "“It's not a motor. It's an inverter.”",
    "t0_rosi#o0": "…Okay. Fine. You can touch one thing.",
    "t0_rosi.o1": "“I'm here to look at the engineer.”",
    "t0_rosi#o1": "Wow, that was cheesy. Here, hold this rag, and don't drop it.",
    "t0_rosi.o2": "“I won't.”",
    "t0_rosi#o2": "Good. Then we'll get along.",
    "t0_rosi.o3": "“Can't we just call a mechanic?”",
    "t0_rosi#o3": "I AM the mechanic, Officer!",

    # ------------------------------------------------------------------ Tag 0 · Maxwell
    "t0_maxwell.titel": "Mr. Maximum",
    "t0_maxwell.lage": "A man lifts an entire pallet over his head. Then a helicopter thunders over the hangar roof, and "
                       "he vanishes behind the pallet in a flash.",
    "t0_maxwell.betroffen.megan": "sighs",
    "t0_maxwell#z0": "Maxwell, steward and trainer. Don't challenge him to anything.",
    "t0_maxwell#z1": "Number One! Mr. Maximum has heard of you! Do you lift?",
    "t0_maxwell#z2": "Mr. Maximum was just checking the pallet. The pallet is fine. Everything is fine.",
    "t0_maxwell.o0": "“Show me. Tomorrow, six thirty.”",
    "t0_maxwell#o0": "A MAN OF HONOUR! Six thirty! Mr. Maximum will cry, but quietly.",
    "t0_maxwell.o1": "“Only my expectations.”",
    "t0_maxwell#o1": "Ha! One push-up for that joke, brother!",
    "t0_maxwell.o2": "“A little.”",
    "t0_maxwell#o2": "A little is the beginning of a lot, brother!",
    "t0_maxwell.o3": "“I have a personal trainer in Frankfurt.”",
    "t0_maxwell#o3": "…Mr. Maximum will be very professional now.",

    # ------------------------------------------------------------------ Tag 0 · Totò
    "t0_toto.titel": "The Bosun",
    "t0_toto.lage": "A man with a gold-tooth grin is carrying a small crate himself, although there are pallets "
                    "everywhere.",
    "t0_toto.betroffen.megan": "rolls her eyes",
    "t0_toto#z0": "Totò, our bosun. If something goes missing, it was Totò. If it comes back, that was also Totò.",
    "t0_toto#z1": "Comandante! Welcome, welcome! Don't mind this. Potatoes. Very small potatoes.",
    "t0_toto.o0": "“Let me help you carry that.”",
    "t0_toto#o0": "No, no! Heavy potatoes. I mean light. Very light. I've got it.",
    "t0_toto.o1": "“What are the odds I survive the week?”",
    "t0_toto#o1": "Ten to one. Against. But I love a long shot, Comandante.",
    "t0_toto.o2": "“Morning.”",
    "t0_toto#o2": "Buongiorno, Comandante!",
    "t0_toto.o3": "“Shouldn't those potatoes be inspected?”",
    "t0_toto#o3": "Inspected? By who? Elsa?! …I mean, yes. Of course. Later.",

    # ------------------------------------------------------------------ Tag 0 · Lola
    "t0_lola.titel": "The Cook",
    "t0_lola.lage": "In a corner of the hangar, a bamboo steamer puffs away on a camping stove. She's barefoot, with "
                    "flour on her cheek.",
    "t0_lola.betroffen.megan": "warns you",
    "t0_lola#z0": "Lola, our cook. Don't ask what's in the oregano.",
    "t0_lola#z1": "Alright, Boss. You look like a bloke who eats with tweezers. Go on, prove me wrong.",
    "t0_lola.o0": "“One day I'll cook for you. Pho, my mother's recipe.”",
    "t0_lola#o0": "…A man who cooks? Okay. Now I'm listening.",
    "t0_lola.o1": "“That's the best thing I've had in years. Who taught you this?”",
    "t0_lola#o1": "Nobody! That's the whole point, mate.",
    "t0_lola.o2": "“Maybe later.”",
    "t0_lola#o2": "Later is how people starve, Boss.",
    "t0_lola.o3": "“Is it gluten-free?”",
    "t0_lola#o3": "It's free. That's all it is, mate.",

    # ------------------------------------------------------------------ Tag 0 · where to first
    "t0_wahl.titel": "Where to First?",
    "t0_wahl.lage": "Megan checks her watch. The tide doesn't wait.",
    "t0_wahl.betroffen.lea": "waves",
    "t0_wahl.betroffen.jana": "hides a crate",
    "t0_wahl.betroffen.siri": "is being filmed",
    "t0_wahl.betroffen.yamamoto": "takes photos",
    "t0_wahl#z0": "Where to first? You've got five minutes.",
    "t0_wahl.o0": WAHL_ZIELE["moore"], "t0_wahl.o1": WAHL_ZIELE["jana"],
    "t0_wahl.o2": WAHL_ZIELE["siri"], "t0_wahl.o3": WAHL_ZIELE["yamamoto"],

    # ------------------------------------------------------------------ Tag 0 · the Moore sisters
    "t0_lea.titel": "Lea",
    "t0_lea.lage": "Between the dive tanks stand two sisters, one with a notebook, one with wet hair.",
    "t0_lea.betroffen.sophia": "watches",
    "t0_lea.betroffen.megan": "introduces them",
    "t0_lea#z0": "The Moore sisters. One plans everything, the other plans nothing.",
    "t0_lea#z1": "Did you see the sea last night? It glowed. I swear it glowed, proper glowing!",
    "t0_lea.o0": "“Bioluminescence. Noctiluca, probably.”",
    "t0_lea#o0": "You know Noctiluca? YOU KNOW NOCTILUCA?",
    "t0_lea.o1": "“Show me tonight.”",
    "t0_lea#o1": "It's a date! A science date. Obviously.",
    "t0_lea.o2": "“I was in Frankfurt.”",
    "t0_lea#o2": "Frankfurt doesn't glow, though, does it?",
    "t0_lea.o3": "“Probably pollution.”",
    "t0_lea#o3": "And that, darling, is how you lose her.",
    "t0_sophia.titel": "Sophia",
    "t0_sophia.lage": "Sophia offers you her hand as if she had rehearsed this moment. Maybe she has.",
    "t0_sophia.betroffen.lea": "grins",
    "t0_sophia#z0": "Sophia Moore. I read your interview, darling. You said sustainability is a question of "
                    "hospitality.",
    "t0_sophia.o0": "“Then you're the expert on board. What would you change?”",
    "t0_sophia#o0": "…Nobody ever asks the concierge. Thank you.",
    "t0_sophia.o1": "“I wrote that for exactly one reader. Didn't know it was you.”",
    "t0_sophia#o1": "Nice line. I might steal it.",
    "t0_sophia.o2": "“Did I say that?”",
    "t0_sophia#o2": "You did. Page three, second column.",
    "t0_sophia.o3": "“I don't usually give interviews to staff.”",
    "t0_sophia#o3": "Of course not. How silly of me.",

    # ------------------------------------------------------------------ Tag 0 · Jana
    "t0_jana.titel": "Jana",
    "t0_jana.lage": "A young deckhand walks backwards into a door and apologises to it. Next to her stands a crate. The "
                    "crate meows.",
    "t0_jana.betroffen.megan": "introduces her",
    "t0_jana#z0": "Jana, first season. She apologises to furniture.",
    "t0_jana#z1": "Sorry, sorry – oh! Sorry, Sir. Not you. I meant the door.",
    "t0_jana.o0": "“I didn't hear anything.”",
    "t0_jana#o0": "…Thank you, Sir. Really.",
    "t0_jana.o1": "“Your potatoes are meowing.”",
    "t0_jana#o1": "Very small potatoes! Like Totò's!",
    "t0_jana.o2": "“Morning.”",
    "t0_jana#o2": "Morning, Sir! Servus!",
    "t0_jana.o3": "“Megan, there's a cat in that box.”",
    "t0_jana#o3": "There is no cat, First Officer.",

    # ------------------------------------------------------------------ Tag 0 · Siri and Yasin
    "t0_siri.titel": "Siri and Yasin",
    "t0_siri.lage": "A convertible, two pairs of sunglasses, and a camera that's already rolling before anyone says "
                    "hello.",
    "t0_siri.betroffen.yasin": "films",
    "t0_siri.betroffen.megan": "smiles through it",
    "t0_siri#z0": "Our guests. Smile, please. She has nearly three million followers, and he has opinions.",
    "t0_siri#z1": "The sustainability guy! Say something green, my man!",
    "t0_siri#z2": "Hi. Sorry – sorry about him.",
    "t0_siri.o0": "Holds a hand over the lens. “Not before coffee, Yasin.”",
    "t0_siri#o0": "…Thank you. Really.",
    "t0_siri.o1": "“Something green? Your eyes.”",
    "t0_siri#o1": "…They're blue, actually. But nice try.",
    "t0_siri.o2": "Waves into the camera.",
    "t0_siri#o2": "Content! That's content, bro!",
    "t0_siri.o3": "“Tag Eden Consulting, please.”",
    "t0_siri#o3": "Sure! Smile for the camera!",

    # ------------------------------------------------------------------ Tag 0 · Yamamoto
    "t0_yamamoto.titel": "Yamamoto-san",
    "t0_yamamoto.lage": "A small gentleman in a Hawaiian shirt bows deeply. Then his camera clicks. He's photographing "
                        "a seagull. Or not.",
    "t0_yamamoto.betroffen.megan": "introduces him",
    "t0_yamamoto#z0": "Mr. Yamamoto. Owner's suite, four weeks. He tips like a king.",
    "t0_yamamoto#z1": "Officer-san. Very honoured.",
    "t0_yamamoto.o0": "Bows, exactly deep enough. “Yamamoto-san. The honour is mine.”",
    "t0_yamamoto#o0": "…You know the bow. Very interesting.",
    "t0_yamamoto.o1": "“Bird photography?”",
    "t0_yamamoto#o1": "Very rare bird. So sorry.",
    "t0_yamamoto.o2": "“Welcome aboard.”",
    "t0_yamamoto#o2": "Thank you. Please take care of me.",
    "t0_yamamoto.o3": "“Can someone take his luggage?”",
    "t0_yamamoto#o3": "I carry my own luggage. Thirty years, Officer-san.",

    # ------------------------------------------------------------------ Hafen · getting help (no fight yet: Rosi follows)
    "hk_hilfe.titel": "Getting Help",
    "hk_hilfe.lage": "The tender bumps against the quay of Cala d'Orsu. You came for cable, diesel, anything at all. "
                     "Instead there's screaming. Fish crates tip over, and a grey wave pours out of the net sheds. "
                     "Rats. Lots of them.",
    "hk_hilfe.betroffen.lea": "steers the tender",
    "hk_hilfe#z0": "Madonna. Comandante, that is not a welcome committee.",
    "hk_hilfe#z1": "Duc, the big one with the torn ear – it's leading them!",
    "hk_hilfe.o0": "Looks around for something to fight with.",
    "hk_hilfe#o0": "Go! I'll keep the engine running!",
    "hk_hilfe.o1": "“Lesson one, Mr. Maximum.” Takes a deep breath.",
    "hk_hilfe#o1": "Two to one on the Comandante. Today I'm feeling generous.",

    # ------------------------------------------------------------------ Hafen · Elsa
    "hk_elsa.titel": "The Coast Guard",
    "hk_elsa.lage": "The rats scatter into the alleys. A young woman in a coast guard uniform stands in the middle of "
                    "the chaos with a notepad, as if it were an ordinary Tuesday. Totò ducks behind a crate. Behind "
                    "her, something barks. Several somethings.",
    "hk_elsa.betroffen.toto": "hides behind a crate",
    "hk_elsa#z0": "Lieutenant Ferrandi, coast guard. You're the yacht with no power, I take it? TOTÒ, I can see you "
                  "behind that crate.",
    "hk_elsa#z1": "I need a status update, and I need it now. The dogs can wait thirty seconds.",
    "hk_elsa.o0": "“Rats are gone, dogs are next, the yacht's dark and nobody's hurt.”",
    "hk_elsa#o0": "…Finally, someone who can count. Thank you.",
    "hk_elsa.o1": "“Status: I'm a consultant holding a baseball bat.”",
    "hk_elsa#o1": "Noted. Badly noted. Now go.",
    "hk_elsa.o2": "“Later.”",
    "hk_elsa#o2": "Later. Fine. I'll be right here, writing.",
    "hk_elsa.o3": "“Shouldn't the coast guard handle the dogs?”",
    "hk_elsa#o3": "The coast guard is me, First Officer. And you brought the chaos with you.",

    # ------------------------------------------------------------------ Hafen · Alva
    "hk_alva.titel": "The Bar Owner",
    "hk_alva.lage": "The dogs slink off, whining. A woman with rolled-up sleeves leans out of the bar on the quay and "
                    "tosses you a bottle of water over the nets. Then the ground shakes. Something heavy is coming down "
                    "the alley.",
    "hk_alva.betroffen.elsa": "takes notes",
    "hk_alva#z0": "Alva. That's my bar you're defending, so drink that, and don't miss.",
    "hk_alva.o0": "“If I win, the first round's on me.”",
    "hk_alva#o0": "If you win, o figliolu, the first round's on the house.",
    "hk_alva.o1": "“Are you always this calm when a boar's coming?”",
    "hk_alva#o1": "Only when there's a stranger standing in front of me.",
    "hk_alva.o2": "Just nods.",
    "hk_alva#o2": "Good. Less talking, more hitting.",
    "hk_alva.o3": "“Can't you just close the bar?”",
    "hk_alva#o3": "And miss the best show this harbour's had in years? No.",

    # ------------------------------------------------------------------ Hafen · Petru
    "hk_petru.titel": "The Fisherman",
    "hk_petru.lage": "The boar stops, snorts, and trots back into the macchia as if it had an appointment. In front of "
                     "the boat workshop at the end of the quay, an old fisherman sits mending a net. He has seen "
                     "everything. He nods once.",
    "hk_petru.betroffen.alva": "breathes out",
    "hk_petru#z0": "Hm. Petru. You fight like a sailor, not like a tourist.",
    "hk_petru.o0": "“I had a good teacher. This morning.”",
    "hk_petru#o0": "Then he is a good teacher. My workshop is there, by the blue boat. I have tools.",
    "hk_petru.o1": "“I was mostly running in circles.”",
    "hk_petru#o1": "So was the boar. That's why you won.",
    "hk_petru.o2": "“Thank you.”",
    "hk_petru#o2": "Hm.",
    "hk_petru.o3": "“Does this happen every day here?”",
    "hk_petru#o3": "No. And that's what worries me.",

    # ------------------------------------------------------------------ Hafen · the goat and the mayor
    "hk_ziege.titel": "Where Do the Animals Come From?",
    "hk_ziege.lage": "Then a goat trots across the quay. Around its neck is a leather band with a small box that blinks "
                     "red. It eats a piece of net and wanders off. A lady with a parasol sweeps towards you as if she "
                     "were arriving at a reception.",
    "hk_ziege.betroffen.elsa": "sighs",
    "hk_ziege.betroffen.alva": "grins",
    "hk_ziege#z0": "Madame Casanova, the mayor. Rats, dogs, a boar, and now a goat with jewellery.",
    "hk_ziege#z1": "Monsieur, where do all these animals come from?",
    "hk_ziege.o0": "“I'll find out. Where did the goat come from?”",
    "hk_ziege#o0": "From the hills. The old monastery is up there, but nobody goes there anymore.",
    "hk_ziege.o1": "“Maybe the goat is the mayor's security.”",
    "hk_ziege#o1": "Charming, and rude. I like you already.",
    "hk_ziege.o2": "“No idea.”",
    "hk_ziege#o2": "Then we both know nothing. That's a good start, Monsieur.",
    "hk_ziege.o3": "“Isn't that the mayor's job?”",
    "hk_ziege#o3": "The mayor's job is the festa, Monsieur. Not goats.",

    # ------------------------------------------------------------------ harbour fights (kaempfe_eden_rise.py)
    "kampf.hafen_ratten.title": "Wave 1 · Rats on the Quay",
    "kampf.hafen_ratten.goal": "Drive the pack out of the harbour",
    "kampf.hafen_ratten.flee_reason": "The village is behind you.",
    "kampf.hafen_ratten.out.ko": "The alpha rat squeals and darts into the alleys. The pack follows.",
    "kampf.hafen_ratten.out.aufgabe": "The pack turns and vanishes under the nets.",
    "kampf.hafen_ratten.out.entkommen": "The alpha rat gives up and runs. The pack follows it into the alleys.",
    "kampf.hafen_ratten.out.flucht": "You back away.",
    "kampf.hafen_ratten.out.niederlage": "You go down between the fish crates. Totò pulls you back up. “Again, Comandante!”",
    "kampf.hafen_hunde.title": "Wave 2 · The Dogs",
    "kampf.hafen_hunde.goal": "Keep the pack away from the village",
    "kampf.hafen_hunde.flee_reason": "The village is behind you.",
    "kampf.hafen_hunde.out.ko": "The alpha dog yelps and slinks off. The pack follows it up the hillside.",
    "kampf.hafen_hunde.out.aufgabe": "The pack backs off and trots away into the macchia.",
    "kampf.hafen_hunde.out.entkommen": "The alpha dog turns tail. The pack disappears into the macchia.",
    "kampf.hafen_hunde.out.flucht": "You back away.",
    "kampf.hafen_hunde.out.niederlage": "The dogs knock you flat. Elsa writes something down. “Again. Properly this time.”",
    "kampf.hafen_keiler.title": "Wave 3 · The Boar",
    "kampf.hafen_keiler.goal": "Stand up to the boar",
    "kampf.hafen_keiler.flee_reason": "Alva's bar is behind you.",
    "kampf.hafen_keiler.out.ko": "The boar snorts, turns and trots back into the macchia as if it had an appointment.",
    "kampf.hafen_keiler.out.aufgabe": "The boar stops, looks you over, and leaves.",
    "kampf.hafen_keiler.out.entkommen": "The boar has had enough. It trots up the alley and is gone.",
    "kampf.hafen_keiler.out.flucht": "You back away.",
    "kampf.hafen_keiler.out.niederlage": "The boar throws you against a barrel. Alva hands you your bat back. “Again.”",
    "gegner.ratte_alpha.name": "Alpha Rat", "gegner.ratte_alpha.attack": "Scratch",
    "gegner.ratte_alpha.w1": "Bite", "gegner.ratte_alpha.s1": "The Pack Joins In",
    "gegner.hund_alpha.name": "Alpha Dog", "gegner.hund_alpha.attack": "Snap",
    "gegner.hund_alpha.w1": "Pounce", "gegner.hund_alpha.s1": "The Pack Circles",
    "gegner.keiler.name": "Boar", "gegner.keiler.attack": "Tusks",
    "gegner.keiler.w1": "Snort", "gegner.keiler.s1": "Charge",
    "gegner.keiler.immun_courage": "The boar just lowers its head. Threats don't impress it.",

    # ------------------------------------------------------------------ Maxwell's lessons (kern/tutorial.py)
    "tut.l1_angriff.en": "Welcome to the Maximum gym, brother! Today you fight with this – the mop. Don't laugh, the mop "
                         "is a teacher. Rule one: hit me. Mr. Maximum can take it!",
    "tut.l1_angriff.hint": "Maxwell tosses you a wooden deck mop – training gear, no element. Choose “Attack”. Every "
                           "attack also gives you 1 stamina ⚡.",
    "tut.l1_absicht.en": "Now Mr. Maximum strikes back! See my speech bubble? It always tells you what I'll do next. No "
                         "surprises, brother.",
    "tut.l1_absicht.hint": "The speech bubble above your opponent shows their next move.",
    "tut.l1_parade.en": "When I wind up, watch for the golden spark and press SPACE right then. Perfect timing means no "
                        "damage, and you hit back!",
    "tut.l1_parade.hint": "Parry: press SPACE at the golden spark. Perfect = no damage + counter, good = half damage.",
    "tut.l1_ausdauer.en": "Feel that? Every hit and every parry fills your stamina, and skills cost stamina. Open your "
                          "skills and try Spot Weakness.",
    "tut.l1_ausdauer.hint": "Stamina ⚡ fills up with attacks and parries. Open “Skill” → “Spot Weakness” (1 ⚡).",
    "tut.l1_schwaeche.en": "Eish! You found it! Now Mr. Maximum is exhausted, so your next hit does more. And look, my "
                           "weakness is charm. Mr. Maximum is soft inside.",
    "tut.l1_schwaeche.hint": "Exhausted: your next hit +4. The golden weakness shows which skill works especially well.",
    "tut.l1_fassung.en": "Two ways to win, brother. Knock me down, or talk me down. Every fighter has composure. Empty "
                         "it with Talk, and they give up.",
    "tut.l1_fassung.hint": "Two ways to win: HP to 0 or Composure 🛡 to 0. “Talk” lowers composure (humans only).",
    "tut.l1_heilen.en": "Hurt? Defend halves the next hit and gives you stamina. A first-aid kit heals you. And Mr. "
                        "Maximum patches you up after every fight.",
    "tut.l1_heilen.hint": "Defend halves the next hit (+2 ⚡). Items heal. Every new phase restores your HP.",
    "tut.l1_ende.en": "Mr. Maximum is PROUD of you! Come up to the sun deck any time, brother. Next lesson: heavy hits, "
                      "criticals and fear.",
    "tut.l1_ende.hint": "Training with Maxwell: any time during free time on the sun deck. Costs 1 action.",
    "tut.l2_heftig.en": "Lesson two! Heavy Attack costs three stamina, but it hits like Mr. Maximum on leg day. Save up "
                        "your stamina, then boom!",
    "tut.l2_heftig.hint": "“Heavy Attack”: 3 ⚡, attack +4, never misses.",
    "tut.l2_krit.en": "Sometimes a hit lands perfectly – a critical, one and a half times the damage! Cunning makes "
                      "that happen more often.",
    "tut.l2_krit.hint": "Critical hits: 5 % + 3 % per point of Cunning, damage ×1.5.",
    "tut.l2_angst.en": "Intimidate weakens a fighter's next blow. But Mr. Maximum? Mr. Maximum fears nothing! Some "
                       "enemies are immune, and the game tells you why.",
    "tut.l2_angst.hint": "“Intimidate”: opponent weakened (next attack −3). Immune opponents are locked, with a reason.",
    "tut.l2_ungedeckt.en": "Careful with the fancy moves, brother. Fumble a roll and you're open, so my next hit lands "
                           "harder. Brave is good. Reckless hurts.",
    "tut.l2_ungedeckt.hint": "Exposed: after a fumble, the next blow against you hits +3.",
    "tut.l3_elemente.en": "Final lesson, brother: the elements. Water beats fire, fire beats earth, earth beats air, and "
                          "air beats water. Remember the circle!",
    "tut.l3_elemente.hint": "Elements in a circle: water > fire > earth > air > water. Strong ×1.2, weak ×0.85.",
    "tut.l3_brennen.en": "Fire burns, brother. Every stack bites each round, up to five of them. Defend to put one out, "
                         "and stop feeding the flames!",
    "tut.l3_brennen.hint": "Burning 🔥: 1–5 stacks, damage every round. Defend removes 1 stack.",
    "tut.l3_reaktion.en": "Mix the elements and things react! Fire on wet makes steam, lightning on wet makes a short "
                          "circuit. Play with it!",
    "tut.l3_reaktion.hint": "Reactions: steam (fire + wet), short circuit (shock + wet), rupture, sparks, mud.",
}

for _z in ("moore", "jana", "siri", "yamamoto"):
    _ev = "t0_wahl2_" + _z
    NEU[_ev + ".titel"] = "And Then?"
    NEU[_ev + ".lage"] = "Megan taps her clipboard. One more stop."
    NEU[_ev + ".betroffen.chiara"] = "waits at the gangway"
    NEU[_ev + "#z0"] = "One more, and then we sail."
    _rest = [w for w in ("moore", "jana", "siri", "yamamoto") if w != _z]
    for _n, _w in enumerate(_rest):
        NEU[_ev + ".o%d" % _n] = WAHL_ZIELE[_w]
    NEU[_ev + ".o3"] = "Back to the gangway"

_ABSCHIED = {"herzlich": ("She touches your arm, just briefly.", "See you at the end of the season, Duc. Don't sink my boat."),
             "frech": ("She gives you a crooked grin.", "See you at the end of the season. Don't sink my boat, and don't call me."),
             "flirt": ("She hesitates at the helicopter door. Very quietly:", "Mac. Nobody's called me that in ten years. Don't sink my boat, Duc."),
             "foermlich": ("A handshake. Firm. Short.", "First Officer. Don't sink my boat.")}
for _chip, (_lage, _satz) in _ABSCHIED.items():
    _ev = "t0_abschied_" + _chip
    NEU[_ev + ".titel"] = "Don't Sink My Boat"
    NEU[_ev + ".lage"] = "The helicopter waits on the apron. Maxwell has disappeared. " + _lage
    NEU[_ev + ".betroffen.holm"] = "salutes"
    NEU[_ev + "#z0"] = _satz
    NEU[_ev + ".o0"] = "Watch her go"
    NEU[_ev + ".o1"] = "Head for the gangway"

# ------------------------------------------------------------------ new: Rosi throws Terremoto (E-049), by Tag-0 chip
# chip flags from Tag 0: tag0_rosi_v (trust) / _b (desire) / _n (nothing) / _f (faux pas)
NEUE_EVENTS = {
    "v": {"titel": "Terremoto", "gefuehl": ("caring", "pride"),
          "lage": "Rosi jumps off the tender behind you, soot still on her cheek from the workshop fire, a baseball bat "
                  "over her shoulder. She throws it to you without a word. *He was the only one who knew what an "
                  "inverter was. If I give it to anyone, it's him.*",
          "zeilen": ["Officer, you can't go out there with your bare hands. The workshop's gone, the whole thing burned, "
                     "and this is the only thing I got out.",
                     "His name's Terremoto. I put a weight in the barrel, so when you hit something, it really feels like "
                     "an earthquake. Go on, I'm right behind you."]},
    "b": {"titel": "Terremoto", "gefuehl": ("amusement", "embarrassment"),
          "lage": "Rosi whistles through her fingers. When you turn round, the bat is already flying at you. *Don't "
                  "grin. Don't you dare grin. Now I'm grinning.*",
          "zeilen": ["Hey, Officer! Since you like looking at engineers so much, here's something an engineer made for "
                     "you. Catch!",
                     "That's Terremoto. There's a weighted core inside, I built it myself, so try not to drop it. And "
                     "stop looking at me, the rats are over there!"]},
    "n": {"titel": "Terremoto", "gefuehl": ("neutral", "optimism"),
          "lage": "Rosi pushes through the people on the quay and tosses you a baseball bat without asking. *Let's see "
                  "what he can do with it.*",
          "zeilen": ["You'll need something to fight with, Officer. That's all I could save from the workshop.",
                     "It's called Terremoto, like the earthquake. There's a weight in the barrel, so just swing it and let "
                     "it do the work. Leave the thinking to me, okay?"]},
    "f": {"titel": "Terremoto", "gefuehl": ("annoyance", "sadness"),
          "lage": "Rosi throws you a baseball bat, a little too hard, and it almost slips through your hands. *The only "
                  "thing I got out of the fire, and of all people, he gets it.* Then her voice drops.",
          "zeilen": ["Here you go, Officer. Compliments of the mechanic.",
                     "His name's Terremoto. Papa would love him. So please don't make me regret this, alright?"]},
}
NEUE_OPTIONEN = ["Catches it and runs at the rats.", "“Thanks, Rosi.” Then charges."]

# ------------------------------------------------------------------ package frame (abnahme_bauen.py)
TITEL = "Englisch-Pilot · Tag 0, Hafen, Maxwells Lektion"
HINWEIS = ("Links alt, rechts neu. 🔊 = wird neu vertont. Pro Text OK oder Ändern (mit Notiz). Graue Zeilen ohne „alt“ "
           "sind unverändert. Unten: neu, Rosi wirft Terremoto – je nach deinem Tag-0-Chip bei ihr eine von vier "
           "Fassungen. Knopfnamen in Hinweisen („Attack“, „Skill“) folgen der englischen Oberfläche, die mit dem "
           "UI-Paket kommt.")
PREFIXE = ["t0_", "hk_", "mx_tutorial"]
ENCOUNTERS = ["hafen_ratten", "hafen_hunde", "hafen_keiler"]
GEGNER = ["ratte_alpha", "hund_alpha", "keiler"]
TUTORIAL = True
