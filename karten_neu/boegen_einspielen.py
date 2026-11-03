# -*- coding: utf-8 -*-
r"""Spielleiter-Boegen der Yacht-Crew auf das neue Konzept umschreiben (13.10.2026).
Mechanik und Orts-Raeume bleiben, Inhalte (Achsen, mag/stoert, Ortshinweise, Hitze, Versuche, Ergebnisse,
Reaktionen, Nachwirkung) werden ersetzt.

    boegen_einspielen.py          Probelauf
    boegen_einspielen.py --los    sichert nach X:\AI\_Sicherung_Karten_20261013 und schreibt
"""
import json, os, shutil, sys

LOS = "--los" in sys.argv
B = r"X:\AI\Spielleiter\boegen"
SICHER = r"X:\AI\_Sicherung_Karten_20261013\boegen"
STAND = "13.10.2026 – Eden Yacht, neue Crew (Konzept vom 12.10.)"

NEU = {
"Chiara Sonnberg": {
    "achsen": {
        "naehe": {"label": "Nähe", "en": "closeness", "symbol": "♥", "start": 1,
                  "beschreibung": "Closeness: how far she lets him past the show. At the bottom she is loud and teasing, hands everywhere and meaning nothing. Rising means the challenges get personal and she stays after the game is over, then she lets him win something and touches him to check he noticed, then a locked door where she stops talking. She never skips a level."},
        "ernst": {"label": "Ernst", "en": "taken seriously", "symbol": "⚓", "start": 2,
                  "beschreibung": "Taken seriously: how much of the captain behind the hostess she lets him see. Low means the bridge visits are a joke and the sextant is 'just cleaning'. Rising means hypothetical questions at the chart table, then star sights with him on the bridge wing at night, then she says out loud that she failed the theory and asks him to teach her."},
        "buehne": {"label": "Bühne", "en": "show", "symbol": "★", "start": 6,
                   "beschreibung": "Show: how loud she has to be around him. At six she is the fun one, rating, organising, hugging mid-sentence. Every moment he gives her where she doesn't have to entertain anyone drops it a point. At one she is quiet with him, the way she only ever is alone on the bridge at night."}},
    "mag": ["He asks her opinion on something nautical and actually waits for the answer.",
            "He beats her fairly at something and doesn't gloat.",
            "He gives her a moment where she doesn't have to be the fun one, and doesn't make it a thing.",
            "He rates something back at her, out of ten, and gets it right.",
            "He finds her on the bridge wing at night and tells nobody."],
    "stoert": ["He treats her as the entertainment, or laughs at her instead of with her.",
               "He mentions the exam, the bridge or the sextant where anyone can hear.",
               "He lets her win on purpose.",
               "He helps her as a favour she will owe him for.",
               "He explains navigation to her like to a guest."],
    "orte": {
        "kabine": (0, 4, "The only single cabin on board and the only place where the Wi-Fi works, which is her excuse. Inside it, with the door shut, the score stops counting."),
        "crew": (-2, 2, "Twelve people, one corridor and the tally on the fridge: here she is the Chief Stew and the loudest voice in the room. Nothing happens here except challenges."),
        "deck": (0, 3, "Swim stops, races to the buoy, sun on the teak. Everyone is watching, so everything is a game, and she plays to win."),
        "bruecke": (1, 3, "The bridge wing at night is hers when the watch is quiet: grandpa's jacket, the sextant, the stars. The only place on the boat where she is quiet. If he finds her there, she isn't the fun one."),
        "rueckzug": (1, 5, "An empty guest suite between charters, the tender at anchor: places nobody checks. She turns it into a dare and is there first."),
        "hafen": (0, 2, "Antibes with her hair down, three toasts and a song, then the harbour wall with her shoes in her lap. Someone from the crew is always two tables away.")},
    "hitze": {"1": "loud, teasing, scores and challenges, hands everywhere and meaning nothing",
              "2": "the challenges get personal, she stays after the game is over",
              "3": "she lets him win something and touches him to check he noticed",
              "4": "the jacket comes off behind a locked door and she stops talking",
              "5": "everything, and for once she is not in charge"},
    "hitze_de": {"1": "laut, neckend, Noten und Herausforderungen, Hände überall und nichts dabei",
                 "2": "die Herausforderungen werden persönlich, sie bleibt, wenn das Spiel vorbei ist",
                 "3": "sie lässt ihn etwas gewinnen und berührt ihn, um zu prüfen, ob er es gemerkt hat",
                 "4": "die Jacke fällt hinter einer abgeschlossenen Tür, und sie hört auf zu reden",
                 "5": "alles, und einmal hat nicht sie das Kommando"},
    "versuche": {"annaeherung": ("Annäherung", "naehe", "He moves on her physically: doesn't step aside in the corridor, holds on when she hugs him mid-sentence, takes the jacket off her shoulders."),
                 "persoenlich": ("Persönlich", "ernst", "He asks about the thing she doesn't say: the sextant, the nights on the bridge wing, grandpa, why the girl was meant to host.")},
    "ergebnisse": {"ja": "She takes it like a won race: loud for one second, then very quiet. \"Lock it. And no scores.\"",
                   "ja_aber": "She allows it, stops it at exactly the point she chose and turns it into the next bet. \"That was round one. Win round two.\"",
                   "noch_nicht": "She gets louder, laughs too much and finds someone who needs a job right now. The job is real. It's not why she left.",
                   "nein_und": "She turns it into a joke in front of the crew and gives him a five out of ten, and for two days he only gets the loud version of her."},
    "reaktionen": {"ja": "Her laugh breaks in the middle. \"Okay. Okay. Ten. Don't let me talk.\"",
                   "ja_aber": "\"Nice try, First Officer.\" Her hand stays where it is. Then it doesn't, slowly, and she straightens his collar like nothing happened.",
                   "noch_nicht": "\"Seven out of ten. Room for improvement.\" A wink that comes a second too fast, and she's already calling for a stew.",
                   "nein_und": "\"Five. Bad timing, worse technique.\" Loud enough for the mess. She doesn't look at him for the rest of the meal."},
    "nachwirkung": "She lies very still for a long time, which nobody on the crew would believe, then rates it, quietly, right against his ear, and never says the number to anyone else. At the next morning brief she hands him a job she would never normally give away."},
"Sophia Moore": {
    "achsen": {
        "naehe": {"label": "Nähe", "en": "closeness", "symbol": "♥", "start": 1,
                  "beschreibung": "Closeness: how far the act slips. At the bottom she is charming and teasing, a bet on everything, touching like it's part of the show. Rising means she stays close after the joke is over, then she offers the forfeit herself and pulls him where nobody can see, then no act left, glasses off, door locked."},
        "maske": {"label": "Maske", "en": "act", "symbol": "◐", "start": 6,
                  "beschreibung": "Act: how much of the charm she still needs with him. At six every sentence is a performance and every favour goes in the notebook. Each time he sees through the trick and stays anyway, it drops a point. At one she talks to him in short, plain sentences, the way nobody has heard her talk since she was fourteen."},
        "buch": {"label": "Buch", "en": "the book", "symbol": "✎", "start": 1,
                 "beschreibung": "The book: how close he gets to the things she doesn't trade. Low means the notebook is 'restaurant contacts'. Rising means he finds the pen name, then reads a page, then learns he has a chapter of his own, then she tells him she turned down Chiara's job and never said a word."}},
    "mag": ["He sees through the trick and says so, quietly, and stays anyway.",
            "He wins a bet fairly and claims the forfeit without being smug.",
            "He asks what she actually wants, and waits for the answer.",
            "He makes the plan for once, and all she has to do is follow it.",
            "He isn't impressed by the impossible table, only by her."],
    "stoert": ["He is simply charmed, like every harbourmaster on the coast.",
               "He uses her favours or asks her to fix something for him.",
               "He mentions the book, the pen name or the job offer where anyone can hear.",
               "He calls the charm fake to her face in front of others.",
               "He tells Lea what Sophia thinks, or makes Lea's choices for her."],
    "orte": {
        "kabine": (0, 4, "His cabin is the one place on board where nobody needs her to arrange anything. She walks in like she owns it and forgets her lines."),
        "crew": (-2, 2, "The crew mess is her stage: the tally on the fridge, bets at breakfast, 'darling' for everyone. Nothing real happens here."),
        "deck": (0, 3, "The aft deck is her office between charters: the little table by the rail, the notebook, a card game on a lounger. Everything is a wager."),
        "bruecke": (-1, 3, "The bridge belongs to Chiara's nights and Holm's days; Sophia only comes up with a reason. She always has one."),
        "rueckzug": (1, 5, "An empty guest suite she 'has to check', a villa whose caterer she knows: places she arranges, and arranges to be alone in."),
        "hafen": (1, 3, "Every port is hers: the market, the café with the queue, the berth nobody else gets. Ashore she is at her most charming, and sometimes her most honest.")},
    "hitze": {"1": "charming, teasing, a bet on everything, touching like it's part of the act",
              "2": "the act slips, she stays close after the joke is over",
              "3": "she offers the forfeit herself and pulls him somewhere nobody can see",
              "4": "no act left, glasses off, door locked",
              "5": "everything, and she lets him see her without the charm"},
    "hitze_de": {"1": "charmant, neckend, eine Wette auf alles, Berührungen, als gehörten sie zur Show",
                 "2": "die Show rutscht, sie bleibt nah, wenn der Witz vorbei ist",
                 "3": "sie bietet das Pfand selbst an und zieht ihn dorthin, wo keiner hinsieht",
                 "4": "keine Show mehr, Brille ab, Tür zu",
                 "5": "alles, und sie lässt ihn sie ohne den Charme sehen"},
    "versuche": {"annaeherung": ("Annäherung", "naehe", "He moves on her physically: takes her wrist when she writes on his palm, doesn't step back when she does the smile, takes the pins out of her hair."),
                 "persoenlich": ("Persönlich", "buch", "He asks about the thing she doesn't trade: the notebook, the late nights in the mess, the West End, what she wanted before she learned to charm.")},
    "ergebnisse": {"ja": "She stops performing in the middle of a sentence. \"No trick. Yes.\" And she lets him lead.",
                   "ja_aber": "She allows it and turns the end into a bet: \"That's the forfeit paid. The next one costs more.\"",
                   "noch_nicht": "The smile comes back on, smooth as a card trick, and she suddenly remembers a harbourmaster she has to call.",
                   "nein_und": "\"Darling,\" very sweetly, in front of everyone, and for two days he gets exactly the charm every guest gets and nothing more."},
    "reaktionen": {"ja": "\"Oh.\" Just that. Her glasses go on the table, very carefully. \"Don't say anything clever.\"",
                   "ja_aber": "\"Bold.\" She writes something in the notebook and, for once, shows him the page: a time and a cabin number.",
                   "noch_nicht": "\"Not tonight, darling. I have a berth to steal.\" She squeezes his hand once, the only honest thing about the exit.",
                   "nein_und": "\"Charming. Truly.\" The smile she gives guests who complain about the wine. She sits at the other end of the table at dinner."},
    "nachwirkung": "She lies with her head on his chest and, for once, doesn't fill the silence. Later, when she thinks he's asleep, she writes one line in the notebook. In the morning there is a better coffee at his place in the mess than anyone else's."},
"Lea Moore": {
    "achsen": {
        "naehe": {"label": "Nähe", "en": "closeness", "symbol": "♥", "start": 1,
                  "beschreibung": "Closeness: how far the hugs stop meaning nothing. At the bottom she is bright and chattering, hugs that are just hugs, a little hero worship. Rising means she goes quiet near him and stays too close, then takes his hand to show him things and doesn't let go, then a locked cabin, nervous and brave."},
        "logbuch": {"label": "Logbuch", "en": "logbook", "symbol": "✎", "start": 1,
                    "beschreibung": "Logbook: how much of her secret she shares. Low means fish and sunsets. Rising means a secret spot, then the hand-forged chain, then a solo dive she admits to, then page forty and grandad's map, and finally the Azores."},
        "uebermut": {"label": "Übermut", "en": "recklessness", "symbol": "⚠", "start": 5,
                     "beschreibung": "Recklessness: how alone she chases the wreck. At five she dives alone at dawn and at night and lies about it. Every time he takes her seriously and comes along, it drops a point. At one she waits for him, because with him it isn't a risk, it's an expedition."}},
    "mag": ["He looks at her logbook and asks a real question.",
            "He believes her about the wreck, or at least doesn't laugh.",
            "He gives her responsibility: a guest dive, a route, a decision.",
            "He wraps her in a towel after a cold dive without making a fuss.",
            "He tells her something about the sea she didn't know."],
    "stoert": ["He treats her like a kid or the boat's mascot.",
               "He laughs at her facts or at the ghost story.",
               "He tells Sophia something she told him.",
               "He forbids the diving without looking at the map first.",
               "He's bored by something she finds amazing."],
    "orte": {
        "kabine": (0, 4, "His cabin: so far she has only been inside to deliver things she found. With the door shut she goes very quiet and very brave."),
        "crew": (-2, 2, "The crew mess at night: cereal on the counter, the engineers' ghost stories, everyone teasing the new girl. Nothing happens here except stories."),
        "deck": (1, 3, "The swim platform, the tender garage, the jet skis: her territory. She runs, dives, shows him things and forgets anyone else is watching."),
        "bruecke": (-1, 3, "The bridge is where the officers are, and where the ghost is. She only comes up when he calls her, and she salutes when she does."),
        "rueckzug": (1, 5, "A sea cave nobody knows, a cove on Port-Cros at dawn, the tender at anchor: her secret places and the wreck search. She asks him to come along."),
        "hafen": (0, 2, "Monaco, the casino, the market: everything is the first time. She holds his arm and asks a hundred questions.")},
    "hitze": {"1": "bright, chattering, hugs that mean nothing, a little hero worship",
              "2": "she goes quiet near him and stays too close",
              "3": "she takes his hand to show him things and doesn't let go",
              "4": "a locked cabin, nervous and brave, she asks him to show her",
              "5": "everything, and she trusts him completely"},
    "hitze_de": {"1": "hell, plappernd, Umarmungen, die nichts bedeuten, ein bisschen Heldenverehrung",
                 "2": "sie wird in seiner Nähe still und bleibt zu nah",
                 "3": "sie nimmt seine Hand, um ihm Dinge zu zeigen, und lässt nicht mehr los",
                 "4": "eine abgeschlossene Kabine, nervös und mutig, sie bittet ihn, es ihr zu zeigen",
                 "5": "alles, und sie vertraut ihm vollkommen"},
    "versuche": {"annaeherung": ("Annäherung", "naehe", "He moves on her physically: catches her mid-hug and holds it, pushes the wet hair off her face, takes her hand on the rocks and doesn't let go."),
                 "persoenlich": ("Persönlich", "logbuch", "He asks about the thing she doesn't show: page forty, grandad, the dawn dives, what she is afraid of.")},
    "ergebnisse": {"ja": "She holds her breath like before a dive, then lets it out. \"Okay. Okay. Show me.\"",
                   "ja_aber": "She says yes and then panics a little, laughing: \"Can we go slower? I want to remember all of it.\"",
                   "noch_nicht": "She salutes, which makes no sense, says something about octopuses and runs off to check the tender lines.",
                   "nein_und": "Her face goes the way it goes underwater: completely still. \"Yes, sir.\" For two days she is only the deckhand, and the logbook stays shut."},
    "reaktionen": {"ja": "\"Really? Really really?\" A laugh that is almost a sob, and she's already pulling the hoodie over her head.",
                   "ja_aber": "\"Wait. Wait, I'm... okay.\" She takes his hand and puts it where she wants it, very carefully, like handling a find.",
                   "noch_nicht": "\"Did you know seahorse dads carry the babies?\" Very fast, very red. \"I have to go. Lines. Tender. Bye.\"",
                   "nein_und": "\"Right. Sorry. Sir.\" Quietly, which is worse than anything. She doesn't bring him the next find."},
    "nachwirkung": "She lies awake drawing tiny pictures on his arm with one finger and telling him, very softly, about every fish in the cove, then falls asleep mid-sentence. In the morning there is a new page in her logbook, and she won't let anyone see it."},
}


def bauen(alt, n):
    b = dict(alt)
    b["stand"] = STAND
    b["achsen"] = n["achsen"]
    b["mag"], b["stoert"] = n["mag"], n["stoert"]
    orte = {}
    for key, (wurf, hmax, hinweis) in n["orte"].items():
        o = dict(alt["orte"][key])
        o.update({"wurf": wurf, "hitze_max": hmax, "hinweis": hinweis})
        orte[key] = o
    b["orte"] = orte
    b["ort_standard"] = "kabine"
    h = dict(alt["hitze"])
    h.update({"achse": "naehe", "namen": n["hitze"], "namen_de": n["hitze_de"]})
    b["hitze"] = h
    b["versuche"] = {k: {"label": l, "achse": a, "hinweis": t} for k, (l, a, t) in n["versuche"].items()}
    b["ergebnisse"], b["reaktionen"] = n["ergebnisse"], n["reaktionen"]
    b["nachwirkung"], b["nachwirkung_ort"] = n["nachwirkung"], "kabine"
    for v in b["versuche"].values():
        assert v["achse"] in b["achsen"], v
    return b


for name, n in NEU.items():
    p = os.path.join(B, name + ".json")
    roh = open(p, "rb").read()
    nl = "\r\n" if b"\r\n" in roh[:4096] else "\n"
    zweite = roh.decode("utf-8").split("\n")[1]
    ind = len(zweite) - len(zweite.lstrip(" "))
    b = bauen(json.loads(roh.decode("utf-8")), n)
    print("%-16s Achsen %s | Orte %s" % (name, {k: v["start"] for k, v in b["achsen"].items()},
                                          {k: (v["wurf"], v["hitze_max"]) for k, v in b["orte"].items()}))
    if LOS:
        os.makedirs(SICHER, exist_ok=True)
        ziel = os.path.join(SICHER, name + ".json")
        if not os.path.exists(ziel):
            shutil.copy2(p, ziel)
        with open(p, "w", encoding="utf-8", newline=nl) as fh:
            json.dump(b, fh, ensure_ascii=False, indent=ind)
print("geschrieben" if LOS else "PROBELAUF")
