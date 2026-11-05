# Brain Trust: Mina Orsoni ausarbeiten und in Akt 3 einbetten

Stand 05.11.2026 · Branch `berichte-audits` · **Vorschlag, wartet auf Ducs Urteil. Nichts davon ist gebaut, der Wiki-Kanon ist
unverändert.** Was Duc annimmt, kommt als Eintrag in `ENTSCHEIDUNGEN.md` und danach auf `docs/wiki/welt/dorf_figuren.md`.

Quellen: `docs/wiki/welt/dorf_figuren.md` (Abschnitt Mina, Paare, Ablauf), `akt3.md`, `enden.md`, `drehbuch_finale.md`
(Auftrag „Türen“), `figuren/elsa.md`, `figuren/rosi.md`, `figuren/kloster.md`, `figuren/casanova.md`, gebaute Szenen in
`werkzeuge/eden_rise/ereignisse_dorf.py`, `ereignisse_belagerung.py` (`bl_tueren`), `ereignisse_schneider.py` (`strap`),
`ereignisse_legenden.py`, `ereignisse_outfit_quest.py` (`ol_dorf`).

## 1. Einordnung

**Luise (Art & Story):** Das stärkste Bild steht schon in den Quellen: eine junge Frau, die jeden Brief im Dorf zustellt und
seit einem Jahr einen einzigen nicht öffnet, ihren eigenen. 🥹 In Akt 3 bekommt sie dazu den schwersten Sack ihres Lebens:
Alons Briefe an ihre Nachbarn. Sie muss Angst austragen und trägt selbst einen Mut mit sich herum, den sie nicht aufmacht.

## 2. Raster

| | Mina Orsoni |
|---|---|
| Kanon | 24, korsische Französin, alte Vespa, Post im Dorf, nach Bastia und jede Woche zum Kloster. Frech, schnell, gut gelaunt, immer etwas außer Atem. Nennt Duc „Yacht“. Keine Pflicht-Romanze, **kein Mechanik-Erklärer** |
| Will | alles zuerst wissen, schnell fahren |
| Angst (neu, Vorschlag) | dass sie die Einzige bleibt, die nie etwas wagt; dass das Dorf in ihr nur den Briefkasten sieht |
| Widerspruch | kennt die Geheimnisse aller, niemand fragt nach ihren |
| Erkennungssätze | “I don't read them. I just know.” · “Not agaaaain!” |
| Bindungen | Elsa (große Schwester, Ex ihres Bruders Dumè), Alva (Wette, wer zuerst weiß), Casanova (keine Rechnungen), Isabelle (der Mut), Nonna (Kuchen), Pascal (Monaco-Post), Sandru (Medizin-Pakete, schweigt) |
| Gebaut | `g1_mina_post` (Tag 3, Strafzettel), `kl_mina_post` (Briefe ans Kloster, `kl_post`), „Did they read them?“ (zwei Fassungen, `mina_ernte`), `bl_tueren` (Tag 22, Flags `bl_tueren_petru/lola/mina`), Schneider-Auftrag `strap` (A Strap That Holds), vier Legenden-Zeilen, `ol_dorf` |
| Offen im Kanon | Akt 3: Alons Briefe zustellen (`akt3.md`), Minas Brief öffnen, Epilog mit Brüssel und dem Einschreiben (`enden.md`). Szene „The Back Seat“ steht aus |

**Neuer Anker (Fund dieser Runde):** Rosis Vater Salvo hat seine Vespa-Werkstatt an die Bank verloren und repariert seitdem
Roller für andere (`figuren/rosi.md`), Rosi hat schon ein Set „Vespa Sunday“. Eine Mina mit kaputter Vespa ist für Rosi
kein Auftrag, sondern Heimkehr.

## 3. Beiträge

**Sienna (Game Direction):** Mina ist unsere Kiki aus *Kiki's Delivery Service*: Sie zeigt dir das Dorf von hinten, Haus
für Haus. In Akt 3 machen wir sie nicht zur Heldin, sondern zur Verbindung, durch die jede Entscheidung von Duc sichtbar wird.
Vorbild: der Postbote in *Animal Crossing*, der Wochen später den Brief bringt, auf den man nicht mehr gewartet hat. Gegenvorbild:
die Briefträger in *Death Stranding*, wo Zustellen Arbeit wird. Bei uns stellt Mina zu, Duc fährt nur mit, und es kostet nie
mehr als eine Phase. ✨

**Aly (Tech):** Ich habe nach Doppelungen gesucht. „Zustellbuch“, „registered“ und „Einschreiben“ gibt es außer im Epilog nirgends,
also nichts doppelt. Die Grundlagen sind da: Vertrauen `mina` (0 bis 10, gestiegen durch `g1_mina_post`, `kl_mina_post`),
`kl_post_dabei`, `mina_ernte`, `bl_tueren_*`. Wichtig aus dem Wirkpunkt-Audit (`docs/berichte/wirkpunkt_audit.md`): Das
Dorf-Vertrauen wird heute nirgends abgefragt. Mina ist die ideale erste Stelle, an der es wirkt, und zwar dreifach: als Zugang
(wer hat welchen Brief bekommen), als Uhr (zwei Türen in einer Phase) und als Beweis (Zustellbuch bei der Kommission). 🤓

**Luise (Art & Story):** Der Brief von Dumè darf nicht tragisch sein, so steht es im Kanon. Mein Vorschlag für den Inhalt: Dumè
heiratet im Herbst in Montréal und fragt, ob sie seine Trauzeugin wird. Der Brief kam vor einem Jahr, die Hochzeit ist noch nicht.
Unten steht ein Satz für Elsa. Das ist warm, ein bisschen witzig und lässt Mina beide Wege offen: fliegen und zurückkommen, oder
bleiben und anrufen. 🥺

## 4. Optionen für die Einbettung

| Option | Kern | Sehnsucht | Kosten |
|---|---|---|---|
| A. Nur der Brief | Minas eigener Bogen: The Long Way Up, Brief öffnen, Epilog | Gefühl | klein (2 Szenen) |
| ⭐ B. Die Runde | Mina trägt Akt 3 als Verbindung: Vespa mit Rosi, Festa-Lieferungen, Alons Briefe mit Duc auf dem Rücksitz, Zustellbuch, Brief, Festa-Einladungen | Wirksamkeit, Zugehörigkeit, Gefühl | mittel (7 Szenen, eine kleine Mechanik) |
| C. Mina als Zeugin im Mittelpunkt | Sie sagt als Hauptzeugin aus | Wirksamkeit | klein, aber sie wird zur Erklärerin und überstrahlt Buenaventuras Aussage |

**Empfehlung ⭐ B.** Sie gibt Woche 5 (Duc überzeugt die Leute einzeln) eine Form, die sich nicht nach Verwaltung anfühlt, und
hängt den Festa-Füllstand an sichtbare Einladungen statt an eine Zahl.

## 5. Der Bogen in Akt 3 (Vorschlag ⭐ B)

Kalender nach `akt3.md`: Tag 24 bis 35, Woche 4 atmet, Woche 5 zieht an, Villa Tag 34, Kommission Tag 35, Festa als Schluss.
Vorher vorkommende Dinge tragen im Satz immer eine Erinnerung (STIL, Verständlich bleiben).

| Tag | Szene (Arbeitstitel) | Was passiert | Wirkpunkt |
|---|---|---|---|
| 24 oder 25 | **Second Gear** | Die Vespa ist in der Nacht von Welle 4 umgekippt, der Gang hakt. Mina schiebt sie über die Piazza. Rosi kniet sich hin, ohne zu fragen | Flag `mina_vespa_heil`; ohne die Szene fährt Mina in Woche 4 langsamer (eine Lieferung weniger pro Tag) |
| Woche 4, laufend | **Parcels** (klein, wiederholbar) | Casanovas Festa-Bestellungen kommen mit Mina: Mehl, Lampions, Fischkisten. Jede erfüllte Bestellung bringt sie selbst und sagt einen Satz dazu | Lieferung zählt auf die Festa-Liste; Minas Zeile wechselt nach Vertrauen |
| 27 | **The Long Way Up** | Duc fährt hinten mit, hoch zum Kloster. Eigene Szene, nicht die geplante „The Back Seat“ mit Bà Tư, Nonna und Isabelle (`dorf_figuren.md`), die bleibt. Mina zeigt ihm den Brief von Dumè und steckt ihn wieder weg | Vertrauen `mina` +; Wahl, ob Duc fragt oder schweigt (Schweigen zählt mehr) |
| 30 | **Forty-One Envelopes** | Woche 5 beginnt. Mina sitzt mit einem Sack voller gleicher A.V.-Umschläge auf der Kirchentreppe: Jobangebote, Kredite, Anwaltsbriefe. Sie muss sie zustellen, es ist ihr Beruf | öffnet die Runde (siehe 6) |
| 30 bis 33 | **The Round** | Duc fährt mit und steht an der Tür, wenn der Brief ankommt. Mina sagt, was drinsteht („I don't read them. I just know.“), Duc wählt das Argument | Zeuge gewonnen oder nicht, siehe 6 |
| 33 | **Return Address** | Mina öffnet Dumès Brief. Wer neben ihr sitzt, wählt der Spieler: Duc, Elsa oder Isabelle (Isabelle nur nach dem Kloster) | Flag `mina_brief_offen` und `mina_bleibt` oder `mina_fliegt`, beides gut |
| 34 | **Heavy Paper** | Mina bringt Duc die Einladung zur Villa. Dicker Umschlag, Goldrand. Sie gibt ihn ihm wie eine Rechnung | nur Ansage der Villa, kein Vorteil |
| 35 | **The Delivery Book** | Bei der Kommission: Wenn Duc in der Runde mitgefahren ist, legt Mina ihr Zustellbuch auf den Tisch. Jedes Einschreiben von A.V. Estates in der Woche vor der Anhörung trägt eine Unterschrift und ein Datum | Beweis für die Säule Gemeinschaft; ohne Runde kein Buch |
| Festa | **Every Name** | Die Einladungen zur Festa stellt Mina zu. Im Schlussbild sitzt jeder, der zugesagt hat; Mina hat den Stapel der Absagen in der Tasche, kleiner oder größer | Festa-Füllstand = Zusagen, sichtbar als Gäste |
| Epilog | unverändert | Brüssel („I read this one.“) und das Einschreiben ohne Empfänger („Sign here.“) wie in `enden.md` | |

### Beat-Plan der zwei wichtigsten Szenen

**Forty-One Envelopes (Tag 30, Morgen, `village_piazza`, ton ernst)**

| Ansage | Inhalt | Handlung | Reaktion | Übergang |
|---|---|---|---|---|
| Titelkarte „Forty-One Envelopes“, Continue, Skip | Mina auf der Kirchentreppe, der Sack offen, alle Umschläge gleich, weiß mit grauem Logo | Mina stellt die Frage: “I have to deliver all of these by Friday. Are you coming with me, or do I do this alone?” Chips: “I'm coming. I'll take the back seat.” / “Do your job. I'll find them later.” | Mit Duc: Mina startet die Vespa, Elsa sieht vom Rathaus zu und zerreißt einen Strafzettel. Allein: Mina nickt und fährt los, zu schnell | Karte „The Round“ mit der Liste der Türen |

Zeilen (Entwurf):
- Mina (sadness): “Forty-one letters, Yacht. [sigh] They all came in the same box, and they all have the same envelope.”
- Mina (anger): “I don't read them. I just know. Jobs for the ones who say nothing, and lawyers for the ones who talk.”
- Elsa (neutral), nur mit Duc: “Mina. I didn't see you on that pavement. [clear throat] I didn't see either of you.”

**Return Address (Tag 33, Abend, Ort nach Wahl: Hafenmauer)**

| Ansage | Inhalt | Handlung | Reaktion | Übergang |
|---|---|---|---|---|
| Titelkarte „Return Address“, Continue, Skip | Mina auf der Hafenmauer, der Brief auf den Knien, der Umschlag weich vom Jahr in der Tasche | Erinnerung im Satz: “The letter from my brother, the one I showed you on the way up to the monastery, is still closed.” Frage: “Will you sit with me while I open it?” Die Begleitung wählt der Spieler vorher (Duc, Elsa, Isabelle) | Sie liest laut. Die Begleitung reagiert in ihrer eigenen Stimme (Elsa auf den Satz für sie, Isabelle auf das Wort Mut) | Mina entscheidet selbst; der Spieler kann zuhören oder einen Satz sagen, aber nicht entscheiden |

Zeilen (Entwurf):
- Mina (nervousness): “It's from Montréal. [sniff] He writes like he talks, too fast and with no full stops.”
- Mina (surprise): “He's getting married. In October. [laugh] He wants me to stand next to him, because I'm the only one who never told him to come home.”
- Mina (amusement): “There's a line at the bottom for you, Elsa. It says he's sorry about your car.”
- Elsa (neutral): “It was my father's car. [sigh] Tell him I'm still not over it.”
- Mina (optimism), bleibt: “I'll fly in October and I'll fly back. Somebody has to bring the post here, and you're all terrible at it.”
- Mina (optimism), fliegt: “I think I'll stay a while there, Yacht. [sniff] Elsa can give the tickets to somebody slower.”

## 6. Die Runde: eine kleine Mechanik ohne Verwaltung

**Kernschleife (eine Phase):** Mina zeigt drei Türen aus dem Sack (Namen mit Bild und einem Satz Klatsch). Duc wählt eine.
An der Tür kommt der Brief an. Mina sagt in einem Satz, was er droht (Job, Kredit, Anwalt). Duc wählt eines von drei Argumenten,
das zu der Person passt. Passt es, sagt die Person aus (Name im Fischernetz, `enden.md`).

| Regel | Zahl | Wirkpunkt (Vorschlag) |
|---|---|---|
| Türen pro Phase | 1, mit Vertrauen `mina` ab 6 und `mina_vespa_heil` 2 | neue Funktion in `kern/aufbau.py` oder eigenes `kern/runde.py`, gelesen aus `regeln.vertrauen` |
| Wie viele Briefe | 41 im Sack, davon 8 bis 10 benannte Zeugen | Daten in `module/eden_rise/` per Builder |
| Hilfe durch Vertrauen | Mina verrät ab Vertrauen 4, welches Argument die Person trägt („She's scared for her son's job, not for herself.“) | Hinweiszeile statt Zufall |
| Dorf-Vertrauen | Hat Duc der Person vorher geholfen (z. B. Pascal, Sandru, Minicu, Bà Tư), reicht ein schwächeres Argument | erste Stelle, an der das Dorf-Vertrauen wirkt (Lücke 3 im Wirkpunkt-Audit) |
| Schaden | Ein falsches Argument kostet nichts außer der Tür; die Person kann an einem späteren Tag wieder kommen | keine Falle für Spieler, die es gut meinen |
| Langes Ziel | Zustellbuch bei der Kommission ab 3 begleiteten Runden | Flag `mina_zustellbuch` |

## 7. Drei Outfits neben dem Standard

Standard (Kanon, E-099): pinke Regenjacke, enge beige Hot Pants, oversized Bluse, pinker Helm. Alle drei neuen Looks behalten den
pinken Helm oder zeigen ihn bewusst, damit man Mina auf einen Blick erkennt. Sonnengebräunt, 24, korsische Französin. Für jeden
Look gilt der Krea-Leitfaden: positiv formulieren, „She is the only person in the picture“, müde als „tired eyes“, nie Dreck.

| # | Name (Set-ID) | Wann im Spiel | Look | Warum |
|---|---|---|---|---|
| 1 | **Summer Round** (`mina_sommer`) | Woche 4, heiße Tage, Parcels und The Long Way Up | zitronengelbes ärmelloses Top mit kleinem Kragen, kurze Jeansshorts, weiße Sneaker, der pinke Helm am Ellbogen, die Posttasche quer mit dem neuen Lederriemen | Der Riemen ist der Lohn aus dem Schneider-Auftrag „A Strap That Holds“: Wer ihn gemacht hat, sieht ihn an ihr. Ohne den Auftrag trägt sie den alten, ausgefransten Gurt (zwei Varianten, ein Detail) |
| 2 | **Dumè's Shirt** (`mina_arbeit`) | Wiederaufbau in Woche 4, The Round in Woche 5 | ein viel zu großes, verwaschenes blaues Männerhemd, Ärmel hochgekrempelt, an der Taille geknotet, darunter ein weißes Top, beige Cargo-Shorts, Arbeitshandschuhe im Gürtel, pinkes Bandana im Haar | Das Hemd ist von ihrem Bruder. Niemand sagt es, bis Elsa es in Return Address erkennt: “That's his shirt.” Text und Bild tragen dieselbe Geschichte |
| 3 | **Festa** (`mina_festa`) | Schlussszene, Einladungen, Epilog | weißes Leinenkleid knielang mit kleiner pinker Stickerei am Saum, offene Haare mit einer Hibiskusblüte, flache braune Ledersandalen, ohne Helm; die Posttasche hängt trotzdem über der Schulter, voller Absagen | Zum ersten Mal ohne Helm. Die Tasche bleibt, weil sie auch an diesem Abend zustellt |

Ersatz-Vorschlag, falls Duc einen Abreise-Look für das Ende `mina_fliegt` lieber will als Summer Round: **Departure**
(`mina_abreise`): Jeansjacke über der oversized Bluse, Rucksack, Bordkarte in der Brusttasche, der pinke Helm hängt an Elsas
Spiegel im Hintergrund. Nur in einem Ende sichtbar, darum Platz 4.

Prompt-Bausteine für das Casting (Englisch, positiv):
- Summer Round: “a tanned Corsican woman, 24, lemon yellow sleeveless top with a small collar, short denim shorts, white sneakers, a pink scooter helmet hanging from her elbow, a postal bag across her body on a new brown leather strap, standing relaxed, she is the only person in the picture”
- Dumè's Shirt: “a tanned Corsican woman, 24, an oversized faded blue men's shirt with rolled sleeves knotted at the waist over a white top, beige cargo shorts, work gloves tucked in her belt, a pink bandana in her hair, clean skin, she is the only person in the picture”
- Festa: “a tanned Corsican woman, 24, a white knee-length linen dress with small pink embroidery at the hem, loose dark hair with a red hibiscus flower, flat brown leather sandals, a postal bag over one shoulder, warm evening light, she is the only person in the picture”

Gefühle je Set: das volle Satz-Raster wie bei den anderen Dorf-Figuren; Pflicht ist eine ruhige, frontale neutral-Variante
(STIL 6). Das Festa-Set braucht `sadness` und `joy` für die beiden Fassungen von Return Address und die Festa.

## 8. Verbesserungsrunde

**Maelle (Producerin):** Die Runde ist der teure Teil. Ich schneide sie auf 8 benannte Türen und eine Szene je Tür mit drei
Argumenten; die übrigen 33 Briefe sind nur eine Zahl auf dem Sack. 📋

**Sora (Spielerstimme / QA):** Minute 1: Ich sitze hinten auf der Vespa und will das sofort wieder. Minute 5: Drei Türen, Mina
flüstert mir, wer Angst um den Job des Sohnes hat, ich wähle richtig, und die Frau sagt „I'll come on Friday.“ Das ist *Persona 5*,
nur mit Briefen. Minute 20: Bei der Kommission knallt das Zustellbuch auf den Tisch und ich schreie. Nochmal-Lust 4 von 5. Und
ja, die Rücksitz-Fahrt darf ein bisschen knistern, ohne Romanze: Arme um ihre Taille, sie fährt absichtlich über jedes Schlagloch. 😏

**Aly (Tech):** Die Runde baue ich auf `kern/aufbau.py` auf, sobald Aufbau angeschlossen ist, nicht daneben. Ein Test
`tests/test_runde.py` prüft: Vertrauen 6 gibt zwei Türen, ein falsches Argument sperrt nichts, drei Runden setzen
`mina_zustellbuch`. 🤓

**Luise (Art & Story):** Im Fliegen-Ende sieht man im Epilog trotzdem eine Vespa-Fahrerin mit pinkem Helm, die Brüssel bringt:
Rosi, auf Minas Vespa. 🥹 Dann kommt „I read this one.“ von Rosi, mit Ernst und Öl am Handgelenk. Kanon bleibt, das Bild wird größer.

## 9. Gegenrede

**Sienna (Game Direction):** Ich widerspreche der Kommissionsszene. Das Wiki sagt klar: Mina ist kein Mechanik-Erklärer und
keine Heldin. Wenn ihr Zustellbuch der Beweis ist, der die Kommission kippt, stiehlt sie Buenaventura und Riscossores Buch die
Bühne. Gegenvorschlag: Das Zustellbuch belegt nur, dass die Briefe kamen, nicht, was in der Nacht geschah. Es schützt die Zeugen
(sie werden nicht als unglaubwürdig abgetan, weil sie bedroht wurden) und zählt auf die Säule Gemeinschaft, aber Riscossores Buch
bleibt der Schlag. ✨

**Luise (Art & Story):** Ich stimme der Hochzeit zu, aber das größte Risiko ist der Satz für Elsa: Er darf nicht wie ein neuer
Romanzenfaden für Elsa wirken. Darum geht es um ein Auto, nicht um Gefühle.

## 10. Vorschlagstabelle

Bewertung nach `EVENT_RANKING.md` (Bindung 30 %, Spielwirkung 25 %, Humor 20 %, Frische 15 %, Sehnsucht 10 %), Punkte 1 bis 5.

| # | Vorschlag | Von | Bindung | Wirkung | Humor | Frische | Sehnsucht | Wert |
|---|---|---|---|---|---|---|---|---|
| 1 | The Round: Duc auf dem Rücksitz bei Alons Briefen, Argument wählen statt würfeln | Sienna, Aly | 5 | 5 | 3 | 5 | 5 | 4,6 |
| 2 | Return Address: Dumè heiratet, Mina wählt selbst, Begleitung wählt der Spieler | Luise | 5 | 3 | 4 | 4 | 5 | 4,2 |
| 3 | Second Gear: Rosi repariert Minas Vespa (Papa Salvo) | Luise, Aly | 5 | 3 | 4 | 4 | 4 | 4,1 |
| 4 | Every Name: Festa-Gäste = Minas zugestellte Zusagen | Sienna | 4 | 5 | 2 | 4 | 4 | 3,9 |
| 5 | The Delivery Book als Zeugenschutz (nach Gegenrede) | Sienna, Sora | 4 | 4 | 3 | 4 | 4 | 3,8 |
| 6 | Drei Outfits: Summer Round, Dumè's Shirt, Festa | Luise | 4 | 2 | 3 | 4 | 3 | 3,3 |
| 7 | Rosi stellt im Fliegen-Ende zu | Luise | 4 | 1 | 3 | 5 | 4 | 3,2 |

## 11. Preis (Maelle)

- Szenen: 7 neue (Second Gear, The Long Way Up, Forty-One Envelopes, Return Address mit 3 Begleitungen, Heavy Paper, Delivery Book,
  Every Name) und 8 Türen der Runde. Etwa 90 neue Sprechzeilen, davon rund 40 für Mina, Rest Dorf und Elsa.
- Sitzungen: 1 für das Drehbuch mit Beat-Tabellen, 1 bis 2 für den Bau der Runde mit Test, 1 für Szenen und Stimmen-Tags.
- Bilder: 3 Sprite-Sets (Outfits oben). Hintergrund Hafenmauer bei Abend fehlt vielleicht; bis dahin `village_harbour`.
- Liegen bleibt dafür: Die freien Dorf-Paare aus Woche 3 (Mina und Sandru, Mina und Alva) kommen höchstens als Legenden-Zeilen.

## 12. Selbstkontrolle

**Sora (Spielerstimme / QA):** Ja, das hat geholfen: Woche 5 hat jetzt eine Schleife, auf die ich mich freue, und Mina bleibt frech
statt Erklär-Bärchen. 😂

**Maelle (Producerin):** Ja, mit einem Haken: Die Runde hängt am Anschluss von `kern/aufbau.py`. Ohne den bauen wir sie doppelt.

**Maelle (Producerin), die eine Frage an Duc:** Soll Mina mit der Runde (⭐ B) die Verbindung von Woche 5 werden, oder bleibt sie bei
ihrem eigenen Brief (A) und die Zeugen überzeugt Duc ohne sie? 📋
