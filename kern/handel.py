# -*- coding: utf-8 -*-
"""Geld, Laeden, Hehlerei, Geschenke und Jobs (16.10.2026).

Duc: Honorar jeden Tag aufs Konto, Geld verdienen mit kleinen Aufgaben, ein Hehler im Team (Toto).
Regeln stehen hier im Code, das Sprachmodell erzaehlt nur (Geschenke spielt die Figur in der Szene aus).
  Konto       z["konto"] in Euro, z["buchungen"]; Honorar am Tagesende (modul.geld.honorar).
  Laeden      Toto (immer, Sortiment wechselt taeglich, Preis je Draht zu ihm), Dorfladen (nur wenn heute an Land).
  Verkauf     Toto kauft Inventar zu 40 % (Yacht-Ware entfernt 29.10.2026: Hehlerei nur noch im Event br_crew_kasse).
  Schmuggel   maechtig beim Benutzen, aber je Tagesende kann Elsa (Kuestenwache) sie finden.
  Geschenke   in der Szene an eine anwesende Frau, eine pro Frau und Tag; Geschmack laut Item.
  Jobs        Schnelljobs im Handy: 1 Energie + W20-Probe, Lohn (Fehlschlag halb). Grosse Jobs sind Szenen
              (szenen.json, art "job") mit {"geld": N} in den Folgen.
  Missionen   (17.10.2026) = die Schnelljobs mit Gesicht: nur von Leuten, die Duc kennt (z["bekannt"]), Ketten
              (nach = erst nach Erfolg), Tagesangebot fest (4, davon mind. 2 von Frauen, je Person eine). Erfolg bei
              einer Frau: +6 Vertrauen/+4 Begehren (eine Wirkung je Frau und Tag), Patzer ab Tag 2: -4 Vertrauen.
              Jede Figur kommentiert mit festen, vertonten Saetzen (modul.job_zeilen, je 5 Erfolg/Fehlschlag)."""
import math, random

from . import chronik, kuechen, moral, regeln, rollen, tisch, vorlieben, wuerfel, zustand

INVENTAR_ARTEN = ("geschenk", "gluecksbringer", "schmuggel", "teil", "schluessel", "snack", "attribut", "werkzeug",
                  "kampf", "material")
# Teile (Missionsausbau 18.10.2026): Besorgungen fuer einen Auftrag. Keine eigene Wirkung, nicht verschenkbar, kaufbar
# nur, solange ein offener Auftrag sie braucht, und sie liegen in einer eigenen Besorgungstasche (nicht im Inventar,
# nicht in der Truhe). Wer ein Teil kauft, hoert dazu einen festen, vertonten Satz der Ladenfigur.
TASCHE_PLAETZE = 3
# Laden-Regeln (wechselnder Ausschnitt, Rabatte, Tageslimit, Essen ...) stehen in modul["laeden"] (rollen.py)
HANDEL_PUNKTE = 4             # Grundlagen: Handel +4 Vertrauen je Kauf (Laden mit handel_punkte), nur bis Stufe 3


def init(z, modul):
    if "konto" not in z:
        z["konto"] = (modul.get("geld") or {}).get("start", 0)
        z["buchungen"] = [{"tag": z["tag"], "text": "Startguthaben", "betrag": z["konto"]}]
    z.setdefault("gekauft_einmalig", [])
    z.setdefault("geschenke", {})             # pid -> Tag des letzten Geschenks
    z.setdefault("jobs_erledigt", [])


def euro(n):
    return ("%d" % n).replace("-", "−") + " €" if abs(n) < 1000 else "{:,}".format(n).replace(",", ".") + " €"


def buchen(z, betrag, text):
    z["konto"] = z.get("konto", 0) + int(betrag)
    z.setdefault("buchungen", []).append({"tag": z["tag"], "text": text, "betrag": int(betrag)})
    return "Money %s%s (%s)" % ("+" if betrag >= 0 else "−", euro(abs(int(betrag))), text)


def draht_faktor(z):
    return round(1.3 - 0.12 * z["werte"].get("draht", 1), 2)


def halb_plus(z, modul, wert, schritt=0.5):
    """Halber Punkt auf einen Wert (Rest gemerkt wie bei den Reaktionen) - fuer Ruf durch Geschenke ans Dorf."""
    rest = z.setdefault("neigung", {})
    neu = rest.get(wert, 0.0) + schritt
    ganz = int(neu)
    rest[wert] = round(neu - ganz, 2)
    return zustand.folgen_anwenden(z, modul, [{"wert": wert, "delta": ganz}]) if ganz else []


# Geschenke an Nebenfiguren (16.10.2026): jede Rolle reagiert anders - Personen-Felder geschenk_reaktion und
# bestechung (rollen.py).


def schenken_npc(z, modul, iid, pid):
    """-> (zeilen, auftrag) - Geschenk an eine Nebenfigur. Wer "bestechung" hat, lehnt Wertvolles ab (Gegenstand bleibt)."""
    if iid not in z["inventar"]:
        raise ValueError("That isn't in your bag.")
    it = modul["items"][iid]
    if "geschenk" not in it:
        raise ValueError("%s ist kein Geschenk." % it["label"])
    if z["geschenke"].get(pid) == z["tag"]:
        raise ValueError("You've already given this person something today.")
    name = modul["personen"][pid].get("kurz") or modul["personen"][pid]["name"].split()[0]
    z["geschenke"][pid] = z["tag"]
    best = rollen.person(modul, pid, "bestechung")
    if best and (it.get("preis") or 0) >= best["ab"]:
        zeilen = ["Gift: " + it["label"], "%s declines – it looks like a bribe" % name]
        zeilen += zustand.folgen_anwenden(z, modul, [{"wert": "ruf", "delta": -1},
                                                    {"codex": "%s noted your gift as an attempted bribe." % name}])
        return zeilen, best["regie"] % it["label"]
    z["inventar"].remove(iid)
    wert, auftrag = rollen.person(modul, pid, "geschenk_reaktion") or (None, "%s takes the gift and reacts in character." % name)
    zeilen = ["Gift: " + it["label"]]
    if "vertrauen." + pid in z["werte"]:
        # eden_rise (Grundlagen 17.10.2026): Geschenke an Nebenfiguren zaehlen auf IHR Vertrauen, nach Geschmack
        if it.get("nur_fuer") and it["nur_fuer"] != pid:
            z["inventar"].append(iid)
            z["geschenke"].pop(pid, None)
            return ["%s shakes her head: “That's not for me.”" % name], (
                "Duc offers her something that is clearly meant for someone else. She refuses it kindly.")
        w = geschenk_wirkung(modul, iid, pid)
        pts = NPC_PUNKTE.get(max(-1, min(3 if it.get("nur_fuer") == pid else 2, w)), 0)
        zeilen.append({2: "%s loves it", 1: "%s is pleased", 0: "%s accepts it politely", -1: "%s doesn't like it",
                       3: "%s is moved"}[max(-1, min(3 if it.get("nur_fuer") == pid else 2, w))] % name)
        zeilen += zustand.punkte_add(z, modul, "vertrauen." + pid, pts,
                                     deckel=zustand.GESPRAECH_DECKEL if 0 < pts <= 4 else None, quelle="geschenke")
        zeilen += _topf_kommentar(z, modul, pid, "vertrauen." + pid, pts)
        vorlieben.aus_geschenk(z, modul, pid, iid, w)        # Duc weiss jetzt, ob sie es mag (nur Wissen)
        if rollen.ist(modul, "haendler", pid):
            zeilen += draht_plus(z, modul)
        return zeilen, auftrag
    zeilen.append("%s accepts it" % name)
    if wert == "draht":
        zeilen += draht_plus(z, modul)
    elif wert == "ruf":
        zeilen += halb_plus(z, modul, "ruf")
    return zeilen, auftrag


NPC_PUNKTE = {3: 12, 2: 8, 1: 4, 0: 0, -1: -4}     # einzigartig / liebt / mag / neutral / mag nicht (Grundlagen)


# Haendler-Saetze (16.10.2026, seit 18.10. in den Moduldaten: laeden[<haendler>].haendler_zeilen/_gefuehl):
# feste Saetze - sofort da, vertonbar, je Draht-Stufe waermer. Englisch (Spielsprache).


def haendler_laden(modul):
    """Laden-Daten des Haendlers (rollen: haendler; Laden-ID = Personen-ID) oder {}."""
    return rollen.laden(modul, rollen.rolle(modul, "haendler"))


def haendler_zeile(modul, zid):
    """'gruss_kumpel.2' -> Text (fuer die Vertonung; nur feste Saetze des Haendlers, nie freier Text)."""
    gruppe, _, i = zid.partition(".")
    liste = (haendler_laden(modul).get("haendler_zeilen") or {}).get(gruppe) or []
    return liste[int(i)] if i.isdigit() and int(i) < len(liste) else None


def _gefuehl(hl, gruppe, i):
    """Sprite-Gefuehl eines Satzes: haendler_gefuehl[gruppe] ist ein Wort oder eine Liste passend zu den Saetzen."""
    g = (hl.get("haendler_gefuehl") or {}).get(gruppe)
    if isinstance(g, list):
        g = g[i] if i < len(g) else None
    return g or "neutral"


def _wechsel(z, gruppe, laenge):
    """Satz der Gruppe fuer diesen Besuch: je acht Besuche (Phasen) einmal jeder Satz, in gemischter Reihenfolge."""
    try:
        s = z["tag"] * len(z["phasen"]) + z["phasen"].index(z["phase"])
    except (KeyError, ValueError):
        s = z.get("tag", 1)
    rng = random.Random("%s-%s" % (z["id"], gruppe))
    schritt = rng.choice([k for k in range(1, laenge) if math.gcd(k, laenge) == 1] or [1])
    return (rng.randrange(laenge) + s * schritt) % laenge       # Schritt teilerfremd: kein Satz kehrt innerhalb einer Runde wieder


def haendler_auftritt(z, modul):
    """Je Stimmung ein Satz. Gruss nach Vertrauen 0-5 (gruss_0 .. gruss_5, wechselt ohne Wiederholung); die anderen
    Saetze wechseln mit jedem Besuch (Tag, Phase, Zahl der Buchungen)."""
    hl = haendler_laden(modul)
    zeilen = hl.get("haendler_zeilen") or {}
    hid = rollen.rolle(modul, "haendler")
    v = max(0, min(5, int(z["werte"].get("vertrauen." + str(hid), 0))))
    if "gruss_%d" % v in zeilen:
        stufe = "gruss_%d" % v
    else:                                   # aeltere Module: Draht in drei Stufen
        d = z["werte"].get("draht", 1)
        stufe = "gruss_fremd" if d <= 1 else "gruss_kumpel" if d <= 3 else "gruss_familie"
    rng = random.Random("%s-%d-%s-%d" % (z["id"], z["tag"], z["phase"], len(z.get("buchungen", []))))
    out = {}
    for stimmung, gruppe in (("gruss", stufe), ("kauf", "kauf"), ("verkauf", "verkauf"), ("pleite", "pleite")):
        n = len(zeilen[gruppe])
        i = _wechsel(z, gruppe, n) if stimmung == "gruss" and n > 1 else rng.randrange(n)
        out[stimmung] = {"id": "%s.%d" % (gruppe, i), "text": zeilen[gruppe][i], "gefuehl": _gefuehl(hl, gruppe, i)}
    return out


def kauf_reaktion(z, modul, laden, iid):
    """Satz des Haendlers nach dem Kauf: je Kategorie (Geschenke) oder Art; bei Geschenken mit etwa 40 % Chance ein
    Hinweis, wer es moegen koennte - immer wahr (Wertung >= 1), Duc 26.10.2026. None, wenn der Haendler nichts dazu hat."""
    if not rollen.ist(modul, "haendler", laden):
        return None
    hl = haendler_laden(modul)
    zeilen = hl.get("haendler_zeilen") or {}
    it = modul["items"].get(iid) or {}
    kat = it.get("kat") if it.get("art") == "geschenk" else None
    nr = len(z.get("buchungen", []))
    rng = random.Random("%s-%s-%s-%d" % (z["id"], "kauf", iid, nr))
    gruppe = None
    if kat and rng.random() < 0.4:
        wer = sorted((w, p) for p, w in (it.get("geschenk") or {}).items()
                     if w >= 1 and "hinweis_%s_%s" % (kat, p) in zeilen)
        if wer:
            topf = [p for w, p in wer for _ in range(2 if w >= 2 else 1)]      # wer es liebt, wird oefter genannt
            gruppe = "hinweis_%s_%s" % (kat, rng.choice(topf))
    if gruppe is None:
        art = it.get("art")
        for g in ("kauf_" + str(kat), "kauf_" + str(art), "kauf_kampf" if art == "material" else "", "kauf"):
            if g in zeilen:
                gruppe = g
                break
    if gruppe is None:
        return None
    i = rng.randrange(len(zeilen[gruppe]))
    return {"id": "%s.%d" % (gruppe, i), "text": zeilen[gruppe][i], "gefuehl": _gefuehl(hl, gruppe, i)}


def draht_plus(z, modul, halb=True):
    """Jeder Handel mit dem Haendler bringt einen halben Punkt Draht (Rest gemerkt wie bei den Reaktionen)."""
    rest = z.setdefault("neigung", {})
    neu = rest.get("draht", 0.0) + (0.5 if halb else 1.0)
    ganz = int(neu)
    rest["draht"] = round(neu - ganz, 2)
    return zustand.folgen_anwenden(z, modul, [{"wert": "draht", "delta": ganz}]) if ganz else []


def an_land(z, modul):
    orte = [h.get("ort") for h in z.get("heute", [])] + [((z.get("szene") or {}).get("def") or {}).get("ort")]
    return any(o and "(ashore)" in modul["raeume"].get(o, {}).get("label", "") for o in orte)


def preis(z, modul, iid, laden):
    """Ladenpreis. Tagesbonus aus dem Essen (kern/kuechen.py, Akzent Zitronen): Preise -x %."""
    p = _preis(z, modul, iid, laden)
    w = kuechen.bonus(z, "preis")
    return max(1, int(round(p * (100 - w) / 100.0))) if w else p


def _preis(z, modul, iid, laden):
    it = modul["items"][iid]
    basis = (it.get("preise") or {}).get(laden, it["preis"])
    l = rollen.laden(modul, laden)
    vertrauen = z["werte"].get("vertrauen." + l.get("wer", laden), 0)
    if rollen.ist(modul, "haendler", laden):
        return int(round(basis * draht_faktor(z) / 5.0) * 5)
    r = l.get("rabatt_ab_vertrauen")                        # z. B. Eden-Shop: Rabatt ab Megans Vertrauen 3
    if r and vertrauen >= r[0]:
        return int(round(basis * r[1] / 5.0) * 5)
    if l.get("rabatt_je_stufe") or l.get("aufschlag"):     # z. B. Alva: je Stufe ueber 1 guenstiger, Diesel teurer
        je, ab = l.get("rabatt_je_stufe") or [0, 0]
        rabatt = je * max(0, vertrauen - ab)
        p = basis * (l.get("aufschlag") or {}).get(iid, 1.0) * (1 - rabatt)
        return max(1, int(round(p / 5.0) * 5)) if basis >= 10 else basis
    return basis


def kueche(modul):
    """Der Laden mit essen=True (Kombuese) oder {} - sein "wer" kocht, ab "zweites_essen_ab" gibt es zwei Essen."""
    return next((l for l in (modul.get("laeden") or {}).values() if l.get("essen")), {})


def essen_extra(z, modul):
    k = kueche(modul)
    return 1 if k and z["werte"].get("vertrauen." + k.get("wer", ""), 0) >= k.get("zweites_essen_ab", 99) else 0


def essen_frei(z, modul):
    """Kombuese: ein Essen am Tag, ab Vertrauen der Koechin (zweites_essen_ab) zwei (Snack oder selbst gekocht)."""
    regeln = (modul.get("essen") or {"pro_tag": 1})
    pro_tag = regeln.get("pro_tag", 1) + essen_extra(z, modul)
    return essen_heute(z)["anzahl"] < pro_tag


def granaten_frei(z):
    """Rosi baut Granaten erst in der reparierten Werkstatt (Flag werkstatt_offen, Tag 8; Testschalter oeffnet sie auch)."""
    from . import kampf
    return "werkstatt_offen" in z.get("flags", []) or bool(kampf.progress(z).get("test"))


def laden_offen(z, l):
    """Laden mit "bedingung" gibt es erst, wenn sie gilt (Danzels Laden nach dem Red Trio, Duc 30.10.2026)."""
    return not l.get("bedingung") or regeln.gilt(l["bedingung"], z)


def _umgezogen(z, modul, laden):
    """Ware eines Ladens mit "uebernimmt": die anderen Laeden verkaufen sie nicht mehr, sobald er offen ist."""
    out = set()
    for k, l in (modul.get("laeden") or {}).items():
        if k != laden and l.get("uebernimmt") and laden_offen(z, l):
            out.update(l["uebernimmt"])
    return out


def sortiment(z, modul, laden):
    l = modul["laeden"][laden]
    if not laden_offen(z, l):
        return None
    if l.get("nur_an_land") and not an_land(z, modul):
        return None
    if l.get("erst_bekannt") and l.get("wer") not in (z.get("bekannt") or []):     # Isabelle erst nach dem Kennenlernen
        return None
    if z.get("tag", 1) < l.get("ab_tag", 0):          # Eden-Shop erst ab Akt 2 (Duc 27.10.2026)
        return None
    wer = l.get("wer")
    weg = _umgezogen(z, modul, laden)
    ids = [i for i, it in modul["items"].items() if laden in (it.get("wo") or []) and i not in weg
           and (not it.get("wenn") or regeln.gilt(it["wenn"], z))         # Ware mit Bedingung (Stoff, Duc 30.10.2026)
           and not it.get("pausiert")                       # ruht bis spaeter (E-076: Diesel/Strom bis Akt 2)
           and not (it.get("einmalig") and i in z["gekauft_einmalig"])
           and (not wer or z["werte"].get("vertrauen." + wer, 0) >= (it.get("ab") or {}).get(laden, 0))
           and not (rollen.ist(modul, "haendler", laden)
                    and z["werte"].get("draht", 0) < (it.get("ab") or {}).get(laden, 0))]
    if not granaten_frei(z):                             # Rosis Granaten erst mit der reparierten Werkstatt (Akt 2)
        ids = [i for i in ids if not (modul["items"][i].get("kampf") or {}).get("granate")]
    for iid, schl in (l.get("tageslimit") or {}).items():     # z. B. unter der Theke: ein Kanister am Tag
        if z.get(schl) == z["tag"]:
            ids = [i for i in ids if i != iid]
    if l.get("essen") and not essen_frei(z, modul):
        return None                                    # heute schon gegessen - die Kombuese sagt es dir
    if not essen_frei(z, modul):                         # Einzelne Mahlzeit in einem Laden (Ba Tus Schale): zaehlt als Essen des Tages
        ids = [i for i in ids if not modul["items"][i].get("essen")]
    fest = [i for i in ids if i in (l.get("fest") or [])]   # feste Ware: immer im Angebot, zaehlt nicht zur Rotation
    ids = [i for i in ids if i not in fest]
    if l.get("wechselnd"):
        rng = random.Random("%s-%d-%s" % (z["id"], z["tag"], laden))
        immer = [i for i in ids if i in (l.get("immer") or [])]
        rest = [i for i in ids if i not in immer]
        rng.shuffle(rest)
        ids = immer + rest[:max(0, l.get("sortiment", 6) - len(immer))]
        special = rest[0] if rest and l.get("sonderangebot") else None
    else:
        special = None
    ids += fest
    ids = [i for i in ids if modul["items"][i].get("art") != "teil"]
    gebraucht = teile_gebraucht(z, modul)                 # Teile stehen ausserhalb der Rotation, solange gebraucht
    ids += [i for i, it in modul["items"].items() if it.get("art") == "teil" and laden in (it.get("wo") or [])
            and i in gebraucht and i not in tasche(z)]
    out = []
    for i in ids:
        it, p = modul["items"][i], preis(z, modul, i, laden)
        if i == special:
            p = int(round(p * 0.75 / 5.0) * 5)
        out.append({"id": i, "label": it["label"], "text": it.get("text", ""), "wirkung_text": it.get("wirkung_text"), "art": it["art"], "preis": p,
                    "special": i == special,
                    "im_inventar": (i in z["inventar"] and zustand.stapel(modul, i) == 1) or i in tasche(z),
                    "anzahl": z["inventar"].count(i), "stapel": zustand.stapel(modul, i),      # Stapeln (28.10.2026)
                    "intim": it.get("intim"), "fuer": gebraucht.get(i, "")})
    return out


def tasche(z):
    """Besorgungstasche: Teile fuer offene Auftraege, 3 Plaetze, getrennt vom Inventar."""
    return z.setdefault("tasche", [])


def jobs_aktiv(modul):
    """Schnelljobs (Handy-Reiter Jobs). eden_rise hat sie am 29.10.2026 abgeschaltet - die Favours ersetzen sie
    (modul["schnelljobs"] = False, gesetzt in modul_eden_rise.py). Ohne Eintrag laufen sie wie bisher; die Daten
    (missionen.json) und der ganze Code bleiben, damit sich das umkehren laesst."""
    return modul.get("schnelljobs", True)


def teile_gebraucht(z, modul, V=None):
    """{teil_id: Name der Auftraggeberin} fuer alle offenen Auftraege, die ein Teil brauchen."""
    if not jobs_aktiv(modul):
        return {}
    from . import showrunner
    V = V or showrunner.vorrat(_moddir(z))
    out = {}
    t = z.get("jobs_tag") or {}
    offen = set(offene_auftraege(z, modul, V)) | set(t.get("ids", []) if t.get("tag") == z["tag"] else [])
    for j in (V or {}).get("jobs", []):
        b = j.get("braucht")
        if b and modul["items"].get(b, {}).get("art") == "teil" and j["id"] in offen and job_frei(z, modul, j):
            out.setdefault(b, anzeigename(modul, j["von"]))
    return out


def _moddir(z):
    import os
    return (z.get("plan") or {}).get("_moddir") or os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "module", z.get("modul", ""))


def offene_auftraege(z, modul, V):
    """Angenommene Auftraege: einmal angebotene Besorgungen und die Fortsetzungen begonnener Ketten - sie bleiben
    sichtbar, bis sie erledigt sind (sonst kauft man ein Teil und der Auftrag ist am naechsten Tag weg)."""
    if not jobs_aktiv(modul):
        return []
    jobs = {j["id"]: j for j in (V or {}).get("jobs", [])}
    return [jid for jid in z.get("auftraege", []) if jid in jobs and job_frei(z, modul, jobs[jid])]


def platz_frei(z, modul):
    return zustand.belegt(z, modul) < zustand.inventar_plaetze(z, modul)


# ------------------------------------------------------------------ Tasche bei Rosi (Duc 29.10.2026, beute.md 5)
def _tasche_fehlt(z, modul, k):
    """English reason why Rosi can't sell the next bag now, else None."""
    t = modul["tasche"]
    if t.get("flag") and t["flag"] not in z.get("flags", []):
        return t.get("text_zu") or "The workshop is still wrecked."
    if z.get("tag", 1) < k.get("ab_tag", 1):
        return k.get("text_frueh") or "Rosi is still working on it."
    if z.get("konto", 0) < k["geld"]:
        return "You're %d € short." % (k["geld"] - z.get("konto", 0))
    return None


def tasche_ansicht(z, modul):
    """Bag block for Rosi's workshop: slots now, the next upgrade (label, slots, price, why not) or None when maxed."""
    t = modul.get("tasche")
    if not t:
        return None
    st, stufen = z.get("tasche_stufe", 0), t.get("stufen") or []
    k = stufen[st] if st < len(stufen) else None
    return {"plaetze": zustand.inventar_plaetze(z, modul), "stufe": st, "stufe_max": len(stufen),
            "naechste": ({"label": k["label"], "plaetze": k["plaetze"], "geld": k["geld"], "text": k.get("text", ""),
                          "bild": k.get("bild"), "fehlt": _tasche_fehlt(z, modul, k)} if k else None)}


def tasche_kaufen(z, modul):
    """Rosi sews the next bag: money only, ready at once, no action. -> (title, Rosi's line, result lines)."""
    t = modul.get("tasche") or {}
    st, stufen = z.get("tasche_stufe", 0), t.get("stufen") or []
    if st >= len(stufen):
        raise ValueError("Your bag can't get any bigger.")
    k = stufen[st]
    grund = _tasche_fehlt(z, modul, k)
    if grund:
        raise ValueError(grund)
    zeile = buchen(z, -k["geld"], k["label"])
    z["tasche_stufe"] = st + 1
    return k["label"], k.get("satz", ""), [zeile, "🎒 Bag: %d slots" % k["plaetze"]]


def kaufen(z, modul, laden, iid):
    ware = next((w for w in (sortiment(z, modul, laden) or []) if w["id"] == iid), None)
    if not ware:
        raise ValueError("That isn't on sale here right now.")
    it = modul["items"][iid]
    if z["konto"] < ware["preis"]:
        raise ValueError("Not enough money: you have %s, %s costs %s." % (euro(z["konto"]), it["label"], euro(ware["preis"])))
    teil = it["art"] == "teil"
    lagern = it["art"] in INVENTAR_ARTEN and not teil
    if lagern and iid in z["inventar"] and zustand.stapel(modul, iid) == 1:     # Stapelbares darf mehrfach (28.10.2026)
        raise ValueError("You already have %s." % it["label"])
    if lagern and not zustand.platz_fuer(z, modul, iid):
        raise ValueError("Inventory full (%d slots) – sell or give something away first." % zustand.inventar_plaetze(z, modul))
    if teil and iid in tasche(z):
        raise ValueError("%s is already in your errand bag." % it["label"])
    if teil and len(tasche(z)) >= TASCHE_PLAETZE:
        raise ValueError("Your errand bag is full (3 places) – hand something over first.")
    l = modul["laeden"][laden]
    wer = l.get("wer")
    if l.get("essen") and not essen_frei(z, modul):
        raise ValueError("You've already eaten today – %s will feed you again tomorrow." % anzeigename(modul, wer))
    zeilen = [buchen(z, -ware["preis"], "%s: %s" % (l["name"], it["label"]))]
    if l.get("essen") or it.get("essen"):
        essen_heute(z)["anzahl"] += 1
    if (l.get("tageslimit") or {}).get(iid):
        z[l["tageslimit"][iid]] = z["tag"]
    if l.get("handel_punkte") and wer:
        zeilen += zustand.punkte_add(z, modul, "vertrauen." + wer, HANDEL_PUNKTE, deckel=zustand.GESPRAECH_DECKEL, quelle="geschenke")
    if wer and rollen.ist(modul, "dorfohr", wer):            # beim Einkauf plaudert das Dorfohr (einmal am Tag)
        vorlieben.tratsch(z, modul, "laden")
    if it.get("einmalig"):
        z["gekauft_einmalig"].append(iid)
    if it.get("rohstoff"):                                   # Stoff und Wolle landen bei den Rohstoffen, nicht in der Tasche
        kuechen.rohstoff_add(z, it["rohstoff"], 1)
        zeilen.append("Added to your materials: " + it["label"])
    elif it.get("zutat"):                                    # Ba Tus Ware: gekauft = ein Stern, wie bei Nonna
        kuechen.vorrat_add(z, it["zutat"], 1)
        zeilen.append("Added to your pantry: " + it["label"])
    elif teil:
        tasche(z).append(iid)
        zeilen.append("In your errand bag: %s (for %s)" % (it["label"], teile_gebraucht(z, modul).get(iid, "a job")))
    elif lagern:
        z["inventar"].append(iid)
        zeilen.append("New in your bag: " + it["label"])
    else:
        zeilen += zustand.folgen_anwenden(z, modul, moral.als(it.get("wirkung", []), "alltag"))
    if rollen.ist(modul, "haendler", laden):
        zeilen += draht_plus(z, modul)
    return zeilen


def ankauf(z, modul):
    """Was der Haendler dir abkauft: Inventar (ausser Beweise/Schluessel/Startausruestung). Ohne Haendler: nichts."""
    l = haendler_laden(modul)
    if not l:
        return []
    start = (z.get("persona") or {}).get("start_items", [])
    out = []
    for iid in z["inventar"]:
        it = modul["items"].get(iid, {})
        if it.get("preis") and iid not in start:
            out.append({"art": "item", "id": iid, "label": it["label"],
                        "preis": int(it["preis"] * l.get("ankauf", 0.4) * (100 + kuechen.bonus(z, "ankauf")) / 100.0)})   # Akzent Sojasauce
    return out


def verkaufen(z, modul, art, vid):
    w = next((x for x in ankauf(z, modul) if x["art"] == art and x["id"] == vid), None)
    if not w:
        raise ValueError("%s can't buy that from you right now." % anzeigename(modul, rollen.rolle(modul, "haendler")))
    z["inventar"].remove(vid)
    return [buchen(z, w["preis"], "an %s: %s" % (anzeigename(modul, rollen.rolle(modul, "haendler")), w["label"]))] \
        + draht_plus(z, modul)


def tagesende(z, modul):
    """Honorar, dann: findet jemand Schmuggelware?"""
    init(z, modul)
    g = modul.get("geld") or {}
    zeilen = [buchen(z, g["honorar"], g.get("honorar_text", "Honorar"))] if g.get("honorar") else []
    rng = random.Random("%s-%d-ende" % (z["id"], z["tag"]))
    for iid in [i for i in z["inventar"] if modul["items"].get(i, {}).get("art") == "schmuggel"]:
        if rng.random() < modul.get("schmuggel_risiko", 0.2):
            z["inventar"].remove(iid)
            label = modul["items"][iid]["label"]
            zeilen.append("⚠ Lieutenant Ferrandi found %s during a check – confiscated." % label)
            zeilen += zustand.folgen_anwenden(z, modul, [{"wert": "ruf", "delta": -2}, {"codex": "Confiscated: " + label}])
    # Truhe in Ducs Kabine (17.10.2026): die Kabine des Kommandanten wird seltener durchsucht
    faktor = (modul.get("kabine") or {}).get("schmuggel_faktor", 0.5)
    for iid in [i for i in z.get("truhe", []) if modul["items"].get(i, {}).get("art") == "schmuggel"]:
        if rng.random() < modul.get("schmuggel_risiko", 0.2) * faktor:
            z["truhe"].remove(iid)
            label = modul["items"][iid]["label"]
            zeilen.append("⚠ Lieutenant Ferrandi found %s in the chest in your cabin – confiscated." % label)
            zeilen += zustand.folgen_anwenden(z, modul, [{"wert": "ruf", "delta": -2}, {"codex": "Confiscated: " + label}])
    return zeilen + _gras_kontrolle(z, modul, rng, faktor)


# ------------------------------------------------------------------ Gras-Kuchen (Duc 27.10.2026)
def _gras_kontrolle(z, modul, rng, faktor):
    """Je Tagesende: Ferrandi findet einen Gras-Kuchen (Inventar "risiko", Truhe mal faktor) - beschlagnahmt, Ruf."""
    c, zeilen = modul.get("gras") or {}, []
    for ort, f, text in (("inventar", 1.0, "fund"), ("truhe", faktor, "fund_truhe")):
        for iid in [i for i in z.get(ort, []) if modul["items"].get(i, {}).get("gras")]:
            if rng.random() < c.get("risiko", 0.1) * f:
                z[ort].remove(iid)
                label = modul["items"][iid]["label"]
                zeilen.append(c.get(text, "⚠ Ferrandi found %s.") % label)
                zeilen += zustand.folgen_anwenden(z, modul, [{"wert": "ruf", "delta": c.get("ruf", -1)},
                                                             {"codex": "Confiscated: " + label}])
    return zeilen


def gras_gegessen(z, modul, iid):
    """Ein Gras-Kuchen wurde gegessen (Inventar oder Kampf): Kater fuer morgen merken. Keine Moral - was Duc selbst
    isst, wirkt nur auf ihn (Duc 27.10.2026)."""
    if (modul["items"].get(iid) or {}).get("gras"):
        z["kater_tag"] = z["tag"]
    return []


def kater(z, modul):
    """Am Morgen nach einem Gras-Kuchen: einmal Energie -1 (egal wie viele es waren)."""
    if z.get("kater_tag") is None or z["kater_tag"] >= z["tag"]:
        return []
    z.pop("kater_tag")
    return [(modul.get("gras") or {}).get("kater", "😵 Still a little floaty.")] + \
        zustand.folgen_anwenden(z, modul, [{"wert": "energie", "delta": -1}])


# ------------------------------------------------------------------ Benutzen und Schenken
def benutzen(z, modul, iid):
    if iid not in z["inventar"]:
        raise ValueError("That isn't in your bag.")
    it = modul["items"][iid]
    if (it.get("kampf") or {}).get("pflege"):          # Waffenpflege vor dem Kampf (27.10.2026): wirkt im naechsten Kampf
        from . import kampf
        return kampf.pflege_vorbereiten(z, modul, iid)
    if not it.get("benutzen") and it.get("art") == "verbrauch" and _ohne_moral(it.get("wirkung")):
        return _verbrauchen(z, modul, iid, it)
    if not it.get("benutzen"):
        raise ValueError("%s kann man nicht benutzen - nur tragen oder verschenken." % it["label"])
    z["inventar"].remove(iid)
    return ["Benutzt: " + it["label"]] + zustand.folgen_anwenden(z, modul, moral.als(it["benutzen"], "genau")) \
        + gras_gegessen(z, modul, iid)


def _verbrauchen(z, modul, iid, it):
    """Verbrauchsware aus dem Inventar (Energy Bar, Doppio ...) wirkt wie beim Kauf - nie auf die Moral: Konsum hebt die
    Crew-Stimmung nicht, Moral aus Essen gibt es nur durchs Kochen fuer die Crew (Duc 27.10.2026)."""
    z["inventar"].remove(iid)
    return ["Benutzt: " + it["label"]] + zustand.folgen_anwenden(z, modul, _ohne_moral(it["wirkung"]))


def _ohne_moral(folgen):
    return [f for f in folgen or [] if f.get("wert") != moral.KEY]


def _topf_kommentar(z, modul, pid, key, pts):
    """Topf voll: Sie sagt es in ihrer Art (Duc 02.11.2026), die Zahlen bleiben unsichtbar."""
    if pts <= 0 or zustand.topf_platz(z, modul, key, "geschenke") != 0:
        return []
    from . import figurenrahmen
    return figurenrahmen.topf_kommentar(z, modul, pid, key, "geschenke")


def geschenk_wirkung(modul, iid, pid):
    g = modul["items"][iid].get("geschenk") or {}
    return g.get(pid, g.get("*", 0))


def schenken(z, modul, iid, pid):
    """-> (zeilen, wertung) - wertung 2/1/0/-1 fuer den Erzaehlauftrag."""
    if iid not in z["inventar"]:
        raise ValueError("That isn't in your bag.")
    it = modul["items"][iid]
    if "geschenk" not in it:
        raise ValueError("%s isn't a gift." % it["label"])
    if z["geschenke"].get(pid) == z["tag"]:
        raise ValueError("She has already had a gift from you today.")
    if it.get("nur_fuer") and it["nur_fuer"] != pid:
        raise ValueError("%s is meant for someone else – she can tell straight away." % it["label"])
    w, grund = geschenk_wirkung(modul, iid, pid), None
    schwelle = it.get("intim")
    if schwelle:
        andere = [p for p in ((z.get("szene") or {}).get("figuren") or []) if p != pid and p != "erzaehler"]
        if andere:
            grund = "vor_anderen"
        elif rollen.vergeben(z, modul, pid):
            grund = "vergeben"
        elif any(z["werte"].get("%s.%s" % (k, pid), 0) < v for k, v in schwelle.items()):
            grund = "zu_frueh"
        if grund:
            w = -1
    z["inventar"].remove(iid)
    z["geschenke"][pid] = z["tag"]
    folgen = {2: [{"wert": "vertrauen." + pid, "delta": 1}, {"wert": "begehren." + pid, "delta": 1}],
              1: [],                                    # "freut sich": kleine Wirkung, unten als Punkte bis Stufe 3
              0: [], -1: [{"wert": "vertrauen." + pid, "delta": -1}]}[max(-1, min(2, w))]
    name = modul["personen"][pid]["name"].split()[0]
    kopf = {2: "%s loves it" % name, 1: "%s is pleased" % name, 0: "%s accepts it politely" % name,
            -1: "It's too much for %s" % name}[max(-1, min(2, w))]
    if grund:
        kopf = {"vor_anderen": "%s is embarrassed in front of the others" % name,
                "vergeben": "%s is still with Yasin" % name,
                "zu_frueh": "Too soon – %s is caught off guard" % name}[grund]
    extra = zustand.punkte_add(z, modul, "vertrauen." + pid, 4, deckel=zustand.GESPRAECH_DECKEL, quelle="geschenke") if w == 1 and not grund else []
    if not grund:                                           # peinlich/zu frueh sagt nichts ueber ihren Geschmack
        vorlieben.aus_geschenk(z, modul, pid, iid, w)
    wirkung = zustand.folgen_anwenden(z, modul, folgen, frei=False, quelle="geschenke")
    if w > 0 and not grund:
        extra += _topf_kommentar(z, modul, pid, "vertrauen." + pid, 1)
    return ["Gift: " + it["label"], kopf] + wirkung + extra, (grund or w)


GESCHENK_AUFTRAG = {
    "vor_anderen": "It is far too intimate to give in front of other people - she is mortified, hides it fast and "
                   "makes him feel it, in character.",
    "vergeben": "She is still with Yasin. A gift this intimate crosses a line for her right now - she refuses it, "
                "flustered and a little hurt, in character.",
    "zu_frueh": "It is much too early and too intimate for where they are - she is caught off guard, embarrassed or "
                "offended, and makes that clear in character. No touching follows from it.",
    2: "She loves it - it is exactly her taste and it shows that he noticed who she is.",
    1: "She likes it and is pleased, a little surprised.",
    0: "It is not really her thing; she is polite about it.",
    -1: "It misses her completely - too flashy or too much; she is a little put off, but stays polite.",
}


# ------------------------------------------------------------------ Schnelljobs
def persona_vorteil(z, art):
    """Hat Ducs Persona diesen Vorteil ("handwerk", "kueche")? Alte Spielstaende tragen noch die Persona-Kopie mit
    id "tueftler" und ohne Liste - die zaehlt wie "handwerk" (17.10.2026, Persona heisst jetzt ESG-Berater)."""
    p = z.get("persona") or {}
    return art in (p.get("vorteile") or []) or (art == "handwerk" and p.get("id") == "tueftler")


# ------------------------------------------------------------------ Kochen (17.10.2026, eden_rise)
KOCH_LEITER = ["ekel", "fade", "normal", "gut", "liebt"]


def essen_heute(z):
    """Zaehler fuer das Essen des Tages: {"tag", "anzahl", "moral"} - Snacks (handel.essen, Phase B) und Kochen teilen ihn."""
    t = z.get("essen_tag") or {}
    if t.get("tag") != z["tag"]:
        t = z["essen_tag"] = {"tag": z["tag"], "anzahl": 0, "moral": 0}
    return t


def koch_stufe(item, pid, schon_voll, ergebnis):
    """Stufe eines Gerichts fuer eine Person: Geschmack, dann Wurf (kritisch +1, Fehlschlag/Patzer -1).
    Das Lieblingsgericht wirkt je Person einmal voll, danach wie "gut"."""
    if pid in (item.get("hasst") or []):
        i = 0
    elif pid in (item.get("liebt") or []):
        i = 3 if schon_voll else 4
    elif pid in (item.get("mag") or []):                      # Baukasten (kern/kuechen.py): Haupt trifft ihren Geschmack
        i = 3
    elif pid in (item.get("mag_nicht") or []):                # Baukasten: Haupt mag sie nicht (lustlos, kein Ekel)
        i = 1
    else:
        i = 2
    if ergebnis == "kritisch":
        i += 1
    elif ergebnis in ("fehlschlag", "patzer"):
        i -= 1
    return KOCH_LEITER[max(0, min(len(KOCH_LEITER) - 1, i))]


def kochen(z, modul, item, regeln, fuer, anwesend=()):
    """Duc kocht ein Gericht (item aus gegenstaende.json, regeln = gegenstaende["kochen"]).
    fuer = Person-ID (ein Teller fuer sie) oder "crew" (alle Anwesenden). -> {"probe", "stufen", "zeilen"}
    Probe: Perception (Abschmecken, Timing) gegen das SG des Gerichts, mit dem Kuechen-Vorteil der Persona."""
    t = essen_heute(z)
    pro_tag = regeln.get("pro_tag", 1) + essen_extra(z, modul)
    if t["anzahl"] >= pro_tag:
        raise ValueError("You've already cooked or eaten today.")
    vorteil = persona_vorteil(z, regeln.get("vorteil", "kueche"))
    sg = (item.get("wirkung") or {}).get("sg", 10)
    att = z["persona"]["attribute"].get("perception", 0) if z.get("persona") else 0
    from . import charms
    p = wuerfel.probe("perception", sg, [("Perception", att)] + charms.boni(z, "perception"), vorteil=vorteil)
    t["anzahl"] += 1
    voll = z.setdefault("koch_liebt", [])
    st = regeln["stufen"]
    zeilen, stufen = [], {}
    crew = fuer == "crew"
    # Teamessen = Breite: alle Anwesenden +2 (Meisterwerk +3, misslungen +1), wer es hasst isst Brot (0); das volle
    # "liebt" gibt es nur beim Teller fuer eine Person (Tiefe) - sonst waere das Teamessen immer besser.
    crew_v = regeln.get("crew_punkte", 2) + {"kritisch": 1, "fehlschlag": -1, "patzer": -1}.get(p["ergebnis"], 0)
    for pid in (list(anwesend) if crew else [fuer]):
        deckel = min(regeln.get("deckel", 36), zustand.GESPRAECH_DECKEL)   # alles zaehlt nur bis zum Deckel ...
        if crew:
            stufe = "fade" if pid in ((item.get("hasst") or []) + (item.get("mag_nicht") or [])) else "crew"
            v, b = (0, 0) if stufe == "fade" else (crew_v + (1 if pid in (item.get("mag") or []) else 0), 0)
        else:
            stufe = koch_stufe(item, pid, pid in voll, p["ergebnis"])
            v, b = st[stufe]
            if stufe == "liebt" and pid not in voll:   # ... ausser dem ersten "liebt" (wie ein Geschenk, das sie liebt)
                voll.append(pid)
                deckel = None
        stufen[pid] = stufe
        zeilen += zustand.punkte_add(z, modul, "vertrauen." + pid, v, deckel=deckel, quelle="geschenke")
        if b and ("begehren." + pid) in z["werte"]:
            zeilen += zustand.punkte_add(z, modul, "begehren." + pid, b, deckel=deckel, quelle="geschenke")
    if crew and t["moral"] < regeln.get("moral_max_tag", 1):
        t["moral"] += 1
        zeilen += zustand.folgen_anwenden(z, modul, [moral.folge(regeln.get("crew_moral", 1), "alltag")])
    return {"probe": p, "stufen": stufen, "zeilen": zeilen}


JOBS_PRO_TAG = 4
FRAUEN_MIN = 2
MISSION_VERTRAUEN, MISSION_BEGEHREN, MISSION_PATZER = 6, 4, -4


MISSION_VERSUCHE = 2          # Fehlschlag: morgen noch einmal; nach dem zweiten Fehlschlag halber Lohn, dann weg


def job_fehl(z, jid):
    return (z.get("jobs_fehl") or {}).get(jid) or {}


def job_frei(z, modul, j):
    """Kann diese Mission heute angeboten werden? (Tage, nicht erledigt, Person bekannt, Kette, Vertrauen, Gruppe,
    heute nicht schon misslungen)"""
    if not (j["tage"][0] <= z["tag"] <= j["tage"][1]) or j["id"] in z["jobs_erledigt"]:
        return False
    if job_fehl(z, j["id"]).get("tag") == z["tag"]:
        return False
    if j.get("gruppe") and j["gruppe"] in z.get("gruppen_erledigt", []):
        return False
    if modul["personen"].get(j["von"]) is None:
        return False
    if j["von"] not in (z.get("bekannt") or modul.get("bekannt_start") or modul["personen"]):
        return False
    if j.get("nach") and j["nach"] not in z.get("jobs_erfolg", []) and j["nach"] not in z.get("gruppen_erledigt", []):
        return False                                       # nach = Mission-ID oder Gruppe (irgendein Weg geschafft)
    return z["werte"].get("vertrauen." + j["von"], 99) >= j.get("ab_vertrauen", 0)


def jobs_angebot(z, modul, V, schreiben=True):
    """Festes Tagesangebot (17.10.2026) - frueher rueckte nach jedem erledigten Job ein neuer nach. Wird am Tag
    einmal gezogen; wer heute erst kennengelernt wird, bietet ab morgen etwas an. Mehrere Wege (gruppe) zaehlen als
    ein Angebot: wird einer gezogen, kommen die anderen offenen Wege der Gruppe dazu (18.10.2026).
    schreiben=False: nur ausrechnen, den Spielstand nicht anfassen (Anzeige, GET /api/stand)."""
    if not V or not V.get("jobs") or not jobs_aktiv(modul):
        return []
    t = z.get("jobs_tag") or {}
    if t.get("tag") == z["tag"]:
        if schreiben:
            annehmen(z, modul, V, t["ids"])
        return t["ids"]
    # wer Duc schon einen Auftrag gegeben hat, kennt ihn (alte Spielstaende: Dorf-Jobs ohne gemeinsame Szene)
    auftraggeber = [j["von"] for j in V["jobs"] if j["id"] in z["jobs_erledigt"]]
    if schreiben:
        zustand.bekannt_machen(z, auftraggeber)
    else:
        z = dict(z, bekannt=list(z.get("bekannt") or []))
        zustand.bekannt_machen(z, auftraggeber)
    kand = [j for j in V["jobs"] if job_frei(z, modul, j)]
    rng = random.Random("%s-%d-jobs" % (z["id"], z["tag"]))
    rng.shuffle(kand)
    frau = lambda j: modul["personen"][j["von"]].get("romanzierbar")
    wahl, wer, gruppen = [], set(), set()

    def nimm(j):
        if j.get("gruppe"):
            if j["gruppe"] in gruppen:
                return False
            gruppen.add(j["gruppe"])
        wahl.append(j)
        wer.add(j["von"])
        return True
    # erst 2 Frauen, dann Nebenfiguren (mehr Dorf im Spiel), dann wieder alle; je Person eine
    for grenze, liste in ((FRAUEN_MIN, [x for x in kand if frau(x)]), (JOBS_PRO_TAG, [x for x in kand if not frau(x)]),
                          (JOBS_PRO_TAG, kand)):
        for j in liste:
            if len(wahl) >= grenze:
                break
            if j not in wahl and j["von"] not in wer:
                nimm(j)
    for j in kand:                                           # zu wenige Personen: dann auch zwei von derselben
        if len(wahl) >= JOBS_PRO_TAG:
            break
        if j not in wahl:
            nimm(j)
    ids = []
    for j in wahl:                                           # Wege einer Gruppe stehen zusammen
        ids += [j["id"]] + [x["id"] for x in kand if j.get("gruppe") and x.get("gruppe") == j["gruppe"] and x is not j]
    if schreiben:
        z["jobs_tag"] = {"tag": z["tag"], "ids": ids}
        annehmen(z, modul, V, ids)
    return ids


def annehmen(z, modul, V, ids):
    """Besorgungen (braucht ein Teil) gelten als angenommen, sobald sie angeboten wurden."""
    jobs = {j["id"]: j for j in V["jobs"]}
    a = z.setdefault("auftraege", [])
    for jid in ids:
        b = jobs.get(jid, {}).get("braucht")
        if b and modul["items"].get(b, {}).get("art") == "teil" and jid not in a:
            a.append(jid)


def zuletzt(z, V, j):
    """Ergebnis der Mission davor, fuer die Karte: Der Spieler hat sie vermutlich vergessen (Duc 31.10.2026)."""
    davor = next((x for x in V["jobs"] if x["id"] == j.get("nach")), None)
    return davor.get("erfolg") if davor and davor["id"] in z.get("jobs_erfolg", []) else None


def kette(z, V, j):
    """Kettenstrang einer Mission (ueber nach=, ohne Gruppen-Abzweig) -> [{"titel", "stand"}] mit stand
    fertig/jetzt/zu, oder [] fuer Einzelauftraege."""
    nach_id = {x["id"]: x for x in V["jobs"]}
    davor, x = [], j
    while x.get("nach") in nach_id:
        x = nach_id[x["nach"]]
        davor.insert(0, x)
    danach, x = [], j
    while True:
        x = next((y for y in V["jobs"] if y.get("nach") == x["id"]), None)
        if not x:
            break
        danach.append(x)
    if not davor and not danach:
        return []
    return [{"titel": y["titel"], "stand": "fertig" if y["id"] in z.get("jobs_erfolg", []) else "zu"} for y in davor] + \
        [{"titel": j["titel"], "stand": "jetzt"}] + [{"titel": y["titel"], "stand": "zu"} for y in danach]


def werkzeug_da(z, j):
    """Erstes Werkzeug der Mission, das Duc dabeihat (Inventar oder Truhe zaehlt nicht - nur, was er traegt)."""
    return next((i for i in j.get("werkzeug") or [] if i in z["inventar"]), None)


def jobs_heute(z, modul, V):
    if not V or not V.get("jobs") or not jobs_aktiv(modul):
        return []
    ids = jobs_angebot(z, modul, V, schreiben=False)      # festgeschrieben wird am Ende jeder Aktion (eden.aktion)
    ids = ids + [i for i in offene_auftraege(z, modul, V) if i not in ids]     # angenommene Auftraege bleiben
    kand = [j for i in ids for j in V["jobs"] if j["id"] == i and job_frei(z, modul, j)]
    out = []
    for j in kand:
        mit_probe = j.get("probe", True) is not False
        bonus = z["persona"]["attribute"].get(j.get("attribut"), 0) if z.get("persona") and mit_probe else 0
        if mit_probe:                                   # Jacken-Charm (28.10.2026)
            from . import charms
            bonus += charms.attribut(z, j.get("attribut"))
        # Vorteil als Anzeigename ("craft"/"kitchen"/"tool", englisch seit 29.10.2026) oder "" - wuerfel.probe nimmt ihn als Wahrheitswert
        vorteil = ("craft" if j.get("reparatur") and persona_vorteil(z, "handwerk") else
                   "kitchen" if j.get("kochen") and persona_vorteil(z, "kueche") else "")
        wz = werkzeug_da(z, j) if mit_probe else None
        wz_bonus = 0
        if wz and vorteil:
            wz_bonus = 2                                   # Vorteil hat er schon: das Werkzeug gibt +2 obendrauf
        elif wz:
            vorteil = "tool"
        if mit_probe:
            p = max(5, min(95, round((21 - (j["sg"] - bonus - wz_bonus)) * 5)))
            if vorteil:
                p = min(95, round(100 - (100 - p) ** 2 / 100))
        else:
            p = 100
        vp = modul["personen"][j["von"]]
        braucht = j.get("braucht")
        out.append(dict(j, von_name=vp["name"], von_kurz=vp["name"].split()[-1] if (vp.get("kurz") or "").startswith("the ") else (vp.get("kurz") or vp["name"].split()[0]), wert=bonus, chance=p,
                        vorteil=vorteil, mit_probe=mit_probe, werkzeug_da=wz, werkzeug_bonus=wz_bonus,
                        werkzeug_label=modul["items"][wz]["label"] if wz else "",
                        braucht_label=modul["items"][braucht]["label"] if braucht in modul["items"] else "",
                        braucht_ok=(braucht in z["inventar"] or braucht in tasche(z)) if braucht else True,
                        braucht_teil=modul["items"].get(braucht, {}).get("art") == "teil",
                        braucht_wo=[modul["laeden"][w]["name"] for w in modul["items"].get(braucht, {}).get("wo") or []
                                    if w in (modul.get("laeden") or {})],
                        offen=j["id"] in offene_auftraege(z, modul, V),
                        versuch=job_fehl(z, j["id"]).get("anzahl", 0) + 1, versuche=MISSION_VERSUCHE,
                        energie=1 if mit_probe else 0, kette=kette(z, V, j), zuletzt=zuletzt(z, V, j),
                        energie_fehlt=max(0, 1 - z["werte"].get("energie", 0)) if mit_probe else 0))
    return out


def energie_tipp(z, modul):
    """Woher die fehlende Energie kommt (Duc 29.10.2026: Jobkarte graut gleich aus statt erst nach dem Klick abzusagen).
    Liegt etwas in der Tasche, das Energie gibt (Verbrauch mit wert energie > 0, z. B. Espresso, Lola's Energy Bar), wird es genannt."""
    for iid in dict.fromkeys(z.get("inventar", [])):
        it = modul["items"].get(iid) or {}
        if it.get("art") == "verbrauch" and any(f.get("wert") == "energie" and f.get("delta", 0) > 0 for f in it.get("wirkung") or []):
            return "Use the %s in your bag, take a relaxed hour with the crew, or come back tomorrow." % it["label"]
    return "An espresso, a relaxed hour with the crew, or tomorrow morning gives you energy back."


def job_machen(z, modul, V, jid):
    j = next((x for x in jobs_heute(z, modul, V) if x["id"] == jid), None)
    if not j:
        raise ValueError("That job isn't on offer today.")
    if j.get("braucht") and not j["braucht_ok"]:
        raise ValueError("You need %s for this." % (j["braucht_label"] or j["braucht"]))
    if j.get("preis") and z["konto"] < j["preis"]:
        raise ValueError("Not enough money: %s costs %s." % (j["titel"], euro(j["preis"])))
    if j["mit_probe"] and z["werte"].get("energie", 0) < 1:
        raise ValueError("You're running on empty. An espresso or a relaxed hour with the crew gives you energy back, "
                         "and tomorrow starts with two more. Jobs without a roll still work.")
    zeilen = zustand.folgen_anwenden(z, modul, [{"wert": "energie", "delta": -1}]) if j["mit_probe"] else []
    if j.get("braucht"):                                   # Abgabe: der Gegenstand ist weg (auch bei Fehlschlag)
        (tasche(z) if j["braucht"] in tasche(z) else z["inventar"]).remove(j["braucht"])
        zeilen.append("Handed over: " + (j["braucht_label"] or j["braucht"]))
    if j.get("preis"):
        zeilen.append(buchen(z, -j["preis"], "%s: %s" % (j["von_kurz"], j["titel"])))
    if j["mit_probe"]:
        boni = [(j["attribut"].capitalize(), j["wert"])]
        if j["werkzeug_bonus"]:
            boni.append((j["werkzeug_label"], j["werkzeug_bonus"]))
        boni += moral.wuerfel_bonus(z, modul, [j["von"]])                # Crew-Mission: Crew-Stimmung (27.10.2026)
        p = wuerfel.probe(j["attribut"], j["sg"], boni, vorteil=j["vorteil"])
        ok = p["ergebnis"] in ("erfolg", "kritisch")
        zeilen += zustand.folgen_anwenden(z, modul, moral.nach_probe(z, modul, p, [j["von"]]))
    else:
        p, ok = None, True
    fehl = z.setdefault("jobs_fehl", {})
    if ok:
        z["jobs_erledigt"].append(jid)
        if j.get("gruppe"):
            z.setdefault("gruppen_erledigt", []).append(j["gruppe"])
        lohn = j["lohn"]
        a = z.setdefault("auftraege", [])               # Kette: die Fortsetzung ist ab jetzt ein offener Auftrag
        for x in V["jobs"]:
            if x.get("nach") in (jid, j.get("gruppe")) and x["id"] not in a:
                a.append(x["id"])
    else:
        f = fehl.setdefault(jid, {"anzahl": 0})
        f["anzahl"] += 1
        f["tag"] = z["tag"]
        letzter = f["anzahl"] >= MISSION_VERSUCHE
        if letzter:
            z["jobs_erledigt"].append(jid)
            zeilen.append("Second failure – the job is gone")
            if moral.crew_dabei(modul, [j["von"]]):                    # Crew-Mission endgueltig verpatzt: -1
                zeilen += zustand.folgen_anwenden(z, modul, [moral.folge(-1, "genau")])
        else:
            zeilen.append("You can try again tomorrow")
        lohn = j["lohn"] // 2 if letzter else 0
    if lohn:
        zeilen.append(buchen(z, lohn, "%s: %s" % (j["von_kurz"], j["titel"])))
    for f in (j.get("folgen", []) if ok else j.get("folgen_fehlschlag", [])):
        if "vertrauen" in f or "begehren" in f:          # Punkte-Folgen der eden_rise-Missionen
            art = "vertrauen" if "vertrauen" in f else "begehren"
            if "%s.%s" % (art, f[art][0]) in z["werte"]:
                zeilen += zustand.punkte_add(z, modul, "%s.%s" % (art, f[art][0]), f[art][1])
        elif "item" in f and f["item"] not in modul.get("items", {}):
            continue
        else:
            zeilen += zustand.folgen_anwenden(z, modul, [f], frei=False)
    if ok and not modul["personen"][j["von"]].get("romanzierbar") and "vertrauen." + j["von"] in z["werte"] \
            and z.setdefault("missionen_tag", {}).get(j["von"]) != z["tag"]:
        z["missionen_tag"][j["von"]] = z["tag"]            # Nebenfiguren: +6 Vertrauen je Erfolg (einmal am Tag)
        zeilen += zustand.punkte_add(z, modul, "vertrauen." + j["von"], MISSION_VERTRAUEN)
    if rollen.ist(modul, "haendler", j["von"]):
        zeilen += draht_plus(z, modul, halb=False)
    pid, vp = j["von"], modul["personen"][j["von"]]
    if ok:
        z.setdefault("jobs_erfolg", []).append(jid)
    if vp.get("romanzierbar"):                  # Missionen der Frauen: Vertrauen je Hilfe, Begehren nur bei persoenlichen
        name = vp["name"].split()[0]
        if ok and z.setdefault("missionen_tag", {}).get(pid) != z["tag"]:
            z["missionen_tag"][pid] = z["tag"]
            zeilen += zustand.punkte_add(z, modul, "vertrauen." + pid, MISSION_VERTRAUEN)
            if j.get("persoenlich"):
                zeilen += zustand.punkte_add(z, modul, "begehren." + pid, MISSION_BEGEHREN)
            chronik.eintragen(z, modul, "mission", "Duc helped %s with something she asked him for, and it went well."
                              % name, wer=[pid], dabei=[], wichtig=1)
        elif ok:
            zeilen.append("Heute schon eine Mission mit %s – keine weiteren Punkte" % name)
        elif p and p["ergebnis"] == "patzer" and z["tag"] > 1:
            zeilen += zustand.punkte_add(z, modul, "vertrauen." + pid, MISSION_PATZER)
    gruppe = "erfolg" if ok else "patzer" if p and p["ergebnis"] == "patzer" else "fehlschlag"
    k = job_kommentar(z, modul, pid, gruppe, jid)
    text = j.get("erfolg" if ok else "fehlschlag") or ""
    return {"probe": p, "zeilen": zeilen, "text": text, "ok": ok, "gruppe": gruppe, "pid": pid, "kommentar": k}


def job_zeilen(modul, pid):
    return (modul.get("job_zeilen") or {}).get(pid) or {}


def job_kommentar(z, modul, pid, gruppe, salz):
    """Einer der festen Saetze (Gefuehl + Text) - stabil je Mission, damit Neuladen nicht umwuerfelt."""
    liste = job_zeilen(modul, pid).get(gruppe) or job_zeilen(modul, pid).get("fehlschlag" if gruppe == "patzer" else "") or []
    if not liste:
        return None
    if gruppe == "patzer" and not job_zeilen(modul, pid).get("patzer"):
        gruppe = "fehlschlag"
    i = random.Random("%s-%s-%s-%d" % (z["id"], salz, gruppe, z["tag"])).randrange(len(liste))
    return {"id": "job.%s.%s.%d" % (pid, gruppe, i), "gefuehl": liste[i][0], "text": liste[i][1]}


def job_angebot_zeile(z, modul, pid, jid):
    return job_kommentar(z, modul, pid, "angebot", jid)


def job_zeile(modul, zid):
    """'job.rosi.erfolg.3' -> (pid, Text) fuer die Vertonung - nur feste Saetze, nie freier Text."""
    teile = (zid or "").split(".")
    if len(teile) != 4 or teile[0] != "job" or not teile[3].isdigit():
        return None, None
    liste = job_zeilen(modul, teile[1]).get(teile[2]) or []
    i = int(teile[3])
    return (teile[1], liste[i][1]) if i < len(liste) else (None, None)


# ------------------------------------------------------------------ Ansicht
def gerichte(z, modul):
    """Ducs Kueche (Persona-Staerke): die Gerichte aus gegenstaende.json, in Lolas Kombuese gekocht."""
    # Lieblingsgerichte (18.10.2026): nur, was Duc schon entdeckt hat (kern/vorlieben.py) - vorher steht nichts da
    bekannt = vorlieben.liste(z)
    return [{"id": i, "label": it["label"], "text": it.get("text", ""), "sg": (it.get("kochen") or {}).get("sg", 10),
             "kueche": (it.get("kochen") or {}).get("kueche", ""),
             "mag": [anzeigename(modul, v["figur"]) for v in bekannt if v["item"] == i and v["reaktion"] == "mag"],
             "mag_nicht": [anzeigename(modul, v["figur"]) for v in bekannt if v["item"] == i and v["reaktion"] == "mag_nicht"]}
            for i, it in modul["items"].items() if it.get("art") == "gericht"]


def ansicht(z, modul, V, in_szene):
    """in_szene = alle anwesenden Personen (Frauen und Nebenfiguren)."""
    init(z, modul)
    inv = []
    for iid, n in zustand.stapel_liste(modul, z["inventar"]):          # eine Kachel je Stapel (Duc 28.10.2026)
        it = modul["items"].get(iid, {"label": iid, "art": "?"})
        inv.append({"id": iid, "label": it["label"], "art": it.get("art"), "text": it.get("text", ""),
                    "wirkung_text": it.get("wirkung_text"), "intim": it.get("intim"),
                    "n": n, "stapel": zustand.stapel(modul, iid),
                    "benutzbar": bool(it.get("benutzen") or (it.get("kampf") or {}).get("pflege")
                                      or (it.get("art") == "verbrauch" and _ohne_moral(it.get("wirkung")))),
                    "geben": [p for p in in_szene if p in modul["personen"] and "geschenk" in it
                              and z["geschenke"].get(p) != z["tag"]]})
    from . import expedition
    inv += expedition.ernte_ansicht(z, modul)                           # Abgebautes und Fang unterwegs (eigene Bilder)
    return {"konto": z["konto"], "buchungen": z["buchungen"][-20:][::-1], "draht": z["werte"].get("draht", 0),
            "honorar": (modul.get("geld") or {}).get("honorar", 0),
            "haendler": rollen.rolle(modul, "haendler"),
            "haendler_name": anzeigename(modul, rollen.rolle(modul, "haendler")) if rollen.rolle(modul, "haendler") else "",
            "belegt": zustand.belegt(z, modul),
            "plaetze": zustand.inventar_plaetze(z, modul),                  # Taschengroesse 8 / 12 / 16 fuers Menue (fix-akt2)
            "laeden": {k: {"name": l["name"], "text": l.get("text", ""), "waren": sortiment(z, modul, k),
                           "essen": bool(l.get("essen")), "nur_an_land": bool(l.get("nur_an_land")), "werkstatt": bool(l.get("werkstatt")), "farm": bool(l.get("farm")),
                           "werkzeug": bool(l.get("werkzeug_laden")),                     # Petrus Werkstatt (28.10.2026)
                           "schneider": bool(l.get("schneider")),                         # Danzels Auftraege (30.10.2026)
                           "mochis": bool(l.get("mochis")),                               # Bibis Tierstation (31.10.2026)
                           "wer_name": anzeigename(modul, l["wer"]) if l.get("wer") in modul["personen"] else ""}
                       for k, l in (modul.get("laeden") or {}).items()
                       if (not l.get("erst_bekannt") or l.get("wer") in (z.get("bekannt") or []))   # Isabelle (27.10.2026)
                       and z.get("tag", 1) >= l.get("ab_tag", 0) and laden_offen(z, l)},   # Eden-Shop ab Akt 2
            "ankauf": ankauf(z, modul), "jobs": jobs_heute(z, modul, V), "jobs_aktiv": jobs_aktiv(modul),
            "inventar_info": inv,
            "energie_tipp": energie_tipp(z, modul),                         # Jobkarte ohne Energie (29.10.2026)
            "tasche": [{"id": i, "label": modul["items"].get(i, {}).get("label", i), "text": modul["items"].get(i, {}).get("text", ""),
                        "fuer": teile_gebraucht(z, modul, V).get(i, "")} for i in tasche(z)] if jobs_aktiv(modul) else [],
            "tasche_plaetze": TASCHE_PLAETZE,
            "gerichte": gerichte(z, modul) if kueche(modul) else [],
            "essen_frei": essen_frei(z, modul), "koch_ziele": koch_ziele(z, modul, in_szene),
            "namen": {p: anzeigename(modul, p) for p in in_szene if p in modul["personen"]}}


def anzeigename(modul, pid):
    p = modul["personen"][pid]
    k = p.get("kurz") or ""
    return p["name"].split()[-1] if k.startswith("the ") else (k or p["name"].split()[0])


def koch_ziele(z, modul, in_szene):
    """Fuer wen Duc kochen kann: die Crew (alle an Bord) oder eine Person aus der laufenden Szene."""
    out = [{"id": "crew", "name": "the crew"}]
    for p in in_szene:
        if p in modul["personen"] and "vertrauen." + p in z["werte"]:
            out.append({"id": p, "name": anzeigename(modul, p)})
    return out


def crew_an_bord(z, modul):
    """Die Crew-Tafel: alle Frauen an Bord plus rollen "isst_mit" (Kochen fuer die Crew, Festessen aus dem Baukasten)."""
    from . import buehne
    an_land = [r for r, rr in modul["raeume"].items() if "(ashore)" not in rr.get("label", "")]
    return [p for p, x in modul["personen"].items() if (x.get("romanzierbar") or rollen.ist(modul, "isst_mit", p))
            and "vertrauen." + p in z["werte"] and buehne.wo_ist(z, modul, p) in an_land]


def kochen_aktion(z, modul, regeln, iid, fuer):
    """Aktion 'kochen': Probe, Wirkung, Zeilen. Crew = alle Frauen an Bord plus rollen "isst_mit"."""
    from . import buehne
    it = modul["items"].get(iid)
    if not it or it.get("art") != "gericht":
        raise ValueError("That dish doesn't exist.")
    item = dict(it, liebt=[p for p, w in (it.get("geschenk") or {}).items() if w == 2],
                hasst=[p for p, w in (it.get("geschenk") or {}).items() if w < 0], wirkung=it.get("kochen") or {})
    if fuer == "crew":
        r = kochen(z, modul, item, regeln, "crew", crew_an_bord(z, modul))
    else:
        r = kochen(z, modul, item, regeln, fuer)
        vorlieben.aus_gericht(z, modul, fuer, iid, r["stufen"].get(fuer))   # ein Teller fuer sie: Duc sieht, wie es ankommt
        if tisch.ausloesen(z, modul, fuer, iid, r["stufen"].get(fuer), r["probe"]["ergebnis"], r["zeilen"]):
            tisch.erinnerung_als_vorliebe(z, modul, fuer, iid)       # erstes volles Lieblingsgericht: Tischszene (27.10.2026)
    p = r["probe"]
    kopf = {"kritisch": "A masterpiece.", "erfolg": "Well done.", "fehlschlag": "Not your day.",
            "patzer": "Burnt."}[p["ergebnis"]]
    zeilen = ["D20 %s + %d = %d vs DC %d · %s" % (p["wurf"], sum(b for _, b in p["boni"]), p["summe"], p["sg"], kopf)]
    lob = {"liebt": "loves it", "gut": "really likes it", "normal": "enjoys it", "fade": "eats bread with it",
           "ekel": "won't touch it", "crew": "eats with you"}
    zeilen += ["%s %s" % (anzeigename(modul, pid), lob.get(st, st)) for pid, st in r["stufen"].items()]
    chronik.eintragen(z, modul, "moment", "Duc cooked %s for %s." % (it["label"], "the crew" if fuer == "crew" else
                                                                    modul["personen"][fuer]["name"].split()[0]),
                      wer=list(r["stufen"]), dabei=[], wichtig=1)
    return "You cook: " + it["label"], zeilen + r["zeilen"]
