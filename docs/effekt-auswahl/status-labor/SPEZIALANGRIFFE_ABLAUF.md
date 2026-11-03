# Spezialattacken in der gemeinsamen Ablaufvorschau

Vorschau: http://127.0.0.1:8337/status-labor/ablaufprobe/

Angriff im Auswahlfeld wählen, darunter eine der drei Varianten anklicken.
Ein Wechsel startet den gewählten Ablauf von vorn. Pause, Zeitlupe, Zeitregler,
Neustart und Effektschalter gelten für alle Angriffe. Direkte Links unterstützen
`?angriff=doubleSlash&variante=0`; die Varianten zählen im Link ab null.

## Geschrieben

Alle zwölf vorhandenen Spezialattacken sind als gemeinsame Abläufe verfügbar.
Die Wasserkugel bleibt die freigegebene Referenz. Die übrigen Angriffe haben
eigene Bewegungen, Auftakte und Kontaktfolgen. Drei Varianten pro Angriff:

| Angriff | Variante 1 | Variante 2 | Variante 3 |
| --- | --- | --- | --- |
| Mistral | Wandernder Tornado | Breiter Sogwirbel | Zwillingswirbel |
| Ressac | Wasserlanze, Referenz | Wasserhammer | Zwillingsstoß |
| Libeccio | Zwei Nebeltrichter | Umlaufender Tornado | Sich öffnende Wirbel |
| Lame de Fond | Schwerer Druckstoß | Steigender Brecher | Doppelte Kaskade |
| Doppio Gioco | Kreuzschnitt | Finte und Rückhand | Auf und ab |
| Sotto Voce | Seitlicher Wechsel | Schleiertritt | Doppeltes Echo |
| Vendetta | Schwerer Diagonalschnitt | Verzögerte Rückhand | Steiler Hieb |
| Omertà | Schnitt im Schatten | Verdeckte Rückhand | Stiller Hieb |
| Point de Mire | Ruhiger Fokus | Wandernder Fokus | Schwäche offenlegen |
| Bonaccia | Glatte Strömung | Windstille | Tiefe Ruhe |
| Phare | Leuchtfeuer | Lichtspalt | Gegenlicht |
| Pluie d’Étoiles | Sternfolge | Schräger Sternfall | Bündelung |

Die Bühne und Darstellung mit 1920 × 1200 Pixeln sind gemeinsam. Vorbereitung
und Wirkung haben passende Zeiten: Wasser startet bei 3,12 Sekunden, die
Schnittangriffe zwischen 1,65 und 2,10 Sekunden. Mehrfachtreffer lösen jeweils
eine neue Reaktion aus. Die verlängerte Trefferpose richtet sich nach dem
letzten Kontakt. Der Ausklang verlängert sich bei versetzten Treffern, damit
keine Erholung abgeschnitten wird. Schutz, Ausweichen und ruhige Wirkungen
verwenden Abwehr, versetzte Silhouetten oder die normale Pose.

Die Schnitte bewegen die gerade silbrige Textur durch den Kontakt; sie werden
nicht nur eingeblendet. Wind nutzt bewegte Nebelfahnen, Licht nutzt weich
maskierte Lichtmaterialien und Dunst. Schüsse haben kurze bewegte Spuren und
örtliche Trefferreflexe. Die Wasserformen übernehmen die abgestimmte bewegte
Kugel und den zuletzt korrigierten Splash ohne künstlich fallende Bildfläche.

## Eingebaut

Nur in die getrennte Vorschau auf Port 8337. Der Menüeintrag
„F · Spezialattacken im Ablauf“ öffnet die gemeinsame Bühne. Die frühere
Dreiervergleichsseite bleibt als Referenz erreichbar. Ihre Rückmeldungen
werden durch die neue Ablaufseite nicht verändert.

- `ablaufprobe/angriffe.js`: Varianten, Kontaktfolgen, Vorbereitung und Materialbewegung.
- `ablaufprobe/probe.js`: gemeinsame Bühne, Figurenreaktion, Zeitsteuerung und Auswahl.
- `ablaufprobe/index.html`: Auswahl und Bedienung.
- `index.html`: Link auf die Ablaufseite.

Die vorherige freigegebene Wasserfassung ist in
`quellen/alle-ablaufangriffe/` gesichert. Originalmaterialien bleiben erhalten.
Keine Änderungen an Kampfregeln, Spielständen, Live-App oder Claude-Dateien.
Keine Commits und kein Push.

## Getestet

Mit Edge ohne GPU-Beschleunigung:

- 36 Varianten an je vier Zeitpunkten, insgesamt 144 Momentaufnahmen.
- Alle Varianten liefern unterschiedliche Abläufe; kein statischer Ablauf.
- Angriffsauswahl, Variantenwechsel, Beschreibungen, Neustart, Zeitlupe und Effektschalter.
- Schmale Darstellung ohne horizontales Überlaufen.
- Keine JavaScript- und Ladefehler.
- Die freigegebene Wasserlanze ist bei fünf geprüften Zeitpunkten pixelgleich
  mit der gesicherten vorherigen Fassung.
- Alle 36 Varianten im Kontaktbogen angesehen; acht größere Einzelansichten
  sowie die vollständige Seite zusätzlich visuell kontrolliert.

Prüfergebnis: `quellen/alle-ablaufangriffe/pruefung.json`.

## Grenzen

Das ist eine überarbeitete Vorschau, noch keine Integration in den echten
Kampf. Die technische Prüfung ersetzt die gestalterische Abnahme nicht.
Die vorhandenen Texturen werden weiterverwendet; es wurden in diesem Schritt
keine neuen LiquiGen- oder EmberGen-Simulationen exportiert. Klingenspur und
Lichtmaterial sind vorhandene erzeugte Einzelbilder mit Bewegung im Renderer;
Wasser und Nebel stammen aus den bereits vorhandenen Animationen. Höhere
Darstellungsauflösung erzeugt keine zusätzlichen Details in diesen Quellen.

## Kleine Tornados statt breiter Windstöße

Mistral und Libeccio verwenden jetzt sechs Varianten mit schmalen, rotierenden Nebeltrichtern. Eine nach oben breiter werdende, leicht gebogene Form trägt bewegte Dichtefelder und weiche spiralförmige Verdichtungen. Die Kontur ist weich und unregelmäßig; nur wenig bodennaher Dunst bleibt am Fuß. Die Form wird aus der vorhandenen Strömungstextur berechnet, kein neuer nativer Simulationsexport. Mistral zieht zum Ziel; Libeccio steht seitlich, läuft um die Figur oder öffnet sich nach außen.

In der isolierten Vorschau eingebaut. Sechs Windvarianten visuell geprüft, 36 Varianten an 144 Zeitpunkten technisch geprüft; keine Browserfehler. Wasserreferenz bei fünf Zeitpunkten weiterhin pixelgleich. Vorherige Fassung unter quellen/kleine-tornados gesichert.

Aktualisierung: Spezialeffekte ohne direkten Schaden verwenden Schutz- oder Ausweichposen. Point de Mire zeigt eine Markierung statt einer Schussbahn. Zuordnung und Prüfung: BODENBRUCH_QUALITAET.md.
