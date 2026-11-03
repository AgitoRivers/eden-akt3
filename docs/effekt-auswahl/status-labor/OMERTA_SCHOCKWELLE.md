# Omertà – Goldaura, Hinterhalt und native Rauch-Druckwelle

Stand: 24.10.2026. Aktueller visueller Ablauf; ersetzt die frühere Goldkugel aus OMERTA_GOLD.md.

## Ablauf

1. Waffenunabhängige Goldaura am Körper, einziehende Funken.
2. Duc verschwindet kurz vor dem Angriff samt Bodenschatten.
3. Zwei gerichtete goldene Wischer von oben links und oben rechts kreuzen sich am Ziel.
4. Nach dem zweiten Schnitt bricht die goldene native Smoke Shockwave auf.
5. Funken und feiner glitzernder Goldstaub laufen aus. Duc kehrt links zurück.

Drei Varianten: Pakt der Stille, Goldener Hinterhalt (breitere Welle), Goldenes Urteil (höhere Welle).
Die drei visuellen Kontakte liegen bei -0,16 / +0,18 / +0,50 Sekunden relativ zum bisherigen Kontaktpunkt. Eigene Trefferreaktionen und Rückstoß sind darauf abgestimmt. Dies ist eine isolierte Vorschau; Schaden, Unsichtbarkeit und Kampfregeln werden hier nicht in der Engine geändert.

## Native Quelle

- Vom Nutzer geöffnet: EmberGen smoke_shockwave_2.
- Eigene Projektkopie und Export: quellen/omerta-shockwave-v1/omerta-rauchdruck.ember.
- Originalexport: omerta-rauchdruck_render_all.png, 4096 × 4096, 8 × 8 Zellen, 512 Pixel je Bild, 64 Bilder, Start 0, Abstand 2.
- Kurzer Export wurde in EmberGen ausgeführt, Projekt gespeichert, Simulation bei Bild 127 angehalten.
- Goldpalette aus dem Export abgeleitet; native Alpha von vormultipliziert in gerades Alpha überführt. Quelle und Hashes: quellen/omerta-shockwave-v1/export.json.
- Laufzeitmaterial: assets/omerta-shockwave-gold-v1.png.

## Pluie d’Étoiles

Favorisierte Variante: Dreifacher Fall. Nur beim dritten Kontakt kommt eine zusätzliche silberblaue Explosion aus dem vorhandenen nativen EmberGen-Explosionsmaterial hinzu. Danach bleibt der bereits abgestimmte feine Eisstaub. Die beiden anderen Varianten bleiben erhalten.

## Status

- Geschrieben: omerta.js, Ablauf- und Figurenanbindung, finales Pluie-Explosionsereignis.
- Eingebaut: nur Effektlabor und dessen Spiegel auf Port 8337.
- Getestet: drei Omertà-Varianten, Aufladen, Verschwinden, Druckwelle, Rückkehr, Effekte aus; Pluie-Explosion ausschließlich am dritten Treffer von Dreifacher Fall. Browserfehler und fehlende Dateien geprüft. Mit Lame de Fond, Vulcano und Pluie anhand tatsächlicher Laboraufnahmen verglichen.
