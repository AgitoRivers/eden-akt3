# -*- coding: utf-8 -*-
"""Nebenquest "The Red Trio" in der Macchia (Duc 30.10.2026). Plot, Beats und Bauplan: docs/wiki/welt/nebenquest_red_trio.md.

Die ganze Kette ist spielbar, die Texte sind Entwuerfe aus der Beat-Tabelle. "The Long Table" (rt_tisch, rt_t_*) ist ein Visual Novel, Regeln im Wiki.

Drei Ausfluege in die Macchia, Start in auftraege_eden_rise.py:
  1  rt_auftritt -> Kampf -> rt_lager -> rt_bruecke -> Kampf -> rt_plan_rouge             das Trio trennt sich
  2  rt_gabelung -> Koehlerweg/Danzel, Knochenschlucht/Bibi, Mastgrat/Charly (frei waehlbar, Rast an der Gabelung)
  3  rt_ankunft -> rt_tisch -> rt_white -> 2 Kaempfe -> rt_ende_alle/_getrennt -> rt_bibi_*

Das Trio greift an, sobald es Duc sieht. Weiter geht es nur nach einem Sieg; ko und Reden setzen je ein Flag und bekommen je
einen eigenen Satz (rt_1_ko/_geredet, rt_3_ko/_geredet)."""
from ereignisse_basis import *  # noqa: F401,F403

KAMPF = lambda bid: {"kampf": bid}
WEITER = lambda ziel: {"weiter": ziel}
EXP = {"expedition": "red_trio"}
EXP_ENDE = {"expedition": "ende"}
TAGE = (11, 14)
S = {"danzel": "danzel_B", "bibi": "bibi_A", "charly": "charly_A", "nonna": "nonna_standard", "mrwhite": "mrwhite_A",
     "elsa": "Standard"}
RAST = {"rt_lager", "rt_danzel"}
MUSIK_PFAD = ("rt_auftritt", "rt_flucht", "rt_bruecke", "rt_platte", "rt_gabelung", "rt_drei", "rt_koehler", "rt_knochen", "rt_schlucht", "rt_mast")
SPERRE = {"rt_plan_rouge", "rt_tisch", "rt_white"}

BADGE = item("babel_badge", "Employee Badge", "quest",
             text="A staff badge with the logo taped over. Only one word is left to read: BABEL. Whoever taped it did it neatly.")

PFADE = [("rt_danzel_fertig", "rt_koehlerweg", "Takes the charcoal road, into the burnt forest, after Danzel."),
         ("rt_bibi_fertig", "rt_knochenschlucht", "Takes the gorge, after Bibi."),
         ("rt_charly_fertig", "rt_mastgrat", "Climbs to the ridge with the mast, after Charly.")]


def FR(id, bild, titel, lage, zeilen, optionen, personen=None, ton="ernst"):
    sets = {p: S[p] for p in (personen or [])}
    pers = {"handelnd": personen[0], "betroffen": [{"id": b, "ton": "?", "was": ""} for b in personen[1:]]} if personen else {}
    e = E(id, "ort", ton, titel, WANN(TAGE), bild, pers, lage, zeilen, optionen, sets)
    if id in RAST or id.startswith("rt_gabelung"):
        e["rast"] = True
    if id in SPERRE or id.startswith("rt_t_"):
        e["sperre"] = True
    if id == "rt_tisch" or id.startswith("rt_t_"):     # Visual Novel: nach der Wahl direkt der naechste Frame
        e["flott"] = True
        e["musik"] = "anhoerung_gestaendnis"
    elif id == "rt_white":                             # Stille, bis der Kampf beginnt
        e["musik"] = "stille"
    elif id.startswith(MUSIK_PFAD):
        e["musik"] = "expedition_macchia"
    return e


def gabel_id(offen):
    """Frame der Gabelung je nach noch offenen Pfaden (Bits in der Reihenfolge von PFADE)."""
    return "rt_gabelung_" + "".join("1" if p in offen else "0" for p, _, _ in PFADE)


def zur_gabel():
    """Weiter-Liste: naechste Gabelung, oder heim, wenn alle drei gefunden sind."""
    ziele = []
    for maske in range(8):
        erledigt = [PFADE[i][0] for i in range(3) if maske & (1 << i)]
        offen = [PFADE[i][0] for i in range(3) if not maske & (1 << i)]
        if not offen:
            continue
        ziele.append({"wenn": {"alle": [{"flag": x} for x in erledigt] + [{"nicht": {"flag": x}} for x in offen]}, "id": gabel_id(offen)})
    return [{"wenn": {"alle": [{"flag": p} for p, _, _ in PFADE]}, "id": "rt_drei_gefunden"}] + ziele


def gabelung(offen):
    return FR(gabel_id(offen), "macchia_three_ways", "Three Ways",
              "This is where the men in black suits scattered Danzel, Bibi and Charly. “Shepherd's hut, tonight,” Danzel shouted. Three "
              "trails leave the clearing, each with footprints on it, running, and none of them lead towards the hut. These three "
              "don't know the macchia at all.",
              [], [O(t, [WEITER(z)]) for p, z, t in PFADE if p in offen])


NACH_1 = [{"wenn": {"flag": "rt_1_geredet"}, "id": "rt_flucht_geredet"}, {"id": "rt_flucht_ko"}]
NACH_3 = [{"wenn": {"flag": "rt_3_geredet"}, "id": "rt_bruecke_geredet"}, {"id": "rt_bruecke_ko"}]
PLATTE = [{"wenn": {"jacke_verbaut": True}, "id": "rt_platte_verbaut"}, {"id": "rt_platte_truhe"}]
GEFUNDEN = [F("rt_notiz_lager")]

# ------------------------------------------------------------------ The Long Table (Visual Novel, Wiki: nebenquest_red_trio.md)
K = "monastery_kitchen"
STILL = lambda m: F("rt_t_still_" + m)
REIN = lambda m: F("rt_t_rein_" + m)
PLUS = lambda p, m: F("rt_t_plus_%s_%s" % (p, m))
MINUS = lambda p, m: F("rt_t_minus_%s_%s" % (p, m))
NICHTS = "Says nothing."
NACH_FRAGE = [{"wenn": {"flag": "kl_loewe_frei"}, "id": "rt_t_frage_frei"}, {"id": "rt_t_frage_erloest"}]
NACH_D1 = [{"wenn": {"flag": "rt_notiz_gesteht"}, "id": "rt_t_d1_gesteht"}, {"id": "rt_t_d1_brief"}]
NACH_C1 = [{"wenn": {"flag": "rt_notiz_spiel"}, "id": "rt_t_c1_spiel"}, {"id": "rt_t_c1_mutter"}]
NACH_B = [{"wenn": {"flag": "rt_notiz_wahrheit"}, "id": "rt_t_b_wahrheit"}, {"id": "rt_t_b_notizbuch"}]
NACH_NONNA = [{"wenn": {"flags_anzahl": ["rt_t_still_", ">=", 5]}, "id": "rt_t_riss_still"},
              {"wenn": {"flags_anzahl": ["rt_t_rein_", ">=", 5]}, "id": "rt_t_riss_rein"}, {"id": "rt_t_haelt"}]
D1_LAGE = "Bibi turns to Danzel. Her voice is very quiet."
D1_ZEILE = [Z("bibi", "On the bridge I asked you something. What did you do at the lab?", "sadness")]
D1_STILL = O(NICHTS, [STILL("d1"), PLUS("danzel", "d1"), WEITER("rt_t_d1r_still")])
C1_LAGE = ("Charly puts her hand on the table, very flat. You know that name, an arms company. For years you have crossed it off clients' "
           "lists, and she can see that you know it. She looks at you and waits for a verdict. Bibi gets there first.")
C1_ZEILE = [Z("bibi", "You didn't care. Not about him and not about us. For you it was just a puzzle.", "anger")]
C1_STILL = O(NICHTS, [STILL("c1"), PLUS("charly", "c1"), WEITER("rt_t_c1r_still")])
B_LAGE = "Bibi stops."
B_ZEILE = [Z("bibi", "Good. Good, so now I know. Two years. I loved you both, and you –", "anger"),
           Z("charly", "You fed him, Bibi. For two years. You carried the food in yourself. You saw the scars.", "sadness")]
B_STILL = O(NICHTS, [STILL("b"), PLUS("bibi", "b"), WEITER("rt_t_br_still")])
NONNA_ZEILEN = [
    Z("nonna", "I am old. I am not deaf.", "neutral"),
    Z("nonna", "I looked for it, you know. Just now, while you talked. I looked for the hate. I have had a long life and a warm one, and I can't find any. There was never anywhere to keep it.", "sadness"),
    Z("nonna", "You wanted me to shout. That would be easier for you. No.", "neutral"),
    Z("nonna", "Ambrosius would have fed you. He fed everyone. So I will too. Eat.", "caring"),
    Z("nonna", "In the morning you go to Elsa, and you say to her what you said at my table. All of it. With your names.", "neutral")]


def WEITER_ZU(id, bild, titel, lage, zeilen, text, ziel, personen, ton="ernst"):
    """Reaktion ohne Wahl: lesen und weiter."""
    return FR(id, bild, titel, lage, zeilen, [O(text, [WEITER(ziel)])], personen=personen, ton=ton)


TISCH = [
    FR("rt_tisch", K, "The Long Table",
       "Nonna serves the soup. She talks while she does it. She doesn't know who she is talking to.",
       [Z("nonna", "Brother Ambrosius, up at the monastery, always baked his bread too dark. Brother Teo said good morning to the bees. Every morning. One by one.", "sadness"),
        Z("nonna", "Then the animals came down. And at the end, a lion. A black one, with steel on his shoulders.", "sadness")],
       [O("Doesn't touch his spoon.", [WEITER([{"wenn": {"flag": "rt_duc_ehrlich"}, "id": "rt_t_weiss"}, {"id": "rt_t_frage"}])])],
       personen=["nonna", "danzel", "bibi", "charly"]),
    WEITER_ZU("rt_t_weiss", K, "The Long Table",
              "Danzel puts his spoon down. Bibi looks at you, and then at the table. She already knows. She says nothing.",
              [], "Says nothing either.", "rt_t_d1", ["bibi", "danzel"]),
    FR("rt_t_frage", K, "The Long Table", "Danzel puts his spoon down. Bibi's hand has stopped halfway to the bread.",
       [Z("bibi", "You were up there. You went into that cave. Tell me.", "fear")],
       [O("Tells her.", [REIN("l"), PLUS("bibi", "l"),
                         WEITER(NACH_FRAGE)]),
        O("“I don't know what you mean.”", [STILL("l"), MINUS("bibi", "l"), MINUS("bibi", "l2"), WEITER("rt_t_luege")])],
       personen=["bibi", "danzel"]),
    WEITER_ZU("rt_t_frage_frei", K, "The Long Table",
              "You tell her. You cut the chip out of his neck, and he walked away. Nobody has seen him since. Bibi cries without a sound.",
              [], "Waits.", "rt_t_d1", ["bibi"]),
    WEITER_ZU("rt_t_frage_erloest", K, "The Long Table",
              "You tell her. It was quick, and he didn't try to get up. Bibi cries without a sound.",
              [], "Waits.", "rt_t_d1", ["bibi"]),
    WEITER_ZU("rt_t_luege", K, "The Long Table", "She looks at you for a long time. Nonna doesn't look up from the pot.",
              [Z("nonna", "He knows. He is the one who went up there.", "neutral")], "Looks at his plate. Then he tells her.", NACH_FRAGE, ["nonna", "bibi"]),
    # Danzel
    WEITER_ZU("rt_t_d1", K, "Danzel", "Nobody eats. The soup goes cold in five bowls.", [], "Waits.", NACH_D1, ["bibi", "danzel"]),
    FR("rt_t_d1_gesteht", K, "Danzel", D1_LAGE, D1_ZEILE,
       [O("Looks at Danzel and nods: tell her, like you promised.", [REIN("d1"), PLUS("danzel", "d1"), PLUS("bibi", "d1"), WEITER("rt_t_d1r_gesteht")]), D1_STILL],
       personen=["bibi", "danzel"]),
    FR("rt_t_d1_brief", K, "Danzel", D1_LAGE, D1_ZEILE,
       [O("Puts Danzel's letter on the table, the resignation he never sent.", [REIN("d1"), MINUS("danzel", "d1"), PLUS("bibi", "d1"), WEITER("rt_t_d1r_brief")]), D1_STILL],
       personen=["bibi", "danzel"]),
    WEITER_ZU("rt_t_d1r_gesteht", K, "Danzel", "He takes a breath.",
              [Z("danzel", "I designed the plates. I thought they were for agents, and then I heard what they were for. I was going to tell you tonight.", "sadness")],
              "Listens.", "rt_t_d2", ["danzel", "bibi"]),
    WEITER_ZU("rt_t_d1r_brief", K, "Danzel", "Bibi reads the date. She reads the rest. Danzel looks at you, and then he looks away.",
              [Z("bibi", "You wrote this. You never sent it.", "sadness"), Z("danzel", "No.", "sadness")],
              "Listens.", "rt_t_d2", ["bibi", "danzel"]),
    WEITER_ZU("rt_t_d1r_still", K, "Danzel", "It takes him a long time.",
              [Z("danzel", "I designed the plates, all of them. It took eleven days, and I was proud of them.", "sadness")],
              "Listens.", "rt_t_d2", ["danzel", "bibi"]),
    FR("rt_t_d2", K, "Danzel", "She doesn't raise her voice. That is the worst part.",
       [Z("bibi", "You sat across from me at lunch for a year. I told you what he ate. How much he weighed.", "sadness"),
        Z("danzel", "I know.", "sadness"),
        Z("bibi", "You would have stayed quiet forever.", "anger")],
       [O("“He stole that plate for you. That could have got him killed.”", [REIN("d2"), PLUS("bibi", "d2"), MINUS("danzel", "d2"), WEITER("rt_t_d2r_rein")]),
        O(NICHTS, [STILL("d2"), PLUS("danzel", "d2"), WEITER("rt_t_d2r_still")])],
       personen=["bibi", "danzel"]),
    WEITER_ZU("rt_t_d2r_rein", K, "Danzel", "Bibi goes on looking at him. Danzel shakes his head at you.",
              [Z("danzel", "Please don't. It doesn't help.", "sadness")], "Stops talking.", "rt_t_c0", ["danzel", "bibi"]),
    WEITER_ZU("rt_t_d2r_still", K, "Danzel", "He looks up, for the first time.",
              [Z("danzel", "Maybe. Probably. That's why I stole the plate. It's the only brave thing I ever did. I did it so I could look at you again.", "sadness")],
              "Lets that stand.", "rt_t_c0", ["danzel", "bibi"]),
    # Charly
    FR("rt_t_c0", K, "Charly", "Nobody has looked at Charly yet. She hasn't touched her soup, and the crisps are still in her jacket.",
       [Z("bibi", "And you? You do something with code.", "sadness"),
        Z("charly", "Yes.", "neutral"),
        Z("bibi", "What code?", "anger"),
        Z("charly", "The collars. I wrote the collars. I knew what they were for. I knew the whole time.", "sadness"),
        Z("charly", "My name is Charlotte de Ravenel. Ravenel Défense. Yes. Those ones.", "neutral"),
        Z("charly", "Red team. It sounded better than accomplices.", "sadness")],
       [O("Doesn't look away.", [WEITER(NACH_C1)])], personen=["bibi", "charly"]),
    FR("rt_t_c1_spiel", K, "Charly", C1_LAGE, C1_ZEILE,
       [O("“Charly. Show her the game on your phone.”", [REIN("c1"), PLUS("charly", "c1"), PLUS("bibi", "c1"), WEITER("rt_t_c1r_spiel")]), C1_STILL],
       personen=["bibi", "charly"]),
    FR("rt_t_c1_mutter", K, "Charly", C1_LAGE, C1_ZEILE,
       [O("“Her mother called. She tried to leave the collar project in March.”", [REIN("c1"), MINUS("charly", "c1"), PLUS("bibi", "c1"), WEITER("rt_t_c1r_mutter")]), C1_STILL],
       personen=["bibi", "charly"]),
    WEITER_ZU("rt_t_c1r_spiel", K, "Charly", "She puts it on the table. Three small figures in red suits run across the screen.",
              [Z("bibi", "...Is that me? With the grenades?", "confusion"), Z("charly", "Two out of ten. The jump is bad.", "sadness")],
              "Watches them run.", "rt_t_dc", ["bibi", "charly"]),
    WEITER_ZU("rt_t_c1r_mutter", K, "Charly", "For a moment nobody moves.",
              [Z("charly", "That wasn't yours to tell.", "anger"), Z("bibi", "...March?", "confusion")],
              "Looks at his hands.", "rt_t_dc", ["charly", "bibi"]),
    WEITER_ZU("rt_t_c1r_still", K, "Charly", "She takes her time. She has never taken her time before.",
              [Z("charly", "It was a puzzle. Until it wasn't. I don't have a number for when.", "sadness")],
              "Lets that stand.", "rt_t_dc", ["charly", "bibi"]),
    # Danzel und Charly
    FR("rt_t_dc", K, "Danzel and Charly", "Danzel has been looking at Charly this whole time.",
       [Z("danzel", "You read my plans. You knew where my plates were going. And you let me keep working.", "anger"),
        Z("charly", "Yes.", "neutral"),
        Z("danzel", "You sat there eating crisps. You were laughing at me.", "anger")],
       [O("“I heard her at the fire. ‘We find proof. Together.’ That isn't laughing.”",
          [REIN("dc"), PLUS("charly", "dc"), PLUS("danzel", "dc"), WEITER("rt_t_dcr_rein")]),
        O(NICHTS, [STILL("dc"), PLUS("danzel", "dc"), WEITER("rt_t_dcr_still")])],
       personen=["danzel", "charly"]),
    WEITER_ZU("rt_t_dcr_rein", K, "Danzel and Charly", "Danzel looks at you. Then at her.",
              [Z("charly", "You were the best part of my day. I never gave you a number for that.", "sadness")],
              "Listens.", "rt_t_b0", ["charly", "danzel"]),
    WEITER_ZU("rt_t_dcr_still", K, "Danzel and Charly", "A long pause. Danzel looks away.",
              [Z("charly", "I wasn't laughing.", "sadness"), Z("charly", "You were the best part of my day.", "sadness")],
              "Listens.", "rt_t_b0", ["charly", "danzel"]),
    # Bibi
    WEITER_ZU("rt_t_b0", K, "Bibi", "Bibi has pushed her chair back. Her hands are shaking.", [], "Waits.", NACH_B, ["bibi", "charly"]),
    FR("rt_t_b_notizbuch", K, "Bibi", B_LAGE, B_ZEILE,
       [O("Puts Bibi's notebook on the table, the one she left with you at the cave.", [REIN("b"), PLUS("bibi", "b"), WEITER("rt_t_br_notizbuch")]), B_STILL],
       personen=["bibi", "charly"]),
    FR("rt_t_b_wahrheit", K, "Bibi", B_LAGE, B_ZEILE,
       [O("“She went looking for Mochi when nobody else did.”", [REIN("b"), PLUS("bibi", "b"), WEITER("rt_t_br_wahrheit")]), B_STILL],
       personen=["bibi", "charly"]),
    WEITER_ZU("rt_t_br_notizbuch", K, "Bibi", "She opens it and turns the pages until she finds the place. Three times, in her small handwriting.",
              [Z("bibi", "I told Julien, my boyfriend, who ran the lab. Three times. He said it was fine. I believed him.", "sadness")],
              "Waits.", "rt_t_nonna", ["bibi"]),
    WEITER_ZU("rt_t_br_wahrheit", K, "Bibi", "Bibi looks at you. For the first time since the cave.",
              [Z("bibi", "I saw them. I told Julien, my boyfriend, who ran the lab, and he said it was fine. I wanted it to be fine.", "sadness")], "Holds her eyes.", "rt_t_nonna", ["bibi"]),
    WEITER_ZU("rt_t_br_still", K, "Bibi", "She doesn't say anything else for a while.",
              [Z("bibi", "...Yes. I saw them.", "sadness")], "Waits.", "rt_t_nonna", ["bibi"]),
    # Nonna
    FR("rt_t_nonna", K, "Nonna", "Nobody speaks. Nonna stopped moving some time ago. She is holding the bread. She cuts it. Four pieces, then one more.",
       NONNA_ZEILEN, [O("Doesn't move.", [WEITER([{"wenn": {"flag": "kloster_frederico_tot"}, "id": "rt_t_ziege"}] + NACH_NONNA)])],
       personen=["nonna"]),
    WEITER_ZU("rt_t_ziege", K, "Nonna", "She takes one of the little wooden animals the boy Frederico carves, a goat, out of her apron and sets it next to the bread. She doesn't say anything about it.",
              [], "Looks at it.", NACH_NONNA, ["nonna"]),
    # Ausgang
    FR("rt_t_haelt", K, "The Long Table", "Bibi takes a piece of bread. She looks at it for a while. Then she pushes it across to Danzel.",
       [], [O("Takes a piece too.", [{"tisch_vertrauen": {"praefix": "rt_t_", "personen": ["danzel", "bibi", "charly"]}},
                                     F("rt_ausgang_alle"), F("rt_tisch_fertig"), WEITER("rt_white")])],
       personen=["bibi", "danzel"], ton="wholesome"),
    WEITER_ZU("rt_t_riss_still", K, "The Long Table", "Bibi gets up. Nonna takes her plate away without a word.",
              [Z("bibi", "You just sat there. All of it. You just sat there.", "anger")], "Stays where he is.", "rt_t_bruch", ["bibi"]),
    WEITER_ZU("rt_t_riss_rein", K, "The Long Table", "Charly gets up. Nobody stops her. Nonna takes her plate away without a word.",
              [Z("charly", "This isn't your table.", "anger")], "Stays where he is.", "rt_t_bruch", ["charly"]),
    dict(FR("rt_t_bruch", K, "Something Broke",
            "Something broke at this table. This may have serious consequences for the story.", [],
            [O("Try again", [{"flags_weg": "rt_t_"}, WEITER("rt_tisch")]),
             O("Live with it", [F("rt_ausgang_getrennt"), F("rt_tisch_fertig"), WEITER("rt_white")])]), warnung=True),
]

ZUM_ABSCHIED = [{"wenn": {"flag": "kl_loewe_frei"}, "id": "rt_abschied_frei"}, {"id": "rt_abschied_erloest"}]


def NACH_TUER(lp):
    """Atempause vor dem letzten Kampf: versoehnt mehr als getrennt."""
    return [{"lp_anteil": lp}, KAMPF("rt_7b_tuer"), F("rt_white_agenten"),
            WEITER([{"wenn": {"flag": "rt_ausgang_alle"}, "id": "rt_ende_alle"}, {"id": "rt_ende_getrennt"}])]


EVENTS = [
    # ------------------------------------------------------------------ Ausflug 1: die Roten
    FR("rt_auftritt", "macchia_path", "The Red Trio",
       "A man in a bright red suit stands on a rock in the middle of the path, the sun behind him. He has clearly been standing "
       "there for a while. Two women in red come out of the bushes. They have already seen you.",
       [Z("danzel", "You there! You have something that belongs to me. Hand it over, and nobody gets – nobody gets very hurt.", "pride"),
        Z("bibi", "Ha ha ha ha! ...Sorry. I do that.", "nervousness"),
        Z("charly", "Three out of ten. He practised that in the car.", "neutral")],
       [O("Grips his weapon.", [F("rt_gestartet"), EXP, KAMPF("rt_1_bibi_charly"), WEITER(NACH_1)])],
       personen=["danzel", "bibi", "charly"]),
    FR("rt_flucht_ko", "macchia_path", "A Tactical Retreat",
       "The rock is empty. Somewhere up the path somebody in expensive shoes is running. Something small lies in the dust.",
       [Z("danzel", "This isn't over! This is a – tactical retreat!", "fear")],
       [O("Picks it up.", [BADGE, WEITER("rt_lager")])], personen=["danzel"]),
    FR("rt_flucht_geredet", "macchia_path", "A Tactical Retreat",
       "Bibi and Charly walk off up the path without looking back. On his rock, the man in red looks at them, at you, and "
       "climbs down very carefully. Something small lies in the dust where he stood.",
       [Z("danzel", "We were winning. I want that noted. This is a – tactical retreat!", "fear")],
       [O("Picks it up.", [BADGE, WEITER("rt_lager")])], personen=["danzel"]),
    FR("rt_lager", "creek_rest", "Someone Else's Fire",
       "After dark you smell smoke by the stream. Three people in red around a small fire. You stay behind the cork oak.",
       [Z("bibi", "Totò's cousin Gennaro isn't coming. And Elsa won't even look at us without proof.", "sadness"),
        Z("danzel", "Mr. White has counted the plates by now. We have days. Maybe.", "fear"),
        Z("bibi", "So what are we now? Three idiots in red suits?", "nervousness"),
        Z("charly", "We're the red team. A red team attacks its own company from the inside, to show where it's weak. We find proof. Together. That's the whole job.", "neutral"),
        Z("bibi", "You two can run if you have to. I'm staying until every one of them has that thing off its neck. I owe them that. And when Julien comes looking for them, I want to be the first thing he sees.", "pride"),
        Z("bibi", "With grenades! Ha ha! ...Sorry. I do that.", "nervousness")],
       [O("Follows them at first light.", GEFUNDEN + [WEITER("rt_bruecke")])], personen=["bibi", "charly", "danzel"]),
    FR("rt_bruecke", "macchia_creek_bridge", "The Bridge",
       "They are on the stone bridge when you come round the bend. All three heads turn. Nobody says anything this time. "
       "Bibi already has a grenade in her hand.",
       [], [O("Keeps walking.", [KAMPF("rt_3_trio"), WEITER(NACH_3)])], personen=["danzel", "bibi", "charly"]),
    FR("rt_bruecke_ko", "macchia_creek_bridge", "The Bridge",
       "They sit on the stones, getting their breath back. Danzel gets up last. He looks at your hands, then at your jacket.",
       [], [O("Waits.", [WEITER(PLATTE)])], personen=["danzel"]),
    FR("rt_bruecke_geredet", "macchia_creek_bridge", "The Bridge",
       "Nobody is hurt. That seems to confuse them more than anything else. Danzel puts the baton away on the third try, "
       "and looks at your jacket.",
       [], [O("Waits.", [WEITER(PLATTE)])], personen=["danzel"]),
    FR("rt_platte_truhe", "macchia_creek_bridge", "The Plate",
       "You tell him where the steel plate from the rock niche is. He laughs, once, and stops.",
       [Z("danzel", "Keep it. Elsa says a plate proves nothing. A plate is a plate.", "sadness"),
        Z("charly", "You found the note too. Four hundred or no deal? That one was mine. Nobody looks twice at a greedy man.", "neutral"),
        Z("bibi", "How do you know so much about it? You said you did something with armour.", "confusion")],
       [O("Says nothing.", [WEITER("rt_plan_rouge")])], personen=["danzel", "bibi"]),
    FR("rt_platte_verbaut", "macchia_creek_bridge", "The Plate",
       "He takes one step closer and stares at the lining of your jacket, where the steel plate from the rock niche now sits, as if it had said something about his mother.",
       [Z("danzel", "That's my plate. You put it on the wrong way round.", "surprise"),
        Z("charly", "You found the note too. Four hundred or no deal? That one was mine. Nobody looks twice at a greedy man.", "neutral"),
        Z("bibi", "Your plate?", "confusion")],
       [O("Says nothing.", [WEITER("rt_plan_rouge")])], personen=["danzel", "bibi"]),
    FR("rt_plan_rouge", "macchia_creek_bridge", "What Did You Do There?",
       "Bibi has stopped laughing. Charly looks at her shoes. Then a whistle comes from the ridge, and there are black suits "
       "between the trees.",
       [Z("bibi", "I told you everything. Every animal. Every name. What did you do at the lab?", "anger"),
        Z("danzel", "Plan Rouge! Shepherd's hut, tonight!", "fear")],
       [O("Watches them run in three directions. Only one of them looks back.", [F("rt_getrennt"), EXP_ENDE])],
       personen=["bibi", "danzel", "charly"]),
    # ------------------------------------------------------------------ Ausflug 2: drei Wege
    *[gabelung([PFADE[i][0] for i in range(3) if maske & (1 << i)]) for maske in range(1, 8)],
    FR("rt_drei_gefunden", "macchia_three_ways", "Three Ways",
       "Three sets of footprints, all going uphill now, towards the bells. You told them you'd find the others. You did.",
       [], [O("Heads back down for now.", [EXP_ENDE])]),
    FR("rt_koehlerweg", "charcoal_road", "The Charcoal Road",
       "Black trunks, grey ash, a pale track between old charcoal mounds. Something heavy is digging around up ahead.",
       [], [O("Keeps going.", [EXP, KAMPF("rt_4a_rotte"), WEITER("rt_koehler_2")])]),
    FR("rt_koehler_2", "charcoal_road", "The Charcoal Road",
       "Further on, a shape on the track. A ram, huge, and when it turns its head the sun flashes on steel.",
       [], [O("Doesn't stop.", [KAMPF("rt_4a_mufflon"), WEITER("rt_danzel")])]),
    FR("rt_danzel", "charcoal_hut", "Just Fine",
       "A stone hut, a small fire. Danzel sits on the bench with his jacket across his knees, sewing up the sleeve. His "
       "stitches are very small and very even. He doesn't look up. A folded letter sticks out of the lining.",
       [Z("danzel", "In Paris they said my work was fine. Just fine. Do you know what that word does to a person?", "sadness"),
        Z("danzel", "There was a mouflon back there, wasn't there. I heard it. That was my plate. On an animal.", "disgust"),
        Z("danzel", "That letter? My resignation. I wrote it the day I heard about the animals. Look, it even has the date. I never sent it.", "sadness")],
       [O("“Tell her yourself. Tonight.”", [F("rt_notiz_gesteht"), F("rt_danzel_fertig"), WEITER("rt_weg_danzel")],
          zeile=Z("danzel", "Tonight. Yes. Of course, tonight. ...Could it be tomorrow? No. Tonight.", "fear")),
        O("Takes the letter. “Nobody has to know what you built.”", [F("rt_notiz_kuendigung"), F("rt_duc_mitwisser"), F("rt_danzel_fertig"), WEITER("rt_weg_danzel")],
          zeile=Z("danzel", "Oh. That's – yes. Thank you. Thank you. Why does that feel worse?", "nervousness"))],
       personen=["danzel"]),
    FR("rt_weg_danzel", "charcoal_hut", "Just Fine",
       "You point up the slope. “Follow the bells up to the old monastery. Tell Nonna Fiora I sent you. I'll find the others.” Far above the burnt trees, right on time, a bell rings.",
       [Z("danzel", "Nonna. Is she dangerous?", "fear")], [O("Turns back.", [WEITER(zur_gabel())])], personen=["danzel"]),
    FR("rt_knochenschlucht", "bone_gorge", "The Gorge",
       "The walls come in close. Old scratches in the rock, a goat's skull on the stones. Something moves along the ledge above.",
       [], [O("Keeps going.", [EXP, KAMPF("rt_4b_affen"), WEITER("rt_schlucht_2")])]),
    FR("rt_schlucht_2", "bone_gorge", "The Gorge",
       "Laughter, somewhere ahead. Not a person's. Three small red lights in the shade, blinking in time.",
       [], [O("Doesn't stop.", [KAMPF("rt_4b_hyaenen"), WEITER([{"wenn": {"flag": "kl_loewe_frei"}, "id": "rt_bibi_frei"}, {"id": "rt_bibi_erloest"}])])]),
    FR("rt_bibi_frei", "lion_den_cave", "This Big",
       "Bibi stands at the mouth of the cave. She has been following tracks for days, and here they stop. She has a bowl in one hand and a notebook in the other.",
       [Z("bibi", "You met them, back in the gorge. Pip. Nougat. Little Bear. They had numbers, so I named them.", "sadness"),
        Z("bibi", "This one is Mochi. Every meal he ever ate is in here. Every scar. I wrote it all down. That was my job.", "sadness"),
        Z("bibi", "He was this big when I got him. He bit my thumb and then he fell asleep on it. You've been up here. Did you see a black lion?", "fear")],
       [O("Tells her. He cut the chip out, and the lion walked away.", [F("rt_notiz_wahrheit"), F("rt_duc_ehrlich"), F("rt_bibi_fertig"), WEITER("rt_weg_bibi")],
          zeile=Z("bibi", "He walked? On all four? His back left leg was always slow in the morning. ...He walked.", "gratitude")),
        O("Says nothing. Holds her notebook when she needs both hands, and helps her look.", [F("rt_notiz_futter"), F("rt_bibi_fertig"), WEITER("rt_weg_bibi_buch")],
          zeile=Z("bibi", "You don't have to stay. ...You can stay.", "sadness"))],
       personen=["bibi"]),
    FR("rt_bibi_erloest", "lion_den_cave", "This Big",
       "Bibi stands at the mouth of the cave. She has been following tracks for days, and here they stop. She has a bowl in one hand and a notebook in the other.",
       [Z("bibi", "You met them, back in the gorge. Pip. Nougat. Little Bear. They had numbers, so I named them.", "sadness"),
        Z("bibi", "This one is Mochi. Every meal he ever ate is in here. Every scar. I wrote it all down. That was my job.", "sadness"),
        Z("bibi", "He was this big when I got him. He bit my thumb and then he fell asleep on it. You've been up here. Did you see a black lion?", "fear")],
       [O("Tells her. It was quick, and he didn't try to get up.", [F("rt_notiz_wahrheit"), F("rt_duc_ehrlich"), F("rt_bibi_fertig"), WEITER("rt_weg_bibi")],
          zeile=Z("bibi", "Quick. Okay. Okay, quick, that's – ha. Ha ha. ...Sorry. I do that.", "sadness")),
        O("Says nothing. Holds her notebook when she needs both hands, and helps her look.", [F("rt_notiz_futter"), F("rt_bibi_fertig"), WEITER("rt_weg_bibi_buch")],
          zeile=Z("bibi", "You don't have to stay. ...You can stay.", "sadness"))],
       personen=["bibi"]),
    FR("rt_weg_bibi", "lion_den_cave", "This Big",
       "You point up the slope. “Follow the bells up to the old monastery. Tell Nonna Fiora I sent you. I'll find the others.” A long way off, a bell rings.",
       [Z("bibi", "Bells. Okay. Bells, I can do bells.", "nervousness")], [O("Turns back.", [WEITER(zur_gabel())])], personen=["bibi"]),
    FR("rt_weg_bibi_buch", "lion_den_cave", "This Big",
       "You look until the light goes, and there is nothing. You point up the slope. “Follow the bells up to the old monastery. Tell Nonna Fiora I sent you. I'll find the others.” A long way off, a bell rings. "
       "She goes fast, the bowl under her arm. Only then do you see that her notebook is still in your hand.",
       [Z("bibi", "Bells. Okay. Bells, I can do bells.", "nervousness")], [O("Turns back.", [WEITER(zur_gabel())])], personen=["bibi"]),
    FR("rt_mastgrat", "antenna_ridge", "The Ridge",
       "A bare ridge, a rusty mast, the sea a long way down. Two men in black are walking the path ahead of you.",
       [], [O("Keeps going.", [EXP, KAMPF("rt_4c_agenten"), WEITER("rt_mast_2")])]),
    FR("rt_mast_2", "antenna_ridge", "The Ridge",
       "A thin whine comes down from above. One small red light. Blink, blink, pause.",
       [], [O("Doesn't stop.", [KAMPF("rt_4c_drohne"), WEITER("rt_charly")])]),
    FR("rt_charly", "antenna_ridge", "Six out of Ten",
       "Charly sits against the mast with her phone. It buzzes. Maman. She declines it. On the screen behind the call, something "
       "small is moving: three little figures in red suits, running and jumping. The phone buzzes again, and this time she lets "
       "the message play. A woman's voice, very calm: “Charlotte. Alon says you asked to leave the collar project in March. We do not leave things. Call me.”",
       [Z("charly", "Six out of ten. For the signal.", "neutral"),
        Z("charly", "Blink, blink, pause. That's my loop. I wrote that on a Tuesday.", "sadness"),
        Z("charly", "The little ones? It's nothing. It's a game. I make it at night. That's Danzel. That's Bibi. That's me, the one who falls down.", "embarrassment"),
        Z("charly", "So now you know about March too. It changed nothing.", "sadness")],
       [O("“Go home. You can afford to.”", [F("rt_notiz_mutter"), F("rt_charly_fertig"), WEITER("rt_weg_charly")],
          zeile=Z("charly", "Correct. Three out of ten.", "sadness")),
        O("“Show them this. Show them who you really are.”", [F("rt_notiz_spiel"), F("rt_charly_fertig"), WEITER("rt_weg_charly")],
          zeile=Z("charly", "It isn't finished. The jump is bad. ...No number yet.", "embarrassment"))],
       personen=["charly"]),
    FR("rt_weg_charly", "antenna_ridge", "Six out of Ten",
       "You point up the slope. “If you're staying, follow the bells up to the old monastery. Tell Nonna Fiora I sent you.” A long way off, a bell rings. She doesn't get up straight away. Then she does.",
       [Z("charly", "Bells. Two out of ten for the technology.", "neutral")], [O("Turns back.", [WEITER(zur_gabel())])], personen=["charly"]),
    # ------------------------------------------------------------------ Ausflug 3: der Tisch und Mr. White
    FR("rt_ankunft", "monastery_garden_dusk", "Three More Plates",
       "They come up the path one at a time and sit as far apart as the garden allows. Nonna looks at them, then at you, and goes in for three more plates.",
       [Z("nonna", "Sit. Questions after soup.", "caring")],
       [O("Goes in after her.", [EXP, WEITER("rt_tisch")])], personen=["nonna"]),
    *TISCH,
    FR("rt_white", "monastery_garden_dusk", "Mr. White",
       "Night. A man in a white suit stands in the garden with his hands behind his back, looking at the rosemary. There are people on the wall behind him.",
       [Z("mrwhite", "Danzel. Lovely stitching. Bibi, your lion sends his regards. Charlotte – your mother is worried.", "neutral"),
        Z("mrwhite", "A consultant. How nice. Tidy up.", "neutral"),
        Z("danzel", "If you want them, you go through me. Which – which won't take long, but still.", "anger")],
       [O("Stands next to him.", [EXP, KAMPF("rt_7a_garten"),
                                  WEITER([{"wenn": {"flag": "rt_ausgang_alle"}, "id": "rt_white_2_alle"}, {"id": "rt_white_2"}])])],
       personen=["mrwhite", "danzel"]),
    FR("rt_white_2_alle", "monastery_garden_dusk", "Nonna's Door",
       "The man in white has gone, without hurrying. There are more of them, and something whining in the air above the well. Bibi has your arm before you see her coming, and she ties it up fast. Her hands aren't shaking now.",
       [Z("bibi", "Hold still. Two seconds. There. Go.", "neutral")],
       [O("Doesn't move from the door.", NACH_TUER(0.45))], personen=["bibi"]),
    FR("rt_white_2", "monastery_garden_dusk", "Nonna's Door",
       "The man in white has gone, without hurrying. There are more of them, and something whining in the air above the well. Behind you the door opens a hand's width. A wet cloth comes through it, and the door closes again.",
       [], [O("Doesn't move from the door.", NACH_TUER(0.2))]),
    FR("rt_ende_alle", "monastery_garden_dusk", "A Prototype",
       "Morning. Three of them on the wall with Nonna's coffee, and nobody sitting apart. Elsa came up at first light because of the noise, and she left with three signed statements. Danzel comes over with something folded across his arm.",
       [Z("danzel", "It's a prototype. I made it for myself, you know. I was going to wear it when I finally had something to celebrate. ...I think this is it. Here. Thank you for everything.", "gratitude")],
       [O("Puts it on.", [F("jacke_jacket_fire"), F("red_trio_fertig"), F("ark_aussagen_3"), {"flag_datiert": "rt_ende_tag"}, WEITER("rt_kragen")])],
       personen=["danzel"], ton="wholesome"),
    FR("rt_ende_getrennt", "monastery_garden_dusk", "A Prototype",
       "Morning. The garden is quiet. Elsa came up at first light because of the noise, and she left with one signed statement. Nobody else would sit down with her. Danzel holds something folded across his arm and doesn't quite look at you.",
       [Z("danzel", "It's a prototype. I was going to wear it myself. Here. Thank you for everything.", "sadness"),
        Z("danzel", "Bibi is going to a zoo in France. Charly's family sent a car. I can't go anywhere, so I'm staying.", "sadness"),
        Z("danzel", "There's an empty room on the piazza with a good window. I'm going to open a shop there, Le Théâtre Rouge. Charly would give the name a three. Come by in a few days, if you want.", "neutral")],
       [O("Takes it, and doesn't know what to say.", [F("jacke_jacket_fire"), F("red_trio_fertig"), F("ark_aussagen_1"), F("rt_bibi_weg"), F("rt_charly_weg"), {"flag_datiert": "rt_ende_tag"}, WEITER("rt_kragen")])],
       personen=["danzel"]),
    FR("rt_kragen", "monastery_garden_dusk", "Incendio",
       "Burgundy, hand-cut, and it fits as if he had measured you in your sleep. There is a note in the collar, in careful pencil: "
       "For the man who found us. Plate on the right way round. It likes a fire: the hotter they burn, the harder you hit. Thank you. – D.",
       [], [O("Folds the note into the lining.", [WEITER([{"wenn": {"flag": "rt_ausgang_alle"}, "id": "rt_was_nun"}] + ZUM_ABSCHIED)])]),
    # Was wird aus den dreien (Duc 30.10.2026): Danzel entscheidet selbst, Charly fragt Duc, Bibi braucht Ducs Idee
    FR("rt_was_nun", "monastery_garden_dusk", "What Now",
       "Nonna has put out more coffee and nobody has touched it. Nobody is chasing anybody now, and there is a lot of morning left.",
       [Z("nonna", "You can't sleep in my garden for ever. So what are you going to do with yourselves?", "caring"),
        Z("danzel", "There's an empty room on the piazza. It has a good window. I went and looked at it, I don't know why I went and looked at it.", "nervousness"),
        Z("danzel", "I'm going to open a shop. With clothes, real ones, for people. I've spent long enough drawing hinges. It's called Le Théâtre Rouge.", "pride"),
        Z("charly", "Three out of ten.", "neutral"),
        Z("danzel", "For the shop or for the name?", "nervousness"),
        Z("charly", "The name.", "neutral")],
       [O("Drinks his coffee.", [WEITER("rt_wn_charly")])], personen=["nonna", "danzel", "charly"], ton="wholesome"),
    FR("rt_wn_charly", "monastery_garden_dusk", "One Question",
       "Charly waits until the others are arguing about curtains. She comes over with her crisps and looks at the wall instead of at you.",
       [Z("charly", "There's a car waiting for me in Bastia. It's been there all week.", "neutral"),
        Z("charly", "You've got a yacht full of old wiring and a very angry engineer. Do you need a techie? I'm only asking once.", "neutral")],
       [O("Holds out his empty hand. “Yes. Rosi will hate you.”", [F("rt_charly_bleibt"), V("charly", 4), WEITER("rt_wn_charly_ja")]),
        O("Shakes his head. “Go home, Charly.”", [F("rt_charly_weg"), WEITER("rt_wn_charly_nein")])], personen=["charly"]),
    WEITER_ZU("rt_wn_charly_ja", "monastery_garden_dusk", "One Question", "She looks at your empty hand for a moment. Then she puts a crisp in it.",
              [Z("charly", "Seven out of ten. Tell her I'll bring my own tools.", "joy")], "Eats it.", "rt_wn_bibi", ["charly"], ton="wholesome"),
    WEITER_ZU("rt_wn_charly_nein", "monastery_garden_dusk", "One Question", "She nods, as if she had already worked it out. The crisp packet goes into her jacket, folded very small.",
              [Z("charly", "Okay. It was a fair answer. Four out of ten.", "sadness")], "Watches her go to tell them.", "rt_wn_bibi", ["charly"]),
    FR("rt_wn_bibi", "monastery_garden_dusk", "A Bowl",
       "Bibi is the last one left at the table. She has turned her bowl upside down and she is drumming on it.",
       [Z("bibi", "So he's got a shop! That's great, everybody's got a thing now, that's really – ha! Ha ha! ...Sorry. I do that.", "nervousness"),
        Z("bibi", "I said I'd stay, you know. At the fire. That was when I still thought I was one of the good ones.", "sadness"),
        Z("bibi", "I could go. I could finally go, you know, the zoos and all of it, that was the plan before I stayed for a man. I just don't know what I'm for any more.", "sadness")],
       [O("Looks up at the macchia. “You said until every collar was off. I heard you at the fire.”",
          [F("rt_bibi_bleibt"), F("mochis_offen"), V("bibi", 4), WEITER("rt_wn_bibi_ja")]),
        O("Nods. “You always wanted to see the world. Go and see it.”", [F("rt_bibi_weg"), V("bibi", 2), WEITER("rt_wn_bibi_nein")])], personen=["bibi"]),
    WEITER_ZU("rt_wn_bibi_ja", "monastery_garden_dusk", "A Bowl", "She stops drumming and turns the bowl the right way up.",
              [Z("bibi", "You were listening? From behind a tree? That's really creepy, Clipboard.", "surprise"),
               Z("bibi", "Me? With what? I haven't got a fence, I haven't got any feed, I've got – I've got a bowl.", "surprise"),
               Z("bibi", "...I've got a bowl.", "gratitude")], "Leaves her to it.", ZUM_ABSCHIED, ["bibi"], ton="wholesome"),
    WEITER_ZU("rt_wn_bibi_nein", "monastery_garden_dusk", "A Bowl", "She breathes out and nods a few times, very fast.",
              [Z("bibi", "I said I'd stay. I say a lot of things.", "sadness"),
               Z("bibi", "Yeah. Yeah, okay! I'm going. I'll send you a postcard, and it'll have a giraffe on it.", "gratitude")], "Leaves her to it.", ZUM_ABSCHIED, ["bibi"], ton="wholesome"),
    FR("rt_abschied_frei", "monastery_garden_dusk", "Somewhere in the Macchia",
       "Bibi stops at the gate on her way past, her bowl under her arm.",
       [Z("bibi", "You let him go. He's out there now, somewhere in the macchia, lying in the sun with nobody telling him what to do. I bet he has a lovely life. Thank you, Duc. Really.", "gratitude")],
       [O("Walks down.", [EXP_ENDE])], personen=["bibi"]),
    FR("rt_abschied_erloest", "monastery_garden_dusk", "His Bowl",
       "Bibi stops at the gate on her way past, her bowl under her arm.",
       [Z("bibi", "I still put out his bowl in the mornings. Isn't that stupid? He was this big when I got him, and now there's nothing left to feed. I keep waiting to hear him snore.", "sadness")],
       [O("Walks down.", [EXP_ENDE])], personen=["bibi"]),
]

# ------------------------------------------------------------------ Folgen: Tierstation Mochi's, Laden, Elsa, Postkarten (Wiki: nebenquest_red_trio.md)
FOLGE_TAGE = (11, 21)
SB = dict(S, alva="alva_standard", petru="Standard", lola="Galley", jana="jana_deck_a")


def FOLGE(id, ton, titel, seit, phase, bed, bild, wer, lage, zeilen, optionen, tage=FOLGE_TAGE):
    """Pflicht-Event an einem der Tage nach der Quest: seit = (datiertes Flag, Tage)."""
    bedingung = {"alle": [{"flag_seit": list(seit)}] + bed}
    pers = {"handelnd": wer[0], "betroffen": [{"id": b, "ton": "?", "was": ""} for b in wer[1:]]} if wer else {}
    sets = {p: SB[p] for p in wer}
    if "bibi" in sets and {"flag": "mochis_offen"} in bed:    # sie ist geblieben und leitet die Station (Duc 01.11.2026)
        sets["bibi"] = "Mochis"
    e = E(id, "gag1", ton, titel, WANN(tage, [phase], bed=bedingung, pflicht=True, holt_leute=True), bild, pers, lage,
          zeilen, optionen, sets)
    if len(wer) == 1:                                 # allein mit Duc: niemand sonst auf der Buehne
        e["solo"] = True
    return e


def JE_STUFE(id, pid, ton, titel, seit, phase, bed, bild, lage, vor, satz, nach, optionen, wer):
    """Folge-Event mit einem Satz je Vertrauensstufe (1, 2, ab 3). Einmal gesehen, nie wieder."""
    out = []
    for stufe, wert, gefuehl in ((3, [">=", 3], "gratitude"), (2, ["==", 2], "neutral"), (1, ["<=", 1], "sadness")):
        out.append(FOLGE("%s_%d" % (id, stufe), ton, titel, seit, phase,
                         [{"flag": bed}, {"nicht": {"flag": id + "_gesehen"}}, {"wert": ["vertrauen." + pid] + wert}],
                         bild, wer, lage, vor + [Z(pid, satz[stufe], gefuehl)] + nach,
                         [O(t, f + [F(id + "_gesehen")], **k) for t, f, k in optionen]))
    return out


SEIT_ENDE = lambda n: ("rt_ende_tag", n)
for _id, _name, _text in (
        ("postcard_bibi", "Postcard from a Zoo", "Giraffes and a French stamp, in big fast handwriting: “I finally went. They have a lion who snores. I'm okay. I think.” No address to write back to."),
        ("postcard_charly", "Postcard from Paris", "No sender, postmarked Paris, a very ugly statue on the front. On the back there is only “2/10”. You can't tell if she means the statue.")):
    item(_id, _name, "quest", text=_text)


def KARTE(id, seit, bed, titel, lage, zeile, iid):
    return FOLGE(id, "ernst", titel, SEIT_ENDE(seit), "fruehstueck", [{"flag": bed}], "crew_mess", ["lola", "jana"], lage,
                 [Z("lola", zeile, "curiosity")],
                 [O("Puts it in his jacket.", [I(iid)]), O("Reads it twice, then puts it in his jacket.", [I(iid)])])


FOLGE_EVENTS = [
    FOLGE("rt_elsa_drei", "ernst", "Three Signatures", ("rt_ende_tag", 1), "tag", [{"flag": "ark_aussagen_3"}], "village_harbour", ["elsa", "petru"],
          "Elsa is on the quay with a folder under her arm, and she has put a paperweight on it, although there is no wind. Petru mends a net a little way off and hears nothing, as usual.",
          [Z("elsa", "Three signed statements from Danzel, Bibi and Charly, with names and dates. In five years nobody has given me anything this good, First Officer.", "approval"),
           Z("elsa", "I sent the copies up to the town hall this morning, with the stamp, the way it's supposed to go. Now we wait.", "neutral")],
          [O("Nods. “Now we wait.”", [V("elsa", 4)]),
           O("“Who reads it at the town hall?”", [V("elsa", 2)],
             zeile=Z("elsa", "The deputy mayor. He deals with all of that for me. It's the one thing that works in this village.", "neutral"))]),
    FOLGE("rt_elsa_eine", "ernst", "One Signature", ("rt_ende_tag", 1), "tag", [{"flag": "ark_aussagen_1"}], "village_harbour", ["elsa", "petru"],
          "Elsa is on the quay with a very thin folder. Petru mends a net a little way off and hears nothing, as usual.",
          [Z("elsa", "One statement. One is a complaint, First Officer, it isn't a case. What happened up at Nonna Fiora's table?", "disappointment"),
           Z("elsa", "I sent it up to the town hall anyway, with the stamp, the way it's supposed to go. Somebody should read it.", "neutral")],
          [O("“They couldn't sit at the same table.”", [V("elsa", 2)]),
           O("Just shakes his head.", [],
             zeile=Z("elsa", "No. Well. Somebody signed, that's already more than I usually get.", "neutral"))]),
    *[FOLGE("rt_mochis_auf" + nachsatz, "wholesome", "Mochi's", SEIT_ENDE(1), "abend", [{"flag": "mochis_offen"}, {"flag": charly}], "mochis", wer,
            "Above the bay there is an old sheep pen with half a roof, and Bibi has taken it for the animals from the lab. A new sign hangs on the gate, black letters, very neat. Two fishermen have come up to look "
            "at it, and they've sent someone down to tell the others. There is a bowl of water on the ground, for animals that aren't here yet.",
            zeilen,
            [O("Pays for a month of feed.", [{"geld": -30}, W("ruf", 2)]),
             O("Takes a shovel and stays until a dog comes to the bowl.", [W("ruf", 1)])])
      for nachsatz, charly, wer, zeilen in (
          ("", "rt_charly_bleibt", ["bibi", "danzel", "charly"],
           [Z("danzel", "I offered her a proper name. I had a logo, I had a whole concept with curtains.", "pride"),
            Z("charly", "Three out of ten.", "neutral"),
            Z("bibi", "It's called Mochi's.", "caring"),
            Z("danzel", "...It's called Mochi's.", "gratitude"),
            Z("charly", "Nine.", "joy"),
            Z("bibi", "You've never given a nine. Not even to me!", "surprise")]),
          ("_ohne", "rt_charly_weg", ["bibi", "danzel"],
           [Z("danzel", "I offered her a proper name. I had a logo, I had a whole concept with curtains.", "pride"),
            Z("bibi", "It's called Mochi's.", "caring"),
            Z("danzel", "...It's called Mochi's.", "gratitude"),
            Z("bibi", "Charly would have given it a three. I'd have liked to hear that, actually.", "sadness")]))],
    *JE_STUFE("rt_danzel_mass", "danzel", "wholesome", "A Proper Fitting", SEIT_ENDE(2), "tag", "rt_ausgang_alle", "village_piazza",
              "The room on the piazza, Danzel's new shop, still smells of old paint, and it has nothing in it yet but a good window. Danzel has a tape measure round his neck and pins in his mouth. He takes them out to talk, and that is the only time he stops working. Two fishermen pretend not to watch from the door.",
              [], {3: "I'm making you a second jacket. The first, the burgundy one, was only a prototype.",
                   2: "Arms up. You've been carrying something on the left, the seam has moved. It's fine, I can let it out.",
                   1: "The jacket fits you. I checked. From over here."},
              [Z("danzel", "And you two can stop staring. Yes, I do waistcoats. No, not for fish money.", "pride")],
              [("Holds his arms out and lets him work.", [V("danzel", 4), W("ruf", 1)], {}),
               ("Orders a waistcoat for Petru and pays for it.", [{"geld": -20}, V("danzel", 2), W("ruf", 2)], {})], ["danzel"]),
    *JE_STUFE("rt_charly_spiel", "charly", "wholesome", "Game Night", SEIT_ENDE(3), "abend", "rt_charly_bleibt", "village_harbour",
              "Charly has run a cable from her phone to an old television on a fish crate, and the game she makes at night is on it. Half the harbour is shouting at a very small man in a red suit. Petru isn't shouting, but he hasn't gone home either.",
              [Z("danzel", "It's me! Look, I'm winning, I'm running away!", "joy")],
              {3: "Eight out of ten. For you. Don't tell anyone.",
               2: "Six out of ten. You jump like Danzel.",
               1: "Four out of ten. For you. You know why."},
              [], [("Takes the controller and loses to a fisherman.", [V("charly", 4), W("ruf", 1)], {}),
                   ("Sits on a crate and bets on Petru.", [V("charly", 2), W("ruf", 1)], {})], ["charly", "danzel"]),
    *JE_STUFE("rt_bibi_frischlinge", "bibi", "wholesome", "Four Striped Piglets", SEIT_ENDE(4), "tag", "mochis_offen", "mochis",
              "Early at Mochi's, Bibi's old sheep pen. Four striped piglets are following Bibi along the wall in a very straight line, and one of them keeps falling over. The bowl finally has customers.",
              [], {3: "You're the only one who asked me how I was. Sit. There's coffee.",
                   2: "Hold this one. She bites, but only people she likes.",
                   1: "Feed's in the sack. ...No, I'm fine. Feed's in the sack."},
              [Z("bibi", "They came down off the burnt road by themselves. Nobody has a lab number on them. I checked.", "caring")],
              [("Sits down in the dirt and lets a piglet climb his boot.", [V("bibi", 4), W("ruf", 1)], {}),
               ("Carries the slow one back to the bowl.", [V("bibi", 2), W("ruf", 1)], {})], ["bibi"]),
    # Ernste Abende an der Station und der Vorbote der Belagerung
    FOLGE("rt_napf_frei", "ernst", "The Empty Bowl", SEIT_ENDE(5), "abend", [{"flag": "mochis_offen"}, {"flag": "kl_loewe_frei"}], "mochis", ["bibi"],
          "Closing time at the pen. Bibi tips out the bowl, rinses it and fills it again, although nothing has drunk from it since noon.",
          [Z("bibi", "Mochi, my lion, was a hundred and ninety kilos, the last time I weighed him. He had a bad tooth on the left side and he only let me near it.", "caring"),
           Z("bibi", "Who's looking at that tooth now? Nobody. That's what you gave him, nobody looking at his teeth. It's a good thing. I keep telling myself it's a good thing.", "sadness")],
          [O("Holds the bowl while she fills it.", [V("bibi", 4)]),
           O("“Tell me about the tooth.”", [V("bibi", 4)])]),
    FOLGE("rt_napf_erloest", "ernst", "The Empty Bowl", SEIT_ENDE(5), "abend", [{"flag": "mochis_offen"}, {"flag": "kl_loewe_erloest"}], "mochis", ["bibi"],
          "Closing time at the pen. Bibi tips out the bowl, rinses it and fills it again, although nothing has drunk from it since noon.",
          [Z("bibi", "Mochi, my lion, was a hundred and ninety kilos, the last time I weighed him. He had a bad tooth on the left side and he only let me near it.", "sadness"),
           Z("bibi", "You don't have to say anything. You're just the only one left who saw him, so I'm telling you.", "sadness")],
          [O("Holds the bowl while she fills it.", [V("bibi", 4)]),
           O("Says nothing and stays until it's dark.", [V("bibi", 2)])]),
    FOLGE("rt_pfote", "ernst", "Paw Print", SEIT_ENDE(6), "tag", [{"flag": "mochis_offen"}, {"flag": "kl_loewe_frei"}], "mochis", ["bibi"],
          "Bibi rang early and wouldn't say why. Next to the bowl she keeps filling for her lion Mochi, pressed deep into the wet ground, there is a paw print wider than your hand. The bowl is empty.",
          [Z("bibi", "It could be a dog.", "curiosity")],
          [O("Crouches and lays his hand in it. “Big dog.”", [F("rt_pfote_gesehen"), V("bibi", 4)]),
           O("Says nothing. Neither does she.", [F("rt_pfote_gesehen"), V("bibi", 4)])]),
    FOLGE("rt_bon", "ernst", "Paid in Full", SEIT_ENDE(1), "tag", [{"flag": "red_trio_fertig"}], "village_piazza", ["danzel"],
          "The cash register is the one thing in Danzel's shop that works properly. This morning it has printed a receipt for a suit nobody ordered: white linen, one fitting, paid in full. "
          "Across the bottom someone has written, in very good handwriting: Lovely stitching.",
          [Z("danzel", "White linen. “Lovely stitching.” That's what the man in white said to me in Nonna's garden. I have never in my life – who has been in my shop?", "fear")],
          [O("Takes the receipt to Elsa.", [F("rt_bon_gesehen"), V("elsa", 2), V("danzel", 2)]),
           O("Folds it into his pocket. “Close early tonight.”", [F("rt_bon_gesehen"), V("danzel", 4)])], tage=(19, 20)),
    KARTE("rt_karte_bibi", 3, "rt_bibi_weg", "A Postcard", "There is a postcard next to your plate. Someone brought it up from the village. Giraffes, a French stamp and very fast handwriting. It must be from Bibi, the woman in red who looked after the lion.", "This came up from the village for you, mate. I didn't read it. Well, I read the front. Who do you know in a zoo?", "postcard_bibi"),
    KARTE("rt_karte_charly", 5, "rt_charly_weg", "A Postcard", "A postcard, propped against your cup. It has no sender, and the statue on the front is very ugly. On the back it only says “2/10”, the way Charly rates everything.", "This one's from Paris, mate. I'm not saying I looked. I looked. Who sends a statue that ugly?", "postcard_charly"),
]
EVENTS += FOLGE_EVENTS
