# -*- coding: utf-8 -*-
r"""Die Dorf-Figuren Pascal, Mina, Bà Tư, Sandru und Don Anghjulu (Duc 30.10.2026, E-089, E-093 bis E-099).

Kanon und Ablauf: docs/wiki/welt/dorf_figuren.md. Neue Szenen kommen hierher, damit sich die Sitzungen nicht in die
Quere kommen; Eingriffe in bestehende Events bleiben in deren Dateien, ihre gesprochene Fassung steht unten in ZUSATZ.
Phase 2: Pascal und Mina in Akt 1. Texte von Duc abgenommen (docs/abnahme/dorf_akt1_texte.json).

Zeilen stehen hier MIT Turbo-Tag (gesprochen); das Spiel zeigt sie ohne. tags_schreiben() traegt sie in stimme_tags.json ein.
Pascal und Sandru bleiben ausserhalb der Faelle: keine Codex-Eintraege, keine Beweise, keine Aussagen in der Anhoerung.
"""
import json
import os
import re

from ereignisse_basis import *  # noqa: F401,F403
from ereignisse_hafen import BILD_ABEND, HF
from ereignisse_grotte import FR as FR_G
from ereignisse_kloster import FR

TAG_RE = re.compile(r"\s*\[(chuckle|clear throat|cough|gasp|laugh|shush|sigh|sniff)\]\s*")
WEITER = lambda ziel: {"weiter": ziel}
STIMME = []         # (wer, Text wie im Spiel, gesprochene Fassung)


def klar(t):
    return " ".join(TAG_RE.sub(" ", t).split())


def S(wer, gesprochen, gefuehl="neutral"):
    """Sprechzeile mit Turbo-Tag: das Spiel bekommt den Text ohne Tag, die Stimme mit."""
    STIMME.append((wer, klar(gesprochen), gesprochen))
    return Z(wer, klar(gesprochen), gefuehl)


def P1(handelnd, *betroffen):
    return {"handelnd": handelnd, "betroffen": [{"id": b[0], "ton": b[1], "was": b[2]} for b in betroffen]}


def H(anrufer, ort, art="video"):
    return {"anrufer": anrufer, "anrufer_ort": ort, "art": art}


def PV(links, rechts, *zuschauer):
    return {"links": links, "rechts": rechts, "zuschauer": list(zuschauer)}


KENNT_PASCAL = {"bekannt": "pascal"}
PFLICHT = dict(pflicht=True, holt_leute=True)

item("fish_sauce", "Fish Sauce", "geschenk",
     text="Amber, salty, and a smell that gets into your shirt and stays until Christmas. It comes from a cousin in Marseille, and she "
          "won't say which cousin. Everybody says it stinks. Everybody comes back.")
item("kl_post", "Three Weeks of Post", "andenken",
     text="A bundle of letters in a rubber band, three weeks thick. Mina couldn't get past the bridge. Some of them are "
          "for people you still have to find.")

EVENTS = [
    # ------------------------------------------------------------------ Tag 2: nach dem Abend am Hafen
    HF("hk_pascal", BILD_ABEND, "The Man with the Barrel",
       "The barrel is nearly empty when Madame Casanova climbs on a crate for one more speech, mostly to the boats. At "
       "the end she stops, lifts her chin and waits. She always leaves this pause, for the applause. Nobody in the "
       "harbour claps. Then somebody does: a thin man behind the barrel, in a double-breasted pinstripe suit and a white "
       "fedora, clapping carefully so he doesn't spill his glass. There is barrel dirt on one knee of the suit. A folded list sticks out of his "
       "breast pocket, in beautiful upright handwriting, like a wedding invitation.",
       [S("pascal", "[chuckle] Somebody has to, or she starts again. Pascal Leca, deputy mayor. If a thing in this town "
                    "doesn't need a speech, it's probably me.", "amusement"),
        S("pascal", "And you're Duc. Yes, I asked. You could have stayed on your boat tonight, and nobody here would "
                    "have blamed you. [sigh] You didn't. This village will remember that, Duc, and so will I.", "gratitude"),
        S("pascal", "Now, you're bleeding on my harbour. [chuckle] That's not a complaint. Here, take these, the pharmacy "
                    "doesn't open until Thursday.", "caring"),
        S("pascal", "The Lieutenant has her list of the damage, and at the top of it I've written that the crew of the "
                    "Eden Rise defended the quay. So nobody will send you a bill. [chuckle] Anything you need while "
                    "you're stuck here, you come to me first. Leave it with me.", "approval")],
       [O("Takes the bandages and shakes his hand. “Thanks, Pascal.”", [I("bandage"), I("bandage"), V("pascal", 6), WEITER("hk_ziege")],
          zeile=S("pascal", "No, no, you have it the wrong way round. We owe you. [chuckle] People here count what they "
                            "owe, Duc. It's the one thing we're good at.", "gratitude")),
        O("Looks at the suit, then at the barrel. “You rolled that thing in that suit?”",
          [I("bandage"), I("bandage"), V("pascal", 4), WEITER("hk_ziege")],
          zeile=S("pascal", "[sigh] I know. My tailor in Bastia is going to cry. But a man with no hair has to look good "
                            "somewhere, Duc, and I've run out of other places.", "amusement")),
        O("“Where were you when the boar came?”", [I("bandage"), I("bandage"), V("pascal", 2), WEITER("hk_ziege")],
          zeile=S("pascal", "[cough] Up in the church tower, ringing the bell. Badly. The priest was, let's say, praying. "
                            "I had never rung a bell in my life, and now the whole town knows it.", "embarrassment")),
        O("“So you're the one who really runs this place.”", [I("bandage"), I("bandage"), WEITER("hk_ziege")],
          zeile=S("pascal", "[clear throat] Shh, please. She has very good ears for that. I carry the broom, Duc. That's "
                            "all I do, I carry the broom.", "nervousness"))],
       personen=P1("pascal"), sets={"pascal": "pascal_standard"}, ton="wholesome"),

    # ------------------------------------------------------------------ Mina kommt (erste freie Phase ab Tag 3)
    E("g1_mina_post", "gag1", "witzig", "Special Delivery", WANN((3, 3), ["nachmittag"], **PFLICHT), "village_harbour",
      P1("mina", ("elsa", "-", "writes the ticket")),
      "An old Vespa comes down the harbour steps. Not the road, the steps. It stops with the front wheel ten centimetres "
      "from your shoe. On it sits a young woman in a pink rain jacket and a pink helmet, already holding out a handful "
      "of envelopes.",
      [S("mina", "You're the yacht! Hi, Yacht! Three bills, one letter from a bank and one love letter. [laugh] No, I "
                 "don't read them. I just know. Love letters are always on the good paper.", "excitement"),
       S("mina", "These ones are from Monaco, that's your boss, yes? Funny, the deputy mayor gets more post from Monaco "
                 "than you do. And he writes back like it's to the Pope, every letter perfect. [chuckle] It must be the hat.", "amusement"),
       S("elsa", "Mina Orsoni. Those are stairs. I have told you what stairs are. [sigh] Thirty euros.", "annoyance"),
       S("mina", "[gasp] Not agaaaain! Elsa, I was going slowly, I was only going slowly downwards!", "surprise")],
      [O("Looks at the wheel, then at his shoe. “You nearly killed me.”", [V("mina", 4)],
         zeile=S("mina", "Nearly! Ask anybody, I've never hit a person. [laugh] Two goats and a priest, but the priest "
                         "was standing in the road.", "joy")),
       O("Holds out five euros. “Who's the love letter for?”", [G(-5), V("mina", 6)],
         zeile=S("mina", "[chuckle] Five euros says it isn't for you. Ten euros says I saw nothing, and I'm very expensive "
                         "when I see nothing.", "amusement")),
       O("“Elsa, let me pay it. She brought my post.”", [V("mina", 6), V("elsa", 2)],
         zeile=S("elsa", "You can't, First Officer. [clear throat] She would only do it again, and then I'd have to be "
                         "nice to you as well.", "amusement")),
       O("“Slow down, kid.”", [V("mina", -2)],
         zeile=S("mina", "Kid? [laugh] I'm twenty-four! I have a licence and everything. Well. I have a licence.", "amusement"))],
      sets={"mina": "mina_standard", "elsa": "Standard"}),

    # ------------------------------------------------------------------ Pascals Hilfen
    E("hy_pascal_holm", "handy", "wholesome", "Visiting Hours", WANN((4, 4), ["fruehstueck"], bed=KENNT_PASCAL, pflicht=True),
      ORT_DUC, H("pascal", "rathaus"),
      "Video call from the town hall. Pascal is at his desk, standing up, eating a sandwich over a stack of paper. His "
      "hat hangs on the corner of the old mayor's portrait.",
      [S("pascal", "Duc, sorry, one minute only. I ring the hospital in Ajaccio every morning, they know me there now, and "
                   "your captain has just thrown a yoghurt at a doctor. [chuckle] I thought you'd want to know. I think "
                   "it's a very good sign.", "amusement"),
       S("pascal", "I told her the boat is in good hands, because nobody else had. [sigh] She said something in Norwegian. "
                   "I wrote it down, in case it was medical.", "caring")],
      [O("“You don't have to do this, you know.”", [V("pascal", 6), W("moral", 1)],
         zeile=S("pascal", "I know. [chuckle] That's why it's nice. You held my quay, Duc. I can hold a telephone.", "caring")),
       O("“What did she say?”", [V("pascal", 4), W("moral", 1)],
         zeile=S("pascal", "I have it here. T, A, K, K. The nurse says it means thank you. [sigh] Then she threw the "
                           "yoghurt, though, so I don't know.", "amusement")),
       O("“Tell her Frankfurt says get well.”", [V("pascal", 4), V("holm", 2), W("moral", 1)],
         zeile=S("pascal", "Frankfurt. [laugh] I will. I'll say it exactly like that, and I'll stand well back.", "joy"))],
      sets={"pascal": "pascal_standard"}),

    E("g1_pascal_gebuehren", "gag1", "wholesome", "Mooring Fees", WANN((4, 4), ["nachmittag"], bed=KENNT_PASCAL, **PFLICHT),
      "village_harbour", P1("pascal"),
      "The harbourmaster has found you on the quay. He is a lovely man with a folder, and this is minute eleven. You have "
      "heard about his cousin in Propriano, and now he is on the third page of what you owe. Then a paper cup of coffee "
      "appears in your hand, and a white fedora appears beside it.",
      [S("pascal", "Toussaint, your wife rang, the fish is getting cold. And think about it, my friend. The Eden Rise can't "
                   "move, so it isn't a boat, it's a building. [chuckle] Buildings don't pay mooring fees.", "amusement"),
       S("pascal", "Look at that, he's gone. Here's what you paid him already, Duc, he had it in the folder. [sigh] Drink "
                   "that, you look like you slept on a rope. It's the least we can do, after the quay.", "gratitude")],
      [O("Raises the paper cup. “I owe you one.”", [G(120), I("americano"), V("pascal", 4)],
         zeile=S("pascal", "You don't, and you won't. [chuckle] I keep very good accounts, Duc, and you are a long way ahead.",
                 "amusement")),
       O("“What do you get out of all this, Pascal?”", [G(120), I("americano"), V("pascal", 6)],
         zeile=S("pascal", "[sigh] Do you know, nobody has ever asked me that. A village that is still here in ten years, I "
                           "suppose. And a chair at Alva's, if I ever get the time to sit down.", "optimism")),
       O("Sniffs the cup. “What's in this?”", [G(120), I("americano"), V("pascal", 2)],
         zeile=S("pascal", "Coffee and a small prayer. [laugh] It's from Alva's, so it's mostly the prayer.", "amusement"))],
      sets={"pascal": "pascal_standard"}),

    E("g1_pascal_telefon", "gag1", "wholesome", "The Town Hall Telephone",
      WANN((6, 6), ["nachmittag"], bed={"flag": "br_satellit"}, **PFLICHT), "village_piazza",
      P1("lola", ("jana", "+", "has a biscuit in each hand")),
      "Lola comes down the town hall steps with red eyes and a huge grin, and Jana comes down behind her, holding "
      "a biscuit in each hand. It turns out the town hall has an old telephone with a real wire. The deputy mayor left it "
      "on his desk with a plate of biscuits, and then he went out for an hour.",
      [S("lola", "[sniff] Boss, that man! He asked me what Nan's name was before I'd even sat down! I was on for an hour and "
                 "ten and she didn't ring the coast guard once!", "joy"),
       S("jana", "[gasp] He says Mama can ring back on it, Sir, any Sunday, and it's free because of you. Because of the "
                 "quay. I don't know what to do. Sorry. Should I write him a letter?", "excitement")],
      [O("“Write him a letter.”", [V("jana", 4), W("moral", 1)],
         zeile=S("jana", "Okay! Yes! [laugh] Lola, how do you spell grateful?", "joy")),
       O("Takes one of Jana's biscuits. “Nobody has ever left me biscuits.”", [V("lola", 4), W("moral", 1)],
         zeile=S("lola", "[laugh] Mate, get in line. I looked in all his drawers for more. They're locked.", "amusement"))],
      sets={"lola": "Off Duty", "jana": "jana_deck_a"}),

    E("g1_pascal_ricci", "gag1", "wholesome", "Eleven Purses",
      WANN((3, 6), ["nachmittag", "tag", "fruehstueck"], bed={"flag": "ricci_3"}, holt_leute=True), "alvas_bar", P1("pascal"),
      "Pascal finds you outside Alva's, a list in one hand and a small wooden box in the other. Word has gone round that "
      "the Ricci brothers have stopped working the harbour, and that their big cousin is walking strangely.",
      [S("pascal", "Duc. Eleven purses this summer, one wedding ring and Petru's tobacco, and the tobacco was the one that "
                   "frightened me. [laugh] And now, nothing, for days. People are leaving their bags on the chairs again.", "joy"),
       S("pascal", "The town can't pay you, you've seen the town. [sigh] But this has been in the safe since before my time. "
                   "A Genoese captain left it to settle a bar bill, and all it has ever done is sit there.", "gratitude"),
       S("pascal", "Your engineer says she can put it in that bat of yours. I didn't understand one word she said, I just "
                   "nodded. [chuckle] Please take it. It's a small thing, for what this village owes you.", "caring")],
      [O("Opens the box. A green stone, cool in the hand. “Pascal, this is worth real money.”", [I("jade"), V("pascal", 4), W("ruf", 1)],
         zeile=S("pascal", "Probably. [chuckle] Don't tell Madame, she'd make it into a fountain.", "amusement")),
       O("“It was three idiots with a bag.”", [I("jade"), V("pascal", 6), W("ruf", 1)],
         zeile=S("pascal", "To you, Duc. To Madame Paoli it was her husband's ring, and he has been dead nine years. [sigh] "
                           "She got it back on Tuesday. She wants to feed you.", "sadness")),
       O("“Tell them they're welcome.”", [I("jade"), V("pascal", 2), W("ruf", 1)],
         zeile=S("pascal", "Tell them yourself. They keep buying you drinks at Alva's, and you keep not being there. "
                           "[chuckle] Petru has drunk three of them for you.", "amusement"))],
      sets={"pascal": "pascal_standard"}),

    # ------------------------------------------------------------------ Casanova
    E("g1_casanova_morgen", "gag1", "wholesome", "Five in the Morning", WANN((6, 6), ["fruehstueck"], **PFLICHT), "village_piazza",
      P1("casanova"),
      "You can't sleep, so you walk up through the village at five in the morning. The piazza is dark. At the top of the "
      "town hall steps Madame Casanova stands in a dressing gown and rubber boots, holding a stack of cards. Her only "
      "audience is Kevin, on the edge of the fountain.",
      [S("casanova", "People of Cala d'Orsu. [clear throat] No. Friends. In this, our hour of… no. Kevin, you are not even "
                     "trying.", "nervousness"),
       S("casanova", "Monsieur. You saw nothing. [cough] This is a mayor inspecting her steps.", "embarrassment"),
       S("casanova", "My father built these, you know. He could fill this square just by coming out to buy cigarettes. "
                     "[sigh] I need a cannon.", "sadness")],
      [O("Sits down on the cold step. “Read me the one you're working on.”", [V("casanova", 8)],
         zeile=S("casanova", "[clear throat] It's very short. “Thank you for coming.” That is all of it. I have been trying "
                             "to give that speech for years, Monsieur, and I always add something.", "caring")),
       O("Claps slowly, alone, in the dark.", [V("casanova", 6)],
         zeile=S("casanova", "[sniff] Oh, don't. Pascal does that. He thinks I don't know that he's the only one.", "sadness")),
       O("Says nothing and walks on, so she can keep going.", [V("casanova", 4)],
         zeile=S("casanova", "[clear throat] People of Cala d'Orsu. Kevin, one more time.", "neutral"))],
      sets={"casanova": "Standard"}),

    E("gv_casanova_megan", "gagv", "witzig", "Every Telephone in Corsica",
      WANN((5, 5), ["nachmittag"], bed={"flag": "megan_besuch"}, **PFLICHT), "main_salon",
      PV("casanova", "megan", "chiara"),
      "Madame Casanova has come aboard with a sash, a photographer and a chart of the bay. Megan is here for one night and "
      "has no time for any of it. Four minutes later they are bent over the same chart, and neither of them wants to be "
      "the first to say she is enjoying herself.",
      [S("casanova", "Here, the yacht, every light on! Here, the cannon! [gasp] Madame, when it fires, every telephone in "
                     "Corsica will point at this bay!", "excitement"),
       S("megan", "Every telephone in Corsica. Go on. [clear throat] I have investors who like a nice view, mind. Could your "
                  "people stand a wee bit further to the left?", "amusement"),
       S("casanova", "Madame! [gasp] My people are the view!", "pride"),
       S("megan", "You would do very well in my business. [chuckle] That's not a compliment, it's a warning.", "neutral")],
      [O("“The village stays in the picture.”", [V("casanova", 6), V("megan", -2), W("ruf", 1)], von="casanova",
         zeile=S("casanova", "Monsieur! Write that down! [laugh] No, I will write it down, you would leave out the adjectives.",
                 "joy")),
       O("“The investors are paying for the fuel.”", [V("megan", 6), V("casanova", -4)], von="megan",
         zeile=S("megan", "Thank you, First Officer. [chuckle] Somebody on this boat can count.", "approval")),
       O("Puts a glass on the chart. “Stand the investors on the quay with everybody else, and give them a drink.”", [],
         probe=P("charm", 12), erfolg=[V("casanova", 4), V("megan", 4), W("ruf", 1)], fehlschlag=[V("megan", -2)],
         zeile=S("megan", "Aye. All right. That's actually not terrible. [sigh] Don't tell her I said so.", "amusement"))],
      sets={"casanova": "Standard", "megan": "Inspection", "chiara": "Uniform"}),

    # ------------------------------------------------------------------ Kloster-Auftrag: danach Pascal und Mina
    FR("kl_pascal_tuer", 0, "mayors_office", "In the Corridor",
       "When you come out, Pascal is standing in the corridor with his hat in his hands, as if he had only just arrived. He "
       "doesn't ask what she said. He gives you a canvas bag: bandages, a flask of coffee, and a sandwich wrapped in the "
       "town's official paper.",
       [S("pascal", "[sigh] You're going up, then. I thought you would. I told the priest to stay down here, and he listened "
                    "to me. I'm glad you are not that kind of man.", "caring"),
        S("pascal", "Bring yourself back, Duc. I mean it, we've only just got you. [chuckle] This village owes you enough "
                    "already, and I don't want to owe you more.", "gratitude")],
       [O("Takes the bag. “Keep the coffee hot.”", [I("bandage"), I("espresso_single"), V("pascal", 4), WEITER("kl_mina_post")],
          zeile=S("pascal", "Always. [chuckle] Leave it with me.", "amusement"))],
       personen=P1("pascal"), sets={"pascal": "pascal_standard"}, ton="wholesome"),
    FR("kl_mina_post", 0, "village_piazza", "Three Weeks of Post",
       "At the bottom of the town hall steps a Vespa is waiting with its engine running. Mina isn't grinning, and it makes "
       "her look like someone else. On the seat is a bundle of letters tied with a rubber band, three weeks thick.",
       [S("mina", "You're going up to San Martinu. Don't look at me like that, Yacht, the whole street knows. [sigh] I go "
                  "every Thursday, and Nonna gives me cake. But since the animals came I can't get past the bridge.", "sadness"),
        S("mina", "So take them, please. [sniff] Some of these are for the brothers, and they'll be wanting them.", "caring")],
       [O("Takes the letters. “I'll bring you back some cake.”", [I("kl_post"), V("mina", 4), F("kl_post_dabei")],
          zeile=S("mina", "[sniff] You'd better. [chuckle] The chestnut one. Not the lemon, the lemon is a punishment.", "optimism"))],
       personen=P1("mina"), sets={"mina": "mina_standard"}, ton="wholesome"),
]

# ================================================================== Phase 3: Woche 2 (Texte abgenommen, dorf_woche2_texte.json)
LAGE_BATU = ("It is behind the harbour, down an alley that smells of drying nets. Inside there are too many shelves for the room: "
             "rice, noodles, tins, a wall of amber bottles, a small Virgin Mary with a fresh flower in front of her. At the back a "
             "very small old woman in a silk blouse stands over a very big pot. ")


def batu_chips():
    """Die vier Antworten kommen in beiden Fassungen vor; die Tags nur einmal eintragen lohnt nicht, S merkt sie doppelt."""
    offen = [F("batu_laden")]
    return [
        O("Takes one bite before he says anything. It's thịt kho, and it tastes like the kitchen at home. “My parents left after "
          "the war. Germany, in the end.”", offen + [V("batu", 8)],
          zeile=S("batu", "[sigh] Germany. Cold. Good schools. She did well, your mother. Eat, there is more egg.", "caring")),
        O("Says it in Vietnamese, badly. “Dạ. Con cảm ơn bà.”", offen + [V("batu", 8)],
          zeile=S("batu", "[chuckle] This accent. Your mother should be ashamed. Say it again, slowly, and then you can have more.",
                  "amusement")),
        O("Looks into the pot. “You put a little too much sugar in the caramel.”", offen + [V("batu", 6)],
          zeile=S("batu", "[laugh] Too much, he says. Sixty years, too much. Good. Now you sit, you tell me how much is right, and "
                          "then I tell you why you are wrong.", "amusement")),
        O("“I'm fine, thank you. I already ate on the boat.”", offen + [V("batu", 2)],
          zeile=S("batu", "On the boat. [sigh] That is not eating. That is fuel. Sit.", "disapproval"))]


def weiter_gehen(*kommentar):
    """Kleine Szene im Vorbeigehen: Das Spiel verlangt zwei Antworten, also Weitergehen und ein kleiner Kommentar."""
    return [O("Walks on.", [])] + list(kommentar)


def vorbei(id, titel, ton, bild, bed, personen, lage, zeilen, kommentar, sets):
    return E(id, "gag1", ton, titel, WANN((8, 21), ["tag", "nachmittag"], bed=bed, holt_leute=True), bild, personen, lage, zeilen,
             weiter_gehen(kommentar), sets=sets)


SET_D = {"pascal": "pascal_standard", "batu": "batu_standard", "anghjulu": "anghjulu_standard", "casanova": "Standard",
         "sandru": "sandru_av", "elsa": "Standard", "mina": "mina_standard", "petru": "Standard", "alva": "alva_standard",
         "nonna": "nonna_standard", "isabelle": "isabelle_standard"}
OHNE_LOLA = {"flag": "gefeuert_lola"}


def set_d(*pids):
    return {p: SET_D[p] for p in pids}


LAGE_FEIER = ("Three days later they hold the service in the monastery garden. There is nothing to bury, so there is a row of folded "
              "habits on a long table, with a candle for each one. ")
TRAUER_DON = [S("anghjulu", "[clear throat] I did not come up here when the animals came. That is the first thing I have to say here, and I should say it "
                            "before the other things.", "sadness"),
              S("nonna", "You're late, Anghjulu.", "disapproval"),
              S("anghjulu", "[sigh] Yes, Fiora.", "sadness")]
BRIEFE = [{"item_weg": "kl_post"}, F("kl_post_abgegeben")]

EVENTS += [
    # ------------------------------------------------------------------ Bà Tư (Tag 9, mit Lola oder, falls Lola entlassen ist, allein)
    E("g1_batu_intro", "gag1", "wholesome", "You, Later", WANN((9, 9), ["nachmittag"], bed={"nicht": OHNE_LOLA}, **PFLICHT), "batu_shop",
      P1("batu", ("lola", "?", "wants fish sauce")),
      "Lola has been talking about this shop for ten minutes and she still can't find the door. " + LAGE_BATU +
      "She looks at Lola. Then she looks at you, for a long time. Then she picks up a bowl.",
      [S("lola", "Auntie! This is my boss, the one from the quay, he cooks too, properly, I told you! [laugh] I just need two bottles "
                 "of the good fish sauce, and then I'll get out of your way.", "joy"),
       S("batu", "You, later.", "neutral"),
       S("batu", "Him, now. [clear throat] Sit. Ăn đi. Eat. You are too thin, con. Who let you go out like this?", "caring")],
      batu_chips(), sets={"lola": "Off Duty", "batu": "batu_standard"}),
    E("g1_batu_intro_allein", "gag1", "wholesome", "You, Later", WANN((9, 9), ["nachmittag"], bed=OHNE_LOLA, **PFLICHT), "batu_shop",
      P1("batu"),
      "Since Lola left, the shopping is yours, and you have spent ten minutes looking for this door. " + LAGE_BATU +
      "She looks at you for a long time. Then she picks up a bowl.",
      [S("batu", "Sit. [clear throat] Ăn đi. Eat. You are too thin, con. Who let you go out like this?", "caring")],
      batu_chips(), sets={"batu": "batu_standard"}),
    E("g1_zg_zitronengras", "gag1", "wholesome", "Foreign Grass", WANN((9, 21), ["nachmittag"], bed={"flag_seit": ["zitronengras_gepflanzt", 1]}, **PFLICHT),
      "batu_shop", P1("nonna", ("batu", "+", "gets a compliment")),
      "You are counting out money for rice when the shop door bangs open. Nonna Fiora has come all the way down the mountain, with a wooden "
      "spoon in one hand and a green stalk in the other. It is the lemongrass you planted.",
      [S("nonna", "[clear throat] There is grass in my garden. Foreign grass, in my bed, next to my garlic. Did you think I wouldn't see it?", "annoyance"),
       S("batu", "It is not grass. [sniff] Smell it. In Saigon we put it in everything, and nobody died.", "disapproval"),
       S("nonna", "I did smell it. I put it in the soup last night, to show them how bad it is. [sigh] The whole table asked for more.", "embarrassment"),
       S("batu", "[chuckle] Of course they did. You keep good soil up there, Fiora. It never grew like that behind my shop.", "amusement"),
       S("nonna", "And you keep good roots. I want more of them. [chuckle] Come up on Sunday, and I will feed you properly.", "caring"),
       S("batu", "You will feed me? [laugh] I will bring the pot. You are too thin.", "joy")],
      [O("Takes a very long time counting his coins, so he can stay and listen.", [V("batu", 3), V("nonna", 3)]),
       O("“So it was good?”", [V("batu", 2), V("nonna", 2)],
         zeile=S("nonna", "Don't push your luck. [chuckle] Pay for your rice. We are talking.", "amusement"))],
      sets=set_d("batu", "nonna")),

    E("g1_batu_mutter", "gag1", "wholesome", "Have You Called Your Mother?", WANN((12, 12), ["nachmittag"], bed={"flag": "batu_laden"}, **PFLICHT),
      "batu_shop", P1("batu"),
      "You only came in for rice. She puts the rice on the counter and keeps her hand on it.",
      [S("batu", "When did you call your mother? [clear throat] I'm not asking when she called you. A mother always calls. I'm asking "
                 "when you called.", "disapproval")],
      [O("Takes out his phone and rings home, right there at the counter. “Mẹ? It's me. No, nothing's wrong.”", [V("batu", 8), W("moral", 1)],
         zeile=S("batu", "[sniff] Good. Now you can have the rice. Tell her you are eating. Don't tell her what.", "caring")),
       O("“Last week, I think.”", [V("batu", 2)],
         zeile=S("batu", "You think. [sigh] She knows exactly. To the day, she knows. The rice stays here until you know too.", "disapproval"))],
      sets={"batu": "batu_standard"}),

    # ------------------------------------------------------------------ Sandru
    E("g1_sandru_logo", "gag1", "witzig", "The New Sign", WANN((10, 10), ["tag"], **PFLICHT), "av_market",
      P1("sandru", ("elsa", "+", "reads his name tag")),
      "The whole village is standing in the street, and nobody is going in. Over the door of the old shop house opposite Alva's bar "
      "hangs a new sign, cold and white even in the sun. You know that logo. You held it in your hand yesterday, on a small black part "
      "from your generator. Across the street Alva stands in her doorway with a cloth in her hand, not wiping anything. In the middle "
      "of it all a thin young man in a white polo shirt is giving out coupons.",
      [S("sandru", "[laugh] Free coffee! Opening day, the first one is free, it's really free, you only need the app. No, there's no app "
                   "yet. Ha. Just take one.", "nervousness"),
       S("elsa", "Alex. [chuckle] It says Alex on your chest. Sandru, I have known you since you were eating sand. Who is Alex?", "amusement"),
       S("sandru", "[laugh] It's for the system, Elsa. The system didn't like the other one.", "embarrassment"),
       S("sandru", "[laugh] You're the one from the quay. Hi. Alex. Sandru. Either is fine, really. Coffee?", "nervousness")],
      [O("Takes a coupon and looks up at the logo. “Who owns this place?”", [F("a2_sandru"), V("sandru", 4), I("espresso_single")],
         zeile=S("sandru", "[laugh] A company in Monaco. They send the prices, and I put them on the shelves. I've never actually met "
                           "anyone. That's normal, I think?", "nervousness")),
       O("Looks across the street at Alva. “She doesn't look happy.”", [F("a2_sandru"), V("sandru", 4), V("alva", 2)],
         zeile=S("sandru", "[sigh] No. It was her mother's house. Sorry, it is her mother's house. I know exactly whose house it is, I "
                           "carried crates in here when I was twelve.", "sadness")),
       O("Hears something small when he steps closer, a thin electric hum. “What's that noise?”", [F("a2_sandru"), F("sandru_surren"), V("sandru", 2)],
         zeile=S("sandru", "[clear throat] Nothing. New shoes.", "fear")),
       O("Gives the coupon back. “Not today.”", [F("a2_sandru"), V("sandru", -2), V("alva", 2)],
         zeile=S("sandru", "[laugh] That's okay. Nobody today, so far. You're in very good company.", "sadness"))],
      sets=set_d("sandru", "elsa")),
    E("g1_sandru_tafel", "gag1", "ernst", "The Chalkboard", WANN((13, 13), ["abend"], **PFLICHT), "alvas_bar",
      P1("sandru", ("alva", "?", "is holding the bottle")),
      "The bar goes quiet when he comes in, the way a bar does. Sandru is still wearing the white shirt, and he walks to the counter "
      "carefully, listening to his own legs. Behind Alva hangs her father's chalkboard, with the whole village on it and what each of "
      "them orders. His name is still there, low down, in an old man's handwriting. Sandru: orangeade.",
      [S("sandru", "[clear throat] A grappa, please, Alva.", "nervousness"),
       S("alva", "[sigh] We're out.", "neutral"),
       S("sandru", "[sigh] You are holding the bottle.", "sadness"),
       S("alva", "I know what I'm holding. [sigh] Here.", "neutral"),
       S("sandru", "[sniff] I'm thirty, Alva.", "sadness"),
       S("alva", "I know how old you are. I was there. [sigh] Take that thing off my mother's house, Sandru.", "sadness"),
       S("sandru", "[sigh] You know I can't.", "sadness"),
       S("alva", "[sigh] I know. Drink your orangeade.", "caring")],
      [O("Sits down on the next stool. “I'll have what he's having.”", [V("sandru", 8), V("alva", 2), F("sandru_tafel")],
         zeile=S("alva", "[sigh] Two orangeades. God help this bar.", "neutral")),
       O("Stays at the counter with her. “He looks like he came to say something.”", [V("alva", 6), F("sandru_tafel")],
         zeile=S("alva", "He did. [sigh] He has been coming to say it since he was eleven.", "sadness")),
       O("Puts money down for both glasses and leaves them to it.", [V("alva", 2), V("sandru", 2), F("sandru_tafel")],
         zeile=S("alva", "Take that back. [sniff] Papa never charged for that orangeade, and I'm not going to start.", "neutral"))],
      sets=set_d("sandru", "alva")),

    # ------------------------------------------------------------------ Totenfeier (direkt nach Le Large), Auflagen der Story-Sitzung
    FR("kl_totenfeier_lebt", 11, "monastery_garden_dusk", "The Long Table",
       LAGE_FEIER + "The deputy mayor arranged all of it: the candles, the chairs carried up the mountain, and the priest, who has shaved "
       "and is nearly standing straight. Pascal has taken off his hat. You have never seen him without it. Frederico holds a basket of "
       "bread, baked too dark on purpose.",
       TRAUER_DON + [
           S("nonna", "Pascal. The chairs, the candles. You paid for all of it, don't tell me you didn't. You are a good man.", "gratitude"),
           S("pascal", "[sigh] No, no. Please, Madame. Leave it with me.", "sadness")],
       [O("Takes the rubber band off Mina's letters and lays each one on the habit it belongs to.", BRIEFE + [V("nonna", 6), WEITER("kl_mina_fragt")],
          zeile=S("nonna", "Brother Teo's sister writes every month. She doesn't know yet. [sniff] I will write to her tonight.", "grief")),
        O("Keeps the letters in his jacket and gives them to Nonna afterwards, without a word.", BRIEFE + [V("nonna", 4), WEITER("kl_mina_fragt")],
          zeile=S("nonna", "[sniff] Later, yes. You were brought up properly. Somebody should tell your mother.", "gratitude"))],
       personen=P1("anghjulu", ("nonna", "?", ""), ("pascal", "?", "")), sets=set_d("anghjulu", "nonna", "pascal")),
    FR("kl_totenfeier_tot", 11, "monastery_garden_dusk", "The Long Table",
       LAGE_FEIER + "The deputy mayor arranged it all, and the priest has shaved. Nonna comes out last and sits at the back. At the end of "
       "the table, past the last habit, somebody has put a wooden goat. It has no candle.",
       TRAUER_DON + [
           S("pascal", "[sigh] Nobody told me there was a boy. I ordered for the brothers, I only ordered for the brothers. Please wait. I'll "
                       "go down and get one more. It's an hour, please don't start without him.", "sadness")],
       [O("Takes the rubber band off Mina's letters and lays each one on the habit it belongs to.", BRIEFE + [V("isabelle", 6), WEITER("kl_mina_fragt_tot")],
          zeile=S("isabelle", "[sniff] He used to run down to the bridge for these, so Mina wouldn't have to climb. He kept the stamps.", "grief")),
        O("Gives the letters to Isabelle and waits with her for the candle.", BRIEFE + [V("isabelle", 8), WEITER("kl_mina_fragt_tot")],
          zeile=S("isabelle", "[sniff] Thank you. It's a long way down. He'll run. Look at him, he's already running.", "grief"))],
       personen=P1("anghjulu", ("nonna", "?", ""), ("pascal", "?", "")), sets=set_d("anghjulu", "nonna", "pascal", "isabelle")),
    FR("kl_mina_fragt", 12, "macchia_creek_bridge", "Did They Read Them?",
       "Mina is waiting at the bridge with the engine off. Nonna gave you something for her, in a napkin: a piece of chestnut cake. Mina "
       "breaks it in two and gives you the bigger half, and for a while nobody says anything.",
       [S("mina", "[sigh] So, Yacht. All those letters I gave you for the brothers. Did they read them?", "sadness")],
       [O("“No. I put them where they belonged.”", [V("mina", 6)],
          zeile=S("mina", "[sniff] Okay. That's okay. I'll go up on Thursday, same as always. There's still post for Nonna.", "sadness")),
        O("“Some of them.”", [V("mina", 4)],
          zeile=S("mina", "[sigh] You're a really bad liar, Yacht. [sniff] Thanks, though.", "caring"))],
       personen=P1("mina"), sets=set_d("mina")),
    FR("kl_mina_fragt_tot", 12, "macchia_creek_bridge", "Did They Read Them?",
       "Mina is waiting at the bridge with the engine off. Nonna gave you something for her, in a napkin: a piece of chestnut cake. Mina "
       "breaks it in two and gives you the bigger half, and for a while nobody says anything.",
       [S("mina", "[sigh] So, Yacht. All those letters I gave you for the brothers. Did they read them?", "sadness")],
       [O("“No. I put them where they belonged.”", [V("mina", 6), F("mina_ernte")],
          zeile=S("mina", "I'll do the harvest now, in the mornings. [sigh] Don't say anything, okay? Just don't say anything.", "sadness")),
        O("“Some of them.”", [V("mina", 4), F("mina_ernte")],
          zeile=S("mina", "[sigh] You're a really bad liar, Yacht. I'll do the harvest now, in the mornings. [sniff] Don't say anything, okay?", "caring"))],
       personen=P1("mina"), sets=set_d("mina")),

    # ------------------------------------------------------------------ Der Pfarrer
    FR_G("kv_don", 5, "village_rooftops", "The Man at the Bottom",
         "At the bottom of the drainpipe a round, sun-browned man in a black cassock stands with his sleeves rolled up and a flask in his "
         "hand, looking up at the tower with deep satisfaction.",
         [S("anghjulu", "My son! [laugh] Fourteen years I fight that devil! I have tried prayer, a broom and one of Petru's nets. I have "
                        "blessed him and I have cursed him, once with the same words. And you just went up there and screamed!", "joy"),
          S("anghjulu", "Don Anghjulu. It isn't my name. My name is Padre Ângelo, but I came here from Portugal for one week, and this village "
                        "doesn't give things back. [chuckle] God sees everything. Have a drink.", "amusement")],
         [O("Takes the flask. “Thank you, Father.”", [V("anghjulu", 6)],
            zeile=S("anghjulu", "[chuckle] Careful, it's blessed. That's what I tell the Lieutenant, anyway.", "amusement")),
          O("“It's ten in the morning, Father.”", [V("anghjulu", 4)],
            zeile=S("anghjulu", "[sigh] It is always ten in the morning somewhere, my son, and God is there too.", "amusement")),
          O("“So you're the one who rang the bell so badly, the day that boar came onto the piazza.”", [V("anghjulu", 2)],
            zeile=S("anghjulu", "[cough] That was Pascal. I was praying. Very deeply. On my back.", "embarrassment"))],
         personen=P1("anghjulu"), sets=set_d("anghjulu"), ton="witzig", tage=(12, 14)),
    E("g1_messe", "gag1", "wholesome", "Sunday Mass", WANN((14, 14), ["fruehstueck"], **PFLICHT), "church",
      P1("anghjulu", ("batu", "?", "knows the Latin"), ("pascal", "+", "carries the plate"), ("casanova", "?", "has a card up her sleeve")),
      "Sunday. The bell rings in nearly the right rhythm. Everybody has come, because the church has a new roof and nobody wants to look as "
      "if they've noticed. Bà Tư sits in the first pew with a prayer book older than the building. Pascal goes along the rows with the "
      "collection plate and says every name. Sandru sits at the back near the door, where it's easier to stand up. Madame Casanova has a "
      "card up her sleeve. Alva hasn't come. Mina arrives during the first reading. You can hear the Vespa.",
      [S("anghjulu", "A man has come to this island with a lot of money, and he says he has brought the future. [clear throat] I have read "
                     "about the future, brothers and sisters. It doesn't end well for the man with the money.", "neutral"),
       S("batu", "Vobiscum, Anghjulu. Vobiscum. [sigh] Sixty years I hear this, and nobody says it right.", "disapproval"),
       S("anghjulu", "[sigh] Thank you, Madame Tu. The Lord heard you. Everybody heard you.", "amusement"),
       S("casanova", "[clear throat] If I may, Father, a small word from the municipality. And was that the blood of Christ I smelled at "
                     "the door, or the good Patrimonio?", "amusement"),
       S("anghjulu", "[chuckle] Yes, Madame.", "amusement"),
       S("pascal", "Good morning, Duc. [chuckle] No, put that away, you've done enough for this village. The roof is paid for, thank God. "
                   "Don't ask me how, I only carry the plate.", "caring")],
      [O("Puts a note on the plate anyway.", [G(-10), W("ruf", 1), F("a2_messe"), V("pascal", 4)],
         zeile=S("pascal", "[sigh] You see, this is what I mean. This is what I tell them about you.", "gratitude")),
       O("Looks up at the pale new beams. “Who did pay for it?”", [F("a2_messe"), V("anghjulu", 2)],
         zeile=S("anghjulu", "The Lord provides, my son. [chuckle] I don't ask which account.", "neutral")),
       O("Turns round to look at all the faces.", [F("a2_messe"), W("moral", 1)],
         zeile=S("batu", "Eyes front, con. [clear throat] God is not back there.", "disapproval"))],
      sets=set_d("anghjulu", "batu", "pascal", "casanova")),

    # ------------------------------------------------------------------ Das Dorf lebt ohne dich
    vorbei("g1_vb_brot", "Bread Under Review", "witzig", "av_market", {"flag": "a2_sandru"}, P1("elsa", ("sandru", "+", "bakes")),
           "Elsa stands at the door of the A.V. Market with a loaf under her arm and her notebook open.",
           [S("elsa", "[clear throat] That's bribery, Sandru.", "neutral"), S("sandru", "[laugh] It's bread, Elsa.", "joy"),
            S("elsa", "[clear throat] Figs are fine. Bread is under review.", "amusement")],
           O("“What's the verdict, Lieutenant?”", [V("elsa", 2)],
             zeile=S("elsa", "Still warm. [chuckle] The investigation continues.", "amusement")), set_d("elsa", "sandru")),
    vorbei("g1_vb_wangen", "Such a Pretty Girl", "witzig", "batu_shop", {"flag": "batu_laden"}, P1("batu", ("elsa", "-", "has a cheek")),
           "Elsa puts a coin on Bà Tư's counter as a tip. A small hand comes across the counter and takes her by the cheek.",
           [S("batu", "Such a pretty girl. [sigh] Twenty-nine years old. Where is the husband?", "caring"),
            S("elsa", "Madame, I am in uniform. [clear throat] I am armed.", "embarrassment"),
            S("batu", "[chuckle] Armed is good. A husband likes a safe house. Take the soup.", "approval")],
           O("Stays in the doorway a moment too long.", [V("elsa", 2)],
             zeile=S("elsa", "First Officer. [sigh] You saw nothing. That's an order, and I can't give you orders.", "annoyance")),
           set_d("batu", "elsa")),
    vorbei("g1_vb_fahne", "Not Driving", "witzig", "village_piazza", {"bekannt": "anghjulu"}, P1("elsa", ("anghjulu", "-", "is walking")),
           "Don Anghjulu comes down the church steps one at a time. Elsa watches him from across the piazza, then walks over.",
           [S("elsa", "[clear throat] You're not driving, Father.", "disapproval"), S("anghjulu", "[chuckle] I am walking, Lieutenant.", "amusement"),
            S("elsa", "[sigh] You're not doing that very well either.", "amusement")],
           O("Offers the priest his arm.", [V("anghjulu", 4)]), set_d("elsa", "anghjulu")),
    vorbei("g1_vb_eu", "European Money", "witzig", "village_piazza", {"flag": "kl_post_dabei"},
           P1("casanova", ("mina", "+", "brings the post"), ("pascal", "+", "says almost")),
           "Mina stops her Vespa on the town hall steps with a handful of envelopes. The window above her flies open.",
           [S("casanova", "Mina! If that is another bill, throw it in the sea! [gasp] Where is my European money?", "anger"),
            S("mina", "Brussels says hi! [laugh] Also, you owe the water company.", "amusement"),
            S("casanova", "[gasp] I have applied FOUR times! Pascal! Tell her I have applied four times!", "anger"),
            S("pascal", "[chuckle] It's with them, Madame. Almost through.", "caring")],
           O("Waves up at the window.", [V("casanova", 2)]), set_d("casanova", "mina", "pascal")),
    vorbei("g1_vb_eintopf", "Fish Stew", "wholesome", "petru_workshop", {"flag": "batu_laden"}, P1("batu", ("petru", "+", "is not alone")),
           "Bà Tư has walked across the whole quay with a pot. Petru looks up from a net that isn't broken. She puts the pot on his workbench "
           "and takes off the lid, and the smell reaches the boats.",
           [S("batu", "You are alone too much. [clear throat] Eat.", "disapproval"), S("petru", "[sigh] It stinks.", "neutral"),
            S("batu", "[sniff] You said this last week. And then the pot was clean.", "neutral"), S("petru", "[chuckle] Hm.", "neutral")],
           O("Asks if there is any left.", [V("batu", 2), V("petru", 2)]), set_d("batu", "petru")),
    vorbei("g1_vb_auntie", "Auntie Tu", "wholesome", "batu_shop", {"flag": "batu_laden"}, P1("batu", ("casanova", "+", "came about the drains")),
           "Through the shop window you can see the mayor at the back table, sash folded on the chair, a third bowl in front of her. She isn't "
           "making a speech. You've never seen that from outside.",
           [S("casanova", "[clear throat] I only came about the municipal drains, Auntie Tu.", "embarrassment"),
            S("batu", "Yes, yes. Drains. [chuckle] A mayor should not be so thin. Sit.", "caring"),
            S("casanova", "[sniff] Is there any more of the egg?", "caring")],
           O("Knocks on the glass and waves.", [V("casanova", 2)]), set_d("batu", "casanova")),
]

for _e in EVENTS:
    if _e["id"] in ("g1_pascal_gebuehren", "g1_pascal_ricci", "g1_casanova_morgen", "g1_batu_mutter", "g1_batu_intro_allein"):
        _e["solo"] = True                       # nur eine Figur auf der Buehne
    if _e["id"] == "g1_zg_zitronengras":
        _e["wann"]["akt2"] = [22, 35]           # auch spaeter gekauft: die Szene kommt trotzdem
    if _e["id"] == "g1_pascal_ricci":
        _e["wann"]["akt2"] = [8, 21]            # die Riccis koennen auch in Akt 2 enden

# Zeilen in bestehenden Events (dort ohne Tag, hier die gesprochene Fassung)
ZUSATZ = [
    ("pascal", "I have the broom, Madame. I brought two. [chuckle] It went much better at eleven o'clock, Duc, you should "
               "have seen it."),
    ("pascal", "[cough] Lieutenant, this is my fault, please write it down. I ordered the small machine. This is the small "
               "machine."),
    ("elsa", "Then I'll need a form, Monsieur Leca. [clear throat] The same kind as the one for my antenna, I suppose. It's "
             "been eleven months."),
    ("pascal", "Almost through, Elsa. [chuckle] I promise you, almost."),
    ("pascal", "Four metres eighty, Madame. [chuckle] It's for the rope, Alva, only the rope. Don't look at me like that, I "
               "just hold the tape."),
    ("casanova", "Nobody. Pascal, of course, Pascal knows everything. Nobody else I trust. Petru says the mountain will "
                 "speak when it wants to. [sigh] I'm tired of waiting for mountains."),
]
STIMME += [(w, klar(g), g) for w, g in ZUSATZ]


def tags_schreiben():
    pfad = os.path.join(EDEN, "module", "eden_rise", "stimme_tags.json")
    d = json.load(open(pfad, encoding="utf-8"))
    neu = [{"wer": w, "text": t, "gesprochen": g, "quelle": "dorf"} for w, t, g in STIMME]
    texte = {z["text"] for z in neu}
    d["zeilen"] = [z for z in d["zeilen"] if z.get("quelle") != "dorf" and z["text"] not in texte] + neu
    json.dump(d, open(pfad, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return len(neu)
