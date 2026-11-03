# -*- coding: utf-8 -*-
r"""Vertonte Zeilen gegen ihren Text halten (01.11.2026): Sprache und Aehnlichkeit laut Whisper. Anlass: Bibis Stimmvorlage ist franzoesisch, und Chatterbox laesst daraus ganze Saetze in Aufnahmen rutschen.
Laeuft im Python der Umgebung wavtranscribe, nicht im Krea-Python:

    %USERPROFILE%\miniconda3\envs\wavtranscribe\python.exe werkzeuge\eden_rise\aufnahmen_pruefen.py --wer bibi
    ... werkzeuge\eden_rise\aufnahmen_pruefen.py --praefix mochis.

Zeigt nur Auffaelliges: weniger als 65 % gleiche Woerter, ab drei Woertern. Verhoerer der Erkennung sind dabei, darum die Liste anhoeren, bevor neu vertont wird.
Neu vertonen: anderen Tag in stimme_fest.json setzen (neuer Text = neue Aufnahme; stimme_tags.json schreiben die Builder bei jedem Bau neu), dann Vertonen_EdenRise.bat --schluessel <Schluessel>."""
import difflib, json, os, re, sys

from faster_whisper import WhisperModel

MOD = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "module", "eden_rise")


def arg(name):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else None


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    idx = json.load(open(os.path.join(MOD, "audio_index.json"), encoding="utf-8"))
    modell = WhisperModel("large-v3", device="cuda", compute_type="float16")
    norm = lambda s: re.sub(r"[^a-z0-9 ]", "", s.lower()).split()
    n = auffaellig = 0
    for key, e in idx.items():
        p = os.path.join(MOD, "audio", e["datei"])
        if (arg("--wer") and e.get("wer") != arg("--wer")) or (arg("--praefix") and not key.startswith(arg("--praefix"))) or not os.path.isfile(p):
            continue
        n += 1
        # Immer fest Englisch: Bei freier Sprachwahl haelt Whisper starken Akzent fuer eine andere Sprache und uebersetzt ("Excellent choice" wird "Excelente eleccion")
        teile, _ = modell.transcribe(p, beam_size=5, language="en")
        ist = " ".join(s.text.strip() for s in teile)
        gleich = difflib.SequenceMatcher(None, norm(e["text"]), norm(ist)).ratio()
        if gleich < .65 and len(e["text"].split()) >= 3:
            auffaellig += 1
            print("%s %.2f\n  soll: %s\n  ist:  %s" % (key, gleich, e["text"], ist), flush=True)
    print("%d Zeilen, %d auffaellig" % (n, auffaellig), flush=True)
    os._exit(0)                                            # ctranslate2 stuerzt unter Windows beim Aufraeumen ab


if __name__ == "__main__":
    main()
