# Drehbuch Akt 3: „Who Saw It?“ · Tag 24 bis Tag 35 · Version 2.1

> Stand 04.11.2026 · Besitz: Brain Trust (Cloud-Sitzung, Branch `akt3-cloud`) · **Entwurf zur Abnahme durch Duc, nichts davon ist gebaut.**
> Version 2 ersetzt Version 1 (`506dce2`). Version 2.1 arbeitet zusätzlich die unabhängige Prüfung von v2 ein (Abschnitt 12b).
> Eingearbeitet: Gegenrede (`docs/uebergabe/drehbuch_gegenrede.md`, Branch `drehbuch-gegenrede`), Wiki gegen Code (`docs/berichte/wiki_vs_code.md`, Branch `wiki-vs-code`),
> Folgen der Belagerung (`docs/wiki/welt/akt3_folgen_belagerung.md`, Branch `folgen-belagerung`), Text-Audit (`docs/uebergabe/audit_text.md`, Branch `audit-text`).
> Code-Stand: Akt 3 ab Tag 24 und die drei Belagerungs-Aufträge sind auf Branch `fix-akt2-folgen` gebaut (E-121), **noch nicht auf `akt3-cloud` und nicht auf `master`**.
> Was Kanon berührt, steht als E-120 „offen“ im Register. Spieltext Englisch, einfach, vertonbar, Erzähltext im Präsens. Turbo-Tags: siehe Abschnitt 9.

## 0. Feste Vorgaben

| Vorgabe | Wie diese Fassung sie einhält |
|---|---|
| Akt 3 = Tag 24 bis 35 (E-114) | Kalender ab Tag 24. Im Code: `sperre.bis = 23`, Schneider, Lesung, Holms Revanche (`HOLM_TAG = 24`), Expedition Pack ab Tag 24 (Branch `fix-akt2-folgen`) |
| Duc trägt **immer** die Sonnenbrille | Keine Zeile, kein Chip nimmt sie ab. Nähe zeigt er über Haltung: setzt sich, stellt etwas ab, bleibt stehen |
| Kommission passt zu `mo_kommission` | Tag 35, Phase „tag“, Kai, Klapptisch, zwei Männer aus Ajaccio, ein Schreiber, Elsa legt vor. `mo_kommission` eröffnet die Kette, wenn es läuft (5.26) |
| Woche 4 atmet | Woche 4: **6** Pflicht-Events, Tag 27 ganz frei, je Tag im Schnitt 3,4 freie Phasen. Woche 5: **16**, je Tag 2,8 |
| Festa-Aufträge sind Spiel | acht kurze Szenen mit einer Entscheidung und wenig Material (4.3) |
| Romanzen fertig spielen | Abschnitt 6, je Frau eine Schluss-Szene mit Beat-Tabelle |
| Ungelesene `bl_`-Flags | jedes mit Wirkpunkt in seiner Szene (Abschnitt 8 ist das Register dazu) |
| Romanzen bleiben privat (E-060) | Festa-Begleitung ist ein privater Moment an der Mole, nicht vor dem Dorf (5.21) |
| Offene Entscheidungen | Weichen mit allen Zweigen (Abschnitt 1) |

## 1. Die Weichen (Duc entscheidet, das Drehbuch trägt alle Zweige)

| Weiche | Zweige | Wo es wirkt |
|---|---|---|
| **W1 · Die Yacht** | **Hält** (der häufigste Fall, Yacht-Leben über 0): alles an Bord wie gewohnt. · **Auf Grund gesetzt** (Vorschlag Drehbuch Finale): fünfte Baustelle `yacht`, Crew schläft bei den Familien, VIP-Kabine erst nach dem Heben. · **Gesunken** (heutiger Code bei `tk_yacht_weg`): keine Baustelle, die Crew bleibt im Dorf bis zum Ende | Jeder Ort an Bord hat dieselbe **Ersatzreihe: Kirche, dann Piazza, dann Kai** (die Kirche brennt nie). In den Szenen steht „Bord (Ersatzreihe)“ |
| **W2 · Minicus Überleben** | **A:** Der Bericht an Tag 23 lässt es offen, am Morgen von Tag 24 steht er am Tor (Vorschlag). · **B:** Der Bericht sagt es schon, Tag 24 zeigt ihn ohne Enthüllung. Kanon: er lebt (`drehbuch_finale.md`, Abschnitt 9) | 5.1, 5.12 |
| **W3 · Festa-Flag** (`akt3_festa`) | **A · die gebauten Events laufen:** Dafür muss `ereignisse_basis.py` beim Festa-Schalter **Tag, Phase und Ort mitsetzen** (heute steht in allen drei `tage: [21, 21]`, `br_ehrenbuerger` spielt nachts in `crew_mess`). Neu: Fenster (35, 35), Phase Abend, Ort `village_piazza`. Das berührt „Festa-Events nicht anfassen“ (`dorf_figuren.md`), Fragenliste F-22. · **B · neu geschrieben:** `a3_festa` übernimmt die drei Szenen als Beats, `akt3_festa` bleibt nur der Schalter | 5.28 |
| **W4 · Wie schwer 100 % ist** | Definition steht (E-121: 100 % = der Spieler hat nichts getan). **A:** Balancing wie heute (Anfänger verlieren in Welle 3 rund 3 von 4 Häusern). **B:** 100 % wird härter (mehr verlorene Häuser, öfter `tk_yacht_weg`) | Akt 3 liest nur das Ergebnis: 0 bis 4 Baustellen plus W1. Jede Szene funktioniert mit 0 und mit 4 abgebrannten Häusern |
| **W5 · Sandrus Schiene** (Kanon-Widerspruch) | `dorf_figuren.md`, Ernste Events 5 (30.10.): Alon schaltet die Beine in Akt 3 ab, danach baut Rosi die Schiene. `dorf_figuren.md`, „Rosis Schiene“ (01.11.): Mit Rosis Schiene hebt Sandru schon an Tag 21 die Trümmer, abgeschaltet wird nur ohne Rosi. **A (Vorschlag):** Switched Off kommt immer, die Schiene danach (die Fassung mit den ausgearbeiteten Zeilen). **B:** Wer Sandru in Akt 2 zu Rosi gebracht hat, trägt Rosis Schiene schon (eine neue Akt-2-Szene wäre nötig). Dann trifft Alon nicht die Beine, sondern **die Arbeit**: Er schließt den A.V. Market, zwölf Leute im Dorf verlieren ihre Stelle, Sandru steht auf eigenen Beinen vor dem dunklen Laden (Alons Drohung mit Jobs, Kanon `akt3.md`). Fragenliste F-24 | 5.18, 5.19 |

## 2. Die Idee in einem Satz

Zwölf Tage lang baut Duc ein Dorf wieder auf, das ihn am ersten Morgen nicht mehr ansehen will, und am Ende zählt nicht, wie stark er ist, sondern wer bereit ist, laut zu sagen, was er gesehen hat.

**Das Motiv:** *Who saw it?* Akt 2 fragte, wer die Linie hält. Akt 3 fragt, wer es gesehen hat und es sagt. Alon droht nicht mit Gewalt, sondern mit Papier: Jobs, Kredite, Anwaltsbriefe. Gegen Papier hilft nur ein Name, laut gesagt. Das Fischernetz am Ende ist die Liste dieser Namen.

**Was Duc weiß (eine Fassung):** Ducs Firma gehört zur Eden Group. Dass die Gruppe das Hafenviertel heimlich verkauft hat und an wen, wusste er nicht (E-001, E-003). Kern seines Satzes: *“My company belongs to the Eden Group. I didn't know they sold your harbour, or who bought it.”* Seine ESG-Arbeit hat mit dem Resort nichts zu tun.

**Zeugen sagen nur, was sie selbst gesehen haben.** Wer bezahlt hat, belegen das Kassenbuch, Riscossores Buch und Buenaventura.

| Wer | Was er gesehen hat | Was ihn schweigen lässt | Seine Tür (4.2) |
|---|---|---|---|
| Petru | die Fackeln an seiner Werkstatt, mit Rudern auch die Boote | A.V. hat den Kredit auf sein Boot gekauft | Dank-Szene der Werkstatt |
| Mina | jede Tür in der Nacht der Türen | sie stellt die Drohbriefe selbst zu | Dank-Szene der Post, oder `bl_tueren_mina` |
| Bà Tư | die Männer in Weiß, die zweimal nach dem Nordweg fragten | Alons Arbeiter sind ihre Kunden | `bl_batu_norden`, oder Dank-Szene des Ladens |
| Alva | die offene Nordbarrikade, die Männer in Weiß | sie war bewusstlos, man glaubt ihr nicht | Dank-Szene der Bar |
| Sandru | wer Alva aus den Trümmern trug | seine Beine (W5 A) oder seine Stelle (W5 B) gehören A.V. | Schiene (5.19) oder W5 B nach 5.18 |
| Don Anghjulu | das offene Tor | das Kirchendach, das Beichtgeheimnis | an seiner Seite an der Tür, **oder** Vertrauen 3, **oder** *The Bell* begonnen |
| Minicu | White, ein Schlag | niemand will ihn vor Fremden reden lassen | nach Hause geschickt (5.4) |
| Casanova | das Papier, das jede Nacht auf den Stufen lag | ihre Schuld am Elternhaus | Elsas Berichte gehört (5.11) |
| Buenaventura | wer ihn bezahlt hat | **nichts**, ihm glaubt nur keiner | meldet sich selbst (5.2) |

## 3. Kalender und Bogen

**Wochentage:** Tag 14 war Sonntag, also sind 21, 28 und 35 Sonntage, Tag 24 ist ein Mittwoch.
**Phasen:** Karten (echte Zeit) gibt es in **Tag, Nachmittag, Dinner, Abend**. Frühstück und Nacht zählen nicht als freie Kartenphasen.

### Woche 4 · „The Morning After“ (Mi 24 bis So 28)

| Tag | Frühstück | Tag | Nachmittag | Dinner | Abend | Pflicht | frei |
|---|---|---|---|---|---|---|---|
| **24** Mi | `a3_morgen` | `a3_schwur` | frei | frei | frei | 2 | 3 |
| **25** Do | `a3_uhr` (mit den Briefen) | frei | frei | `a3_megan_landet` | frei | 2 | 3 |
| **26** Fr | `a3_festa_tafel` | frei | frei | frei | frei | 1 | 4 |
| **27** Sa | Vignette | frei | frei | frei | frei | **0** | 4 |
| **28** So | Vignette | `a3_sonntag` (Messe, Don an der Tür, Schublade) | frei | frei | frei | 1 | 3 |

**Woche 4: 6 Pflicht, 17 freie Phasen.** Ton: 5.1 ernst zu warm, 5.2 komisch, 5.5 trocken, 5.6 Megan-Theater, 5.7 komisch, 5.10 ernst. Dazu morgens an Tag 25 bis 28 je eine **Vignette** (kurz, warm oder komisch, keine Pflicht-Phase): die Dank-Szenen der Häuser, die nicht abgebrannt sind (4.1), oder ein Gag aus dem Dorf.
Angeboten mit Erinnerung, keine Pflicht: Alva besuchen (5.3), Minicu (5.4), Holms Revanche (5.13), Siris Post (5.12, ab Tag 24 Abend), Nonnas Kiste (5.9, ab Tag 28 Nachmittag), Baustellen, Festa-Aufträge, Mochi.

### Woche 5 · „Name Your Price“ (Mo 29 bis So 35)

| Tag | Frühstück | Tag | Nachmittag | Dinner | Abend | Pflicht | frei |
|---|---|---|---|---|---|---|---|
| **29** Mo | `a3_idee` | frei | frei | frei | `a3_berichte` | 2 | 3 |
| **30** Di | `a3_maxwell_flug` | frei | frei | frei | frei | 1 | 4 |
| **31** Mi | frei | frei | frei | `a3_megan_monaco` | frei | 1 | 3 |
| **32** Do | frei | frei | `a3_switched_off` | frei | frei (Maxwell zurück) | 1 | 3 |
| **33** Fr | `a3_einladung` (+ `a3_schiene`, wenn möglich) | frei | frei | frei | `a3_festa_frage` | 2 (3) | 3 |
| **34** Sa | `a3_villa_plan` | `a3_villa_keller` | frei | `a3_villa_dinner` | `a3_villa_ende` | 4 | 1 |
| **35** So | frei | `a3_kommission` (mit `mo_kommission`) | `mo_frei_start`, danach *Last Page* (Bibi, wenn) | frei | `a3_festa` | 5 (mit Ende) | – |
| 35 Nacht | Ende, Epilog | | | | | | |

**Woche 5: 16 Pflicht** (17 mit Schiene), **17 freie Phasen** (Tag 29 bis 34). Gags bis Tag 31, ab Tag 32 gagfrei: **Switched Off liegt auf Tag 32.**

### Spannungsbogen

| Tag | Szene | Spannung |
|---|---|---|
| 24 | Der Morgen danach, der Schwur | 6 → 3 |
| 25 | Die Uhr, Megan | 5 |
| 26 | Die Tafel | 2 |
| 27 | frei | 1 |
| 28 | Sonntag: Messe, Don, Schublade | 4, ein leiser Fund |
| 29 | Die Idee, Elsas Berichte | 3 |
| 30 | Maxwell fliegt | 3 |
| 31 | Monaco | 6 |
| 32 | **Switched Off** | 8 → 4, der eine schwere Moment |
| 33 | Einladung, Festa-Frage | 6 |
| 34 | **Villa** | 9 → 10, Spannung und Aktion, keine Trauer |
| 35 | Kommission, Festa | 7, dann 10 → 2 |

### Zeitbudget (von Hand, Bot-Lauf erst nach dem Bau)

Freie Kartenphasen Tag 24 bis 34: **34**.

| Bedarf | Phasen | |
|---|---|---|
| Baustellen | 2 bis 4 | Duc setzt je Haus den ersten Stein, die Piraten tragen dann weiter (4.1) |
| Zeugen | 3 bis 4 | vier fragt Duc in Dank-Szenen ohne Phase, je eine Phase Sandru (nur W5 B), Don, Minicu, Casanova |
| Festa-Aufträge | 8 bis 9 | acht Szenen, *The Bell* zwei Abende (mit `bl_kirche_don` einer) |
| Romanzen | 2 bis 6 | je Frau eine Szene, die beiden Expeditionen (Lea, Bibi) kosten 2 |
| Freie Dates | 2 bis 4 | |
| Kleine Szenen | 6 bis 10 | Alva 1, Minicu 1 bis 2, Siri 1, Revanche 1, Riscossore 1, Lot 14 1, Nonna 1, Mochi 1 bis 2, Scrap Field 2 |
| **Summe** | **23 bis 37 von 34** | Wer alles will, schafft es nicht. Ein Spieler mit einer Romanze und allen Zeugen braucht etwa 27 bis 30. Vor dem Bau von Woche 5: Bot-Lauf mit zwei Profilen (Bauplan G) |

## 4. Die drei Mechaniken

### 4.1 Die Baustellen („Lend a Hand“)

**Vorbild:** Stardew Valley, Gemeinschaftshaus. **Gegenvorbild:** Anno-Verwaltung ohne Menschen.

- **Fundament (gebaut):** `kern/aufbau.py`, drei Stufen je abgebranntem Haus, geflickt (`tk_haus_geflickt_<id>`) beginnt bei Stufe 1.
- **Neu, Duc entscheidet, wo gebaut wird:** Die Piraten tragen je Tag eine Stufe (gebaut), aber **nur an Häusern, an denen Duc den ersten Stein gesetzt hat** (eine „Lend a Hand“-Karte je Haus). Heute bauen sie automatisch an der am weitesten fortgeschrittenen Baustelle (`kern/aufbau.tag_vorbei`), das ändert Paket B. So zählt Woche 4 für Woche 5: Wessen Haus Duc anfängt, dessen Tür geht zuerst auf.
- **Karte „Lend a Hand“** (1 Phase): eine Stufe mit eigenem Material. Jede Stufe hat eine Wahl: **Wer hält mit?** Der Besitzer (eine Zeile über sein Haus), ein Pirat (eine Zeile über das, was er angezündet hat), ein Crew-Mitglied (zählt als Zeit zusammen).
- **Minicu** trägt nach `a3_minicu_heim` jeden dritten Tag eine Stufe. **Die Legion** mit `bl_verband_wolff` einen Tag lang eine Stufe (Wolff: *“You gave me the bandage, the one good one. The Legion pays its debts.”*).
- **Fertig** (`aufbau_fertig_<id>`) → **Dank-Szene** `a3_dank_<id>`. **Dort öffnet die Zeugen-Tür.** Ist die Zeugenliste schon offen (ab Tag 25), fragt Duc in derselben Szene, ohne eigene Phase:

| Haus | Dank-Szene | Wirkpunkt |
|---|---|---|
| Post | Mina hupt zweimal vor dem Kai. Die erste Post nach dem Brand ist keine Rechnung | Mina bringt einmal am Tag eine Zutat oder ein Baumaterial aus Bastia mit, das es im Dorf nicht gibt (Wahl aus drei, ohne Phase) |
| Bà Tưs Laden | zwei Teller, diesmal auch einer für Lola | Kochen mit Bà Tư (★★), ihr Thịt kho, Akzent „Ăn đi“ (+10 % Leben bis zum Dinner des Folgetags) |
| Alvas Bar | Alva schreibt den ersten neuen Namen auf Papas Tafel. Mit `bl_alva_runde` darunter: *“Everyone. Paid. D.”* | Bar-Abende, Alvas Festa-Auftrag |
| Petrus Werkstatt | Petru hängt das Ruder zurück über die Tür, heil oder verkohlt | Angeln vom Boot, *The Catch* öffnet |

- **Nicht abgebrannt (W4):** Die Dank-Szene kommt als Frühstücks-Vignette an Tag 25 bis 28, je eine (nie mehrere an einem Tag), kurz und warm, **ohne Frage**. Die Zeugenfrage stellt Duc dann über die Karte „Ask <Name>“ (ohne Mindestbedingung, die Tür ist offen).
- **Die Kirche** ist keine Baustelle. Das Dach war Alons Geld, es tropft bis zum Ende, nur Ende 3 und ★ reparieren es (E-096).
- **W1 auf Grund:** Baustelle `yacht` (6 Timber, 4 Iron, 2 Steel). Rosi: *“She floats. She's ugly, she leaks a bit, and she floats. Don't tell her I said ugly.”*

### 4.2 Die Zeugen („Who Saw It?“)

**Vorbild:** Mass Effect 2, Persona 5. **Gegenvorbild:** L.A. Noire. **Kein Rätselchip.**

- **Auslöser:** `a3_uhr` (Tag 25). Codex-Seite „Witnesses“: Bild, Angst, Tür als Satz (*“Not while her bar is a building site.”*).
- **Das Gespräch** stellt eine klare Frage. **Jede der drei Haltungen überzeugt**, sie färbt nur die Aussage vor der Kommission und gibt Vertrauen (+2, die zur Figur passende +6). **Eine Tür ist nie mit einem einzigen Chip für immer zu:** Wer in 5.8 unten bleibt, öffnet Dons Tür später über Vertrauen 3 oder *The Bell*. Wer bei Minicu sitzt und wartet, bekommt die Karte am nächsten Tag wieder.
- **Ein Zeuge schweigt nur**, wenn seine Tür bis Tag 34 zu bleibt. Dann sitzt er am Kai am Rand, ohne Zeile, und sein Name fehlt im Netz.
- **Ergebnis:** `a3_zeuge_<id>`, Haltung `a3_zeuge_<id>_<h>`. Zählt auf Gemeinschaft und auf Monaco (5.17).
- **Pascal** steht nie auf der Liste und in keinem Fall. Am Rand der Liste eine durchgestrichene Zeile. Elsa sagt nichts dazu.

### 4.3 Casanovas Tafel („THIS. IS. THE. FESTA!“)

**Vorbild:** Stardew Valley, Spiritfarer. **Gegenvorbild:** Survival-Einkaufslisten.

- **Auslöser:** `a3_festa_tafel` (Tag 26). Acht Aufträge, **jeder eine Szene** (1 Phase) mit einer Entscheidung. Gekauft zählt nicht: *“From the shop? Monsieur. This is a festa, not a supermarket.”*
- **Wirkung:** `a3_festa_<id>` stellt etwas ins Schlussbild, die Entscheidung bestimmt, **wie** es aussieht. Die Tafel bestimmt Ausstattung und Licht, das Ende bestimmt, wer bleibt (Ende 2a: die Lichter brennen, die Tische leeren sich im Streit).

| Auftrag | Wer | Szene | Frage und Entscheidung | Wenig Material | Ins Schlussbild |
|---|---|---|---|---|---|
| **The Catch** | Petru | Ausfahrt im Morgengrauen | Petru: *“Hm. Where do we go?”* · Zum Riff (viele kleine) · zur Grottenmündung (ein Pirat zeigt die Stelle, mit `a3_riscossore_kommt`) · aufs offene Wasser (ein großer Fisch, Angeln-Probe) | 3 Fische aus dieser Fahrt | Grill am Hafen: Sardinen, Muränen-Spieß oder ein ganzer Zackenbarsch |
| **The Garden** | Nonna | Ernte im Klostergarten | Nonna: *“Who gets the first basket?”* · die lange Tafel · Bà Tưs Topf · Frederico (nur wenn er lebt) | 3 Gemüse ★★★ | Körbe auf der langen Tafel |
| **The Pot** | Bà Tư | Thịt kho (Kanon) | Bà Tư: *“My way, or your mother's way, con?”* · beide gelingen, sie reagiert anders | 1 Gericht ★★ | der Topf, eine Schlange davor |
| **The Menu** | Lola | Lola hat Angst vor so vielen Gästen | Lola: *“Who tastes it first, Boss?”* · Minicu · Casanova · Duc | 1 Kochen. Mit `bl_tueren_lola` kennt sie jede Küche: *“I've been in every kitchen in this village, Boss. Mostly the biscuits.”*, ein Gericht weniger | Lola am Grill |
| **The Lights** | Rosi | Lichterkette | Rosi: *“What goes in the switch, Officer?”* · ein Chip von Duc (echter Verlust, weißes Licht) · ein Teil aus Alons Halsbändern (bernstein, wie Unit-01s Auge) | 2 Steel (Scrap Field oder Belagerungs-Roboter) | Lichter, weiß oder bernstein |
| **The Stage** | Minicu | Bühne bauen | Minicu: *“Who stands on it first?”* · Casanovas Rede · Alvas Flamenco · der Kinderchor (singt hinter der Kirchentür, nur zu hören, Kanon: kein Kind im Bild) | 4 Timber | wer zuerst auf der Bühne steht |
| **The Dresses** | Danzel | Anprobe in „Le Théâtre Rouge“ | Danzel: *“Whose dress first? I can only finish one in time!”* | ein Festa-Auftrag aus `schneider.md` | ein Kleid im Schlussbild |
| **The Bell** | Don | zwei Abende Karten statt Wein (mit `bl_kirche_don` einer, er war schon einmal nüchtern, als es zählte) | Don: *“Shall I win tonight, my son, or will you?”* · Lässt Duc ihn gewinnen? | – | die Glocke läutet zum Tanz im richtigen Takt |

Zwei kleine dazu: **Kinderbilder** (nur `bl_kirche_jana`, ohne Phase: Jana bringt sie, *“Sir, they made these for the festa. For me. Jessas.”*) und **The Eventually bringt Fisch** (Kanon, Buenaventura beliefert die Festa, nach `a3_riscossore_kommt`). Die Konfettikanone fehlt (Pascal hatte sie bezahlt). In Ende 1 ist sie wieder da.

## 5. Die Szenen

Jede Szene: **Ansage → Inhalt → Handlung → Reaktion → Übergang**, Titelkarten mit Continue und Skip, ernste Szenen mit ernsten Posen. Vor jedem Chip eine klare Frage. Chips: zuerst die Handlung als ganzer Satz, dann die Rede.

### 5.1 Tag 24, Frühstück · `a3_morgen` „The Morning After“ (ernst → warm)

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Titelkarte *Day 24 · The Morning After*. Piazza im Morgenlicht, Rauch über der Post (mit `tk_haus_weg_post`). | Erzählerin: *The village spends the night in the church. Nobody sleeps much.* |
| Inhalt | Duc kommt mit zwei Kaffeebechern. Die Leute gehen auseinander. Auf einem Handy läuft Alons Clip. | Mina, leise: *“Sorry, Yacht. I don't know what to say to you today.”* · Erzählerin: *A man near the fountain asks it out loud: “Did you know?”* |
| Handlung | | Chips: Puts both coffees down on the fountain. “My company belongs to the Eden Group. I didn't know they sold your harbour.” · “No. And I'm staying until you believe me.” · Stays where he is and says nothing. |
| Reaktion | Petru tritt vor ihn, das Gesicht zum Dorf. **Mit Rudern** (`bl_dorf_rudert`): | Petru: [clear throat] *“Hm. I rowed out with the village, like in 1924, and he held the church until we came back. Three days. That's all I need to know.”* |
| Reaktion | **Ohne Rudern:** | Petru: [clear throat] *“Hm. Three days he stood between the fire and the church. That's all I need to know.”* |
| Reaktion | | Lola, zu laut: *“Right! Who wants breakfast? I made heaps. Mostly the eggs.”* |
| Wende | W2 A: Titelkarte *Minicu*, er steht verbunden am Tor. W2 B: er steht am Tor, wie man es im Bericht hörte. | A: Jana: [gasp] *“Jessas! He's... Sir, he's standing!”* · B: Jana: *“Sir, he's back at the gate. With the bandage and everything.”* · Minicu: *“Pascal said hold the gate. So I hold it.”* · Lola: [sniff] *“Oh, mate. I'm bringing you eggs, don't you move.”* |
| Übergang | Karten „Talk to Minicu“, „Visit Alva“. Ziel-Zeile: *Buenaventura has asked the whole village to meet at the harbour.* | |

### 5.2 Tag 24, Tag · `a3_schwur` „The Oath“ (komisch → ernst → warm)

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Hafen, *The Eventually*, die Flagge auf halbmast. | Erzählerin: *Forty men stand on the quay. None of them is holding a torch.* |
| Inhalt (Fernseh-Moment, Kanon) | Ein Pirat hält ein Handy hoch: „pirates attacked a small village“. | Buenaventura: [laugh] *“I am famous! Look, Paco, that is our flag!”* · *“...Robots? I have never owned a robot in my life. They are saying I had robots!”* |
| Inhalt | Hut ab. | Buenaventura: [clear throat] *“We burned your houses. I gave the order to stop, and I gave it too late. I am sorry.”* · *“I don't know how a man makes that right. I have a flag, an anthem and forty men who can carry stones. We will find a way. I swear it.”* |
| Reaktion | | Casanova: *“You burned the post office.”* · Buenaventura: *“Yes, Madame.”* |
| Handlung | | Buenaventura: *“You beat me twice, Señor. So you decide. Do we stay and carry, or do we sail?”* · Chips: “Stay. Start with the houses you burned.” · Turns to Casanova. “Ask her, not me.” · “Stay. And you tell the commission who paid you.” |
| Reaktion | „Ask her“: Casanova: *“Stay. And carry everything twice.”* (+4) · Kommission: *“Of course. I am a pirate, not a liar.”* · Petru: *“Hm. Then carry stones.”* | |
| Schluss | | Buenaventura, zu einem Piraten mit ausgebrannter Fackel am Gürtel: *“Leave that.”* · Pirat: *“It's my torch, Capitán.”* |
| Übergang | `buenaventura_schwur`. Ziel-Zeile: *The burned houses are building sites now. Lay the first stone where you want them to start.* | |

Mit Bibi und `mo_eco_idee`: Erzählerin: *Bibi is counting the pirates. You don't know why yet.*

### 5.3 Ab Tag 24, Karte · `a3_alva_wach` „Since Last Night“ (ernst)

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | | Mina: *“Yacht! She's awake. Sandru says come, and Sandru never says come.”* |
| Inhalt | Bar abgebrannt: Feldbett in der Kirche (die Kirche brennt nie). Bar steht: `alvas_hinterzimmer`. Nie im A.V. Market. Sandru auf einem Hocker. | Alva: [cough] *“How long?”* · Sandru: *“Since last night. You missed the end. Ha. That's... sorry. That's not funny.”* · Alva: *“Minicu?”* · Sandru: *“He's standing at the gate. He won't go home.”* · Alva: [sigh] *“Of course he won't.”* |
| Handlung | | Alva: *“Who carried me out, Duc? Don't lie to me, I'll know.”* · Chips: “Sandru. He carried you out of the rubble.” · Looks at Sandru and waits. · “Does it matter?” |
| Reaktion | Wahrheit: *“...Orangeade's on me, then. For a year.”* · Sandru: *“I'm thirty, Alva.”* · Alva: *“I know how old you are. I was there.”* · Warten: Sandru sagt es selbst und lacht davor. · „Does it matter?“: *“Everything matters to me, Duc. That's my whole problem.”* | |
| Übergang | `a3_alva_wach`. Kein Paar. | |

### 5.4 Ab Tag 24, Karte · `a3_minicu_heim` „Is Pascal Coming?“ (ernst, leise)

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Nordtor, Kevin auf dem Pfosten. | Erzählerin: *He has stood here since six. Lola has brought eggs twice.* |
| Inhalt | Minicu fragt jeden, ob es wehtut (Figurenseite). | Minicu: *“Hello. Does it still hurt, from the fighting?”* · mit `bl_minicu_duc_zuerst`: *“You came first, when I was on the ground. Before Pascal. I heard you.”* |
| Handlung | | Minicu: *“Pascal said hold the gate. Did he say stop?”* · Chips: “You can go home now, Minicu. You held it.” · “Not yet. But I'll tell you when.” · Sits down next to him on the stones and waits. |
| Reaktion | Go home: Minicu: *“Is Pascal coming?”* · Chips: “No.” · “I don't know.” · Looks at the gate and doesn't answer. · Minicu nach einer Pause: *“Okay.”* Nach drei Schritten: *“Who holds it now?”* | |
| Reaktion | Warten: Die Karte kommt morgen wieder, Minicu sagt dann zuerst: *“You came back. Thank you.”* | |
| Übergang | `a3_minicu_heim`, Zeugen-Tür, ab morgen trägt er an den Baustellen. | |

### 5.5 Tag 25, Frühstück · `a3_uhr` „Under Control“ (ernst, trocken)

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Messe (Bord, Ersatzreihe), Telefon auf Lautsprecher. | |
| Inhalt | Beamter aus Ajaccio, nur Stimme. | Beamter: *“We received your file, Lieutenant. Two men from the commission will come on the thirty-fifth.”* · Elsa: *“That's ten days.”* · Beamter: [clear throat] *“We're very busy here. And we have the feeling you have this under control. Don't you?”* · *“To be honest, we were surprised. Cala d'Orsu sends us a report every month. 'All quiet.' Signed and stamped.”* |
| Reaktion | | Elsa: *“Five years on this post, and they have never been this polite to me.”* · *“I sent them a report every month too. Through the town hall. So where did mine go?”* |
| Inhalt | Mina mit zwölf Einschreiben aus Monaco. | Mina: *“There's one for Petru. A.V. bought the loan on his boat. And I have to take it to him. Me.”* · mit `bl_tueren_mina`: *“You let me go alone that night, when the phones were dead. I knocked on every door. I can do this too.”* |
| Handlung | | Elsa: *“First Officer. The commission wants witnesses. People who saw it with their own eyes and will sign their name. Will you help me find them?”* · Chips: “I'll talk to every one of them.” · “What about the crew? We saw everything.” · Takes Mina's basket. “Then we start with the letters.” |
| Reaktion | Crew: *“You're guests, and Alon just called you his partner on television. The village has to speak for itself.”* · Korb: Mina: *“...Okay. You knock. I'll hold the bike.”* | |
| Zusatz (Totòs Versprechen) | Nur wenn Duc Totò in der Grotte versprochen hat, dass die Kiste Alon zu Fall bringt (`VER("toto", …, {"flag": "alon_kiste_genutzt"})`, `ereignisse_grotte.py:513-514`), das Versprechen noch offen ist und Duc die Kiste hat. | Totò: *“Comandante. You promised me that crate would bring Alon down, the night we lost Gennaro. Give it to her.”* · Chips: Hands Elsa the crate. · “Not yet, Totò.” (die Frist läuft weiter) · Kiste: `alon_kiste_genutzt`, Beweis für 5.26 |
| Übergang | Zeugenliste offen, Kopfzeile *Commission in 10 days.* Elsa: *“On Saturday I drive to Ajaccio. I want to see these 'all quiet' reports myself.”* | |

### 5.6 Tag 25, Dinner · `a3_megan_landet` „Until I Land“ (Megan-Theater)

Rückkehrtag Vorschlag **Tag 25** (E-117 offen), zwei Tage nach dem Netz. Im Cliffhanger: *“Don't say a word to anyone until I land.”*

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Wassertaxi, ein Koffer, Achterdeck (Bord, Ersatzreihe). | Erzählerin: *No helicopter this time. A water taxi from Bastia, and one suitcase.* |
| Inhalt | | Megan: [sigh] *“How... delightful. I'm gone for three weeks, and my yacht becomes a field hospital.”* · Holm: *“Megan.”* · Megan: *“Captain. You're standing.”* · Holm: *“Mostly.”* |
| Inhalt | Megans alte Kriegstafel hängt noch (`bl_tafel`). | Megan: *“My list. Six jobs. You did {n} of them.”* · Holm, mit `bl_will_ab_niemand` und `bl_will_na_niemand`: *“He slept, both nights. First sensible man on this boat.”* |
| Handlung | Megan nimmt Duc beiseite. | Megan: *“Duc. Alon thanked 'our partners at the Eden Group'. Did you know who was buying the harbour?”* · Chips: “No. Did you?” · “I didn't know they were selling it at all.” · Doesn't joke this time. “Mac. I'd never sell these people.” (nur `megan_funke`) |
| Reaktion | | Megan: *“I negotiated that sale. Every line. I never asked who A.V. was, because the numbers were good. So that's two of us who didn't ask.”* |
| Inhalt | | Megan: *“Here's the deal, First Officer. I'll try to stop the sale. The board in Monaco won't believe a video. They want paper and names. Can you get me names?”* · Chips: “I'm already collecting them.” · “Why do you care now?” · “What's in it for you, Mac?” |
| Reaktion | Warum: *“Because he nearly sank my ship. And because I signed it.”* · Mac: [chuckle] *“A seat on the board. Obviously. And a quiet evening, maybe. Don't push it.”* | |
| Übergang | `megan_zurueck`, VIP-Kabine (W1 auf Grund: erst nach dem Heben, bis dahin Alvas Gästezimmer; W1 gesunken: Alvas Gästezimmer), `a3_megan_handel`. | |

### 5.7 Tag 26, Frühstück · `a3_festa_tafel` „THIS. IS. THE. FESTA!“ (komisch, warm)

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Piazza, eine Tafel an der Kirchenmauer, Kevin darauf. | Erzählerin: *She has been here since five. The board is taller than she is.* |
| Inhalt | Rede mit Pause. Mit `a3_minicu_heim` klatscht Minicu, zu laut und allein. Sonst kreischt Kevin. | Casanova: *“Cala d'Orsu! They burned our houses. They want us to cancel the festa. So we will NOT!”* (Pause) · Erzählerin: *One person claps. Very loudly. It's Minicu.* · Casanova: *“...Thank you, Minicu. That was very loud.”* |
| Inhalt | | Casanova: *“Eight jobs. Every job is a person. Nothing from the shop!”* |
| Handlung | | Casanova: *“Monsieur. I need fish, lights and a stage. Can I count on you, or should I count on someone else?”* · Chips: “Count on me.” · “I'll bring you the fish myself.” · “Count on me. And on the pirates.” |
| Reaktion | | Casanova: *“Good. ...Good. That's all I wanted to know today.”* · *“And somebody get that bird off the fish!”* |
| Übergang | Tafel offen. | |

### 5.8 Tag 28, Tag · `a3_sonntag` „Sunday“ (warm → ernst, leise, eine Kette)

Messe, Don an der Tür und die Schublade in einer Kette (Woche 4 bleibt leicht). Elsa kommt am Sonntagmorgen aus Ajaccio zurück. Spannung 4.

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Kirche, ein Eimer in der ersten Reihe, es tropft. | Erzählerin: *The new roof is his money. The money has stopped. The rain hasn't.* |
| Inhalt | | Don: *“Today I'll keep it short, because the roof is listening.”* · Erzählerin: *Outside, at the bus stop, a father takes the timetable down and folds it very small. The school bus won't come on Monday.* · Bà Tư, eine Dose in Ducs Hand: *“Eat. You're too thin. And don't look at the bus stop like that. You didn't stop that bus.”* |
| Ansage | Nach der Messe: Leute mit Kisten an der Rathaustreppe (Bestellung `town_hall_stairs`). | Erzählerin: *They want to throw everything he owned into the harbour.* |
| Inhalt | Don vor der Tür, ohne Flachmann. | Don: *“No.”* · Mann: *“Father, he opened the gate!”* · Don: *“I know what he did, my son. I was there. Nobody goes in.”* |
| Handlung | | Mann: *“Are you with him or with us?”* · Chips: Walks up the stairs and stands next to Don. · “Elsa is on her way. Leave it for her.” · Stays at the bottom of the stairs. |
| Reaktion | Neben Don: *“Thank you, my son. My knees are not as brave as my mouth.”* (+6, Tür) · Elsa: *“Logic. I never tried that.”* · Unten: Don hält allein (seine Tür bleibt über Vertrauen 3 und *The Bell* erreichbar) | |
| Ansage | Elsa kommt mit einem Brecheisen. Pascals Zimmer (Bestellung `pascal_room`): Schreibtisch, **ein leerer Haken, ein heller Rand an der Wand**. | Elsa: *“Father. I'm going in.”* · Don: *“You're the law, Lieutenant. I'm only a door.”* |
| Inhalt | | Elsa: *“My antenna form. Eleven months. 'Almost through.'”* · Erzählerin: *Elsa's reports to the mayor, never delivered.* · *Casanova's EU applications, signed, never sent.* · *Copies of the monthly report to Ajaccio: “All quiet.” His signature.* · mit `rt_ende_alle` oder `ark_aussagen_3`: *The red team's signed statements. Elsa handed them in herself.* |
| Inhalt | mit `bl_wache_gesehen` (Duc hat Holm von der Nachtwache erzählt, Holm hat es Elsa gesagt): ein Funkbuch. | Elsa: *“Holm told me about three o'clock. Here it is. Night of the twenty-second: two words.”* (Beweis) |
| Wende | Ganz unten ein Kassenbuch in derselben sorgfältigen Hand. | Elsa: [sigh] *“The roof. The school bus. The festa money. And here: the priest. Sandru. ...Madame Casanova.”* |
| Handlung | | Elsa: *“This goes to the commission. All of it, or only his part? Think about it until then.”* · Chips: “All of it.” · “Only Alon's part. The village has paid enough.” · “I don't know yet.” |
| Reaktion | vorgemerkt (`a3_buch_alles` / `_teil` / `_offen`) | Elsa: *“For the record: I'd make the same face you're making.”* |
| Übergang | `a3_don_tuer`, Item „Pascal's Ledger“ bei Elsa. Nonnas Karte ab dem Nachmittag (5.9). | |

### 5.9 Ab Tag 28 Nachmittag, Karte · `a3_nonna_kiste` „The Last Crate“ (ernst, kurz)

Die Kiste stand seit dem Morgen von Tag 24 vor Nonnas Tür. Sie öffnet den Brief erst, nachdem Don vor Pascals Tür stand (Kanon: sie versteht es rückblickend). Kommt Duc bis Tag 30 nicht, bringt Mina Schlüssel und Brief mit einem Zettel von Nonna.

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Klostergarten, Kiste mit Setzlingen, ein gefalteter Brief. | Erzählerin: *Every week there is a crate of seedlings at her door. This one came the morning after the siege. She waited until today to read the letter.* |
| Inhalt | | Nonna (liest): *“I told the priest not to go up the mountain. 'Stay, Don. Leave it with me.' I thought it was for safety.”* · *“And I told him all of it, every month, for nine years. He can't say a word. That's why he drinks.”* · Nonna: *“And today he stood in front of that door for him. Now I understand.”* |
| Zusatz | mit `bl_minicu_sag_es` | Nonna (liest): *“Duc told me to say it to him, to Minicu at the gate. So I did. It was the only true thing I said that night.”* |
| Reaktion | | Nonna: [sniff] *“I told Isabelle that man has a good heart. You don't have a good heart, Pascal. You have a bad conscience.”* |
| Handlung | Ein alter Schlüssel mit Zettel. | Zettel: *“Leave it with... no. You do it. I just have the key.”* · Nonna: *“The cellar door of the Casanova house. Do you want it, or shall I throw it in the sea?”* · Chips: Takes the key. · “Keep it, Nonna. I'll find another way in.” |
| Schluss | | Erzählerin: *She plants them anyway. Nothing in her garden goes hungry.* |

### 5.10 Ab Tag 24 Abend, Karte · `a3_siri_post` „In My Own Words“ (ernst → warm)

Kanon: Siris Post in eigenen Worten, Vaters Pullover, Yasins Geldangebot.

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Kai bei Sonnenuntergang, Siri im Pullover ihres Vaters, dem mit den Sternen. | |
| Inhalt | mit `siri_wartet` (sie wollte auf Minicu warten): Siri geht zuerst zu Minicu. | Siri: *“Minicu, can I show them you're standing?”* · Minicu: *“Does it hurt them to see?”* · Siri: *“No. I think it helps.”* |
| Inhalt | mit `siri_darf_posten`: | Siri: *“It was up for four seconds, and then his video slid over it. This time I'm not giving him four seconds.”* |
| Inhalt | | Yasin: *“Bro. Somebody offered me twenty thousand for the video. Twenty! That's business.”* · Siri: *“It's his company, Yasin. He'll buy it, and nobody will ever see it.”* |
| Handlung | | Siri: *“Duc. I want to post it myself. No filter, no music, just what we saw. Is that brave or stupid?”* · Chips: “Brave. Post it.” · “Post it, and I'll stand next to you when he calls it fake.” · “Ask Yasin. It's his video too.” |
| Reaktion | Yasin, ehrlich, dann überspielt: *“...I filmed Minicu falling, and I kept filming. I don't want money for that. Okay? Don't tell anyone I said okay.”* | |
| Übergang | `a3_siri_post`, Beweis (Wahrheit). Mit `siri_wartet` stärker: der Post zeigt Minicu stehend. | |

### 5.11 Tag 29, Abend · `a3_berichte` „Every Report“ (ernst, Casanovas Wende)

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Kirchenstufen bei Nacht, Kerzen, Elsa mit einem Stapel. | |
| Inhalt | | Elsa: *“March. 'Dogs with collars near the monastery road.'”* · *“May. 'Request for a meeting with the mayor.'”* · *“August. 'Request for a meeting with the mayor.'”* · Erzählerin: *She reads thirty-one of them. Casanova doesn't stop her once.* |
| Reaktion | | Casanova: *“He told me you never wrote.”* · Elsa: *“I wrote every month, Madame.”* |
| Handlung | | Casanova: *“Monsieur. Pascal kept the truth in a drawer for nine years. What did you keep in yours?”* · Chips: “Nothing about your harbour. But I should have asked my own company more questions.” · Sits down on the step below her. “Only that I'm sorry it came on television.” · “I'm still here. That's my answer.” |
| Reaktion | Erste: *“Questions. Nobody here asked enough of those, Monsieur.”* (+6) · Zweite: sie nickt (+4) · Dritte: *“Yes. You are. So is the bell, and the bell has no choice.”* (+2) | |
| Schluss | | Casanova: *“Lieutenant. From now on you report to me. Directly. Every day, if you like.”* · Elsa: *“Every day, Madame?”* · Casanova: *“...Every week.”* |
| Übergang | Casanovas Tür. Elsa schickt die EU-Anträge selbst (Brüssel-Brief im Epilog). | |

### 5.12 Ab Tag 24, Karte · `a3_revanche` „The Rematch“ (komisch, warm)

Mit Gemelli, ab Tag 24 (`HOLM_TAG = 24`, Branch `fix-akt2-folgen`).

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Holm auf der Mole, ohne Krücke. | Holm: *“Frankfurt. You still have my rifle. I want it back, so we shoot for it. Ready?”* |
| Inhalt | Schießwette (gebaut). | Holm: *“It pulls left, like the day you won it from me.”* |
| Reaktion | Duc gewinnt: *“Faen. Keep it. I'll win it back at the festa.”* · verliert: *“Keep it anyway. My hands are fine now. My head isn't, yet.”* · mit `bl_nachtwache_niemand`: *“I told you to send somebody to the north road that night. I should have gone myself.”* | |
| Schluss | | Petru, stellt die letzte Flasche hin: *“Hm. Again.”* · Holm: *“Takk.”* |

### 5.13 Tag 29, Frühstück · `a3_idee` „Forty Men and a Boat“ (komisch → warm)

| Fassung | Bedingung | Kernzeile |
|---|---|---|
| Bibi | `rt_bibi_bleibt` und `mo_eco_idee` | Bibi: [laugh] *“So he's got forty men, a boat and nothing to do? And they know every rock in that bay? Doudou. Doudou, come here. I need you to do some numbers.”* |
| Lea | `margot_geborgen` (F-05) | Lea: *“Did you know a protected bay needs people who know every rock? Proper people, with boats. And they've got forty!”* |
| Petru | sonst | Petru: *“Hm. Boats need captains. He has one boat and forty men who are good at one thing. Finding things in caves.”* |

| Beat | Zeilen |
|---|---|
| Handlung | Buenaventura: *“Tours? Tourists? On my ship? Why would a pirate do that, Señor?”* · Chips: “You were a pirate. Now you're a captain with a debt.” · “You'd be the head of something. The head of the sea captains.” · “Show people the grotto. They'll pay to see it.” |
| Reaktion | Buenaventura: *“The head of...”* (Pause) *“...I would need a hat.”* · *“But the grotto belongs to the old man with the oranges. And I owe him everything already. The ship. Even the name of the ship.”* |
| Übergang | Karte „The Man with the Orange“. |

### 5.14 Ab Tag 29, Karte · `a3_orange` „The Man with the Orange“ (ernst-komisch)

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Grotte, Riscossore schält eine Orange. Totò ab Vertrauen 3 dabei. | mit `gr_8_riscossore`: Riscossore: *“Last time you came with a knife. Today you came with a captain. Better.”* · ohne: Erzählerin: *An old man in a white suit sits by the water and peels an orange. Everybody here owes him money.* |
| Inhalt | | Buenaventura: *“I want to show tourists your grotto. I pay you from every ticket.”* · Riscossore: *“Eventually.”* · Buenaventura: *“...Eventually.”* · Riscossore: *“A man in prison pays nobody. A man with tourists pays me every day, a little. I prefer every day.”* |
| Handlung | | Riscossore: *“You want something too, I think. The commission. Why should I come and open my book for you?”* · Chips: “Because Alon paid Buenaventura through you. It's in your book.” · “Because nobody pays you if Alon gets the bay.” · Looks at Totò and says nothing. (nur `gennaro_verschwunden`, Totò dabei) |
| Reaktion | Erste: *“Clever. Not kind. Clever.”* · Zweite: *“Yes. That is the reason. Not kindness.”* · Dritte: Erzählerin: *Totò walks out. Gennaro's boat is still empty, somewhere off Cap Corse.* Riscossore: *“He hates me. He should. ...I'll come.”* | |
| Schluss (Kanon `akt3.md`) | Ebbe. Buenaventura watet zu dem Felsen vor der Grotte und steckt seine Flagge hinein. | Buenaventura: *“It is an island. Twice a day.”* · Riscossore, ein Orangenstück: *“Here. Your first payment.”* |
| Übergang | `a3_riscossore_kommt`. Bis Tag 35 zeigen die Piraten Wege nur als Freundschaftsdienst. Den Namen „Head of Sea Captains Eco Tours“ gibt es erst im Epilog, nur im guten Weg (Kanon). | |

### 5.15 Tag 30, Frühstück · `a3_maxwell_flug` „Gogo's Medicine“ (warm)

| Beat | Zeilen |
|---|---|
| Inhalt | Maxwell mit einer Kühltasche: [clear throat] *“Number One. Mr. Maximum is going to fly. In an aeroplane. Up there. Gogo's medicine is in Johannesburg, and the post is too slow.”* · mit `bl_verband_maxwell` zeigt er den Verband aus der Belagerung: *“Mr. Maximum kept it. For luck.”* |
| Handlung | Maxwell: *“Tell Mr. Maximum something, brother. What does a big man do when he's scared of the sky?”* · Chips: “He takes the window seat and looks anyway.” · Puts a hand on the cool box. “He carries it. Like you always do.” · “He holds Jana's hand. She's coming to the airport.” |
| Reaktion | dritter: Jana: *“Coach, I'll hold your hand the whole way to Bastia. Sorry. Not sorry.”* |
| Übergang | Maxwell fehlt Tag 30 bis 32, zurück am Abend von Tag 32: *“Mr. Maximum has flown. Mr. Maximum will never speak of it.”* |

### 5.16 Ab Tag 29, Karte · `a3_lot14` „Lot 14“ (ernst)

Kanon: Rosi erfährt durch Yamamoto von „Lot 14“. Ab Vertrauen Yamamoto 3.

| Beat | Zeilen |
|---|---|
| Inhalt | Yamamoto: *“So sorry, Rosi-san. I read A.V.'s property lists for my bank. There is a street in Catania. Lot 14. A workshop, closed three years ago.”* · Rosi: *“...The press in that workshop was older than Papa. It had a crack in the left side. He called it Old Lady.”* |
| Handlung | Rosi: *“Officer. If he goes down, can I buy it back? Tell me the truth.”* · Chips: “If he goes down, yes. So let's make him go down.” · “I don't know. But I'll help you try.” · Sits down on the toolbox next to her and waits. |
| Übergang | `a3_lot14` (Rosis Ende 2a und 3). |

### 5.17 Tag 31, Dinner · `a3_megan_monaco` „The Board“ (ernst, Säule Geld)

Megans Erfolg hängt an Ducs Material: ab **4 Zeugen oder 2 Beweisen**. Yamamoto mit Bindung 5 ruft vorher an: *“Officer-san. So sorry. I have stopped the loan. I did not ask permission. Very rude of me.”*

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | VIP-Kabine (Bord, Ersatzreihe), Megan in Boardroom-Kleidung. | Megan: *“Stay out of the picture, First Officer. And don't breathe so loudly.”* |
| Inhalt | | mit Zeugen: Megan: *“I have {zeugen} people ready to sign, in front of a commission.”* · nur Beweise: *“I have papers from his own cellar, and a video he can't buy.”* · CEO (nur Stimme): *“Megan. A.V. pays us well. Is this about the yacht, or about you?”* |
| Wende (genug) | | Megan: *“It's about a bay that's worth more protected than sold.”* · CEO: *“...Is Duc there? Put him on. Duc, tell me straight. Is this village worth more than what A.V. pays me?”* · Chips: Steps into the picture. “The numbers are hers. The names are the village's. I just carried the letters.” · “Sell them the bay, and you sell them me with it.” |
| Wende (zu wenig) | | CEO: *“Bring me something better than a fishing village, Megan.”* Bildschirm aus. |
| Reaktion | | genug: *“That's the first argument I've won that I actually believe in. It's uncomfortable.”* · zu wenig: *“How... delightful.”* (leise) |
| Übergang | `a3_megan_wende` oder `a3_megan_verloren`. Säule Geld braucht weiter die Margot. | |

### 5.18 Tag 32, Nachmittag · `a3_switched_off` „Switched Off“ (ernst, **der** schwere Moment)

**W5 A (Vorschlag).** Tag 32 ist gagfrei. Die Szene kommt immer, *weil Alon kann* (Kanon).

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Keine Titelkarte, keine Musik. | Mina: *“Yacht! YACHT! The market. It's Sandru.”* |
| Inhalt | A.V. Market, Sandru zwischen den Regalen, die Schienen still. | Erzählerin: *The braces are quiet. You never noticed the sound until it stopped.* · Bildschirm: *Device paused. The user broke the rules of service. Thank you for your understanding.* · Sandru: [laugh] *“Ha. They switched me off. Like a lamp.”* · mit `sandru_surren` (Duc hat das Surren gehört): *“You heard them hum, the first day you came in here. Now listen.”* |
| Wende | Alva betritt **zum ersten Mal** das Haus ihrer Mutter. Titelkarte *Alva*. | Erzählerin: *She has not stepped into this house in six years.* |
| Handlung | | Alva: *“Duc. The door. Can you hold the door?”* · Chips: Holds the door. · Takes his other arm. · Steps back and lets her do it. |
| Reaktion | Alva trägt ihn über die Straße in ihre Bar (oder auf eine Matratze in der Baustelle) und die Treppe hoch. | Alva: [sigh] *“You're my little brother, you idiot. I've carried you since you were six.”* · Sandru: *“I know. That's the whole problem.”* |
| Schluss | Kein Paar. | Erzählerin: *She sits on the stairs for a minute. Then she goes back down to the bar.* |
| Übergang | `a3_sandru_aus`. Gags mit Ton `witzig` bleiben bis zum Ende aus. | |

**W5 B:** gleicher Aufbau, aber die Lampen des A.V. Market gehen aus, ein Zettel an der Tür (*“Closed until further notice. A.V.”*), zwölf Leute aus dem Dorf stehen vor der dunklen Tür. Sandru steht auf Rosis Schiene vor ihnen und lacht nicht: *“He can't switch my legs off any more. So he switched off your jobs.”* Alva kommt herüber und stellt sich neben ihn. Seine Tür öffnet danach.

### 5.19 Tag 33, Frühstück · `a3_schiene` „No Leash“ (warm, leise)

Nur W5 A, wenn Duc sich gekümmert hat (`sandru_surren`, `sandru_herkunft` (noch nicht gebaut, F-20) oder Vertrauen Sandru 3). Ist Rosi gefeuert, hört Maxwell (zurück seit Tag 32 abends) und Rosi hilft per Video (Kanon).

| Beat | Zeilen |
|---|---|
| Inhalt | Rosi: *“Same motors. Same chips. I only took out the part that talks to his computers. The leash, Officer. Like with the collars.”* · gefeuert: Maxwell: *“Mr. Maximum holds the screwdriver. Rosi says which way. Teamwork, brother.”* · Rosi: *“That sound is mine now. Don't let them tell you otherwise.”* |
| Inhalt | Sandru steht auf: *“A.V. gave me six years of walking. You gave me a speech.”* (Kanon) · *“...And her. You gave me her.”* · *“So what do I do now, Duc? Walk over there and say what?”* |
| Handlung | Chips: “Say thank you. Then say nothing.” · “Go and stand in front of Alva. Straight.” · Shrugs. “You gave yourself the speech. I just listened.” |
| Reaktion | mit `sandru_herkunft`: *“Iskander. You can say it. My mother says it.”* · sonst: *“Ha. One thing at a time, Duc.”* |
| Übergang | Namensschild ISKANDER oder SANDRU, `a3_sandru_schiene`, Tür offen. Ohne Schiene: Sandru steht an Tag 34 auf Alons Seite (*“They switched me back on. That's how it works, Duc.”*), sein Name fehlt im Netz. |

### 5.20 Tag 33, Frühstück · `a3_einladung` „An Invitation“ (ernst)

| Beat | Zeilen |
|---|---|
| Inhalt | Mina mit einem cremefarbenen Umschlag: *“This one's for you, Yacht. The good paper. From the house on the hill.”* · Erzählerin: *“Dinner. Tomorrow at eight. Just you. A.V.”* · *Your name on the envelope is in a careful hand. You have seen it before: on Minicu's name sheet, the one you picked up at the gate, and on Alon's letters on the church steps.* (`bl_blatt_gefunden`, das beide Bericht-Chips setzen) |
| Handlung | Mina: *“Are you going?”* · Chips: “Yes.” · “Yes. But not alone.” · “I don't know yet.” |
| Übergang | Ziel-Zeile: *Tomorrow: dinner at the villa.* Mit Schlüssel: *And you have a key.* |

### 5.21 Tag 33, Abend · `a3_festa_frage` „After Midnight“ (frech, warm, **privat**)

E-060: Romanzen sind privat. Darum fragt keine Frau nach einer Begleitung vor dem Dorf, sondern nach einem Moment für sich: **nach Mitternacht an der Mole**, wenn die Festa noch läuft. Das Dorf sieht höchstens zwei Menschen, die zusammen am Wasser stehen. Öffentlich bleibt nur, was gebaut und Kanon ist (Alvas Flamenco). Duc wählt eine oder niemanden. **Lea oder Sophia, nie beide.**
Bedingung je Frau: die Stufe-5-Szene ihrer Leiter gesehen. Megan: `megan_funke` und eine gemeinsame Nacht (sie hat kein Begehren). Bibi: `rt_bibi_bleibt`, Leiter bis *The Brochure*.

| Frau | Ihre Frage | Nach Mitternacht |
|---|---|---|
| Chiara | *“First Officer. I'll ask you once, and if you laugh, it's a two. After midnight, on the mole. Will you come?”* | ihre Zehn (Kanon) |
| Alva | *“After my dance, Duc, I close the bar for one hour. Will you be on the quay?”* | „Only you“ (Kanon, nach dem Flamenco) |
| Lea | *“Two fingers, the sign from the swim platform. After midnight. Yes?”* | ihre Azoren-Antwort (Kanon) |
| Sophia | *“Ten euros says you'll come down to the mole after midnight. ...Oh. Have I just lost?”* | eine Zeile aus ihrem Buch, nur für ihn |
| Rosi | *“Officer. My mother leaves the festa at midnight. Will you be on the mole after that?”* | Rosi sagt „Captain“, wenn er es verdient |
| Lola | *“Boss. When the cooking's done. One song, just us, on the mole. Mostly one song. Yes?”* | Lola setzt sich hin |
| Siri | *“No camera after midnight. Will you meet me by the water?”* | ihre eigenen Worte, ohne Handy |
| Bibi | *“The gates open on Sunday afternoon, and I'll be a mess. After midnight, will you come anyway?”* | nach *Last Page* |
| Megan | *“Don't make me say it twice, First Officer. The aft deck, after midnight. Then we never speak of it. Agreed?”* | Abendkleid ohne Anker |

Die Gewählte steht in der Nacht von Tag 34 oben in der Liste, mit eigener erster Zeile. Kein Echo für die anderen (höchstens eine Leiter-Szene oder ein Echo am Tag, `beziehungen.md`). Sie sind auf der Festa einfach da, jede mit einer Zeile im Festbild.

### 5.22 Tag 34, Frühstück · `a3_villa_plan` „The House on the Hill“ (ernst, kurz)

Elsa ist nicht dabei (sie darf vom Schlüssel nichts wissen). Megan auch nicht (sie und Pascal sollen sich nicht begegnen, `dorf_figuren.md`).

| Beat | Zeilen |
|---|---|
| Inhalt | Holm: *“You're invited, Frankfurt. Better than a police paper.”* · mit Schlüssel: Rosi: *“A cellar door nobody locks properly. Old iron. My favourite kind of door.”* · ohne: Casanova: *“I know the cellar. I hid there from my father when I was seven. I'll take you.”* |
| Handlung | Holm: *“Who goes down with you, Frankfurt?”* · Chips: Nods at Rosi. “You and me.” · Turns to Casanova. “Show me the way, Madame.” (ohne Schlüssel die einzige) · Picks up the key. “I'll go alone.” |
| Übergang | `a3_villa_mit_<id>`. Nachmittag frei. |

### 5.23 Tag 34, Tag · `a3_villa_keller` „The Cellar“ (ernst, Mission)

| Frame | Bild (Bestellung) | Inhalt |
|---|---|---|
| 1 | `villa_cellar` | Der Schlüssel passt. Casanova bleibt an der Tür: *“It's smaller than I remember. ...Go. I'll wait here.”* (Sie betritt das Haus nicht, das bleibt ★) |
| 2 | `villa_cellar` | Server-Schrank zwischen Weinfässern. Rosi: *“He put his computers in a wine cellar. That's a crime too.”* |
| 3 | `villa_office` | Whites Einsatzplan: *Day 22, phase 3: torches, houses.* Quittung an Buenaventura. Item „White's Orders“ (`a3_beweis_feuer`) |
| 4 | Treppe | zwei Agenten, ein Roboter, Kampf (Steel als Beute) |

### 5.24 Tag 34, Dinner · `a3_villa_dinner` „Name Your Price“ (ernst, Spitze)

Ohne Kamera: ruhig und genau. Pascal im weißen Fedora an der Tür, ohne Zeile.

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Speisesaal (`villa_dining`, Platzhalter `alon_keynote`), Tisch für zwei, Fenster zur Bucht. | Erzählerin: *From up here, the village looks like a model. The building sites look like toys.* |
| Inhalt | | Alon: *“Duc. Sit. Two of my people are asleep in my cellar, so I think you came the back way. You've been busy.”* · *“Keep the folder. Paper. In my experience, paper loses.”* · *“Every collar your mechanic cut open sent me one last message. That's how I learned to lock them. You helped me more than any engineer I hired.”* · *“Four hundred thousand people died in wars last year. I can bring that to zero. I need one bay and ten more years. You've seen my health. I don't have ten years. So I need the bay now.”* |
| Handlung | | Alon: *“Join me. Name your price.”* · Chips: “No.” · Looks out of the window at the village and says nothing. · “What would my price be?” · Puts his glass down. “Everyone I've met down there. Can you buy that?” |
| Reaktion | Preis: *“Eden Consulting, free of debt. Your name on a building in Frankfurt. And you never think about this village again. So?”* · Chips: “Deal.” · “No.” · ★ (alle vier Säulen, Yamamoto Bindung 5, Ende 1 gesehen): dritter Chip “Deal. Let's sign it in front of the village.” | |
| Übergang | Ja → 5.25 mit Deal · ★ → 5.25 mit ★ · Nein → 5.25 | |

### 5.25 Tag 34, Abend · `a3_villa_ende` „The Last Push“

| Zweig | Was | Zeilen |
|---|---|---|
| Presse (immer, Kanon „vor laufendem Stream“) | Terrasse, Drohnenkamera, Alon als Großsprecher, Pascal neben ihm. | Alon: *“Hi, Cala d'Orsu! Quick update from your future. And a big thank you to my partner on the ground, Paul... Paolo. Thank you, Paolo.”* Pascal lächelt und korrigiert ihn nicht. · Erzählerin: *The man who knows every name in the village. His master doesn't know his.* |
| Deal | Duc steht im Stream neben Alon, Ende 1 (Kanon). | |
| ★ | Das Dorf steht am Fuß der Villa (Kanon `enden.md`), Alon will vor ihnen unterschreiben. Casanova tritt vor und betritt ihr Elternhaus (Schlussbild ★). Genauer Ablauf mit Ducs Feinschliff der Enden | |
| Nein: Endkampf | Kamera aus, Exoskelett. Kampf (Luft, tödlich). Ducs Ausrüstung fällt nicht aus. Mit Rosi: Unit-01 bricht in Runde 3 durch die Kellertür. | Rosi: *“I took the leash out.”* · Alon: *“I know. That's how I learned to lock it.”* · Rosi: *“She doesn't have a leash. She never did.”* |
| Nein: Festnahme | An der Mole unter der Villa. Elsa hat den Stream gesehen und ist mit der Küstenwache gekommen. Duc kommt als eingeladener Gast mit „White's Orders“ heraus. Bedingung: Elsa Vertrauen 4, `elsa_hilft`. | Elsa: *“I saw your face on his stream, First Officer. I don't want to know how you got in.”* · zu Alon: *“Mr. Varenne. Coast guard. You're under arrest, and I'd honestly prefer it if you said nothing.”* |
| Niederlage | kein Game Over | Alon: *“Go home, Duc. The commission is tomorrow. I'll be watching.”* |
| Pascal | geht in jedem Zweig. Bei der Festnahme: | Pascal: *“Elsa. Your mother's birthday is next week.”* Elsa antwortet nicht. |
| Nachtwache | mit `bl_nachtwache_wolff` / `_elsa` / `_yamamoto`: Die Person steht im Hof, als Pascal vorbeigeht. | Wolff: *“Three o'clock. 'Not yet.' I remember.”* · Elsa: *“For the record, Pascal: three o'clock.”* · Yamamoto: *“Pascal-san. The coffee was very good. I am still worried.”* |
| Übergang | `a3_alon_besiegt`, `a3_alon_festgenommen` (Stärke). Nacht: `a3_letzte_nacht` (wie die Belagerungs-Nächte). Mit Deal: keine Nacht. | |

### 5.26 Tag 35, Tag · `a3_kommission` „Who Saw It?“ mit `mo_kommission`

Ort und Besetzung wie `mo_kommission` (`ereignisse_mochis.py:182-185`): **Kai**, Klapptisch, **zwei Männer aus Ajaccio, ein Schreiber**.
**Reihenfolge:** Hat der Spieler `mo_ark_beweis`, **eröffnet** `mo_kommission` (unverändert, mit seiner eigenen Vorstellung des Tischs), und `a3_kommission` schließt ohne zweite Ansage an. Sonst eröffnet `a3_kommission` mit der Ansage unten. Bau-Hinweis: welches Pflicht-Event zuerst kommt, in `ereignisse_basis.py` festlegen (F-25).
**Mit Deal:** Die Männer kommen, aber das Dorf schweigt, Duc ist oben in der Villa. Drei Zeilen, dann Ende 1.

| Beat | Was | Zeilen |
|---|---|---|
| Ansage (ohne `mo_kommission`) | | Erzählerin: *Two men from Ajaccio. One folding table. One clerk with a lot of paper.* |
| Inhalt | Der ältere der beiden („the gentleman“). | Kommissar: *“We are here to find out what happened in this bay on the twenty-first, twenty-second and twenty-third. Who saw it with their own eyes?”* |
| Inhalt | **Zeugen**, je eine Zeile in ihrer Haltung, nur was sie sahen. Wer schweigt, sitzt am Rand. | Petru: *“I saw the torches at my workshop. And I saw who stayed.”* · mit Rudern: *“And the village rowed out. Like in 1924.”* · Mina: *“I knocked on every door that night. I don't read the post. This time I read it.”* · Bà Tư (mit `bl_batu_norden`): *“Men in white. They asked me twice for the north road. I told Duc then. Now I tell you.”* · Alva: *“From the square I saw the north barricade open. Then men in white came through. I saw that with my own eyes.”* · Sandru: *“My name is {sandru_name}. I carried Alva out of the rubble. And the next week, A.V. switched off my legs.”* (W5 B: *“...closed the shop.”*) · Don, mit `bl_kirche_don`: *“I was sober. Write that down too. It doesn't happen often.”* · Don, ohne: *“I was asleep on the church steps, my son. But I saw the gate open before I fell asleep.”* · Minicu: *“Pascal said hold the gate. I held it. A man in white hit me. Once.”* · Casanova: *“I am the mayor of Cala d'Orsu. I signed nothing. And I am still here.”* |
| Inhalt | **Buenaventura** | *“A man named White paid me in clean money, like a bank. I gave the order to burn. I gave the order to stop.”* · Kommissar: *“And you are?”* · *“Captain Buenaventura of The Eventually.”* · Kommissar: *“...I see.”* |
| Wende | **Riscossore** mit Orange (Kanon) | *“He's telling the truth. It's in my book, page forty-one. A man in prison pays nobody, so I'd like him to stay out.”* |
| Inhalt | **Beweise**, je ein Satz, nur was der Spieler hat. Nichts über die Yacht von Tag 0. | `a3_beweis_feuer` · `alon_kiste_genutzt` · `a3_siri_post` · `sophia_notizen`: Sophia: *“Darling, I wrote down every time and every word I heard on the radio that night. I didn't know why. Now I do.”* · `bl_funk_white` / `bl_funk_charly`: Charly: *“Twenty-one forty. He said 'tonight'. Seven out of ten for clarity.”* · Funkbuch (`bl_wache_gesehen`) · Nachtwache je Person: Wolff: *“Three o'clock, the north radio. Two words: 'not yet'.”* · Elsa: *“For the record: three o'clock, two words, 'not yet'.”* · Yamamoto: *“So sorry. At three o'clock I heard two words. 'Not yet.'”* · Adriens Fotos, Steuerchip, fremdes Teil, Red-Trio-Aussagen |
| Handlung | **Das Kassenbuch**, endgültig | Elsa: *“First Officer. Pascal's book, the one from his locked drawer. All of it, or only Alon's part?”* · Chips: “All of it.” · “Only Alon's part.” |
| Reaktion | Alles: Wahrheit stärker, der Kommissar liest Don, Sandru und Casanova vor, Casanova: *“Yes. Me too.”* · Teil: Gemeinschaft stärker | |
| Schluss | | Kommissar: *“Thank you. We have what we need. Or we don't. You'll know tonight.”* |
| Übergang | Säulen (Abschnitt 7), W3 A setzt `akt3_festa`. | |

Ob der Funkspruch um drei Uhr als Beweis vorkommen darf, prüft die Story-Sitzung (Auflage: Pascal bleibt außerhalb der Fälle, F-26).

### 5.27 Tag 35, Nachmittag · `mo_frei_start` (gebaut) und *Last Page*

Bibis Tore wie gebaut. *Last Page* (Bibi, Leiter Stufe 4, gebaut für Tag 35 Abend) rückt direkt hinter `mo_frei_ende` in den Nachmittag, damit der Abend der Festa gehört.

### 5.28 Tag 35, Abend · `a3_festa` „The Festa“

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Piazza, das Festa-Bild. Ausstattung nach der Tafel. | Erzählerin: *Half the lights work. The tables are full anyway.* · oder *The whole bay is here. Even Kevin.* |
| Inhalt | Casanovas Rede, ihre Pause. Minicu hebt die Hände, sieht auf den leeren Platz neben der Kirchentür, wo Pascal immer stand, und wartet. | Casanova: *“Cala d'Orsu has stood on this rock for four hundred years. Pirates came. Tax men came. A man with a satellite came. And tonight...”* (Pause) |
| Wende | Zwei Takte Stille, dann Alva, langsam (Kanon). Minicu fällt als Erster ein. | Erzählerin: *Nobody claps. Then Alva does. Slowly. Minicu joins her first. Then everyone.* · Casanova: [sniff] *“...Thank you, Alva.”* · Alva: *“Don't get used to it.”* |
| Inhalt | mit `bl_kirche_casanova`: Jana kommt mit einer Bitte von den Kindern hinter der Kirchentür. | Jana: *“Madame, sorry, they want the end of the long story. The one from the church.”* · Casanova: *“...Later. I promise.”* |
| W3 A | `br_ehrenbuerger` (nicht Ende 1), `ab_casanova_flamenco`, `gv_rotes_kleid` in dieser Reihenfolge, mit neuem Fenster (W3) | |
| W3 B | dieselben drei als Beats von `a3_festa` | |
| Inhalt | Holms Mutter (Silhouette, Bestellung) sitzt neben Holm, Petru bringt zwei Gläser. | Holm: *“Mamma, this is Petru. He's the one who taught me to sit still.”* · Petru: *“Hm.”* |
| Inhalt | Die anderen Frauen, je eine Zeile im Festbild (ohne Leiter, ohne Echo) | |
| Mitternacht | **Der private Moment an der Mole** mit der Gewählten (5.21), dann das Ende (Abschnitt 7). | z. B. Chiara: *“Ten. That's a ten, First Officer. Don't let it go to your head. ...Let it go to your head a little.”* |
| Epilog (Nacht) | Minas Einschreiben, Pascals Tür, niemand macht auf (Kanon). | Mina: *“Sign here.”* · Erzählerin: *Nobody is there. It's the first letter she can't deliver.* |

## 6. Romanzen fertig spielen

Je Frau eine Schluss-Szene zwischen Tag 24 und 32 (vor Monaco und Villa), Bedingung: die Stufe-5-Szene ihrer Leiter. Zwei sind Expeditionen mit Rastplatz-Szene (OFFEN.md, Duc 02.11.). Jede beginnt mit einem Rückbezug mit Erinnerung, aus ihrer Belagerungs-Nacht oder ihrem Abend (`bl_will_ab_<pid>`, `bl_ab_fertig_<pid>`), oder aus ihrer Leiter, wenn es keine gab. Zwei Belagerungs-Nächte (`bl_na_fertig_<pid>`) setzen den Status „zusammen“ (Folge `fakt`).

### 6.1 Chiara · „Blackout“ (Deutung von `chiara.md:43`, Character Design prüft, F-18)

| Beat | Zeilen |
|---|---|
| Ansage | Brücke (W1 auf Grund: erste Probefahrt nach dem Heben; sonst Funktest am Kai). Der Strom fällt aus, alles dunkel. |
| Inhalt | Rückbezug: *“The night in the siege, on the bridge wing, when I rated the sky because I'd run out of things to count. It was a six.”* · mit `bl_verband_chiara`: *“And you gave me the good bandage. I never said thank you. I'm not saying it now either.”* |
| Handlung | Chiara, leise: *“First Officer. I don't know which breaker it is. What would you do?”* (Romanze über Gefragtwerden) · Chips: Holds the torch and lets her find it. · “The red one. Second row.” · “I don't know either. Let's find it together.” |
| Reaktion | Licht. Sie bewertet nicht. Erzählerin: *For once, she doesn't give it a number.* |

### 6.2 Alva · „The Board Is Full“

| Beat | Zeilen |
|---|---|
| Ansage | Bar nach Feierabend (nach dem Wiederaufbau oder wenn sie steht). Papas Tafel, frisch gewischt. |
| Inhalt | Rückbezug mit `bl_alva_runde`: *“The evening on the quay, in the siege, when I gave out free drinks and you said you'd pay the first round. You did. I wrote it down.”* |
| Handlung | Alva gibt ihm die Kreide: *“My name isn't on Papa's board. It never was. What do you write next to it?”* · Chips: Writes ALVA and, next to it, “stays”. · Writes ALVA and leaves the space next to it empty. · Gives the chalk back. “You write it.” |
| Reaktion | „Only you“ bleibt der Festa (Kanon). |

### 6.3 Lea · Expedition „One More Dive“ (2 Phasen)

| Beat | Zeilen |
|---|---|
| Ansage | Grottenmündung, ein Pirat zeigt den Weg (nach `a3_riscossore_kommt`). Rastplatz auf dem Felsen, der bei Ebbe eine Insel ist. |
| Inhalt | Rückbezug: *“Two fingers, side by side, the sign I showed you on the swim platform when the squid were up.”* |
| Handlung | Lea: *“The Azores letter is still in my bag. If I go, will you come and see me? Proper see me?”* (nicht bei „locker“) · Chips: “Yes. Dreckly, but yes.” · “Stay. The bay will need you.” · Holds up two fingers and says nothing. |
| Reaktion | färbt ihr Ende, ändert seine Regel nicht (Kanon *No Glow Tonight*) |

### 6.4 Sophia · „The Sixteenth Letter“

| Beat | Zeilen |
|---|---|
| Ansage | Mit Minas Post (wenn die Post steht): ein Brief von einem Verlag, der sechzehnte. |
| Inhalt | Rückbezug: *“Ten euros, the bet that you'd ask me what I actually want. You did ask. I still owe you the answer.”* |
| Handlung | Sophia: *“Darling, will you open it, or shall I?”* · Chips: Gives her the letter. “It's yours.” · Opens it and reads the first line out loud. · Puts it in her notebook, unopened. “Later. Together.” |
| Reaktion | Der Inhalt bleibt offen bis zum Ende (Feinschliff Duc). |

### 6.5 Rosi · „Two Thirds“ (nach `a3_lot14`)

| Beat | Zeilen |
|---|---|
| Inhalt | Rückbezug: *“The night with the stopwatch, when nobody lost.”* Rosi und Duc bauen Unit-01s Arm neu, Stoppuhr, unentschieden. |
| Handlung | Rosi: *“Officer. If I say 'Captain' now, is that an insult or a promotion?”* · Chips: “A promotion. I'll take it.” · “Neither. Say Duc.” · Laughs and hands her the spanner. |
| Reaktion | „Captain“ fällt, wenn er es verdient (Kanon K1). Danzel schwärmt in einer Zeile dazwischen, wenn Ducs Begehren bei Rosi höchstens 3 ist (Kanon, schüchtern) |

### 6.6 Lola · „First Guest, Again“

| Beat | Zeilen |
|---|---|
| Inhalt | Ihre Hütte am Strand. Rückbezug: *“The night in the siege you said yes to the toastie, and it wasn't burnt. Not even a bit.”* |
| Handlung | Lola: *“Boss. If I cook for you here, will you sit down? Properly? No running off?”* · Chips: Sits down and puts his phone away. · “Only if you sit down too.” · “Can I help?” |
| Reaktion | Sie beendet einen ganzen Satz (Kanon). Danzel wie bei Rosi. |

### 6.7 Siri · „No Caption“ (nach `a3_siri_post`)

| Beat | Zeilen |
|---|---|
| Inhalt | Sonnenuntergang ohne Handy. Rückbezug: *“The sunset on the foredeck, when I told you I hadn't written my own caption since I was nineteen.”* |
| Handlung | Siri: *“If this was a photo, what would you write under it?”* · Chips: “Nothing. Some things don't need words.” · “Siri, in her own words.” · Takes her hand and doesn't answer. |

### 6.8 Bibi · Expedition „Mochi“ (2 Phasen, nur `kl_loewe_frei` und offene Station)

| Beat | Zeilen |
|---|---|
| Ansage | Macchia, Mochis Spur (Kanon E-106: in Akt 3 fangbar). Kampf mit Schlafgranate (gebaut), Rastplatz am Feuer. |
| Inhalt | Rückbezug: *“The night at the campfire with the three of us, when you said 'until every collar is off'. This is the last one.”* |
| Handlung | Bibi: *“He's asleep. Do I cut it, or do you? It's the last one.”* · Chips: “You. He's yours.” · “Together.” · Hands her the knife without a word. |
| Reaktion | *Last Page* an Tag 35 (5.27) |

### 6.9 Megan · „Off the Record“ (nur `megan_funke`)

| Beat | Zeilen |
|---|---|
| Inhalt | VIP-Kabine (W1: nach dem Heben, sonst Alvas Gästezimmer). Rückbezug: *“The night of the press release, when I told you not to say a word until I landed. You didn't.”* |
| Handlung | Megan: *“This stays off the record, First Officer. Can you do that?”* · Chips: “I already did, Mac.” · “Only if you call me Duc.” · Nods and closes the door. |
| Reaktion | Am Morgen Outfit `megan_morning_after`. Nie öffentlich (E-060). |

**Holm und Petru** (Kanon): Karte `a3_holm_petru` ab Tag 30, beide ab Vertrauen 3. Ingrid ruft an (Kanon): Holm: *“Ingrid. From the night before Bergen. She has a daughter.”* · Petru: *“Hm. Good.”* · Duc geht still weiter (*When you look back, the metre between them is gone.*) oder stört (*“Frankfurt. Go away.”* · Petru: *“Hm. Go away.”*).
**Ligeia:** keine Romanze. Mit `ligeia_freund` (gebaut, `ereignisse_grotte.py:483`) kommt an Tag 30 eine Flaschenpost: *“Sailor. They say the bay will be safe. I would like to sing at something that isn't a shipwreck.”* Mit `sirene_weg` (der Saphir liegt bei Riposte) eine Zeile mehr: *“And keep my stone safe. It has waited longer than you.”* Die Galionsfigur am Eingang des Schutzgebiets (Kanon) nur mit geborgener Margot.

## 7. Die Enden lesen den Akt

| Säule | Akt 3 zahlt ein über | Erfüllt, wenn (Vorschlag) |
|---|---|---|
| **Wahrheit** | Whites Einsatzplan, Kassenbuch „alles“, Siris Post, Sophias Notizen, Funk-Aufnahme und Mitschrift, Funkbuch, Nachtwache, Kiste, `mo_kommission` (`beweis_stand`), Adriens Fotos, Steuerchip, Red-Trio-Aussagen | 3 Beweise, oder 2 mit „alles“ |
| **Geld** | Margot geborgen (Kanon) und `a3_megan_wende` oder Yamamoto Bindung 5 | Margot und eins davon |
| **Gemeinschaft** | Zeugen, Kassenbuch „teil“, Baustellen fertig, Casanova Vertrauen, Geldkassette der Margot zurück (Kanon `enden.md`), Ruf ab 5 als Bonus | 5 Zeugen, oder 4 mit „teil“ |
| **Stärke** | Endkampf gewonnen oder Festnahme | `a3_alon_besiegt` oder `a3_alon_festgenommen` |

Sichtbar im Schlussbild: Ausstattung der Festa (Tafel), wer im Netz fehlt (Minicu schreibt seinen Namen selbst, schief; vorher gibt Duc ihm das Namensblatt zurück; Pascals Knoten leer, Don knotet ihn wortlos), wer nach Mitternacht an der Mole steht. Die Enden-Tabelle in `enden.md` bleibt. Buenaventura: Eco Tours nur bei freier Bucht, sonst „Pirate Experience“ (Kanon).

## 8. Register der Belagerungs-Flags

| Flag | Szene | Wirkung |
|---|---|---|
| `bl_tafel` | 5.6 | Megan: „My list. Six jobs.“ |
| `bl_verband_wolff` | 4.1 | Legion baut eine Stufe |
| `bl_verband_chiara` | 6.1 | Zeile in ihrer Schluss-Szene |
| `bl_verband_maxwell` | 5.15 | Verband als Glücksbringer |
| `bl_verband_duc` | – | bewusst ohne Wirkpunkt (Duc behielt ihn selbst, Welle 2 war die Folge) |
| `bl_funk_white`, `bl_funk_charly` | 5.26 | Beweise, Charlys Zeile |
| `bl_tueren_petru` | 2 (Tür), 5.1 | Tür ohne Mindestvertrauen; wirkt seit `fix-akt2-folgen` auch beim Rudern |
| `bl_tueren_lola` | 4.3 | *The Menu* kürzer |
| `bl_tueren_mina` | 5.5 | Minas Zeile, Tür ohne Post |
| `bl_batu_norden` | 2, 5.26 | Tür, Aussage „twice“ |
| `bl_nachtwache_*` | 5.25, 5.26 | Hof der Villa, Beweis je Person |
| `bl_nachtwache_niemand` | 5.12 | Holms Nachsatz |
| `bl_wache_gesehen` | 5.8 | Funkbuch |
| `bl_kirche_jana` | 4.3 | Kinderbilder |
| `bl_kirche_don` | 4.3, 5.26 | *The Bell* in einem Abend, „I was sober“; wirkt seit `fix-akt2-folgen` auch in Welle 5 und 6 |
| `bl_kirche_casanova` | 5.28 | Jana und die lange Geschichte |
| `bl_will_ab_<pid>`, `bl_ab_fertig_<pid>` | 6 | Rückbezug |
| `bl_will_ab_niemand`, `bl_will_na_niemand` | 5.6 | Holms Satz |
| `bl_will_na_<pid>`, `bl_na_fertig_<pid>` | 5.21, 6 | oben in der Liste, Status „zusammen“ |
| `bl_alva_runde` | 4.1, 6.2 | zweite Zeile auf Papas Tafel; wirkt seit `fix-akt2-folgen` auch in `bl_bar_runde` |
| `bl_minicu_duc_zuerst` | 5.4 | „You came first.“ |
| `bl_minicu_sag_es` | 5.9 | ein Satz mehr im Brief |
| `bl_minicu_gewartet` | – | bewusst ohne Wirkpunkt |
| `bl_blatt_gefunden` | 5.20, 7 | Handschrift, Namensblatt zurück |
| `bl_werkstatt_heil` | 4.1, 4.3 | keine Baustelle, *The Catch* sofort |
| `sophia_notizen` | 5.26 | Beweis |
| `siri_wartet` | 5.10 | Siri fragt Minicu, stärkerer Post |
| `siri_darf_posten` | 5.10 | „four seconds“ |
| `sirene_weg`, `ligeia_freund` | 6 | Flaschenpost |
| Rettungen, `tk_haus_geflickt_` | 4.1 | Vignette oder Stufe 1 |
| Rudern | 5.1, 5.26 | **neues Flag** `bl_dorf_rudert` (F-21) |
| `tk_yacht_weg` | W1 | drei Zweige |

## 9. Gags, Ton, Englisch, Tags

- **Gags** bis Tag 31, vorher Texte prüfen (Alon, Holm, Festa, „tomorrow“, Megan an Bord, Pascal, Maxwell Tag 30 bis 32, Yacht). Ab Tag 32 gagfrei.
- **Ereignis-Dichte:** Woche 4 auf Faktor 0,6, Woche 5 bei 0,45 (F-17).
- **Ton-Mischung (Ziel):** 35 % warm, 25 % komisch, 20 % ernst, 20 % frech.
- **Englisch:** Rückbezüge mit Erinnerung, Chips mit Rückbezug tragen sie selbst, Erzähltext im Präsens, keine seltenen Wörter ohne Not.
- **Turbo-Tags:** Das Drehbuch setzt Tags nur an den Stellen, an denen das Geräusch die Szene trägt. **Jede vertonte Zeile bekommt beim Bau mindestens einen Tag** in `stimme_tags.json` (CLAUDE.md), Paket F. Grund für die Reihenfolge: Tags hängen am endgültigen Wortlaut, und der ändert sich in Ducs Abnahme noch.

## 10. Brain Trust zu v2.1

**Sienna (Game Direction):** Jetzt zählt Woche 4 wirklich: Duc entscheidet, wo die Piraten anfangen, und damit, wer zuerst aussagen kann. Das ist eine Entscheidung mit Folgen, nicht nur Zeit. ✨ Gegenvorbild Mass Effect 3 bleibt, darum sitzt jeder Schweigende sichtbar am Kai.

**Aly (Tech):** Drei Dinge brauchen Code, bevor eine Zeile gebaut wird: der Festa-Schalter mit Tag, Phase und Ort (W3 A), die Reihenfolge von `mo_kommission` und `a3_kommission`, und `kern/aufbau.tag_vorbei` nur für angefangene Häuser. 🤓 Das Budget ist von Hand gerechnet, 23 bis 37 Phasen auf 34. Ohne Bot-Lauf glaube ich keiner Zahl über 30.

**Luise (Art & Story):** Der private Moment an der Mole ist besser als jede Festa-Begleitung, weil er die Romanze schützt und sie trotzdem in das letzte Bild stellt. 🥹 Kritik: W5 B nimmt Sandru den Moment, in dem Alva ihn trägt. Gegenvorschlag: Wenn Duc W5 B wählt, trägt Alva ihn trotzdem, aber aus einem anderen Grund, nur ohne die Schienen. Das wäre eine Frage an Character Design.

**Maelle (Producerin):** Preis: rund 38 Szenen, grob 700 Sprechzeilen, 8 Hintergründe, 10 Sprite-Wünsche. Fünf Weichen sind viel, aber vier davon sind kleine Ja/Nein-Fragen. 📋 Frage an dich, Duc: Entscheidest du W1 und W5 zuerst? Die beiden ändern die meisten Szenen.

**Sora (Spielerstimme / QA):** Minute 1: Petru tritt vor, und wenn ich gerudert habe, sagt er es. Gänsehaut. Minute 40: Ich entscheide, ob Rosis Lichter bernstein oder weiß leuchten, und ich weiß jetzt schon, dass ich beim zweiten Mal das andere nehme. 😂 Mitternacht an der Mole: Nochmal-Lust 5, und es ist heißer, weil es nicht vor dem ganzen Dorf passiert. 🔥

## 11. Bauplan (nach Ducs Ja)

| Paket | Inhalt |
|---|---|
| A · Kalender | Kalender bis Tag 35, Gags bis 31, Dichte je Woche, `bl_dorf_rudert`, Beta-Schluss nach `akt2_ende` aufheben, Branch `fix-akt2-folgen` vorher mergen |
| B · Woche 4 | 5.1 bis 5.12, Baustellen mit Wahl, Piraten nur an angefangenen Häusern, Dank-Szenen und Vignetten |
| C · Zeugen, Tafel | Liste, Türen, Haltungen, acht Auftrags-Szenen |
| D · Woche 5 | 5.13 bis 5.25, Villa als Frame-Kette, Endkampf |
| E · Romanzen | Abschnitt 6, zwei Expeditionen |
| F · Kommission, Festa, Enden, Stimme | 5.26 bis 5.28, Festa-Schalter (W3), Säulen, alle Zeilen mit Tags in `stimme_tags.json` |
| G · Tests | `test_akt3_kalender`, `test_zeugen`, `test_festa_tafel`, `test_akt3_events`, Bot-Lauf mit zwei Profilen vor Paket D |

## 12. Was aus jedem Befund wurde

### 12a. Gegenrede (G1 bis G19)

| # | Befund | Ergebnis |
|---|---|---|
| G1 | Sonnenbrille | eingearbeitet, keine Zeile nimmt sie ab |
| G2 | Rädchen privat | eingearbeitet: Dinner privat, Presse danach (5.25) |
| G3 | Kommission gegen `mo_kommission` | eingearbeitet: Kai, Besetzung, `mo_kommission` eröffnet (5.26) |
| G4 | Woche 4 voll | eingearbeitet: 6 gegen 16 Pflicht, 3,4 gegen 2,8 freie Phasen je Tag, Tag 27 frei, Tag 26 nur warm und komisch |
| G5 | Zeitbudget | eingearbeitet mit Phasen je Szene. **Nicht eingearbeitet:** Bot-Lauf, weil es noch keinen Kalender gibt (Bauplan G) |
| G6 | Wochentage | eingearbeitet |
| G7 | Petru am Tor | eingearbeitet, zwei Fassungen nach Rudern |
| G8 | Alva | eingearbeitet: „since last night“, Kirche statt Market |
| G9 | Rätselchips | eingearbeitet: jede Haltung überzeugt, keine Tür nach einem Chip für immer zu |
| G10 | Einkaufsliste, Post | eingearbeitet (4.3, 4.1) |
| G11 | Flags | eingearbeitet, jedes Flag in seiner Szene (Abschnitt 8 verweist) |
| G12 | Romanzen | eingearbeitet mit Beat-Tabellen (6) |
| G13 | Schwere Gipfel | eingearbeitet: nur Switched Off |
| G14 | Doppelungen | eingearbeitet: Applaus-Logik über Minicu, Kaffee-Szene gestrichen, *The Bell* mit Plan |
| G15 | Kanon- und Logikbrüche | eingearbeitet |
| G16 | Siris Post | eingearbeitet (5.10) |
| G17 | Säule Geld | eingearbeitet (5.17) |
| G18 | Englisch, Präsens | eingearbeitet: Erzähltext im Präsens, „warrant“, „dividend“, „phones home“, „breach“ ersetzt |
| G19 | Fragen vor Chips | eingearbeitet, auch 5.17, 5.19, 5.22 |

### 12b. Unabhängige Prüfung von v2 (30 Funde)

| # | Befund | Ergebnis |
|---|---|---|
| 1 | W3 A technisch unmöglich | eingearbeitet: W3 A nennt Fenster, Phase, Ort, F-22 |
| 2 | Yacht hat drei Zustände, Ersatzorte können brennen | eingearbeitet: drei Zweige, Ersatzreihe Kirche, Piazza, Kai |
| 3 | Baustellen laufen ohne Duc, Tür Stufe 2 gegen fertig | eingearbeitet: Piraten nur an angefangenen Häusern, Tür einheitlich mit der Dank-Szene |
| 4 | Don und Minicu nach einem Chip zu | eingearbeitet: zweite Tür, Karte kommt wieder |
| 5 | Präteritum, „warrant“ | eingearbeitet |
| 6 | Fragen vor Chips, nackte Namen | eingearbeitet |
| 7 | Woche 4 nur in der Zählung leicht, ernst, Dank-Szenen an Tag 24 | eingearbeitet: neue Verteilung, Vignetten Tag 25 bis 28 ohne Frage, Berichte auf Tag 29 |
| 8 | Sandru: tote Bedingung, Kanon-Konflikt | eingearbeitet: Zeile an `sandru_surren`, Weiche W5, F-24 |
| 9 | Totòs Kiste falsch herum | eingearbeitet (5.5) |
| 10 | Petrus Zeile | eingearbeitet, zwei Fassungen |
| 11 | E-060 | eingearbeitet: privater Moment nach Mitternacht, Bedingungen je Frau |
| 12 | Romanzen als Liste, falsche Rückbezüge, Last Page, Echos | eingearbeitet: Beat-Tabellen, Chiara und Sophia korrigiert, Last Page am Nachmittag, keine Echos |
| 13 | Aussagen ziehen Pascal hinein | eingearbeitet: Alva sagt, was sie sah, Nachtwache je Person, F-26 |
| 14 | Fragenliste und Register veraltet | eingearbeitet (Fragenliste, E-120) |
| 15 | hohle Flags, `sirene_frei` | eingearbeitet: `ligeia_freund`, `sirene_weg`, `siri_wartet` mit Minicu, Chiara, `bl_blatt_gefunden` ohne toten Zweig, Flags in den Szenen |
| 16 | Reihenfolge `mo_kommission` | eingearbeitet, F-25 |
| 17 | Budget optimistisch | eingearbeitet: 23 bis 37 auf 34, Bot-Lauf als Bedingung |
| 18 | Insel bei Ebbe, Eco Tours zu früh | eingearbeitet (5.14) |
| 19 | Applaus-Logik, Kaffee | eingearbeitet (5.28, Kaffee gestrichen) |
| 20 | Kinder im Bild | eingearbeitet: Chor nur zu hören, Jana bringt die Bilder |
| 21 | Turbo-Tags fehlen | **nicht im Drehbuch eingearbeitet:** Tags werden beim Bau je Zeile gesetzt, weil sie am endgültigen Wortlaut hängen (Abschnitt 9) |
| 22 | Rückbezüge ohne Erinnerung | eingearbeitet (Kassenbuch, Lea, Minicu) |
| 23 | Elsa an der Mole | eingearbeitet: sie hat den Stream gesehen |
| 24 | ★ und Deal | eingearbeitet (5.25, 5.26) |
| 25 | `HOLM_TAG` auf welchem Branch | eingearbeitet (Kopf, 5.12) |
| 26 | unklares Englisch | eingearbeitet: „these people“, „I'm gone“, „You're under arrest“, „Old Lady“ |
| 27 | Pascal „Lieutenant“, Don „Hm.“ | eingearbeitet |
| 28 | Zeugen sagen mehr, als sie sahen | eingearbeitet (Regel in Abschnitt 2, Zeilen in 5.26) |
| 29 | `{zeugen}` = 0, Maxwell, Holm in 5.8, Geldkassette | eingearbeitet |
| 30 | Megan in der Villa | eingearbeitet: Megan nicht im Plan, nicht im Keller |
