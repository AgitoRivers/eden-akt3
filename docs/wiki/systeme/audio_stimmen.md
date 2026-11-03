# Stimmen: Zuordnung, Vertonung, Lautheit

> Stand 26.10.2026 · Besitz: Hauptsitzung (Story) · Tags je Zeile: [`stimme_tags.md`](stimme_tags.md) (Items-Sitzung)

## Wer spricht mit welcher Stimme

- Zuordnung Figur → Stimme: `eden-config.json` → `stimmen.eden_rise.<id>` (nicht im Git). Die Stimmen selbst stehen im
  Chatterbox-Katalog `X:\AI\Chatterbox\stimmen.json`, die Referenzdateien in `X:\AI\Chatterbox\voices\`.
- Eine Figur ohne Stimme wird beim Vertonen übersprungen (`--fehlende-auslassen`).
- **Kloster (26.10.):** „Nonna Fiora“, „Isabelle“, „Frederico“ – je die ersten ~30 s (an einer Atempause geschnitten)
  aus Ducs Aufnahmen `Stimmen\Nonna.mp3`, `Isabelle.mp3`, `Frederico.mp3`. Nicht verwechseln: „Isabella“ ist eine
  andere Katalogstimme.
- **Sophia (26.10.):** neue Stimme **„Sophia Eden“** statt „Cora“. Referenz 30,9 s aus Ducs Aufnahmen
  `Stimmen\Sophia.mp3` (22,35 s) und `Stimmen\Sophia1.mp3` (8,2 s), an Atempausen geschnitten. Im Vergleich
  (`docs/abnahme/sophia_stimme/vergleich.html`) gewann Chatterbox gegen ElevenLabs v3: Chatterbox klont die Aufnahme
  direkt und kennt die Turbo-Tags als echte Laute; die ElevenLabs-Stimme ist entworfen (Voice Design), und v3 deutet
  Tags bei kurzen Zeilen unruhig.
- Neue Stimme aus eigener Aufnahme: rund 30 s sauberes Sprechen, als 24 kHz mono WAV nach `Chatterbox\voices\
  <Name> - ENG.wav`, Eintrag im Katalog, dann in `eden-config.json` zuordnen.

## Vertonen

`Vertonen_EdenRise.bat` (Optionen im Kopf der Datei, z. B. `--wer sophia`, `--aufraeumen`). Läuft mit Chatterbox Turbo
auf Port 8004, etwa 1,3 s je Zeile. Ablage `module\eden_rise\audio\<hash>.wav`, Index `audio_index.json`.

## Lautheit (seit 26.10.2026)

Vorher lagen die Figuren zwischen **−29 LUFS** (Jana, Chiara) und **−23 LUFS** (Lola), einzelne Sätze einer Figur bis
20 dB auseinander (Petru), manche Spitzen bei 0 dB. Jetzt:

- **Jede Aufnahme wird auf −20 LUFS gebracht** (EBU R128, integriert), Spitzen höchstens **−1,5 dBTP**.
- Werkzeug: `werkzeuge/eden_rise/lautheit_angleichen.py`. Es läuft **am Ende jeder Vertonung automatisch** mit und
  bearbeitet nur Dateien, die noch nicht angeglichen sind (Liste `audio\_lautheit.json`).
- Die Datei behält ihren Namen; die Originale liegen als Sicherung in `audio\_vor_lautheit\`.
- `--messen` zeigt den Stand je Figur.
- Einzelne sehr kurze Zeilen mit lauten Lauten (Keuchen, Lachen) bleiben leiser (bis etwa −27 LUFS), weil sie sonst
  die Spitzengrenze reißen würden.

## Effekte je Figur (seit 28.10.2026)

- Manche Figuren bekommen nach der Vertonung einen Klang-Effekt, heute nur **die Sirene: Hall leicht** (zwei
  `aecho`-Stufen, kurze Reflexionen plus ein leises spätes Echo, Hörprobe `docs/abnahme/stimmen_sirene/sirene_3_hall_leicht.mp3`).
- Die **Referenzstimme bleibt trocken**, sonst klont Chatterbox den Hall unsauber mit. Bis 29.10. war das
  `The Siren - ENG.wav` (walisisch); die Sirene ist jetzt **Ligeia** mit neapolitanischem Akzent, Referenz
  `Ligeia - ENG.wav` (aus `docs/abnahme/stimmen_ligeia/ligeia_it_3.mp3`, Duc 29.10.).
- Werkzeug: `werkzeuge/eden_rise/effekte.py` (Tabelle `EFFEKTE`, Figur → Filter). Läuft am Ende jeder Vertonung
  **vor** der Lautheit, bearbeitet jede Datei nur einmal (Liste `audio\_effekte.json`), trockene Originale in
  `audio\_vor_effekt\`. Neue Figur mit Effekt = eine Zeile in `EFFEKTE`.

## Aufräumen

`Vertonen_EdenRise.bat --aufraeumen` legt Aufnahmen geänderter oder gelöschter Sätze in den Papierkorb. Aufnahmen
einer abgelösten Stimme stehen nicht mehr im Index und werden davon nicht erfasst – Sophias alte Cora-Aufnahmen
(206 Dateien) wurden am 26.10. gezielt in den Papierkorb gelegt.
