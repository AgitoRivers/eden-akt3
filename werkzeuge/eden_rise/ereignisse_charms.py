# -*- coding: utf-8 -*-
"""Charm-Uebergaben (Duc 28.10.2026): erreicht eine Figur zum ersten Mal Vertrauen 5, schickt sie ein Foto ihres
Anhaengers und zwei Chat-Blasen (STIL.md: echter Handy-Chat mit Emojis). Beide Antworten geben den Charm
(Folge {"charm": id}); "Hangs it on the jacket" haengt ihn sofort an die getragene Jacke ({"charm_an": id}).
Fredericos Loewe kommt erst mit der vollen Farm (Flag farm_voll aus kern/farm.py). Die Engine zieht diese Events
vor allen anderen Handy-Events (kern/ereignisse.py), das Foto kommt aus items\\<bild>.webp (charms_eden_rise.py)."""
from ereignisse_basis import *  # noqa: F401,F403

ALLE_PHASEN = ["fruehstueck", "tag", "nachmittag", "dinner", "abend", "nacht"]
AN = "Hangs it on the jacket straight away."

# pid: (titel, anrufer_ort, lage, [(blase, gefuehl), ...], (zeile_an, gefuehl), (option_2, zeile_2, gefuehl), tags)
# tags = Turbo-Tags der vier gesprochenen Zeilen (Blase 1, Blase 2, Antwort an, Antwort 2)
UEBERGABE = {
    "chiara": ("Sea Miles", "bridge",
               "A photo from Chiara: a little grey-blue plush dolphin with a navy ribbon, sitting on your folded jacket.",
               [("found it in my locker. had it since my first season. it's been to every port i ever worked 🐬", "caring"),
                ("it's yours now. don't make it a big thing. it's a dolphin, not a ring", "embarrassment")],
               ("you hung it up already?? …okay. it looks good there. shut up 😤", "embarrassment"),
               ("“I'll take good care of it, Chief.”", "you'd better. it has more sea miles than you ⚓", "amusement"),
               ("sigh", "clear throat", "gasp", "chuckle")),
    "lola": ("Kanga", "galley",
             "A photo from Lola: a sandy plush kangaroo with a joey in its pouch and a tiny shell necklace, propped "
             "against your coffee mug in the galley.",
             [("boss!! meet kanga 🦘🦘 she came all the way from byron bay in my backpack", "joy"),
              ("mum gave her to me when i left. said she'd keep me tough. now she keeps YOU tough, deal? 🥹💛", "love")],
             ("AHHH she looks so proud up there!! punch something for me 🥊😂", "joy"),
             ("“Are you sure? She's your mum's.”", "that's why, mate. i only give her to people i'm keeping 🫶", "love"),
             ("laugh", "sniff", "laugh", "sigh")),
    "megan": ("Every Predator", "megan_office",
              "The supply boat brings a small black box with the Eden logo. Inside, on black tissue paper, a sleek black "
              "plush puma with a gold anchor pin. Your phone buzzes.",
              [("It arrived, then. Good.", "neutral"),
               ("Don't read into it, First Officer. Every predator needs a mascot. 🖤", "amusement")],
              ("On the jacket. Where everyone can see it. …How bold. Keep it there.", "desire"),
              ("“Thank you, Megan.”", "No conditions this time. Don't get used to it.", "caring"),
              ("clear throat", "chuckle", "chuckle", "sigh")),
    "lea": ("Anemone", "tender_garage",
            "A photo from Lea: an orange and white plush clownfish on the edge of the dive tank, grinning at the camera.",
            [("fact: clownfish stay with their anemone their whole life. it's the safest place they know 🐠", "caring"),
             ("this one's for you. not because of the fact. ok a bit because of the fact 🙈", "embarrassment")],
            ("it's ON you?? okay. okay okay. i'm going to go stare at the sea now 🫣✨", "nervousness"),
            ("“So I'm the anemone?”", "you weren't supposed to work that out so fast 😳🐠", "embarrassment"),
            ("clear throat", "chuckle", "gasp", "laugh")),
    "rosi": ("Mini Unit-01", "power_room",
             "A photo from Rosi: a small white plush robot shaped like a tiny generator, one amber eye, a felt heart "
             "puffing from its exhaust. It sits on top of the real Unit-01.",
             [("made her myself. night shifts are long 🔧", "neutral"),
              ("she's mini unit-01. she doesn't explode. probably. take her, officer, before i change my mind 😤", "embarrassment")],
             ("you put her on?? on the GOOD jacket? …idiot. she suits you 🤍", "love"),
             ("“You sewed this? At night?”", "don't tell anyone i can sew. i have a reputation 😤🧵", "embarrassment"),
             ("sigh", "chuckle", "gasp", "chuckle")),
    "toto": ("Adopted", "crew_corridor",
             "A photo from Totò: a very round plush raccoon with a bandit mask, a gold chain and flip-flops, sitting on "
             "top of his locked locker.",
             [("Comandante! I have for you a very special item. No questions where it comes from 🦝", "joy"),
              ("Okay, one question. It comes from my heart. Also a little bit from a container in Livorno 😂", "amusement")],
             ("Madonna, look at that! Now you are a real smuggler, Comandante. Very handsome 🤌", "joy"),
             ("“Totò. Is this stolen?”", "Stolen is a big word. Let's say it was… adopted 😇", "amusement"),
             ("chuckle", "laugh", "laugh", "chuckle")),
    "holm": ("Every Watch", "bridge",
             "A photo from Captain Holm, the first she has ever sent you: a white plush polar bear in a captain's cap, "
             "standing square on the chart table.",
             [("Tromsø. Thirty years ago. It has stood every watch with me.", "neutral"),
              ("Take it, Frankfurt. A bridge needs someone who doesn't sleep.", "caring")],
             ("Good. Now it stands your watch. Takk.", "approval"),
             ("“Captain, I can't take this.”", "You can. I'm giving it. That's how it works.", "caring"),
             ("clear throat", "sigh", "chuckle", "sigh")),
    "yamamoto": ("Slow but Sees", "main_salon",
                 "A photo from Yamamoto-san: a green plush sea turtle with tiny round sunglasses, placed very precisely "
                 "in the centre of a silk handkerchief.",
                 [("Officer-san. Please accept this small turtle. So sorry, it is not very much.", "neutral"),
                  ("The turtle is slow. But it sees everything. Very interesting animal. 🐢", "amusement")],
                 ("Very honoured. It looks good on you. Better than on me. So sorry.", "gratitude"),
                 ("“Arigatō, Yamamoto-san.”", "Ah. Your Japanese is very… brave. Thank you. 🙇", "amusement"),
                 ("clear throat", "chuckle", "chuckle", "laugh")),
    "petru": ("Eight Arms", "petru_workshop",
              "A photo from Petru, slightly blurred: a coral red plush octopus in a knitted fisherman's cap, sitting on "
              "the bow of the blue boat.",
              [("Hm. My daughter's. She is grown now.", "neutral"),
               ("Eight arms. It catches what comes. Like you, at the harbour.", "approval")],
              ("Good. Now it goes to sea again.", "approval"),
              ("“Thank you, Petru. Really.”", "Hm. …You are welcome.", "caring"),
              ("clear throat", "sigh", "chuckle", "sigh")),
    "nonna": ("The Hen", "village_piazza",
              "A photo from Nonna Fiora: a plump plush hen in a checked apron, perched on a basket of eggs. Frederico "
              "must have held the phone.",
              [("Isabelle showed me how to send pictures. This is the hen. She is for you 🐔", "joy"),
               ("She watches my kitchen. Now she watches you. Eat something, you look thin.", "caring")],
              ("Good boy. And eat! Or I'll cook you!", "amusement"),
              ("“Grazie, Nonna.”", "Don't grazie me. Come for dinner on Sunday. That's thank you.", "caring"),
              ("chuckle", "sigh", "laugh", "chuckle")),
    "isabelle": ("Lavender Thread", "village_piazza",
                 "A photo from Isabelle: a happy white plush sheep with lavender stitched on its chest, sitting between "
                 "two jars in the pharmacy. One jar is smoking a little.",
                 [("i made you something!! the lavender is real thread, i stitched it myself 🐑💜", "joy"),
                  ("lavender is for healing. also it covers the smell when something explodes. sorry. long story", "embarrassment")],
                 ("you put it on!! okay, now nothing bad can happen to you. medically speaking 🥹", "joy"),
                 ("“Is the jar behind it on fire?”", "NO. a little. it's fine!! it's a healing jar 🔥😅", "nervousness"),
                 ("laugh", "cough", "gasp", "cough")),
    "alva": ("Nobody's Mine", "alvas_bar",
             "A photo from Alva: a little black plush bull calf with a red carnation behind one horn, standing on the "
             "bar next to Papa's chalkboard.",
             [("my grandmother's carnation, from sevilla. the bull is new. i'm not 🥀", "sadness"),
              ("everybody's welcome. nobody's mine. …you can have the bull though 🍷", "desire")],
             ("he looks good on you. better than any bull ever looked on me 😏", "amusement"),
             ("“And the carnation?”", "the carnation stays with him. don't push your luck, o figliolu 😘", "amusement"),
             ("sigh", "chuckle", "chuckle", "laugh")),
    "yasin": ("Limited Edition", "vip_cabin",
              "A photo from Yasin: a round, fluffy plush falcon with a tiny gold chain, posed in front of a ring light "
              "like a product shot.",
              [("bro. BRO. limited edition. only one exists. it's literally content 🦅🔥", "excitement"),
               ("the falcon is a winner. i only work with winners. so. yeah. it's yours. don't make it weird", "embarrassment")],
              ("on the jacket?? that's a collab, my man. we're basically brand partners now 🤝", "joy"),
              ("“Yasin, are you being nice?”", "nice is bad for the brand. delete that. …ok don't delete it", "embarrassment"),
              ("laugh", "clear throat", "laugh", "sigh")),
    "frederico": ("No Collar", "village_piazza",
                  "A photo from Frederico, a little crooked: a black plush lion cub with golden eyes, sitting on the "
                  "gate of the finished farm. Nonna's thumb is in the corner.",
                  [("all the sheds are finished!!! so you get the lion 🦁", "excitement"),
                   ("he's black like the real one. but this one doesn't have a collar. nobody gets a collar anymore", "caring")],
                  ("he's on your jacket!! now you're strong like a lion. and brave. both! 🦁💪", "joy"),
                  ("“He's perfect, Frederico.”", "nonna says i'm not allowed to cry on the phone. i'm not crying. it's the onions", "gratitude"),
                  ("laugh", "sigh", "laugh", "sniff")),
    "jana": ("Not Strudel", "crew_corridor",
             "A photo from Jana: a white plush cat with blue eyes and a red and white scarf, hiding in a small wooden "
             "crate. It looks a lot like a certain cat that does not exist.",
             [("sir. this is not strudel. strudel does not exist. this is a different cat 🐱", "nervousness"),
              ("she's for courage. i don't need her, i'm very brave. sorry. i need her a bit. but you more 🙈", "embarrassment")],
             ("na geh, she looks so good on you!! now you're brave and i'm brave. jessas 🥹", "joy"),
             ("“Tell Strudel I said thanks.”", "there is no strudel, sir!! …she says you're welcome 😺", "amusement"),
             ("gasp", "sigh", "laugh", "chuckle")),
    "siri": ("Never on Camera", "vip_cabin",
             "A photo from Siri, no filter, no ring light: a white plush baby seal in a little knitted Nordic hat, lying "
             "on her pillow.",
             [("this is selma. she's been to every shoot since i was nineteen. she's never been on camera 🦭", "caring"),
              ("i want her somewhere real. with someone real. is that silly? it's silly. take her 🤍", "embarrassment")],
             ("she's on your jacket. like, in the world. okay i'm a bit emotional 🥹", "love"),
             ("“Not silly at all.”", "thank you. you always say the thing that makes it quieter in my head 🤍", "gratitude"),
             ("sigh", "chuckle", "sniff", "sigh")),
    "sophia": ("Sees Everything", "main_salon",
               "A photo from Sophia: a brown plush owl with tiny round glasses holding an even tinier book, set on the "
               "poker table between two neat stacks of chips.",
               [("An owl. Because it sees everything and says nothing, darling.", "amusement"),
                ("Lea says it's not a proper gift without a card. So: you're welcome. That's the card. 🦉", "amusement")],
               ("On display already. How very loyal of you. I'll pretend that isn't charming.", "desire"),
               ("“Did you win it at poker?”", "I never win, darling. I collect. Yamamoto-san paid in owls.", "amusement"),
               ("chuckle", "sigh", "chuckle", "laugh")),
    "elsa": ("Backup", "village_harbour",
             "A message from Lieutenant Ferrandi, with a photo: a plush German shepherd in a tiny navy police cap, "
             "sitting on a stack of paperwork.",
             [("Item: one plush dog. Origin: the gendarmerie raffle. Condition: excellent.", "neutral"),
              ("He has stared down three smugglers this year. Do not tell Totò he is soft.", "amusement")],
             ("Good. He's on duty now. Call me if there's trouble.", "approval"),
             ("“You're giving me evidence, Lieutenant?”", "I'm giving you backup, First Officer. Evidence I keep.", "amusement"),
             ("clear throat", "chuckle", "chuckle", "chuckle")),
    "maxwell": ("The Champion", "sun_deck",
                "A photo from Mr. Maximum: a muscular plush gorilla with dark sunglasses and a gold champion belt, "
                "flexing on top of a kettlebell.",
                [("Number One! Mr. Maximum presents: the CHAMPION 🦍💪", "excitement"),
                 ("He won the belt in Durban. Mr. Maximum won it for him. Now he trains you. Eish, brother, no excuses 😂", "amusement")],
                ("LEKKER! Look at him on you, brother! Mr. Maximum is crying. Manly tears only 💪🥹", "joy"),
                ("“Does he skip breakfast?”", "Never. He's a professional. Unlike someone, Number One 👀", "amusement"),
                ("laugh", "chuckle", "laugh", "chuckle")),
    "casanova": ("A Statement", "village_piazza",
                 "A photo from Madame Casanova: a pink plush flamingo in a ruffled red flamenco dress, posed on the town "
                 "hall balcony as if about to give a speech.",
                 [("Monsieur! A gift from the mayor herself. Applause is permitted 💃", "pride"),
                  ("She dances, she poses, she never loses her composure. Unlike our harbour. Wear her with pride!", "pride")],
                 ("Magnifique! You see? You have presence now. Almost as much as she does.", "joy"),
                 ("“Madame, she is… very pink.”", "Pink is a statement, Monsieur. And you will make it with me. 🦩", "amusement"),
                 ("clear throat", "sigh", "laugh", "chuckle")),
}


def bedingung(pid):
    """Vertrauen 5 (Frederico: volle Farm) und den Charm noch nicht bekommen."""
    b = {"flag": "farm_voll"} if pid == "frederico" else {"wert": ["vertrauen." + pid, ">=", 5]}
    return {"alle": [b, {"nicht": {"flag": "charm_" + pid}}]}


# Zwei Fenster, weil kein Event ueber die Aktgrenze nach Tag 7 reichen darf; das Flag charm_<pid> sperrt das zweite.
FENSTER = {"": (2, 6), "_2": (8, 21)}             # Tag 7 = Anhoerung, keine Zufalls-Events
EVENTS = []
for pid, (titel, ort, lage, blasen, an, zweite, _) in UEBERGABE.items():
    for nach, tage in FENSTER.items():
        EVENTS.append(E("ch_" + pid + nach, "handy", "wholesome", titel, WANN(tage, ALLE_PHASEN, bed=bedingung(pid)), ORT_DUC,
                        {"anrufer": pid, "anrufer_ort": ort, "art": "nachricht", "charm": pid},
                        lage, [Z(pid, t, g) for t, g in blasen],
                        [O(AN, [{"charm": pid}, {"charm_an": pid}, F("charm_" + pid)], zeile=Z(pid, an[0], an[1])),
                         O(zweite[0], [{"charm": pid}, F("charm_" + pid)], zeile=Z(pid, zweite[1], zweite[2]))]))


def stimme_tags():
    """Gesprochene Fassung (Turbo-Tag vorn) fuer jede Zeile: [(wer, text, gesprochen)]."""
    out = []
    for pid, (_, _, _, blasen, an, zweite, tags) in UEBERGABE.items():
        for text, tag in zip([b[0] for b in blasen] + [an[0], zweite[1]], tags):
            out.append((pid, text, "[%s] %s" % (tag, text)))
    return out
