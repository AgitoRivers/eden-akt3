# Eden Rise: Stand und Aufgaben

Lebendes Dokument. Der Main Chat hält es aktuell, jede Aufgaben-Sitzung meldet ihm am Ende ihre Zeile. Stand: 02.11.2026 abends, Haupt-Checkout aufgeräumt, erste Sitzungen gestartet.

Details je Bereich stehen in den Übergaben unter `docs/uebergabe/`. Kanon steht im Wiki (`docs/wiki/START.md`). Fallen stehen in `docs/brain_trust/LEHREN.md` und in den Übergaben.

## So arbeiten wir ab jetzt

1. **Main Chat baut nichts.** Er verteilt Aufgaben, merged, hält diese Datei aktuell und meldet Duc. Fragen an Duc immer mit Vorschlag und Abnahme-Link.
2. **Eine Aufgabe = eine Sitzung = ein Branch = ein Worktree.** Sitzungen leben kurz (eine Aufgabe, dann Übergabe und Schluss). Höchstens drei laufen gleichzeitig.
3. **Der Haupt-Checkout `X:\AI\Eden` bleibt sauber.** Dort spielt Duc. Niemand ändert dort Dateien, niemand stagt im gemeinsamen Index.
4. **Worktree anlegen:** `git worktree add <scratchpad>\wt_<thema> -b t/<thema> master`, dann `cp -rn X:/AI/Eden/module/eden_rise/figuren/. <wt>/module/eden_rise/figuren/` und `eden-config.json` kopieren (beide gitignored; Verschachtelungsfalle beachten, `figuren/Bibi` muss existieren).
5. **Landen am selben Tag:** Die Sitzung committet auf ihren Branch, lässt Gate (`tests/lauf_test.py --modul eden_rise --seed 7` und `--seed 3`) und die Tests ihres Bereichs laufen und meldet dem Main Chat „bereit“. Der Main Chat merged auf master, baut die Gate-Referenz auf dem neuen HEAD und zieht den Haupt-Checkout nach.
6. **Grafikkarte:** Nur eine Sitzung nutzt die GPU zur gleichen Zeit (Krea 8189, Chatterbox 8004, Blume 5010 schließen sich aus). Vertonung läuft nachts über `Vertonen_EdenRise.bat`.
7. **Wissen gehört ins Repo:** Mechaniken ins Wiki, Fallen in `LEHREN.md`, Stand in diese Datei. Ins Memory kommen nur Arbeitsregeln und Zeiger.
8. **Zwei feste Gesprächs-Sitzungen neben den Aufgaben-Sitzungen** (Duc 02.11.): **Character Designer** (Ducs eigene Sitzung: bestehende und neue Figuren optimieren, nutzt die GPU) und **Interaction** (Engine, UX/UI, Mechaniken im Gespräch mit Duc). Beide bauen pro Thema auf eigenem Branch `t/<thema>` im eigenen Worktree und melden „bereit“ an den Main Chat wie jede Aufgaben-Sitzung.
9. **Fragen an Duc nie mit Knöpfen.** Jede Entscheidung als Tabelle: Option · Was es ist · Wirkung bei Ja · Bei Nein · Aufwand · Empfehlung, darunter „Ich empfehle …, weil …“ (Duc 03.11.).
10. **Grenze bei Bildern:** keine expliziten Sprites und keine neuen Bilder von Lola, Lea und Jana (wirken auf den Bildern sehr jung). Gilt für jede Sitzung.
11. Bestehende Regeln gelten weiter: Spieltext Englisch und einfach, Chat Deutsch, Abnahme-Seiten als `start chrome "<url>"`, nie endgültig löschen, keine Spoiler (Fall-Auflösungen, Favours-Inhalte, `vh.`/`fv_`/`rt_t_`-Texte) in Chat, Übergaben oder Memory.

## Stand je Bereich

| Bereich | Fertig | Offen | Übergabe |
|---|---|---|---|
| Belagerung (Tag 21–23) | Sechs Wellen, Drehbuch, Beats, Phasen, Abende, Karte mit Stimme und Sounds, alles vertont; Bot spielt sie 27/27 bis Ende Akt 2 | Alles Entwurf, bis Duc das Finale gespielt hat; Prozente und Balancing | `story.md` |
| Crew-Aufträge (Woche 2) | Kriegstafel `bl_tafel` Tag 15, sechs Aufträge an bestehenden Mechaniken, Wirkpunkte im Finale | Häkchen-Wand in Holms Kartenraum, sinkende Prozente je Auftrag, Zeit zusammen, Szene je Auftrag (Mass Effect 2) | `story.md` |
| Tauchgang (Tag 16–18) | Plan im Wiki `welt/ortskapitel_tauchgang.md`, Anschluss-Flags im Spiel | Alles: Events, Kämpfe, Szenen, Überfall in Wellen, Whites Zeile nach Fehlschlag | `story.md` |
| Cliffhanger und Alon | Alon spricht auf der Bühne, 22 Posen, Stimme, elf Zeilen vertont | Duc hat nicht gespielt; Kampf-Sprite für Alon | `character_design_bibi_alon.md` |
| Bibi und Mochi's | Station, Kämpfe, Schlafgranate, Arc bis Geständnis, Kosenamen, Tier-Selfies (zwei Polaroids je Tier), private Selfies, neue Stimme | Duc hat Station und Arc nicht gespielt; Vertonung der neuen Selfie-Zeilen; Outfit-Selfies Urteil; Buenaventura-Szene Akt 3 | `character_design_bibi_alon.md`, `interaction_mechanic.md` |
| Beziehungen | Töpfe je Quelle, Go somewhere private, Orte mit Risiko, Zimmer, Bewegungs-Plugin, Erzählerin liest Ortsbilder (03.11.), Erinnerungen der Auftraggeberinnen (03.11.) | Tippen (Variante C), Megan fern (Video-Anrufe), Ligeia-Briefe, Vertonung neuer fester Zeilen (inkl. 12 Erinnerungs-Zeilen) | `interaction_mechanic.md` |
| Kampf | Roboter-Sprites, Sieg nach Spezial-Sequenz, Ruckel-Fix | Duc hat Ruckel-Fix nicht gespielt; Parry-Notknopf (Duc: erst so lassen); Pixelblätter macht Duc; **Spieltest-Kritik: Kämpfe als Grind ohne taktische Tiefe, Würfe undurchsichtig** | `roboter_und_kampffluss.md` |
| Figuren-Bilder | Outfit-Casting Nebenfiguren, Holm-Uniformen | **Wiki für Character Design:** Maxwells Seite nennt noch die alte Trainingsregel (seit Paket C Tagesaufgabe, E-042 ersetzt); **Casanovas Amtszimmer:** Hintergründe `mayors_office` und `piazza_treppe_tidy` bauen (nach `wiki/systeme/hintergruende.md`), danach den Bildwechsel aus dem Patch in `X:\AI\Eden_Sicherung\` einspielen (`auftraege*`, `ereignisse*`); Holm Satz im Look M, Bibi K neu, Danzels Schneider-Satz, Mina-Satz (Duc), Wunsch-Outfits, Holms Wette Ziel-Sprites und Klang, Paket E (Namensblatt, Umschlag, Kreidetafel, Schadensliste, Kevin) | `character_design_outfits.md`, `character_design_bibi_alon.md` |
| Tests | Gate grün, Spieltest-Bot, Kurve, Modellvergleich (Blume bleibt); 03.11.: 16 rote Tests repariert, Live-Rezension mit Belagerung als Quelle, Bot-Fehler 3/4/5 behoben (Tasche, Chips, Schnellreise), Bot trainiert einmal am Tag und nutzt „Chase them off“; Abschlusslauf auf master 8258457e: 94 grün, Gate 7/3 identisch | `test_kampf_server` und `test_ui_kopfzeile` je einmal zufällig rot (beim zweiten Lauf grün); Bot-Probelauf der neuen Regeln (Tandi, Noor) offen; Spieltest Stufe 3 (Browser) | `testing.md` |
| Prompt Studio | – | Übergabe fehlt noch (wartet auf Ducs Ja in der Sitzung) | – |

## Wartet auf Duc

- Spielen: Mochi's und Bibis Arc, Belagerung bis zum Cliffhanger, ein Kampf (Ruckeln).
- Urteile mit Vorschlag: Yacht „auf Grund gesetzt“, zerstörbare Barrikaden (`docs/abnahme/barrikade/spec.html`), Minicu erfährt sein Überleben erst in Akt 3, Vertrauen 5 schon an Tag 4–6 gewollt?, Bibis Outfit-Selfies, Monsieur-Selfie (`docs/abnahme/bibi_tier_selfies_7/monsieur_tendrils.jpg`).
- Aufräumen: Blume 5010 beenden; Worktree `C:\Users\DucNg\Documents\Codex\eden-holms-bet` und Branch `codex/holms-bet` löschen (überholt); Papierkorb (37 GB Testmodelle).
- Prüfliste der Memory-Dateien (Main Chat hat sie gebaut).

## Haupt-Checkout

Sauber seit `dd648fb1` (02.11. abends, Duc „führe alles aus“), Gate Seed 7 und 3 grün. Übernommen: Sophias Koje-Selfies, Maxwell-Schlag, Sprite-Bögen, Abnahmen und Urteile, Erzählerin-Probe, Minimap-Karten, Effekt-Labor ohne Medien (Medien per `.gitignore` lokal). Nicht übernommen, liegt im Patch `X:\AI\Eden_Sicherung\haupt_checkout_offen_2026-11-02.patch`:
- Casanovas Bildwechsel (`mayors_office`, `piazza_treppe_tidy`): die Bilder gibt es nicht, siehe Figuren-Bilder.
- Zehn Tauchgang-Zeilen in `stimme_tags.json` (Petru, Totò, Lea, Riscossore, Gennaro): prüft die Tauchgang-Sitzung.
- Gelöschte „Grenze“-Abschnitte in `UEBERGABE_TAKTIK.md` und `UEBERGABE_OUTFITS_2026-10-31.md`: bleiben drin.

## Laufende Sitzungen

| Sitzung | Branch | Aufgabe | GPU |
|---|---|---|---|
| Character Designer | je Thema `t/<thema>` | Ducs eigene Sitzung, Figuren optimieren | ja |
| Interaction | je Thema `t/<thema>` | Engine, UX/UI, Mechaniken im Gespräch; Erzählerin und Erinnerungen auf master (03.11.), als Nächstes Geld (G1/G2) | nein |
| Handymechanik (vorher Tests grün) | je Thema `t/<thema>` | Handy Paket 3 „Das Handy erinnert sich“ auf master (03.11.): Chat-Faden erinnert Anrufe und Selfies, Untertitel im Videoanruf, Webcam-Duc, Foto groß; Handy-Klang aus einem Guss (leiser Empfang, Marimba-Klingeln, nachts Vibration). Offen: Klingelton je Frau (geparkt), Herz-Klang im Ablauf mit Blume prüfen, Würfel ruhiger (eigene Entscheidung), Kontaktnamen und Klingeltöne geparkt, Selfie-Format 9:16 für neue Bilder (Duc), `systeme/handy.md` ins Wiki-Register und die START-Tabelle | nein |
| Tauchgang | `t/tauchgang` | Planung fertig, nichts gebaut (Drehbuch, Unterwasser-Probe, Übergabe `docs/uebergabe/tauchgang.md` auf dem Branch, Worktree `wt_tauchgang` steht); Sitzung beendet, Nachfolger offen. Quest-Start Tag 14 (Interaction, ausgefallen) noch nicht gebaut | nein |
| Kampf-Tiefe | je Thema `t/<thema>` | Auf master: Paket C, Kampf lesen (Parade-Rückmeldung, Finten, Taunts, Klänge), Schlag-Bildfolgen bei Attack und Konter, Try again (03.11.). `test_kampf_server` wackelt weiter (1 von 3 rot) | nein |
| Posen neu (Main Chat auf Ducs Wunsch, 03.11.) | `knie-schnitt` (Worktree `X:\AI\Eden_knie`) | 17 umgeschriebene SFW-Karten (stehend statt Hocke/Sitz/Sprung) für 887 Sprites aus 31 Figuren neu erzeugen, Aufgabenplaner „Eden Posen Neu“, Abnahme `X:\AI\Eden_Review\posen_neu\index.html`, danach `--uebernehmen` erst nach Ducs Ja. Megan seit 03.11. dabei (Krea_Meg). Lola, Lea und Jana bleiben ausgesetzt (Punkt 10); neue Bilder von ihnen merged der Main Chat nicht | ja |

## Spieltest-Befunde (gebündelt 02.11.)

Quellen: Peer-Group 9 Typen × 3 Läufe (`tests/spieltest_ergebnis/peer_group.md`), Bot-Rezensionen und Live-Rezensionen Mia und Lenny (`C:\Users\DucNg\Documents\Eden-Live\2026-11-02\`), Kurve, Modellvergleich. Alle Läufe kommen ohne Fehler ans Ende von Akt 2.

| # | Befund | Beleg | Wer |
|---|---|---|---|
| 1 | Kämpfe wirken wie Grind ohne taktische Tiefe, Würfe undurchsichtig | 55–88 Kämpfe in 24 Tagen (3 pro Tag); Mia, Lenny | Kampf-Tiefe: Paket C (Training als Tagesaufgabe, „Chase them off“ bei schwachen Gegnern) auf master seit 03.11.; B + A (Try again, Steady Hand +50 %, Warum-Zeile) warten auf Ducs Ja; Paket 2 (Bruch mit Crew-Moment) wartet auf Ducs Testkampf. Bots nutzen „Chase them off“ noch nicht |
| 2 | Geld ohne Ziel ab der Mitte | Konto 3.200–5.100 am Ende, Lenny gibt nur 340–445 aus | Echt: Kurve stimmt bis Tag 14, danach 1.200–1.400 € ohne Zweck. Duc 03.11.: G1 ja (Tauchausrüstung von Megan, 600 €, wird Quest-Start des Tauchgangs an Tag 14; Interaction stimmt mit Tauchgang ab), G2 ja (Kriegskasse für Crew-Aufträge, dazu Holz und Stein für Barrikaden kaufbar), G3 Wiederaufbau geparkt in `brain_trust/OFFEN.md` |
| 3 | Tasche ständig voll | Lenny 15–17 Tage „Tasche voll“ | Bot-Fehler (Typ Kämpfer verkauft nie), an Tests grün |
| 4 | Chips-Knopf meldet über 50-mal „Werkstatt noch zu“ | Alex (IGN) | Bot-Fehler, kein Spielfehler (an Tests grün) |
| 5 | Kloster-Quest und Flut-Nacht leicht zu verpassen | Alex, Deniz | Teils Bot-Fehler: Bots nutzen die Schnellreise („Or travel“) nie (an Tests grün). Auftraggeberinnen erinnern per Sprachnachricht, auf master seit 03.11. (`t/erinnerung`); 12 Zeilen noch nicht vertont; Kevin-Fakt („gets bored of his treasures, drops them in the sea“) von Duc abgesegnet, gehört ins Wiki (Character Design) |
| 6 | Zugängliche Spieler verlieren viele Kämpfe | Noor: 45–59 Siege bei 76–87 Kämpfen, Hilfe nötig | Kampf-Tiefe |
| 7 | Vertrauen 5 schon an Tag 4–6 | Kurve | Urteil Duc |
| 8 | Belagerung fehlt in Live-Rezensionen; Figurentreue nirgends gemessen; Browser-Stufe 3 offen | Peer-Group „offen“, story.md | Tests grün |
| + | Stärken: Figuren und Chemie (Rosi, Alva, Sophia), Belagerung mit Lernkurve, Kämpfe ohne Romance möglich | alle Rezensionen | – |
