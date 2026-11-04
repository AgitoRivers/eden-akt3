# Akt 3 · Bestellliste Bilder und Ton

Stand 04.11.2026 · Cloud-Sitzung `akt3-cloud`. Bis ein Bild da ist, nutzt das Spiel den genannten Platzhalter (Name aus `modul.json`, Raumliste geprüft). Hintergründe nach `docs/wiki/systeme/hintergruende.md` (keine Tür, Vordergrund unten Mitte frei, frontal, 4 Seeds).

## Hintergründe

| Name (Vorschlag) | Szene | Bildidee | Platzhalter |
|---|---|---|---|
| `town_hall_stairs` | 5.11 Don vor Pascals Tür | schmale Steintreppe im Rathaus, Kisten am Fuß, Licht von oben | `village_piazza` |
| `pascal_room` | 5.12 Die Schublade | kleines Zimmer über dem Rathaus, Schreibtisch mit Schubladen, weißer Fedora an einem Haken, ordentlich wie ein Museum | `village_piazza` |
| `burned_post` (und je ein Bild für `batu`, `bar`, `werkstatt`) | Baustellen in drei Stufen | verkohltes Haus, Gerüst, später fast fertig; Piraten nur als Werkzeug am Boden, keine Personen | `village_harbour` |
| `villa_cellar` | 5.25 Frame 1–2 | alter Weinkeller, Fässer, dazwischen ein Server-Rack mit blauen Lichtern | `power_room` |
| `villa_office` | 5.25 Frame 3 | Büro unter einer Treppe, ein Ordner auf dem Tisch, altes Familienfoto an der Wand | `main_salon` |
| `villa_dining` | 5.26 Name Your Price | langer Tisch für zwei, großes Fenster auf die Bucht bei Nacht, Dorf mit Lichtern unten | `alon_keynote` |
| `scrap_field` | Expedition „The Scrap Field“ (F-10) | Macchia mit liegengebliebenen weißen Robotern, Gras durch die Gelenke | Rastplatz-Bild der Macchia |
| `church` bei Nacht, außen | 5.13 Every Report | Kirchenstufen mit Kerzen | `village_piazza` |

## Sprites und Posen

| Figur | Pose / Gefühl | Szene | Bildidee |
|---|---|---|---|
| Minicu | verbunden, ernst, neutral frontal | 5.1, 5.4 | Kopfverband, Arm in einer Schlinge, Axt gesenkt |
| Alva | verletzt, liegend/sitzend, ernst | 5.3 | Verband an der Schläfe, Decke |
| Sandru | am Boden, ernst (ohne surrende Schienen) | 5.19 | zwischen weißen Regalen |
| Sandru | neue Schienen, stehend, ruhig | 5.20 | Schienen mit Rosis Farbe, Namensschild ISKANDER oder SANDRU |
| Buenaventura | ohne Hut, ernst | 5.2 | Hut in der Hand, Flagge auf halbmast im Hintergrund |
| Alon | in Person, Anzug über dem Exoskelett, ruhig | 5.26 | Kanon-Look, aber ohne Bühne |
| U Riscossore | mit Orange, ruhig | 5.17, 5.30 | Kanon-Look |
| Kommissarin | neutral, ernst | 5.30 | Beamtin aus Ajaccio, Klapptisch, Ordner (neue Nebenfigur, Legenden-Kommentar nötig) |
| Pascal | im weißen Fedora hinter Alon, lächelnd | 5.26 | keine Zeile, nur Bild |

## Items

| Item | Bild |
|---|---|
| Cellar Key | alter Eisenschlüssel mit Bändchen von einer Setzlingskiste |
| Pascal's Ledger | Kassenbuch in sauberer Handschrift |
| White's Orders | Ordner mit Einsatzplan, Stempel „Phase 3“ |

## Ton

Kein `ton` auf Kartenzeilen ohne gewählte Datei (`test_sfx`). Gewünscht, noch nicht gesetzt:

| Klang | Szene |
|---|---|
| Schienen verstummen (Surren bricht ab) | 5.19 |
| Tropfen in einen Eimer | 5.14, 5.30 |
| Brecheisen an Holz | 5.12 |
| Vespa-Hupe zweimal | Dank-Szene Post |
| Glocke im richtigen Takt (gibt es vielleicht schon als `tk_glocke`) | 5.32 |
