# -*- coding: utf-8 -*-
"""Funken und kleine Begehren-Events (Duc 27.10.2026, Brain Trust nach der Beziehungs-Simulation).

Befund: Begehren-Events gibt es genug, aber sie kommen zufaellig - wer sich auf eine Frau konzentriert, bekommt nicht
mehr Events mit ihr. Rosi, Lea und Siri blieben in der Simulation bei 35 Punkten haengen (Deckel), ein einziges Event
fehlte zu Stufe 3. Deshalb:

- FUNKEN: je Frau ohne Abend (Chiara, Sophia, Lea, Rosi, Siri) ein privater Moment als Art "abend" (Gewicht 8 =
  Vorrang, sobald die Bedingung gilt; ohne Intim-Szene kostet er keine Zeit). Bedingung: Tag 4-6, Vertrauen 3,
  Begehren 2. Die tragende Antwort gibt +14 Begehren (reicht aus Stufe 2 fuer Stufe 3), die freundliche nur Vertrauen,
  das Nein bricht nichts. Jede Antwort setzt <pid>_funke, damit der Funke nicht wiederkommt.
  Leiter aus dem Wiki: Chiara "gefragt werden" (nicht die Lernabende - die haengen an ihrem Geheimnis), Sophia "die
  Show rutscht", Lea klein (ihr Bogen ist Akt 2), Rosi "neben ihm arbeiten", Siri erst nach siri_frei.
- KLEINE EVENTS: je zwei fuer Rosi, Sophia und Siri (die wenigsten Begehren-Events am Tag). Siri vor siri_frei nur
  wholesome mit +2 (vergeben), danach frech.
"""
from ereignisse_basis import *  # noqa: F401,F403


def P1(handelnd, *betroffen):
    return {"handelnd": handelnd, "betroffen": [{"id": b[0], "ton": b[1], "was": b[2]} for b in betroffen]}


def VT(pid, n):
    return {"wert": ["vertrauen.%s" % pid, ">=", n]}


def BG(pid, n):
    return {"wert": ["begehren.%s" % pid, ">=", n]}


def FUNKE_WANN(pid, phasen, extra=None):
    bed = [VT(pid, 3), BG(pid, 2), {"nicht": {"flag": "%s_funke" % pid}}] + (extra or [])
    # F-37 (Duc 05.11.2026): Tage und Phase wie im Wiki (beziehungen.md "Funken": Tag 4 bis 6, je Frau Abend oder Nacht).
    # Vorher wurde phasen nicht benutzt, alle Funken kamen ab Tag 3 in beiden Phasen.
    return WANN((4, 6), list(phasen), bed={"alle": bed})


FREI = {"flag": "siri_frei"}
FUNKE_B = 14

EVENTS = [
    # ================================================================== Funken
    E("fk_chiara_frage", "abend", "wholesome", "What Would You Do?", FUNKE_WANN("chiara", ["nacht"]), "bridge",
      {"pid": "chiara"},
      "Past midnight the wind swings round to the north. The anchor chain groans once, then again. Chiara is already "
      "on the bridge wing in her jacket, arms folded, watching the lights on shore drift a little to the left.",
      [Z("chiara", "Holm's gone, and I'm not calling Megan about a wind shift, she'd never let me forget it.", "pride"),
       Z("chiara", "So you're the First Officer. Tell me what we do.", "curiosity")],
      [O("Looks at the shore lights, then at her. “No. You've done six seasons here. What would you do?”",
         [B("chiara", FUNKE_B), V("chiara", 4), F("chiara_funke"), NK("chiara")],
         zeile=Z("chiara", "Nobody asks me that. They ask me where the good champagne is. Let out more chain, ten metres, "
                           "and we watch it for an hour. Together, if you're not too tired.", "love")),
       O("Checks the anchor alarm and makes the call himself. “More chain. I'll take the watch.”",
         [V("chiara", 6), F("chiara_funke")],
         zeile=Z("chiara", "Good call, seven out of ten. I'd have said the same, but you didn't ask, did you?",
                 "approval")),
       O("Yawns. “It'll hold. Get some sleep, Chiara.”", [V("chiara", 2), F("chiara_funke")],
         zeile=Z("chiara", "It'll hold, sure. I'll just stand here and make sure of that on my own, then.",
                 "annoyance"))],
      sets={"chiara": "Bridge Night"}, knistern=True,
      nachklang_text="An hour on the bridge wing, the chain quiet at last. Chiara rated the night a nine and didn't "
                     "explain the missing point."),

    E("fk_sophia_wette", "abend", "frech", "Ten Euros", FUNKE_WANN("sophia", ["abend"]), "aft_deck",
      {"pid": "sophia"},
      "Sophia is leaning on the aft rail with two glasses of white wine and that look she gets before a bet. She hands "
      "you one without asking if you want it.",
      [Z("sophia", "Ten euros says you can't make me laugh. Properly laugh, darling. Not the one I do for harbourmasters.",
         "amusement"),
       Z("sophia", "I've had a lot of practice not laughing. Four seasons of it.", "pride")],
      [O("Doesn't try a joke. Tells her, quite seriously, about the time he got locked in a client's walk-in fridge.",
         [], probe=P("charm", 13), erfolg=[B("sophia", FUNKE_B), V("sophia", 4), F("sophia_funke"), NK("sophia")],
         fehlschlag=[B("sophia", 6), V("sophia", 4), F("sophia_funke")],
         zeile=Z("sophia", "Oh, that was a snort. That was a real snort, I haven't done that since I was twelve. "
                           "Keep the ten euros. I'd rather you remembered the sound.", "love")),
       O("“I'll take the bet. But if I win, you tell me one true thing.”",
         [B("sophia", 8), V("sophia", 6), F("sophia_funke")],
         zeile=Z("sophia", "One true thing. You're a terrible negotiator, you know. I'd have given you two.",
                 "desire")),
       O("Raises his glass. “I'd lose. Cheers anyway.”", [V("sophia", 4), F("sophia_funke")],
         zeile=Z("sophia", "Coward. A charming one, but still. Cheers, Duc.", "amusement"))],
      sets={"sophia": "Shore Leave"}, knistern=True,
      nachklang_text="Sophia laughing at the stern, the real one, a little too loud. She looked around afterwards to "
                     "see if anyone had heard."),

    E("fk_lea_schulter", "abend", "wholesome", "Glow", FUNKE_WANN("lea", ["nacht"]), "swim_platform",
      {"pid": "lea"},
      "The water under the swim platform is glowing blue wherever something moves. Lea is sitting on the edge with "
      "her feet in it, kicking slowly, and she pats the teak next to her without looking up.",
      [Z("lea", "Look. Every time I move, it lights up. It's dinoflagellates, they glow when they're disturbed. "
                "Which is a bit rude of me, really, disturbing them.", "excitement"),
       Z("lea", "Sit down? You don't have to talk. I mean, I'll probably talk. You can just listen.", "nervousness")],
      [O("Sits down beside her and puts his feet in the glowing water. “Tell me everything.”",
         [B("lea", FUNKE_B), V("lea", 4), F("lea_funke"), NK("lea"), {"flag_datiert": "lea_glow"}],
         zeile=Z("lea", "Okay, so the light is a chemical reaction, and it might scare off the things that eat them, "
                         "and – sorry. Your shoulder's warm. I'm just going to rest here for a second.", "love")),
       O("Sits a little apart and asks her questions about the plankton.", [V("lea", 6), F("lea_funke")],
         zeile=Z("lea", "You actually want to know? Nobody wants to know. Right. Okay. Where do I start.",
                 "excitement")),
       O("“It's late, Lea. Don't stay out here too long.”", [V("lea", 2), F("lea_funke")],
         zeile=Z("lea", "I won't. Five more minutes. Maybe ten. The sea doesn't do this every night, you know.",
                 "sadness"))],
      sets={"lea": "Off Duty"}, knistern=True,
      nachklang_text="Lea fell asleep against your shoulder halfway through a sentence about light. The water kept "
                     "glowing where her feet had been."),

    E("fk_rosi_schicht", "abend", "frech", "Night Shift", FUNKE_WANN("rosi", ["nacht"]), "generator_room",
      {"pid": "rosi"},
      "Unit-01 is idling and the generator room smells of hot oil. Rosi is lying half under the frame with a torch "
      "in her teeth. She spits it out when she hears you on the ladder.",
      [Z("rosi", "Officer, good, you're here. Hold the torch and don't touch anything, and I mean anything, it's a delicate moment for her.", "neutral"),
       Z("rosi", "She's been coughing since Tuesday, and nobody else hears it. I hear it.", "caring")],
      [O("Lies down next to her under the frame and holds the torch exactly where she needs it.",
         [B("rosi", FUNKE_B), V("rosi", 4), F("rosi_funke"), NK("rosi")],
         zeile=Z("rosi", "Hm. You're not bad at this. Pass me the – yes, that one. Don't look at me like that, I'm "
                         "talking about the spanner. Mostly.", "desire")),
       O("Holds the torch from the ladder and asks what she's listening for.", [V("rosi", 6), F("rosi_funke")],
         zeile=Z("rosi", "The bearing. Hear that little tick, under everything? No? Then you're not listening "
                         "properly yet. Come back tomorrow.", "pride")),
       O("“It's two in the morning, Rosi. She'll still cough tomorrow.”", [V("rosi", 2), F("rosi_funke")],
         zeile=Z("rosi", "She will, and I'll still be here tomorrow. Go to bed, Officer, I've got her.",
                 "annoyance"))],
      sets={"rosi": "Engine Room"}, knistern=True,
      nachklang_text="Two hours under Unit-01, shoulder to shoulder. Rosi called it a draw. On the whiteboard there's "
                     "a new line at the bottom that she covers with her hand."),

    E("fk_siri_foto", "abend", "frech", "Unposted", FUNKE_WANN("siri", ["abend"], [FREI]), "foredeck",
      {"pid": "siri"},
      "Siri is sitting cross-legged on the foredeck, scrolling through her camera roll with the brightness turned "
      "all the way down. She stops on one picture and turns the phone towards you before she can change her mind.",
      [Z("siri", "This one's not going up, because my manager would hate it. There's no filter, the light's bad, and my hair's doing a thing.",
         "nervousness"),
       Z("siri", "It's from this morning. I was just happy. I don't know when I last took a photo because I was "
                 "happy. Sorry. That's a weird thing to show someone.", "embarrassment")],
      [O("Looks at it for a long moment. “You should write the caption. Your words.”",
         [B("siri", FUNKE_B), V("siri", 4), F("siri_funke"), NK("siri")],
         zeile=Z("siri", "My words. I don't think I have any. Okay. How about: I was happy, and somebody noticed. "
                         "Is that stupid? You can say it's stupid.", "love")),
       O("“It's a good photo. Keep it for yourself.”", [V("siri", 6), F("siri_funke")],
         zeile=Z("siri", "For myself. I like that. I don't think I've got anything that's just for myself.",
                 "caring")),
       O("“Your manager's probably right. Bad light.”", [V("siri", 2), F("siri_funke")],
         zeile=Z("siri", "Ha. Yes. Probably. Sorry, I'll put it away. Sorry.", "sadness"))],
      sets={"siri": "Silver Night"}, knistern=True,
      nachklang_text="Siri's photo stayed in her camera roll, unposted. She showed it to you twice more that evening, "
                     "as if checking it was still there."),

    # ================================================================== Rosi
    E("bk_rosi_tafel", "gag1", "frech", "Rosi vs. Officer", WANN((3, 6), ["tag", "nachmittag"], bed=VT("rosi", 2)),
      "workshop", P1("rosi", ("lola", "?", "is shouting about lunch from the galley and sees nothing")),
      "The whiteboard in the workshop says ROSI VS. OFFICER in big red letters. Rosi has fourteen ticks. You have "
      "three. She's adding a fourth to your side, very slowly, as if it hurts.",
      [Z("rosi", "The bilge pump yesterday, that one was yours. I'm a fair person, so I write it down.", "annoyance"),
       Z("rosi", "Don't get used to it. Fourteen to four is still a massacre, Officer.", "pride")],
      [O("Takes the marker from her hand and draws a tiny crown over her fourteen.", [B("rosi", 6), V("rosi", 2)],
         zeile=Z("rosi", "A crown. Okay, that's – you can't just be nice in the middle of a rivalry, it's against the rules. Give me the marker.", "embarrassment")),
       O("“Fourteen? I counted twelve.”", [V("rosi", 4)], probe=P("cunning", 12),
         erfolg=[B("rosi", 4), V("rosi", 2)], fehlschlag=[V("rosi", 2)],
         zeile=Z("rosi", "You counted wrong, so I'll recount, out loud and with feeling. Sit down, this will take a while.",
                 "amusement")),
       O("Nods and leaves her to it.", [V("rosi", 2)],
         zeile=Z("rosi", "Hm, no speech. Good, I hate speeches.", "neutral"))],
      sets={"rosi": "Engine Room"}),

    E("bk_rosi_fleck", "gag1", "frech", "Grease", WANN((3, 6), ["nachmittag", "dinner"], bed=VT("rosi", 2)),
      "crew_mess", P1("rosi", ("toto", "?", "is arguing with the coffee machine and notices nothing")),
      "You sit down for coffee. Rosi takes one look at you, licks her thumb and wipes a streak of grease off your "
      "cheekbone before either of you has thought about it. Then her thumb stops halfway.",
      [Z("rosi", "That was – a quality check of the cloth. I mean the thumb. It's a very good thumb.",
         "embarrassment")],
      [O("Doesn't move. “Missed a bit.”", [B("rosi", 6), V("rosi", 2), NK("rosi")],
         zeile=Z("rosi", "Did I. Where. No, don't point, I'll find it myself. Stop smiling, Officer, it's distracting "
                         "the inspection.", "desire")),
       O("“Thanks. Comes with the job, I suppose.”", [V("rosi", 4)],
         zeile=Z("rosi", "It does, everything comes with the job. Drink your coffee.", "relief")),
       O("Laughs and wipes the rest off with a napkin.", [V("rosi", 2)],
         zeile=Z("rosi", "Fine, use the napkin. The napkin's never been under a generator, but sure.", "annoyance"))],
      sets={"rosi": "Engine Room"}),

    # ================================================================== Sophia
    E("bk_sophia_arm", "gag1", "frech", "Darling, Hold Still", WANN((3, 6), ["tag", "nachmittag"],
      bed=VT("sophia", 2)), "main_salon", P1("sophia", ("chiara", "?", "is on the phone in the galley")),
      "Sophia's phone buzzes, she glances at the name, and in one smooth movement she hooks her arm through yours "
      "and turns you both towards the window, as if you were deep in a very important conversation.",
      [Z("sophia", "Harbourmaster. He wants to talk about mooring fees. He's lovely and he never stops. Pretend I'm "
                   "telling you something fascinating.", "amusement"),
       Z("sophia", "There. He's given up. You can have your arm back now, darling.", "neutral")],
      [O("Doesn't take it back. “Actually, tell me the fascinating thing.”", [B("sophia", 6), V("sophia", 2)],
         zeile=Z("sophia", "There isn't one. I made it up. I'll have to think of something now, won't I. "
                           "Give me a minute. I'm not used to being asked.", "desire")),
       O("“Happy to be a prop. Anytime.”", [V("sophia", 4)],
         zeile=Z("sophia", "Careful, I might take you up on that. I go through a lot of props.", "amusement")),
       O("Gently frees his arm. “You'll have to call him back eventually.”", [V("sophia", 2)],
         zeile=Z("sophia", "Eventually. That's a lovely word. It means not today.", "neutral"))],
      sets={"sophia": "Concierge"}),

    E("bk_sophia_buechlein", "gag1", "frech", "The Brown Notebook", WANN((3, 6), ["abend"], bed=VT("sophia", 2)),
      "alvas_bar", P1("sophia", ("alva", "?", "is busy at the other end of the bar")),
      "At Alva's bar Sophia is writing in her little brown notebook again. Every few lines she looks up at you, "
      "then down, and writes a bit more. When she sees you watching, she closes it with one finger.",
      [Z("sophia", "Don't ask, it's research. You'd be surprised how much research a person can do at a bar.",
         "amusement")],
      [O("“Am I in it?”", [B("sophia", 6), V("sophia", 2)], probe=P("charm", 12),
         erfolg=[B("sophia", 4)], fehlschlag=[],
         zeile=Z("sophia", "You might be, as a minor character. He's tall and asks too many questions, and he's growing on the author, which is very inconvenient.", "desire")),
       O("Doesn't ask, and orders her another drink.", [V("sophia", 4)],
         zeile=Z("sophia", "No questions? Darling, you're the first man in four seasons who's let a woman keep "
                           "her secrets. I may have to write that down too.", "approval")),
       O("Reaches for the notebook, teasing.", [V("sophia", 2)],
         zeile=Z("sophia", "Ah-ah. Hands where I can see them. Some things you have to earn.", "annoyance"))],
      sets={"sophia": "Shore Leave"}),

    # ================================================================== Siri
    E("bk_siri_stuhl", "gag1", "wholesome", "Talking to the Furniture", WANN((3, 6), ["tag", "nachmittag"],
      bed=VT("siri", 2)), "sun_deck", P1("siri", ("yasin", "?", "is filming himself at the other end of the deck")),
      "Siri has bumped into a sun lounger, and she is apologising to it. Quietly and sincerely. Then she notices you.",
      [Z("siri", "Sorry. I mean, sorry to you too. I was saying sorry to the chair. It didn't do anything wrong.",
         "embarrassment"),
       Z("siri", "Do you ever do that, or is it just me? Please say it's not just me.", "curiosity")],
      [O("Pats the lounger. “It forgives you. It told me.”", [V("siri", 4), B("siri", 2)],
         zeile=Z("siri", "Oh good. That's a relief. It's a very forgiving chair. I like it here.", "amusement")),
       O("“I apologise to my car every morning.”", [V("siri", 4)],
         zeile=Z("siri", "Really? What do you say to it? No, wait, don't tell me, I want to imagine it.", "amusement")),
       O("Smiles and walks on.", [V("siri", 2)],
         zeile=Z("siri", "Okay. Bye. Sorry. Bye.", "embarrassment"))],
      sets={"siri": "Riviera Swim"}),

    E("bk_siri_goldene_stunde", "gag1", "frech", "Golden Hour, Camera Off", WANN((3, 6), ["abend"],
      bed={"alle": [VT("siri", 2), FREI]}), "sun_deck", P1("siri", ("lola", "?", "is singing in the galley")),
      "The sun is low and everything on deck is turning gold. Siri holds out her phone so you can take a picture of "
      "her. Then, halfway through her pose, she lowers her arms and puts the phone face down on the lounger.",
      [Z("siri", "Actually, no, don't take it, just look. Is that okay? I want one golden hour that nobody else gets.", "desire")],
      [O("Puts the phone in his pocket and just looks at her.", [B("siri", 6), V("siri", 2), NK("siri")],
         zeile=Z("siri", "You're really looking. Nobody really looks, they look at the screen. Okay. I'm going to "
                         "go red now. That's allowed too.", "love")),
       O("“Your golden hour. I'll keep watch.”", [V("siri", 4)],
         zeile=Z("siri", "Keep watch, like a lighthouse. I like that, you'd make a good lighthouse.", "caring")),
       O("Takes the picture anyway, as a joke.", [V("siri", -2)],
         zeile=Z("siri", "Oh. Okay. No, it's fine. Delete it later, maybe. It's fine.", "sadness"))],
      sets={"siri": "Silver Night"}),
]
