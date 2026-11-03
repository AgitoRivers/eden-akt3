# -*- coding: utf-8 -*-
r"""Lorebooks "Eden Yacht" (EN) und "Eden Yacht (DE)" auf die neue Crew umstellen (13.10.2026).

Nur oeffentliches Wissen ins Lorebook - Geheimnisse (Chiaras Pruefung, Sophias Romane und das abgelehnte
Jobangebot, Leas Alleintauchgaenge und die Azoren) stehen ausschliesslich in der jeweiligen Karte (depth
prompt), sonst sickern sie in fremde Chats. Alte Eintraege werden ausgeschaltet, nicht geloescht.

    lorebook_einspielen.py          Probelauf
    lorebook_einspielen.py --los    sichert nach X:\AI\_Sicherung_Karten_20261013 und schreibt
"""
import copy, json, os, shutil, sys

LOS = "--los" in sys.argv
W = r"X:\AI\SillyTavern3\SillyTavern-Launcher\SillyTavern\data\default-user\worlds"
SICHER = r"X:\AI\_Sicherung_Karten_20261013\worlds"

AUS = [3, 6, 7, 13, 14, 15, 18, 19]          # Julien, Meldung, Saint-Tropez, Dubletten

# uid: (comment, keys oder None = unveraendert, EN, DE)
NEU = {
    0: ("W1 M/Y Eden (core)", None,
        "M/Y Eden is a 62-metre superyacht owned by the Eden group and chartered out every summer on the Riviera. Home port Antibes; the season runs from June to September: Saint-Tropez, Monaco, Portofino, Corsica, the islands off Hyeres. Twelve crew, up to twelve guests. Between charters the crew has the boat to themselves for a day or two. {{user}} joined mid-season in Antibes three weeks ago as the new First Officer, after the previous First Officer left for a command of his own. It is mid-August, with eight weeks of season left.",
        "M/Y Eden ist eine 62-Meter-Superyacht der Eden-Gruppe, die jeden Sommer an der Riviera verchartert wird. Heimathafen Antibes; die Saison läuft von Juni bis September: Saint-Tropez, Monaco, Portofino, Korsika, die Inseln vor Hyères. Zwölf Leute Crew, bis zu zwölf Gäste. Zwischen den Chartern gehört das Boot für ein, zwei Tage der Crew. {{user}} ist vor drei Wochen mitten in der Saison in Antibes als neuer Erster Offizier an Bord gekommen, nachdem der vorige Erste Offizier ein eigenes Kommando bekommen hat. Es ist Mitte August, noch acht Wochen Saison."),
    1: ("W2 Crew Life (core)", None,
        "Eden crew rules are simple: guests come first, nobody fraternises with guests, and during a charter the crew is invisible and perfect. Relationships between crew are not forbidden, but Captain Holm wants no drama on her boat and no noise after midnight. Between charters the Eden is loud and close: shared meals in the crew mess, swim stops, crew nights ashore, everyone knowing everyone's business by breakfast.",
        "Die Crew-Regeln der Eden sind einfach: Gäste zuerst, niemand fängt etwas mit Gästen an, und während eines Charters ist die Crew unsichtbar und perfekt. Beziehungen innerhalb der Crew sind nicht verboten, aber Kapitänin Holm will kein Drama auf ihrem Boot und keinen Lärm nach Mitternacht. Zwischen den Chartern ist die Eden laut und eng: gemeinsames Essen in der Crewmesse, Badestopps, Crew-Abende an Land, und beim Frühstück weiß jeder alles über jeden."),
    2: ("W3 Captain Marit Holm", None,
        "Captain Marit Holm, 56, Norwegian, thirty years at sea, the last eleven on Eden. Fair, dry, impossible to fool. She hired {{user}} herself and watches him more closely than he knows. She trusts Chiara with everything inside the boat, relies on Sophia for every port, and keeps a careful eye on Lea, who dives too much and asks too many questions.",
        "Kapitänin Marit Holm, 56, Norwegerin, dreißig Jahre auf See, die letzten elf auf der Eden. Fair, trocken, nicht hinters Licht zu führen. Sie hat {{user}} selbst eingestellt und beobachtet ihn genauer, als er ahnt. Chiara vertraut sie alles im Inneren des Boots an, auf Sophia verlässt sie sich in jedem Hafen, und auf Lea, die zu viel taucht und zu viele Fragen stellt, hat sie ein wachsames Auge."),
    5: ("W6 Below Deck", None,
        "Below deck the boat is small: shared bunk cabins, one crew mess, one narrow corridor where everyone squeezes past everyone. The walls are thin. On the crew mess fridge hangs the tally. {{user}}'s officer cabin is the only single cabin, forward of the crew mess, and the only place where the Wi-Fi works properly, which everyone has noticed.",
        "Unter Deck ist das Boot klein: Zweierkabinen mit Stockbetten, eine Crewmesse, ein schmaler Gang, in dem sich alle aneinander vorbeiquetschen. Die Wände sind dünn. Am Kühlschrank der Crewmesse hängt die Strichliste. {{user}}s Offizierskabine ist die einzige Einzelkabine, vor der Crewmesse, und der einzige Ort, an dem das WLAN richtig funktioniert, was allen aufgefallen ist."),
    8: ("A3 Lea's First Season", ["first season", "erste Saison", "deck team", "Deck-Team", "new girl", "Neue"],
        "This is Lea Moore's first season on a superyacht. Sophia got her the job as deckhand and guide for water sports and excursions. She is in {{user}}'s deck team and reports to him directly. Everything is new to her, she runs everywhere, and the crew tells her the most ridiculous sailor's yarns to see what she will believe.",
        "Es ist Lea Moores erste Saison auf einer Superyacht. Sophia hat ihr den Job als Decksfrau und Guide für Wassersport und Ausflüge besorgt. Sie ist in {{user}}s Deck-Team und ihm direkt unterstellt. Alles ist neu für sie, sie rennt überall hin, und die Crew erzählt ihr das absurdeste Seemannsgarn, um zu sehen, was sie glaubt."),
    9: ("A4 The Engine Room Board", None,
        "The engineers run a bet on the whiteboard in the engine room: which of the three ends up with the new First Officer, Chiara, Sophia or Lea, with odds that change every morning. Chiara pretends she has never seen it. Sophia knows the exact odds by heart. Lea thinks it is a fishing competition, and nobody has corrected her.",
        "Die Maschinisten führen auf dem Whiteboard im Maschinenraum eine Wette: welche der drei beim neuen Ersten Offizier landet, Chiara, Sophia oder Lea, mit Quoten, die sich jeden Morgen ändern. Chiara tut so, als hätte sie die Tafel nie gesehen. Sophia kennt die Quoten auswendig. Lea hält das Ganze für einen Angelwettbewerb, und niemand hat sie korrigiert."),
    10: ("W7 Chiara Sonnberg (chief stewardess)", None,
         "Chiara Sonnberg, 29, Chief Stewardess of the M/Y Eden, sixth season, from Hamburg-Blankenese and a family of sea captains. Platinum ponytail, red lipstick, a laugh you hear two decks down. She runs the whole interior from the six o'clock brief to the last reset cabin, knows every guest's name and drink by day two, and spoils her own surprise parties out of excitement. Everyone on the crew knows she rates everything out of ten, out loud, and that she cannot lose a game gracefully.",
         "Chiara Sonnberg, 29, Chefstewardess der M/Y Eden, sechste Saison, aus Hamburg-Blankenese und einer Familie von Kapitänen. Platinblonder Pferdeschwanz, roter Lippenstift, ein Lachen, das man zwei Decks tiefer hört. Sie führt den ganzen Innendienst vom Briefing um sechs bis zur letzten fertigen Kabine, kennt am zweiten Tag von jedem Gast Namen und Drink und verrät ihre eigenen Überraschungspartys vor lauter Vorfreude. Jeder in der Crew weiß, dass sie alles laut auf einer Skala bis zehn bewertet und kein Spiel mit Würde verlieren kann."),
    11: ("Chiara <-> Sophia (the tally)", None,
         "Chiara and Sophia are best friends and permanent rivals. The tally on the crew mess fridge counts who made more guests laugh this season; the score is disputed every single morning. They bicker like an old married couple, borrow each other's things without asking, and defend each other to the death the moment anyone else criticises one of them.",
         "Chiara und Sophia sind beste Freundinnen und Dauerrivalinnen. Die Strichliste am Kühlschrank der Crewmesse zählt, wer in dieser Saison mehr Gäste zum Lachen gebracht hat; der Stand wird jeden Morgen angefochten. Sie zanken wie ein altes Ehepaar, leihen sich ungefragt Sachen aus und verteidigen sich gegenseitig bis aufs Messer, sobald jemand anderes eine von ihnen kritisiert."),
    12: ("Chiara <-> Lea (the chick)", None,
         "Chiara has adopted Lea as her \"chick\". Lea worships her and quotes her sayings, slightly wrong. Chiara is stricter with Lea than with anyone else on board, writes her up for every phone on deck and every run on the stairs, and everyone has noticed except Chiara.",
         "Chiara hat Lea als ihr \"Küken\" adoptiert. Lea vergöttert sie und zitiert ihre Sprüche, leicht falsch. Chiara ist mit Lea strenger als mit allen anderen an Bord, schreibt sie für jedes Handy an Deck und jedes Rennen auf der Treppe auf, und allen ist das aufgefallen außer Chiara."),
    16: ("W9 Sophia Moore (concierge)", ["Sophia", "Sophia Moore", "Moore", "Concierge", "concierge", "Guest Relations"],
         "Sophia Moore, 28, Concierge and Guest Relations of the M/Y Eden, fourth season, from Falmouth in Cornwall, two years as a West End understudy before that. She gets everything: the impossible table, the best berth, the DJ for tomorrow. Every harbourmaster on the Riviera smiles when she walks in, and guests rebook because of her. Everyone on the crew knows she calls people \"darling\" right before she manages them, and that she writes things in a little brown leather notebook mid-conversation.",
         "Sophia Moore, 28, Concierge und Guest Relations der M/Y Eden, vierte Saison, aus Falmouth in Cornwall, davor zwei Jahre Zweitbesetzung im West End. Sie bekommt alles: den unmöglichen Tisch, den besten Liegeplatz, den DJ für morgen. Jeder Hafenmeister an der Riviera lächelt, wenn sie reinkommt, und Gäste buchen ihretwegen wieder. Jeder in der Crew weiß, dass sie Leute \"Darling\" nennt, kurz bevor sie sie managt, und dass sie mitten im Gespräch etwas in ein kleines braunes Lederbüchlein schreibt."),
    17: ("Sophia <-> Lea (sisters)", None,
         "Sophia raised her little sister Lea from the age of nine, when their mother forgot the rent more often than she paid it. This season she got Lea her job on the Eden. She still mothers her: food, sun cream, opinions about bikinis. Lea wants to prove she doesn't need any of it, and it shows.",
         "Sophia hat ihre kleine Schwester Lea großgezogen, seit Lea neun war und ihre Mutter die Miete öfter vergaß als bezahlte. Diese Saison hat sie Lea den Job auf der Eden besorgt. Sie bemuttert sie immer noch: Essen, Sonnencreme, Meinungen zu Bikinis. Lea will beweisen, dass sie nichts davon braucht, und das sieht man."),
    20: ("W11 Lea Moore (water sports and excursions)", ["Lea", "Moore", "Lea Moore", "deckhand", "dive guide", "Decksfrau"],
         "Lea Moore, 23, deckhand and guide for water sports and excursions on the M/Y Eden, first season: tenders, jet skis, guest dives and island trips. Sophia's little sister, from Falmouth. Everyone on the crew knows she draws every fish she sees in a fat waterproof logbook, tells marine facts to anyone standing still, and believes every sailor's yarn the engineers tell her.",
         "Lea Moore, 23, Decksfrau und Guide für Wassersport und Ausflüge auf der M/Y Eden, erste Saison: Tender, Jetskis, Tauchgänge der Gäste und Inselausflüge. Sophias kleine Schwester, aus Falmouth. Jeder in der Crew weiß, dass sie jeden Fisch, den sie sieht, in ein dickes wasserfestes Logbuch zeichnet, jedem, der stillsteht, Fakten über Meerestiere erzählt und jedes Seemannsgarn glaubt, das die Maschinisten ihr auftischen."),
}

ZUSATZ = [
    ("A5 The Tally", ["tally", "Strichliste", "fridge", "Kühlschrank", "score", "Punktestand"],
     "The tally on the crew mess fridge: two columns, Chiara and Sophia, a stroke for every guest one of them made laugh out loud. Rules are disputed, strokes are added at breakfast, and the crew bets on the final score. Whoever loses at the end of the season buys the whole crew dinner in Antibes.",
     "Die Strichliste am Kühlschrank der Crewmesse: zwei Spalten, Chiara und Sophia, ein Strich für jeden Gast, den eine von ihnen laut zum Lachen gebracht hat. Die Regeln sind umstritten, Striche kommen beim Frühstück dazu, und die Crew wettet auf den Endstand. Wer am Saisonende verliert, lädt die ganze Crew in Antibes zum Essen ein."),
    ("A6 The Ghost on the Bridge Wing", ["ghost", "Geist", "Gespenst", "bridge wing", "Brückennock"],
     "The engineers tell every new crew member that the Eden has a ghost: a woman on the bridge wing at night, holding something brass, said to be a captain's wife who drowned. It started as a joke. Lea says she saw something up there last Tuesday, and since then the story has got better every evening. Nobody has actually gone up to check.",
     "Die Maschinisten erzählen jedem Neuen, dass es auf der Eden spukt: eine Frau nachts auf der Brückennock, mit etwas aus Messing in der Hand, angeblich die Frau eines Kapitäns, die ertrunken ist. Es fing als Witz an. Lea sagt, sie hat letzten Dienstag da oben etwas gesehen, und seitdem wird die Geschichte jeden Abend besser. Nachgesehen hat noch niemand."),
    ("A7 The Margot", ["Margot", "wreck", "Wrack", "Esterel", "schooner", "Schoner", "strongbox", "Geldkassette"],
     "A Riviera legend: the Margot, a schooner that went down off the Esterel coast in 1924 with a strongbox that was never found. Divers have looked for it for decades and most believe it broke up long ago. Jack Moore, a Cornish fisherman and Sophia and Lea's grandad, always swore he knew roughly where she lay.",
     "Eine Legende der Riviera: die Margot, ein Schoner, der 1924 vor der Küste des Esterel gesunken ist, mit einer Geldkassette, die nie gefunden wurde. Taucher suchen seit Jahrzehnten nach ihr, und die meisten glauben, sie ist längst zerfallen. Jack Moore, ein Fischer aus Cornwall und Opa von Sophia und Lea, hat immer geschworen, er wisse ungefähr, wo sie liegt."),
]


def umbauen(w, lang):
    e = w["entries"]
    for uid in AUS:
        x = e[str(uid)]
        x["disable"] = True
        if not (x.get("comment") or "").startswith("[alt] "):
            x["comment"] = "[alt] " + (x.get("comment") or "")
    for uid, (comment, keys, en, de) in NEU.items():
        x = e[str(uid)]
        x["comment"] = comment
        if keys is not None:
            x["key"] = keys
        x["content"] = en if lang == "en" else de
        x["disable"] = False
    vorlage = e["9"]
    vorhandene = {(x.get("comment") or "") for x in e.values()}
    for comment, keys, en, de in ZUSATZ:
        if comment in vorhandene:
            continue
        uid = max(int(k) for k in e) + 1
        x = copy.deepcopy(vorlage)
        x.update({"uid": uid, "displayIndex": uid, "comment": comment, "key": keys, "keysecondary": [],
                  "content": en if lang == "en" else de, "disable": False, "constant": False})
        e[str(uid)] = x
    return w


for datei, lang in (("Eden Yacht.json", "en"), ("Eden Yacht (DE).json", "de")):
    p = os.path.join(W, datei)
    roh = open(p, "rb").read()
    nl = "\r\n" if b"\r\n" in roh[:4096] else "\n"
    w = umbauen(json.loads(roh.decode("utf-8")), lang)
    aktiv = sum(1 for x in w["entries"].values() if not x.get("disable"))
    print("%-22s %d Eintraege, davon aktiv %d" % (datei, len(w["entries"]), aktiv))
    if LOS:
        os.makedirs(SICHER, exist_ok=True)
        ziel = os.path.join(SICHER, datei)
        if not os.path.exists(ziel):
            shutil.copy2(p, ziel)
        with open(p, "w", encoding="utf-8", newline=nl) as fh:
            json.dump(w, fh, ensure_ascii=False, indent=2)
print("geschrieben" if LOS else "PROBELAUF")
