# Wasserlanze: zusammenhängende Ablaufprobe

Vorschau: http://127.0.0.1:8337/status-labor/ablaufprobe/

## Geschrieben

Eine getrennte Studie für einen vollständigen Angriff: Druckaufbau, Flug,
Kontakt und Ausklang. Abwehr- und Trefferpose, Rückstoß, örtliches Licht,
bewegte Wassermasken und Spritzwasser reagieren auf dieselben Zeitpunkte.
Pause, Zeitlupe, Zeitregler und ein Vergleich ohne Effekte sind vorhanden.

Die Strömung überlagert drei unabhängig bewegte Masken. Die Methode orientiert
sich an JangaFX' Analyse von Diablo-3-Effekten:
https://jangafx.com/insights/diablo-3-vfx-experiments
Es wurden keine Diablo-Spielressourcen übernommen.

Die vorhandenen LiquiGen- und EmberGen-Exporte bleiben erhalten. Für diese
Studie wurde eine eigene Spritzwasserfassung abgeleitet: gesättigter violetter
Kern und rote Hilfsmarkierung werden vor der neutralen Einfärbung ausgeblendet.
Die Wasseranimation bleibt eine zweidimensionale Bildfolge mit begrenzter
Auflösung. Der Aufbau verbessert den Zusammenhang, ersetzt jedoch keine
maßgeschneiderte Simulation und keine räumliche Beleuchtung.

Zusätzlich wurde die gebogene Klingentextur mit der eingebauten Bildbearbeitung
begradigt. Die bisherige Wischbewegung und der höhere Schnitt bleiben bestehen.
Originalbild und Sicherungen sind erhalten.

- Bild: `assets/realismus-v3/stahl-gerade.png`
- Werkzeug, genauer Prompt und Ausschnitt: `quellen/gerader-schnitt/quelle.json`
- Renderer und Bedienung: `ablaufprobe/probe.js`, `ablaufprobe/index.html`
- Abgeleitete native Bildfolge: `ablaufprobe/spritzwasser.png`

## Eingebaut

In die isolierte Vorschau auf Port 8337; im Effektauswahl-Menü unter
„F · Angriff im Ablauf“ erreichbar. Die gerade Klingentextur wird in den
vorhandenen Spezialangriffen verwendet. Keine Übernahme in den laufenden Kampf.

## Getestet

Mit Edge ohne GPU-Beschleunigung: sieben verschiedene Zeitpunkte,
Effekte ein/aus, Abspielen/Pause, Neustart, Zeitlupe und schmale Darstellung.
Keine JavaScript- oder Ladefehler. Flug und Treffer zusätzlich als Bilder
angesehen; rechteckige Strömungskanten und starrer Trefferkern korrigiert.

Die Klingenspur wurde separat auf wandernde Deckkraft geprüft: Schwerpunkt
bei drei Zeitpunkten 137,74 / 181,16 / 258,82 Pixel; keine Browserfehler.

Die technische Prüfung ist keine gestalterische Abnahme. Die Qualität bleibt
an der neuen Ablaufprobe zu beurteilen; die übrigen Angriffe wurden nicht
pauschal nach diesem Muster umgebaut. Keine Commits, keine Spielstandänderung.

## Druckkern als Wasserkugel

Druckaufbau und Flug verwenden nun eine runde, leicht unregelmäßige Wasserkugel mit bewegter Oberfläche, räumlicher Schattierung und weichem Rand. Beim Flug bleibt ein kurzer Schweif. Treffer und Nachlauf bleiben unverändert. Sicherung: quellen/druckkugel.

In die isolierte Vorschau übernommen. Abspielsteuerung und sieben Zeitpunkte erneut ohne Browserfehler geprüft; Aufbau und Flug zusätzlich visuell kontrolliert.

## Feinere Wasseroberfläche

Die Kugel wird mit 256 statt 128 Pixeln pro Kante berechnet (vierfache Pixelzahl). Die Vorschau zeichnet mit 1920 × 1200 statt 960 × 600 Pixeln bei gleicher Anzeigegröße. Bilinear abgetastete bewegte Oberflächenstrukturen beeinflussen Reflexe und Schattierung; ein verzerrter Ausschnitt des Szenenhintergrunds wird für die Durchsicht verwendet. Die alte helle Linienstruktur wurde durch weichere bewegte Reflexe ersetzt. Das ist eine visuelle Annäherung an Lichtbrechung, keine physikalische Flüssigkeitssimulation. Die vorhandenen Trefferbildfolgen behalten ihre ursprüngliche Auflösung.

Nur in der isolierten Vorschau eingebaut. Aufbau und Flug visuell geprüft; sieben Zeitpunkte und Bedienung erneut ohne Browserfehler getestet, mit ausgeschalteter GPU-Beschleunigung. Keine Leistungszusage für andere Geräte. Sicherung: quellen/wasserdetails.

## Längerer Aufbau, kürzeres Ende

Abschuss jetzt bei 3,12 statt 1,12 Sekunden, Treffer bei 3,50 Sekunden. Nur der Aufbau wird verlängert. Wasseroberfläche und Reflexe laufen währenddessen in normalem Tempo weiter. Flug, Kontakt und Ausklang behalten ihr Tempo. Der Durchlauf endet nach 5,45 Sekunden statt nach 6 Sekunden: Die frühere Wartezeit am Ende entfällt weitgehend. Regler und Phasenanzeige folgen der neuen Zeit. Sicherungen: quellen/aufbau-laenger.

## Gischt und längere Trefferreaktion

Die Wasserkugel trägt zusammenhängende, bewegte Schaumfelder und einen etwas unruhigeren Rand. Keine zusätzlichen Punktschwärme. Die Trefferpose bleibt nach Kontakt 1,25 Sekunden vollständig sichtbar und geht dann über 0,40 Sekunden weich in die normale Pose über (zuvor harter Wechsel nach 0,58 Sekunden). Der längere Aufbau und das Tempo von Flug und Treffer bleiben erhalten. Sicherung: quellen/gischt-hurt.

Geprüft: sieben Zeitpunkte, Phasenwechsel, Schleife und Bedienung ohne Lade- oder JavaScriptfehler. Gischt beim Aufbau und verlängerte Trefferpose zusätzlich visuell angesehen. Nur Vorschau auf Port 8337, keine Spielregeländerung.

## Gerichteter Splash mit Fallbewegung

Der Kontakt beginnt kompakt, breitet die Flüssigkeitsfahnen rasch aus und zieht sie danach nach unten. Eine dünnere hintere Fahne und eine weiche, kurzlebige Gischtschicht ergänzen die vordere Wasserfläche. Bodennachlauf setzt verzögert ein und breitet sich flach aus. Die vorherige helle Doppelüberlagerung und der Staubanteil wurden reduziert. Kugel, Aufbau, Trefferpose und Schleifendauer sind unverändert. Die native Wasserquelle bleibt dieselbe; dies ist eine Überarbeitung ihrer Bewegung und Schichtung, kein neuer hochauflösender Simulationsexport. Sicherung: quellen/splash-kontakt.

Kontakt und spätere Wasserfahnen visuell geprüft. Sieben Zeitpunkte, Phasenwechsel, Wiederholung, Effektschalter und Bedienung ohne Browserfehler geprüft; nur isolierte Vorschau.

## Korrektur: keine fallende Bildfläche

Die künstliche Fallbewegung des gesamten Splashbildes ist entfernt. Ebenso entfernt: zweite gedrehte Wasserfläche hinter der Figur, flach verzerrter Bodensplash und Beton-Trefferanimation am Boden. Diese Kombination erzeugte einen unpassenden Nachlauf. Der Splash nutzt jetzt nur die Bewegung innerhalb der nativen Wasserbildfolge und löst sich am Kontaktpunkt auf.

Das neue Asset spritzwasser-natuerlich.png stammt erneut aus dem unveränderten LiquiGen-Export: kein angehobener Grausockel, zurückhaltendere Deckkraft und leicht weichere Kanten. Originale und vorherige Fassung bleiben erhalten. Die Kugel und die verlängerte Trefferpose sind unverändert. Es handelt sich weiterhin um die vorhandene zweidimensionale Simulation, nicht um einen neuen Export mit mehr Detail. Sicherung: quellen/splash-material.

Verifikation: Kontakt bei 4,20 s und Ende bei 5,30 s visuell kontrolliert; keine nach unten versetzte Splashfläche und kein zusätzlicher Bodentreffer mehr. Sieben Zeitpunkte und Bedienung ohne Browserfehler geprüft. Der ursprüngliche Export begrenzt weiterhin den Detailgrad der Wasserflächen.
