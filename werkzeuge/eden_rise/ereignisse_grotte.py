# -*- coding: utf-8 -*-
"""Strand-Dungeon "The Smugglers' Grotto" und Kevins Daecher (Akt 2 Woche 2, Duc 27.10.2026: "2 Umwege und Nebenquest
mit viel Grau und Tragik, inszeniere preisgekroent").

Plot: docs/wiki/welt/ortskapitel_grotte.md. Gebaut wie die Berge (ereignisse_berge.py): Frame-Kette (art "ort"),
"weiter" oeffnet den naechsten Frame, nach einem Kampf erst nach dem Sieg. Uhr = die Ebbe: wer Bastien befreit, kommt zu
spaet zu Gennaro (gr_spaet: Gennaros Haende, Boss +1).

  Totò gesteht (Tag 11, ereignisse_akt2.py) -> gr_start .. gr_zelle (Gennaro, Sussurro) -> U Riscossore -> die Kiste
  Umweg 1 "The Second Brother"   Matteu taucht fuer die Moerder seines Bruders: Wahrheit (er stirbt im Bosskampf) oder
                                 Luege (er lebt und arbeitet weiter fuer sie)
  Umweg 2 "The Price of the Tide" Chloé und Bastien: Bastien befreien (Gennaro bezahlt mit den Haenden) oder Gennaro zuerst
                                 (Bastien ertrinkt)
  Kevins Daecher (Tag 12-14): die Seite aus Leas Kartenbuch zurueckholen, Mini-Boss Kevin

Graue Entscheidungen (E-073): Matteu, Bastien, die Kiste. Jede Seite kostet etwas."""
from ereignisse_basis import *  # noqa: F401,F403

KAMPF = lambda bid: {"kampf": bid}
WEITER = lambda ziel: {"weiter": ziel}
EXP = {"expedition": "grotte"}
EXP_ENDE = {"expedition": "ende"}
STUFE = 8
DATIERT = lambda name: {"flag_datiert": name}

# Hintergruende: Wunschbild (Auftrag an Character Design 27.10.) -> vorhandener Platzhalter, bis es abgenommen ist
WUNSCH = {"grotto_steps": "hafen_abend", "drowned_beach": "strand_lagerfeuer", "smugglers_tunnel": "lion_den_cave_b",
          "crate_hall": "lion_den_cave", "underground_pool": "hidden_rock_niche", "torch_gallery": "ravine_fire",
          "gennaro_cell": "hidden_rock_niche", "flooded_gallery": "lion_den_cave_b", "air_pocket": "hidden_rock_niche",
          "collapsed_passage": "lion_den_cave", "treasure_camp": "creek_rest", "village_rooftops": "piazza_treppe",
          "bell_tower_nest": "piazza_treppe",
          "underground_pool_tide": "underground_pool"}          # Flut-Nacht (28.10.2026): Teich bei Flut im Mondlicht


def _bg_da(name):
    try:
        cfg = json.load(open(os.path.join(EDEN, "eden-config.json"), encoding="utf-8-sig"))
        return os.path.isfile(os.path.join(cfg["st_daten"], "backgrounds", "eden_rise_%s.png" % name))
    except Exception:
        return False


def BILD(name):
    return name if name not in WUNSCH or _bg_da(name) else WUNSCH[name]


RAST = {"gr_strand", "gr_zelle", "gr_zelle_spaet", "gr_u1_luft", "gr_u2_lager"}
SPERRE = {"gr_wahl", "gr_u1_wahl", "gr_u2_wahl", "kv_nest"}
FUND = {
    "gr_strand": "A cheap plastic lighter, half buried in the wet sand, with a sticker of a cartoon pony on it. Next to "
                 "it, folded small and nearly dry, a child's drawing: a man with a big moustache in a boat, and "
                 "underneath, in crooked letters, PAPÀ.",
    "gr_zelle": "Scratched into the rock beside the ring bolt: a row of little lines, and a name, GIULIA. His "
                "daughter. He counted the tides for her.",
    "gr_u1_luft": "Tally marks on the wall of the air pocket, scratched with a knife. Seven groups of five, and two "
                  "more. Thirty-seven tides. Somebody lived down here for eighteen days.",
    "gr_u2_lager": "A little velvet box at the bottom of Bastien's rucksack, under the spare batteries. Inside, a ring "
                   "with a tiny blue stone. The receipt is still in the box. He bought it in Marseille in March.",
}


def FR(id, nr, bild, titel, lage, zeilen, optionen, personen=None, sets=None, ton="ernst", tage=(11, 21)):
    e = E(id, "ort", ton, titel, WANN(tage), BILD(bild), personen or {}, lage, zeilen, optionen, sets)
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


S = {"toto": "Standard", "lea": "Dive", "gennaro": "gennaro_standard", "matteu": "matteu_standard",
     "chloe": "chloe_standard", "riscossore": "riscossore_standard", "sophia": "Concierge",
     "sirene": "sirene_standard"}


def SETS_(*pids):
    return {p: S[p] for p in pids}


# ------------------------------------------------------------------ Gegenstaende
item("gennaro_drawing", "Giulia's Drawing", "andenken",
     text="A child's drawing of a man with a big moustache in a boat. Underneath, in crooked letters: PAPÀ.")
item("collar_crate", "The Crate from Antibes", "quest",
     text="A heavy plastic crate with a stamped code and a small white logo. Inside, in foam, forty new collars and a "
          "box of control chips. You saw this crate before, in a hangar in Antibes.")
item("ghjacumu_medal", "Ghjacumu's Medal", "andenken",
     text="A small tin medal of Saint Erasmus, patron of sailors, on a green string. The string has been chewed.")
item("bastien_ring", "A Ring in a Velvet Box", "andenken",
     text="A ring with a tiny blue stone. The receipt is still in the box. Marseille, March.")
item("treasure_notes", "Chloé's Notes", "quest",
     text="A waterproof folder: photos of an old schooner, sonar printouts, and a map of the bay with a red circle on it.")
item("lea_chart_page", "Page Forty", "quest",
     text="A page torn from Lea's chart book: her grandfather's pencil marks, a bay, a cross, and a date from 1924. "
          "In the margin, in older pencil: “She sings at the pool when the tide is in.”")

# ------------------------------------------------------------------ Hauptkette
NACH_STRAND = "gr_gang"
NACH_TEICH = "gr_fackel"
ZELLE = [{"wenn": {"flag": "gr_spaet"}, "id": "gr_zelle_spaet"}, {"id": "gr_zelle"}]
BOSS = [{"wenn": {"alle": [{"flag": "gr_matteu_wahrheit"}, {"flag": "gr_spaet"}]}, "id": "gr_boss_matteu_spaet"},
        {"wenn": {"flag": "gr_matteu_wahrheit"}, "id": "gr_boss_matteu"},
        {"wenn": {"flag": "gr_spaet"}, "id": "gr_boss_spaet"},
        {"id": "gr_boss"}]
HEIM = [{"wenn": {"flag": "gr_bastien_zurueckgelassen"}, "id": "gr_rueckweg_bastien"}, {"id": "gr_heim"}]

FRAMES = [
    FR("gr_start", 1, "grotto_steps", "Below Punta d'Orsu",
       "Low tide. Totò rows you round the point in a dinghy that smells of diesel and fish. Under the cliff, where the "
       "sea has pulled back, there are steps cut into the rock, slippery with weed. They lead down into the dark. "
       "Something squeaks in there. A lot of somethings.",
       [Z("toto", "My cousin Gennaro went in on Thursday. He said three hours, in and out. He always says three hours.", "nervousness"),
        Z("toto", "I wait here with the boat. When the water reaches the third step, I have to go. Okay? I'm sorry. "
                  "Bring him out, boss.", "fear")],
       [O("Steps off the dinghy onto the weed. “Third step. Got it.”",
          [EXP, KAMPF("gr_1_ratten"), WEITER("gr_strand")],
          zeile=Z("toto", "And boss? Whatever he did, he's not a bad man. He's just Gennaro.", "sadness")),
        O("“Not today, Totò.”", [],
          zeile=Z("toto", "Okay. Okay. Tomorrow. The tide comes back tomorrow too.", "sadness"))],
       personen=H1("toto"), sets=SETS_("toto")),
    FR("gr_strand", 2, "drowned_beach", "The Drowned Beach",
       "Behind the entrance the grotto opens into a beach the sun has never seen. Grey sand, driftwood, a smell of salt "
       "and old smoke. Someone made a fire here not long ago. Then, from a crack in the rock to the left, a woman's "
       "voice, very far away and very scared.",
       [Z("chloe", "Au secours! Is somebody there? Please! Help!", "fear")],
       [O("Follows the voice into the crack.", [WEITER("gr_u2_start")]),
        O("Gennaro first. Takes the tunnel deeper into the rock.", [F("gr_chloe_ignoriert"), WEITER(NACH_STRAND)])],
       personen=H1("chloe")),
    FR("gr_gang", 3, "smugglers_tunnel", "The Smugglers' Tunnel",
       "A tunnel, too straight to be natural. Old iron rings in the walls where lanterns used to hang, a rail for "
       "carts, rusted to lace. Something long and patient is lying across the rail, enjoying the last of the warmth.",
       [],
       [O("Steps over the rail very slowly.", [KAMPF("gr_3_viper"), WEITER("gr_halle")])]),
    FR("gr_halle", 4, "crate_hall", "The Hall of Crates",
       "A hall full of crates. Cigarettes, whisky, a jet ski still in its plastic. And at the back, on its own, a "
       "heavy grey crate with a stamped code and a small white logo. You know that crate. You saw it in the hangar "
       "in Antibes, the night before all this began. Two men are playing cards on it.",
       [],
       [O("Walks up to the card game. “Deal me in.”", [KAMPF("gr_4_schmuggler"), WEITER("gr_teich")]),
        O("Waits in the dark until one of them goes for a piss.", [WEITER("gr_teich")],
          probe=P("cunning", 13), erfolg=[F("gr_leise")], fehlschlag=[KAMPF("gr_4_schmuggler")])]),
    FR("gr_teich", 5, "underground_pool", "The Black Pool",
       "A pool, black and perfectly still. Then it isn't. A boy surfaces in a torn wetsuit, a net bag full of "
       "packages on his belt. He sees you and nearly goes under again. He can't be more than nineteen. Somewhere under "
       "the rock, very faint, something is humming.",
       [Z("matteu", "You're not one of them. They don't come down here, they're scared of the water.", "surprise"),
        Z("matteu", "I'm Matteu. Pinelli, from the village. I dive for them. They pay. And…", "nervousness"),
        Z("matteu", "My brother Ghjacumu drowned down here last year. They said if I dive for them long enough, they'll "
                    "tell me where. So I can bring him home to our mother.", "sadness")],
       [O("“Show me where you've already looked.”", [V("matteu", 4), WEITER("gr_u1_start")],
          zeile=Z("matteu", "There's a gallery behind the pool. They told me never to go there. That's why I think "
                            "it's there.", "realization")),
        O("“I'm looking for a man called Gennaro. Where do they keep people?”", [WEITER(NACH_TEICH)],
          zeile=Z("matteu", "Past the torches. Be careful. The old man is coming back with the tide. He always does.",
                  "fear"))],
       personen=H1("matteu"), sets=SETS_("matteu")),
    FR("gr_fackel", 6, "torch_gallery", "The Torch Gallery",
       "Torches in iron rings, freshly lit. Somebody is expecting company. A man with a torch in one hand and a "
       "cutlass in the other steps out of a niche and grins with three teeth.",
       [],
       [O("Grins back with all of his.", [KAMPF("gr_6_fackel"), WEITER(ZELLE)])]),
    FR("gr_zelle", 7, "gennaro_cell", "Gennaro",
       "A dry cave above the waterline. A man with a gold tooth and a big moustache is chained to a ring bolt by one "
       "ankle. He has a black eye and a split lip, and when he sees you he starts talking before you've said a word.",
       [Z("gennaro", "Who are you? No. Wait. Totò sent you. Of course he did. Totò sends people. Holy Mother.", "relief"),
        Z("gennaro", "It's not my crate. Okay? I only carry. Three nights, a thousand euros, no questions. Then the old "
                     "man in Bastia says the debt has doubled. Doubled!", "anger"),
        Z("gennaro", "Here. They didn't find this. My grandfather's. He fished out of Bastia for fifty years with it, "
                     "and nobody ever heard him coming. They called it Sussurro. The whisper.", "pride"),
        Z("gennaro", "It whispered me out of worse places than this. Take it. You'll need it more than me, when he comes.",
          "caring")],
       [O("Takes the knife. Weighs it. Cuts the rope that holds the chain. “Let's go home.”",
          [F("waffe_knife"), F("gr_gennaro_gefunden"), V("toto", 4), WEITER(BOSS)],
          zeile=Z("gennaro", "Not yet. Listen. Do you hear the water? That's him. He comes with the tide.", "fear"))],
       personen=H1("gennaro"), sets=SETS_("gennaro"), ton="wholesome"),
    FR("gr_zelle_spaet", 7, "gennaro_cell", "Gennaro, Too Late",
       "A dry cave above the waterline. A man with a gold tooth and a big moustache is chained to a ring bolt by one "
       "ankle. He is sitting very still with his hands in his lap. They are swollen and blue. Someone has taken his "
       "fingers one at a time, and taken his time.",
       [Z("gennaro", "Totò sent you. Of course. You're late, my friend. Only a little. An hour.", "sadness"),
        Z("gennaro", "He asked me for the money, very politely, and every time I said I don't have it, he took a finger. "
                     "Very politely.", "grief"),
        Z("gennaro", "My grandfather's knife. They didn't find it. Sussurro, the whisper. Take it out of my boot. I "
                     "can't close my hand around it anymore.", "sadness")],
       [O("Takes the knife from his boot. Says nothing. Cuts the rope.",
          [F("waffe_knife"), F("gr_gennaro_gefunden"), F("gr_gennaro_haende"), V("toto", 2), WEITER(BOSS)],
          zeile=Z("gennaro", "Don't tell Totò about the hands. Not yet. Listen. That's him. He comes with the tide.",
                  "fear"))],
       personen=H1("gennaro"), sets=SETS_("gennaro")),
]


def _boss(fid, titel, matteu, spaet):
    lage = ("The water comes in over the sand without a sound. With it comes a boat, and in the boat sits an old man "
            "in a linen suit gone yellow at the cuffs, peeling an orange. Two men with torches stand behind him. He "
            "steps out onto the rock as if onto a carpet.")
    zeilen = [Z("riscossore", "Sit down, signore. I'm in no hurry. The tide is always in a hurry. I never am.", "neutral"),
              Z("riscossore", "That man owes me money. And that knife in your hand is his, so it is mine. Shall we talk like "
                              "civilised people?", "amusement")]
    if matteu:
        lage += (" Before he can say another word, Matteu comes out of the pool behind him, Ghjacumu's medal round "
                 "his neck and a diving knife in his fist.")
        zeilen = [Z("matteu", "You locked him in! Eighteen days! He scratched the days into the wall!", "anger"),
                  Z("riscossore", "Ah. The little brother. I told your brother too: the sea keeps what it's given.",
                    "neutral")]
        folge = [F("gr_matteu_tot"), KAMPF("gr_8_riscossore_matteu" + ("_spaet" if spaet else "")), WEITER("gr_wahl")]
        text = "Goes for the old man before the torches reach the boy."
        zeile = Z("matteu", "For Ghjacumu…", "grief")
    else:
        folge = [KAMPF("gr_8_riscossore" + ("_spaet" if spaet else "")), WEITER("gr_wahl")]
        text = "“I'm not here to talk.” Steps between him and Gennaro."
        zeile = Z("riscossore", "Pity. Nobody wants to talk any more. Everybody wants to bleed.", "disappointment")
    return FR(fid, 8, "crate_hall", titel, lage, zeilen, [O(text, folge, zeile=zeile)],
              personen=H1("riscossore", "gennaro") if not matteu else H1("riscossore", "matteu"),
              sets=SETS_("riscossore", "gennaro" if not matteu else "matteu"))


FRAMES += [_boss("gr_boss", "U Riscossore", False, False),
           _boss("gr_boss_spaet", "U Riscossore", False, True),
           _boss("gr_boss_matteu", "U Riscossore", True, False),
           _boss("gr_boss_matteu_spaet", "U Riscossore", True, True)]

FRAMES += [
    FR("gr_wahl", 9, "crate_hall", "The Crate",
       "The old man sits against a crate with his hands in his lap, breathing through his nose. His men are gone. "
       "The water is at your ankles. Gennaro limps to the grey crate and puts his hand on it like on an animal.",
       [Z("riscossore", "Take the crate to my boat, and Gennaro's debt is paid. All of it. My word. I am many things, "
                        "but I keep my word.", "neutral"),
        Z("gennaro", "Forty collars, a box of chips. The same ones they put on the dogs in the harbour. On the goat.",
          "fear"),
        Z("gennaro", "If you take it, you can show the world what Alon Varenne does. And I… I go on owing the old man. Forever. "
                     "You decide. I already decided enough stupid things this year.", "sadness")],
       [O("Pushes the crate into the old man's boat. “His debt is paid. Then we're done.”",
          [F("gr_kiste_abgegeben"), F("gr_gennaro_frei"), V("toto", STUFE), V("gennaro", 8), WEITER("gr_kiste_weg")],
          zeile=Z("riscossore", "Done. You are an honest man, signore. That is rarer than you think, and more "
                                "expensive.", "approval")),
        O("Puts his hand on the crate. “This goes with me. It's proof.”",
          [F("gr_kiste_genommen"), DATIERT("gr_gennaro_gejagt"), I("collar_crate"), V("toto", -4),
           WEITER("gr_kiste_beweis")],
          zeile=Z("riscossore", "Proof. How nice. Proof keeps nobody warm, signore. Ask Gennaro in a week.",
                  "neutral"))],
       personen=H1("gennaro", "riscossore"), sets=SETS_("gennaro", "riscossore")),
    FR("gr_kiste_weg", 9, "crate_hall", "Paid in Full",
       "The old man's boat slides out with the tide, the crate in the bow like a coffin. Gennaro watches it go. Then "
       "he sits down in the water and laughs until he cries, or the other way round.",
       [Z("gennaro", "Free. I'm free. Giulia. I can go home to Giulia.", "relief"),
        Z("gennaro", "Forty collars, though. Forty dogs. Forty goats. Somewhere. I'll think about that tomorrow. Today I "
                     "just want to breathe.", "remorse")],
       [O("Helps him up. “Come on. Totò's waiting at the third step.”", [WEITER(HEIM)])],
       personen=H1("gennaro"), sets=SETS_("gennaro")),
    FR("gr_kiste_beweis", 9, "crate_hall", "Proof",
       "The old man's boat slides out with the tide, empty. He doesn't look back. He doesn't need to. Gennaro stares "
       "at the crate between your feet as if it were a bomb.",
       [Z("gennaro", "You did the right thing. You did. For the dogs, for the goats, for everybody.", "fear"),
        Z("gennaro", "Only… the old man doesn't forget. He'll come to Bastia. Giulia's school is in Bastia.",
          "grief")],
       [O("Lifts the crate. It's heavier than it looks. “We'll keep you safe.”", [WEITER(HEIM)],
          zeile=Z("gennaro", "You'll keep me safe. Sure. Like you kept the boat safe.", "sadness"))],
       personen=H1("gennaro"), sets=SETS_("gennaro")),
    FR("gr_heim", 10, "grotto_steps", "The Third Step",
       "The water is lapping at the third step. Totò is standing up in the dinghy, waving both arms. When he sees "
       "Gennaro, he stops waving and just stands there.",
       [Z("toto", "Gennà. You stupid, stupid… Come here.", "relief"),
        Z("toto", "Boss. I don't know what to say. Me, Totò, I don't know what to say. Thank you.", "gratitude")],
       [O("Climbs into the dinghy. Lets the two of them hug it out.", [F("grotte_fertig"), EXP_ENDE])],
       personen=H1("toto", "gennaro"), sets=SETS_("toto", "gennaro"), ton="wholesome"),
    FR("gr_rueckweg_bastien", 10, "collapsed_passage", "The Way Back",
       "On the way back you pass the crack in the rock. You said you'd come back. You came back. The passage is full "
       "of black water now, up to the roof. Bastien was under those stones. Chloé is sitting on a rock above the waterline, quite still, a velvet box "
       "in her hands.",
       [Z("chloe", "He was talking until the end. About Marseille. About a restaurant by the old port.", "grief"),
        Z("chloe", "Here. He was going to give it to me when we found the strongbox. Give it to someone who gets the "
                   "chance.", "sadness")],
       [O("Takes the box. Stays with her a moment. Then takes her with him to the boat.",
          [I("bastien_ring"), F("gr_bastien_tot"), WEITER("gr_heim")],
          zeile=Z("chloe", "Don't. Don't say sorry. You chose your friend. I would have chosen mine.", "sadness"))],
       personen=H1("chloe"), sets=SETS_("chloe")),
]

# ------------------------------------------------------------------ Umweg 1 "The Second Brother" (Matteu)
U1 = [
    FR("gr_u1_start", 5, "flooded_gallery", "The Forbidden Gallery",
       "Behind the pool a gallery runs down into the rock, half flooded. Matteu swims ahead with a dive lamp. On a "
       "ledge above the water something thick and dark uncoils, slowly, the way only things that have never been "
       "afraid uncoil.",
       [Z("matteu", "There. On the ledge. Don't let it get between us and the air.", "fear")],
       [O("Puts himself between the boy and the ledge.", [KAMPF("gr_u1_viper"), WEITER("gr_u1_luft")])],
       personen=H1("matteu"), sets=SETS_("matteu")),
    FR("gr_u1_luft", 6, "air_pocket", "The Air Pocket",
       "A dome of rock with air in it, and a shelf just above the high-water mark. Matteu pulls himself up next to "
       "you, shivering. Then he holds the lamp to the wall and stops shivering.",
       [Z("matteu", "Lines. Somebody counted. That's… that's how Ghjacumu counted. Fives, with a line through. He did "
                    "it on the wall of our room, for the days until the summer.", "realization"),
        Z("matteu", "He was here. He was alive here.", "realization")],
       [O("Puts a hand on his shoulder. “Let's see where this goes.”", [WEITER("gr_u1_gitter")])],
       personen=H1("matteu"), sets=SETS_("matteu")),
    FR("gr_u1_gitter", 7, "air_pocket", "The Grate",
       "At the end of the air pocket a narrow passage leads back towards the smugglers' tunnel. It is closed by an "
       "iron grate, and the grate is padlocked. From your side there is no keyhole. The lock is on the other side, "
       "where the smugglers walk. Rats come out of the dark when the lamp swings round.",
       [],
       [O("Kicks the rats back into the dark.", [KAMPF("gr_u1_ratten"), WEITER("gr_u1_wahl")])]),
    FR("gr_u1_wahl", 7, "air_pocket", "What Matteu Can't See",
       "Matteu is still at the tally marks with the lamp. He hasn't seen the grate. You have. Behind the bars, on the "
       "other side, is a little green string with a tin medal on it, chewed through. Somebody pushed his hand through "
       "these bars for a long time. Somebody else locked them, and came back with the tide, and didn't open them.",
       [Z("matteu", "What's there? What do you see? Is it him?", "fear")],
       [O("Tells him the truth. “Someone locked him in, Matteu. From the outside.”",
          [F("gr_matteu_wahrheit"), I("ghjacumu_medal"), WEITER(NACH_TEICH)],
          zeile=Z("matteu", "…The old man. He always comes with the tide. He comes with the tide.", "anger")),
        O("Lies. “Just rats. He drowned, Matteu. It was quick. He didn't suffer.”",
          [F("gr_matteu_belogen"), DATIERT("gr_matteu_belogen_tag"), V("matteu", 8), WEITER(NACH_TEICH)],
          zeile=Z("matteu", "Quick. Okay. Okay. Thank you. That's… I can tell my mother that.", "relief"))],
       personen=H1("matteu"), sets=SETS_("matteu")),
]

# ------------------------------------------------------------------ Umweg 2 "The Price of the Tide" (Chloé, Bastien)
U2 = [
    FR("gr_u2_start", 2, "collapsed_passage", "A Voice in the Rock",
       "The crack opens into a passage where the roof has come down. Under the rubble a man is lying on his back, "
       "pale and grinning with pain, one leg buried to the hip. A woman is kneeling next to him, pulling at the "
       "stones with bleeding fingers. Behind her, two men are going through a rucksack. They look up.",
       [Z("chloe", "Thank God! These two came with the tide, they took our lamps, our water…", "fear")],
       [O("“Put the bag down, gentlemen.”", [KAMPF("gr_u2_pirat"), WEITER("gr_u2_lager")])],
       personen=H1("chloe"), sets=SETS_("chloe")),
    FR("gr_u2_lager", 3, "treasure_camp", "The Treasure Hunters' Camp",
       "Their camp is a ledge with two sleeping bags, a winch, a laptop wrapped in cling film and a wall of photos: "
       "an old schooner, a strongbox, a map of the bay with a red circle. On the laptop there's a sticker: a small "
       "white logo you have seen before.",
       [Z("chloe", "Chloé. Chloé Marchal. That's Bastien under the rocks. We're looking for a strongbox, from a "
                   "schooner that went down in 1924.", "nervousness"),
        Z("chloe", "Yes, A.V. Estates pays for the expedition. Yes, we report every find to them. Everybody needs "
                   "money, okay? Treasure hunting doesn't feed anyone.", "embarrassment"),
        Z("chloe", "The winch. With the winch we can lift the stone. But the tide… in twenty minutes the passage is "
                   "under water.", "fear")],
       [O("Shoulders the winch. “Show me.”", [WEITER("gr_u2_wahl")])],
       personen=H1("chloe"), sets=SETS_("chloe")),
    FR("gr_u2_wahl", 3, "collapsed_passage", "Twenty Minutes",
       "Back at the rubble the water is already round Bastien's shoulders. Freeing him will take every minute the "
       "tide has left. Somewhere deeper in the rock Totò's cousin is waiting, and so is a man who comes with the "
       "tide.",
       [Z("chloe", "Please. I'll give you everything. Our notes, the map, the circle on the map. Everything.", "fear"),
        Z("chloe", "Please don't leave him here.", "grief")],
       [O("Sets the winch against the stone and starts cranking.",
          [F("gr_bastien_befreit"), F("gr_spaet"), V("chloe", 8), F("gr_chloe_notizen"), I("treasure_notes"),
           WEITER("gr_u2_frei")],
          zeile=Z("chloe", "Thank you. Thank you, thank you…", "relief")),
        O("“I'll come back for him. I promise.” Goes for Gennaro.",
          [F("gr_bastien_zurueckgelassen"), WEITER(NACH_STRAND)],
          zeile=Z("chloe", "You'll come back. Yes. Of course. Go. GO!", "fear"))],
       personen=H1("chloe"), sets=SETS_("chloe")),
    FR("gr_u2_frei", 3, "collapsed_passage", "Lifted",
       "The stone comes up a finger's width, then a hand. Bastien screams, and then he is out, and Chloé is holding "
       "his head above the water. His leg is bent in the wrong place. He's laughing anyway. It's taken almost an hour. "
       "The tide hasn't waited for anybody.",
       [Z("chloe", "Here. Our notes. The circle on the map. Take them, give them to whoever you want. Just not to "
                   "A.V. Estates. Never again.", "gratitude")],
       [O("Takes the notes, and goes deeper, fast.", [WEITER(NACH_STRAND)])],
       personen=H1("chloe"), sets=SETS_("chloe")),
]

# ------------------------------------------------------------------ Wiederkommen
WIEDER = [
    FR("gr_wieder", 1, "grotto_steps", "The Grotto, Again",
       "Low tide again. Totò doesn't come with you this time. The steps are as slippery as before, and the rats have "
       "forgotten you already.",
       [],
       [O("Goes down to the hall of crates and hunts for leftovers.", [EXP, KAMPF("gr_4_schmuggler"),
                                                                       WEITER("gr_wieder_ende")]),
        O("Sits on the drowned beach for a while.", [EXP, WEITER("gr_wieder_ende")])],
       ton="wholesome"),
    FR("gr_wieder_ende", 2, "drowned_beach", "The Drowned Beach",
       "The fire pit is cold. The sea breathes in and out at the mouth of the grotto.",
       [],
       [O("Goes back up before the third step.", [EXP_ENDE])], ton="wholesome"),
]

# ------------------------------------------------------------------ Kevins Daecher (Tag 12-14)
KEVIN = [
    FR("kv_start", 1, "village_rooftops", "Mine!",
       "The village from above: terracotta roofs, washing lines, TV aerials. On the highest roof, by the bell tower, "
       "a big white gull is standing on one leg with a page of paper in its beak, looking at you the way a cat looks "
       "at a dog behind a fence.",
       [Z("lea", "That's him. That's Kevin. That's Grandad's page. That's forty years of Grandad.", "anger"),
        Z("lea", "I'll take the left. You take the… oh, there are pigeons. Of course there are pigeons.", "annoyance")],
       [O("Climbs out of Alva's attic window onto the roof.", [KAMPF("kv_tauben"), WEITER("kv_glocke")])],
       personen=H1("lea"), sets=SETS_("lea"), ton="witzig", tage=(12, 14)),
    FR("kv_glocke", 2, "bell_tower_nest", "The Bell Tower",
       "Up the drainpipe, over the gutter, onto the bell tower. Kevin is waiting at the top on a nest made of "
       "fishing line, chip papers and, apparently, everything this crew has lost in two weeks. He drops the page into "
       "the nest, spreads his wings and screams.",
       [Z("lea", "Don't hurt him! Just… hurt him a little.", "excitement")],
       [O("Spreads his arms too and screams back.", [KAMPF("kv_kevin"), WEITER("kv_nest")])],
       personen=H1("lea"), sets=SETS_("lea"), ton="witzig", tage=(12, 14)),
    FR("kv_nest", 3, "bell_tower_nest", "Kevin's Treasure",
       "Kevin sulks on the weathervane. The nest is a museum: Totò's lighter, Megan's fountain pen, Holm's spare "
       "sunglasses, a fork from the galley, a sock nobody will ever claim. And, a little wet, page forty.",
       [Z("lea", "Grandad's handwriting. The bay, the cross. 1924. It's all still there.", "relief"),
        Z("lea", "You climbed a bell tower for me. Nobody's ever climbed anything for me. Ever.", "love")],
       [O("Gives her the page, and keeps Megan's pen for himself.", [I("lea_chart_page"), F("kevin_seite"),
                                                                    F("kevin_fertig"), F("kevin_stift"), V("lea", STUFE),
                                                                    GAG("kevin"), WEITER("kv_ende")],
          zeile=Z("lea", "You're keeping Megan's pen. I didn't see that. I saw nothing.", "amusement")),
        O("Gives her the page, and puts everything else back. “He collected it fair and square.”",
          [I("lea_chart_page"), F("kevin_seite"), F("kevin_fertig"), F("kevin_fair"), V("lea", STUFE), GAG("kevin"),
           WEITER("kv_ende")],
          zeile=Z("lea", "You're the only person on this island who respects that gull. That's weird. I like it.",
                  "amusement"))],
       personen=H1("lea"), sets=SETS_("lea"), ton="wholesome", tage=(12, 14)),
    FR("kv_ende", 4, "village_rooftops", "Down Again",
       "Getting down is harder than getting up. It always is. Kevin watches you go with one eye, already planning "
       "the next theft.",
       [],
       [O("Climbs back in through Alva's window.", [WEITER("kv_don")])], ton="witzig", tage=(12, 14)),
]

# ------------------------------------------------------------------ Flut-Nacht (Duc 28.10.2026): die Sirene
# Ort "grotte_flut" (Abend, nach grotte_fertig). Vier Kaempfe (Ratten, Fledermaeuse - mit 10 % die Vampirin -, Schwarze
# Viper, Piraten), dann die Sirene, die man nur durch Reden besiegt (untouchable). Sie kennt das Wrack und gibt den
# Saphir fuer Riposte (Stufe 2) - der Stein wartet auf seine Klinge aus dem Tauchgang (Woche 3, Flag sirene_weg).
# Danach bleibt die Flut-Nacht ein Sammel-Lauf: dieselben vier Kaempfe, am Teich nur noch Stille.
EXP_F = {"expedition": "grotte_flut"}
TEICH = [{"wenn": {"flag": "sirene_fertig"}, "id": "fn_teich_leer"}, {"id": "fn_teich"}]
RAST.add("fn_teich_leer")
FLUT = [
    FR("fn_start", 1, "grotto_steps", "High Tide",
       "Night, and the tide is in. Totò wouldn't bring you, so you rowed yourself and tied the dinghy to an iron ring "
       "in the cliff. The water stands well over the third step now. Everything that lives down here has climbed up "
       "to where you are.",
       [],
       [O("Climbs out onto the wet rock.", [EXP_F, KAMPF("fn_1_ratten"), WEITER("fn_gang")]),
        O("Unties the dinghy again. Not tonight.", [])], tage=(11, 21)),
    FR("fn_gang", 2, "smugglers_tunnel", "The Tunnel at Night",
       "The rail is under water. You wade along it up to your knees, torch in your teeth. Then you notice the ceiling. "
       "It isn't rock. It's moving, very slightly, and all of it at once.",
       [],
       [O("Keeps very still, and keeps walking.", [KAMPF("fn_2_fledermaeuse"), WEITER("fn_galerie")])],
       tage=(11, 21)),
    FR("fn_galerie", 3, "flooded_gallery", "Swimming",
       "The gallery behind the black pool is a canal now. You have to swim the last stretch, holding the torch high. Something "
       "long brushes past your leg, turns, and comes back to have another look.",
       [],
       [O("Swims faster.", [KAMPF("fn_3_viper"), WEITER("fn_halle")])], tage=(11, 21)),
    FR("fn_halle", 4, "crate_hall", "The Night Shift",
       "The high tide floats a boat right into the hall. Men with head torches are unloading new grey crates, each "
       "with the same small white logo. So that's what high tide is for. One of them turns around.",
       [],
       [O("Steps into the light before he can shout.", [KAMPF("fn_4_piraten"), WEITER(TEICH)]),
        O("Gets a look into an open crate first.", [WEITER(TEICH)], probe=P("perception", 13),
          erfolg=[F("fn_kisten_gesehen"), KAMPF("fn_4_piraten")], fehlschlag=[KAMPF("fn_4_piraten")])],
       tage=(11, 21)),
    FR("fn_teich", 5, "underground_pool_tide", "The Singing",
       "Moonlight falls through a crack in the roof and lies on the black pool like a coin. The humming you heard at low tide the first "
       "time is louder now. It has words in it. Then a woman draws herself up onto the rock at the water's edge, wet "
       "honey-blonde hair clinging to her like weed, a long fish tail sliding out of the pool behind her. She looks at you "
       "as if she has been waiting.",
       [Z("sirene", "Well now. A man who comes down at high tide, on purpose. Either very brave, or very lost.",
          "curiosity"),
        Z("sirene", "Most of them run when they hear me. The rest of them stay. Forever, mind. Which are you, sailor?",
          "amusement")],
       [O("Puts the weapon away. “Neither. I came to talk.”", [F("fn_geredet"), KAMPF("fn_5_sirene"), WEITER("fn_perle")],
          zeile=Z("sirene", "Talk? Go on, then. Make it good. I've heard every word the sea ever drowned.",
                  "curiosity")),
        O("Backs away, very slowly.", [F("fn_gegangen"), WEITER("fn_heim")],
          zeile=Z("sirene", "Another night, then. I'm not going anywhere. I never do.", "sadness"))],
       personen=H1("sirene"), sets=SETS_("sirene"), tage=(11, 21)),
    FR("fn_perle", 6, "underground_pool_tide", "What the Sea Keeps",
       "She rests her arms on the edge of the pool like a girl on a windowsill. When she speaks again, the song has "
       "gone out of her voice, and she just sounds old.",
       [Z("sirene", "There's a boat at the bottom of the bay. An old sailing ship. She went down in a storm a hundred years ago, "
                    "and I sang her crew to sleep. That's what I do.", "sadness"),
        Z("sirene", "But she's not resting. Men come with lamps and machines now. They want something she's carrying. "
                    "And there's a blade down there that was never meant for them.", "anger"),
        Z("sirene", "Here. This fell off her when she sank. It's been waiting for its blade ever since. You'll find "
                    "it. And when you dive, I'll be close. Don't go the way the lamps go.", "caring")],
       [O("Takes the stone. It is warm, which makes no sense at all.", [I("saphir"), F("sirene_fertig"),
                                                                         F("sirene_weg"), {"flag_datiert": "ligeia_freund"}, WEITER("fn_heim")],
          zeile=Z("sirene", "Go on, sailor. The tide doesn't wait for anybody. Not even for me.", "amusement"))],
       personen=H1("sirene"), sets=SETS_("sirene"), tage=(11, 21)),
    FR("fn_teich_leer", 5, "underground_pool_tide", "The Quiet Pool",
       "The pool is black and still. No one rises out of it. Only once, very far away, under the rock, someone hums "
       "two notes, as if to say: I know you're there.",
       [],
       [O("Sits a while. Then goes back.", [WEITER("fn_heim")])], tage=(11, 21)),
    FR("fn_heim", 7, "grotto_steps", "Moonlight",
       "The dinghy is still there, knocking against the rock. The moon is out over the point. Behind you the grotto "
       "breathes in and out with the sea.",
       [],
       [O("Rows home.", [EXP_ENDE])], ton="wholesome", tage=(11, 21)),
]

FRAMES += U1 + U2 + WIEDER + KEVIN + FLUT

# ------------------------------------------------------------------ Spaeter: Anrufe, die wehtun
H = lambda anrufer, ort: {"anrufer": anrufer, "anrufer_ort": ort, "art": "video"}
NACHHER = [
    E("hy_gennaro_weg", "handy", "ernst", "Totò", WANN((13, 21), ["tag", "nachmittag", "abend"],
                                                      bed={"flag_seit": ["gr_gennaro_gejagt", 2]}),
      ORT_DUC, H("toto", "village_harbour"),
      "Totò calls from the harbour. You can hear gulls and his breathing. He doesn't say hello.",
      [Z("toto", "The coast guard found Gennaro's boat this morning. Off Cap Corse. Empty. The engine was still warm.",
         "grief"),
       Z("toto", "Giulia's mother called me. She asks where her husband is. What do I tell her, boss? That there's a "
                 "crate in the tender garage, and it's proof?", "anger")],
      [O("“I'm sorry, Totò. I'm so sorry.”", [F("gennaro_verschwunden")],
         zeile=Z("toto", "Yeah. Me too. I'll be at work tomorrow. Don't talk to me for a few days.", "sadness")),
       O("“We'll make it count. I promise you, that crate will bring Alon down.”", [F("gennaro_verschwunden"),
                                                                                    VER("toto", "Make the crate count against Alon", 14, {"flag": "alon_kiste_genutzt"})],
         zeile=Z("toto", "Make it count. Okay. Do that. Then at least it was worth something.", "sadness"))],
      sets=SETS_("toto")),
    E("hy_matteu", "handy", "ernst", "Alva", WANN((13, 21), ["abend", "nacht"],
                                                  bed={"flag_seit": ["gr_matteu_belogen_tag", 2]}),
      ORT_DUC, H("alva", "alvas_bar"),
      "Alva calls from behind the bar. Music, laughter, glasses. She has to shout a little.",
      [Z("alva", "Your little diver from the grotto is here. Matteu Pinelli. New watch, new wetsuit, buying everyone a round.", "curiosity"),
       Z("alva", "He says the men from Bastia are like family now. That the old man came to his mother's house with "
                 "flowers for the dead brother. Isn't that sweet? Why do I want to throw up?", "disgust")],
      [O("Says nothing. Hangs up after a while.", [F("matteu_bei_ihnen")]),
       O("“Tell him to go home, Alva. Please.”", [F("matteu_bei_ihnen")],
         zeile=Z("alva", "I did. He laughed. He said he's never been happier.", "sadness"))],
      sets={"alva": "alva_standard"}),
]

EVENTS = FRAMES + NACHHER
