# -*- coding: utf-8 -*-
"""Rettungen fuer Bibis Tierstation (Duc 01.11.2026, Wiki systeme/tierstation.md). Eingebunden von kaempfe_eden_rise.py.

Das Halsband macht die Tiere verrueckt und zieht an ihrer Kraft. Erst wenn das Tier erschoepft ist, kann die Schlafgranate gegen das Halsband gewinnen:
Duc kaempft es muede und wirft (kern/kampf.schlaf_chance). Grauzonen-Regel E-073: Hier stirbt nichts. Ein Schlag bei fast leeren LP = es ist weg, erneut am naechsten Tag.
schlaf_faktor = wie sehr das Halsband oberhalb von 10 % LP dagegenhaelt. Werte noch ungemessen (tests/expedition_sim.py)."""


def SP(label, icon, bonus=0, effect=None, dodge_only=False):
    return {"label": label, "icon": icon, "bonus": bonus, "effect": effect, "dodge_only": dodge_only}


IMMUN = {"charm": "It can't hear you over the collar.", "courage": "It can't be scared off. The collar won't let it run."}
FASSUNG = 3.0              # reden und drohen zaehlen hier nicht, nur die Granate setzt die Fassung auf 0

ENEMIES = {
    "mo_hund": {"name": "Collared Dog", "sprite": "Dog", "cls": "tier", "element": "erde", "tier": "laestig", "schlafbar": True, "schlaf_faktor": 1.0,
                "attack": {"label": "Bite", "icon": "🐕"}, "specials": {"s1": SP("Snaps at Your Hand", "🐕💥", bonus=2)},
                "pattern": ["n", "n", "s1"], "weakness": None, "fassung_faktor": FASSUNG,
                "immune": IMMUN, "parade": "sprite", "parade_ziel": 75},
    "mo_hyaene": {"name": "Ark Hyena", "sprite": "ArkHyena", "cls": "tier", "element": "erde", "tier": "gefaehrlich", "schlafbar": True, "schlaf_faktor": 0.9,
                  "attack": {"label": "Bite", "icon": "🐾"}, "specials": {"w1": SP("Laughs and Circles", "🐾", effect="ungedeckt"), "s1": SP("Goes for the Arm", "🩸", bonus=2, effect="blutend")},
                  "pattern": ["n", "w1", "n", "s1"], "weakness": None, "fassung_faktor": FASSUNG,
                  "immune": IMMUN, "parade": "sprite", "parade_ziel": 70},
    "mo_mufflon": {"name": "Plated Mouflon", "sprite": "PlatedMouflon", "cls": "tier", "element": "erde", "tier": "gefaehrlich", "schlafbar": True, "schlaf_faktor": 0.8,
                   "attack": {"label": "Horns", "icon": "🐏"}, "specials": {"w1": SP("Scrapes the Ground", "🐾", effect="ungedeckt"), "s1": SP("Ram", "🐏💥", bonus=5, dodge_only=True)},
                   "pattern": ["n", "w1", "s1"], "cls_kampf": "maschine", "weakness": None, "fassung_faktor": FASSUNG,
                   "immune": IMMUN, "parade": "sprite", "parade_ziel": 70},
    "mo_affe": {"name": "Collared Ape", "sprite": "Ape", "cls": "tier", "element": "erde", "tier": "gefaehrlich", "schlafbar": True, "schlaf_faktor": 0.8,
                "attack": {"label": "Grabs", "icon": "🐒"}, "specials": {"s1": SP("Throws a Stone", "🪨", bonus=4, dodge_only=True)},
                "pattern": ["n", "s1", "n"], "weakness": None, "fassung_faktor": FASSUNG,
                "immune": IMMUN, "parade": "sprite", "parade_ziel": 70},
    "mo_wolf": {"name": "Collared Wolf", "sprite": "Wolf", "cls": "tier", "element": "erde", "tier": "gefaehrlich", "schlafbar": True, "schlaf_faktor": 0.7,
                "attack": {"label": "Bite", "icon": "🐺"}, "specials": {"w1": SP("Circles You", "🐾", bonus=3), "s1": SP("Goes for the Throat", "🐺💥", bonus=5, effect="blutend")},
                "pattern": ["n", "w1", "n", "s1"], "weakness": None, "fassung_faktor": FASSUNG,
                "immune": IMMUN, "parade": "sprite", "parade_ziel": 75},
}


def TIER(name, sprite, tier, faktor, biss, icon, specials, pattern, **extra):
    return dict({"name": name, "sprite": sprite, "cls": "tier", "element": "erde", "tier": tier, "schlafbar": True, "schlaf_faktor": faktor,
                 "attack": {"label": biss, "icon": icon}, "specials": specials, "pattern": pattern, "weakness": None, "fassung_faktor": FASSUNG,
                 "immune": IMMUN, "parade": "sprite", "parade_ziel": 70}, **extra)


# Zweite Runde (Duc 01.11.2026). Jeder Kampf soll sich anders anfuehlen: flink, zaeh, aus der Luft, langsam und boese.
ENEMIES.update({
    "mo_madame": TIER("Very Round Cat", "RussianBlue", "laestig", 1.0, "Claws", "🐈", {"s1": SP("Lands on You", "🐈💥", bonus=3, dodge_only=True)}, ["n", "n", "s1"], parade_ziel=75),
    "mo_rotpanda": TIER("Collared Red Panda", "RedPanda", "laestig", 1.0, "Claws", "🐾", {"w1": SP("Stands Up, Arms High", "🐾", effect="ungedeckt"), "s1": SP("Drops on You", "🐾💥", bonus=2)}, ["n", "w1", "s1"], parade_ziel=75),
    "mo_capybara": TIER("Collared Capybara", "Capybara", "gefaehrlich", 1.0, "Teeth", "🦷", {"s1": SP("Charges", "💥", bonus=4, dodge_only=True)}, ["n", "n", "n", "s1"]),
    "mo_keiler": TIER("Collared Boar", "WildschweinKeiler", "gefaehrlich", 0.9, "Tusks", "🐗", {"w1": SP("Scrapes the Ground", "🐾", effect="ungedeckt"), "s1": SP("Charge", "🐗💥", bonus=5, dodge_only=True)}, ["n", "w1", "s1"]),
    "mo_baerchen": TIER("Bear Cub", "BearCub", "laestig", 1.0, "Swipe", "🐾", {"s1": SP("Bluff Charge", "🐾💥", bonus=2)}, ["n", "n", "s1"], parade_ziel=75),
    "mo_schildkroete": TIER("Very Old Tortoise", "Tortoise", "gefaehrlich", 0.8, "Bite", "🐢", {"w1": SP("Pulls Into Her Shell", "🐢"), "s1": SP("Shell Slam", "🐢💥", bonus=4)}, ["n", "w1", "w1", "s1"], cls_kampf="maschine"),
    "mo_geier": TIER("Collared Vulture", "BeardedVulture", "gefaehrlich", 0.8, "Talons", "🪶", {"w1": SP("Climbs Out of Reach", "🪶", effect="ungedeckt"), "s1": SP("Stoop From Above", "🪶💥", bonus=6, dodge_only=True)}, ["n", "w1", "s1"], cls="flieger"),
    "mo_schneeleopard": TIER("Collared Snow Leopard", "SnowLeopard", "gefaehrlich", 0.7, "Claws", "🐆", {"w1": SP("You Lose Sight of Her", "🐾", bonus=3), "s1": SP("Leap", "🐆💥", bonus=6, effect="blutend", dodge_only=True)}, ["w1", "n", "s1"], parade_ziel=65),
    "mo_waran": TIER("Collared Komodo Dragon", "Komodo", "gefaehrlich", 0.7, "Bite", "🦎", {"w1": SP("Waits", "🦎", effect="ungedeckt"), "s1": SP("Tail Sweep", "🦎💥", bonus=5, dodge_only=True), "s2": SP("Patient Bite", "🩸", bonus=2, effect="blutend")}, ["w1", "s2", "n", "s1"]),
})
DROPS = {}


def _r(titel, bild, gegner, schlaeft, weg, nieder):
    """Keine Stufe darf Duc weit davonlaufen: Level folgt ihm. Ausgang "aufgabe" = die Granate wirkt, alles andere = es ist weg."""
    flag = "mo_%s_ruhig" % gegner[3:]
    return {"title": titel, "goal": "Wear it down, then throw the Sleep Grenade", "image": "eden_rise_%s.png" % bild, "enemy": gegner, "level": "duc", "flee_allowed": True,
            "outcomes": {"aufgabe": {"text": schlaeft, "folgen": [{"flag": flag}]},
                         "ko": {"text": weg, "folgen": []}, "entkommen": {"text": weg, "folgen": []},
                         "flucht": {"text": "You back away, slowly. It watches you all the way.", "folgen": []},
                         "niederlage": {"text": nieder, "folgen": []}}}


ENCOUNTERS = {
    "mochis_hund": _r("A Dog on the Road", "macchia_path", "mo_hund", "The collar blinks fast, then slow. The dog sits down in the road, puts its head on your boot and sleeps.",
                      "You hit it once too often. It runs off on three legs with the collar still blinking. You did that.", "Teeth, the road, Bibi's voice from far away. She gets you home."),
    "mochis_hyaene": _r("Laughter in the Gorge", "bone_gorge", "mo_hyaene", "The laughing gets slower and stops. She lies down with her chin on the stones, and for once her face is quiet.",
                        "You hit her once too often. She goes up the rocks, still laughing. It sounds worse from far away.", "She's faster than you. Bibi's water grenade is the last thing you hear."),
    "mochis_mufflon": _r("Steel on the Ridge", "charcoal_road", "mo_mufflon", "She goes down on her knees very slowly, as if it was her own idea. Then her head comes down onto the road.",
                         "One hit too many. She turns and walks into the trunks with the collar still blinking. You won't catch her today.", "It's like being hit by a door. Bibi drags you out by the jacket."),
    "mochis_affe": _r("Something Is Watching", "forest_edge_cliffs", "mo_affe", "He catches the grenade and looks at it. It goes off in his hand. He sits down, very politely, and falls asleep.",
                      "One hit too many. He's up the cliff before you can blink. A stone lands next to your foot, on purpose.", "The last stone was a good one. Bibi walks you home, very slowly."),
    "mochis_wolf": _r("The Grey One Alone", "high_pasture", "mo_wolf", "She fights the sleep for a long time, on her feet, looking at you. Then she lies down and the light on the collar goes slow.",
                      "One hit too many. She's gone over the ridge. There's blood on the grass, and you are the reason.", "She knew exactly what she was doing. Bibi gets you down the hill."),
}

ENCOUNTERS.update({
    "mochis_madame": _r("A Very Round Problem", "shepherd_hut_ruin", "mo_madame", "She sits down in the middle of her own fury and looks surprised. Then she's asleep, with her chin on her front paws.",
                        "One hit too many. She goes under the hut faster than anything that shape should move. You hear her up there all evening.", "You got beaten by a cat. Bibi will never mention it. She'll just smile."),
    "mochis_rotpanda": _r("Something Red in the Trees", "forest_edge_cliffs", "mo_rotpanda", "He's still standing with both arms up when the grenade works. He stays like that for a moment. Then he tips over, very slowly.",
                          "One hit too many. He goes up the trunk and away through the branches, with the light still blinking.", "Small claws, a lot of them, right in the face. Bibi cleans you up and says nothing."),
    "mochis_capybara": _r("The Calmest Animal There Is", "macchia_creek_bridge", "mo_capybara", "All the rage goes out of him at once. He walks into the creek, sits down in it and falls asleep with his nose above the water.",
                          "One hit too many. He crashes away along the creek. It's strange how much that hurts to watch.", "He doesn't stop. He just keeps walking through you. Bibi gets you out of the water."),
    "mochis_keiler": _r("Another Collar in the Macchia", "ravine_fork", "mo_keiler", "His legs fold under him one by one. He goes down like a wall coming down, and the whole ravine is quiet.",
                        "One hit too many. He crashes back into the undergrowth, and you can hear him for a long time.", "It's like being hit by a car, and you remember that it was like that the last time, too. Bibi drags you clear."),
    "mochis_baerchen": _r("Something Small, Again", "forest_edge_cliffs", "mo_baerchen", "It wobbles, sits down, and falls over onto its side. It's asleep before it lands. Bibi is already there.",
                          "One hit too many. It runs into the alders, crying. Nothing answers now.", "You trip over a root. When you get up, it's gone, and your dignity with it."),
    "mochis_schildkroete": _r("Number Twelve", "macchia_path", "mo_schildkroete", "Her head comes down very slowly, and it takes a full minute to reach the ground. You stand there and wait. It seems polite.",
                              "One hit too many. She shuts herself in her shell and won't come out, so you leave. Next morning she's gone. Nobody knows how.", "It's hard to explain how you lost this fight. Bibi doesn't ask you to."),
    "mochis_geier": _r("Over the Ridge", "foggy_ridge", "mo_geier", "He lands badly and folds up, one huge wing at a time. His eye closes last. Up close, he's bigger than you thought.",
                       "One hit too many. He beats away into the fog with the collar blinking, and you lose him in three seconds.", "You never saw that one coming. You had the sky behind you. Bibi walks you down."),
    "mochis_schneeleopard": _r("Tracks and Nothing Else", "ravine_fork", "mo_schneeleopard", "She fights it on her feet for longer than anything should. Then she lies down on the rock, with her long tail around her, as if that's what she had meant to do.",
                               "One hit too many. You look up and she isn't there. She was never there. There's only a little blood on the stone.", "You didn't see any of it. You just wake up, with Bibi's hand on your face."),
    "mochis_waran": _r("Something Long in the Sun", "bone_gorge", "mo_waran", "He stops. He looks at the collar, somehow, and then at you. He lays his head on a warm stone and closes his eyes, as if he had decided to.",
                       "One hit too many. He leaves. He doesn't run. He just walks away, and for some reason you don't follow him.", "It's only a small bite. You feel fine, and then you don't feel anything. Bibi knows what to do, thank God."),
})
