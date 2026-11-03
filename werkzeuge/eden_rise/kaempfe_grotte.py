# -*- coding: utf-8 -*-
"""Gegner und Begegnungen von Akt 2 Woche 2 (Duc 27.10.2026) - Unit-01 an Bord, die Strand-Grotte, Kevins Daecher.
Eingebunden von kaempfe_eden_rise.py wie kaempfe_berge.py.

Story: ereignisse_grotte.py / ereignisse_akt2.py, Wiki docs/wiki/welt/ortskapitel_grotte.md. Level 2-5 (Woche 2 laeuft
neben den Bergen). Die Schmuggler sind Wasser - Sussurro (Luft) bekommt Duc erst in der Zelle, fuer den Boss also genau
rechtzeitig. Unit-01 ist eine Maschine: Terremoto (Stumpf) ist gegen ihn stark. Kevin ist ein Flieger und flieht nie."""

import json, os

EDEN = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Wunschbild -> Platzhalter, bis Character Design es abgenommen hat (wie WUNSCH in ereignisse_grotte.py)
WUNSCH = {"grotto_steps": "hafen_abend", "smugglers_tunnel": "lion_den_cave_b", "crate_hall": "lion_den_cave",
          "torch_gallery": "ravine_fire", "flooded_gallery": "lion_den_cave_b", "air_pocket": "hidden_rock_niche",
          "collapsed_passage": "lion_den_cave", "village_rooftops": "piazza_treppe", "bell_tower_nest": "piazza_treppe",
          "underground_pool_tide": "underground_pool"}


def _bild(name):
    try:
        cfg = json.load(open(os.path.join(EDEN, "eden-config.json"), encoding="utf-8-sig"))
        if os.path.isfile(os.path.join(cfg["st_daten"], "backgrounds", "eden_rise_%s.png" % name)):
            return name
    except Exception:
        pass
    return WUNSCH.get(name, name)


NO_TALK = {"charm": "Animals don't understand you."}
TIER = dict(NO_TALK, courage="It is past being afraid of you.")


def SP(label, icon, bonus=0, effect=None, dodge_only=False):
    return {"label": label, "icon": icon, "bonus": bonus, "effect": effect, "dodge_only": dodge_only}


ENEMIES = {
    "unit01": {
        "name": "Unit-01 (Red Eye)", "sprite": "Unit1", "cls": "maschine", "element": None, "tier": "gefaehrlich",
        "attack": {"label": "Piston Punch", "icon": "⚙"},
        "specials": {"w1": SP("Coughs Soot", "💨", effect="geblendet"), "s1": SP("Full Throttle", "⚙💥", bonus=6)},
        "weakness": "empathy", "parade": "sprite", "boss": True,
        "immune": {"charm": "Unit-01 grinds its teeth. Whatever is giving the orders isn't listening to you."},
        "parade_ziel": 70},
    "schmuggler": {
        "name": "Smuggler", "sprite": "Thief", "cls": "mensch", "element": "wasser", "tier": "gefaehrlich",
        "attack": {"label": "Knife", "icon": "🗡"},
        "specials": {"w1": SP("Sand in Your Eyes", "🌫", effect="geblendet"), "s1": SP("Knife Under the Ribs", "🗡💥",
                                                                                     bonus=6)},
        "weakness": "courage", "parade": "sprite", "immune": {}, "parade_ziel": 70},
    "riscossore": {
        "name": "U Riscossore", "sprite": "PirateAlpha", "cls": "mensch", "element": "wasser", "tier": "toedlich",
        "attack": {"label": "Cane Sword", "icon": "🗡"},
        "specials": {"w1": SP("Peels an Orange", "🍊", effect="geschwaecht"),
                     "s1": SP("The Torches Close In", "🔥🗡", bonus=9, effect="brennend")},
        "weakness": None, "parade": "sprite", "boss": True,
        "immune": {"courage": "He finishes the orange first. “Signore. I have been threatened by better men, in better "
                              "suits.”",
                   "charm": "“Charming. Charm is cheap. I collect debts.”"}, "parade_ziel": 70},
    "tauben": {
        "name": "Kevin's Pigeons", "sprite": "PigeonAlpha", "cls": "flieger", "element": "luft", "tier": "laestig",
        "attack": {"label": "Peck", "icon": "🪶"},
        "specials": {"w1": SP("All at Once", "🕊🕊", bonus=3)},
        "weakness": "courage", "immune": dict(NO_TALK), "flee_at": 0.3, "parade": "sprite"},
    "kevin": {
        "name": "Kevin", "sprite": "Kevin", "cls": "flieger", "element": "luft", "tier": "gefaehrlich",
        "attack": {"label": "Mine!", "icon": "🪶"},
        "specials": {"w1": SP("Screams in Your Face", "📢", effect="erschuettert"),
                     "s1": SP("Dive-Bomb", "💨💥", bonus=6, dodge_only=True)},
        "weakness": None, "parade": "sprite", "boss": True,
        "immune": {"charm": "Kevin looks at you. Kevin has never been charmed by anything but chips.",
                   "courage": "Kevin is not afraid of you. Kevin is not afraid of God."}, "parade_ziel": 75},
    # Flut-Nacht (Duc 28.10.2026): Fledermaeuse, mit 10 % die Vampirin, und die Sirene, die man nur durch Reden besiegt
    "fledermaeuse": {
        "name": "The Bat Swarm", "sprite": "BatAlpha", "cls": "flieger", "element": "luft", "tier": "gefaehrlich",
        "attack": {"label": "Bite", "icon": "🦇"},
        "specials": {"w1": SP("They Drink", "🩸", effect="heal3"),
                     "s1": SP("The Whole Ceiling at Once", "🦇🦇", bonus=6, dodge_only=True)},
        "weakness": "courage", "immune": dict(NO_TALK), "flee_at": 0.25, "parade": "sprite", "halsband": False},
    "schlange_alpha": {
        "name": "Black Viper", "sprite": "SnakeAlpha", "cls": "tier", "element": "erde", "tier": "gefaehrlich",
        "attack": {"label": "Bite", "icon": "🐍"},
        "specials": {"w1": SP("Venom", "🟢", bonus=2, effect="geschwaecht"),
                     "s1": SP("Strikes from the Water", "🐍💥", bonus=7, effect="blutend")},
        "weakness": "courage", "immune": dict(NO_TALK), "flee_at": 0.2, "parade": "sprite", "halsband": False},
    "vampirin": {
        "name": "The Pale Lady", "sprite": "Vampire", "cls": "monster", "element": "feuer", "tier": "toedlich",
        "attack": {"label": "Claws", "icon": "🩸"},
        "specials": {"w1": SP("Eyes Like Lanterns", "👁", effect="ungedeckt"),
                     "w2": SP("A Flutter of Wings", "🦇", bonus=3, dodge_only=True),
                     "s1": SP("The Kiss", "💋🩸", bonus=9, effect="drain")},
        "weakness": None, "parade": "sprite", "boss": True,
        "immune": {"charm": "She smiles with far too many teeth. “Oh, you're sweet. They always are.”",
                   "courage": "She laughs, softly, like someone who has outlived every brave man she ever met."},
        "parade_ziel": 75},
    "sirene": {
        "name": "The Siren", "sprite": "Siren", "cls": "monster", "element": "wasser", "tier": "gefaehrlich",
        "attack": {"label": "Song", "icon": "🎶"},
        "specials": {"w1": SP("A Song Under the Skin", "🎶", effect="ungedeckt"),
                     "s1": SP("The Wave", "🌊💥", bonus=8, effect="nass", dodge_only=True)},
        "weakness": "charm", "parade": "sprite", "boss": True, "fassung_faktor": 2,
        "untouchable": "Your blow goes through her like through water. She laughs. “You can't cut the sea, sailor.”",
        # Duc 29.10.2026: wer sie trifft, bekommt eskalierende Hinweise (necken, zwei kleine, ein direkter - dann leuchtet
        # Talk). Vertont als kampf.sirene.<n> (vertonen_eden_rise.py), Tags in stimme_tags.json (stimme_tags_berge.py).
        "untouchable_hinweise": [
            {"wer": "sirene", "gefuehl": "amusement",
             "text": "Ooh. That tickled, sailor. Do it again, I dare you."},
            {"wer": "sirene", "gefuehl": "amusement",
             "text": "Men have been stabbing the sea for three thousand years. Not one of them thought to talk to it."},
            {"wer": "sirene", "gefuehl": "curiosity",
             "text": "Still swinging? I didn't sing you down here for steel, sailor. I'm starving for a good word."},
            {"wer": "sirene", "gefuehl": "annoyance",
             "text": "Gods, you're slow. Put the steel away and talk to me. Words are the only thing that can touch me."}],
        "immune": {"courage": "“Frighten me? I have sung whole crews to sleep, sailor.”",
                   "empathy": "“Keep your kindness. I want words.”"}, "parade_ziel": 70},
}

# Chips (Duc: "gerne Upgrades verteilen"): der Boss gibt Praezision III, Unit-01 das erste Stueck Agenten-Technik
DROPS = {"unit01": ["praezision", 2], "schmuggler": ["konter", 2], "riscossore": ["praezision", 3],
         "kevin": ["ausdauer", 2],
         # Vampirin (Duc 28.10.2026): immer gute Beute, aber nur eine je Kampf
         "vampirin": {"eins_aus": [["chip", [["praezision", 2], ["konter", 2], ["ausdauer", 2]]], ["geld", 120],
                                   ["material", ["jade", "topas", "aquamarin", "amethyst", "steel_plate"]]]}}


def OUT(text, *folgen):
    return {"text": text, "folgen": list(folgen)}


def _b(titel, ziel, bild, gegner, level, aus, flucht=True, grund=None, niederlage=True):
    b = {"title": titel, "goal": ziel, "image": "eden_rise_%s.png" % _bild(bild), "enemy": gegner, "level": level,
         "flee_allowed": flucht, "expedition_niederlage": niederlage,
         "outcomes": {"ko": OUT(aus[0]), "aufgabe": OUT(aus[1]), "entkommen": OUT(aus[2]),
                      "flucht": OUT("You back away."), "niederlage": OUT(aus[3])}}
    if grund:
        b["flee_reason"] = grund
    return b


ENCOUNTERS = {
    "a2_unit01": dict(_b("A Red Eye in the Dark", "Bring Unit-01 down without breaking her", "workshop", "unit01", 2,
                         ("Unit-01 shudders, coughs one last cloud of soot and sits down. The red in her eye flickers, "
                          "and goes amber.",
                          "Unit-01 stops, whines like a dog, and lies down at your feet.",
                          "Unit-01 rolls back into her corner and stays there, eye flickering red and amber.",
                          "A piston, the wall, the floor. When you come to, Rosi has him switched off."),
                         flucht=False, grund="You're not leaving him like this.", niederlage=False),
                      image="eden_rise_workshop.png"),
    "gr_1_ratten": _b("Something Squeaks", "Get down the steps", "grotto_steps", "ratte_alpha", 2,
                      ("The big rat squeals and the whole carpet of them pours back into the cracks.",
                       "They scatter into the rock.", "They're gone.",
                       "Weed, rock, teeth. Everything goes black.")),
    "gr_3_viper": _b("Something on the Rail", "Get past it", "smugglers_tunnel", "schlange", 2,
                     ("It flows off the rail and into a crack.", "It uncoils and slides away.", "It's gone.",
                      "A bite, a burning arm, the dark.")),
    "gr_4_schmuggler": _b("Cards on a Crate", "Get past the card game", "crate_hall", "schmuggler", 3,
                          ("The smuggler goes down among the cards. His friend has already run.",
                           "He throws his knife on the crate and raises his hands.",
                           "He runs off into the tunnels.", "Two knives. Everything goes black.")),
    "gr_6_fackel": _b("Torches", "Get past the torch gallery", "torch_gallery_2", "fackelpirat", 3,
                      ("The torch rolls into a puddle and hisses out. So does he.",
                       "He drops the torch and backs away into the dark.", "He's gone.",
                       "Fire, then nothing.")),
    "gr_u1_viper": _b("On the Ledge", "Keep it away from Matteu", "flooded_gallery", "schlange", 3,
                      ("It slides off the ledge into the black water.", "It coils up and lets you pass.",
                       "It's gone into the dark.", "A bite at the neck. Everything goes black.")),
    "gr_u1_ratten": _b("Behind the Grate", "Drive the rats back", "air_pocket", "ratte_alpha", 3,
                       ("They pour back through the bars.", "They scatter.", "They're gone.",
                        "Teeth, from everywhere. Everything goes black.")),
    "gr_u2_pirat": _b("Two Men and a Rucksack", "Get the bag back", "collapsed_passage", "pirat", 3,
                      ("The first one goes down. The second drops the rucksack and runs.",
                       "They drop the bag and back off into the dark.", "They're gone, with the lamps.",
                       "A cutlass flat across the head. Everything goes black.")),
    "kv_tauben": _b("Kevin's Pigeons", "Get across the roofs", "village_rooftops", "tauben", 2,
                    ("The pigeons explode into the sky.", "They scatter over the roofs.", "They're gone.",
                     "You slip on a tile. Everything goes sideways."), niederlage=False),
    "kv_kevin": _b("Kevin", "Get the page back", "bell_tower_nest", "kevin", 3,
                   ("Kevin flops onto the weathervane, beaten, and screams at the whole village about it.",
                    "Kevin hops off the nest and sulks.", "Kevin flies one circle round the tower and comes back. "
                    "He always comes back.", "Kevin wins. Kevin always wins. Lea pulls you back in by the belt."),
                   flucht=False, grund="Not in front of Lea.", niederlage=False),
}
# Flut-Nacht (Duc 28.10.2026, ereignisse_grotte.py FLUT): vier Kaempfe, dann die Sirene; Level 4 (nach der Grotte)
_VAMPIRIN = _b("The Pale Lady", "Survive her", "smugglers_tunnel", "vampirin", "duc",
               ("She folds into a cloud of bats and is gone. Something glints on the rail where she stood.",
                "She steps back into the dark, smiling. “Another night, sweet.” She leaves something behind.",
                "She's gone, and so are the bats.", "Cold lips at your neck. Everything goes very quiet."),
               niederlage=False)
ENCOUNTERS.update({
    "fn_1_ratten": _b("Up from the Water", "Get down the steps", "grotto_steps", "ratte_alpha", 4,
                      ("The big rat squeals and the rest of them pour back into the cracks above the waterline.",
                       "They scatter up the rock.", "They're gone.", "Wet rock, teeth. Everything goes black.")),
    "fn_2_fledermaeuse": dict(
        _b("The Ceiling Moves", "Get through the tunnel", "smugglers_tunnel", "fledermaeuse", 4,
           ("The swarm breaks apart and whirls out over the water.", "They lift off the ceiling and stream away.",
            "They're gone into the dark.", "Wings, teeth, everywhere. Everything goes black.")),
        selten=dict({k: v for k, v in _VAMPIRIN.items() if k in ("title", "goal", "enemy", "level", "outcomes")},
                    chance=0.1, steigt=0.1, level_plus=2)),
    "fn_3_viper": _b("Something in the Water", "Get across the gallery", "flooded_gallery", "schlange_alpha", 4,
                     ("It slides off into the black water and doesn't come back.", "It coils up and lets you pass.",
                      "It's gone under.", "A bite at the ankle, then the cold. Everything goes black.")),
    "fn_4_piraten": _b("The Night Shift", "Get past the crates", "crate_hall", "pirat", 4,
                       ("The pirate goes down between the crates. The others leave the boat and run.",
                        "He drops the cutlass and raises his hands.", "They row off into the dark.",
                        "A cutlass flat across the head. Everything goes black.")),
    "fn_5_sirene": dict(_b("The Siren", "Talk her down", "underground_pool_tide", "sirene", "duc",
                           ("", "She sinks down to her shoulders and smiles. “All right, sailor. You talked. Now I'll "
                                "talk.”", "She slides under the black water. The humming goes on for a long time.",
                            "Her song fills your head, and the water fills the rest. You wake on the beach."),
                           niederlage=False), level_plus=1),
})
for _m in (False, True):
    for _s in (False, True):
        ENCOUNTERS["gr_8_riscossore%s%s" % ("_matteu" if _m else "", "_spaet" if _s else "")] = _b(
            "U Riscossore", "Get Gennaro out", "crate_hall", "riscossore", 4 - (1 if _m else 0) + (1 if _s else 0),
            ("The old man sits down against a crate, very slowly, and puts the cane sword across his knees.",
             "He raises one hand. “Enough. Let's talk business.”",
             "His men drag him back to the boat.",
             "The torches close in. Everything goes black."), flucht=False, grund="The tide is behind you.")
