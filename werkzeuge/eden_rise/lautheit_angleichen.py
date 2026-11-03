# -*- coding: utf-8 -*-
r"""Gleicht die Lautheit aller vertonten Saetze an (Duc 26.10.2026): jede Datei aus audio_index.json auf -20 LUFS
(EBU R128, integriert), True Peak hoechstens -1,5 dBTP. Vorher lagen die Figuren zwischen -29 (Jana, Chiara) und
-23 LUFS (Lola), einzelne Saetze bis 20 dB auseinander, manche Spitzen bei 0 dB.

    python werkzeuge\eden_rise\lautheit_angleichen.py            alles, was noch nicht angeglichen ist
    python werkzeuge\eden_rise\lautheit_angleichen.py --messen   nur messen und je Figur zusammenfassen

Die Datei behaelt ihren Namen (der Cache-Schluessel von stimme.chatterbox bleibt gueltig), nur der Inhalt wird ersetzt.
Das Original liegt danach in audio\_vor_lautheit\ (Sicherung, gitignored). Was schon angeglichen ist, steht in
audio\_lautheit.json und wird nie zweimal bearbeitet. vertonen_eden_rise.py ruft das am Ende jedes Laufs selbst auf."""
import collections, json, os, re, shutil, statistics, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

MOD = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "module", "eden_rise")
AUDIO = os.path.join(MOD, "audio")
SICHERUNG = os.path.join(AUDIO, "_vor_lautheit")
STAND = os.path.join(AUDIO, "_lautheit.json")
ZIEL_LUFS, ZIEL_TP, LRA = -20.0, -1.5, 11.0


def messen(pfad):
    """-> (integrierte LUFS, True Peak dBTP) oder (None, None)."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", pfad, "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    i, tp = re.findall(r"I:\s+(-?[\d.]+) LUFS", r), re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r)
    return (float(i[-1]) if i else None), (float(tp[-1]) if tp else None)


def angleichen(pfad):
    """Zwei Durchgaenge loudnorm (linear, wo die Spitzen es erlauben) -> (vorher, nachher) LUFS."""
    filt = "loudnorm=I=%s:TP=%s:LRA=%s" % (ZIEL_LUFS, ZIEL_TP, LRA)
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", pfad, "-af", filt + ":print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    m = json.loads(r[r.rindex("{"):r.rindex("}") + 1])
    if float(m["input_i"]) < -70:                       # Stille / kaputte Datei: nicht anfassen
        return float(m["input_i"]), None
    zweit = filt + (":measured_I=%s:measured_TP=%s:measured_LRA=%s:measured_thresh=%s:offset=%s:linear=true"
                    % (m["input_i"], m["input_tp"], m["input_lra"], m["input_thresh"], m["target_offset"]))
    os.makedirs(SICHERUNG, exist_ok=True)
    sicher = os.path.join(SICHERUNG, os.path.basename(pfad))
    if not os.path.exists(sicher):
        shutil.copy2(pfad, sicher)
    tmp = pfad + ".tmp.wav"
    subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-y", "-i", sicher, "-af", zweit, "-ar", "24000", "-ac", "1",
                    "-c:a", "pcm_s16le", tmp], check=True)
    os.replace(tmp, pfad)
    return float(m["input_i"]), messen(pfad)[0]


def dateien():
    idx = json.load(open(os.path.join(MOD, "audio_index.json"), encoding="utf-8"))
    je = {}
    for v in idx.values():
        je[v["datei"]] = v["wer"]
    return je


def lauf(arbeiter=6, ausgabe=print):
    stand = json.load(open(STAND, encoding="utf-8")) if os.path.exists(STAND) else {}
    offen = [(d, w) for d, w in dateien().items() if d not in stand and os.path.exists(os.path.join(AUDIO, d))]
    if not offen:
        ausgabe("Lautheit: nichts zu tun (alles angeglichen).")
        return stand
    ausgabe("Lautheit: %d Dateien auf %.0f LUFS ..." % (len(offen), ZIEL_LUFS))
    fertig = 0
    with ThreadPoolExecutor(arbeiter) as ex:
        for (d, w), (vor, nach) in zip(offen, ex.map(lambda x: angleichen(os.path.join(AUDIO, x[0])), offen)):
            stand[d] = {"wer": w, "vorher": vor, "nachher": nach}
            fertig += 1
            if fertig % 100 == 0 or fertig == len(offen):
                ausgabe("  %d/%d" % (fertig, len(offen)))
                json.dump(stand, open(STAND, "w", encoding="utf-8"), indent=0)
    return stand


def zusammenfassung(stand, ausgabe=print):
    je = collections.defaultdict(list)
    for v in stand.values():
        if v.get("nachher") is not None:
            je[v["wer"]].append(v["nachher"])
    for w, l in sorted(je.items()):
        ausgabe("  %-10s %4d Dateien  %.1f LUFS (%.1f .. %.1f)" % (w, len(l), statistics.mean(l), min(l), max(l)))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if "--messen" in sys.argv:
        zusammenfassung(json.load(open(STAND, encoding="utf-8")) if os.path.exists(STAND) else {})
    else:
        zusammenfassung(lauf())
