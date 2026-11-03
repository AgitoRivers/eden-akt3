# -*- coding: utf-8 -*-
"""Selfie-Events (Duc 27.10.2026, ersetzt die sechs Einzel-Events vom 26.10.).

Jede Frau schickt bis zu drei Selfies: je eins, wenn ihr Begehren zum ersten Mal 3, 4 und 5 erreicht (knapp, oben ohne,
nackt). Elsa, Isabelle, Jana und Megan haben kein Begehren: bei ihnen zaehlt Vertrauen 3/4/5 plus ein Riegel-Flag.
Pro Frau gibt es zwei bis drei Reihen (Hintergruende); die Engine (kern/ereignisse.py) wuerfelt beim ersten Selfie eine
Reihe aus und bleibt dabei, solange die Reihe die Stufe hat. Texte, Bilder und Nachschlaege: selfie_daten.json
(Abnahme docs/abnahme/selfies_r10 + selfie_texte r10).

Handy-Chat (STIL.md): mehrere Blasen mit Emojis; die Stimme liest Emojis nie (kern/stimme.ohne_emoji).
Antworten: Necken / Kompliment mit Probe (Andenken = genau dieses Foto, Echo = ihre Antwort) / Gentleman / "Leave it on
read". Wer nicht antwortet, bekommt in der naechsten Phase den Nachschlag: Reue (die meisten), offensiv (Chiara, Megan)
oder gekraenkt (Sophia, Rosi)."""
import json, os

from ereignisse_basis import *  # noqa: F401,F403

SPAET = ["abend", "nacht"]
TAGE = (2, 6)
DATEN = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "selfie_daten.json"), encoding="utf-8"))
GRAD = {"knapp": 3, "oben_ohne": 4, "nackt": 5}           # Stufe der Beziehung je Nacktheitsgrad
DATEI = {3: 1, 4: 2, 5: 3}                                  # Dateiendung im Spiel: <frau>_<reihe>_<1-3>.webp
NAME = {"chiara": "Chiara", "sophia": "Sophia", "lea": "Lea", "rosi": "Rosi", "siri": "Siri", "alva": "Alva",
        "lola": "Lola", "elsa": "Elsa", "isabelle": "Isabelle", "jana": "Jana", "megan": "Megan", "bibi": "Bibi"}
ORT = {"chiara": "bridge", "sophia": "crew_corridor", "lea": "tender_garage", "rosi": "power_room", "siri": "vip_cabin",
       "alva": "alvas_bar", "lola": "galley", "elsa": "village_harbour", "isabelle": "village_piazza",
       "jana": "crew_corridor", "megan": "megan_office", "bibi": "mochis"}
# Ohne Begehren: Vertrauen, dazu ein Riegel nur, wo die Geschichte ihn verlangt (Jana: ihre Nacht; Isabelle: ihre Nummer).
# Megan und Elsa nur ueber Vertrauen (Duc 30.10.2026): kein Selfie haengt an einer Entscheidung aus Akt 1
RIEGEL = {"megan": None, "jana": "jana_abend", "elsa": None, "isabelle": "isabelle_handy"}
NACH_ART = {"chiara": "offensiv", "megan": "offensiv", "sophia": "gekraenkt", "rosi": "gekraenkt"}

# frau -> stufe -> (titel, probe, necken (option, zeile, gefuehl), kompliment (option, zeile), gentleman, nachschlag-antwort)
ANTWORT = {
    # Bibi (Duc 02.11.2026): Texte stehen, Bilder fehlen noch. Ohne Eintrag in selfie_daten.bilder entsteht kein Selfie-Event.
    "bibi": {
        3: ("No Animals", "charm",
            ("“The goat saw everything, didn't it?”", "the goat sees EVERYTHING. she's not talking though 😂", "amusement"),
            ("Tells her it's his new favourite page in the field book.", "...ok that's the nicest thing anyone's said to me. keep it. don't show danzel"),
            "“Go to sleep, Bibi. Feeding's at six.”", "ha. ok. good. i was sure you'd hate it"),
        4: ("Washed for You", "charm",
            ("“Ten minutes. I'm counting.”", "nine now. you'd better be looking 😏", "desire"),
            ("Tells her no field book could hold that.", "stop. you're making me laugh at 1am and the hyena is judging me. keep it 🖤"),
            "“Delete it before you regret it. Goodnight.”", "ok. that's fair. i'm going to go and hide in the hay now 🙈"),
        5: ("The Door's Shut", "charm",
            ("“Leaving now. Don't let anything climb in.”", "i'm locking the hyena out. RUN 🏃", "desire"),
            ("Tells her he'd walk up that hill in the dark for her.", "you don't have to walk. you just have to come. keep this one, it's only for you"),
            "“Not tonight. Sleep, Bibi.”", "...ok. good. i'm glad you said that and not nothing"),
    },
    "alva": {
        3: ("Last Round", "charm",
            ("“Put it on my tab.”", "ha. you cant afford it. come over and argue about the price 😏", "amusement"),
            ("Tells her the bar has never looked better.", "careful. say things like that and i start believing them. keep it 🍷"),
            "“Drink some water, Alva. Goodnight.”", "oh thank god. i thought i scared you off 😅"),
        4: ("On the House", "charm",
            ("“Is the house still pouring?”", "the house is closed. the house is also thinking about you. dont tell the house 🙈", "desire"),
            ("Tells her he'd cross the whole village for that view.", "the whole village is asleep. no excuses then 💋"),
            "“Lock up and get some sleep.”", "ok. good. im not embarrassed then. only a bit"),
        5: ("Nobody's Mine", "charm",
            ("“Save me the last shot.”", "im saving you more than the shot. hurry 🥃", "desire"),
            ("Tells her she can be his, just once, without it counting.", "…ok. that one counts. keep it. keep me a bit too 🌙"),
            "“Sober up first. I'll still be here tomorrow.”", "...good. i didnt want to regret it alone"),
    },
    "chiara": {
        3: ("Out of Ten", "courage",
            ("Rates it a seven and waits.", "A SEVEN?? I'm coming down there. …fine. Eight. Final offer 😤", "anger"),
            ("Tells her it's the first eleven on her own scale.", "Eleven isn't on the scale. …Okay. Keep it. Don't you dare show anyone 🔥"),
            "“Ten. Now go to sleep, Chief.”", "Finally. Seven minutes. Noted. 😤"),
        4: ("No Number", "courage",
            ("Sends back a single number: nine and a half.", "Point FIVE? You're doing this on purpose. I know you are 😏", "amusement"),
            ("Tells her she wins, no scale needed.", "Winning feels better than I thought. Keep it. And come up."),
            "“Goodnight, Chiara. You don't need a number.”", "Better. Still a three for timing."),
        5: ("Off the Scale", "courage",
            ("“Permission to come aboard, Captain?”", "Granted. Before I change my mind ⚓", "desire"),
            ("Tells her he likes her quiet, too.", "…Nobody ever says that. Keep it. Keep the quiet one too."),
            "“Not tonight. Get some sleep, Chiara.”", "Good. Bridge. Now."),
    },
    "elsa": {
        3: ("Status Report", "perception",
            ("“Is that an official request?”", "Everything I send is official. That's the problem 🙃", "amusement"),
            ("Tells her the uniform suits her even better off duty.", "Noted. Filed. Not deleted. You may keep the evidence."),
            "“Deleted. Goodnight, Lieutenant.”", "Acknowledged. Relief noted."),
        4: ("For the File", "perception",
            ("“I'd like to read chapter twelve.”", "Chapter twelve is classified. You'll have to earn your clearance.", "amusement"),
            ("Tells her she beats any captain in her novels.", "…That's not a fact. It's an opinion. I'll allow it. Keep it."),
            "“Go home, Elsa. Read your book.”", "Totò remains uninformed. Good."),
        5: ("Case Closed", "perception",
            ("“Witness reporting for duty.”", "Good. Bring figs. Leave Totò at home.", "joy"),
            ("Tells her she has never needed a rule less.", "I'll write that down. In my private file. Keep this. Don't lose it."),
            "“Sleep, Elsa. The coast can guard itself for one night.”", "Then we both had the same dream. Noted."),
    },
    "isabelle": {
        3: ("Lavender", "empathy",
            ("“Your secret's safe. Nonna's too.”", "thank you. I think. oh no, I'm smiling 😳", "embarrassment"),
            ("Tells her she doesn't need to be sorry for anything.", "nobody has ever said that to me. I'll keep that. you keep this 🌿"),
            "“Go to sleep, Isabelle. It's alright.”", "oh. okay. thank you. I can breathe again 🙏"),
        4: ("Patience", "empathy",
            ("“Patience is overrated.”", "don't say things like that, I'll have to confess them too 🙈", "desire"),
            ("Tells her she's braver than she thinks.", "I don't feel brave. I feel like jelly. but thank you. keep it"),
            "“Put the phone down and sleep.”", "you're too kind. now I have to pray for you too"),
        5: ("Confession", "empathy",
            ("“Confess it to me instead.”", "I just did. that was the confession. oh dear Lord 🫣", "desire"),
            ("Tells her there's nothing in it to forgive.", "…then I won't ask for forgiveness. only for you. keep it 🕯️"),
            "“Goodnight, Isabelle. You'll be alright.”", "then I'll keep it a little secret. ours"),
    },
    "jana": {
        3: ("Wrong Photo", "empathy",
            ("“Tell Strudel he has talent.”", "he says thank you!! he's very proud. I'm also proud. sorry 🐱", "joy"),
            ("Tells her it's the best thing he's seen all day.", "really?? Jessas. okay. I'm keeping this message forever. you keep the photo 🥺"),
            "“Goodnight, Jana. Nothing to be sorry for.”", "phew!! sorry. thank you, Sir"),
        4: ("Brave", "empathy",
            ("“Chiara would be proud.”", "NO she wouldn't. okay maybe a bit. don't tell her 😳", "embarrassment"),
            ("Tells her she's braver than anyone on the boat.", "me?? brave?? …okay. I'll try to believe it. keep it, Sir"),
            "“Breakfast will be fine. Promise. Goodnight.”", "okay. I'll look at you at breakfast. maybe. a bit"),
        5: ("Slip Knot", "empathy",
            ("“Jessas is right.”", "hahaha you said Jessas. okay I feel better. a bit 😳", "amusement"),
            ("Tells her it wasn't a mistake. Not even a little.", "okay. okay. now I'm saying sorry to my pillow because I'm so happy. keep it 🥺"),
            "“Sleep, Jana. We'll talk tomorrow.”", "not a mistake. okay. okay okay okay 🥺"),
    },
    "lea": {
        3: ("For Science", "empathy",
            ("“Very scientific.”", "it IS scientific. I'm a scientist. a wet one 🤓", "amusement"),
            ("Tells her she's the best thing in the photo.", "better than the whole ocean?? …okay. keep it. I'm going to scream into my pillow now 🙈"),
            "“Go and dry off, Lea. Sleep well.”", "phew. okay. I can breathe again 🐢"),
        4: ("Nervous Colours", "empathy",
            ("“What colour are you now?”", "RED. all of me. you did that 🐙", "embarrassment"),
            ("Tells her she makes him nervous too.", "really? like octopus nervous? okay. good. keep it 💙"),
            "“You didn't make it awkward. Goodnight.”", "okay, you're not mad. good. great. I'm fine. totally fine"),
        5: ("No Fact for This", "empathy",
            ("“Here's a fact: I'm smiling.”", "that's my favourite fact now. better than the three hearts 💙", "joy"),
            ("Tells her she didn't need a fact for this.", "…okay. then no facts. just you and me. keep it, Duc"),
            "“Get some sleep, Lea. Tomorrow.”", "you didn't. okay. okay. I'm breathing again 💙"),
    },
    "lola": {
        3: ("Rate the Chef", "charm",
            ("Rates the food, only the food.", "ten out of ten for the food. wow. cool. love that for the food 🙄", "annoyance"),
            ("Tells her the food has serious competition.", "okay okay okay. keep it. don't show Rosi, Rosi tells everyone 😂"),
            "“Get some sleep, Lola.”", "hahaha okay good. framing it then"),
        4: ("Not the Bao", "charm",
            ("“I'm not asking about the flour.”", "good. the flour has a story and it's not a good one 😂", "amusement"),
            ("Tells her she's never too much.", "…oh. okay. that's. I'm not crying, it's the onions. keep it 🥺"),
            "“Goodnight, Lola. You're still hired tomorrow.”", "you're too nice to me, Boss"),
        5: ("Too Much", "charm",
            ("“Best idea. Easily.”", "YES. I knew it. I mean I didn't know it. but YES 🙌", "excitement"),
            ("Tells her she's the best thing in every room on this boat.", "Boss. stop. …don't stop. keep it 😇"),
            "“You can cook tomorrow. Promise. Sleep.”", "out of the galley then. for you 😇"),
    },
    "megan": {
        3: ("Third Quarter", "cunning",
            ("“My silence is expensive. Name your price.”", "Dinner. Monaco. You're paying, and you'll overtip ♟️", "amusement"),
            ("Tells her he'd never sell it, not even to the board.", "I know. That's precisely why I sent it. Keep it, Duc."),
            "“Deleted. Get some rest, Megan.”", "Wise. Silence was costing you."),
        4: ("Your Move", "cunning",
            ("Moves a pawn. “e4.”", "How predictable. And yet I'm smiling. Don't tell anyone ♟️", "amusement"),
            ("Tells her the queen is safe with him.", "…Nobody has ever said that and meant it. Keep it."),
            "“Goodnight, Megan. I won't make you regret it.”", "That's more like it."),
        5: ("No Conditions", "cunning",
            ("“Checkmate?”", "Not yet. But I'm letting you think so. That should tell you something.", "desire"),
            ("Tells her he won't make her regret it. Ever.", "Then I won't. …Keep it. Keep me, if you're brave enough."),
            "“Sleep, Megan. Your secret is safe.”", "Good. I was beginning to wonder if you had the nerve."),
    },
    "rosi": {
        3: ("Proof Attached", "cunning",
            ("Zooms in on the background.", "WOW. okay. great. the background says thanks 😒", "annoyance"),
            ("Tells her it's a draw: both look great.", "a draw. fine. I'll take a draw. keep it, Officer 😏"),
            "“Good work today. Goodnight, Rosi.”", "…fine. apology accepted. barely"),
        4: ("Draw", "cunning",
            ("“I didn't blink.”", "you blinked. twice. I counted 😤", "amusement"),
            ("Tells her the mark on the board is for both of them.", "…okay. don't make me soft, Officer. keep it"),
            "“Go and cool off. Goodnight.”", "okay. machines don't apologise. you're better than a machine. barely"),
        5: ("Tactical Surrender", "cunning",
            ("“Rematch tomorrow?”", "every day. you'll lose every time 🔧", "amusement"),
            ("Tells her he'd rather lose to her than beat anyone else.", "that's the dumbest thing anyone has ever said to me. keep it. …Captain."),
            "“Get some sleep, Rosi. No more bets.”", "…okay. maybe don't mention it tomorrow anyway. but thanks"),
    },
    "siri": {
        3: ("Not the Camera Voice", "empathy",
            ("“The wink stays.”", "no!! okay fine. the wink stays 🙈", "amusement"),
            ("Tells her it's the realest photo she's ever sent.", "real. nobody says that to me. keep it. it's yours 🤍"),
            "“It's not weird. Goodnight, Siri.”", "okay, phew. sorry for the panic 🙈"),
        4: ("Just for One", "empathy",
            ("“Peace to you too.”", "✌️ I'm never living this down, am I", "amusement"),
            ("Tells her it's more than okay. It's her.", "it's me. huh. keep it, Duc. I like being me with you"),
            "“It's okay. Sleep well, Siri.”", "honest is good. thank you"),
        5: ("No Filter", "empathy",
            ("“I'm honoured. And a bit speechless.”", "speechless is good. speechless I can work with 🤍", "joy"),
            ("Tells her she has never needed a filter.", "…okay, I'm crying a bit. good crying. keep it"),
            "“No screenshots. Promise. Goodnight.”", "okay. I trust you. still shaking, but the good kind"),
    },
    "sophia": {
        3: ("Research Material", "charm",
            ("“What's the heroine wearing in chapter nine?”", "Less than this. I'm writing it now. Don't go anywhere.", "desire"),
            ("Writes her a reply worth putting in a book.", "Oh. That's going in. Word for word. You keep the photo, I keep the line."),
            "“Get some sleep, Sophia.”", "Hm. I'll take my ten euros back, then."),
        4: ("The Forfeit", "charm",
            ("“I'd like to read your notes.”", "Ten euros says you'll blush 📓", "amusement"),
            ("Tells her she has never lost a bet she wanted to win.", "…Darling. That was dangerously accurate. Keep it."),
            "“Goodnight, Sophia. Your reputation is safe.”", "Apology noted. Review revised. Slightly."),
        5: ("No Bet Tonight", "charm",
            ("“Then write the ending with me.”", "I was hoping you'd say that. Pen's ready 🖋️", "desire"),
            ("Tells her he's glad she asked. Finally.", "So am I. Keep it. And keep asking me, would you?"),
            "“Sleep, Sophia. Ask me again tomorrow.”", "…Thank you. I'll try that again. Some day."),
    },
}
# Antworten je Foto (Duc 31.10.2026): ANTWORT gilt fuer alle Reihen einer Stufe und passte oft nur auf eine ("flour" beim
# Leoparden). Hier steht, was fuer eine Reihe anders ist. Die Antwort auf das Kompliment bleibt je Stufe gleich, sie ist
# das Echo des Andenkens: kompl aendert nur den Chip.
# (frau, stufe, reihe) -> {"titel", "necken": (option, zeile, gefuehl), "kompl": option, "gentle": option}
PASSEND = {
    ("alva", 3, "zimmer"): {"titel": "Too Hot to Sleep",
                            "necken": ("“Send the wine over.”", "the wine stays here. you come to it 😏", "amusement"),
                            "kompl": "Tells her the room over the bar has the best view in the village."},
    ("alva", 4, "tresen"): {"titel": "Counter Dance",
                            "necken": ("“Do that again.”", "no. the fan is tired. come over and clap in person 😏", "amusement")},
    ("alva", 4, "zimmer"): {"titel": "Deny Everything",
                            "necken": ("“Deny what?”", "exactly. you're learning 🤫", "amusement"),
                            "gentle": "“Your secret's safe. Get some sleep.”"},
    ("alva", 5, "zimmer"): {"necken": ("“Two in the morning is a good time.”", "its the worst time. hurry anyway 🌙", "desire"),
                            "gentle": "“Go to sleep, Alva. I'll still be here tomorrow.”"},
    ("chiara", 3, "bruecke"): {"titel": "Report to the Bridge",
                               "necken": ("“On whose orders, Chief?”", "Mine. The captain's asleep. Move 😤", "amusement"),
                               "gentle": "“The bridge is yours, Chief. Goodnight.”"},
    ("chiara", 3, "nock"): {"titel": "Finders Keepers",
                            "necken": ("“That's my shirt.”", "WAS your shirt. Come and get it 😤", "amusement"),
                            "gentle": "“Keep the shirt. Goodnight, Chief.”"},
    ("chiara", 4, "bruecke"): {"titel": "Three Minutes",
                               "necken": ("“What happens at zero?”", "At zero you get a second order. It's worse 😏", "amusement"),
                               "gentle": "“Not tonight, Chiara. Goodnight.”"},
    ("chiara", 4, "nock"): {"titel": "The Arrangement",
                            "necken": ("“Keep the shirt.”", "I was going to. You don't get a vote 😏", "amusement"),
                            "gentle": "“Goodnight, Chiara. The shirt is yours.”"},
    ("chiara", 5, "kabine"): {"necken": ("“That was a please. I heard it.”", "You heard nothing. Bridge. Now ⚓", "desire")},
    ("chiara", 5, "nock"): {"titel": "Come and Fetch It",
                            "necken": ("“I'm only coming for the shirt.”", "Liar. Hurry ⚓", "desire")},
    ("elsa", 3, "verhoerzelle"): {"titel": "Equipment Test",
                                  "necken": ("“What equipment?”", "Classified. You would have to come and inspect it 🙃", "amusement"),
                                  "kompl": "Tells her the equipment has never looked better."},
    ("elsa", 4, "verhoerzelle"): {"titel": "The Suspect",
                                  "necken": ("“I want a lawyer.”", "Denied. Suspects don't get lawyers in chapter fourteen 🙃", "amusement")},
    ("elsa", 5, "verhoerzelle"): {"titel": "Out of Reach",
                                  "necken": ("“Help is on the way.”", "Good. Bring the key. Or don't. Leave Totò at home 🔑", "desire"),
                                  "gentle": "“Stretch for the key, Elsa. Goodnight.”"},
    ("isabelle", 3, "lavendelbad"): {"necken": ("“Nonna doesn't need to know.”", "thank you. I think. oh no, I'm smiling 😳", "embarrassment"),
                                     "kompl": "Tells her she can look at her phone as long as she wants."},
    ("isabelle", 4, "lavendelbad"): {"titel": "The Robe's Fault",
                                     "necken": ("“Blame the robe.”", "I do. very much. now I have to confess that too 🙈", "desire")},
    ("jana", 3, "dusche"): {"titel": "The Light in the Shower",
                            "necken": ("“Good light, Jana.”", "right?? it's very good light!! thank you!! sorry 😳", "joy")},
    ("jana", 3, "shibari"): {"titel": "A New Knot",
                             "necken": ("“Is it hard to tie?”", "no!! okay yes. I can show you. not like that. sorry 🪢", "joy"),
                             "gentle": "“It's not weird. Goodnight, Jana.”"},
    ("jana", 4, "shibari"): {"titel": "Look at the Knots",
                             "necken": ("“Very even knots.”", "THANK you!! you looked at the knots!! only the knots?? 😳", "embarrassment"),
                             "gentle": "“Neat work. Goodnight, Jana.”"},
    ("jana", 5, "dusche"): {"titel": "Counted to Three"},
    ("jana", 5, "shibari"): {"necken": ("“A slip knot. Good to know.”", "hahaha okay. I feel better. a bit 😳", "amusement"),
                             "kompl": "Tells her she is good at a lot more than knots."},
    ("lea", 3, "beach"): {"titel": "The Turtles Hatched",
                          "necken": ("“Wish the turtles good luck.”", "I did. they didn't listen. they're turtles 🐢", "amusement"),
                          "gentle": "“Go to bed, Lea. The turtles will manage.”"},
    ("lea", 3, "plankton"): {"titel": "The Bay Is Glowing",
                             "necken": ("“A nightlight suits you.”", "it's called bioluminescence. but thank you 🤓", "amusement")},
    ("lea", 4, "plankton"): {"titel": "Come Swim",
                             "necken": ("“Scared of what, exactly?”", "you. a bit. the good kind 🙈", "embarrassment"),
                             "gentle": "“Not tonight, Lea. Goodnight.”"},
    ("lea", 5, "beach"): {"titel": "Four Hundred Turtles",
                          "necken": ("“Here's a fact: I saw it.”", "you were supposed to. that's my favourite fact now 🐢", "joy"),
                          "kompl": "Tells her the turtles don't know what they missed."},
    ("lea", 5, "plankton"): {"titel": "Just the Glow",
                             "necken": ("“Mad suits you.”", "tell Opa that. no. don't tell Opa 🐙", "joy"),
                             "kompl": "Tells her she doesn't need the glow."},
    ("lola", 3, "koje"): {"titel": "Rate the Leopard",
                          "necken": ("Rates the leopard, only the leopard.", "ten out of ten for the leopard. wow. cool. love that for the leopard 🙄", "annoyance"),
                          "kompl": "Tells her the leopard has serious competition."},
    ("lola", 3, "sahne"): {"titel": "Dessert Test",
                           "necken": ("Rates the pavlova, only the pavlova.", "ten out of ten for the pavlova. wow. cool. love that for the pavlova 🙄", "annoyance"),
                           "kompl": "Tells her the pavlova has serious competition."},
    ("lola", 4, "koje"): {"titel": "Leopard Update",
                          "necken": ("“My money's on you, not the leopard.”", "smart. the leopard never had a chance 😂", "amusement")},
    ("lola", 4, "sahne"): {"titel": "Change of Plan",
                           "necken": ("“Does the dessert come with a spoon?”", "the dessert comes with a warning. not deleting it though 😂", "amusement")},
    ("lola", 5, "koje"): {"titel": "The Leopard's Gone",
                          "necken": ("“Sleep tight? No chance.”", "HA. knew it. I mean I didn't know it. but YES 🙌", "excitement"),
                          "gentle": "“Sleep tight, Lola.”"},
    ("lola", 5, "sahne"): {"titel": "Cleaning Up",
                           "necken": ("“I'll bring a sponge.”", "no sponge. think harder, Boss 😇", "amusement"),
                           "gentle": "“Clean it up in the morning, Lola. Sleep.”"},
    ("megan", 3, "hubschrauber"): {"titel": "Twelve Minutes",
                                   "necken": ("“Is the pilot still looking forward?”", "He likes his job. You should like yours ♟️", "amusement"),
                                   "kompl": "Tells her that trust is safe with him."},
    ("megan", 4, "hubschrauber"): {"titel": "A Promotion",
                                   "necken": ("“What does the promotion pay?”", "Less than you think. More than you deserve ♟️", "amusement")},
    ("megan", 5, "hubschrauber"): {"titel": "Six Minutes",
                                   "necken": ("“Tell the pilot to keep circling.”", "He has his orders. I have the fuel. Your turn.", "desire"),
                                   "gentle": "“Land the helicopter, Megan. Goodnight.”"},
    ("rosi", 3, "generatorraum"): {"titel": "Spoils of War",
                                   "necken": ("Zooms in on the jacket.", "WOW. okay. great. the jacket says thanks 😒", "annoyance"),
                                   "kompl": "Tells her it's a draw: she and the jacket both look great."},
    ("rosi", 3, "strand"): {"titel": "Day Off",
                            "necken": ("Zooms in on the boat.", "WOW. okay. great. the boat says thanks 😒", "annoyance"),
                            "kompl": "Tells her it's a draw: she and the boat both look great."},
    ("rosi", 3, "werkstatt"): {"titel": "Twelve to Eleven",
                               "necken": ("Zooms in on the tally board.", "WOW. okay. great. the board says thanks 😒", "annoyance"),
                               "kompl": "Tells her the board should say draw, because she looks that good."},
    ("rosi", 4, "generatorraum"): {"titel": "The Jacket Stays",
                                   "necken": ("“The jacket wants to come home.”", "the jacket is happy here. it told me 😤", "amusement"),
                                   "kompl": "Tells her she can keep the jacket. She wears it better."},
    ("rosi", 4, "strand"): {"titel": "Loser Does What",
                            "necken": ("“You're on. What does the loser do?”", "you'll find out. you're losing anyway 😤", "amusement"),
                            "kompl": "Tells her he would lose this bet on purpose."},
    ("rosi", 4, "werkstatt"): {"titel": "A New Mark",
                               "necken": ("“What's the mark for?”", "I said don't ask. you asked. that's a point for me 😤", "amusement")},
    ("rosi", 5, "generatorraum"): {"titel": "Come and Take It",
                                   "necken": ("“I didn't blink.”", "you blinked. twice. I counted 🔧", "amusement"),
                                   "gentle": "“Keep the jacket tonight. Goodnight, Rosi.”"},
    ("rosi", 5, "werkstatt"): {"titel": "Finish What You Start",
                               "necken": ("“Then let's finish it.”", "about time. bring tools. or don't 🔧", "desire"),
                               "gentle": "“It can wait. Get some sleep, Rosi.”"},
    ("siri", 3, "dessous"): {"titel": "Before the Launch",
                             "necken": ("“I won't tell the brand.”", "thank you!! the brand is very scary 🙈", "amusement"),
                             "gentle": "“It's allowed. Goodnight, Siri.”"},
    ("siri", 3, "vordeck"): {"titel": "Second Place",
                             "necken": ("“Say good morning to the winch for me.”", "no!! okay fine. it says good morning back 🙈", "amusement"),
                             "gentle": "“Second is fine. Sleep well, Siri.”"},
    ("siri", 4, "dessous"): {"titel": "Is Pink OK",
                             "necken": ("“Pink works. Don't tell the brand.”", "the brand would kill us both 🙈", "amusement")},
    ("siri", 4, "vordeck"): {"titel": "Didn't Fix Anything",
                             "necken": ("“Leave the hair like that.”", "it's staying. it's a mess. I'm never living this down 🙈", "amusement")},
    ("sophia", 3, "achterdeck"): {"titel": "Ten Euros",
                                  "necken": ("“Make it twenty.”", "Twenty says you're up here before half past. Don't go anywhere 🥂", "desire")},
    ("sophia", 3, "noir"): {"titel": "Chapter One",
                            "necken": ("“What is the detective wearing in chapter two?”", "Less than this. I'm writing it now. Don't go anywhere.", "desire")},
    ("sophia", 4, "achterdeck"): {"necken": ("“What was the bet?”", "Ten euros says you'll blush if I tell you 🥂", "amusement")},
    ("sophia", 4, "koje"): {"titel": "Purely Research",
                            "kompl": "Tells her the hero won't survive this scene.",
                            "gentle": "“Goodnight, Sophia. The hero needs his sleep.”"},
    ("sophia", 4, "noir"): {"titel": "Chapter Two",
                            "necken": ("“Shocked. Taking notes.”", "Ten euros says you'll blush in chapter three 📓", "amusement"),
                            "kompl": "Tells her the reader is in serious trouble.",
                            "gentle": "“Goodnight, Sophia. The reader needs his sleep.”"},
    ("sophia", 5, "achterdeck"): {"titel": "What's Left",
                                  "necken": ("“What's left looks good to me.”", "I was hoping you'd say that. Don't tell anyone 🥂", "desire"),
                                  "kompl": "Tells her he's glad she stopped managing. Finally.",
                                  "gentle": "“Sleep, Sophia. Nobody needs managing tonight.”"},
    ("sophia", 5, "koje"): {"necken": ("“I'm asking now. What else do you want?”", "I was hoping you'd say that. Pen's ready 🖋️", "desire"),
                            "kompl": "Tells her he's glad she told him. Finally."},
    ("sophia", 5, "noir"): {"titel": "Chapter Three"},
}
# Rueckbezug im Foto braucht eine Erinnerung (Duc: der Spieler vergisst): Lage statt der Standardzeile, die Blasen bleiben
LAGE = {
    ("alva", 5, "tresen"): "A photo from Alva, on her counter. The last shot of tequila is still waiting.",
    ("chiara", 4, "kabine"): "A photo from Chiara. She rates everything out of ten, and she still wants your number for her last photo.",
    ("chiara", 5, "kabine"): "A photo from Chiara. She usually rates everything out of ten. Not tonight.",
    ("chiara", 4, "nock"): "A photo from Chiara, still wearing the shirt she took from your laundry.",
    ("chiara", 5, "nock"): "A photo from Chiara. The shirt she took from your laundry is lying next to her.",
    ("elsa", 4, "posten"): "A photo from Elsa. She secretly reads romance novels on duty, and she has reached the good part.",
    ("elsa", 4, "verhoerzelle"): "A photo from Elsa. She secretly reads romance novels on duty, and she has reached the good part.",
    ("lea", 5, "garage"): "A photo from Lea. She usually has an animal fact for everything.",
    ("lola", 4, "koje"): "A photo from Lola, in what is left of her leopard pyjamas.",
    ("lola", 5, "koje"): "A photo from Lola. The leopard pyjamas are on the floor.",
    ("rosi", 3, "werkstatt"): "A photo from Rosi. She keeps score of your duels on a whiteboard in her workshop: Rosi vs. Officer.",
    ("rosi", 4, "werkstatt"): "A photo from Rosi, next to her whiteboard: Rosi vs. Officer.",
    ("rosi", 4, "generatorraum"): "A photo from Rosi in the power room, still wearing the jacket she took from you.",
    ("rosi", 5, "generatorraum"): "A photo from Rosi. She still has your jacket on. Only your jacket.",
    ("rosi", 5, "strand"): "A photo from Rosi, back at the boat. You two had a bet on who could fix it first.",
    ("sophia", 5, "koje"): "A photo from Sophia. She usually turns everything into a ten-euro bet.",
}
GEF = {3: "joy", 4: "desire", 5: "love"}
NACH_GEF = {"reue": "embarrassment", "offensiv": "annoyance", "gekraenkt": "sadness"}


def ohne_begehren(frau):
    return frau in RIEGEL


def nah(frau, n):
    """Folge "naeher": Begehren bei den Romanzen, sonst Vertrauen."""
    return V(frau, n) if ohne_begehren(frau) else B(frau, n)


def bedingung(frau, stufe):
    if ohne_begehren(frau):
        v = {"wert": ["vertrauen." + frau, ">=", stufe]}
        return {"alle": [v, {"flag": RIEGEL[frau]}]} if RIEGEL[frau] else v
    b = {"wert": ["begehren." + frau, ">=", stufe]}
    return {"alle": [b, {"flag": "siri_frei"}]} if frau == "siri" else b


def zeilen(frau, stufe, tag, blasen):
    return [Z(frau, b, GEF[stufe]) for b in blasen]


EVENTS, ECHO = [], {}
for key in sorted(DATEN["bilder"]):
    frau, reihe, grad = key.split("|")
    stufe = GRAD[grad]
    titel, attr, necken, kompl, gentle, _ = ANTWORT[frau][stufe]
    item_titel, item_text = titel, kompl[1]
    anders = PASSEND.get((frau, stufe, reihe), {})
    titel, necken, gentle = anders.get("titel", titel), anders.get("necken", necken), anders.get("gentle", gentle)
    kompl = (anders.get("kompl", kompl[0]), kompl[1])
    tag, blasen = DATEN["haupt"][key]
    iid = "%s_selfie_%d" % (frau, stufe)
    eid = "sf_%s_%d_%s" % (frau, stufe, reihe)
    EVENTS.append(E(eid, "handy", "frech", titel, WANN(TAGE, SPAET, bed=bedingung(frau, stufe)), ORT_DUC,
                    {"anrufer": frau, "anrufer_ort": ORT[frau], "art": "nachricht",
                     "selfie": {"frau": frau, "reihe": reihe, "stufe": stufe, "bild": "%s_%s_%d" % (frau, reihe, DATEI[stufe])}},
                    "Your phone lights up. " + LAGE.get((frau, stufe, reihe), "A photo from %s, and then the messages start." % NAME[frau]),
                    zeilen(frau, stufe, tag, blasen),
                    # Das Foto ist die Belohnung, nicht der Antrieb zur naechsten Stufe (Duc 30.10.2026, vorher +6/+8)
                    [O(necken[0], [nah(frau, 2), V(frau, 2)] if not ohne_begehren(frau) else [V(frau, 2)],
                       zeile=Z(frau, necken[1], necken[2])),
                     O(kompl[0], [], probe=P(attr, 9 + stufe), erfolg=[nah(frau, 3), NK(frau), I(iid)],
                       fehlschlag=[nah(frau, 1)], zeile=Z(frau, kompl[1], "love")),
                     O(gentle, [V(frau, 6)] if not ohne_begehren(frau) else [V(frau, 2)]),
                     O("Leaves it on read.", [F("sfn_%s_%d" % (frau, stufe))])],
                    knistern=True))
    ECHO.setdefault(iid, "%s#o1" % eid)
    item(iid, item_titel, "andenken", text=item_text)
assert all("%s|%s|%s" % (f, r, g) in DATEN["bilder"] for f, s, r in PASSEND for g, n in GRAD.items() if n == s), "PASSEND: Foto fehlt"

# Nachschlag: kommt in der naechsten Phase, wenn Duc das Foto auf "gelesen" liegen liess
for frau, stufen in ANTWORT.items():
    art = NACH_ART.get(frau, "reue")
    for stufe, (titel, *_rest) in stufen.items():
        antwort = _rest[-1]
        tag, blasen = DATEN["nachschlag"][frau][{3: "knapp", 4: "oben_ohne", 5: "nackt"}[stufe]]
        if art == "reue":
            opt = [O("Writes back that it was lovely and she can stop worrying.", [V(frau, 4), nah(frau, 2)],
                     zeile=Z(frau, antwort, "relief")),
                   O("Leaves it.", [V(frau, -2)])]
        elif art == "offensiv":
            opt = [O("Answers the challenge.", [nah(frau, 2)], zeile=Z(frau, antwort, "amusement")),
                   O("Still doesn't answer.", [nah(frau, -4)])]
        else:
            opt = [O("Apologises and means it.", [nah(frau, 2), V(frau, 2)], zeile=Z(frau, antwort, "sadness")),
                   O("Leaves it.", [nah(frau, -4)])]
        EVENTS.append(E("sfn_%s_%d" % (frau, stufe), "handy", "ernst" if art == "gekraenkt" else "witzig",
                        "%s: %s" % (NAME[frau], titel), WANN(TAGE, PHASEN, bed={"flag": "sfn_%s_%d" % (frau, stufe)}),
                        ORT_DUC, {"anrufer": frau, "anrufer_ort": ORT[frau], "art": "nachricht", "nachschlag": True},
                        "%s again. You never answered the photo." % NAME[frau],
                        [Z(frau, b, NACH_GEF[art]) for b in blasen], opt))

# Altlasten vom 26.10. (alte Spielstaende koennen sie im Inventar haben): Gegenstaende bleiben definiert, vergibt nichts mehr
for _f, _t in (("chiara", "Out of Ten"), ("sophia", "Research Material"), ("lea", "Night Dive"), ("siri", "No Filter"),
               ("alva", "After Hours"), ("lola", "Bao on the Left")):
    item("%s_selfie" % _f, _t, "andenken", text="")


def stimme_tags():
    """Gesprochene Fassung (Turbo-Tag) fuer jede neue Zeile: [(wer, text, gesprochen)]."""
    out = []
    for key, (tag, blasen) in DATEN["haupt"].items():
        frau = key.split("|")[0]
        for i, b in enumerate(blasen):
            t = tag if i != 1 else ("sigh" if tag in ("sigh", "gasp") else "chuckle")
            out.append((frau, b, "[%s] %s" % (t, b)))
    for frau, st in DATEN["nachschlag"].items():
        for tag, blasen in st.values():
            for i, b in enumerate(blasen):
                out.append((frau, b, "[%s] %s" % (tag if i == 0 else "sigh", b)))
    gef_tag = {"amusement": "chuckle", "anger": "gasp", "desire": "sigh", "embarrassment": "gasp", "joy": "laugh",
               "annoyance": "sigh", "excitement": "laugh"}
    for frau, stufen in ANTWORT.items():
        for stufe, (titel, attr, necken, kompl, gentle, antwort) in stufen.items():
            out.append((frau, necken[1], "[%s] %s" % (gef_tag.get(necken[2], "chuckle"), necken[1])))
            out.append((frau, kompl[1], "[sigh] %s" % kompl[1]))
            out.append((frau, antwort, "[%s] %s" % ("chuckle" if NACH_ART.get(frau) == "offensiv" else "sigh", antwort)))
    for (frau, _s, _r), anders in PASSEND.items():
        if anders.get("necken"):
            _o, zeile, gef = anders["necken"]
            out.append((frau, zeile, "[%s] %s" % (gef_tag.get(gef, "chuckle"), zeile)))
    return out
