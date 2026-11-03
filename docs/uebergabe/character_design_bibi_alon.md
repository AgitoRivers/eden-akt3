# Übergabe: Character Design, Bibis Arc und Alon (Stand 02.11.2026)

Sitzung 5d6a1874. Bereich: Bibis Arc (Text, Einbau, Kosenamen, Selfies), Alon als Figur (Stimme, Gesicht, Sprites, Bühne), Cliffhanger Ende Akt 2. Outfits, Holm und Nebenfiguren-Outfits stehen in `character_design_outfits.md` (andere Sitzung). Keine Spoiler in dieser Datei.

## Gebaut (master)

| Commit | Was |
|---|---|
| 4fb3fa08, 5ef71b43 | Bibis Arc: Code/Daten und Wiki (Text `docs/brain_trust/BIBI_ARC_TEXTE.md`) |
| 81b95290, c4e279a5, a8c929f3 | Absturz-Fix `szene.karte` ohne ST-Karte, Selfie-Texte, Lautschrift der Kosenamen in `kern/stimme.AUSSPRACHE` |
| d5cdc250, 50518624 | Cliffhanger Ende Akt 2 (`werkzeuge/eden_rise/ereignisse_cliffhanger.py`), Beta-Schlusskarte `kern/abschluss.AKT2_BETA`, Gate-Referenzen |
| 89f280f7 | Alon: Stimme (ElevenLabs Voice Design), Keynote-Casting, Bühne; Bibis Selfie- und Kosenamen-Abnahmen |
| a3d7444a | Alon spricht selbst: Person `alon`, Raum `alon_keynote` (versteckt), Set `alon_standard`, neue Events `bl_cliff_platz` und `bl_cliff_blicke`, Gate-Referenzen |
| c52f9f2a | Gesichter für Alons 22 Sprites gemessen |
| 7c3585b0 (von Interaction Mechanic) | enthält meine `SELFIE_SZENE` in `mochis_daten.py`: Polaroid-Titel A/B und Field-Book-Log je Tier |
| 623af5af | Bühnen-Motive `alon_keynote`/`alon_keynote_nah` in `werkzeuge/hintergrund_bild.py`, Alon-Skripte, Abnahmen und Urteile |

Außerhalb des Repos: Alons Sprites in `module/eden_rise/figuren/Alon` (gitignored, `_name.txt` = `alon_standard`), Bühne `eden_rise_alon_keynote_nah.png` im ST-Hintergrund-Ordner, Stimme `X:\AI\Chatterbox\voices\Alon Varenne - ENG.wav` mit Katalog-Eintrag in `stimmen.json`, Zuordnung `"alon": "Alon Varenne"` in `eden-config.json` (gitignored).

## Bibis Arc: Stand

Gebaut und im Spiel: Bogen bis zum Geständnis (Ducs Seite im Field Book), Kosenamen-Tick (alle Namen von Duc abgenommen), Selfie je gefangenem Tier, Romanze über `personen.bibi.romanze_flags`. Die Tier-Selfies (14 Tiere, Szene A/B) baut jetzt Interaction Mechanic (`karten_neu/bibi_tier_selfies_2.py` ff.).

Offen:
- Die Bilder der privaten Selfies macht Duc selbst im Prompt Studio (Preset `Bibi_Selfie`, Karten-Tag `bibi_selfie`). Die drei privaten Selfies haben noch keine Events.
- Ducs Urteil zu den Outfit-Selfies: Anime-Abend und Pitch-Tag neu machen? Abnahme `docs/abnahme/bibi_outfit_selfies.json`.
- Charlys Presets: `base_prompt` enthält Danzels Subject-Satz, an Prompt Studio gemeldet, nicht behoben.
- Stimmtest der französischen und deutschen Kosenamen, Vertonung, Buenaventura-Szene (Akt 3). Die Beziehungskurve rechnet Bibi nicht (statisch romanzierbar), `tests/bibi_kurve.py` gibt eine Schätzung.
- Duc hat den Arc noch nicht gespielt.

## Alon und Cliffhanger: Stand

Fertig: Stimme (Runde 2 Probe 3), Gesicht „Falke“, 22 Posen im Rollkragen, Bühne „nah“ v5, Szene mit Alon als Sprecher. Gate grün, 27/27 Spieltest-Läufe bis Ende Akt 2 (d419fc47).

Vertont (02.11. abends, Lauf einer anderen Sitzung) und per Whisper gegen den Text geprüft: alle elf Zeilen des Cliffhangers, Alon eingeschlossen, ohne Fehler.

Offen:
- Duc hat die Szene noch nicht gespielt.
- Kampf-Sprite für Alon: `karten_neu/kampf_alon_cyber.py` ist nicht aus dieser Sitzung, dort nachfragen.

## Holms Sets (02.11., a501afbf)

ST-Ordner „Marit Holm“: Hauptordner `Bridge` (weiße Uniform, bis zum Abtransport), set2 `holm_bikini` (nur über `sets=` in Events), set3 `holm_shirt` (Look M, ab Flag `holm_zurueck` über `set_frei`, auch in „Back Aboard“). „Night Watch“ gibt es nicht mehr. Im Hauptordner fehlt `neutral.png`. Ohne neutral nimmt die Engine ein beliebiges anderes Gefühl als Grundbild. Nach einer Umbenennung von Sets den Eden-Server neu starten (`kern/buehne` merkt sich die Sets).

## Vertonung: so geht es (Stand 02.11. abends: 5830 Sätze, 0 fehlen)

1. **Zählen:** `Vertonen_EdenRise.bat --liste` zählt alle Sätze je Figur und startet kein Chatterbox. Welche wirklich fehlen, zeigt erst der Lauf, weil fertige Zeilen übersprungen werden.
2. **Laufen lassen** (über Nacht, im eigenen Fenster): `X:\AI\Eden\Vertonen_EdenRise.bat` ohne Argumente. Die .bat startet Chatterbox TURBO auf Port 8004 selbst, falls er nicht läuft. Sie vertont alles, was fehlt, und gleicht am Ende die Lautheit an (`lautheit_angleichen.py`, -20 LUFS). Teilmengen: `--wer <id>`, `--praefix <anfang>`, `--schluessel <a,b>`, Probelauf `--nur 3`.
3. **Einbau:** Er passiert von selbst. Die Aufnahme heißt nach Stimmdatei und gesprochenem Text (`audio\<md5>.wav`), die Engine findet sie über denselben Schlüssel. `module/eden_rise/audio` und `audio_index.json` sind gitignored, also nichts committen.
4. **Prüfen:** `%USERPROFILE%\miniconda3\envs\wavtranscribe\python.exe werkzeuge\eden_rise\aufnahmen_pruefen.py --wer <id>` (oder `--praefix`) zeigt Zeilen mit weniger als 65 % gleichen Wörtern. Vor allem bei Bibi nötig: Ihre französische Stimmvorlage lässt Sätze in die Aufnahmen rutschen. Die Liste anhören, Whisper verhört sich auch.
5. **Eine Zeile neu würfeln:** In `module/eden_rise/stimme_fest.json` einen anderen Turbo-Tag setzen, nie in `stimme_tags.json`, das schreibt jeder Bau neu. Dann `Vertonen_EdenRise.bat --schluessel <schluessel>`.
6. **Ohne Stimme:** Bricht der Lauf mit „Ohne Stimme im Katalog“ ab, fehlt die Zuordnung in `eden-config.json` → `stimmen.eden_rise.<id>`. Mit `--fehlende-auslassen` läuft er trotzdem weiter.

## Sprite-Sätze anderer Bereiche (zur Info für STAND.md)

- **Mina:** Ordner „Mina Orsoni“ fehlt, Duc macht den Satz selbst. Tags-Abnahme `docs/abnahme/mina_tags.json`.
- **Wunsch-Outfits, Nebenfiguren-Outfits, Holms Uniform:** siehe `character_design_outfits.md`. Holm M ist freigegeben, der Satz ist noch nicht gerendert. Bibi K soll neu gemacht werden.
- **Danzels Schneider:** Pilot ist Chiaras Bridge Jacket (`docs/abnahme/bridge_jacket.json`), der volle Satz kommt erst nach Ducs Wahl. Die Laden-Abnahme `docs/abnahme/theatre_rouge.json` ist offen. Die Dress Whites sind im Spiel.
- **Holms Schießwette:** Ziel-Sprites (`werkzeuge/schiessen_bilder.py`) und die Klang-Abnahme sind offen.

## Abnahmen, die auf Duc warten

```
start chrome "X:\AI\Eden\docs\abnahme\bibi_outfit_selfies\index.html"
```

## Fallen

- Raum in `modul.json`: `bild` muss ein Objekt sein (`{"tag": "datei.png"}`). Ein String lässt das Gate mit `AttributeError: 'str' object has no attribute 'get'` abstürzen.
- Neue Figur für Events: in `ereignisse_basis.py` in `NEBEN` und `SETS`, der Raum in `RAEUME`, die Person in `modul_eden_rise.py` und gezielt in `modul.json`. Danach `gesichter_messen.py --neu` und `gesichter.json` committen.
- `stimme_tags.json` im Haupt-Checkout enthält oft ungespeicherte Zeilen anderer Sitzungen. Beim Nachziehen zusammenführen, nie überschreiben.
- `wt_bibi` im Scratchpad hat Junctions nach `module/eden_rise/figuren`. Nie per `rm -r` oder `git worktree remove --force` löschen, erst die Junctions per `rmdir` entfernen.
- Hintergründe nur über `hintergrund_bild.py` nach `docs/wiki/systeme/hintergruende.md`.
- Vorher kaputt, nicht von mir: `tests/mochis_sim.py` (Status `szene` statt `kampf`) und `tests/test_sprite_stimmung.py` (Sophia `joy` in `ol_stille`) schlagen auf sauberem master fehl.

## Branches, Worktrees, Prozesse

- Kein eigener Branch. Worktree `C:\Users\DucNg\AppData\Local\Temp\claude\C--Users-DucNg\5d6a1874-afaa-4bb2-a988-705b9b9ab96c\scratchpad\wt_bibi` ist detached auf master und sauber (Junctions beachten).
- Abnahme-Server dieser Sitzung, enden mit ihr: 8411 Kosenamen, 8412 Tier-Selfie-Probe, 8413 Kosenamen 2, 8414 Outfit-Selfies, 8415 Alon Look und Bühne, 8416 Alon Stimme.
- Kein Krea-Lauf offen.
