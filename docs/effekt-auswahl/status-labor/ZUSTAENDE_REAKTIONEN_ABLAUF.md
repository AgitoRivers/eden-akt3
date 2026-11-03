# Zustände und Reaktionen: gemeinsamer Ablauf

Zustände: http://127.0.0.1:8337/status-labor/

Reaktionen: http://127.0.0.1:8337/status-labor/?kategorie=reaktionen

## Geschrieben

Vier Zustände und fünf Reaktionen verwenden jetzt denselben Renderer für
Figurenreaktion, Materialschichten, Körperlicht und weiche Kontur:

- Brennend: gestaffelte Flammen, warmer Reflex am Körper, leichter Rauch.
- Nass: länger sichtbare Schutzpose, dunkler feuchter Film und wandernde breite Reflexe.
- Erschüttert: anhaltendes Rütteln, Bodenrisse und wenige Steinfragmente; kein Nebel.
- Unter Strom: unregelmäßige Entladungen und passendes Körperlicht.
- Kurzschluss: nasser Film, mehrere elektrische Impulse und aufsteigender Dunst.
- Schlamm: feuchter brauner Körperfilm und unregelmäßige, bewegte Bodenflächen.
- Feuersturm: gegeneinander bewegte Flammen, elektrische Impulse und Rauch.
- Dampf: Feuer erlischt, mehrere Nebelschichten steigen auf und verlieren Dichte.
- Ausbrennen: kurzer Flammenstoß mit anschließendem Rauch und längerem Ausklang.

Nass und Erschüttert zeigen die Schutzpose; Brennend und Strom zeigen Hurt. Sie bleibt
ungefähr 2,55 Sekunden nach dem Auftakt stehen und kehrt über 0,50 Sekunden
weich zurück. Die fünf Reaktionen behalten ihre eigene Folge: ungefähr 1,15
Sekunden Hurt mit 0,42 Sekunden Erholung nach dem letzten Impuls.
Mehrere Kurzschluss- und Feuersturmimpulse setzen diese Reaktion erneut an.
Die Kontur folgt der Pose. Bei Erschüttert rüttelt der Sprite über den Zustand
weiter; eine kurze Bodenreaktion ersetzt die Wolke vollständig.

Der neue Entwurf zeichnet mit 1200 × 1120 Pixeln bei unveränderter Anzeigegröße.
Diese Darstellungsauflösung erhöht nicht die Details der vorhandenen Texturen.
Die akzeptierten IlluGen-Materialien bleiben die Grundlage; keine neuen
nativen Simulationsexporte und keine kreisförmigen Begrenzungen der Wolken.

## Eingebaut

Nur in der separaten Vorschau auf Port 8337. Links bleibt die bisherige
Darstellung, rechts steht der neue gemeinsame Renderer. Zeitregler, Neustart
und Zeitlupe sind auch für Zustände und Reaktionen verfügbar. Ein Zyklus dauert
4,2 Sekunden; dauerhaft angezeigte Zustände bleiben während der Erholung aktiv.
Die Wiederholung ist eine Vorschaufunktion und verursacht keinen Schaden im Spiel.

Dateien: `zustand-reaktionen.js`, `labor.js`, `index.html`.
Sicherungen: `quellen/zustaende-reaktionen-neu/`.
Rückmeldeschlüssel und Exportformat sind unverändert. Kein Eingriff in den
echten Kampf, Spielstände oder fremde Änderungen; kein Commit und kein Push.

## Getestet

Alle neun Effekte an vier Zeitpunkten geprüft. Tatsächlich gezeichnete
Treffer-/Abwehrpose beim Auftakt und Rückkehr zur normalen Pose am Ende
kontrolliert. Alle neun neuen Darstellungen zusätzlich als Bilder angesehen.

Pause, Abspielen, Zeitregler, Zeitlupe, Neustart, heller Hintergrund,
Figur ein/aus, schmale Darstellung, Rückmeldungen nach Neuladen und Download
geprüft. Keine Lade- oder JavaScriptfehler. Tests mit separatem Edge-Profil
und ausgeschalteter GPU-Beschleunigung.

Prüfergebnis: `quellen/zustaende-reaktionen-neu/pruefung.json`.

## Breiterer Tornado

Der zuvor abgestimmte schmale Tornado bleibt bei Mistral als Variante 1 erhalten.
Variante 2 ist jetzt der breitere, bauchigere Sogwirbel mit langsamer gewundener
Strömung. Variante 1 wurde an drei Zeitpunkten pixelgleich mit der gesicherten
Fassung verglichen; Variante 2 ist sichtbar verändert und visuell kontrolliert.
Keine Browserfehler. Sicherungen: `quellen/tornado-breiter/`.

## Ergänzte Spielwirkungen unter den Spezialattacken

In der gemeinsamen Ablaufseite und der Dreiervergleichsseite stehen jetzt
Angriffstyp, Pfad, Freischaltstufe, Ausdauerkosten und Spielwirkung unter dem
Effekt. Grundlage: `werkzeuge/kampf_balance_v3.py`, die Überschreibungen in
`werkzeuge/kampf_balance_v4.py` und `docs/wiki/systeme/kampf.md` (Gesamt-Balancing).
Diese Dateien wurden nur gelesen; die Simulation wurde nicht gestartet.
Die Texte sind als Kampfplan/Balancingstand gekennzeichnet, weil die Vorschau
keine Regeln ausführt. Insbesondere Point de Mire ist als Erschöpfung für
3 Runden ohne direkten Schaden und Pluie d’Étoiles mit 3 × 85 % beschrieben.

Zusätzlich geprüft: alle vier Zustände zeigen bei 2,5 Sekunden tatsächlich
die Hurt-Pose; Nass verwendet jetzt die Schutzpose. Das Rütteln bei Erschüttert wurde an drei
späten Zeitpunkten anhand der gezeichneten Spritepositionen geprüft.
Alle zwölf Erklärungen und neun Effektabläufe ohne Browserfehler geprüft.
Hurt und Bodenreaktion sowie die Erklärung unter Mistral visuell kontrolliert.
Sicherungen: `quellen/hurt-boden-spielwirkung/`.

Aktuelle Material- und Posenabnahme: BODENBRUCH_QUALITAET.md. Der Bodenbruch verwendet jetzt die erzeugte Steintextur statt gezeichneter Linien und einfacher Polygone.
