# Neue Wasserformen und Treffer aus nativen Exporten

## Geschrieben

EmberGen 1.2.12: Beim Export erschien der Dialog zum Start der kostenlosen Testphase. `Start Trial` wurde gewählt; die App bestätigte die erfolgreiche Aktivierung und zeigt 30 Tage an. Die frühere Annahme, die Meldung `No active license` blockiere diese Arbeit dauerhaft, ist damit widerlegt.

Es wurden vier begrenzte Probeexporte erstellt:

- LiquiGen `ballistic`: 64 Bilder, Ausgangsbild 24, Schrittweite 2, 2048 × 2048. Eigene Projektkopie `quellen/native-v6/wasserstoss.liquigen`. Der Export enthält einen schwarzen Hintergrund und einen roten Helfer; sein Alpha ist vollständig undurchsichtig. Deshalb wird die Transparenz ausdrücklich rekonstruiert, nicht als nativer Alpha-Kanal ausgegeben.
- LiquiGen `fountain`: 64 Bilder, Schrittweite 4, 2048 × 2048, mit nativem Alpha. Eigene Projektkopie `quellen/native-v6/wasserausbruch.liquigen`.
- EmberGen `bullet_impact_concrete`: 64 Bilder, 2048 × 2048, mit nativem Alpha. Eigene Projektkopie `quellen/native-v6/treffer.ember`. Diese wurde vor dem Setzen des Exportverzeichnisses gespeichert; bei einem neuen Export muss der Zielordner gesetzt werden.
- LiquiGen `gushing`: ebenfalls probeweise exportiert, aber nicht eingebaut. Der kurze Ausschnitt zeigt nur einen kleinen dunklen Klumpen und erfüllt die gewünschte Form nicht.

Originale bleiben unter `quellen/native-v6` erhalten. Keine installierte Vorlage wurde überschrieben.

Die CPU-Aufbereitung entfernt winzige isolierte Fragmente, neutralisiert die violetten beziehungsweise kräftig blauen Wasserfarben, entfernt den roten Helfer beim Wasserstoß und hellt das Trefferbild auf. Beim Ausbruch wird der zu harte Ansatz weich ausgeblendet. Gemeinsame Zuschnitte für alle Bilder erhalten die Bewegung innerhalb der Animation. Die drei eingebauten Bildfolgen besitzen jeweils 64 unterschiedliche Bilder; Wasserstoß 64, Ausbruch 61 und Treffer 63 nichtleere Bilder. Leere Anfangsbilder gehören zum Anlauf.

Quelle, SHA-256, Zuschnitt und Transparenzverfahren stehen in `quellen/native-v6/integration.json`. Bildaufbereitung: `work/status-labor/native_v6_bauen.py --assets-only`. Der Einbauabschnitt dieses Skripts ist eine einmalige Migration und soll nicht erneut ausgeführt werden.

## Eingebaut

Nur im Effekte-Labor und der isolierten Vorschau auf Port 8337:

- Ressac: Wasserstoß, Wasserausbruch, Stoß mit anschließendem Ausbruch.
- Lame de Fond: schwerer Wasserstoß, zweilagiger Ausbruch, versetzter Kaskadentreffer.
- Doppelschnitt, Vendetta, gezielter Schuss und fallende Lichtangriffe: neuer gerichteter EmberGen-Treffer mit schnellerem Aufbau und längerem Materialnachlauf.

Die dritte Wasserform kombiniert die zwei brauchbaren Simulationen; es sind keine drei eigenständigen brauchbaren Simulationen. Der Ausbruch wird im Browser vertikal gespiegelt, um ihn vom Boden aufsteigen zu lassen. Die Flüssigkeitsbewegung selbst stammt aus der nativen Bildfolge.

Die Schnittfunktion und die freigegebenen Nebel- und Blitzmaterialien bleiben erhalten. Keine Änderung am Spielkampf oder an Spielständen, kein Commit und kein Push. Geändert wurden `spezial-realismus.js`, `labor.js`, `index.html`, drei Dateien unter `assets/native-v6` sowie Quellen und Dokumentation. Sicherung der vorherigen Einbindung unter `quellen/native-v6/*.vor-einbau`.

## Getestet

`work/status-labor/liquigen_pruefen.cjs`: zwölf Angriffe, 36 unterschiedliche Varianten, sieben Zeitpunkte, Speicherung und Download der dritten Wahl, Zeitregler, Pause/Abspielen, Hintergrundwechsel, ausgeblendete Figur und schmale Ansicht. Keine Browser- oder Ladefehler. Ausgeführt mit deaktivierter Browser-GPU.

`work/status-labor/native_v6_ansehen.cjs`: alle drei neuen Animationsdateien tatsächlich geladen; vier Ansichten bei 1,8 Sekunden aufgenommen. Wasserformen, Schusstreffer und Lichtfall zusätzlich visuell geprüft. Der erste Versuch dieses Prüfskripts verwendete einen für das Bereichsfeld ungültigen Zahlenstring; nach Korrektur auf `1.8` lief die Prüfung erfolgreich. Kein Produktfehler.

## Grenzen

Die Wasserbilder sind weiterhin stilisierte Simulationstests; die Farbkorrektur macht daraus noch keine fotorealistische Endfassung. Der Wasserstoß enthält rekonstruierten Alpha und erreicht stellenweise den Kamerarand. Die schmale Flächenansicht des Ausbruchs und der gerichtete Staubtreffer können weitere Gestaltung benötigen. Die neue Vorschau ist zur Auswahl und Bewertung bestimmt, nicht als endgültig freigegebene Kampfanimation.
