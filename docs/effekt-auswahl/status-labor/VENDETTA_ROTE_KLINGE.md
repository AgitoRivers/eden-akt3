# Slashes nur am Ziel, Vendetta in Rot

Geschrieben:

- Der zweite Wassersplash ist vollständig entfernt, einschließlich eigener
  Materiallage und Bildanforderung. Nass bleibt beim einzelnen Körper-Splash,
  nassem Stoff, Reflexen und blauer Kontur.
- Der kleine vorbereitende Klingenschnitt links ist bei Doppio Gioco,
  Vendetta und Omertà entfernt. Ihre Schnitte erscheinen nur am Ziel rechts.
- Vendetta verwendet eine neue, gerade karminrote Klingentextur in allen
  drei Varianten. Feine helle Materialspuren bleiben erhalten. Die Textur
  wischt weiterhin durch den Kontakt; kein bloßes Einblenden. Ein kurzer,
  örtlicher roter Reflex liegt auf der Figur. Vendetta verwendet nach der präzisierten Nutzervorgabe eine deutliche Hurt-Pose
  und Rückstoß: direkter schmerzhafter Treffer mit Blutung.

Bildwerkzeug: eingebaute Bildbearbeitung auf Basis der geraden silbernen
Klingentextur. Keine neue JangaFX-Simulation. Original bleibt erhalten.

- Bild: `assets/realismus-v3/stahl-vendetta-rot.png`
- Genauer Prompt: `quellen/vendetta-rot/finaler-prompt.txt`
- Quelle und Ausschnitt: `quellen/vendetta-rot/quelle.json`

Eingebaut: ausschließlich Vorschau auf Port 8337. Die rote Vendetta-Textur
ist auch im bisherigen Dreiervergleich vorhanden. Änderungen an Renderer,
Bildladen, Quellenmetadaten und Cacheversionen; Sicherungen in
`quellen/vendetta-rot/`. Keine Spielregeln, Live-Spielstände oder Commits geändert.

Getestet: neun Schnittvarianten ohne vorbereitende Klingentextur links;
rote Materialquelle bei allen drei Vendetta-Varianten tatsächlich gezeichnet.
Alter Dreiervergleich lädt. Nass mit beiden Figuren an fünf Zeitpunkten,
Schutzpose und Bedienung geprüft. Keine Lade- oder JavaScriptfehler.
Die rote Spur am Ziel zusätzlich als Bild angesehen. Gestalterische Abnahme
durch den Nutzer steht noch aus.

## Längere, flachere Spuren und kräftiger Vendetta-Treffer

Alle Klingenspuren sind 30 Prozent länger und 38 Prozent niedriger. Vendetta
zeigt jetzt Hurt statt Schutz, einen stärkeren örtlichen Rückstoß, kurz dosiertes
Kamerarütteln und einen roten Reflex. Hurt bleibt 1,75 Sekunden sichtbar und
kehrt über 0,50 Sekunden zurück; der Ablauf wurde entsprechend verlängert.
Die drei roten Varianten behalten ihre unterschiedlichen Schnittfolgen.

Die frühere Einordnung von Vendetta als reine Statusaktion ist durch die
Nutzervorgabe ersetzt: Vendetta tut direkt weh und verursacht Blutung. Die
Vorschau-Beschreibung wurde angepasst. Konkrete Schadenswerte wurden nicht
erfunden oder in den echten Kampf eingebaut; die Änderung betrifft die
Darstellung und den beschriebenen Angriffsentwurf.

Geprüft: neun Schnittvarianten ohne linken Vorbereitungsschnitt; drei
Vendetta-Varianten zeichnen die rote Spur, die flacheren Maße und die Hurt-Pose
sowohl direkt nach dem Kontakt als auch 1,6 Sekunden später. Keine Browserfehler.
Die neue Darstellung zusätzlich als Bild angesehen. Sicherung:
`quellen/slashes-laenger-wucht/`.


## Rote Körperladung mit Funken

Geschrieben: Waffenunabhängige rote Ladung an Oberkörper und Schultern, deutlich mehr Funken als Doppio Gioco (96 statt 32 Partikel pro Zeichenaufruf). Ein Teil zieht ein, ein Teil springt als kurze Glutfunken vom Körper ab. Die Ladung entlädt sich mit dem sichtbaren Beginn des roten Wischers. Bei der Rückhand-Variante bleibt nach dem ersten Kontakt Restenergie, die für den zweiten Schnitt erneut verdichtet wird. Keine Waffenmasken oder Säbelfärbung.

Eingebaut: Alle drei Vendetta-Varianten im isolierten Effektlabor. Freisetzung von 2 auf 2,85 Sekunden verschoben, sichtbarer Energieaufbau rund 2,6 bis 2,8 Sekunden je Variante. Schnitte, Trefferabstände, Hurt und Rückstoß behalten ihre Geschwindigkeit. Das bestehende Körperladungsmodul doppio-ladung.js zeichnet Violett für Doppio und Rot für Vendetta; die Materialcache-Zuordnung enthält die Fähigkeit, damit ein Wechsel die Farben korrekt aktualisiert. Keine neue JangaFX-Simulation, keine Originalbild- oder Kampfregeländerung. Sicherung unter quellen/vendetta-koerperladung-v1.

Getestet: Alle drei Varianten in Aufbau, Kontakt und Nachlauf, Ladung vor dem Schnitt und vollständiges Erlöschen nach der Entladung. Bilder von Aufbau und rotem Kontakt visuell geprüft. Vorhandene Vendetta-Prüfung bestätigt lange flache Wischer und Hurt bei Kontakt sowie im Nachlauf. Doppio-Gegenprobe mit allen sechs violetten Kontakten und Hurt erfolgreich. Keine Browserfehler. Repo und bediente Kopie synchron.


Aktueller Stand: Kräftigere Ladung mit dichterem roten Dunst, zusätzlicher bewegter Energieschicht, stärkerem Licht und 144 statt 96 längeren Funken. Aufbau jetzt bei allen drei Varianten genau drei Sekunden vor Beginn des ersten sichtbaren Wischers; im letzten Teil bleibt die Ladung voll. Dazu Freisetzungszeit auf 3,25 Sekunden verschoben, Beginn der Körperladung aus dem ersten Wischerzeitpunkt minus drei Sekunden abgeleitet. Schnittabstände, Wischtempo und Hurt unverändert. Drei-Sekunden-Verlauf aller Varianten geprüft, Aufbau visuell geprüft; bestehende Vendetta-Prüfung mit Kontakt und spätem Hurt erfolgreich. Keine Browserfehler. Sicherung unter quellen/vendetta-kraft-3sek-v2.
