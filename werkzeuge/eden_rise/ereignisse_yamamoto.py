# -*- coding: utf-8 -*-
"""Yamamoto, Jana und Maxwell (Duc 24.10.2026): sieben Events 'Yamamoto spannt' (Running Gag mit Stufen, Maxwell erwischt
ihn) und drei Events 'Training mit Maxwell' (06:30, Aft Deck).

Alle drei sind erwachsen; die Gags leben von Fremdschaemen und Slapstick, nicht von Nacktheit. Jana bekommt nie Begehren
(Engine: Begehren nur fuer die Frauen der Crew, Lola und Alva), nur Vertrauen.
Ketten: Jede Option jedes Kettenglieds setzt den Gag (auch beide Zweige einer Probe), die Folge-Events warten auf das
Flag gag_<id>_<stufe> des Vorgaengers. Die Engine waehlt zufaellig - die Kette kann also in sieben Tagen unvollstaendig bleiben."""
from ereignisse_basis import *  # noqa: F401,F403


def P1(handelnd, *betroffen):
    return {"handelnd": handelnd, "betroffen": [{"id": b[0], "ton": b[1], "was": b[2]} for b in betroffen]}


YK = "yamamoto_kamera"
MT = "maxwell_training"
Y_HAWAII, Y_BADE, Y_PARTY = "yamamoto_hawaii_b", "yamamoto_badeanzug_b", "yamamoto_party_b"
M_STEWARD, M_TRAIN = "maximum_steward_a", "maximum_training_b"
J_DECK, J_BIKINI = "jana_deck_a", "jana_bikini_a"


def nach(gag, stufe):
    return {"flag": "gag_%s_%d" % (gag, stufe)}


EVENTS = [
    # ------------------------------------------------------------------ Yamamoto spannt (7)
    E("yk_vogel", "gag1", "witzig", "The Rare Bird", WANN((2, 3), ["tag"]), "swim_platform",
      P1("yamamoto", ("jana", "?", "sunbathes and suspects nothing"), ("maxwell", "?", "isn't here yet")),
      "Jana is wringing out lines on the swim platform in her red-white-red bikini, the tip of her tongue between "
      "her teeth. Two decks up, Yamamoto-san is hanging over the railing with a camera whose lens is as long as a "
      "forearm. He has binoculars and a notebook too, and he's being very busy.",
      [Z("yamamoto", "Officer-san. Shhh. A very rare bird. Only visible at the swim platform. Between ten and noon.", "curiosity"),
       Z("jana", "Sir! Hi! Sorry, am I in the way? I'm only doing the lines. Jessas, the water is cold.", "nervousness")],
      [O("Asks Yamamoto what kind of bird it is.", [V("yamamoto", 4), GAG(YK)],
         zeile=Z("yamamoto", "Latin name: Avis kitsune. Very shy. Very red and white. So sorry, I cannot say more.", "embarrassment")),
       O("Brings Jana a jumper.", [V("jana", 4), V("yamamoto", -2), GAG(YK)]),
       O("Watches quietly to see what happens.", [W("moral", 1), GAG(YK)])],
      gag=YK, sets={"yamamoto": Y_HAWAII, "jana": J_BIKINI}),

    E("yk_schatten", "gag1", "witzig", "Maxwell's Shadow", WANN((2, 4), ["tag"], bed=nach(YK, 1)), "sun_deck",
      P1("maxwell", ("yamamoto", "-", "freezes mid-click"), ("jana", "+", "waves from below")),
      "Yamamoto is lying on the sun deck, just about to take a picture. Suddenly it goes dark. Behind him stands "
      "Maxwell, two metres wide, arms folded, casting a shadow like a wardrobe.",
      [Z("maxwell", "Mr. Maximum sees a rare bird too. The bird is on the camera's side of the lens. Mr. Maximum has a question.", "approval"),
       Z("yamamoto", "So sorry. The bird is gone now. Very fast bird.", "fear")],
      [O("Lets Maxwell handle it.", [V("maxwell", 4), V("yamamoto", -2), GAG(YK)]),
       O("Covers for Yamamoto: “He's photographing clouds.”", [], probe=P("cunning", 12),
         erfolg=[V("yamamoto", 6), V("maxwell", 2), GAG(YK)], fehlschlag=[V("maxwell", 2), V("yamamoto", 2), GAG(YK)],
         zeile=Z("yamamoto", "Yes. Clouds. Beautiful clouds. Very low clouds. Very red clouds.", "embarrassment")),
       O("Invites them both for an iced tea.", [W("moral", 1), V("maxwell", 2), V("yamamoto", 2), GAG(YK)])],
      gag=YK, sets={"yamamoto": Y_HAWAII, "maxwell": M_STEWARD}),

    E("yk_falle", "gag1", "witzig", "Maxwell's Trap", WANN((3, 5), ["tag"], bed=nach(YK, 3)), "swim_platform",
      P1("maxwell", ("yamamoto", "-", "walks into the trap"), ("jana", "?", "knows nothing")),
      "On the swim platform, Maxwell has dressed a dummy made of towels in a red-white-red bikini and tied it to a "
      "deckchair with a line. He's hiding behind the fenders and waving you over. Two decks up, the clicking starts.",
      [Z("maxwell", "Number One, Mr. Maximum has a plan. The towel is the bait. The bird always comes back.", "pride"),
       Z("yamamoto", "Ah. Beautiful. Very still bird. Finally, a bird that does not fly away.", "joy")],
      [O("Stays quiet and lets the trap work.", [V("maxwell", 6), V("yamamoto", -4), GAG(YK)]),
       O("Warns Yamamoto.", [V("yamamoto", 6), V("maxwell", -4), GAG(YK)]),
       O("Fetches Jana so she can see the dummy.", [], probe=P("empathy", 12),
         erfolg=[V("jana", 4), V("maxwell", 2), GAG(YK)], fehlschlag=[V("jana", -2), GAG(YK)],
         zeile=Z("jana", "Sorry, why am I made of towels? Is it a surprise? Jessas, it's a good bikini.", "confusion"))],
      gag=YK, sets={"maxwell": M_STEWARD, "yamamoto": Y_HAWAII, "jana": J_DECK}),

    E("yk_jana_merkt", "gag1", "frech", "Jana Plays Along", WANN((4, 6), ["tag"], bed=nach(YK, 4)), "swim_platform",
      P1("jana", ("yamamoto", "-", "goes red to the ears"), ("maxwell", "?", "is on his way")),
      "Jana has finally worked out what's clicking up there. She goes red and waves up anyway. Then she strikes a "
      "pose, too loud and a step too far. Yamamoto bows so deeply that the camera slips out of his hands and sails "
      "towards the water.",
      [Z("jana", "Hallo, Yamamoto-san! Sorry! I'm the bird! Servus! Is this the good side? Jessas, this is so embarrassing.", "embarrassment"),
       Z("yamamoto", "So sorry, so sorry. The bird is very beautiful. The camera is very wet.", "surprise")],
      [O("Fishes the camera out of the water.", [], probe=P("courage", 12),
         erfolg=[V("yamamoto", 6), V("jana", 2), GAG(YK)], fehlschlag=[V("yamamoto", 2), W("moral", 1), GAG(YK)]),
       O("Praises Jana: “That was brave.”", [V("jana", 6), V("yamamoto", -2), GAG(YK)],
         zeile=Z("jana", "I was brave? Sorry. I mean, thank you. I didn't know I could be brave in a bikini.", "pride")),
       O("Hands Yamamoto a towel.", [V("yamamoto", 4), GAG(YK)])],
      gag=YK, sets={"jana": J_BIKINI, "yamamoto": Y_HAWAII}),

    E("yk_erwischt", "gagv", "frech", "Maxwell Catches Him", WANN((4, 6), ["tag"], bed=nach(YK, 5)), "foredeck",
      {"links": "maxwell", "rechts": "yamamoto", "zuschauer": ["jana"]},
      "This time Yamamoto is sitting on the foredeck with his lens trained on the swim platform. Maxwell comes up "
      "silently behind him, takes him by the collar and lifts him a hand's breadth off the deck. Jana stands by with "
      "her hands over her mouth.",
      [Z("maxwell", "Caught! Mr. Maximum catches the bird! Number One, what happens to a bird that gets caught?", "pride"),
       Z("yamamoto", "So sorry. I am a quiet bird. I only look. I never touch. This is my promise.", "fear")],
      [O("Lets Maxwell decide: the photos get deleted.", [V("maxwell", 6), V("yamamoto", -4), GAG(YK)], von="maxwell"),
       O("“He deletes them, but he keeps one photo.”", [V("yamamoto", 6), V("maxwell", -2), GAG(YK)], von="yamamoto"),
       O("“Ten push-ups for the bird, and we forget it.”", [], probe=P("charm", 13),
         erfolg=[V("maxwell", 4), V("yamamoto", 4), W("moral", 1), GAG(YK)], fehlschlag=[V("jana", -2), GAG(YK)],
         zeile=Z("maxwell", "For the joke! Ten push-ups! Mr. Maximum counts in Zulu! Kunye, kubili, kuthathu!", "excitement"))],
      gag=YK, sets={"maxwell": M_STEWARD, "yamamoto": Y_HAWAII, "jana": J_DECK}),

    E("yk_liste", "gag1", "wholesome", "The Last Item on the List", WANN((5, 6), ["tag"], bed=nach(YK, 6)), "aft_deck",
      P1("yamamoto", ("maxwell", "+", "signs the list"), ("jana", "+", "draws a tick")),
      "Yamamoto has opened his notebook: a list of things he wants to do once in his life. The last item reads: "
      "photograph a real bird. Maxwell reads along, and so does Jana. Then Maxwell sets him on the mat, and Jana "
      "hands him a towel.",
      [Z("maxwell", "Mr. Maximum signs the list. Mr. Maximum will take you to a real bird. After push-ups. Many push-ups.", "approval"),
       Z("yamamoto", "A bird, and a friend with a very large hand. Thirty years of overtime, and this is my holiday.", "joy"),
       Z("jana", "I'll draw the tick, Yamamoto-san. And a little bird next to it. Sorry, a very little bird.", "joy")],
      [O("Joins them on the mat.", [V("yamamoto", 6), V("maxwell", 4), V("jana", 4), W("moral", 2), GAG(YK)]),
       O("Ticks the item off himself.", [V("yamamoto", 6), W("moral", 1), GAG(YK)]),
       O("Takes a photo of all three of them.", [V("jana", 4), V("maxwell", 4), V("yamamoto", 4), GAG(YK)])],
      gag=YK, sets={"yamamoto": Y_BADE, "maxwell": M_TRAIN, "jana": J_DECK}),

    # ------------------------------------------------------------------ Training mit Maxwell (3)
    E("mt_erste", "gag1", "witzig", "06:30 with Mr. Maximum", WANN((2, 4), ["fruehstueck"]), "aft_deck",
      P1("maxwell", ("jana", "-", "hangs on the ropes, panting"), ("toto", "+", "watches with coffee")),
      "Half past six on the aft deck. Maxwell, in his neon-orange training top, stands in front of Jana, hair in a "
      "plait, still half asleep. Totò sits on a bollard and watches, his coffee mug held like a ticket.",
      [Z("maxwell", "Mr. Maximum does not say good morning. Mr. Maximum says: burpees! One joke, one burpee. Go!", "excitement"),
       Z("jana", "Sorry, sorry. Is it already time? Na geh. Okay. One. Two. Servus, legs.", "nervousness")],
      [O("Joins the training.", [], probe=P("strength", 11), erfolg=[W("moral", 1), V("maxwell", 4), V("jana", 4), GAG(MT)],
         fehlschlag=[V("maxwell", 2), V("jana", 2), EN(-1), GAG(MT)]),
       O("Cheers Jana on.", [V("jana", 6), V("maxwell", 2), GAG(MT)],
         zeile=Z("jana", "Thank you, Sir. I can do ten. Maybe six. Okay, three.", "nervousness")),
       O("Steals Totò's coffee and watches.", [V("toto", 4), V("maxwell", -2), GAG(MT)])],
      gag=MT, sets={"maxwell": M_TRAIN, "jana": J_DECK, "toto": "Standard"}),

    E("mt_nicht_aufhoeren", "gag1", "wholesome", "Not at “I Can't”", WANN((3, 5), ["fruehstueck"], bed=nach(MT, 1)),
      "aft_deck", P1("maxwell", ("jana", "-", "is shaking in the plank"), ("lea", "+", "counts out loud")),
      "Jana is holding a plank, her arms trembling, her face bright red. Maxwell crouches in front of her, calm as a "
      "rock. Lea comes past with two mugs and joins in counting.",
      [Z("maxwell", "Mr. Maximum does not hear “I can't”. Mr. Maximum hears “not yet”. Say it with Mr. Maximum.", "caring"),
       Z("jana", "Not… yet. Not yet. Jessas. Not yet! Sorry, my arms are shaking.", "fear")],
      [O("Counts with her.", [], probe=P("empathy", 11), erfolg=[V("jana", 6), V("maxwell", 4), GAG(MT)],
         fehlschlag=[V("jana", 2), GAG(MT)]),
       O("Reins Maxwell in: “That's enough.”", [V("jana", 4), V("maxwell", -4), GAG(MT)]),
       O("Lets Maxwell handle it.", [V("maxwell", 6), V("jana", 2), EN(-1), GAG(MT)])],
      gag=MT, sets={"maxwell": M_TRAIN, "jana": J_DECK, "lea": "Deck"}),

    E("mt_zehn", "gag1", "wholesome", "Ten Push-Ups", WANN((4, 6), ["fruehstueck"], bed=nach(MT, 2)), "aft_deck",
      P1("jana", ("maxwell", "+", "cries with pride and calls it an allergy"), ("toto", "+", "applauds")),
      "Jana is in the starting position. Maxwell counts without blinking. At five she's shaking, at seven she swears "
      "in Viennese, at ten she collapses onto the mat, beaming. Maxwell turns away and wipes his face.",
      [Z("jana", "Ten! TEN! Did you see? Servus, Sir! Sorry! I did ten!", "joy"),
       Z("maxwell", "Mr. Maximum has no tears. Mr. Maximum has an allergy. To very good push-ups. Number One, look away.", "pride")],
      [O("Gives Jana a hand and pulls her up.", [V("jana", 6), V("maxwell", 2), W("moral", 1), GAG(MT)]),
       O("Hands Maxwell a tissue.", [V("maxwell", 6), V("jana", 2), GAG(MT)],
         zeile=Z("maxwell", "Thank you, Number One. This is not a tissue. This is a push-up towel.", "gratitude")),
       O("Invites everyone to breakfast.", [W("moral", 2), V("jana", 4), V("maxwell", 4), V("toto", 2), GAG(MT)])],
      gag=MT, sets={"jana": J_DECK, "maxwell": M_TRAIN, "toto": "Standard"}),
]
