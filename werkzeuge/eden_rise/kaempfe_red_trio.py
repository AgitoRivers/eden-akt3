# -*- coding: utf-8 -*-
"""Gegner und Begegnungen der Nebenquest "The Red Trio" (Duc 30.10.2026). Eingebunden von kaempfe_eden_rise.py.

Story: ereignisse_red_trio.py, Wiki docs/wiki/welt/nebenquest_red_trio.md. Werte aus tests/expedition_sim.py. Das Trio greift an, sobald es Duc sieht; weiter geht es nur nach einem Sieg, ko und Reden
setzen je ein eigenes Flag fuer den Satz danach."""


def SP(label, icon, bonus=0, effect=None, dodge_only=False):
    return {"label": label, "icon": icon, "bonus": bonus, "effect": effect, "dodge_only": dodge_only}


NO_TALK = {"charm": "Animals don't understand you."}
TIER = dict(NO_TALK, courage="It is past being afraid of you.")

ENEMIES = {
    "rt_bibi": {
        "name": "Bibi", "sprite": "Bibi", "cls": "mensch", "element": "wasser", "tier": "gefaehrlich",
        "attack": {"label": "Grenade", "icon": "💣"},
        "specials": {"w1": SP("Flash Grenade", "💥", effect="geblendet"), "w2": SP("Water Grenade", "💧", effect="nass"),
                     "s2": SP("Frag Grenade", "💣", bonus=4), "s1": SP("Nervous Laugh", "😂💣", bonus=6)},
        # Duc 30.10.2026: water, then Charly's Full Charge in the same round = Short Circuit. Alone the water does little,
        # so she throws frag instead. Offsets: Bibi stands directly before Charly in both fights (schritt = position).
        "pattern": ["n", "w2", "w1", "s1"], "pattern_allein": ["n", "s2", "w1", "s2", "s1"],
        "weakness": "perception", "parade": "sprite", "immune": {}, "parade_ziel": 70, "armor_plus": 1, "unterbrechbar": "s1"},
    "rt_charly": {
        "name": "Charly", "sprite": "Charly", "cls": "mensch", "element": "luft", "tier": "gefaehrlich",
        "attack": {"label": "Taser", "icon": "⚡"},
        "specials": {"w1": SP("Three out of Ten", "📉", effect="geschwaecht"), "s1": SP("Full Charge", "⚡💥", bonus=6, effect="strom")},
        "pattern": ["n", "w1", "s1", "n"],
        "weakness": "cunning", "parade": "sprite", "immune": {}, "parade_ziel": 70, "armor_plus": 1},
    "rt_danzel": {
        "name": "Danzel", "sprite": "Danzel", "cls": "mensch", "element": "luft", "tier": "gefaehrlich",
        "attack": {"label": "Baton", "icon": "🕴"},
        "specials": {"w1": SP("Tactical Retreat", "💨", dodge_only=True), "s1": SP("Eyes Shut, Full Swing", "🕴💥", bonus=5)},
        "weakness": "courage", "parade": "sprite", "immune": {}, "parade_ziel": 70, "armor_plus": 1},
    "panzer_mufflon": {
        "name": "Plated Mouflon", "sprite": "PlatedMouflon", "cls": "tier", "element": "erde", "tier": "gefaehrlich",
        "attack": {"label": "Horns", "icon": "🐏"},
        "specials": {"w1": SP("Scrapes the Ground", "🐾", effect="ungedeckt"), "s1": SP("Ram", "🐏💥", bonus=5, dodge_only=True)},
        "pattern": ["n", "w1", "s1"], "cls_kampf": "maschine",
        "weakness": "courage", "immune": dict(TIER), "parade": "sprite", "parade_ziel": 70},
    "ark_hyaene": {
        "name": "Ark Hyena", "sprite": "ArkHyena", "cls": "tier", "element": "erde", "tier": "gefaehrlich",
        "attack": {"label": "Bite", "icon": "🐾"},
        "specials": {"w1": SP("Flanks You", "🐾", effect="ungedeckt"), "s1": SP("Goes for the Throat", "🩸", bonus=2, effect="blutend")},
        "pattern": ["n", "n", "w1", "n", "n", "s1"],
        "weakness": "courage", "immune": dict(TIER), "parade": "sprite", "parade_ziel": 70},
    "ark_hyaene_alpha": {
        "name": "Ark Hyena Alpha", "sprite": "ArkHyena", "cls": "tier", "element": "erde", "tier": "gefaehrlich",
        "attack": {"label": "Bite", "icon": "🐾"},
        "specials": {"w1": SP("The Howl", "🐺", effect="rudel"), "s1": SP("Goes for the Throat", "🩸", bonus=4, effect="blutend")},
        "pattern": ["w1", "n", "s1", "n"],
        "weakness": "courage", "immune": dict(TIER), "parade": "sprite", "parade_ziel": 70},
    "hirtendrohne": {
        "name": "Shepherd Drone", "sprite": "ShepherdDrone", "cls": "maschine", "element": "luft", "tier": "gefaehrlich",
        "attack": {"label": "Pulse", "icon": "📡"},
        "specials": {"w1": SP("The Pulse", "📡", effect="erschuettert"), "s1": SP("Dive", "📡💥", bonus=4, dodge_only=True)},
        "pattern": ["w1", "n", "n", "s1"],
        "weakness": None, "immune": {"charm": "It is a machine. It does not care how you feel.",
                                     "courage": "It is a machine. It has no fear to find."},
        "parade": "sprite", "parade_ziel": 70},
}
DROPS = {}

# Beistand in Station 7: je Runde eine Aktion, siehe kern/kampf.py _beistand
PLATTE = {"wer": "Danzel", "text": "He steps in front of you, and the plate in his lining takes the first of it. Your next hit is halved.", "schutz": True}
BEISTAND = [{"wenn": {"flag": "rt_ausgang_alle"}, "aktionen": [
                {"wer": "Bibi", "text": "A water grenade bursts on %(ziel)s.", "anteil": 0.08, "state": "nass"},
                {"wer": "Charly", "text": "Her taser hits %(ziel)s.", "anteil": 0.12, "state": "strom"},
                PLATTE]},
            {"aktionen": [None, None, PLATTE]}]              # getrennt: nur Danzel bleibt neben Duc stehen


def OUT(text, *folgen):
    return {"text": text, "folgen": list(folgen)}


def _b(titel, ziel, bild, gegner, lp, level, aus, flags=None, flucht=True, beistand=None, musik=None):
    """aus = (ko, aufgabe, entkommen, niederlage). flags = Praefix: setzt <p>_sieg und <p>_ko bzw. <p>_geredet."""
    sieg = [{"flag": flags + "_sieg"}] if flags else []
    b = {"title": titel, "goal": ziel, "image": "eden_rise_%s.png" % bild, "enemy": gegner[0], "enemies": gegner,
         "lp_faktoren": lp, "level": level, "flee_allowed": flucht, "expedition_niederlage": True,
         "outcomes": {"ko": OUT(aus[0], *(sieg + ([{"flag": flags + "_ko"}] if flags else []))),
                      "aufgabe": OUT(aus[1], *(sieg + ([{"flag": flags + "_geredet"}] if flags else []))),
                      "entkommen": OUT(aus[2], *(sieg + ([{"flag": flags + "_ko"}] if flags else []))),
                      "flucht": OUT("You back away."), "niederlage": OUT(aus[3])}}
    if not flucht:
        b["flee_reason"] = "Nonna is behind that door." if beistand else "They've seen you. There's no walking away from this."
    if beistand:
        b["beistand"] = beistand
    if musik:
        b["musik"] = musik
    return b


ENCOUNTERS = {
    "rt_1_bibi_charly": _b("The Red Trio", "Get through them", "macchia_path", ["rt_bibi", "rt_charly"], [0.85, 0.85], 4,
                           ("Bibi lands on her back in the bushes. Charly sits down next to her and opens a bag of crisps.",
                            "They lower their hands. Charly nods once. Bibi looks almost relieved.",
                            "They're gone into the bushes.", "A flash, a blue spark, the ground. Everything goes black."), "rt_1", flucht=False),
    "rt_3_trio": _b("Three in Red", "Get through all three", "macchia_creek_bridge", ["rt_danzel", "rt_bibi", "rt_charly"],
                    [0.5, 0.6, 0.6], 5,
                    ("They go down on the stones, one after the other. Danzel last. He was the furthest back.",
                     "Nobody decides it. They just stop. Danzel's baton is shaking so hard it rattles.",
                     "They're off the bridge.", "Blue light. The stream is very cold, and then everything goes black."), "rt_3", flucht=False),
    "rt_4a_rotte": _b("Between the Black Trunks", "Get down the charcoal road", "charcoal_road", ["bache", "bache"], [0.85, 0.85], 4,
                      ("The boars crash off through the ash.", "They back away, snorting.", "They're gone.",
                       "Tusks, ash, the dark.")),
    "rt_4a_mufflon": _b("Steel on Its Shoulders", "Get past it", "charcoal_road", ["panzer_mufflon"], [2.0], 5,
                        ("It falls on the ash with a clank of metal. The collar blinks, and stops.",
                         "It stands there breathing, head low, and lets you pass.", "It's off through the trunks.",
                         "It hits you like a door. Everything goes black.")),
    "rt_4b_affen": _b("Up on the Walls", "Get into the gorge", "bone_gorge", ["affe", "affe"], [0.6, 0.6], 4,
                      ("The apes scatter up the rock.", "They back away along the ledge.", "They're gone.",
                       "Stones from above. Everything goes black."), musik="kampf_tiere"),
    "rt_4b_hyaenen": _b("Three with Red Lights", "Get through the pack", "bone_gorge", ["ark_hyaene_alpha", "ark_hyaene", "ark_hyaene"],
                        [0.6, 0.45, 0.45], 4,
                        ("The last of them drops. Three red lights keep blinking on the stones.",
                         "They creep back between the rocks, bellies low.", "They run, laughing, down the gorge.",
                         "They come from three sides at once. Everything goes black.")),
    "rt_4c_agenten": _b("Black Suits on the Ridge", "Get up the ridge", "antenna_ridge", ["agent", "agent"], [0.7, 0.7], 5,
                        ("The second agent goes down. Neither of them gets to his radio.",
                         "They drop their batons and keep their hands where you can see them.", "They run for the tree line.",
                         "A baton, the rocks. Everything goes black.")),
    "rt_4c_drohne": _b("Blink, Blink, Pause", "Bring it down", "antenna_ridge", ["hirtendrohne"], [2.6], 5,
                       ("It drops out of the air and breaks apart on the rock.", "It lands. The light goes out on its own.",
                        "It climbs away over the sea.", "The pulse goes through your teeth. Everything goes black.")),
    "rt_7a_garten": _b("Tidy Up", "Hold the garden", "monastery_garden_dusk", ["agent", "agent", "agent"], [0.65, 0.55, 0.55], 5,
                       ("The last one falls into Nonna's rosemary. There are more on the wall.",
                        "They back up against the wall. There are more behind them.", "They fall back over the wall.",
                        "You wake on the boat. Someone carried you."), flucht=False, beistand=BEISTAND),
    "rt_7b_tuer": _b("Nonna's Door", "Hold the door", "monastery_garden_dusk", ["agent", "agent", "hirtendrohne"], [0.6, 0.6, 0.7], 5,
                     ("The drone hits the well and goes dark. The rest of them run. Nobody in the garden moves for a while.",
                      "They carry their own away. Nobody in the garden moves for a while.", "They're gone over the wall.",
                      "You wake on the boat. Someone carried you."), flucht=False, beistand=BEISTAND),
}
