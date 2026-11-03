# -*- coding: utf-8 -*-
r"""Klang der Schlafgranate, lokal synthetisiert (Duc 01.11.2026): weicher Plopp, dann zischt die Wolke aus und atmet aus. Kein Knall, das ist der Witz nach den anderen Granaten.
Schreibt docs\abnahme\schlaf_klang\schlaf_{a,b,c}.mp3 auf Lautheit -20 LUFS und die Abnahme-Liste docs\abnahme\schlaf_klang.json.

    python werkzeuge\eden_rise\schlaf_klang.py
"""
import json, os, subprocess, sys, tempfile, wave

import numpy as np

BASIS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ZIEL = os.path.join(BASIS, "docs", "abnahme", "schlaf_klang")
RATE = 44100


def hull(t, an, ab):
    """Einhuellende: an Sekunden hoch, dann exponentiell mit Zeitkonstante ab."""
    return np.minimum(t / max(an, 1e-3), 1.0) * np.exp(-np.maximum(t - an, 0) / ab)


def gefiltert(n, tief, hoch, rng):
    """Rauschen im Frequenzband tief bis hoch."""
    f = np.fft.rfft(rng.standard_normal(n))
    hz = np.fft.rfftfreq(n, 1 / RATE)
    f *= np.clip((hz - tief) / max(tief * .5, 1), 0, 1) * np.clip((hoch - hz) / (hoch * .4), 0, 1)
    x = np.fft.irfft(f, n)
    return x / np.max(np.abs(x))


def plopp(t):
    """Dumpfer Aufschlag: fallender Sinus, ganz kurz."""
    return np.sin(2 * np.pi * (140 * t - 170 * t ** 2)) * np.exp(-t / .07)


def zisch(t, rng, ab, hell=7000):
    return gefiltert(len(t), 1800, hell, rng) * hull(t, .05, ab) * (1 + .18 * np.sin(2 * np.pi * 5.3 * t))


def atem(t, rng, an, ab):
    return gefiltert(len(t), 70, 620, rng) * hull(t, an, ab)


def schlaf(t):
    """Zwei leise fallende Toene, wie ein Augenzufallen."""
    a = np.sin(2 * np.pi * 392 * t) * hull(np.maximum(t - .5, 0), .35, .9) * (t > .5)
    b = np.sin(2 * np.pi * 294 * t) * hull(np.maximum(t - 1.35, 0), .4, 1.1) * (t > 1.35)
    return a + b


def bauen():
    rng = np.random.default_rng(1)
    dauer = 3.4
    t = np.arange(int(dauer * RATE)) / RATE
    yield "a", .5 * plopp(t) + .55 * zisch(t, rng, 1.0)
    yield "b", .5 * plopp(t) + .42 * zisch(t, rng, .75, 5200) + .6 * atem(t, rng, .6, 1.1)
    yield "c", .45 * plopp(t) + .32 * zisch(t, rng, .7, 4800) + .55 * atem(t, rng, .6, 1.1) + .14 * schlaf(t)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    os.makedirs(ZIEL, exist_ok=True)
    for name, x in bauen():
        n = len(x)
        x = x * np.minimum(1, (n - np.arange(n)) / (.5 * RATE))    # sanft aus
        x = np.int16(np.clip(x / np.max(np.abs(x)) * .9, -1, 1) * 32767)
        with tempfile.TemporaryDirectory() as tmp:
            w = os.path.join(tmp, "x.wav")
            with wave.open(w, "wb") as f:
                f.setnchannels(1); f.setsampwidth(2); f.setframerate(RATE); f.writeframes(x.tobytes())
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", w, "-af", "loudnorm=I=-20:TP=-1.5:LRA=11", "-ar", "44100", "-b:a", "128k",
                            os.path.join(ZIEL, "schlaf_%s.mp3" % name)], check=True)
    spec = {"id": "schlaf_klang", "titel": "Schlafgranate: Klang",
            "hinweis": "Nach dem Wurf-Klang läuft einer dieser drei, während sich die blaue Wolke ausbreitet. Lokal erzeugt, keine Kosten. Im Spiel steht vorerst B.",
            "gruppen": [{"id": "schlaf", "titel": "Die Wolke platzt und atmet aus", "farbe": "#7aa8e6", "max": 1, "soll": "Weich, kein Knall. Das Tier schläft ein.",
                         "kandidaten": [{"titel": "A: Plopp und Zischen", "unter": "am klarsten, etwas technisch", "datei": "schlaf_klang/schlaf_a.mp3"},
                                        {"titel": "B: Plopp, Zischen, Ausatmen (Vorschlag)", "unter": "weicher, mit tiefem Atem", "datei": "schlaf_klang/schlaf_b.mp3"},
                                        {"titel": "C: wie B, mit zwei fallenden Tönen", "unter": "am märchenhaftesten", "datei": "schlaf_klang/schlaf_c.mp3"}]}]}
    json.dump(spec, open(os.path.join(BASIS, "docs", "abnahme", "schlaf_klang.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("fertig:", ZIEL)


if __name__ == "__main__":
    main()
