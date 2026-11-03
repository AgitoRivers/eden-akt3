# -*- coding: utf-8 -*-
r"""Kalender-Pruefung nach dem Spieltest (Duc 02.11.2026: "ob der Kalender richtig gebaut wurde, von Anfang bis Ende von Akt 2").

    python tests\spieltest_kalender.py                      liest tests\spieltest_ergebnis\roh.json
    python tests\spieltest_kalender.py --lauf a.json b.json einzelne Bot-Ergebnisse (tests\spieltest_bot.py)
    python tests\spieltest_kalender.py --von 8 --bis 23     anderer Abschnitt (Standard: Akt 2, Tag 8 bis 23)

Jede Pflicht-Szene eines festen Tags muss in mindestens einem Lauf vorkommen. Ohne Bedingung ist ein Fehlen ein Fehler im
Kalender (Exit 1). Mit Bedingung ist es nur ein Hinweis, weil kein Bot jede Bedingung erfuellt. Dazu: Haben alle Laeufe das
Ende von Akt 2 erreicht (akt2_ende), die Belagerung ohne Abkuerzung gewonnen, und wie oft half der Bot nach?"""
import argparse, json, os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HIER)


def laeufe_laden(a):
    if a.lauf:
        return [json.load(open(p, encoding="utf-8")) for p in a.lauf]
    roh = json.load(open(os.path.join(HIER, "spieltest_ergebnis", "roh.json"), encoding="utf-8"))
    return roh if isinstance(roh, list) else roh.get("laeufe") or list(roh.values())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lauf", nargs="*")
    ap.add_argument("--von", type=int, default=8)
    ap.add_argument("--bis", type=int, default=23)
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    laeufe = laeufe_laden(a)
    ev = json.load(open(os.path.join(BASE, "module", "eden_rise", "ereignisse.json"), encoding="utf-8"))["events"]
    gesehen = set()
    for m in laeufe:
        gesehen |= set(m.get("events") or {})
    pflicht = [e for e in ev if e["wann"].get("pflicht") and e["wann"]["tage"][0] == e["wann"]["tage"][1] and a.von <= e["wann"]["tage"][0] <= a.bis]
    fehler, hinweise = [], []
    for e in sorted(pflicht, key=lambda e: (e["wann"]["tage"][0], ",".join(e["wann"].get("phasen") or []))):
        if e["id"] in gesehen:
            continue
        zeile = "Tag %d %s: %s" % (e["wann"]["tage"][0], "/".join(e["wann"].get("phasen") or ["?"]), e["id"])
        (hinweise if e["wann"].get("bedingung") else fehler).append(zeile)
    print("%d Laeufe, %d Pflicht-Szenen Tag %d bis %d, %d gesehen" % (len(laeufe), len(pflicht), a.von, a.bis, sum(e["id"] in gesehen for e in pflicht)))
    ende = [m for m in laeufe if "akt2_ende" in (m.get("flags") or [])]
    sieg = [m for m in laeufe if "belagerung_gewonnen" in (m.get("flags") or [])]
    hilfe = [(m["typ"], m["seed"], h) for m in laeufe for h in ((m.get("taktik") or {}).get("hilfe") or [])]
    print("Ende von Akt 2 erreicht: %d von %d" % (len(ende), len(laeufe)))
    print("Belagerung gewonnen: %d von %d, Neustarts gesamt %d, Kaempfe von Duc und Maxwell %d" % (
        len(sieg), len(laeufe), sum((m.get("taktik") or {}).get("neustarts", 0) for m in laeufe), sum((m.get("taktik") or {}).get("kaempfe", 0) for m in laeufe)))
    for typ, seed, h in hilfe:
        print("  HILFE %s/%s: Tag %s Welle %s nach drei verlorenen Versuchen abgekuerzt" % (typ, seed, h["tag"], h["welle"]))
    for z in hinweise:
        print("  nicht gesehen (mit Bedingung): " + z)
    for z in fehler:
        print("  FEHLT (ohne Bedingung): " + z)
    nicht_ende = [(m["typ"], m["seed"], (m.get("ende") or {})) for m in laeufe if m not in ende]
    for typ, seed, e in nicht_ende:
        print("  NICHT AM ENDE %s/%s: Tag %s %s, Status %s" % (typ, seed, e.get("tag"), e.get("phase"), e.get("status")))
    return 1 if fehler or nicht_ende else 0


if __name__ == "__main__":
    sys.exit(main())
