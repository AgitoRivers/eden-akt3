# Fähigkeiten: UI und Vorschau

Stand: 25.10.2026. Aktueller PC-Entwurf nach Ducs Freigabe und Braintrust-Bewertung.

## Bedienung

Unter **Character → Open skill tree** (Taste C, siehe `menue.md`) stehen vier horizontale Pfade. Links beginnt jeder Pfad mit seiner Einstiegsfähigkeit, rechts steht sein Finale. Alle 16 Symbole sind gleichzeitig sichtbar. Pfadfarbe, Anzahl gelernter Fähigkeiten und Verbindungslinien zeigen die Entwicklung. Status: gelernt, lernbereit oder gesperrt. Auch gesperrte Fähigkeiten bleiben auswählbar.

Die schmale obere Leiste enthält Level, Erfahrung, Hauptpfad, freie Punkte und „Punkte & Regeln“. Die Hilfe öffnet als kompakte Karte über dem Board und verschiebt den Inhalt nicht.

Rechts zeigt die Auswahl Symbol, Kurzbeschreibung und Ausdauerkosten. Drei Detailreiter ersetzen lange Textspalten: **Wirkung** mit Voraussetzungen, **Kombos** mit ergänzenden Hinweisen, **Pfad** mit den aktuellen Eigenheiten und der Gleichstandsregel. Animation und Lernen stehen nebeneinander. Vor einer verfügbaren Lernentscheidung erscheinen ein möglicher Hauptpfadwechsel und konkrete Attributänderungen. Keine Scrollbereiche im Fähigkeiten-Board.

Maus: Symbol oder Detailreiter anklicken. Tastatur: Tab/Enter; auf einem Skill navigieren die Pfeiltasten zwischen den vier Pfaden und Stufen. Es wird ausschließlich nach Klick auf „Lernen“ die vorhandene Aktion `skill_lernen` ausgelöst. Keine neue Lern- oder Kampfregel.

## Daten und Technik

- `client/plugins/eden-skills/eden-skills.js`: Darstellung, Auswahl und bestehende Lernaktion.
- `client/plugins/eden-skills/eden-skills.css`: vollständiger PC-Entwurf mit horizontalen Pfaden; Rauchglas und Champagner-Akzente folgen Eden.
- `eden-skills-guide.js`: kurze Funktionsbeschreibungen und aus `docs/wiki/systeme/kampf.md` abgeleitete Kombo-Hinweise. Der vorhandene Schmuggler-Hinweis erscheint im zugehörigen Kombo-Reiter.
- `eden-skills-preview.js`: Animationsfenster auf Wunsch. Verbindliche Variante aus `freigabe-spezialangriffe.js`, einmaliger Durchlauf, Pause/Wiederholen, vollständiges Entladen beim Schließen und Fokus zurück zur Auswahl. Keine Engine-Aktion, kein Ausdauer- oder Punkteverbrauch.
- `icons/`: unveränderte Kopien der 16 freigegebenen Einzelsymbole. Spiel-IDs werden ausdrücklich auf die Effektlabor-IDs abgebildet.
- `kern/kampf.py`: `learning_preview` berechnet Prognosen mit `lernen`, `main_path` und `attributes` auf tiefen Zustandskopien. `lernfolgen` enthält bisherigen/neuen Hauptpfad, Attribute vorher/nachher und einen Gleichstand. Gesperrte und gelernte Fähigkeiten erhalten keine Prognose. `hauptpfad_prioritaet`, `skillpunkte_gesamt` und `skillpunkte_plan` stammen aus den bestehenden Konstanten.
- `client/index.html`: eigener Reiter, Plugin-Einbindung und Fenstergröße. `eden-combat.js`: der alte Fähigkeitenblock entfällt im Ausrüstungsreiter; Waffen und Rüstungen bleiben dort.
- `eden.py`: begrenzte öffentliche Plugin-Route. `preview-files.json` ist eine ausdrückliche Dateiliste für den Vorschau-Renderer und seine Bilder; Quellarchive und andere Dokumente werden nicht mit ausgeliefert.

## Showcase

http://127.0.0.1:8337/status-labor/faehigkeiten/

Vier Beispiele: fortgeschritten, Pfadwechsel, Einstieg und vergebene Punkte. Die 24 erreichbaren Beispieldaten werden mit den echten Engine-Funktionen in einer isolierten Codekopie erzeugt. Lernen in der Vorschau wechselt nur zwischen berechneten Beispielen; es gibt keine parallele JavaScript-Kampfberechnung. Erzeugen: `python werkzeuge/eden_rise/skill_showcase_bauen.py`.

## Prüfung

- `tests/test_skills_pc.cjs`: alle 16 Skills sowie Wechselprognosen auf 1280×720, 1366×768, 1600×900 und 1920×1080 ohne Scrollen oder abgeschnittene aktive Detailtexte. Zusätzlich alle Detailreiter auf 720p, Pfeiltasten und Fokus, Hilfe und Punkteverbrauch im Beispiel.
- `tests/test_skills_ui.cjs`: 16 Icons und Detailansichten, Sperrgründe, gelernt, fehlende Punkte, Einstieg und Tastatur.
- `tests/test_skills_preview.cjs`: alle 16 freigegebenen Varianten, Abspielen, Anhalten, Wiederholen, Escape, Entladen, Fokus und unveränderte Punkte; keine schreibenden Netzwerkanfragen.
- `tests/test_skills_assets.py`: Originalbilder, öffentliche Dateiroute und Liste, Datenvertrag für Punktevergabe.
- `tests/test_skills_learning.py`: echte Lernfolgen, unveränderter Eingangszustand, erster/gleicher/gewechselter Hauptpfad, Gleichstände, Sperren, Basiswerte und Rüstungsboni. Ausgeführt in einer eigenen Kopie der Kern-Dateien und öffentlichen Kampfdefinitionen, ohne Engine-Server oder Spielstand.

Browsertests benötigen Playwright; `EDEN_PLAYWRIGHT_PATH` kann den vorhandenen Modulpfad setzen. `EDEN_SKILLS_SHOWCASE_URL` kann auf eine andere isolierte Showcase-Adresse zeigen.

## Level-Up-Zeremonie

Nach einem Kampf mit Aufstieg zeigt `eden-levelup.js` denselben Baum kompakt und bildschirmfüllend (Takt 3 der Zeremonie,
Regeln und Ablauf in `kampf.md` unter „Level-Aufstieg und Attributpunkte“). Er nutzt die Symbole und Pfadbilder dieses
Plugins (`EdenSkills.iconHtml`, `EdenSkills.icons`) und den vorhandenen Animations-Player.

## Designreferenzen

Die Trennung zwischen Skill-Auswahl und Erwerb ist auch im offiziellen [Mirage-Ablauf](https://www.ubisoft.com/en-au/help/assassins-creed-mirage/gameplay) beschrieben. Die [Beschreibung des Hades-II-Arcana-Menüs](https://www.destructoid.com/hades-2-arcana-cards-how-they-work-and-how-to-get-more/) zeigt eine kompakte Auswahlfläche mit zugehöriger Detailansicht. Edens horizontale Pfade, Detailreiter und Größenanpassung sind die eigene Umsetzung für die vorhandenen 16 Skills; keine Spielgrafiken wurden daraus übernommen.

## Status

Geschrieben: PC-Board, Symbole, Erklärungen, Lernprognosen und Player.
Eingebaut: Client-/Engine-Quellcode und separater Showcase auf Port 8337.
Getestet: obige Prüfungen ohne Live-Spielstand. Laufende Engine nicht neu gestartet, keine Regeln geändert. UI, Tests und benötigte Vorschau-Dateien werden gemeinsam lokal committed; kein Push. Mobile Optimierung ist nicht Bestandteil dieses PC-Entwurfs.
