# -*- coding: utf-8 -*-
r"""Karte (EN/DE) in den Char-Creator-Steckbriefen von Mr. Maximum, Yamamoto-san und Jana aus den .txt-Quellen neu
setzen (19.10.2026, nach dem Angleichen an Ducs Outfit-Wahl in Prompt Studio). Schreibt ueber fig_speichern
(fuehrt zusammen, nur die Karte aendert sich). Status karte bleibt "entwurf"; Export nach ST nur fuer Jana.

    cc_karten_auffrischen.py          Probelauf
    cc_karten_auffrischen.py --los    schreibt
"""
import io, sys, time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, r"X:\AI\Eden\karten_neu")
sys.path.insert(0, r"X:\AI\CharCreator")
LOS = "--los" in sys.argv
sys.argv = [sys.argv[0]]
from karten_einspielen import quelle, FELDER  # noqa: E402
sys.argv = ["creator.py", "--no-browser"]
import creator as c  # noqa: E402

for key, fid in (("maximum", "7ecccb65ef0f"), ("yamamoto", "a0ac9a8be128"), ("jana", "16f8e9cf3e9b")):
    f = c.fig_laden(fid)
    q = quelle(key)
    karte = dict(f.get("karte") or {})
    for lang in ("en", "de"):
        karte[lang] = {k: (list(q[lang][k]) if k == "alternate_greetings" else q[lang][k])
                       for k in FELDER + ["alternate_greetings", "depth_prompt"]}
    karte["erzeugt"] = time.strftime("%Y-%m-%d %H:%M:%S")
    karte["gespeichert"] = False
    print("%-15s Kostueme %s | Begruessungen %d" % (f["name_wunsch"], f["kostueme"], 1 + len(karte["en"]["alternate_greetings"])))
    if LOS:
        f["karte"] = karte
        c.fig_speichern(f)
print("geschrieben" if LOS else "PROBELAUF")
