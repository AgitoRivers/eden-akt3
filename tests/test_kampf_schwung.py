# -*- coding: utf-8 -*-
"""Ducs Schlag als Bildfolge (Duc 03.11.2026, werkzeuge/kampf_schwung.py): jede Duc-Figur ausser Gemelli hat sechs
Bilder schwung_a ... schwung_f, gleich gross wie ihre Posen, die Fuesse auf der Bodenlinie. Der Server meldet sie in
duc_bilder, damit der Client sie bei "Attack" und beim Konter abspielt.

  python tests\\test_kampf_schwung.py
"""
import os, sys, tempfile

from PIL import Image

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import lauf_test as L  # noqa: E402

E = L.eden
KAMPF = os.path.join(os.path.dirname(HIER), "module", "eden_rise", "kampf")
BODEN_TOLERANZ = 12


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    namen = E.kampf.SCHWUNG
    sets = sorted(d for d in os.listdir(KAMPF) if d.startswith("Duc") and not d.endswith("Gun"))
    pruefen(len(sets) >= 22, "%d Duc-Figuren ohne Gemelli" % len(sets))
    for s in sets:
        idle = Image.open(os.path.join(KAMPF, s, "idle.webp"))
        boden = idle.getchannel("A").point(lambda a: 255 if a > 40 else 0).getbbox()[3]
        for n in namen:
            p = os.path.join(KAMPF, s, n + ".webp")
            pruefen(os.path.isfile(p), "%s/%s da" % (s, n)) if n == namen[0] else None
            im = Image.open(p)
            if im.size != idle.size:
                raise AssertionError("%s/%s hat %s statt %s" % (s, n, im.size, idle.size))
        unten = Image.open(os.path.join(KAMPF, s, namen[-1] + ".webp")).getchannel("A").point(lambda a: 255 if a > 40 else 0).getbbox()[3]
        if abs(unten - boden) > BODEN_TOLERANZ:
            raise AssertionError("%s: Fuesse auf %d statt %d" % (s, unten, boden))
    pruefen(True, "alle Bildfolgen so gross wie die Posen, Fuesse auf der Bodenlinie (±%d px)" % BODEN_TOLERANZ)

    L.vorbereiten("eden_rise", tempfile.mkdtemp(prefix="eden_schwung_"))
    z = E.aktion("neu", {"modus": "ironman"})
    z = E.aktion("persona", {"index": 0})
    if z["status"] == "prolog":
        z = E.aktion("prolog", {})
    E.kampf_starten(z, E.modul_laden(), "hafen_dieb_test")
    E.sichern(z)
    b = E.ansicht(E.aktiv())["z"]["kampf"]["duc_bilder"]
    pruefen(all(b.get(n) and "/schwung_" in b[n] for n in namen), "die Kampfansicht meldet die sechs Bilder")
    print("OK")


if __name__ == "__main__":
    main()
