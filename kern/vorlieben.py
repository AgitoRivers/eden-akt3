# -*- coding: utf-8 -*-
"""Entdeckte Vorlieben (18.10.2026) - was Duc ueber den Geschmack der Figuren weiss, getrennt von der Wirkung.

Die tatsaechliche Geschenkwirkung steht im Modul (items[].geschenk, kern/handel.py) und aendert sich hier nie. Dieses
Modul merkt sich nur pro Spielstand, welche Vorlieben Duc entdeckt hat - und woher:
  geschenk  nach der Uebergabe (liebt/mag -> "mag", mag nicht/hasst -> "mag_nicht"; neutral: kein Eintrag; peinlich,
            zu frueh oder fuer jemand anderen gedacht: kein Eintrag - ueber ihren Geschmack sagt das nichts)
  gericht   Duc kocht fuer genau eine Person (liebt/gut -> mag, Ekel -> mag_nicht)
  tratsch   das Dorfohr (rollen "dorfohr") verraet ab Vertrauen 2 einmal am Tag eine Vorliebe, in einer Szene mit ihr
            oder beim Einkauf in ihrem Laden
  story     Folgen-Baustein {"vorliebe": {"figur", "item", "reaktion"}} in Events, Missionen, Szenen
Freier KI-Dialog legt nie etwas fest. Bereits Bekanntes wird nicht doppelt eingetragen und nicht erneut gemeldet.
Eintrag: {figur, item, reaktion, quelle, tag, text, gelesen, gemeldet} - "gemeldet" heisst: die Lavendel-Meldung
lief schon (Neuladen spielt sie nicht erneut ab); "gelesen" erst, wenn das Detail im Figurenprofil angezeigt wurde."""
import random

from . import rollen

REAKTIONEN = ("mag", "mag_nicht")
TRATSCH_AB = 2


def liste(z):
    return z.setdefault("vorlieben", [])


def bekannt(z, figur, item):
    return next((v for v in liste(z) if v["figur"] == figur and v["item"] == item), None)


def _pron(modul, pid):
    """Englisches Pronomen fuer die Anzeige (das Modul fuehrt "er"/"sie")."""
    p = (modul["personen"].get(pid) or {}).get("pronomen", "sie")
    return {"er": "he", "sie": "she"}.get(p, p)


def _name(modul, pid):
    p = modul["personen"].get(pid) or {}
    k = p.get("kurz") or ""
    return p.get("name", pid).split()[-1] if k.startswith("the ") else (k or p.get("name", pid).split()[0])


def _text(modul, figur, item, reaktion, quelle, stufe=None):
    sie = _pron(modul, figur).capitalize()
    label = (modul["items"].get(item) or {}).get("label", item)
    if quelle == "geschenk":
        if reaktion == "mag":
            return "%s loves it." % sie if stufe == 2 else "%s is happy with this gift." % sie
        return "%s doesn't know what to do with it." % sie if stufe != "hasst" else "%s hated it." % sie
    if quelle == "gericht":
        return ("%s cleaned the plate." % sie) if reaktion == "mag" else ("%s barely touched it." % sie)
    if quelle == "tratsch":                              # Alvas Stimme (Wiki): warm, spoettisch, der eine Satz sitzt
        wer = _name(modul, rollen.rolle(modul, "dorfohr") or "")
        if reaktion == "mag":
            return "%s leans over the bar: “%s would drop everything for %s. You didn't hear it from me.”" % (
                wer, _name(modul, figur), label)
        return "%s leans over the bar: “%s? Don't even think about %s. Trust me.”" % (wer, _name(modul, figur), label)
    return ("Now you know: %s likes that." % sie) if reaktion == "mag" else ("Now you know: %s doesn't like that." % sie)


def entdecken(z, modul, figur, item, reaktion, quelle, text=None, stufe=None):
    """Neue Vorliebe eintragen -> Eintrag oder None (unbekannte Figur/Gegenstand, schon bekannt, falsche Reaktion)."""
    if reaktion not in REAKTIONEN or figur not in modul["personen"] or item not in modul.get("items", {}):
        return None
    if bekannt(z, figur, item):
        return None
    e = {"figur": figur, "item": item, "reaktion": reaktion, "quelle": quelle, "tag": z.get("tag", 1),
         "text": text or _text(modul, figur, item, reaktion, quelle, stufe), "gelesen": False, "gemeldet": False}
    liste(z).append(e)
    return e


def aus_wertung(w):
    """Geschenkwertung (2 liebt, 1 mag, 0 neutral, -1 mag nicht/hasst) -> Reaktion oder None."""
    if w is None or isinstance(w, str):
        return None
    return "mag" if w >= 1 else "mag_nicht" if w <= -1 else None


def aus_geschenk(z, modul, figur, item, w):
    r = aus_wertung(w)
    return entdecken(z, modul, figur, item, r, "geschenk", stufe=w) if r else None


def aus_gericht(z, modul, figur, item, stufe):
    r = "mag" if stufe in ("liebt", "gut") else "mag_nicht" if stufe == "ekel" else None
    return entdecken(z, modul, figur, item, r, "gericht") if r else None


def aus_folge(z, modul, f):
    """Story-Effekt {"vorliebe": {"figur", "item", "reaktion", "text"?}} -> Zeilen fuer die Anzeige."""
    v = f.get("vorliebe") or {}
    e = entdecken(z, modul, v.get("figur"), v.get("item"), v.get("reaktion"), "story", text=v.get("text"))
    return ["♡ Discovered: %s %s %s" % (_name(modul, e["figur"]), "likes" if e["reaktion"] == "mag" else "doesn't like",
                                        modul["items"][e["item"]]["label"])] if e else []


def tratsch(z, modul, anlass=""):
    """Das Dorfohr verraet einmal am Tag eine noch unbekannte Vorliebe (ab Vertrauen 2). -> Eintrag oder None."""
    wer = rollen.rolle(modul, "dorfohr")
    if not wer or z["werte"].get("vertrauen." + wer, 0) < TRATSCH_AB or z.get("vorlieben_tratsch") == z.get("tag"):
        return None
    kand = []
    bekannte = set(z.get("bekannt") or modul["personen"])
    for iid, it in modul.get("items", {}).items():
        g = it.get("geschenk") or {}
        if it.get("nur_fuer") or it.get("intim") or not g:
            continue
        for pid, w in g.items():
            if pid == wer or pid not in bekannte or pid not in modul["personen"] or bekannt(z, pid, iid):
                continue
            if w >= 2 or w <= -1:                       # Tratsch ueber deutliche Vorlieben, nicht ueber "mag"
                kand.append((pid, iid, "mag" if w >= 1 else "mag_nicht"))
    if not kand:
        return None
    z["vorlieben_tratsch"] = z.get("tag")
    pid, iid, r = random.Random("%s-%s-tratsch" % (z.get("id"), z.get("tag"))).choice(sorted(kand))
    return entdecken(z, modul, pid, iid, r, "tratsch")


def melden(z, schluessel):
    """Die Lavendel-Meldung lief (oder wurde geschlossen) - beim Neuladen nicht wiederholen."""
    for v in liste(z):
        if "%s|%s" % (v["figur"], v["item"]) in schluessel:
            v["gemeldet"] = True


def lesen(z, figur, item):
    v = bekannt(z, figur, item)
    if v:
        v["gelesen"] = True
        v["gemeldet"] = True


def angleichen(z, modul):
    z["vorlieben"] = [v for v in z.get("vorlieben", []) if v.get("figur") in modul["personen"]
                      and v.get("item") in modul.get("items", {})]


def ansicht(z, modul, bild):
    """Fuer den Client: je Figur ihre entdeckten Vorlieben (mit Bild), dazu die noch nicht gemeldeten."""
    out, neu = {}, []
    for v in liste(z):
        it = modul["items"].get(v["item"]) or {}
        e = dict(v, label=it.get("label", v["item"]), bild=bild(v["item"]), name=_name(modul, v["figur"]),
                 quelle_text={"geschenk": "found out with a gift", "gericht": "found out while cooking",
                              "tratsch": "heard in the village", "story": "learned in conversation"}.get(v["quelle"], v["quelle"]))
        out.setdefault(v["figur"], []).append(e)
        if not v.get("gemeldet"):
            neu.append(e)
    return {"je_figur": out, "neu": neu}
