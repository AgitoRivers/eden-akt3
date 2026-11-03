# -*- coding: utf-8 -*-
"""Tag 0 · Der Hangar in Antibes (24.10.2026, docs/wiki/welt/drehbuch_tag0.md, E-017 bis E-021).

Prolog am Morgen von Tag 1, nach dem Cold Open: komplett geskriptet, kein Sprachmodell, alle Zeilen vertont.
Jede Begegnung ist ein Pflicht-Event mit WANN(prolog=True): Prolog-Events laufen auch an Tag 1 und in Phasen ohne
Szene und schliessen direkt aneinander an (kern/ereignisse.pflicht_ziehen, eden.py). Reihenfolge = Reihenfolge hier.

Chips je erster Begegnung (E-018): V Vertrauen +1 Stufe · B Begehren +1 Stufe (Romanzen) bzw. H Humor +Rueckhalt ·
- nichts · F Fettnaepfchen (Vertrauen -1 Stufe, wo eine da ist). Jede Wahl setzt tag0_<id>_<chip> fuer spaetere
Rueckgriffe. Megan: tag0_megan_herzlich/frech/flirt/foermlich -> Anhoerung (kern/anhoerung.py), Flirt zusaetzlich
megan_funke (versteckte Romanze)."""
from ereignisse_basis import *  # noqa: F401,F403

ORT = "hangar_antibes"
STUFE = 8                                    # Punkte je Vertrauens-/Begehrensstufe (kern/zustand.PUNKTE_JE_STUFE)


def P1(handelnd, *betroffen):
    return {"handelnd": handelnd, "betroffen": [{"id": b[0], "ton": b[1], "was": b[2]} for b in betroffen]}


def W0(bed=None):
    return WANN((1, 1), ["tag"], bed=bed, pflicht=True, prolog=True)


def chips(pid, v, b, n, f, romanze=True):
    """Vier Chips: (Duc-Satz, Antwortzeile) je Art. b ist bei Romanzen Begehren, sonst Humor (Rueckhalt)."""
    flag = lambda art: F("tag0_%s_%s" % (pid, art))
    return [O(v[0], [V(pid, STUFE), flag("v")], zeile=v[1]),
            O(b[0], [B(pid, STUFE) if romanze else R(5), flag("b" if romanze else "h")], zeile=b[1]),
            O(n[0], [flag("n")], zeile=n[1]),
            O(f[0], [V(pid, -STUFE), flag("f")], zeile=f[1])]


EVENTS = [
    # ------------------------------------------------------------------ Szene 1 · Die Limousine
    E("t0_limousine", "gag1", "witzig", "Antibes, 06:10", W0(), ORT,
      P1("maxwell", ("toto", "+", "stares"), ("lea", "+", "wants a ride"), ("rosi", "-", "rolls her eyes"),
         ("chiara", "-", "does the maths"), ("lola", "-", "raises an eyebrow")),
      "The hangar doors stand open. Pallets, low sun, and outside the white bow of the Eden Rise. A black stretch "
      "limousine rolls into the hall, and the loading stops.",
      [Z("maxwell", "Number One has arrived! Mr. Maximum salutes the limousine!", "excitement"),
       Z("toto", "Madonna, six windows. Comandante, I like you already. I've already put money on you.", "amusement"),
       Z("lea", "Is that a real limo? Can I sit in it? Not now, obviously. Later? Please?", "excitement"),
       Z("sophia", "That's the founder of Eden Consulting, darlings. Be charming. Not you, Lea. Me.", "amusement"),
       Z("rosi", "Great. A consultant, and he came in a hearse.", "annoyance"),
       Z("chiara", "Six windows. We're thirteen people with no budget for napkins, and he has six windows.", "disapproval"),
       Z("lola", "Mate. Who turns up to a boat in a limo?", "curiosity")],
      [O("“Morning, everyone. I'll carry my own bag.”", [R(5), F("tag0_auftritt_bodenstaendig")],
         zeile=Z("chiara", "…Noted. That's a first.", "curiosity")),
       O("“The CEO insisted on the car. I'd have taken the bus.”", [R(3), F("tag0_auftritt_humor")],
         zeile=Z("lola", "The bus. Sure you would, Boss. Alright, I like you a little.", "amusement")),
       O("“Hi. I'm Duc.”", [F("tag0_auftritt_neutral")]),
       O("“Careful with the bags, they're Louis Vuitton.”", [R(-5), F("tag0_auftritt_snob")],
         zeile=Z("rosi", "See? I told you. A hearse.", "disapproval"))]),

    # ------------------------------------------------------------------ Szene 2 · Mac
    E("t0_megan", "gag1", "wholesome", "Mac", W0(), ORT,
      P1("megan", ("chiara", "?", "watches")),
      "A woman with a clipboard walks out of the glare. Ten years, and she still walks the same way.",
      [Z("megan", "Duc.", "neutral")],
      [O("“It's good to see you, Meg.”", [V("megan", STUFE), F("tag0_megan_herzlich")],
         zeile=Z("megan", "…It's Megan now. Fleet Director Megan.", "joy")),
       O("“Fleet Director? Did you yell your way to the top?”", [F("tag0_megan_frech")],
         zeile=Z("megan", "I did. And I'll yell you right back down if I have to.", "amusement")),
       O("“And you still look so gorgeous, Mac. It feels like time didn't pass.”",
         [F("tag0_megan_flirt"), F("megan_funke")],
         zeile=Z("megan", "…Time passed, Duc. The gangway's that way.", "embarrassment")),
       O("“Ms McAllister.”", [F("tag0_megan_foermlich")],
         zeile=Z("megan", "First Officer. Good. Let's keep it like that.", "approval"))],
      sets={"megan": "Boardroom"}),

    # ------------------------------------------------------------------ Szene 3 · Rundgang (Pflicht)
    E("t0_holm", "gag1", "ernst", "The Captain", W0(), ORT,
      P1("holm", ("megan", "?", "introduces her")),
      "Megan leads you to the gangway. At the top stands a woman with a mug of cold coffee, looking at you the way "
      "she would look at the weather. For a second her hand goes to her side. Then back to the coffee.",
      [Z("megan", "Captain Marit Holm. Eleven seasons on this boat. She doesn't like consultants. She doesn't like "
                  "anyone, really.", "neutral"),
       Z("holm", "So you're the CEO's consultant. Can you tie a bowline?", "neutral")],
      chips("holm",
            ("Ties a bowline one-handed. “Behind my back, if you like.”", Z("holm", "…Hm. Takk. Don't let it go to your "
                                                                                         "head.", "approval")),
            ("“I can tie a tie. Does that count?”", Z("holm", "On my bridge, no. At the party, maybe.", "amusement")),
            ("“I have my Yachtmaster. It's in the papers.”", Z("holm", "Papers don't float, Frankfurt.", "neutral")),
            ("“Can't the crew do the knots?”", Z("holm", "The crew does what I do. My coffee's cold, and so is this "
                                                         "conversation.", "disapproval")),
            romanze=False),
      sets={"megan": "Boardroom"}),

    E("t0_chiara", "gag1", "wholesome", "The Chief Stew", W0(), ORT,
      P1("chiara", ("megan", "?", "checks on her")),
      "At the foot of the gangway: a uniform without a single crease, a clipboard, and a look that finds dust.",
      [Z("megan", "Chiara Sonnberg, Chief Stew. The best in the fleet. Chiara, have you eaten?", "caring"),
       Z("chiara", "Yes.", "neutral"),
       Z("megan", "Liar.", "amusement"),
       Z("chiara", "Welcome aboard, First Officer. Your cabin is ready. It used to be mine.", "neutral")],
      chips("chiara",
            ("“Then you know what's wrong with it. What would you change?”", Z("chiara", "…The shower, and that bell. Thank you "
                                                                                         "for asking. Nobody ever asks.", "surprise")),
            ("“Then I'll take good care of it. And of the one who had it before.”", Z("chiara", "…That was almost charming. Don't do it on duty.", "embarrassment")),
            ("“Thank you.”", Z("chiara", "You're welcome. Breakfast is at seven, and I mean seven.", "neutral")),
            ("“Great. Is there a bigger one?”", Z("chiara", "No, First Officer. There's a smaller one. Mine. As of "
                                                            "now.", "disapproval"))),
      sets={"megan": "Boardroom"}),

    E("t0_rosi", "gag1", "witzig", "The Engineer", W0(), ORT,
      P1("rosi", ("megan", "?", "warns you")),
      "Two legs in work trousers stick out from under the stern. Next to them, a small diesel generator hums away "
      "happily.",
      [Z("megan", "Rosi Scuderi, our ETO. Brilliant. She bites.", "neutral"),
       Z("rosi", "If you're here to look at the motor, don't touch anything.", "annoyance")],
      chips("rosi",
            ("“It's not a motor. It's an inverter.”", Z("rosi", "…Okay. Fine. You can touch one thing.", "surprise")),
            ("“I'm here to look at the engineer.”", Z("rosi", "Wow, that was cheesy. Here, hold this rag, and don't "
                                                              "drop it.", "amusement")),
            ("“I won't.”", Z("rosi", "Good. Then we'll get along.", "neutral")),
            ("“Can't we just call a mechanic?”", Z("rosi", "I AM the mechanic, Officer!", "anger"))),
      sets={"megan": "Boardroom"}),

    E("t0_maxwell", "gag1", "witzig", "Mr. Maximum", W0(), ORT,
      P1("maxwell", ("megan", "?", "sighs")),
      "A man lifts an entire pallet over his head. Then a helicopter thunders over the hangar roof, and he vanishes "
      "behind the pallet in a flash.",
      [Z("megan", "Maxwell, steward and trainer. Don't challenge him to anything.", "neutral"),
       Z("maxwell", "Number One! Mr. Maximum has heard of you! Do you lift?", "excitement"),
       Z("maxwell", "Mr. Maximum was just checking the pallet. The pallet is fine. Everything is fine.", "nervousness")],
      chips("maxwell",
            ("“Show me. Tomorrow, six thirty.”", Z("maxwell", "A MAN OF HONOUR! Six thirty! Mr. Maximum will cry, but quietly.", "joy")),
            ("“Only my expectations.”", Z("maxwell", "Ha! One push-up for that joke, brother!", "amusement")),
            ("“A little.”", Z("maxwell", "A little is the beginning of a lot, brother!", "optimism")),
            ("“I have a personal trainer in Frankfurt.”", Z("maxwell", "…Mr. Maximum will be very professional now.", "disappointment")),
            romanze=False),
      sets={"megan": "Boardroom"}),

    E("t0_toto", "gag1", "witzig", "The Bosun", W0(), ORT,
      P1("toto", ("megan", "?", "rolls her eyes")),
      "A man with a gold-tooth grin is carrying a small crate himself, although there are pallets everywhere.",
      [Z("megan", "Totò, our bosun. If something goes missing, it was Totò. If it comes back, that was also Totò.", "neutral"),
       Z("toto", "Comandante! Welcome, welcome! Don't mind this. Potatoes. Very small potatoes.", "nervousness")],
      [O("“Let me help you carry that.”", [V("toto", STUFE), F("tag0_toto_v"), F("tag0_lieferzettel")],
         zeile=Z("toto", "No, no! Heavy potatoes. I mean light. Very light. I've got it.", "nervousness")),
       O("“What are the odds I survive the week?”", [R(5), F("tag0_toto_h")],
         zeile=Z("toto", "Ten to one. Against. But I love a long shot, Comandante.", "amusement")),
       O("“Morning.”", [F("tag0_toto_n")], zeile=Z("toto", "Buongiorno, Comandante!", "joy")),
       O("“Shouldn't those potatoes be inspected?”", [V("toto", -STUFE), F("tag0_toto_f")],
         zeile=Z("toto", "Inspected? By who? Elsa?! …I mean, yes. Of course. Later.", "fear"))],
      sets={"megan": "Boardroom"}),

    E("t0_lola", "gag1", "wholesome", "The Cook", W0(), ORT,
      P1("lola", ("megan", "?", "warns you")),
      "In a corner of the hangar, a bamboo steamer puffs away on a camping stove. She's barefoot, with flour on her "
      "cheek.",
      [Z("megan", "Lola, our cook. Don't ask what's in the oregano.", "neutral"),
       Z("lola", "Alright, Boss. You look like a bloke who eats with tweezers. Go on, prove me wrong.", "curiosity")],
      chips("lola",
            ("“One day I'll cook for you. Pho, my mother's recipe.”", Z("lola", "…A man who cooks? Okay. Now I'm "
                                                                             "listening.", "curiosity")),
            ("“That's the best thing I've had in years. Who taught you this?”", Z("lola", "Nobody! That's the whole point, mate.", "joy")),
            ("“Maybe later.”", Z("lola", "Later is how people starve, Boss.", "amusement")),
            ("“Is it gluten-free?”", Z("lola", "It's free. That's all it is, mate.", "disapproval"))),
      sets={"megan": "Boardroom", "lola": "Galley"}),

    # ------------------------------------------------------------------ Szene 3 · Wahl (zwei von vier)
    E("t0_wahl", "gag1", "wholesome", "Where to First?", W0(), ORT,
      P1("megan", ("lea", "+", "waves"), ("jana", "?", "hides a crate"), ("siri", "?", "is being filmed"),
         ("yamamoto", "?", "takes photos")),
      "Megan checks her watch. The tide doesn't wait.",
      [Z("megan", "Where to first? You've got five minutes.", "neutral")],
      [O("Visits the Moore sisters at the dive tanks", [F("tag0_station_moore")]),
       O("Visits Jana, the new deckhand", [F("tag0_station_jana")]),
       O("Visits Siri and Yasin, the guests", [F("tag0_station_siri")]),
       O("Visits Yamamoto-san, the guest in the owner's suite", [F("tag0_station_yamamoto")])],
      sets={"megan": "Boardroom"}),
]

# Zweite Wahl: je nach erster Station die drei uebrigen (eine Variante je erster Wahl)
STATIONEN = [("moore", "Visits the Moore sisters at the dive tanks"), ("jana", "Visits Jana, the new deckhand"), ("siri", "Visits Siri and Yasin, the guests"),
             ("yamamoto", "Visits Yamamoto-san, the guest in the owner's suite")]
for erste, _ in STATIONEN:
    EVENTS.append(E("t0_wahl2_%s" % erste, "gag1", "wholesome", "And Then?",
                    W0({"alle": [{"flag": "tag0_station_" + erste}, {"nicht": {"flag": "tag0_wahl2"}}]}), ORT,
                    P1("megan", ("chiara", "?", "waits at the gangway")),
                    "Megan taps her clipboard. One more stop.",
                    [Z("megan", "One more, and then we sail.", "neutral")],
                    [O(text, [F("tag0_station_" + sid), F("tag0_wahl2")]) for sid, text in STATIONEN if sid != erste]
                    + [O("Goes back to the gangway", [F("tag0_station_keine"), F("tag0_wahl2")])],
                    sets={"megan": "Boardroom"}))

EVENTS += [
    E("t0_lea", "gag1", "wholesome", "Lea", W0({"flag": "tag0_station_moore"}), ORT,
      P1("lea", ("sophia", "?", "watches"), ("megan", "?", "introduces them")),
      "Between the dive tanks stand two sisters, one with a notebook, one with wet hair.",
      [Z("megan", "The Moore sisters. One plans everything, the other plans nothing.", "neutral"),
       Z("lea", "Did you see the sea last night? It glowed. I swear it glowed, proper glowing!", "excitement")],
      chips("lea",
            ("“Bioluminescence. Noctiluca, probably.”", Z("lea", "You know Noctiluca? YOU KNOW NOCTILUCA?", "excitement")),
            ("“Show me tonight.”", Z("lea", "It's a date! A science date. Obviously.", "joy")),
            ("“I was in Frankfurt.”", Z("lea", "Frankfurt doesn't glow, though, does it?", "neutral")),
            ("“Probably pollution.”", Z("sophia", "And that, darling, is how you lose her.", "disapproval"))),
      sets={"megan": "Boardroom"}),
    E("t0_sophia", "gag1", "wholesome", "Sophia", W0({"flag": "tag0_station_moore"}), ORT,
      P1("sophia", ("lea", "?", "grins")),
      "Sophia offers you her hand as if she had rehearsed this moment. Maybe she has.",
      [Z("sophia", "Sophia Moore. I read your interview, darling. You said sustainability is a question of "
                   "hospitality.", "neutral")],
      chips("sophia",
            ("“Then you're the expert on board. What would you change?”", Z("sophia", "…Nobody ever asks the concierge. "
                                                                                      "Thank you.", "surprise")),
            ("“I wrote that for exactly one reader. Didn't know it was you.”", Z("sophia", "Nice line. I might steal it.", "amusement")),
            ("“Did I say that?”", Z("sophia", "You did. Page three, second column.", "neutral")),
            ("“I don't usually give interviews to staff.”", Z("sophia", "Of course not. How silly of me.", "neutral")))),
    E("t0_jana", "gag1", "witzig", "Jana", W0({"flag": "tag0_station_jana"}), ORT,
      P1("jana", ("megan", "?", "introduces her")),
      "A young deckhand walks backwards into a door and apologises to it. Next to her stands a crate. The crate "
      "meows.",
      [Z("megan", "Jana, first season. She apologises to furniture.", "neutral"),
       Z("jana", "Sorry, sorry – oh! Sorry, Sir. Not you. I meant the door.", "embarrassment")],
      chips("jana",
            ("“I didn't hear anything.”", Z("jana", "…Thank you, Sir. Really.", "gratitude")),
            ("“Your potatoes are meowing.”", Z("jana", "Very small potatoes! Like Totò's!", "amusement")),
            ("“Morning.”", Z("jana", "Morning, Sir! Servus!", "joy")),
            ("“Megan, there's a cat in that box.”", Z("megan", "There is no cat, First Officer.", "neutral")),
            romanze=False),
      sets={"megan": "Boardroom"}),
    E("t0_siri", "gag1", "frech", "Siri and Yasin", W0({"flag": "tag0_station_siri"}), ORT,
      P1("siri", ("yasin", "+", "films"), ("megan", "?", "smiles through it")),
      "A convertible, two pairs of sunglasses, and a camera that's already rolling before anyone says hello.",
      [Z("megan", "Our guests. Smile, please. She has nearly three million followers, and he has opinions.", "neutral"),
       Z("yasin", "The sustainability guy! Say something green, my man!", "excitement"),
       Z("siri", "Hi. Sorry – sorry about him.", "embarrassment")],
      chips("siri",
            ("Holds a hand over the lens. “Not before coffee, Yasin.”", Z("siri", "…Thank you. Really.", "relief")),
            ("“Something green? Your eyes.”", Z("siri", "…They're blue, actually. But nice try.", "amusement")),
            ("Waves into the camera.", Z("yasin", "Content! That's content, bro!", "joy")),
            ("“Tag Eden Consulting, please.”", Z("siri", "Sure! Smile for the camera!", "neutral"))),
      sets={"megan": "Boardroom"}),
    E("t0_yamamoto", "gag1", "witzig", "Yamamoto-san", W0({"flag": "tag0_station_yamamoto"}), ORT,
      P1("yamamoto", ("megan", "?", "introduces him")),
      "A small gentleman in a Hawaiian shirt bows deeply. Then his camera clicks. He's photographing a seagull. Or "
      "not.",
      [Z("megan", "Mr. Yamamoto. Owner's suite, four weeks. He tips like a king.", "neutral"),
       Z("yamamoto", "Officer-san. Very honoured.", "neutral")],
      chips("yamamoto",
            ("Bows, exactly deep enough. “Yamamoto-san. The honour is mine.”", Z("yamamoto", "…You know the bow. Very interesting.", "admiration")),
            ("“Bird photography?”", Z("yamamoto", "Very rare bird. So sorry.", "embarrassment")),
            ("“Welcome aboard.”", Z("yamamoto", "Thank you. Please take care of me.", "neutral")),
            ("“Can someone take his luggage?”", Z("yamamoto", "I carry my own luggage. Thirty years, Officer-san.", "disapproval")),
            romanze=False),
      sets={"megan": "Boardroom"}),
]

# ------------------------------------------------------------------ Szene 4 · Abschied (Zusatz je Megan-Chip)
ABSCHIED = {
    "herzlich": ("She touches your arm, just briefly.", "See you at the end of the season, Duc. Don't sink my boat.", "joy"),
    "frech": ("She gives you a crooked grin.", "See you at the end of the season. Don't sink my boat, and don't call me.", "amusement"),
    "flirt": ("She hesitates at the helicopter door. Very quietly:",
              "Mac. Nobody's called me that in ten years. Don't sink my boat, Duc.", "love"),
    "foermlich": ("A handshake. Firm. Short.", "First Officer. Don't sink my boat.", "neutral"),
}
for chip, (lage, satz, gef) in ABSCHIED.items():
    EVENTS.append(E("t0_abschied_%s" % chip, "gag1", "wholesome", "Don't Sink My Boat",
                    W0({"flag": "tag0_megan_" + chip}), ORT,
                    P1("megan", ("holm", "?", "salutes")),
                    "The helicopter waits on the apron. Maxwell has disappeared. " + lage,
                    [Z("megan", satz, gef)],
                    [O("Watches her go", [F("tag0_fertig")]),
                     O("Heads for the gangway", [F("tag0_fertig")])],
                    sets={"megan": "Boardroom"}))
