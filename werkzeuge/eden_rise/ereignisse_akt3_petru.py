# -*- coding: utf-8 -*-
"""Akt 3: mehr Petru (Duc 04.11.2026, "gib Petru etwas mehr Dialog und Character"). Figurenseite docs/wiki/figuren/petru.md.

Er bleibt knapp, aber in ganzen, ruhigen Saetzen mit Bildern vom Meer. Marie (Frau, vor fuenf Jahren gestorben, Fish Pie mit
dem Lorbeerblatt in der Milch), Laetitia (Tochter, er hat ihr nie gesagt, dass er sie braucht), das heile Netz, das er jeden
Nachmittag flickt, Bastianu (Oktopus, oeffnet Glaeser), das Radio mit korsischem Fussball, der Grossvater von 1924, Ba Tu
(Fischeintopf, keine Romanze). Vier kleine Szenen ohne eigene Phase:
  a3_petru_netz       beim Besuch der Werkstatt (kern/akt3.szene_besuch), ab Tag 25: das Netz wird das Netz der Namen
  a3_petru_bastianu   Pool Tag 25-31 (Gag): der Oktopus und Rosis Schrauben
  a3_petru_eintopf    Pool Tag 26-31: Ba Tu bringt Eintopf
  a3_petru_brief      Pool Tag 29-33: ein Brief an Laetitia, drei Fassungen nach dem Weg in den Bergen
Wirkung: die Festa liest a3_petru_netz (die Namen der Zeugen im Netz) und a3_petru_brief_<wahl> (Laetitia kommt oder schreibt)."""
from ereignisse_basis import *  # noqa: F401,F403
from ereignisse_gag1 import P1  # noqa: E402
from ereignisse_ligeia import G  # noqa: E402
from ereignisse_akt3_woche4 import FR, FL, NICHT, DA, AKT3, JE, tags_fuer  # noqa: E402

PETRU = [
    FR("a3_petru_netz", "petru_workshop", "Not in the Net",
       "Petru sits in front of his workshop and mends a net. It is the same net as every afternoon, and it is not broken. "
       "The radio on the workbench plays Corsican football, very quietly.",
       [G("petru", "[clear throat] Marie used to say I mend this net so my hands don't think. She was right. She was always right, "
                   "except about the fish pie. Mine was never as good as hers.", "sadness"),
        G("petru", "[sigh] Five years. Every afternoon. Not one hole in it. ...Sit. If you sit, you hold the other end.", "neutral")],
       [O("Sits down and holds the other end of the net.", [F("a3_petru_netz"), F("a3_petru_netz_halten"), V("petru", 6)],
          zeile=G("petru", "[sigh] Good. ...After the festa I give this net away. The people who spoke, their names go in the knots. "
                           "The sea keeps what you tie well.", "caring")),
        O("“Why do you mend a net that isn't broken, Petru?”", [F("a3_petru_netz"), F("a3_petru_netz_frage"), V("petru", 4)],
          zeile=G("petru", "[clear throat] Because one day it breaks. And then my hands know it already. ...This one is for the village now. "
                           "For names. You'll see.", "neutral")),
        O("“Tell me about Marie.”", [F("a3_petru_netz"), F("a3_petru_netz_marie"), V("petru", 6)],
          zeile=G("petru", "[sniff] A bay leaf in the milk. That was her secret. Nobody else knows it. Now you. ...Don't tell Alva.", "love"))],
       personen={"handelnd": "petru", "betroffen": []}, sets={"petru": "Standard"}),
    E("a3_petru_bastianu", "gag1", "witzig", "Bastianu", WANN((25, 31), ["tag", "nachmittag"], bed={"alle": [AKT3, DA("rosi")]}),
      "petru_workshop", P1("rosi", ("petru", "?", "pretends to see nothing")),
      "Rosi is working at Petru's bench. Her jar of small screws is open. A long red arm comes out of the water tank and takes the jar.",
      [G("rosi", "[gasp] Petru! Your octopus has my screws. All of them.", "anger"),
       G("petru", "[clear throat] Bastianu does not steal. He borrows. Like the sea. Everything comes back, eventually.", "neutral"),
       G("rosi", "[sigh] Eventually? I need them now. ...He's screwing the lid back on. From the inside. That's a talent.", "surprise")],
      [O("Offers Bastianu a sardine for the jar.", [V("petru", 2), V("rosi", 2)],
         zeile=G("petru", "[chuckle] A fair trade. He likes you. He doesn't like many people.", "amusement")),
       O("“Hire him, Rosi. He's faster than Totò.”", [V("rosi", 2)],
         zeile=G("rosi", "[laugh] Unit-01 is jealous already.", "amusement"))],
      sets={"rosi": "Engine Room", "petru": "Standard"}),
    E("a3_petru_eintopf", "gag1", "wholesome", "Fish Sauce", WANN((26, 31), ["dinner"], bed=AKT3), "petru_workshop",
      P1("batu", ("petru", "+", "lifts the lid")),
      "Bà Tư comes into the workshop with a pot. She has done this every week since the siege, because she thinks he is lonely.",
      [G("batu", "[clear throat] Fish stew. With fish sauce. You said the first one smelled like a harbour at noon.", "caring"),
       G("petru", "[chuckle] It did. Now I wait for it. The whole week. ...Here. Two mullet. From this morning.", "gratitude"),
       G("batu", "[sigh] He gives me fish, I give him fish. We are two old idiots, con. Eat with us.", "caring")],
      [O("Sits down between them and eats.", [V("batu", 2), V("petru", 2)],
         zeile=G("petru", "[sigh] Marie would like her. She would not say so. Like me.", "caring")),
       O("“Is this a date?”", [V("batu", 2)],
         zeile=G("batu", "[laugh] A date! He has the Norwegian for that. I have the stew. Eat.", "amusement"))]),
    E("a3_petru_brief", "gag1", "wholesome", "A Letter to Laetitia", WANN((29, 33), ["nachmittag"], bed={"alle": [AKT3, {"wert": ["vertrauen.petru", ">=", 3]}]}),
      "petru_workshop", P1("petru", ("mina", "?", "waits with her bag")),
      "Petru has a sheet of paper on the workbench and a pencil he has sharpened three times. Mina waits at the door with her bag.",
      [JE(G("petru", "[sigh] My daughter. She doesn't talk to you since the mountains, I know. To me she writes once a year. "
                     "I want to say something to her. I am bad with paper.", "sadness"), "weg", FL("bg_weg_a")),
       JE(G("petru", "[clear throat] You took her over the sea, that night. I was angry. Her card made me less angry. "
                     "Now I want to write back. I am bad with paper.", "neutral"), "weg", FL("bg_weg_b")),
       JE(G("petru", "[sigh] She is up there, in the Bergerie, with him. Happy, I think. I want to ask her to come down for the festa. "
                     "I am bad with paper.", "sadness"), "weg", None),
       G("petru", "[clear throat] All her life I never told her I need her. What do I write?", "nervousness")],
      [O("“Write exactly that. 'I need you.'”", [F("a3_petru_brief"), F("a3_petru_brief_brauche"), V("petru", 6)],
         zeile=G("petru", "[sniff] Three words. The sea is bigger, and it is easier.", "love")),
       O("“Ask her to come to the festa. Nothing more.”", [F("a3_petru_brief"), F("a3_petru_brief_festa"), V("petru", 4)],
         zeile=G("mina", "[chuckle] Express, Petru. For you, express. No charge.", "caring")),
       O("“Tell her about the fish pie. The bay leaf. She'll understand.”", [F("a3_petru_brief"), F("a3_petru_brief_marie"), V("petru", 6)],
         zeile=G("petru", "[sigh] Her mother's secret. ...Yes. She will understand that better than words.", "love"))],
      sets={"petru": "Standard"}),
]

EVENTS = PETRU


def tags_schreiben():
    return tags_fuer(EVENTS, "akt3_petru")
