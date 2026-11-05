# -*- coding: utf-8 -*-
"""Turbo-Tags in Akt 3 passen zum Gefuehl (Duc 05.11.2026): keine Seufzer oder Raeuspern auf froehlichen Zeilen,
[shush] dort, wo jemand um Schweigen bittet. Liest die Quellen, weil stimme_tags.json kein Gefuehl kennt."""
import glob, os, re
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = os.path.join(BASE, "werkzeuge", "eden_rise")
QUELLEN = glob.glob(os.path.join(W, "ereignisse_akt3_*.py")) + [os.path.join(W, n) for n in ("kommission_akt3.py", "ereignisse_sandru_name.py")]
ZEILE = re.compile(r'''(?:G|S)\("(\w+)",\s*"((?:[^"\\]|\\.)*)"((?:\s*"(?:[^"\\]|\\.)*")*)\s*,\s*"(\w+)"\)''')
FROH = {"joy", "amusement", "excitement"}
fehler, n = [], 0
for q in QUELLEN:
    s = open(q, encoding="utf-8").read()
    for m in ZEILE.finditer(s):
        n += 1
        text = m.group(2) + "".join(re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(3)))
        erster = re.match(r"\s*(\[[a-z ]+\])", text)
        if erster and erster.group(1) in ("[sigh]", "[clear throat]") and m.group(4) in FROH:
            fehler.append("%s:%d %s %s bei %s" % (os.path.basename(q), s.count("\n", 0, m.start()) + 1, m.group(1), erster.group(1), m.group(4)))
        if re.search(r"(?<!\[shush\] )\bDon't tell (Bibi|Lea)\b", text):
            fehler.append("%s:%d %s: [shush] vor der Bitte um Schweigen" % (os.path.basename(q), s.count("\n", 0, m.start()) + 1, m.group(1)))
for f in fehler:
    print(f)
assert not fehler, "%d Tags passen nicht" % len(fehler)
assert n > 600, n
print("ok test_akt3_tags (%d Zeilen)" % n)
