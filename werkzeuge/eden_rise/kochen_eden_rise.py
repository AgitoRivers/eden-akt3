# -*- coding: utf-8 -*-
r"""Kuechenkreis bauen (Duc 27.10.2026, E-079): prueft werkzeuge\eden_rise\kochen_daten.py und schreibt
module\eden_rise\kuechen.json (Zutaten, Fische, Effekte, Geschmack, Garten, Tiere, Nonnas Laden, Fredericos Saetze) sowie die
Turbo-Tag-Eintraege fuer Fredericos Saetze in stimme_tags.json.

  python kochen_eden_rise.py

Die Engine liest nur kuechen.json (kern/kuechen.py, kern/farm.py). Zutaten und Fische haben eine Bild-ID (items\<id>.webp fuer
Zutaten und Rohformen, farm\fische\<id>.png fuer die Fisch-Sprites, farm\tiere\<art>_<variante>.png fuer die Tiere); die Bilder
erzeugt Kochen_Bilder.bat (werkzeuge\kochen_bilder.py)."""
import json, os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, os.path.dirname(os.path.dirname(HIER)))
import kochen_daten as D  # noqa: E402
from kern import stimme  # noqa: E402

MOD = os.path.join(os.path.dirname(os.path.dirname(HIER)), "module", "eden_rise")
KATEGORIEN = {"fish", "shellfish", "poultry", "pork", "beef", "egg", "veg", "mushroom"}
ERLAUBT = {"chuckle", "clear throat", "cough", "gasp", "laugh", "shush", "sigh", "sniff"}
SG_FISCH = {"fish": 0, "shellfish": 1}
VERBOTEN = set('"*_~[]\n')                      # nicht im Klartext einer Zeile (Anzeige und Stimme)


def roh_motiv(roh, fid=None):
    if fid in D.ROH_MOTIV:
        return D.ROH_MOTIV[fid]
    name = roh.replace(", raw", "").lower()
    return "fresh raw %s on a sheet of white butcher paper" % name


def zutaten_bauen():
    z = {}
    for iid, (label, rolle, kat, quelle, preis, sg, heilt, effekt, text) in D.ZUTATEN.items():
        z[iid] = {"label": label, "rolle": rolle, "kat": kat, "quelle": quelle, "preis": preis, "sg": sg, "heilt": heilt,
                  "effekt": effekt, "text": text}
    for fid, label, art, ort, roh, preis, text, motiv in D.FISCHE:       # Rohform: Haupt-Zutat, Stufe 2 (gefangen)
        z[fid + "_roh"] = {"label": roh, "rolle": "haupt", "kat": art, "quelle": "fang", "preis": preis, "sg": SG_FISCH[art],
                           "heilt": 0, "effekt": None, "text": "From the %s: %s" % (label.lower(), text[0].lower() + text[1:]), "fisch": fid}
    return z


def fische_bauen():
    return [{"id": fid, "label": label, "art": art, "ort": ort, "roh": fid + "_roh", "roh_label": roh, "preis": preis,
             "text": text, "motiv": motiv, "motiv_roh": roh_motiv(roh, fid)} for fid, label, art, ort, roh, preis, text, motiv in D.FISCHE]


def pruefen(z, fische):
    f = []
    for iid, v in z.items():
        if v["rolle"] not in ("basis", "haupt", "akzent"):
            f.append("%s: Rolle %s" % (iid, v["rolle"]))
        if v["rolle"] == "haupt" and v["kat"] not in KATEGORIEN:
            f.append("%s: Haupt braucht eine Kategorie (%s)" % (iid, v["kat"]))
        if v["rolle"] == "akzent" and v["effekt"] not in D.EFFEKTE:
            f.append("%s: Akzent braucht einen Effekt (%s)" % (iid, v["effekt"]))
        if v["rolle"] == "basis" and not (v["sg"] and v["heilt"]):
            f.append("%s: Basis braucht SG und Heilung" % iid)
    if len([x for x in fische if x["ort"] == "meer"]) != 10 or len([x for x in fische if x["ort"] == "fluss"]) != 10:
        f.append("Fische: je 10 Meer und Fluss erwartet")
    if len({x["id"] for x in fische}) != 20:
        f.append("Fische: Ids nicht eindeutig")
    for e in D.EFFEKTE:
        if not any(v["effekt"] == e for v in z.values()):
            f.append("Effekt %s hat keine Zutat" % e)
    for pid, (mag, nicht) in D.GESCHMACK.items():
        if len(mag) != 2 or len(nicht) != 1 or not set(mag + nicht) <= KATEGORIEN or set(mag) & set(nicht):
            f.append("Geschmack %s unstimmig" % pid)
    if len(D.GESCHMACK) != 14:
        f.append("Geschmack: 14 Personen erwartet (%d)" % len(D.GESCHMACK))
    for pf in D.PFLANZEN:
        if pf not in z or z[pf]["quelle"] != "garten":
            f.append("Pflanze %s ist keine Gartenzutat" % pf)
    for tid, t in D.TIERE.items():
        for k in ("produkt", "fleisch"):
            if t[k]["art"] not in z or z[t[k]["art"]]["quelle"] != "tier":
                f.append("Tier %s: %s %s ist keine Tierzutat" % (tid, k, t[k]["art"]))
    for iid in list(D.NONNA_DAUERHAFT) + list(D.NONNA_TAGESVORRAT):
        if iid not in z:
            f.append("Nonna verkauft unbekannte Zutat %s" % iid)
    for t in D.FREDERICO:
        roh = [x.strip(" []") for x in stimme.TAG_MUSTER.findall(t)]
        klar = stimme.ohne_tags(t)
        if not roh or any(x not in ERLAUBT for x in roh) or set('"*_~\n[]') & set(klar):
            f.append("Frederico: Tag/Zeichen: %s" % t[:40])
    # Stall-Stufen und Rohstoffe
    for tid, t in D.TIERE.items():
        st = D.STALL_STUFEN.get(tid) or []
        if len(st) != 3:
            f.append("Stall %s: 3 Stufen erwartet" % tid)
            continue
        if st[0]["geld"] != t["stall"] or st[0]["plaetze"] != t["plaetze"]:
            f.append("Stall %s: Stufe 1 passt nicht zu TIERE (Preis/Plaetze)" % tid)
        for s in st:
            if set(s["rohstoffe"]) - set(D.ROHSTOFFE) or s["plaetze"] < st[0]["plaetze"]:
                f.append("Stall %s: Rohstoffe/Plaetze unstimmig" % tid)
    if set(D.NONNA_ROHSTOFF_VORRAT) - set(D.ROHSTOFFE):
        f.append("Nonna verkauft unbekannte Rohstoffe")
    # Angeln
    if set(D.FISCH_STUFE) != {x["id"] for x in fische}:
        f.append("Angeln: FISCH_STUFE muss genau die 20 Fische nennen (%s)" % sorted(set(D.FISCH_STUFE) ^ {x["id"] for x in fische}))
    if set(D.FISCH_STUFE.values()) - {1, 2, 3} or set(D.DRILL) != {0, 1, 2, 3}:
        f.append("Angeln: Stufen 1-3, Drill 0-3")
    for w in ("meer", "fluss"):
        for st in (1, 2, 3):
            if not any(x["ort"] == w and D.FISCH_STUFE[x["id"]] == st for x in fische):
                f.append("Angeln: %s hat keinen Fisch der Stufe %d" % (w, st))
        for fid, label, text, roh in D.FUNDSACHEN.get(w, []):
            if set(roh) - set(D.ROHSTOFFE):
                f.append("Fundsache %s: unbekannter Rohstoff" % fid)
    for oid, o in D.ANGEL_ORTE.items():
        if o["wasser"] not in ("meer", "fluss"):
            f.append("Angelort %s: Wasser?" % oid)
    # Quellen an Rastplaetzen und Werkzeuge (28.10.2026)
    frames = [fr for q in D.QUELLEN.values() for fr in q["frames"]]
    if len(frames) != len(set(frames)):
        f.append("Quellen: ein Frame gehoert zu zwei Plaetzen")
    for pid, q in D.QUELLEN.items():
        for art in ("holz", "stein"):
            for k in q.get(art) or {}:
                if k not in D.KNOTEN or D.KNOTEN[k]["art"] != art:
                    f.append("Quelle %s: Knoten %s passt nicht zu %s" % (pid, k, art))
        if q.get("wasser") and (q["wasser"] not in ("meer", "fluss") or not q.get("angel_bild") or not q.get("pose")):
            f.append("Quelle %s: Wasser braucht meer/fluss, angel_bild und pose" % pid)
        if not (q.get("holz") or q.get("stein") or q.get("wasser")):
            f.append("Quelle %s ist leer" % pid)
    for k, kn in D.KNOTEN.items():
        if set(kn["ertrag"]) - set(D.ROHSTOFFE):
            f.append("Knoten %s: unbekannter Rohstoff" % k)
    for wid, w in D.WERKZEUGE.items():
        if len(w["stufen"]) != 3 or w["art"] not in ("holz", "stein"):
            f.append("Werkzeug %s: 3 Stufen, Art holz/stein" % wid)
        for i, s in enumerate(w["stufen"], 1):
            if set(s["rohstoffe"]) - set(D.ROHSTOFFE) or (s["fisch"] and s["fisch"] not in D.FISCH_STUFE):
                f.append("Werkzeug %s %d: Rohstoff/Fisch unbekannt" % (wid, i))
            if "kauf_%s_%d" % (wid, i) not in D.PETRU_LADEN["zeilen"]:
                f.append("Werkzeug %s %d: Petru hat keine Uebergabe-Zeile" % (wid, i))
    if sorted(k["stufe"] for k in D.KOEDER.values()) != [1, 2, 3]:
        f.append("Koeder: genau eine Stufe 1, 2 und 3")
    for kid, k in D.KOEDER.items():                    # Koeder (30.10.2026): 2 Looks je Stufe, Rohstoffe bekannt, Petru-Zeile je Stufe
        if len(k["looks"]) != 2 or set(k["rohstoffe"]) - set(D.ROHSTOFFE) or set(k["selten"]) != {"2", "3"}:
            f.append("Koeder %s: 2 Looks, bekannte Rohstoffe, selten fuer Stufe 2 und 3" % kid)
        if "kauf_koeder_%d" % k["stufe"] not in D.PETRU_LADEN["zeilen"]:
            f.append("Koeder %s: Petru hat keine Uebergabe-Zeile" % kid)
        for lk in k["looks"]:
            if not os.path.exists(os.path.join(MOD, "farm", "koeder", lk["id"] + ".png")):
                f.append("Koeder %s: Bild farm/koeder/%s.png fehlt" % (kid, lk["id"]))
    for x in fische:                                   # Petru kauft Fisch (28.10.2026): je Art ein Satz, je Stufe ein Anteil
        if "fisch_" + x["id"] not in D.PETRU_LADEN["zeilen"]:
            f.append("Fisch %s: Petru hat keinen Satz (petru_fische.py)" % x["id"])
    if set(D.PETRU_FISCH_ANTEIL) != {"1", "2", "3"}:
        f.append("PETRU_FISCH_ANTEIL braucht die Stufen 1-3")
    return f


def laden_eintragen(lid, vorlage):
    """Buehne eines Ladens in laeden.json (Hintergrund, Figur, Gruesse) und die Turbo-Tag-Eintraege seiner Zeilen. laeden.json wird
    nicht neu gebaut, sondern nur um diesen Eintrag ergaenzt (andere Eintraege, z. B. Isabelle, bleiben unberuehrt)."""
    laden = json.loads(json.dumps(vorlage))
    tags = []
    for gruppe, liste in laden["zeilen"].items():
        for i, t in enumerate(liste):
            roh = [x.strip(" []") for x in stimme.TAG_MUSTER.findall(t)]
            klar = stimme.ohne_tags(t)
            if not roh or any(x not in ERLAUBT for x in roh) or VERBOTEN & set(klar):
                sys.exit("FEHLER: %s %s.%d: Tag/Zeichen" % (lid, gruppe, i))
            liste[i] = stimme.vorlesen(klar)
            tags.append({"wer": vorlage["wer"], "text": liste[i], "gesprochen": t})
    pfad = os.path.join(MOD, "laeden.json")
    d = json.load(open(pfad, encoding="utf-8"))
    d["laeden"][lid] = laden
    json.dump(d, open(pfad, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    pfad = os.path.join(MOD, "stimme_tags.json")
    t = json.load(open(pfad, encoding="utf-8"))
    eigene = {x["text"] for x in tags}
    t["zeilen"] = [x for x in t["zeilen"] if x["text"] not in eigene] + tags
    json.dump(t, open(pfad, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    z, fische = zutaten_bauen(), fische_bauen()
    fehler = pruefen(z, fische)
    if fehler:
        sys.exit("FEHLER:\n  " + "\n  ".join(fehler))
    fred = [{"text": stimme.vorlesen(stimme.ohne_tags(t)), "gesprochen": t} for t in D.FREDERICO]
    daten = {"_hinweis": "Gebaut von werkzeuge/eden_rise/kochen_eden_rise.py - nicht von Hand aendern.",
             "zutaten": z, "fische": fische,
             "effekte": {k: {"label": v[0], "wert": v[1], "wo": v[2]} for k, v in D.EFFEKTE.items()},
             "geschmack": {p: {"mag": m, "mag_nicht": n} for p, (m, n) in D.GESCHMACK.items()},
             "beete": D.BEETE, "pflanzen": {k: dict({"preis": p, "ertrag": e, "tage": t}, **({"flag": D.PFLANZEN_FREI[k][0], "merkt": D.PFLANZEN_FREI[k][1]} if k in D.PFLANZEN_FREI else {}))
                                             for k, (p, e, t) in D.PFLANZEN.items()},
             "tiere": D.TIERE, "tier_varianten": list(D.TIER_VARIANTEN), "tier_groesse": D.TIER_GROESSE, "tier_laut": D.TIER_LAUT,
             "nonna": {"dauerhaft": D.NONNA_DAUERHAFT, "tagesvorrat": D.NONNA_TAGESVORRAT, "ab_tag": D.NONNA_AB_TAG},
             "frederico": fred,
             "rohstoffe": {k: {"label": l, "text": t, "preis": p} for k, (l, t, p) in D.ROHSTOFFE.items()},
             "nonna_rohstoffe": D.NONNA_ROHSTOFF_VORRAT, "stahl_kampf": D.STAHL_KAMPF, "leder_kampf": D.LEDER_KAMPF, "stall_stufen": D.STALL_STUFEN,
             "angeln": {"orte": D.ANGEL_ORTE, "wuerfe": D.WUERFE_PRO_SITZUNG, "stufe": D.FISCH_STUFE,
                        "gewicht": {str(k): v for k, v in D.STUFEN_GEWICHT.items()}, "drill": {str(k): v for k, v in D.DRILL.items()},
                        "fehler": D.DRILL_FEHLER, "tempo_je_treffer": D.DRILL_TEMPO_JE_TREFFER, "wahrnehmung_zone": D.WAHRNEHMUNG_ZONE,
                        "biss": D.BISS, "fund_chance": D.FUND_CHANCE,
                        "fundsachen": {w: [{"id": i, "label": l, "text": t, "rohstoffe": r} for i, l, t, r in xs]
                                       for w, xs in D.FUNDSACHEN.items()},
                        "sammel_bonus": D.SAMMEL_BONUS},
             "abbau": {"quellen": {pid: dict(q, angel_bild_datei="eden_rise_angeln_%s.png" % pid) if q.get("wasser") else q
                                   for pid, q in D.QUELLEN.items()},
                       "menge": D.QUELLE_MENGE, "pause": D.QUELLE_PAUSE, "knoten": D.KNOTEN, "perfekt_plus": D.PERFEKT_PLUS,
                       "ring": D.RING, "stapel": D.ERNTE_STAPEL, "angel_bilder": D.ANGEL_BILDER},
             "werkzeuge": D.WERKZEUGE, "koeder": D.KOEDER,
             "petru": {"ab_tag": D.PETRU_AB_TAG, "fisch_anteil": D.PETRU_FISCH_ANTEIL,
                       "fisch_notiz": {x["id"]: stimme.ohne_tags(D.PETRU_LADEN["zeilen"]["fisch_" + x["id"]][0]) for x in fische}}}
    json.dump(daten, open(os.path.join(MOD, "kuechen.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    pfad = os.path.join(MOD, "stimme_tags.json")
    d = json.load(open(pfad, encoding="utf-8"))
    neu = [{"wer": "frederico", "text": x["text"], "gesprochen": x["gesprochen"]} for x in fred]
    eigene = {x["text"] for x in neu}
    d["zeilen"] = [x for x in d["zeilen"] if x["text"] not in eigene] + neu
    json.dump(d, open(pfad, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    laden_eintragen("nonna", D.NONNA_LADEN)
    laden_eintragen("petru", D.PETRU_LADEN)
    laden_eintragen("danzel", D.DANZEL_LADEN)
    laden_eintragen("mochis", D.MOCHIS_LADEN)
    laden_eintragen("batu", D.BATU_LADEN)
    rollen = {r: sum(1 for v in z.values() if v["rolle"] == r) for r in ("basis", "haupt", "akzent")}
    print("Kuechenkreis: %d Zutaten %s, %d Fische, %d Tiere, %d Pflanzen, %d Frederico-Saetze -> kuechen.json, stimme_tags.json"
          % (len(z), rollen, len(fische), len(D.TIERE), len(D.PFLANZEN), len(fred)))


if __name__ == "__main__":
    main()
