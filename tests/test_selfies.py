# -*- coding: utf-8 -*-
"""Selfie-Events (27.10.2026): Selfie je erreichter Stufe 3/4/5, Reihe je Durchlauf, Vorrang, Nachschlag, Bilder,
Andenken, Stimme ohne Emojis.

  python tests\\test_selfies.py
"""
import json, os, sys

EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, EDEN)
from kern import ereignisse, stimme, zustand  # noqa: E402

MOD = os.path.join(EDEN, "module", "eden_rise")
MODUL = json.load(open(os.path.join(MOD, "modul.json"), encoding="utf-8"))
ROMANZE = ("chiara", "sophia", "lea", "rosi", "siri", "alva", "lola")
OHNE = ("megan", "jana", "elsa", "isabelle")


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def spiel(tag=3, phase="abend"):
    z = zustand.neu(MODUL, "entspannt")
    zustand.persona_setzen(z, MODUL, MODUL["personas"][0])
    z["tag"], z["phase"], z["status"] = tag, phase, "szene"
    for k in [k for k in z["werte"] if k.startswith("begehren.")]:
        z["werte"][k] = 0                            # nur die Frau im Test soll ein Selfie schicken koennen
    return z


def ziehen(z, d):
    """Handy-Spur einmal ziehen (Tageslimit zuruecksetzen) -> Event oder None."""
    e = ereignisse.stand(z)
    e["heute"] = {}
    return ereignisse._handy_ziehen(z, MODUL, d, e)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    d = ereignisse.daten(MOD)
    sel = [e for e in d["events"] if (e["personen"].get("selfie") or {}).get("stufe")]
    pruefen(len(sel) == 90, "90 Selfie-Events, davon 3 von Bibi (%d)" % len(sel))   # Bibi seit 02.11.2026
    fehlt = [e["personen"]["selfie"]["bild"] for e in sel
             if not os.path.isfile(os.path.join(MOD, "selfies", e["personen"]["selfie"]["bild"] + ".webp"))]
    pruefen(not fehlt, "alle Spielbilder da %s" % (fehlt or ""))
    for f in ROMANZE + tuple(OHNE):
        stufen = {e["personen"]["selfie"]["stufe"] for e in sel if e["personen"]["selfie"]["frau"] == f}
        pruefen(stufen == {3, 4, 5}, "%s: Stufen 3/4/5" % f)
        for s in (3, 4, 5):
            it = MODUL["items"].get("%s_selfie_%d" % (f, s)) or {}
            pruefen(it.get("vitrine") and it.get("echo"), "%s: Andenken Stufe %d mit Echo" % (f, s))
            pruefen(any(e["id"] == "sfn_%s_%d" % (f, s) for e in d["events"]), "%s: Nachschlag Stufe %d" % (f, s))
            # Das Echo des Andenkens ist ihre Antwort auf das Kompliment: je Stufe in allen Reihen dieselbe Zeile
            reihen = [e for e in sel if e["personen"]["selfie"]["frau"] == f and e["personen"]["selfie"]["stufe"] == s]
            pruefen(all(e["optionen"][1]["zeile"]["text"] == it["echo"]["text"] for e in reihen), "%s: Echo Stufe %d in jeder Reihe" % (f, s))

    # Romanze: nichts unter Begehren 3, dann Stufe fuer Stufe, Reihe bleibt
    z = spiel()
    z["werte"]["begehren.alva"] = 2
    x = ziehen(z, d)
    pruefen(not (x and x["id"].startswith("sf_alva")), "Alva: kein Selfie bei Begehren 2")
    z["werte"]["begehren.alva"] = 5
    gezogen = []
    for _ in range(6):
        x = ziehen(z, d)
        if x and x["id"].startswith("sf_alva"):
            gezogen.append(x["personen"]["selfie"])
    pruefen([s["stufe"] for s in gezogen] == [3, 4, 5], "Alva: Begehren 5 -> Stufen nacheinander 3, 4, 5 (%s)"
            % [s["stufe"] for s in gezogen])
    pruefen(len({s["reihe"] for s in gezogen}) == 1, "Alva: eine Reihe im Durchlauf (%s)" % gezogen[0]["reihe"])

    # Reihe ohne die Stufe -> Ausweichen (Jana: die Koje hat kein Nacktbild)
    z = spiel()
    z["werte"]["vertrauen.jana"] = 5
    z["flags"].append("jana_abend")
    e = ereignisse.stand(z)
    e["selfie_stufen"] = {"jana": [3, 4]}
    e["selfie_reihe"] = {"jana": "koje"}
    x = ziehen(z, d)
    pruefen(x and x["personen"]["selfie"]["frau"] == "jana" and x["personen"]["selfie"]["stufe"] == 5,
            "Jana: Stufe 5 kommt aus einer anderen Reihe (%s)" % (x and x["id"]))

    # Kein Selfie haengt an Akt 1 (Duc 30.10.2026): alle bis Tag 35, Megan und Elsa nur ueber Vertrauen
    pruefen(all(e["wann"].get("akt2") == [8, 35] for e in sel), "alle Selfies bis Tag 35")
    # Tag 20: ab Tag 21 Nachmittag sperrt die Belagerung alles ausser bl_ (modul "sperre"), bis Akt 3 sie aufhebt
    for f in ("megan", "elsa"):
        z = spiel(tag=20)
        z["werte"]["vertrauen." + f] = 3
        x = ziehen(z, d)
        pruefen(x and x["personen"]["selfie"]["frau"] == f, "%s: Vertrauen 3 reicht, auch an Tag 20 (%s)" % (f, x and x["id"]))
        z = spiel(tag=22)
        z["werte"]["vertrauen." + f] = 3
        pruefen(ziehen(z, d) is None, "%s: in der Belagerung kein Selfie" % f)

    # Riegel aus der Geschichte: Jana erst nach ihrer Nacht
    z = spiel()
    z["werte"]["vertrauen.jana"] = 5
    for _ in range(4):
        x = ziehen(z, d)
        pruefen(not (x and x["id"].startswith("sf_jana")), "Jana: ohne jana_abend kein Selfie")

    # Nachschlag nach "Leave it on read"
    z = spiel(phase="nacht")
    z["flags"].append("sfn_rosi_4")
    x = ziehen(z, d)
    pruefen(x and x["id"] == "sfn_rosi_4", "Rosi: Nachschlag kommt in der naechsten Phase (%s)" % (x and x["id"]))
    alva = next(e for e in d["events"] if e["id"] == "sf_alva_3_bar")
    leave = [o for o in alva["optionen"] if o["text"] == "Leaves it on read."]
    pruefen(leave and leave[0]["folgen"] == [{"flag": "sfn_alva_3"}], "Leave it on read setzt den Nachschlag")

    pruefen(stimme.ohne_emoji("[laugh] THE BAY IS GLOWING 🌊✨") == "[laugh] THE BAY IS GLOWING", "Stimme ohne Emojis")
    print("OK")


if __name__ == "__main__":
    main()
