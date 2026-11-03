# Eden Rise – Soundlabor

31 einzelne Klangbausteine, je vier Varianten: aktuell 120 ElevenLabs-Aufnahmen
und vier eigene, rein aus Rauschen gestaltete Druckstudien. Die Bausteine sind
geordnet nach Klinge/Schatten, Feuer, Wasser, Wind, Schall, Licht/Sternen und
Treffer/Körper. Alle 16 Spezialattacken sind im Katalog zugeordnet.

Vier eigene Prompts pro Baustein: A trocken/realistisch, B schwer/druckvoll,
C schnell/präzise, D rau/charaktervoll. Keine veränderte Kopie desselben Takes.
Gewünschte Aufnahmelängen zwischen 0,8 und 3,5 Sekunden; Originaldauer laut
Anbieter kann geringfügig abweichen. Keine Musik, Stimmen, Harfen oder Chöre
bestellt. Ob jede Generierung diese Vorgaben hörbar erfüllt, entscheidet die
Hörabnahme; Prompts und technische Messungen ersetzen sie nicht.

## Nutzung

http://127.0.0.1:8337/status-labor/soundlabor/

Kategorie wählen, einzeln vorhören oder A–D nacheinander vergleichen. Ein Favorit
pro Baustein; alternativ „Keine passt“. Notizen und Auswahl werden lokal im
Browser gespeichert. „Auswahl sichern“ exportiert eden-soundauswahl.json mit
Baustein-ID, Variantenbuchstabe, Generation-ID, Datei und Notiz. Eine gesicherte
Auswahl lässt sich wieder laden. Es wird nie ungefragt abgespielt.

Nur ein Audio-Player ist gleichzeitig aktiv. Verstecken des Tabs, Filtern und
Kategorie wechseln stoppen die Wiedergabe. Das Labor verändert keine Spielstände,
ruft keine Engine-Funktionen auf und erzeugt keine Sounds im Hintergrund.

## Herkunft und Verarbeitung

Modell: eleven_text_to_sound_v2, Dauer explizit gesetzt, prompt_influence 0,55.
124 eigenständige Knoten, jeweils genau eine Generierung. Warteschlangen-Ablehnungen
wurden vor erneutem Start per Knotenstatus „not_run“ geprüft. Keine fertigen Takes
neu gestartet. Vorabschätzung aller Blöcke: 2.776 Credits. Tatsächliche Preise pro
fertiger Generierung stehen in katalog.json.

Original-MP3s bleiben im Arbeitsordner außerhalb des Repos:
C:\Users\DucNg\Documents\Codex\2026-10-17\hel\work\status-labor\sound-bank\originals

Vorschauen sind OGG Vorbis, Stereo, 48 kHz. Lautheit in zwei Durchgängen auf
-20 LUFS angeglichen, Ziel für True Peak -2 dBTP. Der Katalog enthält die
Original-Prüfsumme, Vorschau-Prüfsumme, gemessenen Sample-Peak und eine kleine
Wellenform. Originale werden nicht überschrieben. Keine RouteNote-Aufnahmen
werden in dieser neuen Auswahl verwendet. Frühere Angriffsmischungen bleiben
unverändert. Für eine Veröffentlichung sind die zum Konto gehörenden
ElevenLabs-Nutzungsrechte gesondert zu dokumentieren; diese Seite ist die lokale
Hörabnahme, keine pauschale Rechtebestätigung.

Geschrieben: Katalog, Audio-Vorschauen, Oberfläche und Auswahl-Export.
Eingebaut: eigenständige Seite im isolierten Labor auf Port 8337.
Getestet: technische Prüfungen separat im Arbeitsbericht; Hörabnahme offen.
Kein Commit, keine Änderungen an Story oder Engine.

## Körperladung korrigiert

Die vier KI-Körperladungen wurden nach Ducs Ablehnung am 24.10.2026 ersetzt.
Neu: A trockener Luftdruck, B verdichteter Druck, C Druck mit feinem Knistern,
D raue Reibung. Ausschließlich breitbandiges Rauschen und unregelmäßige kurze
Geräuschimpulse, keine Stimmen, tonalen Oszillatoren oder Vokal-Resonatoren.
Zusätzliche Credits: 0. Die historische ElevenLabs-Ausgabe bleibt 2.776 Credits.
Alte Aufnahmen und Katalog liegen gesichert außerhalb des öffentlich bedienten
Labors. Bisherige Favoriten für die alte Körperladung werden nicht stillschweigend
auf die Ersatzdateien übertragen; Notizen und andere Favoriten bleiben erhalten.
Die neuen Druckstudien sind technisch geprüft, aber noch nicht von Duc abgehört.

## Neue Alternativen, 25.10.2026

Die Hauptseite und nacharbeit.html zeigen nun ausschließlich 40 neue Alternativen
zu den zehn Nacharbeiten. Der bisherige vollständige Katalog bleibt archiv.html.
Neue Dateien: audio/nacharbeit-v1/. Herkunft und Verarbeitung: nacharbeit-neu.json.
Vier Varianten je Baustein; keine vorherige Auswahl wird als neue Freigabe
übernommen. Eigener Speicherbereich: eden-soundnacharbeit-neu-v1. Exportdatei:
eden-soundnacharbeit-neu.json. Die 25 committeten Originaldateien sind unverändert.

16 Varianten bearbeiten gewählte Grundlagen (Nachbrennen, Wasserstoß,
Resonanzladung, Sternenfall), 16 entstehen aus lokal gestaltetem Luftdruck,
Rauschen und kurzen Impulsen (Windstoß, Schallentladung, Beam, Aufblenden).
Acht neue ElevenLabs-Aufnahmen liefern Körperkontakte und natürliches Geröll.
Zusätzliche Kosten laut Ergebnissen: 157 Credits. Alte und neue Quellen nicht
als dieselbe Auswahl behandeln. Technische Prüfung aller 40 neuen Dateien,
Wiedergabe und Export bestanden; Ducs Hörabnahme steht aus. Kein neuer Commit.


## Sound-Nacharbeit Runde 3 · 25.10.2026

20 frische ElevenLabs-Aufnahmen (5 Kategorien × 4) plus 2 lokale Überarbeitungen der gewählten Schallsounds. Kosten: 592 Credits. Hauptseite zeigt nur diese 22 neuen Hörproben. Alle vorherigen Dateien bleiben erhalten. Keine Engine- oder Spielstandsänderung.

Die fünf Favoriten aus `eden-soundnacharbeit-neu.json` sind mit Dateiprüfsummen in `freigabe-nacharbeit-runde2.json` gesichert; Geschoss B stammt aus der Notiz. Ladung B und Entladung A bleiben als Ausgangsfassungen erhalten und wurden separat überarbeitet. Keine neue Freigabe oder Commit wird daraus automatisch abgeleitet. Neue Auswahl nutzt einen eigenen Browserspeicher und exportiert weiterhin `eden-soundnacharbeit-neu.json` mit Katalogversion 3.

Technisch geprüft: 22 Dateien decodierbar, Wiedergabe, Auswahl und Export, 22 unterschiedliche Prüfsummen, 25 bereits committete Audiodateien unverändert. Hörabnahme durch Duc steht aus.
