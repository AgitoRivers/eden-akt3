# -*- coding: utf-8 -*-
r"""Missionen fuer das Modul eden_rise (17.10.2026) - Ducs Staerken Kueche, Koepfchen, Handwerk.

Format der Schnelljobs (Code: handel.jobs_heute / handel.job_machen): Handy-Auftrag,
1 Energie, W20-Probe; reparatur=True -> Vorteil Handwerk, kochen=True -> Vorteil Kueche (Persona). nach = erst nach
ERFOLG dieser Mission (oder irgendeines Wegs der Gruppe), ab_vertrauen = Mindeststufe bei der Auftraggeberin.
Frauen zahlen nicht: Vertrauen je Hilfe, Begehren nur mit persoenlich=True.
Seit 18.10.2026 (Paket 1): braucht = Gegenstand wird abgegeben; probe=False = kein Wurf, keine Energie; preis = kostet
Geld; werkzeug = [Items] -> Vorteil (oder +2, wenn die Staerke schon Vorteil gibt); gruppe = mehrere Wege, ein Erfolg
schliesst die anderen. Fehlschlag: morgen noch einmal, nach dem zweiten halber Lohn und vorbei (kern\handel.py).

    python missionen_eden_rise.py   -> module\eden_rise\missionen.json (mit Pruefung)
"""
import json, os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(os.path.dirname(HIER))    # werkzeuge\eden_rise -> Eden
ZIEL = os.path.join(EDEN, "module", "eden_rise", "missionen.json")
PERSONEN = ["chiara", "sophia", "lea", "rosi", "siri", "toto", "yasin", "holm", "elsa", "alva", "petru", "casanova",
            "lola", "megan"]
ATTRIBUTE = ["charm", "empathy", "perception", "cunning", "courage", "strength"]
FRAUEN = ["chiara", "sophia", "lea", "rosi", "siri"]

MISSIONEN = [
    # Kueche
    {"id": "lola_kochkurs", "von": "lola", "titel": "Cooking Class: Lola Learns Thịt Kho", "tage": [2, 7], "attribut": "empathy",
     "sg": 13, "lohn": 0, "kochen": True, "folgen": [{"vertrauen": ["lola", 6]}, {"item": "lola_vegemite"}],
     "text": "Lola wants to know how to caramelise pork belly without setting the galley on fire. She has prepared "
             "notes. One of them just says “don't set on fire”.",
     "erfolg": "Lola's first thịt kho gleams. She hugs you with the wooden spoon still in her hand and gives you her "
               "last jar of Vegemite.",
     "fehlschlag": "The sugar turns black. Lola laughs so hard she has to sit down."},
    # Koepfchen
    {"id": "alva_kassenbuch", "von": "alva", "titel": "Alva's Accounts", "tage": [2, 7], "attribut": "perception",
     "sg": 12, "lohn": 120, "folgen": [{"wert": "ruf", "delta": 1}],
     "text": "Alva's accounts are a shoebox full of receipts. The tax office wants figures by the end of the month. "
             "She puts a myrtle liqueur in front of you and slides the box across the bar.",
     "erfolg": "Three columns, one total, and a forgotten supplier who owes her money. Alva kisses you on the "
               "forehead.",
     "fehlschlag": "The figures almost add up. Alva pays half and calls you “Commercialista” anyway."},
    {"id": "casanova_plan", "von": "casanova", "titel": "A Sustainability Plan for the Festa", "tage": [3, 5],
     "attribut": "charm", "sg": 12, "lohn": 100, "nach": "english_kids",
     "folgen": [{"wert": "ruf", "delta": 1}, {"item": "casanova_kanone"}],
     "text": "Madame Casanova has heard that you're a sustainability consultant. She wants the greenest festa in "
             "Corsica. With fireworks. And disposable barbecues. And four hundred balloons.",
     "erfolg": "Deposit cups, fairy lights instead of torches, fish from Petru. She calls it her idea and gives you "
               "her confetti cannon.",
     "fehlschlag": "The balloons stay. The disposable barbecues don't. Half a victory and half the pay."},
    # Handwerk: Kette bei Petru
    {"id": "petru_motor_1", "von": "petru", "titel": "Petru's Old Boat Engine", "tage": [3, 7], "attribut": "cunning",
     "sg": 13, "lohn": 0, "reparatur": True, "werkzeug": ["multitool"], "nach": "nets", "folgen": [{"vertrauen": ["petru", 4]}],
     "text": "In Petru's workshop an engine sits under a tarpaulin. A Volvo Penta, older than you. It belonged to "
             "his father. Petru pulls the tarpaulin off and says nothing.",
     "erfolg": "The engine turns over for the first time in years. Petru puts a hand on your shoulder and leaves it "
               "there.",
     "fehlschlag": "It coughs and dies. Petru nods. “Tomorrow.”"},
    {"id": "petru_motor_2", "von": "petru", "titel": "The First Trip Out", "tage": [4, 7], "attribut": "courage",
     "sg": 12, "lohn": 0, "reparatur": True, "werkzeug": ["multitool"], "nach": "petru_motor_1",
     "folgen": [{"vertrauen": ["petru", 6]}, {"item": "petrus_hammer"}, {"wert": "ruf", "delta": 1}],
     "text": "Petru wants to hear the engine on the water. In his father's boat, with you at the helm, once around "
             "the harbour wall.",
     "erfolg": "You head out. Petru tells a whole story, with a beginning and an end. At the jetty he gives you his "
               "father's hammer.",
     "fehlschlag": "Just short of the harbour wall the engine quits. You row back. Petru laughs. Nobody has ever "
                   "heard that before."},
    # Mehrere Wege (Paket 1): Alvas Kuehlung - ersetzt die alte Eismaschine
    {"id": "alva_kuehlung_eis", "von": "alva", "gruppe": "alva_kuehlung", "titel": "Cooling: Fetch Ice", "tage": [2, 7],
     "probe": False, "preis": 60, "lohn": 0, "folgen": [{"vertrauen": ["alva", 4]}],
     "text": "Totò has block ice in the storeroom. That saves the festa stock for today – tomorrow it starts "
             "sweating again.",
     "erfolg": "You haul two blocks of ice down to Alva's cellar. “Today you're my hero. Tomorrow we'll see.”"},
    {"id": "alva_kuehlung_reparatur", "von": "alva", "gruppe": "alva_kuehlung", "titel": "Cooling: Repair It Yourself",
     "tage": [2, 7], "attribut": "cunning", "sg": 13, "lohn": 150, "reparatur": True, "werkzeug": ["multitool"],
     "folgen": [{"wert": "ruf", "delta": 1}],
     "text": "The compressor is dead, and all the festa stock is sweating. Take it apart, swap the relay – if it "
             "works, the cooling runs for good and Alva pays.",
     "erfolg": "The compressor hums again. Alva puts a myrtle liqueur in front of you and pays without haggling.",
     "fehlschlag": "A spark, a bang, silence. Alva sighs. “Ice, then. Or Totò.”"},
    {"id": "alva_kuehlung_toto", "von": "toto", "gruppe": "alva_kuehlung", "titel": "Cooling: Ask Totò for a Relay",
     "tage": [2, 7], "probe": False, "lohn": 0, "folgen": [{"vertrauen": ["alva", 6]}],
     "text": "Totò “happens” to have exactly the relay Alva's compressor needs. He doesn't want money. He wants you "
             "to remember.",
     "erfolg": "The relay fits. Alva is happy. Totò winks at you. “You owe me a little something, Comandante.”"},
    {"id": "toto_gefallen", "von": "toto", "titel": "Totò's Little Crate", "tage": [3, 7], "attribut": "cunning", "sg": 13,
     "lohn": 0, "nach": "alva_kuehlung_toto", "folgen": [{"vertrauen": ["toto", 6]}],
     "folgen_fehlschlag": [{"wert": "ruf", "delta": -1}],
     "text": "“Comandante, the relay for Alva's compressor? You owe me a little something, remember. I have a little crate that needs to get past Elsa's boat tonight.”",
     "erfolg": "The crate is across, Elsa saw nothing. Totò hugs you like a brother. You're square.",
     "fehlschlag": "Elsa's lamp sweeps over the dinghy. Nobody gets arrested, but the village talks."},
    # Abgabe (Paket 1): eine Ersatzbatterie fuer Rosi - Geld wird zu Strom und Vertrauen
    {"id": "rosi_ersatzbatterie", "von": "rosi", "titel": "A Spare Battery for Rosi", "tage": [3, 7], "probe": False,
     "braucht": "ersatzzellen", "lohn": 0, "folgen": [],
     "text": "Two cells of the hotel battery are dead. Rosi needs replacements, no matter where from. “Don't ask "
             "Chiara what they cost.”",
     "erfolg": "Rosi clamps the cells in and the display jumps to green. She wipes oil off her forehead and grins at "
               "you."},
]


# Dorf- und Crew-Missionen (18.10.2026 aus Gestrandet uebernommen, Text und Werte unveraendert; bis dahin hat
# kern\showrunner.py sie zur Laufzeit aus dem alten Modul gelesen). Reihenfolge wie dort - sie bestimmt das Tagesangebot.
DORF = [
    {"id": "nets", "von": "petru", "titel": "Mending Petru's Nets", "tage": [2, 7], "attribut": "perception", "sg": 10,
     "lohn": 60, "folgen": [{"wert": "ruf", "delta": 1}],
     "text": "Petru points at a heap of nets and says nothing. That's an offer.",
     "erfolg": "Petru nods once. From him, that's a medal.", "fehlschlag": "You missed two holes. Petru pays "
                                                                               "something anyway."},
    {"id": "radio_elsa", "von": "elsa", "titel": "The Radio at the Coast Guard Post", "tage": [2, 6], "attribut": "cunning", "sg": 11,
     "lohn": 90, "reparatur": True, "folgen": [{"wert": "ruf", "delta": 1}],
     "text": "Elsa's radio link to Ajaccio is crackling. No radio, no salvage – she pays cash and hates having to "
             "ask.",
     "erfolg": "Clear reception. Elsa nods once – from her, that's a medal.", "fehlschlag": "It crackles less. Elsa pays half."},
    {"id": "english_kids", "von": "casanova", "titel": "English for the Mayor's Nieces and Nephews", "tage": [2, 6],
     "attribut": "charm", "sg": 10, "lohn": 70, "folgen": [{"wert": "ruf", "delta": 1}],
     "text": "One nephew, one niece, one hour, one schoolbook. Madame Casanova pays cash and tells the whole village.",
     "erfolg": "The children laugh and can say “anchor”. The village speaks well of you.", "fehlschlag": "Chaos, but warm-hearted chaos. Half "
                                                                                                           "pay."},
    {"id": "drone", "von": "yasin", "titel": "Fish Yasin's Drone Out of the Water", "tage": [2, 6], "attribut": "courage",
     "sg": 13, "lohn": 150, "folgen": [],
     "text": "Yasin's drone has fallen into the water next to the anchor. Six metres down. He pays cash, in notes.",
     "erfolg": "You dive it up. Yasin pays and films you doing it.", "fehlschlag": "You only find the battery. Yasin "
                                                                                       "grudgingly pays half."},
    {"id": "toto_box", "von": "toto", "titel": "Move a Crate for Totò", "tage": [2, 6], "attribut": "cunning", "sg": 13,
     "lohn": 120, "folgen": [], "folgen_fehlschlag": [{"wert": "ruf", "delta": -1}],
     "text": "“Don't look inside, Comandante. Just from the tender into the storeroom. And if Lieutenant Elsa asks: "
             "potatoes.”",
     "erfolg": "Nobody saw a thing. Totò kisses you on both cheeks.", "fehlschlag": "Elsa saw something. Totò pays half "
                                                                                             "anyway – and sweats."},
    {"id": "outboard", "von": "petru", "titel": "A Fisherman's Outboard", "tage": [3, 7], "attribut": "cunning", "sg": 12,
     "lohn": 140, "reparatur": True, "folgen": [{"wert": "ruf", "delta": 1}],
     "text": "Petru's neighbour has an outboard that stutters. Petru recommended you. That's new.",
     "erfolg": "It purrs like new. The fisherman pays and brings fish tomorrow.", "fehlschlag": "It runs, but loudly. Half pay."},
    {"id": "guest_breakfast", "von": "yasin", "titel": "Conjure Up Breakfast for the Guests", "tage": [2, 7], "attribut": "charm",
     "sg": 12, "lohn": 80, "kochen": True, "folgen": [{"wert": "moral", "delta": 1}],
     "text": "Yasin wants eggs Benedict without power. He'll tip if it works. A big tip.",
     "erfolg": "A camping stove, charm and good timing. Yasin tips generously.", "fehlschlag": "The eggs are hard. So is the tip."},
]
# Missionen der Frauen und Ketten (17.10.2026). Frauen zahlen nicht - Erfolg bringt Naehe (Code: handel.job_machen,
# +6 Vertrauen/+4 Begehren, eine Wirkung je Frau und Tag) und oft einen kleinen Nutzen fuers Schiff.
# nach = erst nach ERFOLG dieser Mission; ab_vertrauen = Mindest-Stufe bei der Auftraggeberin.
DORF += [
    {"id": "rosi_cells", "von": "rosi", "titel": "Testing the Battery Cells", "tage": [2, 7], "attribut": "perception", "sg": 11,
     "lohn": 0, "reparatur": True, "folgen": [],
     "text": "Twenty-four cells, a multimeter, a torch. Rosi reads out, you measure – one of them is bad somewhere."},
    {"id": "rosi_bleed", "von": "rosi", "titel": "Bleeding Unit-01", "tage": [3, 7], "attribut": "cunning", "sg": 12,
     "lohn": 0, "reparatur": True, "nach": "rosi_cells", "ab_vertrauen": 2, "folgen": [{"uhr": "reparatur", "delta": 1}],
     "text": "There is air in the diesel line of Unit-01, the old emergency generator, and it has to come out. Rosi holds the torch and swears quietly in Sicilian."},
    {"id": "chiara_coldroom", "von": "chiara", "titel": "Cold Room Inventory", "tage": [2, 7], "attribut": "perception", "sg": 10,
     "lohn": 0, "kochen": True, "folgen": [{"wert": "moral", "delta": 1}],
     "text": "What will keep, and what has to go today? Chiara wants a list before the cold room warms up – and a "
             "meal for everyone out of whatever has to go, before Lola turns it into an experiment."},
    {"id": "chiara_complaint", "von": "chiara", "titel": "Heading Off a Guest Complaint", "tage": [3, 7], "attribut": "charm", "sg": 12,
     "lohn": 0, "nach": "chiara_coldroom", "ab_vertrauen": 2, "folgen": [{"wert": "moral", "delta": 1}],
     "text": "Yasin is threatening a one-star review for the whole crew. Chiara needs someone to slow him down, "
             "nicely."},
    {"id": "sophia_papers", "von": "sophia", "titel": "Taking the Papers to the Coast Guard", "tage": [2, 6], "attribut": "charm", "sg": 10,
     "lohn": 0, "folgen": [{"wert": "ruf", "delta": 1}],
     "text": "Anchoring permit, crew list, one stamp missing. Sophia has sorted the folder – you're the one taking "
             "it over."},
    {"id": "sophia_diesel", "von": "sophia", "titel": "Arranging a Diesel Favour", "tage": [3, 7], "attribut": "charm", "sg": 12,
     "lohn": 0, "nach": "sophia_papers", "ab_vertrauen": 2, "folgen": [],
     "text": "Sophia knows someone who knows someone who has a canister to spare. All she needs is your face."},
    {"id": "lea_chain", "von": "lea", "titel": "Diving to Check the Anchor Chain", "tage": [2, 7], "attribut": "courage", "sg": 11,
     "lohn": 0, "folgen": [{"wert": "moral", "delta": 1}],
     "text": "Lea wants to see whether the anchor really holds. Seven metres, clear water, a patch of sea urchins."},
    {"id": "siri_photos", "von": "siri", "titel": "Photos Without Yasin", "tage": [2, 7], "attribut": "charm", "sg": 11,
     "lohn": 0, "folgen": [],
     "text": "Siri wants pictures where she isn't posing. Just light, water and her. You hold the camera."},
    {"id": "siri_samples", "von": "siri", "titel": "Collecting Sea Samples", "tage": [3, 7], "attribut": "perception", "sg": 11,
     "lohn": 0, "nach": "siri_photos", "ab_vertrauen": 2,
     "folgen": [{"codex": "Siri has collected seagrass samples – she wants to study marine biology. She hasn't told "
                          "anyone yet."}],
     "text": "Glass tubes, a notebook, the swim platform. Siri explains seagrass to you as if it were the most "
             "exciting thing in the world."},
    # Ketten im Dorf: die zweite Mission erst nach Erfolg bei der ersten
    {"id": "alva_diesel", "von": "alva", "titel": "Diesel Under the Bar", "tage": [3, 7], "attribut": "cunning", "sg": 12,
     "lohn": 0, "nach": "alva_kuehlung", "folgen": [],
     "text": "Alva has “something in the cellar”. You'll have to collect it yourself, and in a way Lieutenant Elsa "
             "doesn't see."},
    {"id": "casanova_banner", "von": "casanova", "titel": "Hanging the Festa Banner", "tage": [3, 5], "attribut": "courage", "sg": 10,
     "lohn": 60, "nach": "english_kids", "folgen": [{"wert": "ruf", "delta": 1}, {"item": "festa_invite"}],
     "text": "Twenty metres of fabric, a church tower, a ladder from 1962. In return Madame Casanova offers you an "
             "invitation to the festa."},
    {"id": "toto_night", "von": "toto", "titel": "Night Run with Totò's Cousin", "tage": [3, 6], "attribut": "courage", "sg": 13,
     "lohn": 200, "nach": "toto_box", "folgen": [], "folgen_fehlschlag": [{"wert": "ruf", "delta": -1}],
     "text": "A dinghy from Bastia, no lights, an hour after midnight. “You only steer, Comandante.”"},
]


# ======================================================================== Missionsausbau (18.10.2026)
# Duc: Fetch-Missionen mit Teilen (art "teil", Besorgungstasche). Jede Mission muss vier Fragen beantworten:
# Warum will die Person das (aus ihrer Geschichte)? Warum fragt sie Duc? Warum kann sie es nicht kaufen oder selbst
# machen? Was ist die Huerde? Kein Kitsch ohne Grund. Abgaben sind sichere Schritte ohne Wurf (probe=False), das
# Koennen steckt in eigenen Schritten - so geht bei einem Fehlschlag kein gekauftes Teil verloren.
# ton: witzig (Anime-Humor eingeschlossen), wholesome, spannend, ernst - Mischung wird beim Bau ausgegeben.


def M(id, von, titel, tage, text, erfolg, fehlschlag="", ton="wholesome", **kw):
    m = {"id": id, "von": von, "titel": titel, "tage": list(tage), "lohn": kw.pop("lohn", 0),
         "folgen": kw.pop("folgen", []), "text": text, "erfolg": erfolg, "ton": ton}
    if fehlschlag:
        m["fehlschlag"] = fehlschlag
    m.update(kw)
    return m


def ABGABE(id, von, titel, tage, braucht, text, erfolg, ton="wholesome", **kw):
    return M(id, von, titel, tage, text, erfolg, ton=ton, probe=False, braucht=braucht, **kw)


AUSBAU = [
    # ---------------------------------------------------------------- Rosi: ein Schild fuer die Werkstatt (Petru)
    ABGABE("petru_schild_1", "petru", "A Sign for Rosi: The Board", [3, 7], "eichenbrett",
           "Yesterday Petru saw Rosi standing outside his workshop. She looked at the empty board above his door for "
           "a long time and said, “Scuderi & Figlie. That's what Papa would have called it.” Petru wants to carve "
           "her one. He only carves oak, and the only oak in the village belongs to Alva.",
           "Petru knocks on the wood, listens, and nods. “Good. Now we saw.”", ton="ernst",
           folgen=[{"vertrauen": ["petru", 4]}]),
    M("petru_schild_2", "petru", "A Sign for Rosi: Carving", [3, 7],
      "Petru chalks the letters of Rosi's sign onto the oak board, and his hand shakes as he does it. The fine work should be done by someone "
      "whose hands are still steady.",
      "The edges are clean. Petru runs his thumb along them. “Only the brass is missing.”",
      "A splinter tears out, right in the S. Petru planes the spot smooth. “Tomorrow. Slower.”", ton="ernst",
      attribut="cunning", sg=13, reparatur=True, werkzeug=["werkzeugkoffer", "multitool"], nach="petru_schild_1"),
    ABGABE("petru_schild_3", "petru", "A Sign for Rosi: The Letters", [3, 7], "messingbuchstaben",
           "On this island you can only get brass letters from one man, a man who never asks what they're for. Petru "
           "doesn't say his name. He just looks over at the yacht.",
           "Petru screws the last letter in place and slides the sign across the workbench to you. “You give it to "
           "her. She won't take anything from me.”", ton="ernst", nach="petru_schild_2",
           folgen=[{"item": "rosi_schild"}, {"vertrauen": ["petru", 4]}]),
    # ---------------------------------------------------------------- Chiara: eine Tasse (Lola)
    M("lola_tasse_1", "lola", "A Mug for Chiara: The Colours", [2, 7],
      "For three weeks Chiara has been drinking out of guest mugs, because Lola “somehow lost” the crew mugs. Lola "
      "wants to make peace and make Chiara a mug of her own on a potter's wheel. For that, someone has to find out "
      "which colours Chiara likes without Chiara noticing why. Lola can't do it herself. Chiara isn't speaking to "
      "her.",
      "Dark blue with a thin gold rim, like the stripes on her uniform. Chiara noticed nothing. Lola squeals quietly "
      "into a tea towel.",
      "Chiara narrows her eyes. “Why do you want to know?” You change the subject. Lola counts it as a partial "
      "success.",
      ton="witzig", attribut="charm", sg=12),
    ABGABE("lola_tasse_2", "lola", "A Mug for Chiara: The Clay", [2, 7], "tonerde",
           "Petru has an old potter's wheel and lets Lola use it, as long as she brings her own clay and touches "
           "nothing. Lola always touches everything. That's why you are the one taking the clay to Petru.",
           "Petru puts the sack down next to the wheel and points at you, not at Lola.", ton="witzig",
           nach="lola_tasse_1"),
    M("lola_tasse_3", "lola", "A Mug for Chiara: Throwing", [2, 7],
      "Lola works the clay for Chiara's mug on Petru's wheel, you hold the shape, Petru watches and says nothing. The rim has to come out straight or it'll "
      "drip. Chiara hates drips.",
      "The mug is crooked, but only a little. Lola paints the gold rim with her tongue between her teeth. You're "
      "supposed to give it to Chiara. “If it's from me, she'll think there's weed in it.”",
      "The wheel spins out and the clay flies against Petru's wall. Petru says a Corsican word. Again tomorrow.",
      ton="wholesome", attribut="perception", sg=12, reparatur=True, nach="lola_tasse_2",
      folgen=[{"item": "chiara_tasse"}, {"vertrauen": ["lola", 4]}]),
    # ---------------------------------------------------------------- Lea: ein Tauchcomputer (Elsa)
    M("elsa_fund_1", "elsa", "A Lost-and-Found for Lea", [2, 7],
      "A dive computer has been sitting in Elsa's lost-property box for a year. Nobody has claimed it. Elsa has seen "
      "Lea dive without one, and it worries her. She can only release it with a form and a reason she can defend to "
      "Ajaccio.",
      "“Safety on board a disabled vessel.” Elsa stamps the form twice. “It needs a battery. And a strap. I'm a "
      "gendarme, not a watchmaker.”",
      "Elsa pushes the form back. “That sounds as if you wanted a present. I don't give presents. Tomorrow.”",
      ton="ernst", attribut="charm", sg=13),
    ABGABE("elsa_fund_2", "elsa", "A Lost-and-Found for Lea: The Battery", [2, 7], "uhrenbatterie",
           "The dive computer is dead. Elsa opens it with a tiny screwdriver from her uniform vest. She doesn't have "
           "the right button cell. In the village only Alva has things like that.",
           "The display flickers and shows 0.0 metres. Elsa smiles, very briefly.", ton="ernst", nach="elsa_fund_1"),
    ABGABE("elsa_fund_3", "elsa", "A Lost-and-Found for Lea: The Strap", [2, 7], "armband",
           "The dive computer's old strap has rotted away in the salt water. You can only get a seaworthy one through the shipping "
           "company's supplies.",
           "Elsa puts the dive computer in your hand. “You give it to her. If I do it, it's bribery.”",
           ton="wholesome", nach="elsa_fund_2", folgen=[{"item": "lea_tauchcomputer"}, {"vertrauen": ["elsa", 4]}]),
    # ---------------------------------------------------------------- Alva: die Kastagnetten (Lola)
    M("lola_kast_1", "lola", "Alva's Castanets: Listening", [3, 7],
      "After three glasses Alva told Lola that her grandmother's castanets are lying broken in a drawer. She would "
      "never hand them over. Except to someone who spends an evening listening to who that grandmother was. Lola "
      "reckons that only works with a meal that tastes of home.",
      "You cook, Alva eats, and at some point she takes out the drawer. Two halves, wrapped in a handkerchief. “If "
      "you break them, o figliolu, I'll kill you.”",
      "The food is good, but not good enough for memories. Alva talks about the weather. Lola sighs.",
      ton="wholesome", attribut="perception", sg=12, kochen=True, werkzeug=["kochmesser"]),
    ABGABE("lola_kast_2", "lola", "Alva's Castanets: The Glue", [3, 7], "holzleim",
           "Petru says old wood takes bone glue, not modern glue. On this island bone glue belongs to somebody who "
           "has everything else as well.",
           "Petru sniffs the glue pot and pulls a face. That means: right.", ton="witzig", nach="lola_kast_1"),
    M("lola_kast_3", "lola", "Alva's Castanets: Gluing", [3, 7],
      "Alva's castanets, two halves, a hairline crack, sixty years of flamenco. Petru warms the glue, you fit the pieces together. If "
      "one slips, they'll never sound right again.",
      "A dry clack, like it used to be. Petru puts the castanets in your hand. “For her. Not from me.”",
      "One piece slips. Petru loosens the glue again with hot water. Tomorrow.",
      ton="wholesome", attribut="cunning", sg=13, reparatur=True, werkzeug=["werkzeugkoffer", "multitool"],
      nach="lola_kast_2", folgen=[{"item": "alva_kastagnetten"}]),
    # ---------------------------------------------------------------- Totò: San Gennaro (Alva)
    M("alva_gennaro_1", "alva", "A Saint for Totò", [3, 7],
      "Totò's San Gennaro from Naples fell off the shelf on the night of the fire on board. Since then Totò hasn't "
      "laughed, and a Totò who doesn't laugh is bad for business. Alva wants to get him a new one. In the whole of "
      "Corsica only his cousin in Bastia has a figure like that, and he delivers at night, past the coast guard.",
      "A dinghy, no lights, a parcel in newspaper. The saint has arrived, only unfortunately unpainted and very grey.",
      "Elsa's searchlight sweeps the water. The cousin turns away. The village talks.",
      ton="spannend", attribut="cunning", sg=13, folgen_fehlschlag=[{"wert": "ruf", "delta": -1}]),
    ABGABE("alva_gennaro_2", "alva", "A Saint for Totò: Gold", [3, 7], "goldfarbe",
           "Alva wants to paint the saint herself. “Golden, like in Naples. Golden like a lottery win.” She has the "
           "gold paint on her own shelf, but she doesn't pay for presents for Totò. On principle.",
           "Alva paints until the saint shines like a slot machine. “Perfect. Now he just has to look at it.”",
           ton="witzig", nach="alva_gennaro_1"),
    M("alva_gennaro_3", "alva", "A Saint for Totò: The Handover", [3, 7],
      "Alva says you never just hand a Neapolitan something. You give Totò his new saint over a meal. One that tastes like "
      "his mother's: Genovese, six hours of onions.",
      "Totò tastes it, puts his fork down and stares at the figure. Then he laughs, so loudly that Alva grabs the "
      "glasses. You'd better give him the figure yourself.",
      "The onions burn. Totò eats it anyway and praises you. He's a very bad liar. Again tomorrow.",
      ton="witzig", attribut="perception", sg=12, kochen=True, werkzeug=["kochmesser"], nach="alva_gennaro_2",
      folgen=[{"item": "toto_gennaro"}, {"vertrauen": ["alva", 4]}]),
    # ---------------------------------------------------------------- Sophia: ein Fueller (Lea)
    M("lea_fueller_1", "lea", "A Pen for Sophia: The Engraver", [2, 7],
      "Lea wants to give her sister a fountain pen. Engraved with her own name, for what Sophia only writes for "
      "herself. The only engraver for miles is known to Madame Casanova, and she only gives out addresses once she "
      "has been admired for long enough.",
      "Madame Casanova writes the address on a napkin and signs it as if it were an autograph. Lea throws her arms "
      "around your neck.",
      "Madame Casanova talks to you about her festa for two hours and forgets the address. Lea laughs until she gets "
      "hiccups.",
      ton="witzig", attribut="charm", sg=12),
    ABGABE("lea_fueller_2", "lea", "A Pen for Sophia: The Blank", [2, 7], "fueller_rohling",
           "The engraver in Ajaccio only engraves a blank pen you bring yourself. Blank pens are in the shipping company's "
           "supplies, which means Megan.",
           "Two days later the pen arrives on the post boat in a velvet case. Lea presses it into your hand. “You "
           "give it to her. I'd cry.”", ton="wholesome", nach="lea_fueller_1",
           folgen=[{"item": "sophia_fueller"}], persoenlich=True),
    # ---------------------------------------------------------------- Siri: ein Ratgeber fuer ihren Vater (Petru)
    ABGABE("siri_ratgeber_1", "siri", "A Book for Siri's Father: The Net Twine", [3, 7], "netzgarn",
           "Siri's father has fished off Trøndelag for forty years. Petru reminds her of him so much she can hardly "
           "look at him. She wants to write down his stories about fishing in Corsica, for her father. Petru doesn't "
           "talk to influencers. Not until his nets are mended, and he doesn't take money.",
           "Petru weighs the roll of twine in his hand and points at the chair beside him. That's an invitation.",
           ton="wholesome"),
    M("siri_ratgeber_2", "siri", "A Book for Siri's Father: The Conversation", [3, 7],
      "Petru talks when you're quiet. Siri isn't good at being quiet. You're to ask the questions about his fishing, so that Petru "
      "doesn't notice it's an interview, and so that it doesn't annoy him.",
      "Petru talks about tuna, storms and his father. Siri takes notes for three hours without a single photo. In "
      "the evening she binds the pages and gives them to you. “Keep it safe until I go home. I lose everything.”",
      "One question too many. Petru gets up and goes to fetch nets he doesn't need. Siri looks at you for a long "
      "time.",
      ton="ernst", attribut="empathy", sg=13, nach="siri_ratgeber_1", persoenlich=True,
      folgen=[{"item": "siri_ratgeber"}, {"vertrauen": ["petru", 4]}]),
    # ---------------------------------------------------------------- Elsa: ein Strafzettelblock (Casanova)
    M("casanova_elsa_1", "casanova", "A Present for the Lieutenant: The Archive", [2, 7],
      "Elsa has been at the Cala d'Orsu post for five years. The village wants to thank her, but she won't accept "
      "anything. It would all be bribery. Madame Casanova has an idea: Elsa's own tickets from five years, bound "
      "like a book. They're somewhere in the town archive, unsorted, between fishing licences from 1974.",
      "Three hundred and twelve tickets, in order. One of them is for Madame Casanova herself, for fireworks without "
      "a permit. She insists it goes at the front.",
      "You find the fishing licences from 1974. And nothing else. Madame Casanova calls it chapter one.",
      ton="witzig", attribut="perception", sg=12),
    ABGABE("casanova_elsa_2", "casanova", "A Present for the Lieutenant: The Linen", [2, 7], "buchbinde_leinen",
           "Elsa's tickets have to be bound in linen, says Madame Casanova, like a state document. Only Alva has linen, and "
           "Madame Casanova hasn't spoken to Alva since the quarrel over the village shop.",
           "Madame Casanova strokes the linen and whispers, “Dignified.”", ton="witzig", nach="casanova_elsa_1"),
    M("casanova_elsa_3", "casanova", "A Present for the Lieutenant: Binding", [2, 7],
      "Elsa's tickets, three hundred and twelve sheets, one spine, an awl and thread. Meanwhile Madame Casanova gives a speech "
      "nobody asked for.",
      "A thick block bound in linen, with Elsa's initials. Madame Casanova cries a little. “You give it to her. I'd "
      "make a speech.”",
      "The thread snaps at sheet two hundred. Madame Casanova calls it a trial sent by fate.",
      ton="witzig", attribut="perception", sg=12, reparatur=True, werkzeug=["werkzeugkoffer", "multitool"],
      nach="casanova_elsa_2", folgen=[{"item": "elsa_strafzettelblock"}, {"wert": "ruf", "delta": 1}]),
    # ---------------------------------------------------------------- Megan: eine Karte der Crew (Lola)
    M("lola_megan_1", "lola", "A Card for Megan: The Signatures", [3, 6],
      "Lola says Megan has a glass office, and the only things anyone ever sends her are reports. “Everyone hates "
      "the boss, mate. I reckon that's lonely.” She wants to send Megan a card signed by the whole crew. The "
      "problem: half the crew would rather jump overboard.",
      "Eleven signatures. Chiara's is very small, Totò's very big, Rosi's is a drawing of Unit-01. Lola sticks a "
      "heart next to them that nobody asked for.",
      "Chiara refuses, Rosi signs with “No”. Lola says that sort of counts too.",
      ton="witzig", attribut="charm", sg=13),
    ABGABE("lola_megan_2", "lola", "A Card for Megan: The Frame", [3, 6], "bilderrahmen",
           "“Without a frame Megan bins that card. With a frame she has to hang it up. That's science.” Only Alva has frames.",
           "Lola frames the card, crookedly, and hands it to you. “You give it to her. She doesn't believe I can "
           "read.”",
           ton="wholesome", nach="lola_megan_1", folgen=[{"item": "megan_crewkarte"}, {"vertrauen": ["lola", 4]}]),
    # ---------------------------------------------------------------- Einzelne Besorgungen und Gefallen
    M("toto_tabak", "toto", "Tobacco for Petru", [3, 7],
      "For weeks Petru has been smoking something that smells of hay. His tobacco, Bastia Noir, only comes through "
      "Totò's cousin. Totò wants to get it for him, because years ago Petru pulled the cousin out of the water. He "
      "won't pay for the run on his own, and Petru mustn't know who it's from.",
      "Totò puts the tin in your hand. “From you. If Petru finds out it's from me, he'll thank me. I can't take "
      "that.”", ton="wholesome", probe=False, preis=40, folgen=[{"item": "petru_tabak"}]),
    M("siri_lakritz", "siri", "Liquorice for Holm", [3, 7],
      "Siri has a bag of salty Norwegian liquorice in her suitcase. Holm loves the stuff, the whole crew knows it. "
      "Siri doesn't dare send it to the Captain in hospital; in three weeks they've barely exchanged two sentences. "
      "Elsa is going to Ajaccio tomorrow. Someone has to give Siri some courage and ask Elsa.",
      "Elsa takes the bag with a nod. In the evening a message comes from the hospital, just one word: “Takk.” Siri "
      "reads it five times.",
      "Siri gets cold feet and nervously eats half the bag. By tomorrow it's been refilled.",
      ton="wholesome", attribut="empathy", sg=11, folgen=[{"vertrauen": ["holm", 8]}]),
    M("yasin_brille", "yasin", "Yasin's Sunglasses", [2, 6],
      "Yasin's gold sunglasses slipped off the swim platform while he was filming. They're the one thing he never "
      "films: a present from his father. He pays cash, and he doesn't like asking. Eight metres, a current in the "
      "afternoon.",
      "You find them between two rocks. Yasin isn't there when you surface. Give them to him yourself.",
      "The current pushes you away. You see something golden but can't reach it. Tomorrow, at slack water.",
      ton="spannend", attribut="courage", sg=14, lohn=120, folgen=[{"item": "yasin_goldbrille"}]),
    # ---------------------------------------------------------------- Persoenlich (Begehren)
    M("chiara_sterne", "chiara", "Night Watch with Chiara", [3, 7],
      "Chiara hasn't been able to sleep since the fire on board. She asks you to stand the night watch with her and "
      "explain the stars to her. Her grandfather always promised to and never got round to it. She wouldn't ask "
      "anyone else.",
      "You find the Plough, Cassiopeia and a satellite that Chiara declares to be a star. She falls asleep on the "
      "bench. You let her.",
      "Clouds. You can't see anything, and Chiara talks about work instead. Maybe it'll be clear tomorrow.",
      ton="ernst", attribut="perception", sg=12, persoenlich=True),
    M("rosi_arancini", "rosi", "Arancini Like Nonna's", [3, 7],
      "Rosi's nonna died last winter. She never wrote down the recipe for her arancini, and Rosi can't get them "
      "right. She doesn't want to try again on her own.",
      "You change the rice twice and the saffron once. On the third attempt Rosi stops, chews and says nothing. Then "
      "she eats three in a row.",
      "The balls fall apart in the pan. Rosi laughs and cries a little at the same time. Tomorrow.",
      ton="ernst", attribut="perception", sg=12, kochen=True, werkzeug=["kochmesser"], persoenlich=True),
    M("sophia_kapitel", "sophia", "Sophia's First Chapter", [4, 7],
      "Sophia puts twelve pages in front of you. Something of her own, not for a publisher. She wants an honest "
      "opinion, not a nice one. Anyone who only flatters her never gets to read another line.",
      "You tell her what works and what doesn't. She cuts two pages without arguing. Then she asks whether you'd "
      "like to read the second chapter too.",
      "You're too polite. Sophia notices at once, takes the pages back and smiles kindly. That's worse.",
      ton="ernst", attribut="empathy", sg=13, persoenlich=True),
    # ---------------------------------------------------------------- Lola: Paella fuer die Crew
    ABGABE("lola_paella_1", "lola", "Paella for the Crew: Saffron", [2, 7], "safran",
           "Lola wants to make the crew a paella, so that after this week everyone sits at one table again. She has "
           "never made one. “It's basically fancy risotto, how hard can it be.” Without real saffron it'll be yellow "
           "mush, says Chiara. Lola wants to prove her wrong.",
           "Lola holds the little tin up to the light like a gemstone. “Mate. That's not a spice, that's a "
           "personality.”",
           ton="witzig"),
    M("lola_paella_2", "lola", "Paella for the Crew: Cooking", [2, 7],
      "A pan as big as a lifebuoy, a gas burner, and Lola, who wants to stir every two minutes. You don't stir a "
      "paella. Someone has to stop her.",
      "The crust crackles. The crew eats in silence, then very loudly. Chiara takes seconds and says nothing. Lola "
      "counts it as a win.", "Lola stirs. It turns into risotto. The crew eats it anyway.",
      ton="witzig", attribut="perception", sg=12, kochen=True, werkzeug=["kochmesser"], nach="lola_paella_1",
      folgen=[{"wert": "moral", "delta": 1}, {"vertrauen": ["lola", 4]}]),
    # ---------------------------------------------------------------- Megan per Video: Ducs Beruf
    M("megan_esg", "megan", "A Short ESG Report for Megan", [2, 7],
      "The investors want one page on how sustainable a stranded solar yacht is. Megan knows you do this for a "
      "living. She doesn't ask. She orders, with a deadline of this evening.",
      "One page, three figures, not one word too many. Megan reads it on video, is silent, and then says, "
      "“Annoyingly good.”",
      "Megan strikes out half and sends the rest back. “I asked for a report, not a poem.”",
      ton="ernst", attribut="perception", sg=13, lohn=200),
    M("megan_lieferkette", "megan", "Megan's Laundry Supplier", [3, 7],
      "The fleet's new laundry supplier calls itself climate-neutral. Megan wants to know whether that's true before "
      "she signs, and from someone who doesn't work for the supplier.",
      "The certificates belong to a different factory. Megan smiles slowly. “Checkmate.” She pays at once.",
      "You find nothing solid. Megan still doesn't sign. “Then keep looking.”",
      ton="spannend", attribut="cunning", sg=14, lohn=150, nach="megan_esg"),
    # ---------------------------------------------------------------- Elsa: eine Antenne fuer den Posten
    ABGABE("elsa_antenne_1", "elsa", "Elsa's Antenna: The Cable", [3, 7], "antennenkabel",
           "Since the last storm Elsa's radio no longer reaches Ajaccio. The old antenna cable has worn through. The "
           "gendarmerie applied for a new one eleven months ago. The shipping company has some, and Elsa doesn't ask "
           "a shipping company for anything.",
           "Elsa takes the cable and inspects the reel. “You didn't get this from me.”", ton="spannend", nach="radio_elsa"),
    M("elsa_antenne_2", "elsa", "Elsa's Antenna: Up on the Roof", [3, 7],
      "The new cable goes up to the antenna on the roof of the post, four metres above the harbour. Wind from the north-west, gusts. "
      "Elsa holds the ladder and says she would climb up herself if she were allowed to.",
      "Crackling, then Ajaccio, crystal clear. Elsa salutes, half joking, half not.",
      "A gust rips the cable out of your hand. Elsa catches you by the ankle. Tomorrow, with less wind.",
      ton="spannend", attribut="courage", sg=12, reparatur=True, werkzeug=["werkzeugkoffer", "multitool"],
      lohn=100, nach="elsa_antenne_1", folgen=[{"wert": "ruf", "delta": 1}]),
    # ---------------------------------------------------------------- Kueche: Festa und Posten
    M("casanova_buffet", "casanova", "A Tasting Menu for the Festa", [3, 5],
      "Madame Casanova wants a buffet at the festa, “from all over the world, but Corsican”. The jury is her, her "
      "mother and the priest. The village cook has pulled out because she accused him of having “vision”. She has "
      "heard you can cook, and she's already announcing it all over the village.",
      "The priest takes three helpings. The mother says, “Hm.” Madame Casanova declares you the official cook of the "
      "festa, with a sash.",
      "The mother pushes her plate away. Madame Casanova announces that this was part of the plan.",
      ton="witzig", attribut="perception", sg=12, kochen=True, werkzeug=["kochmesser"], lohn=120,
      folgen=[{"wert": "ruf", "delta": 1}]),
    M("elsa_nachtessen", "elsa", "Food for the Night Patrol", [3, 7],
      "Since the fire on board Elsa and her two men have been on patrol every night, eating cold tins on the boat. She "
      "won't take money or presents. But a hot meal for the crew counts as rations, she says, and she's allowed to "
      "accept that. If it's good.",
      "Three fewer empty tins. Elsa's men call you “Chef”. Elsa says nothing and takes the box along again the next "
      "evening.",
      "It's lukewarm by the time the boat casts off. Elsa thanks you anyway, very formally. That's worse than "
      "criticism.",
      ton="wholesome", attribut="perception", sg=12, kochen=True, werkzeug=["kochmesser"],
      folgen=[{"vertrauen": ["elsa", 4]}]),
    # ---------------------------------------------------------------- Alvas Kuehlung: ein vierter Weg
    ABGABE("alva_kuehlung_relais", "alva", "Cooling: Fit a Relay", [2, 7], "relais",
           "The compressor only needs a new relay. Fitting it is easy; getting it isn't. On this island only one man "
           "has things like that.",
           "Click, hum, cold air. Alva pays and gives you a myrtle liqueur on top.",
           ton="wholesome", gruppe="alva_kuehlung", lohn=80, folgen=[{"wert": "ruf", "delta": 1}]),
]

# Ton der bestehenden Missionen (vor dem Ausbau ohne Ton)
TON = {"lola_kochkurs": "witzig", "alva_kassenbuch": "witzig", "casanova_plan": "witzig", "petru_motor_1": "ernst",
       "petru_motor_2": "wholesome", "alva_kuehlung_eis": "wholesome", "alva_kuehlung_reparatur": "spannend",
       "alva_kuehlung_toto": "witzig", "toto_gefallen": "spannend", "rosi_ersatzbatterie": "wholesome",
       "nets": "wholesome", "radio_elsa": "ernst", "english_kids": "witzig", "drone": "spannend", "toto_box": "spannend",
       "outboard": "wholesome", "guest_breakfast": "witzig", "rosi_cells": "wholesome", "rosi_bleed": "spannend",
       "chiara_coldroom": "ernst", "chiara_complaint": "witzig", "sophia_papers": "ernst", "sophia_diesel": "spannend",
       "lea_chain": "spannend", "siri_photos": "wholesome", "siri_samples": "wholesome", "alva_diesel": "spannend",
       "casanova_banner": "witzig", "toto_night": "spannend"}
TOENE = ("witzig", "wholesome", "spannend", "ernst")


# Mehrere Wege: Titel und Lage der Gruppe (Wege-Ansicht im Client) - steht an jedem Weg der Gruppe
GRUPPEN = {
    "alva_kuehlung": {"titel": "The Cooling Has Packed Up",
                      "text": "The compressor in Alva's cellar is dead, and all the festa stock is sweating. "
                              "Something has to happen by this evening."},
}
for _m in MISSIONEN + DORF + AUSBAU:
    _m.setdefault("ton", TON.get(_m["id"], ""))
    if _m.get("gruppe") in GRUPPEN:
        _m["gruppe_titel"] = GRUPPEN[_m["gruppe"]]["titel"]
        _m["gruppe_text"] = GRUPPEN[_m["gruppe"]]["text"]

# Persoenlich (Paket 1): nur diese Frauen-Missionen geben Begehren - sie beruehren ihr Leben, nicht nur Arbeit.
# Weitere persoenliche Missionen fuer Chiara, Rosi und Sophia kommen mit dem Missions-Ausbau.
PERSOENLICH = {"siri_photos", "siri_samples", "lea_chain"}
for _m in DORF:
    if _m["id"] in PERSOENLICH:
        _m["persoenlich"] = True


def pruefe(liste):
    fehler = []
    ids = [m["id"] for m in liste]
    for m in liste:
        k = m["id"]
        if ids.count(k) > 1:
            fehler.append("doppelte id %s" % k)
        if m["von"] not in PERSONEN:
            fehler.append("%s: von %s" % (k, m["von"]))
        mit_probe = m.get("probe", True) is not False
        if mit_probe and m.get("attribut") not in ATTRIBUTE:
            fehler.append("%s: attribut %s" % (k, m.get("attribut")))
        if mit_probe and not isinstance(m.get("sg"), int):
            fehler.append("%s: sg fehlt" % k)
        if not mit_probe and (m.get("werkzeug") or m.get("reparatur") or m.get("kochen")):
            fehler.append("%s: ohne Probe gibt es keinen Vorteil" % k)
        if m.get("preis") is not None and (not isinstance(m["preis"], int) or m["preis"] <= 0):
            fehler.append("%s: preis" % k)
        if m.get("gruppe") and not m.get("gruppe_titel"):
            fehler.append("%s: gruppe %s ohne Eintrag in GRUPPEN" % (k, m["gruppe"]))
        if m.get("gruppe") and sum(1 for x in liste if x.get("gruppe") == m["gruppe"]) < 2:
            fehler.append("%s: gruppe %s hat nur einen Weg" % (k, m["gruppe"]))
        if m.get("persoenlich") and m["von"] not in FRAUEN:
            fehler.append("%s: persoenlich nur bei den Frauen" % k)
        if not (1 <= m["tage"][0] <= m["tage"][1] <= 7):
            fehler.append("%s: tage" % k)
        if (m.get("reparatur") or m.get("kochen")) and m["sg"] < 12 and m not in DORF:   # DORF: alte Werte, so belassen
            fehler.append("%s: Probe mit Persona-Vorteil unter SG 12" % k)
        if m.get("nach") and m["nach"] not in ids and m["nach"] not in {x.get("gruppe") for x in liste}:
            fehler.append("%s: nach %s unbekannt" % (k, m["nach"]))
        for f in m["folgen"]:
            if "vertrauen" in f and f["vertrauen"][0] not in PERSONEN:
                fehler.append("%s: vertrauen %s" % (k, f))
        if "holm" == m["von"] and m["tage"][1] > 1:
            fehler.append("%s: Holm nur an Tag 1" % k)
        if m.get("ton") not in TOENE:
            fehler.append("%s: ton %s" % (k, m.get("ton")))
        if m.get("braucht") and mit_probe:
            fehler.append("%s: Abgabe mit Wurf - bei Fehlschlag waere das Teil verloren" % k)
    try:
        g = json.load(open(os.path.join(EDEN, "module", "eden_rise", "gegenstaende.json"), encoding="utf-8"))
        bekannt = {i["id"] for i in g["items"]} | set(json.load(open(os.path.join(EDEN, "module", "eden_rise", "modul.json"),
                                                                   encoding="utf-8"))["items"])
        fehler += ["%s: item %s unbekannt" % (m["id"], f["item"]) for m in liste for f in m["folgen"]
                   if "item" in f and f["item"] not in bekannt]
        fehler += ["%s: braucht %s unbekannt" % (m["id"], m["braucht"]) for m in liste
                   if m.get("braucht") and m["braucht"] not in bekannt]
        arten = {i["id"]: i["art"] for i in g["items"]}
        fehler += ["%s: braucht %s - %s landet nie im Inventar" % (m["id"], m["braucht"], arten.get(m["braucht"]))
                   for m in liste if m.get("braucht") and arten.get(m["braucht"]) in ("ressource", "verbrauch", "gericht")]
        teile = [i["id"] for i in g["items"] if i["art"] == "teil"]
        fehler += ["Teil %s wird von keiner Mission gebraucht" % t for t in teile
                   if not any(m.get("braucht") == t for m in liste)]
        fehler += ["%s: werkzeug %s ist kein Werkzeug/Gluecksbringer" % (m["id"], w) for m in liste
                   for w in m.get("werkzeug") or [] if arten.get(w) not in ("werkzeug", "gluecksbringer")]
        fehler += ["%s: werkzeug %s unbekannt" % (m["id"], w) for m in liste for w in m.get("werkzeug") or []
                   if w not in bekannt]
    except FileNotFoundError:
        fehler.append("gegenstaende.json fehlt - erst gegenstaende_eden_rise.py laufen lassen")
    return fehler


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    alle = MISSIONEN + DORF + AUSBAU
    f = pruefe(alle)
    for x in f:
        print("FEHLER", x)
    if f:
        sys.exit(1)
    json.dump({"_hinweis": "Gebaut aus werkzeuge\\eden_rise\\missionen_eden_rise.py - dort aendern (eigene Missionen + Dorf/Crew).",
               "missionen": alle}, open(ZIEL, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    import collections
    print("geschrieben:", ZIEL, "-", len(alle), "Missionen")
    ton = collections.Counter(m["ton"] for m in alle)
    print("Ton:", ", ".join("%s %d (%d %%)" % (t, ton[t], round(100 * ton[t] / len(alle))) for t in TOENE))
    st = collections.Counter("Handwerk" if m.get("reparatur") else "Küche" if m.get("kochen") else
                             "Abgabe/Geld" if m.get("probe") is False else
                             {"perception": "Köpfchen", "cunning": "Köpfchen", "charm": "Charme", "empathy": "Charme",
                              "courage": "Mut", "strength": "Kraft"}[m["attribut"]] for m in alle)
    print("Stärken:", dict(st))
    print("Abgaben mit Teil:", sum(1 for m in alle if m.get("braucht")), "| Einzigartige als Lohn:",
          sum(1 for m in alle for f in m["folgen"] if "item" in f))
