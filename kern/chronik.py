# -*- coding: utf-8 -*-
"""Chronik (16.10.2026): das harte Gedaechtnis des Durchlaufs - geschrieben vom Code, nicht vom Sprachmodell.

Duc: "Wuerde eine harte Erinnerung wie temporaere Lorebook-Eintraege helfen?" - Ja, aber der Code weiss das meiste
selbst: Entscheidungen, erfuellte Ausgaenge, Geschenke, Handel, Funde, Andenken. Das wird hier sofort als Eintrag
gespeichert (null Zusatzaufrufe, nichts erfunden). Was nur im Text passiert (Kuss, Gestaendnis, Streit ...), erkennt
die Auswertung am Szenenende im selben Aufruf wie die Beute (szene.auswerten).

Jeder Eintrag: wer beteiligt ist, wo, Tag, wer dabei war und WER DAVON WEISS. Wissen verbreitet sich nach Regeln
im Code (Klatsch): Alva erfaehrt alles an Land, Toto alles aus seinem Spind, bei Gruppenszenen kann ein Geheimnis
die Runde machen - erfaehrt eine Frau von einem Kuss mit einer anderen, steigt die Spannung zwischen den beiden.
Genutzt wird die Chronik im Figuren-Prompt (nur was SIE weiss), als Rueckbezug zum Szenenstart, beim Richter
(Widerspruch zu bekannten Fakten) und im Codex fuer den Spieler."""
import random

from . import rollen, zustand

MOMENTE = {          # Kennung -> (englischer Satz, Wichtigkeit, Lebensdauer in Tagen oder None = dauerhaft)
    "kiss": ("Duc and {n} kissed.", 3, None),
    "intimate": ("Duc and {n} slept together.", 3, None),
    "confession": ("Duc and {n} admitted feelings for each other.", 3, None),
    "fight": ("Duc and {n} had a real fight.", 2, 1),
    "apology": ("Duc and {n} made up after a quarrel.", 2, None),
    "promise": ("Duc made {n} a serious promise.", 1, None),
    "secret": ("{n} told Duc something private about herself.", 2, None),
    "duc_secret": ("Duc told {n} his secret: a firm in Frankfurt wants his answer this week.", 2, None),
    "rebuff": ("{n} turned Duc down.", 2, 1),
    "stood_up": ("Duc stood {n} up: she waited for him all evening, he never came.", 2, 2),
    # Live-Spieltest 31.10.2026: Eine angenommene intime Aktion beweist keinen Sex. Darum eigene, schwaechere Saetze;
    # Wichtigkeit 1 = kein Klatsch (E-060), und sie stehen bewusst nicht in EIFERSUCHT.
    "naehe": ("Duc and {n} shared a private, physical moment.", 1, None),
    "naehe_weit": ("Duc and {n} went further than kissing, in private.", 1, None),
}
EIFERSUCHT = ("kiss", "intimate", "confession", "gesehen")   # gesehen: erwischt an einem Ort (kern/orte.py)     # erfaehrt eine andere Frau davon -> Spannung des Paares +1
NAEHE_RANG = ("naehe", "naehe_weit", "intimate")     # schwach -> stark
GROSSE_MOMENTE = ("kiss", "confession") + NAEHE_RANG  # werden beim naechsten Treffen unter vier Augen aufgegriffen
KLATSCH_CHANCE = 0.3                                 # je Gruppenszene, eine Neuigkeit macht die Runde
KLATSCH_DORFOHR = 0.7                                # ist das Dorfohr dabei (rollen: dorfohr), plaudert es fast immer
PROMPT_MAX = 6


def liste(z):
    return z.setdefault("chronik", [])


def eintragen(z, modul, art, text, wer=(), dabei=None, wichtig=1, dauer=None, ort=None, moment=None, privat=False):
    """Neuer Eintrag. dabei = Anwesende (Standard: Figuren der laufenden Szene); sie wissen es.
    privat = auch das Dorfohr erfaehrt es nicht."""
    sz = z.get("szene") or {}
    if dabei is None:
        dabei = [p for p in sz.get("figuren", []) if p in modul["personen"]]
    ort = ort or (sz.get("def") or {}).get("ort")
    weiss = sorted(set(dabei) | set(wer))
    an_land = bool(ort) and "(ashore)" in modul["raeume"].get(ort, {}).get("label", "")
    ohr = rollen.rolle(modul, "dorfohr")
    if an_land and not privat and ohr in modul["personen"] and ohr not in weiss:
        weiss.append(ohr)                            # das Dorfohr erfaehrt alles, was im Dorf passiert
    e = {"nr": len(liste(z)) + 1, "tag": z["tag"], "phase": z.get("phase"), "ort": ort, "art": art, "text": text,
         "wer": list(wer), "weiss": weiss, "wichtig": wichtig, "bis": z["tag"] + dauer if dauer else None}
    if moment:
        e["moment"] = moment
    liste(z).append(e)
    return e


def gueltig(z, e):
    return not e.get("bis") or z["tag"] <= e["bis"]


def fuer_figur(z, modul, pid, anwesende):
    """Was SIE weiss und gerade zaehlt: beteiligt sie oder Anwesende, wichtig, frisch. Hoechstens PROMPT_MAX."""
    kand = [e for e in liste(z) if pid in e["weiss"] and gueltig(z, e)]
    def punkte(e):
        p = e["wichtig"] * 2 + (3 if pid in e["wer"] else 0) + sum(1 for a in anwesende if a in e["wer"])
        return p - 0.5 * (z["tag"] - e["tag"])
    beste = sorted(kand, key=punkte, reverse=True)[:PROMPT_MAX]
    return ["Day %d: %s" % (e["tag"], e["text"]) for e in sorted(beste, key=lambda e: e["nr"])]


def naehe_eintragen(z, modul, pid, moment):
    """Intime Aktion (Live-Spieltest 31.10.2026): schreibt je Tag und Figur nur den staerksten Eintrag; nur sie weiss davon."""
    rang = NAEHE_RANG.index(moment)
    if any(e.get("moment") in NAEHE_RANG and NAEHE_RANG.index(e["moment"]) >= rang and pid in e["wer"] and e["tag"] == z["tag"]
           for e in liste(z)):
        return None
    satz, wichtig, dauer = MOMENTE[moment]
    return eintragen(z, modul, "moment", satz.format(n=modul["personen"][pid]["name"].split()[0]), wer=[pid], dabei=[pid],
                     wichtig=wichtig, dauer=dauer, moment=moment, privat=True)


def hat_naehe(z, pid):
    return any(e.get("moment") in NAEHE_RANG and pid in e["wer"] for e in liste(z))


def moment_offen(z, pid, momente, tage=3):
    """Romanzen-Leiter (31.10.2026): Gibt es einen frischen Moment, den noch niemand aufgegriffen hat?"""
    return any(e.get("moment") in momente and pid in e["wer"] and not e.get("aufgegriffen") and gueltig(z, e)
               and z["tag"] - e["tag"] <= tage for e in liste(z))


def moment_zahl(z, pid, moment):
    return sum(1 for e in liste(z) if e.get("moment") == moment and pid in e["wer"])


def aufgreifen(z, pid, momente):
    for e in liste(z):
        if e.get("moment") in momente and pid in e["wer"]:
            e["aufgegriffen"] = True


def rueckbezug(z, pid, allein=False):
    """Der letzte gemeinsame Moment mit Duc (aus frueheren Szenen) - fuer den Szenenstart.
    allein: Ein noch nicht aufgegriffener grosser Moment geht vor, damit ein spaeteres Geschenk die Nacht nicht verdraengt."""
    if allein:
        for e in reversed(liste(z)):
            if e.get("moment") in GROSSE_MOMENTE and pid in e["wer"] and not e.get("aufgegriffen") and gueltig(z, e):
                return e
    for e in reversed(liste(z)):
        if pid in e["wer"] and e["art"] in ("moment", "geschenk", "andenken") and gueltig(z, e):
            return e
    return None


def rueckbezug_handy(z, pid, tage=1):
    """Duc's best text line to her from the last `tage` days (chat entries "Duc texted ...") for the next scene start.
    Highest importance first, then the newest. Each entry is picked up once ("genutzt")."""
    kand = [e for e in liste(z) if e["art"] == "handy" and pid in e["wer"] and not e.get("genutzt")
            and e["text"].startswith("Duc texted") and e["tag"] >= z["tag"] - tage and gueltig(z, e)]
    return max(kand, key=lambda e: (e["wichtig"], e["nr"])) if kand else None


def klatsch(z, modul, anwesende, rng=None):
    """Zum Szenenstart: macht eine Neuigkeit die Runde? -> Liste (Lernende, Eintrag, Zeilen fuer die Anzeige)."""
    rng = rng or random.Random("%s-%d-%s-%d" % (z["id"], z["tag"], z.get("phase"), len(liste(z))))
    da = [p for p in anwesende if p in modul["personen"]]
    if len(da) < 2:
        return []
    chance = KLATSCH_DORFOHR if rollen.rolle(modul, "dorfohr") in da else KLATSCH_CHANCE
    if rng.random() >= chance:
        return []
    # Wer beteiligt ist, schweigt - weitererzaehlen koennen nur Zeugen (dabei, aber nicht beteiligt) oder Tratsch-
    # tanten (rollen: tratsch). Lea erzaehlt ihren eigenen Kuss nicht beim Fruehstueck herum (Probelauf 16.10.2026).
    tratsch = rollen.liste(modul, "tratsch")

    def erzaehler(e):
        return [p for p in da if p in e["weiss"] and (p not in e["wer"] or p in tratsch)]
    kand = [e for e in liste(z) if e["wichtig"] >= 2 and gueltig(z, e)
            and erzaehler(e) and any(p not in e["weiss"] for p in da)]
    if not kand:
        return []
    e = max(kand, key=lambda x: (x["wichtig"], x["nr"]))
    lernen = [p for p in da if p not in e["weiss"]]
    e["weiss"] += lernen
    zeilen = []
    for p in lernen:
        if not modul["personen"][p].get("romanzierbar"):
            continue
        zeilen.append("👂 %s found out: %s" % (modul["personen"][p]["name"].split()[0], e["text"]))
        if e.get("moment") in EIFERSUCHT:
            for andere in e["wer"]:
                paar = next((k for k in modul["werte"].get("rivalitaet", {}).get("paare", [])
                             if set(k.split("_")) == {p, andere}), None)
                if paar:
                    zeilen += zustand.folgen_anwenden(z, modul, [{"wert": "rivalitaet." + paar, "delta": 1}])
                elif andere != p and z["werte"].get("begehren." + p, 0) >= 3:
                    # kein festes Rivalinnen-Paar: es trifft sie nur, wenn sie selbst Gefuehle fuer Duc hat
                    zeilen.append("💔 %s ist verletzt" % modul["personen"][p]["name"].split()[0])
                    if "verletzt_" + p not in z["flags"]:      # Romanzen-Leiter: sie sagt am naechsten Morgen etwas dazu
                        z["flags"].append("verletzt_" + p)
                    zeilen += zustand.folgen_anwenden(z, modul, [{"wert": "vertrauen." + p, "delta": -1}])
    return [(lernen, e, zeilen)]


def ansicht(z, modul):
    """Fuer den Codex: neueste zuerst, mit Namen derer, die davon wissen."""
    def nm(p):
        return modul["personen"].get(p, {}).get("name", p).split()[0]
    return [{"tag": e["tag"], "text": e["text"], "art": e["art"], "abgelaufen": not gueltig(z, e),
             "weiss": [nm(p) for p in e["weiss"]]} for e in reversed(liste(z))]
