# -*- coding: utf-8 -*-
"""Events in Akt 2 (Duc 29.10.2026, Brain Trust Punkt 1+3): zeitlose Akt-1-Events haben ein zweites Fenster wann.akt2 =
[8, 21] (Tag 7 = Anhoerung bleibt frei), tragen "nachlauf" und treten in Akt 2 hinter neuen Events zurueck; ab Tag 8 zieht
die Engine ruhiger (AKT2_FAKTOR, hoechstens 2 Gags am Tag).

  python tests\\test_akt2_events.py
"""
import json, os, random, sys

HIER = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(HIER)
sys.path.insert(0, EDEN)
from kern import ereignisse as EV  # noqa: E402

D = json.load(open(os.path.join(EDEN, "module", "eden_rise", "ereignisse.json"), encoding="utf-8"))
IDX = {e["id"]: e for e in D["events"]}


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    nach = [e for e in D["events"] if e.get("nachlauf")]
    lang = lambda e: e["id"].startswith(("sf_", "sfn_")) or e["art"] == "abend"
    def soll(e):                                       # Akt 3 (Drehbuch Akt 3, Paket A): Gags bis Tag 31, mit Maxwell bis 29, Handy bis 21
        if lang(e):
            return [8, 35]
        if e["id"].startswith("hy_"):
            return [8, 21]
        return [8, 29] if "maxwell" in json.dumps(e, ensure_ascii=False).lower() else [8, 31]
    pruefen(len(nach) >= 200 and all(e["wann"].get("akt2") == soll(e) for e in nach), "%d Events mit Akt-2-Fenster" % len(nach))
    pruefen(sum(1 for e in nach if (e["personen"].get("selfie") or {}).get("stufe")) == 90, "Alle Selfies laufen bis Tag 35")  # 87 + Bibis Stufe 3/4/5 (727c75db)
    for bleibt in ("ab_megan_nacht", "lg_lola_meer"):
        pruefen(not IDX[bleibt].get("nachlauf"), "%s bleibt in Akt 1" % bleibt)
    pruefen(all(e["wann"]["tage"][1] <= 6 for e in nach), "Akt-1-Fenster bleiben unverändert (bis Tag 6)")
    gruppen = {"selfie": sum(1 for e in nach if (e["personen"].get("selfie") or {}).get("stufe")),
               "abend": sum(1 for e in nach if e["art"] == "abend"), "flirt": sum(1 for e in nach if e["id"].startswith("fl_")),
               "bordrat": sum(1 for e in nach if e["art"] == "bordrat")}
    pruefen(all(gruppen.values()), "Akt 2 hat wieder Selfies, Abende, Flirts und Bordräte %s" % gruppen)
    for bleibt in ("g1_helikopter", "br_megan_kommt", "hy_holm_krankenhaus", "hy_cousin_falsch", "br_abschiedsfest"):
        pruefen(not IDX[bleibt].get("nachlauf"), "%s bleibt in Akt 1" % bleibt)

    e = IDX["g1_toto_pizza"]
    w = dict(e["wann"], phasen=None)
    tage = lambda t: (w["tage"][0] <= t <= w["tage"][1]) or (w["akt2"][0] <= t <= w["akt2"][1])
    pruefen(tage(4) and not tage(7) and tage(8) and tage(21), "Fenster: Tag 4 ja, Tag 7 (Anhörung) nein, Tag 8–21 ja")

    alt, neu = {"id": "a", "nachlauf": True}, {"id": "n"}
    z8, z5 = {"tag": 8}, {"tag": 5}
    rng = random.Random(1)
    wahl = [EV._akt2_vorrang(z8, rng, [alt, neu])[0]["id"] for _ in range(400)]
    anteil = wahl.count("n") / len(wahl)
    pruefen(0.55 < anteil < 0.75, "Akt 2: neue Events gewinnen etwa zu %d %% (%.0f %%)" % (EV.AKT2_VORRANG * 100, anteil * 100))
    pruefen(EV._akt2_vorrang(z5, rng, [alt, neu]) == [alt, neu], "Akt 1: kein Vorrang")
    pruefen(EV._akt2_faktor(z8, "zufall") < 1 and EV._akt2_faktor(z5, "zufall") == 1, "ab Tag 8 zieht die Engine ruhiger")
    print("ALLES OK")


if __name__ == "__main__":
    main()
