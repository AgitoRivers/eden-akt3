# -*- coding: utf-8 -*-
r"""Auffangstation (fix-akt2): Rosis Schlafgranate (mo_schlafgranate) und die Halsband-Kiste (mo_halsbaender) liefen nur bis Tag 21,
die Spuren im Field Book aber bis Tag 35. Wer das dritte Halsband erst in Akt 3 schnitt, bekam die Kiste nie, und die Kommission
an Tag 35 (mo_kommission) sah nichts. Jetzt: Granate so lange wie die Spuren, Kiste bis Tag 34 (vor der Kommission).

  python tests/test_mochis_fenster.py
"""
import copy, json, os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HIER))
from kern import ereignisse  # noqa: E402

MOD = os.path.join(os.path.dirname(HIER), "module", "eden_rise")
MODUL = json.load(open(os.path.join(MOD, "modul.json"), encoding="utf-8"))
EV = {e["id"]: e for e in json.load(open(os.path.join(MOD, "ereignisse.json"), encoding="utf-8"))["events"]}


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def stand(tag, flags):
    return {"tag": tag, "phase": "tag", "flags": list(flags), "flag_tag": {"rt_ende_tag": 11}, "werte": {}, "inventar": []}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    spur_ende = max(e["wann"]["tage"][1] for i, e in EV.items() if i.startswith("mo_") and i.endswith("_spur"))
    pruefen(spur_ende == 35, "Spuren laufen bis Tag %d" % spur_ende)
    pruefen(EV["mo_schlafgranate"]["wann"]["tage"] == [11, spur_ende], "Granate: Fenster %s wie die Spuren" % EV["mo_schlafgranate"]["wann"]["tage"])
    kiste, kommission = EV["mo_halsbaender"]["wann"]["tage"], EV["mo_kommission"]["wann"]["tage"]
    pruefen(kiste == [11, kommission[0] - 1], "Kiste: Fenster %s, endet vor der Kommission an Tag %d" % (kiste, kommission[0]))
    # Ohne die Belagerungs-Sperre (die gehoert zu Fix 4) muss die Kiste in Akt 3 ziehen, an Tag 35 nicht mehr
    m = copy.deepcopy(MODUL)
    m.pop("sperre", None)
    flags = ["rt_ende_tag", "mo_halsband_3", "mochis_offen"]
    for tag, soll in ((21, True), (28, True), (34, True), (35, False)):
        ist = ereignisse.passt(stand(tag, flags), m, EV["mo_halsbaender"], "tag", pflicht=True)
        pruefen(ist == soll, "Kiste an Tag %d: %s" % (tag, "zieht" if soll else "zieht nicht"))
        ist = ereignisse.passt(stand(tag, flags), m, EV["mo_schlafgranate"], "tag", pflicht=True)
        pruefen(ist, "Granate an Tag %d: zieht" % tag)
    print("\nalles gruen")


if __name__ == "__main__":
    main()
