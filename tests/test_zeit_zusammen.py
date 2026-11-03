# -*- coding: utf-8 -*-
"""Zeit zusammen nach dem Live-Spieltest vom 31.10.2026: Ihr Vorschlag kennt die Szene und ihre letzten Vorschlaege,
laeuft nicht mit Temperatur 0 und bleibt nach einem intimen Moment bei diesem Moment.

  python tests\\test_zeit_zusammen.py
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


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    L.vorbereiten("eden_rise", tempfile.mkdtemp(prefix="eden_zeit_"))
    from kern import gesten as G, llm
    modul = E.modul_laden()
    G.frauen_da = lambda m, s: ["rosi"]
    # Rosi hat seit 01.11. einen Figurenrahmen (Vorschlag aus Daten, geprueft in test_figurenrahmen.py); hier der
    # Modell-Weg, den Figuren ohne Rahmen weiter nehmen
    G.figurenrahmen.gilt = lambda m, p: False
    G.privat = lambda m, s, p: True
    G.weltbuch = lambda z: {"Act: Kissing": "Direction text.", "Act: Other": "Direction text."}
    G.intim_liste = lambda z, m, s, f: [
        {"an": "rosi", "tag": "Act: Kissing", "name": "Kissing", "gruppe": "Akt", "mag": False, "nein": False},
        {"an": "rosi", "tag": "Act: Other", "name": "Other", "gruppe": "Akt", "mag": False, "nein": True}]
    aufrufe, antwort = [], {"line": "'Hold this probe, Officer.'", "category": "arbeit"}

    def falsch_chat(system, user, grammar, max_tokens=120, sampler=None):
        aufrufe.append(dict(user=user, sampler=sampler))
        return (dict(antwort) if antwort else None), 0.0
    llm.json_chat = falsch_chat
    ort = next(iter(modul["raeume"]))

    def szene():
        return {"def": {"ort": ort, "zeit": "21:30"}, "figuren": ["rosi"], "log": [
            {"art": "start", "text": "Late. The engine room hums."},
            {"art": "figur", "wer": "rosi", "name": "Rosi", "text": "Roh", "gezeigt": "Rosi wipes the bench."},
            {"art": "duc", "text": "He steps closer."}]}

    z = {"tag": 15, "phase": "abend", "szene": szene()}

    text, kat = G.zeit_vorschlag(z, modul, "rosi", "PROMPT")
    a = aufrufe[-1]
    pruefen("Rosi wipes the bench." in a["user"] and "He steps closer." in a["user"], "Vorschlag kennt die Szene")
    pruefen("Late. The engine room hums." in a["user"], "Vorschlag kennt den Szenenanfang")
    pruefen((a["sampler"] or {}).get("temperature", 0) > 0, "nicht mit Temperatur 0")
    pruefen(kat == "arbeit" and "just been intimate" not in a["user"], "ohne Intimitaet bleibt die Kategorie frei")

    z["szene"] = szene()
    G.zeit_vorschlag(z, modul, "rosi", "PROMPT")
    pruefen("Hold this probe, Officer." in aufrufe[-1]["user"], "zweiter Vorschlag kennt den ersten, auch in neuer Szene")
    for i in range(8):
        z["szene"] = szene()
        antwort["line"] = "'Vorschlag %d'" % i
        G.zeit_vorschlag(z, modul, "rosi", "PROMPT")
    pruefen(len(z["zeit_vorschlaege"]["rosi"]) == G.ZEIT_GEDAECHTNIS, "nur die letzten Vorschlaege bleiben")

    z["szene"] = szene()
    G.intim(z, modul, "Act: Other", "rosi", lambda t, p, h: False)
    pruefen("intim_zuletzt" not in z["szene"], "ein abgelehnter Wunsch zaehlt nicht als intimer Moment")
    antwort["line"], antwort["category"] = "'Hold the probe, then.'", "arbeit"
    _, kat = G.zeit_vorschlag(z, modul, "rosi", "PROMPT")
    pruefen(kat == "arbeit", "nach Ablehnung bleibt die Kategorie frei")

    z["szene"] = szene()
    G.intim(z, modul, "Act: Kissing", "rosi", lambda t, p, h: False)
    _, kat = G.zeit_vorschlag(z, modul, "rosi", "PROMPT")
    pruefen("just been intimate" in aufrufe[-1]["user"], "nach Intimitaet weiss der Vorschlag davon")
    pruefen(kat == "romantik", "nach Intimitaet zaehlt der Vorschlag als Romantik, auch wenn das Modell 'arbeit' sagt")

    z["szene"] = szene()
    G.intim(z, modul, "__sie__", "rosi", lambda t, p, h: False)
    antwort.clear()
    vorher = list(z["zeit_vorschlaege"]["rosi"])
    text, kat = G.zeit_vorschlag(z, modul, "rosi", "PROMPT")
    pruefen("Right here" in text and kat == "romantik", "Ersatzsatz nach Intimitaet bleibt beim Moment")
    pruefen(z["zeit_vorschlaege"]["rosi"] == vorher, "Ersatzsatz landet nicht im Gedaechtnis")
    print("Alles gut.")


if __name__ == "__main__":
    main()
