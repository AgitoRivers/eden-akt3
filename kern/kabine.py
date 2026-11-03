# -*- coding: utf-8 -*-
"""Ducs Kabine (17.10.2026): statt einer der Szenen einer Wahl-Phase zieht sich Duc in seine Kabine zurueck.

Nur aktiv, wenn das Modul einen Abschnitt "kabine" hat - ohne ihn aendert sich am Spiel nichts.
  modul["kabine"] = {"ort": "duc_cabin",                       # Raum (Bild tag/nacht kommt von dort)
                     "hotspots": {"truhe": [x, y], ...},          # Leuchtpunkte in % des Bildes (Client)
                     "kein_handy": ["petru"],                     # wer nicht anrufbar ist
                     "anruf_orte": {"holm": "a hospital bed ..."},   # wo jemand beim Anruf ist (sonst Tagesablauf)
                     "schmuggel_faktor": 0.5}                     # Kontrollrisiko fuer Schmuggelware in der Truhe

In der Kabine:
  * Truhe: Gegenstaende zwischen Inventar (6 Plaetze) und Truhe verschieben - kostenlos, beliebig oft. Was in der
    Truhe liegt, wirkt nicht (Boni und Glücksbringer nur am Mann). Andenken bleiben immer bei Duc.
  * Keepsake Box (26.10.2026) - Vitrine aller Andenken, die ein Event vergibt (modul item "vitrine"); fehlende als Umriss,
    eigene mit Beschreibung und Echo (vertonte Zeile der Gebenden, item "echo").
  * Anrufen  - Videoanruf als kurze Szene (Vertrauen, Gedaechtnis, Chronik wie jede Szene)
  * Boxhandschuhe - Klick startet das Training mit Maxwell (Kampf, eden.py training_kampf, kostet 1 Aktion).
    Das Attribut-Training der Kabine ist am 25.10.2026 entfallen (Duc: Training ist immer ein Dialog mit Maxwell).
  * Modell B (24.10.2026, Duc): Die Kabine ist ein Drehkreuz und kostet keine Phase; Ausruhen entfaellt - jede neue
    Phase fuellt Lebenspunkte und Ausdauer wieder auf (kern/plan.py). Zurueck geht es immer zur Wahl derselben Phase.
"""
from . import buehne, gesten, handy, zustand


def aktiv(modul):
    return bool(modul.get("kabine"))


def _k(modul):
    return modul.get("kabine") or {}


def _init(z):
    z.setdefault("truhe", [])


def ort(modul):
    return _k(modul).get("ort") or "duc_cabin"


# ------------------------------------------------------------------ Betreten / Verlassen
def gesperrt(z, fixplan=None):
    """Grund (deutsch), warum die Kabine in dieser Wahl-Phase nicht geht, sonst None.
    Wendepunkte (Festa, Sturm ...) und Verabredungen lassen sich nicht in der Kabine aussitzen."""
    inhalt = ((z.get("plan") or {}).get("phasen") or {}).get(z["phase"]) or {}
    if inhalt.get("fix") or inhalt.get("fest") or inhalt.get("dynamisch") or \
            "%d/%s" % (z["tag"], z["phase"]) in (fixplan or {}):
        return "Heute Abend passiert etwas, das du nicht verpassen kannst."
    if any(str(s.get("id", "")).startswith("date_") for s in inhalt.get("szenen", [])):
        return "Du bist verabredet."
    return None


def betreten(z, modul, fixplan=None):
    if not aktiv(modul):
        raise ValueError("In diesem Modul gibt es keine Kabine.")
    if z["status"] != "wahl":
        raise ValueError("In die Kabine geht es nur statt einer Szene.")
    grund = gesperrt(z, fixplan)
    if grund:
        raise ValueError(grund)
    _init(z)
    z["kabine"] = {"tag": z["tag"], "phase": z["phase"], "vorher_bild": z.get("letztes_bild")}
    z["status"] = "kabine"
    z["letztes_bild"] = buehne.hintergrund(modul, ort(modul), z["phase"])


def zurueck(z):
    if z["status"] != "kabine":
        raise ValueError("Du bist gerade nicht in deiner Kabine.")
    z["letztes_bild"] = (z.get("kabine") or {}).get("vorher_bild") or z.get("letztes_bild")
    z["kabine"] = None
    z["status"] = "wahl"                 # z["optionen"] steht noch - dieselbe Wahl wie vorher


def _pruefen(z):
    if z["status"] != "kabine" or not z.get("kabine"):
        raise ValueError("Du bist gerade nicht in deiner Kabine.")


# ------------------------------------------------------------------ Truhe
def truhe(z, modul, iid, richtung, n=1):
    """Ein Stueck oder einen ganzen Stapel (n, Stapeln 28.10.2026) hinein- oder herausnehmen; heraus nur, soweit Platz ist."""
    _pruefen(z)
    _init(z)
    it = modul["items"].get(iid)
    if not it:
        raise ValueError("Unbekannter Gegenstand.")
    if it.get("art") == "andenken":
        raise ValueError("Andenken bleiben bei dir.")
    n = max(1, min(int(n or 1), zustand.stapel(modul, iid)))
    if richtung == "rein":
        if iid not in z["inventar"]:
            raise ValueError("Das trägst du nicht bei dir.")
        for _ in range(min(n, z["inventar"].count(iid))):
            z["inventar"].remove(iid)
            z["truhe"].append(iid)
    elif richtung == "raus":
        if iid not in z["truhe"]:
            raise ValueError("Das liegt nicht in der Truhe.")
        if not zustand.platz_fuer(z, modul, iid):
            raise ValueError("All %d slots are full – put something in the chest first." % zustand.inventar_plaetze(z, modul))
        for _ in range(min(n, z["truhe"].count(iid))):
            if not zustand.platz_fuer(z, modul, iid):
                break
            z["truhe"].remove(iid)
            z["inventar"].append(iid)
    else:
        raise ValueError("Unbekannte Richtung.")


# ------------------------------------------------------------------ Ausruhen
def ausruhen(z, modul):
    """Entfaellt seit Modell B (24.10.2026): jede neue Phase fuellt Lebenspunkte und Ausdauer auf."""
    raise ValueError("Ausruhen gibt es nicht mehr – die nächste Phase bringt dich von selbst wieder zu Kräften.")
    _pruefen(z)
    if "energie" not in z["werte"]:
        raise ValueError("Ausruhen bringt in diesem Modul nichts.")
    lo, hi = zustand.bereich(modul, "energie")
    if z["werte"]["energie"] >= hi:
        raise ValueError("Du bist schon voller Energie.")
    zeilen = zustand.folgen_anwenden(z, modul, [{"wert": "energie", "delta": 1}])
    return "Ausgeruht", "Eine Stunde Schlaf in der Koje, Tür zu, Handy auf lautlos.", zeilen


# ------------------------------------------------------------------ Anrufen
def wo(z, modul, pid):
    """Wo die Person beim Anruf gerade ist (englisch, fuer die Szene) + Raum-ID fuer ihr Outfit."""
    k = _k(modul)
    if pid in (k.get("anruf_orte") or {}):
        return k["anruf_orte"][pid], None
    rid = buehne.wo_ist(z, modul, pid)
    if rid:
        return modul["raeume"][rid]["label"], rid
    if modul["personen"][pid].get("ablauf"):          # hat einen Tagesablauf, ist aber nicht mehr da (Holm ab Tag 2)
        return "far away from the boat", None
    return "somewhere on board", None


def kontakte(z, modul):
    k = _k(modul)
    aus = set(k.get("kein_handy") or [])
    bekannt = z.get("bekannt") or list(modul["personen"])
    return [pid for pid in modul["personen"] if pid in bekannt and pid not in aus]


def anruf_szene(z, modul, pid, cfg):
    """Videoanruf als kurze Szene: Duc in der Kabine (Hintergrund), sie an ihrem Ort (Outfit von dort)."""
    _pruefen(z)
    if pid not in kontakte(z, modul):
        raise ValueError("Diese Nummer hast du nicht.")
    p = modul["personen"][pid]
    vorname = p["name"].split()[0]
    wo_text, rid = wo(z, modul, pid)
    auftrag = {"will": "to talk with Duc on this call - about her day, him, whatever is on her mind",
               "grenze": "it is only a phone call: no touching, nothing handed over, nobody else joins"}
    setname = buehne.set_waehlen(cfg, modul, pid, {"ort": rid or ort(modul)}, z["phase"], None)
    if setname:
        auftrag["set"] = setname
    return {"id": "anruf_%s_t%d_%s" % (pid, z["tag"], z["phase"]), "titel": "Anruf · %s" % vorname,
            "ort": ort(modul), "anwesend": [pid], "anruf": True, "anruf_wo": wo_text, "max_zuege": 4,
            "aktion": 1,                                   # Modell B: ein Anruf kostet 1 Aktion, nicht die Phase
            "ausgangslage": "Duc video-calls %s from his cabin. She picks up; she is at %s. They can only see and "
                            "hear each other on the phone." % (vorname, wo_text),
            "figuren": {pid: auftrag}, "ausgaenge": [], "immer": []}


# ------------------------------------------------------------------ Abschluss einer Kabinen-Phase ohne Szene
def abschluss(z, modul, titel, kurz, bogen_von):
    """Die Phase zaehlt als verbracht: Eintrag in 'heute', danach koennen andere Duc schreiben (wie nach Szenen).
    -> Zeilen (Handy-Hinweise)."""
    z["heute"].append({"phase": z["phase"], "szene": "kabine", "titel": titel, "anwesend": [],
                       "kurz": "Duc spent the %s alone in his cabin." % z["phase"], "ausgaenge": [], "auftraege": {}})
    z["kabine"] = None
    neu = handy.nach_szene(z, modul, {"titel": titel}, [], bogen_von)
    return ["📱 Message from %s" % modul["personen"][pid]["name"].split()[0] for pid in neu]


# ------------------------------------------------------------------ Ansicht fuer den Client
def ansicht(z, modul, cfg, item_bild):
    _init(z)
    k = _k(modul)
    def ware(iid, n=1):
        it = modul["items"].get(iid, {"label": iid})
        eff = it.get("effekt") or {}
        return {"id": iid, "label": it["label"], "art": it.get("art"), "text": it.get("text", ""),
                "wirkung_text": it.get("wirkung_text"), "bild": item_bild(iid),
                "n": n, "stapel": zustand.stapel(modul, iid),
                "schmuggel": it.get("art") == "schmuggel",
                "wirkung": ("%s +%d" % (eff["bonus"][0].capitalize(), eff["bonus"][1])) if eff.get("bonus")
                else ("Vorteil %s" % eff["vorteil"].capitalize()) if eff.get("vorteil") else ""}
    kont = []
    for pid in kontakte(z, modul):
        p = modul["personen"][pid]
        wo_text, rid = wo(z, modul, pid)
        setname = buehne.set_waehlen(cfg, modul, pid, {"ort": rid or ort(modul)}, z["phase"], None)
        kont.append({"id": pid, "name": p["name"], "wo": wo_text, "romanzierbar": bool(p.get("romanzierbar")),
                     "vertrauen": z["werte"].get("vertrauen." + pid),
                     "avatar": buehne.sprite(cfg, modul, pid, setname, "neutral", pid) if setname else None})
    kont.sort(key=lambda x: (not x["romanzierbar"], -(x["vertrauen"] or 0)))
    # Keepsake Box (26.10.2026): alle Andenken der Vitrine, fehlende nur als Umriss (ohne Namen); Echo nur bei eigenen
    vitrine = []
    for iid, it in modul["items"].items():
        if not it.get("vitrine"):
            continue
        da = iid in z["inventar"]
        e = it.get("echo") if da else None
        label = (it.get("titel_je_bild") or {}).get((z.get("selfie_bilder") or {}).get(iid)) or it["label"]
        vitrine.append({"id": iid, "da": da, "label": label if da else "", "text": it.get("text", "") if da else "",
                        "bild": item_bild(iid) if da else None,
                        "echo": dict(e, name=gesten.kurz(modul, e["wer"])) if e else None})
    lo, hi = zustand.bereich(modul, "energie") if "energie" in modul.get("werte", {}) else (0, 0)
    return {"bild": buehne.hintergrund(modul, ort(modul), z["phase"]), "hotspots": k.get("hotspots") or {},
            "bei_dir": [ware(i, n) for i, n in zustand.stapel_liste(modul, z["inventar"])
                        if modul["items"].get(i, {}).get("art") != "andenken"],
            "andenken": [ware(i) for i in z["inventar"] if modul["items"].get(i, {}).get("art") == "andenken"],
            "vitrine": vitrine,
            "truhe": [ware(i, n) for i, n in zustand.stapel_liste(modul, [i for i in z["truhe"] if i in modul["items"]])],
            "plaetze": zustand.inventar_plaetze(z, modul), "belegt": zustand.belegt(z, modul),
            "schmuggel_faktor": k.get("schmuggel_faktor", 0.5),
            "kontakte": kont, "energie": z["werte"].get("energie"), "energie_max": hi}
