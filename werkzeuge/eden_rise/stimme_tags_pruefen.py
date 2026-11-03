# -*- coding: utf-8 -*-
r"""Prueft die Turbo-Tags der vertonten Zeilen (Duc 26.10.2026: mindestens ein Tag je gesprochener Zeile).

    python werkzeuge\eden_rise\stimme_tags_pruefen.py            Bericht, Exit 1 bei Luecken
    python werkzeuge\eden_rise\stimme_tags_pruefen.py --vorlage  Vorlage fuer fehlende Zeilen zum Eintragen

Quelle der Zeilen: vertonen_eden_rise.saetze() (Events, Laeden, Totoe, Jobs, Teile, Tutorial, Anhoerung). Die gesprochene Fassung steht in
module\eden_rise\stimme_tags.json:  {"wer": "toto", "text": "<Klartext wie im Spiel>", "gesprochen": "Wrapped it twice. [chuckle] Once ..."}

  FEHLT     Zeile ohne Eintrag oder ohne Tag (neue oder geaenderte Zeile): Eintrag anlegen, dann vertonen
  VERWAIST  Eintrag, dessen Klartext es in den Daten nicht mehr gibt (Zeile umgeschrieben): Eintrag loeschen oder auf den neuen Text setzen
  ABWEICHT  gesprochene Fassung ohne Tags entspricht nicht dem Klartext (Eintrag veraltet)
"""
import json, os, re, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, os.path.dirname(os.path.dirname(HIER)))
import vertonen_eden_rise as V  # noqa: E402
from kern import stimme  # noqa: E402


def pruefen():
    d = json.load(open(stimme.TAGS_DATEI, encoding="utf-8"))
    erlaubt = set(d.get("tags") or [])
    karte = {z["text"]: z for z in d["zeilen"]}
    texte = {}
    for key, wer, text in V.saetze():
        texte.setdefault(text, (key, wer))
    fehlt, verwaist, abweicht, schlecht = [], [], [], []
    for text, (key, wer) in texte.items():
        z = karte.get(text)
        tags = re.findall(r"\[([a-z ]+)\]", z["gesprochen"]) if z else []
        if not z or not tags:
            fehlt.append((wer, key, text))
            continue
        if any(t not in erlaubt for t in tags):
            schlecht.append((wer, key, z["gesprochen"]))
        if stimme.ohne_emoji(stimme.ohne_tags(z["gesprochen"])) != stimme.ohne_emoji(text):   # Handy-Chat: Emojis stehen nur im Spieltext
            abweicht.append((wer, key, text))
    for text, z in karte.items():
        if text not in texte:
            verwaist.append((z["wer"], z["text"]))
    return len(texte), fehlt, verwaist, abweicht, schlecht


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    n, fehlt, verwaist, abweicht, schlecht = pruefen()
    print("%d Zeilen geprueft: %d ohne Tag, %d verwaist, %d abweichend, %d mit unbekanntem Tag" % (
        n, len(fehlt), len(verwaist), len(abweicht), len(schlecht)))
    for wer, key, text in fehlt[:40]:
        print("  FEHLT    [%s] %s  %s" % (wer, key, text[:70]))
    for wer, text in verwaist[:40]:
        print("  VERWAIST [%s] %s" % (wer, text[:80]))
    for wer, key, text in abweicht[:20]:
        print("  ABWEICHT [%s] %s  %s" % (wer, key, text[:70]))
    for wer, key, text in schlecht[:20]:
        print("  TAG?     [%s] %s  %s" % (wer, key, text[:70]))
    if "--vorlage" in sys.argv and fehlt:
        print("\nVorlage fuer stimme_tags.json (gesprochen mit Tag ergaenzen):")
        for wer, key, text in fehlt:
            print(json.dumps({"wer": wer, "text": text, "gesprochen": text}, ensure_ascii=False))
    return 1 if (fehlt or abweicht or schlecht) else 0


if __name__ == "__main__":
    sys.exit(main())
