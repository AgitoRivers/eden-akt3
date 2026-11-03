# -*- coding: utf-8 -*-
"""Handy - 30 Events: Videoanrufe und Nachrichten, auf die Duc reagieren muss.
bild = wo Duc ist ("ort_duc" = aktueller Raum), personen.anrufer_ort = Hintergrund im Handy."""
from ereignisse_basis import *  # noqa: F401,F403

H = lambda anrufer, ort, art="video", bei_dir=None: dict({"anrufer": anrufer, "anrufer_ort": ort, "art": art},
                                                         **({"bei_dir": bei_dir} if bei_dir else {}))
NACHT = ["nacht"]
TAG = ["fruehstueck", "tag", "dinner"]

EVENTS = [
    E("hy_lola_tresen", "handy", "frech", "Lola Dances on the Bar", WANN((3, 6), NACHT, bed={"wert": ["vertrauen.alva", ">=", 2]}),
      ORT_DUC, H("alva", "alvas_bar"), "Alva calls from the bar. Behind her, Lola is dancing barefoot on the "
                                       "counter. The fishermen are clapping.",
      [Z("alva", "O figliolu, your cook is teaching my fishermen to twerk. It's very educational.", "amusement"),
       Z("alva", "Come and get her. Or don't. Bring nothing but yourself.", "desire"),
       Z("lola", "BOSS! The universe says hi!", "excitement")],
      [O("Takes the tender over.", [EN(-1), V("lola", 6), V("alva", 6), F("lola_kater")]),
       O("“Let her dance. Put it on my tab.”", [G(-40), V("alva", 4), V("lola", 4), W("moral", 1), I("bauchnabelpiercing")]),
       O("Has Chiara call her.", [V("chiara", -4), V("lola", -4), R(3)])],
      sets={"alva": "alva_standard"}),

    E("hy_sophia_0213", "handy", "frech", "02:13", WANN((3, 6), NACHT, bed={"wert": ["vertrauen.sophia", ">=", 3]}), "duc_cabin",
      H("sophia", "crew_corridor"), "At 02:13 Sophia texts: “Are you awake?” Then she calls. She's lying in the "
                                    "dark, her face lit only by the screen. The notebook rests on her chest, and the "
                                    "duvet has slipped a long way down.",
      [Z("sophia", "I wrote something about you. I want to read it to you before I lose my nerve.", "nervousness"),
       Z("sophia", "He listens like it costs him nothing, and that is the most expensive thing I've ever been given.", "love"),
       Z("sophia", "Okay. That's all. Unless you want to tell me what you'd do if you were here. Slowly.", "desire")],
      [O("“Read it again.”", [B("sophia", 6), V("sophia", 4), NK("sophia")]),
       O("Quietly tells her what he'd do.", [], probe=P("charm", 13),
         erfolg=[B("sophia", 8), NK("sophia"), EN(-1), MO("night_call", ["sophia"])],
         fehlschlag=[B("sophia", 4)],
         zeile=Z("sophia", "Keep talking. Don't stop. I'm… my hand is already… God, Duc. Don't stop.", "desire")),
       O("Just “Good night, Sophia.”", [V("sophia", 6), NK("sophia")]),
       O("Doesn't pick up.", [F("sophia_vergessen")], art="auflegen")],
      sets={"sophia": "Writing Night"}, knistern=True,
      nachklang_text="You hardly slept. Her voice at 02:13 is still there, very close to your ear."),

    # hy_megan_erster_anruf entfernt (18.10.2026): Megans erster Anruf ist jetzt eine feste Story-Szene am Morgen von Tag 2
    E("hy_holm_krankenhaus", "handy", "ernst", "Holm Calls from the Hospital", WANN((2, 3), ["abend"]), ORT_DUC,
      H("holm", "krankenhaus"), "Holm is lying in a hospital bed with tubes in her arm, her hair down for once. She "
                                "looks pale, and very angry that she isn't on board.",
      [Z("holm", "They took my appendix and my boat on the same day. Only one of them I want back. How is she?", "annoyance"),
       Z("holm", "And don't lie to me, Frankfurt. I can hear it in your voice when you lie. You get polite.", "neutral")],
      [O("Tells her honestly how bad it is.", [V("holm", 8), R(3)],
         zeile=Z("holm", "Good. Now I know you'll tell me the truth when it matters.", "approval")),
       O("Reassures her: “Everything's under control.”", [], probe=P("cunning", 14), erfolg=[V("holm", 2)], fehlschlag=[V("holm", -6)]),
       O("Asks for her advice.", [V("holm", 6), F("holm_rat")],
         zeile=Z("holm", "Trust your engineer. Feed your crew. And never let them see you guess.", "caring"))]),

    E("hy_holm_nacht", "handy", "wholesome", "Holm Can't Sleep", WANN((3, 6), NACHT, bed={"wert": ["vertrauen.holm", ">=", 2]}),
      ORT_DUC, H("holm", "krankenhaus"), "Holm calls in the middle of the night. The painkillers have made her "
                                         "talkative. She tells you about her first command, a rusty freighter out of "
                                         "Bergen.",
      [Z("holm", "My first command was a rust bucket out of Bergen. Thirty-one, terrified, and nobody listened to me "
                 "for a month.", "amusement"),
       Z("holm", "Then one night I said, I don't know, let's find out together. After that they listened. Funny, hm?", "caring")],
      [O("Listens until she falls asleep.", [V("holm", 6), R(5), EN(-1), I("holms_foto")]),
       O("Tells her about himself.", [V("holm", 4), F("holm_kennt_duc")]),
       O("“Get some sleep, Captain.”", [V("holm", 2)])]),

    E("hy_megan_mitternacht", "handy", "frech", "Megan at 23:40", WANN((3, 4), NACHT, bed={"wert": ["vertrauen.megan", ">=", 2]}),
      ORT_DUC, H("megan", "megan_office"), "Megan calls at 23:40. She's still at the office, shoes off, a glass of "
                                           "whisky in her hand. Behind her the harbour glitters.",
      [Z("megan", "Everyone in this building is afraid of me. It's very boring. Entertain me, First Officer.", "neutral"),
       Z("megan", "And don't mention the boat. I know about the boat. Tell me something nobody tells me.", "curiosity")],
      [O("Tells her something personal.", [V("megan", 6), GAG("megan_lacht")]),
       O("Flirts with her.", [], probe=P("charm", 14), erfolg=[V("megan", 8), F("megan_flirt")], fehlschlag=[V("megan", -4)],
         zeile=Z("megan", "Careful. I bite. Contractually.", "amusement")),
       O("“Go home, Megan.”", [V("megan", 4)],
         zeile=Z("megan", "Nobody tells me to go home. …Fine. You first.", "embarrassment"))],
      sets={"megan": "Boardroom"}),

    E("hy_megan_feuern", "handy", "witzig", "Megan Wants to Fire Someone", WANN((3, 4), ["tag"]), ORT_DUC,
      H("megan", "megan_office"), "Megan has decided that someone from the crew gets fired. You're to name them. Now.",
      [Z("megan", "I've decided someone gets fired. For morale. Pick a name. You have ten seconds.", "pride"),
       Z("megan", "Nine. Eight. I'm counting in my head, it's more threatening.", "amusement")],
      [O("Gives her no name.", [], probe=P("courage", 12), erfolg=[V("megan", 8), R(5), GAG("megan_lacht")], fehlschlag=[V("megan", 2), R(5)],
         zeile=Z("megan", "Correct answer. It was a test. Nobody ever passes. Ahaha— don't tell anyone I laughed.", "amusement")),
       O("“Then fire me.”", [V("megan", 6), R(8)]),
       O("Suggests Totò, as a joke.", [V("megan", 4), V("toto", -6), GAG("megan_lacht")])],
      sets={"megan": "Boardroom"}),

    E("hy_elsa_vorwarnung", "handy", "ernst", "Elsa's Warning", WANN((3, 6), ["abend", "nacht"], bed={"wert": ["vertrauen.elsa", ">=", 4]}),
      ORT_DUC, H("elsa", "village_harbour"), "Elsa calls from the harbour. She's speaking quietly. Tomorrow morning "
                                             "there'll be a raid for smuggling in the bay. She isn't saying it as a "
                                             "police officer.",
      [Z("elsa", "I never called you. Tomorrow, seven o'clock, we search every boat in the bay. Every locker.", "neutral"),
       Z("elsa", "If your bosun has something he shouldn't, tonight would be a good night for swimming lessons.", "caring")],
      [O("“Thank you, Elsa.” Warns Totò.", [V("elsa", 6), V("toto", 6), F("razzia_vorbereitet")]),
       O("Doesn't warn Totò.", [V("elsa", 2), F("razzia_unvorbereitet")]),
       O("“Why are you helping me?”", [V("elsa", 4)],
         zeile=Z("elsa", "Because you didn't try to bribe me. People always try. You just asked questions.", "admiration"))]),

    E("hy_elsa_segler", "handy", "wholesome", "A Drifting Sailboat", WANN((3, 6), ["tag"], bed={"wert": ["vertrauen.elsa", ">=", 1]}),
      ORT_DUC, H("elsa", "village_harbour"), "Elsa needs help. A small sailboat is drifting off the bay with two "
                                             "tourists on board and a dead engine. Her patrol boat is too far away.",
      [Z("elsa", "A little sailboat is drifting at the mouth of the bay. Two Germans, no engine, a lot of shouting.", "neutral"),
       Z("elsa", "My boat is twenty minutes out. Your tender is two. Can you help?", "curiosity")],
      [O("Lea takes the tender.", [], probe=P("courage", 11), erfolg=[V("elsa", 6), V("lea", 6), W("ruf", 1)],
         fehlschlag=[V("elsa", 4), V("lea", 4)]),
       O("Duc goes himself.", [EN(-1), V("elsa", 8), W("ruf", 1), I("elsas_abzeichen")]),
       O("“No time, sorry.”", [V("elsa", -4)])]),

    E("hy_cousin_falsch", "handy", "witzig", "Wrong Number from Bastia", WANN((2, 6), NACHT), ORT_DUC,
      H("toto", "village_harbour", art="nachricht"), "A message from an unknown number: “Gennaro here. Parcel comes "
                                                     "tonight. Tell Salvatore the goat is coming too 🐐” Totò is "
                                                     "Salvatore. Totò is reading over your shoulder, and he goes "
                                                     "pale.",
      [Z("toto", "Comandante. That message. It's a wrong number. Gennaro is a very common name. Very common. Goats "
                 "too.", "nervousness"),
       Z("toto", "Okay. Okay. My cousin brings a small parcel tonight. And maybe a small goat. It's a long story.", "embarrassment")],
      [O("“No goat on board.”", [V("toto", -2), GAG("toto_cousin")]),
       O("“How small is the goat?”", [V("toto", 6), W("moral", 1), GAG("toto_cousin"), F("ziege_an_bord")],
         zeile=Z("toto", "Small! Medium. A medium goat. She's very polite.", "joy")),
       O("Tips off Elsa.", [V("elsa", 6), V("toto", -10)])]),

    E("hy_lola_ziege", "handy", "witzig", "Lola Got Lost", WANN((2, 6), ["tag"], an_land=True), ORT_DUC,
      H("lola", "petru_workshop"), "Lola calls from ashore. She was only supposed to buy lemons. Now she's standing "
                                   "in Petru's workshop with a goat on a lead and no idea how that happened.",
      [Z("lola", "Boss. Don't be mad. I went for lemons, and now I have a goat. Her name's Fiona. She chose me.", "nervousness"),
       Z("lola", "Petru says she eats everything. I said, same, girl. We bonded.", "amusement")],
      [O("“Fiona comes with us.”", [V("lola", 6), W("moral", 1), F("ziege_an_bord"), GAG("toto_cousin")]),
       O("“Take her back. And bring the lemons.”", [V("lola", -2), V("petru", 2)]),
       O("Asks Petru what's going on.", [V("petru", 4)], zeile=Z("lola", "He just pointed at the goat and then at me. "
                                                                       "Very poetic, mate.", "confusion"))],
      sets={"lola": "Off Duty"}),

    E("hy_rosi_foto", "handy", "frech", "Rosi's Photo", WANN((3, 6), ["abend", "nacht"], bed={"wert": ["begehren.rosi", ">=", 2]}),
      ORT_DUC, H("rosi", "power_room", art="nachricht"), "Rosi sends a photo of the spare part she's looking for. It "
                                                         "isn't a spare part. It's a mirror selfie in a towel, fresh "
                                                         "out of the shower. Thirty seconds later she calls.",
      [Z("rosi", "DELETE THAT. That was the wrong photo. The part is the other photo. Why aren't you deleting it?", "embarrassment"),
       Z("rosi", "…Unless you liked it. Did you like it? Say something, you idiot, I'm dying here.", "nervousness")],
      [O("“I'll delete it. Right after I save it.”", [B("rosi", 6), V("rosi", 2), NK("rosi")],
         zeile=Z("rosi", "You're the worst. Keep it. I'll send you a better one when I'm brave.", "amusement")),
       O("Tells her how much he liked it.", [], probe=P("courage", 12), erfolg=[B("rosi", 8), NK("rosi"), EN(-1), I("rosis_foto")],
         fehlschlag=[B("rosi", 2)], zeile=Z("rosi", "Okay. Okay. Then this one's on purpose. Don't show Totò.", "desire")),
       O("Really deletes it, the perfect gentleman.", [V("rosi", 6)])],
      sets={"rosi": "Off Duty"}, knistern=True,
      nachklang_text="A steamed-up mirror, a towel, Rosi's grin. At breakfast she asks, too loudly, whether anyone "
                     "has seen a spare part."),

    E("hy_lea_plankton", "handy", "wholesome", "The Glowing Sea", WANN((2, 6), NACHT, bed={"wert": ["vertrauen.lea", ">=", 2]}),
      ORT_DUC, H("lea", "swim_platform"), "Lea calls from the swim platform. She's holding the phone in the water. "
                                          "Every movement makes the plankton glow blue. She whispers as if she were "
                                          "in a church.",
      [Z("lea", "Look. Look look look. Every time I move my hand, the sea lights up. Like it's happy to see me.", "excitement"),
       Z("lea", "I didn't want to see this alone. Come down? Just for a minute. I'll be quiet. I'll try.", "caring")],
      [O("Goes down.", [V("lea", 6), B("lea", 6), NK("lea"), MO("glowing_sea", ["lea"])],
         zeile=Z("lea", "Give me your hand. In the water. See? Now we're both glowing.", "love")),
       O("Swims with her.", [], probe=P("courage", 11), erfolg=[B("lea", 8), NK("lea"), EN(-1)], fehlschlag=[V("lea", 4), W("moral", 1)]),
       O("“Send me a video.”", [V("lea", 2)])],
      sets={"lea": "Leopard Bikini"}, knistern=True,
      nachklang_text="Blue light between your fingers. In the morning Lea has salt in her hair and smiles at you as "
                     "if you shared a secret."),

    E("hy_siri_ungeschminkt", "handy", "wholesome", "Siri Without a Filter", WANN((2, 6), NACHT, bed={"wert": ["vertrauen.siri", ">=", 3]}),
      ORT_DUC, H("siri", "foredeck"), "Siri calls from the foredeck. No make-up, hair tied back, an old jumper. She "
                                      "says it's the first time in years she's called anyone without a filter.",
      [Z("siri", "No ring light, no filter. This is just my face. It's the first time in two years I've called someone like this.", "nervousness"),
       Z("siri", "Say something nice. Or say something true. I can't tell which one I need.", "sadness")],
      [O("Says something true.", [V("siri", 8), NK("siri"), U("siri_marke", 1)]),
       O("Says something kind.", [V("siri", 4), B("siri", 4)]),
       O("Asks her to switch the camera off and just talk.", [], probe=P("empathy", 12),
         erfolg=[V("siri", 8), B("siri", 4), NK("siri"), EN(-1)], fehlschlag=[V("siri", 4)])],
      sets={"siri": "Dad's Sweater"}, knistern=True,
      nachklang_text="Her face without a filter, her laugh without an audience. At breakfast she's wearing make-up "
                     "again, but she winks at you."),

    E("hy_megan_rundgang", "handy", "witzig", "A Live Tour for Megan", WANN((3, 4), ["tag"]), ORT_DUC,
      H("megan", "megan_office"), "Megan wants a tour, live by video, right now. You walk through the yacht with "
                                  "the phone, and she comments on everything.",
      [Z("megan", "Walk me through my boat. Now. And hold the phone straight, I get seasick through screens.", "neutral"),
       Z("megan", "Why is there a goat. No, don't explain. Show me the engineer. Is she working? She looks like she's working.", "confusion")],
      [O("Shows Rosi at work.", [V("megan", 6), V("rosi", 4)],
         zeile=Z("rosi", "Hello, Mrs Boss. Everything is broken. Lovely to meet you.", "amusement")),
       O("Shows Lola's galley.", [V("megan", 2), V("lola", 4), GAG("megan_lacht")],
         zeile=Z("lola", "Hiii! Want a cookie? It's a normal cookie. Mostly.", "joy")),
       O("“No signal!” Hangs up.", [], probe=P("cunning", 12), erfolg=[V("megan", -2)], fehlschlag=[V("megan", -8)], art="auflegen")],
      sets={"megan": "Boardroom"}),

    E("hy_alva_diesel_tanz", "handy", "frech", "A Canister for a Dance", WANN((3, 6), ["abend"], bed={"wert": ["vertrauen.alva", ">=", 2]}),
      ORT_DUC, H("alva", "alvas_bar"), "Alva has one canister of diesel left. She won't sell it, but she'll trade it "
                                       "for a dance, tonight, on her bar, in front of the whole village.",
      [Z("alva", "One canister. Not for money. For a dance. Tonight. On my bar. In front of everyone.", "desire"),
       Z("alva", "Don't make that face. You'll be wonderful. And if not, you'll be funny. Both sell drinks.", "amusement")],
      [O("Dances.", [], probe=P("courage", 12), erfolg=[V("alva", 8), W("ruf", 1)],
         fehlschlag=[V("alva", 4), W("moral", 1), KL("duc", "alva", "Duc danced on Alva's bar")]),
       O("Sends Lola.", [V("lola", 4), V("alva", 2), F("lola_kater")]),
       O("“I'd rather pay.”", [V("alva", -2)])]),

    E("hy_sophia_kaffee", "handy", "wholesome", "Sophia's Hint", WANN((2, 6), ["fruehstueck", "tag"]), ORT_DUC,
      H("sophia", "main_salon", art="nachricht"), "Sophia sends a short message: Chiara has been sitting alone in "
                                                  "the pantry for an hour, staring at a cup. Maybe someone could "
                                                  "bring her a fresh coffee.",
      [Z("sophia", "Chiara has been staring at one cup for an hour. I'd go, but she'd pretend to be fine for me. Not for you. ☕", "caring"),
       Z("sophia", "Two sugars. She'll say she doesn't take sugar. She takes two. 🙄", "amusement")],
      [O("Brings her a coffee.", [V("chiara", 6), V("sophia", 4)]),
       O("Thanks Sophia, goes later.", [V("sophia", 2)]),
       O("“Why don't you go?”", [V("sophia", 4)], zeile=Z("sophia", "Because I organise people, darling. You "
                                                                        "actually see them. 😘", "admiration"))]),

    E("hy_lola_koster", "handy", "witzig", "Taster Wanted", WANN((2, 6), ["tag", "dinner"]), ORT_DUC,
      H("lola", "galley"), "Lola calls from the galley, her face covered in flour. She's invented something and "
                           "needs a taster right now. Behind her a pot is smoking, but in a good way.",
      [Z("lola", "Boss, emergency. I invented a dish. It's either the best thing ever or a crime. I need a mouth. "
                 "Yours.", "excitement"),
       Z("lola", "It's got fish, lemon, fennel and a secret. The secret is love. And chilli. Mostly the chilli.", "joy")],
      [O("Runs straight over to taste it.", [], probe=P("courage", 10), erfolg=[V("lola", 6), W("moral", 1), I("lolas_gewuerz")],
         fehlschlag=[V("lola", 4), EN(-1)], zeile=Z("lola", "Your face! Is that a good face? That's a good face. I'm crying.", "joy")),
       O("Sends Rosi.", [V("rosi", 2), V("lola", 2)]),
       O("“I trust you. Just go for it.”", [V("lola", 4)])],
      sets={"lola": "Galley"}),

    E("hy_holm_letzter_anruf", "handy", "ernst", "“She's Your Boat.”", WANN((6, 6), ["abend"], bed={"wert": ["vertrauen.holm", ">=", 2]}),
      ORT_DUC, H("holm", "krankenhaus"), "Holm calls on the evening before the hearing. She's sitting up straight in "
                                         "bed, wearing her captain's cap, just for this call.",
      [Z("holm", "Tomorrow it gets decided, one way or another. I wanted you to hear it from me before it does.", "neutral"),
       Z("holm", "She's your boat now, Frankfurt. Whatever you choose, choose it out loud. They'll follow that.", "pride")],
      [O("“Thank you, Captain.”", [V("holm", 6), R(8)]),
       O("“She'll come back to you.”", [V("holm", 8)], zeile=Z("holm", "Good. Then take care of her for me. Both of you.", "caring")),
       O("Asks her for one last order.", [V("holm", 4), R(5)], zeile=Z("holm", "Sleep. That's the order. Heroes who don't sleep make bad decisions.", "caring"))]),

    # Wrong Chat (Duc 26.10.2026) ersetzt "Megan, by Accident" (Goldmaske): nur in der versteckten Romanze, nach
    # "Private Number" (megan_funke_2). Das Foto bleibt Item megan_screenshot (Glücksbringer Charm bei Megan).
    E("hy_megan_wrong_chat", "handy", "frech", "Wrong Chat", WANN((4, 6), NACHT, bed={"flag": "megan_funke_2"}), ORT_DUC,
      H("megan", "megan_office", "nachricht"),
      "Twenty to midnight. A photo from the private number, no text. A tall mirror in a bedroom above Port Hercule, "
      "the harbour lights behind her, and Megan in nothing but a thin gold chain with a small anchor. Forty seconds "
      "later, a second message.",
      [Z("megan", "That was meant for a different chat. I'd think very carefully about what you do next, First "
                  "Officer.", "embarrassment"),
       Z("megan", "Delete it. Or don't. But if anyone on that boat ever sees it, I'll know exactly whose phone it "
                  "came from. ⚓", "desire")],
      [O("Deletes it and says nothing.", [V("megan", 6)],
         zeile=Z("megan", "Hm. A gentleman. How disappointing. 🙄 Goodnight, Duc.", "amusement")),
       O("Keeps it.", [], probe=P("charm", 13), erfolg=[V("megan", 4), F("megan_funke_3"), I("megan_screenshot")],
         fehlschlag=[V("megan", -4)],
         zeile=Z("megan", "There is no other chat, is there. Goodnight, Duc. Delete nothing. 🖤", "desire")),
       O("Sends back a photo of the radar screen.", [V("megan", 2)],
         zeile=Z("megan", "A radar screen. 📡 How... romantic. Go to sleep, First Officer.", "amusement"))],
      sets={"megan": "Boardroom"}, knistern=True),

    E("hy_toto_spind", "handy", "witzig", "A Break-In at Totò's Locker", WANN((2, 6), ["tag", "abend"]), ORT_DUC,
      H("toto", "crew_mess"), "Totò calls in a panic, whispering. Someone is in his locker. He can hear rustling and "
                              "crunching. He doesn't dare open the door.",
      [Z("toto", "Comandante. Someone is in my locker. I hear rustling. Crunching. Come quick, and bring something "
                 "heavy.", "fear"),
       Z("toto", "Oh. Oh no. It has wings. It has wings and it's eating my cigars.", "surprise")],
      [O("Heads over with a broom.", [], probe=P("courage", 10), erfolg=[V("toto", 6), GAG("kevin")], fehlschlag=[V("toto", 2), GAG("kevin"), W("moral", 1)],
         zeile=Z("toto", "Kevin. Of course it's Kevin. He took a cigar. He looks happier than me.", "annoyance")),
       O("Sends Lea.", [V("lea", 4), V("toto", 2), GAG("kevin")]),
       O("Laughs out loud.", [V("toto", -4), W("moral", 1), GAG("kevin")])]),
]

item("bauchnabelpiercing", "Belly Button Piercing with a Shell", "geschenk", text="Alva puts it on your tab for Lola. "
                                                                              "Lola loves it.")
item("rosis_foto", "A Photo You Shouldn't Delete", "andenken", text="Rosi knows you have it. Visible in "
                                                                               "the epilogue.")
item("eden_cap", "Eden-Group-Kappe", "geschenk", text="White, with a golden anchor. Totò loves it, Siri hates it.")
item("lolas_gewuerz", "Lola's Spice Mix", "geschenk", text="A jar of “Ocean Glitter”. Rosi loves it.")
item("megan_screenshot", "Wrong Chat", "gluecksbringer", effekt={"vorteil": "charm"},
     text="She says it was a mistake. Megan McAllister doesn't make mistakes. Once a day: advantage on Charm with Megan.")
item("elsas_abzeichen", "Gendarmerie Maritime Badge", "gluecksbringer", effekt={"vorteil": "courage"},
     text="Elsa tossed it to you. Once a day: advantage on Courage.")
item("holms_foto", "Foto von Holms erstem Kommando", "andenken", text="A rusty freighter off Bergen, a young woman "
                                                                      "in a cap.")
