# -*- coding: utf-8 -*-
"""Waechter der Kreis-Ausschnitte (Duc 31.10.2026): jede Figur mit Sprites steht in module/eden_rise/gesichter.json, und
jeder Kreis liegt ganz im Bild. Neue Sprites ohne Eintrag sind nur eine Warnung, dort gilt der Mittelwert der Figur;
neue Figuren muessen gemessen werden. Beides erledigt Start-Eden.bat, von Hand: python werkzeuge/gesichter_messen.py --neu

  python tests\\test_gesichter.py
"""
import json, os, sys

EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, EDEN)
from kern import buehne  # noqa: E402


def laden(*teile):
    with open(os.path.join(EDEN, *teile), encoding="utf-8") as f:
        return json.load(f)


def kreis_fehler(e):
    """Liegt der Kreis [cx, cy, zoom, r] ganz im Bild? Der Kreisdurchmesser ist 1/zoom Bildbreiten, 1/(zoom*r) Bildhoehen."""
    cx, cy, zoom, r = e
    halb_x, halb_y = 0.5 / zoom, 0.5 / (zoom * r)
    if zoom < 0.999 or zoom * r < 0.999:
        return "Kreis groesser als das Bild"
    if cx - halb_x < -0.002 or cx + halb_x > 1.002 or cy - halb_y < -0.002 or cy + halb_y > 1.002:
        return "Kreis ragt aus dem Bild"
    return None


def main():
    cfg, modul = laden("eden-config.json"), laden("module", "eden_rise", "modul.json")
    daten = laden("module", "eden_rise", "gesichter.json")
    fehler, neu = [], 0
    for pid in modul["personen"]:
        s = buehne.sets(cfg, modul, pid)
        if not s:
            continue
        if pid not in daten:
            fehler.append("%s fehlt, messen: python werkzeuge/gesichter_messen.py --neu" % pid)
            continue
        vorhanden = {"%s/%s" % (si["ordner"] or "_", d) for si in s.values() for ds in si["dateien"].values() for d in ds}
        neu += len(vorhanden - set(daten[pid]["sprites"]) - set(daten[pid]["ohne"]))
    for pid, e in daten.items():
        if pid not in modul["personen"]:
            fehler.append("%s steht in gesichter.json, ist aber keine Figur" % pid)
        for k, w in e["sprites"].items():
            f = kreis_fehler(w)
            if f:
                fehler.append("%s %s: %s %s" % (pid, k, f, w))
    if neu:
        print("Hinweis: %d neue Sprites ohne Messung, dort gilt der Mittelwert der Figur" % neu)
    for f in fehler[:20]:
        print("FEHLER", f)
    if fehler:
        sys.exit(1)
    print("OK: %d Figuren, %d Sprites" % (len(daten), sum(len(e["sprites"]) for e in daten.values())))


if __name__ == "__main__":
    main()
