# Prüfung der Effektauswahl

Stand: 22.10.2026.

## Geschrieben

- 81 Effekte aus der vorhandenen Inventur, je drei Varianten: 243 Auswahlentwürfe.
- 243 transparente PNG-Bilderbögen, je 24 Bilder: 5.832 Einzelbilder.
- 13 aufbereitete IlluGen-Vorlagenvorschauen mit dokumentierter Herkunft.
- HTML-Auswahl mit Suche, Bereichen, Priorität, Notizen, lokalem Speichern, Export und Import.

## Eingebaut

Alle Entwürfe sind in der eigenständigen Auswahlseite verfügbar. Das laufende Spiel wurde nicht verbunden oder geändert.
Es gibt keine 243 neu erstellten IlluGen-Produktionsprojekte. Die Bilderbögen sind Canvas-Vorschau-Aufbereitungen aus
Vorlagenvorschauen und Engine-Animationen. Produktionsauflösung, endgültige Exporte, Sound und Engine-Einbau stehen aus.

## Getestet

- In einer getrennten Kopie unter `work/effekte/testseite`, statischer Server nur auf 127.0.0.1:8337.
- 1.557 Aufrufe der Darstellung mit verschiedenen Zeiten, Varianten, Zielen, Bühnen und Ausprägungen: keine ungültigen
  Zeichenkoordinaten. Dieser Teil nutzt eine nachgebildete Canvas-Schnittstelle und prüft die Aufruflogik.
- Alle 243 Bilderbögen zusätzlich mit echtem Canvas-Bildexport erzeugt und danach als PNG geprüft:
  RGBA, 1536 × 784 Pixel, transparente Bereiche und sichtbare Inhalte. Alle 81 Dreiergruppen unterscheiden sich.
- Jeder Bilderbogen enthält mindestens drei unterschiedliche und mindestens vier sichtbare Einzelbilder.
- Auswahl, Notizen, Suche, Nur-offene-Filter, Export/Import und Zurückweisen ungültiger Auswahldateien geprüft.
- Reduzierte Bewegung: ruhige Vorschau bis zur bewussten Freigabe geprüft.
- Im Browser Auswahl und Notiz gesetzt und nach Neuladen wiedergefunden, anschließend die Prüf-Auswahl aufgehoben.
- Browser-Sichtprüfung repräsentativer Effekte; Kontaktübersichten aller 81 Effekte geprüft.
- Ein Schriftproblem im nativen Vorschau-Export wurde bei der Sichtprüfung erkannt und korrigiert. Kleine isolierte
  Lichtflecken wurden bei der Aufbereitung unterdrückt.
- Keine Änderungen an den installierten IlluGen-Vorlagen; ihre Prüfsummen entsprechen den dokumentierten Quellen.
- Keine Tests mit echten Spielständen, keine Modell- oder API-Aufrufe, keine Commits und kein Push.

Die Bedienprüfung bestätigt die Vorschau. Sie ersetzt keinen späteren Test der gewählten Produktions-Effekte im Kampf.
