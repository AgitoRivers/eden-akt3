# Eden Music – vorbereiteter Einbau

Stand: 18.10.2026, Engine `master`, Ausgangscommit `2a05f1b`. Dies ist die Einbauvorbereitung; Hintergrundmusik und Verwaltungsrouten sind noch nicht aktiviert.

## Geprüfter Iststand

- Die letzten Änderungen betreffen Missionsausbau, Missionsoberfläche und Ortswahl. Das Arbeitsverzeichnis war vor dieser Vorbereitung sauber.
- `eden.py` verwendet `ThreadingHTTPServer`; GET und POST werden in `Handler.do_GET` / `Handler.do_POST` geroutet. `ansicht()` baut die Clientansicht.
- `/api/audio`, `/api/zeile` und `/api/stimme_probe` sowie `kern/stimme.py` bedienen Sprachausgabe. Eine Hintergrundmusikbibliothek, ein Musikplayer und Musikrouten existieren noch nicht.
- Der Client erzeugt mehrere Audioobjekte: Szenenstimmen, Händler, Ereignisse und Stimmproben. `mitTempo()` registriert sie in `laufendeAudios`; `tempoSetzen()` ändert ihre Abspielgeschwindigkeit. Musik darf diesen Weg nicht verwenden.
- `zeichnen()` baut die Ansicht wiederholt auf; `laden()` und die erfolgreichen Spieleraktionen liefern neue Zustände. Während einer Aktion erfolgt zusätzlich ein Polling alle 1,1 Sekunden. Ein Musikplayer muss außerhalb der neu aufgebauten Ansichtsbereiche leben und wiederholte Zustände ohne Neustart übernehmen.
- Der Würfel-Client hält die Darstellung der POST-Antwort bis nach der Animation zurück. Der Musikwechsel muss zum übernommenen Darstellungszustand passen und darf keine kommende Szene vorwegnehmen.
- Szenen-ID und Ort stehen intern unter `z['szene']['def']['id'/'ort']`. Der öffentliche Szenenblock enthält aktuell nur Titel und Bild; daraus lassen sich keine zuverlässigen Musik-IDs ableiten. Das Backend soll einen kleinen öffentlichen Musikhinweis liefern.
- Kabine und Ereignisse haben eigene Darstellungswege. Ereignis-Orte und laufende Szenen dürfen nicht aus dem Hintergrund-Dateinamen geraten werden.
- `module/eden_rise` wird aus `werkzeuge/eden_rise` gebaut. Die Musikzuordnung soll eine eigene Quelle und Sidecar-Datei erhalten; generierte Storydateien nicht von Hand ändern.
- ComfyUI liefert bereits `output/eden_music/{drafts,kept,rejected}` und `records/<take-id>.json` mit Titel, Caption, Lyrics, Seed, geplanter und tatsächlicher Dauer. Beim Check lagen dort noch keine Takes. Der offizielle ältere Workflow speichert separat und wird dadurch nicht erfasst.

## Zielablauf

### Klangrichtung, ergänzt am 18.10.2026

Als musikalische Referenz hat Duc Sal Da Vincis **Per sempre sì** genannt (Titel bestätigt über die [offizielle Teilnehmerseite](https://www.eurovision.com/eurovision-song-contest/vienna-2026/participants/sal-da-vinci/)). Für Eden Rise wird daraus eine eigene instrumentale Klangrichtung entwickelt: italienischer romantischer Pop, kantable Melodik, warmes Piano und Nylongitarre, fließende Streicher und ein sanft wiegender Pop-Groove. Das ist eine kreative Gestaltungsvorgabe, keine Transkription oder Analyse von Tempo, Tonart oder Partitur des Referenzstücks.

Die CSV wurde entsprechend aktualisiert: Hauptthema, Deck, Frühstück, Charter-Party, Meeresleuchten, Hafen, Bar, Nacht, Nähe, Crew-Essen, Festa und Calvi. Das Titelthema darf eine deutliche Vordergrundmelodie und einen emotionalen Aufbau haben. Die Dialogversionen bleiben kleiner und zurückhaltender. Reparatur, Ermittlung, Bericht und Sturm behalten ihre zuvor getrennte musikalische Funktion. Alle 16 Zeilen bleiben instrumental; Titel, Reihenfolge und Längen bleiben erhalten.

Gleiche Textbeschreibungen erzeugen keine garantiert identische Melodie zwischen getrennten MiniMax-Läufen. Für ein später wirklich wiederkehrendes Leitmotiv zuerst einen Titel-Take auswählen und die Wiederverwendung musikalisch beziehungsweise mit einem geeigneten Referenz-/Bearbeitungsworkflow prüfen. Die Engine-Zuordnung verlangt zunächst nur passende kuratierte Tracks, keine behauptete melodische Identität.

1. In ComfyUI einen Take anhören und behalten.
2. In Eden unter Einstellungen → Musik **Behaltene Takes übernehmen** wählen.
3. Eden zeigt neue Dateien mit Titel, tatsächlicher Länge, Quelle, Prompt und Seed als **Ungeprüft**.
4. Track vorhören, Lautstärke pro Track abstimmen, einem oder mehreren Musikslots zuweisen und **Freigeben**.
5. Nur freigegebene Tracks werden im Spiel verwendet. **Archivieren** nimmt einen Track aus der Auswahl, ohne die Datei zu löschen.

ComfyUI entscheidet über die Qualität eines Takes, Eden über dessen Einsatz. Ein in ComfyUI behaltener Take ist daher in Eden nicht automatisch freigegeben. Die CSV-Zeile ist nur ein Zuordnungsvorschlag; dauerhafte Track-IDs dürfen nicht von Zeilennummern oder bearbeitbaren Titeln abhängen.

## Zuständigkeiten beim Einbau

| Datei | Aufgabe |
|---|---|
| `kern/musik.py` (neu) | Lokale Bibliothek, Import, Status und Zuordnung, Auswahl eines freigegebenen Tracks, Prüfung von Medienpfaden |
| `client/plugins/eden-music/eden-music.js` (neu) | Dauerhafter Player mit zwei Audiospuren, Übergang, Loop, Lautstärke, Vorhören und Sprachabsenkung |
| `client/plugins/eden-music/eden-music.css` (neu) | Gekapselte Bibliotheksoberfläche im vorhandenen Engine-Stil |
| `eden.py` | Kleine HTTP-Adapter, sicherer Medienstream, Musikhinweis in `ansicht()` |
| `client/index.html` | Einstellungen → Musik, Plugin laden, übernommenen Zustand weitergeben, Sprecher-Audio anmelden |
| `werkzeuge/eden_rise/musik_eden_rise.py` (neu) | Quelle der Eden-Rise-Musikslots und der geprüften Szenen-/Ortszuordnung |
| `module/eden_rise/musik.json` (neu, erzeugt) | Öffentliche modulbezogene Slots, Regeln, explizite Stille |
| `musik/<modul>/bibliothek.json` und `musik/<modul>/audio/` (neu, lokal) | Dauerhafte kuratierte Bibliothek und importierte Originaldateien; Medien und lokale Bibliothek beim Einbau in `.gitignore` aufnehmen |

Die Zuordnungsgrundlage liegt vorerst in `docs/archiv/eden_rise_musik.entwurf.json`. Sie wird aktuell von keiner Engine-Datei eingelesen.

## Auswahl und öffentlicher Vertrag

Reihenfolge: **explizite Stille → Szene → Ort mit Phase → Ort → Bereich mit Phase → Bereich → Modulstandard**. Ein ausdrücklich stiller Treffer beendet die Suche. Fehlt dagegen eine Audiodatei für einen normalen Slot, werden weniger spezifische Regeln versucht. Gibt es keine freigegebene Musik, bleibt die Engine still und spielbar.

Der Modulstandard ist zunächst nur eine Rückfallebene, kein Zwang zu ständigem Underscoring. Titelbild und Prolog erhalten eigene Regeln. Für Kabine, offene Ereignisse und Händleransichten wird die sichtbare Situation ausdrücklich bestimmt; Menü-Overlays wie Inventar ändern den musikalischen Kontext nicht. Eine Ereignis-ID hat nur dann eine eigene Musikregel, wenn sie im öffentlichen Modul-Sidecar eingetragen ist.

`ansicht()` soll ein Top-Level-Feld `musik` ergänzen, auch vor einem aktiven Spielstand. Vorgeschlagener Vertrag:

```json
{
  "kontext": "opaque-public-context-key",
  "slot": "nacht_anker",
  "stille": false,
  "track": {
    "id": "stable-library-id",
    "url": "/musik/audio/stable-library-id",
    "gain": 0.7,
    "loop": true
  },
  "uebergang_ms": 5000
}
```

Ohne Treffer: `track: null`. Bei expliziter Stille zusätzlich `stille: true`; Musik sofort beziehungsweise entsprechend der Regel ausblenden, keine Ersatzsuche. Öffentliche Hinweise enthalten keine versteckten Fall-IDs, Täterinformationen, internen Regienotizen oder absoluten Dateipfade. Die Musikauswahl verbraucht keinen Spielwürfel-Zufall und verändert weder Spielstand noch Regeln. Bei mehreren freigegebenen Varianten wird beim Kontexteintritt stabil ausgewählt, nicht bei jedem GET oder Dialogsatz neu. Ein neuer Kontext mit derselben Track-ID startet die Datei nicht erneut.

**Blackout:** `blackout` fordert einen harten Musikstopp. Die Party endet laut Szenenvorgabe mit dem Ausfall. Erst nach dem Wechsel in eine folgende Szene darf die nächste Musik beginnen; es gibt keinen neuen Effekt oder Musikbeginn allein durch einen weiteren Dialogsatz.

**Meeresleuchten:** Der Slot existiert als kuratierbares Angebot. Aktuell gibt es dafür keine eigene feste Szene in `buehne.json`; deshalb keine automatische Zuordnung allein aufgrund des Nachtorts.

## Player und Sprache

- Ein eigener Musikplayer bleibt über `zeichnen()` hinweg bestehen. Zwei Audioelemente ermöglichen Crossfades; die Grundlautstärke, Stummschaltung und Aktivierung werden lokal gespeichert.
- Beginn nach einer Benutzerinteraktion; bei blockiertem Autoplay ein sichtbarer Startknopf. Fehler beim Laden blockieren keine Aktion und keine Sprachausgabe.
- Voreinstellungen: Crossfade 5 s, Sprachabsenkung auf 30 % des eingestellten Musikpegels, Absenkung etwa 150 ms, Rückkehr etwa 700 ms. Das sind abstimmbare Startwerte, keine gemessene Lautheitsnormalisierung.
- Sprachaktivität anhand realer `playing`/`pause`/`ended`/`error`-Ereignisse verwalten, nicht während TTS-Berechnung oder Download. Mehrere gleichzeitig aktive Stimmen brauchen einen Zähler beziehungsweise eine Menge; das Ende einer Stimme darf eine zweite nicht übertönen.
- Alle bisherigen Sprachwege erfassen, einschließlich Händler, Ereignisse, Toto und Stimmprobe. Musik und Bibliotheksvorschau nie mit `mitTempo()` registrieren.
- Bibliotheksvorschau pausiert beziehungsweise senkt die Spielmusik ab und stellt sie beim Schließen wieder her. Es dürfen nicht unbemerkt zwei Vorhördateien gleichzeitig laufen.
- Bereits zugespielte Dateien sind nicht automatisch nahtlose Loops. Anfang/Ende vorhören; zunächst HTML-Loop plus optionaler Loop-Crossfade, später Schnittpunkte. Ein Übergang zwischen zwei Tracks ersetzt keinen geprüften Loop innerhalb eines Tracks.

## Import und HTTP

Vorgesehene Routen, noch nicht vorhanden:

- `GET /api/musik`: Bibliothek, Slots und Importverfügbarkeit für das aktive Modul.
- `POST /api/musik/import`: ausdrücklich ausgelöster Import aus dem konfigurierten ComfyUI-Quellordner; nur `kept`, nur FLAC/MP3 und nur dazu passende Metadatensätze. Kein Scan während `/api/stand`.
- `POST /api/musik/upload`: lokale Einzel-/Mehrfachdateien, späterer unabhängiger Import; Größenlimit und Formatprüfung.
- `POST /api/musik/track`: Titel, Notiz, Gain, Slot-Zuordnungen und Status ändern; keine Spielaktion.
- `GET /musik/audio/<id>`: Audio nur über Bibliotheks-ID; begrenztes Streaming mit HTTP-Range/206 für Vorhören und Springen. Die vorhandene `Handler.datei()` liest alles in den Speicher und unterstützt derzeit kein Range, deshalb für längere Musik eine eigene kleine Streamfunktion verwenden.
- `/plugins/eden-music/...`: nur öffentliche JS/CSS-Dateien nach dem bestehenden Plugin-Routenmuster ausliefern.

Quelldateien und Engine-Dateien bleiben unabhängig: beim Import kopieren, nicht verschieben oder dauerhaft auf den ComfyUI-Pfad verweisen. Wiederholter Import erkennt bekannte Quell-Take-IDs und Audiodubletten; bereits kuratierte Titel, Notizen, Status und Zuordnungen bleiben erhalten. Spätere ComfyUI-Bewertungen löschen keine Engine-Dateien. Quelle, Caption, Lyrics, Seed sowie tatsächliche Dauer aufbewahren; die gesamte ComfyUI-Workflowstruktur muss nicht an den Spielclient gesendet werden.

Pfade serverseitig auf den konfigurierten Quellordner beziehungsweise die Medienwurzel begrenzen. Keine beliebigen Dateipfade aus Browserdaten öffnen. Bibliothek atomar speichern und Verwaltungsänderungen mit einem eigenen Lock absichern; nicht den langen LLM-Spielaktionslock für Audioauslieferung verwenden.

## Einbaureihenfolge und Prüfung

1. Bibliothek und Import mit temporären Verzeichnissen testen: erneuter Import, gleiche Datei, fehlende Metadaten, unzulässiger Pfad, Freigabe/Archivierung und dauerhafte Zuordnung.
2. Modul-Sidecar aus der Entwurfszuordnung bauen und Auswahl testen: Szenenvorrang, Nacht/Tag, Kabine/Ereignis, keine Musik, fehlende Datei und explizite Stille. Keine Veränderung an Spielwürfeln oder Referenzständen.
3. HTTP-Adapter und Streaming integrieren: Range, MIME, fehlende Datei, Ablehnung fremder IDs und Größenlimits.
4. Player und kleine Bibliotheksoberfläche verbinden. Im Vorschau-Server mit Wegwerf-Konfiguration testen; dort für Musik ebenfalls Wegwerf-Bibliothek und Medienwurzel einsetzen, damit echte Kuratierung unberührt bleibt.
5. Browserprüfung: wiederholtes Rendern/Polling startet Musik nicht neu, Tempo beeinflusst nur Sprache, Crossfade und Stille beim Blackout, Dialog-Absenkung, Vorschau, blockiertes Autoplay und Neuladen.
6. Nach Eingriffen in Engine/Client die passenden vorhandenen Tests aus `LIESMICH.md` sowie neue Musiktests ausführen. Erst danach den laufenden Spielserver neu starten.

Diese Vorbereitung ändert weder Engine-Code noch Spielstände, Konfiguration, Storydateien, Audiodateien oder laufende Server.
