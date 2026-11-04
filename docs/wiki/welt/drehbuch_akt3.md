# Drehbuch Akt 3: „Who Saw It?“ · Tag 24 bis Tag 35 · Version 3.5

> Stand 04.11.2026 · Besitz: Brain Trust (Cloud-Sitzung, Branch `akt3-cloud`) · **Entwurf zur Abnahme durch Duc, nichts davon ist gebaut.**
> Version 3.5 baut auf v2.1 (`41ae2ac`) auf, die Prüfung von v3 ist eingearbeitet (Abschnitt 13b), dazu Ducs Entscheide vom Abend des 04.11. (E-124: Belagerung ohne Prozent, Freundschaften statt Paare; E-125: Baustoffe je Haus, Charlys Geld, zwei weitere Freundschaften, Sandrus Schiene erst in Akt 3; E-126: Bones statt Kevin, Charly und Danzel statt Charly und Rosi, Festa-Schalter; E-127: Charly und Danzel werden ein Paar) und setzt **Ducs Entscheide vom 04.11.2026** um (E-122, Abschnitt 1). Eingearbeitet: Gegenrede (`docs/uebergabe/drehbuch_gegenrede.md`, Branch `drehbuch-gegenrede`), Wiki gegen Code (`docs/berichte/wiki_vs_code.md`, Branch `wiki-vs-code`), Folgen der Belagerung (`docs/wiki/welt/akt3_folgen_belagerung.md`, Branch `folgen-belagerung`), Text-Audit (`docs/uebergabe/audit_text.md`, Branch `audit-text`), die Audits der anderen Sitzung (`docs/berichte/audits_zusammenfassung.md`, Branch `berichte-audits`) und die unabhängigen Prüfungen von v1, v2 und v3 (Abschnitt 13).
> **Code-Stand:** Akt 3 ab Tag 24, die drei Belagerungs-Aufträge und die Fenster der Auffangstation sind **zweimal** gebaut, auf `fix-akt2` (andere Sitzung, vollständiger, dazu die Taschengröße im Menü) und auf `fix-akt2-folgen` (diese Sitzung). Nur einer darf nach `master`. Empfehlung: `fix-akt2`. Dieses Drehbuch rechnet mit dessen Verhalten: Stahl aus Maschinen erst ab Tag 24, Dons Wahl gibt der Kirche ein Leben in Welle 6. **Falle:** Auf `fix-akt2` steht `HOLM_TAG` noch auf 22 (nur `fix-akt2-folgen` hat 24), das wird beim Merge nachgezogen (F-30).
> Spieltext Englisch, einfach, vertonbar, Erzähltext im Präsens. Turbo-Tags siehe Abschnitt 10.

## 0. Feste Vorgaben

| Vorgabe | Wie Version 3 sie einhält |
|---|---|
| Akt 3 = Tag 24 bis 35 | Kalender ab Tag 24, im Code gebaut (Branch `fix-akt2`) |
| Duc trägt **immer** die Sonnenbrille | keine Zeile, kein Chip nimmt sie ab, Nähe über Haltung |
| Kommission passt zu `mo_kommission` | Tag 35, Phase „tag“, Kai, Klapptisch, zwei Männer aus Ajaccio, ein Schreiber, `mo_kommission` eröffnet die Kette (5.25) |
| Woche 4 atmet | 6 Pflicht-Events, Tag 27 ganz frei, 3,4 freie Phasen je Tag. Woche 5: 16 Pflicht, an Tag 29 bis 34 2,8 freie je Tag |
| Romanzen fertig spielen | Abschnitt 6 (je Frau eine Schluss-Szene). Abschnitt 7: fünf Freundschaften zwischen Yacht und Dorf |
| Ungelesene `bl_`-Flags | jedes mit Wirkpunkt in seiner Szene, Register in Abschnitt 9 |
| Romanzen privat (E-060) | private Momente nach Mitternacht, Paar-Neckereien nur über Tratsch, den das Spiel zeigt |

## 1. Ducs Entscheide (04.11.2026) und die eine Weiche

| | Entscheid | Wie es im Drehbuch wirkt |
|---|---|---|
| **a · Yacht** | „Verloren“ in der Belagerung (`tk_yacht_weg`) heißt **schwer beschädigt**. Rosi und die Eden Group reparieren sie, mit schwarzem Humor (*sie haben es ja schon in Akt 1 geschafft*). Nicht zerstört: nur kleine Reparatur-Events mit denselben Figuren. Witzig und wholesome. **Yacht-Gags erst ab Tag 25**, Tag 24 gehört Buenaventuras Entschuldigung | 4.4 „The Yacht“: zwei Fassungen, Reparatur bis Tag 31, Probefahrt Tag 32 |
| **b · Wohnen** | Während der Reparatur schläft die Crew in der Kirche, bei Alva und bei anderen Dorfbewohnern | 4.4, Tabelle „Wer schläft wo“. Die Unterkünfte tragen zugleich die Paare aus Abschnitt 7 |
| **c · Minicu** | schwer verletzt, sein Überleben erfährt der Spieler **erst zur Festa**, er überlebt **in allen Enden** | keine Minicu-Szene vor Tag 35. Die Tür zum Hinterzimmer der Kirche bleibt zu, Don sagt *“Not today.”* (nicht „Not yet“, das ist Pascals Funkspruch um drei Uhr). `dorf_figuren.md` (Minicu wacht auf, fragt ab Tag 23 nach Pascal, hilft beim Bau) bekommt einen Vermerk Er steht auf der Festa auf (5.27). Er sagt nicht aus. Er steht in jedem Schlussbild |
| **d · Festa-Aufträge** | Casanova vergibt Baumaterial für das Dorf, Essen und Schmuck. Jeder Dorfbewohner nutzt sein Talent. Jedes Los ist eine kleine Szene mit einer Person, **kein Zähler** | 4.3 „Die Lose“ |
| **e · Megan** | kommt zwei Tage nach der Belagerung zurück: **Tag 25** | 5.5 |
| **f · Eco-Idee** | Bibi bekommt ein eigenes Event. Ohne Bibi kommt die Idee von **Lea** | 5.12 |
| **g · Tauchgang-Fehlschlag** | nimmt nur den Weg „Margot“ der Säule Geld. Yamamoto Bindung 5 und Megans Wende bleiben erreichbar. Alles andere am Fehlschlag bleibt (Riposte weg, Galionsfigur am Strand, Lea geht auf die Azoren) | Abschnitt 8: Säule Geld hat drei Wege, einer reicht |
| **h · Paare** | fünf wholesome Ereignisse: Lola und Bà Tư, Chiara und Alva, Isabelle und Sophia, Mina und Lea, Holm und Petru. Je romanzierbarer Frau zwei Fassungen. **Präzisiert (E-124):** Die ersten vier lieben sich nicht im romantischen Sinn, sie verbringen Zeit miteinander und werden tief befreundet. Nur Holm und Petru sind eine späte Liebe (Kanon) | Abschnitt 7, mit Kanon-Prüfung je Paar |
| **~~Weiche W · 100 %~~ entfällt** (E-124) | Die Zahl „Alon … %“ fällt weg, sie war nur eine Planungshilfe (`belagerung.md` auf master, Abschnitt „Entscheid Duc 04.11.2026“). Jede Hilfe wirkt als sichtbarer Auftritt auf der Karte. **Akt 3 liest nie einen Gesamtwert** (auch nicht `werte.belagerung_prozent`), nur einzelne Flags: wer gekommen ist. Rückbezüge nennen Personen, nicht Zahlen | Register in Abschnitt 9 |
| *(alt, nur zur Nachverfolgung)* | **offen.** Definition steht (E-121): 100 % heißt, der Spieler hat nichts getan, um die Belagerung zu schwächen. Offen ist, wie schwer das ist. **Zweig A:** Balancing wie heute (Anfänger verlieren in Welle 3 rund 3 von 4 Häusern, die Yacht hält meist). **Zweig B:** 100 % wird härter (mehr verlorene Häuser, öfter `tk_yacht_weg`) | Akt 3 liest nur das Ergebnis: 0 bis 4 Baustellen und den Zustand der Yacht. Jede Szene funktioniert mit 0 und mit 4 abgebrannten Häusern und mit beiden Fassungen der Yacht |

**Noch an Duc (keine Weiche, mit Vorschlag gebaut, Fragenliste):** Festa-Schalter für die drei gebauten Festa-Events (F-22, Vorschlag: Fenster, Phase und Ort mitsetzen), Sandrus Schiene (F-24, Vorschlag: Switched Off in Akt 3, Schiene danach), Reihenfolge von `mo_kommission` (F-25).

## 2. Die Idee in einem Satz

Zwölf Tage lang baut Duc ein Dorf wieder auf, das ihn am ersten Morgen nicht mehr ansehen will, und am Ende zählt nicht, wie stark er ist, sondern wer bereit ist, laut zu sagen, was er gesehen hat.

**Das Motiv:** *Who saw it?* Akt 2 fragte, wer die Linie hält. Akt 3 fragt, wer es gesehen hat und es sagt. Alon droht nicht mit Gewalt, sondern mit Papier: Jobs, Kredite, Anwaltsbriefe. Gegen Papier hilft nur ein Name, laut gesagt. Das Fischernetz am Ende ist die Liste dieser Namen.
**Der zweite Faden:** Wer gerade kein Dach hat, schläft bei jemandem. Aus diesen Nächten wachsen Freundschaften, nicht nur bei Duc. **Zum ersten Mal wächst die Yacht mit dem Dorf zusammen:** In Akt 1 hat das Dorf die Yacht geduldet, in Akt 2 haben beide zusammengearbeitet, in Akt 3 werden sie eine Gemeinschaft (Duc, E-124).
**Die offene Frage des Akts:** Lebt Minicu? Die Tür zum Hinterzimmer der Kirche bleibt zwölf Tage zu.

**Was Duc weiß (eine Fassung):** Ducs Firma gehört zur Eden Group. Dass die Gruppe das Hafenviertel heimlich verkauft hat und an wen, wusste er nicht (E-001, E-003). Kern: *“My company belongs to the Eden Group. I didn't know they sold your harbour, or who bought it.”*

**Zeugen sagen nur, was sie selbst gesehen haben.** Wer bezahlt hat, belegen das Kassenbuch, Riscossores Buch und Buenaventura.

| Wer | Was er gesehen hat | Was ihn schweigen lässt | Seine Tür (4.2) |
|---|---|---|---|
| Petru | die Fackeln an seiner Werkstatt, mit Rudern auch die Boote | A.V. hat den Kredit auf sein Boot gekauft | Dank-Szene der Werkstatt, oder `bl_tueren_petru` |
| Mina | jede Tür an dem Tag ohne Telefon (Tag 22) | sie stellt die Drohbriefe selbst zu | Dank-Szene der Post, oder `bl_tueren_mina` |
| Bà Tư | die Männer in Weiß, die zweimal nach dem Nordweg fragten | Alons Arbeiter sind ihre Kunden | `bl_batu_norden`, oder Dank-Szene des Ladens |
| Alva | die offene Nordbarrikade | sie war bewusstlos, man glaubt ihr nicht | Dank-Szene der Bar |
| Sandru | wer Alva aus den Trümmern trug | seine Beine gehören A.V. | Schiene (5.19) |
| Don Anghjulu | das offene Tor | Dach und Beichtgeheimnis | an seiner Seite an der Tür, oder Vertrauen 3, oder das Los *The Bell* begonnen |
| Casanova | das Papier, das jede Nacht auf ihren Kirchenstufen lag (sie hat es aufgehoben) | ihre Schuld am Elternhaus | Elsas Berichte gehört (5.11) |
| Buenaventura | wer ihn bezahlt hat | **nichts**, ihm glaubt nur keiner | meldet sich selbst (5.2) |

Minicu steht nicht auf der Liste (Entscheid c). Pascal steht nie darauf (Auflage der Story-Sitzung).

## 3. Kalender und Bogen

**Wochentage:** Tag 14 war Sonntag, also sind 21, 28 und 35 Sonntage, Tag 24 ist ein Mittwoch.
**Phasen:** Karten (echte Zeit) gibt es in Tag, Nachmittag, Dinner, Abend. Frühstück und Nacht zählen nicht.

### Woche 4 · „The Morning After“ (Mi 24 bis So 28)

| Tag | Frühstück | Tag | Nachmittag | Dinner | Abend | Pflicht | frei |
|---|---|---|---|---|---|---|---|
| **24** Mi | `a3_morgen` | `a3_schwur` | frei | frei | frei | 2 | 3 |
| **25** Do | `a3_uhr` | frei | frei | `a3_megan_landet` (mit der Bilanz der Yacht) | frei | 2 | 3 |
| **26** Fr | `a3_festa_tafel` | frei | frei | frei | frei | 1 | 4 |
| **27** Sa | Vignette | frei | frei | frei | frei | **0** | 4 |
| **28** So | Vignette | `a3_sonntag` (Messe, Don an der Tür, Schublade) | frei | frei | frei | 1 | 3 |

**6 Pflicht, 17 freie Phasen.** Vignetten (keine Phase) hängen als Nachsatz an das Frühstück, auch an ein Pflicht-Frühstück: je Morgen eine, Vorrang Dank-Szene eines Hauses, das nicht brannte, dann Reparatur der Yacht (4.4). Dazu an jedem Morgen von Tag 25 bis 34, außer Tag 26 (da sitzt er auf Casanovas Tafel), eine Zeile der Erzählerin: *Kevin is on the church roof again. He hasn't moved.* So vergisst niemand Minicu. Ab Tag 25 laufen die Yacht-Gags im Zufallspool. Die fünf Paar-Ereignisse (Abschnitt 7) beginnen ab Tag 26.

### Woche 5 · „Name Your Price“ (Mo 29 bis So 35)

| Tag | Frühstück | Tag | Nachmittag | Dinner | Abend | Pflicht | frei |
|---|---|---|---|---|---|---|---|
| **29** Mo | `a3_bibi_idee` oder `a3_lea_idee` | frei | frei | frei | `a3_berichte` | 2 | 3 |
| **30** Di | `a3_maxwell_flug` | frei | frei | frei | frei | 1 | 4 |
| **31** Mi | frei | frei | frei | `a3_megan_monaco` | frei | 1 | 3 |
| **32** Do | `a3_probefahrt` (nur wenn die Yacht schwer beschädigt war) | frei | `a3_switched_off` | frei | frei | 1 | 3 |
| **33** Fr | `a3_einladung` (+ `a3_schiene`) | frei | frei | frei | `a3_nach_mitternacht` | 2 (3) | 3 |
| **34** Sa | `a3_villa_plan` | `a3_villa_keller` | frei | `a3_villa_dinner` | `a3_villa_ende` | 4 | 1 |
| **35** So | frei | `a3_kommission` mit `mo_kommission` | `mo_frei_start`, *Last Page* | Vorbereitung (Vignette, keine Wahl) | `a3_festa` | 5 (mit Ende) | 0 |

**16 Pflicht (17 mit Schiene), 17 freie Phasen.** Gags bis Tag 31, ab Tag 32 gagfrei. Switched Off liegt auf Tag 32, dem ersten Tag ohne Gags. Die Probefahrt am Morgen von Tag 32 ist kurz und warm, damit der schwere Nachmittag aus der Ruhe kommt.

### Spannungsbogen

| Tag | Szene | Spannung |
|---|---|---|
| 24 | Morgen danach, Schwur | 6 → 3 |
| 25 | Uhr, Megan und die Yacht | 5, dann 3 (schwarzer Humor) |
| 26 bis 27 | Tafel, Lose, Paare | 2 bis 1 |
| 28 | Sonntag | 4, ein leiser Fund |
| 29 | Idee, Berichte | 3 |
| 30 bis 31 | Maxwell, Monaco | 3 bis 6 |
| 32 | **Switched Off** | 8 → 4, der eine schwere Moment |
| 33 | Einladung | 6 |
| 34 | **Villa** | 9 → 10, Spannung und Aktion |
| 35 | Kommission, Festa, Minicu | 7, dann 10 → 2 |

### Zeitbudget (von Hand, Bot-Lauf nach dem Bau)

Freie Kartenphasen Tag 24 bis 34: **34**.

| Bedarf | Phasen | |
|---|---|---|
| Baustellen | 2 bis 4 | Duc setzt je Haus den ersten Stein |
| Zeugen | 2 bis 3 | vier in Dank-Szenen ohne Phase, je eine Phase Don, Casanova, Sandru (nur wenn ohne Dank-Szene) |
| Lose | 6 bis 8 | ein Spieler schafft etwa die Hälfte der 13 Lose |
| Romanzen | 2 bis 6 | je Frau eine Szene, zwei Expeditionen kosten 2 |
| Paare | 0 | die fünf Paar-Ereignisse kommen im Pool ohne Phase, Ducs Wahl ist Teil des Ereignisses |
| Freie Dates | 2 bis 4 | |
| Kleine Szenen | 5 bis 9 | Alva 1, Siri 1, Revanche 1, Riscossore 1, Lot 14 1, Nonna 1, Mochi 1 bis 2, Scrap Field 2 |
| **Summe** | **19 bis 34 von 34** | Ein Spieler mit einer Romanze und allen Zeugen braucht etwa 26 bis 29 |

## 4. Die Mechaniken

### 4.1 Die Baustellen („Lend a Hand“)

- **Fundament:** `kern/aufbau.py` (gebaut, laut Wirkpunkt-Audit noch **nicht** in `eden.py` eingehängt, Paket B).
- **Duc entscheidet, wo gebaut wird:** Die Piraten tragen je Tag eine Stufe, aber nur an Häusern, an denen Duc den ersten Stein gesetzt hat (Änderung an `aufbau.tag_vorbei`, Paket B). Das ändert `akt3.md` (dort bauen sie von selbst), Duc hat es bestätigt (E-123, 04.11.).
- **Jedes Haus braucht eigene Baustoffe** (Duc, E-125). Damit führt jedes Haus zu einer anderen Mechanik, statt alle dieselbe Liste zu fordern. Heute hat `kern/aufbau.STUFEN` für alle Häuser dieselben drei Stufen, das wird je Haus aufgeteilt (Paket B). Vorschlag, je drei Stufen:

| Haus | führt zu | Stufe 1 | Stufe 2 | Stufe 3 (öffnet das Haus) |
|---|---|---|---|---|
| Post (Mina) | Macchia, Korkeiche (Pinnwand und Postfächer) | 4 Timber | 3 Slate, 2 Cork | 2 Cork, 2 Iron |
| Bà Tưs Laden | Steinbruch, Granitfels (der Herd) | 3 Timber, 2 Granite | 3 Slate | 4 Granite, 1 Iron |
| Alvas Bar | Angeln, Strandgut (Treibholz, Rusty Chain) | 4 Timber | 2 Timber, 2 Slate | 3 Iron |
| Petrus Werkstatt | Kampf, Stahl (Scrap Field oder Villa) | 5 Timber | 2 Timber, 3 Slate | 2 Iron, 2 Steel |

- **Grenzen:** Bauen bleibt „alles oder nichts“ wie bei den Ställen (`kochen.md`), die Baustellenkarte zeigt nur die **nächste** Stufe eines Hauses, jeden Posten grün oder rot. Ohne Charly bleiben die vollen Kosten, kein Satz erinnert an die verpasste Hilfe. Nonna verkauft Timber, Slate und Iron mit Tagesvorrat (6/6/2), Granite und Cork nur selbst abgebaut, Steel nur von Maschinen. Ein Bauen-Los (4.3) ersetzt eine ganze Stufe.
- **Charlys Geld** (Duc, E-125): Nur wenn Charly geblieben ist (`rt_charly_bleibt`, nicht `rt_charly_weg`). Sie holt heimlich Geld vom Konto ihrer Mutter (Ravenel Défense macht Geschäfte mit Alon) und gibt es Casanova. **Wirkung:** Ab dann kostet jede noch offene Stufe 20 % weniger, je Posten abgerundet, mindestens 1 (aus 4 Timber werden 3, aus 2 Iron wird 1, aus 1 bleibt 1). Flag `a3_charly_geld`, Wirkpunkt in `aufbau.braucht`. Szene 5.28.
- **Karte „Lend a Hand“** (1 Phase), mit Wahl: Wer hält mit? Der Besitzer (eine Zeile über sein Haus), ein Pirat (eine Zeile über das, was er angezündet hat) oder ein Crew-Mitglied (Zeit zusammen).
- **Die Legion** mit `bl_verband_wolff` baut einen Tag lang mit. Wolff: *“You gave me the good bandage, the only one. The Legion pays its debts.”*
- **Fertig** → Dank-Szene `a3_dank_<id>`, dort öffnet die Zeugen-Tür, die Frage kostet keine Phase:

| Haus | Dank-Szene | Wirkpunkt |
|---|---|---|
| Post | Mina hupt zweimal am Kai, die erste Post nach dem Brand ist keine Rechnung | Mina bringt einmal am Tag eine Zutat oder ein Material aus Bastia (Wahl aus drei) |
| Bà Tưs Laden | zwei Teller, auch einer für Lola | Kochen mit Bà Tư (★★), Akzent „Ăn đi“ (+10 % Leben bis zum Dinner des Folgetags) |
| Alvas Bar | der erste neue Name auf Papas Tafel, mit `bl_alva_runde` darunter *“Everyone. Paid. D.”* | Bar-Abende, Alvas Los |
| Petrus Werkstatt | das Ruder über der Tür, heil oder verkohlt | Angeln vom Boot, Petrus Los |

- **Nicht abgebrannt:** Dank-Szene als Frühstücks-Vignette (Tag 25 bis 28, je eine), ohne Frage. Gefragt wird später mit der Karte „Ask <Name>“.
- **Die Kirche** ist keine Baustelle, das Dach tropft bis zum Ende, nur Ende 3 und ★ reparieren es (E-096).

### 4.2 Die Zeugen („Who Saw It?“)

- **Auslöser:** `a3_uhr` (Tag 25), Codex-Seite „Witnesses“ mit Bild, Angst und Tür als Satz.
- **Jede der drei Haltungen überzeugt**, sie färbt nur die Aussage und gibt Vertrauen (+2, die passende +6). Keine Tür bleibt nach einem einzigen Chip für immer zu.
- Wessen Tür bis Tag 34 zu bleibt, sitzt am Kai am Rand, sein Name fehlt im Netz.
- Ergebnis `a3_zeuge_<id>`, Haltung `a3_zeuge_<id>_<h>`. **Dorf-Vertrauen wird damit endlich gelesen** (Wirkpunkt-Audit: Vertrauen von Pascal, Mina, Sandru, Minicu steigt in 29 Folgen und wird nirgends abgefragt): Vertrauen 3 öffnet Türen, und die Zahl der Zeugen bestimmt, wie viele Gäste im Festbild sitzen.

### 4.3 Die Lose (Entscheid d: „THIS. IS. THE. FESTA!“)

**Vorbild:** Stardew Valley, Spiritfarer. **Gegenvorbild:** Einkaufslisten. **Kein Zähler, keine Mengen.**

- **Auslöser:** `a3_festa_tafel` (Tag 26). Casanova hängt eine Tafel an die Kirchenmauer mit **13 Losen in drei Spalten: Bauen, Essen, Schmuck.** Jedes Los trägt einen Namen und ein Talent: *“Petru · wood · a table for the whole village”*. Acht Lose hängen ab Tag 26, die übrigen fünf nach dem ersten fertigen Haus. *Capra* (Bibi) ist ein Bonus-Los ohne Platz auf der Tafel: Bibi kommt damit von selbst, wenn die Station offen ist.
- **Kosten:** jedes Los genau eine Phase. Zugang statt Menge: *The Lights* hängt erst, wenn Duc das Scrap Field oder die Villa gesehen hat (Stahl), kein Zähler.
- **Ein Los ist eine Szene** (1 Phase) mit genau einer Person, die ihr Talent zeigt, und **einer Entscheidung**. Material gibt die Person selbst. Duc hilft mit, nicht mit Zahlen.
- **Wirkung:** `a3_los_<id>` stellt ein Ding ins Schlussbild, **so, wie Duc es entschieden hat**. Bauen-Lose helfen zugleich dem Dorf: Sie geben einer Baustelle eine Stufe, wenn eine offen ist.
- Ein Spieler schafft etwa die Hälfte. Was fehlt, fehlt sichtbar und leise (ein leerer Tisch, eine dunkle Gasse), nie mit einer Zahl.

| Spalte | Los | Person und Talent | Frage und Entscheidung | Ins Schlussbild (und fürs Dorf) |
|---|---|---|---|---|
| Bauen | **The Long Table** | Petru, Holz | Petru: *“Hm. The wood from my old boat, or from the burned houses?”* · altes Boot (er gibt etwas her) · Balken aus dem Brand (die Asche wird ein Tisch) | die lange Tafel. Gibt der Werkstatt oder einer anderen Baustelle eine Stufe |
| Bauen | **The Stage** | Buenaventura und seine Männer, Steine tragen | Buenaventura: *“Señor, where do we build it? Where the fire was, or where the people are?”* · auf dem Platz vor der Post · vor der Kirche | die Bühne mit der purpurnen Flagge. Gibt der Post eine Stufe |
| Bauen | **The Lights** | Rosi, Technik | Rosi: *“What goes in the switch, Officer?”* · ein Chip von Duc (echter Verlust, weißes Licht) · ein Teil aus Alons Halsbändern (bernstein wie Unit-01s Auge) | Lichterketten. Zugang nach Scrap Field oder Villa. Rosi gefeuert: Maxwell und Rosi per Video, wie in 5.19 |
| Essen | **Not in the System** | Sandru, das Brett mit den Rezepten seiner Mutter (Gazellenhörnchen, Chebakia, die Blechdose, Kanon) | Sandru: *“Ha. My mother's tin. Do I sell these at the market, under Alon's sign, or only here?”* · im A.V. Market (Risiko für ihn) · nur auf der Festa | ein Tisch mit marokkanischen Süßigkeiten. Mit „Market“ ein Satz in Switched Off: *“They found the tin.”* |
| Essen | **The Pot** | Bà Tư, kocht zu viel (Kanon) | Bà Tư: *“My way, or your mother's way, con?”* · beide gelingen | der Topf, eine Schlange davor |
| Essen | **The Garden** | Nonna und Isabelle, Garten und Kräuter | Nonna: *“Who gets the first basket?”* · die lange Tafel · Bà Tưs Topf · Frederico (nur wenn er lebt) | Körbe mit Kräutern |
| Essen | **The Menu** | Lola, kochen | Lola: *“Who tastes it first, Boss?”* · Bà Tư · Casanova · Duc | Lola am Grill. Mit `bl_tueren_lola`: *“I've been in every kitchen in this village, Boss. Mostly the biscuits.”* |
| Essen | **The Catch** | Buenaventuras Männer auf *The Eventually* (Kanon: er beliefert die Festa), fischen | Buenaventura: *“The reef, the grotto or the open sea?”* · Riff (viele kleine) · Grotte (nur `a3_riscossore_kommt`) · offenes Meer (ein großer Fisch, Angeln-Probe von Duc) | der Grill am Hafen |
| Essen | **The Festa Drink** | Alva, die Bar | Alva: *“Papa's recipe, or a new one? You choose the name if it's new.”* · Papas Myrte · neues Getränk (Duc gibt ihm einen Namen aus drei) | das Getränk auf jedem Tisch |
| Schmuck | **The Dresses** | Danzel, Schneider (liest endlich `danzel_festa_auftrag`) | Danzel: *“Whose dress first? I can only finish one in time!”* · eine der Frauen · Casanova | ein Kleid im Schlussbild. Mit `chiara_festa_kleid` ist Chiaras schon fertig, die Wahl geht an eine andere |
| Schmuck | **The Garland** | Mina, Briefe | Mina: *“I've got a box of post nobody can deliver. Shall I hang it up?”* · ja, alles (auch die Umschläge nach Monaco in der sorgfältigen Hand) · ja, aber ohne Pascals Post · nein, Blumen | eine Girlande aus Briefen über der Gasse |
| Schmuck | **The Bell** | Don, die Glocke | ein Abend Karten statt Wein. Don: *“Shall I win tonight, my son, or will you?”* · Plays to win. · Lets him win. · “Nobody wins. We play until the bell is fixed.” | die Glocke läutet zum Tanz im richtigen Takt. Mit `bl_kirche_don`: *“You let me stay sober once already, at the church door. Twice is a habit.”* |
| Schmuck | **The Pictures** | Jana und die Kinder hinter der Kirchentür (nur `bl_kirche_jana`, ohne Phase) | Jana: *“Sir, they made these for the festa. Where do I hang them?”* · an die Kirchentür · an die Bühne | Bilder an der Tür. Kein Kind im Bild (Kanon) |
| Bonus | **Capra** | Bibi, Tiere (nur Station offen, ohne Phase) | Bibi: *“Capra wants to come. Do we let her?”* · ja (sie frisst ein Kleid an) · nein | eine Ziege mit Blumenkranz |

Die Konfettikanone fehlt, Pascal hatte sie bezahlt (Kanon). In Ende 1 ist sie wieder da.

### 4.4 Die Yacht (Entscheid a und b)

**Zwei Fassungen nach der Belagerung**, beide witzig und wholesome. Yacht-Gags erst ab Tag 25.

| Zustand | Was passiert | Wer schläft wo |
|---|---|---|
| **Schwer beschädigt** (`tk_yacht_weg`) | Tag 25 Dinner: Megan sieht die Bilanz (5.5). Rosi und die Eden Group reparieren (Rosi gefeuert: Maxwell und Rosi per Video, wie 5.19). Die Eden Group schickt aus Monaco Kisten mit Ersatzteilen und eine Hotline mit Wartemusik (keine neue Figur im Bild, nur Stimme). Kleine Szenen im Pool Tag 25 bis 31, fertig am Abend von Tag 31. Tag 32 morgens: Probefahrt im Hafen | Kirche (vorne, das Hinterzimmer bleibt zu): Duc, Maxwell, Jana, Totò, Yamamoto, Siri, Yasin · bei Alva: Chiara · bei Bà Tư: Lola · im Kloster bei Nonna: Sophia · bei Mina: Lea · bei Petru: Holm · Rosi schläft auf der Yacht im Maschinenraum (*“Somebody has to listen to her at night.”*) · Megan: Casanovas Gästezimmer (ihr komisches Bündnis, Kanon) |
| **Nicht zerstört** | Kleine Reparatur-Events im Pool ab Tag 25 (Rosi, Maxwell, Totò, dieselben Figuren; Maxwell nicht an Tag 30 bis 32). Alle schlafen an Bord | an Bord wie gewohnt. Die Paare aus Abschnitt 7 treffen sich dann tagsüber im Dorf |

**Gastgeber ohne Haus:** Ist das Haus eines Gastgebers abgebrannt (`tk_haus_weg_bar`, `_batu`, `_post`, `_werkstatt`), schläft der Gast mit dem Gastgeber im Notquartier vorne in der Kirche, bis das Haus steht. Das Paar-Ereignis spielt dann am Notquartier (Feldbett, Kerze, Kaffeekocher). Gefeuerte Frauen (`gefeuert_<pid>`) schlafen nicht bei Gastgebern, ihr Paar-Ereignis entfällt (Holm und Petru sind nie betroffen).
**Maxwell** fehlt Tag 30 bis 32: Alle Pool-Events mit ihm schließen diese Tage aus.

**Schwarzer Humor, Beispiele (ab Tag 25, Zufallspool, je eine Minute):**
- Rosi zu Megan, Tag 25: *“Don't worry. We fixed her once already, after the explosion. Twice is a tradition.”* · Megan: *“How... reassuring.”*
- Eden-Hotline auf Lautsprecher: *“Thank you for calling Eden Fleet Services. Your yacht is important to us.”* (Wartemusik, sehr lang) · Rosi: *“Eleven minutes. I'm timing it.”*
- Totò mit einer Kiste: *“Comandante! The Eden Group sent us one propeller. One. We have two.”* · Rosi: *“Then we're half finished.”*
- Maxwell trägt eine Tür (nicht Tag 30 bis 32): *“Mr. Maximum has found a door. He does not know where it goes.”* · Rosi: *“The sea. It goes in the sea.”*
- Tag 31, Rosi klopft auf den Rumpf: *“She's ugly, she leaks a bit, and she floats. Don't tell her I said ugly.”*

**Probefahrt** (`a3_probefahrt`, Tag 32 Frühstück, nur bei schwerer Beschädigung): Holm auf der Brücke, eine Runde im Hafen. Holm: *“Frankfurt. Ready to see if she still swims?”* · Chips: Stands next to Holm on the bridge. · Goes down to Rosi in the engine room. · “After you, Captain.” · Ergebnis: Die Crew zieht zurück an Bord. Holm: *“Takk, Rosi.”* · Rosi: *“Don't. I'll cry, and then the engine cries.”* Chiaras Schluss-Szene „Blackout“ (Abschnitt 6) spielt auf dieser Fahrt.

## 5. Die Szenen

Jede Szene: **Ansage → Inhalt → Handlung → Reaktion → Übergang**, Titelkarten mit Continue und Skip, ernste Szenen mit ernsten Posen, vor jedem Chip eine klare Frage, Chips zuerst als Handlung im ganzen Satz. **Marotten sparsam** (Stimmen-Audit): Petrus „Hm.“ und Maxwells „Mr. Maximum“ höchstens einmal je Auftritt, Holm sagt immer „Frankfurt“, Totò „Comandante“.

### 5.1 Tag 24, Frühstück · `a3_morgen` „The Morning After“ (ernst → warm)

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Titelkarte *Day 24 · The Morning After*. Piazza, Rauch über der Post (mit `tk_haus_weg_post`). Die Kirchentür ist offen, die Tür zum Hinterzimmer zu. Lola gefeuert: ihre Zeile spricht Bà Tư (*“Eat. Everybody eat. I made too much.”*) | Erzählerin: *The village spends the night in the church. Nobody sleeps much. The door to the back room stays shut.* |
| Inhalt | Duc mit zwei Kaffeebechern. Die Leute gehen auseinander. Alons Clip läuft auf einem Handy. | Mina, leise: *“Sorry, Yacht. I don't know what to say to you today.”* · Erzählerin: *A man near the fountain asks it out loud: “Did you know?”* |
| Handlung | | Chips: Puts both coffees down on the fountain. “My company belongs to the Eden Group. I didn't know they sold your harbour.” · “No. And I'm staying until you believe me.” · Stays where he is and says nothing. |
| Reaktion | Petru tritt vor ihn. Mit Rudern (`bl_dorf_rudert`, neues Flag F-21; die Türen mit Petru, `bl_tueren_petru`, senken nur die Schwelle dafür): | Petru: [clear throat] *“Hm. I rowed out with the village, like in 1924, and he held the church until we came back. Three days. That's all I need to know.”* |
| Reaktion | Ohne Rudern: | Petru: [clear throat] *“Three days he stood between the fire and the church. That's all I need to know.”* |
| Inhalt | Jana fragt, was alle fragen. | Jana: *“Sir... Minicu. Is he... nobody will tell me.”* · Don, an der Kirchentür: [sigh] *“Not today, my child. Pray, and leave the door shut.”* |
| Reaktion | | Lola, zu laut: *“Right! Who wants breakfast? I made heaps. Mostly the eggs.”* |
| Übergang | Karte „Visit Alva“. Ziel-Zeile: *Buenaventura has asked the whole village to meet at the harbour.* | |

**Keine Yacht-Gags an Tag 24** (Entscheid a).

### 5.2 Tag 24, Tag · `a3_schwur` „The Oath“ (komisch → ernst → warm)

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Hafen, *The Eventually*, Flagge auf halbmast. | Erzählerin: *Forty men stand on the quay. None of them is holding a torch.* |
| Inhalt (Kanon: Fernseh-Moment) | Ein Pirat hält ein Handy hoch: „pirates attacked a small village“. | Buenaventura: [laugh] *“I am famous! Look, Paco, that is our flag!”* · *“...Robots? I have never owned a robot in my life. They are saying I had robots!”* |
| Inhalt | Hut ab. | Buenaventura: [clear throat] *“We burned your houses. I gave the order to stop, and I gave it too late. I am sorry.”* · *“I don't know how a man makes that right. I have a flag, an anthem and forty men who can carry stones. We will find a way. I swear it.”* |
| Reaktion | | Casanova: *“You burned the post office.”* · Buenaventura: *“Yes, Madame.”* |
| Handlung | | Buenaventura: *“You beat me twice, Señor. So you decide. Do we stay and carry, or do we sail?”* · Chips: “Stay. Start with the houses you burned.” · Turns to Casanova. “Ask her, not me.” · “Stay. And you tell the commission who paid you.” |
| Reaktion | „Ask her“: Casanova: *“Stay. And carry everything twice.”* (+4) · Kommission: *“Of course. I am a pirate, not a liar.”* · Petru: *“Then carry stones.”* | |
| Schluss | | Buenaventura zu einem Piraten mit ausgebrannter Fackel am Gürtel: *“Leave that.”* · Pirat: *“It's my torch, Capitán.”* |
| Übergang | `buenaventura_schwur`. Ziel-Zeile: *The burned houses are building sites now. Lay the first stone where you want them to start.* | |

Mit Bibi und `mo_eco_idee`: Erzählerin: *Bibi is counting the pirates. You don't know why yet.*

### 5.3 Ab Tag 24, Karte · `a3_alva_wach` „Since Last Night“ (ernst)

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | | Mina: *“Yacht! She's awake. Sandru says come, and Sandru never says come.”* |
| Inhalt | Bar abgebrannt: Feldbett in der Kirche, vorne, weit weg vom Hinterzimmer. Bar steht: `alvas_hinterzimmer`. Sandru auf einem Hocker. | Alva: [cough] *“How long?”* · Sandru: *“Since last night. You missed the end. Ha. Sorry. That's not funny.”* · Alva: *“And Minicu?”* · Sandru, nach einer Pause: *“Don won't let anyone in.”* · Alva: [sigh] *“Then we wait.”* |
| Handlung | | Alva: *“Who carried me out, Duc? Don't lie to me, I'll know.”* · Chips: “Sandru. He carried you out of the rubble.” · Looks at Sandru and waits. · “Does it matter?” |
| Reaktion | Wahrheit: *“...Orangeade's on me, then. For a year.”* · Sandru: *“I'm thirty, Alva.”* · Alva: *“I know how old you are. I was there.”* · Warten: Sandru sagt es selbst. · „Does it matter?“: *“Everything matters to me, Duc. That's my whole problem.”* | |
| Übergang | `a3_alva_wach`. Kein Paar mit Sandru (Kanon). | |

### 5.4 Tag 25, Frühstück · `a3_uhr` „Under Control“ (ernst, trocken)

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Kirche, vorne (wenn die Crew dort schläft) oder Messe. Telefon auf Lautsprecher. | |
| Inhalt | Beamter aus Ajaccio, nur Stimme. | *“We received your file, Lieutenant. Two men from the commission will come on the thirty-fifth.”* · Elsa: *“That's ten days.”* · Beamter: [clear throat] *“We're very busy here. And we have the feeling you have this under control. Don't you?”* · *“To be honest, we were surprised. Cala d'Orsu sends us a report every month. 'All quiet.' Signed and stamped.”* |
| Reaktion | | Elsa: *“Five years on this post, and they have never been this polite to me. I sent them a report every month too. Through the town hall. So where did mine go?”* |
| Inhalt | Mina mit zwölf Einschreiben aus Monaco. | Mina: *“There's one for Petru. A.V. bought the loan on his boat. And I have to take it to him. Me.”* · mit `bl_tueren_mina`: *“You let me go alone that day, when the phones were dead. I knocked on every door. I can do this too.”* |
| Handlung | | Elsa: *“First Officer. The commission wants witnesses. People who saw it with their own eyes and will sign their name. Will you help me find them?”* · Chips: “I'll talk to every one of them.” · “What about the crew? We saw everything.” · Takes Mina's basket. “Then we start with the letters.” |
| Reaktion | Crew: *“You're guests, and Alon just called you his partner on television. The village has to speak for itself.”* · Korb: Mina: *“Okay. You knock. I'll hold the bike.”* | |
| Zusatz (Totòs Versprechen) | Nur wenn Duc Totò in der Grotte versprochen hat, dass die Kiste Alon zu Fall bringt (`ereignisse_grotte.py:513-514`), das Versprechen offen ist und Duc die Kiste hat. | Totò: *“Comandante. You promised me that crate would bring Alon down, the night we lost Gennaro. Do you give it to her now?”* · Chips: Hands Elsa the crate. · “Not yet, Totò.” · Kiste: `alon_kiste_genutzt`, Beweis (5.25) |
| Übergang | Zeugenliste, Kopfzeile *Commission in 10 days.* Elsa: *“On Saturday I drive to Ajaccio. I want to see these 'all quiet' reports myself.”* | |

### 5.5 Tag 25, Dinner · `a3_megan_landet` „Until I Land“ (Megan-Theater, dann schwarzer Humor)

Entscheid e: Tag 25. Im Cliffhanger: *“Don't say a word to anyone until I land.”*

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Wassertaxi, ein Koffer. Kai vor der Yacht. | Erzählerin: *No helicopter this time. A water taxi from Bastia, and one suitcase.* |
| Inhalt (schwer beschädigt) | Megan sieht die Yacht: Schlagseite, Brandflecken, eine Plane über dem Achterdeck. | Megan: [sigh] *“How... delightful. I'm gone for three weeks, and my yacht is a wreck with people living in it.”* · Rosi: *“Don't worry. We fixed her once already, after the explosion. Twice is a tradition.”* · Megan: *“How reassuring. I'll call Monaco. They'll send parts, and a man who says 'unfortunately' a lot.”* |
| Inhalt (nicht zerstört) | | Megan: *“How... delightful. Three weeks, and my yacht becomes a field hospital.”* · Rosi: *“It's only paint. Nearly only paint.”* |
| Inhalt | Holm und Megans alte Kriegstafel (`bl_tafel`). | Holm: *“Megan.”* · Megan: *“Captain. You're standing.”* · Holm: *“On one leg, yes.”* · Megan: *“My list from the mess wall. Six jobs. You did {n} of them.”* · Holm, wenn kein `bl_ab_fertig_*` und kein `bl_na_fertig_*` gesetzt ist: *“Frankfurt slept, every night of the fighting. First sensible man on this boat.”* |
| Handlung | Megan nimmt Duc beiseite. | Megan: *“Duc. Alon thanked 'our partners at the Eden Group'. Did you know who was buying the harbour?”* · Chips: “No. Did you?” · “I didn't know they were selling it at all.” · Doesn't joke this time. “Mac. I'd never sell these people.” (nur `megan_funke`) |
| Reaktion | | Megan: *“I negotiated that sale. Every line. I never asked who A.V. was, because the numbers were good. So that's two of us who didn't ask.”* |
| Inhalt | | Megan: *“Here's the deal, First Officer. I'll try to stop the sale. The board in Monaco won't believe a video. They want paper and names. Can you get me names?”* · Chips: “I'm already collecting them.” · “Why do you care now?” · “What's in it for you, Mac?” |
| Reaktion | Warum: *“Because he nearly sank my ship. And because I signed it.”* · Mac: [chuckle] *“A seat on the board. Obviously. And a quiet evening, maybe. Don't ask for more.”* | |
| Übergang | `megan_zurueck`, VIP-Kabine (schwer beschädigt: bis Tag 31 Casanovas Gästezimmer; die Raumzuordnung `megan_kabine` in `modul_eden_rise.py:920` braucht dafür die Gegenbedingung `tk_yacht_weg` bis Tag 31), `a3_megan_handel`. | |

### 5.6 Tag 26, Frühstück · `a3_festa_tafel` „THIS. IS. THE. FESTA!“ (komisch, warm)

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Piazza, Tafel an der Kirchenmauer, Kevin darauf. | Erzählerin: *She has been here since five. The board is taller than she is.* |
| Inhalt | Rede mit Pause. Niemand klatscht. Kevin kreischt. | Casanova: *“Cala d'Orsu! They burned our houses. They want us to cancel the festa. So we will NOT!”* (Pause. Kevin kreischt.) · *“...Thank you, Kevin.”* |
| Inhalt | | Casanova: *“Three columns. Building, food, decoration. Every name on this board is a person with a gift. Nothing from the shop!”* |
| Handlung | | Casanova: *“Monsieur. Can I count on you, or should I count on someone else?”* · Chips: “Count on me.” · “Tell me who to start with.” · “Count on me. And on the pirates.” |
| Reaktion | | Casanova: *“Good. ...Good. That's all I wanted to know today.”* · *“And somebody get that bird off the board!”* |
| Übergang | Lose offen (4.3). | |

### 5.7 Tag 28, Tag · `a3_sonntag` „Sunday“ (warm → ernst, leise, eine Kette)

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Kirche, ein Eimer in der ersten Reihe, es tropft. Die Tür zum Hinterzimmer ist zu. | Erzählerin: *Pascal paid for the new roof. That money has stopped. The rain hasn't.* |
| Inhalt | | Don: *“Today I'll keep it short, because the roof is listening. And pray quietly for the one in the back room.”* · Erzählerin: *Outside, a father takes the bus timetable down and folds it very small. The school bus won't come on Monday.* · Bà Tư, eine Dose in Ducs Hand: *“Eat. You're too thin. And don't look at the bus stop like that. You didn't stop that bus.”* |
| Ansage | Nach der Messe: Leute mit Kisten an der Rathaustreppe (Bestellung `town_hall_stairs`). | Erzählerin: *They want to throw everything Pascal owned into the harbour.* |
| Inhalt | Don vor der Tür. | Don: *“No.”* · Mann: *“Father, he opened the gate!”* · Don: *“I know what he did, my son. I was there. Nobody goes in.”* |
| Handlung | | Mann: *“Are you with him or with us?”* · Chips: Walks up the stairs and stands next to Don. · “Elsa is on her way. Leave it for her.” · Stays at the bottom of the stairs. |
| Reaktion | Neben Don: *“Thank you, my son. My knees are not as brave as my mouth.”* (+6, Tür) · Elsa: der Mann: *“...Fine. We wait for the lieutenant.”* · Unten: Don hält allein, seine Tür bleibt über Vertrauen 3 und *The Bell* erreichbar | |
| Ansage | Elsa mit einem Brecheisen. Pascals Zimmer (Bestellung `pascal_room`): Schreibtisch, ein leerer Haken, ein heller Rand an der Wand. | Elsa: *“Father. I'm going in.”* · Don: *“You're the law, Lieutenant. I'm only a door.”* |
| Inhalt | | Elsa: *“My antenna form. Eleven months. 'Almost through.'”* · Erzählerin: *Elsa's reports to the mayor, never delivered.* · *Casanova's EU applications, signed, never sent.* · *Copies of the monthly report to Ajaccio: “All quiet.” His signature.* · mit `rt_ende_alle` oder `ark_aussagen_3`: *The red team's signed statements. Elsa handed them in herself.* · mit `bl_wache_gesehen`: Elsa, mit `bl_nachtwache_elsa`: *“I wrote it down myself that night, at three o'clock. Here it is again. Two words.”* · sonst: *“Holm told me about three o'clock. Here it is. Night of the twenty-second: two words.”* |
| Wende | Ein Kassenbuch in derselben sorgfältigen Hand. | Elsa: [sigh] *“The roof. The school bus. The festa money. And here: the priest. Sandru. ...Madame Casanova.”* |
| Handlung | | Elsa: *“This goes to the commission. All of it, or only his part? Think about it until then.”* · Chips: “All of it.” · “Only Alon's part. The village has paid enough.” · “I don't know yet.” |
| Reaktion | vorgemerkt | Elsa: *“For the record: I'd make the same face you're making.”* |
| Übergang | `a3_don_tuer`, Item „Pascal's Ledger“ bei Elsa, Nonnas Karte ab Nachmittag. | |

### 5.8 Ab Tag 28 Nachmittag, Karte · `a3_nonna_kiste` „The Last Crate“ (ernst, kurz)

Die Kiste stand seit dem Morgen von Tag 24 vor Nonnas Tür, sie liest den Brief erst nach Dons Tat (Kanon). Kommt Duc bis Tag 30 nicht, bringt Mina Schlüssel und Brief.

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Klostergarten, Kiste mit Setzlingen, ein gefalteter Brief. Sophia hilft im Garten (wenn sie hier schläft). | Erzählerin: *Every week there is a crate of seedlings at her door. This one has stood there since the morning after the siege. Today she opens the letter.* |
| Inhalt | | Nonna (liest): *“I told the priest not to go up the mountain. 'Stay, Don. Leave it with me.' I thought it was for safety.”* · *“And I told him all of it, every month, for nine years. He can't say a word. That's why he drinks.”* · Nonna: *“And today he stood in front of that door for him. Now I understand.”* |
| Zusatz | mit `bl_minicu_sag_es` | Nonna (liest): *“Duc told me to say it to him, to Minicu at the gate. So I did. It was the only true thing I said that night.”* |
| Reaktion | | Nonna: [sniff] *“I told Isabelle that man has a good heart. You don't have a good heart, Pascal. You have a bad conscience.”* |
| Handlung | Ein Schlüssel mit Zettel. | Zettel: *“Leave it with... no. You do it. I just have the key.”* · Nonna: *“The cellar door of the Casanova house. Do you want it, or shall I throw it in the sea?”* · Chips: Takes the key. · “Keep it, Nonna. I'll find another way in.” |
| Schluss | | Erzählerin: *She plants them anyway. Nothing in her garden goes hungry.* |

### 5.9 Ab Tag 24 Abend, Karte · `a3_siri_post` „In My Own Words“ (ernst → warm)

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Kai bei Sonnenuntergang, Siri im Pullover ihres Vaters mit den Sternen. | |
| Inhalt | mit `siri_darf_posten`: | Siri: *“It was up for four seconds, and then his video slid over it. This time I'm not giving him four seconds.”* |
| Inhalt | | Yasin: *“Bro. Somebody offered me twenty thousand for the video. Twenty! That's business.”* · Siri: *“It's his company, Yasin. He'll buy it, and nobody will ever see it.”* |
| Handlung | mit `siri_wartet` (sie wollte warten, bis sie weiß, ob Minicu wach ist): | Siri: *“Duc. I said I'd wait for Minicu. Nobody knows if he's awake. Do I post it now, or do I keep waiting?”* · Chips: “Post it now. He'd want them to see.” · “Wait. It's his face.” · “Ask Don what Minicu would say.” |
| Handlung | sonst: | Siri: *“Duc. I want to post it myself. No filter, no music, just what we saw. Is that brave or stupid?”* · Chips: “Brave. Post it.” · “Post it, and I'll stand next to you when he calls it fake.” · “Ask Yasin. It's his video too.” |
| Reaktion | Yasin, ehrlich, dann überspielt: *“...I filmed Minicu falling, and I kept filming. I don't want money for that. Okay? Don't tell anyone I said okay.”* · Warten: Siri postet erst auf der Festa (5.27), nicht als Beweis, aber im Schlussbild | |
| Übergang | `a3_siri_post` (Beweis) oder `a3_siri_festa`. | |

### 5.10 Ab Tag 24, Karte · `a3_revanche` „The Rematch“ (komisch, warm)

Mit Gemelli, ab Tag 24 (`HOLM_TAG = 24` steht auf `fix-akt2-folgen`, auf `fix-akt2` noch 22: beim Merge nachziehen, F-30).

| Beat | Zeilen |
|---|---|
| Ansage | Holm auf der Mole: *“Frankfurt. You still have my rifle. I want it back, so we shoot for it. Ready?”* |
| Inhalt | Schießwette (gebaut). Holm: *“It pulls left, like the day you won it from me.”* |
| Reaktion | gewinnt: *“Faen. Keep it. I'll win it back at the festa.”* · verliert: *“Keep it anyway. My hands are fine now. My head isn't, yet.”* · nur wenn Duc bei der Nachtwache „Nobody. Pascal has it.“ gewählt hat (neues Flag `bl_nachtwache_pascal`, denn `bl_nachtwache_niemand` kommt auch über `bl_wache_keiner`): *“I told you to send somebody to the north road that night. I should have gone myself.”* |
| Schluss | Petru stellt die letzte Flasche hin: *“Again.”* · Holm: *“Takk.”* |

### 5.11 Tag 29, Abend · `a3_berichte` „Every Report“ (ernst, Casanovas Wende)

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Kirchenstufen bei Nacht, Kerzen, Elsa mit einem Stapel. | |
| Inhalt | | Elsa: *“March. 'Dogs with collars near the monastery road.'”* · *“May. 'Request for a meeting with the mayor.'”* · *“August. 'Request for a meeting with the mayor.'”* · Erzählerin: *She reads thirty-one of them. Casanova doesn't stop her once.* |
| Reaktion | | Casanova: *“He told me you never wrote.”* · Elsa: *“I wrote every month, Madame.”* |
| Handlung | | Casanova: *“Monsieur. Pascal kept the truth in a drawer for nine years. What did you keep in yours?”* · Chips: “Nothing about your harbour. But I should have asked my own company more questions.” · Sits down on the step below her. “Only that I'm sorry it came on television.” · “I'm still here. That's my answer.” |
| Reaktion | Erste: *“Questions. Nobody here asked enough of those, Monsieur.”* (+6) · Zweite: sie nickt (+4) · Dritte: *“Yes. You are. That is something.”* (+2) | |
| Schluss | | Casanova: *“Lieutenant. From now on you report to me. Directly. Every day, if you like.”* · Elsa: *“Every day, Madame?”* · Casanova: *“...Every week.”* |

### 5.12 Tag 29, Frühstück · `a3_bibi_idee` oder `a3_lea_idee` (Entscheid f)

**Mit Bibi** (`rt_bibi_bleibt` und `mo_eco_idee`) ein eigenes Event **„Forty Men and a Boat“**. **Ohne Bibi** kommt die Idee von Lea: **„Every Rock“**.

| Beat | Bibi | Lea |
|---|---|---|
| Ansage | Bibi sitzt auf der Mole mit dem Field Book, vierzig Striche auf einer Seite. | Lea sitzt mit Opas Karte am Hafen und zeichnet Felsen ein. |
| Inhalt | Bibi: [laugh] *“So he's got forty men, a boat and nothing to do? And they know every rock in that bay? Doudou. Doudou, come here. I need you to do some numbers.”* (Kanon) · *“People pay me to watch a capybara sleep. They'll pay double to see a pirate who's sorry.”* | Lea: *“Did you know a protected bay needs people who know every rock? Proper people, with boats. And they've got forty!”* · ohne Margot: *“The wreck is gone, but the bay isn't. Somebody has to show people what's still here.”* |
| Handlung | Buenaventura: *“Tourists? On my ship? Why would a pirate do that, Señorita?”* · Chips (Duc): “Because a pirate with tourists can pay his debts.” · “Because you'd be the head of something.” · “Ask Bibi. It's her idea.” | Buenaventura: *“Tourists? On my ship? Why would a pirate do that?”* · Chips: “Because a pirate with tourists can pay his debts.” · “Because you'd be the head of something.” · “Ask Lea. It's her idea.” |
| Reaktion | Buenaventura: *“The head of...”* (Pause) *“...I would need a hat.”* · Bibi: *“I'll make you one. Out of an old feeding bucket. Don't ask.”* | Buenaventura: *“The head of...”* (Pause) *“...I would need a hat.”* · Lea: *“Did you know some sea captains wore two? Probably.”* |
| Übergang | beide: *“But the grotto belongs to the old man with the oranges. And I owe him everything already.”* Karte „The Man with the Orange“. Mit Bibi und Romanze: *Bibi lets her shoulder touch yours. Nobody else sees it.* | |

### 5.13 Ab Tag 29, Karte · `a3_orange` „The Man with the Orange“ (ernst-komisch)

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Grotte, Riscossore schält eine Orange. Totò ab Vertrauen 3 dabei. | wenn Duc ihn in der Grotte getroffen hat (neues Flag `gr_riscossore_gesehen` im Grotten-Frame setzen, denn `gr_8_riscossore` ist eine Kampf-ID): *“Last time you came with a knife. Today you came with a captain. Better.”* · sonst: Erzählerin: *An old man in a linen suit, yellow at the cuffs, sits by the water and peels an orange. Everybody here owes him money.* |
| Inhalt | | Buenaventura: *“I want to show tourists your grotto. I pay you from every ticket.”* · Riscossore: *“Eventually.”* · Buenaventura: *“...Eventually.”* · Riscossore: *“A man in prison pays nobody. A man with tourists pays me every day, a little. I prefer every day.”* |
| Handlung | | Riscossore: *“You want something too, I think. The commission. Why should I come and open my book for you?”* · Chips: “Because Alon paid Buenaventura through you. It's in your book.” · “Because nobody pays you if Alon gets the bay.” · Looks at Totò and says nothing. (nur `gennaro_verschwunden`, Totò dabei) |
| Reaktion | Erste: *“Clever. Not kind. Clever.”* · Zweite: *“Yes. That is the reason. Not kindness.”* · Dritte: Erzählerin: *Totò walks out. Gennaro's boat is still empty, somewhere off Cap Corse.* Riscossore: *“He hates me. He should. ...I'll come.”* | |
| Schluss (Kanon `akt3.md`) | Ebbe, Buenaventura steckt die Flagge auf den Felsen. | Buenaventura: *“It is an island. Twice a day.”* · Riscossore, ein Orangenstück: *“Here. Your first payment.”* |
| Übergang | `a3_riscossore_kommt`. „Head of Sea Captains Eco Tours“ erst im Epilog, nur im guten Weg. | |

### 5.14 Tag 30, Frühstück · `a3_maxwell_flug` „Gogo's Medicine“ (warm)

| Beat | Zeilen |
|---|---|
| Inhalt | Maxwell mit einer Kühltasche: [clear throat] *“Number One. Mr. Maximum is going to fly. In an aeroplane. Gogo needs this medicine in Durban, and the post is too slow.”* · mit `bl_verband_maxwell`: *“I kept the bandage from the siege, brother. For luck.”* · mit 7.6: *“Bibi says a plane has no bad temper. Mr. Maximum fed Bones. Mr. Maximum can sit in a plane.”* |
| Handlung | *“What does a big man do when he's scared of the sky?”* · Chips: “He takes the window seat and looks anyway.” · Puts a hand on the cool box. “He carries it. Like you always do.” · “He holds Jana's hand. She's coming to the airport.” |
| Reaktion | dritter: Jana: *“Coach, I'll hold your hand the whole way to Bastia. And I'm not sorry.”* |
| Übergang | Maxwell fehlt Tag 30 bis 32, zurück am Abend von Tag 32: *“Mr. Maximum has flown. We will never speak of it.”* |

### 5.15 Ab Tag 29, Karte · `a3_lot14` „Lot 14“ (ernst, Rosi-Kanon)

| Beat | Zeilen |
|---|---|
| Inhalt | Yamamoto (ab Vertrauen 3): *“So sorry, Rosi-san. I read A.V.'s property lists for my bank. There is a street in Catania. Lot 14. A workshop, closed three years ago.”* · Rosi: *“...The press in that workshop was older than Papa. It had a crack in the left side. He called it Old Lady.”* |
| Handlung | Rosi: *“Officer. If he goes down, can I buy it back? Tell me the truth.”* · Chips: “If he goes down, yes. So let's make him go down.” · “I don't know. But I'll help you try.” · Sits down on the toolbox next to her and waits. |
| Übergang | `a3_lot14` (Rosis Ende 2a und 3). |

### 5.16 Tag 31, Dinner · `a3_megan_monaco` „The Board“ (Säule Geld)

Megans Wende braucht 4 Zeugen **oder** 2 Beweise. Yamamoto mit Bindung 5 ruft vorher an: *“Officer-san. So sorry. I have stopped the loan. I did not ask permission. Very rude of me.”* Entscheid g: Beide Wege bleiben auch nach einem gescheiterten Tauchgang offen.

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | VIP-Kabine (beschädigt: Casanovas Gästezimmer), Megan in Boardroom-Kleidung. | Megan: *“Stay out of the picture, First Officer. And don't breathe so loudly.”* |
| Inhalt | | mit Zeugen: *“I have {zeugen} people ready to sign, in front of a commission.”* · nur Beweise: *“I have papers and a video he can't buy.”* · CEO (nur Stimme): *“Megan. A.V. pays us well. Is this about the yacht, or about you?”* |
| Wende (genug) | | Megan: *“It's about a bay that's worth more protected than sold.”* · CEO: *“...Is Duc there? Put him on. Duc, tell me straight. Is this village worth more than what A.V. pays me?”* · Chips: Steps into the picture. “The numbers are hers. The names are the village's. I just carried the letters.” · “Sell them the bay, and you sell them me with it.” |
| Wende (zu wenig) | | CEO: *“Bring me something better than a fishing village, Megan.”* Bildschirm aus. |
| Reaktion | | genug: *“That's the first argument I've won that I actually believe in. It's uncomfortable.”* · zu wenig: *“How... delightful.”* (leise) |
| Übergang | `a3_megan_wende` oder `a3_megan_verloren`. | |

### 5.17 Tag 32, Nachmittag · `a3_switched_off` „Switched Off“ (der schwere Moment)

Entschieden (F-24, E-125): kommt immer, *weil Alon kann* (Kanon). Rosis Schiene gibt es erst in Akt 3, danach (5.19). In der Belagerung trägt Sandru noch Alons Schienen.

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Keine Titelkarte, keine Musik. | Mina: *“Yacht! YACHT! The market. It's Sandru.”* |
| Inhalt | A.V. Market, Sandru zwischen den Regalen, die Schienen still. | Erzählerin: *The braces are quiet. You never noticed the sound until it stopped.* · Bildschirm: *Device paused. The user broke the rules of service. Thank you for your understanding.* · Sandru: [laugh] *“Ha. They switched me off. Like a lamp.”* · mit `sandru_surren`: *“You heard them hum, the first day you came in here. Now listen.”* · mit Los „Not in the System“ genommen: *“They counted the pallets.”* |
| Wende | Alva betritt zum ersten Mal das Haus ihrer Mutter. Titelkarte *Alva*. | Erzählerin: *She has not stepped into this house since her mother left for Seville.* |
| Handlung | | Alva: *“Duc. The door. Can you hold the door?”* · Chips: Holds the door. · Takes his other arm. · Steps back and lets her do it. |
| Reaktion | Alva trägt ihn über die Straße und die Treppe hoch zur Bar (Bar ist Baustelle: in die Kirche auf ihr Feldbett). | Alva: [sigh] *“You're my little brother, you idiot. I've carried you since you were six.”* · Sandru: *“I know. That's the whole problem.”* |
| Inhalt | Alons Angebot per Bildschirm im Market. | Bildschirm: *Your device can be switched on again. Please confirm that you will not speak to the commission.* · Sandru: *“Ha. He wants my mouth for my legs.”* Ohne „No Leash“ (5.19) nimmt er an: dann steht er an Tag 34 auf Alons Schienen bei Alon, seine Tür bleibt zu |
| Schluss | Kein Paar. Mit der Freundschaft von Chiara und Alva (7.2) steht Chiara unten an der Treppe und hält die Tür, ohne Zeile. | Erzählerin: *She sits on the stairs for a minute. Then she goes back to work.* |

### 5.18 Tag 32, Frühstück · `a3_probefahrt` (nur schwer beschädigt), siehe 4.4

### 5.19 Tag 33, Frühstück · `a3_schiene` „No Leash“ (warm, leise)

Wenn Duc sich gekümmert hat (`sandru_surren`, `sandru_herkunft` (F-20) oder Vertrauen Sandru 3). Rosi gefeuert: Maxwell (zurück seit Tag 32 abends) und Rosi per Video.

| Beat | Zeilen |
|---|---|
| Inhalt | Rosi: *“Same motors. Same chips. I only took out the part that talks to his computers. The leash, Officer. Like with the collars.”* · gefeuert: Maxwell: *“I hold the screwdriver, Rosi says which way. Teamwork, brother.”* · Rosi: *“That sound is mine now. Don't let them tell you otherwise.”* |
| Inhalt | Sandru steht auf: *“A.V. gave me six years of walking. You gave me a speech.”* (Kanon) · *“...And her. You gave me her. So what do I do now, Duc? Walk over there and say what?”* |
| Handlung | Chips: “Say thank you. Then say nothing.” · “Go and stand in front of Alva. Straight.” · Shrugs. “You gave yourself the speech. I just listened.” |
| Reaktion | mit `sandru_herkunft`: *“Iskander. You can say it. My mother says it.”* · sonst: *“Ha. One thing at a time, Duc.”* |
| Übergang | ISKANDER (nur mit `sandru_herkunft`, F-20) oder SANDRU, `a3_sandru_schiene`, Tür offen. Ohne Schiene hat er Alons Angebot aus 5.17 angenommen. |

### 5.20 Tag 33, Frühstück · `a3_einladung` „An Invitation“ (ernst)

| Beat | Zeilen |
|---|---|
| Inhalt | Mina: *“This one's for you, Yacht. The good paper. From the house on the hill.”* · Erzählerin: *“Dinner. Tomorrow at eight. Just you. A.V.”* · *Your name on the envelope is in a careful hand. You have seen it before: on Minicu's name sheet, the one you picked up at the gate, and on Alon's letters on the church steps.* (`bl_blatt_gefunden`) |
| Handlung | Mina: *“Are you going?”* · Chips: “Yes.” · “Yes. But not alone.” · “I don't know yet.” |
| Übergang | Mit Schlüssel: *And you have a key.* |

### 5.21 Tag 33, Abend · `a3_nach_mitternacht` „After Midnight“ (frech, warm, privat)

E-060: keine öffentliche Begleitung. Jede Frau fragt nach einem Moment für sich **nach Mitternacht an der Mole** während der Festa. Duc wählt eine oder niemanden. Lea oder Sophia, nie beide. Bedingung: Stufe-5-Szene ihrer Leiter; Megan: `megan_funke` und eine gemeinsame Nacht; Bibi: `rt_bibi_bleibt`, Leiter bis *The Brochure*.

| Frau | Ihre Frage | Nach Mitternacht |
|---|---|---|
| Chiara | *“First Officer. I'll ask you once, and if you laugh, it's a two. After midnight, on the mole. Will you come?”* | ihre Zehn (Kanon) |
| Alva | *“After my dance, Duc, I close the bar for one hour. Will you be on the quay?”* | „Only you“ (Kanon) |
| Lea | mit `bl_ab_fertig_lea` oder `bl_na_fertig_lea`: *“Two fingers, the sign from the foredeck, that night in the siege. After midnight. Yes?”* · sonst: *“After midnight, on the mole. Will you come? Proper come?”* | ihre Azoren-Antwort |
| Sophia | *“Ten euros says you'll come down to the mole after midnight. ...Oh. Have I just lost?”* | eine Zeile aus ihrem Buch |
| Rosi | *“Officer. At midnight I take off this stupid dress. Will you be on the mole after that?”* | „Captain“, wenn er es verdient |
| Lola | *“Boss. When the cooking's done. One song, just us, on the mole. Mostly one song. Yes?”* | sie setzt sich hin |
| Siri | *“No camera after midnight. Will you meet me by the water?”* | ihre eigenen Worte |
| Bibi | *“The gates open on Sunday afternoon, and I'll be a mess. After midnight, will you come anyway?”* | nach *Last Page* |
| Megan | *“Don't make me say it twice, First Officer. The aft deck, after midnight. Then we never speak of it. Agreed?”* | Abendkleid ohne Anker |

Die Gewählte steht in der letzten Nacht (34) oben in der Liste der Begleitung für die Nacht vor der Kommission. Kein Echo für die anderen (höchstens eine Leiter-Szene oder ein Echo am Tag), sie sind auf der Festa einfach da.

### 5.22 Tag 34, Frühstück · `a3_villa_plan` (ernst, kurz)

Elsa und Megan sind nicht dabei (Schlüssel, Pascal, `dorf_figuren.md`).

| Beat | Zeilen |
|---|---|
| Inhalt | Holm: *“You're invited, Frankfurt. That's better than a search warrant.”* · mit Schlüssel: Rosi: *“A cellar door nobody locks properly. Old iron. My favourite kind of door.”* · ohne: Casanova: *“I know the cellar. I hid there from my father when I was seven. I'll take you.”* |
| Handlung | Holm: *“Who goes down with you, Frankfurt?”* · Chips: Nods at Rosi. “You and me.” · Turns to Casanova. “Show me the way, Madame.” · Picks up the key. “I'll go alone.” |

### 5.23 Tag 34 · `a3_villa_keller`, `a3_villa_dinner` „Name Your Price“

**Keller** (Frame-Kette, vier Bilder): Casanova bleibt an der Tür (*“It's smaller than I remember. ...Go. I'll wait here.”*, ★ bleibt aufgespart) · Server-Schrank zwischen Weinfässern (Rosi: *“He put his computers in a wine cellar. That's a crime too.”*) · Whites Einsatzplan *“Day 22, phase 3: torches, houses.”* und die Quittung an Buenaventura (`a3_beweis_feuer`) · zwei Agenten, ein Roboter (Steel).

**Dinner** (ohne Kamera, ruhig und genau, Pascal im weißen Fedora an der Tür, ohne Zeile):

| Beat | Zeilen |
|---|---|
| Ansage | Erzählerin: *From up here, the village looks like a model. The building sites look like toys.* |
| Inhalt | Alon: *“Duc. Sit. Two of my people are asleep in my cellar, so I think you came the back way. You've been busy.”* · *“Keep the folder. Paper. In my experience, paper loses.”* · *“Every collar your mechanic cut open sent me one last message. That's how I learned to lock them. You helped me more than any engineer I hired.”* · *“Four hundred thousand people died in wars last year. I can bring that to zero. I need one bay and ten more years. I don't have ten years. So I need the bay now.”* |
| Handlung | Alon: *“Join me. Name your price.”* · Chips: “No.” · Looks out of the window at the village and says nothing. · “What would my price be?” · Puts his glass down. “Everyone I've met down there. Can you buy that?” |
| Reaktion | Preis: *“Eden Consulting, free of debt. Your name on a building in Frankfurt. And you never think about this village again. So?”* · Chips: “Deal.” · “No.” · ★ (alle vier Säulen, Yamamoto Bindung 5, Ende 1 gesehen): “Deal. Let's sign it in front of the village.” |

### 5.24 Tag 34, Abend · `a3_villa_ende` „The Last Push“

| Zweig | Zeilen |
|---|---|
| Presse (immer) | Terrasse, Drohnenkamera. Alon: *“Hi, Cala d'Orsu! Quick update from your future. And a big thank you to my partner on the ground, Paul... Paolo. Thank you, Paolo.”* Pascal lächelt. · Erzählerin: *The man who knows every name in the village. His master doesn't know his.* |
| Deal | Duc steht im Stream neben Alon, Ende 1. |
| ★ | Das Dorf steht am Fuß der Villa, Casanova betritt ihr Elternhaus (Kanon `enden.md`), Feinschliff mit den Enden. |
| Nein: Endkampf | Exoskelett, Kampf (Luft, tödlich), Ducs Ausrüstung fällt nicht aus. Mit Rosi: Unit-01 bricht in Runde 3 durch die Kellertür. Rosi: *“I took the leash out.”* · Alon: *“I know. That's how I learned to lock it.”* · Rosi: *“She doesn't have a leash. She never did.”* |
| Nein: Festnahme | An der Mole unter der Villa, Elsa hat den Stream gesehen (Vertrauen 4, `elsa_hilft`). Elsa: *“I saw your face on his stream, First Officer. I don't want to know how you got in.”* · zu Alon: *“Mr. Varenne. Coast guard. You're under arrest, and I'd honestly prefer it if you said nothing.”* |
| Niederlage | Alon: *“Go home, Duc. The commission is tomorrow. I'll be watching.”* |
| Pascal | geht immer. Bei der Festnahme: *“Elsa. Your mother's birthday is next week.”* |
| Nachtwache | `bl_nachtwache_wolff`: *“Three o'clock. 'Not yet.' I remember.”* · `_elsa`: *“For the record, Pascal: three o'clock.”* · `_yamamoto`: *“Pascal-san. The coffee was very good. I am still worried.”* |
| Übergang | `a3_alon_besiegt`, `a3_alon_festgenommen`. Nacht: `a3_letzte_nacht`. |

### 5.25 Tag 35, Tag · `a3_kommission` mit `mo_kommission`

Kai, Klapptisch, zwei Männer aus Ajaccio, ein Schreiber (`ereignisse_mochis.py:182-185`). Mit `mo_ark_beweis` eröffnet `mo_kommission` (unverändert), `a3_kommission` schließt ohne zweite Ansage an. Sonst eröffnet `a3_kommission` (F-25). Mit Deal: Das Dorf schweigt, Duc ist oben, drei Zeilen, dann Ende 1.

| Beat | Zeilen |
|---|---|
| Ansage (ohne `mo_kommission`) | Erzählerin: *Two men from Ajaccio. One folding table. One clerk with a lot of paper.* |
| Inhalt | Kommissar: *“We are here to find out what happened in this bay on the twenty-first, twenty-second and twenty-third. Who saw it with their own eyes?”* |
| Zeugen | Petru: *“I saw the torches at my workshop. And I saw who stayed.”* (mit Rudern: *“And the village rowed out. Like in 1924.”*) · Mina: *“I knocked on every door that day, when the phones were dead. I saw who opened, and who didn't.”* · Bà Tư: *“Men in white. They asked me twice for the north road. I told Duc then. Now I tell you.”* · Alva: *“From the square I saw the north barricade open. Then men in white came through. I saw that with my own eyes.”* · Sandru: *“My name is {sandru_name}. I carried Alva out of the rubble. And the next week, A.V. switched off my legs.”* · Don mit `bl_kirche_don`: *“I was sober. Write that down too. It doesn't happen often.”* · Don mit `bl_kirche_don_schlaeft`: *“I was asleep on the church steps, my son. But I saw the gate open before I fell asleep.”* · Don sonst: *“I was outside the church door all night. I saw the gate open.”* · Casanova: *“Every night someone left his paper on my church steps. I kept all of it. Here it is.”* |
| Minicu | Kommissar: *“And the man at the gate? The big one?”* · Don: *“He can't come today.”* · Erzählerin: *Nobody on the quay asks what that means.* |
| Buenaventura | *“A man named White paid me in clean money, like a bank. I gave the order to burn. I gave the order to stop.”* · *“And you are?”* · *“Captain Buenaventura of The Eventually.”* · *“...I see.”* |
| Riscossore | *“He's telling the truth. It's in my book, page forty-one. A man in prison pays nobody, so I'd like him to stay out.”* |
| Beweise | nur was der Spieler hat, nichts über die Yacht von Tag 0: `a3_beweis_feuer`, `alon_kiste_genutzt`, `a3_siri_post`, `sophia_notizen` (Sophia gefeuert: die Notizen kommen per Post, Elsa liest vor) (Sophia: *“Darling, I wrote down every time and every word I heard on the radio that night. I didn't know why. Now I do.”*), `bl_funk_white` / `bl_funk_charly` (Charly: *“Twenty-one forty. He said 'tonight'. Seven out of ten for clarity.”*), Funkbuch, Nachtwache je Person (F-26), Adriens Fotos, Steuerchip, fremdes Teil, Red-Trio-Aussagen |
| Kassenbuch | Elsa: *“First Officer. Pascal's book, the one from his locked drawer. All of it, or only Alon's part?”* · Chips: “All of it.” · “Only Alon's part.” · Alles: Casanova: *“Yes. Me too.”* |
| Schluss | Kommissar: *“Thank you. We have what we need. Or we don't. You'll know tonight.”* |

### 5.28 Ab Tag 26, Karte · `a3_charly_geld` „Borrowed“ (komisch-ernst, E-125)

Nur mit `rt_charly_bleibt` und ohne `rt_charly_weg`. Kommt, sobald eine Baustelle begonnen ist.

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Kirchenstufen, Casanova mit der Festa-Tafel. Charly mit Laptop. | Erzählerin: *Charly sits down next to the mayor. She doesn't say hello. She never does.* |
| Inhalt | | Charly: [clear throat] *“My mother's company sells to Alon. I moved some of her money tonight. Quietly. For the houses.”* · Casanova: *“You... moved it? Is this stolen, Mademoiselle?”* · Charly: *“Three out of ten for stolen. Eight for borrowed. She won't notice for a month.”* |
| Handlung | Casanova sieht Duc an. | Casanova: *“Monsieur. Do I take money that a girl took from her own mother?”* · Chips: “Take it. Her mother pays for what Alon burned.” · “Take it, and put Charly's name on the board.” · “Ask Charly, not me.” |
| Reaktion | | erste: Casanova: *“...Then the houses are built with Ravenel money. How funny.”* · zweite: Charly: *“Don't. Five out of ten for that idea.”* Casanova schreibt den Namen trotzdem, klein. · dritte: Charly: *“Take it. It's the first good thing her money ever did.”* |
| Wirkung | `a3_charly_geld`: jede offene Stufe kostet 20 % weniger (4.1). Mit Chip zwei steht Charlys Name auf Casanovas Tafel und im Festbild | Erzählerin: *For the first time, nobody has to count the timber twice.* |

### 5.26 Tag 35, Nachmittag · `mo_frei_start` (gebaut), danach *Last Page* (Bibi)

### 5.27 Tag 35, Abend · `a3_festa` „The Festa“ (Schlussszene, Minicu)

| Beat | Was | Zeilen |
|---|---|---|
| Ansage | Piazza, das Festa-Bild, Ausstattung nach den Losen. | Erzählerin: *Half the lights work. The tables are full anyway.* · oder *The whole bay is here. Even Kevin.* |
| Inhalt | Casanovas Rede, ihre Pause. | Casanova: *“Cala d'Orsu has stood on this rock for four hundred years. Pirates came. Tax men came. A man with a satellite came. And tonight...”* (Pause) |
| Wende | Stille. Dann Alva, langsam (Kanon). | Erzählerin: *Nobody claps. Then Alva does. Slowly.* |
| **Wende (Entscheid c)** | Die Kirchentür geht auf. Minicu, verbunden, Don stützt ihn. Er klatscht, zu laut. Kevin landet auf seinem Kopf. Titelkarte *Minicu*. | Erzählerin: *Then a second pair of hands, much too loud. The church door is open.* · Jana: [gasp] *“Jessas... MINICU!”* · Lola: [sniff] *“Oh, mate. I saved you the leftovers. Twelve days of leftovers.”* · Minicu: *“Does it hurt? The noise? I can clap quieter.”* · Erzählerin: *Then everyone claps. For her, and for him.* · Casanova: [sniff] *“...Thank you. Thank you, Alva. Thank you, Minicu.”* · Alva: *“Don't get used to it.”* |
| Inhalt | Minicu und Duc, kurz. | mit `bl_minicu_duc_zuerst`: Minicu: *“You came first, when I was on the ground. Before Pascal. I heard you.”* · Minicu: *“Is Pascal coming?”* · Chips: “No, Minicu.” · Puts a hand on his shoulder and doesn't answer. · “Not tonight.” |
| Inhalt | mit `a3_siri_festa` (Siri hat gewartet): | Siri: *“Now I can post it. He's standing.”* |
| Inhalt | mit `bl_kirche_casanova`: | Jana: *“Madame, sorry, the children want the end of the long story. The one from the church.”* · Casanova: *“Later. I promise.”* |
| Inhalt | Festa-Schalter (F-22, entschieden E-126: Fenster 35, Phase Abend, Ort `village_piazza`): `br_ehrenbuerger` (nicht Ende 1), `ab_casanova_flamenco`, `gv_rotes_kleid` in dieser Reihenfolge | |
| Inhalt | Die Freundschaften aus Abschnitt 7 stehen im Bild. Holm sitzt neben ihrer Mutter, Petru bringt zwei Gläser. Lola trägt Bà Tưs Topf. Die übrigen je nach ihrem Ereignis | Holm: *“Mamma, this is Petru. He's the one who taught me to sit still.”* · Petru: *“Hm.”* |
| Mitternacht | der private Moment an der Mole (5.21), dann das Ende (Abschnitt 8) | z. B. Chiara: *“Ten. That's a ten, First Officer. Don't let it go to your head. ...Let it go to your head a little.”* |
| Epilog (Nacht) | Minas Einschreiben, Pascals Tür, niemand macht auf (Kanon) | Mina: *“Sign here.”* · Erzählerin: *Nobody is there. It's the first letter she can't deliver.* |

**Minicu in allen Enden (Entscheid c):** Er steht in jedem Schlussbild. Ende 3: Er schreibt seinen Namen selbst ins Netz, schief, neben Pascals leerem Knoten; vorher gibt Duc ihm das Namensblatt zurück (`bl_blatt_gefunden`). In Ende 0 und 1: Er trägt Kisten am Hafen, für A.V., ohne zu fragen.

## 6. Romanzen fertig spielen

Je Frau eine Schluss-Szene zwischen Tag 24 und 33 (vor der Villa), Bedingung: Stufe-5-Szene ihrer Leiter. Zwei sind Expeditionen mit Rastplatz-Szene. Jede beginnt mit einem Rückbezug mit Erinnerung. Zwei Belagerungs-Nächte (`bl_na_fertig_<pid>`) setzen den Status „zusammen“.

| Frau | Szene und Ort | Rückbezug | Frage und Chips |
|---|---|---|---|
| **Chiara** | „Blackout“ (Deutung von `chiara.md:43`, F-18): am Abend von Tag 32 allein auf der Brücke, Ersatz-Fenster bis Tag 33 | mit `bl_ab_fertig_chiara` oder `bl_na_fertig_chiara`: *“The night in the siege, on the bridge wing, when I rated the sky because I'd run out of things to count. It was a six.”* · sonst: *“The first day you came on board, I gave you a four. I'm not changing it. Yet.”* · mit `bl_verband_chiara`: *“And you gave me the good bandage. I never said thank you. I'm not saying it now either.”* | *“First Officer. I don't know which breaker it is. What would you do?”* · Holds the torch and lets her find it. · “The red one. Second row.” · “I don't know either. Let's find it together.” · Erzählerin danach: *For once, she doesn't give it a number.* |
| **Alva** | „The Board Is Full“, Bar nach Feierabend (Bar ist Baustelle: Notbar am Kai) | mit `bl_alva_runde`: *“The evening on the quay, in the siege, when I gave out drinks and wrote down every glass. You paid the first round. You did.”* | *“My name isn't on Papa's board. What do you write next to it?”* · Writes ALVA and, next to it, “stays”. · Writes ALVA and leaves the space empty. · Gives the chalk back. “You write it.” |
| **Lea** | Expedition „One More Dive“ (2 Phasen), Grottenmündung, Rastplatz auf dem Felsen, der bei Ebbe eine Insel ist | mit `bl_ab_fertig_lea` oder `bl_na_fertig_lea`: *“Two fingers, side by side, the sign I showed you on the foredeck, the night of the siege.”* · sonst: *“The squid, the night they came up to the swim platform and you made the okay sign at me.”* | *“The Azores letter is still in my bag. If I go, will you come and see me? Proper see me?”* · “Yes. Not fast, but yes.” · “Stay. The bay will need you.” · Holds up two fingers and says nothing. (Nach gescheitertem Tauchgang geht Lea in jedem Fall, Kanon. Dann entfällt der zweite Chip) |
| **Sophia** | „The Sixteenth Letter“, Klostergarten (wenn sie dort schläft) oder Bord | *“Ten euros, the bet that you'd ask me what I actually want. You did ask. I still owe you the answer.”* | *“Darling, will you open it, or shall I?”* · Gives her the letter. “It's yours.” · Opens it and reads the first line out loud. · Puts it in her notebook, unopened. “Later. Together.” |
| **Rosi** | „Two Thirds“, Maschinenraum (nach `a3_lot14`) | *“The night with the stopwatch, when nobody lost.”* | *“Officer. If I say 'Captain' now, is that an insult or a promotion?”* · “A promotion. I'll take it.” · “Neither. Say Duc.” · Laughs and hands her the spanner. · Danzel schwärmt dazwischen, wenn Ducs Begehren bei Rosi höchstens 3 ist |
| **Lola** | „First Guest, Again“, ihre Hütte am Strand | mit `bl_ab_fertig_lola` oder `bl_na_fertig_lola`: *“The night in the siege you said yes to the toastie, and it wasn't burnt. Not even a bit.”* · sonst: *“The first morning on the yacht, when you ate my eggs and didn't make a face.”* | *“Boss. If I cook for you here, will you sit down? Properly? No running off?”* · Sits down and puts his phone away. · “Only if you sit down too.” · “Can I help?” |
| **Siri** | „No Caption“, Sonnenuntergang ohne Handy | *“The sunset on the foredeck, when I told you I hadn't written my own caption since I was nineteen.”* | *“If this was a photo, what would you write under it?”* · “Nothing. Some things don't need words.” · “Siri, in her own words.” · Takes her hand and doesn't answer. |
| **Bibi** | Expedition „Mochi“ (2 Phasen, `kl_loewe_frei`, Station offen), Rastplatz am Feuer | *“The night at the campfire with the three of us, when I said 'until every collar is off', and you didn't laugh. This is the last one.”* | *“He's asleep. Do I cut it, or do you?”* · “You. He's yours.” · “Together.” · Hands her the knife without a word. |
| **Megan** | „Still Off the Record“, VIP-Kabine (beschädigt: Casanovas Gästezimmer), Fenster Tag 26 bis 30 (vor Monaco) | Rückbezug auf ihren Anruf: *“That night I called you and said it was off the record. You never told anyone.”* | *“This stays off the record too, First Officer. Can you do that?”* · “I already did, Mac.” · “Only if you call me Duc.” · Nods and closes the door. · Morgens Sprite-Set `megan_morning_after`, nie öffentlich |

**Ligeia:** keine Romanze. Mit `ligeia_freund` an Tag 30 eine Flaschenpost: *“Sailor. They say the bay will be safe. I would like to sing at something that isn't a shipwreck.”* Mit `sirene_weg`: *“And keep my stone safe. It has waited longer than you.”*

## 7. Fünf Freundschaften und zwei Paare: Die Yacht wächst mit dem Dorf zusammen (Entscheid h, E-124, E-125)

**Der Bogen:** Akt 1 Duldung, Akt 2 Zusammenarbeit, Akt 3 Gemeinschaft. Je ein Crew-Mitglied und ein Mensch aus dem Dorf verbringen Zeit miteinander, und eine tiefe Freundschaft wächst. Keine Romanze, mit zwei Ausnahmen: **Holm und Petru** (Kanon: späte Liebe, E-125) und **Charly und Danzel** (Kanon: „findet in Akt 3 zu Charly“, E-127) kommen am Ende wirklich zusammen. Dazu die Freundschaft Bibi und Maxwell innerhalb der Gäste. Pool-Regel: höchstens ein Ereignis je Tag, Tag 26 bis 33, also sieben Ereignisse auf acht Tage.

**Regeln:** wholesome, kein Drama, keine Intim-Szene. Jedes Paar hat ein Ereignis (2 bis 3 Beats) im Pool ab Tag 26, höchstens eins je Tag, Vorrang 65 % wie bei Flirt-Events, spätestens Tag 33 als Nachzügler. Duc ist Zeuge oder hilft und hat **eine Wahl mit Wirkung im Festbild**. **„Duc hat die Romanze“** heißt: Leiter-Stufe 3 erreicht oder Status „zusammen“ oder „offen“ (Begehren allein reicht nicht, Lea und Sophia starten bei 2). Gilt Duc für beide Frauen eines Paares (Chiara und Alva), spielt die Fassung der Frau mit der höheren Leiter-Stufe. Dann spielt die Fassung, in der die andere Figur sie herzlich neckt oder unterstützt. Woher sie davon weiß: nur aus Tratsch, den das Spiel zeigt (Mina „just knows“, Lola erzählt es), wie E-060 es erlaubt. Die volle Fassung lässt die Freundschaft zwischen den beiden wachsen. Bei Chiara und Alva (beide romanzierbar) spielt die volle Fassung nur, wenn Duc mit keiner von beiden zusammen ist.

### Kanon-Prüfung der Paare

| Paar | Kanon dafür | Kanon dagegen oder heikel | Wie das Drehbuch es löst |
|---|---|---|---|
| **Lola und Bà Tư** | Bà Tưs Intro: *“You, later. Him, now.”* (Lola bekommt keinen Teller, `dorf_figuren.md`) · Lola ruft jeden Sonntag ihre Nan an (`lola.md`) · Bà Tư kocht zu viel, nennt Duc „con“ | Lola 24, Bà Tư um die 75 | **Familienliebe und Freundschaft:** Bà Tư wird Lolas Insel-Nan (E-124) |
| **Chiara und Alva** | `alva.md`: Chiara ist eifersüchtig auf Alva · Alva flirtet mit jedem, „nobody's mine“ · Chiara bestellt bei Alva auf Italienisch und verwechselt Oliven mit „Olivetti“ (`chiara.md`) | Sandru liebt Alva ohne Paar-Ende · beide für Duc romanzierbar | **Freundschaft:** aus Eifersucht wird die beste Freundin, die keine von beiden je hatte. Alvas heimlicher Wunsch nach einem starken Mann bleibt unberührt. Sandru freut sich für sie (kein Paar mit ihm, Kanon) |
| **Isabelle und Sophia** | Isabelle fragt mit Mina nach einem mutigeren Leben (*“So could you.”*, `kloster.md`) · Sophia schreibt nachts, ist ohne Show schlicht · Bà Tư neckt Isabelle, warum sie keinen jungen Mann hat | Isabelle ist **Novizin** im Habit · Sophia für Duc romanzierbar · Schwester Lea | **Freundschaft:** Sophia wird die ältere Freundin, die Isabelle Mut macht. Kein Gelübde berührt. Sophia schreibt ihr eine Zeile für Mut, die im Spiel ungesagt bleibt |
| **Mina und Lea** | beide jung (24, 23), beide mit einem Brief, der vom Gehen handelt (Dumè in Montréal, die Azoren) · Mina weiß alles, Lea stellt Fragen, die sich keiner traut | Lea für Duc romanzierbar · Mina „keine Pflicht-Romanze“ (gilt für Duc) | **Freundschaft:** zwei, die beide nicht wissen, ob sie bleiben. Lea schläft bei Mina (wenn die Yacht beschädigt ist) |
| **Chiara und Sophia (kein Paar, aber Kanon)** | beide Figurenseiten: ein unausgesprochener Kuss nach Saint-Tropez, Sophia lehnte Megans Angebot wegen Chiara ab | beide werden neu verpaart | Je eine Zeile, die es anerkennt, als Vertrauen unter Freundinnen: Chiara in 7.2 erzählt Alva davon, zum ersten Mal überhaupt · Sophia in 7.3 schreibt die Zeile an Isabelle in dasselbe Notizbuch, in dem noch eine Seite für Chiara steht (Bild, kein Text) |
| **Bibi und Maxwell** | Maxwell hat panische Angst vor allem, was fliegt, und fliegt an Tag 30 Gogos Medizin selbst (`maxwell.md`) · Bibi ist nie genervt, energisch, mit Tieren (`bibi.md`) | Bibi für Duc romanzierbar · Szene muss vor Tag 30 liegen | **Freundschaft:** Bibi übt mit Maxwell seine Angst, mit Kevin. Bedingung `rt_bibi_bleibt`, Station offen |
| **Charly und Danzel** | beste Freunde seit dem Mitarbeiter-Event, Danzel „findet in Akt 3 zu Charly“, ihre erste 10 gehört ihm, sie baut ihm die Kasse (`charly.md`, `danzel.md`) | Danzel schwärmt in Akt 3 schüchtern für Rosi und Lola und wird bei Begehren bis 3 Ducs Rivale (`danzel.md`) | **Paar (E-127):** zwei seltsame Menschen, die sich genau dafür lieben. Wholesome, Kuss auf der Festa, keine Intim-Szene. Die Schwärmerei läuft bis zu diesem Ereignis, danach ist er vergeben (F-33) |
| **Holm und Petru** | Kanon: späte Liebe in Akt 3 (`holm.md`, `petru.md`), Holms Mutter kommt, Ingrid ruft an | keine | volle Fassung immer, beide nicht romanzierbar |

### 7.1 Lola und Bà Tư · „You, Now“ (wholesome, Familienliebe)

| Beat | Volle Fassung | Fassung mit Duc und Lola |
|---|---|---|
| Ansage | Bà Tưs Laden (oder ihre Notküche), früh. Lola schläft hier (wenn die Yacht beschädigt ist) oder kommt jeden Morgen helfen. | gleich |
| Inhalt | Bà Tư bringt Lola bei, Reis richtig zu waschen. Lola macht es zu schnell. Bà Tư: *“Again. Slower. You cook like you're running away.”* · Lola: *“I sort of am, Auntie. Mostly from the dishes.”* | gleich |
| Inhalt | Lola erzählt von ihrer Nan in Byron Bay, 91, die einmal die Küstenwache rief, weil der Anruf ausblieb. Bà Tư hört zu und sagt nichts. | Bà Tư, über den Topf hinweg: *“Mina says the Boss eats at your table now. Good. You feed him. He's too thin.”* · Lola: *“Auntie! ...I feed him toast, mainly.”* |
| Wende | Bà Tư stellt zwei Teller hin, den ersten vor Lola. Mit `g1_batu_intro` gesehen: *“The first time you came to my shop, I said 'You, later.' Now: you, now.”* · sonst: *“In my shop, the first plate goes to family. Here. You, now.”* | gleich, dann: *“And you tell him he can come, too. Later.”* |
| Handlung (Duc) | Lola: *“Boss, she's adopting me. Is that allowed?”* · Chips: “Say yes before she changes her mind.” · Sits down and holds out his own plate. · “Call your Nan and ask her.” | gleich |
| Reaktion | Lola ruft ihre Nan an, auf Lautsprecher. Nan: *“Is she feeding you? Then she's family.”* · Bà Tư: *“Tell her I put extra fish sauce.”* | gleich |
| Wirkung | Los *The Pot* mit Lola als zweiter Köchin, im Festbild trägt Lola den Topf. Chip „Call your Nan“: Lolas Nan ist im Festbild auf einem Handy dabei | gleich |

### 7.2 Chiara und Alva · „Olivetti“ (wholesome, Freundschaft)

| Beat | Volle Fassung (Duc mit keiner von beiden) | Fassung Duc und Chiara | Fassung Duc und Alva |
|---|---|---|---|
| Ansage | Alvas Bar oder Notbar, spät. Chiara schläft bei Alva (wenn die Yacht beschädigt ist). Chiara wischt die Gläser, falsch. | gleich | gleich |
| Inhalt | Chiara: *“Four. Your glasses are a four. The bar is a nine.”* · Alva: *“And me?”* · Chiara, zu schnell: *“Not on the scale. Scales are for things.”* | Alva: *“Mina says you rated the First Officer a nine and a half. Out loud. In a bar.”* · Chiara: *“That's a classified number.”* | Chiara: *“So. You and the First Officer. Lola told me, and Lola tells everybody. Seven out of ten for hiding it.”* |
| Wende | Alva bestellt bei Chiara „in Italian“, wie Chiara es immer tut, und sagt mit Absicht „Olivetti“. Chiara lacht zum ersten Mal ohne Note. Alva: *“Nobody makes me laugh in my own bar. That's my job, Hamburg.”* · Chiara: *“There was someone once. Saint-Tropez. I never told anyone. ...I'm telling you.”* · Alva stellt zwei Gläser hin und setzt sich zum ersten Mal auf die Gästeseite der Theke. | Alva gibt Chiara ein Glas: *“Be good to him. And make him sleep sometimes. He looks like you.”* | Chiara stellt Alva einen Kaffee hin: *“I was jealous of you for three weeks. That's a ten in jealousy. I'm retiring now.”* · Alva: *“Then stay for a drink, Hamburg.”* |
| Inhalt (Sandru) | Am nächsten Morgen bringt Sandru Brot, gratis, und gibt es Chiara statt Alva: *“She laughs different now. You did that. Thank you.”* (Kanon „Fresh Bread“, hier an Chiara; kein Paar mit Sandru) | entfällt | entfällt |
| Handlung (Duc) | Chiara: *“First Officer, is it strange to get a best friend at twenty-nine? I never had one.”* · Chips: “It's not strange. It's a nine.” · Smiles and says nothing. · “Tell her, not me.” | Chiara: *“Is it strange that she's nice to me now?”* · Chips: “It's the best thing that happened all week.” · “She's nice to everyone. You just noticed.” | Alva: *“Hamburg's not bad, o figliolu. Do you mind if she drinks here?”* · Chips: “She can drink here every night.” · “Only if she pays.” |
| Wirkung | Im Festbild tanzen sie nach Alvas Flamenco zusammen, wie zwei alte Freundinnen. Chip „Tell her“: Chiara sagt es Alva selbst, Alva sagt im Festbild ein Wort: *“Ten.”* | Chiara und Alva mischen zusammen das Getränk (Los *The Festa Drink*) | gleich |

### 7.3 Isabelle und Sophia · „A Line in the Margin“ (wholesome, Freundschaft)

| Beat | Volle Fassung | Fassung mit Duc und Sophia |
|---|---|---|
| Ansage | Kloster, Apotheke bei Nacht. Sophia schläft hier (wenn die Yacht beschädigt ist) oder kommt für Kräuter. Isabelle hat schon wieder etwas explodieren lassen. | gleich |
| Inhalt | Sophia hilft beim Aufräumen, ohne Show. Isabelle: *“Sorry. Sorry, it was only rosemary.”* · Sophia: *“Darling, I've seen worse things explode. Usually men.”* | gleich |
| Inhalt | Isabelle fragt, was Sophia nachts schreibt. Rückbezug auf ihr Gespräch mit Mina auf dem Berg: *“Mina once said to me, up on the hill, 'You could have left.' Did you ever leave somewhere, Sophia?”* | Isabelle: *“Mina says you and the officer talk every night. She just knows things. Is it true?”* · Sophia: *“Darling, Mina knows everything. Don't tell Lea.”* |
| Wende | Sophia schreibt eine Zeile für Mut an den Rand von Isabelles Kräuterbuch und geht. Isabelle liest sie, als Sophia weg ist. Erzählerin: *She reads it twice. Then she smiles at the rosemary.* Die Zeile bleibt im Spiel ungesagt. | Sophia schreibt Isabelle eine Zeile für Mut, keine Liebe: *“For when you want to leave somewhere. Or stay.”* |
| Handlung (Duc) | Isabelle, am nächsten Morgen: *“Sir, is it wrong to keep a line somebody wrote for you?”* · Chips: “No. It's yours.” · “Ask Nonna. She'll know.” · “Read it once more, then decide.” | Isabelle: *“She's brave, isn't she? Is it hard, being brave?”* · Chips: “Ask her. She'll tell you it isn't.” · “Yes. She does it anyway.” |
| Wirkung | Isabelle steckt zur Festa eine Rosmarinblüte an Sophias Mantel (Los *The Garden*). Chip „Ask Nonna“: Nonna sagt nur *“Keep it. Friends are rare up here.”* | Isabelle sitzt bei Sophias Lesung in der ersten Reihe |

### 7.4 Mina und Lea · „Two Letters“ (wholesome, Freundschaft)

| Beat | Volle Fassung | Fassung mit Duc und Lea |
|---|---|---|
| Ansage | Minas Zimmer über der Post (nach dem Wiederaufbau) oder die Vespa am Kai. Lea schläft bei Mina (wenn die Yacht beschädigt ist). | gleich |
| Inhalt | Lea: *“Did you know some letters are older than the people who carry them?”* · Mina: *“I know. I carry one. It's from my brother. In Montréal. I never opened it.”* · Lea: *“I have one too. The Azores. I opened it. That's worse.”* | Mina: *“So. You and the Yacht. I didn't read it anywhere. I just know.”* · Lea salutiert, rot. *“Did you know octopuses can change colour? I'm doing that now.”* |
| Wende | Sie tauschen die Briefe, jede liest den der anderen nicht, sie halten sie nur. Mina: *“If you go, I'll bring your post. To the Azores. On the Vespa.”* · Lea: *“That's two thousand kilometres.”* · Mina: *“I'm fast.”* | Mina: *“If he's slow, honk at him. I'll lend you the horn.”* |
| Handlung (Duc) | Mina: *“Yacht. Do you think we should open them? Both?”* · Chips: “Together, then. On the same day.” · “Only if you both want to.” · “Not yet. Keep them for the festa.” | Lea: *“Duc, Mina says you're slow. Are you slow?”* · Chips: “Very. On purpose.” · Holds up two fingers. |
| Wirkung | „Together“ oder „festa“: Auf der Festa öffnet Mina Dumès Brief (Kanon: sie öffnet ihn am Ende und entscheidet selbst, ob sie bleibt), Lea sitzt daneben | Minas Girlande (Los) bekommt Leas Karte von der Bucht |

### 7.5 Holm und Petru · „The Metre“ (wholesome, immer voll)

| Beat | Zeilen |
|---|---|
| Ansage | Mole, Abend. Holm schläft bei Petru (wenn die Yacht beschädigt ist) oder sitzt nach der Reparatur am Kai. Ein Meter zwischen ihnen. |
| Inhalt | Holm: *“My mother is coming. For the festa. She wants to see the man who taught me to sit still.”* · Petru: *“Who?”* · Holm: *“Don't.”* |
| Inhalt | Holms Telefon klingelt: Ingrid (Kanon). Holm: *“Ingrid. A woman I loved, forty years ago, in Norway. She found my number. She has a daughter now.”* · Petru: *“Good.”* |
| Handlung (Duc kommt vorbei) | Holm: *“Frankfurt. Are you lost, or are you staying?”* · Chips: Walks on quietly. · “Evening, you two.” · Sits down on the far end of the bench. |
| Reaktion | still weiter: Erzählerin: *When you look back, the metre between them is gone.* · stören: *“Go away, Frankfurt.”* · Petru: *“Go away.”* · hinsetzen: Petru reicht Duc wortlos ein Bier, Holm rückt einen halben Meter näher an Petru. |
| Wirkung | Holms Mutter auf der Festa, Petru bringt zwei Gläser (5.27). Mit „still weiter“ sitzen sie im Festbild auf derselben Bank |

### 7.6 Bibi und Maxwell · „Six Kilos of Bad Temper“ (wholesome, Freundschaft, Tag 26 bis 29)

Bedingung: `rt_bibi_bleibt`, Station offen und **Bones gerettet** (Bartgeier, `geier` in `mochis.tiere`). Ohne Bones kommt das Ereignis nicht, und Maxwell fliegt an Tag 30 mit seiner Angst (5.14 ohne Zusatz).

| Beat | Volle Fassung | Fassung mit Duc und Bibi |
|---|---|---|
| Ansage | Tierstation am Morgen. Maxwell trägt zwei Eimer mit Knochen, so weit weg vom Himmel wie möglich. Über ihm kreist Bones, drei Meter Flügel. | gleich |
| Inhalt | Maxwell: [gasp] *“Eish! Bibi. The big bird is looking at Mr. Maximum.”* · Bibi: [laugh] *“That's Bones. Six kilos. Three metres of wing, and six kilos! He's mostly air and bad temper. He's looking at the bucket, chéri.”* | gleich |
| Inhalt | Bibi weiß von seinem Flug (Mina hat es erzählt). Bibi: *“In four days you sit in a plane for eleven hours. And you're scared of a bird who eats only bones?”* · Maxwell, leise (Kanon: leise nur, wenn es ernst ist): *“Mr. Maximum is scared of everything that flies, sister. Everything.”* | Bibi: *“Duc says you're the bravest man on the boat. Mina told me he said it. So. Prove it.”* |
| Wende | Bibi legt einen Knochen auf Maxwells offene Hand. Bones landet, nimmt ihn und fliegt wieder hoch. Bibi: *“A plane is just a big bird with no bad temper. You just fed the worst bird in Corsica.”* · Maxwell: *“...Mr. Maximum fed the worst bird in Corsica.”* | gleich |
| Handlung (Duc) | Maxwell: *“Number One. Is it the same, a plane and a bird? Tell me it is the same.”* · Chips: “It's the same. Only the plane is nicer.” · “No. The plane is safer. Bones is not.” · Puts a bone in his own hand, next to Maxwell's. | Bibi: *“Is he ready, Duc? Yes or no?”* · Chips: “Yes. He fed Bones.” · “Nearly. One more bone.” |
| Wirkung | In 5.14 (Tag 30) sagt Maxwell: *“Bibi says a plane has no bad temper. Mr. Maximum fed Bones. Mr. Maximum can sit in a plane.”* Im Festbild landet Bones auf dem Dach hinter Maxwell, und Maxwell winkt ihm | gleich |

### 7.7 Charly und Danzel · „Ten“ (wholesome, ein Paar, beide ein bisschen seltsam)

Bedingung: `rt_charly_bleibt`, nicht `rt_charly_weg`. Kanon: Danzel eröffnet „Le Théâtre Rouge“ an der Piazza, Charly baut ihm die Kasse, ihre erste 10 gibt sie in Akt 3 Danzel für etwas, das er genäht hat (`charly.md`, `danzel.md`). **Ein echtes Paar** (E-127): zwei Menschen, die beide etwas seltsam sind und sich genau dafür lieben. Wholesome. In der Szene zeigt sich die Nähe in Gesten, **der erste Kuss kommt auf der Festa** (Duc, E-127). Weder Charly noch Danzel ist für Duc romanzierbar, darum gibt es nur die volle Fassung.

| Beat | Zeilen |
|---|---|
| Ansage | Le Théâtre Rouge, spät. Stoffe überall, an der Theke eine halbfertige Kasse mit offenen Kabeln. Charly sitzt auf dem Boden mit dem Laptop. Danzel näht. |
| Inhalt | Danzel, als Duc hereinkommt, in seiner Fluchtformel: *“Halt! Nobody touches the fabric, or nobody... nobody touches it very much.”* · Charly, ohne aufzusehen: *“Four out of ten. You got shorter again.”* · Danzel: *“It's getting smaller because I mean it less!”* |
| Inhalt | Charly: *“The cash register works. It says 'Merci' in a robot voice. I couldn't make it stop.”* · Danzel: *“Leave it. It's the only thing in this shop that's polite to me.”* |
| Wende | Danzel steht auf, wird ruhig und genau (Kanon: nur bei Stoff). Er legt Charly einen grauen Kapuzenpulli hin, mit einer Innentasche genau für ihren Laptop und dem Wort RED innen am Kragen, klein. *“Hold still. Your left sleeve has been two centimetres short for three years. I noticed on the first day.”* · Charly zieht ihn an. Lange Pause. *“...Ten.”* · Danzel, die Stimme kippt nach oben: [gasp] *“Ten? TEN? Nobody has ever... Duc, did you hear that?”* |
| Wende 2 | Charly, monoton wie immer, und gerade darum trifft es (Kanon): *“I want to stay. Here. In the shop. With you. That's not a rating, Danzel.”* · Danzel versucht die Formel und bricht: *“Then... then nobody leaves! Nobody leaves very... nobody leaves.”* · Erzählerin: *For once, he finishes the sentence.* |
| Handlung (Duc) | Charly: *“Duc. I've never given a ten. And I've never said that other thing either. Was it a mistake? Be honest.”* · Chips: “No. That was the best ten I've ever heard.” · “Give him a nine next time, so he stays humble.” · Looks at Danzel, who is crying into a curtain, and quietly leaves them alone. |
| Reaktion | erste: Charly: *“Okay. Then it stays a ten. Don't tell Bibi. She'll cry louder than him.”* · zweite: Danzel: *“Never! I will never be humble!”* · dritte: Erzählerin: *Behind you, Charly hands him a piece of fabric to dry his eyes. Then she doesn't let go of his hand.* |
| Wirkung | Im Festbild sitzen beide auf den Stufen vor Le Théâtre Rouge, Charly im Pulli über ihrem Festa-Kleid, ihre Hand in seiner. Die Kasse am Stand sagt „Merci“. Nach Alvas Flamenco steht Charly auf, sagt *“Ten”* und küsst Danzel, kurz und vor allen. Danzel: [gasp] *“In public?!”* · Charly: *“Eleven.”* · Bibi, mit `rt_bibi_bleibt`: [laugh] *“Finally! I had a bet with myself. I won.”* |

## 8. Die Enden lesen den Akt

| Säule | Akt 3 zahlt ein über | Erfüllt, wenn (Vorschlag) |
|---|---|---|
| **Wahrheit** | Whites Einsatzplan, Kassenbuch „alles“, Siris Post, Sophias Notizen, Funk-Aufnahme und Mitschrift, Funkbuch, Nachtwache, Kiste, `mo_kommission` (setzt `mo_kommission_gesehen`, der Beweisstand selbst liegt in `kern/mochis`), Adriens Fotos, Steuerchip, Red-Trio-Aussagen | 3 Beweise, oder 2 mit „alles“ |
| **Geld** (Entscheid g) | **drei Wege, einer reicht:** Margot geborgen · Yamamoto Bindung 5 · Megans Wende (`a3_megan_wende`). Ein gescheiterter Tauchgang nimmt nur den ersten Weg | ein Weg |
| **Gemeinschaft** | Zeugen, Kassenbuch „teil“, Baustellen fertig, Casanova Vertrauen, Geldkassette der Margot zurück (Kanon `enden.md`), Ruf ab 5 als Bonus | 5 Zeugen, oder 4 mit „teil“ |
| **Stärke** | Endkampf gewonnen oder Festnahme | `a3_alon_besiegt` oder `a3_alon_festgenommen` |

Sichtbar im Schlussbild: Lose (was steht, wie es aussieht), wer im Netz fehlt (Minicu steht immer im Bild), wer nach Mitternacht an der Mole steht, die Paare. Die Enden-Tabelle in `enden.md` bleibt. Buenaventura: Eco Tours nur bei freier Bucht.

## 9. Register der Belagerungs-Flags

| Flag | Szene | Wirkung |
|---|---|---|
| `bl_tafel` | 5.5 | Megans alte Liste |
| `bl_verband_wolff` / `_chiara` / `_maxwell` | 4.1 / 6 / 5.14 | Legion baut, Chiaras Zeile, Maxwells Glücksbringer |
| `bl_verband_duc` | – | bewusst ohne |
| `bl_funk_white`, `bl_funk_charly` | 5.25 | Beweise |
| `bl_tueren_petru` | 2 | Tür; senkt die Schwelle fürs Rudern (Code `fix-akt2`), 5.1 liest `bl_dorf_rudert` |
| `bl_tueren_lola` | 4.3 | *The Menu* |
| `bl_tueren_mina` | 2, 5.4 | Tür, Zeile |
| `bl_batu_norden` | 2, 5.25 | Tür, Aussage |
| `bl_nachtwache_*` | 5.24, 5.25 | Hof, Beweis |
| `bl_nachtwache_niemand` | – | nicht mehr gelesen; Holms Zeile in 5.10 liest das neue `bl_nachtwache_pascal` |
| `bl_wache_gesehen` | 5.7 | Funkbuch |
| `bl_kirche_jana` | 4.3 | Los *The Pictures* |
| `bl_kirche_don`, `bl_kirche_don_schlaeft` | 4.3, 5.25 | *The Bell* mit Zusatzzeile, Dons drei Aussagen |
| `bl_kirche_casanova` | 5.27 | die lange Geschichte |
| `bl_will_ab_<pid>`, `bl_ab_fertig_<pid>` | 6 | Rückbezug |
| `bl_ab_fertig_*`, `bl_na_fertig_*` (keins gesetzt) | 5.5 | Holms Satz |
| `bl_minicu_kevin` (Event-ID, Tag 3) | 5.27 | Kevin landet auf Minicus Kopf |
| `gefeuert_<pid>` | 4.4, 5.1, 5.25, 7 | Ersatz oder Paar entfällt |
| `tk_haus_weg_<id>` | 4.4, 5.17, 6, 7 | Notquartier statt Gastgeberhaus |
| `bl_will_na_<pid>`, `bl_na_fertig_<pid>` | 5.21, 6 | oben in der Liste, „zusammen“ |
| `bl_alva_runde` | 4.1, 6 | Papas Tafel |
| `bl_minicu_duc_zuerst` | 5.27 | „You came first“ (auf der Festa) |
| `bl_minicu_sag_es` | 5.8 | Satz im Brief |
| `bl_minicu_gewartet` | – | bewusst ohne |
| `bl_blatt_gefunden` | 5.20, 5.27 | Handschrift, Namensblatt zurück |
| `bl_werkstatt_heil` | 4.1 | keine Baustelle |
| `sophia_notizen`, `siri_wartet`, `siri_darf_posten` | 5.25, 5.9 | Beweis, Siris Wahl |
| `sirene_weg`, `ligeia_freund` | 6 | Flaschenpost |
| Rettungen, `tk_haus_geflickt_` | 4.1 | Vignette oder Stufe 1 |
| Rudern | 5.1, 5.25 | neues Flag `bl_dorf_rudert` (F-21) |
| `tk_yacht_weg` | 4.4 | schwer beschädigt, Reparatur |
| `danzel_festa_auftrag`, `chiara_festa_kleid` (Wirkpunkt-Audit) | 4.3 | Los *The Dresses* |
| `rt_charly_bleibt`, `rt_charly_weg` | 5.28, 7.7 | Charlys Geld, Freundschaft mit Danzel |
| Bones gerettet (`geier` in `mochis.tiere`) | 7.6, 5.14 | Maxwells Übung vor dem Flug |
| `rt_bibi_bleibt` | 5.12, 7.6 | Idee, Freundschaft mit Maxwell |
| `belagerung_gewonnen` | 5.1, 8 | Akt 3 startet nur danach normal; ohne Sieg ist das Dorf stiller (Baustellen bleiben, Fassung beim Bau) |
| `rt_ausgang_alle` (wie `rt_ende_alle`) | 5.7, 5.25 | Red-Trio-Aussagen |
| `holm_zurueck` | 5.5, 5.10, 7.5 | Holm war in der Schlacht dabei, Rückbezug mit Erinnerung |
| `nacht_bei` (Zustand, je Welle) | 6 | wer die Nacht vor einer Welle bei Duc war, Rückbezug in der Schluss-Szene |
| `werte.belagerung_prozent` | – | **nie lesen** (E-124) |
| **neu:** `bl_dorf_rudert` (F-21), `bl_nachtwache_pascal`, `gr_riscossore_gesehen` | 5.1, 5.10, 5.13 | beim Bau setzen |

## 10. Gags, Ton, Englisch, Tags

- **Gags** bis Tag 31, **Yacht-Gags ab Tag 25** (Entscheid a). Vorher Texte prüfen, die Alon, Holm, Festa, „tomorrow“, Megan an Bord, Pascal, Minicu (Entscheid c: niemand sieht ihn bis Tag 35), Maxwell (Tag 30 bis 32) oder die Yacht voraussetzen. Ab Tag 32 gagfrei.
- **Ereignis-Dichte:** Woche 4 Faktor 0,6, Woche 5 0,45 (F-17).
- **Ton (Ziel):** 35 % warm, 25 % komisch, 20 % ernst, 20 % frech.
- **Englisch:** Rückbezüge mit Erinnerung, Erzähltext im Präsens, keine seltenen Wörter ohne Not.
- **Turbo-Tags:** jede vertonte Zeile beim Bau mit mindestens einem Tag in `stimme_tags.json`, weil sie am endgültigen Wortlaut hängen. Das Drehbuch setzt sie nur dort, wo das Geräusch die Szene trägt.

## 11. Brain Trust zu Version 3

### Gegenrede

**Sienna (Game Direction):** Die Unterkünfte während der Reparatur sind der beste Einfall dieser Fassung: Wer bei wem schläft, erzeugt die Paare von selbst, wie die Wohnheim-Wochen in Persona. ✨ Kritik: Minicu fehlt zwölf Tage lang, und das Spiel erinnert nur dreimal an ihn. Gegenvorbild Mass Effect 2, wo man ein fehlendes Crew-Mitglied einfach vergisst. Gegenvorschlag: Kevin sitzt jeden Morgen auf dem Kirchendach, eine Zeile der Erzählerin in jeder Vignette.

**Aly (Tech):** Zwei Code-Branches mit denselben Korrekturen sind eine Falle. Wer den falschen mergt, hat Stahl ab Tag 22 statt 24 und Dons Leben in Welle 5 statt 6. 🤓 Gegenvorschlag: `fix-akt2` nehmen, `fix-akt2-folgen` als Vergleich liegen lassen und das Drehbuch nur gegen `fix-akt2` prüfen. Dazu brauchen die Paar-Ereignisse eine Regel im Pool, sonst kommen zwei an einem Tag.

**Luise (Art & Story):** Chiara und Alva sind die mutigste Paarung, und genau darum heikel: Alvas Satz vom starken Mann ist Kanon. Ihre neue Fassung (*“someone who doesn't let me carry everything”*) verrät ihn nicht, aber Duc muss sie lesen. 🥺 Bei Isabelle darf kein Satz so klingen, als müsse sie wählen. Gegenvorschlag: Die Zeile am Rand bleibt im ganzen Spiel ungesagt.

**Maelle (Producerin):** Preis: rund 45 Szenen, grob 800 Sprechzeilen, fünf Paare mit bis zu drei Fassungen, 8 Hintergründe, 10 Sprite-Wünsche. Das sind sechs Bau-Sitzungen. 📋 Kritik: 13 Lose und ein Bonus-Los sind viel. Gegenvorschlag: Alle Lose schreiben, aber in Woche 4 nur 8 an die Tafel hängen, die anderen 5 kommen nach dem ersten fertigen Haus.

**Sora (Spielerstimme / QA):** Minute 1: Petru tritt vor. Minute 30: Rosi zählt die Wartemusik der Eden-Hotline, elf Minuten, ich lache laut. 😂 Minute 100: Die Kirchentür geht auf, Minicu klatscht zu laut, und ich heule. 😭 Nochmal-Lust 5. Veto: Wenn die Paar-Ereignisse nur Zuschauen sind, langweilt es mich. Gegenvorschlag: In jedem Paar hat Duc eine Wahl, die im Festbild sichtbar wird. 🔥

### Verbesserungsrunde (übernommen)

- Kevin sitzt an jedem Morgen von Tag 25 bis 34 auf dem Kirchendach, eine Zeile der Erzählerin in der Vignette. Damit vergisst niemand Minicu, und auf der Festa landet Kevin auf seinem Kopf (Rückbezug auf Tag 3, `bl_minicu_kevin`).
- Paar-Ereignisse im Pool: höchstens eins je Tag, Vorrang 65 %, spätestens Tag 33 als Nachzügler.
- Lose: 8 hängen ab Tag 26, die übrigen 5 nach dem ersten fertigen Haus.
- Jedes Paar hat eine Duc-Wahl mit Wirkung im Festbild (in 7.1 bis 7.5 eingetragen).
- Das Drehbuch rechnet mit `fix-akt2` (Kopf, 4.3, 9).

### Kurze Runde zu Version 3.3 (Baustoffe je Haus, Charly)

**Sienna (Game Direction):** Jedes Haus führt zu einer anderen Mechanik, wie die Gemeinschaftszentrum-Bündel in Stardew Valley. So wird der Wiederaufbau zum Grund, angeln oder in den Steinbruch zu gehen. ✨ Kritik: Vier Rezepte zu je drei Stufen sind zwölf Kostenzeilen, das riecht nach Einkaufsliste. Gegenvorschlag: Die Karte zeigt nur die nächste Stufe eines Hauses, nie alle zwölf.

**Aly (Tech):** `aufbau.STUFEN` wird ein Wörterbuch je Haus, die 20 % von Charly sitzen an einer Stelle in `braucht`. 🤓 Kritik: Abrunden macht aus 1 Iron eine 0. Gegenvorschlag: mindestens 1 (eingetragen).

**Sora (Spielerstimme / QA):** Charly sagt „Eight for borrowed“ zur Bürgermeisterin, ich liebe das. 😂 Veto: Wenn ich Charly verloren habe, darf das Spiel mich nicht bestrafen. Gegenvorschlag: Ohne Charly bleibt alles bei den vollen Kosten, kein Satz erinnert an die verpasste Hilfe.

**Maelle (Producerin):** Ein nächster Schritt, Duc: Prüfe die Tabelle der Baustoffe in 4.1, ob dir die Zahlen passen. 📋

**Maelle (Producerin):** Ein nächster Schritt, Duc: Lies Abschnitt 7 und gib die beiden heiklen Paare frei oder nicht, Chiara mit Alva und Isabelle mit Sophia. Davon hängen die meisten neuen Zeilen ab. 📋

## 12. Bauplan (nach Ducs Ja)

| Paket | Inhalt |
|---|---|
| A · Kalender **(gebaut 04.11., siehe 12a)** | Branch `fix-akt2` mergen, Kalender bis Tag 35 (`zeitraster.tage`), Gags bis 31, Yacht-Gags ab 25, Dichte je Woche, `bl_dorf_rudert`, Beta-Schluss aufheben |
| B · Woche 4 und Dorf | 5.1 bis 5.11, `kern/aufbau` in `eden.py`, Piraten nur an angefangenen Häusern, Dank-Szenen, Vignetten, Yacht (4.4) |
| C · Zeugen und Lose | Liste, Türen, Haltungen, 13 Lose |
| D · Woche 5 | 5.12 bis 5.24 |
| E · Romanzen und Paare | Abschnitte 6 und 7 |
| F · Kommission, Festa, Enden, Stimme | 5.25 bis 5.27, Festa-Schalter (F-22), Säulen, `stimme_tags.json` |
| G · Tests | `test_akt3_kalender`, `test_zeugen`, `test_lose`, `test_paare` (Fassungen nach Romanze), Bot-Lauf mit zwei Profilen vor Paket D |

### 12a. Paket A, wie es im Code wirkt (gebaut 04.11.2026)

| Mechanik | Auslöser | Wirkung | Grenzen | Stelle im Code |
|---|---|---|---|---|
| **Akt-3-Schalter** | `AKT3_SPIELBAR` in `modul_eden_rise.py`, im Modul `akt3_spielbar` | `false`: Kalender endet nach Tag 23, Beta-Schlusskarte Akt 2. `true`: Kalender bis Tag 35, danach Platzhalter-Karte „End of Act 3“ bis zu den Enden | steht auf `false`, bis Paket B bis F gebaut sind; sonst spielt man zwölf leere Tage | `kern/abschluss.berechnen`, `zeitraster.tage` |
| **Freie Gags bis Tag 31** | `ereignisse_fenster.AKT2 = [8, 31]` | 73 alte Gags laufen bis Tag 31, ab Tag 32 gagfrei | Gags mit Maxwell nur bis Tag 29 (11 Events, er fliegt Tag 30 bis 32). Handy-Events (`hy_`) bleiben bei Tag 21, weil die Handy-Dateien für die Cloud-Sitzung tabu sind. Leiter-Szenen und Abende laufen wie bisher bis 35 | `werkzeuge/eden_rise/ereignisse_fenster.py` |
| **Gags an Bord ruhen bei Reparatur** | `tk_yacht_weg` ab Tag 24, bis `a3_yacht_repariert` (Abend Tag 31, Paket B setzt es) | alte Gags in Räumen an Bord (Unterdeck, Deck, Technik, Kabinen) kommen nicht, Gags an Land schon | Leiter-Szenen (`sf_`, `sfn_`) sind ausgenommen, damit Romanzen nicht stehen bleiben; ihre Orte an Land kommen mit Paket E | `kern/ereignisse.yacht_in_reparatur`, `an_bord`, `passt` |
| **Ereignis-Dichte je Woche** | Tag 24 bis 28 | Zufalls-Events mit Faktor 0,6 statt 0,45 | Handy-Faktor unverändert (0,6) | `kern/ereignisse.AKT3_WOCHE4` |
| **`bl_dorf_rudert`** | Ende einer Welle mit Kapitän, in der das Dorf rudert | Flag bleibt nach der Belagerung, Akt 3 liest es (5.1, 5.25) | einmal je Durchlauf | `kern/taktik.rudern_merken` |
| **Holms Revanche ab Tag 24** | `HOLM_TAG = 24` | Holm wird erst nach der Belagerung vierter Gegner beim Schießen | | `kern/schiessen.py` |

| **Baustellen (Paket B1)** | Karte „Lend a Hand“ (Ort `a3_baustellen`, eine Phase): Duc wählt das Haus und wer den ersten Stein mit ihm setzt (Besitzer +4 Vertrauen, ein Pirat: Buenaventura +2 und Ruf +1, Crew: Moral +1) | Duc liefert die Baustoffe der nächsten Stufe in Nonnas Fenster, Reiter „Village“ (keine Phase). In der Nacht bauen die Piraten jede gelieferte Stufe. Charlys Geld: 20 % weniger je Posten, abgerundet, mindestens 1 | nur nach `buenaventura_schwur`, nur an begonnenen Häusern, je Haus und Nacht eine Stufe, alles oder nichts | `kern/aufbau.py`, `eden.py` (Tagesende, `baustelle_liefern`), `client/plugins/eden-farm/eden-farm.js` |
| **Dank-Szenen** | Morgen nach `aufbau_fertig_<id>` (`flag_seit`) | Besitzer dankt und öffnet die Zeugen-Tür (`a3_zeuge_<id>` mit Haltung `_ehrlich` oder `_frei`). Mina, Bà Tư, Alva, Petru | dritte Wahl verschiebt die Frage, die Tür bleibt dann über spätere Karten offen | `a3_dank_*` |
| **Totòs Kiste** | Tag 25, nur mit Versprechen aus der Grotte, Kiste genommen und noch nicht genutzt | `alon_kiste_genutzt` (Beweis), Totò +6 | neue Bedingung `{"versprochen": [an, Wort]}` | `kern/regeln.py`, `a3_uhr_toto` |
| **Reparatur der Yacht** | `tk_yacht_weg` | vier kleine Szenen im Pool (Hotline, Propeller, Tür, Tag 31 „Ugly“ setzt `a3_yacht_repariert`), Probefahrt Tag 32. Ohne Schaden: eine kleine Szene „Mostly Cosmetic“ | ab Tag 25; Maxwell nur bis Tag 29; Rosi gefeuert: Maxwell spricht ihre Zeile in „Ugly“ | `a3_yacht_*`, `a3_probefahrt` |

Test: `tests/test_akt3_kalender.py`, `tests/test_aufbau_akt3.py`, `tests/test_akt3_woche4.py`.

**Paket B2, gebaut (Woche 4, `ereignisse_akt3_woche4.py`, 34 Events, 157 gesprochene Zeilen):** 5.1 The Morning After, 5.2 The Oath, Lend a Hand (vier Baustellen), Dank-Szenen, 5.3 Alva (Karte), 5.4 Under Control mit Totòs Kiste, 5.5 Until I Land, 5.6 die Festa-Tafel, 5.7 Sunday mit Don an der Tür und der Schublade, 5.8 Nonnas Kiste (Karte), 5.9 Siri (Karte), 5.11 Every Report, die Yacht (4.4), 5.28 Charlys Geld.
**Paket B3, gebaut:** Morgen-Vignetten ohne Phase in der Meldung „Day X is over“ (`kern/akt3.morgen`): Kevin auf dem Kirchendach Tag 25 bis 34 außer 26, Dank je eines heilen Hauses Tag 25 bis 28, die Legion baut mit `bl_verband_wolff` einmal eine Stufe. 5.10 Holms Revanche als Szene im Pool (`a3_revanche`, Tag 24 bis 29), Holms Vorwurf nur mit dem neuen Flag `bl_nachtwache_pascal` (in `bl_nachtwache` gesetzt). Minas Ersatz mit dem Kellerschlüssel an Tag 31 (`a3_nonna_mina`).
**Wandert nach Paket E:** Wer schläft wo, Megans Raum bei `tk_yacht_weg`. Angepasst: `tests/test_akt2_events.py` (neue Fenster), `tests/test_holm_wette.py` (Tag 24, lokal nicht prüfbar wegen `eden-config.json`). Alle `test_*.py` vor und nach Paket A: 47 gegen 48 grün, kein Test hat seinen Status verloren.

## 13. Was aus den Befunden wurde

Gegenrede G1 bis G19 und die 30 Funde der Prüfung von v2 sind in v2.1 eingearbeitet (dort Abschnitt 12, `git show 41ae2ac:docs/wiki/welt/drehbuch_akt3.md`). Version 3 behält diese Lösungen. Was sich durch Ducs Entscheide geändert hat:

| Befund | Stand in Version 3 |
|---|---|
| G1 Sonnenbrille | bleibt eingearbeitet |
| G2 Rädchen | bleibt (5.24) |
| G3 Kommission | bleibt (5.25), Minicu fehlt dort jetzt bewusst |
| G4 Woche 4 | bleibt: 6 gegen 16 Pflicht. Yacht-Szenen als Vignetten und Pool, nicht als Pflicht |
| G5 Zeitbudget | neu gerechnet mit Losen und Paaren. **Nicht eingearbeitet:** Bot-Lauf (kein Kalender gebaut) |
| G6 Wochentage | bleibt |
| G7 Petru | bleibt, zwei Fassungen |
| G8 Alva | bleibt. Neu: ihre Frage nach Minicu bekommt keine Antwort (Entscheid c) |
| G9 Zeugen | bleibt. Minicu nicht mehr auf der Liste (Entscheid c) |
| G10 Einkaufsliste | **neu gelöst** mit Duc: Lose ohne Zähler (Entscheid d) |
| G11 Flags | bleibt, Register erweitert um `danzel_festa_auftrag`, `chiara_festa_kleid` |
| G12 Romanzen | bleibt, dazu Abschnitt 7 |
| G13 schwere Gipfel | bleibt: nur Switched Off. Minicus Rückkehr ist Freude, kein Gipfel der Schwere |
| G14 Doppelungen | Applaus jetzt mit Minicu auf der Festa, kein Klatschen an Tag 26 |
| G15 Kanon-Brüche | bleibt |
| G16 Siri | bleibt, mit `siri_wartet` jetzt eine echte Wahl (Minicu ist unbekannt) |
| G17 Säule Geld | **neu mit Duc** (Entscheid g): drei Wege, einer reicht |
| G18 Englisch | bleibt |
| G19 Fragen vor Chips | bleibt |
| v2-Prüfung 2 (Yacht) | **neu mit Duc** (Entscheid a, b): schwer beschädigt, Reparatur, Unterkünfte |
| v2-Prüfung 8 (Sandru) | Vorschlag bleibt (F-24) |
| v2-Prüfung 1 (Festa-Fenster) | bleibt als Frage F-22 |

## 13b. Prüfung von Version 3 (unabhängiger Prüfer, 30 Befunde)

| Nr | Befund | Stand in 3.1 |
|---|---|---|
| 1 | Unterkünfte setzen stehende Häuser voraus | Notquartier in der Kirche (4.4), 5.17 und Alva (6) mit Fassung „Baustelle“ |
| 2 | gefeuerte Crew fehlt | Ersatz je Szene (4.3 *The Lights*, 4.4, 5.1, 5.25), Paar entfällt (4.4), Register |
| 3 | Sandru ohne Schiene kann nicht stehen | Alons Angebot „legs for silence“ in 5.17; Fall „vorher befreit“ in 5.17 und F-24 |
| 4 | Maxwell: Durban, Abwesenheit, dritte Person | eingearbeitet (5.14, 4.4) |
| 5 | Don ohne `bl_kirche_don` | drei Fassungen (5.25) |
| 6 | Nachtwache-Flags | neues `bl_nachtwache_pascal` (5.10), Elsa-Fassung (5.7) |
| 7 | „Frankfurt slept“ | Bedingung über `bl_ab_fertig_*`/`bl_na_fertig_*` (5.5) |
| 8 | Casanova „I signed nothing“ | neue Zeile über das Papier auf den Stufen (5.25) |
| 9 | Riscossore Flag und Anzug | `gr_riscossore_gesehen`, Leinenanzug (5.13) |
| 10 | `HOLM_TAG` auf `fix-akt2` noch 22 | Falle im Kopf, 5.10, F-30 |
| 11 | Bibi: Sprecher vertauscht | eingearbeitet (6) |
| 12 | Leas Zeichen | Vordeck mit Bedingung, sonst Kalmare (6, 5.21) |
| 13 | Megan: Bedingung, Doppelung, Fenster, Sprite-Set | „Still Off the Record“ mit Rückbezug auf den Anruf, Tag 26 bis 30 (6) |
| 14 | Rückbezüge ohne Bedingung | Bedingungen und Ersatzzeilen (6, 7.1, 7.5) |
| 15 | Alvas Wunsch, „free drinks“ | „I said it once, to an empty bar“, „wrote down every glass“ (7.2, 6) |
| 16 | „six years“ | „since her mother left for Seville“ (5.17) |
| 17 | „Nacht der Türen“ | „that day, when the phones were dead“ (2, 5.4, 5.25), Minas Epilog-Pointe geschont |
| 18 | Chiara und Sophia, Schwelle, Vorrang, Tratsch | Kanon-Zeile, Leiter-Stufe 3, Vorrang-Regel, Tratsch über Mina (7) |
| 19 | Rosis Mutter | neue Zeile ohne Mutter (5.21) |
| 20 | Minicu in `dorf_figuren.md`, Piraten-Kanon, „Not yet“ | Vermerk in `dorf_figuren.md`, E-123 offen, „Not today“ |
| 21 | Lose: 14 statt 13, Stahl als Menge, *The Bell* | 13 plus Bonus *Capra*, Stahl als Zugang, *The Bell* mit Chips und einer Phase |
| 22 | *Not in the System* umgedeutet | Mutters Rezepte, Spalte Essen, „They found the tin.“ |
| 23 | Vignetten und Kevin | Nachsatz am Frühstück, Kevin Tag 25 bis 34 außer 26 (3) |
| 24 | Chiaras Blackout öffentlich | Abend Tag 32 allein, Ersatz bis Tag 33 (6) |
| 25 | Kalender-Brüche | Tag 35, 2,8 nur Tag 29 bis 34, Paare 0 Phasen, Nacht 34, IDs vereinheitlicht |
| 26 | Elsas Zeile am falschen Chip, unbenanntes „he“ | Zeile beim Mann, „Pascal“ (5.7) |
| 27 | Präteritum in 5.8 | Präsens |
| 28 | Dialekt, Redewendungen, „Mostly“, Totò ohne Frage | ersetzt; „Mostly“ nur noch bei Lola; Totò fragt |
| 29 | fehlende Flags | neue Flags im Register 9 (beim Bau setzen), `megan_morning_after` als Sprite-Set |
| 30 | `mo_kommission`, `beweis_stand`, Megans Kabine | Abschnitt 8 präzisiert, Gegenbedingung in 5.5, Reihenfolge bleibt F-25 |
