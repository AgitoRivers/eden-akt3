# -*- coding: utf-8 -*-
"""The Ricci brothers - pickpockets in the harbour (Duc + Brain Trust 29.10.2026). Fight data: werkzeuge/eden_rise/
kaempfe_hafen.py (enemies with voiced taunts, kern/kampf._spruch).

A random fight when Duc walks into Alva's bar or Petru's workshop: 5 % per visit, from day 3, at most every 2 days. It
builds up - every encounter is the next stage, however it ended (otherwise a weak player would stay on stage 1):
    1  Fabbiu OR Santu alone      they steal 1 consumable (no consumable: 20 EUR)
    2  The Ricci Brothers         2 (40 EUR)
    3  The Ricci Gang (+ Matte)   3 (60 EUR)
After stage 3 they stop; Elsa's side quest to lock them up follows (flags ricci_1..3, z["ricci"]["beute"]).
Win: they drop the last thing they stole from Duc (else a few euros from their pockets). Lose / flee / they get away:
the stolen things go into z["ricci"]["beute"] - for the quest. Never stolen: anything that isn't a consumable (gifts,
keepsakes, story items, charms, tools). State: z["ricci"] = {"stufe", "letzte_tag", "besuche", "beute": [ids]}."""
import random

LAEDEN = ("alva", "petru")
CHANCE, AB_TAG, ABSTAND = 0.05, 3, 2
STUFEN = {1: ("hafen_ricci_1f", "hafen_ricci_1s"), 2: ("hafen_ricci_2",), 3: ("hafen_ricci_3",)}
STUFE_VON = {bid: n for n, bids in STUFEN.items() for bid in bids}
KLAUEN = {1: 1, 2: 2, 3: 3}
GELD_JE_STUECK = 20
VERBRAUCH = ("kampf", "snack", "gericht", "verbrauch", "ressource", "essen")   # what the menu calls "Consumables"
NIEDERLAGE = ("niederlage", "flucht", "entkommen")


def stand(z):
    s = z.setdefault("ricci", {})
    s.setdefault("stufe", 0)
    s.setdefault("letzte_tag", None)
    s.setdefault("besuche", 0)
    s.setdefault("beute", [])
    return s


def ausloesen(z, laden):
    """A visit to a harbour shop -> encounter id to start now, or None. Counts the visit (fixed dice per save, day and
    visit, so the gate run stays reproducible)."""
    if laden not in LAEDEN or z.get("status") != "wahl" or z.get("tag", 0) < AB_TAG:
        return None
    s = stand(z)
    if s["stufe"] >= len(STUFEN) or (s["letzte_tag"] is not None and z["tag"] - s["letzte_tag"] < ABSTAND):
        return None
    s["besuche"] += 1
    rng = random.Random("ricci|%s|%s|%d" % (z.get("id"), z.get("tag"), s["besuche"]))
    if rng.random() >= CHANCE:
        return None
    s["letzte_tag"] = z["tag"]
    return rng.choice(STUFEN[s["stufe"] + 1])


def _verbrauch(modul, iid):
    return (modul["items"].get(iid) or {}).get("art") in VERBRAUCH


def _label(modul, iid):
    return (modul["items"].get(iid) or {}).get("label", iid)


def nach_kampf(z, modul):
    """Once the Ricci fight has a result: stage up, steal or give back. Lines go onto the result card."""
    k = z.get("kampf") or {}
    bid = k.get("definition")
    e = k.get("ergebnis")
    if bid not in STUFE_VON or not e or e.get("nochmal") or k.get("ricci_abgerechnet"):
        return []
    k["ricci_abgerechnet"] = True
    s = stand(z)
    stufe = STUFE_VON[bid]
    s["stufe"] = max(s["stufe"], stufe)
    if "ricci_%d" % stufe not in z["flags"]:
        z["flags"].append("ricci_%d" % stufe)
    rng = random.Random("ricci-beute|%s|%s|%s" % (z.get("id"), z.get("tag"), bid))
    zeilen = []
    if e["art"] in NIEDERLAGE:
        weg, geld = [], 0
        for _ in range(KLAUEN[stufe]):
            da = [i for i in z.get("inventar", []) if _verbrauch(modul, i)]
            if da:
                iid = rng.choice(sorted(set(da)))
                z["inventar"].remove(iid)
                s["beute"].append(iid)
                weg.append(_label(modul, iid))
            else:
                geld += GELD_JE_STUECK
        if weg:
            zeilen.append("Stolen: %s." % ", ".join(weg))
        if geld:
            geld = min(geld, max(0, z.get("konto", 0)))
            z["konto"] = z.get("konto", 0) - geld
            if geld:
                zeilen.append("They took %d € from your wallet." % geld)
    else:
        if s["beute"]:
            iid = s["beute"].pop()
            z["inventar"].append(iid)
            zeilen.append("You get back: %s." % _label(modul, iid))
        else:
            n = 10 + 5 * stufe
            z["konto"] = z.get("konto", 0) + n
            zeilen.append("In their pockets: %d €." % n)
    if stufe == len(STUFEN):
        zeilen.append("The Riccis won't try that again. Elsa will want to hear about this.")
    e.setdefault("zeilen", []).extend(zeilen)
    return zeilen
