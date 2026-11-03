# -*- coding: utf-8 -*-
"""Sirene (Duc 29.10.2026): wer sie mit Waffe, Spezialangriff oder Granate trifft, bekommt eskalierende Hinweise -
Schlag 1 neckt sie, 2 und 3 kleine Hinweise, 4 der direkte, dann leuchtet Talk (Schwaeche sichtbar). Je Zug hoechstens
einer, vertont als kampf.sirene.<n>; danach wieder die feste Zeile. Und sie verliert nie LP.

  python tests\\test_sirene.py
"""
import json, os, sys, tempfile

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import lauf_test as L  # noqa: E402

E = L.eden


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


class Fest:
    def random(self):
        return 0.99

    def randint(self, a, b):
        return 10


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    L.vorbereiten("eden_rise", tempfile.mkdtemp(prefix="eden_sirene_"))
    z = E.aktion("neu", {"modus": "ironman"})
    modul = E.modul_laden()
    kampf = E.kampf
    defs = kampf.daten(E.moddir("eden_rise"))
    hinweise = defs["enemies"]["sirene"]["untouchable_hinweise"]
    pruefen(len(hinweise) == 4 and all(h["wer"] == "sirene" for h in hinweise), "vier Hinweise in ihrer Stimme")
    kampf.starten(z, defs, "fn_5_sirene", rng=Fest())
    stimmen = []
    for n in range(6):
        k = z["kampf"]
        kampf.zug(z, modul, "angriff", rng=Fest())
        k = z["kampf"]
        ev = [e for e in k.get("events") or [] if e["art"] == "stimme"]   # vor der Parade lesen: die setzt events neu
        if k["phase"] == "parade":
            kampf.parade_aufloesen(z, modul, "ausweichen" if k["parade"].get("nur_ausweichen") else "gut", rng=Fest())
            k = z["kampf"]
        stimmen.append(ev[0]["schluessel"] if ev else None)
        g = k["gegner"][0]
        pruefen(g["lp"] == g["lp_max"], "Schlag %d: keine LP verloren" % (n + 1))
        if n == 2:
            pruefen(not g["schwaeche_bekannt"], "nach drei Schlaegen noch kein Leuchten")
        if n == 3:
            reden = next(f for f in kampf.faehigkeiten(z) if f["id"] == "reden")
            pruefen(g["schwaeche_bekannt"] and reden["schwaeche"], "nach dem vierten Schlag leuchtet Talk")
        if k.get("ergebnis"):
            break
    pruefen(stimmen[:4] == ["kampf.sirene.%d" % i for i in range(4)], "Hinweise 1-4 der Reihe nach: %s" % stimmen[:4])
    pruefen(all(s is None for s in stimmen[4:]), "danach keine neue Stimme, nur die feste Zeile")
    log = json.dumps(z["kampf"]["log"], ensure_ascii=False)
    pruefen(defs["enemies"]["sirene"]["untouchable"] in log, "die feste Zeile kommt nach den Hinweisen")
    tags = {t["text"] for t in json.load(open(os.path.join(E.moddir("eden_rise"), "stimme_tags.json"), encoding="utf-8"))["zeilen"]}
    pruefen(all(h["text"] in tags for h in hinweise), "jeder Hinweis hat Turbo-Tags")
    print("OK")


if __name__ == "__main__":
    main()
