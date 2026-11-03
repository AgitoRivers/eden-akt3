# Sotto Voce · Schallkugel

Geschrieben: Drei visuelle Varianten – verdichtete Stimme, doppeltes Echo und tiefe Resonanz. Perlmuttgraue, transparente Kugel mit bewegten inneren Druckwellen und unregelmäßig pulsierender Stärke. Sichtbarer Aufbau links, kurze Entladung zum rechten Sprite und auslaufende Resonanz. Nachbilder, Schutzpose und seitliche Bewegung bleiben; die Figur vibriert nach der Ankunft zusätzlich für bis zu 1,65 Sekunden. Kein Hurt und keine schädigende Explosion.

Eingebaut: Ausschließlich im Effektlabor auf Port 8337. Gemeinsames Modul ablaufprobe/sotto-voce.js, Einbindung in angriffe.js, lokale Vibrationsbewegung in probe.js, neue Cache-Versionen in index.html. Beide Vorschaukopien synchron. Vorherige Dateien unter quellen/sotto-voce-v1 gesichert. Keine Spielstände oder Kampfregeln verändert.

Wichtige Zuordnung: Laut docs/wiki/systeme/kampf.md ist Sotto Voce weiterhin L5 Abtauchen: nächster eingehender Treffer halbiert, nächster eigener Angriff sicher kritisch. Die gewünschte Entladung zum rechten Sprite ist eine visuelle Studie. Vor einer Übernahme in den echten Kampf müssen Anwender und Ziel der Darstellung entsprechend dieser Regel zugeordnet werden. Keine stillschweigende Umwandlung in einen Schadens- oder Schallangriff.

Material: Im Browser erzeugte, zeitlich bewegte Drucktextur aus vorhandener Rauschquelle. Keine neue KI-Grafik, kein neuer JangaFX-Export, kein Mauszugriff.

Getestet: Drei Varianten in fünf Phasen, unterschiedliche Bilder für Aufbau, Flug, Kontakt und Nachlauf; Schutzpose, kein Hurt und Effekte-Schalter geprüft. Keine Browser- oder Ladefehler. Gerenderte Bilder zusätzlich visuell geprüft und die zunächst flache Ringstruktur räumlicher gestaltet. Renderaufrufe im Headless-Browser ohne GPU im Mittel ungefähr 9 ms; keine Zusage zur sichtbaren Bildrate. Prüfskript im Codex-Arbeitsordner work/status-labor/sotto_voce_pruefen.cjs.
