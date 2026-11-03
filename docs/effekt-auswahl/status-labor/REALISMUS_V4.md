# Spezialangriffe: größere Schnitte und bewegte Nachläufe

## Geschrieben

- Klingenspuren: 32 Prozent länger, 12 Prozent stärker; zeitliche Pulsbreite von 0,075 auf 0,115 Sekunden erhöht. Die tatsächliche sichtbare Dauer hängt von Transparenz und Hintergrund ab. Keine breiten gezeichneten Bänder ergänzt.
- Wasser: weichere Ausblendung der Seiten sowie des oberen und unteren Randes; überlagerte animierte Gischt aus dem vorhandenen freien Rauchmaterial. Die Wassergrundlage ist weiterhin ein statisches generiertes Material, im Browser verformt. Kein neu berechneter Flüssigkeitsfilm.
- Wind und Treffer: zusätzliche zeitlich begrenzte Druckwolke aus der mit IlluGen gelieferten animierten Textur `explosion_flipbook_2.png` (4 × 4 Bilder). Kein neuer nativer Export. Originalpfad und Prüfsumme stehen in `quellen/native-v4/materialquelle.json`; Nutzung hier als lokale Materialstudie. Eine Weitergaberegelung wurde nicht gesondert geprüft.
- Licht und fallende Lichtangriffe: eigener bewegter Dunst beziehungsweise Drucknachlauf.
- Alle zwölf Angriffe behalten drei verschiedene Abläufe. Die bisherigen Rückmeldungen bleiben erhalten.

## Eingebaut

Nur das Effekte-Labor und seine getrennte Vorschau auf Port 8337. Betroffene Dateien: `spezial-realismus.js`, `labor.js`, `index.html`, `assets/druckstoss.png` sowie Quellen und diese Dokumentation. Kein Einbau in den laufenden Kampf.

Die vorherige Schnittfassung liegt unter `quellen/realismus-v3/spezial-v3-vor-groesseren-schnitten.js`. HTML und Einbindung vor dieser Fassung liegen unter `quellen/native-v4`.

## Getestet

Der vorhandene Browsercheck `work/status-labor/realismus_pruefen.cjs` wurde gegen die isolierte Vorschau ausgeführt:

- zwölf Angriffe, 36 unterscheidbare Varianten, jeweils sieben Zeitpunkte;
- dritte Auswahl und Notiz bleiben nach Neuladen erhalten;
- heruntergeladene Rückmeldung enthält die drei Varianten;
- Pausieren, Abspielen, Zeitregler, heller Hintergrund und ausgeblendete Figur;
- schmale Ansicht mit 699 Pixeln, keine Browserfehler.

Die Bilder für Schnitt, Welle, Flut und Wind wurden zusätzlich angesehen. Die Prüfung bestätigt die Vorschaufunktion, keine Qualität auf dem Niveau eines fertigen Action-RPGs.

## Native Werkzeuge: aktueller Stand

LiquiGen 1.2.1 öffnet die mitgelieferten Projekte. Ein begrenzter Probeexport von `wave_maker_1.liquigen` mit 64 Bildern und einem 2048-Pixel-Bilderbogen wurde in `quellen/native-v4` begonnen. Die zuletzt geprüfte PNG-Datei war leer (0 Byte) und wurde nicht in die Vorschau übernommen. Danach schlug das Aktivieren des LiquiGen-Fensters mit einem Timeout fehl, auch nach erneutem Erkennen des Fensters. Ob der Export noch läuft, ist nicht bestätigt. Die installierte Vorlage wurde nicht gespeichert oder überschrieben.

EmberGen zeigt in seiner Startansicht `No active license`. Es wurde kein Lizenzdialog bedient und kein EmberGen-Export erstellt. Für neue Feuer-, Explosions- und Rauchsimulationen muss der Benutzer die Lizenz beziehungsweise Testversion selbst aktivieren.

Ziel bleibt eine gemeinsame Bibliothek bewegter Bausteine für Wasser, Feuer, Rauch, Staub, Einschläge, Wind und Energie. Native Exporte müssen vor Übernahme auf echte Transparenz, Bildfolge, freien Rand und Laufzeit geprüft werden. Bestehende Materialstudien dürfen nicht als fertige Simulationen bezeichnet werden.
