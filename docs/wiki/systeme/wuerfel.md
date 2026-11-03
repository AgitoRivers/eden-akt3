# Eden Dice 1.0 — Übergabe an Claude

Stand: 18.10.2026. Ausgangspunkt: Eden-Engine `master`, Commit `ad688e0`.

## Vereinbarte Darstellung

Jede sichtbare Probe erhält den goldenen Würfel. Gewöhnliche Proben laufen ungefähr 0,8 Sekunden direkt im vorhandenen Dialog-, Missions- oder Ereignisbereich. Besonders markierte Herausforderungen werden groß gezeigt. Eine gewertete natürliche 20 oder 1 wird standardmäßig ebenfalls groß gezeigt, unabhängig von der Bedeutung der Aufgabe. Die frühere feste 85:15-Verteilung gilt nicht mehr.

- Natürliche 20: verzierter Sonnenanker, Sonnenstrahlen und goldene Lichtpartikel.
- Natürliche 1: gebrochener Anker vor Feuer, Glut, Funken und dezenter Rauch.
- Normaler Erfolg/Fehlschlag: nummerierte Original-Würfelfläche, keine kritischen Effekte.
- Bei Vorteil zählen beide tatsächlichen Würfe; der höhere wird hervorgehoben. Eine verworfene 1 erzeugt keinen Patzer-Effekt.
- Erscheinungsbild: Deck Glass Noir. Das Modul übernimmt die CSS-Variablen der Engine für Rauchglas, Champagner, Schrift und Ergebnisfarben. Kein grünblauer eigener Hintergrund.
- Große Würfe dauern etwa 1,95 Sekunden; kritische Hintergrundeffekte können danach noch ungefähr eine Sekunde ausklingen. Überspringen/Weiter und Escape sind vorhanden. Der kompakte Wurf wartet nicht auf eine Bestätigung.
- Reduzierte Bewegung: Ergebnis sofort, ohne Rollanimation oder Hintergrundeffekte.

Die Wirkung der Animation liegt ausschließlich in der Darstellung. Energie, Geld, Vertrauen, Konsequenzen, Proben und Spielstände werden nicht geändert.

## Dateien und Zuständigkeit

| Datei | Aufgabe |
|---|---|
| `client/plugins/eden-dice/eden-dice.js` | Öffentliche Client-API, kompakt/groß, Vorteil, Bilder, Überspringen, Wiederholschutz, statische Loganzeige |
| `client/plugins/eden-dice/eden-dice.css` | Auf den Engine-Stil abgestimmte, gekapselte Darstellung |
| `client/plugins/eden-dice/eden-dice-effects.js` | Endliche Canvas-Effekte hinter dem großen Würfel |
| `client/plugins/eden-dice/assets/` | 18 nummerierte Atlanten (2–19), zwei freigegebene Anker-Endbilder, gemeinsamer Rollatlas |
| `kern/wuerfel_anzeige.py` | Request-lokaler Sammler und modulbezogene Präsentationskonfiguration |
| `kern/wuerfel.py` | Ein zusätzlicher Aufruf `merken(p)` nach der unveränderten Berechnung |
| `eden.py` | Gesicherte Dateiroute und Ausgabe der Hinweise in der erfolgreichen POST-Antwort |
| `client/index.html` | Lädt das Plugin; wartet vor Ergebnisdarstellung und Stimme auf die Animation; wertet alte Logs statisch auf |
| `module/eden_rise/wuerfel_anzeige.json` | Handgepflegte, optionale Sidecar-Konfiguration; keine generierte Storydatei |

Der Engine-Kern enthält keine neuen Figuren- oder Ereignisnamen. Die Auswahlliste für Eden Rise liegt nur im Sidecar. Andere Module funktionieren ohne diese Datei mit kompakten normalen Würfen und großen natürlichen 1/20.

## Ablauf im echten Client

1. Eine Spieleraktion wird wie bisher als POST gesendet.
2. Während dieser Anfrage sammelt ein `ContextVar` die Ergebnisse von `wuerfel.probe`. Außerhalb einer solchen Anfrage ist der Sammler wirkungslos. `wuerfel.verdeckt` wird nicht erfasst.
3. Die ursprüngliche Spiellogik läuft vollständig durch und speichert wie bisher. Nur bei Erfolg der Anfrage wird die Antwort um `wuerfel_anzeige` ergänzt.
4. Der Client hält die neue Antwort zurück und zeigt zunächst die vorhandenen Würfe mit dem Plugin im bisherigen UI an.
5. Danach übernimmt er die neue Antwort, zeigt Konsequenzen und startet die bisherige Ergebnisstimme. Es wurde keine zweite Ergebnisberechnung eingebaut.
6. Die bestehenden Zahlenkästchen `.wurf > .w` werden beim Rendern durch statische Würfelbilder ersetzt. Das erneute Öffnen eines Logs spielt nichts ab.

### Bewusste Einschränkung der ersten Version

Für Aktionen, bei denen ein Wurf möglich ist, übernimmt der Client während der laufenden POST-Anfrage keine Zwischenstände aus dem 1,1-Sekunden-Polling. Sonst würden Ergebnis und Stimme die Animation vorwegnehmen. Die Anfrage läuft weiterhin serverseitig; die Oberfläche zeigt ihren bisherigen Beschäftigt-Zustand. Bei längeren Modellantworten werden diese Antworten daher erst nach der Anfrage und Würfelanzeige sichtbar. Andere Aktionen behalten das bisherige Live-Polling.

Betroffene Aktionen: `zug`, `waehlen`, `geste`, `job`, `event_wahl`, `kochen`, `verabredung_ort`. Wenn später ein weiterer sichtbarer Probentyp hinzukommt, muss er im Backend-Sammler und im Polling-Schutz ergänzt werden.

## Öffentliche JavaScript-API

```js
await EdenDice.play({
  version: 1,
  run_id: 'opaque-run-id',
  policy: { kritisch_gross: true, effekte: true },
  rolls: [{
    id: 'unique-request:0',
    titel: 'Eine riskante Reparatur',
    modus: 'kompakt', // oder 'gross'
    probe: {
      attribut: 'cunning', sg: 12,
      wuerfe: [16], wurf: 16,
      boni: [['Cunning', 2]], summe: 18,
      ergebnis: 'erfolg'
    }
  }]
}, { target: document.querySelector('.missinfo') });

EdenDice.enhance(document); // vorhandene Ergebnisstreifen, ohne neue Animation
EdenDice.cancel();          // aktuelle Animation abbrechen und ausstehende alte Reihe beenden
```

Ohne geeignetes Ziel erscheint der kompakte Wurf unten als kleine schwebende Karte. Die API erzeugt keine Zufallszahlen. Sie validiert Würfe und verwendet Textknoten für Datenbeschriftungen. Ein ungültiger Hinweis wird übersprungen; das Spielergebnis wird trotzdem dargestellt.

Mehrfach zugestellte IDs werden in der aktuellen Seite dedupliziert. Beim Seitenneuladen wird nicht wiederholt, weil GET-Antworten grundsätzlich keine Animationshinweise enthalten. Es gibt kein persistentes Würfel- oder Fortschrittsfeld im Spielstand. Die API ist kein Schutz gegen das erneute Absenden einer echten Spieleraktion; diese bleibt Aufgabe der Engine.

Vor dem Laden können bei Bedarf Optionen gesetzt werden:

```js
window.EdenDiceOptions = {
  compactMs: 800,
  largeMs: 1950,
  assetBase: '/plugins/eden-dice/assets/'
};
```

Fehlende oder nicht ladbare Bilder ersetzen die Darstellung durch die korrekte Würfelzahl. Ein Bildladeversuch hat ein Zeitlimit von 1,8 Sekunden. Das blockiert die Konsequenzen nicht dauerhaft.

## Backend-Protokoll

`wuerfel_anzeige` ist ein zusätzliches Top-Level-Feld der erfolgreichen POST-Antwort, kein Feld von `z`. Es enthält ausschließlich die gerade erzeugten sichtbaren Spielerproben. GET `/api/stand` enthält dieses Feld nicht. Die IDs sind zufällige Anfragekennungen, keine Fall- oder Spurenkennungen. Die Erzeugung der Kennung verbraucht keinen Zufall aus dem Spielwürfel-Generator.

Die Dateien werden über `/plugins/eden-dice/…` ausgeliefert. Der Handler löst Pfade auf und erlaubt nur Dateien innerhalb dieses Plugin-Verzeichnisses sowie die Endungen `.js`, `.css`, `.webp`. Konfiguration, Pythondateien und beliebige andere Pfade werden nicht ausgeliefert.

## Auslöser ändern

`module/eden_rise/wuerfel_anzeige.json`:

```json
{
  "version": 1,
  "aktiv": true,
  "kritisch_gross": true,
  "effekte": true,
  "gross": {
    "ereignisse": ["ereignis_id"],
    "missionen": ["mission_id"],
    "szenen": ["szene_id"]
  }
}
```

`gross` ändert keine Probe. In einem markierten Ereignis erscheint nur dann ein Würfel, wenn die gewählte Antwort bereits eine Probe hat. Fehlt die Sidecar-Datei, gelten die Standardwerte. `aktiv:false` unterdrückt neue Animationshinweise; die statischen goldenen Würfelbilder im Log bleiben erhalten. `kritisch_gross:false` erlaubt kritische Ergebnisse kompakt, falls die jeweilige Aktion nicht ohnehin groß markiert ist. `effekte:false` schaltet den Hintergrundeffekt aus.

Anfangsauswahl: 17 besondere Ereignisse und drei Missionen. Das ist eine Inhaltsauswahl, keine Quote pro Durchlauf. Normale sichtbare Proben sind ebenfalls animiert.

## Assets

Die Rollbewegung ist eine 2D-Spriteanimation, keine physikalische 3D-Simulation. Der gemeinsame Atlas enthält 61 benutzte Bilder in einem 8×8-Raster. Die nummerierten Atlanten besitzen 18 benutzte Bilder in einem 5×4-Raster. Ein Frame misst ursprünglich 256×256 Pixel. Die Anker-Endbilder sind hochauflösend neu ausgearbeitet (1254×1254, transparente Hintergründe), keine neu gerenderten vollständigen Rollsequenzen. Beim Übergang zum Endbild ist ein Schnitt zwischen gemeinsamem Rollen und gewählter Ergebnisfläche vorgesehen.

Die originalen Würfel und die Rollbewegung stammen aus dem vom Nutzer bereitgestellten „Golden Death Dice Alt“-Paket, Autor laut Metadaten: RubenLime. Die neuen freigegebenen Sonnen- und Feueranker wurden mit Imagegen erstellt. Die Assetdateien werden über das Plugin ausgeliefert und benötigen keinen externen Dienst. Die tatsächlichen Engine-Schriften sind weiterhin Sache des vorhandenen Clients; das Plugin lädt keine weiteren Schriften.

## Prüfen

Vom Engine-Verzeichnis aus:

```powershell
python tests/test_wuerfel_anzeige.py
python tests/test_wuerfel_http.py
python tests/lauf_test.py
python tests/lauf_test.py --seed 3
python werkzeuge/eden_rise/story_pruefen.py
node tests/eden_dice_browser.cjs
```

Der Browsertest benötigt Playwright und einen installierten Edge. `PLAYWRIGHT_MODULE` kann auf eine bestehende Playwright-Installation zeigen. Playwright ist nur eine Testabhängigkeit; das Plugin selbst hat keine Paketabhängigkeiten. Der HTTP-Test und die Wochenläufe verwenden Wegwerf-Konfigurationen und Spielstände. Nicht `--speichern` verwenden: Die Referenz wurde nicht verändert.

Geprüft werden unter anderem: unveränderte Würfel/RNG-Aufrufe, Request-/Thread-Isolation, verdeckte Proben, Vorteil, ausgewertete natürliche 1/20, Summe 20 ohne natürliche 20, doppelte Zustellung, Überspringen, Abbrechen, reduzierte Bewegung, fehlende Assets, mobile Breite und blockierte Dateipfade. Die beiden Wochenläufe stimmen exakt mit ihren vorhandenen Referenzen überein.

## Einstieg für Claude

1. Diese Datei und den mitgelieferten Git-Patch lesen. Vor Änderungen den aktuellen HEAD und `git status` prüfen.
2. Die vorhandene Integration weiterverwenden. Keine zweite Würfelberechnung oder konkurrierende Popup-Steuerung ergänzen.
3. Inhaltsauswahl im Sidecar ändern. Generierte `modul.json`, `story.json`, `ereignisse.json` und `missionen.json` dafür nicht bearbeiten.
4. Bei Änderungen an Anzeige oder Transport mindestens die Modul-, HTTP- und Browserprüfungen ausführen. Bei Kernänderungen zusätzlich die vorhandenen Wochenläufe und Storyprüfung.
5. Ein bereits laufender Pythonserver muss nach dem Update neu gestartet werden, damit er die neue Dateiroute und Transport-Erweiterung kennt. Der Benutzer führt diesen Neustart bei Bedarf aus; kein laufender echter Run wurde für die Installation beendet.

Die Übergabe umfasst das eigenständige Modul, die geprüfte Engine-Anbindung, Assets, Tests, eine lokale Demo und diesen Leitfaden. Die frühere Vorschau allein war noch keine vollständige Integration; dieses Paket enthält die Integrationsänderungen.
