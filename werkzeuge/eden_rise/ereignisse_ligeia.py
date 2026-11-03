# -*- coding: utf-8 -*-
r"""Ligeia, die Sirene im Teich (Duc 29.10.2026, docs/wiki/figuren/ligeia.md): Vertrauens-Stufen und die Spur.

Hidden Character: Im Spiel heisst sie "The Siren". Jede Stufe hat eine spuerbare Wirkung (Mechaniken verweben):
  T2 lg_lied      Wiegenlied am Teich - +1 Energie
  T3 lg_drei      "There were three of us, once." - oeffnet die Felsen (Lea)
  T4 lg_perle     ihre Perle auf dem Wrack - oeffnet Petrus Seekiste
Spur (jede Fundstelle schreibt einen Codex-Eintrag):
  lg_lola_meer    Akt 1: das Meer leuchtet, jemand summt
  lg_siri_lied    Akt 2: Siri summt ein Lied, das sie nie gelernt hat
  lg_petru_1924   nach der Flut-Nacht: die Crew der Margot schlief und sang
  lg_seekiste     Petrus Kaestchen mit der leeren Mulde
  lg_felsen       Lea hat die drei Felsen bei Ebbe fotografiert
Alles als art "abend": kommt in Abend/Nacht, ersetzt die freie Phase, hoechstens einer am Tag (kern/ereignisse.py).
Woche 3 (Galionsfigur, ihr Name, ihr Ende) folgt mit dem Tauchgang.
"""
import re

from ereignisse_basis import *  # noqa: F401,F403

C = lambda text: {"codex": text}
POOL = "siren_pool"
NACH_FLUT = {"flag": "sirene_fertig"}
PETRU_WARM = {"eine": [{"nicht": {"flag": "petru_werkstatt_zu_duc"}}, {"flag": "petru_versoehnt"}]}
SIRENE = {"sirene": "sirene_standard"}


def T(stufe):
    return {"wert": ["vertrauen.sirene", ">=", stufe]}


def NICHT(flag):
    return {"nicht": {"flag": flag}}


TAG = re.compile(r"\s*\[(chuckle|clear throat|cough|gasp|laugh|shush|sigh|sniff)\]\s*")
STIMME = []                  # gesprochene Fassung: [(wer, text, gesprochen)], traegt ereignisse_favours in stimme_tags ein


def G(wer, text, gefuehl):
    """Zeile mit Turbo-Tag: das Spiel zeigt sie ohne, die Stimme liest sie mit."""
    klar = TAG.sub(" ", text).strip()
    assert klar != text, text
    STIMME.append((wer, klar, " ".join(text.split())))
    return Z(wer, klar, gefuehl)


def FLASCHE(stufe, titel, lage, zeile, gefuehl, antworten):
    """Flaschenpost je Vertrauensstufe (Duc 30.10.2026): immer zwei Polaroids, kommt ueber _favour_ziehen ohne Wuerfeln."""
    kid = "sirene_t%d" % stufe
    return E("lg_flasche_t%d" % stufe, "abend", "wholesome", titel,
             WANN((11, 21), ["tag", "abend"], bed={"alle": [{"flag": "ligeia_polaroid"}, T(stufe)]}, holt_leute=True),
             "swim_platform",
             {"handelnd": "sirene", "anrufer": "sirene", "betroffen": [],
              "favour": {"kette": kid, "teil": 4, "ketten_titel": "Polaroids: " + titel, "dank": True, "foto": "fv_" + kid,
                         "stufe": stufe}},
             lage, [G("sirene", zeile, gefuehl)],
             [O(chip, [V("sirene", 3)], zeile=G("sirene", z, g)) for chip, z, g in antworten],
             sets=SIRENE)


FLASCHEN = [
    FLASCHE(2, "My Ceiling", "A green bottle knocks against the swim platform. Inside are two Polaroids, curled from the damp, "
            "each with a line in a slanting old hand.",
            "[chuckle] The girl says I'm to show you things, sailor. So that's what I look at when you've gone home.", "amusement",
            [("Holds up the second one. “Who took this?”",
              "[chuckle] An octopus helped me. She has very steady hands, all of them.", "amusement"),
             ("Turns it over, looking for more.", "[chuckle] There isn't any more. You're greedy, sailor.", "amusement")]),
    FLASCHE(3, "The Three of Us", "Another bottle on the platform, with two more Polaroids. The first one is very dark.",
            "[sigh] I went to look at them at low tide, for the box. I've not looked at them in a long time.", "sadness",
            [("Keeps the first one in his logbook.", "[sniff] That's a good place for them. Thank you, sailor.", "caring"),
             ("Looks at the second one instead. “You look tired.”", "[chuckle] I'm older than your alphabet. Of course I do.",
              "amusement")]),
    FLASCHE(4, "Still Empty", "The bottle is heavier this time. Two Polaroids, wrapped in a bit of old sailcloth.",
            "[sigh] I wore it to show you, and then I felt foolish. Keep the picture. I'll keep the rest.", "remorse",
            [("Wraps them up again. “I won't show anyone.”", "[sniff] You're the only one who ever says that and means it.",
              "caring"),
             ("Studies the first one. “We could still find it.”", "[sigh] Don't be kind to me, sailor. I told you, I'm not used to it.",
              "sadness")]),
    FLASCHE(5, "Past Your Lamps", "The last bottle of the summer, or it feels that way. Two Polaroids. In the second one, she is "
            "laughing.",
            "[laugh] It took me nine squares to get that first one, and the girl's going to be so jealous. Duc. I do like saying it. Duc.",
            "joy",
            [("Pins the second one above his bunk.", "[chuckle] Where everyone can see? You'll have to tell them about the octopus.",
              "amusement"),
             ("Says thank you to the empty sea, out loud, and feels stupid.", "[sigh] I heard that. I hear everything on that water, you know.",
              "caring")]),
]

EVENTS = FLASCHEN + [
    # ------------------------------------------------------------------ Pflichtszene: die erste Nacht nach der Grotte
    # Duc 30.10.2026: Sie will Duc besuchen, Lea erwischt sie im Tenderdock. Das Polaroid traegt danach ihre Favours.
    E("lg_polaroid", "abend", "wholesome", "The Tender Garage", WANN((11, 21), ["nacht"], pflicht=True,
      bed={"alle": [{"flag_seit": ["ligeia_freund", 1]}, NICHT("ligeia_polaroid")]}, holt_leute=True), "tender_garage",
      {"handelnd": "lea", "betroffen": [{"id": "sirene", "ton": "+"}], "duo": True},
      "A splash wakes you, then a voice from the tender garage, very fast and very English. You go down. The stern door is "
      "open to the black water. Lea stands barefoot on the ramp in an old jumper, a dive torch shaking in her hand. On the "
      "teak in front of her, dripping, lies the woman from the black pool in the grotto, her long tail across the cradle of the tender.",
      [G("lea", "[gasp] Duc. Don't shout, okay? I came down for my logbook and she was just there. That's a real caudal fin, "
                "look at the rays on it, that's, oh my days.", "surprise"),
       G("sirene", "[sigh] Put out your little sun, girl, it hurts my eyes. I came to see where he sleeps. I didn't come for "
                   "you.", "annoyance"),
       G("lea", "[gasp] Right, yes, sorry. Is that better? Can I ask, do you breathe through your skin at all? Sorry, is that "
                "rude? I've never met a mermaid.", "embarrassment"),
       G("sirene", "[chuckle] A mermaid. Is that what they say now? Go on, then, ask your questions. It's been a long time "
                   "since anyone asked me for anything but mercy.", "amusement"),
       G("lea", "[laugh] How deep do you go? Have you seen the little squid off the point, the ones that glow? I go down to "
                "six metres at night to watch them, and nobody knows I do that.", "joy"),
       G("sirene", "[chuckle] I know. You draw the fish on your ladder with your tongue out. Six metres is very shallow, girl. "
                   "The pretty ones live lower down.", "caring"),
       G("lea", "[gasp] You've seen my drawings? Okay. Okay! Can I take a photo? Just the one, and it's only for me, I swear.",
         "joy"),
       G("sirene", "[clear throat] Photo. I don't know that word. What is it, a kind of fish?", "curiosity"),
       G("lea", "[laugh] Just look at me a sec. There! See? That's you, that's you in my phone.", "joy"),
       G("sirene", "[gasp] That's my face. Why is my face in there? Give it back, girl. Give it back, you've got me in that "
                   "box.", "fear"),
       G("lea", "[gasp] No, no, it's only a picture! I'm deleting it, look, it's gone, it's all gone. You're fine. Are you "
                "fine? Please don't sing.", "fear"),
       G("sirene", "[sniff] Where did it go? Is it in the dark now?", "nervousness"),
       G("lea", "[sigh] It never had anything of you, I promise. A photo's only the light that bounced off you, and the box "
                "remembers it. You don't lose a thing. Best nobody hears about tonight, though. Especially not Sophia.",
         "caring"),
       G("sirene", "[sigh] It keeps the light. And the light stays the way it was. I've seen things there's nobody left to "
                   "remember, you know.", "sadness"),
       G("lea", "[gasp] Hang on. Wait there. This one's my old dive camera, it's a Polaroid, and it's fine down to forty "
                "metres. It doesn't keep you, it just gives you one picture, and then that's the only one. Would you show me "
                "your world? I'm never getting that deep.", "excitement"),
       G("sirene", "[chuckle] You'd hand this to me, and what do you want for it?", "curiosity"),
       G("lea", "[laugh] Only the pictures. Honest.", "joy"),
       G("sirene", "[sigh] Nobody has ever wanted only that.", "admiration")],
      [O("Takes the torch out of Lea's hand. “I was asleep. I saw nothing.”",
         [V("lea", 6), V("sirene", 4), F("ligeia_polaroid"),
          C("Lea gave the Siren a waterproof Polaroid and asked her to show her world. Nobody is to know.")],
         zeile=G("lea", "[sigh] Thanks, Duc. Proper thanks. I'm going to be awake for about a week.", "gratitude")),
       O("Looks at the woman on the ramp. “You came to see where I sleep?”",
         [V("sirene", 6), V("lea", 4), F("ligeia_polaroid"),
          C("Lea gave the Siren a waterproof Polaroid and asked her to show her world. Nobody is to know.")],
         zeile=G("sirene", "[chuckle] With the door wide open, sailor, as it happens. Keep an eye on your swim platform. The "
                           "sea brings things.", "amusement"))],
      sets={"sirene": "sirene_standard", "lea": "Off Duty"}),

    # ------------------------------------------------------------------ Vertrauen
    E("lg_lied", "abend", "wholesome", "A Lullaby at High Tide", WANN((11, 21), ["abend", "nacht"], an_land=True,
      bed={"alle": [NACH_FLUT, T(2), NICHT("ligeia_lied")]}), POOL, {"pid": "sirene"},
      "The tide is in. You go down the rock steps and switch off the torch at the bottom. The pool is silver. She is "
      "already there, arms folded on the edge, as if she knew you'd come.",
      [Z("sirene", "Back again, sailor. You look like a man who hasn't slept properly since the storm.", "curiosity"),
       Z("sirene", "Lie down on the warm stone. No, I won't drown you. I'm far too curious about what you'll bring me "
                   "next.", "amusement")],
      [O("Lies down on the warm stone and closes his eyes.",
         [EN(1), V("sirene", 6), F("ligeia_lied"),
          C("The Siren hums a song with no words. Whoever sleeps to it wakes rested.")],
         zeile=Z("sirene", "Good. Don't listen for words. There aren't any. There never were.", "caring")),
       O("Sits up. “What's the song about?”",
         [V("sirene", 8), F("ligeia_lied"),
          C("The Siren's song is about “a city that doesn't know it's standing on someone”.")],
         zeile=Z("sirene", "About a city that doesn't know it's standing on someone. That's all you get tonight. Now lie "
                           "down.", "sadness"))],
      sets=SIRENE,
      nachklang_text="You wake on the beach at first light, rested in a way you can't explain."),

    E("lg_drei", "abend", "ernst", "Three of Us", WANN((11, 21), ["abend", "nacht"], an_land=True,
      bed={"alle": [NACH_FLUT, T(3), {"flag": "ligeia_lied"}, NICHT("ligeia_felsen_hinweis")]}), POOL, {"pid": "sirene"},
      "She isn't teasing tonight. Her chin rests on her folded arms and she watches the crack in the roof where the "
      "moon comes through.",
      [Z("sirene", "There were three of us, once. We sang from the same rock, and men came from all over the sea just "
                   "to hear us.", "sadness"),
       Z("sirene", "Go to the black rocks off the grotto at low tide. You'll see what's left of us. And then don't ask "
                   "me about it. Not yet.", "sadness")],
      [O("“I'll go.”", [V("sirene", 6), F("ligeia_felsen_hinweis"),
                         C("The Siren: “There were three of us, once.” Something waits on the black rocks at low tide.")],
         zeile=Z("sirene", "I know you will. You're that kind. Gods help you.", "caring")),
       O("Says nothing and stays with her until the tide turns.",
         [V("sirene", 8), F("ligeia_felsen_hinweis"),
          C("The Siren: “There were three of us, once.” Something waits on the black rocks at low tide.")],
         zeile=Z("sirene", "Nobody has done that in a long time. Stayed, I mean. Without wanting anything.", "caring"))],
      sets=SIRENE),

    E("lg_perle", "abend", "ernst", "What I Left Behind", WANN((11, 21), ["abend", "nacht"], an_land=True,
      bed={"alle": [NACH_FLUT, T(4), {"flag": "ligeia_felsen_hinweis"}, NICHT("ligeia_perle_hinweis")]}), POOL,
      {"pid": "sirene"},
      "Tonight she keeps one hand under the water and won't show you what's in it. When she finally opens it, it's "
      "empty.",
      [Z("sirene", "I had a pearl once, as big as a thumbnail. I carried it for longer than your gods have had names.",
         "sadness"),
       Z("sirene", "The night that old sailing ship went down, I left it on the wreck. For whoever came for the bodies. It seemed "
                   "the decent thing to do.", "remorse")],
      [O("“Somebody came. Maybe they still have it.”",
         [V("sirene", 6), F("ligeia_perle_hinweis"),
          C("The Siren left her pearl on the wreck in 1924, “for whoever came for the bodies”.")],
         zeile=Z("sirene", "For the bodies, sailor. I said for the bodies. Don't be kind to me, I'm not used to it.",
                 "annoyance")),
       O("Takes her empty hand for a moment.",
         [V("sirene", 8), F("ligeia_perle_hinweis"),
          C("The Siren left her pearl on the wreck in 1924, “for whoever came for the bodies”.")],
         zeile=Z("sirene", "Cold, I know. Everything down here is.", "caring"))],
      sets=SIRENE),

    # ------------------------------------------------------------------ Spur
    E("lg_lola_meer", "abend", "witzig", "The Water Is Glowing", WANN((2, 6), ["nacht"],
      bed=NICHT("ligeia_meer")), "galley", {"pid": "lola"},
      "Lola grabs your sleeve in the dark galley and pulls you to the porthole. Outside, the whole bay is lit from "
      "underneath, blue and soft, all the way to the beach.",
      [Z("lola", "Boss, look at the water, it's glowing. It's like someone spilled a lava lamp in the sea.",
         "surprise"),
       Z("lola", "Probably plankton. Probably. Only, can you hear that humming? No? Just me? Cool, totally fine.",
         "nervousness")],
      [O("Listens at the porthole.", [V("lola", 4), F("ligeia_meer"),
                                      C("One night in the bay the water glowed blue, and Lola heard humming over it.")],
         zeile=Z("lola", "See? You heard it. Don't tell me you didn't, your face is doing a thing.", "amusement")),
       O("“It's plankton, Lola. Go to bed.”", [V("lola", 2), F("ligeia_meer")],
         zeile=Z("lola", "Yeah. Yeah, plankton. Plankton that hums. Night, Boss.", "nervousness"))]),

    E("lg_siri_lied", "abend", "ernst", "A Song She Never Learned", WANN((9, 21), ["nacht"],
      bed=NICHT("ligeia_lied_siri")), "solar_deck", {"pid": "siri"},
      "Siri sits on the solar deck in her dad's old sweater, knees pulled up, humming. It's a slow tune that rises and "
      "falls like a boat at anchor. She stops when she sees you.",
      [Z("siri", "Sorry. Was I loud? I've had this in my head since we anchored here, and I don't even know what it is.",
         "embarrassment"),
       Z("siri", "It's not Norwegian. It's not anything I know. It's just there when I wake up. Like someone sang it to "
                 "me while I was asleep.", "confusion")],
      [O("“Hum it again.”", [V("siri", 4), F("ligeia_lied_siri"),
                              C("Siri hums a tune she never learned. It sounds like an old Neapolitan lament.")],
         zeile=Z("siri", "Okay. But if you laugh, I'm throwing you overboard. Nicely.", "embarrassment")),
       O("“Where were you sleeping when you first heard it?”",
         [V("siri", 6), F("ligeia_lied_siri"),
          C("Siri hums a tune she never learned. She first heard it asleep on the swim platform, feet in the water.")],
         zeile=Z("siri", "On the swim platform, with my feet in the water. That's a bit creepy now that I say it out "
                         "loud.", "nervousness"))],
      sets={"siri": "Dad's Sweater"}),

    E("lg_petru_1924", "abend", "ernst", "Asleep on the Wreck", WANN((11, 21), ["abend"], an_land=True,
      bed={"alle": [NACH_FLUT, PETRU_WARM, NICHT("ligeia_1924")]}), "petru_workshop", {"pid": "petru"},
      "For once the radio on the workbench is off. Petru sits with the net in his lap and isn't mending it. When you "
      "come in, he nods at the stool.",
      [Z("petru", "You went down to the grotto at high tide. Totò says so. The whole village says so.", "neutral"),
       Z("petru", "My grandfather rowed out the night that old ship, the Margot, sank. He said they were all asleep on the wreck, every "
                  "man, and singing in their sleep. Nobody drowned. Hm. He never could explain that.", "sadness")],
      [O("“I heard someone singing down there.”",
         [V("petru", 4), F("ligeia_1924"),
          C("1924: the crew of the Margot was found asleep on the wreck, singing in their sleep. Nobody drowned. "
            "Petru calls the Siren's song a lament – a song for the dead.")],
         zeile=Z("petru", "Then you heard a lament. A song for someone dead. The women here used to sing them. Someone "
                          "down there is still mourning.", "sadness")),
       O("“Maybe somebody kept them calm.”",
         [V("petru", 6), F("ligeia_1924"),
          C("1924: the crew of the Margot was found asleep on the wreck, singing in their sleep. Nobody drowned.")],
         zeile=Z("petru", "Hm. My grandfather said the same. Then he went to church every day for a month.",
                 "neutral"))]),

    E("lg_seekiste", "abend", "ernst", "The Empty Box", WANN((11, 21), ["abend"], an_land=True,
      bed={"alle": [{"flag": "ligeia_1924"}, PETRU_WARM, NICHT("ligeia_perle"),
                    {"eine": [{"wert": ["vertrauen.petru", ">=", 3]}, {"flag": "ligeia_perle_hinweis"}]}]}),
      "petru_workshop", {"pid": "petru"},
      "Petru drags an old sea chest out from under the workbench. Inside, wrapped in a shirt that smells of tar, is a "
      "small wooden box. The velvet inside has a hollow the size of a thumbnail.",
      [Z("petru", "My grandfather's. He brought it back from the Margot. There was a pearl in it.", "neutral"),
       Z("petru", "He never sold it. Said it wasn't his, that she left it on the wreck for us, whoever she was. Then one "
                  "night it was gone. The box is still here. Hm.", "sadness")],
      [O("“Gone where?”", [V("petru", 4), F("ligeia_perle"),
                           C("Petru's grandfather kept a pearl from the wreck of the Margot: “She left it on the wreck "
                             "for us.” One night it was gone.")],
         zeile=Z("petru", "Back to the sea, my grandmother said. Some things want to go home. I was six and I believed "
                          "her. I still do.", "caring")),
       O("Closes the box gently and hands it back.",
         [V("petru", 6), F("ligeia_perle"),
          C("Petru's grandfather kept a pearl from the wreck of the Margot: “She left it on the wreck for us.” One "
            "night it was gone.")],
         zeile=Z("petru", "Hm. Good. You understand boxes. Most people only understand what's in them.", "approval"))]),

    E("lg_felsen", "abend", "ernst", "Three Rocks at Low Tide", WANN((11, 21), ["abend"],
      bed={"alle": [{"flag": "ligeia_felsen_hinweis"}, NICHT("ligeia_felsen")]}), "sun_deck", {"pid": "lea"},
      "Lea finds you on the sun deck, still in her wetsuit, hair dripping onto her phone screen. On the screen: three "
      "black rocks in a row, wet and shining. Two have a name scratched deep into them in old letters, worn soft by the "
      "sea. PARTHENOPE. LEUKOSIA. The third rock is bare.",
      [Z("lea", "Okay, don't laugh. I went out to the black rocks at low tide, for the limpets, proper scientific "
                "reasons. And then I found this.", "embarrassment"),
       Z("lea", "Those are Greek, right? Who carves names into rocks you can only reach twice a month? And why is the "
                "third one empty? That's the bit that gives me the creeps.", "curiosity")],
      [O("“Send me that photo.”", [V("lea", 4), F("ligeia_felsen"),
                                    C("Three black rocks off the grotto, only dry at low tide. Two names: PARTHENOPE, "
                                      "LEUKOSIA. The third rock is bare.")],
         zeile=Z("lea", "Sent. I think I'm keeping it as my wallpaper. Is that weird? That's weird.", "nervousness")),
       O("“Maybe it's waiting for someone.”",
         [V("lea", 6), F("ligeia_felsen"),
          C("Three black rocks off the grotto, only dry at low tide. Two names: PARTHENOPE, LEUKOSIA. The third rock is "
            "bare – as if it were waiting for someone.")],
         zeile=Z("lea", "Great, now I've got goosebumps. Thanks, Duc. Thanks a lot.", "surprise"))]),
]
