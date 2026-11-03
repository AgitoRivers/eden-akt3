# Erschüttert: gemeinsame Darstellung für alle Schauplätze

Aktuelle Entscheidung: überall Schutzpose und anhaltendes Rütteln, ergänzt
durch 308 Partikel in sieben überlappenden Ausbrüchen über rund dreieinhalb Sekunden. Kein fester Bodenriss, keine
Steinplatte, kein Nebel und keine vom Schauplatz abhängige Bodenfläche.

Die kleinen fotografischen Splitter werden aus isolierten Fragmenten der
vorhandenen Bodenbruch-Textur gelesen. Die Textur selbst bleibt erhalten,
wird aber nicht mehr als Bodenfläche dargestellt. Splitter bewegen sich
einzeln nach außen, prallen kurz am Boden ab und verschwinden. Jeder Splitter
lebt weniger als eine Sekunde; die versetzten Schübe verlängern den Gesamteffekt. Schutzpose, weiche Erholung und Rütteln laufen danach weiter.

Geschrieben/eingebaut: `zustand-reaktionen.js`, Beschreibung in `labor.js`
und Cacheversion in `index.html`, ausschließlich Vorschau auf Port 8337.
Sicherung unter `quellen/neutrale-steinspritzer/`.

Getestet: kleine Ausschnitte statt kompletter Bodenfläche, längerer
Auslauf und Schutzpose. Darstellung zusätzlich als Bild angesehen.
Keine Browserfehler. Keine Änderung an Spielregeln, Spielständen oder Commits.

Diese Entscheidung ersetzt die frühere Vorgabe eines größeren Bodenrisses.

## Kräftiger Ausbruch und braune Schlammfassung

Der Partikeleffekt wurde auf sieben Schübe mit je 44 unterschiedlich großen Fragmenten erweitert. Feinere Splitter und größere Stücke springen höher, taumeln vor und hinter der Figur und prallen kurz am Boden ab. Die Quelle bleibt fotografisches Steinmaterial; kein Kreis, keine Bodenplatte.

Schlamm verwendet denselben Ausbruch mit braun eingefärbten Erdklumpen. Nasser Körperfilm und frei auslaufender Schlammfuß bleiben erhalten; der Bodendunst wurde reduziert, damit die Klumpen sichtbar bleiben.

Getestet bei 0,8 / 1,5 / 2,5 / 3,4 / 4,05 Sekunden: 88 / 152 / 156 / 38 / 0 gezeichnete Partikel bei beiden Effekten. Braune Farbe geprüft, beide Darstellungen zusätzlich angesehen; keine Browserfehler. Sicherungen unter quellen/partikel-ausbruch. Nur isolierte Vorschau, keine Spielregeländerung.

Aktuelle Abstimmung: Partikelzahl auf die Hälfte reduziert, 22 statt 44 je Schub, insgesamt 154 statt 308. Gilt gemeinsam für Erschüttert und Schlamm. Sieben Schübe, Dauer, Flugbahnen, Größen und Farben bleiben erhalten.
