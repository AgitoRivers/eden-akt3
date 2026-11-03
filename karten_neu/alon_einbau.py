# -*- coding: utf-8 -*-
r"""Alon ins Spiel (Duc 02.11.2026, „ja ok bau das Ende“, Abnahme alon_satz): 22 Posen nach module\eden_rise\figuren\Alon, ohne die Endung _2.

    alon_einbau.py          Probelauf
    alon_einbau.py --los
Danach: python -X utf8 werkzeuge\gesichter_messen.py --neu
"""
import glob, os, shutil, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import alon_gesicht as G  # noqa: E402

SATZ = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions\_alon_satz"
ZIEL = r"X:\AI\Eden\module\eden_rise\figuren\Alon"


def main():
    bilder = sorted(glob.glob(os.path.join(SATZ, "*.png")))
    assert len(bilder) == 22, len(bilder)
    assert not os.path.exists(ZIEL), "Zielordner existiert schon, Abbruch"
    namen = [os.path.basename(p).replace("_2.png", ".png") for p in bilder]
    assert len(set(namen)) == 22
    if "--los" not in sys.argv:
        sys.exit("PROBELAUF - mit --los einbauen: " + ", ".join(namen))
    os.makedirs(ZIEL)
    for p, n in zip(bilder, namen):
        shutil.copy2(p, os.path.join(ZIEL, n))
    with open(os.path.join(ZIEL, "_name.txt"), "w", encoding="utf-8") as f:
        f.write("alon_standard")
    with open(os.path.join(ZIEL, "_prompt.txt"), "w", encoding="utf-8") as f:
        f.write("Wearing: %s\nScene: Plain beige background\n" % G.ANZUG)
    print("eingebaut:", len(glob.glob(os.path.join(ZIEL, "*.png"))))


if __name__ == "__main__":
    main()
