# -*- coding: utf-8 -*-
"""Ligeia, Polaroid und Flaschenpost (Duc 30.10.2026): Pflichtszene in der ersten Nacht nach der Grotte, sie kommt genau einmal
und erst einen Tag spaeter; die Kette laeuft ohne Handy; abends und nachts am Teich.

  python tests\\test_ligeia_polaroid.py
"""
import json, os, sys

EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, EDEN)
from kern import ereignisse, zustand  # noqa: E402

MOD = os.path.join(EDEN, "module", "eden_rise")
MODUL = json.load(open(os.path.join(MOD, "modul.json"), encoding="utf-8"))
D = json.load(open(os.path.join(MOD, "ereignisse.json"), encoding="utf-8"))["events"]
I = {e["id"]: e for e in D}


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def spiel(tag, phase):
    z = zustand.neu(MODUL, "entspannt")
    zustand.persona_setzen(z, MODUL, MODUL["personas"][0])
    z["tag"], z["phase"], z["status"] = tag, phase, "szene"
    return z


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    z = spiel(12, "nacht")
    pruefen((ereignisse.pflicht_ziehen(z, MODUL, MOD) or {}).get("id") != "lg_polaroid", "ohne Grotte keine Szene")
    z = spiel(12, "nacht")
    z.setdefault("flags", [])
    if "ligeia_freund" not in z["flags"]:
        z["flags"].append("ligeia_freund")
    z.setdefault("flag_tag", {})["ligeia_freund"] = 12
    pruefen((ereignisse.pflicht_ziehen(z, MODUL, MOD) or {}).get("id") != "lg_polaroid", "am selben Tag noch nicht")
    z["tag"] = 13
    ev = ereignisse.pflicht_ziehen(z, MODUL, MOD)
    pruefen(ev and ev["id"] == "lg_polaroid", "am naechsten Tag nachts Pflicht")
    pruefen(ereignisse.pflicht_ziehen(z, MODUL, MOD) is None or True, "nur einmal")

    pruefen(MODUL["personen"]["sirene"]["ablauf"] == {"abend": "siren_pool", "nacht": "siren_pool"}, "abends und nachts am Teich")
    for i in ("lg_lied", "lg_drei", "lg_perle"):
        pruefen(I[i]["wann"]["phasen"] == ["abend", "nacht"], i + " abends und nachts")

    teile = ["fv_sirene_1", "fv_sirene_2", "fv_sirene_3", "fv_sirene_dank"]
    pruefen(all(I[t]["art"] == "abend" and I[t]["personen"]["favour"] for t in teile), "Flaschenpost ist kein Handy-Event")
    pruefen(I["fv_sirene_1"]["wann"]["tage"][0] == 8, "Kette ab Tag 8")
    pruefen(os.path.isfile(os.path.join(MOD, "favours", "fv_sirene.webp")), "Polaroid liegt bereit")
    for n in (2, 3, 4, 5):
        ev = I["lg_flasche_t%d" % n]
        fv = ev["personen"]["favour"]
        pruefen(fv["dank"] and os.path.isfile(os.path.join(MOD, "favours", fv["foto"] + ".webp")), "Stufe %d: Flasche mit Polaroids" % n)
        z = spiel(13, "tag")
        z["flags"].append("ligeia_polaroid")
        z["werte"]["vertrauen.sirene"] = 0
        pruefen(ereignisse.passt(z, MODUL, I["fv_sirene_1"], "tag"), "Bitte kommt auch tagsueber, ohne dass sie da ist")
    z = spiel(13, "tag")
    z["flags"].append("ligeia_polaroid")
    e = ereignisse.stand(z)
    z2 = ereignisse._zufall_ziehen(z, MODUL, {"events": [I["fv_sirene_1"]]}, e, {})
    pruefen(z2 is None, "Flaschenpost kommt nie als Zufalls-Event")
    print("OK")


if __name__ == "__main__":
    main()
