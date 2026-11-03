# -*- coding: utf-8 -*-
r"""Bibis Tier-Selfies, Monsieur A (Duc 02.11.2026): a_3 aus bibi_tier_selfies_7 gewaehlt, aber mit Straehnen am Gesicht
(face-framing tendrils). Gleicher Seed (518447), zwei Formulierungen der Frisur; kein Edit im Set (Hautton).

    bibi_tier_selfies_8.py   -> ComfyUI\output\expressions\_bibi_tier_selfies_8\monsieur_<v>_1.png
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.argv[1:] = ["", "_bibi_tier_selfies_8"]            # r4 liest den Ordner beim Import aus argv[2]
import bibi_tier_selfies_4 as r4

r4.SEEDS = (518447,)
HAARE = {
    "a": "half up half down with a small knot on top of her head, a middle part, no bangs, soft wavy face-framing tendrils falling "
         "loose on both sides of her face down to her chin, the rest long and straight over her shoulders",
    "b": "half up half down with a small knot on top of her head, a middle part, no bangs, two long curled face-framing tendrils "
         "hanging loose in front of her ears down past her cheeks, the rest long and straight over her shoulders",
}
outfit, _, moment, _ = r4.TIERE["monsieur"]
moment += ". She is the only person in the picture."

if __name__ == "__main__":
    for v, haar in HAARE.items():
        # r4.main() benennt nach Tier und Teil; die Variante steht im Teil-Namen ueber einen eigenen Tier-Schluessel
        r4.TIERE = {"monsieur_" + v: (outfit, haar, moment, None)}
        sys.argv[1] = "monsieur_" + v
        r4.main()
