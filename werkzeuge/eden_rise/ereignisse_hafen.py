# -*- coding: utf-8 -*-
"""Hafenkampf · Tag 2 nachmittags (25.10.2026, docs/wiki/welt/drehbuch_hafenkampf.md, E-044, E-041, E-020).

Kette am Nachmittag von Tag 2, direkt nach Maxwells erster Lektion (mx_tutorial, Flag tutorial_maxwell):
Hilfe holen -> Welle 1 Ratten -> Elsa -> Welle 2 Hunde -> Alva -> Welle 3 Keiler -> Petru -> Ziege + Casanova.
Jede Welle ist EIN Kampf gegen das Alpha-Tier, das Rudel greift als Sonderangriff mit an (Variante A, Duc 25.10.).
Die Tiere fliehen am Ende in die Macchia, keins stirbt. Niederlage: dieselbe Welle beginnt neu (Begegnung
"neustart_bei_niederlage", eden.py), gewonnen werden muss sie. Die Wellen-Flags setzt der Kampf (kaempfe_eden_rise.py).

Alle Glieder sind Pflicht-Events mit WANN(prolog=True): sie schliessen direkt aneinander an (wie Tag 0).
Das Dorf lernt Duc hier kennen - Elsa, Alva, Petru und Casanova bekommen Kennenlern-Chips wie an Tag 0 (E-018):
V Vertrauen +1 Stufe · B Begehren +1 Stufe (Alva) bzw. H Humor +Rueckhalt · - nichts · F Fettnaepfchen.
Jede Wahl setzt dorf_<id>_<chip>."""
from ereignisse_basis import *  # noqa: F401,F403

ORT = "village_harbour"
STUFE = 8                                    # Punkte je Vertrauens-/Begehrensstufe (kern/zustand.PUNKTE_JE_STUFE)


def P1(handelnd, *betroffen):
    return {"handelnd": handelnd, "betroffen": [{"id": b[0], "ton": b[1], "was": b[2]} for b in betroffen]}


def WH(flag):
    """Glied der Hafen-Kette: Tag 2 nachmittags, nach dem vorigen Glied (Flag)."""
    return WANN((2, 2), ["nachmittag"], bed={"flag": flag}, pflicht=True, prolog=True)


def chips(pid, v, b, n, f, romanze=False, danach=()):
    """Vier Kennenlern-Chips; danach = Folgen fuer jede Wahl (z. B. die naechste Welle)."""
    flag = lambda art: F("dorf_%s_%s" % (pid, art))
    extra = list(danach)
    return [O(v[0], [V(pid, STUFE), flag("v")] + extra, zeile=v[1]),
            O(b[0], [B(pid, STUFE) if romanze else R(5), flag("b" if romanze else "h")] + extra, zeile=b[1]),
            O(n[0], [flag("n")] + extra, zeile=n[1]),
            O(f[0], [V(pid, -STUFE), flag("f")] + extra, zeile=f[1])]


KAMPF = lambda bid: {"kampf": bid}


def WH_ROSI(chip):
    """Rosi's throw: after "Getting Help", one version per Tag-0 chip; "n" is the fallback for every other case."""
    andere = [{"flag": "tag0_rosi_" + c} for c in "vbf"]
    if chip == "n":
        bed = {"alle": [{"flag": "hafen_ankunft"}, {"nicht": {"eine": andere}}]}
    else:
        bed = {"alle": [{"flag": "hafen_ankunft"}, {"flag": "tag0_rosi_" + chip}]}
    return WANN((2, 2), ["nachmittag"], bed=bed, pflicht=True, prolog=True)


ROSI_WURF = {
    "v": ("Rosi jumps off the tender behind you, soot still on her cheek from the workshop fire, a baseball bat over "
          "her shoulder. She throws it to you without a word. *He was the only one who knew what an inverter was. If "
          "I give it to anyone, it's him.*",
          ("Officer, you can't go out there with your bare hands. The workshop's gone, the whole thing burned, and "
           "this is the only thing I got out.", "caring"),
          ("His name's Terremoto. I put a weight in the barrel, so when you hit something, it really feels like an "
           "earthquake. Go on, I'm right behind you.", "pride")),
    "b": ("Rosi whistles through her fingers. When you turn round, the bat is already flying at you. *Don't grin. "
          "Don't you dare grin. Now I'm grinning.*",
          ("Hey, Officer! Since you like looking at engineers so much, here's something an engineer made for you. "
           "Catch!", "amusement"),
          ("That's Terremoto. There's a weighted core inside, I built it myself, so try not to drop it. And stop "
           "looking at me, the rats are over there!", "embarrassment")),
    "n": ("Rosi pushes through the people on the quay and tosses you a baseball bat without asking. *Let's see what "
          "he can do with it.*",
          ("You'll need something to fight with, Officer. That's all I could save from the workshop.", "neutral"),
          ("It's called Terremoto, like the earthquake. There's a weight in the barrel, so just swing it and let it "
           "do the work. Leave the thinking to me, okay?", "optimism")),
    "f": ("Rosi throws you a baseball bat, a little too hard, and it almost slips through your hands. *The only thing "
          "I got out of the fire, and of all people, he gets it.* Then her voice drops.",
          ("Here you go, Officer. Compliments of the mechanic.", "annoyance"),
          ("His name's Terremoto. Papa would love him. So please don't make me regret this, alright?", "sadness")),
}

# ------------------------------------------------------------------ Hafenkampf als Ortskette (Duc 26.10.2026)
# "The Day the Animals Came": jede Welle rettet eine Person (Ratten -> Petru, Hunde -> Alva, Keiler -> Casanova), danach
# die Nachbetrachtung mit allen am Fass, dann die Ziege. Der Auftakt (hk_hilfe) bleibt das Pflicht-Event von Tag 2 und
# startet die Kette (Folge "ort_start"); alle weiteren Frames sind art "ort" im Expeditions-Bildschirm. Kein Rasten, kein
# Rueckweg (sperre), Niederlage: dieselbe Welle neu (E-041, neustart_bei_niederlage in kaempfe_eden_rise.py).
WEITER = lambda ziel: {"weiter": ziel}
WEG = lambda i: "hk_welle%d" % i
BILD_KAI, BILD_BAR, BILD_TREPPE, BILD_ABEND = "hafen_kai_chaos", "hafen_bar_tuer", "piazza_treppe", "hafen_abend"


def HF(id, bild, titel, lage, zeilen, optionen, personen=None, sets=None, ton="ernst"):
    """Ein Frame der Hafenkette (Tag 2, nie gezogen, ohne Rueckweg)."""
    e = E(id, "ort", ton, titel, WANN((2, 2)), bild, personen or {}, lage, zeilen, optionen, sets)
    e["sperre"] = True
    return e


ROSI_ZIEL = [{"wenn": {"flag": "tag0_rosi_" + c}, "id": "hk_rosi_" + c} for c in "vbf"] + [{"id": "hk_rosi_n"}]

# Rosi hilft einmal, nach der ersten Niederlage in einer Welle (Duc 30.10.2026, Spieltest): Hinweis auf die Spezialangriffe,
# 3 Pflaster, Wasser- und Schockgranate. Die Kombi erklaert Kurzschluss, den die Agenten in den Bergen spaeter gegen Duc nutzen.
TIPP = {"ratten": BILD_KAI, "hunde": BILD_BAR, "keiler": BILD_TREPPE}
TIPP_FOLGEN = [F("hafen_hilfe_bekommen"), {"item": "plaster", "n": 3}, {"item": "grenade_water", "n": 1}, {"item": "grenade_shock", "n": 1}]

EVENTS = [
    # ------------------------------------------------------------------ Auftakt (Pflicht, startet die Kette)
    E("hk_hilfe", "ort", "ernst", "Cala d'Orsu Is Screaming", WH("tutorial_maxwell"), BILD_KAI,
      P1("toto", ("lea", "?", "steers the tender")),
      "The tender hasn't even touched the quay when you hear it. Not one scream, but a whole village of them, and "
      "under the screaming a sound like rain on tin. Rats. Hundreds of them, pouring over the fish crates.",
      [Z("toto", "Madonna. Comandante, that is not a welcome committee.", "fear"),
       Z("lea", "They're not running from anything. They're running at everything. That's not how rats work, I "
                "promise you that's not how rats work.", "nervousness")],
      [O("Looks around for something to fight with.", [F("hafen_ankunft"), {"ort_start": "hafen"}, WEITER(ROSI_ZIEL)],
         zeile=Z("lea", "Go! I'll keep the engine running!", "nervousness")),
       O("“Lesson one, Mr. Maximum.” Takes a deep breath.", [W("moral", 1), F("hafen_ankunft"), {"ort_start": "hafen"},
                                                              WEITER(ROSI_ZIEL)],
         zeile=Z("toto", "Two to one on the Comandante. Today I'm feeling generous.", "amusement"))]),
] + [
    # ------------------------------------------------------------------ Rosi wirft Terremoto (E-049, E-052) -> Welle 1
    HF("hk_rosi_" + chip, BILD_KAI, "Wave 1 · Rats on the Quay", lage, [Z("rosi", z1, g1), Z("rosi", z2, g2)],
       [O("Catches it and runs at the rats.", [F("waffe_bat"), KAMPF("hafen_ratten"), WEITER("hk_petru")]),
        O("“Thanks, Rosi.” Then charges.", [F("waffe_bat"), V("rosi", 2), KAMPF("hafen_ratten"), WEITER("hk_petru")])],
       personen=P1("rosi", ("toto", "+", "whistles"), ("lea", "?", "keeps the engine running")),
       sets={"rosi": "Engine Room"}, ton="wholesome" if chip in "vb" else "ernst")
    for chip, (lage, (z1, g1), (z2, g2)) in ROSI_WURF.items()
] + [
    # ------------------------------------------------------------------ Rosis Hilfe nach der ersten Niederlage (eden.py, hilfe_event)
    HF("hk_tipp_" + welle, bild, "Rosi's Advice",
       "Rosi has caught up with you. She looks you over the way she looks at a bad weld, then she starts pulling things "
       "out of her tool bag.",
       [Z("rosi", "You're only swinging at them, Officer. You have special moves, so use them. That's what they're for.", "annoyance"),
        Z("rosi", "Take these three plasters. They heal a little, and using one doesn't cost you your turn.", "neutral"),
        Z("rosi", "These two grenades are mine, so be nice to them. Throw the water one first, so the animal is wet. "
                  "Then throw the shock one at the same animal.", "neutral"),
        Z("rosi", "Wet plus shock makes a short circuit. It hurts, and the animal loses its next turn. That's physics, not luck.", "amusement")],
       [O("Takes everything. “Thanks, Rosi.”", list(TIPP_FOLGEN), zeile=Z("rosi", "Don't thank me. Just win this time.", "neutral")),
        O("“I had it under control.”", list(TIPP_FOLGEN), zeile=Z("rosi", "You were lying on the ground, Officer. Take the grenades.", "amusement"))],
       personen=P1("rosi"), sets={"rosi": "Engine Room"})
    for welle, bild in TIPP.items()
] + [
    # ------------------------------------------------------------------ Rettung Petru (nach Welle 1)
    HF("hk_petru", BILD_KAI, "The Blue Boat",
       "The last rats spill into the alleys. On the blue boat an old man is standing on his workbench with a boat hook "
       "in both hands. He has been holding the gangway for twenty minutes. Not a single one got aboard.",
       [Z("petru", "Hm.", "neutral"),
        Z("petru", "My wife painted that boat. They were not getting on it.", "pride"),
        Z("petru", "Alva's bar is up the lane. Listen. Go. I will hold the quay.", "neutral")],
       chips("petru",
             ("Holds out a hand from the quay wall. “Come down. I've got you.”",
              Z("petru", "…Hm. Your hand is steady. Good.", "approval")),
             ("“Twenty minutes with a boat hook? You should be on my crew.”",
              Z("petru", "I was on crews before your father was born.", "pride")),
             ("Just nods and moves on.", Z("petru", "Hm.", "approval")),
             ("“You could have just run, you know.”", Z("petru", "And you could have stayed on your yacht.", "disapproval")),
             danach=[F("dorf_petru_gesehen"), WEITER(WEG(2))]),
       personen=P1("petru", ("toto", "+", "catches his breath")), sets={"petru": "Standard"}),
    HF(WEG(2), BILD_BAR, "Wave 2 · The Dogs",
       "Barking up the lane, and a door being hit, again and again. The pack has the bar surrounded. Through the gap "
       "in the shutters you see a woman with a broom handle and a bottle of grappa, and she looks like she's choosing "
       "which one to use first.",
       [],
       [O("Puts himself between the dogs and the door.", [KAMPF("hafen_hunde"), WEITER("hk_alva")])]),
    # ------------------------------------------------------------------ Rettung Alva (nach Welle 2)
    HF("hk_alva", BILD_BAR, "Last Orders",
       "The last dog slinks off down the lane. The door opens a crack, then all the way. She looks at the claw marks in "
       "the wood. Then at you.",
       [Z("alva", "Alva. That's my bar you just defended. So don't expect me to thank you properly. Just come back "
                  "when there's music.", "neutral"),
        Z("alva", "Everybody's welcome here, o figliolu. Even the ones who arrive by yacht.", "amusement"),
        Z("alva", "Hear that trumpet up the hill? That's the mayor. …Go on. She'll never forgive me if you're late.", "sadness")],
       chips("alva",
             ("Picks up her bar stool and sets it back at the counter. “Open tomorrow?”",
              Z("alva", "For you, I'll open tonight.", "joy")),
             ("“I fought a pack of dogs for you. I think that's worth a drink.”",
              Z("alva", "Careful. I remember who helps me. And who flirts with me.", "amusement")),
             ("“Are you hurt?”", Z("alva", "Only my pride. And the door.", "neutral")),
             ("“Grappa as a weapon? Bold.”", Z("alva", "It's the cheap one. I'm not an animal.", "annoyance")),
             romanze=True, danach=[WEITER(WEG(3))]),
       personen=P1("alva"), sets={"alva": "alva_standard"}, ton="wholesome"),
    HF(WEG(3), BILD_TREPPE, "Wave 3 · The Boar",
       "Up the hill a church bell starts ringing, wrong, far too fast. Then a trumpet. Then something that sounds like a "
       "confetti cannon going off in fear. On the piazza a boar the size of a small car is pacing at the foot of the town "
       "hall steps. At the top, in a red dress, a woman holds the confetti cannon like a rifle. The boar is covered in "
       "glitter and very angry about it.",
       [],
       [O("Walks out into the middle of the piazza. “Over here!”", [KAMPF("hafen_keiler"), WEITER("hk_casanova")])]),
    # ------------------------------------------------------------------ Rettung Casanova (nach Welle 3)
    HF("hk_casanova", BILD_TREPPE, "The Mayor Holds the Stairs",
       "The boar snorts, turns, and trots back into the macchia as if it had an appointment. At the top of the stairs the "
       "woman lowers the confetti cannon for the first time.",
       [Z("casanova", "Monsieur! You arrive exactly at the climax. That is either destiny or excellent timing, and I "
                      "accept both.", "joy"),
        Z("casanova", "…My father built these steps. I wasn't going to let a pig have them.", "sadness")],
       chips("casanova",
             ("Climbs the stairs and takes the confetti cannon from her. “I think you've won, Madame.”",
              Z("casanova", "We won, Monsieur. Write it down. History is watching.", "pride")),
             ("“You shot a boar with glitter.”",
              Z("casanova", "And it will never look serious again. That's strategy.", "amusement")),
             ("“Is anyone hurt?”", Z("casanova", "Only the festa decorations. A tragedy, but not a fatal one.", "neutral")),
             ("“Next time, maybe hide?”", Z("casanova", "A mayor does not hide, Monsieur. A mayor poses.", "disapproval")),
             danach=[WEITER("hk_abend")]),
       personen=P1("casanova"), sets={"casanova": "Standard"}, ton="witzig"),
    # ------------------------------------------------------------------ Nachbetrachtung (alle zusammen)
    HF("hk_abend", BILD_ABEND, "After the Storm",
       "The sun goes down over a harbour that looks like a party nobody enjoyed. Someone has rolled out a barrel. Petru "
       "brings bread, Alva brings the cheap grappa. Elsa arrives last, in uniform, with her notebook already open. Alva "
       "and the mayor end up standing at the same barrel. Neither of them says anything. Then Casanova pushes her glass a "
       "few centimetres towards Alva, and Alva pours without looking.",
       [Z("elsa", "Lieutenant Ferrandi, coast guard. I'll need statements from everyone. TOTÒ, I can see you behind that "
                  "crate.", "annoyance"),
        Z("toto", "I am also a victim, Lieutenant!", "fear"),
        Z("petru", "He fights like a sailor. Not like a tourist.", "approval"),
        Z("alva", "First round's on the house. Second round you pay. Third round, we'll see.", "amusement"),
        Z("casanova", "People of Cala d'Orsu! Tonight a stranger from a broken yacht defended our quay, our bar and our "
                      "town hall. Tomorrow we clean up.", "pride"),
        Z("casanova", "And the day after tomorrow, Monsieur, you come to my office. There is something I need to ask "
                      "you, and it is not a thing one asks over grappa.", "nervousness")],
       chips("elsa",
             ("“Rats, dogs, a boar. Nobody hurt. The yacht's still dark.”",
              Z("elsa", "…Finally, someone who can count. Thank you.", "approval")),
             ("“Statement: I'm a consultant who owns a baseball bat now.”",
              Z("elsa", "Noted. Badly noted. Unofficially? Thank you.", "amusement")),
             ("Raises his glass to her and says nothing.", Z("elsa", "Officially, you were never here.", "neutral")),
             ("“Where was the coast guard an hour ago?”",
              Z("elsa", "On the other side of the bay with one boat and two men, First Officer. Where were you?",
                "anger")),
             danach=[WEITER("hk_pascal")]),
       personen={"handelnd": "casanova", "betroffen": [{"id": b, "ton": "+", "was": ""} for b in ("elsa", "alva", "petru")]},
       sets={"casanova": "Standard", "alva": "alva_standard", "petru": "Standard", "elsa": "Standard"}, ton="wholesome"),
    # ------------------------------------------------------------------ Die Ziege (Faden zum Kloster)
    HF("hk_ziege", BILD_ABEND, "Something That Blinks",
       "You're walking back to the tender when something stops you. On the stone wall above the quay stands a goat, "
       "perfectly calm, as if the day had nothing to do with her. Around her neck is a collar, and on the collar a small "
       "red light is blinking, slowly, like a heartbeat. Then she turns and climbs the wall, and the macchia swallows "
       "her whole. For a moment Casanova's eyes follow her up to the dark line of the mountains.",
       [],
       [O("Watches the mountains for a long moment. Then goes back to the boat.", [F("kloster_faden")])],
       ton="ernst"),
]
