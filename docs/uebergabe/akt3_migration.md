# Akt 3 · Migration von der Cloud ins lokale Repo

Stand 04.11.2026 · Quelle: Repo `AgitoRivers/eden-akt3`, Branch `akt3-cloud`.

## Warum kein einfaches Mergen

`eden-akt3` ist ein **schlanker Auszug** des lokalen Eden-Repos: nur Code, Wiki und Textdaten, ohne Bilder, Ton, Sprites und Spielstände. Sein erster Commit `bdb05cc` ist ein neuer Anfang („Stand master 2b9575ef“). Die beiden Repos haben **keine gemeinsame Git-Geschichte**. Ein `git merge` geht darum nicht direkt. Übertragen wird der **Unterschied** zwischen `bdb05cc` und `akt3-cloud`: 79 Dateien, nur Text und Code, keine Bilder.

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
4. Mit Bildern und Ton neu bauen. Die JSON-Dateien wurden in der Cloud nur gezielt ergänzt, weil der Neubau dort ohne Bilder Hintergründe tauscht:
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
   Danach `git diff --stat`: Es sollte (fast) leer sein. Was abweicht, ist ein Hinweis auf eine Lücke im Auszug, bitte ansehen statt blind committen.
5. Alle Tests mit Bildern und Config, die Bots mit `PYTHONHASHSEED=0`:
   ```bash
   for f in tests/test_*.py; do PYTHONHASHSEED=0 python "$f" > /dev/null 2>&1 && echo "ok   $f" || echo "ROT  $f"; done
   ```
6. In den heutigen `master` mergen. `master` ist seit `2b9575ef` weitergegangen (andere Sitzungen), hier kann es Konflikte geben:
   ```bash
   git checkout master && git merge akt3-import
   ```
   - **Code-Dateien** (wahrscheinlich: `ereignisse_basis.py`, `eden.py`, `kern/ereignisse.py`, `kern/taktik.py`, `modul_eden_rise.py`, `kern/abschluss.py`): von Hand zusammenführen, beide Seiten behalten.
   - **Gebaute JSON-Dateien** (`ereignisse.json`, `auftraege.json`, `kaempfe.json`, `modul.json`, `stimme_tags.json`, `kommission.json`): nie von Hand. Eine Seite nehmen, dann Schritt 4 wiederholen.
7. Den Merge prüfen (Schritt 5 noch einmal), dann pushen.

## Was danach lokal noch zu tun ist

| Was | Wo |
|---|---|
| Akt 3 einschalten | `AKT3_SPIELBAR = True` in `werkzeuge/eden_rise/modul_eden_rise.py`, dann `modul_eden_rise.py` |
| Spieltest Tag 24 bis 35, Bot-Lauf, Endkampf-Balancing (Alon Level 10, Verbündete) | `tests/spieltest_kalender.py` u. a. |
| Besuchs-Lose und Petrus Netz: kommen sie ohne Phase? | Werkstatt, Bar, Angeln, Kochen, Nonnas Laden |
| Kommission-Bildschirm (Plugin `eden-commission`), dann `kommission.AN = True` | Bauanleitung im Drehbuch 12a |
| Vertonung der neuen Zeilen (Quellen `akt3_*` in `stimme_tags.json`), neue Sprecher `anwalt`, `kommissar` | Vertonen-Werkzeug |
| Bilder aus `docs/uebergabe/akt3_bestellungen.md`, Sprite Buenaventura prüfen | Character Design |
| `belagerung.md` und `drehbuch_finale.md` an E-122 angleichen (Yacht repariert, Minicu erst auf der Festa), Prozentzahl der Belagerung ausbauen | lokale Sitzung |
| Totòs Akt-3-Geheimnis (F-19) | Story-Sitzung |
| Handy-Gags `hy_` bis Tag 31? Megans Anrufe als Handy (F-12) | Handy-Sitzung |

## Nicht übernehmen

- `fix-akt2-folgen`: doppelt zu `fix-akt2`, und `fix-akt2` steckt schon in `akt3-cloud`.
- Die Analyse-Branches (`folgen-belagerung`, `balancing-bericht`, `audit-text`, `drehbuch-gegenrede`, `wiki-vs-code`, `analyse-abschluss`, `berichte-audits`) sind nur Berichte. Bei Bedarf einzeln als Dateien holen: `git show akt3/<branch>:<pfad>`.

## Prompt für die lokale Sitzung (zum Kopieren)

Lies `docs/uebergabe/akt3_migration.md` und `docs/uebergabe/akt3_cloud.md`. Führe die Migration von `AgitoRivers/eden-akt3`, Branch `akt3-cloud`, Schritt für Schritt aus: Import-Branch auf `2b9575ef`, Patch anwenden, mit Bildern neu bauen, alle Tests, dann in `master` mergen. Gebaute JSON-Dateien nie von Hand zusammenführen, sondern neu bauen. Melde mir jede Abweichung nach dem Neubau, bevor du committest. Danach: Akt 3 einschalten und einen Bot-Lauf über Tag 24 bis 35 machen.
