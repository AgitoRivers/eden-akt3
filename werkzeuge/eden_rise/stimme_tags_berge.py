# -*- coding: utf-8 -*-
r"""Turbo-Tags fuer alle Sprechzeilen des Ortskapitels Berge (Duc 26.10.2026: mindestens ein Tag je Zeile).

    python werkzeuge\eden_rise\stimme_tags_berge.py      ergaenzt fehlende Eintraege in module\eden_rise\stimme_tags.json

Der Tag folgt dem Gefuehl der Zeile (Sprite-Gefuehl im Event), bei mehreren Saetzen nach dem ersten Satz, sonst am
Anfang. Bestehende Eintraege bleiben unberuehrt; die Datei behaelt ihr Format (CRLF, Einrueckung 1)."""
import json, os, re, sys

EDEN = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, EDEN)
from kern import stimme  # noqa: E402

MOD = os.path.join(EDEN, "module", "eden_rise")
PRAEFIXE = ("bg_", "hy_ghjuvan_tot", "hy_dumenica_huette",
            "a2_", "gr_", "kv_", "hy_gennaro_weg", "hy_matteu",          # Akt 2 Woche 2 (27.10.2026)
            "fn_",                                                       # Flut-Nacht (28.10.2026)
            "lg_",                                                       # Ligeia (29.10.2026)
            "hb_")                                                       # Holm kommt zurueck (30.10.2026)
TAG = {"sadness": "sigh", "grief": "sniff", "remorse": "sigh", "disappointment": "sigh", "fear": "gasp",
       "surprise": "gasp", "nervousness": "gasp", "anger": "clear throat", "annoyance": "sigh", "disgust": "sniff",
       "disapproval": "clear throat", "amusement": "chuckle", "joy": "laugh", "optimism": "chuckle",
       "gratitude": "sigh", "relief": "sigh", "caring": "sigh", "love": "sniff", "pride": "chuckle",
       "approval": "chuckle", "admiration": "chuckle", "curiosity": "clear throat", "neutral": "clear throat",
       "confusion": "sigh", "realization": "gasp", "excitement": "laugh", "embarrassment": "chuckle", "desire": "sigh"}


def setzen(text, tag):
    m = re.search(r"(?<!Mr)[.!?…](?=\s)|\s-\s", text)
    if not m:
        return "[%s] %s" % (tag, text)
    return text[:m.end()].rstrip() + " [%s] " % tag + text[m.end():].lstrip()


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ev = json.load(open(os.path.join(MOD, "ereignisse.json"), encoding="utf-8"))["events"]
    zeilen = []
    for e in ev:
        if not e["id"].startswith(PRAEFIXE):
            continue
        zeilen += e["zeilen"] + [o["zeile"] for o in e["optionen"] if o.get("zeile")]
    for g in json.load(open(os.path.join(MOD, "kaempfe.json"), encoding="utf-8"))["enemies"].values():
        zeilen += g.get("untouchable_hinweise") or []                    # Sirene im Kampf (29.10.2026): kampf.sirene.<n>
        zeilen += [h for liste in (g.get("sprueche") or {}).values() for h in liste]   # Riccis: kampf.<gegner>.<art>.<n>
    for b in json.load(open(os.path.join(MOD, "kaempfe.json"), encoding="utf-8"))["encounters"].values():
        zeilen += [h for liste in (b.get("sprueche") or {}).values() for h in liste]   # Gruppen-Sprueche (29.10.2026)
    pfad = os.path.join(MOD, "stimme_tags.json")
    d = json.load(open(pfad, encoding="utf-8"))
    da = {z["text"] for z in d["zeilen"]}
    neu = []
    for z in zeilen:
        if z["text"] in da:
            continue
        g = setzen(z["text"], TAG.get(z.get("gefuehl"), "sigh"))
        assert stimme.ohne_tags(g).replace("  ", " ") == z["text"], g
        neu.append({"wer": z["wer"], "text": z["text"], "gesprochen": g})
        da.add(z["text"])
    if neu:
        d["zeilen"] += neu
        json.dump(d, open(pfad, "w", encoding="utf-8", newline="\r\n"), ensure_ascii=False, indent=1)
    print("Berge: %d Zeilen, %d neu getaggt" % (len(zeilen), len(neu)))


if __name__ == "__main__":
    main()
