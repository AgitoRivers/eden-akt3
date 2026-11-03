# -*- coding: utf-8 -*-
"""English rewrite · package 4: missions (missionen_eden_rise.py), 25.10.2026.

Texts addressed by line of the literal (several on one line = list in column order). Fields: titel, text, erfolg,
fehlschlag, codex (dict keys and M()/ABGABE() arguments). Canon fixes on the way (docs/wiki): Siri's father fishes off
Trøndelag (K3), the liquorice is Norwegian and Holm says "Takk", Chiara's grandfather (not father) and the stars,
no decorative Italian (K9: "Fratello", "Perfetto" out).

    python werkzeuge\\englisch\\missionen_paket.py     -> docs\\abnahme\\englisch_missionen.json (spec for uebernehmen.py)
"""
import ast, json, os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(os.path.dirname(HIER))
QUELLE = os.path.join(EDEN, "werkzeuge", "eden_rise", "missionen_eden_rise.py")
FELDER = {"titel", "text", "erfolg", "fehlschlag", "codex"}
POS = {"M": {2: "titel", 4: "text", 5: "erfolg", 6: "fehlschlag"}, "ABGABE": {2: "titel", 5: "text", 6: "erfolg"}}

NEU = {
    26: "Cooking Class: Lola Learns Thịt Kho",
    28: "Lola wants to know how to caramelise pork belly without setting the galley on fire. She has prepared notes. "
        "One of them just says “don't set on fire”.",
    30: "Lola's first thịt kho gleams. She hugs you with the wooden spoon still in her hand and gives you her last jar of "
        "Vegemite.",
    31: "The sugar turns black. Lola laughs so hard she has to sit down.",
    33: "Alva's Accounts",
    35: "Alva's accounts are a shoebox full of receipts. The tax office wants figures by the end of the month. She puts a "
        "myrtle liqueur in front of you and slides the box across the bar.",
    37: "Three columns, one total, and a forgotten supplier who owes her money. Alva kisses you on the forehead.",
    38: "The figures almost add up. Alva pays half and calls you “Commercialista” anyway.",
    39: "A Sustainability Plan for the Festa",
    42: "Madame Casanova has heard that you're a sustainability consultant. She wants the greenest festa in Corsica. With "
        "fireworks. And disposable barbecues. And four hundred balloons.",
    44: "Deposit cups, fairy lights instead of torches, fish from Petru. She calls it her idea and gives you her confetti "
        "cannon.",
    45: "The balloons stay. The disposable barbecues don't. Half a victory and half the pay.",
    47: "Petru's Old Boat Engine",
    49: "In Petru's workshop an engine sits under a tarpaulin. A Volvo Penta, older than you. It belonged to his father. "
        "Petru pulls the tarpaulin off and says nothing.",
    51: "The engine turns over for the first time in years. Petru puts a hand on your shoulder and leaves it there.",
    52: "It coughs and dies. Petru nods. “Tomorrow.”",
    53: "The First Trip Out",
    56: "Petru wants to hear the engine on the water. In his father's boat, with you at the helm, once around the harbour "
        "wall.",
    57: "You head out. Petru tells a whole story, with a beginning and an end. At the jetty he gives you his father's "
        "hammer.",
    58: "Just short of the harbour wall the engine quits. You row back. Petru laughs. Nobody has ever heard that before.",
    60: "Cooling: Fetch Ice",
    62: "Totò has block ice in the storeroom. That saves the festa stock for today – tomorrow it starts sweating again.",
    63: "You haul two blocks of ice down to Alva's cellar. “Today you're my hero. Tomorrow we'll see.”",
    64: "Cooling: Repair It Yourself",
    67: "The compressor is dead, and all the festa stock is sweating. Take it apart, swap the relay – if it works, the "
        "cooling runs for good and Alva pays.",
    69: "The compressor hums again. Alva puts a myrtle liqueur in front of you and pays without haggling.",
    70: "A spark, a bang, silence. Alva sighs. “Ice, then. Or Totò.”",
    71: "Cooling: Ask Totò for a Relay",
    73: "Totò “happens” to have exactly the relay Alva's compressor needs. He doesn't want money. He wants you to "
        "remember.",
    74: "The relay fits. Alva is happy. Totò winks at you. “You owe me a little something, Comandante.”",
    75: "Totò's Little Crate",
    78: "“Remember the relay? I have a little crate that needs to get past Elsa's boat tonight.”",
    79: "The crate is across, Elsa saw nothing. Totò hugs you like a brother. You're square.",
    80: "Elsa's lamp sweeps over the dinghy. Nobody gets arrested, but the village talks.",
    82: "A Spare Battery for Rosi",
    84: "Two cells of the hotel battery are dead. Rosi needs replacements, no matter where from. “Don't ask Chiara what "
        "they cost.”",
    85: "Rosi clamps the cells in and the display jumps to green. She wipes oil off her forehead and grins at you.",
    92: "Mending Petru's Nets",
    94: "Petru points at a heap of nets and says nothing. That's an offer.",
    95: ["Petru nods once. From him, that's a medal.", "You missed two holes. Petru pays something anyway."],
    96: "The Radio at the Coast Guard Post",
    98: "Elsa's radio link to Ajaccio is crackling. No radio, no salvage – she pays cash and hates having to ask.",
    99: ["Clear reception. Elsa nods once – from her, that's a medal.", "It crackles less. Elsa pays half."],
    100: "English for the Mayor's Nieces and Nephews",
    102: "One nephew, one niece, one hour, one schoolbook. Madame Casanova pays cash and tells the whole village.",
    103: ["The children laugh and can say “anchor”. The village speaks well of you.",
          "Chaos, but warm-hearted chaos. Half pay."],
    104: "Fish Yasin's Drone Out of the Water",
    106: "Yasin's drone has fallen into the water next to the anchor. Six metres down. He pays cash, in notes.",
    107: ["You dive it up. Yasin pays and films you doing it.", "You only find the battery. Yasin grudgingly pays half."],
    108: "Move a Crate for Totò",
    110: "“Don't look inside, Comandante. Just from the tender into the storeroom. And if the Lieutenant asks: potatoes.”",
    111: ["Nobody saw a thing. Totò kisses you on both cheeks.", "Elsa saw something. Totò pays half anyway – and sweats."],
    112: "A Fisherman's Outboard",
    114: "Petru's neighbour has an outboard that stutters. Petru recommended you. That's new.",
    115: ["It purrs like new. The fisherman pays and brings fish tomorrow.", "It runs, but loudly. Half pay."],
    116: "Conjure Up Breakfast for the Guests",
    118: "Yasin wants eggs Benedict without power. He'll tip if it works. A big tip.",
    119: ["A camping stove, charm and good timing. Yasin tips generously.", "The eggs are hard. So is the tip."],
    125: "Testing the Battery Cells",
    127: "Twenty-four cells, a multimeter, a torch. Rosi reads out, you measure – one of them is bad somewhere.",
    128: "Bleeding Unit-01",
    130: "Air in the diesel line of the emergency generator. Rosi holds the torch and swears quietly in Sicilian.",
    131: "Cold Room Inventory",
    133: "What will keep, and what has to go today? Chiara wants a list before the cold room warms up – and a meal for "
         "everyone out of whatever has to go, before Lola turns it into an experiment.",
    135: "Heading Off a Guest Complaint",
    137: "Yasin is threatening a one-star review for the whole crew. Chiara needs someone to slow him down, nicely.",
    138: "Taking the Papers to the Coast Guard",
    140: "Anchoring permit, crew list, one stamp missing. Sophia has sorted the folder – you're the one taking it over.",
    141: "Arranging a Diesel Favour",
    143: "Sophia knows someone who knows someone who has a canister to spare. All she needs is your face.",
    144: "Diving to Check the Anchor Chain",
    146: "Lea wants to see whether the anchor really holds. Seven metres, clear water, a patch of sea urchins.",
    147: "Photos Without Yasin",
    149: "Siri wants pictures where she isn't posing. Just light, water and her. You hold the camera.",
    150: "Collecting Sea Samples",
    152: "Siri has collected seagrass samples – she wants to study marine biology. She hasn't told anyone yet.",
    153: "Glass tubes, a notebook, the swim platform. Siri explains seagrass to you as if it were the most exciting thing "
         "in the world.",
    155: "Diesel Under the Bar",
    157: "Alva has “something in the cellar”. You'll have to collect it yourself, and in a way the Lieutenant doesn't see.",
    158: "Hanging the Festa Banner",
    160: "Twenty metres of fabric, a church tower, a ladder from 1962. In return Madame Casanova offers you an invitation "
         "to the festa.",
    161: "Night Run with Totò's Cousin",
    163: "A dinghy from Bastia, no lights, an hour after midnight. “You only steer, Comandante.”",
    190: "A Sign for Rosi: The Board",
    191: "Yesterday Petru saw Rosi standing outside his workshop. She looked at the empty board above his door for a long "
         "time and said, “Scuderi & Figlie. That's what Papa would have called it.” Petru wants to carve her one. He only "
         "carves oak, and the only oak in the village belongs to Alva.",
    194: "Petru knocks on the wood, listens, and nods. “Good. Now we saw.”",
    196: "A Sign for Rosi: Carving",
    197: "Petru chalks the letters out, and his hand shakes as he does it. The fine work should be done by someone whose "
         "hands are still steady.",
    199: "The edges are clean. Petru runs his thumb along them. “Only the brass is missing.”",
    200: "A splinter tears out, right in the S. Petru planes the spot smooth. “Tomorrow. Slower.”",
    202: "A Sign for Rosi: The Letters",
    203: "On this island you can only get brass letters from one man, a man who never asks what they're for. Petru doesn't "
         "say his name. He just looks over at the yacht.",
    205: "Petru screws the last letter in place and slides the sign across the workbench to you. “You give it to her. She "
         "won't take anything from me.”",
    209: "A Mug for Chiara: The Colours",
    210: "For three weeks Chiara has been drinking out of guest mugs, because Lola “somehow lost” the crew mugs. Lola wants "
         "to make peace and make Chiara a mug of her own on a potter's wheel. For that, someone has to find out which "
         "colours Chiara likes without Chiara noticing why. Lola can't do it herself. Chiara isn't speaking to her.",
    213: "Dark blue with a thin gold rim, like the stripes on her uniform. Chiara noticed nothing. Lola squeals quietly into "
         "a tea towel.",
    215: "Chiara narrows her eyes. “Why do you want to know?” You change the subject. Lola counts it as a partial success.",
    217: "A Mug for Chiara: The Clay",
    218: "Petru has an old potter's wheel and lets Lola use it, as long as she brings her own clay and touches nothing. Lola "
         "always touches everything. That's why you are the one taking the clay to Petru.",
    220: "Petru puts the sack down next to the wheel and points at you, not at Lola.",
    222: "A Mug for Chiara: Throwing",
    223: "Lola throws, you hold the shape, Petru watches and says nothing. The rim has to come out straight or it'll drip. "
         "Chiara hates drips.",
    225: "The mug is crooked, but only a little. Lola paints the gold rim with her tongue between her teeth. You're supposed "
         "to give it to Chiara. “If it's from me, she'll think there's weed in it.”",
    227: "The wheel spins out and the clay flies against Petru's wall. Petru says a Corsican word. Again tomorrow.",
    231: "A Lost-and-Found for Lea",
    232: "A dive computer has been sitting in Elsa's lost-property box for a year. Nobody has claimed it. Elsa has seen Lea "
         "dive without one, and it worries her. She can only release it with a form and a reason she can defend to "
         "Ajaccio.",
    235: "“Safety on board a disabled vessel.” Elsa stamps the form twice. “It needs a battery. And a strap. I'm a gendarme, "
         "not a watchmaker.”",
    237: "Elsa pushes the form back. “That sounds as if you wanted a present. I don't give presents. Tomorrow.”",
    239: "A Lost-and-Found for Lea: The Battery",
    240: "The dive computer is dead. Elsa opens it with a tiny screwdriver from her uniform vest. She doesn't have the right "
         "button cell. In the village only Alva has things like that.",
    242: "The display flickers and shows 0.0 metres. Elsa smiles, very briefly.",
    243: "A Lost-and-Found for Lea: The Strap",
    244: "The old strap has rotted away in the salt water. You can only get a seaworthy one through the shipping company's "
         "supplies.",
    245: "Elsa puts the dive computer in your hand. “You give it to her. If I do it, it's bribery.”",
    248: "Alva's Castanets: Listening",
    249: "After three glasses Alva told Lola that her grandmother's castanets are lying broken in a drawer. She would never "
         "hand them over. Except to someone who spends an evening listening to who that grandmother was. Lola reckons that "
         "only works with a meal that tastes of home.",
    252: "You cook, Alva eats, and at some point she takes out the drawer. Two halves, wrapped in a handkerchief. “If you "
         "break them, o figliolu, I'll kill you.”",
    254: "The food is good, but not good enough for memories. Alva talks about the weather. Lola sighs.",
    256: "Alva's Castanets: The Glue",
    257: "Petru says old wood takes bone glue, not modern glue. On this island bone glue belongs to somebody who has "
         "everything else as well.",
    259: "Petru sniffs the glue pot and pulls a face. That means: right.",
    260: "Alva's Castanets: Gluing",
    261: "Two halves, a hairline crack, sixty years of flamenco. Petru warms the glue, you fit the pieces together. If one "
         "slips, they'll never sound right again.",
    263: "A dry clack, like it used to be. Petru puts the castanets in your hand. “For her. Not from me.”",
    264: "One piece slips. Petru loosens the glue again with hot water. Tomorrow.",
    268: "A Saint for Totò",
    269: "Totò's San Gennaro from Naples fell off the shelf on the night of the failure. Since then Totò hasn't laughed, "
         "and a Totò who doesn't laugh is bad for business. Alva wants to get him a new one. In the whole of Corsica only "
         "his cousin in Bastia has a figure like that, and he delivers at night, past the coast guard.",
    272: "A dinghy, no lights, a parcel in newspaper. The saint has arrived, only unfortunately unpainted and very grey.",
    273: "Elsa's searchlight sweeps the water. The cousin turns away. The village talks.",
    275: "A Saint for Totò: Gold",
    276: "Alva wants to paint the saint herself. “Golden, like in Naples. Golden like a lottery win.” She has the gold paint "
         "on her own shelf, but she doesn't pay for presents for Totò. On principle.",
    278: "Alva paints until the saint shines like a slot machine. “Perfect. Now he just has to look at it.”",
    280: "A Saint for Totò: The Handover",
    281: "Alva says you never just hand a Neapolitan something. You give it to him over a meal. One that tastes like his "
         "mother's: Genovese, six hours of onions.",
    283: "Totò tastes it, puts his fork down and stares at the figure. Then he laughs, so loudly that Alva grabs the "
         "glasses. You'd better give him the figure yourself.",
    285: "The onions burn. Totò eats it anyway and praises you. He's a very bad liar. Again tomorrow.",
    289: "A Pen for Sophia: The Engraver",
    290: "Lea wants to give her sister a fountain pen. Engraved with her own name, for what Sophia only writes for herself. "
         "The only engraver for miles is known to Madame Casanova, and she only gives out addresses once she has been "
         "admired for long enough.",
    293: "Madame Casanova writes the address on a napkin and signs it as if it were an autograph. Lea throws her arms "
         "around your neck.",
    295: "Madame Casanova talks to you about her festa for two hours and forgets the address. Lea laughs until she gets "
         "hiccups.",
    297: "A Pen for Sophia: The Blank",
    298: "The engraver in Ajaccio only engraves a blank you bring yourself. Blanks are in the shipping company's supplies, "
         "which means Megan.",
    300: "Two days later the pen arrives on the post boat in a velvet case. Lea presses it into your hand. “You give it to "
         "her. I'd cry.”",
    304: "A Book for Siri's Father: The Net Twine",
    305: "Siri's father has fished off Trøndelag for forty years. Petru reminds her of him so much she can hardly look at "
         "him. She wants to write down his stories about fishing in Corsica, for her father. Petru doesn't talk to "
         "influencers. Not until his nets are mended, and he doesn't take money.",
    308: "Petru weighs the roll of twine in his hand and points at the chair beside him. That's an invitation.",
    310: "A Book for Siri's Father: The Conversation",
    311: "Petru talks when you're quiet. Siri isn't good at being quiet. You're to ask the questions, so that Petru doesn't "
         "notice it's an interview, and so that it doesn't annoy him.",
    313: "Petru talks about tuna, storms and his father. Siri takes notes for three hours without a single photo. In the "
         "evening she binds the pages and gives them to you. “Keep it safe until I go home. I lose everything.”",
    315: "One question too many. Petru gets up and goes to fetch nets he doesn't need. Siri looks at you for a long time.",
    319: "A Present for the Lieutenant: The Archive",
    320: "Elsa has been at the Cala d'Orsu post for five years. The village wants to thank her, but she won't accept "
         "anything. It would all be bribery. Madame Casanova has an idea: Elsa's own tickets from five years, bound like "
         "a book. They're somewhere in the town archive, unsorted, between fishing licences from 1974.",
    323: "Three hundred and twelve tickets, in order. One of them is for Madame Casanova herself, for fireworks without a "
         "permit. She insists it goes at the front.",
    325: "You find the fishing licences from 1974. And nothing else. Madame Casanova calls it chapter one.",
    327: "A Present for the Lieutenant: The Linen",
    328: "It has to be bound in linen, says Madame Casanova, like a state document. Only Alva has linen, and Madame "
         "Casanova hasn't spoken to Alva since the quarrel over the village shop.",
    330: "Madame Casanova strokes the linen and whispers, “Dignified.”",
    331: "A Present for the Lieutenant: Binding",
    332: "Three hundred and twelve sheets, one spine, an awl and thread. Meanwhile Madame Casanova gives a speech nobody "
         "asked for.",
    334: "A thick block bound in linen, with Elsa's initials. Madame Casanova cries a little. “You give it to her. I'd make "
         "a speech.”",
    336: "The thread snaps at sheet two hundred. Madame Casanova calls it a trial sent by fate.",
    340: "A Card for Megan: The Signatures",
    341: "Lola says Megan has a glass office, and the only things anyone ever sends her are reports. “Everyone hates the "
         "boss, mate. I reckon that's lonely.” She wants to send Megan a card signed by the whole crew. The problem: half "
         "the crew would rather jump overboard.",
    344: "Eleven signatures. Chiara's is very small, Totò's very big, Rosi's is a drawing of Unit-01. Lola sticks a heart "
         "next to them that nobody asked for.",
    346: "Chiara refuses, Rosi signs with “No”. Lola says that sort of counts too.",
    348: "A Card for Megan: The Frame",
    349: "“Without a frame she bins it. With a frame she has to hang it up. That's science.” Only Alva has frames.",
    350: "Lola frames the card, crookedly, and hands it to you. “You give it to her. She doesn't believe I can read.”",
    353: "Tobacco for Petru",
    354: "For weeks Petru has been smoking something that smells of hay. His tobacco, Bastia Noir, only comes through "
         "Totò's cousin. Totò wants to get it for him, because years ago Petru pulled the cousin out of the water. He "
         "won't pay for the run on his own, and Petru mustn't know who it's from.",
    357: "Totò puts the tin in your hand. “From you. If Petru finds out it's from me, he'll thank me. I can't take that.”",
    359: "Liquorice for Holm",
    360: "Siri has a bag of salty Norwegian liquorice in her suitcase. Holm loves the stuff, the whole crew knows it. Siri "
         "doesn't dare send it to the Captain in hospital; in three weeks they've barely exchanged two sentences. Elsa is "
         "going to Ajaccio tomorrow. Someone has to give Siri some courage and ask Elsa.",
    363: "Elsa takes the bag with a nod. In the evening a message comes from the hospital, just one word: “Takk.” Siri "
         "reads it five times.",
    365: "Siri gets cold feet and nervously eats half the bag. By tomorrow it's been refilled.",
    367: "Yasin's Sunglasses",
    368: "Yasin's gold sunglasses slipped off the swim platform while he was filming. They're the one thing he never films: "
         "a present from his father. He pays cash, and he doesn't like asking. Eight metres, a current in the afternoon.",
    370: "You find them between two rocks. Yasin isn't there when you surface. Give them to him yourself.",
    371: "The current pushes you away. You see something golden but can't reach it. Tomorrow, at slack water.",
    374: "Night Watch with Chiara",
    375: "Chiara hasn't been able to sleep since the failure. She asks you to stand the night watch with her and explain the "
         "stars to her. Her grandfather always promised to and never got round to it. She wouldn't ask anyone else.",
    377: "You find the Plough, Cassiopeia and a satellite that Chiara declares to be a star. She falls asleep on the bench. "
         "You let her.",
    379: "Clouds. You can't see anything, and Chiara talks about work instead. Maybe it'll be clear tomorrow.",
    381: "Arancini Like Nonna's",
    382: "Rosi's nonna died last winter. She never wrote down the recipe for her arancini, and Rosi can't get them right. "
         "She doesn't want to try again on her own.",
    384: "You change the rice twice and the saffron once. On the third attempt Rosi stops, chews and says nothing. Then she "
         "eats three in a row.",
    386: "The balls fall apart in the pan. Rosi laughs and cries a little at the same time. Tomorrow.",
    388: "Sophia's First Chapter",
    389: "Sophia puts twelve pages in front of you. Something of her own, not for a publisher. She wants an honest opinion, "
         "not a nice one. Anyone who only flatters her never gets to read another line.",
    391: "You tell her what works and what doesn't. She cuts two pages without arguing. Then she asks whether you'd like to "
         "read the second chapter too.",
    393: "You're too polite. Sophia notices at once, takes the pages back and smiles kindly. That's worse.",
    396: "Paella for the Crew: Saffron",
    397: "Lola wants to make the crew a paella, so that after this week everyone sits at one table again. She has never made "
         "one. “It's basically fancy risotto, how hard can it be.” Without real saffron it'll be yellow mush, says Chiara. "
         "Lola wants to prove her wrong.",
    400: "Lola holds the little tin up to the light like a gemstone. “Mate. That's not a spice, that's a personality.”",
    402: "Paella for the Crew: Cooking",
    403: "A pan as big as a lifebuoy, a gas burner, and Lola, who wants to stir every two minutes. You don't stir a paella. "
         "Someone has to stop her.",
    405: "The crust crackles. The crew eats in silence, then very loudly. Chiara takes seconds and says nothing. Lola counts "
         "it as a win.",
    406: "Lola stirs. It turns into risotto. The crew eats it anyway.",
    410: "A Short ESG Report for Megan",
    411: "The investors want one page on how sustainable a stranded solar yacht is. Megan knows you do this for a living. "
         "She doesn't ask. She orders, with a deadline of this evening.",
    413: "One page, three figures, not one word too many. Megan reads it on video, is silent, and then says, “Annoyingly "
         "good.”",
    414: "Megan strikes out half and sends the rest back. “I asked for a report, not a poem.”",
    416: "Megan's Laundry Supplier",
    417: "The fleet's new laundry supplier calls itself climate-neutral. Megan wants to know whether that's true before she "
         "signs, and from someone who doesn't work for the supplier.",
    419: "The certificates belong to a different factory. Megan smiles slowly. “Checkmate.” She pays at once.",
    420: "You find nothing solid. Megan still doesn't sign. “Then keep looking.”",
    423: "Elsa's Antenna: The Cable",
    424: "Since the last storm Elsa's radio no longer reaches Ajaccio. The old antenna cable has worn through. The "
         "gendarmerie applied for a new one eleven months ago. The shipping company has some, and Elsa doesn't ask a "
         "shipping company for anything.",
    427: "Elsa takes the cable and inspects the reel. “You didn't get this from me.”",
    428: "Elsa's Antenna: Up on the Roof",
    429: "The antenna sits on the roof of the post, four metres above the harbour. Wind from the north-west, gusts. Elsa "
         "holds the ladder and says she would climb up herself if she were allowed to.",
    431: "Crackling, then Ajaccio, crystal clear. Elsa salutes, half joking, half not.",
    432: "A gust rips the cable out of your hand. Elsa catches you by the ankle. Tomorrow, with less wind.",
    436: "A Tasting Menu for the Festa",
    437: "Madame Casanova wants a buffet at the festa, “from all over the world, but Corsican”. The jury is her, her mother "
         "and the priest. The village cook has pulled out because she accused him of having “vision”. She has heard you "
         "can cook, and she's already announcing it all over the village.",
    440: "The priest takes three helpings. The mother says, “Hm.” Madame Casanova declares you the official cook of the "
         "festa, with a sash.",
    442: "The mother pushes her plate away. Madame Casanova announces that this was part of the plan.",
    445: "Food for the Night Patrol",
    446: "Since the failure Elsa and her two men have been on patrol every night, eating cold tins on the boat. She won't "
         "take money or presents. But a hot meal for the crew counts as rations, she says, and she's allowed to accept "
         "that. If it's good.",
    449: "Three fewer empty tins. Elsa's men call you “Chef”. Elsa says nothing and takes the box along again the next "
         "evening.",
    451: "It's lukewarm by the time the boat casts off. Elsa thanks you anyway, very formally. That's worse than criticism.",
    455: "Cooling: Fit a Relay",
    456: "The compressor only needs a new relay. Fitting it is easy; getting it isn't. On this island only one man has "
         "things like that.",
    458: "Click, hum, cold air. Alva pays and gives you a myrtle liqueur on top.",
    476: "The Cooling Has Packed Up",
    477: "The compressor in Alva's cellar is dead, and all the festa stock is sweating. Something has to happen by this "
         "evening.",
}


def felder(pfad):
    """{line: [texts in column order]} for all mission text fields."""
    baum = ast.parse(open(pfad, encoding="utf-8").read())
    t = []
    for k in ast.walk(baum):
        if isinstance(k, ast.Dict):
            for kk, v in zip(k.keys, k.values):
                if isinstance(kk, ast.Constant) and kk.value in FELDER and isinstance(v, ast.Constant) \
                        and isinstance(v.value, str):
                    t.append((v.lineno, v.col_offset, v.value))
        if isinstance(k, ast.Call) and getattr(k.func, "id", None) in POS:
            for i, a in enumerate(k.args):
                if i in POS[k.func.id] and isinstance(a, ast.Constant) and isinstance(a.value, str):
                    t.append((a.lineno, a.col_offset, a.value))
            for kw in k.keywords:
                if kw.arg in FELDER and isinstance(kw.value, ast.Constant):
                    t.append((kw.value.lineno, kw.value.col_offset, kw.value.value))
    out = {}
    for z, c, s in sorted(t):
        out.setdefault(z, []).append(s)
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    lit = felder(QUELLE)
    items, fehler = [], []
    for z, neu in NEU.items():
        neu = neu if isinstance(neu, list) else [neu]
        alt = lit.get(z, [])
        if len(alt) != len(neu):
            fehler.append("L%d erwartet %d, gefunden %d %s" % (z, len(neu), len(alt), alt))
            continue
        items += [{"key": "missionen:L%d.%d" % (z, i), "alt": a, "neu": n} for i, (a, n) in enumerate(zip(alt, neu))]
    offen = ["L%d %r" % (z, a[:70]) for z, al in lit.items() for a in al if z not in NEU]
    for f in fehler:
        print("FEHLER", f)
    for o in offen:
        print("OFFEN", o)
    if fehler:
        sys.exit(1)
    ziel = os.path.join(EDEN, "docs", "abnahme", "englisch_missionen.json")
    json.dump({"id": "englisch_missionen", "titel": "Englisch · Paket 4: Missionen",
               "gruppen": [{"titel": "Missionen", "items": items}]},
              open(ziel, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("geschrieben:", ziel, len(items), "Texte; offen:", len(offen))


if __name__ == "__main__":
    main()
