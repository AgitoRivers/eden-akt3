# -*- coding: utf-8 -*-
r"""Klang-Effekte je Figur auf vertonte Saetze (28.10.2026, Duc: Sirene mit leichtem Hall).

Die Referenzstimme bleibt trocken (sonst klont Chatterbox den Hall mit), der Effekt kommt erst nach der Vertonung auf
jede Datei der Figur. Laeuft in vertonen_eden_rise.py VOR lautheit_angleichen, damit die Lautheit den fertigen Klang
misst. Was schon bearbeitet ist, steht in audio\_effekte.json (Datei -> Effekt) und wird nie zweimal bearbeitet; das
trockene Original liegt in audio\_vor_effekt\ (Sicherung, gitignored wie _vor_lautheit).

    python werkzeuge\eden_rise\effekte.py      alles, was noch fehlt
"""
import json, os, shutil, subprocess

MOD = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "module", "eden_rise")
AUDIO = os.path.join(MOD, "audio")
SICHERUNG = os.path.join(AUDIO, "_vor_effekt")
STAND = os.path.join(AUDIO, "_effekte.json")

# Figur -> (Effektname, ffmpeg-Filter). Hoerprobe: docs\abnahme\stimmen_sirene\sirene_3_hall_leicht.mp3 (Duc abgenommen)
EFFEKTE = {
    "sirene": ("hall_leicht", "aecho=0.8:0.7:40|90|160:0.35|0.25|0.15,aecho=0.8:0.6:400:0.25,volume=0.95"),
}


def anwenden(pfad, filt):
    os.makedirs(SICHERUNG, exist_ok=True)
    sicher = os.path.join(SICHERUNG, os.path.basename(pfad))
    if not os.path.exists(sicher):
        shutil.copy2(pfad, sicher)
    tmp = pfad + ".tmp.wav"
    subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-y", "-i", sicher, "-af", filt, "-ar", "24000", "-ac", "1",
                    "-c:a", "pcm_s16le", tmp], check=True)
    os.replace(tmp, pfad)


def lauf(ausgabe=print):
    stand = json.load(open(STAND, encoding="utf-8")) if os.path.exists(STAND) else {}
    idx = json.load(open(os.path.join(MOD, "audio_index.json"), encoding="utf-8"))
    offen = sorted({(v["datei"], v["wer"]) for v in idx.values() if v["wer"] in EFFEKTE
                    and stand.get(v["datei"]) != EFFEKTE[v["wer"]][0] and os.path.exists(os.path.join(AUDIO, v["datei"]))})
    if not offen:
        ausgabe("Effekte: nichts zu tun.")
        return stand
    for d, w in offen:
        name, filt = EFFEKTE[w]
        anwenden(os.path.join(AUDIO, d), filt)
        stand[d] = name
    json.dump(stand, open(STAND, "w", encoding="utf-8"), indent=0)
    ausgabe("Effekte: %d Dateien bearbeitet (%s)." % (len(offen), ", ".join(sorted({w for _, w in offen}))))
    return stand


if __name__ == "__main__":
    lauf()
