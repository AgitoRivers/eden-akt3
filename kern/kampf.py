# -*- coding: utf-8 -*-
r"""Solo combat, stage 4a (24.10.2026) - Duc against one enemy, turn based, no time pressure in the menus.

Rules from docs\wiki\systeme\kampf.md ("Spezialangriffe, Brennen und Kombos", "Formeln", "Gesamt-Balancing"), numbers checked
against werkzeuge\kampf_balance_v5.py. Data: module\<modul>\kaempfe.json (builder werkzeuge\eden_rise\kaempfe_eden_rise.py).
The code decides, the language model at most narrates. New code is English, UI texts are German; the public functions
keep their German names because eden.py, the client and the tests call them (starten, zug, parade_aufloesen, ...).

Round: Duc picks a command -> the enemy carries out the intent announced BEFORE -> end of round (burn, bleed, timers)
-> new intent. If the enemy attacks, the fight waits in phase "parade" for the client's reaction test.
  angriff      hit, +1 stamina
  faehigkeit   basic skill or learned special (ziel = id)
  verteidigen  hit against Duc halved, +2 stamina, wider parade window, removes one burn stack on Duc
  gegenstand   heal (medkit, snack)
  fliehen      courage test against the enemy tier (fails: the enemy still acts)
  aussetzen    only when Duc has to skip (stunned, after Vulcano)
Hit   = max(1, round((6 + attr + weapon + extra + exhausted - weakened) x type x element x factor) - protection)
        attr = strength; knives max(strength, cunning); Berserker main path max(strength, courage)
Crit  5 % + 3 % per cunning (+5 % knives), x1.5 rounded up. W20 tests: crit range grows by one per 2 cunning.
Progress (z["combat"]): level 1-10, xp, skills (1 point at Lv 3/5/7/9, 2 at Lv 10, a tier needs the tier below in the
same path). Main path = most points (tie M, K, L, W): its attribute grows to min(5, 2 + level // 2).
Equipment (z["equipment"]): weapon + armor ids from kaempfe.json. LP stay between fights (z["lp"]).
Invalid commands change nothing; every valid move raises the revision, a move with an old revision is refused.
Everything is computed on a copy and taken over at the end (no half moves)."""
import copy, json, math, os, random, uuid

from . import charms, kuechen, regeln, wuerfel_anzeige, zustand

# ------------------------------------------------------------------ constants (docs "Formeln" / simulation v5)
LP_BASE, LP_PER_LEVEL, LEVEL_MAX = 46, 5, 10        # 26.10.2026: 36 -> 46 (Kloster-Balancing, kampf_sim_kette.py)
GEGNER_MAX = 3                                       # up to three enemies per fight (Duc 29.10.2026, like Final Fantasy)
FLAECHE = ("mistral", "lame_de_fond")                # specials that hit every enemy (grenades always do)
SCHRECK_ANDERE = 2                                   # Intimidate: the others watch it and lose this much composure
SELBST = ("libeccio", "sotto_voce", "bonaccia", "retour", "elicriso", "ponente", "risveglio", "arcangelo")   # no target
STAMINA_BASE = 6                         # Lv 5: 7, Lv 9: 8
DUC_ARMOR = 2                            # + armor protection
LP_AFTER_DEFEAT = 12
BASE_ATTACK = 8                          # 26.10.2026: 6 -> 8
X_MASCHINE, APPROVES_AUSDAUER = 1.5, 3   # Maxwells Angriffe (Duc 01.11.2026)
SKILL_POINTS = {3: 1, 5: 1, 7: 1, 9: 1, 10: 2}
TIERS = (3, 5, 7, 9)
PATH_ATTR = {"K": "strength", "L": "cunning", "W": "perception", "M": "courage", "H": "empathy"}   # H: 26.10.2026
PATH_NAME = {"K": "Fighter", "L": "Smuggler", "W": "Marksman", "M": "Berserker", "H": "Healer"}
PATH_TIE = "MKLWH"                       # equal points: like the simulation's build_report (Healer last)
# Healer (26.10.2026): Elicriso heals 30 %, Ponente 10 % per round for 3 rounds (+10 % parry window),
# Risveglio heals 80 % (once per fight), Arcangelo: back up at 50 % LP once when Duc falls (once per fight)
H3_HEAL, H5_HEAL, H5_ROUNDS, H5_PARRY, H7_HEAL, H9_LP = 0.30, 0.10, 3, 1.10, 0.80, 0.50
ONCE_PER_FIGHT = ("risveglio", "arcangelo")
XP_PER_LEVEL, XP_NEXT = 20, 60           # win: 20 x enemy level x threat factor; next level: 60 x level
THREAT = {-1: ("laestig", "Nuisance", 0.5), 0: ("gefaehrlich", "Dangerous", 1.0), 1: ("toedlich", "Deadly", 1.5),
          2: ("albtraum", "Nightmare", 2.0)}
ENEMY_LP, ENEMY_GROWTH, ENEMY_ATK, ENEMY_ATK_LV = 40, 1.10, 14.0, 0.6   # 26.10.2026: 55/19 -> 40/14
LEVEL_GAP = 0.15                         # per enemy level above Duc: +15 % LP and damage (26.10.2026: was 25 %)
PARADE_PLUS = 1.1 * 1.2                  # all parry windows +10 % (Duc 26.10.2026), then +20 % for older players (Steam, 29.10.2026)
BOSS_LP, BOSS_BURN = 1.2, 0.75
CRIT_BASE, CRIT_PER_CUNNING, CRIT_KNIFE, CRIT_MULT = 0.05, 0.03, 0.05, 1.5
EXHAUSTED_BONUS, KNIFE_EXHAUSTED_BONUS = 4, 5
WEAK_MALUS, EXPOSED_BONUS, REACH, HEAVY_BONUS = 3, 3, 1, 4
WEAKEN_ATTACKS = 2                       # Intimidate weakens the next two enemy attacks (Duc 29.10.2026, was one)
TYPE_ADV, TYPE_DIS, ELEM_ADV, ELEM_DIS, RESIST = 1.25, 0.8, 1.2, 0.85, 0.7
BEATS = {"wasser": "feuer", "feuer": "erde", "erde": "luft", "luft": "wasser"}
STATE_OF = {"feuer": "brennend", "wasser": "nass", "erde": "erschuettert", "luft": "strom"}
STRONG = {"klinge": {"mensch", "tier"}, "stumpf": {"maschine", "monster"}, "messer": {"mensch", "tier"},
          "stange": {"monster"}, "fern": {"flieger"}}   # flyers belong to Gemelli alone (Duc 30.10.2026)
WEAK = {"klinge": {"maschine", "monster"}, "stumpf": {"flieger"}, "messer": {"monster"}, "stange": {"maschine"},
        "fern": set()}
BURN_PER_STACK, BURN_MAX, BLEED, SHORT_CIRCUIT, BURST = 0.03, 5, 0.05, 0.08, 0.05
UNTERBROCHEN_FASSUNG = 4
STROM_FAIL = 0.25                        # under current: 25 % to lose the turn (Duc and enemy)
L9_STATE_CAP, M7_FACTOR, M9_FACTOR, L3_FACTOR, L7_FACTOR, W9_FACTOR = 4, 1.3, 0.6, 0.7, 0.3, 0.85
W_FULL_FROM, W7_PER_POINT = 4, 0.15
M5_MULT = (1.5, 2.0, 0.5)                # parade made / made against a strong special / missed
HARMLESS = {"heal3", "heal5", "buff4", "buff3x2", "buff4x2", "armor2x2", "armor3x2", "wall", "dodge", "rudel"}
PATTERN = {"laestig": ["n", "n", "w1"], "gefaehrlich": ["n", "w1", "n", "s1"],
           "toedlich": ["n", "w1", "n", "w2", "s1"], "albtraum": ["w1", "n", "s1", "w2", "n", "s2"]}
TEMPO_OF = {"laestig": "leicht", "gefaehrlich": "mittel", "toedlich": "stark", "albtraum": "stark"}
FLEE_DC = {"laestig": 10, "gefaehrlich": 14, "toedlich": 18, "albtraum": None}
SNACK_HEAL, KITCHEN_BONUS = 6, 4
SCHWAECHE_FASSUNG = 4                    # success with the enemy's weakness: Fassung -4 extra, exhausted

BEFEHLE = ("angriff", "faehigkeit", "verteidigen", "gegenstand", "fliehen")
BEFEHL_LABEL = {"angriff": "Attack", "faehigkeit": "Skill", "verteidigen": "Defend",
                "gegenstand": "Item", "fliehen": "Flee", "aussetzen": "Skip"}
ENDEN = ("ko", "aufgabe", "entkommen", "flucht", "niederlage")
LOG_MAX = 30
# Parade (stage 3): the client measures, the server sets the windows (ms) per tempo
PARADE_ARTEN = ("sprite", "skala", "ring")
TEMPO = {"leicht": {"gut": 220, "perf": 90, "dauer": 1150},
         "mittel": {"gut": 160, "perf": 60, "dauer": 1000},
         "stark": {"gut": 110, "perf": 40, "dauer": 850}}
PERF_PLUS = 1.1                          # perfect window +10 % (Duc 03.11.2026, new parry bar)
TEMPO = {t: dict(w, gut=round(w["gut"] * PARADE_PLUS), perf=round(w["perf"] * PARADE_PLUS * PERF_PLUS)) for t, w in TEMPO.items()}
PARADE_ERGEBNISSE = ("perfekt", "gut", "ausweichen", "verfehlt")
# Feints (Duc 03.11.2026, like Clair Obscur): an intent can carry "finte" {"art", ...}; the client plays the rhythm, the
# server only checks the data. Always the same per intent, so the player can learn it.
FINTE_TEXT = {"zoegern": "holds the swing for a beat, then strikes. Wait for it.",
              "kette": "several blows in a row. Parry every one.",
              "taeuschung": "fakes a swing first, then the real one comes. Don't bite."}
ANTWORT = ("parieren", "ausweichen", "keine", "flucht")             # the right answer to an intent (the sign above the enemy)
PARADE_SERIE, SERIE_FASSUNG = 3, 4
STATE_LABEL = {"erschoepft": "exhausted", "erschuettert": "shaken", "nass": "wet", "strom": "charged",
               "blutend": "bleeding", "brennend": "burning", "schlamm": "mud", "geblendet": "blinded",
               "geschwaecht": "weakened", "ungedeckt": "exposed", "betaeubt": "stunned", "silence": "silenced",
               "buff": "empowered", "armor_up": "armoured", "wall": "guarding", "dodge": "dodging",
               "skip": "skips", "aussetzen": "skips", "guard": "guarding"}
ATTR_LABEL = {"strength": "Strength", "charm": "Charisma", "empathy": "Empathy", "perception": "Perception",
              "cunning": "Cunning", "courage": "Courage"}

_CACHE = {}


def daten(moddir):
    pfad = os.path.join(moddir, "kaempfe.json")
    if not os.path.exists(pfad):
        return None
    kat = os.path.join(moddir, "erweiterungen.json")
    st = (os.path.getmtime(pfad), os.path.getmtime(kat) if os.path.exists(kat) else 0)
    if _CACHE.get(pfad, (None,))[0] != st:
        d = json.load(open(pfad, encoding="utf-8"))
        d["erweiterungen"] = json.load(open(kat, encoding="utf-8"))["erweiterungen"] if os.path.exists(kat) else {}
        _CACHE[pfad] = (st, d)
    return _CACHE[pfad][1]


# ------------------------------------------------------------------ progress: level, xp, skills
def progress(z):
    c = z.setdefault("combat", {})
    c.setdefault("level", 1)
    c.setdefault("xp", 0)
    c.setdefault("skills", [])
    c.setdefault("taught", [])        # 26.10.2026: specials a mentor taught (no skill point, see beibringen)
    if "attributpunkte" not in c:     # 26.10.2026: free attribute points; old saves get the old main-path growth back as points
        c["attributpunkte"] = _alter_pfadzuwachs(z, c)
    return c


ATTR_MAX = 5
ATTR_POINTS_PER_LEVEL = 1
ATTR_WIRKUNG = {"strength": "Attack damage", "cunning": "Crit chance +3 % per point (knives: also with Cunning)",
                "perception": "Parry window +3 % per point, Point de Mire",
                "courage": "Intimidate; the Berserker attacks with Courage",
                "charm": "Talk lowers composure (humans)", "empathy": "The Healer path"}


def _alter_pfadzuwachs(z, c):
    """Before 26.10.2026 the main path raised its attribute to min(5, 2 + level // 2) by itself. Old saves get exactly
    that difference as points to spend, so nobody loses anything."""
    if not c.get("skills") or c.get("level", 1) < 2:
        return 0
    return max(0, min(5, 2 + c["level"] // 2) - 2)


def attribut_steigern(z, att):
    """Spend one attribute point (level-up card, Character menu). Max 5."""
    c = progress(z)
    if att not in ATTR_LABEL:
        raise ValueError("Unknown attribute.")
    if c["attributpunkte"] <= 0:
        raise ValueError("No attribute point to spend.")
    a = z.setdefault("persona", {}).setdefault("attribute", {})
    wert = a.get(att, 2)
    if wert >= ATTR_MAX:
        raise ValueError("%s is already at its maximum." % ATTR_LABEL[att])
    a[att] = wert + 1
    c["attributpunkte"] -= 1
    from . import lob                          # Lob der Crew bei Wert 3/4/5 (27.10.2026): nur vormerken, ausgespielt wird spaeter
    lob.vormerken(z, att, wert + 1)


def beibringen(z, sid):
    """A mentor teaches a special (Maxwell: Mistral). Usable in combat, costs no skill point, does not decide the
    main path, counts as the tier below for learning the next one on its path."""
    c = progress(z)
    if sid not in c["taught"] and sid not in c["skills"]:
        c["taught"].append(sid)


def known(z):
    """Learned and taught specials, learned first."""
    c = progress(z)
    return c["skills"] + [s for s in c["taught"] if s not in c["skills"]]


START_WEAPON = "bat"   # 24.10.2026: replaces the old "faust" fallback - Duc always holds a weapon
START_ARMOR = "jacket_earth"   # Duc always wears a jacket (Terra Scura); it can only be swapped, in the cabin
# Duc's fight sprite folder = "Duc" + look of the jacket + suffix of the weapon (module\<m>\kampf\DucErdeBat ...), 25.10.2026
DUC_LOOK = {"jacket_earth": "Erde", "jacket_water": "Wasser", "jacket_fire": "Feuer", "jacket_air": "Luft", "cyber_armor": "Cyber"}
DUC_WAFFE = {"sword": "Sword", "bat": "Bat", "knife": "Knife", "spear": "Spear", "gun": "Gun", "mop": "Mop"}


def duc_sprite_name(armor_id, weapon_id):
    """Duc's fight sprite folder (module\\<m>\\kampf\\Duc<Look><Suffix>) or None for an unknown jacket/weapon."""
    look, suffix = DUC_LOOK.get(armor_id), DUC_WAFFE.get(weapon_id)
    return "Duc%s%s" % (look, suffix) if look and suffix else None


def duc_portrait(z, defs):
    """Duc's current front portrait outside a fight (hearing, storm - 29.10.2026), the same picture as the Character
    menu (module\\<m>\\charakter\\Duc<Look><Klasse>.webp, werkzeuge\\charakter_bild.py): worn jacket + weapon held.
    The scrubber portrait exists for Terra Scura only - like eden-menu.js portraet()."""
    look = DUC_LOOK.get(_armor_id(equipment(z), defs), "Erde")
    klasse = DUC_WAFFE.get(aktive_waffe(z, defs), "Bat")
    if klasse == "Mop" and look != "Erde":
        klasse = "Bat"
    return "Duc%s%s" % (look, klasse)


def equipment(z):
    e = z.setdefault("equipment", {})
    e.setdefault("weapon", START_WEAPON)   # old saves with "faust" or a removed weapon: see _weapon_id
    e.setdefault("armor", START_ARMOR)     # old saves with a removed armor: see _armor_id
    return e


def besitz(z, defs):
    """Owned gear {"weapons": [...], "armors": [...]}: defs["start_gear"] plus everything whose unlock flag
    ("waffe_<id>" / "jacke_<id>") is set (inventory items no longer count - weapons and jackets are fixed, 24.10.2026)."""
    start = defs.get("start_gear") or {}
    out = {"weapons": list(start.get("weapons", [START_WEAPON])), "armors": list(start.get("armors", [START_ARMOR]))}
    for table, pre in (("weapons", "waffe_"), ("armors", "jacke_")):
        for iid in defs[table]:
            if pre + iid in z.get("flags", []) and iid not in out[table]:
                out[table].append(iid)
    return out


def freischalten(z, defs, slot, iid):
    """Give Duc a weapon or jacket (slot "weapon"/"armor") - called by events later."""
    table = {"weapon": "weapons", "armor": "armors"}[slot]
    if iid not in defs[table]:
        raise ValueError("Unknown gear.")
    flag = ("waffe_" if slot == "weapon" else "jacke_") + iid
    if flag not in z.setdefault("flags", []):
        z["flags"].append(flag)


def _sig(armor):
    return (armor or {}).get("sig")


# ------------------------------------------------------------------ discoveries -> codex (25.10.2026, Duc: "Lernen und Erkennen sind der Moment")
# Nothing is announced before a hit; what Duc finds out in a fight is written to the codex the first time it happens.
ELEM_DE = {"feuer": "Fire", "wasser": "Water", "erde": "Earth", "luft": "Air"}                # display names (English)
KIND_DE = {"klinge": "Blades", "stumpf": "Blunt weapons", "messer": "Knives", "stange": "Polearms", "fern": "Firearms"}
CLS_DE = {"mensch": "humans", "tier": "animals", "monster": "monsters", "maschine": "machines", "flieger": "flyers"}


def entdeckung_text(defs, ev):
    """Codex line for one fight event, or None."""
    if ev.get("art") == "treffer":
        out = []
        for t in ev.get("tags") or []:
            kind, _, rest = t.partition(":")
            if kind == "elem":
                a, b = rest.split(">")
                out.append("Combat: %s beats %s." % (ELEM_DE[a], ELEM_DE[b]))
            else:
                w, c = rest.split(":")
                out.append("Combat: %s are %s against %s." % (KIND_DE[w], "strong" if kind == "art+" else "weak", CLS_DE[c]))
        return out
    if ev.get("art") == "jacke":
        for a in defs["armors"].values():
            if a.get("sig") == ev.get("sig") and a.get("eigenschaft"):
                return ["Combat: %s – %s" % (a["label"], a["eigenschaft"])]
    return None


def entdeckungen(z, defs):
    """Codex entries for what just happened in the fight -> list of new lines (also shown as a toast event)."""
    k = z.get("kampf") or {}
    neu = []
    for ev in k.get("events") or []:
        for text in entdeckung_text(defs, ev) or []:
            if text not in z["codex"] and text not in neu:
                neu.append(text)
    z["codex"] += neu
    k["events"] = (k.get("events") or []) + [{"art": "codex", "text": t[len("Combat: "):]} for t in neu]
    return neu


# ------------------------------------------------------------------ Bestiary (Duc 03.11.2026, "read, don't calculate")
# Like Sekiro: you learn an enemy by parrying it. After the first parry of a kind its rhythm goes into the Codex.
# Only the rhythm, never a damage number.
TEMPO_TEXT = {"leicht": "Slow swing. You have time.", "mittel": "Steady swing.", "stark": "Fast swing. Be ready early."}


def rhythmus(edef):
    """Rhythm of an enemy kind in short, simple lines (Codex, Bestiary)."""
    zeilen = [TEMPO_TEXT[TEMPO_OF[edef["tier"]]]]
    for sp in (edef.get("specials") or {}).values():
        if sp.get("finte"):
            zeilen.append("%s: %s" % (sp["label"], FINTE_TEXT[sp["finte"]["art"]]))
    if (edef.get("attack") or {}).get("finte"):
        zeilen.append("%s: %s" % (edef["attack"]["label"], FINTE_TEXT[edef["attack"]["finte"]["art"]]))
    dodge = [sp["label"] for sp in (edef.get("specials") or {}).values() if sp.get("dodge_only")]
    if dodge:
        zeilen.append("Dodge, don't parry: %s." % ", ".join(dodge))
    if edef.get("parade") == "ring":
        zeilen.append("You can dodge every blow.")
    return zeilen


def zeile(defs, zid):
    """Voiced fixed combat line -> (speaker, text) or (None, None). speaker is a person id, or "stimme:<catalog name>" for
    the generic taunt voices. Keys: kampf.taunt.<group>.<n> (taunts, 03.11.2026), kampf.<enemy>.<n> (untouchable hints),
    kampf.<enemy or sprueche_id>.<art>.<n> (lines in combat)."""
    teile = zid.split(".")
    if len(teile) < 3 or teile[0] != "kampf" or not teile[-1].isdigit():
        return None, None
    n = int(teile[-1])
    if teile[1] == "taunt" and len(teile) == 4:
        g = (defs.get("taunts") or {}).get(teile[2]) or {}
        z = (g.get("zeilen") or [])[n:n + 1]
        return ("stimme:" + g["stimme"], z[0]["text"]) if z and g.get("stimme") else (None, None)
    enemies, encounters = defs.get("enemies") or {}, defs.get("encounters") or {}
    if len(teile) == 3:
        liste = (enemies.get(teile[1]) or {}).get("untouchable_hinweise") or []
    else:
        quelle = enemies.get(teile[1]) or next((b for bid, b in encounters.items() if b.get("sprueche_id", bid) == teile[1]
                                                and b.get("sprueche")), {})
        liste = (quelle.get("sprueche") or {}).get(teile[2]) or []
    h = liste[n] if n < len(liste) else None
    return (h.get("wer"), h.get("text")) if h else (None, None)


def bestiarium_merken(z, g):
    """After a parry (perfect or good): the kind goes into the Bestiary. -> True the first time."""
    typ = g.get("typ")
    if not typ:
        return False
    b = z.setdefault("bestiarium", {})
    neu = typ not in b
    b.setdefault(typ, {"paraden": 0})["paraden"] += 1
    return neu


def bestiarium(z, defs):
    """Codex page Bestiary: every kind Duc has parried, with its rhythm. Kinds with the same name and rhythm count once."""
    out = {}
    for typ, info in (z.get("bestiarium") or {}).items():
        edef = (defs or {}).get("enemies", {}).get(typ)
        if not edef:
            continue
        r = rhythmus(edef)
        e = out.setdefault((edef["name"], tuple(r)), {"id": typ, "name": edef["name"], "rhythmus": r, "paraden": 0})
        e["paraden"] += info.get("paraden", 0)
    return sorted(out.values(), key=lambda e: e["name"])


# ------------------------------------------------------------------ Rosi's workshop (25.10.2026)
ELEMENT_DROP = {"erde": "smaragd", "feuer": "rubin", "wasser": "saphir", "luft": "opal", None: "titanium_plate"}   # tödlich/Albtraum
def werkstatt(z):
    """{"stufen": {"weapon:sword": 1, ...}, "auftrag": {"slot", "id", "stufe", "tag"} | None} - lives in the combat progress."""
    w = progress(z).setdefault("werkstatt", {})
    w.setdefault("stufen", {})
    w.setdefault("auftrag", None)
    return w


def stufe_von(z, slot, iid):
    return werkstatt(z)["stufen"].get("%s:%s" % (slot, iid), 0)


def material_fuer(defs, slot, iid, stufe):
    """Material id for the next upgrade (stufe = current level 0/1): jackets plates, weapons the next stone of their element."""
    m = defs["werkstatt"]["material"]
    chain = m["armor"] if slot == "armor" else m["weapon"].get(iid) or m["weapon"]["gun"]
    return chain[stufe]


def werkstatt_offen(z, defs):
    """Open once the repair event set its flag (the preview switch opens it too)."""
    w = defs.get("werkstatt") or {}
    return bool(w) and (w.get("flag") in z.get("flags", []) or bool(progress(z).get("test")))


def _werkstatt_fehlt(z, defs, slot, iid):
    """German reason why this piece cannot go to Rosi now, else None."""
    w = defs["werkstatt"]
    table = {"weapon": "weapons", "armor": "armors"}[slot]
    st = stufe_von(z, slot, iid)
    if not werkstatt_offen(z, defs):
        return w["text_zu"]
    if st >= len(w["stufen"]):
        return "Rosi can't improve this any further."
    if werkstatt(z)["auftrag"]:
        return "Rosi is already working on something. One piece a night."
    e = equipment(z)
    if (e.get("weapon") if slot == "weapon" else e.get("armor")) == iid:
        return "You're wearing it right now. Put something else on first."
    k = w["stufen"][st]
    mat = material_fuer(defs, slot, iid, st)
    if z.get("konto", 0) < k["geld"]:
        return "You're %d € short." % (k["geld"] - z.get("konto", 0))
    if mat not in z.get("inventar", []):
        return "You're missing: %s." % w["materialien"][mat]
    return None


def abgeben(z, defs, slot, iid):
    """Hand a weapon or jacket in for the next upgrade (cabin, no action). Pays money and material, Rosi finishes overnight."""
    table = {"weapon": "weapons", "armor": "armors"}.get(slot)
    if not table or iid not in defs[table]:
        raise ValueError("Unknown gear.")
    if iid not in besitz(z, defs)[table]:
        raise ValueError("You don't own that yet.")
    grund = _werkstatt_fehlt(z, defs, slot, iid)
    if grund:
        raise ValueError(grund)
    st = stufe_von(z, slot, iid)
    k = defs["werkstatt"]["stufen"][st]
    z["konto"] = z.get("konto", 0) - k["geld"]
    z["inventar"].remove(material_fuer(defs, slot, iid, st))                  # the old stone/plate is gone for good
    werkstatt(z)["auftrag"] = {"slot": slot, "id": iid, "stufe": st + 1, "tag": z.get("tag")}


def werkstatt_morgen(z, defs):
    """Called when a new day begins: finishes the order. -> {"id", "slot", "stufe", "text"} for Rosi's text, or None."""
    w = werkstatt(z)
    a = w["auftrag"]
    if not a:
        return None
    w["auftrag"] = None
    w["stufen"]["%s:%s" % (a["slot"], a["id"])] = a["stufe"]
    texte = defs["werkstatt"]["texte"].get(a["id"]) or []
    return {"id": a["id"], "slot": a["slot"], "stufe": a["stufe"], "text": texte[a["stufe"] - 1] if len(texte) >= a["stufe"] else ""}


def max_lp(level):
    return LP_BASE + LP_PER_LEVEL * (level - 1)


def max_stamina(level):
    return STAMINA_BASE + (1 if level >= 5 else 0) + (1 if level >= 9 else 0)


def skill_points(level):
    return sum(n for lv, n in SKILL_POINTS.items() if level >= lv)


def xp_needed(level):
    return XP_NEXT * level


def path_depth(defs, skills):
    depth = {p: 0 for p in PATH_ATTR}
    for sid in skills:
        s = defs["specials"].get(sid)
        if s:
            depth[s["path"]] += 1
    return depth


def main_path(defs, skills):
    depth = path_depth(defs, skills)
    if not any(depth.values()):
        return None
    return max(depth, key=lambda p: (depth[p], -PATH_TIE.index(p)))


def _persona_attrs(z):
    return dict((z.get("persona") or {}).get("attribute") or {})


def attributes(z, defs):
    """Combat attributes: persona values (level-ups give attribute points, 26.10.2026), armor, food and charm bonus."""
    c, a = progress(z), _persona_attrs(z)
    for att in ATTR_LABEL:
        a.setdefault(att, 2)
    arm = defs["armors"].get(_armor_id(equipment(z), defs))
    for att, n in ((arm or {}).get("bonus") or {}).items():
        a[att] = a.get(att, 0) + n
    a["courage"] = a.get("courage", 0) + kuechen.bonus(z, "attribut")        # Tagesbonus aus dem Essen (Akzent Knoblauch, 27.10.2026)
    for att in ATTR_LABEL:                                                 # Jacken-Charm (28.10.2026), darf ueber 5 gehen
        a[att] = a.get(att, 0) + charms.attribut(z, att)
    return a


def lp_max_duc(z):
    """Duc's maximum. After a night with someone during the siege he has a little more for that one day (Duc 02.11.2026, kern/taktik.py)."""
    m = max_lp(progress(z)["level"])
    plus = z.get("lp_plus") or {}
    return int(m * (1 + plus["faktor"])) if plus and plus.get("tag") == z.get("tag") else m


def lp(z):
    """Duc's current LP (stay between fights), never above the level's maximum."""
    m = lp_max_duc(z)
    z["lp"] = min(z.get("lp", m), m)
    return z["lp"]


def lp_auffuellen(z):
    z["lp"] = lp_max_duc(z)


def threat(enemy_level, duc_level):
    return THREAT[max(-1, min(2, enemy_level - duc_level))]


def xp_for(enemy_level, duc_level, factor=1.0):
    return int(round(XP_PER_LEVEL * enemy_level * threat(enemy_level, duc_level)[2] * factor))


# Chase them off (Duc 02.11.2026, Brain Trust "Kampf-Tiefe", like EarthBound): an encounter clearly below Duc can be
# chased off on the expedition map with one click instead of a fight. Small reward, no loot. Never for bosses, rare
# enemies, talking groups, fights that forbid fleeing or fights at Duc's level.
VERJAGEN_ABSTAND = 2
VERJAGEN_XP = 0.5


def verjagbar(z, defs, bid):
    """-> True if Duc may chase encounter bid off without a fight."""
    b = (defs.get("encounters") or {}).get(bid)
    if not b or b.get("level") == "duc" or b.get("training") or not b.get("flee_allowed") or b.get("neustart_bei_niederlage"):
        return False
    if b.get("selten") or b.get("sprueche") or b.get("beistand"):
        return False
    edefs = [(defs.get("enemies") or {}).get(e) or {} for e in (b.get("enemies") or [b.get("enemy")])]
    if any(e.get("boss") or e.get("untouchable") or not e for e in edefs):
        return False
    return int(b["level"]) <= progress(z)["level"] - VERJAGEN_ABSTAND


def verjagen(z, defs, bid):
    """Chase encounter bid off: half the xp of a won fight, no loot, no money. -> lines for the message."""
    b = defs["encounters"][bid]
    lv, duc = int(b["level"]), progress(z)["level"]
    ids = (b.get("enemies") or [b["enemy"]])[:GEGNER_MAX]
    anteile = b.get("lp_faktoren") or []
    xp = sum(xp_for(lv, duc, VERJAGEN_XP * b.get("xp_factor", 1.0) * defs["enemies"][e].get("xp_faktor", 1)
                    * (anteile[i] if i < len(anteile) else 1)) for i, e in enumerate(ids))
    wid = b["weapon"] if b.get("weapon") in defs["weapons"] else aktive_waffe(z, defs)   # the fight's own weapon (Kloster: bat)
    waffe = (defs["weapons"].get(wid) or {}).get("label") or "your weapon"
    lines = ["You step forward with %s. They take one look at you and run." % waffe]
    return lines + award_xp(z, xp)


def award_xp(z, xp):
    """-> list of German lines (xp, level ups). LP grow with the level."""
    c = progress(z)
    lines = []
    if xp <= 0 or c["level"] >= LEVEL_MAX:
        return lines
    xp = int(round(xp * (100 + kuechen.bonus(z, "xp")) / 100.0))               # Tagesbonus aus dem Essen (Akzent Wildkraeuter, 27.10.2026)
    c["xp"] += xp
    lines.append("+%d experience" % xp)
    while c["level"] < LEVEL_MAX and c["xp"] >= xp_needed(c["level"]):
        c["xp"] -= xp_needed(c["level"])
        before = skill_points(c["level"])
        c["level"] += 1
        z["lp"] = z.get("lp", max_lp(c["level"] - 1)) + LP_PER_LEVEL
        c["attributpunkte"] += ATTR_POINTS_PER_LEVEL
        new = skill_points(c["level"]) - before
        lines.append("Level %d! +1 attribute point%s" % (c["level"], " · +%d skill point%s" % (new, "s" if new > 1 else "") if new else ""))
    if c["level"] >= LEVEL_MAX:
        c["xp"] = 0
    return lines


def free_points(z):
    c = progress(z)
    return skill_points(c["level"]) - len(c["skills"])


def learn_reason(z, defs, sid):
    """Why this special cannot be learned now (German) or None."""
    s = defs["specials"].get(sid)
    c = progress(z)
    if not s:
        return "Unknown special attack."
    if sid in known(z):
        return "Already learned."
    if free_points(z) <= 0:
        return "No free skill point."
    if s["tier"] > TIERS[0]:
        below = TIERS[TIERS.index(s["tier"]) - 1]
        if not any(defs["specials"][x]["path"] == s["path"] and defs["specials"][x]["tier"] == below for x in known(z)):
            return "Needs %s%d on the same path first." % (s["path"], below)
    return None


def lernen(z, defs, sid):
    grund = learn_reason(z, defs, sid)
    if grund:
        raise ValueError(grund)
    progress(z)["skills"].append(sid)


def _weapon_id(e, defs):
    """Equipped weapon, or the start weapon if the save still names a weapon that no longer exists (24.10.2026)."""
    return e.get("weapon") if e.get("weapon") in defs["weapons"] else START_WEAPON


def aktive_waffe(z, defs):
    """The weapon Duc really holds: the equipped one if he owns it (or the preview switch is on), else the first owned
    weapon, else the fallback (the deck scrubber) - before Rosi hands him Terremoto in the harbour (25.10.2026)."""
    e = equipment(z)
    own = besitz(z, defs)["weapons"]
    w = _weapon_id(e, defs)
    if w in own or progress(z).get("test"):
        return w
    return own[0] if own else defs.get("fallback_weapon") or w


def _armor_id(e, defs):
    """Worn jacket, or the start jacket if the save still names an armor that no longer exists (24.10.2026)."""
    return e.get("armor") if e.get("armor") in defs["armors"] else defs.get("start_armor", START_ARMOR)


def ausruesten(z, defs, slot, iid, test=False):
    """Swap weapon or jacket (slot "weapon"/"armor"). Both always stay equipped; outside the test switch the new one
    must be owned (besitz)."""
    table = {"weapon": "weapons", "armor": "armors"}.get(slot)
    if not table:
        raise ValueError("Unknown gear slot.")
    if iid is None:
        raise ValueError("Your weapon can only be swapped." if slot == "weapon" else "Your jacket can only be swapped.")
    if iid not in defs[table]:
        raise ValueError("Unknown gear.")
    if not test and not progress(z).get("test") and iid not in besitz(z, defs)[table]:
        raise ValueError("You don't own that yet.")
    a = werkstatt(z)["auftrag"]
    if a and a["slot"] == slot and a["id"] == iid:
        raise ValueError("Rosi has it in the workshop right now.")
    equipment(z)[slot] = iid


def test_setup(z, defs, level=None, skills=None, weapon=None, armor=None):
    """Test switch (only test copies / preview server): set level, skills and equipment directly, LP full."""
    c = progress(z)
    c["test"] = True
    if level is not None:
        c["level"] = max(1, min(LEVEL_MAX, int(level)))
        c["xp"] = 0
    if skills is not None:
        bad = [s for s in skills if s not in defs["specials"]]
        if bad:
            raise ValueError("Unknown special attacks: %s" % ", ".join(bad))
        c["skills"] = list(skills)
    if weapon is not None:
        ausruesten(z, defs, "weapon", weapon, test=True)
    if armor is not None:
        ausruesten(z, defs, "armor", armor or START_ARMOR, test=True)
    lp_auffuellen(z)


SMUGGLER_HINT = "The Smuggler path comes into its own with its finisher, Omertà."


def _gear_view(gid, d, kind, stufe=0):
    if not d:
        return None
    out = {"id": gid, "label": d["label"], "untertitel": d.get("untertitel"), "seltenheit": d.get("rarity")}
    if kind == "weapon":
        out.update(schaden=d["dmg"] + stufe, element=d.get("element"), art=d["kind"], slots=d.get("slots", 1),
                   stein=(d.get("stein") or [None])[min(stufe, len(d.get("stein") or [None]) - 1)],
                   eigenschaft=d.get("eigenschaft"))
    else:
        out.update(schutz=d["prot"] + stufe, widerstand=d.get("resist"), schwer=bool(d.get("heavy")), bonus=d.get("bonus") or {},
                   eigenschaft=d.get("eigenschaft"))
    out["stufe"] = stufe
    return out


def main_path_info(path):
    """Presentation of existing path traits, without changing combat rules."""
    traits = {
        "K": ["Path attribute: Strength."],
        "L": ["Path attribute: Cunning."],
        "W": ["Path attribute: Perception.", "Parry window: path bonus +10 %."],
        "H": ["Path attribute: Empathy.", "Heals, holds on and rises again once."],
        "M": ["Path attribute: Courage.", "Parry window: path modifier −10 %.",
              "+1 stamina whenever an enemy hit damages you.",
              "Your attacks use Courage instead of Strength when it is higher."],
    }
    summary = {"K": "Path attribute: Strength.", "L": "Path attribute: Cunning.", "H": "Path attribute: Empathy.",
               "W": "Parry window: path bonus +10 %.",
               "M": "Parry window −10 %; +1 stamina when a hit damages you."}
    return {"id": path, "name": PATH_NAME.get(path), "summary": summary.get(path, ""),
            "attribute_label": ATTR_LABEL.get(PATH_ATTR.get(path)), "traits": traits.get(path, [])}


def _lern_kopie(z):
    """Copy for the forecast: only what lernen()/attributes() write (combat progress, equipment) is copied deep, the
    rest of the save is shared read-only - a deepcopy of the whole save cost ~3 ms per skill at day 12 (28.10.2026)."""
    k = dict(z)
    k["combat"] = copy.deepcopy(z.get("combat") or {})
    k["equipment"] = dict(z.get("equipment") or {})
    return k


def learning_preview(z, defs, sid):
    """Read-only forecast using the actual learning and attribute functions on copies."""
    before = _lern_kopie(z)
    if learn_reason(before, defs, sid):
        return None
    after = _lern_kopie(before)
    lernen(after, defs, sid)
    old_path = main_path(defs, progress(before)["skills"])
    new_path = main_path(defs, progress(after)["skills"])
    old_attrs, new_attrs = attributes(before, defs), attributes(after, defs)
    depth = path_depth(defs, progress(after)["skills"])
    return {"before": main_path_info(old_path), "after": main_path_info(new_path),
            "changed": old_path != new_path,
            "tie": sum(n == max(depth.values()) for n in depth.values()) > 1,
            "attributes": [{"id": a, "label": ATTR_LABEL[a], "before": old_attrs[a], "after": new_attrs[a]}
                           for a in ATTR_LABEL if old_attrs[a] != new_attrs[a]]}


# ------------------------------------------------------------------ Chips (Erweiterungen, 25.10.2026)
def chip_pool(z):
    """{"pool": {familie: stufe}, "plaetze": {"weapon:bat": [familie, ...]}} in the combat progress."""
    d = progress(z).setdefault("chips", {})
    d.setdefault("pool", {})
    d.setdefault("plaetze", {})
    return d


def _chip(defs, familie, stufe):
    for e in (defs.get("erweiterungen") or {}).values():
        if e["familie"] == familie and e["stufe"] == stufe:
            return e
    return None


def chip_nutzbar(z, defs):
    """Chips work once Rosi's workshop is open (before that they are unidentified)."""
    return werkstatt_offen(z, defs)


def chip_finden(z, defs, familie, stufe):
    """A found schematic: unlocks the family or raises its level (the old level is replaced), worse or equal finds are
    sold. -> {"art": neu|besser|schlechter|gleich, "text": str, "geld": int}"""
    e = _chip(defs, familie, stufe)
    if not e:
        raise ValueError("Unknown module: %s %s" % (familie, stufe))
    cfg, pool = defs["chips"], chip_pool(z)["pool"]
    alt = pool.get(familie)
    if alt is None:
        pool[familie] = stufe
        art, geld = "neu", 0
    elif stufe > alt:
        pool[familie] = stufe
        art, geld = "besser", 0
    else:
        art, geld = ("gleich" if stufe == alt else "schlechter"), cfg["verkauf"] * stufe
        z["konto"] = z.get("konto", 0) + geld
    if not chip_nutzbar(z, defs):
        return {"art": art, "geld": geld, "text": cfg["text"]["unbekannt"] if art in ("neu", "besser") else
                cfg["text"][art].format(name=e["label"], familie=familie, geld=geld)}
    return {"art": art, "geld": geld, "text": cfg["text"][art].format(name=e["label"], familie=familie, geld=geld)}


def chip_plaetze(z, slot, iid):
    """Erweiterungs-Plaetze of a piece: 1 / 2 / 3 with Rosi's level."""
    return 1 + stufe_von(z, slot, iid)


def _chip_gruppe(slot):
    return "waffe" if slot == "weapon" else "jacke"


def chip_einsetzen(z, defs, slot, iid, familie):
    """Put a family on a piece (cabin). Moves it away from another piece: there is only one of each.
    "charm:<id>" hangs a jacket charm instead (kern/charms.py, 28.10.2026) - works before Rosi's workshop, too."""
    if familie.startswith("charm:"):
        if slot != "armor" or iid not in besitz(z, defs)["armors"]:
            raise ValueError("Charms only hang on jackets you own.")
        return charms.einsetzen(z, iid, familie[6:])
    table = {"weapon": "weapons", "armor": "armors"}.get(slot)
    if not table or iid not in defs[table]:
        raise ValueError("Unknown gear.")
    if not chip_nutzbar(z, defs):
        raise ValueError("Rosi has to check the chips first, and her workshop is still closed.")
    pool = chip_pool(z)["pool"]
    if familie not in pool:
        raise ValueError("You don't have that chip.")
    e = _chip(defs, familie, pool[familie])
    if e["gruppe"] != _chip_gruppe(slot):
        raise ValueError("That chip doesn't fit %s." % ("weapons" if slot == "armor" else "jackets"))
    if e.get("wirkung", {}).get("nur_waffe") and e["wirkung"]["nur_waffe"] != iid:
        raise ValueError("This chip only fits Gemelli.")
    if iid not in besitz(z, defs)[table]:
        raise ValueError("You don't own that yet.")
    pl = chip_pool(z)["plaetze"]
    key = "%s:%s" % (slot, iid)
    liste = pl.setdefault(key, [])
    if familie in liste:
        return
    if e["kategorie"] == "element" and any(_chip(defs, f, pool[f])["kategorie"] == "element" for f in liste if f in pool):
        raise ValueError("Only one element chip fits at a time.")
    if len(liste) >= chip_plaetze(z, slot, iid):
        raise ValueError("Every slot is taken.")
    for k2, l2 in pl.items():
        if familie in l2:
            l2.remove(familie)
    liste.append(familie)


def chip_entfernen(z, slot, iid, familie):
    if familie.startswith("charm:"):                                      # jacket charm (28.10.2026)
        return charms.entfernen(z, iid, familie[6:])
    liste = chip_pool(z)["plaetze"].get("%s:%s" % (slot, iid), [])
    if familie not in liste:
        raise ValueError("That chip isn't in there.")
    liste.remove(familie)


def chips_aktiv(z, defs, weapon_id, armor_id):
    """Sum of the effects of the chips on the worn weapon and jacket (empty before Rosi's workshop is open)."""
    agg = {"schaden": 0, "krit": 0, "spezial_kosten": 0, "ausdauer_treffer": 0, "konter": 1.0, "proc": [], "element": None,
           "schutz": 0, "parade": 0, "ausdauer_max": 0, "ausdauer_verteidigen": 0, "snack": 0, "heil_kampf": 0,
           "fassung": 0, "abwehr": {}, "aufklaerung": 0, "spezial_schaden": 0, "parade_serie": 0, "vorteil": []}
    if armor_id == _armor_id(equipment(z), defs):                          # Jacken-Charm (28.10.2026): wirkt ohne Werkstatt
        for st, v in charms.kampfwerte(z).items():
            if st == "vorteil":
                agg["vorteil"] += list(v)
            elif st in agg:
                agg[st] += v
    if not chip_nutzbar(z, defs):
        return agg
    pool, pl = chip_pool(z)["pool"], chip_pool(z)["plaetze"]
    for key in ("weapon:%s" % weapon_id, "armor:%s" % armor_id):
        for familie in pl.get(key, []):
            e = _chip(defs, familie, pool.get(familie, 0))
            if not e:
                continue
            w, st, v = e["wirkung"], e["wirkung"]["stat"], e["wirkung"]["wert"]
            if st == "schaden":
                agg["schaden"] += v
            elif st == "krit":
                agg["krit"] += v
            elif st == "spezial_kosten":
                agg["spezial_kosten"] += -v
            elif st == "ausdauer_bei_treffer":
                agg["ausdauer_treffer"] += v
            elif st == "spezial_und_ausdauer":
                agg["spezial_kosten"] += 1
                agg["ausdauer_treffer"] += v
            elif st == "konter":
                agg["konter"] *= v
            elif st == "zustand_chance":
                agg["proc"].append([w["zustand"], v])
            elif st == "element_schaden":
                agg["element"] = w["element"]
                agg["schaden"] += v
            elif st == "schutz":
                agg["schutz"] += v
            elif st == "parade_fenster":
                agg["parade"] += v
            elif st == "ausdauer_max":
                agg["ausdauer_max"] += v
            elif st == "ausdauer_max_und_verteidigen":
                agg["ausdauer_max"] += v
                agg["ausdauer_verteidigen"] += 1
            elif st == "snack_heilung":
                agg["snack"] += v
            elif st == "heilung_nach_kampf":
                agg["heil_kampf"] += v
            elif st == "snack_und_kampf":
                agg["snack"] += v
                agg["heil_kampf"] += 3
            elif st == "fassung":
                agg["fassung"] += v
            elif st == "abwehr":
                agg["abwehr"][w["zustand"]] = v
            elif st == "aufklaerung":                                      # Scout: 1 enemy, 2 + level/threat, 3 + weakness
                agg["aufklaerung"] = max(agg["aufklaerung"], v)
    return agg


def aufklaerung(z, defs):
    """Scout level of the worn jacket (0 without the chip fitted)."""
    e = equipment(z)
    return chips_aktiv(z, defs, _weapon_id(e, defs), _armor_id(e, defs))["aufklaerung"]


def chip_in_jacke(z, defs, familie):
    """Rosi fits a chip into the worn jacket herself (gift). Silent if every slot is taken: then it waits in the pool."""
    try:
        chip_einsetzen(z, defs, "armor", _armor_id(equipment(z), defs), familie)
        return True
    except ValueError:
        return False


def chip_drop_anwenden(z, defs):
    """After a won fight: the enemy's collar chip (once). Adds the message to the result lines."""
    k = z.get("kampf") or {}
    erg = k.get("ergebnis")
    if not erg or k.get("chip_gedroppt") or erg.get("art") not in ("ko", "aufgabe") or (k.get("def") or {}).get("training"):
        return None
    k["chip_gedroppt"] = True
    drop = ((defs.get("chips") or {}).get("drops") or {}).get(k["gegner"][0]["typ"])
    if not drop:
        return None
    if isinstance(drop, dict):                                             # 28.10.2026: genau eine Belohnung aus mehreren
        r = _beute_eins_aus(z, defs, drop["eins_aus"])
        erg["zeilen"] = list(erg.get("zeilen") or []) + [r["text"]]
        return r
    r = chip_finden(z, defs, drop[0], drop[1])
    erg["zeilen"] = list(erg.get("zeilen") or []) + [r["text"]]
    return r


def _beute_eins_aus(z, defs, liste):
    """Vampirin (Flut-Nacht, Duc 28.10.2026): immer gute Beute, aber nur eine je Kampf - ein Modul, Geld oder ein
    Upgrade-Material. Eintraege: ["chip", [[familie, stufe], ...]] | ["geld", n] | ["material", [id, ...]]."""
    art, wert = random.choice(liste)
    if art == "chip":
        fam, st = random.choice(wert)
        return chip_finden(z, defs, fam, st)
    if art == "geld":
        z["konto"] = z.get("konto", 0) + wert
        return {"art": "geld", "geld": wert, "text": "+%d €" % wert}
    mat = random.choice(wert)
    z.setdefault("inventar", []).append(mat)
    return {"art": "material", "geld": 0, "text": "🎁 %s" % ((defs.get("werkstatt") or {}).get("materialien") or {}).get(mat, mat)}


def chip_ansicht(z, defs):
    """Pool and pieces with their slots for the upgrade window (cabin)."""
    pool, pl = chip_pool(z)["pool"], chip_pool(z)["plaetze"]
    nutzbar = chip_nutzbar(z, defs)
    ort = {f: key for key, liste in pl.items() for f in liste}
    out = []
    for f, st in pool.items():
        e = _chip(defs, f, st)
        out.append({"familie": f, "id": e["id"], "stufe": st, "label": e["label"], "kategorie": e["kategorie"],
                    "gruppe": e["gruppe"], "text": e["text"], "ort": ort.get(f), "bekannt": nutzbar,
                    "nur_waffe": (e.get("wirkung") or {}).get("nur_waffe")})
    out.sort(key=lambda c: (c["gruppe"], c["kategorie"], c["label"]))
    e0, e = equipment(z), None
    stuecke = []
    for slot, table in (("weapon", "weapons"), ("armor", "armors")):
        for iid in besitz(z, defs)[table]:
            d = defs[table][iid]
            st = stufe_von(z, slot, iid)
            stuecke.append({"slot": slot, "id": iid, "label": d["label"], "untertitel": d.get("untertitel"),
                            "gruppe": _chip_gruppe(slot), "rosi": st, "plaetze": chip_plaetze(z, slot, iid), "max": 3,
                            "belegt": [f for f in pl.get("%s:%s" % (slot, iid), []) if f in pool],
                            "getragen": (e0.get("weapon") if slot == "weapon" else e0.get("armor")) == iid,
                            "charm": charms.stand(z)["an"].get(iid) if slot == "armor" else None})
    return {"nutzbar": nutzbar, "pool": out, "stuecke": stuecke, "rosi": (defs.get("chips") or {}).get("rosi", {}),
            "charms": charms.ansicht(z)}


def werkstatt_ansicht(z, defs):
    """Workshop block for the cabin: open?, the running order, and per piece the next upgrade with cost and reason."""
    w = defs.get("werkstatt")
    if not w:
        return None
    a = werkstatt(z)["auftrag"]
    mat = w["materialien"]

    def stueck(slot, table):
        out = []
        for iid in besitz(z, defs)[table]:
            d = defs[table][iid]
            st = stufe_von(z, slot, iid)
            k = w["stufen"][st] if st < len(w["stufen"]) else None
            out.append({"slot": slot, "id": iid, "label": d["label"], "untertitel": d.get("untertitel"), "stufe": st,
                        "stufe_max": len(w["stufen"]),
                        "kosten": ({"geld": k["geld"], "material": mat[material_fuer(defs, slot, iid, st)]} if k else None),
                        "fehlt": _werkstatt_fehlt(z, defs, slot, iid)})
        return out
    return {"offen": werkstatt_offen(z, defs), "text_zu": w["text_zu"], "konto": z.get("konto", 0),
            "auftrag": ({"label": defs[{"weapon": "weapons", "armor": "armors"}[a["slot"]]][a["id"]]["label"], "stufe": a["stufe"]}
                        if a else None),
            "waffen": stueck("weapon", "weapons"), "ruestungen": stueck("armor", "armors")}


def profil(z, defs):
    """Equipment and skill tab (outside the fight): level, xp, attributes, gear to choose from, skill tree."""
    c, e = progress(z), equipment(z)
    test = bool(c.get("test"))
    own = besitz(z, defs)
    attrs, base = attributes(z, defs), _persona_attrs(z)
    weapons = [_gear_view(w, d, "weapon", stufe_von(z, "weapon", w)) for w, d in defs["weapons"].items()
               if not d.get("training_only") and (test or w in own["weapons"])]
    armors = [_gear_view(a, d, "armor", stufe_von(z, "armor", a)) for a, d in defs["armors"].items()
              if test or a in own["armors"] or a == e.get("armor")]
    paths, zahlen = [], skill_zahlen(z, defs)
    for p in PATH_ATTR:
        skills = sorted(((sid, s) for sid, s in defs["specials"].items() if s["path"] == p), key=lambda x: x[1]["tier"])
        paths.append({"id": p, "name": PATH_NAME[p], "attribut": PATH_ATTR[p], "attribut_label": ATTR_LABEL[PATH_ATTR[p]],
                      "skills": [{"id": sid, "kuerzel": s["code"], "label": s["label"], "stufe": s["tier"],
                                  "kosten": s["cost"], "text": s["text"], "gelernt": sid in known(z),
                                  "gelehrt": sid in c["taught"] and sid not in c["skills"],
                                  "grund": None if sid in known(z) else learn_reason(z, defs, sid),
                                  "lernfolgen": learning_preview(z, defs, sid),
                                  "zahl": (zahlen.get(sid) or {}).get("chip"), "zahlen": (zahlen.get(sid) or {}).get("zeilen", [])}
                                 for sid, s in skills]})
    mp = main_path(defs, c["skills"])
    depth = path_depth(defs, c["skills"])
    return {"level": c["level"], "level_max": LEVEL_MAX, "xp": c["xp"], "xp_next": xp_needed(c["level"]),
            "lp": lp(z), "lp_max": lp_max_duc(z),
            "ausdauer": max_stamina(c["level"]) + (2 if _sig(defs["armors"].get(_armor_id(e, defs))) == "leicht" else 0),
            "attribute": [{"id": a, "label": ATTR_LABEL[a], "wert": attrs.get(a, 0), "basis": base.get(a, 2),
                           "wirkung": ATTR_WIRKUNG.get(a, ""), "max": ATTR_MAX} for a in ATTR_LABEL],
            "attributpunkte": c["attributpunkte"],
            "hauptpfad": PATH_NAME.get(mp), "skillpunkte": free_points(z), "test": test,
            "hauptpfad_info": main_path_info(mp),
            "hauptpfad_prioritaet": [PATH_NAME[p] for p in PATH_TIE],
            "skillpunkte_gesamt": sum(n for lv, n in SKILL_POINTS.items() if lv <= LEVEL_MAX),
            "skillpunkte_plan": [{"level": lv, "punkte": n} for lv, n in sorted(SKILL_POINTS.items()) if lv <= LEVEL_MAX],
            "waffe": _gear_view(aktive_waffe(z, defs), defs["weapons"][aktive_waffe(z, defs)], "weapon",
                                stufe_von(z, "weapon", aktive_waffe(z, defs))),
            "ruestung": _gear_view(_armor_id(e, defs), defs["armors"].get(_armor_id(e, defs)), "armor",
                                   stufe_von(z, "armor", _armor_id(e, defs))),
            "werkstatt": werkstatt_ansicht(z, defs), "chips": chip_ansicht(z, defs),
            "waffen": weapons, "ruestungen": armors, "pfade": paths,
            "zahlen_basis": {"waffe": defs["weapons"][aktive_waffe(z, defs)]["label"], "staerke": attrs.get("strength", 0),
                             "wahrnehmung": attrs.get("perception", 0), "lp_max": max_lp(c["level"])},
            "hinweis": SMUGGLER_HINT if depth["L"] and "omerta" not in c["skills"] else None}


def skill_zahlen(z, defs):
    """Skill tree (27.10.2026): what each special does right now with Duc's weapon, Rosi's upgrades, chips and attributes.
    -> {sid: {"chip": short text for the node, "zeilen": lines for the detail panel}}. Against an unarmoured enemy
    without weak spots, no crits; display only, uses no game randomness."""
    c, e = progress(z), equipment(z)
    wid, aid = aktive_waffe(z, defs), _armor_id(e, defs)
    w = defs["weapons"][wid]
    dmg = w["dmg"] + stufe_von(z, "weapon", wid) + chips_aktiv(z, defs, wid, aid)["schaden"]
    sp = {"attrs": attributes(z, defs), "weapon": dict(w, dmg=dmg),
          "main_path": main_path(defs, [x for x in c["skills"] if x in defs["specials"]])}
    base = BASE_ATTACK + _attack_attr(sp) + dmg
    lp_max = max_lp(c["level"])
    perc = sp["attrs"].get("perception", 0)
    w_full = perc >= W_FULL_FROM

    def h(f=1.0, extra=0):
        return max(1, round((base + extra) * f))

    def krit(v, mult=CRIT_MULT):
        return int(math.ceil(v * mult))

    def heil(anteil):
        return int(round(lp_max * anteil))

    stun = min(100, int(round(100 * W7_PER_POINT * perc)))
    t = {
        "mistral": ("%d dmg" % h(1, 4), ["%d damage." % h(1, 4), "Shakes them: their armour stops nothing for 2 rounds."]),
        "ressac": ("%d dmg" % h(), ["%d damage, %d against a wet enemy." % (h(), h(2)),
                                    "Against a strong special attack it also weakens them."]),
        "libeccio": ("½ damage", ["For 2 rounds you take only half damage."]),
        "lame_de_fond": ("%d dmg" % h(2), ["%d damage, %d if they're shaken." % (h(2), h(3))]),
        "doppio_gioco": ("2 × %d" % h(L3_FACTOR), ["Two blows of %d damage each, %d in total." % (h(L3_FACTOR), 2 * h(L3_FACTOR))]),
        "sotto_voce": ("Sure crit", ["Your next attack is a sure crit: %d damage with a normal attack." % krit(h()),
                                     "Against a strong special attack their hit is also halved."]),
        "vendetta": ("%d + bleed" % h(L7_FACTOR), ["%d damage, then they bleed: %d%% of their max HP every round."
                                                   % (h(L7_FACTOR), int(BLEED * 100))]),
        "omerta": ("%d+ dmg" % krit(h(), 2.5), ["Always a crit: %d damage." % krit(h(), 2.5),
                                                "+25%% for every state on them, %d with two." % krit(h(1.5), 2.5),
                                                "Right after Sotto Voce: %d." % krit(h(), 3.5)]),
        "point_de_mire": ("Exhaust 3 rds" if w_full else "Exhaust 1 rd", ["They're exhausted for 3 rounds." if w_full else
                                                                "They're exhausted until your next turn. From Perception "
                                                                "%d it lasts 3 rounds (you have %d)." % (W_FULL_FROM, perc)]),
        "bonaccia": ("Block" if w_full else "½ hit", ["Their next hit is halved.",
                                                       "A strong special attack is caught completely." if w_full else
                                                       "From Perception %d it catches a strong special attack completely "
                                                       "(you have %d)." % (W_FULL_FROM, perc)]),
        "phare": ("Skip 1" if w_full else "%d%% stun" % stun,
                  ["Blinds them: they skip a round, two if they're charged with current." if w_full else
                   "Blinds them, and there's a %d%% chance they skip a round (%d%% per Perception, sure from %d)."
                   % (stun, int(W7_PER_POINT * 100), W_FULL_FROM)]),
        "pluie_d_etoiles": ("3 × %d" % h(W9_FACTOR), ["Three blows of %d damage, %d each against flyers." % (h(W9_FACTOR), h())]),
        "scirocco": ("%d + burn" % h(1, 4), ["%d damage and they catch fire." % h(1, 4), "You're exposed for a round."]),
        "retour": ("Counter ×%s" % str(M5_MULT[0]).rstrip("0").rstrip("."),
                   ["Their next attack gets a counter: %d damage after a good parry, %d against a strong special, "
                    "%d if you miss the parry." % (h(M5_MULT[0]), h(M5_MULT[1]), h(M5_MULT[2])),
                    "A made parry also sets them on fire."]),
        "furia": ("+%d%% dmg" % round(100 * (M7_FACTOR - 1)), ["%d damage now, and your hits do %d%% more for 2 rounds."
                                                               % (h(M7_FACTOR), round(100 * (M7_FACTOR - 1))),
                                                               "You catch fire yourself unless your jacket resists it."]),
        "vulcano": ("%d per burn" % h(M9_FACTOR), ["%d damage per burn stack, straight through armour (%d at %d stacks)."
                                                   % (h(M9_FACTOR), BURN_MAX * h(M9_FACTOR), BURN_MAX),
                                                   "Uses up every stack. You skip your next round."]),
        "elicriso": ("+%d HP" % heil(H3_HEAL), ["Heals %d HP, %d%% of your %d." % (heil(H3_HEAL), round(100 * H3_HEAL), lp_max),
                                               "Also ends burning or bleeding on you."]),
        "ponente": ("+%d / round" % heil(H5_HEAL), ["Heals %d HP every round for %d rounds." % (heil(H5_HEAL), H5_ROUNDS),
                                                   "Parrying gets %d%% easier meanwhile." % round(100 * (H5_PARRY - 1))]),
        "risveglio": ("+%d HP" % heil(H7_HEAL), ["Heals %d HP, %d%% of your %d. Once per fight."
                                                % (heil(H7_HEAL), round(100 * H7_HEAL), lp_max)]),
        "arcangelo": ("Revive %d" % heil(H9_LP), ["If you fall in this fight, you rise again with %d HP. Once per fight."
                                                  % heil(H9_LP)]),
    }
    return {sid: {"chip": v[0], "zeilen": v[1]} for sid, v in t.items() if sid in defs["specials"]}


def by_code(defs, codes):
    """["K3", "mistral", ...] -> special ids (working codes or ids)."""
    m = {s["code"].upper(): sid for sid, s in defs["specials"].items()}
    return [m.get(c.strip().upper(), c.strip()) for c in codes if c.strip()]


# ------------------------------------------------------------------ start
def enemy_stats(edef, level, duc_level):
    hp = int(ENEMY_LP * ENEMY_GROWTH ** level)
    atk = ENEMY_ATK + ENEMY_ATK_LV * level
    diff = level - duc_level
    if diff > 0:
        hp, atk = int(hp * (1 + LEVEL_GAP * diff)), atk * (1 + LEVEL_GAP * diff)
    if edef.get("boss"):
        hp = int(hp * BOSS_LP)
    return {"lp": hp, "atk": atk, "armor": 1 + level // 3, "fassung": 12 + 2 * level, "sg": 11 + level // 2}


def _intents(edef):
    out = {"n": {"label": edef["attack"]["label"], "icon": edef["attack"].get("icon", "🗡"), "bonus": 0, "effect": None,
                 "dodge_only": False, "art": "angriff"}}
    if edef["attack"].get("finte"):                       # feint on the normal attack (03.11.2026)
        out["n"]["finte"] = edef["attack"]["finte"]
    for key, sp in edef.get("specials", {}).items():
        out[key] = dict(sp, art="angriff")
    out["flucht"] = {"label": "Flight", "icon": "🏃", "art": "flucht"}
    return out


def starten(z, defs, bid, rueckkehr=None, rng=None, held=None):
    """Start a fight. defs = content of kaempfe.json. Definitions are copied into the fight (stable when data changes).
    held = {"id", "lp_anteil", "tasche"}: another playable fighter instead of Duc (Maxwell at the siege, Duc 01.11.2026). He brings
    his own stats, specials and bag; Duc's bag and LP wait in k["lager"] until schliessen()."""
    if z.get("kampf") and not z["kampf"].get("ergebnis"):
        raise ValueError("A fight is already running.")
    if bid not in defs["encounters"]:
        raise ValueError("Unknown encounter: %s" % bid)
    b = copy.deepcopy(defs["encounters"][bid])
    sel = b.pop("selten", None)                                          # 28.10.2026: seltener Gegner statt des normalen
    if sel:                                                              # Chance steigt je Begegnung ohne ihn um "steigt"
        zaehler = z.setdefault("selten_zaehler", {})
        if (rng or random).random() < sel["chance"] + sel.get("steigt", 0) * zaehler.get(bid, 0):
            b.update({key: v for key, v in sel.items() if key not in ("chance", "steigt")})
            zaehler[bid] = 0
        else:
            zaehler[bid] = zaehler.get(bid, 0) + 1
    if b.get("beistand"):                               # friends at Duc's side (Red Trio), chosen once at the start
        b["beistand"] = next((x["aktionen"] for x in b["beistand"] if regeln.gilt(x.get("wenn"), z)), None)
    b.setdefault("titel", b.get("title"))               # eden.py reads the stage-3 keys (background, chronicle)
    b.setdefault("bild", b.get("image"))
    c = progress(z)
    level = c["level"] + b.get("level_plus", 0) if b.get("level") == "duc" else int(b["level"])
    level = max(1, min(LEVEL_MAX, level))                              # level_plus can go below Duc (Ricci, 29.10.2026)
    thr = threat(level, c["level"])
    # Several enemies (Duc 29.10.2026, like Final Fantasy): "enemies": [id, ...] up to GEGNER_MAX, else "enemy" alone.
    # Same kind twice gets letters (Rat A, Rat B); their patterns are staggered so a pack doesn't strike in unison.
    ids = (b.get("enemies") or [b["enemy"]])[:GEGNER_MAX]
    gegner = []
    for i, eid in enumerate(ids):
        edef = copy.deepcopy(defs["enemies"][eid])
        st = enemy_stats(edef, level, c["level"])
        st["fassung"] = int(st["fassung"] * edef.get("fassung_faktor", 1))     # Rede-Boss (Sirene, 28.10.2026)
        st["armor"] += edef.get("armor_plus", 0)                                # Danzel's plates in the lining (Red Trio)
        lp_f = b.get("lp_faktor", 1) * edef.get("lp_faktor", 1)                 # packs: weak members, one blow each
        anteil = 1
        if b.get("lp_faktoren") and i < len(b["lp_faktoren"]):                    # per member: the alpha stays strong
            anteil = b["lp_faktoren"][i]
            lp_f *= anteil
        if lp_f != 1:
            st["lp"] = max(1, int(round(st["lp"] * lp_f)))
        pattern = list(edef.get("pattern") or PATTERN[edef["tier"]])         # own order, e.g. a combo of two (30.10.2026)
        if len(ids) == 1 and edef.get("pattern_allein"):
            pattern = list(edef["pattern_allein"])
        pattern = [x if x == "n" or x in edef.get("specials", {}) else "n" for x in pattern]
        name = edef["name"]
        if len(ids) > 1 and ids.count(eid) > 1:
            name = "%s %s" % (name, "ABC"[ids[:i + 1].count(eid) - 1])
        gegner.append({"instanz": "%s_%d" % (eid, i + 1), "typ": eid, "name": name, "def": edef, "level": level,
                       "lp": st["lp"], "lp_max": st["lp"], "fassung": st["fassung"], "fassung_max": st["fassung"],
                       "atk": st["atk"], "armor": st["armor"], "sg": st["sg"], "pattern": pattern,
                       "intents": _intents(edef), "schritt": i, "absicht": None, "states": {},
                       "xp_anteil": anteil,                       # a 0.4 rat gives 0.4 of a rat's xp (packs don't inflate levels)
                       "wucht": 0.5 + 0.5 * anteil,               # ...and bites at 70 %: a pack hits often, not three times as hard
                       "bedrohung": {"id": thr[0], "label": thr[1]},
                       # Koepfchen (Duc 29.10.2026, replaces Spot Weakness): a sharp head sees the weakness from round 1
                       "schwaeche_bekannt": has_strength(z, "koepfchen") and bool(edef.get("weakness"))})
    g = gegner[0]
    e = equipment(z)
    wid = b["weapon"] if b.get("weapon") in defs["weapons"] else aktive_waffe(z, defs)   # training: Maxwell's scrubber
    weapon = copy.deepcopy(defs["weapons"][wid])
    weapon["id"] = wid
    weapon["dmg"] += stufe_von(z, "weapon", wid)                           # Rosi's workshop: +1 per upgrade
    armor = copy.deepcopy(defs["armors"][_armor_id(e, defs)])
    armor["id"] = _armor_id(e, defs)
    armor["prot"] += stufe_von(z, "armor", armor["id"])
    agg = chips_aktiv(z, defs, weapon["id"], armor["id"])                  # Erweiterungen (Chips)
    agg["krit"] += kuechen.bonus(z, "krit")                                # Tagesbonus aus dem Essen (Akzent Chilis, 27.10.2026)
    weapon["dmg"] += agg["schaden"]
    if agg["element"] and not weapon.get("element"):
        weapon["element"] = agg["element"]
    armor["prot"] += agg["schutz"]
    attrs = attributes(z, defs)
    stamina = max_stamina(c["level"]) + (2 if _sig(armor) == "leicht" else 0) + agg["ausdauer_max"]          # Zéphyr: Leicht
    skills = [s for s in known(z) if s in defs["specials"]]
    sp = {"lp": lp(z), "lp_max": lp_max_duc(z), "ausdauer": stamina, "ausdauer_max": stamina,
          "level": c["level"], "attrs": attrs, "weapon": weapon, "armor": armor, "skills": skills,
          "main_path": main_path(defs, [s for s in c["skills"] if s in defs["specials"]]), "states": {}, "charged": False, "rausch": 0, "wind": 0,
          "sure_crit": False, "halve_next": False, "bonaccia": None, "hits": 0, "chips": agg}
    h = defs["helden"][held["id"]] if held else None
    if h:
        _held_werte(z, defs, sp, h, held, c["level"])
    pf = None if h else z.get("waffenpflege")
    if pf and pf.get("art") == sp["weapon"]["kind"]:               # weapon care from the inventory (27.10.2026)
        sp["pflege"] = {"bonus": pf["bonus"], "runden": pf["runden"], "label": pf["label"]}
        z.pop("waffenpflege")
    k = {"schema_version": 3, "id": uuid.uuid4().hex[:10], "definition": bid, "def": b,
         "basic": copy.deepcopy(defs["basic"]), "specials": copy.deepcopy(h["specials"]) if h else {s: copy.deepcopy(defs["specials"][s]) for s in skills},
         "revision": 0, "runde": 1, "phase": "spieler_wahl", "spieler": sp, "gegner": gegner, "ziel": 0, "log": [],
         "events": [], "rueckkehr": rueckkehr, "ergebnis": None, "folgen_angewendet": False, "parade": None,
         "parade_serie": 0, "getestet": [], "lp_start": sp["lp"], "inventar_start": list(z.get("inventar", [])), "geld_cfg": defs.get("geld_drop"), "muendung": defs.get("muendung") or {},
         "finten_gesehen": dict(z.get("finten_gesehen") or {})}      # feints met before (marked on the bar, 03.11.2026)
    for x in gegner:
        x["absicht"] = _next_intent(x)
    if h:
        k["held"] = {"id": held["id"], "name": h["name"], "sprite": h["sprite"], "fx_set": h["fx_set"]}
        k["lager"] = {"inventar": list(z.get("inventar", [])), "lp": lp(z), "level": c["level"]}
        z["inventar"] = list(h["tasche"] if held.get("tasche") is None else held["tasche"])
        z["lp"] = sp["lp"]
    if sp["weapon"]["kind"] == "fern":                 # ranged: one free shot before round 1
        ctx = _ctx(k, rng)
        dmg = _hit(ctx)
        if weapon.get("sig") == "first_strom":
            _apply_state(ctx, "strom")
        if weapon.get("sig") == "twin":                  # Gemelli: both barrels (25.10.2026)
            dmg += _hit(ctx)
        ctx["log"].insert(0, "First strike from range: %d damage." % dmg)
        k["log"].append({"runde": 0, "befehl": "erstschlag", "ziel": None, "zeilen": ctx["log"]})
        k["events"] = ctx["events"]
    z["kampf"] = k
    return k


def _held_werte(z, defs, sp, h, held, level):
    """Stats of a playable fighter who is not Duc: his own, growing with Duc's level. No jacket, chips or weapon upgrades of Duc's."""
    weapon = copy.deepcopy(defs["weapons"][h["waffe"]])
    weapon["id"] = h["waffe"]
    weapon["dmg"] += max(0, level - h["level_basis"]) // h["level_schritt"]
    stamina = max(1, max_stamina(level) + h["ausdauer_plus"])
    lp_max = int(round(max_lp(level) * h["lp_faktor"]))
    sp.update(weapon=weapon, armor=copy.deepcopy(h["ruestung"]), attrs=dict(h["attribute"]), skills=list(h["specials"]), main_path=h["pfad"],
              chips=chips_aktiv(z, defs, h["waffe"], None), ausdauer=stamina, ausdauer_max=stamina, lp_max=lp_max,
              lp=max(1, int(round(lp_max * held.get("lp_anteil", 1)))))


def _next_intent(g):
    if g["def"].get("flee_at") and g["lp"] <= g["lp_max"] * g["def"]["flee_at"]:
        return "flucht"
    return g["pattern"][g["schritt"] % len(g["pattern"])]


# ------------------------------------------------------------------ helpers
def lebend(k):
    """Enemies still in the fight (not beaten, not given up, not fled)."""
    return [g for g in k["gegner"] if not g.get("aus")]


def ziel_gegner(k):
    """The enemy Duc is aiming at: the chosen one if it is still standing, else the first one left."""
    i = k.get("ziel", 0)
    if 0 <= i < len(k["gegner"]) and not k["gegner"][i].get("aus"):
        return k["gegner"][i]
    rest = lebend(k)
    return rest[0] if rest else k["gegner"][0]


def _ctx(k, rng=None, probe_fn=None):
    return {"k": k, "sp": k["spieler"], "g": ziel_gegner(k), "rng": rng or random, "probe_fn": probe_fn,
            "log": [], "events": []}


def _sieg_art(k):
    """Everyone is out: a win if at least one was beaten or gave up, else they all got away."""
    aus = [g.get("aus") for g in k["gegner"]]
    return "ko" if "ko" in aus else "aufgabe" if "aufgabe" in aus else "entkommen"


def _ausscheiden(ctx):
    """After a blow: who is down (LP) or gives up (composure) leaves the fight. -> end or None."""
    k, log = ctx["k"], ctx["log"]
    mehrere = len(k["gegner"]) > 1
    for g in lebend(k):
        _unberuehrbar(g)
        if g["lp"] <= 0 and g["def"].get("schlafbar") and not g.get("taumelt"):   # Tierstation: einmal bleibt es stehen, damit die Granate immer eine Chance hat
            g["taumelt"] = True
            g["lp"] = max(1, int(g["lp_max"] * SCHLAF_TAUMELN))
            log.append("%s staggers, but it stays on its feet. One more hit, and it's gone." % g["name"])
        if g["lp"] <= 0:
            g["aus"] = "ko"
            if mehrere:
                log.append("%s goes down." % g["name"])
                _event(ctx, "aus", gegner=g["instanz"], wie="ko")
        elif g["fassung"] <= 0:
            g["aus"] = "aufgabe"
            if mehrere:
                log.append("%s gives up and backs off." % g["name"])
                _event(ctx, "aus", gegner=g["instanz"], wie="aufgabe")
    if not lebend(k):
        return _sieg_art(k)
    if ctx["g"].get("aus"):
        ctx["g"] = ziel_gegner(k)
    return None


def exhausted(g):
    s = g["states"]
    return s.get("erschoepft", 0) > 0 or s.get("blutend", 0) > 0 or bool(s.get("nass") and s.get("schlamm"))


def offen(g, runde=None):
    """Old name (stage 3) for "erschöpft" - the client and the console still ask for it."""
    return exhausted(g)


def _intent(g, key=None):
    return g["intents"][key or g["absicht"]]


def is_special(key):
    return key not in ("n", "flucht")


def hurts(it):
    return it.get("art") == "angriff" and (it.get("bonus", 0) > 0 or it.get("effect") not in HARMLESS)


def _mult(weapon, g):
    m = 1.0
    cls, el = g["def"].get("cls_kampf") or g["def"]["cls"], g["def"].get("element")   # cls_kampf: an animal in steel takes hits like a machine
    if cls in STRONG[weapon["kind"]]:
        m *= TYPE_ADV
    elif cls in WEAK[weapon["kind"]]:
        m *= TYPE_DIS
    if weapon.get("element") and el:
        if BEATS[weapon["element"]] == el:
            m *= ELEM_ADV
        elif BEATS[el] == weapon["element"]:
            m *= ELEM_DIS
    return m


def _mult_tags(weapon, g):
    """What makes a hit strong/weak against this enemy: ["elem:feuer>erde", "art+:fern:flieger", ...] (winner > loser).
    Used for the hit feedback and for codex discoveries (25.10.2026)."""
    tags = []
    cls, el = g["def"].get("cls_kampf") or g["def"]["cls"], g["def"].get("element")   # cls_kampf: an animal in steel takes hits like a machine
    if cls in STRONG[weapon["kind"]]:
        tags.append("art+:%s:%s" % (weapon["kind"], cls))
    elif cls in WEAK[weapon["kind"]]:
        tags.append("art-:%s:%s" % (weapon["kind"], cls))
    if weapon.get("element") and el:
        if BEATS[weapon["element"]] == el:
            tags.append("elem:%s>%s" % (weapon["element"], el))
        elif BEATS[el] == weapon["element"]:
            tags.append("elem:%s>%s" % (el, weapon["element"]))
    return tags


def _attack_attr(sp):
    a = sp["attrs"]
    v = a.get("strength", 2)
    if sp.get("main_path") == "M":
        v = max(v, a.get("courage", 2))
    if sp["weapon"]["kind"] == "messer":
        v = max(v, a.get("cunning", 2))
    return v


def crit_chance(sp):
    return (CRIT_BASE + CRIT_PER_CUNNING * sp["attrs"].get("cunning", 0) + (CRIT_KNIFE if sp["weapon"]["kind"] == "messer" else 0)
            + (sp.get("chips") or {}).get("krit", 0) / 100)


def _enemy_armor(g):
    return g["armor"] + g["states"].get("armor_bonus", 0) if g["states"].get("armor_up") else g["armor"]


def raw_hit(sp, g, extra=0):
    raw = BASE_ATTACK + _attack_attr(sp) + sp["weapon"]["dmg"] + extra - (WEAK_MALUS if sp["states"].get("geschwaecht") else 0)
    raw += (sp.get("pflege") or {}).get("bonus", 0)                 # whetstone, spikes, match ammo
    if exhausted(g):
        raw += KNIFE_EXHAUSTED_BONUS if sp["weapon"]["kind"] == "messer" else EXHAUSTED_BONUS
    return raw


def hit_preview(sp, g, extra=0, factor=1.0, pierce=False):
    """Damage of a normal (non-crit) hit right now - for the menu."""
    f = factor * (M7_FACTOR if sp.get("rausch", 0) > 0 else 1)
    armor = 0 if pierce or g["states"].get("erschuettert") else _enemy_armor(g)
    return max(1, round(raw_hit(sp, g, extra) * _mult(sp["weapon"], g) * f) - armor)


def _event(ctx, art, **kw):
    if len(ctx["k"]["gegner"]) > 1:                        # several enemies: which sprite the client animates
        kw.setdefault("gegner", ctx["g"]["instanz"])
    ctx["events"].append(dict(kw, art=art))


# ------------------------------------------------------------------ states and reactions on the enemy
def _burn_add(holder, n=1):
    holder["brennend"] = min(BURN_MAX, holder.get("brennend", 0) + n)
    holder["burn_new"] = 1
    return holder["brennend"]


def _reaction(ctx, name, text):
    ctx["log"].append("%s! %s" % (name, text))
    _event(ctx, "reaktion", name=name)


def _apply_state(ctx, state, rounds=2, stacks=1):
    """A state on the enemy, with the reactions of the docs. Reaction damage is dealt here -> extra damage."""
    g = ctx["g"]
    s, mx = g["states"], g["lp_max"]
    if state == "blutend" and g["def"]["cls"] == "maschine":
        return 0
    if state in ("strom", "nass") and s.get("nass" if state == "strom" else "strom"):
        s.pop("nass", None)
        s.pop("strom", None)
        s["skip"] = s.get("skip", 0) + 1
        dmg = int(SHORT_CIRCUIT * mx)
        g["lp"] = max(0, g["lp"] - dmg)
        _reaction(ctx, "Short Circuit", "%d damage, and %s skips a round." % (dmg, g["name"]))
        return dmg
    if state == "nass" and s.get("brennend"):
        s.pop("brennend", None)
        s.pop("burn_new", None)
        s["geblendet"] = max(s.get("geblendet", 0), 1)
        _reaction(ctx, "Steam", "Every burn stack is out, and %s is blinded." % g["name"])
        return 0
    if state == "brennend" and s.get("nass"):
        s.pop("nass", None)
        s["geblendet"] = max(s.get("geblendet", 0), 1)
        _reaction(ctx, "Steam", "The water turns to steam, and %s is blinded." % g["name"])
        return 0
    if state == "brennend":
        extra = 0
        if s.get("blutend"):
            extra = int(BURST * mx) * s.pop("blutend")
            g["lp"] = max(0, g["lp"] - extra)
            _reaction(ctx, "Burst", "The wound bursts open: %d damage." % extra)
        n = _burn_add(s, stacks)
        ctx["log"].append("%s is burning (🔥×%d)." % (g["name"], n))
        _event(ctx, "zustand", id="brennend", stufen=n)
        return extra
    if state == "strom" and s.get("brennend"):
        n = _burn_add(s, 1)
        _reaction(ctx, "Sparks", "One more burn stack (🔥×%d)." % n)
    if state == "erschuettert" and s.get("nass"):
        s["schlamm"] = 1
        _reaction(ctx, "Mud", "%s is stuck and counts as exhausted." % g["name"])
    if state == "geschwaecht":
        s["geschwaecht"] = 1
    else:
        s[state] = max(s.get(state, 0), rounds + (1 if state == "blutend" else 0))
    _event(ctx, "zustand", id=state)
    return 0


def n_states(g):
    s = g["states"]
    n = sum(1 for x in ("blutend", "nass", "strom", "erschuettert", "geschwaecht", "erschoepft") if s.get(x))
    return min(L9_STATE_CAP, n + s.get("brennend", 0))


# ------------------------------------------------------------------ Duc's hit
def _hit(ctx, factor=1.0, extra=0, force_crit=False, crit_mult=CRIT_MULT, proc=False, pierce=False):
    """One hit of Duc on the enemy (with crit, weapon state, signature). Deals the damage -> total damage."""
    sp, g, rng = ctx["sp"], ctx["g"], ctx["rng"]
    s, w = g["states"], sp["weapon"]
    if g["def"].get("untouchable"):                                        # Sirene (28.10.2026): nur Reden wirkt
        _unberuehrt(ctx)
        return 0
    if _sig(sp["armor"]) == "glut" and s.get("brennend"):                  # Incendio: +2 per burn stack on the enemy
        extra += 2 * s.get("brennend", 0)
        _event(ctx, "jacke", sig="glut")
    raw = raw_hit(sp, g, extra)
    sp["states"].pop("geschwaecht", None)
    if ctx.get("spezial") and (sp.get("chips") or {}).get("spezial_schaden"):   # Maxwell's charm: specials +20 %
        factor *= 1 + sp["chips"]["spezial_schaden"] / 100.0
    if sp.get("rausch", 0) > 0:
        factor *= M7_FACTOR
    if s.pop("wall", None):
        ctx["log"].append("%s blocks the blow with their guard." % g["name"])
        return 0
    armor = 0 if (pierce or s.get("erschuettert")) else _enemy_armor(g)
    val = max(1, round(raw * _mult(w, g) * factor) - armor)
    crit = force_crit or sp.get("sure_crit") or rng.random() < crit_chance(sp)
    if crit:
        val = int(math.ceil(val * crit_mult))
        _event(ctx, "krit")
    sp["sure_crit"] = False
    if s.pop("dodge", None):
        val //= 2
    g["lp"] = max(0, g["lp"] - val)
    total = val
    ctx["log"].append("%s%d damage." % ("Critical! " if crit else "", val))
    if g["def"].get("unterbrechbar") == g.get("absicht"):                  # Bibi's Nervous Laugh: a hit cuts it off
        g["absicht"] = "n"
        g["fassung"] = max(0, g["fassung"] - UNTERBROCHEN_FASSUNG)
        _reaction(ctx, "Interrupted", "%s loses the thread: only a normal attack, and %d composure gone." % (g["name"], UNTERBROCHEN_FASSUNG))
    m = _mult(w, g)
    _event(ctx, "treffer", schaden=val, krit=bool(crit), wirkung="stark" if m > 1.0 else "schwach" if m < 1.0 else None,
           tags=_mult_tags(w, g))
    sp["hits"] = sp.get("hits", 0) + 1
    ch = sp.get("chips") or {}
    if ch.get("ausdauer_treffer"):                                         # chip: stamina on hits (0.5 = every second hit on average)
        n = ch["ausdauer_treffer"]
        n = int(n) + (1 if rng.random() < n - int(n) else 0)
        sp["ausdauer"] = min(sp["ausdauer_max"], sp["ausdauer"] + n)
    sig = w.get("sig")
    state = STATE_OF.get(w.get("element")) if w.get("element") else ("blutend" if w["kind"] in ("klinge", "messer") else "geschwaecht")
    if sig == "every_burn" and sp["hits"] % 2 == 0:
        total += _apply_state(ctx, "brennend")
    elif sig == "every_strom":
        total += _apply_state(ctx, "strom")
    elif sig == "every_quake":
        total += _apply_state(ctx, "erschuettert")
    if sp.get("rausch", 0) > 0:
        total += _apply_state(ctx, "brennend")
    if crit or proc:
        if sig == "crit_wet_quake":
            total += _apply_state(ctx, "nass")
            total += _apply_state(ctx, "erschuettert")
        elif state == "brennend":
            total += _apply_state(ctx, "brennend", stacks=2 if sig == "burn3" else 1)
        else:
            total += _apply_state(ctx, state)
    for zustand, chance in ch.get("proc") or []:                           # chip: state chance on every hit
        if rng.random() < chance / 100:
            total += _apply_state(ctx, zustand)
    return total


# ------------------------------------------------------------------ skills (basic + specials)
def _resist_state(armor):
    return STATE_OF.get((armor or {}).get("resist") or "")


def _scost(sp, s):
    """Special attack cost after the chips (at least 1)."""
    return max(1, s["cost"] - (sp.get("chips") or {}).get("spezial_kosten", 0))


def skill_info(z, k, sid):
    """Display and check of a skill -> dict or None (not known). Checked against the enemy Duc aims at."""
    sp, g = k["spieler"], ziel_gegner(k)
    attrs = sp["attrs"]
    if sid in k["basic"]:
        f = k["basic"][sid]
        att = f["attr"]
        cost = 0 if f.get("free_with") and has_strength(z, f["free_with"]) else f["cost"]
        weakness = att == g["def"].get("weakness")
        adv = bool(f.get("probe")) and (weakness or (bool(f.get("advantage_with")) and has_strength(z, f["advantage_with"]))
                                         or sid in (sp.get("chips") or {}).get("vorteil", []))      # Elsa's charm: Intimidate
        grund = None
        if att in (g["def"].get("immune") or {}):
            grund = g["def"]["immune"][att]
        elif sp["states"].get("silence"):
            grund = "Silenced: no skills."
        elif sp["ausdauer"] < cost:
            grund = "Not enough stamina (costs %d)." % cost
        info = {"id": sid, "art": "grund", "label": f["label"], "text": f["text"], "attribut": att, "kosten": cost,
                "probe": bool(f.get("probe")), "vorteil": adv, "gesperrt": grund,
                "schwaeche": weakness and g["schwaeche_bekannt"], "zielt": True, "flaeche": False}
        if f.get("probe") and att in (g["def"].get("immune") or {}):
            info["chance"] = None                                           # immune: locked, no odds (Duc 28.10.)
        elif f.get("probe"):
            info.update(sg=g["sg"], wert=attrs.get(att, 0), krit_ab=crit_from(attrs),
                        chance=chance(attrs.get(att, 0), g["sg"], adv, crit_from(attrs)))
        else:
            info["chance"] = 100
            if f["effect"].get("extra"):
                info["schaden"] = hit_preview(sp, g, f["effect"]["extra"])
        return info
    if sid not in k["specials"]:
        return None
    s = k["specials"][sid]
    key = g["absicht"]
    it = _intent(g)
    strong = key.startswith("s")
    grund = None
    if sp["states"].get("silence"):
        grund = "Silenced: no skills."
    elif s.get("answer") and not (is_special(key) and it.get("art") == "angriff"):
        grund = "Only as an answer to an announced special attack."
    elif s.get("strong_only") and not strong:
        grund = "Only against a strong special attack."
    elif s.get("finisher") and not exhausted(g):
        grund = "Finisher: only against an exhausted enemy."
    elif sid == "vulcano" and not g["states"].get("brennend"):
        grund = "They aren't burning, so there's no burn stack to release."
    elif sid == "vendetta" and g["def"]["cls"] == "maschine":
        grund = "Machines don't bleed."
    elif sid == "retour" and sp.get("charged"):
        grund = "Your weapon is already charged."
    elif sid == "parry_the_dirt" and sp.get("charged"):
        grund = "The mop is already waiting for them."
    elif sid == "approves" and sp.get("sure_crit"):
        grund = "Your next hit is already approved."
    elif sid == "libeccio" and sp.get("wind", 0) > 0:
        grund = "Libeccio is still holding."
    elif sid == "furia" and sp.get("rausch", 0) > 0:
        grund = "Furia is still burning."
    elif sid in ONCE_PER_FIGHT and sid in sp.get("einmal", []):
        grund = "Only once per fight."
    elif sid == "ponente" and sp.get("ponente", 0) > 0:
        grund = "Ponente is still blowing."
    elif sid == "arcangelo" and sp.get("arcangelo"):
        grund = "Arcangelo is already watching over you."
    elif sp["ausdauer"] < _scost(sp, s):
        grund = "Not enough stamina (costs %d)." % _scost(sp, s)
    hint = None
    if s.get("answer") and is_special(key) and not grund and not hurts(it):
        hint = "Their special attack won't hurt much, so this is hardly worth it."
    return {"id": sid, "art": "spezial", "label": s["label"], "text": s["text"], "attribut": PATH_ATTR[s["path"]],
            "pfad": s["path"], "pfad_name": PATH_NAME[s["path"]], "stufe": s["tier"], "kuerzel": s["code"],
            "kosten": _scost(sp, s), "probe": False, "chance": 100, "vorteil": False, "gesperrt": grund, "hinweis": hint,
            "schwaeche": False, "flaeche": sid in FLAECHE, "zielt": sid not in FLAECHE and sid not in SELBST}


def skills_view(z, k):
    ids = list(k["basic"]) + [s for s in k["specials"]]
    return [i for i in (skill_info(z, k, sid) for sid in ids) if i]



def has_strength(z, art):
    from . import handel
    return bool(art) and handel.persona_vorteil(z, art)


def crit_from(attrs):
    """W20: crit range grows by one number per 2 cunning (cunning 2: 19-20)."""
    return 20 - attrs.get("cunning", 0) // 2


def chance(bonus, sg, vorteil=False, krit_ab=20):
    """Success chance of a W20 test in percent (crit range always succeeds, natural 1 never)."""
    p = sum(1 for w in range(1, 21) if w >= krit_ab or (w != 1 and w + bonus >= sg)) / 20.0
    return round(100 * (1 - (1 - p) ** 2 if vorteil else p))


def _probe(ctx, att, sg, adv):
    sp = ctx["sp"]
    boni = [(ATTR_LABEL[att], sp["attrs"].get(att, 0))]
    if ctx["probe_fn"]:
        return ctx["probe_fn"](att, sg, boni, adv)
    rng = ctx["rng"]
    w1 = rng.randint(1, 20)
    w2 = rng.randint(1, 20) if adv else None
    wurf = max(w1, w2) if adv else w1
    summe = wurf + sum(b for _, b in boni)
    erg = "kritisch" if wurf >= crit_from(sp["attrs"]) else "patzer" if wurf == 1 else \
        "erfolg" if summe >= sg else "fehlschlag"
    text = {"kritisch": "Critical success", "erfolg": "Success", "fehlschlag": "Failure", "patzer": "Fumble"}[erg]
    p = {"attribut": att, "sg": sg, "wuerfe": [w for w in (w1, w2) if w], "wurf": wurf, "boni": boni, "summe": summe,
         "ergebnis": erg, "text": text}
    wuerfel_anzeige.merken(p)
    return p


def _basic(z, ctx, sid):
    k, sp, g = ctx["k"], ctx["sp"], ctx["g"]
    f = k["basic"][sid]
    info = skill_info(z, k, sid)
    sp["ausdauer"] -= info["kosten"]
    att = f["attr"]
    log = ctx["log"]
    if att not in k["getestet"]:
        k["getestet"].append(att)
    if f.get("probe"):
        p = _probe(ctx, att, g["sg"], info["vorteil"])
        k["letzte_probe"] = p
        w = f["effect"].get(p["ergebnis"], {})
        on_weakness = att == g["def"].get("weakness") and p["ergebnis"] in ("erfolg", "kritisch")
        log.append("%s (%s)." % (f["label"], p["text"]))
    else:
        w, on_weakness = f["effect"], False
        log.append("%s." % f["label"])
    if "extra" in w:
        _hit(ctx, extra=w["extra"])
    minus = w.get("fassung", 0) + (SCHWAECHE_FASSUNG if on_weakness else 0)
    if minus and f.get("probe"):
        minus += (sp.get("chips") or {}).get("fassung", 0)                 # chip: talking and intimidating take more composure
    if minus:
        g["fassung"] = max(0, g["fassung"] - minus)
        log.append("Composure −%d." % minus)
        _event(ctx, "fassung", minus=minus)
    if w.get("exhaust") or on_weakness:
        g["states"]["erschoepft"] = max(g["states"].get("erschoepft", 0), 2)
        log.append("%s is exhausted (next hit +%d)." % (g["name"], EXHAUSTED_BONUS))
    if w.get("weaken"):                                    # Intimidate: two attacks (Duc 29.10.2026, was one)
        g["states"]["geschwaecht"] = max(g["states"].get("geschwaecht", 0), WEAKEN_ATTACKS)
        log.append("%s is weakened (next %d attacks −%d)." % (g["name"], WEAKEN_ATTACKS, WEAK_MALUS))
        andere = [x for x in lebend(k) if x is not g and att not in (x["def"].get("immune") or {})]
        for x in andere:                                   # the rest of the pack saw it (several enemies, 29.10.2026)
            x["fassung"] = max(0, x["fassung"] - SCHRECK_ANDERE)
        if andere:
            log.append("The others flinch: composure −%d." % SCHRECK_ANDERE)
    if on_weakness:
        g["schwaeche_bekannt"] = True
        log.append("You hit their weakness!")
    if w.get("exposed"):
        sp["states"]["ungedeckt"] = 1
        log.append("That backfires, and you're exposed.")



def _special(z, ctx, sid):
    k, sp, g, rng = ctx["k"], ctx["sp"], ctx["g"], ctx["rng"]
    s = k["specials"][sid]
    sp["ausdauer"] -= _scost(sp, s)
    log = ctx["log"]
    log.append("%s!" % s["label"])
    _event(ctx, "spezial", id=sid, phase="start")
    key = g["absicht"]
    strong = key.startswith("s")
    perc = sp["attrs"].get("perception", 0)
    w_full = perc >= W_FULL_FROM
    st = g["states"]
    if sid == "mistral":                                           # hits every enemy (FLAECHE, 29.10.2026)
        for tg in _flaeche(ctx):
            _hit(ctx, extra=4)
            _apply_state(ctx, "erschuettert", 2)
            log.append("%s is shaken (no protection)." % tg["name"])
    elif sid == "ressac":
        _hit(ctx, 2.0 if st.get("nass") else 1.0)
        if strong:
            st["geschwaecht"] = 1
            log.append("%s is weakened." % g["name"])
    elif sid == "libeccio":
        sp["wind"] = 2
        log.append("Libeccio: half damage for 2 rounds.")
    elif sid == "lame_de_fond":                                    # every enemy; the finisher bonus only on the exhausted
        einer = len(lebend(k)) == 1
        for tg in _flaeche(ctx):
            ts = tg["states"]
            _hit(ctx, (3.0 if ts.get("erschuettert") else 2.0) if einer or exhausted(tg) else 1.0)
    elif sid == "doppio_gioco":
        _hit(ctx, L3_FACTOR)
        _hit(ctx, L3_FACTOR)
    elif sid == "sotto_voce":
        sp["sure_crit"] = True
        if strong:
            sp["halve_next"] = True
        log.append("Your next attack is a sure crit%s." % (", and their hit is halved" if strong else ""))
    elif sid == "vendetta":
        _hit(ctx, L7_FACTOR)
        _apply_state(ctx, "blutend")
        log.append("%s is bleeding." % g["name"])
    elif sid == "omerta":
        mult = 3.5 if sp.get("sure_crit") else 2.5
        _hit(ctx, 1 + 0.25 * n_states(g), force_crit=True, crit_mult=mult)
    elif sid == "point_de_mire":
        st["erschoepft"] = max(st.get("erschoepft", 0), 3 if w_full else 2)
        log.append("%s is exhausted%s." % (g["name"], "" if w_full else " (until your next turn)"))
    elif sid == "bonaccia":
        sp["bonaccia"] = "voll" if strong and w_full else "halb"
        log.append("Bonaccia: their hit will be %s." % ("caught completely" if sp["bonaccia"] == "voll" else "halved"))
    elif sid == "phare":
        if w_full:
            n = 2 if st.get("strom") else 1
            st["skip"] = st.get("skip", 0) + n
            st["geblendet"] = max(st.get("geblendet", 0), 1)
            log.append("Blinded: %s skips %d round%s." % (g["name"], n, "s" if n > 1 else ""))
        else:
            st["geblendet"] = max(st.get("geblendet", 0), 1)
            if rng.random() < W7_PER_POINT * perc:
                st["skip"] = st.get("skip", 0) + 1
                log.append("Blinded: %s skips a turn." % g["name"])
            else:
                log.append("%s is blinded but attacks anyway." % g["name"])
    elif sid == "pluie_d_etoiles":
        f = 1.0 if g["def"]["cls"] == "flieger" else W9_FACTOR
        for _ in range(3):
            _hit(ctx, f, proc=True)
    elif sid == "scirocco":
        _hit(ctx, extra=4)
        _apply_state(ctx, "brennend")
        sp["states"]["ungedeckt"] = 1
        log.append("You're exposed.")
    elif sid == "retour":
        sp["charged"] = True
        log.append("Your weapon glows. Their next attack gets a counter.")
        _event(ctx, "spezial", id=sid, phase="aufladen")
    elif sid == "parry_the_dirt":                                  # Maxwell: wie Retour, ohne Feuer
        sp["charged"] = "dreck"
        log.append("You plant your feet and wait. Their next attack gets a counter.")
        _event(ctx, "spezial", id=sid, phase="aufladen")
    elif sid == "maximum":
        _hit(ctx, X_MASCHINE if g["def"].get("cls") == "maschine" else 1.0, extra=5)
        _apply_state(ctx, "erschuettert", 1)
        log.append("%s is shaken (no protection)." % g["name"])
    elif sid == "approves":
        sp["ausdauer"] = min(sp["ausdauer_max"], sp["ausdauer"] + APPROVES_AUSDAUER)
        sp["sure_crit"] = True
        log.append("+%d stamina, and your next hit is a sure crit." % APPROVES_AUSDAUER)
        _event(ctx, "spezial", id=sid, phase="aufladen")
    elif sid == "furia":
        sp["rausch"] = 2
        if _resist_state(sp["armor"]) != "brennend":
            n = _burn_add(sp["states"], 1)
            log.append("You catch fire yourself (🔥×%d)." % n)
        _hit(ctx)
    elif sid == "elicriso":
        _heilen(ctx, H3_HEAL)
        for x in ("brennend", "blutend"):
            if sp["states"].pop(x, None):
                sp["states"].pop("burn_new", None)
                log.append("The oil soothes it: no more %s." % STATE_LABEL.get(x, x))
                break
    elif sid == "ponente":
        sp["ponente"] = H5_ROUNDS
        log.append("Ponente: a mild west wind. You heal a little every round, and parrying gets easier.")
    elif sid == "risveglio":
        sp.setdefault("einmal", []).append(sid)
        _heilen(ctx, H7_HEAL)
    elif sid == "arcangelo":
        sp.setdefault("einmal", []).append(sid)
        sp["arcangelo"] = True
        log.append("Arcangelo watches over you. If you fall in this fight, you rise again.")
        _event(ctx, "spezial", id=sid, phase="aufladen")
    elif sid == "vulcano":
        n = st.get("brennend", 0)
        for _ in range(n):
            _hit(ctx, M9_FACTOR, pierce=True)
        st.pop("brennend", None)
        st.pop("burn_new", None)
        sp["states"]["aussetzen"] = 1
        log.append("%d blows, every burn stack used up. You have to skip a round." % n)


def _flaeche(ctx):
    """Area effect: run the body once per enemy still standing, with ctx["g"] set to it (one enemy = once, as before)."""
    k, alt = ctx["k"], ctx["g"]
    for g in lebend(k):
        ctx["g"] = g
        yield g
    ctx["g"] = alt if not alt.get("aus") and alt["lp"] > 0 else ziel_gegner(k)


def _heilen(ctx, anteil):
    """Healer path: heal a share of Duc's max LP."""
    sp = ctx["sp"]
    plus = min(sp["lp_max"] - sp["lp"], int(round(sp["lp_max"] * anteil)))
    sp["lp"] += plus
    ctx["log"].append("You heal %d HP." % plus)
    return plus


def _arcangelo(ctx):
    """Arcangelo: Duc fell - he rises once with half his LP. -> True if it saved him."""
    sp = ctx["sp"]
    if sp["lp"] > 0 or not sp.pop("arcangelo", False):
        return False
    sp["lp"] = int(round(sp["lp_max"] * H9_LP))
    ctx["log"].append("Arcangelo! You rise again with %d HP." % sp["lp"])
    _event(ctx, "spezial", id="arcangelo", phase="rettung")
    return True


# ------------------------------------------------------------------ items
# Combat consumables (Duc + Brain Trust 27.10.2026, wiki kampf.md "Gegenstände"): the item's "kampf" field holds one rule:
# heilen (flat) / heil_pct, stoppt (states on Duc or "alle"), ausdauer, ausdauer_runden [n, rounds], parade [factor, rounds],
# schutz, immun [state, rounds], gegner {class: {aussetzen, fassung, erschoepft}}, rauch, pflege {art, bonus, runden},
# granate {pct (of the enemy's max HP, through armour, bosses BOSS_BURN), zustand, runden, stapel} (Rosi, Akt 2).
# schnell: costs no turn, one quick item per round.
DUC_BAD = ("brennend", "blutend", "nass", "strom", "erschuettert", "geblendet", "silence", "ungedeckt", "betaeubt", "geschwaecht")
GEGNER_NEIN = {"dog_food": "%s isn't interested in dog food."}
SCHLAF_TAUMELN = 0.05        # auf so viel LP-Anteil faengt sich ein Stationstier beim ersten Mal, wenn der Schlag es umhauen wuerde


def heilwert(z, modul, iid):
    it = (modul.get("items") or {}).get(iid) or {}
    if (it.get("kampf") or {}).get("heilen"):
        return it["kampf"]["heilen"]
    if it.get("art") == "snack":
        bonus = (((z.get("kampf") or {}).get("spieler") or {}).get("chips") or {}).get("snack", 0)
        return SNACK_HEAL + (KITCHEN_BONUS if has_strength(z, "kueche") else 0) + bonus
    return 0


def kampfwirkung(z, modul, iid):
    """The item's combat rule -> dict ({} = no use in a fight). Snacks heal a flat amount."""
    w = dict(((modul.get("items") or {}).get(iid) or {}).get("kampf") or {})
    h = heilwert(z, modul, iid)
    if h:
        w["heilen"] = h
    return w


def _heilung(sp, w):
    return w.get("heilen", 0) + int(round(sp["lp_max"] * w.get("heil_pct", 0)))


def _stoppt(sp, w):
    st = w.get("stoppt") or []
    return [x for x in (DUC_BAD if st == "alle" else st) if sp["states"].get(x)]


def schlaf_chance(g, w):
    """Schlafgranate (Duc 01.11.2026, Wiki systeme/tierstation.md): unter "sicher" LP-Anteil immer, darueber faellt sie im Quadrat bis "boden" ab. Das Halsband haelt dagegen."""
    s, anteil = w["schlaf"], g["lp"] / g["lp_max"]
    if anteil <= s["sicher"]:
        return 1.0
    return max(s["boden"], ((1 - anteil) / (1 - s["sicher"])) ** 2 * g["def"].get("schlaf_faktor", 1))


def _granat_schaden(g, w):
    gr = w.get("granate") or {}
    if not gr.get("pct"):
        return 0
    return max(1, int(round(g["lp_max"] * gr["pct"] * (BOSS_BURN if g["def"].get("boss") else 1))))


def gegenstand_grund(k, w, iid=None):
    """Why this item can't be used now -> English text or None."""
    sp, g = k["spieler"], ziel_gegner(k)
    if not w:
        return "That won't help in a fight."
    if w.get("schnell") and sp.get("schnell_runde") == k["runde"]:
        return "One quick item per round."
    if w.get("pflege") and w["pflege"]["art"] != sp["weapon"]["kind"]:
        return "Not for %s." % sp["weapon"].get("label", "this weapon")
    if w.get("gegner") and g["def"]["cls"] not in w["gegner"]:
        return (GEGNER_NEIN.get(iid) or "No effect on %s.") % g["name"]
    if w.get("schutz") and sp.get("tape"):
        return "Your jacket is already patched."
    if (w.get("granate") or {}).get("zustand") == "blutend" and g["def"]["cls"] == "maschine":
        return "Shrapnel does nothing to a machine."
    if w.get("schlaf"):
        return None if g["def"].get("schlafbar") else "This is only for Bibi's animals."
    if (_heilung(sp, w) and sp["lp"] < sp["lp_max"]) or _stoppt(sp, w) \
            or (w.get("ausdauer") and sp["ausdauer"] < sp["ausdauer_max"]) \
            or any(w.get(x) for x in ("ausdauer_runden", "schutz", "immun", "rauch", "gegner", "pflege", "granate")) \
            or (w.get("parade") or [0])[0] > 0:                      # the double espresso's shaky hands are no reason
        return None
    if _heilung(sp, w):
        return "You're not hurt."
    if w.get("ausdauer"):
        return "Your stamina is full."
    return "That wouldn't do anything right now."


def _kurz(sp, w, g=None):
    """Short number for the item list: +9 HP, +2 stamina, ..."""
    if w.get("schlaf") and g and g["def"].get("schlafbar"):
        return "%d %%" % round(schlaf_chance(g, w) * 100)
    if w.get("granate") and g:
        return "%d dmg" % _granat_schaden(g, w) if _granat_schaden(g, w) else STATE_LABEL.get(w["granate"]["zustand"], "")
    h = _heilung(sp, w)
    if h:
        return "+%d HP" % h
    if w.get("ausdauer"):
        return "+%d stamina" % w["ausdauer"]
    if w.get("pflege"):
        return "+%d dmg" % w["pflege"]["bonus"]
    return ""


def gegenstaende(z, modul):
    """Inventory items usable in a fight (with the reason when they can't be used right now)."""
    k = z["kampf"]
    out = []
    for iid in dict.fromkeys(z.get("inventar", [])):
        w = kampfwirkung(z, modul, iid)
        if not w:
            continue
        it = modul["items"][iid]
        out.append({"id": iid, "label": it["label"], "text": it.get("wirkung_text") or it.get("text", ""), "n": z["inventar"].count(iid),   # Stapeln (28.10.2026)
                    "heilen": _heilung(k["spieler"], w),
                    "zahl": _kurz(k["spieler"], w, ziel_gegner(k)), "schnell": bool(w.get("schnell")),
                    "gesperrt": gegenstand_grund(k, w, iid),
                    "flaeche": bool(w.get("granate")), "zielt": bool(w.get("gegner"))})   # Zielwahl im Client (29.10.2026)
    return out


def gegenstand_anwenden(ctx, modul, iid, w):
    """Use one item in the fight (already checked). Writes the log lines."""
    sp, g, log = ctx["sp"], ctx["g"], ctx["log"]
    ds, s, label = sp["states"], g["states"], modul["items"][iid]["label"]
    teile = []
    h = _heilung(sp, w)
    if h:
        before = sp["lp"]
        sp["lp"] = min(sp["lp_max"], sp["lp"] + h)
        teile.append("+%d HP" % (sp["lp"] - before))
    weg = _stoppt(sp, w)
    for x in weg:
        ds.pop(x, None)
        if x == "brennend":
            ds.pop("burn_new", None)
    if weg:
        teile.append("no longer " + ", ".join(STATE_LABEL.get(x, x) for x in weg))
    if w.get("ausdauer"):
        before = sp["ausdauer"]
        sp["ausdauer"] = min(sp["ausdauer_max"], sp["ausdauer"] + w["ausdauer"])
        teile.append("+%d stamina" % (sp["ausdauer"] - before))
    if w.get("ausdauer_runden"):
        sp["koffein"] = list(w["ausdauer_runden"])
        teile.append("+%d stamina every round for %d rounds" % tuple(w["ausdauer_runden"]))
    if w.get("parade"):
        f, n = w["parade"]
        sp.setdefault("parade_mods", []).append([f, n])
        teile.append("parry window %+d %% for %d round%s" % (round(f * 100), n, "s" if n > 1 else ""))
    if w.get("schutz"):
        sp["armor"]["prot"] = sp["armor"].get("prot", 0) + w["schutz"]
        sp["tape"] = True
        teile.append("protection +%d for this fight" % w["schutz"])
    if w.get("immun"):
        x, n = w["immun"]
        sp.setdefault("immun", {})[x] = n
        teile.append("you can't be %s for %d rounds" % (STATE_LABEL.get(x, x), n))
    if w.get("rauch"):
        sp["rauch"] = {"angriff": True, "runden": 2}
        teile.append("smoke all around you")
    if w.get("gegner"):
        e = w["gegner"][g["def"]["cls"]]
        if e.get("aussetzen"):
            s["skip"] = s.get("skip", 0) + e["aussetzen"]
            teile.append("%s skips a round" % g["name"])
        if e.get("fassung"):
            g["fassung"] = max(0, g["fassung"] - e["fassung"])
            teile.append("composure −%d" % e["fassung"])
        if e.get("erschoepft"):
            s["erschoepft"] = max(s.get("erschoepft", 0), e["erschoepft"])
            teile.append("%s is exhausted" % g["name"])
    if w.get("pflege"):
        p = w["pflege"]
        sp["pflege"] = {"bonus": p["bonus"], "runden": p["runden"], "label": label}
        teile.append("+%d damage for %d rounds" % (p["bonus"], p["runden"]))
    if w.get("granate"):                                   # straight through armour, every enemy (29.10.2026), then states
        schaden = []
        for tg in _flaeche(ctx):
            if tg["def"].get("untouchable"):               # the sea swallows it - and she comments (Sirene, 29.10.2026)
                _unberuehrt(ctx)
            dmg = _granat_schaden(tg, w)
            if dmg:
                tg["lp"] = max(0, tg["lp"] - dmg)
                schaden.append(dmg)
                _event(ctx, "treffer", schaden=dmg, krit=False, wirkung=None, tags=[])
        if schaden:
            teile.append("%s damage" % " / ".join(str(x) for x in schaden))
    if w.get("schlaf"):                                    # Fassung 0 = "aufgabe": So endet die Rettung in _ausscheiden
        if ctx["rng"].random() < schlaf_chance(g, w):
            g["fassung"] = 0
            teile.append("%s falls asleep, and the collar goes quiet" % g["name"])
        else:
            teile.append("the collar fires, and %s shakes it off" % g["name"])
    log.append("%s: %s." % (label, "; ".join(teile) or "nothing happens"))
    _event(ctx, "gegenstand", id=iid, schnell=bool(w.get("schnell")),
           granate="schlaf" if w.get("schlaf") else (w.get("granate") or {}).get("zustand"))       # the client throws it and blows it up in the element's colour
    if w.get("granate"):
        gr = w["granate"]
        for tg in _flaeche(ctx):
            if tg["lp"] > 0:
                _apply_state(ctx, gr["zustand"], rounds=gr.get("runden", 2), stacks=gr.get("stapel", 1))


def _gegenstand_runde(ctx):
    """Item effects that run out at the end of a round."""
    sp, log = ctx["sp"], ctx["log"]
    if sp.get("koffein") and sp["lp"] > 0:
        n, r = sp["koffein"]
        sp["ausdauer"] = min(sp["ausdauer_max"], sp["ausdauer"] + n)
        log.append("Americano: +%d stamina." % n)
        sp["koffein"] = [n, r - 1] if r > 1 else None
    mods = [[f, n - 1] for f, n in sp.get("parade_mods") or [] if n > 1]
    sp["parade_mods"] = mods
    sp["immun"] = {x: n - 1 for x, n in (sp.get("immun") or {}).items() if n > 1}
    if sp.get("rauch"):
        sp["rauch"]["runden"] -= 1
        if sp["rauch"]["runden"] <= 0:
            sp.pop("rauch")
    if sp.get("pflege"):
        sp["pflege"]["runden"] -= 1
        if sp["pflege"]["runden"] <= 0:
            log.append("%s has worn off." % sp.pop("pflege")["label"])


def pflege_vorbereiten(z, modul, iid):
    """Weapon care used from the inventory before a fight: works in the next fight with that kind of weapon."""
    it = modul["items"][iid]
    p = (it.get("kampf") or {}).get("pflege")
    if not p:
        raise ValueError("%s isn't weapon care." % it["label"])
    z["inventar"].remove(iid)
    z["waffenpflege"] = {"item": iid, "art": p["art"], "bonus": p["bonus"], "runden": p["runden"], "label": it["label"]}
    return ["%s: ready for your next fight with %s, +%d damage for %d rounds."
            % (it["label"], KIND_DE.get(p["art"], p["art"]).lower(), p["bonus"], p["runden"])]


# ------------------------------------------------------------------ move
def must_skip(sp):
    return bool(sp["states"].get("aussetzen") or sp["states"].get("betaeubt"))


def pruefen(z, modul, befehl, ziel=None, revision=None):
    """German error text or None - changes nothing."""
    k = z.get("kampf")
    if not k or k.get("ergebnis"):
        return "There's no fight running."
    if revision is not None and revision != k["revision"]:
        return "That turn has already happened (the screen was out of date)."
    if k.get("phase") == "parade":
        return "Parry first, the blow is coming."
    sp = k["spieler"]
    if must_skip(sp):
        return None if befehl == "aussetzen" else "You have to skip this round."
    if befehl not in BEFEHLE:
        return "Unknown command."
    if befehl == "faehigkeit":
        info = skill_info(z, k, ziel)
        if not info:
            return "You don't have that skill."
        return info["gesperrt"]
    if befehl == "verteidigen" and sp.get("rausch", 0) > 0:
        return "No defending during Furia."
    if befehl == "gegenstand":
        if ziel not in z.get("inventar", []):
            return "Not in your inventory."
        return gegenstand_grund(k, kampfwirkung(z, modul, ziel), ziel)
    if befehl == "fliehen":
        if not k["def"].get("flee_allowed", True):
            return k["def"].get("flee_reason") or "You can't run away here."
        if _flucht_sg(k) is None:
            return "There's no escaping this enemy."
    return None


def _flucht_sg(k):
    """Flee DC of the whole group: the hardest one still standing decides (None = no escape)."""
    dcs = [FLEE_DC[g["def"]["tier"]] for g in lebend(k)] or [FLEE_DC[k["gegner"][0]["def"]["tier"]]]
    return None if None in dcs else max(dcs)


def ziel_waehlen(z, index):
    """Aim at another enemy (Final Fantasy style). Costs nothing; only enemies still standing."""
    k = z.get("kampf")
    try:
        i = int(index)
    except (TypeError, ValueError):
        raise ValueError("Unknown target.")
    if not k or not 0 <= i < len(k["gegner"]) or k["gegner"][i].get("aus"):
        raise ValueError("That enemy is no longer in the fight.")
    k["ziel"] = i


def zug(z, modul, befehl, ziel=None, revision=None, probe_fn=None, parade=None, rng=None, gegner=None):
    """Carry out one command. probe_fn(attr, sg, boni, advantage) and rng (.random/.randint) for fixed dice in tests.
    gegner = index of the enemy Duc aims at (several enemies, 29.10.2026; default: the last one chosen / the first left).
    If the enemy attacks afterwards the fight is in phase "parade" until parade_aufloesen() gets the reaction result;
    parade="verfehlt"/... resolves it right away (tests, console)."""
    if gegner is not None:
        ziel_waehlen(z, gegner)
    fehler = pruefen(z, modul, befehl, ziel, revision)
    if fehler:
        raise ValueError(fehler)
    z_copy = {"persona": z.get("persona"), "inventar": list(z.get("inventar", [])), "kampf": copy.deepcopy(z["kampf"])}
    k = z_copy["kampf"]
    ctx = _ctx(k, rng, probe_fn)
    sp, g, log = ctx["sp"], ctx["g"], ctx["log"]
    guard, ende, schnell = False, None, False
    if befehl == "aussetzen":
        why = "Stunned" if sp["states"].pop("betaeubt", None) else "Worn out after Vulcano"
        sp["states"].pop("aussetzen", None)
        log.append("%s, so you skip a turn." % why)
    elif sp["states"].get("strom") and ctx["rng"].random() < STROM_FAIL:
        log.append("Current jolts through your muscles and your turn fizzles out.")
    elif befehl == "angriff":
        log.append("You attack %s." % g["name"])
        _hit(ctx)
        sp["ausdauer"] = min(sp["ausdauer_max"], sp["ausdauer"] + 1)
    elif befehl == "verteidigen":
        guard = True
        sp["states"]["guard"] = 1
        sp["ausdauer"] = min(sp["ausdauer_max"], sp["ausdauer"] + 2 + (sp.get("chips") or {}).get("ausdauer_verteidigen", 0))
        log.append("You take cover.")
        if sp["states"].get("brennend"):
            sp["states"]["brennend"] -= 1
            if sp["states"]["brennend"] <= 0:
                sp["states"].pop("brennend")
                sp["states"].pop("burn_new", None)
            log.append("You smother a flame on yourself.")
    elif befehl == "faehigkeit":
        if ziel in k["basic"]:
            _basic(z_copy, ctx, ziel)
        else:
            if g["states"].get("erschoepft"):              # training task (Duc 02.11.2026): special on an exhausted target
                k.setdefault("stat", {})["spezial_erschoepft"] = True
            ctx["spezial"] = True
            _special(z_copy, ctx, ziel)
            ctx.pop("spezial", None)
    elif befehl == "gegenstand":
        w = kampfwirkung(z, modul, ziel)
        gegenstand_anwenden(ctx, modul, ziel, w)
        z_copy["inventar"].remove(ziel)
        from . import handel                               # Gras-Kuchen: Kater morgen, Brownie Moral +1
        log += [str(x) for x in handel.gras_gegessen(z, modul, ziel)]
        if w.get("schnell"):                               # quick item: Duc still has his turn
            schnell = True
            sp["schnell_runde"] = k["runde"]
    elif befehl == "fliehen" and sp.get("rauch") and not any(x["def"].get("boss") for x in lebend(k)):
        ende = "flucht"
        log.append("Under cover of the smoke you slip away.")
    elif befehl == "fliehen":
        p = _probe(ctx, "courage", _flucht_sg(k) - (3 if _sig(sp["armor"]) == "leicht" else 0), False)
        k["letzte_probe"] = p
        if p["ergebnis"] in ("erfolg", "kritisch"):
            ende = "flucht"
            log.append("Flee (%s): you get away." % p["text"])
        else:
            log.append("Flee (%s): they cut you off." % p["text"])
    if sp.get("rausch", 0) > 0 and not (befehl == "faehigkeit" and ziel == "furia") and not schnell:
        sp["rausch"] -= 1
    if ende:
        for x in lebend(k):
            _unberuehrbar(x)
    else:
        ende = _ausscheiden(ctx)
    if not ende and not schnell:
        ende = _gegner_runde(ctx, neu=True)
    _spruch(ctx, ende, zug=True)
    k["revision"] += 1
    k["events"] = ctx["events"]
    k["log"] = (k["log"] + [{"runde": k["runde"], "befehl": befehl, "ziel": ziel, "zeilen": log}])[-LOG_MAX:]
    z["inventar"] = z_copy["inventar"]
    z["kampf"] = k
    if ende:
        _finish(z, modul, k, ende)
    elif k["phase"] == "parade" and parade is not None:
        return parade_aufloesen(z, modul, parade, probe_fn=probe_fn, rng=rng)
    z["lp"] = k["spieler"]["lp"]
    return k


def _unberuehrt(ctx):
    """Duc strikes an untouchable enemy (weapon, special or grenade) - once per action, however many hits. The first
    strikes get her escalating hints (Duc 29.10.2026, untouchable_hinweise: tease, small hints, then the direct one),
    voiced as kampf.<enemy>.<n>; the last one also shows her weakness, so Talk lights up. After that the plain line."""
    g = ctx["g"]
    if ctx.get("unberuehrt"):
        return
    ctx["unberuehrt"] = True
    n = g["unberuehrt"] = g.get("unberuehrt", 0) + 1
    hinweise = g["def"].get("untouchable_hinweise") or []
    if n > len(hinweise):
        ctx["log"].append(g["def"]["untouchable"])
        return
    h = hinweise[n - 1]
    ctx["log"].append("%s: “%s”" % (g["name"], h["text"]))
    _event(ctx, "stimme", schluessel="kampf.%s.%d" % (g["typ"], n - 1), wer=h.get("wer"), text=h["text"],
           name=g["name"], icon="🎶")
    if n == len(hinweise):
        g["schwaeche_bekannt"] = True


def _spruch(ctx, ende, zug=False):
    """Enemies who talk while they fight (the Ricci brothers, Duc 29.10.2026, def "sprueche"): after each of Duc's
    turns one taunt - first the "start" lines in order, then "runde" in a cycle -, at the end "verliert" (Duc won) or
    "gewinnt" (Duc lost, fled, they got away). Voiced as kampf.<enemy>.<art>.<n>, shown like the Siren's hints."""
    g, b = ctx["g"], ctx["k"]["def"]
    # a group talks as one (encounter "sprueche", keys kampf.<sprueche_id>.*), a lone enemy with its own lines
    s = b.get("sprueche") or g["def"].get("sprueche")
    schluessel_id = b.get("sprueche_id", ctx["k"].get("definition")) if b.get("sprueche") else g["typ"]
    zaehler = ctx["k"] if b.get("sprueche") else g
    if not s:
        return
    if ende in ("ko", "aufgabe"):
        art, i = "verliert", 0
    elif ende in ("niederlage", "flucht", "entkommen"):
        art, i = "gewinnt", 0
    elif zug and not ende:
        n = zaehler["sprueche_n"] = zaehler.get("sprueche_n", 0) + 1
        start = s.get("start") or []
        art, i = ("start", n - 1) if n <= len(start) else ("runde", (n - 1 - len(start)) % max(1, len(s.get("runde") or [])))
    else:
        return
    liste = s.get(art) or []
    if i >= len(liste):
        return
    h = liste[i]
    name = h.get("name") or h["wer"].capitalize()
    ctx["log"].append("%s: “%s”" % (name, h["text"]))
    _event(ctx, "stimme", schluessel="kampf.%s.%s.%d" % (schluessel_id, art, i), wer=h["wer"], name=name, text=h["text"],
           icon="💬")


def _unberuehrbar(g):
    """Gegner mit "untouchable" (Sirene) verlieren nie LP - Feuer, Blutung und Granaten gehen durch wie Wasser."""
    if g["def"].get("untouchable"):
        g["lp"] = g["lp_max"]


def _gegner_runde(ctx, neu=False):
    """The enemies act one after the other (Final Fantasy order, the order of k["gegner"]). An attack stops the round
    for the parade (parade_aufloesen continues with the rest); when all have acted the round ends. -> end or None."""
    k = ctx["k"]
    if neu:
        k["zug_rest"] = [i for i, g in enumerate(k["gegner"]) if not g.get("aus")]
    while k.get("zug_rest"):
        g = k["gegner"][k["zug_rest"].pop(0)]
        if g.get("aus"):
            continue
        ctx["g"] = g
        r = _enemy_turn(ctx)
        if r == "parade":
            return None
        if r == "flucht":
            g["aus"] = "entkommen"
            if not lebend(k):
                return _sieg_art(k)
    ctx["g"] = ziel_gegner(k)
    return _end_of_round(ctx)


def _enemy_turn(ctx):
    """One enemy carries out its announced intent. -> "parade" (an attack waits for Duc's reaction), "flucht" (it runs
    off) or None (done, the next one acts)."""
    k, sp, g, log = ctx["k"], ctx["sp"], ctx["g"], ctx["log"]
    key = g["absicht"]
    it = _intent(g)
    if it.get("art") == "flucht":
        log.append("%s runs off." % g["name"])
        return "flucht"
    g["schritt"] += 1
    s = g["states"]
    if s.get("skip"):
        s["skip"] -= 1
        if s["skip"] <= 0:
            s.pop("skip")
        log.append("%s skips a turn." % g["name"])
        return None
    if s.get("strom") and ctx["rng"].random() < STROM_FAIL:
        log.append("%s twitches with current and misses their turn." % g["name"])
        return None
    eff = it.get("effect")
    if eff in HARMLESS:
        if eff in ("heal3", "heal5"):
            n = 3 if eff == "heal3" else 5
            before = g["lp"]
            g["lp"] = min(g["lp_max"], g["lp"] + n)
            log.append("%s: %s – +%d HP." % (g["name"], it["label"], g["lp"] - before))
        elif eff.startswith("buff"):
            s["buff"] = 2 if eff.endswith("x2") else 1
            s["buff_atk"] = 4 if "4" in eff else 3
            log.append("%s: %s – attack +%d (%d round%s)." % (g["name"], it["label"], s["buff_atk"], s["buff"],
                                                              "s" if s["buff"] > 1 else ""))
        elif eff.startswith("armor"):
            s["armor_up"] = 2
            s["armor_bonus"] = 2 if eff == "armor2x2" else 3
            log.append("%s: %s – protection +%d." % (g["name"], it["label"], s["armor_bonus"]))
        elif eff == "wall":
            s["wall"] = 1
            log.append("%s: %s – your next hit bounces off." % (g["name"], it["label"]))
        elif eff == "dodge":
            s["dodge"] = 1
            log.append("%s: %s – your next hit counts half." % (g["name"], it["label"]))
        elif eff == "rudel":                                 # the alpha howls: the rest of the pack hits harder (Red Trio)
            for x in lebend(ctx["k"]):
                if x is not g:
                    x["states"]["buff"], x["states"]["buff_atk"] = 2, 2
            log.append("%s: %s – the rest of the pack attacks harder (2 rounds)." % (g["name"], it["label"]))
        if not it.get("bonus"):
            return None
    if (sp.get("rauch") or {}).pop("angriff", None):                  # smoke pot: the attack hits only smoke
        log.append("%s: %s – into the smoke, and hits nothing." % (g["name"], it["label"]))
        return None
    k["parade"] = _parade_data(ctx, key, it)
    k["parade"]["gegner"] = k["gegner"].index(g)                        # who strikes (several enemies, 29.10.2026)
    k["phase"] = "parade"
    return "parade"


def _parade_data(ctx, key, it):
    """What the client needs for the reaction test: kind, windows (ms), expected damage without parade."""
    sp, g = ctx["sp"], ctx["g"]
    tempo = TEMPO_OF[g["def"]["tier"]]
    t = TEMPO[tempo]
    heavy = key.startswith("s")
    f = 1 + 0.03 * sp["attrs"].get("perception", 0)
    f *= 0.8 if heavy else 1
    f *= 1.5 if sp["states"].get("guard") else 1
    f *= 0.9 if (sp["armor"] or {}).get("heavy") else 1
    f *= 1.05 if _sig(sp["armor"]) == "fliessend" else 1                   # Meramie: Fließend
    f *= 1 + (sp.get("chips") or {}).get("parade", 0) / 100                # chip: wider parry window
    f *= 0.8 if (sp["states"].get("nass") or sp["states"].get("geblendet")) else 1
    f *= 0.9 if sp.get("main_path") == "M" else 1.1 if sp.get("main_path") == "W" else 1
    f *= 1.3 if g["states"].get("nass") else 1
    f *= H5_PARRY if sp.get("ponente", 0) > 0 else 1                          # Healer H5 Ponente
    f *= 1 + sum(m for m, _ in sp.get("parade_mods") or [])                  # green tea, double espresso
    mode = "ring" if it.get("dodge_only") else g["def"].get("parade", "sprite")
    return {"absicht": key, "label": it["label"], "halb": bool(sp["states"].get("guard")), "modus": mode,
            "tempo": tempo, "schwer": heavy, "sa": is_special(key), "nur_ausweichen": bool(it.get("dodge_only")),
            "ziel": g["def"].get("parade_ziel", 75),                       # gold zone on the parry bar in % (26.10.2026)
            "aufgeladen": bool(sp.get("charged")), "schaden": incoming(sp, g, key), "finte": it.get("finte"),
            "taunt": g["def"].get("taunt") if (it.get("finte") or {}).get("art") == "zoegern" else None,   # spoken / growled while it holds
            "serie": ctx["k"].get("parade_serie", 0),                          # perfect parries in a row (dots by the bar)
            "serie_max": max(1, PARADE_SERIE - (sp.get("chips") or {}).get("parade_serie", 0)),
            "finte_bekannt": bool(it.get("finte")) and (ctx["k"].get("finten_gesehen") or {}).get("%s:%s" % (g.get("typ"), key), 0) > 0,
            "schuss": bool(it.get("schuss") or (key == "n" and g["def"]["attack"].get("schuss"))),   # Muendungsfeuer (Duc 01.11.2026)
            "fenster": {"gut": round(t["gut"] * f), "perf": round(t["perf"] * f), "dauer": t["dauer"],
                        "faktor": round(f, 2)}}


def incoming(sp, g, key):
    """Damage of the enemy's attack against Duc without parade (None if it does not attack)."""
    it = g["intents"].get(key) or {}
    if it.get("art") != "angriff" or (it.get("effect") in HARMLESS and not it.get("bonus")):
        return None
    return _enemy_damage(sp, g, key, it)[0]


def _enemy_damage(sp, g, key, it):
    s, ds = g["states"], sp["states"]
    heavy = key.startswith("s")
    atk = g["atk"] + it.get("bonus", 0) + (HEAVY_BONUS if heavy else 0) + (s.get("buff_atk", 0) if s.get("buff") else 0)
    atk -= WEAK_MALUS if s.get("geschwaecht") else 0
    atk -= REACH if sp["weapon"]["kind"] == "stange" else 0
    arm = sp["armor"] or {}
    standfest = _sig(arm) == "standfest"
    armor = 0 if (ds.get("erschuettert") and not standfest) or it.get("effect") == "pierce" \
        else DUC_ARMOR + arm.get("prot", 0) + (2 if standfest and ds.get("guard") else 0)
    dmg = max(1, round(atk) - armor + (EXPOSED_BONUS if ds.get("ungedeckt") else 0))
    notes = []
    if arm.get("resist") and (arm["resist"] == g["def"].get("element") or (arm["resist"] == "alle" and g["def"].get("element"))):
        dmg = max(1, round(dmg * RESIST))
        notes.append("resistance")
    if it.get("effect") == "scent" and ds.get("blutend"):
        dmg += 5
    if arm.get("bite") and g["def"]["cls"] in ("tier", "monster"):
        dmg = max(1, round(dmg * (1 - arm["bite"])))
    if g.get("wucht", 1) != 1:                                             # pack member (Mehrgegner, 29.10.2026)
        dmg = max(1, round(dmg * g["wucht"]))
    if s.get("geblendet") or sp.get("halve_next"):
        dmg = max(1, dmg // 2)
        notes.append("geblendet" if s.get("geblendet") else "abgetaucht")
    if ds.get("guard") or sp.get("wind", 0) > 0:
        dmg = max(1, dmg // 2)
        notes.append("guard" if ds.get("guard") else "Libeccio")
    if sp.get("bonaccia") == "voll":
        dmg = 0
        notes.append("Bonaccia")
    elif sp.get("bonaccia") == "halb":
        dmg = max(1, dmg // 2)
        notes.append("Bonaccia")
    return dmg, notes


def parade_aufloesen(z, modul, ergebnis, revision=None, probe_fn=None, rng=None):
    """Result of the reaction test -> the enemy's hit, counters, states, end of round.
    perfekt: no damage, +1 stamina, counter (proc), enemy exhausted; 3 perfect in a row: Fassung -4
    gut / ausweichen: damage halved (min. 1) · verfehlt: full damage. A charged M5 replaces the normal counter."""
    k0 = z.get("kampf")
    if not k0 or k0.get("ergebnis") or k0.get("phase") != "parade":
        raise ValueError("No blow is coming right now.")
    if revision is not None and revision != k0["revision"]:
        raise ValueError("That parry has already been counted (the screen was out of date).")
    if ergebnis not in PARADE_ERGEBNISSE:
        raise ValueError("Unknown parry result.")
    p = k0["parade"]
    if ergebnis == "ausweichen" and p["modus"] != "ring":
        raise ValueError("You can't dodge this enemy.")
    if p.get("nur_ausweichen") and ergebnis in ("perfekt", "gut"):
        raise ValueError("You can't parry this blow, only dodge it.")
    k = copy.deepcopy(k0)
    ctx = _ctx(k, rng, probe_fn)
    p = k["parade"]
    ctx["g"] = k["gegner"][p.get("gegner", 0)]                       # the one who strikes takes the counter
    sp, g, log = ctx["sp"], ctx["g"], ctx["log"]
    key = p["absicht"]
    it = g["intents"][key]
    heavy = key.startswith("s")
    s, ds = g["states"], sp["states"]
    dmg, notes = _enemy_damage(sp, g, key, it)
    sp["halve_next"] = False
    if s.get("geschwaecht"):                                  # counts attacks: Intimidate weakens two (Duc 29.10.2026)
        s["geschwaecht"] -= 1
        if s["geschwaecht"] <= 0:
            s.pop("geschwaecht")
    bon = sp.pop("bonaccia", None)
    charged = sp.pop("charged", False)
    if bon and sp["attrs"].get("perception", 0) >= W_FULL_FROM:
        log.append("Bonaccia: counter.")
        _hit(ctx, 1.0 if bon == "voll" else 0.5)
    made = ergebnis in ("perfekt", "gut", "ausweichen")
    if it.get("finte"):                                     # from the second time on the bar marks the feint (Duc 03.11.2026)
        fk = "%s:%s" % (g.get("typ"), key)
        gesehen = z.setdefault("finten_gesehen", {})
        gesehen[fk] = gesehen.get(fk, 0) + 1
        k["finten_gesehen"] = dict(gesehen)
    if ergebnis in ("perfekt", "gut") and bestiarium_merken(z, g):      # first parry of this kind: its rhythm goes into the Codex
        _event(ctx, "bestiarium", name=g["def"]["name"])
    if ergebnis == "perfekt":
        dmg = 0
        sp["ausdauer"] = min(sp["ausdauer_max"], sp["ausdauer"] + 1)
        log.append("%s: %s – perfect parry! +1 stamina." % (g["name"], it["label"]))
        k["parade_serie"] = k.get("parade_serie", 0) + 1
        st = k.setdefault("stat", {})                       # training tasks: longest run of perfect parries
        st["serie"] = st.get("serie", 0) + 1
        st["serie_max"] = max(st.get("serie_max", 0), st["serie"])
        if not it.get("dodge_only") and not charged:
            log.append("Counter:")
            if _sig(sp["armor"]) == "fliessend":
                _event(ctx, "jacke", sig="fliessend")
            c = _hit(ctx, (1.1 if _sig(sp["armor"]) == "fliessend" else 1.0) * (sp.get("chips") or {}).get("konter", 1.0), proc=True)
            if sp["weapon"].get("sig") == "twin":                # Gemelli: the second barrel fires on every counter
                log.append("Second barrel:")
                _hit(ctx, proc=True)
            if sp["weapon"].get("sig") == "counter15" and c:
                bonus = int(c * 1.5) - c
                g["lp"] = max(0, g["lp"] - bonus)
                log.append("Holm's sabre: +%d." % bonus)
            s["erschoepft"] = max(s.get("erschoepft", 0), 2)
            log.append("%s is exhausted." % g["name"])
            if sp.get("wind", 0) > 0:
                _apply_state(ctx, "erschuettert", 2)
                log.append("Libeccio: %s is shaken." % g["name"])
        serie = max(1, PARADE_SERIE - (sp.get("chips") or {}).get("parade_serie", 0))   # Casanova's charm: 2 instead of 3
        if k["parade_serie"] >= serie:
            g["fassung"] = max(0, g["fassung"] - SERIE_FASSUNG)
            k["parade_serie"] = 0
            log.append("%d perfect parries in a row: composure −%d." % (serie, SERIE_FASSUNG))
        eff_rounds = 0
    else:
        k["parade_serie"] = 0
        k.setdefault("stat", {})["serie"] = 0
        if made and dmg > 0:
            dmg = max(1, dmg // 2)
        notes += ["parried"] if ergebnis == "gut" else ["dodged"] if ergebnis == "ausweichen" else []
        if ds.get("ungedeckt"):
            notes.append("exposed")
        log.append("%s: %s – %d damage%s." % (g["name"], it["label"], dmg, " (%s)" % ", ".join(notes) if notes else ""))
        eff_rounds = 1 if made else 2 + it.get("linger", 0)   # linger: a full hit lasts longer (water grenade, 28.10.)
    if _sig(sp["armor"]) == "alles" and dmg > 0 and not sp.get("erster_treffer"):
        sp["erster_treffer"] = True                                       # Citadelle: the first hit per fight counts half
        dmg = max(1, dmg // 2)
        log.append("Citadelle: the first hit only counts half.")
        _event(ctx, "jacke", sig="alles")
    ds.pop("ungedeckt", None)
    sp["lp"] = max(0, sp["lp"] - dmg)
    if sp.get("main_path") == "M" and dmg > 0:
        sp["ausdauer"] = min(sp["ausdauer_max"], sp["ausdauer"] + 1)
    _event(ctx, "treffer_duc", schaden=dmg)
    if charged:                                         # M5 Retour de Flamme: the charged counter
        f = (M5_MULT[1] if heavy else M5_MULT[0]) if made else M5_MULT[2]
        log.append("%s – counter ×%s:" % ("Parry the Dirt" if charged == "dreck" else "Retour de Flamme", str(f).replace(".", ",")))
        _event(ctx, "spezial", id="parry_the_dirt" if charged == "dreck" else "retour", phase="konter")
        _hit(ctx, f)
        if made:
            if charged != "dreck":
                _apply_state(ctx, "brennend")
            if ergebnis == "perfekt":
                s["erschoepft"] = max(s.get("erschoepft", 0), 2)
    if it.get("effect") == "drain" and dmg:
        g["lp"] = min(g["lp_max"], g["lp"] + dmg)
        log.append("%s drains %d HP." % (g["name"], dmg))
    if eff_rounds and it.get("effect"):
        _duc_state(ctx, it["effect"], eff_rounds)
    if heavy:
        s["erschoepft"] = max(s.get("erschoepft", 0), 2)
        log.append("%s is exhausted after the blow." % g["name"])
    k["parade"] = None
    k["phase"] = "spieler_wahl"
    k["letzte_parade"] = ergebnis
    for x in lebend(k):                                    # Tierstation: Der Konter passiert von selbst, darum verjagt er ein taumelndes Tier nicht
        if x["def"].get("schlafbar") and x.get("taumelt"):
            x["lp"] = max(1, x["lp"])
    ende = _ausscheiden(ctx)
    if not ende and sp["lp"] <= 0 and not _arcangelo(ctx):
        ende = "niederlage"
    elif not ende:
        ende = _gegner_runde(ctx)                                   # the others still to act this round, then its end
    if ende in ("ko", "aufgabe") and (ergebnis == "perfekt" or (charged and made)):
        k.setdefault("stat", {})["sieg_konter"] = True              # training task: the counter decided the fight
    _spruch(ctx, ende)
    k["revision"] += 1
    k["events"] = ctx["events"]
    k["log"] = (k["log"] + [{"runde": k["runde"] - (0 if ende else 1), "befehl": "parade", "ziel": ergebnis,
                             "zeilen": log}])[-LOG_MAX:]
    z["kampf"] = k
    if ende:
        _finish(z, modul, k, ende)
    z["lp"] = k["spieler"]["lp"]
    return k


def _duc_state(ctx, effect, rounds):
    sp, g, log = ctx["sp"], ctx["g"], ctx["log"]
    ds = sp["states"]
    immune = _resist_state(sp["armor"])
    base = "brennend" if effect.startswith("brennend") else "geblendet" if effect.startswith("geblendet") else effect
    if base == "erschuettert" and _sig(sp["armor"]) == "standfest":
        _event(ctx, "jacke", sig="standfest")
    if base == immune or (base == "erschuettert" and _sig(sp["armor"]) == "standfest"):
        log.append("Your %s protects you." % sp["armor"]["label"])
        return
    if (sp.get("immun") or {}).get(base):                                    # cooling spray
        log.append("The cooling spray protects you.")
        return
    abw = (sp.get("chips") or {}).get("abwehr", {}).get(base)               # chip: defence against this state
    if abw == "immun":
        log.append("Your chip protects you from %s." % STATE_LABEL.get(base, base))
        return
    if abw in ("kuerzer", "halb") and base not in ("brennend", "blutend"):
        rounds = max(1, rounds - 1) if abw == "kuerzer" else max(1, (rounds + 1) // 2)
    if base == "brennend":
        n = _burn_add(ds, 2 if effect == "brennend3" else 1)
        if abw == "kuerzer" and n > 1:
            ds["brennend"] -= 1
            n -= 1
        log.append("You're burning (🔥×%d)." % n)
    elif base in ("strom", "nass") and ds.get("nass" if base == "strom" else "strom"):
        ds.pop("nass", None)                                  # short circuit on Duc (agents at the ridge, 28.10.2026)
        ds.pop("strom", None)
        ds["betaeubt"] = 1
        dmg = int(SHORT_CIRCUIT * sp["lp_max"])
        sp["lp"] = max(0, sp["lp"] - dmg)
        _reaction(ctx, "Short Circuit", "You take %d damage and lose your next turn." % dmg)
        base = "betaeubt"
    elif effect in ("nass", "blutend", "erschuettert", "strom", "geblendet", "geblendet2"):
        ds[base] = max(ds.get(base, 0), rounds)
        if base == "nass" and ds.get("brennend"):
            ds.pop("brennend", None)
            ds.pop("burn_new", None)
            log.append("The water puts out the flames on you.")
        log.append("You're %s." % STATE_LABEL[base])
    elif effect in ("ungedeckt", "betaeubt", "geschwaecht"):
        ds[effect] = 1
        log.append("You're %s." % STATE_LABEL[effect])
    elif effect == "silence":
        ds["silence"] = 2
        log.append("You're silenced: no skills for 2 rounds.")
    elif effect == "stamina":
        sp["ausdauer"] = max(0, sp["ausdauer"] - 1)
        log.append("The wind is knocked out of you: −1 stamina.")
    else:
        return
    _event(ctx, "zustand_duc", id=base)


def _beistand(ctx):
    """Friends act at the end of the round (Red Trio, station 7): no units of their own, one action per round in turn.
    Action: {"wer", "text", "anteil": share of max HP, "state": state on the target, "schutz": Duc's next hit taken is halved}."""
    k = ctx["k"]
    aktionen = k["def"].get("beistand")
    a = aktionen[(k["runde"] - 1) % len(aktionen)] if aktionen else None
    if not a:
        return
    if a.get("schutz"):
        ctx["sp"]["halve_next"] = True
        _reaction(ctx, a["wer"], a["text"])
        return
    g = ctx["g"] = ziel_gegner(k)
    _reaction(ctx, a["wer"], a["text"] % {"ziel": g["name"]})
    if a.get("anteil"):
        dmg = max(1, int(a["anteil"] * g["lp_max"]))
        g["lp"] = max(0, g["lp"] - dmg)
        ctx["log"].append("%d damage." % dmg)
        _event(ctx, "treffer", schaden=dmg, krit=False, wirkung=None, tags=[])
    if a.get("state"):
        _apply_state(ctx, a["state"])


def _end_of_round(ctx):
    """Burn, bleed and timers on both sides. -> end or None (then the next round starts)."""
    k, sp, log = ctx["k"], ctx["sp"], ctx["log"]
    ds = sp["states"]
    if sp.get("wind", 0) > 0:
        sp["wind"] -= 1
    _gegenstand_runde(ctx)
    _beistand(ctx)
    if sp.get("ponente", 0) > 0 and sp["lp"] > 0:          # Healer H5: mild west wind
        sp["ponente"] -= 1
        plus = min(sp["lp_max"] - sp["lp"], int(round(sp["lp_max"] * H5_HEAL)))
        if plus:
            sp["lp"] += plus
            log.append("Ponente: you heal %d HP." % plus)
    for g in lebend(k):                                   # every enemy still standing burns, bleeds, counts down
        s = g["states"]
        if s.get("brennend"):
            n = s["brennend"]
            dmg = int(BURN_PER_STACK * g["lp_max"] * n * (BOSS_BURN if g["def"].get("boss") else 1))
            g["lp"] = max(0, g["lp"] - dmg)
            log.append("Fire: %s loses %d HP (🔥×%d)." % (g["name"], dmg, n))
            if not s.pop("burn_new", None):
                s["brennend"] -= 1
                if s["brennend"] <= 0:
                    s.pop("brennend")
        if s.get("blutend"):
            dmg = int(BLEED * g["lp_max"])
            g["lp"] = max(0, g["lp"] - dmg)
            log.append("Bleeding: %s loses %d HP." % (g["name"], dmg))
        if g["def"].get("schlafbar"):                     # Tierstation: Nur ein Schlag von Duc verjagt das Tier, Feuer und Blutung nehmen ihm nicht das Fenster fuer die Granate
            g["lp"] = max(1, g["lp"])
        for x in ("blutend", "nass", "strom", "erschuettert", "geblendet", "schlamm", "armor_up", "buff", "erschoepft"):
            if s.get(x):
                s[x] -= 1
                if s[x] <= 0:
                    s.pop(x)
                    if x == "buff":
                        s.pop("buff_atk", None)
                    if x == "armor_up":
                        s.pop("armor_bonus", None)
    if ds.get("brennend"):
        n = ds["brennend"]
        dmg = int(BURN_PER_STACK * sp["lp_max"] * n)
        if (sp.get("chips") or {}).get("abwehr", {}).get("brennend") == "halb":
            dmg = max(1, dmg // 2)
        sp["lp"] = max(0, sp["lp"] - dmg)
        log.append("Fire: you lose %d HP (🔥×%d)." % (dmg, n))
        if not ds.pop("burn_new", None):
            ds["brennend"] -= 1
            if ds["brennend"] <= 0:
                ds.pop("brennend")
    if ds.get("blutend"):
        dmg = int(BLEED * sp["lp_max"])
        if (sp.get("chips") or {}).get("abwehr", {}).get("blutend") == "halb":
            dmg = max(1, dmg // 2)
        sp["lp"] = max(0, sp["lp"] - dmg)
        log.append("Bleeding: you lose %d HP." % dmg)
    ds.pop("guard", None)
    for x in ("nass", "blutend", "erschuettert", "strom", "geblendet", "silence"):
        if ds.get(x):
            ds[x] -= 1
            if ds[x] <= 0:
                ds.pop(x)
    for g in lebend(k):                                   # fire and bleeding can finish them
        if g["lp"] <= 0:
            g["aus"] = "ko"
            if len(k["gegner"]) > 1:
                log.append("%s goes down." % g["name"])
                _event(ctx, "aus", gegner=g["instanz"], wie="ko")
    if not lebend(k):
        return _sieg_art(k)
    if sp["lp"] <= 0 and not _arcangelo(ctx):
        return "niederlage"
    k["runde"] += 1
    for g in lebend(k):
        if len(lebend(k)) == 1 and g["def"].get("pattern_allein"):            # the partner is down: no combo left
            g["pattern"] = g["def"]["pattern_allein"]
        g["absicht"] = _next_intent(g)
    ctx["g"] = ziel_gegner(k)
    return None


def geld_drop(z, k, g, i=0):
    """Money a beaten enemy leaves behind: only classes in kaempfe.json geld_drop (people), amount by tier, fixed per fight."""
    cfg = k.get("geld_cfg") or {}
    span = (cfg.get("spanne") or {}).get(g["def"].get("tier"))
    if k["def"].get("training") or not span or g["def"].get("cls") not in (cfg.get("klassen") or []):
        return 0
    salz = "%s-%s-%s-%s-geld" % (z.get("id"), z.get("tag"), z.get("phase"), k.get("definition"))   # reproducible (gate)
    salz += "-%d" % i if i else ""                                       # every member of a group has its own wallet
    return random.Random(salz).randint(span[0], span[1])


def _finish(z, modul, k, art):
    if k.get("held") and "held_tasche" not in k:       # Beute gehoert in Ducs Tasche, Maxwells Rest bleibt fuer den naechsten Kampf
        k["held_tasche"] = list(z.get("inventar", []))
        z["inventar"] = list(k["lager"]["inventar"])
    """Exactly one outcome, consequences exactly once; xp for a win, training costs no LP."""
    a = k["def"]["outcomes"].get(art) or {}
    sp = k["spieler"]
    # who counts for xp, stones and money: everyone beaten or talked down (several enemies, 29.10.2026)
    besiegt = [x for x in k["gegner"] if x.get("aus") in ("ko", "aufgabe")] or [ziel_gegner(k)]
    wieder_auf = None
    if art == "niederlage" and not k.get("held"):                            # the end card shows 0 and then the comeback
        wieder_auf = max(sp["lp"], LP_AFTER_DEFEAT)
        sp["lp"] = wieder_auf
    if k.get("aufgabe") and not k["folgen_angewendet"]:          # Maxwell's task of the day sets the xp (Duc 02.11.2026)
        from . import tutorial
        k["def"]["xp_factor"] = tutorial.aufgabe_werten(k, art)
    if k["def"].get("training"):
        sp["lp"] = max(sp["lp"], k.get("lp_start", sp["lp"]))
    lines, xp, lv0 = [], 0, progress(z)["level"]
    nochmal = art == "niederlage" and nochmal_moeglich(k)
    if not k["folgen_angewendet"] and not nochmal:          # Try again (Duc 03.11.2026): consequences wait for the choice
        lines = zustand.folgen_anwenden(z, modul, a.get("folgen", []))
        k["folgen_angewendet"] = True
        if art in ("ko", "aufgabe"):
            xp = sum(xp_for(g["level"], sp["level"], k["def"].get("xp_factor", 1.0) * g["def"].get("xp_faktor", 1)
                            * g.get("xp_anteil", 1)) for g in besiegt)
            z["lp"] = sp["lp"]
            lines += award_xp(z, xp)
            sp["lp"] = z["lp"]
            for i, g in enumerate(besiegt):
                drop = g["def"].get("drop") or (ELEMENT_DROP.get(g["def"].get("element")) if g["def"].get("tier") in ("toedlich", "albtraum") else None)
                if drop and not k["def"].get("training") and drop in modul["items"]:      # strong enemies drop their element's end stone
                    lines += zustand.folgen_anwenden(z, modul, [{"item": drop, "beute": True}])
                geld = geld_drop(z, k, g, i)
                if geld:                                                           # people carry money (28.10.2026)
                    lines += zustand.folgen_anwenden(z, modul, [{"geld": geld, "text": "%s's wallet" % g["name"]}])
                    k["geld_drop"] = k.get("geld_drop", 0) + geld
            stahl = (kuechen.daten(modul) or {}).get("stahl_kampf")
            if stahl and not k["def"].get("training") and z.get("tag", 0) >= stahl["ab_tag"]:
                n_stahl = stahl["n"] * sum(1 for g in besiegt if g["def"].get("cls") == stahl["klasse"])
                if n_stahl:                                                    # Akt 3 (Duc 30.10.2026): Stahl steckt in den Maschinen
                    kuechen.rohstoff_add(z, "steel", n_stahl)
                    lines.append("You pull %d Steel out of the wreck." % n_stahl)
            leder = (kuechen.daten(modul) or {}).get("leder_kampf")
            if leder and not k["def"].get("training"):
                n_leder = leder["n"] * sum(1 for g in besiegt if g["def"].get("name") in leder["gegner"])
                if n_leder:                                                    # Danzels Auftraege (Duc 30.10.2026)
                    kuechen.rohstoff_add(z, "leather", n_leder)
                    lines.append("You take %d Boar Leather." % n_leder)
    heil = (sp.get("chips") or {}).get("heil_kampf", 0)
    if heil and art in ("ko", "aufgabe") and sp["lp"] > 0:                  # chip: heal after a won fight
        sp["lp"] = min(sp["lp_max"], sp["lp"] + heil)
        lines.append("Your chip heals you for %d HP." % heil)
    k["phase"] = "ende"
    c = progress(z)
    k["ergebnis"] = {"art": art, "text": a.get("text", ""), "zeilen": lines, "xp": xp, "level": c["level"], "nochmal": nochmal,
                     "skillpunkte": free_points(z), "wieder_auf": wieder_auf,
                     "aufstieg": {"von": lv0, "auf": c["level"], "lp": LP_PER_LEVEL * (c["level"] - lv0),
                                  "ausdauer": max_stamina(c["level"]) - max_stamina(lv0)} if c["level"] > lv0 else None}


# Try again (Duc 03.11.2026): after a defeat Duc may fight the same fight once more, under the same conditions (HP and bag as
# at the start, enemies unchanged). A second defeat, or "Accept the defeat", brings the usual consequences (back to the yacht,
# a lost phase, on an expedition the loot). Not for Maxwell's training, the harbour waves (they restart anyway), the siege
# (its own retry) or Maxwell as a fighter.
def nochmal_moeglich(k):
    d = k.get("def") or {}
    return not (k.get("nochmal_genutzt") or k.get("held") or d.get("training") or d.get("neustart_bei_niederlage")
                or (k.get("rueckkehr") or {}).get("status") == "taktik")


def nochmal(z, defs):
    """Start the same fight again: HP and bag as at the start, marked so it can't be repeated a second time."""
    k = z.get("kampf") or {}
    if not (k.get("ergebnis") or {}).get("nochmal"):
        raise ValueError("There is no second try here.")
    z["lp"] = k.get("lp_start", z.get("lp"))
    z["inventar"] = list(k.get("inventar_start", z.get("inventar", [])))
    starten(z, defs, k["definition"], rueckkehr=k.get("rueckkehr"))
    z["kampf"]["nochmal_genutzt"] = True
    return z["kampf"]


def niederlage_annehmen(z, modul):
    """Duc gives up the second try: now the defeat's consequences apply, exactly once. -> new lines"""
    k = z.get("kampf") or {}
    e = k.get("ergebnis") or {}
    if not e.get("nochmal"):
        return []
    e["nochmal"] = False
    k["nochmal_genutzt"] = True
    lines = []
    if not k["folgen_angewendet"]:
        lines = zustand.folgen_anwenden(z, modul, ((k["def"]["outcomes"].get("niederlage") or {}).get("folgen") or []))
        k["folgen_angewendet"] = True
    e["zeilen"] = list(e.get("zeilen") or []) + lines
    return lines


def schliessen(z):
    """Result seen -> fight gone. Returns the return reference for eden.py."""
    k = z.get("kampf")
    if not k or not k.get("ergebnis"):
        raise ValueError("The fight isn't over yet.")
    if k.get("held"):                                  # Maxwell: Ducs LP zurueck, Maxwells Stand geht an die Taktik-Karte
        sp = k["spieler"]
        z["held_zurueck"] = {"id": k["held"]["id"], "lp_anteil": sp["lp"] / max(1, sp["lp_max"]), "tasche": k.get("held_tasche", []),
                             "gegner_anteil": k["gegner"][0]["lp"] / max(1, k["gegner"][0]["lp_max"])}
        z["lp"] = k["lager"]["lp"] + LP_PER_LEVEL * (progress(z)["level"] - k["lager"]["level"])
    z["kampf"] = None
    return k.get("rueckkehr")


# ------------------------------------------------------------------ view
def befehle(z, modul):
    """Main menu with reasons (UI and console)."""
    k = z["kampf"]
    if must_skip(k["spieler"]):
        return [{"id": "aussetzen", "label": BEFEHL_LABEL["aussetzen"], "gesperrt": None}]
    out = []
    for b in BEFEHLE:
        if b == "faehigkeit":
            fs = skills_view(z, k)
            grund = None if any(not f["gesperrt"] for f in fs) else "No skill is possible right now."
        elif b == "gegenstand":
            gs = gegenstaende(z, modul)
            grund = "Nothing useful in your inventory." if not gs else (None if any(not x["gesperrt"] for x in gs)
                                                                   else gs[0]["gesperrt"])
        else:
            grund = pruefen(z, modul, b)
        out.append({"id": b, "label": BEFEHL_LABEL[b], "gesperrt": grund})
    return out


def faehigkeiten(z):
    return skills_view(z, z["kampf"])


ATTRIBUTE = tuple(ATTR_LABEL)
# Ducs Schlag als Bildfolge (Duc 03.11.2026, werkzeuge/kampf_schwung.py): sechs Bilder vom Ausholen bis zum Durchschwung,
# der Client spielt sie bei "Attack" und beim Konter. Fehlen sie (Gemelli), bleibt es bei der einen Pose.
SCHWUNG = tuple("schwung_%s" % c for c in "abcdef")
POSEN = ("idle", "windup", "attack", "heavy_windup", "heavy_attack", "hurt", "guard", "weakened", "enraged", "flee",
         "surrender", "defeated", "victory")


def chips(states, rounds_hint=True):
    """States as display chips: [{id, label, wert}] (wert = rounds or burn stacks)."""
    out = []
    for x, v in states.items():
        if x in ("burn_new", "buff_atk", "armor_bonus") or not v:
            continue
        out.append({"id": x, "label": STATE_LABEL.get(x, x), "wert": v if isinstance(v, int) and v is not True else 1})
    return out


def antwort(g, it):
    """The right answer to an intent, for the sign above the enemy: parieren / ausweichen / keine (no blow) / flucht."""
    if it.get("art") == "flucht":
        return "flucht"
    if it.get("effect") in HARMLESS and not it.get("bonus"):
        return "keine"
    return "ausweichen" if it.get("dodge_only") else "parieren"


def intent_view(sp, g, key):
    it = g["intents"][key]
    return {"id": key, "icon": it.get("icon", ""), "label": it["label"], "sa": is_special(key),
            "antwort": antwort(g, it), "auch_ausweichen": g["def"].get("parade") == "ring" and not it.get("dodge_only"),
            "finte": bool(it.get("finte")),
            "stark": key.startswith("s"), "tut_weh": hurts(it) if is_special(key) else None,
            "nur_ausweichen": bool(it.get("dodge_only")), "flucht": it.get("art") == "flucht",
            "schaden": incoming(sp, g, key), "wirkung": it.get("effect")}


def zugfolge(k, n=3):
    """Coming enemy intents for the turn order display. One enemy: its next n intents (fixed pattern). Several
    (29.10.2026): this round's order - every enemy still standing with its intent ("wer", "instanz")."""
    sp = k["spieler"]
    if len(k["gegner"]) == 1:
        g = k["gegner"][0]
        out = []
        for i in range(n):
            key = g["absicht"] if i == 0 else g["pattern"][(g["schritt"] + i) % len(g["pattern"])]
            out.append(intent_view(sp, g, key))
        return out
    return [dict(intent_view(sp, g, g["absicht"]), wer=g["name"], instanz=g["instanz"]) for g in lebend(k) if g["absicht"]]


def _gegner_ansicht(k, g, bild):
    sp = k["spieler"]
    a = intent_view(sp, g, g["absicht"]) if g["absicht"] and not g.get("aus") else {}
    wk = g["def"].get("weakness")
    attribute = [{"id": att, "status": "schwach" if g["schwaeche_bekannt"] and att == wk
                  else "getestet" if att in k.get("getestet", []) else "unbekannt"} for att in ATTRIBUTE]
    sprite = g["def"].get("sprite")
    bilder = {p: bild(sprite, p) for p in POSEN + ("avatar",)} if bild and sprite else {}
    absicht_text = a.get("label", "") + (" (%d)" % a["schaden"] if a.get("schaden") is not None else "")
    return {"instanz": g["instanz"], "name": g["name"], "lp": g["lp"], "lp_max": g["lp_max"],
            "fassung": g["fassung"], "fassung_max": g["fassung_max"], "offen": exhausted(g),
            "erschoepft": exhausted(g), "finte": False, "geschwaecht": bool(g["states"].get("geschwaecht")),
            "level": g["level"], "bedrohung": g["bedrohung"], "klasse": g["def"]["cls"],
            "element": g["def"].get("element"), "zustaende": chips(g["states"]),
            "brand": g["states"].get("brennend", 0),
            "schwaeche": wk if g["schwaeche_bekannt"] else None, "attribute": attribute,
            "bilder": bilder, "parade_art": g["def"].get("parade", "sprite"), "aus": g.get("aus"),
            "absicht": dict(a, text=absicht_text, danach="offen" if a.get("stark") else None)}


def ansicht(z, modul, bild=None):
    """Everything for the combat screen. bild(sprite, pose) -> URL (eden.py knows the route), else no images.
    "gegner" lists every enemy (with "aus" once it left), "zielgegner" is the index Duc aims at (29.10.2026)."""
    k = z.get("kampf")
    if not k:
        return None
    sp, r = k["spieler"], k["runde"]
    g = ziel_gegner(k)
    laufend = not k["ergebnis"]
    duc_sprite = (k.get("held") or {}).get("sprite") or duc_sprite_name((sp.get("armor") or {}).get("id"), (sp.get("weapon") or {}).get("id"))
    duc_bilder = {p: bild(duc_sprite, p) for p in POSEN + ("konter",) + SCHWUNG} if bild and duc_sprite else {}   # konter: Duc 01.11.2026, nur Duc
    wahl = laufend and k.get("phase") != "parade"
    c = progress(z)
    spieler = dict(sp, offen=bool(sp["states"].get("ungedeckt")), angriff=hit_preview(sp, g),
                   krit=round(100 * crit_chance(sp)), zustaende=chips(sp["states"]),
                   xp=c["xp"], xp_next=xp_needed(c["level"]), skillpunkte=free_points(z),
                   hauptpfad=PATH_NAME.get(sp.get("main_path")), muss_aussetzen=must_skip(sp))
    return {"id": k["id"], "titel": k["def"].get("title"), "ziel": k["def"].get("goal"), "runde": r,
            "revision": k["revision"], "phase": k.get("phase"), "parade": k.get("parade"),
            "letzte_parade": k.get("letzte_parade"), "parade_serie": k.get("parade_serie", 0), "spieler": spieler,
            "duc_bilder": duc_bilder, "held": k.get("held"), "muendung": k.get("muendung") or {},
            "gegner": [_gegner_ansicht(k, x, bild) for x in k["gegner"]], "zielgegner": k["gegner"].index(g),
            "zugfolge": zugfolge(k) if laufend else [],
            "befehle": befehle(z, modul) if wahl else [],
            "faehigkeiten": skills_view(z, k) if wahl else [],
            "gegenstaende": gegenstaende(z, modul) if wahl else [],
            "events": k.get("events", []),
            "log": k["log"][-6:], "ergebnis": k["ergebnis"], "vorschau_hinweis": k.get("vorschau_hinweis")}
