# -*- coding: utf-8 -*-
"""Flirt and NSFW events (Duc 25.10.2026, Sora's point from the Brain Trust reflection): raise the share of 'frech'
events to about 25 %. One person per event - no two women competing for Duc; romances stay private (E-060), so any
bystander in a gag1 is somewhere else, asleep or looking the other way. Every option allows a no without breaking
anything. Romance ladders from the wiki are not skipped; everything sits in Act 1 (days 2-6).

Desire (begehren) only for the crew women, Lola and Alva (engine rule). Siri: desire only after siri_frei. Jana: no
romance, a repeatable one-night stand (wiki). Megan: hidden romance only with megan_funke (Tag-0 flirt).
NSFW: art "abend" with INTIM(...) like Lola and Alva (ereignisse_abende.py).
"""
from ereignisse_basis import *  # noqa: F401,F403


def H(anrufer, ort, art="video"):
    return {"anrufer": anrufer, "anrufer_ort": ort, "art": art}


def P1(handelnd, *betroffen):
    return {"handelnd": handelnd, "betroffen": [{"id": b[0], "ton": b[1], "was": b[2]} for b in betroffen]}


def VT(pid, n):
    return {"wert": ["vertrauen.%s" % pid, ">=", n]}


N = ["nacht"]
TAG = ["tag"]
FREI = {"flag": "siri_frei"}
FUNKE = {"flag": "megan_funke"}

EVENTS = [
    # ================================================================== Lea
    E("fl_lea_neopren", "gag1", "frech", "Zip Me Up", WANN((2, 6), TAG, wetter=["klar"]), "swim_platform",
      P1("lea", ("siri", "?", "is underwater and sees nothing")),
      "Lea is hopping on one foot on the swim platform, half into her wetsuit, one arm twisted behind her back. The zip "
      "is stuck exactly where she can't reach it.",
      [Z("lea", "Duc! Help. Emergency. Not a real emergency. A zip emergency. Could you – the back, it's stuck.",
         "embarrassment"),
       Z("lea", "Did you know octopuses can reach every part of their own body? I'd make a terrible octopus.",
         "nervousness")],
      [O("Pulls the zip up slowly, one tooth at a time.", [B("lea", 6), V("lea", 2), NK("lea")],
         zeile=Z("lea", "That was – yes. Thank you. That was very thorough. Proper thorough. I'm going in the water "
                         "now. Immediately.", "desire")),
       O("Does it quickly, like a professional.", [V("lea", 4)],
         zeile=Z("lea", "Thanks! You're very efficient. That's – yeah. That's good. Efficient is good.", "neutral")),
       O("“For the record, I think you'd make a lovely octopus.”", [], probe=P("charm", 12),
         erfolg=[B("lea", 8), V("lea", 2), NK("lea")], fehlschlag=[V("lea", 2)],
         zeile=Z("lea", "Eight arms and three hearts. Two of them would be going very fast right now.", "amusement"))],
      sets={"lea": "Dive", "siri": "Riviera Swim"}, knistern=True),

    E("fl_lea_seite41", "gag1", "frech", "Page Forty-One", WANN((3, 6), ["abend"], bed=VT("lea", 2)), "aft_deck",
      P1("lea", ("lola", "?", "is singing in the galley and hears nothing")),
      "Lea has fallen asleep over her logbook on the aft deck. The wind turns a page. Fish, a crab, a jellyfish with a "
      "face. And on page forty-one, very carefully drawn: you, at the helm. She wakes up exactly now.",
      [Z("lea", "Don't – that's a fish. That's a very big fish. With a jaw. Okay, it's you. It's research.",
         "embarrassment")],
      [O("Sits down next to her. “Show me how you did the eyes.”", [B("lea", 6), V("lea", 4), NK("lea")],
         zeile=Z("lea", "You look at things like the sea's about to tell you a secret. That's the hard part. I had to "
                         "watch you for ages. Oh no. I said that out loud.", "love")),
       O("“It's good. You should draw the whole crew.”", [V("lea", 4)],
         zeile=Z("lea", "The whole crew. Right. Yes. Good idea. Very… crew.", "disappointment")),
       O("Takes the pencil and adds a small octopus on his shoulder.", [], probe=P("empathy", 11),
         erfolg=[B("lea", 6), V("lea", 4)], fehlschlag=[V("lea", 2)],
         zeile=Z("lea", "Now it's a portrait of two of my favourite things. I mean – octopuses. Two octopuses.",
                 "amusement"))],
      sets={"lea": "Off Duty"}, knistern=True),

    E("fl_lea_fakt", "handy", "frech", "Fact of the Night", WANN((2, 6), N, bed=VT("lea", 2)), "duc_cabin",
      H("lea", "foredeck", "nachricht"),
      "A message from Lea, sent at 00:47. Then a second one at 00:48. Then a third at 00:48.",
      [Z("lea", "Fact of the night: some fish only glow when someone else is looking. 🐟✨ Unrelated. Goodnight.",
         "nervousness"),
       Z("lea", "That wasn't about anyone. It was about fish. Proper fish facts. 🐠 Goodnight properly now. 🙈", "embarrassment")],
      [O("“Then I'll keep looking.”", [B("lea", 6), V("lea", 2), NK("lea"), EN(-1)],
         zeile=Z("lea", "Okay. Okay okay okay. 🫣 I'm putting my phone under the pillow now. It's glowing. ✨", "joy")),
       O("Sends a fish emoji.", [V("lea", 4)],
         zeile=Z("lea", "It's a clownfish. You sent me a clownfish. 🐠 I'm choosing to find that romantic. 🥹", "amusement")),
       O("“Sleep, Lea. Early start.”", [V("lea", 2)])],
      knistern=True),

    E("fl_lea_salut", "gag1", "frech", "At Ease", WANN((2, 5), ["fruehstueck"]), "foredeck",
      P1("lea", ("toto", "?", "is coiling lines and pretending not to notice")),
      "Since yesterday, Lea salutes every time you walk past. On the foredeck, at breakfast, once from inside the "
      "tender. This morning she salutes, drops her coffee and salutes again.",
      [Z("lea", "Morning, sir! Duc. Sorry. Morning, Duc. I don't know why my hand does that. It just goes up.",
         "embarrassment")],
      [O("Steps closer and lowers her hand gently. “At ease, deckhand.”", [B("lea", 6), V("lea", 2), NK("lea")],
         zeile=Z("lea", "At ease. Right. I am so far from at ease. You have no idea.", "desire")),
       O("Salutes back, perfectly straight-faced.", [V("lea", 4), W("moral", 1)],
         zeile=Z("lea", "Oh, that's worse. Now I can't stop smiling either.", "joy")),
       O("Fetches her a new coffee.", [V("lea", 4)])],
      sets={"lea": "Deck"}, knistern=True),

    # ================================================================== Rosi
    E("fl_rosi_pfand", "gag1", "frech", "Loser Does What Winner Says", WANN((2, 6), TAG), "power_room",
      P1("rosi", ("toto", "?", "is taking bets outside the door and can't see in")),
      "Two identical faulty relays on the workbench. Rosi slides one over to you and keeps a screwdriver behind her ear "
      "like a weapon. The stake, she says, is one minute. Loser does whatever the winner says.",
      [Z("rosi", "One minute, Officer, and you do anything I say. Don't look at me like that, I haven't decided yet. I'll decide when I win.", "pride")],
      [O("Wins, just. “One minute. Tell me something you've never told anyone on this boat.”", [],
         probe=P("cunning", 12, "handwerk"), erfolg=[B("rosi", 6), V("rosi", 6), NK("rosi")], fehlschlag=[V("rosi", 2)],
         zeile=Z("rosi", "That's not fair, that's a question, not an order. …Fine. I talk to the generator when I'm "
                         "lonely. And lately I talk about you. Time's up.", "embarrassment")),
       O("Lets her win.", [B("rosi", 4), V("rosi", 2)],
         zeile=Z("rosi", "You let me win. I saw it. One minute: stand still and don't say anything. …Okay. That was "
                         "enough. Go away before I do something stupid.", "desire")),
       O("Calls it even, so nobody won.", [V("rosi", 6)],
         zeile=Z("rosi", "A draw, so nobody won. Hm, I like draws. Everyone keeps their minute for later.", "amusement"))],
      sets={"rosi": "Engine Room"}, knistern=True),

    E("fl_rosi_bandana", "gag1", "frech", "The Red Bandana", WANN((2, 6), ["nachmittag"]), "generator_room",
      P1("rosi", ("lola", "?", "is asleep on the galley bench")),
      "Unit-01 spits oil. Rosi takes the red bandana off her head without thinking and ties it round your forehead "
      "before the next spray. Then she notices how close she's standing.",
      [Z("rosi", "There, now you look like you know what you're doing. Don't get used to it, because it's on loan.", "pride"),
       Z("rosi", "…Your eyes are nicer with it on. That's a technical observation.", "embarrassment")],
      [O("“Then I'm keeping it.”", [B("rosi", 6), V("rosi", 2), NK("rosi")],
         zeile=Z("rosi", "You're keeping nothing. You can borrow it, every day, until I say so.", "desire")),
       O("Ties it back on her, carefully.", [B("rosi", 4), V("rosi", 4)],
         zeile=Z("rosi", "…Your hands are steady, that's good. Very good. Okay, go, Unit-01 is getting jealous.", "love")),
       O("Hands it back with a nod.", [V("rosi", 4)])],
      sets={"rosi": "Engine Room"}, knistern=True),

    E("fl_rosi_vespa", "handy", "frech", "First Ride", WANN((3, 6), ["abend"], bed=VT("rosi", 2)), ORT_DUC,
      H("rosi", "power_room", "nachricht"),
      "A photo from Rosi: an old green Vespa in a Catania street, her father leaning against it in the sun. Underneath, "
      "after a long pause, a message.",
      [Z("rosi", "Papa's Vespa. 🛵 If I ever get the workshop back, you get the first ride. On the back. You'll have to "
                 "hold on. Tight. That's physics. 😏", "desire")],
      [O("“Hold on where, exactly?”", [], probe=P("charm", 12), erfolg=[B("rosi", 8), V("rosi", 2), NK("rosi")],
         fehlschlag=[V("rosi", 2)],
         zeile=Z("rosi", "Where I say. I'm in front, I decide. 😤 …Officer, stop smiling at your phone, I can feel it from here.",
                 "amusement")),
       O("“Deal. First ride is mine.”", [B("rosi", 4), V("rosi", 4)]),
       O("“Your father looks proud.”", [V("rosi", 6)],
         zeile=Z("rosi", "He was. Of the Vespa. And me. Mostly the Vespa. 🥲 Goodnight.", "sadness"))],
      knistern=True),

    E("fl_rosi_schicksal", "gag1", "frech", "This Is My Destiny", WANN((3, 6), N, bed=VT("rosi", 2)), "generator_room",
      P1("rosi", ("maxwell", "?", "is snoring two decks up")),
      "Past midnight, under Unit-01, two torches, one tight space. Rosi tightens the last bolt, shouts \"THIS IS MY "
      "DESTINY!\" at the ceiling, turns her head, and finds your face ten centimetres from hers.",
      [Z("rosi", "That was – I yell that, at bolts. It's not about you. Mostly.", "embarrassment"),
       Z("rosi", "…You're not moving. Why aren't you moving?", "desire")],
      [O("Doesn't move.", [B("rosi", 8), V("rosi", 2), NK("rosi"), EN(-1)],
         zeile=Z("rosi", "Okay, nothing happened. Nothing happened, and I'm keeping score. Now get out before Unit-01 sees us, because she talks.", "love")),
       O("Slides out first and offers her a hand.", [V("rosi", 6), B("rosi", 2)],
         zeile=Z("rosi", "Such a gentleman. Ugh. Fine, thank you.", "gratitude")),
       O("“Your destiny's got oil on its nose.”", [], probe=P("charm", 11), erfolg=[B("rosi", 6), V("rosi", 4)],
         fehlschlag=[V("rosi", 2)],
         zeile=Z("rosi", "Then wipe it off. …Slowly. That's an order.", "amusement"))],
      sets={"rosi": "Engine Room"}, knistern=True),

    # ================================================================== Lola
    E("fl_lola_mehl", "gag1", "frech", "Flour", WANN((2, 6), N), "galley",
      P1("lola", ("chiara", "?", "is asleep and will never know")),
      "One in the morning, dough for tomorrow's bread. Lola laughs at something, flicks flour at you, misses, and hits "
      "your face anyway. Then she steps in close to wipe it off with her thumb. Very slowly.",
      [Z("lola", "Oops. Hold still, Boss. You've got a bit – there. And there. And… there was nothing there, I just "
                 "wanted to do that.", "desire")],
      [O("Flicks flour back.", [B("lola", 6), V("lola", 4), NK("lola")],
         zeile=Z("lola", "Oh, it's on now. Chiara's going to kill us, but it's worth it. Mostly the flour.", "joy")),
       O("Catches her wrist, gently.", [], probe=P("charm", 11), erfolg=[B("lola", 8), V("lola", 2), NK("lola")],
         fehlschlag=[V("lola", 2)],
         zeile=Z("lola", "Hi. Hello. Okay, the bread can wait. Bread is very patient.", "desire")),
       O("“The bread, Lola.”", [V("lola", 2)],
         zeile=Z("lola", "The bread, yes. You're no fun. You're a bit of fun.", "amusement"))],
      sets={"lola": "Galley"}, knistern=True),

    E("fl_lola_haengematte", "handy", "frech", "Room for Two. Ish.", WANN((2, 6), N, bed=VT("lola", 2)), "duc_cabin",
      H("lola", "sun_deck", "nachricht"),
      "A photo from Lola: her bare feet sticking out of a hammock on the sun deck, a sky full of stars behind them.",
      [Z("lola", "Hammock. 🌌 Stars. ✨ Room for two. Ish. Mostly ish. No pressure, Boss, just letting you know the "
                 "universe is available. 😇", "desire")],
      [O("Goes up to the sun deck.", [B("lola", 6), V("lola", 4), NK("lola"), EN(-1)],
         zeile=Z("lola", "You came! Careful, careful, it flips – oh, we're in. We're very in. Hi.", "joy")),
       O("“Tell me which stars you can see.”", [V("lola", 6)],
         zeile=Z("lola", "That one's the Saucepan. That's not its real name. Mostly the Saucepan. 🍳 Night, Boss. 🌙", "love")),
       O("Sends a sleeping emoji.", [V("lola", 2)])],
      knistern=True),

    E("fl_lola_bao", "gag1", "frech", "Hands-On Lesson", WANN((2, 6), ["nachmittag"]), "galley",
      P1("lola", ("jana", "?", "is eating the failed ones in the corner")),
      "Lola is teaching you to pleat bao. You're bad at it. She steps behind you, puts her hands over yours and folds "
      "with your fingers. Her chin is almost on your shoulder.",
      [Z("lola", "Pinch, turn, pinch, turn. No, gentle, like you mean it but you're not in a hurry. …You're getting it, so keep going. I'm staying right here.", "desire")],
      [O("Keeps going very slowly.", [B("lola", 6), V("lola", 4), NK("lola")],
         zeile=Z("lola", "Perfect, that's the best one you've done. I'm not letting go yet, for quality control.", "love")),
       O("Turns his head. “Like this?”", [], probe=P("courage", 12), erfolg=[B("lola", 8), V("lola", 2), NK("lola")],
         fehlschlag=[V("lola", 2), W("moral", 1)],
         zeile=Z("lola", "…Yeah, exactly like that. Jana, out, and take the bao. Take all the bao.", "desire")),
       O("Pleats one perfectly on his own.", [], probe=P("perception", 12, "kueche"),
         erfolg=[V("lola", 6), B("lola", 2)], fehlschlag=[V("lola", 2)],
         zeile=Z("lola", "Oh, you were faking being bad. You sneaky – that's hot, actually. Annoying and hot.",
                 "amusement"))],
      sets={"lola": "Galley", "jana": "jana_deck_a"}, knistern=True),

    E("fl_lola_sonnencreme", "gag1", "frech", "Backs Are Hard", WANN((2, 6), TAG, wetter=["klar"]), "sun_deck",
      P1("lola", ("maxwell", "?", "is doing push-ups at the far end with his eyes shut")),
      "Lola is lying on her front on the sun deck, holding a bottle of sun cream over her shoulder in your direction "
      "without looking. Her hair is pushed to one side.",
      [Z("lola", "Backs are hard, Boss. I can do arms and I can do legs, but the middle bit is a mystery, so help a girl out.", "desire")],
      [O("Takes the bottle and takes his time.", [B("lola", 6), V("lola", 2), NK("lola")],
         zeile=Z("lola", "Mmm, you've got good hands. Lower. No, higher. No – yeah, there. Don't stop.", "desire")),
       O("Does it quickly and hands back the bottle.", [V("lola", 4)],
         zeile=Z("lola", "Speedrun. Respect. Bit rude. Respect.", "amusement")),
       O("“Ask Maxwell. He loves a challenge.”", [V("lola", 2), V("maxwell", 2), W("moral", 1)])],
      sets={"lola": "lola_bikini"}, knistern=True),

    # ================================================================== Siri (Begehren erst nach siri_frei)
    E("fl_siri_blick", "gag1", "frech", "No Camera", WANN((2, 5), ["abend"], bed={"nicht": FREI}), "foredeck",
      P1("siri", ("yasin", "?", "is filming the sunset at the other end of the deck")),
      "Golden hour on the foredeck. Siri isn't posing for once. She catches you looking, and instead of the camera "
      "smile she gives you the other one, the crooked one. Then she looks away first.",
      [Z("siri", "Sorry. I was – that wasn't a look. It was a… sorry. Do you ever do that, look at someone by "
                 "accident?", "embarrassment")],
      [O("“All the time. Never by accident.”", [V("siri", 6), U("siri_marke", 1)],
         zeile=Z("siri", "…You can't say things like that to me. Not yet. Say them later.", "desire")),
       O("Looks at the sunset instead, smiling.", [V("siri", 4)]),
       O("“Your real smile is better.”", [V("siri", 6)],
         zeile=Z("siri", "Nobody's seen it in years. Don't tell my manager it exists.", "joy"))],
      sets={"siri": "Sea Siren"}, knistern=True),

    E("fl_siri_date", "handy", "frech", "Too Soon?", WANN((3, 6), N, bed=FREI), "duc_cabin",
      H("siri", "vip_cabin", "nachricht"),
      "A message from Siri. Then a second one, deleted. Then the first one again.",
      [Z("siri", "Is it too soon to ask you out? 🙈 Sorry. Delete that. Don't delete it. I mean a real one, no camera, no "
                 "Yasin. Just tea somewhere. Or a walk. Or whatever people do when they mean it. 🥺", "nervousness")],
      [O("“Not too soon. Tomorrow at sunset, the foredeck.”", [B("siri", 6), V("siri", 4), NK("siri")],
         zeile=Z("siri", "A real date. 🥹 I'm going to wear something nobody's paying me to wear.", "joy")),
       O("“Ask me again when you're sure.”", [V("siri", 4)],
         zeile=Z("siri", "That's fair. That's… kind. 🤍 I'll ask again. Soon.", "caring")),
       O("Sends a heart.", [B("siri", 2), V("siri", 2)])],
      knistern=True),

    E("fl_siri_schulter", "gag1", "frech", "Shoulder", WANN((3, 6), N, bed=FREI), "sun_deck",
      P1("siri", ("maxwell", "?", "is asleep on a lounger, snoring")),
      "Stars over the sun deck. Siri has been talking about her island for an hour, slower and quieter each time, until "
      "her head lands on your shoulder. She wakes up five minutes later and doesn't move.",
      [Z("siri", "Sorry. Sorry, I fell asleep on you. I'll move. …I'm not moving, am I? I'm really not moving.",
         "desire")],
      [O("“Stay.”", [B("siri", 8), V("siri", 4), NK("siri"), EN(-1)],
         zeile=Z("siri", "Okay. Staying. Don't say anything clever, I'll cry.", "love")),
       O("Tucks the blanket around her.", [V("siri", 6), B("siri", 2)]),
       O("Wakes Maxwell so he can carry her down.", [V("maxwell", 4), V("siri", -2)],
         zeile=Z("maxwell", "Mr. Maximum is a taxi now? Eish. Fine. For the princess.", "amusement"))],
      sets={"siri": "Dad's Sweater"}, knistern=True),

    # ================================================================== Megan (versteckte Romanze, nur mit megan_funke)
    E("fl_megan_palstek", "handy", "frech", "Behind Your Back", WANN((3, 4), ["abend"], bed=FUNKE), ORT_DUC,
      H("megan", "megan_office"),
      "Megan, on video, late, office lights low. She isn't talking about reports. She has a length of rope in her "
      "gloved hands and is tying a bowline without looking down.",
      [Z("megan", "In the hangar you offered to tie one of these behind your back. I've been practising. Mine's "
                  "faster.", "pride"),
       Z("megan", "That's all. That's the call. …Don't you dare tell anyone I called for that.", "embarrassment")],
      [O("Ties one on camera, behind his back.", [], probe=P("courage", 12, "handwerk"),
         erfolg=[V("megan", 8), F("megan_funke_2")], fehlschlag=[V("megan", 4)],
         zeile=Z("megan", "…Show-off. Same time tomorrow, First Officer. I'll be faster.", "desire")),
       O("“You didn't call for the knot, Mac.”", [V("megan", 6), F("megan_funke_2")],
         zeile=Z("megan", "It's Megan now. …No. I didn't.", "desire")),
       O("“Is this about work?”", [V("megan", -2)],
         zeile=Z("megan", "Of course it's about work. Goodnight.", "annoyance"))],
      sets={"megan": "Boardroom"}, knistern=True),

    E("fl_megan_privat", "handy", "frech", "Private Number", WANN((3, 5), N, bed=FUNKE), "duc_cabin",
      H("megan", "megan_office", "nachricht"),
      "Two in the morning. A message from a number you don't know. It has no signature. It doesn't need one.",
      [Z("megan", "This number is private. Nobody at Eden has it. Don't make me regret giving it to you.", "desire")],
      [O("“Goodnight, Megan.”", [V("megan", 6), F("megan_funke_2")],
         zeile=Z("megan", "You used my name. Good. Goodnight. 🖤", "caring")),
       O("“What are you wearing?”", [], probe=P("charm", 13), erfolg=[V("megan", 6), F("megan_funke_2")],
         fehlschlag=[V("megan", -4)],
         zeile=Z("megan", "Ambition. 💼 Go to sleep, First Officer.", "amusement")),
       O("Saves the number without answering.", [V("megan", 2)])],
      knistern=True),

    # ================================================================== Alva
    E("fl_alva_eis", "gag1", "frech", "Ice", WANN((2, 6), ["abend"], an_land=True, bed=VT("alva", 2)), "alvas_bar",
      P1("alva", ("petru", "?", "is watching football with his back to the bar")),
      "It's hot. Alva leans over the bar, fishes an ice cube out of your glass with two fingers and runs it slowly "
      "along the inside of her wrist, watching you the whole time.",
      [Z("alva", "Hot night, o figliolu. Everybody's welcome here. Nobody's mine. …Ask me why I'm looking at you, "
                 "then.", "desire")],
      [O("“Why are you looking at me?”", [B("alva", 6), V("alva", 4), NK("alva")],
         zeile=Z("alva", "Because you're the only man in here who hasn't asked me for anything. Yet.", "desire")),
       O("Takes the ice cube from her and drops it back in his glass.", [], probe=P("cunning", 12),
         erfolg=[B("alva", 8), V("alva", 2), NK("alva")], fehlschlag=[V("alva", 2)],
         zeile=Z("alva", "Bold. I like bold. It costs extra.", "amusement")),
       O("“Another myrtle, please.”", [V("alva", 2)])],
      sets={"alva": "alva_standard"}, knistern=True),

    E("fl_alva_tuer", "handy", "frech", "Last Orders", WANN((3, 6), N, bed=VT("alva", 2)), "duc_cabin",
      H("alva", "alvas_bar", "nachricht"),
      "A message from Alva, a photo of the bar's door, half open, light falling onto the cobbles.",
      [Z("alva", "Bar's closed. Door isn't. 🚪 I'm counting the till. It's a very boring job. 🥱 Somebody should make it "
                 "less boring. 😏", "desire")],
      [O("Rows over to the bar.", [B("alva", 6), V("alva", 4), NK("alva"), EN(-1)],
         zeile=Z("alva", "You rowed. In the dark. For me and a till. Sit. You can count the coins I drop.", "love")),
       O("“Count slower. Tell me the total in the morning.”", [V("alva", 4), B("alva", 2)],
         zeile=Z("alva", "Smart answer. Cowardly, but smart. 🐔", "amusement")),
       O("Sends a goodnight.", [V("alva", 2)])],
      knistern=True),

    E("fl_alva_schritt", "gag1", "frech", "One Step", WANN((3, 6), ["abend"], an_land=True, bed=VT("alva", 2)),
      "alvas_bar",
      P1("alva", ("toto", "?", "is outside arguing with a delivery van")),
      "The jukebox is silent, as always, but Alva hums. She pulls you off the bar stool by the collar and shows you one "
      "step. Just one. Her hand on your back says the rest.",
      [Z("alva", "Heel, then the floor, then you look at me like you've already won. No, at me. There.", "desire")],
      [O("Gets the step right.", [], probe=P("courage", 12), erfolg=[B("alva", 8), V("alva", 4), NK("alva")],
         fehlschlag=[B("alva", 2), W("moral", 1)],
         zeile=Z("alva", "…Again. Slower. I'm not finished with you.", "desire")),
       O("Gets it wrong on purpose so she has to show him again.", [B("alva", 6), V("alva", 2)],
         zeile=Z("alva", "You did that on purpose. Good. Again.", "amusement")),
       O("“I dance like a sailor, Alva.”", [V("alva", 4)],
         zeile=Z("alva", "Then hold on like one.", "amusement"))],
      sets={"alva": "alva_standard"}, knistern=True),

    # ================================================================== Chiara (allein, privat)
    E("fl_chiara_zehn", "gag1", "frech", "Out of Ten", WANN((3, 6), N, bed=VT("chiara", 2)), "bridge",
      P1("chiara", ("maxwell", "?", "is folding napkin swans in the mess, two decks down")),
      "The bridge at night, just the instrument lights. Chiara rates everything: the coffee, the moon, the anchor "
      "light. Then she stops in front of you with her arms folded.",
      [Z("chiara", "Coffee, six. Moon, eight. Too showy. And you, First Officer… no. You first. What would you give me? "
                   "Honestly.", "curiosity")],
      [O("“Ask me again on a night you're not working.”", [B("chiara", 6), V("chiara", 4), NK("chiara")],
         zeile=Z("chiara", "That's not a number, that's a date. …Seven for the answer. Maybe eight.", "desire")),
       O("“What would you want me to say?”", [V("chiara", 6), B("chiara", 2)],
         zeile=Z("chiara", "Nobody asks me what I want. Stop doing that. Don't stop doing that.", "love")),
       O("“Nine.”", [], probe=P("charm", 12), erfolg=[B("chiara", 8), V("chiara", 2)], fehlschlag=[V("chiara", -2)],
         zeile=Z("chiara", "Nine. Not ten? …Good. Ten is for later.", "amusement"))],
      sets={"chiara": "Bridge Night"}, knistern=True),

    E("fl_chiara_kragen", "gag1", "frech", "The Collar", WANN((2, 6), ["fruehstueck"]), "crew_corridor",
      P1("chiara", ("jana", "?", "practises the same move on a coat hanger, out of sight")),
      "In the crew corridor Chiara stops you with one finger on your chest. Your collar is crooked. She straightens it, "
      "then the other side, then the first side again, which was already straight.",
      [Z("chiara", "Uniform: four. Collar: crime. Hold still. …There. Now you look like someone I'd take orders from.",
         "desire")],
      [O("“You can let go now.”", [B("chiara", 4), V("chiara", 4)],
         zeile=Z("chiara", "I know, I'm letting go. Look, I'm letting go.", "embarrassment")),
       O("Straightens hers in return.", [], probe=P("courage", 11), erfolg=[B("chiara", 8), V("chiara", 2), NK("chiara")],
         fehlschlag=[V("chiara", 2)],
         zeile=Z("chiara", "…Oh. Okay, that's – we're even. Don't be late for the briefing.", "desire")),
       O("“Thanks, Chief.”", [V("chiara", 4)])],
      sets={"chiara": "Uniform"}, knistern=True),

    E("fl_chiara_tee", "handy", "frech", "Two Cups", WANN((3, 6), N, bed=VT("chiara", 2)), "duc_cabin",
      H("chiara", "bridge", "nachricht"),
      "A photo from Chiara: two cups of tea on the chart table, steam rising, one with a slice of lemon. No text. Then, "
      "a minute later, text.",
      [Z("chiara", "I made two by accident. ☕☕ Don't read anything into it. The lemon one is yours. 🍋 Accidentally.",
         "embarrassment")],
      [O("Goes up to the bridge.", [B("chiara", 6), V("chiara", 4), NK("chiara"), EN(-1)],
         zeile=Z("chiara", "You came for an accident. That's – sit. It's still warm. So am I. Forget I said that.",
                 "desire")),
       O("“Save it for me. Tomorrow night.”", [V("chiara", 4), B("chiara", 2)]),
       O("Sends a lemon emoji.", [V("chiara", 2)],
         zeile=Z("chiara", "A lemon. 🍋 Three out of ten. 😒 Goodnight.", "amusement"))],
      knistern=True),

    # ================================================================== Sophia
    E("fl_sophia_blick", "gag1", "frech", "Ten Seconds", WANN((2, 6), ["abend"]), "aft_deck",
      P1("sophia", ("lea", "?", "is asleep in a deckchair with a book on her face")),
      "Sophia puts a ten-euro note on the table between you. The bet: you can't hold her eye for ten seconds without "
      "looking away. Nobody has ever managed it, she says. She counts very slowly.",
      [Z("sophia", "One. Two. Darling, you're blinking. Three. That's allowed. Four…", "desire")],
      [O("Holds it all the way to ten.", [], probe=P("courage", 12), erfolg=[B("sophia", 8), V("sophia", 4), NK("sophia")],
         fehlschlag=[B("sophia", 2), G(-10)],
         zeile=Z("sophia", "…Ten. You win. Keep the money. I'll keep the rest of the evening.", "desire")),
       O("Looks away at seven, on purpose.", [B("sophia", 4), V("sophia", 4), G(-10)],
         zeile=Z("sophia", "You let me win. Nobody lets me win. That's the most dangerous thing you've done yet.",
                 "amusement")),
       O("“Double or nothing, and you count faster.”", [V("sophia", 4), B("sophia", 2)])],
      sets={"sophia": "Shore Leave"}, knistern=True),

    E("fl_sophia_ungeprobt", "handy", "frech", "Unscripted", WANN((3, 6), N, bed=VT("sophia", 2)), "duc_cabin",
      H("sophia", "aft_deck"),
      "Sophia on video, late, hair down, a cardigan over her shoulders. Halfway through a perfectly polished sentence "
      "she laughs, a real one, too loud, and covers her mouth.",
      [Z("sophia", "Oh no. That wasn't in the script. Pretend you didn't hear it, darling. …You heard it.", "embarrassment")],
      [O("“Do it again.”", [B("sophia", 6), V("sophia", 4), NK("sophia")],
         zeile=Z("sophia", "I can't do it on command. That's the whole problem with it. …Say something stupid.", "joy")),
       O("“That was the best line you've said all week.”", [], probe=P("charm", 12),
         erfolg=[B("sophia", 8), V("sophia", 2)], fehlschlag=[V("sophia", 2)],
         zeile=Z("sophia", "Careful. If you keep saying things like that, I'll stop performing for you altogether.",
                 "desire")),
       O("“Goodnight, Sophia.”", [V("sophia", 2)])],
      sets={"sophia": "Writing Night"}, knistern=True),

    # ================================================================== Jana (keine Romanze) und Elsa (kein Begehren)
    E("fl_jana_knoten", "gag1", "frech", "Bowline for Two", WANN((2, 6), TAG), "foredeck",
      P1("jana", ("toto", "?", "has turned his back and is shaking with laughter")),
      "Jana is practising knots. She is very fast now. So fast that she ties a bowline round her own waist and yours "
      "before either of you notices. You're standing very close. The knot is very good.",
      [Z("jana", "Jessas. Sorry, Sir. Sorry! That's – the rabbit came out of the hole and went round the wrong tree. "
                 "Two trees. You're a tree.", "embarrassment")],
      [O("“Untie it. Slowly. Show me how you did it.”", [V("jana", 6)],
         zeile=Z("jana", "Slowly. Yes. I can do slowly. I can do… okay. My hands are shaking. That's the knot's fault.",
                 "desire")),
       O("“It's a very good knot. Leave it a minute.”", [V("jana", 4), W("moral", 1)],
         zeile=Z("jana", "A minute. Okay. I'll count. Out loud. No, in my head. Na geh.", "joy")),
       O("Cuts it with his knife.", [V("jana", -2)],
         zeile=Z("jana", "That was a perfect bowline! …Sorry. Yes. Practical. Very practical, Sir.", "disappointment"))],
      sets={"jana": "jana_deck_a"}, knistern=True),

    E("fl_elsa_strafzettel", "gag1", "frech", "A Ticket for You", WANN((2, 6), TAG, an_land=True), "village_harbour",
      P1("elsa", ("toto", "?", "is hiding behind a crate, delighted")),
      "Elsa walks straight up to you on the quay, writes something on her pad, tears off the sheet and holds it out "
      "with a perfectly straight face.",
      [Z("elsa", "First Officer. Excessive charm in a working harbour. Two counts. The fishermen's wives are "
                 "distracted, and so, apparently, is the coast guard.", "amusement")],
      [O("“I'd like to contest it. Over dinner.”", [], probe=P("charm", 12), erfolg=[V("elsa", 8), F("elsa_dinner")],
         fehlschlag=[V("elsa", 2)],
         zeile=Z("elsa", "Contested. Noted. Dinner is not a legal procedure, First Officer. …Tomorrow, eight o'clock.", "desire")),
       O("Pays the fine with a fig.", [V("elsa", 6)],
         zeile=Z("elsa", "Respect, yes. Money, never. Figs are fine. Case closed.", "joy")),
       O("Signs it and hands it back.", [V("elsa", 4)])],
      knistern=True),

    # ================================================================== NSFW (Intim-Szenen wie Lola und Alva)
    E("ab_jana_nacht", "abend", "frech", "Nobody Has to Know", WANN((3, 6), N,
      bed={"alle": [VT("jana", 3), {"nicht": {"flag": "jana_abend"}}]}), "duc_cabin", {"pid": "jana"},
      "A knock, very quiet, then a second one, louder, as if she had to argue herself into it. Jana is standing in the "
      "corridor with her hair down and her arms wrapped round herself. She has clearly rehearsed something.",
      [Z("jana", "Sorry, Sir. Sorry. I know it's late. I'm not – this isn't a romance thing. I don't want a romance "
                 "thing. I just want one night where I'm not the quiet one.", "nervousness"),
       Z("jana", "And then tomorrow everything's normal. Nobody has to know. You can say no. I'll go and say sorry to "
                 "the door.", "desire")],
      [O("Lets her in.", [V("jana", 6), F("jana_abend"), EN(-1),
                          INTIM("jana", "duc_cabin", "jana_kitty_b", "jana",
                                "Jana is shy for exactly one minute and then surprisingly bold - she wanted to be caught "
                                "for once. A one-night thing, no romance, warm and a little clumsy; she checks in with a "
                                "nervous laugh and means it.")],
         zeile=Z("jana", "Okay. Okay. Don't laugh. Actually, you can laugh. Just not at me.", "desire")),
       O("Lets her in, but they only talk.", [V("jana", 8), F("jana_abend")],
         zeile=Z("jana", "Talking is good. Talking is also something I don't do. So it still counts.", "gratitude")),
       O("“Not tonight, Jana. But thank you for asking.”", [V("jana", 4)],
         zeile=Z("jana", "Thank you for asking back. …I mean answering. Sorry, door.", "embarrassment"))],
      sets={"jana": "jana_kitty_b"}, knistern=True,
      nachklang_text="In the morning Jana says “Morning, Sir” exactly like always, and then trips over the same rope "
                     "twice. Nobody notices. Lola notices."),

    E("ab_jana_handy", "abend", "frech", "Jana Texts: “Sorry. Again?”", WANN((4, 6), N,
      bed={"alle": [VT("jana", 3), {"flag": "jana_abend"}]}), "duc_cabin", {"pid": "jana"},
      "Three messages from Jana in a row. The first says “Sorry.” The second says “Again?” The third says “Sorry.”",
      [Z("jana", "Still not a romance thing. Promise. I just liked not being quiet. You choose where. I'll find it.",
         "desire")],
      [O("Chooses a place to meet.", [V("jana", 4),
                              INTIM("jana", "frei", "jana_kitty_b", "jana",
                                    "Jana again, less nervous, more mischievous; still no romance, just fun she chose. "
                                    "She checks in and laughs at herself.")],
         zeile=Z("jana", "On my way. Not running. Okay, running a bit.", "joy"), art="ort_waehlen"),
       O("Sends a kind no.", [V("jana", 4)], zeile=Z("jana", "Okay! Totally okay. Goodnight, Sir. Sorry.", "caring"))],
      sets={"jana": "jana_kitty_b"}),

    E("ab_megan_nacht", "abend", "frech", "Off the Record", WANN((5, 6), N,
      bed={"alle": [{"flag": "megan_besuch"}, FUNKE, VT("megan", 2), {"nicht": {"flag": "megan_abend"}}]}),
      "duc_cabin", {"pid": "megan"},
      "Long after midnight. Megan is standing in your doorway without her gloves, without her coat, without a single "
      "file in her hands. She doesn't come in. She waits to be asked.",
      [Z("megan", "Off the record, First Officer. For one night I am not the Eden Group. I'm the girl who sat behind you "
                  "in Statistics and never said anything.", "desire"),
       Z("megan", "In two days I judge your crew, and I'll be fair, and I'll be cold. That's why tonight is the only "
                  "night. You can close the door. I'd understand.", "caring")],
      [O("“Come in, Mac.”", [V("megan", 6), F("megan_abend"), EN(-1),
                             INTIM("megan", "duc_cabin", "Boardroom", "megan",
                                   "Megan, off the record for one night: she wants it and hates wanting it, takes control "
                                   "precisely and then lets go of it; dry humour, no villain voice. She checks in once, "
                                   "very directly, and leaves before anyone wakes.")],
         zeile=Z("megan", "It's Megan. …Tonight it's Mac.", "desire")),
       O("Lets her in, and they only talk until dawn.", [V("megan", 8), F("megan_abend"), NK("megan")],
         zeile=Z("megan", "Talking. You always were the dangerous one.", "love")),
       O("“Not while you're judging my crew.”", [V("megan", 4)],
         zeile=Z("megan", "…Correct answer. Infuriating, but correct. Goodnight, Duc.", "admiration"))],
      sets={"megan": "Boardroom"}, knistern=True,
      nachklang_text="At breakfast Megan is colder than ever. Under the table, for exactly one second, her shoe "
                     "touches yours."),
]
