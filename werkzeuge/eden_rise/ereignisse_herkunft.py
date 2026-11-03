# -*- coding: utf-8 -*-
"""Duc's background (Duc 25.10.2026, E-067): his parents fled Vietnam after the war and built a new life in Germany;
he grew up in a migrant working-class family and worked his way up. Two quiet conversations in Act 1 where it comes up.

Chips as in Tag 0 (E-018): an honest answer wins trust (+1 stage), a warm/funny one wins desire (Chiara) or backing,
a neutral one changes nothing, a faux pas costs a stage. Each choice sets herkunft_<pid>_<chip>.
"""
from ereignisse_basis import *  # noqa: F401,F403

STUFE = 8


def P1(handelnd, *betroffen):
    return {"handelnd": handelnd, "betroffen": [{"id": b[0], "ton": b[1], "was": b[2]} for b in betroffen]}


def flag(pid, art):
    return F("herkunft_%s_%s" % (pid, art))


EVENTS = [
    # ------------------------------------------------------------------ Yamamoto asks how life was
    E("yk_herkunft", "gag1", "ernst", "Before the Suits", WANN((3, 6), ["abend", "nacht"]), "sun_deck",
      P1("yamamoto", ("maxwell", "?", "asleep on a lounger nearby")),
      "Late on the sun deck. For once Yamamoto has put his camera away. He's holding a small glass of whisky he isn't "
      "drinking, and he asks you something nobody on this boat has asked yet.",
      [Z("yamamoto", "Officer-san. Thirty years in a bank, and I never asked anyone this. So I ask you now. How was your "
                     "life? Before the yachts. Before the suits.", "curiosity")],
      [O("Tells him the whole story: parents who fled Vietnam after the war, a small flat in Germany, night shifts, and "
         "a son who was supposed to have it better.",
         [V("yamamoto", STUFE), flag("yamamoto", "v")],
         zeile=Z("yamamoto", "My father was a fisherman in Noto. He smelled of the sea until the day he died, and he never "
                             "once complained. …I think our fathers would have understood each other, Officer-san.",
                 "admiration")),
       O("“Short version: rice, homework, and a mother who checked both.”", [R(5), flag("yamamoto", "h")],
         zeile=Z("yamamoto", "Ha. My mother checked the rice. Homework was my father's war. Very interesting.", "amusement")),
       O("“It was fine. It's a long story.”", [flag("yamamoto", "n")],
         zeile=Z("yamamoto", "Long stories are the best kind. Another evening, then.", "neutral")),
       O("“I'm a self-made man. Nobody helped me.”", [V("yamamoto", -STUFE), flag("yamamoto", "f")],
         zeile=Z("yamamoto", "Nobody? Hm. In my experience, a self-made man has usually forgotten who made the tea. So "
                             "sorry.", "disapproval"))],
      sets={"yamamoto": "yamamoto_hawaii_b"}),

    # ------------------------------------------------------------------ Chiara, after midnight
    E("ak_chiara_herkunft", "gag1", "wholesome", "Who Believed in You?",
      WANN((3, 6), ["nacht"], bed={"vertrauen": ["chiara", 2]}), "crew_mess",
      P1("chiara", ("lola", "?", "is snoring in the galley next door")),
      "The crew mess, after midnight. Chiara is sitting with a cup of tea and a stack of checklists she is "
      "re-laminating for no reason. She looks up when you come in, and for once she doesn't hand you a job.",
      [Z("chiara", "Can I ask you something? Not as the Chief Stew. You've got a company, a sabbatical, a limousine with "
                   "six windows. How did you get there? Who believed in you?", "curiosity")],
      [O("Tells her about his parents' flight from Vietnam, the years of night shifts, and that nobody expected him to "
         "get this far.",
         [V("chiara", STUFE), flag("chiara", "v")],
         zeile=Z("chiara", "My grandfather had a captain's licence and a whole wall of photos. Everyone expected my brother "
                           "to get one too. Nobody ever asked me. …Thank you for telling me. I won't make it a story. "
                           "It's yours.", "caring")),
       O("“My mother believed in me. Loudly. In front of the whole street.”", [B("chiara", STUFE), flag("chiara", "b")],
         zeile=Z("chiara", "…I like her already. Loud women raise people who get things done. I'd know.", "amusement")),
       O("“It's a long story. Another night.”", [flag("chiara", "n")],
         zeile=Z("chiara", "Okay. I'm holding you to that. Another night.", "neutral")),
       O("“Hard work. Anyone can do it if they really want to.”", [V("chiara", -STUFE), flag("chiara", "f")],
         zeile=Z("chiara", "Anyone? Some of us were told what we're allowed to want before we could spell it. Goodnight, "
                           "First Officer.", "annoyance"))],
      sets={"chiara": "Cabin Night"}),
]
