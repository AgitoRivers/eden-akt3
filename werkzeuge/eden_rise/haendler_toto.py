# -*- coding: utf-8 -*-
"""Totòs feste Saetze (26.10.2026, Duc: Haendler-Pilot) - Quelle fuer modul_eden_rise.py (MODUL["laeden"]["toto"]).

Aufbau (alles Englisch, Spielsprache; Stimme: docs/wiki/figuren/toto.md - Comandante, Madonna, piccola, gigante, sonst kein
Deko-Italienisch):
  gruss_0 .. gruss_5   8 Gruesse je Vertrauensstufe, wechseln ohne Wiederholung (kern/handel.py haendler_auftritt)
  kauf                 allgemeiner Satz nach dem Kauf (Rueckfall)
  kauf_<kategorie>     Reaktion je Kategorie; bei Geschenken neckt er: "fuer wen?"
  kauf_<art>           dasselbe fuer Kampf, Schmuggel, Vorraete, Werkzeug
  hinweis_<kat>_<pid>  Hinweis, wer das Geschenk moegen koennte - nur ausgewaehlt, wenn die Person es wirklich mag
                       (Wertung >= 1 in items[...].geschenk); Chance ca. 40 % beim Kauf eines Geschenks
  verkauf, pleite      wie bisher
TOTO_GEFUEHL: je Gruppe ein Gefuehl (Sprite) oder eine Liste, die zu den Saetzen passt. Standard ist NEUTRAL, joy nur bei
hohem Vertrauen (Duc 26.10.).
"""

TOTO_ZEILEN = {
    # ---------------------------------------------------------------- trust 0: a stranger, selling hard
    "gruss_0": [
        "Comandante! Come in, come in. Don't look at the boxes, the boxes are for the engine room.",
        "A new captain. Good. New captains always need things, and they never know yet what they need. That's where I come in.",
        "Everything in here is legal. Nearly. Nobody has complained so far, and in Naples that's the law.",
        "The prices are on the list. The list is a suggestion, but we don't know each other yet, so I'll pretend it's not.",
        "You want something, I have something. You don't want something, I still have something. That's just how a locker works.",
        "Careful with the door, Comandante, it sticks. It sticks on purpose. Fewer visitors that way.",
        "I'm Totò. Bosun, shopkeeper, cousin to half of Naples. Ask anyone on the boat about me. Except Elsa. Don't ask Elsa.",
        "No, I don't know where it came from. Yes, I can get you another one. Both things are true, so don't make that face.",
    ],
    # ---------------------------------------------------------------- trust 1: he remembers you
    "gruss_1": [
        "Comandante, you're back. Good, good. I was starting to think the lock scared you.",
        "Ah, my favourite customer. Don't tell the others. They all think they're my favourite customer.",
        "Be honest, when did you last eat something proper? I have a sandwich. It's mostly bread, but it's bread with feelings.",
        "Elsa was asking about you. Not about me, for once. Congratulations, I'm jealous.",
        "Take your time. Look around. Touch nothing that glows.",
        "The coffee is terrible, Comandante, but it's free. That's the best kind of terrible.",
        "I put a few things aside for you. Not the best things. The best things I'm still deciding about.",
        "Business is slow, which is good. Slow business means nobody is watching.",
    ],
    # ---------------------------------------------------------------- trust 2: friends, with jokes
    "gruss_2": [
        "Comandante! There he is. Sit on the crate, it's the comfortable one. The other crate bites.",
        "My mother says a man who comes back twice is a man you can trust. My mother also says that about cats.",
        "I have a good feeling about today. It's the garlic. Or the weather. Mostly the garlic.",
        "Rosi beat me at arm wrestling again. Don't say anything. If you say anything, the prices go up.",
        "Tell me what you need and I'll tell you what it costs. Then we're both a little disappointed, and then we have a deal.",
        "You're the first captain who says thank you when I hand him something. Don't stop. It's confusing and I like it.",
        "I've been practising a bet on you. Two to one that you walk out with something you didn't come for.",
        "Careful, Comandante, I'm starting to enjoy these visits. It's bad for business.",
    ],
    # ---------------------------------------------------------------- trust 3: he starts to confide
    "gruss_3": [
        "Come in, close the door. No, not for a secret. The draught is bad for the cheese.",
        "Do you want to hear something silly? I'd like a market stall. In the village, with a stamp from the town hall. Nobody in my family ever sold anything with a stamp.",
        "A man in my position meets a lot of people, Comandante. Most of them I wouldn't leave alone with my wallet. You I'd leave with my wallet and the keys.",
        "Jana tied her first bowline today. I nearly cried. Don't tell her, she thinks I only cry at football.",
        "Good price today, and I'm not even trying to cheat you. I checked twice. It feels strange, I'm not used to it.",
        "My cousin called from Bastia. He says hello. He says a lot of other things too, mostly about money, but hello comes first.",
        "You're good to this crew, you know. People notice. I notice. I wrote it in the book, next to the bets I lost on purpose.",
        "Sit down, eat something. We'll talk prices once you have a full stomach. That's how it's done in Naples.",
    ],
    # ---------------------------------------------------------------- trust 4: family
    "gruss_4": [
        "Comandante. For you, the family price. Not the one I tell Megan's drone. The real one.",
        "I told my mother about you. She says you sound too thin. She's praying for you now. That's good news, she doesn't pray for everyone.",
        "Whatever you need, you ask me first. Before Elsa, before Chiara. I won't tell them I'm better.",
        "Nobody comes into my locker without knocking. You can come in without knocking. Don't make it a habit. No, okay, make it a habit.",
        "You know what I like about you? You don't ask where things come from, and you pay. Both. It's rare. It's like a rainbow.",
        "I kept the good bottle for you, behind the life jackets. If Chiara finds it, it was a gift from the sea.",
        "When Elsa finally takes me away, you'll water my basil, yes? It's the only honest thing I own.",
        "Eh. Comandante. It's good to see you. Is that strange to say? It is. Don't make a face.",
    ],
    # ---------------------------------------------------------------- trust 5: brother
    "gruss_5": [
        "My brother! No, don't correct me. It's what you are now. Naples never forgets, and neither do I.",
        "Take whatever you want, I'll write it in the book. The book is a lie. The book has been a lie for years, but a loving one.",
        "I'll tell you something one day, Comandante. Not today. Today I sell you a fish and we're both happy.",
        "Do you know what it means to have someone at the door you don't have to check first? It means I sleep. A little. Mostly.",
        "For you, everything is on the house. Everything except the things that aren't. That's most of it. But the feeling is on the house.",
        "When I get my stall with the stamp, the first sale is for you. First sale is always free. My mother's rule. Also a terrible business plan.",
        "You pulled me out of a very bad week, Comandante, and you never asked for a share. I'm still waiting for the catch.",
        "Sit. Eat. Tell me about your day. I'm not selling anything, I just want to hear it. That's new for me. I like it.",
    ],
    # ---------------------------------------------------------------- after any purchase
    "kauf": [
        "Excellent choice! You have taste, Comandante.",
        "Pleasure doing business. And remember, you didn't buy it here.",
        "Wrapped with love. Well. Wrapped.",
    ],
    # ---------------------------------------------------------------- gifts: he teases ("who is it for?")
    "kauf_intim": [
        "Ah. Ah! Comandante. No, I don't ask. I only wonder, very loudly, inside my head, who it's for.",
        "No receipt, no warranty, no witnesses. I have never respected a man's privacy so much.",
        "I wrapped it twice. Once for the gift, once for your dignity.",
    ],
    "kauf_schmuck": [
        "Something that shines! Who's it for, Comandante? Don't answer. I'm nosy, but I'm discreet.",
        "Good eye. Small things shine the most. That's why I wear a very large chain.",
        "Real? Real enough that nobody asks. And that's the only real that matters at sea.",
    ],
    "kauf_papier": [
        "Paper! Somebody is going to feel very understood. Who? Don't tell me, let me guess for a week.",
        "A gift you can read. Good, Comandante. Things you can read last longer than things you can eat.",
        "They say the pen is mightier than the sword. I've seen Maxwell. I'd still bet on Maxwell.",
    ],
    "kauf_technik": [
        "A thing with parts! Whoever gets that will say 'Oh' first and 'Thank you' second. I've seen it happen.",
        "Batteries not included. Batteries never are. It's the oldest joke in the world and I still fall for it.",
        "I'd tell you it works. But I'm a man of honour. I'd tell you it probably works.",
    ],
    "kauf_essen": [
        "Food as a gift. Good. Nobody ever says 'I hate it' to the person who brought food. Except Maxwell, once. About broccoli.",
        "Give it fast or eat it fast, Comandante. A present that goes soft has a short career.",
        "For somebody hungry, or for somebody you'd like to stay a little longer? Don't answer. I like not knowing.",
    ],
    "kauf_alkohol": [
        "Now we're talking. A bottle is the best way to say 'I thought about you' without having to talk.",
        "Taste the first sip yourself. It's a rule. A Neapolitan rule, I just made it up, but it's still a rule.",
        "I'll write it down as 'medicinal'. It's what I always write. Nobody has ever asked what for.",
    ],
    "kauf_party": [
        "Noise and glitter! Somebody will have a very good day, Comandante. And somebody else will have to clean up.",
        "A present with confetti. I've been to less joyful weddings.",
        "Don't open it in the engine room. Rosi will tell you why. Loudly.",
    ],
    "kauf_natur": [
        "From the sea or the earth, no tax, no stamp. The best presents come that way.",
        "Natural things! My mother would approve. She'd complain about the price, but she'd approve.",
        "Hold it gently. It's alive. Or it was. Or it will be, if you're lucky.",
    ],
    # ---------------------------------------------------------------- other wares
    "kauf_kampf": [
        "For fighting! I like a man who is prepared. I like a man who is prepared and also pays.",
        "Try not to need it, Comandante. But if you do, you'll thank me, and I'll say it was nothing. It was something. It was the price.",
        "Take it. And if someone hits you, hit them back. Politely. Neapolitan style.",
    ],
    "kauf_schmuggel": [
        "I don't know where that came from. I never knew. Do you know what a clean conscience is? An empty head.",
        "Put it somewhere dry. And somewhere Elsa doesn't look. Those are two different places.",
        "Between us, it's very good. Between us. If it ever comes up, I was in Naples.",
    ],
    "kauf_ressource": [
        "Supplies! Practical. Boring. Necessary. My three favourite words on a receipt.",
        "Without these the boat is just a very expensive raft. I'm glad you thought of it.",
        "Take it, Comandante, and tell Rosi it was her idea. She always likes that.",
    ],
    "kauf_werkzeug": [
        "A tool. Good. A man with a good tool is dangerous. A man with a good tool and a plan is Rosi.",
        "It's heavy because it's good. That's what I tell my cousin about everything.",
        "Treat it well. A tool you love is a tool that doesn't hit your thumb. Mostly.",
    ],
    # ---------------------------------------------------------------- hints: who might like the gift (always true)
    "hinweis_intim_sophia": [
        "If you're asking who'd like that, I'll say this much: somebody with a little brown notebook who never tells you what's in it. I'm not saying a name. I'm saying notebook.",
    ],
    "hinweis_intim_lola": [
        "That one would get a laugh out of the galley. Somebody down there laughs at her own jokes, and I'd like to be in the room when she opens it.",
    ],
    "hinweis_intim_alva": [
        "The woman with the only bar in the village sees everything and tells nobody. If she got that, she'd know who sent it before you did.",
    ],
    "hinweis_schmuck_chiara": [
        "Somebody on this boat gives everything a number out of ten. This one would get a nine, and then she'd wear it every day without telling a soul.",
    ],
    "hinweis_schmuck_sophia": [
        "A person who calls everyone darling would say nothing at all when she opens that. For her, that's a love letter.",
    ],
    "hinweis_schmuck_alva": [
        "Put that on the bar in front of the right woman and she'll pretend not to look. For about two seconds.",
    ],
    "hinweis_schmuck_megan": [
        "There's a boss on the mainland who likes small, expensive things she can pretend she never wanted. This is small. This is expensive. I'm only describing a ring.",
    ],
    "hinweis_schmuck_yasin": [
        "A man with a very large watch always has room for one more shiny thing. I'm not naming names. I'm naming the watch.",
    ],
    "hinweis_schmuck_casanova": [
        "If the mayor sees it, Comandante, there will be a speech. A long one. With music. I'm only warning you.",
    ],
    "hinweis_papier_chiara": [
        "Paper and pens make a certain person very happy. She has a clipboard for everything. She even rates her clipboards.",
    ],
    "hinweis_papier_sophia": [
        "Nice paper, a good pen. That's for a woman who writes things down and closes the book when you walk in.",
    ],
    "hinweis_papier_siri": [
        "There's a girl on the foredeck who apologises to chairs. Give her something to write in and she'll apologise to the page, but she'll write.",
    ],
    "hinweis_papier_holm": [
        "The captain reads a checklist the way other people read love poems. Nobody dares say it. I just said it. Please don't tell her.",
    ],
    "hinweis_papier_petru": [
        "Old Petru has a drawer full of charts and nobody to show them to. Something with paper and a little sea in it. He'd say 'Hm.' That means yes.",
    ],
    "hinweis_papier_megan": [
        "Fine paper, serious paper, paper that says 'I'm in charge'. There's someone in a very tall building who'd like that. She'd never say thank you without a condition.",
    ],
    "hinweis_technik_rosi": [
        "Anything with a switch, a dial or a very sad cable. There's a woman in the engine room who talks to her tools. She'd be talking to this one by lunchtime.",
    ],
    "hinweis_technik_yasin": [
        "Anything with a screen or a camera. A man who films everything would film the box before he opened it.",
    ],
    "hinweis_technik_elsa": [
        "For the coast guard, anything that takes batteries and doesn't need a form. She'd call it evidence. She'd keep it.",
    ],
    "hinweis_technik_lea": [
        "Our little diver likes things that go underwater, or at least try. She'd tell you three facts about it before you could say thank you.",
    ],
    "hinweis_essen_holm": [
        "The captain eats what's in front of her and says nothing. That means it's good. Make it salty, she has Norway in the blood.",
    ],
    "hinweis_essen_elsa": [
        "Somebody in a uniform, with a boat and two men, would eat that too. She'll call it a courtesy and write it down.",
    ],
    "hinweis_essen_petru": [
        "The old fisherman likes simple. Bread, cheese, a bit of salt. He'd say 'Hm.' and mean 'sit down'.",
    ],
    "hinweis_essen_casanova": [
        "The mayor would call that a feast and make a speech about it. Bring it near the village, and bring earplugs.",
    ],
    "hinweis_alkohol_lola": [
        "Somebody in the galley says she cooks with wine. I think half goes in the pot. The other half goes in the cook.",
    ],
    "hinweis_alkohol_alva": [
        "A gift for the woman who owns a bar? She'll grade it like a judge and then drink it like a friend.",
    ],
    "hinweis_alkohol_megan": [
        "Somebody on the mainland drinks single malt and calls it a quiet moment. She'd ask what it cost. And then she'd keep it.",
    ],
    "hinweis_alkohol_petru": [
        "The old man at the harbour has a bottle he never opens and a friend he never mentions. A good one would start a story. Maybe two.",
    ],
    "hinweis_party_lola": [
        "Somebody who makes the whole galley sing would love that. She says it's for the mood. Mostly it's for the cheese.",
    ],
    "hinweis_party_alva": [
        "Noise and glitter for the woman with the bar. She'll put it next to the bottles and pretend she bought it herself.",
    ],
    "hinweis_party_casanova": [
        "The mayor lives for that. You give her confetti, she gives you the village. Do you want the village? I'd think about it.",
    ],
    "hinweis_party_lea": [
        "Our young diver would hang it on the dive locker and call it a celebration. For no reason. That's the best kind.",
    ],
    # ---------------------------------------------------------------- selling to him, and no money
    "verkauf": [
        "Mm. It's worth less than you think. But I'll give you more than it's worth, because I'm stupid.",
        "Don't ask where it goes. It goes where it's loved.",
        "Cash, no receipt. The best kind of cash.",
    ],
    "pleite": [
        "No money? Comandante... even I can't sell air. Not yet.",
        "The prices won't jump into your pocket on their own. Come back with more, and I'll pretend I never saw this.",
        "Empty pockets, Comandante? Madonna. Sit, have a coffee. The coffee is on the house. Only the coffee.",
    ],
}

# Sprite expression per line (GoEmotions labels of the figure set). Neutral by default, warm with trust, joy only late;
# "amusement" (laughing behind the hand) only for a few teasing lines (Duc 26.10.: not everything on joy).
_N = "neutral"
TOTO_GEFUEHL = {
    "gruss_0": [_N] * 8,
    "gruss_1": [_N, "optimism", _N, _N, _N, _N, _N, _N],
    "gruss_2": ["approval", "optimism", "optimism", "pride", _N, "gratitude", "optimism", "approval"],
    "gruss_3": [_N, "optimism", "approval", "pride", "approval", "caring", "approval", "caring"],
    "gruss_4": ["approval", "caring", "approval", "optimism", "admiration", "optimism", "caring", "gratitude"],
    "gruss_5": ["joy", "caring", _N, "gratitude", "optimism", "joy", "gratitude", "joy"],
    "kauf": [_N, "approval", "optimism"],
    "kauf_intim": ["curiosity", "amusement", "approval"],
    "kauf_schmuck": ["curiosity", "pride", _N],
    "kauf_papier": ["curiosity", "approval", "optimism"],
    "kauf_technik": ["curiosity", _N, "approval"],
    "kauf_essen": ["optimism", _N, "curiosity"],
    "kauf_alkohol": ["approval", "optimism", _N],
    "kauf_party": ["optimism", "amusement", _N],
    "kauf_natur": ["approval", "caring", "curiosity"],
    "kauf_kampf": ["approval", "caring", "optimism"],
    "kauf_schmuggel": [_N, "nervousness", _N],
    "kauf_ressource": [_N, "approval", "optimism"],
    "kauf_werkzeug": ["approval", "optimism", _N],
    "verkauf": ["approval", _N, _N],
    "pleite": [_N, _N, "caring"],
}
for _g in TOTO_ZEILEN:                      # hints: a knowing look
    if _g.startswith("hinweis_"):
        TOTO_GEFUEHL[_g] = "optimism"
FALLBACK_GEFUEHL = "neutral"
