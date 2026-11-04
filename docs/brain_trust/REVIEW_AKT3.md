# Brain Trust · Review Akt 3 (Tag 24 bis 35)

> Stand 04.11.2026 · Branch `akt3-cloud` · Grundlage: der gebaute Code und die Daten (140 Akt-3-Events, 18 Karten, 4 Kämpfe, 529 Sprechzeilen), Drehbuch 3.5.
> **Einmal vorweg, ehrlich:** Niemand hat Akt 3 gespielt. Ohne Bilder, Ton und `eden-config.json` läuft das Spiel hier nicht. Jede Wertung ist eine Prognose aus Code, Text und Zahlen, wie eine Preview vor dem Test. Die Zahlen unten sind gezählt, nicht geschätzt.
> **Spoiler:** Diese Datei enthält Wendungen und Enden. Sie ist für Duc, nicht für Tester.

## Die Kriterien

Jede Rolle schreibt in der Form eines bekannten Formats und legt dessen Maßstab an.

| Rolle | Format | Maßstab |
|---|---|---|
| **Sienna** (Game Direction) | GameStar-Test mit Wertungskasten, dazu der Blick von Game Maker's Toolkit | Spielspaß je Kategorie, Pro und Contra, Prognose in Prozent. Haben Entscheidungen eine sichtbare Folge? |
| **Luise** (Art & Story) | Eurogamer- oder Polygon-Essay, dazu der Blick von Jacob Geller | Thema, Figuren, Ton. Sagt das Kapitel etwas, und trägt die Form das? |
| **Aly** (Tech) | Digital Foundry | Stabilität, Datenfluss, Werkzeugkette, was kaputtgehen kann |
| **Sora** (Spielerstimme / QA) | IGN-Review mit Verdict und Score von 10, dazu der Bauch von Dunkey | Macht es Spaß? Wo lacht, heult oder gähnt man? |
| **Maelle** (Producerin) | Skill Up und ACG („Kaufen, Warten, Lassen“) | Wert für die Zeit, Umfang gegen Tiefe, was vor dem Release fehlt |

## Die gezählten Befunde

| Befund | Zahl | Warum es zählt |
|---|---|---|
| Wahl-Flags der Festa-Lose, die nichts liest | **33 von 47** | Die Entscheidung im Los landet nicht im Schlussbild. Nur Bühne, Topf und Getränk tauchen auf der Festa auf |
| Wahl-Flags der Paar-Szenen, die nichts liest | **25 von 34** | Drehbuch verspricht „jede Duc-Wahl wirkt im Festbild“. Gelesen werden nur Holm, Charly, Mina und Siri |
| Antwort-Flags der Schluss-Szenen, die nichts liest | **27 von 36** | Die Antwort in der letzten Romanzen-Szene hat keine Folge |
| Haltungs-Flags der Zeugen, die nichts liest | **21 von 31** | Die Kommission sagt denselben Satz, egal wie Duc gefragt hat |
| Szenen am Hafen (`village_harbour`) | **62 von 140** | Ein Ort für fast die Hälfte. Dazu 26 auf der Piazza |
| Neue Karten (kosten je eine Phase) | **18**, davon 8 nur nachmittags oder abends | In Woche 4 können sechs bis neun Karten gleichzeitig offen sein |
| Petrus „Hm.“ in Akt 3 | **16** | Das Stimmen-Audit nannte 29 von 76 schon zu dicht |
| „Don't get used to …“ bei Alva | **4** | ein schöner Satz, der sich abnutzt |
| Szenen mit nur einem Chip | **19** | gewollt (Villa, Übergänge), aber vier davon sind Stellen mit echter Spannung |
| Fehler: Megans Schluss-Szene spielt in der VIP-Kabine | 1 | bei `tk_yacht_weg` ist die Yacht bis Tag 31 kaputt, die Karte gilt bis Tag 30 |
| Fehler: „Nach Mitternacht“ zeigt alle neun Frauen als Chip | 1 | verrät, wer romanzierbar ist, und „Not her, Yacht“ kränkt eher, als dass es neckt |

## Sienna (Game Direction) · im Stil eines GameStar-Tests

**Zwischentitel: Ein Dorf baut sich selbst, aber nur halb**

Der beste Moment kommt ohne Kampf. Duc steht am ersten Morgen mit zwei Kaffeebechern auf der Piazza, und Petru tritt vor ihn. Wer in der Belagerung das Dorf rudern ließ, hört *“I rowed out with the village, like in 1924”*. Das ist Game Maker's Toolkit in Reinform: Eine Tat aus Akt 2 kommt zurück, mit Erinnerung im Satz. Davon hat Akt 3 viele. Bà Tư erinnert an die Männer in Weiß, Alva an die Runde am Kai, Holm nur dann an den Nordweg, wenn Duc „Pascal has it“ gesagt hat. ✨

Die Baustellen sind das neue Herz, und sie sind gut gedacht. Jedes Haus schickt Duc woanders hin: Kork aus der Macchia für die Post, Granit für Bà Tưs Herd, Eisen vom Angeln für die Bar, Stahl aus dem Scrap Field für Petru. Das ist Stardew Valleys Gemeinschaftszentrum, und es verbindet vier Mechaniken, ohne eine Einkaufsliste zu zeigen. Die Karte zeigt nur die nächste Stufe. Charlys Geld macht alles billiger, ohne dass ein Spieler ohne Charly bestraft wird.

Dann die Lücke. Die Lose sind charmant geschrieben, aber 33 von 47 Entscheidungen verschwinden. Ob Petrus Tafel aus dem alten Boot oder aus der Asche ist, sieht man an der Festa nie. Mark Brown würde sagen: Eine Wahl ohne Rückmeldung ist ein Knopf, keine Entscheidung. Dasselbe gilt für die Paar-Szenen und die Schluss-Szenen der Romanzen.

| Wertungskasten | Prognose |
|---|---|
| Story und Inszenierung | 86 % |
| Figuren | 88 % |
| Spielmechanik (Bauen, Lose, Zeugen) | 71 % |
| Entscheidungen mit Folge | 58 % |
| Abwechslung der Orte | 55 % |
| **Gesamt** | **77 %** |

**Pro:** Rückbezüge mit Erinnerung · Baustellen verweben vier Mechaniken · Woche 4 atmet wirklich (6 Pflicht-Szenen, Tag 27 frei) · Minicus Auftritt
**Contra:** Wahlen ohne Echo · Kartenflut in Woche 4 · fast alles am Hafen · Endkampf ohne eigene Idee

**Gegenvorschlag:** ein Frame „The Festa, Seen from the Stage“ vor Casanovas Rede, das jedes erledigte Los mit seiner Wahl in einem Satz zeigt (*The long table is black. It used to be a house.*). Das kostet 13 mal zwei Sätze und macht 33 tote Flags lebendig.

## Luise (Art & Story) · im Stil eines Eurogamer-Essays

**Who saw it, and who said so**

Akt 3 hat ein Thema, und es zieht sich durch: Papier gegen Namen. Alon droht mit Krediten und Briefen, das Dorf antwortet mit Menschen, die laut sagen, was sie gesehen haben. Die Kommission an Tag 35 ist darum keine Gerichtsszene, sondern eine Liste von Sätzen, und jeder Satz gehört einer Figur: Mina, die an jede Tür geklopft hat; Don in drei Fassungen, nüchtern, eingeschlafen oder vor der Tür; Buenaventura, der sich selbst anzeigt. Jacob Geller würde die Stelle mögen, an der der Kommissar nach dem großen Mann am Tor fragt und Don nur sagt, er könne heute nicht kommen. Niemand fragt nach. Das Spiel hält zwölf Tage lang eine Tür geschlossen, und der Spieler spürt sie jeden Morgen über Kevin auf dem Kirchendach. 🥺

Die Freundschaften sind der zweite Faden, und sie sind die mutigste Entscheidung des Akts: Wer kein Dach hat, schläft bei jemandem, und daraus wächst etwas. Lola wird Bà Tưs Insel-Enkelin, Chiara findet in Alva die erste beste Freundin mit neunundzwanzig. Charly und Danzel sind das schönste Paar im Spiel, weil beide seltsam sind und das Spiel sie nicht dafür entschuldigt: *“That's not a rating, Danzel.”*

Die Kritik: Die Figuren treten fast immer an denselben zwei Orten auf, und das nimmt ihnen ihre Räume. Bà Tưs Laden kommt fünfmal vor, Petrus Werkstatt kaum. Isabelle und Sophia treffen sich auf den Kirchenstufen statt im Kloster, weil das Kloster kein Raum für normale Szenen ist. Und die Haltung, mit der Duc einen Zeugen fragt, verändert dessen Aussage nicht. Disco Elysium lebt davon, dass die Art der Frage die Antwort färbt.

**Gegenvorschlag:** je Zeuge zwei Fassungen seiner Aussage in der Kommission (ehrlich gefragt oder mit Druck gefragt). Und die Paar-Szenen an den Ort des Gastgebers legen: Petrus Werkstatt für Holm, Minas Post für Lea.

## Aly (Tech) · im Stil von Digital Foundry

Die Werkzeugkette hält, aber sie hängt an einem Trick. Der Neubau der Events tauscht hier ohne Bilder bei 64 alten Events den Hintergrund, der Kampf-Builder bricht an 40 fehlenden Sounds ab. Darum sind `ereignisse.json`, `auftraege.json`, `kaempfe.json` und `stimme_tags.json` gezielt ergänzt, nicht neu gebaut. Ein Abgleich zeigt: Die 140 Akt-3-Events aus dem Builder sind identisch mit den eingetragenen. Das ist sauber, aber erst der lokale Neubau mit leerem `git diff` ist der Beweis. 🤓

Stabil: 53 Tests grün, keiner schlechter als vorher, sieben neue Tests für Akt 3. Der Schalter `akt3_spielbar` steht auf aus, das Spiel endet also weiter sicher nach Tag 23.

Risiken:
- Die Prüfregeln in `ereignisse_basis.pruefe` sind für `a3_` gelockert (Holm, Megan, Kloster-Figuren, ein Chip). Das war nötig, nimmt aber Schutz weg. Ein Tippfehler bei Megan an Bord fällt jetzt nicht mehr auf.
- Megans Schluss-Szene in der VIP-Kabine bei kaputter Yacht ist ein echter Logikfehler.
- `tags_fuer` entfernt beim lokalen Neubau gleichlautende Zeilen anderer Quellen (Petrus „Hm.“). Heute ohne Schaden, aber fragil.
- Der Endkampf nutzt das Sprite eines Agenten. Level 10 ist ungetestet, und das Balancing-Audit zeigte schon bei White, dass Level 10 hart an der Kappe liegt.

**Gegenvorschlag:** eine Ausnahme für Megan nur mit `megan_zurueck`, nicht für alle `a3_`. `tags_fuer` nur gleiche Sprecher und gleiche Quelle ersetzen lassen. Megans Karte mit `nicht tk_yacht_weg oder a3_yacht_repariert` und einer Fassung in Casanovas Gästezimmer.

## Sora (Spielerstimme / QA) · im Stil eines IGN-Reviews

**Titel: Twelve Days, One Door**

Minute eins: Petru tritt vor, und ich habe Gänsehaut. Minute zwanzig: Rosi zählt die Wartemusik der Eden-Hotline, dreizehn Minuten, und sie will vor Wut weinen, wenn jemand abhebt. Ich lache laut. 😂 Tag 26: Casanova brüllt THIS IS THE FESTA, niemand klatscht, Kevin kreischt, *“...Thank you, Kevin.”* Bestes Timing im Spiel.

Dann wird es zäh. In Woche 4 habe ich irgendwann Lend a Hand, Who Saw It, The Festa Board, Scrap Field, Alva, Siri, Nonna und zwei Romanzen-Karten gleichzeitig offen. Das fühlt sich an wie eine Aufgabenliste in einem Spiel, das Durchatmen versprochen hat. Persona 5 zeigt auch viele Optionen, aber der Kalender sagt mir, was heute selten ist.

Tag 32 ist ein Tonbruch: morgens die warme Probefahrt, nachmittags wird Sandru abgeschaltet, zum Dinner kommt Maxwell lustig aus dem Flugzeug zurück, abends knutscht man vielleicht auf der Brücke. Vier Stimmungen an einem Tag.

Der Endkampf ist ein normaler Kampf mit einem stärkeren Gegner. Nach zwölf Tagen Aufbau will ich, dass die Leute, denen ich geholfen habe, mitkämpfen. Hades und Clair Obscur machen ihren letzten Boss zur Summe der Reise. Hier gibt es eine Zeile von Rosi, mehr nicht.

Und dann Tag 35: Alva klatscht langsam, dann jemand viel zu laut an der Kirchentür. Ich heule. 😭

**Verdict:** Akt 3 hat die besten Einzelmomente des Spiels und einen Mittelteil, der zu viel gleichzeitig anbietet. **Score: 7,5 von 10.** Nochmal-Lust: 4 von 5, weil ich die Enden sehen will.

**Gegenvorschlag:** Maxwells Rückkehr auf Tag 33 Frühstück. Im Endkampf ab der Hälfte ein Auftritt je Verbündetem, der da ist (Rosi mit Unit-01, Elsa, Wolff), wie in der Belagerung: sichtbare Wirkung statt Zahl.

## Maelle (Producerin) · im Stil von Skill Up und ACG

Was bekommt man für die Zeit? Zwölf Tage, rund 34 freie Phasen, 140 Szenen. Ein Spieler mit einer Romanze und allen Zeugen braucht etwa 26 bis 29 Phasen. Das passt. Der Umfang stimmt, die Tiefe noch nicht: Viele Szenen enden in einem Flag, das niemand liest. Das ist kein Inhaltsproblem, sondern eine fehlende letzte Verbindung. 📋

Was vor einem Release fehlt, in der Reihenfolge der Wirkung:
1. die Festa liest die Wahlen (Lose, Paare, Schluss-Szenen),
2. die zwei Logikfehler (Megans Kabine, Mitternachts-Chips),
3. ein Endkampf mit Verbündeten,
4. die Bilder aus der Bestellliste, sonst bleibt der Hafen die Hälfte des Akts,
5. ein Bot-Lauf über Tag 24 bis 35.

**ACG-Urteil: Warten.** Nicht, weil es schlecht ist, sondern weil zwei Tage Arbeit den Unterschied zwischen gut und sehr gut machen.

## Gegenrede

**Sienna (Game Direction):** Luise will zwei Fassungen je Zeugenaussage. Das sind 16 neue Zeilen, gut. Aber die Haltung darf nie bestrafen, so hat Duc entschieden. Also färben, nicht schwächen. ✨

**Luise (Art & Story):** Soras Endkampf mit allen Verbündeten darf den Moment nicht verwässern. Alon ist kein Kriegsgegner. Er droht mit Papier. Vielleicht sollte der Kampf kürzer sein und das Gespräch davor länger. 🥺

**Aly (Tech):** Ein Festa-Frame, der 13 Lose liest, ist eine lange Szene mit vielen Bedingungen. Besser ein Frame je Spalte (Bauen, Essen, Schmuck), jeder mit höchstens fünf Zeilen. Dann bleibt es testbar. 🤓

**Sora (Spielerstimme / QA):** Die Kartenflut ist mein größter Ärger, und keiner hat einen Gegenvorschlag gemacht. Ich will höchstens drei Karten am Tag plus die Romanze. 😤

**Maelle (Producerin):** Soras Grenze ist richtig, aber sie darf keine Karte für immer verstecken. Vorschlag: Karten haben eine Reihenfolge, die nächste kommt, wenn eine erledigt ist. 📋

## Verbesserungsrunde

| Nr | Maßnahme | Grund | Aufwand |
|---|---|---|---|
| 1 | Festa: drei Frames „Building“, „Food“, „Decoration“ vor Casanovas Rede, je erledigtem Los ein Satz mit der Wahl | 33 tote Flags, Kern von Ducs Wunsch „Aufträge entscheiden, wie voll die Festa ist“ | mittel |
| 2 | Festbild liest jede Paar-Wahl und jede Schluss-Antwort in einem Satz | 25 und 27 tote Flags | mittel |
| 3 | Kommission: je Zeuge die Aussage in zwei Färbungen (ehrlich gefragt, unter Druck gefragt), nie schwächer | Disco-Elysium-Maßstab, 21 tote Flags | klein |
| 4 | Megans Schluss-Szene: Gästezimmer bei Casanova, solange die Yacht kaputt ist | Logikfehler | klein |
| 5 | Nach Mitternacht: statt neun Chips kommen die Einladungen als eigene kurze Szenen, nur von Frauen, die bereit sind | E-060, kein Verraten der Optionen, keine Kränkung | mittel |
| 6 | Kartenflut: höchstens drei Akt-3-Karten gleichzeitig (Reihenfolge: Baustelle, Zeugen, Tafel, dann der Rest), Romanzen zusätzlich | Woche 4 soll atmen, Persona-Kalender | mittel |
| 7 | Maxwells Rückkehr von Tag 32 Dinner auf Tag 33 Frühstück | Tonbruch an Tag 32 | klein |
| 8 | Endkampf: ein Auftritt je Verbündetem ab der Hälfte, kurz (Rosi und Unit-01, Elsa, Wolff), Kampf kürzer, Gespräch davor bleibt | Hades- und Clair-Obscur-Maßstab, Luises Einwand | groß |
| 9 | Orte: Paar-Szenen beim Gastgeber, Zeugen bei sich zu Hause, weniger Hafen | 62 von 140 am Hafen | klein |
| 10 | Petrus „Hm.“ auf höchstens eins je Szene, Alvas „Don't get used to it“ einmal im Akt | Stimmen-Audit | klein |
| 11 | Prüfregeln: Ausnahmen für `a3_` enger fassen, `tags_fuer` nur gleiche Quelle ersetzen | Schutz der Werkzeugkette | klein |

**Maelle (Producerin):** Ein nächster Schritt, Duc: Gib die Nummern 1 bis 4 frei. Das sind die fehlenden Verbindungen zwischen Wahl und Folge, und sie heben Akt 3 von gut auf sehr gut, ohne neue Bilder. 📋

## Stand nach dem Umbau (04.11.2026, gleicher Tag)

Umgesetzt: 1, 2, 3, 4, 7, 9 und dazu die Lose bei den Menschen (Besuch ohne Phase, Rundgang mit bis zu drei Losen). Gelesene Wahlen: Lose 46 von 47, Paare 32 von 34, Schluss-Szenen 36 von 36. Hafen 51 von 147. Offen: 5, 6, 8, 10, 11. Einzelheiten: `docs/wiki/welt/drehbuch_akt3.md`, Abschnitt 12a.
