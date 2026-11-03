# -*- coding: utf-8 -*-
"""Einstiege und Spuren von Naehe (Live-Spieltest 31.10.2026). Laeuft ohne Modell, Stimme und Netz.

  python tests\\test_einstiege_naehe.py
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(HERE)
sys.path.insert(0, EDEN)
from kern import chronik, gesten, szene, zustand  # noqa: E402

MODUL = json.load(open(os.path.join(EDEN, "module", "eden_rise", "modul.json"), encoding="utf-8"))


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def neues_spiel(tag=3):
    z = zustand.neu(MODUL, "entspannt")
    zustand.persona_setzen(z, MODUL, MODUL["personas"][0])
    z["tag"], z["phase"], z["status"] = tag, "abend", "wahl"
    z["heute"] = []
    return z


def szene_von(pid, ausgangslage="Rosi is at the workbench."):
    return {"def": {"ausgangslage": ausgangslage, "ort": next(iter(MODUL["raeume"]))}, "log": [], "figuren": [pid]}


def einstiege():
    t = 'Rosi leans on the bench. She waits. "You\'re late, Officer. The fish pie is cold."'
    pruefen(szene.einstieg_von(t) == 'Rosi leans on the bench. "You\'re late, Officer."', "Einstieg: Handlung und Rede, je erster Satz")
    pruefen(szene.einstieg_von('"Morning. Coffee?"') == '"Morning."', "Einstieg ohne Handlung")
    sz = szene_von("rosi")
    pruefen(szene.erste_zeile(sz, "rosi"), "noch keine Zeile: erste Zeile")
    sz["log"].append({"art": "figur", "wer": "rosi", "text": t})
    pruefen(not szene.erste_zeile(sz, "rosi"), "danach nicht mehr")
    pruefen(not szene.erste_zeile(sz, szene.ERZAEHLER), "Erzaehler zaehlt nicht")
    z = neues_spiel()
    for i in range(6):
        szene.einstiege_merken(z, {"log": [{"art": "figur", "wer": "rosi", "text": '"Zeile %d."' % i},
                                           {"art": "figur", "wer": "rosi", "text": '"Zweite Zeile."'}]})
    pruefen(z["einstiege"]["rosi"] == ['"Zeile %d."' % i for i in range(2, 6)], "merkt nur die ersten Zeilen der letzten 4 Szenen")
    h = szene.einstieg_hinweis(z, "rosi")
    pruefen('"Zeile 5."' in h and "late" in h, "Hinweis nennt die Einstiege und den Satz")
    pruefen("late" not in szene.einstieg_hinweis(neues_spiel(), "holm"), "Holm darf den Satz")
    pruefen(szene.einstieg_hinweis(neues_spiel(), "rosi").count("opened like this") == 0, "ohne Vorgeschichte keine Liste")


def zu_spaet():
    sz = szene_von("rosi")
    pruefen(szene.eroeffnet_zu_spaet(sz, "rosi", '"You\'re late, Officer."'), "Rosi: wird erkannt")
    pruefen(szene.eroeffnet_zu_spaet(sz, "chiara", '"You are late for the briefing."'), "Langform wird erkannt")
    pruefen(szene.eroeffnet_zu_spaet(sz, "lola", "\"You’re late, boss.\""), "typografisches Apostroph wird erkannt")
    pruefen(not szene.eroeffnet_zu_spaet(sz, "holm", '"Frankfurt. You\'re late."'), "Holm darf")
    pruefen(not szene.eroeffnet_zu_spaet(sz, "rosi", '"The chocolate is late this year."'), "anderes late ist frei")
    pruefen(not szene.eroeffnet_zu_spaet(szene_von("rosi", "Duc is late for dinner."), "rosi", '"You\'re late."'), "stimmt laut Szene: darf")
    pruefen(szene.ohne_zu_spaet('She looks up. "You\'re late, Officer. The pie is cold."') == 'She looks up. "The pie is cold."', "Satz faellt weg, Rest bleibt")
    pruefen(szene.ohne_zu_spaet('She looks up. "You\'re late."') == "She looks up.", "leere Anfuehrung faellt mit weg")
    pruefen(szene.ohne_zu_spaet('"You\'re late."') == '"You\'re late."', "nie eine leere Antwort")


def antwort_schreibt_neu():
    sz = dict(szene_von("rosi"), zug=0, auftraege={}, figuren=["rosi"])
    sz["def"]["max_zuege"] = 10
    aufrufe = []
    alt = (szene.figur_prompt, szene.richter, szene.mitschrift, szene.llm.chat)

    def chat(system, user, sampler=None, max_tokens=0):
        aufrufe.append(user)
        return antworten.pop(0), None
    szene.figur_prompt = lambda *a: "sys"
    szene.richter = lambda *a: ([], "neutral")
    szene.mitschrift = lambda *a: ""
    szene.llm.chat = chat
    try:
        antworten = ['"You\'re late, Officer."', '"Hand me the wrench."']
        z = neues_spiel()
        text, verworfen, _, _ = szene.antwort(z, MODUL, sz, "rosi", "(the scene begins)")
        pruefen(text == '"Hand me the wrench."' and verworfen == [["opens_late"]], "erste Fassung wird neu geschrieben")
        pruefen("he is not" in aufrufe[1], "das Neuschreiben nennt den Grund")
        antworten = ['"You\'re late, Officer. Sit."', '"You\'re late again. Sit."']
        text = szene.antwort(z, MODUL, sz, "rosi", "(the scene begins)")[0]
        pruefen("late" not in text and "Sit." in text, "zweimal: der Satz wird gestrichen")
        sz["log"].append({"art": "figur", "wer": "rosi", "text": '"Hello."'})
        antworten = ['"You\'re late with the logs."']
        pruefen("late" in szene.antwort(z, MODUL, sz, "rosi", "x")[0], "mitten in der Szene bleibt der Satz frei")
    finally:
        szene.figur_prompt, szene.richter, szene.mitschrift, szene.llm.chat = alt


def naehe():
    pruefen(gesten.naehe_kennung(MODUL, "Act: Kissing") == "naehe", "Stufe 3: schwach")
    pruefen(gesten.naehe_kennung(MODUL, "Act: Fingering") == "naehe_weit", "Stufe 4: weiter")
    pruefen(gesten.naehe_kennung(MODUL, "Act: Her Climax") == "naehe_weit", "Stufe 5 ohne Sex: weiter")
    pruefen(gesten.naehe_kennung(MODUL, "Position: Cowgirl") == "intimate", "Stellung: slept together")
    pruefen(gesten.naehe_kennung(MODUL, "Act: Anal") == "intimate", "Anal: slept together")
    for k in ("naehe", "naehe_weit"):
        pruefen(k not in chronik.EIFERSUCHT, "%s loest keine Eifersucht aus" % k)
        pruefen(chronik.MOMENTE[k][1] < 2, "%s wird nicht weitererzaehlt" % k)
        pruefen("slept" not in chronik.MOMENTE[k][0], "%s behauptet keinen Sex" % k)
    z = neues_spiel()
    e = chronik.naehe_eintragen(z, MODUL, "rosi", "naehe")
    pruefen(e["weiss"] == ["rosi"], "nur sie weiss davon")
    pruefen(chronik.naehe_eintragen(z, MODUL, "rosi", "naehe") is None, "gleich stark am selben Tag: kein zweiter Eintrag")
    pruefen(chronik.naehe_eintragen(z, MODUL, "rosi", "naehe_weit") is not None, "staerker: neuer Eintrag")
    pruefen(chronik.naehe_eintragen(z, MODUL, "rosi", "naehe") is None, "schwaecher: keiner")
    pruefen(chronik.naehe_eintragen(z, MODUL, "lea", "naehe") is not None, "andere Figur: eigener Eintrag")
    z["tag"] += 1
    pruefen(chronik.naehe_eintragen(z, MODUL, "rosi", "naehe") is not None, "neuer Tag: neuer Eintrag")
    pruefen(chronik.hat_naehe(z, "rosi") and not chronik.hat_naehe(z, "megan"), "hat_naehe")
    mit_klatsch = neues_spiel()
    chronik.naehe_eintragen(mit_klatsch, MODUL, "lola", "naehe_weit")
    class Immer:
        def random(self):
            return 0.0
    pruefen(chronik.klatsch(mit_klatsch, MODUL, ["lola", "rosi"], rng=Immer()) == [], "Naehe wird nicht zu Klatsch")


def rueckbezug():
    z = neues_spiel()
    nacht = chronik.naehe_eintragen(z, MODUL, "rosi", "naehe_weit")
    chronik.eintragen(z, MODUL, "geschenk", "Duc gave Rosi a wrench.", wer=["rosi"], dabei=["rosi"])
    pruefen(chronik.rueckbezug(z, "rosi", True) is nacht, "allein: das Geschenk verdraengt die Nacht nicht")
    pruefen(chronik.rueckbezug(z, "rosi")["art"] == "geschenk", "vor anderen: wie bisher der letzte Eintrag")
    nacht["aufgegriffen"] = True
    pruefen(chronik.rueckbezug(z, "rosi", True)["art"] == "geschenk", "aufgegriffen: zurueck zum letzten Eintrag")
    pruefen(chronik.rueckbezug(z, "lea", True) is None, "ohne Eintrag nichts")


def kueche():
    z = neues_spiel()
    pruefen("Lola cooks" in szene.kueche_regel(z) and "Chiara runs" in szene.kueche_regel(z), "Lola kocht, Chiara serviert")
    z["flags"] = list(z.get("flags", [])) + ["gefeuert_chiara"]
    pruefen("Chiara" not in szene.kueche_regel(z), "Chiara gefeuert: faellt aus der Regel")
    z["flags"].append("gefeuert_lola")
    pruefen(szene.kueche_regel(z) == "", "Lola gefeuert: keine Regel")


if __name__ == "__main__":
    kueche()
    einstiege()
    zu_spaet()
    antwort_schreibt_neu()
    naehe()
    rueckbezug()
    print("Alle Pruefungen bestanden.")
