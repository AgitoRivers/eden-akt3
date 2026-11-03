# L3 Doppelschnitt · Doppio Gioco

Die Arbeitsnamen und Kürzel stammen aus docs/wiki/systeme/kampf.md (22.10.2026). Spielnamen und IDs bleiben bestehen.

Drei Varianten verwenden eine eigene violette, gerade Klingentextur mit unverändertem Alpha. Lange, flache Spuren wischen durch das Ziel. Zwei getrennte Kontakte mit Hurt, örtlichem violettem Körperreflex und Rückstoß; der zweite Treffer reagiert stärker. Keine vorbereitende Klingenspur links. Die Varianten unterscheiden sich weiter in Richtung und Rhythmus.

Bildbearbeitung: eingebautes OpenAI-Bildwerkzeug, keine neue JangaFX-Simulation. Asset: assets/realismus-v3/stahl-doppio-violett-v1.png. Exakter Prompt und Herkunft: quellen/doppio-violett/.

Nur Effektlabor und isolierte Vorschau auf Port 8337. Keine Änderung an Kampfregeln oder Live-Spiel. Frühere Dateien im Quellenordner gesichert.


## Säbelladung

Geschrieben: Neues Modul ablaufprobe/doppio-ladung.js. Violette Energie liegt direkt auf den Klingenflächen der vorhandenen Posen windup, attack und heavy_attack. Posebezogene Masken in den Originalbildkoordinaten behalten die Metalltextur; weicher Saum, ein wandernder Lichtreflex und wenige einziehende Partikel unterstützen die Ladung. Die Masken sind auf DucErdeSaebel abgestimmt und müssen bei anderen Waffenbildern neu angepasst werden.

Die Energie steigt vor dem ersten Schnitt an, fällt mit dessen sichtbarem Beginn teilweise ab, verdichtet sich zwischen den Hieben erneut und klingt nach dem zweiten Wischer vollständig aus. Die beiden Treffer und ihre Schadenswerte bleiben unverändert. Keine zusätzliche fliegende linke Slash-Grafik und keine frei schwebende Kugel.

Eingebaut: In allen drei Varianten über die gemeinsame Duc-Zeichenroutine; Energie und Pose werden im selben Koordinatensystem einschließlich Skalierung, Vorstoß und kurzer Überblendungen gezeichnet. Nur isoliertes Effektlabor auf Port 8337. Originalbilder und Kampf-Testdateien unverändert. Vorheriger Stand unter quellen/doppio-ladung-v1 gesichert. Keine neue JangaFX-Simulation oder KI-Bildgenerierung.

Getestet: Alle drei Varianten in fünf Phasen, Energieabfall nach dem ersten Schnitt, erneute Verdichtung und vollständiges Erlöschen nach dem zweiten Schnitt. Bilder von Ladung, Rückholbewegung und zweitem Kontakt visuell geprüft. Bestehende Doppio-Gegenprobe bestätigt sechs Kontakte mit violettem Material und Hurt. Keine Browserfehler. Repo und bediente Kopie synchron.
