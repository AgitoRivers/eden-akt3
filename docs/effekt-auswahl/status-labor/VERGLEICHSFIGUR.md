# Größerer Riss und Vergleichsfigur

Der Bodenbruch zeichnet jetzt mit 480 × 112 statt 340 × 78 Vorschau-Pixeln,
also rund 40 Prozent breiter. Die Perspektive bleibt flach; Rütteln und
Schutzpose von Erschüttert bleiben erhalten.

Auf Zustands-/Reaktionsseite und in der gemeinsamen Spezialattacken-Vorschau
gibt es eine Auswahl „Vergleichsfigur“. Standard ist eine vorhandene Anzugfigur
mit vollständigen Normal-, Schutz- und Hurt-Posen. Der bisherige Dieb bleibt
auswählbar. Alle drei Posen werden vor einem Wechsel vollständig geladen.
Die Auswahl wird lokal gemerkt und zwischen den Vorschauseiten übernommen.
Beim Wechsel werden die poseabhängigen Konturen neu aufgebaut.

Die Auswahl gilt auf den Vergleichsseiten für den neuen Entwurf; links bleibt
die bisherige Referenz. Auf der gemeinsamen Angriffsbühne gilt sie für die
gesamte dargestellte Figur. Keine Änderungen am echten Spiel oder dessen Assets:
die verwendeten Bilder liegen als Kopien unter `assets/vergleich_*.webp`.
Ein erster Kandidat mit abgeschnittenen Beinen wurde verworfen und gesichert.

Geschrieben/eingebaut: `figur-auswahl.js`, die beiden Vorschauseiten und ihre
Renderer; drei Bildkopien. Sicherungen unter `quellen/vergleichsfigur/`.

Getestet: neun Zustände/Reaktionen mit passenden Posen der neuen Figur,
Spezialattacken mit Hurt und Schutz, Umschalten in beide Richtungen,
bildgleiche Rückkehr zur ersten Auswahl, gespeicherte Wahl nach Neuladen und
Seitenwechsel, schmale Darstellung. Keine Browser- oder Ladefehler.
Bodenriss und vollständige Figur in beiden Ansichten zusätzlich visuell geprüft.
