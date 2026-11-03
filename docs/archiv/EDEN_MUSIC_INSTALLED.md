# Eden-Musik – eingebauter Stand

Stand: 18.10.2026. Die erste Wiedergabe ist aktiv, der frühere Entwurf ist keine Beschreibung des Iststands.

- Bibliothek: `musik/eden_rise/bibliothek.json`, lokale Kopien unter `musik/eden_rise/audio/` (Git-ignoriert). Importiert wurden ausschließlich die 9 behaltenen Takes der vier angeforderten Gruppen: Hauptthema (3), Deck (3), Frühstück (2), Hafen (1). Keine automatische Freigabe zukünftiger Takes.
- Auswahl: `kern/musik.py`. Titel/Persona/Prolog nehmen das neueste behaltene Hauptthema. Deck- und Frühstücksvarianten werden anhand eines stabilen Hashes von Durchlauf/Tag/Phase/Szene gewählt; wiederholte Zustandsabfragen ändern den Track nicht und verbrauchen keinen Spielzufall.
- Szenen: tagsüber Deck-Orte → Deck; Frühstücksphase → Frühstück; Landgang/Hafen → Hafen. Nacht, Events, Kabine, Telefon-Szenen und ausdrücklich ausgeschlossene besondere Storyszenen bleiben vorerst still. `blackout` stoppt ohne Übergang. Keine globale Hauptthema-Rückfallebene während des Spiels.
- Server: `ansicht()` liefert `musik` und `musik_titel`, ohne lokale Pfade. `/musik/audio/<id>` streamt nur Bibliotheksdateien, unterstützt HTTP Range/206 und begrenzte Lese-Blöcke. Öffentliche Plugin-Dateien sind fest zugelassen.
- Player: `client/plugins/eden-music/`. Zwei dauerhafte Audiospuren, Übergang 1,8 s, Loop, eigener Ein/Aus-Knopf und Lautstärkeregler unten links. Beginnt nach Benutzerinteraktion. Einstellungen lokal gespeichert. Musik bleibt bei 1x unabhängig vom Sprechtempo und wird bei tatsächlich spielender Sprache auf 28 % abgesenkt; mehrere gleichzeitig spielende Stimmen werden berücksichtigt.
- Tests: `tests/test_musik.py` (Zuordnung/Stille, stabile Auswahl ohne Spiel-RNG, Bibliotheksdateien, HTTP-Range und Pfadprüfung); `tests/test_musik_player.cjs` (Start, Tempo, Redraw, parallele Stimmen, Übergang, Blackout, Mute). Titelbild und Musikstart im Browser geprüft. Keine vollständige Spielsitzung durchgeführt; Spielmodell war nicht gestartet. Loops sind noch nicht auf nahtlose Schnittpunkte kuratiert.

Start wie gewohnt über `Start-Eden.bat`. Der reine Engine-Server wurde für den Test unter `http://127.0.0.1:8308` gestartet und danach beendet; kein zusätzliches Sprachmodell geladen. Bei bereits laufender Engine genügt Neuladen für Client-Dateien, Python-Änderungen benötigen Neustart.


UI-Korrektur: Die Musiksteuerung wurde in das Einstellungsmenü verschoben; die frühere Position unten links entfällt. Audioelemente bleiben beim Menüwechsel erhalten.


## Aktuelle Ablage und Playlist

Bibliothek jetzt unter `module/eden_rise/musik/bibliothek.json`, Audios mit sprechenden Szenen-/Variantennamen in `audio/`, Take-Metadaten in `records/`. Die ursprünglichen übernommenen ComfyUI-Dateien wurden dorthin verschoben und aus der ComfyUI-Take-Liste entfernt. Promptvorlagen bleiben bestehen.

Alle Varianten eines Slots spielen jetzt als zufällig gemischte Endlos-Playlist: jede einmal pro Runde, keine unmittelbare Wiederholung bei mehreren Varianten; ein einzelner Track wird wiederholt. Hauptthema ebenfalls im Variantenpool. Gleiche Zustandsabfragen oder Szenen mit derselben Musikgruppe starten den Track nicht neu. Browser-Auswahl beeinflusst keine Spielwürfel. Vorige Angaben zu Einzeltrack-Loop, neuestem Titeltrack und alter Bibliothekswurzel sind überholt. Engine neu starten und Browser neu laden, um die neue Ablage zu übernehmen.

Freigegeben: Takes 046 und 049 sind jetzt event_witzig_01.flac und event_ernst_01.flac in der Modulbibliothek (11 Tracks insgesamt). Ereignisse erhalten Musik nach ihrer gespeicherten Tonlage witzig/ernst; andere Event-Tonlagen bleiben zunächst still. Engine-Neustart für die neue Zuordnung erforderlich.

