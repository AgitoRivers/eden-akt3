# -*- coding: utf-8 -*-
"""Akt 2, Woche 2 "Die Insel oeffnet sich" (Tag 8-14, Duc 27.10.2026, E-083) - die Pflicht-Events der Woche.

Roter Faden: ein fremdes Teil in Unit-01 fuehrt zu A.V. Estates, Gennaro verschwindet in der Grotte, Kevin klaut Leas
Seite 40, und am Sonntag steht Lea mit den Koordinaten in der Tuer (Auftakt Woche 3). Die Orte dazu (Grotte, Kevins
Daecher) stehen in ereignisse_grotte.py, die Berge in ereignisse_berge.py. Rosis Werkstatt (Tag 8) in ereignisse_gag1.py.

  Tag 8   Fruehstueck: die Crew nach dem Urteil (drei Fassungen) · Abend: Unit-01 mit rotem Auge (Kampf) · Nacht: das Teil
  Tag 9   Fruehstueck: Megan erkennt das Logo
  Tag 10  Nachmittag: Yamamotos Vogelfoto (Totò mit einem Fremden)
  Tag 11  Fruehstueck: Totò gesteht - die Grotte oeffnet
  Tag 12  Tag: Kevin klaut Seite 40 - Kevins Daecher oeffnen (bis Tag 14)
  Tag 14  Abend: Sonntag am Strand · Nacht: Lea mit den Koordinaten, eine Drohne ueber der Bucht"""
from ereignisse_basis import *  # noqa: F401,F403
from ereignisse_gag1 import P1  # noqa: E402

KAMPF = lambda bid: {"kampf": bid}
DIREKT = lambda ziel: {"direkt": ziel}
_STEELMOP_SETS = {"rosi": "Engine Room", "maxwell": "maximum_steward_a", "chiara": "Uniform"}
PFL = lambda tag, phase, bed=None: WANN((tag, tag), [phase], bed=bed, pflicht=True)
H = lambda anrufer, ort: {"anrufer": anrufer, "anrufer_ort": ort, "art": "video"}
GNAEDIG = [{"flag": "urteil_erbarmen"}, {"flag": "urteil_entlastet"}, {"flag": "urteil_aufgeklaert"}]

item("foreign_part", "The Part That Isn't Ours", "quest",
     text="A small black module, warm to the touch, with a stamped code and a tiny white logo. Rosi pulled it out of "
          "Unit-01's control board. It doesn't belong to anything on this boat.")

EVENTS = [
    # ------------------------------------------------------------------ Tag 8: The Morning After
    E("a2_morgen_gefeuert", "gag1", "ernst", "The Morning After", PFL(8, "fruehstueck", {"flag": "gefeuert"}),
      "crew_mess",
      P1("lola", ("maxwell", "?", "eats in silence"), ("toto", "?", "counts the chairs")),
      "The first morning after the hearing. Lola has laid the table the way she always does, and then taken one plate "
      "away again, the plate of the one who was fired at the hearing. Nobody mentions the empty chair. Everybody looks at it.",
      [Z("lola", "I made pancakes. I made one too many. I'll eat it. It's fine. I'm fine.", "sadness"),
       Z("maxwell", "Mr. Maximum has seen many teams lose a player. The team that talks about it wins.", "caring"),
       Z("toto", "Comandante, one question. Is it over now, or is this only the start?", "nervousness")],
      [O("“It was the right call. It still hurts. Both things are true.”", [R(2), W("moral", -1)],
         zeile=Z("lola", "Both things. Okay. I can hold two things. I'm a chef.", "sadness")),
       O("“It's the start, Totò. We're going to find out who's really behind all this.”", [W("moral", 1)],
         zeile=Z("toto", "Then I want more coffee. A lot more coffee.", "optimism"))],
      sets={"lola": "Galley", "maxwell": "maximum_steward_a", "toto": "Standard"}),
    E("a2_morgen_warm", "gag1", "wholesome", "The Morning After",
      PFL(8, "fruehstueck", {"alle": [{"eine": GNAEDIG}, {"nicht": {"flag": "gefeuert"}}]}), "crew_mess",
      P1("lola", ("maxwell", "+", "has made a speech"), ("toto", "+", "is taking bets again")),
      "The first morning after the hearing. Somebody has hung a bedsheet over the mess door with GOOD MORNING EDEN "
      "on it in ketchup. Lola is singing. The coffee is strong enough to stand a spoon in.",
      [Z("lola", "We survived the hearing and nobody went to prison! I made the celebration pancakes, and they're shaped like Megan. Eat her face.", "joy"),
       Z("maxwell", "Mr. Maximum would like to say a few words. Twenty-five words. Maybe thirty.", "pride"),
       Z("toto", "One euro says Maxwell needs a hundred. Who's in?", "amusement")],
      [O("Puts a euro on the table. “A hundred and twenty.”", [W("moral", 1), V("toto", 2)],
         zeile=Z("toto", "Ha! A man of the people!", "joy")),
       O("Lets Maxwell talk. All hundred and forty words.", [V("maxwell", 4)],
         zeile=Z("maxwell", "…and that, brothers and sisters, is why we are a team. Thank you. Mr. Maximum is crying.",
                 "joy"))],
      sets={"lola": "Galley", "maxwell": "maximum_steward_a", "toto": "Standard"}),
    E("a2_morgen_kalt", "gag1", "ernst", "The Morning After",
      PFL(8, "fruehstueck", {"alle": [{"nicht": {"eine": GNAEDIG}}, {"nicht": {"flag": "gefeuert"}}]}), "crew_mess",
      P1("lola", ("maxwell", "-", "avoids your eyes"), ("toto", "-", "isn't joking")),
      "The first morning after the hearing. Breakfast is on the table, but nobody talks while you're in the room. "
      "When you sit down, two people find a reason to get up.",
      [Z("lola", "Coffee's there. Pancakes are there. I'm… there. Over there.", "nervousness"),
       Z("toto", "Comandante, nobody knows what really happened the night of the fire. That's the problem, everybody guesses.",
         "disapproval")],
      [O("“Then let's stop guessing. Whatever it takes, I'll find out.”", [R(3)],
         zeile=Z("toto", "Okay. Prove it. I'll believe it when I see it.", "neutral")),
       O("Eats in silence. Some mornings you just eat.", [W("moral", -1)])],
      sets={"lola": "Galley", "maxwell": "maximum_steward_a", "toto": "Standard"}),

    # ------------------------------------------------------------------ Tag 8 Abend: Unit-01 mit rotem Auge
    E("a2_unit01", "gag1", "ernst", "A Red Eye in the Dark", PFL(8, "abend"), "generator_room",
      P1("maxwell", ("toto", "-", "is hiding behind you")),
      "Evening. A noise comes up from the generator room that Unit-01, Rosi's old diesel, has never made. Not a cough, not a purr. A "
      "grinding, like teeth. When you open the door, the old diesel turns its head towards you. Its eye is not amber "
      "any more. It's red.",
      [Z("maxwell", "Brother. Unit-01 is looking at us like Mr. Maximum looks at a buffet.", "fear"),
       Z("toto", "She's never done that. Thirty-one years, two owners, one explosion, and she's never done that.", "fear")],
      [O("Steps in and closes the door behind him. “Easy, old girl. Easy.”", [KAMPF("a2_unit01")],
         zeile=Z("maxwell", "Mr. Maximum is right behind you. Quite far behind you.", "nervousness")),
       O("Pulls the fuel line first, then goes in. “Sorry, old girl.”", [KAMPF("a2_unit01")],
         probe=P("perception", 12), erfolg=[F("a2_unit01_leitung")], fehlschlag=[],
         zeile=Z("toto", "She'll forgive you. She's a diesel, and diesels forgive everything.", "nervousness"))],
      sets={"maxwell": "maximum_steward_a", "toto": "Standard"}),
    E("a2_teil", "gag1", "ernst", "The Part That Isn't Ours", PFL(8, "nacht", {"nicht": {"flag": "gefeuert_rosi"}}),
      "workshop",
      P1("rosi", ("maxwell", "?", "is listening at the door")),
      "Midnight in the workshop. Unit-01 is lying on the bench like a patient, purring again, amber again. Rosi has her control board open and is holding something up to the lamp with tweezers. Her hands are shaking, and "
      "Rosi's hands never shake.",
      [Z("rosi", "This isn't ours, and it isn't anybody's on this boat. Somebody soldered it into her, and it's neat work. Better than mine.", "anger"),
       Z("rosi", "It listens, and when it hears the right signal it gives orders. Like the collars on those animals in the harbour. "
                 "Somebody can make my Unit-01 bite.", "fear"),
       Z("maxwell", "Then somebody was on board who shouldn't have been. Mr. Maximum will say nothing. Mr. Maximum is a "
                    "vault.", "fear")],
      [O("Takes the little black module and turns it in the light. There's a stamped code. And a tiny white logo.",
         [I("foreign_part"), F("a2_teil_gefunden"), V("rosi", 4)],
         zeile=Z("rosi", "I know that logo from somewhere, but I don't know where, and I hate that.", "annoyance")),
       O("“Can you make it talk? Find out who it was listening to?”", [I("foreign_part"), F("a2_teil_gefunden"),
                                                                      F("a2_teil_analyse"), V("rosi", 6)],
         zeile=Z("rosi", "Give me a week and a very large coffee. And don't tell Unit-01 I said she got hacked. She's sensitive.", "pride"))],
      sets={"rosi": "Engine Room", "maxwell": "maximum_steward_a"}),
    E("a2_teil_maxwell", "gag1", "ernst", "The Part That Isn't Ours", PFL(8, "nacht", {"flag": "gefeuert_rosi"}),
      "workshop",
      P1("maxwell", ("toto", "?", "holds the lamp")),
      "Midnight in the workshop. Without Rosi it's just a room. Maxwell has Unit-01's control board open on the bench "
      "and a phone torch in his teeth, following a video tutorial with the volume turned down.",
      [Z("maxwell", "Mr. Maximum is no engineer. But Mr. Maximum knows what doesn't belong. This doesn't belong.",
         "anger"),
       Z("toto", "Rosi would have known in one second. Rosi isn't here.", "sadness")],
      [O("Takes the little black module. A stamped code. A tiny white logo.", [I("foreign_part"), F("a2_teil_gefunden")]),
       O("“Rosi should see this. Wherever she is.”", [I("foreign_part"), F("a2_teil_gefunden"), F("a2_teil_rosi_foto")],
         zeile=Z("toto", "I'll send her a photo. She'll swear. That's how we know she still cares.", "sadness"))],
      sets={"maxwell": "maximum_steward_a", "toto": "Standard"}),

    # ------------------------------------------------------------------ Tag 9: das Logo
    E("a2_logo", "handy", "ernst", "The Logo", PFL(9, "fruehstueck"), ORT_DUC, H("megan", "megan_office"),
      "You sent Megan a photo of the little black module from Unit-01 at three in the morning. At seven she calls back. She has "
      "not slept either.",
      [Z("megan", "That logo. A.V. Estates. I sat across a table from them in Monaco a year ago. They wanted to buy "
                  "the bay for a resort.", "neutral"),
       Z("megan", "A.V. Estates belongs to Alon Varenne. The man behind those collars in the harbour. The man who owns the mountain.",
         "anger"),
       Z("megan", "Somebody put his hardware into my generator. On my ship. Find out who, First Officer. Quietly.",
         "disapproval")],
      [O("“Quietly. Understood.”", [F("a2_av_bekannt"), V("megan", 2)],
         zeile=Z("megan", "And Duc? Lock your cabin. I mean it.", "caring")),
       O("“Quietly is how they got on board in the first place.”", [F("a2_av_bekannt")],
         zeile=Z("megan", "Fair. Then loudly. But carefully loudly.", "amusement"))],
      sets={"megan": "Boardroom"}),

    # ------------------------------------------------------------------ Tag 10: das Vogelfoto
    E("a2_vogelfoto", "gag1", "ernst", "Bird Photography", PFL(10, "nachmittag"), "aft_deck",
      P1("yamamoto", ("maxwell", "-", "is in every photo")),
      "Yamamoto-san is cleaning his long lens on the aft deck. He waves you over and scrolls through his camera with "
      "the solemn joy of a man about to show a stranger four hundred pictures of a cormorant.",
      [Z("yamamoto", "Bird photography. Very relaxing. Very… ah. This one is not a bird. Mm.", "embarrassment"),
       Z("yamamoto", "Thursday night, harbour. The cook… no. The trader. Totò-san. With a man from a dinghy. Big "
                     "moustache. Gold tooth. They are arguing. Then the moustache goes out to sea. Towards the cliffs.",
         "curiosity"),
       Z("yamamoto", "I am a banker. In my experience, two men arguing at night about a dinghy is always about money.",
         "neutral")],
      [O("“Send me that one, please.”", [F("a2_foto_gesehen"), V("yamamoto", 2)],
         zeile=Z("yamamoto", "Of course. I send you also the cormorant. As a gift.", "joy")),
       O("“Delete it. Totò's business is Totò's business.”", [F("a2_foto_geloescht"), V("toto", 2)],
         zeile=Z("yamamoto", "Deleted. Mm. Loyalty. Also very relaxing.", "approval"))],
      sets={"yamamoto": "yamamoto_hawaii_b", "maxwell": "maximum_training_b"}),

    # ------------------------------------------------------------------ Tag 11: Totò gesteht - die Grotte
    E("a2_toto_beichte", "gag1", "ernst", "Low Tide", PFL(11, "fruehstueck"), "crew_mess",
      P1("toto", ("lola", "?", "pretends to wipe the counter")),
      "Totò hasn't touched his coffee. That has never happened before. He waits until the mess is empty, then sits "
      "down opposite you and puts his phone on the table between you, face up. No new messages.",
      [Z("toto", "My cousin Gennaro, from Bastia, owes money to some people. The wrong people. The worst people.",
         "nervousness"),
       Z("toto", "Thursday he went into the grotto under Punta d'Orsu to fetch a crate for them. Three hours, he "
                 "said. It's Monday, boss.", "fear"),
       Z("toto", "I can't go to the police. If I go to the police, they find out what's in my locker. And Gennaro has "
                 "a little girl. Giulia. Seven years old. Please.", "grief")],
      [O("“When's low tide?”", [F("grotte_offen"), V("toto", 4)],
         zeile=Z("toto", "Today. Tomorrow. Every day, twice. I have a boat. I always have a boat.", "relief")),
       O("“You should have told me on Thursday.”", [F("grotte_offen")],
         zeile=Z("toto", "On Thursday I thought he was just drunk somewhere. He's usually just drunk somewhere.",
                 "remorse"))],
      sets={"toto": "Standard", "lola": "Galley"}),

    # ------------------------------------------------------------------ Tag 12: Kevin klaut Seite 40
    E("a2_kevin_raub", "gag1", "witzig", "Page Forty", PFL(12, "tag"), "swim_platform",
      P1("lea", ("sophia", "?", "was helping her")),
      "Lea and Sophia are sitting on the swim platform with Lea's battered chart book open between them, comparing "
      "her grandfather's pencil marks with a nautical chart. Then a shadow, a scream, a rush of wings. Kevin, the fat seagull who steals everything on this boat. And "
      "page forty goes up into the sky in his beak.",
      [Z("lea", "NO! No no no no. That's Grandad's page! That's the only one with the cross on it!", "anger"),
       Z("sophia", "He's flying towards the village, to the bell tower. That gull has a nest up there, everybody knows.",
         "surprise"),
       Z("lea", "Officer. I've never asked you for anything. I'm asking now. Get that bird.", "grief")],
      [O("Already pulling off his shoes. “The bell tower. Got it.”", [F("kevin_jagd"), V("lea", 4), GAG("kevin")],
         zeile=Z("lea", "Not now! Low tide, the grotto, Totò's cousin… whenever. Just before Sunday. Please.", "caring")),
       O("“It's a page, Lea. You know it by heart.”", [F("kevin_jagd")],
         zeile=Z("lea", "I know it by heart. I don't know HIS HANDWRITING by heart.", "sadness"))],
      sets={"lea": "Deck", "sophia": "Concierge"}),

    # ------------------------------------------------------------------ Tag 14: Sonntag und die Koordinaten
    E("a2_sonntag", "gag1", "wholesome", "Sunday", PFL(14, "abend"), "aft_deck",
      P1("lola", ("lea", "+", "is happy"), ("maxwell", "+", "is grilling"), ("toto", "+", "is quiet")),
      "Sunday evening. Nobody planned it, and everybody came. Lola grills sardines, Maxwell grills Lola's sardines "
      "again because Mr. Maximum likes them burnt, Totò plays something sad on a phone speaker. Two weeks ago you "
      "were strangers stranded on a broken yacht. Now you're strangers stranded on a broken yacht together.",
      [Z("lola", "To week two! Nobody died, though some people nearly did, and I made a cake shaped like a gull!", "joy"),
       Z("maxwell", "Mr. Maximum would like to say thirty words. Fifty. A hundred. It's Sunday.", "joy"),
       Z("toto", "To my cousin Gennaro. Wherever he is.", "sadness")],
      [O("Raises his glass to all of it.", [W("moral", 1)]),
       O("Sits next to Totò and doesn't say anything.", [V("toto", 4)])],
      sets={"lola": "Galley", "lea": "Off Duty", "maxwell": "maximum_party_b", "toto": "Standard"}),
    E("a2_koordinaten", "gag1", "ernst", "Coordinates", PFL(14, "nacht", {"flag": "kevin_seite"}), "duc_cabin",
      P1("lea", ("sophia", "?", "did the maths")),
      "Past midnight. A knock, three short, one long. Lea is standing in your doorway in a hoodie, hair still wet, "
      "the page Kevin stole in one hand and Sophia's tablet in the other. Behind her, over the bay, something small is humming "
      "in the dark. A drone. No lights.",
      [Z("lea", "Sophia worked it out. Grandad's cross and the old chart and the sonar. It fits. It all fits.",
         "excitement"),
       Z("lea", "Forty metres down, off Punta d'Orsu. Grandad's schooner. The one he looked for his whole life.", "realization"),
       Z("lea", "Do you hear that? That hum? It's been there since you climbed the bell tower after Kevin. I think somebody else knows too.",
         "fear")],
      [O("Pulls her inside and closes the door. “Then we dive first.”", [F("woche2_ende"), F("wrack_koordinaten"),
                                                                         V("lea", 8)],
         zeile=Z("lea", "We dive first. Week three. Oh God. I need a bigger tank.", "excitement")),
       O("Looks out at the drone. “Then we dive fast. And we tell nobody.”", [F("woche2_ende"), F("wrack_koordinaten"),
                                                                            F("wrack_geheim"), V("lea", 6)],
         zeile=Z("lea", "Nobody. Not even Sophia? …Sophia already knows. Sophia did the maths.", "nervousness"))],
      sets={"lea": "Off Duty", "sophia": "Concierge"}),
    E("a2_koordinaten_ohne", "gag1", "ernst", "From Memory", PFL(14, "nacht", {"nicht": {"flag": "kevin_seite"}}),
      "duc_cabin",
      P1("lea", ("sophia", "?", "did the maths")),
      "Past midnight. A knock. Lea is standing in your doorway with a pencil behind her ear and a sheet of paper "
      "covered in rubbed-out lines. Behind her, over the bay, something small is humming in the dark. A drone. No "
      "lights.",
      [Z("lea", "Kevin's nest on the bell tower is empty. Grandad's page is gone. Sea, rain, I don't know. So I drew it. From memory.",
         "sadness"),
       Z("lea", "It's close. It's not Grandad's. I don't know if it's close enough.", "grief"),
       Z("lea", "And that hum. It's been there since the day Kevin stole the page. I think somebody else is looking too.", "fear")],
      [O("“Close is a start. We'll dive anyway.”", [F("woche2_ende"), F("wrack_gedaechtnis"), V("lea", 4)],
         zeile=Z("lea", "Anyway. Okay. Week three. We dive anyway.", "optimism")),
       O("“I should have climbed that bell tower for your page. I'm sorry, Lea.”", [F("woche2_ende"), F("wrack_gedaechtnis"), V("lea", 2)],
         zeile=Z("lea", "You had Totò's cousin to save and a grotto full of… stuff. I know. I'm just sad. Let me be sad.",
                 "sadness"))],
      sets={"lea": "Off Duty", "sophia": "Concierge"}),
    # ------------------------------------------------------------------ Tag 19: Rosi uebergibt Steel Mop und Taser-Gewehr (Duc 01.11.2026)
    E("a2_steelmop", "gag1", "witzig", "The Steel Mop", WANN((19, 19), ["fruehstueck"], pflicht=True, holt_leute=True), "workshop",
      P1("rosi", ("maxwell", "?", "has lost his mop"), ("chiara", "+", "came to see what the noise is")),
      "The workshop smells of hot metal. Two long shapes lie on the bench under a sheet. Mr. Maximum has been looking for "
      "his mop since last night, and he has checked your cabin twice.",
      [Z("maxwell", "Number One, Mr. Maximum reports a crime. The old wooden mop is gone. On day two you laughed at it, "
                    "brother, and it taught you to parry anyway. Now somebody has stolen it in the night.", "nervousness"),
       Z("rosi", "I stole it. Stop crying and help me with the sheet.", "annoyance")],
      [O("Takes one corner of the sheet.", [DIREKT("a2_steelmop_2")]),
       O("Takes one corner of the sheet. “That mop hit me in the ear on day two. I won't miss it.”", [DIREKT("a2_steelmop_2")])],
      sets=_STEELMOP_SETS),
    E("a2_steelmop_2", "gag1", "witzig", "The Steel Mop", WANN((8, 21), bed={"flag": "a2_steelmop_nie"}), "workshop",
      P1("rosi", ("maxwell", "+", "has found his bristles"), ("chiara", "+", "watches")),
      "Under the sheet is a long steel pipe with a steel cube on the end, as big as a beer crate. Just under the cube, a "
      "thick ring of white bristles sits around the pipe. You know those bristles.",
      [Z("maxwell", "Those are… eish. Those are the bristles.", "surprise"),
       Z("rosi", "You would have cried if I threw them out, so they stay. The block held Unit-01 down for longer than I've "
                 "been alive, so don't you dare dent it. It's called a Steel Mop, because I couldn't think of anything "
                 "that would make you happier.", "pride")],
      [O("Steps back and gives him room.", [DIREKT("a2_steelmop_3")]),
       O("“Can anybody even lift that?”", [DIREKT("a2_steelmop_3")])],
      sets=_STEELMOP_SETS),
    E("a2_steelmop_3", "gag1", "witzig", "The Steel Mop", WANN((8, 21), bed={"flag": "a2_steelmop_nie"}), "workshop",
      P1("chiara", ("maxwell", "+", "has no sleeves now"), ("rosi", "+", "watches")),
      "He lifts it with both hands. The sleeves of his shirt tear at the shoulders, one and then the other, and everybody "
      "hears it.",
      [Z("chiara", "That shirt was a uniform. Sleeves: zero. Arms: nine, and I'm not happy about it. The bow tie stays, "
                   "Mr. Ndlovu, or I call your Gogo.", "disapproval"),
       Z("maxwell", "Mr. Maximum keeps the bow tie. Mr. Maximum is a professional. Parry the dirt, Number One! Only now the "
                    "dirt has to be very brave.", "joy")],
      [O("Looks at the second shape on the bench.", [F("steel_mop"), DIREKT("a2_steelmop_4")]),
       O("Picks up one torn sleeve and hands it to Chiara.", [F("steel_mop"), DIREKT("a2_steelmop_4")])],
      sets=dict(_STEELMOP_SETS, maxwell="maximum_steelmop")),
    E("a2_steelmop_4", "gag1", "witzig", "The Steel Mop", WANN((8, 21), bed={"flag": "a2_steelmop_nie"}), "workshop",
      P1("rosi", ("chiara", "+", "has a rifle now"), ("maxwell", "+", "is still holding the mop")),
      "Rosi puts the second shape into Chiara's hands, a short grey rifle with a thick wire coiled under the barrel.",
      [Z("rosi", "The other one is yours, Mole. It's a taser rifle. It reaches further than you can throw a napkin swan, and "
                 "whoever it hits stops moving for a while. Robots don't care, so don't waste it on them.", "neutral"),
       Z("chiara", "Balance: eight. Colour: two. Who chose grey?", "curiosity"),
       Z("rosi", "The capacitor is the best one we had, and that's all I'm going to say about it. Well, Officer? Will they do?",
         "embarrassment")],
      [O("Looks at both of them. “They'll do. Nobody on that beach is ready for him.”", [F("taser_gewehr"), V("rosi", 1)],
         zeile=Z("rosi", "Nobody on this boat is either. Now get out of my workshop.", "amusement")),
       O("“And what did you build for me?”", [F("taser_gewehr"), V("rosi", 1)],
         zeile=Z("rosi", "Terremoto, Officer, on the worst day of my life, and you've dented it twice. I'm writing that on the "
                         "board.", "amusement"))],
      sets=dict(_STEELMOP_SETS, maxwell="maximum_steelmop")),
]
