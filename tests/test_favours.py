# -*- coding: utf-8 -*-
"""Favours (29.10.2026): Ketten aus drei Bitten per Handy, Energie je Weg, Ablehnen beendet die Kette, Fehlschlag
mit eigener Pointe, Dank-Foto nur nach geglücktem Finale, hoechstens eine Bitte am Tag, Journal-Rubrik, Stimmen-Tags.

  python tests\\test_favours.py
"""
import json, os, sys

EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, EDEN)
from kern import ereignisse, zustand  # noqa: E402

MOD = os.path.join(EDEN, "module", "eden_rise")
MODUL = json.load(open(os.path.join(MOD, "modul.json"), encoding="utf-8"))
OK = lambda a, sg, extra: {"ergebnis": "erfolg", "wurf": 20, "summe": 20, "sg": sg}
NEIN = lambda a, sg, extra: {"ergebnis": "fehlschlag", "wurf": 1, "summe": 1, "sg": sg}


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def spiel(tag=3, phase="tag"):
    z = zustand.neu(MODUL, "entspannt")
    zustand.persona_setzen(z, MODUL, MODUL["personas"][0])
    z["tag"], z["phase"], z["status"] = tag, phase, "szene"
    z["werte"]["energie"] = 3                       # Bereich 0-3
    zustand.bekannt_machen(z, ["alva", "petru", "elsa"])
    return z


def favour(z, d, tage=12):
    """Zieht die naechste Bitte (Chance und Tageslimit wie im Spiel, ueber mehrere Phasen)."""
    e = ereignisse.stand(z)
    for _ in range(tage):
        for ph in ("tag", "nachmittag", "abend"):
            z["phase"], z["event"] = ph, None
            ev = ereignisse._favour_ziehen(z, MODUL, d, e)
            if ev:
                return ev
        z["tag"] += 1
        e["heute"] = {}
        z["werte"]["energie"] = 3                   # neuer Tag, volle Energie
    return None


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    d = ereignisse.daten(MOD)
    fv = [e for e in d["events"] if e["personen"].get("favour")]
    fv = [e for e in fv if not e["personen"]["favour"].get("stufe")]      # Stufen-Flaschen: test_ligeia_polaroid
    ketten = {e["personen"]["favour"]["kette"] for e in fv}
    pruefen(len(fv) == 36 and len(ketten) == 9, "9 Ketten mit je 3 Bitten und Dank (%d Events)" % len(fv))
    for e in fv:
        f = e["personen"]["favour"]
        if f.get("dank"):
            pruefen(os.path.isfile(os.path.join(MOD, "favours", f["foto"] + ".webp")), "Foto %s da" % f["foto"])
            continue
        wege = [o for o in e["optionen"] if o.get("probe")]
        assert len(wege) == 2 and all(o["energie"] == 1 and o.get("zeile") and o.get("zeile_fehlschlag") for o in wege), e["id"]
        assert [o for o in e["optionen"] if o.get("art") == "auflegen" and not o.get("energie")], e["id"]
    pruefen(True, "jede Bitte: 2 Wege mit Probe, 1 Energie, Pointe bei Erfolg und Fehlschlag, Ablehnen kostenlos")
    pro_figur = {}
    for e in fv:
        if not e["personen"]["favour"].get("dank"):
            pro_figur[e["personen"]["anrufer"]] = pro_figur.get(e["personen"]["anrufer"], 0) + 1
    pruefen(max(pro_figur.values()) <= 3, "hoechstens 3 Bitten je Figur")

    # Akt 2 erst ab Tag 8, Kloster nur mit Isabelles Nummer
    z = spiel(tag=3)
    frueh = {e["personen"]["anrufer"] for e in fv if e["personen"]["favour"]["teil"] == 1
             and ereignisse.passt(z, MODUL, e, "tag")}
    pruefen(frueh == {"lola", "alva", "petru", "elsa"}, "Akt 1: Lola, Alva, Petru, Elsa (%s)" % sorted(frueh))
    z = spiel(tag=9)
    spaet = {e["personen"]["anrufer"] for e in fv if e["personen"]["favour"]["teil"] == 1
             and ereignisse.passt(z, MODUL, e, "tag")}
    pruefen({"jana", "maxwell"} <= spaet and not {"nonna", "isabelle"} & spaet, "Akt 2 ohne Kloster-Nummer: kein Kloster")
    z["flags"].append("isabelle_handy")
    zustand.bekannt_machen(z, ["nonna", "isabelle"])
    spaet = {e["personen"]["anrufer"] for e in fv if e["personen"]["favour"]["teil"] == 1
             and ereignisse.passt(z, MODUL, e, "tag")}
    pruefen({"nonna", "isabelle"} <= spaet, "mit Isabelles Nummer: Nonna und Isabelle")

    # Eine Kette ganz durchspielen: Teil 1 ok, Teil 2 daneben, Teil 3 ok -> Dank mit Foto, Journal
    z = spiel(tag=2)
    e = ereignisse.stand(z)
    e["gesehen"] += [x["id"] for x in fv if x["personen"]["favour"]["kette"] != "lola"]
    ev = favour(z, d)
    pruefen(ev and ev["id"] == "fv_lola_1", "erste Bitte kommt (%s)" % (ev and ev["id"]))
    pruefen(ereignisse._favour_ziehen(z, MODUL, d, e) is None, "hoechstens eine Bitte am Tag")
    en = z["werte"]["energie"]
    r = ereignisse.waehlen(z, MODUL, MOD, 0, probe_fn=OK)["ergebnis"]
    pruefen(z["werte"]["energie"] == en - 1 and r["zeile_id"] == "fv_lola_1#o0", "Weg kostet 1 Energie, Pointe #o0")
    pruefen(ereignisse.favour_journal(z, MODUL, MOD, str)[0]["teile"][0]["ausgang"] == "ok", "Journal: geholfen")
    z["event"] = None
    pruefen(ereignisse.passt(z, MODUL, d["_index"]["fv_lola_2"], "tag") is False, "Teil 2 nicht am selben Tag")
    ev = favour(z, d)
    pruefen(ev and ev["id"] == "fv_lola_2", "Teil 2 am naechsten Tag")
    r = ereignisse.waehlen(z, MODUL, MOD, 1, probe_fn=NEIN)["ergebnis"]
    pruefen(r["zeile_id"] == "fv_lola_2#f1" and r["zeile"]["text"], "Fehlschlag mit eigener Pointe #f1")
    z["event"] = None
    ev = favour(z, d)
    pruefen(ev and ev["id"] == "fv_lola_3", "Kette geht nach Fehlschlag weiter")
    ereignisse.waehlen(z, MODUL, MOD, 0, probe_fn=OK)
    z["event"] = None
    ev = favour(z, d)
    pruefen(ev and ev["id"] == "fv_lola_dank" and z["event"]["foto"] == "/favourfoto/fv_lola.webp", "Dank mit Foto")
    ereignisse.waehlen(z, MODUL, MOD, 0)
    j = ereignisse.favour_journal(z, MODUL, MOD, lambda n: "/favourfoto/%s.webp" % n)
    pruefen(len(j) == 1 and [t["ausgang"] for t in j[0]["teile"]] == ["ok", "daneben", "ok"]
            and j[0]["foto"] == "/favourfoto/fv_lola.webp", "Journal: drei Teile und das Foto")

    # Finale daneben -> kein Dank; Ablehnen beendet die Kette; ohne Energie gesperrt
    z = spiel(tag=2)
    e = ereignisse.stand(z)
    e["gesehen"] += [x["id"] for x in fv if x["personen"]["favour"]["kette"] not in ("alva", "petru")]
    ids = []
    for _ in range(8):                                 # bis beide Ketten entschieden sind (Reihenfolge haengt am Wuerfel)
        ev = favour(z, d)
        if not ev:
            break
        ids.append(ev["id"])
        if ev["personen"]["favour"]["kette"] == "petru":
            ereignisse.waehlen(z, MODUL, MOD, 2, probe_fn=NEIN)            # Petru: ablehnen
        else:
            ereignisse.waehlen(z, MODUL, MOD, 0, probe_fn=OK if ev["id"] != "fv_alva_3" else NEIN)
        z["event"] = None
        z["tag"] += 1
        e["heute"] = {}
    pruefen("fv_petru_aus" in z["flags"] and "fv_petru_1" not in z["flags"], "Ablehnen beendet Petrus Kette")
    pruefen([i for i in ids if i.startswith("fv_petru")] == ["fv_petru_1"], "nach Ablehnen keine weitere Bitte von Petru")
    pruefen("fv_alva_3" in ids and "fv_alva_dank" not in ids, "Finale daneben: kein Dank-Foto (%s)" % ids)
    z = spiel(tag=2)
    z["werte"]["energie"] = 0
    ereignisse.stand(z)["gesehen"] += [x["id"] for x in fv if x["id"] != "fv_lola_1"]
    favour(z, d)
    z["werte"]["energie"] = 0                          # favour() fuellt beim Tageswechsel auf
    try:
        ereignisse.waehlen(z, MODUL, MOD, 0, probe_fn=OK)
        pruefen(False, "ohne Energie gesperrt")
    except ValueError:
        pruefen(True, "ohne Energie: Weg gesperrt, Ablehnen geht")
    ereignisse.waehlen(z, MODUL, MOD, 2)

    # Stimmen-Tags: jede Favour-Zeile hat einen Eintrag mit Turbo-Tag
    tags = {t["text"]: t["gesprochen"] for t in json.load(open(os.path.join(MOD, "stimme_tags.json"), encoding="utf-8"))["zeilen"]}
    zeilen = [zl["text"] for x in fv for zl in x["zeilen"] + [o[k] for o in x["optionen"] for k in ("zeile", "zeile_fehlschlag") if o.get(k)]]
    fehlt = [t for t in zeilen if "[" not in tags.get(t, "")]
    pruefen(not fehlt, "alle %d Favour-Zeilen mit Turbo-Tag %s" % (len(zeilen), fehlt[:2] or ""))
    print("\nalle Favour-Tests bestanden")


if __name__ == "__main__":
    main()
