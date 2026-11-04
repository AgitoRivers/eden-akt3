# -*- coding: utf-8 -*-
r"""Drei Belagerungs-Wahlen, die vorher nichts bewirkten (fix-akt2):

  1. Tueren mit Petru (bl_tueren_petru, Tag 22 Mittag): Das Dorf rudert in Welle 4 schon bei einem Punkt Ruf weniger (Ruf 4 statt 5),
     zusammen mit Petrus heilem Ruder bei Ruf 3 (kern/taktik._rudert, Wiki systeme/taktik.md).
  2. Alvas Runde (bl_alva_runde, Tag 21 Abend): In der Bar an Tag 22 erinnert Alva an das Versprechen, danach kommt die Rechnung
     (bl_bar_rechnung): Duc zahlt, Alva merkt es sich (Vertrauen). Ohne Versprechen gibt sie die Runde aus und es gibt keinen zweiten Takt.
  3. Dons Kirchen-Wahl (bl_kirche_don, Tag 23 Mittag): Don laeutet nuechtern, die Kirche hat in Welle 6 ein Leben mehr.

  python tests/test_belagerung_wahlen.py
"""
import json, os, sys

EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, EDEN)
from kern import ereignisse, taktik  # noqa: E402

M = os.path.join(EDEN, "module", "eden_rise")
EV = {e["id"]: e for e in json.load(open(os.path.join(M, "ereignisse.json"), encoding="utf-8"))["events"]}


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def petru():
    D = taktik.daten(M)
    schwelle = D["ruf_rudert"]
    heil, weg = {"haeuser": {D["ruder_haus"]: {"status": "gerettet"}}}, {"haeuser": {D["ruder_haus"]: {"status": "verloren"}}}
    z = lambda ruf, *f: {"werte": {"ruf": ruf}, "flags": list(f)}
    pruefen(not taktik._rudert(z(schwelle - 1), D, weg), "ohne Petru und ohne Ruder: Ruf %d reicht nicht" % (schwelle - 1))
    pruefen(taktik._rudert(z(schwelle - 1, "bl_tueren_petru"), D, weg), "Petru an den Tueren: Ruf %d reicht" % (schwelle - 1))
    pruefen(not taktik._rudert(z(schwelle - 2, "bl_tueren_petru"), D, weg), "Petru allein: Ruf %d reicht nicht" % (schwelle - 2))
    pruefen(taktik._rudert(z(schwelle - 2, "bl_tueren_petru"), D, heil), "Petru und heiles Ruder: Ruf %d reicht" % (schwelle - 2))
    for andere in ("bl_tueren_lola", "bl_tueren_mina"):
        pruefen(not taktik._rudert(z(schwelle - 1, andere), D, weg), "%s senkt die Schwelle nicht" % andere)
    # Durch beginnen: dorf_rudert steht in der echten Welle
    zz = {"flags": ["bl_tueren_petru"], "status": "wahl", "werte": {"ruf": schwelle - 1}, "tag": 22}
    taktik.beginnen(zz, M, art="echt")
    pruefen(zz["taktik"]["dorf_rudert"], "beginnen(echt) mit Petru und Ruf %d: das Dorf rudert" % (schwelle - 1))


def alva():
    bar, rechnung = EV["bl_bar"], EV["bl_bar_rechnung"]
    z = {"flags": ["bl_alva_runde"], "werte": {}}
    mit = [zl["text"] for _, zl in ereignisse.zeilen_aktiv(bar, z) if zl["wer"] == "alva"]
    ohne = [zl["text"] for _, zl in ereignisse.zeilen_aktiv(bar, {"flags": [], "werte": {}}) if zl["wer"] == "alva"]
    pruefen("promised" in mit[0] and "on the house" not in " ".join(mit), "mit Versprechen: Alva erinnert daran")
    pruefen("on the house" in ohne[0] and "promised" not in " ".join(ohne), "ohne Versprechen: die Runde geht aufs Haus")
    pruefen(len(mit) == len(ohne), "je eine Alva-Zeile pro Fassung, die anderen Zeilen bleiben")
    for o in bar["optionen"]:
        d = [f["direkt"] for f in o["folgen"] if "direkt" in f]
        pruefen(d and d[0] == [{"wenn": {"flag": "bl_alva_runde"}, "id": "bl_bar_rechnung"}], "Option '%s' fuehrt zur Rechnung" % o["text"][:30])
        z = {"flags": ["bl_alva_runde"], "werte": {}, "ev_direkt": d[0]}
        pruefen(ereignisse.direkt_ziel(z) == "bl_bar_rechnung", "  mit Versprechen: Rechnung")
        z = {"flags": [], "werte": {}, "ev_direkt": d[0]}
        pruefen(ereignisse.direkt_ziel(z) is None, "  ohne Versprechen: kein zweiter Takt")
    pruefen("phasen" not in rechnung["wann"], "Rechnung wird nie zufaellig gezogen")
    for o in rechnung["optionen"]:
        geld = sum(f.get("geld", 0) for f in o["folgen"])
        alva_v = sum(f["vertrauen"][1] for f in o["folgen"] if f.get("vertrauen", [None])[0] == "alva")
        pruefen(geld < 0 and alva_v > 0, "Rechnung '%s': Geld %d, Vertrauen Alva +%d" % (o["text"][:24], geld, alva_v))


def don():
    D = taktik.daten(M)
    finale = next(i + 1 for i, w in enumerate(D["wellen"]) if w.get("finale"))

    def kirche(flags):
        z = {"flags": list(flags), "status": "wahl", "werte": {"vertrauen.anghjulu": 3}, "tag": 23}
        taktik.beginnen(z, M, art="echt")
        t = z["taktik"]
        taktik._welle_start(z, D, t, finale)
        return t["kirche"], t["kirche_max"], t

    k0, m0, _ = kirche([])
    k1, m1, t = kirche(["bl_kirche_don"])
    pruefen((k1, m1) == (k0 + 1, m0 + 1), "Welle %d mit Don: Kirche %d/%d statt %d/%d" % (finale, k1, m1, k0, m0))
    kj, _, _ = kirche(["bl_kirche_casanova"])
    pruefen(kj == k0, "Casanova in der Kirche: kein Extra-Leben")
    vorher = t["kirche"]
    taktik._welle_start({"flags": ["bl_kirche_don"], "werte": {}, "tag": 23, "lp": 100}, D, t, finale)
    pruefen(t["kirche"] == vorher, "zweiter Start derselben Welle zaehlt das Leben nicht doppelt")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    petru()
    alva()
    don()
    print("\nalles gruen")


if __name__ == "__main__":
    main()
