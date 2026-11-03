# -*- coding: utf-8 -*-
"""Bibis Arc (Duc 02.11.2026): Romanze erst mit allen drei Flags, Umriss und Seite im Field Book, Kosenamen nur auf dem Romanzen-Weg."""
import copy, json, os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HIER))
sys.stdout.reconfigure(encoding="utf-8")
from kern import figurenrahmen, mochis, rollen, stimme, szene  # noqa: E402

MOD = os.path.join(os.path.dirname(HIER), "module", "eden_rise")
MODUL = json.load(open(os.path.join(MOD, "modul.json"), encoding="utf-8"))
EV = {e["id"]: e for e in json.load(open(os.path.join(MOD, "ereignisse.json"), encoding="utf-8"))["events"]}
FLAGS = ["kl_loewe_frei", "rt_ausgang_alle", "rt_bibi_bleibt"]


def stand(flags=(), **werte):
    return {"flags": list(flags) + ["mochis_offen"], "werte": dict(werte), "tag": 20, "status": "wahl", "mochis": {"tiere": {}, "halsbaender": 0}}


def karte_duc(z):
    return next((k for k in mochis.ansicht(z, MODUL)["karten"] if k["id"] == "duc"), None)


def main():
    mochis.offen = lambda z, modul: "mochis_offen" in z["flags"]
    m = copy.deepcopy(MODUL)
    assert not m["personen"]["bibi"]["romanzierbar"]
    # Zwei von drei Flags reichen nicht, auch nicht fuer Begehren
    z = stand(FLAGS[:2])
    rollen.romanze_abgleichen(z, m)
    assert not m["personen"]["bibi"]["romanzierbar"] and "begehren.bibi" not in z["werte"]
    # Alle drei: Romanze mit Begehren, und ein anderer Stand ohne Flags nimmt es wieder weg
    z = stand(FLAGS)
    rollen.romanze_abgleichen(z, m)
    assert m["personen"]["bibi"]["romanzierbar"] and z["werte"]["begehren.bibi"] == 1
    rollen.romanze_abgleichen(stand(), m)
    assert not m["personen"]["bibi"]["romanzierbar"]

    # Field Book: kein Umriss vor Begehren 4, dann namenlos, nach dem Gestaendnis die Seite
    assert karte_duc(stand(FLAGS, **{"begehren.bibi": 3})) is None
    k = karte_duc(stand(FLAGS, **{"begehren.bibi": 4}))
    assert k["status"] == "nicht_da" and k["name"] == "?" and not k["art"], k
    k = karte_duc(stand(FLAGS + ["bibi_seite"], **{"begehren.bibi": 4}))
    assert k["name"] == "Spatz" and "Clipboard" in k["gestrichen"] and any("Release" in s for s in k["seiten"]), k
    assert mochis.ansicht(stand(), MODUL)["gesamt"] == len(MODUL["mochis"]["tiere"])       # zaehlt nicht als Tier

    # Jedes Tier hat ein Selfie-Text und keine zweite Spur sagt mehr „Same collar“
    assert all(t.get("selfie") for t in MODUL["mochis"]["tiere"].values())
    for eid, e in EV.items():
        if eid.startswith("mo_") and eid.endswith("_wieder"):
            assert "Same collar" not in e["zeilen"][0]["text"], eid

    # Leiter: gesperrt ohne Romanze, jede Szene mit Bedingung auf alle drei Flags
    for eid in ("rm_b1", "rm_b2", "rm_b3", "rm_b4"):
        bed = json.dumps(EV[eid]["wann"]["bedingung"])
        assert all(f in bed for f in FLAGS), eid
        assert EV[eid]["wann"].get("leiter"), eid
    assert "rt_bibi_bleibt" in json.dumps(EV["rm_b4"]["wann"]) and "mo_freigelassen" in json.dumps(EV["rm_b4"]["wann"])

    # Am Feuer das Versprechen, bei der Idee der Rueckbezug
    assert any("every one of them" in z_["text"] for z_ in EV["rt_lager"]["zeilen"])
    assert "I heard you at the fire" in EV["rt_wn_bibi"]["optionen"][0]["text"]

    # Kosenamen: ohne Romanze bleibt es Clipboard
    z = stand()
    z["werte"]["vertrauen.bibi"] = 5
    assert figurenrahmen._erster(z, "bibi", figurenrahmen.figur(MODUL, "bibi")["anrede"]) == "Clipboard"
    z["werte"]["begehren.bibi"] = 4
    assert figurenrahmen._erster(z, "bibi", figurenrahmen.figur(MODUL, "bibi")["anrede"]) == "mon loup"
    # Romanze ohne ST-Karte: Szene und Handy brauchen trotzdem einen Bogen (Absturz im Bot-Lauf 02.11.2026)
    assert szene.karte(MODUL, MODUL["personen"]["bibi"])["bogen"]
    # Deutsche Kosenamen: nur die Stimme bekommt die Lautschrift aus der Hoerprobe (Duc 02.11.2026), Woerter mit gleichem Anfang bleiben
    assert stimme.aussprechen("Hase, Bärchen, Hasen, Phase") == "Haaseh, Bear-shen, Hasen, Phase"
    print("test_bibi_arc ok")


if __name__ == "__main__":
    main()
