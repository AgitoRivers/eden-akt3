# -*- coding: utf-8 -*-
r"""Erinnerungen, Paket 2 (Duc 31.10.2026, STIL.md "Verstaendlich bleiben"): die Liste erinnerungen_paket2.json einmalig in die
Builder und nach stimme_tags.json uebernehmen. Bleibt als Beleg liegen.

    erinnerungen_einbau2.py <Eden-Ordner>
"""
import json, os, re, sys

B = sys.argv[1]
HIER = os.path.dirname(os.path.abspath(__file__))
L = json.load(open(os.path.join(HIER, "erinnerungen_paket2.json"), encoding="utf-8"))
TAG = re.compile(r"\s*\[[a-z ]+\]")
for x in L:
    p = os.path.join(B, x["datei"])
    s = open(p, encoding="utf-8", newline="").read()
    assert s.count(x["alt"]) == 1, (x["datei"], x["alt"], s.count(x["alt"]))
    open(p, "w", encoding="utf-8", newline="").write(s.replace(x["alt"], x["neu"]))
T = os.path.join(B, "module/eden_rise/stimme_tags.json")
d = json.load(open(T, encoding="utf-8"))
n = 0
for x in L:
    alt, neu = TAG.sub("", x["alt"]).strip(), TAG.sub("", x["neu"]).strip()
    for z in d["zeilen"]:
        if alt not in z.get("text", ""):
            continue
        z["text"] = z["text"].replace(alt, neu)
        n += 1
        g = z.get("gesprochen", "")
        if alt in g:
            z["gesprochen"] = g.replace(alt, neu)
        else:                                  # der Tag sass mitten im geaenderten Stueck: nach dem ersten Satz neu setzen
            tags = [t.strip() for t in TAG.findall(g)]
            m = re.search(r"[.!?…](?=\s)", z["text"])
            z["gesprochen"] = (z["text"][:m.end()] + " " + " ".join(tags) + z["text"][m.end():]) if m and tags else z["text"] + (" " + " ".join(tags) if tags else "")
json.dump(d, open(T, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", B, len(L), "Aenderungen,", n, "Stimm-Eintraege")
