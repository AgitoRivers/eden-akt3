# Der Sturm · Tag 5

> Stand 27.10.2026 · Besitz: Story · Quelle: `kern/sturm.py` (Regeln), `client/plugins/eden-storm` (Bildschirm),
> `werkzeuge/eden_rise/sturm_eden_rise.py` → `module/eden_rise/sturm.json` (Posten, Eignung, alle Zeilen), Test `tests/test_sturm.py`.
> Vorschau: launch `eden-sturm` (8383, Vorbereitung) und `eden-sturm-nacht` (8385, Nacht nach Bot-Einteilung).

## Worum es geht

An Tag 5 ist Megan an Bord, und abends zieht ein Sturm auf. Duc teilt seine Crew ein, und in der Nacht zeigt sich, ob er
sie kennt. Vorbild ist die Selbstmordmission aus *Mass Effect 2*. Gespielt wird wie die Anhörung: Titelkarten,
alles vertont, Reaktionen, Tratsch, *Continue*/Enter/Leertaste, *Skip*. Die Spielleisten sind ausgeblendet.

## Ablauf

**Dinner, 18:00 – „Before the Storm“** (Szene `sturmvorbereitung`)
1. Titelkarte, Funkknistern, Megan kündigt den Sturm an (3 Varianten).
2. **Bitten:** Chiara, Rosi, Lea, Lola und Maxwell sagen je zwei Sätze, wohin sie wollen. Die Posten-Karte, um die sie
   bitten, hebt sich dabei an. Die Bitten enthalten Hinweise (z. B. Rosi: jemand anderes soll ihre Notlösung prüfen).
3. Megan: *„Five jobs, and six people if you count yourself.“* Dann das **Brett**: fünf Posten, darunter sechs Chips
   (die fünf und Duc). Chip anklicken oder ziehen, dann einen Posten. Nochmals auf den Posten klicken nimmt ihn zurück.
   Wer keinen Posten hat, **ruht**. *Send them* schickt alle los, leere Posten sind erlaubt, gehen aber nachts schief.
4. **Jede Einteilung wird kommentiert:** Die Person sagt zu, froh auf einem passenden Posten, zögernd auf einem schlechten.
   Wer ruht, sagt etwas dazu. Megan bewertet den Plan (stark/gemischt/schwach) und ob Duc selbst einen Posten nimmt
   oder frei bleibt. Danach **tuschelt die Crew** (Lea auf dem Anker, Lea nicht auf dem Anker, jemand ruht, sonst allgemein).

**Abend:** Megans leises Telefonat bleibt unverändert.

**Nacht, 23:30 – „What You Hear in the Dark“** (Szene `sturmnacht`)
1. Titelkarte, Donner. **Die erste Böe gelingt immer**: Alle packen zusammen an (drei Rufe), damit die Nacht nie
   ganz ins Frustige kippt.
2. Dann **fünf Krisen** in fester Reihenfolge: Kombüse 01:10 · Beiboot 01:35 · Strom 02:05 · Notlösung 02:30 ·
   Anker 03:15. Jede Krise: Blitz, Karte mit Uhrzeit, Ton, der Posten leuchtet auf dem Brett.
3. Ausgang je Posten nach **Eignung** der eingeteilten Person:

   | Eignung | Ergebnis | Was man sieht und hört |
   |---|---|---|
   | 3 | ✓ hält | stolzer Ruf der Person, Megan lobt |
   | 2 | ≈ hält knapp | angespannter Ruf, Megan notiert „barely“ |
   | 1 oder leer | ✕ verloren | Panik-Ruf, Erzähltext mit dem Schaden, Megan tadelt |

4. **Sprint:** Bleibt Duc beim Einteilen frei, darf er **einmal** in der Nacht hinrennen, wenn ein Posten verloren geht
   (*Run there* / *Stay put*). Die Person dort ist erleichtert. Ergebnis: ✓ bei der Notlösung (Ducs Stärke), sonst ≈.
   Nimmt Duc selbst einen Posten, gibt es keinen Sprint. *„You can't be everywhere.“*
5. **Stromausfall:** Ab der Krise *Power* gilt Notlicht (rot, dunkel), bis jemand den Strom wirklich zurückholt (✓).
   Danach rufen alle durcheinander (*„Torches!“*).
6. **Morgen** (06:10): Titelkarte, die Crew tuschelt je nach Nacht, wer geruht hat, bringt Frühstück, Megans Schlusssatz,
   *„Megan writes something down.“*, dann die **Bilanzkarte** (Posten ✓/≈/✕ mit Namen, alle Folgen).

## Eignung (wer passt wohin)

| | Lines & Anchor | Power | Galley | The Tender | The Makeshift Fix | bittet um |
|---|---|---|---|---|---|---|
| Chiara | **3** | 1 | 2 | 2 | 1 | Anker |
| Rosi | 1 | **3** | 1 | 1 | 2 | Strom |
| Lea | 2 | 1 | 2 | **3** | 1 | Anker |
| Lola | 1 | 1 | **3** | 1 | 1 | Kombüse |
| Maxwell | **3** | 1 | 2 | **3** | 1 | Beiboot |
| Duc | 2 | 2 | 1 | 2 | **3** | – |

Bester Plan: Duc prüft die Notlösung selbst, alle anderen auf ihre Stärke, eine Person ruht. Leas Wunsch (Anker) ist
die reizvolle Abwägung: Auf dem Anker hält sie nur knapp, aber sie bekommt das Vertrauen, um das sie gebeten hat.

## Folgen (fest, kein Würfeln)

- **Megans Haltung:** mindestens 4 Posten ✓ → Flag `sturm_bestanden` (+1), höchstens 2 ✓ → `sturm_chaos` (−1).
  Megans Haltung bestimmt in der Anhörung ihre Geduld (Haltung unter 0 kostet eine Ader, siehe [anhoerung.md](anhoerung.md)).
- **Vertrauen +1** für jede Person, die ihren **Wunschposten** gehalten hat (✓ oder ≈).
- **Verlorene Posten:** Kombüse und Strom je Crew-Moral −1, Beiboot 60 €, Notlösung 80 €, Anker 120 €.
- **Ruhe-Bonus:** Wer geruht hat, kümmert sich im Morgengrauen um alle, Crew-Moral +1.
- Flags je Posten `sturm_<posten>_<ok|knapp|weg>`, Chronik-Eintrag, je Figur eine Gedächtnis-Zeile.
- **Lagerfeuer an Tag 6:** Die Figuren bekommen die Nacht als Rückbezug und sprechen sie einmal an.

## Stimme, Musik, Ton

- 111 vertonte Zeilen (`st.*`), jede mit Turbo-Tag (`stimme_tags.json`), Vertonung: `Vertonen_EdenRise.bat` (vertont alles, was fehlt).
- Musik: Slot *sturm*, am Morgen *event_wholesome* (gute Nacht) oder *event_ernst*. Ambience: Deck abends, Nacht nachts.
- **Donner** (`donner`, Pixabay 192165 und 124463, Duc 27.10.): zu jedem Blitz einer Krise und **ab und an** alle 25–50 s
  im ganzen Sturm (nachts mit Blitz, abends ohne), nie innerhalb von 10 s nach dem letzten Schlag; dazu einmal zu Beginn
  von Megans leisem Telefonat (der Sturm zieht auf).
- Effekte: `funk_rauschen` (Auftakt), `chip_einrasten` (Zusagen), `sturm_nacht` (Wind zur ersten Böe),
  `schraubenschluessel_klong` (Kombüse), `wasser_platsch` (Beiboot), `blackout` / `strom_zurueck` (Strom), `alarm`
  (Notlösung), `ankerkette` (Anker), `schritte_kies` (Sprint), `wuerfel_fehlschlag` (verloren), `tag_beginnt`, `auftrag_feder`.
- Bilder: Nacht `yacht_aft_deck_storm.png`; neue Motive (Nacht vor Anker, Sturmfront in der Dämmerung) sind bei
  Character Design in Abnahme.
- **Duc im Bild (29.10.2026):** Die Crew-Kachel *You* und Ducs Zeilen im Sturm-Log zeigen sein Bild von vorne aus dem
  Character-Menü (Jacke = Look, gehaltene Waffe), derselbe Helfer wie in der Anhörung (den.duc_bild). Im runden
  Avatar zoomt die Kachel auf das Gesicht (den-storm.css).
