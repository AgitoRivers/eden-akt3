# -*- coding: utf-8 -*-
r"""Taktik-Karte der Belagerung (Duc 31.10.2026, E-102): Raster, Trupps, Wellen und Szenen -> module\eden_rise\taktik.json.

    python werkzeuge\eden_rise\taktik_eden_rise.py

Prototyp: Die Zahlen sind erste Werte, die Szenen Entwurf und noch nicht vertont. Regeln: kern/taktik.py, Wiki docs/wiki/systeme/taktik.md.
Raster: 48x32 Felder auf der Karte (module/eden_rise/taktik/). "." frei, "W" Wald, "B" Berg, "S" Strand, "T" Kirchentreppe, "#" gesperrt, "~" Wasser.
FARBEN und BODEN kommen aus Farbanalysen des Bilds, FREI, ZU, BERGE, WEGE und TREPPE sind von Hand am Bild nachgetragen.
"""
import json, os

BASIS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SP, ZE = 48, 32
FARBEN = [
    "................................................",
    "................................................",
    "................#...............................",
    "...####................~~~.#....................",
    "...##.##.................~...................~~~",
    "...##.........................##..........~~~~~~",
    "................................#........~~~~~~~",
    ".........................................~~~~~~~",
    ".................##......................~~~~~~~",
    "..................####...##.##.#.#.......~~~~~~~",
    "...................#..###...#####.....~~~~~~~~~~",
    ".....................#..######....#...~~~~~~~~~~",
    ".................#.####.##..##..###..~.~~~~~~~~~",
    ".......#........##.#....##.#######..~~~~~~~~~~~~",
    "................##.#........####.##...~~~~~~~~~~",
    "................#######......####...~.~..~~~~~~~",
    "................##..##.....########~~......~~~~~",
    "........#..........................~~....~~~~~~~",
    "............................###.....~~~~~~~~~~~~",
    "...................~~~~~~~~#####~~...~~~....~~~~",
    "....................~~~~~~~~~.~~~~~~~.........~~",
    ".....................~~~~~~~~~~~~~~~...........~",
    "......................~~~~~~~~~~~..............~",
    "~~~....................~~~~~~~~~...............~",
    "~~~~~~~~~..............~~~~~~~~~................",
    "~~~~~~~~~~~~~~~........~~~~~~~~~..............~~",
    "~~~~~~~~~~~~~~~~~~~~....~~~~~~~~~~.............~",
    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~......~~....~~",
    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~..~....~~~~....~",
    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~..~~~",
    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
]
# (x0, y0, x1, y1) einschliesslich
BERGE = [(9, 0, 33, 0), (10, 1, 33, 1), (37, 0, 47, 3), (19, 2, 33, 2), (19, 3, 30, 4), (38, 4, 44, 6)]
ZU = [(35, 1, 37, 2), (16, 2, 17, 3), (3, 3, 8, 6), (5, 12, 8, 14), (30, 5, 34, 7),                             # Turm, Hirtenhuette, Kloster, Koehler, Villa
      (17, 8, 19, 10), (19, 9, 21, 10), (22, 10, 25, 10), (25, 9, 27, 10), (29, 9, 31, 11), (32, 10, 34, 11),    # Dorf oben
      (19, 12, 21, 14), (16, 12, 17, 15), (24, 11, 27, 14), (29, 12, 34, 14), (33, 14, 34, 14),                  # Dorf Mitte, Kirche
      (16, 15, 17, 17), (19, 15, 22, 17), (29, 16, 32, 17), (33, 16, 34, 17), (27, 16, 27, 17),                  # Dorf unten
      (28, 18, 31, 20),                                                                                          # Petrus Werkstatt
      (0, 19, 3, 21), (19, 19, 24, 26),                                                                          # Felsen am Strand
      (31, 24, 47, 29), (31, 20, 36, 23), (42, 19, 47, 23),                                                      # Insel mit der Grotte
      (27, 8, 28, 8)]                                                                                            # Barrikade im Norden
WASSER = [(35, 16, 36, 17), (36, 15, 36, 15),(19, 19, 36, 19), (37, 18, 47, 19), (41, 17, 47, 17), (44, 15, 47, 16), (39, 14, 47, 14)]
FREI = [(39, 15, 43, 16),                                                                                        # Yacht
        (36, 14, 38, 14), (37, 15, 38, 16), (37, 17, 40, 17),                                                    # Mole
        (19, 18, 27, 18), (32, 18, 36, 18), (34, 19, 37, 20), (37, 20, 41, 21), (38, 22, 41, 23),                # Kai, Weg zur Grotte
        (18, 11, 23, 11), (22, 12, 23, 14), (23, 15, 28, 15), (28, 9, 28, 15), (28, 15, 33, 15), (23, 16, 26, 17)]  # Gassen, Platz

BODEN = [
    "WW.WWW.WW.........................BB............",
    "WW..WW..WW........................W.............",
    "WWWWW.W.W...WWW.................................",
    "WWW.......WW.....................W..............",
    "WWW......WW.WW....W............W................",
    "WWW......WW..WWW..WWW...BW.WWW......WB..........",
    "W........WWW..WWWWWWWW.WW..WW.......WW..........",
    "W.W..W...WWW......W.WW..W.WWWW..................",
    "WWW.....W...........WWW.WWW...W..W..W...........",
    "WWW.WWWWW...W...W.....WWW.......W...............",
    "WWWWW..WWWW..WW....................WW...........",
    ".WWWWW...WWWW....SS................W............",
    "W..WW....WW...W...S.............................",
    "WWW......W.W.WW........W........................",
    "W.WW......WW.WWW................................",
    ".WWWWWWW..W.............W.......................",
    ".WWWBWW..WWS..W........WW..............BB.......",
    "W.WWWWW..W.WWWWW........S.......................",
    "SS.W..W.WW.WWW..WW..............................",
    "....SS..W.WWWWWBW...............................",
    ".....SS..SWWWWW.WW......................W.......",
    "....SSSSSSWW...WWWW..................WW..W......",
    "SSSSSSSSSSSSSS........................W.WW......",
    ".......SSSSSSSSSSSS...................W..W......",
    "...........SSSSSSSS.............................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
]
# Wege durch Wald und Macchia: Wer auf dem Weg bleibt, ist schnell und ungeschuetzt (Duc 31.10.2026)
WEGE = [(0, 12, 2, 12), (2, 12, 2, 13), (2, 13, 4, 13), (4, 13, 4, 15), (4, 15, 10, 15), (10, 15, 10, 21), (10, 16, 15, 16), (15, 16, 15, 18), (15, 18, 18, 18),   # West, Strand
        (9, 8, 16, 8), (16, 8, 16, 11), (16, 11, 18, 11),                                                                                                       # Bruecke
        (22, 7, 29, 7), (29, 8, 40, 8)]                                                                                                                         # Nord, Villa
TREPPE = [(23, 16, 26, 16)]
GELAENDE = {".": {"name": "Open ground", "abwehr": 0, "text": "No cover."},
            "W": {"name": "Forest", "abwehr": 1, "tarnung": True, "text": "Slow. +1 DEF. Hides your troop: enemies only see it from 2 fields, drones always."},
            "B": {"name": "Rocks", "abwehr": 2, "text": "Very slow. +2 DEF. Robots cannot climb."},
            "S": {"name": "Beach", "abwehr": 0, "text": "Heavy units and robots sink in. No cover."},
            "T": {"name": "Church Steps", "abwehr": 1, "text": "+1 DEF."}}
# Laufkosten je Gangart, was fehlt, ist gesperrt. Drohnen fliegen und zahlen immer 1.
GANG = {"fuss": {".": 1, "W": 2, "B": 3, "S": 1, "T": 1}, "schwer": {".": 1, "W": 2, "B": 4, "S": 2, "T": 1},
        "tier": {".": 1, "W": 1, "B": 2, "S": 1, "T": 1}, "maschine": {".": 1, "W": 3, "S": 2, "T": 1}}


def raster():
    r = [list(z) for z in FARBEN]
    for y, z in enumerate(BODEN):
        for x, c in enumerate(z):
            if c != "." and r[y][x] == ".":
                r[y][x] = c
    for liste, zeichen in ((BERGE, "B"), (ZU, "#"), (WASSER, "~"), (FREI, ".")):
        for x0, y0, x1, y1 in liste:
            for y in range(y0, y1 + 1):
                for x in range(x0, x1 + 1):
                    r[y][x] = zeichen
    for liste, zeichen in ((WEGE, "."), (TREPPE, "T")):
        for x0, y0, x1, y1 in liste:
            for y in range(y0, y1 + 1):
                for x in range(x0, x1 + 1):
                    if r[y][x] not in "#~":
                        r[y][x] = zeichen
    return ["".join(z) for z in r]


TRUPPS = {
    "duc": {"name": "Duc", "text": "You play him. His attacks open a real fight. If he falls, the wave starts again.", "art": "stumpf", "lp": 0, "angriff": 0, "abwehr": 3, "bewegung": 7, "start": [26, 17], "kann": "Fights for real"},
    "maxwell": {"name": "Mr. Maximum", "rolle": "schwer", "sprite": "MaxwellSteelMop", "text": "You play him too. His attacks open a real fight, with his own bag. Strong against robots. On the pier or the yacht he strikes back twice. If he falls, he is out until the next wave.", "art": "stumpf", "gang": "schwer", "lp": 46, "angriff": 11, "abwehr": 4, "bewegung": 5, "start": [39, 17], "kann": "Fights for real"},
    "chiara": {"name": "Chiara", "rolle": "fern", "text": "The crew, with a taser rifle that Rosi built. Reach of two fields. Whoever she hits stops for one round, but not robots. No strike back up close.", "art": "taser", "lp": 30, "angriff": 7, "abwehr": 2, "bewegung": 6, "reichweite": 2, "start": [37, 15], "kann": "Taser Rifle"},
    "wolff": {"name": "Wolff", "rolle": "schnell", "sprite": "Wolff", "text": "The Legion. Blades, strong against people and animals. Strikes first when attacked.", "art": "klinge", "lp": 34, "angriff": 10, "abwehr": 3, "bewegung": 7, "start": [15, 15], "kann": "First Strike"},
}
# Verdiente Trupps (Duc 31.10.2026): hoechstens sechs auf der Karte. vertrauen oder flag schaltet frei. Werte sind erste Zahlen.
RESERVE = {
    "elsa": {"name": "Elsa", "rolle": "fern", "text": "The law, with a service pistol. Once each round she fires first at an enemy that comes into reach. Reach of two fields, no strike back up close. Strong against drones.", "art": "fern", "lp": 26, "angriff": 8, "abwehr": 2, "bewegung": 6, "reichweite": 2, "kann": "Overwatch", "vertrauen": 2, "flag": "elsa_hilft"},
    "rosi": {"name": "Rosi", "rolle": "schwer", "text": "A hammer and a bad mood. She knows where robots break: their armour does nothing against her.", "art": "stumpf", "lp": 30, "angriff": 10, "abwehr": 3, "bewegung": 6, "kann": "Knows the Machine", "vertrauen": 2},
    "yamamoto": {"name": "Yamamoto", "rolle": "schnell", "text": "One katana. If he defeats his target, he may move and attack again, once each round. He cannot take much.", "art": "klinge", "lp": 24, "angriff": 12, "abwehr": 2, "bewegung": 7, "kann": "Clean Cut", "vertrauen": 2},
    "bibi": {"name": "Bibi", "rolle": "fern", "text": "The Red Trio, with flash and water grenades. Reach of two fields, no strike back up close. A dog she hits stops for one round. Her water grenade can also slow a burning house.", "art": "fern", "lp": 24, "angriff": 7, "abwehr": 2, "bewegung": 7, "reichweite": 2, "kann": "Light and Water", "flag": "rt_ausgang_alle"},
}
# Welle 2: Der Brandtrupp zuendet das Dorf an. lunte = Runden bis das Haus verloren ist, ein Brandtrupp daneben macht es schneller.
HAEUSER = [{"id": "post", "name": "Post Office", "x": 21, "y": 13, "lunte": 5}, {"id": "batu", "name": "Ba Tu's Shop", "x": 22, "y": 17, "lunte": 6},
           {"id": "bar", "name": "Alva's Bar", "x": 27, "y": 17, "lunte": 7}, {"id": "werkstatt", "name": "Petru's Workshop", "x": 28, "y": 18, "lunte": 8}]
# Machtleiste (Advance Wars): Schaden laedt sie, eingesteckter doppelt so schnell. Voll = einmal der grosse Moment des Truppenfuehrers.
MACHT = {
    "duc": {"art": "sammeln", "titel": "Rally", "ruf": "Everyone up. We are not done here.", "text": "All troops get back a quarter of their health, you too."},
    "maxwell": {"art": "rundum", "titel": "Maximum Force", "ruf": "Mr. Maximum does not step aside.", "text": "Hits every enemy next to him at once, harder than normal, and nobody strikes back."},
    "chiara": {"art": "weit", "titel": "Sweep the Deck", "ruf": "Five stars for the taser. Zero for you.", "text": "Hits every enemy within two fields, and nobody strikes back."},
    "wolff": {"art": "nochmal", "titel": "Legion Drill", "ruf": "Again. Faster.", "text": "He may move and attack again this round."},
    "elsa": {"art": "drohnen", "titel": "Clear the Sky", "ruf": "You do not have a permit for that.", "text": "Shoots down every drone within six fields."},
    "rosi": {"art": "roboter", "titel": "Pull the Plug", "ruf": "I know exactly where you break.", "text": "Hits every robot within three fields very hard."},
    "yamamoto": {"art": "schnitt", "titel": "One Cut", "ruf": "Only one.", "text": "One enemy in reach takes huge damage and cannot strike back."},
    "bibi": {"art": "lachen", "titel": "Nervous Laugh", "ruf": "Ha ha ha ha! Sorry. I do that.", "text": "Her laugh pulls every enemy within five fields onto her this round."},
}
# Doppelangriff: Beim ersten Mal sagen die zwei etwas (Entwurf, unvertont)
DUO = {
    "maxwell+wolff": "Wolff: You hit like a door. Mr. Maximum: Mr. Maximum IS the door.",
    "chiara+maxwell": "Chiara: Three stars. Mr. Maximum: Only three? Chiara: You stood on my foot.",
    "chiara+wolff": "Wolff: Your hook was late. Chiara: Your face was early.",
    "maxwell+rosi": "Rosi: Don't break the part I want. Mr. Maximum: Mr. Maximum breaks only the rest.",
    "elsa+wolff": "Elsa: I did not see that. Wolff: Nobody did, Lieutenant.",
}
# Die Buergerwehr steht fest und wehrt sich nur, geskriptet im Zentrum (Duc 31.10.2026). Minicu steht neben Pascal im Norden, erst zum Verrat schickt Pascal ihn ans Tor (Duc 02.11.2026).
WEHR = {
    "pascal": {"name": "Pascal", "text": "Village guard at the north barricade. Fixed.", "art": "stange", "lp": 24, "angriff": 8, "abwehr": 2, "start": [28, 9]},
    "minicu": {"name": "Minicu", "rolle": "schwer", "text": "The strongest man in the village. He stands where Pascal tells him. Fixed.", "art": "klinge", "lp": 60, "angriff": 10, "abwehr": 4, "start": [28, 10], "start_finale": [29, 15]},
    "alva": {"name": "Alva", "rolle": "fern", "text": "Village guard on the square, with her father's shotgun. Reach of two fields. Fixed.", "art": "fern", "lp": 24, "angriff": 8, "abwehr": 2, "reichweite": 2, "start": [23, 14]},
}
# Eckige Plaetze der Aufstellung, dorthin zieht der Spieler die Trupps (Duc 31.10.2026). Holms Vorschlag steht schon darauf.
PLAETZE = [{"x": x, "y": y, "front": f} for f, felder in (("West", ((14, 11), (15, 15), (15, 18))), ("South", ((12, 20), (16, 20), (20, 18))),
                                                         ("Church", ((24, 16), (26, 16), (26, 17))), ("Yacht", ((37, 15), (42, 16), (39, 17), (40, 15))), ("North", ((28, 11),))) for x, y in felder]
# Hilfe ohne Trupp (Duc 31.10.2026): Holm ist immer dabei, dazu zwei, die man sich mit Vertrauen verdient hat. takt: wie oft einsetzbar, None = wirkt immer
HILFE = {
    "holm": {"name": "Holm", "kann": "Bridge Command", "fest": True, "takt": "runde", "text": "One order each round: a troop that has already acted may act again."},
    "sophia": {"name": "Sophia", "kann": "Radio", "vertrauen": 2, "takt": None, "text": "She listens to their radio. You also see where each enemy will stand in two rounds."},
    "lola": {"name": "Lola", "kann": "Galley", "vertrauen": 2, "takt": "welle", "text": "Once each wave she patches up a troop that stands on the quay or the pier. Her galley is on the yacht, so she needs the yacht afloat."},
    "lea": {"name": "Lea", "kann": "Tender", "vertrauen": 2, "takt": None, "text": "She gets in the way of their boats. Enemies from the sea start one round late."},
    "siri": {"name": "Siri", "kann": "The Stream", "vertrauen": 2, "takt": "welle", "text": "Her stream answers Alon's. Once each wave, one whole front stops for one round."},
    "ligeia": {"name": "Ligeia", "pid": "sirene", "kann": "The Song", "vertrauen": 3, "takt": "schlacht", "text": "One song in the whole battle. Every pirate near the water falls asleep for two rounds. Robots do not listen."},
    "danzel": {"name": "Danzel", "kann": "Steel Lining", "flags": ["rt_ausgang_alle", "rt_ausgang_getrennt"], "takt": "welle", "text": "He designed those plates. Once each wave he sews one into a troop's coat: it takes half the damage until the next round. He also fights at the church door, but he will not stay for Mr. White.",
               "einheit": {"name": "Danzel", "rolle": "schnell", "text": "He fights whatever reaches the church door. Fixed. He will not stay for Mr. White.", "art": "stumpf", "lp": 22, "angriff": 8, "abwehr": 2, "start": [27, 15]}},
}
# Was die Figuren in der Belagerung tragen, in Szene und Seitenleiste (Duc 03.11.2026: Holm im langaermligen Hemd, nicht in Uniform)
SETS = {"holm": "holm_shirt"}
FEINDE = {
    "hund": {"name": "Collared Dog", "rolle": "schnell", "ki": "jaeger", "text": "Fast. It hunts the most wounded troop it can reach.", "klasse": "tier", "gang": "tier", "lp": 14, "angriff": 6, "abwehr": 1, "bewegung": 8, "kampf": "tk_hund"},
    "agent": {"name": "Agent", "rolle": "schnell", "text": "One of Mr. White's men, with a baton. Goes for the nearest troop.", "klasse": "mensch", "lp": 20, "angriff": 7, "abwehr": 2, "bewegung": 6, "kampf": "tk_agent"},
    "brute": {"name": "Brute", "rolle": "schwer", "ki": "brecher", "text": "Ignores your troops and walks straight to the church.", "klasse": "mensch", "gang": "schwer", "lp": 32, "angriff": 10, "abwehr": 4, "bewegung": 5, "kampf": "tk_brute"},
    "schuetze": {"name": "Marksman", "rolle": "fern", "ki": "wache", "text": "One of Mr. White's agents, with a rifle. Holds her ground for three rounds and shoots from three fields, unless a troop comes close. No strike back up close.", "klasse": "mensch", "lp": 14, "angriff": 8, "abwehr": 1, "bewegung": 5, "reichweite": 3, "kampf": "tk_schuetze"},
    "brand": {"name": "Torch Pirate", "rolle": "schnell", "ki": "brand", "pirat": True, "text": "One of Buenaventura's men, paid to burn the village. Runs to the burning houses and makes them burn faster.", "klasse": "mensch", "lp": 20, "angriff": 9, "abwehr": 2, "bewegung": 6, "kampf": "tk_pirat"},
    "gunner": {"name": "Pirate Gunner", "rolle": "fern", "pirat": True, "text": "One of Buenaventura's men, with a long pistol. Shoots from two fields. No strike back up close.", "klasse": "mensch", "lp": 16, "angriff": 9, "abwehr": 1, "bewegung": 5, "reichweite": 2, "kampf": "tk_gunner"},
    "brawler": {"name": "Pirate Brawler", "rolle": "schwer", "pirat": True, "text": "One of Buenaventura's men, all muscle and a sabre. Slow and hard to put down.", "klasse": "mensch", "gang": "schwer", "lp": 34, "angriff": 10, "abwehr": 3, "bewegung": 5, "kampf": "tk_brawler"},
    "bonaventure": {"name": "Captain Buenaventura", "rolle": "schnell", "pirat": True, "text": "The king of no island. Beat him, and his men stop fighting.", "klasse": "mensch", "lp": 44, "angriff": 11, "abwehr": 3, "bewegung": 6, "kampf": "tk_bonaventure"},
    "roboter": {"name": "Boarding Robot", "rolle": "schwer", "text": "Slow and very tough. It tears the yacht apart while nobody stands near it.", "klasse": "maschine", "gang": "maschine", "lp": 26, "angriff": 8, "abwehr": 6, "bewegung": 4, "kampf": "tk_roboter"},
    "roboter_schwer": {"name": "Heavy Boarding Robot", "rolle": "schwer", "text": "Bigger, slower and much harder to stop. It tears the yacht apart while nobody stands near it.", "klasse": "maschine", "gang": "maschine", "lp": 42, "angriff": 11, "abwehr": 8, "bewegung": 3, "kampf": "tk_roboter_schwer"},
    "roboter_kobra": {"name": "Cobra Robot", "rolle": "schnell", "ki": "jaeger", "text": "A fast steel snake from the beach. It hunts the most wounded troop it can reach, and rocks do not stop it. A taser does nothing.", "klasse": "maschine", "gang": "tier", "lp": 16, "angriff": 8, "abwehr": 3, "bewegung": 8, "kampf": "tk_kobra"},
    "roboter_skorpion": {"name": "Scorpion Robot", "rolle": "schnell", "ki": "schwaeche", "text": "Small, fast and low to the ground. It goes for the troop with the weakest armour, and rocks do not stop it. A taser does nothing.", "klasse": "maschine", "gang": "tier", "lp": 18, "angriff": 9, "abwehr": 4, "bewegung": 7, "kampf": "tk_skorpion"},
    "drohne": {"name": "Combat Drone", "rolle": "fern", "ki": "schwaeche", "text": "Flies over everything and goes for the troop with the weakest armour. It sees hidden troops.", "klasse": "flieger", "lp": 12, "angriff": 7, "abwehr": 0, "bewegung": 11, "fliegt": True, "reichweite": 2, "kampf": "tk_drohne"},
    "white": {"name": "Mr. White", "text": "He walks slowly to the church. Nothing stops him until the giant at the gate falls. After that, only you can.", "klasse": "mensch", "lp": 999, "angriff": 16, "abwehr": 9, "bewegung": 2, "boss": True, "kampf": "tk_white"},
}
SUED, WEST, OST, NORD = [[6, 21], [9, 22], [12, 22], [5, 20], [8, 20], [11, 21]], [[4, 9], [6, 11], [4, 13], [5, 10], [4, 12], [4, 15]], \
    [[43, 15], [43, 16], [42, 15], [42, 16], [41, 15], [41, 16]], [[28, 6], [27, 6], [29, 6], [28, 5], [27, 5], [29, 5]]
# Was von der Karte offen ist, (x0, y0, x1, y1) einschliesslich, damit man nicht scrollen muss (Duc 02.11.2026). Klein: nur Sued und West. Breit: bis zur Yacht. Ganz: auch der Norden.
KLEIN, BREIT, GANZ = [3, 7, 33, 24], [3, 5, 44, 25], [3, 3, 44, 26]
# Sechs Wellen auf drei Tage (Duc 01.11.2026, E-114), am ersten Tag deutlich weniger Gegner. par: so viele Runden sind kein Fehler (kern/belagerung.py).
# Balancing Duc 02.11.2026 nach Simulation (tests/sim_belagerung.py): weniger Masse in Welle 4 und 5, die flinken Roboter kommen von Sued, West und Nord.
WELLEN = [
    {"id": 1, "ausschnitt": KLEIN, "titel": "The First Wave", "szene": "welle_1", "ende": "ende_1", "par": 5,
     "beats": [{"runde": 1, "szene": "w1_legion"}, {"runde": 2, "szene": "w1_hund"}, {"runde": 3, "szene": "w1_boote"}], "nachschub": [{"runde": 3, "feinde": [("hund", WEST[1]), ("agent", SUED[4])]}],
     "feinde": [("agent", SUED[0]), ("agent", SUED[1]), ("hund", SUED[2]), ("hund", WEST[0]), ("agent", WEST[2])]},
    {"id": 2, "ausschnitt": BREIT, "titel": "The Second Wave", "szene": "welle_2", "ende": "ende_2", "par": 8,
     "beats": [{"runde": 1, "szene": "w2_elsa", "bed": {"einheit": "elsa"}}, {"runde": 2, "szene": "w2_deck"}, {"runde": 3, "szene": "w2_gewehr"}], "nachschub": [{"runde": 3, "feinde": [("schuetze", WEST[1]), ("roboter_kobra", SUED[1])]}],
     "feinde": [("agent", WEST[0]), ("agent", SUED[0]), ("hund", SUED[2]), ("roboter", OST[0]), ("roboter", OST[1]), ("drohne", OST[4])]},
    {"id": 3, "ausschnitt": KLEIN, "titel": "The Third Wave", "szene": "welle_3", "ende": "ende_3", "par": 7, "feuer": True,
     "beats": [{"runde": 2, "szene": "w3_post"}, {"runde": 3, "szene": "w3_trio", "bed": {"flag": "rt_ausgang_alle"}},
               {"runde": 3, "szene": "w3_dach_leer", "bed": {"nicht_flag": "rt_ausgang_alle"}}, {"runde": 4, "szene": "w3_pascal"}], "nachschub": [{"runde": 3, "feinde": [("gunner", SUED[4]), ("roboter_skorpion", WEST[2])]}],
     "feinde": [("brand", SUED[0]), ("brand", SUED[1]), ("brand", SUED[3]), ("gunner", SUED[5]), ("agent", WEST[0]), ("agent", WEST[1])]},
    {"id": 4, "ausschnitt": BREIT, "titel": "The Fourth Wave", "szene": "welle_4", "ende": "ende_4", "par": 9, "feuer": True, "kapitaen": True,
     "beats": [{"runde": 3, "szene": "w4_1924", "bed": {"t": "dorf_rudert"}}, {"runde": 3, "szene": "w4_allein", "bed": {"nicht_t": "dorf_rudert"}}], "nachschub": [{"runde": 3, "feinde": [("roboter_kobra", SUED[4])]}, {"runde": 5, "feinde": [("roboter_skorpion", WEST[3]), ("schuetze", WEST[2])]}],
     "feinde": [("brand", SUED[0]), ("brand", SUED[1]), ("bonaventure", SUED[2]), ("brawler", SUED[3]), ("agent", WEST[0]), ("roboter", OST[0]), ("roboter", OST[1]), ("drohne", OST[4])]},
    {"id": 5, "ausschnitt": BREIT, "titel": "The Fifth Wave", "szene": "welle_5", "ende": "falscher_sieg", "par": 9, "yacht_sinkt": True,
     "beats": [{"runde": 3, "szene": "w5_schlange"}], "nach_ende": {"szene": "white_angebot", "bed": {"flag": "bl_funk_white"}}, "nachschub": [{"runde": 3, "feinde": [("roboter_kobra", SUED[3]), ("roboter_kobra", NORD[0])]}, {"runde": 5, "feinde": [("roboter_skorpion", WEST[2])]}],
     "feinde": [("roboter_schwer", OST[0]), ("roboter", OST[2]), ("drohne", OST[4]), ("agent", WEST[0]), ("agent", WEST[1]), ("brute", SUED[0]), ("agent", SUED[1])]},
    {"id": 6, "ausschnitt": GANZ, "titel": "The Last Wave", "szene": "verrat", "finale": True, "yacht_sinkt": True, "nachschub": [{"runde": 3, "feinde": [("roboter_kobra", NORD[5])]}],
     "feinde": [("white", NORD[0]), ("agent", NORD[1]), ("agent", NORD[2]), ("agent", NORD[3]), ("brute", NORD[4]), ("agent", SUED[0]), ("agent", SUED[1]), ("roboter_skorpion", WEST[0]), ("drohne", OST[0])]},
]
# Vor jeder Welle ausser der letzten (Duc 02.11.2026, Vorbild Fire Emblem): Titel, Lage auf der Karte, klarer Auftrag, dann erst die Aufstellung. Entwurf, unvertont.
# Holm steht im Kommandoposten mit dem Fernglas: Sie sagt, was sie sieht und wo, nie Runden (Duc 02.11.2026). Die Zahl auf der Karte erklaert ein Hinweis ohne Sprecher.
# zu: wohin die Kamera faehrt. zeigt: welche Feinde dort leuchten. wenn: nur mit dieser Reserve, sonst spricht sonst. kurz: der eine Satz beim Neustart.
ZIEL = "Defeat them all. You lose if the church falls or you go down."
BRIEFING = {
    "1": {"kurz": "Someone south, someone west. Don't let the dogs reach the wounded.", "zeilen": [
        {"art": "titel", "ober": "Day 21 · Afternoon", "text": "The First Wave", "ziel": ZIEL},
        {"wer": "Holm", "text": "I wanted to be on that quay. Fine. I can see all of you from here, so nobody gets to be stupid."},
        {"wer": "Holm", "text": "Boats on the south beach. Agents with batons, and dogs in collars. A dog runs past you and goes for whoever is bleeding.", "zu": SUED[1], "zeigt": ["agent", "hund"]},
        {"wer": "Wolff", "text": "More in the scrub to the west. On the road you are fast. In the trees they cannot see you until they are close.", "zu": WEST[1], "zeigt": ["agent", "hund"]},
        {"wer": "Holm", "text": "They want the church. Casanova is inside, with the children and the old people. If it falls, we have lost.", "zu": [25, 15]},
        {"wer": "Holm", "text": "And far out on the water, behind them, more boats. Not here yet, but they are coming."},
        {"wer": "", "text": "A number on the map means more enemies are on the way. It counts the rounds until they arrive."},
        {"wer": "Holm", "text": "Put your people on the lit squares, one south and one west. Then say begin."}]},
    "2": {"kurz": "Keep somebody heavy at the yacht. More are coming from the west.", "zeilen": [
        {"art": "titel", "ober": "Day 21 · Sunset", "text": "The Second Wave", "ziel": ZIEL},
        {"wer": "Holm", "text": "Two robots on the water, and they want the yacht. If nobody stands near it, they tear it open.", "zu": OST[0], "zeigt": ["roboter"]},
        {"wer": "Rosi", "text": "They are slow and thick. Send someone heavy. A taser does nothing to them.", "gefuehl": "anger", "zu": OST[1], "zeigt": ["roboter"], "wenn": "rosi",
         "sonst": {"wer": "Mr. Maximum", "text": "Number One. Mr. Maximum will explain the mop to them. A taser does nothing to them."}},
        {"wer": "Holm", "text": "That drone sees everyone, also in the trees. It goes for whoever has the thinnest armour.", "zu": OST[4], "zeigt": ["drohne"]},
        {"wer": "Holm", "text": "Agents and a dog again, south and west. And further back in the scrub, something shines. A rifle, I think. It will be here soon.", "zu": WEST[1], "zeigt": ["agent", "hund", "schuetze"]},
        {"wer": "Chiara", "text": "Something is moving on the beach behind them. A snake. Made of steel. One star. My taser does nothing to it.", "gefuehl": "anger", "zu": SUED[1], "zeigt": ["roboter_kobra"]},
        {"wer": "Holm", "text": "One troop at the yacht, one in the west, one on the beach. Places."}]},
    "3": {"kurz": "Torches first. Stand next to a burning house and get them out.", "zeilen": [
        {"art": "titel", "ober": "Day 22 · Afternoon", "text": "The Third Wave", "ziel": "Defeat them all, and get people out of the burning houses. You lose if the church falls or you go down."},
        {"wer": "Buenaventura", "text": "I am Captain Buenaventura of The Eventually! This is nothing personal. I have debts.", "zu": SUED[1], "zeigt": ["brand", "gunner"]},
        {"wer": "Holm", "text": "That flag. Frankfurt, that's your man from the wreck. And he's not paying for those torches himself.", "zu": SUED[1]},
        {"wer": "Holm", "text": "Pirates with torches. They run to the houses, and they make them burn faster. The gunner shoots from two fields away.", "zu": SUED[3], "zeigt": ["brand", "gunner"]},
        {"wer": "Petru", "text": "Hm. There are people in those houses. Stand next to a burning house and get them out. It costs that troop's action.", "zu": [21, 13]},
        {"wer": "Holm", "text": "Agents in the west. Further out I see another boat with a gunner, and something small and fast in the scrub. It goes for the thinnest armour.", "zu": WEST[2], "zeigt": ["agent", "roboter_skorpion"]},
        {"wer": "Holm", "text": "Stop the torches first. Then the rest. Places."}]},
    "4": {"kurz": "Beat the captain and his men stop. Keep somebody at the yacht.", "zeilen": [
        {"art": "titel", "ober": "Day 22 · Sunset", "text": "The Fourth Wave", "ziel": "Defeat them all, and get people out of the burning houses. You lose if the church falls or you go down."},
        {"wer": "Buenaventura", "text": "Today I pay what I owe! Men, the houses!", "zu": SUED[2], "zeigt": ["bonaventure", "brand", "brawler"]},
        {"wer": "Holm", "text": "That's the captain, and he has come himself. Beat him, and his men stop fighting.", "zu": SUED[2], "zeigt": ["bonaventure"]},
        {"wer": "Holm", "text": "Two robots and a drone at the yacht again.", "zu": OST[0], "zeigt": ["roboter", "drohne"]},
        {"wer": "Mr. Maximum", "text": "Number One. Mr. Maximum will stand on the pier. On the pier, he strikes back twice.", "gefuehl": "anger", "zu": [39, 17]},
        {"wer": "Holm", "text": "Don't look only at the sea. Something made of steel is moving on the beach behind them. And far back in the west, a rifle and something small. They come later.", "zu": WEST[3], "zeigt": ["roboter_kobra", "roboter_skorpion", "schuetze"]},
        {"wer": "Holm", "text": "The captain, the robots, the fires. You choose the order, but choose fast. Places."}]},
    "5": {"kurz": "Stop the big man first. Pascal and Minicu hold the north.", "zeilen": [
        {"art": "titel", "ober": "Day 23 · Afternoon", "text": "The Fifth Wave", "ziel": ZIEL},
        {"wer": "Holm", "text": "A heavy robot on the water, with a smaller one and a drone.", "zu": OST[0], "zeigt": ["roboter_schwer", "roboter", "drohne"]},
        {"wer": "Rosi", "text": "The big one is mine. Its armour stops nearly everything. It does not stop me.", "gefuehl": "anger", "zu": OST[0], "zeigt": ["roboter_schwer"], "wenn": "rosi",
         "sonst": {"wer": "Mr. Maximum", "text": "The big one is for Mr. Maximum. Nobody else will scratch it."}},
        {"wer": "Holm", "text": "A very big man on the beach, and he doesn't care about you at all. He walks straight to the church. Stop him first.", "zu": SUED[0], "zeigt": ["brute"]},
        {"wer": "Holm", "text": "Behind them I see steel snakes. One on the beach, one on the north road. And later, something small in the west.", "zu": NORD[0], "zeigt": ["roboter_kobra", "roboter_skorpion"]},
        {"wer": "Pascal", "text": "Leave the north to Minicu and me. Nothing comes through here unless I let it.", "zu": [28, 9]},
        {"wer": "Minicu", "text": "I hold. Pascal said so.", "zu": [28, 10]},
        {"wer": "Holm", "text": "Good. Send one troop up there anyway, if you can spare one. Church first, yacht second. Places."}]},
}
# Der Morgen danach (kern/belagerung.py). Erste Zahlen, der Spieltest legt sie fest. Stein ist Slate oder Granite.
BESTAND = {"notration": {"timber": 4, "stein": 2}, "mini_max": 3, "treffer": 3, "perfekt_spart": 2, "crew_aufschlag": 2, "fehler_eine": 2, "fehler_zwei": 5,
           "kosten": {"barrikade": {"timber": 4}, "kirche": {"timber": 2, "stein": 2}, "yacht": {"timber": 3, "stein": 1}, "haus": {"timber": 3, "stein": 3}},
           "barrikaden": {"South": {"name": "South Barricade", "feld": [14, 19]}, "West": {"name": "West Barricade", "feld": [12, 13]}},
           "texte": {"barrikade": "Whole, it costs them a round at this front.", "kirche": "Gives the church one life back.", "yacht": "Gives the yacht one point back.",
                     "haus": "Only boards and a roof for now. It will be easier to rebuild later."},
           "holm": {"gut": "Holm: \"You did well yesterday. We got off lightly.\"", "mittel": "Holm: \"It could be worse. It could also be a lot better.\"", "schlecht": "Holm: \"That was bad. Don't look at it for long. Start at one end.\""},
           "bilder": {"barrikade": "/bg/eden_rise_piazza_treppe.png", "kirche": "/bg/eden_rise_piazza_treppe.png", "yacht": "/bg/yacht_aft_deck_dining.png", "haus": "/bg/eden_rise_piazza_treppe.png"}}
SZENEN = {
    "welle_1": [["Holm", "Three fronts: the south beach, the scrub in the west, and the sea. Today it is only dogs and agents."],
                ["Holm", "Agents walk and dogs run. Hold the church. If they get the church, they have the village."]],
    # Drehbuch "Hold the Line" (Duc 02.11.2026): Beats je Runde. Holm sagt nur, was sie sieht, Lagemeldungen auch von Chiara und Totò.
    "w1_legion": [["Wolff", "You asked for a line. The Legion brought one.", {"zu": WEST[1]}]],
    "w1_hund": [["Chiara", "Dog! On the left! It's going for whoever is bleeding!"]],
    "w1_boote": [["Totò", "Comandante! More boats! Behind the first ones!"]],
    "ende_1": [["Holm", "They're pulling back. Faen. They didn't even try."], ["Pascal", "North is quiet. Leave it with me.", {"zu": [28, 9]}]],
    "w2_elsa": [["Elsa", "Five years in a locker. It still fits. Don't say anything."]],
    "w2_deck": [["Chiara", "They're on my deck! That's a zero! A ZERO!", {"zu": OST[0]}]],
    "w2_gewehr": [["Holm", "Something shines in the scrub. A rifle.", {"zu": WEST[1]}]],
    "w3_post": [["Petru", "Hm. There are still people in the post office. Get them out before the roof goes.", {"zu": [21, 13]}]],
    "w3_trio": [["Bibi", "Ha ha! ...Sorry. I do that. Okay! Where's the fire? ...No, I can see it. Stupid question."]],
    "w3_dach_leer": [["Holm", "Nobody on the west roofs today."]],
    "w3_pascal": [["Pascal", "Holm. The post office is burning. How long does this go on?", {"zu": [28, 9]}], ["Holm", "Until they stop."]],
    "w4_1924": [["", "1924", {"art": "titel", "ober": "Day 22 · Sunset", "ziel": "The village rows out."}],
                ["", "Mina has knocked on every door. Petru stands in the first boat with his grandfather's oar, and Lea is in the second.", {"zu": OST[0]}],
                ["Petru", "Hm. In 1924 my grandfather rowed out to the Margot. Tonight it's our turn."],
                ["Lea", "It was me, Petru. I sent the coordinates, and Alon saw them. It's my fault."],
                ["Petru", "The sea doesn't ask whose fault. It asks who rows."],
                ["Holm", "The boats have turned across the bay. Nothing more is landing tonight."]],
    "w4_allein": [["Mina", "They heard me. They just didn't open."]],
    "ligeia_singt": [["Ligeia", "I sang a ship to sleep once, and I thought that was all my voice could do. Tonight I sang for you, Duc."]],
    "w5_schlange": [["Minicu", "Does it hurt?", {"zu": [28, 10]}], ["Pascal", "It's a machine, Minicu."], ["Minicu", "Still."]],
    "white_angebot": [["", "Holm is still counting. On Pascal's channel, very quietly, a calm voice speaks. Rosi's radio picks it up."],
                      ["Mr. White", "Three days of fire, Pascal. You can end it tonight. Nobody gets hurt. You have my word."],
                      ["", "Pascal does not answer."]],
    "welle_2": [["Holm", "The sun is going down, and they are back. There's a rifle in the west, and those shapes on the water are robots. Keep somebody close to the yacht."]],
    "ende_2": [["Holm", "That's the first day. Nobody goes home. Sleep where you can."],
               ["Casanova", "I have the paper again. Mr. Alon's man left it on the church step. He says one signature, and tomorrow nobody comes."],
               ["Casanova", "I have not signed it. I want you to know that I read it twice."],
               ["Casanova", "Whoever brings these has beautiful handwriting. 'Madame la Maire'. Like an invitation."]],
    "welle_3": [["Holm", "New boats on the beach, and those aren't agents. They're pirates, with torches."],
                ["Buenaventura", "I am Captain Buenaventura of The Eventually! This is nothing personal. I have debts."],
                ["Petru", "Hm. They are lighting the houses, and there are people inside. Stand next to a burning house and get them out."]],
    "ende_3": [["Totò", "They're going back to the boats! ...The captain isn't. He's just sitting out there, Comandante."]],
    "welle_4": [["Holm", "All of them this time. Pirates on the beach, robots on the water, a drone in the sky."],
                ["Buenaventura", "Today I pay what I owe! Men, the houses!"]],
    "ende_4": [["Holm", "Two days. The bay is ours for one more night. Mend what you can in the morning."],
               ["Casanova", "The paper was on the step again. It has a new line now: the same offer, and the pirates are gone. As if they were ever his to send away."],
               ["Casanova", "I lit the stove with it."], ["", "Pascal stands next to her while the paper burns, and looks away."]],
    "welle_5": [["Holm", "A heavy robot on the water, and a very big man on the beach who doesn't care about you at all. He wants the church. Stop him first."]],
    "bonaventure_gibt_auf": [["Buenaventura", "There are people in that house. Nobody told me there were people in that house."],
                             ["Buenaventura", "We rob ships. We do not burn grandmothers. Men! Torches out! Tell Mr. White he can keep his money."],
                             ["Buenaventura", "Clean money. White pays in clean money, like a bank. Ask yourself who has a bank."],
                             ["Holm", "The pirates are dropping their weapons. Finish the rest."]],
    "manoever_start": [["Holm", "The fishermen play the agents, and Unit-01 plays the robots. Nobody gets hurt today, and you cannot lose. Move a troop to a lit field, then attack."]],
    "manoever_ende": [["Holm", "Good enough. Now you know where it hurts."], ["Megan", "That's the first number that looks better than a hundred. Keep going, and I'll tell you the rest at the war council."]],
    "falscher_sieg": [["Maxwell", "Eish! Look at them run! Mr. Maximum is undefeated!"], ["Petru", "Hm."], ["Chiara", "Did we do it? Tell me we did it."],
                      ["Holm", "Stay at your places. I want to count them first. Nobody celebrates until I say so."]],
    "verrat": [["Pascal", "It ends tonight. I'm sorry. It ends tonight.", {"zu": [28, 9]}], ["Minicu", "Pascal? You sent me down here. Why is the north open?", {"zu": [29, 15]}],
               ["Alva", "Pascal, no. Close it! Close it!", {"zu": [23, 14]}], ["Mr. White", "Thank you. Now step aside.", {"zu": [28, 6]}],
               ["", "The Last Wave", {"art": "titel", "ober": "Day 23 · Sunset", "ziel": "Mr. White walks to the church. You lose if he gets there or you go down."}],
               ["Holm", "The north is open. Faen. That's the one side I wasn't worried about."],
               ["", "Alva has Pascal in her sights. The shotgun goes off.", {"zu": [23, 14]}],
               ["Holm", "She missed. Alva doesn't miss."],
               ["Holm", "...The quiet side. Megan tried to tell us."],
               ["Holm", "White is walking, and nothing stops him while the giant holds the gate. Everybody else, hold them off."]],
    # Pascal versteckt sich und kommt bei Minicus Sturz wieder (Duc 02.11.2026)
    "pascal_geht": [["Pascal", "I can't watch this. I can't."],
                    ["Holm", "Pascal just left the gate. He's gone in between the houses. I can't see him anymore. We don't have time to look for him."]],
    "danzel_flieht": [["Mr. White", "Danzel. Lovely stitching."], ["Danzel", "This isn't over! This is a – a tactical retreat!"], ["Holm", "Your tailor just left through a window."]],
    "alva_faellt": [["Mr. White", "The woman with the shotgun. Then the church."], ["Holm", "Alva's group is down. I can't see if they're moving. Duc, make a decision."]],
    "mochi": [["Bibi", "MOCHI?! That's my boy! That's my big stupid boy!"], ["Mr. White", "A pet. How sweet."], ["Bibi", "Not today!"],
              ["Holm", "Smoke on the square. The lion is gone. But White had to stop and wait."]],
    "mochi_allein": [["Holm", "A lion just came out of the scrub and went straight for White. I am not joking."], ["Mr. White", "A pet. How sweet."],
                     ["Holm", "It's hurt, and it's running. But White had to stop and wait."]],
    # Duc 02.11.2026, Drehbuch Abschnitt 6: Minicu spricht vor dem Schlag, Lola und Jana schreien, Siri drueckt Yasins Kamera runter,
    # Duc waehlt, Pascal kommt aus seinem Versteck, Casanova nennt ihn einen Verraeter. "wahl": Chips nur fuer die Chronik. Entwurf, unvertont.
    "minicu_faellt": [["", "White comes down the lane, slowly. Minicu steps into his way and lowers the axe.", {"zu": [29, 15]}],
                      ["Minicu", "You can't come in. Pascal said hold the gate.", {"gefuehl": "disapproval"}],
                      ["Minicu", "Does it hurt? When you do this? To people?", {"gefuehl": "confusion"}],
                      ["Mr. White", "No."],
                      ["Minicu", "Then I'm sorry for you.", {"gefuehl": "sadness"}],
                      ["", "One blow. Then only the sound of the axe on the stones."],
                      ["Holm", "He's down. One hit. Only one."],
                      ["Lola", "Minicu? MINICU! No, no, no, mate, get up – that's my Minicu, he eats all my leftovers, he –", {"gefuehl": "fear"}],
                      ["Jana", "Jessas – Minicu! Get up! Please get up, you said I don't have to say sorry –", {"gefuehl": "sadness"}],
                      ["", "Yasin has his camera on Minicu. Siri pushes it down, slowly."],
                      ["Siri", "Not like this. Not him.", {"gefuehl": "sadness"}],
                      ["", "Pascal comes out from between the houses and kneels next to him."],
                      ["Minicu", "Pascal. Did I hold it? Did I do good?", {"gefuehl": "sadness"}],
                      ["", "What do you do?", {"art": "wahl", "standard": 1, "optionen": [
                          {"text": "Kneels next to him first. “You held it, Minicu. You did good.”", "flag": "bl_minicu_duc_zuerst",
                           "dann": [["Duc", "You held it, Minicu. You did good."], ["Pascal", "...He did."]]},
                          {"text": "Waits.", "flag": "bl_minicu_gewartet", "dann": [["Pascal", "You did good, Minicu. You did so good."]]},
                          {"text": "Looks at Pascal. “Say it to him.”", "flag": "bl_minicu_sag_es",
                           "dann": [["Duc", "Say it to him."], ["Pascal", "You did good, Minicu. You did so good."]]}]}],
                      ["Pascal", "You gave me your word. Nobody gets hurt."],
                      ["Mr. White", "You didn't really think we'd hold back?"],
                      ["Casanova", "Pascal! You always clapped first! Every speech, every pause, you were the first! And you opened that gate!", {"gefuehl": "anger"}],
                      ["", "Pascal looks at her. He says nothing, and he follows White."],
                      ["", "A folded sheet has fallen out of Minicu's shirt pocket. MINICU at the top in a careful hand, and twice below it, crooked."],
                      ["Holm", "Frankfurt. The gate's open, and he's walking to the church. It's you now."]],
    # Nachtwache von Tag 22 steht neben ihm (Drehbuch Tag 22 Abend): diese Zeile kommt nach der ersten
    "minicu_nachtwache": [["Minicu", "You came. Thank you."]],
    "holm_ohne_wache": [["Holm", "I told you to send somebody. I should have told myself."]],
    # Kevin fliegt vom Tor, eine Runde bevor White kommt (Drehbuch Welle 6, Runde 4). Es gibt noch kein Bild von ihm, darum eine Zeile.
    "kevin_fliegt": [["", "On the gate, Kevin the seagull spreads his wings and flies away."]],
    "casanova": [["Casanova", "I will not hide in there while you fight on my square."], ["Mr. White", "Madame Mayor. What will you do, make a speech?"],
                 ["Duc", "He's right. We need you. In there, with them, standing up."], ["Casanova", "Then take this. It's the last one. Hit him hard."]],
    # Der dritte Gurt ist echt, nur fuer Bueros und Fabriken (Duc 01.11.2026). Six Sigma erlaubt 3,4 Fehler auf eine Million.
    "white_warnung_danzel": [["Danzel", "Duc! WAIT! I came back! Don't look at me! Before you walk over there, you must hear the terrible truth!"],
                             ["Duc", "Danzel, we're in the middle of a war."],
                             ["Danzel", "I saw that man's file at Alon's plant. I was not allowed to read it. So I read it twice."],
                             ["Danzel", "UFC champion! Eleven years! Nobody has ever come back for round two!"],
                             ["Duc", "He's in his fifties."],
                             ["Danzel", "THAT'S WHAT THE LAST ONE SAID!"],
                             ["Danzel", "A black belt in karate! A black belt in taekwondo! AND!"],
                             ["", "He stops. His knees are shaking."],
                             ["Danzel", "...a black belt in Six Sigma."],
                             ["Duc", "That's an office course. For factories."],
                             ["Danzel", "HE CUT WASTE IN THIS COMPANY BY FORTY PERCENT, DUC! DO YOU KNOW WHAT \"WASTE\" MEANS TO THAT MAN?!"],
                             ["Danzel", "I would come with you! But I have a rare illness. When I see a white suit, my legs leave. This isn't over! This is a –"],
                             ["", "He looks at the church, and his voice drops."],
                             ["Danzel", "No. Go. I'll hold the door. Just don't die, okay? I already made your funeral suit, and it's too good to use."],
                             ["Mr. White", "He's right about the belts. Six Sigma allows three point four errors in a million. You are one of them. I'm fixing it."]],
    # Megan ist seit dem Kriegsrat nicht mehr erreichbar (Duc 02.11.2026): Die Akte kam noch vorher an
    "white_warnung_holm": [["Holm", "Before you walk over there. Megan sent me a threat file on him, just before the screen went dark. You'll want to hear this."],
                            ["Holm", "UFC champion for eleven years, and nobody ever came back for round two. A black belt in karate, a black belt in taekwondo, and..."],
                            ["Holm", "...Six Sigma. I don't know why this is in the threat file."],
                            ["Duc", "That's an office course. For factories."],
                            ["Holm", "It says he cut waste in Alon's company by forty percent. Think about what that man calls waste."],
                            ["Mr. White", "I can hear your radio. The file is correct. Six Sigma allows three point four errors in a million. You are one of them. I'm fixing it."]],
    "sieg": [["Mr. White", "This is only a pause in the meeting."], ["Holm", "His people are carrying him off. They're leaving. All of them."],
             ["Holm", "Nobody can find Pascal. And I have no word on Alva's group yet."],
             ["Casanova", "Ring the bell. Ring it! Cala d'Orsu is still here."]],
    "verloren_kirche": [["Holm", "They're inside the church. Duc, it's over."]],
    "verloren_duc": [["Holm", "Duc is down. Nobody is holding them. It's over."]],
}
# Der Appell vor Ducs Kampf gegen White (Drehbuch Abschnitt 7): wer steht, antwortet, wer gefallen ist, bekommt Stille. Lola immer, aus der Kombuese.
APPELL = {"start": "All stations. Check in.", "ende": "Frankfurt. It's yours.", "stille": "Nothing on the radio.",
          "zeilen": {"maxwell": "Eish. Mr. Maximum is still standing, brother. Mr. Maximum is very angry.",
                     "chiara": "Still here! That's a nine, and I want it written down.",
                     "wolff": "Legion holds.", "elsa": "Section nine, present.",
                     "rosi": "Still standing, Officer. The big one isn't. If anybody tells Unit-01 I cried, they're next.",
                     "bibi": "Here! Ha! ...Still here.", "yamamoto": "Present, Officer-san. So sorry. Still alive."},
          "lola": "Galley, still here, Boss! Kettle's on. Come back and drink it.",
          "gefallen": ["alva", "minicu"]}
# Funk nach der Nacht (Drehbuch 5b, Zeilen von Character Design): die Frau der letzten Nacht funkt in der ersten Welle des Tages. 1 niedrig, 2 mittel, 3 hoch.
# voraus: ohne diese Leiter-Szene bleibt es bei der niedrigen Zeile.
FUNK = {"chiara": ["First Officer, your coffee is on the bridge. It's a six. Drink it anyway.",
                   "First Officer, keep your head down today. That's an order, and I don't care who outranks who.",
                   "Duc. First Officer. Come back in one piece. I'm still saving my ten."],
        "sophia": ["Duc, ten euros says you're back before dinner. Please don't make me lose.",
                   "Darling, I've kept your seat at breakfast. Nobody else is allowed it, so come back and sit in it.",
                   "Duc. I wrote one line last night, and you're in it. I'd like the chapter to go on."],
        "lea": ["Duc! Did you know an octopus has three hearts? So you've got no excuse. Come back.",
                "Two fingers, Duc. Stay together. You know what it means.",
                "Duc, I'm not saying anything clever today. Just come back. Proper come back."],
        "rosi": ["Officer, I checked your blade last night. If it breaks today, that's on you, not me.",
                 "Officer. Same time on the stopwatch, remember? Nobody's allowed to lose today.",
                 "Captain. ...Don't make me say it twice. Come back."],
        "siri": ["Duc? No camera today. I'm watching you with my own eyes, so be careful.",
                 "Duc, I'm not filming you. I want to remember this one myself.",
                 "Duc. In my own voice: please come back to me."],
        "lola": ["Boss? Come back for dinner. I mean it.",
                 "Boss, I've saved you the good bread. Mostly the good bread. Don't make me eat it alone.",
                 "Boss. I didn't burn breakfast this morning, not once. So come back and see what else I can do."],
        "alva": ["Duc, your tab is still open. Nobody leaves my bar with an open tab.",
                 "Duc. Nobody's mine, I keep saying it. Come back anyway.",
                 "Duc. I'll keep the light on over the bar. Don't make me turn it off."]}
FUNK_VORAUS = {"lea": "lea_zeichen", "rosi": "rm_r2"}
# Gefuehl je Zeile, damit der Redner zur Lage passt (Duc 02.11.2026: Holm war staendig neutral). Was eine Zeile selbst setzt, gilt weiter.
GEFUEHL = {'welle_1': ['neutral', 'disapproval'], 'w1_legion': ['pride'], 'w1_hund': ['fear'], 'w1_boote': ['surprise'], 'ende_1': ['disapproval', 'approval'], 'w2_elsa': ['pride'], 'w2_deck': ['anger'], 'w2_gewehr': ['curiosity'], 'w3_post': ['sadness'], 'w3_trio': ['nervousness'], 'w3_dach_leer': ['disappointment'], 'w3_pascal': ['nervousness', 'disapproval'], 'w4_1924': [None, None, 'pride', 'sadness', 'caring', 'surprise'], 'w4_allein': ['disappointment'], 'ligeia_singt': ['gratitude'], 'w5_schlange': ['confusion', 'amusement', 'sadness'], 'white_angebot': [None, 'neutral'], 'welle_2': ['annoyance'], 'ende_2': ['approval', 'disgust', 'pride', 'curiosity'], 'welle_3': ['surprise', 'pride', 'anger'], 'ende_3': ['surprise'], 'welle_4': ['anger', 'pride'], 'ende_4': ['approval', 'disgust', 'pride'], 'welle_5': ['fear'], 'bonaventure_gibt_auf': ['fear', 'anger', 'disgust', 'surprise'], 'manoever_start': ['neutral'], 'manoever_ende': ['approval', 'approval'], 'falscher_sieg': ['excitement', 'neutral', 'excitement', 'disapproval'], 'verrat': ['sadness', 'confusion', 'fear', 'neutral', None, 'anger', None, 'surprise', 'sadness', 'anger'], 'pascal_geht': ['sadness', 'disgust'], 'danzel_flieht': ['amusement', 'fear', 'annoyance'], 'alva_faellt': ['neutral', 'fear'], 'mochi': ['excitement', 'amusement', 'anger', 'surprise'], 'mochi_allein': ['surprise', 'amusement', 'sadness'], 'minicu_faellt': [None, 'disapproval', 'confusion', 'neutral', 'sadness', None, 'sadness', 'fear', 'sadness', None, 'sadness', None, 'sadness', None, 'sadness', 'neutral', 'anger', None, None, 'sadness'], 'minicu_nachtwache': ['gratitude'], 'holm_ohne_wache': ['disappointment'], 'casanova': ['anger', 'amusement', None, 'caring'], 'white_warnung_danzel': ['fear', None, 'nervousness', 'fear', None, 'fear', 'fear', None, 'fear', None, 'fear', 'embarrassment', None, 'caring', 'amusement'], 'white_warnung_holm': ['nervousness', 'neutral', 'confusion', None, 'disgust', 'amusement'], 'sieg': ['annoyance', 'surprise', 'sadness', 'pride'], 'verloren_kirche': ['sadness'], 'verloren_duc': ['fear']}
GEFUEHL_BRIEFING = {'1': [None, 'annoyance', 'neutral', 'pride', 'caring', 'curiosity', None, 'approval'], '2': [None, 'nervousness', 'anger', 'disapproval', 'curiosity', 'anger', 'approval'], '3': [None, 'pride', 'disgust', 'anger', 'sadness', 'curiosity', 'approval'], '4': [None, 'pride', 'anger', 'annoyance', 'anger', 'nervousness', 'approval'], '5': [None, 'nervousness', 'anger', 'fear', 'nervousness', 'neutral', 'pride', 'approval']}
GEFUEHL_FUNK = {'chiara': ['annoyance', 'caring', 'caring'], 'sophia': ['amusement', 'caring', 'caring'], 'lea': ['excitement', 'caring', 'caring'], 'rosi': ['annoyance', 'caring', 'caring'], 'siri': ['caring', 'caring', 'caring'], 'lola': ['caring', 'caring', 'caring'], 'alva': ['amusement', 'caring', 'caring']}
APPELL["gefuehl"] = {'start': 'pride', 'ende': 'pride', 'lola': 'caring', 'name': 'sadness', 'zeilen': {'maxwell': 'anger', 'chiara': 'pride', 'wolff': 'pride', 'elsa': 'pride', 'rosi': 'annoyance', 'bibi': 'nervousness', 'yamamoto': 'approval'}}
for _sid, _liste in GEFUEHL.items():
    for _i, _g in enumerate(_liste):
        if _g and _i < len(SZENEN[_sid]):
            _x = SZENEN[_sid][_i]
            if len(_x) < 3:
                _x.append({})
            _x[2].setdefault("gefuehl", _g)
for _nr, _liste in GEFUEHL_BRIEFING.items():
    for _i, _g in enumerate(_liste):
        _x = BRIEFING[_nr]["zeilen"][_i]
        if _g and _x.get("wer"):
            _x.setdefault("gefuehl", _g)
            if _x.get("sonst"):
                _x["sonst"].setdefault("gefuehl", _g)
for _pid, _zeilen in FUNK.items():
    for _i, _text in enumerate(_zeilen):
        SZENEN["funk_%s_%d" % (_pid, _i + 1)] = [[_pid.capitalize(), _text, {"gefuehl": GEFUEHL_FUNK[_pid][_i], "ton": "funk_rauschen"}]]
# Ton an einer Zeile (Duc 02.11.2026): die Karte spielt ihn, wenn die Zeile erscheint. Nur bestehende Effekte aus sfx.json.
# Szenen-Toene am Anfang (SZENE_TON in eden-tactics.js) bleiben, darum hier nie Zeile 0 einer Szene, die dort schon klingt.
TON = {"w1_legion": {0: "tk_schritte"}, "w1_hund": {0: "rudel_hunde"}, "w1_boote": {0: "tender_motor"},
       "w2_elsa": {0: "gun_reload"}, "w2_deck": {0: "tk_roboter"}, "w3_post": {0: "tk_haus_schreie"}, "w3_trio": {0: "kampf_granate_wasser"},
       "w3_pascal": {0: "funk_rauschen"}, "w4_1924": {0: "tk_glocke", 1: "tk_rudern"}, "ligeia_singt": {0: "tk_ligeia"}, "ende_4": {3: "tk_papier"}, "kevin_fliegt": {0: "tk_kevin"},
       "w5_schlange": {0: "tk_roboter"}, "white_angebot": {0: "funk_rauschen"},
       "bonaventure_gibt_auf": {2: "geld_ein"}, "verrat": {4: "tk_glocke", 6: "tk_flinte"}, "pascal_geht": {1: "tk_schritte"},
       "alva_faellt": {1: "tk_ko"},
       "minicu_faellt": {0: "tk_schritte", 5: "tk_minicu_fall", 9: "kamera_ausloeser", 18: "hinweis_gefunden"},
       "casanova": {3: "heilung"}, "white_warnung_holm": {0: "funk_rauschen", 5: "funk_rauschen"}}
for _sid, _toene in TON.items():
    for _i, _t in _toene.items():
        _x = SZENEN[_sid][_i]
        if len(_x) < 3:
            _x.append({})
        _x[2]["ton"] = _t
FUNK_LP = 0.10        # Duc hat am Tag nach einer Nacht bei einer Frau 10 % mehr Leben (Duc 02.11.2026)
NACHTWACHE = {"feld": [30, 15], "wer": ["wolff", "elsa", "yamamoto"]}     # Tag 22 abends in den Norden geschickt: steht in Welle 6 neben Minicu
RUDER_HAUS = "werkstatt"   # Petrus Werkstatt in Welle 3 gerettet: das Dorf rudert in Welle 4 schon bei einem Punkt weniger Ruf

# Hintergrund des echten Kampfs nach dem Feld des Gegners (Duc 01.11.2026), kern/taktik.py kampf_ort
# Eigene Bilder in golden hour, Buehnen-Perspektive, damit die Sprites stehen (werkzeuge/hintergrund_bild.py, siege_*)
ORTE = {o: "eden_rise_siege_%s.png" % o for o in ("yacht", "mole", "hafen", "strand", "macchia", "felsen", "dorf", "kirchplatz")}
# Duc kaempft im echten Bildschirm: Begegnungen nur fuer die Karte (kommen zur Laufzeit dazu, kaempfe.json bleibt unberuehrt)
AUSGANG = {"ko": {"text": "That one stays down.", "folgen": []}, "aufgabe": {"text": "They back away.", "folgen": []}, "entkommen": {"text": "They fall back.", "folgen": []},
           "flucht": {"text": "You back away.", "folgen": []}, "niederlage": {"text": "You go down.", "folgen": []}}


def begegnung(titel, feinde, level_plus, ziel="Hold the village", lp=None):
    b = {"title": titel, "goal": ziel, "image": "eden_rise_piazza_treppe.png", "enemy": feinde[0], "enemies": feinde, "level": "duc", "level_plus": level_plus,
         "flee_allowed": False, "flee_reason": "The church is behind you.", "outcomes": AUSGANG}
    if lp:
        b["lp_faktoren"] = lp
    return b


BEGEGNUNGEN = {"tk_hund": begegnung("A Dog in a Collar", ["hund_wild"], -2), "tk_agent": begegnung("Agent on the Square", ["agent"], -1), "tk_schuetze": begegnung("Agent with a Rifle", ["tk_schuetze"], -1), "tk_pirat": begegnung("Pirate with a Torch", ["fackelpirat", "pirat"], -1, lp=[1, 0.4]),
               "tk_gunner": begegnung("Pirate Gunner", ["tk_gunner", "pirat"], -1, lp=[1, 0.4]), "tk_brawler": begegnung("Pirate Brawler", ["tk_brawler", "pirat"], 0, lp=[1, 0.4]),
               "tk_bonaventure": begegnung("Captain Buenaventura", ["tk_bonaventure", "pirat"], 1, lp=[1, 0.4]), "tk_brute": begegnung("The Big One", ["brute_solo"], 0),
               "tk_roboter": begegnung("Boarding Robot", ["tk_robot"], -1), "tk_roboter_schwer": begegnung("Heavy Boarding Robot", ["tk_robot_schwer"], 1), "tk_drohne": begegnung("Combat Drone", ["hirtendrohne"], -1),
               "tk_kobra": begegnung("Cobra Robot", ["tk_kobra"], -1), "tk_skorpion": begegnung("Scorpion Robot", ["tk_skorpion"], -1),
               "tk_white": begegnung("Mr. White", ["tk_white"], 4, "Stop him before the church")}
# Gegner nur fuer die Karte, zur Laufzeit aus einer Vorlage. Fehlt der Kampf-Sprite noch, bleibt der der Vorlage.
VORLAGEN = {"tk_white": {"vorlage": "agent_fuehrer", "name": "Mr. White", "tier": "albtraum"},
            "tk_robot": {"vorlage": "unit01", "name": "Boarding Robot", "sprite": "BoardingRobot"},
            "tk_robot_schwer": {"vorlage": "unit01", "name": "Heavy Boarding Robot", "sprite": "BoardingRobotHeavy", "tier": "gefaehrlich"},
            "tk_kobra": {"vorlage": "unit01", "name": "Cobra Robot", "sprite": "RobotCobra", "boss": False, "attack": {"label": "Neck Blades", "icon": "⚙"},
                         "specials": {"w1": {"label": "Hot Oil Spray", "icon": "💨", "bonus": 0, "effect": "geblendet", "dodge_only": False},
                                      "s1": {"label": "Lunge", "icon": "⚙💥", "bonus": 6, "effect": None, "dodge_only": True}},
                         "immune": {"charm": "It looks at you with its one red eye. Whatever gives its orders isn't listening."}},
            "tk_skorpion": {"vorlage": "unit01", "name": "Scorpion Robot", "sprite": "RobotScorpion", "boss": False, "attack": {"label": "Pincers", "icon": "⚙"},
                            "specials": {"w1": {"label": "Tail Shock", "icon": "⚡", "bonus": 2, "effect": "strom", "dodge_only": False},
                                         "s1": {"label": "Tail Blade", "icon": "⚙💥", "bonus": 6, "effect": None, "dodge_only": True}},
                            "immune": {"charm": "It keeps walking. Whatever gives its orders isn't listening."}},
            "tk_schuetze": {"vorlage": "agent", "name": "Marksman", "sprite": "AgentGunman", "attack": {"label": "Rifle Shot", "icon": "🔫", "schuss": True},
                            "specials": {"w1": {"label": "Shock Grenade", "icon": "⚡", "bonus": 2, "effect": "strom", "dodge_only": False},
                                         "s1": {"label": "Long Burst", "icon": "🔫", "bonus": 7, "effect": None, "dodge_only": True, "schuss": True}}},
            "tk_gunner": {"vorlage": "pirat", "name": "Pirate Gunner", "sprite": "PirateGunner", "attack": {"label": "Pistol Shot", "icon": "🔫", "schuss": True},
                          "specials": {"w1": {"label": "Powder in the Eyes", "icon": "💥", "bonus": 0, "effect": "geblendet", "dodge_only": False},
                                       "s1": {"label": "Point Blank", "icon": "🔫", "bonus": 6, "effect": None, "dodge_only": True, "schuss": True}}},
            "tk_brawler": {"vorlage": "pirat", "name": "Pirate Brawler", "sprite": "PirateBrawler", "tier": "gefaehrlich"},
            "tk_bonaventure": {"vorlage": "pirat", "name": "Captain Buenaventura", "sprite": "Bonaventure", "tier": "toedlich"}}


# Was einzahlt (belagerung.md). Erste Zahlen, der Spieltest legt sie fest. Boden 30 %: nie zu leicht (Duc 01.11.2026).
VORBEREITUNG = {"boden": 30, "punkte": [
    {"text": "The manoeuvre showed you your weak spots", "abzug": 5, "bed": {"flag": "manoever_fertig"}},
    {"text": "Elsa has your back", "abzug": 5, "bed": {"flag": "elsa_hilft"}},
    {"text": "Rosi knows where robots break", "abzug": 5, "bed": {"wert": "vertrauen.rosi", "min": 2}},
    {"text": "Yamamoto will fight", "abzug": 5, "bed": {"wert": "vertrauen.yamamoto", "min": 2}},
    {"text": "The Red Trio stands with you", "abzug": 10, "bed": {"flag": "rt_ausgang_alle"}},
    {"text": "You already beat some of White's men", "abzug": 5, "bed": {"flag": "rt_white_agenten"}},
    {"text": "You kept the crate of collars", "abzug": 5, "bed": {"flag": "gr_kiste_genommen"}},
    {"text": "Ba Tu hears when they leave", "abzug": 5, "bed": {"wert": "vertrauen.batu", "min": 3}},
    {"text": "Don Anghjulu will ring the bell sober", "abzug": 5, "bed": {"wert": "vertrauen.anghjulu", "min": 3}},
    {"text": "The village will row out with you", "abzug": 10, "bed": {"wert": "ruf", "min": 5}},
    {"text": "Holm gives the orders", "abzug": 5, "bed": {"flag": "holm_zurueck"}},
    {"text": "Maxwell and Chiara have their new weapons", "abzug": 5, "bed": {"flag": "steel_mop"}},
]}
MANOEVER = {"feinde": [("agent", SUED[0]), ("agent", SUED[1]), ("hund", WEST[0]), ("agent", WEST[1]), ("roboter", OST[0])]}


def figuren_setzen(ordner):
    """Pixel-Blaetter aus taktik/figuren.json an die Einheiten haengen (werkzeuge/eden_rise/taktik_figuren.py)."""
    fig = json.load(open(os.path.join(ordner, "taktik", "figuren.json"), encoding="utf-8"))
    for tabelle in (TRUPPS, RESERVE, WEHR, FEINDE):
        for tid, q in tabelle.items():
            if tid in fig:
                q["figur"] = fig[tid]
    FEINDE["roboter_schwer"]["figur"] = fig.get("roboter_schwer") or fig["roboter"]     # bis Ducs eigenes Blatt da ist
    klein = dict(fig["roboter"], hoehe=120, stand=dict(fig["roboter"]["stand"], hoehe=116))   # Kobra und Skorpion: kleiner Roboter, bis ihre Blaetter da sind
    FEINDE["roboter_kobra"]["figur"] = fig.get("roboter_kobra") or klein
    FEINDE["roboter_skorpion"]["figur"] = fig.get("roboter_skorpion") or klein
    TRUPPS["duc"]["figur"] = fig["duc_erde"]
    TRUPPS["duc"]["figur_jacke"] = {"jacket_earth": fig["duc_erde"], "jacket_water": fig["duc_wasser"], "jacket_fire": fig["duc_feuer"], "jacket_air": fig["duc_luft"]}
    # Chiara traegt Danzels Dress Whites nur, wenn sie sie bekommen hat. Ohne Uniform-Blatt bleibt es vorerst Weiss.
    TRUPPS["chiara"]["figur"] = fig.get("chiara_uniform") or fig["chiara_whites"]
    TRUPPS["chiara"]["figur_flag"] = {"flag": "sn_dress_whites_fertig", "figur": fig["chiara_whites"], "set": "Dress Whites"}
    for vid, q in VORLAGEN.items():
        if q.get("sprite") and not os.path.isdir(os.path.join(ordner, "kampf", q["sprite"])):
            print("Kampf-Sprite fehlt noch:", q["sprite"])
            del q["sprite"]
    HILFE["danzel"]["einheit"]["figur"] = fig["danzel"]


def main():
    r = raster()
    assert len(r) == ZE and all(len(z) == SP for z in r)
    ordner = os.path.join(BASIS, "module", "eden_rise")
    figuren_setzen(ordner)
    d = {"orte": ORTE, "spalten": SP, "zeilen": ZE, "ausschnitt": GANZ, "raster": r, "barrikade": [[27, 8], [28, 8]], "barrikade_bild": {"box": [24.5, 5.75, 31.5, 11.75], "zu": "barrikade_zu.webp", "offen": "barrikade_offen.webp"}, "kirche": {"tueren": [[25, 15], [26, 15]], "lp": 3},
         "plaetze": PLAETZE, "gelaende": GELAENDE, "gang": GANG, "hilfe": HILFE, "sets": SETS, "fronten": {"South": SUED, "West": WEST, "Yacht": OST, "North": NORD}, "bilder": {"ruhig": "karte_ruhig.webp", "kampf": "karte_kampf.webp"},
         "yacht_lp": 3, "macht": MACHT, "duo": DUO, "rueckspruenge": 2, "bestand": BESTAND, "trupps": TRUPPS, "reserve": RESERVE, "trupps_max": 6, "trupps_klein": 4, "haeuser": HAEUSER, "wehr": WEHR, "feinde": FEINDE, "wellen": WELLEN, "szenen": SZENEN, "briefing": BRIEFING, "appell": APPELL, "funk": FUNK, "funk_voraus": FUNK_VORAUS, "funk_lp": FUNK_LP, "nachtwache": NACHTWACHE, "ruder_haus": RUDER_HAUS, "begegnungen": BEGEGNUNGEN, "vorlagen": VORLAGEN, "vorbereitung": VORBEREITUNG, "manoever": MANOEVER, "ruf_rudert": 5, "neustart_milde": 0.15, "neustart_milde_max": 3}
    ziel = os.path.join(BASIS, "module", "eden_rise", "taktik.json")
    json.dump(d, open(ziel, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("taktik.json:", sum(z.count(".") for z in r), "begehbare Felder,", len(WELLEN), "Wellen")


if __name__ == "__main__":
    main()
