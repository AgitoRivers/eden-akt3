# Kochen und Küche

Stand 27.10.2026 · Besitz: Interaction Mechanic · Beschluss Duc 27.10. (Register-Eintrag E-079, Pflege durch die Hauptsitzung). Dieses Seite beschreibt, was **gilt**; die Planung vom 20./21.10. in [tage_erkundung.md](tage_erkundung.md) (3.276 Kombinationen, Brauner Schleim, Kühlschrank als Lager) ist dadurch teils überholt.

## Beschluss (27.10.2026)

- **Moral:** Eigener Verzehr gibt nie Crew-Moral, Teilen entfällt. Moral kommt aus dem Essen nur noch durchs Kochen für die Crew (+1, einmal am Tag, Zähler `essen_heute` in `kern/handel.py`). Die Moral-Session hat Brownie und Notizen entsprechend bereinigt.
- **Baukasten (gebaut 27.10.2026):** 1 Haupt + 1 Akzent + 1 Basis. Haupt bestimmt, wer es mag; Akzent bestimmt den Bonus am nächsten Tag (6 Effekte, je ein Wirkpunkt); Basis bestimmt Sättigung und Heilung. Die 14 Lieblingsgerichte bleiben fest. Qualität ★ / ★★ / ★★★ nach Herkunft der Zutat (gekauft, gepflückt, selbst angebaut).
- **Farmen (gebaut 27.10.2026):** Nonnas Garten ohne Phasenkosten (Menü wie Rosis Werkstatt, 1 Tag Wachstum) und drei Ställe als Upgrades: Chicken, Pig, Cow (Duc 27.10.: „Chicken, Pork, Beef“ als Tiere, Details unten).
- **Angeln (Minispiel geparkt, Daten und Bilder gebaut):** 20 Fische, 10 Meer (am Boot), 10 Fluss (an Rastplätzen mit Fluss), kein Date. Das Minispiel selbst kommt später; `kuechen.fang()` ist der Einhängepunkt.
- **Zeitgrenze:** nur 2 freie Phasen pro Tag (Mittag, Nachmittag), 42 über 21 Tage. Alles, was eine Phase kostet, konkurriert mit Dating.

## Heute im Spiel (gebaut)

14 Gerichte, jedes das Lieblingsgericht genau einer Person. Aktion „Kochen“ in Lolas Kombüse, einmal pro Tag, ersetzt das Essen des Tages. Wahrnehmungs-Probe gegen SG 9–13 mit dem Vorteil „Küche“. Teller für eine Person (Vertrauen und Begehren je nach Stufe: Ekel −6/−6 … „liebt“ +6/+4, das volle „liebt“ nur einmal je Person) oder Crew-Essen (+2 für alle, Moral +1, wer es hasst, isst Brot). Details der Stufen: [beziehungen.md](beziehungen.md).

## Der Küchenkreis (gebaut 27.10.2026, Duc: „baue die gesamte Kochmechanik“)

Alles ist datengetrieben: `werkzeuge/eden_rise/kochen_daten.py` → Builder `kochen_eden_rise.py` → `module/eden_rise/kuechen.json`. Die **Zutatenliste ist ein Platzhalter**, Duc liefert die endgültige später; jede Zutat mit Rolle Basis, Haupt oder Akzent funktioniert sofort.

### Vorrat und Qualität
`z["kueche"]["vorrat"]` zählt je Zutat und Qualität: ★ gekauft, ★★ gefangen oder gepflückt, ★★★ selbst angebaut oder gezüchtet. Die Qualität wirkt als Faktor ×1 / ×1,5 / ×2 auf den Akzent-Bonus und die Heilung der Basis. Ein Spielstand ohne Küche bekommt keinen Schlüssel (nur lesen).

### Baukasten (Lolas Kombüse, „Cook from your pantry“)
1 Basis + 1 Haupt + 1 Akzent aus dem Vorrat, drei verschiedene. Das Spiel zeigt vor dem Kochen Name, SG, Heilung, Bonus und wer es mag (`GET /api/kuechen_vorschau`).

| Rolle | Entscheidet | Wirkung |
|---|---|---|
| **Haupt** | wer es mag | Kategorie (fish, shellfish, poultry, pork, beef, egg, veg, mushroom) gegen den Geschmack der Person (2 mag, 1 mag nicht, 14 Personen, `GESCHMACK`): mag = „gut“, neutral = „normal“, mag nicht = „lustlos“ (kein Ekel). Kritisch +1, Fehlschlag −1. |
| **Akzent** | Tagesbonus | 7 Effekte (siehe unten), je ein Wirkpunkt im Code |
| **Basis** | Sättigung | Duc heilt Life (Reis 4, Nudeln 3, Mehl 3, Kartoffeln 5, Kohl 2) und gibt den Grund-SG (8–10) |

- Kochen läuft über `handel.kochen`: Wahrnehmungs-Probe mit Küchen-Vorteil, **ein Essen am Tag** (derselbe Zähler wie bei Snacks und Lieblingsgerichten), Crew-Moral +1 nur für das Crew-Essen (E-079). Ein misslungener Versuch („heute schon gegessen“) verbraucht nichts.
- Teller für eine Person oder Crew: bei der Crew bekommt jeder +2 (wer das Haupt mag +1, wer es nicht mag 0), wie das Crew-Essen der Lieblingsgerichte.
- Die 14 Lieblingsgerichte bleiben fest und kochbar wie bisher (Tischszene unten).
- Namen: „<Haupt> with <Akzent> on <Basis>“ (kein LLM-Name, kostet nichts).

**Akzent-Effekte** (Wert bei ★, ×1,5 bei ★★, ×2 bei ★★★, ganzzahlig gerundet; **ein Bonus gleichzeitig, bis zum Dinner des Folgetags einschließlich**):

| Effekt | Zutaten (Platzhalter) | Wirkpunkt |
|---|---|---|
| Krit +5 % | Chillies | `kampf.py` Chips-Summe (`agg["krit"]`) |
| Erfahrung +10 % | Wild Herbs, Lemongrass | `kampf.award_xp` |
| Vertrauen +1 bei allen am Tisch | Tomaten, Milch | sofort beim Kochen, kein Tagesbonus |
| Ladenpreise −10 % | Zitronen | `handel.preis` |
| Mut +1 im Kampf | Knoblauch | `kampf.attributes` |
| Verkaufspreise +10 % | Sojasauce | `handel.ankauf` (Totò) |
| Niemand lehnt das Gericht ab (Fischsauce, 31.10.) | Fish Sauce | `kuechen.vorschau` leert „mag nicht“; wirkt sofort auf diesen Teller, kein Tagesbonus, Sterne ändern nichts |

**Bà Tưs Laden (31.10.):** verkauft Zutaten direkt in den Vorrat, gekauft = ★ (Item-Feld `zutat`, `handel.kaufen`): Fish Sauce 12 €, Tofu 8 € (Haupt, zählt als Gemüse), Rice Paper 5 € (Basis, SG 9, heilt 3), Rice 3 € und Soy Sauce 5 €, je einen Euro unter Nonna. Dazu Green Tea 9 €. Offen ab ihrer ersten Szene (Tag 9).

- **Bowl from the Pot (8 €, Duc 31.10.):** Energie +1, keine Moral, zählt als Essen des Tages, einmal am Tag (Item-Feld `essen`, `tageslimit`). Kein Heilen, kein Tagesbonus.
- **Lemongrass Cuttings (25 €, einmalig):** schalten die Pflanze Lemongrass in Nonnas Garten frei (Flag `zitronengras_da`, Eintrag `PFLANZEN_FREI`). Flavour wie Wild Herbs: Erfahrung +10 %, aus dem Garten ★★★ also +20 %. Am Tag nach dem ersten Pflanzen kommt Nonna in Bà Tưs Laden (`g1_zg_zitronengras`, „Foreign Grass“): erst Geschimpfe, dann gegenseitiger Respekt. Vertrauen bei beiden.

### Nonnas Farm (Laden „Nonna's Farm“, ab Tag 4)
Im Orte-Menü neben Totò, Rosi und Lola. Vier Reiter: **Garden**, **Animals**, **Shop**, **Pantry**. Nonna begrüßt (3 vertonte Zeilen), Hintergrund Klostergarten.

- **Shop:** Grundzutaten dauerhaft (Reis, Nudeln, Mehl, Zitronen, Sojasauce), tierische Zutaten als **kleiner, teurerer Tagesvorrat** (Eier 3, Milch 2, Huhn 2, Schwein 1, Rind 1, Lachs 1; füllt sich jeden Tag neu). Eigene Tiere zu halten lohnt sich deutlich mehr. Das Geld geht sofort weg; die Ware kommt erst beim **Verlassen des Ladens („Goodbye“)**: **Frederico** bringt sie rüber mit einem von 8 neckischen, manchmal süßen Sätzen (vertont, Turbo-Tags, kein Flirt, er ist das einzige Kind im Spiel).
- **Garden:** 4 Beete, pflanzen kostet Saatgeld (2 €) und **keine Phase**; Ernte am nächsten Morgen im Vorrat, ★★★. Sieben Pflanzen (Kartoffeln, Kohl, Chillies, Wild Herbs, Tomaten, Knoblauch, Zucchini).
- **Animals:** drei Ställe als einmaliges Upgrade (Chicken 120 €, Pig 200 €, Cow 320 €); Tiere kauft man als Baby (25 / 60 / 110 €). Italienische Rassen: Livorno-Huhn, Cinta Senese, **Pisana** (seltene, fast schwarze Toskana-Kuh aus der Gegend um Pisa; Duc 28.10. statt der weißen Chianina, die alten Sprites liegen in `farm/_kandidaten/cow_weiss_*.png`).

| Art | Plätze | Baby | erwachsen (liefert) | Zucht | alt (Stufe 3) |
|---|---|---|---|---|---|
| Chicken | 6 | 2 Tage | 5 Tage: Eier, nur Weibchen, täglich | Paar → Baby alle 3 Tage | schlachten: 2 Chicken |
| Pig | 4 | 3 Tage | 6 Tage: Trüffel, jedes Tier, alle 2 Tage | alle 5 Tage | schlachten: 3 Pork |
| Cow | 3 | 4 Tage | 7 Tage: Milch, nur Weibchen, täglich | alle 7 Tage | schlachten: 4 Beef |

Stufen nach Alter in Tagen: 1 Baby, 2 erwachsen (Männchen oder Weibchen, andere Sprites), 3 alt. Erste Produkte am Tag nach der Reife; alte Tiere liefern nichts mehr, nur Fleisch (★★★). Ein erwachsenes Paar bekommt nach der Zuchtzeit ein Baby, solange im Stall Platz ist. **Neue Tiere kann man benennen** (1–16 Buchstaben, sonst Vorschlagsname). Die Ställe zeigen die Tiere als **Einzelbilder, die hüpfen (Baby), trippeln (erwachsen) oder schlurfen (alt)**; ein Klick spielt den Laut (`tier_cluck`, `tier_grunt`, `tier_moo`, je `_baby`; ElevenLabs, 4 Varianten). Fehlt ein Bild, steht ein Emoji da.

### Baustoffe und Stall-Stufen
Ställe brauchen neben Geld **Baustoffe** (Duc 30.10.2026: Stein geteilt in Schiefer und Granit, neu Stahl). Nonna verkauft **Timber** (8 €), **Slate** (6 €) und **Iron** (25 €) unter „Building materials“ (Tagesvorrat 6 / 6 / 2), Frederico bringt sie mit der übrigen Ware. **Granite** und **Cork** gibt es nur selbst abgebaut: Granitfels gibt Granit, Schieferfels Schiefer, Korkeiche Kork (siehe „Quellen an Rastplätzen“). **Steel** kommt nur von **Maschinen-Gegnern** (Duc 30.10.2026): ab Tag 22 (Akt 3) je besiegter Gegner der Klasse `maschine` 1 Stück (`kochen_daten.STAHL_KAMPF`), kein Ladenartikel. **Offen:** Die Maschinen für Akt 3 sind noch nicht entworfen. Bis dahin ist Stufe 3 im Spiel nicht erreichbar, Unit-01 in Akt 2 gibt noch keinen Stahl. Beim Angeln fischt man manchmal Strandgut heraus (siehe unten). Bauen ist „alles oder nichts“: Fehlt ein Teil, passiert nichts. Die Stallkarte zeigt jede Kostenposition grün (hast du) oder rot (fehlt). Alter Stein im Spielstand wird zu Schiefer (`zustand.angleichen`).

| Art | Stufe 1 (bauen) | Stufe 2 | Stufe 3 |
|---|---|---|---|
| Chicken | 120 € + 4 Timber, 2 Slate | 150 € + 6 Timber, 2 Cork, 2 Slate, 2 Granite → **9 Plätze** | 220 € + 6 Timber, 4 Granite, 2 Iron, 2 Steel → **+1 Ei je Huhn, Zucht 1 Tag schneller** |
| Pig | 200 € + 6 Timber, 2 Slate | 220 € + 6 Timber, 3 Cork, 4 Slate, 2 Granite → **6 Plätze** | 300 € + 8 Timber, 6 Granite, 2 Iron, 3 Steel → **+1 Trüffel, Zucht −1** |
| Cow | 320 € + 8 Timber, 4 Slate | 300 € + 8 Timber, 4 Cork, 6 Slate, 4 Granite → **5 Plätze** | 400 € + 10 Timber, 8 Granite, 3 Iron, 4 Steel → **+1 Milch, Zucht −1** |

Code: `farm.stall_kaufen` (Stufe 1), `farm.stall_ausbauen` (2 und 3), Kosten in `kochen_daten.STALL_STUFEN`.

### Angeln (gebaut 27.10.2026 nachts)
**Orte (seit 28.10.2026, Duc: „Angeln nur wo es auch Wasser gibt“):** das Boot („Fishing off the Swim Platform“, Meer) in der freien Wahl, sonst nur an **Rastplätzen mit Wasser** auf Expeditionen (siehe „Quellen an Rastplätzen“). **Hintergründe wechseln** (Duc 28.10.2026: „alle 20 nutzen, wechselnd je Kategorie“, alle abgenommen): Jeder Angelgang zieht zufällig ein Bild aus seiner Gruppe, Wasser immer links. Seit 29.10. (Duc: „10 umsetzen“) ist Meer geteilt: **das Boot** zieht nur die 5 Yacht-Bilder (`meer_01` Badeplattform, `02` Achterdeck, `05` Bug, `06` Badeplattform bei Nacht, `09` Beiboot), **Rastplätze am Meer** nur die 5 Küstenbilder (`meer_03` Granitbucht, `04` Hafenmole, `07` Strandsteg, `08` Felsküste, `10` Leuchtturm), **Fluss-Plätze** weiter `fluss_01–10`. Am selben Platz kommt nie zweimal hintereinander dasselbe Bild; innerhalb eines Gangs bleibt es fest, auch nach Neuladen. Liste in `kochen_daten.ANGEL_BILDER`, Wahl in `kern/angeln.py` (`_bild_waehlen`, merkt sich `kueche.angel_bild_letzt`), Dateien kopiert `werkzeuge\angeln_bilder.py uebernehmen`. Das feste `angel_bild` je Platz zeigt nur noch die Boot-Karte in der freien Wahl.

**Angel-Kreis (seit 29.10.2026, Duc: „Angeln sollte eher als Kreis oben rechts, links neben Kabine dargestellt werden“):**
In der freien Wahl ist Angeln keine Wahlkarte mehr, sondern ein runder Knopf **„Fishing“ (Taste F)** links neben „Cabin“,
im selben Stil, mit dem Bild des Angelplatzes. Ein Abzeichen zeigt die restlichen Würfe. Beißt nirgends etwas, wird der
Kreis grau und zeigt „back in N days“. Bei einem Platz startet der Klick sofort, bei mehreren öffnet er eine kleine
Liste der Plätze. Code: `kreis()`/`kreisKlick()` in `client/plugins/eden-angeln/eden-angeln.js` (die alte `karten()` bleibt
ungenutzt stehen), Kopfzeile in `client/index.html` (Klasse `mit-angel`, Taste `f`), Stil `.eakreis` in der Plugin-CSS.
Prüfung im Browser (Tag 10: Kreis mit 4 Würfen, F startet, Esc zurück zur Wahl), `tests/test_angeln.py` grün.

**Ablauf einer Sitzung:** Angeln **kostet keine Zeit**. Jeder Platz hat 4 Würfe Bestand; jeder Wurf zieht einen ab. Ist er leer, beißt dort 3 Tage nichts. Einpacken geht jederzeit (Esc), der Rest bleibt im Wasser. Am Rastplatz geht es danach zurück ans Feuer, am Boot zurück zur Wahl.
1. **Werfen** (Leertaste oder Klick): Schwimmer fliegt aufs Wasser, Kreise, Schatten eines Fisches.
2. **Warten** 1,4–3,6 s, dann **Biss**: Der Schwimmer taucht unter, und man hat 0,95 s zum Anschlagen (Wahrnehmung +0,1 s je Punkt über 2). Zu früh: „Too early“, der Fisch ist weg. Zu spät: „Too slow – it spat the hook“.
3. **Drill** (Duc: „wie Paraden“): Ein Punkt hüpft in einem senkrechten Balken auf und ab, eine helle Zone liegt im Balken. Leertaste drücken, wenn der Punkt in der Zone ist. Jeder Treffer versetzt die Zone und macht den Punkt 8 % schneller. Die Zone **schrumpft ständig**, und jeder Fehlklick kostet zusätzlich Breite. Ist sie weg, **reißt die Leine**.
4. **Ergebnis-Karte:** Fang mit Bild, Sternen, „New in your journal“, Vorrat. Ohne Fehlklick und ohne Entspannten Modus ★★★, sonst ★★.

| Stufe | Treffer | Tempo | Zonenbreite | Schwund/s | Fische |
|---|---|---|---|---|---|
| 0 (Strandgut) | 2 | 0,65 | 0,40 | 0,022 | – |
| 1 (60 %) | 3 | 0,85 | 0,34 | 0,028 | Meer: Sardine, Bream, Mullet, Sea Bass · Fluss: Trout, Perch, Carp, Tench |
| 2 (30 %) | 3 | 1,10 | 0,29 | 0,030 | Meer: Scorpionfish, Cuttlefish, Octopus, Atlantic Salmon · Fluss: Barbel, Crayfish, Crab, Pike |
| 3 (10 %) | 4 | 1,30 | 0,27 | 0,030 | Meer: Red Prawn, Spiny Lobster · Fluss: Eel, Zander |

Fehlklick −0,06 Zone; Wahrnehmung über 2 gibt +0,015 Zone je Punkt.

**Die Möwe (gebaut 29.10.2026, Duc: „Möwe, die beim Angeln dir Fische klauen kann. Wenn du sie besiegst, kriegst du den
Fisch zurück“):** Am **Meer** (Boot und Rastplätze am Meer, nicht am Fluss) schnappt mit **15 %** eine Möwe den gerade
gelandeten Fisch, **höchstens einmal je Angelgang**. Sofort folgt ein kurzer Kampf „A Gull Steals Your Catch“ gegen die
Möwe aus dem Frühstückskampf (Gegner `moewe`, Sprite `Seagull`, Level Duc −1, lästig), vor dem Bild des Angelgangs.
**Sieg oder Aufgabe:** der Fisch kommt zurück (Tasche bzw. Vorrat, gleiche Sterne; ohne Platz in der Tasche schwimmt er
davon). **Niederlage, Flucht oder sie entkommt:** der Fisch ist weg. Im Journal zählt er trotzdem. Danach geht der
Angelgang weiter; die Ergebniskarte zeigt „🪶 Won back from a gull“ bzw. „The gull got away with it“, der Wurf-Pip eine
Feder. Code: `angeln.MOEWE_CHANCE`, `moewe_offen`, `moewe_nach_kampf` (`kern/angeln.py`), Start in `eden.py`
(`angeln_ergebnis`), Begegnung `angel_moewe` in `kaempfe_eden_rise.py`; Test `tests/test_moewe.py`.

**Balance** (`python werkzeuge\angeln_sim.py`, 4000 Drills je Feld, Spieler mit Zeitabweichung):

| Spieler | Stufe 1 | Stufe 2 | Stufe 3 | entspannt St. 1/2/3 |
|---|---|---|---|---|
| gut (40 ms) | 100 % | 98 % | 85 % | – |
| mittel (75 ms) | 97 % | 77 % | 37 % | 99 / 96 / 72 % |
| schwach (120 ms) | 80 % | 44 % | 14 % | 95 / 74 / 36 % |

**Relaxed reel** (Häkchen oben, bleibt im Browser gespeichert): Tempo und Schwund ×0,7, dafür höchstens ★★.

**Strandgut** (15 % je Wurf, Stufe 0): Meer Driftwood (+1 Timber) oder Rusty Chain (+1 Iron), Fluss River Slate (+2 Stone) oder Old Branch (+1 Timber).

**Journal** (Taste J): 20 Felder, Unbekanntes als Silhouette, Fortschritt je Gewässer. Wer alle 10 eines Gewässers gefangen hat, bekommt einen Sammelbonus: **Lea's Lucky Lure** (Meer) bzw. **Petru's Cork Float** (Fluss), je Zone +0,03 dort. Packen mit Esc (nur wenn ein Fisch am Haken hängt, fragt das Spiel nach).

Töne: `angeln_wurf`, `angeln_biss`, `angeln_treffer`, `angeln_fehl`, `angeln_fang`, `angeln_riss` (ElevenLabs, mehrere Varianten).

### Quellen an Rastplätzen und Abbauen (gebaut 28.10.2026)
Duc 28.10.: „Angeln und Holz sowie Stein abbauen können wir an Rastplätzen … bis die Quelle erschöpft ist für den Tag … danach erschöpft für 3 Tage.“

**Wo (Kreise seit 30.10.2026, Duc: „wenn der Rohstoff vorhanden ist, dann ist er zu sehen, und wenn nicht mehr verfügbar, ist der Kreis zwar noch da, aber ausgegraut“):** An einem Rastplatz stehen links neben Ducs Tafel runde Knöpfe wie der Angel-Kreis: *Fell trees* (Taste C), *Break rocks* (M), *Fish* (F). Das Abzeichen zeigt den Bestand, das Bild, was am Platz am meisten steht (Korkeiche, Steineiche, Granit, Schiefer; `farm/abbau/kreis_*.png`) bzw. das Angelbild. Es erscheinen nur Quellen, die der Platz hat. Ist eine leer oder fehlt etwas, bleibt der Kreis grau stehen: „back in 2 days“, „needs an axe · Petru“ oder „bag full“. Code: `EdenAbbau.quellenHtml`, Baustein `EdenAngeln.kreisKnopf`. Mehrere Frames desselben Ortes teilen eine Quelle (Schlucht mit und ohne Feuer, Bergsee und Hütte am See).

| Platz | Frames | Holz (Korkeiche / Steineiche) | Stein (Granit / Schiefer) | Wasser |
|---|---|---|---|---|
| Swim Platform (Boot) | – (freie Wahl) | | | Meer |
| Under the Holm Oak | `kl_bachufer` | 60 / 40 | | Fluss |
| The Shepherd's Hut | `kl_huette` | 50 / 50 | | |
| The Brothers' Camp | `kl_lager` | 40 / 60 | | |
| Fire on the Ledge | `kl_schluchtfeuer`, `kl_schluchtfeuer_kalt` | | 60 / 40 | |
| The Charcoal Burners' Clearing | `bg_koehler` | 30 / 70 | | |
| The Mountain Lake | `bg_see`, `bg_see_rast` | | 70 / 30 | Fluss/See |
| The Foggy Ridge | `bg_kamm_funk` | | 40 / 60 | |
| Ghjuvan's Summer Hut | `bg_u1_huette` | 40 / 60 | | |
| An Empty Hut | `bg_u2_huette_leer` | 30 / 70 | | |
| The Drowned Beach | `gr_strand` | | 50 / 50 | Meer |
| The Air Pocket | `gr_u1_luft` | | 40 / 60 | |
| The Treasure Hunters' Camp | `gr_u2_lager` | | 60 / 40 | |
| The Quiet Pool | `fn_teich_leer` | | | Meer |

Keine Quelle: Nonnas Küche, die Bergerie und Gennaros Zelle (drinnen bzw. passt nicht).

**Bestand:** je Quelle 4 Bäume, 4 Felsen bzw. 4 Würfe. Kein Zeitpreis: man baut ab, bis sie leer ist. Leer = **3 Tage erschöpft**, dann wieder voll. Angefangene Quellen behalten ihren Rest.

**In die Tasche (Stapeln, 28.10.2026):** Der Ertrag landet nicht im Zähler, sondern in der Tasche (Timber/Slate/Granite/Cork 10 je Platz, Fisch 3 je Art) und wird erst bei der Heimkehr ausgepackt. Ist die Tasche voll, zeigt der Chip „🎒 bag full“; was beim letzten Baum nicht mehr passt, bleibt liegen („Left behind, the bag was full“), ein Fisch ohne Platz schwimmt davon. Bei einer Niederlage zählt die Ernte als Beute. Details: [`items.md`](items.md) „Stapeln“.

**Minispiel (wie die Ring-Parade im Kampf):** Vollbild vor dem abgedunkelten Bild des Rastplatzes, der Baum oder Fels steht in der Mitte. Ein heller Ring zieht sich in 1,1 s auf den **goldenen Zielring** an der Kerbe zusammen; Leertaste, wenn sie sich treffen. Abweichung ≤ 60 ms = **Perfect**, ≤ 150 ms = **Good**, sonst **Glancing blow** (zählt nicht). Jeder Treffer macht den nächsten Ring 10 % schneller. Läuft der Ring zweimal ohne Schlag durch, wartet das Spiel („Space · Ready when you are“); das zählt nicht als Schlag. **Kraft** über 2 macht das Perfekt-Fenster je Punkt 10 ms breiter (höchstens +30 ms).

| Werkzeug-Stufe | Treffer je Baum oder Fels |
|---|---|
| 1 (Old Hatchet / Old Pick) | 3 |
| 2 (Forester's Axe / Quarry Pick) | 1 |
| 3 (Tempered Axe / Tempered Pick) | keiner: ein Druck, er fällt (zählt als perfekt) |

**Bäume sehen verschieden aus** (Duc 30.10.2026): Steineiche 3 Bilder, Korkeiche 2 (`bilder` in `kochen_daten.KNOTEN`). Das Bild steht je Tag und Platz fest, und gleiche Arten wechseln der Reihe nach durch ihre Bilder (`abbau._knoten_bilder`). Am Ertrag ändert das nichts. Jede Korkeiche hat ihre eigene Schälkante (`BAEUME` in `werkzeuge/kork_rinde_bild.py`).

**Ertrag je Knoten:** Steineiche 3 Timber, **Korkeiche 2 Cork**, Granitfels 2 Granite, Schieferfels 2 Slate. **Die Korkeiche wird nicht gefällt** (Duc 30.10.2026): Beim letzten Hieb löst sich die Rinde am Stück und fällt am Stamm zusammen, gleichzeitig erscheint der Ertrag. Der Baum bleibt rostrot stehen. Holz gibt es nur von der Steineiche. Ton `abbau_rinde_faellt`; die beiden Baumbilder sind deckungsgleich aus demselben Bild gerechnet (`werkzeuge/kork_rinde_bild.py`). Ist der **letzte** Schlag perfekt, gibt es +1 auf den ersten Rohstoff („Clean finish“). Bei Erfolg kippt der Baum mit Knacken und Krachen bzw. bricht der Fels in zwei Hälften, Staub steigt auf, der Ertrag schwebt nach oben. Am Ende kommt eine Karte mit der Summe; zurück ans Feuer mit Leertaste oder Esc (geht jederzeit, ohne Verlust).

Töne (ElevenLabs, je 2–3 Varianten im Wechsel): `abbau_axt`, `abbau_baum_faellt`, `abbau_rinde_faellt`, `abbau_hacke`, `abbau_stein_bricht`, `abbau_daneben`.

### Petrus Werkstatt (Laden „Petru's Workshop“, ab Tag 2)
Freier Laden (Duc 28.10.: „5a muss ich kaufen, der Arme hat kein Geld“). Reiter **Tools**, seit 28.10. **Sell Fish** und seit 30.10. **Baits**; die Upgrades Line/Reel/Landing Net kommen später dazu. Im Reiter Tools zeigt jede Karte die aktuelle Stufe und die nächste mit Kosten (grün = hast du, rot = fehlt); der Kauf ist „alles oder nichts“.

| Stufe | Axt | Spitzhacke | Kosten |
|---|---|---|---|
| 1 | Old Hatchet | Old Pick | 40 € |
| 2 | Forester's Axe | Quarry Pick | 120 € + 2 Iron + 4 Timber + ein **Northern Pike** (Axt) bzw. eine **Barbel** (Spitzhacke) aus dem Vorrat |
| 3 | Tempered Axe | Tempered Pick | 220 € + 3 Iron + 6 Timber + ein **European Eel** bzw. ein **Zander**; nur wenn **Rosis Werkstatt offen** ist (Flag `werkstatt_offen`, sie härtet den Stahl) und **Vertrauen Petru 3** |

Der Wunschfisch wird in der schlechtesten Qualität genommen, die im Vorrat liegt. Bei jeder Übergabe sagt Petru einen eigenen Satz (`laden.petru.kauf_<werkzeug>_<stufe>.0`), dazu kommen drei Grüße (`laden.petru.gruss.*`). Alle 9 Zeilen haben Turbo-Tags und werden über `Vertonen_EdenRise.bat --praefix laden.petru.` vertont. Die Zahlen sind vorläufig (Mathe am Ende).

**Baits** (Duc 30.10.2026: „dauerhaft, und man kann immer zwischen zwei Varianten je Stufe wählen“): Reiter **Baits** in Petrus Werkstatt (Taste 2, Code `kern/koeder.py`). Drei Stufen, **nie verbraucht**; der **beste gebaute Koeder gilt** automatisch, die niedrigeren bleiben gebaut. Jede Stufe hat **zwei Looks** mit gleicher Wirkung (die sechs abgenommenen Bilder aus `farm/koeder/`). Vor dem Bauen klickt man den Look an, nach dem Bauen lässt er sich **jederzeit und kostenlos umschalten**. Der Look des besten Köders ersetzt den gezeichneten Schwimmer im Angel-Minispiel (`angeln.ansicht().koeder`); ohne Köder liegt der **Standard-Schwimmer** im Wasser: ein Flaschenkorken mit Möwenfeder und blauer Schnur (`koeder_0_4`, Duc 03.11.2026), ohne Bonus. Den gezeichneten CSS-Schwimmer gibt es nur noch als Rückfall, falls kein Bild kommt.

| Stufe | Koeder (Looks) | Kosten | Wirkung |
|---|---|---|---|
| 1 | Cork Float (rot/weiß · grün/weiß) | 30 € + 2 Cork + 1 Timber | goldene Zone **+0,03** |
| 2 | Balsa Float (rote Spitze, cremefarben · rosa Spitze, blau) | 70 € + 2 Cork + **2 Feather** + 1 Iron | Zone **+0,05**, seltenere Fische (+5 Punkte auf Stufe 2, +2 auf Stufe 3, von Stufe 1 abgezogen), Biss **10 % früher** |
| 3 | Wooden Lure (Silbersardine · Rotbarbe) | 130 € + 2 Timber + **3 Feather** + 2 Iron | Zone **+0,07**, seltenere Fische (+9 / +6), Biss **25 % früher** |

Die Zone kommt zu Wahrnehmung und Sammel-Bonus hinzu (`angeln.auswerfen`). Die Seltenheit verschiebt nur die Gewichte 60/30/10 der Fischstufen; der Zufall pro Wurf bleibt derselbe, ohne Köder ändert sich nichts. Alle Zahlen sind vorläufig (Mathe am Ende), bearbeitet werden sie in `werkzeuge/eden_rise/kochen_daten.py` (`KOEDER`).

**Gull Feather** (Rohstoff `feather`, kein Ladenartikel): kommt aus dem **Möwen-Kampf** (Sieg oder Aufgabe der Möwe: **+2**, Zeile „The gull leaves 2 feathers behind“; am Rastplatz in die Tasche) und als **Fundsache am Meer** („Gull Feather“, +1). Fluss und Niederlage geben keine. Zum Bauen reichen 5 Federn für beide Stufen. Petru sagt bei der Übergabe einen eigenen Satz (`laden.petru.kauf_koeder_<stufe>.0`, Turbo-Tags, vertont über `Vertonen_EdenRise.bat --praefix laden.petru.`). Test: `tests/test_koeder.py`; Vorschau: `tests\vorschau_server.py --tag 2 --frei --rohstoffe cork:4,feather:5,iron:3,timber:3 --konto 300`.

**Sell Fish** (Story-Sitzung, gebaut 28.10.2026): Der Reiter erscheint ab dem ersten Fang. Preis = Rohpreis × **50 / 65 / 80 %** je Qualitätsstufe, dazu **+5 % je Vertrauensstufe** bei Petru und der Küchen-Tagesbonus „Ankauf“. Beim ersten Verkauf einer Fischart sagt Petru einen eigenen, vertonten Satz (`laden.petru.fisch_<id>.0`, 20 Zeilen), danach steht er als Notiz im Fisch-Journal. Code: `kern/abbau.py` (`fisch_ansicht`, `fisch_verkaufen`), Daten `kochen_daten.py` (aus `petru_fische.py`). Details und Regeln: [`beute.md`](beute.md) „Fisch entdecken und verkaufen“.

### Fische (20)
**Meer (am Boot):** Sea Bass, Gilt-head Bream, Red Mullet, Scorpionfish, Sardine, Atlantic Salmon, Cuttlefish, Common Octopus, Red Prawn, Spiny Lobster. **Fluss (Rastplätze mit Fluss):** Mediterranean Trout, European Eel, Common Carp, Northern Pike, European Perch, Tench, Barbel, Zander, River Crayfish, River Crab. Jeder Fisch hat ein **Sprite** für das Angel-Minispiel und eine **verarbeitete Rohform** als Haupt-Zutat (z. B. „Trout Fillets, raw“, ★★). **Atlantic Salmon** ersetzt seit 28.10.2026 die Little Tunny (Duc, Story/Petru; Meer, Stufe 2, Rohform „Salmon Fillets, raw“ ★★). Er ist ein Irrgast aus dem Norden; gekaufte „Salmon Steaks, raw“ (★) gibt es weiter bei Nonna.

### Bilder und Töne
`Kochen_Bilder.bat` erzeugt mit Krea 2 plus BEN2-Freistellung die Sprites (15 Tiere: Baby, Männchen, Weibchen, alt Männchen, alt Weibchen je Art; 20 Fische) und die Item-Bilder (20 Rohformen, 7 Tierprodukte). Abnahme: `docs/abnahme/kochen_bilder.html`. Ein Skript warnt, wenn ein Sprite den Bildrand berührt (angeschnitten).

### Dateien
| Datei | Rolle |
|---|---|
| `kern/kuechen.py` | Vorrat, Baukasten, Tagesbonus, Nonnas Laden, Frederico, `fang()` |
| `kern/farm.py` | Garten, Ställe und Stall-Stufen, Tiere, Tageswechsel (Ernte, Produkte, Geburten) |
| `kern/angeln.py` | Angelorte, Sitzung, Wurf (Fisch, Stufe, Drillwerte, Biss), Ergebnis, Journal, Sammelbonus |
| `client/plugins/eden-angeln/` | Angel-Minispiel (Wasserbühne, Biss, Drill, Ergebnis-Karten, Journal) |
| `werkzeuge/angeln_sim.py` | Balance-Simulation der Drillwerte |
| `tests/test_angeln.py` | Orte (Boot, Rastplätze), Bestand und Nachwuchs, Sitzung, Verteilung der Stufen, Wahrnehmung, Sammelbonus |
| `kern/abbau.py` | Quellen je Rastplatz, Bestand und Nachwuchs, Abbau-Sitzung (Schlag, Ertrag), Werkzeuge und Petrus Kauf |
| `client/plugins/eden-abbau/` | Quellen-Chips am Rastplatz, Ring-Minispiel (Fallen, Brechen, Späne), Petrus Werkzeug-Fenster |
| `kern/koeder.py`, `tests/test_koeder.py` | Köder bei Petru: Bauen, Look-Wahl, Wirkung im Angeln, Möwenfedern |
| `tests/test_abbau.py` | Quellen, Stufen 1–3, Ertrag mit Kork, 3 Tage Pause, Kraft, Petru (Geld, Rohstoffe, Wunschfisch, Rosi, Vertrauen) |
| `werkzeuge/abbau_bilder.py` | Sprites (Steineiche, Korkeiche, Granit, Schiefer), Werkzeug-Icons, Kork; Abnahme `docs/abnahme/abbau_bilder.json` |
| `werkzeuge/angeln_bilder.py uebernehmen` | kopiert die gewählten Angel-Hintergründe als `eden_rise_angeln_<platz>.png` |
| Vorschau | `tests\vorschau_server.py --tag 9 --frei --flags kloster_angenommen --ort-weg kl_start,kl_bachufer --werkzeug axe:1,pickaxe:1` |
| `werkzeuge/eden_rise/kochen_daten.py`, `kochen_eden_rise.py` | Daten und Builder → `kuechen.json`, Nonnas Bühne in `laeden.json`, Turbo-Tags |
| `client/plugins/eden-farm/` | Farm-Fenster und Baukasten-Oberfläche |
| `werkzeuge/kochen_bilder.py`, `Kochen_Bilder.bat` | Bilder |
| `Vertonen_EdenRise.bat` | vertont alles, was fehlt, auch Fredericos 8 Sätze (`fred.*`) und Nonnas 5 Ladenzeilen (`laden.nonna.*`); nur diese: `--praefix fred.` bzw. `--praefix laden.nonna.` |
| `tests/test_kuechen.py` | Daten, Vorrat, Baukasten, Wirkpunkte, Nonna, Garten, Tiere |

## Tischszene (⭐1, gebaut 27.10.2026)

Kocht Duc das Lieblingsgericht als **Teller für genau diese Person** und sie isst es zum ersten Mal ganz (Stufe „liebt“), kommt statt der kleinen Meldung eine kurze, vertonte Szene. Jede Figur sieht ihre Szene höchstens einmal.

| Beat | Inhalt | Ton |
|---|---|---|
| 1 | Titelkarte: Gericht · Figur's favourite | Continue |
| 2 | Teller (zwei Fassungen: normal und kritischer Wurf) | Text |
| 3 | Erster Bissen | vertont, Sprite-Gefühl |
| 4 | „Your answer“: Duc sagt in einem Satz, woher das Gericht kommt (nur bei nicht-europäischen Gerichten: Lea, Sophia, Totò, Alva, Rosi, Yasin, Lola) | Text |
| 5 | Erinnerung 1 und 2 | vertont |
| 6 | Folgenkarte: „Favourite dish discovered“ mit den Folgen des Tellers | System |

- **Auslöser:** `handel.kochen_aktion` → `tisch.ausloesen`. Nur Teller für eine Person, nur Stufe „liebt“. Misslingt der Wurf, bleibt es bei „gut“ und die Szene wartet auf den nächsten Versuch (die Figur wird erst bei „liebt“ als gesehen gebucht). Crew-Essen und falsche Gerichte lösen nichts aus.
- **Zustand:** `z["tisch"]` ist nur offen, solange die Szene läuft (Neuladen zeigt sie von vorn); `z["tisch_gesehen"]` merkt die Figuren. Ein Spielstand ohne Szene bekommt keine neuen Schlüssel.
- **Bedienung:** Continue per Klick, Enter, Leertaste oder Pfeil rechts; Skip beendet die Szene sofort. Beides ruft die Aktion `tisch_fertig` (kostet keine Aktion, keine Phase).
- **Profil:** Die erste Erinnerung steht danach als Text der entdeckten Vorliebe im Figurenprofil (nur, wenn die Vorliebe gerade erst durch dieses Gericht entdeckt wurde).
- **Texte:** fest, Englisch, von Duc freigegeben (`docs/abnahme/tischszenen_texte.md`); 42 vertonte Zeilen (3 je Figur), jede mit mindestens einem Turbo-Tag, Tags nie sichtbar. Der Teller und „Your answer“ sind Erzähltext ohne Stimme, weil es für die Erzählerstimme keine Tags gibt.
- **Grund der südostasiatischen Gerichte:** Ducs Eltern sind nach dem Vietnamkrieg geflohen (E-067), Duc kocht, was seine Mutter kochte. Figuren, die das Gericht nicht kennen (Totò, Alva), fragen „WHAT IS THAT?!“. Opa Jack Moore hatte eine vietnamesische Lebensgefährtin (Arbeitsname Linh), Lea ist Vietnam-Fan, Sophia ist mit Linh aufgewachsen (Duc 27.10.).

### Dateien

| Datei | Rolle |
|---|---|
| `kern/tisch.py` | Auslöser, Beats für den Client, Audio-Zeilen, Zustand |
| `module/eden_rise/tisch.json` | Szenentexte (gebaut von `werkzeuge/eden_rise/tisch_eden_rise.py`, nicht von Hand ändern) |
| `module/eden_rise/stimme_tags.json` | Einträge für die 42 Zeilen (Klartext → gesprochen mit Tags) |
| `eden.py` | Aktion `tisch_fertig`, Ansicht `z.tisch`, Audio-Zweig `tisch.<figur>.<0\|1\|2>` in `/api/zeile`, Route für das Plugin |
| `client/plugins/eden-tisch/` | Overlay (Beats, Continue, Skip, Stimme); Einhängen in `zeichnen()` (`client/index.html`) |
| `werkzeuge/eden_rise/vertonen_eden_rise.py` | Schlüssel `tisch.*`; vertont wird über `Vertonen_EdenRise.bat` (alles, was fehlt) |
| `tests/test_tisch.py` | Daten, Auslöser, Grenzen, Beats, Audio-Zeilen (ohne Modell und Netz) |

Texte ändern: Zeile im Builder ändern → `python werkzeuge\eden_rise\tisch_eden_rise.py` → `Vertonen_EdenRise.bat` (neue Hashes, alte Aufnahmen bleiben ungenutzt liegen).

## Offen

- ~~Fisch verkaufen~~ gebaut 28.10. (Reiter „Sell Fish“, siehe Petrus Werkstatt). ~~Köder~~ gebaut 30.10. (Reiter „Baits“). Offen bei Petru: die Upgrades Line/Reel/Landing Net.
- ~~Köder-Looks~~ erledigt 30.10.: je Stufe zwei Looks, jederzeit umschaltbar (statt „fix nach der Wahl“), siehe „Baits“.
- ~~Stapeln~~ **gebaut 28.10.:** Holz, Stein, Kork und Fisch vom Rastplatz liegen bis zur Heimkehr in der Tasche (10 je Platz bzw. 3 je Fischart) und sind bei einer Niederlage Beute wie alles andere. Regeln: [`items.md`](items.md) „Stapeln“.
- **Heimweg von Rastplätzen:** Expeditionen enden heute nur an ihrem Schluss-Frame (`{"expedition": "ende"}`); „heim von jedem Rastplatz“ (orte.md) kommt mit Expeditionen 2.0. Bis dahin trägt man die Ernte bis zum Ende.
- ~~Angel-Hintergründe~~ erledigt 28.10.: alle 20 abgenommen und im Wechsel (siehe Angeln, „Hintergründe wechseln“).
- **Testen:** Bach-Rastplatz mit Werkzeug siehe Dateien (Vorschau); Boot: `tests\vorschau_server.py --tag 3 --frei`.
- **Zutatenliste** von Duc: endgültige Basis-, Haupt- und Akzent-Zutaten samt Bildern ersetzt den Platzhalter (`kochen_daten.py`, `Kochen_Bilder.bat`).
- **Verpatzte Experimente** („lustig statt Strafe“ aus dem Plan vom 27.10.): im Baukasten gibt es kein Scheitern durch falsche Kombination, nur durch den Wurf.
