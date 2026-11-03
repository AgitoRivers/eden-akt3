# -*- coding: utf-8 -*-
"""Entdeckte Vorlieben (18.10.2026): erstmalige und doppelte Entdeckung, positive/negative/neutrale Geschenke,
Ausnahmen (zu frueh, fuer jemand anderen), Nebenfiguren, Kochen, Dorftratsch, Story-Effekt, Meldung/gelesen,
Speichern und Laden, alte Spielstaende. Die Geschenkwirkung selbst bleibt unveraendert.

  python tests\\test_vorlieben.py
"""
import copy, os, sys, tempfile

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import lauf_test as L  # noqa: E402

E = L.eden
H = E.handel
VL = E.vorlieben


def basis():
    L.vorbereiten("eden_rise", tempfile.mkdtemp(prefix="eden_vorl_"))
    L.random.seed(5)
    protokoll = {"schritte": [], "erledigt": {}}
    z = E.aktion("neu", {"modus": "ironman"})
    while not (z["tag"] >= 3 and z["status"] == "wahl"):
        a = L.schritt(z, protokoll)
        if a[0] != "_tagesarbeit":
            L.versuch(a, protokoll)
        z = E.aktiv()
    return z


def item_mit(modul, pid, wert, ohne_intim=True):
    return next(i for i, it in sorted(modul["items"].items()) if (it.get("geschenk") or {}).get(pid) == wert
                and not it.get("nur_fuer") and (not ohne_intim or not it.get("intim")) and it["art"] == "geschenk")


def schenke(z, modul, pid, iid, npc=False):
    z["inventar"].append(iid)
    z["geschenke"].pop(pid, None)
    return (H.schenken_npc if npc else H.schenken)(z, modul, iid, pid)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    modul = E.modul_laden()
    z0 = basis()
    z0["vorlieben"] = []

    # 1) erstmalige Entdeckung (mag) - Wirkung wie ohne Vorlieben-System
    z = copy.deepcopy(z0)
    iid = item_mit(modul, "rosi", 2)
    v0 = E.zustand.punkte(z, "vertrauen.rosi")
    zeilen, w = schenke(z, modul, "rosi", iid)
    assert w == 2 and E.zustand.punkte(z, "vertrauen.rosi") > v0
    v = VL.bekannt(z, "rosi", iid)
    assert v and v["reaktion"] == "mag" and v["quelle"] == "geschenk" and not v["gelesen"] and not v["gemeldet"], v
    assert v["tag"] == z["tag"] and v["text"]
    print("OK erstmalige Entdeckung")

    # 2) doppelt: dasselbe noch einmal -> kein zweiter Eintrag, keine neue Meldung
    VL.melden(z, {"rosi|" + iid})
    z["tag"] += 1
    schenke(z, modul, "rosi", iid)
    assert len([x for x in z["vorlieben"] if x["figur"] == "rosi" and x["item"] == iid]) == 1
    assert not [x for x in z["vorlieben"] if not x["gemeldet"]], "bekannte Vorliebe meldet sich nicht neu"
    print("OK doppelte Entdeckung")

    # 3) negativ und neutral
    z = copy.deepcopy(z0)
    neg, neu = item_mit(modul, "rosi", -1), item_mit(modul, "rosi", 0)
    schenke(z, modul, "rosi", neg)
    assert VL.bekannt(z, "rosi", neg)["reaktion"] == "mag_nicht"
    z["tag"] += 1
    schenke(z, modul, "rosi", neu)
    assert not VL.bekannt(z, "rosi", neu), "neutral erzeugt keinen Eintrag"
    print("OK negativ und neutral")

    # 4) Ausnahmen: intim zu frueh -> kein Eintrag; Einzigartiges fuer jemand anderen -> abgelehnt, kein Eintrag
    z = copy.deepcopy(z0)
    intim = next(i for i, it in sorted(modul["items"].items()) if it.get("intim") and (it.get("geschenk") or {}).get("rosi", 0) != 0)
    z["werte"]["vertrauen.rosi"] = 0
    _, grund = schenke(z, modul, "rosi", intim)
    assert isinstance(grund, str) and not VL.bekannt(z, "rosi", intim), "zu frueh sagt nichts ueber den Geschmack"
    fremd = next(i for i, it in modul["items"].items() if it.get("nur_fuer") and it["nur_fuer"] != "rosi")
    z["inventar"].append(fremd)
    z["geschenke"].pop("rosi", None)
    try:
        H.schenken(z, modul, fremd, "rosi")
        raise AssertionError("haette abgelehnt werden muessen")
    except ValueError:
        pass
    assert not VL.bekannt(z, "rosi", fremd)
    print("OK Ausnahmen (zu frueh, fuer jemand anderen)")

    # 5) Nebenfigur
    z = copy.deepcopy(z0)
    iid = item_mit(modul, "petru", 2)
    schenke(z, modul, "petru", iid, npc=True)
    assert VL.bekannt(z, "petru", iid)["reaktion"] == "mag" and "He " in VL.bekannt(z, "petru", iid)["text"]
    print("OK Nebenfigur (mit Pronomen)")

    # 6) Kochen fuer eine Person (nicht fuer die Crew)
    z = copy.deepcopy(z0)
    regeln = E.json.load(open(os.path.join(E.moddir("eden_rise"), "gegenstaende.json"), encoding="utf-8"))["kochen"]
    gericht = next(i for i, it in modul["items"].items() if it.get("art") == "gericht" and (it.get("geschenk") or {}).get("lea") == 2)
    alt = E.wuerfel.random.randint
    E.wuerfel.random.randint = lambda a, b: 15
    H.kochen_aktion(z, modul, regeln, gericht, "lea")
    assert VL.bekannt(z, "lea", gericht)["quelle"] == "gericht"
    z2 = copy.deepcopy(z0)
    z2["essen_tag"] = {}
    H.kochen_aktion(z2, modul, regeln, gericht, "crew")
    E.wuerfel.random.randint = alt
    assert not z2["vorlieben"], "Crew-Essen deckt nichts auf"
    print("OK Kochen")

    # 7) Dorftratsch: ab Vertrauen 2, einmal am Tag
    z = copy.deepcopy(z0)
    z.pop("vorlieben_tratsch", None)            # seit dem Hafenkampf (Tag 2) kennt Duc Alva - im Lauf kann sie schon getratscht haben
    wer = E.rollen.rolle(modul, "dorfohr")
    z["werte"]["vertrauen." + wer] = 1
    assert VL.tratsch(z, modul) is None, "unter Vertrauen 2 kein Tratsch"
    z["werte"]["vertrauen." + wer] = 2
    a = VL.tratsch(z, modul)
    assert a and a["quelle"] == "tratsch" and a["figur"] != wer
    assert VL.tratsch(z, modul) is None, "nur einmal am Tag"
    z["tag"] += 1
    assert VL.tratsch(z, modul), "am naechsten Tag wieder"
    print("OK Dorftratsch")

    # 8) Story-Effekt ueber die normalen Folgen
    z = copy.deepcopy(z0)
    iid = item_mit(modul, "chiara", 1)
    zeilen = E.zustand.folgen_anwenden(z, modul, [{"vorliebe": {"figur": "chiara", "item": iid, "reaktion": "mag"}}])
    assert VL.bekannt(z, "chiara", iid)["quelle"] == "story" and zeilen
    assert not E.zustand.folgen_anwenden(z, modul, [{"vorliebe": {"figur": "chiara", "item": iid, "reaktion": "mag"}}])
    print("OK Story-Effekt")

    # 9) Meldung, gelesen, Speichern und Laden, Ansicht
    z = E.aktiv()
    z["vorlieben"] = []
    iid = item_mit(modul, "rosi", 2)
    VL.entdecken(z, modul, "rosi", iid, "mag", "geschenk")
    E.sichern(z)
    v = E.ansicht(E.aktiv())["z"]["vorlieben"]
    assert [x["item"] for x in v["neu"]] == [iid] and v["je_figur"]["rosi"][0]["bild"] is not None
    E.aktion("vorliebe_gemeldet", {"schluessel": ["rosi|" + iid]})
    v = E.ansicht(E.aktiv())["z"]["vorlieben"]
    assert not v["neu"] and not v["je_figur"]["rosi"][0]["gelesen"], "gemeldet, aber noch nicht gelesen"
    E.aktion("vorliebe_gelesen", {"figur": "rosi", "item": iid})
    assert VL.bekannt(E.aktiv(), "rosi", iid)["gelesen"], "gelesen bleibt nach dem Laden"
    assert any(p["id"] == "rosi" and p["bild"] and p["sprite"] for p in E.ansicht(E.aktiv())["z"]["profile"])
    print("OK Meldung, gelesen, Speichern/Laden, Profil")

    # 10) alte Spielstaende: ohne Sammlung -> leer, nichts wird aufgedeckt
    z = copy.deepcopy(z0)
    z.pop("vorlieben", None)
    E.zustand.angleichen(z, modul)
    assert z["vorlieben"] == []
    print("OK alte Spielstaende")
    print("OK")


if __name__ == "__main__":
    main()
