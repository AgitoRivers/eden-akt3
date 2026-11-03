# Wasserball · Bodenaufprall

Exportiert am 28.10.2026 aus LiquiGen 1.2.1, Vorlage ball_drop_splash. Kein Press-Splash zwischen Wänden: eine Flüssigkeitskugel fällt und zerplatzt am Boden. Ansicht von der Seite, leicht erhöht. Material Water. Boden und Hilfsformen wirken in der Simulation, werden aber nicht mitgerendert. Himmel ebenfalls aus; transparente PNGs.

- Bildfolge: bildfolge/wasserball-boden_000.png bis _063.png, je 512 × 512 RGBA.
- Bilderbogen: wasserball-boden-flipbook.png, 4096 × 4096, 8 × 8, Reihenfolge zeilenweise.
- Unveränderter nativer Export: Untitledrender_all_path_tracer_.png.
- Arbeitsprojekt: wasserball-boden-export.liquigen. Originalpreset separat gesichert.
- Einstellungen und Bildprüfungen: wasserball-boden.json. Für die sichtbare Fassung wurde RGB um Faktor 4 angehoben und über eine sRGB-Kurve aufgehellt; Alpha und Bewegung sind unverändert. Der dunkle native Export liegt separat bei.
- Vorschau: index.html. 20 Bilder/s entsprechen der ursprünglichen Simulationszeit; Spieltempo kann später angepasst werden.

Startframe 60, 64 Bilder, Schritt 3, Simulation 60 Hz. Export endet während der seitlichen Ausbreitung: beim späteren Einbau einen kurzen Ausklang vorsehen. Die Bildfolge enthält kein künstliches Ausblenden.

Geschrieben/exportiert: native Simulation, PNG-Bilderbogen und farbkorrigierte Einzelbilder. Eingebaut: ausschließlich separate Quellen-Vorschau, keine Engine-Dateien geändert. Getestet: PNG-Lesbarkeit, Transparenz und unterschiedliche Frames; Geschmack/Freigabe liegt bei Duc. Alte Fontäne bleibt im Spiel unverändert. Nicht committed.

wasserball-boden-belichtung-v1.png ist ein dunkler Vorversuch und gehört nicht zur Auswahl.
