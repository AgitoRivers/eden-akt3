# -*- coding: utf-8 -*-
"""Orte fuer Zweisamkeit (Duc 02.11.2026, Brain-Trust-Runde): Bei "Go somewhere private" waehlt Duc den Ort.

- Jeder Ort hat ein Risiko 0-3 je Tageszeit (modul["orte"]["risiko"]). Nach ihrem Ja kommt der Zufall: Platzt jemand
  herein, folgt Klatsch (ein Zeuge, die Chronik traegt es weiter), Peinlich (Vertrauen -4, fuer diese Szene nichts
  Intimes mehr, sie bittet ihn zu bleiben) oder Komisch (nur eine Zeile). Wer sich traut und nicht erwischt wird,
  bekommt Begehren je Risikostufe.
- Jede Romanze hat ab Vertrauen 4 ihren eigenen Ort (modul["orte"]["eigen"]), an ihre Geschichte gebunden. Dort hat Duc
  einen Bonus; der erste Besuch bringt ihre feste Zeile. Neue Orte ohne Bild stehen nicht in modul["raeume"] und
  fehlen deshalb, bis Duc das Bild abnimmt.
- Manchmal schlaegt sie ihren Ort selbst vor (feste Zeile), dann ist der Bonus groesser.
Texte: figurenrahmen.json (ort_vorschlag, ort_erster_besuch, erwischt, stoerer). Wiki: systeme/interaktion.md.
"""
import hashlib, random, re

from . import chronik, figurenrahmen, regeln, zustand

FANG = {0: 0.0, 1: 0.12, 2: 0.25, 3: 0.4}           # Chance, erwischt zu werden, je Risikostufe
FOLGEN = (("klatsch", 0.4), ("peinlich", 0.3), ("komisch", 0.3))
EIGEN_BONUS, VORSCHLAG_BONUS = 2, 3
LOHN_JE_STUFE = 2                                   # Begehren-Punkte je Risikostufe, wenn niemand kommt
PRIVAT_STUFE = 4                                    # gewaehlte Orte gelten fuer diese Szene als privat
VORSCHLAG_CHANCE = 0.35
STANDARD = "duc_cabin"


def daten(modul):
    return modul.get("orte") or {}


def label(modul, ort):
    return re.sub(r"\s*\([^)]*\)", "", modul["raeume"][ort]["label"]).strip()


def risiko(modul, ort, phase):
    r = (daten(modul).get("risiko") or {}).get(ort) or {}
    return int(r.get(phase, r.get(regeln.phase_wie(phase), r.get("*", 0))))


def eigen(z, modul, pid):
    """Ihr eigener Ort, wenn er gerade gilt (Vertrauen, Tageszeit, Raum vorhanden) -> Raum-ID oder None."""
    e = (daten(modul).get("eigen") or {}).get(pid)
    if not e or e["ort"] not in modul["raeume"] or z["werte"].get("vertrauen." + pid, 0) < e.get("ab", 4):
        return None
    if e.get("phasen") and z["phase"] not in e["phasen"] and regeln.phase_wie(z["phase"]) not in e["phasen"]:
        return None
    if e.get("flag") and e["flag"] not in z.get("flags", []):
        return None
    return e["ort"]


def zimmer(z, modul, pid):
    """Ihr Zimmer (welt/wohnen.md): erste Zeile, deren Flag gesetzt ist -> Raum-ID oder None."""
    for e in (daten(modul).get("zimmer") or {}).get(pid) or []:
        if e["ort"] in modul["raeume"] and (not e.get("flag") or e["flag"] in z.get("flags", [])):
            return e["ort"]
    return None


def wahl(z, modul, sz, pid):
    """Orte, die Duc jetzt waehlen kann -> [{id, label, risiko, eigen, vorschlag, zimmer}]."""
    hier = sz["def"]["ort"]
    out, gesehen = [], set()
    mein = eigen(z, modul, pid)
    ihr = zimmer(z, modul, pid)
    vorgeschlagen = (sz.get("ort_vorschlag") or {}).get(pid)
    if mein and mein != hier:
        out.append(mein)
    if ihr and ihr != hier and ihr not in out:
        out.append(ihr)
    for ort in daten(modul).get("gemeinsam") or []:
        o = ort if isinstance(ort, str) else ort["ort"]
        if o == hier or o not in modul["raeume"] or o in out:
            continue
        if isinstance(ort, dict) and (ort.get("nur") and pid not in ort["nur"] or ort.get("flag") and ort["flag"] not in z.get("flags", [])):
            continue
        status, _ = regeln.zugang(modul["raeume"][o], z, {"anwesend": [pid], "phase": z["phase"]})
        if status == "offen":
            out.append(o)
    for o in out:
        if o in gesehen:
            continue
        gesehen.add(o)
    return [{"id": o, "label": label(modul, o), "risiko": risiko(modul, o, z["phase"]), "eigen": o == mein,
             "vorschlag": o == vorgeschlagen, "zimmer": o == ihr} for o in out]


def bonus(z, modul, sz, pid, ort):
    """Zusatz-Boni fuer den Wurf -> [(Name, Wert)]."""
    out = []
    if (sz.get("ort_vorschlag") or {}).get(pid) == ort:
        out.append(("She suggested it", VORSCHLAG_BONUS))
    elif ort and ort == eigen(z, modul, pid):
        out.append(("Her place", EIGEN_BONUS))
    return out


def _zufall(z, ort, salz=""):
    return random.Random(int(hashlib.md5(("%s|%s|%s|%s|%s" % (z.get("id"), z["tag"], z["phase"], ort, salz)).encode()).hexdigest(), 16))


def _text(z, modul, pid, satz):
    return figurenrahmen.fuellen(z, modul, pid, satz) if satz else ""


def ankommen(z, modul, sz, pid, ort, zeile_fn):
    """Nach ihrem Ja: Raum gewechselt (gesten.raum_wechseln); jetzt Risiko, Lohn, erster Besuch.
    zeile_fn(pid, text, gefuehl) schreibt eine feste Zeile ins Log. -> Zeilen fuer die Anzeige."""
    zeilen, f = [], figurenrahmen.figur(modul, pid) if figurenrahmen.gilt(modul, pid) else {}
    if ort == eigen(z, modul, pid) and "ort_besucht_" + pid not in z["flags"]:
        z["flags"].append("ort_besucht_" + pid)
        if f.get("ort_erster_besuch"):
            zeile_fn(pid, _text(z, modul, pid, f["ort_erster_besuch"]), "love")
    r = risiko(modul, ort, z["phase"])
    rng = _zufall(z, ort)
    if not r or rng.random() >= FANG[r]:
        if r:
            zeilen += zustand.punkte_add(z, modul, "begehren." + pid, LOHN_JE_STUFE * r, deckel=zustand.GESPRAECH_DECKEL, quelle="szenen")
        return zeilen
    stoerer = ((figurenrahmen.daten(modul).get("stoerer") or {}).get(ort)) or {}
    moeglich = [(k, w) for k, w in FOLGEN if k in stoerer or (f.get("erwischt") or {}).get(k)]
    if not moeglich:
        return zeilen
    x, folge = rng.random() * sum(w for _, w in moeglich), moeglich[-1][0]
    for k, w in moeglich:
        if x < w:
            folge = k
            break
        x -= w
    st = stoerer.get(folge)
    if st:
        wer = st.get("wer") or ""
        sz["log"].append({"art": "ereignis", "text": st["text"] if not wer or wer.lower() in ("kevin", "fiona") else "%s: “%s”" % (wer, st["text"])})
    if (f.get("erwischt") or {}).get(folge):
        zeile_fn(pid, _text(z, modul, pid, f["erwischt"][folge]), {"klatsch": "embarrassment", "peinlich": "embarrassment", "komisch": "amusement"}[folge])
    name = modul["personen"][pid].get("kurz") or pid
    if folge == "klatsch":
        zeuge = next((p for p in modul["personen"] if st and (modul["personen"][p].get("kurz") or "").lower() == (st.get("wer") or "").lower()), None)
        zeuge = zeuge or next((p for p in (modul.get("rollen") or {}).get("tratsch", []) if p != pid), None)
        chronik.eintragen(z, modul, "moment", "Somebody saw Duc and %s slip away together to %s." % (name, label(modul, ort)),
                          wer=[pid], dabei=[zeuge] if zeuge else [], wichtig=2, dauer=3, moment="gesehen")
        zeilen.append("👂 Someone saw you. This will get around.")
    elif folge == "peinlich":
        sz["intim_gesperrt"] = True
        zeilen += zustand.punkte_add(z, modul, "vertrauen." + pid, -4)
    sz.setdefault("erwischt", []).append(folge)
    return zeilen


def vorschlag(z, modul):
    """Nach Ducs Zug: Manchmal schlaegt sie ihren eigenen Ort vor (einmal am Tag). -> True, wenn eine Zeile kam."""
    sz = z.get("szene")
    if not sz or len(sz.get("figuren") or []) != 1 or sz.get("intim_gesperrt"):
        return False
    pid = sz["figuren"][0]
    if not modul["personen"].get(pid, {}).get("romanzierbar") or not figurenrahmen.gilt(modul, pid):
        return False
    satz = figurenrahmen.figur(modul, pid).get("ort_vorschlag")
    mein = eigen(z, modul, pid)
    if not satz or not mein or mein == sz["def"]["ort"] or z["werte"].get("begehren." + pid, 0) < 3:
        return False
    if (z.get("ort_vorschlag_tag") or {}).get(pid) == z["tag"] or sum(1 for e in sz["log"] if e.get("art") == "duc") < 2:
        return False
    z.setdefault("ort_vorschlag_tag", {})[pid] = z["tag"]
    if _zufall(z, mein, "vorschlag").random() >= VORSCHLAG_CHANCE:
        return False
    from . import szene
    szene.zeile_einfuegen(z, modul, sz, pid, _text(z, modul, pid, satz), "desire")
    sz.setdefault("ort_vorschlag", {})[pid] = mein
    return True
