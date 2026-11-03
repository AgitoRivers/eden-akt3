# JangaFX-Exportbibliothek · 27.10.2026

Geschrieben/exportiert: sechs unterschiedliche Presets, je 4096 × 4096 RGBA, 8 × 8 Felder, 64 Bilder à 512 px. Die 4096 px beziehen sich auf den gesamten Bilderbogen, nicht auf ein einzelnes Bild.

Eingebaut: noch nicht im Spiel. Getestet: Dateien lesbar, Alpha, Raster, mehrere unterschiedliche und nichtleere Frames; keine künstlerische Freigabe vorweggenommen. Kein Commit dieser Serie.

## Zuordnung der sechs Granaten

| Granate | Material | Noch zu ergänzen |
| --- | --- | --- |
| Feuer | aerial-explosion-2; bodennah artillery-explosion-1 | Glutfunken, Brandfleck, Timing |
| Wasser | press-splash als Ausbruch; bereinigter fountain als schmaler Fallstrahl | Vorlauf zuschneiden, Sprühfahnen gestalten; noch keine fertige Granate |
| Schock | vorhandene Labor-Blitzbögen (assets/strom.png) | radial ausrichten, dreimal flackern und Sprite-Reaktion |
| Flash | vorhandener Phare-Lichtschein (assets/realismus-v3/licht.png, blendung.js) | Weißblende und Tinnitus mit Spielreglern abstimmen |
| Erschütterung | smoke-shockwave-2, Staub aus artillery-explosion-1 | Rauch entsättigen, Feueranteil vermeiden, Wackeln/Unschärfe |
| Splitter | smoke-shockwave-2 oder vorhandener Omertà-Rohdruck | Metalllinien und Trefferstriche als getrennte Ebene |

## Zusätzliche Reserve

- toroidal-force: geschlossener Wasserring für Schild, Aufladung oder Ringbewegung. Path Tracer. Projektkopie mit Export-Einstellungen liegt daneben.
- fountain: korrigiert nach Ducs Hinweis. Beide Collider-Gruppen sind inaktiv und ausgeblendet; Shapes Rendering = Ignore. Neu simuliert ab Frame 240, Schrittweite 4, Path Tracer. Jetzt ein schmaler freier Fallstrahl, keine breite Granatenfontäne. Arbeitskopie fountain-ohne-hindernisse.liquigen gesichert. Der alte Rasterizer-Export zeichnet Hinderniskonturen nach und ist ausschließlich verworfene Referenz, nicht mehr Hauptauswahl.
- press-splash: Schrittweite 8 erfasst auch die spätere Kompression und den Ausbruch. Path Tracer; Shapes Rendering = Ignore, Boden aus. Der komplette Vorlauf ist Rohmaterial und soll nicht unverändert im Spiel laufen.
- smoke-shockwave-2: blau/violett im Original; der Grau-Schalter der Vorschau ändert nur die Darstellung.
- Bereits vorhandener kompakter Rauchdruck: ../omerta-shockwave-v1/omerta-rauchdruck_render_all.png (blau/violett, noch ohne die goldene Omertà-Bearbeitung). Nicht erneut exportiert.

## Herkunft und Wiederholung

Original-Presets wurden vor den Exporten separat als *-original.ember / *-original.liquigen kopiert. SHA256, Bildprüfungen und Export-Zeitfelder stehen in exporte.json. EmberGen 1.2.12, LiquiGen 1.2.1. Die ursprünglichen Installations-Presets wurden nicht gespeichert oder überschrieben.

Export-Overrides: Flipbook 4096 × 4096, Raster 8 × 8, 64 Frames. Aerial, Artillery, Smoke und Toroidal: Start 0 / Schritt 1. Fountain: Start 240 / Schritt 4. Press Splash: Start 0 / Schritt 8. Originalprojekte enthalten diese Overrides nicht automatisch; gespeicherte Arbeitskopien sind gesondert benannt. Zeitwerte der Vorschau sind frei wählbar, keine zugesagte physikalische Wiedergabedauer.

Vorversuche bleiben als *startup-reference.png bzw. *2048.png erhalten und werden nicht in der Hauptauswahl gezeigt. smoke-shockwave und gushing enthalten nur vorbereitete Originalprojekte, noch keinen Export. Gushing zeigt im Standard schwarzes Öl und wurde deshalb nicht als Wasser-Kandidat ausgegeben.

index.html öffnet die sechs Haupt-Bilderbögen als Animation, ohne Spielzustand oder Engine zu laden. Die Originaldateien bleiben unverändert. exporte.json ist der technische Katalog.
