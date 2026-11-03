# Übergabe: Interaction Mechanic (Stand 02.11.2026, Erzählerin eingebaut)

Bereich: Handy, Romanzen, Figurenrahmen, Selfies, Töpfe, Orte/Zimmer, Mikro-Interaktionen. Keine Spoiler (Favours, Fall-Auflösungen) in dieser Datei.

## Gebaut (master)

| Commit | Was |
|---|---|
| e1200749 | **Töpfe je Quelle**: Vertrauen/Begehren je Figur aus Szenen, Handy, Geschenken, Events getrennt begrenzt (`zustand.punkte_add(..., quelle=)`, `MODUL["toepfe"]`, `topf_platz`); Figuren kommentieren volle Töpfe (`figurenrahmen.topf_kommentar`); E-117; `tests/test_toepfe.py` |
| 345a0174 | **Go somewhere private** (Geste `privat_gehen`, `raum_wechseln`, `absage_text`); Dates, `frei_`, `intim`, `gespraech` unter dem 7-Tage-Abstand (`szene.story_frei`); E-118; `tests/test_privat.py` |
| 0573ff0f | **Orte für Zweisamkeit** `kern/orte.py`: Risiko 0–3 je Raum, eigener Ort je Frau, ihr Vorschlag, Erwischt-Folgen (Klatsch/peinlich/komisch) und Lohn; `MODUL["orte"]`; E-119; `tests/test_orte.py`; Demo `docs/orte_demo.html` |
| 32e7af09 | **Zimmer und Orte**: Crew-Kabinen 1–3, Spare Cabin, Alvas Hinterzimmer, Bibis Häuschen, Tenderboot, Mochi's Bucht, Kühlraum, Genueser Turm (Hintergründe Tag/Nacht in ST `backgrounds`); Belegung in `docs/wiki/welt/wohnen.md` |
| af6c22b3 | Megans VIP-Kabine (Flag `megan_zurueck`, Risiko 1), Crew-Dusche und Crew-Toilette (Risiko 0, abschließbar); Bibis Mochi-Daten wiederhergestellt |
| 78e86a0f, ac4a9caa | Wiki `docs/wiki/systeme/hintergruende.md`: wie Raumbilder gebaut werden (keine Tür, Vordergrund frei, frontal, Yacht-Stil, 4 Seeds) |
| 18695711, 3d05d295 | Styleguide 2b „Bewegung“ + Plugin `client/plugins/eden-bewegung` (Stufe steigt, Wert fliegt zur Beziehungskarte, Wahl leuchtet, Gefühl blendet über); Trust = Smiley, Desire = Herz; Showcase `docs/abnahme/bewegung/index.html` |
| 2c7073da, 65507279 | Karten-Sounds (Vorhang, Brücke, Tag), Hintergrund-Abschnitt im Prompt, Bibis Karte an der Station, Schlafgranaten-Klang im Bauplan |
| c0951e71, 45bb73b7 | `docs/brain_trust/OFFEN.md`: Dusche/Toilette, Expeditions-Romanzen Akt 3, Megans VIP-Kabine |
| (siehe unten) | Bibis Tier-Selfies: Skripte `karten_neu/bibi_tier_selfies_2/4/6.py`, Texte von Character Design in `werkzeuge/eden_rise/mochis_daten.py` (`selfie_titel`, `log`) |

## Wartet auf Ducs Urteil

- **Bibis Tier-Selfies, Nachlauf**: 7 Momente × 4 Seeds (Sorry B, Monsieur B, Truffle B, Pudding B, Ghost A, Bones B, Mr. V. B), Ordner `ComfyUI_krea2\ComfyUI\output\expressions\_bibi_tier_selfies_6`. Die übrigen Momente hat Duc am 02.11. freigegeben (Wahl in der Tabelle unten). Erzeugt am 02.11. abends, Abnahme `docs/abnahme/bibi_tier_selfies_6.html` (Bögen in `docs/abnahme/bibi_tier_selfies_6/`). Vorschlag: sorry b_1, monsieur b_2, truffle b_3, pudding b_4, ghost a_2, bones b_4. Bei Mr. V. B ist der Nachlauf misslungen (die Brille sitzt bei allen vier wieder auf Bibis Kopf, der Waran trägt keine); Vorschlag: die alte `_bibi_tier_selfies_5/mr_v_b_1` nehmen.
- **Duc 02.11. abends, Nachlauf freigegeben:** sorry b_2, monsieur b_2, truffle b_1, pudding b_2, ghost a_2, bones b_2, mr_v b_1 (alle aus `_bibi_tier_selfies_6`). Monsieur A neu mit der Frisur von b_2 (`karten_neu/bibi_tier_selfies_7.py`, Ordner `_bibi_tier_selfies_7`, Abnahme `docs/abnahme/bibi_tier_selfies_7.html`), Duc wählt a_3, aber mit Strähnen am Gesicht: gleicher Seed neu mit zwei Frisur-Formulierungen (`karten_neu/bibi_tier_selfies_8.py`, Ordner `_bibi_tier_selfies_8`, Vergleich `docs/abnahme/bibi_tier_selfies_7/monsieur_tendrils.jpg`); Vorschlag `monsieur_b_a_1.png` (Variante b, Szene fast gleich wie a_3), Urteil offen. Damit ersetzt: sorry/monsieur/truffle/pudding/bones/mr_v B und ghost A aus der Liste unten.
- Freigegebene Wahl Runde 4/5 (Ordner `_bibi_tier_selfies_4`, ohne Pony `_bibi_tier_selfies_5`): biscuit a_1/b_2, sorry a_1, monsieur a_2, madame a_1/b_1, monday a_2/b_1, twelve a_1/b_2, ghost b_2, duchess a_1/b_1, rusty a_1/b_1, truffle a_2, bones a_2, mr_v a_1, sunday a_2/b_2, pudding a_2.

## Bibis private Selfies (gebaut 02.11. nachts, 727c75db)

Duc hat die drei Bilder im Prompt Studio erzeugt (Preset `Selfie_Bibi`): `ComfyUI_krea2\ComfyUI\output\expressions\CHARACTER\selfie_bibi_knapp.png`, `selfie_bibi_oben_ohne-2.png`, `selfie_bibi_nackt-7.png`. Eingetragen in `selfie_daten.json` als Reihe `station`, Spielbilder `module/eden_rise/selfies/bibi_station_1..3.webp`, Events `sf_bibi_<3|4|5>_station` (Texte standen schon in `ereignisse_selfies.py`), Andenken `bibi_selfie_3..5` in `modul.json` gezielt ergänzt, Fenster bis Tag 35 (`ereignisse_fenster.py`). `selfie_webp.py` lässt `bibi_fang_*` jetzt liegen (vorher hätte es die Tier-Selfies in den Papierkorb geworfen).
- **Vertonung:** Die neuen Zeilen (Bibis Blasen und Antworten) fehlen noch. Ein voller Lauf `Vertonen_EdenRise.bat` nimmt sie mit, `--wer erzaehler` allein nicht.
- **Fallen:** `modul_eden_rise.py` bricht auf master ab (Alon-Zeile mit `false` statt `False`, fremde Sitzung). `tests/test_selfies.py` scheitert schon auf master vor diesem Commit bei „megan/elsa: Vertrauen 3 reicht, auch an Tag 30“; Ursache nicht untersucht.

## Erzählerin für Ortsbilder (Duc 02.11.2026: „extrem gut“)

Die Erzählerin (Stimme `Erzaehlerin`, `eden-config.json` → `stimmen.eden_rise.erzaehler`) liest den Lagetext der 295 Ortsbilder (`art: "ort"`, rund 50.000 Zeichen). Hörprobe mit fünf Beispielen: `docs/abnahme/erzaehlerin_probe.html`.

**Vorbereitet:** `werkzeuge/eden_rise/vertonen_eden_rise.py` erzeugt für jedes Ortsbild den Satz `<event>#l`, Figur `erzaehler`, Text = `lage` ohne `*` (Lagetexte mit `{…}`-Platzhaltern bleiben aus). Duc lässt den Lauf nachts selbst laufen:

    Vertonen_EdenRise.bat --wer erzaehler

Dauer grob 45–60 Minuten (Probe: 5 Texte, 1.170 Zeichen, gut 1 Minute). Danach `--liste --wer erzaehler` und prüfen, dass nichts fehlt; Stichproben anhören.

**Eingebaut (Branch `t/erzaehlerin`, 02.11.2026):** Alle 295 Aufnahmen lagen schon vor (`audio_index.json`, Schlüssel `#l`).
`eden.event_zeile` liefert für `<event>#l` die Erzählerin mit der Lage ohne `*` (nicht bei `{Platzhalter}`), `evSprich` im Client
setzt `["lage", <id>#l]` vor die Figuren-Zeilen, `.ev-lage.spricht` hebt die Lage im normalen Event-Fenster hervor (die
Expeditions-Karte zeigt sie ohnehin hell). Geprüft im Vorschau-Server (`--tag 2 --event hk_ziege`): 29 s Erzählerin, danach
die Wahl. Test `tests/test_erzaehlerin.py`, Wiki `systeme/interaktion.md` Abschnitt „Erzählerin bei Ortsbildern“.
Frage für später: auch Erzähltext anderer Events? Duc hat bisher nur die Ortsbilder gewollt.

## Offen (nicht angefangen)

- **Selfies eingebaut (02.11. abends)**: `werkzeuge/bibi_fang_webp.py` (Wahl → `module/eden_rise/selfies/bibi_fang_<tier>_<a|b>.webp`), `kern/mochis._selfie` liefert `bilder` [A, B] mit Titel, `text`, `log`; Field Book und Fang-Overlay zeigen zwei Polaroids (`eden-mochis.js/.css`, v=4); Route in `eden.py`; `modul.json` gezielt um `selfie_titel`/`log` ergänzt (Builder hat sie schon); Test `test_selfie_szene`. Vorschau `docs/abnahme/bibi_selfie_polaroids.html`. Im laufenden Spiel noch nicht angesehen.
- **Tippen** (Variante C aus dem LLM-Vergleich von Testing): feste Absage, feste zweite Absage bei Nachfrage, fester Themenwechsel nach Nähe-Gesten. Nicht gebaut.
- **Megan fern**: Video-Anrufe Tag 8–20 im Tablet-Rahmen (Zoom aufs Gesicht bei den letzten Gesten), Fern-Gesten über `megan_funke`, Rückkehr Akt 3 (Charly hackt den Satelliten, sonst findet Rosi ein Agenten-Handy), VIP-Kabine. Nicht gebaut außer dem Raum.
- **Ligeia**: seltene Flaschenpost-Briefe, nur unsichtbarer Wärme-Wert. Nicht gebaut.
- **Vertonung** der neuen festen Zeilen (Absagen, Topf voll, Erwischt, Orte, Rosis „I came here“): über `Vertonen_EdenRise.bat`.
- Polaroids „aufwendiger“ (Duc: später), Expeditions-Rastplatz als intime Szene in Akt 3, Dusche/Toilette-Szenen.
- Zahlen der Töpfe sind Entwurf; mit `tests/spieltest_kurve.py` im eigenen Worktree nachrechnen.

## Erinnerungen der Auftraggeberinnen (Branch `t/erinnerung`, 02.11.2026)

Spieltest-Befund 5 („Kloster und Flut-Nacht leicht zu verpassen“). Messung in `tests/spieltest_ergebnis/roh.json`: Kloster in 27/27 Läufen
angenommen, 11 nicht fertig; Flut-Nacht 3/27. Ursache vor allem der Bot: Die Profil-Bots nutzen die Schnellreise (`kern/wegpunkte.py`)
nie und laufen jedes Mal von vorn (an Tests grün gemeldet, ebenso der Chips-Befund 4 als Bot-Fehler). Für Menschen gebaut: morgens
eine vertonte Sprachnachricht der Auftraggeberin, wenn ein Auftrag 3 Tage still liegt oder die Frist bald endet. Sechs Events
`er_*` in `werkzeuge/eden_rise/ereignisse_erinnerung.py`, Bedingung `ort_ruhe`, höchstens eine am Tag. Wiki `systeme/interaktion.md`
(„Die Auftraggeberin erinnert“), Test `tests/test_erinnerung.py`.
- **Offen:** Vertonung der 12 Zeilen (`Vertonen_EdenRise.bat`). Neuer Fakt für Character Design: Lea sagt, Kevin werde seiner Schätze
  nach ein paar Tagen müde und lasse sie ins Meer fallen (Grund für die Frist Tag 14).

## Branches, Worktrees, Prozesse

- Kein eigener Branch offen. Eigener Worktree `wt_drei_raeume` entfernt (Junctions vorher per `rmdir`).
- Keine laufenden Server dieser Sitzung (Vorschau `eden-bewegung` 8471 gestoppt).
- Krea-Nachlauf: wartet auf freie GPU (Kobold), startet dann die Aufgabe „Eden Krea2 Server“ (Port 8189) und `karten_neu/bibi_tier_selfies_6.py`.

## Fallen

- Commits nur über eigenen `GIT_INDEX_FILE` + `commit-tree` + `update-ref` mit Prüfung, dass master sich nicht bewegt hat; danach `git reset -q -- <dateien>` im Hauptordner. Fremde Änderungen im Hauptordner (z. B. `index.html`, `eden.py`, `hintergrund_bild.py`) nie überschreiben, nur Patches auf HEAD anwenden.
- `modul.json` nie komplett neu bauen, wenn andere Sitzungen Hand-Daten drin haben (Taktik-Commit a8281c48 verlor Bibis Mochi-Daten); gezielt patchen oder den Builder ergänzen.
- Raumbilder: nur `werkzeuge/hintergrund_bild.py` nach `docs/wiki/systeme/hintergruende.md`; jedes Bild selbst ansehen, bevor Duc es sieht (Türkanten, Tisch im Vordergrund).
- Bibi-Selfies: das Preset `Bibi_Selfie` hat im `base_prompt` keine Tag-Platzhalter; `fashion_prompt` nehmen und nur die Tags aus `tags_on` einsetzen. Eine zweite Bibi „im Hintergrund“ beschreiben erzeugt eine doppelte Bibi; „She is the only person in the picture“ anhängen.
- Python-Skripte mit Backslashes oder Zeilenumbrüchen in Strings nur per Write-Tool schreiben.
