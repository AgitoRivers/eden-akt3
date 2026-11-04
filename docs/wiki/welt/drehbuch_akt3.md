# Drehbuch Akt 3: „Who Saw It?“ · Tag 24 bis Tag 35 · Version 2

> Stand 04.11.2026 · Besitz: Brain Trust (Cloud-Sitzung, Branch `akt3-cloud`) · **Entwurf zur Abnahme durch Duc, nichts davon ist gebaut.**
> Version 2 ersetzt Version 1 (Commit `506dce2`). Eingearbeitet sind die Gegenrede (`docs/uebergabe/drehbuch_gegenrede.md`, Branch `drehbuch-gegenrede`),
> der Abgleich Wiki gegen Code (`docs/berichte/wiki_vs_code.md`, Branch `wiki-vs-code`), die Folgen der Belagerung (`docs/wiki/welt/akt3_folgen_belagerung.md`,
> Branch `folgen-belagerung`) und das Text-Audit (`docs/uebergabe/audit_text.md`, Branch `audit-text`). Abschnitt 12 zeigt je Befund, was daraus wurde.
> Quellen im Kanon: [`akt3.md`](akt3.md), [`enden.md`](enden.md), [`dorf_figuren.md`](dorf_figuren.md), [`drehbuch_finale.md`](drehbuch_finale.md), [`belagerung.md`](belagerung.md),
> [`ortskapitel_tauchgang.md`](ortskapitel_tauchgang.md), die Figurenseiten, `kern/aufbau.py`, `ereignisse_mochis.py` (`mo_kommission`, `mo_frei_start`).
> Was neu ist und Kanon berührt, steht als E-120 „offen“ im Register. Spieltext Englisch, einfach, vertonbar. Turbo-Tags stehen hier in eckigen Klammern vor der Stelle, im Spiel nie sichtbar.

## 0. Feste Vorgaben dieser Fassung

| Vorgabe | Wie v2 sie einhält |
|---|---|
| Akt 3 = Tag 24 bis 35 (E-114) | Kalender beginnt an Tag 24 nach dem Cliffhanger. Im Code gebaut auf Branch `fix-akt2-folgen` (E-121): Sperre der Belagerung endet nach Tag 23, Schneider, Lesung, Holms Revanche und Rosis Expedition Pack ab Tag 24 |
| Duc trägt **immer** die Sonnenbrille (`figuren/duc.md:47`) | Keine Zeile und kein Chip nimmt sie ab. Nähe zeigt Duc über Haltung: er setzt sich, stellt etwas ab, bleibt stehen |
| Kommission passt zu `mo_kommission` | Tag 35, Phase „tag“, am Kai, Klapptisch, zwei Männer aus Ajaccio und ein Schreiber, Elsa legt vor. `mo_kommission` ist ein Beat darin (5.27) |
| Woche 4 atmet | Woche 4: 8 Pflicht-Events, höchstens 2 je Tag, Tag 27 ganz frei. Woche 5: 16 Pflicht-Events |
| Festa-Aufträge sind Spiel | Jeder Auftrag ist eine kurze Szene mit einer Entscheidung und kleinen Mengen (4.3) |
| Romanzen fertig spielen | Eigener Abschnitt 6 mit einer Schluss-Szene je Frau |
| Ungelesene `bl_`-Flags | Jedes bekommt einen Wirkpunkt (Abschnitt 8) |
| Offene Entscheidungen | Als Weiche mit zwei Zweigen (Abschnitt 1), nie als Tatsache |

## 1. Die Weichen (Duc entscheidet, das Drehbuch trägt beide Zweige)

| Weiche | Zweig A | Zweig B | Wo es im Drehbuch wirkt |
|---|---|---|---|
| **W1 · Die Yacht** (`tk_yacht_weg`) | **Auf Grund gesetzt** (Vorschlag Drehbuch Finale, Abschnitt 9): Sie sitzt mit dem Heck im flachen Hafen. Die Crew schläft bei den Familien, deren Häuser sie gerettet hat. Fünfte Baustelle `yacht` (Rosi, Petru, das Dorf). Megans VIP-Kabine und alle Szenen „an Bord“ spielen bis zum Heben im Dorf | **Gesunken** (heutiger Code): keine Baustelle, die Crew bleibt im Dorf bis zum Ende, Megan wohnt in Alvas Gästezimmer | 4.1, 5.1, 5.5, 6, Bestellliste. Jede Szene „an Bord“ nennt ihren Ersatzort |
| **W2 · Minicus Überleben** | **Erst in Akt 3 gezeigt** (Vorschlag): Der Bericht an Tag 23 lässt es offen, am Morgen von Tag 24 steht er am Tor (5.1, Beat „Wende“) | **Schon im Bericht gesagt:** Der Morgen von Tag 24 beginnt ohne die Enthüllung, Minicu steht trotzdem am Tor. Jana und Lola reagieren auf den Verband, nicht auf das Überleben | 5.1, 5.4, Siris Post (5.12) |
| **W3 · Festa-Flag** (`akt3_festa`) | **Die gebauten Festa-Events laufen, wie sie sind:** `akt3_festa` wird nach der Kommission gesetzt, `br_ehrenbuerger`, `ab_casanova_flamenco`, `gv_rotes_kleid` laufen innerhalb von `a3_festa` in fester Reihenfolge | **Die Festa wird neu geschrieben:** `a3_festa` übernimmt die drei Szenen als Beats, `akt3_festa` bleibt nur der Schalter, die alten Events werden stillgelegt | 5.29 |
| **W4 · Was 100 % schwer heißt** | Definition steht (E-121): 100 % = der Spieler hat nichts getan. **Balancing bleibt wie heute:** Anfänger verlieren in Welle 3 rund 3 von 4 Häusern, Vorbereitete 1 | **100 % wird härter:** mehr verlorene Häuser, öfter `tk_yacht_weg` | Akt 3 liest nur das Ergebnis: 0 bis 4 Baustellen plus W1. Jede Szene funktioniert mit 0 und mit 4 abgebrannten Häusern (4.1, „Nicht abgebrannt“) |

## 2. Die Idee in einem Satz

Zwölf Tage lang baut Duc ein Dorf wieder auf, das ihn am ersten Morgen nicht mehr ansehen will, und am Ende zählt nicht, wie stark er ist, sondern wer bereit ist, laut zu sagen, was er gesehen hat.

**Das Motiv:** *Who saw it?* Akt 2 fragte, wer die Linie hält. Akt 3 fragt, wer es gesehen hat und es sagt. Alon droht nicht mit Gewalt, sondern mit Papier: Jobs, Kredite, Anwaltsbriefe. Gegen Papier hilft nur ein Name, laut gesagt. Das Fischernetz am Ende ist die Liste dieser Namen.

**Was Duc weiß (eine Fassung für alle Szenen):** Ducs Firma gehört zur Eden Group. Dass die Gruppe das Hafenviertel heimlich verkauft hat und an wen, wusste er nicht (E-001, E-003). Sein Satz dazu ist immer derselbe Kern: *“My company belongs to the Eden Group. I didn't know they sold your harbour, or who bought it.”* Seine ESG-Arbeit hat mit dem Resort nichts zu tun (`figuren/duc.md`).

| Wer | Was er gesehen hat | Was ihn schweigen lässt | Seine Tür (4.2) |
|---|---|---|---|
| Petru | die Fackeln an seiner Werkstatt, die Boote von 1924 | A.V. hat den Kredit auf sein Boot gekauft | Werkstatt Stufe 2 oder heil |
| Mina | jede Tür in der Nacht der Türen | sie stellt die Drohbriefe selbst zu | Post Stufe 2 oder heil |
| Bà Tư | die Männer in Weiß, die zweimal nach dem Nordweg fragten | Alons Arbeiter sind ihre Kunden | `bl_batu_norden` oder Vertrauen 3 |
| Alva | Pascal an der offenen Barrikade, in ihrem Visier | sie war bewusstlos, man glaubt ihr nicht | Alva besucht (5.3), Bar Stufe 2 oder heil |
| Sandru | wer Alva aus den Trümmern trug | seine Beine gehören A.V. | Schiene (5.20) |
| Don Anghjulu | den Verrat am Tor, wenn er nüchtern war | das Kirchendach, das Beichtgeheimnis | an seiner Seite an der Tür (5.8) |
| Minicu | White, ein Schlag | niemand will ihn vor Fremden reden lassen | nach Hause geschickt (5.4) |
| Casanova | das Papier, das jede Nacht auf den Stufen lag | ihre Schuld am Elternhaus | Elsas Berichte gehört (5.11) |
| Buenaventura | wer ihn bezahlt hat | **nichts**, ihm glaubt nur keiner | meldet sich selbst (5.2) |

## 3. Kalender und Bogen

**Wochentage:** Tag 14 war Sonntag (Messe), also sind Tag 21, 28 und 35 Sonntage. Tag 24 ist ein Mittwoch.
**Phasen:** Frühstück, Tag, Nachmittag, Dinner, Abend, Nacht. Karten (also echte Zeit des Spielers) gibt es in **Tag, Nachmittag, Dinner, Abend** (`akt2_kalender.md`, Messung). Frühstück und Nacht zählen nicht als freie Kartenphasen.

### Woche 4 · „The Morning After“ (Mi 24 bis So 28)

| Tag | Frühstück | Tag | Nachmittag | Dinner | Abend | Pflicht |
|---|---|---|---|---|---|---|
| **24** Mi | `a3_morgen` | `a3_schwur` | frei | frei | frei | 2 |
| **25** Do | `a3_uhr` (mit den ersten Briefen) | frei | frei | `a3_megan_landet` | frei | 2 |
| **26** Fr | `a3_festa_tafel` | frei | `a3_don_tuer` | frei | frei | 2 |
| **27** Sa | frei | frei | frei | frei | frei | **0** |
| **28** So | frei | `a3_messe_schublade` | frei | frei | `a3_berichte` | 2 |

Woche 4: **8 Pflicht-Events**, freie Kartenphasen **15**. Empfohlen und mit Erinnerung angeboten (keine Pflicht): Alva besuchen (5.3), Minicu nach Hause schicken (5.4), Nonnas Kiste (5.9, ab Tag 27), Holms Revanche (5.13, ab Tag 24 mit Gemelli), Baustellen, erste Festa-Aufträge, Mochi in der Macchia.

### Woche 5 · „Name Your Price“ (Mo 29 bis So 35)

| Tag | Frühstück | Tag | Nachmittag | Dinner | Abend | Pflicht |
|---|---|---|---|---|---|---|
| **29** Mo | `a3_idee` | frei | frei | frei | frei | 1 |
| **30** Di | `a3_maxwell_flug` | frei | frei | frei | frei | 1 |
| **31** Mi | frei | frei | frei | `a3_megan_monaco` | frei | 1 |
| **32** Do | frei | frei | `a3_switched_off` | frei | frei | 1 |
| **33** Fr | `a3_einladung` (Maxwell zurück) | frei | frei | frei | `a3_festa_frage` | 2 (+1 `a3_schiene`, wenn möglich) |
| **34** Sa | `a3_villa_plan` | `a3_villa_keller` | frei | `a3_villa_dinner` | `a3_villa_ende` | 4 (Nacht: `a3_letzte_nacht`) |
| **35** So | `a3_sonntag` | `a3_kommission` mit `mo_kommission` | `mo_frei_start` (gebaut) | `a3_festa` | Ende, Epilog | 5 |

Woche 5: **16 Pflicht-Events** (17 mit Schiene). Freie Kartenphasen Tag 29 bis 34: **18**. Gags laufen bis Tag 31, ab Tag 32 ist das Spiel gagfrei. **Switched Off liegt deshalb auf Tag 32**, dem ersten Tag ohne Gags.

### Spannungsbogen

| Tag | Szene | Spannung | Aufgabe |
|---|---|---|---|
| 24 | Der Morgen danach | 6 → 3 | dem Dorf ins Gesicht sehen |
| 24 | Der Schwur | 3 | Bleiben lassen oder prüfen |
| 25 | Die Uhr, die Briefe | 5 | Zeugenliste öffnet |
| 25 | Megan | 4 | ihr die Wahrheit sagen |
| 26 | Die Tafel | 2 | Aufträge sehen |
| 26 | Don an der Tür | 4 | dazustellen oder nicht |
| 27 | frei | 1 | durchatmen |
| 28 | Messe, Schublade | 4 | ein leiser Fund, kein Gipfel |
| 28 | Elsas Berichte | 3 | Casanova taut auf |
| 29 | Die Idee | 3 | Lösung für Buenaventura |
| 30 | Maxwell fliegt | 3 | Abschied auf Zeit |
| 31 | Monaco | 6 | Wer zahlt? |
| 32 | **Switched Off** | 8 → 4 | der eine schwere Moment |
| 33 | Einladung, Festa-Frage | 6 | Wen nimmst du mit? |
| 34 | **Villa** | 9 → 10 | „Join me. Name your price.“ |
| 35 | Kommission | 7 | Wer sagt aus? |
| 35 | Festa | 10 → 2 | Schlussbild |

**Ein schwerer Moment (Prüfstein Ton):** Nur Switched Off ist schwer. Schublade und Nonna bleiben kurz und leise (`dorf_figuren.md`). Die Villa ist Spannung und Aktion, keine Trauer.

### Zeitbudget (Prüfstein Zeitbudget, ohne Bot-Lauf)

Freie Kartenphasen Tag 24 bis 34: **33**. Ein Bot-Lauf ist erst möglich, wenn der Kalender gebaut ist, die Zahl ist von Hand gerechnet.

| Bedarf | Phasen | Begründung |
|---|---|---|
| Baustellen | 2 bis 4 | Die Piraten tragen ab Tag 24 je Tag eine Stufe (gebaut), Minicu jeden dritten Tag eine. Bei 4 Häusern (12 Stufen) ist fast alles bis Tag 34 fertig. Duc beschleunigt, er muss nicht alles selbst tragen |
| Zeugen | 4 | Petru, Mina, Bà Tư und Alva fragt Duc in ihrer Dank-Szene (ohne Phase, 4.1). Sandru, Don, Minicu, Casanova je eine Phase |
| Festa-Aufträge | 6 bis 8 | acht kurze Szenen, zwei davon zählen zugleich als Romanzen-Zeit (4.3) |
| Romanzen | 2 bis 4 | eine Schluss-Szene je verfolgter Frau, meist eine oder zwei Frauen |
| Freie Dates und Abende | 3 bis 5 | |
| Optional | 3 bis 6 | Mochi, Riscossore, Scrap Field, Siris Post, Alva, Minicu, Lot 14 |
| **Summe** | **20 bis 31 von 33** | etwa 60 bis 95 %. Wer alles will, muss wählen, aber nicht hetzen |

## 4. Die drei Mechaniken

### 4.1 Die Baustellen („Lend a Hand“)

**Vorbild:** das Gemeinschaftshaus in Stardew Valley. **Gegenvorbild:** Anno-Verwaltung ohne Menschen.

- **Fundament (gebaut):** `kern/aufbau.py`. Jedes Haus mit `tk_haus_weg_<id>` (`post`, `batu`, `bar`, `werkstatt`) wird Baustelle mit drei Stufen. Notdürftig geflickt (`tk_haus_geflickt_<id>`) beginnt bei Stufe 1. Nach `buenaventura_schwur` tragen die Piraten je Tag eine Stufe.
- **Karte „Lend a Hand“** (1 Phase): Duc baut eine Stufe mit eigenem Material. Jede Stufe hat eine kleine Wahl, keine Menge: *Wer hält mit?* Ein Pirat, der Besitzer oder ein Crew-Mitglied. Der Besitzer bringt eine Zeile über sein Haus, der Pirat eine Zeile über das, was er angezündet hat, das Crew-Mitglied eine Romanzen-Zeile (zählt als Zeit zusammen, `kern`-Töpfe Quelle „Szene“). So ist jede Stufe auch ein Gespräch.
- **Minicu** trägt nach `a3_minicu_heim` jeden dritten Tag eine Stufe dazu. Keine Szene nennt das als Belohnung (Kanon).
- **Fertig** (`aufbau_fertig_<id>`, gebaut) → **Dank-Szene** `a3_dank_<id>`. In dieser Szene fragt Duc den Besitzer, ob er aussagt (4.2). Das kostet keine eigene Phase:

| Haus | Dank-Szene | Wirkpunkt im Code |
|---|---|---|
| Post | Mina hupt zweimal vor dem Kai. Sie stellt die erste Post nach dem Brand zu, und es ist keine Rechnung | **Zugang:** Mina bringt einmal am Tag eine Zutat oder ein Baumaterial aus Bastia mit, das es im Dorf nicht gibt (Wahl aus drei, ohne Phase) |
| Bà Tưs Laden | Bà Tư stellt zwei Teller hin, diesmal auch einen für Lola | **Küche:** Kochen mit Bà Tư (Zutaten ★★), ihr Thịt kho als Rezept, Akzent „Ăn đi“ (+10 % Leben bis zum Dinner des Folgetags) |
| Alvas Bar | Alva schreibt den ersten neuen Namen auf Papas Tafel | **Abende:** Bar-Abende wieder möglich, Alvas Festa-Auftrag öffnet, mit `bl_alva_runde` schreibt sie unter *“Paid. P.”* eine zweite Zeile (8, `bl_alva_runde`) |
| Petrus Werkstatt | Petru hängt das Ruder zurück über die Tür, heil oder verkohlt | **Angeln vom Boot:** die fünf Küstenbilder ohne Expedition, Auftrag *The Catch* öffnet |

- **Nicht abgebrannt (W4):** Ohne Baustelle kommt die Dank-Szene am Abend von Tag 24 als „Danke fürs Retten“, kürzer, mit derselben Frage nach der Aussage. Wer gut gespielt hat, gewinnt Zeit, nicht weniger Inhalt.
- **Die Kirche** ist keine Baustelle. Das Dach war Alons Geld (Kanon „Der Preis“). Es tropft bis zum Ende, nur Ende 3 und ★ reparieren es im Epilog (E-096).
- **W1 Zweig A:** fünfte Baustelle `yacht`, Stufen 6 Timber, 4 Iron, 2 Steel. Ihre Dank-Szene ist Rosis: *“She floats. She's ugly, she leaks a bit, and she floats. Don't tell her I said ugly.”* Megan zieht dann in die VIP-Kabine.

### 4.2 Die Zeugen („Who Saw It?“)

**Vorbild:** Mass Effect 2, Loyalitätsmissionen; Persona 5, Confidants. **Gegenvorbild:** L.A. Noire (Raten ohne lesbare Gründe). **Darum kein Rätselchip.**

- **Auslöser:** `a3_uhr` (Tag 25). Elsa gibt eine Liste mit neun Namen, als Seite im Codex („Witnesses“), mit Bild, Angst und Tür. Kein Prozentbalken.
- **Die Tür** ist eine Tat aus dem Spiel (Tabelle in Abschnitt 2). Ist sie zu, sagt die Liste warum, als Satz: *“Not while her bar is a building site.”*
- **Das Gespräch** stellt eine klare Frage. Duc hat drei Chips. **Jeder Chip ist eine ehrliche Haltung** (herzlich, frech, nüchtern), und **jeder überzeugt**, wenn die Tür offen ist. Die Haltung entscheidet nur, **wie** der Zeuge aussagt: Die Zeile vor der Kommission ändert sich, und die Haltung zählt bei der Figur als Vertrauen (+4 / +2 / +2, die passende Haltung nach Figurenseite +6). So gibt es keine falsche Antwort, nur eine, die besser zu diesem Menschen passt.
- **Ein Zeuge schweigt nur**, wenn seine Tür bis Tag 34 zu bleibt. Dann sitzt er bei der Kommission sichtbar am Rand, ohne Zeile, und sein Name fehlt im Netz.
- **Ergebnis:** `a3_zeuge_<id>` und die Haltung `a3_zeuge_<id>_<h>`. Zählt auf Säule Gemeinschaft und auf Megans Anruf (5.18).
- **Selbst im besten Durchlauf fehlt einer** (Kanon „Das Netz hat Lücken“): Pascals Knoten bleibt immer leer. Sandru kann nur mit Schiene aussagen.

**Pascal steht nicht auf der Liste** und nie in einem Fall (Auflage der Story-Sitzung). Elsas Liste hat am Rand eine durchgestrichene Zeile. Sie sagt nichts dazu.

### 4.3 Casanovas Tafel („THIS. IS. THE. FESTA!“)

**Vorbild:** Stardew Valley, Bündel und Festival; Spiritfarer (jeder Wunsch hat einen Menschen). **Gegenvorbild:** Survival-Einkaufslisten.

- **Auslöser:** `a3_festa_tafel` (Tag 26). Acht Aufträge an der Kirchenmauer. **Jeder Auftrag ist eine kurze Szene** (1 Phase) mit einer Entscheidung. Material braucht es wenig, gekauft zählt nicht (*“From the shop? Monsieur. This is a festa, not a supermarket.”*).
- **Wirkung:** `a3_festa_<id>` stellt etwas ins Schlussbild, und **die Entscheidung bestimmt, wie es aussieht**. Wie voll die Festa ist, liest das Ende zusammen mit den Säulen (Abschnitt 7): Die Tafel bestimmt Ausstattung und Licht, das Ende bestimmt, wer bleibt.

| Auftrag | Wer | Szene | Die Entscheidung | Wenig Material | Ins Schlussbild |
|---|---|---|---|---|---|
| **The Catch** | Petru | Eine Ausfahrt im Morgengrauen auf Petrus Boot (nach Wiederaufbau oder heil) | Wohin? Zum Riff (viele kleine Fische), zur Grotte (Buenaventuras Leute zeigen die Stelle, nur mit `a3_eco_tours`), aufs offene Wasser (ein großer Fisch, Angeln-Probe) | 3 Fische aus dieser Fahrt | Grill am Hafen, je nach Wahl Sardinen, Muränen-Spieß oder ein ganzer Zackenbarsch |
| **The Garden** | Nonna | Ernte mit Nonna im Klostergarten | Für wen ist das erste Körbchen? Für die lange Tafel, für Bà Tưs Topf oder für Frederico (nur wenn er lebt) | 3 Gemüse ★★★ (gebaut: Garten) | Körbe auf der langen Tafel |
| **The Pot** | Bà Tư | Bà Tư korrigiert Ducs Thịt kho (Kanon) | Ihr Rezept oder das Rezept seiner Mutter? Beide gelingen, Bà Tư reagiert anders | 1 Gericht ★★ | dampfender Topf, eine Schlange davor |
| **The Menu** | Lola | Lola hat Angst vor so vielen Gästen | Wer probiert zuerst? Minicu, Casanova oder Duc selbst | 1 Kochen in der Kombüse (W1: in Alvas Küche) | Lola am Grill, Schürze |
| **The Lights** | Rosi | Rosi baut die Lichterkette | Was kommt in den Schalter? Ein Chip von Duc (echter Verlust, die Kette leuchtet weiß) oder ein Teil aus Alons Halsbändern (die Kette leuchtet bernstein wie Unit-01s Auge) | 2 Steel (Scrap Field oder Belagerungs-Roboter) | Lichter über der Piazza, weiß oder bernstein |
| **The Stage** | Minicu | Bühne bauen, Minicu trägt | Für wen ist die Bühne zuerst? Kinderchor, Casanovas Rede oder Alvas Flamenco | 4 Timber | wer zuerst auf der Bühne steht |
| **The Dresses** | Danzel | Anprobe in „Le Théâtre Rouge“ (gebaut: Schneider) | Wessen Kleid zuerst? Eine der Frauen oder Casanova | ein Festa-Auftrag aus `schneider.md` | ein Kleid im Schlussbild |
| **The Bell** | Don | Zwei Abende Karten statt Wein (zwei kurze Besuche, je eine Abend-Phase; mit `bl_kirche_don` reicht einer) | Lässt Duc ihn gewinnen oder nicht? | – | die Glocke läutet zum Tanz im richtigen Takt |

Zwei kleine Aufträge kommen dazu, wenn Akt 2 sie verdient hat: **Kinderbilder** (Jana, nur `bl_kirche_jana`, ohne Phase, die Kinder bringen sie) und **The Eventually liefert** (Buenaventura, nur `a3_eco_tours`, Kanon: er beliefert die Festa). Die Konfettikanone fehlt, Pascal hatte sie bezahlt (Kanon). In Ende 1 ist sie wieder da.

## 5. Die Szenen

Jede Szene: **Ansage → Inhalt → Handlung → Reaktion → Übergang**. Titelkarten mit Continue und Skip. Ernste Szenen nur mit ernsten Posen, kein joy oder amusement (`test_sprite_stimmung`). Vor jedem Chip stellt eine Figur eine klare Frage.

### 5.1 Tag 24, Frühstück · `a3_morgen` „The Morning After“ (ernst → warm)

Anschluss an den Cliffhanger: Alon hat Duc vor dem Dorf „their consultant on the ground“ genannt.

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Titelkarte *Day 24 · The Morning After*. Piazza im Morgenlicht (`village_piazza`), Rauch über der Post (nur mit `tk_haus_weg_post`). | Erzählerin: *The village slept in the church. Nobody slept much.* |
| Inhalt | Duc kommt mit zwei Kaffeebechern von Bà Tư (W4: steht ihr Laden nicht, aus der Kombüse oder vom Feuer am Kai). Die Leute gehen auseinander, als er kommt. Auf einem Handy läuft noch Alons Clip. | Mina, leise: *“Sorry, Yacht. I don't know what to say to you today.”* |
| Inhalt | | Erzählerin: *A man near the fountain asks it out loud: “Did you know?”* |
| Handlung | Duc antwortet. | Chips: Puts both coffees down on the fountain. “My company belongs to the Eden Group. I didn't know they sold your harbour.” · “No. And I'm staying until you believe me.” · Stays where he is and says nothing. |
| Reaktion | Stille. Dann tritt Petru vor ihn, mit dem Rücken zu Duc, das Gesicht zum Dorf. | Petru: [clear throat] *“Hm. I rowed out with Mina while he carried water to the church. Three days. That's all I need to know.”* |
| Reaktion | Er geht. Ein paar folgen ihm. Die anderen bleiben, aber sie bleiben. | Lola, zu laut: *“Right! Who wants breakfast? I made heaps. Mostly the eggs.”* |
| Wende (W2 A) | Am Tor steht jemand, groß, verbunden, die Axt gesenkt. Titelkarte *Minicu*. | Jana: [gasp] *“Jessas! He's... Sir, he's standing!”* |
| Wende (W2 B) | Minicu steht am Tor, wie man es im Bericht gehört hat. | Jana: *“Sir, he's back at the gate. With the bandage and everything.”* |
| Inhalt | | Minicu: *“Pascal said hold the gate. So I hold it.”* · Lola: [sniff] *“Oh, mate. Oh, you big... I'm bringing you eggs, don't you move.”* |
| Übergang | Neue Karten: „Talk to Minicu“ (5.4), „Visit Alva“ (5.3). Ziel-Zeile: *Buenaventura has asked the whole village to meet at the harbour.* | |

Zu W1 A: Die Crew kommt aus den Häusern der Familien, Lola aus Bà Tưs Küche. Der Wohnort steht nur in der Lage, die Beats bleiben gleich.

### 5.2 Tag 24, Tag · `a3_schwur` „The Oath“ (komisch → ernst → warm)

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Titelkarte *The Oath*. Hafen (`village_harbour`). *The Eventually* an der Mole, die purpurne Flagge auf halbmast. | Erzählerin: *Forty men stand on the quay. None of them is holding a torch.* |
| Inhalt (Kanon: der Fernseh-Moment) | Ein Pirat hält ein Handy hoch. Alons Clip: „pirates attacked a small village“. | Buenaventura: [laugh] *“I am famous! Look, Paco, that is our flag!”* (Pause) *“...Robots? I have never owned a robot in my life. They are saying I had robots!”* |
| Inhalt | Er wird ernst, nimmt den Hut ab. | Buenaventura: [clear throat] *“We burned your houses. I gave the order to stop, and I gave it too late. I am sorry.”* · *“I don't know how a man makes that right. I have a flag, an anthem and forty men who can carry stones. We will find a way. I swear it.”* |
| Reaktion | | Casanova: *“You... you burned the post office.”* · Buenaventura: *“Yes, Madame.”* |
| Handlung | Er fragt Duc, nicht das Dorf. | Buenaventura: *“You beat me twice, Señor. So you decide. Do we stay and carry, or do we sail?”* · Chips: “Stay. Start with the houses you burned.” · Turns to Casanova. “Ask her, not me.” · “Stay. And you tell the commission who paid you.” |
| Reaktion | „Ask her“: Casanova: *“Stay. And carry everything twice.”* (Vertrauen Casanova +4). Kommission: *“Of course. I am a pirate, not a liar.”* | |
| Reaktion | | Petru: *“Hm. Then carry stones.”* |
| Schluss | Ein Pirat trägt eine ausgebrannte Fackel am Gürtel (Saat für die Fackelgalerie, Kanon). | Buenaventura: *“Leave that.”* · Pirat: *“It's my torch, Capitán.”* |
| Übergang | `buenaventura_schwur`. Baustellen auf der Karte. Ziel-Zeile: *The burned houses are building sites now. Lend a hand when you can.* | |

Mit Bibi und `mo_eco_idee` steht sie hinten und zählt die Piraten. Erzählerin: *Bibi is counting the pirates. You don't know why yet.* Ihr Einfall kommt an Tag 29 (Kanon: an diesem Tag kennt niemand die Lösung).

### 5.3 Ab Tag 24, freie Karte · `a3_alva_wach` „Since Last Night“ (ernst)

Karte „Visit Alva“ ab Tag 24 Nachmittag, mit Erinnerung, wenn sie zwei Tage liegt.

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Mina holt Duc. | Mina: *“Yacht! She's awake. Sandru says come, and Sandru never says come.”* |
| Inhalt | **Bar abgebrannt:** Hinterzimmer in Bà Tưs Laden (oder, wenn auch der Laden brannte, ein Feldbett in der Kirche). **Bar steht:** `alvas_hinterzimmer`. Nie im A.V. Market, das gehört zu 5.19. Sandru sitzt auf einem Hocker, die Schienen surren. | |
| Inhalt | | Alva: [cough] *“How long?”* · Sandru: *“Since last night. You missed the end. Ha. That's... sorry. That's not funny.”* |
| Inhalt | | Alva: *“Minicu?”* · Sandru: *“He's standing at the gate. He won't go home.”* · Alva: [sigh] *“Of course he won't.”* |
| Handlung | | Alva: *“Who carried me out, Duc? Don't lie to me, I'll know.”* · Chips: “Sandru. He carried you out of the rubble.” · Looks at Sandru and waits. · “Does it matter?” |
| Reaktion | Wahrheit: Alva sieht Sandru lange an. *“...Orangeade's on me, then. For a year.”* · Sandru: *“I'm thirty, Alva.”* · Alva: *“I know how old you are. I was there.”* Warten: Sandru sagt es selbst und lacht davor. „Does it matter?“: *“Everything matters to me, Duc. That's my whole problem.”* | |
| Übergang | `a3_alva_wach`. Alvas Zeugen-Tür geht mit der Bar auf. Kein Paar (Kanon). | |

### 5.4 Ab Tag 24, freie Karte · `a3_minicu_heim` „Is Pascal Coming?“ (ernst, leise)

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Nordtor, die Barrikade halb weg. Kevin sitzt auf dem Torpfosten. | Erzählerin: *He has been standing here since six. Lola brought eggs twice.* |
| Inhalt | | Minicu: *“Hello. Does it still hurt? Your arm. You had a cut.”* |
| Handlung | | Minicu: *“Pascal said hold the gate. Did he say stop?”* · Chips: “You can go home now, Minicu. You held it.” · “Not yet. But I'll tell you when.” · Sits down next to him on the stones and waits. |
| Reaktion | „Go home“: | Minicu: *“Is Pascal coming?”* · Chips: “No.” · “I don't know.” · Looks at the gate and doesn't answer. |
| Reaktion | | Minicu, nach einer langen Pause: *“Okay.”* Er nimmt die Axt. Nach drei Schritten: *“Who holds it now?”* Kevin bleibt sitzen. |
| Übergang | `a3_minicu_heim`. Ab morgen trägt er an den Baustellen. Zeugen-Tür offen. | |

Mit `bl_minicu_duc_zuerst` (Welle 6) sagt Minicu zuerst: *“You came first. Before Pascal. I heard you.”* Wer sich setzt und wartet, bekommt die Karte am nächsten Tag noch einmal, und Minicu sagt: *“You came back. Thank you.”*

### 5.5 Tag 25, Frühstück · `a3_uhr` „Under Control“ (ernst, mit trockenem Haken)

Zusammengelegt aus „Uhr“ und „Briefe“ (Gegenrede G4). Elsa hat in der Nacht von Tag 23 alles an die Kommission geschickt (Cliffhanger, gebaut).

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Messe (`crew_mess`, W1 A: Bà Tưs Laden), Telefon auf Lautsprecher. Titelkarte *Under Control*. | |
| Inhalt | Ein Beamter aus Ajaccio (Stimme ohne Bild). | Beamter: *“We received your file, Lieutenant. All of it. Two men from the commission will come on the thirty-fifth.”* · Elsa: *“That's ten days.”* |
| Inhalt | | Beamter: [clear throat] *“We're very busy here. And we have the feeling you have this under control. Don't you?”* · *“To be honest, we were surprised. Cala d'Orsu sends us a report every month. 'All quiet.' Signed and stamped.”* |
| Reaktion | Elsa legt auf. | Elsa: *“Five years on this post, and they have never been this polite to me.”* · *“I sent them a report every month too. Through the town hall. So where did mine go?”* |
| Inhalt | Mina kommt mit der Vespa, ohne Hupe, zwölf Einschreiben aus Monaco im Korb. Einen hält sie hoch. | Mina: *“There's one for Petru. A.V. bought the loan on his boat. And I have to take it to him. Me.”* |
| Handlung | Elsa wendet sich an Duc. | Elsa: *“First Officer. The commission wants witnesses. People who saw it with their own eyes and will sign their name. Will you help me find them?”* · Chips: “I'll talk to every one of them.” · “What about the crew? We saw everything.” · Takes Mina's basket. “Then we start with the letters.” |
| Reaktion | Crew: *“You're guests, and Alon just called you his partner on television. The village has to speak for itself.”* · Korb: Mina: *“...Okay. You knock. I'll hold the bike.”* | |
| Zusatz | **Totòs Versprechen** (`ereignisse_grotte.py:514`, „Make the crate count against Alon“): Hat Duc die Kiste aus der Grotte behalten (`gr_kiste_genommen`), bietet Totò sie hier an. Totò: *“Comandante. The crate from the grotto, the one with the collars. Give it to her. I promised you it would count.”* Chip: Hands Elsa the crate. Setzt `alon_kiste_genutzt` (innerhalb der Frist) und einen Beweis für 5.27 | |
| Übergang | Zeugenliste offen. Kopfzeile: *Commission in 10 days.* Elsa: *“Tomorrow I drive to Ajaccio. I want to see these 'all quiet' reports myself.”* | |

### 5.6 Tag 25, Dinner · `a3_megan_landet` „Until I Land“ (ernst, Megan-Theater)

Vorschlag zum offenen Rückkehrtag (E-117): **Tag 25**, zwei Tage nach dem Netz. Ihr Satz im Cliffhanger: *“Don't say a word to anyone until I land.”*

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Wassertaxi aus Bastia, ein Koffer. Achterdeck (`aft_deck`; W1 A: der Kai). | Erzählerin: *No helicopter this time. A water taxi from Bastia, and one suitcase.* |
| Inhalt | | Megan: [sigh] *“How... delightful. I leave for three weeks, and my yacht becomes a field hospital.”* · Holm: *“Megan.”* · Megan: *“Captain. You're standing.”* · Holm: *“Mostly.”* |
| Handlung | Megan nimmt Duc beiseite. | Megan: *“Duc. Alon thanked 'our partners at the Eden Group'. Did you know who was buying the harbour?”* · Chips: “No. Did you?” · “I didn't know they were selling it at all.” · Doesn't joke this time. “Mac. I'd never sell them.” (nur mit `megan_funke`) |
| Reaktion | | Megan: *“I negotiated that sale. Every line. I never asked who A.V. was, because the numbers were good.”* · *“So that's two of us who didn't ask.”* |
| Inhalt | Sie bietet einen Handel an, wie immer mit Preis. | Megan: *“Here's the deal, First Officer. I'll try to stop the sale. The board in Monaco won't believe a video, they'll call it fake. They want paper and names. Can you get me names?”* · Chips: “I'm already collecting them.” · “Why do you care now?” · “What's in it for you, Mac?” |
| Reaktion | Warum: *“Because he nearly sank my ship. And because I signed it.”* · Mac: [chuckle] *“A seat on the board. Obviously. And a quiet evening, maybe. Don't push it.”* | |
| Übergang | `megan_zurueck` (gebaut, VIP-Kabine; W1 A: Alvas Gästezimmer bis zum Heben), löscht `megan_abgereist`, setzt `a3_megan_handel`. | |

### 5.7 Tag 26, Frühstück · `a3_festa_tafel` „THIS. IS. THE. FESTA!“ (komisch, warm)

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Piazza. Casanova auf einem Stuhl, eine Tafel an der Kirchenmauer, Kevin darauf. | Erzählerin: *She has been here since five. The board is taller than she is.* |
| Inhalt | Rede mit Pause für Applaus. **Diesmal klatscht Minicu**, zu laut und allein (nur mit `a3_minicu_heim`, sonst Kevin, der kreischt). | Casanova: *“Cala d'Orsu! They burned our houses. They want us to cancel the festa. So we will NOT!”* (Pause) · Erzählerin: *One person claps. Very loudly. It's Minicu.* · Casanova: *“...Thank you, Minicu. Thank you. That was very loud.”* |
| Inhalt | | Casanova: *“Eight jobs. Every job is a person. Nothing from the shop! This is a festa, not a supermarket.”* |
| Handlung | Sie sieht Duc an, zum ersten Mal seit dem Cliffhanger. | Casanova: *“Monsieur. I need fish, lights and a stage. Can I count on you, or should I count on someone else?”* · Chips: “Count on me.” · “I'll bring you the fish myself.” · “Count on me. And on the pirates.” |
| Reaktion | | Casanova: *“Good. ...Good. That's all I wanted to know today.”* Sie dreht sich schnell weg. |
| Komisch | Kevin sitzt auf „The Catch“. | Casanova: *“And somebody get that bird off the fish!”* |
| Übergang | Tafel offen (4.3). | |

So bleibt die Stille ohne Applaus allein der Festa (Muster dreimal vermieden, G14).

### 5.8 Tag 26, Nachmittag · `a3_don_tuer` „The Priest at the Door“ (ernst, Heiter-Moment)

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Rathaus, Treppe zu Pascals Zimmer (Bestellung `town_hall_stairs`, Platzhalter `village_piazza`). Ein Dutzend Leute mit Kisten. Elsa ist in Ajaccio. | Erzählerin: *They want to throw everything he owned into the harbour.* |
| Inhalt | Don vor der Tür, ohne Flachmann. | Don: *“No.”* · Mann: *“Father, he opened the gate!”* · Don: *“I know what he did, my son. I was there.”* · *“Nobody goes in. Not today.”* |
| Handlung | | Mann: *“Are you with him or with us?”* · Chips: Walks up the stairs and stands next to Don. · “Elsa needs what's in there. Leave it until she's back.” · Stays at the bottom of the stairs. |
| Reaktion | Neben Don: *“Thank you, my son. My knees are not as brave as my mouth.”* (Vertrauen +6, Zeugen-Tür) · Elsa: Die Leute gehen murrend, Don: *“Hm. Logic. I never tried that.”* · Unten: Don hält allein, später: *“Not everyone has to stand on stairs.”* | |
| Schluss | Don holt den Flachmann doch heraus, sieht ihn an, steckt ihn wieder ein. | |
| Übergang | `a3_don_tuer`. Die Schublade bleibt heil. | |

### 5.9 Ab Tag 27, freie Karte · `a3_nonna_kiste` „The Last Crate“ (ernst, kurz, leise)

Kanon: Die Kiste stand am Morgen nach der Belagerung (Tag 24) vor Nonnas Tür. Nonna öffnet den Brief erst, **nachdem** Don sich vor Pascals Tür gestellt hat, so versteht sie es rückblickend (`dorf_figuren.md`). Karte ab Tag 27 („Nonna asks for you“, über Frederico oder den Boten). Kommt Duc bis Tag 29 nicht, bringt Mina Schlüssel und Brief mit einem Zettel von Nonna (kürzer, ohne ihre Stimme).

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Klostergarten. Titelkarte *The Last Crate*. Eine Holzkiste mit Setzlingen, ein sauber gefalteter Brief. | Erzählerin: *Every week there was a crate of seedlings at her door. This one came the morning after the siege. She waited three days to open the letter.* |
| Inhalt | Nonna liest Pascals Sätze vor. | Nonna (liest): *“I told the priest not to go up the mountain. 'Stay, Don. Leave it with me.' I thought it was for safety.”* · *“And I told him all of it, every month, for nine years. He can't say a word. That's why he drinks.”* |
| Inhalt | Nonna, zu sich: | Nonna: *“And on Friday he stood in front of that door for him. Now I understand.”* |
| Reaktion | Zur Kiste: | Nonna: [sniff] *“I told Isabelle that man has a good heart. You don't have a good heart, Pascal. You have a bad conscience.”* |
| Zusatz | Mit `bl_minicu_sag_es` steht ein Satz mehr im Brief: | Nonna (liest): *“Duc told me to say it to him. So I did. It was the only true thing I said that night.”* |
| Handlung | Unter den Setzlingen ein alter Schlüssel mit Zettel. | Zettel: *“Leave it with... no. You do it. I just have the key.”* · Nonna: *“The cellar door of the Casanova house. Do you want it, or shall I throw it in the sea?”* · Chips: Takes the key. · “Keep it, Nonna. I'll find another way in.” |
| Reaktion | Nimmt: Item „Cellar Key“ (`a3_kellerschluessel`). Lehnt ab: `a3_schluessel_nein`, Casanova führt an Tag 34 (Kanon). | |
| Schluss | Sie pflanzt die Setzlinge trotzdem. | Erzählerin: *She plants them anyway. Nothing in her garden goes hungry.* |

Item: *Old iron, a little rust, a ribbon from a seedling tray. It came in a crate of seedlings. The man who sent it used to open every door in this village.*

### 5.10 Tag 28, Tag · `a3_messe_schublade` „Sunday, Eleven Months“ (warm → ernst, leise)

Zusammengelegt (G4). Erst die Messe, dann die Schublade. Spannung 4, ein Fund, kein Gipfel (G13).

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Kirche (`church`). Ein Eimer in der ersten Reihe, es tropft. | Erzählerin: *The new roof was his money. The money stopped. The rain did not.* |
| Inhalt | | Don: *“Today I'll keep it short, because the roof is listening.”* |
| Inhalt | Draußen an der Haltestelle reißt ein Vater den Busfahrplan ab. Kein Kind im Bild (Kanon). | Erzählerin: *The school bus won't come on Monday. A father takes the timetable down and folds it very small.* |
| Inhalt | Bà Tư drückt Duc eine Dose in die Hand. | Bà Tư: *“Eat. You're too thin. And don't look at the bus stop like that. You didn't stop that bus.”* |
| Ansage | Rathaus, Pascals Zimmer (Bestellung `pascal_room`). Schreibtisch, verschlossen. **Ein leerer Haken an der Wand, ein heller Rand, wo der Hut hing.** Elsa ist zurück, mit einem Brecheisen. | |
| Inhalt | | Elsa: *“Father. I'm going in.”* · Don: *“You're the law, Lieutenant. I'm only a door.”* |
| Inhalt | Erstes Blatt. | Elsa: *“My antenna form. Eleven months. 'Almost through.'”* Kein Witz. |
| Inhalt | Vier Bilder, je ein Satz. | Erzählerin: *Elsa's reports to the mayor, never delivered.* · *Casanova's EU applications, signed, never sent.* · *Copies of the monthly report to Ajaccio: “All quiet.” His signature.* · mit `rt_ende_alle` oder `ark_aussagen_3`: *The signed statements from the red team. Elsa handed them in herself.* · mit `bl_wache_gesehen`: *A radio log. Night of the twenty-second, three o'clock: two words.* Holm erkennt die Uhrzeit, ein Beweis mehr |
| Wende | Ganz unten ein Kassenbuch in derselben sorgfältigen Hand. | Elsa: [sigh] *“The roof. The school bus. The festa money. And here: the priest. Sandru. ...Madame Casanova.”* |
| Handlung | | Elsa: *“This goes to the commission. All of it, or only his part? Think about it until then. You'll be there when I hand it over.”* · Chips: “All of it.” · “Only Alon's part. The village has paid enough.” · “I don't know yet.” |
| Reaktion | Vorgemerkt (`a3_buch_alles` / `_teil` / `_offen`), endgültig an Tag 35. | Elsa: *“For the record: I'd make the same face you're making.”* |
| Übergang | Item „Pascal's Ledger“ bei Elsa. Ziel-Zeile: *Elsa wants to read the reports to Casanova tonight.* | |

### 5.11 Tag 28, Abend · `a3_berichte` „Every Report“ (ernst, Casanovas Wende)

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Kirchenstufen bei Nacht (Bestellung, Platzhalter `village_piazza`). Kerzen, Elsa mit einem Stapel. | |
| Inhalt | | Elsa: *“March. 'Dogs with collars near the monastery road.'”* · *“May. 'Request for a meeting with the mayor.'”* · *“August. 'Request for a meeting with the mayor.'”* · Erzählerin: *She reads thirty-one of them. Casanova doesn't stop her once.* |
| Reaktion | Casanova leise und kurz, ihre Stimme beim Thema Elternhaus. | Casanova: *“He told me you never wrote.”* · Elsa: *“I wrote every month, Madame.”* |
| Handlung | | Casanova: *“Monsieur. Pascal kept the truth in a drawer for nine years. What did you keep in yours?”* · Chips: “Nothing about your harbour. But I should have asked my own company more questions.” · Sits down on the step below her. “Only that I'm sorry it came on television.” · “I'm still here. That's my answer.” |
| Reaktion | Erste: *“Questions. Hm. Nobody here asked enough of those, Monsieur.”* (+6) · Zweite: Sie nickt. (+4) · Dritte: *“Yes. You are. So is the bell, and the bell has no choice.”* (+2) | |
| Schluss | | Casanova: *“Lieutenant. From now on you report to me. Directly. Every day, if you like.”* · Elsa: *“Every day, Madame?”* · Casanova: *“...Every week.”* |
| Übergang | `a3_berichte`, Casanovas Zeugen-Tür. Elsa schickt die EU-Anträge selbst (Saat für den Brüssel-Brief im Epilog). | |

### 5.12 Ab Tag 25, freie Karte · `a3_siri_post` „In My Own Words“ (ernst → warm)

Kanon: Siris Post in eigenen Worten (Säule Wahrheit), Yasin bekommt Geld für sein Video angeboten (`belagerung.md`), Vaters Pullover (`siri.md`).

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Vorderdeck oder Kai bei Sonnenuntergang (W1). Yasin mit Handy, Siri im Pullover ihres Vaters, dem mit den Sternen. | |
| Inhalt | | Yasin: *“Bro. Somebody offered me twenty thousand for the video. Twenty! That's business.”* |
| Inhalt | Wer kauft? Eine Agentur, die Alon gehört. Siri weiß es. | Siri: *“It's his company, Yasin. He'll buy it and nobody will ever see it.”* |
| Handlung | Siri fragt Duc. | Siri: *“Duc. I want to post it myself. No filter, no music, just what we saw. Is that brave or stupid?”* · Chips: “Brave. Post it.” · “Post it, and I'll stand next to you when he calls it fake.” · “Ask Yasin. It's his video too.” |
| Reaktion | Yasin, beim dritten Chip, ein ehrlicher Satz, dann überspielt: *“...I filmed Minicu falling, and I kept filming. I don't want money for that. Okay? Don't tell anyone I said okay.”* | |
| Weiche W2 | Mit `siri_wartet` (sie wollte auf Minicu warten): Die Karte kommt erst, wenn Minicu wieder steht (W2 A: Tag 24 Morgen; W2 B: sofort). Mit `siri_darf_posten`: Siri erinnert an die vier Sekunden im Cliffhanger: *“It was up for four seconds, and then his video slid over it. This time I'm not giving him four seconds.”* | |
| Übergang | `a3_siri_post`, Beweis für Säule Wahrheit. | |

### 5.13 Ab Tag 24, freie Karte · `a3_revanche` „The Rematch“ (komisch, warm)

Nur mit Gemelli (gebaut, `kern/schiessen.HOLM_TAG = 24`). Holm hatte im Bericht gesagt: *“Keep it until the rematch.”*

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Holm auf der Mole, ohne Krücke. Petru hat Flaschen auf einen Felsen gestellt. | Holm: *“Frankfurt. You still have my rifle. I want it back, so we shoot for it. Ready?”* |
| Inhalt | Schießwette (gebaut). | Holm: *“It pulls left, like the day you won it from me.”* |
| Reaktion | Gewinnt Duc: *“Faen. Keep it. I'll win it back at the festa.”* · Verliert Duc: Sie prüft Gemelli und gibt es zurück. *“Keep it anyway. My hands are fine now. My head isn't, yet.”* Mit `bl_nachtwache_niemand`: leiser Nachsatz: *“I told you to send somebody to the north road that night. I should have gone myself.”* | |
| Schluss | Petru stellt die letzte Flasche wieder hin. | Petru: *“Hm. Again.”* · Holm, zu ihm: *“Takk.”* |

### 5.14 Tag 29, Frühstück · `a3_idee` „Forty Men and a Boat“ (komisch → warm)

Drei Fassungen, die erste passende gilt.

| Fassung | Bedingung | Kernzeile |
|---|---|---|
| Bibi | `rt_bibi_bleibt` und `mo_eco_idee` | Bibi: [laugh] *“So he's got forty men, a boat and nothing to do? And they know every rock in that bay? Doudou. Doudou, come here. I need you to do some numbers.”* (Kanon) |
| Lea | `margot_geborgen` (Flag der Tauchgang-Sitzung, Fragenliste F-05) | Lea: *“Did you know a protected bay needs people who know every rock? Proper people, with boats. And they've got forty!”* |
| Petru | sonst | Petru: *“Hm. Boats need captains. He has one boat and forty men who are good at one thing. Finding things in caves.”* |

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Hafen, die Piraten tragen Schiefer, Buenaventura zählt laut auf Spanisch und verliert sich. | |
| Inhalt | Die Idee (Fassung oben). | |
| Handlung | | Buenaventura: *“Tours? Tourists? On my ship? Why would a pirate do that, Señor?”* · Chips: “You were a pirate. Now you're a captain with a debt.” · “You'd be head of something. Head of Sea Captains Eco Tours.” · “There's a rock in front of the grotto. At low tide, it's an island.” |
| Reaktion | | Buenaventura: *“Head of...”* (Pause) *“...Sea Captains Eco Tours.”* (Pause) *“I would need a hat.”* |
| Wende | | Buenaventura: *“But the grotto belongs to him. The old man with the oranges. And I owe him everything already. The ship. Even the name of the ship.”* |
| Übergang | Karte „The Man with the Orange“ (5.15). | |

### 5.15 Ab Tag 29, freie Karte · `a3_orange` „The Man with the Orange“ (ernst-komisch, grau)

Bitter mit `gennaro_verschwunden` (Kanon: Riscossore hat Gennaro auf dem Gewissen). Wird nicht aufgelöst.

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Grotte, Halle. Riscossore schält eine Orange. Totò kommt mit, ab Vertrauen 3. | Mit `gr_8_riscossore` (Duc hat ihn besiegt): Riscossore: *“Last time you came with a knife. Today you came with a captain. Better.”* · Ohne: Erzählerin: *An old man in a white suit sits by the water and peels an orange. Everybody here owes him money.* |
| Inhalt | | Buenaventura: *“I want to show tourists your grotto. I pay you from every ticket.”* · Riscossore: *“Eventually.”* · Buenaventura: *“...Eventually.”* · Riscossore: *“A man in prison pays nobody. A man with tourists pays me every day, a little. I prefer every day.”* |
| Handlung | | Riscossore: *“You want something too, I think. The commission. Why should I come and open my book for you?”* · Chips: “Because Alon paid Buenaventura through you. It's in your book.” · “Because nobody pays you if Alon gets the bay.” · Looks at Totò and says nothing. (nur mit `gennaro_verschwunden` und Totò dabei) |
| Reaktion | Erste: *“Clever. Not kind. Clever.”* · Zweite: *“Yes. That is the reason. Not kindness. I want you to know that.”* · Dritte: Erzählerin: *Totò walks out. Somewhere off Cap Corse, Gennaro's boat is still empty.* Riscossore: *“He hates me. He should.”* (Pause) *“I'll come.”* | |
| Schluss | | Riscossore, zu Buenaventura, ein Orangenstück: *“Here. Your first payment.”* |
| Übergang | `a3_riscossore_kommt`, `a3_eco_tours` (nur im guten Weg sichtbar, Kanon). | |

Ohne diese Szene kommt Riscossore trotzdem zur Kommission (Kanon), als Überraschung.

### 5.16 Tag 30, Frühstück · `a3_maxwell_flug` „Gogo's Medicine“ (warm, Maxwell-Kanon)

Kanon (`maxwell.md`): Maxwell fliegt Gogos Medizin selbst, drei Tage weg, seine Angst gegen seine Liebe.

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Kai, Maxwell mit einer Kühltasche, sehr still. | |
| Inhalt | | Maxwell: [clear throat] *“Number One. Mr. Maximum is going to fly. In an aeroplane. Up there.”* · *“Gogo's medicine is in Johannesburg, and the post is too slow. So he carries it himself.”* |
| Handlung | | Maxwell: *“Tell Mr. Maximum something, brother. What does a big man do when he's scared of the sky?”* · Chips: “He takes the window seat and looks anyway.” · Puts a hand on the cool box. “He carries it. Like you always do.” · “He holds Jana's hand. She's coming to the airport.” |
| Reaktion | Jana: *“Coach, I'll hold your hand the whole way to Bastia. Sorry. Not sorry.”* (dritter Chip) | |
| Übergang | Maxwell fehlt Tag 30 bis 32 (kein Training, kein Maxwell in Szenen), zurück an Tag 33. | |

### 5.17 Ab Tag 29, freie Karte · `a3_lot14` „Lot 14“ (ernst, Rosi-Kanon)

Kanon (`rosi.md`): Rosi erfährt durch Yamamoto, dass Alon Papas Werkstatt in Catania für Bürogebäude kaufte, „Lot 14“. Nur wenn Yamamoto ab Vertrauen 3. Liegt vor Monaco, damit es auf Ende 2a und 3 einzahlt.

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Werkstatt. Yamamoto mit einem Tablet, verbeugt sich zu oft. | |
| Inhalt | | Yamamoto: *“So sorry, Rosi-san. I read A.V.'s property lists for my bank. There is a street in Catania. Lot 14. A workshop, closed three years ago.”* |
| Reaktion | Rosi redet über eine Maschine statt über sich (Figurenseite). | Rosi: *“...The press in that workshop was older than Papa. It had a crack in the left side. He called it Nonna.”* |
| Handlung | | Rosi: *“Officer. If he goes down, can I buy it back? Tell me the truth.”* · Chips: “If he goes down, yes. So let's make him go down.” · “I don't know. But I'll help you try.” · Sits down on the toolbox next to her and waits. |
| Übergang | `a3_lot14`. Zahlt auf Rosis Ende (kauft die Werkstatt zurück, Enden 2a und 3). | |

### 5.18 Tag 31, Dinner · `a3_megan_monaco` „The Board“ (ernst, Säule Geld)

Videoanruf aus der VIP-Kabine (W1 A: Alvas Gästezimmer). Der CEO ist laut Kanon Ducs Fan und tritt kaum auf (`nebenfiguren.md`): nur Stimme, schwarzer Bildschirm mit Logo.

**Megans Erfolg hängt an dem, was Duc ihr bringt** (G17): ab 4 Zeugen **oder** 2 Beweisen (Abschnitt 7). Yamamoto mit Bindung 5 ruft vorher an und stoppt den Kredit (Kanon): *“Officer-san. So sorry. I have stopped the loan. I did not ask permission. Very rude of me.”*

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Megan in Boardroom-Kleidung, Duc außerhalb der Kamera. | Megan: *“Stay out of the picture, First Officer. And don't breathe so loudly.”* |
| Inhalt | | Megan: *“I have {zeugen} people ready to sign. In front of a commission.”* · CEO: *“Megan. A.V. pays us well. Is this about the yacht, or about you?”* |
| Wende (genug) | | Megan: *“It's about a bay that's worth more protected than sold.”* · CEO: *“...Is Duc there? Put him on.”* · Chips (Duc tritt ins Bild): “The numbers are hers. The names are the village's. I just carried the letters.” · “Sell them the bay, and you sell them me with it.” |
| Wende (zu wenig) | | CEO: *“Bring me something better than a fishing village, Megan.”* Bildschirm aus. |
| Reaktion | | genug: Megan: *“That's the first argument I've won that I actually believe in. It's... uncomfortable.”* · zu wenig: *“How... delightful.”* (leise) |
| Übergang | `a3_megan_wende` oder `a3_megan_verloren`. Die Säule Geld braucht weiter die Margot (Kanon). | |

### 5.19 Tag 32, Nachmittag · `a3_switched_off` „Switched Off“ (ernst, **der** schwere Moment)

Tag 32 ist der erste Tag ohne Gags. Die Szene kommt immer, ob Sandru reden wollte oder nicht. Sonst passiert es, *weil Alon kann* (Kanon).

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Keine Titelkarte. Mina rennt die Mole herunter, ohne Vespa. | Mina: *“Yacht! YACHT! The market. It's Sandru.”* |
| Inhalt | A.V. Market (`av_market`), Sandru zwischen den weißen Regalen. Die Schienen sind still. Keine Musik. | Erzählerin: *The braces are quiet. You never noticed the sound until it stopped.* |
| Inhalt | Ein Bildschirm über der Kasse, nur Text. | Bildschirm: *Device paused. The user broke the rules of service. Thank you for your understanding.* |
| Inhalt | | Sandru: [laugh] *“Ha. They switched me off. Like a lamp.”* · mit `a3_zeuge_sandru`: *“I said one word on the phone. One. 'Yes.'”* |
| Wende | Die Tür. Alva kommt herüber, **zum ersten Mal** in das Haus ihrer Mutter. Titelkarte *Alva*. | Erzählerin: *She has not stepped into this house in six years.* |
| Handlung | | Alva: *“Duc. The door. Can you hold the door?”* · Chips: Holds the door. · Takes his other arm. · Steps back and lets her do it. |
| Reaktion | Alva trägt ihn über die Straße in ihre Bar (W4: oder auf eine Matratze in der Baustelle) und die Treppe hoch. | Alva: [sigh] *“You're my little brother, you idiot. I've carried you since you were six.”* · Sandru: *“I know. That's the whole problem.”* |
| Schluss | Kein Paar. | Erzählerin: *She sits on the stairs for a minute. Then she goes back down to the bar.* |
| Übergang | `a3_sandru_aus`. Siehe 5.20. Gags mit Ton `witzig` bleiben für den Rest des Akts aus. | |

### 5.20 Tag 33, Frühstück · `a3_schiene` „No Leash“ (warm, leise)

Nur wenn Duc sich um Sandru gekümmert hat (`sandru_surren` oder `sandru_herkunft` oder Vertrauen Sandru ab 3; `sandru_herkunft` ist noch nicht gebaut, Fragenliste). Zwei Fassungen (Kanon: ist Rosi gefeuert, hört Maxwell das Surren und Rosi hilft aus der Ferne).

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | **Rosi da:** ihre Werkstatt. **Rosi gefeuert:** Maxwells Kabine (W1 A: Petrus Werkstatt), Maxwell gerade zurück, Rosi per Video. | |
| Inhalt | | Rosi: *“Same motors. Same chips. I only took out the part that talks to his computers. The leash, Officer. Like with the collars.”* · gefeuert: Maxwell: *“Mr. Maximum holds the screwdriver. Rosi says which way. It's teamwork, brother.”* |
| Inhalt | Sandru steht auf. Die Schienen surren tiefer. | Rosi: *“That sound is mine now. Don't let them tell you otherwise.”* |
| Handlung | | Sandru: *“A.V. gave me six years of walking. You gave me a speech.”* (Kanon) · *“...And her. You gave me her.”* · Chips: “You gave yourself the speech. I just listened.” · “Go and stand in front of Alva. Straight.” |
| Reaktion | Erste, mit `sandru_herkunft`: Sandru lacht nicht. *“Iskander. You can say it. My mother says it.”* · Zweite: *“Ha. One thing at a time, Duc.”* | |
| Übergang | Namensschild ISKANDER mit `sandru_herkunft`, sonst SANDRU. `a3_sandru_schiene`, Zeugen-Tür offen. | |

Ohne Schiene steht Sandru an Tag 34 auf Alons Seite, auf Beinen, die wieder an sind: *“They switched me back on. That's how it works, Duc.”* Sein Name fehlt im Netz.

### 5.21 Tag 33, Frühstück · `a3_einladung` „An Invitation“ (ernst, Mina)

| Beat | Zeilen |
|---|---|
| Ansage | Mina an der Mole mit einem schweren, cremefarbenen Umschlag. Sie hält ihn nur. |
| Inhalt | Mina: *“This one's for you, Yacht. The good paper. From the house on the hill.”* · Erzählerin liest: *“Dinner. Tomorrow at eight. Just you. A.V.”* |
| Inhalt | Mit `bl_blatt_gefunden`: Erzählerin: *Your name on the envelope is in a careful hand. You have seen it before: on Minicu's name sheet, the one you picked up at the gate, and on Alon's letters on the church steps.* Sonst nur: *Your name is written in a very careful hand.* |
| Handlung | Mina: *“Are you going?”* · Chips: “Yes.” · “Yes. But not alone.” · “I don't know yet.” |
| Übergang | Ziel-Zeile: *Tomorrow: dinner at the villa.* Mit Schlüssel: *And you have a key.* Maxwell kommt am Kai an, mit leerer Kühltasche: *“Mr. Maximum has flown. Mr. Maximum will never speak of it.”* |

### 5.22 Tag 33, Abend · `a3_festa_frage` „Who Are You Taking?“ (frech, warm)

Startet die Schluss-Szenen der Romanzen (Abschnitt 6). Jede Frau ab Vertrauen und Begehren 4 fragt in einer kurzen Szene. Duc wählt **eine** oder niemanden. **Lea oder Sophia, nie beide** (Schwestern-Regel). Megan nur mit `megan_funke` und einer gemeinsamen Nacht.

| Frau | Ihre Frage | Bei Ja auf der Festa |
|---|---|---|
| Chiara | *“First Officer. I'll ask you once, and if you laugh, it's a two. The festa on Sunday. With me?”* | ihre Zehn (Kanon) |
| Alva | *“Somebody has to dance with me at the festa, Duc, or I'll dance with Kevin. Your choice?”* | Flamenco, „Only you“ (Kanon) |
| Lea | *“Two fingers? For the festa. Stay together. You know what it means. Yes?”* | ihre Azoren-Antwort wird Bild (Kanon) |
| Sophia | *“Ten euros says you'll ask me before I ask you. ...Oh. I've just asked you. Have I lost?”* | erste Lesung vor dem Dorf |
| Rosi | *“Officer. My mother wears yellow at every festa. If you come, she'll ask questions. Will you come anyway?”* | Rosis Mutter in Zitronengelb |
| Lola | *“Boss. I'm cooking for everyone on Sunday. Will you sit down with me for one song? Mostly one song.”* | Lola setzt sich hin |
| Siri | *“No camera at the festa. I want to be there with my own eyes. With you?”* | Siri ohne Handy im Bild |
| Bibi | *“Okay. Okay! The gates open on Sunday afternoon, the festa's at eight, and I'll be a mess. Will you come anyway?”* | nach *Last Page* (Kanon) |
| Megan | *“Don't make me say it twice, First Officer. One dance. Then we never speak of it. Agreed?”* | Abendkleid ohne Anker |

Die Gewählte steht in der Nacht von Tag 34 oben auf der Liste, mit eigener erster Zeile. Die anderen bekommen am Tag 35 ein freundliches Echo (`rm_e_*`, Anlass `festa_nein`), z. B. Chiara: *“A nine. For honesty. I'll live.”*

### 5.23 Tag 34, Frühstück · `a3_villa_plan` „The House on the Hill“ (ernst, kurz)

Eine Wahl, drei Zeilen (G4). **Elsa ist nicht dabei** (sie darf vom Schlüssel nichts wissen, `dorf_figuren.md`).

| Beat | Zeilen |
|---|---|
| Inhalt | Messe: Holm, Rosi, Megan, Casanova. Holm: *“You're invited, Frankfurt. That's not a warrant. It's better.”* · Mit Schlüssel: Rosi: *“A cellar door nobody locks properly. Old iron. My favourite kind of door.”* · Ohne: Casanova: *“I know the cellar. I hid there from my father when I was seven. I'll take you.”* |
| Handlung | Holm: *“Who goes down with you, Frankfurt?”* · Chips: Rosi · Casanova (ohne Schlüssel Pflicht) · Megan · Alone. |
| Übergang | `a3_villa_mit_<id>`. Der Nachmittag bleibt frei. |

### 5.24 Tag 34, Tag · `a3_villa_keller` „The Cellar“ (ernst, Mission)

Frame-Kette, vier Bilder, ein Kampf (zwei Agenten, ein Roboter, Steel als Beute). Ziel: der Beweis, dass das Feuer befohlen war (Säule Wahrheit, gegen die Lüge im Cliffhanger).

| Frame | Bild (Bestellung) | Inhalt |
|---|---|---|
| 1 | `villa_cellar` | Der Schlüssel passt. Mit Casanova: Sie bleibt an der Tür stehen. *“It's smaller than I remember. ...Go. I'll wait here.”* Sie betritt das Haus **nicht** (das bleibt ★, `enden.md`) |
| 2 | `villa_cellar` | Ein Server-Schrank zwischen alten Weinfässern. Rosi: *“He put his computers in a wine cellar. That's a crime too.”* |
| 3 | `villa_office` | Ein Ordner mit Whites Einsatzplan: *Day 22, phase 3: torches, houses.* Die Quittung an Buenaventura, bar. Item „White's Orders“ (`a3_beweis_feuer`) |
| 4 | Treppe | Zwei Agenten, ein Roboter. Kampf. Danach Musik von oben |

### 5.25 Tag 34, Dinner · `a3_villa_dinner` „Name Your Price“ (ernst, Spitze)

Alon ohne Kamera: ruhig und genau, kein Großsprecher (Figurenseite).

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Titelkarte *Name Your Price*. Speisesaal (`villa_dining`, Platzhalter `alon_keynote`). Ein Tisch für zwei, das Fenster zur Bucht. Pascal steht im weißen Fedora an der Tür. | Erzählerin: *From up here, the village looks like a model. The building sites look like toys.* |
| Inhalt | Alon im Anzug über dem Exoskelett. | Alon: *“Duc. Sit. Two of my people are asleep in my cellar, so I assume you came the back way. You've been busy.”* · *“Keep the folder. Paper. In my experience, paper loses.”* |
| Inhalt | Die Chips-Wendung (Kanon, `aufruestung.md`). | Alon: *“Every collar your mechanic cut open sent me one last message. That's how I learned to lock them. You helped me more than any engineer I hired.”* |
| Inhalt | Sein Motiv in einer Zahl. | Alon: *“Four hundred thousand people died in wars last year. I can bring that to zero. I need one bay and ten more years.”* · *“You've seen my health. I don't have ten years. So I need the bay now.”* |
| Handlung | **Das Angebot.** | Alon: *“Join me. Name your price.”* · Chips: “No.” · Looks out of the window at the village and says nothing. · “What would my price be?” · Puts his glass down. “Everyone I've met down there. Can you buy that?” |
| Reaktion | „What would my price be?“: *“Eden Consulting, free of debt. Your name on a building in Frankfurt. And you never think about this village again.”* Dann nur zwei Chips: “Deal.” · “No.” · ★ (alle vier Säulen, Yamamoto Bindung 5, Ende 1 gesehen): dritter Chip *“Deal. Let's sign it in front of the village.”* (Kanon) | |
| Übergang | Ja → `a3_deal`. Nein → 5.26. | |

### 5.26 Tag 34, Abend · `a3_villa_ende` „The Last Push“ (Presse, dann Kampf oder Festnahme)

| Beat | Was | Zeilen |
|---|---|---|
| Presse (Kanon: „vor laufendem Stream“) | Alon tritt auf die Terrasse. Eine Drohnenkamera streamt. Jetzt ist er der Großsprecher. Pascal neben ihm. | Alon: *“Hi, Cala d'Orsu! Quick update from your future. And a big thank you to my partner on the ground, Paul... Paolo. Thank you, Paolo.”* Pascal lächelt. Er korrigiert ihn nicht. · Erzählerin: *The man who knew every name in the village. His master doesn't know his.* |
| Mit Deal | Duc steht im Stream neben Alon. → Ende 1 (Kanon: Dank unter falschem Namen auch an Duc). | |
| Endkampf | Ohne Deal: Kamera aus, Alon wird ruhig, das Exoskelett fährt hoch. Kampf (Luft, tödlich, Kanon). Ducs Ausrüstung fällt nicht aus (Kanon). Mit Rosi (`werkstatt_offen`): Unit-01 bricht in Runde 3 durch die Kellertür, ein alter Diesel ohne Chip. | Rosi: *“I took the leash out.”* · Alon: *“I know. That's how I learned to lock it.”* · Rosi: *“She doesn't have a leash. She never did.”* |
| Festnahme | **Draußen**, an der Mole unter der Villa (G15): Duc kommt mit „White's Orders“ heraus, als eingeladener Gast. Elsa (Vertrauen ab 4, `elsa_hilft`) und die Küstenwache warten. Gilt auch nach einem gewonnenen Kampf. | Elsa: *“Mr. Varenne. Section nine. You have the right to say nothing, and I'd honestly prefer it.”* |
| Niederlage | Kein Game Over. | Alon: *“Go home, Duc. The commission is tomorrow. I'll be watching.”* |
| Pascal | Er geht in jedem Fall. Bei der Festnahme sieht er Elsa an. | Pascal: *“Lieutenant. Your mother's birthday is next week.”* Elsa antwortet nicht. |
| Übergang | `a3_alon_besiegt` und/oder `a3_alon_festgenommen` (Säule Stärke). Nacht: `a3_letzte_nacht` (wie die Belagerungs-Nächte, gebaut; mit Deal keine). | |

### 5.27 Tag 35, Tag · `a3_kommission` „Who Saw It?“ (ernst) **mit `mo_kommission`**

Ort und Besetzung wie das gebaute `mo_kommission` (`ereignisse_mochis.py:182-185`): **am Kai** (`village_harbour`), Klapptisch, **zwei Männer aus Ajaccio und ein Schreiber**, Elsa legt vor. Die Szene ist eine Kette in der Phase „tag“. Bau-Hinweis: `a3_kommission` öffnet, `mo_kommission` (unverändert, nur mit `mo_ark_beweis`) folgt als Beat, `a3_kommission_2` schließt. Reihenfolge über `direkt`.

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Titelkarte *The Commission*. Erzählerin: *Two men from Ajaccio. One folding table. One clerk with a lot of paper.* | |
| Inhalt | Der ältere der beiden (Rolle `kommissar`, „the gentleman“ aus `mo_kommission`). | Kommissar: *“We are here to find out what happened in this bay on the twenty-first, twenty-second and twenty-third. Who saw it?”* |
| Inhalt | **Die Zeugen**, je eine Zeile in ihrer Haltung (4.2). Wer schweigt, sitzt sichtbar am Rand. | Petru: *“I saw the torches. I saw who paid for them. And I saw who stayed.”* · mit Rudern: *“And the village rowed out. Like in 1924.”* · Mina: *“I knocked on every door that night. I don't read the post. This time I read it.”* · Bà Tư (mit `bl_batu_norden`): *“Men in white. They asked me twice for the north road. I told him then. Now I tell you.”* · Alva: *“I had him in my sights. I missed on purpose. Write that down.”* · Sandru: *“My name is {sandru_name}. I carried her out. And the man who switched off my legs is the man who paid for the fire.”* · Don, mit `bl_kirche_don`: *“I was sober. Write that down too. It doesn't happen often.”* · Don, ohne: *“I was asleep on the church steps, my son. But I saw the gate open before I fell asleep.”* · Minicu: *“Pascal said hold the gate. I held it. A man in white hit me. Once.”* · Casanova: *“I am the mayor of Cala d'Orsu. I signed nothing. And I am still here.”* |
| Inhalt | **Buenaventura.** | Buenaventura: *“A man named White paid me in clean money, like a bank. I gave the order to burn. I gave the order to stop.”* · Kommissar: *“And you are?”* · Buenaventura: *“Captain Buenaventura of The Eventually.”* · Kommissar: *“...I see.”* |
| Wende | **Riscossore** mit Orange (Kanon). | Riscossore: *“He's telling the truth. It's in my book, page forty-one. A man in prison pays nobody, so I'd like him to stay out.”* |
| Beat `mo_kommission` | Elsas Schuhschachtel mit den Halsbändern (gebaut, Wert nach `kern/mochis.beweis_stand`) | (gebaute Zeilen) |
| Inhalt | **Die Beweise**, je ein Satz, nur was der Spieler hat: Whites Einsatzplan (`a3_beweis_feuer`), die Kiste aus der Grotte (`alon_kiste_genutzt`), Siris Post (`a3_siri_post`), Sophias Notizen (`sophia_notizen`), Charlys Mitschrift und die Aufnahme von Whites Angebot (`bl_funk_charly`, `bl_funk_white`), das Funkbuch der Nacht (`bl_wache_gesehen`), die Zeugen der Nachtwache (`bl_nachtwache_*`), Adriens Fotos, der Steuerchip, das fremde Teil, die Aussagen des Red Trio. **Nichts über die Yacht von Tag 0** (`dorf_figuren.md`). | Sophia: *“Darling, I wrote down every time and every word that night on the radio. I didn't know why. Now I do.”* · Elsa (Nachtwache): *“For the record: Pascal used the radio at three. Two words, 'not yet'.”* |
| Handlung | **Das Kassenbuch**, jetzt endgültig. | Elsa: *“First Officer. All of it, or only his part?”* · Chips: “All of it.” · “Only Alon's part.” |
| Reaktion | Alles: Wahrheit stärker, der Kommissar liest auch Don, Sandru und Casanova vor. Casanova: *“Yes. Me too.”* Gemeinschaft schwächer. · Teil: Gemeinschaft stärker, Wahrheit bleibt, schwächer (Kanon) | |
| Schluss | | Kommissar: *“Thank you. We have what we need. Or we don't. You'll know tonight.”* |
| Übergang | Rechnet die Säulen (Abschnitt 7), setzt bei W3 A `akt3_festa`. | |

**Alvas Aussage zieht Pascal in keinen Fall** (Auflage der Story-Sitzung): Sie sagt nur, was sie sah, nicht, wer es war. Ihr Name für ihn fällt nicht.

### 5.28 Tag 35, Frühstück · `a3_sonntag` „Coffee, Not Wine“ (warm, kurz)

| Beat | Zeilen |
|---|---|
| Inhalt | Lola gibt Duc zwei Tassen. Lola: *“One for you, one for the priest. Will you take it to him, Boss, or shall I?”* |
| Handlung | Chips: Takes both cups to the church. · “You take it. He likes you better.” |
| Reaktion | Don: *“Coffee. On a Sunday. Like the morning of the last wave.”* Er trinkt. (Zahlt nur auf *The Bell*, wenn der Auftrag schon begonnen ist.) |

### 5.29 Tag 35, Dinner · `a3_festa` „The Festa“ (Schlussszene)

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Titelkarte *The Festa*. Piazza (`village_piazza`, das Festa-Bild). Die Tafel bestimmt Ausstattung und Licht (4.3), das Ende bestimmt, wer bleibt. | Erzählerin je Ausstattung: *Half the lights work. The tables are full anyway.* · *The whole bay is here. Even Kevin.* |
| Inhalt | Casanovas Rede mit Pause. Niemand klatscht, weil der, der immer anfing, weg ist (Bericht Tag 23). | Casanova: *“Cala d'Orsu has stood on this rock for four hundred years. Pirates came. Tax men came. A man with a satellite came. And tonight...”* (Pause) |
| Wende | Zwei Takte Stille. Dann fängt Alva an, langsam (Kanon). | Erzählerin: *Nobody claps. Then Alva does. Slowly. Then everyone.* · Casanova: [sniff] *“...Thank you, Alva.”* · Alva: *“Don't get used to it.”* |
| W3 A | `br_ehrenbuerger` (nicht in Ende 1), `ab_casanova_flamenco`, `gv_rotes_kleid` laufen in dieser Reihenfolge, wie gebaut | |
| W3 B | dieselben drei als Beats von `a3_festa`, neu geschrieben | |
| Inhalt | Der Moment der gewählten Frau (5.22). | z. B. Chiara: *“Ten. That's a ten, First Officer. Don't let it go to your head. ...Let it go to your head a little.”* |
| Inhalt | Holm tanzt nicht. Ihre Mutter (Kanon, Silhouette, Bestellung) sitzt neben ihr. Petru bringt zwei Gläser. | Holm: *“Mamma, this is Petru. He's the one who taught me to sit still.”* · Petru: *“Hm.”* |
| Wende | Mitternacht, das Ende (Abschnitt 7). | |
| Epilog | Minas Einschreiben (Kanon, jedes Ende): Pascals Tür, niemand macht auf. | Mina: *“Sign here.”* · Erzählerin: *Nobody is there. It's the first letter she can't deliver.* |

## 6. Romanzen fertig spielen

Jede Frau, deren Leiter bei Stufe 5 angekommen ist (`beziehungen.md`, Romanzen-Leiter), hat in Akt 3 **eine Schluss-Szene** zwischen Tag 24 und 32. Sie liegt vor Monaco und vor der Villa, damit sie dort zählt, und sie ist Durchatmen, kein Drama. Zwei davon sind **Expeditionen mit Rastplatz-Szene** (OFFEN.md, Duc 02.11.2026: Romanzen auf Expeditionen, Rastplatz als intime Szene). Jede beginnt mit einem Rückbezug auf ihre Belagerungs-Nacht oder ihren Abend (`bl_will_ab_<pid>`, `bl_ab_fertig_<pid>`), mit Erinnerung im Satz. Zwei Belagerungs-Nächte mit ihr (`bl_na_fertig_<pid>`) heißt Status „zusammen“ (Folge `fakt`, gebaut).

| Frau | Szene | Kern | Rückbezug mit Erinnerung |
|---|---|---|---|
| Chiara | **„Blackout“** (Kanon, `chiara.md:43`, Deutung zur Prüfung): Stromausfall auf der Brücke bei der ersten Probefahrt nach dem Heben (W1 A) oder beim Funktest im Dorf (W1 B). Sie muss Duc um Hilfe bitten, zum ersten Mal ohne Wertung | Romanze über Gefragtwerden | *“That night in the siege, when you came up to the bridge wing and I gave you a nine and a half...”* |
| Alva | „The Board Is Full“: Papas Tafel ist neu geschrieben, ihr eigener Name steht jetzt darauf, von Duc geschrieben | „Only you“ bleibt der Festa | *“...the evening on the quay, when I gave out free drinks and you said you'd pay the first round...”* |
| Lea | **Expedition** „One More Dive“: kurzer Tauchgang an der Mündung der Grotte mit Buenaventuras Leuten als Führer (nach `a3_eco_tours`), Rastplatz auf dem Felsen, der nur bei Ebbe eine Insel ist | die Azoren-Antwort reift | *“...two fingers, stay together, the sign I showed you on the swim platform...”* |
| Sophia | „The Fifteenth Letter“: Die fünfzehnte Antwort eines Verlags kommt mit Minas Post (wenn die Post steht). Duc öffnet ihn nicht, sie entscheidet | keine Show, ihre echte Stimme | *“...ten euros, the bet that you'd ask me what I actually want...”* |
| Rosi | nach `a3_lot14`: „Two Thirds“: Rosi und Duc setzen Unit-01 neu zusammen, Stoppuhr, unentschieden | „Captain“ fällt, wenn er es verdient hat | *“...the night with the stopwatch, when nobody lost...”* |
| Lola | „First Guest, Again“: Ihre Hütte am Strand hat überlebt (oder nicht), sie kocht für einen Gast | sie beendet einen ganzen Satz | *“...the night you said yes to the toastie and it wasn't burnt...”* |
| Siri | nach `a3_siri_post`: „No Caption“: Sonnenuntergang ohne Handy | ihre eigenen Worte | *“...the sunset when I told you I hadn't written my own caption since I was nineteen...”* |
| Bibi | **Expedition** „Mochi“ (nur `kl_loewe_frei` und offene Station): Mochi in der Macchia einfangen (Kanon E-106), Rastplatz am Feuer. *Last Page* bleibt an Tag 35 | das Field Book bekommt Ducs Seite | *“...the night you said 'until every collar is off', at the campfire with the three of us...”* |
| Megan | nur `megan_funke`: „Off the Record“: VIP-Kabine (W1 A: nach dem Heben), Outfit `megan_morning_after` am Morgen danach | nie öffentlich (E-060) | *“...the night you called me Mac in the press release week...”* |

**Danzel als Rivale** (Kanon, `danzel.md`): Liegt Ducs Begehren bei Rosi oder Lola höchstens bei 3, schwärmt Danzel in ihrer Szene schüchtern dazwischen, eine Zeile, nie übergriffig.
**Holm und Petru** (Kanon): freie Abend-Szene `a3_holm_petru` ab Tag 30, beide ab Vertrauen 3. Ingrid ruft dabei an (Kanon, `holm.md`), sie ist Mutter geworden: Holm: *“Ingrid. From the night before Bergen. She has a daughter.”* · Petru: *“Hm. Good.”* Duc kann still weitergehen (*When you look back, the metre between them is gone.*) oder stören (*“Frankfurt. Go away.”* · Petru: *“Hm. Go away.”*).
**Ligeia:** keine Romanze. Mit `sirene_frei` kommt eine Flaschenpost (Kanon E-117) an Tag 30: *“Sailor. They say the bay will be safe. I would like to sing at something that isn't a shipwreck.”* In den Enden mit geschützter Bucht steht die Galionsfigur am Eingang (Kanon).

Der Anteil „frech“ steigt so auf rund 20 % (Festa-Frage, Expeditionen, Megan).

## 7. Die Enden lesen den Akt

Die Säulen werden am Spielende umgebaut (Duc 01.11.). Bis dahin (Vorschlag, Zahlen Entwurf):

| Säule | Akt 3 zahlt ein über | Erfüllt, wenn |
|---|---|---|
| **Wahrheit** | Whites Einsatzplan, Kassenbuch „alles“, Siris Post, Sophias Notizen, Funk-Aufnahme und Mitschrift, Funkbuch, Nachtwache, Kiste (`alon_kiste_genutzt`), `mo_kommission` (`beweis_stand`), Adriens Fotos, Steuerchip, Red-Trio-Aussagen | 3 Beweise, oder 2 mit Kassenbuch „alles“ |
| **Geld** | Margot geborgen (Kanon: ohne sie ist die Säule hin) und `a3_megan_wende` oder Yamamoto Bindung 5 | Margot und eins der beiden |
| **Gemeinschaft** | Zeugen, Kassenbuch „teil“, Baustellen fertig, Casanova Vertrauen, Ruf ab 5 als Bonus (der Ruf wird hier nur gelesen) | 5 Zeugen, oder 4 mit Kassenbuch „teil“ |
| **Stärke** | Endkampf gewonnen oder Festnahme | `a3_alon_besiegt` oder `a3_alon_festgenommen` |

**Megans Wende (Monaco)** braucht 4 Zeugen **oder** 2 Beweise bis Tag 31. So hängt sie an Ducs Arbeit, nicht an der Säule, die sie trägt.

**Sichtbar im Schlussbild:** Ausstattung der Festa (Tafel), wer im Netz fehlt (Zeugen; Minicu schreibt seinen Namen selbst, schief, neben Pascals leerem Knoten, den Don wortlos knotet; mit `bl_blatt_gefunden` gibt Duc ihm vorher das Namensblatt zurück), wer an Ducs Tisch sitzt (5.22). Die Enden-Tabelle in `enden.md` bleibt. Buenaventura (Kanon): Eco Tours nur bei freier Bucht, sonst „Pirate Experience“.

## 8. Wirkpunkte der Belagerungs-Flags

Alle Flags aus `akt3_folgen_belagerung.md`, die nach Tag 23 niemand liest, und wo sie in v2 wirken. (Drei davon wirken seit `fix-akt2-folgen` auch schon in Akt 2.)

| Flag | Wirkt in v2 | Wie |
|---|---|---|
| `bl_tafel` | 5.6 | Megan sieht ihre alte Kriegstafel: *“My list. Six jobs. You did {n} of them.”* |
| `bl_verband_wolff` | 4.1 | Die Legion trägt einen Tag an einer Baustelle (+1 Stufe) |
| `bl_verband_chiara` / `_maxwell` / `_duc` | 6, 5.16 | Chiara: ihre Schluss-Szene ab Tag 24 statt 25 · Maxwell zeigt am Kai den Verband: *“Mr. Maximum kept it. Mr. Maximum keeps everything.”* · Duc: Lola: *“You kept it for yourself? Good. Somebody on this boat has sense.”* |
| `bl_funk_white`, `bl_funk_charly` | 5.27, Charly | Aufnahme und Mitschrift als Beweis · Charly: *“Twenty-one forty. He said 'tonight'. Seven out of ten for clarity.”* · Grund für Rosi, ihr eine Stelle anzubieten (E-098) |
| `bl_tueren_petru` | 4.2, 5.27 | Petrus Tür ohne Mindestvertrauen, er bringt einen zweiten Namen mit (ein namenloser Fischer, Legenden-Kommentar) |
| `bl_tueren_lola` | 4.3 | *The Menu*: Lola kennt jede Küche. *“I've been in every kitchen in this village, Boss. Every single one. Mostly the biscuits.”* Der Auftrag wird eine Entscheidung kürzer |
| `bl_tueren_mina` | 5.5 | Mina beim Korb: *“You let me go alone that night, when the phones were dead. I knocked on every door. I can do this too.”* Ihre Tür öffnet ohne Post |
| `bl_batu_norden` | 4.2, 5.27 | Bà Tưs Tür offen, ihre Aussage nimmt „twice“ auf |
| `bl_nachtwache_wolff` / `_elsa` / `_yamamoto` | 5.27, 5.26 | Zeuge des Funkspruchs um drei, im Ton der Person · steht im Hof der Villa und sagt einen Satz zu Pascal |
| `bl_nachtwache_niemand` | 5.13 | Holms Nachsatz bei der Revanche |
| `bl_wache_gesehen` | 5.10 | Funkbuch in der Schublade wird Beweis |
| `bl_kirche_jana` | 4.3 | Auftrag Kinderbilder |
| `bl_kirche_don` | 4.3, 5.27 | *The Bell* mit einem Abend · Dons ehrliche Zeile „I was sober“ |
| `bl_kirche_casanova` | 5.29 | Die Kinder wollen ihre lange Geschichte hören: Casanovas Rede bekommt nach Alvas Applaus einen zweiten, kleinen Teil |
| `bl_will_ab_<pid>`, `bl_ab_fertig_<pid>` | 6 | Rückbezug am Anfang der Schluss-Szene |
| `bl_will_ab_niemand`, `bl_will_na_niemand` | 5.1 | Holm, eine Zeile: *“You slept, both nights. Good. Now you can work.”* |
| `bl_will_na_<pid>`, `bl_na_fertig_<pid>` | 5.22, 6 | erste in der Festa-Frage · Status „zusammen“ |
| `bl_alva_runde` | 4.1, 6 | Zweite Zeile auf Papas Tafel nach dem Wiederaufbau: *“Everyone. Paid. D.”* · Alvas Rückbezug in ihrer Schluss-Szene |
| `bl_minicu_duc_zuerst` | 5.4 | *“You came first. Before Pascal. I heard you.”* (gilt in W2 A und B) |
| `bl_minicu_sag_es` | 5.9 | ein Satz mehr in Pascals Brief |
| `bl_minicu_gewartet` | – | bewusst ohne Wirkpunkt, Warten war in Ordnung |
| `bl_blatt_gefunden` | 5.21, 7 | Handschrift auf dem Umschlag, Namensblatt zurück an Minicu |
| `bl_werkstatt_heil` | 4.1, 4.3 | keine Baustelle, *The Catch* ab Tag 24 |
| `sophia_notizen` | 5.27 | Beweis |
| `siri_wartet` | 5.12 | Siris Post wartet auf Minicu |
| Rettungen (`haeuser[*].status`), `tk_haus_geflickt_` | 4.1 | Dank-Szene je gerettetem Haus, geflickt startet Stufe 1 |
| Rudern (`dorf_rudert`) | 5.27, 5.29 | **neues Flag** `bl_dorf_rudert` am Ende von Welle 4 (Bau): Petrus Zusatz bei der Kommission, die Boote von 1924 geschmückt im Hafen |
| `tk_yacht_weg` | W1 | beide Zweige |

## 9. Gags, Ton, Englisch

- **Gags** bis Tag 31 (`wann.akt2` auf `[8, 31]`), vorher Texte prüfen, die Alon, Holm, die Festa, „tomorrow“, Megan an Bord, Pascal, Maxwell (Tag 30 bis 32 weg) oder die Yacht (W1) voraussetzen. Ab Tag 32 gagfrei.
- **Ereignis-Dichte:** Der Faktor 0,45 aus Akt 2 (`kern/ereignisse.AKT2_FAKTOR`) gilt ohne Ende auch in Akt 3. Vorschlag: In Woche 4 auf 0,6 (Durchatmen heißt mehr kleine Momente), in Woche 5 bei 0,45 lassen. Fragenliste F-17.
- **Ton-Mischung (Ziel):** 35 % warm, 25 % komisch, 20 % ernst, 20 % frech.
- **Englisch** nach dem Text-Audit: Rückbezüge tragen die Erinnerung im Satz, Chips mit Rückbezug immer im Chip selbst, keine seltenen Wörter ohne Not (in v2 ersetzt: *phones home, dividend, in breach of service agreement, the one who knocks, no warrant*). Seemannswörter einmal erklärt (Audit, Muster 3). Erzähltext im Präsens.

## 10. Brain Trust zu v2

**Sienna (Game Direction):** Die Kette Baustelle, Dank-Szene, Aussage ist jetzt ohne Reibung: Wer ein Haus fertig hat, fragt den Besitzer in derselben Szene. Das ist Stardew mit Mass-Effect-Folgen. ✨ Gegenvorbild bleibt Mass Effect 3 (Zahlen, die niemand fühlt). Darum sitzt jeder Schweigende sichtbar am Kai.

**Aly (Tech):** Gebaute Haken passen jetzt: `mo_kommission` ist ein Beat, `alon_kiste_genutzt` fällt in Totòs Frist, Akt 3 startet im Code an Tag 24 (E-121). 🤓 Einwand: 33 freie Phasen sind von Hand gerechnet. Ich will einen Bot-Lauf, sobald der Kalender steht, mit zwei Profilen (eine Romanze, alle Zeugen). Gegenvorschlag bis dahin: Zeugen in Dank-Szenen ohne Phase, das spart vier.

**Luise (Art & Story):** Der leere Haken in Pascals Zimmer und der tropfende Eimer sind die zwei stillen Bilder des Akts, und Minicus zu lautes Klatschen an Tag 26 ist das warme. 🥹 Kritik: Chiaras „Blackout“ ist eine Deutung. Wenn der Kanon etwas anderes meint, verliert sie ihre stärkste Szene. Gegenvorschlag: Duc fragt Character Design, bevor sie gebaut wird.

**Maelle (Producerin):** Preis: rund 36 Szenen, grob 650 Sprechzeilen, 8 Hintergründe, 10 Sprite-Wünsche, drei kleine Mechaniken. Das sind fünf bis sechs Bau-Sitzungen. 📋 Kritik: Woche 5 hat an Tag 34 und 35 neun Pflicht-Events am Stück. Das ist gewollt (das Finale zieht an), aber der Nachmittag von Tag 34 muss frei bleiben. Meine Frage an dich, Duc: Bauen wir zuerst Woche 4 mit Baustellen und Zeugen, spielst du sie, und erst dann Woche 5?

**Sora (Spielerstimme / QA):** Minute 1: Petru tritt vor, ich habe Gänsehaut. Minute 30: Ich trage Steine mit einem Piraten, der seine Fackel nicht hergeben will. 😂 Minute 90: Alva trägt Sandru die Treppe hoch. 😭 Nochmal-Lust 5: Die Festa-Tafel ist jetzt eine Reihe kleiner Dates mit dem Dorf, und die Lichter leuchten bernstein, wenn ich Alons Teile nehme. Das will ich beim zweiten Mal anders sehen. 🔥 Veto bleibt bereit für jeden Auftrag, der wieder zur Mengenliste wird.

## 11. Bauplan (nach Ducs Ja)

| Paket | Inhalt | Dateien |
|---|---|---|
| A · Kalender | Akt-3-Kalender bis Tag 35, `zeitraster`, Gags bis 31, Dichte je Woche, `bl_dorf_rudert` | `modul_eden_rise.py`, `ereignisse_basis.py`, `kern/taktik.py`, `kern/abschluss.py` (Beta-Schluss nach `akt2_ende` aufheben) |
| B · Woche 4 | 5.1 bis 5.13, Baustellen-Karte mit Wahl, Dank-Szenen | `ereignisse_akt3_woche4.py`, `kern/aufbau.py` |
| C · Zeugen und Tafel | Liste, Türen, Haltungen, acht Auftrags-Szenen | `ereignisse_akt3_zeugen.py`, `ereignisse_akt3_festa.py`, `kern/zeugen.py`, `kern/festa.py` |
| D · Woche 5 | 5.14 bis 5.26, Villa als Frame-Kette, Endkampf | `ereignisse_akt3_woche5.py`, `ereignisse_akt3_villa.py` |
| E · Romanzen | Abschnitt 6, zwei Expeditionen | `ereignisse_akt3_romanzen.py` |
| F · Kommission, Festa, Enden | 5.27 bis 5.29 mit `mo_kommission`, Säulen | `ereignisse_akt3_finale.py` |
| G · Stimme, Tests | `stimme_tags.json`, `test_akt3_kalender`, `test_zeugen`, `test_festa_tafel`, `test_akt3_events`, Bot-Lauf | `module/eden_rise/`, `tests/` |

## 12. Was aus jedem Befund wurde

### Gegenrede (G1 bis G19)

| # | Befund | Ergebnis in v2 |
|---|---|---|
| G1 | Sonnenbrille dreimal ab | **eingearbeitet:** keine Zeile nimmt sie ab (0, 5.1, 5.6, 5.25) |
| G2 | Rädchen privat statt Stream | **eingearbeitet:** Dinner privat, danach Pressemoment mit Drohnenkamera (5.26) |
| G3 | Kommission gegen `mo_kommission` | **eingearbeitet:** Kai, zwei Männer und ein Schreiber, `mo_kommission` als Beat (5.27) |
| G4 | Woche 4 voller als Woche 5 | **eingearbeitet:** 8 gegen 16 Pflicht, Tag 27 frei, Uhr und Briefe zusammen, Messe und Schublade zusammen |
| G5 | Zeitbudget falsch | **eingearbeitet:** nur vier Kartenphasen gezählt, 33 frei, Bedarf 20 bis 31. **Nicht eingearbeitet:** Bot-Lauf, weil der Kalender noch nicht gebaut ist (Bauplan G) |
| G6 | Wochentage | **eingearbeitet:** Tag 24 Mittwoch, 28 und 35 Sonntag |
| G7 | Petru „am Tor“ | **eingearbeitet:** *“I rowed out with Mina...”* (5.1) |
| G8 | Alva drei Tage, zweimal „erstes Mal“ | **eingearbeitet:** „since last night“, wacht bei Bà Tư auf, betritt das Haus ihrer Mutter erst in 5.19 |
| G9 | Zeugen-Chips als Rätsel | **eingearbeitet:** jede Haltung überzeugt, sie färbt nur die Aussage (4.2) |
| G10 | Tafel als Einkaufsliste, Post wirkungslos | **eingearbeitet:** acht Szenen mit Entscheidung (4.3), Post bringt Zugang aus Bastia (4.1) |
| G11 | Akt-2-Flags ungenutzt | **eingearbeitet:** Abschnitt 8, jedes Flag mit Wirkpunkt |
| G12 | Romanzen fehlen | **eingearbeitet:** Abschnitt 6 |
| G13 | drei schwere Gipfel | **eingearbeitet:** nur Switched Off schwer, Schublade Spannung 4 |
| G14 | Doppelungen (Applaus, Don) | **eingearbeitet:** Minicu klatscht an Tag 26, *The Bell* mit Plan, Kaffee mit Erinnerung, Dons Epilog-Pointe nicht vorweggenommen |
| G15 | kleine Kanon- und Logikbrüche | **eingearbeitet:** Lea oder Sophia; „on Sunday“ statt „tomorrow“; Nonna nach Don; Elsa nicht bei der Planung, Festnahme draußen; Casanova bleibt an der Kellertür; Schiene mit Maxwell; Don ohne Flag ehrlich |
| G16 | Siris Post fehlt | **eingearbeitet:** 5.12, mit Yasins Angebot |
| G17 | Säule Geld zirkulär | **eingearbeitet:** Megan braucht Zeugen oder Beweise, CEO will Duc sprechen (5.18) |
| G18 | schwieriges Englisch | **eingearbeitet:** ersetzt (Abschnitt 9), Präsens |
| G19 | Chips ohne Frage | **eingearbeitet:** jede Wahl hat eine Frage davor (5.14, 5.23, 5.28) |

### Fragen aus der Gegenrede

| Frage | Ergebnis |
|---|---|
| Was wusste Duc über den Verkauf? | **entschieden im Drehbuch nach Kanon:** nichts, eine feste Fassung (Abschnitt 2) |
| Petrus Platz an Tag 23 | **nach Kanon:** auf dem Wasser, nicht am Tor |
| Ort der Kommission | **nach dem gebauten Event:** Kai |
| Stream oder privat | beides, nacheinander (5.26) |
| `megan_funke_3`, `sandru_herkunft` | `megan_funke_3` ersetzt durch `megan_funke` und eine gemeinsame Nacht; `sandru_herkunft` bleibt Bedingung, ist aber noch nicht gebaut (Fragenliste) |
| Alvas Aussage und Pascal | eingehalten (5.27, Hinweis) |
| Yacht von Tag 0 bei der Kommission | ausgeschlossen (5.27) |

### Weitere Befunde des Prüfers zu v1, die nicht in G1 bis G19 standen

| Befund | Ergebnis |
|---|---|
| Totòs Versprechen `alon_kiste_genutzt` | eingearbeitet (5.5, 5.27) |
| Totòs Akt-3-Geheimnis | **nicht eingearbeitet:** gehört der Story-Sitzung und steht in `story.json`, die diese Sitzung nicht öffnet. Anschlussstelle in der Fragenliste |
| Maxwells Flug, Ingrid, Buenaventuras Fernseh-Moment und Festa-Lieferung | eingearbeitet (5.16, 6, 5.2, 4.3) |
| Rosi und Lot 14 | eingearbeitet (5.17) |
| Riscossore kennt den Grottenkampf | eingearbeitet, zwei Fassungen (5.15) |
| Alon weiß vom Keller | eingearbeitet (5.25) |
| Festa-Fülle gegen Ende 2a | eingearbeitet: Tafel = Ausstattung, Ende = wer bleibt (4.3, 5.29) |
| leerer Fedora-Haken, Kinder an der Haltestelle | eingearbeitet (5.10) |
| Gags am Tag von Switched Off | eingearbeitet: Switched Off auf Tag 32 |
| „Brain-Trust-Runde zu zahm“ | eingearbeitet: Abschnitt 10 mit Preis, Einwand und offener Frage |
