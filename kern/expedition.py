# -*- coding: utf-8 -*-
"""Expeditions (26.10.2026, Duc): longer trips away from the ship - first the Kloster quest (Akt 2).

Rule for a defeat (Duc 26.10., stacks 28.10.): black screen, Duc wakes up on the ship, one phase is lost and he may keep
exactly ONE place of the loot he found on the way - one piece or one full stack (5 Plasters, 10 Timber). Everything else
he found is gone. What he brought along stays, experience and level stay. Generic on purpose: later expeditions (Akt 3,
...) use the same module.

    folgen {"expedition": "kloster"}   start (snapshot of inventory and chips) - the frame chain calls it
    folgen {"expedition": "ende"}      finished successfully, loot stays, the harvest is unpacked
    fights with "expedition_niederlage": true end the expedition on a defeat (eden.py, kampf_schliessen)

Harvest (Duc 28.10.2026, stacking): what Duc fells, breaks or catches at rest sites rides in the bag until he is home -
z["expedition"]["ernte"] = {"roh": {rid: n}, "fisch": {fid: [stars, ...]}}. Raw materials stack to 10 per place, fish
3 per species (kuechen.json abbau.stapel). It counts towards zustand.belegt and is lost on a defeat like other loot.

State in z["expedition"] = {"id", "inventar", "chips", "behalten", "ernte"}. Rules here, the client only shows the choice."""
from . import kampf, kuechen

# Story-critical things never count as loot (art "beweis", e.g. the control chip - E-073 / Kloster chapter)
NIE_BEUTE = ("beweis",)


def aktiv(z):
    return z.get("expedition")


def starten(z, eid, modul=None):
    zeilen = ernte_einlagern(z, modul) if modul and aktiv(z) else []   # an old trip that never ended: its harvest comes home
    c = kampf.chip_pool(z)
    z["expedition"] = {"id": eid, "inventar": list(z.get("inventar", [])), "chips": dict(c["pool"]), "behalten": None}
    return zeilen


def ende(z, modul=None):
    """Successful return: loot stays, the harvest goes into the counters and the kitchen, the snapshot is dropped."""
    zeilen = ernte_einlagern(z, modul) if modul else []
    z.pop("expedition", None)
    return zeilen


# ------------------------------------------------------------------ harvest in the bag (stacking, 28.10.2026)
def _stapel(modul):
    return (kuechen.daten(modul).get("abbau") or {}).get("stapel") or {"rohstoff": 10, "fisch": 3}


def _aufrunden(n, g):
    return -(-n // g) if n > 0 else 0


def ernte_plaetze(z, modul):
    """Bag places the harvest of the running expedition takes."""
    r = (aktiv(z) or {}).get("ernte")
    if not r:
        return 0
    st = _stapel(modul)
    return (sum(_aufrunden(n, st["rohstoff"]) for n in (r.get("roh") or {}).values())
            + sum(_aufrunden(len(l), st["fisch"]) for l in (r.get("fisch") or {}).values()))


def ernte_frei(z, modul, art, key):
    """How many more pieces of raw material rid (art "roh") or fish fid (art "fisch") fit: the open stack plus free places."""
    from . import zustand
    r = (aktiv(z) or {}).get("ernte") or {}
    g = _stapel(modul)["rohstoff" if art == "roh" else "fisch"]
    da = (r.get("roh") or {}).get(key, 0) if art == "roh" else len((r.get("fisch") or {}).get(key) or [])
    return (-da) % g + max(0, zustand.inventar_plaetze(z, modul) - zustand.belegt(z, modul)) * g


def fisch_platz(z, modul):
    """Is there room for one more fish of any kind (a free place or an open fish stack)?"""
    from . import zustand
    if zustand.belegt(z, modul) < zustand.inventar_plaetze(z, modul):
        return True
    g = _stapel(modul)["fisch"]
    return any(len(l) % g for l in (((aktiv(z) or {}).get("ernte") or {}).get("fisch") or {}).values())


def unterwegs(z):
    """Harvest goes into the bag only while an expedition runs and Duc stands at one of its rest sites."""
    return bool(aktiv(z)) and z.get("status") in ("ereignis", "abbau", "angeln")


def ernte_roh(z, modul, rid, n, bag=True):
    """Book n raw material: on the trip into the bag (as much as fits), at home straight into the counter. -> pieces taken."""
    if not (bag and unterwegs(z)):
        kuechen.rohstoff_add(z, rid, n)
        return n
    k = min(n, ernte_frei(z, modul, "roh", rid))
    if k:
        r = aktiv(z).setdefault("ernte", {}).setdefault("roh", {})
        r[rid] = r.get(rid, 0) + k
    return k


def ernte_fisch(z, modul, fid, stern, bag=True):
    """Book one fish: on the trip into the bag (False = no room, it goes back into the water), at home into the kitchen."""
    if not (bag and unterwegs(z)):
        kuechen.fang(z, modul, fid, 1, stern)
        return True
    if ernte_frei(z, modul, "fisch", fid) < 1:
        return False
    aktiv(z).setdefault("ernte", {}).setdefault("fisch", {}).setdefault(fid, []).append(stern)
    return True


def ernte_einlagern(z, modul):
    """Unpack the harvest at home: raw materials into the counters, fish into the kitchen. -> lines for the report."""
    e = aktiv(z)
    r = (e or {}).pop("ernte", None) or {}
    d = kuechen.daten(modul)
    teile = []
    for rid, n in (r.get("roh") or {}).items():
        if n:
            kuechen.rohstoff_add(z, rid, n)
            teile.append("+%d %s" % (n, d["rohstoffe"][rid]["label"]))
    fische = 0
    for fid, sterne in (r.get("fisch") or {}).items():
        for s in sterne:
            kuechen.fang(z, modul, fid, 1, s)
            fische += 1
    if fische:
        teile.append("%d fish for the kitchen" % fische)
    return ["Unpacked: %s." % ", ".join(teile)] if teile else []


def _fisch_label(modul, fid):
    return next((f["label"] for f in kuechen.daten(modul).get("fische", []) if f["id"] == fid), fid)


def ernte_ansicht(z, modul):
    """Bag tiles for the harvest: [{"id", "label", "art", "n", "stapel", "bild", "text"}], one per place."""
    r = (aktiv(z) or {}).get("ernte") or {}
    st, d, out = _stapel(modul), kuechen.daten(modul), []
    for rid, n in (r.get("roh") or {}).items():
        while n > 0:
            k = min(n, st["rohstoff"])
            out.append({"id": "roh:" + rid, "label": d["rohstoffe"][rid]["label"], "art": "rohstoff", "n": k,
                        "stapel": st["rohstoff"], "text": d["rohstoffe"][rid].get("text", ""), "bild": "/itembild/" + rid})
            n -= k
    for fid, sterne in (r.get("fisch") or {}).items():
        sterne = sorted(sterne, reverse=True)
        for i in range(0, len(sterne), st["fisch"]):
            teil = sterne[i:i + st["fisch"]]
            out.append({"id": "fisch:" + fid, "label": _fisch_label(modul, fid), "art": "fisch", "n": len(teil),
                        "stapel": st["fisch"], "sterne": teil, "text": "Caught on the trip. Goes to the kitchen when you are home.",
                        "bild": "/farm/fische/%s.png" % fid})
    return out


# ------------------------------------------------------------------ loot and defeat
def _mal(label, n):
    return "%s ×%d" % (label, n) if n > 1 else label


def beute(z, modul, defs):
    """What Duc found since the start, one entry per kind:
    [{"id": "item:<id>" | "roh:<id>" | "fisch:<id>" | "chip:<familie>", "label", "name", "n", "halten"}] -
    halten = what keeping it saves (one place: at most one full stack)."""
    from . import zustand
    e = aktiv(z)
    if not e:
        return []
    items = modul.get("items", {})
    vorher = {}
    for i in e["inventar"]:
        vorher[i] = vorher.get(i, 0) + 1
    jetzt = {}
    for i in z.get("inventar", []):
        jetzt[i] = jetzt.get(i, 0) + 1
    out = []
    for i, n in jetzt.items():
        n -= vorher.get(i, 0)
        if n > 0 and items.get(i, {}).get("art") not in NIE_BEUTE:
            name = items.get(i, {}).get("label") or i
            out.append({"id": "item:" + i, "name": name, "label": _mal(name, n), "n": n, "halten": min(n, zustand.stapel(modul, i))})
    r, st = e.get("ernte") or {}, _stapel(modul)
    for rid, n in (r.get("roh") or {}).items():
        if n:
            name = kuechen.daten(modul)["rohstoffe"][rid]["label"]
            out.append({"id": "roh:" + rid, "name": name, "label": _mal(name, n), "n": n, "halten": min(n, st["rohstoff"])})
    for fid, sterne in (r.get("fisch") or {}).items():
        if sterne:
            name = _fisch_label(modul, fid)
            out.append({"id": "fisch:" + fid, "name": name, "label": _mal(name, len(sterne)), "n": len(sterne),
                        "halten": min(len(sterne), st["fisch"])})
    for f, stufe in kampf.chip_pool(z)["pool"].items():
        if stufe > e["chips"].get(f, 0):
            try:
                label = kampf._chip(defs, f, stufe)["label"]
            except (KeyError, TypeError):
                label = f
            out.append({"id": "chip:" + f, "name": "Chip: " + label, "label": "Chip: " + label, "n": 1, "halten": 1})
    return out


def behalten(z, modul, defs, bid):
    """Duc picks the one piece he keeps (None = nothing)."""
    e = aktiv(z)
    if not e:
        raise ValueError("No expedition is running.")
    if bid is not None and bid not in [b["id"] for b in beute(z, modul, defs)]:
        raise ValueError("That is not part of the loot.")
    e["behalten"], e["gewaehlt"] = bid, True


def scheitern(z, modul, defs):
    """Defeat: everything found is lost except the chosen place (one piece or one stack); LP full, the snapshot is dropped.
    The phase jump happens in eden.py (weiter). -> lines for the report."""
    e = aktiv(z)
    if not e:
        return []
    keep, verloren, alles = e.get("behalten"), [], beute(z, modul, defs)
    behalten_label = None
    r = e.get("ernte") or {}
    for b in alles:
        halten = b["halten"] if b["id"] == keep else 0
        art, key = b["id"].split(":", 1)
        if art == "item":
            for _ in range(b["n"] - halten):
                z["inventar"].remove(key)
        elif art == "roh":
            r["roh"][key] = halten
        elif art == "fisch":
            r["fisch"][key] = sorted(r["fisch"][key], reverse=True)[:halten]       # the best ones stay
        elif not halten:
            c = kampf.chip_pool(z)
            alt = e["chips"].get(key, 0)
            if alt:
                c["pool"][key] = alt
            else:
                c["pool"].pop(key, None)
                for liste in c["plaetze"].values():
                    if key in liste:
                        liste.remove(key)
        if halten:
            behalten_label = _mal(b["name"], halten)
        if b["n"] > halten:
            verloren.append(_mal(b["name"], b["n"] - halten))
    ernte_einlagern(z, modul)                     # a kept stack of Timber or fish comes home with him
    kampf.lp_auffuellen(z)
    z.pop("expedition", None)
    flag = "expedition_%s_gescheitert" % e["id"]
    if flag not in z["flags"]:
        z["flags"].append(flag)
    zeilen = ["You wake up on the ship. Half a day is gone."]
    if behalten_label:
        zeilen.append("You still have: %s." % behalten_label)
    if verloren:
        zeilen.append("Lost: %s." % ", ".join(verloren))
    return zeilen


def ansicht(z, modul, defs):
    """For the client's defeat screen: the loot to choose from and the current choice."""
    e = aktiv(z)
    if not e:
        return None
    return {"id": e["id"], "beute": beute(z, modul, defs), "behalten": e.get("behalten"), "gewaehlt": bool(e.get("gewaehlt"))}


# ------------------------------------------------------------------ expedition screen (plugin eden-expedition, 26.10.2026)
def scout_stufe(z, defs):
    """Level of the Scout chip in the worn jacket (kampf.aufklaerung, Items): 0 = enemies hidden, 1 = who, 2 = + level."""
    return kampf.aufklaerung(z, defs) if defs.get("erweiterungen") is not None else 0


def wahl_info(z, defs, option, bild_fn):
    """What a frame choice leads to, for the expedition screen: a fight (who only with the Scout chip), going on, or
    the end of the trip. option = the raw event option (folgen, bei_fehlschlag)."""
    folgen = list(option.get("folgen", [])) + list(option.get("bei_fehlschlag", []))
    bid = next((f["kampf"] for f in folgen if "kampf" in f), None)
    weiter = any("weiter" in f for f in option.get("folgen", []) + option.get("bei_erfolg", []))
    out = {"kampf": None, "weiter": weiter or bool(bid), "ende": not weiter and not bid,
           "kampf_nur_fehlschlag": bool(bid) and not any("kampf" in f for f in option.get("folgen", []))}
    if bid and bid in defs.get("encounters", {}):
        b = defs["encounters"][bid]
        e = defs["enemies"][b["enemy"]]
        stufe, info = scout_stufe(z, defs), {"bekannt": False}
        if stufe >= 1 and e.get("halsband") is False and stufe < 2:     # the chip hears collars: no collar, no name
            info = {"bekannt": True, "name": "Animal", "bild": None}
        elif stufe >= 1:
            info = {"bekannt": True, "name": e["name"], "bild": bild_fn(e["sprite"], "avatar")}
            if stufe >= 2:
                lv = kampf.progress(z)["level"] if b.get("level") == "duc" else int(b["level"])
                t = kampf.threat(lv, kampf.progress(z)["level"])
                info.update(level=lv, bedrohung={"id": t[0], "label": t[1]})
        out["kampf"] = info
        out["verjagbar"] = not out["kampf_nur_fehlschlag"] and kampf.verjagbar(z, defs, bid)   # Duc 02.11.2026
    return out


# ------------------------------------------------------------------ rest sites (Duc 26.10.2026, Elden Ring principle)
# Resting at a rest frame (event field "rast": true): LP full, every enemy since the last rest comes back
# (z["ort_besiegt"] is emptied - without a rest a won frame stays quiet), and someone from the ship calls.
# Who calls: the three people aboard with the most trust; if the last call came from the first, now the second, then the
# third, then the first again. Texts: module/eden_rise/rast_anrufe.json (Story, builder rast_anrufe_eden_rise.py),
# per person and trust level 3 calls; each call has two short answers (+1 trust = 8 points).
RAST_ANRUFER = ("chiara", "rosi", "lola", "sophia", "lea", "holm", "toto", "maxwell", "jana")


def rast_texte(moddir):
    import json, os
    p = os.path.join(moddir, "rast_anrufe.json")
    return json.load(open(p, encoding="utf-8")).get("anrufe", {}) if os.path.isfile(p) else {}


def rast_anrufer(z):
    """-> pid of the caller after the rotation rule (top 3 by trust points)."""
    from . import zustand
    rang = sorted(RAST_ANRUFER, key=lambda pid: (-zustand.punkte(z, "vertrauen." + pid), RAST_ANRUFER.index(pid)))[:3]
    letzt = z.get("rast_anruf_letzt")
    return rang[(rang.index(letzt) + 1) % len(rang)] if letzt in rang else rang[0]


def rast_anruf(z, texte):
    """Pick the caller and a call they haven't made yet at their trust level. -> call dict or None (no text)."""
    pid = rast_anrufer(z)
    jetzt = int(z["werte"].get("vertrauen." + pid, 0))
    da = [int(x) for x in (texte.get(pid) or {}) if int(x) <= jetzt]     # texts for higher levels may still be missing:
    stufe = str(max(da)) if da else str(jetzt)                          # then the highest level below
    liste = (texte.get(pid) or {}).get(stufe) or []
    gehabt = z.setdefault("rast_anrufe_gehabt", [])
    for i, a in enumerate(liste):
        aid = "%s.%s.%d" % (pid, stufe, i)
        if aid not in gehabt:
            z["rast_anruf_letzt"] = pid
            gehabt.append(aid)
            return dict(a, id=aid, pid=pid)
    if liste:                                         # all heard: start again with the first one
        z["rast_anruf_letzt"] = pid
        return dict(liste[0], id="%s.%s.0" % (pid, stufe), pid=pid)
    return None


def rasten(z, moddir):
    """Rest: LP full, the path's enemies come back, the call. -> lines."""
    kampf.lp_auffuellen(z)
    z["ort_besiegt"] = []
    z["rast_fund_neu"] = False                         # the discovery card belongs to the arrival, not to the rest
    rast = z.setdefault("ort_rasten", [])
    if z.get("ort_frame") and z["ort_frame"] not in rast:
        rast.append(z["ort_frame"])
    z["rast_anruf"] = rast_anruf(z, rast_texte(moddir))
    return ["You rest by the fire. Your strength comes back, and so do the animals on the path."]


def rast_antwort(z, modul, index):
    """Duc answers the rest call: +1 trust (8 points) with the caller, the call is over."""
    from . import zustand
    a = z.get("rast_anruf")
    if not a:
        raise ValueError("Nobody is on the line.")
    antworten = a.get("antworten") or []
    if not 0 <= index < max(1, len(antworten)):
        raise ValueError("Unknown answer.")
    z["rast_anruf"] = None
    return zustand.folgen_anwenden(z, modul, [{"wert": "vertrauen." + a["pid"], "delta": 1}], frei=False)
