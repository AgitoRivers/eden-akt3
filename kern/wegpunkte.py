# -*- coding: utf-8 -*-
"""Fast travel in location chapters (Duc + Brain Trust 29.10.2026, like the expedition flags in Clair Obscur).

Every chapter starts at its first frame, the waypoint at the entrance. From there Duc either sets out on foot (as
before) or travels straight to a rest site he has already found on an earlier visit (z["rast_gefunden"] keeps every
frame he ever reached). At a rest site, before a choice, he can travel on to another found rest site of the chapter.

Rules (the phase mechanic stays: a defeat still wakes Duc on the ship, the phase is gone):
- Targets are rest frames ("rast": true) reachable from the start frame over "weiter". Story re-entries of a place
  (the Mountains: "Back at the Tower", "Back at the Bergerie") stay start frames - walking from the very beginning
  would replay the first meeting with Wolff - and the waypoint simply sits on them.
- From the entrance every found waypoint is open: the decisions on the way were made on the earlier visit (flags).
- From a rest site only waypoints that do not lie before the last locked frame ("sperre") of this trip: travelling must
  not replay a decision (the same rule as "Go back").
- Travelling heals nothing and does not wake the animals - that is what resting is for. It starts the expedition
  snapshot exactly like the first step on foot would.
- Each card says how many fights lie on the way from the entrance (skipped from the entrance, nothing more).

State: z["ort_start"] = first frame of this visit (eden.ort_betreten). The rest lives in eden.py (ort_frame, ort_weg)."""
from . import regeln
def _ziele_von(o, z):
    """Frames an option leads to. A conditional "weiter" list goes where the engine would go now: the first entry whose
    condition holds (so a shortcut Duc hasn't opened doesn't shorten the way)."""
    for f in list(o.get("folgen", [])) + list(o.get("bei_erfolg", [])) + list(o.get("bei_fehlschlag", [])):
        w = f.get("weiter") if isinstance(f, dict) else None
        if isinstance(w, str):
            yield w
        elif isinstance(w, list):
            x = next((x for x in w if x.get("id") and regeln.gilt(x.get("wenn"), z)), None)
            if x:
                yield x["id"]


def _kaempfe(e):
    return any("kampf" in f for o in e.get("optionen", []) for f in o.get("folgen", []))


def karte(idx, start, z):
    """Breadth-first over "weiter": {frame: (steps from the start, fights on the shortest way up to, not incl., it)}."""
    out = {start: (0, 0)}
    rand = [start]
    while rand:
        neu = []
        for fid in rand:
            e = idx.get(fid)
            if not e:
                continue
            schritte, kaempfe = out[fid]
            k = kaempfe + (1 if _kaempfe(e) else 0)
            for o in e.get("optionen", []):
                for ziel in _ziele_von(o, z):
                    if ziel in idx and (ziel not in out or out[ziel][0] > schritte + 1):
                        out[ziel] = (schritte + 1, k)
                        neu.append(ziel)
        rand = neu
    return out


def _alle(z, idx):
    """All found rest sites reachable from this visit's start: [{"id", "titel", "bild", "schritte", "kaempfe"}]."""
    start = z.get("ort_start")
    if not start or start not in idx:
        return [], {}
    k = karte(idx, start, z)
    gefunden = set(z.get("rast_gefunden") or [])
    out = [{"id": fid, "titel": idx[fid]["titel"], "bild": idx[fid].get("bild"), "schritte": s, "kaempfe": n}
           for fid, (s, n) in k.items() if fid != start and idx[fid].get("rast") and fid in gefunden]
    out.sort(key=lambda x: (x["schritte"], x["titel"]))
    return out, k


def ziele(z, idx):
    """Where Duc can travel from the frame that is open now -> {"von": "eingang"|"rast", "ziele": [...]} or None."""
    offen = z.get("event") or {}
    hier = offen.get("id")
    e = idx.get(hier) or {}
    if not z.get("ort_aktiv") or offen.get("ergebnis") or z.get("status") != "ereignis":
        return None
    weg = z.get("ort_weg") or []
    am_eingang = hier == z.get("ort_start") and len(weg) <= 1
    if not am_eingang and not e.get("rast"):
        return None
    alle, k = _alle(z, idx)
    if not am_eingang:                                  # from a rest site: never back past the last locked frame
        grenze = k.get(z.get("ort_sperre_frame"), (0, 0))[0]
        alle = [w for w in alle if w["schritte"] >= grenze]
    alle = [w for w in alle if w["id"] != hier]
    if not alle:
        return None
    return {"von": "eingang" if am_eingang else "rast", "ziele": alle}


def expedition_von(idx, start):
    """The expedition id the start frame would start on foot (folgen {"expedition": id}) or None."""
    for o in (idx.get(start) or {}).get("optionen", []):
        for f in o.get("folgen", []):
            if isinstance(f.get("expedition"), str) and f["expedition"] != "ende":
                return f["expedition"]
    return None
