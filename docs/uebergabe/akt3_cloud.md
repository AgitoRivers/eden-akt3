# Übergabe Akt 3 · Cloud-Sitzung (Branch `akt3-cloud`)

Stand 04.11.2026, Block 3: Drehbuch Version 3.4 (Bones, Charly und Danzel, Festa-Schalter, E-126), davor 3.3 (Baustoffe je Haus, Charlys Geld, sieben Ereignisse in Abschnitt 7, E-125), davor 3.2 (Belagerung ohne Prozent, Freundschaften, E-124), davor 3.1 mit Ducs Entscheiden (E-122) und der unabhängigen Prüfung (30 Befunde, Abschnitt 13b). **Keine Events gebaut.**

## Gebaut (Commits)

| Branch | Commit | Inhalt |
|---|---|---|
| `akt3-cloud` | `506dce2` | Drehbuch v1, Fragenliste, Bestellliste, E-120 offen |
| `akt3-cloud` | `e1d9891` | Drehbuch v2 (Gegenrede, Wiki gegen Code, Belagerungs-Flags, Text-Audit eingearbeitet) |
| `akt3-cloud` | (dieser) | Drehbuch v2.1 (unabhängige Prüfung von v2 eingearbeitet), Fragenliste F-17 bis F-27, E-120 nachgezogen |
| `akt3-cloud` | (dieser) | Drehbuch Version 3: Yacht schwer beschädigt mit Reparatur, Unterkünfte, Minicu erst zur Festa, Festa-Lose ohne Zähler, Megan Tag 25, Bibi- und Lea-Idee, Säule Geld mit drei Wegen, fünf Paare (Abschnitt 7), Brain Trust; E-122; Vermerke in `ortskapitel_tauchgang.md` und `enden.md`; Fragen F-28 bis F-30 |
| `fix-akt2-folgen` | `57b9204`, `6351a04` | **Code:** Türen mit Petru (Ruf 4), Alvas Runde (`bl_bar_runde`, Duc zahlt), Dons Kirche (+1 Leben ab Welle 5), Akt 3 ab Tag 24 (Sperre endet nach Tag 23, Schneider, Lesung, Holms Revanche, Expedition Pack), Station-Beweis auch in Akt 3, `tests/test_akt2_folgen.py` (15 grün), E-121 |

## Paket A (Code, 04.11.2026)

- `fix-akt2` in `akt3-cloud` gemergt (ohne Konflikt), `HOLM_TAG` auf 24.
- Akt-3-Schalter `akt3_spielbar` (steht auf `false`), Gags bis Tag 31 (mit Maxwell bis 29), Gags an Bord ruhen während der Reparatur, Dichte Woche 4 bei 0,6, Flag `bl_dorf_rudert`. Einzelheiten: Drehbuch 12a.
- `ereignisse.json` und `modul.json` gezielt geändert (nur `wann.akt2` von 84 Events und `akt3_spielbar`), weil der Neubau hier ohne Bilder die Hintergründe tauscht. **Lokal neu bauen** (`ereignisse_basis.py`, `modul_eden_rise.py`) und prüfen, dass `git diff` danach leer ist.
- Tests: `test_akt3_kalender` neu und grün, `test_akt2_events` angepasst. Alle Tests 47 gegen 48 grün, keine Verschlechterung. `test_holm_wette` lokal prüfen (braucht `eden-config.json`).
- Handy-Events (`hy_`) bleiben bei Tag 21: Ob sie bis Tag 31 dürfen, prüft die Handy-Sitzung.

## Paket B (Code und Szenen, 04.11.2026)

- **B1 Baustellen:** `kern/aufbau.py` neu (erster Stein, Baustoffe je Haus, Lieferung ohne Phase, Piraten nachts, Charly, Bauen-Los), eingehängt in `eden.py`, Reiter „Village“ in Nonnas Fenster. Tests `test_aufbau_akt3`, `test_taktik.test_aufbau` angepasst.
- **B2 Woche 4:** `werkzeuge/eden_rise/ereignisse_akt3_woche4.py`, 34 Events, 4 neue Karten in `auftraege.json`, 157 Zeilen mit Turbo-Tags in `stimme_tags.json` (quelle `akt3_woche4`). Test `test_akt3_woche4`.
- **Buenaventura** (`bonaventure`) spricht jetzt in Events: in `ereignisse_basis.NEBEN` und `SETS` (`bonaventure_standard`) eingetragen. Lokal prüfen, ob das Sprite im Figurenordner „Captain Bonaventure“ liegt.
- `ereignisse_basis.pruefe` erlaubt für `a3_` dasselbe wie für `bl_` (Holm und Megan sind zurück, Kloster-Figuren, `gag1` ohne Betroffene).
- `ereignisse.json`, `stimme_tags.json` gezielt ergänzt (nur die 34 neuen Events, nur die neuen Zeilen). **Lokal neu bauen** (`ereignisse_basis.py`, dann `auftraege_eden_rise.py`), `git diff` sollte leer sein.
- Alle Tests: 50 grün, keine Verschlechterung. Vertonung der neuen Zeilen steht aus.
- Offen aus Paket B: siehe Drehbuch 12a, „Noch nicht gebaut aus Paket B“.

## Paket C bis F (04.11.2026)

- **C** Zeugen-Karte und Festa-Tafel (`ereignisse_akt3_lose.py`). **D** Woche 5 mit Villa und Endkampf (`ereignisse_akt3_woche5.py`, `kaempfe_akt3.py`). **E** Schluss-Szenen der Romanzen, Freundschaften und Paare (`ereignisse_akt3_romanzen.py`). **F** Kommission, Festa mit Minicu, Mitternacht, Säulen und Enden (`ereignisse_akt3_finale.py`, `kern/akt3.py`, `kern/abschluss.py`).
- Zusammen: 140 Akt-3-Events, 18 neue Karten, 4 Kämpfe, 529 gesprochene Zeilen mit Turbo-Tags. Alle Tests: 53 grün, keine Verschlechterung. Neue Tests: `test_akt3_kalender`, `test_aufbau_akt3`, `test_akt3_woche4`, `test_akt3_lose`, `test_akt3_woche5`, `test_akt3_romanzen`, `test_akt3_finale`.
- **Akt 3 ist noch ausgeschaltet** (`AKT3_SPIELBAR = False`). Einschalten nach dem lokalen Durchlauf, siehe Drehbuch 12a.
- **Lokal neu bauen und prüfen:** `ereignisse_basis.py`, `auftraege_eden_rise.py`, `kaempfe_eden_rise.py`, `modul_eden_rise.py`. `ereignisse.json`, `auftraege.json`, `kaempfe.json`, `stimme_tags.json` sind hier gezielt ergänzt. Nach dem Neubau sollte `git diff` leer sein.
- **Paket G (lokal):** Bot-Lauf mit `PYTHONHASHSEED=0` über Tag 24 bis 35, Endkampf-Balancing (Alon Level 10), Vertonung der neuen Zeilen.

## Ducs Antworten vom 04.11. abends (E-130), Stand

- Gebaut: Enden mit Entwürfen und Erklärung, ★ über `kern/meta.py` (`spielstaende/_meta.json`), Riscossore immer, Feldbett in der Kirche, Einladungen nach Mitternacht, höchstens drei Karten, Endkampf mit Verbündeten (`beistand`), Alvas Satz, Sandrus „Your Own Name“, mehr Petru, Stella und Holms Los.
- **Für die Story-Sitzung:** Totòs Akt-3-Geheimnis schreiben (F-19), Platz in Woche 5.
- **Für Character Design (optional):** Holms Mutter als Bild (F-14), bis dahin nur ihre Zeile. Der Chef der Eden Group bleibt nur Stimme (F-07), kein Bild.
- **Kommission als Verhandlung (F-08):** Regeln, Daten, 49 Zeilen und Test gebaut (`kern/kommission.py`, `kommission_akt3.py`). **Lokal:** Plugin `eden-commission` bauen und `kommission.AN = True` setzen, Bauanleitung im Drehbuch 12a. Sprecher `anwalt` und `kommissar` brauchen Stimmen. Die Anhörung selbst ist an die Fall-Daten und die vh.-Texte gebunden, die diese Sitzung nicht öffnen darf; die Kommission bekommt eigenes Modul und eigene Daten.

## Wartet auf Ducs Urteil

- E-128 (Säulen und Enden im Code), F-34 (Wohnen als Raum-Logik), F-35 (Enden ohne Wahrheit), F-36 (★).

- (erledigt) Zahlen der Baustoffe je Haus bestätigt.
- Für die lokale Sitzung: `belagerung.md` und `drehbuch_finale.md` an E-122 angleichen (Yacht repariert, Minicu erst auf der Festa).
- F-31: Yacht und Minicu, in E-122 entschieden, in `belagerung.md` noch offen.
- Nach master geht `fix-akt2` (E-124), `fix-akt2-folgen` bleibt liegen.
- Fragenliste `docs/uebergabe/akt3_fragen.md` (F-01 bis F-30).
- Merge von `fix-akt2-folgen` (vorher lokal: `tests/test_taktik.py` und `test_sfx.py`, die hier an fehlenden Sprites und `eden-config.json` scheitern; `test_sfx` ist schon auf master rot).

## Bekannte Fallen

- `ereignisse_basis.py` baut hier ohne Bilder und tauscht dabei bei 64 Events den Hintergrund. In `fix-akt2-folgen` sind darum nur die 23 betroffenen Events übernommen. Lokal neu bauen und `git diff module/eden_rise/ereignisse.json` prüfen.
- Neue und geänderte Zeilen aus `fix-akt2-folgen` sind nicht vertont (Alva in `bl_bar` und `bl_bar_runde`).
- Auf `fix-akt2` steht `HOLM_TAG = 22`, Akt 3 braucht 24.
- Neue Flags fürs Bauen: `bl_dorf_rudert`, `bl_nachtwache_pascal`, `gr_riscossore_gesehen`.
- Favours und Handy nicht öffnen (F-11, F-12).
