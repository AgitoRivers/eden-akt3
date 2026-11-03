# -*- coding: utf-8 -*-
"""Buehne: was der Client zeigt - Hintergrund je Raum und Tageszeit, Outfit-Set je Figur, Sprite je Gefuehl.

Bilder kommen aus SillyTavern (dieselben Sets wie im Chat): characters\\<Name>\\ = Set 1, setN\\ = weitere Sets,
_name.txt = Set-Name, _prompt.txt = "Wearing: ..." (wird zur Outfit-Beschreibung im Prompt -> Text und Bild passen).
Sprites heissen <gefuehl>.png oder <gefuehl>-<n>.png (ST-Schema)."""
import hashlib, os, re

from .regeln import phase_wie, phase_passt

GEFUEHLE = ["admiration", "amusement", "anger", "annoyance", "approval", "caring", "confusion", "curiosity", "desire",
            "disappointment", "disapproval", "disgust", "embarrassment", "excitement", "fear", "gratitude", "grief",
            "joy", "love", "nervousness", "neutral", "optimism", "pride", "realization", "relief", "remorse",
            "sadness", "surprise"]
INTIM = ["climax", "intercourse"]
TAGESZEIT = {"fruehstueck": "tag", "tag": "tag", "nachmittag": "tag", "dinner": "abend", "abend": "abend", "nacht": "nacht"}
_SETS = {}


class SetListe(dict):
    """Sets einer Figur; Nachschlagen loest zusaetzlich personen.<pid>.set_alias auf (alter Name -> Ordnername, 25.10.2026:
    Rosis Sets wurden in ST umbenannt, die Events nennen die alten Namen). Aufzaehlen zeigt nur die echten Sets."""

    def __init__(self, sets, alias):
        super().__init__(sets)
        self.alias = {a: z for a, z in (alias or {}).items() if z in sets}

    def __contains__(self, name):
        return dict.__contains__(self, name) or name in self.alias

    def __getitem__(self, name):
        return dict.__getitem__(self, name if dict.__contains__(self, name) else self.alias.get(name, name))

    def get(self, name, default=None):
        return self[name] if name in self else default


def figur_ordner(cfg, modul, pid):
    """Nebenfiguren ohne ST-Karte liegen im Modul (module\\<id>\\figuren\\<Name>, 24.10.2026: Duc spielt sie nur in
    Eden), alle anderen in SillyTavern. Der Modul-Ordner hat Vorrang."""
    p = modul["personen"][pid]
    name = p.get("karte") or p.get("st_ordner") or p["name"]
    lokal = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "module", modul.get("id", ""),
                         "figuren", name)
    if os.path.isdir(lokal):
        return lokal
    return os.path.join(cfg["st_daten"], "characters", name)


def sets(cfg, modul, pid):
    """{Set-Name: {"ordner": "" | "setN", "outfit": "Wearing-Text", "dateien": {gefuehl: [dateien]}}}"""
    basis = figur_ordner(cfg, modul, pid)
    alias = modul["personen"][pid].get("set_alias")
    if basis in _SETS:
        return SetListe(_SETS[basis], alias)
    out = {}
    if os.path.isdir(basis):
        for unter in [""] + sorted(x for x in os.listdir(basis) if re.fullmatch(r"set\d+", x)):
            o = os.path.join(basis, unter)
            try:
                name = open(os.path.join(o, "_name.txt"), encoding="utf-8").read().strip()
            except OSError:
                name = unter or "Standard"
            outfit = ""
            try:
                prompt = open(os.path.join(o, "_prompt.txt"), encoding="utf-8").read()
                m = re.search(r"Wearing:\s*(.+)", prompt)
                outfit = m.group(1).strip().rstrip(".") if m else ""
            except OSError:
                pass
            dateien = {}
            for f in os.listdir(o):
                m = re.fullmatch(r"([a-z]+)(?:-\d+)?\.png", f)
                if m:
                    dateien.setdefault(m.group(1), []).append(f)
            out[name] = {"ordner": unter, "outfit": outfit, "dateien": dateien}
    _SETS[basis] = out
    return SetListe(out, alias)


def set_waehlen(cfg, modul, pid, s, phase, auftrag, z=None):
    """Plan-Vorgabe > Set-Regeln des Moduls (Ort/Phase) > freigeschaltetes Outfit (set_frei, Danzels Massstueck) > Standard-Set."""
    vorhanden = sets(cfg, modul, pid)
    if not vorhanden:
        return None
    p = modul["personen"][pid]
    wunsch = (auftrag or {}).get("set")
    if not wunsch:
        for r in p.get("set_regeln", []):
            if r.get("nur_date") and not str(s.get("id", "")).startswith("date_"):    # Jana: das rote Kleid nur beim Date (Duc 31.10.2026)
                continue
            if ("ort" not in r or r["ort"] == s["ort"]) and ("phase" not in r or phase_passt(phase, [r["phase"]])):
                wunsch = r["set"]
                break
    if not wunsch and z:
        wunsch = next((f["set"] for f in p.get("set_frei", []) if f["flag"] in z.get("flags", []) and f["set"] in vorhanden), None)
    wunsch = wunsch or p.get("set_standard")
    return wunsch if wunsch in vorhanden else next(iter(vorhanden))


def sprite(cfg, modul, pid, setname, gefuehl, schluessel=""):
    """URL-Pfad fuer den Client; Variante stabil je Eintrag (gleiche Antwort = gleiches Bild)."""
    s = sets(cfg, modul, pid).get(setname)
    if not s:
        return None
    kandidaten = s["dateien"].get(gefuehl) or s["dateien"].get("neutral") or next(iter(s["dateien"].values()), [])
    if not kandidaten:
        return None
    i = int(hashlib.md5(schluessel.encode()).hexdigest(), 16) % len(kandidaten)
    return "/sprite/%s/%s/%s" % (pid, s["ordner"] or "_", sorted(kandidaten)[i])


def wo_ist(z, modul, pid):
    """Raum-ID, in dem sich die Person laut Tagesablauf gerade aufhaelt, oder None (nicht an Bord/im Dorf).
    Eine Stelle fuer Karte, Missions-Buehne und Kabinen-Anruf. Personen mit "von_bord_ab_tag" (Holm) sind ab
    diesem Tag weg."""
    p = modul["personen"].get(pid) or {}
    ab_tag = p.get("von_bord_ab_tag")
    if ab_tag and z["tag"] >= ab_tag:
        return None
    if p.get("weg_flag") and p["weg_flag"] in z.get("flags", []):     # z. B. holm_evakuiert (eden_rise)
        return None
    ab = p.get("ablauf") or {}
    rid = ab.get(z["phase"], ab.get(phase_wie(z["phase"]), ab.get("*")))
    return rid if rid in modul["raeume"] else None


def hintergrund(modul, raum_id, phase):
    bild = modul["raeume"][raum_id].get("bild") or {}
    zeit = TAGESZEIT.get(phase, "tag")
    datei = bild.get(zeit) or (bild.get("nacht") if zeit == "abend" else None) or bild.get("tag") or bild.get("nacht")
    return "/bg/" + datei if datei else None


def szenenbild(modul, s, phase):
    """Bild einer Szene: eigenes Szenenbild (s["bild"], z. B. Hubschrauber, Sturm) vor dem Raum-Hintergrund."""
    return "/bg/" + s["bild"] if s.get("bild") else hintergrund(modul, s["ort"], phase)


def sprite_datei(cfg, modul, pid, ordner, datei):
    """Pfad pruefen (nur Dateien aus den Sets der Figur) und liefern."""
    if not re.fullmatch(r"[a-z]+(?:-\d+)?\.png", datei) or not re.fullmatch(r"_|set\d+", ordner):
        return None
    pfad = os.path.join(figur_ordner(cfg, modul, pid), "" if ordner == "_" else ordner, datei)
    return pfad if os.path.isfile(pfad) else None


def hintergrund_datei(cfg, datei):
    if not re.fullmatch(r"[\w\- ]+\.(png|jpg|jpeg|webp)", datei):
        return None
    pfad = os.path.join(cfg["st_daten"], "backgrounds", datei)
    return pfad if os.path.isfile(pfad) else None
