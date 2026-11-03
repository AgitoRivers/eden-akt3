# -*- coding: utf-8 -*-
"""Figurenrahmen (Duc 31.10.2026, Brain Trust; Probe zuerst nur Rosi): Die Werte schaffen den Kontext, nicht das Modell.

Live-Spieltest 31.10.2026: Das Modell verfehlte nach grossen Momenten den Rueckbezug in 11 von 11 Treffen, und seine eigenen
Erinnerungen trugen Witze weiter. Fuer eine Figur mit Eintrag in module/<id>/figurenrahmen.json gilt deshalb:
  - Getippter Text aendert nie Vertrauen oder Begehren. Zeit zusammen und gewaehlte Gesten zaehlen fest (Code).
  - Das Modell bekommt ein Faktenblatt aus dem Code statt seiner eigenen Erinnerungen.
  - Der Code waehlt das Thema der freien Szene und schreibt ihre erste Zeile; das Modell spielt von dort aus weiter.
  - Das Modell legt keine Momente in der Chronik an; das tun nur Gesten und Events."""
import json, os, re

from . import chronik, zustand

ZEIT_PUNKTE = (("vertrauen", 4), ("begehren", 2))    # je freie Szene, sobald Duc einen Zug gemacht hat
ZEIT_PUNKTE_CHIP = (("vertrauen", 2), ("begehren", 1))    # Szene mit Start-Chips: der Rest kommt ueber den Chip (Duc 01.11.2026)
CHIP_PUNKTE = {"vertrauen": (("vertrauen", 2),), "begehren": (("begehren", 2),), "beide": (("vertrauen", 1), ("begehren", 1))}
FRISCH_TAGE = 5                                      # so lange wartet ein Moment auf das naechste Treffen
ERLEBT_MAX = 12
MOMENT_RANG = ("intimate", "naehe_weit", "confession", "kiss", "naehe")     # stark -> schwach
_CACHE = {}


def daten(modul):
    pfad = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "module", modul.get("id", ""),
                        "figurenrahmen.json")
    try:
        mt = os.path.getmtime(pfad)
    except OSError:
        return {}
    c = _CACHE.get(pfad)
    if not c or c[0] != mt:
        c = _CACHE[pfad] = (mt, json.load(open(pfad, encoding="utf-8")))
    return c[1]


def figur(modul, pid):
    return (daten(modul).get("figuren") or {}).get(pid)


def gilt(modul, pid):
    return bool(figur(modul, pid))


def stand(z, pid):
    return z.setdefault("figurenrahmen", {}).setdefault(pid, {"gesehen": [], "erlebt": [], "momente": [], "abende": 0,
                                                              "vorschlag": 0})


def bedingung(z, pid, w):
    """{"flag": x, "nicht": {...}, "v": n, "b": n, "moment": x oder [x, y]}, alle muessen gelten."""
    for k, v in (w or {}).items():
        if k == "flag" and v not in z.get("flags", []):
            return False
        if k == "nicht" and bedingung(z, pid, v):
            return False
        if k == "v" and z["werte"].get("vertrauen." + pid, 0) < v:
            return False
        if k == "b" and z["werte"].get("begehren." + pid, 0) < v:
            return False
        if k == "moment" and not any(chronik.moment_zahl(z, pid, m) for m in ([v] if isinstance(v, str) else v)):
            return False
    return True


def _erster(z, pid, liste):
    return next((x["text"] for x in liste if bedingung(z, pid, x.get("wenn"))), "")


def fuellen(z, modul, pid, text):
    return text.replace("{anrede}", _erster(z, pid, figur(modul, pid).get("anrede") or []))


def alle_zeilen(moddir):
    """[(schluessel, figur, text)] fuer werkzeuge/eden_rise/vertonen_eden_rise.py: jede feste erste Zeile, je Anrede einmal."""
    with open(os.path.join(moddir, "figurenrahmen.json"), encoding="utf-8") as fh:
        figuren = json.load(fh)["figuren"]
    out = []
    for pid, f in figuren.items():
        anreden = list(dict.fromkeys(a["text"] for a in f.get("anrede") or []))
        for t in f.get("momente", []) + f.get("abende", []) + f.get("themen", []):
            if "{anrede}" not in t["einstieg"]:
                out.append(("rahmen.%s.%s" % (pid, t["id"]), pid, t["einstieg"]))
                continue
            for a in anreden:
                out.append(("rahmen.%s.%s.%s" % (pid, t["id"], a.lower().replace(" ", "_")), pid, t["einstieg"].replace("{anrede}", a)))
        ab = f.get("abschied") or {}
        saetze = [("nah.%s" % k, s) for k, s in (ab.get("nah") or {}).items()]
        saetze += [("%s.%s" % (v, b), s) for v, reihe in (ab.get("stand") or {}).items() for b, s in reihe.items()]
        for k, s in saetze:
            for a in (anreden if "{anrede}" in s else [""]):
                out.append(("rahmen.%s.abschied.%s%s" % (pid, k, "." + a.lower().replace(" ", "_") if a else ""), pid, s.replace("{anrede}", a)))
    return out


# ------------------------------------------------------------------ Faktenblatt
HINTERGRUND = "Her background, which Duc only knows if she tells him: "     # ihre Geschichte, nichts Gemeinsames (Duc 02.11.2026)


def faktenblatt(z, modul, pid):
    """Nur, was der Code weiss: Leiter-Flags, Chronik-Eintraege aus Gesten und Events, erlebte Themen."""
    f = figur(modul, pid)
    out = [x["text"] for x in f.get("fakten", []) if bedingung(z, pid, x.get("wenn"))]
    gesehen = set()
    for e in chronik.liste(z):
        if pid in e["wer"] and e["art"] in ("moment", "fakt", "geschenk", "andenken") and chronik.gueltig(z, e):
            zeile = "Day %d: %s" % (e["tag"], e["text"])
            if e["text"] not in gesehen:
                gesehen.add(e["text"])
                out.append(zeile)
    return out + stand(z, pid)["erlebt"]


def prompt_teile(z, modul, pid):
    f, name = figur(modul, pid), modul["personen"][pid]["name"].split()[0]
    teile = []
    alle = faktenblatt(z, modul, pid)
    hintergrund = [x[len(HINTERGRUND):] for x in alle if x.startswith(HINTERGRUND)]
    fakten = [x for x in alle if not x.startswith(HINTERGRUND)]
    if hintergrund:
        teile.append("[%s's own background - true, but Duc only knows it if she tells him, so never treat it as a memory you share]\n%s" % (name, "\n".join(hintergrund)))
    if fakten:
        teile.append("[What has really happened between %s and Duc - hard facts, never contradict them]\n%s" % (name, "\n".join(fakten)))
    haltung = _erster(z, pid, f.get("haltung") or [])
    if haltung:
        teile.append("[Where %s stands with Duc now]\n%s" % (name, haltung))
    regeln = [x["text"] for x in f.get("regeln", []) if bedingung(z, pid, x.get("wenn"))]
    if regeln:
        teile.append("[Rules for %s]\n- %s" % (name, "\n- ".join(regeln)))
    return teile


def erinnerung(z, modul, pid, n=4):
    """Fuer den Handy-Chat: was sie ueber Duc weiss."""
    if gilt(modul, pid):
        return [x for x in faktenblatt(z, modul, pid) if not x.startswith(HINTERGRUND)][-n:]
    return z["gedaechtnis"].get(pid, [])[-n:]


# ------------------------------------------------------------------ Thema der freien Szene
def szene_gilt(modul, s, figuren):
    return len(figuren) == 1 and gilt(modul, figuren[0]) and str(s.get("id", "")).startswith(("frei_", "date_"))


def _offene_momente(z, pid):
    erledigt = stand(z, pid)["momente"]
    return [e for e in chronik.liste(z) if e.get("moment") in MOMENT_RANG and pid in e["wer"] and e["nr"] not in erledigt
            and 0 < z["tag"] - e["tag"] <= FRISCH_TAGE and chronik.gueltig(z, e)]    # erst ab dem naechsten Tag: die Zeilen sagen "the other night" (Spieltest 01.11.2026)


def _laengst_her(st, liste):
    """Noch nie gesehen zuerst, in Reihenfolge der Liste; danach das am laengsten zurueckliegende."""
    frisch = [t for t in liste if t["id"] not in st["gesehen"]]
    return frisch[0] if frisch else min(liste, key=lambda t: st["gesehen"].index(t["id"])) if liste else None


def thema_fuer(z, modul, s, figuren):
    """-> Thema (Eintrag aus den Daten, mit "art") oder None. Noch nichts gebucht."""
    if not szene_gilt(modul, s, figuren):
        return None
    pid = figuren[0]
    f, st = figur(modul, pid), stand(z, pid)
    offen = _offene_momente(z, pid)
    for m in MOMENT_RANG:
        if any(e["moment"] == m for e in offen):
            passend = [t for t in f.get("momente", []) if t["moment"] == m
                       and chronik.moment_zahl(z, pid, m) <= t.get("bis_zahl", 99)]
            if passend:
                return dict(passend[0], art="moment")
    if s["id"].startswith("date_"):
        abende = f.get("abende") or []
        if abende:
            t = abende[st["abende"]] if st["abende"] < len(abende) else _laengst_her(st, abende)
            return dict(t, art="abend")
    t = _laengst_her(st, [x for x in f.get("themen", []) if bedingung(z, pid, x.get("wenn"))])
    return dict(t, art="thema") if t else None


def thema_buchen(z, modul, pid, t):
    st = stand(z, pid)
    if t["id"] in st["gesehen"]:
        st["gesehen"].remove(t["id"])
    st["gesehen"].append(t["id"])
    if t["art"] == "moment":
        st["momente"] += [e["nr"] for e in _offene_momente(z, pid)]
        chronik.aufgreifen(z, pid, MOMENT_RANG)
    if t["art"] == "abend":
        st["abende"] += 1
    if t.get("fakt"):
        st["erlebt"] = (st["erlebt"] + ["Day %d: %s" % (z["tag"], t["fakt"])])[-ERLEBT_MAX:]


def thema_hinweis(t):
    return ("[What this scene is about - background for you, never quote it. The player has just read her first line, so "
            "continue from it and do not change the subject on your own]\n%s" % t.get("regie", ""))


def szene_auswerten(z, modul, sz):
    """Feste Wirkung am Ende der freien Szene. Abende bringen ihre Stufe ueber "immer"."""
    s, figuren = sz["def"], [p for p in sz["figuren"]]
    if not szene_gilt(modul, s, figuren) or s["id"].startswith("date_") or not sz.get("zug"):
        return []
    zeilen = []
    for achse, n in (ZEIT_PUNKTE_CHIP if sz.get("chip_start") else ZEIT_PUNKTE):
        zeilen += zustand.punkte_add(z, modul, "%s.%s" % (achse, figuren[0]), n, deckel=zustand.GESPRAECH_DECKEL, quelle="szenen")
    return zeilen


# ------------------------------------------------------------------ Szenenende (Duc 01.11.2026)
NAH_GETIPPT = re.compile(r"\b(kiss\w*|mak\w+ out|caress\w*|breasts?|undress\w*)\b", re.I)
GESTE_ZEILE = re.compile(r"^Gesture: (.+) – it (lands|doesn't land)$")


def abschied_faellig(modul, sz):
    figuren = list(sz.get("figuren") or [])
    return bool(sz.get("zug") and not sz.get("abschluss") and szene_gilt(modul, sz["def"], figuren)
                and figur(modul, figuren[0]).get("abschied"))


def _bereich(stufe):
    return "niedrig" if stufe <= 1 else "mittel" if stufe <= 3 else "hoch"


def abschied_text(z, modul, pid, sz):
    """Fester Abschied nach Stand. Nach Naehe in dieser Szene die Variante "nah", auch wenn sie nur getippt war."""
    a = figur(modul, pid)["abschied"]
    v, b = _bereich(z["werte"].get("vertrauen." + pid, 0)), _bereich(z["werte"].get("begehren." + pid, 0))
    nah = any(e.get("moment") in MOMENT_RANG and pid in e["wer"] and e["tag"] == z["tag"] and e["phase"] == z["phase"]
              for e in chronik.liste(z)) or any(e["art"] == "duc" and NAH_GETIPPT.search(e["text"]) for e in sz["log"])
    return fuellen(z, modul, pid, a["nah"]["vertrauen_" + v] if nah else a["stand"]["vertrauen_" + v]["begehren_" + b])


CHANCE_NIEDRIG = 45                                    # darunter lag ein Fehlschlag am Attribut, sonst am Wurf


def rueckmeldung(modul):
    pfad = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "module", modul.get("id", ""), "rueckmeldung.json")
    try:
        mt = os.path.getmtime(pfad)
    except OSError:
        return {}
    c = _CACHE.get(pfad)
    if not c or c[0] != mt:
        c = _CACHE[pfad] = (mt, json.load(open(pfad, encoding="utf-8")))
    return c[1]


def _gesten_der_szene(z, modul, sz, pid):
    """Gesten aus dem Protokoll, mit Satz und ehrlichem Grund: Der Wurf entscheidet, also sagt der Grund nie, die Geste sei falsch."""
    from . import gesten as G
    alle = G.gesten(modul)
    text, out = rueckmeldung(modul), []
    for e in sz["log"]:
        for t in (e.get("zeilen") or []) if e["art"] == "folgen" else []:
            m = GESTE_ZEILE.match(t)
            if not m:
                continue
            gid = next((k for k, g in alle.items() if g["label"] == m.group(1)), None)
            ok = m.group(2) == "lands"
            satz = ((text.get("gesten") or {}).get(gid) or {}).get("ok" if ok else "nein", "")
            warum = ""
            if not ok and gid:
                g = alle[gid]
                bonus = G.LIEBLING_BONUS if G.liebling(modul, pid, gid) else 0
                warum = ("Your %s is still low." % g["attribut"].capitalize() if G.chance(z, modul, g["attribut"], g["sg"], bonus) < CHANCE_NIEDRIG
                         else "The dice were against you. Try again another day.")
            out.append({"id": gid, "label": m.group(1), "ok": ok, "satz": satz, "warum": warum})
    return out


def absage_text(z, modul, pid, art=None):
    """Ihre feste Absage: art (privat, nachhaken) oder nach Vertrauensstufe. -> Text oder None."""
    if not gilt(modul, pid):
        return None
    a = figur(modul, pid).get("absage") or {}
    satz = a.get(art) if art else a.get("vertrauen_" + _bereich(z["werte"].get("vertrauen." + pid, 0)))
    return fuellen(z, modul, pid, satz) if satz else None


def topf_kommentar(z, modul, pid, key, quelle):
    """Ihr Satz, wenn diese Quelle bei ihr nichts mehr bringt. -> Zeilen fuer die Anzeige."""
    if zustand.topf_platz(z, modul, key, quelle) != 0:
        return []
    f = figur(modul, pid) if gilt(modul, pid) else {}
    satz = (f.get("topf_voll") or {}).get(quelle)
    return ['%s: “%s”' % (modul["personen"][pid].get("kurz") or pid, fuellen(z, modul, pid, satz))] if satz else []


def _was_geschah(z, sz, pid):
    zeilen = [sz["thema_fakt"]] if sz.get("thema_fakt") else []
    for e in chronik.liste(z):
        if e.get("moment") and pid in e["wer"] and e["tag"] == z["tag"] and e["phase"] == z["phase"]:
            zeilen.append(e["text"])
    return list(dict.fromkeys(zeilen))[:3]


def _tipps(z, modul, pid, sz, gesten, werte):
    """Hoechstens ein Satz, was gut war, und einer fuers naechste Mal."""
    text = rueckmeldung(modul)
    fig = (text.get("figuren") or {}).get(pid) or {}
    lieb = next((fig.get("liebling", {}).get(g["id"]) for g in gesten if g["ok"] and fig.get("liebling", {}).get(g["id"])), "")
    chip = (fig.get("chip") or {}).get(sz.get("chip_achse") or "", "")
    gut = lieb or chip or next((g["satz"] for g in gesten if g["ok"] and g["satz"]), "")
    w = text.get("werte") or {}
    besser = ""
    for achse in ("vertrauen", "begehren"):
        if achse in werte and werte[achse]["delta"] < 0:
            besser = besser or (w.get(achse) or {}).get("minus", "")
    if not besser:
        for achse in ("vertrauen", "begehren"):
            if achse in werte and not werte[achse]["delta"] and not zustand.topf_platz(z, modul, "%s.%s" % (achse, pid), "szenen") \
                    and zustand.topf_platz(z, modul, "%s.%s" % (achse, pid), "szenen") is not None:
                besser = besser or fuellen(z, modul, pid, (figur(modul, pid).get("topf_voll") or {}).get("szenen", ""))
    if not besser:
        for achse in ("vertrauen", "begehren"):
            if achse in werte and not werte[achse]["delta"] and werte[achse]["am_deckel"]:
                besser = besser or (w.get(achse) or {}).get("deckel", "")
    if not besser:
        for achse in ("vertrauen", "begehren"):
            if achse in werte and not werte[achse]["delta"]:
                besser = besser or (w.get(achse) or {}).get("gleich", "")
    if not gut:
        for achse in ("vertrauen", "begehren"):
            if achse in werte and werte[achse]["delta"] > 0:
                gut = gut or (w.get(achse) or {}).get("plus", "")
    return {"gut": gut, "besser": besser}


def abschluss_daten(z, modul, sz, pid):
    """Was das Overlay zeigt, alles aus dem Code: was geschah, Gesten, Punkte und Stufen seit Szenenbeginn, zwei Tipps."""
    gesten = _gesten_der_szene(z, modul, sz, pid)
    start = sz.get("punkte_start") or {}
    werte = {}
    for achse in ("vertrauen", "begehren"):
        key = "%s.%s" % (achse, pid)
        if key in z["werte"]:
            jetzt = zustand.punkte(z, key)
            von = start.get(achse, jetzt)
            werte[achse] = {"delta": jetzt - von, "am_deckel": jetzt == zustand.GESPRAECH_DECKEL,
                            "stufe_von": zustand.stufe_aus(von), "stufe": z["werte"][key]}
    return {"titel": sz["def"]["titel"], "pid": pid, "fakt": sz.get("thema_fakt") or "", "was": _was_geschah(z, sz, pid),
            "gesten": gesten, "werte": werte, "tipps": _tipps(z, modul, pid, sz, gesten, werte)}


def chip_buchen(z, modul, pid, chip):
    """Start-Chip: feste Wirkung nach seiner Achse, bis zum Gespraechs-Deckel. -> Zeilen fuer die Anzeige."""
    punkte = CHIP_PUNKTE[chip["achse"]]
    if "begehren.%s" % pid not in z["werte"]:             # Jana, Megan, Ligeia: keine Begehren-Achse, jeder Ton zaehlt etwas fuers Vertrauen
        punkte = (("vertrauen", 2 if chip["achse"] == "vertrauen" else 1),)
    zeilen = []
    for achse, n in punkte:
        zeilen += zustand.punkte_add(z, modul, "%s.%s" % (achse, pid), n, deckel=zustand.GESPRAECH_DECKEL, quelle="szenen")
    return zeilen


# ------------------------------------------------------------------ Zeit zusammen
def vorschlag(z, modul, pid, nah):
    """Ihr Vorschlag aus den Daten; die Kategorie und damit die Wirkung stehen fest. -> (text, kategorie)"""
    f, st = figur(modul, pid), stand(z, pid)
    if nah and f.get("nah_vorschlag"):
        return '"%s"' % fuellen(z, modul, pid, f["nah_vorschlag"]), "romantik"
    liste = [x for x in f.get("vorschlaege", []) if bedingung(z, pid, x.get("wenn"))]
    if not liste:
        return '"Stay a while, right here with me."', "entspannung"
    v = liste[st["vorschlag"] % len(liste)]
    st["vorschlag"] += 1
    return '"%s"' % fuellen(z, modul, pid, v["text"]), v["kategorie"]
