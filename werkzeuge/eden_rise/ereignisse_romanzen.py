# -*- coding: utf-8 -*-
r"""Romanzen-Leiter, Probe alle sieben Romanzen, dazu das Echo fuer Jana und Megan (Duc 31.10.2026, Beta-Kritik, docs/brain_trust/ROMANZEN_PROBE_*.md).
Der Spieler hat die Szene davor vergessen: Jeder Rueckbezug traegt eine Erinnerung in Lage oder Satz (Duc 31.10.2026).

Beziehungen laufen nicht mehr ueber Zufall: Jede Szene ist Pflicht, sobald ihre Stufe und ihr fruehester Tag erreicht sind,
hoechstens eine Leiter-Szene am Tag (wann.leiter, kern/ereignisse.pflicht_ziehen).
  Rosi  rm_r1 Nothing's Broken · rm_r2 Nobody Lost · rm_r3 What She Tells Unit-01 · rm_r4 Read It
  Lea   rm_l1 Stay Together · rm_l2 What Are We? · rm_l3 Sweet · rm_l4 No Glow Tonight
Echo (rm_e_*): am naechsten Morgen sagt sie etwas zu dem, was passiert ist, kurz und unter vier Augen (E-060).
Wirkung und Grenzen: docs/wiki/systeme/beziehungen.md, Abschnitt "Romanzen-Leiter".
"""
from ereignisse_basis import *  # noqa: F401,F403
from ereignisse_ligeia import G

FD = lambda name: {"flag_datiert": name}
DIREKT = lambda ziel: {"direkt": ziel}
FAKT = lambda pid, text: {"fakt": {"wer": pid, "text": text}}
AUF = lambda pid, *momente: {"aufgegriffen": [pid, list(momente)]}
N = lambda flag: {"nicht": {"flag": flag}}
GROSS = ("kiss", "confession", "naehe", "naehe_weit", "intimate")


def AB(pid, v=None, b=None):
    """Stufen-Bedingung; wer gefeuert wurde, ist nicht mehr an Bord."""
    out = [N("gefeuert_" + pid)]
    if v:
        out.append({"wert": ["vertrauen." + pid, ">=", v]})
    if b:
        out.append({"wert": ["begehren." + pid, ">=", b]})
    return out


def W_L(tage, phase, *bed, spaet=False):
    """Pflicht ueber mehrere Tage: Akt 1 und Akt 2/3 als getrennte Fenster (pruefe: nie ueber eine Aktgrenze)."""
    w = WANN(tage, [phase], bed={"alle": list(bed)}, pflicht=True, holt_leute=True)
    w["leiter"] = True
    if tage[1] <= 6 or spaet:
        w["akt2"] = list(AKT3) if spaet else [8, 35]
    return w


def FRAME():
    """Zweiter Takt einer Szene: wird nie gezogen, nur ueber die Folge "direkt" geoeffnet."""
    return WANN((8, 21))


def ABEND(id, ton, titel, wann, bild, pid, lage, zeilen, optionen, set_):
    return E(id, "abend", ton, titel, wann, bild, {"pid": pid}, lage, zeilen, optionen, sets={pid: set_}, knistern=True)


# ------------------------------------------------------------------ Rosi
ROSI = [
    ABEND("rm_r1", "wholesome", "Nothing's Broken", W_L((4, 6), "nacht", *AB("rosi", 3, 3), N("rm_r1")), "workshop", "rosi",
          "Your phone says: “workshop. urgent.” There is one relay on the bench. You test it, and it works. Behind Rosi, at the "
          "very bottom of the whiteboard, there's a small line of writing. She puts her hand over it without looking.",
          [G("rosi", "[clear throat] It's faulty, very faulty, and it's a two-person job, so sit down and hold the lamp.", "pride"),
           G("rosi", "What? [chuckle] Don't look at the meter, because the meter's wrong, and it has never liked me.", "embarrassment")],
          [O("Sits down and holds the lamp. “Terrible relay. This could take all night.”",
             [B("rosi", 6), V("rosi", 2), FD("rm_r1")],
             zeile=G("rosi", "All night, at least, because I've seen relays like this end careers. [chuckle] …Move the lamp left, thanks.", "desire")),
           O("“What's written at the bottom of the board?”", [V("rosi", 3), FD("rm_r1")],
             zeile=G("rosi", "Nothing, it's only inventory, a list of screws. [clear throat] Do you want to count my screws, Officer? No? Then fix the relay.", "embarrassment")),
           O("“This one works fine, Rosi. Get some sleep.”", [V("rosi", 3), FD("rm_r1")],
             zeile=G("rosi", "…Yes, right. [sigh] Good catch, so you get a tick for that, on your side. Goodnight, Officer.", "sadness"))],
          "Engine Room"),
    ABEND("rm_r2", "frech", "Nobody Lost", W_L((6, 6), "nacht", *AB("rosi", 3, 4), {"flag_seit": ["rm_r1", 2]}, N("rm_r2")),
          "generator_room", "rosi",
          "Two worn bearings, two spanners and one stopwatch. The stake is one minute: the loser does whatever the winner says. "
          "You put your spanner down. She puts hers down. The stopwatch shows one time for both of you.",
          [G("rosi", "[gasp] The same time. That can't be right, we'll do it again. …No. No, leave it.", "surprise"),
           G("rosi", "So nobody won. [clear throat] That's a draw, and in a draw nobody owes anybody anything, and nobody has to do what anybody says.", "nervousness"),
           G("rosi", "So if someone closed that door now, it wouldn't be because they lost. [sigh] Do you understand the difference? It's important to me that you understand the difference.", "desire")],
          [O("Closes the door. “Nobody lost.”",
             [V("rosi", 4), FD("rm_r2"),
              INTIM("rosi", "generator_room", "Engine Room", "rosi",
                    "The door is shut, and Unit-01 hums behind it. Nobody lost. Rosi is still keeping score out loud, and she is not as sure "
                    "of herself as she is with machines.")],
             zeile=G("rosi", "Nobody lost, good. [chuckle] I'm writing that down later.", "desire")),
           O("Stays by the ladder. “Is this what you want, or is this the bet talking?”",
             [V("rosi", 8), FD("rm_r2"),
              INTIM("rosi", "generator_room", "Engine Room", "rosi",
                    "Nobody has ever asked Rosi if she really wants this. She sits down on the toolbox and talks fast, and she is in no hurry "
                    "for anything else.")],
             zeile=G("rosi", "…Nobody has ever asked me that. [sigh] It's what I want. It's also the bet. Can it be both?", "love")),
           O("“Not tonight, Rosi. Ask me when you haven't got a stopwatch in your hand.”", [V("rosi", 4), FD("rm_r2"), F("rm_r_nein")],
             zeile=G("rosi", "Ha, fine, I'll put it down, then. [chuckle] But I'm putting it down where I can find it.", "amusement"))],
          "Engine Room"),
    ABEND("rm_r3", "wholesome", "What She Tells Unit-01", W_L((9, 21), "nacht", *AB("rosi", 4, 4), {"flag_seit": ["rm_r2", 2]}, N("rm_r3"), spaet=True),
          "generator_room", "rosi",
          "You come down the ladder and stop. Rosi is sitting with her back to you and a rag in her hands. She's talking to the "
          "generator, in a quiet voice you have never heard from her. She doesn't know you're there.",
          [G("rosi", "You're running hot again, you know that? [sigh] You're running hot and you won't tell anyone why. I know what that's like.", "sadness"),
           G("rosi", "He fixed the bilge pump and told nobody. Who does that? [sniff] I had a plan. Four more seasons, then Papa's workshop, and then I never have to ask anyone for anything again. There's no officer in that plan.", "nervousness"),
           G("rosi", "And on the last day he goes back to Frankfurt, and I say see you, Officer, good rivalry. [sniff] And I'll be fine. I will be fine, so stop looking at me like that.", "sadness")],
          [O("Goes back up the ladder without a sound.", [V("rosi", 4), FD("rm_r3"), F("rm_r3_still")]),
           O("Goes back up, then comes down again, loudly. “You're up late.”", [V("rosi", 4), B("rosi", 4), FD("rm_r3")],
             zeile=G("rosi", "So are you. [gasp] Did you – how long have you – no, don't answer that. Just hold this.", "embarrassment")),
           O("Sits down next to her. “She's not the only one running hot.”",
             [B("rosi", 6), V("rosi", 4), FD("rm_r3"), F("rm_r3_offen"),
              FAKT("rosi", "Duc heard Rosi telling Unit-01 about him, about her plan and about the last day, and he told her he heard it.")],
             zeile=G("rosi", "How long were you standing there? No, don't tell me, I'd have to kill you and I need you for the relay. [sigh] Sit down and don't talk, she likes it quiet.", "love"))],
          "Off Duty"),
    ABEND("rm_r4", "wholesome", "Read It",
          W_L((15, 21), "nacht", *AB("rosi", 4, 5), {"flag_seit": ["rm_r3", 2]}, N("rm_r4"),
              {"eine": [{"heute_gekaempft": True}, {"tag_ab": 19}]}, spaet=True),
          "workshop", "rosi",
          "You come back after midnight. There's a burnt hole in your jacket, right over the shoulder. Rosi takes the jacket from "
          "you. She doesn't look at you.",
          [G("rosi", "Put the chips on the bench – no, not there. [sigh] Look at this, there's a hole in it, and your shoulder was right behind it. I built this jacket, and I sat here all night with a radio that doesn't work.", "anger"),
           G("rosi", "Do you know what my father did when the bank came? [sniff] He stood outside the workshop with his hands in his pockets, because there was nothing else he could do. And tonight I looked down, and I had my hands in my pockets.", "anger"),
           G("rosi", "[gasp] NOBODY DOES THAT TO ME! NOT THE BANK, NOT THE SEA, AND NOT YOU, OFFICER! THIS IS NOT YOUR DESTINY, DO YOU HEAR ME?", "anger")],
          [O("Says nothing and waits.", [FD("rm_r4"), DIREKT("rm_r4_b")])],
          "Engine Room"),
    ABEND("rm_r4_b", "wholesome", "Read It", FRAME(), "workshop", "rosi",
          "It's very quiet. Ten seconds. She wipes her hands on her trousers. Then she walks to the whiteboard, to the small line "
          "at the bottom that she has covered with her hand all these weeks, and she takes her hand away. It reads: Times he "
          "stayed when nothing was broken. Next to it, small careful ticks. There are {striche} of them.",
          [G("rosi", "Go on, read it, and count them if you like, because I already did. [sniff] I made up half of those repairs, you know. That first relay, the night you held the lamp, was perfectly fine.", "neutral"),
           dict(G("rosi", "And I know you stood on that ladder and heard me talking to Unit-01, so don't look so surprised. [chuckle] She talks.", "amusement"),
                gruppe="gehoert", wenn={"flag": "rm_r3_still"}),
           G("rosi", "I don't lose, you know that. [sigh] I've never said it to anyone, not to Papa and not to a machine, so listen carefully, because I'm only going to say it once. I lost. It happened a long time ago, probably when you fixed that bilge pump and told nobody, and you can write that down.", "love")],
          [O("Takes the marker and writes under the ticks: DRAW.",
             [V("rosi", 8), B("rosi", 8), F("rosi_zusammen"),
              FAKT("rosi", "Rosi showed Duc the hidden line on her whiteboard and told him she lost. He wrote DRAW under it. They are together now, in private, and she calls him Captain when they are alone.")],
             zeile=G("rosi", "You idiot, you can't just – that's not how it works. [laugh] So nobody won, is that what you're telling me? …Okay. Then nobody won, Captain.", "love")),
           O("Puts the burnt jacket on the bench and adds one more tick himself. “Fix it. I'll stay.”",
             [V("rosi", 8), B("rosi", 8), F("rosi_zusammen"),
              FAKT("rosi", "Rosi showed Duc the hidden line on her whiteboard and told him she lost. He added a tick and stayed all night. They are together now, in private, and she calls him Captain when they are alone.")],
             zeile=G("rosi", "That's not a repair, and you know it's not a – yes, all right. [sniff] Sit down, Captain, because this is going to take all night.", "love")),
           O("“I don't know what happens on the last day, Rosi. I won't promise you something I don't know.”",
             [V("rosi", 12), F("rosi_offen"),
              FAKT("rosi", "Rosi showed Duc the hidden line on her whiteboard and told him she lost. He told her he could promise nothing about the last day, and she respected that.")],
             zeile=G("rosi", "Good, because I hate speeches. [sigh] I didn't ask you for anything, I only asked you to read it. …Now give me the jacket.", "sadness"))],
          "Engine Room"),
]

# ------------------------------------------------------------------ Lea
LEA = [
    ABEND("rm_l1", "wholesome", "Stay Together", W_L((3, 6), "nacht", *AB("lea", 3, 3), N("rm_l1")), "swim_platform", "lea",
          "Past midnight. Three short knocks, one long. Lea is in your doorway in a wetsuit, whispering much too loudly, and a "
          "minute later you are standing with her on the swim platform. The water is black and still.",
          [dict(G("lea", "You said to wake you next time I went diving. [chuckle] You did say that, I've got witnesses. Well, I haven't got witnesses, that's the whole point, it's a secret. The squid are up.", "excitement"),
                gruppe="wecken", wenn={"flag": "lea_weck_mich"}),
           dict(G("lea", "I know you never said to wake you. [chuckle] I'm waking you anyway, because the squid are up and I can't be the only one who knows. It's a secret.", "excitement"),
                gruppe="wecken"),
           G("lea", "You can't talk down there, which I know is hard to believe coming from me. [laugh] So there are signs. This one's okay, this one's going up, and this one's something's wrong.", "joy"),
           G("lea", "And this one, two fingers side by side. [clear throat] It means stay together. You use it when it's dark and you want to know the other person's still there. You don't have to do it back. Well, you do, that's the rule, that's how it works.", "nervousness")],
          [O("Goes into the water with her.", [FD("rm_l1"), DIREKT("rm_l1_b")]),
           O("Stays on the platform. “I'll hold the torch. Someone should.”", [V("lea", 3), FD("rm_l1")],
             zeile=G("lea", "Okay. That's – yeah, that's proper safe, actually. [chuckle] Keep the light on me?", "caring"))],
          "Dive"),
    ABEND("rm_l1_b", "wholesome", "Stay Together", FRAME(), "swim_platform", "lea",
          "Six metres. Small squid light up around her hands. For the first time since you met her, Lea isn't saying anything. She "
          "turns to you and holds up two fingers. You can almost hear what she's thinking.",
          [G("lea", "Okay. Okay okay okay. [sigh] You can't talk down here, Lea. Just look at him.", "love")],
          [O("Holds up two fingers.", [B("lea", 6), V("lea", 3), F("lea_zeichen")],
             zeile=G("lea", "You did it back. [sniff] …That's just the rule, I know. I know it's the rule.", "love")),
           O("Makes the okay sign and points at the biggest squid.", [V("lea", 6), F("lea_zeichen")],
             zeile=G("lea", "You saw the big one? [laugh] That's the biggest I've ever seen, and I've been down here eleven times, did you see its arms?", "excitement"))],
          "Dive"),
]


def L2_ANTWORT(erste):
    """Die Frage selbst, einmal mit Taucherzeichen als Antwort und einmal ohne (wer in L1 auf dem Steg blieb)."""
    return [O(erste, [V("lea", 8), B("lea", 8), F("lea_zusammen"),
                      FAKT("lea", "Lea asked Duc what they are, and he told her they stay together. They are together now, in private. She has written something at the top of his page in her logbook and won't show him.")],
              zeile=G("lea", "You can't answer a question with a dive signal. [laugh] That's not – okay. Yes. You can.", "love")
              if "fingers" in erste else G("lea", "With you. [sniff] Okay. That's going at the top, then. You're not allowed to read it.", "love")),
            O("“I like you a lot, and I don't know yet. Can that go at the top?”", [V("lea", 10), F("lea_offen"),
              FAKT("lea", "Lea asked Duc what they are. He said he likes her a lot and doesn't know yet, and she accepted that and will ask again.")],
              zeile=G("lea", "‘Don't know yet.’ That's proper science, that is. [chuckle] Yes, that's allowed. I'll be checking again, though. I check things.", "joy")),
            O("“We're having fun, Lea. I don't want to make it bigger than it is.”", [V("lea", 4), B("lea", -6), F("lea_locker"),
              FAKT("lea", "Lea asked Duc what they are. He told her they are only having fun, and she thanked him for saying it straight, though it hurt.")],
              zeile=G("lea", "Okay. No, that's fine, thanks for saying it straight. I mean that. Nobody does. [sniff] …I'll just write ‘fun’. Sorry, I'm going to go and look at a crab.", "sadness"))]


LAGE_L2 = ("She closes the logbook. When she speaks again, it's slowly.")
FRAGE_L2 = "So. What are we? [sigh] I've got a page for you and I don't know what to write at the top. I'd rather know, even if it's a bad answer. People never tell me things straight, because they think it's sweet."

LEA += [
    ABEND("rm_l2", "wholesome", "What Are We?", W_L((9, 21), "abend", *AB("lea", 4, 4), {"flag_seit": ["rm_l1", 2]}, N("rm_l2"), N("sophia_zusammen"), spaet=True),
          "tender_garage", "lea",
          "Lea is sitting in the tender garage with her logbook open. The page has columns. When you come in she stands up, salutes "
          "and sits down again.",
          [G("lea", "Okay. I need to ask you something and I've prepared. [clear throat] Sit down, it's got sections.", "nervousness"),
           G("lea", "So swans stay together for life, which is lovely, except they don't, they cheat all the time. Penguins, same. [chuckle] And with the anglerfish, the male bites on to the female and sort of dissolves into her, and I don't think that's what we're doing.", "nervousness"),
           G("lea", "What I mean is, I've looked everywhere, and there's no species for this. [sigh] Sophia asked me why I keep smiling at breakfast and I said plankton. I told my own sister I was smiling at plankton.", "embarrassment")],
          [O("Waits.", [FD("rm_l2"), DIREKT([{"wenn": {"flag": "lea_zeichen"}, "id": "rm_l2_b"}, {"id": "rm_l2_c"}])])],
          "Off Duty"),
    ABEND("rm_l2_b", "wholesome", "What Are We?", FRAME(), "tender_garage", "lea", LAGE_L2, [G("lea", FRAGE_L2, "love")],
          L2_ANTWORT("Holds up two fingers, side by side, the divers' sign she taught you for stay together."), "Off Duty"),
    ABEND("rm_l2_c", "wholesome", "What Are We?", FRAME(), "tender_garage", "lea", LAGE_L2, [G("lea", FRAGE_L2, "love")],
          L2_ANTWORT("“You're with me, if you want that.”"), "Off Duty"),
    E("rm_l3", "abend", "wholesome", "Sweet",
      W_L((10, 21), "abend", {"eine": [{"flag": "lea_zusammen"}, {"flag": "lea_offen"}]}, {"flag_seit": ["rm_l2", 1]}, N("rm_l3"), N("gefeuert_sophia"), spaet=True),
      "aft_deck", {"pid": "sophia"},
      "Sophia is writing in her brown notebook. She doesn't look up, and she moves her bag from the chair next to her.",
      [G("sophia", "Sit with me a moment, darling. [sigh] My sister has stopped borrowing my things, she hums in the shower, and yesterday she told me the plankton was very well, thank you.", "neutral"),
       G("sophia", "I'm not cross. I raised her, so I know what she looks like when she has found something. [clear throat] I only want to know one thing, and I shall know if you lie.", "caring"),
       dict(G("sophia", "And we both remember our little bet on the aft deck, the ten euros, so let me save you some trouble. [chuckle] One of us. Never both.", "amusement"),
            gruppe="wette", wenn={"flag": "sophia_funke"}),
       G("sophia", "Do you take her seriously? [sniff] Everyone thinks she's sweet. I've thought so for fourteen years, and she hates it.", "sadness")],
      [O("“More than she knows.”", [V("sophia", 4), FD("rm_l3")],
         zeile=G("sophia", "Then tell her, darling. [chuckle] Not me.", "caring")),
       O("“Ask her, not me.”", [V("sophia", 4), FD("rm_l3")],
         zeile=G("sophia", "I did. [chuckle] She said plankton.", "amusement")),
       O("“That's between Lea and me.”", [V("sophia", 4), V("lea", 3), FD("rm_l3")],
         zeile=G("sophia", "A good answer. [sigh] Unpleasant, but good.", "approval"))],
      sets={"sophia": "Concierge"}, knistern=True),
    ABEND("rm_l4", "wholesome", "No Glow Tonight",
          W_L((15, 21), "nacht", *AB("lea", 5, 5), {"flag_seit": ["rm_l2", 2]}, N("lea_locker"), N("rm_l4"), spaet=True),
          "swim_platform", "lea",
          "The water is black. Lea is sitting on the edge with her phone in her lap and her feet in the sea. Nothing glows. She "
          "doesn't salute.",
          [G("lea", "There's no plankton tonight. It doesn't do it every night. [sigh] I did tell you that.", "neutral"),
           G("lea", "I applied for something in the spring, before all this. Whale research in the Azores, for eighteen months. [clear throat] Sophia doesn't know, nobody knows. They said yes. It came on Tuesday.", "sadness"),
           G("lea", "I should be jumping up and down, shouldn't I? I jump up and down about crabs. [sniff] But I read it and I felt nothing, for a whole minute. That's never happened to me. It frightened me more than that drone over the bay did.", "fear"),
           G("lea", "Grandad looked for that old wreck, the Margot, his whole life. What if that's what kept him going? [sniff] What if I find her, and the whales say yes, and then one morning I look at the sea and it's only water?", "sadness"),
           G("lea", "I'm not asking you what to do. Everyone tells me what to do. [sigh] I just didn't want to look at it on my own.", "love")],
          [O("Puts his hand in the black water and leaves it there. “Then we wait. It doesn't do it every night.”",
             [V("lea", 8), B("lea", 8), F("rm_l4"), F("lea_azoren_offen"),
              FAKT("lea", "Lea told Duc about the Azores offer and about her fear that one day the sea will be only water. Sophia doesn't know yet. He waited with her until the water glowed, and neither of them decided anything.")],
             zeile=G("lea", "Did you know – no. Never mind. [sniff] I don't need one.", "love")),
           O("“Go. You'd never forgive yourself. I'll come and see the whales.”",
             [V("lea", 8), F("rm_l4"), F("lea_azoren_geh"),
              FAKT("lea", "Lea told Duc about the Azores offer and her fear that one day the sea will be only water. Sophia doesn't know yet. He told her to go and promised to visit.")],
             zeile=G("lea", "You'd be seasick the whole time and you'd hate it. [chuckle] …You'd really come?", "love")),
           O("“Stay. I want you here.”",
             [V("lea", 8), FD("rm_l4_bleib"), F("rm_l4"), F("lea_azoren_bleib"),
              FAKT("lea", "Lea told Duc about the Azores offer and her fear that one day the sea will be only water. Sophia doesn't know yet. He asked her to stay, and she asked him to say it again in daylight.")],
             zeile=G("lea", "Nobody has ever said that to me without laughing. [sniff] Just don't say it because it's a nice night. Say it again tomorrow, in daylight, and then I'll believe you.", "love"))],
          "Off Duty"),
]

# ------------------------------------------------------------------ Echo: am naechsten Morgen
LAGE_ECHO = {
    "rosi": ("crew_mess", "Off Duty", "Early morning in the crew mess, and nobody else is up yet. Rosi is at the coffee machine with her back "
             "to you. She knows it's you."),
    "lea": ("foredeck", "Deck", "Early morning on the foredeck, and nobody else is up yet. Lea has a mug in one hand and a pencil in the "
            "other, and she looks up when she hears you."),
}


def ECHO(id, pid, titel, bed, zeile, gefuehl, chips, los=None):
    """chips: [(Text, Antwort, Gefuehl)]. los: Folgen, die den Anlass als erledigt markieren."""
    bild, set_, lage = LAGE_ECHO[pid]
    w = WANN((2, 6), ["fruehstueck"], bed={"alle": [{"nicht": {"flag": "gefeuert_" + pid}}, {"nicht": {"flag": "rm_e_" + id}}] + bed},
             pflicht=True, holt_leute=True)
    w["leiter"] = True
    w["akt2"] = [8, 35]
    return ABEND("rm_e_" + id, "wholesome", titel, w, bild, pid, lage, [G(pid, zeile, gefuehl)],
                 [O(t, [V(pid, 2), F("rm_e_" + id)] + (los or []), zeile=G(pid, a, g) if a else None) for t, a, g in chips], set_)


def NEU(pid, moment, zahl):
    """Offener Moment; zahl: "==1" erste Nacht, ">=2" weitere."""
    return [{"moment_offen": [pid, [moment]]}, {"moment_zahl": [pid, moment, zahl[:2], int(zahl[2:])]}]


ECHOS = [
    # Rosi
    ECHO("rosi_nacht1", "rosi", "It Was a Duel", NEU("rosi", "intimate", "==1"),
         "About last night. [clear throat] That was a duel, nobody won, and I've written it on the board, so there's no need to talk about it. Also, your watch is in the generator room, and Unit-01 is not giving it back.", "embarrassment",
         [("“I'll come and get it tonight.”", "You can try. [chuckle] She bites.", "desire"),
          ("Drinks his coffee and says nothing, smiling.", "Stop that. [sigh] It's far too early for your face.", "amusement")],
         [AUF("rosi", *GROSS)]),
    ECHO("rosi_nacht2", "rosi", "Statistically Unusual", NEU("rosi", "intimate", ">=2"),
         "That's two draws now. [chuckle] Statistically that's very unusual, so I'm looking into it.", "amusement",
         [("“Keep me posted.”", "I'll need more data. [chuckle] That's just science, Officer.", "desire"),
          ("Hands her a coffee.", None, None)],
         [AUF("rosi", *GROSS)]),
    ECHO("rosi_kuss", "rosi", "Not Talking About It", [{"moment_offen": ["rosi", ["kiss", "naehe", "naehe_weit"]]}],
         "We're not talking about it. [clear throat] I'm only telling you we're not talking about it so you know.", "embarrassment",
         [("“Talking about what?”", "Exactly. [chuckle] Good. You learn fast.", "amusement"),
          ("Nods, very seriously.", None, None)],
         [AUF("rosi", *GROSS)]),
    ECHO("rosi_nein", "rosi", "The Stopwatch", [{"flag": "rm_r_nein"}],
         "I put the stopwatch down, by the way. [chuckle] Just so you know where it is.", "amusement",
         [("“Good to know.”", None, None), ("Looks around for the stopwatch.", "Not that fast, Officer. [chuckle] Drink your coffee.", "amusement")]),
    ECHO("rosi_versetzt", "rosi", "Cold Coffee", [{"moment_offen": ["rosi", ["stood_up"]]}],
         "I waited until the coffee went cold last night, Officer. [sigh] I'm not angry. I've written it on the board, that's all, on my side.", "disappointment",
         [("“I'm sorry, Rosi. I should have come.”", "Yes, you should. [sniff] Okay. Now you've said it.", "sadness"),
          ("“Something came up.”", "Something always does. [sigh] Pass me the sugar.", "annoyance")],
         [AUF("rosi", "stood_up")]),
    ECHO("rosi_verletzt", "rosi", "Not on the Board", [{"flag": "verletzt_rosi"}],
         "I heard you've been busy, Officer. [sniff] That doesn't go on the board, nothing goes on the board. Pass me that.", "sadness",
         [("Passes it to her and stays.", None, None), ("“Rosi, let me explain.”", "No. [sigh] I'm not asking, so you don't have to explain.", "annoyance")]),
    ECHO("rosi_captain", "rosi", "Officer", [{"flag_seit": ["rm_r4", 1]}, {"flag": "rosi_zusammen"}],
         "Morning, Capt– Officer. Officer. [chuckle] Morning, Officer. Stop smiling, it's very unprofessional.", "embarrassment",
         [("“Morning, Rosi.”", None, None), ("Salutes her, very correctly.", "Oh, I hate you. [laugh] Get out of my kitchen.", "love")]),
    # Lea
    ECHO("lea_nacht1", "lea", "The Hand", NEU("lea", "intimate", "==1"),
         "Morning, s– no. I'm not doing that. My hand is not doing that. [gasp] …My hand is doing that. Did you know clownfish can change sex? I don't know why I said that.", "embarrassment",
         [("Lowers her hand gently.", "Okay. [sigh] Thanks. Okay. I'm going to go and be normal over there.", "love"),
          ("“I did not know that about clownfish.”", "Well, now you do. [chuckle] You're welcome. Oh my days.", "joy")],
         [AUF("lea", *GROSS)]),
    ECHO("lea_nacht2", "lea", "Four Hours", NEU("lea", "intimate", ">=2"),
         "I slept four hours and I feel amazing. Did you know sharks never sleep? [laugh] That's actually not true. I'm just happy.", "joy",
         [("“Me too.”", None, None), ("“Go back to bed, Lea.”", "Is that an order, or an invitation? [gasp] Don't answer that, Sophia's up.", "desire")],
         [AUF("lea", *GROSS)]),
    ECHO("lea_kuss", "lea", "For Science", [{"moment_offen": ["lea", ["kiss", "naehe", "naehe_weit"]]}],
         "I've written it down. [chuckle] Not what happened, only the date. For science.", "embarrassment",
         [("“What did you give it out of ten?”", "That's Chiara's thing. [laugh] Mine's a very good date, that's all.", "joy"),
          ("Asks to see the entry.", "Absolutely not. [gasp] It's peer-reviewed. By me.", "amusement")],
         [AUF("lea", *GROSS)]),
    ECHO("lea_glow", "lea", "About Light", [{"flag_seit": ["lea_glow", 1]}],
         "Sorry I fell asleep on your shoulder, out on the swim platform, and in the middle of a sentence too. [chuckle] The bit I didn't finish was about light, if you still want it.", "embarrassment",
         [("“Tell me everything.”", "You keep saying that. [laugh] Nobody keeps saying that.", "love"),
          ("“Another time. You needed the sleep.”", "Okay. [sigh] Another time, then. That's a promise, I'm writing it down.", "caring")]),
    ECHO("lea_versetzt", "lea", "No Face", [{"moment_offen": ["lea", ["stood_up"]]}],
         "I waited on the platform last night. The plankton came, so it wasn't a waste. [sniff] It's fine. I drew you a fish. It doesn't have a face.", "sadness",
         [("“I'm sorry, Lea. Can I see it?”", "You can. [sniff] It's not a very good fish. Thanks for asking.", "caring"),
          ("“Something came up.”", "Yeah. [sigh] That's what people say to me. Okay.", "disappointment")],
         [AUF("lea", "stood_up")]),
    ECHO("lea_verletzt", "lea", "Seahorses", [{"flag": "verletzt_lea"}],
         "Siri says you've been busy. That's nice. Busy's nice. [sniff] Did you know seahorses – no. Never mind.", "sadness",
         [("“Lea. Tell me about seahorses.”", "No. [sniff] Not today. Maybe dreckly.", "sadness"), ("Stays next to her and says nothing.", None, None)]),
    ECHO("lea_sophia", "lea", "Terrifying", [{"flag_seit": ["rm_l3", 1]}],
         "What did you say to Sophia? [chuckle] She's being nice to me. It's terrifying.", "nervousness",
         [("“Only the truth.”", "Oh no. [gasp] That's worse, that's so much worse.", "joy"), ("“Ask her.”", "I did. [laugh] She said plankton.", "amusement")]),
    ECHO("lea_tageslicht", "lea", "In Daylight", [{"flag_seit": ["rm_l4_bleib", 1]}],
         "It's daylight. [clear throat] You said you'd say it again in daylight. I'm only mentioning it.", "nervousness",
         [("“Stay. I want you here.”", "Okay. [sniff] Okay. I heard that. It's going in the book, and I still don't know.", "love"),
          ("“It was a nice night, Lea.”", "Yeah. [sniff] It was. Thanks for not saying it just to be kind.", "sadness")]),
]

# ------------------------------------------------------------------ Chiara
CHIARA = [
    ABEND("rm_c1", "wholesome", "Examiner", W_L((4, 6), "nacht", *AB("chiara", 3, 3), N("rm_c1")), "bridge", "chiara",
          "Two in the morning. On the chart table there's a stack of cards in Chiara's handwriting, all of them laminated. She "
          "pushes them across to you with one finger and doesn't look up.",
          [G("chiara", "I failed the Yachtmaster theory exam in April, and I'm sitting it again in Nice. [clear throat] Nobody knows, so now you do. You read the question and I answer, and if I get it wrong you say nothing at all. No sighing, no face.", "nervousness"),
           G("chiara", "Examiner so far: four. [chuckle] You're holding the card upside down.", "pride")],
          [O("Turns the card over and reads the first question.", [FD("rm_c1"), DIREKT("rm_c1_b")])],
          "Bridge Night"),
    ABEND("rm_c1_b", "wholesome", "Examiner", FRAME(), "bridge", "chiara",
          "She gets the first three right, fast and loud. On the fourth she stops, and her thumb starts rubbing the edge of her "
          "grandfather's old sextant.",
          [G("chiara", "Thirty-one. No. [sigh] Thirty-three. Don't look at me.", "nervousness")],
          [O("Says nothing and waits, as she asked.", [B("chiara", 6), V("chiara", 2)],
             zeile=G("chiara", "…Thirty-one degrees. Yes. Thirty-one. [chuckle] You didn't sigh. Six, for the examiner. Next card.", "pride")),
           O("“What would you do if I weren't here?”", [V("chiara", 6)],
             zeile=G("chiara", "I'd say it out loud to the sextant, like an idiot. [sniff] It was my grandfather's, and it has never once corrected me. …Fine. Thirty-one.", "caring")),
           O("“It's late, Chiara. You know this stuff.”", [V("chiara", 3)],
             zeile=G("chiara", "I knew it in April as well. [sigh] Goodnight, First Officer. Leave the cards.", "sadness"))],
          "Bridge Night"),
    ABEND("rm_c2", "frech", "Lie Still", W_L((6, 6), "nacht", *AB("chiara", 3, 4), {"flag_seit": ["rm_c1", 2]}, N("rm_c2")),
          "duc_cabin", "chiara",
          "A knock, two hard ones. Chiara comes in wearing an old St. Pauli shirt, and she is holding a laminated sheet. She closes "
          "the door behind her and starts talking before it has clicked.",
          [G("chiara", "I've made a list. [clear throat] Don't laugh, it's a short list. I have the bridge at five and you have the briefing at eight, so that gives us until about half past three, and I've left room at the end for us to agree that nobody talks about this.", "nervousness"),
           G("chiara", "Why are you looking at me like that? It's a good list. [sigh] I run a whole interior on lists. Everyone on this boat needs me to know what happens next, and I always know.", "embarrassment")],
          [O("Takes the list out of her hand and puts it face down on the desk. “Stop organising, and lie still.”",
             [V("chiara", 4), FD("rm_c2"),
              INTIM("chiara", "duc_cabin", "Cabin Night", "duc",
                    "The list lies face down on the desk. Chiara has never had nothing to plan. She finds it hard, then funny. She will rate "
                    "things, but she won't say ten.")],
             zeile=G("chiara", "…Nobody has ever said that to me. [sigh] Okay. I don't know how to do that. You'll have to tell me if I'm doing it wrong.", "love")),
           O("Reads the list carefully. “Item four needs more time.”",
             [V("chiara", 4), FD("rm_c2"),
              INTIM("chiara", "duc_cabin", "Cabin Night", "chiara",
                    "Chiara is laughing, and she takes charge of your changes to item four. She rates everything out loud, but she won't say ten.")],
             zeile=G("chiara", "More time. You want to change my schedule. [laugh] That's – eight, and you're very annoying. Show me what you'd change.", "desire")),
           O("“Not tonight, Chiara. Not on a timetable.”", [V("chiara", 4), FD("rm_c2"), F("rm_c_nein")],
             zeile=G("chiara", "No. Right, you're right, good call. [clear throat] Seven. I'm going to go and be very busy somewhere.", "embarrassment"))],
          "Cabin Night"),
    ABEND("rm_c3", "wholesome", "Who Gets the Ship?", W_L((9, 21), "abend", *AB("chiara", 4, 4), {"flag_seit": ["rm_c2", 2]}, N("rm_c3"), spaet=True),
          "sun_deck", "chiara",
          "The whole crew has just laughed at something Chiara said at dinner, and you can still hear them below. She's up here on "
          "her own now, with her shoes in one hand, and she isn't smiling at all.",
          [G("chiara", "Six seasons. I've made every one of them laugh, and every one of them tells me I'm the fun one. [sigh] Holm signed my lists without reading them, and I was so proud of that.", "neutral"),
           G("chiara", "Then you come aboard, and after three weeks Holm gives you the job. [sniff] A man with a limousine, and I had to show you where the bridge was.", "sadness"),
           G("chiara", "So I'm asking you, and don't be nice, because I'd smell it. [clear throat] If somebody asked you tomorrow who should have this ship, you or me, what do you say?", "anger")],
          [O("“You. I'd tell them today.”", [V("chiara", 6), FD("rm_c3"), F("chiara_schiff_du")],
             zeile=G("chiara", "You'd say that, and you'd mean it, and that's the problem. [chuckle] Nobody's asking you. But nine. For the answer, not for you.", "pride")),
           O("“Me, for now. You, after you pass that exam. I'll tell Megan so myself.”",
             [V("chiara", 6), B("chiara", 3), FD("rm_c3"), F("chiara_schiff_zusage"),
              FAKT("chiara", "Duc promised Chiara he will tell Megan that the ship should be hers once she has passed the Yachtmaster exam.")],
             zeile=G("chiara", "After I pass. So you do think I can. [sniff] …You'd really say that to Megan? To her face? I'm holding you to that, and I don't forget.", "love")),
           O("“You're the best one on this boat, and you know it. Why do you need me to say it?”", [B("chiara", 6), FD("rm_c3")],
             zeile=G("chiara", "Because nobody ever has. [sigh] I know what I am, First Officer. I just wanted to hear it once in somebody else's voice.", "love")),
           O("“That was Holm's call, not mine. I can't answer that.”", [V("chiara", 3), FD("rm_c3")],
             zeile=G("chiara", "No. Of course you can't. [sigh] Three.", "disappointment"))],
          "Uniform"),
    ABEND("rm_c4", "wholesome", "Vega", W_L((15, 21), "nacht", *AB("chiara", 5, 5), {"flag_seit": ["rm_c3", 2]}, N("rm_c4"), spaet=True),
          "bridge", "chiara",
          "You find her on the bridge wing in her grandfather's jacket, which is too big for her. She doesn't turn round. There are "
          "none of her laminated exam cards tonight. She lifts the old sextant, and for once in her life she is quiet.",
          [G("chiara", "[sigh] Vega, thirty-eight degrees.", "neutral"),
           G("chiara", "Arcturus, fifty-one and a bit. Polaris, forty-two, which is what it's supposed to be, so we are where we think we are. [clear throat] That's the whole sheet, and I haven't looked at a single card.", "neutral")],
          [O("Steps closer to hear her.", [FD("rm_c4"), DIREKT("rm_c4_b")])],
          "Bridge Night"),
    ABEND("rm_c4_b", "wholesome", "Vega", FRAME(), "bridge", "chiara",
          "She lowers the sextant and holds on to it with both hands. You have never heard her speak this quietly.",
          [G("chiara", "I go loud when I'm scared. You've noticed that, you notice everything. [sniff] In April I got up from that Yachtmaster exam and went straight back to the boat, and I organised a birthday party for a deckhand I didn't even like. Everyone said it was the best one yet.", "fear"),
           G("chiara", "I've rated everybody on this boat, and I've told you your number so many times it's a joke now. [sigh] Here's something that isn't a joke. Nobody has ever asked me what I want and then stayed to hear the answer. So ask me.", "love")],
          [O("“What do you want, Chiara?”",
             [V("chiara", 8), B("chiara", 8), F("chiara_zusammen"),
              FAKT("chiara", "Chiara told Duc she wants the ship and him on it, in that order. They are together now, in private. She gave him nine and a half; ten is still to come.")],
             zeile=G("chiara", "The ship. And you on it. In that order, and don't you dare be offended. [sigh] …That's the first time I've said that out loud. It wasn't so bad. Nine and a half.", "love")),
           O("Takes the sextant from her, gently, and holds it up. “Show me Vega.”",
             [V("chiara", 8), B("chiara", 8), F("chiara_zusammen"),
              FAKT("chiara", "Chiara told Duc she goes loud when she is scared, and he asked her to teach him the stars. They are together now, in private. She gave him nine and a half; ten is still to come.")],
             zeile=G("chiara", "You're asking me to teach you, now, after all that? [chuckle] …Yes. Come here, stand in front of me. Left a bit. That's it. Nine and a half, you idiot.", "love")),
           O("“You'll pass, Chiara. I know you will.”",
             [V("chiara", 8), F("chiara_offen"),
              FAKT("chiara", "Chiara told Duc she goes loud when she is scared. He told her she will pass, but he did not ask what she wants.")],
             zeile=G("chiara", "That's what everyone says, and it's still kind of you. [sigh] …Six. Goodnight, Duc.", "sadness"))],
          "Bridge Night"),
]

# ------------------------------------------------------------------ Sophia
SOPHIA = [
    ABEND("rm_s1", "wholesome", "Upside Down", W_L((4, 6), "abend", *AB("sophia", 3, 3), N("rm_s1")), "aft_deck", "sophia",
          "Sophia is at the table on the aft deck with her brown notebook open. She has just been charming a harbour master on the "
          "phone, and now she puts the phone down and the smile stays on a moment too long. A ten-euro note lies on the table.",
          [G("sophia", "Ten euros says you can't tell me what's in this notebook, darling. [chuckle] Everyone has a theory. Lea thinks it's love letters, and Chiara thinks it's a list of everyone I've ever lied to, which would need a bigger notebook.", "amusement"),
           G("sophia", "And another ten says you'll never ask me what I actually want. Nobody does. [sigh] Now go on, you've been reading that page upside down for at least a minute.", "neutral")],
          [O("Looks at the last line, in small neat letters.", [FD("rm_s1"), DIREKT("rm_s1_b")])],
          "Concierge"),
    ABEND("rm_s1_b", "wholesome", "Upside Down", FRAME(), "aft_deck", "sophia",
          "The last line in her notebook says: The vicar had been dead since Tuesday, which explained the marmalade. It's a detective "
          "story. Sophia watches you read it and does not move at all.",
          [G("sophia", "Well, darling? [clear throat] What does it say?", "nervousness")],
          [O("Reads the line out loud, very seriously. “…which explained the marmalade.”", [B("sophia", 6), V("sophia", 2), F("sophia_vikar")],
             zeile=G("sophia", "[laugh] …Keep the ten euros, darling. You didn't read that. Say you didn't read that.", "embarrassment")),
           O("Pushes the note back. “Love letters. Lea's right.”", [V("sophia", 6), F("sophia_vikar")],
             zeile=G("sophia", "How kind of you. You read every word, and you're giving me my lie back. [chuckle] I shall remember that.", "caring")),
           O("“I wouldn't read your private notes.”", [V("sophia", 3)],
             zeile=G("sophia", "No? How very correct. [chuckle] I do wonder who raised you.", "amusement"))],
          "Concierge"),
    ABEND("rm_s2", "frech", "The Forfeit", W_L((6, 6), "nacht", *AB("sophia", 3, 4), {"flag_seit": ["rm_s1", 2]}, N("rm_s2")),
          "aft_deck", "sophia",
          "Past midnight. Sophia has laid out a pack of cards on the table, and she's dealing to you without asking. Her glasses are "
          "pushed up in her hair. She loses the first hand, and the second. You've watched her take money from Yamamoto every night "
          "for a week.",
          [G("sophia", "How careless of me. [chuckle] That's two you've won, darling, and we never agreed what we were playing for.", "amusement"),
           G("sophia", "I'm offering the forfeit myself, you'll notice, and that has never happened. [sigh] I've gone over it, and I can't find the angle, and I generally can.", "nervousness"),
           G("sophia", "So you may tell me to go to bed, and I'll be perfectly charming about it at breakfast. Or you may tell me what you'd like. [clear throat] Do be careful which, because I'd rather like you to mean it.", "desire")],
          [O("Gathers up the cards. “You lost on purpose. What do you want, Sophia?”",
             [V("sophia", 4), FD("rm_s2"),
              INTIM("sophia", "duc_cabin", "Writing Night", "sophia",
                    "Sophia takes off her glasses and folds them. Her charm slips bit by bit, and her sentences get short and plain.")],
             zeile=G("sophia", "[sigh] …You owe me ten euros. Come inside.", "love")),
           O("“My cabin. Bring the cards.”",
             [V("sophia", 4), FD("rm_s2"),
              INTIM("sophia", "duc_cabin", "Writing Night", "sophia",
                    "Sophia brings the cards, and she bets on everything. Somewhere along the way the show slips, and she notices and lets it.")],
             zeile=G("sophia", "Oh, well played. [chuckle] That's the first thing you've said all week that I could have written.", "desire")),
           O("“Go to bed, Sophia. Lose to me when you mean it.”", [V("sophia", 6), FD("rm_s2"), F("rm_s_nein")],
             zeile=G("sophia", "Hm. That's a better line than any I had ready. [chuckle] Goodnight, darling.", "admiration"))],
          "Writing Night"),
    ABEND("rm_s3", "wholesome", "Fourteen", W_L((9, 21), "abend", *AB("sophia", 4, 4), {"flag_seit": ["rm_s2", 2]}, N("rm_s3"), spaet=True),
          "duc_cabin", "sophia",
          "Sophia knocks and comes in, which she never does, because people come to her. She has an envelope in her hand. It's "
          "addressed to M. J. Penrose, care of the harbour office in Cala d'Orsu, and it has been opened.",
          [G("sophia", "You once read a line in my notebook, the vicar and the marmalade, so I suppose you may as well have the rest. [sigh] There's no such person as M. J. Penrose. She has written three detective novels and has had fourteen letters from publishers. This one makes fifteen.", "neutral"),
           G("sophia", "They're very polite. This one says my dialogue is charming. [chuckle] I've been told so all my life, darling, and I've come to think it's what people say when they haven't looked at you.", "amusement"),
           G("sophia", "Nobody on this boat knows. I don't want to be comforted, and I'd see it coming anyway. [sniff] I only wanted somebody to know, and I find that was the whole of it.", "sadness")],
          [O("Holds out his hand for the letter. “What's the next book about?”", [V("sophia", 6), B("sophia", 3), FD("rm_s3"),
              FAKT("sophia", "Sophia told Duc that she writes detective novels as M. J. Penrose and has fifteen rejection letters. Nobody else on board knows.")],
             zeile=G("sophia", "The next – you're asking me about the next one. Not one of the fifteen ever asked that. [sniff] …A woman who manages everyone. She's found on page one, and nobody can say who she was.", "love")),
           O("“Can I read the first one?”", [V("sophia", 6), FD("rm_s3"),
              FAKT("sophia", "Sophia told Duc that she writes detective novels as M. J. Penrose and has fifteen rejection letters. Nobody else on board knows. She lent him the first book.")],
             zeile=G("sophia", "It isn't very good. Yes, you may. [clear throat] Bring it back, and don't be kind about it, or I shall know.", "nervousness")),
           O("“Fifteen letters, and you still write every night. That's the bravest thing on this boat.”", [B("sophia", 6), FD("rm_s3"),
              FAKT("sophia", "Sophia told Duc that she writes detective novels as M. J. Penrose and has fifteen rejection letters. Nobody else on board knows.")],
             zeile=G("sophia", "There it is, the comfort. It's very well made, darling. [sigh] …Thank you. Don't do it again.", "caring"))],
          "Writing Night"),
    ABEND("rm_s4", "wholesome", "The Last Train",
          W_L((15, 21), "nacht", *AB("sophia", 5, 5), {"flag_seit": ["rm_s3", 2]}, N("lea_zusammen"), N("rm_s4"), spaet=True),
          "aft_deck", "sophia",
          "The aft deck after everyone has gone. Sophia is sitting on the deck boards with her back against a chair. No lipstick. She "
          "has her glasses on, properly, and you have never seen that. She doesn't call you darling.",
          [G("sophia", "Sit down, Duc. [sigh] There's no bet.", "neutral"),
           G("sophia", "My father left when I was ten. I was charming by eleven. [sniff] You see how that works.", "sadness"),
           G("sophia", "Then there was Lea, and the rent, and Mum. I got good at it. I got so good that nobody asks any more. [sigh] Two years I stood in the wings of a London theatre, waiting to go on for someone else. I knew every line. I never once went on.", "sadness"),
           dict(G("sophia", "My sister salutes you in corridors. I've noticed. [sigh] You'll have to choose before the Festa, and I won't do it for you.", "caring"),
                gruppe="lea", wenn={"flag": "rm_l1"})],
          [O("Waits.", [FD("rm_s4"), DIREKT("rm_s4_b")])],
          "Writing Night"),
    ABEND("rm_s4_b", "wholesome", "The Last Train", FRAME(), "aft_deck", "sophia",
          "She looks at the dark water for a while. Then she says something, not loud and not to you, as if the theatre were empty.",
          [G("sophia", "The last train has gone, and I find I don't mind at all. [sniff] …That's the line, from the play. I waited two years to say it, and I never have until now. I don't know who I am when I'm not performing. So tell me. What do you see?", "love")],
          [O("Sits down next to her. “I see a tired woman with ink on her chin. I like her.”",
             [V("sophia", 8), B("sophia", 8), F("sophia_zusammen"),
              FAKT("sophia", "Sophia dropped the show with Duc and asked him what he sees, and he said a tired woman with ink on her chin, and that he likes her. They are together now, in private. With him she does not have to charm.")],
             zeile=G("sophia", "…Ink? Have I? [sniff] Good. Leave it there. Nobody has ever liked that one.", "love")),
           O("“You once bet me ten euros I'd never ask what you want. So I'm asking. What do you want?”",
             [V("sophia", 8), B("sophia", 8), F("sophia_zusammen"),
              FAKT("sophia", "Sophia dropped the show with Duc. He asked what she wants: her own name on a book, and somebody she does not have to charm. They are together now, in private.")],
             zeile=G("sophia", "You remembered that bet. [sigh] …I want my own name on a book. And I want somebody I don't have to charm. I'd like both, if that's allowed.", "love")),
           O("“I don't know what I see yet, Sophia. But I'm still here.”",
             [V("sophia", 8), F("sophia_offen"),
              FAKT("sophia", "Sophia dropped the show with Duc and asked him what he sees. He said he doesn't know yet, but stayed.")],
             zeile=G("sophia", "Yes, you are. [sigh] That's honest. Stay a little.", "caring"))],
          "Writing Night"),
]

LAGE_ECHO.update({
    "chiara": ("bridge", "Uniform", "Early morning on the bridge, and nobody else is up yet. Chiara is checking a list that doesn't need "
               "checking. She doesn't look up, but she has poured a second coffee."),
    "sophia": ("aft_deck", "Concierge", "Early morning on the aft deck, and nobody else is up yet. Sophia sits with her notebook and a "
               "cup of tea, already perfect, as if she had never been to bed."),
})

ECHOS += [
    ECHO("chiara_nacht1", "chiara", "No Number", NEU("chiara", "intimate", "==1"),
         "Last night. I'm not giving you a number. [chuckle] I have one, I'm just not giving it to you. Your coffee's there.", "embarrassment",
         [("“Is it a good number?”", "It's a number. [chuckle] Drink your coffee, First Officer.", "amusement"),
          ("Drinks the coffee, and makes a face at it. “Coffee: four.”", "You don't get to rate. [laugh] Only I rate. …Five, for trying.", "joy")],
         [AUF("chiara", *GROSS)]),
    ECHO("chiara_nacht2", "chiara", "Eight", NEU("chiara", "intimate", ">=2"),
         "Eight. That's for last night, and it's only eight because you looked as if you were going to ask. [chuckle] Don't ask.", "desire",
         [("Doesn't ask.", "Good. [chuckle] Eight and a bit.", "amusement"), ("“What would make it nine?”", "Oh, you'd love to know. [laugh] Bridge, tonight. Bring your own coffee.", "desire")],
         [AUF("chiara", *GROSS)]),
    ECHO("chiara_kuss", "chiara", "Six", [{"moment_offen": ["chiara", ["kiss", "naehe", "naehe_weit"]]}],
         "Kiss: six. [clear throat] The technique was fine and the timing was terrible. You're on the watch list tonight, and that's unrelated.", "amusement",
         [("“Six? I'll want a rematch.”", "That's what the watch list is for. [chuckle] Don't be late.", "desire"), ("Salutes.", None, None)],
         [AUF("chiara", *GROSS)]),
    ECHO("chiara_nein", "chiara", "Seven, for the No", [{"flag": "rm_c_nein"}],
         "You said no, the other night. Nobody says no to me. [chuckle] Seven, for the no, so don't let it go to your head.", "pride",
         [("“Thanks, Chief.”", None, None), ("“I still don't do timetables.”", "We'll see. [chuckle] I can make a very short one.", "amusement")]),
    ECHO("chiara_versetzt", "chiara", "Zero", [{"moment_offen": ["chiara", ["stood_up"]]}],
         "You left me waiting last night. Last night: zero. [sigh] I looked to see if the scale goes any lower, and it doesn't.", "disappointment",
         [("“I'm sorry, Chiara. I should have come.”", "Yes. [sigh] That gets you up to one.", "sadness"), ("“Something came up.”", "On this boat, something always does. [clear throat] I know, I'm usually the one fixing it.", "annoyance")],
         [AUF("chiara", "stood_up")]),
    ECHO("chiara_verletzt", "chiara", "Nothing to Rate", [{"flag": "verletzt_chiara"}],
         "I heard about you and someone else. You don't need to say anything. [sniff] The deck's clean, the coffee's hot, and I've got nothing to rate today.", "sadness",
         [("Stays next to her and says nothing.", None, None), ("“Chiara, let me explain.”", "No. [sigh] I run a boat, First Officer. I've got work to do.", "annoyance")]),
    ECHO("chiara_duc", "chiara", "Your Name", [{"flag_seit": ["rm_c4", 1]}, {"flag": "chiara_zusammen"}],
         "Good morning, Duc. I know, I said your name. [chuckle] If you tell anyone, I'll put you on toilets.", "embarrassment",
         [("“Good morning, Chiara.”", None, None), ("“Nine and a half, you said.”", "I did. [laugh] And I'm not rounding up, so don't ask.", "love")]),
    ECHO("sophia_nacht1", "sophia", "A First", NEU("sophia", "intimate", "==1"),
         "Good morning, darling. You look rested, and I'd hide that if I were you. [chuckle] I've written nothing at all about last night, which is a first.", "amusement",
         [("“Nothing at all?”", "Not a word. [sigh] It's a little frightening, actually.", "love"), ("Sits down and steals her tea.", "That is my tea. [chuckle] Well. It seems we've moved on to that.", "desire")],
         [AUF("sophia", *GROSS)]),
    ECHO("sophia_nacht2", "sophia", "The Weather", NEU("sophia", "intimate", ">=2"),
         "Ten euros says you smile at the briefing. [chuckle] I've already told Chiara it's about the weather.", "amusement",
         [("“You're on.”", "Do try, darling. [chuckle] I've seen your face.", "desire"), ("Smiles, and loses the bet.", "That's ten euros. [laugh] You're terribly easy.", "joy")],
         [AUF("sophia", *GROSS)]),
    ECHO("sophia_kuss", "sophia", "Not in the Script", [{"moment_offen": ["sophia", ["kiss", "naehe", "naehe_weit"]]}],
         "That wasn't in the script, darling. [chuckle] I've checked.", "amusement",
         [("“Then write it in.”", "I already have. [chuckle] You come out of it rather well.", "desire"), ("Says nothing and smiles.", None, None)],
         [AUF("sophia", *GROSS)]),
    ECHO("sophia_nein", "sophia", "Lose When You Mean It", [{"flag": "rm_s_nein"}],
         "You said no to me, over the cards. [chuckle] Nobody's done that since the West End. I shall have to use it.", "admiration",
         [("“Use it well.”", "I always do, darling. [chuckle] It keeps me honest.", "amusement"), ("“I meant it.”", "I know. [sigh] That's what makes it so usable.", "caring")]),
    ECHO("sophia_versetzt", "sophia", "Until One", [{"moment_offen": ["sophia", ["stood_up"]]}],
         "I sat on the aft deck until one, and nobody has ever done that to me. [sigh] I'm not cross, darling. I'm writing it down.", "disappointment",
         [("“I'm sorry, Sophia. I should have come.”", "Yes, you should. [sigh] It's a very good scene, though. I may keep it.", "sadness"), ("“Something came up.”", "Something so often does. [chuckle] Do try to be more original next time.", "annoyance")],
         [AUF("sophia", "stood_up")]),
    ECHO("sophia_verletzt", "sophia", "Lovely for Everyone", [{"flag": "verletzt_sophia"}],
         "I hear you've been busy, darling. [sigh] How lovely for everyone.", "sadness",
         [("“Sophia, let me explain.”", "Oh, please don't. [sigh] I'd only correct the dialogue.", "annoyance"), ("Stays, and doesn't explain.", None, None)]),
    ECHO("sophia_lippenstift", "sophia", "Nine O'Clock", [{"flag_seit": ["rm_s4", 1]}, {"flag": "sophia_zusammen"}],
         "Morning, darling. Yes, the lipstick's back on, and it's nine o'clock. [chuckle] You know what's under it, so behave.", "amusement",
         [("“There's still ink on your chin.”", "[gasp] There is not. …Is there?", "embarrassment"), ("Nods. “Morning, Sophia.”", None, None)]),
]

for _e in ECHOS:                  # eine Antwort ohne Zeile bleibt still
    for _o in _e["optionen"]:
        if _o.get("zeile") is None:
            _o.pop("zeile", None)

# ------------------------------------------------------------------ Lola
LOLA = [
    ABEND("rm_o1", "wholesome", "The Spoon", W_L((4, 6), "abend", *AB("lola", 3, 3), N("rm_o1")), "galley", "lola",
          "The galley smells of burnt sugar. A pan is in the sink, and there's another one on the stove. Lola looks up, sees you in "
          "the doorway, and waves her wooden spoon at you.",
          [G("lola", "Don't watch me, Boss, that's the whole problem. [laugh] I'm the best cook you've ever met until somebody looks at me, and then I burn things. Two caramels tonight, and that's since you walked in.", "embarrassment"),
           G("lola", "So turn round and face the wall, and tell me something boring. [sigh] I reckon it's the only way this one makes it to the table.", "nervousness")],
          [O("Turns his back and tells her about the insurance forms.", [FD("rm_o1"), DIREKT("rm_o1_b")])],
          "Galley"),
    ABEND("rm_o1_b", "wholesome", "The Spoon", FRAME(), "galley", "lola",
          "You talk to the wall for five minutes. Behind you the pan stops hissing. Then a warm spoon touches your lip, and bare feet "
          "come up on the tiles beside you.",
          [G("lola", "Don't turn round yet. Just taste. [clear throat] And tell me straight: is it actually good, or are you just being nice to me?", "nervousness")],
          [O("“It's actually good, Lola. Now can I turn round?”", [B("lola", 6), V("lola", 2)],
             zeile=G("lola", "Yeah? Okay. [laugh] Okay, you can turn round, but slowly, I'm still holding hot sugar. Mostly the sugar.", "love")),
           O("“It needs a little salt.”", [V("lola", 6)],
             zeile=G("lola", "It does, doesn't it? [chuckle] Nobody ever tells me that. They just say yum and run away. Sweet as, Boss. Salt it is.", "joy")),
           O("“It's great. You always say that, and it's always great.”", [V("lola", 3)],
             zeile=G("lola", "Yeah. No worries. [sigh] That's what everyone says, mate.", "sadness"))],
          "Galley"),
    ABEND("rm_o2", "frech", "Breakfast in Bed", W_L((6, 6), "fruehstueck", *AB("lola", 3, 4), {"flag": "lola_abend"}, {"flag_seit": ["rm_o1", 1]}, N("rm_o2")),
          "duc_cabin", "lola",
          "Someone kicks your cabin door, gently, because both her hands are full. Lola comes in backwards with a tray, wearing your "
          "shirt, and there is a pancake on it that is nearly in the shape of a heart.",
          [G("lola", "Room service, Boss. It's meant to be a heart, like the one from the morning after I knocked on your door, but this one slid. [laugh] So it's more of a kidney. It's a very romantic kidney.", "joy"),
           G("lola", "I've never done this before. In Sydney you ate standing up, if the chef let you eat at all. [sigh] So I don't know how it goes. Do I stay, or do I just put it down and go back to my stove?", "nervousness")],
          [O("Moves over and lifts the covers. “Stay. It can get cold.”",
             [V("lola", 4), FD("rm_o2"),
              INTIM("lola", "duc_cabin", "Off Duty", "lola",
                    "The pancakes are getting cold on the tray. Lola has never been allowed to be slow near food, and here she can be. She laughs a lot, and nobody yells.")],
             zeile=G("lola", "It can get cold. [gasp] Oh, that's the best thing anyone's ever said about my food.", "desire")),
           O("Takes the fork and eats the kidney, all of it, watching her.", [V("lola", 8), B("lola", 3), FD("rm_o2")],
             zeile=G("lola", "You're looking at me, and I didn't burn it. [sniff] Mate. I didn't burn it. …Is there more? I can do more.", "love")),
           O("“I've got the briefing, Lola. Leave it on the desk, thanks.”", [V("lola", 2), FD("rm_o2")],
             zeile=G("lola", "No worries, Boss. Yep. On the desk. [clear throat] Mostly on the desk.", "sadness"))],
          "Off Duty"),
    ABEND("rm_o3", "wholesome", "Sunday, Nan", W_L((9, 21), "nacht", *AB("lola", 4, 4), {"flag_seit": ["rm_o2", 2]}, N("rm_o3"), spaet=True),
          "galley", "lola",
          "The galley lights are off. Lola is sitting on the floor against the fridge with her phone in her lap. It's Sunday, and she "
          "has just rung her Nan in Byron Bay, as she does every Sunday, because Nan once called out the coast guard when she didn't.",
          [G("lola", "Nan's ninety-one. She asked if I was head chef yet. [sniff] I said yes, Nan, on a superyacht. I didn't say it's a broken boat in a bay, and I didn't say what I do when somebody yells at me.", "sadness"),
           G("lola", "You've seen it. Somebody shouts an order and I go “Yes, Chef”, and my hands stop. I got out of that kitchen in Sydney years ago, and I still do it. [sigh] Everyone's dead keen on me until it counts.", "fear"),
           G("lola", "So, straight answer, Boss, and no jokes, I do enough for both of us. [sigh] If it all goes wrong here, do you want me next to you, or do you want somebody useful?", "fear")],
          [O("“You. Next to me. And I'll stop anyone who yells at you.”", [V("lola", 6), B("lola", 4), FD("rm_o3"),
              FAKT("lola", "Lola told Duc that she freezes when someone yells and that she is homesick. He told her he wants her next to him when it counts.")],
             zeile=G("lola", "You can't stop everyone. [sniff] …You'd try, though, wouldn't you? Okay. Okay, cool. Cool cool cool.", "love")),
           O("“You. And you'll stop them yourself. I've seen you with a knife.”", [V("lola", 8), FD("rm_o3"),
              FAKT("lola", "Lola told Duc that she freezes when someone yells and that she is homesick. He told her she can stand up to it herself.")],
             zeile=G("lola", "With a knife. [laugh] Mate, that's the nicest thing anyone's ever said to me on a floor.", "joy")),
           O("Sits down next to her and rings Nan back on speaker. “Tell her the truth. I'll hold the phone.”", [V("lola", 8), FD("rm_o3"),
              FAKT("lola", "Lola told Duc that she freezes when someone yells and that she lied to her Nan about her job. He sat with her while she rang Nan back and told her the truth.")],
             zeile=G("lola", "Oh, you absolute – it's ringing. Boss, it's ringing! [gasp] Nan? Hi, Nan. No, nobody's died. I've got something to tell you.", "nervousness")),
           O("“Get some sleep, Lola. It'll look better tomorrow.”", [V("lola", 2), FD("rm_o3")],
             zeile=G("lola", "Yeah. Sweet as. [sigh] Night, Boss.", "sadness"))],
          "Off Duty"),
    ABEND("rm_o4", "wholesome", "First Guest", W_L((15, 21), "abend", *AB("lola", 5, 5), {"flag_seit": ["rm_o3", 2]}, N("rm_o4"), spaet=True),
          "village_harbour", "lola",
          "Evening at the far end of the harbour. Lola has walked you past the last boat to an old fisherman's hut with no door. There's "
          "a stove inside on two bricks, and in front of it there are four stools that don't match. You know this place: she has been "
          "drawing it on napkins ever since you met her.",
          [G("lola", "Four stools, one stove and no head chef. Nobody yells. If somebody yells, they're out. [chuckle] Petru says the roof's mostly a suggestion.", "nervousness"),
           G("lola", "I always lose the end of my sentences, you've noticed. I do it on purpose. If you don't finish, nobody can tell you it's wrong. [sigh] So this one I'm going to finish. Watch me.", "fear"),
           G("lola", "I want this hut, and I want you on that stool, the one that doesn't wobble. [sigh] Not tonight, I mean every day. Will you be my first guest?", "love")],
          [O("Sits down on the stool that doesn't wobble. “First guest. Every day. What's for dinner?”",
             [V("lola", 8), B("lola", 8), F("rm_o4"), F("lola_zusammen"),
              FAKT("lola", "Lola showed Duc the old fisherman's hut at the harbour, the beach kitchen she dreams of, and asked him to be her first guest every day. He said yes. They are together now, in private.")],
             zeile=G("lola", "You said it. You actually – I finished a whole sentence, and you said yes. [sniff] Bao. Obviously bao. Don't you dare say they need salt.", "love")),
           O("“What's it called? On the napkins there's only half a name.”",
             [V("lola", 8), B("lola", 6), F("rm_o4"), F("lola_zusammen"),
              FAKT("lola", "Lola showed Duc the old fisherman's hut at the harbour, the beach kitchen she dreams of, and asked him to be her first guest every day. They are together now, in private. The kitchen still has no name.")],
             zeile=G("lola", "I never could finish that either. [laugh] We've got time. Sit down, you're the first guest, you can help me pick.", "love")),
           O("“It's beautiful, Lola. But I can't promise you every day.”",
             [V("lola", 8), F("rm_o4"), F("lola_offen"),
              FAKT("lola", "Lola showed Duc the old fisherman's hut at the harbour and asked him to be her first guest every day. He said he cannot promise that, and she took it well.")],
             zeile=G("lola", "No. Fair enough. [sniff] First guest some days, then. The stool's not going anywhere, mate. It's got a very bad leg.", "caring"))],
          "Off Duty"),
]

# ------------------------------------------------------------------ Alva
ALVA = [
    ABEND("rm_a1", "wholesome", "The Board", W_L((4, 6), "abend", *AB("alva", 3, 3), N("rm_a1")), "alvas_bar", "alva",
          "Closing time at the bar. Behind the counter hangs her father's old chalkboard: every name in the village, and next to each "
          "name what that person orders. She catches you reading it and takes down the chalk.",
          [G("alva", "Forty years of my father's handwriting, and I've kept it going. [chuckle] Everyone's up there, o figliolu, everyone's welcome. You've been coming in for days and you're still not on it.", "amusement"),
           G("alva", "So what do you drink? And don't say what you think sounds good. [sigh] The board only takes the truth.", "curiosity")],
          [O("“Whatever you pour for yourself after closing.”", [B("alva", 6), V("alva", 2), FD("rm_a1"), F("alva_tafel_ihr")],
             zeile=G("alva", "That's clever, and you can't have it, because nobody knows what that is. [chuckle] It isn't even on the board. Look for my name, you won't find it.", "desire")),
           O("“Myrtle. It's what you gave me the first night, and I've been drinking it to be polite.”", [V("alva", 6), FD("rm_a1")],
             zeile=G("alva", "Polite. [laugh] I'm writing that down: one myrtle, reluctantly. That's the best one on the board.", "amusement")),
           O("“Just coffee. I've got an early start.”", [V("alva", 3), FD("rm_a1")],
             zeile=G("alva", "Coffee. Sensible. [chuckle] There's one of you in every village, and he never gets a story.", "neutral"))],
          "alva_standard"),
    ABEND("rm_a2", "frech", "The Jukebox", W_L((6, 6), "nacht", *AB("alva", 3, 4), {"flag_seit": ["rm_a1", 2]}, N("rm_a2")), "alvas_bar", "alva",
          "The bar is shut and the chairs are up. The old jukebox in the corner, silent since her father died three years ago, has its "
          "back panel off. You've been at it for an hour with Rosi's screwdriver, because Alva asked you not to bother. Now it hums.",
          [G("alva", "Don't. [gasp] I didn't say you could. That machine played one song all my life, because Papa only ever wanted the one.", "fear"),
           G("alva", "Everybody in this village has asked me to fix that thing, and every one of them wanted something. [sigh] So what do you want, o figliolu, standing there with your hands full of my father's jukebox?", "desire")],
          [O("Drops in a coin. “One dance. That's all.”",
             [V("alva", 4), FD("rm_a2"),
              INTIM("alva", "alvas_bar", "alva_flamenco_noche", "alva",
                    "Her father's song is playing in her locked bar for the first time in three years. Alva leads: heel, then the floor. She is warm and mocking, and very close.")],
             zeile=G("alva", "One. [sigh] That's what they all say. Heel, then the floor, and you look at me as if you've already won. Come here.", "desire")),
           O("Puts the panel back on and leaves the coin on the bar. “Nothing. It's yours. Play it when you want.”",
             [V("alva", 10), B("alva", 3), FD("rm_a2")],
             zeile=G("alva", "Nothing. [chuckle] You'll have to explain that word to me. Nobody in here has ever used it. …Go on, go home, before I ask you to stay.", "love")),
           O("“I wanted to see if I could. Goodnight, Alva.”", [V("alva", 3), FD("rm_a2")],
             zeile=G("alva", "An honest man and a working jukebox, on the same night. [chuckle] I'll need a drink.", "amusement"))],
          "alva_flamenco_noche"),
    ABEND("rm_a3", "wholesome", "Papa's Photo", W_L((9, 21), "fruehstueck", *AB("alva", 4, 4), {"flag": "alva_abend"}, {"flag_seit": ["rm_a2", 2]}, N("rm_a3"), spaet=True),
          "alvas_bar", "alva",
          "Morning in the bar, before anyone comes. You came over for coffee. Alva is on a stool in a man's old shirt, with her father's "
          "photo from the wall lying on the counter in front of her, and she has not put the lights on.",
          [G("alva", "I tell everyone the same story. I was twenty-two, I had a place in Seville to dance, Papa had his stroke, and I came home. [sigh] They all love it. Poor Alva, she gave it all up. I've served a lot of drinks on that story.", "neutral"),
           G("alva", "I had a place in the back row, o figliolu. I'd seen the others. I was never going to be my grandmother. When my mother rang about Papa, I cried, and then, God forgive me, I was glad. [sniff] I've never said that to anyone. Not to him either.", "remorse"),
           G("alva", "So tell me, since you're the one who's here. [sigh] Would you still come in for a coffee, knowing the woman behind this bar stayed because she was scared?", "fear")],
          [O("Pulls up a stool. “Twice a day. What do you drink, Alva?”", [V("alva", 6), B("alva", 4), FD("rm_a3"),
              FAKT("alva", "Alva told Duc that she came home from Seville partly because she was scared, not only for her father. Nobody else knows. He stayed.")],
             zeile=G("alva", "You and that question. [sniff] Bring the coffee over here, then. I don't serve scared women, they drink for free.", "love")),
           O("“You stayed thirteen years. That isn't what scared people do.”", [V("alva", 8), FD("rm_a3"),
              FAKT("alva", "Alva told Duc that she came home from Seville partly because she was scared, not only for her father. Nobody else knows. He told her that staying thirteen years took courage.")],
             zeile=G("alva", "No. It's what stubborn people do. [chuckle] Don't be kind to me this early, it's bad for business.", "gratitude")),
           O("“Go to Seville, Alva. It isn't too late.”", [V("alva", 4), FD("rm_a3"),
              FAKT("alva", "Alva told Duc that she came home from Seville partly because she was scared. He told her to go now.")],
             zeile=G("alva", "Thirty-five, in the back row, in ruffles. [laugh] Oh, o figliolu. Drink your coffee.", "amusement"))],
          "alva_morgen"),
    ABEND("rm_a4", "wholesome", "Chalk", W_L((15, 21), "nacht", *AB("alva", 5, 5), {"flag_seit": ["rm_a3", 2]}, N("rm_a4"), spaet=True),
          "alvas_bar", "alva",
          "Last orders were an hour ago. Alva has wiped the whole bottom corner of her father's chalkboard, the board with every name in "
          "the village and what they drink. There is one new line there, in her own handwriting: ALVA, and next to it nothing. She is "
          "holding out the chalk to you.",
          [G("alva", "Everybody's welcome, nobody's mine. I've been saying that for thirteen years, and I'm very good at it. [sigh] Forty years on that board, and not one person ever asked what goes next to my name.", "neutral"),
           G("alva", "You did, the first week, and I made a joke. [sniff] So I'm not joking now. Take the chalk, o figliolu. What goes next to my name?", "love")],
          [O("“I don't know. Tell me, and I'll write it.”",
             [V("alva", 8), B("alva", 8), F("rm_a4"), F("alva_zusammen"),
              FAKT("alva", "Alva wrote her own name on her father's board and asked Duc what goes next to it. She told him what she really drinks: water, and one coffee at four when nobody is there. They are together now, in private, and she tells nobody.")],
             zeile=G("alva", "Water. And one coffee, at four, when nobody's here. [sniff] That's all it's ever been. Write it down. You're the only one who's ever going to know that.", "love")),
           O("Writes his own name next to hers, small, and gives back the chalk.",
             [V("alva", 8), B("alva", 8), F("rm_a4"), F("alva_zusammen"),
              FAKT("alva", "Alva wrote her own name on her father's board and asked Duc what goes next to it, and he wrote his own name. They are together now, in private, and she tells nobody.")],
             zeile=G("alva", "That's not a drink. [laugh] It's bad chalk work, too. …Papa would have wiped that off. Leave it where it is.", "love")),
           O("Puts the chalk on the bar. “That's yours to write, Alva. Not mine.”",
             [V("alva", 10), F("rm_a4"), F("alva_offen"),
              FAKT("alva", "Alva wrote her own name on her father's board and asked Duc what goes next to it. He told her it is hers to write, and she respected that.")],
             zeile=G("alva", "Hm. [chuckle] Thirteen years, and the first man I ask tells me to do it myself. That's why I asked you, o figliolu.", "admiration"))],
          "alva_flamenco_noche"),
]

# ------------------------------------------------------------------ Siri (nur nach der Trennung von Yasin, ueberspringt nie eine Stufe)
FREI_S = {"flag": "siri_frei"}
SIRI = [
    ABEND("rm_i1", "wholesome", "Caption", W_L((4, 6), "abend", *AB("siri", 3, 3), FREI_S, N("rm_i1")), "foredeck", "siri",
          "The foredeck at sunset. Siri is sitting on a coil of rope in her father's old jumper, the one with the stars on it, and she "
          "says sorry to the rope as you sit down. Her phone is showing a photo of her and a message from her manager.",
          [G("siri", "Hiii guys, golden hour, grateful for this journey. [sigh] That's the caption my manager wants under this. I haven't written my own since I was nineteen. Six years, can you believe that? I don't even know how I'd sound.", "neutral"),
           G("siri", "Can I ask you something? Just us, no camera. [clear throat] You've seen me with no make-up and with a chair I was apologising to. What would you write under this picture, if it was true?", "curiosity")],
          [O("Looks at the photo for a long time. “Tired. But she's smiling with the left side now.”", [B("siri", 6), V("siri", 2), FD("rm_i1")],
             zeile=G("siri", "The left side. [laugh] That's the real one, nobody's ever noticed that. …Sorry. Sorry, I'm doing it now, aren't I?", "love")),
           O("“I wouldn't. What would you write?”", [V("siri", 6), FD("rm_i1")],
             zeile=G("siri", "I don't know. Isn't that terrible? [sniff] But you asked, and nobody asks. Give me some time, I'll try.", "gratitude")),
           O("“Grateful for this journey. It's good. It's your job.”", [V("siri", 2), FD("rm_i1")],
             zeile=G("siri", "Yes. Sorry. [sigh] It is my job. Golden hour, yes.", "sadness"))],
          "Dad's Sweater"),
    ABEND("rm_i2", "frech", "One Star", W_L((6, 6), "nacht", *AB("siri", 3, 4), FREI_S, {"flag_seit": ["rm_i1", 2]}, N("rm_i2")), "foredeck", "siri",
          "A warm night on the foredeck, and nobody else is up. Siri has put her phone face down on the deck, far away from her, the way "
          "you'd move a dog that bites. She is holding the sleeve of her father's jumper out to you, the one he knitted with a star for "
          "each winter evening.",
          [G("siri", "He knitted one star every evening, all one winter, and I never wore it. Feel, they're all a bit wrong. [sniff] It's the only thing I own that nobody took a picture of until this week.", "caring"),
           G("siri", "I've been looked at for six years by nearly three million people. I know exactly how I look from every side. [sigh] I don't know how it is when nobody's looking and nobody's going to post it. Will you go slowly? Is that a stupid thing to ask?", "nervousness")],
          [O("“It isn't stupid. As slow as you want. You can stop whenever you like.”",
             [V("siri", 4), FD("rm_i2"),
              INTIM("siri", "foredeck", "Dad's Sweater", "siri",
                    "No camera and no poses. Siri laughs at herself first and says sorry too often, and she stops now and then to check how this feels, because nobody has ever asked her.")],
             zeile=G("siri", "Okay. [sigh] Okay. Then I'll keep the jumper on for now. Sorry. No, I'm not sorry.", "love")),
           O("Takes her sleeve and counts the stars out loud, all of them, and doesn't do anything else.", [V("siri", 10), B("siri", 3), FD("rm_i2")],
             zeile=G("siri", "Forty-one. He was so stubborn. [sniff] …I think that's the nicest thing anyone's ever done to me, and you didn't even do anything.", "love")),
           O("“It's late, Siri. Another night.”", [V("siri", 3), FD("rm_i2"), F("rm_i_nein")],
             zeile=G("siri", "Yes. Sorry. No, you're right. [sigh] Thank you for saying it nicely.", "caring"))],
          "Dad's Sweater"),
    ABEND("rm_i3", "wholesome", "Salmon", W_L((9, 21), "abend", *AB("siri", 4, 4), FREI_S, {"flag_seit": ["rm_i2", 2]}, N("rm_i3"), spaet=True), "solar_deck", "siri",
          "The solar deck, in the evening. Siri holds out her phone without saying anything. It's a contract from her manager, a big "
          "sponsorship with a salmon company, already signed in her name. You've heard about her father, the fisherman on a tiny Norwegian "
          "island who has spent two years fighting these farms and hardly speaks to her.",
          [G("siri", "It's the same farms, the ones my father stands up against at every island meeting. [sniff] He thinks I'm ashamed of where I'm from. If I post this, he'll never call me again.", "fear"),
           G("siri", "But if I say no, my manager leaves, and he runs my whole account. It's all I've got, and I don't know how to do anything else. [sigh] I've never decided anything by myself. What would you do?", "fear")],
          [O("“I'd say no. And I'd ring him first, before I told anyone.”", [V("siri", 8), FD("rm_i3"), F("siri_lachs_nein"),
              FAKT("siri", "Siri's manager signed a salmon farm deal in her name, against the farms her father fights. Duc told her to refuse and to ring her father. She has not told anyone else.")],
             zeile=G("siri", "Ring him. After two years. [sniff] What do I even say? Sorry, I'm good at that. …Okay. Stay near the phone with me?", "love")),
           O("“It isn't my call. But whatever you pick, you'll pick it, and I'll be here.”", [V("siri", 8), B("siri", 3), FD("rm_i3"),
              FAKT("siri", "Siri's manager signed a salmon farm deal in her name, against the farms her father fights. Duc told her the choice is hers and that he will stand by her.")],
             zeile=G("siri", "Nobody's ever told me that. [sigh] It's horrible. Thank you. It's really horrible.", "gratitude")),
           O("“Post it. Get paid, then get out, and tell him why later.”", [V("siri", 3), FD("rm_i3"),
              FAKT("siri", "Siri's manager signed a salmon farm deal in her name, against the farms her father fights. Duc advised her to post it and explain later.")],
             zeile=G("siri", "Yes. That's the clever way. [sniff] That's what they'd all say, isn't it?", "disappointment"))],
          "Dad's Sweater"),
    ABEND("rm_i4", "wholesome", "My Own Words", W_L((15, 21), "nacht", *AB("siri", 5, 5), FREI_S, {"flag_seit": ["rm_i3", 2]}, N("rm_i4"), spaet=True), "foredeck", "siri",
          "The foredeck, late. Siri is wearing her father's jumper, no make-up, her hair tied back. There's no ring light and no golden "
          "hour. She hands you her phone before you can sit down. There's a picture of a knitted star on the screen, and under it, typed "
          "and deleted and typed again, a few words. For the first time in six years, they are hers.",
          [G("siri", "Read it. Out loud, please, I can't. [clear throat] “My dad knits badly. One star for every winter evening. I never wore it. I'm wearing it.”", "nervousness"),
           G("siri", "That's all. There's no hashtag, and my manager would have a heart attack. [sniff] I rang my father. He didn't pick up. I'm posting it anyway, to two point eight million people, and maybe one of them is him.", "sadness"),
           G("siri", "Nobody has read a single thing I wrote since I was nineteen. [sigh] So tell me, and don't be nice. Is it any good?", "fear")],
          [O("“It's the best thing I've read on this boat. Post it.”",
             [V("siri", 8), B("siri", 8), F("rm_i4"), F("siri_zusammen"),
              FAKT("siri", "Siri wrote her first caption in six years, about her father's jumper, and posted it. Duc read it first and told her it was good. They are together now, in private.")],
             zeile=G("siri", "Okay. Okay, there. It's gone. [gasp] Oh no. …Oh. Sorry, I'm shaking. Can you hold on to me? Not for a picture.", "love")),
           O("“The third line is too long. Otherwise, yes.”",
             [V("siri", 10), B("siri", 6), F("rm_i4"), F("siri_zusammen"),
              FAKT("siri", "Siri wrote her first caption in six years, about her father's jumper, and posted it after Duc gave her an honest note on it. They are together now, in private.")],
             zeile=G("siri", "You actually read it. You told me something's wrong with it. [laugh] That's the best thing anyone's ever said to me! Which word?", "love")),
           O("“It's yours, Siri. You don't need me to tell you.”",
             [V("siri", 8), F("rm_i4"), F("siri_offen"),
              FAKT("siri", "Siri wrote her first caption in six years, about her father's jumper. Duc told her she doesn't need his opinion on it.")],
             zeile=G("siri", "No. I don't, do I? [sniff] That's new. …Stay anyway? Only if you like.", "caring"))],
          "Dad's Sweater"),
]

LAGE_ECHO.update({
    "lola": ("galley", "Galley", "Early morning in the galley, and nobody else is up yet. Lola is flipping something, barefoot, and pretends "
             "she hasn't heard you come in."),
    "alva": ("alvas_bar", "alva_standard", "Early morning at Alva's bar. You've come over for coffee and nobody else is here yet. She is taking "
             "the chairs down from the tables."),
    "siri": ("foredeck", "Dad's Sweater", "Early morning on the foredeck, and nobody else is up yet. Siri is holding a coffee she's forgotten about, "
             "and she smiles when she sees you, with the left side first."),
    "jana": ("foredeck", "jana_deck_a", "Early morning on deck, and nobody else is up yet. Jana is coiling a rope that is already coiled. When she "
             "sees you she pulls her ponytail tighter."),
})

ECHOS_NEU = [
    ECHO("lola_nacht1", "lola", "A Heart, Mostly", NEU("lola", "intimate", "==1"),
         "Morning, Boss. That one on your plate's meant to be a heart. [chuckle] It isn't a heart, it's a pancake that went wrong, and I'm not saying anything about last night. Mostly the pancake.", "love",
         [("Eats it first, before anything else.", "You ate the heart first. [laugh] I'm going to have to sit down.", "love"), ("“Mostly?”", "Mostly. [chuckle] Don't push your luck, I've got a hot pan.", "desire")],
         [AUF("lola", *GROSS)]),
    ECHO("lola_nacht2", "lola", "Burnt Toast", NEU("lola", "intimate", ">=2"),
         "I burnt the toast again this morning, because I was thinking about last night, mate. [laugh] That's on you. You owe me toast.", "joy",
         [("“I'll take it burnt.”", "Good, because it's all there is. [chuckle] Mostly the butter.", "love"), ("Makes her some toast.", "Oh, you're doing it wrong. [laugh] Keep going, it's great.", "joy")],
         [AUF("lola", *GROSS)]),
    ECHO("lola_kuss", "lola", "Don't Tell Anyone", [{"moment_offen": ["lola", ["kiss", "naehe", "naehe_weit"]]}],
         "Don't tell anyone I told you, but somebody kissed me. [chuckle] Nice bloke, bad timing, he's standing in my galley right now.", "love",
         [("“Sounds dangerous.”", "He is. [laugh] He eats everything I make.", "desire"), ("Takes a spoon and tastes what's in the pan.", None, None)],
         [AUF("lola", *GROSS)]),
    ECHO("lola_versetzt", "lola", "Two Plates", [{"moment_offen": ["lola", ["stood_up"]]}],
         "I kept a plate for you last night, Boss, and you didn't come. [sniff] No worries. Jana ate it. Mostly Jana.", "sadness",
         [("“I'm sorry, Lola. I should have come.”", "Yeah, you should've. [sigh] It was good, too. …Sit, I'll do you an egg.", "caring"), ("“Something came up.”", "Yep. Sweet as. [sniff] Toast's on the side.", "sadness")],
         [AUF("lola", "stood_up")]),
    ECHO("lola_verletzt", "lola", "Heaps Busy", [{"flag": "verletzt_lola"}],
         "Heard you've been heaps busy, mate. [sniff] Don't tell anyone I told you, but that one got to me. Mostly – no. All of it got to me.", "sadness",
         [("Stays and doesn't explain.", None, None), ("“Lola, let me explain.”", "Nah. [sigh] Eat your breakfast, Boss.", "sadness")]),
    ECHO("lola_erster", "lola", "The Good Stool", [{"flag_seit": ["rm_o4", 1]}, {"flag": "lola_zusammen"}],
         "Morning, first guest. [laugh] I went down to the hut at six and I nailed the leg on that stool, so it's yours now, officially.", "love",
         [("“Mine?”", "Yours. [chuckle] And I finished that sentence too, did you hear?", "love"), ("Salutes her with his coffee.", None, None)]),
    ECHO("alva_nacht1", "alva", "On the Board", NEU("alva", "intimate", "==1"),
         "Good morning, o figliolu. Coffee's on the house, and only this once. [chuckle] Nobody saw you leave last night. Well, Mina did. Which means nobody yet.", "amusement",
         [("“Should I be worried?”", "Always. [chuckle] Drink up, and go out by the back this time.", "desire"), ("Leaves money on the bar anyway.", "Put that away. [sigh] You'll spoil me.", "love")],
         [AUF("alva", *GROSS)]),
    ECHO("alva_nacht2", "alva", "Regular", NEU("alva", "intimate", ">=2"),
         "Twice now. [chuckle] Careful, or I'll have to put you on Papa's board as a regular, and then the whole village can read it.", "desire",
         [("“What would it say?”", "Nothing I could write in chalk, o figliolu. [chuckle] Not with my father watching.", "desire"), ("“Rub it out, then.”", None, None)],
         [AUF("alva", *GROSS)]),
    ECHO("alva_kuss", "alva", "Costs Extra", [{"moment_offen": ["alva", ["kiss", "naehe", "naehe_weit"]]}],
         "I told you bold costs extra. [chuckle] That's on your tab, and I'm the only one who keeps it.", "amusement",
         [("“What do I owe?”", "I'll let you know. [chuckle] Alva remembers.", "desire"), ("“Put it on the board.”", "Not a chance. [laugh] Nobody's mine, remember?", "amusement")],
         [AUF("alva", *GROSS)]),
    ECHO("alva_versetzt", "alva", "Closed Early", [{"moment_offen": ["alva", ["stood_up"]]}],
         "I closed early last night, for you. [sigh] I don't close early. Three fishermen know it, and by noon the whole harbour will.", "disappointment",
         [("“I'm sorry, Alva. I should have come.”", "Yes. [sigh] Alva remembers who helps her, o figliolu. And who doesn't.", "sadness"), ("“Something came up.”", "It always does. [chuckle] Coffee's two euros today.", "annoyance")],
         [AUF("alva", "stood_up")]),
    ECHO("alva_verletzt", "alva", "Everybody's Welcome", [{"flag": "verletzt_alva"}],
         "I hear everything in this bar, you know that. [sigh] Everybody's welcome here, o figliolu. Nobody's mine. I just forgot for a moment.", "sadness",
         [("Stays until she has taken down the last chair.", None, None), ("“Alva, let me explain.”", "Don't. [chuckle] I've heard it, from better liars.", "annoyance")]),
    ECHO("alva_kreide", "alva", "Four O'Clock", [{"flag_seit": ["rm_a4", 1]}, {"flag": "alva_zusammen"}],
         "It's four in the afternoon somewhere. [chuckle] I've made two coffees. Don't read anything into it, it's only that the board says so.", "love",
         [("Sits down and drinks it.", None, None), ("“Only you and me know about that line.”", "And my father. [sniff] He'd have wiped it off.", "love")]),
    ECHO("siri_nacht1", "siri", "No Picture", NEU("siri", "intimate", "==1"),
         "I didn't take a picture this morning. I always do. [sniff] I had the phone in my hand, and then I just looked at the sea. Sorry, is that weird to say?", "love",
         [("“How was the sea?”", "Grey. It wasn't very good. [laugh] It was wonderful.", "joy"), ("Stands next to her and looks at it too.", None, None)],
         [AUF("siri", *GROSS)]),
    ECHO("siri_nacht2", "siri", "Sorry", NEU("siri", "intimate", ">=2"),
         "I didn't say sorry once last night. Did you notice? [chuckle] Sorry. That doesn't count, it's morning.", "joy",
         [("“I noticed.”", "Oh. [laugh] Okay. Good. I'll try to do it again.", "love"), ("“Don't be sorry.”", "I'm not. [chuckle] I'm really not. That's new.", "love")],
         [AUF("siri", *GROSS)]),
    ECHO("siri_kuss", "siri", "Off Camera", [{"moment_offen": ["siri", ["kiss", "naehe", "naehe_weit"]]}],
         "Nobody filmed that. [sigh] I keep thinking of it. Something happened to me, and there's no proof at all.", "love",
         [("“I'll sign a statement.”", "You're terrible. [laugh] Two copies, please.", "joy"), ("Nods, and says nothing.", None, None)],
         [AUF("siri", *GROSS)]),
    ECHO("siri_nein", "siri", "Another Night", [{"flag": "rm_i_nein"}],
         "You said another night, about the jumper. [clear throat] I wasn't sad. I only wanted to tell you I wasn't sad.", "caring",
         [("“I know.”", None, None), ("“It still counts as another night.”", "Yes. [chuckle] I've put it in my diary. I don't have a diary.", "joy")]),
    ECHO("siri_versetzt", "siri", "Golden Hour", [{"moment_offen": ["siri", ["stood_up"]]}],
         "I waited on the foredeck last night. It's fine. [sniff] I'm very good at waiting for people, it's most of my job. Sorry.", "sadness",
         [("“I'm sorry, Siri. Don't say sorry to me.”", "Okay. Sorry. [sniff] No, okay.", "caring"), ("“Something came up.”", "Of course. [sigh] Golden hour, yes.", "sadness")],
         [AUF("siri", "stood_up")]),
    ECHO("siri_verletzt", "siri", "Everyone Sees", [{"flag": "verletzt_siri"}],
         "I heard about you and someone else. It's fine. [sniff] Three million people have opinions about me, so I know how quickly it gets around.", "sadness",
         [("Stays next to her and says nothing.", None, None), ("“Siri, let me explain.”", "You don't have to. [sigh] I've got a very good sad face. I'll be fine.", "sadness")]),
    ECHO("siri_geschrieben", "siri", "Two Point Eight Million", [{"flag_seit": ["rm_i4", 1]}, {"flag": "siri_zusammen"}],
         "My manager has rung eleven times. [laugh] And one message from an island with one ferry. It's a heart. It's only a heart, and it's from my mum, but she says he read it.", "love",
         [("“He read it.”", "He read it. [sniff] Oh, I'm not going to cry on deck, there's a seagull watching.", "love"), ("Puts his arm around her, jumper and all.", None, None)]),
    ECHO("jana_nacht", "jana", "One Night", [{"moment_offen": ["jana", list(GROSS)]}],
         "Good morning, Sir. Sorry. I said one night, and it was one night, and I'm completely fine. [clear throat] You don't have to be nice about it. Na geh, you're being nice about it.", "embarrassment",
         [("“Good morning, Jana. Your rope's very tidy.”", "Ja. Thanks. [chuckle] It's a very tidy rope, Sir.", "gratitude"), ("“Are you all right?”", "Yes. Ja. [sigh] Thank you for asking. Nobody asks. Sorry.", "caring")],
         [AUF("jana", *GROSS)]),
]
_MEGAN = WANN((5, 6), ["fruehstueck"], bed={"alle": [{"moment_offen": ["megan", list(GROSS)]}, {"nicht": {"flag": "rm_e_megan_nacht"}}]}, pflicht=True)
_MEGAN["leiter"] = True
_MEGAN["akt2"] = [8, 35]
ECHOS_NEU.append(E("rm_e_megan_nacht", "handy", "wholesome", "On the Record", _MEGAN, ORT_DUC,
                   {"anrufer": "megan", "anrufer_ort": "megan_office"},
                   "Your phone rings before breakfast, from the private number. Megan, in her office above Port Hercule, dressed for a board meeting, as if the other night had happened to someone else.",
                   [G("megan", "Good morning, Duc. I said that night was off the record, and so it is. [clear throat] I'm only ringing to say I have read your weekly report, and that it's the second-best thing you've done this week.", "amusement")],
                   [O("“Only the second?”", [V("megan", 2), F("rm_e_megan_nacht"), AUF("megan", *GROSS)],
                      zeile=G("megan", "Don't push it, First Officer. [chuckle] How... delightful. Goodbye.", "desire")),
                    O("“Thank you for the call.”", [V("megan", 2), F("rm_e_megan_nacht"), AUF("megan", *GROSS)])],
                   sets={"megan": "Boardroom"}))

for _e in ECHOS_NEU:                  # eine Antwort ohne Zeile bleibt still
    for _o in _e["optionen"]:
        if _o.get("zeile") is None:
            _o.pop("zeile", None)
ECHOS += ECHOS_NEU

# ------------------------------------------------------------------ Alte Events reagieren auf die erste Nacht (Hades-Prinzip)
# Zeile am Ende eines alten Flirt-Events, nur nach einer gemeinsamen Nacht. Nur Events unter vier Augen (E-060).
NACH_NACHT = lambda pid: {"moment_zahl": [pid, "intimate", ">=", 1]}
ZUSATZ = {
    "fl_rosi_vespa": ("rosi", "and yes, I remember what I said about holding on. [chuckle] the other night you held on just fine 😏", "desire"),
    "hy_rosi_foto": ("rosi", "…Officer, you've seen more than that anyway. [gasp] So why am I this red?", "embarrassment"),
    "fl_rosi_schicksal": ("rosi", "I don't know why I'm embarrassed. [sigh] We've been a lot closer than this, and you know it.", "desire"),
    "hy_lea_plankton": ("lea", "You've been down here with me before, so you know how this goes. [chuckle] I'll talk, and you'll stay.", "love"),
    "fl_lea_fakt": ("lea", "also, fact: you snore. very small snore. [chuckle] like a sea otter 🦦 goodnight for real", "love"),
    "hy_chiara_jonas": ("chiara", "You're the only one I'm ringing, Duc. [sigh] You've seen me without my lists, so you may as well see this.", "caring"),
    "fl_chiara_tee": ("chiara", "and yes, I know you know how I take mine now. [chuckle] don't get clever 🍋", "amusement"),
    "fl_chiara_zehn": ("chiara", "And no, the other night doesn't count. [chuckle] That one has its own number, and you're not getting it.", "desire"),
    "hy_sophia_0213": ("sophia", "You already know how this one ends, darling. [chuckle] You were there. I'm only writing it down.", "desire"),
    "fl_sophia_ungeprobt": ("sophia", "You've heard that laugh before, of course, in the dark. [sigh] I'd rather you didn't mention it.", "love"),
    "fl_lola_haengematte": ("lola", "and you know how it flips, mate, we've done this. [laugh] mostly the flipping 😇", "desire"),
    "hy_lola_koster": ("lola", "And don't look at me like that, Boss. [laugh] I know what that mouth's good for, that's why I rang.", "desire"),
    "fl_lola_mehl": ("lola", "You've got flour on you again. [chuckle] Last time you walked back to your cabin like that, and I laughed for an hour.", "amusement"),
    "fl_alva_tuer": ("alva", "you know the way round the back now, o figliolu. [chuckle] I'm not saying anything 🚪", "desire"),
    "hy_alva_sevilla": ("alva", "You've seen this bar with the chairs up and me with my shoes off, so don't ask me if I'm fine. [sigh] Just talk.", "caring"),
    "hy_siri_ungeschminkt": ("siri", "You've seen this face with a lot less on it. [sniff] I don't know why a phone still makes me nervous. Sorry.", "love"),
    "fl_siri_schulter": ("siri", "I've slept on you before, you know. [sigh] It's still my favourite place on this boat. Sorry. I'm not sorry.", "love"),
}
# Erste Annaeherungen passen nach einer gemeinsamen Nacht nicht mehr
NUR_DAVOR = {"fl_siri_date": "siri", "fl_siri_blick": "siri"}


def zusatz(events):
    """Von ereignisse_basis.bauen() nach dem Sammeln aufgerufen."""
    idx = {e["id"]: e for e in events}
    for eid, (pid, text, gefuehl) in ZUSATZ.items():
        idx[eid]["zeilen"].append(dict(G(pid, text, gefuehl), gruppe="nach_nacht", wenn=NACH_NACHT(pid)))
    for eid, pid in NUR_DAVOR.items():
        w = idx[eid]["wann"]
        w["bedingung"] = {"alle": [{"nicht": NACH_NACHT(pid)}] + ([w["bedingung"]] if w.get("bedingung") else [])}

# Echos stehen vorn: Am Morgen danach geht das Echo der naechsten Szene vor
EVENTS = ECHOS + ROSI + LEA + CHIARA + SOPHIA + LOLA + ALVA + SIRI
