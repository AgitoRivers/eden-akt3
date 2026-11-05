# -*- coding: utf-8 -*-
"""Bibis Tierstation "Mochi's" (Duc 31.10.2026, Wiki systeme/tierstation.md): die Tiere, ihre Seiten im Field Book und ihr Beistand.
Jedes Tier traegt ein ARK-Halsband, das es verrueckt macht (Duc 01.11.2026): Kaempfen, bis die Kraft fehlt, dann die Schlafgranate.

Regeln: kern/mochis.py. Kaempfe: kaempfe_mochis.py. Szenen: ereignisse_mochis.py. Alle Sprites gibt es schon (module/eden_rise/kampf).
ab = so viele Tage nach dem Quest-Ende (rt_ende_tag) ist die Spur da. futter = Zutaten aus der Speisekammer, die es liebt.
fund = was es morgens findet, wenn es an der Station lebt: ("r", Rohstoff) oder ("z", Zutat)."""

TIERE = {
    "hund": {
        "name": "Biscuit", "vorher": "A Collared Dog", "art": "Stray Dog", "sprite": "Dog", "ab": 2, "halsband": True,
        "futter": ["eggs", "chicken_meat"], "fund": [("z", "wildkraeuter"), ("z", "eggs"), ("r", "timber")],
        "gewicht": "Fourteen kilos. It should be twenty.",
        "narbe": "An old rope mark around the neck, and a fresh burn on top of it. The rope was somebody who left. The burn was ARK.",
        "gefunden": "Digs in the same three places every morning, and brings you whatever it finds. It is very proud of the sticks.",
        "besuch": ["Biscuit brings you a stick. Then a bigger stick. Then he sits on your foot.",
                   "He has gained two kilos. Bibi says it's three. He sleeps with one paw on your boot until you move.",
                   "He barks at a butterfly, looks at you to check it was the right thing, and barks again."],
        "aktion": {"wer": "Biscuit", "text": "Biscuit gets %(ziel)s by the leg.", "anteil": 0.06},
        "text_frei": "Biscuit looks back once at the gate, then runs. By the evening a fisherman is feeding a dog at the harbour, and says it isn't his.",
    },
    "hyaene": {
        "name": "Sorry", "vorher": "An Ark Hyena", "art": "Ark Hyena", "sprite": "ArkHyena", "ab": 4, "halsband": True,
        "futter": ["pork", "beef"], "fund": [("r", "leather"), ("r", "cork"), ("z", "wildkraeuter")],
        "gewicht": "Forty-one kilos. Lab tag 7-114. She laughs when she is afraid, so she laughs all day.",
        "narbe": "Burn marks under the collar, in a neat row. Somebody was counting.",
        "gefunden": "Bibi named her in one second. She sits next to Bibi when the two of them are scared, and nobody can tell who started it.",
        "besuch": ["Sorry doesn't come to the gate. She waits until you sit down, and then she sits a little closer than yesterday.",
                   "It's quiet in her pen today. Bibi says she hasn't laughed since breakfast. Bibi is crying a bit about it.",
                   "She laughs when you drop your keys. You look at her. It wasn't fear. She just thinks you're funny."],
        "aktion": {"wer": "Sorry", "text": "Sorry laughs and tears at %(ziel)s.", "anteil": 0.05, "state": "blutend"},
        "text_frei": "She stops at the edge of the macchia and laughs once, not very loud. It's the first time it has sounded like a joke.",
    },
    "mufflon": {
        "name": "Duchess", "vorher": "A Plated Mouflon", "art": "Plated Mouflon", "sprite": "PlatedMouflon", "ab": 5, "halsband": True,
        "futter": ["cabbage", "wildkraeuter"], "fund": [("r", "wool"), ("r", "granite"), ("z", "wildkraeuter")],
        "gewicht": "Fifty-eight kilos, and nine of those were steel. Danzel took the plates off himself and didn't say anything for an hour.",
        "narbe": "Bolt holes in the shoulder, closed now. Bibi cleans them every day. The fur is coming back.",
        "gefunden": "Danzel named her, because of the way she looks at people. She lets him measure her. Nobody else.",
        "besuch": ["Duchess looks at you for a long time. You feel you should have brought something. You feel you should have dressed better.",
                   "The fur on her shoulders has come back, a little lighter than the rest. Danzel is here again, measuring nothing.",
                   "She lets you stand next to her. She doesn't move. From her, that's a hug."],
        "aktion": {"wer": "Duchess", "text": "Duchess walks in front of you and stands there. Your next hit is halved.", "schutz": True},
        "text_frei": "She goes up the ridge at her own speed and doesn't look back. Duchesses don't. Danzel watches until she is very small.",
    },
    "affe": {
        "name": "Monsieur", "vorher": "A Collared Ape", "art": "Ape", "sprite": "Ape", "ab": 6, "halsband": True,
        "futter": ["zucchini", "tomaten", "potatoes"], "fund": [("r", "iron"), ("r", "cork"), ("z", "tomaten")],
        "gewicht": "Thirty-three kilos. He solved the lab's feeding puzzle in a week. It took Bibi two to notice.",
        "narbe": "A shaved patch behind the ear, and a small square scar under it. He doesn't let you look for long.",
        "gefunden": "Steals tools and returns them cleaner. Rosi says he can stay. Rosi has never said that about anyone.",
        "besuch": ["Monsieur checks your pockets, very politely, and gives back everything except the pen.",
                   "He has taken the gate latch apart and put it back together. It works better now. Bibi has stopped asking.",
                   "He holds out your pen. When you reach for it, he takes it away again. He seems to think this is the best thing ever."],
        "aktion": {"wer": "Monsieur", "text": "Monsieur throws a stone at %(ziel)s, and he doesn't miss.", "anteil": 0.1},
        "text_frei": "He takes one spanner with him. Next week you find a clean spanner on the rail of the yacht, and nobody saw who left it.",
    },
    "wolf": {
        "name": "Sunday", "vorher": "A Collared Wolf", "art": "Collared Wolf", "sprite": "Wolf", "ab": 7, "halsband": True,
        "futter": ["beef", "salmon_steak", "pork"], "fund": [("r", "leather"), ("r", "wool"), ("r", "timber")],
        "gewicht": "Thirty-six kilos. Bibi found her on a Sunday. She wouldn't take any food from a hand for three days.",
        "narbe": "A torn ear. That one isn't from the lab, it's from another wolf. Bibi thinks it's the best thing on her.",
        "gefunden": "She sleeps with her back to the wall and her eyes on the door. You've seen people do that. On the fourth day she slept facing you.",
        "besuch": ["Sunday watches you from the far wall. You leave the food and walk away, as Bibi told you. You don't look back. She eats.",
                   "She's a few steps closer than last time. You pretend not to notice. She pretends not to have moved.",
                   "You sit with your back to her for a while. When you get up, there's a warm patch in the grass right behind you."],
        "aktion": {"wer": "Sunday", "text": "Sunday comes in low and takes %(ziel)s from the side.", "anteil": 0.08, "state": "blutend"},
        "text_frei": "That night there are two voices up on the ridge. Bibi stands at the gate with her coffee and listens until it goes cold.",
    },
}

# Zweite Runde (Duc 01.11.2026): ARK-Tiere aus den Ortskapiteln und exotische Tiere aus der Anlage. wenn = zusaetzliche Bedingung fuer die Spur.
TIERE.update({
    "madame": {
        "name": "Madame", "vorher": "A Very Round Cat", "art": "Russian Blue", "sprite": "RussianBlue", "ab": 3, "halsband": True,
        "futter": ["salmon_steak", "chicken_meat"], "fund": [("z", "eggs"), ("z", "wildkraeuter"), ("r", "wool")],
        "gewicht": "Seven and a half kilos. Bibi has checked twice. It isn't the collar. It's just Madame.",
        "narbe": "Nothing. Not one mark on her. She lived on the director's desk. He put the collar on her himself, to show the staff it was safe.",
        "gefunden": "Sits on the feed sacks, so nobody can open them. Bibi feeds everyone else around her.",
        "besuch": ["Madame looks at your hand. You stroke her twice. She bites you, once, not hard. The visit is over.",
                   "She lies across the path, and every animal here walks around her. Even Sunday.",
                   "You find her asleep in your jacket. You didn't take your jacket off. You don't know how she did that."],
        "aktion": {"wer": "Madame", "text": "Madame lands on %(ziel)s with all of her weight.", "anteil": 0.06},
        "text_frei": "She walks out of the gate, sits down outside it, and looks back at you. Then she walks back in, very slowly, and sits down on Bibi's foot. She has decided.",   # Duc 05.11.2026: Madame bleibt
    },
    "rotpanda": {
        "name": "Rusty", "vorher": "Something Red in the Trees", "art": "Red Panda", "sprite": "RedPanda", "ab": 8, "halsband": True,
        "futter": ["wildkraeuter", "eggs"], "fund": [("z", "wildkraeuter"), ("r", "timber"), ("r", "cork")],
        "gewicht": "Five kilos. Came in a crate from somebody's private zoo. There was a ribbon on the crate.",
        "narbe": "The collar was made for a much bigger neck, so they took in the gap with tape. The fur under the tape never grew back.",
        "gefunden": "Stands up with both arms in the air when anything surprises him. He thinks this is terrifying. Everybody lets him think so.",
        "besuch": ["Rusty stands up with both arms in the air. You stand up with both arms in the air. He's very impressed.",
                   "He's up on the barn roof, and he can't get down. He's been there since breakfast. Bibi says he's fine.",
                   "He eats a leaf with both hands, and he watches you the whole time, in case you want it."],
        "aktion": {"wer": "Rusty", "text": "Rusty stands up, arms in the air. %(ziel)s stops to look. Your next hit is halved.", "schutz": True},
        "text_frei": "There are no red pandas on Corsica. There is one now. The village argues about it, and the children leave out eggs.",
    },
    "capybara": {
        "name": "Monday", "vorher": "A Big Wet Animal", "art": "Capybara", "sprite": "Capybara", "ab": 9, "halsband": True,
        "futter": ["cabbage", "zucchini", "wildkraeuter"], "fund": [("z", "wildkraeuter"), ("z", "zucchini"), ("r", "cork")],
        "gewicht": "Fifty-two kilos. Bibi found him on a Monday. Sunday has been in the next pen since then, and nobody planned that.",
        "narbe": "Chewed wire on the back teeth. He is the calmest animal there is, so they wanted to see how long it took. It took four days.",
        "gefunden": "Every animal here sleeps next to him at some point. He doesn't seem to notice. The dog uses him as a pillow.",
        "besuch": ["Monday is sitting in the trough. He looks at you. He goes on sitting in the trough.",
                   "Biscuit is asleep on him, and something small is asleep on Biscuit. Nobody moves. You stay a while.",
                   "You sit down next to him. Ten minutes later you notice your shoulders have come down. You didn't know they were up."],
        "aktion": {"wer": "Monday", "text": "Monday walks into %(ziel)s and keeps walking.", "anteil": 0.08},
        "text_frei": "He gets as far as the creek and stops. A month later there are ducks on him. He has never looked happier, as far as anyone can tell.",
    },
    "keiler": {
        "name": "Truffle", "vorher": "A Collared Boar", "art": "Wild Boar", "sprite": "WildschweinKeiler", "ab": 10, "halsband": True,
        "futter": ["potatoes", "zucchini", "eggs"], "fund": [("z", "potatoes"), ("z", "wildkraeuter"), ("r", "timber")],
        "gewicht": "A hundred and twenty kilos. A local boar. ARK needed something that was already on the island, so nobody would ask.",
        "narbe": "The collar left a groove all the way round. His sister broke hers on the monastery bridge. He has been looking for that bridge.",
        "gefunden": "Digs up everything. Bibi was angry, until he found the old well that nobody could find for eighty years.",
        "besuch": ["Truffle pushes you with his snout until you give him what is in your pocket. There's nothing in your pocket. He checks again.",
                   "He has dug a hole in the exact place Bibi told him not to. He's lying in it. He looks like the happiest thing on the island.",
                   "He leans on you. It's like a wall leaning on you. You lean back, and you both stay up."],
        "aktion": {"wer": "Truffle", "text": "Truffle hits %(ziel)s from the side at full speed.", "anteil": 0.1},
        "text_frei": "He trots into the macchia without looking back. Every autumn after that, someone finds a neat pile of truffles by the gate.",
    },
    "baerchen": {
        "name": "Pudding", "vorher": "A Bear Cub Alone", "art": "Bear Cub", "sprite": "BearCub", "ab": 11, "halsband": True, "wenn": {"flag": "bg_u1_fertig"},
        "futter": ["salmon_steak", "eggs", "potatoes"], "fund": [("z", "eggs"), ("z", "wildkraeuter"), ("r", "wool")],
        "gewicht": "Twenty-two kilos, and most of that is paws. Old Grey's smallest. It came down from the mountain by itself.",
        "narbe": "They made the collar in one size. It would have grown into the neck, the way it did with the mother. Bibi got there first.",
        "gefunden": "Follows whoever has a bucket. Falls over the bucket. Looks at the bucket as if the bucket did it.",
        "besuch": ["Pudding runs at you, doesn't stop in time, and sits down on your feet. It's pleased with how that went.",
                   "It's got its head stuck in a feed bowl. It walks around like that for a while, quite happily.",
                   "It climbs into your lap. It doesn't fit into your lap. It doesn't care, and you can't feel your legs."],
        "aktion": {"wer": "Pudding", "text": "Pudding swats %(ziel)s and is very surprised that it worked.", "anteil": 0.05},
        "text_frei": "Bibi drives it up to the high pasture herself. It looks back twice. Up in the alders, something big makes a sound, or maybe that's only the wind.",
    },
    "schildkroete": {
        "name": "Twelve", "vorher": "A Very Old Tortoise", "art": "Hermann's Tortoise", "sprite": "Tortoise", "ab": 12, "halsband": True,
        "futter": ["tomaten", "cabbage", "zucchini"], "fund": [("z", "tomaten"), ("r", "granite"), ("z", "wildkraeuter")],
        "gewicht": "Nine kilos, and about eighty years old. Number twelve of forty in a test about how long a collar battery lasts. The battery lost.",
        "narbe": "Someone painted the 12 on twice, because the first one wore off. Nobody knows what happened to the other thirty-nine. She's still looking.",
        "gefunden": "Nobody has seen Twelve move. But each morning she's somewhere else, usually where she shouldn't be.",
        "besuch": ["Twelve looks at you. You look at Twelve. After a while you check your watch. It has been eleven minutes.",
                   "You bring her a tomato. She starts walking towards it. You come back after lunch to see how it ended.",
                   "She's asleep on the path to the barn. Everybody steps over her. She was here before the barn, Bibi says, and she might be right."],
        "aktion": {"wer": "Twelve", "text": "Twelve bites %(ziel)s and doesn't let go.", "anteil": 0.07, "state": "blutend"},
        "text_frei": "Bibi opens the gate on a Monday. On Thursday Twelve is at the bend in the road. In the spring someone sees her up on the hill, still going, and still furious.",
    },
    "geier": {
        "name": "Bones", "vorher": "Something Big Over the Ridge", "art": "Bearded Vulture", "sprite": "BeardedVulture", "ab": 13, "halsband": True,
        "futter": ["pork", "beef", "chicken_meat"], "fund": [("r", "iron"), ("r", "leather"), ("r", "granite")],
        "gewicht": "Six kilos, and three metres from wing to wing. Wild. He came over the fence for the food bins. They needed a bird for the range test.",
        "narbe": "The rust colour on the chest isn't blood. He paints himself in red mud, every day, on purpose. Nobody here has any idea why.",
        "gefunden": "Carries things up high and drops them on the rocks, to see what's inside. So far: bones, a padlock, and Danzel's thermos.",
        "besuch": ["Bones drops a bone in front of you and looks at you. You think it's a present. Bibi says it's a warning.",
                   "He's on the top of the barn with his wings half open, in the sun. He looks like something from an old church.",
                   "You hold up a piece of meat. He takes it very gently. Then he takes your hat, and that wasn't as gentle."],
        "aktion": {"wer": "Bones", "text": "Something drops from high above onto %(ziel)s. It's a rock.", "anteil": 0.12},
        "text_frei": "He goes up in three slow circles and doesn't come back. But now and then a bone drops onto the quay, from very high up. The fishermen have stopped looking up.",
    },
    "schneeleopard": {
        "name": "Ghost", "vorher": "Tracks and Nothing Else", "art": "Snow Leopard", "sprite": "SnowLeopard", "ab": 15, "halsband": True,
        "futter": ["beef", "salmon_steak", "pork"], "fund": [("r", "wool"), ("r", "leather"), ("r", "iron")],
        "gewicht": "Forty kilos, Bibi thinks. Nobody has got close enough with a scale. From a private zoo. Somebody paid more for her than for this bay.",
        "narbe": "The fur on her paws is worn thin. A cage that was too small, for years. She has never seen snow. Corsica has some, up on the tops. Bibi looks up there a lot.",
        "gefunden": "You won't see her. You'll see the bowl is empty. You'll find a fresh print on the wall, higher than should be possible.",
        "besuch": ["You look for Ghost for a long time. She isn't there. When you turn to leave, she is on the wall behind you.",
                   "She lets you see her today. Just the tail, hanging over the top of the rocks, moving a little.",
                   "You sit down and wait. Nothing happens. When you get up, there are prints all around where you were sitting."],
        "aktion": {"wer": "Ghost", "text": "You didn't see where she came from. %(ziel)s did, for a moment.", "anteil": 0.11, "state": "blutend"},
        "text_frei": "Nobody sees her leave. That winter a shepherd comes down from the top of Monte Cinto, and he won't say what he saw in the snow, but he's smiling.",
    },
    "waran": {
        "name": "Mr. V.", "vorher": "Something Long in the Sun", "art": "Komodo Dragon", "sprite": "Komodo", "ab": 17, "halsband": True,
        "futter": ["beef", "pork", "salmon_steak"], "fund": [("r", "iron"), ("r", "leather"), ("z", "eggs")],
        "gewicht": "Ninety kilos. Bought for a rich man's collection, and it came with a certificate. Charly named him back at the lab. He's cold, he's never in a hurry, and he lies on everything he owns.",
        "narbe": "None you can see. The collar didn't change him much, Bibi says. That's the part she doesn't like to think about.",
        "gefunden": "Lies in the best sun on the whole hill. Nobody told him it was his. Nobody has told him it isn't.",
        "besuch": ["Mr. V. opens one eye. He looks at you as if he has already read your file. He closes the eye.",
                   "He has moved four metres since last time. It was to the place you were going to stand.",
                   "You offer him an egg. He looks at it, and at you, for a long time. Then he takes it, and you feel you've agreed to something."],
        "aktion": {"wer": "Mr. V.", "text": "Mr. V. bites %(ziel)s once and just waits. He's in no hurry.", "anteil": 0.06, "state": "blutend"},
        "text_frei": "It takes him all day to reach the gate, and he doesn't thank anyone. Three weeks later a very expensive villa reports a very large lizard in the pool.",
    },
})

# Seiten ohne Spur: Mochi kommt von selbst oder gar nicht (Wiki welt/belagerung.md). Old Grey und der Black Beast haben ihr Ende schon in den Bergen (ortskapitel_berge.md).
# zeilen: Flag -> Text, die erste passende gilt. Ohne passendes Flag keine Seite. frei = Flags, bei denen das Tier ohne Halsband lebt (Stationsbild).
SEITEN = {
    "mochi": {"name": "Mochi", "art": "Black Lion", "sprite": "LionAlpha",
              "gewicht": "A hundred and ninety kilos, the last time she weighed him. A bad tooth on the left side.",
              "zeilen": {"kl_loewe_frei": "Nobody looks at his teeth now. That's what you gave him.",
                         "kl_loewe_erloest": "She keeps this page anyway. She fills the bowl anyway."}},
    "old_grey": {"name": "Old Grey", "art": "Grizzly", "sprite": "GrizzlyAlpha", "sprite_frei": "GrizzlyFrei",
                 "gewicht": "Nobody ever weighed her. The collar had grown so deep that the fur had closed over the light.",
                 "zeilen": {"bg_baer_frei": "She stayed up there, with the chip out of her neck. Bibi drew her from what you told her, and she got the muzzle right.",
                            "bg_baer_getoetet": "Bibi drew this one from what you told her. She didn't ask you how it ended. She drew the cubs in the corner."},
                 "frei": ["bg_baer_frei"]},
    "beast": {"name": "The Black Beast", "art": "Black Panther", "sprite": "PantherAlpha",
              "gewicht": "Thin to the bone, you said. Bibi wrote that down, and then she didn't write anything for a while.",
              "zeilen": {"bg_panther_erloest": "It was awake when it ended. Bibi says that's more than most of them got.",
                         "bg_panther_gehetzt": "The chip burned out on the ridge. She asks you where, exactly. She goes up there alone and stays until dark."}},
}

FUTTER_GELD = 15           # Bibis einfaches Futter, wenn nichts Passendes in der Speisekammer liegt: dauert einen Tag laenger
TAGE_FUTTER = 1            # gesund einen Tag nach dem Lieblingsfutter
TAGE_EINFACH = 2           # ... und zwei Tage nach dem einfachen
KOEDER_RUNDEN = 1          # Lieblingsfutter dabei: das Tier frisst erst und setzt eine Runde aus
GRANATEN = 2               # so viele Schlafgranaten gibt Bibi je Spur; was uebrig bleibt, geht zurueck (kern/mochis.kampf_ende)
GRANATE = "grenade_sleep"
STUFE_AB = {2: 3, 3: 8}    # Bindung: gemeinsame Kaempfe bis Stufe 2 und 3
HALSBAND_ZIEL = 3          # so viele Halsbaender, und Bibi bringt sie zu Elsa (mo_halsband_3)
AUSBAU_AB = 5              # so viele gerettete Tiere, dann zeigt die Station den Ausbau statt des Anfangsbilds
BILD_ANFANG = "eden_rise_mochis_station.png"
BILD_VOLL = "eden_rise_mochis_station_voll.png"

# Epilog (Duc 01.11.2026): Am letzten Tag oeffnet Bibi die Tore. Je Tier ihr letztes Wiegen, die Antwort auf das Gewicht aus dem Field Book. wort = him/her/it fuer den Knopf.
ABSCHIED = {
    "hund": ("him", "Twenty-one kilos. I said twenty, and you went over, you big biscuit. I'm not sorry. Go on, go!", "joy"),
    "madame": ("her", "Seven and a half kilos, exactly the same as the day she came. Go on, Madame. ...She's sitting on my foot. She's sitting on my foot! Fine. Fine! You're staff now. Unpaid.", "amusement"),   # bleibt (Duc 05.11.2026)
    "hyaene": ("her", "Forty-eight kilos. Ha. Did you hear that? That one was real. She meant it. ...Sorry. I do that.", "gratitude"),
    "mufflon": ("her", "Fifty-four kilos, and now all of it is her. There's no steel left on her. I won't tell you to look back, Your Grace. You never do.", "caring"),
    "affe": ("him", "Thirty-seven kilos. Yes, that's Petru's spanner. No, let him have it. He'll bring it back when he has finished with it.", "amusement"),
    "wolf": ("her", "Forty-one kilos. She never took food from my hand, not once in all these weeks. I think that's the best thing about her.", "gratitude"),
    "rotpanda": ("him", "Six kilos. He raised both arms at me this morning, to scare me. I was very scared, Rusty. Go on, you terrible animal.", "joy"),
    "capybara": ("him", "Sixty kilos. There's no rush, Monday. You can take all day. ...You're going to take all day, aren't you?", "amusement"),
    "keiler": ("him", "A hundred and thirty-one kilos, and I'm not going to ask how many of those were truffles. Go on. Go and dig.", "joy"),
    "baerchen": ("it", "Forty kilos, and it's still mostly paws. It won't remember any of this. That was the whole idea. Go on, Pudding. Go on. ...Please go on.", "sadness"),
    "schildkroete": ("her", "Nine kilos, the same as ever. She's still looking for the other thirty-nine, you know. I hope she finds a few of them.", "caring"),
    "geier": ("him", "Six kilos, still. He looked at my skeleton one last time this morning. Go on, you horrible bird. I'll miss you.", "joy"),
    "schneeleopard": ("her", "I never did find out what she weighs. I left her gate open last night, and this morning she had gone. Well. Goodbye, Ghost, I suppose.", "admiration"),
    "waran": ("him", "Ninety-one kilos. That's one whole kilo, in all this time. It's a very big island, Mr. V. Please don't eat anyone important.", "amusement"),
}

# Fang (Duc 01.11.2026, Wiki systeme/tierstation.md): erster Fang = Overlay von Bibi (zeilen, vertont: Kommentar, Fun Fact, Name, Dank), zweiter Fang = Handy (zweit, getippt).
# Mehr als zwei gibt es nicht. allein = es gibt nur dieses eine (kein zweiter Fang), der zweite Fakt kommt dort mit dem ersten Besuch. szene = was bei der Rettung passiert ist, steht im Field Book.
FANG = {'hund': {'szene': "Bibi cuts the box off the collar and checks its teeth. It sleeps through all of it. When it wakes up, it's looking at you, and it's only a dog.",
          'zeilen': [('bibi', "Fourteen kilos. It should be twenty. Look at you, you're just a big biscuit, aren't you? Ha! Yes. That's your name now. Sorry.", 'joy'),
                     ('bibi',
                      "Did you know no two dogs have the same nose? The lines on it work like your fingerprints. So thank you. That nose is one of a kind, and now it's "
                      'safe.',
                      'gratitude')],
          'fakt': 'No two dogs have the same nose. The lines on it work like fingerprints.',
          'fakt2': 'A happy dog wags more to its right side. Scientists have measured it.',
          'zweit': ['biscuit has company!! 🐕🐕',
                    "another stray, same stupid box on the collar. it's off now",
                    "he's thrilled. he brought her a stick. then a bigger stick",
                    "fun fact: a happy dog wags more to its right side. people measured this. i've been checking all morning 😂",
                    'thank you. really']},
 'madame': {'szene': 'Bibi cuts the collar and picks her up with both arms, because you need both arms. Madame opens one green eye, looks at you, and remembers you.',
            'zeilen': [('bibi', "Seven and a half kilos. It isn't the collar. It's just her. Hello, Madame. You look terrible. Ha!", 'joy'),
                       ('bibi',
                        "Her fur is so thick that you can draw in it with a finger, and the picture stays. She hates that. Thank you. I never thought I'd get her back.",
                        'gratitude')],
            'fakt': "A Russian Blue's coat is so thick that a line drawn in it with a finger stays there.",
            'fakt2': 'The breed came off ships from the port of Arkhangelsk in Russia. Sailors called them Archangel Cats.',
            'allein': True},
 'hyaene': {'szene': 'The hyena lies on the stones with her sides going in and out. Bibi cuts the collar and sits down next to her, not too close. After a while she '
                     'starts to laugh too, very quietly.',
            'zeilen': [('bibi', 'Ha ha ha ha! ...Sorry. I do that.', 'nervousness'),
                       ('bibi', "...Sorry. Yeah. That's her name, isn't it? Hello, Sorry.", 'gratitude'),
                       ('bibi',
                        'You know what that laugh really is? Other hyenas can hear in it how old she is and how much she matters. I listened to her for two years and '
                        'never understood a word. Thank you for getting her out.',
                        'remorse')],
            'fakt': "A hyena's laugh tells the others its age and its rank.",
            'fakt2': 'In a hyena clan the females are in charge. Even a cub outranks a grown male from outside.',
            'zweit': ['sorry has a friend',
                      'a second one, same block in the lab. they sat next to each other and laughed at nothing for an hour. i cried a bit. normal',
                      'fun fact: in a hyena clan the females are in charge. even a cub outranks a grown male from outside',
                      'so this is her clan now. you and me work for her 😅']},
 'mufflon': {'szene': 'Danzel came up the hill with a bag of tools, though nobody asked him to. He takes the plates off one bolt at a time while she sleeps, and his '
                      "hands are completely steady. It's the first time you've seen that. Bibi cuts the collar last.",
             'zeilen': [('bibi',
                         "Fifty-eight kilos, and nine of those were steel. She's going to look at you like that for the rest of your life, by the way.",
                         'caring'),
                        ('danzel', "Your Grace. Hold still, please. I made this. I'm taking it back.", 'remorse'),
                        ('bibi',
                         'Danzel calls her Duchess, and nobody is going to argue. Her kind has been on Corsica for about eight thousand years, so she was here long '
                         'before any of us. Thank you for that.',
                         'gratitude')],
             'fakt': 'Mouflon have lived on Corsica for about eight thousand years. They are among the ancestors of our sheep.',
             'fakt2': "You can read a mouflon's age in its horns. Every year leaves a ring, like in a tree.",
             'allein': True},
 'affe': {'szene': "He wakes up on Bibi's blanket with no collar on. He takes the food out of your hand and sniffs it. Then he feels the shaved patch behind his ear, "
                   'and he looks at Bibi, and she looks at the ground.',
          'zeilen': [('bibi', 'I never knew what that scar was for. I signed the sheets. I signed all the sheets.', 'remorse'),
                     ('bibi', "Well, Monsieur? Are you coming? ...He's taking your sandwich with him. I think that's a yes.", 'gratitude'),
                     ('bibi',
                      "Did you know apes laugh when you tickle them? It's real laughing, people have recorded it. I'm going to find out if he still can. Thank you for "
                      'that.',
                      'gratitude')],
          'fakt': 'Great apes laugh when you tickle them. It has been recorded, and it sounds a lot like us.',
          'fakt2': 'Great apes build a fresh bed of branches almost every night.',
          'zweit': ['monsieur has a colleague 🐒 second ape, same scar',
                    'he showed her the feeding puzzle. she solved it. now they both look at me and i feel like the test',
                    'fun fact: apes build a new bed of branches almost every single night',
                    "he made one. out of petru's rope. please don't tell petru 🙈"]},
 'wolf': {'szene': "She sleeps with her eyes half open. Bibi cuts the collar without touching anything else, and it's the most careful thing you've ever seen anyone do. "
                   "Later she wakes up a few steps away from you. She doesn't come closer, and she doesn't leave.",
          'zeilen': [('bibi',
                      "Thirty-six kilos. Do you know what day it is? It's Sunday. It was always Sunday in the lab, I think. It was the only day nobody came in.",
                      'caring'),
                     ('bibi', "She won't eat from your hand, so don't ask her to. Just leave it and walk away. Come on, Sunday.", 'gratitude'),
                     ('bibi',
                      'People say wolves have an alpha, but that idea came from wolves kept in cages. Out there, a pack is just a family. Thank you. I think she needed '
                      "somebody who didn't try to own her.",
                      'gratitude')],
          'fakt': 'The idea of the alpha wolf came from studies of wolves in cages. A wild pack is a family.',
          'fakt2': 'Every wolf has its own howl, and the others can tell who is calling.',
          'allein': True},
 'rotpanda': {'szene': "He sleeps in Bibi's jacket on the way down. She has cut off the collar and the tape. He wakes up once, sees you, and raises both arms. Then he "
                       'goes back to sleep.',
              'zeilen': [('bibi', "Five kilos. Yes, you're very scary. Look how scary he is. Rust all over him, the poor thing. Rusty. All right, Rusty.", 'caring'),
                         ('bibi',
                          "He's the first panda, you know. People called him that long before anyone in Europe had seen the big black and white one. Thank you. He's had "
                          'a terrible month and he still wants to fight me.',
                          'joy')],
              'fakt': 'The red panda was called a panda decades before the giant panda. The big one took the name from him.',
              'fakt2': 'A red panda has a false thumb, a long wrist bone for holding bamboo.',
              'allein': True},
 'capybara': {'szene': "He wakes up in the shallows with no collar on. He looks at the water, and at the sky, and at Bibi. He doesn't do anything else, and he goes on "
                       "not doing anything for the rest of the afternoon. It's beautiful.",
              'zeilen': [('bibi',
                          "Fifty-two kilos. It's a Monday. Sunday's going to hate this. Come on, Monday. No rush. No, really. There's no rush at all now.",
                          'gratitude'),
                         ('bibi',
                          "Here's one for you. In Venezuela the church once decided that he counts as a fish, so people could eat him in Lent, the weeks with no meat. A "
                          'fish! Thank you for getting him out.',
                          'amusement')],
              'fakt': 'In Venezuela the church once decided that a capybara counts as a fish, so people could eat it in Lent.',
              'fakt2': 'A capybara can stay under water for about five minutes, and it can sleep with only its nose out.',
              'zweit': ['monday has a tuesday 😂',
                        "yes i'm calling her tuesday. she got in the pond and he moved over a bit. that's it. that's the whole story",
                        'fun fact: they can stay under water for five minutes, and they sleep with just the nose out',
                        'a duck has landed on them. nobody reacted']},
 'keiler': {'szene': "Bibi cuts the collar with bolt cutters. It takes both of you. He wakes up, snorts once, starts digging, and he finds something, and he's happy. It "
                     'really is that quick with him.',
            'zeilen': [('bibi',
                        "A hundred and twenty kilos. Oh, you're digging already. What is that? Is that a truffle? You're worth more than the whole station, do you know "
                        'that? Truffle. There you go.',
                        'joy'),
                       ('bibi',
                        "Do you know why pigs find truffles? To a pig, a truffle smells like another pig in love. He's going to be so disappointed. Thank you, and "
                        "please don't tell Nonna how we found this.",
                        'amusement')],
            'fakt': 'Pigs find truffles because to them a truffle smells like another pig looking for love.',
            'fakt2': 'Wild boars are strong swimmers. People have seen them far out at sea.',
            'zweit': ['truffle brought a friend 🐗',
                      'another boar, another collar. they dug up the whole east pen in one night',
                      'fun fact: boars are great swimmers, people have seen them far out at sea',
                      'so if your boat ever grunts. you know']},
 'baerchen': {'szene': "It sleeps on its back with all four paws in the air. The collar comes off easily. There's only a bare ring in the fur, and it's not deep yet. "
                       'Bibi holds that ring for a moment with her thumb.',
              'zeilen': [('bibi',
                          "Twenty-two kilos, and most of that is paws. You're not going to remember any of this, you know that? That's the idea. That's the whole idea. "
                          'Hello, Pudding.',
                          'gratitude'),
                         ('bibi',
                          'A bear is born while its mother is asleep, and it weighs about as much as two packs of butter. Look at this one now. Thank you. You were so '
                          'careful with it.',
                          'gratitude')],
              'fakt': 'A bear is born while its mother sleeps, and it weighs about as much as two packs of butter.',
              'fakt2': 'Bear cubs hum when they drink, like a small motor.',
              'zweit': ["pudding has a brother or a sister, i can't check, it bites 🐻",
                        "second cub from up the mountain. old grey's too, i think",
                        'fun fact: bear cubs hum when they drink. like a little motor',
                        "they're both humming right now. i'm holding the phone next to them. can you hear it. no. sorry"]},
 'schildkroete': {'szene': 'Bibi cuts the collar and sits down on the path, and she waits. It takes a very long time. Finally one small black eye opens, looks at you '
                           "both, and it's not grateful at all.",
                  'zeilen': [('bibi',
                              "Nine kilos, and about eighty years old. She was here before all of us. She'll be here after. Hello, Twelve. Sorry about the paint. I "
                              "can't get it off. I tried.",
                              'caring'),
                             ('bibi',
                              'Everyone thinks a shell is like armour, but she can feel it. There are nerves in it, so she knew when I was scratching at the paint. '
                              "Thank you. I think. She hasn't decided yet.",
                              'amusement')],
                  'fakt': 'A tortoise can feel through its shell. There are nerves in it.',
                  'fakt2': 'The weather decides if a tortoise egg hatches male or female. A warm nest makes females, a cool nest makes males.',
                  'zweit': ['twelve found one 🐢 number thirty-one!! THIRTY-ONE',
                            "she walked right up to her and just stood there. it took an hour. i think it was the happiest hour of anyone's life",
                            'fun fact: the weather decides if a tortoise egg hatches male or female. warm nest, girls. cool nest, boys',
                            'two of forty. keep looking, please']},
 'geier': {'szene': "Up close, he's the size of a child. Bibi cuts the thin steel collar under the rust-red feathers, and she doesn't breathe until it's done. When he "
                    "wakes up, he looks at the two of you, without hurry, as if he's working out how you'd break.",
           'zeilen': [('bibi',
                       "Six kilos. Three metres of wing, and six kilos! He's mostly air and bad temper. He eats bones, you know. Only bones. Hello, Bones. Don't look at "
                       'me like that, I have a good skeleton.',
                       'joy'),
                      ('bibi',
                       "That rust colour isn't really his, you know. He rolls in red mud on purpose, so it's make-up. Thank you. I've wanted to meet him since the day "
                       'he robbed my food bins.',
                       'joy')],
           'fakt': 'The rust colour of a bearded vulture is make-up. It rolls in red mud full of iron on purpose.',
           'fakt2': 'The Greek writer Aeschylus is said to have died when a bird dropped a tortoise on his head. Many think it was a bearded vulture.',
           'zweit': ['bones has company 🦴',
                     "another huge one. they haven't said a word. they just look at my skeleton together",
                     'fun fact: long ago a greek writer called aeschylus died when a bird dropped a tortoise on his head. people think it was one of these',
                     "i'm keeping twelve's pen far away from his. just saying"]},
 'schneeleopard': {'szene': 'She sleeps on the stone with her long tail around her, and for the first time you can really look at her. You understand what somebody paid '
                            "for. Bibi cuts the collar, and her hands shake, and she isn't scared.",
                   'zeilen': [('bibi',
                               "I don't know what she weighs, and I'm not going to find out. Look at her paws. She has never even seen snow. We've got some, you know. "
                               "Up at the top. Ghost, I think. Because that's all anyone's going to see.",
                               'admiration'),
                              ('bibi',
                               "And here's the strange part: she can't roar. All that cat, and the biggest noise she has is a sort of friendly puff. Thank you. Nobody "
                               'else on this island could have brought her down alive.',
                               'admiration')],
                   'fakt': "A snow leopard can't roar. Its friendly greeting is a soft puff through the nose.",
                   'fakt2': 'Its tail is almost as long as its body. It sleeps with the tail around its face like a scarf.',
                   'allein': True},
 'waran': {'szene': 'Cutting the collar takes a minute. It seems to change nothing at all. When he wakes up, he just looks at the two of you, and flicks out his long '
                    'tongue, and goes back to lying in the sun.',
           'zeilen': [('bibi',
                       "Ninety kilos. Every other animal I took a collar off, something came back into its eyes. Him? Look at him. I don't think that was the collar. "
                       "Come on, Mr. V. We've got a very good rock for you.",
                       'nervousness'),
                      ('bibi',
                       'That tongue is how he smells. It has two points, so he knows if a smell is on his left or on his right. He has known exactly where you were the '
                       'whole time. Thank you, I think. Go and wash.',
                       'nervousness')],
           'fakt': 'A Komodo dragon smells with its tongue. The two points tell it if a smell is on the left or on the right.',
           'fakt2': 'A female Komodo dragon can lay eggs with no male at all. It happened in a zoo in England.',
           'zweit': ['bad news for mr. v 🦎 the new one is a female',
                     'fun fact: komodo females can lay eggs with no male at all. it happened in a zoo in england',
                     "so he's not needed. he hasn't noticed. he's on his rock",
                     "charly wants to call her mrs. v. i said she doesn't need the name either 😂"]}}
for _t, _f in FANG.items():
    TIERE[_t].update(_f)

WIEDER_TAGE = 4            # so viele Tage nach einem Fang hoert Bibi von einem weiteren Tier derselben Art

# Bibis Selfie je Tier (Duc 02.11.2026): Bild /selfie/bibi_fang_<tier>.webp, fehlt es, zeigt das Field Book nichts
SELFIE = {
    "hund": "look who's a good boy 🐶 he's been licking my ear for an hour",
    "hyaene": "she laughed. i laughed. we are both fine 🙃",
    "mufflon": "no plates on her now!! don't tell her i said she's pretty",
    "affe": "he took the phone off me and took this himself. i'm not joking",
    "wolf": "she is asleep. i am very brave. don't look at the teeth",
    "madame": "she let me take ONE. then she looked at me like i owe her rent",
    "rotpanda": "he's doing the arms again 😂 terrifying",
    "capybara": "he sat on me. i live here now",
    "keiler": "i asked him to smile. this is him smiling",
    "baerchen": "i'm not crying, you're crying 🐻",
    "schildkroete": "this photo took forty minutes. she was walking the whole time",
    "geier": "don't ask what's in his beak",
    "schneeleopard": "she's in this photo. i swear. look at the rocks",
    "waran": "this is as close as i go. he has not moved since tuesday"
}
for _t, _s in SELFIE.items():
    TIERE[_t]["selfie"] = _s

# Bibis Tier-Selfies als kleine Szene A, dann B (Duc 02.11.2026, Bilder von Interaction Mechanic): selfie_titel = Polaroid-Boden
# je Bild (handgeschrieben, hoechstens 8 Woerter), log = ihre Notiz im Field Book danach. Noch nicht angebunden.
SELFIE_SZENE = {
    "hund": (["he says hello. with his whole tongue", "help. i live in the straw now"],
             "biscuit 1, bibi 0. he won by lying on me. i let him win. mostly."),
    "hyaene": (["we laughed at the same time!!", "my best joke. she yawned."],
               "sorry laughed with me today. not scared laughing, real laughing. then she yawned at my second joke. tough crowd."),
    "affe": (["no. no. it's MY phone", "photo by monsieur. i've been replaced"],
             "monsieur took my phone and took a better selfie than me. he gave the phone back. he did not give back your pen."),
    "mufflon": (["her majesty, duchess 👑", "she's eating my scarf. royally."],
                "duchess ate half my scarf. i think it means she likes me. danzel says it means she likes the scarf."),
    "rotpanda": (["very scary. please don't eat me", "the terrifying beast, off duty"],
                 "rusty did the arms at me for ten minutes. then he fell asleep in my lap, belly up. most dangerous animal on the island."),
    "keiler": (["this is his nice face. promise", "shh. he's being gentle 🍎"],
               "truffle took the apple like it was glass. a hundred and twenty kilos of good manners. don't tell him, he has a reputation."),
    "madame": (["she does not approve of me", "new hat. still does not approve"],
               "madame sat on my head for twenty minutes. she still doesn't like me. she just likes being higher than everyone."),
    "geier": (["what is in your beak, sir", "a present. thank you. i love it."],
              "bones gave me a bone. danzel says it's a warning. it's on my shelf now, and i'm keeping it."),
    "capybara": (["i am wearing a capybara today", "bath time. we have the same face"],
                 "sat in the trough with monday for an hour. we didn't talk. best meeting i've had all year."),
    "waran": (["this is my safe distance", "he looks better in my sunglasses"],
              "mr. v. has my sunglasses now. i'm not asking for them back. he looks better in them anyway."),
    "schildkroete": (["she's leaving. any minute now.", "an hour later. still leaving."],
                     "twelve walked out of the photo. i went for a coffee, came back, and she was still walking out of it."),
    "wolf": (["she's asleep. i'm calm. totally calm.", "don't breathe. don't breathe. don't breathe."],
             "sunday put her head in my lap today. i didn't move for forty minutes. my leg is still asleep. worth it."),
    "baerchen": (["asleep on me. i'm fine. i'm crying", "it ate my lion. the betrayal 🦁"],
                 "pudding fell asleep on me and i cried a bit. then it woke up and ate my lion. we're still friends. the lion is not."),
    "schneeleopard": (["she's here. somewhere. trust me.", "she was behind me THE WHOLE TIME"],
                      "i took a photo to show you she was on the rocks. she was right behind me. i didn't hear a thing. light on tonight."),
}
for _t, (_titel, _log) in SELFIE_SZENE.items():
    TIERE[_t]["selfie_titel"] = _titel
    TIERE[_t]["log"] = _log

# Ducs Seite im Field Book (Bibis Gestaendnis, rm_b4): Umriss ab Begehren 4, ganze Seite mit bibi_seite (kern/mochis._duc_karte)
DUC_SEITE = {
    "name": "Spatz",
    "gestrichen": [
        "Clipboard",
        "Mon lapin",
        "Hase",
        "Mon canard",
        "Mon chou",
        "Bärchen"
    ],
    "art": "Human, probably",
    "sprite": "/kampfbild/Duc/idle.webp",
    "seiten": [
        "Favourite food: mine, sadly.",
        "Bites: only people he likes.",
        "Release: no. ...Ask him first."
    ]
}
