# -*- coding: utf-8 -*-
r"""Textabnahme-Seite fuer die Saetze eines Haendlers (26.10.2026): python werkzeuge\eden_rise\haendler_abnahme.py toto

Schreibt docs\abnahme\haendler_<id>.json (Format von werkzeuge\text_abnahme.py). Anzeigen:
    python werkzeuge\text_abnahme.py --serve docs\abnahme\haendler_toto.json 8357
"""
import json, os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(os.path.dirname(HIER))
sys.path.insert(0, HIER)

STUFEN = {0: "stranger, selling hard", 1: "he remembers you", 2: "friends, with jokes", 3: "he starts to confide",
          4: "family", 5: "brother"}
KAT = {"intim": "intimate", "schmuck": "jewellery", "papier": "paper and books", "technik": "tools and tech", "essen": "food",
       "alkohol": "alcohol", "party": "party", "natur": "sea and nature", "kampf": "combat gear", "schmuggel": "contraband",
       "ressource": "supplies", "werkzeug": "tools"}


def spec(pid):
    mod = __import__("haendler_" + pid)
    zeilen, gefuehl = getattr(mod, pid.upper() + "_ZEILEN"), getattr(mod, pid.upper() + "_GEFUEHL")

    def item(gruppe, i, text, wer, feld):
        g = gefuehl.get(gruppe)
        g = g[i] if isinstance(g, list) else g
        return {"key": "haendler:%s.%s.%d" % (pid, gruppe, i), "feld": feld, "alt": "", "neu": text, "wer": wer,
                "gefuehl": g or "neutral", "vertont": False}

    gruppen = []
    for n in range(6):
        g = "gruss_%d" % n
        gruppen.append({"titel": "Greetings · trust %d · %s" % (n, STUFEN[n]),
                        "items": [item(g, i, t, "Totò", "greeting %d" % (i + 1)) for i, t in enumerate(zeilen[g])]})
    for k, label in KAT.items():
        g = "kauf_" + k
        if g in zeilen:
            tag = "gift: " if k in ("intim", "schmuck", "papier", "technik", "essen", "alkohol", "party", "natur") else "ware: "
            gruppen.append({"titel": "After buying · %s%s" % (tag, label),
                            "items": [item(g, i, t, "Totò", "reaction %d" % (i + 1)) for i, t in enumerate(zeilen[g])]})
    hint = {}
    for g in zeilen:
        if g.startswith("hinweis_"):
            _, kat, wer = g.split("_", 2)
            hint.setdefault(kat, []).append((wer, g))
    for kat, lst in hint.items():
        gruppen.append({"titel": "Hints (always true) · gift: %s" % KAT[kat],
                        "items": [item(g, 0, zeilen[g][0], "Totò", "hints at %s" % wer) for wer, g in lst]})
    gruppen.append({"titel": "Other · selling to him, no money, general",
                    "items": [item(g, i, t, "Totò", "%s %d" % (g, i + 1)) for g in ("kauf", "verkauf", "pleite")
                              for i, t in enumerate(zeilen[g])]})
    n = sum(len(g["items"]) for g in gruppen)
    return {"id": "haendler_" + pid, "titel": "Totò: Händler-Sätze (%d)" % n,
            "hinweis": "Pilot. Sechs Vertrauensstufen mit je acht Grüßen, Reaktionen auf den Kauf je Kategorie (bei Geschenken neckt er), "
                       "wahre Hinweise darauf, wer das Geschenk mögen könnte (etwa 40 % der Geschenk-Käufe), dazu Verkauf und Pleite. "
                       "Das Gefühl pro Satz ist das Sprite (neutral als Standard). Nach deinem OK vertone ich alles.",
            "gruppen": gruppen}


if __name__ == "__main__":
    pid = sys.argv[1] if len(sys.argv) > 1 else "toto"
    s = spec(pid)
    ziel = os.path.join(EDEN, "docs", "abnahme", "haendler_%s.json" % pid)
    json.dump(s, open(ziel, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(ziel, s["titel"])
