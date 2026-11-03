# Berserker-Spezialangriffe im Effekt-Labor

Quelle: docs/wiki/systeme/kampf.md, Abschnitt Alle 16 Spezialangriffe, Stand v5 vom 23.10.2026. Eingebaut am 24.10.2026 ausschließlich in der isolierten Vorschau auf Port 8337. Kein Kampfrechnen und kein Live-Spiel geändert.

- M3 Scirocco: ein Treffer +4 und eine Brandstufe; danach ungedeckt. Drei verschiedene Hiebrichtungen.
- M5 Retour de Flamme: voller gegnerischer Spezialtreffer mit Ducs eigener Hurt-Pose; anschließend feuriger Gegenschlag, beide mit einer zusätzlichen Brandstufe. Die Vorschau zeigt den starken Spezialangriff. Regeltext nennt auch die schwache Variante.
- M7 Furia: kürzere Vorbereitung für den sofortigen Auftakttreffer. Danach Feuer und Funken am Körper als Rauschzustand. Zwei Runden ×1,3 und weitere Brandstufen je Treffer sind im Regeltext erklärt, nicht als zusätzliche Treffer erfunden.
- M9 Vulcano: 1–5 Brandstufen per eigener Auswahl. Genau ein Schlag pro gewählter Stufe, Abstand 0,48 Sekunden, eigener Rückholschwung und passende Hurt-Reaktion bei jedem Kontakt. Danach Aussetzen im Hinweistext. Ohne Brandstufen wäre der jederzeit startbare Angriff wirkungslos; das Labor stellt nur 1–5 dar. Kein Live-Status wird verbraucht.

Geschrieben: berserker.js, vier Definitionen und vier Regelbeschreibungen, Timing und Ducs Hurt-Pose als verlustfreie Kopie. Neue Posen-Metadaten programmatisch serialisiert. Bestehende zwölf Regeltexte wurden nicht auf den neuen Gesamtstand umgeschrieben.

Eingebaut: Alle vier im Angriff-Dropdown, je drei Varianten, insgesamt sechzehn Spezialangriffe. Nur eigenes Labor und gespiegelter lokaler Serverordner.

Getestet: zwölf Varianten, achtzehn Kontakte mit Feuer, Gegner-Hurt und Angriffs-Pose, Ducs Hurt vor Retour, Vulcano für alle fünf Schlagzahlen, Effektschalter und Ladefehler. Screenshots von Treffern und Retour-Gegentreffer geprüft.

Material: vorhandenes assets/feuer.png, vorhandene fotografische Stahltextur, vorhandener nativer Trefferatlas. Neue 2D-Komposition und Partikel, keine neue JangaFX-Simulation. Ducs hurt.png stammt aus seinem vorhandenen DucErdeSaebel-Satz; Original bleibt unverändert.

Sicherungen des vorherigen Stands: quellen/berserker-v1. CRLF beibehalten. Keine Commits oder Pushes; fremde Änderungen an Engine, Spielständen, Karten und Kampfplan unangetastet.

Abschließende gemeinsame Prüfung: alle 16 Angriffe in 48 Varianten und 240 Phasen; Duc immer sichtbar, Selbst-Effekte am Angreifer, keine JavaScript- oder Ladefehler. Der ältere Testbericht benennt Varianten noch fest mit 36, seine tatsächlich durchlaufenen 240 Phasen entsprechen 16 × 3 × 5.

## Neuer Stand

Die erste Studie oben ist durch BERSERKER_FEUERPHASEN.md abgelöst: neue native EmberGen-Exporte, Feuerball statt Scirocco-Klinge, Feuersturm bei Vulcano, getrennte Konter-/Ladephase bei Retour und Brennzustand / Feuerpeitsche bei Furia.
