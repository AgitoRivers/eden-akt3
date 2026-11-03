# -*- coding: utf-8 -*-
"""Journal: Kevins Seite und die Flut-Nacht als Nebenauftraege, optionale Umweg-Schritte in der Grotte, Frist (Duc 29.10.2026,
Quest-Designer-Durchgang). Prueft die Daten (auftraege.json) und kern/auftraege.journal.

  python tests\\test_journal_nebenquests.py
"""
import json, os, sys

EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, EDEN)
from kern import auftraege, zustand  # noqa: E402

MOD = os.path.join(EDEN, "module", "eden_rise")
MODUL = json.load(open(os.path.join(MOD, "modul.json"), encoding="utf-8"))


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def spiel(tag, flags=()):
    z = zustand.neu(MODUL, "entspannt")
    zustand.persona_setzen(z, MODUL, MODUL["personas"][0])
    z["tag"], z["phase"] = tag, "tag"
    z["flags"] += list(flags)
    return z


def j(z, aid):
    return next((a for a in auftraege.journal(z, MODUL, MOD, lambda p: None) if a["id"] == aid), None)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    d = auftraege.daten(MOD)
    pruefen(len(d["auftraege"]) == 8 and d["auftraege"]["kevin"]["neben"] and d["auftraege"]["grotte_flut"]["neben"],
            "8 Auftraege (mit Red Trio), Kevin und die Flut-Nacht sind Nebenauftraege")
    pruefen(not d["auftraege"]["grotte"].get("neben"), "die Grotte bleibt ein Hauptauftrag")

    # Kevin (Tag 12-14)
    pruefen(j(spiel(11), "kevin") is None, "vor Tag 12 kein Eintrag")
    z = spiel(12, ["kevin_jagd"])
    k = j(z, "kevin")
    pruefen(k and k["status"] == "aktiv" and k["neben"] and k["von"] == "lea", "Tag 12: Kevins Seite steht als offener Nebenauftrag (von Lea)")
    pruefen(k["naechster"] == "Climb out onto the rooftops and chase Kevin." and len(k["schritte"]) == 3, "naechster Schritt: die Dacher")
    z["flags"].append("kv_tauben")
    pruefen(j(z, "kevin")["naechster"] == "Get up the bell tower to his nest.", "nach den Tauben: der Glockenturm")
    z["flags"] += ["kv_kevin", "kevin_fertig", "kevin_stift"]
    k = j(z, "kevin")
    pruefen(k["status"] == "fertig" and k["grau"][0]["entschieden"] == "You kept Megan's pen for yourself.", "fertig, graue Wahl (Stift) steht da")
    k2 = j(spiel(13, ["kevin_jagd", "kevin_fertig", "kevin_fair"]), "kevin")
    pruefen(k2["grau"][0]["entschieden"] == "You put everything back in the nest.", "graue Wahl (fair) steht da")
    v = j(spiel(15, ["kevin_jagd"]), "kevin")
    pruefen(v["status"] == "verpasst" and v["naechster"] is None, "Tag 15 ohne Seite: verpasst")
    pruefen(j(spiel(14, ["kevin_jagd"]), "kevin")["status"] == "aktiv", "Tag 14: noch offen")
    pruefen(auftraege.journal(spiel(15, ["kevin_jagd", "kloster_angenommen"]), MODUL, MOD, lambda p: None)[-1]["status"] == "verpasst",
            "Verpasstes steht unten bei den Erledigten")

    # Grotte: optionale Umweg-Schritte erst sichtbar, wenn der Abzweig bekannt ist; nie der naechste Schritt
    z = spiel(11, ["grotte_offen"])
    g = j(z, "grotte")
    pruefen(len(g["schritte"]) == 3 and not any(s["optional"] for s in g["schritte"]), "Grotte vor dem Abstieg: drei Schritte, keine Umwege (kein Spoiler)")
    z["flags"].append("gr_1_ratten")
    g = j(z, "grotte")
    opt = [s for s in g["schritte"] if s["optional"]]
    pruefen(len(opt) == 1 and "drowned beach" in opt[0]["text"], "nach den Ratten: der Ruf vom Strand erscheint als optional")
    pruefen(g["naechster"] == "Go down into the grotto at low tide.", "optional ist nie der naechste Schritt")
    z["flags"].append("gr_4_schmuggler")
    pruefen(len([s for s in j(z, "grotte")["schritte"] if s["optional"]]) == 2, "nach der Halle: auch der Taucher")
    z["flags"] += ["gr_gennaro_gefunden", "gr_bastien_befreit", "gr_matteu_wahrheit"]
    g = j(z, "grotte")
    pruefen(all(s["erledigt"] for s in g["schritte"] if s["optional"]), "beide Umwege abgehakt, wenn sie gegangen wurden")
    pruefen(g["naechster"] == "Get Gennaro past the man who comes with the tide.", "naechster Schritt bleibt der Hauptweg")
    g = j(spiel(11, ["grotte_offen", "gr_1_ratten", "gr_chloe_ignoriert"]), "grotte")
    pruefen([s["erledigt"] for s in g["schritte"] if s["optional"]] == [False], "Strand ignoriert: bleibt offen, blockiert nichts")

    # Flut-Nacht: erscheint, sobald die Grotte fertig ist
    pruefen(j(spiel(12, ["grotte_offen"]), "grotte_flut") is None, "ohne grotte_fertig keine Flut-Nacht im Journal")
    z = spiel(12, ["grotte_offen", "grotte_fertig"])
    f = j(z, "grotte_flut")
    pruefen(f and f["status"] == "aktiv" and f["neben"], "nach der Grotte: High Tide steht als Nebenauftrag da")
    pruefen("Ligeia" not in json.dumps(f) and "siren" not in json.dumps(f).lower() and "woman" not in json.dumps(f).lower(), "kein Spoiler im Text (keine Sirene, keine Frau)")
    z["flags"] += ["fn_1_ratten", "fn_gegangen"]
    f = j(z, "grotte_flut")
    pruefen(f["status"] == "aktiv" and f["naechster"] == "Listen to the voice in the black pool." and f["grau"][0]["entschieden"] == "You backed away, for tonight.",
            "Rueckzug: bleibt offen (\"another night\")")
    z["flags"] += ["fn_geredet", "sirene_fertig"]
    pruefen(j(z, "grotte_flut")["status"] == "fertig" and j(z, "grotte_flut")["grau"][0]["entschieden"] == "You put the weapon away and talked to the woman with the fish tail.",
            "geredet und fertig: Done")
    # Ort, Tageszeiten, Frist (Duc 29.10.2026): letzter Tag = bis_tag - 1; ohne Frist None
    k = j(spiel(12, ["kevin_jagd"]), "kevin")
    pruefen(k["ort"] == "Kevin's Rooftops" and k["zeiten"] == ["tag", "nachmittag"] and k["frist"] == 14, "Kevin: Ort, Mittag/Nachmittag, letzter Tag 14")
    f = j(spiel(12, ["grotte_offen", "grotte_fertig"]), "grotte_flut")
    pruefen(f["zeiten"] == ["abend"] and f["frist"] == 21, "High Tide: nur abends, letzter Tag 21 (der Ort schliesst mit Tag 22)")
    pruefen(j(spiel(22, ["grotte_offen", "grotte_fertig"]), "grotte_flut")["status"] == "verpasst", "High Tide ab Tag 22: verpasst")
    pruefen(j(spiel(12, ["grotte_offen"]), "grotte")["frist"] is None, "Grotte: keine Frist")
    print("\nalle Journal-Tests bestanden")


if __name__ == "__main__":
    main()
