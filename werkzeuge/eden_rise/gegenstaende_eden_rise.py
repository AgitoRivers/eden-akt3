# -*- coding: utf-8 -*-
"""Gegenstaende fuer das Modul eden_rise (17.10.2026) - Pool nach den Grundlagen (entwuerfe\\eden-grundlagen.html).

Regeln: Jede Art hat genau eine Wirkstelle im Code. Geschenke wirken nach Geschmack: jede Person hat eine Grundhaltung zu
acht Kategorien (mag / neutral / mag_nicht), Ausnahmen je Gegenstand setzen liebt / hasst / einzigartig.
Ziele je Person: 3 "liebt" (Megan, Holm: 2), 1 einzigartig, mind. 5 "mag", 2 "mag nicht", 1 "hasst",
ein Lieblingsgeschenk unter 20 Euro. Story-Gegenstaende und Beweise der Faelle stehen NICHT hier (fest je Fall).

Aufruf: python gegenstaende_eden_rise.py  -> module\\eden_rise\\gegenstaende.json + Y:\\AI\\mission-control\\entwuerfe\\eden-gegenstaende.html
"""
import collections, html, json, os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(os.path.dirname(HIER))    # werkzeuge\eden_rise -> Eden
ZIEL = os.path.join(EDEN, "module", "eden_rise", "gegenstaende.json")
SEITE = r"Y:\AI\mission-control\entwuerfe\eden-gegenstaende.html"

KAT = ["essen", "alkohol", "schmuck", "technik", "papier", "natur", "party", "intim"]
KAT_DE = {"essen": "Essen", "alkohol": "Alkohol", "schmuck": "Schmuck", "technik": "Werkzeug & Technik",
          "papier": "Bücher & Papier", "natur": "Meer & Natur", "party": "Party & Kitsch", "intim": "Intim"}
NAMEN = {"chiara": "Chiara", "sophia": "Sophia", "lea": "Lea", "rosi": "Rosi", "siri": "Siri", "lola": "Lola", "alva": "Alva",
         "megan": "Megan", "holm": "Holm", "toto": "Totò", "yasin": "Yasin", "elsa": "Elsa", "petru": "Petru", "casanova": "Casanova"}
FRAUEN = ["chiara", "sophia", "lea", "rosi", "siri"]
# Grundhaltung: + mag, 0 neutral, - mag nicht  (Reihenfolge wie KAT)
HALTUNG = {
    "chiara":   dict(zip(KAT, "0 0 + 0 + + - 0".split())),
    "sophia":   dict(zip(KAT, "+ + + - + 0 0 +".split())),
    "lea":      dict(zip(KAT, "+ - 0 0 0 + + 0".split())),
    "rosi":     dict(zip(KAT, "+ 0 - + - 0 + 0".split())),
    "siri":     dict(zip(KAT, "0 0 - - + + 0 0".split())),
    "lola":     dict(zip(KAT, "+ + 0 - 0 + + +".split())),
    "alva":     dict(zip(KAT, "0 + + - 0 0 + +".split())),
    "megan":    dict(zip(KAT, "- + + 0 0 - - 0".split())),
    "holm":     dict(zip(KAT, "+ 0 - 0 + + - -".split())),
    "toto":     dict(zip(KAT, "+ + + 0 - 0 + 0".split())),
    "yasin":    dict(zip(KAT, "0 + + + - - + 0".split())),
    "elsa":     dict(zip(KAT, "+ - 0 + 0 0 - -".split())),
    "petru":    dict(zip(KAT, "+ + - - 0 + - -".split())),
    "casanova": dict(zip(KAT, "+ 0 + - 0 0 + -".split())),
}
PERSONEN = list(HALTUNG)
# Wirkung je Stufe (Grundlagen): Frauen (V, B) / Nebenfiguren (V)
WIRKUNG = {"einzigartig": ((10, 6), 12), "liebt": ((6, 4), 8), "mag": ((4, 0), 4), "neutral": ((0, 0), 0),
           "mag_nicht": ((-4, 0), -4), "hasst": ((-8, 0), -8)}
ARTEN = {
    "geschenk": ("Vertrauen und Begehren nach Geschmack", "handel.schenken (Geschmack je Person)", 66),
    "einzigartig": ("nur eine Person nimmt es an, +10 V · +6 B bzw. +12 V", "handel.schenken (einzigartig)", 14),
    "attribut": ("+1 aufs Attribut, solange getragen, höchstens +2 pro Attribut", "szene.feste_probe / Proben-Boni", 10),
    "gluecksbringer": ("einmal am Tag Vorteil auf ein Attribut", "szene.feste_probe (vorteil, tagesnutzung)", 10),
    "ressource": ("Strom, Diesel, Moral, Energie, Reparatur", "handel.benutzen -> zustand.folgen_anwenden", 10),
    "teil": ("Besorgung für einen Auftrag: keine Wirkung, nicht verschenkbar, nur kaufbar solange ein offener Auftrag es "
             "braucht, eigene Besorgungstasche mit 3 Plätzen", "handel.sortiment/kaufen/job_machen (braucht)", 15),
    "werkzeug": ("Vorteil (oder +2) bei Aufträgen, die es nennen (werkzeug)", "handel.jobs_heute (werkzeug_da)", 2),
    "kampf": ("wirkt nur im Kampf (heilen, Ausdauer, Zustaende, Gegner, Waffenpflege, Granaten), einmal verbraucht",
              "kampf.gegenstand_anwenden", 24),
    "material": ("Rosis Material für Upgrades: Platten für Jacken, Steine und Barren für Waffen; wird beim Aufrüsten verbraucht",
                 "kampf.aufruesten (werkstatt.material)", 12),
    "quest": ("Quest-Gegenstand: noch keine Wirkung, wird später gebraucht; nicht verkaufbar, nicht verschenkbar, belegt "
              "keinen Taschenplatz", "Menü Key Items (später Story/Aufträge)", 3),
    "schluessel": ("öffnet einen Ort, belegt keinen Taschenplatz", "regeln.zugang ({\"item\": id})", 3),
    "schmuggel": ("wirkt beim Benutzen, Kontrollrisiko beim Tragen", "handel.tagesende (Kontrolle bei Elsa)", 5),
    "andenken": ("keine Spielwirkung: Epilog und Sammlung", "Epilog / Sammlung", 7),
    "snack": ("1 Essen am Tag: selbst essen = Energie +1, verschenken = Lieblingsessen +6 V/+6 B, sonst +1/+1, Ekel −6; "
              "zählt bis 36", "handel.essen (neu, Merkmal 'heute gegessen')", 22),
    "gericht": ("selbst gekocht in Lolas Kombüse, 1 am Tag statt eines Snacks; Lieblingsgericht wirkt wie „liebt“ "
                "(+6 V · +4 B, je Person einmal voll), für die Crew Moral +1 (höchstens +1 am Tag aus Essen) und +2 für "
                "alle Anwesenden bis 36; Meisterwerk eine Stufe besser, misslungen eine schlechter",
                "handel.kochen (Küchen-Vorteil der Persona)", 12),
}
# Kochen (Duc 17.10.2026): Ducs eigene Rezepte, europaeische und suedostasiatische Hausmannskost. Probe mit dem
# Kuechen-Vorteil der Persona; SG je Gericht in wirkung["sg"]. Ersetzt das Essen des Tages (ESSEN pro_tag).
# Balance (17.10.2026): Stufenleiter [Vertrauen, Begehren]; das Lieblingsgericht wirkt je Person einmal voll ("liebt"),
# danach wie "gut". Teamessen: +2 fuer alle Anwesenden (wer es hasst: "fade"), nur bis zum Essens-Deckel 36, ebenso
# Wiederholungen; Moral aus Essen hoechstens +1 am Tag (Skala 0-5, Events liefern schon viel). Code: kern/handel.kochen.
KOCHEN = {"pro_tag": 1, "ersetzt_essen": True, "je_person_voll": 1, "crew_moral": 1, "moral_max_tag": 1,
          "crew_punkte": 2, "deckel": 36, "vorteil": "kueche",
          "stufen": {"ekel": [-6, -6], "fade": [0, 0], "normal": [1, 1], "gut": [3, 2], "liebt": [6, 4]},
          "kritisch": "+1 Stufe", "fehlschlag": "-1 Stufe"}
# Essens-Regeln (Duc 17.10.2026): EIN Essen pro Tag insgesamt - selbst essen (Energie +1) ODER verschenken.
# Lola ab Vertrauen 3: zwei Essen am Tag. Begehren nur bei Frauen, Lola und Alva. Positive Punkte bis 36 (Gespraechsdeckel),
# Ekel wirkt immer voll. Snacks mit Gras nur ohne Bordregel "kein_gras_an_bord", tragen Kontrollrisiko.
ESSEN = {"pro_tag": 1, "lola_ab_3": 2, "lieblings": 6, "normal": 1, "ekel": -6, "deckel": 36, "energie": 1}
# Quellen: toto[stufe], alva[stufe] (Alvas Bar, verkauft seit 17.10. auch alles aus dem Dorf), lola[stufe] (Kombuese), eden (Megan), event, mission, kette, fund
ITEMS = []
INTIM_BEGEHREN_AB = 3          # Duc 26.10.2026: intime Geschenke nur ab Begehren-Stufe 3 (Untergrenze, hoehere Schwellen bleiben)


def it(iid, label, art, kat=None, preis=None, quelle=(), liebt=(), hasst=(), einzig=None, wirkung=None, intim=None, text="",
       kampf=None):
    if kat == "intim":
        intim = dict(intim or {}, begehren=max(INTIM_BEGEHREN_AB, (intim or {}).get("begehren", 0)))
    ITEMS.append({"id": iid, "label": label, "art": art, "kat": kat, "preis": preis, "quelle": list(quelle),
                  "liebt": list(liebt), "hasst": list(hasst), "einzigartig": einzig, "wirkung": wirkung or {},
                  "intim": intim, "text": text, **({"kampf": kampf} if kampf else {})})


# ------------------------------------------------------------------ Geschenke (Pool ~66)
G = "geschenk"
it("arancini", "Arancini vom Bäcker", G, "essen", 15, ["alva"], liebt=["rosi"])
it("olive_oil", "Korsisches Olivenöl", G, "essen", 35, ["alva"])
it("lolas_gewuerz", "Lolas Gewürzmischung „Ocean Glitter“", G, "essen", None, ["event"], liebt=["rosi"])
it("tim_tams", "Tim Tams aus Alvas Bar", G, "essen", 6, ["alva"], liebt=["lola"], hasst=["yasin"],
   text="Die einzigen australischen Kekse in ganz Korsika. Lola weint ein bisschen.")
it("lolas_kekse", "Ein Teller von Lolas Keksen", G, "essen", None, ["event", "mission"], liebt=["megan"],
   text="Megan isst keinen Zucker. Außer diesen.")
it("feigen", "Korsische Feigen", G, "essen", 12, ["alva"], liebt=["elsa"])
it("proteinriegel", "Proteinriegel", G, "essen", 6, ["toto"], liebt=["yasin"], hasst=["lola"])
it("franzbroetchen", "Franzbrötchen (selbst gebacken)", G, "essen", None, ["mission"], liebt=["chiara"],
   text="Wie in Hamburg. Fast. Lola hat geholfen.")
it("canistrelli", "Canistrelli mit Anis", G, "essen", 9, ["alva"], liebt=["petru"], text="Korsisches Gebäck, hält ewig.")
it("myrtle", "Myrtenlikör", G, "alkohol", 30, ["alva"], liebt=["alva", "petru"], hasst=["elsa"])
it("single_malt", "Single Malt aus Islay", G, "alkohol", 95, ["eden", "toto"], liebt=["megan"])
it("limoncello", "Hausgemachter Limoncello", G, "alkohol", 22, ["alva"], liebt=["toto"])
it("cap_corse", "Cap Corse Aperitif", G, "alkohol", 28, ["alva"])
it("pink_pearl", "Rosa Perle an feiner Kette", G, "schmuck", 150, ["toto"], liebt=["chiara"], hasst=["rosi"])
it("designer_perfume", "Designerparfum", G, "schmuck", 140, ["toto", "eden"], liebt=["megan"], hasst=["siri", "lea"])
it("shell_anklet", "Fußkettchen mit Muschel", G, "schmuck", 30, ["alva"], liebt=[], intim={"vertrauen": 2})
it("herzbrille", "Diva-Sonnenbrille in Herzform", G, "schmuck", 25, ["alva"], liebt=["casanova"])
it("goldkette", "Dicke Goldkette (vermutlich echt)", G, "schmuck", 90, ["toto"], liebt=["toto"], hasst=["chiara"])
it("designer_sonnenbrille", "Designer-Sonnenbrille", G, "schmuck", 140, ["toto"], liebt=["yasin"], hasst=["petru"])
it("silberring", "Schmaler Silberring vom Markt", G, "schmuck", 45, ["alva"])
it("torque_wrench", "Profi-Drehmomentschlüssel", G, "technik", 90, ["toto"], liebt=["rosi"])
it("dive_torch", "Tauchlampe", G, "technik", 80, ["toto", "alva"], liebt=["lea", "elsa"])
it("moka", "Neapolitanische Espressokanne", G, "technik", 30, ["alva"], liebt=["toto"])
it("selfie_stick", "Selfie-Stick aus Karbon", G, "technik", 35, ["toto"], liebt=["yasin"], hasst=["petru"])
it("polbrille", "Polarisierte Sonnenbrille", G, "technik", 60, ["alva"], liebt=["elsa"])
it("schweizer_messer", "Taschenmesser", G, "technik", 40, ["alva"])
it("fountain_pen", "Füllfederhalter", G, "papier", 70, ["toto", "eden"], liebt=["sophia", "megan"])
it("notebook", "Notizbuch aus Leder", G, "papier", 40, ["alva"], liebt=["siri"])
it("gedichtband", "Gedichtband aus dem Antiquariat", G, "papier", 15, ["alva"], liebt=["sophia"], hasst=["toto"])
it("almanac", "Nautischer Almanach", G, "papier", 60, ["toto"], liebt=["holm", "petru"], hasst=["casanova"])
it("old_chart", "Alte Seekarte der Westküste", G, "papier", 120, ["toto"], liebt=["petru"])
it("pinup_magazin", "Herrenmagazin mit Pin-up", G, "papier", 12, ["toto", "alva"], liebt=["toto"], hasst=["sophia", "elsa"],
   text="Italienisches Magazin, auf dem Titel eine schöne, halbnackte Frau. Totò liest es „wegen der Artikel“.")
it("ducs_gedicht", "Ducs Gedicht über das Meer", G, "papier", None, ["event"], liebt=["chiara"])
it("muschelkette_kinder", "Selbstgemachte Muschelkette mit Perlen", G, "schmuck", None, ["event"], liebt=["siri"],
   text="Von den Dorfkindern gebastelt, ein bisschen schief. Siri trägt sie sofort.")
it("pretty_shell", "Schöne Muschel", G, "natur", 12, ["alva", "fund"], liebt=["lea"])
it("seeglas", "Grünes Seeglas", G, "natur", None, ["event", "fund"], liebt=["siri"])
it("alvas_rose", "Alvas Rose", G, "natur", None, ["event"], liebt=["lola", "siri"])
it("wool_socks", "Handgestrickte Wollsocken", G, "natur", 18, ["alva"], liebt=["holm", "chiara"], hasst=["yasin"])
it("wollmuetze", "Wollmütze mit Norwegermuster", G, "natur", 22, ["alva"], liebt=["holm"])
it("candles", "Duftkerzen „Maquis“", G, "natur", 25, ["alva"], liebt=["sophia"], hasst=["rosi"])
it("messing_anker", "Messing-Anker als Schlüsselanhänger", G, "natur", None, ["event", "fund"], liebt=["holm"],
   text="Rostig, aus der Bucht geangelt.")
it("macchia_strauss", "Strauß aus der Macchia", G, "natur", 0, ["fund"], liebt=[], text="Wilde Myrte und Rosmarin vom Hang.")
it("korallenzweig", "Kleiner Korallenzweig (Strandfund)", G, "natur", None, ["fund"], liebt=["petru"])
it("bauchnabelpiercing", "Bauchnabelpiercing mit Muschel", G, "schmuck", 18, ["alva", "event"], liebt=["lola"])
it("eden_cap", "Eden-Group-Kappe", G, "party", 25, ["eden", "event"], hasst=["siri", "holm", "alva"])
it("goldfisch", "Goldfisch in der Wassertüte", G, "natur", None, ["event"], liebt=["lea"], hasst=["chiara"],
   text="Vom Festa-Stand. Lea nennt ihn sofort irgendwie.")
it("konfetti", "Tüte Konfetti", G, "party", 8, ["alva"], liebt=["casanova"], hasst=["megan"])
it("schaerpe", "Glitzer-Schärpe „Miss Cala d'Orsu“", G, "party", 30, ["alva"], liebt=["casanova"], hasst=["elsa"])
it("faecher", "Flamenco-Fächer", G, "party", 18, ["alva"], liebt=["alva"])
it("lichterkette", "Solar-Lichterkette", G, "party", 20, ["alva"])
it("ukulele", "Gebrauchte Ukulele", G, "party", 55, ["toto"], liebt=["lola"])
# Intim (Schwellen + Privatsphaere wie bisher; Lola und Alva mit eigenen Vorlieben)
I_ = "intim"
it("massage_oil", "Massageöl mit Neroli", G, I_, 35, ["alva"], liebt=[], intim={"vertrauen": 2})
it("silk_blindfold", "Seidene Augenbinde", G, I_, 45, ["toto"], intim={"begehren": 3})
it("silk_kimono", "Seidenkimono", G, I_, 95, ["toto"], liebt=["alva"], intim={"begehren": 2})
it("massage_candle", "Massagekerze mit Wärmeöl", G, I_, 40, ["alva"], intim={"begehren": 3})
it("stockings", "Halterlose Strümpfe mit Spitzenrand", G, I_, 55, ["toto"], liebt=["alva"], intim={"vertrauen": 3, "begehren": 3})
it("satin_ties", "Satin-Fesselband fürs Bett", G, I_, 50, ["toto"], intim={"vertrauen": 4, "begehren": 4})
it("nipple_clamps", "Nippelklemmen mit Kettchen", G, I_, 45, ["toto"], intim={"vertrauen": 4, "begehren": 5})
it("lingerie", "Spitzen-Dessous in Champagner", G, I_, 120, ["toto"], intim={"vertrauen": 3, "begehren": 3})
it("plush_cuffs", "Plüsch-Handschellen", G, I_, 40, ["toto"], liebt=[], intim={"vertrauen": 3, "begehren": 4})
it("eden_wave", "Vibrator „Eden Wave“", G, I_, 90, ["toto"], intim={"vertrauen": 3, "begehren": 4})
it("jeweled_plug", "Butt Plug mit Schmuckstein", G, I_, 60, ["toto"], intim={"vertrauen": 4, "begehren": 5})
it("flamenco_dessous", "Dessous mit Rüschen", G, I_, 85, ["alva"], liebt=["alva"], intim={"vertrauen": 3, "begehren": 3},
   text="Rot und schwarz, aus Alvas eigenem Laden unter der Theke.")

# ------------------------------------------------------------------ Einzigartige (eine Person)
# Seit 29.10.2026 (Schnelljobs abgeschaltet, Favours ersetzen sie) liegen zwoelf davon fest bei Totoe (ab Vertrauen 3,
# laeden.toto.fest in modul_eden_rise.py); die Kette der Schnelljobs war ihre alte Quelle. Die Crew-Karte (megan_crewkarte)
# kann man nicht kaufen: Lola bringt sie als Dank ihrer Favour-Kette (ereignisse_favours.py).
E_ = "einzigartig"
it("chiara_tasse", "Eine Tasse nur für sie", E_, "technik", 90, ["toto3"], einzig="chiara",
   text="Handbemalt in Petrus Werkstatt, mit ihrem Namen. Für sie, nicht für die Gäste. Kette: Petru + Lola.")
it("rosi_schild", "Werkstattschild „Scuderi & Figlie“", E_, "technik", 110, ["toto3"], einzig="rosi",
   text="Aus Treibholz, von Petru geschnitzt. Für die Werkstatt, die sie eines Tages haben will.")
it("sophia_fueller", "Füller mit ihrem eigenen Namen", E_, "papier", 140, ["toto3"], einzig="sophia",
   text="Graviert mit Sophia Moore, nicht mit irgendeinem anderen Namen. Für das, was sie selbst schreiben will.")
it("lea_tauchcomputer", "Tauchcomputer", E_, "technik", 190, ["toto3"], einzig="lea",
   text="Für ihre eigenen Pläne, sicher geplant. Kette: Elsa + Totò.")
it("siri_ratgeber", "Ratgeber: Die Kunst der Fischerei auf Korsika", E_, "papier", 100, ["toto3"], einzig="siri",
   text="Aus Petrus Erzählungen, von Hand gebunden. Für ihren Vater.")
it("lola_vegemite", "Ein Glas Vegemite", E_, "essen", 60, ["toto3"], einzig="lola",
   text="Aus Alvas Geheimvorrat. Lola nennt es Heimat in braun.")
it("alva_kastagnetten", "Die Kastagnetten ihrer Großmutter", E_, "party", 130, ["toto3"], einzig="alva",
   text="Von Petru repariert. Kette: Alva + Petru.")
it("megan_crewkarte", "Eine Karte, von der ganzen Crew unterschrieben", E_, "papier", None, ["kette"], einzig="megan",
   text="Gerahmt. Nichts davon kann man kaufen.")
it("holm_lakritz", "Eine Dose norwegischer Salzlakritz", E_, "essen", None, ["mission"], einzig="holm",
   text="Bring-mir-Auftrag: Elsa bringt sie ins Krankenhaus.")
it("toto_gennaro", "Figur des San Gennaro aus Neapel", E_, "party", 110, ["toto3"], einzig="toto",
   text="Kette: der Cousin aus Bastia + Alva.")
it("yasin_goldbrille", "Goldene Sonnenbrille „Monaco“", E_, "schmuck", 150, ["toto3"], einzig="yasin")
it("elsa_strafzettelblock", "Strafzettelblock, in Leder gebunden", E_, "papier", 120, ["toto3"], einzig="elsa",
   text="Mit ihren Initialen. Sie lacht zum ersten Mal laut.")
it("petru_tabak", "Pfeifentabak „Bastia Noir“", E_, "natur", 80, ["toto3"], einzig="petru",
   text="Bring-mir-Auftrag: nur Totò kann ihn besorgen.")
it("casanova_kanone", "Konfettikanone", E_, "party", 100, ["toto3"], einzig="casanova",
   text="Für die Festa. Sie wird damit auf die Yacht zielen.")

# ------------------------------------------------------------------ Attribut-Gegenstaende (+1 solange getragen, max +2 je Attribut)
A = "attribut"
it("holm_compass", "Holms Messingkompass", A, wirkung={"bonus": ["courage", 1]}, quelle=["event"],
   text="Beim Abschied, ab Holms Vertrauen 2. Der Kompass ihres Vaters.")
it("petrus_hammer", "Petrus kleiner Hammer", A, wirkung={"bonus": ["courage", 1]}, quelle=["event"])
it("leas_taucherbrille", "Leas alte Taucherbrille", A, wirkung={"bonus": ["perception", 1]}, quelle=["event"])
it("elsas_taschenlampe", "Elsas Dienst-Taschenlampe", A, wirkung={"bonus": ["perception", 1]}, quelle=["mission"])
it("rosis_handschuhe", "Rosis Werkstatthandschuhe", A, wirkung={"bonus": ["cunning", 1]}, quelle=["event"])
it("totos_notizbuch", "Totòs Notizbuch mit Preisen", A, preis=220, wirkung={"bonus": ["cunning", 1]}, quelle=["toto4"])
it("siris_halstuch", "Siris Seidenhalstuch", A, wirkung={"bonus": ["charm", 1]}, quelle=["mission"])
it("megans_manschetten", "Megans Manschettenknöpfe", A, preis=260, wirkung={"bonus": ["charm", 1]}, quelle=["eden"],
   text="Schwarzer Onyx, ein goldener Anker. Ab Megans Vertrauen 3 im Eden-Shop.")
it("lolas_band", "Lolas Freundschaftsband", A, wirkung={"bonus": ["empathy", 1]}, quelle=["mission"])
it("sophias_lesezeichen", "Sophias Lesezeichen", A, wirkung={"bonus": ["empathy", 1]}, quelle=["mission"])

# ------------------------------------------------------------------ Gluecksbringer (einmal am Tag Vorteil)
L = "gluecksbringer"
it("multitool", "Multitool", L, preis=90, wirkung={"vorteil": "cunning"}, quelle=["alva"])
it("lockpicks", "Dietrich-Set", L, preis=180, wirkung={"vorteil": "cunning"}, quelle=["toto3"])
it("binoculars", "Fernglas", L, preis=220, wirkung={"vorteil": "perception"}, quelle=["alva"])
it("petrus_messer", "Petrus altes Fischermesser", L, wirkung={"vorteil": "perception"}, quelle=["event"])
it("aftershave", "Rasierwasser „Bastia“", L, preis=150, wirkung={"vorteil": "charm"}, quelle=["alva3"])
it("plektrum", "Lolas Plektrum", L, wirkung={"vorteil": "charm"}, quelle=["event"])
it("megan_screenshot", "Wrong Chat (Megans Foto)", L, wirkung={"vorteil": "charm"}, quelle=["event"])
it("lucky_coin", "Glücksmünze von Alva", L, preis=120, wirkung={"vorteil": "courage"}, quelle=["alva2"])
it("elsas_abzeichen", "Abzeichen der Gendarmerie maritime", L, wirkung={"vorteil": "courage"}, quelle=["event"])
# Ortskapitel Berge (27.10.2026, ereignisse_berge.py): Dumenicas Amulett (Panther erloest), Wolffs Képi (Weg A) -
# Vorteil statt +1, weil Mut und Wahrnehmung ihre zwei Attribut-Gegenstaende schon haben
it("dumenica_amulet", "Dumenica's Amulet", L, wirkung={"vorteil": "perception"}, quelle=["event"],
   text="A little silver hand on a black cord. Mazzere wear it so they wake up from the hunt.")
it("legion_kepi", "Wolff's Képi", L, wirkung={"vorteil": "courage"}, quelle=["event"],
   text="A white képi with a frayed band. People stand up straighter when they see it.")
it("tarot", "Tarotkarten", L, preis=100, wirkung={"vorteil": "empathy"}, quelle=["alva", "event"])
it("netzknoten", "Petrus Netzknoten", L, wirkung={"vorteil": "empathy"}, quelle=["event"])

# ------------------------------------------------------------------ Ressourcen / Verbrauch
R_ = "ressource"
it("diesel_canister", "Kanister Diesel", R_, preis=120, wirkung={"wert": ["diesel", 1]}, quelle=["toto", "alva"],
   text="Bei Alva höchstens ein Kanister am Tag und teurer als bei Totò.")
it("used_battery", "Gebrauchte Bootsbatterie", R_, preis=250, wirkung={"wert": ["strom", 2]}, quelle=["toto"])
it("panel_cleaner", "Paneel-Reiniger", R_, preis=60, wirkung={"wert": ["strom", 1]}, quelle=["alva"])
it("ersatzteilkiste", "Kiste Ersatzteile", R_, preis=180, wirkung={"uhr": ["reparatur", 1]}, quelle=["eden", "toto"],
   text="Schrauben, Dichtungen, Kabelschuhe. Rosi strahlt.")
it("espresso", "Doppelter Espresso", R_, preis=5, wirkung={"wert": ["energie", 1]}, quelle=["toto", "alva"],
   kampf={"ausdauer": 3, "parade": [-0.10, 1], "schnell": True})          # 27.10.2026: auch im Kampf (Doppio)
it("energieriegel", "Lolas Energieriegel", R_, preis=None, wirkung={"wert": ["energie", 1]}, quelle=["lola3"])
it("lolas_pesto", "Lolas „Spezial-Pesto“", R_, quelle=["event"])           # Duc 27.10.: Konsum gibt keine Moral
it("frischer_fang", "Frischer Fang", R_, quelle=["event", "mission"])
it("kuehlakkus", "Kühlakkus aus dem Dorf", R_, preis=40, wirkung={"flag": "vorraete_gekuehlt"}, quelle=["alva"],
   text="Die Vorräte halten einen Tag länger, wenn der Strom knapp ist.")
it("rose_festa", "Die Rose der Bürgermeisterin", R_, preis=None, wirkung={"punkte_frauen": ["begehren", 6]}, quelle=["event"],
   text="Aus Madame Casanovas Haar, nach dem Flamenco. Einmal benutzt: Begehren +6 bei allen Frauen.")


# ------------------------------------------------------------------ Teile (Besorgungen fuer Auftraege, 18.10.2026)
# Kaufbar nur, solange ein offener Auftrag sie braucht (Laden zeigt "fuer <Person>"), Besorgungstasche mit 3 Plaetzen.
# kommentar = fester, vertonter Satz der Ladenfigur beim Kauf (englisch, Spielsprache).
T_ = "teil"


def teil(iid, label, preis, laden, wer, gefuehl, kommentar, text=""):
    it(iid, label, T_, preis=preis, quelle=[laden], text=text)
    ITEMS[-1]["kommentar"] = {"wer": wer, "gefuehl": gefuehl, "text": kommentar}


teil("ersatzzellen", "Ersatzzellen für die Hotelbatterie", 180, "toto", "toto", "amusement",
     "Cells for Rosi? Tell her they come from a very honest boat. Mostly honest.", "Zwei Lithium-Zellen, gebraucht, geprüft.")
teil("relais", "Kompressor-Relais", 90, "toto", "toto", "pride",
     "The relay for Alva. I knew somebody would need it one day. That's why I had it.")
teil("messingbuchstaben", "Messingbuchstaben", 70, "toto", "toto", "amusement",
     "Brass letters. I have three R's and far too many S's. Spell carefully, Comandante.")
teil("holzleim", "Knochenleim im Topf", 15, "toto", "toto", "neutral",
     "Glue. The one thing even I can't steal - it sticks to the fingers.")
teil("eichenbrett", "Ein altes Eichenbrett", 45, "alva", "alva", "amusement",
     "Oak from the old church pews. Don't tell the priest, o figliolu. He'll want it back.")
teil("tonerde", "Ein Sack Tonerde", 30, "alva", "alva", "joy",
     "Clay for Petru's wheel? He'll grumble and love it. Like everything.")
teil("uhrenbatterie", "Knopfzelle", 25, "alva", "alva", "curiosity",
     "A battery this small and you look so serious. Who is it for? Don't tell me. I'll find out anyway.")
teil("goldfarbe", "Goldfarbe und ein feiner Pinsel", 40, "alva", "alva", "amusement",
     "Gold paint. Either you're painting a saint, or you've fallen for a pirate.")
teil("safran", "Echter Safran", 60, "alva", "alva", "approval",
     "Real saffron from Sardinia. Costs more than gold, smells better. Tell Lola to be gentle with it.")
teil("buchbinde_leinen", "Buchbinder-Leinen", 30, "alva", "alva", "caring",
     "Bookbinding linen. Somebody is making something to keep. Good. We need more of that.")
teil("netzgarn", "Rolle Netzgarn", 25, "alva", "alva", "amusement",
     "Net yarn for Petru. He'll never say thank you. He'll just mend faster.")
teil("bilderrahmen", "Ein schlichter Bilderrahmen", 35, "alva", "alva", "surprise",
     "A frame. For what, a wanted poster? ...Oh. That's sweet. Don't tell anyone I said sweet.")
# Bis 27.10.2026 im Eden-Shop - der oeffnet erst in Akt 2, die Auftraege laufen aber in Akt 1 (Duc: Alva und Toto)
teil("armband", "Silikon-Armband", 60, "toto", "toto", "amusement",
     "A silicone strap. It fell off a container in Livorno. Very gently, Comandante.")
teil("fueller_rohling", "Füller-Rohling zum Gravieren", 90, "alva", "alva", "curiosity",
     "A pen blank? Somebody's going to write love letters. Don't look at me like that, I sell everything.")
teil("antennenkabel", "Antennenkabel, seewasserfest", 120, "toto", "toto", "amusement",
     "Seawater-proof cable for the gendarmerie. Beautiful. Just don't tell Elsa where it came from.")

# ------------------------------------------------------------------ Werkzeuge (Vorteil bei Auftraegen, die sie nennen)
W_ = "werkzeug"
it("werkzeugkoffer", "Werkzeugkoffer", W_, preis=180, quelle=["toto"],
   text="Vorteil bei Reparatur-Aufträgen (oder +2, wenn dein Handwerk schon Vorteil gibt).")
it("kochmesser", "Japanisches Kochmesser", W_, preis=110, quelle=["alva"],
   text="Vorteil bei Koch-Aufträgen (oder +2, wenn deine Küche schon Vorteil gibt).")

# ------------------------------------------------------------------ Kampf (19.10.2026, wirkt nur in kern\kampf.py)
# Kampf-Verbrauchsgegenstaende (Duc + Brain Trust 27.10.2026, docs/wiki/systeme/kampf.md "Gegenstaende"): eine Regel je
# Gegenstand. Schluessel der Wirkung (kern\kampf.gegenstand_anwenden): heil_pct, stoppt (Zustaende an Duc oder "alle"),
# ausdauer, ausdauer_runden [n, Runden], parade [Faktor, Runden], schutz, immun [Zustand, Runden], gegner {Klasse: {aussetzen,
# fassung, erschoepft}}, rauch, pflege {art: Waffenart} (auch vor dem Kampf aus dem Inventar), schnell (kostet keinen Zug,
# eines je Runde). Herkunft: herkoemmliche Medizin bei Toto, Naturmedizin bei Isabelle, Waffenpflege bei Rosi, Megafon bei
# Megan; Kaffee, Mate, Hundefutter, Tee und Panzertape nur als Fruehstuecksgeschenk der Crew (moral-Runde 26.10.2026).
K_ = "kampf"
it("plaster", "Pflaster", K_, preis=10, quelle=["toto"], wirkung={"heil_pct": 0.10, "stoppt": ["blutend"], "schnell": True})
it("bandage", "Verband", K_, preis=25, quelle=["toto"], wirkung={"heil_pct": 0.25, "stoppt": ["blutend"]})
it("verbandskasten", "Verbandskasten", K_, preis=60, quelle=["toto"],
   wirkung={"heil_pct": 0.40, "stoppt": ["blutend", "brennend"]})
it("cooling_spray", "Kühlspray", K_, preis=20, quelle=["toto"],
   wirkung={"stoppt": ["brennend"], "immun": ["brennend", 2], "schnell": True})
it("smoke_pot", "Rauchtopf", K_, preis=45, quelle=["toto"], wirkung={"rauch": True})
it("antidote", "Kräutertinktur (Gegengift)", K_, preis=40, quelle=["isabelle"], wirkung={"stoppt": "alle"})
it("espresso_single", "Espresso", K_, wirkung={"ausdauer": 2, "schnell": True}, quelle=["event"])
it("americano", "Americano", K_, wirkung={"ausdauer_runden": [1, 4], "schnell": True}, quelle=["event"])
it("mate", "Mate", K_, wirkung={"stoppt": ["betaeubt", "geblendet"], "ausdauer": 1}, quelle=["event"])
it("green_tea", "Grüner Tee", K_, wirkung={"parade": [0.15, 3], "schnell": True}, quelle=["event"])
it("dog_food", "Hundefutter", K_, wirkung={"gegner": {"tier": {"aussetzen": 1, "fassung": 4}}}, quelle=["event"])
it("megaphone", "Megafon", K_, preis=80, quelle=["eden"],
   wirkung={"gegner": {"mensch": {"fassung": 5}, "tier": {"erschoepft": 2}}})
it("duct_tape", "Panzertape", K_, wirkung={"schutz": 2}, quelle=["event"])
# Waffenpflege (Duc 27.10.2026): ein Gegenstand je Waffenart, vor dem Kampf oder im Kampf, +3 Schaden fuer 5 Runden
for _iid, _label, _art in (("whetstone_blue", "Blauer Schleifstein", "klinge"), ("whetstone", "Grauer Schleifstein", "messer"),
                           ("whetstone_red", "Roter Schleifstein", "stange"), ("spikes", "Spikes", "stumpf"),
                           ("match_ammo", "Präzisionsmunition", "fern")):
    it(_iid, _label, K_, preis=30, quelle=["rosi"], wirkung={"pflege": {"art": _art, "bonus": 3, "runden": 5}})
# Granaten (Duc + Brain Trust 27.10.2026, Akt 2): Rosi baut sie selbst, ihr Laden oeffnet mit der Werkstatt (Tag 8).
# Schaden in % der Gegner-LP durch die Ruestung (Bosse 75 %), dann der Element-Zustand mit seinen Reaktionen; kosten den Zug.
for _iid, _label, _preis, _gr in (
        ("grenade_fire", "Brandgranate", 40, {"pct": 0.12, "zustand": "brennend", "stapel": 2}),
        ("grenade_water", "Wassergranate", 30, {"pct": 0.12, "zustand": "nass"}),
        ("grenade_shock", "Schockgranate", 40, {"pct": 0.12, "zustand": "strom"}),
        ("grenade_flash", "Blendgranate", 45, {"pct": 0, "zustand": "geblendet", "runden": 1}),
        ("grenade_concussion", "Erschütterungsgranate", 40, {"pct": 0.12, "zustand": "erschuettert"}),
        ("grenade_shrapnel", "Splittergranate", 50, {"pct": 0.18, "zustand": "blutend"})):
    it(_iid, _label, K_, preis=_preis, quelle=["rosi"], wirkung={"granate": _gr})
# Schlafgranate (Duc 01.11.2026): Rosi baut sie fuer Bibi, nicht zu kaufen; Bibi gibt sie vor jeder Spur (kern/mochis). Chance: kern/kampf.schlaf_chance.
it("grenade_sleep", "Schlafgranate", K_, wirkung={"schlaf": {"sicher": 0.10, "boden": 0.05}})

# Material fuer Rosis Werkstatt (25.10.2026): Plates fuer Jacken (und vorlaeufig Gemelli), Steine fuer die Waffen. Die Preise
# und Fundorte sind VORLAEUFIG (Beschaffung und Geld werden am Ende festgelegt): Stufe-1-Material bei Toto, Stufe 2 als Drop.
# 26.10.2026 (Duc): eigene Art "material" statt "kampf" - auch die Stahlplatte aus der Felsnische ist Material.
M_ = "material"
it("steel_plate", "Steel Plate", M_, preis=80, quelle=["toto"],
   text="Eine Stahlplatte für Rosis Werkstatt: Jacke oder Gemelli zum ersten Mal verbessern.")
it("titanium_plate", "Titanium Plate", M_, quelle=["drop"],
   text="Eine Titanplatte für Rosis Werkstatt: Jacke oder Gemelli zum zweiten Mal verbessern.")
for _iid, _label, _el in (("jade", "Jade", "Terremoto"), ("topas", "Topas", "Le Large"), ("aquamarin", "Aquamarin", "Riposte"),
                          ("amethyst", "Amethyst", "Sussurro")):
    it(_iid, _label, M_, preis=80, quelle=["toto"], text="Ein Stein für Rosi: Er ersetzt den Basisstein von %s (erste Verbesserung)." % _el)
for _iid, _label, _el in (("smaragd", "Smaragd", "Terremoto"), ("rubin", "Rubin", "Le Large"), ("saphir", "Saphir", "Riposte"),
                          ("opal", "Opal", "Sussurro")):
    it(_iid, _label, M_, quelle=["drop"], text="Ein edler Stein für Rosi: der Endstein für %s (zweite Verbesserung)." % _el)

it("kupfer", "Kupfer", M_, preis=80, quelle=["toto"], text="Ein Kupfer-Barren für Rosi: erste Verbesserung für Gemelli.")
it("silber", "Silber", M_, quelle=["drop"], text="Ein Silber-Barren für Rosi: zweite Verbesserung für Gemelli.")

# ------------------------------------------------------------------ Schluessel
S_ = "schluessel"
it("petru_key", "Schlüssel zu Petrus Werkstatt", S_, quelle=["mission"], wirkung={"ort": "petru_workshop"})
it("festa_invite", "Einladung der Bürgermeisterin zur Festa", S_, quelle=["event"], wirkung={"ort": "village_piazza"})
it("alvas_schluessel", "Schlüssel zu Alvas Hinterzimmer", S_, quelle=["event"], wirkung={"ort": "alvas_bar_hinterzimmer"})

# ------------------------------------------------------------------ Schmuggel (Totò gegen Elsa)
X = "schmuggel"
it("sat_data", "Satelliten-Datenpaket", X, preis=300, wirkung={"benutzen": "phone feature for one day"}, quelle=["toto"])
it("cuban_rum", "Kubanischer Rum", X, preis=120, quelle=["toto", "event"],          # Duc 27.10.: keine Moral mehr
   text="Echter Havana Club, sieben Jahre. Zum Handeln oder Verschenken.")
it("cigars", "Cohiba-Zigarren", X, preis=150, wirkung={"benutzen": "Village Reputation +2 with the old men at the harbour"}, quelle=["toto"])
it("limoncello_kiste", "Kiste Limoncello ohne Steuerbanderole", X, preis=90, wirkung={"benutzen": "to Alva: +240 €"}, quelle=["toto"])
it("taschen", "Drei „Designer“-Taschen", X, preis=60, wirkung={"benutzen": "to Yasin or Casanova: Trust +8"}, quelle=["toto"])

# ------------------------------------------------------------------ Andenken (ohne Spielwirkung - Epilog und Sammlung)
N_ = "andenken"
# 26.10.2026 (Duc): Andenken ohne Quelle in Eden Rise entfernt (Ringschluessel, Haarspange, Notizbuchseite, Muschelkette,
# Knotenarmband, Festa-Medaille) - es bleiben nur die, die ein Event wirklich vergibt
for iid, label in [("muschelkrone", "Muschelkrone der Festa"), ("rosis_foto", "Ein Foto, das du nicht löschen solltest"),
                   ("siris_karte", "Siris Dankeskarte"), ("holms_foto", "Foto von Holms erstem Kommando"),
                   ("siris_haarband", "Siris Haarband"), ("drohnen_propeller", "Propeller von Megans Drohne")]:
    it(iid, label, N_, quelle=["event"])
# 25.10.2026 (Duc): Doppelflinte und Legionaersmesser sind gestrichen. Tritons Dreizack bleibt als Andenken: geplant als
# "Masterwaffe" fuer die Saufeder (je Waffenart eine; Yamamotos Katana fuer den Saebel), noch nicht umgesetzt.
# 26.10.2026 (Duc, E-074): Fund in der Felsnische beim Kloster - die erste Stahlplatte (steel_plate) und der Zettel des Agenten,
# der sie gestohlen und dort versteckt hat. G. = Gennaro, unausgesprochen.
# Kloster San Martinu (E-073/E-074): Andenken von Bruder Ambrosius (keine Waffe, keine Spielwirkung)
# 26.10.2026 (Duc): Streitkolben, Zettel des Agenten und Tritons Dreizack sind Quest-Gegenstaende (werden spaeter gebraucht),
# die Tagebuchseiten bleiben Andenken.
Q_ = "quest"
it("ambrosius_keule", "Goldener Streitkolben von Bruder Ambrosius", Q_, quelle=["event"],
   text="Der goldene Streitkolben des Abts mit Elfenbeingriff. Frederico hat ihn versteckt, bis jemand Gutes kam.")
it("diary_page_1", "Tagebuchseite von Bruder Ambrosius (1)", N_, quelle=["event"],
   text="„Die Tiere fliehen nicht vor uns. Sie fliehen vor etwas in sich selbst.“")
it("diary_page_2", "Tagebuchseite von Bruder Ambrosius (2)", N_, quelle=["event"],
   text="Der Abt hat den Löwen gesehen: Er trägt etwas im Nacken, das blinkt, und er leidet wie die Brüder.")
it("agent_note", "Torn Note", Q_, quelle=["event"],
   text="A torn note, written to sound greedy. On the back, in pencil, someone has sketched the collar of a jacket with far more care than the note itself.")
it("tritons_dreizack", "Tritons Dreizack (Drop Sirene)", Q_, quelle=["event"],
   text="Ehemalige Waffe – später als Masterwaffe für Le Large vorgesehen.")


# ------------------------------------------------------------------ Lolas Kombuese: Snacks und Desserts
K = "snack"
it("fairy_bread", "Fairy Bread", K, "essen", 4, ["lola"], liebt=["lea"], hasst=["chiara"],
   text="Toast mit Butter und bunten Streuseln. Lea denkt an Geburtstage.")
it("lamingtons", "Lamingtons", K, "essen", 6, ["lola"], liebt=["toto"], hasst=["megan"], text="Schokowürfel mit Kokos.")
it("pavlova", "Pavlova mit Feigen und Myrte", K, "essen", 12, ["lola"], liebt=["alva"], hasst=["rosi"])
it("anzac", "Anzac Biscuits", K, "essen", 5, ["lola"], liebt=["holm"], text="Haferkekse. Holms Keks für jede Nachtwache.")
it("vegemite_schnecken", "Vegemite-Käse-Schnecken", K, "essen", 5, ["lola"], liebt=["lola"], hasst=["sophia"])
it("tim_tam_slam", "Tim-Tam-Slam-Set", K, "essen", 8, ["lola"], liebt=["siri"], hasst=["yasin"],
   text="Kekse und heißer Kakao zum Durchsaugen.")
it("ocean_popcorn", "Ocean-Glitter-Popcorn", K, "essen", 4, ["lola"], liebt=["casanova"], hasst=["elsa"])
it("kevins_rache", "Kevins Rache", K, "essen", 6, ["lola"], liebt=["lea"], hasst=["siri"], text="Kekse in Möwenform.")
it("rote_gruetze", "Rote Grütze mit Vanillesauce", K, "essen", 7, ["lola"], liebt=["chiara"], hasst=["alva"])
it("madeleines", "Lavendel-Madeleines", K, "essen", 9, ["lola"], liebt=["sophia"], hasst=["toto"])
it("cannoli", "Cannoli mit Schraubenschlüssel-Keks", K, "essen", 10, ["lola"], liebt=["rosi"])
it("plankton_gelee", "Leuchtendes Plankton-Gelee", K, "essen", 8, ["lola"], liebt=["lea"], hasst=["petru"])
it("seegras_chips", "Seegras-Chips mit Limette", K, "essen", 5, ["lola"], liebt=["siri"], hasst=["toto"])
it("protein_pancakes", "Protein-Pancakes ohne Spaß", K, "essen", 9, ["lola"], liebt=["yasin"], hasst=["lola"])
it("ghost_brownies", "Ghost-Pepper-Brownies", K, "essen", 7, ["lola"], liebt=["elsa"], hasst=["chiara"],
   wirkung={"bonus": "beim Verschenken Courage-Probe SG 11: Erfolg +4 Vertrauen extra"})
it("fiadone", "Fiadone", K, "essen", 8, ["lola"], liebt=["petru"], text="Korsischer Käsekuchen mit Zitrone.")
it("tiramisu_martini", "Espresso-Martini-Tiramisu", K, "essen", 12, ["lola"], liebt=["megan"], hasst=["lea"])
it("unit01_muffins", "Unit-01-Muffins", K, "essen", 6, ["lola"], liebt=["rosi"], hasst=["sophia"], text="Schwarz, schmecken nach Vanille.")
it("mango_sorbet", "Mango-Chili-Sorbet", K, "essen", 7, ["lola"], liebt=["alva"], hasst=["holm"])
it("space_cake", "Space Cake „Universe Edition“", K, "essen", 15, ["lola3"], liebt=["lola"], hasst=["chiara", "elsa"],
   wirkung={"gras": True, "naechster_morgen": "energie -1", "kontrollrisiko": 10},
   kampf={"ausdauer_runden": [1, 5]})                                       # Gras (Duc 27.10.2026): +1 Ausdauer je Runde
it("brownie_calm", "Brownie „Captain's Calm“", K, "essen", 12, ["lola4"], liebt=["toto"], hasst=["holm"],
   wirkung={"gras": True, "naechster_morgen": "energie -1", "kontrollrisiko": 10},
   kampf={"ausdauer_runden": [1, 5]})                                       # Gras (Duc 27.10.2026): +1 Ausdauer je Runde
it("toastie", "Mitternachts-Toastie mit Käse und Feige", K, "essen", 6, ["lola"], liebt=["chiara"],
   wirkung={"nur_phase": "nacht", "bonus": "mit Chiara nach der Wache: Vertrauen +2"})

# ------------------------------------------------------------------ Ducs Kueche: Gerichte (selbst gekocht, Kuechen-Vorteil)
# Jede Person hat genau ein Lieblingsgericht. 24.10. (Beschluss 21.10.): Lola = Bao Buns, Petru = Fish Pie.
C_ = "gericht"
it("bun_rieu", "Bún riêu", C_, "essen", None, ["kochen"], liebt=["lea"],
   wirkung={"sg": 12, "kueche": "suedostasiatisch"}, text="Vietnamesische Nudelsuppe mit Krabben und Tomate.")
it("thit_kho", "Thịt kho", C_, "essen", None, ["kochen"], liebt=["toto"],
   wirkung={"sg": 10, "kueche": "suedostasiatisch"}, text="Karamellisierter Schweinebauch mit Ei, dazu Reis.")
it("bibimbap", "Bibimbap", C_, "essen", None, ["kochen"], liebt=["yasin"], hasst=["petru"],
   wirkung={"sg": 11, "kueche": "suedostasiatisch"}, text="Petru: „Why is it in a bowl?“")
it("summer_rolls", "Sommerrollen", C_, "essen", None, ["kochen"], liebt=["sophia"],
   wirkung={"sg": 10, "kueche": "suedostasiatisch"}, text="Frische Reispapierrollen mit Garnelen und Kräutern.")
it("ramen", "Ramen", C_, "essen", None, ["kochen"], liebt=["rosi"],
   wirkung={"sg": 13, "kueche": "suedostasiatisch"}, text="Die Brühe braucht Geduld. Rosi kennt Ramen aus ihren Manga.")
it("chili_noodles", "Chili Noodles", C_, "essen", None, ["kochen"], liebt=["alva"], hasst=["megan"],
   wirkung={"sg": 9, "kueche": "suedostasiatisch"}, text="Zu scharf für eine seekranke Flottenmanagerin.")
it("bouillabaisse", "Bouillabaisse", C_, "essen", None, ["kochen"], liebt=["casanova"],
   wirkung={"sg": 12, "kueche": "europaeisch"}, text="Provenzalischer Fischtopf mit Rouille.")
it("bao_buns", "Bao Buns", C_, "essen", None, ["kochen"], liebt=["lola"],
   wirkung={"sg": 11, "kueche": "suedostasiatisch"}, text="Gedämpfte Hefebrötchen mit Schweinebauch. Lola: „Fluffy clouds, Boss.“")
it("fish_pie", "Fish Pie", C_, "essen", None, ["kochen"], liebt=["petru"],
   wirkung={"sg": 10, "kueche": "europaeisch"}, text="Fisch unter Kartoffelhaube. Petru: „Hm.“ Das heißt: noch eins.")
it("bolognese", "Spaghetti Bolognese", C_, "essen", None, ["kochen"], liebt=["chiara"], hasst=["toto"],
   wirkung={"sg": 9, "kueche": "europaeisch"}, text="Totò: „In Napoli, this is a crime.“")
it("pytt_i_panna", "Pytt i panna", C_, "essen", None, ["kochen"], liebt=["holm"],
   wirkung={"sg": 9, "kueche": "europaeisch"}, text="Bratkartoffeln mit Wurst, Zwiebel, Spiegelei und Roter Bete.")
it("fiskesuppe", "Fiskesuppe", C_, "essen", None, ["kochen"], liebt=["siri"],      # K3 (25.10.): Siri ist Norwegerin
   wirkung={"sg": 11, "kueche": "europaeisch"}, text="Norwegische Fischsuppe mit Lachs, Sahne und Dill.")
it("lauchsuppe", "Cullen Skink", C_, "essen", None, ["kochen"], liebt=["megan"],      # 28.10.: statt Kartoffel-Lauch-Suppe (Duc)
   wirkung={"sg": 9, "kueche": "europaeisch"}, text="Schottische Suppe aus Räucherschellfisch, Kartoffeln und Milch. Das Einzige, was Megan auf See bei sich behält.")
it("baguettes", "Baguettes", C_, "essen", None, ["kochen"], liebt=["elsa"],
   wirkung={"sg": 13, "kueche": "europaeisch"}, text="Brot ist die schwerste Disziplin.")


# ------------------------------------------------------------------ Auswertung
def stufe(item, pid):
    if item["art"] == "einzigartig":
        return "einzigartig" if item["einzigartig"] == pid else "ablehnen"
    if pid in item["hasst"]:
        return "hasst"
    if pid in item["liebt"]:
        return "liebt"
    if item["kat"] == "intim" and pid not in FRAUEN + ["lola", "alva"]:
        return "ablehnen"
    h = HALTUNG[pid][item["kat"]]
    return {"+": "mag", "0": "neutral", "-": "mag_nicht"}[h]


def auswerten():
    geschenke = [i for i in ITEMS if i["art"] in ("geschenk", "einzigartig")]
    zeilen, fehler = [], []
    for pid in PERSONEN:
        st = collections.Counter(stufe(i, pid) for i in geschenke)
        billig = [i for i in geschenke if stufe(i, pid) == "liebt" and i["art"] == "geschenk" and (i["preis"] or 0) < 20]
        ziel_liebt = 2 if pid in ("megan", "holm") else 3
        z = {"pid": pid, "liebt": st["liebt"], "einzigartig": st["einzigartig"], "mag": st["mag"], "mag_nicht": st["mag_nicht"],
             "hasst": st["hasst"], "unter20": [i["label"] for i in billig], "ziel_liebt": ziel_liebt}
        zeilen.append(z)
        if st["liebt"] < ziel_liebt:
            fehler.append("%s: nur %d x liebt" % (pid, st["liebt"]))
        if st["liebt"] > ziel_liebt + 2:
            fehler.append("%s: %d x liebt (zu viele, Ziel %d)" % (pid, st["liebt"], ziel_liebt))
        if st["einzigartig"] != 1:
            fehler.append("%s: %d einzigartig" % (pid, st["einzigartig"]))
        if st["mag"] < 5 or st["mag_nicht"] < 2 or st["hasst"] < 1:
            fehler.append("%s: mag %d / mag nicht %d / hasst %d" % (pid, st["mag"], st["mag_nicht"], st["hasst"]))
        if not billig:
            fehler.append("%s: kein Lieblingsgeschenk unter 20 €" % pid)
    ids = collections.Counter(i["id"] for i in ITEMS)
    fehler += ["doppelt: %s" % k for k, n in ids.items() if n > 1]
    for i in ITEMS:
        for pid in i["liebt"] + i["hasst"]:
            if pid not in PERSONEN:
                fehler.append("%s: Person %s" % (i["id"], pid))
        if i["art"] in ("geschenk", "einzigartig") and i["kat"] not in KAT:
            fehler.append("%s: Kategorie %s" % (i["id"], i["kat"]))
    gerichte = [i for i in ITEMS if i["art"] == "gericht"]
    for pid in PERSONEN:
        if not any(pid in g["liebt"] for g in gerichte):
            fehler.append("%s: kein Lieblingsgericht" % pid)
    for g in gerichte:
        if not g["liebt"] or "sg" not in g["wirkung"]:
            fehler.append("%s: Gericht braucht einen Fan und einen SG" % g["id"])
    snacks = [i for i in ITEMS if i["art"] == "snack"]
    for pid in PERSONEN:
        if not any(pid in s["liebt"] for s in snacks):
            fehler.append("%s: kein Lieblingssnack" % pid)
    for s in snacks:
        if len(s["liebt"]) != 1:
            fehler.append("%s: Snack braucht genau einen Fan" % s["id"])
    bonus = collections.Counter(i["wirkung"]["bonus"][0] for i in ITEMS if i["art"] == "attribut")
    for att, n in bonus.items():
        if n > 2:
            fehler.append("Attribut %s: %d Gegenstaende (max +2 erreichbar)" % (att, n))
    return zeilen, fehler


def events_abgleich():
    try:
        ev = json.load(open(os.path.join(EDEN, "module", "eden_rise", "ereignisse.json"), encoding="utf-8"))
    except Exception:
        return []
    ids = {i["id"] for i in ITEMS}
    fehlt = set()
    for e in ev["events"]:
        for o in e["optionen"]:
            for f in o["folgen"] + o.get("bei_erfolg", []) + o.get("bei_fehlschlag", []):
                if "item" in f and f["item"] not in ids:
                    fehlt.add(f["item"])
    return sorted(fehlt)


# ------------------------------------------------------------------ Seite
CSS = """:root{--bg:#0f1115;--flaeche:#171a20;--flaeche2:#1d2128;--linie:#2b3039;--fg:#ece6da;--leise:#a3a8b1;--akz:#d8bd86;
--akz2:#9db9d6;--gut:#a8d5b1;--schlecht:#d9a198;--f-titel:"Bricolage Grotesque","Segoe UI",system-ui,sans-serif;
--f-text:"Geist","Segoe UI",system-ui,sans-serif;--f-zahl:"Geist Mono",ui-monospace,monospace;color-scheme:dark}
@media (prefers-color-scheme:light){:root:not([data-theme="dark"]){--bg:#f3f4f6;--flaeche:#fff;--flaeche2:#eceef2;--linie:#d7dbe2;
--fg:#1a1c21;--leise:#5a606a;--akz:#8a6526;--akz2:#33628c;--gut:#2f7a45;--schlecht:#a2483a;color-scheme:light}}
:root[data-theme="light"]{--bg:#f3f4f6;--flaeche:#fff;--flaeche2:#eceef2;--linie:#d7dbe2;--fg:#1a1c21;--leise:#5a606a;--akz:#8a6526;
--akz2:#33628c;--gut:#2f7a45;--schlecht:#a2483a;color-scheme:light}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.6 var(--f-text);padding:28px 16px 64px}
.seite{max-width:1000px;margin:0 auto;display:flex;flex-direction:column;gap:40px}
h1,h2{font-family:var(--f-titel);margin:0;letter-spacing:-.015em}h1{font-size:clamp(30px,6vw,44px);line-height:1.05}
h2{font-size:22px;color:var(--akz)}p{margin:0;max-width:72ch}.leise{color:var(--leise)}.klein{font-size:13px}
section{display:flex;flex-direction:column;gap:12px}.eyebrow{font:500 12px var(--f-zahl);letter-spacing:.14em;text-transform:uppercase;color:var(--akz2)}
.tab{overflow-x:auto;border:1px solid var(--linie);border-radius:12px;background:var(--flaeche)}
table{width:100%;border-collapse:collapse;font-size:13.5px;min-width:640px}
th,td{text-align:left;padding:8px 11px;vertical-align:top;border-bottom:1px solid var(--linie)}tr:last-child td{border-bottom:0}
th{font:500 11px var(--f-zahl);letter-spacing:.06em;text-transform:uppercase;color:var(--leise);background:var(--flaeche2);position:sticky;top:0}
td.n{font-family:var(--f-zahl);white-space:nowrap}.plus{color:var(--gut)}.minus{color:var(--schlecht)}
.chip{display:inline-block;font:500 11px/1 var(--f-zahl);padding:3px 7px;border-radius:999px;border:1px solid var(--linie);color:var(--leise);margin:1px 2px 1px 0;white-space:nowrap}
.chip.l{color:var(--gut);border-color:color-mix(in srgb,var(--gut) 50%,transparent)}.chip.h{color:var(--schlecht);border-color:color-mix(in srgb,var(--schlecht) 50%,transparent)}
.chip.e{color:var(--bg);background:var(--akz);border-color:var(--akz)}
nav{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:13px}nav a{color:var(--leise);text-decoration:none;border-bottom:1px solid var(--linie)}
.ok{color:var(--gut)}.warn{color:var(--schlecht)}"""


def seite(zeilen, fehler, fehlt):
    e = html.escape
    nach_art = collections.defaultdict(list)
    for i in ITEMS:
        nach_art[i["art"]].append(i)
    out = ['<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">',
           '<title>Eden Gegenstände</title><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500&display=swap">',
           '<style>%s</style></head><body><div class="seite">' % CSS,
           '<div><div class="eyebrow">Eden Rise · Neufassung · Stand 17.10.2026</div><h1>Gegenstände</h1>',
           '<p class="leise">Der Pool für eden_rise nach den Grundlagen: jede Art mit genau einer Wirkstelle im Code, Geschenke nach '
           'Geschmack (Grundhaltung je Kategorie plus Ausnahmen). Story-Gegenstände und Beweise der Fälle sind fest und stehen '
           'nicht auf dieser Seite. Gebaut aus <code>werkzeuge\\eden_rise\\gegenstaende_eden_rise.py</code>.</p></div>',
           '<nav>' + "".join('<a href="#%s">%s</a>' % (a, a.capitalize()) for a in ARTEN) + '<a href="#personen">Personen</a></nav>']
    out.append('<section><h2>Überblick</h2><div class="tab"><table><tr><th>Art</th><th>Wirkung</th><th>wirkt in</th><th>Pool</th><th>Ziel</th></tr>')
    for a, (wirk, wo, ziel) in ARTEN.items():
        n = len(nach_art[a])
        out.append('<tr><td><b>%s</b></td><td>%s</td><td class="klein leise">%s</td><td class="n">%d</td><td class="n leise">~%d</td></tr>' % (
            a.capitalize(), e(wirk), e(wo), n, ziel))
    out.append('</table></div>')
    pruef = ('<p class="ok">Prüfung: alle Ziele je Person erfüllt, keine Doppelungen, höchstens +2 je Attribut.</p>' if not fehler
             else '<p class="warn">Prüfung: ' + "; ".join(e(f) for f in fehler) + '</p>')
    out.append(pruef)
    if fehlt:
        out.append('<p class="warn">In Events vergeben, hier noch nicht beschrieben: %s</p>' % e(", ".join(fehlt)))
    else:
        out.append('<p class="ok klein">Alle Gegenstände, die Events vergeben, sind hier beschrieben.</p>')
    out.append('</section>')
    out.append('<section id="personen"><h2>Geschmack je Person</h2><p class="leise klein">Grundhaltung zu den acht Kategorien '
               '(+ mag, · neutral, − mag nicht) und das Ergebnis über alle Geschenke.</p><div class="tab"><table><tr><th>Person</th>'
               + "".join("<th>%s</th>" % e(KAT_DE[k]) for k in KAT) + '<th>liebt</th><th>einzig</th><th>mag</th><th>mag nicht</th><th>hasst</th><th>Liebling unter 20 €</th></tr>')
    for z in zeilen:
        h = HALTUNG[z["pid"]]
        zeichen = {"+": '<span class="plus">+</span>', "0": '<span class="leise">·</span>', "-": '<span class="minus">−</span>'}
        out.append('<tr><td><b>%s</b></td>%s<td class="n">%d/%d</td><td class="n">%d</td><td class="n">%d</td><td class="n">%d</td><td class="n">%d</td><td class="klein">%s</td></tr>' % (
            NAMEN[z["pid"]], "".join("<td>%s</td>" % zeichen[h[k]] for k in KAT), z["liebt"], z["ziel_liebt"], z["einzigartig"],
            z["mag"], z["mag_nicht"], z["hasst"], e(", ".join(z["unter20"]))))
    out.append('</table></div></section>')
    for a, (wirk, wo, ziel) in ARTEN.items():
        out.append('<section id="%s"><h2>%s <span class="leise klein">· %d</span></h2><p class="leise klein">%s · wirkt in %s</p>' % (
            a, a.capitalize(), len(nach_art[a]), e(wirk), e(wo)))
        out.append('<div class="tab"><table><tr><th>Gegenstand</th><th>Kategorie / Wirkung</th><th>Preis</th><th>Quelle</th><th>Geschmack</th><th>Notiz</th></tr>')
        for i in nach_art[a]:
            if a in ("geschenk", "einzigartig"):
                spalte = e(KAT_DE.get(i["kat"], ""))
                if i["intim"]:
                    spalte += '<br><span class="klein leise">ab %s</span>' % e(", ".join("%s %d" % (k, v) for k, v in i["intim"].items()))
            else:
                spalte = '<span class="klein">%s</span>' % e(json.dumps(i["wirkung"], ensure_ascii=False).strip("{}").replace('"', ""))
            gesch = "".join('<span class="chip l">♥ %s</span>' % NAMEN[p] for p in i["liebt"])
            gesch += "".join('<span class="chip h">✕ %s</span>' % NAMEN[p] for p in i["hasst"])
            if i["einzigartig"]:
                gesch += '<span class="chip e">nur %s</span>' % NAMEN[i["einzigartig"]]
            out.append('<tr><td><b>%s</b><br><span class="klein leise">%s</span></td><td>%s</td><td class="n">%s</td><td class="klein">%s</td><td>%s</td><td class="klein leise">%s</td></tr>' % (
                e(i["label"]), e(i["id"]), spalte, "%d €" % i["preis"] if i["preis"] is not None else "–",
                e(", ".join(i["quelle"])), gesch, e(i["text"])))
        out.append('</table></div></section>')
    out.append('<section><h2>Quellen</h2><p class="klein leise">toto / toto3 / toto4 = Totòs Spind (ab Vertrauen 3/4) · alva / alva2 / alva3 = '
               'Alvas Bar an Land (verkauft seit 17.10. auch alles aus dem Dorf) · eden = Eden-Shop über Megan (Ersatzteile −10 % je Stufe) · event = Belohnung '
               'eines Events · mission = Auftrag · kette = Kette über mehrere Tage · fund = beim Erkunden.</p></section>')
    out.append('</div></body></html>')
    return "\n".join(out)


def englisch():
    """Spielsprache Englisch (Abnahme 25.10.2026): label/text aus werkzeuge\\englisch\\items_paket.py, Deutsch bleibt
    unter "de" als Vorlage fuers spaetere Mapping."""
    sys.path.insert(0, os.path.join(EDEN, "werkzeuge", "englisch"))
    from items_paket import NEU
    fehlt = []
    for i in ITEMS:
        if i["id"] not in NEU:
            fehlt.append(i["id"])
            continue
        i["de"] = {"label": i["label"], "text": i["text"]}
        i["label"], i["text"] = NEU[i["id"]]
    return fehlt


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ohne_en = [] if os.environ.get("EDEN_ITEMS_DE") else englisch()     # EDEN_ITEMS_DE=1: deutscher Stand (Vergleich)
    if ohne_en:
        print("Ohne englischen Text (items_paket.py ergaenzen):", ", ".join(ohne_en))
    zeilen, fehler = auswerten()
    fehlt = events_abgleich()
    print("Gegenstaende:", len(ITEMS), dict(collections.Counter(i["art"] for i in ITEMS)))
    for z in zeilen:
        print("  %-9s liebt %d/%d einzig %d mag %2d mag_nicht %2d hasst %d unter20: %s" % (
            z["pid"], z["liebt"], z["ziel_liebt"], z["einzigartig"], z["mag"], z["mag_nicht"], z["hasst"], ", ".join(z["unter20"])))
    for f in fehler:
        print("FEHLER", f)
    if fehlt:
        print("In Events vergeben, hier fehlend:", fehlt)
    os.makedirs(os.path.dirname(ZIEL), exist_ok=True)
    json.dump({"_hinweis": "Gebaut aus werkzeuge\\eden_rise\\gegenstaende_eden_rise.py - dort aendern.", "kategorien": KAT,
               "haltung": HALTUNG, "wirkung": WIRKUNG, "essen": ESSEN, "kochen": KOCHEN, "arten": {k: v[:2] for k, v in ARTEN.items()}, "items": ITEMS},
              open(ZIEL, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(SEITE, "w", encoding="utf-8").write(seite(zeilen, fehler, fehlt))
    print("geschrieben:", ZIEL, "und", SEITE)
    return 1 if fehler or fehlt else 0


if __name__ == "__main__":
    sys.exit(main())
