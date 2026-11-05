# -*- coding: utf-8 -*-
"""Akt 3: Mina und ihre Vespa (Mina-Dossier docs/brain_trust/mina_dossier.md, Abschnitt "Abgleich mit akt3-cloud", 05.11.2026).

"Second Gear": Minas Vespa springt seit dem Brand aus dem zweiten Gang. Rosi repariert sie (ihr Vater Salvo hatte eine
Vespa-Werkstatt in Catania, figuren/rosi.md); ist Rosi gefeuert, macht es Petru. Wirkung:
  * mina_vespa_heil: Minas Fahrt nach Bastia bringt von Baustoff und Zutat das Doppelte (kern/post.py).
  * a3_post_bastia: Ist die Post nie abgebrannt, gibt es keine Dank-Szene a3_dank_post mit Minas Versprechen. Dann oeffnet
    diese Szene die Fahrt nach Bastia.
Pool Tag 25 bis 30, Tag oder Nachmittag, nur wenn die Post steht (heil oder wieder aufgebaut). Jede Zeile mit Turbo-Tag (G)."""
from ereignisse_basis import *  # noqa: F401,F403
from ereignisse_gag1 import P1  # noqa: E402
from ereignisse_ligeia import G  # noqa: E402
from ereignisse_akt3_woche4 import AKT3, DA, FL, NICHT, tags_fuer  # noqa: E402

VESPA = "mina_vespa_heil"
POST_AN = "a3_post_bastia"
POST_STEHT = {"eine": [FL("aufbau_fertig_post"), NICHT(FL("tk_haus_weg_post"))]}
HEIL = [F(VESPA), F(POST_AN)]


def _wann(*bed):
    return WANN((25, 30), ["tag", "nachmittag"], bed={"alle": [AKT3, POST_STEHT, NICHT(FL(VESPA))] + list(bed)})


VERSPRECHEN = G("mina", "[chuckle] If she runs again, I can go to Bastia every day. So tell me what you need, Yacht, and I'll bring it. "
                        "Double, if second gear holds.", "optimism")

EVENTS = [
    E("a3_mina_vespa", "gag1", "wholesome", "Second Gear", _wann(DA("rosi")), "village_piazza",
      P1("mina", ("rosi", "+", "is already kneeling next to the engine")),
      "Mina is pushing her Vespa across the square. Every few metres it makes a noise like a coffee grinder. "
      "Rosi stops in the middle of the square and listens. Then she puts her toolbox down on the stones.",
      [G("mina", "[sigh] Don't look, Yacht. It's been doing this since the fire. Second gear jumps out, so I go up the hill in first, like a grandmother.", "annoyance"),
       G("rosi", "Who put this clutch cable in, a goat? [laugh] No, don't answer. Mina, give me the key.", "amusement"),
       G("rosi", "[sniff] This one's from nineteen eighty-two. My papa would say she isn't broken, she's tired. He says that about everything he fixes.", "caring"),
       VERSPRECHEN,
       G("rosi", "[clear throat] Officer. Are you going to hold the lamp for me, or are you going to stand there and look important?", "neutral")],
      [O("Holds the lamp. “Like this?”", HEIL + [V("rosi", 4), V("mina", 4)],
         zeile=G("rosi", "Like that. [chuckle] When we're back, write it on the board in the workshop: Rosi one, Vespa nothing.", "pride")),
       O("Holds the lamp and asks: “What was your father's workshop like?”", HEIL + [V("rosi", 6), V("mina", 2)],
         zeile=G("rosi", "[sigh] It had a blue door, and it smelled of oil and coffee. Now it's a car park for an office. ...Pass me the ten, please.", "sadness")),
       O("Holds the lamp and says to Mina: “Ride her up the hill when she's done. I want to hear second gear.”", HEIL + [V("mina", 6), V("rosi", 2)],
         zeile=G("mina", "[laugh] Up the hill in second gear! Okay. Tomorrow I'm in Bastia and back before lunch.", "joy"))],
      sets={"mina": "mina_standard", "rosi": "Vespa Sunday"}),
    E("a3_mina_vespa_petru", "gag1", "wholesome", "Second Gear", _wann(FL("gefeuert_rosi")), "petru_workshop",
      P1("petru", ("mina", "+", "is holding the handlebars")),
      "Mina has pushed her Vespa all the way to Petru's workshop. Petru looks at it the way he looks at a net with a hole in it.",
      [G("mina", "[sigh] Second gear jumps out, Petru. Since the fire. I go up the hill in first, like a grandmother. Can you do anything?", "annoyance"),
       G("petru", "[clear throat] Hm. I fix boats. A Vespa is a small boat with no water under it.", "neutral"),
       VERSPRECHEN,
       G("petru", "[clear throat] You. Will you hold the wheel still while I work, or will you talk?", "neutral")],
      [O("Holds the wheel still and says nothing.", HEIL + [V("petru", 4), V("mina", 4)],
         zeile=G("petru", "[chuckle] Good. You can stay.", "approval")),
       O("Holds the wheel and asks: “Did your grandfather fix engines too, the man who rowed out in 1924?”", HEIL + [V("petru", 6), V("mina", 2)],
         zeile=G("petru", "[sigh] He had no engine. He had two arms and an oar. That was enough.", "pride")),
       O("Holds the wheel and says to Mina: “Ride her up the hill when he's done. I want to hear second gear.”", HEIL + [V("mina", 6), V("petru", 2)],
         zeile=G("mina", "[laugh] Up the hill in second gear! Okay. Tomorrow I'm in Bastia and back before lunch.", "joy"))],
      sets={"mina": "mina_standard", "petru": "Standard"}),
]


def tags_schreiben():
    return tags_fuer(EVENTS, "akt3_mina")
