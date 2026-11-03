# -*- coding: utf-8 -*-
r"""Bibis Tier-Selfies, Nachlauf (Duc 02.11.2026): die Momente aus Runde 4/5, in denen das Tier fehlt, nicht tut was es soll oder Bibi
doppelt im Bild ist. Outfit und Frisur wie in bibi_tier_selfies_4.TIERE, nur der Moment ist neu formuliert; je Moment vier Seeds.

    bibi_tier_selfies_6.py   -> ComfyUI\output\expressions\_bibi_tier_selfies_6\<tier>_<a|b>_<n>.png
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.argv[1:] = ["", "_bibi_tier_selfies_6"]            # r4 liest den Ordner beim Import aus argv[2]
import bibi_tier_selfies_4 as r4

r4.SEEDS = (240211, 771903, 518447, 90391)
ALLEIN = " She is the only person in the picture."
NEU = {
    ("sorry", "b"): "The same spotted hyena lies beside her in the straw with its eyes shut tight and its jaws stretched wide in one huge "
                    "sleepy yawn, ears flat, utterly bored. She looks into the camera with a flat deadpan face, lips pressed together, one "
                    "eyebrow raised, as if her best joke just died" + ALLEIN,
    ("monsieur", "b"): "The grey macaque now sits on her shoulder and holds her phone in both of his hands, his serious face pushed close "
                       "to the lens and filling half the picture, slightly crooked. Right next to him she laughs with both of her hands "
                       "raised and empty" + ALLEIN,
    ("truffle", "b"): "She holds a red apple far out on her flat open palm at arm's length, well away from her face. The same huge dark "
                      "wild boar takes it very gently from her palm with its lips. She smiles with closed lips, eyes shining" + ALLEIN,
    ("pudding", "b"): "The same tiny brown bear cub, no bigger than a house cat, sits wide awake in her lap and chews happily on her small "
                      "black plush lion keychain. She gasps in mock outrage into the camera" + ALLEIN,
    ("ghost", "a"): "Behind her, high on a grey rock in the background, a snow leopard with thick pale grey spotted fur and a long fluffy "
                    "tail lies stretched out in profile, clearly visible, watching. She points back over her shoulder at it with a grin" + ALLEIN,
    ("bones", "b"): "The same bearded vulture with rusty orange chest feathers sits on the stone wall right behind her shoulder, clearly "
                    "visible, and has just dropped a big old white bone into her free hand. She holds the bone up to the camera with a "
                    "very polite, very forced smile" + ALLEIN,
    ("mr_v", "b"): "The same long grey Komodo dragon now wears her round sunglasses on its head and lies in the sun, completely "
                   "unimpressed. Her own head is bare except for the mustard bandana. She crouches a careful distance away and gives a "
                   "proud thumbs up" + ALLEIN,
}
# Je Tier nur der neue Moment; der andere ist None und wird in r4.main() uebersprungen
alt = dict(r4.TIERE)
r4.TIERE = {}
for (tier, teil), moment in NEU.items():
    outfit, haar, a, b = alt[tier]
    r4.TIERE[tier] = (outfit, haar, moment if teil == "a" else None, moment if teil == "b" else None)

if __name__ == "__main__":
    sys.argv[1] = ",".join(r4.TIERE)
    r4.main()
