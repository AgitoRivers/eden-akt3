# -*- coding: utf-8 -*-
r"""Granaten-Klaenge zur Abnahme (Duc 27.10.2026): Splint ziehen + Wurf gibt es bei Pixabay nicht -> ElevenLabs.

    python werkzeuge\eden_rise\granaten_klang.py            fehlende Varianten erzeugen (vorhandene bleiben)
    python werkzeuge\eden_rise\granaten_klang.py --liste    nur anzeigen

Ablage: docs\abnahme\granaten_klang\<id>_<n>.mp3. Die Einschlag-Kandidaten kommen direkt vom Pixabay-CDN
(docs\abnahme\granaten_klang\index.html); die gewaehlten wandern danach in sfx_pixabay.py."""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sfx_erzeugen as E  # noqa: E402  (ElevenLabs-Aufruf und Schluessel, nie ausgegeben)

ZIEL = os.path.join(E.EDEN, "docs", "abnahme", "granaten_klang")
KLAENGE = [
    {"id": "granate_splint", "dauer": 1.6, "einfluss": 0.6,
     "prompt": "close foley: the safety pin of a metal hand grenade is pulled with a sharp metallic ring ping, "
               "the spoon lever flips off with a click, then a short fast whoosh as it is thrown, dry, no explosion"},
    {"id": "granate_splint_kurz", "dauer": 1.0, "einfluss": 0.7,
     "prompt": "hand grenade pin pull: quick metallic clink of a ring and pin, spring lever snap, tiny air whoosh, "
               "close and dry, no explosion"},
]
VARIANTEN = 2


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    os.makedirs(ZIEL, exist_ok=True)
    offen = [(s, n) for s in KLAENGE for n in range(1, VARIANTEN + 1)
             if not os.path.exists(os.path.join(ZIEL, "%s_%d.mp3" % (s["id"], n)))]
    for s, n in offen:
        print("%s_%d  %.1f s  %s" % (s["id"], n, s["dauer"], s["prompt"][:70]))
    if "--liste" in sys.argv or not offen:
        return
    key = E.schluessel()
    for s, n in offen:
        open(os.path.join(ZIEL, "%s_%d.mp3" % (s["id"], n)), "wb").write(E.erzeugen(key, s))
        print("ok", s["id"], n)


if __name__ == "__main__":
    main()
