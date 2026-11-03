# -*- coding: utf-8 -*-
r"""Spielbilder der Selfie-Events (Duc 27.10.2026): die abgenommenen PNGs aus werkzeuge\eden_rise\selfie_daten.json
("bilder": frau|reihe|grad -> PNG) als WebP nach module\eden_rise\selfies\<frau>_<reihe>_<1-3>.webp (1152 hoch, Q 88).
Alte Spielbilder, die keine Reihe mehr nutzt, gehen in den Papierkorb.

    selfie_webp.py            alle bauen
    selfie_webp.py --liste    nur zeigen, was entstuende
"""
import json, os, sys

EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATEN = os.path.join(EDEN, "werkzeuge", "eden_rise", "selfie_daten.json")
ZIEL = os.path.join(EDEN, "module", "eden_rise", "selfies")
STUFE = {"knapp": 1, "oben_ohne": 2, "nackt": 3}
H = 1152


def papierkorb(pfad):
    from ctypes import windll, wintypes, Structure, byref, c_uint, c_wchar_p

    class OP(Structure):
        _fields_ = [("hwnd", wintypes.HWND), ("wFunc", c_uint), ("pFrom", c_wchar_p), ("pTo", c_wchar_p),
                    ("fFlags", wintypes.WORD), ("fAnyOperationsAborted", wintypes.BOOL), ("hNameMappings", wintypes.LPVOID),
                    ("lpszProgressTitle", c_wchar_p)]
    op = OP(None, 3, pfad + "\0", None, 0x40 | 0x10 | 0x4, False, None, None)   # FO_DELETE, ALLOWUNDO|NOCONFIRMATION|SILENT
    windll.shell32.SHFileOperationW(byref(op))


def main():
    from PIL import Image
    bilder = json.load(open(DATEN, encoding="utf-8"))["bilder"]
    soll = {}
    for key, png in bilder.items():
        frau, reihe, grad = key.split("|")
        soll["%s_%s_%d.webp" % (frau, reihe, STUFE[grad])] = png
    if "--liste" in sys.argv:
        for n in sorted(soll):
            print(n, "<-", os.path.basename(soll[n]))
        return
    os.makedirs(ZIEL, exist_ok=True)
    for n, png in sorted(soll.items()):
        im = Image.open(png).convert("RGB")
        im = im.resize((round(im.width * H / im.height), H), Image.LANCZOS)
        im.save(os.path.join(ZIEL, n), "WEBP", quality=88, method=6)
    # Bibis Tier-Selfies (bibi_fang_*, werkzeuge/bibi_fang_webp.py) gehoeren nicht zu diesen Reihen und bleiben liegen
    alt = [f for f in os.listdir(ZIEL) if f.endswith(".webp") and f not in soll and not f.startswith("bibi_fang_")]
    for f in alt:
        papierkorb(os.path.join(ZIEL, f))
    print("%d Spielbilder geschrieben, %d alte in den Papierkorb: %s" % (len(soll), len(alt), ", ".join(alt)))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
