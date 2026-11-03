# -*- coding: utf-8 -*-
"""Crew-Moral als Wochenstimmung (27.10.2026, Variante C): Skala, Momente doppelt, Alltag bis +2, Verfall ueber
Nacht, Wuerfel, Bordrat, Geschenke, Abschluss - gegen das echte Modul eden_rise.

  python tests\\test_moral.py
"""
import json, os, random, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
from kern import moral, zustand  # noqa: E402

MODUL = json.load(open(os.path.join(BASE, "module", "eden_rise", "modul.json"), encoding="utf-8"))


def stand(w=0, tag=3):
    return {"id": "test", "tag": tag, "werte": {"moral": w, "vertrauen.rosi": 2, "vertrauen.lea": 3}, "flags": [],
            "inventar": [], "codex": [], "uhren": {}}


def setzen(z, folgen):
    zustand.folgen_anwenden(z, MODUL, folgen)
    return moral.wert(z)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    assert moral.aktiv(MODUL)
    assert MODUL["werte"]["moral"]["bereich"] == [-5, 5] and MODUL["werte"]["moral"]["start"] == 0
    for w, s in [(5, "buzzing"), (4, "buzzing"), (3, "good"), (1, "good"), (0, "calm"), (-1, "tense"), (-3, "tense"),
                 (-4, "mutinous"), (-5, "mutinous")]:
        assert moral.stufe(stand(w), MODUL) == s, (w, s)
    print("OK Stufen")

    assert setzen(stand(0), [{"wert": "moral", "delta": 1}]) == 2, "Moment +1 zaehlt doppelt"
    assert setzen(stand(0), [{"wert": "moral", "delta": -1}]) == -2, "Moment -1 zaehlt doppelt"
    assert setzen(stand(4), [{"wert": "moral", "delta": 2}]) == 5, "Deckel +5"
    assert setzen(stand(0), [moral.folge(1, "alltag")]) == 1
    assert setzen(stand(1), [moral.folge(1, "alltag")]) == 2
    assert setzen(stand(2), [moral.folge(1, "alltag")]) == 2, "Alltag nur bis +2"
    assert setzen(stand(-3), [moral.folge(1, "alltag")]) == -2, "Alltag holt aus dem Minus"
    assert setzen(stand(0), [moral.folge(2, "genau")]) == 2, "Rum: genau +2"
    assert setzen(stand(0), [moral.folge(-2, "genau")]) == -2
    print("OK Momente, Alltag, genau")

    z = stand(3)
    moral.morgen(z, MODUL)
    assert moral.wert(z) == 2, "Verfall ueber Nacht"
    z = stand(-2)
    moral.morgen(z, MODUL)
    assert moral.wert(z) == -2, "kein Verfall unter 0"
    z = stand(0)
    zeilen = moral.morgen(z, MODUL)
    assert moral.wert(z) == 0 and any("Calm" in x for x in zeilen), zeilen
    print("OK Nacht + Fruehstueckszeile")

    assert moral.wuerfel_bonus(stand(4), MODUL, ["rosi", "lea"]) == [("Lea's got your back", 1)], "beste Vertraute"
    assert moral.wuerfel_bonus(stand(4), MODUL, ["toto"]) == [], "ohne Crew kein Bonus"
    assert moral.wuerfel_bonus(stand(-2), MODUL, ["rosi"]) == [("The crew is sulking", -1)]
    assert moral.wuerfel_bonus(stand(-1), MODUL, ["rosi"]) == []
    assert moral.nach_probe(stand(0), MODUL, {"ergebnis": "patzer"}, ["chiara"]) == [moral.folge(-1, "genau")]
    assert moral.nach_probe(stand(0), MODUL, {"ergebnis": "patzer"}, ["toto"]) == []
    print("OK Wuerfel + Patzer")

    assert moral.dritter_weg(stand(4), MODUL) == {"vorteil": True, "sg": 0}
    assert moral.dritter_weg(stand(1), MODUL) == {"vorteil": False, "sg": 0}
    assert moral.dritter_weg(stand(-1), MODUL) == {"vorteil": False, "sg": 2}
    rng = random.Random(1)
    kand = [{"ton": "ernst"}, {"ton": "witzig"}]
    zaehl = sum(moral.gewichtet(stand(-5), MODUL, rng, kand)["ton"] == "ernst" for _ in range(2000))
    assert zaehl > 1200, "Mutinous zieht ernste Events: %d/2000" % zaehl
    print("OK Bordrat + Ton")

    assert moral.grund_gefuehl(stand(5), MODUL, "chiara") == "joy"
    assert moral.grund_gefuehl(stand(-2), MODUL, "chiara") == "annoyance"
    assert moral.grund_gefuehl(stand(-2), MODUL, "toto") == "neutral"
    assert moral.grund_gefuehl(stand(2), MODUL, "chiara") == "neutral"
    assert moral.szene_hinweis(stand(0), MODUL) is None and "tense" in moral.szene_hinweis(stand(-1), MODUL)
    assert moral.geduld(stand(4), MODUL)[0] == 1 and moral.geduld(stand(-1), MODUL)[0] == -1 and not moral.geduld(stand(2), MODUL)
    print("OK Sprites, Prompt, Anhoerung")

    gaben = 0
    for tag in range(2, 40):
        z = stand(5, tag)
        if MODUL["items"].get("espresso") and any("🎁" in str(x) for x in moral.geschenk(z, MODUL)):
            gaben += 1
            assert moral.geschenk(z, MODUL) == [], "hoechstens ein Geschenk am Tag"
    assert 15 <= gaben <= 37, "Geschenk-Chance 70 %%: %d von 38" % gaben
    assert moral.geschenk(stand(3, 5), MODUL) == [], "nur bei Buzzing"
    print("OK Geschenke (%d von 38 Buzzing-Morgen)" % gaben)

    # Lolas Fruehstuecksgeschenke: Snack mit Tipp ab 2, Energy Bar ab 3, Space Cake ab 4; hoechstens jeden zweiten Tag,
    # nicht zusaetzlich zum Crew-Geschenk
    def lola(v, tag, w=0):
        z = stand(w, tag)
        z["werte"]["vertrauen.lola"] = v
        return z

    def woche(v, tage=range(2, 80)):
        z, gaben = lola(v, 2), {}
        for tag in tage:
            z["tag"] = tag
            r = moral.freundes_geschenk(z, MODUL)
            if r:
                assert r[0].startswith("🎁") and "Lola" in r[0], r
                iid = z["inventar"].pop()                      # Inventar leeren: es hat nur begrenzt Platz
                gaben[iid] = gaben.get(iid, 0) + 1
                assert moral.freundes_geschenk(z, MODUL) == [], "nur eins am Morgen"
        return z, gaben
    assert woche(1)[1] == {}, "unter Vertrauen 2 nichts"
    z, g2 = woche(2)
    assert g2 and all(MODUL["items"][i]["art"] == "snack" and not MODUL["items"][i].get("ab") for i in g2), g2
    assert len(z["vorlieben"]) >= len(g2) and all(v["reaktion"] == "mag" for v in z["vorlieben"]), "Tipp = Vorliebe"
    z, g3 = woche(3)
    assert "energieriegel" in g3 and "space_cake" not in g3, g3
    z, g4 = woche(4)
    assert "space_cake" in g4, g4
    n = sum(g4.values())
    assert 18 <= n <= 39, "hoechstens jeden zweiten Tag: %d Geschenke in 78 Tagen" % n
    for tag in range(2, 40):                                       # Tag-Abstand mindestens 2
        z = lola(4, tag)
        z["morgen_geschenk_tag"] = {"lola": tag - 1}
        assert moral.freundes_geschenk(z, MODUL) == []
    z = lola(2, 5)                                                 # alle Snack-Vorlieben bis auf eine bekannt -> genau die
    from kern import vorlieben
    kand = [(i, f) for i, it in MODUL["items"].items() if it.get("art") == "snack" and "lola" in (it.get("wo") or [])
            and not it.get("ab") for f, w in (it.get("geschenk") or {}).items() if w >= 2 and f != "lola"]
    for i, f in kand[1:]:
        vorlieben.entdecken(z, MODUL, f, i, "mag", "story")
    for tag in range(5, 60):
        z["tag"] = tag
        if moral.freundes_geschenk(z, MODUL):
            assert z["inventar"][-1] == kand[0][0], (z["inventar"], kand[0])
            break
    for tag in range(2, 40):
        zeilen = moral.morgen(lola(5, tag, w=5), MODUL)
        assert sum(1 for x in zeilen if str(x).startswith("🎁")) <= 1, "ein Geschenk je Fruehstueck"
    for i in ("space_cake", "brownie_calm"):
        assert MODUL["items"][i]["kampf"] == {"ausdauer_runden": [1, 5]}, i
    # Gras-Kuchen: Kater einmal am naechsten Morgen, Brownie Moral +1, Ferrandi findet sie (10 %, Truhe 5 %)
    from kern import handel
    assert MODUL["items"]["space_cake"].get("gras") and MODUL["items"]["brownie_calm"].get("gras")
    z = stand(0, 4)
    z["werte"]["energie"] = 3
    z["inventar"] = ["space_cake", "brownie_calm"]
    handel.benutzen(z, MODUL, "space_cake")
    e = z["werte"]["energie"]
    handel.benutzen(z, MODUL, "brownie_calm")
    assert moral.wert(z) == 0, "selbst essen gibt nie Moral (Duc 27.10.)"
    assert z["kater_tag"] == 4 and handel.kater(z, MODUL) == [], "noch derselbe Tag"
    e = z["werte"]["energie"]
    z["tag"] = 5
    zeilen = moral.morgen(z, MODUL)
    assert zeilen[0].startswith("😵") and z["werte"]["energie"] == e - 1, (zeilen, z["werte"]["energie"])
    z["tag"] = 6
    e = z["werte"]["energie"]
    moral.morgen(z, MODUL)
    assert z["werte"]["energie"] == e, "Kater nur einmal"
    funde = truhe = 0
    for tag in range(2, 202):
        z = stand(0, tag)
        z["werte"]["ruf"] = 3
        z["inventar"], z["truhe"] = ["space_cake"], ["brownie_calm"]
        zeilen = handel.tagesende(z, MODUL)
        if "space_cake" not in z["inventar"]:
            funde += 1
            assert any("Ferrandi" in str(x) for x in zeilen) and z["werte"]["ruf"] <= 2, zeilen
        truhe += "brownie_calm" not in z["truhe"]
    assert 8 <= funde <= 35 and 1 <= truhe <= 22, (funde, truhe)
    for i in ("tim_tam_slam", "cannoli", "brownie_calm", "cuban_rum"):
        it = MODUL["items"][i]
        assert not any(f.get("wert") == "moral" for f in (it.get("benutzen") or []) + (it.get("gras_folgen") or [])), i
        assert "moral" not in (it.get("text") or "").lower(), (i, it.get("text"))

    # Verbrauchsware aus dem Inventar: Energy Bar wirkt; Konsum gibt nie Moral (auch Fresh Catch und Pesto nicht)
    z = stand(0, 4)
    z["werte"]["energie"] = 2
    z["inventar"] = ["energieriegel"]
    handel.benutzen(z, MODUL, "energieriegel")
    assert z["werte"]["energie"] == 3 and moral.wert(z) == 0 and z["inventar"] == []
    for i in ("frischer_fang", "lolas_pesto"):
        assert not any(f.get("wert") == "moral" for f in MODUL["items"][i].get("wirkung") or []), i

    # Geschenke nur, was Duc nicht schon hat; volles Inventar: nichts
    z = stand(0, 8)
    z["werte"]["vertrauen.lola"] = 3
    z["inventar"] = ["energieriegel"]
    for tag in range(8, 80):
        z["tag"] = tag
        vorher = list(z["inventar"])
        r = moral.freundes_geschenk(z, MODUL)
        if r:
            assert len(z["inventar"]) == len(vorher) + 1, (r, vorher, z["inventar"])
            z["inventar"] = ["energieriegel"]
    voll = stand(0, 9)
    voll["werte"]["vertrauen.lola"] = 4
    voll["inventar"] = [i for i, it in MODUL["items"].items() if it.get("art") == "geschenk"][:zustand.inventar_plaetze(voll, MODUL)]
    assert all(moral.freundes_geschenk(dict(voll, tag=t, inventar=list(voll["inventar"])), MODUL) == [] for t in range(2, 40))
    print("OK Gras-Kuchen (Ferrandi: %d/200 Inventar, %d/200 Truhe)" % (funde, truhe))
    print("OK Lolas Geschenke (V2 %s, V3 %s, V4 %s)" % (sum(g2.values()), sum(g3.values()), g4))

    print("OK Abschluss")
    print("OK")


if __name__ == "__main__":
    main()
