# -*- coding: utf-8 -*-
r"""Katalog der Erweiterungen (25.10.2026, Duc: Anime-Stil, einfache englische Namen, drei Stufen je Familie).

Erweiterungen aendern Kampfwerte von Waffe oder Jacke (Attribute gehoeren den Charms). Plaetze je Stueck: 1 / 2 / 3 mit
Rosis Stufe; der Pool gehoert Duc, Tausch frei in der Kabine, jede Erweiterung gibt es nur einmal. Dieser Katalog ist DATEN:
Die Wirkungen sind noch nicht in der Engine (kern\kampf.py), die Zahlen sind vorlaeufig bis zur Simulation.

  gruppe      waffe | jacke
  kategorie   waffen: wucht, praezision, technik, konter, zustand, element (nur Gemelli, hoechstens eine gleichzeitig)
              jacken: schutz, parade, ausdauer, erholung, auftritt, abwehr, aufklaerung
  stufe       1 gewoehnlich, 2 selten, 3 episch
  wirkung     {"stat": ..., "wert": ..., ["zustand"|"element": ...]} - maschinenlesbar fuer die Engine
  text        englischer Spieltext (fest, wird vorab vertont), kurz, mit etwas Anime-Humor

    python erweiterungen_eden_rise.py   -> module\eden_rise\erweiterungen.json (validiert)
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(os.path.dirname(HERE))
TARGET = os.path.join(EDEN, "module", "eden_rise", "erweiterungen.json")
SELTENHEIT = {1: "gewoehnlich", 2: "selten", 3: "episch"}
ZUSTAENDE = ["brennend", "strom", "blutend", "erschuettert", "nass", "geblendet"]
ELEMENTE = ["feuer", "wasser", "erde", "luft"]
ERWEITERUNGEN = {}


def fam(gruppe, kategorie, familie, namen, wirkungen, texte, **extra):
    """Eine Familie mit drei Stufen anlegen."""
    for k in range(3):
        name = namen[k]
        eid = name.lower().replace("'", "").replace(" ", "_").replace("-", "_")
        e = {"id": eid, "label": name, "gruppe": gruppe, "kategorie": kategorie, "familie": familie, "stufe": k + 1,
             "seltenheit": SELTENHEIT[k + 1], "wirkung": dict(wirkungen[k], **extra), "text": texte[k]}
        ERWEITERUNGEN[eid] = e


# ------------------------------------------------------------------ Waffen
fam("waffe", "wucht", "wucht", ["Hammer Time", "Hammer Down", "Hammerfall"],
    [{"stat": "schaden", "wert": 2}, {"stat": "schaden", "wert": 3}, {"stat": "schaden", "wert": 4}],
    ["A little extra weight behind every swing. +2 damage.", "Now it really lands. +3 damage.",
     "Gravity does the rest. +4 damage."])
fam("waffe", "praezision", "praezision", ["Bullseye", "Dead Center", "Perfect Shot"],
    [{"stat": "krit", "wert": 8}, {"stat": "krit", "wert": 12}, {"stat": "krit", "wert": 16}],
    ["Aim for the middle. Critical chance +8%.", "Right where it hurts. Critical chance +12%.",
     "You never miss. You just pick the moment. Critical chance +16%."])
fam("waffe", "technik", "technik", ["Quick Draw", "Second Wind", "Full Flow"],
    [{"stat": "spezial_kosten", "wert": -1}, {"stat": "ausdauer_bei_treffer", "wert": 1},
     {"stat": "spezial_und_ausdauer", "wert": 1}],
    ["Special attacks cost 1 stamina less.", "Every hit gives you 1 stamina back.",
     "Quick Draw and Second Wind in one. Just keep moving."])
fam("waffe", "konter", "konter", ["Payback", "Backlash", "Reversal"],
    [{"stat": "konter", "wert": 1.2}, {"stat": "konter", "wert": 1.35}, {"stat": "konter", "wert": 1.5}],
    ["Hit me and I hit back. Counters deal x1.2.", "They'll regret that swing. Counters deal x1.35.",
     "Your parry turns the whole fight around. Counters deal x1.5."])
ZUSTAND_FAMILIEN = [
    ("brennend", ["Hot Blade", "Flame Blade", "Inferno Blade"], "set the enemy on fire",
     ["A warm edge.", "It hisses on contact.", "Bring marshmallows."]),
    ("strom", ["Spark Blade", "Shock Blade", "Thunder Blade"], "shock the enemy",
     ["A tingle at the tip.", "Hair stands up. Not just yours.", "Zeus called. He wants his edge back."]),
    ("blutend", ["Sharp Cut", "Deep Cut", "Bloody Edge"], "make the enemy bleed",
     ["Just a scratch. Mostly.", "Not a scratch.", "Dramatic, but effective."]),
    ("erschuettert", ["Rattle", "Quake", "Earthshaker"], "shake the enemy so its armour is gone for 2 rounds",
     ["Teeth rattle.", "The ground disagrees with them.", "Even the floor feels it."]),
    ("nass", ["Splash", "Soak", "Flood"], "soak the enemy, so parrying gets easier",
     ["A bit damp.", "Thoroughly wet.", "Someone should have brought a towel."]),
]
for zustand, namen, was, witz in ZUSTAND_FAMILIEN:
    fam("waffe", "zustand", "zustand_" + zustand, namen,
        [{"stat": "zustand_chance", "wert": w} for w in (20, 30, 40)],
        ["%s Every hit has a %d%% chance to %s." % (witz[k], (20, 30, 40)[k], was) for k in range(3)],
        zustand=zustand)
ELEMENT_FAMILIEN = [
    ("feuer", ["Ember Shell", "Flame Shell", "Inferno Shell"], "fire"),
    ("wasser", ["Rain Shell", "Tide Shell", "Tsunami Shell"], "water"),
    ("erde", ["Stone Shell", "Boulder Shell", "Mountain Shell"], "earth"),
    ("luft", ["Breeze Shell", "Gust Shell", "Storm Shell"], "wind"),
]
for element, namen, en in ELEMENT_FAMILIEN:
    fam("waffe", "element", "element_" + element, namen,
        [{"stat": "element_schaden", "wert": w} for w in (1, 2, 3)],
        ["Loads the barrels with %s. +%d %s damage on every shot. Only one element shell at a time." % (en, w, en)
         for w in (1, 2, 3)], element=element, nur_waffe="gun")

# ------------------------------------------------------------------ Jacken
fam("jacke", "schutz", "schutz", ["Tough Coat", "Iron Coat", "Dragon Coat"],
    [{"stat": "schutz", "wert": 1}, {"stat": "schutz", "wert": 2}, {"stat": "schutz", "wert": 3}],
    ["A thicker lining. Protection +1.", "Heavy, but it holds. Protection +2.", "Scales, apparently. Protection +3."])
fam("jacke", "parade", "parade", ["Steady Hands", "Calm Mind", "Zen Cuffs"],
    [{"stat": "parade_fenster", "wert": 10}, {"stat": "parade_fenster", "wert": 15}, {"stat": "parade_fenster", "wert": 20}],
    ["Calm hands. Parry window +10%.", "Nothing rattles you. Parry window +15%.",
     "Breathe in. Parry. Breathe out. Parry window +20%."])
fam("jacke", "ausdauer", "ausdauer", ["Deep Breath", "Runner's High", "Endless Run"],
    [{"stat": "ausdauer_max", "wert": 1}, {"stat": "ausdauer_max", "wert": 2},
     {"stat": "ausdauer_max_und_verteidigen", "wert": 2}],
    ["One more breath. +1 maximum stamina.", "The legs just keep going. +2 maximum stamina.",
     "+2 maximum stamina, and defending gives 1 stamina extra."])
fam("jacke", "erholung", "erholung", ["Snack Time", "Power Nap", "Phoenix Heart"],
    [{"stat": "snack_heilung", "wert": 2}, {"stat": "heilung_nach_kampf", "wert": 3},
     {"stat": "snack_und_kampf", "wert": 2}],
    ["Snacks heal 2 more. It looks like a biscuit, don't ask.", "You recover 3 HP after every fight. Eyes closed, still alert.",
     "Snack Time and Power Nap in one. Burns bright, comes back."])
fam("jacke", "auftritt", "auftritt", ["Neat Look", "Cool Smile", "Boss Aura"],
    [{"stat": "fassung", "wert": 2}, {"stat": "fassung", "wert": 3}, {"stat": "fassung", "wert": 4}],
    ["Looking sharp helps. Talk and Intimidate take 2 more composure.", "Harmless face, unsettling eyes. 3 more composure.",
     "They fold before you open your mouth. 4 more composure."])
ABWEHR_FAMILIEN = [
    ("brennend", ["Cool Head", "Ice Veins", "Frozen Heart"], "burning"),
    ("nass", ["Dry Cuffs", "Dry Heart", "Desert Soul"], "being soaked"),
    ("strom", ["Rubber Soles", "Static Guard", "Lightning Rod"], "shock"),
    ("blutend", ["Thick Skin", "Steel Skin", "Iron Will"], "bleeding"),
    ("erschuettert", ["Firm Stance", "Iron Stance", "Rock Stance"], "being shaken"),
    ("geblendet", ["Clear Eyes", "Sharp Eyes", "Third Eye"], "being blinded"),
]
for zustand, namen, was in ABWEHR_FAMILIEN:
    fam("jacke", "abwehr", "abwehr_" + zustand, namen,
        [{"stat": "abwehr", "wert": "kuerzer"}, {"stat": "abwehr", "wert": "halb"}, {"stat": "abwehr", "wert": "immun"}],
        ["Effects of %s end 1 round sooner." % was, "Effects of %s are only half as strong." % was,
         "Immune to %s." % was], zustand=zustand)
# Scout (26.10.2026, Duc): Rosi baut einen Halsband-Sender um, der die Signale der anderen Halsbaender auffaengt. Wirkt nur in
# der getragenen Jacke. Anzeige im Expeditions-Bildschirm (Plugin eden-expedition, liest chips_aktiv()["aufklaerung"]).
fam("jacke", "aufklaerung", "scout", ["Radio Ear", "Signal Hunter", "Know Thy Enemy"],
    [{"stat": "aufklaerung", "wert": 1}, {"stat": "aufklaerung", "wert": 2}, {"stat": "aufklaerung", "wert": 3}],
    ["A rebuilt collar that listens in. On an expedition you see who's waiting. Animals without a collar stay just \"animal\".",
     "Clearer signal. You also see their level and how dangerous they are.",
     "You hear them think, almost. You also see their weakness."])


def check():
    err = []
    for eid, e in ERWEITERUNGEN.items():
        if e["gruppe"] not in ("waffe", "jacke") or e["stufe"] not in (1, 2, 3) or not e["text"] or not e["wirkung"].get("stat"):
            err.append("%s: unvollstaendig" % eid)
        if e.get("kategorie") == "zustand" and e["wirkung"].get("zustand") not in ZUSTAENDE:
            err.append("%s: unbekannter Zustand" % eid)
        if e.get("kategorie") == "element" and e["wirkung"].get("element") not in ELEMENTE:
            err.append("%s: unbekanntes Element" % eid)
    waffe = {k for e in ERWEITERUNGEN.values() if e["gruppe"] == "waffe" for k in [e["kategorie"]]}
    jacke = {k for e in ERWEITERUNGEN.values() if e["gruppe"] == "jacke" for k in [e["kategorie"]]}
    if len(waffe) != 6 or len(jacke) != 7:
        err.append("erwartet 6 Waffen- und 7 Jacken-Kategorien, gefunden Waffe %d, Jacke %d" % (len(waffe), len(jacke)))
    return err


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    err = check()
    if err:
        print("\n".join(err))
        sys.exit(1)
    data = {"_hinweis": "Gebaut aus werkzeuge\\eden_rise\\erweiterungen_eden_rise.py - dort aendern, nicht hier. Wirkungen noch nicht in der Engine.",
            "version": 1, "erweiterungen": ERWEITERUNGEN}
    tmp = TARGET + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
    os.replace(tmp, TARGET)
    w = sum(1 for e in ERWEITERUNGEN.values() if e["gruppe"] == "waffe")
    print("erweiterungen.json: %d Waffen, %d Jacken, 0 Fehler" % (w, len(ERWEITERUNGEN) - w))


if __name__ == "__main__":
    main()
