# Lame de Fond · echte LiquiGen-Simulation

Geschrieben: neuer nativer LiquiGen-Export mit 64 unterschiedlichen Flüssigkeitsbildern, 512 × 512 Pixel pro Ausgangsbild. Grundlage wave_maker_3, Profilkamera, engerer Blickwinkel, sichtbare Hilfsobjekte ignoriert, Boden ohne Darstellung. Frühere Testexporte bleiben erhalten.

Eingebaut: erste Variante im isolierten Ablauf-Labor auf Port 8337 spielt die neue Sequenz mit weichen Bildübergängen ab. Das generierte Einzelbild und sein Verformungsnetz werden nicht mehr geladen. Gischt, Rückstoß und Hurt bleiben erhalten. Keine Live-Spieländerung.

Grenze: Die Simulation zeigt eine breite Wasserfront. Die Form entspricht noch nicht vollständig der einzelnen überhängenden Bild-Krone. Die künstlerische Abnahme steht aus.

Quelle und genaue Verarbeitung: quellen/lame-native-v2/integration.json. Originalexport bleibt unverändert.

Getestet: 64 unterschiedliche native Bilder nachgewiesen; sieben verschiedene Ablaufphasen, längeres Hurt, Effektschalter und die beiden bisherigen Varianten ohne Browserfehler geprüft. Sichtkontrolle durchgeführt; harte obere Schnittkante durch erweiterten Quellausschnitt entfernt.

Bedienung: Nach Ducs Bitte keine weitere Maus-/App-Steuerung. Exportdateien sind fertig; das offene LiquiGen-Projekt wurde danach nicht per UI gespeichert. Exportparameter sind in integration.json dokumentiert.

Exportreferenz: https://docs.jangafx.com/liquigen/pages/references/node_list.html (Export: Image).
