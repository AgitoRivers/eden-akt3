# -*- coding: utf-8 -*-
"""Die Kommission an Tag 35 als Verhandlung (Duc 04.11.2026, Ace Attorney als Vorbild). Nur Logik, keine Oberflaeche.
Daten: module/eden_rise/kommission.json (werkzeuge/eden_rise/kommission_akt3.py). Wiki: docs/wiki/welt/drehbuch_akt3.md 12a.

Zustand z["kommission"]: runde (0-2, dann "plaedoyer", dann fertig), geduld, gepresst (Saetze dieser Runde), runden
{id: "gewonnen"/"verloren"}, log [{wer, text, gefuehl, art}].
Aktionen (eden.py "kommission" {was, ...}): press {satz} · vorlegen {satz, karte} · nichts · plaedoyer {art: alles/teil}.
  press      Der Anwalt legt sich fest. Saetze mit nur_nach_press sind erst danach angreifbar.
  vorlegen   Karte passt zum Satz (und der Satz ist angreifbar): Runde gewonnen. Sonst Geduld -1 (bei einem wahren
             Satz mit dem Spott des Anwalts, bei einem noch nicht festgelegten Satz mit "zu_frueh").
  nichts     Duc hat keine Antwort: Runde verloren, ohne Geduld.
Geduld 0: die uebrigen Runden sind verloren, es folgt gleich das Plaedoyer. Ergebnis als Flags a3_kom_<runde> (gewonnen),
a3_kom_runden_<n>, a3_kassenbuch_alles/teil, a3_kommission_fertig. kern/akt3.saeulen liest a3_kom_runden_<n>."""
import json, os

from . import regeln

AN = False          # Schalter: erst an, wenn das Plugin eden-commission (blind gebaut 04.11.2026) lokal geprueft ist. Bis dahin laeuft die Szenen-Kette a3_kommission.


def daten(moddir):
    p = os.path.join(moddir, "kommission.json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def _k(z):
    return z.get("kommission")


def _log(k, zl, art="zeile"):
    k["log"].append(dict(zl, art=art))


def karten(z, d):
    """Karten, die Duc hat: Zeugen, die zugesagt haben, und Beweise, die er gefunden hat."""
    return [c for c in d["karten"] if regeln.gilt(c.get("wenn"), z)]


def beginnen(z, d):
    k = z["kommission"] = {"runde": 0, "geduld": d["geduld"], "gepresst": [], "runden": {}, "log": [], "schritt": "aussage",
                           "fertig": False, "falsch_n": 0}
    _log(k, d["texte"]["eroeffnung"])
    _log(k, d["texte"]["anwalt_auftritt"])
    if d["texte"].get("erinnerung"):
        _log(k, d["texte"]["erinnerung"], "hinweis")     # wie die Anhoerung in Akt 1 (LATE_GAME.md, Punkt 2)
    _runde_beginnen(k, d)
    return k


def _runde(k, d):
    return d["runden"][k["runde"]] if isinstance(k["runde"], int) and k["runde"] < len(d["runden"]) else None


def _runde_beginnen(k, d):
    r = _runde(k, d)
    k["gepresst"] = []
    _log(k, r["ansage"], "ansage")
    for s in r["saetze"]:
        _log(k, s["text"], "aussage")


def press(z, d, satz):
    k = _k(z)
    r = _runde(k, d)
    if not r or k["fertig"]:
        raise ValueError("Gerade gibt es keine Aussage.")
    s = r["saetze"][int(satz)]
    if int(satz) not in k["gepresst"]:
        k["gepresst"].append(int(satz))
    _log(k, s["press"], "press")
    return k


def vorlegen(z, d, satz, karte):
    k = _k(z)
    r = _runde(k, d)
    if not r or k["fertig"]:
        raise ValueError("Gerade gibt es keine Aussage.")
    c = next((c for c in karten(z, d) if c["id"] == karte), None)
    if not c:
        raise ValueError("Diese Karte hast du nicht.")
    i = int(satz)
    s = r["saetze"][i]
    k["log"].append({"wer": "duc", "text": "Objection!", "gefuehl": "anger", "art": "einspruch", "karte": c["id"]})
    angreifbar = s["falsch"] and (not s.get("nur_nach_press") or i in k["gepresst"])
    if angreifbar and [r["id"], i] in c["passt"]:
        k["runden"][r["id"]] = "gewonnen"
        _log(k, r["treffer"], "treffer")
        _log(k, r["anwalt_wackelt"], "wackelt")
        _log(k, r["dorf"], "dorf")
        return _naechste(z, d)
    if not s["falsch"]:
        _log(k, d["texte"]["falsch_wahr"], "spott")
    elif s.get("nur_nach_press") and i not in k["gepresst"]:
        _log(k, d["texte"]["zu_frueh"], "spott")
    texte = d["texte"]["falsch_gelegt"]
    _log(k, texte[min(k["falsch_n"], len(texte) - 1)], "geduld")
    k["falsch_n"] += 1
    k["geduld"] -= 1
    if k["geduld"] <= 0:
        _log(k, d["texte"]["geduld_weg"], "geduld_weg")
        for x in d["runden"]:
            k["runden"].setdefault(x["id"], "verloren")
        return _plaedoyer_beginnen(k, d)
    return k


def nichts(z, d):
    k = _k(z)
    r = _runde(k, d)
    if not r or k["fertig"]:
        raise ValueError("Gerade gibt es keine Aussage.")
    k["runden"][r["id"]] = "verloren"
    _log(k, d["texte"]["nichts"], "nichts")
    return _naechste(z, d)


def _naechste(z, d):
    k = _k(z)
    k["runde"] += 1
    if _runde(k, d):
        _runde_beginnen(k, d)
        return k
    return _plaedoyer_beginnen(k, d)


def _plaedoyer_beginnen(k, d):
    k["runde"], k["schritt"] = "plaedoyer", "plaedoyer"
    _log(k, d["plaedoyer"]["ansage"], "wende")
    _log(k, d["plaedoyer"]["stille"], "frage")
    return k


def plaedoyer(z, d, art):
    k = _k(z)
    if k.get("schritt") != "plaedoyer" or art not in ("alles", "teil"):
        raise ValueError("Jetzt nicht.")
    p = d["plaedoyer"][art]
    k["log"].append({"wer": "duc", "text": p["chip"], "gefuehl": "neutral", "art": "plaedoyer"})
    _log(k, p["folge"])
    _log(k, p["kommission"])
    n = sum(1 for v in k["runden"].values() if v == "gewonnen")
    _log(k, d["texte"]["urteil"][str(n)] if str(n) in d["texte"]["urteil"] else d["texte"]["urteil"][n], "urteil")
    f = z.setdefault("flags", [])
    for rid, v in k["runden"].items():
        if v == "gewonnen" and "a3_kom_" + rid not in f:
            f.append("a3_kom_" + rid)
    for neu in ("a3_kom_runden_%d" % n, "a3_kassenbuch_" + art, "a3_kommission_fertig"):
        if neu not in f:
            f.append(neu)
    k["fertig"], k["schritt"] = True, "fertig"
    return k


def ansicht(z, d):
    """Fuer das Plugin: Runde, Aussage mit drei Saetzen, Karten, Geduld, Verlauf."""
    k = _k(z)
    if not k:
        return None
    r = _runde(k, d)
    return {"runde": k["runde"], "schritt": k["schritt"], "geduld": k["geduld"], "geduld_max": d["geduld"], "fertig": k["fertig"],
            "titel": r["titel"] if r else ("The Plea" if k["schritt"] == "plaedoyer" else d["texte"]["titel"]),
            "runden": [{"id": x["id"], "titel": x["titel"], "ergebnis": k["runden"].get(x["id"])} for x in d["runden"]],
            "aussage": [{"text": s["text"]["text"], "gepresst": i in k["gepresst"]} for i, s in enumerate(r["saetze"])] if r else [],
            "karten": [{"id": c["id"], "titel": c["titel"], "text": c["text"], "art": c["art"], "wer": c.get("wer")} for c in karten(z, d)],
            "plaedoyer": [{"id": a, "chip": d["plaedoyer"][a]["chip"]} for a in ("alles", "teil")] if k["schritt"] == "plaedoyer" else [],
            "log": k["log"][-24:], "sprecher": d["sprecher"]}
