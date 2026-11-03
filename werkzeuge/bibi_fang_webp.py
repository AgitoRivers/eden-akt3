# -*- coding: utf-8 -*-
r"""Spielbilder fuer Bibis Tier-Selfies (Duc 02.11.2026): je gefangenem Tier eine Mini-Szene aus zwei Bildern, A dann B.
Die abgenommenen PNGs (Runden karten_neu/bibi_tier_selfies_4 bis _8) als WebP nach module\eden_rise\selfies\bibi_fang_<tier>_<a|b>.webp
(1152 hoch, Q 88). <tier> ist der Schluessel aus mochis_daten.TIERE.

    bibi_fang_webp.py
"""
import os

EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUELLE = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions"
ZIEL = os.path.join(EDEN, "module", "eden_rise", "selfies")
H = 1152
# Tier (mochis_daten) -> (Bild A, Bild B), Pfade relativ zu QUELLE; Wahl Duc 02.11.2026
WAHL = {
    "hund": ("_bibi_tier_selfies_4/biscuit_a_1", "_bibi_tier_selfies_4/biscuit_b_2"),
    "hyaene": ("_bibi_tier_selfies_4/sorry_a_1", "_bibi_tier_selfies_6/sorry_b_2"),
    "affe": ("_bibi_tier_selfies_8/monsieur_b_a_1", "_bibi_tier_selfies_6/monsieur_b_2"),
    "madame": ("_bibi_tier_selfies_4/madame_a_1", "_bibi_tier_selfies_4/madame_b_1"),
    "capybara": ("_bibi_tier_selfies_4/monday_a_2", "_bibi_tier_selfies_4/monday_b_1"),
    "schildkroete": ("_bibi_tier_selfies_4/twelve_a_1", "_bibi_tier_selfies_4/twelve_b_2"),
    "schneeleopard": ("_bibi_tier_selfies_6/ghost_a_2", "_bibi_tier_selfies_4/ghost_b_2"),
    "mufflon": ("_bibi_tier_selfies_5/duchess_a_1", "_bibi_tier_selfies_5/duchess_b_1"),
    "rotpanda": ("_bibi_tier_selfies_5/rusty_a_1", "_bibi_tier_selfies_5/rusty_b_1"),
    "keiler": ("_bibi_tier_selfies_5/truffle_a_2", "_bibi_tier_selfies_6/truffle_b_1"),
    "geier": ("_bibi_tier_selfies_5/bones_a_2", "_bibi_tier_selfies_6/bones_b_2"),
    "waran": ("_bibi_tier_selfies_5/mr_v_a_1", "_bibi_tier_selfies_6/mr_v_b_1"),
    "wolf": ("_bibi_tier_selfies_5/sunday_a_2", "_bibi_tier_selfies_5/sunday_b_2"),
    "baerchen": ("_bibi_tier_selfies_5/pudding_a_2", "_bibi_tier_selfies_6/pudding_b_2"),
}


def main():
    from PIL import Image
    os.makedirs(ZIEL, exist_ok=True)
    for tier, paar in WAHL.items():
        for teil, rel in zip("ab", paar):
            im = Image.open(os.path.join(QUELLE, rel.replace("/", os.sep) + ".png")).convert("RGB")
            im = im.resize((round(im.width * H / im.height), H), Image.LANCZOS)
            im.save(os.path.join(ZIEL, "bibi_fang_%s_%s.webp" % (tier, teil)), quality=88, method=6)
    print(len(WAHL) * 2, "Bilder ->", ZIEL)


if __name__ == "__main__":
    main()
