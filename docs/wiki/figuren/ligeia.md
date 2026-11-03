# Ligeia – die Sirene im Teich

> Kanon-Stand 29.10.2026 · Besitz: Character Design · Quellen: Brain Trust 29.10. (Duc: „Okay Ligeia“; „Waliser ist
> raus“; Stimme IT · 3, neapolitanisch), Flut-Nacht (`ereignisse_grotte.py` fn_teich/fn_perle, `kaempfe_grotte.py` sirene),
> Lea (Margot), Petru (1924)
>
> **Hidden Character.** Im Spiel heißt sie bis zum Geheimnis nur „The Siren“. Ihr Name, ihre Herkunft und der Bogen
> unten sind so gebaut, dass Spieler sie selbst zusammensetzen (Wiki-Kaninchenbau, „hidden gems you probably missed“).
> Sie erklärt ihren Mythos **nie** selbst.

## Kurz
Die letzte der drei Sirenen aus der griechischen Sage. Ihre Schwestern Parthenope und Leukosia sind tot – Parthenope
trieb an Land, und auf ihr wurde Neapel gegründet. Ligeia ist nicht gestorben. Sie schämt sich seit dreitausend Jahren
für eine Stimme, die nur töten kann, und lebt in einem Teich unter der Strand-Grotte von Cala d'Orsu. Sie neckt, sie
ist einsam, und sie glaubt, sie hätte 1924 die Crew der Margot umgebracht. Hat sie nicht.

## Fakten
| | |
|---|---|
| Name | **Ligeia** (griechisch „die mit der hellen Stimme“; sprich *Li-gé-ja*). Spieler sehen den Namen erst über das Geheimnis |
| Herkunft | eine der drei Sirenen (Parthenope, Leukosia, Ligeia). Die Sage sagt, sie stürzten sich ins Meer, als ein Schiff ihren Gesang überstand. Bei Ligeia stimmt das nicht |
| Aussehen | honigblondes nasses Haar wie Seetang, helle grüne Augen, langer smaragdgrüner Fischschwanz, leere Perlenfassung am Lederband. Sprite-Set `sirene_standard`: 52 eigene Posen ohne Beine (`karten_neu/ligeia_sfw_posen.py`, Preset `Yacht_Ligeia`). Die Kampf-Sprites `Siren` zeigen sie seit 30.10. ebenso (`karten_neu/kampf_ligeia.py`) |
| Wohnt | im Teich unter der Strand-Grotte, nur bei Flut erreichbar (`underground_pool_tide`) |
| Die Margot (1924) | altes Segelschiff (Zweimaster) aus Falmouth (Kanon über Lea und Petru). Am Bug eine **Galionsfigur aus Neapel: eine Sirene mit dem Gesicht Parthenopes**. Ligeia sah das Gesicht ihrer toten Schwester und folgte dem Schiff |
| Die Sturmnacht | Die Margot sank in der Bucht. Ligeia sang die Crew in den Schlaf, damit niemand in Panik ins schwarze Wasser sprang. Das Dorf ruderte hinaus (Petrus Großvater), fand die Männer schlafend auf dem Wrack und brachte alle lebend heim. **Ligeia weiß das nicht.** Sie tauchte ab, bevor die Boote kamen, und ließ ihre Perle für die Retter auf dem Wrack |
| Sprache | Englisch mit **neapolitanischem Akzent**. Den Klang hat sie aus dem Golf von Neapel, wo sie jahrhundertelang lebte – neben der Stadt, die auf ihrer toten Schwester steht. Das Englisch selbst hat sie von dreitausend Jahren Seeleuten aufgeschnappt, ein Wort von hier, eins von da, manches klingt altmodisch |
| Anrede | nennt jeden Mann **„sailor“** – seit dreitausend Jahren. Bei Vertrauen 5 sagt sie zum ersten Mal **„Duc“** |
| Fluch | **„Gods“** in der Mehrzahl (“Gods, you're slow.”) – sie stammt aus einer älteren Welt |
| Erkennungssatz | “I've heard every word the sea ever drowned.” |
| Schwäche | Worte. Waffen gehen durch sie hindurch (`untouchable`), nur Reden erreicht sie |

## Stimme
- Ätherisch, hell und alt zugleich, mit neapolitanischem Akzent; im Spiel mit leichtem Hall (`effekte.py`). Referenz:
  ElevenLabs Voice Design, Probe auf Italienisch (`stimmen_design.py` `ligeia_it`, **Probe 3**, Duc 29.10.;
  Abnahme `docs/abnahme/stimmen_ligeia/`), Chatterbox-Datei `Ligeia - ENG.wav`, Katalogname „Ligeia“. Die alte walisische
  Stimme („The Siren“, `stimmen_sirene`, 28.10.) steht im Katalog auf „ersetzt“.
- Neckt gern, fordert heraus, lacht über Gewalt. Sagt „sailor“, wo andere einen Namen sagen würden.
- Unter dem Spott liegt Müdigkeit: Wenn sie ernst wird, „geht der Gesang aus ihrer Stimme“ und sie klingt alt.
- Sagt nie „Siren“, „Homer“, „Odysseus“ oder „sisters“ ausdrücklich. Höchstens Andeutungen: “There were three of us,
  once.”
- Keine walisischen Wörter mehr („cariad“, „Duw“, „isn't it“ sind gestrichen).

So klingt sie:
> “Most of them run when they hear me. The rest of them stay. Forever, mind. Which are you, sailor?”
> “There's a boat at the bottom of the bay. An old sailing ship. She went down in a storm a hundred years ago, and I
> sang her crew to sleep. That's what I do.”

Eigene Gesten (für freie Szenen):
- rests her arms on the edge of the pool like a girl on a windowsill
- hums when she doesn't want to answer
- lets the water rise to her chin when she's hurt
- trails her fingers through the water and watches the rings

## Vertrauen und Geschenke (gebaut 29.10.2026)
Ligeia hat eine **Vertrauensleiste 0–5** (Beziehungsmenü unter „Crew and locals“), aber kein Begehren – sie ist keine
Romanze, nur **eine einzige, wiederholbare Nacht** nach ihrem Ende (Duc 30.10.2026, siehe „Die Nacht der Stimme“). Sie startet auf **1** und erscheint in der Liste, sobald Duc sie in der Flut-Nacht getroffen hat.

**Briefe (Duc 02.11.2026, Texte fertig, nicht gebaut):** Sieben Briefe per Flasche statt Handy, höchstens einer alle paar Tage, nur über Vertrauen, in ihrer alten Art. Duc antwortet mit einem von drei Sätzen, ihre Antwort kommt am nächsten Tag. Die Briefe sind ihr Handy-Topf. Sie sind getrennt von den Favours und von der „Again?“-Flasche (`briefe` in `figurenrahmen.json`). **Kein sichtbares Begehren, keine Stufen, keine Selfies, kein Herz-Ende.** Dazu ein unsichtbarer Wert `waerme.sirene`, der nichts öffnet oder sperrt und nur die Nacht der Stimme färbt: Regie und Zeile auf dem Polaroid am Morgen danach ändern sich in drei Stufen (`nacht_waerme`, Vorschlag).

**Abends und nachts** (Duc 30.10.2026) ist sie am Teich, siehe „Warum sie nicht immer da ist“.

**Das Polaroid (`lg_polaroid`, Pflichtszene):** In der ersten Nacht nach der Grotte will sie Duc besuchen, und Lea erwischt sie
im Tenderdock. Lea macht ein Foto, Ligeia fürchtet um ihre Seele, Lea löscht es und erklärt ihr Fotografie. Sie schenkt ihr ihre
wasserfeste Sofortbildkamera: Sie soll ihre Welt für Lea einfangen. Niemand soll davon wissen. Auslöser ist der Datums-Flag
`ligeia_freund` aus `fn_perle` (Pflicht-Events dürfen seit 30.10. mit `flag_seit` ein Tagesfenster haben).

**Flaschenpost (Favours):** Sie hat kein Handy. Ihre Kette `sirene` kommt ab Tag 8 als Flasche auf die Badeplattform (Events
art `abend`, nur über `_favour_ziehen`), Mechanik wie alle Favours. **Zwei Polaroids** bringt jede Vertrauensstufe 2–5 (`lg_flasche_t2`–`t5`, kommen ohne Würfeln) und der Dank der Kette: eine Szene mit handschriftlicher Zeile darunter und ein Selfie von ihr ohne Kamera, oben ohne wie ihre Sprites (`werkzeuge/sirene_polaroid.py`, Schrift nachträglich statt aus Krea). Inhalte stehen nur im Builder.

**Wo man sie trifft:** Raum `siren_pool` („The pool under the beach grotto (high tide)“, Bild
`eden_rise_siren_pool.png` (mit Felsen)), Zugang erst mit `sirene_fertig`. Sie ist nur **nachts** dort (`ablauf`). Dann
gibt es in der freien Phase **jede Nacht eine Karte „Time with the Siren“**: Sie steht in `freie_zeit_extra` und hat
`frei_immer` – in Nächten, in denen sie da ist, gehört ihr der Nebenfiguren-Platz (`hauptstory.frei_phase`), die
anderen Karten bleiben Romanzen. In dieser Szene kann Duc ihr Geschenke geben (`handel.schenken_npc`, Punkte wie bei
allen Nebenfiguren: liebt +8, mag +4, mag nicht −4). Das Sprachmodell spielt sie mit ihrer Beschreibung, vier eigenen
Gesten und „sailor“; Name, Schwestern, Homer und Sirenen spricht sie nie aus.

| Vertrauen | Was es öffnet | Event (`werkzeuge/eden_rise/ereignisse_ligeia.py`) |
|---|---|---|
| 1 | Ankunft | geskriptet | Nacht, Flut, Duc kommt allein ohne Lampe. Sie sagt „Duc“ und flirtet poetisch. *„You carry a small summer in your hands.“* | ruhig, frontal (neutral), zärtlich |
| 2 | sie summt Duc in den Schlaf: **+1 Energie** (oder er fragt, worum es im Lied geht: mehr Vertrauen, keine Energie) | `lg_lied` *A Lullaby at High Tide* |
| 3 | “There were three of us, once.” – sie schickt Duc zu den **drei Felsen** bei Ebbe | `lg_drei` *Three of Us* |
| 4 | Die Nacht | Modell spielt (`INTIM`, Stufe 3) | Sie will zuerst nur warm werden. Neugierig, langsam, zärtlich, poetisch, fragt vor jedem Schritt. Der Spieler darf die Frage aller stellen: “How does this even work?” Antwort: “You'd be the first to stay awake long enough to find out.” Die Anatomie wird nie geklärt | desire, amusement, embarrassment |
| 5 | Der Ausrutscher | Regieanweisung im `hinweis` | Sie wird zum ersten Mal warm und summt, ohne es zu merken, wie eine Katze schnurrt. Duc schläft auf ihrer Schulter ein, lächelnd, und lebt. Sie erstarrt, Hände vor den Mund: *„Gods. Gods, I'm sorry“*, dann lacht sie zum ersten Mal ohne Bitterkeit. **Dann die Ebbe:** Sie müsste gehen und bleibt, weil sie nicht loslassen will. Sie schafft es gerade noch | Hände vor dem Mund, dann lachend |

Die Stufen-Events haben art „abend“: Sie kommen in der Nacht (Vorrang vor Zufall, höchstens ein Abend-Event am Tag) und
ersetzen die freie Phase. Jede Stufe kommt nur einmal.

**Geschenke** (Wirkung bleibt geheim, wie bei allen):

| Reaktion | Items | Warum |
|---|---|---|
| liebt | Underlined Book of Poems, Duc's Poem about the Sea, Alva's Rose, Bouquet from the Macchia | “I'm starving for a good word” – und Dinge vom Land, das sie nie betritt |
| mag | Pink Pearl on a Fine Chain, Spiral Shell with the Sea Inside, Green Sea Glass, Pineapple-Sticker Ukulele, Fishermen's Aniseed Canistrelli | die Perle als Echo, Musik, das Meer, Fischerbrot |
| hasst | Night-Dive Torch, Solar Fairy Lights, Tourist's Red Pocket Knife, Goldfish in a Water Bag | “Don't go the way the lamps go”; Stahl; ein gefangener Fisch |
| zu viel | alle Intim-Geschenke | dreitausend Jahre alt und keine Romanze |

## Die Nacht der Stimme (Duc 30.10.2026, Entwurf, noch nicht gebaut)

Vorbild ist die Bären-Szene mit Halsin (Baldur's Gate 3): Mitten in der Nähe bricht die Natur der Figur durch, es ist
peinlich, komisch und danach zärtlich. Bei Ligeia ist diese Natur ihre **Stimme**. Sie hat 3000 Jahre geglaubt, sie könne
nur töten. Sie weiß jetzt, dass sie die Margot nur in den Schlaf gesungen hat (`sirene_frei`), aber **wissen ist nicht
glauben**. In der Nacht fängt sie ohne es zu merken an zu summen. Duc wird schwer, schläft ein und lebt. Sie erschrickt,
dann lacht sie zum ersten Mal ohne Bitterkeit. Die Szene ist Gag und Beweis zugleich.

**Was sie sich wünscht (Duc 30.10.2026):** Sie ist seit 3000 Jahren einsam und **kalt** („Cold, I know. Everything down here
is.“, `lg_perle`). Sie sehnt sich nach der Wärme eines Mannes, erst danach kommt das Begehren, und es überrascht sie selbst.

**Sie flirtet poetisch (Duc 30.10.2026, ersetzt das plumpe Flirten):** so wie ihre Polaroid-Zeilen, uralt und ungeübt im Berühren,
aber nie albern:
> “The tide has touched every shore I know. I would like, once, to be the shore.”
> “You carry a small summer in your hands. Hold still, let me learn it.”
> “I have sung ten thousand men to sleep. I would like one to stay awake for me.”
> “Stay until the moon is tired. She is very old, so it takes a while.”

**Aufbau (Duc 30.10.2026, Entwurf):** Wer Vertrauen 5 gewählt hat, bekommt **zwei geskriptete Nachtszenen**. Sie kommen von
selbst, sobald er den Tag beendet. Beide sind romantisch und zärtlich, nichts passiert sofort.
1. **Erste Nacht:** Reden, Hände, Wärme. Sie summt, Duc schläft ein. Sie bleibt, bis das Wasser geht. Am Ende: “Please come back.”
   und der Hinweis, etwas zu nehmen, um wach zu bleiben.
2. **Mini-Mission 1:** Die Energie-Leiste wird einmalig auf **5** erweitert. Ohne **+5** aus Energie-Items startet die zweite Nacht nicht.
3. **Zweite Nacht:** Der Anfang ist geskriptet, **danach chattet der Spieler frei mit ihr** (`INTIM`, Modell spielt) und entscheidet
   selbst, wie die Nacht endet. Am Morgen danach: ein wertvoller Schatz, **Modul Stufe 2 für den Skill Reden, +50 %** (Modul
   noch anzulegen, Zahl vorläufig, „Mathe am Ende“). Wieder: “Please come back.”
4. **Mini-Mission 2:** Die Leiste wird einmalig auf **10** erweitert. Jede weitere Nacht braucht **+10**, sonst startet sie nicht.

**Energie-Items für die Mini-Missionen (Duc 30.10.2026, Entwurf):** Sie tauchen **zufällig über das Spiel verteilt** auf, jedes wirkt nur
einmal pro Nacht. Holm's Black Thermos (+2), Nonna's Chinotto Cordial (+2), Rosi's Engine-Room Brew (+3, kostet 1 Moral), Totò's
"Vitamin" Tablets (+3), Bà Tư's Bitter Melon Tea (+2), dazu Sandrus türkischer Kaffee aus Marokko (Wert beim Bau). Daneben bleiben
Double Espresso und Lola's Energy Bar (je +1). Item-Texte nach der Item-Regel beim Bau; die Zahlen sind vorläufig.

**Spuren vorher:** Warme Geschenke bedeuten ihr mehr als Perlen (Thermoskanne, Wärmflasche, Lolas Suppe; sie hält sie, bis sie
kalt sind). Stufe 2: “What does a fire feel like? Not the light. I know the light.” Stufe 3: Sie legt die Hand auf den Stein,
auf dem Duc gesessen hat. Stufe 4: Sie zieht die Hand nicht mehr zurück. Dazu ein Polaroid: ein Lagerfeuer, von weit draußen im
Wasser fotografiert. Das sind Vorgaben für den Bau, gebaut ist davon nichts.

**Regeln:** keine Romanze, kein Begehren, keine Selfies, keine Eifersucht, kein Herz-Ende (wie Jana und Megan). Eine
Nacht, danach wiederholbar. Intim-Liste fest auf **Stufe 3** (Küssen, Streicheln, Ausziehen, Massage). Ligeia lässt
Duc nur zu, wenn er allein und ohne Lampe kommt (siehe „Warum sie nicht immer da ist“).

| # | Beat | Art | Inhalt | Ton / Sprite |
|---|---|---|---|---|
| 1 | Ankunft | geskriptet | Nacht, Flut, Duc kommt allein ohne Lampe. Sie neckt nicht. Hände im Wasser, sie sagt „Duc“. *„You came without the lamp. Good.“* | ruhig, frontal (neutral) |
| 2 | Ihr Bekenntnis | geskriptet | *„I know what my voice does now. I just don't believe it yet.“* Sie bittet: Wenn sie summt, soll er gehen. | ernst, müde, kein Spott |
| 3 | Die Wahl | geskriptet | **Hand nehmen** → Nacht (EN −1, Vertrauen +6, `ligeia_nacht`). **Nur reden und bleiben** → Vertrauen +8, `ligeia_nacht`, sie summt ihm absichtlich ein Lied. **Nicht heute** → Vertrauen +4, kommt wieder. Jede Antwort lässt ein Nein zu | |
| 4 | Die Nacht | Modell spielt (`INTIM`, Stufe 3) | Sie hat 3000 Jahre Liebe vom Wasser aus beobachtet und nie berührt. Neugierig, langsam, ein bisschen gierig, witzig über ihren Schwanz, fragt vor jedem Schritt. Beim zärtlichsten Punkt fängt sie ohne es zu merken an zu summen | desire, amusement |
| 5 | Der Ausrutscher | Regieanweisung im `hinweis` | Das Wasser antwortet, Duc wird schwer und schläft auf ihrer Schulter ein, lächelnd. Sie erstarrt, Hände vor den Mund: *„Gods. Gods, I'm sorry. Three thousand years and I– you're alive. You're snoring.“* Dann lacht sie, richtig | Pose „summt“, danach „Hände vor dem Mund“ (embarrassment, amusement) |
| 6 | Der Morgen danach | geskriptet, am nächsten Morgen | Duc wacht allein auf, der Stein neben ihm ist noch warm, Kratzspuren führen zum Wasser. Auf der Badeplattform eine Flasche mit Polaroid: Duc schläft auf dem Felsen, darunter ein kleines Gedicht in ihrer Handschrift. Oktopus-Arm am Rand | |
| 7 | Reaktion | geskriptet | Beim Frühstück sagt Lea ahnungslos: *„Fish can't make their own heat, you know. They just take it from whatever they're touching.“* Duc verschluckt sich. Petru legt ihm wortlos ein trockenes Handtuch hin | Lea, Petru |

**Wiederholung** (wie Alva und Jana, `lg_nacht_wieder`): Sie hat kein Handy und kann den Teich nicht verlassen. Statt der
Handy-Nachricht kommt eine **Flasche** mit einem Polaroid und einem Wort darunter: *„Again?“* Das ist Janas Zeile, die
Ligeia nicht kennt. Bedingungen: `ligeia_nacht`, Vertrauen 5, nachts. Der Ort ist fest `siren_pool` (kein `ort_waehlen`, sie
ist ans Wasser gebunden). Zwei Antworten: hingehen (Intim, Stufe 3) oder eine leere Flasche zurückschicken (Vertrauen +4).
Die Regieanweisung ändert sich: Sie kennt Ducs Müdigkeit jetzt und summt **absichtlich** leise, wenn er nicht einschlafen
soll, und verliert die Wette trotzdem meistens (Running Gag: Duc schläft jedes Mal ein, die Anatomie-Frage bleibt offen). **Wirkpunkt:** Wer bei ihr einschläft, wacht ausgeruht auf
(**+1 Energie**, wie ihr Wiegenlied T2; Zahl vorläufig, „Mathe am Ende“). Ein Abkühlfenster von 2 Tagen (Flag mit Datum)
verhindert, dass es zur Energiequelle wird.

**Technische Punkte (Stand der Prüfung 30.10.):**
- Der Raum `siren_pool` hat `privat=3`, die Intim-Liste braucht `PRIVAT_AB = 4` (`kern/gesten.py`). Er muss auf 4.
- `sirene_frei` gibt es noch nicht im Code; es gehört zum Tauchgang und zur Namens-Szene in Woche 3. Bis dahin lässt sich
  die Nacht nur mit gesetztem Flag testen.
- Die Intim-Szene spielt das Sprachmodell. Der Ausrutscher ist darum eine Regieanweisung, keine Garantie; der Morgen danach
  (Beat 6) ist die geskriptete Absicherung des Gags.
- Fenster: ab `sirene_frei` bis Tag 35 (das Spiel endet nach 5 Wochen).
- Neu zu machen: 6–8 Sprites für Ligeia (Pose „summt“, „Hände vor dem Mund“, „Hände im Wasser, schüchtern“, „lehnt sich
  vor“, „lacht im Wasser“, „am Felsrand, Haar im Wasser“, „zärtlich lächelnd“), **ein** Polaroid-Bild von Duc im Schlaf
  (Oktopus-Arm am Rand, nachträglich eingesetzt), ein kurzes Hall-Summen als SFX. Alle Bilder gehen vorher über die Abnahme-Seite.
- Stimme: jede Zeile mit mindestens einem Turbo-Tag (Helfer `G()` in `ereignisse_ligeia.py`), nie sichtbar.

## Warum sie nicht immer da ist (Duc 30.10.2026)

Duc trifft sie nur spät am Tag und nur, wenn er allein und ruhig kommt. Gebaut ist bisher die Phase Nacht. Dafür gibt es zwei Gründe:

- **Die Flut.** Bei Ebbe verliert der Teich die Verbindung zum Meer. Ligeia geht, bevor das Wasser geht: Wer dort festsitzt, liegt ohne Wasser auf dem Stein. Tagsüber ist sie draußen bei der Margot. Darum ist der Teich am Tag nur ein Loch im Fels.
- **Stahl und Lärm.** Schreie und Eisen tragen weit durchs Wasser. Wer sich durch die Gänge kämpft, findet den Teich leer (`fn_teich_leer`), sie summt höchstens zwei Töne aus der Ferne. Sie zeigt sich nur dem, der die Felsstufen allein herunterkommt und die Lampe ausmacht (`lg_lied`). Das passt zu „Don't go the way the lamps go“ und dazu, dass sie Lampen und Stahl hasst.

Spieler bekommen das nie als Erklärung. Sie merken es selbst, und Ligeia sagt es höchstens einmal nebenbei.

## Beziehungen
Petru (sein Großvater rettete die Crew, die sie für tot hält – Petru ist ihr Schlüssel) · Lea (Opa Jack suchte die
Margot; Seite 40 ihres Kartenbuchs: “She sings at the pool when the tide is in”; fotografiert die drei Felsen) · Siri
(summt nachts eine Melodie, die sie nicht kennen kann) · Lola (sieht in Akt 1 das leuchtende Meer).

## Die Spur (Geheimnisse, verdeckt)
Keins davon ist Pflicht. Zusammen ergeben sie Name, Herkunft und Ende. Jeder Fund schreibt einen **Codex-Eintrag**
(Folge `codex`), so dass Spieler die Teile im Codex nebeneinander sehen. (Eine eigene Codex-Seite „The Siren“ mit
sichtbaren Lücken ist noch offen.)

| # | Fundstelle | Was man findet | Wann |
|---|---|---|---|
| 1 | Petru, abends in der Werkstatt (`lg_petru_1924`) | seine Zeile über 1924: die Crew lag schlafend auf dem Wrack und **sang im Schlaf** | ab `sirene_fertig`, nicht bei kaltem Petru (Weg B) |
| 2 | Petrus Seekiste (`lg_seekiste`) | ein Kästchen mit einer Mulde, die **Perle fehlt** (Großvater: “she left it on the wreck for us”); die Perle ist eines Nachts verschwunden | nach #1, ab Vertrauen Petru 3 oder Ligeia 4 |
| 3 | Tauchgang, Wrack der Margot | die **Galionsfigur**: eine Sirene, darunter eingeschnitzt „PARTHENOPE – NAPOLI“, ins Holz gekratzt „Ligeia“ | Woche 3 |
| 4 | der Teich | „Ligeia“ im Freitext zu ihr sagen löst ihre Namens-Szene aus | nach #3 und Vertrauen 5 |
| 5 | Siri, nachts auf dem Solar-Deck (`lg_siri_lied`) | summt ein Lied, das sie nie gelernt hat (gemeint: **„Fenesta ca lucive“**, neapolitanisches Klagelied, gemeinfrei; Klavier-Schnipsel als SFX offen) | Tag 9–21 |
| 6 | Lola, nachts in der Kombüse (`lg_lola_meer`) | das Meer leuchtet blau, und Lola hört Summen | Tag 2–6 (Tag 1 ist die Party) |
| 7 | Lea mit einem Foto (`lg_felsen`) | drei Felsen vor der Grotte bei Ebbe; auf zweien „PARTHENOPE“ und „LEUKOSIA“, der dritte ist leer | nach T3 (Ligeia 3); ein eigenes Felsen-Bild ist offen |
| + | Petru hört ihren Gesang | “That's a lament. Someone's mourning.” – er kennt das korsische *voceru* | bei #1 |

## Bogen
- **Flut-Nacht (gebaut, Tag 11–21):** Rede-Kampf am Teich, sie erzählt vom Wrack und gibt den **Saphir**. Flags
  `sirene_fertig`, `sirene_weg`.
- **Nächte am Teich (gebaut 29.10.):** „Time with the Siren“, Geschenke, Stufen T2–T4 (siehe oben). Test
  `tests/test_ligeia.py`.
- **Woche 3, Tauchgang:** sie ist nah (“Don't go the way the lamps go”); an der Galionsfigur findet Duc ihren Namen.
- **Ihr Ende am Teich (`sirene_frei`):** Duc nennt sie beim Namen und erzählt ihr, was Petrus Großvater gesehen hat.
  Sie hat nicht getötet. Zum ersten Mal singt sie, um zu retten – bei der **Belagerung (Tag 21)** hilft sie.
- **Die Nacht der Stimme (Entwurf 30.10., nach `sirene_frei`, Fenster bis Tag 35):** eine wiederholbare Nacht, in der sie
  im Moment der Nähe zu summen beginnt und Duc einschläft. Siehe oben.
- Ohne die Spur bleibt sie „The Siren“, und das Spiel endet trotzdem rund. Wer sie findet, hat etwas, das andere nie
  sehen.

## Offen (Klärungsliste)
- Bei der Belagerung singt sie die Piraten am Strand für 2 Runden in den Schlaf, Roboter bleiben immun. Danach verschwindet sie erschöpft und wünscht Duc noch einmal alles Gute (Duc 01.11.2026, [`belagerung.md`](../welt/belagerung.md)).
- Die Galionsfigur ist ein Quest-Item: Duc bringt sie ihr und nennt ihren Namen (`sirene_frei`), danach steht sie am Eingang des Schutzgebiets (Duc 01.11.2026).
- Bilder der Galionsfigur und der drei Felsen fehlen noch.
