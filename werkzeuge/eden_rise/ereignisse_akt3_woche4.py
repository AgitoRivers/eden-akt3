# -*- coding: utf-8 -*-
"""Akt 3, Woche 4 "The Morning After" (Tag 24-28, Paket B). Drehbuch: docs/wiki/welt/drehbuch_akt3.md, Abschnitte 4.1, 4.4, 5.1-5.11.

Pflicht: a3_morgen (24 Fruehstueck), a3_schwur (24 Tag), a3_uhr (25 Fruehstueck), a3_megan_landet (25 Dinner),
a3_festa_tafel (26 Fruehstueck), a3_sonntag (28 Tag), a3_berichte (29 Abend, gehoert zum Bogen der Schublade).
Karten (Orte in auftraege_eden_rise.py, kosten die Phase): Lend a Hand (a3_bau_*), Alva (a3_alva_*), Siri (a3_siri_*),
Nonnas Kiste (a3_nonna_*). Dank-Szenen am Morgen nach dem fertigen Haus (a3_dank_*), Reparatur der Yacht (a3_yacht_*).
Alles erst spielbar, wenn modul.akt3_spielbar an ist (kern/abschluss.py). Jede gesprochene Zeile mit Turbo-Tag (G)."""
import json, os

from ereignisse_basis import *  # noqa: F401,F403
from ereignisse_gag1 import P1  # noqa: E402
from ereignisse_ligeia import G, STIMME as _LIGEIA  # noqa: E402

HIER = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(os.path.dirname(HIER))
DIREKT = lambda ziel: {"direkt": ziel}
WEITER = lambda ziel: {"weiter": ziel}
FRAME = lambda: WANN((24, 35))                         # nie gezogen, nur ueber "direkt" geoeffnet
AKT3 = {"flag": "akt2_ende"}                           # Akt 3 beginnt nach dem Cliffhanger


def PFL(tag, phase, bed=None):
    b = {"alle": [AKT3, bed]} if bed else AKT3
    return WANN((tag, tag), [phase], bed=b, pflicht=True, holt_leute=True)


def JE(zl, gruppe, wenn):
    """Zeile nur, wenn die Bedingung passt; je Gruppe gilt die erste passende (kern/ereignisse.zeilen_aktiv)."""
    return dict(zl, gruppe=gruppe, wenn=wenn)


NICHT = lambda b: {"nicht": b}
FL = lambda name: {"flag": name}
KAPUTT = FL("tk_yacht_weg")
DA = lambda pid: NICHT(FL("gefeuert_" + pid))
BAU = lambda hid: {"aufbau_beginnen": hid}


def FR(id, bild, titel, lage, zeilen, optionen, personen=None, sets=None, ton="wholesome"):
    """Frame einer Karte (Ortskapitel): wiederholbar, kostet zusammen mit den anderen Frames der Karte eine Phase."""
    return E(id, "ort", ton, titel, WANN((24, 35)), bild, personen or {}, lage, zeilen, optionen, sets=sets)


# ------------------------------------------------------------------ 5.1 The Morning After (Tag 24, Fruehstueck)
MORGEN = [
    E("a3_morgen", "gag1", "ernst", "The Morning After", PFL(24, "fruehstueck"), "village_piazza",
      P1("mina", ("petru", "?", "is watching you"), ("anghjulu", "?", "is standing at the church door"), ("jana", "?", "has not slept")),
      "Day 24. The village spent the night in the church, and nobody slept much. Smoke still hangs over the square. "
      "The church door is open. The door to the back room behind the altar is shut. You are holding two cups of coffee. "
      "On someone's phone, Alon's video is playing again, and a man near the fountain asks it out loud: Did you know?",
      [G("mina", "[sigh] Sorry, Yacht. I don't know what to say to you today.", "sadness")],
      [O("Puts both coffees down on the fountain. “My company belongs to the Eden Group. I didn't know they sold your harbour.”",
         [V("casanova", 2), DIREKT("a3_morgen_petru")]),
       O("“No, I didn't know. And I'm staying here until you believe me.”", [W("ruf", 1), DIREKT("a3_morgen_petru")]),
       O("Stays where he is and says nothing.", [DIREKT("a3_morgen_petru")])]),
    E("a3_morgen_petru", "gag1", "ernst", "The Morning After", FRAME(), "village_piazza",
      P1("petru", ("jana", "?", "wants to ask something"), ("anghjulu", "?", "is guarding the back room")),
      "Petru steps out of the crowd and stands in front of you. He looks at you for a long time. Then he turns to the others.",
      [JE(G("petru", "[clear throat] Hm. I rowed out with the village, like in 1924, and he held the church until we came back. "
                     "Three days. That's all I need to know.", "neutral"), "petru", FL("bl_dorf_rudert")),
       JE(G("petru", "[clear throat] Three days he stood between the fire and the church. That's all I need to know.", "neutral"), "petru", None),
       G("jana", "[sniff] Sir... Minicu. Is he... nobody will tell me.", "fear"),
       G("anghjulu", "[sigh] Not today, my child. Pray for him, and leave that door shut.", "sadness"),
       JE(G("lola", "[clear throat] Right! Who wants breakfast? I made heaps. Mostly the eggs.", "nervousness"), "essen", DA("lola")),
       JE(G("batu", "[sigh] Eat. Everybody eat. I made too much, like always.", "caring"), "essen", None)],
      [O("Picks up his coffee again and goes to the church door to wait with Don.", [V("anghjulu", 2), F("a3_morgen_fertig")],
         zeile=G("anghjulu", "[sigh] You can wait with me, my son. But you can't go in. Nobody can.", "sadness")),
       O("Sits down next to Jana and eats something, so she does too.", [V("jana", 2), F("a3_morgen_fertig")],
         zeile=G("jana", "[sniff] Okay. One egg. For Minicu.", "sadness"))]),
]

# ------------------------------------------------------------------ 5.2 The Oath (Tag 24, Tag)
SCHWUR = [
    E("a3_schwur", "gag1", "ernst", "The Oath", PFL(24, "tag"), "village_harbour",
      P1("bonaventure", ("casanova", "-", "has her arms folded"), ("petru", "?", "waits")),
      "The harbour. The Eventually is tied up at the quay, its purple flag at half-mast. Forty men stand on the stones, "
      "and none of them is holding a torch. One of them holds up a phone. A news video is playing: pirates attacked a small village.",
      [G("bonaventure", "[laugh] I am famous! Look, Paco, that is our flag! ...Robots? I have never owned a robot in my life. "
                        "They are saying I had robots!", "surprise"),
       G("bonaventure", "[clear throat] We burned your houses. I gave the order to stop, and I gave it too late. I am sorry.", "remorse"),
       G("bonaventure", "I don't know how a man makes that right. I have a flag, an anthem and forty men who can carry stones. "
                        "[sigh] We will find a way. I swear it.", "remorse"),
       G("casanova", "[sigh] You burned the post office.", "anger"),
       G("bonaventure", "[sigh] Yes, Madame. ...Señor. You beat me twice. So you decide. Do we stay and carry stones, or do we sail away?", "remorse"),
       JE(G("bibi", "[chuckle] Forty men. I'm counting them. Don't ask me why yet.", "curiosity"), "bibi",
          {"alle": [FL("rt_bibi_bleibt"), FL("mo_eco_idee")]})],
      [O("“Stay. Start with the houses you burned.”", [F("buenaventura_schwur"), V("bonaventure", 4), DIREKT("a3_schwur_ende")],
         zeile=G("petru", "[clear throat] Hm. Then carry stones.", "neutral")),
       O("Turns to Madame Casanova. “Ask her, not me. It's her village.”", [F("buenaventura_schwur"), V("casanova", 4), DIREKT("a3_schwur_ende")],
         zeile=G("casanova", "[sigh] Stay. And carry everything twice.", "neutral")),
       O("“Stay. And when the commission comes, you tell them who paid you.”", [F("buenaventura_schwur"), F("a3_buenaventura_aussage"), DIREKT("a3_schwur_ende")],
         zeile=G("bonaventure", "[laugh] Of course. I am a pirate, not a liar.", "pride"))]),
    E("a3_schwur_ende", "gag1", "wholesome", "The Oath", FRAME(), "village_harbour",
      P1("bonaventure", ("petru", "?", "is already giving orders")),
      "The pirates put their hats back on. One of them still has a burnt-out torch on his belt.",
      [G("bonaventure", "[clear throat] Leave that.", "neutral"),
       G("bonaventure", "[sigh] ...Señor, the burned houses are building sites now. My men will carry, but only where somebody "
                        "lays the first stone. Tell us where to start.", "neutral")],
      [O("“I'll show you. Today.”", [F("a3_schwur_fertig")]),
       O("Looks up at the burned roofs. “Give me a day to choose.”", [F("a3_schwur_fertig")])]),
]

# ------------------------------------------------------------------ 4.1 Lend a Hand (Karte, ein Frame je Baustelle)
BESITZER = {"post": ("mina", "Mina", "Post Office"), "batu": ("batu", "Bà Tư", "Bà Tư's shop"),
            "bar": ("alva", "Alva", "Alva's bar"), "werkstatt": ("petru", "Petru", "Petru's workshop")}
FOLGE = ["post", "batu", "bar", "werkstatt"]


def _offen(hid):
    return {"alle": [FL("tk_haus_weg_" + hid), NICHT(FL("aufbau_begonnen_" + hid))]}


def _naechste(hid):
    """Weiter zur naechsten offenen Baustelle (Reihenfolge der Karte), sonst zurueck."""
    i = FOLGE.index(hid)
    rest = FOLGE[i + 1:] + FOLGE[:i]
    return WEITER([{"wenn": _offen(h), "id": "a3_bau_" + h} for h in rest] + [{"id": "a3_bau_" + hid}])


BAU_LAGE = {
    "post": "The post office has no roof. Mina's old Vespa is lying in the ashes, black with soot. Mina is sorting letters on the steps anyway.",
    "batu": "Bà Tư's shop is black inside. The sign is still there, half of it. Bà Tư is cooking in the street, on a gas ring.",
    "bar": "Alva's bar is a shell. Papa's chalk board hangs on the one wall that is still standing.",
    "werkstatt": "Petru's workshop is open to the sky. The tools are hanging on the wall, black, in the right order.",
}
BAU_ZEILE = {
    "post": G("mina", "[chuckle] You want to start here? With my post office? Okay. I'll hold the ladder. It's what I do.", "gratitude"),
    "batu": G("batu", "[sigh] Here, con? First you eat. Then you carry. Then you eat again.", "caring"),
    "bar": G("alva", "[cough] My bar first? ...I'm not saying thank you. Write that down.", "gratitude"),
    "werkstatt": G("petru", "[clear throat] Here. Wood first, then we talk. A house is like a boat. You start with the bones.", "approval"),
}
BAU_BILD = {"post": "village_piazza", "batu": "batu_shop", "bar": "alvas_bar", "werkstatt": "petru_workshop"}   # beim Haus, nicht am Hafen
PIRAT = {"post": "the pirate who burned it", "batu": "the pirate who burned it", "bar": "the pirate who burned it",
         "werkstatt": "the pirate who burned it"}

BAU = [
    FR("a3_bau_" + hid, BAU_BILD[hid], "Lend a Hand: " + BESITZER[hid][2],
       BAU_LAGE[hid] + " Who holds the first stone with you?",
       [BAU_ZEILE[hid]],
       [O("Lays the first stone here, with %s." % BESITZER[hid][1], [BAU(hid), V(BESITZER[hid][0], 4)]),
        O("Lays the first stone here, with one of the pirates who set the fire.", [BAU(hid), V("bonaventure", 2), W("ruf", 1)],
          zeile=G("bonaventure", "[clear throat] Paco! You burned it. You carry it.", "neutral")),
        O("Lays the first stone here, with someone from the crew.", [BAU(hid), W("moral", 1)]),
        O("Walks on to the next building site.", [_naechste(hid)])],
       personen={"handelnd": BESITZER[hid][0], "betroffen": []}) for hid in FOLGE
]

# ------------------------------------------------------------------ Dank-Szenen (am Morgen nach dem fertigen Haus)
def _dank(hid):
    return WANN((25, 35), ["fruehstueck"], bed={"alle": [AKT3, {"flag_seit": ["aufbau_fertig_" + hid, 1]}]}, pflicht=True, holt_leute=True)


DANK = [
    E("a3_dank_post", "gag1", "wholesome", "The First Post", _dank("post"), "village_piazza", P1("mina", ("casanova", "+", "is reading")),
      "The post office has a roof again. Mina rides past the harbour on her Vespa and honks twice. The first letter after the fire is not a bill.",
      [G("mina", "[laugh] Yacht! A postcard. From Montréal. It's not for me, it's for the baker. But still!", "joy"),
       G("mina", "[clear throat] You did this. So listen. Every day I go to Bastia anyway. What do you need? I'll bring it.", "gratitude"),
       G("mina", "[clear throat] And one more thing. The day the phones were dead, I knocked on every door. I saw who opened and who didn't. "
                 "If the commission asks, I'll tell them. Will you want me to?", "neutral")],
      [O("“Yes. Tell them what you saw.”", [F("a3_zeuge_mina"), F("a3_zeuge_mina_ehrlich"), V("mina", 6)],
         zeile=G("mina", "[sigh] Okay. I'm scared. But okay.", "nervousness")),
       O("“Only if you want to, Mina. It's your name, not mine.”", [F("a3_zeuge_mina"), F("a3_zeuge_mina_frei"), V("mina", 4)],
         zeile=G("mina", "[sniff] Then I want to. Nobody asked me that before.", "gratitude")),
       O("“Think about it. Ask me again next week.”", [V("mina", 2)],
         zeile=G("mina", "[chuckle] Next week. You sound like the post.", "amusement"))]),
    E("a3_dank_batu", "gag1", "wholesome", "Two Plates", _dank("batu"), "batu_shop", P1("batu", ("lola", "+", "gets a plate too")),
      "Bà Tư's shop is open again. She puts two plates on the counter, and the second one is for Lola.",
      [G("batu", "[sigh] Eat. You're too thin, con. Both of you.", "caring"),
       G("batu", "[clear throat] Men in white. Twice they asked me for the north road. I told you then. "
                 "If the men from Ajaccio ask, do I tell them too?", "neutral")],
      [O("“Yes. You told me first. Now tell them.”", [F("a3_zeuge_batu"), F("a3_zeuge_batu_ehrlich"), V("batu", 6)],
         zeile=G("batu", "[chuckle] Good. My mother was afraid of nobody. Me too.", "pride")),
       O("“Only if you're not afraid for the shop.”", [F("a3_zeuge_batu"), F("a3_zeuge_batu_frei"), V("batu", 4)],
         zeile=G("batu", "[sigh] I'm afraid. I still tell them. Eat.", "caring")),
       O("Eats first, and doesn't answer yet.", [V("batu", 2)],
         zeile=G("batu", "[chuckle] Smart boy. Eating first is always right.", "amusement"))]),
    E("a3_dank_bar", "gag1", "wholesome", "Papa's Board", _dank("bar"), "alvas_bar", P1("alva", ("sandru", "+", "brings the bread")),
      "Alva's bar is open again. On Papa's chalk board there is a new name, the first one after the fire.",
      [JE(G("alva", "[chuckle] Look. Under the new name somebody wrote: Everyone. Paid. D. That's you. You paid the first round, on the quay, in the siege.", "gratitude"),
          "board", FL("bl_alva_runde")),
       JE(G("alva", "[chuckle] Look. The first name after the fire. I wrote it myself. I'm not telling you whose it is.", "gratitude"), "board", None),
       G("alva", "[sigh] From the square, that night, I saw the north barricade open. Then the men in white came through. "
                 "Nobody believes me, because I was knocked out after. Will you stand next to me when I say it?", "neutral")],
      [O("“Yes. Every word.”", [F("a3_zeuge_alva"), F("a3_zeuge_alva_ehrlich"), V("alva", 6)],
         zeile=G("alva", "[sigh] Then I'll say it. Out loud. In front of men in suits. ...You'll owe me a drink for this.", "pride")),
       O("“They'll believe you. You don't need me for that.”", [F("a3_zeuge_alva"), F("a3_zeuge_alva_frei"), V("alva", 4)],
         zeile=G("alva", "[chuckle] Liar. A kind one. I'll take it.", "amusement")),
       O("“Let's open the bar first. Then we talk about the commission.”", [V("alva", 2)],
         zeile=G("alva", "[laugh] The bar first. You're learning, o figliolu.", "amusement"))]),
    E("a3_dank_werkstatt", "gag1", "wholesome", "The Rudder", _dank("werkstatt"), "petru_workshop", P1("petru", ("bonaventure", "+", "carried the beams")),
      "Petru's workshop has a roof again. He hangs the old rudder over the door, the one that came through the fire.",
      [G("petru", "[clear throat] The rudder stays over the door. My grandfather steered with it in 1924. Burned wood still knows the way home.", "pride"),
       G("petru", "[sigh] I saw the torches at my workshop. And I saw who stayed. A.V. bought the loan on my boat. "
                  "If I talk, they take the boat. You want me to talk?", "neutral")],
      [O("“Yes. And if they take your boat, we build you a new one.”", [F("a3_zeuge_petru"), F("a3_zeuge_petru_ehrlich"), V("petru", 6)],
         zeile=G("petru", "[chuckle] A new boat. You don't know how to build a boat. ...I'll teach you. Then I talk.", "approval")),
       O("“It's your boat, Petru. You decide.”", [F("a3_zeuge_petru"), F("a3_zeuge_petru_frei"), V("petru", 4)],
         zeile=G("petru", "[sigh] Nobody asked me that since my wife Marie died. I decide. I talk.", "neutral")),
       O("Says nothing and helps him with the rudder.", [V("petru", 2)],
         zeile=G("petru", "[clear throat] You hold it like a fisherman now. Good. ...I'll talk to them.", "approval"))]),
]

# ------------------------------------------------------------------ 5.3 Since Last Night (Karte Alva)
ALVA = [
    FR("a3_alva_wach", "village_piazza", "Since Last Night",
       "Mina found you: Sandru says come, and Sandru never says come. Alva is awake. She is lying on a camp bed at the front of "
       "the church, far away from the back room. Sandru sits on a stool next to her.",
       [G("alva", "[cough] How long?", "confusion"),
        G("sandru", "[laugh] Since last night. You missed the end. Ha. Sorry. That's not funny.", "nervousness"),
        G("alva", "[cough] And Minicu?", "fear"),
        G("sandru", "[sigh] Don won't let anyone in.", "sadness"),
        G("alva", "[sigh] Then we wait. ...Duc. Who carried me out? Don't lie to me, I'll know.", "neutral")],
       [O("“Sandru. He carried you out of the rubble.”", [F("a3_alva_wach"), V("sandru", 4), V("alva", 2)],
          zeile=G("alva", "[chuckle] ...Orangeade's on me, then. For a year.", "gratitude")),
        O("Looks at Sandru and waits.", [F("a3_alva_wach"), V("sandru", 6)],
          zeile=G("sandru", "[sigh] It was me. Okay? I'm thirty, Alva. I can carry things.", "embarrassment")),
        O("“Does it matter?”", [F("a3_alva_wach")],
          zeile=G("alva", "[sigh] Everything matters to me, Duc. That's my whole problem.", "sadness"))],
       personen={"handelnd": "alva", "betroffen": [{"id": "sandru", "ton": "?", "was": ""}]}, sets={"alva": "alva_morgen"}, ton="ernst"),
]

# ------------------------------------------------------------------ 5.4 Under Control (Tag 25, Fruehstueck)
TOTO_KISTE = {"alle": [{"versprochen": ["toto", "crate"]}, FL("gr_kiste_genommen"), NICHT(FL("alon_kiste_genutzt"))]}
ZU_TOTO = DIREKT([{"wenn": TOTO_KISTE, "id": "a3_uhr_toto"}, {"id": "a3_uhr_ende"}])
SAMSTAG = G("elsa", "[sigh] On Saturday I drive to Ajaccio. I want to see these 'all quiet' reports with my own eyes.", "neutral")
UHR = [
    E("a3_uhr", "gag1", "ernst", "Under Control", PFL(25, "fruehstueck"), "village_harbour",
      P1("elsa", ("mina", "?", "has a basket of letters")),
      "Elsa's phone lies on the harbour wall, on speaker. A tired man from Ajaccio is talking: Commissioner Luciani. "
      "“We received your file, Lieutenant. Two men from the commission will come in ten days, on Sunday. "
      "We are very busy here. And we have the feeling you have this under control. To be honest, we were surprised. "
      "Cala d'Orsu sends us a report every month. All quiet. Signed and stamped.”",
      [G("elsa", "[sigh] That's ten days. ...Five years on this post, and they have never been this polite to me.", "anger"),
       G("elsa", "[clear throat] I sent them a report every month too. Through the town hall. So where did mine go?", "realization"),
       G("mina", "[sigh] Twelve letters from Monaco, all signed by a lawyer in Lyon, Maître Delorme. One is for Petru. A.V. bought the loan on his boat. "
                 "And I have to take it to him. Me.", "sadness"),
       JE(G("mina", "[sniff] You let me go alone that day, when the phones were dead. I knocked on every door. I can do this too.", "pride"),
          "mina", FL("bl_tueren_mina")),
       G("elsa", "[clear throat] First Officer. The commission wants witnesses. People who saw it with their own eyes and will sign "
                 "their name. Will you help me find them?", "neutral")],
      [O("“I'll talk to every one of them.”", [F("a3_zeugen_auftrag"), V("elsa", 4), ZU_TOTO]),
       O("“What about the crew? We saw everything.”", [F("a3_zeugen_auftrag"), ZU_TOTO],
         zeile=G("elsa", "[sigh] You're guests. And Alon just called you his partner on television. The village has to speak for itself.", "neutral")),
       O("Takes Mina's basket. “Then we start with the letters.”", [F("a3_zeugen_auftrag"), V("mina", 4), ZU_TOTO],
         zeile=G("mina", "[chuckle] Okay. You knock. I'll hold the ladder.", "gratitude"))],
      sets={"elsa": "Standard"}),
    E("a3_uhr_toto", "gag1", "ernst", "Under Control", FRAME(), "village_harbour", P1("elsa", ("toto", "?", "is waiting")),
      "Elsa writes a list on the back of an envelope. At the top, she writes: Commission in 10 days.",
      [SAMSTAG,
       G("toto", "[clear throat] Comandante. The night we lost Gennaro, you promised me that crate would bring Alon down. "
                 "Do you give it to her now?", "grief")],
      [O("Hands Elsa the crate of collars from the grotto.", [F("alon_kiste_genutzt"), V("toto", 6)],
         zeile=G("toto", "[sniff] Madonna. ...Now it counts, Comandante.", "gratitude")),
       O("“Not yet, Totò. When the men from Ajaccio are here.”", [],
         zeile=G("toto", "[sigh] Not yet. Okay. But you remember.", "sadness"))],
      sets={"elsa": "Standard"}),
    E("a3_uhr_ende", "gag1", "ernst", "Under Control", FRAME(), "village_harbour", P1("elsa", ("mina", "?", "is waiting")),
      "Elsa writes a list on the back of an envelope. At the top, she writes: Commission in 10 days.",
      [SAMSTAG],
      [O("“Then we have ten days.”", [V("elsa", 2)]),
       O("Reads the list over her shoulder.", [])],
      sets={"elsa": "Standard"}),
]

# ------------------------------------------------------------------ 5.5 Until I Land (Tag 25, Dinner)
MEGAN = [
    E("a3_megan_landet", "gag1", "wholesome", "Until I Land", PFL(25, "dinner"), "village_harbour",
      P1("megan", ("rosi", "?", "has oil on her hands")),
      "No helicopter this time. A water taxi from Bastia, and one suitcase. Megan walks along the quay and stops in front of the yacht.",
      [JE(G("megan", "[sigh] How... delightful. Five days away, and my yacht is a wreck with people living in it.", "disapproval"), "yacht", KAPUTT),
       JE(G("megan", "[sigh] How... delightful. Three weeks, and my yacht becomes a field hospital.", "disapproval"), "yacht", None),
       JE(G("rosi", "[laugh] Don't worry. We fixed her once already, after the explosion. Twice is a tradition.", "pride"), "rosi", {"alle": [KAPUTT, DA("rosi")]}),
       JE(G("rosi", "[chuckle] It's only paint. Nearly only paint.", "pride"), "rosi", DA("rosi")),
       JE(G("megan", "[sigh] How reassuring. I'll call Monaco. They'll send parts, and a man who says 'unfortunately' a lot.", "annoyance"), "teile", KAPUTT),
       JE(G("holm", "[chuckle] Megan.", "neutral"), "holm", FL("holm_zurueck")),
       JE(G("megan", "[clear throat] Captain. You're standing.", "surprise"), "holm2", FL("holm_zurueck")),
       JE(G("holm", "[chuckle] On one leg, yes. Frankfurt did the rest.", "amusement"), "holm3", FL("holm_zurueck"))],
      [O("Takes her suitcase.", [DIREKT("a3_megan_frage")]),
       O("“Welcome back, Megan.”", [DIREKT("a3_megan_frage")])],
      sets={"megan": "Boardroom", "rosi": "Engine Room"}),
    E("a3_megan_frage", "gag1", "ernst", "Until I Land", FRAME(), "village_harbour", P1("megan"),
      "Megan pulls you away from the others, to the end of the quay.",
      [G("megan", "[clear throat] Duc. Alon thanked 'our partners at the Eden Group'. Did you know who was buying the harbour?", "neutral")],
      [O("“No. Did you?”", [DIREKT("a3_megan_handel")]),
       O("“I didn't know they were selling it at all.”", [DIREKT("a3_megan_handel")]),
       O("Doesn't joke this time. “Megan. I'd never sell these people.”", [V("megan", 2), DIREKT("a3_megan_handel")])],
      sets={"megan": "Boardroom"}),
    E("a3_megan_handel", "gag1", "ernst", "Until I Land", FRAME(), "village_harbour", P1("megan"),
      "She looks at the burned roofs for a moment before she speaks.",
      [G("megan", "[sigh] I negotiated that sale. Every line. I never asked who A.V. was, because the numbers were good. So that's two of us who didn't ask.", "remorse"),
       G("megan", "[clear throat] Here's the deal, First Officer. I'll try to stop the sale. The board in Monaco won't believe a video. "
                  "They want paper and names. Can you get me names?", "neutral")],
      [O("“I'm already collecting them.”", [F("megan_zurueck"), F("a3_megan_handel"), V("megan", 4)],
         zeile=G("megan", "[chuckle] Of course you are. How... efficient.", "approval")),
       O("“Why do you care now?”", [F("megan_zurueck"), F("a3_megan_handel")],
         zeile=G("megan", "[sigh] Because he nearly sank my ship. And because I signed it.", "sadness")),
       O("“And what's in it for you?”", [F("megan_zurueck"), F("a3_megan_handel")],
         zeile=G("megan", "[chuckle] A seat on the board. Obviously. And a quiet evening, maybe. Don't ask for more.", "pride"))],
      sets={"megan": "Boardroom"}),
]

# ------------------------------------------------------------------ 5.6 THIS. IS. THE. FESTA! (Tag 26, Fruehstueck)
TAFEL = [
    E("a3_festa_tafel", "gag1", "witzig", "THIS. IS. THE. FESTA!", PFL(26, "fruehstueck"), "village_piazza",
      P1("casanova", ("petru", "?", "is holding the ladder"), ("mina", "+", "claps too early")),
      "Madame Casanova has been here since five in the morning. There is a big board on the church wall, taller than she is. "
      "Kevin the gull is sitting on top of it.",
      [G("casanova", "[clear throat] Cala d'Orsu! They burned our houses. They want us to cancel the festa. So we will NOT!", "pride"),
       G("casanova", "[sigh] ...Thank you, Kevin.", "annoyance"),
       G("casanova", "[clear throat] Three columns. Building, food, decoration. Every name on this board is a person with a gift. "
                     "Nothing from the shop! ...Monsieur. Can I count on you, or should I count on someone else?", "neutral")],
      [O("“Count on me.”", [F("a3_festa_tafel"), V("casanova", 4)],
         zeile=G("casanova", "[sigh] Good. ...Good. That's all I wanted to know today. And somebody get that bird off the board!", "relief")),
       O("“Tell me who to start with.”", [F("a3_festa_tafel"), V("casanova", 2)],
         zeile=G("casanova", "[chuckle] With everyone, Monsieur. One at a time.", "amusement")),
       O("“Count on me. And on the pirates.”", [F("a3_festa_tafel"), V("casanova", 2), V("bonaventure", 2)],
         zeile=G("casanova", "[sigh] The pirates. On my festa. ...Fine. They carry the tables.", "annoyance"))]),
]

# ------------------------------------------------------------------ 5.7 Sunday (Tag 28, Tag)
SONNTAG = [
    E("a3_sonntag", "gag1", "ernst", "Sunday", PFL(28, "tag"), "church", P1("anghjulu", ("batu", "+", "has a tin for you")),
      "The church. A bucket stands in the first row, and it is dripping. Pascal paid for the new roof. That money has stopped. "
      "The rain hasn't. The door to the back room is still shut. Outside, a father takes down the bus timetable and folds it very small. "
      "The school bus won't come on Monday.",
      [G("anghjulu", "[clear throat] Today I'll keep it short, because the roof is listening. And pray quietly for the one in the back room.", "sadness"),
       G("batu", "[sigh] Eat. You're too thin. And don't look at the bus stop like that. You didn't stop that bus.", "caring")],
      [O("Takes the tin and goes outside after the mass.", [DIREKT("a3_sonntag_treppe")]),
       O("Eats one biscuit from the tin right away, so Bà Tư sees it.", [V("batu", 2), DIREKT("a3_sonntag_treppe")])],
      sets={"anghjulu": "anghjulu_standard"}),
    E("a3_sonntag_treppe", "gag1", "ernst", "Sunday", FRAME(), "village_piazza", P1("anghjulu"),
      "People with boxes stand at the town hall stairs. They want to throw everything Pascal owned into the harbour. "
      "Don stands in front of the door, alone.",
      [G("anghjulu", "[sigh] No. ...I know what he did, my son. I was there. Nobody goes in.", "anger"),
       G("anghjulu", "[clear throat] Monsieur Duc. They are asking you. Are you with them, or with an old priest?", "neutral")],
      [O("Walks up the stairs and stands next to Don.", [V("anghjulu", 6), F("a3_don_tuer"), F("a3_zeuge_tuer_don"), DIREKT("a3_sonntag_zimmer")],
         zeile=G("anghjulu", "[sigh] Thank you, my son. My knees are not as brave as my mouth.", "gratitude")),
       O("“Elsa is on her way. Leave it for her.”", [V("anghjulu", 2), DIREKT("a3_sonntag_zimmer")],
         zeile=G("anghjulu", "[sigh] ...They are putting the boxes down. Logic. I never tried that.", "relief")),
       O("Stays at the bottom of the stairs.", [DIREKT("a3_sonntag_zimmer")],
         zeile=G("anghjulu", "[sigh] Then I stand here alone. I have done it before.", "sadness"))],
      sets={"anghjulu": "anghjulu_standard"}),
    E("a3_sonntag_zimmer", "gag1", "ernst", "The Drawer", FRAME(), "village_piazza", P1("elsa", ("anghjulu", "?", "opens the door")),
      "Elsa comes up the stairs with a crowbar. Behind the door is Pascal's room: a desk, an empty hook, and a lighter square on the wall "
      "where a picture used to hang. She opens the locked drawer.",
      [G("elsa", "[clear throat] My antenna form. Eleven months. Every week Pascal told me: 'Almost through.'", "anger"),
       G("elsa", "[sigh] My reports to the mayor. Never delivered. Madame Casanova's EU applications, signed, never sent. "
                 "And copies of the monthly report to Ajaccio. 'All quiet.' His signature.", "realization"),
       JE(G("elsa", "[clear throat] Three o'clock, the night of the twenty-second. I wrote it down myself, that night. Two words from the north road: 'Not yet.'", "neutral"),
          "wache", {"alle": [FL("bl_wache_gesehen"), FL("bl_nachtwache_elsa")]}),
       JE(G("elsa", "[clear throat] Holm told me about three o'clock. Here it is. The night of the twenty-second, from the north road, two words: 'Not yet.'", "neutral"),
          "wache", FL("bl_wache_gesehen")),
       G("elsa", "[sigh] And this. A cash book in the same neat handwriting. The roof. The school bus. The festa money. And here: the priest. "
                 "Sandru. ...Madame Casanova.", "sadness"),
       G("elsa", "[clear throat] This goes to the commission. All of it, or only his part? Think about it until then.", "neutral")],
      [O("“All of it.”", [F("a3_kassenbuch"), F("a3_kassenbuch_alles_vor")],
         zeile=G("elsa", "[sigh] For the record: I'd make the same face you're making.", "neutral")),
       O("“Only Alon's part. The village has paid enough.”", [F("a3_kassenbuch"), F("a3_kassenbuch_teil_vor")],
         zeile=G("elsa", "[sigh] Kind. I'm not sure it's right. But it's kind.", "neutral")),
       O("“I don't know yet.”", [F("a3_kassenbuch")],
         zeile=G("elsa", "[sigh] Good. Then you're thinking. Most people here stopped doing that years ago.", "neutral"))],
      sets={"elsa": "Standard"}),
]

# ------------------------------------------------------------------ 5.8 The Last Crate (Karte Nonna, ab Tag 28 Nachmittag)
NONNA = [
    FR("a3_nonna_kiste", "monastery_garden_dusk", "The Last Crate",
       "Every week there is a crate of seedlings at Nonna's door. This one has stood there since the morning after the siege. "
       "Today she opens the folded letter that came with it. She reads it out loud. It is from Pascal.",
       [G("nonna", "[sigh] He writes: 'I told the priest not to go up the mountain. Stay, Don. Leave it with me. I thought it was for safety.'", "sadness"),
        G("nonna", "[sigh] 'And I confessed all of it to him, every month, for nine years. He can't say a word. That's why he drinks.'", "sadness"),
        JE(G("nonna", "[sniff] 'Duc told me to tell Minicu the truth, at the gate. So I did. It was the only true thing I said that night.'", "grief"),
           "minicu", FL("bl_minicu_sag_es")),
        G("nonna", "[sniff] That's the end of the letter. ...I told Isabelle that man has a good heart. You don't have a good heart, Pascal. You have a bad conscience.", "anger"),
        G("nonna", "[clear throat] There's a key in the crate. The cellar door of the Casanova house. Do you want it, or shall I throw it in the sea?", "neutral")],
       [O("Takes the key.", [F("a3_kellerschluessel"), F("a3_nonna_kiste"), V("nonna", 4)],
          zeile=G("nonna", "[sigh] Go carefully. And plant something when you come back.", "caring")),
        O("“Keep it, Nonna. I'll find another way in.”", [F("a3_nonna_kiste"), V("nonna", 2)],
          zeile=G("nonna", "[chuckle] Then I plant the seedlings anyway. Nothing in my garden goes hungry.", "caring"))],
       personen={"handelnd": "nonna", "betroffen": []}, sets={"nonna": "nonna_standard"}, ton="ernst"),
]

# ------------------------------------------------------------------ 5.9 In My Own Words (Karte Siri)
SIRI = [
    FR("a3_siri_post", "village_harbour", "In My Own Words",
       "The quay at sunset. Siri is wearing her father's jumper with the stars on it. Yasin sits next to her with his phone.",
       [JE(G("siri", "[sigh] My post from the siege was up for four seconds, and then his video slid over it. This time I'm not giving him four seconds.", "anger"),
           "vier", FL("siri_darf_posten")),
        G("yasin", "[laugh] Bro. Somebody offered me twenty thousand for the video. Twenty! That's business.", "pride"),
        G("siri", "[sigh] It's his company, Yasin. He'll buy it, and nobody will ever see it.", "anger"),
        JE(G("siri", "[clear throat] Duc. I said I'd wait for Minicu. Nobody knows if he's awake. Do I post it now, or do I keep waiting?", "nervousness"),
           "frage", FL("siri_wartet")),
        JE(G("siri", "[clear throat] Duc. I want to post it myself. No filter, no music, just what we saw. Is that brave or stupid?", "nervousness"),
           "frage", None)],
       [O("“Post it now. Everybody should see what happened.”", [F("a3_siri_post"), V("siri", 4)],
          zeile=G("yasin", "[sigh] ...I filmed Minicu falling, and I kept filming. I don't want money for that. Okay? That's not business. That's just true.", "remorse")),
        O("“Post it, and I'll stand next to you when he calls it fake.”", [F("a3_siri_post"), V("siri", 6)],
          zeile=G("siri", "[sniff] Okay. Hold my hand when I press it. No, don't. Yes. Hold it.", "nervousness")),
        O("“Wait. It's Minicu's face. Wait until we know.”", [F("a3_siri_festa"), V("siri", 4)],
          zeile=G("siri", "[sigh] Okay. I wait. But not forever.", "sadness"))],
       personen={"handelnd": "siri", "betroffen": [{"id": "yasin", "ton": "?", "was": ""}]}, sets={"siri": "Dad's Sweater"}, ton="ernst"),
]

# ------------------------------------------------------------------ 5.11 Every Report (Tag 29, Abend)
BERICHTE = [
    E("a3_berichte", "gag1", "ernst", "Every Report", PFL(29, "abend", FL("a3_kassenbuch")), "church",
      P1("elsa", ("casanova", "?", "doesn't stop her")),
      "The church steps at night. Candles. Elsa has a pile of papers on her knees, and she reads them out one by one. "
      "Madame Casanova sits two steps higher and listens. Elsa reads thirty-one of them. Casanova doesn't stop her once.",
      [G("elsa", "[clear throat] March. 'Dogs with collars near the monastery road.' May. 'Request for a meeting with the mayor.' "
                 "August. 'Request for a meeting with the mayor.'", "neutral"),
       G("casanova", "[sigh] He told me you never wrote.", "sadness"),
       G("elsa", "[sigh] I wrote every month, Madame.", "sadness"),
       G("casanova", "[sniff] Monsieur. Pascal kept the truth in a drawer for nine years. What did you keep in yours?", "neutral")],
      [O("“Nothing about your harbour. But I should have asked my own company more questions.”", [V("casanova", 6), F("a3_zeuge_tuer_casanova"), DIREKT("a3_berichte_ende")],
         zeile=G("casanova", "[sigh] Questions. Nobody here asked enough of those, Monsieur.", "neutral")),
       O("Sits down on the step below her. “Only that I'm sorry it came out on television.”", [V("casanova", 4), F("a3_zeuge_tuer_casanova"), DIREKT("a3_berichte_ende")]),
       O("“I'm still here. That's my answer.”", [V("casanova", 2), DIREKT("a3_berichte_ende")],
         zeile=G("casanova", "[sigh] Yes. You are. That is something.", "neutral"))]),
    E("a3_berichte_ende", "gag1", "wholesome", "Every Report", FRAME(),
      "church", P1("casanova", ("elsa", "+", "almost smiles")),
      "Madame Casanova stands up and brushes off her skirt.",
      [G("casanova", "[clear throat] Lieutenant. From now on you report to me. Directly. Every day, if you like.", "neutral"),
       G("elsa", "[chuckle] Every day, Madame?", "amusement"),
       G("casanova", "[sigh] ...Every week.", "embarrassment")],
      [O("Blows out the last candle.", [F("a3_berichte_fertig")]),
       O("Walks them both home.", [F("a3_berichte_fertig"), V("elsa", 2), V("casanova", 2)])],
      sets={"elsa": "Standard"}),
]

# ------------------------------------------------------------------ 4.4 Die Yacht (schwer beschaedigt: Reparatur bis Tag 31)
def _rep(tag_von, tag_bis, bed=None):
    b = [AKT3, KAPUTT, NICHT(FL("a3_yacht_repariert"))] + ([bed] if bed else [])
    return WANN((tag_von, tag_bis), ["tag", "nachmittag"], bed={"alle": b})


YACHT = [
    E("a3_yacht_hotline", "gag1", "witzig", "Eden Fleet Services", _rep(25, 31, DA("rosi")), "petru_workshop",
      P1("rosi", ("toto", "+", "is humming along")),
      "Rosi works in Petru's workshop while the yacht is broken. Her phone lies on a crate, on speaker. A friendly voice says: “Thank you for calling Eden Fleet Services. "
      "Your yacht is important to us.” Then the music starts. It is very long music.",
      [G("rosi", "[sigh] Eleven minutes. I'm timing it. ...Twelve.", "annoyance"),
       G("toto", "[laugh] Comandante, I know this song now. All of it. Even the sad part.", "amusement")],
      [O("Sits down next to Rosi and waits with her.", [V("rosi", 2)],
         zeile=G("rosi", "[chuckle] Thirteen minutes. If they answer now, I'll cry. From anger.", "amusement")),
       O("Hangs up for her. “We fix it ourselves.”", [V("rosi", 4), W("moral", 1)],
         zeile=G("rosi", "[laugh] Finally somebody on this boat who talks sense.", "approval"))],
      sets={"rosi": "Engine Room"}),
    E("a3_yacht_propeller", "gag1", "witzig", "One Propeller", _rep(26, 31, DA("rosi")), "petru_workshop",
      P1("toto", ("rosi", "-", "reads the delivery note")),
      "A crate from Monaco stands in Petru's workshop. Totò opens it like a birthday present.",
      [G("toto", "[gasp] Comandante! The Eden Group sent us one propeller. One. We have two.", "surprise"),
       G("rosi", "[sigh] Then we're half finished.", "neutral")],
      [O("“Half is better than nothing.”", [W("moral", 1)],
         zeile=G("toto", "[laugh] You see? That's why he is the Comandante.", "amusement")),
       O("Helps Totò carry the crate anyway.", [V("toto", 2)],
         zeile=G("toto", "[chuckle] Heavy. For one propeller. Monaco puts stones in it, I think.", "amusement"))],
      sets={"rosi": "Engine Room"}),
    E("a3_yacht_tuer", "gag1", "witzig", "A Door", _rep(26, 29, DA("rosi")), "village_harbour",
      P1("maxwell", ("rosi", "-", "points at the sea")),
      "Maxwell comes along the quay with a door on his shoulder. Nobody knows where he found it.",
      [G("maxwell", "[clear throat] Mr. Maximum has found a door. He does not know where it goes.", "pride"),
       G("rosi", "[sigh] The sea. It goes in the sea.", "annoyance")],
      [O("“Put it on the pile, Maxwell. It'll be a table at the festa.”", [V("maxwell", 2)],
         zeile=G("maxwell", "[laugh] Eish! A door that becomes a table. Lekker.", "joy")),
       O("Takes the other end of the door.", [V("maxwell", 2), W("moral", 1)],
         zeile=G("maxwell", "[chuckle] Teamwork, brother. Into the sea. Slowly.", "amusement"))],
      sets={"maxwell": "maximum_steelmop", "rosi": "Engine Room"}),
    E("a3_yacht_haesslich", "gag1", "wholesome", "Ugly", WANN((31, 31), ["abend"], bed={"alle": [AKT3, KAPUTT, NICHT(FL("a3_yacht_repariert"))]}, pflicht=True, holt_leute=True),
      "village_harbour", P1("rosi", ("toto", "+", "claps")),
      "The evening of day 31. Someone knocks on the hull twice, from the engine room.",
      [JE(G("rosi", "[laugh] Officer! Up here. She's ugly, she leaks a bit, and she floats. Don't tell her I said ugly.", "pride"), "rosi", DA("rosi")),
       JE(G("maxwell", "[laugh] Rosi says on the video: she floats. Mr. Maximum has checked. She floats.", "pride"), "rosi", None)],
      [O("Knocks on the hull too.", [F("a3_yacht_repariert"), W("moral", 1)]),
       O("“Tomorrow we take her out.”", [F("a3_yacht_repariert")])],
      sets={"rosi": "Engine Room"}),
    E("a3_probefahrt", "gag1", "wholesome", "She Still Swims", WANN((32, 32), ["fruehstueck"], bed={"alle": [AKT3, KAPUTT, FL("a3_yacht_repariert"), DA("rosi")]}, pflicht=True, holt_leute=True),
      "bridge", P1("holm", ("rosi", "+", "is listening to the engine")),
      "Holm stands on the bridge for the first time since the siege. One slow round in the harbour.",
      [G("holm", "[clear throat] Frankfurt. Ready to see if she still swims?", "neutral")],
      [O("Stands next to Holm on the bridge.", [V("holm", 4), F("a3_probefahrt")],
         zeile=G("holm", "[sigh] Takk, Rosi. ...She swims.", "gratitude")),
       O("Goes down to Rosi in the engine room.", [V("rosi", 4), F("a3_probefahrt")],
         zeile=G("rosi", "[sniff] Don't say anything nice. I'll cry, and then the engine cries.", "embarrassment")),
       O("“After you, Captain.”", [V("holm", 2), F("a3_probefahrt")],
         zeile=G("holm", "[chuckle] After me. Of course after me. It's my bridge.", "amusement"))],
      sets={"holm": "Bridge", "rosi": "Engine Room"}),
    # Duc 05.11.2026 (F-42): die Probefahrt auch ohne Rosi. Maxwell ist an Tag 32 fort, also hoert Petru auf den Motor.
    E("a3_probefahrt_petru", "gag1", "wholesome", "She Still Swims", WANN((32, 32), ["fruehstueck"], bed={"alle": [AKT3, KAPUTT, FL("a3_yacht_repariert"), NICHT(DA("rosi"))]}, pflicht=True, holt_leute=True),
      "bridge", P1("holm", ("petru", "+", "is listening to the engine")),
      "Holm stands on the bridge for the first time since the siege. Rosi is not on board any more. "
      "So this morning Petru went down to the engine room without asking anyone. One slow round in the harbour.",
      [G("holm", "[clear throat] Frankfurt. Ready to see if she still swims? Petru says the engine sounds fine. From Petru, that is a speech.", "neutral")],
      [O("Stands next to Holm on the bridge.", [V("holm", 4), F("a3_probefahrt")],
         zeile=G("holm", "[sigh] Takk, Petru. ...She swims.", "gratitude")),
       O("Goes down to Petru in the engine room.", [V("petru", 4), F("a3_probefahrt")],
         zeile=G("petru", "[clear throat] I only listen to it. Somebody built this engine well. Go up. She wants you on the bridge.", "neutral")),
       O("“After you, Captain.”", [V("holm", 2), F("a3_probefahrt")],
         zeile=G("holm", "[chuckle] After me. Of course after me. It's my bridge.", "amusement"))],
      sets={"holm": "Bridge", "petru": "Standard"}),
    E("a3_yacht_klein", "gag1", "witzig", "Mostly Cosmetic", WANN((25, 29), ["tag", "nachmittag"], bed={"alle": [AKT3, NICHT(KAPUTT), DA("rosi")]}),
      "aft_deck", P1("rosi", ("maxwell", "+", "holds the paint")),
      "The yacht came through the siege. Mostly. Rosi is painting over a burn mark on the aft deck, very slowly.",
      [G("rosi", "[sigh] If anyone asks, this was always here. It's a design.", "annoyance"),
       G("maxwell", "[laugh] Mr. Maximum likes the design. Very modern.", "amusement")],
      [O("“It's a beautiful design, Rosi.”", [V("rosi", 2)],
         zeile=G("rosi", "[chuckle] Liar. Give me the brush.", "amusement")),
       O("Picks up a second brush.", [V("rosi", 2), W("moral", 1)])],
      sets={"rosi": "Engine Room", "maxwell": "maximum_steelmop"}),
]

# ------------------------------------------------------------------ 5.28 Borrowed (Charlys Geld, Karte im Pool)
CHARLY = [
    E("a3_charly_geld", "gag1", "frech", "Borrowed",
      WANN((26, 33), ["tag", "nachmittag"], bed={"alle": [AKT3, FL("rt_charly_bleibt"), NICHT(FL("rt_charly_weg")),
                                                         {"eine": [FL("aufbau_begonnen_" + h) for h in FOLGE]}]}),
      "village_piazza", P1("charly", ("casanova", "?", "is holding the festa board")),
      "Charly sits down next to the mayor on the church steps with her laptop. She doesn't say hello. She never does.",
      [JE(G("charly", "[sigh] I switched off one of my mother's machines on the ridge. Now her money. My mother's company sells to Alon. "
                    "I moved some of it tonight. Quietly. For the houses.", "neutral"), "kamm", FL("a3_mast_fertig")),
       JE(G("charly", "[clear throat] My mother's company sells to Alon. I moved some of her money tonight. Quietly. For the houses.", "neutral"), "kamm", None),
       G("casanova", "[gasp] You... moved it? Is this stolen, Mademoiselle?", "surprise"),
       G("charly", "[sigh] Three out of ten for stolen. Eight for borrowed. She won't notice for a month.", "neutral"),
       G("casanova", "[clear throat] Monsieur. Do I take money that a girl took from her own mother?", "confusion")],
      [O("“Take it. Her mother pays for what Alon burned.”", [F("a3_charly_geld"), V("charly", 4)],
         zeile=G("casanova", "[chuckle] ...Then the houses are built with Ravenel money. How funny.", "amusement")),
       O("“Take it, and put Charly's name on the board.”", [F("a3_charly_geld"), F("a3_charly_tafel"), V("charly", 2), V("casanova", 2)],
         zeile=G("charly", "[sigh] Don't. Five out of ten for that idea.", "embarrassment")),
       O("“Ask Charly, not me.”", [F("a3_charly_geld"), V("charly", 6)],
         zeile=G("charly", "[sigh] Take it. It's the first good thing her money ever did.", "neutral"))]),
]

# ------------------------------------------------------------------ 5.8 Ersatz: Mina bringt Schluessel und Brief (Tag 31)
NONNA_MINA = [
    E("a3_nonna_mina", "gag1", "ernst", "A Key from Nonna", PFL(31, "fruehstueck", {"alle": [{"gesehen": "a3_sonntag"}, NICHT(FL("a3_nonna_kiste"))]}),
      "village_piazza", P1("mina"),
      "Mina comes across the square with a small parcel. Inside: an old iron key with a ribbon from a crate of seedlings, and a letter in Nonna's hand.",
      [G("mina", "[clear throat] From Nonna. She says you didn't come, so the mountain comes to you. That's what she said. I don't know what it means.", "neutral"),
       G("mina", "[sigh] The letter says: It's the cellar door of the Casanova house. Pascal left it for me. I don't want it. Do you?", "neutral")],
      [O("Takes the key.", [F("a3_kellerschluessel"), F("a3_nonna_kiste")],
         zeile=G("mina", "[chuckle] Signed and delivered. That's my job.", "pride")),
       O("“Give it back to her. I'll find another way in.”", [F("a3_nonna_kiste")],
         zeile=G("mina", "[sigh] Okay. Up the mountain again. My legs hate you.", "annoyance"))]),
]

# ------------------------------------------------------------------ 5.10 The Rematch (Holm, Tag 24-29)
REVANCHE = [
    E("a3_revanche", "gag1", "witzig", "The Rematch", WANN((24, 29), ["nachmittag"], bed={"alle": [AKT3, FL("holm_zurueck")]}),
      "village_harbour", P1("holm", ("petru", "?", "is setting up bottles")),
      "Holm is sitting on the mole with a stick next to her and a row of empty bottles on the wall. Petru is putting up the last one.",
      [G("holm", "[clear throat] Frankfurt. You still have my rifle. I want it back, so we shoot for it. At the stand, whenever you're ready.", "neutral"),
       G("holm", "[chuckle] It pulls left. Like the day you won it from me.", "amusement"),
       JE(G("holm", "[sigh] And one more thing. That night in the siege, you said nobody goes to the north road, Pascal has it. "
                    "I should have gone myself. That's mine, not yours.", "remorse"), "nacht", FL("bl_nachtwache_pascal")),
       G("petru", "[clear throat] The sea doesn't hurry. Neither do bottles. Again.", "neutral")],
      [O("“Tomorrow. And I'm keeping it.”", [V("holm", 2), F("a3_revanche")],
         zeile=G("holm", "[laugh] Faen. We'll see, Frankfurt.", "amusement")),
       O("Sits down next to her on the mole first.", [V("holm", 4), F("a3_revanche")],
         zeile=G("holm", "[sigh] My hands are fine now. My head isn't, yet. Takk.", "gratitude"))]),
]

EVENTS = NONNA_MINA + REVANCHE + MORGEN + SCHWUR + BAU + DANK + ALVA + UHR + MEGAN + TAFEL + SONNTAG + NONNA + SIRI + BERICHTE + YACHT + CHARLY

# Orte (Karten) fuer auftraege_eden_rise.py: kosten die ganze Phase
ORTE = {
    "a3_baustellen": {
        "label": "Lend a Hand", "bild": "village_piazza", "phasen": ["tag", "nachmittag"],
        "text": "The burned houses are building sites now. Lay the first stone where you want the pirates to start. Takes the whole phase.",
        "wenn": {"alle": [FL("buenaventura_schwur"), {"eine": [_offen(h) for h in FOLGE]}]},
        "start": [{"wenn": _offen(h), "id": "a3_bau_" + h} for h in FOLGE]},
    "a3_alva": {
        "label": "Alva Is Awake", "bild": "church", "phasen": ["nachmittag", "dinner", "abend"],
        "text": "Mina says Sandru wants you to come. Sandru never asks. Takes the whole phase.",
        "wenn": {"alle": [FL("a3_morgen_fertig"), NICHT(FL("a3_alva_wach"))]},
        "start": [{"id": "a3_alva_wach"}]},
    "a3_siri": {
        "label": "The Quay at Sunset", "bild": "village_harbour", "phasen": ["abend"],
        "text": "Siri is sitting on the quay with Yasin and a phone. Takes the whole phase.",
        "wenn": {"alle": [FL("a3_morgen_fertig"), NICHT(FL("a3_siri_post")), NICHT(FL("a3_siri_festa")), DA("siri")]},
        "start": [{"id": "a3_siri_post"}]},
    "a3_nonna": {
        "label": "Nonna's Crate", "bild": "monastery_garden_dusk", "phasen": ["nachmittag", "dinner"],
        "text": "There is a crate of seedlings at Nonna's door, with a letter. Takes the whole phase.",
        "wenn": {"alle": [{"gesehen": "a3_sonntag"}, NICHT(FL("a3_nonna_kiste"))]},
        "start": [{"id": "a3_nonna_kiste"}]},
}


def tags_fuer(events, quelle):
    """Gesprochene Fassungen dieser Events in stimme_tags.json (G() sammelt sie in ereignisse_ligeia.STIMME). -> Anzahl."""
    eigene = {(zl["wer"], zl["text"]) for e in events for zl in e["zeilen"] + [o["zeile"] for o in e["optionen"] if o.get("zeile")]}
    neu, gesehen = [], set()
    for w, t, g in _LIGEIA:
        if (w, t) in eigene and (w, t) not in gesehen:
            gesehen.add((w, t))
            neu.append({"wer": w, "text": t, "gesprochen": g, "quelle": quelle})
    pfad = os.path.join(EDEN, "module", "eden_rise", "stimme_tags.json")
    d = json.load(open(pfad, encoding="utf-8"))
    texte = {z["text"] for z in neu}
    paare = {(z["wer"], z["text"]) for z in neu}               # nur gleicher Sprecher und gleicher Text wird ersetzt (Review Nr. 11)
    d["zeilen"] = [z for z in d["zeilen"] if z.get("quelle") != quelle and (z["wer"], z["text"]) not in paare] + neu
    json.dump(d, open(pfad, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return len(neu)


def tags_schreiben():
    return tags_fuer(EVENTS, "akt3_woche4")
