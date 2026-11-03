# -*- coding: utf-8 -*-
r"""Events der Hauptstory eden_rise (B5, 18.10.2026) - die vier Ereignisarten plus Duell, Auftritt, Abend.

Daten: module\eden_rise\ereignisse.json (werkzeuge\eden_rise\ereignisse_*.py, Entwurf entwuerfe\eden-ereignisarten.html).
  bordrat  nachts: eine Person stellt das Problem vor, zwei Positionen links/rechts, dritter Weg/Versprechen/Bordregel
  handy    Anruf/Nachricht, auf die Duc sofort reagieren muss
  gag1     eine Person tut etwas, das andere trifft (Buehne, Betroffene oben rechts)
  gagv     zwei gegeneinander, Zuschauer in der Mitte (Versus); duell/auftritt laufen ueber denselben Bildschirm
  abend    persoenliche Abende (Lola, Alva), an Vertrauen gebunden; koennen in eine Szene fuehren
Ziehung in Stufen je Phase (Duc 25.10.2026): Pflicht -> (Nacht) Bordrat -> ein Zufalls-Event -> Handy. Nach jedem
geschlossenen Event zieht eden.py die naechste Stufe; keine Stufe kostet die Phase. Nie in exklusiven Story-Phasen, nie
zweimal im Durchlauf. Bordrat: in 3 von 4 freien Naechten (ab Tag 2), sonst eine Meldung "ruhige Nacht", damit es nicht
wie ein Fehler aussieht. Handy: eigene Spur, hoechstens zwei am Tag. Zufall je Durchlauf/Tag/Phase fest (Seed).
Erklaert fuer Duc: docs/wiki/systeme/interaktion.md, Abschnitt "Tagesablauf und Events".
Folgen setzt der Code um (Grundlagen-Seite): Punkte auf Vertrauen/Begehren, Rueckhalt 0-100, Versprechen (gehalten
+8 / gebrochen -16), Bordregeln (bis 5, wirken jeden Abend), Running Gags (Zaehler + Flags gag_<id>_<stufe>), Klatsch
und Momente in die Chronik. Kein Event beruehrt die Faelle (Pruefung beim Bau der Events)."""
import collections, copy, json, os, random, re

from . import album, charms, chronik, moral, regeln, rollen, wuerfel, zustand

_CACHE = {}
CHANCE = {"fruehstueck": 0.35, "tag": 0.6, "nachmittag": 0.5, "dinner": 0.25, "abend": 0.5, "nacht": 0.8}
# Zufalls-Stufe: Bordrat und Handy haben eigene Stufen (25.10.2026) und stehen hier nicht mehr drin
ARTEN_JE_PHASE = {"nacht": ("abend", "auftritt", "gagv", "gag1"),
                  "fruehstueck": ("gag1",), "tag": ("gagv", "gag1", "duell"),
                  "nachmittag": ("gagv", "gag1", "duell"),
                  "dinner": ("gag1", "gagv", "duell"), "abend": ("abend", "gagv", "gag1", "duell", "auftritt")}
MAX_JE_TAG = {"bordrat": 1, "handy": 2, "abend": 1}
# Gewicht je Art in der Zufalls-Stufe: Abende haben Vorrang, sobald sie gelten
GEWICHT = {"abend": 8, "gag1": 2.5, "gagv": 2.5, "duell": 1.2, "auftritt": 1.2}
HANDY_CHANCE = {"fruehstueck": 0.15, "tag": 0.2, "nachmittag": 0.2, "dinner": 0.2, "abend": 0.35, "nacht": 0.45}
# Akt 2 (Duc 29.10.2026: "eher ruhig, 2-4 Events am Tag"): ab Tag 8 seltener ziehen, hoechstens 2 Gags am Tag, und neue
# Akt-2-Events vor den aus Akt 1 geoeffneten ("nachlauf", werkzeuge\eden_rise\ereignisse_fenster.py)
AKT2_AB = 8
AKT2_FAKTOR = {"zufall": 0.45, "handy": 0.6}
AKT2_GAGS_MAX = 2
AKT2_VORRANG = 0.65                  # Anteil, mit dem ein neues Akt-2-Event gewinnt, wenn beide Sorten passen
# Favours (Duc 29.10.2026, Brain Trust: ersetzen die Schnelljob-Liste): Bitten per Handy, eigene Stufe vor dem Handy, hoechstens
# eine am Tag, nur tagsueber und abends. Wege mit Probe kosten Energie (Option "energie"), ohne Energie sind sie gesperrt.
FAVOUR_CHANCE = {"tag": 0.35, "nachmittag": 0.35, "abend": 0.3}
FAVOUR_MAX_JE_TAG = 1
FAVOUR_WEITER = 0.6                     # Anteil, mit dem eine laufende Kette vor einer neuen Bitte kommt
RUHIGE_NACHT_JEDE = 4                # jede vierte freie Nacht ohne Bordrat (welche, ist je Durchlauf zufaellig)
RUHIGE_NACHT = {"titel": "A Quiet Night", "kurz": "No crew meeting tonight.",
                "folgen": ["Nobody knocks, nobody needs a decision. The crew turns in early, and all you can hear is "
                           "the sea against the hull."]}
RUECKHALT_START = 50
BORDREGELN_MAX = 5
VERSPRECHEN_GEHALTEN, VERSPRECHEN_GEBROCHEN = 8, -16
ABEND_BEGEHREN_STUFE = 3      # ein angenommener Intim-Abend hebt Begehren mindestens hierauf (Duc 27.10.2026)
FOKUS_FAKTOR = 3              # Flirts mit den zwei Frauen, die Duc am naechsten sind, kommen so viel oefter (Duc 31.10.2026)


def daten(moddir):
    pfad = os.path.join(moddir, "ereignisse.json")
    if not os.path.exists(pfad):
        return None
    st = os.path.getmtime(pfad)
    if _CACHE.get(pfad, (None,))[0] != st:
        d = json.load(open(pfad, encoding="utf-8"))
        d["_index"] = {e["id"]: e for e in d["events"]}
        _CACHE[pfad] = (st, d)
    return _CACHE[pfad][1]


def stand(z):
    e = z.setdefault("ev", {})
    e.setdefault("gesehen", [])          # Event-IDs dieses Durchlaufs
    e.setdefault("heute", {})            # art -> Anzahl (Tag in "tag")
    e.setdefault("tag", z["tag"])
    e.setdefault("gags", {})             # Running Gag -> Stufe
    e.setdefault("bordregeln", [])
    e.setdefault("versprechen", [])      # {"an", "text", "bis", "status", "gehalten_wenn"}
    e.setdefault("kontrollrisiko", 0)
    if e["tag"] != z["tag"]:
        e["tag"], e["heute"] = z["tag"], {}
    z["werte"].setdefault("rueckhalt", RUECKHALT_START)
    return e


# ------------------------------------------------------------------ Ziehen
def _da(z, modul, pid):
    """Ist die Person fuer ein Event verfuegbar? (bekannt, an Bord/im Dorf bzw. Anrufer)"""
    from . import buehne
    if pid not in modul["personen"]:
        return pid == "crew" or rollen.ist(modul, "nur_anruf", pid)    # die ganze Crew, Anrufer ohne Bild
    if rollen.person(modul, pid, "immer_erreichbar"):
        return True                                    # per Bedingung im Event bzw. Anruf geregelt
    return pid in (z.get("bekannt") or modul["personen"]) and buehne.wo_ist(z, modul, pid) is not None


def _beteiligte(ev):
    p = ev["personen"]
    out = []
    for k in ("sprecher", "links", "rechts", "handelnd", "pid", "gegner", "anrufer"):
        if p.get(k):
            out.append(p[k])
    for b in p.get("betroffen", []):
        out.append(b["id"])
    return out


def gesperrt_durch_story(z, modul, phase):
    """Laeuft gerade die Belagerung (modul "sperre")? Dann gibt es nur noch ihre eigenen Szenen, keine Selfies mitten im Krieg (Duc 01.11.2026)."""
    s = modul.get("sperre")
    if not s:
        return None
    ph = modul["zeitraster"]["phasen"]
    return s["praefix"] if z["tag"] > s["tag"] or (z["tag"] == s["tag"] and ph.index(phase) >= ph.index(s["phase"])) else None


def passt(z, modul, ev, phase, wetter=None, pflicht=False):
    w = ev["wann"]
    praefix = gesperrt_durch_story(z, modul, phase)
    if praefix and not ev["id"].startswith(praefix):
        return False
    if "phasen" not in w:                              # Szenen-Frames (z. B. Holms Wette) ziehen nie zufaellig, erst ab Tag 15 sichtbar
        return False
    a, b = w["tage"]
    a2 = w.get("akt2")                                 # zweites Fenster fuer Akt 2 (29.10.2026, ereignisse_fenster.py)
    if not (a <= z["tag"] <= b or a2 and a2[0] <= z["tag"] <= a2[1]) or not regeln.phase_passt(phase, w["phasen"]):
        return False
    if w.get("wetter") and wetter not in w["wetter"]:
        return False
    if w.get("an_land") and z["tag"] < 2:
        return False
    if w.get("bedingung") and not regeln.gilt(w["bedingung"], z, {"phase": phase}):
        return False
    if ev["art"] != "handy" and not w.get("prolog") and not w.get("holt_leute") and not all(_da(z, modul, p) for p in _beteiligte(ev)):
        return False                                   # Prolog-Ketten (Tag 0, Hafenkampf) stellen ihre Leute selbst
    stumm = rollen.person(modul, ev["personen"].get("anrufer"), "ruft_nicht_an_wenn") if ev["art"] == "handy" else None
    if stumm and regeln.gilt(stumm, z) and not pflicht:
        return False                                   # z. B. Megan ist an Bord - sie ruft nicht an (ausser Pflicht)
    return True


def heute_neu(z, modul, moddir, pid):
    """Tageswahl (UX-Paket 03.11.2026): Steht fuer diese Person heute etwas Neues an? Eine Leiter-Szene, die heute noch
    kommen kann, oder eine Stufe, die eine Begegnung erreichen kann. Nur fuer die Anzeige, aendert nichts am Stand."""
    e = z.get("ev") or {}
    if not (e.get("tag") == z["tag"] and (e.get("heute") or {}).get("leiter")):
        phasen = modul["zeitraster"]["phasen"]
        rest = phasen[phasen.index(z["phase"]):] if z["phase"] in phasen else [z["phase"]]
        wetter = (z.get("plan") or {}).get("wetter")
        for ev in (daten(moddir) or {}).get("events", []):
            if ev["wann"].get("leiter") and ev["id"] not in e.get("gesehen", []) and pid in _beteiligte(ev)                     and any(passt(z, modul, ev, ph, wetter, True) for ph in rest):
                return True
    for achse in ("vertrauen", "begehren"):
        key = achse + "." + pid
        s = z["werte"].get(key)
        if s is None or s >= 5 or s == 2:                 # Stufe 3 gibt es nur ueber ein Erlebnis (Deckel 35)
            continue
        if s >= 3 and zustand.STUFEN_ABSTAND and z["tag"] - z.get("stufe_tag", {}).get(key, 1) < zustand.STUFEN_ABSTAND:
            continue
        p, ab = (z.get("punkte") or {}).get(key), zustand.STUFEN_AB          # lesen, nie anlegen (zustand.punkte schreibt)
        if p is not None and (p - ab[s]) / float(ab[s + 1] - ab[s]) >= .75:
            return True
    return False


def pflicht_ziehen(z, modul, moddir, nur_prolog=False):
    """Pflicht-Events (Megans Sprachnachrichten, Tag 0) kommen vor allem anderen. nur_prolog: nur Prolog-Events
    (Tag 0) - die laufen auch an Tag 1, in exklusiven Phasen und direkt hintereinander (eden.py event_schliessen)."""
    d = daten(moddir)
    if not d or not z.get("persona"):
        return None
    e = stand(z)
    wetter = (z.get("plan") or {}).get("wetter")
    for ev in d["events"]:
        w = ev["wann"]
        if w.get("pflicht") and (w.get("prolog") or not nur_prolog) and ev["id"] not in e["gesehen"] \
                and not (w.get("leiter") and e["heute"].get("leiter")) \
                and not (w.get("erinnerung") and e["heute"].get("erinnerung")) \
                and passt(z, modul, ev, z["phase"], wetter, True):
            e["gesehen"].append(ev["id"])
            if w.get("leiter"):                       # Romanzen-Leiter (31.10.2026): hoechstens eine Szene am Tag
                e["heute"]["leiter"] = 1
            if w.get("erinnerung"):                   # Erinnerung einer Auftraggeberin (02.11.2026): hoechstens eine am Tag
                e["heute"]["erinnerung"] = 1
            e["heute"][ev["art"]] = e["heute"].get(ev["art"], 0) + 1
            z["event"] = {"id": ev["id"], "tag": z["tag"], "phase": z["phase"], "ergebnis": None}
            if w.get("prolog"):                       # wer hier auftritt, ist jetzt bekannt (Dorf am Hafen, 25.10.)
                zustand.bekannt_machen(z, [p for p in _beteiligte(ev) if p in modul["personen"]])
            return ev
    return None


def ziehen(z, modul, moddir):
    """Naechstes Event dieser Phase oder None. Jede Phase durchlaeuft ihre Stufen einmal: Pflicht -> (Nacht) Bordrat
    -> Zufall -> Handy. Aufgerufen zu Beginn der Phase und nach jedem geschlossenen Event (eden.py). In exklusiven
    Story-Phasen nur Prolog-Pflicht."""
    d = daten(moddir)
    if not d or not z.get("persona"):
        return None
    inhalt = ((z.get("plan") or {}).get("phasen") or {}).get(z["phase"]) or {}
    gesperrt = bool(inhalt.get("fix")) or z["tag"] < 2 and z["phase"] != "nacht" or bool(gesperrt_durch_story(z, modul, z["phase"]))
    e = stand(z)
    schl = "%d-%s" % (z["tag"], z["phase"])
    st = e.get("stufe") or {}
    if st.get("schl") != schl:
        st = e["stufe"] = {"schl": schl, "i": 0}
    stufen = ["pflicht"] if gesperrt else (["pflicht"] + (["bordrat"] if z["phase"] == "nacht" else [])
                                           + ["zufall", "favour", "handy"])
    while st["i"] < len(stufen):
        s = stufen[st["i"]]
        st["i"] += 1
        if s == "pflicht":
            ev = pflicht_ziehen(z, modul, moddir, nur_prolog=gesperrt and not gesperrt_durch_story(z, modul, z["phase"]))
            if ev:                                     # Pflicht heisst garantiert: Fallen zwei auf eine Phase, kommt danach die zweite (Duc 01.11.2026)
                st["i"] -= 1
        elif s == "bordrat":
            ev = _bordrat_ziehen(z, modul, d, e)
        elif s == "zufall":
            ev = _zufall_ziehen(z, modul, d, e, inhalt)
        elif s == "favour":
            ev = _favour_ziehen(z, modul, d, e)
        else:
            ev = _handy_ziehen(z, modul, d, e)
        if ev:
            return ev
    return None


def weiter_ziel(z):
    """Naechster Frame einer Ortskette oder None. "weiter" ist eine Event-ID oder eine Liste [{"wenn": Bedingung,
    "id": ...}, ..., {"id": ...}] - die erste passende gilt (ausgewertet erst beim Schliessen, nach allen Folgen)."""
    w = z.pop("ev_weiter", None)
    if isinstance(w, list):
        w = next((x["id"] for x in w if not x.get("wenn") or regeln.gilt(x["wenn"], z)), None)
    return w


def direkt_ziel(z):
    """Zweiter Takt einer Szene (Romanzen-Leiter, 31.10.2026), Form wie "weiter", aber ausserhalb der Ortskapitel."""
    w = z.pop("ev_direkt", None)
    if isinstance(w, list):
        w = next((x["id"] for x in w if not x.get("wenn") or regeln.gilt(x["wenn"], z)), None)
    return w


def striche(z, pid):
    """Rosis Strichliste: wirklich gezaehlt, wie oft Duc bei ihr war. Die erste Reparatur war schon erfunden: mindestens 3."""
    szenen = z.get("verlauf", []) + z.get("heute", [])
    return max(3, sum(1 for h in szenen if pid in h.get("anwesend", [])))


def lage_text(ev, z):
    return ev["lage"].replace("{striche}", str(striche(z, ev["personen"].get("pid")))) if "{striche}" in ev["lage"] else ev["lage"]


def zeilen_aktiv(ev, z):
    """Zeilen, die gerade gelten, als (Index, Zeile); der Index bleibt der Stimm-Schluessel. Eine Zeile darf "gruppe"
    und "wenn" tragen: je Gruppe gilt die erste, deren Bedingung passt (Holm, 30.10.2026). Ohne Gruppe immer."""
    out, erledigt = [], set()
    for i, zl in enumerate(ev["zeilen"]):
        g = zl.get("gruppe")
        if g and (g in erledigt or (zl.get("wenn") and not regeln.gilt(zl["wenn"], z))):
            continue
        if g:
            erledigt.add(g)
        out.append((i, zl))
    return out


def ort_oeffnen(z, modul, moddir, eid):
    """Frame einer Ortskette als offenes Event setzen (Ortskapitel, 26.10.2026). Frames zaehlen nicht als "gesehen":
    beim Wiederkommen laufen sie erneut. Wer im Frame auftritt, ist danach bekannt."""
    ev = daten(moddir)["_index"][eid]
    zustand.bekannt_machen(z, [p for p in _beteiligte(ev) + [zl["wer"] for zl in ev["zeilen"]] if p in modul["personen"]])
    z["event"] = {"id": eid, "tag": z["tag"], "phase": z["phase"], "ergebnis": None}
    return z["event"]


def spur_uhr(z, name, a, b=None):
    """Spur-Uhr eines Ortskapitels: ("kloster", "start", 4) stellt sie, ("kloster", -1) zaehlt herunter, ("kloster",
    "aus") nimmt sie weg.
    Bei 0 wird das Flag spur_<name>_abgelaufen gesetzt. -> Zeilen fuer die Anzeige."""
    u = z.setdefault("spur_uhren", {})
    if a == "aus":                                   # Kapitel vorbei: die Uhr verschwindet
        u.pop(name, None)
        return []
    if a == "start":
        u[name] = {"stand": int(b), "von": int(b)}
    elif name in u:
        u[name]["stand"] = max(0, u[name]["stand"] + int(a))
    else:
        return []
    if u[name]["stand"] <= 0 and "spur_%s_abgelaufen" % name not in z["flags"]:
        z["flags"].append("spur_%s_abgelaufen" % name)
    return ["⏳ Trail: %d/%d" % (u[name]["stand"], u[name]["von"])]


def selfie_bild(z, s):
    """Selfie-Event -> Dateiname ohne Endung (module/<m>/selfies). Seit 27.10.2026 steht das Bild im Event (s["bild"]);
    alt (26.10.): Raum je Durchlauf ausgewuerfelt, Nacktheitsgrad nach Begehren (2 -> 1, 3 -> 2, ab 4 -> 3)."""
    if s.get("bild"):
        return s["bild"]
    raum = random.Random("%s-selfie-%s" % (z["id"], s["frau"])).choice(s["raeume"])
    grad = max(1, min(3, z["werte"].get("begehren." + s["frau"], 2) - 1))
    return "%s_%s_%d" % (s["frau"], raum, grad)


def _setzen(z, e, ev):
    e["gesehen"].append(ev["id"])
    e["heute"][ev["art"]] = e["heute"].get(ev["art"], 0) + 1
    z["event"] = {"id": ev["id"], "tag": z["tag"], "phase": z["phase"], "ergebnis": None}
    if ev["personen"].get("selfie"):                 # Bild beim Ziehen festlegen: dieses Selfie sieht Duc
        s = ev["personen"]["selfie"]
        z["event"]["selfie"] = selfie_bild(z, s)
        album.merken(z, ev, z["event"]["selfie"])
        if s.get("stufe"):                           # Stufe abhaken, Reihe fuer den Durchlauf merken (27.10.2026)
            e.setdefault("selfie_stufen", {}).setdefault(s["frau"], []).append(s["stufe"])
            e.setdefault("selfie_reihe", {}).setdefault(s["frau"], s["reihe"])
    if ev["id"].startswith("rm_"):
        album.merken(z, ev)
    fv = ev["personen"].get("favour") or {}
    if fv.get("foto"):                               # Favour-Dank (29.10.2026): das Foto, das sie/er schickt
        z["event"]["foto"] = "/favourfoto/%s.webp" % fv["foto"]
    if ev["personen"].get("charm"):                  # Charm-Uebergabe (28.10.2026): Foto des Anhaengers
        c = charms.daten(z.get("modul")).get(ev["personen"]["charm"])
        if c:
            z["event"]["foto"] = "/itembild/%s" % c["bild"]
    return ev


def _selfie_auswahl(e, kand):
    """Selfie-Stufen (27.10.2026): je Frau und Stufe nur ein Selfie, Stufe 4/5 erst nach der vorigen, und die einmal
    gezogene Reihe (Hintergrund) bleibt, solange sie die Stufe hat. Andere Events bleiben unberuehrt."""
    stufen, reihe = e.get("selfie_stufen", {}), e.get("selfie_reihe", {})
    frei = []
    for ev in kand:
        s = ev["personen"].get("selfie") or {}
        if s.get("stufe"):
            schon = stufen.get(s["frau"], [])
            if s["stufe"] in schon or (s["stufe"] > 3 and s["stufe"] - 1 not in schon):
                continue
        frei.append(ev)
    gleich = {(s["frau"], s["stufe"]) for s in ((ev["personen"].get("selfie") or {}) for ev in frei)
              if s.get("stufe") and s["reihe"] == reihe.get(s["frau"])}
    return [ev for ev in frei if not (ev["personen"].get("selfie") or {}).get("stufe")
            or (ev["personen"]["selfie"]["frau"], ev["personen"]["selfie"]["stufe"]) not in gleich
            or ev["personen"]["selfie"]["reihe"] == reihe.get(ev["personen"]["selfie"]["frau"])]


def _bordrat_ziehen(z, modul, d, e):
    """Nachtprogramm: in 3 von 4 freien Naechten ein Bordrat, sonst die Meldung "ruhige Nacht"."""
    if z["tag"] < 2 or e["heute"].get("bordrat", 0) >= MAX_JE_TAG["bordrat"]:
        return None
    e["freie_naechte"] = e.get("freie_naechte", 0) + 1
    if "ruhige_nacht" not in e:
        e["ruhige_nacht"] = random.Random("%s-ruhig" % z["id"]).randint(1, RUHIGE_NACHT_JEDE)
    wetter = (z.get("plan") or {}).get("wetter")
    kand = [ev for ev in d["events"] if ev["art"] == "bordrat" and ev["id"] not in e["gesehen"]
            and passt(z, modul, ev, z["phase"], wetter)]
    if (e["freie_naechte"] - e["ruhige_nacht"]) % RUHIGE_NACHT_JEDE == 0 or not kand:
        z.setdefault("meldungen", []).append(dict(RUHIGE_NACHT, folgen=list(RUHIGE_NACHT["folgen"])))
        return None
    return _setzen(z, e, random.Random("%s-%d-bordrat" % (z["id"], z["tag"])).choice(kand))


def _handy_ziehen(z, modul, d, e):
    """Eigene Spur: eine Nachricht oder ein Anruf zusaetzlich zu allem anderen, hoechstens zwei am Tag (Megans
    Pflicht-Sprachnachrichten zaehlen nicht mit)."""
    if e["heute"].get("handy_zufall", 0) >= MAX_JE_TAG["handy"]:
        return None
    rng = random.Random("%s-%d-%s-handy" % (z["id"], z["tag"], z["phase"]))
    wetter = (z.get("plan") or {}).get("wetter")
    kand = _selfie_auswahl(e, [ev for ev in d["events"] if ev["art"] == "handy" and ev["id"] not in e["gesehen"]
                               and not ev["personen"].get("favour") and passt(z, modul, ev, z["phase"], wetter)])
    # Vorrang (27.10.2026): ein faelliger Nachschlag oder ein neues Selfie kommt ohne Wuerfeln - das Foto ist die
    # Belohnung genau dann, wenn die Beziehung eine Stufe weiter ist.
    vorrang = [ev for ev in kand if ev["personen"].get("nachschlag")] or               [ev for ev in kand if (ev["personen"].get("selfie") or {}).get("stufe")] or \
        [ev for ev in kand if ev["personen"].get("charm")]                    # Charm-Uebergabe (Vertrauen 5, 28.10.2026)
    if vorrang:
        kand = vorrang
    elif rng.random() > HANDY_CHANCE.get(z["phase"], 0) * _akt2_faktor(z, "handy"):
        return None
    if not kand:
        return None
    e["heute"]["handy_zufall"] = e["heute"].get("handy_zufall", 0) + 1
    kand = _akt2_vorrang(z, rng, kand)
    faktor = fokus_faktor(z, modul)
    return _setzen(z, e, rng.choices(kand, [faktor(ev) for ev in kand])[0])


def _favour_ziehen(z, modul, d, e):
    """Favours (Duc 29.10.2026, ersetzen die Schnelljob-Liste): eine Bitte per Handy, hoechstens eine am Tag, nur in den
    Phasen aus FAVOUR_CHANCE. Ein faelliger Dank (Ketten-Abschluss mit Foto) kommt ohne Wuerfeln, sonst nach Chance."""
    if e["heute"].get("favour", 0) >= FAVOUR_MAX_JE_TAG or z["phase"] not in FAVOUR_CHANCE \
            or e["heute"].get("handy_zufall", 0) >= MAX_JE_TAG["handy"]:      # zaehlt zu den zwei Handy-Meldungen am Tag
        return None
    wetter = (z.get("plan") or {}).get("wetter")
    kand = [ev for ev in d["events"] if (ev["personen"].get("favour") and ev["id"] not in e["gesehen"]
                                         and passt(z, modul, ev, z["phase"], wetter))]
    if not kand:
        return None
    rng = random.Random("%s-%d-%s-favour" % (z["id"], z["tag"], z["phase"]))
    dank = [ev for ev in kand if ev["personen"]["favour"].get("dank")]
    if dank:
        kand = dank
    elif rng.random() > FAVOUR_CHANCE[z["phase"]]:
        return None
    else:                                            # laufende Ketten zuerst, damit Bitten zu Ende kommen
        weiter = [ev for ev in kand if ev["personen"]["favour"].get("teil", 1) > 1]
        if weiter and rng.random() < FAVOUR_WEITER:
            kand = weiter
    e["heute"]["favour"] = e["heute"].get("favour", 0) + 1
    e["heute"]["handy_zufall"] = e["heute"].get("handy_zufall", 0) + 1
    return _setzen(z, e, rng.choice(sorted(kand, key=lambda ev: ev["id"])))


def favour_journal(z, modul, moddir, foto_fn):
    """Journal (Menue, Rubrik Favours): nur was Duc schon bekommen hat, je Kette die Teile mit Ausgang, Foto am Ende."""
    d = daten(moddir)
    if not d:
        return []
    ketten = collections.OrderedDict()
    for eintrag in z.get("favours") or []:
        ev = d["_index"].get(eintrag["id"])
        if not ev:
            continue
        fv = ev["personen"]["favour"]
        k = ketten.setdefault(fv["kette"], {"kette": fv["kette"], "titel": fv.get("ketten_titel") or ev["titel"],
                                             "von": ev["personen"].get("anrufer"), "teile": [], "foto": None})
        if fv.get("dank"):
            k["foto"] = foto_fn(fv["foto"]) if fv.get("foto") else None
        else:
            k["teile"].append({"titel": ev["titel"], "ausgang": eintrag["ausgang"], "weg": eintrag.get("weg", "")})
    from . import handel
    out = []
    for k in ketten.values():
        k["von_name"] = handel.anzeigename(modul, k["von"]) if k["von"] in modul["personen"] else k["von"]
        out.append(k)
    return out[::-1]


def _akt2_faktor(z, stufe):
    return AKT2_FAKTOR[stufe] if z["tag"] >= AKT2_AB else 1.0


def _akt2_vorrang(z, rng, kand):
    """Akt 2: neue Events vor den geoeffneten Akt-1-Events (nachlauf) - beide Sorten bleiben moeglich."""
    if z["tag"] < AKT2_AB:
        return kand
    neu = [ev for ev in kand if not ev.get("nachlauf")]
    alt = [ev for ev in kand if ev.get("nachlauf")]
    if neu and alt:
        return neu if rng.random() < AKT2_VORRANG else alt
    return kand


def _naechste(z, kand):
    """Abende und Funken (27.10.2026): Unter mehreren passenden kommt die Frau zuerst, der Duc am naechsten ist
    (Vertrauen + Begehren in Punkten) - sonst entschied der Zufall, und Fokus auf eine Frau zaehlte nicht."""
    def naehe(ev):
        pid = (ev.get("personen") or {}).get("pid")
        pk = z.get("punkte") or {}
        return pk.get("vertrauen.%s" % pid, 0) + pk.get("begehren.%s" % pid, 0)
    beste = max(naehe(ev) for ev in kand)
    return [ev for ev in kand if naehe(ev) == beste]


def fokus_faktor(z, modul):
    """Beziehungen nicht dem Zufall ueberlassen (Duc 31.10.2026, Beta-Kritik): Wer sich um eine Frau kuemmert, sieht mehr von ihr.
    Gags und Geschichten bleiben Zufall, nur Flirt-Events (knistern) und nur die zwei Frauen, die ihm am naechsten sind."""
    pk = z.get("punkte") or {}
    frauen = [p for p, v in modul["personen"].items() if v.get("romanzierbar")]
    nah = sorted(frauen, key=lambda p: (-(pk.get("vertrauen." + p, 0) + pk.get("begehren." + p, 0)), p))[:2]

    def faktor(ev):
        return FOKUS_FAKTOR if ev.get("knistern") and any(p in nah for p in _beteiligte(ev)) else 1
    return faktor


def _zufall_ziehen(z, modul, d, e, inhalt):
    """Ein Zufalls-Event (Gags, Duell, Auftritt, Abend) nach Phasen-Chance und Gewicht."""
    wetter = (z.get("plan") or {}).get("wetter")
    rng = random.Random("%s-%d-%s-ev" % (z["id"], z["tag"], z["phase"]))
    if rng.random() > CHANCE.get(z["phase"], 0) * _akt2_faktor(z, "zufall"):
        return None
    gags_heute = sum(e["heute"].get(a, 0) for a in ("gag1", "gagv", "duell", "auftritt"))
    gags_max = AKT2_GAGS_MAX if z["tag"] >= AKT2_AB else 3
    topf = []                                          # (Gewicht, Art, Kandidaten)
    for art in ARTEN_JE_PHASE.get(z["phase"], ()):
        if e["heute"].get(art, 0) >= MAX_JE_TAG.get(art, 2):
            continue
        if art in ("gag1", "gagv", "duell", "auftritt") and gags_heute >= gags_max:
            continue
        if art == "abend" and inhalt.get("folge"):
            continue                                   # Abende fuehren in eine Szene - nur in freien Phasen
        kand = [ev for ev in d["events"] if ev["art"] == art and ev["id"] not in e["gesehen"]
                and not ev["personen"].get("favour")           # Flaschenpost (Ligeia): kommt nur ueber _favour_ziehen
                and passt(z, modul, ev, z["phase"], wetter)]
        if kand:
            topf.append((GEWICHT.get(art, 1), art, kand))
    if not topf:
        return None
    x = rng.random() * sum(g for g, _, _ in topf)
    for g, art, kand in topf:
        x -= g
        if x <= 0:
            break
    if art == "abend":
        kand = _naechste(z, kand)
    kand = _akt2_vorrang(z, rng, kand)                               # Akt 2: neue Events zuerst (29.10.2026)
    return _setzen(z, e, moral.gewichtet(z, modul, rng, kand, fokus_faktor(z, modul)))     # Ton nach Crew-Stimmung (27.10.2026)


# ------------------------------------------------------------------ Antworten
def _intim_pid(o):
    """Person der Szene, in die eine Option fuehrt (szene_intim/szene_gespraech) - oder None."""
    for f in o.get("folgen", []):
        s = f.get("szene_intim") or f.get("szene_gespraech")
        if s:
            return s.get("pid")
    return None


def ort_auswahl(z, modul, pid):
    """Orte fuer eine Option 'ort_waehlen' (18.10.2026): privat genug, fuer Duc und sie jetzt offen (keine Probe), an
    Land nur, wenn Duc heute an Land war. Ihre Lieblingsorte zuerst. -> [{"id", "name", "liebling"}]"""
    from . import gesten, handel
    if not pid:
        return []
    lieb = (modul["personen"].get(pid) or {}).get("lieblingsorte") or []
    an_land = handel.an_land(z, modul)
    out = []
    for rid, r in modul["raeume"].items():
        if r.get("privat", 1) < gesten.PRIVAT_AB or r.get("versteckt") or (r.get("bereich") == "land" and not an_land):
            continue
        if regeln.zugang(r, z, {"anwesend": [pid], "phase": z.get("phase")})[0] != "offen":
            continue
        out.append({"id": rid, "name": re.sub(r"\s*\([^)]*\)", "", r["label"]).strip(), "liebling": rid in lieb})
    return sorted(out, key=lambda x: (not x["liebling"], x["name"]))


def ort_festlegen(z, modul, szene, ort):
    """'frei' in einer Szene durch den gewaehlten Ort ersetzen - ungueltig/fehlend: erster Lieblingsort, sonst
    Ducs Kabine (die Engine stuerzt nie mehr an einem Ort 'frei' ab)."""
    if not szene or szene.get("ort") != "frei":
        return szene
    erlaubt = ort_auswahl(z, modul, szene.get("pid"))
    ids = [o["id"] for o in erlaubt]
    if ort not in ids:
        ort = next((o["id"] for o in erlaubt if o["liebling"]), None) or (
            "duc_cabin" if "duc_cabin" in modul["raeume"] else (ids[0] if ids else next(iter(modul["raeume"]))))
    return dict(szene, ort=ort)


def waehlen(z, modul, moddir, index, probe_fn=None, ort=None):
    """Antwort auf das offene Event -> Ergebnis (wird angezeigt, bis Duc es schliesst). ort = gewaehlter Raum bei
    Optionen mit art "ort_waehlen"."""
    d = daten(moddir)
    offen = z.get("event")
    if not offen or offen.get("ergebnis"):
        raise ValueError("Gerade wartet kein Ereignis auf eine Antwort.")
    ev = d["_index"][offen["id"]]
    o = ev["optionen"][index]
    folgen = list(o.get("folgen", []))
    if o.get("energie"):                                                  # Favour-Weg mit Probe (29.10.2026)
        if z["werte"].get("energie", 0) < o["energie"]:
            raise ValueError("You're running on empty – this needs %d energy." % o["energie"])
        folgen.insert(0, {"wert": "energie", "delta": -o["energie"]})
    probe = None
    if o.get("probe"):
        pr = o["probe"]
        extra = []
        if pr.get("vorteil"):
            from . import handel
            if handel.persona_vorteil(z, pr["vorteil"]):
                extra.append(("Your strength", 2))
        extra += moral.wuerfel_bonus(z, modul, _beteiligte(ev))            # Crew-Stimmung (27.10.2026)
        sg, mit_vorteil = pr["sg"], False
        if o.get("art") == "dritter_weg":                                  # Bordrat: Buzzing Vorteil, ab Tense SG +2
            dw = moral.dritter_weg(z, modul)
            sg, mit_vorteil = sg + dw["sg"], dw["vorteil"]
        probe = probe_fn(pr["attribut"], sg, extra) if probe_fn else wuerfel.probe(
            pr["attribut"], sg, [(pr["attribut"].capitalize(), z["persona"]["attribute"].get(pr["attribut"], 0))]
            + charms.boni(z, pr["attribut"]) + extra,
            vorteil=mit_vorteil)
        ok = probe["ergebnis"] in ("erfolg", "kritisch")
        folgen += o.get("bei_erfolg", []) if ok else o.get("bei_fehlschlag", [])
        folgen += moral.nach_probe(z, modul, probe, _beteiligte(ev))
        if o.get("art") == "dritter_weg" and moral.aktiv(modul):           # Tiefpunkt/Hochpunkt: +2 / -2
            folgen.append(moral.folge(2 if ok else -2, "genau"))
    zeilen, szene = anwenden(z, modul, ev, folgen)
    ok = not probe or probe["ergebnis"] in ("erfolg", "kritisch")
    zeile, zeile_id = (o.get("zeile"), "%s#o%d" % (ev["id"], index)) if ok else \
        (o.get("zeile_fehlschlag"), "%s#f%d" % (ev["id"], index))         # Pointe auch beim Fehlschlag (Favours)
    chronik.eintragen(z, modul, "ereignis", "%s - Duc: %s" % (ev["titel"], o["text"]),
                      wer=[p for p in _beteiligte(ev) if p in modul["personen"]], dabei=[], wichtig=1)
    offen["ergebnis"] = {"index": index, "text": o["text"], "probe": probe, "zeilen": zeilen,
                         "zeile": zeile, "zeile_id": zeile_id if zeile else None}
    if ev["personen"].get("favour"):                                      # Journal: Ausgang der Bitte (29.10.2026)
        z.setdefault("favours", []).append({"id": ev["id"], "weg": o["text"],
                                            "ausgang": "abgelehnt" if o.get("art") == "auflegen" else ("ok" if ok else "daneben")})
    if szene:
        offen["szene"] = ort_festlegen(z, modul, szene, ort)
    return offen


def tisch_vertrauen(z, modul, praefix, personen, basis=2):
    """Vertrauen nach einer Aussprache: Basis, je nach Saldo der Flags <praefix>plus_<pid>_* und <praefix>minus_<pid>_*
    eine Stufe mehr (Saldo ab 2) oder weniger (Saldo ab -1). Flags bleiben fuer spaetere Saetze stehen."""
    for pid in personen:
        plus = sum(1 for f in z["flags"] if f.startswith("%splus_%s_" % (praefix, pid)))
        minus = sum(1 for f in z["flags"] if f.startswith("%sminus_%s_" % (praefix, pid)))
        saldo = plus - minus
        stufe = basis + (1 if saldo >= 2 else -1 if saldo <= -1 else 0)
        key = "vertrauen." + pid
        zustand.punkte_add(z, modul, key, zustand.STUFEN_AB[stufe] - zustand.punkte(z, key), roh=True)


def anwenden(z, modul, ev, folgen):
    """Event-Folgen umsetzen -> (Zeilen fuer die Anzeige, Szene oder None)."""
    e = stand(z)
    zeilen, szene = [], None
    for f in folgen:
        if "vertrauen" in f or "begehren" in f:
            art = "vertrauen" if "vertrauen" in f else "begehren"
            pid, pts = f[art]
            key = "%s.%s" % (art, pid)
            if key in z["werte"] or pid in modul["personen"] and art == "vertrauen" and \
                    pid in modul["werte"]["vertrauen"].get("je", []):
                zeilen += zustand.punkte_add(z, modul, key, pts)
        elif "wert" in f or "geld" in f or "flag" in f or "flag_datiert" in f or "nacht_bei" in f:
            zeilen += zustand.folgen_anwenden(z, modul, [f])
        elif "flags_weg" in f:                         # Neustart einer Szene: alle Flags mit diesem Anfang (Long Table)
            z["flags"] = [x for x in z["flags"] if not x.startswith(f["flags_weg"])]
        elif "lp_anteil" in f:                         # kurze Atempause zwischen zwei Kaempfen (Red Trio, Station 7)
            from . import kampf
            voll = kampf.lp_max_duc(z)
            alt = kampf.lp(z)
            z["lp"] = min(voll, alt + int(voll * f["lp_anteil"]))
            if z["lp"] != alt:
                zeilen.append("+%d HP" % (z["lp"] - alt))
        elif "tisch_vertrauen" in f:                   # still, ohne Anzeige: Wiki welt/nebenquest_red_trio.md
            tisch_vertrauen(z, modul, **f["tisch_vertrauen"])
        elif "item" in f:
            if f["item"] in modul.get("items", {}):
                zeilen += zustand.folgen_anwenden(z, modul, [f])
                if (z.get("event") or {}).get("selfie"):      # Andenken zeigt genau das gesehene Selfie
                    z.setdefault("selfie_bilder", {})[f["item"]] = z["event"]["selfie"]
        elif "rueckhalt" in f:
            alt = z["werte"].get("rueckhalt", RUECKHALT_START)
            z["werte"]["rueckhalt"] = max(0, min(100, alt + int(f["rueckhalt"])))
            if z["werte"]["rueckhalt"] != alt:
                zeilen.append("Crew Backing %+d" % (z["werte"]["rueckhalt"] - alt))
        elif "uhr" in f:
            name, delta = f["uhr"]
            if name in modul.get("uhren", {}):
                zeilen += zustand.folgen_anwenden(z, modul, [{"uhr": name, "delta": delta}])
        elif "gag" in f:
            st = e["gags"][f["gag"]] = e["gags"].get(f["gag"], 0) + 1
            fl = "gag_%s_%d" % (f["gag"], st)
            if fl not in z["flags"]:
                z["flags"].append(fl)
            g = (daten_von(z).get("gags") or {}).get(f["gag"])
            if g:
                zeilen.append("🎭 Running gag “%s” · %d" % (g["label"], st))
        elif "bordregel" in f:
            r = f["bordregel"]
            if r not in e["bordregeln"]:
                e["bordregeln"].append(r)
                if len(e["bordregeln"]) > BORDREGELN_MAX:
                    e["bordregeln"].pop(0)
                lab = ((daten_von(z).get("bordregeln") or {}).get(r) or {}).get("label", r)
                zeilen.append("📜 New ship's rule: " + lab)
        elif "versprechen" in f:
            v = f["versprechen"]
            e["versprechen"].append({"an": v["an"], "text": v["text"], "bis": z["tag"] + v.get("frist_tage", 2),
                                     "status": "offen", "gehalten_wenn": v.get("gehalten_wenn"), "seit": z["tag"]})
            zeilen.append("🤝 Promise: %s (until day %d)" % (v["text"], z["tag"] + v.get("frist_tage", 2)))
        elif "vorliebe" in f:
            from . import vorlieben
            zeilen += vorlieben.aus_folge(z, modul, f)
        elif "taktik" in f:                            # Belagerung (Duc 01.11.2026): Taktik-Karte nach dem Event
            z["ev_taktik"] = f["taktik"]
        elif "kampf" in f:                             # 24.10.2026: Kampf nach dem Event (eden.py, event_schliessen)
            z["ev_kampf"] = f["kampf"]
        elif "weiter" in f:                            # Ortskapitel (26.10.2026): naechster Frame nach dem Schliessen
            z["ev_weiter"] = f["weiter"]               # (nach einem Kampf erst danach); aufgeloest in weiter_ziel()
        elif "ort_ende" in f:
            z["ort_ende"] = f["ort_ende"]              # Besuch vorbei: die Phase ist verbraucht (eden.py)
        elif "spur_uhr" in f:
            zeilen += spur_uhr(z, *f["spur_uhr"])
        elif "ort_start" in f:                         # Pflicht-Event startet eine Ortskette (Hafenkampf, 26.10.2026)
            z["ort_aktiv"] = f["ort_start"]
            if z.get("event"):
                z["ort_weg"], z["ort_frame"] = [z["event"]["id"]], z["event"]["id"]
        elif "charm" in f or "charm_an" in f:           # Jacken-Charms (28.10.2026): zustand.py -> kern/charms.py
            zeilen += zustand.folgen_anwenden(z, modul, [f])
        elif "chip" in f or "expedition" in f or "beibringen" in f:    # Kloster 26.10.2026: zustand.py
            zeilen += zustand.folgen_anwenden(z, modul, [f])
        elif "kontrollrisiko" in f:
            e["kontrollrisiko"] = max(0, min(100, e["kontrollrisiko"] + int(f["kontrollrisiko"])))
        elif "klatsch" in f:
            k = f["klatsch"]
            von = k.get("von")
            chronik.eintragen(z, modul, "klatsch", k.get("was", ""), wer=[von] if von in modul["personen"] else [],
                              dabei=[], wichtig=2, dauer=3)
            if von in modul["personen"]:
                zeilen.append("👂 %s will tell everyone." % modul["personen"][von]["name"].split()[0])
        elif "moment" in f:
            m = f["moment"]
            chronik.eintragen(z, modul, "moment", "%s (%s)" % (ev["titel"], m.get("art", "")),
                              wer=[p for p in m.get("wer", []) if p in modul["personen"]],
                              dabei=[p for p in m.get("zeugen", []) if p in modul["personen"]], wichtig=2, dauer=3,
                              moment=m.get("art"))
        elif "nachklang" in f:
            chronik.eintragen(z, modul, "moment", ev.get("nachklang_text") or ev["titel"],
                              wer=[f["nachklang"]] if f["nachklang"] in modul["personen"] else [], dabei=[], wichtig=2,
                              dauer=3)
        elif "aufgegriffen" in f:                      # Romanzen-Leiter (31.10.2026): das Echo hat den Moment angesprochen
            chronik.aufgreifen(z, *f["aufgegriffen"])
        elif "fakt" in f:                              # harte Tatsache fuer die freien Szenen, privat (E-060)
            chronik.eintragen(z, modul, "moment", f["fakt"]["text"], wer=[f["fakt"]["wer"]], dabei=[f["fakt"]["wer"]],
                              wichtig=1, privat=True)
        elif "direkt" in f:                            # naechster Takt derselben Szene, siehe direkt_ziel()
            z["ev_direkt"] = f["direkt"]
        elif "partner_waehlen" in f:
            kand = [p for p in f["partner_waehlen"] if p in modul["personen"]]
            if kand:
                p = max(kand, key=lambda x: z["werte"].get("vertrauen." + x, 0))
                zeilen += zustand.punkte_add(z, modul, "vertrauen." + p, 4)
                if "begehren." + p in z["werte"]:
                    zeilen += zustand.punkte_add(z, modul, "begehren." + p, 4)
                zeilen.append("You choose %s." % modul["personen"][p]["name"].split()[0])
        elif "szene_intim" in f or "szene_gespraech" in f:
            szene = dict(f.get("szene_intim") or f.get("szene_gespraech"), art="intim" if "szene_intim" in f else "gespraech")
            key = "begehren.%s" % szene.get("pid")
            if "szene_intim" in f and key in z["werte"] and z["werte"][key] < ABEND_BEGEHREN_STUFE:
                # Sie kommt zu ihm: das IST Begehren. Der Abend hebt auf Stufe 3, sonst bliebe die Intim-Liste leer
                # (Lola startet bei 0, Bot-Lauf: nach ihrem Abend erst Stufe 2) - Duc 27.10.2026
                zeilen += zustand.punkte_add(z, modul, key, zustand.STUFEN_AB[ABEND_BEGEHREN_STUFE] - zustand.punkte(z, key),
                                          roh=True)
    return zeilen, szene


def daten_von(z):
    from . import hauptstory
    moddir = (z.get("plan") or {}).get("_moddir")
    return daten(moddir) or {} if moddir else {}


# ------------------------------------------------------------------ Tagesende: Bordregeln und Versprechen
def tagesende(z, modul, moddir):
    d = daten(moddir)
    if not d or not z.get("persona"):
        return []
    e = stand(z)
    zeilen = []
    for r in e["bordregeln"]:
        for f in moral.als((d.get("bordregeln") or {}).get(r, {}).get("taeglich", []), "alltag"):
            zeilen += anwenden(z, modul, {"titel": "Bordregel"}, [f])[0]
    for v in e["versprechen"]:
        if v["status"] != "offen":
            continue
        if versprechen_gehalten(z, modul, v):
            v["status"] = "gehalten"
            zeilen += _versprechen_folge(z, modul, v, VERSPRECHEN_GEHALTEN)
            zeilen.append("🤝 Kept: " + v["text"])
        elif z["tag"] >= v["bis"]:
            v["status"] = "gebrochen"
            zeilen += _versprechen_folge(z, modul, v, VERSPRECHEN_GEBROCHEN)
            zeilen.append("💔 Broken: " + v["text"])
            if moral.aktiv(modul):                                     # die Crew merkt es sich: -2
                zeilen += zustand.folgen_anwenden(z, modul, [moral.folge(-2, "genau")])
            chronik.eintragen(z, modul, "moment", "Duc broke his promise: %s." % v["text"],
                              wer=[v["an"]] if v["an"] in modul["personen"] else [], dabei=[], wichtig=2, dauer=3)
    return zeilen


def versprechen_gehalten(z, modul, v):
    """Mit Bedingung: gehalten nur, wenn sie gilt (18.10.2026 - vorher reichte auch eine gemeinsame Szene, die Suppe
    musste nie gekocht werden). Ohne Bedingung (vage Zusage): Zeit mit der Person seit dem Versprechen (eine Szene mit
    ihr, bei 'crew' mit mindestens zwei aus der Crew)."""
    if v.get("gehalten_wenn"):
        return regeln.gilt(v["gehalten_wenn"], z)
    szenen = [h for h in z.get("verlauf", []) + [dict(h, tag=z["tag"]) for h in z.get("heute", [])]
              if h.get("tag", 0) >= v["seit"] and h.get("tag", 0) <= v["bis"]]
    if v["an"] == "crew":
        nicht_crew = rollen.liste(modul, "nicht_crew")
        return any(len([p for p in h.get("anwesend", []) if p not in nicht_crew]) >= 2 for h in szenen)
    return any(v["an"] in h.get("anwesend", []) for h in szenen)


def _versprechen_folge(z, modul, v, pts):
    if v["an"] == "crew":
        alt = z["werte"].get("rueckhalt", RUECKHALT_START)
        z["werte"]["rueckhalt"] = max(0, min(100, alt + (5 if pts > 0 else -10)))
        return ["Crew Backing %+d" % (z["werte"]["rueckhalt"] - alt)]
    if "vertrauen." + v["an"] in z["werte"]:
        return zustand.punkte_add(z, modul, "vertrauen." + v["an"], pts)
    return []


# ------------------------------------------------------------------ Ansicht fuer den Client
# Zwischenkarte vor einem Event (Duc 01.11.2026): sagt, warum man jetzt woanders ist. Handy und Ortskapitel brauchen keine.
UEBERGANG_OHNE = ("handy", "ort")
UEBERGANG_ZEIT = {"fruehstueck": "It is morning.", "tag": "The day moves on.", "nachmittag": "It is afternoon now.",
                  "dinner": "It is time for dinner.", "abend": "Evening comes.", "nacht": "It is night now."}
_UEBERGAENGE = {}


def uebergang_text(z, moddir, ev):
    """-> (Satz, eigener Satz?). Eigener Satz aus uebergaenge.json (Character Design), sonst aus Tageszeit gebaut. Leer = keine
    Karte: Handy, Ortskapitel und Zwischenschritte derselben Szene ("ohne_karte", z. B. Holms Schiesswette)."""
    if ev["art"] in UEBERGANG_OHNE:
        return "", False
    pfad = os.path.join(moddir, "uebergaenge.json")
    try:
        mt = os.path.getmtime(pfad)
    except OSError:
        mt = None
    if mt and _UEBERGAENGE.get(pfad, (None,))[0] != mt:
        _UEBERGAENGE[pfad] = (mt, json.load(open(pfad, encoding="utf-8")))
    d = _UEBERGAENGE[pfad][1] if mt else {}
    if ev["id"] in (d.get("ohne_karte") or []):
        return "", False
    eigen = (d.get("zeilen") or {}).get(ev["id"])
    return (eigen, True) if eigen else ("%s Something else needs you." % UEBERGANG_ZEIT.get(z["phase"], "Time moves on."), False)


def ansicht(z, modul, moddir, cfg, sprite_fn, bild_fn):
    offen = z.get("event")
    if not offen:
        return None
    d = daten(moddir)
    ev = d["_index"].get(offen["id"]) if d else None
    if not ev:
        return None
    p = ev["personen"]

    def figur(pid, gefuehl="neutral"):
        if pid not in modul["personen"]:
            return {"id": pid, "name": "Die Crew" if pid == "crew" else (rollen.rolle(modul, "nur_anruf") or {}).get(pid, pid),
                    "sprite": None}
        from . import handel
        return {"id": pid, "name": handel.anzeigename(modul, pid),
                "sprite": sprite_fn(pid, (ev.get("sets") or {}).get(pid), gefuehl, ev["id"])}
    gef = {}
    for zl in ev["zeilen"]:
        gef.setdefault(zl["wer"], zl.get("gefuehl", "neutral"))
    besetzt = {}
    for k in ("sprecher", "links", "rechts", "handelnd", "pid", "gegner", "anrufer"):
        if p.get(k):
            besetzt[k] = figur(p[k], gef.get(p[k], "neutral"))
    besetzt["betroffen"] = [dict(figur(b["id"], gef.get(b["id"], "neutral")), ton=b.get("ton"), was=b.get("was", ""))
                            for b in p.get("betroffen", [])]
    besetzt["zuschauer"] = [figur(x) for x in p.get("zuschauer", []) + p.get("publikum", []) if x in modul["personen"]]
    ort = ev["bild"]
    if ev["art"] == "handy" and p.get("art") != "video" and p.get("anrufer_ort") in modul["raeume"]:
        hinter = bild_fn(None, False)                           # Nachricht von Bord: Duc bleibt, wo er ist
    elif ev["art"] == "handy":
        hinter = bild_fn(p.get("anrufer_ort"), True)            # Videoanruf: ihr Ort (Duc 03.11.2026)
    elif ev["art"] == "ort" and ort not in modul["raeume"]:     # Ortskapitel: eigene Hintergruende
        hinter = "/bg/eden_rise_%s.png" % ort
    else:
        hinter = bild_fn(None if ort == "ort_duc" else ort, False)
    if ort == "village_piazza" and gesperrt_durch_story(z, modul, z["phase"]):   # Belagerung: statt der Festa der verbarrikadierte Kirchplatz (Duc 01.11.2026)
        hinter = "/bg/eden_rise_siege_kirchplatz.png"
    erg = offen.get("ergebnis")
    if erg and erg.get("zeile"):
        erg = dict(erg, zeile=dict(erg["zeile"], name=figur(erg["zeile"]["wer"])["name"],
                                   sprite=figur(erg["zeile"]["wer"], erg["zeile"].get("gefuehl", "neutral"))["sprite"]))
    uebergang, ueb_eigen = uebergang_text(z, moddir, ev)
    return {"id": ev["id"], "art": ev["art"], "titel": ev["titel"], "lage": lage_text(ev, z), "ton": ev.get("ton"),
            "uebergang": uebergang, "uebergang_eigen": ueb_eigen, "uebergang_ort": re.sub(r"\s*\([^)]*\)", "", (modul["raeume"].get(ort) or {}).get("label", "")).strip(),
            "bild": hinter, "anruf_art": p.get("art"), "staerke": p.get("staerke"), "duo": p.get("duo"),
            "selfie": "/selfie/%s.webp" % offen["selfie"] if offen.get("selfie") else offen.get("foto"),
            "zeilen": [dict(zl, id="%s#z%d" % (ev["id"], i), name=figur(zl["wer"])["name"],
                            sprite=figur(zl["wer"], zl.get("gefuehl", "neutral"))["sprite"])
                       for i, zl in zeilen_aktiv(ev, z)],
            "rollen": besetzt,
            "favour": bool(p.get("favour")),
            "optionen": [{"text": o["text"], "von": o.get("von"), "art": o.get("art"), "energie": o.get("energie", 0),
                          "gesperrt": ("needs %d energy" % o["energie"]) if o.get("energie")
                          and z["werte"].get("energie", 0) < o["energie"] else "",
                          "orte": ort_auswahl(z, modul, _intim_pid(o)) if o.get("art") == "ort_waehlen" else None,
                          "probe": o.get("probe"), "folgen": folgen_text(modul, o.get("folgen", [])),
                          "erfolg": folgen_text(modul, o.get("bei_erfolg", [])),
                          "fehlschlag": folgen_text(modul, o.get("bei_fehlschlag", []))} for o in ev["optionen"]],
            "ergebnis": erg, "rueckhalt": z["werte"].get("rueckhalt", RUECKHALT_START),
            "spur": (z.get("spur_uhren") or {}).get(ev.get("spur") or ""), "frame": ev.get("frame"),
            "warnung": bool(ev.get("warnung")), "flott": bool(ev.get("flott")), "tier_bild": ev.get("tier_bild"),
            "gag": (d.get("gags") or {}).get(ev.get("gag") or "", {}).get("label")}


def folgen_text(modul, folgen):
    """Kurze Hinweise zu den Folgen (ohne Punktzahlen): Namen mit ▲/▼, Werte, Regeln."""
    from . import handel
    out = []
    for f in folgen:
        for art in ("vertrauen", "begehren"):
            if art in f:
                pid, pts = f[art]
                n = handel.anzeigename(modul, pid) if pid in modul["personen"] else pid
                out.append("%s %s%s" % (n, "▲" if pts > 0 else "▼", " ♥" if art == "begehren" else ""))
        if "wert" in f and not zustand.verborgen(modul, f["wert"]):
            out.append("%s %+d" % (zustand.wert_label(modul, f["wert"]), f.get("delta", 0)))
        if "rueckhalt" in f:
            out.append("Crew Backing %+d" % f["rueckhalt"])
        if "geld" in f:
            out.append("%+d €" % f["geld"])
        if "bordregel" in f:
            out.append("📜 Ship's rule")
        if "versprechen" in f:
            out.append("🤝 Promise")
        if "item" in f and f["item"] in modul.get("items", {}):
            out.append("🎁 " + modul["items"][f["item"]]["label"])
        if "szene_intim" in f or "szene_gespraech" in f:
            out.append("leads to a scene")
    return out


def offene_versprechen(z):
    return [v for v in (z.get("ev") or {}).get("versprechen", [])]
