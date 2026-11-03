# -*- coding: utf-8 -*-
"""Phone chat (24.10.2026): driver, tone consequences with guard rails, answer chips, callback, referee, no action cost.

Runs without model, voice and network: the model calls are replaced by fixed answers.

  python tests\\test_handy.py
"""
import copy, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(HERE)
sys.path.insert(0, EDEN)
from kern import chronik, handy, llm, plan, zustand  # noqa: E402

MODUL = json.load(open(os.path.join(EDEN, "module", "eden_rise", "modul.json"), encoding="utf-8"))
BOGEN = lambda pid: "she is %s" % pid
STATE = {"ton": "warm", "pruef": [], "chat": [], "calls": []}


def fake_json_chat(system, user, gram, max_tokens=0, sampler=None):
    STATE["calls"].append(gram[:60])
    if "contradicts_facts" in gram:
        v = STATE["pruef"].pop(0) if STATE["pruef"] else []
        return {"contradicts_facts": "contradicts_facts" in v, "invents_event": "invents_event" in v}, 0.0
    if "tone" in gram:
        return {"tone": STATE["ton"]}, 0.0
    if "warm" in gram:
        return {"warm": "nice work. get some sleep.", "funny": "the ghost has a name? i'll buy it a coffee.",
                "flirty": "i like it when you talk to machines. talk to me."}, 0.0
    return {}, 0.0


def fake_chat(system, user, sampler=None, max_tokens=0, grammar=None):
    STATE["chat"].append(user)
    return "ok, noted.", 0.0


llm.json_chat, llm.chat = fake_json_chat, fake_chat


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def neues_spiel(tag=2, phase="tag"):
    z = zustand.neu(MODUL, "entspannt")
    zustand.persona_setzen(z, MODUL, MODUL["personas"][0])
    z["tag"], z["phase"], z["status"] = tag, phase, "szene"
    z["heute"] = []
    return z


def faden_mit(z, pid, text="found the ghost drain."):
    f = handy.faden_von(z, pid)
    f["verlauf"].append({"wer": pid, "text": text, "tag": z["tag"], "phase": z["phase"]})
    return z["handy"].index(f)


def pkt(z, pid, achse):
    return zustand.punkte(z, "%s.%s" % (achse, pid))


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    pid = "rosi"
    dat = handy.daten(MODUL)
    pruefen(dat["max_replies"] == 3 and dat["min_progress"] == 4 and "warm" in dat["tones"],
            "Ton-Tabelle kommt aus module/eden_rise/handy.json (Zahlen + Toene)")

    # --- consequences with guard rails
    z = neues_spiel()
    i = faden_mit(z, pid)
    STATE["ton"] = "warm"
    v0 = pkt(z, pid, "vertrauen")
    handy.antworten(z, MODUL, i, "i'll fix it alone.", BOGEN)
    pruefen(pkt(z, pid, "vertrauen") == v0 + 4, "warm: +4 Vertrauen")
    handy.antworten(z, MODUL, i, "rest tonight.", BOGEN)
    pruefen(pkt(z, pid, "vertrauen") == v0 + 4, "zweiter Text am selben Tag: keine zweite Wirkung")
    ich = [v for v in z["handy"][i]["verlauf"] if v["wer"] == "duc"]
    pruefen(ich[0].get("reaktion") == "herz" and not ich[1].get("reaktion"),
            "Wirkung als Herz an Ducs Nachricht, die zweite am Tag ohne (Duc 03.11.2026)")
    pruefen(not any(v["wer"] == "system" for v in z["handy"][i]["verlauf"]), "keine Zahlen-Zeilen mehr im Chat")
    z["tag"] = 3
    handy.antworten(z, MODUL, i, "morning.", BOGEN)
    pruefen(pkt(z, pid, "vertrauen") == v0 + 8, "naechster Tag: wieder eine Wirkung")

    z = neues_spiel()
    i = faden_mit(z, pid)
    z["punkte"]["vertrauen." + pid] = 40
    z["werte"]["vertrauen." + pid] = 3
    handy.antworten(z, MODUL, i, "thanks.", BOGEN)
    pruefen(pkt(z, pid, "vertrauen") == 44 and z.get("handy_wirkung", {}).get(pid) == z["tag"],
            "Ueber Stufe 3 wirkt das Handy bis zu seinem Topf (Duc 02.11.2026)")

    z = neues_spiel()
    z["punkte"]["vertrauen." + pid] = 14
    z["werte"]["vertrauen." + pid] = 1
    i = faden_mit(z, pid)
    STATE["ton"] = "flirty"
    handy.antworten(z, MODUL, i, "you looked amazing.", BOGEN)
    pruefen(pkt(z, pid, "vertrauen") == 11, "Flirt bei niedrigem Vertrauen kostet Vertrauen (Backfire -3)")
    pruefen("far too forward" in STATE["chat"][-1], "Antwort bekommt den Backfire-Eindruck")

    z = neues_spiel(tag=1)
    i = faden_mit(z, pid)
    STATE["ton"] = "rude"
    v0 = pkt(z, pid, "vertrauen")
    handy.antworten(z, MODUL, i, "whatever.", BOGEN)
    pruefen(pkt(z, pid, "vertrauen") == v0, "Tag 1: nur Positives")
    z["tag"] = 2
    handy.antworten(z, MODUL, i, "whatever, not now.", BOGEN)
    pruefen(pkt(z, pid, "vertrauen") == v0 - 4, "ab Tag 2: grob kostet -4")

    # --- reply limit and "she is asleep / on watch"
    z = neues_spiel()
    i = faden_mit(z, pid)
    STATE["ton"] = "neutral"
    for _ in range(3):
        handy.antworten(z, MODUL, i, "ok", BOGEN)
    try:
        handy.antworten(z, MODUL, i, "one more", BOGEN)
        pruefen(False, "vierte Antwort muss gesperrt sein")
    except ValueError as e:
        pruefen("busy" in str(e), "vierte Antwort am Tag gesperrt: " + str(e))
    pruefen(handy.status(z, MODUL, pid) == "busy", "Status nach drei Antworten: busy")
    z["phase"] = "nacht"
    pruefen("on watch" in handy.gesperrt(z, MODUL, pid) or "asleep" in handy.gesperrt(z, MODUL, pid), "nachts: Wache oder Schlaf")
    z["tag"] = 3
    pruefen(handy.gesperrt(z, MODUL, pid) is None, "naechster Tag: wieder frei")

    # --- several short bubbles, like a person (Duc 03.11.2026)
    pruefen(handy._teile("hey\n\nwait\nok fine\nlast\none more") == ["hey", "wait", "ok fine last one more"],
            "Antwort in hoechstens drei Blasen")
    z = neues_spiel()
    i = faden_mit(z, pid)
    STATE["ton"] = "neutral"
    alt = fake_chat
    llm.chat = lambda *a, **k: ("omg\nthank you\nseriously", 0.0)
    handy.antworten(z, MODUL, i, "here you go", BOGEN)
    llm.chat = alt
    pruefen([v["text"] for v in z["handy"][i]["verlauf"][-3:]] == ["omg", "thank you", "seriously"], "drei Blasen von ihr")
    z["album"] = [{"art": "selfie", "wer": pid, "tag": 2, "bild": "rosi_3"}, {"art": "selfie", "wer": pid, "tag": 4, "bild": "rosi_4"}]
    pruefen(handy.profilbild(z, pid) == "/selfie/rosi_4.webp", "Profilbild = letztes Selfie")
    pruefen(handy.profilbild(z, "lea") is None, "ohne Selfie kein Profilbild")

    # --- chat never costs a phase or an action
    z = neues_spiel()
    vorher = (z["tag"], z["phase"], plan.aktionen(z))
    i = faden_mit(z, pid)
    handy.make_chips(z, MODUL, i, BOGEN)
    handy.antworten(z, MODUL, i, "ok", BOGEN)
    pruefen((z["tag"], z["phase"], plan.aktionen(z)) == vorher and "aktionen" not in z,
            "Chat und Chips kosten nie Phase oder Aktion")

    # --- chips
    z = neues_spiel()
    z["punkte"]["vertrauen." + pid] = 14
    z["werte"]["vertrauen." + pid] = 1
    i = faden_mit(z, pid)
    handy.make_chips(z, MODUL, i, BOGEN)
    ans = handy.chips_ansicht(z, MODUL, z["handy"][i])
    pruefen([c["ton"] for c in ans] == ["warm", "funny", "flirty"], "drei Chips: warm, funny, flirty")
    pruefen(ans[2]["riskant"] and not ans[0]["riskant"], "Flirt-Chip ist bei niedrigem Vertrauen als riskant markiert")
    pruefen(ans[0]["etikett"] == "Trust ↑", "Etikett kommt aus der Ton-Tabelle")
    STATE["calls"].clear()
    handy.antworten(z, MODUL, i, ans[0]["text"], BOGEN, ton="warm")
    pruefen(not any("tone" in c for c in STATE["calls"]), "Chip unveraendert gesendet: keine Ton-Erkennung")
    pruefen(z["handy"][i]["chips"] == [], "Chips verschwinden nach dem Senden")

    # --- driver: she texts only after progress with her
    z = neues_spiel()
    handy.random.random = lambda: 0.0
    szene = {"titel": "Test"}
    pruefen(handy.nach_szene(z, MODUL, szene, ["chiara"], BOGEN) == [], "ohne Fortschritt keine Nachricht (auch kein Sockel)")
    zustand.punkte_add(z, MODUL, "begehren." + pid, 4)
    neu = handy.nach_szene(z, MODUL, szene, ["chiara"], BOGEN)
    pruefen(pid in neu, "nach +4 Punkten schreibt sie")
    pruefen(handy.nach_szene(z, MODUL, szene, ["chiara"], BOGEN).count(pid) == 0, "danach wieder still bis zum naechsten Fortschritt")
    zustand.punkte_add(z, MODUL, "vertrauen." + pid, 3)
    pruefen(pid not in handy.nach_szene(z, MODUL, szene, ["chiara"], BOGEN), "+3 reichen nicht (Schwelle 4)")
    zustand.punkte_add(z, MODUL, "vertrauen." + pid, 2)
    pruefen(pid in handy.nach_szene(z, MODUL, szene, ["chiara"], BOGEN), "+5 seit dem letzten Text reichen")
    pruefen(pid not in handy.nach_szene(z, MODUL, szene, [pid], BOGEN), "wer in der Szene ist, schreibt nicht")
    ein = [e for e in chronik.liste(z) if e["art"] == "handy" and e["weiss"] == [pid]]
    pruefen(len(ein) >= 2, "ihre Texte stehen in ihrer Chronik (nur sie weiss davon)")

    # --- callback
    z = neues_spiel()
    i = faden_mit(z, pid)
    STATE["ton"] = "warm"
    handy.antworten(z, MODUL, i, "i'll fix the bracket alone.", BOGEN)
    e = chronik.rueckbezug_handy(z, pid, 1)
    pruefen(e and "bracket" in e["text"], "Rueckbezug findet Ducs Chat-Zeile")
    e["genutzt"] = True
    pruefen(chronik.rueckbezug_handy(z, pid, 1) is None, "jede Zeile wird nur einmal aufgegriffen")
    z2 = neues_spiel()
    i = faden_mit(z2, pid)
    handy.antworten(z2, MODUL, i, "old line", BOGEN)
    z2["tag"] = 5
    pruefen(chronik.rueckbezug_handy(z2, pid, 1) is None, "Zeilen aelter als 1 Tag zaehlen nicht")
    pruefen(not any("Duc texted" in h for fig in [chronik.fuer_figur(z2, MODUL, "lea", [])] for h in fig),
            "andere Frauen wissen nichts vom Chat")

    # --- referee for her texts
    z = neues_spiel()
    i = faden_mit(z, pid)
    STATE["ton"] = "neutral"
    STATE["chat"].clear()
    STATE["pruef"] = [["invents_event"], []]
    handy.antworten(z, MODUL, i, "hello", BOGEN)
    pruefen(len(STATE["chat"]) == 2 and "broke a rule" in STATE["chat"][1],
            "erfundenes Ereignis: einmal neu schreiben, mit Hinweis")
    STATE["chat"].clear()
    STATE["pruef"] = [["invents_event"], ["invents_event"]]
    handy.antworten(z, MODUL, i, "hello again", BOGEN)
    pruefen(len(STATE["chat"]) == 2, "nie mehr als ein Neuschreiben")

    ablage_test()
    print("OK")


def ablage_test():
    """Das Handy erinnert sich (Paket 3, 03.11.2026): Handy-Events landen in ihrem Chat-Faden."""
    ev = [e for e in json.load(open(os.path.join(EDEN, "module", "eden_rise", "ereignisse.json"), encoding="utf-8"))["events"]
          if e.get("art") == "handy"]
    karte = lambda e: MODUL["personen"].get(e["personen"].get("anrufer") or (e["personen"].get("selfie") or {}).get("frau"), {}).get("karte")
    ende = lambda e, i, **x: dict({"id": e["id"], "ergebnis": {"index": i, "text": e["optionen"][i]["text"],
                                                                "zeile": e["optionen"][i].get("zeile")}}, **x)
    video = next(e for e in ev if e["personen"].get("art") == "video" and karte(e) and not e["personen"].get("favour")
                 and any(o.get("art") == "auflegen" for o in e["optionen"]))
    pid, auf = video["personen"]["anrufer"], next(i for i, o in enumerate(video["optionen"]) if o.get("art") == "auflegen")
    an = next(i for i, o in enumerate(video["optionen"]) if o.get("art") != "auflegen" and "“" in o["text"])
    z = neues_spiel()
    n = handy.event_ablegen(z, MODUL, video, ende(video, an))
    v = handy.faden_von(z, pid)["verlauf"]
    pruefen(n >= 3 and v[0].get("art") == "anruf" and any(x["wer"] == "duc" for x in v) and "“" not in v[-1]["text"],
            "Videoanruf: grauer Eintrag, ihre Zeilen, Ducs gesagte Antwort ohne Anfuehrungszeichen")
    pruefen("(video call)" in handy._verlauf_text(handy.faden_von(z, pid), MODUL["personen"][pid]),
            "Blume liest den Anruf im Chat-Gedaechtnis")
    z = neues_spiel()
    handy.event_ablegen(z, MODUL, video, ende(video, auf))
    pruefen([x.get("art") for x in handy.faden_von(z, pid)["verlauf"]] == ["verpasst"], "abgelehnt: nur Missed video call")
    selfie = next(e for e in ev if (e["personen"].get("selfie") or {}).get("stufe") and karte(e))
    z = neues_spiel()
    handy.event_ablegen(z, MODUL, selfie, ende(selfie, 0, selfie="x_test_1"))
    f = handy.faden_von(z, selfie["personen"]["selfie"]["frau"])["verlauf"]
    pruefen(f[0].get("art") == "foto" and f[0]["bild"] == "/selfie/x_test_1.webp", "Selfie steht als Foto im Faden")
    erzaehlt = next((i for i, o in enumerate(selfie["optionen"]) if "“" not in o["text"] and '"' not in o["text"]), None)
    if erzaehlt is not None:
        z = neues_spiel()
        handy.event_ablegen(z, MODUL, selfie, ende(selfie, erzaehlt, selfie="x"))
        pruefen(not any(x["wer"] == "duc" for x in handy.faden_von(z, selfie["personen"]["selfie"]["frau"])["verlauf"]),
                "erzaehlte Antwort (ohne Anfuehrungszeichen) bleibt draussen")
    for name, e in (("Favour", next(e for e in ev if e["personen"].get("favour"))),
                    ("ohne Karte (Megan)", next(e for e in ev if e["personen"].get("anrufer") == "megan"))):
        z = neues_spiel()
        pruefen(handy.event_ablegen(z, MODUL, e, ende(e, 0)) == 0 and not z.get("handy"), "%s bleibt draussen" % name)


if __name__ == "__main__":
    main()
