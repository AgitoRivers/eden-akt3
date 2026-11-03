# Übergabe Sitzung Story · 02.11.2026

Bereich: Belagerung Tag 15–23 als Drama („Hold the Line“), Taktik-Karte im Finale, Sounds und Vertonung der Karte, End-to-End-Spieltest bis Ende Akt 2. Kanon steht in `docs/wiki/welt/drehbuch_finale.md`, `welt/belagerung.md`, `systeme/taktik.md`, `systeme/spieltest.md`.

## Gebaut (alles auf master)

| Commit | Inhalt |
|---|---|
| 305d4c55, 26e20825, 19b00dc5 | Holm meldet, was sie sieht; Minicu neben Pascal in Welle 1–5, am Tor in Welle 6; Pascal versteckt sich in Runde 2 und kommt bei Minicus Sturz wieder; Lola und Jana schreien, Casanova nennt Pascal Verräter |
| c87c9db5, 248cacd9 | Nord-Barrikade als Bild-Overlay (`werkzeuge/barrikade_bild.py`), zu und offen von Duc abgenommen |
| 69f972f3 … bfd951b1 | Drehbuch Finale im Wiki mit drei Stimmen-Durchgängen von Character Design und Ducs Entscheiden |
| a4f760db | Wellen-Beats je Runde, Welle 6 mit Verrat und Minicus Szene mit Wahl (`art: wahl`), Appell, Whites Angebot, Funk nach der Nacht (+10 % Leben, `kampf.lp_max_duc`), Aufträge Funk/Türen/Nachtwache/Kirche, Alvas Bar, Aufbau-Pause, Bericht neu |
| 629ebd33 | Säen vorher: Kriegstafel Tag 15 (`bl_tafel`), Minicu Tag 3/6/10/14, Pascals Handschrift, Alvas Tafel, Petrus Ruder, Megans abgebrochener Satz |
| 42b2885d, a8281c48 | Karte mit Stimme (`tk.*`-Kennungen), Gefühl je Zeile, White und Buenaventura mit Figurensatz statt eckigem Avatar |
| fbba8586, 4dcb5cec | Sounds je Zeile, acht Pixabay-Töne nach Ducs Wahl (`werkzeuge/sfx_belagerung.py`) |
| 54e96c9e | Wiki Abschnitt 11: Cliffhanger (gebaut von Character Design, d5cdc250) |
| d419fc47 | Spieltest End-to-End: der Bot spielt die Belagerung echt, `tests/spieltest_kalender.py`; 27/27 Läufe bis Ende Akt 2 |
| (dieser Commit) | Übergabe, LEHREN, Stand-Zeile im Drehbuch |

Vertont: alle 5817 Sätze über `Vertonen_EdenRise.bat`, Stand 02.11. nachmittags.

## Tauchgang (Tag 16–18)

- **Nicht gebaut.** Es gibt keine Events, keine Kämpfe, keine Szenen. Plan und Kanon: `docs/wiki/welt/ortskapitel_tauchgang.md` (Stakes, Erfolg/Fehlschlag, Riposte, Galionsfigur, Buenaventura, Schuldenkette). Der Ablauf des Tauchgangs selbst und der Überfall in Wellen danach sind offen.
- Duc macht den Tauchgang selbst (02.11.), die Story-Sitzung hat ihn nicht angefasst.
- Im Haupt-Checkout liegen **nicht von mir** uncommittete Zeilen in `module/eden_rise/stimme_tags.json` (Petru und Laetitia, Totò, Lea „Sophia worked it out … the sonar“). Sie sehen nach Tauchgang-Arbeit einer anderen Sitzung aus. Vor dem Bau klären, wem sie gehören.
- Anschlüsse, die schon im Spiel sind: `sirene_weg`, `treasure_notes`, `wrack_koordinaten`/`wrack_gedaechtnis`, Alons Drohne in `a2_koordinaten` (Tag 14 Nacht), Buenaventura als Gegner in Welle 4. Nach einem Fehlschlag sagt White ihm, Duc habe das Wrack gesprengt; diese Zeile ist noch nicht gebaut.

## Crew-Aufträge in Woche 2 (Tag 15–20)

- **Gebaut:** `bl_tafel` (Tag 15 Frühstück): Megans Seite mit sechs Aufträgen hängt in der Messe. Jeder Auftrag hängt an einer Mechanik, die es schon gibt: Wood and Stone = Abbauen, Arm the Crew = Rosis Waffen Tag 19, The Law = Elsas Angebot Tag 20, The Red Trio = Versöhnung, The Village = Ruf über Favours, The Bell = Don Vertrauen 3. Die Wirkpunkte im Finale sind gebaut (Welle 2 Elsa, Welle 3 Bibi, Welle 4 Rudern, Welle 6 Mochi und Don).
- **Nicht gebaut:** die Wand mit Häkchen in Holms Kartenraum, sinkende Prozente je Auftrag auf der Tafel, „Aufgaben der Crew zählen als Zeit zusammen“ (`welt/akt2_kalender.md`, Offen), eigene Szenen je Auftrag im Stil von Mass Effect 2.

## Was noch Entwurf ist (Belagerung)

Alles ist gebaut und vertont, aber Duc hat das Finale noch nicht selbst gespielt. Bis dahin gelten als Entwurf:
- Briefings und Beats aller sechs Wellen, Appell, Funkzeilen, Whites Angebot (`taktik_eden_rise.py`).
- Phasen zwischen den Wellen: Casanovas Rede, Verband, Funk, Türen, Aufbau, Alvas Bar, Bà Tư, Nachtwache, Kirche, Bericht (`ereignisse_belagerung.py`).
- Abende und Nächte der sieben Frauen und Maxwells (`ereignisse_belagerung_nacht.py`).
- Prozente und Balancing (Gegner 7/8/8/11/10/10, Heilung 60 %, Neuversuch −15 %).

## Wartet auf Ducs Urteil

- **Yacht-Untergang:** Vorschlag „auf Grund gesetzt“, die Crew schläft bei den Familien (Drehbuch Abschnitt 9, Punkt 0).
- **Zerstörbare Barrikaden:** 2 Energie, leuchtend, vier Stellen, dafür mehr Gegner. Nicht gebaut, wartet auf Ducs Ja. Abnahme Barrikade: `docs/abnahme/barrikade/spec.html`.
- **Minicus Überleben:** Vorschlag, er erfährt es erst in Akt 3.
- **Bilder (Paket E):** Namensblatt, Umschlag, Kreidetafel, Schadensliste, Kevin-Sprite. Nicht bestellt.
- **Alon:** Stimme und Gesicht gewählt (siehe Memory `project_eden_alon_keynote`), Bühne und Sprite offen.
- **Spieltest-Rezensionen:** Mia (Game Two) und Lenny (Steam/Reddit) liegen nach dem Lauf in `C:\Users\DucNg\Documents\Eden-Live\2026-11-02\ausgabe\Eden-Rise-Live-Prioritaet-*`. Duc ließ den Stapel nach Lenny beenden, die übrigen sechs Profile und die vollen Reviews laufen nicht mehr. Befund 02.11. 20:20: Beide loben Figuren und Chemie (Rosi, Alva, Sophia, Lola, Lea) und kritisieren die Kämpfe als Grind ohne taktische Tiefe. Mia findet die Würfe zu undurchsichtig. **Keine der beiden erwähnt die Belagerung, Minicu oder das Finale.** Nächster Schritt: prüfen, ob der Review-Auftrag die Belagerungs-Transkripte überhaupt als Quelle bekommt (`spieltest_live_batch.py`, `reviews()`), bevor man daraus Schlüsse zieht.

## Prozesse, Ports, Worktrees

- Aufgabenplaner **„Eden Live Batch“**: wird nach Lennys Rezensionen beendet (Wächter `stopp_nach_lenny.ps1` im Scratchpad der Sitzung). Neu starten mit `C:\Users\DucNg\Documents\Eden-Live\Live-Batch-0211.bat`, er setzt per Checkpoint fort.
- Aufgabenplaner **„Eden Blume 5010“**: Giftige Blume auf Port 5010 läuft weiter (Limit 48 h), Eden nutzt diese URL.
- Krea (8189) auf Ducs Wunsch am 02.11. beendet.
- Vorschau-Ports der Belagerung (8442, 8443, 8447–8450) sind gestoppt.
- Worktree `X:\AI\Eden_ton` ist weg; keine Branches von dieser Sitzung.

## Fallen

- **Mehrere Pflicht-Events in einer Phase** laufen in Listen-Reihenfolge; Ketten nur über `direkt` mit `wenn`.
- **Drehbuch Welle 6** (`_drehbuch` in `kern/taktik.py`): Runden sind fest (r2 Pascal, r3 Alva, r4 Mochi, r5 Minicu). Zusätze wie Kevin **nach** der Kette anhängen, nie als `elif`, sonst rutscht Minicu in Runde 6.
- **`test_sprite_stimmung`** verbietet joy/amusement in Events mit Ton `ernst`.
- **`NUR_ORT`** braucht die Ausnahme `bl_` in `ereignisse_basis.py`, sonst bricht der Bau bei Wolff.
- **Bild-Namen:** `mayors_office` ist kein erlaubtes Bild, ich nehme `village_piazza`. Im Haupt-Checkout steht in `ereignisse.json` gerade `mayors_office` (fremder, uncommitteter Bau, wohl Casanovas Büro).
- **Sounds:** Jeder `ton` auf einer Kartenzeile braucht eine gewählte Datei (`test_sfx`). ffmpeg concat und loudnorm in einem Schritt schreiben nichts, darum in zwei Schritten.
- **Vertonen** braucht freien Grafikspeicher: Chatterbox (8004) startet nicht, solange Krea oder Blume den Speicher halten.
- **Spieltest:** Bots brauchen `PYTHONHASHSEED=0`. Taktik-Phasen haben das fünffache Schritt-Limit. Live-Läufe nur über den Aufgabenplaner.
- **Commits:** eigener `GIT_INDEX_FILE` + `commit-tree`; bei „HEAD bewegt“ neu ansetzen. Erzeugte Dateien im eigenen Worktree bauen.
