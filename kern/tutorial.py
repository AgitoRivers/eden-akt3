# -*- coding: utf-8 -*-
"""Kampf-Tutorial mit Maxwell (24.10.2026, Duc: "Maxwell erklaert dir im Kampf, wie die Mechanik funktioniert").

Drei kurze Lektionen statt einer langen - je Schritt genau ein Begriff, ausgeloest vom echten Kampfgeschehen
(Hades/Persona: zeigen, wenn es passiert, nicht vorher alles erklaeren):
  Lektion 1  Tag 2, erster Kampf (Begegnung maxwell_tutorial): Angriff -> Absicht -> Parade -> Ausdauer ->
             Schwaeche (Koepfchen, seit 29.10.2026 statt Schwachstelle) -> Fassung und Reden -> Verteidigen/Heilen
  Lektion 2  zweites Training: Mistral (K3, bringt Maxwell am Ende von Lektion 1 bei - LEHRT), kritische Treffer
             (List), geschwaecht und Immunitaet, ungedeckt. Seit 26.10.2026 gibt es keinen Heftigen Angriff mehr.
  Lektion 3  drittes Training: die Elemente im Kreis, Brennen, Reaktionen - Maxwell erklaert, Erklaerbilder folgen
Jeder Schritt: "en" = Maxwells gesprochener Satz (englisch, vorab vertont, Schluessel tut.<id>), "de" = Bedienhinweis
(seit 25.10.2026 englisch, der Schluesselname blieb), "bild" = Erklaerbild (Pose/Grafik, folgt spaeter; bis dahin zeigt der Client Maxwells Avatar).
Fortschritt in z["tutorial"] = {"lektion": n, "gesehen": [...], "aktuell": id}. Regeln bleiben in kern/kampf.py."""

LEKTIONEN = {
    1: [
        {"id": "l1_angriff", "wann": "start",
         "en": "Welcome to the Maximum gym, brother! Today you fight with this – the mop. Don't laugh, the mop is a "
               "teacher. Rule one: hit me. Mr. Maximum can take it!",
         "de": "Maxwell tosses you a wooden deck mop – training gear, no element. Choose “Attack”. Every attack also "
               "gives you 1 stamina ⚡.",
         "bild": "maxwell_zeigt"},
        {"id": "l1_absicht", "wann": "parade",
         "en": "Now Mr. Maximum strikes back! See my speech bubble? It always tells you what I'll do next. No "
               "surprises, brother.",
         "de": "The speech bubble above your opponent shows their next move.", "bild": "maxwell_blase"},
        {"id": "l1_parade", "wann": "parade",
         "en": "When I wind up, watch for the golden spark and press SPACE right then. Perfect timing means no "
               "damage, and you hit back!",
         "de": "Parry: press SPACE at the golden spark. Perfect = no damage + counter, good = half damage.",
         "bild": "maxwell_ausholen"},
        {"id": "l1_ausdauer", "wann": "runde2",
         "en": "Feel that? Every hit and every parry fills your stamina, and skills cost stamina. Save it up, brother, "
               "and spend it when it counts.",
         "de": "Stamina ⚡ fills up with attacks and parries. Skills and special attacks cost ⚡.",
         "bild": "maxwell_ausdauer"},
        # 29.10.2026: Spot Weakness is gone - the strength Koepfchen shows the weakness from the first round
        {"id": "l1_schwaeche", "wann": "schwaeche",
         "en": "See the gold on my card, brother? That's my weakness. A sharp head like yours spots it straight away. "
               "Mine is charm. Mr. Maximum is soft inside.",
         "de": "Your sharp head shows the opponent's weakness in gold from the first round. Skills on it work "
               "especially well.",
         "bild": "maxwell_erschoepft"},
        {"id": "l1_fassung", "wann": "runde3",
         "en": "Two ways to win, brother. Knock me down, or talk me down. Every fighter has composure. Empty it with "
               "Talk, and they give up.",
         "de": "Two ways to win: HP to 0 or Composure 🛡 to 0. “Talk” lowers composure (humans only).",
         "bild": "maxwell_fassung"},
        {"id": "l1_heilen", "wann": "angeschlagen",
         "en": "Hurt? Defend halves the next hit and gives you stamina. A first-aid kit heals you. And Mr. Maximum "
               "patches you up after every fight.",
         "de": "Defend halves the next hit (+2 ⚡). Items heal. Every new phase restores your HP.",
         "bild": "maxwell_verteidigen"},
        {"id": "l1_ende", "wann": "ende",
         "en": "Mr. Maximum is PROUD of you! Before you go, one real technique. Mistral. Plant your feet and put "
               "the whole storm behind it. Practise it, brother, and come up to the sun deck any time.",
         "de": "You learned Mistral (special attack, no skill point needed). Training with Maxwell: any time during "
               "free time on the sun deck, costs 1 action. The first round each day comes with a task.", "bild": "maxwell_pose"},
    ],
    2: [
        {"id": "l2_mistral", "wann": "start",
         "en": "Lesson two! Show me Mistral, brother. It costs three stamina, so save up first. It hits harder, and "
               "after it they're shaken. No guard for two rounds. Boom!",
         "de": "“Mistral” (Skill): 3 ⚡, +4 damage, the opponent is shaken for 2 rounds (protection 0).",
         "bild": "maxwell_heftig"},
        {"id": "l2_krit", "wann": "runde2",
         "en": "Sometimes a hit lands perfectly – a critical, one and a half times the damage! Cunning makes that "
               "happen more often.",
         "de": "Critical hits: 5 % + 3 % per point of Cunning, damage ×1.5.", "bild": "maxwell_krit"},
        {"id": "l2_angst", "wann": "runde3",
         "en": "Intimidate weakens a fighter's next two blows. But Mr. Maximum? Mr. Maximum fears nothing! Some enemies "
               "are immune, and the game tells you why.",
         "de": "“Intimidate”: opponent weakened for their next two attacks (−3 each). Immune opponents are locked, with "
               "a reason.",
         "bild": "maxwell_lacht"},
        {"id": "l2_ungedeckt", "wann": "runde4",
         "en": "Careful with the fancy moves, brother. Fumble a roll and you're open, so my next hit lands harder. "
               "Brave is good. Reckless hurts.",
         "de": "Exposed: after a fumble, the next blow against you hits +3.", "bild": "maxwell_warnt"},
    ],
    3: [
        {"id": "l3_elemente", "wann": "start",
         "en": "Final lesson, brother: the elements. Water beats fire, fire beats earth, earth beats air, and air "
               "beats water. Remember the circle!",
         "de": "Elements in a circle: water > fire > earth > air > water. Strong ×1.2, weak ×0.85.",
         "bild": "erklaer_elementkreis"},
        {"id": "l3_brennen", "wann": "runde2",
         "en": "Fire burns, brother. Every stack bites each round, up to five of them. Defend to put one out, and "
               "stop feeding the flames!",
         "de": "Burning 🔥: 1–5 stacks, damage every round. Defend removes 1 stack.", "bild": "erklaer_brennen"},
        {"id": "l3_reaktion", "wann": "runde3",
         "en": "Mix the elements and things react! Fire on wet makes steam, lightning on wet makes a short circuit. "
               "Play with it!",
         "de": "Reactions: steam (fire + wet), short circuit (shock + wet), rupture, sparks, mud.",
         "bild": "erklaer_reaktionen"},
    ],
}
SCHRITTE = {s["id"]: s for l in LEKTIONEN.values() for s in l}
# Was Maxwell nach einer Lektion beibringt (Lektion -> Spezialangriff, kern/kampf.beibringen). Weitere Lehrer spaeter
# ueber denselben Weg (kampf.beibringen), nicht ueber Skillpunkte.
LEHRT = {1: "mistral"}
BEGEGNUNGEN = ("maxwell_tutorial", "maxwell_training")


def stand(z):
    t = z.setdefault("tutorial", {})
    t.setdefault("lektion", 1)
    t.setdefault("gesehen", [])
    t.setdefault("aktuell", None)
    _lehren(z, t)
    return t


def _lehren(z, t):
    """Alles beibringen, was abgeschlossene Lektionen lehren (holt es auch fuer alte Spielstaende nach)."""
    from . import kampf
    for n, sid in LEHRT.items():
        if t["lektion"] > n and sid not in kampf.known(z):
            kampf.beibringen(z, sid)


def _gilt(wann, k):
    g = (k.get("gegner") or [{}])[0]
    sp = k.get("spieler") or {}
    befehle = [e.get("befehl") for e in k.get("log", [])]
    if wann == "start":
        return k["phase"] == "spieler_wahl" and k.get("runde", 1) == 1 and "angriff" not in befehle
    if wann == "parade":
        return k["phase"] == "parade"
    if wann.startswith("runde"):
        return k["phase"] == "spieler_wahl" and k.get("runde", 1) >= int(wann[5:])
    if wann == "schwaeche":
        return bool(g.get("schwaeche_bekannt"))
    if wann == "angeschlagen":
        return k["phase"] == "spieler_wahl" and sp.get("lp", 1) <= sp.get("lp_max", 1) // 2
    if wann == "ende":
        return k["phase"] == "ende"
    return False


def schritt(z):
    """Naechster faelliger Schritt der aktiven Lektion im laufenden Maxwell-Kampf (merkt ihn sich) oder der zuletzt
    gezeigte. -> Schritt-Dict oder None."""
    k = z.get("kampf") or {}
    if k.get("definition") not in BEGEGNUNGEN or z.get("status") != "kampf":
        return None
    t = stand(z)
    lektion = LEKTIONEN.get(t["lektion"])
    if not lektion:
        return None
    bei = "%s|%s|%d" % (k.get("runde"), k.get("phase"), len(k.get("log", [])))
    if t.get("bei") != bei or not t["aktuell"]:            # hoechstens ein neuer Schritt je Kampfmoment
        for s in lektion:
            if s["id"] not in t["gesehen"] and _gilt(s["wann"], k):
                t["gesehen"].append(s["id"])
                t["aktuell"], t["bei"] = s["id"], bei
                break
    s = SCHRITTE.get(t["aktuell"])
    return dict(s, lektion=t["lektion"], audio="tut." + s["id"]) if s else None


def kampf_vorbei(z):
    """Nach einem Maxwell-Kampf: Lektion abgeschlossen (naechste beim naechsten Training)."""
    t = stand(z)
    if t["lektion"] in LEKTIONEN:
        t["lektion"] += 1
    t["aktuell"] = None
    _lehren(z, t)                                     # sofort beibringen, nicht erst beim naechsten Lesen des Stands


def zeile(zid):
    """Fester Satz fuer die Vorab-Vertonung: tut.<id> -> (Sprecher, Text) oder (None, None)."""
    s = SCHRITTE.get(zid[4:]) if zid.startswith("tut.") else None
    return ("maxwell", s["en"]) if s else (None, None)


def ansicht(z):
    """Aktueller Schritt fuer den Client (schaltet nicht weiter - das passiert nach jeder Kampfaktion)."""
    if z.get("status") != "kampf" or (z.get("kampf") or {}).get("definition") not in BEGEGNUNGEN:
        return None
    t = stand(z)
    s = SCHRITTE.get(t["aktuell"])
    return dict(s, lektion=t["lektion"], audio="tut." + s["id"]) if s else None


# ------------------------------------------------------------------ Training auf dem Sonnendeck (Duc 24.10.2026)
# Unter freiem Himmel, die Crew schaut zu. Kostet 1 Aktion. Erster Sieg je Akt: Kraft +1 (Duc 23.10.: "pro Akt 1
# Attributpunkt"). Zaehler fuer Events: 10 Siege -> Jana himmelt Duc an, 3 Niederlagen -> Chiara lacht ihn aus.
SIEGE_FUER_JANA = 10
NIEDERLAGEN_FUER_CHIARA = 3
SIEG = ("ko", "aufgabe")


# Aufgabe des Tages (Duc 02.11.2026, Brain Trust "Kampf-Tiefe"): Das erste Training am Tag stellt eine Aufgabe. Wer
# gewinnt und sie schafft, bekommt doppelte Training-Erfahrung, sonst die alte. Jedes weitere Training am selben Tag
# bringt keine Erfahrung ("muscles grow when you sleep") - kein Verbot, nur kein Lohn. Anlass: Spieltest-Bots
# trainierten bis zu 40-mal als Erfahrungsfarm. Die Zaehler schreibt kern/kampf.py in k["stat"].
XP_AUFGABE = 0.5           # task done (before: 0.25 for every training)
XP_OHNE = 0.25             # first training of the day, task missed
XP_EXTRA = 0.0             # every further training that day
SCHADEN_MAX = 0.2          # task "wenig": lose at most this share of max HP
RUNDEN_MAX = 4
AUFGABEN = (
    {"id": "serie", "text": "Maxwell's task: parry perfectly three times in a row, then win.",
     "ok": "Task done: three perfect parries in a row.", "nein": "Task missed: no three perfect parries in a row."},
    {"id": "erschoepft", "text": "Maxwell's task: make him exhausted, then hit him with a special attack.",
     "ok": "Task done: a special attack on an exhausted Maxwell.", "nein": "Task missed: no special attack while he was exhausted."},
    {"id": "konter", "text": "Maxwell's task: finish him with a counter.",
     "ok": "Task done: the counter ended it.", "nein": "Task missed: the last blow wasn't a counter."},
    {"id": "wenig", "text": "Maxwell's task: win and keep at least 80 % of your HP.",
     "ok": "Task done: you kept your HP.", "nein": "Task missed: you lost more than 20 % of your HP."},
    {"id": "schnell", "text": "Maxwell's task: win within %d rounds." % RUNDEN_MAX,
     "ok": "Task done: a quick win.", "nein": "Task missed: it took more than %d rounds." % RUNDEN_MAX},
)
AUFGABE = {a["id"]: a for a in AUFGABEN}
EXTRA_TEXT = "Extra round. No XP today – muscles grow when you sleep, brother."


def aufgabe_vergeben(z):
    """Right after the training fight starts: the first one of the day gets a task, every further one is an extra round.
    The task with the fewest successes comes next (ties: rotate by day), so every player meets all five."""
    k = z.get("kampf") or {}
    if k.get("definition") != "maxwell_training":
        return None
    tr = z.setdefault("training_kampf", {"siege": 0, "niederlagen": 0})
    if tr.get("aufgabe_tag") == z.get("tag"):
        k["aufgabe"] = {"id": None}
        k["def"]["xp_factor"] = XP_EXTRA
        k["def"]["goal"] = EXTRA_TEXT
        return k["aufgabe"]
    tr["aufgabe_tag"] = z.get("tag")
    geschafft = tr.setdefault("aufgaben", {})
    n = len(AUFGABEN)
    reihe = [AUFGABEN[(z.get("tag", 0) + i) % n] for i in range(n)]
    a = min(reihe, key=lambda x: geschafft.get(x["id"], 0))
    k["aufgabe"] = {"id": a["id"]}
    k["def"]["goal"] = a["text"]
    return k["aufgabe"]


def aufgabe_werten(k, art):
    """-> xp factor for this training; marks k["aufgabe"]["erfuellt"]. Called once from kampf._finish."""
    a = k.get("aufgabe") or {}
    if not a.get("id"):
        return XP_EXTRA
    st, sp = k.get("stat") or {}, k.get("spieler") or {}
    sieg = art in SIEG
    pruef = {"serie": st.get("serie_max", 0) >= 3,
             "erschoepft": bool(st.get("spezial_erschoepft")),
             "konter": bool(st.get("sieg_konter")),
             "wenig": k.get("lp_start", 0) - sp.get("lp", 0) <= SCHADEN_MAX * sp.get("lp_max", 1),
             "schnell": k.get("runde", 99) <= RUNDEN_MAX}
    a["erfuellt"] = sieg and pruef.get(a["id"], False)
    return XP_AUFGABE if a["erfuellt"] else XP_OHNE


def training_verfuegbar(z):
    return stand(z)["lektion"] > 1 or "tutorial_maxwell" in z.get("flags", [])


def training_ende(z, modul, ergebnis, k=None):
    """-> Zeilen. Zaehler, Flags fuer die Events, Kraft +1 beim ersten Sieg im Akt, Ergebnis der Tagesaufgabe."""
    tr = z.setdefault("training_kampf", {"siege": 0, "niederlagen": 0})
    zeilen = []
    a = (k or {}).get("aufgabe") or {}
    if a.get("id"):
        if a.get("erfuellt"):
            tr.setdefault("aufgaben", {})[a["id"]] = tr.setdefault("aufgaben", {}).get(a["id"], 0) + 1
        zeilen.append(AUFGABE[a["id"]]["ok" if a.get("erfuellt") else "nein"])
    elif a:
        zeilen.append(EXTRA_TEXT)
    if ergebnis in SIEG:
        tr["siege"] += 1
        akt_flag = "maxwell_kraft_akt1"
        if akt_flag not in z["flags"]:
            z["flags"].append(akt_flag)
            att = z["persona"]["attribute"]
            if att.get("strength", 0) < 5:
                att["strength"] = att.get("strength", 0) + 1
                zeilen.append("Strength +1 → %d (Maxwell's training, once per act)" % att["strength"])
        if tr["siege"] >= SIEGE_FUER_JANA and "training_siege_10" not in z["flags"]:
            z["flags"].append("training_siege_10")
    elif ergebnis == "niederlage":
        tr["niederlagen"] += 1
        if tr["niederlagen"] >= NIEDERLAGEN_FUER_CHIARA and "training_niederlagen_3" not in z["flags"]:
            z["flags"].append("training_niederlagen_3")
    zeilen.append("Training: %d wins, %d losses" % (tr["siege"], tr["niederlagen"]))
    return zeilen
