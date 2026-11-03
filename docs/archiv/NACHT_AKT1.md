# Nacht-Session Akt 1 (24.10.2026) – Protokoll

Zweig `nacht-akt1` im Arbeitsordner `X:\AI\Eden-nacht` (Haupt-Repo `X:\AI\Eden` bleibt unberührt, Zusammenführen morgens
mit Duc). Freigegeben von Duc: Scheiben 1–5, Events prüfen/aussortieren, Vertonung selbst starten, ab 5 Uhr Bilder
(Items, Hintergründe für Akt-1-Missionen, Nonna/Adrien/Laetitia über Prompt Studio). Regel: bei Unsicherheit berät der
Brain Trust zweimal; nur bei gleichem Ergebnis wird gebaut, sonst die vorsichtigere Lösung + Markierung hier.

## Brain-Trust-Entscheidungen (je zwei Runden)

| # | Frage | Runde 1 | Runde 2 | Ergebnis |
|---|---|---|---|---|
| 1 | Alva jetzt romanzierbar machen? | Nein: ohne Karte kein Bogen für Szenen/Handy (szene.karte), Plan-Prüfung verlangt will/verbirgt/grenze | Nein: romanzierbar zieht sie in Crew-Szenen, Partnerwahl und Eifersucht; an Land unpassend | **Nur Begehren-Wert** (Events wirken), romanzierbar sobald Karte existiert → offen für Duc |
| 2 | Totòs „Draht“ in „Vertrauen“ umbenennen? | Interner Schlüssel `draht` ist über rollen.ALIAS schon `vertrauen.toto` – Umbenennen bricht Spielstände | Nur die Anzeige zählt für den Spieler | **Nur Label** „Vertrauen Totò“ (Werte + Client) |
| 3 | Maxwell/Jana ohne sortierte Sprites eintragen? | Ja, Engine kommt ohne Sprites aus (sets() leer → kein Bild) | Ja, Sortieren ist Ducs Handarbeit im Prompt Studio | **Eingetragen**, Sprites offen für Duc |
| 4 | Prompt-Studio-Prompts aufräumen (Lola blond?, Rosi mit Lea-Resten, Jana blaue Augen, Casanova mit Schauspielerin)? | Ja, beschlossen (5A) | Nein: Die Sprites sind schon gerendert; geänderte Prompts/Referenzen ändern die Identität künftiger Bilder, ohne dass Duc es sieht | **Nicht angefasst** → Liste für Duc (Sichtprüfung nötig) |
| 5 | Cold Open zeigt 06:35, die Fälle fallen 06:11–06:35 aus – Zeiten angleichen? | Aly: Nein, sechs Zeitleisten + PMS-Versatz umzuschreiben bricht Prüfungen. Der **Knall** ist ein eigener Moment um 06:35 (Alons Gerät treibt LM3 nach dem Ausfall ins Durchgehen), der Ausfall davor bleibt je Fall | Sora: Wiederspieler erkennen den Fall nicht am Abstand Stille→Knall, weil keine Szene Minuten nennt; die Ausfallzeit steht ohnehin im Logbuch. Luise: passt zu Megans „Überlast allein explodiert nicht“ | **Knall 06:35 in allen Fällen**, Fall-Zeitleisten unverändert; Galley-Szene beginnt 05:50 (vorher 06:15 – lag nach dem Ausfall in Fall 1/4) |
| 6 | Was bleibt von der alten zweiten Wahrheit (Herstellermeldung, Megans Mitzeichnung, Routen, Wendung, Bericht)? | Luise: Megans Schuld ist nicht mehr Teil der Story (sie arbeitet unwissentlich für den Deal). Akt 1 bekommt nur unscheinbare Alon-Hinweise ohne Kettenfunktion | Sora: Kein Hinweis darf die Anhörung auf Totò lenken (2A: seine Akt-1-Aussagen bleiben wahr) – also nur Beobachtungen, keine zum Auslöser; kein Codex-Eintrag nennt Alon. Aly: Routen raus, Megans Haltung bleibt (Anhörung braucht sie) | **Umgeschrieben**: Kern = Alons Gerät (verdeckt), 6 Akt-1-Hinweise (rotes Licht, Goldkette, Totò zuckt, Ultimatum, „PX-480 brennt nicht einfach so“, „A.V.“), keine Routen; Haltung aus Vertrauen, offener Inspektion, falschen Vorwürfen, Pressedrohung |
| 7 | Wochenbogen Akt 1 – was raus, was wohin? | Maelle: wie am 22.10. beschlossen; raus: Festa, Bericht, Endfassung, Auslaufen, Zukunft, Schlussbild, Wendung, der Satz, Megans Entwurf, Brand | Sienna: Megan bleibt bis zur Anhörung an Bord (sie ist Richterin), Sturm wandert auf Tag 5 (Druck in Person + Wetter), Warnzeichen/Brand aus, weil der Umrichter schon im Cold Open zerstört ist | **Gebaut** wie unten; Anhörung als Bühnen-Szene, Logik in Scheibe 3 |
| 8 | Ende nach Tag 7: altes Ende (Schiff/Bericht/Zukunft) oder „Ende Akt 1“? | Aly: Altes Ende rechnet mit Bericht und Calvi – passt nicht mehr | Maelle: Schlusskarte „Ende von Akt 1“ mit Anhörung, Crew, Ausblick; Frauen-Abschlüsse erst am Spielende | **„Ende von Akt 1“**, gleiche Form für den Client, Frauen-Liste leer |
| 9 | Anhörung ohne neue Oberfläche – wie spielbar? | Aly: drei Story-Szenen mit je einem Wahlmoment (Anklage, eigene Rolle, Plädoyer); Zeugen und Einsprüche wertet der Code aus Ducs Belegen aus (Einspruch genau dann, wenn der Beweis bekannt ist) | Sora: Spieler muss Geduld, Zeugen und Urteil sehen → Zeilen im Szenen-Log (⚖), das Sprachmodell bekommt das Ergebnis als festen Hinweis. Eigener Einspruch-Knopf = späterer Bildschirm | **Gebaut** (kern/anhoerung.py, Hook in szene.waehlen) |
| 10 | Wie hart sind die Urteile in Akt 1? | Sienna: Eine romanzierbare Figur jetzt zu entlassen, nimmt Akt 2 Inhalte; die Kündigung der Crew als Roguelike-Folge ist noch nicht entworfen | Maelle: Nur Flags setzen (`bewaehrung_<id>`, `praemie_gestrichen`, `kuendigung_angedroht`), echte Folgen entscheidet Duc | **Nur Flags + Werte** (Vertrauen/Moral), Folgen in Akt 2 offen für Duc |
| 11 | Motiv und Loyalität – woher? | Luise: Motiv bekannt = Geständnis oder Vertrauen ≥ 3 (sie hat es ihm erzählt); Loyalität nur, wo sie in den Karten steht: Lea ↔ Sophia (Schwestern) | Sora: Weitere Loyalitäten (z. B. Yasin ↔ Siri) wären erfunden → nicht bauen; Schwester lügt nur für die Schuldige und nur bei Vertrauen < 3 | **Gebaut** wie R1; weitere Loyalitäten offen für Duc |
| 12 | Anklage hat 7 Optionen, der Plan erlaubt 4 | Aly: Optionen = die drei Anwesenden der Besetzung (enthält immer die Verantwortliche, gemischt wie beim Widerspruch) + „niemand allein“ | Sora: „niemand allein“ und „kein Name“ führen in Fällen mit Verantwortlicher zum selben Urteil (offen) → zusammenlegen ist fair; in Fall 6 ist es mit Kette die richtige Antwort | **Gebaut**, 4 Optionen |
| 13 | Festa-Events: alle nach Akt 3? | Sienna: Nein – Casanovas Über-Planung ist ihr Running Gag; Probe, Einladung, Rede, VIP-Lounge, Crew-Auftritt und Ehrenbürger sind Planung „für das Fest am Ende des Sommers“ und bleiben in Akt 1 | Sora: Was *auf* oder direkt vor der Festa spielt (Kleid, Outfits, Platz neben Duc, Flamenco auf der Piazza danach), bricht Akt 1 – das nach Akt 3 (Piazza öffnet erst dort) | **4 Events nach Akt 3**, Rest bleibt |
| 14 | Muss ein Event ganz raus? | Luise: Keins widerspricht der neuen Story; Totòs Cousin Gennaro mit Ziege passt sogar (späterer Geld-Bote, Elsas Fernglas) | Maelle: Nichts streichen, was Duc nicht kennt, ohne dass es stört; Köln-Jobangebot bleibt als Nebenfaden der ersten Woche | **Keins entfernt** |
| 15 | Zufalls-Events an Tag 7? | Sienna: 4C verlangt einen Stimmungsfilter nach dem schweren Moment | Aly: einfachste sichere Form – Akt-1-Fenster enden an Tag 6, der Builder verbietet Tag 7 | **Gebaut** (45 Fenster von Tag 7 auf 6) |
| 16 | Megans tägliche Nachricht – wie garantiert, wie vertont? | Aly: als Anruf-Event mit `pflicht` (kommt immer zu Beginn der Phase, vor dem Zufall); Events werden schon vertont und abgespielt | Sora: Ab Tag 5 ist sie an Bord – die Sperre „Megan ruft nicht an“ gilt für Pflicht-Events nicht, der Witz („ein Deck über dir“) trägt es; Tag 7 eiskalt statt laut | **Gebaut**, Tag 2–7 (Tag 1 = Party, exklusiv) |
| 17 | Stimmen für Maxwell, Jana, Yamamoto? | Luise: Stimmwahl ist Ducs Geschmack (Katalog-Tags) | Sora: Ohne Stimme bleiben Maxwells Zeilen stumm, sonst läuft alles | **Nicht gewählt** → offen für Duc |

## Scheibe 1 · Umbau-Liste

- Lola: romanzierbar, Karte „Lola Brennan“, schätzt Charm/Empathy, Lieblingsorte Kombüse/Achterdeck, Gesten Kompliment/
  Geheimnis/Zeit, Intim-Vorlieben aus der Karte, Beschreibung mit Sterneküchen-Narbe, Anrede „Boss“.
- Maxwell, Jana, Yamamoto als Personen (Tagesablauf, Beschreibung, Vertrauen 1/0/1, bekannt ab Start); Yamamoto mit
  Set-Regeln (Hawaii Standard, nachts Leder, Badeplattform Badeanzug, abends/Piazza Party).
- Begehren für Lola und Alva; Totòs Herkunft (afrikanischer Abstammung, Neapel) in der Beschreibung.
- Tests: lauf_test läuft bis zum Ende (Referenz neu, Abweichungen = Folge von Lola als Romanze), test_missionen OK,
  test_kampf OK.
- Scheibe 1B: Beschreibungen nach der Figuren-Runde (Holm 52/Ålesund/„Frankfurt“, Elsa mit Familie Ferrandi und
  Gap Moe, Alva mit Ghjuvan/Sevilla/Jukebox, Petru mit Marie/„Hm.“, Casanova mit Elternhaus und Schuld) – nur
  öffentliches Wissen. Lieblingsgerichte: neu **Bao Buns** (Lola) und **Fish Pie** (Petru), Chili Noodles nur noch Alva,
  Bouillabaisse nur noch Casanova. Elsa „seit fünf Jahren“, Casanovas „Enkel“ → Neffe und Nichte.


## Scheibe 2 · Wochenbogen auf Akt 1

| Tag | Titel | Hauptszenen (neu **fett**) |
|---|---|---|
| 1 | Noch eine Minute Licht | **Cold Open 06:35** → Party (Rückblende, erster Tatort, Maxwell dabei) → Die Stille → **06:35 Knall** (Maxwell rettet Totò + Lea, Rosi schlägt Notaus, Holm bricht zusammen) → Wen rufst du an? |
| 2 | Gestrandet | Lage → **Megans Ultimatum** (Anime-Wut, 7 Tage, Anhörung) → Holm-Moment → Abschied (Petru schaut nach) → freier Platz · Ermittlung · Widerspruch |
| 3 | Die Bucht | **Sonnenaufgang** · Landgang (Dorf öffnet sich) · zweites Vorhaben · **Lolas erstes Essen in der Bucht** · Nähe · Nachtende |
| 4 | Spuren | freie Phasen/Missionen · **Rosi vs. Officer** (Whiteboard) · **Megan: „Morgen komme ich“** |
| 5 | Druck in Person | Megan kommt · Inspektion (**Wahl alles zeigen / zurückhalten**) · Sturmvorbereitung · **Ein leises Telefonat („A.V.“)** · Sturmnacht |
| 6 | Letzte Spuren | freie Phasen · **Lagerfeuer** (Pflicht-Atempause) · Abend, den du wählst |
| 7 | Die Anhörung | **Anhörung** (Bühne, Logik Scheibe 3) · **Nach dem Urteil** (Megan fliegt) · **Cliffhanger: rotes Licht in den Bergen** |

- Raus aus Akt 1: Festa, der Satz, Megans Entwurf, Wendung, „Was schreibst du über mich?“, Bericht, technischer Weg,
  Brand, Endfassung, Auslaufen, Zukunft, Schlussbild. Warnzeichen am Umrichter abgeschaltet (Story mit `akt`).
- Sturm jetzt Tag 5 (`story.sturm_tag`, showrunner liest es; andere Module unverändert Tag 3).
- Zweite Wahrheit = Alons Gerät (Akt 3, verdeckt); in Akt 1 sechs Hinweise ohne Kettenfunktion, keine Routen.
- `anhoerung` als Daten in story.json (Ablauf, 3 Adern, Zeugen, Plädoyer, Erbarmen-Bedingungen), Logik folgt.
- Ende: Schlusskarte „Ende von Akt 1“ (Anhörung / Crew / Was bleibt), gleiche Form, Frauen-Abschlüsse erst am Spielende.
- story_pruefen: neue Soll-Flags (Cold Open, Explosion, Ultimatum, Anhörung, akt1_ende), alte Szenen verboten,
  Megan-Fenster bis T7 abend, keine Alon-Nennung und keine Verdächtige in den Hinweisen. 0 Fehler, 0 Warnungen.
- Tests: lauf_test läuft bis Ende (Titel „Ende von Akt 1“, Urteil abgeleitet „offen“), Referenz neu; Missionen,
  Kampf (47), Versprechen, Vorlieben, Ortswahl OK.
- Offen für Duc: Party-Text sagt weiter „morgen um sieben nach Calvi in die Winterwerft“ – passt das noch zu
  „Megan hat die Yacht in die Bucht geschickt“? Lagerfeuer läuft vorerst auf der Badeplattform (kein Strand-Raum;
  Hintergrund ab 5 Uhr).

## Scheibe 3 · Anhörung (Logik, ohne neue Oberfläche)

- `kern/anhoerung.py`: Anklage → Zeugen (vorher erspielt: wer Duc Bekanntes über die Nacht gesagt hat, Vertrauteste
  zuerst; dazu eine loyale Person) → Einspruch (automatisch, nur mit Beweis) → Ducs Rolle → Plädoyer → Urteil.
- Megans Geduld 3 Adern, nur Raten kostet: Anklage ohne Kette, offene öffentliche falsche Vorwürfe, Haltung < 0.
- Erbarmen nur mit richtiger Person + voller Kette + Motiv + Ehrlichkeit + Geduld > 0; „Schuld teilen“ setzt zusätzlich
  `schuld_geteilt`. Urteile: erbarmen · aufgeklärt (Bewährung) · unbelegt · falsch · offen · entlastet.
- Die Anklage zählt als öffentlicher Vorwurf → Entschuldigung danach über die vorhandene „Vor allen zurücknehmen“-Aktion
  (z. B. in „Nach dem Urteil“).
- Tag 7: `anhoerung` (Anklage, Optionen beim Szenenbau), `anhoerung_rolle`, `anhoerung_urteil`; Schlusskarte liest das Urteil.
- Tests: `tests/test_anhoerung.py` (alle sechs Fälle: Erbarmen, ohne Ehrlichkeit/Motiv, Strafe, ohne Kette, falsche
  Person, kein Name, Fall ohne Verantwortliche, Adern, Loyalität, Anklage-Optionen) OK; Gate-Lauf spielt die Anhörung
  bis zur Schlusskarte (Referenz neu); alle übrigen Tests OK, story_pruefen 0/0.

## Scheibe 4 · Events gegen den Story-Bogen (142 geprüft)

- **Entfernt: keins.** Kein Event widerspricht Akt 1 so, dass es raus muss (Details Brain Trust 13/14).
- **Nach Akt 3 (Tag 19–21):** Ein Kleid für Chiara, Wer zieht die Crew an?, Der Platz neben Duc, Flamenco mit der
  Bürgermeisterin – sie spielen auf/nach der Festa bzw. auf der Piazza.
- **Ab Tag 3 (Dorf öffnet sich):** 10 Events mit Alva, Elsa, Petru oder Casanova, die schon an Tag 2 möglich waren.
- **Megan aus Büro/Lobby nur Tag 3–4** (7 Anrufe): ab Tag 5 ist sie an Bord; ihre Bord-Events bleiben Tag 5–6.
- **Tag 7 frei von Zufalls-Events** (45 Fenster 7 → 6); der Builder prüft jetzt 21 Tage, Fenster nie über eine
  Aktgrenze, nie Tag 7.
- Akt 2 (Tag 8–14) hat noch keine Events – die Verteilung dorthin braucht die Akt-2-Planung.
- Tests: story_pruefen 0/0, Gate-Lauf bis Ende (Referenz neu), alle übrigen Tests OK.

## Scheibe 5 · Neue Texte

- **Megans Sprachnachrichten** (`werkzeuge/eden_rise/ereignisse_akt1.py`, Pflicht-Events): Tag 2 Mitternacht im Büro
  („no engine“ → Rosi korrigiert) · Tag 3 Tabelle mit einer Spalte „who“ · Tag 4 Vorstand, „Frühstücksfotos sind
  inakzeptabel“ · Tag 5 aus dem Hubschrauber · Tag 6 aus der VIP-Kabine „ein Deck über dir“ · Tag 7 eiskalt „Today I
  listen“. Countdown 5–4–3–2–morgen–heute, je 2–3 Reaktionen.
- **Lola:** Sprosse 1 „Der Vorkoster“ (Lob-Mechanik: lautes Lob vor der Crew am stärksten, Sternekoch-Kritik lässt sie
  einfrieren, NO-TWEEZERS-Sticker) · Stufe 2 „Service!“ mit Megan an Bord („Alle raus. Lola, atmen.“ setzt `lola_bogen`).
- **Chiara:** Stolz Stufe 1 „Ein Zettel voller Sterne“ (Lolas Tratsch, setzt `chiara_lernt_bekannt`) · Stufe 2
  „Brückennock bei Nacht“ ab Vertrauen 3 („Zeigst du mir…“ setzt `chiara_bogen`, Polaris, zweimal durchgefallen).
- Engine: `WANN(pflicht=True)`, `kern/ereignisse.ziehen` zieht Pflicht-Events zuerst; Builder erlaubt Pflicht-Events
  an Tag 7, verlangt genau einen Tag + eine Phase. Maxwell/Jana/Yamamoto dürfen in Events vorkommen.
- Holms letzter Anruf: „am Abend vor der Anhörung“ statt „vor dem letzten Tag“.
- Tests: Gate-Lauf spielt alle sechs Nachrichten (Referenz neu), alle übrigen OK, story_pruefen 0/0.

## Vertonung und Bild-Vorbereitung

- **Vertonung** (Aufgabenplaner, nicht als Sitzungs-Kind): 798 Sätze geprüft, **34 neu erzeugt, 0 Fehler**. Maxwell
  hat keine Stimme → seine Zeilen bleiben stumm (neuer Schalter `--fehlende-auslassen`). Neue Audios ergänzend ins
  Haupt-Repo kopiert (812 Dateien, 36 neue Index-Einträge, nichts überschrieben).
- **Lolas Tratsch** „Totò zählt nachts Geld“ (ab Tag 4, Vertrauen 2) zeigt auf Totòs Wettbuch – in allen sechs Fällen
  gleich, nur Wegweiser.
- **Orts-Hintergründe Macchia/Kloster/Berge**: 68 Varianten vom 21.10. lagen unausgewählt vor. Trypophobie-Vorprüfung
  (alle angesehen): keine Lochmuster, nur einzelne Felshöhlen und Flechtenflecken. Abnahmeseite
  `docs/abnahme/orte_akt1.html` – je Ort eine Variante mit OK markieren.
- Vorbereitet für ab 5 Uhr: Item-Motive Bao Buns / Fish Pie (`werkzeuge/item_bilder.py`), Hintergründe
  `strand_lagerfeuer` + `berge_rotes_licht` (`werkzeuge/hintergrund_bild.py`), Casting Nonna Fiora / Laetitia /
  Adrien (`karten_neu/castings_akt1.py`, je 2 Gesichtsfassungen × 2 Seeds).

## Bilder ab 5 Uhr

- Krea2 (8189) und Prompt Studio (8301, ohne Browser) über den Aufgabenplaner gestartet – laufen noch in eigenen Fenstern.
- **Items:** Bao Buns, Fish Pie, dazu der bisher fehlende Verbandskasten.
- **Hintergründe:** `strand_lagerfeuer` und `berge_rotes_licht`, je 4 Varianten (noch nicht in die Bühne eingetragen –
  erst nach Ducs Wahl, sonst zeigt die Engine ein fehlendes Bild).
- **Casting:** Nonna Fiora, Laetitia, Adrien je 2 Fassungen × 2 Seeds (Presets `Yacht_<Name>_A/_B` im Prompt Studio).
- Trypophobie-Prüfung: alle angesehen, keine Lochmuster (Nonnas Kleid: feiner Mehlstaub).
- Abnahmeseite `docs/abnahme/bilder_akt1.html` (23 Bilder), Orte weiter in `docs/abnahme/orte_akt1.html`.

## Ducs Abnahme (24.10. morgens)

- Items Bao Buns, Fish Pie, Verbandskasten: OK.
- Hintergründe: Lagerfeuer Variante 3, Bergen-Licht Variante 2 → übernommen und in die Szenen `lagerfeuer` /
  `cliffhanger` eingetragen.
- Casting: Laetitia Fassung B (Seed 2), Adrien Fassung A (Seed 2) gewählt. Nonna A/B abgelehnt („etwas jünger und
  schöner, eine schön gealterte Frau, weniger Nonna-Klischee“) → Runde 2 mit Fassung C/D (um 60, Leinenbluse,
  ohne Kopftuch, Kochlöffel bleibt).
- Orte (Macchia, Kloster, Berge): 17 Hintergründe übernommen als `eden_rise_<ort>.png` im ST-Hintergrundordner.
  Doppelt freigegeben: `macchia_path` (1 Haupt, 4 als `_b`) und `lion_den_cave` (2 Haupt mit Schädel, 4 als `_b`).
  Die Ortskapitel selbst (Frames, Missionen) sind noch nicht gebaut – die Bilder liegen bereit.
- Casting abgeschlossen: Nonna Fassung C Seed 1, Laetitia B Seed 2, Adrien A Seed 2. Feste Presets `Yacht_Nonna`,
  `Yacht_Laetitia`, `Yacht_Adrien` (Muster Petru, Outfit-Karten `*_standard`); Casting-Presets entfernt, 13 abgelehnte
  Portraits im Papierkorb. Sprites erzeugt Duc selbst.
- Kloster-Figuren (`karten_neu/kloster_figuren.py`): neue Studio-Tags `Color: Chestnut`, `Skin: Olive Tan`;
  `Yacht_Laetitia` jetzt tag-basiert (Subject nur Name/Alter/Gesicht/Augen; Tags Athletic, Chestnut, Side Braid,
  Freckles, Olive Tan). Isabelle als Casting (tag-basiert, Runde 1 wirkte kindlich → Runde 2 ausdrücklich erwachsen),
  Frederico fest als `Yacht_Frederico` (Fassung A) + 4 Varianten. Abnahme `docs/abnahme/bilder_kloster.json`.
- Prompt Studio (24.10.): NPC-Knopf 🙂 im ST-Deck (23 Ausdrücke inkl. brave `_2`-Karten für excitement,
  embarrassment, admiration, love, desire; `fear_2` statt `fear`). Frederico: 22 Sprites ohne desire in
  `expressions\Yacht_Frederico\Standard\roh` (von Duc abgenommen), Lächeln aus dem Preset entfernt.
- ST-Übernahme (24.10.): Nonna Fiora (27), Laetitia Albertini (23), Adrien Morel (23), Isabelle (23), Frederico (22,
  ohne desire; aus roh einsortiert, `_2`-Karten auf den ST-Slot) in `characters\<Name>`, Set-Namen `*_standard`.
  In Eden noch nicht als Personen eingetragen (kommt mit den Ortskapiteln).
