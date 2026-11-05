# Akt 3 · Migration von der Cloud ins lokale Repo

Stand 05.11.2026 · Quelle: Repo `AgitoRivers/eden-akt3`, Branch `akt3-cloud` (Commit `9458ca0` oder neuer).

## Warum kein einfaches Mergen

`eden-akt3` ist ein **schlanker Auszug** des lokalen Eden-Repos: nur Code, Wiki und Textdaten, ohne Bilder, Ton, Sprites, Spielstände und `eden-config.json`. Sein erster Commit `bdb05cc` ist ein neuer Anfang („Stand master 2b9575ef“). Die beiden Repos haben **keine gemeinsame Git-Geschichte**. Übertragen wird darum der **Unterschied** zwischen `bdb05cc` und `akt3-cloud`: **122 Dateien**, nur Text und Code (52 davon neu), keine Bilder.

## Vor dem Start: eine Entscheidung

Der Branch **`mina-akt3`** (andere Sitzung: Minas Fahrten nach Bastia, „Second Gear“) baut auf `akt3-cloud` auf. Probe-Merge in der Cloud: konfliktfrei, alle Tests grün.
- **Mit Mina:** Duc sagt der Cloud-Sitzung „Mina zusammenführen“. Dann steckt alles in `akt3-cloud`, und die Migration bleibt wie unten.
- **Ohne Mina:** Migration wie unten, `mina-akt3` später.

## Schritt für Schritt (lokal, Git Bash im Eden-Ordner)

1. Den Cloud-Stand holen:
   ```bash
   git remote add akt3 https://github.com/AgitoRivers/eden-akt3.git
   ```
   ```bash
   git fetch akt3 akt3-cloud
   ```
2. Einen Import-Branch **auf dem Stand, aus dem der Auszug gemacht wurde**, anlegen. Dort passt der Unterschied ohne Konflikte:
   ```bash
   git checkout -b akt3-import 2b9575ef
   ```
3. Den Unterschied als Patch erzeugen und anwenden:
   ```bash
   git diff bdb05cc akt3/akt3-cloud > ../akt3-cloud.diff
   ```
   ```bash
   git apply --3way ../akt3-cloud.diff
   ```
   ```bash
   git add -A && git commit -m "Akt 3 aus der Cloud-Sitzung (eden-akt3 akt3-cloud)"
   ```
4. Mit Bildern und Ton neu bauen. Die JSON-Dateien wurden in der Cloud nur gezielt ergänzt (ein Neubau ohne Bilder tauscht Hintergründe, der Kampf-Builder scheitert an fehlenden Sounds):
   ```bash
   python werkzeuge/eden_rise/ereignisse_basis.py
   ```
   ```bash
   python werkzeuge/eden_rise/auftraege_eden_rise.py
   ```
   ```bash
   python werkzeuge/eden_rise/kaempfe_eden_rise.py
   ```
   ```bash
   python werkzeuge/eden_rise/modul_eden_rise.py
   ```
   ```bash
   python werkzeuge/eden_rise/kommission_akt3.py
   ```
   Danach `git diff --stat`. Es sollte fast leer sein. **Erwartete Abweichungen** (in der Cloud von Hand ergänzt, der Builder schreibt sie gleich): `julien` in `modul.json`, Kampf `a3_julien` in `kaempfe.json`, Alvas Vater „Francescu“ in `modul.json`. Alles andere ansehen, nicht blind committen.
5. Alle Tests mit Bildern und Config, die Bots mit `PYTHONHASHSEED=0`:
   ```bash
   for f in tests/test_*.py; do PYTHONHASHSEED=0 python "$f" > /dev/null 2>&1 && echo "ok   $f" || echo "ROT  $f"; done
   ```
   ```bash
   PYTHONHASHSEED=0 python tests/bot_akt3.py
   ```
   In der Cloud nicht prüfbar waren: `test_legenden`, `test_taktik`, `test_holm_wette`, `test_sfx`, `test_mochis` (brauchen Config, Sprites oder Ton). `test_sfx` war schon auf `master` rot.
6. In den heutigen `master` mergen. `master` ist seit `2b9575ef` weitergegangen, hier kann es Konflikte geben:
   ```bash
   git checkout master && git merge akt3-import
   ```
   - **Code-Dateien** (wahrscheinlich: `ereignisse_basis.py`, `eden.py`, `kern/ereignisse.py`, `kern/taktik.py`, `kern/abschluss.py`, `modul_eden_rise.py`, `ereignisse_mochis.py`, `ereignisse_bibi.py`, `client/index.html`): von Hand zusammenführen, beide Seiten behalten.
   - **Gebaute JSON-Dateien** (`ereignisse.json`, `auftraege.json`, `kaempfe.json`, `modul.json`, `stimme_tags.json`, `kommission.json`, `legenden.json`): nie von Hand. Eine Seite nehmen, dann Schritt 4 wiederholen.
7. Den Merge prüfen (Schritt 5 noch einmal), dann pushen.

## To-dos für die lokale Sitzung (nach dem Merge, in dieser Reihenfolge)

| Nr | Was | Wo, wie |
|---|---|---|
| 1 | **Akt 3 einschalten** | `AKT3_SPIELBAR = True` in `werkzeuge/eden_rise/modul_eden_rise.py`, dann `modul_eden_rise.py` bauen, `test_akt3_kalender` anpassen (prüft heute „aus“) |
| 2 | **Bot über Tag 24 bis 35** mit echten Figurenkarten | `tests/bot_akt3.py` (8 Läufe, Bericht `akt3_bot_bericht.md` zum Vergleich) |
| 3 | **Kommissions-Bildschirm** einmal ganz durchspielen (Press, Karte, OBJECTION!, „I have nothing“, Plädoyer, Continue), Spielleisten ausblenden wie `eden-hearing`, Sprecher-Bilder; dann `kommission.AN = True` | `client/plugins/eden-commission/`, `kern/kommission.py` |
| 4 | **Alvas Vater** heißt jetzt Francescu: Figurenkarte „Alva Santoni“ (RoleplayGen) und `story.json` nach „Ghjuvan“ als ihrem Vater durchsuchen | E-132 |
| 5 | **Bibis Ende** an den Toren spielen (Sieg und Niederlage gegen Julien), Titelbild mit gesehenen Enden prüfen, Reiter „Village“ mit fehlendem Baustoff | `test_akt3_julien.py` als Vorlage |
| 6 | **Endkampf-Balancing**: Alon (Level 10, Verbündete), Julien (Level 8, drei Agenten), Mast-Wächter (Level 9) | Kampf-Tests |
| 7 | **Vertonen**: alle Zeilen mit Quelle `akt3_*` in `stimme_tags.json` (rund 850), neue Sprecher `anwalt` (Maître Delorme), `kommissar` (Commissioner **Luciani**), `julien`; dazu Bà Tưs „You, later.“ (jetzt mit `[sigh]`). Der alte Eintrag „Spatz. My mother called me that.“ (Quelle favours) ist veraltet | Vertonen-Werkzeug |
| 8 | **Bilder und Sprites** aus `docs/uebergabe/akt3_bestellungen.md` (Prompts stehen dort): Julien, Delorme, Luciani, AlonExo, Häuser je Bauphase, Villa, Mochi auf dem Hügel, Plüschlöwe | Character Design |
| 9 | `belagerung.md` und `drehbuch_finale.md` an E-122 angleichen (Yacht repariert, Minicu erst auf der Festa) | Wiki |
| 10 | Offene Fehler aus Akt 1 und 2, wenn Duc zustimmt: F-37 (Funken-Fenster), F-38 (Funk-Vorwarnung in Welle 3) | `akt3_fragen.md` |
| 11 | Totòs Akt-3-Geheimnis (F-19) | Story-Sitzung |
| 12 | Handy-Gags `hy_` bis Tag 31? Megans Anrufe als Handy (F-12) | Handy-Sitzung (die Cloud darf diese Dateien nicht öffnen) |

## To-dos für Duc

| Nr | Was | Wo |
|---|---|---|
| 1 | **Entscheiden:** `mina-akt3` vor der Migration zusammenführen? | oben |
| 2 | **Entscheiden:** E-131, Balance der Enden (Ende 3 kommt zu oft) | `akt3_enden_simulation.md` |
| 3 | **Entscheiden:** E-128, Säulen und Enden im Code bestätigen | `ENTSCHEIDUNGEN.md` |
| 4 | **Entscheiden:** F-37 und F-38 (Fehler in Akt 1 und 2) beheben lassen? | `akt3_fragen.md` |
| 5 | Die lokale Sitzung mit dem Prompt unten starten | unten |
| 6 | Spieltest an den wichtigsten Stellen: Tag 24 Morgen, Holms Warnung Tag 31, Villa Tag 34, Kommission, Bibis Tore, Festa, Mitternacht | lokal |
| 7 | Feinschliff der zehn Enden (Texte in `kern/akt3.ENDE_TEXT`, `kern/abschluss.py` EPILOG und BIBI_BILD) und drei Rest-Befunde der Textprüfung (Nr. 30, 57, 78) | `enden.md`, `akt3_textpruefung.md` |
| 8 | Bilder und Stimmen bestellen und abnehmen | `akt3_bestellungen.md` |
| 9 | Nach dem Merge: Analyse-Branches im Cloud-Repo aufräumen lassen (oder behalten) | GitHub |

## Nicht übernehmen

- `fix-akt2-folgen`: doppelt zu `fix-akt2`, und `fix-akt2` steckt schon in `akt3-cloud`.
- Die Analyse-Branches (`folgen-belagerung`, `balancing-bericht`, `audit-text`, `drehbuch-gegenrede`, `wiki-vs-code`, `analyse-abschluss`, `berichte-audits`) sind nur Berichte. Bei Bedarf einzeln als Dateien holen: `git show akt3/<branch>:<pfad>`.

## Prompt für die lokale Sitzung (zum Kopieren)

Lies `docs/uebergabe/akt3_migration.md` und `docs/uebergabe/akt3_cloud.md`. Führe die Migration von `AgitoRivers/eden-akt3`, Branch `akt3-cloud`, Schritt für Schritt aus: Import-Branch auf `2b9575ef`, Patch anwenden, mit Bildern neu bauen, alle Tests und `tests/bot_akt3.py`, dann in `master` mergen. Gebaute JSON-Dateien nie von Hand zusammenführen, sondern neu bauen. Melde mir jede Abweichung nach dem Neubau, die nicht in der Liste „Erwartete Abweichungen“ steht, bevor du committest. Danach arbeite die Tabelle „To-dos für die lokale Sitzung“ ab, beginnend mit Nr. 1 bis 3, und frag mich vor Nr. 10.
