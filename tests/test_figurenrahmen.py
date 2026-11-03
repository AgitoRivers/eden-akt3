# -*- coding: utf-8 -*-
"""Figurenrahmen (Duc 31.10.2026): Bei Rosi schaffen die Werte den Kontext, das Modell entscheidet nichts. Ohne Modell.

  python tests\\test_figurenrahmen.py
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(HERE)
sys.path.insert(0, EDEN)
from kern import chronik, figurenrahmen as R, gesten, llm, reaktion, zustand  # noqa: E402

MODUL = json.load(open(os.path.join(EDEN, "module", "eden_rise", "modul.json"), encoding="utf-8"))
ROSI = R.figur(MODUL, "rosi")


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def neues_spiel(tag=9):
    z = zustand.neu(MODUL, "entspannt")
    zustand.persona_setzen(z, MODUL, MODUL["personas"][0])
    z["tag"], z["phase"], z["status"], z["heute"] = tag, "abend", "wahl", []
    return z


def frei(pid="rosi"):
    return {"id": "frei_%s_t9_abend" % pid, "ausgangslage": "%s is here." % pid, "ort": "workshop"}


def daten():
    pruefen(R.gilt(MODUL, "rosi") and not R.gilt(MODUL, "holm"), "Holm hat keinen Rahmen")
    alle = [t for pid in R.daten(MODUL)["figuren"] for f in [R.figur(MODUL, pid)] for t in f["momente"] + f["abende"] + f["themen"]]
    ids = [t["id"] for t in alle]
    pruefen(len(ids) == len(set(ids)), "Themen-Kennungen eindeutig")
    romanzen = [p for p in R.daten(MODUL)["figuren"] if MODUL["personen"][p].get("romanzierbar")]
    pruefen(len(romanzen) == 7, "alle sieben Romanzen haben einen Rahmen")
    for pid in romanzen:
        for m in ("kiss", "naehe", "naehe_weit", "intimate", "confession"):
            pruefen(any(t["moment"] == m for t in R.figur(MODUL, pid)["momente"]), "%s: Moment hat einen Einstieg: %s" % (pid, m))
        pruefen(len(R.figur(MODUL, pid)["abende"]) >= 3, "%s: Abende bauen aufeinander auf" % pid)
    chiara = " ".join(t["einstieg"] for t in R.figur(MODUL, "chiara")["themen"] + R.figur(MODUL, "chiara")["abende"] + R.figur(MODUL, "chiara")["momente"])
    pruefen(not re.search(r"\bten\b", chiara, re.I), "Chiara sagt in festen Zeilen nie ten")
    pruefen(all(t.get("wenn", {}).get("flag") or t.get("wenn", {}).get("v", 0) >= 0 for t in R.figur(MODUL, "chiara")["themen"]), "Chiara: Bedingungen lesbar")
    pruefung = [t["id"] for t in R.figur(MODUL, "chiara")["themen"] if re.search(r"exam|yachtmaster", t["einstieg"], re.I)
                and t.get("wenn", {}).get("flag") != "rm_c1"]
    pruefen(not pruefung, "Chiaras Pruefung kommt erst nach ihrem Gestaendnis")
    for t in alle:
        pruefen(t["einstieg"].rstrip().endswith("?"), "%s endet mit einer klaren Frage" % t["id"])
        pruefen(len(re.findall(r"[.!?]+(\s|$)", t["einstieg"])) <= 5, "%s ist kurz" % t["id"])
        pruefen(t.get("regie"), "%s hat eine Regie" % t["id"])
    pruefen(not any("Captain" in t["einstieg"] for t in ROSI["momente"] + ROSI["abende"] + ROSI["themen"]), "Rosi setzt die Anrede nicht fest")
    technik = [t["id"] for t in ROSI["themen"] if re.search(r"\b(relay|inverter|sensor|wiring)\b", t["einstieg"], re.I)]
    pruefen(not technik, "kein Thema dreht sich um Reparaturen")
    for m in ("kiss", "naehe", "naehe_weit", "intimate", "confession"):
        pruefen(any(t["moment"] == m for t in ROSI["momente"]), "Moment hat einen Einstieg: " + m)


def reaktion_zaehlt_nicht():
    z = neues_spiel()
    sz = {"figuren": ["rosi"], "auftraege": {"rosi": {}}}
    aufrufe = []
    alt = llm.json_chat
    llm.json_chat = lambda *a, **k: (aufrufe.append(1), ({"rosi": "desire"}, None))[1]
    try:
        pruefen(reaktion.urteilen(z, MODUL, sz, "You are amazing.", "", gesten.kurz) == {} and not aufrufe,
                "allein mit Rosi urteilt kein Modell")
    finally:
        llm.json_chat = alt
    vorher = dict(z["werte"])
    reaktion.anwenden(z, MODUL, sz, "You are amazing.", {"rosi": "desire"}, gesten.kurz)
    pruefen(z["werte"] == vorher, "ein Urteil aendert Rosis Werte nicht")


def feste_punkte():
    z = neues_spiel()
    v0, b0 = zustand.punkte(z, "vertrauen.rosi"), zustand.punkte(z, "begehren.rosi")
    sz = {"def": frei(), "figuren": ["rosi"], "zug": 0}
    R.szene_auswerten(z, MODUL, sz)
    pruefen(zustand.punkte(z, "vertrauen.rosi") == v0, "ohne Zug keine Punkte")
    sz["zug"] = 1
    R.szene_auswerten(z, MODUL, sz)
    pruefen(zustand.punkte(z, "vertrauen.rosi") == v0 + 4, "ein Zug in freier Szene gibt fest Vertrauen")
    pruefen(zustand.punkte(z, "begehren.rosi") > b0, "und fest Begehren")
    v1 = zustand.punkte(z, "vertrauen.rosi")
    R.szene_auswerten(z, MODUL, {"def": dict(frei(), id="date_rosi"), "figuren": ["rosi"], "zug": 3})
    pruefen(zustand.punkte(z, "vertrauen.rosi") == v1, "Abende zaehlen ueber ihre feste Folge, nicht doppelt")
    R.szene_auswerten(z, MODUL, {"def": dict(frei(), id="ev_x"), "figuren": ["rosi"], "zug": 3})
    pruefen(zustand.punkte(z, "vertrauen.rosi") == v1, "gescriptete Szenen bleiben, wie sie sind")


def themen():
    z = neues_spiel()
    gefunden = []
    for _ in range(4):
        t = R.thema_fuer(z, MODUL, frei(), ["rosi"])
        R.thema_buchen(z, MODUL, "rosi", t)
        gefunden.append(t["id"])
    pruefen(len(set(gefunden)) == 4, "vier Szenen, vier Themen")
    pruefen(gefunden[0] == ROSI["themen"][0]["id"], "Reihenfolge wie in den Daten")
    pruefen(R.thema_fuer(z, MODUL, frei("holm"), ["holm"]) is None, "keine Themen fuer Holm")
    pruefen(R.thema_fuer(z, MODUL, frei(), ["rosi", "lola"]) is None, "keine Themen in Gruppenszenen")
    pruefen(R.thema_fuer(z, MODUL, dict(frei(), id="ev_x"), ["rosi"]) is None, "keine Themen in Event-Szenen")
    ids = {t["id"] for t in ROSI["themen"] if not R.bedingung(z, "rosi", t.get("wenn"))}
    pruefen("t_ohne_grund" in ids and "t_plan" in ids, "spaete Themen sind anfangs gesperrt")
    z2 = neues_spiel()
    z2["flags"].append("rosi_zusammen")
    pruefen("Captain" in R.fuellen(z2, MODUL, "rosi", "{anrede}") and "Officer" in R.fuellen(z, MODUL, "rosi", "{anrede}"),
            "Anrede folgt der Leiter")


def abende():
    z = neues_spiel()
    d = dict(frei(), id="date_rosi")
    folge = []
    for _ in range(len(ROSI["abende"]) + 2):
        t = R.thema_fuer(z, MODUL, d, ["rosi"])
        R.thema_buchen(z, MODUL, "rosi", t)
        folge.append(t["id"])
    pruefen(folge[:3] == ["a_erster", "a_regeln", "a_sie_waehlt"], "Abende bauen aufeinander auf")
    pruefen(folge[-2:] == ["a_erster", "a_regeln"], "danach kommt das am laengsten zurueckliegende")
    pruefen(any("first evening" in x for x in R.faktenblatt(z, MODUL, "rosi")), "der Abend steht im Faktenblatt")


def momente():
    z = neues_spiel()
    chronik.eintragen(z, MODUL, "moment", "Duc and Rosi kissed.", wer=["rosi"], moment="kiss", dabei=["rosi"])
    pruefen(R.thema_fuer(z, MODUL, frei(), ["rosi"])["art"] == "thema", "am selben Tag noch keine Moment-Zeile")
    z["tag"] += 1
    t = R.thema_fuer(z, MODUL, frei(), ["rosi"])
    pruefen(t["id"] == "m_kuss", "am naechsten Tag kommt die Kuss-Zeile")
    R.thema_buchen(z, MODUL, "rosi", t)
    pruefen(R.thema_fuer(z, MODUL, frei(), ["rosi"])["art"] == "thema", "nur einmal")
    pruefen(not chronik.moment_offen(z, "rosi", ["kiss"]), "das Echo am Fruehstueck kommt danach nicht mehr")
    chronik.eintragen(z, MODUL, "moment", "Duc and Rosi slept together.", wer=["rosi"], moment="intimate", dabei=["rosi"])
    chronik.eintragen(z, MODUL, "moment", "Duc and Rosi kissed.", wer=["rosi"], moment="kiss", dabei=["rosi"])
    z["tag"] += 1
    t = R.thema_fuer(z, MODUL, dict(frei(), id="date_rosi"), ["rosi"])
    pruefen(t["id"] == "m_nacht1", "der staerkste Moment geht vor, auch am Abend")
    R.thema_buchen(z, MODUL, "rosi", t)
    pruefen(R.thema_fuer(z, MODUL, frei(), ["rosi"])["art"] == "thema", "ein Einstieg nimmt alle offenen Momente mit")
    chronik.eintragen(z, MODUL, "moment", "Duc and Rosi slept together.", wer=["rosi"], moment="intimate", dabei=["rosi"])
    z["tag"] += 1
    pruefen(R.thema_fuer(z, MODUL, frei(), ["rosi"])["id"] == "m_nacht2", "die zweite Nacht hat eine eigene Zeile")
    z3 = neues_spiel()
    chronik.eintragen(z3, MODUL, "moment", "Duc and Rosi kissed.", wer=["rosi"], moment="kiss", dabei=["rosi"])
    z3["tag"] += R.FRISCH_TAGE + 1
    pruefen(R.thema_fuer(z3, MODUL, frei(), ["rosi"])["art"] == "thema", "ein alter Moment kommt nicht Wochen spaeter")


def faktenblatt():
    z = neues_spiel()
    z["gedaechtnis"]["rosi"] = ["Day 2: She successfully charmed him and invented a story."]
    z["flags"] += ["rm_r1"]
    chronik.eintragen(z, MODUL, "moment", "Duc and Rosi kissed.", wer=["rosi"], moment="kiss", dabei=["rosi"])
    chronik.eintragen(z, MODUL, "zeit", "Modelltext", wer=["rosi"], dabei=["rosi"])
    teile = "\n".join(R.prompt_teile(z, MODUL, "rosi"))
    pruefen("relay" in teile and "kissed" in teile, "Leiter und Chronik stehen im Blatt")
    pruefen("charmed" not in teile and "Modelltext" not in teile, "keine Modell-Erinnerung im Blatt")
    pruefen("never Captain" in teile, "vor der Leiter nie Captain")
    pruefen("They have been close" in teile, "Haltung folgt dem Stand")
    pruefen("charmed" not in "\n".join(R.erinnerung(z, MODUL, "rosi")), "auch das Handy bekommt das Blatt")
    z["gedaechtnis"]["holm"] = ["Day 2: Holm text."]
    pruefen(R.erinnerung(z, MODUL, "holm") == ["Day 2: Holm text."], "bei Holm bleibt die Erinnerung")
    z["flags"] += ["rm_r4", "rosi_zusammen"]
    teile = "\n".join(R.prompt_teile(z, MODUL, "rosi"))
    pruefen("Alone she calls him Captain" in teile and "stays covered" not in teile, "nach der Leiter gilt das Neue")


def vorschlaege():
    z = neues_spiel()
    z["werte"]["begehren.rosi"] = 1
    gesehen = {R.vorschlag(z, MODUL, "rosi", False) for _ in range(12)}
    pruefen(all(k != "romantik" for _, k in gesehen), "ohne Begehren kein romantischer Vorschlag")
    pruefen(len(gesehen) > 3, "Vorschlaege wechseln")
    pruefen(R.vorschlag(z, MODUL, "rosi", True)[1] == "romantik", "nach Naehe bleibt sie dabei")
    sz = {"figuren": ["rosi"], "gesten_genutzt": [], "def": {"ort": "workshop"}, "log": []}
    z["szene"] = sz
    alt = llm.json_chat
    llm.json_chat = lambda *a, **k: (_ for _ in ()).throw(AssertionError("Modell gefragt"))
    try:
        text, kat = gesten.zeit_vorschlag(z, MODUL, "rosi", "prompt")
    finally:
        llm.json_chat = alt
    pruefen(text.startswith('"') and sz["zeit_angebot"]["kategorie"] == kat, "Zeit zusammen kommt ohne Modell aus")


def keine_zusammenfassung():
    from kern import szene
    z = neues_spiel()
    z["szene"] = {"def": dict(frei(), titel="Time with Rosi"), "figuren": ["rosi"], "auftraege": {"rosi": {}}, "log": [], "zug": 1}
    gefragt = []
    alt = llm.chat
    llm.chat = lambda system, *a, **k: (gefragt.append(system), ("Modelltext", None))[1]
    try:
        meldung, _ = szene.beenden(z, MODUL)
    finally:
        llm.chat = alt
    pruefen(meldung["kurz"] == "" and not any("summarise" in s for s in gefragt), "freie Szene mit Rahmen: keine Zusammenfassung vom Modell")
    pruefen(z["heute"][-1]["kurz"] == "", "auch der Kalender bleibt ohne Modelltext")


def start_chips():
    z = neues_spiel()
    for k, a in (("vertrauen", "vertrauen.rosi"), ("begehren", "begehren.rosi")):
        v, g = zustand.punkte(z, "vertrauen.rosi"), zustand.punkte(z, "begehren.rosi")
        R.chip_buchen(z, MODUL, "rosi", {"text": "x", "achse": k})
        pruefen(zustand.punkte(z, a) > (v if k == "vertrauen" else g), "Chip %s wirkt" % k)
    v, g = zustand.punkte(z, "vertrauen.rosi"), zustand.punkte(z, "begehren.rosi")
    R.chip_buchen(z, MODUL, "rosi", {"text": "x", "achse": "beide"})
    pruefen(zustand.punkte(z, "vertrauen.rosi") == v + 1 and zustand.punkte(z, "begehren.rosi") > g, "Chip beide wirkt etwas auf beides")
    v = zustand.punkte(z, "vertrauen.rosi")
    R.szene_auswerten(z, MODUL, {"def": frei(), "figuren": ["rosi"], "zug": 1, "chip_start": True})
    pruefen(zustand.punkte(z, "vertrauen.rosi") == v + 2, "mit Chips zaehlt die Zeit zusammen weniger")
    for f in R.daten(MODUL)["figuren"].values():
        for t in f["momente"] + f["abende"] + f["themen"]:
            if t.get("chips"):
                pruefen(sorted(c["achse"] for c in t["chips"]) == ["begehren", "beide", "vertrauen"], "%s: je ein Chip pro Richtung" % t["id"])
                pruefen(all(c["text"] and not re.search(r"\+\d|\b\d+ points?\b|\b(trust|desire)\b", c["text"], re.I) for c in t["chips"]), "%s: Chips ohne Zahlen" % t["id"])


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    daten()
    reaktion_zaehlt_nicht()
    feste_punkte()
    themen()
    abende()
    momente()
    faktenblatt()
    vorschlaege()
    keine_zusammenfassung()
    start_chips()
    from kern import szene
    t = '"Go on." *He\'s actually listening.* "Well?"'
    pruefen("listening" not in szene.ohne_leeren_gedanken(t) and '"Well?"' in szene.ohne_leeren_gedanken(t), "der leere Gedanke faellt weg, die Rede bleibt")
    pruefen("*He fears the dark.*" in szene.ohne_leeren_gedanken('*He fears the dark.*'), "ein echter Gedanke bleibt")
    print("Figurenrahmen: alles gruen")


if __name__ == "__main__":
    main()
