# -*- coding: utf-8 -*-
r"""Builds the old | new approval spec for an English rewrite package (25.10.2026).

    python werkzeuge\englisch\abnahme_bauen.py pilot_tag0_hafen   -> docs\abnahme\englisch_pilot_tag0_hafen.json
    python werkzeuge\text_abnahme.py --serve docs\abnahme\englisch_pilot_tag0_hafen.json 8343

Old texts are read from the built module data (ereignisse.json, kaempfe.json) and kern/tutorial.py; new texts come
from the package module (NEU, NEUE_EVENTS). Every old text of the package must have a new one and vice versa.
"""
import importlib, json, os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(os.path.dirname(HIER))
MOD = os.path.join(EDEN, "module", "eden_rise")
sys.path.insert(0, HIER)
sys.path.insert(0, EDEN)

NAMEN = {"duc": "Duc"}


def alte_texte(prefixe, encounters, gegner, tutorial):
    """[(gruppe, key, wer, gefuehl, feld, alt, vertont)] in game order."""
    out = []
    d = json.load(open(os.path.join(MOD, "ereignisse.json"), encoding="utf-8"))
    for e in d["events"]:
        if isinstance(prefixe, set):
            if e["id"] not in prefixe:                      # explicit set of event ids (package by builder file)
                continue
        elif not (e["id"].startswith(tuple(p for p in prefixe if p.endswith("_"))) or e["id"] in prefixe):
            continue
        k, g = e["id"], "%s · %s" % (e["id"], e["titel"])
        out.append((g, k + ".titel", "", "", "Titel", e["titel"], False))
        out.append((g, k + ".lage", "", "", "Erzählung", e["lage"], False))
        for b in e["personen"].get("betroffen", []):
            out.append((g, k + ".betroffen." + b["id"], b["id"], "", "Reaktion", b["was"], False))
        for i, z in enumerate(e["zeilen"]):
            out.append((g, "%s#z%d" % (k, i), z["wer"], z["gefuehl"], "Rede", z["text"], True))
        for i, o in enumerate(e["optionen"]):
            out.append((g, "%s.o%d" % (k, i), "Duc", "", "Chip", o["text"], False))
            if o.get("zeile"):
                z = o["zeile"]
                out.append((g, "%s#o%d" % (k, i), z["wer"], z["gefuehl"], "Antwort", z["text"], True))
    if encounters or gegner:
        kd = json.load(open(os.path.join(MOD, "kaempfe.json"), encoding="utf-8"))
        for bid in encounters:
            b, g = kd["encounters"][bid], "Kampf · " + bid
            for f in ("title", "goal", "flee_reason"):
                if b.get(f):
                    out.append((g, "kampf.%s.%s" % (bid, f), "", "", f, b[f], False))
            for end, o in b["outcomes"].items():
                out.append((g, "kampf.%s.out.%s" % (bid, end), "", "", "Ausgang " + end, o["text"], False))
        for eid in gegner:
            e, g = kd["enemies"][eid], "Gegner · " + eid
            out.append((g, "gegner.%s.name" % eid, "", "", "Name", e["name"], False))
            out.append((g, "gegner.%s.attack" % eid, "", "", "Angriff", e["attack"]["label"], False))
            for slot, sp in e.get("specials", {}).items():
                out.append((g, "gegner.%s.%s" % (eid, slot), "", "", "Spezial " + slot, sp["label"], False))
            if "courage" in e.get("immune", {}):
                out.append((g, "gegner.%s.immun_courage" % eid, "", "", "Immun Mut", e["immune"]["courage"], False))
    if tutorial:
        from kern import tutorial as T
        for lek, schritte in T.LEKTIONEN.items():
            g = "Maxwells Lektion %d (kern/tutorial.py)" % lek
            for s in schritte:
                out.append((g, "tut.%s.en" % s["id"], "maxwell", "", "Rede", s["en"], True))
                out.append((g, "tut.%s.hint" % s["id"], "", "", "Hinweis", s.get("de", ""), False))
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    name = sys.argv[1] if len(sys.argv) > 1 else "pilot_tag0_hafen"
    P = importlib.import_module(name)
    texte = alte_texte(P.PREFIXE, P.ENCOUNTERS, P.GEGNER, P.TUTORIAL)
    fehlend = [t[1] for t in texte if t[1] not in P.NEU]
    uebrig = sorted(set(P.NEU) - {t[1] for t in texte})
    if fehlend or uebrig:
        sys.exit("Schlüssel ohne neuen Text: %s\nNeue Texte ohne alten Schlüssel: %s" % (fehlend, uebrig))
    gruppen, index = [], {}
    for g, key, wer, gef, feld, alt, vertont in texte:
        if g not in index:
            index[g] = len(gruppen)
            gruppen.append({"titel": g, "items": []})
        gruppen[index[g]]["items"].append({"key": key, "wer": NAMEN.get(wer, wer.capitalize()) if wer else "",
                                          "gefuehl": gef, "feld": feld, "alt": alt, "neu": P.NEU[key],
                                          "vertont": vertont and alt != P.NEU[key]})
    for g in gruppen:                                    # speaker changes (done by hand when taking over)
        for it in g["items"]:
            neu_wer = getattr(P, "SPRECHER", {}).get(it["key"])
            if neu_wer:
                it["notiz"] = "Sprecher neu: %s (vorher %s)" % (neu_wer.capitalize(), it["wer"])
                it["wer"] = neu_wer.capitalize()
                it["vertont"] = True
    for chip, ev in getattr(P, "NEUE_EVENTS", {}).items():
        g = {"titel": "NEU · Rosi wirft Terremoto (Tag-0-Chip %s)" % chip, "items": []}
        k = "hk_rosi_" + chip
        g["items"].append({"key": k + ".lage", "wer": "", "feld": "Erzählung", "alt": "", "neu": ev["lage"]})
        for i, z in enumerate(ev["zeilen"]):
            g["items"].append({"key": "%s#z%d" % (k, i), "wer": "Rosi", "gefuehl": ev["gefuehl"][i], "feld": "Rede",
                               "alt": "", "neu": z, "vertont": True})
        for i, o in enumerate(P.NEUE_OPTIONEN):
            g["items"].append({"key": "%s.o%d" % (k, i), "wer": "Duc", "feld": "Chip", "alt": "", "neu": o})
        gruppen.append(g)
    spec = {"id": "englisch_" + name, "titel": P.TITEL, "hinweis": P.HINWEIS, "gruppen": gruppen}
    ziel = os.path.join(EDEN, "docs", "abnahme", "englisch_%s.json" % name)
    os.makedirs(os.path.dirname(ziel), exist_ok=True)
    json.dump(spec, open(ziel, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    n = sum(len(g["items"]) for g in gruppen)
    geaendert = sum(1 for g in gruppen for it in g["items"] if it["alt"] != it["neu"])
    ton = sum(1 for g in gruppen for it in g["items"] if it.get("vertont"))
    print("geschrieben:", ziel, "-", n, "Texte,", geaendert, "geändert/neu,", ton, "neu zu vertonen")


if __name__ == "__main__":
    main()
