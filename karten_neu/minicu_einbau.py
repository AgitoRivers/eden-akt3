# -*- coding: utf-8 -*-
r"""Minicu ins Spiel (Duc 01.11.2026, Abnahme minicu_satz): 22 Posen nach module\eden_rise\figuren\Minicu, ohne die Endung _2 wie in den anderen NPC-Saetzen.

    minicu_einbau.py          Probelauf
    minicu_einbau.py --los
Danach: python -X utf8 werkzeuge\gesichter_messen.py --neu
"""
import glob, os, shutil, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import casting_minicu as cm  # noqa: E402

SATZ = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions\_minicu_satz"
ZIEL = r"X:\AI\Eden\module\eden_rise\figuren\Minicu"


def main():
    bilder = sorted(glob.glob(os.path.join(SATZ, "*.png")))
    assert len(bilder) == 22, len(bilder)
    assert not os.path.exists(ZIEL), "Zielordner existiert schon, Abbruch"
    namen = [os.path.basename(p).replace("_2.png", ".png") for p in bilder]
    assert len(set(namen)) == 22
    print("\n".join(namen))
    if "--los" not in sys.argv:
        sys.exit("PROBELAUF - mit --los einbauen")
    os.makedirs(ZIEL)
    for p, n in zip(bilder, namen):
        shutil.copy2(p, os.path.join(ZIEL, n))
    with open(os.path.join(ZIEL, "_name.txt"), "w", encoding="utf-8") as f:
        f.write("minicu_standard")
    with open(os.path.join(ZIEL, "_prompt.txt"), "w", encoding="utf-8") as f:
        f.write("Wearing: %s\nScene: Plain beige background\n" % cm.VARIANTEN["1"][2])
    print("eingebaut:", len(glob.glob(os.path.join(ZIEL, "*.png"))))


if __name__ == "__main__":
    main()
