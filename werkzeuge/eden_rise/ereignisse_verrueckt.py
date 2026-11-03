# -*- coding: utf-8 -*-
"""Verrueckte Events (18.10.2026, Duc): vier Gags im Anime-Ton fuer Figuren mit wenigen Events (Casanova, Petru,
Elsa, Totò, Megan) und ein intimer Abend: die Flamenco-Stunde mit Madame Casanova (fuehrt in eine Szene, Lohn ist die
Rose der Buergermeisterin - einmal pro Durchlauf). Casanova traegt bei Festa und Feierlichkeiten ihr Flamenco-Kleid
(ST-Set "alva_flamenco_rojo")."""
from ereignisse_basis import *  # noqa: F401,F403

KLEID = "alva_flamenco_rojo"      # Casanovas Flamenco-Kleid (so heisst das Set im ST-Ordner)

EVENTS = [
    # ---------------------------------------------------------------- Casanova: die Generalprobe
    E("g1_casanova_nebel", "gag1", "witzig", "The Dress Rehearsal", WANN((3, 5), ["tag"], an_land=True), "village_harbour",
      {"handelnd": "casanova", "betroffen": [{"id": "elsa", "ton": "-", "was": "her boat is lost in the fog"},
                                             {"id": "toto", "ton": "+", "was": "is selling seats"},
                                             {"id": "petru", "ton": "?", "was": "saw nothing"},
                                             {"id": "pascal", "ton": "+", "was": "takes the blame"}]},
      "Madame Casanova is rehearsing her festa entrance. In a flamenco dress, on a fishing boat, with a hired fog "
      "machine. The fog is thicker than planned. The whole harbour has gone white. Somewhere in it, Elsa's patrol "
      "boat is sounding its horn.",
      [Z("casanova", "Behold! The mayor rises from the mists of Corsica! …Is it working? I can't see anything. "
                     "Perfect.", "excitement"),
       Z("elsa", "Madame. I can't see my own bow. Turn. It. Off.", "annoyance"),
       Z("toto", "Front row in the fog, ten euros! Second row, five! You see nothing, but you see nothing first!", "amusement"),
       Z("pascal", "Lieutenant, this is my fault, please write it down. I ordered the small machine. This is the small "
                   "machine.", "amusement"),
       Z("elsa", "Then I'll need a form, Monsieur Leca. The same kind as the one for my antenna, I suppose. It's been "
                 "eleven months.", "annoyance"),
       Z("pascal", "Almost through, Elsa. I promise you, almost.", "caring")],
      [O("Fixes the fog machine so it doses properly.", [], probe=P("cunning", 12, "handwerk"),
         erfolg=[V("casanova", 6), V("elsa", 4), W("ruf", 1)], fehlschlag=[V("elsa", -4), GAG("casanova_kapelle")],
         zeile=Z("casanova", "A gentle mist! A mysterious mist! You have given me the gift of drama, Monsieur!", "joy")),
       O("Applauds loudly until she bows.", [V("casanova", 6), W("moral", 1)],
         zeile=Z("casanova", "The people love me! Even the ones I cannot see!", "pride")),
       O("Guides Elsa back to her boat.", [V("elsa", 6), V("casanova", -2)],
         zeile=Z("elsa", "…Thank you. Tell her the fog machine is now evidence.", "gratitude"))],
      sets={"casanova": KLEID}),

    # ---------------------------------------------------------------- Petru: der Oktopus
    E("g1_petru_oktopus", "gag1", "witzig", "Petru's Lodger", WANN((3, 6), ["fruehstueck", "tag"]), "galley",
      {"handelnd": "lola", "betroffen": [{"id": "petru", "ton": "-", "was": "is looking for his friend"},
                                         {"id": "chiara", "ton": "-", "was": "ink on her uniform"},
                                         {"id": "toto", "ton": "+", "was": "smells calamari"}]},
      "Petru left a bucket on board when he made his delivery. In the bucket was an octopus he's been feeding for "
      "weeks and calls Bastianu. Now the bucket is empty. Lola is standing in the galley with a wooden spoon, "
      "swearing she only had a look. An arm waves from the sink.",
      [Z("lola", "Okay, so, in my defence, he looked hungry. And then he looked at the garlic. And then he was GONE.", "nervousness"),
       Z("petru", "Bastianu. Come here.", "sadness"),
       Z("toto", "Comandante, think about it. The garlic is already here. Destiny is calling.", "amusement")],
      [O("Gently coaxes Bastianu back into the bucket.", [], probe=P("empathy", 12),
         erfolg=[V("petru", 8), V("lola", 4)], fehlschlag=[V("chiara", -4)],
         zeile=Z("petru", "…Grazie. He likes you. He never likes anybody.", "gratitude")),
       O("Makes it clear to Totò: you don't eat friends.", [V("petru", 6), V("toto", -2)],
         zeile=Z("toto", "Fine! Fine. I will eat my feelings. Also not octopus.", "disappointment")),
       O("Lets Lola draw the octopus until Petru collects him.", [V("lola", 6), W("moral", 1)],
         zeile=Z("lola", "Look, I gave him eyebrows. He's thrilled. He's not thrilled. He's an octopus.", "joy"))]),

    # ---------------------------------------------------------------- Elsa gegen Totò: die Kiste, die miaut
    E("gv_elsa_kiste", "gagv", "witzig", "Potatoes That Meow", WANN((3, 6), ["tag", "abend"], an_land=True),
      "village_harbour", {"links": "elsa", "rechts": "toto", "zuschauer": ["casanova", "alva"]},
      "Elsa has stopped one of Totò's crates on the quay. The crate says “Potatoes”. The crate meows. Totò claims "
      "they're very young potatoes. Elsa has already pulled out her notebook.",
      [Z("elsa", "Monsieur Esposito. Potatoes do not purr.", "disapproval"),
       Z("toto", "Corsican potatoes, Lieutenant. Very emotional. It's the soil.", "amusement"),
       Z("alva", "Open it. If it's a cat, I'm keeping it. If it's potatoes, I'm keeping those too.", "amusement")],
      [O("Backs Elsa: open it.", [V("elsa", 6), V("toto", -4), KL("toto", "alva", "Totòs Kartoffeln haben miaut")],
         von="elsa", zeile=Z("elsa", "A kitten. Three kittens. Esposito, you are smuggling kittens.", "surprise")),
       O("Covers for Totò: “Those are my potatoes.”", [V("toto", 6), V("elsa", -4), KR(5)], von="toto",
         zeile=Z("toto", "Comandante! A man of honour! …They are kittens, by the way. For my nonna.", "gratitude")),
       O("Suggests giving the kittens to the village.", [], probe=P("charm", 13),
         erfolg=[V("elsa", 4), V("toto", 4), V("casanova", 6), W("ruf", 1)], fehlschlag=[V("elsa", -2)],
         zeile=Z("casanova", "The official cats of the festa! I declare it! Somebody write it down!", "excitement"),
         art="dritter_weg")],
      sets={"casanova": KLEID}),

    # ---------------------------------------------------------------- Megan: Abendessen per Laptop
    E("hy_megan_dinner", "handy", "witzig", "Megan Joins Dinner", WANN((3, 4), ["dinner", "abend"],
      bed={"nicht": {"flag": "megan_besuch"}}), "ort_duc",
      {"anrufer": "megan", "anrufer_ort": "megan_office", "art": "video"},
      "Megan calls during the crew dinner and demands to be put on a chair. “Team building.” Lola puts a napkin in "
      "front of the laptop and serves Megan a plate of pasta that nobody will eat.",
      [Z("megan", "Put me at the head of the table. Yes. There. Now everyone may look at me while they eat.", "pride"),
       Z("megan", "Mwahaha. That was a laugh. I'm told laughing builds trust. Is it working?", "amusement")],
      [O("Raises a toast to Megan.", [V("megan", 8), R(-2), W("moral", -1)],
         zeile=Z("megan", "To me. How thoughtful. I'm writing it in your file. The nice part of your file.", "joy")),
       O("Lets her “taste” the pasta.", [], probe=P("charm", 12),
         erfolg=[V("megan", 8), W("moral", 1), GAG("megan_lacht")], fehlschlag=[V("megan", -2)],
         zeile=Z("megan", "…Don't tell anyone I laughed. If this leaks, I'll know it was you.", "amusement")),
       O("Politely hangs up so the crew can eat in peace.", [R(3), V("megan", -4)], art="auflegen")],
      sets={"megan": "Boardroom"}),

    # ---------------------------------------------------------------- Abend: Flamenco mit der Buergermeisterin
    E("ab_casanova_flamenco", "abend", "frech", "Flamenco with the Mayor", WANN((21, 21), ["abend", "nacht"],
      an_land=True, bed={"alle": [{"wert": ["vertrauen.casanova", ">=", 2]}, {"nicht": {"flag": "casanova_abend"}}]}),
      "village_piazza", {"pid": "casanova"},
      "The piazza is empty, the festa lights still strung up. Madame Casanova stands by the fountain in a red "
      "flamenco dress, an old portable radio at her feet. She summoned you “for a lesson on behalf of the "
      "municipality”. Then she switches on the radio and stops being the mayor.",
      [Z("casanova", "Tonight there is no mayor. No festa. No speeches. …Well. Maybe one speech. A short one.", "nervousness"),
       Z("casanova", "Flamenco is not dancing, Monsieur. It is a conversation where nobody is allowed to lie.", "desire"),
       Z("casanova", "Give me your hand. If you want to stop, you stop. If you don't… we'll see where the music goes.", "desire")],
      [O("Takes her hand and lets her lead.", [V("casanova", 8), F("casanova_abend"), EN(-1), I("rose_festa"),
                                                    INTIM("casanova", "village_piazza", KLEID, "casanova",
                                                          "Madame Casanova drops the act: no poses, no speeches. She leads the dance, "
                                                          "slow and proud, and it turns intimate between two adults who both want it. "
                                                          "She checks in, laughs at herself, means every step.")],
         zeile=Z("casanova", "Good. Now listen to the guitar. Your feet will lie. Your hands won't.", "desire")),
       O("Dances with her, just dances.", [V("casanova", 8), F("casanova_abend"), NK("casanova"), I("rose_festa")],
         zeile=Z("casanova", "Only dancing. Yes. That is also a conversation. A beautiful one.", "love")),
       O("“Not tonight, Madame.”", [V("casanova", 2)],
         zeile=Z("casanova", "Then the music waits. The way the whole village waits for me. Patiently. Dramatically.", "amusement"))],
      sets={"casanova": KLEID}, knistern=True,
      nachklang_text="A rose from her hair lies in your hand as you walk to the tender. The next morning she greets "
                     "you at the harbour as if nothing had happened. Her eyes say otherwise."),
]

item("rose_festa", "The Mayor's Rose", "verbrauch",
     benutzen=[{"punkte": "begehren." + p, "n": 6} for p in FRAUEN],
     text="From Madame Casanova's hair, after the flamenco. Used once: desire +6 with all the women.")
