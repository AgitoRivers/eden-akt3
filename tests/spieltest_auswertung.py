# -*- coding: utf-8 -*-
r"""Evaluates the raw runs of tests/spieltest_bot.py: seven areas with a traffic light, findings and tables, plus the HTML report.

The limits at the top are starting values (Duc 30.10.2026: mine to propose, his to change), not an industry standard.
Everything shown is ids and numbers. Story text stays out of the page: it would spoil the game for Duc.
"""
import collections, html, json, os, re, statistics, subprocess, sys

HIER = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HIER)
MOD = os.path.join(BASE, "module", "eden_rise")

GRENZEN = {
    "events_gruen": 70, "events_gelb": 40,        # % of the built events reached by at least one player type
    "leere_tage_gelb": 1,                         # days without an event, fight or reward
    "luecke_gelb": 8, "luecke_rot": 14,           # phases between two rewards (6 phases = one day)
    "offen_gruen": 80,                            # % of day ends with something open ("one more day")
    "mechanik_luecke_gelb": 4,                    # days without a new mechanic
    "sieg_stark_rot": 50, "sieg_stark_gelb": 70,  # % fights won, strong player
    "sieg_schwach_gelb": 25,                      # below this a fight is a wall for beginners
    "zuege_zu_kurz": 2, "zuege_zu_lang": 12,      # target per expeditionen_2.md: 5-7 turns
    "geld_rest_gelb": 60,                         # % of all income still unspent at the end
    "scheinwahl_gelb": 25, "beste_option_gelb": 10,   # % of events with two or more answers
    "wiederholung_gelb": 85,                      # % of events shared by two runs of the same type
    "tote_flags_gelb": 30,                        # % of flags set by answers that nothing ever reads
    "satz_woerter": 25, "zeile_zeichen": 220, "item_zeichen": 220,
}
ZIEL_TAGE = 35                                    # Duc 30.10.2026: five weeks, the calendar in the code is only how far it is built
STARK, NORMAL, SCHWACH = ("sammler", "kaempfer"), ("romantiker", "sparer", "chaos"), ("schwach",)
SIEG = ("ko", "aufgabe", "entkommen")
OHNE_WERTUNG = ("maxwell_training",)              # sparring ends in surrender by design
NICHT_NOETIG = {"neu", "test_neustart", "szene_neu", "plan_laden", "job", "kabine_ausruhen", "intim"}   # engine paths the bot skips on purpose
PHASEN = ["fruehstueck", "tag", "nachmittag", "dinner", "abend", "nacht"]
TYP_NAME = {"sammler": "Alles-Sammler", "romantiker": "Romantiker", "kaempfer": "Kämpfer", "sparer": "Sparer", "schwach": "Schwacher Spieler",
            "chaos": "Chaos-Spieler"}
from spieltest_profile import PROFILE
TYP_NAME.update({k: p["name"] for k, p in PROFILE.items()})
STARK += tuple(k for k, p in PROFILE.items() if p["stil"] == "klug")
SCHWACH += ("noor",)


def _lade(name):
    return json.load(open(os.path.join(MOD, name), encoding="utf-8"))


def _prozent(a, b):
    return round(100.0 * a / b) if b else 0


def _median(w):
    w = list(w)
    return statistics.median(w) if w else 0


def _befund(stufe, text, ids=None):
    return {"stufe": stufe, "text": text, "ids": list(ids or [])}


class Bereich:
    def __init__(self, id, titel, vorbild, frage):
        self.d = {"id": id, "titel": titel, "vorbild": vorbild, "frage": frage, "befunde": [], "tabellen": [], "zahlen": {}}

    def b(self, stufe, text, ids=None):
        self.d["befunde"].append(_befund(stufe, text, ids))

    def t(self, titel, kopf, zeilen):
        self.d["tabellen"].append({"titel": titel, "kopf": kopf, "zeilen": zeilen})

    def z(self, name, wert):
        self.d["zahlen"][name] = wert

    def fertig(self):
        st = [b["stufe"] for b in self.d["befunde"]]
        self.d["ampel"] = "rot" if "rot" in st else "gelb" if "gelb" in st else "gruen"
        return self.d


# ------------------------------------------------------------------ 1 stability
def stabilitaet(L, wieder):
    a = Bereich("stabilitaet", "Stabilität", "Mindeststandard", "Läuft das Spiel bis zum Ende, ohne abzustürzen oder festzuhängen?")
    abst = collections.Counter()
    for r in L:
        for x in r["abstuerze"]:
            abst["%s %s in %s bei %s (%s, Tag %s)" % (x["fehler"], x["art"], x["wo"], x["aktion"], x["status"], x["tag"])] += 1
    for t, n in abst.most_common():
        a.b("rot", "Absturz, %d× : %s" % (n, t))
    sack = collections.Counter()
    for r in L:
        for x in r["sackgassen"]:
            sack["%s (Tag %s, %s, Status %s%s)" % (x["text"], x["tag"], x["phase"], x["status"], ", Event %s" % x["event"] if x.get("event") else "")] += 1
    for t, n in sack.most_common():
        a.b("rot", "Sackgasse, %d× : %s" % (n, t))
    nicht_fertig = [r for r in L if r["ende"]["status"] != "ende"]
    if nicht_fertig:
        a.b("rot", "%d von %d Läufen erreichen das Ende nicht." % (len(nicht_fertig), len(L)),
            ["%s/%s" % (r["typ"], r["seed"]) for r in nicht_fertig])
    sp = [r for r in L if r.get("speicher_abweichung")]
    if sp:
        a.b("rot", "Speichern und Laden verändert den Spielstand (%d Läufe)." % len(sp), ["%s/%s" % (r["typ"], r["seed"]) for r in sp])
    ang = collections.Counter()
    for r in L:
        ang.update(r["angebot_abgelehnt"])
    if ang:
        a.b("gelb", "%d angebotene Aktionen wurden vom Spiel abgelehnt: Der Knopf ist da, geht aber nicht." % sum(ang.values()),
            ["%s (%d×)" % kv for kv in ang.most_common(12)])
    lang = [x for r in L for x in r["lange_phasen"]]
    if lang:
        a.b("gelb", "%d Phasen ziehen sich über mehr als 400 Schritte, vielleicht eine Schleife." % len(lang),
            sorted({"Tag %s %s %s" % (x["tag"], x["phase"], x.get("event") or "") for x in lang})[:12])
    if wieder is not None and not wieder["gleich"]:
        a.b("gelb", "Derselbe Lauf endet beim zweiten Mal anders (%s/%s). Fehler sind dann schwer nachzustellen." % (wieder["typ"], wieder["seed"]))
    a.z("Läufe", len(L))
    a.z("Abstürze", sum(abst.values()))
    a.z("Sackgassen", sum(sack.values()))
    a.z("Schritte", sum(r["schritte"] for r in L))
    if not a.d["befunde"]:
        a.b("info", "Alle %d Läufe kommen ohne Absturz und Sackgasse ans Ende, mit %d Aktionen." % (len(L), sum(r["schritte"] for r in L)))
    return a.fertig()


# ------------------------------------------------------------------ 2 completeness
def aktionen_katalog():
    text = open(os.path.join(BASE, "eden.py"), encoding="utf-8").read()
    teil = text[text.index("def aktion(name, daten):"):text.index("def szene_beenden(z, modul):")]
    namen = set(re.findall(r'name == "(\w+)"', teil))
    for gruppe in re.findall(r"name in \(([^)]*)\)", teil):
        namen.update(re.findall(r'"(\w+)"', gruppe))
    return namen


def vollstaendigkeit(L, tage):
    a = Bereich("vollstaendigkeit", "Vollständigkeit", "Zelda", "Erreicht man alles, was gebaut ist?")
    ev = _lade("ereignisse.json")["events"]
    im_bau = [e for e in ev if (e["wann"].get("tage") or [0])[0] <= tage]
    spaeter = len(ev) - len(im_bau)
    gesehen = set().union(*[set(r["events"]) for r in L])
    erreicht = [e for e in im_bau if e["id"] in gesehen]
    pz = _prozent(len(erreicht), len(im_bau))
    a.z("Events erreicht %", pz)
    fehlt = [e for e in im_bau if e["id"] not in gesehen]
    pflicht = [e["id"] for e in fehlt if e["wann"].get("pflicht")]
    if pflicht:
        a.b("gelb", "%d Pflicht-Events hat kein Spielertyp gesehen. Pflicht heißt: Sie sollten kommen, wenn ihre Bedingung erfüllt ist." % len(pflicht), pflicht[:30])
    stufe = "info" if pz >= GRENZEN["events_gruen"] else "gelb" if pz >= GRENZEN["events_gelb"] else "rot"
    a.b(stufe, "%d %% der %d gebauten Events wurden erreicht (%d von %d)%s." % (
        pz, len(im_bau), len(erreicht), len(im_bau), ", %d liegen hinter dem Baustand" % spaeter if spaeter else ""))
    jeart = collections.defaultdict(lambda: [0, 0])
    for e in im_bau:
        jeart[e["art"]][1] += 1
        jeart[e["art"]][0] += e["id"] in gesehen
    a.t("Events je Art", ["Art", "erreicht", "gebaut", "%"], [[k, v[0], v[1], _prozent(*v)] for k, v in sorted(jeart.items(), key=lambda x: x[1][0] / max(1, x[1][1]))])
    if fehlt:
        a.b("info", "Nie erreichte Events, nach Art.", sorted("%s:%s" % (e["art"], e["id"]) for e in fehlt)[:60])
    optionen = sum(len(e["optionen"]) for e in erreicht)
    gewaehlt = set().union(*[set(r["event_wahl"]) for r in L])
    a.z("Antworten probiert %", _prozent(len(gewaehlt), optionen))
    a.b("info", "%d %% der Antworten in erreichten Events wurden mindestens einmal gewählt." % _prozent(len(gewaehlt), optionen))

    k = _lade("kaempfe.json")
    enc = {i: b for i, b in k["encounters"].items() if not b.get("test")}
    gek = {x["id"] for r in L for x in r["kaempfe"]}
    nie = sorted(set(enc) - gek)
    a.z("Kämpfe gesehen", "%d/%d" % (len(set(enc) & gek), len(enc)))
    if len(nie) > len(enc) / 2:
        a.b("gelb", "%d von %d Kampf-Begegnungen hat kein Spielertyp gesehen." % (len(nie), len(enc)), nie[:50])
    elif nie:
        a.b("info", "%d von %d Kampf-Begegnungen hat kein Spielertyp gesehen." % (len(nie), len(enc)), nie[:50])

    au = _lade("auftraege.json")
    orte = set().union(*[set(r["orte"]) for r in L])
    a.z("Orte besucht", "%d/%d" % (len(orte & set(au["orte"])), len(au["orte"])))
    if set(au["orte"]) - orte:
        a.b("info", "Orte, die kein Spielertyp betreten hat.", sorted(set(au["orte"]) - orte))
    fertig = set().union(*[set(r["auftraege_fertig"]) for r in L])
    a.z("Aufträge fertig", "%d/%d" % (len(fertig & set(au["auftraege"])), len(au["auftraege"])))
    if set(au["auftraege"]) - fertig:
        a.b("info", "Aufträge, die kein Spielertyp abgeschlossen hat.", sorted(set(au["auftraege"]) - fertig))

    modul = _lade("modul.json")
    items = {i: x for i, x in modul["items"].items() if x.get("art") not in ("gericht", "teil")}
    be = set().union(*[set(r["items"]) for r in L])
    nie_i = [i for i in items if i not in be]
    a.z("Items besessen %", _prozent(len(items) - len(nie_i), len(items)))
    je = collections.Counter(items[i].get("art") for i in nie_i)
    a.b("info", "%d von %d Items hat nie jemand besessen." % (len(nie_i), len(items)), ["%s: %d" % kv for kv in je.most_common()])

    katalog = aktionen_katalog() - NICHT_NOETIG
    benutzt = set().union(*[set(r["aktionen"]) for r in L])
    fehlend = sorted(katalog - benutzt)
    a.z("Aktionen getestet", "%d/%d" % (len(katalog & benutzt), len(katalog)))
    if fehlend:
        a.b("gelb" if len(fehlend) > 10 else "info", "%d Spiel-Aktionen hat der Bot nicht ausgelöst, sie sind ungetestet." % len(fehlend), fehlend)
    return a.fertig()


# ------------------------------------------------------------------ 3 loop and pace
def _reihe(tag, phase):
    return tag * 6 + (PHASEN.index(phase) if phase in PHASEN else 0)


def tempo(L, tage):
    a = Bereich("tempo", "Tagesschleife und Tempo", "Stardew Valley, Persona 5", "Passiert jeden Tag etwas, und zieht einen der Abend in den nächsten Tag?")
    zeilen, gr_leer, gr_luecke, gr_offen = [], [], [], []
    for typ in TYP_NAME:
        rs = [r for r in L if r["typ"] == typ]
        if not rs:
            continue
        leer, luecke, offen, fest, frei = [], [], [], [], []
        for r in rs:
            t = [x for x in r["tage"] if 1 <= x["tag"] <= tage]
            leer.append(sum(1 for x in t if not x["events"] and not x["kaempfe"] and not x["belohnungen"]))
            morgen = [x for x in t if x["tag"] >= 2]        # measured at the start of a day = the end of the day before
            reihe = [_reihe(b[0], b[1]) for b in r["belohnungen"]]
            spitze = 0
            letzter = _reihe(1, PHASEN[0])
            for w in sorted(reihe) + [_reihe(tage + 1, PHASEN[0])]:
                spitze = max(spitze, w - letzter)
                letzter = max(letzter, w)
            luecke.append(spitze)
            offen.append(_prozent(sum(1 for x in morgen if x["offene_ziele"]), len(morgen)))
            s = r["sekunden"]
            fest.append((s.get("events", 0) + s.get("kaempfe", 0) + s.get("minispiele", 0) + s.get("laeden", 0) + s.get("handy", 0)) / 60)
            frei.append(s.get("szenen", 0) / 60)
        zeilen.append([TYP_NAME[typ], round(_median(fest)), round(_median(frei)), round((_median(fest) + _median(frei)) / max(1, tage)),
                       round(_median(leer), 1), round(_median(luecke)), "%d %%" % _median(offen)])
        gr_leer.append((typ, _median(leer)))
        gr_luecke.append((typ, _median(luecke)))
        gr_offen.append((typ, _median(offen)))
    a.t("Je Spielertyp (Median)", ["Typ", "Min. feste Inhalte", "Min. freie Szenen", "Min. je Tag", "Leere Tage", "Längste Lücke ohne Belohnung (Phasen)", "Tagesenden mit offenem Ziel"], zeilen)
    def je_typ(liste):
        return ["%s: %g" % (TYP_NAME[t], w) for t, w in liste]
    wenig = [x for x in gr_leer if x[1] >= GRENZEN["leere_tage_gelb"]]
    if wenig:
        a.b("gelb", "Es gibt Tage ohne Event, Kampf oder Belohnung (Anzahl je Spielertyp).", je_typ(wenig))
    rot = [x for x in gr_luecke if x[1] >= GRENZEN["luecke_rot"]]
    gelb = [x for x in gr_luecke if GRENZEN["luecke_gelb"] <= x[1] < GRENZEN["luecke_rot"]]
    if rot:
        a.b("rot", "Mehr als zwei Tage vergehen ohne jede Belohnung (Phasen je Spielertyp).", je_typ(rot))
    if gelb:
        a.b("gelb", "Lange Strecken ohne Belohnung: bis zu %g Phasen, ein Tag hat 6 (Stufe, Item, Vertrauensstufe, Geld, Auftrag ...)." % max(x[1] for x in gelb), je_typ(gelb))
    zu = [x for x in gr_offen if x[1] < GRENZEN["offen_gruen"]]
    if zu:
        a.b("gelb", "Nicht jeder Abend lässt etwas offen: Bei unter %d %% der Tagesenden läuft ein Auftrag, ein Versprechen oder ein Favour (die Hauptstory zählt hier nicht)." % GRENZEN["offen_gruen"], je_typ(zu))
    a.z("Min. je Tag (erstes Profil)", zeilen[0][3] if zeilen else 0)
    a.z("Leere Tage (schlechtester Typ)", max((w for _, w in gr_leer), default=0))
    a.z("Längste Lücke (schlechtester Typ)", max((w for _, w in gr_luecke), default=0))

    from spieltest_bot_mechaniken import MECHANIKEN       # kept apart so this module runs without the engine
    erste = {}
    for r in L:
        for k, tag in r["erste"].items():
            if k in MECHANIKEN:
                erste[MECHANIKEN[k]] = min(erste.get(MECHANIKEN[k], 99), tag)
    je_tag = collections.defaultdict(list)
    for name, tag in erste.items():
        je_tag[tag].append(name)
    a.t("Wann welche Mechanik zum ersten Mal möglich war (bester Spielertyp)", ["Tag", "Neu"], [[t, ", ".join(sorted(n))] for t, n in sorted(je_tag.items())])
    bekannt = sorted(je_tag)
    if bekannt:
        lu, stelle, alt = 0, None, bekannt[0]
        for t in bekannt[1:] + [tage]:
            if t - alt > lu:
                lu, stelle = t - alt, alt
            alt = t
        a.z("Tage ohne neue Mechanik", lu)
        if lu >= GRENZEN["mechanik_luecke_gelb"]:
            a.b("gelb", "%d Tage lang kommt keine neue Mechanik dazu (nach Tag %s)." % (lu, stelle))
    if tage < ZIEL_TAGE:
        a.b("info", "Das Spiel ist bis Tag %d gebaut, geplant sind %d Tage. Die Spielzeit gilt nur für den gebauten Teil." % (tage, ZIEL_TAGE))
    a.b("info", "Die Spielzeit ist eine Schätzung: 200 Wörter/min lesen, echte Audiodauer, 8 s je Kampfzug, 4 Minuten je freier Szene (Annahme, das Sprachmodell ist im Test aus).")
    return a.fertig()


# ------------------------------------------------------------------ 4 combat
def kampf(L):
    a = Bereich("kampf", "Kampf und Schwierigkeit", "Hades, Clair Obscur", "Ist jeder Kampf fair, und lohnt sich Taktik?")
    je = collections.defaultdict(lambda: collections.defaultdict(list))
    alle = collections.defaultdict(list)
    for r in L:
        gruppe = "stark" if r["typ"] in STARK else "schwach" if r["typ"] in SCHWACH else "normal"
        for k in r["kaempfe"]:
            if k["id"] in OHNE_WERTUNG or "art" not in k:
                continue
            je[k["id"]][gruppe].append(k)
            alle[k["id"]].append(k)

    def quote(xs):
        return _prozent(sum(1 for k in xs if k["art"] in SIEG), len(xs)) if xs else None
    zeilen, zu_hart, wand, trivial, lang = [], [], [], [], []
    for eid, g in sorted(je.items(), key=lambda kv: min(k["tag"] for k in alle[kv[0]])):
        xs = alle[eid]
        zuege = _median(k["zuege"] for k in xs)
        rest = _median(_prozent(k.get("lp_ende") or 0, k.get("lp_max") or 1) for k in xs if k["art"] in SIEG)
        qs, qn, qw = quote(g["stark"]), quote(g["normal"]), quote(g["schwach"])
        zeilen.append([eid, "%d–%d" % (min(k["tag"] for k in xs), max(k["tag"] for k in xs)), len(xs), "-" if qs is None else "%d %%" % qs,
                       "-" if qn is None else "%d %%" % qn, "-" if qw is None else "%d %%" % qw, zuege, "%d %%" % rest])
        if qs is not None and len(g["stark"]) >= 2 and qs < GRENZEN["sieg_stark_gelb"]:
            zu_hart.append((eid, qs))
        if qw is not None and len(g["schwach"]) >= 2 and qw < GRENZEN["sieg_schwach_gelb"]:
            wand.append((eid, qw))
        if all(k["art"] in SIEG for k in xs) and zuege <= GRENZEN["zuege_zu_kurz"] and len(xs) >= 3 and rest >= 70:
            trivial.append(eid)
        if zuege >= GRENZEN["zuege_zu_lang"]:
            lang.append((eid, zuege))
    a.t("Je Begegnung (Siege, Median-Züge, Median-Leben am Ende)", ["Kampf", "Tage", "n", "Stark", "Normal", "Schwach", "Züge", "Leben"], zeilen)
    # a fight with a trick (untouchable enemy) says more about the bot than about the fight; a red light also needs enough runs
    defs = _lade("kaempfe.json")
    def raetsel(eid):
        b = defs["encounters"].get(eid) or {}
        gegner = b.get("enemy") if isinstance(b.get("enemy"), list) else [b.get("enemy")]
        return any((defs["enemies"].get(g) or {}).get("untouchable") for g in gegner if isinstance(g, str))
    knifflig = [x for x in zu_hart if raetsel(x[0])]
    if knifflig:
        a.b("gelb", "Rätselkämpfe, die der Bot oft verliert: %d. Er kennt den Trick nicht unbedingt, also selbst ansehen." % len(knifflig), ["%s (%d %%)" % x for x in knifflig])
    zu_hart = [x for x in zu_hart if not raetsel(x[0])]
    rot = [x for x in zu_hart if x[1] < GRENZEN["sieg_stark_rot"] and len(je[x[0]]["stark"]) >= 5]
    if rot:
        a.b("rot", "Kämpfe, die selbst ein starker Spieler in weniger als %d %% der Fälle gewinnt: %d." % (GRENZEN["sieg_stark_rot"], len(rot)), ["%s (%d %%)" % x for x in rot])
    gelb = [x for x in zu_hart if x not in rot]
    if gelb:
        a.b("gelb", "Kämpfe, die für starke Spieler hart sind (unter %d %% Siege): %d." % (GRENZEN["sieg_stark_gelb"], len(gelb)), ["%s (%d %%)" % x for x in gelb])
    if wand:
        a.b("gelb", "Kämpfe, die für schwache Spieler kaum zu schaffen sind (unter %d %% Siege): %d." % (GRENZEN["sieg_schwach_gelb"], len(wand)), ["%s (%d %%)" % x for x in wand])
    if trivial:
        a.b("gelb", "%d Kämpfe sind nach höchstens %d Zügen vorbei, und alle Spielertypen gewinnen sie fast unverletzt." % (len(trivial), GRENZEN["zuege_zu_kurz"]), trivial)
    if lang:
        a.b("gelb", "%d Kämpfe dauern im Median mindestens %d Züge (Ziel 5–7)." % (len(lang), GRENZEN["zuege_zu_lang"]), ["%s (%g)" % x for x in lang])
    hilfe = [h for r in L for h in r["hilfe"] if h.get("kampf")]
    if hilfe:
        a.b("gelb", "Festgefahren: In %d Läufen kam ein Spielertyp nach 5 Niederlagen nicht weiter, der Bot half ihm dann durch." % len(hilfe),
            sorted({"%s (Tag %s)" % (h["kampf"], h["tag"]) for h in hilfe}))
    einfache_typen = ("romantiker", "sparer") + tuple(pid for pid, p in PROFILE.items() if p["stil"] == "einfach")
    einfach = [k for r in L if r["typ"] in einfache_typen for k in r["kaempfe"] if k["id"] not in OHNE_WERTUNG and "art" in k]
    klug = [k for r in L if r["typ"] in STARK for k in r["kaempfe"] if k["id"] not in OHNE_WERTUNG and "art" in k]
    qe, qk = quote(einfach), quote(klug)
    if qe is not None and qk is not None:
        a.z("Siege nur Angriff %", qe)
        a.z("Siege mit Taktik %", qk)
        if qe >= 90:
            a.b("gelb", "Wer nur angreift, gewinnt %d %% seiner Kämpfe. Taktik wird kaum gebraucht (mit Taktik: %d %%)." % (qe, qk))
        else:
            a.b("info", "Nur Angriff gewinnt %d %% der Kämpfe, mit Taktik und besserer Parade %d %%." % (qe, qk))
    lv = []
    for typ in TYP_NAME:
        rs = [r for r in L if r["typ"] == typ]
        if rs:
            lv.append([TYP_NAME[typ], _median(r["level"] for r in rs), _median(len(r["kaempfe"]) for r in rs),
                       ", ".join("%s %d %%" % (b, _prozent(n, sum(sum(k["befehle"].values()) for r in rs for k in r["kaempfe"])))
                                 for b, n in collections.Counter({c: sum(k["befehle"].get(c, 0) for r in rs for k in r["kaempfe"])
                                                                  for c in ("angriff", "faehigkeit", "verteidigen", "gegenstand")}).most_common() if n)])
    a.t("Fortschritt je Spielertyp (Median am Ende)", ["Typ", "Level", "Kämpfe", "Befehle"], lv)
    levels = [x[1] for x in lv]
    if levels and max(levels) - min(levels) >= 5:
        a.b("gelb", "Die Stufe am Ende liegt je nach Spielweise zwischen %g und %g. Für die späteren Kämpfe im Blick behalten." % (min(levels), max(levels)))
    waffen = collections.defaultdict(list)
    for r in L:
        if r["typ"] in STARK:
            for k in r["kaempfe"]:
                if k.get("waffe") and k["id"] not in OHNE_WERTUNG and "art" in k:
                    waffen[k["waffe"]].append(k)
    if waffen:
        a.t("Waffen (starke Spieler)", ["Waffe", "Kämpfe", "Siege", "Median-Züge"],
            [[w, len(x), "%d %%" % quote(x), _median(k["zuege"] for k in x)] for w, x in sorted(waffen.items(), key=lambda kv: -len(kv[1]))])
    a.z("Begegnungen gemessen", len(zeilen))
    return a.fertig()


# ------------------------------------------------------------------ 5 economy
def wirtschaft(L, tage):
    a = Bereich("wirtschaft", "Wirtschaft", "Dave the Diver", "Bleibt Geld ein Ziel, oder sammelt es sich an?")
    zeilen, rest_hoch = [], []
    punkte = [t for t in (1, 3, 7, 10, 14, 21, 28, 35) if t <= tage + 1]
    for typ in TYP_NAME:
        rs = [r for r in L if r["typ"] == typ]
        if not rs:
            continue
        spalte = []
        for t in punkte:
            w = [x["konto"] for r in rs for x in r["tage"] if x["tag"] == t]
            spalte.append(round(_median(w)) if w else "-")
        ein = _median(sum(r["einnahmen"].values()) for r in rs)
        aus = _median(sum(r["ausgaben"].values()) for r in rs)
        ende = _median(r["konto"] for r in rs)
        zeilen.append([TYP_NAME[typ]] + spalte + [round(ende), round(ein), round(aus)])
        if ein and _prozent(ende, ein) >= GRENZEN["geld_rest_gelb"] and typ in ("sammler", "kaempfer", "romantiker", "chaos"):   # the others hold back by design
            rest_hoch.append("%s: %d %% von %d €" % (TYP_NAME[typ], _prozent(ende, ein), ein))
    a.t("Kontostand morgens (Median, €)", ["Typ"] + ["Tag %d" % t for t in punkte] + ["Ende", "Einnahmen", "Ausgaben"], zeilen)
    if rest_hoch:
        a.b("gelb", "Auch Spielertypen, die gern ausgeben, haben am Ende den größten Teil ihrer Einnahmen noch. Das Geld findet zu wenig Ziele.", rest_hoch)
    ein_ges, aus_ges = collections.Counter(), collections.Counter()
    for r in L:
        ein_ges.update(r["einnahmen"])
        aus_ges.update(r["ausgaben"])
    a.t("Geldquellen, alle Läufe", ["Woher", "€"], [[k, round(v)] for k, v in ein_ges.most_common(10)])
    a.t("Geldsenken, alle Läufe", ["Wofür", "€"], [[k, round(v)] for k, v in aus_ges.most_common(12)])
    modul = _lade("modul.json")
    kaeuflich = {i: x for i, x in modul["items"].items() if x.get("preis") and x.get("wo") and x.get("art") not in ("teil", "gericht")}
    be = set().union(*[set(r["items"]) for r in L])
    nie = [i for i in kaeuflich if i not in be]
    a.z("Kaufbare Items je besessen %", _prozent(len(kaeuflich) - len(nie), len(kaeuflich)))
    if nie:                                   # the bot buys a few things a day, so this is no verdict on the items
        a.b("info", "%d von %d kaufbaren Items hat kein Spielertyp gekauft oder gefunden." % (len(nie), len(kaeuflich)),
            ["%s: %d" % kv for kv in collections.Counter(kaeuflich[i].get("art") for i in nie).most_common()])
    spitze = max((r["konto"] for r in L), default=0)
    teuer = [i for i, x in kaeuflich.items() if x["preis"] > max(spitze, 1)]
    if teuer:
        a.b("gelb", "%d Items kosten mehr, als je ein Spieler auf dem Konto hatte (%d €)." % (len(teuer), spitze), teuer[:20])
    voll = [(TYP_NAME[t], _median(r.get("tasche_voll_tage", 0) for r in L if r["typ"] == t)) for t in TYP_NAME if any(r["typ"] == t for r in L)]
    a.z("Tage mit voller Tasche (Spitze)", max((n for _, n in voll), default=0))
    hoch = [x for x in voll if x[1] >= tage / 3]
    if hoch:
        a.b("gelb", "Die Tasche ist oft voll: An mindestens einem Drittel der Tage ist beim Einkauf kein Platz mehr. Das fühlt sich nach Verwaltung an.",
            ["%s: %g Tage" % x for x in hoch])
    a.z("Ende Median €", round(_median(r["konto"] for r in L)))
    return a.fertig()


# ------------------------------------------------------------------ 6 decisions
NUMERISCH = ("vertrauen", "begehren", "rueckhalt", "geld", "energie", "wert", "uhr")


def _vektor(o):
    v, rest = collections.Counter(), []
    for f in list(o.get("folgen") or []):
        if "vertrauen" in f or "begehren" in f:
            art = "vertrauen" if "vertrauen" in f else "begehren"
            v["%s:%s" % (art, f[art][0])] += f[art][1]
        elif "geld" in f:
            v["geld"] += f["geld"]
        elif "rueckhalt" in f:
            v["rueckhalt"] += f["rueckhalt"]
        elif "wert" in f:
            v["wert:" + f["wert"]] += f.get("delta", 0)
        elif "weiter" in f:
            continue
        else:
            rest.append(json.dumps(f, sort_keys=True))
    return v, sorted(rest)


def entscheidungen(L):
    a = Bereich("entscheidungen", "Entscheidungen", "Hades, Balatro", "Haben Antworten Folgen, und lohnt sich ein zweiter Durchlauf?")
    ev = _lade("ereignisse.json")["events"]
    mehr = [e for e in ev if len(e["optionen"]) >= 2]
    gleich, beste, ohne = [], [], []
    for e in mehr:
        sig = {json.dumps([o.get("folgen"), o.get("probe"), o.get("bei_erfolg"), o.get("bei_fehlschlag"), o.get("energie")], sort_keys=True, default=str)
               for o in e["optionen"]}
        if len(sig) == 1:
            gleich.append(e["id"])
            continue
        vs = [_vektor(o) + (o,) for o in e["optionen"]]
        for i, (v, r, o) in enumerate(vs):
            if o.get("probe") or o.get("energie"):
                continue
            besser = True
            for j, (w, s, q) in enumerate(vs):
                if i == j:
                    continue
                keys = set(v) | set(w)
                if q.get("probe") or r != s or not all(v[k] >= w[k] for k in keys) or not any(v[k] > w[k] for k in keys):
                    besser = False
                    break
            if besser:
                beste.append(e["id"])
                break
    pz_g, pz_b = _prozent(len(gleich), len(mehr)), _prozent(len(beste), len(mehr))
    a.z("Scheinwahl %", pz_g)
    a.z("Klar beste Antwort %", pz_b)
    if pz_g >= GRENZEN["scheinwahl_gelb"]:
        a.b("gelb", "Bei %d %% der Events (%d von %d) haben alle Antworten dieselbe Wirkung. Nur die Stimmung ändert sich." % (pz_g, len(gleich), len(mehr)), gleich[:40])
    else:
        a.b("info", "Bei %d %% der Events (%d von %d) haben alle Antworten dieselbe Wirkung." % (pz_g, len(gleich), len(mehr)), gleich[:40])
    if pz_b >= GRENZEN["beste_option_gelb"]:
        a.b("gelb", "Bei %d %% der Events (%d) ist eine Antwort in jedem Wert mindestens so gut wie alle anderen, ohne Risiko." % (pz_b, len(beste)), beste[:40])
    else:
        a.b("info", "Bei %d %% der Events (%d) ist eine Antwort in jedem Wert mindestens so gut wie alle anderen, ohne Risiko." % (pz_b, len(beste)), beste[:40])
    # do set flags ever matter?
    setzer = collections.defaultdict(set)
    for e in ev:
        for o in e["optionen"]:
            for f in list(o.get("folgen") or []) + list(o.get("bei_erfolg") or []) + list(o.get("bei_fehlschlag") or []):
                for k in ("flag", "flag_datiert"):
                    if isinstance(f.get(k), str):
                        setzer[f[k]].add(e["id"])
    worte = collections.Counter()
    for ordner, endung in ((MOD, ".json"), (os.path.join(BASE, "kern"), ".py"), (BASE, "eden.py")):
        if os.path.isfile(os.path.join(ordner, endung)):
            dateien = [os.path.join(ordner, endung)]
        else:
            dateien = [os.path.join(ordner, n) for n in os.listdir(ordner) if n.endswith(endung)]
        for p in dateien:
            if os.path.basename(p) in ("audio_index.json", "stimme_tags.json"):
                continue
            worte.update(re.findall(r"\w+", open(p, encoding="utf-8", errors="replace").read()))
    roh = open(os.path.join(MOD, "ereignisse.json"), encoding="utf-8").read()
    setz_n = collections.Counter(re.findall(r'"flag(?:_datiert)?": "(\w+)"', roh))
    tot = sorted(f for f in setzer if worte[f] <= setz_n[f])
    pz_t = _prozent(len(tot), len(setzer))
    a.z("Flags ohne Wirkung %", pz_t)
    ev_tot = collections.Counter(next(iter(setzer[f])) for f in tot)
    (a.b)("gelb" if pz_t >= GRENZEN["tote_flags_gelb"] else "info",
          "%d %% der von Antworten gesetzten Flags (%d von %d) liest nichts im Spiel. Solche Entscheidungen haben später keine Folge (grobe Prüfung, Flags mit Präfix-Lesern zählen hier mit)." % (pz_t, len(tot), len(setzer)),
          ["%s (%d)" % kv for kv in ev_tot.most_common(30)])
    # second run: how much is new?
    def ueberlapp(A, B):
        return _prozent(len(A & B), len(A | B)) if A | B else 100
    gleich_typ = []
    for typ in TYP_NAME:
        rs = [set(r["events"]) for r in L if r["typ"] == typ]
        gleich_typ += [ueberlapp(rs[i], rs[j]) for i in range(len(rs)) for j in range(i + 1, len(rs))]
    zwischen = []
    for i, r in enumerate(L):
        for q in L[i + 1:]:
            if r["typ"] != q["typ"]:
                zwischen.append(ueberlapp(set(r["events"]), set(q["events"])))
    if gleich_typ:
        wie = _median(gleich_typ)
        a.z("Gleiche Events, 2. Lauf %", round(wie))
        a.b("gelb" if wie >= GRENZEN["wiederholung_gelb"] else "info",
            "Zwei Läufe desselben Spielertyps teilen %d %% der Events, zwei verschiedene Spielertypen %d %%." % (wie, _median(zwischen)))
    faelle = collections.Counter(str(r.get("fall")) for r in L if r.get("fall"))
    if faelle:
        a.t("Gezogene Fälle", ["Fall", "Läufe"], [[k, v] for k, v in sorted(faelle.items())])
    return a.fertig()


# ------------------------------------------------------------------ 7 content
def _saetze(t):
    return [x for x in re.split(r"(?<=[.!?…])\s+", t or "") if x.strip()]


def inhalte(L):
    a = Bereich("inhalte", "Inhalte und Sprache", "Lokalisierungsprüfung", "Fehlt etwas, und versteht auch ein Nicht-Muttersprachler den Text?")
    sys.path.insert(0, os.path.join(BASE, "werkzeuge", "eden_rise"))
    sys.path.insert(0, BASE)
    import vertonen_eden_rise as V
    index = json.load(open(os.path.join(MOD, "audio_index.json"), encoding="utf-8")) if os.path.exists(os.path.join(MOD, "audio_index.json")) else {}
    cfg = json.load(open(os.path.join(BASE, "eden-config.json"), encoding="utf-8-sig"))
    stimmen = (cfg.get("stimmen") or {}).get("eden_rise") or {}
    alle = V.saetze()
    fehlt, alt, ohne = [], [], collections.Counter()
    for key, wer, text in alle:
        if not stimmen.get(wer):
            ohne[wer] += 1
            continue
        e = index.get(key)
        if not e or not os.path.isfile(os.path.join(MOD, "audio", e.get("datei", ""))):
            fehlt.append(key)
        elif e.get("text") != text:
            alt.append(key)
    a.z("Zeilen vertont %", _prozent(len(alle) - len(fehlt) - len(alt) - sum(ohne.values()), len(alle)))
    if fehlt:
        a.b("gelb", "%d von %d festen Zeilen haben keine Aufnahme." % (len(fehlt), len(alle)), fehlt[:30])
    if alt:
        a.b("gelb", "%d Aufnahmen passen nicht mehr zum aktuellen Text." % len(alt), alt[:30])
    if ohne:
        a.b("gelb", "%d Zeilen von Figuren ohne zugeordnete Stimme." % sum(ohne.values()), ["%s: %d" % kv for kv in ohne.most_common()])
    if not fehlt and not alt and not ohne:
        a.b("info", "Alle %d festen Zeilen sind vertont." % len(alle))
    try:
        r = subprocess.run([sys.executable, os.path.join(BASE, "werkzeuge", "eden_rise", "stimme_tags_pruefen.py")], cwd=BASE,
                           capture_output=True, encoding="utf-8", errors="replace", env=dict(os.environ, PYTHONUTF8="1"), timeout=120)
        z = collections.Counter(m.group(1) for m in re.finditer(r"^\s*(FEHLT|VERWAIST|ABWEICHT)\b", r.stdout, re.M))
        a.z("Zeilen ohne Stimm-Tag", z.get("FEHLT", 0))
        if z.get("FEHLT") or z.get("ABWEICHT"):
            a.b("gelb", "Stimm-Tags: %d Zeilen ohne Tag, %d weichen vom Text ab." % (z["FEHLT"], z["ABWEICHT"]))
        if z.get("VERWAIST"):
            a.b("info", "Stimm-Tags: %d Einträge ohne passende Zeile (verwaist)." % z["VERWAIST"])
    except (OSError, subprocess.SubprocessError):
        a.b("info", "Stimm-Tags konnten nicht geprüft werden.")
    deutsch, bild, ohne_b = collections.Counter(), collections.Counter(), collections.Counter()
    for r in L:
        deutsch.update(r["deutsch"])
        bild.update(r["bild_fehlt"])
        ohne_b.update(r["ohne_bild"])
    a.z("Deutsche Reste", len(deutsch))
    a.z("Fehlende Bilder", len(bild))
    if deutsch:
        # only field and first three words on the page: the full text sits in letzter.json, these lines can be case notes
        kurz = sorted({" ".join(k.split()[:6]) + " …" for k in deutsch})
        a.b("gelb", "%d Texte sehen im Spiel deutsch aus (grobe Prüfung, gekürzt wegen Spoilern; volle Texte in letzter.json)." % len(deutsch), kurz[:25])
    if bild:
        a.b("gelb", "%d Hintergrundbilder fehlen, das Spiel zeigt dort nichts." % len(bild), sorted(bild))
    if ohne_b:
        a.b("info", "Anzeige-Felder, die kein Bild liefern (können gewollte Platzhalter sein).", ["%s" % k for k, _ in ohne_b.most_common(10)])
    ev = _lade("ereignisse.json")["events"]
    lang_satz, lange_zeile = [], []
    for e in ev:
        texte = [e.get("lage") or ""] + [z.get("text") or "" for z in e.get("zeilen") or []]
        n = max((len(s.split()) for t in texte for s in _saetze(t)), default=0)
        if n > GRENZEN["satz_woerter"]:
            lang_satz.append((e["id"], n))
        if any(len(z.get("text") or "") > GRENZEN["zeile_zeichen"] for z in e.get("zeilen") or []):
            lange_zeile.append(e["id"])
    a.z("Events mit langem Satz", len(lang_satz))
    if lang_satz:
        lang_satz.sort(key=lambda x: -x[1])
        a.b("gelb" if _prozent(len(lang_satz), len(ev)) >= 10 else "info",
            "%d Events enthalten Sätze über %d Wörter. Schwer für Nicht-Muttersprachler." % (len(lang_satz), GRENZEN["satz_woerter"]),
            ["%s (%d)" % x for x in lang_satz[:25]])
    if lange_zeile:
        a.b("info", "%d Events enthalten Sprechzeilen über %d Zeichen." % (len(lange_zeile), GRENZEN["zeile_zeichen"]), lange_zeile[:25])
    modul = _lade("modul.json")
    item_lang = [i for i, x in modul["items"].items() if len(x.get("text") or "") > GRENZEN["item_zeichen"]]
    a.z("Item-Texte zu lang", len(item_lang))
    if item_lang:
        a.b("gelb", "%d Item-Texte sind länger als %d Zeichen (Regel aus dem Item-Stil)." % (len(item_lang), GRENZEN["item_zeichen"]), item_lang[:30])
    return a.fertig()


# ------------------------------------------------------------------ everything
def auswerten(L, tage, wieder):
    return [stabilitaet(L, wieder), vollstaendigkeit(L, tage), tempo(L, tage), kampf(L), wirtschaft(L, tage), entscheidungen(L), inhalte(L)]


def vergleichen(bereiche, alt):
    """Marks findings that are new against the last run and collects the numbers that moved."""
    if not alt:
        return
    vorher = {b["id"]: b for b in alt.get("bereiche", [])}
    for b in bereiche:
        v = vorher.get(b["id"])
        if not v:
            continue
        b["ampel_vorher"] = v.get("ampel")
        texte = {re.sub(r"\d+", "N", x["text"]) for x in v.get("befunde", [])}
        for x in b["befunde"]:
            x["neu"] = re.sub(r"\d+", "N", x["text"]) not in texte
        b["weg"] = sorted({x["text"] for x in v.get("befunde", []) if re.sub(r"\d+", "N", x["text"]) not in
                           {re.sub(r"\d+", "N", y["text"]) for y in b["befunde"]} and x["stufe"] != "info"})[:10]
        b["zahlen_vorher"] = {k: x for k, x in v.get("zahlen", {}).items() if k in b["zahlen"] and x != b["zahlen"][k]}


# ------------------------------------------------------------------ the page
FARBE = {"rot": "Rot", "gelb": "Gelb", "gruen": "Grün"}


def _e(x):
    return html.escape(str(x))


def seite(meta, bereiche):
    wichtig = []
    for b in bereiche:
        for x in b["befunde"]:
            if x["stufe"] in ("rot", "gelb"):
                wichtig.append((0 if x["stufe"] == "rot" else 1, b["titel"], x))
    wichtig.sort(key=lambda w: (w[0], not w[2].get("neu")))
    gesamt = "rot" if any(b["ampel"] == "rot" for b in bereiche) else "gelb" if any(b["ampel"] == "gelb" for b in bereiche) else "gruen"
    aus = []
    w = aus.append
    w("<!doctype html><html lang='de'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>")
    w("<title>Eden Spieltest</title><style>%s</style></head><body><main>" % CSS)
    w("<header><p class='klein'>Eden Rise · Spieltest · %s</p><h1>%s</h1><p class='unter'>%s</p></header>" % (
        _e(meta["zeit"]), _e({"rot": "Es gibt ernste Probleme", "gelb": "Spielbar, mit offenen Punkten", "gruen": "Keine auffälligen Probleme"}[gesamt]),
        _e("%d Läufe (%d Spielertypen × %d Seeds), gebaut bis Tag %d von %d. Stand %s%s, %s." % (
            meta["laeufe"], meta["typen"], meta["seeds"], meta["tage"], ZIEL_TAGE, meta["commit"],
            ", mit nicht committeten Änderungen" if meta["dirty"] else "", meta["dauer"]))))
    w("<section class='karten'>")
    for b in bereiche:
        vor = b.get("ampel_vorher")
        hin = " <span class='klein'>(vorher %s)</span>" % FARBE[vor] if vor and vor != b["ampel"] else ""
        n = sum(1 for x in b["befunde"] if x["stufe"] in ("rot", "gelb"))
        w("<a class='karte' href='#%s'><span class='punkt %s' aria-label='%s'></span><strong>%s</strong><span class='klein'>%s%s</span></a>" % (
            b["id"], b["ampel"], FARBE[b["ampel"]], _e(b["titel"]), "%d offen" % n if n else "ok", hin))
    w("</section>")
    if wichtig:
        w("<section><h2>Das Wichtigste zuerst</h2><ol class='liste'>")
        for _, titel, x in wichtig:
            w("<li><span class='punkt %s'></span><div><span class='klein'>%s%s</span><br>%s</div></li>" % (
                x["stufe"], _e(titel), " · neu" if x.get("neu") else "", _e(x["text"])))
        w("</ol></section>")
    for b in bereiche:
        w("<section id='%s'><h2><span class='punkt %s'></span>%s</h2><p class='unter'>%s <span class='klein'>Vorbild: %s</span></p>" % (
            b["id"], b["ampel"], _e(b["titel"]), _e(b["frage"]), _e(b["vorbild"])))
        if b["zahlen"]:
            w("<div class='zahlen'>")
            for k, v in b["zahlen"].items():
                alt = b.get("zahlen_vorher", {}).get(k)
                w("<div><b>%s</b><span class='klein'>%s%s</span></div>" % (_e(v), _e(k), " (vorher %s)" % _e(alt) if alt is not None else ""))
            w("</div>")
        for x in sorted(b["befunde"], key=lambda y: {"rot": 0, "gelb": 1, "info": 2}[y["stufe"]]):
            w("<div class='befund'><span class='punkt %s'></span><div>%s%s" % (x["stufe"], _e(x["text"]), " <span class='neu'>neu</span>" if x.get("neu") else ""))
            if x["ids"]:
                w("<details><summary>%d Einträge</summary><p class='ids'>%s</p></details>" % (len(x["ids"]), _e(", ".join(x["ids"]))))
            w("</div></div>")
        if b.get("weg"):
            w("<details><summary>Seit dem letzten Lauf erledigt: %d</summary><ul>%s</ul></details>" % (len(b["weg"]), "".join("<li>%s</li>" % _e(t) for t in b["weg"])))
        for t in b["tabellen"]:
            w("<details class='tabelle'><summary>%s</summary><div class='rollen'><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div></details>" % (
                _e(t["titel"]), "".join("<th>%s</th>" % _e(k) for k in t["kopf"]),
                "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % _e(c) for c in z) for z in t["zeilen"])))
        w("</section>")
    w("<footer><p>Der Bot misst Anzeichen, keinen Spaß. Ob eine Szene wirkt, sieht er nicht: Das Sprachmodell ist im Test aus, die Grenzwerte sind Startwerte und stehen oben in <code>tests/spieltest_auswertung.py</code>. Der Bericht zeigt nur IDs und Zahlen.</p></footer>")
    w("</main></body></html>")
    return "".join(aus)


CSS = """
:root{--bg:#f6f5f2;--flaeche:#fff;--text:#1d1c1a;--leise:#6b6862;--linie:#e2dfd8;--rot:#c8372d;--gelb:#d99a12;--gruen:#2f8f57;--info:#8b8880}
@media (prefers-color-scheme:dark){:root{--bg:#141413;--flaeche:#1e1e1c;--text:#ecebe6;--leise:#a09d95;--linie:#33322e;--rot:#e8604f;--gelb:#e6b03a;--gruen:#4cb478;--info:#7f7c74}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:16px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:1040px;margin:0 auto;padding:32px 16px 64px}h1{font-size:30px;margin:4px 0 8px;line-height:1.2}h2{font-size:21px;margin:0 0 4px;display:flex;align-items:center;gap:10px}
.klein{font-size:13px;color:var(--leise)}.unter{color:var(--leise);margin:0 0 14px}section{background:var(--flaeche);border:1px solid var(--linie);border-radius:10px;padding:20px;margin:16px 0}
.punkt{flex:none;display:inline-block;width:12px;height:12px;border-radius:50%;background:var(--info);margin-top:6px}h2 .punkt{margin-top:0}.rot{background:var(--rot)}.gelb{background:var(--gelb)}.gruen{background:var(--gruen)}
.karten{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:10px;background:none;border:0;padding:0}.karte{display:grid;grid-template-columns:auto 1fr;column-gap:10px;background:var(--flaeche);border:1px solid var(--linie);border-radius:10px;padding:12px 14px;color:inherit;text-decoration:none}
.karte .klein{grid-column:2}.karte:hover{border-color:var(--leise)}.liste{list-style:none;margin:0;padding:0}.liste li{display:flex;gap:10px;padding:9px 0;border-top:1px solid var(--linie)}.liste li:first-child{border-top:0}
.zahlen{display:flex;flex-wrap:wrap;gap:8px 26px;margin:6px 0 14px}.zahlen div{display:flex;flex-direction:column}.zahlen b{font-size:20px;font-variant-numeric:tabular-nums}
.befund{display:flex;gap:10px;padding:7px 0}.neu{font-size:12px;border:1px solid var(--linie);border-radius:4px;padding:0 5px;color:var(--leise)}details{margin-top:5px}summary{cursor:pointer;color:var(--leise);font-size:14px}.ids{font:13px/1.6 ui-monospace,Consolas,monospace;color:var(--leise);overflow-wrap:anywhere;margin:6px 0}
.tabelle{margin-top:12px}.rollen{overflow-x:auto}table{border-collapse:collapse;width:100%;margin-top:8px;font-size:14px;font-variant-numeric:tabular-nums}th,td{text-align:left;padding:5px 12px 5px 0;border-bottom:1px solid var(--linie);white-space:nowrap}td:last-child{white-space:normal}th{color:var(--leise);font-weight:500}
footer{color:var(--leise);font-size:14px;margin-top:20px}code{font-family:ui-monospace,Consolas,monospace;font-size:13px}
"""
