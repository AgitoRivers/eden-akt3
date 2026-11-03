# Phare und Pluie d’Étoiles

Nur isoliertes Effektlabor auf Port 8337. Keine Kampfregeländerung und kein Zugriff auf Spielstände. Vorherige Ablaufdateien in quellen/licht-sterne-v1 gesichert. Andere offene Arbeiten bleiben unangetastet.

## Geschrieben

Gemeinsames Effektmodul ablaufprobe/licht-sterne.js. Phare verwendet Elfenbein und Gold: Suchscheinwerfer, zusammenlaufende Lichtspalten und gefächertes Gegenlicht. Zeitlich bewegte Dunststruktur, Lichtstreuung, schwebender Staub und warme Figurenreflexe. Die vorhandene rechte Figur steht als Ziel im Leuchtfeuer und zeigt die Schutzpose, keine Hurt-Reaktion. Laut Kampfplan setzt das Ziel einen Zug aus; die Vorschau führt diese Regel nicht aus.

Pluie d’Étoiles verwendet Saphirblau und Silber: zunehmend kräftige Dreierfolge, wechselnde schräge Flugrichtungen und fast gleichzeitige Konvergenz. Drei Kontakte pro Variante. Kurze Flugspuren mit hellem Kern, bewegte Staubfahnen und unregelmäßig verteilte Partikel. Jeder Kontakt erneuert Hurt und Rückstoß; bei der Dreierfolge setzt der letzte Kontakt den stärksten visuellen Akzent. Das verändert keine Schadenswerte.

## Eingebaut

Im gemeinsamen Vorschauablauf, einschließlich Variantenbeschreibungen und aktualisierten Dateiversionen. Repo und bediente Vorschaukopie synchron. Trefferzeiten werden von Effekt und Figurenreaktion gemeinsam verwendet. Keine linke Figur ergänzt.

Material: Licht und bewegter Staub entstehen im Browser aus vorhandener Rauschtextur. Die Sternentreffer verwenden zusätzlich den vorhandenen nativen Treffer-Bilderbogen assets/native-v6/treffer.png mit blauer Färbung auf einer separaten Zeichenfläche. Kein neuer JangaFX-Export, keine neue KI-Bildgenerierung, kein Mauszugriff.

## Getestet

Alle sechs Varianten in je fünf Phasen: Aufbau, Flug beziehungsweise Entfaltung, Kontakt, Höhepunkt und später Nachlauf. Phare ohne Hurt, mit Schutzpose; Sternsalve mit Hurt an jedem der drei Kontakte und längerem Hurt-Nachlauf. Unterschiedliche Variantenbilder und abschaltbare Effekte geprüft. Keine Browser- oder Ladefehler. Gerenderte Bilder von Licht und Einschlägen zusätzlich visuell geprüft. Renderaufrufe im Headless-Browser ohne GPU im Mittel ungefähr 18 ms; keine Zusage zur Bildrate im sichtbaren Browser.

Prüfskript: work/status-labor/licht_sterne_pruefen.cjs im Codex-Arbeitsordner.

Zusätzliche Gegenprobe: Mistral und Omertà weiterhin mit jeweils drei Varianten in zwölf Phasen ohne Browserfehler. Der neu gestartete statische Laborserver läuft mit unterdrückter Request-Ausgabe, damit die Ausgabepuffer keine weiteren Seitenaufrufe blockieren.
