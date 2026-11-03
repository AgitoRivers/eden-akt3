# -*- coding: utf-8 -*-
"""Vertrauens-Abende mit Lola und Alva (Grundlagen: Lola Tag 3 ab Vertrauen 3, Alva Tag 4 ab Vertrauen 3; Wiederholung
per Handy ab Vertrauen 4, Ort frei waehlbar, kostet keine Zeit). Fuehren in eine Intim-Szene, die das Modell spielt
(szene_intim: pid, ort, set, fuehrung = wer fuehrt, hinweis = Regieanweisung). Beide Frauen entscheiden mit:
jede Option laesst ein Nein zu, ohne dass die Beziehung bricht."""
from ereignisse_basis import *  # noqa: F401,F403

EVENTS = [
    E("ab_lola_klopft", "abend", "frech", "A Knock at the Cabin", WANN((3, 6), ["nacht"],
      bed={"alle": [{"wert": ["vertrauen.lola", ">=", 3]}, {"nicht": {"flag": "lola_abend"}}]}), "duc_cabin", {"pid": "lola"},
      "Just after midnight there's a knock. Lola is standing in the doorway, barefoot, in a T-shirt far too big for "
      "her, her eyes glassy and happy. She smells of the sea and sweet smoke. She leans against the door frame and "
      "grins.",
      [Z("lola", "Hiii. I was smoking on the stern and the stars told me to come here. The stars are very bossy tonight.", "amusement"),
       Z("lola", "Can I come in? I'm not that high, I'm medium high. High enough to say I've wanted you since the galley.", "desire"),
       Z("lola", "You can say no, Boss, and I'll just go back and tell the stars they were wrong. They'll get over it.", "caring")],
      [O("Lets her in.", [V("lola", 6), B("lola", 8), F("lola_abend"), EN(-1),
                               INTIM("lola", "duc_cabin", "Off Duty", "lola",
                                     "Lola is high, giggly and very forward, and she leads. Playful, dirty, warm; she checks in with a laugh and means it.")],
         zeile=Z("lola", "Oh, thank god. Lie down and let me show you what the stars had in mind.", "desire")),
       O("Lets her in, but talks first.", [V("lola", 8), B("lola", 4), F("lola_abend"), NK("lola")],
         zeile=Z("lola", "Talking first? You're so sweet it hurts. Okay, talk to me, then maybe kiss me, then maybe more.", "love")),
       O("“Not tonight, Lola. Come back when you're clear-headed.”", [V("lola", 4)],
         zeile=Z("lola", "Respect. Annoying, but respect. I'll come back sober and twice as dangerous.", "amusement"))],
      sets={"lola": "Off Duty"}, knistern=True,
      nachklang_text="Smoke, salt, Lola's laugh in the dark. At breakfast you're the only one who gets a "
                     "heart-shaped pancake."),

    E("ab_lola_handy", "abend", "frech", "Lola Texts: “You Awake?”", WANN((4, 6), ["abend", "nacht"],
      bed={"alle": [{"wert": ["vertrauen.lola", ">=", 4]}, {"flag": "lola_abend"}]}), "duc_cabin", {"pid": "lola"},
      "A message from Lola: a photo of her bare back in the moonlight, and underneath, a single word: “Again?” She "
      "lets you choose the place. The night is long, she writes.",
      [Z("lola", "Again? You choose where. I'll be there before you've finished reading this. I'm fast when I want "
                 "something.", "desire"),
       Z("lola", "No pressure, Boss. If you're tired, send me a heart and I'll dream about you instead. Loudly.", "amusement")],
      [O("Chooses a place to meet.", [B("lola", 6), V("lola", 4),
                                INTIM("lola", "frei", "Off Duty", "lola", "Lola chose this, again. Familiar now, bolder, laughing, filthy and tender.")],
         zeile=Z("lola", "On my way, so leave the light off. I know the way by heart now.", "desire"), art="ort_waehlen"),
       O("Sends a heart.", [V("lola", 4)], zeile=Z("lola", "Dreaming about you, out loud. Sorry, Rosi.", "love"))],
      sets={"lola": "Nude"}),

    E("ab_alva_barabend", "abend", "frech", "After Hours at Alva's", WANN((4, 6), ["abend"], an_land=True,
      bed={"alle": [{"wert": ["vertrauen.alva", ">=", 3]}, {"nicht": {"flag": "alva_abend"}}]}), "alvas_bar", {"pid": "alva"},
      "The last fishermen have gone. Alva turns the sign to “Chiuso” and locks the door. She goes into the back room "
      "and comes back in something black with ruffles that hardly covers anything. There's a rose in her curls.",
      [Z("alva", "For forty years this bar has been open to everybody. Tonight it's open to one man. Sit, o figliolu.", "desire"),
       Z("alva", "My grandmother danced flamenco in Seville. I only learned the parts that end on a table.", "amusement"),
       Z("alva", "You can walk out, you know. The door is right there. But you won't.", "desire")],
      [O("Stays with her.", [V("alva", 8), B("alva", 8), F("alva_abend"), EN(-1),
                      INTIM("alva", "alvas_bar", "alva_flamenco_noche", "alva",
                            "Alva is in charge in her own bar: slow, teasing, experienced, very sure of what she wants; she dances first.")],
         zeile=Z("alva", "Good. Now watch. Don't touch. Not yet. I'll tell you when.", "desire")),
       O("Dances with her, very slowly.", [V("alva", 6), B("alva", 6), F("alva_abend"), NK("alva")],
         zeile=Z("alva", "You dance like a sailor. Hold me closer. There. Now you dance like a man who stays.", "love")),
       O("“Not tonight, Alva.”", [V("alva", 2)], zeile=Z("alva", "Then I'll leave the dress on the chair. It's "
                                                                 "patient. I'm not.", "amusement"))],
      sets={"alva": "alva_flamenco_noche"}, knistern=True,
      nachklang_text="Black ruffles on a bar stool, a rose on the floor. You can still smell her as you row back to "
                     "the boat in the morning."),

    E("ab_alva_handy", "abend", "frech", "Alva Calls: “Come Over.”", WANN((5, 6), ["abend", "nacht"],
      bed={"alle": [{"wert": ["vertrauen.alva", ">=", 4]}, {"flag": "alva_abend"}]}), "duc_cabin", {"pid": "alva"},
      "Alva calls. She's wearing something black with white polka dots and swinging a small key on a red cord in "
      "front of the camera. The key to her back room.",
      [Z("alva", "I had a key made for the back room, for you. Nobody else has one, not even my accountant.", "desire"),
       Z("alva", "Tonight or whenever you want, and wherever you want. I'll bring the fan. You know what the fan is for.", "amusement")],
      [O("Chooses a place to meet.", [B("alva", 6), V("alva", 6), I("alvas_schluessel"),
                         INTIM("alva", "frei", "alva_flamenco_noche", "alva", "Alva again, playful and possessive, a little jealous, very skilled.")],
         zeile=Z("alva", "Perfect. Don't eat. I'll feed you after.", "desire"), art="ort_waehlen"),
       O("“Tomorrow. I promise.”", [VER("alva", "Duc visits Alva tomorrow", 1, {"flag": "alva_besucht"}), V("alva", 4), I("alvas_schluessel")],
         art="versprechen")],
      sets={"alva": "alva_flamenco_noche"}),
]

item("alvas_schluessel", "Key to Alva's Back Room", "schluessel",
     text="On a red cord. Opens the bar's back room, also for quiet talks without witnesses.")
