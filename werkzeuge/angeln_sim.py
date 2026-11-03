# -*- coding: utf-8 -*-
r"""Balance des Angel-Drills (27.10.2026): simuliert Spieler mit unterschiedlicher Treffsicherheit gegen die Drill-Werte aus
module\eden_rise\kuechen.json (gleiche Physik wie client/plugins/eden-angeln: Punkt huepft 0..1, Zone schrumpft, Fehlklick kostet).

    python werkzeuge\angeln_sim.py            Fangquote je Stufe und Spielertyp (je 4000 Drills)

Spielermodell: der Spieler zielt auf die Mitte der Zone und drueckt mit einer Zeitabweichung (Normalverteilung, sigma in ms);
nach jedem Druck mindestens 0,35 s Pause; er wartet nach Drillbeginn 0,4 s (Orientierung). Entspannter Modus: Tempo und Schwund x0,7."""
import json, os, random, sys

EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = json.load(open(os.path.join(EDEN, "module", "eden_rise", "kuechen.json"), encoding="utf-8"))["angeln"]
TYPEN = {"gut (40 ms)": 0.040, "mittel (75 ms)": 0.075, "schwach (120 ms)": 0.120}
DT = 0.004


def drill(stufe, sigma, rng, leicht=False, wahrnehmung=2):
    d = A["drill"][str(stufe)]
    lam = 0.7 if leicht else 1.0
    tempo, schwund = d["tempo"] * lam, d["schwund"] * lam
    zone = d["zone"] + A["wahrnehmung_zone"] * max(0, min(3, wahrnehmung - 2))
    y, richtung = rng.random(), rng.choice((1, -1))
    mitte = neue_mitte(zone, y, rng)
    t, treffer, fehler, naechster = 0.0, 0, 0, 0.4
    geplant = None
    while t < 30:
        t += DT
        y += richtung * tempo * DT
        if y > 1:
            y, richtung = 2 - y, -1
            tempo *= 0.9 + rng.random() * 0.2
        if y < 0:
            y, richtung = -y, 1
            tempo *= 0.9 + rng.random() * 0.2
        zone -= schwund * DT
        if zone <= 0.015:
            return False, fehler
        zu = (mitte - y) * richtung > 0                           # der Punkt laeuft auf die Zone zu
        if t >= naechster and geplant is None and zu and abs(mitte - y) / tempo < 0.6:
            geplant = t + abs(mitte - y) / tempo + rng.gauss(0, sigma)   # der Spieler zielt auf die Mitte der Zone
        if geplant is not None and t >= geplant:
            geplant = None
            naechster = t + 0.35
            if abs(y - mitte) <= zone / 2:
                treffer += 1
                if treffer >= d["treffer"]:
                    return True, fehler
                tempo *= A["tempo_je_treffer"]
                mitte = neue_mitte(zone, y, rng)
            else:
                fehler += 1
                zone -= A["fehler"]
    return False, fehler


def neue_mitte(zone, y, rng):
    h = zone / 2
    for _ in range(12):
        m = h + rng.random() * (1 - 2 * h)
        if abs(m - y) > 0.3:
            return m
    return h if y > 0.5 else 1 - h


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    rng = random.Random(7)
    n = 4000
    print("Fangquote (perfekt = ohne Fehlklick) je Stufe, %d Drills" % n)
    for leicht in (False, True):
        print("\n%s" % ("Entspannter Modus" if leicht else "Normal"))
        print("%-18s %s" % ("Spieler", "  ".join("Stufe %d" % s + (" (Fund)" if s == 0 else "       ") for s in range(4))))
        for name, sigma in TYPEN.items():
            zeile = []
            for s in range(4):
                ok = perfekt = 0
                for _ in range(n):
                    g, f = drill(s, sigma, rng, leicht)
                    ok += g
                    perfekt += g and f == 0
                zeile.append("%3d %% (%2d %%)  " % (100 * ok / n, 100 * perfekt / n))
            print("%-18s %s" % (name, " ".join(zeile)))


if __name__ == "__main__":
    main()
