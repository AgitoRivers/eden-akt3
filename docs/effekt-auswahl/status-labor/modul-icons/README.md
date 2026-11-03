# Eden Rise · Chip Art Kit

SVG-Studie vom 25.10.2026. Eigenständig gezeichnete Vektoren, keine generierten Rasterbilder, keine externen Grafikbibliotheken. Nur Darstellung; keine Änderung an Engine, Regeln oder Spielständen.

## Export

- `kategorien/`: zwölf Kategorien × Bronze, Silber, Gold.
- `chips/`: alle 72 aktuell katalogisierten Chips; Dateinamen entsprechen den Spiel-IDs.
- `symbole/kategorie-*`: zwölf Kategoriezeichen.
- `symbole/status-*`: sechs Zustandsvarianten; die Wasserwelle ist ein ergänzendes Zeichen, keine neue Spielfamilie.
- `symbole/abwehr-*`: sechs Abwehrvarianten, entsprechend dem bestehenden Katalog einschließlich Blendabwehr.
- `rahmen/`: Raute und Wappen mit drei Materialstufen.
- `slots/`: belegt, frei, gesperrt, unidentifiziert; runder Charm mit kurzem Band.
- `feedback/`: Hover, Auswahl und deaktivierter Zustand als eigene SVG-Beispiele.
- `raster/`: transparente, unbeschriftete 6×3-SVG-Bögen für Waffen, Jacken, Zustände und Abwehr. Auf der Webseite können diese auch als PNG exportiert werden. Beschriftungen stehen nur im HTML neben den Chips.
- `tokens.json` und `chip-tokens.css`: Palette, Maße, Abstände, Bewegung und Focus-/Motion-Regeln.
- `katalog.json`: Zuordnung der Bilder zu den aktuellen Spiel-IDs. Text und Rosi-Kommentare stammen aus dem bestehenden Katalog.
- `eden-chip-icons.zip`: sämtliche SVGs, Daten und das ausführbare lokale HTML-Labor. Kein externer Dienst, keine Telemetrie, kein externer Font-Download.

## Bildsprache

Glatte, geschlossene, flache Hardware. Ein leiser Verlauf ins fast Schwarze, dünne präzise Metallfassung, ein abgerundetes Linienzeichen. Eine einzelne Leiterbahn und eine kleine warme Reparaturbrücke am Rand zeigen Rosis Handarbeit. Keine Edelsteinfacetten, Runen, Lochmuster, Perforationen oder porösen Texturen. Die drei Punkte sind solide Statusmarken, keine Löcher.

Waffe = Raute, Jacke = Wappen. Die Kategorie wird durch Farbe UND ein eigenes Zeichen vermittelt. Bronze/Silber/Gold zeigen die Stufe zusätzlich zu einem, zwei oder drei aktiven Punkten. Die noch nicht aktiven Punkte bleiben solide grau. Gold leuchtet nur zurückhaltend an der Fassung; kein Partikelglitzer.

## Maßsystem

Iconboxen: 28 / 48 / 64 / 96 px. Grundzeichen auf 24×24, einheitliche Linie 1,8, runde Enden und Verbindungen. Feine Randdetails werden bei 28 px ausgeblendet, Zeichen und Punkte bleiben erhalten. Abstände: 4 / 8 / 12 / 16 / 24 / 32 px. Glasflächen mit Radius 24 px, weicher Hintergrundunschärfe und dünner Fassung. Akzent #d8bd86. Kategorien und Materialtöne stehen vollständig in tokens.json.

## Verhalten

Hover hebt um 3 px; Auswahl bekommt einen goldenen Rand, Fokus eine klare zusätzliche Kontur. Deaktiviert = 45 % Deckkraft. Freier Platz = gestrichelte Form und Plus; gesperrt = Lock-Symbol plus außenstehender Hinweis „Rosi, level 2“. Unbekannte Chips zeigen ein gezeichnetes Fragezeichen statt des Kategoriezeichens, keinen Namen im Chip. Der Charm erscheint erst nach „Erster Charm gefunden“ und hängt versetzt an einem kurzen Band.

Einsetzen: 120 ms Snap, 240 ms Randlicht. Der vorhandene freigegebene UI-Klick (`ui_klick_2.mp3`) wird auf Wunsch leise abgespielt. Ton startet nicht automatisch. `prefers-reduced-motion` schaltet Lift, Snap und Übergänge aus. Die Drop-/Klick-Demo schreibt nichts und setzt keine echten Module ein.

## Typografie und Text

Namen: Bricolage-artige Display-Proportionen mit lokalem Trebuchet-/System-Fallback. UI-Texte: Systemschrift. Keine Schrift in den SVG-Chipbildern. Der Name, Kategorie, Stufe, einzeilige Wirkung und Rosis Kommentar stehen in der Tooltip-Karte daneben. Die Familiendaten kommen aus `module/eden_rise/erweiterungen.json`; es werden keine zusätzlichen Wirkungen erfunden.

Gestaltung und Varianten brauchen noch Ducs visuelle Freigabe. Kein Commit automatisch erstellt.
