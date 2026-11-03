# -*- coding: utf-8 -*-
r"""Bibis Tier-Selfies, Monsieur A neu (Duc 02.11.2026): Duc nimmt Monsieur B aus dem Nachlauf (bibi_tier_selfies_6, b_2), dort
ohne Pony mit Mittelscheitel. Moment A bekommt dieselbe Frisur, damit die Mini-Szene zusammenpasst; vier Seeds.

    bibi_tier_selfies_7.py   -> ComfyUI\output\expressions\_bibi_tier_selfies_7\monsieur_a_<n>.png
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.argv[1:] = ["", "_bibi_tier_selfies_7"]            # r4 liest den Ordner beim Import aus argv[2]
import bibi_tier_selfies_4 as r4

r4.SEEDS = (240211, 771903, 518447, 90391)
HAAR = ("half up half down with a small knot on top of her head, a middle part, no bangs, her forehead free, a few thin loose "
        "strands at her temples, the rest long and straight over her shoulders")
outfit, _, a, _ = r4.TIERE["monsieur"]
r4.TIERE = {"monsieur": (outfit, HAAR, a + ". She is the only person in the picture.", None)}

if __name__ == "__main__":
    sys.argv[1] = "monsieur"
    r4.main()
