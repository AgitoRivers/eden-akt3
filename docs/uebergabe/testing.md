# Übergabe: Testing (Stand 02.11.2026)

Zuständig für Gate, Spieltest-Bot, Beziehungskurve, Live-Spieltest und Modellvergleich. Diese Datei enthält keine Spoiler.

## Gebaut (master)

| Commit | Was |
|---|---|
| e34a54dd | Spieltest-Bot: 6 Spielertypen × 3 Seeds, Bericht mit Ampel (`tests/spieltest.py`, Wiki `docs/wiki/systeme/spieltest.md`) |
| b3ab6ca1 … f4419f0b, e5366283 | Beziehungskurve `tests/spieltest_kurve.py`: Stufe je Spieltag je Frau, mit und ohne 7-Tage-Abstand, Messung der längsten Stille |
| 4c2347c3 | Live-Bot und Peer-Group von Codex gesichert (`tests/spieltest_live*.py`, `spieltest_profile.py`) |
| ab4ea374 | Album: leuchtender Punkt bei neuen Selfies |
| 11d19008, d9b55ccb, 6e3aaf7d (Branch `llm_vergleich`, jetzt in master) | Modellvergleich: `tests/llm_vergleich.py`, `llm_vergleich_jury.py`, `llm_vergleich_seite.py`, Rohdaten und Jury unter `docs/abnahme/llm_vergleich/` |

Den End-to-End-Spieltest durch die Belagerung (d419fc47, `tests/spieltest_kalender.py`) hat die Story-Sitzung gebaut.

## Ergebnis Modellvergleich (an Duc und Interaction Mechanic gemeldet)

Giftige Blume bleibt das Spielmodell. Getestet wurden Blume, MeroMero 26B, PersonalityEngine 24B, Mag-Mell 12B, GemStrike 31B und MeroMero v2 31B,
je 180 Antworten auf die echten Prompts, bewertet von einer blinden Jury. Erfundene Erinnerungen und das aufgeweichte Nein zeigen alle Modelle.
Runde 3 (nur Blume, echte Absagen) zählte die Szenen mit Fehler: mit Absage allein 12 von 18, mit fester zweiter Absage 6 von 18,
mit festem Themenwechsel dazu 2 von 18. Diese Variante C baut Interaction Mechanic, die Texte schreibt Character Design (`figurenrahmen.json`).
Abnahme: `start chrome "file:///X:/AI/Eden/docs/abnahme/llm_vergleich/index.html"`

## Live-Spieltest mit Blume (gestoppt)

- Aufgabe „Eden Live Batch“ (`C:\Users\DucNg\Documents\Eden-Live\Live-Batch-0211.bat`), Ausgabe in
  `C:\Users\DucNg\Documents\Eden-Live\2026-11-02\batch`. Auf Ducs Wunsch hat Story den Lauf nach Lennys Rezensionen gestoppt.
  Fertig sind Naomi, Mia und Lenny. Die übrigen sechs Profile laufen nicht. Den Befund zu Mia und Lenny hat Story in
  `docs/uebergabe/story.md` festgehalten (3763de68). Neu starten lässt sich der Stapel mit derselben .bat, fertige Läufe überspringt er.
- Die Aufgabe „Eden Blume 5010“ läuft noch. Ob sie beendet wird, entscheidet Duc. Solange sie läuft, ist die GPU für Krea belegt.

## Wartet auf Duc

- Blume 5010 beenden oder weiterlaufen lassen.
- Offene Frage von Interaction Mechanic: Der Bot erreicht Vertrauen 5 schon an Tag 4–6 (Kurve), gewollt oder nicht?

## Offen (nicht angefangen)

- Chiaras neue Regel aus `figurenrahmen.json` (Abstand nach einem Nein) einzeln messen: `tests/llm_vergleich.py --szenarien nein_thema` nur mit Chiara, etwa 5 Minuten.
- Stufe 3 des Spieltests: Bildschirmprüfung im Browser (720p/1080p/1440p, Konsole, Tastatur).
- Bibi hat keine Lob-Zeilen (`module/eden_rise/lob.json`), obwohl sie Attribute schätzt; Zeilen schreiben und vertonen, dann `OHNE_LOB` in `test_lob.py` leeren.
- Die Belagerungs-Sperre (`modul.sperre`, ab Tag 21 Nachmittag) gilt bis zum Ende: Selfie-Fenster „bis Tag 35“, Mochi's-Spuren und Holms Wette ab Tag 22 wirken erst, wenn Akt 3 die Sperre aufhebt.

## Tests grün (Branch `t/tests-gruen`, 02.11. nachts)

Alle `tests/test_*.py` und `tests/mochis_sim.py` laufen grün. Die Tabelle vom Abend nannte acht rote Tests, im Worktree waren es
sechzehn. Was geändert wurde und warum:

| Test | Ursache | Fix |
|---|---|---|
| test_holm_wette | Gruppen sind seit 31.10. allgemein (`nach_nacht`, `ruf` …); Texte neu formuliert; Holms Intro verlor nach der Belagerungs-Sperre die Phase | Test prüft jetzt tote Gruppen-Zeilen statt „nur `hb_`“; neue Texte; **Engine-Fix** `eden.py`: nach der Intro-Szene der Wette greift die Sperre nicht (`schiessen_folgt`), sonst startet die Wette gegen Holm ab Tag 22 nie |
| test_journal_nebenquests | Erinnerungs-Paket 2 hat zwei `grotte_flut`-Texte geändert | Test auf die neuen Texte |
| test_labor_duc_sprites | Maxwells Steel-Mop-Set (26. Set, kleiner) und fünf neue Messer-`heavy_attack` vom 01.11. | Labor-Bilder nachgezogen: `werkzeuge/eden_rise/labor_duc_sprites.py --erneuern` (nur geänderte Quellen); Test kennt 26 Sets und Maxwells Größe |
| test_red_trio | Test setzte nur `werte`, die Punkte blieben alt; der nächste Zuwachs rechnete die Stufe zurück | Test setzt Punkte passend zur Stufe |
| test_selfies, mochis_sim | Nicht Megans Abwesenheit: ab Tag 21 Nachmittag zieht wegen `modul.sperre` nur noch `bl_`, an Tag 30 also nichts | Test an Tag 20 plus Prüfung „in der Belagerung kein Selfie“; Simulation an Tag 20 mit früherem `rt_ende_tag` |
| test_sprite_stimmung | Neue ernste Szenen | Inhalt: `ol_stille` (Sophia) auf `gratitude` (im Mantel-Set dreht `embarrassment` sie weg, `test_outfit_quest`), `rm_b3_b` (Bibi) auf `embarrassment` (Builder + JSON). Geprüft und in `FREI`: Rosis Rat nach dem Kampf, Wolffs Spott über seine Waffe, Alons Bühnenlächeln (gehört zur Szene) |
| test_zeit_zusammen | Rosi hat einen Figurenrahmen, der Modell-Weg lief nicht mehr | Test schaltet den Rahmen für den Modell-Weg ab (Daten-Weg prüft `test_figurenrahmen`) |
| test_akt2_events | Bibis drei private Selfies | 90 statt 87 |
| test_expedition | Aufbau füllte Lolas Events-Topf, der Rast-Anruf brachte nichts | Aufbau-Punkte aus der Quelle `szenen` |
| test_legenden | Alon und Buenaventura | in `OHNE` (Gegenspieler wie Mr. White) |
| test_lob | Bibi schätzt Attribute (Bewunderung), hat aber keine Lob-Zeilen | Test kennt Bibi als Lücke `OHNE_LOB` (offen, siehe unten) |
| test_musik | Musik ist gitignored und fehlte im Worktree | Musik kopieren (siehe Fallen) |
| test_sturm, test_ui_kopfzeile | Ausgabe mit Sonderzeichen in einer cp1252-Konsole | `sys.stdout.reconfigure(encoding="utf-8")` wie die übrigen Tests |

`test_kampf_server` schlägt weiter nur zufällig fehl.

**Live-Rezensionen und Belagerung:** Die Belagerung ist gescriptet, kam also nie als Modell-Dialog an, und aus den Events nur als ein
Kalenderpunkt (`bl_welle_6`). Minicus Szene und das Ende von Akt 2 fehlten. `tests/spieltest_live_batch.py` gibt jeder Rezension jetzt eine
Quelle `belagerung:<profil>/<seed>` (Taktik-Ergebnis, alle erreichten `bl_`-Szenen, Welle 6, Bericht und Cliffhanger mit ersten Zeilen),
knapp gehalten für Blumes 16k-Kontext (Paket etwa 28k Zeichen). Geprüft ohne Modell mit den Läufen von Mia, Lenny und Naomi und in
`test_spieltest_live_contract`. Ein neuer Live-Lauf ist nicht gestartet. Die alten `review-*.json` im Batch-Ordner werden wiederverwendet;
für neue Rezensionen sie vorher wegräumen.

## Branches, Worktrees, Prozesse

- Branch `llm_vergleich` ist in master gemergt, Branch und Worktree sind entfernt.
- Kein eigener Server. Kobold auf Port 5021 ist beendet. Die Testmodelle GemStrike und MeroMero v2 liegen im Papierkorb, Duc leert ihn selbst (37,4 GB).
- Laufend: nur noch „Eden Blume 5010“, siehe oben.

## Fallen

- Tests in `tests/` haben kein `__init__.py`: `python tests\test_x.py` starten, nicht `-m unittest tests.test_x`.
- Lange Läufe (Modellvergleich, Live-Spieltest) nur über den Aufgabenplaner, nie aus der Sitzung starten. Nur eigene Ports und Prozesse beenden.
- Ein eigenes Kobold für Messungen nie auf 5010 starten, dort läuft das Spiel. Die VRAM reicht neben Chatterbox für bis zu etwa 30 GB.
- Messläufe brauchen die Texte, die gerade im Haupt-Checkout liegen (etwa uncommittete `figurenrahmen.json`). Für den Lauf in den Worktree kopieren, danach `git checkout --`.
- Die Jury-Bewertung läuft über Sonnet-Subagenten, blind gemischt. Den Schlüssel (`*_geheim.json`) erst nach dem Urteil öffnen.
- Worktree für Tests: neben `figuren/` und `eden-config.json` auch `module/eden_rise/musik/` kopieren (gitignored, 930 MB), sonst ist `test_musik` rot.
- Tests, die den Tag weit vorstellen, landen hinter der Belagerungs-Sperre (ab Tag 21 Nachmittag nur `bl_`). Für „spät in Akt 2“ Tag 20 nehmen.
- Vertrauen/Begehren im Test nie nur über `z["werte"]` setzen: die Punkte (`z["punkte"]`) bleiben sonst alt, und der nächste Zuwachs rechnet die Stufe zurück. Punkte `STUFEN_AB[stufe] + 4` mitsetzen.
- Punkte im Testaufbau über `punkte_add` füllen den Topf der Quelle (Standard `events`); wer danach einen Events-Zuwachs prüft, baut über eine andere Quelle auf.
- Ausgabe aus Hintergrund-Läufen ist gepuffert: `python -u` nehmen, sonst sieht ein hängender Test aus wie ein langsamer.
- `ereignisse.json` hat CRLF: gezielte Text-Ersetzungen mit `\r?\n` schreiben, und dieselbe Änderung im Builder unter `werkzeuge/eden_rise/` machen.
