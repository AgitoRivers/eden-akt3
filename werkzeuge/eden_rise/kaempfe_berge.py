# -*- coding: utf-8 -*-
"""Gegner und Begegnungen des Ortskapitels Berge (Akt 2, Duc 27.10.2026) - eingebunden von kaempfe_eden_rise.py.

Story: ereignisse_berge.py, Wiki docs/wiki/welt/ortskapitel_berge.md. Level 3-6 (das Kloster laeuft flach 1-3).
Freie Waffenwahl: Le Large (Feuer) lohnt sich gegen alle Tiere (Erde) und haelt die grossen auf Abstand (Stange:
Gegner trifft mit -2); die Agenten sind Technik (Luft) und fallen mit Terremoto (Erde).
Grauzonen-Regel E-073: Tiere fliehen, Agenten duerfen fallen. Das Baerenjunge flieht sofort (flee_at 1.0).
Sprites liegen in module\\eden_rise\\kampf; Wolff und BearCub bestellt (27.10.), bis dahin AgentAlpha/Grizzly."""
import os

IMAGES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "module",
                      "eden_rise", "kampf")


def _sprite(wunsch, ersatz):
    return wunsch if os.path.isfile(os.path.join(IMAGES, wunsch, "idle.webp")) else ersatz


def SP(label, icon, bonus=0, effect=None, dodge_only=False, linger=0):
    sp = {"label": label, "icon": icon, "bonus": bonus, "effect": effect, "dodge_only": dodge_only}
    if linger:
        sp["linger"] = linger                     # a full hit lasts this many rounds longer
    return sp


NO_TALK = {"charm": "Animals don't understand you."}
TIER = dict(NO_TALK, courage="It is past being afraid of you.")

ENEMIES = {
    "bache": {
        "name": "Wild Sow", "sprite": "Wildschwein", "cls": "tier", "element": "erde", "tier": "gefaehrlich",
        "attack": {"label": "Tusks", "icon": "🐗"},
        "specials": {"w1": SP("Squeal", "💨", effect="geschwaecht"), "s1": SP("Defends Her Young", "🐗💥", bonus=7)},
        "weakness": None, "flee_at": 0.3, "parade": "sprite", "immune": dict(TIER), "parade_ziel": 60},
    "wolf": {
        "name": "Collared Wolf", "sprite": "Wolf", "cls": "tier", "element": "erde", "tier": "gefaehrlich",
        "attack": {"label": "Bite", "icon": "🐺"},
        "specials": {"w1": SP("Circles You", "🐾", bonus=3), "s1": SP("Goes for the Throat", "🐺💥", bonus=7,
                                                                       effect="blutend")},
        "weakness": "courage", "flee_at": 0.25, "parade": "sprite", "immune": dict(NO_TALK), "parade_ziel": 75},
    "wolf_alpha": {
        "name": "The Grey Wolf", "sprite": "WolfAlpha", "cls": "tier", "element": "erde", "tier": "gefaehrlich",
        "attack": {"label": "Bite", "icon": "🐺"},
        "specials": {"w1": SP("Howl", "🌕", effect="erschuettert"), "s1": SP("Leaps from the Bridge Rope", "🐺💥",
                                                                             bonus=8)},
        "weakness": None, "flee_at": 0.2, "parade": "sprite", "immune": dict(TIER), "parade_ziel": 70},
    "agent": {
        "name": "A.V. Agent", "sprite": "Agent", "cls": "mensch", "element": "luft", "tier": "gefaehrlich",
        "attack": {"label": "Baton", "icon": "🕴"},
        "specials": {"w1": SP("Shock Grenade", "⚡", bonus=2, effect="strom"), "s1": SP("Draws the Pistol", "🔫", bonus=7,
                                                                             dodge_only=True)},
        "weakness": "perception", "parade": "sprite", "immune": {}, "parade_ziel": 70},
    # Mehrgegner (Duc 29.10.2026): keine Sammel-Gegner mehr. Der Gruppenfuehrer wirft Blendgranaten, der Wasser-Agent
    # macht nass - und sein Partner (ein normaler Agent) hat die Schockgranate. Die Kombo entsteht von selbst.
    "agent_fuehrer": {
        "name": "A.V. Team Leader", "sprite": "AgentAlpha", "cls": "mensch", "element": "luft", "tier": "gefaehrlich",
        "attack": {"label": "Baton", "icon": "🕴"},
        "specials": {"w1": SP("Flash Grenade", "💥", effect="geblendet"), "s1": SP("Draws the Pistol", "🔫", bonus=7,
                                                                                  dodge_only=True)},
        "weakness": "perception", "parade": "sprite", "immune": {}, "parade_ziel": 70},
    "agent_nass": {                               # Umweg U2: water grenade, then the partner's shock (28.10.2026)
        "name": "A.V. Agent with Lamps", "sprite": "AgentAlpha", "cls": "mensch", "element": "luft",
        "tier": "gefaehrlich", "attack": {"label": "Baton", "icon": "🕴"},
        "specials": {"w1": SP("Water Grenade", "💧", effect="nass", linger=1)},
        "weakness": "perception", "parade": "sprite", "immune": {}, "parade_ziel": 70},
    "brute_solo": {
        "name": "The Big Man", "sprite": "BruteAlpha", "cls": "mensch", "element": "erde", "tier": "toedlich",
        "attack": {"label": "Fist", "icon": "👊"},
        "specials": {"w1": SP("Grabs You", "✊", bonus=3, effect="erschuettert"), "s1": SP("Throws You at the Wall",
                                                                                         "💥", bonus=9)},
        "weakness": "cunning", "parade": "sprite", "boss": True,
        "immune": {"courage": "He has never been afraid of anything smaller than himself."}, "parade_ziel": 65},
    "wolff": {
        "name": "Sergent Wolff", "sprite": _sprite("Wolff", "AgentAlpha"), "cls": "mensch", "element": None,
        "tier": "toedlich", "attack": {"label": "Long Sword", "icon": "🗡"},
        "specials": {"w1": SP("Service Regulations", "📕", effect="geschwaecht"), "s1": SP("Thirty Years of Drill",
                                                                                         "🎖💥", bonus=9)},
        "weakness": "empathy", "flee_at": 0.35, "parade": "sprite", "boss": True,
        "immune": {"courage": "Wolff almost smiles. “I was shouted at by better men than you in Castelnaudary.”"},
        "parade_ziel": 75},
    "wolff_hart": {
        "name": "Sergent Wolff", "sprite": _sprite("Wolff", "AgentAlpha"), "cls": "mensch", "element": None,
        "tier": "toedlich", "attack": {"label": "Long Sword", "icon": "🗡"},
        "specials": {"w1": SP("He Remembers Your Lies", "📕", bonus=2, effect="geschwaecht"),
                     "s1": SP("Thirty Years of Drill", "🎖💥", bonus=11)},
        "weakness": None, "parade": "sprite", "boss": True,
        "immune": {"courage": "“You lied to me twice. Don't try to frighten me now.”",
                   "charm": "“No. Not from you. Not any more.”"}, "parade_ziel": 70},
    "baer_junges": {
        "name": "Bear Cub", "sprite": _sprite("BearCub", "Grizzly"), "cls": "tier", "element": "erde",
        "tier": "laestig", "attack": {"label": "Swipe", "icon": "🐾"}, "specials": {},
        "weakness": None, "flee_at": 1.0, "parade": "skala", "immune": dict(NO_TALK), "parade_ziel": 75},
    "old_grey": {
        "name": "Old Grey", "sprite": "GrizzlyAlpha", "cls": "tier", "element": "erde", "tier": "toedlich",
        "attack": {"label": "Claws", "icon": "🐻"},
        "specials": {"w1": SP("Roar", "🐻", effect="erschuettert"), "s1": SP("Charge", "🐻💥", bonus=10,
                                                                           effect="blutend")},
        "weakness": None, "parade": "sprite", "boss": True, "immune": dict(TIER), "parade_ziel": 60},
    "panther": {
        "name": "The Black Beast", "sprite": "PantherAlpha", "cls": "tier", "element": "erde", "tier": "toedlich",
        "attack": {"label": "Claws", "icon": "🐆"},
        "specials": {"w1": SP("Vanishes into the Dark", "🌑", bonus=3, dodge_only=True),
                     "s1": SP("Leaps", "🐆💥", bonus=9, effect="blutend")},
        "weakness": None, "parade": "sprite", "boss": True, "immune": dict(TIER), "parade_ziel": 80},
}

# Chips der Halsbaender und der Agenten-Technik (Upgrades, Duc: "gerne auch Upgrades verteilen")
DROPS = {"bache": ["erholung", 1], "wolf": ["ausdauer", 2], "wolf_alpha": ["konter", 2], "agent": ["praezision", 2],
         "agent_fuehrer": ["scout", 3], "agent_nass": ["scout", 3], "brute_solo": ["schutz", 3],
         "old_grey": ["wucht", 3], "panther": ["zustand_blutend", 2]}


def OUT(text, *folgen):
    return {"text": text, "folgen": list(folgen)}


def _b(titel, ziel, bild, gegner, level, aus, flucht=True, grund=None, niederlage=True, extra=None):
    b = {"title": titel, "goal": ziel, "image": "eden_rise_%s.png" % bild, "enemy": gegner, "level": level,
         "flee_allowed": flucht, "expedition_niederlage": niederlage,
         "outcomes": {"ko": OUT(aus[0]), "aufgabe": OUT(aus[1]), "entkommen": OUT(aus[2]),
                      "flucht": OUT("You back away."), "niederlage": OUT(aus[3])}}
    if grund:
        b["flee_reason"] = grund
    b.update(extra or {})
    return b


ENCOUNTERS = {
    "berge_1_bache": _b("The Sow on the Switchbacks", "Get past her without hurting the young", "chestnut_switchbacks",
                        "bache", 2, ("The sow grunts, rounds up her piglets and crashes off downhill.",
                                     "She turns and herds her young into the chestnuts.",
                                     "The sow and her piglets are gone between the trees.",
                                     "She hits you at the knees. The chestnuts spin, and everything goes black.")),
    "berge_4_wolf": _b("A Wolf Below the Tower", "Get past the wolf on the ledge", "genoese_tower_camp", "wolf", 3,
                       ("The collar snaps. The wolf stares at it, then lopes off along the cliff.",
                        "The wolf backs away, tail low, and slips over the edge onto a lower path.",
                        "The wolf is gone, grey into grey.",
                        "Teeth, rock, sky. Everything goes black."), flucht=False,
                       grund="The ledge is too narrow to turn round."),
    "berge_5_affe": _b("An Ape at the Lake", "Get to the shore", "mountain_lake", "affe", 3,
                       ("The collar breaks with a crack. The ape splashes off through the shallows.",
                        "The ape tears off its collar and flees into the rocks.",
                        "The ape is gone, up the scree faster than you could ever climb it.",
                        "A rock, the water, cold. Everything goes black.")),
    "berge_7_agent": _b("A Man in Black", "Get past the agent", "foggy_ridge", "agent", 3,
                        ("The agent goes down in the wet grass and stays there.",
                         "He raises both hands and backs into the fog.",
                         "He's gone, swallowed by the fog.",
                         "A grenade, a spasm, the ground. Everything goes black.")),
    "berge_8_agenten": _b("Two on the Ridge", "Take the radio", "foggy_ridge", "agent_fuehrer", 4,
                          ("The second agent drags the first one away into the fog. The radio stays behind.",
                           "They back off together, guns lowered, and disappear.",
                           "They're gone. The radio is still hissing in the grass.",
                           "A white flash, then a baton. Everything goes black.")),
    "berge_9_wolf_alpha": _b("The Grey Wolf at the Bridge", "Cross the rope bridge", "foggy_ridge", "wolf_alpha", 3,
                             ("The collar falls into the gorge, blinking all the way down. The wolf turns and goes.",
                              "The grey wolf lowers its head and slips past you into the trees.",
                              "The wolf is gone into the dark on the other side.",
                              "The bridge swings, the wolf hits, and everything goes black."), flucht=False,
                             grund="You're in the middle of a rope bridge."),
    "berge_u1_hunde": _b("Dogs on the Goat Path", "Drive the dogs off", "ravine_fork", "hund_wild", 3,
                         ("The dogs yelp and scatter down the slope.", "They give up the goats and slink away.",
                          "Both dogs bolt.", "They come from both sides. Everything goes black.")),
    "berge_u1_junges": _b("Something Small", "Don't hurt it", "forest_edge_cliffs", "baer_junges", 5,
                          ("The cub tumbles over, squeals, and runs back into the alders.",
                           "The cub turns and scrambles away, squealing for its mother.",
                           "The cub bolts into the bushes, crying. Somewhere deeper in, something big answers.",
                           "You trip over a root. When you get up, the cub is gone."), niederlage=False),
    "berge_u1_old_grey": _b("Old Grey", "Face the bear", "lion_den_cave", "old_grey", 4,
                            ("Old Grey goes down on her side and stays down, breathing like a bellows.",
                             "She sinks down in front of her cubs. She doesn't get up again.",
                             "She drags herself back into the dark, to the crying.",
                             "She comes out of the dark like a falling wall. Everything goes black."), flucht=False,
                            grund="She is between you and the light."),
    "berge_u2_agenten": _b("Lights on the Ridge", "Take the controller", "berge_rotes_licht", "agent_nass", 3,
                           ("One agent lies still. The other runs, and drops the grey handset.",
                            "They throw down the lamps and run into the dark.",
                            "Their lights go out one by one, further and further away.",
                            "Red light, then nothing. Everything goes black.")),
    "berge_u2_hunde": _b("The Pack", "Stand in their way", "ravine_fork", "hund_alpha", 4,
                         ("The lead dog yelps and the pack breaks up into the dark.",
                          "The pack turns aside and loses the scent.",
                          "They're gone, barking further and further down the ravine.",
                          "Teeth from every side. Everything goes black.")),
    "berge_u2_panther": _b("The Black Beast", "End the hunt", "hidden_rock_niche", "panther", 4,
                           ("The panther sinks down and lies still, breathing, waiting.",
                            "It lies down at your feet as if it had decided something.",
                            "It drags itself back into the crack in the rock.",
                            "It comes out of the dark without a sound. Everything goes black."), flucht=False,
                           grund="It's faster than you."),
    "berge_12_wolff": _b("Sergent Wolff", "Make him look at the pictures", "bergerie_dusk_exterior", "wolff", 5,
                         ("Wolff goes down on one knee, breathing hard, and holds up a hand. Enough.",
                          "Wolff steps back and lowers the sword. “Enough. Show me.”",
                          "Wolff steps back and lowers the sword. “Enough. Show me.”",
                          "He puts you down the way thirty years of drill put people down."), flucht=False,
                         grund="Not in front of his men.", niederlage=False),
    "berge_12_wolff_hart": _b("Sergent Wolff", "Make him look at the pictures", "bergerie_dusk_exterior",
                              "wolff_hart", 6,
                              ("Wolff goes down and stays down a long time before he holds up a hand.",
                               "Wolff spits, steps back and lowers the sword. “Show me, then. Liar.”",
                               "Wolff spits, steps back and lowers the sword. “Show me, then. Liar.”",
                               "He doesn't stop until you stop moving."), flucht=False,
                              grund="Not in front of his men.", niederlage=False),
}
for _id in ("berge_12_wolff", "berge_12_wolff_hart"):         # verloren = wie Weg A (naechster Besuch: bg_wolff_verloren)
    ENCOUNTERS[_id]["outcomes"]["niederlage"]["folgen"] = [{"flag": "bg_wolff_niederlage"}]
for _ag, _gegner in (("duo", "brute_solo"), ("trio", "brute_solo"), ("solo", "brute_solo")):   # Gruppen: kaempfe_eden_rise.py
    for _baer in (False, True):
        ENCOUNTERS["berge_11_%s%s" % (_ag, "_baer" if _baer else "")] = _b(
            "Nightfall at the Bergerie", "Hold the door", "bergerie_dusk_exterior", _gegner,
            4 - (1 if _baer else 0) + (1 if _ag == "trio" else 0),
            ("The big man goes down like a tree. The others drag him away into the dark.",
             "They pick up the big man between them and retreat down the slope.",
             "They run, leaving a trail of torn black cloth in the thorns.",
             "The door, the wall, the floor. Everything goes black."), flucht=False,
            grund="Adrien can't run, and Laetitia won't.")
