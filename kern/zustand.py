# -*- coding: utf-8 -*-
"""Spielstand eines Durchlaufs - gehoert dem Code, nicht dem Sprachmodell.

Ein Durchlauf (run) haelt: Tag/Phase, Persona, Werte, Uhren, Flags, Inventar, Codex, Gedaechtnis je Figur,
"heute" (was heute schon passiert ist), Verlauf, aktuellen Tagesplan und die laufende Szene.
Gespeichert wird nach jedem Zug (Ironman braucht das ohnehin)."""
import copy, json, os, random, time, uuid

from . import moral

INVENTAR_PLAETZE = 6          # Fallback ohne modul["tasche"]; Eden Rise: 8 / 12 / 16 (Duc 29.10.2026, Rosi ruestet auf)


def inventar_plaetze(z, modul):
    """Plaetze der Tasche: Start aus modul["tasche"], je gekaufter Stufe bei Rosi mehr (kern/handel.tasche_kaufen)."""
    t = modul.get("tasche") or {}
    st = min(z.get("tasche_stufe", 0), len(t.get("stufen") or []))
    return t["stufen"][st - 1]["plaetze"] if st else t.get("start", INVENTAR_PLAETZE)
# Punkte-Skala (16.10.2026): Rechnung 5 Stufen -> ein fokussierter Spieler war an Tag 2-3 bei 5/5 (20+ Erlebnisse,
# nur 2 noetig). Jetzt: Punkte 0-100, Stufe aus Schwellen, nach oben teurer.
STUFEN_AB = [0, 10, 22, 36, 55, 80]
GESPRAECH_DECKEL = 35          # Gespraeche und kleine Gesten tragen bis KNAPP vor Stufe 3 (Duc 27.10.2026: Stufe 3 nur
                               # ueber Erlebnisse - Events, Abende, grosse Gesten, Missionen; vorher 36 = Stufe 3 erreicht)
PUNKTE_JE_STUFE = 8            # ein "+1" in Folgen (Erlebnis) = 8 Punkte
PUNKTE_ACHSEN = ("vertrauen", "begehren")
GEDAECHTNIS_MAX = 8


def neu(modul, modus="ironman"):
    z = {
        "id": uuid.uuid4().hex[:10], "modul": modul["id"], "erstellt": time.strftime("%Y-%m-%d %H:%M"),
        "modus": modus, "status": "persona_wahl", "tag": 1, "phase": modul["zeitraster"]["phasen"][0],
        "persona": None, "werte": {}, "uhren": {u: 0 for u in modul["uhren"]}, "flags": [],
        "inventar": [], "codex": [], "gedaechtnis": {}, "gesehene_storylets": [], "heute": [], "verlauf": [],
        "plan": None, "plan_fehler": [], "optionen": [], "szene": None, "tagesnutzung": {}, "meldungen": [],
        "wahrheit": modul["wahrheit"].get("fest") or random.choice(list(modul["wahrheit"]["vorrat"])),
    }
    for name, w in modul["werte"].items():
        start = w.get("start", {})
        for x in w.get("je", []) + w.get("paare", []):
            z["werte"]["%s.%s" % (name, x)] = start.get(x, w["bereich"][0]) if isinstance(start, dict) else start
        if not w.get("je") and not w.get("paare"):
            z["werte"][name] = start if not isinstance(start, dict) else w["bereich"][0]
    for k in list(z["werte"]):
        if ist_achse(k):
            punkte(z, k)
    z["flags"] += modul.get("start_flags", [])
    z["inventar"] += modul.get("start_inventar", [])
    z["bekannt"] = list(modul.get("bekannt_start", []))
    # Phone driver baseline (24.10.2026): she texts only after progress with her since her last text
    z["handy_stand"] = {p: punkte(z, "vertrauen." + p) + punkte(z, "begehren." + p)
                        for p, d in modul["personen"].items()
                        if d.get("romanzierbar") and "vertrauen." + p in z["werte"] and "begehren." + p in z["werte"]}
    return z


def bekannt_machen(z, pids):
    """Wen Duc kennengelernt hat (17.10.2026) - schaltet die Missionen dieser Person frei."""
    b = z.setdefault("bekannt", [])
    for p in pids:
        if p not in b and p != "erzaehler":
            b.append(p)


def persona_setzen(z, modul, p):
    p = copy.deepcopy(p)
    z["persona"] = p
    for item in p.get("start_items", []):
        if item not in z["inventar"]:
            z["inventar"].append(item)
    z["status"] = "warte_auf_plan"


# Arten ohne Taschenplatz: Andenken, Quest-Gegenstaende und Schluessel (26.10.2026, wie Key Items in JRPGs)
OHNE_PLATZ = ("andenken", "quest", "schluessel")


def stapel(modul, iid):
    """Wie viele Stueck auf einem Platz liegen (Duc 28.10.2026: gewoehnlich 5, gut 3, sonst 1; Feld "stapel" im Modul)."""
    return max(1, int((modul["items"].get(iid) or {}).get("stapel") or 1))


def stapel_liste(modul, ids):
    """[(iid, n)] - gleiche Stuecke zu Stapeln zusammengefasst, in der Reihenfolge des ersten Auftretens; mehr als ein Stapel
    voll ergibt mehrere Eintraege (7 Pflaster = 5 + 2)."""
    zahl = {}
    for i in ids:
        zahl[i] = zahl.get(i, 0) + 1
    out = []
    for i, n in zahl.items():
        g = stapel(modul, i)
        while n > 0:
            out.append((i, min(n, g)))
            n -= g
    return out


def _plaetze(modul, ids):
    return sum(1 for i, _ in stapel_liste(modul, ids) if modul["items"].get(i, {}).get("art") not in OHNE_PLATZ)


def belegt(z, modul):
    """Belegte Inventarplaetze: je Stapel einer (Andenken, Quest-Gegenstaende und Schluessel zaehlen nicht mit), dazu was auf
    der laufenden Expedition abgebaut oder geangelt wurde (kern/expedition.py ernte)."""
    from . import expedition
    return _plaetze(modul, z["inventar"]) + expedition.ernte_plaetze(z, modul)


def platz_fuer(z, modul, iid, n=1):
    """Passen n Stueck noch in die Tasche (in einen offenen Stapel oder auf einen freien Platz)?"""
    if modul["items"].get(iid, {}).get("art") in OHNE_PLATZ:
        return True
    from . import expedition
    return _plaetze(modul, z["inventar"] + [iid] * n) + expedition.ernte_plaetze(z, modul) <= inventar_plaetze(z, modul)


def bereich(modul, key):
    name = key.split(".")[0]
    return modul["werte"][name]["bereich"]


def verborgen(modul, key):
    """Wert laeuft intern, wird aber nirgends angezeigt (Diesel/Strom in eden_rise, Duc 26.10.2026)."""
    return bool((modul["werte"].get(key.split(".")[0]) or {}).get("verborgen"))


def wert_label(modul, key):
    teile = key.split(".")
    label = modul["werte"][teile[0]].get("label", teile[0])
    if len(teile) > 1:
        wer = teile[1]
        if "_" in wer:
            wer = " / ".join(modul["personen"].get(x, {}).get("name", x).split()[0] for x in wer.split("_"))
        else:
            wer = modul["personen"].get(wer, {}).get("name", wer).split()[0]
        return "%s %s" % (label, wer)
    return label


def ist_achse(key):
    return key.split(".")[0] in PUNKTE_ACHSEN and "." in key


def stufe_aus(p):
    return max(i for i, a in enumerate(STUFEN_AB) if p >= a)


def punkte(z, key):
    """Punkte eines Werts; fehlen sie (alter Spielstand), aus der Stufe ableiten."""
    pk = z.setdefault("punkte", {})
    if key not in pk:
        pk[key] = STUFEN_AB[max(0, min(5, z["werte"].get(key, 0)))] + 4
    return pk[key]


def anteil(z, key):
    """Fuellstand innerhalb der aktuellen Stufe (0..1) fuer die Anzeige."""
    p, s = punkte(z, key), z["werte"].get(key, 0)
    if s >= 5:
        return 1.0
    return max(0.0, min(1.0, (p - STUFEN_AB[s]) / float(STUFEN_AB[s + 1] - STUFEN_AB[s])))


def anziehung(z, modul, pid):
    """Bewunderung (Duc 27.10.2026, nach Breedhaven): jede Frau schaetzt 2 Attribute (personen.<pid>.schaetzt).
    Ducs Werte darin ergeben 0/1/2 (Schnitt unter 2,5 / ab 2,5 / ab 3,5)."""
    att = (modul["personen"].get(pid) or {}).get("schaetzt") or []
    werte = (z.get("persona") or {}).get("attribute") or {}
    if not att or not werte:
        return 0
    from . import charms                        # Jacken-Charm zaehlt mit (Duc 28.10.2026: Attribut-Charms wirken ueberall)
    schnitt = sum(werte.get(a, 2) + charms.attribut(z, a) for a in att) / float(len(att))
    return 2 if schnitt >= 3.5 else 1 if schnitt >= 2.5 else 0


ANZIEHUNG_BONUS = 0.25        # Begehren-Gewinne x(1 + 0,25 je Stufe); Verluste und Spruenge (roh) bleiben unveraendert
QUELLEN = ("szenen", "handy", "geschenke", "events")   # Duc 02.11.2026: je Quelle ein eigener, unsichtbarer Topf (modul["toepfe"])
STUFEN_ABSTAND = 7            # Duc 31.10.2026: ab Stufe 3 steigt eine Achse erst nach so vielen Tagen weiter; 0 = aus (eden-config: stufen_abstand)


def topf_platz(z, modul, key, quelle):
    """Wie viele Punkte diese Quelle bei dieser Figur noch bringen darf; None = kein Topf (Nebenfiguren)."""
    achse, _, pid = key.partition(".")
    groesse = ((modul.get("toepfe") or {}).get(pid) or {}).get(quelle)
    if groesse is None or achse not in PUNKTE_ACHSEN:
        return None
    return max(0, groesse[PUNKTE_ACHSEN.index(achse)] - z.get("topf", {}).get(key, {}).get(quelle, 0))


def punkte_add(z, modul, key, pts, deckel=None, roh=False, frei=False, quelle="events"):
    """Punkte auf Vertrauen/Begehren; Stufe folgt. deckel: bis dorthin, darueber erst, wenn ein Erlebnis Stufe 3 gebracht hat
    (Gespraeche: 35). quelle: fuellt ihren Topf, ist er voll, bringt sie nichts mehr; roh zaehlt mit, wird aber nie begrenzt.
    roh: genau diese Punkte (Spruenge auf eine Stufe), ohne Bewunderungs-Bonus.
    frei: Story-Folge. Sie und roh sind vom Stufen-Abstand ausgenommen: Verdiente Spruenge bremst er nicht."""
    achse, _, pid = key.partition(".")
    if achse == "begehren" and key not in z["werte"]:
        return []                                      # Figuren ohne Begehren (Jana, Megan ...) bekommen keins
    if achse == "begehren" and pts > 0 and not roh:
        pts = int(round(pts * (1 + ANZIEHUNG_BONUS * anziehung(z, modul, pid))))
    p0 = punkte(z, key)
    if pts > 0 and deckel is not None and p0 <= deckel:
        if p0 == deckel:
            return []
        p1 = min(p0 + pts, deckel)
    else:
        p1 = p0 + pts
    platz = topf_platz(z, modul, key, quelle)
    if pts > 0 and not roh and platz is not None:
        if not platz:
            return []
        p1 = min(p1, p0 + platz)
    p1 = max(0, min(100, p1))
    s0 = z["werte"].get(key, 0)
    wartet = False
    if pts > 0 and not roh and not frei and STUFEN_ABSTAND and stufe_aus(p1) > s0:   # der Balken bleibt voll stehen
        erlaubt = 3 if s0 < 3 else s0 + 1 if z["tag"] - z.get("stufe_tag", {}).get(key, 1) >= STUFEN_ABSTAND else s0
        if stufe_aus(p1) > erlaubt:
            p1, wartet = STUFEN_AB[erlaubt + 1] - 1, True
    z["punkte"][key] = p1
    if p1 > p0 and platz is not None:
        t = z.setdefault("topf", {}).setdefault(key, {})
        t[quelle] = t.get(quelle, 0) + p1 - p0
    s1 = stufe_aus(p1)
    z["werte"][key] = s1
    if s1 > s0:
        z.setdefault("stufe_tag", {})[key] = z["tag"]
    if wartet and s1 == s0 and p1 != p0:
        return ["⏳ %s: the next step needs a few more days" % wert_label(modul, key)]
    if s1 != s0:
        return ["%s %+d" % (wert_label(modul, key), s1 - s0)]
    if p1 != p0:
        return ["%s %s" % (wert_label(modul, key), "↗" if p1 > p0 else "↘")]
    return []


def _ueberlauf(z, f, it, n=1):
    """Tasche voll (Duc 31.10.2026): Was die Story Duc gibt, wartet in der Kabinen-Truhe. Kampf-Beute ("beute") und alles auf
    einer Expedition bleibt liegen: dort ist die Wahl Teil des Spiels (docs/wiki/systeme/beute.md), und die Truhe darf die
    Verlust-Regel bei einer Niederlage nicht umgehen."""
    from . import expedition
    if f.get("beute") or expedition.aktiv(z):
        return "Inventory full – %s stays behind" % it["label"]
    z.setdefault("truhe", []).extend([f["item"]] * n)
    return "No room in your bag. %s is waiting in your cabin chest." % ("%s ×%d" % (it["label"], n) if n > 1 else it["label"])


def folgen_anwenden(z, modul, folgen, frei=True, quelle="events"):
    """Wendet Folgen an und liefert lesbare Zeilen (deutsch) fuer die Anzeige.
    frei: Story-Folge, ausgenommen vom Stufen-Abstand. Gesten, Geschenke, Reaktionen und Missionen geben frei=False."""
    zeilen = []
    for f in folgen:
        if "wert" in f and ist_achse(f["wert"]):        # Vertrauen/Begehren: Erlebnis in Punkten (8 je Stufe)
            zeilen += punkte_add(z, modul, f["wert"], PUNKTE_JE_STUFE * max(-2, min(2, f.get("delta", 0))), frei=frei, quelle=quelle)
        elif "wert" in f and f["wert"].split(".")[0] not in modul["werte"]:
            pass                                   # Wert gibt es im Modul nicht (mehr), z. B. Strom/Diesel seit 30.10.2026
        elif "wert" in f:
            lo, hi = bereich(modul, f["wert"])
            alt = z["werte"].get(f["wert"], lo)
            d = moral.delta(z, modul, f) if f["wert"] == moral.KEY else max(-2, min(2, f.get("delta", 0)))
            neu_w = max(lo, min(hi, alt + d))      # Moral: Momente doppelt, Alltag nur bis +2 (kern/moral.py)
            z["werte"][f["wert"]] = neu_w
            if neu_w != alt and f["wert"] == "ruf":
                z["ruf_tag"] = z.get("tag", 0)        # Ruf bewegt: Verblassen beginnt von vorn (kern/legenden.py)
            if neu_w != alt and not verborgen(modul, f["wert"]):
                zeilen.append("%s %+d" % (wert_label(modul, f["wert"]), neu_w - alt))
        if "uhr" in f:
            u = modul["uhren"][f["uhr"]]
            alt = z["uhren"].get(f["uhr"], 0)
            z["uhren"][f["uhr"]] = max(0, min(u["segmente"], alt + f.get("delta", 1)))
            if not u.get("verdeckt"):
                zeilen.append("Clock “%s” %d/%d" % (u["label"], z["uhren"][f["uhr"]], u["segmente"]))
            if z["uhren"][f["uhr"]] >= u["segmente"] and "uhr_%s_voll" % f["uhr"] not in z["flags"]:
                z["flags"].append("uhr_%s_voll" % f["uhr"])
                if not u.get("verdeckt"):
                    zeilen.append("⏰ %s" % u["voll"])
        if "vorliebe" in f:                         # Story-Effekt: eine Vorliebe wird bekannt (kern/vorlieben.py)
            from . import vorlieben
            zeilen += vorlieben.aus_folge(z, modul, f)
        if "flag" in f and f["flag"] not in z["flags"]:
            z["flags"].append(f["flag"])
        if "flag_datiert" in f:                 # Flag mit Datum (27.10.2026, Berge): Bedingung flag_seit [flag, tage]
            if f["flag_datiert"] not in z["flags"]:
                z["flags"].append(f["flag_datiert"])
            z.setdefault("flag_tag", {}).setdefault(f["flag_datiert"], z["tag"])
        if "nacht_bei" in f:                    # Wer die Nacht in der Belagerung mit Duc verbracht hat (Duc 02.11.2026, kern/taktik.py)
            z["nacht_bei"] = {"pid": f["nacht_bei"], "tag": z["tag"]}
        if "flag_weg" in f and f["flag_weg"] in z["flags"]:
            z["flags"].remove(f["flag_weg"])
        if "item" in f:
            it = modul["items"][f["item"]]
            if it.get("art") == "beweis":
                z["codex"].append("Beweis: " + it["label"])
                zeilen.append("Evidence in your codex: " + it["label"])
            elif f.get("n"):                    # several pieces at once, also on top of what he owns (Duc 30.10.2026)
                rein = sum(1 for _ in range(int(f["n"])) if platz_fuer(z, modul, f["item"]) and not z["inventar"].append(f["item"]))
                if rein:
                    zeilen.append("New in your bag: %s ×%d" % (it["label"], rein) if rein > 1 else "New in your bag: " + it["label"])
                if rein < int(f["n"]):
                    zeilen.append(_ueberlauf(z, f, it, int(f["n"]) - rein))
            elif f["item"] not in z["inventar"] and not platz_fuer(z, modul, f["item"]):
                zeilen.append(_ueberlauf(z, f, it))
            elif f["item"] not in z["inventar"]:
                z["inventar"].append(f["item"])
                zeilen.append("New in your bag: " + it["label"])
        if "item_weg" in f and f["item_weg"] in z["inventar"]:      # Gegenstand abgegeben (Minas Briefe, 30.10.2026)
            z["inventar"].remove(f["item_weg"])
        elif "item_weg" in f and f["item_weg"] in z.get("truhe", []):    # liegt in der Truhe: zaehlt fuer Bedingungen (kern/regeln.py), geht also auch von dort
            z["truhe"].remove(f["item_weg"])
        if "geld" in f:                         # Konto in Euro (16.10.2026), z. B. Lohn eines grossen Jobs
            betrag = int(f["geld"])
            z["konto"] = z.get("konto", 0) + betrag
            z.setdefault("buchungen", []).append({"tag": z["tag"], "text": f.get("text", "Szene"), "betrag": betrag})
            zeilen.append("Money %s%d € (%s)" % ("+" if betrag >= 0 else "−", abs(betrag), f.get("text", "Szene")))
        if "chip" in f:                         # Chip als Folge (26.10.2026): {"chip": [familie, stufe(, "jacke")]}, z. B. der Loewen-Chip
            from . import kampf
            defs = kampf.daten(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "module", z.get("modul") or "eden_rise"))
            if defs:
                zeilen.append(kampf.chip_finden(z, defs, f["chip"][0], int(f["chip"][1]))["text"])
                if f["chip"][2:] == ["jacke"] and kampf.chip_in_jacke(z, defs, f["chip"][0]):     # Rosi baut ihn gleich ein (Scout)
                    zeilen.append("Rosi fitted it into your jacket.")
        if "charm" in f:                        # Jacken-Charm (28.10.2026): {"charm": id}, z. B. Uebergabe bei Vertrauen 5, Mazzera-Fund
            from . import charms
            zeilen += charms.geben(z, f["charm"])
        if "charm_an" in f:                     # {"charm_an": id}: sofort an die getragene Jacke
            from . import charms, kampf
            if f["charm_an"] in charms.stand(z)["besitz"]:
                charms.einsetzen(z, (z.get("equipment") or {}).get("armor") or kampf.START_ARMOR, f["charm_an"])
        if "beibringen" in f:                   # Lehrer (26.10.2026): {"beibringen": "elicriso"} - Nonna, wie Maxwell Mistral
            from . import kampf
            if f["beibringen"] not in kampf.known(z):
                kampf.beibringen(z, f["beibringen"])
                zeilen.append("New technique: %s" % f["beibringen"].replace("_", " ").title())
        if "expedition" in f:                   # Expedition (26.10.2026, kern/expedition.py): Name = Start, "ende" = geschafft
            from . import expedition
            zeilen += expedition.ende(z, modul) if f["expedition"] == "ende" else expedition.starten(z, f["expedition"], modul)
        if "aufbau_beginnen" in f:              # Akt 3 (04.11.2026): Duc setzt den ersten Stein (kern/aufbau.py)
            from . import aufbau
            zeilen += aufbau.beginnen(z, f["aufbau_beginnen"])
        if "aufbau_stufe" in f:                 # Bauen-Los der Festa: eine Stufe ohne Baustoffe
            from . import aufbau
            zeilen += aufbau.stufe_geschenkt(z, f["aufbau_stufe"])
        if "codex" in f and f["codex"] not in z["codex"]:
            z["codex"].append(f["codex"])
            zeilen.append("Codex: " + f["codex"])
        if "punkte" in f and ist_achse(f["punkte"]):   # kleine Punkte statt Erlebnis (17.10.2026, Lieblingsort-Date)
            zeilen += punkte_add(z, modul, f["punkte"], int(f.get("n", 0)), deckel=GESPRAECH_DECKEL if f.get("deckel") else None)
    return zeilen


def gedaechtnis_add(z, pid, satz):
    z["gedaechtnis"].setdefault(pid, []).append("Day %d: %s" % (z["tag"], satz))
    z["gedaechtnis"][pid] = z["gedaechtnis"][pid][-GEDAECHTNIS_MAX:]


def speichern(ordner, z):
    os.makedirs(ordner, exist_ok=True)
    pfad = os.path.join(ordner, z["id"] + ".json")
    tmp = pfad + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(z, fh, ensure_ascii=False, indent=1)
    os.replace(tmp, pfad)


def laden(ordner, rid):
    return json.load(open(os.path.join(ordner, rid + ".json"), encoding="utf-8"))


# Personen, die im Modul ersetzt oder umbenannt wurden, stehen in modul["migration"] (rollen.py): alte Spielstaende
# spielen mit der neuen Figur weiter.


def angleichen(z, modul):
    """Alten Spielstand an das aktuelle Modul anpassen (16.10.2026): Werte, die es nicht mehr gibt, fallen weg
    (z. B. bordkasse), neue Werte/Uhren kommen mit Startwert dazu, unbekannte Gegenstaende fallen weg, ersetzte
    Personen (paoli -> elsa) werden in Plan, Szene und Handy getauscht. Liefert True, wenn sich etwas geaendert hat."""
    vorher = json.dumps(z, sort_keys=True)
    for roh in ((z.get("kueche") or {}).get("rohstoffe"), ((z.get("expedition") or {}).get("ernte") or {}).get("roh")):
        if roh and "stone" in roh:                     # Stein gibt es nicht mehr (Duc 30.10.2026): alter Vorrat wird Schiefer
            roh["slate"] = roh.get("slate", 0) + roh.pop("stone")
    neu = neu_werte(modul)
    z["werte"] = {k: v for k, v in z.get("werte", {}).items() if k.split(".")[0] in modul["werte"]}
    for k, v in neu.items():
        z["werte"].setdefault(k, v)
    for u in modul["uhren"]:
        z.setdefault("uhren", {}).setdefault(u, 0)
    mig = modul.get("migration") or {}
    ersetzt = mig.get("ersetzt") or {}
    if ersetzt and any(alt in vorher for alt in ersetzt):
        roh = json.dumps(z, ensure_ascii=False)
        for alt, ersatz in ersetzt.items():
            if ersatz in modul["personen"]:     # ID und Anzeigename (paoli -> elsa, Paoli -> Elsa)
                roh = roh.replace('"%s"' % alt, '"%s"' % ersatz).replace(alt.capitalize(), ersatz.capitalize())
        z.clear()
        z.update(json.loads(roh))
    # Umbenannt (z. B. 17.10.2026 Lulu -> Alva), im ganzen Text (IDs wie lulus_bar, Gegenstaende, Chronik, Gedaechtnis,
    # Chat). Vor dem Inventar-Filter, sonst fielen lulus_rose & Co. als "unbekannt" weg.
    umb = mig.get("umbenannt") or []
    if any(alt in vorher for alt, _ in umb):
        roh = json.dumps(z, ensure_ascii=False)
        for alt, neu_name in umb:
            roh = roh.replace(alt, neu_name)
        z.clear()
        z.update(json.loads(roh))
    z["inventar"] = [i for i in z.get("inventar", []) if i in modul["items"]]
    z["tasche"] = [i for i in z.get("tasche", []) if i in modul["items"]]      # Besorgungstasche (Teile)
    from . import vorlieben
    vorlieben.angleichen(z, modul)                                             # alte Spielstaende: leere Sammlung
    z["handy"] = [f for f in z.get("handy", []) if f.get("von") in modul["personen"]]
    from . import handy as _handy                       # 17.10.2026: ein Chat pro Frau (alte Spielstaende zusammenfuehren)
    _handy.zusammenfuehren(z)
    z.setdefault("chronik", [])
    if "bekannt" not in z:                               # 17.10.2026: Start-Bekannte + wer schon ein Gedaechtnis hat
        z["bekannt"] = list(modul.get("bekannt_start", []))
        bekannt_machen(z, [p for p in z.get("gedaechtnis", {}) if p in modul["personen"]])
        bekannt_machen(z, [p for p in ((z.get("szene") or {}).get("figuren") or []) if p in modul["personen"]])
    if "jobs_erfolg" not in z:                           # alte Spielstaende: erledigte Jobs zaehlen als gelungen
        z["jobs_erfolg"] = list(z.get("jobs_erledigt", []))
    for k in z["werte"]:
        if ist_achse(k):
            punkte(z, k)                                 # Punkte-Skala nachruesten (alte Spielstaende)
    if z.get("persona"):                                 # 19.10.2026: neue Attribute (strength) mit Startwert der Persona
        att = z["persona"].setdefault("attribute", {})
        vorlage = next((p for p in modul.get("personas", []) if p.get("id") == z["persona"].get("id")), None) or {}
        for a in modul.get("attribute", []):
            att.setdefault(a, (vorlage.get("attribute") or {}).get(a, 0))
    return json.dumps(z, sort_keys=True) != vorher


def neu_werte(modul):
    """Startwerte aller Werte des Moduls (wie in neu())."""
    out = {}
    for name, w in modul["werte"].items():
        start = w.get("start", {})
        for x in w.get("je", []) + w.get("paare", []):
            out["%s.%s" % (name, x)] = start.get(x, w["bereich"][0]) if isinstance(start, dict) else start
        if not w.get("je") and not w.get("paare"):
            out[name] = start if not isinstance(start, dict) else w["bereich"][0]
    return out
