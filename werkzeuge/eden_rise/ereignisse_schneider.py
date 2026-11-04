# -*- coding: utf-8 -*-
"""Danzels Auftraege (Duc 30.10.2026, Wiki systeme/schneider.md): die Uebergaben als Events, die Daten fuer kern/schneider.py.

Duc bringt das Material (sn_<id> datiert), am naechsten Tag kommt beim Tagesbeginn die Szene an der Piazza. Jede Szene endet mit einer
kleinen Wahl: Lohn nehmen (Ruf +1) oder darauf verzichten (Ruf +2, Vertrauen des Kunden)."""
import json, os, sys

from ereignisse_basis import *  # noqa: F401,F403

HIER = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(os.path.dirname(HIER))
sys.path.insert(0, EDEN)
from kern import stimme  # noqa: E402
import ereignisse_outfit_quest as _oq  # noqa: E402

TAGE = (11, 21)                  # Akt 2, dazu Akt 3 als zweites Fenster (nie ueber eine Aktgrenze)
BILD = "village_piazza"
S = {"danzel": "danzel_B", "batu": "batu_standard", "mina": "mina_standard", "petru": "Standard", "anghjulu": "anghjulu_standard",
     "elsa": "Standard", "sandru": "sandru_av", "chiara": "Uniform"}
_TAGS = []


def S_(wer, gesprochen, gefuehl="neutral"):
    """Zeile mit Turbo-Tag: im Text ohne Tag, in stimme_tags.json mit."""
    klar = stimme.vorlesen(stimme.ohne_tags(gesprochen))
    _TAGS.append((wer, klar, gesprochen))
    return Z(wer, klar, gefuehl)


# id, Kunde, Name, Bestelltext, Material, Lohn, Ton, Lage, Zeilen, Text "Lohn nehmen", Text "verzichten"
AUFTRAEGE = [
    ("apron", "batu", "An Apron With Room", "Bà Tư wants an apron that lets her bend to the oven. She has offered to pay partly in soup.",
     {"cloth": 2}, 30, "wholesome",
     "A wide apron lies across Danzel's cutting table. Bà Tư has brought a pot, because she goes nowhere without one.",
     [("batu", "[sniff] Two pockets. Good. One for the ladle, one for the ladle you forget.", "amusement"),
      ("danzel", "I cut it wide at the hip, for the oven. [clear throat] You are the first person who ever asked me for room.", "pride"),
      ("batu", "[chuckle] Eat. You're too thin to sew. You too, First Officer.", "caring")],
     "Takes his pay for the job.", "Takes a bowl of soup instead."),
    ("strap", "mina", "A Strap That Holds", "Mina's mail bag has cut into her shoulder for years. She wants a strap that doesn't.",
     {"leather": 2}, 35, "wholesome",
     "Mina stands on the piazza with the mail bag on her shoulder and moves her arm in a slow circle. Nothing hurts. She doesn't trust it yet.",
     [("mina", "[sigh] I carry everything this village writes. It weighs exactly what you'd think.", "neutral"),
      ("danzel", "Boar hide, doubled, and the buckle sits behind you now. [clear throat] I tested it with a sack of bricks.", "pride"),
      ("mina", "[chuckle] It's good. I don't read them, I just know. You'll get a letter about this strap by Friday.", "amusement")],
     "Takes his pay for the job.", "Tells her the first letter is free."),
    ("jumper", "petru", "The Old Jumper", "Petru has left a paper bag on the counter. Inside is an old navy jumper with no elbows left. He didn't say anything else.",
     {"wool": 2}, 25, "ernst",
     "Petru has come up from the boats for this. He holds the navy jumper in both hands, and neither of them says what it is.",
     [("petru", "Hm. [sigh] My Marie knitted it. The elbows went years ago. I didn't know who to ask.", "sadness"),
      ("danzel", "I didn't make it new. It's the same stitch, and you can see where I was. [clear throat] A repair should be honest.", "neutral"),
      ("petru", "Hm. [sniff] Good.", "gratitude")],
     "Takes the money. Petru insists.", "Shakes his head at the money."),
    ("cassock", "anghjulu", "A Deeper Sleeve", "Don Anghjulu needs his cassock altered. Only the left sleeve. He would prefer not to explain.",
     {"cloth": 3}, 40, "witzig",
     "Don Anghjulu turns in front of the window with his arm held out, as if he were blessing the whole square. Something in his sleeve clicks.",
     [("anghjulu", "[chuckle] A cassock is a serious garment, my son. God sees everything. So the left sleeve must be very deep.", "amusement"),
      ("danzel", "It holds one deck of cards and a small bottle, and it doesn't swing when you bless people. [clear throat] I'm not asking why.", "neutral"),
      ("anghjulu", "[laugh] A tailor who doesn't ask! Cut the cards, First Officer. For luck.", "joy")],
     "Takes the money. All of it, in small coins.", "Cuts the cards instead. Loses gracefully."),
    ("waistcoat", "toto", "A Waistcoat for a Businessman", "Totò wants a waistcoat with red coral buttons and a lining in Napoli blue. He says it's for business.",
     {"cloth": 2, "coral": 1}, 50, "witzig",
     "Totò stands in the middle of the piazza and opens his waistcoat for anyone who will look. Nobody asked.",
     [("toto", "[laugh] Comandante, look at me! Red coral buttons, and inside it's Napoli blue. Nobody can see it. I know it's there.", "joy"),
      ("danzel", "You said no pockets for anything illegal. [clear throat] So I made them very small.", "neutral"),
      ("toto", "[chuckle] Eh. This one understands commerce.", "amusement")],
     "Takes the money, and counts it twice.", "Tells him he can owe you."),
    ("coat", "elsa", "A Coat for Bad Weather", "Lieutenant Ferrandi's patrol coat lets the wind in. Her request is one line long, and it has a reference number.",
     {"wool": 1, "leather": 1}, 45, "witzig",
     "Elsa wears the coat on the hottest square in Corsica, buttoned to the neck, and checks every seam with her thumb.",
     [("elsa", "[clear throat] The lining is warm. The collar stands up in wind. I have no complaints, and I have looked for them.", "approval"),
      ("danzel", "There's a pocket on the inside. It fits a paperback. [clear throat] If somebody on patrol owned a paperback.", "nervousness"),
      ("elsa", "[sniff] Noted. Totò remains uninformed.", "amusement")],
     "Takes the money, against a receipt.", "Tells her the coast guard can owe the village."),
    ("shirt", "sandru", "A Plain Shirt", "Sandru came in after closing and asked for one shirt. Plain, and not for work. He paid for the cloth in advance and left quickly.",
     {"cloth": 2}, 30, "ernst",
     "Sandru has left the shop for an hour. He has never done that before. He looks at the shirt and not at anybody.",
     [("sandru", "[clear throat] There's no place for the name badge.", "neutral"),
      ("danzel", "No. [sigh] You said you wanted one shirt that isn't for work.", "caring"),
      ("sandru", "[sniff] Yes. Thank you. It's a good shirt.", "gratitude")],
     "Takes the money.", "Says the cloth was already paid for."),
    ("hat", "casanova", "A Hat for the Mayor", "Madame Casanova requires a hat. It must be seen from the harbour. Danzel has asked you for gull feathers, and he is very calm about it.",
     {"feather": 2, "cloth": 1}, 70, "witzig",
     "Madame Casanova takes the hat from Danzel with two fingers, and the piazza goes quiet. She puts it on. It can certainly be seen from the harbour.",
     [("casanova", "[clear throat] Gull feathers. On the Mayor of Cala d'Orsu. It is either very bold or very stupid.", "disapproval"),
      ("danzel", "In Paris it would be stupid. [chuckle] Here the gulls will think you're one of them, and at last they'll show some respect.", "pride"),
      ("casanova", "[chuckle] I'll take it. And you'll dress the whole Festa, young man. The budget is small. The expectations aren't.", "amusement")],
     "Takes the money from the town hall.", "Tells her to put it towards the Festa."),
]

MASSSTUECKE = [{"id": "dress_whites", "frau": "chiara", "label": "Dress Whites", "geld": 110, "material": {"wool": 3}, "items": {"aquamarin": 1},
                "text": "White wool, washed nine times, with buttons cut from one pale blue stone. The tailor left both cuffs plain. He says there is room on each for four stripes."}] + _oq.MASSSTUECKE


def _beide_akte(e):
    e["wann"]["akt2"] = list(AKT3)
    return e


def _uebergabe(a):
    aid, kunde, label, _text, _mat, lohn, ton, lage, zeilen, nehmen, lassen = a
    bed = {"alle": [{"flag_seit": ["sn_" + aid, 1]}]}
    fertig = F("sn_%s_fertig" % aid)
    folgen_extra = [F("danzel_festa_auftrag")] if aid == "hat" else []
    e = E("sn_" + aid, "gag1", ton, label, WANN(TAGE, ["tag"], bed=bed, pflicht=True, holt_leute=True), BILD,
          {"handelnd": "danzel", "betroffen": [{"id": kunde, "ton": "?", "was": ""}]}, lage,
          [S_(w, t, g) for w, t, g in zeilen],
          [O(nehmen, [G(lohn), W("ruf", 1), V("danzel", 4), fertig] + folgen_extra),
           O(lassen, [W("ruf", 2), V(kunde, 4), V("danzel", 4), fertig] + folgen_extra)],
          {p: S[p] for p in ("danzel", kunde) if p in S})
    return _beide_akte(e)


EVENTS = [_uebergabe(a) for a in AUFTRAEGE] + [
    _beide_akte(E("sn_dress_whites", "gag1", "frech", "Dress Whites",
      WANN(TAGE, ["tag"], bed={"alle": [{"flag_seit": ["sn_dress_whites", 1]}]}, pflicht=True, holt_leute=True), BILD,
      {"handelnd": "danzel", "betroffen": [{"id": "chiara", "ton": "?", "was": ""}]},
      "Chiara stands at Danzel's mirror in white. Two rows of pale blue stone run down the jacket. She has been looking at the cuffs for some time. There is nothing on them.",
      [S_("chiara", "[clear throat] You forgot the stripes.", "annoyance"),
       S_("danzel", "I forgot nothing. [chuckle] A tailor only leaves the room. The stripes you sew on yourself, the day you have earned them.", "amusement"),
       S_("chiara", "[sigh] Who told you? No. Don't answer that. Nine. And if you tell my brother, it's a two.", "desire")],
      [O("Says the stripes will look good there.", [B("chiara", 8), V("chiara", 6), F("sn_dress_whites_fertig")]),
       O("Says nothing, and looks at the cuffs with her.", [V("chiara", 8), V("danzel", 4), F("sn_dress_whites_fertig")])],
      {"danzel": S["danzel"], "chiara": S["chiara"]})),
]
SET_FREI = {"chiara": [{"flag": "sn_dress_whites_fertig", "set": "Dress Whites"}]}
DATEN = {"auftraege": [{"id": a[0], "kunde": a[1], "label": a[2], "text": a[3], "material": a[4], "lohn": a[5]} for a in AUFTRAEGE],
         "massstuecke": MASSSTUECKE}


def tags_schreiben():
    pfad = os.path.join(EDEN, "module", "eden_rise", "stimme_tags.json")
    d = json.load(open(pfad, encoding="utf-8"))
    neu = [{"wer": w, "text": t, "gesprochen": g, "quelle": "schneider"} for w, t, g in _TAGS]
    texte = {z["text"] for z in neu}
    d["zeilen"] = [z for z in d["zeilen"] if z.get("quelle") != "schneider" and z["text"] not in texte] + neu
    json.dump(d, open(pfad, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return len(neu)
