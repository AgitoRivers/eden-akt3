# -*- coding: utf-8 -*-
"""Ortskapitel "The Mountain and the Daughter" - Berge & Genueser Turm (Akt 2, Duc 27.10.2026).

Plot: docs/wiki/welt/ortskapitel_berge.md. Gebaut wie das Kloster (ereignisse_kloster.py): Frame-Kette (art "ort"),
"weiter" oeffnet den naechsten Frame (nach einem Kampf erst nach dem Sieg), ohne "weiter" ist der Ausflug vorbei.
Keine Spur-Uhr: Wolff laesst Duc Zeit, Adrien zu finden (Duc). Wiedereinstieg am Turm und an der Bergerie.

  Petru (Bootsschuppen, ab Tag 9, nach dem Kloster) -> bg_start .. bg_bruecke -> Bergerie -> Bosskampf -> drei Wege
  Umweg 1 "Old Grey"         Ghjuvan, die Baerin mit Jungen: Mutter toeten oder Chip schneiden (Ghjuvan stirbt spaeter)
  Umweg 2 "The Mazzera's Dream" Dumenica, der Panther: erloesen (mehr Agenten, Huette brennt) oder hetzen (Petru steigt auf)

Graue Entscheidungen (E-073): Turm (Wahrheit/Luege), Old Grey, Panther, drei Wege. Jede Seite kostet etwas."""
from ereignisse_basis import *  # noqa: F401,F403

KAMPF = lambda bid: {"kampf": bid}
WEITER = lambda ziel: {"weiter": ziel}
EXP = {"expedition": "berge"}
EXP_ENDE = {"expedition": "ende"}
STUFE = 8                                    # Punkte je Vertrauensstufe
DATIERT = lambda name: {"flag_datiert": name}          # Flag + Tag, an dem es fiel (Bedingung flag_seit, kern/regeln.py)

# Hintergruende: Wunschbild (Auftrag an Character Design 27.10.) -> vorhandener Platzhalter, bis es abgenommen ist
WUNSCH = {"charcoal_clearing": "creek_rest", "tower_cliff": "forest_edge_cliffs", "high_pasture": "macchia_path_b",
          "goat_path": "ravine_fork", "summer_hut_fire": "shepherd_hut_ruin", "bear_thicket": "forest_edge_cliffs",
          "bear_den": "lion_den_cave", "mazzera_hut": "mountain_lake", "ridge_night_lights": "berge_rotes_licht",
          "abandoned_mountain_hut": "monks_camp_abandoned", "panther_lair": "hidden_rock_niche",
          "rope_bridge_gorge": "macchia_creek_bridge"}
VORHANDEN = ["chestnut_switchbacks", "genoese_tower_camp", "mountain_lake", "foggy_ridge", "bergerie_interior",
             "bergerie_dusk_exterior", "berge_rotes_licht", "macchia_path_b"]


def _bg_da(name):
    try:
        cfg = json.load(open(os.path.join(EDEN, "eden-config.json"), encoding="utf-8-sig"))
        return os.path.isfile(os.path.join(cfg["st_daten"], "backgrounds", "eden_rise_%s.png" % name))
    except Exception:
        return False


def BILD(name):
    b = name if name not in WUNSCH or _bg_da(name) else WUNSCH[name]
    if b not in ORT_BILDER:
        ORT_BILDER.append(b)
    return b


RAST = {"bg_koehler", "bg_see", "bg_see_rast", "bg_kamm_funk", "bg_u1_huette", "bg_u2_huette_leer", "bg_bergerie"}
FUND = {
    "bg_koehler": "Someone slept here, and not long ago. Two army blankets are folded under a chestnut tree, the "
                  "corners squared the way only soldiers fold them. One has a dark stain at the edge that has dried "
                  "brown.",
    "bg_see_rast": "A flat rock by the water, warm from the day. Someone has stacked three stones on it, small to big, "
                   "the way children do. Or the way a woman does when she wants someone to know she was here.",
    "bg_u1_huette": "Ghjuvan's summer hut. A bed, a stove, a calendar from a feed merchant in Corte, every day crossed "
                    "out in red. Under the calendar is a letter from the bank, folded so often it is falling apart.",
    "bg_u2_huette_leer": "The hut has been empty for twenty years and nobody has touched it. Dust on the table, a cup "
                         "turned upside down, and in the middle a small dog carved out of chestnut wood. A child's toy. "
                         "Someone has dusted the dog. Only the dog.",
    "bg_bergerie": "The bergerie smells of smoke, sheep and iodine. Bandages are drying on a line over the hearth. On "
                   "the table, next to a camera with a cracked lens, someone has laid out bread for three.",
}
SPERRE = {"bg_drei_wege", "bg_drei_wege_petru", "bg_u1_wahl", "bg_u2_wahl", "bg_turm_f1", "bg_turm_f2", "bg_turm_f3"}


def FR(id, nr, bild, titel, lage, zeilen, optionen, personen=None, sets=None, ton="ernst"):
    e = E(id, "ort", ton, titel, WANN((9, 21)), BILD(bild), personen or {}, lage, zeilen, optionen, sets)
    e["frame"] = nr
    if id in RAST:
        e["rast"] = True
    if id in SPERRE:
        e["sperre"] = True
    if id in FUND:
        e["fund"] = FUND[id]
    return e


def H1(handelnd, *betroffen):
    return {"handelnd": handelnd, "betroffen": [{"id": b, "ton": "?", "was": ""} for b in betroffen]}


S = {"petru": "Standard", "laetitia": "laetitia_standard", "adrien": "adrien_standard", "wolff": "wolff_standard",
     "ghjuvan": "ghjuvan_standard", "dumenica": "dumenica_standard", "toto": "Standard"}


def SETS_(*pids):
    return {p: S[p] for p in pids}


# ------------------------------------------------------------------ Gegenstaende
item("laetitia_scarf", "Laetitia's Red Scarf", "andenken",
     text="A faded red scarf, still damp from the lake. It smells of woodsmoke and of a girl who left in a hurry.")
item("av_radio", "A.V. Estates Radio", "andenken",
     text="A black field radio with a small white logo: A.V. Estates. The last channel used is still set.")
item("ir_controller", "Collar Controller", "andenken",
     text="A grey handset with an infrared lamp and a dial. Every blinking collar on the mountain answers to it.")
item("ghjuvan_knife", "Ghjuvan's Father's Knife", "andenken",
     text="A shepherd's knife with a horn handle worn smooth by three generations of the same thumb.")
# Dumenicas Amulett und Wolffs Képi (Vorteil auf Wahrnehmung/Mut) stehen in gegenstaende_eden_rise.py - hier fuer die Pruefung
item("dumenica_amulet", "Dumenica's Amulet", "gluecksbringer")
item("legion_kepi", "Wolff's Képi", "gluecksbringer")


# ------------------------------------------------------------------ Auftakt: Petru am Bootsschuppen (ab Tag 9)
AUFTAKT = FR(
    "bg_petru_auftrag", 0, "petru_workshop", "Petru's Daughter",
    "Evening at the boathouse. Petru is mending a net that isn't torn. On the hook by the door hangs a red hair tie, "
    "the kind a girl leaves behind when she means to come back. The radio plays football. He turns it off when he "
    "sees you, and that is how you know it's serious.",
    [Z("petru", "Hm.", "sadness"),
     Z("petru", "Laetitia went up to the summer huts. Twelve days ago. She always comes back after three.", "sadness"),
     Z("petru", "In the village they say she was seen with a man in uniform, a soldier, up there by the tower.", "fear"),
     Z("petru", "I have never asked anyone for anything. Not since Marie died. Bring her down, Officer. Please.", "grief")],
    [O("Puts the net down for him. “I'll find her. Tell me the way.”",
       [F("berge_angenommen"), V("petru", 4)],
       zeile=Z("petru", "Through the chestnut woods, up to the old Genoese tower. After that, ask the mountain.",
               "gratitude")),
     O("“Did you two argue before she left?”", [F("berge_angenommen")],
       zeile=Z("petru", "We don't argue. We say nothing. It's worse.", "remorse")),
     O("“Give me a day to get ready.”", [],
       zeile=Z("petru", "Hm. The mountain has waited twelve days. It can wait one more. I'm not sure I can.",
               "sadness"))],
    personen=H1("petru"), sets=SETS_("petru"))


# ------------------------------------------------------------------ Hauptkette (12 Stationen)
NACH_TURM = [{"wenn": {"flag": "capra_dabei"}, "id": "bg_turm_capra"}, {"id": "bg_turm_parole"}]
# Bergerie, Bosskampf: Old Grey hilft (Chip geschnitten) und die Agenten zaehlen nach dem Panther (Umweg 2)
BOSS = [{"wenn": {"alle": [{"flag": "bg_panther_gehetzt"}, {"flag": "bg_baer_frei"}]}, "id": "bg_abend_solo_baer"},
        {"wenn": {"flag": "bg_panther_gehetzt"}, "id": "bg_abend_solo"},
        {"wenn": {"alle": [{"flag": "bg_panther_erloest"}, {"flag": "bg_baer_frei"}]}, "id": "bg_abend_trio_baer"},
        {"wenn": {"flag": "bg_panther_erloest"}, "id": "bg_abend_trio"},
        {"wenn": {"flag": "bg_baer_frei"}, "id": "bg_abend_duo_baer"},
        {"id": "bg_abend_duo"}]
# Nach einem Umweg: weiter den Kamm hinauf - oder heim, wenn die Bergerie schon erreicht ist (eigener Ausflug)
NACH_UMWEG = [{"wenn": {"flag": "bg_bergerie_erreicht"}, "id": "bg_wieder_ende"}, {"id": "bg_kamm"}]
# Umweg 2 beginnt am See (Station 5): danach kommt noch die Hochweide, wenn Duc Ghjuvan noch nicht getroffen hat
NACH_U2 = [{"wenn": {"flag": "bg_bergerie_erreicht"}, "id": "bg_wieder_ende"},
           {"wenn": {"flag": "bg_ghjuvan_getroffen"}, "id": "bg_kamm"}, {"id": "bg_hochweide"}]
DREI_WEGE = [{"wenn": {"flag": "bg_panther_gehetzt"}, "id": "bg_drei_wege_petru"}, {"id": "bg_drei_wege"}]

FRAMES = [
    FR("bg_start", 1, "chestnut_switchbacks", "The Chestnut Switchbacks",
       "The path climbs in tight bends through old chestnut trees. In the mud by the first bend there are boot prints, "
       "deep and evenly spaced, military soles. Further up, something grunts. A wild sow with four striped piglets "
       "stands across the path and has no intention of moving.",
       [],
       [O("Lowers his weapon a little and steps forward slowly.", [EXP, KAMPF("berge_1_bache"), WEITER("bg_koehler")]),
        O("Reads the boot prints first. “Two men. One of them limps.”", [EXP, KAMPF("berge_1_bache"), WEITER("bg_koehler")],
          probe=P("perception", 12), erfolg=[F("bg_spur_hinkt")], fehlschlag=[]),
        O("Turns back. “Not today.”", [])]),
    FR("bg_koehler", 2, "charcoal_clearing", "The Charcoal Burners' Clearing",
       "An old charcoal pit, a ring of blackened earth, and a fire pit somebody has used recently. The chestnuts here "
       "are huge. For a moment the mountain is just a mountain.",
       [],
       [O("Rests a while, then climbs towards the tower.", [WEITER("bg_turm")])],
       ton="wholesome"),
    FR("bg_turm", 3, "genoese_tower_camp", "The Genoese Tower",
       "The old tower stands on the ridge like a broken tooth. Below it is a camp: three green tents, a radio aerial, "
       "men in Legion fatigues cleaning rifles. A sergeant with a grey beard and a black eye patch sees you coming long before you reach "
       "him, and waits.",
       [Z("wolff", "Halt. This is a military operation. Sergent Kaspar Wolff, Foreign Legion.", "neutral"),
        Z("wolff", "You are not a hiker. Hikers have better shoes. Who are you?", "curiosity")],
       [O("Gives his name and his job. “First Officer of the Eden Rise. Down in the bay.”", [WEITER(NACH_TURM)])],
       personen=H1("wolff"), sets=SETS_("wolff")),
    FR("bg_turm_capra", 3, "genoese_tower_camp", "The Goat and the Sergeant",
       "Capra, the goat with the collar, trots past you, straight into the camp, and starts eating a map off the field table. Two legionnaires "
       "jump up. Wolff raises one hand and they freeze.",
       [Z("wolff", "A goat. On an operation. With a collar.", "surprise"),
        Z("wolff", "…May I?", "caring"),
        Z("wolff", "When I was a boy in the Vosges we had one like her. She ate my homework, my shoelaces and once a "
                   "lieutenant's letter. Good animal.", "amusement")],
       [O("Lets him scratch Capra behind the ears. “She likes you.”", [F("bg_wolff_capra"), WEITER("bg_turm_parole")])],
       personen=H1("wolff"), sets=SETS_("wolff"), ton="witzig"),
    # Herkunft des Schwerts (Duc 01.11.2026): Parole, das Ehrenwort; Rueckbezug in bg_weg_c_sieg
    FR("bg_turm_parole", 3, "genoese_tower_camp", "Parole",
       "Wolff's sword is long and straight, in a scabbard worn pale at the edges. You don't know anyone who still "
       "carries one.",
       [],
       [O("Looks at the sword. “Is that part of the uniform?”", [WEITER("bg_turm_parole_2")])],
       personen=H1("wolff"), sets=SETS_("wolff")),
    FR("bg_turm_parole_2", 3, "genoese_tower_camp", "Parole",
       "He rests one hand on the hilt.",
       [Z("wolff", "No. The Legion gave me a rifle, a number and a new name. This one I got from Adjudant Hoffer, who "
                   "taught me to march.", "neutral"),
        Z("wolff", "He called it Parole. His word. When he retired he gave it to me in front of the whole company, and "
                   "he made me read what is on the blade. Honneur et Fidélité.", "pride"),
        Z("wolff", "He said a rifle does what it is told. With this you have to stand close and look at the man. So I "
                   "carry it. It is heavy and it is stupid, and I have been told so in nine languages.", "amusement")],
       [O("Just nods.", [WEITER("bg_turm_f1")])],
       personen=H1("wolff"), sets=SETS_("wolff")),
    FR("bg_turm_f1", 3, "genoese_tower_camp", "Three Questions · One",
       "Wolff pulls a folding stool out for you. He doesn't sit himself. He takes out a notebook, and a pencil he has "
       "sharpened with a knife.",
       [Z("wolff", "I am looking for a deserter. Caporal Adrien Morel, twenty-eight, wounded. Has anyone in the village "
                   "spoken of a soldier?", "neutral")],
       [O("Tells him the truth. “Petru's daughter was seen up here with a man in uniform.”",
          [F("bg_wolff_wahr_1"), WEITER("bg_turm_f2")],
          zeile=Z("wolff", "Thank you. The truth costs nothing, and still most people are too stingy with it.",
                  "approval")),
        O("Shrugs. “Nobody tells a stranger anything down there.”", [F("bg_wolff_luege_1"), WEITER("bg_turm_f2")],
          zeile=Z("wolff", "Hm. That is true of villages everywhere. It may even be true of you.", "disapproval"))],
       personen=H1("wolff"), sets=SETS_("wolff")),
    FR("bg_turm_f2", 3, "genoese_tower_camp", "Three Questions · Two",
       "He writes something down. It takes longer than one word should take.",
       [Z("wolff", "So. Why does an officer from a yacht climb a mountain in the wrong shoes?", "curiosity")],
       [O("“A father asked me to bring his daughter home.”", [F("bg_wolff_wahr_2"), WEITER("bg_turm_f3")],
          zeile=Z("wolff", "Then we want different things from the same mountain. That is not a problem yet.",
                  "neutral")),
        O("“The view. I needed a day off the boat.”", [F("bg_wolff_luege_2"), WEITER("bg_turm_f3")],
          zeile=Z("wolff", "The view. Of course. It is a very good view. I have looked at it for nine days.",
                  "annoyance"))],
       personen=H1("wolff"), sets=SETS_("wolff")),
    FR("bg_turm_f3", 3, "genoese_tower_camp", "Three Questions · Three",
       "Wolff closes the notebook and puts it in his breast pocket. Now he sits down, on an ammunition crate, so that "
       "his one eye is level with yours.",
       [Z("wolff", "Last question. If you find him before I do, will you tell me?", "neutral")],
       [O("Holds his gaze. “I'll hear his side first. Then I'll decide.”", [F("bg_wolff_wahr_3"), WEITER("bg_turm_ende")],
          zeile=Z("wolff", "An honest answer that I don't like. I will remember both parts.", "approval")),
        O("“Of course, Sergent.”", [F("bg_wolff_luege_3"), WEITER("bg_turm_ende")],
          zeile=Z("wolff", "Of course. Good. I have written it down.", "neutral"))],
       personen=H1("wolff"), sets=SETS_("wolff")),
    FR("bg_turm_ende", 3, "genoese_tower_camp", "The Sergeant's Patience",
       "Wolff stands up and points along the ridge with the pencil.",
       [Z("wolff", "The deserter is wounded. He will not get far, and he knows it. So I wait. Waiting is half of my job, "
                   "and the half I am best at.", "neutral"),
        Z("wolff", "Go and find your girl, Officer. Take as long as you need. I will be here.", "caring")],
       [O("Nods and follows the ridge.", [F("bg_turm_erreicht"), WEITER("bg_steilhang")])],
       personen=H1("wolff"), sets=SETS_("wolff")),
    FR("bg_turm_zurueck", 3, "genoese_tower_camp", "Back at the Tower",
       "The legionnaires nod at you. Wolff is writing in his notebook and does not look up.",
       [Z("wolff", "Still looking? Good. So am I.", "neutral")],
       [O("Takes the ridge path again.", [EXP, WEITER("bg_steilhang")]),
        O("Goes back down to the boat.", [])],
       personen=H1("wolff"), sets=SETS_("wolff")),
    FR("bg_steilhang", 4, "tower_cliff", "Below the Tower",
       "The path runs along a cliff below the tower. A wolf stands on the ledge ahead, grey and thin, a red light "
       "blinking at its throat. There are no wolves on Corsica. This one doesn't know that.",
       [],
       [O("Holds his ground on the narrow path.", [KAMPF("berge_4_wolf"), WEITER("bg_see")])]),
    FR("bg_see", 5, "mountain_lake", "The Mountain Lake",
       "The lake is so still it looks like a second sky. An ape crouches on the rocks at the shore, collar blinking, "
       "and something red floats in the reeds behind it.",
       [],
       [O("Walks along the shore towards the red thing.", [KAMPF("berge_5_affe"), WEITER("bg_see_tuch")])]),
    FR("bg_see_tuch", 5, "mountain_lake", "Red in the Reeds",
       "It's a scarf, soaked through and caught in the reeds. Faded red, like the hair tie on Petru's door. It's the kind a girl ties "
       "round her neck when she climbs.",
       [],
       [O("Wrings it out and puts it in his pocket. “I'll give it back to her.”",
          [I("laetitia_scarf"), F("bg_halstuch"), WEITER("bg_see_rast")]),
        O("Leaves it where it is. “She lost it. That's all it means.”", [WEITER("bg_see_rast")])]),
    FR("bg_see_rast", 5, "mountain_lake", "An Old Woman at the Water",
       "There's a small stone hut at the far end of the lake, herbs drying over the door, a candle in the window in "
       "broad daylight. An old woman in black is sitting on the step. She has been watching you the whole time.",
       [Z("dumenica", "You found the scarf. Of course you did. The mountain wanted you to.", "neutral")],
       [O("Walks over to her.", [F("bg_dumenica_getroffen"), WEITER("bg_u2_huette")]),
        O("Nods to her and keeps climbing. “Later.”", [F("bg_dumenica_getroffen"), WEITER("bg_hochweide")])],
       personen=H1("dumenica"), sets=SETS_("dumenica")),
    FR("bg_hochweide", 6, "high_pasture", "The High Pasture",
       "A stone fold, a handful of sheep, and a farmhouse that has been patched more often than it has been painted. "
       "A shepherd with a shotgun over his shoulder is counting his sheep. He counts them twice. Then a third time.",
       [Z("ghjuvan", "Forty. Still forty. Thank God. Who are you? Not one of the men in black, I can see that.", "relief")],
       [O("Asks what he's afraid of.", [F("bg_ghjuvan_getroffen"), WEITER("bg_u1_hochweide")]),
        O("Tells him he's looking for Petru's daughter and moves on.", [F("bg_ghjuvan_getroffen"), WEITER("bg_kamm")],
          zeile=Z("ghjuvan", "Laetitia? Up at the bergerie, past the ridge. And if you change your mind, I'll be here. "
                             "Counting.", "sadness"))],
       personen=H1("ghjuvan"), sets=SETS_("ghjuvan")),
    FR("bg_kamm", 7, "foggy_ridge", "The Foggy Ridge",
       "The fog comes up so fast you can hear it. A man in a black suit steps out of it as if he had been waiting for "
       "you. Earpiece, gloves, a pistol he doesn't bother to draw.",
       [],
       [O("“Lost your way to the office?”", [KAMPF("berge_7_agent"), WEITER("bg_kamm_oben")])]),
    FR("bg_kamm_oben", 8, "foggy_ridge", "Higher on the Ridge",
       "Two more of them, back to back in the fog. One is talking into a radio. When he sees you he doesn't stop "
       "talking, he just says it faster.",
       [],
       [O("Goes for the one with the radio.", [KAMPF("berge_8_agenten"), WEITER("bg_kamm_funk")])]),
    FR("bg_kamm_funk", 8, "foggy_ridge", "A.V. Estates",
       "The radio lies in the wet grass, still hissing. A small white logo on the side: A.V. Estates. Somebody on the "
       "other end says a name you know from the hearing, then the line goes dead.",
       [],
       [O("Takes the radio.", [I("av_radio"), F("bg_av_funk"), WEITER("bg_bruecke")]),
        O("Smashes it on a rock.", [F("bg_av_funk_kaputt"), WEITER("bg_bruecke")])]),
    FR("bg_bruecke", 9, "rope_bridge_gorge", "The Rope Bridge",
       "A rope bridge over a gorge so deep the river is only a sound. On the other side a big grey wolf is waiting, and "
       "behind it, the smoke of a chimney. The bergerie.",
       [],
       [O("Steps onto the bridge. It sways. So does he.", [KAMPF("berge_9_wolf_alpha"), WEITER("bg_bergerie")])]),
    FR("bg_bergerie", 10, "bergerie_interior", "The Bergerie",
       "A rifle barrel comes out of the dark before anything else does. Behind it is a young woman with her father's "
       "eyes and none of his patience. On a cot by the fire lies a man with a bandaged chest, trying to sit up.",
       [Z("laetitia", "One more step and I'll find out if this thing still works. Who sent you? The suits or the Legion?",
          "anger"),
        Z("adrien", "Laetitia. Look at his shoes. He's not either.", "amusement"),
        Z("laetitia", "Then he's my father's. That's worse.", "annoyance")],
       [O("Holds out the red scarf. “He's worried sick. And you dropped this.”",
          [WEITER("bg_bergerie_fotos")], zeile=Z("laetitia", "…You went into the lake for that? Idiot. Thank you.",
                                                  "gratitude")),
        O("Raises his hands. “Petru sent me. Nobody else knows I'm here.”", [WEITER("bg_bergerie_fotos")],
          zeile=Z("laetitia", "Everybody knows everything on this mountain. That's the whole problem.", "annoyance"))],
       personen=H1("laetitia", "adrien"), sets=SETS_("laetitia", "adrien")),
    FR("bg_bergerie_fotos", 10, "bergerie_interior", "What Adrien Saw",
       "Adrien hands you the camera with the cracked lens. The pictures are blurry and terrible and you can't stop "
       "looking at them. Cages in a long hall. A bear with a blinking collar. Men in black suits with clipboards.",
       [Z("adrien", "My unit was lent out. Officially it was a security contract. An estate in the mountains, a rich man, "
                    "very nervous.", "neutral"),
        Z("adrien", "They were testing the animals. Making them do things. Attack things. I took pictures, and then I "
                    "ran. Desertion. Five years, if Wolff takes me back.", "fear"),
        Z("laetitia", "He's not going back. I don't care what anyone says.", "anger")],
       [O("“Then we need a better plan than a rifle and a bergerie.”",
          [F("bg_bergerie_erreicht"), WEITER(BOSS)],
          zeile=Z("adrien", "They'll come tonight. The suits. They always come at night.", "fear"))],
       personen=H1("adrien", "laetitia"), sets=SETS_("adrien", "laetitia")),
]

# Bosskampf vor der Bergerie, sechs Varianten (Agenten nach dem Panther, Old Grey hilft nach dem Chip)
_ABEND_LAGE = {
    "duo": "The light goes orange, then grey. Then two men in black come up the slope, and behind them a third one, "
           "much bigger, who doesn't need a weapon.",
    "trio": "They come at dusk, and there are more of them than Adrien expected. Three suits and one enormous man "
            "who walks like a door that has learned to move. They knew someone was on the mountain.",
    "solo": "Only one of them comes, the big one, alone. The others never came down from the ridge last night. You "
            "heard the screaming. Nobody in the bergerie has slept since.",
}
_BAER = (" Halfway up the slope something huge and grey bursts out of the alders and throws the big man sideways "
         "like a sack of flour. Old Grey, the bear you cut the chip out of, looks at you once. Then she is gone.")
for _ag in ("duo", "trio", "solo"):
    for _baer in (False, True):
        _id = "bg_abend_%s%s" % (_ag, "_baer" if _baer else "")
        FRAMES.append(FR(_id, 11, "bergerie_dusk_exterior", "Nightfall at the Bergerie",
                         _ABEND_LAGE[_ag] + (_BAER if _baer else ""),
                         [Z("laetitia", "Adrien, stay down. I mean it.", "fear")],
                         [O("Steps out in front of the door.",
                            [KAMPF("berge_11_%s%s" % (_ag, "_baer" if _baer else "")), WEITER(DREI_WEGE)])],
                         personen=H1("laetitia"), sets=SETS_("laetitia")))

# ------------------------------------------------------------------ Drei Wege (Streit statt Plaedoyer)
_WEGE_LAGE = ("The last agent drags himself into the dark. In the silence afterwards you hear boots on the path. "
              "Wolff, with two legionnaires and a torch. He takes in the bodies, the bandages, the rifle in Laetitia's "
              "hands, and he doesn't raise his voice once.")
_WEGE_ZEILEN = [
    Z("wolff", "Caporal Morel. On your feet, if you can.", "neutral"),
    Z("adrien", "Sergent. They lent us out. To him. You saw the contract, you know what the estate is.", "fear"),
    Z("wolff", "I know what a contract is. I also know what desertion is.", "disapproval"),
    Z("laetitia", "He was shot running away from a cage full of tortured animals, and you want to put him in one.",
      "anger"),
    Z("wolff", "Mademoiselle, I didn't write the law. I only carry it up mountains.", "sadness"),
    Z("adrien", "Show him the pictures. Please. He won't believe me. Maybe he'll believe you.", "fear"),
]


def _wege(id, lage, zeilen, extra=None):
    toto = [{"wenn": {"wert": ["vertrauen.toto", ">=", 3]}, "id": "bg_weg_b"}, {"id": "bg_weg_b_zu"}]
    lueger = {"wenn": {"eine": [{"alle": [{"flag": "bg_wolff_luege_1"}, {"flag": "bg_wolff_luege_2"}]},
                                {"alle": [{"flag": "bg_wolff_luege_1"}, {"flag": "bg_wolff_luege_3"}]},
                                {"alle": [{"flag": "bg_wolff_luege_2"}, {"flag": "bg_wolff_luege_3"}]}]},
              "id": "bg_weg_c_hart"}
    return FR(id, 12, "bergerie_dusk_exterior", "Three Ways Down", lage, zeilen + (extra or []),
              [O("Hands Adrien over. “He'll get a fair hearing. That's all I can give him.”",
                 [F("bg_weg_a"), WEITER("bg_weg_a")]),
               O("Gets between Wolff and the door. “They're leaving tonight. By sea.”", [WEITER(toto)]),
               O("Hands Wolff the camera. “Look at these first. Then decide.”",
                 [F("bg_weg_c"), WEITER([lueger, {"id": "bg_weg_c"}])])],
              personen=H1("wolff", "laetitia", "adrien"), sets=SETS_("wolff", "laetitia", "adrien"))


FRAMES += [
    _wege("bg_drei_wege", _WEGE_LAGE, _WEGE_ZEILEN),
    _wege("bg_drei_wege_petru", _WEGE_LAGE + " Then a second light comes up the path, an old hunting rifle, a man who "
          "climbed all night. Petru.", _WEGE_ZEILEN,
          [Z("petru", "Laetitia. Old Dumenica dreamed you dead. I came. I'm here.", "fear"),
           Z("laetitia", "Papa? You climbed up here? At night? You can't even climb onto your own boat!", "surprise")]),
    FR("bg_weg_b_zu", 12, "bergerie_dusk_exterior", "No Boat Tonight",
       "You call Totò. He answers on the second ring, and he doesn't let you finish.",
       [Z("toto", "Comandante, I like you. But a deserter, the Legion and the mayor's favourite fisherman's daughter, "
                  "on my boat, tonight? You don't know me well enough to ask. Not yet.", "nervousness")],
       [O("Hangs up and turns back to Wolff.", [WEITER(DREI_WEGE)])],
       personen=H1("toto"), sets=SETS_("toto")),
]

# Weg A: uebergeben
FRAMES += [
    FR("bg_weg_a", 12, "bergerie_dusk_exterior", "The Law",
       "Adrien doesn't fight. He lets them put the cuffs on and looks at Laetitia the whole time, as if he wanted to "
       "remember her exactly. Wolff hands you an envelope and his képi.",
       [Z("wolff", "For your trouble. And the képi, because you are the first civilian in nine years who made my job "
                   "easier. Don't wear it in the village.", "neutral"),
        Z("laetitia", "I hope you can sleep, Officer. I really do. I won't.", "disgust"),
        Z("adrien", "It's all right, Laetitia. He did what the law says. That's not nothing.", "sadness")],
       [O("Says nothing. Walks down behind them.",
          [G(300), I("legion_kepi"), F("bg_laetitia_schweigt"), F("bg_fotos_weg"), F("bg_adrien_verhaftet"),
           WEITER("bg_hafen_a")])],
       personen=H1("wolff", "laetitia", "adrien"), sets=SETS_("wolff", "laetitia", "adrien")),
    FR("bg_weg_b", 12, "bergerie_dusk_exterior", "The Smugglers' Route",
       "Totò says one word on the phone, “Midnight,” and hangs up. Wolff looks at you for a long time. Then he looks "
       "at the dark where the path goes down to the sea, and he doesn't send anyone after you.",
       [Z("wolff", "I will report that the deserter was not found. I will hate writing it.", "sadness"),
        Z("laetitia", "Tell Papa… no. Don't tell him anything. He'll know.", "grief"),
        Z("adrien", "We'll send a postcard. From somewhere without mountains.", "gratitude")],
       [O("Walks them down to the cove, where Totò's boat waits without lights.",
          [F("bg_weg_b"), F("bg_legion_npc_zu"), F("bg_fotos_adrien"), V("petru", -40), V("toto", 4),
           WEITER("bg_hafen_b")])],
       personen=H1("wolff", "laetitia", "adrien"), sets=SETS_("wolff", "laetitia", "adrien")),
    FR("bg_weg_c", 12, "bergerie_dusk_exterior", "The Pictures",
       "Wolff looks at the first picture. Then he puts the camera down very carefully on the wall, as if it might go off, "
       "and draws his sword.",
       [Z("wolff", "You show me this in front of my men. You know I have to answer it. Defend yourself.", "anger")],
       [O("Takes his stance. “Then let's get it over with.”", [KAMPF("berge_12_wolff"), WEITER("bg_weg_c_sieg")])],
       personen=H1("wolff"), sets=SETS_("wolff")),
    FR("bg_weg_c_hart", 12, "bergerie_dusk_exterior", "The Pictures",
       "Wolff looks at the pictures, then at you, and his face closes like a door.",
       [Z("wolff", "Of course, Sergent, you said to me at the tower. The view, you said. And now you hand me pictures and want me to "
                   "believe them. Defend yourself, liar.", "anger")],
       [O("Takes his stance. He's earned that one.", [KAMPF("berge_12_wolff_hart"), WEITER("bg_weg_c_sieg")])],
       personen=H1("wolff"), sets=SETS_("wolff")),
]
NACH_C = [{"wenn": {"flag": "bg_panther_gehetzt"}, "id": "bg_weg_c_petru"}, {"id": "bg_weg_c_ende"}]
FRAMES += [
    FR("bg_weg_c_sieg", 12, "bergerie_dusk_exterior", "Fallen in Action",
       "Wolff sits on the wall, breathing hard, and goes through the pictures one by one. When he gets to the bear he "
       "stops for a long time. Then he looks at the words on his sword, Honneur et Fidélité, and puts it away.",
       [Z("wolff", "We swore an oath. To the Legion. Not to a company, and not to a man who keeps animals in cages.",
          "anger"),
        Z("wolff", "Caporal Adrien Morel died in action on this mountain. I will write it myself. Tonight.", "sadness")],
       [O("Gives him a hand up.", [WEITER(NACH_C)])],
       personen=H1("wolff"), sets=SETS_("wolff")),
    FR("bg_weg_c_ende", 12, "bergerie_interior", "A Dead Man at the Bergerie",
       "Adrien laughs until his bandages hurt. Laetitia doesn't laugh. She sits down next to him and holds his hand, "
       "and that is the answer to the question her father will ask.",
       [Z("adrien", "A dead man needs a job. I'll keep the bergerie. Come up whenever you need someone who knows the "
                    "mountain.", "gratitude"),
        Z("laetitia", "I'm staying with him. Tell Papa I'll come down on Sunday. Tell him I said Sunday.", "caring")],
       [O("Promises to tell him exactly that.",
          [F("bg_weg_c_gewonnen"), F("bg_adrien_bergerie"), F("bg_fotos_duc"), V("petru", STUFE),
           WEITER("bg_hafen_c")])],
       personen=H1("adrien", "laetitia"), sets=SETS_("adrien", "laetitia")),
    FR("bg_weg_c_petru", 12, "bergerie_dusk_exterior", "Between Them",
       "When Wolff came at you, Petru stepped in front of his daughter with his old rifle and caught the blow meant for "
       "her on his right hand. Now he sits on the wall with it wrapped in Laetitia's scarf and doesn't complain.",
       [Z("petru", "Hm. It was a good hand. Forty years of nets.", "sadness"),
        Z("laetitia", "Papa, it's broken. It's completely… why did you do that?", "grief"),
        Z("petru", "Because the old woman dreamed you. And I'm your father. That's all.", "caring")],
       [O("Splints the hand as well as he can.",
          [F("bg_weg_c_gewonnen"), F("bg_adrien_bergerie"), F("bg_fotos_duc"), F("petru_hand_steif"),
           V("petru", STUFE), WEITER("bg_hafen_c")])],
       personen=H1("petru", "laetitia"), sets=SETS_("petru", "laetitia")),
]


# ------------------------------------------------------------------ Abschluss am Hafen
def HAFEN(id, lage, zeilen, folgen):
    return FR(id, 13, "petru_workshop", "The Boathouse", lage, zeilen,
              [O("Stays a while.", folgen + [F("berge_fertig"), EXP_ENDE])], personen=H1("petru"), sets=SETS_("petru"))


FRAMES += [
    HAFEN("bg_hafen_a", "Laetitia walks past the boathouse without looking in. Petru watches her go up to the house. "
                        "Then he turns to you.",
          [Z("petru", "She's home. Thank you, Officer. She won't speak to you again. Maybe not to me either. But she's "
                      "home.", "sadness")], [V("petru", STUFE)]),
    HAFEN("bg_hafen_b", "The boathouse is dark. Petru is sitting in it anyway. Somebody from the village has already "
                        "told him about Totò's boat.",
          [Z("petru", "Get out of my workshop.", "anger")], [DATIERT("petru_werkstatt_zu_duc")]),
    HAFEN("bg_hafen_c", "Petru listens without a word. When you get to Sunday, he puts the net down.",
          [Z("petru", "Sunday. Hm. I'll make the fish pie.", "caring")], []),
]

# ------------------------------------------------------------------ Umweg 1: Old Grey (Ghjuvan, die Baerin)
U1 = [
    FR("bg_u1_hochweide", "U1", "high_pasture", "The Last Shepherd",
       "Ghjuvan leans his shotgun against the fold and talks without looking at you, as if he had said it to the sheep "
       "too many times already.",
       [Z("ghjuvan", "Five generations on this pasture. My grandfather, my father, me. We never sold a metre.",
          "pride"),
        Z("ghjuvan", "Then the bank. Then the men in black suits, twice, with a pen and a very good price. And now a bear. "
                     "There are no bears on Corsica. Every night, one sheep.", "fear"),
        Z("ghjuvan", "Ten more and I sign. Kill it. Please. I have my father's knife and forty sheep. That's "
                     "everything.", "grief")],
       [O("“Show me where it comes from.”", [F("bg_u1_angenommen"), WEITER("bg_u1_pfad")],
          zeile=Z("ghjuvan", "Along the goat path. You'll see. You'll wish you hadn't.", "sadness")),
        O("“I'll come back for it. I promise.”", [F("bg_u1_angenommen"), WEITER("bg_kamm")],
          zeile=Z("ghjuvan", "Everybody promises. The bear comes anyway.", "disappointment"))],
       personen=H1("ghjuvan"), sets=SETS_("ghjuvan")),
    FR("bg_u1_start", "U1", "high_pasture", "Ghjuvan's Pasture",
       "Ghjuvan is counting again. Thirty-eight. He doesn't say anything. He just looks at you.",
       [Z("ghjuvan", "Two more last week. Go, Officer. Please go.", "grief")],
       [O("Takes the goat path.", [F("bg_u1_angenommen"), EXP, WEITER("bg_u1_pfad")]), O("Not today, Ghjuvan.", [])],
       personen=H1("ghjuvan"), sets=SETS_("ghjuvan")),
    FR("bg_u1_pfad", "U1·1", "goat_path", "The Goat Path",
       "Three goats lie along the path, a few steps apart. They are torn open and not eaten. Something killed them for "
       "nothing. Two feral dogs have found them first and they don't want to share.",
       [],
       [O("Drives the dogs off the path.", [KAMPF("berge_u1_hunde"), WEITER("bg_u1_huette")])]),
    FR("bg_u1_huette", "U1·2", "summer_hut_fire", "Ghjuvan's Summer Hut",
       "Ghjuvan has come up after you with a pot of soup. He sits by the fire with the shotgun across his knees and "
       "talks to the flames.",
       [Z("ghjuvan", "My wife used to sing up here. Badly. The sheep loved it. Since she died they don't come when I "
                     "call.", "sadness"),
        Z("ghjuvan", "If I sign, the men in black put a fence round it and the pasture is gone. Five generations, and I'm "
                     "the one who ends it.", "grief")],
       [O("Eats the soup and listens.", [V("ghjuvan", 4), WEITER("bg_u1_dickicht")])],
       personen=H1("ghjuvan"), sets=SETS_("ghjuvan")),
    FR("bg_u1_dickicht", "U1·3", "bear_thicket", "Something Small",
       "A high, thin squeal from the alders. Then it steps out: a bear cub, fat and clumsy, with a blinking red collar "
       "of its own. It stares at you. A second little face peers out of the bushes behind it.",
       [],
       [O("Freezes.", [KAMPF("berge_u1_junges"), WEITER("bg_u1_hoehle")])]),
    FR("bg_u1_hoehle", "U1·4", "bear_den", "Old Grey",
       "The den smells of wet fur and old bones. She is enormous and grey at the muzzle, and the collar has cut so deep "
       "into her neck that the fur has grown over the light. Somewhere behind her, the cubs are crying.",
       [],
       [O("Plants Le Large in the ground. “Come on, then.”", [KAMPF("berge_u1_old_grey"), WEITER("bg_u1_wahl")])]),
    FR("bg_u1_wahl", "U1·5", "bear_den", "The Mother",
       "Old Grey lies on her side and breathes like a bellows. The red light blinks under her fur. The cubs have "
       "crawled up against her belly and are shaking. She is still trying to get up between you and them.",
       [],
       [O("Ends it, quickly, for Ghjuvan.",
          [F("bg_baer_getoetet"), I("topas"), G(120), WEITER("bg_u1_getoetet")]),
        O("Takes out his knife. “Hold still.” Cuts the chip out of her neck.",
          [DATIERT("bg_baer_frei"), I("control_chip"), WEITER("bg_u1_frei")])]),
    FR("bg_u1_getoetet", "U1·6", "high_pasture", "Forty Sheep",
       "Ghjuvan listens to it all and then sits down in the grass among his sheep. He takes his father's knife off his "
       "belt and holds it out to you, handle first.",
       [Z("ghjuvan", "You saved five generations today. Take it. My father would want it in a hand that did something.",
          "gratitude"),
        Z("ghjuvan", "…The little ones. Will they make it, without her?", "sadness")],
       [O("Doesn't answer. Takes the knife.", [I("ghjuvan_knife"), V("ghjuvan", STUFE), F("bg_u1_fertig"),
                                                 WEITER(NACH_U2)])],
       personen=H1("ghjuvan"), sets=SETS_("ghjuvan")),
    FR("bg_u1_frei", "U1·6", "high_pasture", "You Let It Live",
       "Ghjuvan stares at the chip in your hand, then at you.",
       [Z("ghjuvan", "She has cubs. I understand. I have sheep. Do you understand that?", "anger"),
        Z("ghjuvan", "She will be hungry and she will have three mouths. You know where she'll come.", "fear")],
       [O("“Without the chip she'll stay in the mountains. I'm sure of it.”", [V("ghjuvan", -4), F("bg_u1_fertig"),
                                                                                WEITER(NACH_U2)],
          zeile=Z("ghjuvan", "You're sure. Good. Then I'll sleep tonight.", "disapproval"))],
       personen=H1("ghjuvan"), sets=SETS_("ghjuvan")),
    FR("bg_u1_wieder_tot", "U1", "bear_den", "Two Cubs",
       "You go back to Old Grey's den once more. You don't know why. The two cubs are lying in front of it, curled up against "
       "each other in the sun. One of them lifts its head when you come. The other one doesn't.",
       [],
       [O("Stays until the light goes.", [F("bg_u1_junge_gesehen")])]),
    FR("bg_u1_wieder_leer", "U1", "high_pasture", "Sold",
       "Ghjuvan's fold is empty. A new fence runs across the pasture, and on the gate hangs a white sign with a small logo. "
       "A.V. Estates. Private property. On the doorstep of the farmhouse lies a shepherd's crook nobody picked up.",
       [],
       [O("Walks back down.", [F("bg_u1_verkauft_gesehen")])]),
]

# ------------------------------------------------------------------ Umweg 2: The Mazzera's Dream (Dumenica, Panther)
U2 = [
    FR("bg_u2_huette", "U2", "mazzera_hut", "The Mazzera",
       "Inside, the hut is all herbs and candles. Dumenica pours you something bitter in a cup without a handle and "
       "sits down so close that her knees touch yours.",
       [Z("dumenica", "I hunt when I sleep, my son. Every night. And the beast I kill in the dream always has a face.",
          "neutral"),
        Z("dumenica", "Last night it was black, with yellow eyes. And it had the face of Petru's girl.", "fear"),
        Z("dumenica", "Kill the beast while you are awake, and the dream breaks. That is the only way. I'm too old to do "
                      "it.", "sadness")],
       [O("“Where is it?”", [F("bg_u2_angenommen"), WEITER("bg_u2_kamm")],
          zeile=Z("dumenica", "Up on the ridge, at night, you'll see the lights. Follow the lights.", "neutral")),
        O("“I don't believe in dreams. But I'll look.”", [F("bg_u2_angenommen"), WEITER("bg_hochweide")],
          zeile=Z("dumenica", "Nobody believes. Then they come back to me, afterwards. Go.", "sadness"))],
       personen=H1("dumenica"), sets=SETS_("dumenica")),
    FR("bg_u2_start", "U2", "mazzera_hut", "Dumenica's Hut",
       "The candle is burning in the window again. Dumenica opens the door before you knock.",
       [Z("dumenica", "I dreamed the black beast again. Closer.", "fear")],
       [O("Goes up to the ridge.", [F("bg_u2_angenommen"), EXP, WEITER("bg_u2_kamm")]), O("Not tonight.", [])],
       personen=H1("dumenica"), sets=SETS_("dumenica")),
    FR("bg_u2_kamm", "U2·1", "ridge_night_lights", "Lights on the Ridge",
       "Night. Red lights move along the ridge in the fog, slow, in a line. Not torches. Infrared lamps. Two men in "
       "black, and one of them is holding a grey handset with a dial, turning it like a radio.",
       [],
       [O("Moves in before they can call anyone.", [KAMPF("berge_u2_agenten"), WEITER("bg_u2_geraet")])]),
    FR("bg_u2_geraet", "U2·1", "ridge_night_lights", "The Controller",
       "The handset is still warm. On its little screen a dot is moving, further up the mountain. Next to the dot it "
       "says PANTHERA 02 and a percentage, falling. They weren't hunting the beast. They were steering it, like a dog, "
       "to sniff out Adrien.",
       [],
       [O("Pockets the controller.", [I("ir_controller"), F("bg_u2_geraet"), WEITER("bg_u2_huette_leer")])]),
    FR("bg_u2_huette_leer", "U2·2", "abandoned_mountain_hut", "An Empty Hut",
       "A hut on the way to the dot, and nobody has lived in it for a long time. A little wooden dog stands on the table, the only thing without dust. When you come back out, Dumenica is "
       "standing in the dark by the door. She must have followed you up the whole way.",
       [Z("dumenica", "My son's. Twenty years ago I dreamed his face. I told him. He laughed. A week later the mountain "
                      "kept him.", "grief"),
        Z("dumenica", "I dust his dog every Sunday. Only the dog. I can't touch the rest.", "sadness")],
       [O("Puts a hand on her shoulder. Then keeps going.", [V("dumenica", 4), WEITER("bg_u2_hunde")])],
       personen=H1("dumenica"), sets=SETS_("dumenica")),
    FR("bg_u2_hunde", "U2·3", "ravine_fork", "The Pack",
       "Barking ahead, wild and close. A pack of feral dogs has the black beast's scent and is hunting it up the "
       "ravine, and you are standing in their way.",
       [],
       [O("Stands his ground.", [KAMPF("berge_u2_hunde"), WEITER("bg_u2_lager")])]),
    FR("bg_u2_lager", "U2·4", "panther_lair", "The Black Beast",
       "In a crack in the rock lies a panther, black, thin to the bone. The collar has been burned into its fur. It "
       "doesn't hide. It drags itself out to meet you like something that only wants it to be over.",
       [],
       [O("Lifts his weapon.", [KAMPF("berge_u2_panther"), WEITER("bg_u2_wahl")])]),
    FR("bg_u2_wahl", "U2·5", "panther_lair", "Awake or Dreaming",
       "The panther lies at your feet. Behind it, deep in the crack, something hangs from a red thread: a crescent of "
       "boar tusk with raven feathers and a pale moonstone. Somebody hung it there long before the collar, and you take "
       "it. The controller in your pocket is buzzing. On its screen there are three more dots "
       "now, up on the ridge, coming down towards the bergerie. The agents. And one dial that would turn the beast "
       "around and send it at them.",
       [],
       [O("Ends it, here, awake, the way Dumenica asked.",          # Mazzera-Charm: Unikat der Berge (Duc 28.10.2026)
          [{"charm": "mazzera"}, DATIERT("bg_panther_erloest"), WEITER("bg_u2_erloest")]),
        O("Turns the dial. Sends the beast at its masters.", [{"charm": "mazzera"}, F("bg_panther_gehetzt"), WEITER("bg_u2_gehetzt")])]),
    FR("bg_u2_erloest", "U2·6", "mazzera_hut", "The Dream Breaks",
       "Dumenica cries without making a sound. Then she takes a little silver hand off her own neck and puts it round "
       "yours.",
       [Z("dumenica", "It's broken. I feel it. The girl will live. Wear this, so you always wake up.", "relief"),
        Z("dumenica", "…But something is still looking for her. I can feel that too.", "fear")],
       [O("Thanks her. Doesn't tell her about the three dots on the screen.",
          [I("dumenica_amulet"), V("dumenica", STUFE), F("bg_u2_fertig"), WEITER(NACH_U2)])],
       personen=H1("dumenica"), sets=SETS_("dumenica")),
    FR("bg_u2_gehetzt", "U2·6", "ridge_night_lights", "Screams in the Dark",
       "The panther gets up as if someone had pulled it on a string, and runs. A minute later the screaming starts on "
       "the ridge, men's voices, three of them, then fewer. Then the beast itself screams, high and long, as the chip "
       "burns out. Then nothing. When you come down, Dumenica is standing at the lake with a candle.",
       [Z("dumenica", "I heard it die. In the dark. Screaming. Exactly as I dreamed it.", "fear"),
        Z("dumenica", "Then the dream is true. The girl will die. I have to tell Petru. I have to tell him now.", "grief")],
       [O("“Dumenica, wait. It doesn't mean…”", [F("bg_u2_fertig"), F("bg_petru_weiss"), WEITER(NACH_U2)],
          zeile=Z("dumenica", "It always means. That is the curse, my son. It always means.", "sadness"))],
       personen=H1("dumenica"), sets=SETS_("dumenica")),
]

# ------------------------------------------------------------------ Wiederkommen
WIEDER = [
    FR("bg_wieder", 1, "chestnut_switchbacks", "Back in the Chestnut Woods",
       "The switchbacks are quieter now. Something still rustles under the chestnuts, and the tower is still up there.",
       [],
       [O("Hunts along the ridge for collars.", [EXP, KAMPF("berge_7_agent"), WEITER("bg_wieder_ende")]),
        O("Climbs up to the bergerie.", [EXP, WEITER("bg_wieder_bergerie")]),
        O("Just walks, and turns back at the clearing.", [])],
       ton="wholesome"),
    FR("bg_wieder_bergerie", 10, "bergerie_interior", "The Bergerie",
       "Adrien is splitting wood with one arm. He lifts the axe in greeting.",
       [Z("adrien", "The dead man says hello. Coffee? It's terrible. Laetitia says it's the best on the mountain.",
          "amusement")],
       [O("Has the terrible coffee.", [WEITER("bg_wieder_ende")])],
       personen=H1("adrien"), sets=SETS_("adrien"), ton="wholesome"),
    FR("bg_bergerie_zurueck", 10, "bergerie_interior", "Back at the Bergerie",
       "Laetitia lowers the rifle when she sees it's you. Adrien is pale and sweating. Outside, the light is going.",
       [Z("laetitia", "You came back. Good. They'll come tonight, I can feel it.", "fear")],
       [O("Checks his weapon and waits by the door.", [EXP, WEITER(BOSS)]), O("Goes back down for now.", [])],
       personen=H1("laetitia", "adrien"), sets=SETS_("laetitia", "adrien")),
    FR("bg_wieder_ende", 1, "chestnut_switchbacks", "The Way Down",
       "The way down always takes longer than the way up.",
       [],
       [O("Heads back to the boat.", [EXP_ENDE])], ton="wholesome"),
    FR("bg_wolff_verloren", 12, "bergerie_dusk_exterior", "The Law, After All",
       "When you come to, Adrien is already in cuffs. Wolff is sitting on the wall with the camera on his knees. He "
       "hasn't looked at it. He won't now.",
       [Z("wolff", "You fought well. It changes nothing. I am taking him down.", "neutral"),
        Z("laetitia", "Get out. Get out of here.", "anger")],
       [O("Goes.", [EXP, F("bg_laetitia_schweigt"), F("bg_fotos_weg"), F("bg_adrien_verhaftet"), WEITER("bg_hafen_a")])],
       personen=H1("wolff", "laetitia"), sets=SETS_("wolff", "laetitia")),
]

FRAMES += U1 + U2 + WIEDER

# ------------------------------------------------------------------ Spaeter: Anrufe, die wehtun
H = lambda anrufer, ort: {"anrufer": anrufer, "anrufer_ort": ort, "art": "video"}
NACHHER = [
    E("hy_ghjuvan_tot", "handy", "ernst", "Ghjuvan", WANN((10, 21), ["tag", "nachmittag", "abend"], bed={"flag_seit": ["bg_baer_frei", 2]}), ORT_DUC,
      H("petru", "petru_workshop"),
      "Petru calls. He never calls. Behind him you can hear the radio, turned off, and the harbour.",
      [Z("petru", "Ghjuvan Santucci. The shepherd. They found him this morning on his pasture.", "grief"),
       Z("petru", "The bear you let live came down in the night with her young. He went out with the shotgun for his last sheep. "
                  "Hm. Forty sheep.", "sadness"),
       Z("petru", "The men in black were at the funeral. With flowers. And a pen.", "anger")],
      [O("Says nothing for a long time. Then: “Thank you for telling me.”", [F("bg_ghjuvan_tot")]),
       O("“That's on me, Petru.”", [F("bg_ghjuvan_tot"), V("petru", 2)],
         zeile=Z("petru", "On you, on the bear, on the bank. On the men with the pen. Mostly on them.", "sadness"))],
      sets=SETS_("petru")),
    E("hy_dumenica_huette", "handy", "ernst", "Smoke by the Lake", WANN((10, 21), ["tag", "nachmittag", "abend"], bed={"flag_seit": ["bg_panther_erloest", 2]}),
      ORT_DUC, H("petru", "petru_workshop"),
      "Petru, short of breath, as if he'd run to the phone.",
      [Z("petru", "The old woman's hut by the lake burned down last night. Dumenica. They found her sitting outside "
                  "in the grass, holding a little wooden dog.", "fear"),
       Z("petru", "She said men in black were looking for someone and didn't find him. So they found her hut. She is "
                  "alive. She says she didn't dream it. That's what frightens her.", "sadness")],
      [O("“Bring her to the village. I'll pay for whatever she needs.”", [G(-100), F("bg_dumenica_unterkunft")],
         zeile=Z("petru", "Hm. She can have Laetitia's room. Until.", "caring")),
       O("Tells him to keep her safe.", [F("bg_dumenica_obdachlos")])],
      sets=SETS_("petru")),
]

# ------------------------------------------------------------------ Nach Weg B: Laetitias Karte und Petrus Versoehnung
# Duc + Brain Trust 29.10.2026: Der Rauswurf bleibt nicht folgenlos (dunkler Laden, kern/abbau.petru_kalt), aber es gibt eine
# Bruecke. Adrien hatte eine Karte versprochen ("From somewhere without mountains"); Totò bringt sie, Duc muss sie selbst
# zu Petru tragen. Die -40 Vertrauen bleiben, Fish Pie gibt es nur in Weg C. Meramie (Petrus alte Jacke) kommt hier spaet.
NACHHER += [
    E("bg_b_postkarte", "gag1", "ernst", "A Postcard from Somewhere Flat",
      WANN((8, 21), ["fruehstueck", "tag", "nachmittag"], bed={"alle": [{"flag_seit": ["petru_werkstatt_zu_duc", 3]},
                                                                   {"nicht": {"flag": "petru_versoehnt"}}]}),
      "village_harbour", H1("toto", "petru"),
      "Totò catches you on the quay and presses a postcard into your hand. On the front, a town you don't know, flat as "
      "a plate. On the back, in biro, a blue boat on trestles, and one line: “Papa – the sea is different here. Not "
      "better. – L.”",
      [Z("toto", "From our two runaways, Comandante, Laetitia and her soldier. It came to my cousin in Bastia. It's not for me. And I don't think "
                 "it's for you either.", "caring")],
      [O("Takes it to Petru.", [F("petru_karte_bringen")]),
       O("Keeps it for now.", [DATIERT("petru_karte_behalten")])],
      sets=SETS_("toto")),
    E("bg_b_versoehnung", "gag1", "ernst", "The Radio",
      WANN((8, 21), ["tag", "nachmittag", "abend"],
           bed={"alle": [{"eine": [{"flag": "petru_karte_bringen"}, {"flag_seit": ["petru_karte_behalten", 2]}]},
                         {"nicht": {"flag": "petru_versoehnt"}}]}),
      "petru_workshop", H1("petru", "toto"),
      "The boathouse is dark again. You put Laetitia's postcard on the workbench, next to the net. Petru reads it. Then he "
      "reads it again.",
      [Z("petru", "Twelve years she wanted to leave. Twelve years I said nothing.", "sadness"),
       Z("petru", "She drew the boat. She still knows where the keel goes.", "caring"),
       Z("petru", "Take this. I wore it the night Marie, my wife, said yes. I was strong then, and stupid. Like you.", "caring")],
      [O("Takes the coat.", [F("petru_versoehnt"), F("jacke_jacket_water")]),
       O("Takes the coat, and switches the radio on for him.", [F("petru_versoehnt"), F("jacke_jacket_water"), V("petru", 2)])],
      sets=SETS_("petru"),
      nachklang_text="He puts the net down and switches the radio back on. Corsican football. He doesn't look up, but "
                     "he turns it a little louder."),
]

# ------------------------------------------------------------------ Meramie nach Weg C und Weg A (Duc 29.10.2026)
# Petrus alte Jacke aus der Zeit, als er jung und stark war - jeder Weg erzaehlt sie anders (Weg B: die Nacht, in der
# Marie ja sagte). C: warm, Abend an der Seekiste, die steife Hand aus dem Bosskampf. A: kuehl, die Jacke als Bezahlung.
# Freischalten wie in Weg B ueber das Flag jacke_jacket_water (kampf.freischalten-Konvention).
NACHHER += [
    E("bg_c_jacke", "gag1", "ernst", "The Sea Chest",
      WANN((9, 21), ["abend"], bed={"alle": [{"flag": "bg_weg_c_gewonnen"}, {"flag": "berge_fertig"},
                                             {"nicht": {"flag": "jacke_jacket_water"}}]}),
      "petru_workshop", H1("petru", "toto"),
      "Evening. The radio is off. Petru has pulled the old sea chest out from under the workbench. His splinted hand "
      "rests on the lid. Totò sits on a crate by the door and pretends not to listen.",
      [Z("petru", "When I was twenty, I could lift the mooring stone at the end of the quay. Alone. The whole village "
                  "came to watch.", "pride"),
       Z("petru", "I wore this that winter. On the tuna boats out of Bastia. Six weeks, and the sea never got through it.",
         "caring"),
       Z("petru", "This hand can't hold a net now. Hm. The coat still holds. Take it.", "caring")],
      [O("Puts the coat on.", [F("jacke_jacket_water")]),
       O("Puts the coat on, and lifts the chest back under the bench for him.", [F("jacke_jacket_water"), V("petru", 2)])],
      sets=SETS_("petru", "toto"),
      nachklang_text="It fits. Petru looks at you for a long moment. “Hm.” This one means yes."),
    E("bg_a_jacke", "gag1", "ernst", "Paid in Full",
      WANN((9, 21), ["tag", "nachmittag"], bed={"alle": [{"flag": "bg_adrien_verhaftet"}, {"flag": "berge_fertig"},
                                                          {"nicht": {"flag": "jacke_jacket_water"}}]}),
      "petru_workshop", H1("petru", "toto"),
      "A coat lies folded on the workbench when you come in. Navy wool, old brass buttons. Petru doesn't put the net "
      "down. Outside on the quay, Totò mends a fender and doesn't come in.",
      [Z("petru", "I wore this when I was young and strong. Twenty years at sea in it. It bought me my first boat.",
         "neutral"),
       Z("petru", "You brought my daughter home. Take it. We are even.", "sadness")],
      [O("Takes the coat.", [F("jacke_jacket_water")]),
       O("“She'll come round, Petru.”", [F("jacke_jacket_water")],
         zeile=Z("petru", "Hm. The sea doesn't hurry.", "sadness"))],
      sets=SETS_("petru", "toto"),
      nachklang_text="He goes back to the net. The radio stays off."),
]

EVENTS = [AUFTAKT] + FRAMES + NACHHER
