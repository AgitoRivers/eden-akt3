# Wiki gegen Code · Widersprüche

Stand 04.11.2026 · Cloud-Sitzung, Branch `wiki-vs-code` · **Nur Bericht, nichts geändert.** Verglichen: alle Seiten unter `docs/wiki/systeme/` und die Story-Seiten unter `docs/wiki/welt/` mit Regeln oder Zahlen, dazu Stichproben in `docs/wiki/figuren/` (Alter, Herkunft, Anrede). Gegen `kern/`, `werkzeuge/eden_rise/` und die gebauten Daten in `module/eden_rise/`. Nicht geöffnet: Favours, Handy-Builder, `handy.json`, `story.json`. Wo ein Punkt nur damit prüfbar wäre, steht „nicht geprüft“.

**Wie „veraltet“ bestimmt ist:** Der Auszug hat nur einen Commit, `git log` hilft nicht. Geurteilt wurde nach dem Stand-Datum der Wiki-Seite und den datierten Kommentaren im Code. Die Prüfung lief in drei Teilen (zwei davon von Prüf-Agenten). Die Funde der Gewichtsklasse „hoch“ habe ich selbst am Code nachgesehen.

**Gewicht:** hoch = Spieler sieht es oder ein Test hängt daran · mittel = Regel oder Zahl ohne direkte Sichtbarkeit · niedrig = Benennung, Zählung, Doku.

## Hoch

| # | Thema | Wiki | Code | Was abweicht | Wahrscheinlich veraltet |
|---|---|---|---|---|---|
| H1 | **Taschenplätze im Menü** | `systeme/items.md:108` „6 Plätze“, `menue.md:47`, `interaktion.md:488` | `modul_eden_rise.py:856-866` (Start 8, dann 12 ab Tag 8, 16 ab Tag 22), `kern/zustand.py:14-18`; aber `client/plugins/eden-menu/eden-menu.js:140` zeigt fest `/6` und `leer(6 - tasche.length)` | Die Engine rechnet mit 8/12/16, das Inventar-Menü zeigt dem Spieler immer „x/6“ | Wiki **und** Menü-Plugin. `beute.md:175` (gebaut 29.10.) stimmt |
| H2 | **Halsbänder und Granate enden an Tag 21** | `systeme/tierstation.md:95` „Die Spuren laufen bis Tag 35“, `:125` Pflicht-Event bei 3 Halsbändern | `ereignisse_mochis.py:10` `TAGE = (11, 35)`, aber `:152` `mo_schlafgranate` und `:165` `mo_halsbaender` nur `WANN((11, 21) …)` | Wer das dritte Halsband in Akt 3 findet, bekommt nie `mo_ark_beweis`, dann fällt `mo_kommission` an Tag 35 aus | Code (Fenster zu kurz) |
| H3 | **Funken: Tage und Phasen** | `systeme/beziehungen.md:189-193` (z. B. Chiara Tag 4 bis 6, Nacht) | `ereignisse_funken.py:32-34`: `FUNKE_WANN(pid, phasen, …)` ignoriert `phasen` und setzt immer `WANN((3, 6), ["abend", "nacht"])` | Funken kommen ab Tag 3 und in beiden Phasen, Chiaras Brücken-Nacht auch am Abend | Code (Parameter wird nicht benutzt, sieht nach Fehler aus) |
| H4 | **Akt 3 beginnt im Code an Tag 22** | `systeme/interaktion.md:58` „Akt 3 = Tag 22–35“, `schiesswette.md:46, 52`, `beute.md:110, 177` | `ereignisse_schneider.py:17` und `ereignisse_outfit_quest.py:20` `AKT3 = [22, 35]`, `kern/schiessen.py:22` `HOLM_TAG = 22`, `kochen_daten.py:213` Stahl `ab_tag 22`, Tasche 16 `ab_tag 22` | Wiki und Code stimmen untereinander, aber Ducs Vorgabe (E-114, CLAUDE.md) ist Akt 3 = Tag 24–35. Tasche, Stahl, Holms Revanche und Schneider-Aufträge öffnen mitten in der Belagerung | beide gegen E-114 |
| H5 | **Auftrag „Türen“ wirkt nicht** | `welt/drehbuch_finale.md:217`, `systeme/taktik.md:233` „mit Petru ab Ruf 4“ | `kern/taktik.py:1599-1602` `_rudert` liest `bl_tueren_petru` nicht (gesetzt `ereignisse_belagerung.py:204`) | Die Wahl ändert nichts. Beleg-Test: `tests/test_balancing_befunde.py` (Branch `balancing-bericht`) | Code unvollständig |
| H6 | **Auftrag „Kirche“: Dons Wahl wirkt nicht** | `welt/drehbuch_finale.md:294` „Don (Vertrauen ab 3): 4 Leben“ | `kern/taktik.py:81-82` gibt das vierte Leben allein über Vertrauen ≥ 3, `bl_kirche_don` (`ereignisse_belagerung.py:314`) liest niemand | Wer Don nicht wählt, bekommt das Leben trotzdem | Code (älterer Stand aus `belagerung.md`) |
| H7 | **Auftrag „Funk“: Vorwarnung in Welle 3 fehlt** | `welt/drehbuch_finale.md:201` „Holm hört die Fackeln eine Runde früher“ | `bl_funk_white` wirkt nur nach Welle 5 (`taktik_eden_rise.py:227`) | Die versprochene Wirkung in Welle 3 fehlt | Code unvollständig |
| H8 | **Alvas Runde** | `welt/drehbuch_finale.md:265` „Mit `bl_alva_runde` zahlt Duc“ | `bl_bar` (`ereignisse_belagerung.py:249-260`) liest das Flag nicht | Alva zahlt immer selbst | Code unvollständig |
| H9 | **Rethink: Zahl der Rücksprünge** | `systeme/taktik.md:194` „drei Rücksprünge je Schlacht“ | `taktik_eden_rise.py:587` `"rueckspruenge": 2`, je Tag zurückgesetzt (`kern/taktik.py:293-294`), Docstring `kern/taktik.py:647` noch „drei“ | Spieler hat 2 je Tag | Wiki Zeile 194 und der Docstring; `taktik.md:11` stimmt |
| H10 | **Sprechzeile ohne Turbo-Tag** | `systeme/stimme_tags.md:3` „jede gesprochene Zeile mindestens einen Tag“ | `stimme_tags.json` Eintrag `batu` „You, later.“ (aus `ereignisse_dorf.py:312`) ohne Tag; `S()` in `ereignisse_dorf.py:29` prüft nicht | Prüfer `stimme_tags_pruefen.py` sollte es melden (hier nicht ausgeführt, lokal prüfen) | Code |

## Mittel

| # | Thema | Wiki | Code | Was abweicht | Veraltet |
|---|---|---|---|---|---|
| M1 | Rosis Werkstatt: Preise | `systeme/aufruestung.md:67` 120 € / 240 € | `kaempfe_eden_rise.py:204` 150 € / 400 € („vorher 120/240“, 28.10.) | Preise | Wiki (`beute.md:95` stimmt) |
| M2 | Geschenkpunkte bei Romanzen | `systeme/beziehungen.md:104` einzigartig +12, mag nicht −4 | `kern/handel.py:617-619` (Romanzen: einzigartig gedeckelt auf +8/+8, mag nicht −8), `:113` NPC +12/−4, `gegenstaende_eden_rise.py:43` `WIRKUNG` passt zu keinem | Wiki trennt Frauen und Nebenfiguren nicht, Builder-Tabelle tot | Wiki und Builder-Tabelle |
| M3 | Anhörung: zwei Ader-Regeln fehlen | `systeme/anhoerung.md:164-166` | `kern/anhoerung.py:116-125` (Crew-Stimmung ±1, Anklage ohne Kette −1) | Regeln fehlen im Wiki | Wiki |
| M4 | Anhörung: Joker erscheint nie | `systeme/anhoerung.md:87` grüner Zettel +1 Ader | `kern/anhoerung.py:1312-1322` braucht Item-Feld `anhoerung_ader`, kein Item hat es | Regel ohne Daten | Daten fehlen |
| M5 | Ereignis-Dichte ab Tag 8 | `systeme/interaktion.md:65-66` „sinkt auf 45 %“ | `kern/ereignisse.py:36, 482` Faktor 0,45 auf die Phasen-Chance, ohne Ende | Faktor statt Wert, gilt auch in Akt 3 | Wiki unpräzise; für Akt 3 Duc fragen |
| M6 | Werkstatt-Auslöser | `systeme/aufruestung.md:134`, `items.md:61-62, 198` („`akt2_werkstatt_bereit`, noch nicht gesetzt“) | `ereignisse_gag1.py:326` fest Tag 8 mittags, Flag existiert nicht | Auslöser | Wiki |
| M7 | Dorf redet: Red Trio | `systeme/dorf_redet.md:50` „noch nicht gebaut“ | `ereignisse_red_trio.py:418` setzt `red_trio_fertig`, `ereignisse_legenden.py:40` `ruf=1` | Legenden laufen | Wiki und Kommentar |
| M8 | Map: Orte | `systeme/menue.md:32` nur fünf Orte | `modul.json` `laeden` hat elf; Pharmacy, Farm und Petru stehen unter „On board“, weil `nur_an_land` fehlt (`kochen_daten.py`, `PETRU_LADEN`) | Seite veraltet **und** Datenfehler bei der Einordnung | Wiki; Daten |
| M9 | Charms | `systeme/items.md:101-103` „Konzept, Federico gibt keinen“ | `charms_eden_rise.py:53` Frederico's Black Lion, gebaut 28.10. | Stand | Wiki |
| M10 | Schießwette, alter Abschnitt | `systeme/schiesswette.md:64-94` (45 s, Holm 40 Punkte, `RUNDE_S`, `HOLM_ENDSTAND`) | `kern/schiessen.py:14-34` drei Runden, 13 Ziele, Konstanten gibt es nicht | Seite widerspricht sich selbst (oben stimmt) | Wiki ab Zeile 64 |
| M11 | Ankauf je Laden | `systeme/beute.md:167-170` beschreibt es als gebaut | `kern/handel.py:473-484` nur Totò, ohne Vertrauen | Plan als Stand | Wiki |
| M12 | Kobra und Skorpion: Wellen | `systeme/taktik.md:261` „Kobra 2 und 5, Skorpion 4“ | `taktik_eden_rise.py:217-229` Kobra 2, 4, 5, 6; Skorpion 3, 4, 5, 6 | Wellen | Wiki Zeile 261 (Zeile 100 stimmt) |
| M13 | Heavy Boarding Robot | `systeme/taktik.md:263` „ab Welle 2“ | nur Welle 5 | Welle | Wiki |
| M14 | Wann White angreifbar wird | `systeme/taktik.md:107` „bis Petrus Trupp in Runde 6 fällt“ | `kern/taktik.py:1641-1657` Minicu fällt in Runde 5 | Runde und Figur | Wiki Zeile 107 (Zeile 220 stimmt) |
| M15 | Kiste behalten | `welt/belagerung.md:154` „Wirkung offen“, Flag `collar_crate` | `taktik_eden_rise.py:547` −5 % mit `gr_kiste_genommen` | Wirkung gebaut, anderer Flag-Name | Wiki |
| M16 | Vorbereitung und Prozent | `systeme/taktik.md:33, 277` „noch nicht im Kalender“ | `taktik_eden_rise.py:540-552`, `kern/taktik.py:58-66`, Wellen als `bl_*` im Kalender | Stand | Wiki |
| M17 | Gebaut-Tabelle der Belagerung | `welt/belagerung.md:129-130` (`bl_belagerung` Dinner, `bl_bericht` Tag 21 Nacht, „Kalender endet“) | `bl_belagerung` Tag 21 Nachmittag, `bl_bericht` Tag 23 Abend, danach `bl_cliff_*` | Phasen und Tage | Wiki (Kalender oben auf der Seite stimmt) |
| M18 | Belagerung als drei Wellen | `welt/belagerung.md:74`, `systeme/taktik.md:46, 106-107` | sechs Wellen auf Tag 21 bis 23, Feuer in Welle 3 und 4 | Grundaufbau | Wiki (Kopfnotizen erklären es nur halb) |
| M19 | Empfang kommt zurück | `welt/belagerung.md:113` „nicht gebaut“, Charly oder Rosi | `ereignisse_cliffhanger.py:27-32` gebaut, immer Rosi | Stand; Charly-Fassung fehlt im Code | Wiki; Code unvollständig |
| M20 | Alon im Cliffhanger | `welt/drehbuch_finale.md` Abschnitt 11 „keine Stimme, kein Sprite, Videotext“ | `bl_cliff_alon` mit Bild `alon_keynote`, Set und Stimme | Stand | Wiki |
| M21 | Minicu und Kevin: Tag | `welt/drehbuch_finale.md:91, 138, 434` „Tag 2“ | `ereignisse_belagerung.py:33` `PFL(3, "tag")` | Tag | Wiki |
| M22 | Red-Trio-Frist | `welt/akt2_kalender.md:76` „16: Frist endet“ | `ereignisse_red_trio.py:19` `TAGE = (11, 14)` | Tag; die Seite führt es selbst unter „Zu ändern beim Bau“ | Code nicht nachgezogen |
| M23 | Parade-Fenster | `systeme/kampf.md:538, 545-546` | `kern/kampf.py:54, 91` ergibt perfekt 131/87/58 ms, gut 290/211/145 ms | Zahlen | Wiki (Zeile 559 stimmt) |
| M24 | Gegner-Tabelle, Duc-LP | `systeme/kampf.md:679` „36 + 5/Level“, `:933-934` Tabelle mit 55/19 | `kern/kampf.py:30` LP 46, `:52` 40/1,10/14/0,6 | Zahlen | Wiki (Zeile 929 stimmt) |
| M25 | „Gegner geschwächt“ | `systeme/kampf.md:53` „ein Angriff“ | `kern/kampf.py:59` `WEAKEN_ATTACKS = 2` | Dauer | Wiki Zeile 53 (Zeile 37 stimmt) |

## Niedrig

| # | Thema | Wiki | Code | Veraltet |
|---|---|---|---|---|
| N1 | Chiara wertet mit Sternen | Stimmen-Durchgang `welt/drehbuch_finale.md` Abschnitt 10 (Zehnerskala) | `taktik_eden_rise.py:153` „Five stars“, `:163` „Three stars“, `:253` „One star“ | Code (Text) |
| N2 | Plätze und Bürgerwehr | `systeme/taktik.md:44` 13 Plätze, Wehr Pascal/Petru/Alva | 14 Plätze (mit North), Wehr Pascal/Minicu/Alva | Wiki |
| N3 | Ligeia | `systeme/taktik.md:207` „Code hat noch …“ | `kern/taktik.py:864-869` schon umgebaut | Wiki |
| N4 | Rudern und `rt_white_agenten` | `welt/belagerung.md:139, 142` (Welle 3, Welle 2), `drehbuch_finale.md:259` „Umbau nötig“ | `kern/taktik.py:1217` (Welle 4), `:608` (Welle 6) | Wiki |
| N5 | Elsa als Trupp | `systeme/taktik.md:115` nur Vertrauen 2 | auch über `elsa_hilft` (`kern/taktik.py:753-755`) | Wiki |
| N6 | Verdiente Trupps | `welt/belagerung.md:53` mit Danzel | Reserve mit Bibi, Danzel ist Support | Wiki |
| N7 | Beats Welle 5 und 6 | `welt/drehbuch_finale.md:305, 320, 287` | Rosis Satz im Briefing mit anderem Wortlaut (`taktik_eden_rise.py:274`), Kevin mit Erzählzeile (`:388`), `bl_kirche` mittags | Wiki |
| N8 | Tage und Erkundung | `systeme/tage_erkundung.md:8, 16-22, 31` (21 Tage, 5 Phasen, Tasche 6) | `modul.json` `zeitraster` 23 Tage, 6 Phasen, Tasche 8 | Wiki (Konzept vom 20.10.) |
| N9 | Kalenderlänge | `welt/ortskapitel_grotte.md:9` `tage = 14` | `tage = 23` | Wiki |
| N10 | Fähigkeiten-UI | `systeme/faehigkeiten_ui.md:7, 21, 34` vier Pfade, 16 Skills | `kaempfe.json` fünf Pfade, 20 Skills | Wiki; ob der Client 20 zeigt, nicht geprüft |
| N11 | Zahl der festen Zeilen | `systeme/stimme_tags.md:37` 1577 | `stimme_tags.json` 5179 | Wiki |
| N12 | Maxwells Tasche | `systeme/kampf.md:965` „3 Espressos“ (Double) | `helden.maxwell.tasche` `espresso_single` | Wiki |
| N13 | Kopf von kampf.md | `systeme/kampf.md:3` Stand 19.10., „noch kein Kampf“ | – | Wiki |
| N14 | Aussagen des Red Trio | `welt/nebenquest_red_trio.md:132, 307, 385` Wert `ark_aussagen` 0–3 | nur Flags `ark_aussagen_3`, `ark_aussagen_1` | Wiki |
| N15 | Selfies, Abende, Funken bis Tag 35 | `systeme/beziehungen.md:150, 163` | alle `sf_*`, `ab_*`, `fk_*` mit `akt2: [8, 35]`; 90 statt 85/87 Selfies | Wiki |
| N16 | Lob: Bibi | `systeme/beziehungen.md:60` 13 Figuren | `modul.json` Bibi schätzt Empathie und Mut, `lob.json` ohne Bibi-Zeilen | Daten (Zeilen fehlen) |
| N17 | Gemelli „nicht gebaut“ | `systeme/items.md:22` | `kern/schiessen.py:114` | Wiki |
| N18 | Jacken-Freischaltung | `systeme/aufruestung.md:86` (Vorschlag) | `kaempfe_eden_rise.py:185-189` | Wiki (`items.md:51-53` stimmt) |
| N19 | Chip-Katalog | `aufruestung.md:209, 214`, `items.md:75` 72 Chips, 24 Familien | `erweiterungen.json` 75, 25 Familien | Wiki |
| N20 | Dorf redet: Zahlen | `systeme/dorf_redet.md:40` 66 Kommentare, 20 Figuren | `legenden.json` 85, 25 Sprecher; Kommentar `kern/legenden.py:23` „Kalender endet an Tag 14“ | Wiki und Kommentar |
| N21 | Strandgut | `systeme/kochen.md:127` | `kochen_daten.py:270-276` mehr Funde; Kommentar `:207` „Stahl gegen Menschen“ falsch (Daten sagen Maschine) | Wiki; Code-Kommentar |
| N22 | Klingelabstand | `systeme/handy.md:40` 3,6 s gegen `:78` 5,2 s | `client/index.html:1738` 5,2 s | Wiki Zeile 40 |
| N23 | Expeditionen 2.0 | `systeme/expeditionen_2.md:35` gegen `:67` (Serie alle 3 oder 2 Kämpfe), `:29` gegen `beute.md:34-35` | nichts gebaut | Wiki widerspricht sich selbst |
| N24 | Register | `brain_trust/ENTSCHEIDUNGEN.md` E-093 „Sandru Giorgi“ | `modul.json` „Sandru Amrani“, Wiki „Iskander Amrani“ | Register |

## Geprüft, ohne Widerspruch

`sturm.md` (Eignung, Schwellen, Schadenskosten, Flags) · `wuerfel.md` (17 Events, 3 Missionen) · `audio_*.md` (Lautheit, Hall nur Sirene, Ton-IDs) · `wohnen.md` (Zimmer und Risiko) · `schneider.md` (acht Aufträge, Muster, Stoffpreise) · `hintergruende.md` (Werkzeuge, Format) · `ortskapitel_berge.md` (Flags, Level) · `akt3.md` (Wiederaufbau in `kern/aufbau.py` wie beschrieben) · `spieltest.md` · Figurenseiten: Alter und Herkunft stimmen mit `modul.json` `personen` überein (alle Seiten mit Alterszeile verglichen), keine Zeile in den Buildern lässt Holm oder Rosi Duc beim Namen nennen. Einzelheiten der Teilprüfungen stehen in den Abschnitten oben, nur Abweichungen sind aufgeführt.

## Was Duc entscheiden muss

1. **H4:** Akt 3 beginnt im Code an Tag 22 (Schneider, Tasche, Stahl, Holms Revanche). Auf Tag 24 ziehen? Empfehlung: ja, als ein Paket mit dem Akt-3-Kalender.
2. **M5:** Soll die gedrosselte Ereignis-Dichte aus Akt 2 auch in Akt 3 gelten (Durchatmen spricht für mehr Zufall)?
3. **H5 bis H8:** Die vier Belagerungs-Aufträge erst nachbauen, bevor Akt 3 sie liest (siehe `docs/wiki/welt/akt3_folgen_belagerung.md` auf Branch `folgen-belagerung`).
