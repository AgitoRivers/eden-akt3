# -*- coding: utf-8 -*-
r"""Combat data for module eden_rise (stage 4a, 24.10.2026) - skills, weapons, armor, enemies and encounters for
kern\kampf.py. Rules live in kern\kampf.py, numbers here. Source: docs\wiki\systeme\kampf.md ("Spezialangriffe, Brennen und
Kombos", "Formeln", "Waffen", "Rüstung", "Gesamt-Balancing") and the simulation werkzeuge\kampf_balance_v5.py.
Player-visible texts are English (25.10.2026, docs\wiki\STIL.md), keys and ids English (code ids of the specials
= their game names); the working names (work) stay German for chat and docs.

Format
  BASIC[id]       label, attr, cost, probe, text, effect   (the four basic skills, always available)
                  effect without probe: {extra, exhaust, reveal}
                  effect with probe:    {erfolg|kritisch|fehlschlag|patzer: {fassung, weaken, exposed}}
                  advantage_with / free_with: a strength of the persona (charme, koepfchen)
  SPECIALS[id]    code (K3 ...), path (K/L/W/M), tier (3/5/7/9), label (game name), work (working name for chat/docs),
                  cost, text; answer = only against an announced enemy special, strong_only = only against a strong one,
                  finisher = only against an exhausted enemy
  WEAPONS[id]     label, dmg, element (wasser/feuer/erde/luft/None), kind (klinge/stumpf/messer/stange/fern), slots,
                  rarity, sig (signature from the simulation), price, source
  ARMORS[id]      label, prot, resist (element: damage x0.7 and immune to its state), heavy, bite, bonus, rarity, source
  ENEMIES[id]     name, sprite, cls (mensch/tier/monster/maschine/flieger), element, tier (laestig/gefaehrlich/toedlich/
                  albtraum: pattern, parade tempo, flee DC), specials {w1/w2/s1/s2: {label, icon, bonus, effect,
                  dodge_only}}, attack {label, icon}, weakness, immune {attr: reason}, flee_at (share of max LP),
                  parade (sprite/skala/ring), boss
  ENCOUNTERS[id]  title, goal, image, enemy, level (number or "duc"), training, xp_factor, flee_allowed,
                  outcomes {ko, aufgabe, entkommen, flucht, niederlage: {text, folgen}}, test

    python kaempfe_eden_rise.py   -> module\eden_rise\kaempfe.json (validated)
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(os.path.dirname(HERE))    # werkzeuge\eden_rise -> Eden
TARGET = os.path.join(EDEN, "module", "eden_rise", "kaempfe.json")
IMAGES = os.path.join(EDEN, "module", "eden_rise", "kampf")
ATTRS = ["strength", "charm", "empathy", "perception", "cunning", "courage"]
STRENGTHS = ["koepfchen", "kueche", "charme", "handwerk"]
ENDS = ["ko", "aufgabe", "entkommen", "flucht", "niederlage"]
ELEMENTS = [None, "wasser", "feuer", "erde", "luft", "alle"]
KINDS = ["klinge", "stumpf", "messer", "stange", "fern"]
CLASSES = ["mensch", "tier", "monster", "maschine", "flieger"]
TIERS = ["laestig", "gefaehrlich", "toedlich", "albtraum"]
RARITIES = ["gewoehnlich", "selten", "episch", "legendaer", None]
ARMOR_SIGS = ["standfest", "fliessend", "glut", "leicht", "alles"]
SIGNATURES = [None, "every_strom", "every_quake", "every_burn", "first_strom", "crit_wet_quake", "counter15", "burn3", "twin"]
EFFECTS = [None, "nass", "brennend", "brennend3", "blutend", "erschuettert", "strom", "geschwaecht", "geblendet",
           "geblendet2", "ungedeckt", "betaeubt", "silence", "stamina", "drain", "scent", "pierce",
           "heal3", "heal5", "buff4", "buff3x2", "buff4x2", "armor2x2", "armor3x2", "wall", "dodge", "rudel"]
PATHS = {"K": "strength", "L": "cunning", "W": "perception", "M": "courage", "H": "empathy"}
FOLGEN_KEYS = {"flag", "flag_weg", "item", "geld", "codex", "wert", "delta", "text"}

# ------------------------------------------------------------------ basic skills (decided 20.10.; 26.10.: Heavy Strike
# removed - there are only special attacks now, Maxwell teaches Mistral instead, kern/tutorial.py LEHRT)
BASIC = {
    "reden": {
        "label": "Talk", "attr": "charm", "cost": 2, "probe": True, "advantage_with": "charme",
        "text": "Talk them down. Lowers their composure (anyone who can listen; animals can't).",
        "effect": {"erfolg": {"fassung": 6}, "kritisch": {"fassung": 9}, "fehlschlag": {}, "patzer": {"exposed": True}}},
    "einschuechtern": {
        "label": "Intimidate", "attr": "courage", "cost": 2, "probe": True,
        "text": "Stand tall and look dangerous: their next two attacks are weaker, and they lose composure. "
                "Works on most animals too.",
        "effect": {"erfolg": {"weaken": True, "fassung": 3}, "kritisch": {"weaken": True, "fassung": 6},
                   "fehlschlag": {}, "patzer": {"exposed": True}}},
    # Spot Weakness removed (Duc 29.10.2026, Kloster simulation: a whole turn for +4 cost more than it brought).
    # W3 Point de Mire exhausts, the strength Koepfchen shows the weakness from the first round (kern/kampf.starten).
}

# ------------------------------------------------------------------ the 16 specials (decided 22.-24.10.)
def S(code, label, work, cost, text, **kw):
    return dict({"code": code, "path": code[0], "tier": int(code[1:]), "label": label, "work": work, "cost": cost,
                 "text": text}, **kw)


SPECIALS = {
    "mistral": S("K3", "Mistral", "Erschütterer", 3, "+4 damage, and the enemy is shaken for 2 rounds (no protection)."),
    "ressac": S("K5", "Ressac", "Konterwelle", 3, "Answer to their special attack: a counter (×2 against a wet "
                "enemy); against a strong one they are also weakened.", answer=True),
    "libeccio": S("K7", "Libeccio", "Windrüstung", 2, "For 2 rounds you take half damage, and every perfect parry "
                  "shakes them."),
    "lame_de_fond": S("K9", "Lame de Fond", "Riesenwelle", 4, "Finisher against an exhausted enemy: ×2, "
                      "against a shaken one ×3.", finisher=True),
    "doppio_gioco": S("L3", "Doppio Gioco", "Doppelschnitt", 3, "Two cuts at 70 % each."),
    "sotto_voce": S("L5", "Sotto Voce", "Abtauchen", 2, "Answer to their special attack: your next attack is a sure "
                    "crit; against a strong one their hit is also halved.", answer=True),
    "vendetta": S("L7", "Vendetta", "Blutschnitt", 3, "A cut at 30 %, then they bleed (not machines)."),
    "omerta": S("L9", "Omertà", "Gnadenstoß", 4, "Finisher against an exhausted enemy: crit ×2.5 (×3.5 with a sure "
                "crit), +25 % per condition, up to 4.", finisher=True),
    "point_de_mire": S("W3", "Point de Mire", "Zielmarke", 2, "They are exhausted for 3 rounds (below Perception 4: until "
                       "your next turn)."),
    "bonaccia": S("W5", "Bonaccia", "Ruhepuls", 2, "Answer to their special attack: catch a strong one completely "
                  "and strike back, halve a weak one and strike back at half strength (below Perception 4: only halved).",
                  answer=True),
    "phare": S("W7", "Phare", "Leuchtfeuer", 3, "Against a strong special attack: blinds them and they skip 1 "
               "round (2 if charged with current); below Perception 4 only at 15 % per point.", answer=True, strong_only=True),
    "pluie_d_etoiles": S("W9", "Pluie d'Étoiles", "Sternsalve", 4, "Finisher: 3 hits at 85 % (full damage against flyers)."),
    "scirocco": S("M3", "Scirocco", "Glutschlag", 3, "+4 damage and one burn stack, but afterwards you are exposed."),
    "retour": S("M5", "Retour de Flamme", "Rachefeuer", 2, "Charges your weapon: their next attack is met with a "
                "counter. Parry it for ×1.5 and a burn stack (×2 against a strong special attack), miss it for ×0.5."),
    "furia": S("M7", "Furia", "Flammenrausch", 3, "One hit right away, then 2 rounds at ×1.3, and every hit adds a "
               "burn stack. You catch fire yourself and cannot defend."),
    "vulcano": S("M9", "Vulcano", "Feuersturm", 4, "Finisher: one blow per burn stack on the enemy at 60 %, ignores "
                 "protection and uses up every stack. You skip 1 round afterwards."),
    # Healer (H, Empathy - Duc + Brain Trust 26.10.2026): Nonna Fiora teaches Elicriso in the Kloster (Story)
    "elicriso": S("H3", "Elicriso", "Heilöl", 3, "Heals 30 % of your HP and soothes a burn or a bleeding wound."),
    "ponente": S("H5", "Ponente", "Westwind", 3, "For 3 rounds you heal 10 % of your HP every round, and your parry "
                 "window is 10 % wider."),
    "risveglio": S("H7", "Risveglio", "Erwachen", 4, "Heals 80 % of your HP. Once per fight."),
    "arcangelo": S("H9", "Arcangelo", "Erzengel", 4, "If you fall in this fight, you rise again with half your HP. "
                   "Once per fight."),
}

# ------------------------------------------------------------------ weapons (docs table; Harpune 9 + Doppelflinte 7 per Gesamt-Balancing)
def W(label, dmg, element, kind, rarity, source, slots=1, sig=None, price=None):
    return {"label": label, "dmg": dmg, "element": element, "kind": kind, "slots": slots, "rarity": rarity,
            "sig": sig, "price": price, "source": source}


# 24.10.2026 (Duc): exactly five fixed weapons, one per kind (docs\wiki\systeme\aufruestung.md). Faust and all story weapons are
# gone (their text lives in the docs; they return later as Erweiterungen/Verstaerkungen/Charms). Upgrades come with Rosi's workshop.
def W5(label, untertitel, dmg, kind, source, slots=1, element=None, sig=None):
    w = W(label, dmg, element, kind, "gewoehnlich", source, slots=slots, sig=sig)
    w["untertitel"] = untertitel
    return w


WEAPONS = {
    "sword": W5("Riposte", "Cavalry Sabre", 5, "klinge", "Wreck dive, week 3 (open)", element="wasser"),
    "bat": W5("Terremoto", "Baseball Bat", 2, "stumpf", "Rosi, at the harbour after the workshop fire", element="erde"),
    "knife": W5("Sussurro", "Combat Knife", 2, "messer", "Gennaro's cell, the grotto", element="luft"),
    "spear": W5("Le Large", "Boar Spear", 4, "stange", "Madame Casanova, after her mission (Act 2)", element="feuer"),
    "gun": W5("Gemelli", "Double Rifle", 3, "fern", "Captain Holm, before the siege (open)", slots=2, sig="twin"),   # no element, no stone: twin barrels
}
# 25.10.2026 (Duc): Maxwell's training gear - the deck scrubber ("Parry the dirt"). Never owned or unlocked, only the
# encounters with "weapon": "mop" hand it out; sprite DucErdeMop.
WEAPONS["steel_mop"] = dict(W5("Steel Mop", "Maxwell's own, by Rosi", 5, "stumpf", "Rosi, day 19"), training_only=True)    # nie Ducs Waffe (Duc 01.11.2026)
WEAPONS["mop"] = dict(W5("Deck Scrubber", "Maxwell's training gear", 0, "stumpf", "Training with Maxwell only"), training_only=True)
# Basisstein je Waffe (Stufe 0, schon eingebaut) und die zwei Upgrade-Steine, dazu der feste Erklaersatz von Rosi.
STEINE = {"bat": ["Granit", "Jade", "Smaragd"], "spear": ["Lavastein", "Topas", "Rubin"],
          "sword": ["Seeglas", "Aquamarin", "Saphir"], "knife": ["Quarz", "Amethyst", "Opal"]}
STEIN_SATZ = {
    "bat": "There's a chunk of granite from the harbour wall in the barrel. It's heavy, and that's the whole trick.",
    "spear": "A piece of lava stone from the coast sits in the spearhead. It holds heat longer than you'd think.",
    "sword": "Sea glass from the harbour is set in the grip. Smooth, a little wet, and it never lets go of the water.",
    "knife": "A small quartz sits in the handle. Every cut leaves a spark, and no, I won't explain how.",
    "gun": "Two barrels, no stone. On the first shot and on every counter, both fire."}
for _wid, _w in WEAPONS.items():
    if _wid in STEINE:
        _w["stein"] = STEINE[_wid]
    if _wid in STEIN_SATZ:                      # the training mop and other test weapons have no stone story
        _w["eigenschaft"] = STEIN_SATZ[_wid]
START_WEAPON = "bat"   # Duc always holds a weapon
# Duc owns only the bat and Terra Scura at the start. Everything else is unlocked by an event that sets the flag
# "waffe_<id>" / "jacke_<id>" (kern\kampf.py besitz, freischalten); who hands out what: docs/wiki/systeme/items.md.
START_GEAR = {"weapons": [], "armors": ["jacket_earth"]}      # Terremoto: Rosi wirft ihn im Hafen zu (Flag waffe_bat)
FALLBACK_WEAPON = "mop"      # Kaempfe vor Terremoto: Duc nimmt den Holzschrubber

# Wo die Waffe endet, je Sprite und Pose (werkzeuge/muendung_messen.py): Muendungsfeuer im Client
_MF = os.path.join(EDEN, "module", "eden_rise", "muendung.json")
MUENDUNG = json.load(open(_MF, encoding="utf-8")) if os.path.isfile(_MF) else {}

# ------------------------------------------------------------------ Maxwell als zweite Spielfigur (Duc 01.11.2026, kern/kampf._held_werte)
# Effekte und Klaenge kommen aus dem Labor (EFFEKT_ID im Client): Rauch, Explosion, Buff, nichts Neues.
HELDEN = {"maxwell": {
    "name": "Mr. Maximum", "sprite": "MaxwellSteelMop", "fx_set": "DucMaxwellSteelMop", "waffe": "steel_mop", "pfad": "K",
    "lp_faktor": 1.2, "ausdauer_plus": -1, "level_basis": 5, "level_schritt": 2,
    "attribute": {"strength": 5, "cunning": 1, "perception": 2, "courage": 5, "empathy": 3, "charm": 3},
    "ruestung": {"id": "steward_shirt", "label": "Steward Shirt", "untertitel": "No sleeves", "prot": 2, "resist": None, "heavy": False, "bite": 0.0, "bonus": {},
                 "rarity": "gewoehnlich", "sig": None, "eigenschaft": "", "source": "Chiara"},
    "tasche": ["verbandskasten", "verbandskasten", "verbandskasten", "espresso_single", "espresso_single", "espresso_single", "grenade_fire", "grenade_concussion"],
    "specials": {
        "parry_the_dirt": S("K3", "Parry the Dirt", "Konter", 2, "He plants his feet and waits: their next attack gets a counter. Parry it for ×1.5, a strong one for ×2. Miss it for ×0.5."),
        "maximum": S("K5", "Maximum", "Wucht", 3, "+5 damage, ×1.5 against machines, and the enemy is shaken for a round (no protection)."),
        "approves": S("K7", "Mr. Maximum Approves", "Ansporn", 1, "+3 stamina, and his next hit is a sure crit."),
    }}}

# ------------------------------------------------------------------ armor (1 slot, swapped only in the cabin)
def A(label, untertitel, prot, source, sig, eigenschaft, resist=None, heavy=False):
    return {"label": label, "untertitel": untertitel, "prot": prot, "resist": resist, "heavy": heavy, "bite": 0.0,
            "bonus": {}, "rarity": "gewoehnlich" if prot < 5 else "episch", "sig": sig, "eigenschaft": eigenschaft,
            "source": source}


ARMORS = {
    "jacket_earth": A("Terra Scura", "Biker Jacket", 3, "Starting gear", "standfest",
                      "Steadfast: protection +1, defending gives protection +2, and you are never shaken."),
    "jacket_water": A("Meramie", "Navy Pea Coat", 2, "Petru, after the mountains", "fliessend",
                      "Flowing: parry window +5 %, and a counter after a perfect parry does ×1.1."),
    "jacket_fire": A("Incendio", "Burgundy Pea Coat", 2, "Danzel, The Red Trio", "glut",
                     "Embers: you hit +2 harder for every burn stack on the enemy."),
    "jacket_air": A("Zéphyr", "White Pea Coat", 2, "Unlockable (open)", "leicht",
                    "Light: stamina +2, and fleeing is easier."),
    "cyber_armor": A("Citadelle", "Cyber Armor", 5, "After defeating Alon", "alles",
                     "All-in-one: protects against every element, the first hit in each fight counts only half, "
                     "parry window −10 %.", resist="alle", heavy=True),
}
START_ARMOR = "jacket_earth"

# ------------------------------------------------------------------ Rosi's workshop (25.10.2026, docs\wiki\systeme\aufruestung.md)
# Two upgrades per weapon/jacket (+1 damage or +1 protection each). One piece per night, handed in through the cabin
# ("Für Rosi", no action); next morning Rosi texts Duc. The workshop opens with the flag set by the repair event.
# The texts are fixed, English (game language) and get voiced beforehand - the language model invents none of them.
WERKSTATT = {
    "flag": "werkstatt_offen",
    "event": "rosi_werkstatt_offen",
    "stufen": [{"geld": 150}, {"geld": 400}],                 # Duc 28.10.2026 (beute.md 3b), vorher 120/240
    # Material je Stufe. Jacken: Steel Plate, Titanium Plate. Waffen: Rosi tauscht den eingebauten Basisstein gegen den
    # naechsten Stein desselben Elements (endgueltig, kein Zurueck). Gemelli hat keinen Stein und nimmt Metall: Kupfer, dann Silber (Barren).
    "material": {"armor": ["steel_plate", "titanium_plate"],
                 "weapon": {"bat": ["jade", "smaragd"], "spear": ["topas", "rubin"], "sword": ["aquamarin", "saphir"],
                            "knife": ["amethyst", "opal"], "gun": ["kupfer", "silber"]}},
    "materialien": {"steel_plate": "Steel Plate", "titanium_plate": "Titanium Plate", "jade": "Jade", "smaragd": "Emerald",
                    "topas": "Topaz", "rubin": "Ruby", "aquamarin": "Aquamarine", "saphir": "Sapphire",
                    "amethyst": "Amethyst", "opal": "Opal", "kupfer": "Copper", "silber": "Silver"},
    "text_zu": "The workshop is still wrecked after the explosion.",
    "texte": {
        "sword": ["Riposte has aquamarine in the grip now. Clear as the water at the harbour, and it balances much better. It's waiting in your cabin.",
                  "Sapphire for Riposte. I balanced it on one finger and it stayed. Do not tell Totò that I said it's pretty."],
        "bat": ["Terremoto has jade in the barrel now. Heavier, tougher, and it still goes bang. It's waiting in your cabin.",
                "Emerald this time. I tested it on a pallet and the pallet gave up. Come and get it, Maestro."],
        "knife": ["Sussurro has amethyst in the handle now. It sparks more than the quartz did, so keep it away from the fuel.",
                  "Opal in Sussurro's handle. It flashes every colour when it cuts. I may have stared at it for ten minutes."],
        "spear": ["Le Large has topaz in the spearhead. It glows a little when it's warm. Don't ask me why, I'm still enjoying it.",
                  "A ruby in the spearhead now. The boar will see it coming and still lose. It's in your cabin."],
        "gun": ["Gemelli has copper in the barrels now. It runs warm and it still kicks like a mule, I kept that part. It's in your cabin.",
                "Silver this time, all the way down both barrels. Come and pick it up before I get attached."],
        "jacket_earth": ["Terra Scura is stitched, lined, and heavier in a good way. It's waiting in your cabin.",
                         "Terra Scura is done. I hit it with a hammer to test it. The hammer lost."],
        "jacket_water": ["Meramie is dry, mended, and smells less like the sea. Slightly. It's in your cabin.",
                         "Meramie is finished. New buttons, new lining, same attitude. Wear it in the rain, I dare you."],
        "jacket_fire": ["Incendio has fresh seams and a patch where the burn was. I think it looks cooler now. It's in your cabin.",
                        "Incendio is done. It's warm. It's very warm. Maybe don't wear it in the engine room."],
        "jacket_air": ["Zéphyr is lighter and tighter at the cuffs. You'll run faster. Not that you should have to.",
                       "Zéphyr is finished. It weighs about as much as a promise. Go and make some trouble in it."],
        "cyber_armor": ["Citadelle is open on my bench. Every panel. I've never seen a better armor. Don't tell Alon I said that.",
                        "Citadelle is done. All panels re-seated, all joints oiled. Wear it like you earned it, because you did."]},
}

# ------------------------------------------------------------------ Chips (Erweiterungen, 25.10.2026)
# Lore: Alons Halsbaender (Behaviour Control Units) und Agenten-Technik. Rosi schneidet den Sender heraus und baut die Chips so um,
# dass sie nur Duc helfen. Funde sind Schaltplaene: sie schalten eine Familie frei oder heben sie auf eine bessere Stufe (ersetzt
# die alte). Vor Rosis Werkstatt (Akt 2) sind Funde "unidentifiziert" und wirken nicht. Katalog: erweiterungen_eden_rise.py.
CHIPS = {
    "verkauf": 10,                                                     # EUR je Stufe fuer schlechtere/gleiche Funde
    "text": {"unbekannt": "You found a strange chip. Maybe Rosi can make something out of it.",
             "neu": "New module found: {name}. Rosi can make use of it.",
             "besser": "Better module: {name}. Rosi folds the old one into it.",
             "schlechter": "You already have a better {familie}. Sold the spare for {geld} EUR.",
             "gleich": "You already have {name}. Sold the spare for {geld} EUR."},
    # Rosi sagt je Kategorie etwas anderes, wenn sie einen Chip einbaut oder ersetzt (Entwurf, Duc ergaenzt noch)
    "rosi": {"wucht": "More weight behind it. Don't drop it on your foot.",
             "praezision": "I tuned the sight. Try not to miss on purpose.",
             "technik": "Faster hands. Don't ask what I did to the wiring.",
             "konter": "Now it hits back harder. I like it.",
             "zustand": "It does something nasty on contact. I love that.",
             "element": "I rebuilt the shell for you. Fire, water, whatever you like. One at a time, please.",
             "schutz": "Thicker lining. I sewed it myself. Badly, but it holds.",
             "parade": "Your hands will feel steadier. That's the chip, not you.",
             "ausdauer": "More air in your lungs. Mind the stairs now.",
             "erholung": "It patches you up a little between the bruises.",
             "auftritt": "Stand straight and look like you mean it. The chip does the rest.",
             "abwehr": "Whatever it was made to hurt you with, it won't work now.",
             "aufklaerung": "It listens to their collars. You'll know who's out there before they know you are."},
    # Drops: Gegner-Typ -> (Familie, Stufe). Tiere mit Halsband liefern Stufe 1, Agenten Stufe 2, "Alpha" ist Platzhalter fuer Stufe 3.
    "drops": {"ratte_alpha": ["zustand_blutend", 1], "hund_alpha": ["ausdauer", 1], "keiler": ["wucht", 1],
              # Kloster (26.10.2026): der Alpha-Keiler traegt den seltenen Chip (Ausgleich fuer alle, die den Loewen verschonen),
              # die Affen tragen Halsbaender; der Loewen-Chip kommt aus der Szene nach dem Kampf (Story), nicht als Drop
              "keiler_kloster": ["wucht", 2], "affe": ["technik", 1],
              # Scout (26.10.2026): Stufe I schenkt Rosi bei der Wiedereroeffnung, Stufe II tragen die wilden Hunde im Rudel,
              # Stufe III kommt spaeter von Agenten (noch kein Gegner)
              "hunde_paar": ["scout", 2]},
}

# ------------------------------------------------------------------ enemies for act 1 (values from kampf_balance_v3.E)
def SP(label, icon, bonus=0, effect=None, dodge_only=False):
    return {"label": label, "icon": icon, "bonus": bonus, "effect": effect, "dodge_only": dodge_only}


NO_TALK_ANIMAL = {"charm": "Animals don't understand you."}
ENEMIES = {
    "taschendieb": {
        "name": "Pickpocket", "sprite": "Thief", "cls": "mensch", "element": None, "tier": "laestig",
        "attack": {"label": "Punch", "icon": "🗡"},
        "specials": {"w1": SP("Knife Jab", "🔪", bonus=2)},
        "weakness": "charm", "immune": {}, "flee_at": 0.25, "parade": "sprite"},
    "moewe": {
        "name": "Seagull", "sprite": "Seagull", "cls": "flieger", "element": "luft", "tier": "laestig",
        "attack": {"label": "Peck", "icon": "🪶"},
        "specials": {"w1": SP("Dive", "💨", bonus=3, dodge_only=True)},
        "weakness": "courage", "immune": dict(NO_TALK_ANIMAL), "flee_at": 0.2, "parade": "sprite"},
    "ratte": {
        "name": "Rat", "sprite": "Rat", "cls": "tier", "element": "erde", "tier": "laestig",
        "attack": {"label": "Scratch", "icon": "🐾"},
        "specials": {"w1": SP("Bite", "🦷", bonus=2)},
        "weakness": "courage", "immune": dict(NO_TALK_ANIMAL), "parade": "skala",
        "halsband": False},                                  # Scout chip I hears collars only (Items 26.10.2026)
    "pirat": {
        "name": "Pirate", "sprite": "Pirate", "cls": "mensch", "element": "wasser", "tier": "laestig",
        "attack": {"label": "Cutlass Slash", "icon": "🗡"},
        "specials": {"w1": SP("Splash of Seawater", "🌊", effect="nass")},
        "weakness": "courage", "immune": {}, "parade": "sprite"},
    "fackelpirat": {
        "name": "Pirate with a Torch", "sprite": "PirateTorch", "cls": "mensch", "element": "feuer", "tier": "gefaehrlich",
        "attack": {"label": "Slash", "icon": "🗡"},
        "specials": {"w1": SP("Torch Strike", "🔥", bonus=3), "s1": SP("Burst of Flame", "🔥🔥", bonus=6, effect="brennend")},
        "weakness": "perception", "immune": {}, "parade": "sprite"},
    "maxwell": {
        "name": "Maxwell", "sprite": "MaxwellSports", "cls": "mensch", "element": None, "tier": "gefaehrlich",
        "attack": {"label": "Jab", "icon": "👊"},
        "specials": {"w1": SP("Power Pose", "💪", effect="buff3x2"),
                     "s1": SP("Maximum Hammer", "👊👊", bonus=9, effect="stamina")},
        "weakness": "charm", "immune": {"courage": "Maxwell just laughs. “Mr. Maximum fears nothing, brother!”"},
        "parade": "sprite"},
    # Hafenkampf Tag 2 (25.10.2026, docs/wiki/welt/drehbuch_hafenkampf.md): je Welle das Alpha-Tier, das Rudel ist ein
    # Sonderangriff. Gegner-Regeln (E-045/E-046): Landtiere = Erde, immun gegen Reden; Alphas haben keine Schwaeche
    # und sind immun gegen Einschuechtern - Ausnahme Ratte/Hund: erster Ernstfall, Einschuechtern soll wirken.
    "ratte_alpha": {
        "name": "Alpha Rat", "sprite": "RatAlpha", "cls": "tier", "element": "erde", "tier": "laestig",
        "attack": {"label": "Scratch", "icon": "🐾"},
        "specials": {"w1": SP("Bite", "🦷", bonus=2), "s1": SP("The Pack Joins In", "🐀🐀", bonus=4)},
        "weakness": None, "immune": dict(NO_TALK_ANIMAL), "flee_at": 0.2, "parade": "skala"},
    "hund_alpha": {
        "name": "Alpha Dog", "sprite": "DogAlpha", "cls": "tier", "element": "erde", "tier": "gefaehrlich",
        "attack": {"label": "Snap", "icon": "🦷"},
        "specials": {"w1": SP("Pounce", "🐾", bonus=3), "s1": SP("The Pack Circles", "🐕🐕", bonus=5,
                                                                        effect="erschuettert")},
        "weakness": None, "immune": dict(NO_TALK_ANIMAL), "flee_at": 0.2, "parade": "sprite"},
    "keiler": {
        "name": "Boar", "sprite": "WildschweinKeiler", "cls": "tier", "element": "erde", "tier": "gefaehrlich",
        "attack": {"label": "Tusks", "icon": "🐗"},
        "specials": {"w1": SP("Snort", "💨", effect="geschwaecht"), "s1": SP("Charge", "🐗💥", bonus=7)},
        "weakness": None, "flee_at": 0.25, "parade": "sprite",
        "immune": dict(NO_TALK_ANIMAL, courage="The boar just lowers its head. Threats don't impress it.")},
    # Kloster San Martinu (Akt 2, docs/wiki/welt/ortskapitel_kloster.md): Macchia = Erde. Grauzonen-Regel E-073: Tiere
    # werden verschont - Halsband bricht, Chip faellt, sie fliehen. Zweiergegner wie im Hafen: das zweite Tier ist der
    # starke Sonderangriff (die Engine kennt einen Gegner je Kampf).
    "schlange": {
        "name": "Snake", "sprite": "Snake", "cls": "tier", "element": "erde", "tier": "laestig",
        "attack": {"label": "Bite", "icon": "🐍"},
        "specials": {"w1": SP("Venom", "🟢", bonus=1, effect="geschwaecht")},
        "weakness": "courage", "immune": dict(NO_TALK_ANIMAL), "flee_at": 0.25, "parade": "skala", "halsband": False},
    "keiler_kloster": {
        "name": "Alpha Boar", "sprite": "WildschweinKeiler", "cls": "monster", "element": "erde", "tier": "gefaehrlich",
        "attack": {"label": "Tusks", "icon": "🐗"},
        "specials": {"w1": SP("Snort", "💨", effect="geschwaecht"), "s1": SP("Charge", "🐗💥", bonus=8)},
        "weakness": None, "flee_at": 0.2, "parade": "sprite", "boss": True,
        "immune": dict(NO_TALK_ANIMAL, courage="The boar just lowers its head. Threats don't impress it.")},
    "hund_wild": {
        "name": "Feral Dog", "sprite": "Dog", "cls": "tier", "element": "erde", "tier": "gefaehrlich",
        "attack": {"label": "Snap", "icon": "🦷"},
        "specials": {"w1": SP("Pounce", "🐾", bonus=3), "s1": SP("Tears at the Leg", "🦷🦷", bonus=5, effect="blutend")},
        "weakness": "courage", "immune": dict(NO_TALK_ANIMAL), "flee_at": 0.25, "parade": "sprite"},
    "affe": {
        "name": "Ape", "sprite": "Ape", "cls": "tier", "element": "erde", "tier": "gefaehrlich",
        "attack": {"label": "Fist", "icon": "✊"},
        "specials": {"w1": SP("Throws a Rock", "🪨", bonus=3, dodge_only=True), "s1": SP("Frenzy", "💢", bonus=6)},
        "weakness": "perception", "immune": dict(NO_TALK_ANIMAL), "flee_at": 0.2, "parade": "ring"},
    "loewe_schwarz": {
        "name": "The Black Lion", "sprite": "LionPlated", "cls": "monster", "element": "erde", "tier": "toedlich",
        "attack": {"label": "Claws", "icon": "🐾"},
        "specials": {"w1": SP("Roar", "🦁", effect="geschwaecht"), "s1": SP("Leap", "🦁💥", bonus=9, effect="erschuettert")},
        "weakness": None, "parade": "sprite", "boss": True,
        "immune": dict(NO_TALK_ANIMAL, courage="The lion looks straight through you. It is past being afraid.")},
}

# Parry zone per enemy (Duc + Brain Trust 26.10.2026): where the gold sits on the parry bar, in %. 55-85 only - never
# at the start, that would be mean. The marker still reaches the gold exactly at the blow; an early zone just makes it
# run slower. The position fits the animal: the snake strikes very late, the boar charges early. Default 75.
PARADE_ZIEL_MIN, PARADE_ZIEL_MAX, PARADE_ZIEL_STD = 55, 85, 75
PARADE_ZIEL = {"taschendieb": 70, "moewe": 80, "ratte": 70, "pirat": 70, "fackelpirat": 65, "maxwell": 75,
               "ratte_alpha": 70, "hund_alpha": 75, "keiler": 60, "schlange": 85, "keiler_kloster": 60, "hund_wild": 75,
               "affe": 65, "loewe_schwarz": 80}
for _eid, _ziel in PARADE_ZIEL.items():
    ENEMIES[_eid]["parade_ziel"] = _ziel


# ------------------------------------------------------------------ encounters (act 1 - events start them in stage 4c)
def OUT(text, *folgen):
    return {"text": text, "folgen": list(folgen)}


ENCOUNTERS = {
    "hafen_dieb_test": {
        "test": True, "title": "The Pickpocket at the Harbour", "goal": "Get your bag back",
        "image": "corsican_village_harbour.png", "enemy": "taschendieb", "level": 1, "flee_allowed": True,
        "outcomes": {
            "ko": OUT("The thief lies on the cobbles. You have your bag back.", {"flag": "kampftest_tasche_zurueck"}),
            "aufgabe": OUT("He tosses you the bag and raises his hands. “All right, all right.”",
                           {"flag": "kampftest_tasche_zurueck"}, {"flag": "kampftest_ohne_gewalt"}),
            "entkommen": OUT("He ducks between the nets. The bag is gone.", {"flag": "kampftest_tasche_weg"}),
            "flucht": OUT("You let him run. The bag is gone.", {"flag": "kampftest_tasche_weg"}),
            "niederlage": OUT("Everything goes black. When you come round, he's gone, and so is the bag.",
                              {"flag": "kampftest_tasche_weg"}, {"flag": "kampftest_niederlage"})}},
    # Pruefstand (Duc 29.10.2026): die akt1_*-Kaempfe startet kein Event mehr - sie bleiben als feste Testkaempfe fuer
    # test_kampf, test_charms, test_kampf_gegenstaende und die Vorschau (tests\vorschau_server.py --kampf akt1_...).
    "akt1_taschendieb": {
        "title": "Pickpocket in the Harbour Quarter", "goal": "Get your wallet back",
        "image": "corsican_village_harbour.png", "enemy": "taschendieb", "level": 1, "flee_allowed": True,
        "outcomes": {
            "ko": OUT("He slumps against a crate of nets. Your wallet lies in the dust.", {"flag": "akt1_dieb_besiegt"}),
            "aufgabe": OUT("“Okay, okay. Tourists aren't usually this stubborn.” He gives it back, along with a tip about "
                           "where you'd better not walk at night in the harbour.", {"flag": "akt1_dieb_ueberredet"}),
            "entkommen": OUT("He vanishes between the boats. You're twenty euros lighter.", {"geld": -20}),
            "flucht": OUT("You let him go. You're twenty euros lighter.", {"geld": -20}),
            "niederlage": OUT("You end up on the cobbles. When you get up, he's gone, and so are twenty euros.",
                              {"geld": -20})}},
    "akt1_moewe": {
        "title": "The Seagull on the Aft Deck", "goal": "Defend your breakfast",
        "image": "yacht_aft_deck_dining.png", "enemy": "moewe", "level": 1, "flee_allowed": True,
        "outcomes": {
            "ko": OUT("The seagull wobbles off over the railing, deeply offended. The croissant is yours.",
                      {"flag": "akt1_moewe_besiegt"}),
            "aufgabe": OUT("The seagull gives up and screams at you from the mast.", {"flag": "akt1_moewe_besiegt"}),
            "entkommen": OUT("It flies off with your croissant.", {}),
            "flucht": OUT("You leave it the croissant. Dignity intact? Not really.", {}),
            "niederlage": OUT("You lost to a seagull. Lola saw the whole thing.", {"flag": "akt1_moewe_peinlich"})}},
    # Moewe beim Angeln (Duc 29.10.2026, kern/angeln.py): sie schnappt den Fang, gewinnen holt ihn zurueck. Das Bild setzt
    # eden.py auf den Hintergrund des Angelgangs. Die Folgen fuer den Fisch rechnet angeln.moewe_nach_kampf ab.
    "angel_moewe": {
        "title": "A Gull Steals Your Catch", "goal": "Get your fish back",
        "image": "yacht_aft_deck_dining.png", "enemy": "moewe", "level": "duc", "level_plus": -1, "flee_allowed": True,
        "outcomes": {
            "ko": OUT("The gull lets go with a furious scream. Your fish slaps down at your feet, a little pecked.", {}),
            "aufgabe": OUT("The gull drops the fish and sulks on a post, pretending it never wanted it.", {}),
            "entkommen": OUT("A white dot over the water, and your fish goes with it.", {}),
            "flucht": OUT("You let the gull have it. It doesn't say thank you.", {}),
            "niederlage": OUT("Beaten by a seagull. It eats your fish right in front of you, slowly.", {})}},
    "akt1_ratte": {
        "title": "A Rat in the Workshop", "goal": "Get the rat out of the nets",
        "image": "corsican_fisherman_workshop.png", "enemy": "ratte", "level": 1, "flee_allowed": True,
        "outcomes": {
            "ko": OUT("The rat shoots out through a gap in the wall and doesn't come back.", {"flag": "akt1_ratte_weg"}),
            "aufgabe": OUT("The rat gives up and slinks off.", {"flag": "akt1_ratte_weg"}),
            "entkommen": OUT("It's gone, somewhere in the nets.", {}),
            "flucht": OUT("You leave the workshop to the rat.", {}),
            "niederlage": OUT("Bitten. That will sting for a while.", {})}},
    "akt1_pirat": {
        "title": "Pirate at the Swim Platform", "goal": "Keep him off the boat",
        "image": "yacht_swim_platform.png", "enemy": "pirat", "level": 2, "flee_allowed": False,
        "flee_reason": "There's nothing behind you but the yacht.",
        "outcomes": {
            "ko": OUT("The pirate topples backwards into the water and swims for his dinghy.", {"flag": "akt1_pirat_besiegt"}),
            "aufgabe": OUT("He holds his cutlass over his head and jumps back into his boat.", {"flag": "akt1_pirat_besiegt"}),
            "entkommen": OUT("He's gone before you can follow.", {}),
            "flucht": OUT("You fall back.", {}),
            "niederlage": OUT("You go down. When you come round, a can of diesel is missing.", {"flag": "akt1_pirat_diesel"})}},
    "akt1_fackelpirat": {
        "title": "The Pirate with the Torch", "goal": "Stop him before the yacht catches fire",
        "image": "yacht_swim_platform_night.png", "enemy": "fackelpirat", "level": 4, "flee_allowed": True,
        "outcomes": {
            "ko": OUT("The torch hisses in the sea. The pirate paddles off, swearing.", {"flag": "akt1_fackelpirat_besiegt"}),
            "aufgabe": OUT("He throws the torch at your feet and disappears into the night.",
                           {"flag": "akt1_fackelpirat_besiegt"}),
            "entkommen": OUT("He's gone. A black scorch mark is left on the teak deck.", {}),
            "flucht": OUT("You run for help. By the time you're back, he's gone.", {}),
            "niederlage": OUT("You go down. Rosi puts the fire out and tells you off for half an hour.", {})}},
    # Erste Lektion (Tag 2, Duc 24.10.2026): Maxwell erklaert im Kampf die Mechanik (kern/tutorial.py)
    "maxwell_tutorial": {
        "title": "Maxwell's First Lesson", "goal": "Learn to fight from Mr. Maximum",
        "image": "yacht_sun_deck.png", "enemy": "maxwell", "level": "duc", "training": True, "xp_factor": 0.25,
        "flee_allowed": True, "weapon": "mop",
        "outcomes": {
            "ko": OUT("Maxwell lies on the teak, laughing. “Mr. Maximum has a student! Same time tomorrow, Number One!”", {}),
            "aufgabe": OUT("Maxwell taps out and gives you a very sweaty hug. “Lesson one: passed! Eish, brother, that was lekker.”", {}),
            "entkommen": OUT("Maxwell drops for twenty push-ups. “Lesson one is over. You'll be back, Mr. Maximum knows it.”", {}),
            "flucht": OUT("“Running away is also a technique, brother!” Maxwell throws you a towel.", {}),
            "niederlage": OUT("“You learn the most on the floor, brother.” Maxwell pulls you back up.", {})}},
    "maxwell_training": {
        "title": "Training with Maxwell", "goal": "Show Mr. Maximum what you've got",
        "image": "yacht_sun_deck.png", "enemy": "maxwell", "level": "duc", "training": True, "xp_factor": 0.25,
        "flee_allowed": True, "weapon": "mop",
        "outcomes": {
            "ko": OUT("Maxwell lies on his back and laughs. “MAXIMUM! You've got it, brother!”", {}),
            "aufgabe": OUT("Maxwell taps out. “Enough! Mr. Maximum is proud of you, Number One!”", {}),
            "entkommen": OUT("Maxwell starts on his push-ups. Training is over.", {}),
            "flucht": OUT("“A break is training too, brother!” Maxwell hands you a towel.", {}),
            "niederlage": OUT("“Again, brother! Mr. Maximum believes in you!” He pulls you back up.", {})}},
    # Kloster San Martinu (Akt 2, 26.10.2026): Level flach 1-3 (Balancing, kampf_sim_kette.py: Level-2-Duc schafft die
    # Kette mit mittlerer Parade in ~80 %, der Loewe ist die Huerde). Expedition (kern/expedition.py) - eine Niederlage endet mit Schwarzblende auf
    # dem Schiff, eine Phase ist weg, Duc behaelt EIN Stueck Beute. Nur mit Terremoto. Frame-Kette baut Story.
    "kloster_1_ratte": {
        "title": 'Rats on the Path', "goal": 'Get past the rats',
        "image": "eden_rise_macchia_path.png", "enemy": "ratte", "level": 1, "flee_allowed": True, "weapon": "bat", "expedition_niederlage": True,
        "outcomes": {
            "ko": OUT('The rat squeaks and vanishes into the cistus.', {"flag": "kloster_1_ratte_weg"}),
            "aufgabe": OUT('The rat backs off and disappears under a rock.', {"flag": "kloster_1_ratte_weg"}),
            "entkommen": OUT('The rat is gone before you can blink.', {"flag": "kloster_1_ratte_weg"}),
            "flucht": OUT('You step back down the path.', {}),
            "niederlage": OUT('Something bites, the path tilts, and everything goes black.', {})}},
    "kloster_1_schlange": {
        "title": 'A Snake in the Cistus', "goal": "Don't get bitten",
        "image": "eden_rise_macchia_path.png", "enemy": "schlange", "level": 1, "flee_allowed": True, "weapon": "bat", "expedition_niederlage": True,
        "outcomes": {
            "ko": OUT('The snake slides off into the bushes. It has had enough of you.', {"flag": "kloster_1_schlange_weg"}),
            "aufgabe": OUT('The snake coils up, thinks it over, and slides away.', {"flag": "kloster_1_schlange_weg"}),
            "entkommen": OUT('The snake is gone, just a rustle in the dry grass.', {"flag": "kloster_1_schlange_weg"}),
            "flucht": OUT('You take the long way round.', {}),
            "niederlage": OUT('The bite burns up your arm. Your knees give, and everything goes black.', {})}},
    "kloster_2_keiler": {
        "title": 'The Alpha Boar at the Bridge', "goal": 'Get across the bridge',
        "image": "eden_rise_macchia_creek_bridge.png", "enemy": "keiler_kloster", "level": 2, "flee_allowed": False, "flee_reason": 'The bridge is the only way across.', "weapon": "bat", "expedition_niederlage": True,
        "outcomes": {
            "ko": OUT('The collar cracks and falls into the creek. The boar shakes its head, snorts once, and trots off into the macchia.', {"flag": "kloster_2_keiler_weg"}),
            "aufgabe": OUT('The boar stops, its sides heaving. The collar slips off. It turns and leaves.', {"flag": "kloster_2_keiler_weg"}),
            "entkommen": OUT('The boar crashes back into the undergrowth. The collar lies in the dust.', {"flag": "kloster_2_keiler_weg"}),
            "flucht": OUT('You back away.', {}),
            "niederlage": OUT('The boar hits you like a car. You fly, the stones come up, and everything goes black.', {})}},
    "kloster_3_hund": {
        "title": 'A Feral Dog at the Hut', "goal": 'Make the dog back off',
        "image": "eden_rise_shepherd_hut_ruin.png", "enemy": "hund_wild", "level": 2, "flee_allowed": True, "weapon": "bat", "expedition_niederlage": True,
        "outcomes": {
            "ko": OUT('The dog yelps and runs off between the ruins.', {"flag": "kloster_3_hund_weg"}),
            "aufgabe": OUT('The dog drops its head, tail low, and slinks away.', {"flag": "kloster_3_hund_weg"}),
            "entkommen": OUT('The dog bolts up the slope.', {"flag": "kloster_3_hund_weg"}),
            "flucht": OUT('You give the hut a wide berth.', {}),
            "niederlage": OUT('Teeth, dust, the sky spinning. Everything goes black.', {})}},
    "kloster_5_affe": {
        "title": 'An Ape at the Forest Edge', "goal": 'Get past the ape',
        "image": "eden_rise_forest_edge_cliffs.png", "enemy": "affe", "level": 2, "flee_allowed": True, "weapon": "bat", "expedition_niederlage": True,
        "outcomes": {
            "ko": OUT('The collar snaps off with a crack. The ape stares at it, then at you, and swings away into the trees.', {"flag": "kloster_5_affe_weg"}),
            "aufgabe": OUT('The ape screeches, tears at its collar until it breaks, and flees.', {"flag": "kloster_5_affe_weg"}),
            "entkommen": OUT('The ape is gone, up the cliff faster than you could climb it.', {"flag": "kloster_5_affe_weg"}),
            "flucht": OUT('You leave the ape its rock.', {}),
            "niederlage": OUT('A rock hits your temple. The trees lean over you, and everything goes black.', {})}},
    "kloster_6_hunde": {
        "title": 'Two Dogs at the Fork', "goal": 'Hold the fork in the ravine',
        "image": "eden_rise_ravine_fork.png", "enemy": "hund_wild", "level": 2, "flee_allowed": True, "weapon": "bat", "expedition_niederlage": True,
        "outcomes": {
            "ko": OUT('The first dog yelps and runs. The second one follows it down the ravine.', {"flag": "kloster_6_hunde_weg"}),
            "aufgabe": OUT('The two dogs back off together and disappear between the rocks.', {"flag": "kloster_6_hunde_weg"}),
            "entkommen": OUT('Both dogs bolt down the ravine.', {"flag": "kloster_6_hunde_weg"}),
            "flucht": OUT('You back away from the fork.', {}),
            "niederlage": OUT('They come from both sides at once. You go down, and everything goes black.', {})}},
    "kloster_6b_wildschwein_affe": {
        "title": 'Boar and Ape at the Niche', "goal": 'Reach the rock niche',
        "image": "eden_rise_hidden_rock_niche.png", "enemy": "bache", "level": 3, "flee_allowed": True, "weapon": "bat", "expedition_niederlage": True,
        "outcomes": {
            "ko": OUT("The boar crashes off into the bushes. The ape's collar breaks and it flees after it.", {"flag": "kloster_6b_wildschwein_affe_weg"}),
            "aufgabe": OUT('The two of them give up and scatter into the macchia.', {"flag": "kloster_6b_wildschwein_affe_weg"}),
            "entkommen": OUT('Boar one way, ape the other. The niche is free.', {"flag": "kloster_6b_wildschwein_affe_weg"}),
            "flucht": OUT('You leave the niche for later.', {}),
            "niederlage": OUT('The boar knocks your legs out, the ape lands on your back, and everything goes black.', {})}},
    "kloster_7_affe": {
        "title": 'Ambush in the Camp', "goal": 'Survive the ambush',
        "image": "eden_rise_monks_camp_abandoned.png", "enemy": "affe", "level": 3, "flee_allowed": False, "flee_reason": "It came from above. There's nowhere to run.", "weapon": "bat", "expedition_niederlage": True,
        "outcomes": {
            "ko": OUT('The collar snaps. The ape drops from the kettle, shakes itself, and runs into the woods.', {"flag": "kloster_7_affe_weg"}),
            "aufgabe": OUT('The ape screeches, rips the collar off, and flees.', {"flag": "kloster_7_affe_weg"}),
            "entkommen": OUT('The ape is gone, back up into the trees.', {"flag": "kloster_7_affe_weg"}),
            "flucht": OUT('You back away.', {}),
            "niederlage": OUT('It drops on you from the branches. Your head hits the kettle, and everything goes black.', {})}},
    "kloster_8_loewe": {
        "title": 'The Black Lion', "goal": 'Face the lion',
        "image": "eden_rise_lion_den_cave.png", "enemy": "loewe_schwarz", "level": 3, "flee_allowed": False, "flee_reason": 'The lion is between you and the way out.', "weapon": "bat", "expedition_niederlage": True,
        "outcomes": {
            "ko": OUT('The lion goes down and stays down, breathing hard. The red light at the back of its neck keeps blinking.', {"flag": "kloster_8_loewe_weg"}),
            "aufgabe": OUT("The lion sinks to the ground. It doesn't get up again. The red light keeps blinking.", {"flag": "kloster_8_loewe_weg"}),
            "entkommen": OUT('The lion drags itself into the dark of the cave.', {"flag": "kloster_8_loewe_weg"}),
            "flucht": OUT('You back out of the cave.', {}),
            "niederlage": OUT('The lion is on you before you can lift the bat. Weight, heat, breath, and everything goes black.', {})}},
    # Hafenkampf Tag 2 (E-044): Flucht gesperrt, Niederlage startet die Welle neu (E-041, eden.py), die Tiere fliehen.
    "hafen_ratten": {
        "title": "Wave 1 · Rats on the Quay", "goal": "Drive the pack out of the harbour",
        "image": "corsican_village_harbour.png", "enemy": "ratte_alpha", "level": 1, "flee_allowed": False,
        "flee_reason": "The village is behind you.", "neustart_bei_niederlage": True,
        "hilfe_event": "hk_tipp_ratten", "hilfe_flag": "hafen_hilfe_bekommen",
        "outcomes": {
            "ko": OUT("The alpha rat squeals and darts into the alleys. The pack follows.", {"flag": "hafen_ratten_weg"}),
            "aufgabe": OUT("The pack turns and vanishes under the nets.", {"flag": "hafen_ratten_weg"}),
            "entkommen": OUT("The alpha rat gives up and runs. The pack follows it into the alleys.",
                             {"flag": "hafen_ratten_weg"}),
            "flucht": OUT("You back away.", {}),
            "niederlage": OUT("You go down between the fish crates. A boat hook hooks your collar and hauls you up. "
                              "Petru: “Hm. Again.”", {})}},
    "hafen_hunde": {
        "title": "Wave 2 · The Dogs", "goal": "Keep the pack away from the village",
        "image": "eden_rise_hafen_bar_tuer.png", "enemy": "hund_alpha", "level": 2, "flee_allowed": False,
        "flee_reason": "The village is behind you.", "neustart_bei_niederlage": True,
        "hilfe_event": "hk_tipp_hunde", "hilfe_flag": "hafen_hilfe_bekommen",
        "outcomes": {
            "ko": OUT("The alpha dog yelps and slinks off. The pack follows it up the hillside.", {"flag": "hafen_hunde_weg"}),
            "aufgabe": OUT("The pack backs off and trots away into the macchia.", {"flag": "hafen_hunde_weg"}),
            "entkommen": OUT("The alpha dog turns tail. The pack disappears into the macchia.",
                             {"flag": "hafen_hunde_weg"}),
            "flucht": OUT("You back away.", {}),
            "niederlage": OUT("The pack knocks you flat against the shutters. The bar door opens a crack and Alva drags you "
                              "in by the sleeve. “Again, o figliolu. Properly this time.”", {})}},
    "hafen_keiler": {
        "title": "Wave 3 · The Boar", "goal": "Stand up to the boar",
        "image": "eden_rise_piazza_treppe.png", "enemy": "keiler", "level": 3, "flee_allowed": False,
        "flee_reason": "The mayor is on the stairs behind you.", "neustart_bei_niederlage": True,
        "hilfe_event": "hk_tipp_keiler", "hilfe_flag": "hafen_hilfe_bekommen",
        "outcomes": {
            "ko": OUT("The boar snorts, turns and trots back into the macchia as if it had an appointment.",
                      {"flag": "hafen_keiler_weg"}),
            "aufgabe": OUT("The boar stops, looks you over, and leaves.", {"flag": "hafen_keiler_weg"}),
            "entkommen": OUT("The boar has had enough. It trots up the alley and is gone.", {"flag": "hafen_keiler_weg"}),
            "flucht": OUT("You back away.", {}),
            "niederlage": OUT("The boar throws you against the fountain. From the top of the stairs: "
                              "“Up, Monsieur! The audience is waiting!”", {})}},
}


# ------------------------------------------------------------------ validation
def check():
    err = []
    for sid, s in BASIC.items():
        for k in ("label", "attr", "cost", "probe", "text", "effect"):
            if k not in s:
                err.append("basic %s: %s missing" % (sid, k))
        if s.get("attr") not in ATTRS:
            err.append("basic %s: unknown attr %s" % (sid, s.get("attr")))
        for k in ("advantage_with", "free_with"):
            if s.get(k) and s[k] not in STRENGTHS:
                err.append("basic %s: %s %s is no strength" % (sid, k, s[k]))
        if s.get("probe"):
            for e in ("erfolg", "kritisch", "fehlschlag", "patzer"):
                if e not in s["effect"]:
                    err.append("basic %s: result %s missing" % (sid, e))
    seen = set()
    for sid, s in SPECIALS.items():
        if s["path"] not in PATHS or s["tier"] not in (3, 5, 7, 9):
            err.append("special %s: bad code %s" % (sid, s["code"]))
        if s["code"] in seen:
            err.append("special %s: duplicate code %s" % (sid, s["code"]))
        seen.add(s["code"])
        if sid in BASIC:
            err.append("special %s: id also used by a basic skill" % sid)
    if len(seen) != 4 * len(PATHS):                    # four tiers per path (5 paths since the Healer, 26.10.2026)
        err.append("expected %d specials, got %d" % (4 * len(PATHS), len(seen)))
    for wid, w in WEAPONS.items():
        if w["element"] not in ELEMENTS or w["kind"] not in KINDS or w["rarity"] not in RARITIES:
            err.append("weapon %s: bad element/kind/rarity" % wid)
        if w["sig"] not in SIGNATURES or w["slots"] not in (1, 2):
            err.append("weapon %s: bad sig/slots" % wid)
    for gid in [w for w in WEAPONS if not WEAPONS[w].get("training_only")] + list(ARMORS):   # Rosi never upgrades the mop
        if len(WERKSTATT["texte"].get(gid, [])) != len(WERKSTATT["stufen"]):
            err.append("workshop: %s needs %d texts" % (gid, len(WERKSTATT["stufen"])))
    for aid, a in ARMORS.items():
        if a["resist"] not in ELEMENTS or a["rarity"] not in RARITIES or a["sig"] not in ARMOR_SIGS:
            err.append("armor %s: bad resist/rarity/sig" % aid)
        for k in a["bonus"]:
            if k not in ATTRS:
                err.append("armor %s: bonus on unknown attr %s" % (aid, k))
    for eid, e in ENEMIES.items():
        for k in ("name", "sprite", "cls", "tier", "attack", "specials"):
            if k not in e:
                err.append("enemy %s: %s missing" % (eid, k))
        if e.get("cls") not in CLASSES or e.get("tier") not in TIERS or e.get("element") not in ELEMENTS:
            err.append("enemy %s: bad cls/tier/element" % eid)
        for key, sp in e.get("specials", {}).items():
            if key not in ("w1", "w2", "s1", "s2"):
                err.append("enemy %s: unknown special slot %s" % (eid, key))
            if sp.get("effect") not in EFFECTS:
                err.append("enemy %s: unknown effect %s" % (eid, sp.get("effect")))
        if e.get("weakness") and e["weakness"] not in ATTRS:
            err.append("enemy %s: unknown weakness %s" % (eid, e["weakness"]))
        for a in e.get("immune", {}):
            if a not in ATTRS:
                err.append("enemy %s: immune to unknown attr %s" % (eid, a))
        if e.get("parade", "sprite") not in ("sprite", "skala", "ring"):
            err.append("enemy %s: unknown parade %s" % (eid, e.get("parade")))
        for key, it in [("n", e["attack"])] + list((e.get("specials") or {}).items()):     # Finten (03.11.2026)
            f = it.get("finte")
            if not f:
                continue
            if f.get("art") not in FINTE_ARTEN:
                err.append("enemy %s/%s: unknown finte %s" % (eid, key, f.get("art")))
                continue
            if it.get("dodge_only") or e.get("parade") == "ring":
                err.append("enemy %s/%s: no finte on dodge-only blows or ring enemies" % (eid, key))
            for feld, (lo, hi) in FINTE_ARTEN[f["art"]].items():
                if not lo <= f.get(feld, -1) <= hi:
                    err.append("enemy %s/%s: finte %s must be %s-%s" % (eid, key, feld, lo, hi))
            if f["art"] == "kette" and not (1 <= len(f.get("abstaende") or []) <= 3
                                             and all(250 <= a <= 800 for a in f["abstaende"])):
                err.append("enemy %s/%s: kette needs 1-3 gaps of 250-800 ms (2-4 blows)" % (eid, key))
        t = e.get("taunt") or {}
        if t and not (t.get("sfx") or t.get("zeilen")):
            err.append("enemy %s: taunt needs a sound or lines" % eid)
        if t.get("zeilen") and not TAUNTS[t["gruppe"]].get("stimme"):
            err.append("enemy %s: taunt group %s has lines but no voice" % (eid, t["gruppe"]))
        if t.get("sfx") and not any(f.startswith(t["sfx"] + "_") for f in os.listdir(os.path.join(os.path.dirname(TARGET), "sfx"))):
            err.append("enemy %s: taunt sound %s not in sfx/" % (eid, t["sfx"]))
        if not PARADE_ZIEL_MIN <= e.get("parade_ziel", PARADE_ZIEL_STD) <= PARADE_ZIEL_MAX:
            err.append("enemy %s: parade_ziel must be %d-%d %%" % (eid, PARADE_ZIEL_MIN, PARADE_ZIEL_MAX))
    for bid, b in ENCOUNTERS.items():
        if b.get("enemy") not in ENEMIES:
            err.append("encounter %s: unknown enemy %s" % (bid, b.get("enemy")))
        if b.get("enemies"):                                      # Mehrgegner-Kampf (29.10.2026): max. 3, alle bekannt
            if len(b["enemies"]) > 3 or any(e not in ENEMIES for e in b["enemies"]):
                err.append("encounter %s: enemies must be 1-3 known enemies" % bid)
            if b.get("lp_faktoren") and len(b["lp_faktoren"]) != len(b["enemies"]):
                err.append("encounter %s: one lp_faktor per enemy" % bid)
        lv = b.get("level")
        if not (lv == "duc" or (isinstance(lv, int) and 1 <= lv <= 12)):
            err.append("encounter %s: level must be 1-12 or 'duc'" % bid)
        for e in ENDS:
            if e not in b.get("outcomes", {}):
                err.append("encounter %s: outcome %s missing" % (bid, e))
        for e, o in b.get("outcomes", {}).items():
            if e not in ENDS:
                err.append("encounter %s: unknown outcome %s" % (bid, e))
            for f in o.get("folgen", []):
                bad = set(f) - FOLGEN_KEYS
                if bad:
                    err.append("encounter %s/%s: unknown folge %s" % (bid, e, sorted(bad)))
    return err


# ------------------------------------------------------------------ Rudel (Mehrgegner-Kampf, Duc 29.10.2026)
# "Tiere in der Macchia gerne in Rudeln, ausser die Alphas; am Hafen alle in Gruppen." enemies = wer kaempft (max. 3),
# lp_faktoren = Leben je Mitglied (Rudeltiere schwach: ein Schlag, zwei Schlaege - die Alpha bleibt stark).
# Der Alpha-Keiler (kloster_2) und der schwarze Loewe (kloster_8) bleiben allein.
def _rudel(bid, enemies, lp, **texte):
    b = ENCOUNTERS[bid]
    b.update(enemies=enemies, lp_faktoren=lp)
    for ende, text in texte.items():
        b["outcomes"][ende]["text"] = text


_rudel("kloster_1_ratte", ["ratte", "ratte", "ratte"], [0.4, 0.4, 0.4],
       ko="The last rat squeaks, and the whole pack vanishes into the cistus.",
       aufgabe="The rats back off and disappear under the rocks.", entkommen="The rats are gone before you can blink.")
_rudel("kloster_1_schlange", ["schlange", "schlange"], [0.55, 0.55],
       ko="The snakes slide off into the bushes. They've had enough of you.",
       aufgabe="The snakes coil up, think it over, and slide away.",
       entkommen="The snakes are gone, just a rustle in the dry grass.")
_rudel("kloster_3_hund", ["hund_wild", "hund_wild"], [0.6, 0.6],
       ko="The dogs yelp and run off between the ruins.", aufgabe="The dogs drop their heads and slink away.",
       entkommen="The dogs bolt up the slope.")
_rudel("kloster_5_affe", ["affe", "affe"], [0.6, 0.6],
       ko="The collars snap off with a crack. The apes stare at them, then at you, and swing away into the trees.",
       aufgabe="The apes screech, tear at their collars until they break, and flee.",
       entkommen="The apes are gone, up the cliff faster than you could climb it.")
_rudel("kloster_6_hunde", ["hund_wild", "hund_wild", "hund_wild"], [0.5, 0.5, 0.5],
       ko="The last dog yelps, and the pack runs off down the ravine.",
       aufgabe="The pack backs off together and disappears between the rocks.", entkommen="The pack bolts down the ravine.")
_rudel("kloster_6b_wildschwein_affe", ["bache", "affe"], [0.6, 0.6])
_rudel("kloster_7_affe", ["affe", "affe"], [0.6, 0.6],
       ko="The collars snap. The apes drop from the kettle, shake themselves, and run into the woods.",
       aufgabe="The apes screech, rip their collars off, and flee.", entkommen="The apes are gone, back up into the trees.")
_rudel("hafen_ratten", ["ratte_alpha", "ratte", "ratte"], [1.0, 0.4, 0.4])
_rudel("hafen_hunde", ["hund_alpha", "hund_wild"], [1.0, 0.5])
_rudel("hafen_keiler", ["keiler", "bache"], [1.0, 0.45])


# Ortskapitel Berge (Akt 2, 27.10.2026): eigene Datei, damit die Kampf-Sitzung hier ungestoert weiterbauen kann
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kaempfe_berge as _berge  # noqa: E402
ENEMIES.update(_berge.ENEMIES)
ENCOUNTERS.update(_berge.ENCOUNTERS)
CHIPS["drops"].update(_berge.DROPS)
# Akt 2 Woche 2 (27.10.2026): Unit-01, Strand-Grotte, Kevins Daecher
import kaempfe_grotte as _grotte  # noqa: E402
ENEMIES.update(_grotte.ENEMIES)
ENCOUNTERS.update(_grotte.ENCOUNTERS)
CHIPS["drops"].update(_grotte.DROPS)
# Die Brueder Ricci, Taschendiebe am Hafen (29.10.2026, kern/taschendieb.py)
import kaempfe_hafen as _hafen  # noqa: E402
ENEMIES.update(_hafen.ENEMIES)
ENCOUNTERS.update(_hafen.ENCOUNTERS)
# Nebenquest Red Trio (30.10.2026)
import kaempfe_red_trio as _red_trio  # noqa: E402
ENEMIES.update(_red_trio.ENEMIES)
ENCOUNTERS.update(_red_trio.ENCOUNTERS)
# Bibis Tierstation (31.10.2026): Rettungen, Wiki systeme/tierstation.md
import kaempfe_mochis as _mochis  # noqa: E402
ENEMIES.update(_mochis.ENEMIES)
ENCOUNTERS.update(_mochis.ENCOUNTERS)
CHIPS["drops"].update(_red_trio.DROPS)
# Akt 3 (04.11.2026): Scrap Field, Villa-Keller, Endkampf gegen Alon (kaempfe_akt3.py)
import kaempfe_akt3 as _akt3  # noqa: E402
ENEMIES.update(_akt3.ENEMIES)
ENCOUNTERS.update(_akt3.ENCOUNTERS)

# Finten (Duc 03.11.2026, Paket "Lesen statt rechnen", Vorbild Clair Obscur): ein Angriff je Gegnerart hat einen eigenen
# Rhythmus, den man lernt. Immer gleich je Absicht, nie Zufall. Der Client spielt sie (client/plugins/eden-combat/eden-qte.js):
#   zoegern     {bei, halt}       der Marker bleibt kurz vor der Zone stehen, der Schlag kommt halt ms spaeter
#   taeuschung  {bei, zurueck}    der Gegner zuckt, der Marker springt zurueck, dann erst der echte Schlag
#   kette       {abstaende}       2-4 Schlaege hintereinander (gebaut, noch keinem Gegner gegeben: Combos entscheidet Duc)
# Keine Finten fuer die ersten Gegner (Ratte, Moewe, Pirat, Taschendieb, Maxwell) und nicht auf Angriffen, denen man nur
# ausweicht, oder bei Ring-Gegnern. "n" ist der normale Angriff.
ZOEGERN = {"art": "zoegern", "bei": 0.7, "halt": 450}
ZOEGERN_LANG = {"art": "zoegern", "bei": 0.75, "halt": 650}
TAEUSCHUNG = {"art": "taeuschung", "bei": 0.8, "zurueck": 0.55}   # springt weiter vorn an, nie an den Anfang
FINTEN = {
    "dieb_fabbiu": {"w1": TAEUSCHUNG}, "fackelpirat": {"s1": ZOEGERN}, "keiler": {"s1": ZOEGERN},
    "keiler_kloster": {"s1": ZOEGERN}, "bache": {"s1": ZOEGERN}, "hund_wild": {"s1": TAEUSCHUNG},
    "loewe_schwarz": {"s1": TAEUSCHUNG}, "wolf": {"s1": ZOEGERN}, "mo_wolf": {"s1": ZOEGERN},
    "wolf_alpha": {"s1": ZOEGERN_LANG}, "agent": {"w1": ZOEGERN}, "agent_fuehrer": {"w1": ZOEGERN},
    "brute_solo": {"s1": ZOEGERN_LANG}, "wolff": {"n": TAEUSCHUNG, "s1": ZOEGERN}, "wolff_hart": {"n": TAEUSCHUNG, "s1": ZOEGERN_LANG},
    "old_grey": {"s1": ZOEGERN_LANG}, "panther": {"s1": TAEUSCHUNG}, "unit01": {"s1": ZOEGERN},
    "schmuggler": {"s1": TAEUSCHUNG}, "riscossore": {"n": TAEUSCHUNG, "s1": ZOEGERN}, "vampirin": {"s1": ZOEGERN_LANG},
    "matte": {"s1": ZOEGERN}, "rt_charly": {"s1": ZOEGERN}, "rt_danzel": {"s1": TAEUSCHUNG},
    "ark_hyaene": {"s1": TAEUSCHUNG}, "schlange_alpha": {"s1": ZOEGERN},
}
for _eid, _f in FINTEN.items():
    for _key, _finte in _f.items():
        (ENEMIES[_eid]["attack"] if _key == "n" else ENEMIES[_eid]["specials"][_key])["finte"] = dict(_finte)
# Taunt beim Zoegern (Duc 03.11.2026: "Hesitation immer mit Taunt, Tiere knurren einfach"). Gruppen von Duc abgenommen
# (Sitzung taunt-gruppen, Commit 953bcec7): taunt_gruppen.json neben dieser Datei. Menschen sprechen Zeilen ihrer Gruppe
# (Schluessel kampf.taunt.<gruppe>.<n>, vertont mit der Katalogstimme der Gruppe), Tiere und Maschinen nur einen Laut.
_TG = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "taunt_gruppen.json"), encoding="utf-8"))
TAUNTS = {gid: {"stimme": g.get("stimme"), "sfx": g.get("sfx"),
                "zeilen": [{"id": "kampf.taunt.%s.%d" % (gid, i), "text": z["text"]} for i, z in enumerate(g.get("zeilen") or [])]}
          for gid, g in _TG["gruppen"].items()}
for _eid, _gid in _TG["gegner"].items():
    _t = TAUNTS[_gid]
    ENEMIES[_eid]["taunt"] = dict({"gruppe": _gid}, **({"sfx": _t["sfx"]} if _t["sfx"] else {}),
                                  **({"zeilen": _t["zeilen"]} if _t["zeilen"] else {}))
FINTE_ARTEN = {"zoegern": {"bei": (0.5, 0.85), "halt": (300, 800)}, "taeuschung": {"bei": (0.6, 0.85), "zurueck": (0.4, 0.7)},
               "kette": {}}

# Akt 2 in Gruppen (Duc 29.10.2026: "alles, was du vorgeschlagen hast" - Sammel-Gegner wie "Two A.V. Agents" werden echte
# Gruppen, gemischt wo es Sinn macht). Bosse, Rede-Gegner und Alphas am Ende eines Wegs bleiben allein.
_RATTEN = ["ratte_alpha", "ratte", "ratte"], [1.0, 0.4, 0.4]
for _bid in ("gr_1_ratten", "gr_u1_ratten"):
    _rudel(_bid, *_RATTEN)
_rudel("fn_1_ratten", ["ratte_alpha", "ratte", "ratte"], [0.9, 0.3, 0.3])   # Flut-Nacht: vier Kaempfe ohne Rast
_rudel("gr_4_schmuggler", ["schmuggler", "schmuggler"], [0.7, 0.5],
       ko="The smugglers go down among the cards, one after the other.",
       aufgabe="They throw their knives on the crate and raise their hands.", entkommen="They run off into the tunnels.")
_rudel("gr_6_fackel", ["fackelpirat", "pirat"], [0.8, 0.5],
       ko="The torch rolls into a puddle and hisses out. His mate drags him off into the dark.",
       aufgabe="They drop the torch and back away into the dark.", entkommen="They're gone.")
_rudel("gr_u2_pirat", ["pirat", "pirat"], [0.7, 0.7])
_rudel("fn_4_piraten", ["fackelpirat", "pirat", "pirat"], [0.6, 0.35, 0.35],
       ko="The torch goes into the water. The others leave the boat and run.")
_rudel("berge_4_wolf", ["wolf", "wolf"], [0.65, 0.65],
       ko="The collars snap. The wolves stare at them, then lope off along the cliff.",
       aufgabe="The wolves back away, tails low, and slip over the edge onto a lower path.",
       entkommen="The wolves are gone, grey into grey.")
ENCOUNTERS["berge_4_wolf"]["title"] = "Wolves Below the Tower"
ENCOUNTERS["berge_4_wolf"]["goal"] = "Get past the wolves on the ledge"
_rudel("berge_8_agenten", ["agent_fuehrer", "agent"], [0.8, 0.6])
_rudel("berge_u1_hunde", ["hund_wild", "hund_wild"], [0.6, 0.6])
_rudel("berge_u2_hunde", ["hund_alpha", "hund_wild", "hund_wild"], [0.8, 0.4, 0.4])
_rudel("berge_u2_agenten", ["agent_nass", "agent"], [0.8, 0.8])
for _baer in ("", "_baer"):                                  # der Big Man bringt seine Agenten wirklich mit
    _rudel("berge_11_duo" + _baer, ["brute_solo", "agent"], [0.9, 0.5])
    _rudel("berge_11_trio" + _baer, ["brute_solo", "agent", "agent"], [0.8, 0.45, 0.45])


# Geld nur von Menschen (Duc 28.10.2026, beute.md 3c): Spanne je Gefahrenstufe, Tiere/Flieger/Maschinen/Monster nichts
GELD_DROP = {"klassen": ["mensch"], "spanne": {"laestig": [10, 20], "gefaehrlich": [20, 40], "toedlich": [60, 120],
                                                 "albtraum": [60, 120]}}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    err = check()
    if err:
        print("\n".join(err))
        print("%d errors - nothing written." % len(err))
        sys.exit(1)
    data = {"_hinweis": "Gebaut aus werkzeuge\\eden_rise\\kaempfe_eden_rise.py - dort aendern, nicht hier.",
            "version": 3, "basic": BASIC, "specials": SPECIALS, "weapons": WEAPONS, "helden": HELDEN, "muendung": MUENDUNG, "start_weapon": START_WEAPON, "start_armor": START_ARMOR, "start_gear": START_GEAR, "chips": CHIPS, "fallback_weapon": FALLBACK_WEAPON, "werkstatt": WERKSTATT,
            "geld_drop": GELD_DROP,
            "armors": ARMORS,
            "enemies": ENEMIES, "encounters": ENCOUNTERS, "taunts": TAUNTS}
    for eid, e in ENEMIES.items():                    # hint, no error: images come from werkzeuge\kampf_bilder.py
        need = ["idle", "avatar", "windup", "attack", "heavy_windup", "heavy_attack"]
        missing = [p for p in need if not os.path.isfile(os.path.join(IMAGES, e["sprite"], p + ".webp"))]
        if missing:
            print("Hinweis: %s – Bilder fehlen (%s), Kampf_Bilder.bat starten" % (eid, ", ".join(missing)))
    tmp = TARGET + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
    os.replace(tmp, TARGET)
    print("kaempfe.json: %d basic skills, %d specials, %d weapons, %d armors, %d enemies, %d encounters, 0 errors"
          % (len(BASIC), len(SPECIALS), len(WEAPONS), len(ARMORS), len(ENEMIES), len(ENCOUNTERS)))


if __name__ == "__main__":
    main()
