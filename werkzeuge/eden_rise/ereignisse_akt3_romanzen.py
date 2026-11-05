# -*- coding: utf-8 -*-
"""Akt 3, Paket E: Romanzen fertig spielen (Drehbuch 6) und die Freundschaften und Paare zwischen Yacht und Dorf (Drehbuch 7,
E-122 h, E-124, E-125, E-127). Bogen: Akt 1 Duldung, Akt 2 Zusammenarbeit, Akt 3 Gemeinschaft.

Schluss-Szenen: je Frau eine Karte (eine Phase), sobald ihre Leiter oben ist (rm_<k>4 oder <pid>_zusammen; Bibi und Megan
eigene Bedingungen), Tag 24 bis 33, Chiaras Blackout erst ab Tag 32. Flag a3_schluss_<pid>.
Freundschaften: sieben kleine Szenen ueber den Leiter-Mechanismus (Pflicht mit wann.leiter: hoechstens eine am Tag,
kern/ereignisse.pflicht_ziehen), Tag 26 bis 33. Je romanzierbarer Frau zwei Fassungen: "Duc hat die Romanze" (Leiter-Stufe
3 oder zusammen oder offen) neckt oder unterstuetzt, sonst die volle Fassung. Nur Holm und Petru, Charly und Danzel werden
ein Paar. Jede Szene hat eine Duc-Wahl mit Wirkung im Festbild (Flag a3_paar_<id>_<wahl>)."""
from ereignisse_basis import *  # noqa: F401,F403
from ereignisse_gag1 import P1  # noqa: E402
from ereignisse_ligeia import G  # noqa: E402
from ereignisse_akt3_woche4 import FR, FL, NICHT, DA, AKT3, JE, FRAME, DIREKT, tags_fuer  # noqa: E402

KAPUTT = FL("tk_yacht_weg")
LEITER = {"chiara": "c", "sophia": "s", "lea": "l", "rosi": "r", "lola": "o", "alva": "a", "siri": "i"}


def oben(pid):
    """Leiter oben: Stufe 4 der Leiter oder zusammen."""
    if pid == "megan":
        return FL("megan_funke")
    if pid == "bibi":
        return {"alle": [FL("rt_bibi_bleibt"), {"wert": ["begehren.bibi", ">=", 4]}]}
    return {"eine": [FL("rm_%s4" % LEITER[pid]), FL(pid + "_zusammen")]}


def romanze(pid):
    """Duc hat die Romanze (Drehbuch 7): Leiter-Stufe 3 oder zusammen oder offen."""
    return {"eine": [FL("rm_%s3" % LEITER[pid]), FL(pid + "_zusammen"), FL(pid + "_offen")]}


def NACHT_MIT(pid):
    return {"eine": [FL("bl_ab_fertig_" + pid), FL("bl_na_fertig_" + pid)]}


# ------------------------------------------------------------------ Drehbuch 6: Schluss-Szenen
def SCHLUSS(pid, bild, titel, lage, zeilen, chips, sets=None, eid=None):
    opt = [O(t, [F("a3_schluss_" + pid), F("a3_schluss_%s_%d" % (pid, i)), V(pid, 4)] + ([B(pid, 4)] if pid != "megan" else []), zeile=z)
           for i, (t, z) in enumerate(chips)]
    return FR(eid or "a3_schluss_" + pid, bild, titel, lage, zeilen, opt, personen={"handelnd": pid, "betroffen": []}, sets=sets, ton="wholesome")


SCHLUESSE = [
    SCHLUSS("chiara", "bridge", "Blackout",
            "The evening of day 32. You are alone with Chiara on the bridge when every light goes out at once. Only the stars are left.",
            [JE(G("chiara", "[sigh] The night in the siege, on the bridge wing, when I rated the sky because I'd run out of things to count. It was a six.", "caring"), "rueck", NACHT_MIT("chiara")),
             JE(G("chiara", "[chuckle] The first day you came on board, I gave you a four. I'm not changing it. Yet.", "amusement"), "rueck", None),
             JE(G("chiara", "[sniff] And you gave me the good bandage. I never said thank you. I'm not saying it now either.", "embarrassment"), "verband", FL("bl_verband_chiara")),
             G("chiara", "[clear throat] First Officer. I don't know which breaker it is. What would you do?", "nervousness")],
            [("Holds the flashlight and lets her find it.", G("chiara", "[sigh] ...There. Light. For once I won't give it a number.", "love")),
             ("“The red one. Second row.”", G("chiara", "[laugh] Show-off. It was the red one.", "amusement")),
             ("“I don't know either. Let's find it together.”", G("chiara", "[sigh] Together. Okay. That's a ten. Nobody hears that number but you.", "love"))],
            sets={"chiara": "Bridge Night"}),
    SCHLUSS("alva", "alvas_bar", "The Board Is Full",
            "Alva's bar after closing time. Papa's chalk board is full of names. There is one empty space at the bottom.",
            [JE(G("alva", "[chuckle] The evening on the quay, in the siege, when I gave out drinks and wrote down every glass. You paid the first round. You did.", "amusement"), "rueck", FL("bl_alva_runde")),
             G("alva", "[sigh] My name isn't on Papa's board. What do you write next to it?", "nervousness")],
            [("Writes ALVA and, next to it, “stays”.", G("alva", "[sniff] Stays. ...Idiot. Okay. Stays.", "love")),
             ("Writes ALVA and leaves the space next to it empty.", G("alva", "[chuckle] Empty. So I can choose. You know me too well.", "caring")),
             ("Gives her the chalk back. “You write it.”", G("alva", "[sigh] Me? ...Fine. Don't look.", "embarrassment"))],
            sets={"alva": "alva_standard"}),
    SCHLUSS("lea", "swim_platform", "One More Dive",
            "The mouth of the grotto, at low tide. You sit with Lea on the flat rock that is an island twice a day.",
            [JE(G("lea", "[chuckle] Two fingers, side by side, the sign I showed you on the foredeck, the night of the siege.", "love"), "rueck", NACHT_MIT("lea")),
             JE(G("lea", "[chuckle] The squid, the night they came up to the swim platform and you made the okay sign at me.", "joy"), "rueck", None),
             G("lea", "[sigh] The Azores letter is still in my bag. If I go, will you come and see me? Proper see me?", "nervousness")],
            [("“Yes. Not fast, but yes.”", G("lea", "[laugh] Not fast. That's very you.", "love")),
             ("“Stay. The bay will need you.”", G("lea", "[sniff] The bay. ...And you?", "love")),
             ("Holds up two fingers and says nothing.", G("lea", "[sigh] Two fingers. Okay. That's an answer.", "love"))],
            sets={"lea": "Dive"}),
    SCHLUSS("sophia", "aft_deck", "The Sixteenth Letter",
            "Sophia has a letter from a publisher in her hand. Fifteen publishers said no to her novel. This is number sixteen, and it is still closed.",
            [G("sophia", "[chuckle] Ten euros, the bet that you'd ask me what I actually want. You did ask. I still owe you the answer.", "amusement"),
             G("sophia", "[sigh] Darling, will you open it, or shall I?", "nervousness")],
            [("Gives her the letter. “It's yours.”", G("sophia", "[gasp] ...Yes. It says yes. Oh God.", "joy")),
             ("Opens it and reads the first line out loud.", G("sophia", "[sniff] Read it again. Slowly.", "love")),
             ("Puts it in her notebook, unopened. “Later. Together.”", G("sophia", "[sigh] Together. That's the best line anyone ever wrote for me.", "love"))],
            sets={"sophia": "Writing Night"}),
    SCHLUSS("rosi", "generator_room", "Two Thirds",
            "The engine room. Rosi is wiping her hands for the third time, which means she wants to say something.",
            [G("rosi", "[clear throat] Remember the night with the stopwatch? Nobody lost. ...Officer. If I say 'Captain' now, is that an insult or a promotion?", "nervousness")],
            [("“A promotion. I'll take it.”", G("rosi", "[laugh] Then, Captain. Don't let it go to your head. It's a small head.", "love")),
             ("“Neither. Say Duc.”", G("rosi", "[sigh] ...Duc. That's harder than Captain.", "love")),
             ("Laughs and hands her the spanner.", G("rosi", "[chuckle] A draw. So nobody won. I'll take it.", "amusement"))],
            sets={"rosi": "Engine Room"}),
    SCHLUSS("lola", "village_harbour", "First Guest, Again",
            "Lola's hut on the beach. One table, two chairs, a pan that is too big.",
            [JE(G("lola", "[laugh] The night in the siege you said yes to the toastie, and it wasn't burnt. Not even a bit.", "joy"), "rueck", NACHT_MIT("lola")),
             JE(G("lola", "[chuckle] You remember the first morning on the yacht? You ate my eggs and didn't make a face.", "joy"), "rueck", None),
             G("lola", "[sigh] Boss. If I cook for you here, will you sit down? Properly? No running off?", "nervousness")],
            [("Sits down and puts his phone away.", G("lola", "[sniff] Phone away. Oh, mate. Okay. Okay.", "love")),
             ("“Only if you sit down too.”", G("lola", "[laugh] Me? Sit? ...Mostly I can do that.", "love")),
             ("“Can I help?”", G("lola", "[chuckle] You can stir. Badly. Perfect.", "amusement"))],
            sets={"lola": "Off Duty"}),
    SCHLUSS("siri", "village_harbour", "No Caption",
            "Sunset on the quay. Siri has left her phone on the yacht. Her hands don't know what to do.",
            [G("siri", "[sigh] The sunset on the foredeck, when I told you I hadn't written my own caption since I was nineteen. "
                       "If this was a photo, what would you write under it?", "nervousness")],
            [("“Nothing. Some things don't need words.”", G("siri", "[sniff] Nothing. That's the best caption.", "love")),
             ("“Siri, in her own words.”", G("siri", "[chuckle] My own words. I'll think of some.", "love")),
             ("Takes her hand and doesn't answer.", G("siri", "[sigh] ...Okay. No caption.", "love"))],
            sets={"siri": "Dad's Sweater"}),
    SCHLUSS("bibi", "mochis", "Mochi",
            "The last collar. An old lion sleeps by the campfire at the station, and Bibi has the knife.",
            [G("bibi", "[sigh] The night at the campfire with the three of us, when I said 'until every collar is off', and you didn't laugh. "
                       "This is the last one. He's asleep. Do I cut it, or do you?", "nervousness")],
            [("“You. He's yours.”", G("bibi", "[sniff] Mine. ...There. Off. Every one of them.", "love")),
             ("“Together.”", G("bibi", "[laugh] Together. Hold his head. Gently.", "love")),
             ("Hands her the knife without a word.", G("bibi", "[sigh] You always know when to shut up. I love that. Oops.", "embarrassment"))]),
    SCHLUSS("megan", "vip_cabin", "Still Off the Record",
            "Megan closes the cabin door and leans against it.",
            [G("megan", "[sigh] That night I called you and said it was off the record. You never told anyone. "
                        "This stays off the record too, First Officer. Can you do that?", "nervousness")],
            [("“I already did, Megan.”", G("megan", "[chuckle] How... reassuring.", "love")),
             ("“Only if you call me Duc.”", G("megan", "[sigh] ...Duc. Don't make it a habit.", "love")),
             ("Nods and closes the door behind him.", G("megan", "[clear throat] Good. Then we never speak of it.", "desire"))],
            sets={"megan": "Boardroom"}),
    SCHLUSS("megan", "village_harbour", "Still Off the Record",
            "Her cabin is still a building site, so Megan walks with you to the end of the quay, where nobody can hear.",
            [G("megan", "[sigh] That night I called you and said it was off the record. You never told anyone. "
                        "This stays off the record too, First Officer. Can you do that?", "nervousness")],
            [("“I already did, Megan.”", G("megan", "[chuckle] How... reassuring.", "love")),
             ("“Only if you call me Duc.”", G("megan", "[sigh] ...Duc. Don't make it a habit.", "love")),
             ("Nods and stays next to her in the dark.", G("megan", "[clear throat] Good. Then we never speak of it.", "desire"))],
            sets={"megan": "Boardroom"}, eid="a3_schluss_megan_kai"),
]

# ------------------------------------------------------------------ Drehbuch 7: Freundschaften und Paare (Leiter, eine am Tag)
def _paar_wann(bed, phase="abend", tage=(26, 33)):
    w = WANN(tage, [phase], bed={"alle": [AKT3] + bed}, pflicht=True, holt_leute=True)
    w["leiter"] = True
    return w


def PAAR(id, titel, phase, bed, bild, personen, lage, zeilen, chips, sets=None, tage=(26, 33)):
    """chips: [(text, kurz, zeile)] - jede setzt a3_paar_<id> und a3_paar_<id>_<kurz>."""
    basis = id.split("_")[0]
    opt = [O(t, [F("a3_paar_" + basis), F("a3_paar_%s_%s" % (basis, k))], zeile=z) for t, k, z in chips]
    return E("a3_paar_" + id, "gag1", "wholesome", titel, _paar_wann(bed + [NICHT(FL("a3_paar_" + basis))], phase, tage), bild, personen, lage, zeilen, opt, sets=sets)


WO = lambda gast, haus: JE(G(gast[0], gast[1], gast[2]), "wo", {"alle": [KAPUTT, NICHT(FL("tk_haus_weg_" + haus))]})

PAARE = [
    # 7.1 Lola und Ba Tu: Familienliebe
    PAAR("lola", "You, Now", "fruehstueck", [DA("lola"), NICHT(romanze("lola"))], "batu_shop", P1("batu", ("lola", "+", "is learning")),
         "Bà Tư's shop, early. Lola has come to help again. Bà Tư is teaching her to wash rice. Lola does it too fast.",
         [G("batu", "[sigh] Again. Slower. You cook like you're running away.", "caring"),
          G("lola", "[chuckle] I sort of am, Auntie. Mostly from the dishes. ...My Nan in Byron Bay is ninety-one. Once she called the coast guard because I didn't ring on a Sunday.", "joy"),
          JE(G("batu", "[clear throat] The first time you came to my shop, I said: you, later. Now: you, now.", "caring"), "teller", {"gesehen": "g1_batu_intro"}),
          JE(G("batu", "[clear throat] In my shop, the first plate goes to family. Here. You, now.", "caring"), "teller", None),
          G("lola", "[gasp] Boss, she's adopting me. Is that allowed?", "surprise")],
         [("“Say yes before she changes her mind.”", "ja", G("batu", "[chuckle] I don't change my mind. Eat.", "caring")),
          ("Sits down and holds out his own plate.", "teller", G("batu", "[laugh] You too. Later.", "amusement")),
          ("“Call your Nan and ask her.”", "nan", G("lola", "[laugh] Nan says: is she feeding you? Then she's family.", "joy"))],
         sets={"lola": "Off Duty"}),
    PAAR("lola_duc", "You, Now", "fruehstueck", [DA("lola"), romanze("lola")], "batu_shop", P1("batu", ("lola", "+", "is learning")),
         "Bà Tư's shop, early. Lola is learning to wash rice. Bà Tư watches the pot and Lola at the same time.",
         [G("batu", "[clear throat] Mina says the Boss eats at your table now. Good. You feed him. He's too thin.", "caring"),
          G("lola", "[gasp] Auntie! ...I feed him toast, mainly.", "embarrassment"),
          G("batu", "[chuckle] In my shop, the first plate goes to family. Here. You, now. And you tell him he can come, too. Later.", "caring")],
         [("“Later is fine.”", "spaeter", G("batu", "[laugh] Good boy.", "amusement")),
          ("Sits down next to Lola anyway.", "teller", G("lola", "[chuckle] Told you he's stubborn, Auntie.", "joy"))],
         sets={"lola": "Off Duty"}),
    # 7.2 Chiara und Alva: Freundschaft
    PAAR("chiara", "Olivetti", "abend", [DA("chiara"), NICHT(romanze("chiara")), NICHT(romanze("alva"))], "alvas_bar",
         P1("alva", ("chiara", "+", "dries the glasses wrong")),
         "Alva's bar, late. Chiara dries the glasses, wrongly. Alva lets her.",
         [WO(("chiara", "[chuckle] I sleep upstairs now. Your sofa is a seven.", "amusement"), "bar"),
          G("chiara", "[clear throat] Four. Your glasses are a four. The bar is a nine.", "neutral"),
          G("alva", "[chuckle] And me?", "curiosity"),
          G("chiara", "[sigh] Not on the scale. Scales are for things.", "embarrassment"),
          G("alva", "[laugh] Due Olivetti, per favore. ...Nobody makes me laugh in my own bar. That's my job, Hamburg.", "joy"),
          G("chiara", "[sigh] There was someone once. Saint-Tropez. I never told anyone. ...I'm telling you. "
                      "First Officer, is it strange to get a best friend at twenty-nine? I never had one.", "nervousness")],
         [("“It's not strange. It's a nine.”", "neun", G("alva", "[chuckle] A nine. She'll take it.", "amusement")),
          ("Smiles and says nothing.", "still", G("chiara", "[sigh] Good answer. Seven.", "caring")),
          ("“Tell her, not me.”", "sag", G("alva", "[sniff] ...Ten. Don't you dare cry, Hamburg.", "caring"))]),
    PAAR("chiara_duc", "Olivetti", "abend", [DA("chiara"), {"eine": [romanze("chiara"), romanze("alva")]}], "alvas_bar",
         P1("alva", ("chiara", "+", "dries the glasses wrong")),
         "Alva's bar, late. Chiara dries the glasses, wrongly. Alva lets her.",
         [JE(G("alva", "[chuckle] Mina says you rated the First Officer a nine and a half. Out loud. In a bar.", "amusement"), "tratsch", romanze("chiara")),
          JE(G("chiara", "[chuckle] So. You and the First Officer. Lola told me, and Lola tells everybody. Hiding it: a three.", "amusement"), "tratsch", None),
          JE(G("chiara", "[sigh] That's a classified number. ...Is it strange that she's nice to me now?", "embarrassment"), "frage", romanze("chiara")),
          JE(G("chiara", "[sigh] I was jealous of you for three weeks. That's a ten in jealousy. I'm retiring now.", "embarrassment"), "frage", None)],
         [("“It's the best thing that happened all week.”", "gut", G("alva", "[laugh] Then stay for a drink, Hamburg.", "joy")),
          ("“She's nice to everyone. You just noticed.”", "alle", G("alva", "[shush] Not to everyone.", "amusement"))]),
    # 7.3 Isabelle und Sophia: Freundschaft
    PAAR("sophia", "A Line in the Margin", "abend", [DA("sophia"), NICHT(romanze("sophia"))], "church",
         P1("sophia", ("isabelle", "+", "has exploded something again")),
         "Isabelle has come down from the monastery with her herb basket, and something in it has exploded again. Sophia helps her clean up, without a show.",
         [JE(G("sophia", "[chuckle] I sleep up at the monastery now, in a cell with a crucifix. Very good for writing.", "amusement"), "wo", KAPUTT),
          G("isabelle", "[gasp] Sorry. Sorry, it was only rosemary.", "embarrassment"),
          G("sophia", "[chuckle] Darling, I've seen worse things explode. Usually men.", "amusement"),
          G("isabelle", "[sigh] Mina once said to me, up on the hill: you could have left. Did you ever leave somewhere, Sophia?", "curiosity")],
         [("“She did. Ask her where.”", "frag", G("sophia", "[sigh] Everywhere. Then I stopped. Here, write this down.", "caring")),
          ("“Isabelle, you can ask her anything. She's a good friend.”", "freundin", G("isabelle", "[sniff] A friend. I've never had one outside the walls.", "gratitude")),
          ("Leaves them alone.", "allein", G("sophia", "[chuckle] He's tactful. Rare in a man.", "amusement"))],
         sets={"sophia": "Writing Night"}),
    PAAR("sophia_duc", "A Line in the Margin", "abend", [DA("sophia"), romanze("sophia")], "church",
         P1("sophia", ("isabelle", "+", "is curious")),
         "Isabelle has come down from the monastery with her herbs. Sophia is helping her sort them on the church steps.",
         [G("isabelle", "[chuckle] Mina says you and the officer talk every night. She just knows things. Is it true?", "curiosity"),
          G("sophia", "[sigh] Darling, Mina knows everything. Don't tell Lea. ...Here. For when you want to leave somewhere. Or stay.", "caring"),
          G("isabelle", "[sigh] She's brave, isn't she? Is it hard, being brave?", "curiosity")],
         [("“Ask her. She'll tell you it isn't.”", "frag", G("sophia", "[chuckle] It isn't. It's terrible. Do it anyway.", "amusement")),
          ("“Yes. She does it anyway.”", "ja", G("isabelle", "[sniff] Anyway. I like that word.", "gratitude"))],
         sets={"sophia": "Writing Night"}),
    # 7.4 Mina und Lea: Freundschaft
    PAAR("lea", "Two Letters", "dinner", [DA("lea"), NICHT(romanze("lea"))], "village_piazza", P1("mina", ("lea", "+", "has a letter too")),
         "Mina's Vespa in front of the post office. Mina and Lea sit on it, not going anywhere.",
         [WO(("lea", "[chuckle] Mina's flat has a hundred and four letters in it. I counted. I sleep next to them.", "amusement"), "post"),
          G("lea", "[gasp] Did you know some letters are older than the people who carry them?", "curiosity"),
          G("mina", "[sigh] I know. I carry one. It's from my brother. In Montréal. I never opened it.", "sadness"),
          G("lea", "[sigh] I have one too. The Azores. I opened it. That's worse.", "sadness"),
          G("mina", "[chuckle] If you go, I'll bring your post. To the Azores. On the Vespa. ...Yacht. Do you think we should open them? Both?", "curiosity")],
         [("“Together, then. On the same day.”", "zusammen", G("lea", "[laugh] Same day. Deal.", "joy")),
          ("“Only if you both want to.”", "frei", G("mina", "[sigh] Only if. Okay.", "caring")),
          ("“Not yet. Keep them for the festa.”", "festa", G("mina", "[chuckle] The festa. Then I'll open it with everybody watching. Terrible. Okay.", "amusement"))],
         sets={"lea": "Off Duty"}),
    PAAR("lea_duc", "Two Letters", "dinner", [DA("lea"), romanze("lea")], "village_piazza", P1("mina", ("lea", "+", "is red")),
         "Mina's Vespa in front of the post office. Lea sits on the back.",
         [G("mina", "[chuckle] So. You and the Yacht. I didn't read it anywhere. I just know.", "amusement"),
          G("lea", "[gasp] Did you know octopuses can change colour? I'm doing that now.", "embarrassment"),
          G("mina", "[laugh] If he's slow, honk at him. I'll lend you the horn. ...Duc, Lea says you're slow. Are you slow?", "amusement")],
         [("“Very. On purpose.”", "langsam", G("lea", "[laugh] On purpose. Mina, he's doing it on purpose!", "joy")),
          ("Holds up two fingers.", "finger", G("lea", "[sigh] ...Two fingers. Okay. Not slow.", "caring"))]),
    # 7.5 Holm und Petru: die spaete Liebe (immer voll)
    PAAR("holm", "The Metre", "abend", [FL("holm_zurueck")], "petru_workshop", P1("holm", ("petru", "+", "sits a metre away")),
         "The bench outside Petru's workshop, in the evening. Holm and Petru sit on it. There is one metre between them.",
         [WO(("holm", "[chuckle] Petru's spare room has a boat engine in it. I sleep next to a boat engine. Very Norwegian.", "amusement"), "werkstatt"),
          G("holm", "[clear throat] My mother is coming. For the festa. She wants to see the man who taught me to sit still.", "neutral"),
          G("petru", "[clear throat] Who?", "neutral"),
          G("holm", "[sigh] Don't. ...Frankfurt. Are you lost, or are you staying?", "embarrassment")],
         [("Walks on quietly.", "still", G("petru", "[clear throat] Hm.", "approval")),
          ("“Evening, you two.”", "stoeren", G("holm", "[sigh] Go away, Frankfurt.", "annoyance")),
          ("Sits down on the far end of the bench.", "bank", G("petru", "[clear throat] Hm. Beer.", "neutral"))],
         sets={"holm": "holm_shirt"}),
    # 7.6 Bibi und Maxwell: Freundschaft, Bones (vor Tag 30)
    PAAR("bones", "Six Kilos of Bad Temper", "nachmittag", [FL("rt_bibi_bleibt"), FL("mochis_offen"), {"mochi": "geier"}],
         "mochis", P1("bibi", ("maxwell", "-", "is scared of the sky")),
         "The animal station in the afternoon. Maxwell carries two buckets of bones, as far from the sky as possible. Above him circles Bones, "
         "the bearded vulture, with three metres of wing.",
         [G("maxwell", "[gasp] Eish! Bibi. The big bird is looking at Mr. Maximum.", "fear"),
          G("bibi", "[laugh] That's Bones. Six kilos. Three metres of wing, and six kilos! He's mostly air and bad temper. He's looking at the bucket, Maxwell.", "joy"),
          G("maxwell", "[sigh] Everything that flies scares me, sister. Everything. And soon I sit in a plane.", "fear"),
          G("bibi", "[chuckle] A plane is just a big bird with no bad temper. Here. Hold out your hand.", "caring"),
          G("maxwell", "[gasp] ...Mr. Maximum fed the worst bird in Corsica. Number One. Is it the same, a plane and a bird? Tell me it is the same.", "surprise")],
         [("“It's the same. Only the plane is nicer.”", "gleich", G("maxwell", "[laugh] Nicer. Okay. Lekker.", "relief")),
          ("“No. The plane is safer. Bones is not.”", "sicher", G("bibi", "[laugh] True. Bones bites.", "amusement")),
          ("Puts a bone in his own hand, next to Maxwell's.", "hand", G("maxwell", "[chuckle] Two brave men. Brother.", "gratitude"))], tage=(26, 29)),
    # 7.7 Charly und Danzel: ein Paar (E-127)
    PAAR("charly", "Ten", "abend", [FL("rt_charly_bleibt"), NICHT(FL("rt_charly_weg"))], "village_piazza",
         P1("danzel", ("charly", "+", "sits on the floor")),
         "Le Théâtre Rouge, late. Fabric everywhere. On the counter, a cash register with open cables. Charly sits on the floor with her laptop. Danzel sews.",
         [G("danzel", "[gasp] Halt! Nobody touches the fabric, or nobody... nobody touches it very much.", "nervousness"),
          G("charly", "[sigh] Four out of ten. You got shorter again.", "neutral"),
          G("charly", "[clear throat] The cash register works. It says 'Merci' in a robot voice. I couldn't make it stop.", "neutral"),
          G("danzel", "[clear throat] Hold still. Your left sleeve has been two centimetres short for three years. I noticed on the first day. Here. A pullover. "
                      "A pocket for your laptop. And RED, inside the collar. Small.", "caring"),
          G("charly", "[sigh] ...Ten. I want to stay. Here. In the shop. With you. That's not a rating, Danzel.", "love"),
          G("danzel", "[gasp] Then... then nobody leaves! Nobody leaves very... nobody leaves. ...Duc, did you hear that?", "love")],
         [("“That was the best ten I've ever heard.”", "zehn", G("charly", "[chuckle] Then it stays a ten. Don't tell Bibi. She'll cry louder than him.", "love")),
          ("“Give him a nine next time, so he stays humble.”", "neun", G("danzel", "[laugh] Never! I will never be humble!", "joy")),
          ("Looks at Danzel, who is crying into a curtain, and quietly leaves them alone.", "allein", G("charly", "[sigh] Seven out of ten for crying. Come here.", "love"))]),
]

# Duc 05.11.2026 (Empfehlung 5): Megans Schluss-Karte endet vor Monaco (Tag 30), Holms Warnung kommt erst an Tag 31.
# Darum warnt Megan selbst, am Abend vor ihrem letzten Fenster. Am Kai, weil ihre Kabine kaputt sein kann.
from ereignisse_akt3_woche4 import PFL  # noqa: E402
MEGAN_TUER = [
    E("a3_megan_tuer", "gag1", "wholesome", "The Day After Tomorrow",
      PFL(29, "nacht", {"alle": [FL("megan_zurueck"), oben("megan"), NICHT(FL("a3_schluss_megan"))]}), "village_harbour", P1("megan"),
      "Late at night Megan finds you on the quay. She has her phone in her hand and doesn't look at it.",
      [G("megan", "[clear throat] Monaco calls me the day after tomorrow, First Officer. After that, I am a different person for a while. "
                  "If you want a word with me as I am now, tomorrow evening is the time.", "nervousness")],
      [O("“Tomorrow evening, then.”", [F("a3_megan_tuer")],
         zeile=G("megan", "[sigh] Good. Don't be late. I hate waiting almost as much as I hate saying this.", "embarrassment")),
       O("Nods and walks her back.", [F("a3_megan_tuer"), V("megan", 1)])]),
]

EVENTS = SCHLUESSE + PAARE + MEGAN_TUER

_KARTE = {"chiara": ("A Moment on the Bridge", ["abend"], [{"tag_ab": 32}]), "megan": ("Megan's Cabin", ["abend"], [{"nicht": {"tag_ab": 31}}])}
ORTE = {}
for _pid in ("chiara", "alva", "lea", "sophia", "rosi", "lola", "siri", "bibi", "megan"):
    _label, _ph, _extra = _KARTE.get(_pid, ("A Moment with " + _pid.capitalize(), ["nachmittag", "abend"], []))
    ORTE["a3_schluss_" + _pid] = {
        "label": _label, "bild": next(e["bild"] for e in SCHLUESSE if e["id"] == "a3_schluss_" + _pid), "phasen": _ph,
        "text": "She has been waiting for a moment with you alone. Takes the whole phase.",
        "wenn": {"alle": [AKT3, oben(_pid), NICHT(FL("a3_schluss_" + _pid)), {"nicht": {"tag_ab": 34}}]
                 + ([DA(_pid)] if _pid not in ("megan", "bibi") else []) + _extra},
        "start": ([{"wenn": {"alle": [KAPUTT, NICHT(FL("a3_yacht_repariert"))]}, "id": "a3_schluss_megan_kai"}] if _pid == "megan" else [])
                 + [{"id": "a3_schluss_" + _pid}]}


def tags_schreiben():
    return tags_fuer(EVENTS, "akt3_romanzen")
