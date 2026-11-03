# -*- coding: utf-8 -*-
"""Ortskapitel "The Silence of San Martinu" - Macchia & Kloster (Akt 2, 26.10.2026, E-073/E-074).

Plot: docs/wiki/welt/ortskapitel_kloster.md. Gebaut als Frame-Kette (art "ort") im Format der spaeteren
Erkundung: jeder Frame ist ein Event mit eigenem Hintergrund, die Folge "weiter" oeffnet den naechsten Frame (nach einem
Kampf erst nach dem Sieg), ohne "weiter" ist der Ausflug vorbei und die Phase verbraucht (eden.py). Betreten wird die
Macchia in einer freien Phase ueber den Ort "macchia" (auftraege_eden_rise.py).

  Casanova (Hafen, Tag 8)  ->  kl_start .. kl_bau (Kaempfe der Kampf-Sitzung, kloster_<frame>_<gegner>)
  Gabelung: Spur-Uhr 4 -> Faehrte (-1) oder Felsnische (-3); Lager -1. Bei 0 ist Frederico tot (Ausgang B).
  Loewe: Leiden beenden (Steuerchip + Loewen-Chip) oder Chip herausschneiden (nur Steuerchip, Loewe hilft in Akt 3).
  Garten (mit/ohne Frederico) -> Hafen: Casanova, Le Large (waffe_spear), Auftrag fertig.
  Wiederkommen (kloster_fertig): Pfad jagen (leveln) oder die Felsnische nachholen.

Graue Entscheidungen (E-073, mindestens eine je Auftrag): Faehrte/Schatz und der Loewe."""
from ereignisse_basis import *  # noqa: F401,F403

SPUR = "kloster"
KAMPF = lambda bid: {"kampf": bid}
WEITER = lambda ziel: {"weiter": ziel}
UHR = lambda *a: {"spur_uhr": [SPUR] + list(a)}
EXP = {"expedition": "kloster"}
EXP_ENDE = {"expedition": "ende"}
ELICRISO = {"beibringen": "elicriso"}          # Heiler-Pfad H3, Nonna wie Maxwell mit Mistral (Kampf 656ba6a)
STUFE = 8                                    # Punkte je Vertrauensstufe
# Loewen-Chip: Familie und Stufe legt die Items-Sitzung fest (Anfrage 26.10.); solange None, entfaellt die Folge
LOEWEN_CHIP = ("auftritt", 2)          # "Cool Smile" (Items-Sitzung 26.10.)

item("control_chip", "Control Chip", "andenken",   # Andenken: kein Platz, kein Fall-Beweis; nach dem Loewen kein Kampf mehr
     text="A small black chip, grown into the lion's collar. Engraved: “A.V. Estates – Behaviour Control Unit”.")
# Andenken (ambrosius_keule, diary_page_1/2), steel_plate und agent_note legt die Items-Sitzung an (gegenstaende_eden_rise.py)


# Rastplaetze (Kampf 5c64589, Elden-Ring-Prinzip): "Rest by the fire" - LP voll, die Tiere kommen zurueck, ein Anruf.
RAST = {"kl_huette", "kl_kueche", "kl_lager", "kl_bachufer", "kl_schluchtfeuer", "kl_schluchtfeuer_kalt"}
# Fund-Karte beim ersten Erreichen eines Rastplatzes (Kampf 5db3323): Duc findet den Platz, jemand war vor ihm da.
FUND = {
    "kl_kueche": "Nonna's kitchen smells of bread and rosemary. Next to the stove there's a second chair, pulled up close, "
                 "the cushion worn flat, as if someone sat here every evening and waited. Tonight it's yours.",
    "kl_bachufer": "You almost walk past it. A ring of stones under the holm oak, and when you hold your hand over the ash, "
                   "it's still warm. Someone sat here, and not that long ago. By the water there's a cigarette end, and it "
                   "isn't a cheap one.",
    "kl_huette": "Someone has swept the floor of the hut. By the old hearth there's a neat pile of dry wood, the kind you "
                 "leave for whoever comes next. Shepherds do that. Or monks, maybe.",
    "kl_lager": "The brothers made their fire here. You can still see where they sat, flat stones in a circle, and one "
                "smaller stone a little apart from the others. That one must have been the boy's.",
    "kl_schluchtfeuer": "There's a fire on the ledge, and it's still burning. Nobody's here. Someone fed it not long "
                        "ago, the new wood hasn't even caught properly yet. They have to be close. Very close.",
    "kl_schluchtfeuer_kalt": "A fire pit on the ledge, and it's cold. The ash is grey and days old. Whoever made it "
                             "hasn't come back to it.",
}
# Rueckweg-Sperre: hinter diese Frames fuehrt "Go back" nicht mehr - sonst liessen sich Entscheidungen wiederholen
# (Kueche: Vertrauen; Gabelung: Spur-Uhr; Loewe: Leben oder Tod).
SPERRE = {"kl_waldrand", "kl_gabel", "kl_nische", "kl_lager", "kl_frederico", "kl_frederico_tot"}


def FR(id, nr, bild, titel, lage, zeilen, optionen, personen=None, sets=None, spur=False, ton="ernst"):
    """Ein Frame. nr = Frame-Nummer aus dem Drehbuch (Anzeige), spur = Spur-Uhr sichtbar."""
    e = E(id, "ort", ton, titel, WANN((8, 14)), bild, personen or {}, lage, zeilen, optionen, sets)
    e["frame"] = nr
    if spur:
        e["spur"] = SPUR
    if id in RAST:
        e["rast"] = True
    if id in SPERRE:
        e["sperre"] = True
    if id in FUND:
        e["fund"] = FUND[id]
    return e


def H1(handelnd, *betroffen):
    return {"handelnd": handelnd, "betroffen": [{"id": b, "ton": "?", "was": ""} for b in betroffen]}


# ------------------------------------------------------------------ Auftakt: Casanova am Hafen (Tag 8)
AUFTAKT = FR(
    "kl_casanova_auftrag", 0, "village_piazza", "The Mayor's Office",
    "The town hall smells of floor polish and old paper. Madame Casanova receives you under the portrait of her father, "
    "and for the first time since you met her there is no stage. No confetti, no speech. She closes the door herself.",
    [Z("casanova", "Fiora, from the monastery at San Martinu, has not missed a single market day in forty years. Not one. Since the animals came: no herbs, "
                   "no cheese, no letters from San Martinu.", "sadness"),
     Z("casanova", "You saw that goat at the harbour, didn't you? With the blinking light on her collar. Monsieur, I think the animals came from up there. And I "
                   "think the monks are in trouble.", "fear")],
    [O("Puts his hand flat on her desk. “I'll go up and look. Tell me the way.”",
       [F("kloster_angenommen"), V("casanova", 4), WEITER("kl_pascal_tuer")],
       zeile=Z("casanova", "Past the old bridge and keep climbing until the bells would be ringing. If there are any "
                           "bells left. Thank you.", "gratitude")),
     O("Weighs Terremoto in his hand. “If something's wrong up there, it won't stay up there. I'll go.”",
       [F("kloster_angenommen"), R(2), WEITER("kl_pascal_tuer")],
       zeile=Z("casanova", "That's what I was afraid you'd say. And what I hoped you'd say. Both at once.", "optimism")),
     O("“Who else knows about this?”", [F("kloster_angenommen"), WEITER("kl_pascal_tuer")],
       zeile=Z("casanova", "Nobody. Pascal, of course, Pascal knows everything. Nobody else I trust. Petru says the mountain "
                           "will speak when it wants to. I'm tired of waiting for mountains.", "annoyance")),
     O("“Give me a day or two to get ready.”", [],
       zeile=Z("casanova", "A day or two. The mountain has been patient for weeks. It will not be patient forever.",
               "sadness"))],
    personen={"handelnd": "casanova"}, sets={"casanova": "Standard"})


# ------------------------------------------------------------------ Der Weg
# nach dem Lager: das Feuer ueber der Schlucht - brennt noch, solange die Spur nicht abgelaufen ist (fair: kein
# "knapp verpasst", wenn Frederico schon tot ist)
NACH_LAGER = [{"wenn": {"flag": "spur_kloster_abgelaufen"}, "id": "kl_schluchtfeuer_kalt"}, {"id": "kl_schluchtfeuer"}]
# nach der Felsnische: beim ersten Besuch weiter zum Lager, beim Wiederkommen nach Hause
NACH_NISCHE = [{"wenn": {"flag": "kloster_fertig"}, "id": "kl_wieder_ende"}, {"id": "kl_lager"}]
FRAMES = [
    FR("kl_start", 1, "macchia_path", "The Macchia Path",
       "The path climbs between cistus and myrtle. Halfway up a cork oak stands with deep claw marks in the bark, at "
       "chest height. Far too big for a dog.",
       [],
       [O("Follows the claw marks up the path, bat ready.", [EXP, KAMPF("kloster_1_ratte"),
                                                              WEITER("kl_bachufer")]),
        O("Cuts through the cistus to stay out of sight.", [EXP, KAMPF("kloster_1_schlange"), WEITER("kl_bachufer")]),
        O("Turns back. “Not today.”", [])],
       ton="ernst"),
    FR("kl_bachufer", "1b", "creek_rest", "Under the Holm Oak",
       "The path dips down to the creek. Shade, cold water, a flat stone that fits your back exactly. The bridge can't be "
       "far now. Under the oak somebody has left a tin bowl and a note held down with a stone: *Eat this. Not the hikers. – B.*",
       [],
       [O("Fills his bottle and walks on.", [WEITER("kl_bruecke")])],
       ton="wholesome"),
    FR("kl_bruecke", 2, "macchia_creek_bridge", "The Stone Bridge",
       "A goat lies dead on the bank below the bridge. Around its neck is a collar with a red light that is still "
       "blinking. On the far side something heavy snorts and paws the ground.",
       [],
       [O("Steps onto the bridge before the boar can choose the moment.", [KAMPF("kloster_2_keiler"),
                                                                            WEITER("kl_huette")]),
        O("Climbs down to the goat first and reads the collar.",
         [KAMPF("kloster_2_keiler"), WEITER("kl_huette")], probe=P("perception", 12),
         erfolg=[F("kl_bcu_0417")], fehlschlag=[])]),
    FR("kl_huette", 3, "shepherd_hut_ruin", "The Shepherd's Hut",
       "The shepherd's hut has lost its roof. A thin dog stands in the doorway, ribs showing, a collar blinking at its "
       "throat. It doesn't bark. It just watches you. By the door there's a tin bowl, licked clean, with a note under it: *If you can read this, you are not a wolf. Please put the bowl back. – B.*",
       [],
       [O("Keeps walking, slow and steady, bat low.", [KAMPF("kloster_3_hund"), WEITER("kl_capra")]),
        O("Crouches and holds out half a sandwich. “Easy. I'm not here for you.”",
         [WEITER("kl_capra")], probe=P("empathy", 13),
         erfolg=[F("kl_hund_satt")], fehlschlag=[KAMPF("kloster_3_hund")])]),
    FR("kl_capra", 3, "shepherd_hut_ruin", "An Old Friend",
       "Behind the hut a goat is chewing on your bag. It is the goat from the harbour, the one that got away, and its "
       "collar is still blinking. It looks at you as if you're late.",
       [],
       [O("Gives her the rest of the sandwich. “Fine. You can come.”", [F("capra_dabei"), WEITER("kl_tor")]),
        O("Tries to shoo her away. She follows anyway.", [F("capra_dabei"), WEITER("kl_tor")])],
       ton="witzig"),
    FR("kl_tor", 4, "monastery_gate", "The Monastery Gate",
       "The gate of San Martinu is shut. On the wall above it stands a woman with silver hair and a wooden spoon, "
       "and she is holding the spoon like a sword.",
       [Z("nonna", "Stand still, or I'll cook you!", "anger"),
        Z("isabelle", "Nonna! He's a person.", "nervousness"),
        Z("nonna", "So are the monkeys, apparently. Look at the way they throw things.", "annoyance")],
       [O("Raises both hands. “Madame Casanova sent me. She's worried about you.”", [F("kl_tor_offen"),
                                                                                    WEITER("kl_kueche")],
          zeile=Z("nonna", "Casanova. Of course she did. Open the gate, Isabelle, before the goat eats the hinges.",
                  "amusement")),
        O("Points at the goat. “She vouches for me.”", [F("kl_tor_offen"), WEITER("kl_kueche")],
          zeile=Z("isabelle", "Oh! That's one of ours. Nonna, she came back!", "joy"))],
       personen=H1("nonna", "isabelle"), sets={"nonna": "nonna_standard", "isabelle": "isabelle_standard"},
       ton="witzig"),
    FR("kl_kueche", 4, "monastery_kitchen", "Nonna Fiora's Kitchen",
       "Bread, too much of it, cooling on every surface. Isabelle puts a bowl in front of you before you sit down. "
       "Then Nonna tells it. The animals came weeks ago, monkeys, dogs, and a lion, on Corsica. Brother Ambrosius "
       "took the brothers out to hunt it. Frederico, twelve, ran after them. Nobody came back. "
       "When you stand up, she presses a small bottle of yellow oil into your hand, everlasting from the macchia, and "
       "shows you how to use it on a burn.",
       [Z("nonna", "He carves everyone who lives here an animal. He wanted to do something important, just once.",
          "sadness"),
        Z("nonna", "He's been gone three days. Three days with no bread.", "grief"),
        Z("nonna", "A girl leaves bowls on my hill, too. I put soup in them when she is gone. She thinks the animals are doing very well.", "caring")],
       [O("Puts the spoon down. “I'll bring them back. All of them, if I can.”", [F("kloster_kueche"), ELICRISO, V("nonna", 4),
                                                                                  WEITER("kl_waldrand")],
          probe=P("courage", 12), erfolg=[V("isabelle", 4)], fehlschlag=[]),
        O("“Show me exactly where they went in.”", [F("kloster_kueche"), ELICRISO, WEITER("kl_waldrand")],
          probe=P("perception", 12), erfolg=[F("kl_spur_gelesen")], fehlschlag=[]),
        O("“Where did they camp the first night? Monks plan ahead.”", [F("kloster_kueche"), ELICRISO,
                                                                       WEITER([{"wenn": {"flag": "kl_abkuerzung"},
                                                                                "id": "kl_gabel"},
                                                                               {"id": "kl_waldrand"}])],
          probe=P("cunning", 13), erfolg=[F("kl_abkuerzung")], fehlschlag=[])],
       personen=H1("nonna", "isabelle"), sets={"nonna": "nonna_standard", "isabelle": "isabelle_standard"}),
    FR("kl_waldrand", 5, "forest_edge_cliffs", "The Forest Edge",
       "Where the trees end, the cliffs begin. A torn page is stuck on a thorn bush, the handwriting neat and "
       "careful. Above you, something with a blinking collar is sitting very still.",
       [],
       [O("Takes the page and reads it aloud, quietly.", [I("diary_page_1"), KAMPF("kloster_5_affe"),
                                                          WEITER("kl_gabel")]),
        O("Leaves the page and keeps his eyes on the ape.", [KAMPF("kloster_5_affe"), WEITER("kl_gabel")])]),
    FR("kl_gabel", 6, "ravine_fork", "The Fork in the Ravine",
       "The ravine splits in two. Two dogs come out of the left fork, low and growling, collars blinking in time. On a flat rock at the fork there's a tin bowl with a note beside it: *This one is for the hyenas. Everybody else, I can see you. – B.*",
       [],
       [O("Stands his ground at the fork.", [UHR("start", 4), KAMPF("kloster_6_hunde"), WEITER("kl_gabelung")])]),
    FR("kl_gabelung", 6, "ravine_fork", "Trail or Treasure",
       "Now you can see both ways. To the left, dark spots on the stones, a blood trail, and a small sandal lying "
       "on its side. To the right, high in the rock, something glints in a niche, metal in the sun. You can't do "
       "both quickly.",
       [],
       [O("Follows the blood trail. “A sandal that size… come on, kid.”", [UHR(-1), F("kl_faehrte"), WEITER("kl_lager")]),
        O("Climbs to the niche first. “Somebody hid that up there on purpose.”",
         [UHR(-3), F("kl_schatz"), WEITER("kl_nische")])],
       spur=True),
    FR("kl_nische", "6b", "hidden_rock_niche", "The Rock Niche",
       "The niche is deeper than it looked. A boar has made its bed in front of it, and an ape is crouching on the "
       "ledge above.",
       [],
       [O("Goes in anyway.", [KAMPF("kloster_6b_wildschwein_affe"),
                              WEITER([{"wenn": {"flag": "kl_nische_geleert"}, "id": "kl_nische_leer"},
                                      {"id": "kl_nische_fund"}])]),
        O("Leaves the niche for another day.", [WEITER(NACH_NISCHE)])],
       spur=True),
    FR("kl_nische_fund", "6b", "hidden_rock_niche", "What Someone Hid",
       "Wrapped in an oilcloth: a steel plate, cut clean, the kind Rosi would kiss. Tucked under it, a torn note in "
       "a hurried hand. G. – plate stays here till you come. Thursday, the late boat from Bastia. 400 or no deal, I'm not a charity. Burn this. On the back, someone has drawn the collar of a jacket in careful pencil.",
       [],
       [O("Takes the plate and the note.", [I("agent_note"), I("steel_plate"),
                                            WEITER([{"wenn": {"item": "steel_plate"}, "id": "kl_nische_eingepackt"},
                                                    {"id": "kl_nische_voll"}])])],
       spur=True),
    FR("kl_nische_eingepackt", "6b", "hidden_rock_niche", "Heavier Than It Looks",
       "The plate is heavier than it looks. You fold the note twice and put it in your shirt pocket. Who on earth is G.?",
       [],
       [O("Climbs back down.", [F("kl_nische_geleert"), WEITER(NACH_NISCHE)])],
       spur=True),
    FR("kl_nische_voll", "6b", "hidden_rock_niche", "No Room",
       "Your bag is already full. You wrap the plate back in the oilcloth and push it deep into the niche. It has "
       "waited this long, it can wait for you.",
       [],
       [O("Climbs back down.", [WEITER(NACH_NISCHE)])],
       spur=True),
    FR("kl_nische_leer", "6b", "hidden_rock_niche", "An Empty Niche",
       "The oilcloth is still there, folded the way you left it. Nothing else.",
       [],
       [O("Heads back down.", [WEITER(NACH_NISCHE)])]),
    FR("kl_lager", 7, "monks_camp_abandoned", "The Brothers' Camp",
       "Folded habits, a kettle on its side, ashes gone cold. The brothers' camp is very quiet. On a flat stone lies "
       "a second page, weighed down with a pebble, as if someone wanted it found.",
       [],
       [O("Reads the page.", [UHR(-1), I("diary_page_2"), KAMPF("kloster_7_affe"), WEITER(NACH_LAGER)]),
        O("Leaves the page under its pebble and keeps going.", [UHR(-1), KAMPF("kloster_7_affe"), WEITER(NACH_LAGER)])],
       spur=True),
    FR("kl_schluchtfeuer", "7b", "ravine_fire", "Fire on the Ledge",
       "Across the ravine the cave opens like a mouth. From here you can hear it breathing. Or maybe that's the wind.",
       [],
       [O("Checks the bat, then crosses over.", [WEITER("kl_bau")])],
       spur=True),
    FR("kl_schluchtfeuer_kalt", "7b", "ravine_fork", "Fire on the Ledge",
       "Across the ravine the cave opens like a mouth. It's very quiet over there.",
       [],
       [O("Checks the bat, then crosses over.", [WEITER("kl_bau")])],
       spur=True),
    FR("kl_bau", 8, "lion_den_cave", "The Lion's Den",
       "The cave smells of old blood. In the dark something enormous lifts its head. A lion, thin as a coat on a "
       "hook, with a steel plate bolted to each shoulder and four empty bolt holes over its heart. A red light at the back of its neck blinks with "
       "every breath.",
       [],
       [O("Grips Terremoto with both hands. “Okay. Okay.”", [KAMPF("kloster_8_loewe"), WEITER("kl_loewe_wahl")])],
       spur=True),
]

LOEWE_ERLOESEN = [F("kl_loewe_erloest"), I("control_chip")] + ([{"chip": list(LOEWEN_CHIP)}] if LOEWEN_CHIP else [])
NACH_LOEWE = [{"wenn": {"flag": "spur_kloster_abgelaufen"}, "id": "kl_frederico_tot"}, {"id": "kl_frederico"}]

FRAMES += [
    FR("kl_loewe_wahl", 8, "lion_den_cave", "The Lion",
       "The lion lies on its side and breathes hard. With the other animals the collar broke on its own. His didn't. "
       "The chip has grown into the skin at the back of his neck, and the red light keeps blinking. He looks at you "
       "and doesn't try to get up.",
       [],
       [O("Kneels beside him. “I'm sorry.” Ends it, quickly, the way the brothers meant to.",
         LOEWE_ERLOESEN + [WEITER(NACH_LOEWE)]),
        O("Takes out his knife. “Hold still. This is going to hurt, and then it's over.” Cuts the chip out.",
         [F("kl_loewe_frei"), I("control_chip"), WEITER(NACH_LOEWE)])]),
    FR("kl_frederico", 8, "lion_den_cave_b", "Someone Good",
       "Behind a boulder at the back of the cave something moves. A boy, twelve at most, holding a golden club that "
       "is far too big for him.",
       [Z("frederico", "Are you… are you a person?", "fear")],
       [O("Lowers the bat. “With a goat.”", [F("kloster_frederico_lebt"), I("ambrosius_keule"),
                                            WEITER("kl_garten")],
          zeile=Z("frederico", "Brother Ambrosius said I should hide and wait until someone good came. This was his. "
                               "He would have wanted you to have it.", "gratitude"))],
       personen=H1("frederico"), sets={"frederico": "frederico_standard"}, ton="wholesome"),
    FR("kl_frederico_tot", 8, "lion_den_cave_b", "Too Late",
       "Behind the boulder lies Frederico, a little wooden goat in his hand. Next to him lies Brother Ambrosius, the "
       "golden club beside him. Nobody says anything, because there's nobody left to say it.",
       [],
       [O("Takes the wooden goat. Carries it all the way down.", [F("kloster_frederico_tot"),
                                                                 WEITER("kl_garten_ohne")])]),
    FR("kl_garten", 9, "monastery_garden_dusk", "Home Before Dark",
       "Frederico runs the last stretch. Isabelle catches him before he reaches the gate. Nonna sits down on the wall, "
       "very slowly, as if her knees have only just remembered how old they are.",
       [Z("nonna", "And the brothers?", "fear"),
        Z("nonna", "Ambrosius always baked his bread too dark. Brother Paolo snored while he prayed. Brother Teo greeted "
                   "the bees every morning, one by one, by name.", "grief"),
        Z("nonna", "…Thank you for bringing the boy home.", "gratitude")],
       [O("“None of them.” Sits down next to her and stays a while.",
         [V("nonna", STUFE), V("isabelle", STUFE), F("kloster_berg_fertig"), F("isabelle_handy"),  # Ducs Nummer (Selfies)
          WEITER("kl_hafen_lebt")])],
       personen=H1("nonna", "isabelle"), sets={"nonna": "nonna_standard", "isabelle": "isabelle_standard"}),
    FR("kl_garten_ohne", 9, "monastery_garden_dusk", "The Wooden Goat",
       "Isabelle takes the wooden goat out of your hand and says nothing. Nonna looks at it for a long time. Then she "
       "goes into the house and closes the door behind her.",
       [],
       [O("Waits until the light goes out in the kitchen. Then walks down.", [F("kloster_berg_fertig"),
                                                                              WEITER("kl_hafen_tot")])]),
]


# ------------------------------------------------------------------ Abschluss: Casanova, Le Large
def ABSCHLUSS(id, erste, gefuehl, danach):
    return FR(id, 10, "village_harbour", "Le Large",
              "Madame Casanova listens without making a speech, and that alone tells you how serious it is. Then she "
              "goes into her house and comes back with an old hunting spear, a brass cartridge on the shaft and "
              "something blue set in the spearhead.",
              [Z("casanova", erste, gefuehl),
               Z("casanova", "My father carried this when the boars came down into the village, the winter I was born. "
                             "He named it after the open sea, because he always said that's where courage comes from.",
                 "pride"),
               Z("casanova", "You bring our news down from the mountain. You should carry it now.", "caring")],
              [O("Takes Le Large with both hands.", [F("waffe_spear"), F("kloster_fertig"), V("casanova", STUFE),
                                                     W("ruf", 1), UHR("aus"), EXP_ENDE, WEITER(danach)])],
              personen=H1("casanova"), sets={"casanova": "Standard"})


FRAMES += [
    ABSCHLUSS("kl_hafen_lebt", "The boy will bring the herbs and cheese down now? Then the mountain is breathing again.", "relief", "kl_totenfeier_lebt"),
    ABSCHLUSS("kl_hafen_tot", "Then we carry them in our names. All of them.", "grief", "kl_totenfeier_tot"),
]

# ------------------------------------------------------------------ Wiederkommen (nach dem Auftrag)
FRAMES += [
    FR("kl_wieder", 1, "macchia_path", "Back in the Macchia",
       "The claw marks in the cork oak have grown over a little. The macchia is quieter than last time, but not "
       "empty. Something still rustles in the cistus.",
       [],
       [O("Hunts along the path for collars.", [EXP, KAMPF("kloster_1_ratte"), WEITER("kl_wieder_ende")]),
        O("Climbs up to the rock niche.", [EXP, WEITER("kl_nische")]),
        O("Just walks, and turns back at the bridge.", [])],
       ton="wholesome"),
    FR("kl_wieder_ende", 1, "macchia_path", "The Way Down",
       "The sun is lower than you expected. The way down always takes longer than the way up.",
       [],
       [O("Heads back to the boat.", [EXP_ENDE])],
       ton="wholesome"),
]

EVENTS = [AUFTAKT] + FRAMES
