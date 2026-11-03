# Bonaccia: Wasser-Schutzschild, Stand 3

Geschrieben: Eigenes LiquiGen-Projekt und neuer nativer Export. Nutzer-Ausgangsprojekt shieldwall.liquigen bleibt unverändert und ist zusätzlich gesichert.

Eingebaut: Nur isoliertes Status-Labor auf Port 8337, Angriff calm. Drei Darstellungen derselben nativen Simulation: breiter Schild, schmaler vorgeschobener Bogen, breite leicht geneigte Wasserlinse. Alle liegen links vor Duc. Kein Gegner-Hurt, keine Regeländerung, kein Einbau im Live-Spiel.

Getestet: 3 Varianten in je 5 Phasen, native Textur tatsächlich gezeichnet, 64 unterschiedliche Quellbilder, Effekte abschaltbar, keine Bildlade- oder JavaScript-Fehler. Aufbau und fertiger Schild per Screenshot geprüft.

## Herkunft und Grenzen

Projekt: quellen/bonaccia-liquigen-v3/shieldwall-native-v1.liquigen
Ausgangssicherung: shieldwall-ausgang.liquigen
Native Rohbilder: shieldwall-native-v1_render_all_rasterizer_.png
Spielatlas: assets/bonaccia-liquigen-v3.png
Metadaten: quellen/bonaccia-liquigen-v3/export.json

LiquiGen sphere_slosh als Ausgangsvorlage, eigener abgeflachter ellipsoider Behälter mit Radien 20/7/26; Quelle 34/10/42 bei Z=26; Schwerkraft 0, anfängliche Geschwindigkeit 8 nach oben. Camera 2, FOV 45, 64 Bilder ab Frame 0 mit Schrittweite 3. Rohatlas 8192 x 8192, 1024 Pixel pro Bild, Rasterizer 5 Samples. Hintergrund, Boden und feste Formen nicht gerendert. Gleichbleibender Beschnitt pro Bild und Alpha-Kantenglättung 0,45 Pixel; keine KI-Vergrößerung.

Die Wasserbewegung und Oberflächenreflexe sind tatsächlich simuliert. Das Anwachsen vor der Figur und die Bahnen der einziehenden Tropfen sind 2D-Spielchoreografie; das ist keine vollständig physikalisch simulierte Tropfenverschmelzung. Tropfen verwenden das native Wassermaterial plus Glanzreflex. Es werden keine Splash-Atlanten oder Nebel-Ersatzflächen verwendet.

Der erste Versuch schnürte sich zu stark ein. Er bleibt als test-01-einschnuerung.png in der Sicherung und wird nicht ausgespielt. Vorheriger eingebauter Stand unter quellen/bonaccia-liquigen-v3/vor-einbau. Dateien mit vorhandenen CRLF-Zeilenenden geschrieben. Keine Commits.

## Anpassung 4: Aufbau aus der Mitte

Der Kern entsteht mittig vor dem Oberkörper. Die komplette native Wasserfläche wächst bei festem Mittelpunkt gleichmäßig nach außen; keine Bodenverankerung mehr. Tropfen ziehen aus allen Richtungen zur Mitte ein. Vorherige Choreografie unter quellen/bonaccia-mitte-v4 gesichert. Native Simulation und Kampfregeln unverändert.

## Anpassung 5: bewegtes Wasser über der gesamten Fläche

Der turbulente untere Ausschnitt des nativen Flipbooks wird zusätzlich in drei weich überblendeten, unterschiedlich orientierten Bereichen über den Schild verteilt. Die ursprüngliche simulierte Alpha-Silhouette begrenzt diese Wasserdetails. Kein neuer Export: 2D-Komposition des vorhandenen LiquiGen-Materials. Aufbau aus der Mitte bleibt erhalten. Drei Varianten in fünf Phasen geprüft, Screenshots kontrolliert und harte Übergänge entfernt. Sicherung vor der Änderung unter quellen/berserker-v1.
