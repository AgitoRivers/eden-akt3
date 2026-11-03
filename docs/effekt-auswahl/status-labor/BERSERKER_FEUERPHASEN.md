# Berserker: Feuerball, Sturm, Konter und Peitsche – Stand 2

Neueste Nutzerfreigabe: vier unterschiedliche Abläufe, aktive Verwendung des geöffneten EmberGen; sofort starten statt des zuvor geplanten Starts um 01:30 Uhr. Dieser geplante Start wurde über die App auf PAUSED gesetzt, damit keine doppelte Ausführung beginnt.

## Bedienung im Labor

Angriff wählen, eine von drei Varianten ansehen und mit Phase zwischen Kompletter Ablauf, Aufladen und halten sowie Entladung wechseln. Bei Furia heißen die getrennten Phasen Brennzustand / Angriff. Die gehaltene Phase läuft mit weiterhin bewegtem Feuer, ohne selbst einen Treffer auszulösen. Sie wird erst durch Umschalten in die Entladung verlassen; kein automatischer Neustart nach sieben Sekunden. Vulcano hat zusätzlich die Auswahl 1–5 Brandstufen. Scirocco nutzt Ducs freie Hand-/Schutzpose; kein Klingenschlag.

- Scirocco: Feuerball vor dem Oberkörper laden, zum Gegner schleudern, explosiver Einschlag. Varianten: gerader Flug, höherer schwerer Bogen, konzentrierter Tiefflug.
- Retour de Flamme: Körperladung und Funken halten, beim Konter als Feuer-Schweif am Ziel entladen. Varianten: flacher Hieb, diagonale Rückhand, steile Entladung. Im kompletten Ablauf erfolgt davor ein gegnerischer Treffer mit Ducs eigener Hurt-Pose; in der gehaltenen Ladephase kein erzwungener Gegentreffer.
- Furia: anhaltendes Brennen an Duc, beim Angriff eine bewegte Feuerpeitsche zum Ziel. Varianten: züngelnder Seitenschlag, Überkopf-Geißel, S-Bahn. 3 Runden Brennzustand sind die jüngste ausdrückliche Vorgabe des Nutzers. Der ältere Kampfplan nennt noch 2 Runden und einen sofortigen Auftakttreffer. Diese Differenz ist hier dokumentiert; Engine und Kampfplan werden nicht nebenbei geändert.
- Vulcano: wachsende Feuerspirale, gegenläufige Feuerfronten oder obere Sturmkrone. Danach große explosive Entladung mit genau einem Feuer-Schweif je gewählter Brandstufe. Jeder Kontakt hat passende Angriffs-/Hurt-Pose und Rückstoß. Keine zusätzlichen Schadentreffer durch bloße Funken oder Flammen.

## Tatsächlich neu aus EmberGen exportiert

1. scirocco-feuerball.ember aus game_fire_ball_loop.ember: 64 Bilder, erster Frame 160, Schrittweite 2; Rohatlas 4096 × 4096, 512 Pixel pro Bild. Neue native Simulation der Vorlage. Der Export enthielt RGB-Emission, aber Alpha überall 0; für die Spieltextur wurde aus der Emission eine Alpha-Maske abgeleitet und auf gerade Alpha umgerechnet.
2. feuer-entladung.ember aus game_explosion_1.ember: 64 Bilder, erster Frame 0, Schrittweite 2; Endexport 8192 × 8192, 1024 Pixel pro Bild, vorhandenes natives Alpha, für Canvas auf gerade Alpha umgerechnet. Vorheriger 512-Pixel-Test erhalten.

Eigene Projektkopien und unveränderte Rohexporte unter quellen/berserker-ember-v2. Dort stehen in export.json auch Hashes, feste Beschnitte und Zellgrößen. Spieltexturen unter assets/berserker-v2. Je 64 unterschiedliche Quellbilder geprüft. Beide Projekte mit den finalen Exportparametern gespeichert. Simulation am Ende des begrenzten Exports angehalten; kein unbeschränkter Renderlauf gestartet.

Die Feuerball- und Explosionsbewegung stammt aus echten neuen EmberGen-Exporten. Sturm, Feuer-Schweife und Peitschenbahn sind 2D-Kompositionen dieser bewegten Materialien, keine separat neu simulierten 3D-Sturm-/Peitschenprojekte. Hinzu kommen das vorhandene Feuer-Flipbook für Furia und prozedurale Funken. Keine neuen KI-Standbilder und keine Stahltextur in den neuen Feuer-Schweifen.

## Einbau und Absicherung

Nur docs/effekt-auswahl/status-labor/ablaufprobe und eigene Assets geändert; auf die isolierte Testseite gespiegelt. Port 8337. Kein Engine-Einbau, keine Kampfberechnung, keine Spielstände, keine fremden Git-Änderungen, keine Commits oder Pushes. Der fertige Wasserschild bleibt erhalten. Sicherung unmittelbar vor dem Einbau unter quellen/berserker-ember-v2/vor-einbau. Bestehende CRLF-Zeilenenden erhalten, JSON programmatisch geschrieben.

berserker.js exportiert getrennte drawCharge und drawRelease-Funktionen. Die Laborsteuerung liefert previewMode und eine eigene weiterlaufende animationClock, damit gehaltene Effekte nicht einfrieren. Das ist eine Vorbereitung für spätere Kampfevents, keine Live-Integration.

Geschrieben: vier neue Choreografien, zwölf Varianten und getrennte Phasenauswahl.
Eingebaut: ausschließlich die isolierte Laborvorschau.
Getestet: native Bildquellen und Alphakanäle, sichtbare Lade-/Flug-/Kontaktphasen; zwölf Varianten, 36 Ladeproben und 18 Kontakte, keine Entladung oder Hurt-Pose beim Halten, animiertes Halten auch nach neun Sekunden, Scirocco ohne Stahltextur, Retour mit eigener Hurt-Pose im kompletten Ablauf, Vulcano mit 1–5 Trefferzahlen und Effektschalter. Gemeinsame Regression zusätzlich prüfen.

Abschließende Regression bestanden: 16 Angriffe × 3 Varianten × 5 Phasen = 240 Phasen; Duc durchgehend sichtbar, Selbst-Effekte am richtigen Akteur, keine Lade- oder JavaScript-Fehler. Gehaltene neue Feuerphasen zusätzlich nach 9,1 Sekunden geprüft. Der ältere Regressionstest nennt in seinem Ausgabe-Feld Varianten weiterhin fest 36; tatsächlich wurden alle 48 Varianten durchlaufen.
