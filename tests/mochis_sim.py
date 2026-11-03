# -*- coding: utf-8 -*-
"""Rettungen der Tierstation messen (Duc 01.11.2026): je Tier und Spielertyp mehrere echte Kaempfe. Der Spieler kaempft das Tier muede und wirft
die Schlafgranate bei hoechstens 10 % LP (kern/kampf.schlaf_chance). Aufruf: python tests/mochis_sim.py [Laeufe je Tier, Standard 5]"""
import copy, json, os, random, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import expedition_sim as S  # noqa: E402

E, K, B = S.E, S.K, S.B
LEVEL = 6                  # etwa dort steht Duc, wenn die Station offen ist


class Retter(S.Messung):
    def __init__(self, typ, rng):                          # keine Zeitmessung, also kein Audio-Index noetig
        self.typ, self.rng = typ, rng

    def zug(self, z, k, modul):
        g = k["gegner"][0]
        granate = next((x for x in E.kampf.gegenstaende(z, modul) if x["id"] == "grenade_sleep" and not x["gesperrt"]), None)
        if granate and g["lp"] <= .10 * g["lp_max"]:
            return "gegenstand", "grenade_sleep"
        if self.typ != "einfach" and g["lp"] <= .25 * g["lp_max"]:       # jetzt nicht mehr hart zuschlagen
            return "angriff", None
        return super().zug(z, k, modul)


def main():
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
    laeufe = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    print("Tier            Typ       gerettet  Niederlage  weg   Zuege")
    K.bis_freie_phase(7)                                   # einmal vorspielen, jeder Kampf startet von diesem Stand
    K.flags_setzen("mochis_offen", "rt_ausgang_alle", "rt_ende_tag", "bg_u1_fertig")
    z = E.aktiv()
    z["tag"] = 20                                          # vor der Belagerungs-Sperre (ab Tag 21 Nachmittag nur bl_)
    z.setdefault("flag_tag", {})["rt_ende_tag"] = 3       # alle Spuren offen (spaetestes Tier 17 Tage danach)
    E.sichern(z)
    S.Messung.stufe(Retter("klug", None), LEVEL)
    start = copy.deepcopy(E.aktiv())
    for tid in json.load(open(os.path.join(S.MOD, "modul.json"), encoding="utf-8"))["mochis"]["tiere"]:
        for typ in S.PARADE:
            m = Retter(typ, random.Random(tid + typ))
            zaehl, zuege = {"aufgabe": 0, "niederlage": 0, "weg": 0}, 0
            for i in range(laeufe):
                E.sichern(copy.deepcopy(start))
                E.aktion("mochis_spur", {"id": tid})
                E.aktion("event_wahl", {"index": 0})
                E.aktion("event_schliessen", {})
                assert E.aktiv()["status"] == "kampf", E.aktiv()["status"]
                erg, n, _ = m.kampf(E.modul_laden())
                zaehl["aufgabe" if erg == "aufgabe" else "niederlage" if erg in ("niederlage", "flucht") else "weg"] += 1
                zuege += n
            print("%-15s %-9s %5d/%d  %8d  %4d  %5.1f" % (tid, typ, zaehl["aufgabe"], laeufe, zaehl["niederlage"], zaehl["weg"], zuege / laeufe))


if __name__ == "__main__":
    main()
