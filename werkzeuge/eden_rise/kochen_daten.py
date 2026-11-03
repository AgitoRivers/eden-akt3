# -*- coding: utf-8 -*-
"""Daten fuer den Kuechenkreis (Duc 27.10.2026, E-079): Baukasten (Haupt + Akzent + Basis), Farm bei Nonna (Garten, drei Staelle),
20 Fische. Wird von kochen_eden_rise.py geprueft und nach module\\eden_rise\\kuechen.json geschrieben - nur hier aendern.

Platzhalter: Duc liefert die endgueltige Zutatenliste spaeter. Die Engine (kern/kuechen.py, kern/farm.py) ist datengetrieben;
jede Zutat mit Rolle basis/haupt/akzent funktioniert sofort. Texte und Motive Englisch (STIL.md), Kommentare Deutsch.

Qualitaet (E-079): 1 = gekauft, 2 = gefangen/gepfluckt/gesammelt, 3 = selbst angebaut oder gezuechtet; wirkt als Faktor 1 / 1,5 / 2
auf den Akzent-Bonus. Fuer die Haupt-Kategorie (Geschmack) gilt: fish, shellfish, poultry, pork, beef, egg, veg, mushroom."""

# ------------------------------------------------------------------ Fische (Duc: 10 Meer am Boot, 10 Fluss an Rastplaetzen mit Fluss)
# id, label, kind (fish|shellfish), ort (meer|fluss), roh-Label der verarbeiteten Form, Preis roh (Totò Ankauf/Nonna), Text, Motiv
FISCHE = [
    # Meer (Cala d'Orsu, Mittelmeer vor Korsika)
    ("sea_bass", "European Sea Bass", "fish", "meer", "Sea Bass Fillets, raw", 14, "Silvery and shy, it hides near the rocks of the bay.",
     "a European sea bass, silvery body with a faint dark spot on the gill cover"),
    ("gilt_head_bream", "Gilt-head Bream", "fish", "meer", "Bream Fillets, raw", 13, "Recognised by the golden band between its eyes.",
     "a gilt-head bream, silver-grey body with a golden crescent mark between the eyes"),
    ("red_mullet", "Red Mullet", "fish", "meer", "Red Mullet Fillets, raw", 12, "Pink-red, with two whiskers it uses to feel the sand.",
     "a red mullet, rosy red body with two small chin barbels"),
    ("scorpionfish", "Scorpionfish", "fish", "meer", "Rascasse for the Pot, raw", 15, "Ugly as sin, wonderful in a bouillabaisse.",
     "a scorpionfish, mottled red-brown body with spiny fins and a wide mouth"),
    ("sardine", "Sardine", "fish", "meer", "Sardine Fillets, raw", 6, "Small, silver, and everywhere in summer.",
     "a sardine, slim silver body with a blue-green back and a row of dark spots"),
    # Lachs statt Little Tunny (Duc 28.10.2026, Story/Petru): Oily Fish Stufe 2; Rohform heisst "Fillets", damit sie nicht mit
    # Nonnas gekauften "Salmon Steaks" (salmon_steak, Qualitaet 1) verwechselt wird
    ("salmon", "Atlantic Salmon", "fish", "meer", "Salmon Fillets, raw", 24, "Silver and strong. Nobody knows what it is doing this far south.",
     "an Atlantic salmon, sleek bright silver body with a blue-grey back and a faint pink sheen along the sides"),
    ("cuttlefish", "Cuttlefish", "shellfish", "meer", "Cuttlefish Strips, raw", 11, "It changes colour when it is curious.",
     "a cuttlefish, soft oval body with a ruffled fin skirt and eight short arms with two long tentacles"),
    ("octopus", "Common Octopus", "shellfish", "meer", "Octopus Tentacle, raw", 18, "Clever hands, eight of them.",
     "a common octopus, mottled orange-brown rounded head with eight curling arms"),
    ("red_prawn", "Red Prawn", "shellfish", "meer", "Peeled Red Prawns, raw", 20, "From the deep water off the cape, red even before cooking.",
     "a red prawn, deep coral-red body with long antennae and fine legs"),
    ("spiny_lobster", "Spiny Lobster", "shellfish", "meer", "Lobster Tail, raw", 35, "No claws, but a crown of spines. A festa fish.",
     "a spiny lobster, brick-red spiny shell with very long antennae and no claws"),
    # Fluss (Rastplaetze mit Fluss, Berge und Macchia)
    ("brown_trout", "Mediterranean Trout", "fish", "fluss", "Trout Fillets, raw", 12, "Spotted like the stones in its stream.",
     "a Mediterranean trout, olive-brown body covered in red and dark spots"),
    ("eel", "European Eel", "fish", "fluss", "Eel Pieces, raw", 16, "Slippery and old. Some say it is older than the village.",
     "a European eel, long snake-like dark olive body with a pale yellow belly, curved in a gentle S-shape so that the whole eel fits inside the frame"),
    ("carp", "Common Carp", "fish", "fluss", "Carp Steaks, raw", 10, "Slow, wide and patient, like the river itself.",
     "a common carp, heavy golden-bronze scaled body with two small barbels"),
    ("pike", "Northern Pike", "fish", "fluss", "Pike Fillets, raw", 15, "A long green hunter that waits in the reeds.",
     "a northern pike, long olive-green body with pale spots and a duck-bill snout"),
    ("perch", "European Perch", "fish", "fluss", "Perch Fillets, raw", 11, "Striped like a tiny tiger, with a red fin.",
     "a European perch, green-gold body with dark vertical stripes and orange-red fins"),
    ("tench", "Tench", "fish", "fluss", "Tench Fillets, raw", 9, "The quiet doctor fish of the slow pools.",
     "a tench, thick olive-bronze body with small scales and round fins"),
    ("barbel", "Barbel", "fish", "fluss", "Barbel Fillets, raw", 10, "It feeds along the stony bottom with four whiskers.",
     "a barbel, slim olive-brown body with a flat head and four fleshy barbels"),
    ("zander", "Zander", "fish", "fluss", "Zander Fillets, raw", 17, "Pike-perch: firm white meat, shy eyes.",
     "a zander, long grey-green body with a dark banded back and large glassy eyes"),
    ("river_crayfish", "River Crayfish", "shellfish", "fluss", "Crayfish Tails, raw", 14, "A small armoured fighter under the river stones.",
     "a freshwater crayfish, olive-brown shell with two strong claws and a fan tail"),
    ("river_crab", "River Crab", "shellfish", "fluss", "River Crab Meat, raw", 13, "The sweet little crab of the Italian streams.",
     "a freshwater river crab, rounded brown-orange shell with two claws, seen from above"),
]
# Bildmotiv der Rohform, wo der Spielname das Bildmodell in die Irre fuehrt (Duc 28.10.: "Rascasse" ergab einen braunen Fremdfisch)
ROH_MOTIV = {
    "scorpionfish": "a whole fresh raw red scorpionfish, bright red-orange mottled skin with spiny fins and a wide mouth, cleaned and "
                    "ready for the pot, on a sheet of white butcher paper",
}

# ------------------------------------------------------------------ Zutaten (Platzhalter bis Duc die Liste liefert)
# id: (label, rolle, Kategorie fuer Geschmack oder None, Quelle, Preis, sg (Basis: Grund-SG, Haupt: Zuschlag), Heilung (nur Basis), Akzent-Effekt, Text)
ZUTATEN = {
    # Basis
    "rice": ("Rice", "basis", None, "nonna", 4, 8, 4, None, "Plain white rice. It forgives a lot."),
    "noodles": ("Noodles", "basis", None, "nonna", 5, 9, 3, None, "Wheat noodles, dried, from a good packet."),
    "flour": ("Flour", "basis", None, "nonna", 3, 10, 3, None, "For dough, pancakes and everything that needs a base."),
    "rice_paper": ("Rice Paper", "basis", None, "batu", 5, 9, 3, None, "Thin round sheets, dry as old letters. One second in warm water."),
    "potatoes": ("Potatoes", "basis", None, "garten", 3, 8, 5, None, "Firm, earthy and honest."),
    "cabbage": ("Cabbage", "basis", None, "garten", 3, 9, 2, None, "A tight green head from Nonna's garden."),
    # Haupt (Land): Tiere und Garten
    "chicken_meat": ("Chicken", "haupt", "poultry", "tier", 18, 0, 0, None, "From a hen that had a name."),
    "pork": ("Pork", "haupt", "pork", "tier", 28, 1, 0, None, "Dark, well-marbled, from a Cinta Senese pig."),
    "beef": ("Beef", "haupt", "beef", "tier", 45, 2, 0, None, "From a dark Pisana. Slow and generous."),
    "eggs": ("Eggs", "haupt", "egg", "tier", 6, 0, 0, None, "Still warm, if you were quick."),
    "truffle": ("Truffle", "haupt", "mushroom", "tier", 60, 3, 0, None, "Found by a pig with excellent priorities."),
    "zucchini": ("Zucchini", "haupt", "veg", "garten", 4, 0, 0, None, "Long, green, and always more than you asked for."),
    "salmon_steak": ("Salmon Steaks, raw", "haupt", "fish", "nonna", 24, 1, 0, None, "Not a local fish. Nonna's cousin sends it from the north."),
    "tofu": ("Tofu", "haupt", "veg", "batu", 8, 0, 0, None, "White, firm, pressed this morning. It tastes of almost nothing until you teach it."),
    # Akzent (je Effektkategorie bis zu zwei Zutaten)
    "chilis": ("Chillies", "akzent", None, "garten", 4, 0, 0, "krit", "Small, red and rude."),
    "wildkraeuter": ("Wild Herbs", "akzent", None, "garten", 3, 0, 0, "xp", "Thyme, myrtle and sage from the maquis."),
    "lemongrass": ("Lemongrass", "akzent", None, "garten", 4, 0, 0, "xp", "Smells of lemon and tastes of somewhere else. It likes Nonna's soil."),
    "tomaten": ("Tomatoes", "akzent", None, "garten", 4, 0, 0, "vertrauen", "Sun-warm and a little too ripe."),
    "milk": ("Milk", "akzent", None, "tier", 8, 0, 0, "vertrauen", "Whole milk, still cool from the cow."),
    "knoblauch": ("Garlic", "akzent", None, "garten", 3, 0, 0, "attribut", "A braid of bulbs. Vampires and cowards stay away."),
    "zitronen": ("Lemons", "akzent", None, "nonna", 4, 0, 0, "preis", "From the terraces above the cove."),
    "sojasauce": ("Soy Sauce", "akzent", None, "nonna", 6, 0, 0, "ankauf", "Dark and salty. Smells like the kitchen at home."),
    "fish_sauce": ("Fish Sauce", "akzent", None, "batu", 12, 0, 0, "umami", "Amber and salty. Everybody says it stinks. Everybody comes back."),
}

# Akzent-Effekte (7 Kategorien, je ein Wirkpunkt im Code), Wert bei Qualitaet 1; Faktor x1 / x1,5 / x2 (kern/kuechen.py)
EFFEKTE = {
    "krit": ("Crit chance +%d %%", 5, "kampf.crit_chance (Chips-Summe)"),
    "xp": ("Experience +%d %%", 10, "kampf.award_xp"),
    "vertrauen": ("Trust +%d with everyone at the table", 1, "kuechen.kochen_baukasten (sofort, Teller und Crew)"),
    "preis": ("Shop prices -%d %%", 10, "handel.preis"),
    "attribut": ("Courage +%d in combat", 1, "kampf.attributes"),
    "ankauf": ("Sell prices +%d %%", 10, "handel.ankauf (Totò)"),
    "umami": ("Nobody dislikes this dish", 1, "kuechen.vorschau (sofort, leert mag_nicht)"),
}

# Geschmack je Person: (mag, mag nicht) - Haupt-Kategorien. Platzhalter nach den Figurenseiten, jederzeit aenderbar.
GESCHMACK = {
    "lea": (["shellfish", "fish"], ["pork"]), "sophia": (["fish", "veg"], ["beef"]), "rosi": (["beef", "egg"], ["veg"]),
    "alva": (["pork", "shellfish"], ["fish"]), "lola": (["poultry", "veg"], ["mushroom"]), "siri": (["fish", "egg"], ["pork"]),
    "yasin": (["beef", "poultry"], ["veg"]), "megan": (["veg", "egg"], ["shellfish"]), "holm": (["pork", "fish"], ["veg"]),
    "toto": (["pork", "shellfish"], ["veg"]), "elsa": (["poultry", "egg"], ["fish"]), "petru": (["fish", "shellfish"], ["beef"]),
    "casanova": (["fish", "mushroom"], ["egg"]), "chiara": (["beef", "shellfish"], ["egg"]),
}

# ------------------------------------------------------------------ Garten (Nonna)
BEETE = 4
PFLANZEN = {  # Zutat -> (Saatpreis, Ertrag je Beet, Tage bis zur Ernte)
    "potatoes": (2, 3, 1), "cabbage": (2, 2, 1), "chilis": (2, 3, 1), "wildkraeuter": (2, 3, 1), "tomaten": (2, 3, 1),
    "knoblauch": (2, 2, 1), "zucchini": (2, 2, 1), "lemongrass": (2, 3, 1),
}
# Pflanzen, die erst freigeschaltet werden: Pflanze -> (Flag, das sie freigibt; datiertes Flag beim ersten Pflanzen)
PFLANZEN_FREI = {"lemongrass": ("zitronengras_da", "zitronengras_gepflanzt")}

# ------------------------------------------------------------------ Tiere (Toskana/Italien: Livorno-Huhn, Cinta Senese, Pisana)
# Stufen: 1 Baby, 2 erwachsen (Maennchen/Weibchen), 3 alt. Produktion ab Stufe 2, Schlachten nur Stufe 3.
TIERE = {
    "chicken": {"label": "Chicken", "rasse": "Livorno hen", "stall": 120, "plaetze": 6, "baby_preis": 25,
                "baby_tage": 2, "erwachsen_tage": 5, "zucht_tage": 3,
                "produkt": {"art": "eggs", "wer": "weibchen", "alle_tage": 1, "menge": 1},
                "fleisch": {"art": "chicken_meat", "menge": 2}, "namen": ["Gina", "Pepe", "Bianca", "Tito", "Rosa", "Nello"],
                "motiv": "a Livorno hen, a slender white Italian chicken with a bright red comb and yellow legs"},
    "pig": {"label": "Pig", "rasse": "Cinta Senese", "stall": 200, "plaetze": 4, "baby_preis": 60,
            "baby_tage": 3, "erwachsen_tage": 6, "zucht_tage": 5,
            "produkt": {"art": "truffle", "wer": "alle", "alle_tage": 2, "menge": 1},
            "fleisch": {"art": "pork", "menge": 3}, "namen": ["Gigi", "Fiora", "Bruno", "Lupa", "Tonno", "Mina"],
            "motiv": "a Cinta Senese pig, a black Italian pig with a broad white band around its shoulders and front legs"},
    "cow": {"label": "Cow", "rasse": "Pisana", "stall": 320, "plaetze": 3, "baby_preis": 110,     # Duc 28.10.: schwarze Pisana statt weisser Chianina
            "baby_tage": 4, "erwachsen_tage": 7, "zucht_tage": 7,
            "produkt": {"art": "milk", "wer": "weibchen", "alle_tage": 1, "menge": 1},
            "fleisch": {"art": "beef", "menge": 4}, "namen": ["Bella", "Gino", "Stella", "Marco", "Olga", "Dino"],
            "motiv": "a Pisana cow, a rare Tuscan cattle with a solid very dark chestnut coat that looks almost black, short smooth hair, short curved horns, dark muzzle"},
}
# Sprite-Varianten je Art: baby, adult_m, adult_f, old_m, old_f (Duc: sonst gleiche Variante groesser skaliert)
TIER_VARIANTEN = {"baby": "a baby", "adult_m": "an adult male", "adult_f": "an adult female", "old_m": "an old male with a weathered look",
                  "old_f": "an old female with a weathered look"}
# Anzeigegroesse je Art und Variante (Faktor auf 100 px): die Sprites sind auf das Motiv zugeschnitten, die Art traegt die Groesse
TIER_GROESSE = {"chicken": {"baby": 0.5, "adult_m": 0.95, "adult_f": 0.85, "old_m": 1.0, "old_f": 0.9},
                "pig": {"baby": 0.6, "adult_m": 1.1, "adult_f": 1.0, "old_m": 1.15, "old_f": 1.05},
                "cow": {"baby": 0.9, "adult_m": 1.55, "adult_f": 1.4, "old_m": 1.6, "old_f": 1.45}}
TIER_LAUT = {"chicken": "cluck", "pig": "grunt", "cow": "moo"}

# ------------------------------------------------------------------ Nonnas Laden (Tagesvorrat) und Fredericos Lieferung
# Dauerhaft da (Grundzutaten, unbegrenzt) und knapper Tagesvorrat tierischer Zutaten (teurer als eigene Zucht lohnt)
NONNA_DAUERHAFT = ["rice", "noodles", "flour", "zitronen", "sojasauce"]
NONNA_TAGESVORRAT = {"eggs": 3, "milk": 2, "chicken_meat": 2, "pork": 1, "beef": 1, "salmon_steak": 1}
NONNA_AB_TAG = 4

# Frederico bringt den Einkauf rueber (Kind, Botenjunge: neckisch, manchmal suess, keine Flirtinhalte). Stimme: frederico.
FREDERICO = [
    "I'll bring it over right now, Officer! [chuckle] Well... right after the goat finishes her lunch. She's very particular.",
    "It'll be there before you've even said goodbye. [laugh] Okay, maybe a little after. The cart has a wobbly wheel.",
    "Nonna says I must carry it carefully. [sniff] I have never dropped anything. Only once. Twice, if you count Tuesday.",
    "I'll run all the way! [gasp] Almost all the way. The hill is very steep, and the goat has opinions.",
    "Your shopping is in good hands, Officer. [chuckle] Small hands, but fast ones.",
    "I'll put it in the kitchen myself and I won't peek. [laugh] Only a little peek. At the cheese.",
    "Leave it to me! [cough] That's what Nonna says right before she gives me more work. But I like it.",
    "Goodbye, Officer! The cart and I are faster than the weather. [chuckle] Usually.",
]

# Nonnas Buehne im Laden-Fenster (Hintergrund, Figur, Gruesse): wird von kochen_eden_rise.py in laeden.json eingetragen (die Zeilen
# werden vorab vertont wie alle Ladenzeilen). Stimme: resolut, herzlich, droht mit dem Kochloeffel (kloster.md).
NONNA_LADEN = {
    "name": "Nonna's Farm", "wer": "nonna", "nur_an_land": False, "hintergrund": "eden_rise_monastery_garden_dusk.png",
    "text": "Beds, sheds and a very opinionated goat. Nonna sells what she can spare, and Frederico runs it down to the harbour.",
    "gruss_stufen": {"gruss": [0, 5]},
    "zeilen": {
        "gruss": [
            "Stand still, or I'll cook you! [laugh] There. Now you can look at the animals. Don't feed the goat, she bites.",
            "Come in, come in. Nobody leaves my farm hungry and rude. [chuckle] Wash your hands first.",
            "The beds are ready, the animals are loud, and Frederico has been waiting all morning for an errand. [sigh] What do you need?",
        ],
        "kauf": [
            "Good. Frederico will bring it over before it gets cold. [cough] Frederico! Where is that boy?",
            "Honest money for honest food. [chuckle] And don't haggle with the goat, she always wins.",
        ],
    },
    "gefuehl": {"gruss": "joy", "kauf": "approval"},
}

# ------------------------------------------------------------------ Rohstoffe fuer die Staelle (Duc 27.10.2026)
# Quellen: Nonnas Tagesvorrat (Frederico liefert), Fundsachen beim Angeln (Treibholz, Ankerkette, Flusskiesel), spaeter Beute
# aus Erkundungen (kern/farm.rohstoff_add). id: (Label, Text, Preis bei Nonna)
ROHSTOFFE = {
    "timber": ("Timber", "Split logs from the valley, stacked to dry. They smell better than anything you'll ever build with them.", 8),
    # Stein geteilt (Duc 30.10.2026): Schiefer verkauft Nonna, Granit bricht man selbst. Der Schieferfels gibt Schiefer, der Granitfels Granit.
    "slate": ("Slate", "Dark plates split from the ridges above Corte. The old roofs here wear it. It breaks along its own grain, never along yours.", 6),
    "granite": ("Granite", "Grey, speckled and in no hurry. The island is made of it, and so is every wall still standing after a winter.", 8),
    "iron": ("Iron Fittings", "Hinges, nails and brackets from the smith in Corte.", 25),
    # Beiprodukt der Korkeiche beim Holzfaellen (Duc 28.10.2026): Material fuer Petrus Koeder, kein Ladenartikel
    "cork": ("Cork", "Bark from a cork oak, light and warm to the touch. Petru carves floats from it.", 5),
    # Moewenfeder (Duc 30.10.2026, Koeder): Beute aus dem Moewen-Kampf beim Angeln und Fundsache am Meer, kein Ladenartikel
    "feather": ("Gull Feather", "A stiff grey-white feather, clean as paper. Petru ties them onto his best lures.", 0),
    # Danzels Auftraege (Duc 30.10.2026, systeme/schneider.md)
    "cloth": ("Cloth", "A bolt of plain linen that fell off a ferry, according to the man who sold it. It still smells of the ferry.", 15),
    "wool": ("Corsican Wool", "Rough, oily and warm, straight off a mountain sheep. It keeps out everything except the smell of sheep.", 15),
    "leather": ("Boar Leather", "Thick hide with a few old scars in it. The boar had a hard life, and the leather remembers.", 12),
    "coral": ("Red Coral", "A branch of red coral from the rocks off the Punta d'Orsu. A good tailor can get six buttons out of it. A bad one gets four.", 20),
    # Stahl (Duc 30.10.2026): nur fuer Stall-Stufe 3, kein Ladenartikel, faellt ab Tag 22 (Akt 3) aus gewonnenen Kaempfen gegen Menschen
    "steel": ("Steel", "Nobody on this island makes it. It only comes ashore inside the machines sent to find you, so you take it back out.", 40),
}
NONNA_ROHSTOFF_VORRAT = {"timber": 6, "slate": 6, "iron": 2}
STAHL_KAMPF = {"ab_tag": 22, "n": 1, "klasse": "maschine"}
LEDER_KAMPF = {"n": 1, "gegner": ["Boar", "Alpha Boar"]}

# Stall-Stufen: Stufe 1 = bauen, 2 und 3 = ausbauen. Geld + Rohstoffe; Wirkung: Plaetze, +Menge je Produkt, Zucht schneller.
# Rezepte (Duc 30.10.2026): Stufe 1 Holz + Schiefer, Stufe 2 Holz + Kork + Schiefer + Granit, Stufe 3 Holz + Granit + Eisen + Stahl.
STALL_STUFEN = {
    "chicken": [
        {"geld": 120, "rohstoffe": {"timber": 4, "slate": 2}, "plaetze": 6, "text": "A small henhouse with one perch row."},
        {"geld": 150, "rohstoffe": {"timber": 6, "cork": 2, "slate": 2, "granite": 2}, "plaetze": 9, "text": "A bigger run and a second perch row: room for three more."},
        {"geld": 220, "rohstoffe": {"timber": 6, "granite": 4, "iron": 2, "steel": 2}, "plaetze": 9, "menge_plus": 1, "zucht_minus": 1,
         "text": "Nesting boxes full of straw: every hen lays one more egg, and chicks come sooner."},
    ],
    "pig": [
        {"geld": 200, "rohstoffe": {"timber": 6, "slate": 2}, "plaetze": 4, "text": "A stone sty under the chestnut trees."},
        {"geld": 220, "rohstoffe": {"timber": 6, "cork": 3, "slate": 4, "granite": 2}, "plaetze": 6, "text": "A fenced oak grove next door: room for two more."},
        {"geld": 300, "rohstoffe": {"timber": 8, "granite": 6, "iron": 2, "steel": 3}, "plaetze": 6, "menge_plus": 1, "zucht_minus": 1,
         "text": "A muddy wallow and the deep oak wood: the pigs find one more truffle, and piglets come sooner."},
    ],
    "cow": [
        {"geld": 320, "rohstoffe": {"timber": 8, "slate": 4}, "plaetze": 3, "text": "A barn with a hayloft."},
        {"geld": 300, "rohstoffe": {"timber": 8, "cork": 4, "slate": 6, "granite": 4}, "plaetze": 5, "text": "A second stall row and a water trough: room for two more."},
        {"geld": 400, "rohstoffe": {"timber": 10, "granite": 8, "iron": 3, "steel": 4}, "plaetze": 5, "menge_plus": 1, "zucht_minus": 1,
         "text": "A summer pasture on the terraces: every cow gives one more milk, and calves come sooner."},
    ],
}

# ------------------------------------------------------------------ Angeln (Duc 27.10.2026)
# pose = [x, y] in Prozent der Wasserflaeche (linke 72 % des Bildschirms): dort liegt im Hintergrundbild das Wasser.
# Ablauf: auswerfen -> Biss (rechtzeitig anschlagen) -> Drill: ein Punkt huepft im senkrechten Balken auf und ab, in der goldenen Zone
# treffen (wie eine Parade). 3-4 Treffer = gefangen. Die Zone schrumpft die ganze Zeit (Fehlklick: noch mehr); ist sie weg, reisst
# die Leine. Niedrige Stufe = langsamer Punkt, grosse Zone.
# Seit 28.10.2026 (Duc): geangelt wird nur, wo Wasser ist - an den Rastplaetzen der Expeditionen (QUELLEN unten) und am Boot.
# Kein Zeitpreis mehr: man angelt, bis die Quelle leer ist (WUERFE_PRO_SITZUNG Fische), dann 3 Tage Pause.
ANGEL_ORTE = {
    "boot": {"label": "Fishing off the Swim Platform", "text": "Rod, bucket, the stern in the shade. The sea doesn't hurry.",
             "bild": "eden_rise_angeln_boot.png", "wasser": "meer", "frei": None, "pose": [34, 62]},
}
WUERFE_PRO_SITZUNG = 4
FISCH_STUFE = {
    "sardine": 1, "gilt_head_bream": 1, "red_mullet": 1, "sea_bass": 1, "scorpionfish": 2, "cuttlefish": 2, "octopus": 2,
    "salmon": 2, "red_prawn": 3, "spiny_lobster": 3,
    "brown_trout": 1, "perch": 1, "carp": 1, "tench": 1, "barbel": 2, "river_crayfish": 2, "river_crab": 2, "pike": 2,
    "eel": 3, "zander": 3,
}
STUFEN_GEWICHT = {1: 60, 2: 30, 3: 10}
# Drill je Stufe (0 = Fundsache): Treffer, Tempo (Balkenhoehen je Sekunde), Zone (Anteil am Balken), Schwund (je Sekunde)
DRILL = {
    0: {"treffer": 2, "tempo": 0.65, "zone": 0.40, "schwund": 0.022},
    1: {"treffer": 3, "tempo": 0.85, "zone": 0.34, "schwund": 0.028},
    2: {"treffer": 3, "tempo": 1.10, "zone": 0.29, "schwund": 0.030},
    3: {"treffer": 4, "tempo": 1.30, "zone": 0.27, "schwund": 0.030},
}
DRILL_FEHLER = 0.06            # ein Fehlklick nimmt so viel von der Zone
DRILL_TEMPO_JE_TREFFER = 1.08  # nach jedem Treffer wird der Fisch schneller
WAHRNEHMUNG_ZONE = 0.015       # je Punkt Wahrnehmung ueber 2 (hoechstens 3 Punkte)
BISS = {"warten": [1.4, 3.6], "fenster": 0.95, "fenster_wahrnehmung": 0.1}
FUND_CHANCE = 0.15
FUNDSACHEN = {
    "meer": [("driftwood", "Driftwood", "A bleached plank, still good wood.", {"timber": 1}),
             ("rusty_chain", "Rusty Anchor Chain", "A length of old chain. The smith will want it.", {"iron": 1}),
             ("gull_feather", "Gull Feather", "A grey-white feather caught in the rocks. Petru would know what to do with it.", {"feather": 1}),
             ("red_coral", "Red Coral", "A branch of red coral tangled in your line. Somebody on the island will want that.", {"coral": 1})],
    "fluss": [("river_slate", "River Slate", "A handful of thin flat plates from the bottom.", {"slate": 2}),
              ("old_branch", "Waterlogged Branch", "A heavy oak branch. It'll dry.", {"timber": 1})],
}
# Alle 10 Fische eines Gewaessers gefangen: dauerhafter Bonus (groessere Zone) - Sammelziel fuers Fisch-Journal
SAMMEL_BONUS = {
    "meer": {"label": "Lea's Lucky Lure", "zone": 0.03,
             "text": "Lea saw your journal and pressed her grandad's old lure into your hand. The golden band stays a little wider."},
    "fluss": {"label": "Petru's Cork Float", "zone": 0.03,
              "text": "Petru turned your journal page by page and gave you a cork float he carved himself. The golden band stays a little wider."},
}

# ------------------------------------------------------------------ Quellen an Rastplaetzen (Duc 28.10.2026)
# Holz, Stein und Wasser an den Rastplaetzen der Expeditionen (kern/abbau.py). Man baut ab bzw. angelt, bis die Quelle leer ist
# (QUELLE_MENGE Baeume/Felsen, WUERFE_PRO_SITZUNG Wuerfe), dann ist sie QUELLE_PAUSE Tage erschoepft. Kein Zeitpreis. Mehrere
# Frames desselben Ortes (Tag/Nacht, vorher/nachher) teilen eine Quelle. holz/stein = Mischung der Knoten (Gewicht),
# wasser = Gewaesser fuers Angeln, angel_bild = Kandidat aus werkzeuge/angeln_bilder.py (Duc waehlt auf der Abnahme-Seite;
# angeln_bilder.py uebernehmen kopiert ihn als eden_rise_angeln_<platz>.png), pose = wo der Schwimmer liegt.
# Seit 28.10. (Duc: "alle 20 nutzen, wechselnd je Kategorie") ist angel_bild nur noch das Bild der Karte in der freien Wahl und
# der Rueckfall: jeder Angelgang zieht zufaellig eines der 10 Bilder seines Gewaessers, nie zweimal hintereinander dasselbe
# am selben Platz (kern/angeln.py starten). Dateien: eden_rise_angeln_<meer|fluss>_NN.png (angeln_bilder.py uebernehmen).
# Duc 29.10.: das Boot zieht nur die Yacht-Bilder (Badeplattform Tag/Nacht, Achterdeck, Bug, Beiboot), die Rastplaetze am Meer
# nur die Kuestenbilder (Granitbucht, Hafenmole, Strandsteg, Felskueste, Leuchtturm); Fluss bleibt fluss_01-10.
_AB = "eden_rise_angeln_%s_%02d.png"
ANGEL_BILDER = {"boot": [_AB % ("meer", n) for n in (1, 2, 5, 6, 9)],
                "meer": [_AB % ("meer", n) for n in (3, 4, 7, 8, 10)],
                "fluss": [_AB % ("fluss", n) for n in range(1, 11)]}
QUELLE_MENGE = 4
QUELLE_PAUSE = 3
QUELLEN = {
    "boot": {"label": "Swim Platform", "frames": [], "wasser": "meer", "angel_bild": "meer_01", "pose": [34, 62]},
    "kl_bachufer": {"label": "Under the Holm Oak", "frames": ["kl_bachufer"], "holz": {"cork_oak": 60, "holm_oak": 40},
                    "wasser": "fluss", "angel_bild": "fluss_01", "pose": [34, 66]},
    "kl_huette": {"label": "The Shepherd's Hut", "frames": ["kl_huette"], "holz": {"cork_oak": 50, "holm_oak": 50}},
    "kl_lager": {"label": "The Brothers' Camp", "frames": ["kl_lager"], "holz": {"holm_oak": 60, "cork_oak": 40}},
    "kl_schlucht": {"label": "Fire on the Ledge", "frames": ["kl_schluchtfeuer", "kl_schluchtfeuer_kalt"], "stein": {"granite": 60, "schist": 40}},
    "bg_koehler": {"label": "The Charcoal Burners' Clearing", "frames": ["bg_koehler"], "holz": {"holm_oak": 70, "cork_oak": 30}},
    "bg_see": {"label": "The Mountain Lake", "frames": ["bg_see", "bg_see_rast"], "stein": {"granite": 70, "schist": 30},
               "wasser": "fluss", "angel_bild": "fluss_02", "pose": [36, 60]},
    "bg_kamm": {"label": "The Foggy Ridge", "frames": ["bg_kamm_funk"], "stein": {"schist": 60, "granite": 40}},
    "bg_u1_huette": {"label": "Ghjuvan's Summer Hut", "frames": ["bg_u1_huette"], "holz": {"holm_oak": 60, "cork_oak": 40}},
    "bg_u2_huette": {"label": "An Empty Hut", "frames": ["bg_u2_huette_leer"], "holz": {"holm_oak": 70, "cork_oak": 30}},
    "gr_strand": {"label": "The Drowned Beach", "frames": ["gr_strand"], "stein": {"granite": 50, "schist": 50},
                  "wasser": "meer", "angel_bild": "meer_03", "pose": [32, 64]},
    "gr_u1_luft": {"label": "The Air Pocket", "frames": ["gr_u1_luft"], "stein": {"schist": 60, "granite": 40}},
    "gr_u2_lager": {"label": "The Treasure Hunters' Camp", "frames": ["gr_u2_lager"], "stein": {"granite": 60, "schist": 40}},
    "fn_teich": {"label": "The Quiet Pool", "frames": ["fn_teich_leer"], "wasser": "meer", "angel_bild": "meer_06", "pose": [36, 62]},
}
# Knoten: was faellt bzw. bricht. Ertrag in Rohstoffen; der erste Rohstoff bekommt beim perfekten letzten Schlag +1.
KNOTEN = {
    # Korkeiche (Duc 30.10.2026): nur die Rinde kommt ab, der Baum bleibt stehen und wird nicht zu Holz. Steineiche dafuer 3 statt 2.
    "holm_oak": {"art": "holz", "label": "Holm Oak", "ertrag": {"timber": 3}, "bilder": ["holm_oak", "holm_oak_2", "holm_oak_3"]},
    "cork_oak": {"art": "holz", "label": "Cork Oak", "ertrag": {"cork": 2}, "bilder": ["cork_oak", "cork_oak_2"]},
    "granite": {"art": "stein", "label": "Granite Boulder", "ertrag": {"granite": 2}},
    "schist": {"art": "stein", "label": "Slate Rock", "ertrag": {"slate": 2}},
}
PERFEKT_PLUS = 1
# Stapeln (Duc 28.10.2026): Was man auf einer Expedition abbaut oder angelt, liegt in der Tasche (kern/expedition.py ernte) -
# Rohstoffe bis 10 je Platz, Fische 3 je Art (die Sterne bleiben je Fisch). Bei der Heimkehr wandert es in Zaehler und Kueche.
ERNTE_STAPEL = {"rohstoff": 10, "fisch": 3}
# Ring-Minispiel (wie die Ring-Parade im Kampf): ein Kreis zieht sich in `dauer` Sekunden auf den Zielring zusammen; jeder Treffer
# macht den naechsten Ring um `schneller` flotter. Zeitfenster in ms um den Treffpunkt; Kraft ueber 2 verbreitert das
# Perfekt-Fenster je Punkt (hoechstens 3 Punkte).
RING = {"dauer": 1.1, "schneller": 0.9, "gut_ms": 150, "perfekt_ms": 60, "kraft_ms": 10}

# Werkzeuge bei Petru (Duc 28.10.2026): Stufe 1 kaufen ("der Arme hat kein Geld"), Stufe 2 Material + Wunschfisch, Stufe 3
# schmiedet Petru und Rosi haertet (ihre Werkstatt offen, Vertrauen Petru 3). treffer = Ring-Treffer je Baum/Fels (0 = direkt).
WERKZEUGE = {
    "axe": {"art": "holz", "label": "Axe", "stufen": [
        {"label": "Old Hatchet", "treffer": 3, "geld": 40, "rohstoffe": {}, "fisch": None,
         "text": "His father's hatchet. Not sharp, but it has never let go of the handle."},
        {"label": "Forester's Axe", "treffer": 1, "geld": 120, "rohstoffe": {"iron": 2, "timber": 4}, "fisch": "pike",
         "text": "A new head on a hickory handle. One clean stroke per tree."},
        {"label": "Tempered Axe", "treffer": 0, "geld": 220, "rohstoffe": {"iron": 3, "timber": 6}, "fisch": "eel",
         "rosi": True, "vertrauen": 3, "text": "Petru forged it and Rosi hardened the steel. The tree simply comes down."},
    ]},
    "pickaxe": {"art": "stein", "label": "Pickaxe", "stufen": [
        {"label": "Old Pick", "treffer": 3, "geld": 40, "rohstoffe": {}, "fisch": None,
         "text": "Heavy, blunt and honest. The rock decides when it breaks."},
        {"label": "Quarry Pick", "treffer": 1, "geld": 120, "rohstoffe": {"iron": 2, "timber": 4}, "fisch": "barbel",
         "text": "Freshly forged points. One good blow and the rock splits."},
        {"label": "Tempered Pick", "treffer": 0, "geld": 220, "rohstoffe": {"iron": 3, "timber": 6}, "fisch": "zander",
         "rosi": True, "vertrauen": 3, "text": "Tempered twice by Rosi. The stone gives way before you finish the swing."},
    ]},
}

# Koeder bei Petru (Duc 30.10.2026): dauerhaft (kein Verbrauch), 3 Stufen, je Stufe zwei Looks mit gleicher Wirkung, die Wahl
# bleibt jederzeit umschaltbar (kern/koeder.py). Der beste gebaute Koeder gilt; sein Look ersetzt den Schwimmer im Angel-Minispiel.
# zone = breitere goldene Zone (wie der Sammel-Bonus), selten = Gewichtspunkte, die von Stufe 1 auf Stufe 2/3 wandern (seltenerer
# Fisch), warten = Faktor auf die Wartezeit bis zum Biss. Looks = abgenommene Bilder (farm/koeder/<id>.png).
KOEDER = {
    "cork_float": {"stufe": 1, "label": "Cork Float", "geld": 30, "rohstoffe": {"cork": 2, "timber": 1},
                   "text": "A round float carved from oak bark, painted by hand. It doesn't do much. It does it every time.",
                   "zone": 0.03, "selten": {"2": 0, "3": 0}, "warten": 1.0,
                   "looks": [{"id": "koeder_1_1", "label": "Red and white"}, {"id": "koeder_1_4", "label": "Green and white"}]},
    "balsa_float": {"stufe": 2, "label": "Balsa Float", "geld": 70, "rohstoffe": {"cork": 2, "feather": 2, "iron": 1},
                    "text": "A slim balsa float with a gull's feather in the varnish. The golden band is wider and the better fish come closer.",
                    "zone": 0.05, "selten": {"2": 5, "3": 2}, "warten": 0.9,
                    "looks": [{"id": "koeder_2_3", "label": "Red tip, cream body"}, {"id": "koeder_2_4", "label": "Pink tip, blue body"}]},
    "wooden_lure": {"stufe": 3, "label": "Wooden Lure", "geld": 130, "rohstoffe": {"timber": 2, "feather": 3, "iron": 2},
                    "text": "A little wooden fish with a diving lip and two silver hooks. It swims like something alive, and the fish are not clever about that.",
                    "zone": 0.07, "selten": {"2": 9, "3": 6}, "warten": 0.75,
                    "looks": [{"id": "koeder_3_1", "label": "Silver sardine"}, {"id": "koeder_3_3", "label": "Red mullet"}]},
}

# Petrus Werkstatt als Laden (Duc 28.10.2026: freier Laden ab Tag 2). Bisher nur der Reiter Tools; Koeder, Upgrades und
# Fischverkauf docken spaeter hier an. Wird von kochen_eden_rise.py in laeden.json eingetragen und wie alle Ladenzeilen vertont
# (Vertonen_EdenRise.bat). Stimme: wenige Worte, ganze Saetze, Bilder vom Meer (figuren/petru.md). kauf_<werkzeug>_<stufe> =
# seine Zeile bei der Uebergabe.
PETRU_AB_TAG = 2
PETRU_LADEN = {
    "name": "Petru's Workshop", "wer": "petru", "nur_an_land": False, "hintergrund": "corsican_fisherman_workshop.png",
    "text": "Nets, a blue boat on trestles and a radio that only plays Corsican football. Petru sells tools now, because someone has to pay for the diesel.",
    "gruss_stufen": {"gruss": [0, 5]},
    "zeilen": {
        "gruss": [
            "Hm. Sit down, if you like. [sigh] Bastia is losing again, so don't expect much talking from me today.",
            "You came back. [chuckle] Good. Mind the blue boat, the paint on her is still wet.",
            "The tools are on the wall. [clear throat] Look as long as you want, nobody in here is in a hurry.",
        ],
        "kauf_axe_1": ["It was my father's. [sigh] Old, and not very sharp, but it has never once let go of the handle. I'm sorry about the money. Marie, my wife, always did that part."],
        "kauf_pickaxe_1": ["For the rock up in the hills. [clear throat] Swing it slowly at first. The stone will tell you where it wants to break."],
        "kauf_axe_2": ["You brought me a pike. [chuckle] Then you get the good axe. Let the weight do the work, not your shoulders."],
        "kauf_pickaxe_2": ["A barbel. Hm. [sniff] Marie would have baked it with fennel. Here, I forged the head new last night."],
        "kauf_axe_3": ["Rosi hardened the steel and complained the whole time. [laugh] That means she enjoyed it. This edge will outlive both of us."],
        "kauf_pickaxe_3": ["Rosi tempered it twice, to be sure. [chuckle] Don't tell her I said so, but she is better at this than I am."],
        # Koeder (30.10.2026): kauf_koeder_<stufe> = seine Zeile bei der Uebergabe
        "kauf_koeder_1": ["Oak bark from the river. [clear throat] A float is only a promise to the sea. Watch it, not the water."],
        "kauf_koeder_2": ["Balsa, and a gull's feather in the paint. [chuckle] The sea will think it is dinner. Hold the line gently."],
        "kauf_koeder_3": ["Marie called this one the liar. [sigh] It swims like something alive. Be kind to it, it has a short life in the water."],
    },
    "gefuehl": {"gruss": "neutral", "kauf_axe_1": "embarrassment", "kauf_pickaxe_1": "neutral", "kauf_axe_2": "approval",
                "kauf_pickaxe_2": "joy", "kauf_axe_3": "amusement", "kauf_pickaxe_3": "approval",
                "kauf_koeder_1": "approval", "kauf_koeder_2": "amusement", "kauf_koeder_3": "approval"},
}
# Ba Tus Laden hinter dem Hafen (Duc 30.10.2026, docs/wiki/welt/dorf_figuren.md): eigener Satzbau, nie als Witz.
BATU_LADEN = {
    "name": "B\u00e0 T\u01b0's Shop", "wer": "batu", "nur_an_land": True, "hintergrund": "eden_rise_batu_shop.png", "set": "batu_standard",
    "text": "Too many shelves for the room, a wall of amber bottles and a small Virgin Mary with a fresh flower. The pot at the back is always on.",
    "gruss_stufen": {"gruss_fremd": [0, 1], "gruss_freund": [2, 3], "gruss_naehe": [4, 5]},
    "zeilen": {
        "gruss_fremd": ["[clear throat] You again. Good. You are still too thin.", "Look, don't touch. [sigh] Touch means buy.",
                        "Prices are prices. [chuckle] I don't give a discount for handsome."],
        "gruss_freund": ["Con. You ate today? [clear throat] Don't lie, I can see.", "[chuckle] For you I kept the good bottle. It costs the same."],
        "gruss_naehe": ["[chuckle] Con. Sit first. Buying is after.", "[sniff] Your mother called me? No. But she would."],
        "kauf": ["[clear throat] Correct money. Good boy.", "This one you cook slowly. [chuckle] Not like the Italians."],
        "pleite": ["[sigh] No money, no sauce. Soup I give you for free. Soup is different."],
    },
    "gefuehl": {"gruss": "caring", "kauf": "approval", "pleite": "disappointment"},
}

# Bibis Tierstation (Duc 31.10.2026): laut und schnell, aber leise und genau, wenn es um ein Tier geht (figuren/bibi.md).
MOCHIS_LADEN = {
    "name": "Mochi's", "wer": "bibi", "nur_an_land": True, "hintergrund": "eden_rise_mochis_station_voll.png", "set": "Mochis",
    "text": "An old sheep pen above the bay with half a roof, a very neat sign and a bowl of water. Bibi keeps a field book here, and she is the only one who can read it.",
    "gruss_stufen": {"gruss_fremd": [0, 1], "gruss_freund": [2, 3], "gruss_naehe": [4, 5]},
    "zeilen": {
        "gruss_fremd": [
            "Mind the bowl! [laugh] Everybody kicks the bowl. Sorry. I do that. Is that why you came up?",
            "There are tracks by the road again. [sniff] I wrote it all down. You can read it if you can read my writing.",
            "Keep your hands where they can see them. [clear throat] I don't mean me. I mean them.",
        ],
        "gruss_freund": [
            "You're back! [laugh] Good. I need someone to hold things, and you've got arms.",
            "Look in the book. [sigh] I've got more trails than legs. Pick one and be nice to it.",
            "Don't ask how I slept. [chuckle] Ask how they slept. They slept great.",
        ],
        "gruss_naehe": [
            "There you are. [chuckle] There's coffee. It's terrible. I made it for you specially.",
            "I used to think I needed the whole world for this. [sigh] Turns out it fits in a sheep pen.",
            "They know your boots now. [laugh] Listen, you can hear them getting up.",
        ],
    },
}

# Danzels Laden an der Piazza (Duc 30.10.2026): laut, bis es um Stoff geht, dann ruhig und genau (figuren/danzel.md).
DANZEL_LADEN = {
    "name": "Le Th\u00e9\u00e2tre Rouge", "wer": "danzel", "nur_an_land": True, "hintergrund": "corsican_village_festa.png", "set": "danzel_B",
    "text": "The old room on the piazza with the good window. One red curtain, one mannequin, and a man who measures you with his eyes before he says hello.",
    "text_allein": "The old room on the piazza with the good window. One red curtain, one mannequin, and a man who works alone and doesn't look up until you speak.",
    "gruss_stufen": {"gruss_fremd": [0, 1], "gruss_freund": [2, 3], "gruss_naehe": [4, 5]},
    "zeilen": {
        # Trio zerbrochen (E-112): knapp und ernst, statt der Stufen (eden.py laden_auftritt)
        "gruss_allein": [
            "Come in. [sigh] Mind the pins.",
            "It's you. [clear throat] What do you need?",
            "Look around. [sigh] There's only me here now.",
        ],
        "gruss_fremd": [
            "Welcome to Le Th\u00e9\u00e2tre Rouge, the finest house on the – [clear throat] the only house. Please don't touch the silk.",
            "You came in! [gasp] People mostly stand at the window. Looking is free. I checked.",
            "Everything in here is cut by hand. My hand. [clear throat] So if a seam is wrong, please tell me quietly.",
        ],
        "gruss_freund": [
            "It's you. Good. [chuckle] Stand straight, I'm measuring you. Terrible shoulders. I can work with that.",
            "Nobody in this village owns a proper hem. [sigh] I have decided to take that personally.",
            "Come in, come in. [chuckle] Mind the pins. The pins are the only ones here who are on my side.",
        ],
        "gruss_naehe": [
            "There you are. [chuckle] I kept something back for you. Don't tell the others I have favourites. I have one.",
            "In Paris they said my work was fine. [sigh] Here a fisherman cried over a waistcoat. I'll take the fisherman.",
            "Sit. No, not there, [laugh] that's the mannequin. She's a better customer than you, but I like you more.",
        ],
        "kauf": [
            "Look at the seam, not the price. [clear throat] The price is only a number. The seam took me two nights.",
            "Sold! A triumph! A – [sniff] yes. Thank you. That pays for the window.",
            "I'll wrap it. [chuckle] I always wrap it. Paper is the one thing here that doesn't need altering.",
        ],
        "kauf_intim": [
            "I won't ask who it's for. [clear throat] I only need her size. No. Don't tell me. Just take it.",
            "Silk shows every mistake. [sigh] So be careful with it. And with her.",
        ],
        "pleite": ["You can't afford it. [sigh] Neither can I, and I made it."],
    },
    "gefuehl": {"gruss": "neutral", "gruss_allein": "sadness", "gruss_naehe": "joy", "gruss_freund": "amusement", "kauf": "approval", "kauf_intim": "embarrassment", "pleite": "amusement"},
}
# Nach Weg B in den Bergen (Duc + Brain Trust 29.10.2026): der Laden bleibt offen, aber dunkel - kein Radio, keine Geschichten,
# Fisch 20 % billiger (kern/abbau.petru_kalt). Bis Laetitias Karte und die Versoehnung (ereignisse_berge.py bg_b_versoehnung).
PETRU_LADEN["text_kalt"] = "The radio on the workbench is off. Petru serves you without looking up."
PETRU_LADEN["zeilen"].update({
    "kalt_gruss": ["Hm. [sigh] What do you need.", "[clear throat] Say what you want. Then go.",
                   "The tools are where they always are. [sniff]"],
    "kalt_kauf": ["Hm. [sigh] Take it."],
    "kalt_fisch": ["[clear throat] Put it on the scale. Don't talk.", "I'll give you less. [sigh] You know why."],
})
PETRU_LADEN["gefuehl"].update({"kalt_gruss": "disapproval", "kalt_kauf": "disapproval", "kalt_fisch": "anger"})
# Petru kauft Fisch (Brain Trust, Duc 28.10.2026): beim ersten Verkauf einer Art sein Satz (Gruppe fisch_<id>), danach Notiz im
# Journal. Saetze und Anteile je Seltenheit stehen in petru_fische.py (Abnahme docs\abnahme\petru_fische).
import petru_fische as _pf  # noqa: E402
PETRU_LADEN["zeilen"].update({"fisch_" + fid: [satz] for fid, satz in _pf.SAETZE.items()})
PETRU_LADEN["gefuehl"].update({"fisch_" + fid: _pf.GEFUEHL for fid in _pf.SAETZE})
PETRU_FISCH_ANTEIL = {str(k): v for k, v in _pf.PETRU_ANTEIL.items()}
