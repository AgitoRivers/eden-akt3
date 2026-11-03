# LiquiGen-Bildfolge eingebaut

## Geschrieben

Der inzwischen abgeschlossene Export `quellen/native-v4/wave_maker_1_render_all_rasterizer_.png` ist lesbar: 2048 × 2048 Pixel, RGBA, 623821 Byte. Er enthält Wasser und mitgerenderte Beckengeometrie. Deshalb wird nicht der gesamte Export als Effekt gezeichnet.

Aus den letzten 32 Bildern wurden der Wasserbereich ausgeschnitten, beige Beckenteile transparent gesetzt und die Ränder weich ausgeblendet. Alle 32 aufbereiteten Bilder unterscheiden sich. Der ursprüngliche Export bleibt unverändert. Quelle, Prüfsumme, Zuschnitt und Bildaufteilung sind in `quellen/native-v4/liquigen-integration.json` dokumentiert.

Das Ergebnis `assets/liquigen-welle.png` hat acht Spalten und vier Reihen mit 128 × 96 Pixeln je Bild. Die Originalaufnahme zeigt das Wasser nur klein in einer weiten Kameraansicht; entsprechend ist die Detailauflösung begrenzt. Diese Integration ersetzt keinen späteren Export mit besserer Kamera und ausgeschalteter Beckengeometrie.

## Eingebaut

`spezial-realismus.js` spielt die tatsächliche Bildfolge mit weichem Übergang zwischen aufeinanderfolgenden Bildern ab. Die verformte statische Wasserquelle wird dabei nicht mehr verwendet oder geladen.

- Welle: alle drei Varianten.
- Flut: alle drei Varianten, einschließlich der Ebene hinter der Figur.
- Ruhiges Wasser: erste Variante. Die beiden weiteren Varianten bleiben wie bisher reine Nebelabläufe.

Die drei Varianten behalten ihre unterschiedlichen Richtungen, Größen und Zeitversätze. Die übrigen Angriffe und gespeicherte Rückmeldungen bleiben bestehen. Einbindung über `labor.js`, Cache-Version in `index.html` erhöht. Vorherige Dateien liegen unter `quellen/native-v4/*.vor-liquigen`.

Eingebaut ist die Vorschauseite auf Port 8337. Kein Einbau in den laufenden Spielkampf, keine Spielstandänderungen.

## Getestet

Bildaufbereitung ausschließlich mit Pillow auf der CPU; keine neue Simulation und kein neuer GPU-Export.

Der Browsercheck `work/status-labor/liquigen_pruefen.cjs` startete Edge mit `--disable-gpu` und `--disable-gpu-compositing`. Er prüfte zwölf Angriffe und 36 Varianten an sieben Zeitpunkten, die Speicherung der dritten Auswahl, heruntergeladene Rückmeldungen, Pause und Abspielen, Zeitregler, Hintergrundwechsel, ausgeblendete Figur und schmale Ansicht. Keine Browser- oder Ladefehler. Die eingebauten Flutbilder wurden zusätzlich visuell geprüft.

Der Export ist damit eingebaut und funktional geprüft. Die geringe Detailauflösung ist weiterhin eine sichtbare Einschränkung; keine Qualitätsfreigabe für den endgültigen Kampf.
