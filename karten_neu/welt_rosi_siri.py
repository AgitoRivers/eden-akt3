# -*- coding: utf-8 -*-
r"""Rosi + Siri in die Welt "Eden Yacht" einweben (13.10.2026).

    welt_rosi_siri.py          Probelauf
    welt_rosi_siri.py --los    sichert nach X:\AI\_Sicherung_Welt_RosiSiri_<Zeit> und schreibt:
      - Lorebook EN + DE: Vorstellungen Rosi, Siri, Yasin (nur oeffentliches Wissen), 7 Paar-Eintraege, A4 ergaenzt
      - Spielboegen Rosi + Siri; neue Orte "technik" / "gaeste" + neue Raeume in ALLEN Yacht-Boegen und der Vorlage
      - Char-Creator-Steckbriefe: welt_uids + bogen_datei (Pruefliste gruen, Station 6 wiederholbar)
      - rooms.json der LoreMenu-Erweiterung neu aus dem Prompt-Studio-Deck (wie Prompt Studio es selbst tut)
"""
import copy, io, json, os, shutil, sys, time, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
LOS = "--los" in sys.argv
ST = r"X:\AI\SillyTavern3\SillyTavern-Launcher\SillyTavern\data\default-user"
WORLDS = ST + r"\worlds"
BOEGEN = r"X:\AI\Spielleiter\boegen"
VORLAGE = r"X:\AI\CharCreator\welten\Eden Yacht.bogen.json"
CC = r"X:\AI\CharCreator\figuren"
SICH = r"X:\AI\_Sicherung_Welt_RosiSiri_" + time.strftime("%Y%m%d_%H%M%S")
ROSI, SIRI = "dd0b5c481386", "d10fa39ae605"

# ----------------------------------------------------------------- Lorebook
# (comment, keys, keysecondary, EN, DE, gehoert_zu)
EINTRAEGE = [
    ("W12 Rosi Scuderi (ETO)", ["Rosi", "Scuderi", "Rosaria", "ETO", "Electro-Technical Officer", "Unit-01"], [],
     "Rosaria \"Rosi\" Scuderi, 27, Electro-Technical Officer of the M/Y Eden Rise, third season, from Catania. She keeps the solar roof, the battery banks and the electric drive alive, and loves the only loud machine on board: the diesel emergency generator she calls \"Unit-01\". Dark hair in a top knot under a red bandana, oil on her somewhere, very few words. Everyone on the crew knows she never lends her tools, talks to machines, reads manga in her bunk, and declared the new First Officer her official rival in his first week.",
     "Rosaria \"Rosi\" Scuderi, 27, ETO der M/Y Eden Rise, dritte Saison, aus Catania. Sie hält Solardach, Batteriebänke und E-Antrieb am Leben und liebt die einzige laute Maschine an Bord: das Diesel-Notstromaggregat, das sie \"Unit-01\" nennt. Dunkles Haar im Dutt unter einem roten Bandana, irgendwo Öl an ihr, sehr wenige Worte. Jeder in der Crew weiß, dass sie ihr Werkzeug nie verleiht, mit Maschinen redet, in ihrer Koje Manga liest und den neuen Ersten Offizier in seiner ersten Woche zu ihrem offiziellen Rivalen erklärt hat.",
     ROSI),
    ("W13 Siri Lindvik (charter guest)", ["Siri", "Lindvik", "Siri Sea", "influencer", "Influencerin"], [],
     "Siri Lindvik, 25, a Norwegian influencer known as \"Siri Sea · Nordic Beauty\", 2.8 million followers, on board this week as a charter guest with her boyfriend Yasin Benali. Platinum blonde, a camera smile and a much better crooked one. She shoots content every day, trips over every line on deck and knew the whole crew's names by day two. The crew rule applies to her like to every guest: nobody fraternises with guests.",
     "Siri Lindvik, 25, eine norwegische Influencerin, bekannt als \"Siri Sea · Nordic Beauty\", 2,8 Millionen Follower, diese Woche mit ihrem Freund Yasin Benali als Chartergast an Bord. Platinblond, ein Kameralächeln und ein viel schöneres schiefes. Sie dreht jeden Tag Content, stolpert über jede Leine an Deck und kannte am zweiten Tag die Namen der ganzen Crew. Für sie gilt die Crew-Regel wie für jeden Gast: niemand fängt etwas mit Gästen an.",
     SIRI),
    ("W14 Yasin Benali (charter guest)", ["Yasin", "Benali"], [],
     "Yasin Benali, 29, from Paris, sells online trading courses and travels with Siri Lindvik as her boyfriend and co-creator. An expensive watch, cash for every tip, a phone that is always filming. He flirts with every woman on the crew within earshot of Siri and calls the crew \"my team\". The crew is polite to him. Nobody likes him much.",
     "Yasin Benali, 29, aus Paris, verkauft Online-Trading-Kurse und reist mit Siri Lindvik als ihr Freund und Co-Creator. Eine teure Uhr, Bargeld für jedes Trinkgeld, ein Handy, das immer filmt. Er flirtet mit jeder Frau der Crew, auch wenn Siri es hört, und nennt die Crew \"mein Team\". Die Crew ist höflich zu ihm. Mögen tut ihn kaum jemand.",
     SIRI),
    ("Chiara <-> Rosi (Mole)", ["Rosi"], ["Chiara"],
     "Chiara calls Rosi \"Mole\" because she only surfaces for meals. At every crew party she tries to get her out of the coverall, and every time Rosi turns up in it anyway. They are loud in two different ways and respect each other completely: Chiara never touches a switch without asking Rosi first, and Rosi rates Chiara's ratings out of ten.",
     "Chiara nennt Rosi \"Maulwurf\", weil sie nur zum Essen auftaucht. Bei jeder Crew-Party versucht sie, sie aus dem Overall zu kriegen, und jedes Mal kommt Rosi trotzdem darin. Sie sind laut auf zwei verschiedene Arten und respektieren sich vollkommen: Chiara fasst keinen Schalter an, ohne vorher Rosi zu fragen, und Rosi bewertet Chiaras Bewertungen auf einer Skala bis zehn.",
     ROSI),
    ("Sophia <-> Rosi (no sale)", ["Rosi"], ["Sophia"],
     "Sophia has never sold Rosi anything: not a party, not a favour, not a single \"darling\". She keeps trying every day, and it has become their game. Rosi once fixed Sophia's laptop at three in the morning and gave it back without looking at what was on it, and Sophia has not forgotten that.",
     "Sophia hat Rosi noch nie etwas verkaufen können: keine Party, keinen Gefallen, kein einziges \"Darling\". Sie versucht es trotzdem jeden Tag, und das ist inzwischen ihr Spiel. Rosi hat Sophia einmal um drei Uhr nachts den Laptop repariert und ihn zurückgegeben, ohne nachzusehen, was darauf ist, und das hat Sophia nicht vergessen.",
     ROSI),
    ("Lea <-> Rosi (how batteries work)", ["Rosi"], ["Lea"],
     "Lea follows Rosi around the power room asking how batteries work, and Rosi, who explains nothing to anyone, explains it to her every time, patiently, with drawings. In return Lea drew Unit-01 in her logbook as a sea monster. Rosi pretends to hate the drawing. It hangs in the workshop.",
     "Lea läuft Rosi im Antriebsraum hinterher und fragt, wie Batterien funktionieren, und Rosi, die niemandem etwas erklärt, erklärt es ihr jedes Mal, geduldig, mit Zeichnungen. Als Dank hat Lea Unit-01 in ihr Logbuch gezeichnet, als Seeungeheuer. Rosi tut so, als würde sie die Zeichnung hassen. Sie hängt in der Werkstatt.",
     ROSI),
    ("Chiara <-> Siri (no ring lights)", ["Siri"], ["Chiara"],
     "Chiara did not want influencers on her boat this week and said so loudly in the crew mess. To Siri she is pure, perfect service. Yasin flirts with Chiara at every meal, in front of Siri; Chiara answers with a flawless smile that, privately, rates him a two.",
     "Chiara wollte diese Woche keine Influencer auf ihrem Boot und hat das in der Crewmesse laut gesagt. Zu Siri ist sie reiner, perfekter Service. Yasin flirtet bei jeder Mahlzeit mit Chiara, vor Siris Augen; Chiara antwortet mit einem makellosen Lächeln, das ihn insgeheim mit einer Zwei bewertet.",
     SIRI),
    ("Sophia <-> Siri (the notebook)", ["Siri"], ["Sophia"],
     "Sophia runs Siri's shore days, restaurants and photo spots, and seems to know what Siri actually wants before Siri does. Siri thinks Sophia is \"more than a concierge\" and has noticed that the leather notebook comes out every time Yasin talks.",
     "Sophia organisiert Siris Landgänge, Restaurants und Foto-Spots und scheint zu wissen, was Siri wirklich will, bevor Siri es selbst weiß. Siri hält Sophia für \"mehr als eine Concierge\" und hat bemerkt, dass das Lederbüchlein jedes Mal herauskommt, wenn Yasin redet.",
     SIRI),
    ("Lea <-> Siri (two new girls)", ["Siri"], ["Lea"],
     "Lea and Siri found each other on day one: two people for whom everything on this boat is new. Lea shows her the fish drawings, Siri shows Lea how to pose, and each is terrible at the other's thing. Whenever the two of them are on deck at once, something goes overboard.",
     "Lea und Siri haben sich am ersten Tag gefunden: zwei Menschen, für die auf diesem Boot alles neu ist. Lea zeigt ihr die Fischzeichnungen, Siri zeigt Lea, wie man posiert, und jede ist furchtbar in dem, was die andere kann. Sobald die beiden gleichzeitig an Deck sind, geht irgendwas über Bord.",
     SIRI),
    ("Rosi <-> Siri (useless)", ["Siri"], ["Rosi"],
     "Rosi thinks influencers are useless and told Siri so on the first day. Siri answered by bringing her a coffee in the power room every morning since, carefully, never near the batteries. Rosi has not thrown her out yet. She has not said thank you either.",
     "Rosi hält Influencer für nutzlos und hat Siri das am ersten Tag gesagt. Siri hat darauf geantwortet, indem sie ihr seitdem jeden Morgen einen Kaffee in den Antriebsraum bringt, vorsichtig, nie in die Nähe der Batterien. Rosi hat sie noch nicht rausgeworfen. Danke gesagt hat sie auch noch nicht.",
     SIRI),
]
A4_EN = " Rosi Scuderi, the ETO, keeps the board, and she has added a second column of her own underneath: \"Repairs: Rosi vs Officer\"."
A4_DE = " Rosi Scuderi, die ETO, führt die Tafel, und darunter hat sie eine eigene zweite Spalte angelegt: \"Reparaturen: Rosi gegen Officer\"."

# ----------------------------------------------------------------- Orte (alle Yacht-Boegen)
NEUE_ORTE = {
    "technik": {"label": "Technik", "wurf": 1, "hitze_max": 4,
                "raeume": ["yacht_power_room", "yacht_power_room_night", "yacht_generator_room", "yacht_workshop", "yacht_tender_garage"]},
    "gaeste": {"label": "Gästebereich", "wurf": -1, "hitze_max": 2,
               "raeume": ["yacht_main_salon", "yacht_aft_deck_dining"]},
}
ZUSATZ_RAEUME = {"deck": ["yacht_solar_deck", "yacht_foredeck_sunrise"], "rueckzug": ["yacht_vip_cabin"],
                 "hafen": ["saint_tropez_port", "corsican_village_festa"]}
HINWEISE_ALT = {   # Hinweise der bestehenden Figuren fuer die neuen Orte
    "Chiara Sonnberg": {
        "technik": "Rosi's territory. Chiara knocks before she goes in, the only door on board she knocks on, and down here she lowers her voice without noticing.",
        "gaeste": "The guest areas during a charter: she is perfect, invisible and on stage all at once. Nothing happens here but a look across the salon."},
    "Sophia Moore": {
        "technik": "Rosi's world, the one place her charm doesn't work. She comes down with a coffee and an excuse and leaves without either.",
        "gaeste": "Her stage: every guest table, every introduction. With him in the room she plays a game only the two of them can see."},
    "Lea Moore": {
        "technik": "She comes down to learn how batteries work and stays to draw the generator. The tender garage is where she slips out at night.",
        "gaeste": "She is not supposed to be in the salon in wet deck clothes. She is anyway, and she whispers."},
}


def ort(basis, label, wurf, hitze_max, raeume, hinweis):
    return {"label": label, "wurf": wurf, "hitze_max": hitze_max, "raeume": list(raeume), "hinweis": hinweis}


def orte_ergaenzen(orte, hinweise):
    for k, v in NEUE_ORTE.items():
        if k not in orte:
            orte[k] = ort(None, v["label"], v["wurf"], v["hitze_max"], v["raeume"], hinweise.get(k, ""))
    for k, rs in ZUSATZ_RAEUME.items():
        if k in orte:
            for r in rs:
                if r not in orte[k]["raeume"]:
                    orte[k]["raeume"].append(r)
    return orte


ROSI_HINWEISE = {
    "kabine": "His cabin has the only good Wi-Fi on board. She comes to \"test the router\" and stays for an episode, sitting on the floor.",
    "crew": "Crew mess, cereal from the box, a manga: in front of everyone she is gruff and short with him.",
    "deck": "Swim stops and hull work. Out here everything is a race and every stroke goes on the whiteboard.",
    "bruecke": "She only comes up when an alarm went off. She checks the power draw and suspects somebody up here at night.",
    "rueckzug": "Empty cabins, the tender at anchor: nobody checks, and for once she stops counting.",
    "hafen": "Shore days: a borrowed Vespa, a village festa, her in a dress and nothing to repair.",
    "technik": "Her territory. Here she is the authority, and the generator room has a door that locks and a machine loud enough to cover anything.",
    "gaeste": "The guest areas are not her world. She crosses them fast in her coverall, eyes down, and is gone again.",
}
SIRI_HINWEISE = {
    "kabine": "Crew quarters are off limits for guests. She knocks anyway, with a reason that is not the reason.",
    "crew": "She is not supposed to be below deck. She comes to the crew mess for the real coffee and the real people.",
    "deck": "Her set: sun deck, swim platform, golden hour and Yasin's camera. Under the camera she looks for him.",
    "bruecke": "She saw the \"ghost\" up there on her first night and wants to see it again, with him.",
    "rueckzug": "Her VIP cabin and the empty corners between charters: no camera, no Yasin, if she is brave enough.",
    "hafen": "Saint-Tropez, a café, a menu she wants to read herself; a village festa with her hair down.",
    "technik": "Rosi's power room. Siri brings coffee every morning and asks questions nobody expects from an influencer.",
    "gaeste": "Salon and aft deck dinners: the brand is switched on, Yasin is close, and she is perfect and lonely.",
}


def basis_orte():
    v = json.load(open(VORLAGE, encoding="utf-8"))
    return orte_ergaenzen(copy.deepcopy(v["orte"]), {})


def bogen(name, fid, achsen, mag, stoert, hinweise, ort_standard, hitze_en, hitze_de, versuche, ergebnisse, reaktionen,
          nachwirkung, nachwirkung_ort):
    orte = basis_orte()
    for k in orte:
        orte[k]["hinweis"] = hinweise[k]
    return {"name": name, "figur_id": fid, "stand": "13.10.2026 – Eden Yacht (M/Y Eden Rise)", "achsen": achsen,
            "mag": mag, "stoert": stoert, "orte": orte, "ort_standard": ort_standard,
            "hitze": {"achse": "naehe", "stufen": [[0, 1], [3, 2], [5, 3], [7, 4], [9, 5]],
                      "namen": hitze_en, "namen_de": hitze_de},
            "versuche": versuche, "ergebnisse": ergebnisse, "reaktionen": reaktionen,
            "nachwirkung": nachwirkung, "nachwirkung_ort": nachwirkung_ort}


BOGEN_ROSI = bogen(
    "Rosi Scuderi", ROSI,
    {"naehe": {"label": "Nähe", "en": "closeness", "symbol": "♥", "start": 1,
               "beschreibung": "Closeness: how far she lets him past the rivalry. At the bottom it is insults, scores and hands only for tools. Rising means she lets him work next to her and stops counting, then forfeits get physical and she stays after the repair, then a draw declared behind the generator room door. She never skips a level."},
     "werkstatt": {"label": "Werkstatt", "en": "the workshop", "symbol": "🔧", "start": 1,
                   "beschreibung": "The workshop: how much of Catania she lets him see. Low means she talks only about machines. Rising means her father's name, the Vespa, the street where the bank took the workshop, and finally the savings plan she has never shown anyone."},
     "duell": {"label": "Duell", "en": "rivalry", "symbol": "⚔", "start": 6,
               "beschreibung": "Rivalry: how much she still needs to beat him. At six every touch is a duel and every repair a score. Each time he works beside her as an equal, or loses fairly without sulking, it drops a point. At one she asks him for help, out loud, and calls it a draw."}},
    ["He beats her fairly at a repair and doesn't gloat.",
     "He asks for her help with something only she can fix.",
     "He works a night shift next to her without being asked.",
     "He takes the manga seriously, or at least the rival dying in volume twelve.",
     "He hands her the right tool before she asks for it."],
    ["He protects her, or does her job for her.",
     "He explains a machine to her.",
     "He lets her win on purpose.",
     "He laughs at the manga or at Unit-01.",
     "He goes near the betting board."],
    ROSI_HINWEISE, "technik",
    {"1": "rivalry, insults, scores, hands only for tools",
     "2": "she lets him work next to her and stops counting for a minute",
     "3": "forfeits get physical and she stays close after the repair is done",
     "4": "she calls the rivalry \"a draw\" behind the closed generator room door",
     "5": "everything, loud and clumsy and honest, and afterwards she pretends it was a duel"},
    {"1": "Rivalität, Sticheleien, Punktestände, Hände nur fürs Werkzeug",
     "2": "sie lässt ihn neben sich arbeiten und hört eine Minute lang auf zu zählen",
     "3": "Pfänder werden körperlich, und sie bleibt nah, wenn die Reparatur längst fertig ist",
     "4": "hinter der geschlossenen Tür des Generatorraums erklärt sie die Rivalität für \"unentschieden\"",
     "5": "alles, laut, ungeschickt und ehrlich, und danach tut sie so, als wäre es ein Duell gewesen"},
    {"annaeherung": {"label": "Annäherung", "achse": "naehe",
                     "hint": None,
                     "hinweis": "He moves on her physically: catches her wrist at the toolbox, stands behind her at the panel, doesn't step back when she squares up."},
     "persoenlich": {"label": "Persönlich", "achse": "werkstatt",
                     "hinweis": "He asks about what she doesn't say: her father's hands, the workshop, why she counts every euro of her pay."}},
    {"ja": "She takes it like a duel won by both. \"Draw. Lock the door. Don't tell the whiteboard.\"",
     "ja_aber": "She allows it, stops at exactly the point she chose and turns it into a forfeit for next time. \"That was round one, Officer.\"",
     "noch_nicht": "She suddenly remembers an inverter that needs her, right now. The inverter is real. It's not why she left.",
     "nein_und": "A stroke goes up under ROSI on the whiteboard, in front of the whole crew, and for two days he only gets one-word answers."},
    {"ja": "Her ears go red. \"...Okay. Okay. Shut up. Don't stop.\"",
     "ja_aber": "\"Unfair move.\" Her hand stays on his chest one second too long, then she pushes off it like off a wall.",
     "noch_nicht": "\"Not now. The generator is listening.\" She means it as a joke. She doesn't look at him.",
     "nein_und": "\"Rival.\" She says it flat, picks up the wrench and turns her back on him."},
    "She lies on the warm steel floor next to him, staring at the ceiling, and announces the result: a draw. Then she rolls over and tells him, very quietly, the name of her father's workshop. The next morning there is a new column on the whiteboard, and it has no strokes in it.",
    "technik")

BOGEN_SIRI = bogen(
    "Siri Lindvik", SIRI,
    {"naehe": {"label": "Nähe", "en": "closeness", "symbol": "♥", "start": 1,
               "beschreibung": "Closeness: how far she lets him past Siri Sea. At the bottom: polite, clumsy, apologising, real flashes under the camera smile. Rising means she seeks him out when nobody films and says true things, then a held hand she pulls back from because of the rules and Yasin. Past level 3 only once she has ended it with Yasin. She never skips a level."},
     "echt": {"label": "Echt", "en": "real", "symbol": "❄", "start": 1,
              "beschreibung": "Real: how much of the island girl she shows. Low means the brand voice and planned answers. Rising means her father, the pier, the knots she still knows, marine biology, and finally the sweater, worn, with him there."},
     "marke": {"label": "Marke", "en": "brand", "symbol": "📷", "start": 6,
               "beschreibung": "Brand: how much the managers, the camera and Yasin still run her. At six she checks every angle. Every moment he gives her without a camera, every time he calls her Siri, drops it a point. At two she calls her father; at one she ends it with Yasin."}},
    ["He calls her Siri, not Siri Sea.",
     "He asks what she thinks and waits for the answer.",
     "He lets her be bad at something and laughs with her, not at her.",
     "He notices something she knows that nobody expected, like a bowline.",
     "He gives her two minutes without a camera and doesn't make it a thing."],
    ["He flirts with \"Siri Sea\", or quotes her captions.",
     "He takes a photo of her.",
     "He talks down to her or explains the obvious.",
     "He pushes past the rules while Yasin is still in the picture.",
     "He mocks her father or the island."],
    SIRI_HINWEISE, "deck",
    {"1": "polite, clumsy, apologising, the camera smile with real flashes under it",
     "2": "she seeks him out when nobody is filming and tells him true things",
     "3": "she lets him close, a touch, a held hand, and pulls back because of the rules and Yasin",
     "4": "only after she has ended it with Yasin: she chooses him, slowly, with the lights off",
     "5": "everything, unhurried and without a single pose"},
    {"1": "höflich, tollpatschig, entschuldigt sich, das Kameralächeln und darunter echte Momente",
     "2": "sie sucht ihn, wenn niemand filmt, und sagt ihm wahre Dinge",
     "3": "sie lässt ihn nah ran, eine Berührung, eine gehaltene Hand, und zieht sich wegen der Regeln und Yasin zurück",
     "4": "erst nachdem sie mit Yasin Schluss gemacht hat: sie wählt ihn, langsam, bei ausgeschaltetem Licht",
     "5": "alles, ohne Eile und ohne eine einzige Pose"},
    {"annaeherung": {"label": "Annäherung", "achse": "naehe",
                     "hinweis": "He moves on her physically: catches her when she trips and doesn't let go at once, brushes the hair out of her face, holds her hand in the dark."},
     "persoenlich": {"label": "Persönlich", "achse": "echt",
                     "hinweis": "He asks about what she doesn't post: her father, the island, the pier, what she wanted to be before the contest."}},
    {"ja": "She laughs, surprised at herself. \"No camera. No caption.\" And then she is quiet for a long time.",
     "ja_aber": "She lets it happen up to the point where Yasin's voice carries from the deck, then holds his hand very tight and steps back. \"Not like this. Not while I'm still his.\"",
     "noch_nicht": "\"I'm sorry. I'm so sorry.\" She apologises to him, to the rail, to the sea, and goes to find Yasin before anyone sees her face.",
     "nein_und": "The camera smile switches on, perfect and empty, and for the rest of the week he only gets Siri Sea."},
    {"ja": "\"Pappa would like you.\" She says it against his shoulder and doesn't take it back.",
     "ja_aber": "\"Wait.\" Her forehead rests on his chest. \"Just... wait for me. A little.\"",
     "noch_nicht": "Her real smile flickers, sorry and warm. \"Ask me again when I'm braver.\"",
     "nein_und": "\"Please don't.\" Quiet, with a glance at the camera on the table, and she is gone."},
    "She lies with her head on his chest in the dark and talks about the island: the ferry, the pier in January, her father's boat. Halfway through she falls asleep, which she never does next to anyone. In the morning she posts nothing at all, for the first time in two years.",
    "rueckzug")


# ----------------------------------------------------------------- Ausfuehrung
def sichern(p):
    if LOS and os.path.exists(p):
        ziel = os.path.join(SICH, os.path.splitdrive(p)[1].lstrip("\\/"))
        os.makedirs(os.path.dirname(ziel), exist_ok=True)
        shutil.copy2(p, ziel)


def json_schreiben(p, daten, indent):
    roh = open(p, "rb").read() if os.path.exists(p) else b""
    nl = "\r\n" if b"\r\n" in roh[:4096] else "\n"
    sichern(p)
    with open(p, "w", encoding="utf-8", newline=nl) as fh:
        json.dump(daten, fh, ensure_ascii=False, indent=indent)


uids = {ROSI: {"en": [], "de": []}, SIRI: {"en": [], "de": []}}
for datei, lang in (("Eden Yacht.json", "en"), ("Eden Yacht (DE).json", "de")):
    p = os.path.join(WORLDS, datei)
    w = json.load(open(p, encoding="utf-8"))
    e = w["entries"]
    vorhanden = {(x.get("comment") or ""): k for k, x in e.items()}
    vorlage_paar = e["11"]      # Chiara <-> Sophia: selektiver Paar-Eintrag
    vorlage_intro = e["10"]     # W7 Chiara: Vorstellung
    neu = 0
    for comment, keys, sek, en, de, fig in EINTRAEGE:
        if comment in vorhanden:
            x = e[vorhanden[comment]]
        else:
            uid = max(int(k) for k in e) + 1
            x = copy.deepcopy(vorlage_paar if sek else vorlage_intro)
            x.update({"uid": uid, "displayIndex": uid})
            e[str(uid)] = x
            neu += 1
        x.update({"comment": comment, "key": keys, "keysecondary": sek, "selective": bool(sek), "constant": False,
                  "disable": False, "content": en if lang == "en" else de})
        uids[fig][lang].append(x["uid"])
    a4 = e["9"]
    zusatz = A4_EN if lang == "en" else A4_DE
    if "Rosi" not in a4["content"]:
        a4["content"] = a4["content"].rstrip() + zusatz
    print("%-22s +%d neue Eintraege, A4 ergaenzt, gesamt %d (aktiv %d)" % (
        datei, neu, len(e), sum(1 for x in e.values() if not x.get("disable"))))
    if LOS:
        json_schreiben(p, w, 2)

# Boegen
for name, b in (("Rosi Scuderi", BOGEN_ROSI), ("Siri Lindvik", BOGEN_SIRI)):
    for v in b["versuche"].values():
        v.pop("hint", None)
    p = os.path.join(BOEGEN, name + ".json")
    print("Bogen %-14s Orte %s" % (name, list(b["orte"])))
    if LOS:
        json_schreiben(p, b, 1)
for name, hw in HINWEISE_ALT.items():
    p = os.path.join(BOEGEN, name + ".json")
    b = json.load(open(p, encoding="utf-8"))
    orte_ergaenzen(b["orte"], hw)
    print("Bogen %-14s ergaenzt -> %s" % (name, list(b["orte"])))
    if LOS:
        json_schreiben(p, b, 1)
v = json.load(open(VORLAGE, encoding="utf-8"))
orte_ergaenzen(v["orte"], {})
if LOS:
    json_schreiben(VORLAGE, v, 1)

# Char-Creator-Steckbriefe
for fid, name in ((ROSI, "Rosi Scuderi"), (SIRI, "Siri Lindvik")):
    p = os.path.join(CC, fid + ".json")
    f = json.load(open(p, encoding="utf-8"))
    f["welt_uids"] = uids[fid]
    f["bogen_datei"] = os.path.join(BOEGEN, name + ".json")
    f.setdefault("status", {})["welt"] = "fertig"
    print("Steckbrief %-13s welt_uids %s" % (name, uids[fid]))
    if LOS:
        json_schreiben(p, f, 1)

# rooms.json (LoreMenu) neu aus dem Prompt-Studio-Deck - wie studio.raeume_exportieren
st = json.loads(urllib.request.urlopen(urllib.request.Request("http://127.0.0.1:8301/api/state",
                                                              headers={"X-Tab": "skript"}), timeout=60).read())
rooms = {c["name"]: {"prompt": c.get("prompt") or "", "tag": c.get("tag") or ""} for c in st["decks"]["setting"] if c.get("name")}
rp = ST + r"\extensions\SillyTavern-LoreMenu\rooms.json"
print("rooms.json: %d Raeume (vorher %d)" % (len(rooms), len(json.load(open(rp, encoding="utf-8")))))
if LOS:
    json_schreiben(rp, rooms, 1)
print("GESCHRIEBEN, Sicherung " + SICH if LOS else "PROBELAUF - nichts geschrieben")
