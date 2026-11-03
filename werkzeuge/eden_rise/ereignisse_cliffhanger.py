# -*- coding: utf-8 -*-
"""Cliffhanger am Ende von Akt 2 (Duc 02.11.2026, Brain Trust Variante B, docs/wiki/welt/drehbuch_finale.md Abschnitt 11).

Nacht von Tag 23 nach dem Bericht: Das Netz kommt zurueck, Elsa schickt die Beweise, Alons Keynote ist schneller (mit
siri_darf_posten rutscht sie ueber Siris Video). Er dankt der Eden Group und ihrem Berater vor Ort, Duc. Das Dorf erfaehrt
damit vom heimlichen Verkauf (E-001/E-003). Megans Anruf, dann akt2_ende: Die Schlusskarte der Beta kommt aus kern/abschluss.
Alon spricht selbst auf seiner Buehne (Raum alon_keynote, Set alon_standard, Stimme Alon Varenne); die Reaktionen kommen auf
dem Kirchplatz. Noch nicht vertont."""
from ereignisse_basis import *  # noqa: F401,F403
from ereignisse_gag1 import P1
from ereignisse_ligeia import G

DIREKT = lambda ziel: {"direkt": ziel}
FRAME = lambda: WANN((23, 23))                    # nur ueber "direkt" geoeffnet
ALON = {"alon": "alon_standard"}

KEYNOTE = [G("alon", "[clear throat] Last night, pirates attacked a small village in Corsica. Our security team was there in forty minutes.", "pride"),
           G("alon", "Zero dead. [sigh] That is what a future without fear looks like.", "joy")]


def _je(z, gruppe, wenn):
    """Zeile nur, wenn die Bedingung passt (kern/ereignisse.zeilen_aktiv)."""
    return dict(z, gruppe=gruppe, wenn=wenn)


EVENTS = [
    E("bl_cliff_netz", "gag1", "ernst", "Signal", WANN((23, 23), ["nacht"], bed={"flag": "belagerung_bericht"}, pflicht=True, holt_leute=True),
      "village_piazza", P1("rosi", ("elsa", "+", "is holding a folder against her chest")),
      "Nobody has gone home. People sit on the church steps and on the edge of the fountain, too tired to talk. Rosi has a laptop "
      "on her knees and a cable running up into the dark. Then, all over the square, the phones light up at once.",
      [G("rosi", "There. Got you. [laugh] ...We have a signal, Officer. It had a very bad password.", "pride"),
       G("elsa", "Sent. Every photo, every name, straight to the commission. [sigh] Now we wait.", "neutral")],
      [O("Takes out his phone.", [F("akt2_netz"),
                                  DIREKT([{"wenn": {"flag": "siri_darf_posten"}, "id": "bl_cliff_alon_siri"}, {"id": "bl_cliff_alon"}])])],
      sets={"rosi": "Engine Room", "elsa": "Standard"}),
    E("bl_cliff_alon", "gag1", "ernst", "Breaking News", FRAME(), "alon_keynote", P1("alon"),
      "Every phone in the square shows the same video: a white stage, a sunrise on a giant screen, and a man in a black turtleneck. "
      "Alon Varenne smiles like a man launching a phone.",
      KEYNOTE, [O("Keeps watching.", [DIREKT("bl_cliff_platz")])], sets=ALON),
    E("bl_cliff_alon_siri", "gag1", "ernst", "Breaking News", FRAME(), "alon_keynote", P1("alon"),
      "For four seconds, Siri's video is the first thing on every screen: the gate, the smoke, Minicu. Then another video slides over it, "
      "and that is the one everybody plays. A white stage, a sunrise, and a man in a black turtleneck: Alon Varenne.",
      KEYNOTE + [G("alon", "Some of you have seen other videos tonight. [chuckle] Please be careful. Today, anyone can make a video.", "amusement")],
      [O("Keeps watching.", [DIREKT("bl_cliff_platz")])], sets=ALON),
    E("bl_cliff_platz", "gag1", "ernst", "Breaking News", FRAME(), "village_piazza", P1("casanova", ("siri", "?", "is staring at her phone")),
      "Across the square the church door is open, and candlelight falls through it onto the stones. Inside, Don is still sitting with Minicu.",
      [_je(G("siri", "That was mine. [sniff] It was up for four seconds.", "sadness"), "siri", {"flag": "siri_darf_posten"}),
       G("casanova", "Forty minutes. [sigh] ...Nobody came in forty minutes. Nobody came at all.", "anger")],
      [O("Looks back at the screen.", [DIREKT("bl_cliff_team")])]),
    E("bl_cliff_team", "gag1", "ernst", "Welcome to the Team", FRAME(), "alon_keynote", P1("alon"),
      "Alon leans a little closer to the camera, and his smile gets warmer.",
      [G("alon", "And I want to thank our partners at the Eden Group, [chuckle] and one man in particular. Their consultant on the ground.", "gratitude"),
       G("alon", "Duc. [laugh] Welcome to the team.", "joy")],
      [O("Lowers the phone.", [DIREKT("bl_cliff_blicke")])], sets=ALON),
    E("bl_cliff_blicke", "gag1", "ernst", "Welcome to the Team", FRAME(), "village_piazza", P1("casanova"),
      "The square goes quiet. Nobody here knew that their harbour was being sold. One by one, the faces in the blue light turn "
      "towards you. Madame Casanova is the last.",
      [G("casanova", "[sigh] ...Monsieur?", "sadness")], [O("Opens his mouth.", [DIREKT("bl_cliff_megan")])]),
    E("bl_cliff_megan", "gag1", "ernst", "Megan", FRAME(), "village_piazza", P1("megan", fern=True),
      "Before you can say anything, your phone rings. Megan. It is the first call that has come through since the war council.",
      [G("megan", "Duc. I've just read the press release. [sigh] You're in it, and so is my deal. Neither of us was supposed to be. "
                  "Don't say a word to anyone until I land.", "anger")],
      [O("Says nothing. The screen goes dark.", [F("akt2_ende")])]),
]
