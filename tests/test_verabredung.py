# -*- coding: utf-8 -*-
"""Dates nach dem Live-Spieltest vom 31.10.2026: Eine angenommene Einladung verschwindet nicht mehr still.

  python tests\\test_verabredung.py
"""
import os, sys, tempfile

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import lauf_test as L  # noqa: E402

E = L.eden


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def frei(pid):
    return {"id": "frei_%s" % pid, "anwesend": [pid], "frei": True, "titel": "Time with %s" % pid}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    L.vorbereiten("eden_rise", tempfile.mkdtemp(prefix="eden_date_"))
    from kern import chronik, gesten as G, showrunner as S
    z = E.aktion("neu", {"modus": "ironman"})
    modul = E.modul_laden()
    S.figuren_fuellen = lambda z, m, v, s: s
    S.vorrat = lambda d: {}
    tag = 7

    def stand(verabredungen, szenen, **extra):
        z["tag"], z["phase"], z["heute"], z["meldungen"] = tag, "abend", [], []
        z["verabredungen"] = verabredungen
        inhalt = dict(extra)
        if szenen is not None:
            inhalt["szenen"] = szenen
        z["plan"] = {"_moddir": "x", "phasen": {"abend": inhalt}}
        S.verabredung_einbauen(z, modul, "abend", inhalt)
        return inhalt

    i = stand([{"pid": "lola", "tag": tag, "phase": "abend"}], [frei("lola"), frei("rosi")])
    ids = [s["id"] for s in i["szenen"]]
    pruefen(ids == ["date_lola", "frei_rosi"], "das Date ersetzt ihre freie Karte")
    pruefen(not z["verabredungen"], "die Zusage ist damit erledigt")

    i = stand([{"pid": "lola", "tag": tag, "phase": "abend"}], [frei("alva"), frei("rosi"), frei("lea")])
    pruefen([s["id"] for s in i["szenen"]] == ["frei_alva", "frei_rosi", "date_lola"], "bei drei Karten fliegt die letzte freie")

    plot = {"id": "story", "anwesend": ["rosi"]}
    i = stand([{"pid": "lola", "tag": tag, "phase": "abend"}], [plot, dict(plot, id="story2"), dict(plot, id="story3")])
    pruefen([s["id"] for s in i["szenen"]] == ["story", "story2", "story3", "date_lola"], "eine Story-Szene wird nie verdraengt")

    v = {"pid": "lola", "tag": tag, "phase": "abend", "ort": "sun_deck"}
    i = stand([v], [{"id": "urteil", "anwesend": ["lola", "rosi"]}])
    pruefen([s["id"] for s in i["szenen"]] == ["urteil"], "spielt sie in der Story-Szene mit, bleibt die Szene allein")
    pruefen(v["tag"] == tag + 1 and z["verabredungen"] == [v], "das Date rueckt auf morgen")
    pruefen(v["ort"] == "sun_deck", "der gewaehlte Ort bleibt")
    pruefen("moves your date" in z["meldungen"][-1]["titel"] and "tomorrow" in z["meldungen"][-1]["kurz"], "Meldung auf Englisch")

    v = {"pid": "lola", "tag": tag, "phase": "abend"}
    anderes = {"pid": "rosi", "tag": tag + 1, "phase": "abend"}
    stand([v, anderes], None, dynamisch=True)
    pruefen(v["tag"] == tag + 2, "ein Abend mit einem anderen Date wird uebersprungen")
    pruefen("day %d" % (tag + 2) in z["meldungen"][-1]["kurz"], "die Meldung nennt den neuen Tag")

    stand([{"pid": "lola", "tag": tag - 2, "phase": "abend"}], [frei("rosi")])
    pruefen(not z["verabredungen"], "Reste aus alten Spielstaenden verschwinden")

    z["werte"]["vertrauen.lola"] = 3
    i = stand([{"pid": "lola", "tag": tag, "phase": "abend"}], [frei("lola"), frei("rosi")])
    z["heute"].append({"phase": "abend", "szene": "date_lola"})
    S.verabredung_versetzt(z, modul)
    pruefen(z["werte"]["vertrauen.lola"] == 3 and not z["meldungen"], "ein gespieltes Date hat keine Strafe")

    i = stand([{"pid": "lola", "tag": tag, "phase": "abend"}], [frei("lola"), frei("rosi")])
    z["heute"].append({"phase": "abend", "szene": "frei_rosi"})
    S.verabredung_versetzt(z, modul)
    pruefen(z["werte"]["vertrauen.lola"] < 3, "versetzt kostet Vertrauen")
    pruefen("waited for you" in z["meldungen"][-1]["titel"], "Meldung auf Englisch")
    pruefen(any(e.get("moment") == "stood_up" and "lola" in e["wer"] for e in chronik.liste(z)), "die Chronik weiss es")
    nach = z["werte"]["vertrauen.lola"]
    S.verabredung_versetzt(z, modul)
    pruefen(z["werte"]["vertrauen.lola"] == nach, "nur einmal")

    z["phase"], z["verabredungen"] = "dinner", [{"pid": "rosi", "tag": tag, "phase": "abend"}]
    einladen = {"verabredung": True, "bereich": "x", "art": "gross", "id": "einladen"}
    pruefen("already have a date" in (G.gesperrt(z, modul, {}, einladen, "lola") or ""), "zweite Einladung fuer denselben Abend gesperrt")
    z["phase"] = "abend"
    pruefen(G.gesperrt(z, modul, {}, einladen, "lola") is None, "fuer morgen geht die Einladung")
    print("Alles gut.")


if __name__ == "__main__":
    main()
