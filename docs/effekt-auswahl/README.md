# Eden Rise – Effektauswahl

**Aktuell, 24.10.2026:** Alle 16 Spezialangriffe sind freigegeben. Verbindliche Varianten und Einbaustatus: [SPEZIALANGRIFFE_FREIGABE.md](SPEZIALANGRIFFE_FREIGABE.md). Die aktuelle Ablaufvorschau liegt in `status-labor/ablaufprobe/`. Die folgenden Abschnitte beschreiben die frühere Hauptgalerie.

Stand: 22.10.2026. Eigenständige Auswahlseite mit **81 Effekten und 243 animierten Entwürfen**.

## Öffnen und auswählen

`X:\AI\Eden\docs\effekt-auswahl\index.html` im Browser öffnen, oder die danebenliegende `Start-Auswahl.bat` doppelklicken.
Es ist kein laufender Eden-Server nötig. Alle Bilder, Skripte und Daten liegen lokal.

1. Einen Effekt im Katalog wählen. In schmalen Fenstern öffnet der Knopf „Katalog“ die Liste.
2. „Vergleich abspielen“ startet die drei Varianten gleichzeitig. Die kleinen Play-Knöpfe spielen sie einzeln ab.
3. Variante 1, 2 oder 3 wählen und bei Bedarf einen Änderungswunsch eintragen.
4. Mit „Zum nächsten offenen Effekt“ weitergehen. Suche und Bereichsfilter helfen beim späteren Vergleichen.
5. **„Auswahl herunterladen“** sichert alle Entscheidungen und Notizen als JSON-Datei. Diese Datei kann wieder importiert und als Grundlage für den Engine-Einbau verwendet werden.

Die Browser-Auswahl wird automatisch lokal gespeichert. Sie ist an diesen Browser und diesen Datei-/Seitenort gebunden.
Eine heruntergeladene Auswahldatei ist die übertragbare Sicherung. Import ergänzt bzw. ersetzt die in der Datei genannten
Entscheidungen; der vorherige Stand wird im Browser unter `eden-rise-effektauswahl-v1-vor-import` gesichert.

Auf der Bühne lassen sich Testfigur, reiner Effekt auf dunklem Grund und heller Grund vergleichen. Kampfzustände können
auch auf der Duc-Karte dargestellt werden. Einträge mit mehreren Ausprägungen haben zusätzliche Knöpfe, etwa Feuer/Wasser,
Kochqualität, Geschenkreaktion und Kampfende. Diese Ausprägung wird mitgesichert.

Reduzierte Bewegung des Betriebssystems wird beachtet. Animationen starten grundsätzlich erst nach einem Klick;
Wiederholen ist optional. Die Seite pausiert beim Wechsel in einen anderen Tab.

## Was tatsächlich erzeugt wurde

- Drei Canvas-Kompositionen je Eintrag der bestehenden Effekt-Inventur: dezent, dynamisch und filmisch.
- 243 transparente Vorschau-Bilderbögen in `assets/varianten`: je 24 Bilder, sechs Spalten und vier Zeilen,
  je Bild 256 × 196 Pixel. Zusammen 5.832 Einzelbilder. Die jeweilige Laufzeit steht im Katalog.
- Aufbereitete Vorschautexturen aus 13 lokal installierten IlluGen-Vorlagen; Figur und Posen aus der bestehenden Kampf-Testfigur.
- Quelle, Prüfsumme, Aufteilung und Herkunft der Vorschautexturen in `quellen/illugen-vorschauen.json`.
- Originalvorlagen als Kopien in `quellen/illugen-projekte`, eingebettete Originalvorschauen in `quellen/vorlagen-vorschauen`.
- Ein vollständig lokaler Katalog samt nachvollziehbaren Varianteneinstellungen, Auswahl und Notizen.

**Es sind keine 243 neu in IlluGen gebauten Projekte und keine fertigen Produktionsrender.**
Der direkte Exportversuch über die IlluGen-Oberfläche lieferte zunächst eine technische Pack-Textur statt eines fertigen
Schnitts. Diese Ausgabe wird nicht als Effekt verwendet. Für die fertige Auswahl wurden deshalb die vorhandenen
IlluGen-Vorlagenvorschauen verwendet. Ihre Auflösung und die vereinfachte Aufbereitung begrenzen die Qualität.

Die Vorschauen dienen zur Entscheidung über Form, Bewegung, Stärke und Aufbau. Nach der Auswahl müssen die passenden
IlluGen-Graphen für Produktionsauflösung und saubere Transparenz eingerichtet, exportiert und in der isolierten
Kampfkopie geprüft werden. Soundabstimmung, finale Anker und Engine-Einbau stehen ebenfalls aus. Die lokale Vorlage
enthält teilweise 3D-Meshes bzw. Materialtexturen; eine Vorlagenkopie ist noch kein passender 2D-Export.

Keine Loch-, Tropfen-, Blasen- oder Punktwolken-Muster werden als Gestaltungsmittel verwendet. Einzeltropfenwolken,
Waben-Schilde und ähnliche ungeeignete Vorlagen wurden ausgeschlossen. Blut erscheint als Streifen. Die Vorschau ist
eine erste Sichtprüfung, keine Garantie, dass jeder spätere Produktionsrender dieselben Eigenschaften besitzt.

## Nachbauen

Mit dem vorhandenen ComfyUI-Python, ohne Installation zusätzlicher Pakete:

```powershell
& 'X:\AI\ComfyUI_krea2\python_embeded\python.exe' 'X:\AI\Eden\werkzeuge\eden_rise\effekt_vorschau_quellen.py'
& 'X:\AI\ComfyUI_krea2\python_embeded\python.exe' 'X:\AI\Eden\werkzeuge\eden_rise\effekt_auswahl.py'
```

Das erste Werkzeug nutzt das bereits vorhandene Pillow zur Aufbereitung der Bilder. Das zweite verwendet nur die
Standardbibliothek und erzeugt `katalog.json` sowie `katalog.js` aus Inventur und Rezepten. Entscheidungen liegen
im Browser bzw. in der heruntergeladenen Auswahldatei und werden durch einen Neubau nicht überschrieben.

Die transparenten Vorschau-Bilderbögen werden mit `werkzeuge/eden_rise/effekt_export.cjs` erzeugt. Dafür wurde das bereits
vorhandene Canvas-Paket der lokalen Codex-Werkzeuge verwendet; es wurde nichts installiert. Der Aufruf auf diesem Rechner:

```powershell
& 'C:\Users\DucNg\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe' 'X:\AI\Eden\werkzeuge\eden_rise\effekt_export.cjs' --canvas-module 'C:\Users\DucNg\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules\@napi-rs\canvas'
& 'X:\AI\ComfyUI_krea2\python_embeded\python.exe' 'X:\AI\Eden\werkzeuge\eden_rise\effekt_auswahl.py'
```

Der Canvas-Export ist eine eigene Vorschau-Aufbereitung. Er steuert IlluGen nicht und erzeugt keine IlluGen-Produktionsrender.

HTML, CSS und JavaScript gehören ausschließlich zu dieser Vorschau. Es gibt keine Abhängigkeit von Eden-Konfiguration,
Sprachmodell, API-Schlüsseln, Spielständen oder der laufenden App. Keine Kampfregeln wurden geändert.
