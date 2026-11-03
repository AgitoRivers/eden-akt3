# -*- coding: utf-8 -*-
"""Laeden fuer eden_rise (17.10.2026) mit festen, vorab vertonten Saetzen - wie Totos Spind (Haendler-Saetze in modul_eden_rise.py).

  toto   Totos Spind an Bord (Saetze aus kern/handel.py, hier nur referenziert)
  alva   Alvas Bar an Land - verkauft seit 17.10. alles aus dem Dorf (der Dorfladen entfaellt), Diesel hoechstens 1/Tag
  lola   Lolas Kombuese an Bord - Snacks und Desserts (1 Essen am Tag), Gras-Snacks ab Vertrauen 3/4
  megan  Eden-Shop per Videoanruf - Ersatzteile und Eden-Ware, -10 % je Vertrauensstufe ab 3

Je Laden: Buehne (Hintergrund + Figur), Gruesse nach Vertrauen, dann Anlass-Gruppen. Gefuehl je Gruppe fuer das Sprite.
Aufruf: python laeden_eden_rise.py -> module\\eden_rise\\laeden.json
"""
import json, os, sys

EDEN = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # werkzeuge\eden_rise -> Eden
ZIEL = os.path.join(EDEN, "module", "eden_rise", "laeden.json")

LAEDEN = {
    "alva": {
        "name": "Alva's Bar", "wer": "alva", "nur_an_land": True, "hintergrund": "corsican_village_bar.png", "set": "alva_standard",
        "text": "The only bar in Cala d'Orsu, and since the quarrel over the village shop the only shop too. Alva sells "
                "everything, diesel under the counter included.",
        "gruss_stufen": {"gruss_fremd": [0, 1], "gruss_freundin": [2, 3], "gruss_naehe": [4, 5]},
        "zeilen": {
            "gruss_fremd": [
                "Benvenutu, o figliolu. Bar, bakery, hardware shop and post office. If I don't have it, it doesn't exist.",
                "The yacht man. Everybody talks about you. Sit, buy something, give them something new to talk about.",
                "Prices are on the board. The board lies a little. Ask nicely and it lies less.",
            ],
            "gruss_freundin": [
                "There he is. I put your glass aside before you came in. Don't ask how I knew.",
                "My favourite customer. Don't tell the fishermen, they think it's them.",
                "Ah, you again. Good. The day was getting boring.",
            ],
            "gruss_naehe": [
                "Close the door behind you, o figliolu. Slowly. I like watching you do it.",
                "For you, everything is cheaper. Almost everything. Some things you pay for differently.",
                "I was thinking about you just now. Then you walked in. The universe owes me money.",
            ],
            "kauf": [
                "Bravu. Good choice. I'd have chosen it too.",
                "On the tab or cash? Cash. Good boy.",
                "Take it. And come back tomorrow, I'll have something you didn't know you wanted.",
            ],
            "diesel": [
                "One canister, under the counter. Only one a day, I'm a bar, not a refinery.",
                "Diesel again? You'll smell like a fisherman. I don't mind fishermen.",
            ],
            "diesel_leer": [
                "No more diesel today. Come back tomorrow. Or come back tonight, without a reason.",
            ],
            "pleite": [
                "No money? Then sing for it. No? Then come back richer, o figliolu.",
                "Empty pockets and that face. Unfair. Still no.",
            ],
        },
        "gefuehl": {"gruss": "joy", "gruss_naehe": "desire", "kauf": "amusement", "diesel": "approval", "diesel_leer": "amusement",
                    "pleite": "disappointment"},
    },
    "lola": {
        "name": "Lola's Galley", "wer": "lola", "nur_an_land": False, "hintergrund": "yacht_galley.png", "set": "Galley",
        "text": "The galley smells of butter, sugar and something nobody talks about. One meal a day: eat it yourself or "
                "give it away.",
        "gruss_stufen": {"gruss_fremd": [0, 1], "gruss_freundin": [2, 3], "gruss_naehe": [4, 5]},
        "zeilen": {
            "gruss_fremd": [
                "Boss! Welcome to the galley. Everything here is made with love. And butter. Mostly butter.",
                "Hungry? You look hungry. You look like a man who forgot breakfast. Sit.",
                "Today's menu is whatever survived the fridge. Trust me, it's good.",
            ],
            "gruss_freundin": [
                "There's my favourite taster! I made something weird today. You're going to love it. Or die. Probably love it.",
                "Boss, my boss. I saved you the corner piece. The corner piece is the best piece.",
                "You came back! The galley missed you. I missed you. The galley mostly.",
            ],
            "gruss_naehe": [
                "Hey, you. Come here. Taste this. From the spoon. From my spoon.",
                "I baked something special. It's for you. It's also a little bit for me, if you know what I mean.",
                "Every time you walk in, I burn something. That's a compliment, babe.",
            ],
            "kauf": [
                "Enjoy! Eat it slowly. Or give it to someone you like. Food is love, that's science.",
                "Good choice, mate. That one has a secret ingredient. The secret is more sugar.",
                "Wrapped in a napkin with a little heart on it. Don't tell Chiara I used the good napkins.",
            ],
            "satt": [
                "No, no, you already ate today. One a day, Boss. Otherwise you'll fall asleep in the generator room.",
                "You're full. I can see it. Come back tomorrow, I'll make it worth your while.",
            ],
            "special": [
                "Today's special! Thirty percent off, because I made too much and the seagull is watching me.",
            ],
            "gras": [
                "These ones are… special special. Don't eat them before a meeting. Or a coast guard visit.",
                "Shh. Under the tea towel. For grown-ups with nothing to do tomorrow morning.",
            ],
            "pleite": [
                "No money? That's fine. I'll put it on your tab. Your tab is a little drawing of you on the fridge.",
            ],
        },
        "gefuehl": {"gruss": "joy", "gruss_naehe": "desire", "kauf": "amusement", "satt": "caring", "special": "excitement",
                    "gras": "amusement", "pleite": "caring"},
    },
    "megan": {
        "name": "Eden Shop", "wer": "megan", "nur_an_land": False, "hintergrund": "eden_hq_megan_office.png", "set": "Boardroom",
        "anruf": True,
        "text": "Spare parts and Eden goods, ordered by video call from the fleet director and delivered with the next "
                "supply boat. From trust level 3 with Megan there is a discount.",
        "gruss_stufen": {"gruss_kalt": [0, 2], "gruss_warm": [3, 5]},
        "zeilen": {
            "gruss_kalt": [
                "First Officer. You're calling the Eden shop. Which means you want something. Be quick, I bill by the minute.",
                "Spare parts, merchandise, miracles. Two of those are in stock.",
                "Order something sensible, and I'll pretend you're a responsible man.",
            ],
            "gruss_warm": [
                "Ah, my favourite disaster. What can I sell you today? I'm in a generous mood. It won't last.",
                "You again. Good. Nobody else calls me just to buy screws. It's almost romantic.",
                "For you, a discount. Don't tell the other captains. They'd cry. I'd enjoy it.",
            ],
            "kauf": [
                "Ordered. It arrives with the next supply boat. Try not to break it before then.",
                "Excellent purchase. I'll put it on the Group's account and your conscience.",
                "Done. You see? We can do business without anyone crying.",
            ],
            "rabatt": [
                "Ten percent off. Per level of my affection. You're doing better than most.",
            ],
            "pleite": [
                "Insufficient funds. How very human. Come back when you're liquid, First Officer.",
                "No money. I'd lend you some, but I'm not that kind of villain. Yet.",
            ],
        },
        "gefuehl": {"gruss": "neutral", "gruss_warm": "amusement", "kauf": "pride", "rabatt": "amusement", "pleite": "disapproval"},
    },
    # Rosis Werkstatt (25.10.2026, Duc): ein Ort wie ein Laden, aber ohne Waren: umziehen (Waffen, Jacken), Chips, Verbessern.
    # Kein Gespraech, keine Szene - nur Gruss und Auswahlfelder. "zu" = Werkstatt noch kaputt (der Spind ist offen).
    "rosi": {
        "name": "Rosi's Workshop", "wer": "rosi", "nur_an_land": False, "werkstatt": True,
        "hintergrund": "eden_rise_workshop.png", "set": "Engine Room",
        "text": "Rosi's workshop on the lower deck: chips fitted, weapons and jackets upgraded.",
        "gruss_stufen": {"gruss_fremd": [0, 1], "gruss_freundin": [2, 3], "gruss_naehe": [4, 5]},
        "zeilen": {
            "gruss_fremd": [
                "If you're here to look at the motor, don't touch anything. If you're here to fix something, welcome.",
                "Workshop rules: you break it, you carry it. Now, what are we building?",
                "Your plan is probably bad. Show me the part and I'll tell you how bad.",
            ],
            "gruss_freundin": [
                "Officer. Good. I was starting to talk to the drill again.",
                "Put it on the bench. Gently. It's the only bench I trust.",
                "You've got that look. Either you broke something or you have an idea. Both are fine.",
            ],
            "gruss_naehe": [
                "You came back. I kept the good stool for you. Don't make a thing of it.",
                "Sit. Hold this. No, like that. ...Yes. You're not bad at this.",
                "Everything on this bench has a name. You're the first person who asked what they are.",
            ],
            "zu": [
                "The workshop is still a mess. Give me a few more days. The locker's open, though.",
                "I can't work in here yet. I can hand you your gear, nothing more.",
            ],
            "kauf": [
                "Put it on the bench. You'll hear from me in the morning.",
                "Got it. Don't poke it while I'm gone.",
            ],
        },
        "gefuehl": {"gruss": "joy", "gruss_naehe": "amusement", "zu": "annoyance", "kauf": "pride"},
    },
    "toto": {"name": "Totò's Locker", "wer": "toto", "zeilen_aus": "modul.json laeden.toto.haendler_zeilen", "hintergrund": "eden_rise_toto_spind.png"},
}


def pruefen():
    fehler = []
    for lid, l in LAEDEN.items():
        for gruppe, liste in (l.get("zeilen") or {}).items():
            for s in liste:
                if '"' in s:
                    fehler.append("%s.%s: doppeltes Anfuehrungszeichen" % (lid, gruppe))
        for g in (l.get("gruss_stufen") or {}):
            if g not in l["zeilen"]:
                fehler.append("%s: Grussgruppe %s fehlt" % (lid, g))
    return fehler


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    f = pruefen()
    for x in f:
        print("FEHLER", x)
    if f:
        sys.exit(1)
    json.dump({"_hinweis": "Gebaut aus werkzeuge\\eden_rise\\laeden_eden_rise.py - dort aendern.", "laeden": LAEDEN},
              open(ZIEL, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    n = sum(len(v) for l in LAEDEN.values() for v in (l.get("zeilen") or {}).values())
    print("geschrieben:", ZIEL, "-", n, "Saetze")
