# -*- coding: utf-8 -*-
"""Tischszenen (27.10.2026, Kochen Stern 1): Daten, Ausloeser beim ersten vollen "liebt", Grenzen, Beats, Audio-Zeilen.

Laeuft ohne Modell, Stimme und Netz (der Wurf wird festgelegt).

  python tests\\test_tisch.py
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(HERE)
sys.path.insert(0, EDEN)
from kern import handel, stimme, tisch, wuerfel, zustand  # noqa: E402

MODUL = json.load(open(os.path.join(EDEN, "module", "eden_rise", "modul.json"), encoding="utf-8"))
REGELN = json.load(open(os.path.join(EDEN, "module", "eden_rise", "gegenstaende.json"), encoding="utf-8"))["kochen"]
EUROPAEISCH = {"casanova", "petru", "chiara", "holm", "siri", "megan", "elsa"}       # kein "Your answer": Duc muss nichts erklaeren
ERLAUBT = {"chuckle", "clear throat", "cough", "gasp", "laugh", "shush", "sigh", "sniff"}


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def neues_spiel():
    z = zustand.neu(MODUL, "entspannt")
    zustand.persona_setzen(z, MODUL, MODUL["personas"][0])
    z["tag"], z["phase"], z["status"] = 3, "dinner", "wahl"
    z["heute"] = []
    handel.init(z, MODUL)
    return z


def festen_wurf(ergebnis):
    wuerfel.probe = lambda *a, **k: {"ergebnis": ergebnis, "wurf": 15, "boni": [("Perception", 2)], "summe": 17, "sg": 10}


def kochen(z, figur, gericht, ergebnis="erfolg"):
    festen_wurf(ergebnis)
    z.pop("essen_tag", None)                                  # ein neuer Tag: heute darf wieder gekocht werden
    return handel.kochen_aktion(z, MODUL, REGELN, gericht, figur)


def lieblinge():
    """figur -> Lieblingsgericht laut Modul (Geschenkwert 2 auf einem Gericht)."""
    out = {}
    for iid, it in MODUL["items"].items():
        if it.get("art") == "gericht":
            for p, w in (it.get("geschenk") or {}).items():
                if w == 2:
                    out[p] = iid
    return out


def daten_pruefen():
    d = tisch.daten(MODUL)
    soll = lieblinge()
    pruefen(len(soll) == 14 and set(d) == set(soll), "14 Figuren mit Lieblingsgericht, jede hat eine Szene (%s)" % sorted(set(d) ^ set(soll)))
    tags = {z["text"]: z["gesprochen"] for z in json.load(open(stimme.TAGS_DATEI, encoding="utf-8"))["zeilen"]}
    fehler, n = [], 0
    for pid, s in d.items():
        if s["item"] != soll[pid]:
            fehler.append("%s: Gericht %s statt %s" % (pid, s["item"], soll[pid]))
        if bool(s["antwort"]) == (pid in EUROPAEISCH):
            fehler.append("%s: Your answer passt nicht zur Einteilung" % pid)
        if not s["titel"] or set(s["teller"]) != {"normal", "kritisch"} or len(s["erinnerung"]) != 2:
            fehler.append("%s: Beats unvollstaendig" % pid)
        for r in [s["bissen"]] + s["erinnerung"]:
            n += 1
            g = tags.get(r["text"])
            roh = [t.strip(" []") for t in stimme.TAG_MUSTER.findall(g or "")]
            if not g or not roh or any(t not in ERLAUBT for t in roh) or stimme.ohne_tags(g).replace("  ", " ") != r["text"]:
                fehler.append("%s: Tag fehlt oder Klartext weicht ab: %s" % (pid, r["text"][:40]))
            if stimme.getaggt(r["text"]) != g or stimme.TAG_MUSTER.search(r["text"]) or set('"*_~\n[]') & set(r["text"]):
                fehler.append("%s: Anzeige/Stimme: %s" % (pid, r["text"][:40]))
        for feld in ("antwort",) + tuple(s["teller"]):
            t = s["antwort"] if feld == "antwort" else s["teller"][feld]
            if t and ("[" in t or set('"*_~\n') & set(t)):
                fehler.append("%s.%s: Zeichen im Erzaehltext" % (pid, feld))
    pruefen(n == 42, "42 vertonte Zeilen")
    pruefen(not fehler, "Gericht, Einteilung, Beats, Tags: Anzeige ohne Tag, Stimme mit Tag %s" % fehler[:3])


def ausloeser_pruefen():
    z = neues_spiel()
    pruefen("tisch" not in z and "tisch_gesehen" not in z, "frischer Spielstand: keine neuen Schluessel")
    kochen(z, "lola", "fiskesuppe")
    pruefen("tisch" not in z and "tisch_gesehen" not in z, "falsches Gericht: keine Szene, kein Schluessel")
    kochen(z, "crew", "bao_buns")
    pruefen("tisch" not in z and "tisch_gesehen" not in z, "Crew-Essen: keine Szene")
    kochen(z, "elsa", "baguettes", "fehlschlag")
    pruefen("tisch" not in z, "Wurf misslungen: nur \"gut\", die Szene wartet")
    kochen(z, "elsa", "baguettes", "erfolg")
    pruefen(z.get("tisch", {}).get("pid") == "elsa" and not z["tisch"]["kritisch"], "erster voller Treffer: Szene startet (Elsa)")
    pruefen(any(isinstance(x, str) and x for x in z["tisch"]["zeilen"]), "Folgenzeilen mitgenommen: %s" % z["tisch"]["zeilen"])
    pruefen(next(v for v in z["vorlieben"] if v["figur"] == "elsa")["text"] == tisch.daten(MODUL)["elsa"]["erinnerung"][0]["text"],
            "Erinnerung 1 steht als Text der Vorliebe im Profil")
    tisch.fertig(z)
    pruefen("tisch" not in z and z["tisch_gesehen"] == ["elsa"], "Weiterklicken beendet die Szene, gesehen bleibt")
    kochen(z, "elsa", "baguettes", "kritisch")
    pruefen("tisch" not in z, "dieselbe Figur sieht ihre Szene nur einmal")
    kochen(z, "rosi", "ramen", "kritisch")
    pruefen(z["tisch"]["pid"] == "rosi" and z["tisch"]["kritisch"], "kritischer Wurf: Szene mit der Meisterwerk-Fassung (Rosi)")


def beats_pruefen():
    z = neues_spiel()
    kochen(z, "rosi", "ramen", "kritisch")
    sprite = lambda pid, gef: "/sprite/%s/_/%s-1.png" % (pid, gef)
    a = tisch.ansicht(z, MODUL, sprite)
    arten = [b["art"] for b in a["beats"]]
    pruefen(arten == ["titel", "teller", "rede", "antwort", "rede", "rede", "folgen"], "nicht-europaeisch: 7 Beats mit Your answer (%s)" % arten)
    pruefen(a["beats"][1]["text"] == tisch.daten(MODUL)["rosi"]["teller"]["kritisch"], "Teller: kritische Fassung")
    pruefen([b["id"] for b in a["beats"] if b["art"] == "rede"] == ["tisch.rosi.0", "tisch.rosi.1", "tisch.rosi.2"], "Audio-Schluessel der drei Figurenzeilen")
    pruefen(all(b.get("sprite") for b in a["beats"]), "jeder Beat hat ein Sprite")
    pruefen(a["beats"][-1]["titel"] == "Favourite dish discovered" and a["beats"][-1]["zeilen"], "Folgenkarte mit Zeilen")
    z2 = neues_spiel()
    kochen(z2, "holm", "pytt_i_panna")
    b2 = [b["art"] for b in tisch.ansicht(z2, MODUL, sprite)["beats"]]
    pruefen(b2 == ["titel", "teller", "rede", "rede", "rede", "folgen"], "europaeisch: 6 Beats ohne Your answer (%s)" % b2)
    pruefen(tisch.ansicht(neues_spiel(), MODUL, sprite) is None, "ohne offene Szene keine Ansicht")


def audio_pruefen():
    d = tisch.daten(MODUL)
    pruefen(tisch.zeile(MODUL, "tisch.lola.0") == ("lola", d["lola"]["bissen"]["text"]), "tisch.lola.0 = erster Bissen")
    pruefen(tisch.zeile(MODUL, "tisch.lola.2") == ("lola", d["lola"]["erinnerung"][1]["text"]), "tisch.lola.2 = Erinnerung 2")
    for schlecht in ("tisch.lola.3", "tisch.nobody.0", "tisch.lola", "tisch.lola.0.x", "laden.lola.0", "tisch.lola.-1"):
        pruefen(tisch.zeile(MODUL, schlecht) == (None, None), "kein freier Text aus der URL: %s" % schlecht)
    try:
        sys.path.insert(0, os.path.join(EDEN, "werkzeuge", "eden_rise"))
        import vertonen_eden_rise as v
        tisch_saetze = [s for s in v.saetze() if s[0].startswith("tisch.")]
        pruefen(len(tisch_saetze) == 42 and len({s[0] for s in tisch_saetze}) == 42, "Vertonen kennt 42 tisch.*-Schluessel")
    except ImportError as e:
        print("uebersprungen (Vertonen nicht ladbar):", e)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    daten_pruefen()
    ausloeser_pruefen()
    beats_pruefen()
    audio_pruefen()
    print("ALLES OK")
