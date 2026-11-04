# Beat-Plan-Audit der gescripteten Events

Stand 04.11.2026 · Branch `berichte-audits` · nur gelesen, nichts am Spiel geändert, nichts committet.

## 1. Kopf

### 1.1 Methode

Geprüft wurden Code, gebaute Daten und Wiki je Block:

| Block | Quellen |
|---|---|
| Anhörung | `kern/anhoerung.py`, `client/plugins/eden-hearing/eden-hearing.js`, `werkzeuge/eden_rise/anhoerung_aussagen.py` und `module/eden_rise/anhoerung_aussagen.json` (nur Aufbau und Gefühle ausgewertet, keine Falltexte), `docs/wiki/systeme/anhoerung.md`. Ein Grep nach „anh“ in `werkzeuge/eden_rise/ereignisse_*.py` fand **keine** Anhörungs-Events, nur Kommentare. Die Anhörung läuft ganz im eigenen Bildschirm. |
| Belagerung | `werkzeuge/eden_rise/ereignisse_belagerung.py`, `ereignisse_belagerung_nacht.py`, `kern/belagerung.py` (reine Bestand/Flicken-Mechanik, keine gescripteten Zeilen), Wellen-Szenen in `taktik_eden_rise.py` und `client/plugins/eden-tactics`, `docs/wiki/welt/belagerung.md`, `drehbuch_finale.md` Abschnitte 2 bis 8 |
| Cliffhanger | `werkzeuge/eden_rise/ereignisse_cliffhanger.py` (alle `bl_cliff_*`), `drehbuch_finale.md` Abschnitt 11 |
| Tauchgang | `docs/wiki/welt/ortskapitel_tauchgang.md`, Tauchgang-Zeilen in `drehbuch_finale.md` und `akt2_kalender.md`. Grep nach „tauch\|margot\|dive“ in `werkzeuge/eden_rise` und `ereignisse.json`: kein Tauchgang-Event gebaut (einziger Treffer `g1_lea_nachttauchen`, ein Gag aus Akt 1). Geprüft wird darum der **Plan**. |

Zusätzlich lief ein Skript über `module/eden_rise/ereignisse.json` und `module/eden_rise/uebergaenge.json`: je Event Art der Zwischenkarte (eigener Satz, generisch, `ohne_karte`), Sprecher gegen Beteiligte aus `P1()`, Gefühle, Frage in der letzten Zeile.

Bewertung: **J** = Ja, **t** = teils (Grund als Buchstabe, Legende in 1.4, sonst in der Bemerkung), **N** = Nein, **n/a** = trifft nicht zu. Gleichartige Events sind zu Gruppen zusammengefasst, die IDs stehen in der Zeile.

### 1.2 Regeln

| Regel | Inhalt | Quelle |
|---|---|---|
| R1 | Titelkarte mit Continue | `CLAUDE.md` Punkt 4; `sturm.md` Z. 10f.; `anhoerung.md` Z. 209; `kochen.md` Z. 234 und 243 |
| R2 | Skip möglich | `CLAUDE.md` Punkt 4; `anhoerung.md` Z. 209 („*Skip* springt über alles“); `sturm.md` Z. 11; `taktik.md` Z. 97 („Skip mit Esc“) |
| R3 | Reaktionen der Anwesenden | `CLAUDE.md` Punkt 4; `anhoerung.md` Abschnitt Tratsch |
| R4 | Gefühl auf dem Sprite passt zur Lage (ernst = ernste Pose, kein joy/amusement in `ton: ernst` ohne Freigabe) | `STIL.md` Abschnitt 6 „Sprite passt zur Lage“; `tests/test_sprite_stimmung.py` (Liste `FREI`) |
| R5 | keine stumme Umschaltung, der Übergang wird angesagt oder gezeigt | `CLAUDE.md` Punkt 4 |
| R6 | klare Handlungsaufforderung, klare Frage vor Antwort-Chips | `CLAUDE.md` Punkt 3 und 4; `STIL.md` „Verständlich bleiben“: „Erst die klare Frage, dann die Antworten“ |
| R7 | alle Beteiligten kommen zu Wort (wer im Bild steht oder in `P1` genannt ist, spricht oder reagiert) | `CLAUDE.md` Punkt 4 |
| R8 | Beat-Plan vorhanden: Ansage, Inhalt, Handlung, Reaktion, Übergang erkennbar, Drehbuch im Wiki | `CLAUDE.md` Punkt 4 und „Technische Umsetzung“; `LEHREN.md` 02.11. („erst das ganze Drehbuch schreiben“) |
| R9 | Erinnerung im Satz bei Rückbezügen | `STIL.md` „Verständlich bleiben“; `CLAUDE.md` Punkt 3 |

Weitere Fundstellen zu Titelkarte, Skip und Continue: `kampf.md` Z. 433 (Titelkarte beim neuen Frame, verblasst nach 4 Sekunden), `nebenquest_red_trio.md` Z. 313ff. (Beat-Tabelle mit Titelkarten, das beste Muster im Wiki), `drehbuch_finale.md` Z. 228, 254, 316 (Titelkarten „Fire“, „1924“, „The Last Wave“ auf der Taktik-Karte).

### 1.3 Wie die Engine Titelkarte, Skip und Continue umsetzt

Skip und Continue gibt es **nicht** automatisch für alle Karten, sondern je Bildschirm. Die Anhörung (`eden-hearing.js`, `momentHtml`) zeigt auf jedem Moment einen Knopf „Skip ▸▸“, Titelkarten mit `warte` haben einen eigenen Knopf („Begin“, „Continue“, „Hear the statement“) und gehen auch mit Enter oder Leertaste weiter; die Taktik-Karte zeigt „Continue · Space“ und „Skip · Esc“ (`eden-tactics.js` Z. 322f.). Normale Events (`client/index.html`, `evBrueckeHtml`, `ereignisHtml`) haben nur eine **Zwischenkarte** mit Tag, Phase, einem Satz und dem Knopf „Go on“; der Satz kommt aus `uebergaenge.json` oder wird aus der Tageszeit gebaut (`kern/ereignisse.py`, `uebergang_text`: „It is night now. Something else needs you.“), der Event-Titel steht nicht auf der Karte, sondern klein im Kopf des Event-Bildschirms. Einen Skip-Knopf hat der Event-Bildschirm nicht; die Stimme bricht nur ab, wenn man eine Antwort wählt (`evWahl`), und nach einer Antwort mit Folgezeile kommt „Continue“. Takte einer Kette über `direkt` ohne Antwortzeile springen ohne Ergebnis-Bildschirm weiter (`eden.py` Z. 517f.), bekommen aber trotzdem eine neue Zwischenkarte, außer ihre ID steht in `ohne_karte`.

### 1.4 Legende der Kurzgründe

- (a) Zwischenkarte nur mit dem generischen Satz („The day moves on. Something else needs you.“ bzw. „It is night now. Something else needs you.“).
- (b) kein Skip; die Stimme bricht nur ab, wenn man eine Antwort wählt.
- (c) Takt einer Kette über `direkt`, keine Abkürzung über die ganze Kette.
- (d) generische Zwischenkarte mitten in der laufenden Szene (ID fehlt in `ohne_karte`).
- (e) der Wechsel steht im Lagetext, aber die Zwischenkarte (d) unterbricht ihn.
- (f) eine Figur steht als Kreis im Bild und spricht nicht.
- (g) das Wiki beschreibt Ablauf und Zeilen, aber ohne Beat-Tabelle Ansage → Inhalt → Handlung → Reaktion → Übergang.
- (h) nur eine Person reagiert, die übrigen Anwesenden bleiben stumm.
- (i) vor den Chips steht keine Frage und keine Aufforderung; die Chips sind reine Handlungen.

### 1.5 Tests

| Test | Ergebnis |
|---|---|
| `python tests/test_sprite_stimmung.py` | OK: 791 Zeilen in ernsten Events passen zur Lage, Sturm ohne Schock-Pose, 7 Krisenszenen mit Stimmungsrahmen |
| `python tests/test_cliffhanger.py` | OK (`test_cliffhanger ok`) |
| `python tests/test_anhoerung.py` | OK: Fall 1 bis 5, Loyalität Fall 2 und 3 |

Alle drei laufen ohne `module/eden_rise/figuren` und `eden-config.json`. **Lokal nicht prüfbar:** ob die Sprite-Dateien zu den Gefühlen wirklich existieren (z. B. `alon_standard` für Alons Bühne), weil `module/eden_rise/figuren` in diesem Auszug fehlt.

## 2. Tabellen je Block

### 2.1 Anhörung (eine Zeile je Szene im Bildschirm, `kern/anhoerung.py`)

| Szene | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | Bemerkung |
|---|---|---|---|---|---|---|---|---|---|---|
| A1 Auftritt: Titelkarte „The Hearing“, Antibes-Satz, Werftbericht | J | J | t | J | J | J | n/a | t(g) | t | R3: die Crew ist nur Untertitel („the whole crew is watching“), sie reagiert erst nach Punkt 1. R9: zwei der vier Antibes-Sätze tragen keine Erinnerung (siehe Fund A2) |
| A2 Punkt 1 „What happened that night?“ | t | J | J | J | J | J | J | t(g) | J | R1: die Titelkarte von Punkt 1 hat keinen Knopf (`warte=nr > 1`), sie läuft nach der Lesezeit weiter. R9 vorbildlich: Ducs Gedanke unter der Titelkarte nennt, was fehlt (`tafel_tipp`) |
| A3 Plädoyers und Anklage | J | J | J | t | J | J | J | t(g) | J | R4: das erste Plädoyer bekommt für **jede** Figur `pride` (siehe Fund A1). R6: Megan fordert vor den Namen klar zur Anklage auf |
| A4 Punkt 2 „Testimony of …“ mit Nervosität, Konter, Zeugen, Zusammenbruch | J | J | J | J | J | J | J | t(g) | n/a | Raunen, Reaktion, Tratsch, Zeuge per Videoanruf: das stärkste Reaktionsgerüst im Spiel |
| A5 Nachbessern „Revised testimony“ | J | J | t | J | J | J | J | t(g) | n/a | R3: nur der Zeuge rudert zurück und Megan stichelt, kein Saal |
| A6 Punkt 3 mit Kettenbrett | J | J | J | J | J | J | J | t(g) | J | Kettenbrett zeigt What und Who als Zettel: Erinnerung im Bild, vorbildlich |
| A7 Geständnis | n/a | J | t | J | J | n/a | J | t(g) | n/a | Gefühle passen (embarrassment, remorse, sadness, nervousness, grief). R3: bis „The Verdict“ reagiert niemand aus der Crew |
| A8 Urteil: „The Verdict“ → Rolle → Plädoyer → „Megan decides …“ → Urteil → Reaktion → Tratsch → „The hearing is closed“ | J | J | J | J | J | J | J | t(g) | J | R6 vorbildlich: Megan fragt vor beiden Wahlen klar („What do you ask of me?“), die Karten erklären die Folge |
| A9 Abbruch bei 0 Adern | J | J | J | J | J | n/a | J | t | n/a | R8: im Wiki nur ein Satz (Abschnitt „Megans Geduld“) |

### 2.2 Belagerung (Tag 3 bis 23)

| Nr. | Event-IDs | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | Bemerkung |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `bl_frist` (Handy) | J | t(b) | t | J | J | J | J | t(g) | J | R1: Klingeln mit „Accept“ ersetzt die Karte. R3: niemand am Frühstückstisch reagiert, erst `bl_tafel` |
| 2 | `bl_tafel` | t(a) | t(b) | J | J | J | t(i) | J | t(g) | J | Lage verbindet sauber („After Megan hangs up“) |
| 3 | `bl_minicu_kevin`, `bl_minicu_lola`, `bl_minicu_jana`, `bl_minicu_name` | t(a) | t(b) | J | J | J | t(i) | t(f) | t(g) | n/a | R7: Mina in `bl_minicu_kevin` stumm |
| 4 | `bl_manoever` | J | t(b) | J | J | J | J | t(f) | t(g) | n/a | Maxwell stumm; Pascal spricht, steht aber nicht in `P1`, also ohne Bild |
| 5 | `bl_alva_flinte` | J | t(b) | J | J | J | J | t(f) | t(g) | n/a | Totò stumm |
| 6 | `bl_elsa_hilfe` | J | t(b) | J | J | J | J | t(f) | t(g) | n/a | Elsa spricht Totò an, er antwortet nicht |
| 7 | `bl_kriegsrat` | J | t(b) | J | J | J | t | t(f) | t(g) | J | R6: Chip „Looks at the dead screen.“ setzt ein Bild voraus, das nur als Ton `tk_megan_weg` kommt. Chiara und Maxwell stumm (Maxwell „is very quiet“ ist gewollt). R9 gut: „the timber and stone Megan told you to gather on day fifteen“ |
| 8 | `bl_letzte_nacht` | J | t(b) | J | J | J | t(i) | J | t(g) | n/a | |
| 9 | `bl_rede` | t(a) | t(b) | J | J | J | t(i) | t(f) | t(g) | n/a | Casanovas große Rede startet mit „The day moves on. Something else needs you.“; Holm stumm |
| 10 | `bl_belagerung` (vor Welle 1) | J | t(b) | J | J | J | J | t(f) | t(g) | n/a | Chiara stumm |
| 11 | `bl_welle_2` (Verband) | J | t(b) | J | J | J | J | t(f) | t(g) | J | Lola fragt klar („Who's it for?“); Chiara ist eine der Antworten, sagt aber nichts |
| 12 | `bl_funk` | t(a) | t(b) | J | J | J | J | t(f) | t(g) | n/a | Rosi und Sophia stehen im Bild und sind Antworten, sprechen aber nicht |
| 13 | `bl_funk_rosi`, `bl_funk_rosi_charly`, `bl_funk_sophia`, `bl_funk_nichts` | N(d) | N(c) | t(h) | J | t(e) | J | t(f) | t(g) | n/a | Holm „is waiting“ und reagiert nicht auf das Ergebnis |
| 14 | `bl_morgen_22`, `bl_morgen_23` | J | t(b) | J | J | J | J | t(f) | t(g) | J | Petru am 23. stumm. R9 vorbildlich (Petru: „Megan told you to bring timber and stone back on day fifteen, when she called about the six days.“) |
| 15 | `bl_tueren` | t(a) | t(b) | J | J | J | J | J | t(g) | t | R9: Mina „like in 1924“ kommt vor der Ruder-Geschichte in `bl_flicken_22`; 1924 ist vorher nur in optionalen Events gesät (`lg_petru_1924` u. a.) |
| 16 | `bl_flicken_22`, `bl_flicken_23` | J | t(b) | n/a | J | J | J | J | t(g) | J | |
| 17 | `bl_welle_3`, `bl_welle_4`, `bl_welle_5` | J | t(b) | J | J | J | J | t(f) | t(g) | J | Rosi in Welle 5 stumm, laut Lage gewollt („Rosi has stopped talking“) |
| 18 | `bl_aufbau_heil`, `bl_aufbau_asche` | t(a) | t(b) | J | J | J | t(i) | J | t(g) | J | |
| 19 | `bl_bar` | t(a) | t(b) | J | J | J | t(i) | t(f) | t(g) | N | R9: Alva sagt immer „Somebody promised me a round when this is over.“, auch ohne Flag `bl_alva_runde` (siehe Fund B3). Pascal spricht nur über den zweiten Chip |
| 20 | `bl_batu` | t(a) | t(b) | n/a | J | J | J | J | t(g) | J | |
| 21 | `bl_nachtwache` | t(a) | t(b) | n/a | J | J | J | J | t(g) | n/a | Wolff antwortet, steht aber nicht in `P1` |
| 22 | `bl_wache_elsa`, `bl_wache_yamamoto`, `bl_wache_keiner` | N(d) | N(c) | n/a | J | t(e) | J | J | t(g) | t | R9: Holm „That one isn't here tonight, Frankfurt.“ sagt nicht, wer und warum (Elsa ohne `elsa_hilft`, Yamamoto unter Vertrauen 2) |
| 23 | `bl_wache_wolff_bericht`, `bl_wache_elsa_bericht`, `bl_wache_yamamoto_bericht` | t(a) | t(b) | J | J | J | J | t | t(g) | J | R7: Holm antwortet, steht aber nicht in `P1`, also ohne Bild |
| 24 | `bl_kirche` | t(a) | t(b) | J | J | J | J | t(f) | t(g) | n/a | Don stumm; Casanova fragt klar |
| 25 | `bl_kirche_don`, `bl_kirche_don_schlaeft` | N(d) | N(c) | J | J | t(e) | J | t(f) | t(g) | n/a | |
| 26 | `bl_welle_6` | J | t(b) | J | J | J | J | t(f) | t(g) | n/a | Chiara stumm |
| 27 | `bl_bericht` | J | t(b) | J | J | J | J | J | t(g) | t | R9: „until the rematch“ ohne Erinnerung an Holms Wette mit Gemelli an Tag 18 (siehe Fund B3) |
| 28 | `bl_abend_wahl_21`, `bl_abend_wahl_22`, `bl_abend_s2`, `bl_abend_s3` | J | t(b) | J | J | J | J | t(f) | N | n/a | Folgeseiten korrekt in `ohne_karte`. Holm fragt auf jeder Seite klar („So who do you go to tonight?“) |
| 29 | `bl_leer`, `bl_ab_schon` | J | t(b) | N | N | J | t(i) | N | N | J | Chiara steht immer als Kreis („says nothing“) im Bild, egal wessen Tür es ist; die Zwischenkarte nennt sie mit („with Holm, Chiara“). Siehe Fund B1 |
| 30 | `bl_ab_chiara`, `bl_ab_sophia`, `bl_ab_lea`, `bl_ab_rosi`, `bl_ab_siri`, `bl_ab_lola`, `bl_ab_alva`, `bl_ab_maxwell` | J | t(b) | n/a | J | J | J | J | N | t | R4: `amusement`/`joy` bei Sophia und Alva sind freigegeben. R9: zwei Chips brauchen Vorwissen (Lola: „you walked out on him that same night“; Maxwell: „does lesson one“). R8: im Wiki nur ein Absatz (`belagerung.md` Z. 16) |
| 31 | `bl_nacht_wahl_20`, `_21`, `_22`, `bl_nacht_s2`, `bl_nacht_s3` | J | t(b) | J | J | J | J | t(f) | N | n/a | Folgeseiten korrekt in `ohne_karte` |
| 32 | `bl_na_<pid>` und `bl_na_<pid>_still` für chiara, sophia, lea, rosi, siri, lola, alva (14) | J | t(b) | n/a | J | J | J | J | N | J | jede Szene endet mit einer echten Frage, eigene Zwischenkarte („Of everyone, you choose …“) |
| 33 | `bl_na_<pid>_wieder` und `_wieder_still` (14) | J | t(b) | n/a | J | J | J | J | N | J | Lage erinnert („It's the divers' sign: stay together.“) |
| 34 | `bl_echo_<pid>` (7) | J | t(b) | n/a | J | J | t | J | N | J | R9 vorbildlich, jede Lage nennt die Nacht davor. R6: `bl_echo_chiara` und `bl_echo_lola` ohne Frage. Nebenfund: Kopf-Chip zeigt „Evening“ beim Frühstück (Art `abend`) |
| 35 | Wellen-Szenen auf der Karte (`taktik_eden_rise.py`, `briefing`/`szene`) | J | J | J | n/a | J | J | n/a | t(g) | t | Titelkarte mit „Continue · Space“ und „Skip · Esc“. R9: Holm im Briefing Welle 3 „that's your man from the wreck“ (Z. 258), der Tauchgang ist nicht gebaut. R7 nicht je Runde geprüft |

### 2.3 Cliffhanger (`ereignisse_cliffhanger.py`)

| Event-ID | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | Bemerkung |
|---|---|---|---|---|---|---|---|---|---|---|
| `bl_cliff_netz` | t(a) | N(c) | J | J | J | J | J | t(g) | t | Karte: „It is night now. Something else needs you.“ R9: Elsa „straight to the commission“; ob der Spieler die Kommission vor Tag 23 kennt, ist offen |
| `bl_cliff_alon` | N(d) | N(c) | n/a | J | t(e) | J | J | t(g) | J | `joy`/`pride` für Alon freigegeben (`FREI`: Bühnenlächeln als Lüge) |
| `bl_cliff_alon_siri` | N(d) | N(c) | n/a | J | t(e) | J | J | t(g) | J | Erinnerung im Satz vorbildlich („the gate, the smoke, Minicu“) |
| `bl_cliff_platz` | N(d) | N(c) | t(h) | J | t(e) | J | t(f) | t(g) | J | Siri steht mit `siri_wartet` als Kreis im Bild und sagt nichts (Zeile nur mit `siri_darf_posten`) |
| `bl_cliff_team` | N(d) | N(c) | n/a | J | t(e) | J | J | t(g) | J | |
| `bl_cliff_blicke` | N(d) | N(c) | t(h) | J | t(e) | J | J | t(g) | J | Der Höhepunkt: das Dorf erfährt vom Verkauf, nur Casanova spricht („...Monsieur?“). Siehe Fund C3 |
| `bl_cliff_megan` | N(d) | N(c) | N | J | t | J | J | t(g) | J | R5: „your phone rings“ steht nur im Text, kein Klingeln, kein Handy-Bildschirm (anders als `bl_frist`). R3: niemand auf dem Platz reagiert |

R8 für den ganzen Block: Abschnitt 11 hat eine Tabelle (# · Event · Was passiert · Zeilen), aber keine Spalten für Handlung, Reaktion und Übergang; `bl_cliff_platz` und `bl_cliff_blicke` fehlen als eigene Zeilen, und der Satz „Alon hat weder Stimme noch Sprite, darum steht seine Rede als Videotext in der Lage“ widerspricht dem Code (Alon spricht selbst, Raum `alon_keynote`, Set `alon_standard`). `belagerung.md` Z. 113 lässt Charly die Satelliten hacken, Code und Abschnitt 11 lassen Rosi das Netz knacken.

### 2.4 Tauchgang (nur Plan, `ortskapitel_tauchgang.md`: „Idee von Duc, noch nicht gebaut“)

| Teil des Plans | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | Bemerkung |
|---|---|---|---|---|---|---|---|---|---|---|
| T1 Der Tauchgang selbst (Riposte, Name an der Galionsfigur) | N | N | N | n/a | N | N | N | N | n/a | „Offen.“ Keine Beats, keine Figuren, kein Ablauf |
| T2 Überfall in Wellen nach dem Auftauchen | t | t | N | n/a | N | N | N | N | n/a | nur „Aufbau wie der Hafenkampf, nur epischer“. Wenn er auf der Taktik-Karte läuft, bringt die Engine Titelkarte und Skip mit; geplant ist es nicht |
| T3 Fehlschlag (Frist verpasst, Galionsfigur treibt an den Strand) | N | n/a | N | n/a | N | N | N | N | n/a | Folgen stehen fest, die Szene nicht |
| T4 Galionsfigur zu Ligeia (`sirene_frei`) | N | n/a | N | n/a | N | N | N | N | n/a | `sirene_frei` kommt in keinem Builder vor |
| T5 Rückbezüge in gebauten Szenen | n/a | n/a | n/a | n/a | n/a | n/a | n/a | N | N | Holm Welle 3 „your man from the wreck“ (`taktik_eden_rise.py` Z. 258), Petru Welle 4 „rowed out to the Margot“ (Z. 307), Drehbuch Tag 16 bis 18 „Buenaventura: Duc hat sein Wrack gesprengt“: alles verweist auf eine Szene, die es nicht gibt |

## 3. Die drei wichtigsten Funde je Block

### 3.1 Anhörung

**A1 · Das erste Plädoyer ist immer stolz.** `kern/anhoerung.py`, `_plaedoyers`: `gefuehl="pride" if i == 0 else "sadness"`. Das passt zu Rosi oder Chiara, aber nicht zu Lea, deren erster Satz unsicher ist („I was on deck most of the night. I don't even know how the drive works“). Vorschlag: eine kleine Tabelle `PLAEDOYER_GEFUEHL` je Figur, z. B. Lea `("nervousness", "sadness")`, Sophia `("disapproval", "neutral")`, Yasin `("annoyance", "neutral")`, Rosi und Chiara `("pride", "sadness")`. Für die Plädoyers aus den Falldaten gilt dieselbe Tabelle, damit das Gefühl nichts verrät.

**A2 · Zwei Antibes-Sätze ohne Erinnerung.** `kern/anhoerung.py`, `ANTIBES`: „You were kind in Antibes“ und „You yelled your way in here in Antibes“ tragen den Ort; `tag0_megan_flirt` („And I will be harder on you than on anyone. You know why.“) und `tag0_megan_foermlich` („You were always the professional one. Prove it.“) nicht. Zwischen Tag 0 und Tag 7 liegt eine Woche. Vorschlag in einfachem Englisch: flirt „You flirted with me in Antibes, Duc. So today I will be harder on you than on anyone.“; förmlich „In Antibes you were the professional one. Prove it today.“ (neu vertonen, Tags je nach Vertonungsweg der Anhörung).

**A3 · Kein Beat-Plan im Wiki, Titel weichen ab.** `anhoerung.md` hat einen nummerierten Ablauf, aber keine Beat-Tabelle; R8 ist für alle neun Szenen nur teils. Dazu nennt das Wiki die Titelkarten „What?“, „Who?“, „Why?“, der Code zeigt „What happened that night?“, für Punkt 2 eine Frage nach Täterin und Absicht (mit einem Gedankenstrich im Spieltext, darum hier nicht wörtlich) und „Did exactly that kill the drive?“ (`RUNDE_TITEL`). Vorschlag: in `anhoerung.md` eine Tabelle Ansage → Inhalt → Handlung → Reaktion → Übergang für A1 bis A9, die echten Titel eintragen, und die Titelkarte von Punkt 1 wie die anderen auf Klick warten lassen (`_titel`: `warte=True`), damit alle drei Punkte gleich beginnen.

### 3.2 Belagerung

**B1 · Falsche Figur im leeren Zimmer.** `ereignisse_belagerung_nacht.py`, `bl_leer` und `bl_ab_schon`: beide haben fest `P1("holm", ("chiara", "?", "says nothing"))`, gelten aber für jede Frau (`ZU_ABEND`). Wurde z. B. Lola gefeuert, sieht der Spieler vor Lolas leerer Kabine Chiaras Kreis, und die Zwischenkarte sagt „with Holm, Chiara“. Wurde Chiara selbst gefeuert, steht sie in der Szene über ihr eigenes leeres Zimmer. Vorschlag: den Kreis streichen (`P1("holm")`) oder die beiden Frames je Person bauen (`bl_leer_<pid>`, `bl_ab_schon_<pid>`) mit dem Namen im Satz, z. B. Holm „[sigh] Lola isn't on this boat any more, Officer. You signed the paper yourself. Go and get some sleep.“

**B2 · Die großen Pflichtszenen beginnen mit dem Standardsatz, Folgetakte reißen ab.** Ohne eigenen Satz in `uebergaenge.json`: `bl_tafel`, `bl_minicu_*`, `bl_rede`, `bl_funk`, `bl_tueren`, `bl_aufbau_*`, `bl_bar`, `bl_batu`, `bl_nachtwache`, `bl_wache_*_bericht`, `bl_kirche`. Casanovas Rede vor dem ganzen Dorf beginnt so mit „The day moves on. Something else needs you.“ Dazu bekommen die Folgetakte `bl_funk_rosi`, `bl_funk_rosi_charly`, `bl_funk_sophia`, `bl_funk_nichts`, `bl_wache_elsa`, `bl_wache_yamamoto`, `bl_wache_keiner`, `bl_kirche_don`, `bl_kirche_don_schlaeft` mitten in der Szene dieselbe Standardkarte. Vorschlag: die Folgetakte in `ohne_karte` eintragen (wie schon `bl_abend_s2` und die `rm_*_b`), für die Pflichtszenen eigene Sätze, z. B. `bl_rede` „It is noon. The whole village has come to the church, and so have you.“, `bl_bar` „The fighting has stopped for tonight. Alva has opened her bar again, so you walk over.“, `bl_kirche` „You hear children crying inside the church, so you go up the steps.“

**B3 · Rückbezüge ohne Erinnerung oder ohne Bedingung.** `bl_bar`: Alvas „Somebody promised me a round when this is over.“ läuft immer, das Drehbuch (Abschnitt 5, „Die letzte Runde“) will mit `bl_alva_runde` diesen Satz und sonst „On the house. Don't get used to it.“ Vorschlag: zwei Zeilen mit `gruppe`/`wenn` wie in `bl_cliff_platz` (`_je`). `bl_bericht`: „Keep the rifle until the rematch“ erinnert nicht an die Wette; Vorschlag: „...Keep Gemelli until our rematch at the bottles, Frankfurt. I can't hold it straight tonight.“ `bl_wache_keiner`: „That one isn't here tonight“ sagt nicht, wer; Vorschlag je Frame: „Elsa never signed on, Frankfurt. Then nobody goes. Pascal has it.“ bzw. ein Satz für Yamamoto. `bl_tueren`: Mina „like in 1924“ mit einem Halbsatz versehen („like in 1924, when the whole village rowed out“).

### 3.3 Cliffhanger

**C1 · Fünf Standardkarten in einer Szene von zwei Minuten, kein Skip.** `bl_cliff_alon`, `bl_cliff_alon_siri`, `bl_cliff_platz`, `bl_cliff_team`, `bl_cliff_blicke`, `bl_cliff_megan` stehen nicht in `ohne_karte`. Nach jedem Chip erscheint „It is night now. Something else needs you.“ mit „Go on“, also genau dort, wo der Schnitt vom Platz auf Alons Bühne sitzen soll. `bl_cliff_netz` selbst hat auch nur den Standardsatz. Vorschlag: die sechs Folgetakte in `ohne_karte`, für `bl_cliff_netz` ein eigener Satz, z. B. „It is late, and nobody has gone home. You sit down with the others on the church steps.“ Besser auf Dauer: `kern/ereignisse.py`, `uebergang_text` gibt für Events, die über `direkt` geöffnet wurden, immer `""` zurück (Merker in `ort_oeffnen`), dann kann das nicht mehr passieren.

**C2 · Megans Anruf klingelt nicht.** `bl_cliff_megan` ist `gag1` mit `fern=True` auf dem Kirchplatz; die Lage sagt „your phone rings“, aber es gibt keinen Ton und keinen Annehmen-Bildschirm, anders als bei `bl_frist` (Art `handy`, Video, „Accept“). Vorschlag: `ZEILEN_TON` in `client/index.html` um `bl_cliff_megan: {0: "anruf_klingeln"}` ergänzen (die Kennung nutzt der Client schon für Videoanrufe); oder das Event als `handy`/Video bauen, wenn Megans Ort im Flugzeug als Hintergrund bestellt wird (Bestellliste).

**C3 · Das Dorf dreht sich um, und niemand außer Casanova reagiert.** `bl_cliff_blicke`: „the faces in the blue light turn towards you“, aber in `P1` steht nur Casanova. Rosi und Elsa sind seit `bl_cliff_netz` auf dem Platz. Vorschlag: zwei Kreise ohne Zeile, damit die Stille bleibt (`("rosi", "?", "closes the laptop")`, `("elsa", "-", "has stopped writing")`), und eine kurze Zeile vor Casanovas Frage, damit eine zweite Stimme trägt: Elsa „[clear throat] For the record, Duc. Did you know about this?“ (Gefühl `disappointment`). Der Chip „Opens his mouth.“ bleibt, Megans Anruf schneidet weiter ab. Danach Abschnitt 11 auf eine Tabelle mit allen sieben Takten und den fünf Spalten umstellen und die Zeile zu Alons Sprite berichtigen.

### 3.4 Tauchgang

**T1 · Der Plan hat keinen einzigen Beat.** `ortskapitel_tauchgang.md` legt Folgen, Figuren und Gegner fest, aber nicht, wie die Szene beginnt, wer spricht und wie sie endet. Vorschlag: vor dem Bau eine Beat-Tabelle nach dem Muster `nebenquest_red_trio.md` Z. 313ff. (Titelkarte, vertont, Reaktionen), mit den Spalten Ansage → Inhalt → Handlung → Reaktion → Übergang, mindestens für Abtauchen, Fund am Wrack, Name an der Galionsfigur, Auftauchen, Überfall, Rückkehr in den Hafen.

**T2 · Gebaute Szenen zitieren den Tauchgang schon.** Holm im Briefing von Welle 3 (`taktik_eden_rise.py` Z. 258): „That flag. Frankfurt, that's your man from the wreck.“ Ohne Tauchgang hat der Spieler Buenaventura dort nie gesehen. Vorschlag für die Zeit bis zum Bau: „That flag, Frankfurt. That's Captain Buenaventura. He has wanted the old wreck in our bay for years, and he's not paying for those torches himself.“ Nach dem Bau zurück auf die alte Zeile, dann mit Erinnerung im Satz („your man from the wreck, the one who chased you up from the Margot“).

**T3 · Überfall nur als „wie der Hafenkampf, nur epischer“.** Drei Tage später kommen sechs Wellen Belagerung; ohne Plan droht eine Wiederholung derselben Mechanik, und `akt2_kalender.md` Z. 61 rechnet nur etwa 2 Phasen für den Tauchgang. Vorschlag: im Plan festlegen, ob der Überfall auf der Taktik-Karte (Titelkarte und Skip sind dort schon da) oder als Ortskette läuft, wie viele Wellen, wer funkt und wer reagiert, und was ihn von Welle 3 und 4 unterscheidet.

## 4. Schluss

### 4.1 Gesamtquote je Regel (Ja von bewertbar, n/a nicht mitgezählt)

| Regel | Ja | teils | Nein | bewertbar | Quote Ja |
|---|---|---|---|---|---|
| R1 Titelkarte mit Continue | 28 | 14 | 12 | 54 | 52 % |
| R2 Skip möglich | 10 | 32 | 11 | 53 | 19 % |
| R3 Reaktionen der Anwesenden | 31 | 7 | 6 | 44 | 70 % |
| R4 Gefühl passt zur Lage | 48 | 1 | 1 | 50 | 96 % |
| R5 keine stumme Umschaltung | 42 | 9 | 4 | 55 | 76 % |
| R6 klare Frage vor den Chips | 40 | 9 | 4 | 53 | 75 % |
| R7 alle kommen zu Wort | 28 | 20 | 5 | 53 | 53 % |
| R8 Beat-Plan im Wiki | 0 | 44 | 12 | 56 | 0 % |
| R9 Erinnerung im Satz | 24 | 7 | 2 | 33 | 73 % |

Je Block (Ja von bewertbar): Anhörung R1 7/8, R2 9/9, R3 6/9, R4 8/9, R5 9/9, R6 7/7, R7 8/8, R8 0/9, R9 4/5. Belagerung R1 21/35, R2 1/35, R3 24/27, R4 33/34, R5 32/35, R6 26/35, R7 14/34, R8 0/35, R9 14/20. Cliffhanger R1 0/7, R2 0/7, R3 1/4, R4 7/7, R5 1/7, R6 7/7, R7 6/7, R8 0/7, R9 6/7. Tauchgang (Plan) überall 0.

Lesart: Die Anhörung erfüllt die Regeln fast vollständig, weil ihr Bildschirm Titelkarte, Continue, Skip und Tratsch eingebaut hat. Gefühle und klare Fragen sind überall stark (der Sprite-Test greift). Schwach sind Skip und Titelkarte im normalen Event-Bildschirm, stumme Kreise und der fehlende Beat-Plan im Wiki.

### 4.2 Top 5 Verbesserungen

1. **Keine Zwischenkarte mitten in einer Kette.** `kern/ereignisse.py`, `uebergang_text`: für Events, die über `direkt` geöffnet wurden, `""` zurückgeben; bis dahin die 15 Folgetakte aus C1 und B2 in `module/eden_rise/uebergaenge.json` unter `ohne_karte` eintragen. Hebt R1 und R5 im Cliffhanger von 0 bzw. 1 auf fast 7 von 7.
2. **Skip und Titel für ernste Pflichtketten.** `client/index.html`: in `evBrueckeHtml` den Event-Titel groß auf die Karte (`e.titel`), und für Pflicht-Events mit `ton: ernst` einen Knopf „Skip ▸▸“ wie in der Anhörung, der die Kette bis zum letzten Takt mit Folgen durchspielt. Dazu den Kopf-Chip „Gag“ (`EV_ART.gag1`) in ernsten Szenen wie „Breaking News“ oder „What Is Left“ durch „Story“ ersetzen und „Evening“ bei `bl_echo_*` durch „Morning“.
3. **Falsche Figur in `bl_leer` und `bl_ab_schon` beheben** (Fund B1). Kleinster Eingriff: `P1("holm")` ohne Chiara-Kreis.
4. **Rückbezüge mit Erinnerung und Bedingung** (Funde B3, A2, T2): `bl_bar` mit `gruppe`/`wenn` auf `bl_alva_runde`, `bl_bericht` Gemelli nennen, `bl_wache_keiner` je Person, Holms „your man from the wreck“ bis zum Tauchgang ersetzen, zwei Antibes-Sätze ergänzen. Stumme Kreise, die angesprochen werden (Totò in `bl_elsa_hilfe`, Holm in `bl_funk_rosi` und `bl_funk_sophia`, Rosi und Elsa in `bl_cliff_blicke`), bekommen eine kurze Reaktion.
5. **Beat-Tabellen ins Wiki, Stand-Zeilen nachziehen** (R8 = 0 %). `drehbuch_finale.md` Abschnitt 11 und `anhoerung.md` auf die fünf Spalten umstellen, für die Abende und Nächte einen eigenen Abschnitt anlegen, vor dem Bau des Tauchgangs die ganze Tabelle schreiben (`LEHREN.md` 02.11.). Dabei die veralteten Stellen berichtigen: Abschnitt 11 (Alon ohne Sprite), `belagerung.md` Tabelle „Gebaut“ (`bl_belagerung` steht dort auf Tag 21 Dinner, im Code Nachmittag; `bl_bericht` auf Tag 21 Nacht, im Code Tag 23 Abend) und Z. 113 (Charly statt Rosi am Satelliten).

Nebenfund ohne Regel: `ereignisse_belagerung.py` baut seine Zeilen mit `Z()` ohne Turbo-Tags, `ereignisse_belagerung_nacht.py` und `ereignisse_cliffhanger.py` mit `G()` und Tags. Laut Drehbuch ist die Belagerung schon vertont; neue oder geänderte Zeilen dort sollten über `G()` laufen.
