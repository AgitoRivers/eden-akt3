# L3 Doppelschnitt · Doppio Gioco

Die Arbeitsnamen und Kürzel stammen aus docs/wiki/systeme/kampf.md (22.10.2026). Spielnamen und IDs bleiben bestehen.

Drei Varianten verwenden eine eigene violette, gerade Klingentextur mit unverändertem Alpha. Lange, flache Spuren wischen durch das Ziel. Zwei getrennte Kontakte mit Hurt, örtlichem violettem Körperreflex und Rückstoß; der zweite Treffer reagiert stärker. Keine vorbereitende Klingenspur links. Die Varianten unterscheiden sich weiter in Richtung und Rhythmus.

Bildbearbeitung: eingebautes OpenAI-Bildwerkzeug, keine neue JangaFX-Simulation. Asset: assets/realismus-v3/stahl-doppio-violett-v1.png. Exakter Prompt und Herkunft: quellen/doppio-violett/.

Nur Effektlabor und isolierte Vorschau auf Port 8337. Keine Änderung an Kampfregeln oder Live-Spiel. Frühere Dateien im Quellenordner gesichert.


## Körperladung statt Waffenladung

Geschrieben: Violette Ladung an Oberkörper und Schultern. Bewegte, weich auslaufende Energie mit einziehenden Partikeln, keine Kugel und keine gezeichneten Ringe. Die spezielle Säbelfärbung und sämtliche Klingenmasken wurden auf Nutzerwunsch entfernt: Ausrüstung kann wechseln.

Eingebaut: Alle drei Doppio-Varianten im isolierten Effektlabor. Das Modul doppio-ladung.js verwendet eine normalisierte Oberkörperposition aus Bildgröße, Skalierung und Fußanker statt Waffenkoordinaten. Die Ladung bewegt sich im Koordinatensystem der jeweiligen Pose. Ihr Verlauf bleibt gleich: Aufbau, Teilentladung, kurze erneute Verdichtung, zweite Entladung und vollständiges Erlöschen. Treffer, Schadenswerte und Posenzeiten unverändert. Originalbilder und Kampf-Testdateien unverändert. Vorherige Waffenladung unter quellen/doppio-koerper-v2 gesichert.

Grenze: Die Oberkörperposition wird aus Bildproportionen abgeleitet, nicht automatisch anatomisch erkannt. Keine neue JangaFX-Simulation oder KI-Grafik.

Getestet: Drei Varianten in je drei Phasen; Körperpixel verändert sich durch die Ladung, geprüfter Klingenpixel bleibt unverändert. Bestehende Doppio-Prüfung bestätigt beide violetten Kontakte und Hurt in allen Varianten. Ladung am Körper visuell geprüft, keine Browserfehler. Beide Vorschaukopien synchron.


Ladezeit verlängert: Freisetzungszeit von 1,65 auf 2,85 Sekunden, also 1,2 Sekunden mehr Vorbereitung. Sichtbare Körperladung rund 2,6 statt 1,4 Sekunden. Beide Schnittabstände, Wischdauer, Hurt und Rückstoß unverändert; gemeinsame Zeitpunkte verschieben Figur, Energie und Kontakt zusammen. Nur Effektlabor. Vorheriger Stand unter quellen/doppio-ladezeit-v3 gesichert.
