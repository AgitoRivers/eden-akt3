# Oil Fire und organischer Nachbrand

Stand: 24.10.2026. Nur Effektlabor auf Port 8337.

## Export

EmberGen oil_fire wurde als eigene Projektkopie gespeichert und nativ exportiert.

- Projekt: quellen/oil-fire-v1/oil-fire-vorlage.ember
- Original: quellen/oil-fire-v1/oil-fire-vorlage_render_all.png
- Vollständige Fassung mit geradem Alpha: quellen/oil-fire-v1/oil-fire-gerades-alpha.png
- 4096 × 4096 Pixel, 8 × 8 Zellen, je 512 Pixel, 64 Bilder; Startbild 120, Abstand 2. Dadurch enthält die Folge bereits entwickeltes Feuer.
- Simulation nach dem kurzen Export bei Bild 247 angehalten, Projekt mit Exporteinstellungen gespeichert.
- Quelle, Alpha-Aufbereitung und Hashes: quellen/oil-fire-v1/export.json.

## Wiederverwendbares Brennen

brennen.js zeichnet mehrere verankerte Flammenbereiche mit versetzten Phasen und Größen. Die native Feuerbewegung bleibt erhalten. Zwischen Einzelbildern und über dem Übergang der Folge wird überblendet. Kleine Funken steigen unregelmäßig auf. Die Körperfassung assets/oil-fire-koerper-v1.png reduziert undurchsichtigen Ruß und federt den Ansatz weich aus; die vollständige Vorlage bleibt erhalten.

Verwendung:

- Scirocco: Nachbrand statt der alten einzelnen Feuerschicht.
- Retour de Flamme: sichtbarer Nachbrand nach dem Konter.
- Furia: anhaltendes Feuer an Duc, auch während der gehaltenen Phase. Nach dem Peitschentreffer zusätzlich sichtbarer Nachbrand am Gegner, wie bei Scirocco und Retour. Beschriftung weiterhin drei Runden; die Vorschau verändert keine Rundenzählung.
- Vulcano: Restfeuer nach der letzten Entladung, danach langsames Erlöschen. Die konsumierten Brandstufen werden nicht neu gesetzt.
- Zustand Brennend: loderndes Feuer und warme weiche Kontur.
- Reaktion Feuersturm: gleiche native Flammen, vorhandene Blitze bleiben erhalten.

Die vier Berserker-Vorschauen haben eine zusätzliche Sekunde für den Ausklang. Der Nachbrand legt keine neuen Status- oder Schadensregeln fest. Alle Spielregeln und Spielstände bleiben außerhalb dieser Vorschau.

## Status

Geschrieben: gemeinsame Feuerdarstellung, vier Ausklänge, Zustand/Reaktion, Vorlagenmetadaten.
Eingebaut: Effektlabor und lokaler Spiegel.
Getestet: zwölf Angriffsvarianten; richtige Figur, bewegte Feuerfolge, gehaltene Furia-Phase, keine vorzeitige Entladung in Ladephasen, Effekte ausschaltbar, Brennend-Ansicht ohne Browser- oder Ladefehler. Feuerbilder visuell geprüft.
