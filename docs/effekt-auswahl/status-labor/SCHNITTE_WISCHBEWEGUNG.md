# Schnitte als Wischbewegung

Geschrieben: Der bisherige Helligkeitspuls wurde durch eine wandernde Materialspur ersetzt. Die fotografische Stahltextur bewegt sich entlang der Schnittachse durch das Ziel und verlässt die Bahn mit einem kurzen Schweif. Die Transparenz wird nicht mehr als zeitlicher Einblendpuls gesteuert. Eine weiche räumliche Maske begrenzt den Ein- und Austritt.

Die zusätzliche Längenskalierung wurde entfernt. Die Höhe beträgt jetzt das 4,5-Fache des ursprünglichen Höhenparameters statt zuletzt das 1,4-Fache; die tatsächliche sichtbare Stärke hängt von der Transparenz der Materialtextur ab. Ziel ist eine höhere, kräftigere Spur. Nebel, Blitz, Wasser und Treffer wurden nicht geändert.

Eingebaut: Die gemeinsame Schnittfunktion in `spezial-realismus.js` gilt für die drei Varianten von Doppelschnitt, Vendetta und dunklem Schnitt. Die Cache-Version in `index.html` wurde erhöht, die isolierte Vorschau auf Port 8337 aktualisiert. Vorherige Fassung unter `quellen/native-v4/spezial-vor-wischbewegung.js` gesichert. Kein Einbau in den laufenden Kampf.

Getestet: Browserprüfung mit `--disable-gpu` und `--disable-gpu-compositing`. An drei Zeitpunkten bewegt sich der Schwerpunkt der tatsächlichen Spur von x=138,8 über x=181,0 nach x=266,8 im Hilfsbild. Damit ist eine räumliche Bewegung nachgewiesen. Keine Browserfehler. Die drei gerenderten Phasen wurden zusätzlich visuell geprüft. Prüfsystem: `work/status-labor/wischen_pruefen.cjs`, Bild `work/status-labor/schnitt-wischfolge.png`. Keine Simulation oder GPU-Exporte gestartet.
