# Gegner, Duc und Kampfgeräusche – Hörlabor

38 neue Bausteine × 4 Varianten = 152 Aufnahmen. Erzeugt mit ElevenLabs über den vorhandenen lokalen Generator, ohne dessen Quelltext zu ändern. Kosten aus 162 Sekunden angeforderter Audiolänge mit dem zuletzt beobachteten Tarif geschätzt: 1.620 Credits; keine Abfrage des tatsächlichen Kontostands.

Die Spielregeln, Kampfdefinitionen und Client-Dateien wurden nicht verändert. `zuordnung.json` enthält Vorschläge zur späteren Kopplung und die Herkunft aus dem aktuellen Gegnerkatalog. Keine automatische Freigabe, kein Commit.

## Zuordnung und Timing

- Deckung einnehmen: `guard_raise` einmal beim Wechsel in die Guard-Pose, ohne Schmerzenslaut.
- Abgefangener Treffer: `guard_body`; bei Klinge gegen Klinge `parry_blade`. Eine perfekte Parade darf betonter sein, ohne neue Spielregel.
- Ausweichen: `dodge_step` auf den Bewegungsbeginn, kein zusätzlicher Trefferkontakt.
- Waffen: Bewegung kurz vor dem Kontakt; Schmerz nur bei tatsächlichem Schaden. Fünf Waffentypen brauchen keine fünf verschiedenen Stimmen oder Rüstungssounds.
- Windup und Heavy-Windup: kurze Körper-/Kleidungsbewegung, nicht bereits der komplette Treffer. Für schwere Angriffe `duc_effort` nach Auswahl zuschalten.
- Hurt: `duc_hurt` als kurze trockene Körperreaktion; kein Huhuhu oder langer Schrei. Tiere erhalten eigene kurze Trefferreaktionen.
- Nass und erschüttert ohne Schaden: Schutzpose und Zustandsgeräusch, kein Hurt-/Schmerzenssound.
- Zustände nur bei Eintritt, Verstärkung oder Reaktion vertonen; nicht bei jedem Rendern, Polling oder Sprite-Bildwechsel.
- Ein Statusende nutzt `state_recover` nur wenn es als hörbare Erholung sinnvoll ist. Kein Ton für jede ablaufende Zahl, Skip oder Leerlauf.
- Spezialattacken behalten ihre gewählten Bausteine. Feuer und Wasser aus Runde 3 bleiben als noch nicht freigegebene Quellen markiert.
- Rudel-Ratten, Rudel-Hunde, Keiler und Ziege aus dem Hafenkampf bleiben Begegnungsstart-Töne. Diese neuen kurzen Aktionen ersetzen sie nicht.

## Dateien

- `index.html`: eigenständige Auswahlseite mit Gruppen, Vorhören, Vergleich und JSON-Export.
- `katalog.json`: lokale OGG-Hörproben mit Prüfsummen und Herkunft.
- `zuordnung.json`: Gegneraktionen und vorhandene Bausteine.
- Audio-Originale und WAV-Master liegen separat im Arbeitsordner; keine Schlüssel im Katalog.

Lautstärke angeglichen, Originaltonhöhe beibehalten. Hörabnahme durch Duc steht aus.
