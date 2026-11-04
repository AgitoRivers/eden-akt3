# -*- coding: utf-8 -*-
r"""Outfit-Quests (Duc 31.10.2026, E-104, Wiki systeme/schneider.md). Pilot: Sophias Lesung, Text docs/brain_trust/QUEST_SOPHIA_LESUNG.md.

Vier Schritte: Wunsch, ein besonderes Material, Anprobe mit einer Wahl, Anlass mit Echo. Die Quest setzt nach der Leiter-Szene an und
ersetzt das Schnittmuster (massstueck "quest": kern/schneider.py). Der Mantel bleibt Anlass-Outfit, also kein set_frei.
  ol_wunsch -> ol_mantel -> ol_poker (3 Haende) -> Massstueck bei Danzel -> ol_etikett -> ol_tuer_* -> ol_auftritt_* -> ol_stille
  -> ol_kipp -> ol_reaktion -> ol_tresen, danach ol_echo und ol_dorf.
Zeilen stehen hier MIT Turbo-Tag; tags_schreiben() traegt sie in stimme_tags.json ein. Vertont wird erst ganz am Ende (Duc 31.10.2026).
"""
import json, os, sys

from ereignisse_basis import *  # noqa: F401,F403

HIER = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(os.path.dirname(HIER))
sys.path.insert(0, EDEN)
from kern import stimme  # noqa: E402

TAGE = (11, 21)                  # Akt 2, dazu Akt 3 als zweites Fenster (nie ueber eine Aktgrenze)
AKT3 = [24, 35]             # Akt 3 beginnt nach dem Cliffhanger (E-114, Duc 04.11.2026)
READING = "Book Reading"
FD = lambda name: {"flag_datiert": name}
DIREKT = lambda ziel: {"direkt": ziel}
FAKT = lambda pid, text: {"fakt": {"wer": pid, "text": text}}
N = lambda flag: {"nicht": {"flag": flag}}
SEIT = lambda flag, tage: {"flag_seit": [flag, tage]}
_TAGS = []

MANTEL = item("old_camel_coat", "Old Camel Coat", "quest", preis=None,
              text="Heavy camel wool from the thirties, with an English tailor's mark worn nearly smooth. It has been lost at cards at least twice. Both times, someone was very upset.")
GEWONNEN = {"flags_anzahl": ["ol_p_g", ">=", 2]}
MASSSTUECKE = [{"id": "penrose_coat", "frau": "sophia", "label": "Penrose's Coat", "geld": 60, "material": {}, "items": {"old_camel_coat": 1},
                "quest": True, "wenn": {"item": "old_camel_coat"},
                "text": "A camel coat from the thirties, taken apart and built again around one person. The tailor always leaves the name in the collar until the last minute."}]


def S_(wer, gesprochen, gefuehl="neutral", **kw):
    """Zeile mit Turbo-Tag: im Text ohne Tag, in stimme_tags.json mit."""
    klar = stimme.vorlesen(stimme.ohne_tags(gesprochen))
    assert klar != gesprochen, gesprochen
    _TAGS.append((wer, klar, gesprochen))
    return dict(Z(wer, klar, gefuehl), **kw)


def WP(phase, *bed):
    """Pflicht-Szene, ausgeloest ueber flag_seit, Akt 2 und Akt 3 als getrennte Fenster."""
    w = WANN(TAGE, [phase], bed={"alle": list(bed)}, pflicht=True, holt_leute=True)
    w["akt2"] = list(AKT3)
    return w


def FRAME():
    """Weiterer Takt einer Szene: wird nie gezogen (Flag bleibt aus), nur ueber die Folge "direkt" geoeffnet."""
    return WANN((8, 21), bed={"flag": "ol_nur_direkt"})


def GAG(id, ton, titel, wann, bild, wer, betroffen, lage, zeilen, optionen, sets):
    return E(id, "gag1", ton, titel, wann, bild, {"handelnd": wer, "betroffen": [{"id": p, "ton": "?", "was": ""} for p in betroffen]},
             lage, zeilen, optionen, sets)


def TAKT(id, ton, titel, wann, bild, pid, lage, zeilen, optionen, sets):
    """Ein Takt mit nur einer Antwort (art abend erlaubt das)."""
    return E(id, "abend", ton, titel, wann, bild, {"pid": pid}, lage, zeilen, optionen, sets)


# ------------------------------------------------------------------ 1 Wunsch
WUNSCH = [
    GAG("ol_wunsch", "wholesome", "The Slow Night",
        WP("tag", SEIT("rm_s3", 2), SEIT("rt_ende_tag", 3), N("gefeuert_sophia")),
        "alvas_bar", "sophia", ["alva"],
        "A slow day at Alva's bar. Sophia sits at the end of the counter with her little brown notebook. Alva is drying a glass and looking at all the empty chairs.",
        [S_("alva", "My quiet nights are killing me, Sophia. [sigh] You did theatre in London, didn't you? Come and read something out loud, a story, anything, and I'll sell wine to the people who come to listen.", "annoyance"),
         S_("sophia", "Alva, darling, I stood at the side of a stage for two years and I never once went on. [chuckle] It's the thing I'm best at.", "amusement"),
         S_("sophia", "You've seen the letters, Duc, now that Alva's gone down to the cellar. [sigh] Fifteen publishers have said no to M. J. Penrose, and that's me, as you know. But not one of them has ever heard the book out loud.", "nervousness"),
         S_("sophia", "Ten euros says I'd be sick before the first page. [clear throat] So tell me, and please don't be kind. Should I do it?", "neutral")],
        [O("Puts ten euros on the counter. “I'll take that bet. Three days from now.”", [F("ol_wette"), FD("ol_wunsch"), DIREKT("ol_wunsch_b")],
           zeile=S_("sophia", "You put money on the bar. [chuckle] Oh, that's low. You know I can't walk away from a bet.", "amusement")),
         O("“Would you read the vicar? The one who'd been dead since Tuesday?”", [V("sophia", 4), FD("ol_wunsch"), DIREKT("ol_wunsch_b")],
           zeile=S_("sophia", "[laugh] You remember the marmalade. Yes, I suppose I'd have to read the vicar.", "joy")),
         O("“It's your secret. What do you want, Sophia?”", [B("sophia", 4), FD("ol_wunsch"), DIREKT("ol_wunsch_b")],
           zeile=S_("sophia", "There you go, asking. Nobody ever does. [sigh] I want to go on, Duc. Only once, just so I know.", "love"))],
        {"sophia": "Concierge", "alva": "alva_standard"}),
    TAKT("ol_wunsch_b", "wholesome", "The Slow Night", FRAME(), "alvas_bar", "sophia",
         "Sophia turns the notebook over twice, and then she looks down at her uniform.",
         [S_("sophia", "But I can't go up there in this, because they'd all ask me for a table. [clear throat] M. J. Penrose has a coat. I've had it in my head for three books, a camel coat from the thirties with a belt. Ask your friend Danzel if such a thing still exists.", "curiosity")],
         [O("Says he'll ask Danzel.", [])],
         {"sophia": "Concierge"}),
]

# ------------------------------------------------------------------ 2 Material
_TELL = "Sophia's message is still on your phone: “he says sorry when his cards are good. thirty years in a bank, poor man. don't you dare tell him”"


def _hand(id, lage, zeilen, mehr_gut, antwort_mehr, antwort_weg, weiter):
    """Eine Pokerhand. Wer richtig liest, bekommt ein Flag ol_p_g*, zwei davon gewinnen den Mantel."""
    gut = [F("ol_p_g" + id[-1])]
    return TAKT(id, "witzig", "A Coat at Cards", FRAME(), "crew_mess", "yamamoto", lage, zeilen,
                [O("Puts in more money.", (gut if mehr_gut else []) + [DIREKT(weiter)], zeile=antwort_mehr),
                 O("Gives up the hand.", ([] if mehr_gut else gut) + [DIREKT(weiter)], zeile=antwort_weg)],
                {"yamamoto": "yamamoto_hawaii_b"})


ENDE_POKER = [{"wenn": GEWONNEN, "id": "ol_p_sieg"}, {"id": "ol_p_nieder"}]
MATERIAL = [
    GAG("ol_mantel", "witzig", "A Coat at Cards", WP("tag", SEIT("ol_wunsch", 1)), "village_piazza", "danzel", ["toto"],
        "You ask Danzel about a camel coat from the thirties, for a friend. He stops pretending to be busy. Totò is across the piazza, eating something, and he comes over when he hears the word coat.",
        [S_("danzel", "A camel coat from the thirties, with real wool. No, nobody makes that cloth any more, and what they sell now would be an insult to her. [clear throat] I would need an old one to take apart, very slowly.", "neutral"),
         S_("danzel", "There's only one on this coast that I know of. Totò had it in his locker. [sigh] He wanted a price that made me feel unwell.", "curiosity"),
         S_("toto", "Comandante, that coat! It was an English gentleman's, and nine years I kept it safe. [sigh] Last night I put it on the table, and I lost it to Yamamoto-san. Two to one on me, I gave myself, and I'm still upset.", "remorse"),
         S_("toto", "If you're going to play him, [clear throat] ask Sophia first. She's the only one who beats him.", "curiosity")],
        [O("Sends Sophia a message. “How do you beat Yamamoto?”", [FD("ol_mantel")]),
         O("“I'll play him tonight. Tell Sophia I said so.”", [FD("ol_mantel")],
           zeile=S_("toto", "[chuckle] I'll tell her, Comandante. Two to one against you, and today I am generous.", "amusement"))],
        {"danzel": "danzel_B", "toto": "Standard"}),
    TAKT("ol_poker", "witzig", "A Coat at Cards", WP("abend", SEIT("ol_mantel", 0)), "crew_mess", "yamamoto",
         _TELL + ". Yamamoto is sitting alone with a pack of cards, and the coat is folded on the chair beside him. He stands up and bows to you, and then, you are nearly sure, to the coat.",
         [S_("yamamoto", "Officer-san. Very honoured. [clear throat] Three hands, please. If you win two, you take the coat with my respect.", "neutral")],
         [O("Sits down and cuts the cards.", [DIREKT("ol_p1")])],
         {"yamamoto": "yamamoto_hawaii_b"}),
    _hand("ol_p1", "First hand. Yamamoto looks at his cards and his thumb goes to his watch. Sophia wrote: he says sorry when his cards are good.",
          [S_("yamamoto", "So sorry. [sigh] I am very tired tonight.", "neutral")], False,
          S_("yamamoto", "So sorry, Officer-san. [cough] Three queens.", "remorse"),
          S_("yamamoto", "Very wise. [clear throat] I had three queens, and I was so sorry about them.", "approval"), "ol_p2"),
    _hand("ol_p2", "Second hand. Yamamoto looks at his cards. His hands lie flat on the table. Sophia wrote: he says sorry when his cards are good.",
          [S_("yamamoto", "Very interesting. [clear throat] Your turn, please.", "curiosity")], True,
          S_("yamamoto", "[sigh] Very interesting. I have a pair of twos, and now I have nothing.", "disappointment"),
          S_("yamamoto", "[chuckle] A pair of twos, Officer-san. You were afraid of a pair of twos.", "amusement"), "ol_p3"),
    _hand("ol_p3", "Last hand. Yamamoto smiles at you and doesn't say a word. Then his thumb goes to his watch, the same way it did on the first hand.",
          [S_("yamamoto", "Sophia-san also watches my mouth. [clear throat] Tonight I will say nothing.", "amusement")], False,
          S_("yamamoto", "[sigh] You should have watched more than my mouth. A full house.", "remorse"),
          S_("yamamoto", "[gasp] You did not watch my mouth. You watched my hands. Who taught you this?", "surprise"), ENDE_POKER),
    TAKT("ol_p_sieg", "witzig", "A Coat at Cards", FRAME(), "crew_mess", "yamamoto",
         "Yamamoto stands up and lifts the coat from the chair with both hands. He holds it out to you, and he bows.",
         [S_("yamamoto", "Very interesting. So sorry. [chuckle] Please tell Sophia-san she owes me a new way to lose.", "admiration")],
         [O("Takes the coat with both hands, and bows back.", [MANTEL, W("ruf", 1)])],
         {"yamamoto": "yamamoto_hawaii_b"}),
    TAKT("ol_p_nieder", "witzig", "A Coat at Cards", FRAME(), "crew_mess", "yamamoto",
         "Yamamoto squares the pack and looks at the coat for some time. Then he looks at you, and he bows.",
         [S_("yamamoto", "The coat is heavy, Officer-san, and I carry my own luggage. [clear throat] Forty euros, for Totò's feelings.", "neutral")],
         [O("Pays him forty euros and takes the coat.", [G(-40), MANTEL])],
         {"yamamoto": "yamamoto_hawaii_b"}),
]

# ------------------------------------------------------------------ 3 Anprobe
ANPROBE = [
    GAG("ol_etikett", "wholesome", "The Label", WP("tag", SEIT("sn_penrose_coat", 1)), "village_piazza", "danzel", ["sophia"],
        "Danzel has carried his low box out to the good window of Le Théâtre Rouge. Sophia stands on it in the camel coat, with the belt tied, the hat tilted and a pencil behind her ear. He is kneeling at the hem, and for once he isn't performing. Her long hair has gone. You look again, and it's a short, glossy wave, pinned flat on one side.",
        [S_("danzel", "Stand still, please. This cloth is eighty years old and it is better than anything I will ever make, so I took it apart slowly and I built it again around you. [clear throat] The left shoulder is new. I don't think you can tell.", "caring"),
         S_("sophia", "Don't stare, darling, it's all still there under the pins. [chuckle] In London I learned to make long hair look short in ninety seconds in the dark, in case somebody fell ill before the second act. Nobody ever did.", "approval"),
         S_("danzel", "Everything I make has a small label inside the collar, with one name on it. [clear throat] I always leave that until last. What do I stitch?", "neutral"),
         S_("sophia", "He's asking you as well, Duc, and you've read the letters. [sigh] Which name should go in the coat?", "approval")],
        [O("“M. J. Penrose. She wrote the book, so let her wear the coat.”", [F("ol_name_penrose"), FD("ol_etikett"), F("sn_penrose_coat_fertig"), V("danzel", 4)],
           zeile=S_("sophia", "Yes. [sigh] She's braver than I am, and she has nothing to lose. Stitch it, Danzel.", "neutral")),
         O("“Sophia Moore. That's the name you want on a book cover, isn't it?”", [F("ol_name_moore"), FD("ol_etikett"), F("sn_penrose_coat_fertig"), V("danzel", 4)],
           zeile=S_("sophia", "You don't make things easy, do you? [sniff] …Stitch it before I change my mind.", "love")),
         O("“Leave it empty. You'll know when you're standing up there.”", [F("ol_name_leer"), FD("ol_etikett"), F("sn_penrose_coat_fertig"), V("danzel", 4)],
           zeile=S_("sophia", "That is the worst thing anyone has ever said to an actress. [chuckle] …Leave it empty, Danzel.", "approval"))],
        {"danzel": "danzel_B", "sophia": READING}),
]

# ------------------------------------------------------------------ 4 Anlass
_RUF = [S_("alva", "I've got people standing on the piazza, Sophia, [chuckle] and they're asking me to open the windows.", "joy", gruppe="ruf", wenn={"wert": ["ruf", ">=", 4]}),
        S_("alva", "Every chair is gone, Sophia, [chuckle] and I've given Totò a crate.", "amusement", gruppe="ruf", wenn={"wert": ["ruf", ">=", 2]}),
        S_("alva", "Six people, Sophia, and one of them is the priest, [chuckle] so I'm counting him twice.", "amusement", gruppe="ruf")]
_VARIANTEN = {
    "penrose": ("“You're on, Miss Penrose.”", "She walks to the counter and lays down her pages. Every face in the bar turns to her.",
                [S_("sophia", "Good evening. My name is M. J. Penrose. [chuckle] I don't exist, so please don't ask for your money back.", "neutral")]),
    "moore": ("“You're on, Miss Moore.”", "She walks to the counter and lays down her pages. Every face in the bar turns to her.",
              [S_("sophia", "Good evening. You all know me, because I've got you your tables and lied to you about the weather. [clear throat] My name is Sophia Moore, and I've been writing at night for years. I'd like to read you something.", "neutral")]),
    "leer": ("“You're on.”", "She walks to the counter and stands there. She takes the pencil from behind her ear and looks at it. Nobody in this room has ever seen her without a line ready.",
             [S_("sophia", "My name is… [sigh] My name is Sophia Moore. M. J. Penrose sends her apologies.", "neutral")]),
}
_VIKAR = "The vicar had been dead since Tuesday, [clear throat] which explained the marmalade."


def _tuer(name):
    an_tuer, lage, zeilen = _VARIANTEN[name]
    return [
        TAKT("ol_tuer_" + name, "wholesome", "You're On", WP("abend", {"flag": "ol_name_" + name}, SEIT("ol_etikett", 1), SEIT("ol_wunsch", 3)),
             "alvas_bar", "sophia",
             "The storeroom behind Alva's bar smells of diesel and old lemons. Through the door you can hear chairs and glasses and people talking. Sophia is standing very straight in the camel coat, holding three pages, and the pages are shaking.",
             _RUF + [S_("sophia", "Two years, Duc. [sigh] Every single night there was a young man with a clipboard who came along the corridor to say it to the others, and he walked straight past me.", "neutral"),
                     S_("sophia", "I'd like somebody to say it to me, just once. [clear throat] Would you mind?", "gratitude")],
             [O("Opens the door. " + an_tuer, [FD("ol_lesung"), DIREKT("ol_auftritt_" + name)])],
             {"sophia": READING, "alva": "alva_standard"}),
        TAKT("ol_auftritt_" + name, "wholesome", "You're On", FRAME(), "alvas_bar", "sophia",
             "She takes one breath, and the pages stop shaking. She walks past you, and she doesn't look back. " + lage,
             zeilen + [S_("sophia", _VIKAR, "neutral")],
             [O("Waits.", [DIREKT("ol_stille")])],
             {"sophia": READING}),
    ]


FREMD = lambda pid: {"nicht": {"flag": "gefeuert_" + pid}}
ANLASS = [e for n in _VARIANTEN for e in _tuer(n)] + [
    TAKT("ol_stille", "ernst", "You're On", FRAME(), "alvas_bar", "sophia",
         "Nobody laughs. Her voice was too thin, and the back of the room didn't hear the line. A chair creaks. Somebody asks Alva for more wine. The pages have started shaking again, and Sophia looks down at them and can't find her place. Then she looks up, across the whole bar, at you.",
         [S_("sophia", "I'm so sorry. [clear throat] I seem to have lost my place. Where was I?", "confusion")],
         [O("Nods once, and doesn't look away.", [V("sophia", 4), DIREKT("ol_kipp")],
            zeile=S_("sophia", "Yes. [sigh] Thank you. I was at the marmalade, wasn't I?", "gratitude")),
          O("Calls across the room. “The vicar had been dead since Tuesday!”", [B("sophia", 4), DIREKT("ol_kipp")],
            zeile=S_("sophia", "[laugh] So he had, darling, thank you. Would anybody else like to read?", "gratitude")),
          O("Stands still and says nothing.", [V("sophia", 6), DIREKT("ol_kipp")],
            zeile=S_("sophia", "No. You're quite right. [sigh] Nobody is coming to help me, and I think that's rather the point of going on.", "neutral"))],
         {"sophia": READING}),
    TAKT("ol_kipp", "witzig", "You're On", FRAME(), "alvas_bar", "sophia",
        "She takes a breath and reads the line again, louder, and this time she makes them wait for the last word. Don Anghjulu laughs so hard that he has to put down his glass. After that, the whole room is hers. You have watched her work a room a hundred times, but she has never done it like this, because she isn't asking anybody for anything.",
        [S_("sophia", "Mrs Trelawney from the post office found him in the church that morning, sitting very straight, with a spoon in his hand. [clear throat] She said good morning to him twice, because she had been brought up properly.", "approval"),
         S_("anghjulu", "A spoon! [chuckle] No priest eats marmalade with a spoon. God sees everything, and this woman knows my profession.", "amusement"),
         S_("sophia", "Three people in the village had wanted the vicar dead for years. [chuckle] All three of them brought a cake to his funeral, and all three cakes were very good.", "approval"),
         S_("toto", "Two to one on the cakes! [laugh] Comandante, I'm taking bets. Two to one on the lady from the post office!", "joy"),
         S_("batu", "It's the cook. [sniff] It's always the one who feeds everybody, because nobody looks at her.", "neutral"),
         S_("sophia", "Nobody looked at Mrs Pascoe either, who had made all three cakes. [clear throat] She had been waiting for this funeral since Easter.", "approval")],
        [O("Puts five euros on Mrs Pascoe.", [G(-5), DIREKT("ol_reaktion")],
           zeile=S_("toto", "[chuckle] Five on the cook! The Comandante reads people. I'm already sorry I asked.", "amusement")),
         O("Tells Totò to be quiet, and keeps listening.", [DIREKT("ol_reaktion")],
           zeile=S_("toto", "[sniff] Comandante. I'm quiet. Look how quiet I am. It's still two to one.", "embarrassment"))],
        {"sophia": READING, "anghjulu": "anghjulu_standard", "toto": "Standard", "batu": "batu_standard"}),
    TAKT("ol_reaktion", "wholesome", "You're On", FRAME(), "alvas_bar", "sophia",
        "She reads for twenty minutes more. Alva sells no wine at all, because nobody gets up. Near the end of the chapter Sophia slows down, and then she stops in the middle of a page and looks up. She isn't reading now.",
        [S_("sophia", "The last train has gone, and… [sigh] No. Forgive me, that isn't in the book. That's from something else.", "neutral"),
         S_("sophia", "That's the end of the chapter, I'm afraid. [clear throat] I'm told it's a good place to stop.", "approval"),
         S_("batu", "No. You can't stop there. [sniff] Who killed him? Sit down, eat something, and then read the next part.", "anger"),
         S_("anghjulu", "God sees everything, but He hasn't told me about the vicar. [chuckle] I would also like to know.", "amusement"),
         S_("sophia", "Did you hear that, Duc? She wants to know what happens next. [sniff] Fifteen letters, and not one of them ever wanted to know that.", "joy"),
         S_("sophia", "Give me that receipt, Auntie Tu. [chuckle] I've got a pen with my own name on it, and I've never had anything to sign.", "joy", gruppe="stift", wenn={"item": "sophia_fueller"})],
        [O("Stands up and claps with everyone else.", [V("sophia", 4), DIREKT("ol_tresen")]),
         O("Doesn't clap, and just looks at her until she looks back.", [B("sophia", 4), DIREKT("ol_tresen")])],
        {"sophia": READING, "anghjulu": "anghjulu_standard", "batu": "batu_standard"}),
    TAKT("ol_tresen", "wholesome", "You're On", FRAME(), "alvas_bar", "sophia",
        "Later, at the counter. The crew came ashore for the wine and stayed for the vicar, and now they've got Sophia cornered.",
        [S_("chiara", "Eight and a half. No, nine. You've lived next to me for four seasons, and you wrote three books? [laugh] I want every one of them, and I'm going to be so loud about this.", "surprise", gruppe="chiara", wenn=FREMD("chiara")),
         S_("lea", "You always had ink on your chin in the mornings. I thought it was from doing the bills. [sniff] Did you know that a vicar – no, sorry. I'm just proper proud of you, that's all.", "love", gruppe="lea", wenn=FREMD("lea"))],
        [O("Raises a glass to them.", [W("ruf", 2), V("sophia", 6), FD("ol_erledigt"),
                                       FAKT("sophia", "Sophia read from her detective novel at Alva's bar, in Penrose's camel coat. Now the whole crew and the village know that she writes.")]),
         O("Leaves them to it, and lets them have her for the night.", [W("ruf", 2), V("sophia", 6), FD("ol_erledigt"),
                                                                        FAKT("sophia", "Sophia read from her detective novel at Alva's bar, in Penrose's camel coat. Now the whole crew and the village know that she writes.")])],
        {"chiara": "Harbor Night", "lea": "Off Duty", "sophia": READING}),
]

# ------------------------------------------------------------------ 5 Echo
ECHO = [
    TAKT("ol_echo", "wholesome", "Ten Euros", WP("fruehstueck", SEIT("ol_lesung", 1)), "crew_mess", "sophia",
         "Breakfast, the morning after the reading at Alva's bar. Sophia is back in her uniform, with her hair up, and she sits down next to you without being asked.",
         [S_("sophia", "You'll want your ten euros, from when you bet me at Alva's that I'd go through with it. [chuckle] But I was sick in her storeroom about a minute before you got there, darling, so strictly speaking I won.", "amusement", gruppe="wette", wenn={"flag": "ol_wette"}),
          S_("sophia", "I was sick in Alva's storeroom before the reading, you know, about a minute before you got there. [chuckle] I thought somebody ought to have it in writing.", "amusement", gruppe="wette"),
          S_("sophia", "I never did find out what it's like to go on in that play. [sigh] I'll tell you what, though, I find I don't mind at all.", "caring")],
         [O("Just smiles.", [])],
         {"sophia": "Concierge"}),
    GAG("ol_dorf", "witzig", "The Talk of the Piazza", WP("tag", SEIT("ol_lesung", 1)), "village_piazza", "toto", ["mina", "alva"],
        "The morning after the reading, nobody on the piazza is talking about anything else.",
        [S_("toto", "Comandante, I'm telling everyone that coat was mine. [chuckle] Nobody has to know about the cards.", "amusement"),
         S_("mina", "There's a letter for M. J. Penrose at the post office again. [clear throat] I've been wondering who that was for years, you know. I've only been wondering, of course.", "curiosity"),
         S_("alva", "Best quiet night I ever had. [chuckle] Tell her that she drinks free, once.", "joy")],
        [O("Says he'll tell her.", [V("alva", 4)]),
         O("“Once? After that crowd?”", [],
           zeile=S_("alva", "Once. [chuckle] I'm grateful, I'm not stupid.", "amusement"))],
        {"toto": "Standard", "mina": "mina_standard", "alva": "alva_standard"}),
]

EVENTS = WUNSCH + MATERIAL + ANPROBE + ANLASS + ECHO


def tags_schreiben():
    pfad = os.path.join(EDEN, "module", "eden_rise", "stimme_tags.json")
    d = json.load(open(pfad, encoding="utf-8"))
    neu = [{"wer": w, "text": t, "gesprochen": g, "quelle": "outfit_quest"} for w, t, g in _TAGS]
    texte = {z["text"] for z in neu}
    d["zeilen"] = [z for z in d["zeilen"] if z.get("quelle") != "outfit_quest" and z["text"] not in texte] + neu
    json.dump(d, open(pfad, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return len(neu)
