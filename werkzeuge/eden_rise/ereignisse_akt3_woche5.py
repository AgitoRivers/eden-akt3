# -*- coding: utf-8 -*-
"""Akt 3, Woche 5 "Name Your Price" (Tag 29-34, Paket D). Drehbuch: docs/wiki/welt/drehbuch_akt3.md, 5.12-5.24, F-10.

Pflicht: Idee von Bibi oder Lea (29 Fruehstueck), Maxwells Flug (30 Fruehstueck), Monaco (31 Dinner), Switched Off
(32 Nachmittag), Maxwell zurueck (32 Dinner), Schiene oder Alons Angebot (33 Fruehstueck), Einladung (33 Tag),
Nach Mitternacht (33 Abend), Villa: Plan (34 Fruehstueck), Keller (34 Tag), Dinner (34 Dinner), Ende (34 Abend), Pascal (34 Nacht).
Karten: The Man with the Orange (a3_orange), Lot 14 (a3_lot14), The Scrap Field (a3_scrap). Pool: Ligeias Flaschenpost.
Die Saeulen (Zeugen, Beweise) zaehlt die Bedingung {"anzahl": [...]} (kern/regeln.py); Paket F liest dieselben Listen."""
from ereignisse_basis import *  # noqa: F401,F403
from ereignisse_gag1 import P1  # noqa: E402
from ereignisse_ligeia import G  # noqa: E402
from ereignisse_akt3_woche4 import FR, FL, NICHT, DA, AKT3, JE, PFL, FRAME, DIREKT, tags_fuer  # noqa: E402

WEITER = lambda ziel: {"weiter": ziel}
KAMPF = lambda bid: {"kampf": bid}

# ------------------------------------------------------------------ Listen fuer Saeulen (auch Paket F)
ZEUGEN = ["petru", "mina", "batu", "alva", "anghjulu", "casanova", "sandru", "bonaventure"]
ZEUGE = lambda p: FL("a3_zeuge_" + p)
BEWEISE = ["alon_kiste_genutzt", "a3_siri_post", "sophia_notizen", "bl_funk_white", "bl_funk_charly", "bl_wache_gesehen",
           "rt_ausgang_alle", "mo_ark_beweis", "a3_beweis_feuer"]
ZEUGEN_N = lambda op, n: {"anzahl": [[ZEUGE(p) for p in ZEUGEN], op, n]}
BEWEISE_N = lambda op, n: {"anzahl": [[FL(b) for b in BEWEISE], op, n]}
MEGAN_WENDE = {"eine": [ZEUGEN_N(">=", 4), BEWEISE_N(">=", 2), {"wert": ["vertrauen.yamamoto", ">=", 5]}]}
# Das geheime Ende ★ (enden.md, F-36): alle Saeulen bis auf Staerke (die ersetzt das Dorf vor der Villa), Yamamoto Bindung 5,
# und Ende 1 in einem frueheren Durchlauf gesehen (kern/meta.py setzt meta_ende_1).
STERN = {"alle": [FL("meta_ende_1"), {"wert": ["vertrauen.yamamoto", ">=", 5]}, BEWEISE_N(">=", 3), ZEUGEN_N(">=", 5)]}
GEKUEMMERT = {"eine": [FL("sandru_surren"), FL("sandru_herkunft"), {"wert": ["vertrauen.sandru", ">=", 3]}]}
BIBI = {"alle": [FL("rt_bibi_bleibt"), FL("mo_eco_idee")]}

# ------------------------------------------------------------------ 5.12 Die Idee (Tag 29, Fruehstueck)
IDEE = [
    E("a3_bibi_idee", "gag1", "witzig", "Forty Men and a Boat", PFL(29, "fruehstueck", BIBI), "mochis",
      P1("bibi", ("bonaventure", "?", "doesn't understand yet")),
      "Bibi sits at the gate of her animal station with her field book. On one page there are forty little lines. Buenaventura has come up to see her, hat in hand.",
      [G("bibi", "[laugh] So he's got forty men, a boat and nothing to do? And they know every rock in that bay? "
                 "Doudou. Doudou, come here. I need you to do some numbers.", "excitement"),
       G("bibi", "[chuckle] People pay me to watch a capybara sleep. They'll pay double to see a pirate who's sorry.", "amusement"),
       G("bonaventure", "[clear throat] Tourists? On my ship? Why would a pirate do that, Señorita?", "confusion")],
      [O("“Because a pirate with tourists can pay his debts.”", [F("a3_eco_idee"), DIREKT("a3_idee_hut")]),
       O("“Because you'd be the head of something.”", [F("a3_eco_idee"), DIREKT("a3_idee_hut")]),
       O("“Ask Bibi. It's her idea.”", [F("a3_eco_idee"), V("bibi", 4), DIREKT("a3_idee_hut")])]),
    E("a3_lea_idee", "gag1", "witzig", "Every Rock", PFL(29, "fruehstueck", {"alle": [NICHT(BIBI), DA("lea")]}), "village_harbour",
      P1("lea", ("bonaventure", "?", "doesn't understand yet")),
      "Lea sits at the harbour with her grandfather's chart and draws in the rocks with a pencil. Buenaventura looks over her shoulder.",
      [G("lea", "[gasp] Did you know a protected bay needs people who know every rock? Proper people, with boats. And they've got forty!", "excitement"),
       JE(G("lea", "[sigh] The wreck is gone, but the bay isn't. Somebody has to show people what's still here.", "sadness"), "wrack", FL("a3_tauchgang_gescheitert")),
       G("bonaventure", "[clear throat] Tourists? On my ship? Why would a pirate do that?", "confusion")],
      [O("“Because a pirate with tourists can pay his debts.”", [F("a3_eco_idee"), DIREKT("a3_idee_hut")]),
       O("“Because you'd be the head of something.”", [F("a3_eco_idee"), DIREKT("a3_idee_hut")]),
       O("“Ask Lea. It's her idea.”", [F("a3_eco_idee"), V("lea", 4), DIREKT("a3_idee_hut")])],
      sets={"lea": "Deck"}),
    E("a3_idee_hut", "gag1", "witzig", "The Head of Something", FRAME(), "village_harbour", P1("bonaventure"),
      "Buenaventura takes off his hat and looks at it for a long time.",
      [G("bonaventure", "[clear throat] The head of... [sigh] ...I would need a hat.", "pride"),
       JE(G("bibi", "[laugh] I'll make you one. Out of an old feeding bucket. Don't ask.", "amusement"), "hut", BIBI),
       JE(G("lea", "[chuckle] Did you know some sea captains wore two? Probably.", "amusement"), "hut", None),
       G("bonaventure", "[sigh] But the grotto belongs to the old man with the oranges. And I owe him everything already.", "nervousness")],
      [O("“Then we go and ask him. Together.”", [F("a3_idee_fertig")]),
       O("“Leave the old man to me.”", [F("a3_idee_fertig")])]),
]

# ------------------------------------------------------------------ 5.13 The Man with the Orange (Karte, Riscossore)
ORANGE = [
    FR("a3_orange", "underground_pool_tide", "The Man with the Orange",
       "The grotto at low tide. An old man in a linen suit, yellow at the cuffs, sits by the water and peels an orange. "
       "Everybody on this coast owes him money. Buenaventura stands behind you with his hat in his hands.",
       [JE(G("riscossore", "[chuckle] Last time you came with a knife. Today you came with a captain. Better.", "amusement"),
           "gruss", {"eine": [FL("gr_kiste_genommen"), FL("gr_kiste_abgegeben")]}),
        G("bonaventure", "[clear throat] I want to show tourists your grotto. I pay you from every ticket.", "nervousness"),
        G("riscossore", "[chuckle] Eventually.", "amusement"),
        G("bonaventure", "[sigh] ...Eventually.", "embarrassment"),
        G("riscossore", "[clear throat] A man in prison pays nobody. A man with tourists pays me every day, a little. I prefer every day. "
                        "But you want something too, I think. The commission. Why should I come and open my book for you?", "neutral")],
       [O("“Because Alon paid Buenaventura through you. It's in your book.”", [F("a3_riscossore_kommt"), WEITER("a3_orange_insel")],
          zeile=G("riscossore", "[chuckle] Clever. Not kind. Clever.", "neutral")),
        O("“Because nobody pays you if Alon gets the bay.”", [F("a3_riscossore_kommt"), WEITER("a3_orange_insel")],
          zeile=G("riscossore", "[sigh] Yes. That is the reason. Not kindness.", "neutral")),
        O("Says nothing and looks at the empty water where Gennaro's boat used to come in.", [F("a3_riscossore_kommt"), WEITER("a3_orange_insel")],
          zeile=G("riscossore", "[sigh] Totò's cousin. ...He should hate me. Fine. I'll come.", "remorse"))],
       personen={"handelnd": "riscossore", "betroffen": [{"id": "bonaventure", "ton": "?", "was": ""}]}, sets={"riscossore": "riscossore_standard"}, ton="ernst"),
    FR("a3_orange_insel", "underground_pool_tide", "An Island, Twice a Day",
       "The tide goes out. A flat rock comes up out of the water. Buenaventura climbs onto it and plants his purple flag.",
       [G("bonaventure", "[laugh] It is an island. Twice a day.", "joy"),
        G("riscossore", "[chuckle] Here. Your first payment.", "amusement")],
       [O("Watches the old man hand the pirate a piece of orange.", [F("a3_orange_fertig")]),
        O("Takes a piece of orange too.", [F("a3_orange_fertig")])],
       personen={"handelnd": "bonaventure", "betroffen": [{"id": "riscossore", "ton": "+", "was": ""}]}, sets={"riscossore": "riscossore_standard"}),
]

# ------------------------------------------------------------------ 5.14 Gogo's Medicine (Tag 30) und Maxwells Rueckkehr (Tag 32)
MAXWELL = [
    E("a3_maxwell_flug", "gag1", "wholesome", "Gogo's Medicine", PFL(30, "fruehstueck"), "village_harbour",
      P1("maxwell", ("jana", "+", "holds his hand")),
      "Maxwell stands on the quay with a cool box in his arms, like a baby. A taxi to the airport in Bastia is waiting.",
      [G("maxwell", "[clear throat] Number One. Mr. Maximum is going to fly. In an aeroplane. Gogo needs this medicine in Durban, and the post is too slow.", "fear"),
       JE(G("maxwell", "[sniff] I kept the bandage from the siege, brother. For luck.", "caring"), "verband", FL("bl_verband_maxwell")),
       JE(G("maxwell", "[chuckle] Bibi says a plane has no bad temper. Mr. Maximum fed Bones. Mr. Maximum can sit in a plane.", "pride"), "bones", FL("a3_paar_bones")),
       G("maxwell", "[sigh] Number One. What does a big man do when he's scared of the sky?", "nervousness")],
      [O("“He takes the window seat and looks anyway.”", [F("a3_maxwell_weg"), V("maxwell", 4)],
         zeile=G("maxwell", "[gasp] The window! Eish. ...Okay. Okay.", "nervousness")),
       O("Puts a hand on the cool box. “He carries it. Like he always does.”", [F("a3_maxwell_weg"), V("maxwell", 6)],
         zeile=G("maxwell", "[sniff] Like always. Thank you, brother.", "gratitude")),
       O("“He holds Jana's hand. She's coming to the airport.”", [F("a3_maxwell_weg"), V("jana", 4)],
         zeile=G("jana", "[laugh] Coach, I'll hold your hand the whole way to Bastia. And I'm not sorry.", "joy"))],
      sets={"maxwell": "maximum_steward_a", "jana": "jana_deck_a"}),
    E("a3_maxwell_zurueck", "gag1", "witzig", "Mr. Maximum Has Flown", PFL(33, "fruehstueck", FL("a3_maxwell_weg")), "village_piazza",
      P1("maxwell", ("jana", "+", "runs to him")),
      "Early morning. A taxi stops on the square. Maxwell gets out with an empty cool box and a face like a man who has seen the clouds from above.",
      [G("maxwell", "[sigh] Mr. Maximum has flown. We will never speak of it.", "pride"),
       G("maxwell", "[chuckle] Gogo says thank you. And she says you are too thin.", "joy")],
      [O("“Welcome back, Maxwell.”", [F("a3_maxwell_da"), V("maxwell", 2)]),
       O("Hugs him, cool box and all.", [F("a3_maxwell_da"), V("maxwell", 4)],
         zeile=G("maxwell", "[laugh] Eish! Careful, brother. Mr. Maximum is still a bit airsick.", "amusement"))],
      sets={"maxwell": "maximum_steward_a"}),
]

# ------------------------------------------------------------------ 5.15 Lot 14 (Karte, Rosi und Yamamoto)
LOT14 = [
    FR("a3_lot14", "generator_room", "Lot 14",
       "Yamamoto has a printout from her bank. She holds it out to Rosi with both hands, like a gift she is ashamed of.",
       [G("yamamoto", "[clear throat] So sorry, Rosi-san. I read A.V.'s property lists for my bank. There is a street in Catania. Lot 14. A workshop, closed three years ago.", "nervousness"),
        G("rosi", "[sniff] ...The press in that workshop was older than Papa. It had a crack in the left side. He called it Old Lady.", "grief"),
        G("rosi", "[clear throat] Officer. If he goes down, can I buy it back? Tell me the truth.", "neutral")],
       [O("“If he goes down, yes. So let's make him go down.”", [F("a3_lot14"), V("rosi", 6)],
          zeile=G("rosi", "[sigh] Okay. Then that's the plan. My plan.", "pride")),
        O("“I don't know. But I'll help you try.”", [F("a3_lot14"), V("rosi", 4)],
          zeile=G("rosi", "[sniff] Honest. Annoying. Thank you.", "gratitude")),
        O("Sits down on the toolbox next to her and waits.", [F("a3_lot14"), V("rosi", 4), V("yamamoto", 2)],
          zeile=G("yamamoto", "[sigh] I will wait too. So sorry. I am bad at waiting.", "caring"))],
       personen={"handelnd": "yamamoto", "betroffen": [{"id": "rosi", "ton": "?", "was": ""}]}, sets={"rosi": "Engine Room"}, ton="ernst"),
]

# ------------------------------------------------------------------ The Scrap Field (Karte, F-10: Stahl fuer The Lights)
SCRAP = [
    FR("a3_scrap_1", "antenna_ridge", "The Scrap Field",
       "Up on the ridge, between the cistus and the rocks, lie the white machines from the siege. Grass grows through their joints. "
       "One of them still turns its head when you come closer.",
       [], [O("Goes closer, slowly.", [KAMPF("a3_scrap_drohne"), WEITER("a3_scrap_2")]),
            O("Goes back down. Not today.", [])], ton="ernst"),
    FR("a3_scrap_2", "antenna_ridge", "The Scrap Field",
       "Behind the next rock, two more. They wake up at the same time.",
       [], [O("Stands his ground.", [KAMPF("a3_scrap_paar"), WEITER("a3_scrap_3")]),
            O("Takes the steel he has and goes home.", [F("a3_scrap_field")])], ton="ernst"),
    FR("a3_scrap_3", "antenna_ridge", "The Scrap Field",
       "It is quiet now. You fill your bag with good steel. From up here you can see the villa on the other side of the bay.",
       [], [O("Carries the steel down to the village.", [F("a3_scrap_field")]),
            O("Looks at the villa for a long time first.", [F("a3_scrap_field")])]),
]

# ------------------------------------------------------------------ 5.16 The Board (Tag 31, Dinner, Monaco)
MONACO = [
    E("a3_megan_monaco", "gag1", "ernst", "The Board", PFL(31, "dinner", FL("megan_zurueck")), "main_salon",
      P1("megan"),
      "Megan has put her laptop on the table. She is wearing her boardroom clothes. On the screen: a dark room in Monaco and one man.",
      [JE(G("yamamoto", "[clear throat] Officer-san. So sorry. I have stopped the loan to A.V. I did not ask permission. Very rude of me.", "nervousness"),
          "yama", {"wert": ["vertrauen.yamamoto", ">=", 5]}),
       G("megan", "[sigh] Stay out of the picture, First Officer. And don't breathe so loudly.", "neutral")],
      [O("Stands next to the screen, out of the picture.", [DIREKT([{"wenn": MEGAN_WENDE, "id": "a3_monaco_wende"}, {"id": "a3_monaco_verloren"}])]),
       O("Gives her a glass of water first.", [V("megan", 2), DIREKT([{"wenn": MEGAN_WENDE, "id": "a3_monaco_wende"}, {"id": "a3_monaco_verloren"}])])],
      sets={"megan": "Boardroom"}),
    E("a3_monaco_wende", "gag1", "ernst", "The Board", FRAME(), "main_salon", P1("megan"),
      "The man in Monaco listens with his chin in his hand.",
      [G("megan", "[clear throat] I have names, people who will sign in front of a commission. And papers he can't buy.", "pride"),
       G("megan", "[sigh] It's about a bay that's worth more protected than sold. ...He wants to talk to you, Duc. Is this village worth more than what A.V. pays him?", "neutral")],
      [O("Steps into the picture. “The numbers are hers. The names are the village's. I just carried the letters.”", [F("a3_megan_wende"), V("megan", 6)],
         zeile=G("megan", "[sigh] That's the first argument I've won that I actually believe in. It's uncomfortable.", "relief")),
       O("“Sell them the bay, and you sell them me with it.”", [F("a3_megan_wende"), V("megan", 4)],
         zeile=G("megan", "[chuckle] Bold. He hates bold. It worked.", "relief"))],
      sets={"megan": "Boardroom"}),
    E("a3_monaco_verloren", "gag1", "ernst", "The Board", FRAME(), "main_salon", P1("megan"),
      "The man in Monaco says: Bring me something better than a fishing village, Megan. The screen goes black.",
      [G("megan", "[sigh] How... delightful.", "sadness")],
      [O("“We still have the commission.”", [F("a3_megan_verloren")],
         zeile=G("megan", "[sigh] We have the commission. And we have you. God help us.", "neutral")),
       O("Closes the laptop for her.", [F("a3_megan_verloren"), V("megan", 2)])],
      sets={"megan": "Boardroom"}),
]

# ------------------------------------------------------------------ 5.17 Switched Off (Tag 32, Nachmittag) und 5.19 No Leash (Tag 33)
SANDRU = [
    E("a3_switched_off", "gag1", "ernst", "Switched Off", PFL(32, "nachmittag"), "av_market",
      P1("sandru", ("alva", "?", "comes through the door")),
      "Mina comes running: The market. It's Sandru. In the A.V. Market, Sandru is sitting on the floor between the white shelves. "
      "The braces on his legs are quiet. You never noticed the sound until it stopped. A small screen on his knee says: "
      "Device paused. The user broke the rules of service. Thank you for your understanding.",
      [G("sandru", "[laugh] Ha. They switched me off. Like a lamp.", "sadness"),
       JE(G("sandru", "[sigh] You heard them hum, the first day you came in here. Now listen.", "sadness"), "summen", FL("sandru_surren")),
       JE(G("sandru", "[sigh] They found the tin. My mother's recipes, under his sign.", "sadness"), "dose", FL("a3_los_system_markt")),
       G("sandru", "[clear throat] And now the screen says I can walk again if I don't talk to the commission. He wants my mouth for my legs.", "anger"),
       G("alva", "[sigh] Duc. The door. Can you hold the door?", "neutral")],
      [O("Holds the door.", [F("a3_switched_off"), DIREKT("a3_switched_off_alva")]),
       O("Takes his other arm.", [F("a3_switched_off"), V("sandru", 2), DIREKT("a3_switched_off_alva")]),
       O("Steps back and lets Alva do it.", [F("a3_switched_off"), V("alva", 2), DIREKT("a3_switched_off_alva")])],
      sets={"sandru": "sandru_av", "alva": "alva_standard"}),
    E("a3_switched_off_alva", "gag1", "ernst", "Alva", FRAME(), "village_piazza", P1("alva", ("sandru", "?", "is carried")),
      "Alva has not stepped into her mother's old shop since her mother left for Seville. Today she carries her brother out of it, "
      "across the street, and up the stairs.",
      [G("alva", "[sigh] You're my little brother, you idiot. I've carried you since you were six.", "caring"),
       G("sandru", "[sniff] I know. That's the whole problem.", "sadness")],
      [O("Walks behind them up the stairs.", []),
       O("Waits at the bottom of the stairs, so they can be alone.", [V("alva", 2)])],
      sets={"alva": "alva_standard", "sandru": "sandru_av"}),
    E("a3_schiene", "gag1", "wholesome", "No Leash", PFL(33, "fruehstueck", {"alle": [FL("a3_switched_off"), GEKUEMMERT]}), "alvas_bar",
      P1("sandru", ("rosi", "+", "is proud")),
      "Sandru sits on a chair in Alva's bar. On his legs: the same braces, with a new box on the side, painted in Rosi's colours.",
      [JE(G("rosi", "[clear throat] Same motors. Same chips. I only took out the part that talks to his computers. The leash, Officer. Like with the collars. "
                    "That sound is mine now. Don't let them tell you otherwise.", "pride"), "rosi", DA("rosi")),
       JE(G("maxwell", "[laugh] Rosi says which way on the video, I hold the screwdriver. Teamwork, brother.", "pride"), "rosi", None),
       G("sandru", "[chuckle] A.V. gave me six years of walking. You gave me a speech. ...And her. You gave me her. "
                   "So what do I do now, Duc? Walk over there and say what?", "nervousness")],
      [O("“Say thank you. Then say nothing.”", [F("a3_sandru_schiene"), F("a3_zeuge_sandru"), V("sandru", 4)],
         zeile=G("sandru", "[laugh] Ha. One thing at a time, Duc.", "amusement")),
       O("“Go and stand in front of Alva. Straight.”", [F("a3_sandru_schiene"), F("a3_zeuge_sandru"), V("sandru", 6)],
         zeile=G("sandru", "[sigh] Straight. Okay. ...She's going to cry. I'm going to cry.", "nervousness")),
       O("Shrugs. “You gave yourself the speech. I just listened.”", [F("a3_sandru_schiene"), F("a3_zeuge_sandru"), V("sandru", 4)],
         zeile=G("sandru", "[chuckle] Then I'll give it to the men from Ajaccio too. The whole thing.", "pride"))],
      sets={"sandru": "sandru_frei", "rosi": "Engine Room"}),
    E("a3_sandru_alon", "gag1", "ernst", "Back On", PFL(33, "fruehstueck", {"alle": [FL("a3_switched_off"), NICHT(GEKUEMMERT)]}), "village_piazza",
      P1("sandru"),
      "In the morning Sandru walks across the square again. The braces hum. He doesn't look at you.",
      [G("sandru", "[sigh] I said yes to the screen, Duc. Legs for a quiet mouth. Don't look at me like that. Nobody else offered.", "sadness")],
      [O("“I should have offered. I'm sorry.”", [F("a3_sandru_alon"), V("sandru", 2)],
         zeile=G("sandru", "[sigh] Yeah. Me too.", "sadness")),
       O("Lets him walk past.", [F("a3_sandru_alon")])],
      sets={"sandru": "sandru_av"}),
]

# ------------------------------------------------------------------ 5.20 An Invitation (Tag 33, Tag)
EINLADUNG = [
    E("a3_einladung", "gag1", "ernst", "An Invitation", PFL(33, "tag"), "village_piazza", P1("mina"),
      "Mina hands you an envelope made of very good paper. Your name is on it, in a careful hand.",
      [G("mina", "[clear throat] This one's for you, Yacht. The good paper. From the house on the hill.", "nervousness"),
       JE(G("mina", "[sigh] It says: Dinner. Tomorrow at eight. Just you. A.V. ...Yacht, that's the hand from the name sheet you picked up at the gate. "
                    "And from the letters on the church steps.", "fear"), "hand", FL("bl_blatt_gefunden")),
       JE(G("mina", "[sigh] It says: Dinner. Tomorrow at eight. Just you. A.V.", "fear"), "hand", None),
       G("mina", "[clear throat] Are you going?", "nervousness")],
      [O("“Yes.”", [F("a3_einladung")]),
       O("“Yes. But not alone.”", [F("a3_einladung"), F("a3_villa_nicht_allein")]),
       O("“I don't know yet.”", [F("a3_einladung")])]),
]

# ------------------------------------------------------------------ 5.21 After Midnight (Tag 33, Abend) - Seiten wie in der Belagerung
MN_FRAUEN = [("chiara", "Chiara"), ("alva", "Alva"), ("lea", "Lea"), ("sophia", "Sophia"), ("rosi", "Rosi"),
             ("lola", "Lola"), ("siri", "Siri"), ("bibi", "Bibi"), ("megan", "Megan")]


def _mn_bereit(pid):
    """Duc 04.11.2026: Jede Frau mit Vertrauen 4 und Begehren 4 laedt ein (Megan: Vertrauen 4 und megan_funke). Duc antwortet jeder."""
    if pid == "megan":
        return {"alle": [FL("megan_funke"), {"wert": ["vertrauen.megan", ">=", 4]}]}
    b = [{"wert": ["vertrauen." + pid, ">=", 4]}, {"wert": ["begehren." + pid, ">=", 4]}, DA(pid)]
    if pid == "bibi":
        b.append(FL("rt_bibi_bleibt"))
    return {"alle": b}


MN_FRAGE = {
    "chiara": ("[clear throat] First Officer. I'll ask you once, and if you laugh, it's a two. After midnight, on the mole. Will you come?", "nervousness"),
    "alva": ("[chuckle] After my dance, Duc, I close the bar for one hour. Will you be on the quay?", "desire"),
    "lea": ("[sigh] After midnight, on the mole. Will you come? Proper come?", "nervousness"),
    "sophia": ("[chuckle] Ten euros says you'll come down to the mole after midnight. ...Oh. Have I just lost?", "amusement"),
    "rosi": ("[clear throat] Officer. At midnight I take off this stupid dress. Will you be on the mole after that?", "embarrassment"),
    "lola": ("[laugh] Boss. When the cooking's done. One song, just us, on the mole. Mostly one song. Yes?", "joy"),
    "siri": ("[sigh] No camera after midnight. Will you meet me by the water?", "nervousness"),
    "bibi": ("[chuckle] The gates open on Sunday afternoon, and I'll be a mess. After midnight, will you come anyway?", "desire"),
    "megan": ("[sigh] Don't make me say it twice, First Officer. The aft deck, after midnight. Then we never speak of it. Agreed?", "desire"),
}
MN_NEIN = {
    "chiara": "[sigh] Okay. That's a three. ...For the night, not for you.",
    "alva": "[chuckle] Fine. I'll close the bar for nobody, then. Nobody is good company.",
    "lea": "[sniff] Okay. Did you know octopuses hide when they're sad? I'm going to hide a bit.",
    "sophia": "[sigh] Then I keep my ten euros. It's not much comfort, darling.",
    "rosi": "[clear throat] Okay. The dress comes off anyway. For me.",
    "lola": "[sigh] Oh. No worries, Boss. Mostly no worries.",
    "siri": "[sigh] Okay. Thank you for saying it to my face. Nobody does that.",
    "bibi": "[sigh] Then I'll sit with the animals. They never say no.",
    "megan": "[clear throat] Noted, First Officer. We never spoke of it. That part is easy.",
}
MN_REIHE = [p for p, _n in MN_FRAUEN]


def _mn_weiter(ab):
    """Zur naechsten Frau, die einlaedt (nach Ja: die ehrliche Absage), am Ende der Abschluss."""
    ziele = []
    for p in MN_REIHE[ab + 1:]:
        ziele += [{"wenn": {"alle": [_mn_bereit(p), FL("a3_mitternacht")]}, "id": "a3_einl_%s_spaet" % p},
                  {"wenn": _mn_bereit(p), "id": "a3_einl_" + p}]
    return DIREKT(ziele + [{"wenn": FL("a3_mitternacht"), "id": "a3_einl_ende_ja"}, {"id": "a3_einl_ende_nein"}])


MITTERNACHT = [
    E("a3_mn_start", "gag1", "wholesome", "After Midnight", PFL(33, "abend"), "village_harbour", P1("mina"),
      "The evening before the villa. The festa is the day after tomorrow, and everybody already knows: after midnight, the mole "
      "belongs to whoever is standing there with you. Tonight, people come to ask.",
      [G("mina", "[chuckle] Yacht. Everybody's asking who you'll be with after midnight. I'm not asking. I just know you'll have to answer.", "amusement")],
      [O("Waits on the quay.", [_mn_weiter(-1)])]),
] + [
    E("a3_einl_" + pid, "gag1", "frech", "After Midnight", FRAME(), ["village_harbour", "alvas_bar", "village_piazza"][n % 3], P1(pid),
      "She finds you before you find her.",
      [G(pid, MN_FRAGE[pid][0], MN_FRAGE[pid][1])],
      [O("“Yes.”", [F("a3_mitternacht_" + pid), F("a3_mitternacht"), _mn_weiter(n)]),
       O("“Not this time. I'm sorry.”", [F("a3_mitternacht_nein_" + pid), _mn_weiter(n)],
         zeile=G(pid, MN_NEIN[pid], "sadness"))]) for n, pid in enumerate(MN_REIHE)
] + [
    E("a3_einl_%s_spaet" % pid, "gag1", "wholesome", "After Midnight", FRAME(), ["village_harbour", "alvas_bar", "village_piazza"][n % 3], P1(pid),
      "She finds you too. You have already said yes to someone tonight.",
      [G(pid, MN_FRAGE[pid][0], MN_FRAGE[pid][1])],
      [O("“I already said yes to someone else. I'm sorry. You deserve the truth.”", [F("a3_mitternacht_nein_" + pid), V(pid, 2), _mn_weiter(n)],
         zeile=G(pid, MN_NEIN[pid], "sadness")),
       O("“Not tonight.”", [F("a3_mitternacht_nein_" + pid), _mn_weiter(n)],
         zeile=G(pid, MN_NEIN[pid], "sadness"))]) for n, pid in enumerate(MN_REIHE)
] + [
    E("a3_einl_ende_ja", "gag1", "wholesome", "After Midnight", FRAME(), "village_harbour", P1("mina"),
      "The quay is quiet again. You said yes once tonight, and only once.",
      [G("mina", "[chuckle] Good night, Yacht. Don't be late on Sunday. Midnight comes fast at a festa.", "amusement")],
      [O("Goes to bed.", [])]),
    E("a3_einl_ende_nein", "gag1", "wholesome", "After Midnight", FRAME(), "village_harbour", P1("mina"),
      "The quay is quiet again. Nobody waits for you after midnight, and that's fine. The festa is for everyone.",
      [G("mina", "[chuckle] Nobody? Then you dance with me. Once. Badly.", "amusement")],
      [O("“Deal, Mina.”", [F("a3_mitternacht_niemand")])]),
]

# ------------------------------------------------------------------ 5.22 - 5.24 Die Villa (Tag 34)
VILLA = [
    E("a3_villa_plan", "gag1", "ernst", "The Back Way", PFL(34, "fruehstueck"), "village_harbour", P1("holm", ("rosi", "?", "has her tools")),
      "The morning of the dinner. Holm, Rosi and Madame Casanova stand at the end of the quay. Up on the hill, the villa shines in the sun.",
      [G("holm", "[clear throat] You're invited, Frankfurt. That's better than a search warrant.", "neutral"),
       JE(G("rosi", "[chuckle] A cellar door nobody locks properly. Old iron. My favourite kind of door.", "pride"), "weg", FL("a3_kellerschluessel")),
       JE(G("casanova", "[sigh] I know the cellar. I hid there from my father when I was seven. I'll take you.", "sadness"), "weg", None),
       G("holm", "[clear throat] Who goes down with you, Frankfurt?", "neutral")],
      [O("Nods at Rosi. “You and me.”", [F("a3_villa_mit_rosi")]),
       O("Turns to Madame Casanova. “Show me the way, Madame.”", [F("a3_villa_mit_casanova"), V("casanova", 2)]),
       O("Picks up the key. “I'll go alone.”", [F("a3_villa_allein")])],
      sets={"holm": "holm_shirt", "rosi": "Engine Room"}),
    E("a3_villa_keller", "gag1", "ernst", "The Wine Cellar", PFL(34, "tag"), "power_room", P1("casanova"),
      "The cellar under the villa. Wine barrels, very old, and between them a tall black cabinet with blue lights. It hums. "
      "Madame Casanova stops at the door.",
      [JE(G("casanova", "[sigh] It's smaller than I remember. ...Go. I'll wait here.", "sadness"), "tuer", FL("a3_villa_mit_casanova")),
       JE(G("rosi", "[sigh] He put his computers in a wine cellar. That's a crime too.", "disgust"), "tuer", FL("a3_villa_mit_rosi")),
       JE(G("casanova", "[sigh] My father kept his best wine down here. Now look at it.", "sadness"), "tuer", None)],
      [O("Goes to the cabinet.", [KAMPF("a3_villa_keller"), DIREKT("a3_villa_ordner")])]),
    E("a3_villa_ordner", "gag1", "ernst", "White's Orders", FRAME(), "power_room", P1("casanova"),
      "Under the stairs is a small office with a folder on the desk. A plan, typed, with a stamp: Day 22, phase 3: torches, houses. "
      "Under it, a receipt. Paid to Captain Buenaventura, in clean money.",
      [G("casanova", "[gasp] ...Torches, houses. He wrote it down. Like a shopping list.", "anger")],
      [O("Puts the folder under his jacket.", [F("a3_beweis_feuer"), F("a3_villa_keller")]),
       O("Takes a photo of every page, then the folder too.", [F("a3_beweis_feuer"), F("a3_villa_keller")])]),
    E("a3_villa_dinner", "gag1", "ernst", "Name Your Price", PFL(34, "dinner"), "alon_keynote", P1("alon", ("pascal", "?", "stands at the door")),
      "A long table for two. A big window over the bay. From up here the village looks like a model, and the building sites look like toys. "
      "Pascal stands at the door in his white fedora. He doesn't say anything.",
      [G("alon", "[chuckle] Duc. Sit. Two of my people are asleep in my cellar, so I think you came the back way. You've been busy.", "neutral"),
       G("alon", "[sigh] Keep the folder. Paper. In my experience, paper loses.", "neutral"),
       G("alon", "[clear throat] Every collar your mechanic cut open sent me one last message. That's how I learned to lock them. "
                 "You helped me more than any engineer I hired.", "pride"),
       G("alon", "[sigh] Four hundred thousand people died in wars last year. I can bring that to zero. I need one bay and ten more years. "
                 "I don't have ten years. So I need the bay now.", "neutral"),
       G("alon", "[clear throat] Join me. Name your price.", "neutral")],
      [O("“No.”", [F("a3_alon_nein")]),
       O("Looks out of the window at the village and says nothing.", [F("a3_alon_nein")]),
       O("“What would my price be?”", [DIREKT("a3_villa_preis")]),
       O("Puts his glass down. “Everyone I've met down there. Can you buy that?”", [F("a3_alon_nein")],
         zeile=G("alon", "[sigh] I can buy most of them. I already did. But not tonight, I see.", "disappointment"))],
      sets={"alon": "alon_standard"}),
    E("a3_villa_preis", "gag1", "ernst", "Name Your Price", FRAME(), "alon_keynote", P1("alon"),
      "Alon smiles like a man who already wrote the contract.",
      [G("alon", "[chuckle] Eden Consulting, free of debt. Your name on a building in Frankfurt. And you never think about this village again. So?", "neutral")],
      [O("“Deal.”", [F("a3_deal")],
         zeile=G("alon", "[laugh] Welcome to the team. Again. This time for real.", "pride")),
       O("“No.”", [F("a3_alon_nein")],
         zeile=G("alon", "[sigh] Pity. I liked you.", "disappointment")),
       O("“Deal. But we sign it tomorrow night, in front of the village.”",
         [DIREKT([{"wenn": STERN, "id": "a3_villa_stern"}, {"id": "a3_villa_publikum"}])])],
      sets={"alon": "alon_standard"}),
    E("a3_villa_publikum", "gag1", "ernst", "Name Your Price", FRAME(), "alon_keynote", P1("alon"),
      "Alon laughs quietly and shakes his head.",
      [G("alon", "[chuckle] An audience? No, Duc. You don't have enough people for that. Here, tonight, or not at all.", "neutral")],
      [O("“Deal.”", [F("a3_deal")],
         zeile=G("alon", "[laugh] Welcome to the team. Again. This time for real.", "pride")),
       O("“No.”", [F("a3_alon_nein")],
         zeile=G("alon", "[sigh] Pity. I liked you.", "disappointment"))],
      sets={"alon": "alon_standard"}),
    E("a3_villa_stern", "gag1", "ernst", "The Long Game", FRAME(), "alon_keynote", P1("alon", ("pascal", "?", "goes pale")),
      "For a second, Alon says nothing. Then he smiles, the stage smile.",
      [G("alon", "[laugh] In front of the village. With cameras. A consultant who finally understands marketing. Fine. Tomorrow night.", "pride"),
       G("yamamoto", "[clear throat] So sorry, Officer-san. My bank has already stopped his loan. He does not know yet. Very rude of me.", "nervousness")],
      [O("Shakes Alon's hand and smiles back.", [F("a3_stern")])],
      sets={"alon": "alon_standard"}),
    E("a3_villa_ende", "gag1", "ernst", "The Last Push", PFL(34, "abend"), "alon_keynote", P1("alon", ("pascal", "?", "smiles")),
      "The terrace. A drone camera hums in the air. Alon talks to it with a big smile.",
      [G("alon", "[laugh] Hi, Cala d'Orsu! Quick update from your future. And a big thank you to my partner on the ground, Paul... Paolo. Thank you, Paolo.", "joy")],
      [O("Looks at Pascal, the man who knows every name in the village.",
         [DIREKT([{"wenn": FL("a3_stern"), "id": "a3_villa_lange"}, {"wenn": FL("a3_deal"), "id": "a3_villa_deal"}, {"id": "a3_villa_kampf"}])])],
      sets={"alon": "alon_standard"}),
    E("a3_villa_lange", "gag1", "ernst", "The Long Game", FRAME(), "alon_keynote", P1("casanova", ("alon", "?", "stops smiling")),
      "Below the terrace, torches are coming up the path. Not pirates' torches: the whole village, with candles from the church. "
      "Madame Casanova walks in front. She opens the door of the house she grew up in and steps inside.",
      [G("casanova", "[clear throat] Good evening, Monsieur Varenne. This was my father's house. And this man behind you is Pascal Leca. "
                     "He was my deputy mayor for nine years.", "pride"),
       G("alon", "[sigh] ...Who?", "confusion"),
       G("casanova", "[sigh] Exactly. That is the whole problem with you.", "anger")],
      [O("Tears the contract in two, slowly, in front of the camera.", [F("a3_villa_ende"), F("a3_alon_entlarvt")])],
      sets={"alon": "alon_standard"}),
    E("a3_villa_deal", "gag1", "ernst", "The Last Push", FRAME(), "alon_keynote", P1("alon"),
      "You stand next to Alon in the stream. Down in the village, the phones light up one by one.",
      [G("alon", "[chuckle] Say hello, Duc. They're all watching.", "pride")],
      [O("Waves at the camera.", [F("a3_ende_deal")]),
       O("Doesn't wave.", [F("a3_ende_deal")])],
      sets={"alon": "alon_standard"}),
    E("a3_villa_kampf", "gag1", "ernst", "The Last Push", FRAME(), "alon_keynote", P1("alon"),
      "The camera drone flies away. Alon taps his chest twice, and under the suit something wakes up with a long electric whine.",
      [G("alon", "[sigh] I hoped you'd say yes. Nobody gets hurt when people say yes.", "disappointment"),
       JE(G("rosi", "[clear throat] I took the leash out.", "pride"), "rosi", FL("a3_villa_mit_rosi")),
       JE(G("alon", "[chuckle] I know. That's how I learned to lock it.", "neutral"), "rosi2", FL("a3_villa_mit_rosi"))],
      [O("Stands his ground.", [KAMPF("a3_alon"), F("a3_villa_ende")])],
      sets={"alon": "alon_standard"}),
    E("a3_villa_pascal", "gag1", "ernst", "Pascal", PFL(34, "nacht", NICHT(FL("a3_deal"))), "village_harbour", P1("pascal"),
      "Later, at the mole under the villa. Pascal walks down the path with a small suitcase. He stops next to you.",
      [JE(G("elsa", "[clear throat] Mr. Varenne. Coast guard. You're under arrest, and I'd honestly prefer it if you said nothing.", "neutral"),
          "elsa", {"alle": [FL("elsa_hilft"), {"wert": ["vertrauen.elsa", ">=", 4]}]}),
       JE(G("pascal", "[sigh] Elsa. Your mother's birthday is next week.", "neutral"), "pascal",
          {"alle": [FL("elsa_hilft"), {"wert": ["vertrauen.elsa", ">=", 4]}]}),
       JE(G("pascal", "[sigh] Good night, Monsieur. Everybody has a price. I just never found out mine.", "neutral"), "pascal", None),
       JE(G("wolff", "[clear throat] Three o'clock. 'Not yet.' I remember.", "anger"), "wache", FL("bl_nachtwache_wolff")),
       JE(G("elsa", "[clear throat] For the record, Pascal: three o'clock.", "anger"), "wache", FL("bl_nachtwache_elsa")),
       JE(G("yamamoto", "[sigh] Pascal-san. The coffee was very good. I am still worried.", "sadness"), "wache", FL("bl_nachtwache_yamamoto"))],
      [O("Lets him go.", [DIREKT([{"wenn": {"alle": [FL("elsa_hilft"), {"wert": ["vertrauen.elsa", ">=", 4]}]}, "id": "a3_villa_festnahme"}, {"id": "a3_villa_nacht"}])]),
       O("“Where will you go?”", [DIREKT([{"wenn": {"alle": [FL("elsa_hilft"), {"wert": ["vertrauen.elsa", ">=", 4]}]}, "id": "a3_villa_festnahme"}, {"id": "a3_villa_nacht"}])],
         zeile=G("pascal", "[chuckle] Somewhere with no post office.", "neutral"))],
      sets={"elsa": "Standard"}),
    E("a3_villa_festnahme", "gag1", "ernst", "Arrest", FRAME(), "village_harbour", P1("elsa"),
      "Elsa comes up the path from the mole with two officers from Bastia. Alon walks between them. He has a cut on his lip and he is smiling anyway.",
      [G("elsa", "[sigh] I saw your face on his stream, First Officer. I don't want to know how you got in.", "neutral")],
      [O("“Then I won't tell you.”", [F("a3_alon_festgenommen"), V("elsa", 4)],
         zeile=G("elsa", "[chuckle] Good. Go to bed. Tomorrow you're a witness.", "relief")),
       O("Hands her the folder from the cellar.", [F("a3_alon_festgenommen"), V("elsa", 6)],
         zeile=G("elsa", "[sigh] ...Torches, houses. Thank you. Now go to bed.", "gratitude"))],
      sets={"elsa": "Standard"}),
    E("a3_villa_nacht", "gag1", "ernst", "The Last Night", FRAME(), "village_harbour", P1("mina"),
      "The last night before the commission. The village is quiet. Kevin is on the church roof.",
      [G("mina", "[sigh] Tomorrow, Yacht. Two men and a folding table. Get some sleep.", "neutral")],
      [O("Goes to bed.", [F("a3_letzte_nacht")]),
       O("Sits on the quay a little longer.", [F("a3_letzte_nacht")])]),
]

# ------------------------------------------------------------------ Ligeia (Tag 30, Flaschenpost im Pool)
LIGEIA = [
    E("a3_ligeia_post", "gag1", "wholesome", "A Bottle on the Beach", WANN((30, 33), ["tag", "nachmittag"], bed={"alle": [AKT3, FL("ligeia_freund")]}),
      "village_harbour", P1("lea", ("toto", "?", "found it")),
      "Totò found a bottle on the beach with a wet note inside. The handwriting is very old.",
      [G("lea", "[gasp] It's from her. It says: Sailor. They say the bay will be safe. I would like to sing at something that isn't a shipwreck.", "excitement"),
       JE(G("lea", "[sigh] And: Keep my stone safe. It has waited longer than you.", "caring"), "stein", FL("sirene_weg"))],
      [O("“Then she sings at the festa.”", [F("a3_ligeia_festa")]),
       O("Puts the note in his pocket.", [F("a3_ligeia_festa")])],
      sets={"lea": "Deck"}),
]

EVENTS = IDEE + ORANGE + MAXWELL + LOT14 + SCRAP + MONACO + SANDRU + EINLADUNG + MITTERNACHT + VILLA + LIGEIA

ORTE = {
    "a3_orange": {
        "label": "The Man with the Orange", "bild": "underground_pool_tide", "phasen": ["tag", "nachmittag"],
        "text": "Buenaventura wants to ask the old man in the grotto about tourists. He doesn't want to go alone. Takes the whole phase.",
        "wenn": {"alle": [FL("a3_idee_fertig"), NICHT(FL("a3_orange_fertig"))]},
        "start": [{"id": "a3_orange"}]},
    "a3_lot14": {
        "label": "Lot 14", "bild": "generator_room", "phasen": ["nachmittag", "abend"],
        "text": "Yamamoto found something in A.V.'s property lists. It's about Rosi. Takes the whole phase.",
        "wenn": {"alle": [AKT3, {"tag_ab": 29}, {"wert": ["vertrauen.yamamoto", ">=", 3]}, DA("rosi"), NICHT(FL("a3_lot14"))]},
        "start": [{"id": "a3_lot14"}]},
    "a3_scrap": {
        "label": "The Scrap Field", "bild": "antenna_ridge", "phasen": ["tag", "nachmittag"],
        "text": "Up on the ridge lie the machines from the siege. Some of them still move. Good steel. Takes the whole phase.",
        "wenn": {"alle": [AKT3, {"tag_ab": 25}, NICHT(FL("a3_scrap_field")), {"nicht": {"tag_ab": 34}}]},
        "start": [{"id": "a3_scrap_1"}]},
}


def tags_schreiben():
    return tags_fuer(EVENTS, "akt3_woche5")
