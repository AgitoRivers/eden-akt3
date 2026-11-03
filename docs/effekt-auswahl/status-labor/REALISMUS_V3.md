# Spezialangriffe: drei Varianten mit natürlichen Materialien

Stand: 22.10.2026.

Geschrieben: 12 Angriffe mit je 3 einzeln abgestimmten Abläufen. Der Renderer spezial-realismus.js verwendet Rastermaterialien statt der breiten gezeichneten Schnittbänder. Klingenspuren bleiben kurz und schmal. Unterschiede betreffen Richtung, Reihenfolge, Stärke, Materialeinsatz und Nachlauf. Die Namen und Beschreibungen stehen im Renderer unter defs.

Eingebaut: ausschließlich in der Vergleichsvorschau docs/effekt-auswahl/status-labor. Drei Varianten, gemeinsame Zeitleiste, Wiedergabe, große Vorschau bei schmalem Fenster, eigener Bewertungsspeicher v3 und Export einschließlich der drei Variantennamen. Vorherige Dateien und Bewertungen sind erhalten. Keine Kampfintegration und keine Regeländerungen.

Getestet: isolierte Kopie auf Port 8337 in Edge. 36 verschiedene Bildausgaben; jede Variante an sieben Zeitpunkten geprüft. Dritte Variante wählen, Notiz, Neuladen und JSON-Inhalt des Downloads geprüft. Reduzierte Bewegung, heller Hintergrund, ausgeblendete Figur und schmale Ansicht mit 699 Pixeln geprüft. Keine Browser- oder Ladefehler. Zustands- und Reaktionsprüfungen weiterhin erfolgreich. Kontaktbögen aller 36 Vorschläge gesichtet.

## Bildgenerierung

Eingebaute OpenAI-Bildgenerierung, kein CLI-Fallback und kein Zugriff auf API-Schlüssel. Das Werkzeug hat keine konkrete DALL-E-Modellversion ausgewiesen. Drei statische Ausgangsmaterialien wurden erzeugt und mit ihrer ursprünglichen Transparenz unverändert kopiert:

- X:/AI/Eden/docs/effekt-auswahl/status-labor/assets/realismus-v3/stahl.png
- X:/AI/Eden/docs/effekt-auswahl/status-labor/assets/realismus-v3/wasser.png
- X:/AI/Eden/docs/effekt-auswahl/status-labor/assets/realismus-v3/licht.png

Die vollständigen Prompts liegen in quellen/realismus-v3/PROMPTS.md. Unveränderte Originalkopien und Prüfsummen liegen daneben. Bounding-Boxes für die Darstellung werden aus den Alphakanälen ermittelt, die Bilddateien selbst bleiben unverändert. Die Bewegungen werden im Browser aufgebaut. Die Wasserverformung ist eine Materialanimation, keine physikalische Flüssigkeitssimulation. Es wurden keine 36 KI-Videos oder IlluGen-Simulationen erzeugt.

## Bibliothek

[Kenney Particle Pack](https://kenney.nl/assets/particle-pack), CC0. Heruntergeladen wurde das Originalarchiv vom Anbieter. Die mitgelieferte License.txt erlaubt persönliche und kommerzielle Verwendung. Die Vorschau verwendet flare_01.png als kleinen Trefferglanz und trace_04.png als kurze Schussspur. Archiv und Lizenz liegen unter quellen/realismus-v3; der Renderer greift auf die projektlokalen Kopien zu. Es wurde keine fremde Software installiert oder gestartet. Vorhandener IlluGen-Rauch wird weiterverwendet; nicht geprüfte Discord-Projekte wurden nicht übernommen.

## Grenzen und fremde Arbeit

36 visuelle Auswahlentwürfe; die künstlerische Bewertung steht Duc zu. Noch kein Ton und keine Verbindung zu echten Schadensereignissen. Eine Funktionsprüfung bestätigt nicht automatisch Realismus. Die währenddessen offenen Änderungen von Claude an Engine, Musik, Kampfkarten und Werkzeugen wurden nicht überschrieben oder committet. Kein Push, keine Spielstände geändert.
