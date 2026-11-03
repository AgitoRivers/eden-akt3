# -*- coding: utf-8 -*-
"""Die Brueder Ricci - Taschendiebe am Hafen (Duc + Brain Trust 29.10.2026). Eingebunden von kaempfe_eden_rise.py.

Zufallskampf beim Besuch von Alvas Bar oder Petrus Werkstatt (kern/taschendieb.py): 5 % je Besuch, ab Tag 3, hoechstens
alle 2 Tage. Es baut sich auf - jede Begegnung ist die naechste Stufe, egal wie sie ausging:
  1  Fabbiu ODER Santu allein   Level Duc -1, laestig        klauen 1 Verbrauchsgegenstand (ohne einen: 20 EUR)
  2  The Ricci Brothers          Level Duc,    gefaehrlich    klauen 2 (40 EUR)
  3  The Ricci Gang (+ Matte)    Level Duc +1, gefaehrlich    klauen 3 (60 EUR)
Danach: Elsas Nebenquest (folgt). Sie sticheln vertont ("sprueche": start / runde / gewinnt / verliert, Schluessel
kampf.<gegner>.<art>.<n>, kern/kampf._spruch). Ein Ricci gehoert besiegt: niemand flieht (kein flee_at).
Sprites: Thief (Fabbiu, Brille) und ThiefArab (Santu, Maske); Gruppenbilder fuer Stufe 2 und 3 folgen bei Character
Design - bis dahin Thief bzw. ThiefAlpha (der Cousin)."""


def SP(label, icon, bonus=0, effect=None, dodge_only=False):
    return {"label": label, "icon": icon, "bonus": bonus, "effect": effect, "dodge_only": dodge_only}


def Z(wer, text, gefuehl="amusement"):
    z = {"wer": wer, "text": text, "gefuehl": gefuehl}
    if wer == "matte":
        z["name"] = "Mattè"                       # Anzeige mit Akzent, die Stimm-ID ohne
    return z


ENEMIES = {
    "dieb_fabbiu": {
        "name": "Fabbiu", "sprite": "Thief", "cls": "mensch", "element": None, "tier": "laestig",
        "attack": {"label": "Cheap Shot", "icon": "👊"},
        "specials": {"w1": SP("Sand in the Eyes", "🫳", bonus=1, effect="geblendet")},
        "weakness": "charm", "immune": {}, "parade": "sprite", "parade_ziel": 70,
        "sprueche": {
            "start": [Z("fabbiu", "Ooh, nice jacket, tourist. Very leather. Very mine.")],
            "runde": [Z("fabbiu", "Is that your fighting face? My nonna makes that face at the fish market."),
                      Z("fabbiu", "Too slow! You swing like a man carrying shopping."),
                      Z("fabbiu", "Careful, consultant. Don't spill your little snacks."),
                      Z("fabbiu", "You know what you are? A walking pocket.")],
            "gewinnt": [Z("fabbiu", "Thanks for the shopping, tourist! Same time next week?", "joy")],
            "verliert": [Z("fabbiu", "Ow! Ow! Okay, okay! I'm telling my brother!", "fear")]}},
    "dieb_santu": {
        "name": "Santu", "sprite": "ThiefArab", "cls": "mensch", "element": None, "tier": "laestig",
        "attack": {"label": "Elbow", "icon": "👊"},
        "specials": {"w1": SP("Trip You Up", "🦶", bonus=2, effect="ungedeckt")},
        "weakness": "charm", "immune": {}, "parade": "sprite", "parade_ziel": 70,
        "sprueche": {
            "start": [Z("santu", "Easy, easy. We're just talking. Nice bag, by the way.")],
            "runde": [Z("santu", "Hit me, then. My grandmother hits harder, and she's ninety."),
                      Z("santu", "You're sweating, friend. Is it the sun, or is it me?"),
                      Z("santu", "Your pockets are getting lighter just looking at me."),
                      Z("santu", "Hey, everybody! The man in the jacket is losing!", "joy")],
            "gewinnt": [Z("santu", "Keep the change. Oh, wait. I already did.", "joy")],
            "verliert": [Z("santu", "Fine. Fine. You'll see us again. There are more Riccis than you think.", "anger")]}},
    # Matte, der Cousin (Sprite ThiefAlpha): eigener Gegner in der Bande (Mehrgegner-Kampf, 29.10.2026)
    "matte": {
        "name": "Mattè", "sprite": "ThiefAlpha", "cls": "mensch", "element": None, "tier": "gefaehrlich",
        "attack": {"label": "Swing", "icon": "👊"},
        "specials": {"w1": SP("Grabs Your Arms", "🫳", bonus=3, effect="ungedeckt"),
                     "s1": SP("Mattè's Haymaker", "💥", bonus=8, effect="erschuettert")},
        "weakness": "charm", "immune": {}, "parade": "sprite", "parade_ziel": 65},
}


def _b(titel, ziel, gegner, plus, n, ko, aufgabe, nieder):
    weg = "They took %d thing%s from your bag." % (n, "s" if n > 1 else "")
    return {"title": titel, "goal": ziel, "image": "corsican_village_harbour.png", "enemy": gegner, "level": "duc",
            "level_plus": plus, "flee_allowed": True,
            "outcomes": {"ko": {"text": ko, "folgen": []}, "aufgabe": {"text": aufgabe, "folgen": []},
                         "entkommen": {"text": "They're gone between the boats. " + weg, "folgen": []},
                         "flucht": {"text": "You let them go. " + weg, "folgen": []},
                         "niederlage": {"text": nieder, "folgen": []}}}


ENCOUNTERS = {
    "hafen_ricci_1f": _b("A Hand in Your Pocket", "They want: 1 thing from your bag", "dieb_fabbiu", -1, 1,
                         "Fabbiu sits in a puddle and holds his nose. He drops what he had in his sleeve and runs.",
                         "“Okay, okay, take it!” He throws it at your feet and is gone before you can say anything.",
                         "You end up on the cobbles. When you get up, Fabbiu is gone, and so is something from your bag."),
    "hafen_ricci_1s": _b("A Hand in Your Pocket", "They want: 1 thing from your bag", "dieb_santu", -1, 1,
                         "Santu limps off between the nets. He leaves something on a crate, as if he'd never touched it.",
                         "Santu raises both hands, grinning. “You win, you win.” He leaves it on a bollard and strolls off.",
                         "You end up on the cobbles. Santu waves from the end of the quay with something of yours."),
    "hafen_ricci_2": _b("The Ricci Brothers", "They want: 2 things from your bag", "dieb_fabbiu", 0, 2,
                        "Both brothers sit on the quay, holding their ribs and arguing about whose fault it was.",
                        "“Truce, truce!” The brothers back away together, still bickering.",
                        "Two pairs of hands, and then you're on the ground. They take their time choosing."),
    "hafen_ricci_3": _b("The Ricci Gang", "They want: 3 things from your bag", "dieb_fabbiu", 0, 3,
                        "Mattè goes down like a sack of flour. The brothers drag him off, and the harbour applauds.",
                        "The brothers grab Mattè by the arms and pull him away. “Not today, not today!”",
                        "Mattè holds you, the brothers empty your bag. Three things are gone."),
}
# Mehrgegner-Kampf (Duc 29.10.2026): die Brueder zu zweit, die Bande zu dritt - und sie reden als Gruppe. sprueche_id
# haelt die Schluessel kampf.ricci_brueder.* / kampf.ricci_bande.* (schon vertont).
ENCOUNTERS["hafen_ricci_2"].update(enemies=["dieb_fabbiu", "dieb_santu"], lp_faktoren=[0.7, 0.7], sprueche_id="ricci_brueder",
                                   sprueche={
                                   "start": [Z("fabbiu", "Remember us? We brought family this time."),
                                             Z("santu", "Two of us, one of you. Do the maths, consultant.")],
                                   "runde": [Z("santu", "He goes left, I go right, and your wallet goes with us."),
                                             Z("fabbiu", "Last time was luck. Pure luck!", "anger"),
                                             Z("santu", "Tell Elsa we said hello. Oh, wait. She can't catch us either."),
                                             Z("fabbiu", "Your snacks miss us. They told us.")],
                                   "gewinnt": [Z("fabbiu", "Two for two! Write it down, tourist!", "joy")],
                                   "verliert": [Z("santu", "Okay. Okay. Next time we bring Mattè. You'll love Mattè.", "anger")]})
ENCOUNTERS["hafen_ricci_3"].update(enemies=["dieb_fabbiu", "dieb_santu", "matte"], sprueche_id="ricci_bande",
                                   lp_faktoren=[0.6, 0.6, 1.0], sprueche={
                                   # Matte (Duc 29.10.2026: auch eine Stimme, tiefer Bass) - wortkarg, wenige schwere Saetze
                                   "start": [Z("santu", "This is our cousin Mattè. He doesn't talk much. He doesn't need to."),
                                             Z("matte", "Bag. Now.", "anger")],
                                   "runde": [Z("fabbiu", "Mattè, he's looking at you funny!"),
                                             Z("matte", "Stand still.", "annoyance"),
                                             Z("santu", "Three bags this time. We counted."),
                                             Z("matte", "You hit like the wind. Soft.", "amusement"),
                                             Z("fabbiu", "Run, consultant! It's the healthy thing to do!"),
                                             Z("santu", "Everybody in this harbour pays the Riccis. Why not you?")],
                                   "gewinnt": [Z("matte", "Thank you. Come again.", "amusement")],
                                   "verliert": [Z("santu", "Mattè's on the floor. Mattè is never on the floor. Who are you?", "fear")]})
STUFEN = {1: ("hafen_ricci_1f", "hafen_ricci_1s"), 2: ("hafen_ricci_2",), 3: ("hafen_ricci_3",)}
KLAUEN = {1: 1, 2: 2, 3: 3}
