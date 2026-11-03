# -*- coding: utf-8 -*-
r"""Senden-Klang fuers Handy (Duc 03.11.2026): kurzer, weicher Swoosh mit Plopp, lokal erzeugt (keine API, kein Download).
Platzhalter, bis Duc einen Pixabay-Klang waehlt. Schreibt module\eden_rise\sfx\handy_senden_<n>.mp3 (braucht ffmpeg).

    python werkzeuge\handy_senden_klang.py
"""
import os, subprocess, tempfile, wave

import numpy as np

EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZIEL = os.path.join(EDEN, "module", "eden_rise", "sfx")
RATE = 44100


def swoosh(dauer, f0, f1, seed):
    """Rauschen durch ein wanderndes Bandpass-Fenster, dazu ein kurzer Ton-Plopp am Ende."""
    rng = np.random.default_rng(seed)
    n = int(RATE * dauer)
    t = np.arange(n) / RATE
    rausch = rng.standard_normal(n)
    spek = np.fft.rfft(rausch)
    freq = np.fft.rfftfreq(n, 1 / RATE)
    mitte = np.sqrt(f0 * f1)
    spek *= np.exp(-((np.log(freq + 1) - np.log(mitte)) ** 2) / 0.9)       # weiches Band um die Mitte
    rausch = np.fft.irfft(spek, n)
    huelle = np.sin(np.pi * np.clip(t / dauer, 0, 1)) ** 2 * np.exp(-t * 3)
    s = rausch / (np.abs(rausch).max() + 1e-9) * huelle * 0.55
    # Plopp: kurzer, steigender Ton
    tp = t[: int(RATE * 0.09)]
    plopp = np.sin(2 * np.pi * (620 + 900 * tp / tp[-1]) * tp) * np.exp(-tp * 45) * 0.5
    start = int(n * 0.55)
    s[start:start + len(plopp)] += plopp[: n - start]
    s = s / (np.abs(s).max() + 1e-9) * 0.8
    return (s * 32767).astype(np.int16)


def main():
    os.makedirs(ZIEL, exist_ok=True)
    for nr, (dauer, f0, f1, seed) in enumerate([(0.32, 900, 4200, 3), (0.28, 1100, 5200, 8)], 1):
        daten = swoosh(dauer, f0, f1, seed)
        with tempfile.TemporaryDirectory() as tmp:
            wav = os.path.join(tmp, "s.wav")
            with wave.open(wav, "wb") as w:
                w.setnchannels(1); w.setsampwidth(2); w.setframerate(RATE); w.writeframes(daten.tobytes())
            mp3 = os.path.join(ZIEL, "handy_senden_%d.mp3" % nr)
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-codec:a", "libmp3lame", "-q:a", "3", mp3], check=True)
            print("geschrieben:", mp3)


if __name__ == "__main__":
    main()
